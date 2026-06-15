#!/usr/bin/env python3
"""okf_mcp_server.py — self-hostable MCP server over an OKF bundle.

The access layer for enterprise cross-session / cross-agent use (see
docs/ENTERPRISE.md). Reads are instant; writes are **PR-gated** — propose_change
never touches `main`, it pushes a branch and (optionally) opens a PR on the
internal git server. Works air-gapped.

Tools exposed to agents:
  okf_search(query, k, type)            — hybrid (BM25 + semantic) ranked retrieval
  okf_get_concept(concept_id)           — frontmatter + body of one concept
  okf_list_concepts(prefix)             — id/type/description listing
  okf_read_index(path)                  — an index.md (progressive disclosure)
  okf_propose_change(...)               — PR-gated write (branch + PR); the default model
  okf_acquire_lease / renew / release / list_leases  — advisory lease coordination
  okf_commit_concept(..., token)        — lease-gated DIRECT write (OKF_WRITE_MODE=lease only)

Transport (env OKF_MCP_TRANSPORT): stdio (default) | streamable-http | sse
Config (env):
  OKF_REPO_DIR     git repo root (default: parent of this file's dir)
  OKF_BUNDLE       bundle dir     (default: <repo>/wiki)
  OKF_BASE_BRANCH  default: main
  OKF_WRITE_MODE   "pr" (default, PR-gated) | "lease" (enables okf_commit_concept)
  OKF_AGENT_ID     this server's default agent identity for leases (real identity at the proxy)
  OKF_LEASE_DIR    where leases live (default: $TMPDIR/okf-leases)
  OKF_READONLY     "1" disables all writes (reader role)
  OKF_GIT_PUSH     "1" (default) push branch to origin; "0" local-only
  OKF_GITEA_API / OKF_GITEA_TOKEN / OKF_GITEA_OWNER / OKF_GITEA_REPO
                   if set, propose_change opens a PR via the Gitea API
  OKF_MCP_HOST / OKF_MCP_PORT  for http/sse transports (default 0.0.0.0:8765)
Role/auth (reader/proposer/curator) and TLS/mTLS/OIDC are enforced at the
reverse proxy in front of this server — see docs/ENTERPRISE.md.
"""
import importlib.util
import json
import os
import re
import subprocess
import threading
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.abspath(os.getenv("OKF_REPO_DIR", os.path.join(HERE, "..")))
BUNDLE = os.path.abspath(os.getenv("OKF_BUNDLE", os.path.join(REPO_DIR, "wiki")))
BASE_BRANCH = os.getenv("OKF_BASE_BRANCH", "main")
READONLY = os.getenv("OKF_READONLY") == "1"
WRITE_MODE = os.getenv("OKF_WRITE_MODE", "pr")        # "pr" (PR-gated) | "lease" (lease-gated direct write)
DEFAULT_OWNER = os.getenv("OKF_AGENT_ID", "agent")    # agent identity (real identity enforced at the proxy)
INDEX_PATH = os.path.join(BUNDLE, ".okf-index.json")
RESERVED = {"index.md", "log.md"}
_git_lock = threading.Lock()                          # serialize git mutations on this single-authority server


def _load(modname, filename):
    spec = importlib.util.spec_from_file_location(modname, os.path.join(HERE, "..", "tools", filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

okfindex = _load("okfindex", "okf-index.py")          # reuse build/query/parse_frontmatter
okfsearch = _load("okfsearch", "okf-search.py")        # hybrid BM25 + semantic (RRF), graceful fallback
okflease = _load("okflease", "okf-lease.py")           # advisory lease/lock for concurrent writes


def ensure_index():
    if not os.path.exists(INDEX_PATH):
        okfindex.build(BUNDLE, INDEX_PATH)
    return json.load(open(INDEX_PATH, encoding="utf-8"))


def safe_concept_path(concept_id):
    cid = concept_id.strip().lstrip("/")
    if cid.endswith(".md"):
        cid = cid[:-3]
    if ".." in cid.split("/") or os.path.basename(cid) + ".md" in RESERVED or not re.match(r"^[\w\-/]+$", cid):
        raise ValueError(f"invalid concept_id: {concept_id!r}")
    return cid, os.path.join(BUNDLE, cid + ".md")


def to_frontmatter(meta):
    if "type" not in meta or not str(meta["type"]).strip():
        raise ValueError("frontmatter must include a non-empty `type`")
    out = ["---"]
    for k, v in meta.items():
        if isinstance(v, (list, tuple)):
            out.append(f"{k}:")
            out += [f"- {i}" for i in v]
        else:
            out.append(f"{k}: {v}")
    out.append("---")
    return "\n".join(out) + "\n"


def git(*args):
    return subprocess.run(["git", "-C", REPO_DIR, *args], capture_output=True, text=True, check=True).stdout.strip()


def open_pr(branch, title, body):
    api, token = os.getenv("OKF_GITEA_API"), os.getenv("OKF_GITEA_TOKEN")
    owner, repo = os.getenv("OKF_GITEA_OWNER"), os.getenv("OKF_GITEA_REPO")
    if not all([api, token, owner, repo]):
        return None
    req = urllib.request.Request(
        f"{api.rstrip('/')}/repos/{owner}/{repo}/pulls",
        data=json.dumps({"head": branch, "base": BASE_BRANCH, "title": title, "body": body}).encode(),
        headers={"Authorization": f"token {token}", "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("html_url")


try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    raise SystemExit("Missing dependency: pip install mcp  (see server/requirements.txt)")

mcp = FastMCP("okf-knowledge-base", host=os.getenv("OKF_MCP_HOST", "0.0.0.0"),
              port=int(os.getenv("OKF_MCP_PORT", "8765")))


@mcp.tool()
def okf_search(query: str, k: int = 8, type: str = "") -> dict:
    """Search the knowledge base (hybrid BM25 + semantic, RRF-fused; falls back to BM25 if no
    embeddings / Ollama). Returns {mode, results:[{id,type,description,rrf_score}]}."""
    ensure_index()
    results, mode = okfsearch.search(BUNDLE, query, k=k, type_filter=type or None)
    return {"mode": mode, "results": results}


@mcp.tool()
def okf_get_concept(concept_id: str) -> dict:
    """Return the frontmatter and markdown body of one concept by its Concept ID (e.g. 'tables/orders')."""
    cid, path = safe_concept_path(concept_id)
    if not os.path.exists(path):
        return {"error": "not found", "concept_id": cid}
    meta, body = okfindex.parse_frontmatter(open(path, encoding="utf-8").read())
    return {"concept_id": cid, "frontmatter": meta, "body": body}


@mcp.tool()
def okf_list_concepts(prefix: str = "") -> list:
    """List concept ids (optionally under a path prefix) with type and description."""
    return [{"id": d["id"], "type": d["type"], "description": d["description"]}
            for d in ensure_index()["docs"] if d["id"].startswith(prefix)]


@mcp.tool()
def okf_read_index(path: str = "") -> str:
    """Read an index.md for progressive disclosure. path='' = bundle root; else a subdir like 'tables'."""
    target = os.path.join(BUNDLE, path, "index.md")
    return open(target, encoding="utf-8").read() if os.path.exists(target) else f"(no index.md at {path or '/'})"


@mcp.tool()
def okf_propose_change(concept_id: str, frontmatter: dict, body: str, summary: str) -> dict:
    """Propose a new/updated concept. Creates a branch + PR (never writes main). Returns branch & PR url."""
    if READONLY:
        return {"error": "server is read-only (reader role); proposals disabled"}
    cid, path = safe_concept_path(concept_id)
    content = to_frontmatter(dict(frontmatter)) + "\n" + body.rstrip() + "\n"
    push = os.getenv("OKF_GIT_PUSH", "1") == "1"
    with _git_lock:
        branch = "okf/" + re.sub(r"[^\w\-]+", "-", cid) + "-" + git("rev-parse", "--short", "HEAD")[:7]
        if push:
            git("fetch", "origin", BASE_BRANCH)
        git("checkout", "-B", branch, BASE_BRANCH)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        git("add", path)
        git("commit", "-m", f"okf: {summary}\n\nConcept: {cid}")
        pr_url = None
        if push:
            git("push", "-u", "origin", branch, "--force-with-lease")
            pr_url = open_pr(branch, f"OKF: {summary}", f"Proposed change to `{cid}`.\n\n{summary}")
        git("checkout", BASE_BRANCH)
    return {"concept_id": cid, "branch": branch, "pr_url": pr_url,
            "note": "PR opened — pending CI (okf-validate) + review/merge" if pr_url
            else "branch committed locally; set OKF_GITEA_* to auto-open a PR"}


# ── Lease/lock concurrency (alternative to PR-gated writes) ──────────────────────
# Advisory, short-TTL leases so two agents don't edit the SAME concept at once.
# Always available for coordination; the lease-GATED direct write below is enabled
# only when OKF_WRITE_MODE=lease.

@mcp.tool()
def okf_acquire_lease(concept_id: str, ttl_seconds: int = 300, owner: str = "") -> dict:
    """Acquire an advisory lease on a concept before editing it. Returns {token, expires_at}
    or {error, held_by} if another agent holds a live lease."""
    try:
        return okflease.acquire(concept_id, owner or DEFAULT_OWNER, ttl=ttl_seconds)
    except okflease.Locked as e:
        return {"error": "locked", "held_by": e.holder}
    except ValueError as e:
        return {"error": str(e)}


@mcp.tool()
def okf_renew_lease(concept_id: str, token: str, ttl_seconds: int = 300, owner: str = "") -> dict:
    """Extend a lease you hold (keep working). Fails if you are not the holder."""
    try:
        return okflease.renew(concept_id, owner or DEFAULT_OWNER, token, ttl=ttl_seconds)
    except PermissionError as e:
        return {"error": str(e)}


@mcp.tool()
def okf_release_lease(concept_id: str, token: str, owner: str = "") -> dict:
    """Release a lease when done editing a concept."""
    try:
        return okflease.release(concept_id, owner or DEFAULT_OWNER, token)
    except PermissionError as e:
        return {"error": str(e)}


@mcp.tool()
def okf_list_leases() -> list:
    """List currently-held (non-expired) leases: concept, owner, seconds-to-expiry."""
    return okflease.list_active()


@mcp.tool()
def okf_commit_concept(concept_id: str, frontmatter: dict, body: str, token: str,
                       summary: str, owner: str = "") -> dict:
    """Lease-gated DIRECT write to the shared branch (OKF_WRITE_MODE=lease only). Requires a valid
    lease token for the concept. Use okf_propose_change instead when the server is PR-gated."""
    if READONLY:
        return {"error": "server is read-only"}
    if WRITE_MODE != "lease":
        return {"error": "server WRITE_MODE is 'pr' — use okf_propose_change (branch + PR)"}
    cid, path = safe_concept_path(concept_id)
    try:
        okflease._verify(cid, owner or DEFAULT_OWNER, token)          # must hold the lease
    except PermissionError as e:
        return {"error": str(e)}
    content = to_frontmatter(dict(frontmatter)) + "\n" + body.rstrip() + "\n"
    push = os.getenv("OKF_GIT_PUSH", "1") == "1"
    with _git_lock:
        git("checkout", BASE_BRANCH)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        git("add", path)
        git("commit", "-m", f"okf: {summary}\n\nConcept: {cid}")
        if push:
            git("pull", "--rebase", "origin", BASE_BRANCH)           # absorb others' (different-file) commits
            git("push", "origin", BASE_BRANCH)
    return {"concept_id": cid, "committed": True, "branch": BASE_BRANCH,
            "note": "lease still held — call okf_release_lease when you're done with this concept"}


if __name__ == "__main__":
    ensure_index()
    transport = os.getenv("OKF_MCP_TRANSPORT", "stdio")
    mcp.run(transport=transport)

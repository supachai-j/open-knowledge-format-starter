# Enterprise Self-Hosted Deployment

How to run this OKF knowledge base **on-prem**, shared **across sessions and across agent
teams**, fully **internal** (works air-gapped). No SaaS, no external model/API required.

## The one idea

> **Git is the source of truth. An internal MCP server is the universal access layer.**
> Every session and every agent — on any framework, any model — talks to the *same* internal
> MCP endpoint. Git history *is* the cross-session memory; the MCP server is how live agents
> reach it and propose changes. Reads are instant; writes are **PR-gated** for audit & safety.

```
                          ┌─────────────────────────────────────────────┐
                          │              INTERNAL NETWORK                 │
                          │                                               │
  Agent team A ─┐         │   ┌────────────┐      pull/webhook            │
  (Claude Code) │         │   │  Git server │◄──────────────┐            │
                │  MCP    │   │ (Gitea/     │               │            │
  Agent team B ─┼────────►│   │  GitLab CE) │   ┌───────────┴─────────┐  │
  (any agent)   │ (HTTP/  │   │  = OKF repo │   │   OKF MCP server    │  │
                │  SSE +  │   └─────┬───────┘   │  read · search ·    │  │
  CI / cron   ──┘  token/ │         │ PR/MR     │  propose_change     │  │
                   mTLS)  │         ▼           │  (FastMCP, stdio+   │  │
                          │   ┌────────────┐    │   streamable-HTTP)  │  │
                          │   │ CI runner  │    └───────────┬─────────┘  │
                          │   │ okf-validate│               │ builds      │
                          │   │ + viz regen │        ┌──────▼───────┐    │
                          │   └────────────┘        │ search index │    │
                          │                          │ (BM25 +/-    │    │
                          │                          │  local embed)│    │
                          │                          └──────────────┘    │
                          └─────────────────────────────────────────────┘
```

## Components

| # | Component | Self-hosted choice | Role |
|---|-----------|--------------------|------|
| 1 | **Git server** | Gitea (light) or GitLab CE | Durable, versioned **source of truth**. Per-team repos or one monorepo bundle with CODEOWNERS. |
| 2 | **OKF MCP server** | `server/okf_mcp_server.py` (FastMCP) | The access layer. Exposes read/search/propose tools over the bundle to every agent. stdio (local) + streamable-HTTP/SSE (remote internal). |
| 3 | **Search index** | `tools/okf-index.py` (pure-Python BM25; sqlite/embeddings optional) | Sub-second retrieval once the wiki passes ~150 pages. Rebuilt on every change. |
| 4 | **CI conformance gate** | Gitea Actions / GitLab CI runner | Blocks merges of non-conformant bundles; regenerates `wiki/viz.html`. |
| 5 | **Reverse proxy** | Caddy / Traefik / nginx | TLS + auth (token / OIDC / **mTLS**) in front of the MCP HTTP endpoint. |

## Read path (the common case — fast, no locks)

1. Agent calls MCP `okf_search("how is WAU defined")` → BM25 over the index → top-k concept IDs.
2. Agent calls `okf_get_concept("metrics/weekly-active-users")` → frontmatter + body, loaded into context.
3. `okf_read_index()` for progressive disclosure when browsing.

Reads never touch git write paths, so any number of agents/sessions read concurrently with zero contention.

## Write path (PR-gated — default; safe for concurrent teams)

`okf_propose_change(concept_id, frontmatter, body, summary)` does **not** write to `main`. It:

1. Creates a branch `okf/<concept-id>-<short-id>` from `main`.
2. Writes the concept file, commits, pushes to the internal git server.
3. Opens a PR/MR via the git server API (Gitea/GitLab) and returns its URL.
4. CI runs `okf-validate.py` (+ regenerates `viz.html`); a human or **curator agent** reviews & merges.

This gives every enterprise property for free: **audit trail** (git log), **review/diff**, **rollback**
(git revert), **no write conflicts** (merge happens once, in order), and a **quality gate** (CI + review).
Merging `main` triggers a webhook → MCP server pulls → reindexes. Knowledge is now visible to all sessions.

> **Concurrency alternatives** (pick per write-volume; default is PR-gated):
> - **Lease/lock** — high write volume: MCP hands out a short TTL lease per concept/directory so
>   two agents don't edit the same file; still commits to branches. Faster, weaker review.
> - **Append-only proposals + curator** — agents drop proposals into an `inbox/`; a single curator
>   agent batches, reconciles contradictions, and merges. Strongest quality gate; matches our supervised INGEST.

## Cross-session & cross-team semantics

- **Cross-session:** there is no per-session state. A new session connects to the same MCP endpoint
  and `git pull` gives it everything prior sessions wrote. The wiki *compounds*.
- **Cross-team:** two options —
  - *Monorepo bundle* + `CODEOWNERS` per subtree (`tables/` owned by data-eng, `playbooks/` by SRE).
  - *Federated bundles* — one repo per domain/team; the MCP server mounts several and namespaces
    concept IDs by bundle (`sales:tables/orders`). Cross-bundle links stay relative within a bundle.

## Access control & security (internal)

- **Git layer:** org/team membership on Gitea/GitLab; branch protection on `main` (require CI + review).
- **MCP layer:** put the HTTP transport behind the reverse proxy with **mTLS** (service-to-service) or
  **OIDC/SSO** (humans) + a bearer token per agent identity. Map identity → role:
  - `reader` → search/get/list only.
  - `proposer` → + `okf_propose_change` (branch/PR only; never direct to `main`).
  - `curator` → may merge (via git server, not MCP).
- **Air-gapped:** `okf-viz.py` already **inlines** Cytoscape + marked from `tools/vendor/` by default, so
  `viz.html` is a true single file that fetches nothing at view time (use `--cdn` only if you prefer CDN).
  Semantic search runs on a **self-hosted** embedding model via Ollama — nothing leaves the network.
- **Secrets/PII:** `raw/` stays out of the bundle (already `.gitignore`d); never put credentials in concepts.

## Scaling

- **< ~150 concepts:** flat `index.md` progressive disclosure is enough; search optional.
- **> ~150:** build the BM25 index (`tools/okf-index.py build`). `okf_search` uses it automatically.
- **Recall not enough? add the semantic layer** — embed concepts with a self-hosted model and let
  `okf-search.py` fuse BM25 + semantic via Reciprocal Rank Fusion:
  ```bash
  ollama pull nomic-embed-text            # one-time, on-prem
  python3 tools/okf-embed.py build        # writes wiki/.okf-embed.json
  python3 tools/okf-search.py "…" -k 8    # mode: hybrid (bm25+semantic, RRF)
  ```
  If embeddings aren't built or Ollama is down, search **automatically falls back to BM25-only** and
  reports the mode — so semantic is a pure opt-in upgrade with no hard dependency.
- **Very large / many teams:** federate bundles, run one MCP server per domain behind one gateway,
  cache the index in memory and rebuild incrementally on webhook.

## Deploy (one VM, internal)

`deploy/docker-compose.yml` brings up the internal stack:

```bash
cd deploy
cp .env.example .env          # set OKF_GIT_REMOTE, tokens, OIDC/mTLS as needed
docker compose up -d          # gitea + okf-mcp + caddy (TLS/auth) + ci runner
```

Point agents at the MCP endpoint:

```jsonc
// Claude Code / any MCP client, internal URL
{ "mcpServers": { "okf": {
    "transport": "http",
    "url": "https://okf.internal.example/mcp",
    "headers": { "Authorization": "Bearer ${OKF_TOKEN}" }
} } }
```

Local/dev (stdio, no network):

```bash
python3 server/okf_mcp_server.py            # stdio transport
# or: OKF_MCP_TRANSPORT=streamable-http OKF_MCP_PORT=8765 python3 server/okf_mcp_server.py
```

## Operational runbook

| Task | Command / action |
|------|------------------|
| Rebuild search index | `python3 tools/okf-index.py build` (CI does this on merge) |
| Rebuild semantic embeddings | `python3 tools/okf-embed.py build` (needs on-prem Ollama; optional) |
| Validate before merge | `python3 tools/okf-validate.py` (CI gate) |
| Regenerate viewer | `python3 tools/okf-viz.py` (CI artifact) |
| Force MCP resync | restart server, or hit the post-merge webhook |
| Audit "who changed WAU" | `git log --follow wiki/metrics/weekly-active-users.md` |
| Roll back bad knowledge | `git revert <sha>` → PR → merge |

## What stays the same as local mode

The bundle, `AGENTS.md` schema, conformance rules, and the `okf` skill are **identical**. Enterprise mode
only adds *where it lives* (internal git), *how agents reach it* (MCP), and *how writes are gated* (PR + CI).
A laptop clone and the enterprise server are the same format — that is the whole point of OKF.
```

#!/usr/bin/env python3
"""okf-embed.py — local semantic embeddings for an OKF bundle (on-prem, air-gap).

Embeds each concept with a **self-hosted** embedding model via Ollama — no external
API, nothing leaves the network. Stores vectors in `<bundle>/.okf-embed.json`.
Pure stdlib (urllib + math). Used by `okf-search.py` for hybrid (BM25 + semantic) search.

Usage:
  python3 tools/okf-embed.py build [bundle] [-o .okf-embed.json]
  python3 tools/okf-embed.py query "how is WAU defined" [--bundle ../wiki] [-k 8]

Config (env):
  OKF_OLLAMA_URL    default http://localhost:11434
  OKF_EMBED_MODEL   default nomic-embed-text
"""
import argparse
import json
import math
import os
import re
import urllib.request

RESERVED = {"index.md", "log.md"}
OLLAMA = os.getenv("OKF_OLLAMA_URL", "http://localhost:11434").rstrip("/")
MODEL = os.getenv("OKF_EMBED_MODEL", "nomic-embed-text")
BODY_CAP = 2000


def parse_frontmatter(text):
    meta, body = {}, text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            block, body = text[3:end], text[end + 4:].lstrip("\n")
            key = None
            for line in block.splitlines():
                if re.match(r"\s*-\s+", line) and key:
                    meta.setdefault(key, [])
                    if isinstance(meta[key], list):
                        meta[key].append(line.split("-", 1)[1].strip().strip("'\""))
                    continue
                m = re.match(r"([A-Za-z0-9_]+)\s*:\s*(.*)$", line)
                if m:
                    key, val = m.group(1), m.group(2).strip()
                    meta[key] = [] if val == "" else (
                        [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
                        if val.startswith("[") and val.endswith("]") else val.strip().strip("'\""))
    return meta, body


class OllamaError(RuntimeError):
    pass


def embed(text):
    """Return an embedding vector via Ollama, or raise OllamaError if unreachable."""
    req = urllib.request.Request(f"{OLLAMA}/api/embeddings",
                                 data=json.dumps({"model": MODEL, "prompt": text}).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.load(r)
        vec = data.get("embedding") or (data.get("embeddings") or [None])[0]
        if not vec:
            raise OllamaError(f"no embedding in response (model {MODEL!r} pulled?)")
        return vec
    except OllamaError:
        raise
    except Exception as e:
        raise OllamaError(f"Ollama unreachable at {OLLAMA} ({e}). Run `ollama pull {MODEL}` and start ollama.")


def concept_text(meta, body):
    tags = meta.get("tags", [])
    tags = [tags] if isinstance(tags, str) else tags
    return "\n".join([meta.get("title", ""), meta.get("description", ""),
                      " ".join(tags), body[:BODY_CAP]]).strip()


def build(bundle, out):
    docs = []
    for root, _, files in os.walk(bundle):
        for fn in files:
            if not fn.endswith(".md") or fn in RESERVED:
                continue
            rel = os.path.relpath(os.path.join(root, fn), bundle).replace(os.sep, "/")
            meta, body = parse_frontmatter(open(os.path.join(root, fn), encoding="utf-8").read())
            docs.append({"id": rel[:-3], "type": meta.get("type", "Concept"),
                         "title": meta.get("title", rel[:-3]), "description": meta.get("description", ""),
                         "vec": embed(concept_text(meta, body))})
    dim = len(docs[0]["vec"]) if docs else 0
    json.dump({"model": MODEL, "dim": dim, "docs": docs}, open(out, "w", encoding="utf-8"))
    print(f"✓ embedded {len(docs)} concepts → {out}  (model={MODEL}, dim={dim})")
    return {"model": MODEL, "dim": dim, "docs": docs}


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1
    nb = math.sqrt(sum(y * y for y in b)) or 1
    return dot / (na * nb)


def query(index, q, k=8, type_filter=None):
    qv = embed(q)
    scored = [(cosine(qv, d["vec"]), d) for d in index["docs"]
              if not type_filter or d["type"] == type_filter]
    scored.sort(key=lambda x: -x[0])
    return [{"id": d["id"], "type": d["type"], "title": d["title"],
             "description": d["description"], "score": round(s, 4)} for s, d in scored[:k]]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    pb = sub.add_parser("build"); pb.add_argument("bundle", nargs="?", default=os.path.join(here, "..", "wiki")); pb.add_argument("-o", "--out")
    pq = sub.add_parser("query"); pq.add_argument("q"); pq.add_argument("--bundle", default=os.path.join(here, "..", "wiki")); pq.add_argument("-i", "--index"); pq.add_argument("-k", type=int, default=8); pq.add_argument("--type")
    a = ap.parse_args()
    try:
        if a.cmd == "build":
            bundle = os.path.abspath(a.bundle)
            build(bundle, a.out or os.path.join(bundle, ".okf-embed.json"))
        else:
            idx_path = a.index or os.path.join(os.path.abspath(a.bundle), ".okf-embed.json")
            if not os.path.exists(idx_path):
                print(f"✗ no embeddings at {idx_path} — run `okf-embed.py build` first"); return 1
            for r in query(json.load(open(idx_path, encoding="utf-8")), a.q, a.k, a.type):
                print(f"  {r['score']:>7}  {r['id']:<40} [{r['type']}]  {r['description']}")
    except OllamaError as e:
        print(f"✗ {e}"); return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

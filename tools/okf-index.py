#!/usr/bin/env python3
"""okf-index.py — build & query a BM25 search index over an OKF bundle.

Pure Python (stdlib only) — no external services, works air-gapped. The MCP
server uses the same module for `okf_search`. For semantic search, fuse these
BM25 results with a local embedding model (e.g. via Ollama) using RRF; this
tool deliberately stays dependency-free.

Usage:
  python3 tools/okf-index.py build [bundle_dir] [-o index.json]
  python3 tools/okf-index.py query "how is WAU defined" [-i index.json] [-k 8] [--type Metric]

Defaults: bundle=../wiki, index=<bundle>/.okf-index.json
"""
import argparse
import json
import math
import os
import re

RESERVED = {"index.md", "log.md"}
TOKEN_RE = re.compile(r"[a-z0-9_]+")
K1, B = 1.5, 0.75
# field boosts: title/tags/description matter more than raw body
FIELD_WEIGHTS = {"title": 3, "tags": 2, "description": 2, "type": 2, "body": 1}


def tokenize(text):
    return TOKEN_RE.findall((text or "").lower())


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
                    if val == "":
                        meta[key] = []
                    elif val.startswith("[") and val.endswith("]"):
                        meta[key] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
                    else:
                        meta[key] = val.strip().strip("'\"")
    return meta, body


def build(bundle, out):
    docs, df = [], {}
    for root, _, files in os.walk(bundle):
        for fn in files:
            if not fn.endswith(".md") or fn in RESERVED:
                continue
            rel = os.path.relpath(os.path.join(root, fn), bundle).replace(os.sep, "/")
            meta, body = parse_frontmatter(open(os.path.join(root, fn), encoding="utf-8").read())
            tags = meta.get("tags", [])
            tags = [tags] if isinstance(tags, str) else tags
            fields = {"title": meta.get("title", ""), "tags": " ".join(tags),
                      "description": meta.get("description", ""), "type": meta.get("type", ""),
                      "body": body}
            tf = {}
            for field, weight in FIELD_WEIGHTS.items():
                for tok in tokenize(fields[field]):
                    tf[tok] = tf.get(tok, 0) + weight
            for tok in tf:
                df[tok] = df.get(tok, 0) + 1
            docs.append({"id": rel[:-3], "type": meta.get("type", "Concept"),
                         "title": meta.get("title", rel[:-3]), "description": meta.get("description", ""),
                         "len": sum(tf.values()), "tf": tf})
    N = len(docs)
    avgdl = (sum(d["len"] for d in docs) / N) if N else 0
    index = {"N": N, "avgdl": avgdl, "df": df, "docs": docs}
    json.dump(index, open(out, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"✓ indexed {N} concepts → {out}  (avgdl={avgdl:.0f}, vocab={len(df)})")
    return index


def query(index, q, k=8, type_filter=None):
    N, avgdl, df = index["N"], index["avgdl"] or 1, index["df"]
    terms = tokenize(q)
    scored = []
    for d in index["docs"]:
        if type_filter and d["type"] != type_filter:
            continue
        s = 0.0
        for t in terms:
            f = d["tf"].get(t)
            if not f:
                continue
            idf = math.log(1 + (N - df.get(t, 0) + 0.5) / (df.get(t, 0) + 0.5))
            s += idf * (f * (K1 + 1)) / (f + K1 * (1 - B + B * d["len"] / avgdl))
        if s > 0:
            scored.append((s, d))
    scored.sort(key=lambda x: -x[0])
    return [{"id": d["id"], "type": d["type"], "title": d["title"],
             "description": d["description"], "score": round(s, 3)} for s, d in scored[:k]]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    pb = sub.add_parser("build"); pb.add_argument("bundle", nargs="?", default=os.path.join(here, "..", "wiki")); pb.add_argument("-o", "--out")
    pq = sub.add_parser("query"); pq.add_argument("q"); pq.add_argument("-i", "--index"); pq.add_argument("-k", type=int, default=8); pq.add_argument("--type"); pq.add_argument("--bundle", default=os.path.join(here, "..", "wiki"))
    a = ap.parse_args()
    if a.cmd == "build":
        bundle = os.path.abspath(a.bundle)
        out = a.out or os.path.join(bundle, ".okf-index.json")
        build(bundle, out)
    else:
        idx_path = a.index or os.path.join(os.path.abspath(a.bundle), ".okf-index.json")
        if not os.path.exists(idx_path):
            print(f"✗ no index at {idx_path} — run `okf-index.py build` first"); return 1
        for r in query(json.load(open(idx_path, encoding="utf-8")), a.q, a.k, a.type):
            print(f"  {r['score']:>6}  {r['id']:<40} [{r['type']}]  {r['description']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

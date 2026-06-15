#!/usr/bin/env python3
"""okf-search.py — hybrid search over an OKF bundle: BM25 ⊕ semantic via RRF.

Fuses lexical (okf-index.py / BM25) and semantic (okf-embed.py / Ollama) rankings
using Reciprocal Rank Fusion. Degrades gracefully: if embeddings aren't built or
Ollama is unreachable, it returns BM25-only and reports the mode. This is the
single search entrypoint the MCP server calls.

Usage:
  python3 tools/okf-search.py "how is WAU defined" [--bundle ../wiki] [-k 8] [--type Metric] [--bm25-only]

RRF: fused(doc) = Σ_signals 1 / (RRF_K + rank).  RRF_K=60 (conventional).
"""
import argparse
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RRF_K = 60
POOL = 50  # how many results to pull from each signal before fusing


def _load(name, filename):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_bm25 = _load("okfindex", "okf-index.py")
_sem = _load("okfembed", "okf-embed.py")


def _rrf(rankings):
    """rankings: list of [ {id,...}, ... ] ordered best-first. Returns fused id->score."""
    fused = {}
    meta = {}
    for ranked in rankings:
        for rank, r in enumerate(ranked):
            fused[r["id"]] = fused.get(r["id"], 0.0) + 1.0 / (RRF_K + rank)
            meta.setdefault(r["id"], r)
    return fused, meta


def search(bundle, query, k=8, type_filter=None, bm25_only=False):
    """Return (results, mode). mode ∈ {'hybrid (bm25+semantic)', 'bm25-only', 'bm25-only (<reason>)'}."""
    bundle = os.path.abspath(bundle)
    idx_path = os.path.join(bundle, ".okf-index.json")
    if not os.path.exists(idx_path):
        _bm25.build(bundle, idx_path)
    bm25_ranked = _bm25.query(json.load(open(idx_path, encoding="utf-8")), query, k=POOL, type_filter=type_filter)

    rankings, mode = [bm25_ranked], "bm25-only"
    emb_path = os.path.join(bundle, ".okf-embed.json")
    if not bm25_only:
        if not os.path.exists(emb_path):
            mode = "bm25-only (no embeddings — run okf-embed.py build)"
        else:
            try:
                sem_ranked = _sem.query(json.load(open(emb_path, encoding="utf-8")), query, k=POOL, type_filter=type_filter)
                rankings.append(sem_ranked)
                mode = "hybrid (bm25+semantic, RRF)"
            except _sem.OllamaError as e:
                mode = f"bm25-only (semantic unavailable: {e})"

    fused, meta = _rrf(rankings)
    top = sorted(fused.items(), key=lambda kv: -kv[1])[:k]
    results = [{"id": cid, "type": meta[cid]["type"], "title": meta[cid]["title"],
                "description": meta[cid]["description"], "rrf_score": round(score, 5)}
               for cid, score in top]
    return results, mode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("q")
    ap.add_argument("--bundle", default=os.path.join(HERE, "..", "wiki"))
    ap.add_argument("-k", type=int, default=8)
    ap.add_argument("--type")
    ap.add_argument("--bm25-only", action="store_true")
    a = ap.parse_args()
    results, mode = search(a.bundle, a.q, a.k, a.type, a.bm25_only)
    print(f"mode: {mode}")
    for r in results:
        print(f"  {r['rrf_score']:>8}  {r['id']:<40} [{r['type']}]  {r['description']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

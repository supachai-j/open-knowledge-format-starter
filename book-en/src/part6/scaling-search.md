# Search at Scale and Semantic Search

As the wiki grows, scanning a flat `index.md` becomes slow. This chapter covers search that scales, entirely on-prem.

## By Wiki Size

| Size | What to use |
|------|-------------|
| < ~150 concepts | `index.md` progressive disclosure is sufficient |
| > ~150 | Build a BM25 index (`okf-index.py build`) — `okf_search` uses it automatically |
| Recall is insufficient | Add a semantic + RRF layer (below) |
| Very large / multi-team | Federate bundles, one MCP server per domain, cache index in memory and rebuild via webhook |

## Semantic Layer (on-prem)

Embed concepts using a self-hosted embedding model (via Ollama) — nothing leaves the network:

```bash
ollama pull nomic-embed-text          # one-time
python3 tools/okf-embed.py build ./wiki   # → wiki/.okf-embed.json
python3 tools/okf-search.py "active customers" --bundle ./wiki
# → mode: hybrid (bm25+semantic, RRF)
```

## Reciprocal Rank Fusion (RRF)

`okf-search.py` combines **BM25 (lexical)** and **semantic (vector)** results using RRF:

```
fused(doc) = Σ_signals  1 / (RRF_K + rank)      (RRF_K = 60)
```

Each signal ranks its own set of docs, then the reciprocal of each rank is summed — docs that rank well across multiple signals rise to the top, without any single signal dominating.

Why two signals:

- **BM25** excels at exact keyword/code matching (policy codes, column names)
- **semantic** excels at meaning/synonym matching ("active customers" ↔ "weekly active users")

## Automatic Fallback (important)

> If embeddings have not been built **or** Ollama is not running → search **automatically falls back to BM25**
> and reports the mode so you know. Semantic search is therefore a **purely opt-in upgrade with no hard dependency**.

This makes the system resilient: machines without Ollama can still search using BM25.

## Scaling Further

- **Federate bundles** — separate repo per domain/team
- **One MCP server per domain** behind a single gateway
- **Cache index in memory** and rebuild incrementally when a webhook signals a merge
- Indexes/embeddings are **generatable artifacts** (built by CI / MCP server on demand) — no need to commit
  (`.okf-index.json`, `.okf-embed.json` are in `.gitignore`)

Next: security and governance → [Security and Governance](./security.md)

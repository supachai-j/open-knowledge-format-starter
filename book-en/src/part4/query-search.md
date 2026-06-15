# Query and Search

There are two ways to retrieve knowledge from the wiki, depending on its size.

## Method 1 — Query via Index (Small Wiki)

For small wikis (up to ~150 pages), reading `index.md` is sufficient:

1. Read `wiki/index.md` first to find relevant concepts.
2. Drill into those specific concept files.
3. Answer **only from the concepts loaded** and **always cite the Concept ID**.
4. If the coverage is incomplete, say so directly and offer to ingest additional sources.

Via agent: *"What does the wiki say about WAU?"* → agent reads the index → opens the concept → answers with citations.

## Method 2 — Search with an Index (Large Wiki)

Beyond ~150 pages, scanning the index becomes slow. Build a search index instead:

```bash
# Build a BM25 index (once / rebuild when content changes)
python3 tools/okf-index.py build ./wiki

# Search
python3 tools/okf-search.py "how is WAU defined" --bundle ./wiki -k 8
```

Results (ranked by BM25):

```
mode: bm25-only (no embeddings — run okf-embed.py build)
   2.675  metrics/weekly-active-users   [Metric]  Number of unique customers with orders...
   2.463  tables/customers              [BigQuery Table]  ...
```

> **What is BM25:** A keyword-based retrieval algorithm that scores relevance. Excellent for matching exact terms and codes
> (e.g. policy codes, column names). The tool is pure Python with no additional dependencies.

## Hybrid Search (BM25 + Semantic)

If keyword search alone doesn't capture enough meaning, add a semantic layer using a local embedding model (Ollama):

```bash
ollama pull nomic-embed-text          # once (on-prem)
python3 tools/okf-embed.py build ./wiki   # build embeddings → wiki/.okf-embed.json
python3 tools/okf-search.py "active customers" --bundle ./wiki
# → mode: hybrid (bm25+semantic, RRF)
```

`okf-search.py` will **fuse BM25 + semantic results using Reciprocal Rank Fusion (RRF)** automatically.

> **Always safe:** If embeddings haven't been built yet, or Ollama isn't running, search will **fall back to BM25
> automatically** and report the mode — semantic is a pure upgrade, not a hard dependency.

(Architecture details for hybrid search are in the [Search at Scale and Semantic Search](../part6/scaling-search.md) chapter.)

## Comparison

| Situation | Use |
|-----------|-----|
| Small wiki (< ~150 pages) | Read `index.md` directly |
| Large wiki, matching keywords/codes | `okf-search.py` (BM25) |
| Need to match meaning/synonyms | Hybrid (BM25 + semantic) |

Next: how to add and edit concepts → [Adding and Editing Concepts](./authoring.md)

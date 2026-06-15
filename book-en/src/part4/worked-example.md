# Worked Example: a Bookstore KB

This chapter walks the whole path from zero to searchable — a small knowledge base for an
online bookstore, with real commands. Use it as a template for your own domain.

## 1. Scaffold (init)

```bash
python3 tools/okf-init.py ./bookstore-kb
cd bookstore-kb
```
You get `AGENTS.md` + `wiki/{index.md, log.md, getting-started.md}` + `raw/`.

## 2. Add knowledge (simulated ingest)

Create concepts in the canonical layout — two tables, a metric, a join, a playbook. Example
`wiki/tables/books.md`:

```markdown
---
type: BigQuery Table
title: Books
description: One row per book in the catalog.
tags: [catalog, books]
timestamp: 2026-06-16T00:00:00Z
---

# Schema
| Column | Type | Description |
| :--- | :--- | :--- |
| book_id | STRING | Book id (PK) |
| author_id | STRING | FK to [authors](authors.md) |
| price | NUMERIC | Price (USD) |
| stock | INT64 | Units in stock |

# Joins
Join [authors](authors.md) on `author_id` — see [Books → Authors](../references/joins/books__authors.md).
Low stock → [restock runbook](../playbooks/low-stock-runbook.md)
```

Do the same for `authors`, `references/metrics/monthly-revenue`, `references/joins/books__authors`,
and `playbooks/low-stock-runbook`, then update `wiki/index.md` + `wiki/log.md`.

> In real use: drop a source into `raw/` and have the agent run the supervised INGEST flow
> ([Ingest chapter](./ingest.md)) — it extracts claims, shows them for approval, then writes the
> concepts and updates index/log for you.

The resulting KB is this graph:

<pre class="mermaid">
flowchart LR
  D["datasets/bookstore"] --> B["tables/books"]
  D --> A["tables/authors"]
  B -->|author_id| A
  J["references/joins/books__authors"] --> B
  J --> A
  M["references/metrics/monthly-revenue"] --> D
  P["playbooks/low-stock-runbook"] --> B
</pre>

## 3. Validate conformance

```bash
python3 tools/okf-validate.py ./wiki
# → ✓ CONFORMANT with OKF v0.1  (0 warning(s), 0 info)
```

## 4. Search

```bash
python3 tools/okf-index.py build ./wiki                       # build the BM25 index
python3 tools/okf-search.py "how to join books to authors" --bundle ./wiki
# → references/joins/books__authors  [Reference]   ranked #1
```

Add semantic (optional, on-prem):
```bash
ollama pull nomic-embed-text
python3 tools/okf-embed.py build ./wiki
python3 tools/okf-search.py "who wrote the novels" --bundle ./wiki
# → mode: hybrid (bm25+semantic, RRF) — finds authors even with no keyword overlap
```

## 5. Visualize

```bash
python3 tools/okf-viz.py ./wiki --name "Bookstore KB"
open wiki/viz.html        # one file, opens offline
```

## 6. (Team) Share via MCP

To let the whole team/agents use it: commit `wiki/` to an internal git server and bring up the
[MCP server](../part6/self-host.md) pointed at this bundle — agents can then `okf_search` (hybrid)
and propose changes via PR/lease.

## Summary

```text
okf-init → (ingest concepts) → okf-validate → okf-index/okf-search → okf-viz → [MCP share]
```

That's the full loop! Next, see [Authoring Well](../part5/best-practices.md) to grow the KB with quality.

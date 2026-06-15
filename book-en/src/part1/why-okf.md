# Why OKF? (vs. RAG)

If you have ever built an AI question-answering system on top of organizational documents, you have probably
used **RAG** (Retrieval-Augmented Generation) before. OKF is not here to kill RAG — it is here to address
the weaknesses that RAG most commonly hits in production.

## How traditional RAG works

```
Raw documents → chunk → embed → store in vector DB
                                       ↓ (at query time)
                   query → find nearest chunks → stuff into context → answer
```

The LLM **re-discovers knowledge from scratch on every query** — no accumulation, no understanding of which
chunk relates to what, contradicts what, or is stale.

## Common RAG failure modes

| Problem | What happens |
|-------|-------------|
| **Chunking artifacts** | Sentences are cut mid-way — e.g. "employees may work from home, except during the first 90 days" may be reduced to just "employees may work from home" → confidently wrong answer |
| **Knowledge decay** | New documents keep arriving but old contradicting content stays → old content gets retrieved (a leading cause of RAG project failures) |
| **Black box** | Retrieval returns chunks that look similar but are not the best answer, and nobody can see why |
| **No accumulation** | A question requiring synthesis across 5 documents must be reassembled from scratch every time; nothing is built up permanently |

## How OKF is different

OKF shifts from "pull raw chunks at query time" to **"a wiki that AI maintains and pre-synthesizes"**:

- When a new source arrives, AI **reads, summarizes, and merges it into the existing wiki** — updating pages, fixing cross-references,
  and **flagging conflicts when new information contradicts old**.
- At query time, already-digested Markdown pages are loaded directly into context — no chunking, no vector math.
- Knowledge becomes **a compounding asset**: every new source added makes the wiki richer.

| Dimension | RAG (raw) | OKF (pre-synthesized) |
|------|-----------|---------------------|
| Storage format | Specialized vector DB | Plain Markdown files + git |
| Human-readable? | No (UI / binary) | Yes, with any text editor |
| Version control | Difficult | Built-in (git diff / PR / blame) |
| Knows about conflicts / staleness? | No | Can flag and supersede |
| Vendor lock-in | High | None (it's just files) |

## Is "RAG is dead" actually true?

**No** — most engineers view them as **separate layers, not an either/or choice**:

- **Layer 1 — wiki (OKF):** Core synthesized knowledge. Finding the answer here is the end of the search (fastest, highest signal).
- **Layer 2 — raw documents + vector search:** Used when the wiki does not yet cover the question (fall back to raw sources).
- **Layer 3 — LLM general knowledge:** Fills gaps that exist in neither the wiki nor the raw documents.

The OKF starter in this book supports both worlds: the wiki as the primary layer, plus **hybrid search (BM25 + semantic)**
available as a next step when the wiki grows (see Part 6).

## When to use / not use OKF

**Good fit** when: knowledge must be long-lived, reused, shared across multiple people or agents, auditable,
and you want to avoid vendor lock-in.

**May not be worth it** when: you have a massive corpus of raw documents that will never be synthesized
(straight RAG is more cost-effective), or the data is single-use and throwaway.

Ready to get started → [Install](../part2/install.md)

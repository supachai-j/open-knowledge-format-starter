# Core Concepts Explained (with Examples)

This chapter summarizes the foundational concepts of Knowledge Base systems introduced in the [History](./history.md)
chapter — each topic includes a **short definition + concrete example + how it relates to OKF** so you can apply it immediately.

## 1. Knowledge Representation

**What it is:** A way of storing "what is known" so a machine can process it. Classic forms: production rules (IF-THEN),
semantic networks (concept graphs), frames (slot-filler).

**Example** (frame):
```
FRAME: Bacteroides
  IS-A: Anaerobic-Gram-Negative-Rod
  Gram-stain: negative (default)
  Treatment: [metronidazole, clindamycin]
```

**In OKF:** Each concept (a `.md` file) is one unit of knowledge — the frontmatter holds queryable fields; the body holds detail.

## 2. Ontology

**What it is:** A machine-readable specification of the concepts and relationships in a domain (more than a taxonomy — it includes logic that enables inference).

**Example** (RDF triple): `TimBernersLee — invented — WorldWideWeb` (subject–predicate–object)

**In OKF:** Markdown links between concepts serve a similar role to triples but are **untyped** — the type of relationship lives in the prose (much lighter than OWL).

## 3. Inverted Index

**What it is:** A data structure that maps "term → list of documents containing that term" — the heart of full-text search.

**Example:**
| Term | Documents |
|------|-----------|
| cat  | D1, D2 |
| dog  | D3 |

Search "dog" → returns D3 immediately, without scanning every document.

**In OKF:** `okf-index.py` builds an in-memory inverted index to power BM25.

## 4. TF-IDF & BM25 (Relevance Ranking)

**What it is:** A scoring formula measuring how well a document matches a query — **TF** (how often the term appears in the document) × **IDF** (how rare the term is across the corpus = more distinctive);
**BM25** improves on this with length normalization and saturation.

**Example:** The word "the" appears in every document → IDF = log(3/3) = 0 → score 0 (does not help discriminate). The word "dog" appears in only one document → high IDF → distinctive.

**In OKF:** BM25 is the primary search method in `okf-search.py` (lightweight, no extra dependencies).

## 5. Embeddings (Semantic Vectors)

**What it is:** Converting text into a numeric vector where "similar meaning = similar vector".

**Example** (word2vec): `king − man + woman ≈ queen` — semantic relationships become vector arithmetic.

**In OKF:** `okf-embed.py` generates embeddings for concepts using a local model (Ollama) for semantic search.

## 6. Vector / Semantic Search

**What it is:** Searching by vector proximity (e.g., cosine similarity) → captures meaning and synonymy that keyword search misses.

**Example:** Searching "car" finds a document written with "automobile" because their vectors are close.

**In OKF:** An optional layer (opt-in) — if embeddings/Ollama are unavailable it automatically falls back to BM25.

## 7. RAG (Retrieval-Augmented Generation)

**What it is:** Retrieving relevant information and inserting it into the LLM's context at query time to ground the answer (reduce hallucination, enable citation).

**Example** (5 steps):

<pre class="mermaid">
flowchart LR
  D["Documents"] --> C["chunk"] --> E["embed"] --> S["vector store"]
  Q["Query"] --> R["retrieve top-k"]
  S --> R --> G["LLM generate<br/>grounded answer"]
</pre>

**In OKF:** The wiki = Layer 1 (pre-synthesized; finding it in the wiki is sufficient); RAG = Layer 2 (mining raw documents when the wiki does not yet cover the topic).

## 8. Hybrid Search & RRF

**What it is:** Combining results from multiple retrieval methods (BM25 + semantic) using **Reciprocal Rank Fusion**: `score(d) = Σ 1/(k + rank)` (k=60).

**Example:** A document that ranks highly in both BM25 and semantic search floats to the top, with no single signal dominating.

**In OKF:** `okf-search.py` uses RRF to fuse BM25 + semantic results.

## 9. Knowledge Graph

**What it is:** A graph of entities (nodes) + typed relationships (edges) — "things, not strings" — enabling entity-level disambiguation and reasoning.

**Example:**

<pre class="mermaid">
flowchart LR
  CU["Customer A"] -->|orders| O["Order 123"]
  O -->|contains| P["Product X"]
  CU -->|in segment| SEG["High-value"]
</pre>

**In OKF:** The entire bundle forms a knowledge graph (concepts = nodes, links = edges) — viewable with `okf-viz.py`.

## Summary Table

| Concept | What it captures | Example in OKF |
|---------|-----------------|----------------|
| Knowledge representation | Knowledge structure | concept + frontmatter |
| Ontology | Semantic relationships | Markdown links (untyped) |
| Inverted index / BM25 | Exact term matching | `okf-index.py` |
| Embeddings / vector search | Semantic meaning | `okf-embed.py` |
| RAG | Grounding LLM answers | wiki (L1) + RAG (L2) |
| Hybrid / RRF | Fusing multiple signals | `okf-search.py` |
| Knowledge graph | Entities + relationships | bundle + `okf-viz.py` |

See the [Bibliography](../appendix/references.md) for the original papers and standards behind each concept.

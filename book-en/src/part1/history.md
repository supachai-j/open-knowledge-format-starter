# History and Evolution of the Knowledge Base

OKF did not emerge from thin air — it is the (provisional) destination of a journey spanning more than 60 years
of human effort to make "knowledge" storable, searchable, and machine-usable. This chapter traces that path
from the earliest era to the present and beyond, so you can see how OKF assembles lessons from each era.

> Reference numbers `[n]` in this chapter point to the [Bibliography](../appendix/references.md)

## Timeline Overview

| Period | Era | Key Advance |
|--------|-----|-------------|
| 1960s–1980s | Expert systems & KR | Separating "knowledge" from "reasoning"; IF-THEN rules, frames |
| 1990s–2000s | Ontologies & Semantic Web | RDF triples, OWL, linked data — machine-readable meaning |
| 1970→2010s | Databases & IR | Relational DB, inverted index, TF-IDF, BM25, Lucene/Elasticsearch |
| 1995→2020 | Wiki & PKM | Wikipedia, Zettelkasten, Markdown + `[[wikilinks]]` (Obsidian/Notion/Roam) |
| 2012→2020s | AI era | Embeddings, vector DB, RAG, knowledge graph |
| 2026→ | LLM-wiki & OKF | AI synthesizes knowledge into continuously maintained Markdown |

## Era 1 — Expert Systems & Knowledge Representation (1960s–1980s)

This era rested on a simple belief: "intelligent behavior in a narrow domain can be captured by explicitly encoding
expert knowledge and letting a machine reason over it." The key insight was **separating the knowledge base
(what is known: facts/rules) from the inference engine (how to reason)** — an architecture that remains foundational to this day.

- **DENDRAL** (1965, Feigenbaum/Buchanan/Lederberg, Stanford) — the first expert system, analyzing mass spectrometry [1]
- **MYCIN** (early 1970s, Shortliffe, Stanford) — ~600 IF-THEN rules for diagnosing bacterial infections, using "certainty factors" to handle uncertainty [1]
- **Frames** (1974, Minsky, MIT) — slot-filler structures for representing structured knowledge [1]
- **Cyc** (1984, Lenat) — an attempt to hand-encode all commonsense knowledge → exposed the **"knowledge acquisition bottleneck"**: hand-entering knowledge does not scale [1]

Example of a MYCIN-style rule:

```
IF   infection-type = primary-bacteremia
AND  culture-site  = blood
AND  portal-of-entry = gastrointestinal-tract
THEN there is suggestive evidence (CF = 0.4) that the organism is Bacteroides
```

> **Lesson for OKF:** Separating "knowledge" from "the engine that uses knowledge" is the core principle —
> OKF stores knowledge as files (producer) separately from the agents that consume it (consumer), exactly matching this pattern.

## Era 2 — Ontologies & the Semantic Web (1990s–2000s)

In 2001, Tim Berners-Lee and colleagues proposed the **Semantic Web** in Scientific American [2]: extending the web
from "documents for humans to read" to "data whose meaning machines can understand." The foundations were
**RDF** (storing knowledge as *subject–predicate–object* triples = edges in a graph), **OWL** (an ontology
language that allows a reasoner to infer new facts), and **SPARQL** (a graph query language) [2].

**Ontology** = a machine-readable specification of the concepts and relationships in a domain (not merely a taxonomy).

Example RDF (Turtle):

```turtle
@prefix ex: <http://example.org/> .
@prefix schema: <https://schema.org/> .

ex:TimBernersLee a schema:Person ;
    schema:name "Tim Berners-Lee" ;
    ex:invented ex:WorldWideWeb .
```

Each line `subject predicate object` is one triple — chained together they form a massive knowledge graph.

Full adoption never spread widely (in 2013 fewer than 2% of websites used semantic markup) because formal
representation is difficult. But the "practically usable" descendants survived: **linked data**, **schema.org** (2011),
and the **knowledge graph** [2].

> **Lesson for OKF:** Machine-traversable relationships are valuable — OKF simplifies this with plain
> **Markdown links** (untyped) instead of the RDF/OWL formalism that proves too demanding for everyday authors.

## Era 3 — Databases & Information Retrieval (1970→2010s)

The journey from "exact matching" to "relevance ranking":

- **Relational model** (1970, Codd, IBM) — storing data in tables and querying with SQL, but matching fields exactly [3]
- **TF-IDF** — Luhn (1957) showed that word frequency correlates with relevance; Spärck Jones (1972) added **IDF**: words appearing in fewer documents carry a stronger signal [3]
- **BM25** (~1994, Robertson & Spärck Jones, Okapi system) — adds length normalization and saturation; still the baseline for lexical search today [3]
- **Lucene** (1999, Doug Cutting) and **Elasticsearch** (2010) — bringing industrial-grade full-text search to everyone [3]

Example inverted index for three small documents:

| Term | Posting list |
|------|--------------|
| cat | D1, D2 |
| sat | D1, D3 |
| dog | D3 |

**Main limitation:** it is *lexical* — it matches exact terms. Searching "car" misses a document that says "automobile" (no understanding of meaning or synonymy).

> **Lesson for OKF:** BM25 is still powerful and lightweight — `tools/okf-index.py` uses BM25 as its primary search method.

## Era 4 — Wiki & Personal Knowledge Management (1995→2020)

- **WikiWikiWeb** (25 Mar 1995, Ward Cunningham) — the first editable web, with automatic linking via CamelCase [4]
- **Wikipedia** (15 Jan 2001, Wales & Sanger) — a community-edited open encyclopedia; the largest in history [4]
- **Zettelkasten** (Niklas Luhmann, 1950s–1998) — ~90,000 interconnected index cards; produced 50+ books. **The value lies in the "links between notes", not the notes themselves** [4]
- **Notion** (2016), **Roam** (2019, bidirectional links), **Obsidian** (2020, local-first Markdown + graph view) [4]

Markdown won the format wars because **humans can read it without rendering and machines can read it without a special parser**.

Example PKM-style Markdown note:

```markdown
---
title: "Zettelkasten Principle"
tags: [pkm, luhmann]
---
The value of the card box lies in the **links between notes**, not the individual notes themselves.
See also: [[Bidirectional Links]], [[Obsidian]]
```

> **Lesson for OKF:** This is OKF's direct DNA — Markdown + YAML frontmatter + links between concepts.

## Era 5 — AI Era: Embeddings, Vector Search, RAG (2012→2020s)

Core idea: **"meaning = geometry"**

- **Google Knowledge Graph** (2012, Singhal) — "things, not strings": 500M entities, 3.5B relationships [5]
- **word2vec** (2013, Mikolov, Google) — embedding words as vectors, capturing analogies such as `king − man + woman ≈ queen` [5]
- **FAISS** (2017, Facebook AI) — approximate nearest-neighbor (ANN) search over billions of vectors [5]
- **BERT** (2018, Devlin, Google) — contextual embeddings (the same word gets a different vector depending on context) [5]
- **RAG** (2020, Lewis et al., Facebook AI) — retrieving relevant passages to ground LLM answers and reduce hallucination [5]
- **Hybrid search + RRF** (RRF: Cormack et al., 2009) — combining BM25 + semantic with `Σ 1/(k+rank)` [5]

RAG pipeline example: chunk → embed → store → retrieve top-k → generate

> **Lesson for OKF:** OKF is Layer 1 (pre-synthesized knowledge); RAG/vector is Layer 2 (mining raw sources).
> `okf-search.py` combines BM25 + semantic with RRF, following this era's patterns.

## Era 6 — Present: LLM-wiki & Open Knowledge Format (2026)

In April 2026, **Andrej Karpathy** proposed the concept of an **"LLM wiki"** [6]: instead of retrieving raw chunks
on every query, have an agent **compile raw sources into organized, interlinked, continuously maintained Markdown**
— synthesize once at ingest, not on every query; knowledge **compounds**.

On 12 June 2026, **Google Cloud** (Sam McVeety, Amir Hormati) published **Open Knowledge Format (OKF)
v0.1** [6] — an open specification that standardizes the LLM-wiki pattern: a directory of Markdown files + YAML
frontmatter, requiring only a `type` field, with separate producer/consumer roles, portable across clouds and frameworks.

Before this, **MemGPT/Letta** (2023, Packer et al., UC Berkeley) [6] demonstrated "LLM as OS" — managing memory
in a tiered fashion (in-context = RAM, external = disk), paving the way toward agents with persistent memory.

## The Future — Self-Maintaining & Agentic Knowledge

The direction is a **self-maintaining knowledge base**: agents do not merely "query" knowledge — they
**curate it** — checking whether information is stale (via `timestamp`/`log.md`), reconciling conflicts across
concepts, and proposing updates for human approval before committing [6].

The next layer will likely be a **hybrid wiki + RAG** architecture: the pre-synthesized wiki serves as a fast index
while RAG fills gaps for rapidly-changing or too-voluminous-to-precompile data — with an agent memory runtime
(e.g., Letta) underneath, and multi-agent systems that divide responsibilities (one agent curates knowledge, others
consume it), moving toward what is beginning to be called **"compiled-knowledge generation"**.

## Summary: How History Shaped OKF

OKF does not reinvent everything — it **assembles the best parts of each era**:

| From era | What OKF takes |
|----------|----------------|
| Expert systems | Separating knowledge (files) from the engine that uses it (agent) |
| Semantic Web | Knowledge as an interconnected graph (but using simple Markdown links) |
| IR / BM25 | Lightweight and powerful search |
| Wiki / PKM | Markdown + frontmatter + `[[links]]`, human-readable, version-controllable |
| AI era | Embeddings/RAG as an optional layer + AI-synthesized knowledge |

Next, read [Core Concepts Explained (with Examples)](./foundations.md)

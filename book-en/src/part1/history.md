# History and Evolution of the Knowledge Base

<p class="okf-lead"><span class="drop">F</span>or over sixty years, humanity has asked the same question again and again: "How do we make machines <em>remember</em> and <em>understand</em> what we know?" The answer has changed with every era — from hand-crafted rules, to semantic graphs, to word indexes, to interlinked notes, and most recently to AI that synthesizes knowledge on our behalf. This chapter is the story of that journey, and its (provisional) destination: OKF.</p>

> Reference numbers `[n]` point to the [Bibliography](../appendix/references.md)

<pre class="mermaid">
flowchart LR
  E1["1960s–80s<br/>Expert systems"] --> E2["1990s–2000s<br/>Semantic Web"] --> E3["1970s–2010s<br/>Databases &amp; IR"] --> E4["1995–2020<br/>Wiki &amp; PKM"] --> E5["2012–2020s<br/>AI / RAG"] --> E6["2026<br/>LLM-wiki &amp; OKF"]
</pre>

## Act 1 — The Era We Tried to Hand-Feed Knowledge to Machines

In the 1960s at Stanford, a group of scientists believed that intelligence in a narrow domain could be captured by
**encoding expert knowledge as rules** and letting a machine reason over them. They built **DENDRAL**
(1965), which analyzed molecular structures from mass spectrometry data on par with a trained chemist [1] — the
first time the world saw that "knowledge," not "search," was the real key to AI.

A few years later, **MYCIN** (early 1970s, Edward Shortliffe) used around 600 IF-THEN rules to diagnose
bloodstream infections with accuracy matching senior physicians — and it could **explain its own reasoning** [1].
The heart of MYCIN was an architecture that lives with us to this day: separating the **knowledge base**
(what is known) from the **inference engine** (how to reason):

```
IF   infection-type = primary-bacteremia
AND  culture-site   = blood
AND  portal-of-entry = gastrointestinal-tract
THEN there is suggestive evidence (CF = 0.4) that the organism is Bacteroides
```

But the dream hit a wall. In 1984, Douglas Lenat launched the **Cyc** project — an attempt to hand-encode
*all* of human commonsense knowledge [1]. Decades and tens of millions of dollars later, the world learned an
expensive lesson called the **"knowledge acquisition bottleneck"**: hand-entering knowledge can never scale.

> 🧬 **DNA inherited by OKF:** Separating "knowledge (files)" from "the engine that uses knowledge (agent)" — OKF's producer/consumer architecture is a direct descendant of this idea.

## Act 2 — The Era We Tried to Give "Meaning" to the Web

In 2001, the father of the web, **Tim Berners-Lee**, published an article in *Scientific American* dreaming of
the **Semantic Web** [2] — a web that was not merely documents for humans to read, but data whose *meaning
machines could understand*. He proposed storing knowledge as **triples** (subject–predicate–object), which
are simply "edges in a graph":

```turtle
@prefix ex: <http://example.org/> .
ex:TimBernersLee  ex:invented  ex:WorldWideWeb .
```

With **RDF, OWL, and SPARQL**, machines could infer new facts from the graph automatically [2]. It was
beautiful in theory — but writing a correct ontology was far beyond what ordinary people could manage.
By 2013, fewer than 2% of websites used semantic markup. What survived and flourished instead were the
"easier to use" successors: **linked data**, **schema.org** (2011), and the **knowledge graph** [2].

> 🧬 **DNA into OKF:** Knowledge connected as a graph has enormous value — but OKF chose plain **Markdown links** (untyped) over strict RDF/OWL, so that people can actually write it.

## Act 3 — The Era We Learned to Search Intelligently

While AI dreamed big, another line of work proceeded quietly — and changed the world. In 1970, **Edgar Codd**
of IBM proposed the **relational model**, allowing data to be stored in tables and queried with SQL [3]. But it
matched records exactly; it could not search free text and rank results by relevance.

The answer came from **Karen Spärck Jones** (1972), who proposed **IDF** — a simple but profound idea:
*a word that appears in fewer documents is a stronger signal than one that appears everywhere* [3]. Combined
with term frequency this became **TF-IDF**, and later **BM25** (~1994), which remains the standard for
lexical search to this day. Here is a tiny example — the word "the" lives in every document and is worthless
for discrimination, while the word "dog," found in a single document, stands out sharply:

| Term | Documents | Distinctiveness |
|------|-----------|-----------------|
| the  | D1, D2, D3 | 0 (useless) |
| dog  | D3 | high |

When **Doug Cutting** released **Lucene** (1999) and later **Elasticsearch** (2010), industrial-grade
full-text search landed in everyone's hands [3]. The one limitation that lingered: it was *lexical* — searching
"car" would miss "automobile" because it understood no meaning.

> 🧬 **DNA into OKF:** BM25 is still powerful and lightweight — `tools/okf-index.py` uses it as the primary search method.

## Act 4 — The Era Knowledge Became Everyone's

In 1995, **Ward Cunningham** created **WikiWikiWeb**, the first website that anyone could edit [4]. Six years
later, **Wikipedia** (2001) proved that humanity's collective knowledge could grow through open contribution [4].

But the most remarkable story had unfolded earlier, on the desk of a German sociologist. **Niklas Luhmann**
had accumulated a **Zettelkasten** of some 90,000 index cards, each linked to others. He produced more than
50 books from it and left behind an immortal principle: **"The value lies not in the individual note, but in the
links between notes."** [4]

The digital age rediscovered this principle around 2016–2020 through **Notion, Roam, and Obsidian** — all
built on **Markdown + `[[wikilinks]]`**, which won the format wars for compounding reasons: *humans can read
it without rendering, and machines can parse it without a special parser* [4].

```markdown
---
title: "Zettelkasten Principle"
tags: [pkm]
---
The value of the card box lies in the **links between notes** — see also [[Obsidian]]
```

> 🧬 **DNA into OKF:** This is the most direct lineage — Markdown + YAML frontmatter + links between concepts is exactly what OKF looks like.

## Act 5 — The Era "Meaning" Became Geometry

In 2013, **Tomas Mikolov**'s team at Google revealed something that looked like magic: **word2vec** converted
words into vectors where "similar meaning = nearby position," making arithmetic of meaning possible [5].

<pre class="mermaid">
flowchart LR
  K["king"] -- " − man + woman " --> Q["≈ queen"]
</pre>

The years that followed accelerated relentlessly: **Google Knowledge Graph** (2012, "things, not strings"),
**FAISS** (2017) searching billions of vectors, **BERT** (2018) giving the same word different meanings
depending on context [5]. Then in 2020, **RAG** (Lewis et al.) arrived to fix the largest weakness of LLMs —
fabrication — by retrieving real evidence to ground answers [5]:

<pre class="mermaid">
flowchart LR
  D["Documents"] --> C["Chunk"] --> EM["Embed"] --> S["Vector store"]
  Q["Query"] --> R["Retrieve top-k"]
  S --> R --> G["LLM generate<br/>grounded answer"]
</pre>

And to combine the strengths of "exact term matching (BM25)" with "semantic matching (vector)," the world
reached for **Reciprocal Rank Fusion** (RRF, 2009), producing the **hybrid search** that is today's
default [5].

> 🧬 **DNA into OKF:** wiki = Layer 1 (pre-synthesized); RAG/vector = Layer 2 (mining raw sources); `okf-search.py` fuses BM25 + semantic with RRF.

## Act 6 — The Present: When AI Takes Care of Knowledge Itself

In April 2026, **Andrej Karpathy** posted a short idea that ignited the entire field: **"LLM wiki"** [6] — instead
of retrieving raw chunks on every query (as RAG does), have an agent **compile raw sources into organized,
interlinked, continuously maintained Markdown**. Synthesize once at ingest; knowledge therefore **compounds** —
the more you use it, the richer it gets, rather than starting from zero every time.

Two months later, on 12 June 2026, **Google Cloud** (Sam McVeety, Amir Hormati) made this pattern an open
standard under the name **Open Knowledge Format (OKF) v0.1** [6] — a directory of Markdown files + YAML
frontmatter requiring only a `type` field, with separate producer/consumer roles, portable across clouds and
frameworks.

Before that, **MemGPT/Letta** (2023) had already demonstrated "LLM as OS" — managing memory in a tiered
fashion (in-context = RAM, external = disk) and paving the way for agents with persistent memory [6].

## Epilogue — And the Future That Is Coming

The direction ahead is a **self-maintaining knowledge base**: agents do not merely "query" knowledge — they
*curate* it — checking whether information has gone stale (via `timestamp`/`log.md`), reconciling conflicts
across concepts, and proposing updates for human approval before committing [6]. The next layer will likely be
a **hybrid wiki + RAG** architecture: the pre-synthesized wiki serves as a fast index, while RAG fills gaps
for data that changes too frequently to precompile — with agent memory as the runtime and multi-agent systems
dividing responsibilities for curating and consuming knowledge, moving toward what is beginning to be called
**"compiled-knowledge generation"**.

## Why OKF Is the Sum of All Six Acts

OKF does not reinvent everything — it **fuses the best parts of every era into one**. Six streams converge into a single confluence:

<pre class="mermaid">
flowchart TD
  A["Expert systems<br/>knowledge vs. engine"] --> OKF
  B["Semantic Web<br/>knowledge as a connected graph"] --> OKF
  C["IR / BM25<br/>fast and lightweight search"] --> OKF
  D["Wiki / PKM<br/>Markdown + links, readable &amp; versionable"] --> OKF
  E["AI / RAG<br/>embeddings + AI synthesis"] --> OKF
  OKF["✦ Open Knowledge Format ✦"]
</pre>

Next, dive into the [Core Concepts Explained (with Examples)](./foundations.md) introduced throughout this chapter.

# AGENTS.md — OKF Bundle Schema & Agent Operating Rules

> This is the **schema file** for this repository. It is the first file an agent
> reads. It tells the agent how the knowledge base is structured and how to behave
> when ingesting sources, answering questions, or maintaining the wiki.
> (Equivalent file names for other agents: `CLAUDE.md`, `GEMINI.md`.)

This repository follows the **Open Knowledge Format (OKF) v0.1** (Google Cloud,
2026-06-12) layered on the "LLM-wiki" pattern. The OKF bundle lives in `wiki/`.

---

## 1. Directory layout (3-layer architecture)

```text
/ (repo root)
├── AGENTS.md          ← this schema (agent behavior + conventions)
├── raw/               ← LAYER 1: immutable source materials. Agent READS, never edits.
├── wiki/              ← LAYER 2: the OKF bundle. Agent OWNS and maintains this.
│   ├── index.md       ← reserved: progressive-disclosure catalog
│   ├── log.md         ← reserved: append-only chronological audit trail
│   ├── tables/
│   ├── metrics/
│   └── playbooks/
└── tools/             ← scripts + the concept template
```

- **`raw/` is the source of truth.** Drop PDFs, notes, exports here. Read-only for the agent.
- **`wiki/` is the OKF bundle.** Its root is `wiki/`, so a file at `wiki/tables/orders.md`
  has **Concept ID `tables/orders`** (path within the bundle, minus `.md`).
- **`tools/`** holds helpers: `concept-template.md`, `okf-validate.py` (conformance checker),
  and `okf-viz.py` (generates `wiki/viz.html`, a self-contained interactive graph viewer —
  a port of the visualizer from Google's reference implementation).

---

## 2. Concept files & frontmatter schema

Every non-reserved `.md` file in `wiki/` is a **Concept** — one unit of knowledge.

**Required (OKF v0.1 conformance):**
- `type` — short string for the kind of concept. Use the controlled vocabulary below.

**Recommended (priority order):**
- `title` — human-readable name.
- `description` — one-line relevance summary. **This is what an agent reads to decide whether to load the file — write it well.**
- `resource` — URI of the underlying real-world asset (omit for self-describing curated concepts).
- `tags` — YAML array, e.g. `[sales, revenue]`.
- `timestamp` — ISO 8601 UTC of the last meaningful change.

**Extension fields:** producers MAY add custom keys. Consumers MUST tolerate unknown keys.

**Controlled `type` vocabulary for this bundle** (extend as needed, keep consistent — inconsistent typing breaks aggregation):
`BigQuery Table` · `BigQuery Dataset` · `Metric` · `Reference` · `Playbook` · `API Endpoint` · `Concept` · `Entity`

> **Canonical grouping (from Google's reference bundles):** derived/curated knowledge — joins,
> metric definitions, glossaries — is grouped under a `references/` subtree (e.g.
> `references/joins/`, `references/metrics/`) and typed `Reference`. Tangible assets go under
> `tables/` (`BigQuery Table`) and `datasets/` (`BigQuery Dataset`). See `wiki/references/`.

Body rules: favor **structural Markdown** (headings, atomic bullets, tables) over dense prose.
Conventional headings (use when applicable, in this order): `# Overview` → `# Schema` →
`# Common query patterns` (fenced ` ```sql ` blocks) → `# Joins` → `# Examples` → `# Citations`.

---

## 3. Linking (the knowledge graph)

- Link concepts with **file-relative Markdown links**: `[Customers](../tables/customers.md)`.
- **Never start a link with `/`.** The OKF spec §5.1 *recommends* bundle-root-absolute links, but
  Google's reference enrichment agent forbids them because `/`-rooted links **break GitHub rendering**.
  We follow the reference implementation: file-relative only. (`tools/okf-validate.py` warns on `/` links.)
- Links are **untyped** in OKF — the relationship kind (depends-on, joins-with, references) is
  expressed in the **surrounding prose**, not the link syntax.
- **Only link to concepts that exist** (or intentionally leave a placeholder). **Broken links are allowed** —
  they mark knowledge not yet written.
- One link per concept-mention per section is enough; don't over-link. **Don't** link from headings,
  fenced code blocks, or schema field-name lists. Don't link a doc to itself.

---

## 4. Reserved files (MUST follow defined structure)

- **`index.md`** — a catalog enabling *progressive disclosure*: each entry = link + one-line summary,
  so an agent sees what exists before opening files. Every directory SHOULD have one. Update on every ingest.
- **`log.md`** — append-only, **newest-first**, grouped by ISO-8601 date (`## [YYYY-MM-DD]`).
  Each entry starts with a consistent prefix so it is greppable, e.g.
  `- ingest | <source title> | touched: tables/orders, metrics/wau`.

These two filenames MUST NOT be used for concept documents.

---

## 5. INGEST workflow (supervised — this is a quality gate, NOT a background daemon)

Ingestion is **always user-triggered**. Run these steps and **show the user the extracted claims
and proposed mappings BEFORE writing anything**:

1. Read the source in `raw/`.
2. Read `wiki/index.md` to learn which concepts already exist.
3. Extract 5–15 key claims, facts, or decisions worth retaining.
4. Map claims to existing concepts. Propose a **new** concept only if 5+ claims share a theme not covered.
5. **Reconcile contradictions.** If new data contradicts an existing concept, append to the OLD file:
   `> **CONTRADICTION FLAG**: <explanation; see <new concept>>` and attach context to the new one.
6. Create/update concept pages: append claims, update `tags`/`timestamp` in frontmatter.
7. Update the relevant `index.md` files.
8. Append one entry to `wiki/log.md` under today's date heading.

> **Why supervised:** an automated daemon accumulates noise at the same rate as signal and the
> wiki rots invisibly. The human "is this worth synthesizing?" decision is the quality gate.

---

## 6. QUERY workflow

1. Read `wiki/index.md` first to locate relevant concepts.
2. Drill into the specific concept files.
3. Answer **only** from loaded concepts; cite Concept IDs. If coverage is missing, say so and offer to ingest.

> **At scale / shared use:** past ~150 concepts, search with `tools/okf-search.py` (hybrid BM25 +
> optional on-prem semantic via Ollama, RRF-fused; auto-falls back to BM25) instead of scanning the
> index. For cross-session / cross-team enterprise use, agents reach the bundle through the self-hosted
> MCP server (`server/okf_mcp_server.py`) and propose writes via PR (default) — or, for high write
> volume, via advisory leases (`OKF_WRITE_MODE=lease`, `tools/okf-lease.py`). See `docs/ENTERPRISE.md`.

---

## 7. LINT / maintenance (ad-hoc, on request)

Don't hardcode a fixed lint command — ask the agent for the specific check you want. Common ones:
stale concepts (old `timestamp`, single old source), orphaned pages (no inbound links),
broken wikilinks, scope drift, duplicate concepts that should merge.

---

## 8. Conformance checklist (OKF v0.1)

A bundle is conformant if:
1. Every non-reserved `.md` file has a **parseable YAML frontmatter block**.
2. Every frontmatter block has a **non-empty `type`** field.
3. `index.md` / `log.md`, where present, follow their reserved structure.

Consumers MUST NOT reject a bundle for missing optional fields, missing `index.md`, unknown `type`
values, unknown keys, or broken links.

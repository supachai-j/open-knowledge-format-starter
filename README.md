# open-knowledge-format-starter

A ready-to-fork starter for building an **AI-maintained knowledge base** on the
**Open Knowledge Format (OKF) v0.1** (Google Cloud, 2026-06-12) — a directory of
Markdown files with YAML frontmatter that humans and AI agents can author, exchange,
and consume without translation.

> OKF formalizes Andrej Karpathy's "LLM-wiki" pattern into a portable, vendor-neutral spec.
> Instead of re-retrieving raw chunks on every query (classic RAG), an agent continuously
> synthesizes sources into curated, cross-linked Markdown that loads straight into context.

[![Conformance](https://img.shields.io/badge/OKF-v0.1-blue)](AGENTS.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## What's in here

```text
AGENTS.md            ← schema + agent operating rules (READ FIRST)
.claude/skills/okf/  ← Claude Code skill that drives ingest/query/lint/validate
raw/                 ← Layer 1: immutable source materials (read-only for the agent)
wiki/                ← Layer 2: the OKF bundle (agent-maintained concepts)
  index.md           ← reserved: progressive-disclosure catalog
  log.md             ← reserved: append-only change log
  tables/ metrics/ playbooks/   ← example concepts (replace with yours)
tools/               ← concept-template.md + okf-validate.py (conformance checker)
docs/                ← USAGE.md (how-to, EN/TH) + GUIDELINES.md (authoring rules)
research/            ← sourced best-practice report + concept mind map
```

## Quickstart

```bash
git clone https://github.com/supachai-j/open-knowledge-format-starter.git
cd open-knowledge-format-starter
python3 tools/okf-validate.py          # → ✓ CONFORMANT with OKF v0.1
```

1. Read **[AGENTS.md](AGENTS.md)** — governs how concepts are structured and how the agent behaves.
2. Browse the bundle from **[wiki/index.md](wiki/index.md)**.
3. Add knowledge: drop a source in `raw/`, then run the supervised **INGEST** workflow.
4. New concepts start from **[tools/concept-template.md](tools/concept-template.md)**.

Full walkthrough (EN/TH): **[docs/USAGE.md](docs/USAGE.md)** · Authoring rules: **[docs/GUIDELINES.md](docs/GUIDELINES.md)**

## Using the skill (Claude Code)

This repo ships a skill at `.claude/skills/okf/`. Open the repo in Claude Code and just state intent:

| You say | The agent does |
| :--- | :--- |
| "ingest raw/notes.pdf into the wiki" | Extracts 5–15 claims, shows them for approval, then writes concepts + updates `index.md`/`log.md` |
| "what does the wiki say about WAU?" | Reads the index, opens concepts, answers with Concept-ID citations |
| "create an OKF concept for the Sessions table" | Scaffolds a conformant concept from the template |
| "validate the bundle" | Runs `tools/okf-validate.py` and reports |

Any agent that reads `AGENTS.md` (e.g. via `CLAUDE.md`/`GEMINI.md`) can follow the same procedures.

## Conformance (OKF v0.1)

- Every non-reserved `.md` in `wiki/` has parseable YAML frontmatter with a non-empty `type`.
- `index.md` / `log.md` follow their reserved structure.
- Concept ID = path within `wiki/` minus `.md` (e.g. `tables/orders.md` → `tables/orders`).
- Consumers tolerate unknown keys, unknown `type` values, missing optional fields, and broken links.

## Background & caveats

See [`research/okf-best-practice-implementation-report.md`](research/okf-best-practice-implementation-report.md)
for the sourced best-practice guide and [`research/okf-mindmap.json`](research/okf-mindmap.json) for the concept map.

> OKF is **v0.1** (days old at scaffold time). Versioning is `<major>.<minor>`; expect changes.
> The normative spec requires only the `type` field — most "best practices" here come from the
> surrounding LLM-wiki community, not the spec itself. Patterns like confidence-decay and hybrid
> search are optional add-ons, not part of v0.1.

## License

[MIT](LICENSE) © 2026 Supachai-ja

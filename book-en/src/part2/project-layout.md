# Project Layout

The OKF starter uses a **three-layer architecture** with clearly separated responsibilities.

```text
my-kb/
├── AGENTS.md          ← Layer 3: schema + agent operating rules (read this first)
├── raw/               ← Layer 1: raw source material (read-only)
│   └── README.md
├── wiki/              ← Layer 2: OKF bundle (agent-managed)
│   ├── index.md       ← reserved file: table of contents (progressive disclosure)
│   ├── log.md         ← reserved file: change log
│   └── getting-started.md
└── tools/             ← tooling (validate, viz, index, ...)
```

## What are the three layers?

| Layer | Folder | Who writes | Role |
|------|----------|----------|-------|
| 1. Raw sources | `raw/` | Human | Source of truth — **read-only**, agents never modify |
| 2. Wiki | `wiki/` | Agent | Synthesized knowledge (OKF bundle) |
| 3. Schema | `AGENTS.md` | Human + agent jointly | Rules, conventions, and workflow that govern the agent |

Key point: **`wiki/` is the "bundle root"**, so Concept IDs are counted from `wiki/`. For example,
`wiki/tables/orders.md` has Concept ID = `tables/orders`.

## `AGENTS.md` — The most important file

This is the first file an agent reads. It tells the agent:

- The structure of the bundle
- Frontmatter rules (which fields are required/recommended, the controlled vocabulary for `type`)
- Linking rules (use relative paths, never start with `/`)
- The ingest / query / validate workflow

> This file is what turns the AI into a "disciplined wiki curator" rather than a generic chatbot.
> You and the agent will gradually develop this file together to fit your domain.

If you use a different agent, the filename might be `CLAUDE.md` (Claude Code) or `GEMINI.md` — the content is the same.

## `raw/` — Raw source material

Place your originals here: PDFs, meeting notes, exports, datasets.

- **Immutable** — agents read but never modify. This is the source of truth.
- Files in `raw/` are **not part of the bundle** (the bundle is `wiki/`); they are the *input* to the ingest process.
- In the real starter, `.gitignore` will **not commit files inside `raw/`** to prevent accidentally pushing private or large data
  (only `raw/README.md` is kept) — if you want to version-control your actual sources, comment out the `raw/*` line.

## `wiki/` — OKF bundle

This folder is owned by the agent. It organizes concepts into categories. The initial scaffold contains:

```text
wiki/
├── index.md              ← root table of contents (contains okf_version)
├── log.md                ← change log
├── getting-started.md    ← example concept
└── (yours) tables/  references/  playbooks/ ...
```

Commonly seen categories (from the Google reference implementation):

- `tables/` — tables (`type: BigQuery Table`)
- `datasets/` — datasets (`type: BigQuery Dataset`)
- `references/` — synthesized knowledge, e.g. `references/metrics/`, `references/joins/` (`type: Reference`)

Next, dive into the core concepts — start with [Bundle, Concept, and Concept ID](../part3/concepts.md).

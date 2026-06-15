# Build Your First Knowledge Base

Let's create your first OKF bundle in just a few minutes.

## Step 1 — Scaffold the structure

Use `okf-init.py` to scaffold a new bundle in the current directory (or a directory you specify):

```bash
python3 tools/okf-init.py .            # scaffold in the current directory
# or if installed as a skill:
python3 ~/.claude/skills/okf/scripts/okf-init.py ./my-kb
```

Output:

```text
Scaffolding OKF bundle in /path/to/project
  wrote: AGENTS.md
  wrote: raw/README.md
  wrote: wiki/index.md
  wrote: wiki/log.md
  wrote: wiki/getting-started.md
✓ done. Next: validate with okf-validate.py, then ingest sources from raw/.
```

> **Safe:** If a non-empty `wiki/` directory already exists, the script will **not overwrite** it unless you pass `--force`.

## Step 2 — Check conformance

```bash
python3 tools/okf-validate.py ./wiki
# → ✓ CONFORMANT with OKF v0.1  (0 warning(s), 0 info)
```

## Step 3 — View the graph

```bash
python3 tools/okf-viz.py ./wiki --name "My First KB"
# → wiki/viz.html  (single file, open in a browser instantly — no internet required)
```

Open `wiki/viz.html` to see concepts as nodes connected by edges. Click any node to view its details.

## Step 4 — Start capturing knowledge

1. Drop your source files (PDFs, notes, exports) into the `raw/` folder.
2. Tell the AI agent to *"ingest raw/<file> into the wiki"* — the agent will extract key points for your approval before writing anything.
   (Details in the [Ingest](../part4/ingest.md) chapter.)

## Writing concepts by hand

OKF is plain Markdown — you can create a concept yourself. For example, create `wiki/glossary/wau.md`:

```markdown
---
type: Metric
title: Weekly Active Users (WAU)
description: The number of unique customers who placed at least one order in the past 7 days
tags: [growth, metric]
timestamp: 2026-06-15T00:00:00Z
---

# Definition
Count unique `customer_id` values that have at least one order in the last 7-day window.
```

Then run `okf-validate.py` again to confirm it is still conformant.

## Quick-reference command table

| Task | Command |
|--------|--------|
| Create a new bundle | `okf-init.py <dir>` |
| Check conformance | `okf-validate.py ./wiki` |
| View the graph | `okf-viz.py ./wiki` |
| Build the search index | `okf-index.py build ./wiki` |
| Search | `okf-search.py "question" --bundle ./wiki` |

Next, understand the [project layout](./project-layout.md) that was scaffolded for you.

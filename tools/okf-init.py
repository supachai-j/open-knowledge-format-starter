#!/usr/bin/env python3
"""okf-init.py — scaffold a new, conformant OKF v0.1 bundle in any project.

Creates an `AGENTS.md` schema + a `wiki/` bundle (index.md with okf_version, log.md,
and one example concept) so an agent can start ingesting immediately. Safe: refuses
to overwrite an existing wiki/ unless --force.

Usage:
  python3 okf-init.py [target_dir]   # default: current directory
  python3 okf-init.py . --force
"""
import argparse
import os

AGENTS_MD = """# AGENTS.md — OKF Bundle Schema & Agent Rules

This repo is an **Open Knowledge Format (OKF) v0.1** bundle: a directory of Markdown files
with YAML frontmatter that agents and humans co-maintain. The bundle lives in `wiki/`.

## Layout
- `raw/`  — immutable sources (read-only for the agent).
- `wiki/` — the OKF bundle (agent-maintained). Concept ID = path under `wiki/` minus `.md`.
- Reserved: `wiki/index.md` (catalog), `wiki/log.md` (append-only, `## YYYY-MM-DD`).

## Frontmatter
- **Required:** `type` (non-empty). **Recommended:** `title`, `description`, `resource`, `tags`, `timestamp` (ISO 8601).
- Curated/derived knowledge (joins, metric defs) → `references/` with `type: Reference`.

## Linking
- **File-relative** Markdown links only (`../tables/orders.md`). **Never start a link with `/`** (breaks GitHub).
- Links are untyped — relationship meaning lives in the prose. Broken links are allowed (= unwritten knowledge).

## INGEST (supervised — a quality gate, never automatic)
Read source in `raw/` → read `wiki/index.md` → extract 5–15 claims → **show the user for approval** →
write/update concepts → update `index.md` → append to `log.md` → run `okf-validate.py`.

## QUERY
Read `wiki/index.md` first, drill into concepts, answer only from loaded concepts and cite Concept IDs.

## Conformance (OKF v0.1)
Every non-reserved `.md` in `wiki/` has parseable frontmatter with a non-empty `type`; reserved files
follow their structure. Validate with `okf-validate.py`.
"""

ROOT_INDEX = """---
okf_version: "0.1"
---
# Concepts

* [getting-started](getting-started.md) - How this knowledge base is organized and how to add to it.
"""

LOG_MD = """# Directory Update Log

## {date}
* **Initialization**: Scaffolded OKF v0.1 bundle with `okf-init.py`.
"""

GETTING_STARTED = """---
type: Reference
title: Getting started
description: How this knowledge base is organized and how to add to it.
tags: [meta, okf]
timestamp: {ts}
---

# Overview

This is an **Open Knowledge Format (OKF) v0.1** bundle. Each `.md` file under `wiki/` is one *concept*
(a unit of knowledge) with YAML frontmatter (`type` is the only required field) and a Markdown body.

# How to add knowledge

1. Drop a source in `raw/`.
2. Ask your agent to *ingest* it (it extracts claims, shows them for approval, then writes concepts).
3. Link concepts with file-relative Markdown links; the relationship is described in the prose.

See `AGENTS.md` for the full rules, and run `okf-validate.py` to check conformance.
"""

RAW_README = """# raw/ — Source materials (read-only)
Drop original sources here (PDFs, notes, exports). The agent reads from here but never edits these files.
"""


def write(path, content, force, base):
    rel = os.path.relpath(path, base)
    if os.path.exists(path) and not force:
        print(f"  skip (exists): {rel}")
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  wrote: {rel}")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", default=".")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    ap.add_argument("--date", default="2026-01-01", help="ISO date for the initial log/timestamp")
    a = ap.parse_args()
    root = os.path.abspath(a.target)
    wiki = os.path.join(root, "wiki")
    if os.path.isdir(wiki) and os.listdir(wiki) and not a.force:
        print(f"✗ {wiki} already exists and is non-empty. Use --force to overwrite.")
        return 1
    ts = a.date + "T00:00:00Z"
    print(f"Scaffolding OKF bundle in {root}")
    write(os.path.join(root, "AGENTS.md"), AGENTS_MD, a.force, root)
    write(os.path.join(root, "raw", "README.md"), RAW_README, a.force, root)
    write(os.path.join(wiki, "index.md"), ROOT_INDEX, a.force, root)
    write(os.path.join(wiki, "log.md"), LOG_MD.format(date=a.date), a.force, root)
    write(os.path.join(wiki, "getting-started.md"), GETTING_STARTED.format(ts=ts), a.force, root)
    print("✓ done. Next: validate with okf-validate.py, then ingest sources from raw/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

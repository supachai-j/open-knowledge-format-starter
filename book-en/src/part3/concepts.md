# Bundle, Concept, and Concept ID

These three terms are the heart of OKF. Understand them and you understand half the spec.

## Bundle (knowledge set)

A **bundle** is the directory containing all knowledge files — it is the **unit of distribution**.
A single bundle can be shared in several forms:

- As a **git repository** (recommended — you get history, diffs, and code review for free)
- As a tarball / zip
- As a subdirectory inside a larger repository

In this project the bundle is the `wiki/` folder.

## Concept (unit of knowledge)

A **concept** is one unit of knowledge, represented as **a single Markdown file**. It may describe:

- Tangible things — a database table, an API endpoint
- Abstract things — a business metric, a playbook, a process

**The golden rule: one file = one concept.** Do not pack three topics into one file.

A concept has two parts:

```markdown
---
type: Metric          ← (1) Frontmatter — YAML block
title: ...
---
                      ← (2) Body — free-form Markdown
# Definition
...
```

## Concept ID (concept identifier)

**Concept ID = the file's path inside the bundle with `.md` removed.**

| File (inside `wiki/`) | Concept ID |
|-------------------|------------|
| `tables/orders.md` | `tables/orders` |
| `references/metrics/wau.md` | `references/metrics/wau` |
| `playbooks/incident.md` | `playbooks/incident` |

Key point: **identity is tied to the file path**, so…

> ⚠️ **Renaming or moving a file = changing the Concept ID = breaking all inbound links.**
> Choose stable filenames from the start. Use lowercase with hyphens (kebab-case), e.g. `weekly-active-users.md`.

The advantage of using the path as identity: you get **sovereign identity** with no central registry —
just look at the file's address to know which concept it is.

## Tree structure, graph relationships

Folders provide a tree structure (parent-child), but concepts can link to each other freely via **Markdown links**,
forming a **graph** that is richer than the folder hierarchy (see the [Linking](./linking.md) chapter).

```text
wiki/
├── tables/orders.md ─────┐ (link "joins-with")
├── tables/customers.md ◄─┘
└── references/metrics/wau.md ──► tables/orders.md ("derived-from")
```

Next, examine the file header in detail → [Frontmatter](./frontmatter.md)

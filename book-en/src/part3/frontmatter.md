# Frontmatter (Metadata)

**Frontmatter** is a YAML block at the top of a file, delimited by `---`, that stores metadata intended for search, filtering, and indexing.

```yaml
---
type: BigQuery Table              # required
title: Orders                     # recommended
description: หนึ่งแถวต่อหนึ่งคำสั่งซื้อ   # recommended
resource: https://...             # recommended (if a real resource exists to point to)
tags: [sales, orders]             # recommended
timestamp: 2026-06-15T00:00:00Z   # recommended (ISO 8601)
---
```

## Required Fields

| Field | Description |
|-------|-------------|
| **`type`** | The kind of concept — this is the **only required field** in v0.1. Consumers use this value for routing, filtering, and display. |

## Recommended Fields (in order of importance)

| Field | Description |
|-------|-------------|
| `title` | A human-readable name. If omitted, consumers may infer it from the filename. |
| `description` | A one-line summary — **this is what an agent reads to decide whether to load the file**. Write it to be precise. |
| `resource` | URI of the real-world resource that the concept describes (may be omitted for abstract concepts). |
| `tags` | A YAML list for cross-domain categorisation, e.g. `[sales, revenue]`. |
| `timestamp` | The time of the most recent significant edit (ISO 8601 format). |

> 💡 **`description` matters more than you think** — write it precisely, e.g.
> *"Number of unique customers with ≥1 order in the last 7 days"* is better than *"About WAU"*

## Extension Fields

Producers **may add any fields they like**, and consumers **must tolerate unknown keys** (they must not reject the file).
For example, add `owner`, `sla`, or `pii: true` as your domain requires.

## Controlled Vocabulary for `type`

Although the spec does not enforce a taxonomy, **`type` values should be used consistently** — otherwise data aggregation becomes impossible.
This starter uses the following set:

`BigQuery Table` · `BigQuery Dataset` · `Metric` · `Reference` · `Playbook` · `API Endpoint` · `Concept` · `Entity`

> **Convention from Google's reference bundle:** Synthesised or reference knowledge (joins, metric definitions, glossary)
> is typically placed under `references/` with `type: Reference`, while concrete assets live under `tables/` / `datasets/`.

## Pitfalls

- **Do not over-stuff frontmatter** — keep it semantic (entity, intent, definition); do not dump keywords,
  because noise degrades search quality.
- **Use field names consistently** — if one file uses `author_name` and another uses `written_by`, aggregation breaks.

## Body Below Frontmatter

The content section is free-form Markdown, but **structured markup** (headings, bullets, tables) is preferred over long prose paragraphs.
Conventional headings (use when appropriate, in this order):

`# Overview` → `# Schema` → `# Common query patterns` (code: `sql`) → `# Joins` → `# Examples` → `# Citations`

Next, see how to connect concepts together → [Linking as a knowledge graph](./linking.md)

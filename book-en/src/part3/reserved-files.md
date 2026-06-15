# Reserved Files: index.md and log.md

OKF reserves two filenames that carry special meaning at every level of the directory tree, and
**must not be used as concept files**.

| File | Purpose |
|------|---------|
| `index.md` | Directory table of contents (progressive disclosure) |
| `log.md` | Change history log |

## `index.md` — Table of Contents for Progressive Disclosure

Allows people and agents to **see what is available before opening any real file** — this is crucial for preventing
context-window overflow during exploration. An agent reads `index.md` first to find relevant concepts, then drills into individual files.

Format: no frontmatter (except at the root index — see below); content is headings and lists in the form
`* [Name](link) - short description`

```markdown
# Subdirectories

* [tables](tables/index.md) - BigQuery tables and schema/join information
* [references](references/index.md) - Synthesised knowledge (joins, metric definitions)

# Concepts

* [tables/orders](tables/orders.md) - One row per order
```

> Producers may **auto-generate `index.md`**; consumers may **build it on the fly when reading** if it is absent.

### `okf_version` at the Root Index

At the **bundle root only**, `index.md` may carry frontmatter — and only one field: `okf_version`, which declares
the spec version this bundle conforms to:

```markdown
---
okf_version: "0.1"
---
# Concepts
...
```

## `log.md` — Change History

Records changes within that scope as a list **sorted newest first**, grouped under ISO date headings.

```markdown
# Directory Update Log

## 2026-06-15
* **Update**: เพิ่มตาราง [Customer Metrics](references/metrics/cm.md)
* **Creation**: สร้าง [Dataplex Playbook](playbooks/dataplex.md)

## 2026-06-12
* **Initialization**: สร้างโครงสร้างไดเรกทอรีพื้นฐาน
```

Rules:

- Date headings **must** follow the ISO format `YYYY-MM-DD` (**no brackets**)
- Bold prefixes (`**Update**`, `**Creation**`, `**Deprecation**`) are **convention, not mandatory**

> 💡 Consistent prefixes make grepping easy, e.g. `grep '^- ' log.md` to view the latest entries.

## Why These Two Files Matter

- `index.md` = **navigator** that lets an agent explore the bundle without loading all of it into context
- `log.md` = **readable audit trail** that shows how the wiki has evolved and helps an agent understand what was recently changed

> `okf-validate.py` checks that `index.md` has no frontmatter (except `okf_version` at the root)
> and warns if any date heading in `log.md` is not in ISO format.

That concludes the core concepts. Next, put it all into practice → [Ingest: Adding Knowledge to the Wiki](../part4/ingest.md)

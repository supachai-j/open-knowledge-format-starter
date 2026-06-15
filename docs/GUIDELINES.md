# Authoring Guidelines / แนวทางการเขียน

Conventions for writing high-quality OKF concepts so both humans and agents can use the wiki
reliably. These layer on top of the normative spec (which only *requires* a `type` field).

แนวทางเขียน concept ให้มีคุณภาพ เพื่อให้คนและ agent ใช้ wiki ได้อย่างเชื่อถือได้

---

## Golden rules

1. **One concept per file.** A concept is a single unit of knowledge (a table, a metric, a playbook).
   Don't bundle three ideas into one file. / หนึ่งไฟล์ = หนึ่ง concept
2. **Write `description` for the agent.** It's the one line an agent reads to decide whether to load the
   file. Make it specific: *"Count of distinct customers with ≥1 order in a rolling 7-day window"*, not *"WAU stuff"*.
3. **Structure beats prose.** Favor headings, atomic bullets (`**key** — value`), and tables. Models extract
   structured Markdown far more reliably than dense paragraphs. / ใช้ heading/bullet/table แทนย่อหน้า
4. **Identity = path.** Choose stable, lowercase, kebab-case filenames. Renaming a file changes its Concept ID
   and breaks inbound links. / ชื่อไฟล์คือ identity เปลี่ยนแล้วลิงก์พัง
5. **Keep `type` consistent.** Pick from the controlled vocabulary in `AGENTS.md`. `author_name` in one file and
   `written_by` in another means machines can't aggregate. / ใช้ `type` ให้สม่ำเสมอ
6. **Cite your source.** Every synthesized claim should trace to a file in `raw/`. Put it under a `# Citations`
   heading. / อ้างอิงแหล่งที่มาเสมอ

---

## Frontmatter style

```yaml
---
type: BigQuery Table          # REQUIRED. Controlled vocabulary only.
title: Orders                 # Human-readable.
description: One sharp line.   # What an agent reads to decide to load the file.
resource: https://...         # URI of the real asset. Omit if self-describing.
tags: [sales, revenue]        # YAML array. Semantic only — NOT a keyword dump.
timestamp: 2026-06-15T00:00:00Z  # ISO 8601 UTC, last meaningful change.
---
```

- **Don't over-stuff frontmatter.** Keep it semantic (entities, intent, definitions). Noise lowers retrieval quality.
- **Extension fields are allowed** — add domain keys freely; consumers must tolerate unknown keys.

---

## Linking

- Use **relative Markdown links**: `[customers](../tables/customers.md)`.
- Links are **untyped** — express the relationship in the prose: *"Joins to [customers] on `customer_id`."*
- **Broken links are fine** — they mark knowledge not yet written. Don't fabricate a page just to satisfy a link.

---

## Reserved files

- **`index.md`** — one entry per child: link + a one-line summary. Update on every change.
- **`log.md`** — append-only, **newest-first**, grouped by `## [YYYY-MM-DD]`. Greppable prefix `- <verb> | ...`.

---

## Anti-patterns (don't do these) / สิ่งที่ไม่ควรทำ

| Anti-pattern | Why it hurts | Do instead |
| :--- | :--- | :--- |
| **Automated background ingest** | Accumulates noise as fast as signal; the wiki rots invisibly | Make ingest a deliberate, reviewed command |
| **Dumping raw PDFs into `wiki/`** | Unreliable retrieval; defeats synthesis | Synthesize into Markdown/YAML concepts; keep raw in `raw/` |
| **Over-stuffed frontmatter** | Noise lowers retrieval accuracy | Keep `tags` semantic and minimal |
| **Skipping header levels** (H1→H3) | Breaks the document outline for the model | Maintain strict H1→H2→H3 |
| **Paragraphs inside lists** | Fragments the list for parsers | Use nested indentation or finish the list first |
| **Inconsistent `type` / field names** | Machines can't aggregate | Use the controlled vocabulary |
| **Vague anchor text** ("click here") | No topical signal for the LLM | Use descriptive link text |
| **Sacrificing human readability** | The wiki must serve people too | Structure for the machine, prose for the human |

---

## Definition of done (per change) / ถือว่าเสร็จเมื่อ

- [ ] Concept file has a non-empty `type` and a sharp `description`.
- [ ] `timestamp` updated to now (UTC).
- [ ] Relevant `index.md` updated.
- [ ] Entry appended to `log.md` under today's date.
- [ ] `python3 tools/okf-validate.py` passes.

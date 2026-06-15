# Usage Guide / วิธีการใช้งาน

How to use this **Open Knowledge Format (OKF) v0.1** starter — an AI-maintained
knowledge base made of Markdown + YAML-frontmatter files.

วิธีใช้ starter ของ **Open Knowledge Format (OKF) v0.1** — ฐานความรู้ที่ AI ดูแล
เก็บเป็นไฟล์ Markdown + YAML frontmatter

---

## 1. Get the repo / ดึงโปรเจกต์

```bash
git clone https://github.com/supachai-j/open-knowledge-format-starter.git
cd open-knowledge-format-starter
```

Or use it as a **template** on GitHub (green "Use this template" button) to start your own KB.
หรือกดปุ่ม **"Use this template"** บน GitHub เพื่อสร้าง KB ของคุณเอง

---

## 2. Understand the layout / เข้าใจโครงสร้าง

| Path | Layer | Rule |
| :--- | :--- | :--- |
| `raw/` | Sources (Layer 1) | Immutable. Drop sources here. The agent reads, never edits. / วางไฟล์ต้นทาง อ่านอย่างเดียว |
| `wiki/` | The OKF bundle (Layer 2) | Agent-maintained concepts. Bundle root. / concept ที่ agent ดูแล |
| `AGENTS.md` | Schema (Layer 3) | Agent behavior + conventions. Read first. / กฎการทำงานของ agent |
| `tools/` | Helpers | `concept-template.md`, `okf-validate.py` |

**Concept ID = file path inside `wiki/` minus `.md`.** `wiki/tables/orders.md` → `tables/orders`.
**Concept ID = path ในโฟลเดอร์ `wiki/` ตัด `.md` ออก**

---

## 3. The four everyday operations / 4 งานหลักที่ใช้ประจำ

This repo ships a Claude Code **skill** (`.claude/skills/okf/`). With Claude Code (or any
agent that reads `AGENTS.md`), just speak the intent — the agent follows the procedure.
Repo มี **skill** ของ Claude Code อยู่แล้ว — แค่บอกความต้องการ agent จะทำตามขั้นตอนให้

### A. Ingest a source / เก็บความรู้เข้า wiki
1. Put a file (PDF, notes, export) into `raw/`. / วางไฟล์ลง `raw/`
2. Tell the agent: **"ingest raw/<file> into the wiki"** / สั่ง: "ingest raw/<file> เข้า wiki"
3. The agent extracts 5–15 claims and **shows them for your approval before writing.** / agent ดึง 5–15 ข้อมาให้อนุมัติก่อนเขียน
4. On approval it updates concepts, `index.md`, and appends to `log.md`. / เมื่ออนุมัติ มันจะอัปเดตไฟล์ให้

> ⚠️ Ingestion is **supervised on purpose** — it is a quality gate, not a background job.
> ⚠️ ตั้งใจให้มีคนกำกับ — เป็น "ประตูคุณภาพ" ไม่ใช่ daemon อัตโนมัติ

### B. Query the wiki / ถาม wiki
Ask: **"what does the wiki say about WAU?"** The agent reads `wiki/index.md`, opens the
relevant concepts, and answers **with Concept-ID citations** — or tells you coverage is missing.
ถาม: "wiki ว่าไงเรื่อง WAU" → agent อ่าน index แล้วตอบพร้อมอ้าง Concept ID

### C. Add / edit a concept / เพิ่ม-แก้ concept
Start from `tools/concept-template.md`, set a real `type`, write the body with relative links,
then update `index.md` + `log.md`. / เริ่มจาก template ตั้ง `type` เขียนเนื้อหา แล้วอัปเดต index/log

### D. Validate conformance / ตรวจ conformance
```bash
python3 tools/okf-validate.py
# → ✓ CONFORMANT with OKF v0.1
```
Run it after every change. Zero dependencies (stdlib only). / รันหลังแก้ทุกครั้ง ไม่ต้องลง dependency

---

## 4. Manual authoring (no agent) / เขียนเองโดยไม่ใช้ agent

You can author OKF by hand — it's just Markdown:
เขียน OKF มือเองได้ เพราะมันคือ Markdown ธรรมดา

```markdown
---
type: Metric
title: Conversion Rate
description: Orders divided by sessions in a day.
tags: [growth, metric]
timestamp: 2026-06-15T00:00:00Z
---

# Definition
Orders / sessions for a given day. Source: [orders](../tables/orders.md).
```

Then `python3 tools/okf-validate.py` to confirm it conforms.

---

## 5. Scale up (optional) / ขยายเมื่อโตขึ้น (ทางเลือก)

When the wiki passes ~150 pages, a flat `index.md` gets slow. Add **hybrid search**
(BM25 + semantic, fused with RRF) over `wiki/`, exposed to agents via an **MCP** server
(e.g. a local markdown search engine). The synthesis layer is unchanged — you're only
adding smarter navigation. See `research/okf-best-practice-implementation-report.md` §6.

เมื่อเกิน ~150 หน้า ให้เพิ่ม hybrid search (BM25 + semantic, รวมด้วย RRF) ต่อผ่าน MCP server

---

## 6. Conformance cheat-sheet / สรุปกฎ conformance

1. Every non-reserved `.md` in `wiki/` has a **parseable YAML frontmatter block**.
2. Every frontmatter has a **non-empty `type`**.
3. `index.md` / `log.md` follow their reserved structure.
4. Consumers tolerate unknown keys, unknown `type` values, missing optional fields, and broken links.

See [GUIDELINES.md](GUIDELINES.md) for authoring style rules and anti-patterns.
ดูกฎการเขียนและ anti-patterns ที่ [GUIDELINES.md](GUIDELINES.md)

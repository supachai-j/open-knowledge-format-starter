# ตัวอย่างใช้งานจริง: KB ร้านหนังสือ

บทนี้เดินครบทุกขั้นตั้งแต่ศูนย์จนค้นได้ — สร้าง knowledge base เล็ก ๆ ของร้านหนังสือออนไลน์
ด้วยคำสั่งจริง ใช้เป็นแม่แบบกับโดเมนของคุณได้เลย

## 1. สร้างโครง (init)

```bash
python3 tools/okf-init.py ./bookstore-kb
cd bookstore-kb
```
ได้ `AGENTS.md` + `wiki/{index.md, log.md, getting-started.md}` + `raw/`

## 2. ใส่ความรู้ (จำลอง ingest)

สร้าง concept ตามโครงสร้าง canonical — ตาราง 2 ตัว, metric, join, playbook ตัวอย่าง `wiki/tables/books.md`:

```markdown
---
type: BigQuery Table
title: Books
description: หนึ่งแถวต่อหนังสือหนึ่งเล่มในแคตตาล็อก
tags: [catalog, books]
timestamp: 2026-06-16T00:00:00Z
---

# Schema
| Column | Type | Description |
| :--- | :--- | :--- |
| book_id | STRING | รหัสหนังสือ (PK) |
| author_id | STRING | FK ไปยัง [authors](authors.md) |
| price | NUMERIC | ราคา (USD) |
| stock | INT64 | จำนวนคงคลัง |

# Joins
เชื่อม [authors](authors.md) ผ่าน `author_id` — ดู [Books → Authors](../references/joins/books__authors.md)
stock ต่ำ → [restock runbook](../playbooks/low-stock-runbook.md)
```

ทำแบบเดียวกันกับ `authors`, `references/metrics/monthly-revenue`, `references/joins/books__authors`,
`playbooks/low-stock-runbook` แล้วอัปเดต `wiki/index.md` + `wiki/log.md`

> ในงานจริง: วาง source ลง `raw/` แล้วให้ agent ทำ INGEST แบบมีคนกำกับ ([บท Ingest](./ingest.md)) — agent จะดึงประเด็น แสดงให้อนุมัติ แล้วเขียน concept + อัปเดต index/log ให้

KB ที่ได้เป็นกราฟแบบนี้:

<pre class="mermaid">
flowchart LR
  D["datasets/bookstore"] --> B["tables/books"]
  D --> A["tables/authors"]
  B -->|author_id| A
  J["references/joins/books__authors"] --> B
  J --> A
  M["references/metrics/monthly-revenue"] --> D
  P["playbooks/low-stock-runbook"] --> B
</pre>

## 3. ตรวจ conformance

```bash
python3 tools/okf-validate.py ./wiki
# → ✓ CONFORMANT with OKF v0.1  (0 warning(s), 0 info)
```

## 4. ค้นหา

```bash
python3 tools/okf-index.py build ./wiki                       # สร้าง BM25 index
python3 tools/okf-search.py "how to join books to authors" --bundle ./wiki
# → references/joins/books__authors  [Reference]   อันดับ 1
```

เพิ่ม semantic (ไม่บังคับ, on-prem):
```bash
ollama pull nomic-embed-text
python3 tools/okf-embed.py build ./wiki
python3 tools/okf-search.py "who wrote the novels" --bundle ./wiki
# → mode: hybrid (bm25+semantic, RRF) — จับ authors ได้แม้ไม่มีคำตรงกัน
```

## 5. ดูกราฟ

```bash
python3 tools/okf-viz.py ./wiki --name "Bookstore KB"
open wiki/viz.html        # ไฟล์เดียว เปิด offline ได้
```

## 6. (ทีม) แชร์ผ่าน MCP

ทำให้ทั้งทีม/agent ใช้ร่วมกัน: commit `wiki/` ขึ้น git ภายใน แล้วยก [MCP server](../part6/self-host.md)
ชี้มาที่ bundle นี้ — agent จะ `okf_search` แบบ hybrid และเสนอแก้ผ่าน PR/lease ได้

## สรุปลำดับ

```text
okf-init → (ingest concepts) → okf-validate → okf-index/okf-search → okf-viz → [MCP share]
```

ครบลูปแล้ว! ต่อไปดู[แนวทางการเขียนที่ดี](../part5/best-practices.md) เพื่อให้ KB โตอย่างมีคุณภาพ

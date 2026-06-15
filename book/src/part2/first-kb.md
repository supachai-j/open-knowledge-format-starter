# สร้าง knowledge base แรก

มาสร้าง OKF bundle แรกกันภายในไม่กี่นาที

## ขั้นที่ 1 — scaffold โครงสร้าง

ใช้ `okf-init.py` สร้างโครง bundle ใหม่ในโฟลเดอร์ปัจจุบัน (หรือโฟลเดอร์ที่ระบุ):

```bash
python3 tools/okf-init.py .            # สร้างในโฟลเดอร์ปัจจุบัน
# หรือถ้าติดตั้งเป็น skill:
python3 ~/.claude/skills/okf/scripts/okf-init.py ./my-kb
```

ผลลัพธ์:

```text
Scaffolding OKF bundle in /path/to/project
  wrote: AGENTS.md
  wrote: raw/README.md
  wrote: wiki/index.md
  wrote: wiki/log.md
  wrote: wiki/getting-started.md
✓ done. Next: validate with okf-validate.py, then ingest sources from raw/.
```

> **ปลอดภัย:** ถ้ามี `wiki/` ที่ไม่ว่างอยู่แล้ว สคริปต์จะ **ไม่เขียนทับ** เว้นแต่ใส่ `--force`

## ขั้นที่ 2 — ตรวจ conformance

```bash
python3 tools/okf-validate.py ./wiki
# → ✓ CONFORMANT with OKF v0.1  (0 warning(s), 0 info)
```

## ขั้นที่ 3 — ดู graph

```bash
python3 tools/okf-viz.py ./wiki --name "My First KB"
# → wiki/viz.html  (ไฟล์เดียว เปิดในเบราว์เซอร์ได้ทันที ไม่ต้องต่อเน็ต)
```

เปิด `wiki/viz.html` จะเห็น concept เป็นจุด เชื่อมกันด้วยเส้น คลิกดูรายละเอียดได้

## ขั้นที่ 4 — เริ่มเก็บความรู้

1. วางไฟล์ต้นทาง (PDF, โน้ต, export) ลงในโฟลเดอร์ `raw/`
2. บอก AI agent ว่า *"ingest raw/<ไฟล์> เข้า wiki"* — agent จะดึงประเด็นสำคัญมาให้คุณอนุมัติก่อนเขียน
   (รายละเอียดในบท [Ingest](../part4/ingest.md))

## เขียนเองด้วยมือก็ได้

OKF คือ Markdown ธรรมดา — สร้าง concept เองได้เลย เช่นไฟล์ `wiki/glossary/wau.md`:

```markdown
---
type: Metric
title: Weekly Active Users (WAU)
description: จำนวนลูกค้าไม่ซ้ำที่มีคำสั่งซื้ออย่างน้อย 1 ครั้งในรอบ 7 วัน
tags: [growth, metric]
timestamp: 2026-06-15T00:00:00Z
---

# นิยาม
นับ `customer_id` ไม่ซ้ำ ที่มีออเดอร์อย่างน้อย 1 ครั้งในหน้าต่าง 7 วันล่าสุด
```

แล้วรัน `okf-validate.py` อีกครั้งเพื่อยืนยันว่ายัง conformant

## สรุปคำสั่งที่ใช้บ่อย

| ทำอะไร | คำสั่ง |
|--------|--------|
| สร้าง bundle ใหม่ | `okf-init.py <dir>` |
| ตรวจ conformance | `okf-validate.py ./wiki` |
| ดู graph | `okf-viz.py ./wiki` |
| สร้าง index ค้นหา | `okf-index.py build ./wiki` |
| ค้นหา | `okf-search.py "คำถาม" --bundle ./wiki` |

ต่อไปทำความเข้าใจ [โครงสร้างโปรเจกต์](./project-layout.md) ที่ scaffold ให้

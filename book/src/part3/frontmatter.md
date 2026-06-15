# Frontmatter (เมทาดาทา)

**Frontmatter** คือบล็อก YAML บนหัวไฟล์ คั่นด้วย `---` เก็บ metadata ที่ต้องการให้ค้น/กรอง/ทำดัชนีได้

```yaml
---
type: BigQuery Table              # บังคับ
title: Orders                     # แนะนำ
description: หนึ่งแถวต่อหนึ่งคำสั่งซื้อ   # แนะนำ
resource: https://...             # แนะนำ (ถ้ามีของจริงให้ชี้)
tags: [sales, orders]             # แนะนำ
timestamp: 2026-06-15T00:00:00Z   # แนะนำ (ISO 8601)
---
```

## ฟิลด์ที่บังคับ

| ฟิลด์ | คำอธิบาย |
|-------|----------|
| **`type`** | ชนิดของ concept — เป็น **ฟิลด์เดียวที่บังคับ** ใน v0.1 ผู้บริโภคใช้ค่านี้ในการ route/filter/แสดงผล |

## ฟิลด์ที่แนะนำ (เรียงตามความสำคัญ)

| ฟิลด์ | คำอธิบาย |
|-------|----------|
| `title` | ชื่อสำหรับมนุษย์อ่าน ถ้าไม่ใส่ ผู้บริโภคอาจเดาจากชื่อไฟล์ |
| `description` | สรุปหนึ่งบรรทัด — **นี่คือสิ่งที่ agent อ่านเพื่อตัดสินใจว่าจะโหลดไฟล์นี้ไหม** เขียนให้คม |
| `resource` | URI ของของจริงที่ concept อธิบาย (ละได้ถ้าเป็นแนวคิดนามธรรม) |
| `tags` | YAML list สำหรับจัดหมวดข้ามสายงาน เช่น `[sales, revenue]` |
| `timestamp` | เวลาที่แก้ครั้งสำคัญล่าสุด (รูปแบบ ISO 8601) |

> 💡 **`description` สำคัญกว่าที่คิด** — เขียนให้เจาะจง เช่น
> *"จำนวนลูกค้าไม่ซ้ำที่มีออเดอร์ ≥1 ใน 7 วัน"* ดีกว่า *"เรื่อง WAU"*

## ฟิลด์เสริม (extension fields)

ผู้ผลิต **เพิ่มฟิลด์อะไรก็ได้** และผู้บริโภค **ต้องทนต่อ key ที่ไม่รู้จัก** (ไม่ปฏิเสธไฟล์)
เช่นเพิ่ม `owner`, `sla`, `pii: true` ตามโดเมนของคุณ

## controlled vocabulary ของ `type`

แม้สเปกไม่บังคับ taxonomy แต่ **ควรใช้ค่า `type` ให้สม่ำเสมอ** (ไม่งั้นเครื่องรวมข้อมูลไม่ได้)
ชุดที่ starter นี้ใช้:

`BigQuery Table` · `BigQuery Dataset` · `Metric` · `Reference` · `Playbook` · `API Endpoint` · `Concept` · `Entity`

> **ขนบจาก reference bundle ของ Google:** ความรู้สังเคราะห์/อ้างอิง (join, นิยาม metric, glossary)
> มักจัดไว้ใต้ `references/` และตั้ง `type: Reference` ส่วนของจับต้องได้อยู่ `tables/` / `datasets/`

## ข้อควรระวัง

- **อย่ายัด frontmatter เกินจำเป็น** — เก็บให้เป็น semantic (entity, intent, นิยาม) อย่าทุ่ม keyword
  เพราะ noise ลดคุณภาพการค้น
- **ใช้ชื่อฟิลด์ให้สม่ำเสมอ** — ไฟล์หนึ่งใช้ `author_name` อีกไฟล์ใช้ `written_by` เครื่องรวมข้อมูลไม่ได้

## Body ใต้ frontmatter

ส่วนเนื้อหาเป็น Markdown อิสระ แต่ **ควรใช้โครงสร้าง** (heading, bullet, ตาราง) มากกว่าย่อหน้ายาว ๆ
heading ที่เป็นขนบ (ใช้เมื่อเหมาะ เรียงตามนี้):

`# Overview` → `# Schema` → `# Common query patterns` (โค้ด `sql`) → `# Joins` → `# Examples` → `# Citations`

ต่อไปดูวิธีเชื่อม concept เข้าด้วยกัน → [การลิงก์เป็น knowledge graph](./linking.md)

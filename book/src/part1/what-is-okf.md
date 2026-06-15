# OKF คืออะไร

**Open Knowledge Format (OKF)** คือสเปกแบบเปิดสำหรับเก็บ "ความรู้" ขององค์กรในรูปของ
**ไดเรกทอรีของไฟล์ Markdown ที่มี YAML frontmatter** เพื่อให้ทั้งคนและ AI agent เขียน อ่าน
แลกเปลี่ยน และใช้งานได้ — โดยไม่ต้องมี SDK, ฐานข้อมูล, หรือเครื่องมือเฉพาะทาง

> ถ้าคุณ `cat` ไฟล์ได้ คุณก็อ่าน OKF ได้ · ถ้าคุณ `git clone` repo ได้ คุณก็ส่งต่อ OKF ได้

## ที่มา

OKF v0.1 เผยแพร่เมื่อ **12 มิถุนายน 2026** โดยทีม Data Cloud ของ **Google Cloud**
(Sam McVeety และ Amir Hormati) เป็นการทำให้ **"LLM-wiki pattern"** ที่ Andrej Karpathy
เสนอไว้ กลายเป็นมาตรฐานที่พกพาได้และเป็นกลาง (vendor-neutral)

แนวคิด LLM-wiki คือ: แทนที่จะให้ LLM ไปค้นเอกสารดิบใหม่ทุกครั้งที่ถาม ให้ AI **ค่อย ๆ
สังเคราะห์ความรู้ลงเป็นหน้า Markdown ที่จัดระเบียบและเชื่อมโยงกันไว้ล่วงหน้า** แล้วโหลด
หน้าที่เกี่ยวข้องเข้า context ตรง ๆ

## องค์ประกอบหลัก (ดูละเอียดในภาคที่ 3)

| คำ | ความหมายสั้น ๆ |
|----|----------------|
| **Bundle** | ไดเรกทอรีของไฟล์ความรู้ทั้งหมด — หน่วยที่ใช้แจกจ่าย |
| **Concept** | ความรู้หนึ่งหน่วย = ไฟล์ `.md` หนึ่งไฟล์ (เช่น ตาราง, metric, playbook) |
| **Concept ID** | path ของไฟล์ใน bundle ตัด `.md` ออก เช่น `tables/orders.md` → `tables/orders` |
| **Frontmatter** | บล็อก YAML บนหัวไฟล์ (เก็บ metadata เช่น `type`, `title`, `tags`) |
| **Link** | ลิงก์ Markdown ระหว่าง concept = สร้างความสัมพันธ์เป็น graph |

## ตัวอย่าง concept หนึ่งไฟล์

ไฟล์ `tables/orders.md`:

```markdown
---
type: BigQuery Table
title: Orders
description: หนึ่งแถวต่อหนึ่งคำสั่งซื้อของลูกค้า
tags: [sales, orders]
timestamp: 2026-06-15T00:00:00Z
---

# Schema
| Column | Type | Description |
| :--- | :--- | :--- |
| order_id | STRING | รหัสคำสั่งซื้อ (unique) |
| customer_id | STRING | FK ไปยัง [customers](customers.md) |

# Joins
เชื่อมกับ [customers](customers.md) ผ่าน `customer_id`
```

จะเห็นว่ามันคือ Markdown ธรรมดาที่อ่านออกได้ทันที — แค่มีหัว YAML เล็ก ๆ และมีลิงก์ไปยัง concept อื่น

## หลักการออกแบบ 3 ข้อ

1. **บังคับน้อยที่สุด (minimally opinionated)** — frontmatter บังคับแค่ฟิลด์ `type` เดียว ที่เหลือผู้ผลิตกำหนดเอง
2. **ผู้ผลิตกับผู้บริโภคแยกอิสระ** — bundle ที่คนเขียนด้วยมือ, agent สร้าง, หรือ pipeline export มา ล้วนถูกอ่านได้ด้วยเครื่องมือใดก็ได้
3. **เป็นกราฟ ไม่ใช่แค่ต้นไม้** — concept เชื่อมกันด้วยลิงก์ Markdown เกิดเป็นความสัมพันธ์ที่รวยกว่าโครงสร้างโฟลเดอร์

## OKF ไม่ใช่อะไร

- ไม่ใช่ taxonomy ตายตัว — ไม่ได้กำหนดว่าต้องมี type อะไรบ้าง
- ไม่ได้กำหนดว่าต้องเก็บ/เสิร์ฟ/ค้นด้วยโครงสร้างพื้นฐานแบบไหน
- ไม่ได้มาแทน schema เฉพาะทาง (Avro, Protobuf, OpenAPI) — OKF **อ้างอิง** ถึงพวกนั้น ไม่ได้กลืนมันเข้าไป

ต่อไปเราจะดูว่า **ทำไม** ถึงเลือก OKF แทนการทำ RAG แบบเดิม → [ทำไมต้อง OKF](./why-okf.md)

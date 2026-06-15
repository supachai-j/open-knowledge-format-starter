# เพิ่มและแก้ไข concept

## เริ่มจาก template

ใช้ `tools/concept-template.md` เป็นจุดเริ่ม:

```markdown
---
type: Concept            # บังคับ — เลือกจาก controlled vocabulary ใน AGENTS.md
title: <ชื่อสำหรับมนุษย์>
description: <สรุปหนึ่งบรรทัด — ใช้ตัดสินใจว่า agent จะโหลดไฟล์นี้ไหม>
resource: <URI ของของจริง หรือลบบรรทัดนี้ถ้าเป็นนามธรรม>
tags: [<tag1>, <tag2>]
timestamp: 2026-06-15T00:00:00Z   # ISO 8601 UTC
---

# <หัวข้อ>
ใช้โครงสร้าง: heading, bullet สั้น ๆ, ตาราง มากกว่าย่อหน้ายาว

# Related
ลิงก์ concept อื่นด้วย relative path เช่น [orders](../tables/orders.md)
ชนิดความสัมพันธ์อยู่ในประโยคนี้ ไม่ใช่ที่ตัวลิงก์

# Citations
อ้างอิงแหล่งใน raw/ ที่ใช้สังเคราะห์ concept นี้
```

## ขั้นตอนเพิ่ม/แก้ concept

1. คัดลอก template → ตั้งชื่อไฟล์ (kebab-case, นิ่ง)
2. ตั้ง `type` ให้ถูก (จาก controlled vocabulary)
3. เขียน body ใช้โครงสร้าง + ลิงก์ relative
4. อัปเดต `tags` + `timestamp`
5. อัปเดต `index.md` ของไดเรกทอรีนั้น
6. เพิ่มรายการลง `wiki/log.md`
7. รัน `okf-validate.py`

## ลำดับ section ที่เป็นขนบ

ใช้เมื่อเหมาะ เรียงตามนี้ (มาจาก enrichment prompt ของ Google):

```markdown
# Overview                  ← เกริ่น 1–3 ย่อหน้า: คืออะไร ใช้ยังไง
# Schema                    ← สรุปคอลัมน์/ฟิลด์ (RECORD ซ้อนให้ย่อหน้า/ตาราง)
# Common query patterns     ← 1–3 SQL snippet (โค้ด sql)
# Joins                     ← เชื่อมกับ concept ไหน ผ่าน key อะไร
# Citations                 ← แหล่งอ้างอิง (รูปแบบ [1] [Title](url))
```

## ตัวอย่าง concept แบบ Reference (join)

ไฟล์ `wiki/references/joins/orders__customers.md`:

````markdown
---
type: Reference
title: Orders → Customers join
description: วิธี join ตาราง orders กับ customers ผ่าน customer_id
tags: [join, sales]
timestamp: 2026-06-15T00:00:00Z
---

Join [orders](../../tables/orders.md) กับ [customers](../../tables/customers.md)
ผ่าน `customer_id` (หลายออเดอร์ → ลูกค้าหนึ่งคน)

# Common query patterns
```sql
SELECT c.email, COUNT(*) AS orders, SUM(o.total) AS ltv
FROM orders o JOIN customers c USING (customer_id)
GROUP BY c.email;
```
````

## หลังแก้เสร็จ — Definition of Done

- [ ] concept มี `type` ไม่ว่าง และ `description` ที่คม
- [ ] อัปเดต `timestamp` เป็นปัจจุบัน
- [ ] อัปเดต `index.md` ที่เกี่ยวข้อง
- [ ] เพิ่มรายการใน `log.md` ใต้วันที่วันนี้
- [ ] `python3 tools/okf-validate.py ./wiki` ผ่าน

ต่อไป: ตรวจสอบและมองเห็น wiki → [Validate และ Visualize](./validate-viz.md)

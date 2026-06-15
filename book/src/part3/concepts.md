# Bundle, Concept และ Concept ID

สามคำนี้คือหัวใจของ OKF เข้าใจสามคำนี้ก็เข้าใจสเปกครึ่งหนึ่งแล้ว

## Bundle (มัด/ชุดความรู้)

**Bundle** คือไดเรกทอรีของไฟล์ความรู้ทั้งหมด — เป็น **หน่วยที่ใช้แจกจ่าย** (unit of distribution)
หนึ่ง bundle อาจส่งต่อได้หลายรูปแบบ:

- เป็น **git repository** (แนะนำ — ได้ history, diff, review ฟรี)
- เป็น tarball / zip
- เป็นไดเรกทอรีย่อยใน repo ที่ใหญ่กว่า

ในโปรเจกต์นี้ bundle คือโฟลเดอร์ `wiki/`

## Concept (หน่วยความรู้)

**Concept** คือความรู้หนึ่งหน่วย แทนด้วย **ไฟล์ Markdown หนึ่งไฟล์** มันอาจอธิบาย:

- ของที่จับต้องได้ — ตารางในฐานข้อมูล, API endpoint
- ของที่เป็นนามธรรม — metric ทางธุรกิจ, playbook, กระบวนการ

**กฎทอง: หนึ่งไฟล์ = หนึ่ง concept** อย่ายัด 3 เรื่องลงไฟล์เดียว

concept มี 2 ส่วน:

```markdown
---
type: Metric          ← (1) Frontmatter — บล็อก YAML
title: ...
---
                      ← (2) Body — Markdown อิสระ
# นิยาม
...
```

## Concept ID (รหัสประจำ concept)

**Concept ID = path ของไฟล์ใน bundle ตัด `.md` ออก**

| ไฟล์ (ใน `wiki/`) | Concept ID |
|-------------------|------------|
| `tables/orders.md` | `tables/orders` |
| `references/metrics/wau.md` | `references/metrics/wau` |
| `playbooks/incident.md` | `playbooks/incident` |

จุดสำคัญ: **identity ผูกกับ path ของไฟล์** ดังนั้น...

> ⚠️ **การเปลี่ยนชื่อ/ย้ายไฟล์ = เปลี่ยน Concept ID = ลิงก์ที่ชี้เข้ามาพัง**
> ตั้งชื่อไฟล์ให้นิ่งตั้งแต่แรก ใช้ตัวพิมพ์เล็ก-คั่นด้วยขีด (kebab-case) เช่น `weekly-active-users.md`

ข้อดีของการใช้ path เป็น identity: ได้ **identity แบบ sovereign** โดยไม่ต้องมี registry กลาง —
แค่ดูที่อยู่ไฟล์ก็รู้ว่าเป็น concept อะไร

## โครงสร้างเป็นต้นไม้ แต่ความสัมพันธ์เป็นกราฟ

โฟลเดอร์ให้โครงสร้างแบบต้นไม้ (พ่อ-ลูก) แต่ concept เชื่อมกันด้วย **ลิงก์ Markdown** ได้อิสระ
เกิดเป็น **กราฟ** ที่รวยกว่าโครงสร้างโฟลเดอร์ (ดูบท [การลิงก์](./linking.md))

```text
wiki/
├── tables/orders.md ─────┐ (ลิงก์ "joins-with")
├── tables/customers.md ◄─┘
└── references/metrics/wau.md ──► tables/orders.md ("derived-from")
```

ต่อไปดูส่วนหัวของไฟล์ให้ละเอียด → [Frontmatter](./frontmatter.md)

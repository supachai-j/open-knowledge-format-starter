# ไฟล์สงวน: index.md และ log.md

OKF สงวนชื่อไฟล์ไว้ 2 ชื่อ ที่มีความหมายพิเศษในทุกระดับของไดเรกทอรี และ
**ห้ามใช้เป็นไฟล์ concept**

| ไฟล์ | หน้าที่ |
|------|---------|
| `index.md` | สารบัญของไดเรกทอรี (progressive disclosure) |
| `log.md` | บันทึกประวัติการเปลี่ยนแปลง |

## `index.md` — สารบัญเพื่อ progressive disclosure

ช่วยให้คน/agent **เห็นว่ามีอะไรบ้างก่อนเปิดไฟล์จริง** — สำคัญมากเพราะช่วยไม่ให้ context window
ล้นตอนสำรวจ agent อ่าน `index.md` ก่อนเพื่อหา concept ที่เกี่ยว แล้วค่อยเจาะเข้าไฟล์

รูปแบบ: ไม่มี frontmatter (ยกเว้น root index — ดูด้านล่าง) เนื้อหาเป็นหัวข้อ + รายการ
`* [ชื่อ](ลิงก์) - คำอธิบายสั้น`

```markdown
# Subdirectories

* [tables](tables/index.md) - BigQuery tables และ schema/join
* [references](references/index.md) - ความรู้สังเคราะห์ (join, นิยาม metric)

# Concepts

* [tables/orders](tables/orders.md) - หนึ่งแถวต่อหนึ่งคำสั่งซื้อ
```

> ผู้ผลิตจะ **gen `index.md` อัตโนมัติ** ก็ได้ ผู้บริโภคจะ **สร้างเองตอนอ่าน** ก็ได้ ถ้าไม่มี

### `okf_version` ที่ root index

ที่ **root ของ bundle เท่านั้น** `index.md` สามารถมี frontmatter ได้ — และมีได้แค่ฟิลด์เดียวคือ
`okf_version` เพื่อประกาศเวอร์ชันสเปกที่ bundle นี้ยึด:

```markdown
---
okf_version: "0.1"
---
# Concepts
...
```

## `log.md` — บันทึกประวัติ

บันทึกการเปลี่ยนแปลงของขอบเขตนั้น เป็นรายการ **เรียงใหม่สุดขึ้นก่อน** จัดกลุ่มด้วยหัววันที่ ISO

```markdown
# Directory Update Log

## 2026-06-15
* **Update**: เพิ่มตาราง [Customer Metrics](references/metrics/cm.md)
* **Creation**: สร้าง [Dataplex Playbook](playbooks/dataplex.md)

## 2026-06-12
* **Initialization**: สร้างโครงสร้างไดเรกทอรีพื้นฐาน
```

กฎ:

- หัววันที่ **ต้อง** เป็นรูปแบบ ISO `YYYY-MM-DD` (**ไม่มีวงเล็บ**)
- คำขึ้นต้นตัวหนา (`**Update**`, `**Creation**`, `**Deprecation**`) เป็น **ขนบ ไม่ใช่ข้อบังคับ**

> 💡 ถ้าใช้ prefix สม่ำเสมอ จะ grep ได้ง่าย เช่น `grep '^- ' log.md` ดูรายการล่าสุด

## ทำไมไฟล์สองตัวนี้สำคัญ

- `index.md` = **ตัวนำทาง** ให้ agent ไม่ต้องโหลดทั้ง bundle เข้า context
- `log.md` = **audit trail** ที่อ่านง่าย ช่วยให้รู้ว่า wiki วิวัฒน์มายังไง และช่วย agent เข้าใจว่าเพิ่งทำอะไรไป

> `okf-validate.py` จะตรวจว่า `index.md` ไม่มี frontmatter (ยกเว้น root ที่มีได้แค่ `okf_version`)
> และเตือนถ้าหัววันที่ใน `log.md` ไม่ใช่รูปแบบ ISO

จบภาคแนวคิดหลักแล้ว ต่อไปลงมือใช้งานจริง → [Ingest: เก็บความรู้เข้า wiki](../part4/ingest.md)

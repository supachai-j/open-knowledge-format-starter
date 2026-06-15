# การลิงก์เป็น knowledge graph

concept เชื่อมกันด้วย **ลิงก์ Markdown มาตรฐาน** ทำให้ไดเรกทอรีกลายเป็น **กราฟของความสัมพันธ์**
ที่รวยกว่าโครงสร้างพ่อ-ลูกของโฟลเดอร์

## ใช้ลิงก์แบบ file-relative เท่านั้น

```markdown
ดูตาราง [customers](../tables/customers.md) สำหรับ key ที่ใช้ join
```

> ⚠️ **อย่าขึ้นต้นลิงก์ด้วย `/`** — นี่คือกฎที่สำคัญและละเอียดอ่อน
>
> สเปก OKF §5.1 *แนะนำ* ลิงก์แบบ absolute (`/tables/customers.md`) โดยอ้างว่าเสถียรเมื่อย้ายไฟล์
> **แต่ enrichment agent ตัวจริงของ Google สั่งห้าม** เพราะลิงก์ `/` **ทำให้ GitHub render พัง**
> และ bundle จริงทุกตัวของ Google ก็ใช้ลิงก์ **relative** ทั้งหมด
>
> **เราทำตาม implementation จริง: ใช้ relative เท่านั้น** (`okf-validate.py` จะเตือนถ้าเจอลิงก์ `/`)

## ลิงก์เป็นแบบ "ไม่มีชนิด" (untyped)

ลิงก์จาก concept A → B แค่ "ยืนยันว่ามีความสัมพันธ์" แต่ **ชนิดของความสัมพันธ์**
(พ่อ-ลูก, อ้างอิง, joins-with, depends-on) อยู่ใน **เนื้อความรอบ ๆ ไม่ใช่ตัวลิงก์**

```markdown
เชื่อมกับ [customers](../tables/customers.md) ผ่าน `customer_id` (หลายออเดอร์ → ลูกค้าหนึ่งคน)
        └─ ลิงก์ untyped         └─ ชนิดความสัมพันธ์อยู่ในประโยคนี้
```

ผู้บริโภคที่สร้าง graph view จะมองทุกลิงก์เป็น "เส้นเชื่อมมีทิศทาง" แบบไม่ระบุชนิด

## ลิงก์เสียได้ (broken links อนุญาต)

ลิงก์ที่ชี้ไปยัง concept ที่ **ยังไม่มี** ไม่ถือว่าผิด — มันแทน **"ความรู้ที่ยังไม่ได้เขียน"**
(เหมือน placeholder/ช่องว่างให้เติมทีหลัง) ผู้บริโภค **ต้องทนต่อ broken link**

## กฎการลิงก์ที่ดี

- ✅ ใช้ relative path เท่านั้น (`../tables/orders.md`, `customers.md`)
- ✅ ลิงก์เฉพาะ concept ที่มีอยู่จริง (หรือจงใจทิ้ง placeholder)
- ❌ อย่า over-link — ลิงก์ครั้งเดียวต่อการกล่าวถึงต่อ section ก็พอ
- ❌ อย่าลิงก์จาก **heading**, ใน **code block**, หรือในรายการชื่อฟิลด์ schema
- ❌ อย่าลิงก์ไฟล์หาตัวเอง

## ตัวอย่าง: graph เล็ก ๆ

```text
references/joins/orders__customers.md
   ├──► tables/orders.md
   └──► tables/customers.md

metrics/weekly-active-users.md ──► tables/orders.md
playbooks/incident-response.md ──► metrics/weekly-active-users.md
```

เมื่อเปิด `viz.html` คุณจะเห็นกราฟนี้แบบ interactive พร้อม **"Cited by"** (backlink — ใครลิงก์มาหา concept นี้บ้าง)

ต่อไปดูไฟล์พิเศษ 2 ตัวที่ช่วยนำทางกราฟ → [ไฟล์สงวน: index.md และ log.md](./reserved-files.md)

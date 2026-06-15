# โครงสร้างโปรเจกต์

OKF starter ใช้แนวคิด **สถาปัตยกรรม 3 ชั้น** ที่แยกหน้าที่ชัดเจน

```text
my-kb/
├── AGENTS.md          ← ชั้นที่ 3: schema + กฎการทำงานของ agent (อ่านก่อน)
├── raw/               ← ชั้นที่ 1: แหล่งข้อมูลดิบ (อ่านอย่างเดียว)
│   └── README.md
├── wiki/              ← ชั้นที่ 2: OKF bundle (agent ดูแล)
│   ├── index.md       ← ไฟล์สงวน: สารบัญ (progressive disclosure)
│   ├── log.md         ← ไฟล์สงวน: บันทึกการเปลี่ยนแปลง
│   └── getting-started.md
└── tools/             ← เครื่องมือ (validate, viz, index, ...)
```

## สามชั้นคืออะไร

| ชั้น | โฟลเดอร์ | ใครเขียน | บทบาท |
|------|----------|----------|-------|
| 1. แหล่งดิบ | `raw/` | คน | ต้นทางความจริง — **อ่านอย่างเดียว** agent ไม่แก้ |
| 2. wiki | `wiki/` | agent | ความรู้ที่สังเคราะห์แล้ว (OKF bundle) |
| 3. schema | `AGENTS.md` | คน + agent ร่วมกัน | กฎ/ขนบ/workflow ที่กำกับ agent |

แนวคิดสำคัญ: **`wiki/` คือ "bundle root"** ดังนั้น Concept ID จะนับจาก `wiki/` เช่น
`wiki/tables/orders.md` มี Concept ID = `tables/orders`

## `AGENTS.md` — ไฟล์ที่สำคัญที่สุด

นี่คือไฟล์แรกที่ agent อ่าน มันบอก agent ว่า:

- โครงสร้าง bundle เป็นยังไง
- กฎ frontmatter (ฟิลด์ไหนบังคับ/แนะนำ, controlled vocabulary ของ `type`)
- กฎการลิงก์ (ใช้ relative, ห้ามขึ้นต้นด้วย `/`)
- workflow ของ ingest / query / validate

> ไฟล์นี้คือสิ่งที่ทำให้ AI เป็น "ผู้ดูแล wiki ที่มีวินัย" แทนที่จะเป็น chatbot ทั่วไป
> คุณกับ agent จะค่อย ๆ พัฒนาไฟล์นี้ร่วมกันตามโดเมนของคุณ

ถ้าคุณใช้ agent อื่น ชื่อไฟล์อาจเป็น `CLAUDE.md` (Claude Code) หรือ `GEMINI.md` ก็ได้ — เนื้อหาเหมือนกัน

## `raw/` — แหล่งข้อมูลดิบ

วางต้นฉบับไว้ที่นี่: PDF, โน้ตประชุม, export, dataset

- **เปลี่ยนแปลงไม่ได้ (immutable)** — agent อ่านแต่ไม่แก้ นี่คือต้นทางความจริง
- ไฟล์ใน `raw/` **ไม่ใช่ส่วนหนึ่งของ bundle** (bundle คือ `wiki/`) แต่เป็น "input" ของการ ingest
- ใน starter ตัวจริง `.gitignore` จะ **ไม่ commit ไฟล์ใน `raw/`** เพื่อกันเผลอ push ข้อมูลส่วนตัว/ใหญ่
  (เก็บแค่ `raw/README.md`) — ถ้าอยาก version คุม source จริง ให้คอมเมนต์บรรทัด `raw/*` ออก

## `wiki/` — OKF bundle

โฟลเดอร์นี้ agent เป็นเจ้าของ มันจะจัด concept เป็นหมวด เช่นในโครงเริ่มต้นจะมี:

```text
wiki/
├── index.md              ← สารบัญ root (มี okf_version)
├── log.md                ← บันทึกการเปลี่ยนแปลง
├── getting-started.md    ← concept ตัวอย่าง
└── (ของคุณ) tables/  references/  playbooks/ ...
```

หมวดที่เจอบ่อย (ตาม reference implementation ของ Google):

- `tables/` — ตาราง (`type: BigQuery Table`)
- `datasets/` — ชุดข้อมูล (`type: BigQuery Dataset`)
- `references/` — ความรู้สังเคราะห์ เช่น `references/metrics/`, `references/joins/` (`type: Reference`)

ต่อไปเจาะลึกแนวคิดหลัก เริ่มที่ [Bundle, Concept และ Concept ID](../part3/concepts.md)

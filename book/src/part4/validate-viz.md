# Validate และ Visualize

## Validate — ตรวจ conformance

รันหลังแก้ทุกครั้ง:

```bash
python3 tools/okf-validate.py ./wiki
# → ✓ CONFORMANT with OKF v0.1  (0 warning(s), 0 info)
```

### เกณฑ์ conformance (OKF v0.1)

bundle ผ่านเมื่อ:

1. ทุกไฟล์ `.md` ที่ไม่ใช่ไฟล์สงวน มี **YAML frontmatter ที่ parse ได้**
2. ทุก frontmatter มีฟิลด์ **`type` ที่ไม่ว่าง**
3. ไฟล์สงวน (`index.md`, `log.md`) ที่มีอยู่ ทำตามโครงสร้างที่กำหนด

### ระดับของผลตรวจ

| ระดับ | ความหมาย | ตัวอย่าง |
|-------|----------|----------|
| ✗ **error** | ไม่ conformant (ต้องแก้) | ไม่มี frontmatter / ไม่มี `type` / index.md มี frontmatter ผิดกฎ |
| ! **warn** | ผ่าน แต่ควรแก้ | ลิงก์ขึ้นต้นด้วย `/` (พัง GitHub) / หัว log ไม่ใช่ ISO |
| · **info** | ไม่ใช่ปัญหา | broken link (สเปก §5.3 อนุญาต) |

> ผู้บริโภค **ต้องไม่ปฏิเสธ** bundle เพราะ: ฟิลด์ optional หาย, `type` แปลก, key เกิน, ลิงก์เสีย,
> หรือไม่มี `index.md` — นี่คือ "permissive consumption" ที่ทำให้ OKF ยังใช้ได้แม้ bundle โต/ถูก refactor

## Visualize — ดู knowledge graph

```bash
python3 tools/okf-viz.py ./wiki --name "My Wiki"
# → wiki/viz.html  (ไฟล์เดียว เปิดในเบราว์เซอร์)
```

`viz.html` เป็น **ไฟล์ HTML เดียวที่ self-contained** — ฝังไลบรารี (Cytoscape + marked) และข้อมูล bundle
ไว้ในตัว **ไม่ดึงอะไรจากเน็ตตอนเปิด** เหมาะกับ air-gap แชร์เป็นไฟล์ หรือ commit ไว้ข้าง bundle

### สิ่งที่ viewer แสดง

- **กราฟ force-directed** ของทุก concept ระบายสีตาม `type` เส้นเชื่อมตามลิงก์ในเนื้อหา
- **แผงรายละเอียด** ของ concept ที่เลือก: frontmatter + body ที่ render แล้ว
- **"Cited by"** — backlink (ใครลิงก์มาหา concept นี้บ้าง)
- **ช่องค้นหา** (จับ title/id/tags), **ตัวกรองตาม type**, สลับ layout ได้

> ค่าเริ่มต้นจะ **ฝังไลบรารีจาก `tools/vendor/`** ทำให้ air-gap ได้จริง ถ้าต้องการใช้ CDN ใส่ `--cdn`

### ลองเล่นของจริง

ด้านล่างคือ `viz.html` ของ wiki ตัวอย่างในโปรเจกต์นี้ (คลิกที่ node เพื่อดูรายละเอียด ลองค้นหา/กรองตาม type ได้):

<iframe src="../viz-example.html" title="OKF graph ตัวอย่าง" loading="lazy" style="width:100%;height:520px;border:1px solid var(--table-border-color,#ddd);border-radius:12px;margin:0.5rem 0;"></iframe>

[เปิดแบบเต็มจอ →](../viz-example.html)

## ทำให้เป็นนิสัย

รวมสองคำสั่งนี้หลังการแก้ทุกครั้ง:

```bash
python3 tools/okf-validate.py ./wiki && python3 tools/okf-viz.py ./wiki
```

ในระดับองค์กร CI จะรัน validate ทุก PR และ regenerate viz อัตโนมัติ (ดูภาคที่ 6)

จบภาคการใช้งานประจำวัน ต่อไปดูแนวทางเขียนให้ดี → [แนวทางการเขียนและ anti-patterns](../part5/best-practices.md)

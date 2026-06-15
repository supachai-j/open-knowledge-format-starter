# Query และ Search

มีสองวิธีในการดึงความรู้ออกมาใช้ ขึ้นกับขนาดของ wiki

## วิธีที่ 1 — Query ผ่าน index (wiki เล็ก)

สำหรับ wiki ขนาดเล็ก (ไม่เกิน ~150 หน้า) การอ่าน `index.md` ก็เพียงพอ:

1. อ่าน `wiki/index.md` ก่อน เพื่อหา concept ที่เกี่ยว
2. เจาะเข้าไฟล์ concept นั้น ๆ
3. ตอบ **จากเฉพาะ concept ที่โหลดมา** และ **อ้าง Concept ID** เสมอ
4. ถ้าไม่มีข้อมูลครอบคลุม ให้บอกตรง ๆ และเสนอให้ ingest แหล่งเพิ่ม

ผ่าน agent: *"wiki ว่ายังไงเรื่อง WAU"* → agent อ่าน index → เปิด concept → ตอบพร้อมอ้างอิง

## วิธีที่ 2 — Search ด้วย index (wiki ใหญ่)

เมื่อเกิน ~150 หน้า การสแกน index จะช้า ให้สร้างดัชนีค้นหา:

```bash
# สร้าง BM25 index (ทำครั้งเดียว / รันใหม่เมื่อเนื้อหาเปลี่ยน)
python3 tools/okf-index.py build ./wiki

# ค้นหา
python3 tools/okf-search.py "how is WAU defined" --bundle ./wiki -k 8
```

ผลลัพธ์ (จัดอันดับด้วย BM25):

```
mode: bm25-only (no embeddings — run okf-embed.py build)
   2.675  metrics/weekly-active-users   [Metric]  จำนวนลูกค้าไม่ซ้ำที่มีออเดอร์...
   2.463  tables/customers              [BigQuery Table]  ...
```

> **BM25 คืออะไร:** อัลกอริทึมค้นแบบ keyword ที่ให้คะแนนความเกี่ยวข้อง ดีมากสำหรับการจับคำ/รหัสตรงตัว
> (เช่น รหัส policy, ชื่อคอลัมน์) เครื่องมือนี้เป็น Python ล้วน ไม่ต้องลง dependency

## Hybrid search (BM25 + semantic)

ถ้า keyword อย่างเดียวยังจับความหมายไม่พอ เพิ่มชั้น semantic ด้วยโมเดล embedding ในเครื่อง (Ollama):

```bash
ollama pull nomic-embed-text          # ครั้งเดียว (on-prem)
python3 tools/okf-embed.py build ./wiki   # สร้าง embeddings → wiki/.okf-embed.json
python3 tools/okf-search.py "ลูกค้าที่ active" --bundle ./wiki
# → mode: hybrid (bm25+semantic, RRF)
```

`okf-search.py` จะ **ฟิวชันผลของ BM25 + semantic ด้วย Reciprocal Rank Fusion (RRF)** เอง

> **ปลอดภัยเสมอ:** ถ้ายังไม่ได้สร้าง embeddings หรือ Ollama ไม่ทำงาน search จะ **fallback เป็น BM25
> อัตโนมัติ** และบอก mode ให้รู้ — semantic เป็น upgrade ล้วน ๆ ไม่ใช่ dependency บังคับ

(รายละเอียดสถาปัตยกรรม hybrid อยู่ในบท [Search ระดับ scale และ semantic](../part6/scaling-search.md))

## เปรียบเทียบ

| สถานการณ์ | ใช้อะไร |
|-----------|---------|
| wiki เล็ก (< ~150 หน้า) | อ่าน `index.md` ตรง ๆ |
| wiki ใหญ่ จับ keyword/รหัส | `okf-search.py` (BM25) |
| ต้องจับความหมาย/พ้องความ | hybrid (BM25 + semantic) |

ต่อไป: วิธีเพิ่มและแก้ไข concept → [เพิ่มและแก้ไข concept](./authoring.md)

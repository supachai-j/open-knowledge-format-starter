# แนวคิดพื้นฐานที่ต้องรู้ (พร้อมตัวอย่าง)

บทนี้สรุปแนวคิดพื้นฐานของระบบ Knowledge Base ที่กล่าวถึงในบท[ประวัติศาสตร์](./history.md) —
แต่ละหัวข้อมี **นิยามสั้น + ตัวอย่างรูปธรรม + เกี่ยวกับ OKF ยังไง** เพื่อให้นำไปใช้ต่อได้ทันที

## 1. Knowledge representation (การแทนความรู้)

**คือ** วิธีเก็บ "สิ่งที่รู้" ให้เครื่องประมวลผลได้ รูปแบบคลาสสิก: production rule (IF-THEN),
semantic network (กราฟแนวคิด), frame (slot-filler)

**ตัวอย่าง** (frame):
```
FRAME: Bacteroides
  IS-A: Anaerobic-Gram-Negative-Rod
  Gram-stain: negative (default)
  Treatment: [metronidazole, clindamycin]
```

**ใน OKF:** แต่ละ concept (ไฟล์ `.md`) คือหน่วยความรู้หนึ่งหน่วย — frontmatter เก็บ field ที่ query ได้, body เก็บรายละเอียด

## 2. Ontology (ออนโทโลยี)

**คือ** ข้อกำหนดความหมายของแนวคิด/ความสัมพันธ์ในโดเมน แบบเครื่องอ่านได้ (มากกว่า taxonomy — มี logic ให้อนุมานได้)

**ตัวอย่าง** (RDF triple): `TimBernersLee — invented — WorldWideWeb` (subject–predicate–object)

**ใน OKF:** ลิงก์ Markdown ระหว่าง concept ทำหน้าที่คล้าย triple แต่ **untyped** — ชนิดความสัมพันธ์อยู่ในเนื้อความ (เบากว่า OWL มาก)

## 3. Inverted index (ดัชนีกลับด้าน)

**คือ** โครงสร้างที่ map "คำ → รายการเอกสารที่มีคำนั้น" หัวใจของ full-text search

**ตัวอย่าง:**
| คำ | เอกสาร |
|----|--------|
| cat | D1, D2 |
| dog | D3 |

ค้น "dog" → ตอบ D3 ทันที โดยไม่ต้องสแกนทุกเอกสาร

**ใน OKF:** `okf-index.py` สร้าง inverted index ในหน่วยความจำเพื่อทำ BM25

## 4. TF-IDF & BM25 (การจัดอันดับความเกี่ยวข้อง)

**คือ** สูตรให้คะแนนว่าเอกสารตรงกับคำค้นแค่ไหน — **TF** (คำนี้ปรากฏบ่อยในเอกสาร) × **IDF** (คำนี้หายากทั้งคลัง = เด่น);
**BM25** ปรับปรุงด้วย length normalization + saturation

**ตัวอย่าง:** คำ "the" อยู่ทุกเอกสาร → IDF = log(3/3) = 0 → คะแนน 0 (ไม่ช่วยแยกแยะ); คำ "dog" อยู่เอกสารเดียว → IDF สูง → เด่น

**ใน OKF:** BM25 คือ search หลักของ `okf-search.py` (เบา ไม่ต้องมี dependency)

## 5. Embeddings (เวกเตอร์ความหมาย)

**คือ** การแปลงข้อความเป็นเวกเตอร์ตัวเลข ที่ "ความหมายใกล้ = เวกเตอร์ใกล้"

**ตัวอย่าง** (word2vec): `king − man + woman ≈ queen` — ความสัมพันธ์เชิงความหมายกลายเป็นเลขคณิตของเวกเตอร์

**ใน OKF:** `okf-embed.py` สร้าง embedding ของ concept ผ่านโมเดลในเครื่อง (Ollama) สำหรับ semantic search

## 6. Vector / semantic search

**คือ** ค้นด้วยความใกล้เคียงของเวกเตอร์ (เช่น cosine similarity) → จับความหมาย/พ้องความที่ keyword พลาด

**ตัวอย่าง:** ค้น "รถ" แล้วเจอเอกสารที่เขียน "ยานยนต์/automobile" เพราะเวกเตอร์ใกล้กัน

**ใน OKF:** เป็นชั้นเสริม (opt-in) — ถ้าไม่มี embeddings/Ollama จะ fallback เป็น BM25 อัตโนมัติ

## 7. RAG (Retrieval-Augmented Generation)

**คือ** ดึงข้อมูลที่เกี่ยวมาใส่ context ของ LLM ตอนถาม เพื่อ ground คำตอบ (ลด hallucination, อ้างอิงได้)

**ตัวอย่าง** (5 ขั้น):

<pre class="mermaid">
flowchart LR
  D["เอกสาร"] --> C["chunk"] --> E["embed"] --> S["vector store"]
  Q["คำถาม"] --> R["retrieve top-k"]
  S --> R --> G["LLM generate<br/>คำตอบที่อ้างอิงได้"]
</pre>

**ใน OKF:** wiki = Layer 1 (สังเคราะห์ไว้แล้ว ค้นเจอก็จบ); RAG = Layer 2 (ขุดเอกสารดิบเมื่อ wiki ยังไม่ครอบคลุม)

## 8. Hybrid search & RRF

**คือ** รวมผลค้นหลายแบบ (BM25 + semantic) ด้วย **Reciprocal Rank Fusion**: `score(d) = Σ 1/(k + rank)` (k=60)

**ตัวอย่าง:** เอกสารที่ติดอันดับดีทั้งใน BM25 และ semantic จะลอยขึ้นบนสุด โดยไม่มีสัญญาณใดครอบงำ

**ใน OKF:** `okf-search.py` ใช้ RRF รวม BM25 + semantic พอดี

## 9. Knowledge graph (กราฟความรู้)

**คือ** กราฟของ entity (จุด) + ความสัมพันธ์มีชนิด (เส้น) — "things, not strings" ให้ disambiguation และเหตุผลระดับ entity

**ตัวอย่าง:**

<pre class="mermaid">
flowchart LR
  CU["ลูกค้า A"] -->|สั่ง| O["ออเดอร์ 123"]
  O -->|มีสินค้า| P["สินค้า X"]
  CU -->|อยู่กลุ่ม| SEG["ลูกค้าชั้นดี"]
</pre>

**ใน OKF:** bundle ทั้งก้อนเป็น knowledge graph (concept = จุด, ลิงก์ = เส้น) — เปิดดูได้ด้วย `okf-viz.py`

## ตารางสรุป

| แนวคิด | จับอะไร | ตัวอย่างใน OKF |
|--------|---------|----------------|
| Knowledge representation | โครงสร้างความรู้ | concept + frontmatter |
| Ontology | ความสัมพันธ์เชิงความหมาย | ลิงก์ Markdown (untyped) |
| Inverted index / BM25 | จับคำตรงตัว | `okf-index.py` |
| Embeddings / vector search | จับความหมาย | `okf-embed.py` |
| RAG | ground คำตอบ LLM | wiki (L1) + RAG (L2) |
| Hybrid / RRF | รวมหลายสัญญาณ | `okf-search.py` |
| Knowledge graph | entity + ความสัมพันธ์ | bundle + `okf-viz.py` |

ดู[แหล่งข้อมูลอ้างอิงท้ายเล่ม](../appendix/references.md) สำหรับเปเปอร์/มาตรฐานต้นทางของแต่ละแนวคิด

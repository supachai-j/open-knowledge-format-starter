# ประวัติศาสตร์และวิวัฒนาการของ Knowledge Base

OKF ไม่ได้เกิดขึ้นลอย ๆ แต่เป็นปลายทาง (ชั่วคราว) ของเส้นทางกว่า 60 ปี ที่มนุษย์พยายามทำให้
"ความรู้" เก็บ ค้น และให้เครื่องใช้งานได้ บทนี้เล่าเส้นทางนั้นตั้งแต่ยุคแรกถึงปัจจุบันและอนาคต —
เพื่อให้เห็นว่า OKF หยิบบทเรียนจากแต่ละยุคมาประกอบกันอย่างไร

> หมายเลขอ้างอิง `[n]` ในบทนี้ชี้ไปยัง [แหล่งข้อมูลอ้างอิงท้ายเล่ม](../appendix/references.md)

## ไทม์ไลน์ภาพรวม

| ช่วงเวลา | ยุค | ความก้าวหน้าหลัก |
|----------|-----|------------------|
| 1960s–1980s | Expert systems & KR | แยก "ความรู้" ออกจาก "การให้เหตุผล"; กฎ IF-THEN, frames |
| 1990s–2000s | Ontologies & Semantic Web | RDF triples, OWL, linked data — ความหมายที่เครื่องอ่านได้ |
| 1970→2010s | Databases & IR | relational DB, inverted index, TF-IDF, BM25, Lucene/Elasticsearch |
| 1995→2020 | Wiki & PKM | Wikipedia, Zettelkasten, Markdown + `[[wikilinks]]` (Obsidian/Notion/Roam) |
| 2012→2020s | AI era | embeddings, vector DB, RAG, knowledge graph |
| 2026→ | LLM-wiki & OKF | AI สังเคราะห์ความรู้เป็น Markdown ที่ดูแลต่อเนื่อง |

## ยุคที่ 1 — Expert systems & knowledge representation (1960s–1980s)

ยุคนี้ตั้งอยู่บนความเชื่อง่าย ๆ ว่า "พฤติกรรมฉลาดในโดเมนแคบ ๆ จับได้ด้วยการเข้ารหัสความรู้ของ
ผู้เชี่ยวชาญอย่างชัดเจน แล้วให้เครื่องให้เหตุผลบนนั้น" จุดสำคัญคือการ **แยก knowledge base
(สิ่งที่รู้: ข้อเท็จจริง/กฎ) ออกจาก inference engine (วิธีให้เหตุผล)** — สถาปัตยกรรมที่ยังเป็นรากฐานถึงทุกวันนี้

- **DENDRAL** (1965, Feigenbaum/Buchanan/Lederberg, Stanford) — expert system ตัวแรก วิเคราะห์ mass spectrometry [1]
- **MYCIN** (ต้นยุค 1970, Shortliffe, Stanford) — ~600 กฎ IF-THEN วินิจฉัยการติดเชื้อแบคทีเรีย ใช้ "certainty factor" จัดการความไม่แน่นอน [1]
- **Frames** (1974, Minsky, MIT) — โครงสร้าง slot-filler แทนความรู้แบบมีโครงสร้าง [1]
- **Cyc** (1984, Lenat) — ความพยายามเข้ารหัส commonsense ทั้งหมดด้วยมือ → เผยให้เห็น **"knowledge acquisition bottleneck"**: การป้อนความรู้ด้วยมือไม่ scale [1]

ตัวอย่างกฎสไตล์ MYCIN:

```
IF   ชนิดการติดเชื้อ = primary-bacteremia
AND  ตำแหน่งเพาะเชื้อ = blood
AND  ช่องทางเข้า = gastrointestinal-tract
THEN มีหลักฐานพอควร (CF = 0.4) ว่าเชื้อคือ Bacteroides
```

> **บทเรียนสู่ OKF:** การแยก "ความรู้" ออกจาก "เครื่องที่ใช้ความรู้" คือหัวใจ — OKF เก็บความรู้เป็นไฟล์
> (producer) แยกจาก agent ที่บริโภค (consumer) พอดี

## ยุคที่ 2 — Ontologies & the Semantic Web (1990s–2000s)

ปี 2001 Tim Berners-Lee และคณะ เสนอ **Semantic Web** ใน Scientific American [2]: ขยายเว็บจาก
"เอกสารให้คนอ่าน" เป็น "ข้อมูลที่เครื่องเข้าใจความหมาย" รากฐานคือ **RDF** (เก็บความรู้เป็น triple
*subject–predicate–object* = เส้นเชื่อมในกราฟ), **OWL** (ภาษา ontology ที่ reasoner อนุมานข้อเท็จจริงใหม่ได้),
และ **SPARQL** (ภาษา query กราฟ) [2]

**Ontology** = ข้อกำหนดความหมายของแนวคิด/ความสัมพันธ์ในโดเมนแบบที่เครื่องอ่านได้ (ไม่ใช่แค่ taxonomy)

ตัวอย่าง RDF (Turtle):

```turtle
@prefix ex: <http://example.org/> .
@prefix schema: <https://schema.org/> .

ex:TimBernersLee a schema:Person ;
    schema:name "Tim Berners-Lee" ;
    ex:invented ex:WorldWideWeb .
```

แต่ละบรรทัด `subject predicate object` คือหนึ่ง triple — ต่อกันเป็นกราฟความรู้ขนาดยักษ์

การใช้งานเต็มรูปแบบไม่แพร่หลาย (ปี 2013 มีเว็บใช้ markup เชิงความหมาย < 2%) เพราะ formalize ยาก
แต่ทายาทที่ "ใช้ได้จริง" อยู่รอด: **linked data**, **schema.org** (2011), และ **knowledge graph** [2]

> **บทเรียนสู่ OKF:** ความสัมพันธ์ที่เครื่องเดินตามได้มีค่า — OKF ทำให้ง่ายลงด้วย "ลิงก์ Markdown
> ธรรมดา" (untyped) แทน RDF/OWL ที่เข้มงวดจนคนทั่วไปเขียนไม่ไหว

## ยุคที่ 3 — Databases & Information Retrieval (1970→2010s)

เส้นทางจาก "จับคู่ตรงตัว" สู่ "จัดอันดับความเกี่ยวข้อง":

- **Relational model** (1970, Codd, IBM) — เก็บข้อมูลเป็นตาราง query ด้วย SQL แต่ match field แบบตรงตัว [3]
- **TF-IDF** — Luhn (1957) ชี้ว่าความถี่คำสัมพันธ์กับความเกี่ยวข้อง; Spärck Jones (1972) เพิ่ม **IDF**: คำที่พบในเอกสารน้อยชิ้น = สัญญาณเด่นกว่า [3]
- **BM25** (~1994, Robertson & Spärck Jones, ระบบ Okapi) — เพิ่ม length normalization + saturation ยังเป็น baseline ของ lexical search ถึงวันนี้ [3]
- **Lucene** (1999, Doug Cutting) และ **Elasticsearch** (2010) — ทำ full-text search ระดับอุตสาหกรรมให้ใคร ๆ ก็ใช้ได้ [3]

ตัวอย่าง inverted index ของ 3 เอกสารจิ๋ว:

| คำ | posting list |
|----|--------------|
| cat | D1, D2 |
| sat | D1, D3 |
| dog | D3 |

**ข้อจำกัดหลัก:** เป็น *lexical* — จับคำตรงตัว ค้น "car" จะพลาดเอกสารที่เขียน "automobile" (ไม่เข้าใจความหมาย/พ้องความ)

> **บทเรียนสู่ OKF:** BM25 ยังทรงพลังและเบา — `tools/okf-index.py` ใช้ BM25 เป็น search หลัก

## ยุคที่ 4 — Wiki & Personal Knowledge Management (1995→2020)

- **WikiWikiWeb** (25 มี.ค. 1995, Ward Cunningham) — เว็บแก้ไขได้ตัวแรก ลิงก์อัตโนมัติจาก CamelCase [4]
- **Wikipedia** (15 ม.ค. 2001, Wales & Sanger) — สารานุกรมเปิดให้ชุมชนแก้ ใหญ่ที่สุดในประวัติศาสตร์ [4]
- **Zettelkasten** (Niklas Luhmann, 1950s–1998) — กล่องบัตร ~90,000 ใบ เชื่อมโยงกัน ผลิตหนังสือ 50+ เล่ม; **คุณค่าอยู่ที่ "ลิงก์ระหว่างโน้ต" ไม่ใช่ตัวโน้ต** [4]
- **Notion** (2016), **Roam** (2019, bidirectional links), **Obsidian** (2020, local-first Markdown + graph view) [4]

Markdown ชนะสงครามฟอร์แมตเพราะ **คนอ่านออกโดยไม่ต้อง render และเครื่องอ่านออกโดยไม่ต้อง parser พิเศษ**

ตัวอย่างโน้ต Markdown แบบ PKM:

```markdown
---
title: "Zettelkasten Principle"
tags: [pkm, luhmann]
---
คุณค่าของกล่องบัตรอยู่ที่ **ลิงก์ระหว่างโน้ต** ไม่ใช่ตัวโน้ตเดี่ยว ๆ
ดูเพิ่ม: [[Bidirectional Links]], [[Obsidian]]
```

> **บทเรียนสู่ OKF:** นี่คือ DNA ตรงของ OKF — Markdown + YAML frontmatter + ลิงก์ระหว่าง concept

## ยุคที่ 5 — AI era: embeddings, vector search, RAG (2012→2020s)

แนวคิดแกน: **"ความหมาย = เรขาคณิต"**

- **Google Knowledge Graph** (2012, Singhal) — "things, not strings" 500M entity, 3.5B ความสัมพันธ์ [5]
- **word2vec** (2013, Mikolov, Google) — ฝังคำเป็นเวกเตอร์ จับ analogy เช่น `king − man + woman ≈ queen` [5]
- **FAISS** (2017, Facebook AI) — ค้นเวกเตอร์ใกล้เคียง (ANN) ระดับพันล้านเวกเตอร์ [5]
- **BERT** (2018, Devlin, Google) — contextual embedding (คำเดียวกันได้เวกเตอร์ต่างกันตามบริบท) [5]
- **RAG** (2020, Lewis et al., Facebook AI) — ดึง passage ที่เกี่ยวมา ground คำตอบ LLM ลดการแต่งเรื่อง [5]
- **Hybrid search + RRF** (RRF: Cormack et al., 2009) — รวม BM25 + semantic ด้วย `Σ 1/(k+rank)` [5]

ตัวอย่างขั้นตอน RAG: chunk → embed → store → retrieve top-k → generate

> **บทเรียนสู่ OKF:** OKF เป็น Layer 1 (ความรู้สังเคราะห์แล้ว) ส่วน RAG/vector เป็น Layer 2 (ขุดของดิบ);
> `okf-search.py` รวม BM25 + semantic ด้วย RRF ตามยุคนี้

## ยุคที่ 6 — ปัจจุบัน: LLM-wiki & Open Knowledge Format (2026)

เมษายน 2026 **Andrej Karpathy** เสนอแนวคิด **"LLM wiki"** [6]: แทนที่จะดึง chunk ดิบทุกครั้งที่ถาม
ให้ agent **คอมไพล์แหล่งดิบเป็น Markdown ที่จัดระเบียบ เชื่อมโยง และดูแลต่อเนื่อง** — สังเคราะห์ครั้งเดียว
ตอน ingest ไม่ใช่ทุก query; ความรู้ **ทบต้น**

12 มิถุนายน 2026 **Google Cloud** (Sam McVeety, Amir Hormati) เผยแพร่ **Open Knowledge Format (OKF)
v0.1** [6] — สเปกเปิดที่ทำให้ LLM-wiki pattern เป็นมาตรฐาน: ไดเรกทอรีของ Markdown + YAML frontmatter
บังคับแค่ฟิลด์ `type`, แยก producer/consumer, พกพาข้ามคลาวด์/เฟรมเวิร์ก

ก่อนหน้านั้น **MemGPT/Letta** (2023, Packer et al., UC Berkeley) [6] แสดงให้เห็น "LLM as OS" — จัดการ
หน่วยความจำแบบ tiered (in-context = RAM, external = disk) ปูทางสู่ agent ที่มีความจำถาวร

## อนาคต — self-maintaining & agentic knowledge

ทิศทางคือ **knowledge base ที่ดูแลตัวเอง**: agent ไม่ใช่แค่ "ถาม" ความรู้ แต่ **คอยดูแล** — ตรวจว่าข้อมูล
เก่าไหม (ผ่าน `timestamp`/`log.md`), ปรับข้อขัดแย้งข้าม concept, เสนอการอัปเดตให้คนอนุมัติก่อน commit [6]

ชั้นถัดไปน่าจะเป็น **hybrid wiki + RAG**: wiki ที่สังเคราะห์ไว้เป็น index เร็ว ส่วน RAG เติมช่องว่างของข้อมูล
ที่เปลี่ยนบ่อย/เยอะเกินจะ precompile — โดยมี agent memory (เช่น Letta) เป็น runtime; และ multi-agent ที่
แบ่งหน้าที่ (agent หนึ่งดูแลความรู้ อีกกลุ่มบริโภค) มุ่งสู่สิ่งที่เริ่มเรียกกันว่า **"compiled-knowledge generation"**

## สรุป: ประวัติศาสตร์หล่อหลอม OKF อย่างไร

OKF ไม่ได้คิดใหม่ทั้งหมด แต่ **ประกอบชิ้นส่วนที่ดีที่สุดของแต่ละยุค**:

| จากยุค | OKF หยิบอะไรมา |
|--------|----------------|
| Expert systems | แยกความรู้ (ไฟล์) ออกจากเครื่องที่ใช้ (agent) |
| Semantic Web | ความรู้เป็นกราฟที่เชื่อมโยง (แต่ใช้ลิงก์ Markdown ง่าย ๆ) |
| IR / BM25 | search ที่เบาและทรงพลัง |
| Wiki / PKM | Markdown + frontmatter + `[[links]]` คนอ่านออก version control ได้ |
| AI era | embeddings/RAG เป็นชั้นเสริม + AI สังเคราะห์ความรู้ |

ต่อไปดู [แนวคิดพื้นฐานที่ต้องรู้ (พร้อมตัวอย่าง)](./foundations.md)

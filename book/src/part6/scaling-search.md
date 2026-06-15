# Search ระดับ scale และ semantic

เมื่อ wiki โตขึ้น การสแกน `index.md` แบน ๆ จะช้า บทนี้ว่าด้วยการค้นที่ scale ได้ บน on-prem ล้วน

## ตามขนาด wiki

| ขนาด | ใช้อะไร |
|------|---------|
| < ~150 concept | `index.md` progressive disclosure ก็พอ |
| > ~150 | สร้าง BM25 index (`okf-index.py build`) — `okf_search` ใช้อัตโนมัติ |
| recall ไม่พอ | เพิ่มชั้น semantic + RRF (ด้านล่าง) |
| ใหญ่มาก/หลายทีม | federate bundles, MCP ต่อโดเมน, cache index ใน memory rebuild ตาม webhook |

## ชั้น semantic (on-prem)

ฝัง concept ด้วยโมเดล embedding ที่ self-host (ผ่าน Ollama) — ไม่มีอะไรออกนอกเครือข่าย:

```bash
ollama pull nomic-embed-text          # ครั้งเดียว
python3 tools/okf-embed.py build ./wiki   # → wiki/.okf-embed.json
python3 tools/okf-search.py "ลูกค้าที่ active" --bundle ./wiki
# → mode: hybrid (bm25+semantic, RRF)
```

## Reciprocal Rank Fusion (RRF)

`okf-search.py` รวมผล **BM25 (lexical)** กับ **semantic (vector)** ด้วย RRF:

```
fused(doc) = Σ_signals  1 / (RRF_K + rank)      (RRF_K = 60)
```

แต่ละสัญญาณจัดอันดับ doc ของตัวเอง แล้วเอาคะแนนผกผันของอันดับมาบวกกัน — doc ที่ติดอันดับดี
ในหลายสัญญาณจะลอยขึ้นบน โดยไม่มีสัญญาณใดครอบงำ

ทำไมต้องสองสัญญาณ:

- **BM25** เก่งเรื่องจับคำ/รหัสตรงตัว (policy code, ชื่อคอลัมน์)
- **semantic** เก่งเรื่องจับความหมาย/พ้องความ ("ลูกค้าที่ active" ↔ "weekly active users")

## fallback อัตโนมัติ (สำคัญ)

> ถ้ายังไม่ได้สร้าง embeddings **หรือ** Ollama ไม่ทำงาน → search **fallback เป็น BM25 อัตโนมัติ**
> และรายงาน mode ให้รู้ semantic จึงเป็น **upgrade แบบ opt-in ล้วน ๆ ไม่มี hard dependency**

ทำให้ระบบทนทาน: เครื่องไหนไม่มี Ollama ก็ยังค้นได้ด้วย BM25

## ทำให้ scale ขึ้นอีก

- **federate bundles** — แยก repo ต่อโดเมน/ทีม
- **MCP server ต่อโดเมน** หลังหนึ่ง gateway
- **cache index ใน memory** และ rebuild แบบ incremental เมื่อ webhook แจ้งว่ามีการ merge
- index/embeddings เป็น **artifact ที่ gen ได้** (CI / MCP server สร้างเมื่อต้องการ) — ไม่ต้อง commit
  (`.okf-index.json`, `.okf-embed.json` อยู่ใน `.gitignore`)

ต่อไป: ความปลอดภัยและการกำกับดูแล → [ความปลอดภัยและ governance](./security.md)

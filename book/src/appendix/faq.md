# คำถามที่พบบ่อย (FAQ)

### OKF ต่างจาก Obsidian / Notion ยังไง?
ใกล้เคียงกันมาก (Markdown + frontmatter + ลิงก์) แต่ OKF **ถูก specify** — กำหนดกฎเล็ก ๆ ที่จำเป็น
ต่อการ interoperate (เช่น `type` บังคับ, ไฟล์สงวน, กฎ conformance) โดยไม่บังคับเครื่องมือ คุณเปิด OKF
bundle ใน Obsidian/MkDocs/Hugo ได้เลยเพราะมันคือ Markdown

### ต้องใช้ Google Cloud / BigQuery ไหม?
ไม่ OKF เป็น vendor-neutral ตัวอย่างใน reference ของ Google ใช้ BigQuery แต่ `type` เป็นอะไรก็ได้
starter นี้ไม่ผูกกับ cloud ใด

### จำเป็นต้องมี AI agent ไหม?
ไม่จำเป็น เขียน concept เองด้วยมือได้ (มันคือ Markdown) AI agent แค่ช่วยงานหนัก — สรุป, cross-reference,
filing, bookkeeping

### ลิงก์ควรเป็น relative หรือ absolute?
**relative เท่านั้น** อย่าขึ้นต้นด้วย `/` เพราะพัง GitHub rendering (ดู [การลิงก์](../part3/linking.md))
แม้สเปกจะแนะนำ absolute แต่ implementation จริงของ Google ใช้ relative

### broken link ผิดไหม?
ไม่ผิด — แทน "ความรู้ที่ยังไม่ได้เขียน" `okf-validate.py` รายงานเป็น info ไม่ใช่ error

### ทำ ingest อัตโนมัติเลยได้ไหม?
**ไม่แนะนำอย่างยิ่ง** — daemon เบื้องหลังจะสะสม noise จน wiki เน่า ให้ ingest เป็นคำสั่งที่คนสั่ง + รีวิว

### wiki ใหญ่แค่ไหนถึงต้องใช้ search?
ประมาณ **~150 หน้า** ก่อนหน้านั้น `index.md` ก็พอ เกินกว่านั้นใช้ `okf-search.py` (BM25) และเพิ่ม semantic เมื่อ recall ไม่พอ

### ต้องมี Ollama ไหมถึงจะค้นได้?
ไม่ BM25 ทำงานโดยไม่ต้องมี Ollama · semantic เป็น upgrade เสริม ถ้า Ollama ไม่ทำงาน search จะ fallback เป็น BM25 เอง

### หลาย agent เขียนชนกันทำยังไง?
เลือกโมเดลการเขียน: **PR-gated** (ปลอดภัย มี review) หรือ **lease/lock** (เร็ว สำหรับทีมเขียนหนัก)
ดู [โมเดลการเขียน](../part6/write-models.md)

### air-gap (เครือข่ายปิด) ใช้ได้ไหม?
ได้ — `viz.html` ฝังไลบรารีในตัว, เครื่องมือเป็น stdlib, semantic ใช้ Ollama ในองค์กร, git/MCP อยู่ภายใน

### `.okf-index.json` / `.okf-embed.json` ต้อง commit ไหม?
ไม่ — เป็น artifact ที่ gen ได้ อยู่ใน `.gitignore` แล้ว CI/MCP server สร้างใหม่เมื่อต้องการ

### validate ขึ้น error "missing type" แก้ยังไง?
ทุก concept ต้องมี `type` ที่ไม่ว่างใน frontmatter เพิ่ม `type: ...` (เลือกจาก controlled vocabulary)

### จะ migrate wiki เดิม (Obsidian ฯลฯ) เข้า OKF ยังไง?
ส่วนใหญ่แค่เพิ่มฟิลด์ `type` ใน frontmatter + เพิ่ม `index.md`/`log.md` + ปรับลิงก์ให้ relative แล้วรัน validate

### จะตรวจว่า toolchain ใช้ได้จริงทั้งชุดยังไง?
รัน `bash tools/okf-selftest.sh` — เทสต์ end-to-end 10 ข้อ (init/validate/index/search/viz/lease + embed/hybrid ถ้ามี Ollama) exit ≠ 0 ถ้ามีข้อพลาด · ดู[ตัวอย่างใช้งานจริง](../part4/worked-example.md) สำหรับการเดินครบลูปด้วยมือ

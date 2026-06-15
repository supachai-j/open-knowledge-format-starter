# อภิธานศัพท์

| คำ | ความหมาย |
|----|----------|
| **OKF** (Open Knowledge Format) | สเปกเปิดสำหรับเก็บความรู้เป็นไดเรกทอรีของ Markdown + YAML frontmatter (v0.1, Google Cloud, 2026) |
| **Bundle** | ไดเรกทอรีของไฟล์ความรู้ทั้งหมด — หน่วยที่ใช้แจกจ่าย (ในโปรเจกต์นี้คือ `wiki/`) |
| **Concept** | ความรู้หนึ่งหน่วย = ไฟล์ `.md` หนึ่งไฟล์ |
| **Concept ID** | path ของไฟล์ใน bundle ตัด `.md` ออก เช่น `tables/orders.md` → `tables/orders` |
| **Frontmatter** | บล็อก YAML บนหัวไฟล์ คั่นด้วย `---` เก็บ metadata |
| **Body** | เนื้อหา Markdown ใต้ frontmatter |
| **Link** | ลิงก์ Markdown ระหว่าง concept = ความสัมพันธ์ (untyped) |
| **Citation** | ลิงก์จาก concept ไปแหล่งภายนอกที่สนับสนุน claim ในเนื้อหา |
| **Reserved file** | ไฟล์สงวน: `index.md` (สารบัญ), `log.md` (บันทึกการเปลี่ยนแปลง) |
| **Progressive disclosure** | การให้เห็นสารบัญก่อนเปิดไฟล์จริง — ลดการล้น context window |
| **Conformance** | การที่ bundle ทำตามกฎ v0.1 (frontmatter parse ได้ + มี `type` + ไฟล์สงวนถูกโครงสร้าง) |
| **type** | ฟิลด์ frontmatter เดียวที่บังคับ — ระบุชนิดของ concept |
| **Reference** | `type` ที่ใช้กับความรู้สังเคราะห์ (join, นิยาม metric) มักอยู่ใต้ `references/` |
| **RAG** | Retrieval-Augmented Generation — ดึง chunk เอกสารดิบตอนถามมายัด context |
| **LLM-wiki pattern** | แนวคิด (Karpathy) ที่ให้ AI สังเคราะห์ความรู้ลง Markdown wiki ที่ดูแลต่อเนื่อง แทนการดึงดิบทุกครั้ง |
| **Ingest** | การนำแหล่งดิบมาสังเคราะห์เป็น concept ใน wiki (ควรมีคนกำกับ) |
| **Contradiction flag** | ธง `> **CONTRADICTION FLAG**: ...` ที่เติมเมื่อข้อมูลใหม่ขัดของเก่า |
| **BM25** | อัลกอริทึมค้นแบบ keyword ให้คะแนนความเกี่ยวข้อง |
| **Embedding** | เวกเตอร์แทนความหมายของข้อความ (สร้างด้วยโมเดล เช่นผ่าน Ollama) |
| **Semantic search** | ค้นด้วยความใกล้เคียงเชิงความหมาย (cosine ของ embedding) |
| **Hybrid search** | รวม BM25 + semantic |
| **RRF** (Reciprocal Rank Fusion) | วิธีรวมผลจัดอันดับหลายสัญญาณ: `Σ 1/(k + rank)` |
| **MCP** (Model Context Protocol) | มาตรฐานเปิดให้ AI agent ต่อกับเครื่องมือ/ข้อมูลภายนอก |
| **MCP server** | service ที่เปิด tool (search/get/propose) ครอบ bundle ให้ agent ต่อ |
| **PR-gated** | โมเดลเขียนผ่าน branch + Pull Request + CI + review |
| **Lease/lock** | โมเดลเขียนที่จองสิทธิ์ต่อ concept แบบมี TTL กันเขียนชนกัน |
| **Lease** | สิทธิ์จองแบบมี TTL หมดอายุเอง ตรวจด้วย token |
| **Curator** | (โมเดลที่ 3) agent ตัวเดียวที่รวบ proposal แล้ว merge เข้า wiki |
| **CODEOWNERS** | ไฟล์กำหนดเจ้าของต่อ subtree (ใช้แบ่งความรับผิดชอบข้ามทีมใน monorepo) |
| **Federated bundles** | หลาย repo/bundle ต่อโดเมน MCP server mount หลายตัว namespace ด้วยชื่อ bundle |
| **air-gap** | สภาพแวดล้อมที่ไม่ต่ออินเทอร์เน็ต (เครือข่ายปิด) |
| **Gitea / GitLab CE** | git server ที่ self-host ได้ ใช้เป็นต้นทางความจริง |
| **AGENTS.md** | ไฟล์ schema ที่บอก agent ถึงโครงสร้าง/กฎ/workflow (อาจชื่อ `CLAUDE.md`/`GEMINI.md`) |

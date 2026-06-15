# ติดตั้ง

OKF starter เป็นเครื่องมือ **Python ล้วน (ไม่มี dependency บังคับ)** ใช้ได้แบบ offline/air-gap
สิ่งที่ต้องมี:

- **Python 3.13+** (เครื่องมือทุกตัวเป็น stdlib ล้วน)
- **Git** (สำหรับ version control ของ bundle)
- *(ไม่บังคับ)* **Ollama** ถ้าจะใช้ semantic search ในเครื่อง
- *(ไม่บังคับ)* **Docker** ถ้าจะ deploy แบบ self-host (ภาคที่ 6)

## ทางเลือกที่ 1 — ติดตั้งเป็น Claude Code skill (แนะนำ)

วิธีนี้ทำให้ทุกโปรเจกต์/ทุก session สร้างและดูแล OKF bundle ได้ โดยไม่ต้องอยู่ใน repo ต้นทาง

```bash
git clone https://github.com/supachai-j/open-knowledge-format-starter.git
cd open-knowledge-format-starter

./install.sh                 # ติดตั้ง global → ~/.claude/skills/okf  (ทุกโปรเจกต์ใช้ได้)
./install.sh --project       # ติดตั้งเฉพาะโปรเจกต์ → ./.claude/skills/okf
./install.sh --dir <path>    # ติดตั้งที่อื่น
./install.sh --uninstall     # ถอนออก
```

`install.sh` จะประกอบ skill (ไฟล์ `SKILL.md` + เครื่องมือ Python ทั้งหมด + ไลบรารี viewer ที่ฝังในตัว)
ไปไว้ในโฟลเดอร์ skill ที่ self-contained จากนั้นเปิด Claude Code แล้วพิมพ์ `/okf` หรือพูดว่า
*"init an OKF knowledge base here"* ได้เลย

> **skill ทำงานยังไง:** เมื่อเรียกใช้ Claude Code จะรู้ตำแหน่งของ skill และรันสคริปต์ใน `scripts/`
> ของ skill นั้น — ไม่ว่าจะติดตั้ง global หรือ project ก็ทำงานได้

## ทางเลือกที่ 2 — ใช้จาก repo ตรง ๆ

ถ้าอยากทำงานในตัว repo เอง (หรือยังไม่อยากติดตั้ง skill) เครื่องมือทั้งหมดอยู่ใน `tools/`:

```bash
git clone https://github.com/supachai-j/open-knowledge-format-starter.git
cd open-knowledge-format-starter
python3 tools/okf-validate.py ./wiki        # → ✓ CONFORMANT with OKF v0.1
python3 tools/okf-viz.py ./wiki             # → wiki/viz.html (เปิดในเบราว์เซอร์)
```

## ทางเลือกที่ 3 — ใช้เป็น GitHub template

repo ต้นทางตั้งเป็น **template repository** — กดปุ่ม **"Use this template"** บน GitHub
เพื่อสร้าง repo ใหม่ของคุณเองพร้อมโครงสร้างครบ

## ตรวจว่าติดตั้งสำเร็จ

```bash
python3 --version                  # ควรเป็น 3.13 ขึ้นไป
python3 tools/okf-validate.py --help 2>/dev/null || python3 tools/okf-validate.py ./wiki
```

ถ้าเห็น `✓ CONFORMANT with OKF v0.1` แปลว่าพร้อมแล้ว ไปสร้าง knowledge base แรกกัน →
[สร้าง knowledge base แรก](./first-kb.md)

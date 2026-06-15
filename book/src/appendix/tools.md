# อ้างอิงเครื่องมือ (CLI)

เครื่องมือทั้งหมดเป็น Python stdlib ล้วน อยู่ใน `tools/` (หรือ `scripts/` ถ้าติดตั้งเป็น skill)

## okf-init.py — สร้าง bundle ใหม่
```bash
python3 tools/okf-init.py [target_dir] [--force] [--date YYYY-MM-DD]
```
สร้าง `AGENTS.md` + `wiki/{index.md, log.md, getting-started.md}` + `raw/` · ไม่เขียนทับ `wiki/` ที่ไม่ว่าง เว้นแต่ `--force`

## okf-validate.py — ตรวจ conformance
```bash
python3 tools/okf-validate.py [wiki_dir]
```
ออก 0 ถ้า conformant, 1 ถ้าไม่ · error = ไม่มี frontmatter/`type`, index.md ผิดกฎ · warn = ลิงก์ `/`, log ไม่ใช่ ISO · info = broken link

## okf-viz.py — สร้าง graph viewer
```bash
python3 tools/okf-viz.py [bundle] [-o out.html] [--name "ชื่อ"] [--cdn]
```
สร้าง `viz.html` ไฟล์เดียว self-contained (ฝัง Cytoscape + marked) · `--cdn` = โหลดไลบรารีจาก CDN แทนการฝัง

## okf-index.py — BM25 search index
```bash
python3 tools/okf-index.py build [bundle] [-o index.json]
python3 tools/okf-index.py query "คำถาม" [-k 8] [--type Metric]
```

## okf-embed.py — embeddings (Ollama)
```bash
python3 tools/okf-embed.py build [bundle]
python3 tools/okf-embed.py query "คำถาม" [-k 8]
```
env: `OKF_OLLAMA_URL` (default `http://localhost:11434`), `OKF_EMBED_MODEL` (default `nomic-embed-text`)

## okf-search.py — hybrid search (BM25 + semantic, RRF)
```bash
python3 tools/okf-search.py "คำถาม" [--bundle ./wiki] [-k 8] [--type ...] [--bm25-only]
```
fallback เป็น BM25 อัตโนมัติถ้าไม่มี embeddings / Ollama ไม่ทำงาน

## okf-lease.py — lease/lock concurrency
```bash
python3 tools/okf-lease.py acquire <concept> --owner <id> [--ttl 300]
python3 tools/okf-lease.py renew   <concept> --owner <id> --token <tok> [--ttl 300]
python3 tools/okf-lease.py release <concept> --owner <id> --token <tok>
python3 tools/okf-lease.py list
python3 tools/okf-lease.py break   <concept>      # admin บังคับปลด
```
env: `OKF_LEASE_DIR` (ที่เก็บ lease), `OKF_LEASE_TTL` (default 300)

## install.sh — ติดตั้ง skill
```bash
./install.sh                 # global  → ~/.claude/skills/okf
./install.sh --project       # project → ./.claude/skills/okf
./install.sh --dir <path>    # custom
./install.sh --uninstall
```

## server/okf_mcp_server.py — MCP access layer
```bash
python3 server/okf_mcp_server.py            # stdio
OKF_MCP_TRANSPORT=streamable-http OKF_MCP_PORT=8765 python3 server/okf_mcp_server.py
```
env หลัก: `OKF_REPO_DIR`, `OKF_BUNDLE`, `OKF_BASE_BRANCH`, `OKF_WRITE_MODE` (`pr`|`lease`),
`OKF_READONLY`, `OKF_GITEA_API/TOKEN/OWNER/REPO`, `OKF_AGENT_ID`

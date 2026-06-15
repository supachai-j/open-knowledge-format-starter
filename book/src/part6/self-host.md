# ติดตั้งแบบ self-host

`deploy/docker-compose.yml` ยกสแต็กภายในขึ้นมาทั้งชุดบน VM เดียว — ไม่เปิดสู่ภายนอก ใช้ได้แม้ air-gap

## สแต็กที่ได้

```
gitea   →  ต้นทางความจริง (git server)
okf-mcp →  access layer ที่ agent ต่อ (build จาก deploy/Dockerfile)
proxy   →  Caddy: TLS + auth (token/OIDC/mTLS) หน้า MCP
```

## ขั้นตอน

```bash
cd deploy
cp .env.example .env        # ตั้งค่า OKF_GIT_REMOTE, token, ฯลฯ
docker compose up -d
```

ค่าใน `.env` ที่ต้องตั้ง:

```bash
OKF_GIT_REMOTE=http://gitea:3000/okf/knowledge.git   # repo ที่ MCP จะ clone/pull
OKF_GITEA_API=http://gitea:3000/api/v1               # เปิด PR อัตโนมัติจาก propose_change
OKF_GITEA_TOKEN=<token>
OKF_GITEA_OWNER=okf
OKF_GITEA_REPO=knowledge
OKF_TOKEN=<long-random>                              # token ที่ agent ต้องส่งให้ proxy
OKF_READONLY=0                                       # 1 = replica อ่านอย่างเดียว
```

## ต่อ agent เข้า MCP endpoint

ใน Claude Code (หรือ MCP client ใด ๆ) ชี้ไป URL ภายใน:

```jsonc
{ "mcpServers": { "okf": {
    "transport": "http",
    "url": "https://okf.internal.example/mcp",
    "headers": { "Authorization": "Bearer ${OKF_TOKEN}" }
} } }
```

## โหมด local / dev (ไม่ต้องมีเน็ต)

ทดสอบ server โดยไม่ต้องยกทั้งสแต็ก:

```bash
python3 server/okf_mcp_server.py                       # stdio transport
# หรือ HTTP:
OKF_MCP_TRANSPORT=streamable-http OKF_MCP_PORT=8765 \
  python3 server/okf_mcp_server.py
```

## เครื่องมือ (tools) ที่ server เปิดให้ agent

| Tool | ทำอะไร |
|------|--------|
| `okf_search(query, k, type)` | ค้นแบบ hybrid (BM25 + semantic ถ้ามี) |
| `okf_get_concept(id)` | คืน frontmatter + body ของ concept |
| `okf_list_concepts(prefix)` | ลิสต์ id/type/description |
| `okf_read_index(path)` | อ่าน `index.md` (progressive disclosure) |
| `okf_propose_change(...)` | เขียนผ่าน branch + PR (โหมด PR) |
| `okf_acquire_lease / renew / release / list_leases` | จองสิทธิ์เขียน (โหมด lease) |
| `okf_commit_concept(..., token)` | เขียนตรงโดยถือ lease (โหมด lease เท่านั้น) |

## CI conformance gate

ตั้ง branch protection บน `main` ให้ต้องผ่าน check นี้ — bundle ที่ไม่ conformant จะ merge ไม่ได้

- **Gitea Actions:** `.gitea/workflows/conformance.yml`
- **GitLab CI:** `ci/.gitlab-ci.yml`

ทั้งคู่รัน `okf-validate.py` (บล็อกถ้าไม่ผ่าน) + rebuild index + regenerate `viz.html`

## ความปลอดภัยเบื้องต้น

- หน้า MCP มี reverse proxy ทำ TLS + auth (รายละเอียดในบท [ความปลอดภัยและ governance](./security.md))
- `raw/` ไม่อยู่ใน bundle (มี `.gitignore` กันเผลอ commit ข้อมูลส่วนตัว)
- air-gap: `viz.html` ฝังไลบรารีในตัว, semantic ใช้ Ollama ในองค์กร — ไม่มีอะไรออกนอกเครือข่าย

ต่อไป: เลือกโมเดลการเขียน → [โมเดลการเขียน: PR-gated และ Lease](./write-models.md)

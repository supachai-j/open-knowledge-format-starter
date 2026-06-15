# ความปลอดภัยและ governance

ระบบ self-host ภายในต้องคุมว่าใครอ่าน/เขียนอะไรได้ และตรวจสอบย้อนหลังได้ OKF ได้ governance
หลายอย่างมาฟรีจาก git อยู่แล้ว

## คุมการเข้าถึง 2 ชั้น

### ชั้น git
- สมาชิก org/team บน Gitea/GitLab
- **branch protection** บน `main` — บังคับให้ผ่าน CI + review ก่อน merge

### ชั้น MCP
วาง HTTP transport ไว้หลัง reverse proxy พร้อม:

- **mTLS** (service-to-service) **หรือ** **OIDC/SSO** (สำหรับคน) + bearer token ต่อ agent identity
- map identity → role:

| role | ทำได้ |
|------|-------|
| `reader` | search / get / list เท่านั้น |
| `proposer` | + `okf_propose_change` (branch/PR เท่านั้น ไม่แตะ `main`) |
| `curator` | merge ได้ (ผ่าน git server ไม่ใช่ผ่าน MCP) |

ตั้ง `OKF_READONLY=1` เพื่อรัน MCP replica แบบอ่านอย่างเดียว

## ตัวอย่าง Caddy (proxy) — bearer token

```
okf.internal.example {
    # internal CA / self-signed สำหรับ air-gap:
    #   tls /etc/caddy/okf.crt /etc/caddy/okf.key
    # หรือ mTLS:
    #   tls { client_auth { mode require_and_verify trusted_ca_cert_file /etc/caddy/internal-ca.crt } }

    @noauth not header Authorization "Bearer {$OKF_TOKEN}"
    respond @noauth "Unauthorized" 401
    reverse_proxy okf-mcp:8765
}
```

สำหรับ SSO ให้แทน bearer ด้วย `forward_auth` ไปยัง OIDC proxy (เช่น oauth2-proxy) แล้ว map identity → role

## ความลับและ PII

- **`raw/` ไม่อยู่ใน bundle** และอยู่ใน `.gitignore` แล้ว — กันเผลอ push ข้อมูลส่วนตัว/ใหญ่
- **อย่าใส่ credential ใน concept** — concept คือความรู้ ไม่ใช่ที่เก็บความลับ
- รีวิว PR ช่วยจับข้อมูลอ่อนไหวก่อนเข้า `main` (อีกเหตุผลที่ PR-gated ดีในองค์กร)

## air-gap (เครือข่ายปิด)

- `viz.html` ฝังไลบรารี (Cytoscape + marked) ในตัว — ไม่ดึง CDN ตอนเปิด
- semantic search ใช้โมเดล embedding ที่ self-host (Ollama) — ไม่มีอะไรออกนอกเครือข่าย
- เครื่องมือทั้งหมดเป็น Python stdlib (ยกเว้น MCP server ที่ใช้แพ็กเกจ `mcp` — ติดตั้งจาก mirror ภายในได้)

## audit & rollback (มาจาก git)

| งาน | คำสั่ง |
|-----|--------|
| ใครแก้ WAU บ้าง | `git log --follow wiki/metrics/weekly-active-users.md` |
| ย้อนความรู้ที่ผิด | `git revert <sha>` → PR → merge |
| ไทม์ไลน์การเปลี่ยนแปลง | อ่าน `wiki/log.md` หรือ `git log` |

## governance ที่ได้มาฟรี

เพราะ wiki เป็นไฟล์ใน git ทุกการเปลี่ยนแปลงจึงมี **diff, blame, review, history, rollback**
เหมือนการพัฒนาซอฟต์แวร์ปกติ — การดูแลความรู้กลายเป็น workflow วิศวกรรมที่ทีมคุ้นเคยอยู่แล้ว

จบภาคองค์กร ดูภาคผนวกสำหรับอ้างอิง → [อ้างอิงเครื่องมือ (CLI)](../appendix/tools.md)

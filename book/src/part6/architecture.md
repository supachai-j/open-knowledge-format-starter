# ภาพรวมสถาปัตยกรรม (Enterprise)

เมื่อต้องใช้ knowledge base ร่วมกัน **ข้าม session และข้ามทีม ระดับองค์กร** บน on-prem
(เชื่อมต่อภายใน ใช้ได้แม้ air-gap) แนวคิดหลักมีประโยคเดียว:

> **Git คือต้นทางความจริง · MCP server ภายในคือ access layer กลาง**
>
> ทุก session และทุก agent — ไม่ว่า framework หรือ model ไหน — ต่อ **MCP endpoint ภายในตัวเดียวกัน**
> ประวัติ git *คือ* "ความจำข้าม session" โดยธรรมชาติ · อ่านเร็วทันที · เขียนผ่าน gate (PR หรือ lease)

## แผนภาพ

```
                ┌─────────────── เครือข่ายภายใน ────────────────┐
  ทีม A ─┐      │   ┌──────────┐   pull / webhook                │
 (agent) │ MCP  │   │ Git server│◄──────────────┐                │
  ทีม B ─┼─────►│   │ (Gitea/   │   ┌────────────┴──────────┐    │
 (agent) │(HTTP/│   │  GitLab)  │   │   OKF MCP server      │    │
 CI/cron─┘ SSE +│   │ = OKF repo│   │  search · get ·       │    │
           token│   └─────┬─────┘   │  propose / commit     │    │
           /mTLS)│        │ PR/MR    │  (FastMCP)            │    │
                 │        ▼          └──────────┬────────────┘    │
                 │   ┌──────────┐    builds     │ search index    │
                 │   │ CI runner │              ▼ (BM25 +/- embed) │
                 │   │ validate  │                                 │
                 │   └──────────┘                                 │
                 └────────────────────────────────────────────────┘
```

## องค์ประกอบ

| # | ส่วน | ตัวเลือก self-host | บทบาท |
|---|------|---------------------|-------|
| 1 | **Git server** | Gitea / GitLab CE | ต้นทางความจริง versioned (repo ต่อทีม หรือ monorepo + CODEOWNERS) |
| 2 | **OKF MCP server** | `server/okf_mcp_server.py` | access layer ที่ทุก agent ต่อ — read/search/propose; stdio + HTTP/SSE |
| 3 | **Search index** | `tools/okf-index.py` (+ embed) | ค้นเร็วเมื่อ wiki โตเกิน ~150 หน้า |
| 4 | **CI gate** | Gitea Actions / GitLab CI | บล็อก merge ที่ไม่ conformant + regen viz |
| 5 | **Reverse proxy** | Caddy / Traefik / nginx | TLS + auth (token / OIDC / mTLS) หน้า MCP |

## Read path (กรณีปกติ — เร็ว ไม่มี lock)

1. agent เรียก `okf_search("WAU นิยามยังไง")` → ได้ Concept ID จัดอันดับ
2. `okf_get_concept("metrics/weekly-active-users")` → frontmatter + body โหลดเข้า context
3. `okf_read_index()` เมื่อต้องการสำรวจแบบ progressive disclosure

อ่านพร้อมกันได้ไม่จำกัด ไม่มี contention

## Write path

มี 2 โมเดลให้เลือก (บทถัดไป):

- **PR-gated (ค่าเริ่มต้น):** เขียนผ่าน branch + PR → CI ตรวจ → คน/curator merge — ปลอดภัย มี audit/review
- **Lease/lock:** สำหรับทีมที่เขียนหนัก — lease ต่อ concept กันชนกัน เขียนตรงเข้า shared branch

## ความหมายของ "ข้าม session / ข้ามทีม"

- **ข้าม session:** ไม่มี state ต่อ session — session ใหม่ `git pull` ได้ทุกอย่างที่ session ก่อนเขียน wiki ทบต้น
- **ข้ามทีม:** *monorepo* + `CODEOWNERS` ต่อ subtree **หรือ** *federated bundles* (repo ต่อโดเมน,
  MCP server mount หลาย bundle และ namespace ด้วยชื่อ bundle เช่น `sales:tables/orders`)

ต่อไป: ลงมือ deploy → [ติดตั้งแบบ self-host](./self-host.md)

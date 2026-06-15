# โมเดลการเขียน: PR-gated และ Lease

เมื่อหลาย agent เขียนความรู้ร่วมกัน ต้องเลือกว่าจะคุม concurrency ยังไง starter รองรับ 2 โมเดล
(และมีโมเดลที่ 3 เป็นแนวคิด) เลือกด้วย env `OKF_WRITE_MODE`

## โมเดล 1 — PR-gated (ค่าเริ่มต้น)

`okf_propose_change(...)` **ไม่เขียน `main`** แต่:

1. สร้าง branch `okf/<concept>-<id>` จาก `main`
2. เขียนไฟล์ commit push ขึ้น git server ภายใน
3. เปิด PR/MR ผ่าน API ของ git server แล้วคืน URL
4. CI รัน `okf-validate.py` (+ regen viz) → คน/curator รีวิวและ merge

<pre class="mermaid">
flowchart LR
  AG["Agent"] -->|propose_change| BR["branch + commit"]
  BR --> PR["Pull Request"]
  PR --> CIv["CI: okf-validate"]
  CIv --> RV["review (คน/curator)"]
  RV -->|merge| MAIN["main"]
  MAIN -->|webhook| RE["MCP pull + reindex"]
</pre>

ได้คุณสมบัติ enterprise ครบ: **audit trail** (git log), **review/diff**, **rollback** (git revert),
**ไม่มี write conflict** (merge ทีละครั้งตามลำดับ), **quality gate** (CI + review)

เมื่อ merge เข้า `main` → webhook → MCP server `pull` → reindex → ทุก session เห็น

> เหมาะเมื่อ **review ทุกการเปลี่ยนแปลงสำคัญกว่าความเร็ว**

## โมเดล 2 — Lease/lock (เขียนตรง)

เปิดด้วย `OKF_WRITE_MODE=lease` สำหรับทีมที่เขียนหนัก ใช้ **lease (สิทธิ์จองแบบมี TTL)** กันสอง agent
แก้ concept เดียวกันพร้อมกัน

```bash
# flow ต่อ agent:
okf_acquire_lease("tables/orders", ttl_seconds=300)   # → {token, expires_at}
# ... แก้ ...
okf_commit_concept("tables/orders", frontmatter, body, token=...)   # server ตรวจ lease แล้ว write+commit+push
okf_release_lease("tables/orders", token=...)         # คืนเมื่อเสร็จ
```

<pre class="mermaid">
flowchart LR
  ACQ["acquire_lease<br/>(TTL)"] --> ED["edit concept"]
  ED --> CM["commit_concept<br/>(verify token)"]
  CM --> PUSH["pull --rebase + push"]
  PUSH --> REL["release_lease"]
  OT["agent อื่น ขอ concept เดียวกัน"] -.->|locked| ACQ
</pre>

agent อื่นที่ขอ concept เดียวกันจะได้ `{error:"locked", held_by}` → ไปทำตัวอื่น
ความปลอดภัยจาก concurrency: lease กัน concept ซ้ำ + `git pull --rebase` ก่อน push จัดการ
commit คนละไฟล์ (auto-merge)

คุณสมบัติของ lease:

- **advisory + TTL หมดอายุเอง** — agent crash ไม่ทำให้ concept ค้าง (lease ที่หมดอายุถูก "ขโมย" ได้)
- **token-verified** — เฉพาะผู้ถือ lease commit/renew/release ได้
- **single-authority** — MCP server ตัวเดียวแจก lease ด้วยไฟล์ atomic (`O_CREAT|O_EXCL`); git ถูก serialize ด้วย lock

CLI สำหรับ ops: `python3 tools/okf-lease.py list` · `... break <concept>` (admin บังคับปลด)

> เหมาะเมื่อ **throughput การเขียนสำคัญกว่าการรีวิวทุกครั้ง**

## โมเดล 3 — Append-only proposals + curator (แนวคิด)

agent หย่อน proposal ลง `inbox/`; มี **curator agent ตัวเดียว** รวบ, ปรับข้อขัดแย้ง, แล้ว merge เข้า wiki
— quality gate สูงสุด ตรงกับปรัชญา supervised ingest (ยังไม่ implement ใน starter)

## เปรียบเทียบ

| โมเดล | ความเร็ว | review | conflict | เหมาะกับ |
|-------|---------|--------|----------|----------|
| **PR-gated** | ปานกลาง | ทุกครั้ง | ไม่มี (merge ตามลำดับ) | governance, ทีมทั่วไป |
| **Lease/lock** | เร็ว | อ่อน | กันด้วย lease | ทีมเขียนหนัก |
| **Curator** | ช้า | สูงสุด | curator จัดการ | คุณภาพสำคัญสุด |

> 💡 **รันได้ทั้งสองโหมดบน repo เดียว** — ทีมเขียนหนักใช้ server โหมด lease, ที่เหลือ PR-gated ชี้ git ตัวเดียวกัน

ต่อไป: ค้นหาเมื่อ wiki โตใหญ่ → [Search ระดับ scale และ semantic](./scaling-search.md)

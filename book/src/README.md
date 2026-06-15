<div class="okf-cover">
<svg class="okf-net" viewBox="0 0 800 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><g stroke="#fff" stroke-width="1.2" fill="#fff"><line x1="80" y1="60" x2="220" y2="140"/><line x1="220" y1="140" x2="380" y2="80"/><line x1="380" y1="80" x2="540" y2="170"/><line x1="540" y1="170" x2="700" y2="90"/><line x1="220" y1="140" x2="300" y2="250"/><line x1="540" y1="170" x2="480" y2="260"/><line x1="380" y1="80" x2="620" y2="220"/><circle cx="80" cy="60" r="6"/><circle cx="220" cy="140" r="8"/><circle cx="380" cy="80" r="7"/><circle cx="540" cy="170" r="8"/><circle cx="700" cy="90" r="6"/><circle cx="300" cy="250" r="6"/><circle cx="480" cy="260" r="6"/><circle cx="620" cy="220" r="7"/></g></svg>
<div class="okf-cover-logo"><svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><circle cx="32" cy="13" r="6" fill="#fff"/><circle cx="13" cy="46" r="6" fill="#fff"/><circle cx="51" cy="46" r="6" fill="#fff"/><g stroke="#fff" stroke-width="2.5" opacity="0.85"><line x1="32" y1="13" x2="13" y2="46"/><line x1="32" y1="13" x2="51" y2="46"/><line x1="13" y1="46" x2="51" y2="46"/></g></svg></div>
<div class="okf-cover-badge">OKF v0.1 · คู่มือฉบับภาษาไทย</div>
<h1 class="okf-cover-title">Open Knowledge Format<small>สร้าง knowledge base ที่ AI ช่วยดูแล — ตั้งแต่เริ่มต้นจนถึงระดับองค์กร</small></h1>
<p class="okf-cover-sub">ฐานความรู้ที่เก็บเป็นไฟล์ Markdown ธรรมดา ที่ทั้งคนและ AI agent อ่าน เขียน และใช้งานร่วมกันได้</p>
<div class="okf-cover-cta">
<a class="okf-btn okf-btn-primary" href="./part1/what-is-okf.md">เริ่มอ่าน →</a>
<a class="okf-btn" href="./okf-manual-th.pdf">📄 ดาวน์โหลด PDF</a>
<a class="okf-btn" href="./viz-example.html">🕸 ดู graph ตัวอย่าง</a>
</div>
<div class="okf-cover-meta">เรียบเรียงโดย <strong>Supachai Jaturaprom [TumEz]</strong><br/>เขียนโดย Claude Code — Opus 4.8 (AI) · ปรับปรุง <span id="okf-date">2026-06-15</span> · OKF v0.1</div>
</div>

# คำนำ

ยินดีต้อนรับสู่ **คู่มือ Open Knowledge Format (OKF)** ฉบับภาษาไทย — หนังสือที่จะพาคุณสร้างและดูแล
**knowledge base ที่ AI ช่วยดูแล** ด้วยรูปแบบ OKF: ฐานความรู้ที่เก็บเป็นไฟล์ Markdown กับ YAML frontmatter
ที่ทั้งคนและ AI agent ใช้งานร่วมกันได้ โดยไม่ต้องพึ่ง SDK หรือฐานข้อมูลเฉพาะทาง

> 🌐 อ่านฉบับภาษาอังกฤษได้ที่ปุ่ม **EN** มุมขวาบน (English version available — click **EN** in the top bar)

## สารบัญ

<div class="okf-toc-grid">
<a class="okf-toc-card" href="./part1/what-is-okf.md"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><line x1="12" y1="11" x2="12" y2="16"/><line x1="12" y1="8" x2="12" y2="8"/></svg><span class="num">ภาคที่ 1</span><span class="ttl">รู้จัก OKF</span><span class="dsc">OKF คืออะไร · ประวัติศาสตร์ · ทำไมดีกว่า RAG</span></a>
<a class="okf-toc-card" href="./part2/install.md"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="8 5 19 12 8 19 8 5"/></svg><span class="num">ภาคที่ 2</span><span class="ttl">เริ่มต้นใช้งาน</span><span class="dsc">ติดตั้ง · สร้าง KB แรก · โครงสร้างโปรเจกต์</span></a>
<a class="okf-toc-card" href="./part3/concepts.md"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M12 12l8-4.5"/><path d="M12 12v9"/><path d="M12 12L4 7.5"/></svg><span class="num">ภาคที่ 3</span><span class="ttl">แนวคิดหลัก</span><span class="dsc">concept · frontmatter · การลิงก์ · ไฟล์สงวน</span></a>
<a class="okf-toc-card" href="./part4/ingest.md"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9l3 3-3 3"/><line x1="13" y1="15" x2="17" y2="15"/></svg><span class="num">ภาคที่ 4</span><span class="ttl">การใช้งานประจำวัน</span><span class="dsc">ingest · query/search · เขียน concept · validate/viz</span></a>
<a class="okf-toc-card" href="./part5/best-practices.md"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20l1-4L16 5l3 3L8 19z"/><line x1="14" y1="7" x2="17" y2="10"/></svg><span class="num">ภาคที่ 5</span><span class="ttl">เขียนให้ดี</span><span class="dsc">แนวทางการเขียนและ anti-patterns</span></a>
<a class="okf-toc-card" href="./part6/architecture.md"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="7" rx="1.5"/><rect x="3" y="13" width="18" height="7" rx="1.5"/><line x1="7" y1="7.5" x2="7" y2="7.5"/><line x1="7" y1="16.5" x2="7" y2="16.5"/></svg><span class="num">ภาคที่ 6</span><span class="ttl">ระดับองค์กร</span><span class="dsc">self-host · MCP · write models · security</span></a>
<a class="okf-toc-card" href="./appendix/tools.md"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 4h12v16l-6-4-6 4z"/></svg><span class="num">ภาคผนวก</span><span class="ttl">อ้างอิง</span><span class="dsc">CLI reference · FAQ · อภิธานศัพท์ · บรรณานุกรม</span></a>
</div>

## หนังสือเล่มนี้เหมาะกับใคร

- **ผู้เริ่มต้น** ที่อยากมี knowledge base ส่วนตัว/ของทีม ที่ค้นได้และไม่ผูกกับ vendor
- **นักพัฒนา/ทีมข้อมูล** ที่อยากให้ AI agent เข้าถึงความรู้ภายในองค์กรอย่างเป็นระบบ
- **สถาปนิกระบบ/ทีม platform** ที่ต้องวางระบบใช้ร่วมกัน **ข้าม session และข้ามทีม ระดับองค์กร (on-prem)**

ไม่ต้องมีพื้นฐาน OKF มาก่อน ขอแค่พอใช้ command line และ Git ได้บ้าง

## ข้อตกลงในหนังสือ

- คำสั่งที่พิมพ์ใน terminal อยู่ในกล่องโค้ด · **ศัพท์เทคนิค** (`concept`, `frontmatter`, `bundle`, `MCP`)
  คงไว้เป็นภาษาอังกฤษเพื่อให้ตรงกับเอกสารต้นทางและโค้ด · กล่อง blockquote คือข้อควรระวัง/เคล็ดลับ

> **หมายเหตุเรื่องเวอร์ชัน:** OKF เป็นสเปก **v0.1** (เผยแพร่ 12 มิ.ย. 2026 โดย Google Cloud) สเปกหลักบังคับแค่
> ฟิลด์ `type` — "แนวปฏิบัติที่ดี" อื่น ๆ ในเล่มนี้ส่วนใหญ่มาจากชุมชน LLM-wiki และ reference implementation ของ Google

โปรเจกต์ต้นทาง (โค้ด + เครื่องมือทั้งหมด): **<https://github.com/supachai-j/open-knowledge-format-starter>**

เริ่มกันเลยที่ [OKF คืออะไร](./part1/what-is-okf.md)

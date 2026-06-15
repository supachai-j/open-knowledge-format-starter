<div class="okf-cover">
<svg class="okf-net" viewBox="0 0 800 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><g stroke="#fff" stroke-width="1.2" fill="#fff"><line x1="80" y1="60" x2="220" y2="140"/><line x1="220" y1="140" x2="380" y2="80"/><line x1="380" y1="80" x2="540" y2="170"/><line x1="540" y1="170" x2="700" y2="90"/><line x1="220" y1="140" x2="300" y2="250"/><line x1="540" y1="170" x2="480" y2="260"/><line x1="380" y1="80" x2="620" y2="220"/><circle cx="80" cy="60" r="6"/><circle cx="220" cy="140" r="8"/><circle cx="380" cy="80" r="7"/><circle cx="540" cy="170" r="8"/><circle cx="700" cy="90" r="6"/><circle cx="300" cy="250" r="6"/><circle cx="480" cy="260" r="6"/><circle cx="620" cy="220" r="7"/></g></svg>
<div class="okf-cover-badge">OKF v0.1 · English Handbook</div>
<h1 class="okf-cover-title">Open Knowledge Format<small>Build an AI-maintained knowledge base — from beginner to enterprise</small></h1>
<p class="okf-cover-sub">A knowledge base stored as plain Markdown files that humans and AI agents can read, write, and use together.</p>
<div class="okf-cover-cta">
<a class="okf-btn okf-btn-primary" href="./part1/what-is-okf.md">Start reading →</a>
<a class="okf-btn" href="./okf-manual-en.pdf">📄 Download PDF</a>
<a class="okf-btn" href="./viz-example.html">🕸 See an example graph</a>
</div>
</div>

# Preface

Welcome to **The Open Knowledge Format (OKF) Handbook**. This book walks you through building and
operating an **AI-maintained knowledge base** with OKF — a knowledge base stored as Markdown files
with YAML frontmatter that both humans and AI agents can use, without any SDK or special database.

> 🌐 อ่านฉบับภาษาไทยได้ที่ปุ่ม **ไทย** มุมขวาบน (Thai version available — click **ไทย** in the top bar)

## Table of Contents

<div class="okf-toc-grid">
<a class="okf-toc-card" href="./part1/what-is-okf.md"><span class="num">PART 1</span><span class="ttl">Meet OKF</span><span class="dsc">What OKF is, and why it beats classic RAG</span></a>
<a class="okf-toc-card" href="./part2/install.md"><span class="num">PART 2</span><span class="ttl">Getting Started</span><span class="dsc">Install · first KB · project layout</span></a>
<a class="okf-toc-card" href="./part3/concepts.md"><span class="num">PART 3</span><span class="ttl">Core Concepts</span><span class="dsc">concept · frontmatter · linking · reserved files</span></a>
<a class="okf-toc-card" href="./part4/ingest.md"><span class="num">PART 4</span><span class="ttl">Everyday Operations</span><span class="dsc">ingest · query/search · authoring · validate/viz</span></a>
<a class="okf-toc-card" href="./part5/best-practices.md"><span class="num">PART 5</span><span class="ttl">Authoring Well</span><span class="dsc">best practices and anti-patterns</span></a>
<a class="okf-toc-card" href="./part6/architecture.md"><span class="num">PART 6</span><span class="ttl">Enterprise</span><span class="dsc">self-host · MCP · write models · security</span></a>
<a class="okf-toc-card" href="./appendix/tools.md"><span class="num">APPENDIX</span><span class="ttl">Reference</span><span class="dsc">CLI reference · FAQ · glossary</span></a>
</div>

## Who this book is for

- **Beginners** who want a searchable, vendor-neutral personal/team knowledge base
- **Developers / data teams** who want AI agents to reach internal knowledge systematically
- **Architects / platform teams** who need a shared system **across sessions and teams, on-prem**

No prior OKF knowledge needed — just basic command line and Git.

## Conventions

- Commands you type go in code blocks · **technical terms** (`concept`, `frontmatter`, `bundle`, `MCP`)
  stay in English to match the source docs and code · blockquotes are warnings/tips

> **Versioning note:** OKF is a **v0.1** spec (published 2026-06-12 by Google Cloud). The core spec
> requires only the `type` field — most "best practices" here come from the LLM-wiki community and
> Google's reference implementation.

Source project (code + all tools): **<https://github.com/supachai-j/open-knowledge-format-starter>**

Start at [What is OKF](./part1/what-is-okf.md)

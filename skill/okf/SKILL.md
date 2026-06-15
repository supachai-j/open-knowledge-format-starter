---
name: okf
description: Create and operate an Open Knowledge Format (OKF v0.1) knowledge base — a directory of Markdown files with YAML frontmatter that an AI agent maintains as an "LLM-wiki". Use to INITIALIZE a new bundle in any project, INGEST a source, QUERY/SEARCH the wiki, ADD/EDIT a concept, VALIDATE conformance, VISUALIZE the graph, or coordinate concurrent writes with leases. Triggers on "start an OKF knowledge base", "init okf", "ingest this into the wiki/KB", "what does the wiki say about X", "search the knowledge base", "create an OKF concept", "validate the bundle", "เริ่ม/สร้าง knowledge base", "เก็บเข้า wiki", "ถาม wiki", "ตรวจ bundle". Do NOT use for unrelated web research or non-OKF notes.
---

# OKF Knowledge Base Operator

Build and run an **Open Knowledge Format (OKF) v0.1** bundle: Markdown + YAML-frontmatter concepts
that humans and agents co-maintain. This skill bundles all the tooling under `scripts/` (relative to
this skill's directory) — pure-Python, zero external services, air-gap friendly.

> **Scripts location:** everything below runs from this skill's `scripts/` folder. If you're inside a
> project that already has the tools in `tools/`, use those instead — they're identical.
> **Bundle location:** the OKF bundle is the project's `wiki/` directory. Pass it explicitly to scripts.

## Concept model (read first)
- One `.md` file = one **concept**. **Concept ID** = its path under `wiki/` minus `.md` (`tables/orders.md` → `tables/orders`).
- Frontmatter: **`type` is the only required field**; recommended `title`, `description`, `resource`, `tags`, `timestamp` (ISO 8601).
- Curated/derived knowledge (joins, metric defs) → `references/` with `type: Reference`.
- **Links: file-relative only** (`../tables/orders.md`). **Never start a link with `/`** (breaks GitHub). Links are untyped — relationship lives in the prose. Broken links are allowed (= unwritten knowledge).
- Reserved files: `index.md` (catalog, per directory) and `log.md` (append-only, `## YYYY-MM-DD`).

---

## Operation: INIT — scaffold a new bundle in this project
```bash
python3 scripts/okf-init.py .            # creates AGENTS.md + wiki/{index.md,log.md,getting-started.md} + raw/
python3 scripts/okf-validate.py ./wiki   # confirm conformant
```

## Operation: INGEST a source  (supervised — a quality gate, NEVER automatic)
1. Read the source in `raw/`. 2. Read `wiki/index.md` for what exists. 3. Extract 5–15 key claims.
4. **Show the user the claims + proposed concept mappings and WAIT for approval before writing.**
5. Reconcile contradictions: append `> **CONTRADICTION FLAG**: …` to the superseded concept.
6. Write/update concepts (start from `scripts/concept-template.md`); update `tags`+`timestamp`.
7. Update affected `index.md`; append to `wiki/log.md` under today's date. 8. Run VALIDATE.

## Operation: QUERY / SEARCH
- Small wiki: read `wiki/index.md`, drill into concepts, answer **only** from loaded concepts, cite Concept IDs.
- Larger wiki: `python3 scripts/okf-index.py build ./wiki` then
  `python3 scripts/okf-search.py "your question" --bundle ./wiki -k 8`
  (hybrid BM25 + optional on-prem semantic via Ollama, RRF-fused; auto-falls back to BM25).

## Operation: ADD / EDIT a concept
Copy `scripts/concept-template.md`, set a real `type`, write the body with file-relative links,
update `index.md` + `log.md`, then VALIDATE.

## Operation: VALIDATE  (always before declaring done)
```bash
python3 scripts/okf-validate.py ./wiki   # → ✓ CONFORMANT with OKF v0.1
```

## Operation: VISUALIZE
```bash
python3 scripts/okf-viz.py ./wiki --name "My Wiki"   # → wiki/viz.html (single self-contained file)
```

## Operation: SEMANTIC search (optional, on-prem)
```bash
ollama pull nomic-embed-text
python3 scripts/okf-embed.py build ./wiki            # embeddings → wiki/.okf-embed.json
```
Then `okf-search.py` automatically fuses semantic + BM25. No Ollama → it stays BM25-only.

## Operation: LEASE (concurrent multi-agent writes)
Advisory, TTL-expiring per-concept locks so two agents don't edit the same file:
```bash
python3 scripts/okf-lease.py acquire tables/orders --owner me --ttl 300   # → {token}
python3 scripts/okf-lease.py list
python3 scripts/okf-lease.py release tables/orders --owner me --token <token>
```

## Guardrails
- Never auto-ingest in the background — the human "is this worth keeping?" decision is the quality gate.
- Never invent facts; leave a broken-link placeholder instead. Never edit `raw/` (read-only ground truth).
- Keep prose readable for humans; structure (headings/tables) for the machine.

## Enterprise / self-hosted
For cross-session, cross-team, on-prem use (internal MCP server over git, PR-gated or lease-gated writes,
CI conformance gate, Docker deploy), see the source project's `server/`, `deploy/`, and `docs/ENTERPRISE.md`:
https://github.com/supachai-j/open-knowledge-format-starter

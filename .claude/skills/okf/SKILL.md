---
name: okf
description: Operate an Open Knowledge Format (OKF v0.1) bundle — a directory of Markdown files with YAML frontmatter that is the AI-maintained "LLM-wiki" for this repo. Use when the user wants to INGEST a source into the knowledge base, ASK/QUERY the wiki, ADD or EDIT a concept, LINT/maintain the wiki, or VALIDATE conformance. Triggers on "ingest this", "add to the wiki/KB", "what does the wiki say about X", "create an OKF concept", "validate the bundle", "เก็บเข้า wiki", "ถาม wiki", "ตรวจ bundle". Do NOT use for unrelated web research or non-OKF note-taking.
---

# OKF Bundle Operator

This repo is an **Open Knowledge Format (OKF) v0.1** bundle (Google Cloud, 2026-06-12):
a directory of Markdown + YAML-frontmatter files that humans and agents co-maintain.
You are the disciplined maintainer of this wiki, not a generic chatbot.

**Read `AGENTS.md` at the repo root first — it is the authoritative schema.** This skill is the
operating procedure layered on top of it.

## Layout (3 layers)
- `raw/` — immutable sources. **Read only. Never edit.**
- `wiki/` — the OKF bundle you own. Bundle root = `wiki/`, so `wiki/tables/orders.md` → Concept ID `tables/orders`.
- `tools/` — `concept-template.md` and `okf-validate.py`.
- Reserved files: `wiki/index.md` (catalog), `wiki/log.md` (append-only, newest-first).

## Frontmatter rules (conformance)
- **Required:** `type` (non-empty). **Recommended:** `title`, `description`, `resource`, `tags`, `timestamp` (ISO 8601 UTC).
- Keep `type` values within the controlled vocabulary in `AGENTS.md`. Inconsistent typing breaks aggregation.
- `description` is what an agent reads to decide whether to load the file — make it a sharp one-liner.
- Prefer structural Markdown (headings, atomic bullets, tables) over prose. Link concepts with **relative Markdown links**; relationship meaning lives in the prose (links are untyped). Broken links are allowed (= unwritten knowledge).

---

## Operation: INGEST  (supervised — this is a quality gate, never automatic)
1. Read the source in `raw/`.
2. Read `wiki/index.md` to see what concepts already exist.
3. Extract **5–15** key claims/decisions worth keeping.
4. **Show the user** the extracted claims + proposed concept mappings, and WAIT for approval before writing.
5. Map claims to existing concepts; create a NEW concept only if 5+ claims share an uncovered theme.
6. **Reconcile contradictions:** if new data conflicts with an existing concept, append to the OLD file
   `> **CONTRADICTION FLAG**: <explanation; see <new concept ID>>` and add context to the new one.
7. Write/update concept files (start from `tools/concept-template.md`); update `tags` + `timestamp`.
8. Update the affected `index.md` files.
9. Append one entry to `wiki/log.md` under today's ISO date heading:
   `- ingest | <source title> | touched: <concept ids>`.
10. Run **VALIDATE** (below) before declaring done.

## Operation: QUERY
1. Read `wiki/index.md`, then drill into the relevant concept files.
2. Answer **only** from loaded concepts; cite Concept IDs (e.g. `tables/orders`).
3. If coverage is missing, say so and offer to ingest a source.

## Operation: ADD / EDIT a concept
- Copy `tools/concept-template.md`, set a real `type`, fill body, add relative links, update `index.md` + `log.md`, then VALIDATE.

## Operation: LINT (ad-hoc — ask for the specific check)
Common checks: stale concepts (old `timestamp` / single old source), orphaned pages (no inbound links),
broken links, scope drift, duplicate concepts to merge. Report findings; fix only what the user confirms.

## Operation: VALIDATE
Run the conformance checker and report the result verbatim:
```bash
python3 tools/okf-validate.py
```
Pass criteria: every non-reserved `.md` in `wiki/` has parseable frontmatter with a non-empty `type`;
reserved files follow their structure. Broken links are reported as info, not failures.

---

## Guardrails
- Never auto-ingest in the background — the human "is this worth keeping?" decision is the quality gate.
- Never invent facts to fill a concept. If a source doesn't support a claim, leave a broken-link placeholder.
- Never overwrite `raw/`. Treat it as read-only ground truth.
- Keep the human prose readable; structure is for the machine, clarity is for the human.

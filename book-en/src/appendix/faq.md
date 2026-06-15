# Frequently Asked Questions (FAQ)

### How is OKF different from Obsidian / Notion?
They are quite similar (Markdown + frontmatter + links), but OKF is **specified** — it defines the minimal rules necessary for interoperability (e.g. `type` is required, reserved files, conformance rules) without mandating a tool. You can open an OKF bundle in Obsidian/MkDocs/Hugo directly because it is just Markdown.

### Do I need Google Cloud / BigQuery?
No. OKF is vendor-neutral. The reference examples use BigQuery but `type` can be anything. This starter is not tied to any cloud provider.

### Do I need an AI agent?
No. You can write concepts by hand yourself (they are just Markdown). AI agents simply handle the heavy lifting — summarizing, cross-referencing, filing, and bookkeeping.

### Should links be relative or absolute?
**Relative only.** Do not prefix with `/` because it breaks GitHub rendering (see [Linking](../part3/linking.md)). Although the spec suggests absolute links, the actual Google implementation uses relative ones.

### Is a broken link an error?
No — it represents "knowledge not yet written." `okf-validate.py` reports it as info, not an error.

### Can I fully automate ingest?
**Strongly not recommended** — a background daemon will accumulate noise until the wiki rots. Ingest should be a human-triggered command with a review step.

### How large does the wiki need to be before search is necessary?
Around **~150 pages**. Before that, `index.md` is sufficient. Beyond that, use `okf-search.py` (BM25) and add semantic search when recall is insufficient.

### Do I need Ollama to search?
No. BM25 works without Ollama. Semantic search is an optional upgrade. If Ollama is not running, search automatically falls back to BM25.

### What do I do when multiple agents write concurrently?
Choose a write model: **PR-gated** (safe, with review) or **lease/lock** (faster, for write-heavy teams). See [Write Models](../part6/write-models.md).

### Does it work air-gapped (closed network)?
Yes — `viz.html` embeds its libraries, tools use stdlib only, semantic search uses on-prem Ollama, and git/MCP run internally.

### Do `.okf-index.json` / `.okf-embed.json` need to be committed?
No — they are generatable artifacts and are already in `.gitignore`. CI/MCP server regenerates them on demand.

### validate shows "missing type" — how do I fix it?
Every concept must have a non-empty `type` in its frontmatter. Add `type: ...` (chosen from the controlled vocabulary).

### How do I migrate an existing wiki (Obsidian, etc.) into OKF?
In most cases: add a `type` field to each frontmatter, add `index.md`/`log.md`, convert links to relative paths, then run validate.

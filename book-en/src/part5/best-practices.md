# Writing Guidelines and Anti-patterns

These guidelines layer on top of the spec (which only enforces `type`) to make the wiki reliable for both humans and agents.

## Golden Rules

1. **One concept per file** — do not cram three topics into one file
2. **Write `description` for the agent** — this is the single line an agent reads to decide whether to load the file; make it specific
3. **Structure beats paragraphs** — headings, bullets (`**key** — value`), tables; models extract information from structured Markdown more accurately
4. **identity = path** — use stable kebab-case filenames; renaming breaks inbound links
5. **Consistent `type`** — use a controlled vocabulary
6. **Always cite sources** — every synthesized claim should be traceable to a file in `raw/`; add them under `# Citations`

## Anti-pattern Table

| Anti-pattern | Why it is bad | Do this instead |
|--------------|---------------|-----------------|
| **Automated background ingest** | Accumulates noise as fast as signal; the wiki decays silently | Make ingest an explicit human-triggered command with review |
| **Dumping raw PDFs into `wiki/`** | Unreliable retrieval; breaks synthesis | Synthesize into a concept Markdown file; keep the raw file in `raw/` |
| **Over-stuffed frontmatter** | Noise reduces search precision | Keep `tags` semantic and minimal |
| **Skipping heading levels** (H1→H3) | Breaks document structure for the model | Maintain H1→H2→H3 order |
| **Paragraphs interspersed in lists** | The list splits into fragments in the parser's view | Use nested paragraphs, or close the list first |
| **Inconsistent `type`/field names** | Tools cannot aggregate the data | Use a controlled vocabulary |
| **Vague anchor text** ("click here") | No topic signal for the LLM | Use descriptive link text |
| **Absolute paths starting with `/`** | Breaks GitHub rendering | Use relative paths |
| **Sacrificing readability for machines** | The wiki must serve humans too | Structure for machines; clarity for humans |

## Core Spec vs. Community Best Practices

Keep these separate:

- **OKF v0.1 spec (very small):** enforces only `type` + index/log rules + conformance rules
- **Best practices (in this book):** mostly from the LLM-wiki community and the Google reference implementation
  — e.g., confidence decay, hybrid search, grouping `references/` — these are supplementary patterns, not requirements

## Points Where Sources Disagree

- **"RAG is dead"** — most engineers say wiki = Layer 1, RAG = Layer 2 fallback; it is not either/or
- **Absolute vs. relative links** — the spec recommends absolute, but implementations use relative (we follow the implementation)
- **Four-dimension freshness scoring** — a guideline promoted by a vendor (Atlan), not part of the spec

Next, move to the enterprise level → [Architecture Overview](../part6/architecture.md)

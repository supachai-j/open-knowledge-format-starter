# Findings: GoogleCloudPlatform/knowledge-catalog → improvements to this starter

Deep-read of the **official OKF reference implementation**
([GoogleCloudPlatform/knowledge-catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog),
Apache-2.0, ~1.4k★, pushed 2026-06-14) on 2026-06-15, to harden this starter against ground truth.

## What the repo actually contains

| Path | What it is |
| :--- | :--- |
| `okf/SPEC.md` | The normative **OKF v0.1 (Draft)** spec — the authoritative source. |
| `okf/README.md` | "Enrichment Agent — an OKF proof of concept." Format is the contribution; agent + viewer make it tangible. |
| `okf/bundles/{ga4,stackoverflow,crypto_bitcoin}/` | Three real, browsable bundles produced by the agent — each ships a `viz.html`. |
| `okf/src/enrichment_agent/` | Reference **producer**: ADK + Gemini agent. BQ pass (metadata) + web pass (LLM-as-crawler). |
| `okf/src/enrichment_agent/viewer/` | Reference **consumer**: a self-contained HTML graph viewer generator. |
| `okf/src/enrichment_agent/prompts/` | The agent's actual instruction prompts (enrichment + web ingestion). |

## Key findings (and how each maps to a change here)

### 1. Spec vs. implementation disagree on link form — implementation wins
- **SPEC §5.1** *recommends* bundle-root-**absolute** links (`/tables/customers.md`) as "stable when documents move."
- **The agent's own `enrichment_instruction.md`** says the opposite, verbatim:
  > "Use file-relative paths only. **Never start a link with `/`** (that breaks GitHub rendering)."
- Every real bundle (e.g. `ga4/tables/events_.md`) uses **relative** links (`../references/metrics/event_count.md`).
- ✅ **Our starter already used relative links — confirmed correct.** Added an explicit "never `/`" rule to
  `AGENTS.md`/`SKILL.md`, and the validator now **warns on `/`-rooted links**.

### 2. The flagship consumer feature: a self-contained `viz.html`
- Every bundle commits a `viz.html` — one file, no backend, Cytoscape.js (graph) + marked (markdown), CDN-loaded,
  bundle embedded as JSON. Shows: type-colored force graph, detail panel with rendered body, **"Cited by" backlinks**,
  search, type filter, layout switch; internal links rewired to navigate in-viewer.
- ✅ **Ported as `tools/okf-viz.py`** (zero-dependency). Generates `wiki/viz.html`; backlinks + link-rewiring included.

### 3. Canonical bundle structure
- Real layout: `index.md` (lists subdirs) · `datasets/` (`BigQuery Dataset`) · `tables/` (`BigQuery Table`) ·
  `references/{metrics,joins}/` (**`type: Reference`**). Derived/curated knowledge lives under `references/`.
- ✅ Added `wiki/references/joins/orders__customers.md` (`type: Reference`) + indexes; expanded the controlled
  `type` vocabulary (`BigQuery Dataset`, `Reference`) and documented the grouping in `AGENTS.md`.

### 4. `index.md` format & the `okf_version` declaration
- Index files carry **no frontmatter**, except the **bundle-root** index may declare `okf_version` (SPEC §11).
- Format is flat sections of `* [Title](relative-url) - description`.
- ✅ Reworked all `index.md` to the flat format; added `okf_version: "0.1"` to `wiki/index.md`. Validator now
  enforces the index-frontmatter rule.

### 5. `log.md` heading format
- SPEC §7 uses `## YYYY-MM-DD` (**no brackets**) with `* **Update**/**Creation**/**Deprecation**:` entries.
- ✅ Our earlier `## [YYYY-MM-DD]` (a community convention, not OKF) was switched to the spec form. Validator
  now warns on non-ISO log headings.

### 6. Conventional body sections & the two-pass producer model
- The enrichment prompt favors: prose overview → `# Schema` (flatten nested RECORDs) → `# Common query patterns`
  (`sql` fences) → `# Citations` (numbered `[1] [Title](url)`, first entry = the `resource`). One concept per write.
- The agent runs a **BQ pass** (metadata-only docs) then a **web pass** (LLM crawls seed URLs under a same-domain +
  max-pages cap, choosing to enrich a doc, mint a `references/<slug>`, or skip).
- ✅ Encoded the section ordering into `AGENTS.md`/`SKILL.md`; the two-pass model informs our supervised INGEST flow.

## What we deliberately did NOT copy
- The **ADK/Gemini/BigQuery producer agent** — heavy, GCP-specific, and orthogonal to a vendor-neutral starter.
  Our producer is the human-supervised INGEST workflow in `AGENTS.md` (any agent, any model).
- **Absolute links** (see finding 1).

## Net result
Bundle grew from 4 → 5 concepts across 4 types; `tools/okf-validate.py` reports **CONFORMANT, 0 warnings, 0 info**;
`wiki/viz.html` renders the graph. Conventions now track the reference implementation, not just the spec prose.

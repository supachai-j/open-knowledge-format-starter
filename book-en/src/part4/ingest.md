# Ingest: Adding Knowledge to the Wiki

**Ingest** is the process of taking raw source material and synthesizing it into concepts in the wiki. This is the heart of making the wiki "richer."

## The Most Important Principle: Ingest Must Be Human-Supervised

> 🚫 **Do not run ingest automatically in the background (as a background daemon)**
>
> This is the most critical anti-pattern — a daemon that swallows everything it sees will **accumulate noise as fast as it accumulates signal**,
> and the wiki will **rot silently** until nothing in it can be trusted.
>
> Keep ingest as a **deliberate human command** — the human decision "is this source worth synthesizing?"
> is the **quality gate** that eliminates an entire class of failures.

## Ingest Steps (Human-Supervised)

1. **Read the source** in `raw/`
2. **Read `wiki/index.md`** to see what concepts already exist
3. **Extract 5–15 key points** (claims/decisions/insights) worth keeping
4. **Show the extracted points + their proposed mapping to concepts for your approval — then wait before writing anything**
5. **Reconcile contradictions** — if new information conflicts with an existing concept, add a flag to the old file:
   ```markdown
   > **CONTRADICTION FLAG**: New findings supersede this value. See references/metrics/new-wau.md
   ```
6. **Write/update the concept** (starting from the template), update `tags` + `timestamp`
7. **Update the relevant `index.md`**
8. **Add an entry to `log.md`** under today's date
9. **Run validate** before considering the work done

## Using via AI Agent

If the skill is installed, simply say:

```
ingest raw/q3-strategy.pdf into the wiki
```

The agent will follow the steps above — extracting key points, **showing them for your approval first**, then writing the concept,
and updating `index.md` and `log.md`.

## Why Reconcile Contradictions Every Time

Suppose a paper says "Model Z is best" but the wiki has a page that says "Model X is best."

- **Traditional RAG:** both pages coexist; the agent may retrieve the old page and answer incorrectly with confidence.
- **OKF (agentic ingest):** every time knowledge is added, it **checks the surroundings** for conflicts, supersessions, and confirmations,
  then writes those relationships explicitly — the old page gets flagged "superseded, see B" and the new page gets context "updated from A."
  **Both pages are correct simultaneously** — the wiki has a consistent "present tense."

## Tips

- **Ingest one source at a time** and stay present to review it — read the summary, check the updates, guide the focus.
- A single source may touch 10–15 pages in the wiki (concepts + entities + indexes + log).
- Start ingest **selectively** — no need to pour everything in at once. The cold-start problem is smaller than you think,
  because the topics you care about most tend to be covered first.

Next: once you have knowledge in the wiki, how do you query and search it? → [Query and Search](./query-search.md)

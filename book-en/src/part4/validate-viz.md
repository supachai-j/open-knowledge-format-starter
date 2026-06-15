# Validate and Visualize

## Validate — Check Conformance

Run this after every edit:

```bash
python3 tools/okf-validate.py ./wiki
# → ✓ CONFORMANT with OKF v0.1  (0 warning(s), 0 info)
```

### Conformance Criteria (OKF v0.1)

A bundle passes when:

1. Every `.md` file that is not a reserved file has **parseable YAML frontmatter**
2. Every frontmatter has a **non-empty `type` field**
3. Reserved files (`index.md`, `log.md`) that exist follow the defined structure

### Result Levels

| Level | Meaning | Example |
|-------|---------|---------|
| ✗ **error** | Not conformant (must fix) | Missing frontmatter / missing `type` / index.md has disallowed frontmatter |
| ! **warn** | Passes, but should fix | Link starts with `/` (breaks GitHub) / log heading is not ISO |
| · **info** | Not a problem | Broken link (spec §5.3 permits this) |

> Consumers **must not reject** a bundle because of: missing optional fields, unknown `type`, extra keys, broken links,
> or a missing `index.md` — this is "permissive consumption," which keeps OKF usable even as bundles grow or get refactored.

## Visualize — View the Knowledge Graph

```bash
python3 tools/okf-viz.py ./wiki --name "My Wiki"
# → wiki/viz.html  (single file, open in a browser)
```

`viz.html` is a **single self-contained HTML file** — it embeds the library (Cytoscape + marked) and the bundle data
directly inside, **fetching nothing from the network when opened**. Suitable for air-gapped environments, file sharing, or committing alongside the bundle.

### What the Viewer Shows

- **Force-directed graph** of all concepts, colored by `type`, with edges drawn from links in the content
- **Detail panel** for the selected concept: frontmatter + rendered body
- **"Cited by"** — backlinks (which other concepts link to this one)
- **Search box** (matches title/id/tags), **type filter**, and toggleable layouts

> By default it **embeds libraries from `tools/vendor/`**, enabling true air-gap use. To use a CDN instead, pass `--cdn`.

### Try the Live Demo

Below is the `viz.html` of the example wiki included in this project (click a node to see its details; try searching and filtering by type):

<iframe class="okf-screen-only" src="../viz-example.html" title="OKF graph example" loading="lazy" style="width:100%;height:520px;border:1px solid var(--table-border-color,#ddd);border-radius:12px;margin:0.5rem 0;"></iframe>

<div class="okf-print-only okf-embed-fallback">
🕸 <strong>Interactive graph</strong> — shown on the web only (iframes don't render in the PDF).<br>
View it online at: <span class="okf-url">https://supachai-j.github.io/open-knowledge-format-starter/en/viz-example.html</span>
</div>

[Open full-screen →](../viz-example.html)

## Make It a Habit

Combine both commands after every editing session:

```bash
python3 tools/okf-validate.py ./wiki && python3 tools/okf-viz.py ./wiki
```

At an organizational level, CI runs validate on every PR and regenerates the viz automatically (see Part 6).

That wraps up the day-to-day usage section. Next, see guidelines for writing well → [Authoring Guidelines and Anti-Patterns](../part5/best-practices.md)

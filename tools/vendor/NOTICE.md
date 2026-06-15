# Vendored third-party libraries

These are committed so `okf-viz.py` can produce a **fully self-contained, air-gapped**
`viz.html` (no CDN, no network at view time). Both are MIT-licensed.

| File | Library | Version | License | Upstream |
|------|---------|---------|---------|----------|
| `cytoscape.min.js` | Cytoscape.js | 3.30.2 | MIT | https://github.com/cytoscape/cytoscape.js |
| `marked.min.js` | marked | 12.0.2 | MIT | https://github.com/markedjs/marked |

To update: re-download the same paths from `https://cdn.jsdelivr.net/npm/<lib>@<version>/...`
and bump the versions referenced in `tools/okf-viz.py` (the `--cdn` fallback URLs).

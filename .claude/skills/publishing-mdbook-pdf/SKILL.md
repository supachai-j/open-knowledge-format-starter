---
name: publishing-mdbook-pdf
description: Publish a book / handbook / manual as an mdBook site on GitHub Pages WITH a print-quality PDF — cover page, running header + page-number footer with a credit line, REAL table-of-contents page numbers, Mermaid diagrams, non-Latin (e.g. Thai) fonts, and an optional single-file air-gap HTML viewer. Use when the user wants to turn Markdown into a book/handbook/manual, build or deploy an mdBook, ship docs to GitHub Pages, generate a polished/print-quality PDF from mdBook or HTML, or fix PDF problems (broken Thai/CJK glyphs, missing header/footer, blank pages, no page numbers in the TOC). Triggers — "ทำหนังสือ/handbook/คู่มือ", "mdBook", "deploy docs to GitHub Pages", "PDF จากหนังสือ", "print-quality PDF", "หน้าปก/สารบัญ/เลขหน้าใน PDF", "Thai font in PDF broken". The non-obvious part is the headless-Chrome/Puppeteer gotchas that defeat naive attempts — they are all captured here.
---

# Publishing an mdBook → GitHub Pages + a print-quality PDF

A battle-tested pipeline for turning a Markdown book into (1) an mdBook website on GitHub
Pages and (2) a polished PDF. The hard part is the PDF: headless Chrome has many traps.
**Every gotcha below cost real debugging — read them before reinventing.**

Bundled reusable scripts live in `scripts/` next to this file:
- `scripts/print-pdf.js` — Puppeteer renderer (cover / body / measure modes; header/footer; outline)
- `scripts/pdf-toc-pages.py` — reads a measured PDF's outline and injects real page numbers into the TOC

## Architecture

```
markdown (src/) ──mdbook build──▶ static site (book/)  ──▶ GitHub Pages
                                        │
                          print.html ───┴── Puppeteer (CDP) ──▶ PDF
```

- **Site:** `mdbook build` → upload with `actions/upload-pages-artifact` + `deploy-pages`.
- **PDF:** mdBook auto-generates `book/print.html` (whole book on one page). Render THAT with
  Puppeteer (NOT `mdbook`-native, NOT `--print-to-pdf` CLI). See gotchas.
- **Bilingual:** keep two books (`book/` default, `book-en/`), build both, copy the 2nd under
  `/en/`, add a language-switch button via `additional-js`.

---

## The gotchas (and the fixes)

### 1. `chrome --headless --print-to-pdf` CANNOT add headers/footers or page numbers
The CLI flag has no header/footer support. **Use Puppeteer (`puppeteer-core` driving system
Chrome) `page.pdf({displayHeaderFooter, headerTemplate, footerTemplate})`.** Header/footer
templates use the special spans `class="pageNumber"` / `class="totalPages"` / `title` / `date`.
Set an explicit `font-size` (default is ~0) and a font-family in the template.

### 2. Non-Latin fonts (Thai/CJK) render BROKEN in CI PDFs
Two failures combine: the runner has no Thai font, and the Google-Fonts webfont hasn't loaded
when print snapshots. **Fix both:**
- Install system fonts on the runner: `sudo apt-get install -y fonts-thai-tlwg fonts-noto-core fonts-noto-color-emoji` then `sudo fc-cache -f`.
- Wait for fonts before `page.pdf`: `await page.evaluate(() => document.fonts.ready)` (and `waitUntil:'networkidle0'`).
- Put a Thai-capable family in the header/footer template too (e.g. `'Noto Sans Thai','Loma'`).

### 3. Full-bleed A4 cover WITHOUT a leading blank page
- `@page { size: A4; margin: 17mm 15mm }` for body; `@page :first { margin: 0 }` for the cover.
- Cover element: `box-sizing:border-box; min-height:100vh; page-break-after:always; -webkit-print-color-adjust:exact`.
- **Do NOT use a named page (`@page cover{}` + `page:cover`)** — assigning a named page to the
  first element inserts a break before it → a blank page 1, cover on page 2. `@page :first` avoids it.

### 4. `displayHeaderFooter` puts the header/footer on the COVER too
It applies to every page, overriding `@page:first{margin:0}`. **Two-pass + stitch:**
- Pass A (cover): `pageRanges:'1'`, `displayHeaderFooter:false` → clean full-bleed cover (1 page).
- Pass B (body): `displayHeaderFooter:true` → all pages with header/footer.
- Stitch cover page 1 + body pages 2..N with poppler: `pdfseparate body.pdf p-%04d.pdf; rm p-0001.pdf; pdfunite cover.pdf p-*.pdf out.pdf`.
- Because final = cover + body[2..N], the body footer page numbers already equal final page numbers.

### 5. Credit / branding on EVERY page
Put it in the footer template (flex: credit left, `pageNumber / totalPages` right). The cover
(no footer) carries the credit in its own cover meta, so it appears on all pages.

### 6. REAL page numbers in the Table of Contents
You can't know a chapter's page until it's paginated. Loop:
1. **Measure render** = body config + `outline: true` (Puppeteer ≥23.3 → CDP document outline of headings→pages).
2. `scripts/pdf-toc-pages.py` reads the outline with **pypdf**, maps each chapter's H1 (read from
   source in SUMMARY order; exact then shared-prefix fuzzy match) to its page, and fills the
   in-order `<span class="okf-pg"></span>` placeholders in `print.html`.
3. **Final body render** — the TOC now shows numbers. It stays ONE page, so the measured numbers
   stay valid. Fail-safe: if measuring/pypdf/outline is unavailable, placeholders stay empty and
   the TOC renders without numbers (never breaks the build).
TOC markup per entry: `- [Title](link)<span class="okf-leader"></span><span class="okf-pg"></span>`.
Show leaders/numbers in print only (web TOC = plain clickable list); `li:has(.okf-pg:not(:empty)) .okf-leader{...dotted...}`.

### 7. Mermaid diagrams in mdBook WITHOUT the preprocessor
Write diagrams as raw HTML `<pre class="mermaid">flowchart LR; A--&gt;B</pre>` and load vendored
`mermaid.min.js` + an init that calls `mermaid.run({querySelector:'pre.mermaid'})` via `additional-js`.
For the PDF, set a global flag when done (`window.__okfMermaidDone=true`) and
`await page.waitForFunction('window.__okfMermaidDone===true')` before `page.pdf`. Escape `&` as `&amp;`
inside labels; avoid raw `<`.

### 8. Single-file air-gap HTML (e.g. a graph viewer)
Inline vendored libs into one `.html`. Escape `</script` → `<\/script` in the inlined JS AND in any
embedded JSON blob (`blob.replace('</','<\\/')`) or the `<script>` closes early.

### 9. Blank pages = double page-break
mdBook already starts each chapter on a fresh page in print. Adding your OWN
`page-break-before/after` on a wrapper → double break → a blank page. **Detect** by scanning per
page: `pdftotext -f P -l P file.pdf -` and counting body chars after stripping header/footer text;
a page with only header/footer is blank. **Fix** by removing the redundant break.

### 10. Long TOC overflowing to a 2nd (near-empty) page
Tighten print spacing so all entries fit one page: smaller `line-height`/`font-size`, reduced
paragraph + `li` margins inside the TOC wrapper. English entries are taller than Thai — test both.

---

## CI workflow (sketch)

`.github/workflows/book.yml` (Pages permissions: `pages: write`, `id-token: write`):
```yaml
- run: curl -sSL https://github.com/rust-lang/mdBook/releases/download/v0.4.40/mdbook-v0.4.40-x86_64-unknown-linux-gnu.tar.gz | tar -xz -C /usr/local/bin
- run: mdbook build book && mdbook build book-en
- run: |   # assemble: EN under /en, copy any example artifacts
    mkdir -p book/book/en && cp -r book-en/book/* book/book/en/
- run: |   # PDFs (best-effort, never block deploy)
    sudo apt-get update -qq && sudo apt-get install -y -qq fonts-thai-tlwg fonts-noto-core fonts-noto-color-emoji poppler-utils
    export CHROME_PATH="$(command -v google-chrome || command -v chromium-browser)"
    npm i --no-save puppeteer-core@24
    python3 -m pip install --quiet pypdf || python3 -m pip install --quiet --break-system-packages pypdf || true
    gen() { local src=$1 out=$2 title=$3 credit=$4 summ=$5 srcdir=$6 d; d=$(mktemp -d)
      if node scripts/print-pdf.js "$src" "$d/m.pdf" "$title" measure "$credit"; then
        python3 scripts/pdf-toc-pages.py "$d/m.pdf" "$summ" "$src" "$srcdir" || true; fi
      node scripts/print-pdf.js "$src" "$d/cover.pdf" "" cover "" || return 1
      node scripts/print-pdf.js "$src" "$d/body.pdf" "$title" body "$credit" || return 1
      pdfseparate "$d/body.pdf" "$d/p-%04d.pdf"; rm -f "$d/p-0001.pdf"
      pdfunite "$d/cover.pdf" $(ls "$d"/p-*.pdf|sort) "$out"; rm -rf "$d"; }
    gen "$PWD/book/book/print.html" "$PWD/book/book/manual.pdf" "TITLE" "CREDIT" "$PWD/book/src/SUMMARY.md" "$PWD/book/src" || true
  continue-on-error: true
- uses: actions/upload-pages-artifact@v3
  with: { path: book/book }
```
Enable Pages once: `gh api -X POST repos/<owner>/<repo>/pages -f build_type=workflow`.

## CSS recipes (additional-css)
```css
@media print {
  @page { size: A4; margin: 17mm 15mm; }
  @page :first { margin: 0; }                 /* full-bleed cover, no leading blank */
  .cover { box-sizing:border-box; min-height:100vh; page-break-after:always;
           -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  .toc li:has(.okf-pg:not(:empty)) .okf-leader { flex:1; border-bottom:1px dotted #b9a7e6; }
}
.okf-leader,.okf-pg{ display:none; }          /* web TOC stays a plain list */
```

## Verify (always)
```bash
# blank-page scan
for p in $(seq 1 $(pdfinfo f.pdf|awk '/Pages:/{print $2}')); do
  c=$(pdftotext -f $p -l $p f.pdf - | grep -vE 'HEADER|FOOTER|CREDIT' | tr -d '[:space:]' | wc -c)
  [ "$c" -lt 45 ] && echo "page $p near-blank ($c)"; done
# embedded fonts (Thai present?)
pdffonts f.pdf | grep -i thai
# TOC has numbers
pdftotext -f <toc-page> -l <toc-page> -layout f.pdf -
```

## Gotcha quick-reference
| Symptom | Cause | Fix |
|---|---|---|
| No header/footer in PDF | `--print-to-pdf` CLI | Puppeteer `displayHeaderFooter` |
| Thai/CJK glyphs broken | no system font + webfont not loaded | install `fonts-thai-tlwg` + `document.fonts.ready` |
| Blank page 1, cover on 2 | named `@page`+`page:` | `@page :first { margin:0 }` |
| Header/footer on cover | `displayHeaderFooter` is global | two-pass + `pdfunite` stitch |
| No TOC page numbers | can't know pages pre-render | measure `outline:true` → pypdf → inject → re-render |
| Mermaid not in PDF | JS not finished | wait `window.__okfMermaidDone` |
| Blank page mid-doc | double page-break | remove your own break (mdBook breaks chapters) |
| TOC spills 2nd page | entries too tall | tighten print line-height/margins |

#!/usr/bin/env python3
"""Fill TOC page-number placeholders in mdBook's print.html from a measured PDF outline.

Usage: pdf-toc-pages.py <measured.pdf> <SUMMARY.md> <print.html> <src_dir>

Reads the heading outline of the measured PDF (rendered with outline:true), maps each
chapter's H1 (read from source) to its real page number, then fills the in-order
<span class="okf-pg"></span> placeholders in print.html. Fail-safe: on ANY problem it
leaves placeholders empty, so the TOC still renders (just without page numbers).
"""
import os
import re
import sys

try:
    from pypdf import PdfReader
except Exception as e:  # pypdf missing → no-op
    print("pdf-toc-pages: pypdf unavailable (%s) — skipping" % e)
    sys.exit(0)


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()


def main():
    if len(sys.argv) < 5:
        print("usage: pdf-toc-pages.py <pdf> <summary> <print.html> <src_dir>")
        return 0
    pdf, summary, printhtml, srcdir = sys.argv[1:5]

    try:
        reader = PdfReader(pdf)
    except Exception as e:
        print("pdf-toc-pages: cannot read pdf (%s) — skipping" % e)
        return 0

    title2pg = {}
    ordered = []

    def walk(items):
        for it in items:
            if isinstance(it, list):
                walk(it)
                continue
            try:
                pg = reader.get_destination_page_number(it) + 1
            except Exception:
                continue
            t = norm(getattr(it, "title", ""))
            if t:
                ordered.append((t, pg))
                if t not in title2pg:
                    title2pg[t] = pg

    def lookup(h1):
        if not h1:
            return None
        if h1 in title2pg:
            return title2pg[h1]
        key = h1[:14]
        for t, pg in ordered:  # fuzzy: shared long prefix (handles minor heading-text drift)
            if len(key) >= 8 and (t.startswith(key) or h1.startswith(t[:14])):
                return pg
        return None

    try:
        walk(reader.outline)
    except Exception as e:
        print("pdf-toc-pages: no outline (%s)" % e)

    if not title2pg:
        print("pdf-toc-pages: empty outline — leaving TOC without page numbers")
        return 0

    # chapter files in SUMMARY order (exclude the README/toc prefix chapters)
    try:
        summ = open(summary, encoding="utf-8").read()
    except Exception as e:
        print("pdf-toc-pages: cannot read summary (%s)" % e)
        return 0
    files = re.findall(r"\]\((\./[^)]+\.md)\)", summ)

    pages = []
    for rel in files:
        if os.path.basename(rel) in ("README.md", "toc.md"):
            continue
        h1 = None
        try:
            for line in open(os.path.join(srcdir, rel[2:]), encoding="utf-8"):
                m = re.match(r"#\s+(.+?)\s*$", line)
                if m:
                    h1 = norm(m.group(1))
                    break
        except Exception:
            pass
        pages.append(lookup(h1))

    try:
        html = open(printhtml, encoding="utf-8").read()
    except Exception as e:
        print("pdf-toc-pages: cannot read print.html (%s)" % e)
        return 0

    idx = [0]

    def repl(_m):
        i = idx[0]
        idx[0] += 1
        pg = pages[i] if i < len(pages) else None
        return '<span class="okf-pg">%s</span>' % (pg if pg else "")

    html2 = re.sub(r'<span class="okf-pg"></span>', repl, html)
    try:
        open(printhtml, "w", encoding="utf-8").write(html2)
    except Exception as e:
        print("pdf-toc-pages: cannot write print.html (%s)" % e)
        return 0

    filled = sum(1 for p in pages if p)
    print("pdf-toc-pages: filled %d/%d TOC page numbers" % (filled, len(pages)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

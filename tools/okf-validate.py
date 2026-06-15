#!/usr/bin/env python3
"""okf-validate.py — OKF v0.1 conformance checker (stdlib only).

Checks a bundle directory (default: ../wiki):

ERRORS (fail conformance):
  1. Every non-reserved .md has a YAML frontmatter block (--- ... ---).
  2. Every frontmatter block has a non-empty `type:` field.
  3. index.md must NOT carry frontmatter, EXCEPT the bundle-root index.md
     which may declare only `okf_version` (spec §11).

WARNINGS (allowed, but flagged):
  - Links beginning with `/` (bundle-root-absolute). The spec §5.1 *recommends*
    them, but Google's reference enrichment agent forbids them because they
    break GitHub rendering. We follow the reference impl: prefer file-relative.
  - log.md date headings not in ISO `YYYY-MM-DD` form (spec §7).

INFO (not failures — spec §5.3 says broken links are valid):
  - Relative/absolute links whose target file is missing.

Usage: python3 tools/okf-validate.py [wiki_dir]
Exit 0 if conformant (errors == 0), else 1.
"""
import os
import re
import sys

RESERVED = {"index.md", "log.md"}
LINK_RE = re.compile(r"(?<!\!)\[[^\]]+\]\(([^)]+)\)")
DATE_HDR_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def split_frontmatter(text):
    """Return (has_block, block_text, type_value_or_None)."""
    if not text.startswith("---"):
        return False, "", None
    end = text.find("\n---", 3)
    if end == -1:
        return False, "", None
    block = text[3:end]
    type_val = None
    for line in block.splitlines():
        m = re.match(r"\s*type\s*:\s*(.+?)\s*$", line)
        if m:
            type_val = m.group(1).strip().strip("'\"")
            break
    return True, block, (type_val or None)


def main():
    wiki = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "wiki")
    wiki = os.path.abspath(wiki)
    if not os.path.isdir(wiki):
        print(f"✗ bundle dir not found: {wiki}")
        return 1

    errors, warns, infos, concepts = [], [], [], 0
    for root, _, files in os.walk(wiki):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, wiki).replace(os.sep, "/")
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            has_fm, block, type_val = split_frontmatter(text)

            if fn == "log.md":                      # reserved: check date headings
                for hdr in DATE_HDR_RE.findall(text):
                    if not ISO_DATE_RE.match(hdr):
                        warns.append(f"{rel}: log heading '## {hdr}' is not ISO YYYY-MM-DD")
                continue
            if fn == "index.md":                    # reserved: frontmatter rules
                is_root = (rel == "index.md")
                if has_fm:
                    keys = [k.split(":")[0].strip() for k in block.splitlines()
                            if re.match(r"\s*[A-Za-z0-9_]+\s*:", k)]
                    extra = [k for k in keys if k != "okf_version"]
                    if not is_root:
                        errors.append(f"{rel}: index.md must not have frontmatter")
                    elif extra:
                        errors.append(f"{rel}: root index.md frontmatter may only contain okf_version (found: {', '.join(extra)})")
                continue

            concepts += 1
            if not has_fm:
                errors.append(f"{rel}: missing YAML frontmatter block")
            elif not type_val:
                errors.append(f"{rel}: frontmatter has no non-empty `type` field")

            for target in LINK_RE.findall(text):
                t = target.split("#")[0]
                if not t or t.startswith(("http://", "https://", "mailto:")) or not t.endswith(".md"):
                    continue
                if t.startswith("/"):
                    warns.append(f"{rel}: absolute link '{t}' breaks GitHub rendering — use a file-relative path")
                    tgt = os.path.normpath(os.path.join(wiki, t[1:]))
                else:
                    tgt = os.path.normpath(os.path.join(root, t))
                if not os.path.exists(tgt):
                    infos.append(f"{rel}: broken link -> {target} (allowed by spec §5.3)")

    print(f"OKF bundle: {wiki}")
    print(f"Concept files checked: {concepts}")
    for i in infos:
        print(f"  · info: {i}")
    for w in warns:
        print(f"  ! warn: {w}")
    if errors:
        print(f"\n✗ NON-CONFORMANT ({len(errors)} error(s)):")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print(f"\n✓ CONFORMANT with OKF v0.1  ({len(warns)} warning(s), {len(infos)} info)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

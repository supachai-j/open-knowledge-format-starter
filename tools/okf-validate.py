#!/usr/bin/env python3
"""okf-validate.py — minimal OKF v0.1 conformance checker (stdlib only).

Checks, for a bundle directory (default: ../wiki):
  1. Every non-reserved .md file has a YAML frontmatter block (--- ... ---).
  2. Every frontmatter block has a non-empty `type:` field.
  3. Reserved files index.md / log.md are NOT used as concept docs.
  4. Reports relative Markdown links whose target file is missing (broken links
     are ALLOWED by the spec — reported as info, not failures).

Usage:
  python3 tools/okf-validate.py [wiki_dir]

Exit code 0 if conformant, 1 otherwise. This is a lightweight gate, not a full
YAML parser — for strict parsing, run under `uv` with PyYAML.
"""
import os
import re
import sys

RESERVED = {"index.md", "log.md"}
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_frontmatter(text):
    """Return (has_block, type_value_or_None). YAML-lite: good enough for v0.1."""
    if not text.startswith("---"):
        return False, None
    end = text.find("\n---", 3)
    if end == -1:
        return False, None
    block = text[3:end]
    type_val = None
    for line in block.splitlines():
        m = re.match(r"\s*type\s*:\s*(.+?)\s*$", line)
        if m:
            type_val = m.group(1).strip().strip("'\"")
            break
    return True, (type_val or None)


def main():
    wiki = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "wiki")
    wiki = os.path.abspath(wiki)
    if not os.path.isdir(wiki):
        print(f"✗ bundle dir not found: {wiki}")
        return 1

    errors, infos, concepts = [], [], 0
    for root, _, files in os.walk(wiki):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, wiki)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()

            if fn in RESERVED:
                continue  # reserved files are exempt from the frontmatter rule

            concepts += 1
            has_fm, type_val = parse_frontmatter(text)
            if not has_fm:
                errors.append(f"{rel}: missing YAML frontmatter block")
            elif not type_val:
                errors.append(f"{rel}: frontmatter has no non-empty `type` field")

            for target in LINK_RE.findall(text):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                tgt = os.path.normpath(os.path.join(root, target.split("#")[0]))
                if not os.path.exists(tgt):
                    infos.append(f"{rel}: broken link -> {target} (allowed by spec)")

    print(f"OKF bundle: {wiki}")
    print(f"Concept files checked: {concepts}")
    for i in infos:
        print(f"  · {i}")
    if errors:
        print(f"\n✗ NON-CONFORMANT ({len(errors)} error(s)):")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print("\n✓ CONFORMANT with OKF v0.1 (frontmatter + type checks passed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

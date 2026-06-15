# Contributing

Thanks for helping improve this OKF starter! Contributions fall into two buckets.

## 1. Improving the starter itself
(schema, skill, tooling, docs)

1. Fork and branch: `git checkout -b feat/<short-name>`.
2. Make your change. If you touch the bundle, run `python3 tools/okf-validate.py` and keep it green.
3. Keep `AGENTS.md`, `.claude/skills/okf/SKILL.md`, and `docs/` consistent with each other — they
   describe the same rules and must not drift apart.
4. Open a PR describing **what** changed and **why**.

## 2. Contributing knowledge to a wiki built on this starter
(concepts under `wiki/`)

1. Add sources to `raw/` (or reference them); never edit existing `raw/` files.
2. Follow [docs/GUIDELINES.md](docs/GUIDELINES.md) for concept style and frontmatter.
3. Every new/changed concept must:
   - have a non-empty `type` from the controlled vocabulary in `AGENTS.md`,
   - update the relevant `index.md`,
   - append an entry to `wiki/log.md`,
   - pass `python3 tools/okf-validate.py`.

## Conformance

This project targets **OKF v0.1**. The normative spec requires only a non-empty `type` field per
concept; everything else here is recommended best practice. PRs that break conformance won't be merged.

## Code of conduct

Be kind, be precise, cite your sources.

# Tool Reference (CLI)

All tools are pure Python stdlib, located in `tools/` (or `scripts/` if installed as a skill).

## okf-init.py — Create a New Bundle
```bash
python3 tools/okf-init.py [target_dir] [--force] [--date YYYY-MM-DD]
```
Creates `AGENTS.md` + `wiki/{index.md, log.md, getting-started.md}` + `raw/` · Does not overwrite a non-empty `wiki/` unless `--force`

## okf-validate.py — Check Conformance
```bash
python3 tools/okf-validate.py [wiki_dir]
```
Exits 0 if conformant, 1 if not · error = missing frontmatter/`type`, index.md rule violation · warn = `/`-prefixed links, non-ISO log dates · info = broken link

## okf-viz.py — Generate Graph Viewer
```bash
python3 tools/okf-viz.py [bundle] [-o out.html] [--name "Name"] [--cdn]
```
Produces a single self-contained `viz.html` (embeds Cytoscape + marked) · `--cdn` = load libraries from CDN instead of embedding

## okf-index.py — BM25 Search Index
```bash
python3 tools/okf-index.py build [bundle] [-o index.json]
python3 tools/okf-index.py query "question" [-k 8] [--type Metric]
```

## okf-embed.py — Embeddings (Ollama)
```bash
python3 tools/okf-embed.py build [bundle]
python3 tools/okf-embed.py query "question" [-k 8]
```
env: `OKF_OLLAMA_URL` (default `http://localhost:11434`), `OKF_EMBED_MODEL` (default `nomic-embed-text`)

## okf-search.py — Hybrid Search (BM25 + semantic, RRF)
```bash
python3 tools/okf-search.py "question" [--bundle ./wiki] [-k 8] [--type ...] [--bm25-only]
```
Automatically falls back to BM25 if embeddings are absent or Ollama is not running.

## okf-lease.py — Lease/Lock Concurrency
```bash
python3 tools/okf-lease.py acquire <concept> --owner <id> [--ttl 300]
python3 tools/okf-lease.py renew   <concept> --owner <id> --token <tok> [--ttl 300]
python3 tools/okf-lease.py release <concept> --owner <id> --token <tok>
python3 tools/okf-lease.py list
python3 tools/okf-lease.py break   <concept>      # admin force-release
```
env: `OKF_LEASE_DIR` (lease storage location), `OKF_LEASE_TTL` (default 300)

## okf-selftest.sh — exercise the whole toolchain
```bash
bash tools/okf-selftest.sh
```
Runs 10 end-to-end checks (init → validate both a clean bundle and a deliberately-broken one →
index → search → air-gap viz → lease → embed/hybrid if Ollama is up) · exits non-zero on any
failure · suitable for CI.

## install.sh — Install Skill
```bash
./install.sh                 # global  → ~/.claude/skills/okf
./install.sh --project       # project → ./.claude/skills/okf
./install.sh --dir <path>    # custom
./install.sh --uninstall
```

## server/okf_mcp_server.py — MCP Access Layer
```bash
python3 server/okf_mcp_server.py            # stdio
OKF_MCP_TRANSPORT=streamable-http OKF_MCP_PORT=8765 python3 server/okf_mcp_server.py
```
Key env vars: `OKF_REPO_DIR`, `OKF_BUNDLE`, `OKF_BASE_BRANCH`, `OKF_WRITE_MODE` (`pr`|`lease`),
`OKF_READONLY`, `OKF_GITEA_API/TOKEN/OWNER/REPO`, `OKF_AGENT_ID`

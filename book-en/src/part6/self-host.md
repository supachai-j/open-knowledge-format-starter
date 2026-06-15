# Self-host Setup

`deploy/docker-compose.yml` brings up the full internal stack on a single VM — no external exposure, works even air-gapped.

## Stack Overview

```
gitea   →  source of truth (git server)
okf-mcp →  access layer that agents connect to (built from deploy/Dockerfile)
proxy   →  Caddy: TLS + auth (token/OIDC/mTLS) in front of MCP
```

## Steps

```bash
cd deploy
cp .env.example .env        # set OKF_GIT_REMOTE, token, etc.
docker compose up -d
```

Required `.env` values:

```bash
OKF_GIT_REMOTE=http://gitea:3000/okf/knowledge.git   # repo that MCP will clone/pull
OKF_GITEA_API=http://gitea:3000/api/v1               # for opening PRs automatically from propose_change
OKF_GITEA_TOKEN=<token>
OKF_GITEA_OWNER=okf
OKF_GITEA_REPO=knowledge
OKF_TOKEN=<long-random>                              # token agents must send to the proxy
OKF_READONLY=0                                       # 1 = read-only replica
```

## Connecting an Agent to the MCP Endpoint

In Claude Code (or any MCP client), point to the internal URL:

```jsonc
{ "mcpServers": { "okf": {
    "transport": "http",
    "url": "https://okf.internal.example/mcp",
    "headers": { "Authorization": "Bearer ${OKF_TOKEN}" }
} } }
```

## Local / Dev Mode (no network required)

Test the server without standing up the full stack:

```bash
python3 server/okf_mcp_server.py                       # stdio transport
# or HTTP:
OKF_MCP_TRANSPORT=streamable-http OKF_MCP_PORT=8765 \
  python3 server/okf_mcp_server.py
```

## Tools the Server Exposes to Agents

| Tool | What it does |
|------|--------------|
| `okf_search(query, k, type)` | Hybrid search (BM25 + semantic if available) |
| `okf_get_concept(id)` | Returns the frontmatter + body of a concept |
| `okf_list_concepts(prefix)` | Lists id/type/description |
| `okf_read_index(path)` | Reads `index.md` (progressive disclosure) |
| `okf_propose_change(...)` | Writes via branch + PR (PR mode) |
| `okf_acquire_lease / renew / release / list_leases` | Acquires write rights (lease mode) |
| `okf_commit_concept(..., token)` | Writes directly while holding a lease (lease mode only) |

## CI Conformance Gate

Set branch protection on `main` to require this check — non-conformant bundles cannot be merged.

- **Gitea Actions:** `.gitea/workflows/conformance.yml`
- **GitLab CI:** `ci/.gitlab-ci.yml`

Both run `okf-validate.py` (blocks on failure) + rebuild the index + regenerate `viz.html`.

## Basic Security

- The MCP endpoint is behind a reverse proxy that handles TLS + auth (details in the [Security and Governance](./security.md) chapter)
- `raw/` is excluded from the bundle (`.gitignore` prevents accidentally committing private data)
- Air-gap: `viz.html` bundles its libraries inline; semantic search uses on-premises Ollama — nothing leaves the network

Next: choose a write model → [Write Models: PR-gated and Lease](./write-models.md)

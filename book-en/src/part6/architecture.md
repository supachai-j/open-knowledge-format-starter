# Architecture Overview (Enterprise)

When a knowledge base must be shared **across sessions and teams at the enterprise level** on-prem
(internal network, works even air-gapped), the core idea fits in one sentence:

> **Git is the source of truth · the internal MCP server is the central access layer**
>
> Every session and every agent — regardless of framework or model — connects to **the same single internal MCP endpoint**.
> Git history *is* "cross-session memory" by nature · reads are instant · writes go through a gate (PR or lease)

## Diagram

<pre class="mermaid">
flowchart TB
  subgraph net["Internal network (on-prem / air-gap)"]
    MCP["OKF MCP server<br/>search · get · propose / commit"]
    GIT["Git server (Gitea/GitLab)<br/>= OKF repo · source of truth"]
    IDX["Search index<br/>BM25 (+ semantic)"]
    CI["CI runner<br/>okf-validate + viz"]
    MCP -->|"pull / webhook"| GIT
    MCP --> IDX
    GIT -->|"PR/MR triggers"| CI
  end
  A1["Agent team A"] -->|"MCP: HTTP/SSE + token/mTLS"| MCP
  A2["Agent team B"] --> MCP
  CR["CI / cron"] --> MCP
</pre>

## Components

| # | Component | Self-host option | Role |
|---|-----------|------------------|------|
| 1 | **Git server** | Gitea / GitLab CE | Versioned source of truth (one repo per team, or monorepo + CODEOWNERS) |
| 2 | **OKF MCP server** | `server/okf_mcp_server.py` | Access layer that every agent connects to — read/search/propose; stdio + HTTP/SSE |
| 3 | **Search index** | `tools/okf-index.py` (+ embed) | Fast search once the wiki grows beyond ~150 pages |
| 4 | **CI gate** | Gitea Actions / GitLab CI | Blocks non-conformant merges + regenerates viz |
| 5 | **Reverse proxy** | Caddy / Traefik / nginx | TLS + auth (token / OIDC / mTLS) in front of MCP |

## Read Path (normal case — fast, no lock)

1. Agent calls `okf_search("how is WAU defined")` → receives ranked Concept IDs
2. `okf_get_concept("metrics/weekly-active-users")` → frontmatter + body loaded into context
3. `okf_read_index()` when progressive disclosure exploration is needed

Concurrent reads are unlimited with no contention.

## Write Path

Two models to choose from (next chapter):

- **PR-gated (default):** write via branch + PR → CI checks → human/curator merges — safe, with audit/review
- **Lease/lock:** for heavy-write teams — per-concept lease prevents collision, writes directly to a shared branch

## Meaning of "Cross-session / Cross-team"

- **Cross-session:** no per-session state — a new session `git pull`s everything a previous session wrote; the wiki compounds automatically
- **Cross-team:** *monorepo* + `CODEOWNERS` per subtree **or** *federated bundles* (one repo per domain,
  MCP server mounts multiple bundles and namespaces them by bundle name, e.g. `sales:tables/orders`)

Next: deploy it → [Self-host Setup](./self-host.md)

# Security and Governance

A self-hosted internal system must control who can read/write what, and must be auditable after the fact. OKF gets much of its governance for free from git.

## Two-Layer Access Control

### Git Layer
- Org/team membership on Gitea/GitLab
- **Branch protection** on `main` — enforces passing CI + review before merge

### MCP Layer
Place the HTTP transport behind a reverse proxy with:

- **mTLS** (service-to-service) **or** **OIDC/SSO** (for humans) + a bearer token per agent identity
- Map identity → role:

| role | allowed |
|------|---------|
| `reader` | search / get / list only |
| `proposer` | + `okf_propose_change` (branch/PR only, cannot touch `main`) |
| `curator` | may merge (via git server, not via MCP) |

Set `OKF_READONLY=1` to run an MCP replica in read-only mode.

## Caddy (proxy) Example — Bearer Token

```
okf.internal.example {
    # internal CA / self-signed for air-gap:
    #   tls /etc/caddy/okf.crt /etc/caddy/okf.key
    # or mTLS:
    #   tls { client_auth { mode require_and_verify trusted_ca_cert_file /etc/caddy/internal-ca.crt } }

    @noauth not header Authorization "Bearer {$OKF_TOKEN}"
    respond @noauth "Unauthorized" 401
    reverse_proxy okf-mcp:8765
}
```

For SSO, replace the bearer check with `forward_auth` to an OIDC proxy (e.g. oauth2-proxy) and map identity → role.

## Secrets and PII

- **`raw/` is not included in the bundle** and is already in `.gitignore` — prevents accidentally pushing private or large data
- **Do not put credentials in concepts** — concepts are knowledge, not a secrets store
- PR review helps catch sensitive data before it reaches `main` (another reason PR-gated writes are good in organizations)

## Air-Gap (Closed Networks)

- `viz.html` embeds its libraries (Cytoscape + marked) inline — it does not fetch from a CDN at render time
- Semantic search uses a self-hosted embedding model (Ollama) — nothing leaves the network
- All tools are Python stdlib only (except the MCP server, which uses the `mcp` package — installable from an internal mirror)

## Audit & Rollback (from git)

| Task | Command |
|------|---------|
| Who changed WAU? | `git log --follow wiki/metrics/weekly-active-users.md` |
| Revert incorrect knowledge | `git revert <sha>` → PR → merge |
| Change timeline | Read `wiki/log.md` or `git log` |

## Governance for Free

Because the wiki is files in git, every change has a **diff, blame, review, history, and rollback** — just like normal software development. Knowledge maintenance becomes an engineering workflow the team already knows.

End of the organizational section. See the appendix for reference → [Tool Reference (CLI)](../appendix/tools.md)

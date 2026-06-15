# Write Models: PR-gated and Lease

When multiple agents write knowledge concurrently, you must choose how to manage concurrency. The starter supports two models
(plus a third as a concept). Select with the `OKF_WRITE_MODE` env var.

## Model 1 — PR-gated (default)

`okf_propose_change(...)` **does not write to `main`** — instead it:

1. Creates branch `okf/<concept>-<id>` from `main`
2. Writes the file, commits, and pushes to the internal git server
3. Opens a PR/MR via the git server API and returns the URL
4. CI runs `okf-validate.py` (+ regenerates viz) → a human/curator reviews and merges

<pre class="mermaid">
flowchart LR
  AG["Agent"] -->|propose_change| BR["branch + commit"]
  BR --> PR["Pull Request"]
  PR --> CIv["CI: okf-validate"]
  CIv --> RV["review (human/curator)"]
  RV -->|merge| MAIN["main"]
  MAIN -->|webhook| RE["MCP pull + reindex"]
</pre>

Full enterprise properties: **audit trail** (git log), **review/diff**, **rollback** (git revert),
**no write conflicts** (merges applied one at a time in order), **quality gate** (CI + review)

Once merged to `main` → webhook → MCP server `pull` → reindex → all sessions see the update

> Suitable when **reviewing every change matters more than speed**

## Model 2 — Lease/lock (direct write)

Enable with `OKF_WRITE_MODE=lease` for heavy-write teams. Uses a **lease (TTL-based write reservation)** to prevent two agents
from editing the same concept simultaneously.

```bash
# per-agent flow:
okf_acquire_lease("tables/orders", ttl_seconds=300)   # → {token, expires_at}
# ... make edits ...
okf_commit_concept("tables/orders", frontmatter, body, token=...)   # server checks lease then write+commit+push
okf_release_lease("tables/orders", token=...)         # release when done
```

<pre class="mermaid">
flowchart LR
  ACQ["acquire_lease<br/>(TTL)"] --> ED["edit concept"]
  ED --> CM["commit_concept<br/>(verify token)"]
  CM --> PUSH["pull --rebase + push"]
  PUSH --> REL["release_lease"]
  OT["another agent requests the same concept"] -.->|locked| ACQ
</pre>

Another agent requesting the same concept receives `{error:"locked", held_by}` → it works on something else instead.
Concurrency safety: the lease prevents duplicate concepts + `git pull --rebase` before push handles
commits to different files (auto-merge).

Lease properties:

- **Advisory + self-expiring TTL** — a crashed agent does not leave a concept permanently locked (an expired lease can be "stolen")
- **Token-verified** — only the lease holder can commit/renew/release
- **Single-authority** — one MCP server issues all leases using atomic file creation (`O_CREAT|O_EXCL`); git is serialized with a lock

CLI for ops: `python3 tools/okf-lease.py list` · `... break <concept>` (admin force-release)

> Suitable when **write throughput matters more than reviewing every change**

## Model 3 — Append-only proposals + curator (concept)

Agents drop proposals into `inbox/`; a **single curator agent** collects them, resolves conflicts, then merges into the wiki
— the highest quality gate, consistent with the supervised-ingest philosophy (not yet implemented in the starter)

## Comparison

| Model | Speed | Review | Conflict | Best for |
|-------|-------|--------|----------|----------|
| **PR-gated** | Moderate | Every change | None (sequential merge) | Governance, general teams |
| **Lease/lock** | Fast | Lightweight | Prevented by lease | Heavy-write teams |
| **Curator** | Slow | Maximum | Curator handles it | Quality above all else |

> 💡 **Both modes can run against the same repo** — a heavy-write team uses the server in lease mode; everyone else uses PR-gated, all pointing to the same git remote

Next: search as the wiki scales → [Search at Scale and Semantic Search](./scaling-search.md)

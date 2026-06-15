# Linking as a Knowledge Graph

Concepts connect to one another via **standard Markdown links**, turning the directory into a **graph of relationships**
that is richer than the parent–child structure of folders alone.

## Use File-Relative Links Only

```markdown
See the [customers](../tables/customers.md) table for the key used in the join.
```

> ⚠️ **Do not begin a link with `/`** — this is an important and subtle rule.
>
> OKF spec §5.1 *recommends* absolute-style links (`/tables/customers.md`), claiming they are stable when files move.
> **However, Google's actual enrichment agent forbids them** because `/`-prefixed links **break GitHub rendering**,
> and every real Google bundle uses **relative** links throughout.
>
> **We follow the real implementation: relative links only** (`okf-validate.py` will warn if it finds a `/`-prefixed link).

## Links Are Untyped

A link from concept A → B simply "asserts that a relationship exists", but the **type of that relationship**
(parent–child, reference, joins-with, depends-on) lives in the **surrounding prose, not in the link itself**.

```markdown
Joins with [customers](../tables/customers.md) via `customer_id` (many orders → one customer)
           └─ untyped link          └─ relationship type is expressed in this sentence
```

Consumers that build graph views treat every link as a directed, untyped edge.

## Broken Links Are Permitted

A link pointing to a concept that **does not yet exist** is not an error — it represents **knowledge not yet written**
(a placeholder / gap to be filled later). Consumers **must tolerate broken links**.

## Rules for Good Linking

- ✅ Use relative paths only (`../tables/orders.md`, `customers.md`)
- ✅ Link only to concepts that actually exist (or intentionally leave placeholders)
- ❌ Do not over-link — one link per mention per section is enough
- ❌ Do not link from **headings**, inside **code blocks**, or in schema field-name lists
- ❌ Do not link a file to itself

## Example: A Small Graph

```text
references/joins/orders__customers.md
   ├──► tables/orders.md
   └──► tables/customers.md

metrics/weekly-active-users.md ──► tables/orders.md
playbooks/incident-response.md ──► metrics/weekly-active-users.md
```

When you open `viz.html` you will see this graph interactively, including **"Cited by"** (backlinks — which concepts link to this one).

Next, see the two special files that help navigate the graph → [Reserved files: index.md and log.md](./reserved-files.md)

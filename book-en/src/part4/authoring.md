# Adding and Editing Concepts

## Start from the Template

Use `tools/concept-template.md` as your starting point:

```markdown
---
type: Concept            # required — choose from the controlled vocabulary in AGENTS.md
title: <human-readable name>
description: <one-line summary — used to decide whether an agent will load this file>
resource: <URI of the real-world thing, or delete this line if purely abstract>
tags: [<tag1>, <tag2>]
timestamp: 2026-06-15T00:00:00Z   # ISO 8601 UTC
---

# <Title>
Use structure: headings, short bullets, tables — rather than long paragraphs.

# Related
Link to other concepts using relative paths, e.g. [orders](../tables/orders.md).
The relationship type belongs in this sentence, not in the link text itself.

# Citations
Cite the sources in raw/ that were used to synthesize this concept.
```

## Steps to Add / Edit a Concept

1. Copy the template → name the file (kebab-case, stable).
2. Set `type` correctly (from the controlled vocabulary).
3. Write the body using structure + relative links.
4. Update `tags` + `timestamp`.
5. Update the `index.md` of that directory.
6. Add an entry to `wiki/log.md`.
7. Run `okf-validate.py`.

## Conventional Section Order

Use when appropriate, in this order (derived from Google's enrichment prompt):

```markdown
# Overview                  ← 1–3 paragraph intro: what it is, how it's used
# Schema                    ← column/field summary (nested RECORDs as sub-sections/tables)
# Common query patterns     ← 1–3 SQL snippets (```sql code blocks)
# Joins                     ← which concepts this joins to, via which keys
# Citations                 ← references (format: [1] [Title](url))
```

## Example Reference Concept (join)

File `wiki/references/joins/orders__customers.md`:

````markdown
---
type: Reference
title: Orders → Customers join
description: How to join the orders table to customers via customer_id
tags: [join, sales]
timestamp: 2026-06-15T00:00:00Z
---

Join [orders](../../tables/orders.md) with [customers](../../tables/customers.md)
via `customer_id` (many orders → one customer).

# Common query patterns
```sql
SELECT c.email, COUNT(*) AS orders, SUM(o.total) AS ltv
FROM orders o JOIN customers c USING (customer_id)
GROUP BY c.email;
```
````

## After Editing — Definition of Done

- [ ] Concept has a non-empty `type` and a sharp `description`
- [ ] `timestamp` updated to current
- [ ] Relevant `index.md` updated
- [ ] Entry added to `log.md` under today's date
- [ ] `python3 tools/okf-validate.py ./wiki` passes

Next: validate and visualize the wiki → [Validate and Visualize](./validate-viz.md)

---
type: Reference
title: Orders → Customers join
description: How to join the orders table to the customers table on customer_id.
tags: [join, sales, customers]
timestamp: 2026-06-15T00:00:00Z
---

Join [orders](../../tables/orders.md) to [customers](../../tables/customers.md)
on `customer_id` (many orders → one customer).

# Common query patterns

```sql
SELECT c.email, COUNT(*) AS order_count, SUM(o.total) AS lifetime_value
FROM orders o
JOIN customers c USING (customer_id)
GROUP BY c.email;
```

# Citations

[1] Example reference concept created during bundle scaffolding. Replace with a real source from `raw/`.

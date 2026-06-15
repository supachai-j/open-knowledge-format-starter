---
type: Metric
title: Weekly Active Users (WAU)
description: Count of distinct customers with >=1 order in a rolling 7-day window.
tags: [growth, engagement, metric]
timestamp: 2026-06-15T00:00:00Z
---

# Definition

**WAU** = number of distinct `customer_id` values with at least one order in the
rolling 7-day window ending on the reporting date.

# Calculation

```sql
SELECT COUNT(DISTINCT customer_id) AS wau
FROM orders
WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY);
```

# Source tables

- Derived from [orders](../tables/orders.md); customer attributes from [customers](../tables/customers.md).

# Citations

- Example concept created during bundle scaffolding. Replace with a real source from `raw/`.

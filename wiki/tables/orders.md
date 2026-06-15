---
type: BigQuery Table
title: Orders
description: Primary table for customer purchase history; one row per order.
resource: https://console.cloud.google.com/bigquery?t=orders
tags: [sales, revenue, orders]
timestamp: 2026-06-15T00:00:00Z
---

# Schema

| Column | Type | Description |
| :--- | :--- | :--- |
| order_id | STRING | Unique order identifier (primary key). |
| customer_id | STRING | FK to [customers](customers.md). |
| total | FLOAT | Transaction value in USD. |
| created_at | TIMESTAMP | Order creation time (UTC). |

# Joins

- Joins to [customers](customers.md) on `customer_id` (many orders → one customer).

# Citations

- Example concept created during bundle scaffolding. Replace with a real source from `raw/`.

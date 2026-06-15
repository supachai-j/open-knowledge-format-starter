---
type: BigQuery Table
title: Customers
description: Customer master record; one row per customer, referenced by orders.
resource: https://console.cloud.google.com/bigquery?t=customers
tags: [customers, crm]
timestamp: 2026-06-15T00:00:00Z
---

# Schema

| Column | Type | Description |
| :--- | :--- | :--- |
| customer_id | STRING | Unique customer identifier (primary key). |
| email | STRING | Primary contact email. |
| signup_at | TIMESTAMP | Account creation time (UTC). |

# Joins

- Referenced by [orders](orders.md) via `customer_id` (one customer → many orders).
- Feeds the [weekly-active-users](../metrics/weekly-active-users.md) metric.

# Citations

- Example concept created during bundle scaffolding. Replace with a real source from `raw/`.

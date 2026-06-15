---
okf_version: "0.1"
---
# Subdirectories

* [tables](tables/index.md) - BigQuery tables and their schemas/joins.
* [metrics](metrics/index.md) - Business metric definitions.
* [playbooks](playbooks/index.md) - Operational runbooks.
* [references](references/index.md) - Curated reference concepts (joins, derived definitions).

# Concepts

* [tables/orders](tables/orders.md) - Primary customer purchase-history table.
* [tables/customers](tables/customers.md) - Customer master record (one row per customer).
* [metrics/weekly-active-users](metrics/weekly-active-users.md) - Distinct customers with ≥1 order in a rolling 7-day window.
* [playbooks/incident-response](playbooks/incident-response.md) - Sev1/Sev2 incident response runbook.
* [references/joins/orders__customers](references/joins/orders__customers.md) - How to join orders to customers.

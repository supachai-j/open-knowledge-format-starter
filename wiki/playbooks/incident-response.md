---
type: Playbook
title: Incident Response (Sev1/Sev2)
description: Step-by-step runbook for declaring and resolving a Sev1/Sev2 incident.
tags: [oncall, incident, ops]
timestamp: 2026-06-15T00:00:00Z
---

# When to use

Trigger when a customer-facing outage or data-integrity issue is suspected.

# Steps

1. **Declare** — open an incident channel; assign an Incident Commander (IC).
2. **Assess severity** — Sev1 = full outage / data loss; Sev2 = degraded / partial.
3. **Mitigate** — stop the bleeding before root-causing (roll back, failover, feature-flag off).
4. **Communicate** — post status updates on a fixed cadence (Sev1: every 15 min).
5. **Resolve & verify** — confirm recovery against [weekly-active-users](../metrics/weekly-active-users.md) and key dashboards.
6. **Post-mortem** — blameless review within 48h; file follow-up actions.

# Related

- Data sources to check: [orders](../tables/orders.md), [customers](../tables/customers.md).

# Citations

- Example concept created during bundle scaffolding. Replace with a real source from `raw/`.

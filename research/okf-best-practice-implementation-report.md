# Open Knowledge Format (OKF): Best-Practice Implementation Guide

### 1. Foundations: The Logic of OKF

**Definition & Origin**
The Open Knowledge Format (OKF) v0.1 is an open, vendor-neutral specification released on June 12, 2026, by Google Cloud. Authored by Sam McVeety (Tech Lead, Data Analytics) and Amir Hormati (Tech Lead, BigQuery), the format formalizes the "LLM Wiki" pattern. OKF represents knowledge as a directory of Markdown files with YAML frontmatter, ensuring that organizational intelligence is portable, version-controlled, and human-readable without proprietary SDKs.

**The Problem vs. Traditional RAG**
Traditional Retrieval-Augmented Generation (RAG) often suffers from "context fragmentation." Knowledge is locked in silos—proprietary metadata APIs, stagnant wikis, or the private notes of senior engineers—forcing agent builders to solve the same context-assembly problem repeatedly. OKF addresses this by acting as a "format, not a platform." 

It capitalizes on the insight famously articulated by AI researcher Andrej Karpathy: **"LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass."** OKF turns the bookkeeping tasks that humans find tedious into a machine-executable workflow. Upon the format's release, Google updated its **Cloud Knowledge Catalog** to natively ingest OKF bundles, providing an immediate enterprise-grade pathway for sovereign data integration.

**Strategic Advantage**

| Dimension | Platform-Centric RAG | Format-First OKF |
| :--- | :--- | :--- |
| **Vendor Lock-in** | High (Proprietary APIs/Vector DBs) | None (Plain Markdown/Git) |
| **Human Readability** | Low (Binary/UI-only) | High (Standard Text Editors) |
| **Data Sovereignty** | Dependent on platform registry | Sovereign (RFC 4151 tag: URIs) |
| **Version Control** | Complex (Database snapshots) | Native (Git Diffs/PRs/Branches) |
| **Tooling** | Requires Specific SDKs | Tool-Agnostic (CLI, Python, Node) |

---

### 2. OKF Document Anatomy: Concepts & Metadata

**The "Concept" Unit**
In OKF, a "Concept" is a single unit of knowledge (e.g., a BigQuery table, a business metric, or a playbook). Each concept is represented by exactly one Markdown file. The unique identifier (**Concept ID**) is the relative file path within the bundle. For example, `tables/orders.md` carries the ID `tables/orders`. This approach links identity directly to the filesystem, supporting **Sovereign Identity** without central registries.

**YAML Frontmatter Schema**
Structured metadata is contained in a YAML block delimited by `---`.

*   **Required Fields:**
    *   `type`: A short string identifying the kind of concept (e.g., `Metric`, `Playbook`). **This is the only mandatory field for v0.1 conformance.**
*   **Recommended Fields:**
    *   `title`: A human-readable name.
    *   `description`: A one-line summary used by agents to determine relevance.
    *   `resource`: A URI identifying the underlying asset (e.g., a URL to a Google Cloud console page).
    *   `tags`: A YAML array of strings for categorization.
    *   `timestamp`: The ISO 8601 datetime of the last meaningful change.

**Formatting Example (`tables/orders.md`):**
```markdown
---
type: BigQuery Table
title: Orders
description: Primary table for customer purchase history.
resource: https://console.cloud.google.com/bigquery?t=orders
tags: [sales, revenue]
timestamp: 2026-06-12T14:30:00Z
---

# Schema
| Column | Type | Description |
| :--- | :--- | :--- |
| order_id | STRING | Unique ID |
| total | FLOAT | Transaction value |

# Joins
Linked to `tables/customers` via `customer_id`.
```

---

### 3. Knowledge-Graph Linking & Hierarchy

**Linking Mechanics**
Relationships are asserted using standard Markdown links or `[[wikilinks]]`. While links are "untyped" at the structural level, they transform the directory into a directed graph of relationships richer than the parent/child hierarchy of the filesystem. The specific nature of the relationship (e.g., "depends on") is conveyed through the surrounding prose.

**Reserved Filenames**
*   **`index.md`**: Used for **progressive disclosure**. It allows an agent to see what is available before opening individual documents, effectively preventing **context window saturation** during the discovery phase.
*   **`log.md`**: Records chronological history using ISO 8601 date headings (YYYY-MM-DD). This provides a flat, newest-first audit trail of the bundle's evolution.

---

### 4. Lifecycle Management: Maintaining Knowledge Integrity

**History & Supersession**
Integrity is maintained via the `timestamp` field and `log.md`. Newer entries or later timestamps denote the current state (**supersession**). Broken links in OKF are treated as a feature, not a bug; they represent **"unwritten knowledge"** or placeholder slots for agents to fill in the future.

**Advanced Management Patterns (Extensions)**
*   **Confidence Scoring:** Agents can use **Bayesian updating (Beta distribution)** to assign confidence. If a new `log.md` entry confirms a memory, the confidence increases; if it contradicts, the older memory is programmatically decayed.
*   **Active-Time Decay:** To prevent "evaporation" of knowledge during inactivity, apply exponential decay tied to **agent active time** (monotonic clock) rather than wall-clock time.

---

### 5. Reference Implementations & Ingestion

Google provides two official reference implementations to ensure producer/consumer independence:
1.  **Enrichment Agent:** An automated workflow that crawls metadata (e.g., BigQuery) to draft OKF files and enriches them with citations and join paths.
2.  **Static HTML Visualizer:** A self-contained file that transforms any OKF bundle into an interactive graph view. It requires no backend and ensures no data leaves the local page.

**High-Rigidity Ingestion Logic**
To ingest legacy data into OKF, use the following engineering standards:
*   **Messy Spreadsheets:** Use `openpyxl` over `pandas`. Unlike `pandas`, which assumes tabular structure, `openpyxl` allows agents to identify **merged cells, free text, and arbitrary layouts** common in organizational knowledge.
*   **Dual-Path PPT Extraction:** Reach 90-95% accuracy by combining XML structure extraction (`python-pptx`) with **vision-language model (VLM) captioning** of slide images.
*   **Environment Management:** Use **PEP 723 inline script metadata** with `uv run` for all extraction scripts. This ensures isolated, reproducible environments without `requirements.txt` bloat.

```python
# /// script
# dependencies = ["openpyxl", "python-pptx", "pillow"]
# ///
# Ingestion logic follows...
```

---

### 6. Hybrid Retrieval and MCP Integration

**Hybrid Retrieval Strategy**
To ensure technical identifiers (like policy codes) are not lost to paraphrasing, implementations must combine:
1.  **Semantic Search (Vector):** Captures conceptual meaning.
2.  **Keyword Search (BM25):** Ensures exact matches for specific technical IDs.

**Model Context Protocol (MCP)**
Utilize an OKF-compatible MCP server (e.g., **Kwipu**) to allow agents like Claude Desktop to query the knowledge graph locally. These servers extract entity-relation triples from OKF YAML and links, providing a local Graph RAG engine that runs on a local LLM (e.g., via Ollama).

---

### 7. Implementation Checklist & Repository Layout

**Recommended Repository Layout**
```text
/bundle-root/
├── index.md
├── log.md
├── metrics/
│   ├── index.md
│   └── weekly_active_users.md
├── tables/
│   ├── index.md
│   ├── orders.md
└── playbooks/
    └── incident_response.md
```

**Step-by-Step Checklist**
1.  **Define Concept IDs:** Establish file-path naming conventions.
2.  **Initialize Hierarchy:** Create directories for major categories.
3.  **Standardize Types:** Define mandatory `type` values.
4.  **Populate Frontmatter:** Ensure all `.md` files have at least a `type` field.
5.  **Dual-Path Extraction:** Ingest PPTs via XML + VLM captioning.
6.  **Granular Spreadsheet Parsing:** Use `openpyxl` for non-tabular data.
7.  **Establish Links:** Use relative Markdown links for the graph.
8.  **Create Indexes:** Add `index.md` for progressive disclosure.
9.  **Audit via Log:** Implement `log.md` for chronological tracking.
10. **Validate Conformance:** Ensure YAML is parseable and `type` is present.

---

### 8. Pitfalls and Anti-Patterns

*   **Spatial/Miro Traps:** Representing spatial or color-coded data (e.g., Miro boards) is **token-inefficient**. These remain "hard to crack" and require high-density summarization rather than raw conversion.
*   **Document Dumping:** Uploading raw PDFs into the bundle is an anti-pattern. Data must be processed into Markdown/YAML to avoid unreliable retrieval.
*   **YAML Indentation:** Indentation errors are the primary cause of parsing failure; use automated validation.

---

### 9. Source Attributions & Conformance

**Citations**
*   **Google Cloud Blog:** Sam McVeety & Amir Hormati, "Introducing the Open Knowledge Format" (June 2026).
*   **PPC Land:** Luis Rijo, "Google's OKF wants to be the lingua franca for AI agent knowledge" (June 2026).
*   **Personal Knowledge Management:** Eric J. Ma, "Mastering PKM with Obsidian and AI" (March 2026).

**Conformance Summary**
A bundle is conformant with OKF v0.1 if it meets these three conditions:
1.  Every non-reserved Markdown file contains a **parseable YAML frontmatter block**.
2.  Every frontmatter block contains a **non-empty `type` field**.
3.  Every **reserved filename** (`index.md`, `log.md`), where present, follows the specification's structural definitions.
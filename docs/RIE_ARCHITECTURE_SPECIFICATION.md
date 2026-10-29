# RIE Architecture Specification (OS Contract Document)

**Document Version:** `v1.0.0`  
**Governing Standard:** Sovereign Epistemic Intelligence OS Specification  
**Classification:** Canonical Architectural Specification  

---

## 1. 3-Layer Dependency Law

RIE enforces strict, unidirectional architectural layering:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Layer 1: Pure Epistemic Kernel (engine/core/)                               │
│ • Deterministic epistemic rules, taxonomy engine, schema contracts         │
│ • 24 Deterministic Validation Gates (Structural & Semantic)                 │
│ • STRICT LAW: ZERO imports of openpyxl, sqlite3, adapters, or file paths    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (Pure Epistemic Invariants & Gates)
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ Layer 2A: Deterministic Runtime Adapters (engine/adapters/)                 │
│ • Excel SSOT Engine (atomic pre-save backups, SpreadsheetML validation)     │
│ • SQLite Sidecar Adapter (downstream CTE graph projection)                  │
│ • Obsidian Vault Adapter (atomic frontmatter & wikilink compiler)           │
│ • HybridBatchOrchestrator & RCAuditor                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Layer 2B: Human & AI Interface Definitions                                  │
│ • Domain Packs (modules/<domain>/domain_module.json)                        │
│ • Progressive Disclosure Agent Skills (.agents/skills/)                     │
│ • Claude Code Command Runbooks (.claude/commands/)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Layer 2C: Sandboxed Agent Gateway (engine/mcp_server.py)                     │
│ • Standard JSON-RPC 2.0 Model Context Protocol (MCP) Stdio Server           │
│ • Fail-closed authorization: Agents cannot directly mutate storage files    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (Atomic Physical I/O)
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ Layer 3: Knowledge Substrate (workspace/)                                   │
│ • inbox/                  - Raw document intake                             │
│ • RIE_COMMAND_CENTER.xlsx - 20-sheet Authoritative Human SSOT               │
│ • rie_substrate.db        - Synchronized SQLite Graph Sidecar               │
│ • obsidian_vault/         - Compiled Atomic Markdown Notes Vault            │
│ • transactions/           - Staged Candidate Batches & Audit Proofs         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Epistemic Hierarchy & Source Registration Boundary

RIE prohibits epistemic collapse by enforcing an inviolable structural hierarchy:

```text
External Source Reference (URL, DOI, Citation)
         │
         ▼
DATA_SOURCE Registration Record (Source Pointer Only)
         │
         ├─────────────────────────────────────────────┐
         ▼ (Verified primary text captured in inbox)   ▼ (Primary text unavailable)
Discourse Unit Layer (DUL)                        [WAITING_FOR_EVIDENCE]
         │                                        "Primary transcript required"
         ▼
Evidence Objects (EO: Verbatim spans + SHA-256)
         │
         ▼
Interpretation Objects (IO: Competing H1 vs H2)
         │
         ▼
Knowledge Objects (KO: Transferable Principles)
         │
         ▼
Human Level 5 Ratification (CANONICAL)
```

### Constitutional Boundaries:
1. **$\text{SOURCE\_REFERENCE} \neq \text{EVIDENCE\_OBJECT}$:** A URL or citation only registers a pointer. An Evidence Object requires verified primary text captured locally in `workspace/inbox/`.
2. **Prohibited Automations:**
   - RIE MUST NOT scrape external websites or YouTube automatically.
   - RIE MUST NOT summarize external videos or articles from metadata, titles, descriptions, or comment sections.
   - RIE MUST NOT generate Evidence Objects from bare URLs.
   - RIE MUST NOT generate Knowledge Objects from unverified references.
3. **No Direct KO Generation:** A Knowledge Object must NEVER be created directly from raw source material without grounded Evidence and Interpretation Objects.

---

## 3. Canonical JSON Schemas

All data exchanging between layers must conform to schemas under `engine/core/schemas/`:
1. `discourse_unit_stream.schema.json` — Segmented discourse units ($DU_1 \dots DU_N$) with span hashes.
2. `candidate_eo_batch.schema.json` — Verbatim evidence objects with timecodes.
3. `dialectical_io_batch.schema.json` — Competing causal models ($H_1 \neq H_2$) and research questions.
4. `conceptual_ko_batch.schema.json` — High-level transferable principles.
5. `domain_module.schema.json` — Pluggable domain pack definitions.

---

## 4. Excel SSOT Contract (`workspace/RIE_COMMAND_CENTER.xlsx`)

- **20 Dedicated Sheets:**
  - 10 Interactive UI tabs: `01_Executive_Dashboard` through `07_Human_Decision_Log`.
  - 10 Data Tables: `DATA_SOURCE`, `DATA_EO`, `DATA_IO`, `DATA_KO`, `DATA_RELATIONSHIPS`, `DATA_CLUSTERS`, `DATA_PROVENANCE`, `DATA_DECISION_LOG`, `DATA_EVOLUTION`, `DATA_KO_HISTORY`.
- **Primary & Foreign Key Invariants:**
  - `Source_ID`, `EO_ID`, `IO_ID`, `KO_ID`, `Relationship_ID` must be unique and non-null.
  - In `DATA_KO`, rank formula must utilize dynamic range `$V$2:$V$5000` to prevent `#N/A` errors.
- **Atomic Pre-Save Backup:** Every mutation creates a bit-exact timestamped copy in `workspace/BACKUP_BEFORE_UPDATE/`.

---

## 5. SQLite Performance Sidecar Contract (`workspace/rie_substrate.db`)

- **Role:** Non-authoritative performance sidecar strictly rebuilt from the Excel SSOT.
- **Authority Lock Table (`SSOT_AUTHORITY_METADATA`):** Contains `authority_rule`, `ssot_sha256`, and `synchronized_utc`.
- **Graph Traversal Interface:** Supports recursive Common Table Expression (CTE) graph queries (`query_ko_graph_traversal`).

---

## 6. MCP Server Protocol Interface (`engine/mcp_server.py` - Layer 2C)

- Standard input/output JSON-RPC 2.0 server.
- Exposes safe tools: `rie_status`, `rie_query_graph`, `rie_export_dul`.
- Fail-closed error reporting with standard JSON-RPC error codes.
- AI agents are denied write access to Excel/SQLite; they stage candidate files for deterministic engine processing.

---

## 7. Steward Lifecycle State Machine

Every knowledge object progresses through distinct deterministic states:

```text
[RAW_DOCUMENT / TRANSCRIPT]
       │
       ▼ (export-dul)
[DISCOURSE_UNITS] (with span hashes)
       │
       ▼ (Frontier AI Synthesis)
[STAGED_BATCH] (EO, IO, KO, Relationships)
       │
       ▼ (24-Gate Semantic & Structural Validation)
[CANDIDATE_COMMITTED] (Human_Approval_State: PENDING_LEVEL_5_REVIEW)
       │
       ├─────────────────────────────────────────┐
       ▼ (Level 5 Ratification)                  ▼ (Level 5 Rejection)
[CANONICAL_RATIFIED] (APPROVED)           [REJECTED_ARCHIVE]
```

---

## 8. The 24 Deterministic Validation Gates

Ingested candidate batches must pass 24 gates before entering storage:
- **12 Structural Gates:** Schema conformity, primary/foreign key integrity, timestamp ordering, span SHA-256 integrity, formula sanity.
- **12 Semantic Gates:**
  1. `GATE_SEM_SRC_01`: Source fingerprint and span deduplication.
  2. `GATE_SEM_EO_01`: Timecode and span hash verification.
  3. `GATE_SEM_EO_02`: Propositional completeness and clause structure.
  4. `GATE_SEM_EO_03`: Intra-batch Jaccard overlap strictly bounded ($< 0.45$).
  5. `GATE_SEM_EO_04`: Ingestion cardinality dynamic envelope compliance.
  6. `GATE_SEM_IO_01`: Counter-hypotheses dialectical diversity (Cosine $< 0.55$).
  7. `GATE_SEM_IO_02`: Dialectical independence ($H_1 \neq H_2$).
  8. `GATE_SEM_IO_03`: Research questions domain inquiry orthogonality.
  9. `GATE_SEM_IO_04`: Dynamic confidence score calibration (variance $> 0$).
  10. `GATE_SEM_IO_05`: Contradiction preservation without silent erasure.
  11. `GATE_SEM_KO_01`: Authentic abstract principle titles without boilerplate.
  12. `GATE_SEM_KO_02`: Balanced evidence/interpretation binding without monolithic collapse.
  13. `GATE_SEM_KO_03`: Dynamic KO confidence calibration and causal edge transmission rationale ($\ge 10$ words).

---

## 9. Pluggable Extension API

To add new operational domains without modifying engine code, drop a directory into `modules/<name>/` containing `domain_module.json` conforming to `domain_module.schema.json`.
The taxonomy loader auto-discovers and registers enabled domains on startup.

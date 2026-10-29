---
name: rie-ingest
description: Use this skill when ingesting raw transcripts or technical notes into RIE Knowledge Objects or registering external source pointers.
---

# RIE Ingestion Runbook

## Governing Operational Law
> **Humans express intent. Antigravity operates the interface. RIE enforces deterministic epistemic governance.**

Antigravity may orchestrate operations, but it cannot bypass RIE evidence validation boundaries.

---

## Workflow 1: Direct Ingestion ("RIE ingest the new file in inbox")

When the user says:
> **"RIE ingest the new file in inbox"**

1. **Scan `workspace/inbox/`:**
   Detect newly deposited research files (`.pdf`, `.txt`, `.md`, `.json`, transcript files).

2. **Segment Source into Discourse Units:**
   ```bash
   python rie.py export-dul workspace/inbox/<file> --out workspace/transactions/staged_dul.json
   ```

3. **Frontier AI Synthesis:**
   Synthesize candidate batches adhering strictly to schemas in `engine/core/schemas/`:
   - `SOURCE_METADATA.json` (Source title, author, duration, SHA-256)
   - `EO_BATCH.json` (Verbatim quotes, timecodes, byte-span hashes)
   - `IO_BATCH.json` (Causal research questions, competing models $H_1 \neq H_2$, calibrated confidence)
   - `KO_BATCH.json` (Transferable domain principles, domain taxonomy code)
   - `RELATIONSHIP_BATCH.json` (Causal graph edges connecting KOs)

4. **Validate and Stage:**
   ```bash
   python rie.py stage-batch <batch_dir> --commit
   ```
   - Evaluates all 24 structural and semantic validation gates.
   - Enforces `Status = "CANDIDATE"` and `Human_Approval_State = "PENDING_LEVEL_5_REVIEW"`.
   - Appends records to `workspace/RIE_COMMAND_CENTER.xlsx` with pre-mutation backup.
   - Auto-synchronizes the `rie_substrate.db` SQLite sidecar.

---

## Workflow 2: Source Registration ("RIE register this YouTube source")

When the user says:
> **"RIE register this YouTube source"** *(or "RIE register this research paper source")*

1. **Register Metadata in `DATA_SOURCE`:**
   Record `source_id`, URL, title, author/channel, publication metadata, and capture timestamp.

2. **Check Evidence Availability in `workspace/inbox/`:**
   - **If primary text (transcript/captions/PDF) exists in `workspace/inbox/`:**  
     Proceed into Workflow 1 (DUL segmentation $\rightarrow$ EO/IO/KO synthesis).
   - **If primary text is missing:**  
     **STOP.** Do not fabricate quotes or summarize. Mark status as `WAITING_FOR_EVIDENCE`.  
     Return to the user:
     > *"Source registered.*  
     > *Primary transcript evidence is required before RIE can generate Evidence Objects.*  
     > *Please place the transcript/caption text into `workspace/inbox/`."*

### 🛡️ Constitutional Prohibitions:
- **Never** scrape YouTube or websites automatically.
- **Never** summarize from titles, descriptions, or comments.
- **Never** generate Evidence Objects ($EO$) from bare URLs.
- **Never** generate Knowledge Objects ($KO$) from unverified external references.
- **Invariant:** `SOURCE_REFERENCE != EVIDENCE_OBJECT`. An Evidence Object strictly requires verified primary text captured locally inside the workspace.

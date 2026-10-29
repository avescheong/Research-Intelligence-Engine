# RIE Human User Guide

Welcome to the **Research Intelligence Engine (RIE v1.0.0)**. This guide explains how to operate RIE as a human researcher without needing technical command-line knowledge.

---

## 🏛️ Governing Operational Law

RIE is governed by a foundational constitutional law:

> **Humans express intent. Antigravity operates the interface. RIE enforces deterministic epistemic governance.**

### What RIE Is NOT:
- **RIE is not a chatbot:** It does not produce ephemeral, hallucinated conversations.
- **RIE is not a note-taking application:** It does not passively store unchecked claims.
- **RIE is not simple RAG:** It does not retrieve raw text chunks into unverified summaries.

### What RIE IS:
**A human-governed epistemic operating system.** RIE turns complex research papers, technical briefings, and multi-speaker transcripts into high-confidence, verified knowledge graphs while strictly preserving intellectual custody and human sovereignty.

---

## 🧭 Your Workspace at a Glance

All human interaction centers around a single folder: [`workspace/`](../workspace/):

```text
workspace/
├── inbox/                  <-- Drop your raw research documents (PDF, TXT, MD, transcripts) here
├── RIE_COMMAND_CENTER.xlsx <-- Open this in Microsoft Excel to inspect & ratify candidate knowledge
├── rie_substrate.db        <-- Fast SQLite graph sidecar used by AI search & graph traversal
└── obsidian_vault/         <-- Open this in Obsidian for bidirectional linked Markdown notes
```

---

## 💬 Natural Language Human Commands

As a researcher, you communicate directly with your AI assistant (e.g., Antigravity or Claude Code). You never need to memorize internal Python flags or CLI options.

### 1. Ingesting New Research
> **"RIE ingest the new file in inbox"**

- **What happens:**
  1. Detects new files in `workspace/inbox/` (`.pdf`, `.txt`, `.md`, `.json`, transcript files).
  2. Extracts text and structures it into propositionally aligned Discourse Units (DUL) with SHA-256 byte-span hashes.
  3. Synthesizes grounded Evidence Objects ($EO$), dialectical Interpretation Objects ($IO$), and Knowledge Objects ($KO$).
  4. Runs all 24 deterministic structural and semantic validation gates.
  5. Stages validated objects atomically into `workspace/RIE_COMMAND_CENTER.xlsx` strictly as **CANDIDATE**.

### 2. Registering an External Source Pointer
> **"RIE register this YouTube source"**  
> *(or "RIE register this research paper source")*

- **What happens:**
  1. Registers source metadata (`source_id`, URL, title, author/channel, publication date) into `DATA_SOURCE`.
  2. Checks whether verified primary evidence material is present in `workspace/inbox/`.
  3. **Evidence Availability Gate:**
     - **If verified primary text/transcript exists in `workspace/inbox/`:** Continues into DUL segmentation $\rightarrow$ EO $\rightarrow$ IO $\rightarrow$ KO synthesis.
     - **If primary text is unavailable:** Stops immediately at `WAITING_FOR_EVIDENCE`. RIE responds:
       > *"Source registered.*  
       > *Primary transcript evidence is required before RIE can generate Evidence Objects.*  
       > *Please place the transcript/caption text into `workspace/inbox/`."*

#### 🛡️ Explicit Epistemic Prohibitions:
- **RIE MUST NOT** scrape YouTube or websites automatically.
- **RIE MUST NOT** summarize videos or articles from titles, descriptions, or comment sections.
- **RIE MUST NOT** treat URLs as evidence.
- **RIE MUST NOT** generate Evidence Objects from external metadata alone.
- **RIE MUST NOT** generate Knowledge Objects from unverified references.
- **Core Invariant:**  
  $$\text{SOURCE\_REFERENCE} \neq \text{EVIDENCE\_OBJECT}$$  
  A source reference only identifies where evidence may exist. An Evidence Object strictly requires verified primary text captured locally inside the workspace.

### 3. Searching the Knowledge Graph
> **"RIE query everything about <topic>"** *(e.g. "RIE query everything about liquidity")*

- **What happens:** Performs multi-hop recursive graph walks over the SQLite sidecar and presents connected concepts, evidence citations, and causal relationships.

### 4. Preparing for Human Ratification
> **"RIE prepare this source for review"** *(or "RIE summarize pending candidates")*

- **What happens:** Assembles a structured review summary highlighting proposed concepts, competing hypotheses ($H_1$ vs. $H_2$), and confidence calibrations awaiting your decision.

### 5. Running Diagnostics
> **"RIE run diagnostics"**

- **What happens:** Verifies environment health, dependencies (`openpyxl`), workbook integrity, and domain taxonomies.

---

## ⚖️ Two Operational Tiers

| Aspect | Tier 1: Human Intent Commands (Primary) | Tier 2: Advanced CLI (Engineers & Debugging) |
| :--- | :--- | :--- |
| **Interface** | Antigravity / Claude Code conversational chat | System Terminal (`cmd`, `powershell`, `bash`) |
| **Command Style**| Natural intent: *"RIE ingest..."*, *"RIE register..."* | Direct syntax: `python rie.py <cmd> [flags]` |
| **User Role** | Human Researcher / Knowledge Architect | Developer / Automation Engineer |
| **Complexity** | Zero CLI friction; automated orchestration | Direct execution with manual parameters |

---

## 🛡️ Epistemic Hierarchy & Non-Collapse

RIE enforces strict architectural separation between 3 layers of reasoning:

1. **Evidence Objects ($EO$):** Verbatim, ground-truth observations directly quoted from primary sources. Must include start/end timecodes and immutable SHA-256 span hashes. *("What was actually observed.")*
2. **Interpretation Objects ($IO$):** Explicit research questions evaluated by competing hypotheses ($H_1 \neq H_2$). Preserves uncertainty and dialectical tension with calibrated confidence scores. *("What explanations could account for the evidence.")*
3. **Knowledge Objects ($KO$):** High-level transferable principles, validated causal relationships, and cross-source synthesis. *A Knowledge Object must never be created directly from raw source material without grounded EOs and IOs.*

```text
Primary Source Material
         │
         ▼
Discourse Unit Layer (DUL)
         │
         ▼
Evidence Objects (EO)
         │
         ▼
Interpretation Objects (IO: H1 vs H2)
         │
         ▼
Knowledge Objects (KO)
         │
         ▼
Human Level 5 Ratification (CANONICAL)
```

---

## 👑 Sovereign Human Ratification Boundary

In RIE:
- **AI creates candidates.**  
- **RIE validates structure.**  
- **Humans ratify canonical knowledge.**

All generated objects enter `workspace/RIE_COMMAND_CENTER.xlsx` with:
- `Status = "CANDIDATE"`
- `Human_Approval_State = "PENDING_LEVEL_5_REVIEW"`
- `Canonical_Status = "NOT_APPROVED"`

Only explicit human ratification (via in-person review or `python rie.py approve <tx_id>`) can promote candidates to `CANONICAL` (`APPROVED`).

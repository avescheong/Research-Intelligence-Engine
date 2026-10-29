# RIE Portable OS (v1.0.0)

> **Research Intelligence Engine — Sovereign Epistemic Operating System for Desktop, Antigravity, and Claude Code.**

RIE is a local, privacy-first intelligence OS designed to extract, synthesize, validate, and query deep knowledge graphs from complex multi-speaker discourse, research papers, and technical transcripts.

---

## 🧭 Human Workflow & Zero-Friction Operation

RIE is governed by a single operational law:

**Humans express intent. Antigravity operates the interface. RIE enforces deterministic epistemic governance.**

For a human researcher, working with RIE requires **zero memorization of technical commands or Python syntax**:
1. **Humans express intent:** You converse naturally with your AI assistant (e.g., Antigravity). You drop raw documents, research papers, or media transcripts into your workspace inbox and specify what you want to achieve.
2. **Antigravity acts as the operational interface:** Antigravity discovers and invokes RIE's specialized agent skills on demand, coordinating multi-step extraction, dialectical synthesis, and file validation. Antigravity may orchestrate operations, but it cannot bypass RIE evidence validation boundaries.
3. **RIE handles the engine mechanics:** Behind the scenes, the RIE Epistemic Kernel segments text into verifiable Discourse Units, checks 24 structural and semantic validation gates, prevents hallucinations, performs bit-exact workbook backups, and synchronizes the SQLite graph sidecar.
4. **The user retains sovereign control:** The user does not need to operate internal scripts. The user directs the research workflow and holds exclusive authority to ratify knowledge candidates into canonical knowledge.

> **AI generates candidates. RIE validates structure. Humans ratify canonical knowledge.**

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Human Researcher (Intent & Sovereignty)                                 │
│    "RIE ingest the new file in inbox"                                       │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (Natural Language Intent)
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ 2. AI Interface Layer (Antigravity / Claude Code)                          │
│    Loads RIE agent skills (rie-ingest, rie-query-graph, rie-ratify)        │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (Automated Tool Orchestration)
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ 3. RIE Deterministic Engine & Adapters (Layer 1 & Layer 2A/2C)              │
│    • DUL Segmentation (span hashes & timecodes)                             │
│    • 24 Semantic & Structural Gates (EO != IO != KO, Jaccard bound, CTE)    │
│    • Atomic Excel SSOT commit & SQLite sidecar graph indexing               │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (Candidate Review Package)
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ 4. Human Single Source of Truth (workspace/RIE_COMMAND_CENTER.xlsx)        │
│    Human inspects candidates → Grants Level 5 Ratification (CANONICAL)      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 💬 Common RIE Commands (Antigravity Natural Interface)

Interact with RIE directly in the Antigravity conversation window using these natural language instructions:

### 1. Ingest New Material
> **"RIE ingest the new file in inbox"**
- **Purpose:** 
  - Automatically detects new source files dropped into `workspace/inbox/` (`.pdf`, `.txt`, `.md`, `.json`, transcript files).
  - Extracts and normalizes content into discrete proposition units.
  - Generates propositionally aligned Discourse Units (DUL) with byte-span SHA-256 hashes.
  - Synthesizes grounded Evidence Objects ($EO$), dialectical Interpretation Objects ($IO$), and Knowledge Objects ($KO$).
  - Executes all 24 structural and semantic validation gates.
  - Stages validated candidates into `workspace/RIE_COMMAND_CENTER.xlsx` strictly for human review.

### 2. Register an External Source Pointer
> **"RIE register this YouTube source"** *(or "RIE register this research paper source")*
- **Operational Model:**
  ```text
  External URL / Pointer
         │
         ▼
  DATA_SOURCE Registration Only (Metadata Record)
         │
         ▼
  Evidence Availability Check (workspace/inbox/)
         │
         ├─────────────────────────────────────────────┐
         ▼ (Verified local transcript/PDF exists)     ▼ (Primary text unavailable)
  [DUL Segmentation → EO → IO → KO Pipeline]     [WAITING_FOR_EVIDENCE]
  ```
- **Purpose & Workflow:**
  - Registers the source metadata (`source_id`, URL, title, author/channel, publication metadata, capture timestamp) into `DATA_SOURCE`.
  - Creates a tracking record and immediately verifies evidence availability in `workspace/inbox/`.
  - **Evidence Availability Gate:**
    - **Verified local transcript/PDF exists:** Continues into DUL segmentation $\rightarrow$ EO $\rightarrow$ IO $\rightarrow$ KO pipeline.
    - **Primary text unavailable:** Stops cleanly at `WAITING_FOR_EVIDENCE`.
- **Expected System Response When Evidence Is Missing:**
  > *"Source registered.*  
  > *Primary transcript evidence is required before RIE can generate Evidence Objects.*  
  > *Please place the transcript/caption text into `workspace/inbox/`."*
- **Explicit Epistemic Boundaries (RIE MUST NOT):**
  - **RIE MUST NOT** scrape YouTube automatically.
  - **RIE MUST NOT** summarize videos from titles, descriptions, or comments.
  - **RIE MUST NOT** treat URLs as evidence.
  - **RIE MUST NOT** generate Evidence Objects from external metadata.
  - **RIE MUST NOT** generate Knowledge Objects from unverified external references.
- **Core Invariant:**
  > `SOURCE_REFERENCE != EVIDENCE_OBJECT`  
  > A source reference only identifies where evidence may exist.  
  > An Evidence Object requires verified primary text captured locally inside the RIE workspace.

### 3. Search and Graph Traversal
> **"RIE query everything about <topic>"** *(e.g. "RIE query everything about liquidity")*
- **Purpose:**
  - Performs multi-hop Common Table Expression (CTE) recursive graph walks across the `rie_substrate.db` SQLite sidecar.
  - Returns connected canonical and candidate Knowledge Objects, causal relationships, and evidentiary citations.

### 4. Prepare for Human Ratification
> **"RIE prepare this source for review"** *(or "RIE summarize pending candidates")*
- **Purpose:**
  - Compiles a human review package summarizing newly staged candidate batches.
  - Highlights competing hypotheses ($H_1$ vs. $H_2$), confidence calibrations, and any unresolved contradictions.
  - Prepares the transaction ID for Level 5 human ratification.

### 5. Check System Integrity
> **"RIE run diagnostics"** *(or "RIE doctor")*
- **Purpose:**
  - Diagnoses Python runtime, dependency status (`openpyxl`), workbook structure, and active domain taxonomies.

---

## ⚖️ Two Operational Tiers: Human vs. Advanced Commands

| Aspect | Tier 1: Human Commands (Primary) | Tier 2: Advanced CLI (Engineers & Debugging) |
| :--- | :--- | :--- |
| **Interface** | Antigravity / Claude Code conversational chat | System Terminal / Command Line (`cmd`, `powershell`, `bash`) |
| **Command Style**| Natural intent: *"RIE ingest..."*, *"RIE query..."* | Explicit CLI syntax: `python rie.py <subcommand> [flags]` |
| **User Role** | Human Researcher / Knowledge Architect | System Developer / CI Automation / Audit Engineer |
| **Complexity** | **Zero-friction:** Hides AST checks, JSON schemas, XML validation | **Full control:** Direct access to individual pipeline flags |
| **Examples** | • *"RIE ingest the new file in inbox"*<br>• *"RIE query liquidity"*<br>• *"RIE run diagnostics"* | • `python rie.py stage-batch <dir> --commit`<br>• `python rie.py query "liquidity" --depth 3`<br>• `python rie.py rc-audit` |

---

## 💎 RIE's 5 Core Value Pillars

1. **Epistemic Separation ($EO \neq IO \neq KO$):**  
   RIE strictly separates facts from interpretations and theories. Verbatim quotes from primary sources ($EO$), dialectical competing hypotheses ($IO$), and overarching transfer principles ($KO$) live in distinct schemas. AI is prevented from collapsing them into unverifiable text.

2. **Evidence-First Knowledge Creation:**  
   Knowledge cannot be created from thin air or vague web summaries. Every Knowledge Object must be explicitly anchored to verified Evidence Objects with transcript timecodes and immutable SHA-256 byte-span hashes.

3. **Sovereign Human Ratification Boundary:**  
   Frontier AI generates **only candidates** (`Status = "CANDIDATE"`, `Human_Approval_State = "PENDING_LEVEL_5_REVIEW"`). AI can **never** ratify its own output. Only the Human Architect can promote candidates to `CANONICAL`.

4. **Long-Term Knowledge Custody:**  
   RIE preserves the entire lineage of understanding—not just static answers. Every record tracks its original source, alternative hypotheses considered, human decision logs, and relationship graph over years.

5. **Vendor-Independent AI Workflow:**  
   Your data and reasoning logic are completely decoupled from any single AI vendor. Switch between Google Gemini, Anthropic Claude, OpenAI, or local models at will without losing your knowledge substrate.

---

## ⏱️ First 5 Minutes With RIE

1. **Open `RIE_PORTABLE_DESKTOP`** in Antigravity or Claude Code.
2. **Place a document** (PDF, transcript, research note, or article) into:
   ```text
   workspace/inbox/my_research.pdf
   ```
3. **Tell RIE:**
   > "RIE ingest the new file in inbox"
4. **Wait for processing:** RIE segments the text, formulates hypotheses, and verifies all 24 structural and semantic gates.
5. **Review candidates:** Open Microsoft Excel to inspect newly staged objects:
   ```text
   workspace/RIE_COMMAND_CENTER.xlsx
   ```
6. **Approve only the knowledge you trust:** Promote candidates to canonical knowledge via Excel or terminal command (`python rie.py approve <tx_id>`).

---

## 🚀 60-Second Quickstart (Environment Setup)

### 1. Prerequisites
- Python 3.10+ (tested on Windows 10/11, macOS, and Linux).
- Single external dependency: `openpyxl`.

```bash
# Clone or unzip repository
cd RIE_PORTABLE_DESKTOP

# Install dependency
pip install -r requirements.txt

# Initialize workspace from clean-slate templates
python rie.py init

# Verify system health
python rie.py doctor
```

---

## ⚡ Quick Start: Ingest Your First Knowledge Source

This is the primary day-to-day workflow for human researchers:

### Step 1: Drop Your Source File
Place any research document, article, paper, or transcript (`.pdf`, `.txt`, `.md`, `.json`) into:
```text
workspace/inbox/
```

### Step 2: Trigger Ingestion via AI Interface
Through an AI interface such as Antigravity or Claude Code, send:
> **"RIE ingest the new file in inbox"**

### Step 3: What RIE Does Automatically
Behind the scenes, RIE runs a deterministic, fail-closed pipeline:
- **Extracts and structures** the source payload into clean propositional units.
- **Creates Discourse Units (DUL)** with start/end timecodes and cryptographic span hashes (`span_sha256`).
- **Synthesizes grounded epistemic objects**:
  - **Evidence Objects ($EO$):** Verbatim cited spans from primary text.
  - **Dialectical Interpretation Objects ($IO$):** Research questions with competing models ($H_1$ vs. $H_2$) and calibrated confidence.
  - **Knowledge Objects ($KO$):** Transferable domain principles evaluated across $EO$s and $IO$s.
- **Validates through RIE gates:** Enforces all 24 structural and semantic integrity gates (anti-hallucination Jaccard bounding, cardinality envelopes, dialectical independence, contradiction preservation).
- **Stages candidates for human review:** Appends objects atomically into `workspace/RIE_COMMAND_CENTER.xlsx` and synchronizes the `rie_substrate.db` SQLite graph sidecar.

### Step 4: Sovereign Human Ratification
> [!IMPORTANT]
> **AI does not approve knowledge.**  
> All generated objects are committed strictly with `Status = "CANDIDATE"` and `Human_Approval_State = "PENDING_LEVEL_5_REVIEW"`.  
> **Human approval is required before CANONICAL promotion.** Only the Human Architect can ratify candidate transactions into canonical knowledge (via Excel review or `python rie.py approve <tx_id>`).

---

## 🌟 Why RIE Is Different

### 1. Human-Friendly AI Interface
Users do not need to memorize or type complex CLI commands for normal workflows.

The primary human interaction happens through simple intent commands with an AI interface such as Antigravity or Claude Code, such as:
> **"RIE ingest the new file in inbox"**

This single command triggers the complete governed pipeline:
```text
Source File (PDF, text, transcript, markdown)
       │
       ▼
Content Extraction & Cleaning
       │
       ▼
Discourse Unit Layer (DUL) Segmentation (with span hashes)
       │
       ▼
Epistemic Candidate Generation (EO / IO / KO / Relationships)
       │
       ▼
24 Deterministic Validation Gates (Structural & Semantic)
       │
       ▼
Human Review in workspace/RIE_COMMAND_CENTER.xlsx
```
This simple conversational trigger hides immense technical complexity (tokenization, schema validation, XML SpreadsheetML checks, database sync) while fully preserving human governance at every step.

#### Source Registration Commands
For known external sources, users register source pointers prior to raw material capture:
> **"RIE register this YouTube source"**  
> **"RIE register this research paper source"**

This registers the source pointer and checks whether primary evidence material is present:
```text
External URL (YouTube / Research Paper / Web Link)
       │
       ▼
DATA_SOURCE Registration Only (Metadata Pointer)
       │
       ▼
Evidence Availability Check (workspace/inbox/)
       │
       ├─────────────────────────────────────────────┐
       ▼ (Verified local transcript/PDF exists)     ▼ (Primary text unavailable)
[DUL Segmentation → EO → IO → KO Pipeline]     [WAITING_FOR_EVIDENCE]
```
- **YouTube Source:** Registers metadata; stops at `WAITING_FOR_EVIDENCE` until transcript/caption text is dropped into `workspace/inbox/`.
- **Research Paper Source:** Registers bibliographic citation; requires PDF or full-text capture in `workspace/inbox/` before synthesis.
- **Web Article Source:** Registers canonical URL; requires verified archived text capture in `workspace/inbox/`.

> [!IMPORTANT]
> **SOURCE_REFERENCE != EVIDENCE_OBJECT**  
> A source reference only identifies where evidence may exist. An Evidence Object strictly requires verified primary text captured locally inside the RIE workspace. RIE must never treat URLs as evidence, scrape external websites silently, or synthesize knowledge from titles, descriptions, or comment sections.

---

### 2. A Sovereign Epistemic Operating System
To understand RIE, it is essential to understand what it is **not**:
- **RIE is not a chatbot:** General-purpose chatbots are optimized for conversational assistance. Their outputs are usually not designed as permanent, auditable knowledge records.
- **RIE is not a simple note-taking application:** Note tools (like standard wikis or markdown apps) are passive storage containers; they do not systematically validate reasoning, enforce source citations, or detect dialectical contradictions.
- **RIE is not only a RAG search system:** Traditional Retrieval-Augmented Generation (RAG) is designed for semantic search and question answering; it typically lacks dynamic cardinality envelopes, dialectical hypothesis modeling ($H_1$ vs. $H_2$), and sovereign human approval workflows.

**RIE is a human-governed epistemic operating system.** It provides an operating kernel for thinking, validating, accumulating, and querying durable knowledge over years of research.

---

### 3. Epistemic Non-Collapse
Traditional AI systems suffer from *epistemic collapse*—they blend facts, guesses, and grand conclusions into a single paragraph where you cannot tell what was actually said versus what the AI inferred.

RIE strictly enforces **epistemic separation** across 3 distinct object layers:
1. **Evidence Objects ($EO$):** Verbatim, ground-truth observations directly quoted from primary sources, anchored by timecodes and immutable cryptographic byte-span hashes (`span_sha256`).
2. **Interpretation Objects ($IO$):** Explicit causal research questions accompanied by competing dialectical hypotheses ($H_1$ vs. $H_2$). RIE forbids one-sided assertions and requires authentic dialectical tension with calibrated confidence scores.
3. **Knowledge Objects ($KO$):** High-level, transferable principles and mental models evaluated across multiple $EO$s and $IO$s, connected by causal edges in a graph.

Keeping these layers structurally separate prevents premature AI conclusions, ensures every claim can be audited back to primary data, and preserves intellectual honesty when new evidence contradicts old assumptions.

---

### 4. Knowledge Custody Over Time
RIE is designed not only to answer questions today, but to preserve the evolution of understanding over years.

Every knowledge object maintains:
- Its original evidence source and verbatim text spans (`DATA_EO` & `DATA_SOURCE`).
- The competing dialectical interpretations considered ($H_1$ vs. $H_2$).
- The human decisions made with full audit trails (`DATA_DECISION_LOG`).
- The semantic and causal relationships linking it to other knowledge objects (`DATA_RELATIONSHIPS`).
- Historical revisions and confidence calibrations over time (`DATA_KO_HISTORY`).

This creates a durable intelligence memory that can evolve dynamically without losing its reasoning history.

**RIE does not simply store answers. RIE preserves the journey from information → evidence → understanding → knowledge.**

---

### 5. Sovereign Human Ratification Boundary
In RIE, **AI never creates canonical knowledge on its own.**

- **AI generates candidates:** When frontier models process material, all synthesized objects enter the system strictly marked as:
  - `Status = "CANDIDATE"`
  - `Human_Approval_State = "PENDING_LEVEL_5_REVIEW"`
  - `Canonical_Status = "NOT_APPROVED"`
- **Human reviews:** The Human Architect inspects the evidence, competing models, and proposed concepts directly in Microsoft Excel (`workspace/RIE_COMMAND_CENTER.xlsx`).
- **Only human approval creates canonical knowledge:** Knowledge is only promoted to `CANONICAL` (`APPROVED`) when explicitly ratified by human decision. The human retains sovereign custody of truth.

---

### 6. Architectural Separation & Agent Gateway
RIE is built upon a strict, unidirectional layered architecture:
- **Layer 1: Deterministic Epistemic Kernel (`engine/core/`):** Pure epistemic logic and 24 validation gates. Completely isolated from physical file I/O, databases, or third-party libraries (zero storage dependencies).
- **Layer 2A: Adapters and Runtime (`engine/adapters/`):** The exclusive physical I/O gateway. Manages atomic Excel transactions with bit-exact backups, SpreadsheetML validation, SQLite sidecar indexing, and Obsidian note compilation.
- **Layer 2B: AI Skills and Interfaces (`modules/`, `.agents/skills/`, `.claude/commands/`):** Pluggable domain taxonomies and progressive-disclosure agent runbooks.
- **Layer 2C: Agent Gateway (`engine/mcp_server.py`):** Standard JSON-RPC 2.0 Stdio Model Context Protocol (MCP) server providing a sandboxed, fail-closed bridge so AI agents can only query or trigger permitted operations without direct file mutation privileges.
- **Layer 3: Human Knowledge Substrate (`workspace/`):** User data isolated in a single directory (`inbox/`, `RIE_COMMAND_CENTER.xlsx`, `rie_substrate.db`, `obsidian_vault/`), completely protected by `.gitignore` so personal research remains private.

---

### 7. RIE Vision
- **Sovereign Personal Intelligence:** Total privacy. Your data never leaves your machine unless you choose to send it. No mandatory cloud subscriptions or proprietary formats.
- **Institutional Intelligence:** A rigorous, auditable knowledge base where teams can trace every strategic insight back to primary sources with zero ambiguity.
- **Model and Vendor Independence:** RIE is completely decoupled from any single AI vendor. Switch between Google Gemini, Anthropic Claude, OpenAI, or local open-source models without losing your underlying knowledge graph.
- **Long-Term Knowledge Custody:** Stored in open, widely supported formats designed for long-term accessibility: standard Microsoft Excel XML (`.xlsx`), SQLite (`.db`), and human-readable Markdown (`.md`). Your research graph remains accessible and portable into the future, independent of the lifecycle of individual AI tools.

---

### 8. Comparison Tables

#### RIE vs. Chatbots
| Capability / Feature | Traditional Chatbot (ChatGPT, Claude Chat) | Research Intelligence Engine (RIE) |
| :--- | :--- | :--- |
| **Output Type** | Ephemeral text streams in chat window | Persistent, structured epistemic objects ($EO / IO / KO$) |
| **Fact vs. Inference** | Blended together (epistemic collapse) | Strictly separated into verifiable layers |
| **Source Citation** | Vague paraphrases or hallucinated links | Verbatim spans with cryptographic SHA-256 hashes |
| **Dialectical Models** | Sycophantic or one-sided summaries | Mandatory competing hypotheses ($H_1$ vs. $H_2$) |
| **Governance** | AI decides what is "true" | Only the Human Architect can ratify canonical knowledge |
| **Long-Term Memory** | Lossy context window or opaque embeddings | Authoritative Excel SSOT + SQLite graph sidecar |

#### RIE vs. Note-Taking Apps
| Capability / Feature | Note Apps (Notion, Obsidian, Roam) | Research Intelligence Engine (RIE) |
| :--- | :--- | :--- |
| **Core Nature** | Passive text storage containers | Active epistemic operating system |
| **Validation** | None (accepts anything typed or pasted) | 24 automated structural and semantic validation gates |
| **Contradiction Handling**| Contradictions sit unnoticed across pages | Built-in contradiction detection and tension tracking |
| **Graph Generation** | Manual `[[wikilink]]` typing | Automated multi-hop causal graph synthesis with CTE queries |
| **Agent Integration** | Unstructured text plugins | Governed agent skills with fail-closed boundaries |
| **Obsidian Support** | Native app | Automatically compiles into a clean Obsidian vault (`sync --vault`) |

#### RIE vs. Traditional RAG
| Capability / Feature | Traditional RAG Systems | Research Intelligence Engine (RIE) |
| :--- | :--- | :--- |
| **Chunking** | Blind fixed-character or token splitting | Semantic Discourse Unit Layer (DUL) with clause boundaries |
| **Retrieval Mechanism** | Vector similarity (frequently loses context) | Deterministic graph walks + relational database queries |
| **Synthesis Guardrails**| None; model hallucinates on retrieved chunks| Strict cardinality envelopes and anti-hallucination Jaccard bounds |
| **Auditability** | Opaque vector distances | Bit-exact pre-mutation backups and transparent decision logs |
| **Authority** | Vector database is a black box | Human Single Source of Truth in standard Excel |

---

## 📂 Human-Friendly Workspace Architecture

All human day-to-day workflow lives in **one folder: `workspace/`**:

```text
workspace/
├── inbox/                  # 1. Drop raw transcripts, articles, or notes here
├── RIE_COMMAND_CENTER.xlsx # 2. Open in Excel to review & ratify candidates
├── rie_substrate.db        #    (Auto-synced SQLite graph sidecar)
└── obsidian_vault/         # 3. Open this folder as your Obsidian vault!
```

---

## 🧠 3-Layer Epistemic Architecture

RIE enforces strict epistemic separation:
- **Layer 1: `engine/core/` (Pure Epistemic Kernel):** 24 deterministic validation gates (`EO != IO != KO`, dynamic confidence calibration, source deduplication). Zero dependencies on external storage.
- **Layer 2A: `engine/adapters/` (Deterministic Runtime):** Atomic Excel SSOT, cross-platform SQLite sidecar, Obsidian vault compiler, and Stdio MCP server.
- **Layer 2B: `modules/` & `.agents/skills/` (Human & AI Interfaces):** Pluggable domain packs and progressive-disclosure agent runbooks.
- **Layer 3: `workspace/` (Knowledge Substrate):** User data isolated from version control.

---

## 🛠️ Everyday Workflows

| Task | Command |
| :--- | :--- |
| **Check System Health** | `python rie.py doctor` |
| **Segment Transcript into DUL** | `python rie.py export-dul workspace/inbox/notes.txt --out dul.json` |
| **Stage & Validate AI Batch** | `python rie.py stage-batch batch_dir/ --commit` |
| **Query Knowledge Graph** | `python rie.py query "liquidity"` |
| **Ratify Candidates into Canonical** | `python rie.py approve <tx_id>` |
| **Sync SQLite & Obsidian** | `python rie.py sync --vault` |
| **Run Release Candidate Audit** | `python rie.py rc-audit` |

---

## 🤖 Using with Antigravity & Claude Code
- **Antigravity:** Open this directory in Antigravity. RIE rules and skills (`rie-ingest`, `rie-query-graph`, `rie-ratify`) load automatically on demand via progressive disclosure.
- **Claude Code:** Claude Code reads `CLAUDE.md` and discovers custom commands under `.claude/commands/` (`/rie-ingest`, `/rie-query`, etc.).
- **MCP Server:** To use RIE as native agent tools, configure `engine/mcp_server.py` in your agent's MCP settings (sample config in `templates/mcp.json.example`).

---

## 📜 Documentation & Governance
- [docs/HUMAN_USER_GUIDE.md](docs/HUMAN_USER_GUIDE.md) — Visual walkthrough for human users.
- [docs/RIE_ARCHITECTURE_SPECIFICATION.md](docs/RIE_ARCHITECTURE_SPECIFICATION.md) — Authoritative 9-contract OS specification.
- [CONTRIBUTING.md](CONTRIBUTING.md) — How to add domain modules, skills, and adapters.
- [RELEASE_MANIFEST_v1.0.md](RELEASE_MANIFEST_v1.0.md) — Official release manifest and checksums.

# RIE Agent Constitution & Operational Rules

You are operating within the **Research Intelligence Engine (RIE)** workspace.

---

## 🏛️ Governing Operational Law
> **Humans express intent. Antigravity operates the interface. RIE enforces deterministic epistemic governance.**

Antigravity may orchestrate operations, but it cannot bypass RIE evidence validation boundaries.

---

## 🛡️ Epistemic Non-Collapse Invariant
Never collapse or confuse epistemic layers:
1. **Fact (Evidence Object - EO):** Must cite verbatim spans from verified primary sources with timestamps/span hashes.
2. **Interpretation (Interpretation Object - IO):** Must present causal research questions and competing models ($H_1 \neq H_2$). Preserves uncertainty and contradiction.
3. **Knowledge (Knowledge Object - KO):** High-level transferable principles evaluated through multiple EOs and IOs. *Never created directly from raw source material.*

---

## 🔗 External Source Registration Protocol
- **Invariant:** `SOURCE_REFERENCE != EVIDENCE_OBJECT`. A source reference only identifies where evidence may exist.
- **Prohibited:** Never scrape YouTube/web pages automatically, never summarize from titles/descriptions/comments, never create EOs from URLs, and never create KOs from unverified references.
- **Protocol:**
  - Register metadata in `DATA_SOURCE`.
  - Check `workspace/inbox/` for verified primary text.
  - If text is missing, STOP at `WAITING_FOR_EVIDENCE` and request the user to deposit primary text.

---

## ⚖️ Human Review & Sovereignty Boundary
- **Zero Direct Excel Mutations:** Never write ad-hoc Python scripts to directly mutate `workspace/RIE_COMMAND_CENTER.xlsx`.
- **CANDIDATE Invariant:** All generated objects MUST have:
  - `Status = "CANDIDATE"`
  - `Human_Approval_State = "PENDING_LEVEL_5_REVIEW"`
  - `Canonical_Status = "NOT_APPROVED"`
- **Approval Privilege:** Only the Human Architect can ratify candidate transactions into canonical knowledge.

---

## 🎯 Command Reference
- Segment transcript: `python rie.py export-dul <file> --out <path>`
- Stage batch: `python rie.py stage-batch <batch_dir> --commit`
- Search knowledge graph: `python rie.py query "<keyword>"`
- Ratify candidate transaction: `python rie.py approve <tx_id>`
- Sync database and notes: `python rie.py sync --vault`
- Release Candidate Audit: `python rie.py rc-audit`

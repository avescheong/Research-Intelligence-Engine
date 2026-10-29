---
name: rie-ratify
description: Use this skill when reviewing, preparing, approving, or ratifying pending candidate knowledge objects.
---

# RIE Ratification Runbook

## Governing Invariant
> **AI creates candidates. RIE validates structure. Humans ratify canonical knowledge.**

AI agents can NEVER promote objects to CANONICAL on their own authority. Only the Human Architect can ratify candidate transactions into canonical knowledge.

---

## Workflow 1: Prepare Review Package ("RIE prepare this source for review")

When the user says:
> **"RIE prepare this source for review"** *(or "RIE summarize pending candidates")*

1. Inspect staged transactions in `workspace/transactions/` or open `workspace/RIE_COMMAND_CENTER.xlsx`.
2. Present a clear, structured summary to the Human Architect:
   - Transaction ID (`tx_id`)
   - Origin source and domain classification
   - Key Evidence Objects ($EO$) and verbatim citations
   - Competing Dialectical Hypotheses ($H_1$ vs. $H_2$) in Interpretation Objects ($IO$)
   - Proposed Knowledge Objects ($KO$) with calibrated confidence scores
   - Any active tension states or contradictions flagged by the contradiction engine

---

## Workflow 2: Executing Ratification ("RIE approve <tx_id>")

When the Human Architect approves the candidate transaction:
```bash
python rie.py approve <tx_id> --by "Human Architect"
```

### What This Does:
1. Promotes all candidate rows in `DATA_KO` belonging to `<tx_id>` from `CANDIDATE` to `CANONICAL`.
2. Flips `Human_Approval_State` to `APPROVED`.
3. Appends an audit decision row into `DATA_DECISION_LOG` (`DEC-RATIFY-<tx_id>`).
4. Re-synchronizes the downstream `rie_substrate.db` SQLite sidecar.

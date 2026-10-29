# Claude Code Project Memory for RIE Portable OS (v1.0.0)

See [AGENTS.md](./AGENTS.md) for core epistemic rules, constitutional laws, and the sovereign human boundary.

## Operational Law
> **Humans express intent. Antigravity/Claude Code operates the interface. RIE enforces deterministic epistemic governance.**

- **AI creates candidates:** All generated objects enter with `Status: CANDIDATE` and `Human_Approval_State: PENDING_LEVEL_5_REVIEW`.
- **Humans approve knowledge:** Only explicit human action promotes candidates to `CANONICAL` (`APPROVED`).
- **Epistemic Invariant:** `SOURCE_REFERENCE != EVIDENCE_OBJECT`. A URL or reference alone is never evidence.
- **Prohibited:** Never scrape YouTube/web pages automatically, never summarize from titles/descriptions/comments, never create EOs from URLs.

## Natural Intent Mapping
When the human user issues natural intent instructions, map them as follows:

- `"RIE ingest the new file in inbox"`:
  Scan `workspace/inbox/`, extract text, segment DUL, synthesize candidate EO/IO/KO/Relationships, validate through 24 gates, and stage with `--commit`.
- `"RIE register this YouTube source"` / `"RIE register this research paper source"`:
  Register metadata into `DATA_SOURCE`. If primary text is not in `workspace/inbox/`, stop at `WAITING_FOR_EVIDENCE` and prompt the user to deposit the primary text.
- `"RIE query everything about <topic>"`:
  Run `python rie.py query "<topic>"` to perform recursive graph walks.
- `"RIE prepare this source for review"`:
  Summarize staged candidate batches for Level 5 human review.
- `"RIE run diagnostics"`:
  Run `python rie.py doctor`.

## Key Desktop Commands (Tier 2 CLI)
- System health diagnosis: `python rie.py doctor`
- Export DUL from raw source: `python rie.py export-dul workspace/inbox/<file> --out <out.json>`
- Stage and validate AI batch: `python rie.py stage-batch <batch_dir> --commit`
- Search knowledge graph: `python rie.py query "<keyword>"`
- Ratify candidates into canonical: `python rie.py approve <tx_id>`
- Synchronize SQLite sidecar & Obsidian: `python rie.py sync --vault`
- 6-Gate Release Candidate Audit: `python rie.py rc-audit`

## Custom Slash Commands
Custom runbooks located in `.claude/commands/`:
- `/rie-ingest` — Ingestion runbook
- `/rie-ratify` — Human ratification runbook
- `/rie-query` — Graph traversal runbook
- `/rie-export-obsidian` — Vault compilation runbook
- `/rie-audit` — Health & RC audit runbook

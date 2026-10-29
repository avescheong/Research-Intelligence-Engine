---
name: rie-audit
description: Use this skill when checking system health, substrate parity, or running Release Candidate audits.
---

# RIE System & Release Candidate Audit Runbook

1. Check local environment and configuration:
   ```bash
   python rie.py doctor
   ```

2. Run the full 6-Gate Release Candidate Audit:
   ```bash
   python rie.py rc-audit
   ```

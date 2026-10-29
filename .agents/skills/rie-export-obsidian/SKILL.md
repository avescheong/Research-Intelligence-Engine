---
name: rie-export-obsidian
description: Use this skill when compiling the RIE Knowledge Base into an Obsidian Markdown vault.
---

# RIE Obsidian Vault Export Runbook

Execute 7-gate validated vault compilation:
```bash
python rie.py sync --vault
```

Atomic Markdown notes with bidirectional wikilinks will be compiled into `workspace/obsidian_vault/`.

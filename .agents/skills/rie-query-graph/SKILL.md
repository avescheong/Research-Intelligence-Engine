---
name: rie-query-graph
description: Use this skill when searching or traversing the RIE knowledge graph.
---

# RIE Knowledge Graph Query Runbook

## Natural Intent Command
> **"RIE query everything about <topic>"** *(e.g. "RIE query everything about liquidity")*

## Execution
Run multi-hop recursive queries against the SQLite sidecar:
```bash
python rie.py query "<keyword_or_ko_id>" --depth 3
```

## Results Returned
- Connected canonical and candidate Knowledge Objects ($KO$).
- Causal and dialectical relationship classifications.
- Evidentiary provenance and supporting evidence paths.

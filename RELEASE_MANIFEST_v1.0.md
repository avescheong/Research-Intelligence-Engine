# RIE Portable OS — Official Release Manifest (v1.0.0)

**Release Version:** `v1.0.0`  
**Release Date:** `2026-10-29`  
**Architecture:** 3-Layer Epistemic Sovereign Operating System  
**Tracked File Count:** 136 files  
**Third-Party Runtime Dependencies:** `openpyxl>=3.1.2` (Zero other pip packages)  

---

## 1. Release Inventory & Directory Specification
```text
RIE_PORTABLE_DESKTOP/
├── engine/
│   ├── core/           # [Layer 1] Pure Epistemic Kernel (Deterministic validation, DUL segmentation)
│   └── adapters/       # [Layer 2A] Concrete Storage Adapters (Excel, SQLite, Obsidian, AITG)
├── modules/            # [Layer 2B] Drop-In Domain Packs (example_education, example_investing)
├── workspace/          # [Layer 3] Human Knowledge Workspace (Inbox, Command Center Excel, Obsidian Vault)
├── templates/          # Immutable Clean-Slate Substrate Blueprints (rie init)
├── docs/               # Architecture Specification & Human User Guides
└── tests/              # 10 Test Suites + Automated RC-01..RC-06 Release Candidate Gate
```

---

## 2. Release Candidate Verification Status
- **RC-01 Structure Audit:** PASS (AST proof: Layer 1 has zero Layer 3 / storage imports)
- **RC-02 Security Audit:** PASS (Zero personal names, emails, Google Drive IDs, or cloud paths)
- **RC-03 Build Audit:** PASS (Template integrity, 20-sheet Excel XML validity, SQLite sidecar parity)
- **RC-04 Extension Audit:** PASS (Pluggable modules API, Antigravity skills, Claude Code commands)
- **RC-05 GitHub Audit:** PASS (.gitignore, LICENSE, README, CONTRIBUTING, Architecture Spec)
- **RC-06 Reproducibility:** PASS (Fresh clone / temp unzip first launch verified)

---

## 3. Legacy Cloud (000..007) Migration Cross-Reference
| Legacy Cloud Folder (v1.5) | Portable OS v1.0 Layout | Architectural Role |
| :--- | :--- | :--- |
| `000_READ_ME_FIRST` | `docs/` & `README.md` | Human user guides and epistemic constitution |
| `001_SOURCES` | `workspace/inbox/` | Raw text/markdown intake |
| `002_EVIDENCE_OBJECTS` | `workspace/transactions/` | Epistemic evidence staging |
| `004_HUMAN_GOVERNANCE` | `rie_config.json` & `docs/` | Configuration & constitutional laws |
| `005_CANONICAL_MEMORY` | `workspace/obsidian_vault/`| Compiled Obsidian notes vault |
| `006_ENGINE` | `engine/core/` & `adapters/` | 3-Layer Epistemic Engine & Adapters |
| `007_RIE_DASHBOARD` | `workspace/` | RIE_COMMAND_CENTER.xlsx & SQLite sidecar |

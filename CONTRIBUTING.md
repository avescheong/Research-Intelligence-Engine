# Contributing to RIE Portable OS

Thank you for contributing to RIE! RIE is designed with strict modularity so you can extend domain ontologies, add storage adapters, or author agent skills without modifying core engine logic.

---

## Architectural Ground Rules (Must Read Before Submitting PRs)

RIE enforces an **AST-verified 3-Layer Dependency Rule**:
1. **Layer 1 (`engine/core/`):** Pure epistemic algorithms and validator gates.
   - ⚠️ **NEVER** import `openpyxl`, `sqlite3`, `engine.adapters`, or reference `workspace/` inside `engine/core/`.
   - Core modules must accept Python data structures and return typed validation verdicts.
2. **Layer 2A (`engine/adapters/`):** Concrete storage, CLI, and MCP adapters.
   - All physical file I/O and storage mutations live here.
   - Storage writes must be atomic (e.g., using `tempfile` before replacing files).
3. **Layer 2B (`modules/`, `.agents/skills/`, `.claude/commands/`):**
   - Pluggable domain packs and agent runbooks.
   - Keep `.agents/skills/` as the single source of truth; `.claude/commands/` should remain thin wrappers.
4. **Layer 3 (`workspace/`):**
   - User workspace data is strictly ignored by Git. Never commit `.xlsx` or `.db` files from `workspace/` to Git.

---

## Adding a Custom Domain Pack

To add a new domain ontology:
1. Create a directory in `modules/<your_domain>/`
2. Add a `domain_module.json` file conforming to `engine/core/schemas/domain_module.schema.json`:
   ```json
   {
     "domain_id": "my_domain",
     "domain_code": "DOM",
     "display_name": "My Custom Domain",
     "description": "Domain description...",
     "enabled": true,
     "entity_keywords": ["keyword1", "keyword2"],
     "polarity_vectors": {"positive": ["gain"], "negative": ["loss"]},
     "research_question_templates": ["How does {entities} behave?"],
     "causal_h1_templates": ["H1: {entities} causes outcome."],
     "dialectical_h2_templates": ["H2: Alternative mechanism."],
     "concept_blueprints": []
   }
   ```
3. Run `python rie.py doctor` — your module will be auto-discovered and registered!

---

## Pre-PR Verification Checklist

Before submitting a pull request, run all automated checks:

```bash
# 1. Run unit test suites
python -m unittest discover -s tests -p "test_*.py" -v

# 2. Run the 6-Gate Release Candidate Audit
python rie.py rc-audit
```

Both commands must pass with 100% success.

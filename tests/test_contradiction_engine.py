import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path: sys.path.insert(0, str(REPO_ROOT))
#!/usr/bin/env python3
"""
UNIT TEST SUITE: CONTRADICTION ENGINE (PHASE 6B.3)
Directive Reference: RIE-DIR-L5-PHASE-6B-IMPLEMENTATION-REMEDIATION-v1.0
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 (Autonomous Repository Steward)
Classification: SYSTEM_TEST (REMEDIATION_V3_DEV)

Verifies:
1. Supporting evidence identification.
2. Conflicting evidence detection (direct empirical refutation and directional inversion).
3. Unknown / orthogonal relationship between unrelated EOs.
4. Unresolved contradiction handling: confidence depression (< 0.65) and status transition to CANDIDATE_UNRESOLVED_CONFLICT.
"""

import os
import sys
import unittest
from pathlib import Path

# Setup paths
CURRENT_DIR = Path(__file__).resolve().parent
DEV_DIR = CURRENT_DIR.parent
if str(DEV_DIR) not in sys.path:
    sys.path.insert(0, str(DEV_DIR))

from engine.core.contradiction_engine import ContradictionEngine, ContradictionType, ContradictionStatus
from engine.core.taxonomy_loader import TaxonomyLoader

class TestContradictionEngine(unittest.TestCase):
    def setUp(self):
        self.taxonomy = TaxonomyLoader()
        self.engine = ContradictionEngine(self.taxonomy)

    def test_01_supporting_evidence(self):
        """Verifies concordant evidence does not trigger contradiction."""
        eo_1 = {
            "EO_ID": "EO-MACRO-YIELD-001",
            "Direct_Observation": "Treasury bond yields rose sharply as sovereign debt issuance widened primary dealer spreads."
        }
        eo_2 = {
            "EO_ID": "EO-MACRO-YIELD-002",
            "Direct_Observation": "Primary dealer debt inventories expanded significantly while benchmark yields accelerated higher."
        }
        rel = self.engine.evaluate_contradiction_pair(eo_1, eo_2, "macroeconomics")
        if rel:
            self.assertNotEqual(rel["contradiction_type"], ContradictionType.DIRECT_EMPIRICAL_REFUTATION)
            self.assertTrue(rel["opposition_score"] < 0.65)

    def test_02_conflicting_evidence_direct_refutation(self):
        """Verifies opposing empirical claims trigger direct refutation."""
        eo_bullish = {
            "EO_ID": "EO-MACRO-YIELD-001",
            "Direct_Observation": "Treasury bond yields rose sharply as sovereign debt issuance widened clearing spreads."
        }
        eo_bearish = {
            "EO_ID": "EO-MACRO-YIELD-003",
            "Direct_Observation": "Treasury bond yields fell precipitously while secondary market debt spreads contracted."
        }
        rel = self.engine.evaluate_contradiction_pair(eo_bullish, eo_bearish, "macroeconomics")
        self.assertIsNotNone(rel)
        self.assertEqual(rel["contradiction_type"], ContradictionType.DIRECT_EMPIRICAL_REFUTATION)
        self.assertGreaterEqual(rel["opposition_score"], 0.70)
        self.assertTrue(any("yield" in e for e in rel["shared_entities"]))

    def test_03_unknown_relationship(self):
        """Verifies completely unrelated evidence across disparate concepts yields no contradiction."""
        eo_finance = {
            "EO_ID": "EO-MACRO-YIELD-001",
            "Direct_Observation": "Treasury bond yields rose sharply as sovereign debt issuance widened."
        }
        eo_weather = {
            "EO_ID": "EO-MISC-001",
            "Direct_Observation": "Acoustic bird chirping was observed outside the conference hall in the early morning."
        }
        rel = self.engine.evaluate_contradiction_pair(eo_finance, eo_weather, "macroeconomics")
        self.assertIsNone(rel)

    def test_04_unresolved_contradiction_and_confidence_penalty(self):
        """Verifies that unresolved contradictions depress confidence below 0.65 and mark UNRESOLVED_CONFLICT."""
        conf, status = self.engine.calculate_dialectic_confidence(
            supporting_count=1,
            contradicting_count=2,
            dialectical_cosine=0.45,
            base_confidence=0.88
        )
        self.assertLess(conf, 0.65)
        self.assertEqual(status, ContradictionStatus.CANDIDATE_UNRESOLVED_CONFLICT)

    def test_05_tension_state_with_minor_contradiction(self):
        """Verifies that minor contradiction puts IO in CANDIDATE_UNDER_TENSION without dropping below 0.65."""
        conf, status = self.engine.calculate_dialectic_confidence(
            supporting_count=3,
            contradicting_count=1,
            dialectical_cosine=0.35,
            base_confidence=0.88
        )
        self.assertGreaterEqual(conf, 0.65)
        self.assertEqual(status, ContradictionStatus.CANDIDATE_UNDER_TENSION)

    def test_06_environmental_domain_contradiction(self):
        """Verifies contradiction engine functions on non-financial domain (environmental)."""
        eo_env_exceed = {
            "EO_ID": "EO-ENV-TSS-001",
            "Direct_Observation": "Monsoon runoff discharge exceeded statutory TSS thresholds and silt basin overflowed."
        }
        eo_env_settled = {
            "EO_ID": "EO-ENV-TSS-002",
            "Direct_Observation": "Suspended sediment settled rapidly and runoff discharge decreased below statutory limits."
        }
        rel = self.engine.evaluate_contradiction_pair(eo_env_exceed, eo_env_settled, "environmental_engineering")
        self.assertIsNotNone(rel)
        self.assertEqual(rel["contradiction_type"], ContradictionType.DIRECT_EMPIRICAL_REFUTATION)
        self.assertIn("runoff", rel["shared_entities"])

if __name__ == "__main__":
    unittest.main()

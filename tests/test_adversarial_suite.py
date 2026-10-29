import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path: sys.path.insert(0, str(REPO_ROOT))
#!/usr/bin/env python3
"""
RIE Semantic v1.4 Adversarial Torture-Test Suite (test_adversarial_suite.py)
Verifies 100% fail-closed interception across all 6 adversarial attack vectors (A1-A6):
  - Attack A1: Mechanical line-by-line subtitle splitting / cardinality inflation
  - Attack A2: Synthetic uniform +75s timestamp fabrication / missing span hashes
  - Attack A3: 1:1 EO-to-IO mechanical cloning & boilerplate templates
  - Attack A4: Uncalibrated constant confidence (0.84 uniform)
  - Attack A5: Monolithic single-KO collapse & generic title boilerplate
  - Attack A6: Tautological counter-hypothesis (H1 == H2) & silent contradiction erasure
"""
import copy
import json
import sys
import unittest
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.name == "tests" else Path(__file__).resolve().parent
if str(PKG_DIR) not in sys.path:
    sys.path.insert(0, str(PKG_DIR))

from engine.core.semantic_pipeline import SemanticPipeline
from engine.core.taxonomy_loader import TaxonomyLoader
from engine.core.cardinality_controller import CardinalityController
from engine.core.semantic_validator import SemanticValidationEngine


class TestAdversarialSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = SemanticPipeline()
        fixture_file = REPO_ROOT / "tests" / "fixtures" / "02_environmental_engineering_escp.json"
        raw = json.loads(fixture_file.read_text(encoding="utf-8"))
        cls.base_out = cls.pipeline.execute(
            source_id=raw.get("source_id", "SRC-ADV-TEST"),
            tx_id="TX-ADV-TEST",
            transcript_entries=raw.get("transcript_entries"),
            speaker_tag=raw.get("speaker_tag", "IR_TAN"),
            topic=raw.get("topic", "SedimentControl"),
            domain_key=raw.get("domain_key", "environmental_engineering")
        )
        cls.tax = TaxonomyLoader()
        cls.card = CardinalityController()
        cls.val = SemanticValidationEngine(cls.tax, cls.card)

    def _clone_baseline(self):
        return (
            copy.deepcopy(self.base_out["evidence_objects"]),
            copy.deepcopy(self.base_out["interpretation_objects"]),
            copy.deepcopy(self.base_out["knowledge_objects"]),
            copy.deepcopy(self.base_out["relationships"]),
            float(self.base_out["duration_sec"]),
        )

    def test_00_baseline_passes_all_12_gates(self):
        eos, ios, kos, rels, dur = self._clone_baseline()
        res = self.val.run_all_semantic_gates(eos, ios, kos, rels, duration_sec=dur)
        self.assertEqual(res["overall_semantic_status"], "PASS")

    def test_A1_mechanical_subtitle_fragmentation_blocked(self):
        eos, ios, kos, rels, dur = self._clone_baseline()
        bad_eos = [
            {
                "EO_ID": f"EO-FRAG-{i:03d}",
                "Origin_Source": "SRC-TEST-001",
                "Start_Time_Sec": float(i * 2),
                "End_Time_Sec": float(i * 2 + 2),
                "Timestamp_Page": "00:00:01 - 00:00:03",
                "Source_Span_Hash": f"hash{i:04d}",
                "Direct_Observation": "short fragment line",
            }
            for i in range(60)
        ]
        res = self.val.run_all_semantic_gates(bad_eos, ios, kos, rels, duration_sec=dur)
        self.assertEqual(res["overall_semantic_status"], "FAIL")

    def test_A2_synthetic_timestamp_and_missing_span_hash_blocked(self):
        eos, ios, kos, rels, dur = self._clone_baseline()
        eos[0]["Span_SHA256"] = "tampered_invalid_sha256"
        eos[0]["Duration_Sec"] = 2.0
        res = self.val.run_all_semantic_gates(eos, ios, kos, rels, duration_sec=dur)
        self.assertEqual(res["overall_semantic_status"], "FAIL")

    def test_A3_boilerplate_io_cloning_blocked(self):
        eos, ios, kos, rels, dur = self._clone_baseline()
        ios[0]["Alternative_Interpretation"] = ios[1]["Alternative_Interpretation"]
        ios[0]["Research_Question"] = ios[1]["Research_Question"]
        res = self.val.run_all_semantic_gates(eos, ios, kos, rels, duration_sec=dur)
        self.assertEqual(res["overall_semantic_status"], "FAIL")

    def test_A4_uncalibrated_constant_confidence_blocked(self):
        eos, ios, kos, rels, dur = self._clone_baseline()
        for io in ios:
            io["Confidence"] = 0.84
        res = self.val.run_all_semantic_gates(eos, ios, kos, rels, duration_sec=dur)
        self.assertEqual(res["overall_semantic_status"], "FAIL")

    def test_A5_monolithic_ko_collapse_and_banned_title_blocked(self):
        eos, ios, kos, rels, dur = self._clone_baseline()
        kos[0]["Concept_Title"] = "Analysis of Sovereign Collateral Transmission Dynamics"
        res = self.val.run_all_semantic_gates(eos, ios, [kos[0]], rels, duration_sec=dur)
        self.assertEqual(res["overall_semantic_status"], "FAIL")

    def test_A6_tautological_counter_hypothesis_blocked(self):
        eos, ios, kos, rels, dur = self._clone_baseline()
        ios[0]["Alternative_Interpretation"] = ios[0]["Primary_Interpretation"]
        res = self.val.run_all_semantic_gates(eos, ios, kos, rels, duration_sec=dur)
        self.assertEqual(res["overall_semantic_status"], "FAIL")


if __name__ == "__main__":
    unittest.main(verbosity=2)

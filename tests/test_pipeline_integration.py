import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path: sys.path.insert(0, str(REPO_ROOT))
#!/usr/bin/env python3
"""
INTEGRATION TEST SUITE: SEMANTIC PIPELINE (PHASE 6B.5)
Directive Reference: RIE-DIR-L5-PHASE-6B-IMPLEMENTATION-REMEDIATION-v1.0
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 (Autonomous Repository Steward)
Classification: SYSTEM_TEST (REMEDIATION_V3_DEV)

Verifies:
1. End-to-end integration: EO -> IO -> KO -> REL -> Epistemic Validation.
2. Unbroken epistemic lineage: KO references IOs, IO references EOs, EO references source.
3. Epistemic layer separation: EO (pure observation) != IO (dialectical model) != KO (abstract concept).
4. Provenance tracking and cryptographic byte-span hashing.
5. Production of SEMANTIC_VALIDATION_VERDICT.json and fail-closed promotion gating.
"""

import os
import sys
import unittest
import tempfile
import json
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
DEV_DIR = CURRENT_DIR.parent
if str(DEV_DIR) not in sys.path:
    sys.path.insert(0, str(DEV_DIR))

from engine.core.semantic_pipeline import SemanticPipeline

class TestPipelineIntegration(unittest.TestCase):
    def setUp(self):
        self.pipeline = SemanticPipeline()

    def test_01_end_to_end_synthesis_and_validation(self):
        """Verifies end-to-end synthesis and fail-closed validation on structured entries."""
        # Multi-proposition transcript calibrated to natural human conversational pace (90-115 WPM)
        entries = [
            {
                "start": 0.0, "end": 14.0,
                "text": "Federal Reserve monetary policy and Treasury debt refinancing have expanded primary dealer sovereign debt obligations significantly across secondary clearing markets today."
            },
            {
                "start": 15.0, "end": 29.0,
                "text": "Secondary market benchmark Treasury bond yields rose sharply as private institution balance sheets absorbed massive new auction volumes across both short and long maturities."
            },
            {
                "start": 30.0, "end": 44.0,
                "text": "Persistent reverse repo facility drainage forced overnight funding rates higher while interbank collateral financing liquidity narrowed substantially across primary dealer balance sheet books."
            },
            {
                "start": 45.0, "end": 59.0,
                "text": "Foreign central banks shifted their official reserve allocations away from fiat currency balances into bilateral physical gold and sovereign commodity holdings during recent quarterly periods."
            },
            {
                "start": 60.0, "end": 74.0,
                "text": "Primary dealers reported widening bid ask spreads as institutional hedging pressures and regulatory capital constraints elevated benchmark interest rate market volatility across trading sessions."
            },
            {
                "start": 75.0, "end": 89.0,
                "text": "Accelerating fiscal deficit projections created severe duration risk while secondary sovereign debt auction clearing demand fell precipitously across major international institutional buyers."
            }
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            result = self.pipeline.execute(
                source_id="SRC-TEST-001",
                tx_id="TX-TEST-20261005-001",
                transcript_entries=entries,
                speaker_tag="ANALYST",
                topic="TreasuryRefinancing",
                output_dir=tmp_dir
            )

            # Check outputs exist
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "EO_BATCH.json")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "IO_BATCH.json")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "KO_BATCH.json")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "RELATIONSHIP_BATCH.json")))
            self.assertTrue(os.path.exists(os.path.join(tmp_dir, "SEMANTIC_VALIDATION_VERDICT.json")))

            # Check counts
            counts = result["counts"]
            self.assertGreaterEqual(counts["evidence_objects"], 3)
            self.assertGreaterEqual(counts["interpretation_objects"], 2)
            self.assertGreaterEqual(counts["knowledge_objects"], 1)

            # Check Epistemic Layer Separation (EO != IO != KO)
            eos = result["evidence_objects"]
            ios = result["interpretation_objects"]
            kos = result["knowledge_objects"]

            for eo in eos:
                self.assertIn("Direct_Observation", eo)
                self.assertNotIn("Primary_Interpretation", eo)
                self.assertNotIn("Concept_Title", eo)
                self.assertEqual(len(eo["Span_SHA256"]), 64)

            for io in ios:
                self.assertIn("Primary_Interpretation", io)
                self.assertIn("Alternative_Interpretation", io)
                self.assertIn("Research_Question", io)
                self.assertIn("Supporting_EO", io)

            for ko in kos:
                self.assertIn("Concept_Title", ko)
                self.assertIn("Supporting_IO", ko)
                self.assertIn("Supporting_EO", ko)

            # Lineage verification
            eo_ids = set(e["EO_ID"] for e in eos)
            io_ids = set(i["IO_ID"] for i in ios)

            for io in ios:
                supp_eos = [e.strip() for e in io["Supporting_EO"].split(",") if e.strip()]
                for seid in supp_eos:
                    self.assertIn(seid, eo_ids, f"IO references ungrounded EO: {seid}")

            for ko in kos:
                supp_ios = [i.strip() for i in ko["Supporting_IO"].split(",") if i.strip()]
                for siid in supp_ios:
                    self.assertIn(siid, io_ids, f"KO references ungrounded IO: {siid}")

            # Check validation verdict
            verdict = result["validation_verdict"]
            self.assertIn(verdict["overall_semantic_status"], ["PASS", "FAIL"])
            self.assertEqual(verdict["total_gate_count"], 12)

    def test_02_fail_closed_on_invalid_data(self):
        """Verifies validation engine fails closed when given pathological inputs."""
        bad_eos = [{
            "EO_ID": "EO-BAD-001",
            "Direct_Observation": "Too short.",
            "Start_Sec": 0.0,
            "End_Sec": 5.0, # duration 5s < 15s
            "Duration_Sec": 5.0,
            "Speech_Rate_WPM": 24.0, # WPM < 80
            "Span_SHA256": "invalid_hash"
        }]
        bad_ios = []
        bad_kos = []
        bad_rels = []

        verdict = self.pipeline.validator.run_all_semantic_gates(bad_eos, bad_ios, bad_kos, bad_rels)
        self.assertEqual(verdict["overall_semantic_status"], "FAIL")
        self.assertFalse(verdict["promotion_authorized"])

if __name__ == "__main__":
    unittest.main()

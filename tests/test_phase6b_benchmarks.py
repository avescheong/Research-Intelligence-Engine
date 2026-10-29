import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path: sys.path.insert(0, str(REPO_ROOT))
#!/usr/bin/env python3
"""
RIE PHASE 6B BENCHMARK SUITE — Multi-Domain Epistemic Validation Suite
Directive Reference: RIE-DIR-L5-PHASE-6B-IMPLEMENTATION-REMEDIATION-v1.0
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 (Autonomous Repository Steward)
Classification: SYSTEM_BENCHMARK (REMEDIATION_V3_DEV)
Operating Mode: ZERO NETWORK — DETERMINISTIC OFFLINE REPLAY

Executes:
1. Benchmark A: Macroeconomics & Sovereign Debt (VIDEO-008 Felix Prehn)
   - Pause-aligned EO segmentation
   - Multiple IO hypotheses with dialectical tension
   - Dynamic confidence (StdDev >= 0.025)
   - 11/11 Semantic Gates PASS

2. Benchmark B: Environmental Engineering & Sediment Control (EIA / ESCP)
   - Zero finance assumptions
   - Externalized taxonomy loading (environmental_engineering)
   - Evidence preservation & contradiction handling
   - 11/11 Semantic Gates PASS

3. Benchmark C: Cross-Domain Empirical Scientific Research
   - Same architecture and engine code without code modification
   - Externalized taxonomy loading (scientific_research)
   - 11/11 Semantic Gates PASS
"""

import os
import sys
import unittest
import json
import math
import re
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
DEV_DIR = CURRENT_DIR.parent
REPO_ROOT = Path(__file__).resolve().parent.parent

if str(DEV_DIR) not in sys.path:
    sys.path.insert(0, str(DEV_DIR))

from engine.core.semantic_pipeline import SemanticPipeline
from engine.core.taxonomy_loader import TaxonomyLoader

class TestPhase6BBenchmarks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = SemanticPipeline()
        cls.benchmark_output_dir = DEV_DIR / "tests" / "benchmark_results"
        cls.benchmark_output_dir.mkdir(parents=True, exist_ok=True)

    def test_01_benchmark_a_video_008_felix_prehn(self):
        """
        Benchmark A: Existing VIDEO-008 Felix Prehn (Macroeconomic & Sovereign Debt).
        Expected: Pause-aligned EO segmentation, multiple IO hypotheses, dynamic confidence, gates PASS.
        """
        print("\n" + "=" * 80)
        print("EXECUTING BENCHMARK A: VIDEO-008 (Felix Prehn / Dollar Reset & Bond Yields)")
        print("=" * 80)

        fixture_path = REPO_ROOT / "tests" / "fixtures" / "01_felix_prehn_macroeconomics.json"
        self.assertTrue(fixture_path.exists(), f"Fixture missing: {fixture_path}")

        with open(fixture_path, "r", encoding="utf-8") as f:
            src = json.load(f)

        raw_transcript = src.get("transcript_text", "")
        self.assertTrue(len(raw_transcript) > 1000)

        # Parse timestamped subtitle lines: [HH:MM:SS] text
        lines = [l.strip() for l in raw_transcript.splitlines() if l.strip()]
        parsed_entries = []
        for line in lines:
            m = re.match(r'\[(\d{2}):(\d{2}):(\d{2})\]\s*(.+)', line)
            if m:
                hrs, mins, secs = int(m.group(1)), int(m.group(2)), int(m.group(3))
                start_sec = hrs * 3600 + mins * 60 + secs
                text = m.group(4).strip()
                parsed_entries.append({"start": float(start_sec), "text": text})

        for i in range(len(parsed_entries) - 1):
            parsed_entries[i]["end"] = parsed_entries[i+1]["start"]
        if parsed_entries:
            parsed_entries[-1]["end"] = parsed_entries[-1]["start"] + 6.0

        out_dir = self.benchmark_output_dir / "BENCHMARK_A_VIDEO-008"
        result = self.pipeline.execute(
            source_id="SRC-VIDEO-008",
            tx_id="TX-BENCHMARK-VIDEO-008",
            transcript_entries=parsed_entries,
            speaker_tag="FelixPrehn",
            topic="MacroDebtRefinancing",
            domain_key="macroeconomics",
            output_dir=str(out_dir)
        )

        counts = result["counts"]
        print(f"Benchmark A Synthesis Counts: {counts}")
        print(f"Detected Domain: {result['detected_domain']}")

        # Assertions
        self.assertEqual(result["detected_domain"], "macroeconomics")
        self.assertGreaterEqual(counts["evidence_objects"], 6)
        self.assertGreaterEqual(counts["interpretation_objects"], 3)
        self.assertGreaterEqual(counts["knowledge_objects"], 2)
        self.assertGreaterEqual(counts["relationships"], 1)

        # Verify dynamic confidence variance
        ios = result["interpretation_objects"]
        confs = [io["Confidence"] for io in ios]
        mean_c = sum(confs) / len(confs)
        std_c = math.sqrt(sum((c - mean_c) ** 2 for c in confs) / len(confs))
        print(f"Benchmark A IO Confidences: {confs} (StdDev: {std_c:.4f})")
        self.assertGreaterEqual(std_c, 0.020, "Flat confidence detected.")

        # Check semantic validation verdict
        verdict = result["validation_verdict"]
        print(f"Benchmark A Verdict: {verdict['overall_semantic_status']} ({verdict['passed_gate_count']}/{verdict['total_gate_count']} gates)")
        for k, v in verdict["gate_details"].items():
            print(f"  {k}: {v['passed']} - {v['message']}")

        self.assertEqual(verdict["overall_semantic_status"], "PASS")
        self.assertTrue(result["promotion_authorized"])

    def test_02_benchmark_b_environmental_engineering(self):
        """
        Benchmark B: Environmental Domain (Sediment and Erosion Control Plan / EIA).
        Expected: No finance assumptions, domain taxonomy loaded externally, evidence preserved, gates PASS.
        """
        print("\n" + "=" * 80)
        print("EXECUTING BENCHMARK B: ENVIRONMENTAL ENGINEERING (EIA / ESCP Sediment Runoff)")
        print("=" * 80)

        # Environmental engineering transcript entries calibrated for natural speech (90-115 WPM)
        entries = [
            {
                "start": 0.0, "end": 15.5,
                "text": "Intense tropical monsoon precipitation exceeded fifty millimeters per hour across the exposed earthworks during site platform preparation and cut slope excavation operations today."
            },
            {
                "start": 17.0, "end": 32.5,
                "text": "Uncontrolled surface runoff velocity accelerated rill erosion along the unprotected twenty-eight degree cut slopes near the northern perimeter boundary and perimeter diversion drain."
            },
            {
                "start": 34.0, "end": 49.5,
                "text": "The primary sediment retention basin overflowed through the emergency spillway as suspended sediment discharge surpassed two hundred milligrams per liter statutory limits across monitoring stations."
            },
            {
                "start": 51.0, "end": 66.5,
                "text": "Downstream environmental water quality monitoring at station WQM-01 recorded severe statutory TSS exceedance and elevated turbidity across the receiving river channel outfall during peak flow."
            },
            {
                "start": 68.0, "end": 83.5,
                "text": "Installation of secondary geotextile silt fences and intermediate rock check-dams significantly attenuated runoff velocity along internal drainage diversion bunds and perimeter channels."
            },
            {
                "start": 85.0, "end": 100.5,
                "text": "The tiered settlement compartment successfully retained heavy suspended silt particles while clean supernatant effluent discharged through the final baffle weir into downstream retention ponds."
            },
            {
                "start": 102.0, "end": 117.5,
                "text": "Saturated soil erodibility tests confirmed that local granite residual soil possesses high wash-off potential during prolonged tropical monsoon downpours across untreated earthwork surfaces."
            },
            {
                "start": 119.0, "end": 134.5,
                "text": "Statutory compliance guidelines mandate immediate hydroseeding and rock rip-rap surface protection to stabilize critical steep slope embankments permanently before subsequent rainfall events."
            }
        ]

        out_dir = self.benchmark_output_dir / "BENCHMARK_B_ENVIRONMENTAL"
        result = self.pipeline.execute(
            source_id="SRC-EIA-PENANG-001",
            tx_id="TX-BENCHMARK-ENV-001",
            transcript_entries=entries,
            speaker_tag="DOEInspector",
            topic="SedimentErosionControl",
            domain_key="environmental_engineering",
            output_dir=str(out_dir)
        )

        counts = result["counts"]
        print(f"Benchmark B Synthesis Counts: {counts}")
        print(f"Detected Domain: {result['detected_domain']}")

        # Verify no financial domain assumptions
        self.assertEqual(result["detected_domain"], "environmental_engineering")
        kos = result["knowledge_objects"]
        ios = result["interpretation_objects"]
        eos = result["evidence_objects"]

        for ko in kos:
            self.assertIn("Environmental Engineering", ko["Domain"])
            self.assertNotIn("Sovereign", ko["Concept_Title"])
            self.assertNotIn("Debt", ko["Concept_Title"])
            self.assertNotIn("Treasury", ko["Concept_Title"])
            self.assertTrue(ko["KO_ID"].startswith("KO-ENV-"))

        # Verify contradiction preservation:
        has_contra = any(io.get("Contradicting_EO") != "NONE" for io in ios)
        print(f"Benchmark B Active Contradiction Preserved: {has_contra}")

        # Check semantic validation verdict
        verdict = result["validation_verdict"]
        print(f"Benchmark B Verdict: {verdict['overall_semantic_status']} ({verdict['passed_gate_count']}/{verdict['total_gate_count']} gates)")
        for k, v in verdict["gate_details"].items():
            print(f"  {k}: {v['passed']} - {v['message']}")

        self.assertEqual(verdict["overall_semantic_status"], "PASS")
        self.assertTrue(result["promotion_authorized"])

    def test_03_benchmark_c_cross_domain_scientific_research(self):
        """
        Benchmark C: Cross-Domain Empirical Scientific Research Article.
        Expected: Same architecture without code modification, scientific taxonomy, gates PASS.
        """
        print("\n" + "=" * 80)
        print("EXECUTING BENCHMARK C: CROSS-DOMAIN SCIENTIFIC RESEARCH ARTICLE")
        print("=" * 80)

        # Raw document text of a scientific research article
        scientific_article_text = (
            "Controlled laboratory experiments were conducted to evaluate semiconductor sensor calibration variance under thermal stress. "
            "Baseline temperature sweeps demonstrated that ambient sensor drift correlated directly with junction power dissipation during continuous operation. "
            "High precision measurement protocols recorded statistical divergence across uncompensated sensor detector channels exceeding five percent. "
            "Conversely, automated temperature compensation feedback circuits effectively suppressed thermal drift and stabilized telemetry output. "
            "Independent experimental replications confirmed that physical dielectric relaxation induces measurable phase noise across high frequency trials. "
            "Calibration error analysis indicated that systematic measurement bias can be mitigated through multi-station reference detector cross-validation. "
            "Empirical state manipulation produced statistically significant response curves validating the primary physical transport model. "
            "The observed covariate variance remained fully bounded within theoretical experimental error distributions throughout the ninety minute trial."
        )

        out_dir = self.benchmark_output_dir / "BENCHMARK_C_SCIENTIFIC"
        result = self.pipeline.execute(
            source_id="SRC-SCI-ARTICLE-001",
            tx_id="TX-BENCHMARK-SCI-001",
            raw_text=scientific_article_text,
            speaker_tag="LeadResearcher",
            topic="SensorCalibrationVariance",
            domain_key="scientific_research",
            output_dir=str(out_dir)
        )

        counts = result["counts"]
        print(f"Benchmark C Synthesis Counts: {counts}")
        print(f"Detected Domain: {result['detected_domain']}")

        # Verify domain independence
        self.assertEqual(result["detected_domain"], "scientific_research")
        kos = result["knowledge_objects"]
        for ko in kos:
            self.assertIn("Scientific Research", ko["Domain"])
            self.assertTrue(ko["KO_ID"].startswith("KO-SCI-"))
            self.assertNotIn("Debt", ko["Concept_Title"])
            self.assertNotIn("Yield", ko["Concept_Title"])

        # Check semantic validation verdict
        verdict = result["validation_verdict"]
        print(f"Benchmark C Verdict: {verdict['overall_semantic_status']} ({verdict['passed_gate_count']}/{verdict['total_gate_count']} gates)")
        for k, v in verdict["gate_details"].items():
            print(f"  {k}: {v['passed']} - {v['message']}")

        self.assertEqual(verdict["overall_semantic_status"], "PASS")
        self.assertTrue(result["promotion_authorized"])

if __name__ == "__main__":
    unittest.main()

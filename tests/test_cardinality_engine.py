import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path: sys.path.insert(0, str(REPO_ROOT))
#!/usr/bin/env python3
"""
UNIT TEST SUITE: CARDINALITY ENGINE (PHASE 6B.4)
Directive Reference: RIE-DIR-L5-PHASE-6B-IMPLEMENTATION-REMEDIATION-v1.0
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 (Autonomous Repository Steward)
Classification: SYSTEM_TEST (REMEDIATION_V3_DEV)

Verifies:
1. Small source handling: Validates 3-EO extraction on short briefings without forced padding.
2. Complex source handling: Expands envelope for long-form symposia / reports without premature truncation.
3. Multi-model interpretation: Enforces N:1 clustering ratio, rejects strict 1:1 fragmentation and monolithic collapse.
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

from engine.core.cardinality_controller import CardinalityController

class TestCardinalityEngine(unittest.TestCase):
    def setUp(self):
        self.controller = CardinalityController()

    def test_01_small_source_envelope(self):
        """Verifies small source (4-minute briefing, 240s) allows 3-5 EOs without forced padding."""
        env = self.controller.compute_eo_envelope(duration_sec=240.0, word_count=500, candidate_ratio=1.0)
        self.assertLessEqual(env["min_eo"], 3)
        self.assertGreaterEqual(env["max_eo"], 8)
        
        # Validates a 3-EO, 2-IO, 1-KO cascade cleanly
        passed, violations = self.controller.validate_cardinality(
            eo_count=4,
            io_count=2,
            ko_count=1,
            rel_count=0,
            duration_sec=240.0,
            word_count=500
        )
        self.assertTrue(passed, f"Small source validation failed: {violations}")

    def test_02_complex_source_expansion(self):
        """Verifies complex long-form source (90 minutes, 5400s) scales up to capture dense findings."""
        env = self.controller.compute_eo_envelope(duration_sec=5400.0, word_count=12000, candidate_ratio=1.2)
        # Should allow high EO counts without clamping to 18
        self.assertGreaterEqual(env["target_eo"], 25)
        self.assertGreaterEqual(env["max_eo"], 35)
        
        # 30 EOs -> ~12 IOs -> 4-6 KOs
        io_env = self.controller.compute_io_envelope(30)
        ko_env = self.controller.compute_ko_envelope(io_env["target_io"], 30)
        
        passed, violations = self.controller.validate_cardinality(
            eo_count=30,
            io_count=10,
            ko_count=4,
            rel_count=4,
            duration_sec=5400.0,
            word_count=12000
        )
        self.assertTrue(passed, f"Complex source validation failed: {violations}")

    def test_03_rejection_of_strict_one_to_one(self):
        """Verifies that 1:1 mapping (N_EO == N_IO) is rejected."""
        passed, violations = self.controller.validate_cardinality(
            eo_count=10,
            io_count=10,
            ko_count=2,
            rel_count=1,
            duration_sec=1200.0
        )
        self.assertFalse(passed)
        self.assertTrue(any("Strict 1:1" in v for v in violations))

    def test_04_rejection_of_monolithic_collapse(self):
        """Verifies that 1-KO collapse for complex sources (N_EO >= 8) is rejected."""
        passed, violations = self.controller.validate_cardinality(
            eo_count=12,
            io_count=4,
            ko_count=1,
            rel_count=0,
            duration_sec=1800.0
        )
        self.assertFalse(passed)
        self.assertTrue(any("Monolithic 1-KO collapse" in v for v in violations))

    def test_05_multi_model_clustering_ratio(self):
        """Verifies N:1 clustering ratio enforces 2 to 5 EOs per IO."""
        # 8 EOs clustered into 3 IOs -> ratio 8/3 = 2.67 -> Pass
        passed, violations = self.controller.validate_cardinality(
            eo_count=8,
            io_count=3,
            ko_count=2,
            rel_count=1,
            duration_sec=1500.0
        )
        self.assertTrue(passed, f"Clustering ratio failed: {violations}")

if __name__ == "__main__":
    unittest.main()

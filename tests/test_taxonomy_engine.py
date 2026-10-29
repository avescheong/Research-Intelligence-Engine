import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path: sys.path.insert(0, str(REPO_ROOT))
#!/usr/bin/env python3
"""
UNIT TEST SUITE: TAXONOMY ENGINE (PHASE 6B.2)
Directive Reference: RIE-DIR-L5-PHASE-6B-IMPLEMENTATION-REMEDIATION-v1.0
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 (Autonomous Repository Steward)
Classification: SYSTEM_TEST (REMEDIATION_V3_DEV)

Verifies:
1. Loading baseline taxonomy from JSON.
2. Dynamic addition of a new domain (e.g. quantum_computing).
3. Dynamic removal of a domain.
4. Dynamic modification of taxonomy attributes.
5. Domain detection and engine adaptation without modifying core code.
"""

import os
import sys
import unittest
import tempfile
import json
from pathlib import Path

# Setup paths
CURRENT_DIR = Path(__file__).resolve().parent
DEV_DIR = CURRENT_DIR.parent
if str(DEV_DIR) not in sys.path:
    sys.path.insert(0, str(DEV_DIR))

from engine.core.taxonomy_loader import TaxonomyLoader, DEFAULT_TAXONOMY_PATH

class TestTaxonomyEngine(unittest.TestCase):
    def setUp(self):
        self.loader = TaxonomyLoader(DEFAULT_TAXONOMY_PATH)

    def test_01_baseline_load(self):
        """Verifies baseline domains load correctly."""
        domains = self.loader.list_domains()
        self.assertIn("macroeconomics", domains)
        self.assertIn("environmental_engineering", domains)
        self.assertIn("drone_photogrammetry", domains)
        self.assertIn("scientific_research", domains)
        
        macro = self.loader.get_domain("macroeconomics")
        self.assertEqual(macro["domain_code"], "MACRO")
        self.assertTrue(len(macro["entity_keywords"]) > 10)

    def test_02_add_new_domain(self):
        """Verifies dynamic addition of a new domain without code modification."""
        new_domain = {
            "domain_id": "quantum_computing",
            "domain_code": "QCOMP",
            "display_name": "Quantum Computing & Information Architecture",
            "description": "Superconducting qubits, quantum decoherence, error mitigation, and quantum teleportation.",
            "entity_keywords": ["qubit", "superposition", "entanglement", "decoherence", "teleportation", "hamiltonian"],
            "polarity_vectors": {
                "positive": ["coherent", "entangled", "amplified", "suppressed_error"],
                "negative": ["decohered", "attenuated", "decayed", "erred"]
            },
            "research_question_templates": ["How does empirical phase noise in {entities} degrade logical gate fidelity?"],
            "causal_h1_templates": ["Primary Model (H1): Environmental thermal fluctuations (Root Trigger) induce dielectric relaxation in {entities} (Transmission Mechanism), producing qubit state decoherence (Observable Outcome)."],
            "dialectical_h2_templates": ["Competing Model (H2): Observable gate errors stem from control pulse calibration jitter rather than physical thermal dissipation."],
            "concept_blueprints": [{
                "slug": "DECOHERENCE-SUPPRESSION",
                "title": "Quantum Error Mitigation and Dynamic Decoupling Mechanics",
                "subtopic": "Qubit Fidelity",
                "cluster": "CLUSTER_QUANTUM_COHERENCE"
            }]
        }
        self.loader.add_domain("quantum_computing", new_domain)
        self.assertIn("quantum_computing", self.loader.list_domains())
        
        retrieved = self.loader.get_domain("quantum_computing")
        self.assertEqual(retrieved["domain_code"], "QCOMP")
        
        # Test detection for new domain
        sample_text = "The superconducting qubit experienced rapid decoherence and loss of quantum entanglement."
        detected = self.loader.detect_domain_from_text(sample_text)
        self.assertEqual(detected, "quantum_computing")

    def test_03_remove_domain(self):
        """Verifies dynamic removal of a domain."""
        # Add temporary domain then remove
        temp_domain = {
            "domain_id": "temp_domain",
            "domain_code": "TEMP",
            "display_name": "Temporary Test Domain",
            "entity_keywords": ["temporary", "transient"]
        }
        self.loader.add_domain("temp_domain", temp_domain)
        self.assertIn("temp_domain", self.loader.list_domains())
        
        removed = self.loader.remove_domain("temp_domain")
        self.assertTrue(removed)
        self.assertNotIn("temp_domain", self.loader.list_domains())

    def test_04_modify_taxonomy(self):
        """Verifies modification of existing taxonomy definitions."""
        self.loader.modify_domain("drone_photogrammetry", {
            "display_name": "UAV Remote Sensing and Advanced Aerial Photogrammetry",
            "test_flag": "MODIFIED_IN_MEMORY"
        })
        drone = self.loader.get_domain("drone_photogrammetry")
        self.assertEqual(drone["display_name"], "UAV Remote Sensing and Advanced Aerial Photogrammetry")
        self.assertEqual(drone.get("test_flag"), "MODIFIED_IN_MEMORY")

    def test_05_engine_adapts_without_code_change(self):
        """Verifies engine behaviour changes through taxonomy input only."""
        # Environmental text detection
        env_text = "The sediment basin overflowed during intense rainfall, discharging silt into the stream with high turbidity."
        d_env = self.loader.detect_domain_from_text(env_text)
        self.assertEqual(d_env, "environmental_engineering")
        
        # Macro text detection
        macro_text = "Federal reserve reverse repo drain widened Treasury yield spreads and elevated primary dealer debt."
        d_macro = self.loader.detect_domain_from_text(macro_text)
        self.assertEqual(d_macro, "macroeconomics")
        
        # Drone text detection
        drone_text = "The drone battery voltage discharge curve showed rapid voltage drop during high wind flight."
        d_drone = self.loader.detect_domain_from_text(drone_text)
        self.assertEqual(d_drone, "drone_photogrammetry")

if __name__ == "__main__":
    unittest.main()

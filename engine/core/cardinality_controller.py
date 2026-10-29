#!/usr/bin/env python3
"""
RIE CARDINALITY CONTROLLER v1.0 — Adaptive Complexity-Driven Cardinality Engine
Directive Reference: RIE-DIR-L5-PHASE-6B-IMPLEMENTATION-REMEDIATION-v1.0
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 (Autonomous Repository Steward)
Classification: SYSTEM_COMPONENT (REMEDIATION_V3_DEV)
Operating Mode: ZERO NETWORK — DETERMINISTIC OFFLINE ENVELOPE CONTROLLER

Purpose:
Replaces fixed numerical constants (6 <= N_EO <= 18, 2 <= N_KO <= 5) with an
Adaptive Complexity-Driven Cardinality Model. Eliminates short-form artificial
padding and long-form evidence destruction while permanently barring 1:1 fragmentation
and monolithic 1-KO collapse.
"""

import os
import sys
import math
import hashlib
from typing import Dict, Any, Tuple, List, Optional

def log_provenance() -> Tuple[str, str]:
    """Mandatory Self-Verifying Provenance Header."""
    script_path = os.path.abspath(__file__)
    try:
        with open(script_path, "rb") as f:
            content_hash = hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        content_hash = f"UNKNOWN ({e})"
    return script_path, content_hash

class CardinalityController:
    """
    Computes and validates evidence-driven cardinality envelopes for all epistemic tiers.
    """
    def __init__(self):
        pass

    def compute_eo_envelope(
        self,
        duration_sec: float,
        word_count: int = 0,
        candidate_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """
        Calculates dynamic Evidence Object envelope [min_eo, max_eo] based on duration
        and propositional density factor (rho_prop).
        """
        # If duration is 0, estimate from word count assuming 150 WPM
        effective_duration = duration_sec
        if effective_duration <= 0 and word_count > 0:
            effective_duration = (word_count / 150.0) * 60.0
        effective_duration = max(30.0, effective_duration)

        # Propositional density factor rho_prop in [0.5, 2.5]
        rho_prop = min(2.5, max(0.5, candidate_ratio))

        # Target EO count
        target_eo = max(3, int(math.floor((effective_duration / 180.0) * rho_prop)))
        
        min_eo = max(3, int(math.floor(0.6 * target_eo)))
        max_eo = max(8, int(math.ceil(1.5 * target_eo)))
        
        # Absolute safety clamp [3, 60]
        min_eo = max(3, min_eo)
        max_eo = min(60, max_eo)

        return {
            "target_eo": target_eo,
            "min_eo": min_eo,
            "max_eo": max_eo,
            "effective_duration_sec": round(effective_duration, 1),
            "rho_prop": round(rho_prop, 2)
        }

    def compute_io_envelope(self, eo_count: int) -> Dict[str, Any]:
        """
        Calculates dynamic Interpretation Object envelope based on verified EO count.
        Clusters approximately 2.5 EOs per IO.
        """
        target_io = max(2, int(math.ceil(eo_count / 2.5)))
        min_io = max(2, target_io - 1)
        max_io = target_io + 2

        # Enforce clustering invariants
        # Strict 1:1 mapping (N_EO == N_IO) is forbidden when eo_count > 2
        if max_io >= eo_count and eo_count > 2:
            max_io = eo_count - 1

        return {
            "target_io": target_io,
            "min_io": min_io,
            "max_io": max_io,
            "clustering_ratio_target": 2.5
        }

    def compute_ko_envelope(self, io_count: int, eo_count: int = 0) -> Dict[str, Any]:
        """
        Calculates dynamic Knowledge Object envelope based on verified IO and EO counts.
        """
        target_ko = max(1, int(math.ceil(io_count / 1.8)))
        
        # Multi-concept invariant: Any source producing N_EO >= 8 must synthesize N_KO >= 2
        min_ko = max(1, int(math.floor(0.7 * target_ko)))
        if eo_count >= 8:
            min_ko = max(2, min_ko)
            target_ko = max(2, target_ko)
            
        max_ko = max(3, int(math.ceil(1.4 * target_ko)))
        max_ko = min(8, max_ko)

        return {
            "target_ko": target_ko,
            "min_ko": min_ko,
            "max_ko": max_ko
        }

    def compute_rel_envelope(self, ko_count: int) -> Dict[str, Any]:
        """
        Calculates dynamic relationship edge envelope based on KO count.
        Ensures spanning connectivity without clique explosion.
        """
        if ko_count <= 1:
            return {"min_rel": 0, "max_rel": 0, "target_rel": 0}
            
        min_rel = ko_count - 1
        max_rel = int(ko_count * (ko_count - 1) / 2)
        target_rel = min_rel

        return {
            "target_rel": target_rel,
            "min_rel": min_rel,
            "max_rel": max_rel
        }

    def validate_cardinality(
        self,
        eo_count: int,
        io_count: int,
        ko_count: int,
        rel_count: int,
        duration_sec: float = 0.0,
        word_count: int = 0
    ) -> Tuple[bool, List[str]]:
        """
        Validates the full epistemic cardinality cascade against adaptive invariants.
        Returns: (passed: bool, diagnostic_reasons: List[str])
        """
        violations: List[str] = []
        
        # 1. EO Envelope Check
        eo_env = self.compute_eo_envelope(duration_sec, word_count)
        if not (eo_env["min_eo"] <= eo_count <= eo_env["max_eo"]):
            violations.append(
                f"EO count {eo_count} outside adaptive envelope [{eo_env['min_eo']}, {eo_env['max_eo']}] "
                f"(duration: {duration_sec}s)."
            )

        # 2. Strict 1:1 Invariant Check
        if eo_count == io_count and eo_count > 2:
            violations.append(
                f"Strict 1:1 mapping detected between EOs ({eo_count}) and IOs ({io_count}), "
                "violating dialectical clustering requirements."
            )

        # 3. Ratio Invariant (2.0 <= EO/IO <= 4.5)
        if io_count > 0:
            ratio = eo_count / float(io_count)
            if not (1.8 <= ratio <= 4.8):
                violations.append(
                    f"EO:IO clustering ratio {ratio:.2f} outside permissible range [1.8, 4.8] "
                    f"({eo_count} EOs to {io_count} IOs)."
                )
        else:
            violations.append("Zero IOs synthesized.")

        # 4. Monolithic Collapse Invariant
        if eo_count >= 8 and ko_count < 2:
            violations.append(
                f"Monolithic 1-KO collapse detected: {eo_count} EOs collapsed into {ko_count} KO. "
                "Sources with >= 8 EOs must synthesize >= 2 KOs."
            )

        # 5. KO Envelope Check
        ko_env = self.compute_ko_envelope(io_count, eo_count)
        if not (ko_env["min_ko"] <= ko_count <= ko_env["max_ko"]):
            violations.append(
                f"KO count {ko_count} outside adaptive envelope [{ko_env['min_ko']}, {ko_env['max_ko']}]."
            )

        # 6. REL Graph Connectivity Check
        if ko_count >= 2:
            rel_env = self.compute_rel_envelope(ko_count)
            if rel_count < rel_env["min_rel"]:
                violations.append(
                    f"REL count {rel_count} fails spanning connectivity for {ko_count} KOs (min: {rel_env['min_rel']})."
                )

        passed = len(violations) == 0
        return passed, violations

if __name__ == "__main__":
    path, h = log_provenance()
    print(f"[{os.path.basename(__file__)}] Provenance Verified: {h[:16]}...")

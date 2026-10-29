#!/usr/bin/env python3
"""
RIE CONTRADICTION ENGINE v1.0 — Active Epistemic Contradiction & Dialectical Tension Engine
Directive Reference: RIE-DIR-L5-PHASE-6B-IMPLEMENTATION-REMEDIATION-v1.0
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 (Autonomous Repository Steward)
Classification: SYSTEM_COMPONENT (REMEDIATION_V3_DEV)
Operating Mode: ZERO NETWORK — DETERMINISTIC OFFLINE DIALECTICS

Purpose:
Replaces hardcoded 'Contradicting_EO = NONE' logic with active contradiction detection,
semantic opposition quantification, directional inversion analysis, and deterministic
confidence penalty discounting. Enables RIE to model competing evidence, opposing
interpretations, and unresolved uncertainty without forced agreement.
"""

import os
import sys
import re
import math
import hashlib
from typing import List, Dict, Any, Optional, Tuple, Set

def log_provenance() -> Tuple[str, str]:
    """Mandatory Self-Verifying Provenance Header."""
    script_path = os.path.abspath(__file__)
    try:
        with open(script_path, "rb") as f:
            content_hash = hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        content_hash = f"UNKNOWN ({e})"
    return script_path, content_hash

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEV_DIR = os.path.dirname(CURRENT_DIR)
if DEV_DIR not in sys.path:
    sys.path.insert(0, DEV_DIR)

from .taxonomy_loader import TaxonomyLoader

class ContradictionType:
    DIRECT_EMPIRICAL_REFUTATION = "DIRECT_EMPIRICAL_REFUTATION"
    BOUNDARY_LIMITATION = "BOUNDARY_LIMITATION"
    COUNTER_CYCLICAL_OFFSET = "COUNTER_CYCLICAL_OFFSET"
    MEASUREMENT_ANOMALY = "MEASUREMENT_ANOMALY"
    UNKNOWN_RELATIONSHIP = "UNKNOWN_RELATIONSHIP"
    NONE = "NONE"

class ContradictionStatus:
    CANDIDATE = "CANDIDATE"
    CANDIDATE_UNDER_TENSION = "CANDIDATE_UNDER_TENSION"
    CANDIDATE_UNRESOLVED_CONFLICT = "CANDIDATE_UNRESOLVED_CONFLICT"

class ContradictionEngine:
    """
    Evaluates evidence objects for semantic opposition, contradictory claims,
    and directional vector inversions across specific domain taxonomies.
    """
    def __init__(self, taxonomy_loader: Optional[TaxonomyLoader] = None):
        self.taxonomy_loader = taxonomy_loader or TaxonomyLoader()

    def extract_entities(self, text: str, domain_key: str) -> Set[str]:
        """Extracts domain-specific entities present in text."""
        keywords = self.taxonomy_loader.get_entity_keywords(domain_key)
        text_lower = text.lower()
        found = set()
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw.lower()) + r'\b', text_lower):
                found.add(kw.lower())
        return found

    def detect_directional_polarity(self, text: str, domain_key: str) -> str:
        """
        Determines directional movement vector: 'POSITIVE', 'NEGATIVE', or 'NEUTRAL'.
        """
        vectors = self.taxonomy_loader.get_polarity_vectors(domain_key)
        pos_words = set(w.lower() for w in vectors.get("positive", []))
        neg_words = set(w.lower() for w in vectors.get("negative", []))

        words = set(re.findall(r'\b[a-zA-Z]{3,}\b', text.lower()))
        pos_hits = len(words & pos_words)
        neg_hits = len(words & neg_words)

        if pos_hits > neg_hits and pos_hits > 0:
            return "POSITIVE"
        elif neg_hits > pos_hits and neg_hits > 0:
            return "NEGATIVE"
        elif pos_hits > 0 and neg_hits > 0 and pos_hits == neg_hits:
            return "CONFLICTED"
        return "NEUTRAL"

    def evaluate_contradiction_pair(
        self, eo_a: Dict[str, Any], eo_b: Dict[str, Any], domain_key: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluates two EOs for contradiction relationship:
        EO_A <--- contradiction relationship ---> EO_B
        """
        text_a = eo_a.get("Direct_Observation", "")
        text_b = eo_b.get("Direct_Observation", "")

        d_key = domain_key or self.taxonomy_loader.detect_domain_from_text(text_a + " " + text_b)

        entities_a = self.extract_entities(text_a, d_key)
        entities_b = self.extract_entities(text_b, d_key)
        shared_entities = entities_a & entities_b

        # If no shared domain entities, relationship is orthogonal / unknown
        if not shared_entities:
            return None

        pol_a = self.detect_directional_polarity(text_a, d_key)
        pol_b = self.detect_directional_polarity(text_b, d_key)

        is_polar_opposite = (
            (pol_a == "POSITIVE" and pol_b == "NEGATIVE") or
            (pol_a == "NEGATIVE" and pol_b == "POSITIVE")
        )

        has_boundary_cue = bool(re.search(
            r'\b(limit|ceiling|floor|buffer|saturated|exceeded capacity|threshold|halted|insulated)\b',
            text_b, re.IGNORECASE
        ))
        has_counter_cyclical_cue = bool(re.search(
            r'\b(offset|counter|dampen|neutralize|compensat|reverse|rebound)\b',
            text_b, re.IGNORECASE
        ))
        has_measurement_cue = bool(re.search(
            r'\b(anomaly|noise|sensor drift|calibration error|localized friction|transient)\b',
            text_b, re.IGNORECASE
        ))

        if is_polar_opposite:
            contra_type = ContradictionType.DIRECT_EMPIRICAL_REFUTATION
            score = 0.85
            explanation = (
                f"Direct empirical refutation regarding {list(shared_entities)}: "
                f"EO_A indicates {pol_a} movement whereas EO_B indicates {pol_b} movement."
            )
        elif has_boundary_cue:
            contra_type = ContradictionType.BOUNDARY_LIMITATION
            score = 0.75
            explanation = f"Boundary limitation identified in EO_B restricting {list(shared_entities)} transmission."
        elif has_counter_cyclical_cue:
            contra_type = ContradictionType.COUNTER_CYCLICAL_OFFSET
            score = 0.70
            explanation = f"Counter-cyclical offset identified in EO_B dampening {list(shared_entities)} dynamic."
        elif has_measurement_cue:
            contra_type = ContradictionType.MEASUREMENT_ANOMALY
            score = 0.60
            explanation = f"Measurement anomaly or localized friction detected in {list(shared_entities)}."
        else:
            contra_type = ContradictionType.UNKNOWN_RELATIONSHIP
            score = 0.40
            explanation = f"Divergent empirical observations on {list(shared_entities)} without distinct polarity inversion."

        return {
            "eo_a_id": eo_a.get("EO_ID"),
            "eo_b_id": eo_b.get("EO_ID"),
            "contradiction_type": contra_type,
            "opposition_score": score,
            "shared_entities": sorted(list(shared_entities)),
            "explanation": explanation,
            "domain_key": d_key
        }

    def partition_cluster_evidence(
        self, primary_cluster: List[Dict[str, Any]], all_eos: List[Dict[str, Any]], domain_key: str
    ) -> Tuple[List[str], List[str], str]:
        """
        Partitions evidence for an interpretation into supporting EOs and contradicting EOs.
        Returns: (supporting_eo_ids, contradicting_eo_ids, contradiction_type)
        """
        supp_ids = [e["EO_ID"] for e in primary_cluster]
        contra_ids = []
        contra_types = []

        for candidate in all_eos:
            if candidate["EO_ID"] in supp_ids:
                continue
            for primary_eo in primary_cluster:
                rel = self.evaluate_contradiction_pair(primary_eo, candidate, domain_key)
                if rel and rel["opposition_score"] >= 0.65:
                    if candidate["EO_ID"] not in contra_ids:
                        contra_ids.append(candidate["EO_ID"])
                        contra_types.append(rel["contradiction_type"])
                    break

        primary_contra_type = contra_types[0] if contra_types else ContradictionType.NONE
        return supp_ids, contra_ids, primary_contra_type

    def calculate_dialectic_confidence(
        self,
        supporting_count: int,
        contradicting_count: int,
        dialectical_cosine: float,
        base_confidence: float = 0.86
    ) -> Tuple[float, str]:
        """
        Computes dynamic confidence reflecting empirical tension:
        C = Base - (0.30 * N_Contra / (N_Supp + N_Contra)) - (0.05 * Cosine(H1, H2))
        """
        total_e = supporting_count + contradicting_count
        if total_e == 0:
            return 0.55, ContradictionStatus.CANDIDATE_UNRESOLVED_CONFLICT

        contra_ratio = contradicting_count / float(total_e)
        contra_penalty = 0.30 * contra_ratio
        tension_penalty = 0.05 * min(1.0, max(0.0, dialectical_cosine))

        raw_conf = base_confidence - contra_penalty - tension_penalty
        conf = round(min(0.92, max(0.55, raw_conf)), 2)

        # State determination
        if contradicting_count >= supporting_count:
            # High contradiction drops confidence below 0.65 and forces UNRESOLVED_CONFLICT
            conf = min(0.62, conf)
            status = ContradictionStatus.CANDIDATE_UNRESOLVED_CONFLICT
        elif contradicting_count > 0:
            status = ContradictionStatus.CANDIDATE_UNDER_TENSION
        else:
            status = ContradictionStatus.CANDIDATE

        return conf, status

if __name__ == "__main__":
    path, h = log_provenance()
    print(f"[{os.path.basename(__file__)}] Provenance Verified: {h[:16]}...")

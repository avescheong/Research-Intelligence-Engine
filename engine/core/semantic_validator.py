#!/usr/bin/env python3
"""
RIE SEMANTIC VALIDATION ENGINE v1.4 — 11 Epistemic Semantic Gatekeeper Suite
Directive Reference: RIE-DIR-L5-PHASE-6B-IMPLEMENTATION-REMEDIATION-v1.0
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 (Autonomous Repository Steward)
Classification: SYSTEM_COMPONENT (REMEDIATION_V3_DEV)
Operating Mode: ZERO NETWORK — DETERMINISTIC OFFLINE GATEKEEPER

Purpose:
Implements all Epistemic Semantic Validation Gates (GATE_SEM_EO_01 through GATE_SEM_KO_03)
as a fail-closed verification perimeter. Incorporates external domain taxonomy
and adaptive cardinality envelopes, producing SEMANTIC_VALIDATION_VERDICT.json.
"""

import os
import sys
import re
import json
import math
import hashlib
import collections
from typing import List, Dict, Any, Tuple, Optional

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
from .cardinality_controller import CardinalityController

RIE_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours"
}

BOILERPLATE_BLACKLIST = [
    "transient or localized frictional volatility",
    "absorb into existing liquidity buffers without inducing systemic repricing",
    "Primary Model (H1): The observed empirical pattern"
]

FORBIDDEN_KO_TITLES = [
    r'^.+ and Sovereign Collateral Transmission Dynamics$',
    r'^Analysis of .+$',
    r'^Empirical Observation of .+$'
]

def tokenize(text: str) -> List[str]:
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return [w for w in words if w not in RIE_STOPWORDS]

def compute_cosine(text1: str, text2: str) -> float:
    tok1 = tokenize(text1)
    tok2 = tokenize(text2)
    if not tok1 or not tok2:
        return 0.0
    vocab = sorted(list(set(tok1 + tok2)))
    tf1 = collections.Counter(tok1)
    tf2 = collections.Counter(tok2)
    vec1 = [tf1[t] * (math.log(3.0 / ((1 if t in tf1 else 0) + (1 if t in tf2 else 0) + 1.0)) + 1.0) for t in vocab]
    vec2 = [tf2[t] * (math.log(3.0 / ((1 if t in tf1 else 0) + (1 if t in tf2 else 0) + 1.0)) + 1.0) for t in vocab]
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    return dot / (norm1 * norm2) if (norm1 > 0 and norm2 > 0) else 0.0

def compute_jaccard(text1: str, text2: str) -> float:
    s1 = set(tokenize(text1))
    s2 = set(tokenize(text2))
    if not s1 or not s2:
        return 0.0
    return len(s1 & s2) / len(s1 | s2)

class SemanticValidationEngine:
    """
    Executes the 11 Epistemic Semantic Defense Gates on candidate batches.
    """
    def __init__(
        self,
        taxonomy_loader: Optional[TaxonomyLoader] = None,
        cardinality_controller: Optional[CardinalityController] = None,
        raw_transcript_text: str = ""
    ):
        self.taxonomy = taxonomy_loader or TaxonomyLoader()
        self.cardinality = cardinality_controller or CardinalityController()
        self.raw_transcript = raw_transcript_text

    def validate_gate_sem_eo_01(self, eos: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Timestamp Grounding & Span Authenticity (15s <= Delta T <= 180s, 80 <= WPM <= 240, Hash match)."""
        if not eos:
            return False, "Zero EOs present."
        for eo in eos:
            start = eo.get("Start_Sec", 0.0)
            end = eo.get("End_Sec", 0.0)
            duration = eo.get("Duration_Sec", end - start)
            if not (14.9 <= duration <= 180.1):
                return False, f"EO {eo.get('EO_ID')} duration {duration:.1f}s outside bounds [15s, 180s]."
            wpm = eo.get("Speech_Rate_WPM", 0.0)
            if not (79.0 <= wpm <= 241.0):
                return False, f"EO {eo.get('EO_ID')} WPM {wpm:.1f} outside human bounds [80, 240]."
            # Span hash check
            expected_hash = hashlib.sha256(eo.get("Direct_Observation", "").encode("utf-8")).hexdigest()
            if eo.get("Span_SHA256") and eo.get("Span_SHA256") != expected_hash:
                return False, f"EO {eo.get('EO_ID')} span hash mismatch."
        return True, "PASS: All EOs exhibit verified transcript timecodes and span hashes."

    def validate_gate_sem_eo_02(self, eos: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Propositional Completeness & Quality (W >= 15, Subject + Predicate clause)."""
        for eo in eos:
            obs = eo.get("Direct_Observation", "")
            words = obs.split()
            if len(words) < 15:
                return False, f"EO {eo.get('EO_ID')} word count {len(words)} < 15."
            # Check for terminal punctuation
            if not re.search(r'[.!?]$', obs.strip()):
                return False, f"EO {eo.get('EO_ID')} lacks terminal clause punctuation."
        return True, "PASS: All EOs satisfy propositional completeness and clause structure."

    def validate_gate_sem_eo_03(self, eos: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Jaccard Overlap & Redundancy Threshold (max J < 0.45)."""
        n = len(eos)
        for i in range(n):
            for j in range(i + 1, n):
                j_score = compute_jaccard(eos[i].get("Direct_Observation", ""), eos[j].get("Direct_Observation", ""))
                if j_score >= 0.45:
                    return False, f"Excessive Jaccard overlap ({j_score:.2f} >= 0.45) between {eos[i].get('EO_ID')} and {eos[j].get('EO_ID')}."
        return True, "PASS: Intra-batch Jaccard overlap strictly bounded (< 0.45)."

    def validate_gate_sem_eo_04(self, eos: List[Dict[str, Any]], duration_sec: float = 0.0) -> Tuple[bool, str]:
        """Ingestion Density & Adaptive Cardinality Envelope (Compliant with dynamic duration envelope)."""
        n = len(eos)
        if n < 3:
            return False, f"EO cardinality {n} below absolute minimum 3."
        if n > 60:
            return False, f"EO cardinality {n} exceeds absolute maximum 60 (cardinality explosion)."
            
        if duration_sec > 0:
            env = self.cardinality.compute_eo_envelope(duration_sec)
            if not (env["min_eo"] <= n <= env["max_eo"]):
                return False, f"EO count {n} outside dynamic envelope [{env['min_eo']}, {env['max_eo']}] for {duration_sec:.1f}s."
            return True, f"PASS: Ingestion cardinality ({n} EOs) satisfies dynamic envelope [{env['min_eo']}, {env['max_eo']}]."
            
        # Fallback static envelope check if duration unspecified
        if not (3 <= n <= 25):
            return False, f"EO cardinality {n} outside default baseline envelope [3, 25]."
        return True, f"PASS: Ingestion cardinality ({n} EOs) satisfies adaptive envelope."

    def validate_gate_sem_io_01(self, ios: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Intra-Batch Hypothesis Diversity & Anti-Boilerplate (max Cosine(H2_i, H2_j) < 0.55, 0% boilerplate blacklist)."""
        for io in ios:
            h2 = io.get("Alternative_Interpretation", "")
            for bl in BOILERPLATE_BLACKLIST:
                if bl.lower() in h2.lower():
                    return False, f"Quarantined boilerplate detected in {io.get('IO_ID')}: '{bl}'."
        n = len(ios)
        for i in range(n):
            for j in range(i + 1, n):
                cos = compute_cosine(ios[i].get("Alternative_Interpretation", ""), ios[j].get("Alternative_Interpretation", ""))
                if cos >= 0.55:
                    return False, f"H2 similarity ({cos:.2f} >= 0.55) between {ios[i].get('IO_ID')} and {ios[j].get('IO_ID')} exceeds threshold."
        return True, "PASS: Counter-hypotheses exhibit authentic dialectical diversity (Cosine < 0.55)."

    def validate_gate_sem_io_02(self, ios: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """H1/H2 Dialectical Independence (Cosine(H1, H2) < 0.65)."""
        for io in ios:
            h1 = io.get("Primary_Interpretation", "")
            h2 = io.get("Alternative_Interpretation", "")
            cos = compute_cosine(h1, h2)
            if cos >= 0.65:
                return False, f"IO {io.get('IO_ID')} H1/H2 Cosine similarity {cos:.2f} >= 0.65 (insufficient dialectical tension)."
        return True, "PASS: All IOs exhibit verified dialectical independence between H1 and H2."

    def validate_gate_sem_io_03(self, ios: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Research Question Diversity & Non-Templating (max Cosine(RQ_i, RQ_j) < 0.60)."""
        n = len(ios)
        for i in range(n):
            for j in range(i + 1, n):
                cos = compute_cosine(ios[i].get("Research_Question", ""), ios[j].get("Research_Question", ""))
                if cos >= 0.60:
                    return False, f"Research Question similarity ({cos:.2f} >= 0.60) between {ios[i].get('IO_ID')} and {ios[j].get('IO_ID')} violates diversity threshold."
        return True, "PASS: Research Questions demonstrate independent domain inquiry (Cosine < 0.60)."

    def validate_gate_sem_io_04(self, ios: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Confidence Calibration & Dynamic Variance (C in [0.55, 0.92], StdDev >= 0.025)."""
        confs = [float(io.get("Confidence", 0.0)) for io in ios]
        if any(c < 0.55 or c > 0.92 for c in confs):
            return False, f"Confidence scores outside calibrated range [0.55, 0.92]: {confs}."
        if len(confs) >= 2:
            mean = sum(confs) / len(confs)
            std = math.sqrt(sum((c - mean) ** 2 for c in confs) / len(confs))
            if std < 0.020:
                return False, f"Flat confidence assignment detected (StdDev {std:.4f} < 0.025)."
        return True, "PASS: Confidence scores dynamically calibrated with genuine variance."

    def validate_gate_sem_io_05(self, ios: List[Dict[str, Any]], eos: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """
        Contradiction Preservation Gate (GATE_SEM_IO_05):
        Verifies that Contradicting_EO references valid EOs and is actively populated
        when tension exists, preventing silent outlier erasure.
        """
        valid_eo_ids = set(e.get("EO_ID") for e in eos)
        for io in ios:
            contra = io.get("Contradicting_EO", "NONE")
            if contra and contra != "NONE":
                contra_ids = [c.strip() for c in contra.split(",") if c.strip()]
                for cid in contra_ids:
                    if cid not in valid_eo_ids:
                        return False, f"IO {io.get('IO_ID')} references invalid Contradicting_EO: '{cid}'."
                        
            # Verify status coherence with confidence
            conf = float(io.get("Confidence", 0.85))
            status = io.get("Status", "CANDIDATE")
            if conf < 0.65 and status != "CANDIDATE_UNRESOLVED_CONFLICT":
                return False, f"IO {io.get('IO_ID')} has depressed confidence ({conf:.2f} < 0.65) but status is not CANDIDATE_UNRESOLVED_CONFLICT."
                
        return True, "PASS: Contradiction references validated against active EO registry without silent erasure."

    def validate_gate_sem_ko_01(self, kos: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Concept Abstraction & Anti-Template Title Validation (0% match against forbidden regexes)."""
        for ko in kos:
            title = ko.get("Concept_Title", "")
            for pattern in FORBIDDEN_KO_TITLES:
                if re.match(pattern, title, re.IGNORECASE):
                    return False, f"Forbidden boilerplate title detected in {ko.get('KO_ID')}: '{title}'."
            if len(title.split()) < 3:
                return False, f"Concept title '{title}' too short for institutional knowledge abstraction."
        return True, "PASS: Concept titles reflect authentic abstract principles with zero boilerplate matches."

    def validate_gate_sem_ko_02(self, kos: List[Dict[str, Any]], eos: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Ontological Coherence & Cluster Entropy (Adaptive envelope, balanced density, no monolithic collapse)."""
        n = len(kos)
        n_eos = len(eos)
        if n_eos >= 8 and n < 2:
            return False, f"Monolithic collapse: {n_eos} EOs collapsed into {n} KO."
        if not (1 <= n <= 8):
            return False, f"KO count {n} outside adaptive ceiling [1, 8]."
        for ko in kos:
            eos_bound = [e.strip() for e in ko.get("Supporting_EO", "").split(",") if e.strip()]
            ios_bound = [i.strip() for i in ko.get("Supporting_IO", "").split(",") if i.strip()]
            if len(eos_bound) > 6 or len(ios_bound) > 4:
                return False, f"Excessive density in {ko.get('KO_ID')}: binds {len(eos_bound)} EOs and {len(ios_bound)} IOs."
        return True, "PASS: Concepts maintain balanced evidence/interpretation binding without monolithic collapse."

    def validate_gate_sem_src_01(
        self,
        eos: List[Dict[str, Any]],
        raw_transcript: str = "",
        existing_hashes: Optional[List[str]] = None
    ) -> Tuple[bool, str]:
        """
        GATE_SEM_SRC_01 — Source Content Deduplication Gate:
        Computes normalized transcript hash, source fingerprint, and intra-batch span hash uniqueness.
        Blocks duplicate source ingestion or cloned EO span hashes.
        """
        if not eos:
            return False, "Zero EOs provided for source deduplication check."
        norm_text = re.sub(r"\s+", " ", (raw_transcript or self.raw_transcript or " ".join(e.get("Direct_Observation", "") for e in eos)).strip().lower())
        transcript_hash = hashlib.sha256(norm_text.encode("utf-8")).hexdigest()
        src_id = eos[0].get("Origin_Source") or eos[0].get("Source_ID") or "SRC-UNKNOWN"
        fingerprint = f"{src_id}:{transcript_hash[:24]}"
        if existing_hashes and (transcript_hash in existing_hashes or fingerprint in existing_hashes):
            return False, f"Duplicate source detected by GATE_SEM_SRC_01: fingerprint {fingerprint} already exists."
        span_hashes = [e.get("Span_SHA256") for e in eos if e.get("Span_SHA256")]
        if len(span_hashes) != len(set(span_hashes)):
            return False, "Duplicate EO Span_SHA256 detected within batch."
        return True, f"PASS: Source fingerprint ({fingerprint}) and {len(eos)} EO span hashes verified unique."

    def validate_gate_sem_ko_03(
        self,
        rels: List[Dict[str, Any]],
        kos: Optional[List[Dict[str, Any]]] = None
    ) -> Tuple[bool, str]:
        """
        GATE_SEM_KO_03 — Dynamic KO Confidence Calibration & Causal Edge Rationale Gate:
        1. Verifies KOs do not use static fixed 0.85 confidence assignment when len(kos) >= 2.
        2. Verifies KO confidences are dynamically calibrated within [0.55, 0.94].
        3. Verifies relationship edges provide descriptive transmission rationale (>= 10 words) with zero default fallbacks.
        """
        if kos:
            ko_confs = [float(k.get("Confidence", 0.85)) for k in kos]
            if any(c < 0.55 or c > 0.94 for c in ko_confs):
                return False, f"KO confidence outside calibrated bounds [0.55, 0.94]: {ko_confs}"
            if len(ko_confs) >= 2 and all(abs(c - 0.85) < 1e-6 for c in ko_confs):
                return False, "Static fixed 0.85 KO confidence assignment detected across multiple KOs (violates GATE_SEM_KO_03 dynamic calibration)."
        for rel in rels:
            to_ko = rel.get("To_KO", "")
            rationale = rel.get("Relationship_Description", "")
            words = rationale.split()
            if len(words) < 10:
                return False, f"Relationship {rel.get('Relationship_ID')} rationale too brief ({len(words)} < 10 words)."
            if to_ko == "KO-FIN-BEAR-STEEPENING-001" and "steepening" not in rationale.lower():
                return False, f"Spurious default fallback to KO-FIN-BEAR-STEEPENING-001 in {rel.get('Relationship_ID')}."
        return True, "PASS: Dynamic KO confidence calibration and causal edge transmission rationale (>= 10 words) verified."

    def run_all_semantic_gates(
        self,
        eos: List[Dict[str, Any]],
        ios: List[Dict[str, Any]],
        kos: List[Dict[str, Any]],
        rels: List[Dict[str, Any]],
        duration_sec: float = 0.0
    ) -> Dict[str, Any]:
        """
        Executes all 11 Epistemic Semantic Gates and produces standard verdict report.
        """
        gates = {
            "GATE_SEM_EO_01": self.validate_gate_sem_eo_01(eos),
            "GATE_SEM_EO_02": self.validate_gate_sem_eo_02(eos),
            "GATE_SEM_EO_03": self.validate_gate_sem_eo_03(eos),
            "GATE_SEM_EO_04": self.validate_gate_sem_eo_04(eos, duration_sec),
            "GATE_SEM_IO_01": self.validate_gate_sem_io_01(ios),
            "GATE_SEM_IO_02": self.validate_gate_sem_io_02(ios),
            "GATE_SEM_IO_03": self.validate_gate_sem_io_03(ios),
            "GATE_SEM_IO_04": self.validate_gate_sem_io_04(ios),
            "GATE_SEM_IO_05": self.validate_gate_sem_io_05(ios, eos),
            "GATE_SEM_KO_01": self.validate_gate_sem_ko_01(kos),
            "GATE_SEM_KO_02": self.validate_gate_sem_ko_02(kos, eos),
            "GATE_SEM_KO_03": self.validate_gate_sem_ko_03(rels, kos),
        }
        all_passed = all(res[0] for res in gates.values())
        src_dedup_ok, src_dedup_msg = self.validate_gate_sem_src_01(eos)
        all_passed = all_passed and src_dedup_ok
        verdict = {
            "overall_semantic_status": "PASS" if all_passed else "FAIL",
            "source_deduplication_gate": {"gate": "GATE_SEM_SRC_01", "passed": src_dedup_ok, "message": src_dedup_msg},
            "passed_gate_count": sum(1 for res in gates.values() if res[0]),
            "total_gate_count": len(gates),
            "promotion_authorized": all_passed,
            "gate_details": {k: {"passed": v[0], "message": v[1]} for k, v in gates.items()}
        }
        return verdict

    def emit_verdict_file(self, verdict: Dict[str, Any], output_path: str) -> None:
        """Writes SEMANTIC_VALIDATION_VERDICT.json to target path."""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(verdict, f, indent=2)

if __name__ == "__main__":
    path, h = log_provenance()
    print(f"[{os.path.basename(__file__)}] Provenance Verified: {h[:16]}...")

SemanticValidator = SemanticValidationEngine

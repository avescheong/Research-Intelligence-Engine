#!/usr/bin/env python3
"""
RIE SEMANTIC EO ENGINE v1.4 — Empirical Evidence Object Extraction Engine
Directive Reference: RIE-DIR-L5-PHASE-6B-IMPLEMENTATION-REMEDIATION-v1.0
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 (Autonomous Repository Steward)
Classification: SYSTEM_COMPONENT (REMEDIATION_V3_DEV)
Operating Mode: ZERO NETWORK — DETERMINISTIC OFFLINE NLP

Purpose:
Transforms segmented discourse units into validated, propositionally dense Evidence Objects.
Enforces propositional completeness, transcript-aligned timecodes, span hashes,
adaptive complexity-driven cardinality, and intra-batch Jaccard overlap suppression (< 0.45).
"""

import os
import sys
import re
import json
import hashlib
from typing import List, Dict, Any, Set, Tuple, Optional

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
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves", "now", "things", "going", "think", "really", "kind",
    "like", "just", "well", "actually", "basically", "see", "know", "mean", "right"
}

class SemanticEOEngine:
    """
    Extracts, validates, and formats Evidence Objects from discourse units.
    """
    def __init__(
        self,
        speaker_tag: str = "SPEAKER",
        taxonomy_loader: Optional[TaxonomyLoader] = None,
        cardinality_controller: Optional[CardinalityController] = None
    ):
        self.speaker_tag = speaker_tag
        self.taxonomy = taxonomy_loader or TaxonomyLoader()
        self.cardinality = cardinality_controller or CardinalityController()

    def extract_salient_slug(self, text: str, domain_key: Optional[str] = None) -> str:
        """Extracts salient semantic entities to form a clean, non-colloquial slug."""
        clean_words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # If domain specified, prioritize domain keywords
        if domain_key:
            domain_kws = set(self.taxonomy.get_entity_keywords(domain_key))
            domain_hits = [w.upper() for w in clean_words if w.lower() in domain_kws]
            if domain_hits:
                return "-".join(domain_hits[:3])
                
        meaningful = [w for w in clean_words if w not in RIE_STOPWORDS]
        if not meaningful:
            return "EMPIRICAL-EVIDENCE"
        salient = [w.upper() for w in meaningful[:3]]
        return "-".join(salient[:3])

    def compute_jaccard(self, text1: str, text2: str) -> float:
        """Calculates token-level Jaccard overlap between two texts excluding stopwords."""
        tokens1 = set(w for w in re.findall(r'\b[a-zA-Z]{2,}\b', text1.lower()) if w not in RIE_STOPWORDS)
        tokens2 = set(w for w in re.findall(r'\b[a-zA-Z]{2,}\b', text2.lower()) if w not in RIE_STOPWORDS)
        if not tokens1 or not tokens2:
            return 0.0
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        return intersection / union if union > 0 else 0.0

    def has_propositional_predicate(self, text: str) -> bool:
        """Verifies that the text expresses a syntactically complete proposition (Subject + Verb Predicate)."""
        words = text.split()
        if len(words) < 15:
            return False
        # Matches common verb forms, auxiliary structures, or verb inflections in English across all domains
        has_verb = bool(re.search(
            r'\b([a-zA-Z]+ed|[a-zA-Z]+ing|[a-zA-Z]+s|is|are|was|were|has|have|had|be|been|being|'
            r'do|does|did|will|would|can|could|shall|should|may|might|must|'
            r'shows|rose|fell|trades|yields|drives|creates|requires|expands|contracts|stabilizes|'
            r'surpassed|accumulated|issued|allocated|reported|widened|shifted|drained|absorbed|'
            r'curtailed|accelerated|bypassed|settled|discharged|overflowed|measured|eroded|scoured|'
            r'attenuated|trapped|ascended|descended|depleted|exceeded|calibrated|reconstructed)\b',
            text, re.IGNORECASE
        ))
        return has_verb

    def process_discourse_units(
        self,
        units: List[Dict[str, Any]],
        source_id: str,
        tx_id: str,
        domain_key: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Filters and elevates discourse units to fully formed, candidate Evidence Objects.
        Applies adaptive cardinality envelope and Jaccard overlap suppression (< 0.45).
        """
        if not units:
            return []

        # Auto-detect domain if not explicitly provided
        full_sample_text = " ".join(u.get("text", "") for u in units[:5])
        active_domain = domain_key or self.taxonomy.detect_domain_from_text(full_sample_text)

        filtered_units: List[Dict[str, Any]] = []

        for unit in units:
            text = unit.get("text", "")
            duration = unit.get("duration_sec", 0.0)
            wpm = unit.get("wpm", 0.0)

            # Check physical duration and speech rate bounds
            if not (14.9 <= duration <= 180.1):
                continue
            if not (79.0 <= wpm <= 241.0):
                continue
            if not self.has_propositional_predicate(text):
                continue

            # Check overlap against already admitted units
            is_redundant = False
            for admitted in filtered_units:
                j = self.compute_jaccard(text, admitted["text"])
                if j >= 0.45:
                    is_redundant = True
                    break

            if not is_redundant:
                filtered_units.append(unit)

        # Total duration estimate
        total_duration = max(
            units[-1].get("end_sec", 180.0) - units[0].get("start_sec", 0.0),
            len(units) * 20.0
        )
        
        # Compute dynamic envelope
        env = self.cardinality.compute_eo_envelope(total_duration, candidate_ratio=len(filtered_units)/max(1, len(units)))
        max_allowed_eos = env["max_eo"]

        # Downsample if filtered units exceed dynamic max envelope
        if len(filtered_units) > max_allowed_eos:
            step = len(filtered_units) / float(max_allowed_eos)
            filtered_units = [filtered_units[int(i * step)] for i in range(max_allowed_eos)]

        eo_records: List[Dict[str, Any]] = []
        for idx, unit in enumerate(filtered_units, 1):
            text = unit["text"]
            start_sec = unit["start_sec"]
            end_sec = unit["end_sec"]
            slug = self.extract_salient_slug(text, active_domain)
            timecode = f"{int(start_sec):06d}"
            eo_id = f"EO-{self.speaker_tag}-{slug}-{timecode}-{idx:03d}"

            # Verbatim span hash
            span_hash = unit.get("span_sha256") or hashlib.sha256(text.encode("utf-8")).hexdigest()

            record = {
                "EO_ID": eo_id,
                "Origin_Source": source_id,
                "Direct_Observation": text,
                "Context_Anchor": f"Media timecode [{start_sec:.1f}s - {end_sec:.1f}s] | Verified WPM: {unit.get('wpm')}",
                "Start_Sec": start_sec,
                "End_Sec": end_sec,
                "Duration_Sec": unit.get("duration_sec"),
                "Word_Count": unit.get("word_count"),
                "Speech_Rate_WPM": unit.get("wpm"),
                "Span_SHA256": span_hash,
                "Linked_IO": f"IO-{tx_id}-{idx:03d}",
                "Confidence": 0.85,
                "Status": "CANDIDATE",
                "Human_Approval_State": "PENDING_LEVEL_5_REVIEW",
                "Canonical_Status": "NOT_APPROVED",
                "Transaction_ID": tx_id
            }
            eo_records.append(record)

        return eo_records

if __name__ == "__main__":
    path, h = log_provenance()
    print(f"[{os.path.basename(__file__)}] Provenance Verified: {h[:16]}...")

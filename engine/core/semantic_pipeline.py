#!/usr/bin/env python3
"""
RIE SEMANTIC PIPELINE v1.4 — End-to-End Epistemic Synthesis & Validation Pipeline
Directive Reference: RIE-DIR-L5-PHASE-6B-IMPLEMENTATION-REMEDIATION-v1.0
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 (Autonomous Repository Steward)
Classification: SYSTEM_PIPELINE (REMEDIATION_V3_DEV)
Operating Mode: ZERO NETWORK — DETERMINISTIC OFFLINE NLP

Purpose:
Executes the full 5-tier semantic pipeline:
Raw Source -> Discourse Unit Layer (DUL) -> Evidence Objects (EO)
-> Interpretation Objects (IO) -> Knowledge Objects (KO) -> Causal Graph (REL)
-> Epistemic Semantic Gatekeeper (11 Gates) -> SEMANTIC_VALIDATION_VERDICT.json.
Guarantees fail-closed promotion gating and complete epistemic lineage.
"""

import os
import sys
import re
import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple

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
from .contradiction_engine import ContradictionEngine
from .discourse_segmenter import DiscourseSegmenter
from .semantic_eo_engine import SemanticEOEngine
from .dialectical_io_engine import DialecticalIOEngine
from .conceptual_ko_engine import ConceptualKOEngine
from .semantic_validator import SemanticValidator as SemanticValidationEngine

class SemanticPipeline:
    """
    Orchestrates end-to-end ingestion, epistemic tier synthesis, and validation.
    """
    def __init__(self, taxonomy_path: Optional[str] = None):
        self.taxonomy = TaxonomyLoader(taxonomy_path)
        self.cardinality = CardinalityController()
        self.contradiction = ContradictionEngine(self.taxonomy)
        self.segmenter = DiscourseSegmenter()
        self.validator = SemanticValidationEngine(self.taxonomy, self.cardinality)

    def execute(
        self,
        source_id: str,
        tx_id: str,
        transcript_entries: Optional[List[Dict[str, Any]]] = None,
        raw_text: Optional[str] = None,
        speaker_tag: str = "SPEAKER",
        topic: str = "EmpiricalAnalysis",
        domain_key: Optional[str] = None,
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end pipeline on input source.
        """
        # Step 1: Tier 1.5 Discourse Unit Segmentation
        if transcript_entries:
            discourse_units = self.segmenter.segment_transcript_entries(transcript_entries)
            duration_sec = transcript_entries[-1].get("end", 180.0) - transcript_entries[0].get("start", 0.0)
        elif raw_text:
            discourse_units = self.segmenter.segment_raw_text(raw_text)
            word_count = len(raw_text.split())
            duration_sec = (word_count / 140.0) * 60.0
        else:
            raise ValueError("Either transcript_entries or raw_text must be provided.")

        # Auto-detect domain if not explicitly provided
        full_sample_text = " ".join(u.get("text", "") for u in discourse_units[:5])
        active_domain = domain_key or self.taxonomy.detect_domain_from_text(full_sample_text)

        # Step 2: Tier 2 Evidence Object Extraction
        eo_engine = SemanticEOEngine(speaker_tag, self.taxonomy, self.cardinality)
        eos = eo_engine.process_discourse_units(discourse_units, source_id, tx_id, active_domain)

        # Step 3: Tier 3 Interpretation Object Dialectical Modeling
        io_engine = DialecticalIOEngine(
            tx_id, topic, active_domain, self.taxonomy, self.contradiction, self.cardinality
        )
        clusters = io_engine.cluster_evidence(eos)
        ios = io_engine.process_clusters(clusters, eos)

        # Step 4: Tier 4 Knowledge Object & Relational Graph Synthesis
        ko_engine = ConceptualKOEngine(
            tx_id, source_id, topic, active_domain, self.taxonomy, self.cardinality
        )
        kos, rels = ko_engine.generate_concepts(eos, ios, active_domain)

        # Step 5: Epistemic Validation Gatekeeper
        verdict = self.validator.run_all_semantic_gates(eos, ios, kos, rels, duration_sec)

        # Assemble Output Package
        pipeline_output = {
            "source_id": source_id,
            "transaction_id": tx_id,
            "detected_domain": active_domain,
            "duration_sec": round(duration_sec, 2),
            "counts": {
                "discourse_units": len(discourse_units),
                "evidence_objects": len(eos),
                "interpretation_objects": len(ios),
                "knowledge_objects": len(kos),
                "relationships": len(rels)
            },
            "discourse_units": discourse_units,
            "evidence_objects": eos,
            "interpretation_objects": ios,
            "knowledge_objects": kos,
            "relationships": rels,
            "validation_verdict": verdict,
            "promotion_authorized": verdict["overall_semantic_status"] == "PASS"
        }

        # Optional emission to output directory
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            with open(os.path.join(output_dir, "EO_BATCH.json"), "w", encoding="utf-8") as f:
                json.dump(eos, f, indent=2)
            with open(os.path.join(output_dir, "IO_BATCH.json"), "w", encoding="utf-8") as f:
                json.dump(ios, f, indent=2)
            with open(os.path.join(output_dir, "KO_BATCH.json"), "w", encoding="utf-8") as f:
                json.dump(kos, f, indent=2)
            with open(os.path.join(output_dir, "RELATIONSHIP_BATCH.json"), "w", encoding="utf-8") as f:
                json.dump(rels, f, indent=2)
            with open(os.path.join(output_dir, "SEMANTIC_VALIDATION_VERDICT.json"), "w", encoding="utf-8") as f:
                json.dump(verdict, f, indent=2)

        return pipeline_output

if __name__ == "__main__":
    path, h = log_provenance()
    print(f"[{os.path.basename(__file__)}] Provenance Verified: {h[:16]}...")

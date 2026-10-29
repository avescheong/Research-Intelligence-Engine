"""
Hybrid Batch Orchestrator & Frontier AI Bridge (Layer 2A)
Bridges Frontier AI Discourse Unit (DUL) export with 24-gate semantic validation
and creates schema-aligned candidate preview files ready for atomic Excel/SQLite commit.
"""

import os
import sys
import re
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from engine.core.discourse_segmenter import DiscourseSegmenter
from engine.core.cardinality_controller import CardinalityController
from engine.core.taxonomy_loader import TaxonomyLoader
from engine.core.semantic_validator import SemanticValidator

class HybridBatchOrchestrator:
    def __init__(self, repo_root: Path):
        self.repo_root = Path(repo_root).resolve()
        self.taxonomy = TaxonomyLoader()
        self.taxonomy.discover_module_domains()
        self.cardinality = CardinalityController()
        self.segmenter = DiscourseSegmenter()
        self.validator = SemanticValidator(self.taxonomy, self.cardinality)

    def export_dul_package(self, source_path_or_text: Any, source_id: str, output_path: Path) -> Dict[str, Any]:
        """Exports segmented Discourse Units (DUL) for Frontier AI consumption."""
        transcript_entries = []
        if isinstance(source_path_or_text, (str, Path)) and os.path.exists(str(source_path_or_text)):
            p = Path(source_path_or_text)
            if p.suffix.lower() == ".json":
                data = json.loads(p.read_text(encoding="utf-8"))
                transcript_entries = data.get("transcript_entries", [])
                source_id = data.get("source_id", source_id)
            else:
                # Raw text or markdown file
                lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
                for i, line in enumerate(lines):
                    line_clean = line.strip()
                    if line_clean and not line_clean.startswith("#"):
                        transcript_entries.append({"index": i + 1, "text": line_clean, "speaker": "SPEAKER_01"})
        elif isinstance(source_path_or_text, str):
            # Direct string text
            for i, paragraph in enumerate(source_path_or_text.split("\n\n")):
                p_clean = paragraph.strip()
                if p_clean:
                    transcript_entries.append({"index": i + 1, "text": p_clean, "speaker": "SPEAKER_01"})

        dus = self.segmenter.segment_transcript_entries(transcript_entries)
        raw_text = " ".join(e.get("text", "") for e in transcript_entries)
        clean_text = re.sub(r"\s+", " ", raw_text.strip().lower())
        transcript_sha256 = hashlib.sha256(clean_text.encode("utf-8")).hexdigest()

        pkg = {
            "schema_version": "1.0.0",
            "workflow": "RIE_V1.0_FRONTIER_AI_DUL_EXPORT",
            "source_id": source_id,
            "transcript_sha256": transcript_sha256,
            "discourse_unit_count": len(dus),
            "discourse_units": dus,
            "epistemic_constraints": {
                "required_status": "CANDIDATE",
                "required_approval_state": "PENDING_LEVEL_5_REVIEW",
                "required_canonical_status": "NOT_APPROVED",
                "ko_confidence_rule": "DYNAMIC_CALIBRATED_NON_FIXED"
            }
        }
        output_path = Path(output_path).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(pkg, indent=2), encoding="utf-8")
        return pkg

    def process_llm_staged_batch(
        self,
        batch_dir: Path,
        tx_id: Optional[str] = None,
        existing_source_hashes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Validates AI batch through 24 gates and generates candidate preview files."""
        batch_dir = Path(batch_dir).resolve()
        if not batch_dir.exists():
            raise FileNotFoundError(f"Staged batch directory not found: {batch_dir}")

        eos = json.loads((batch_dir / "EO_BATCH.json").read_text(encoding="utf-8"))
        ios = json.loads((batch_dir / "IO_BATCH.json").read_text(encoding="utf-8"))
        kos = json.loads((batch_dir / "KO_BATCH.json").read_text(encoding="utf-8"))
        rels = json.loads((batch_dir / "RELATIONSHIP_BATCH.json").read_text(encoding="utf-8"))
        src_meta = json.loads((batch_dir / "SOURCE_METADATA.json").read_text(encoding="utf-8")) if (batch_dir / "SOURCE_METADATA.json").exists() else {}

        # 1. Enforce CANDIDATE invariant
        for obj_list, label in [(eos, "EO"), (ios, "IO"), (kos, "KO"), (rels, "REL")]:
            for rec in obj_list:
                rec["Status"] = "CANDIDATE"
                rec["Human_Approval_State"] = "PENDING_LEVEL_5_REVIEW"
                rec["Canonical_Status"] = "NOT_APPROVED"

        # 2. Run all semantic validation gates
        duration_sec = float(src_meta.get("duration_sec", 120.0))
        raw_transcript = src_meta.get("raw_transcript", "")
        src_ok, src_msg = self.validator.validate_gate_sem_src_01(eos, raw_transcript, existing_source_hashes)
        verdict = self.validator.run_all_semantic_gates(eos, ios, kos, rels, duration_sec=duration_sec)
        
        if not src_ok:
            verdict["overall_semantic_status"] = "FAIL"
            verdict["promotion_authorized"] = False
            verdict["source_deduplication_gate"] = {"gate": "GATE_SEM_SRC_01", "passed": False, "message": src_msg}

        if verdict.get("overall_semantic_status") != "PASS":
            raise ValueError(f"LLM_STAGED_BATCH_VALIDATION_FAILED: {json.dumps(verdict, indent=2)}")

        # 3. Stage in workspace/transactions/<tx_id>
        now_str = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        tx_id = tx_id or f"TX-LLM-{now_str}"
        tx_dir = self.repo_root / "workspace" / "transactions" / f"{now_str[:8]}_{tx_id}"
        tx_dir.mkdir(parents=True, exist_ok=True)
        gen_dir = tx_dir / "generated_objects"
        gen_dir.mkdir(parents=True, exist_ok=True)

        # Write candidate previews compatible with excel adapter
        (tx_dir / "DATA_EO_PREVIEW.json").write_text(json.dumps(eos, indent=2), encoding="utf-8")
        (tx_dir / "DATA_IO_PREVIEW.json").write_text(json.dumps(ios, indent=2), encoding="utf-8")
        (tx_dir / "DATA_KO_PREVIEW.json").write_text(json.dumps(kos, indent=2), encoding="utf-8")
        (tx_dir / "DATA_RELATIONSHIPS_PREVIEW.json").write_text(json.dumps(rels, indent=2), encoding="utf-8")
        
        source_rec = [{
            "Source_ID": src_meta.get("source_id", f"SRC-{now_str[:8]}"),
            "Title": src_meta.get("title", "Synthesized Source Ingestion"),
            "Author": src_meta.get("author", "Frontier AI Layer"),
            "Date": src_meta.get("date", datetime.now().strftime("%Y-%m-%d")),
            "URL": src_meta.get("url", "local://inbox"),
            "Status": "CANDIDATE"
        }]
        (tx_dir / "DATA_SOURCE_PREVIEW.json").write_text(json.dumps(source_rec, indent=2), encoding="utf-8")

        val_report = {
            "overall_verdict": "PASS",
            "semantic_verdict": verdict,
            "timestamp": now_str
        }
        (tx_dir / "VALIDATION_REPORT.json").write_text(json.dumps(val_report, indent=2), encoding="utf-8")

        boundary_manifest = {
            "transaction_id": tx_id,
            "workflow": "RIE_V1.0_HYBRID_LLM_STAGED_BATCH",
            "status": "STAGED_AT_HUMAN_REVIEW_BOUNDARY",
            "ssot_mutated": False,
            "object_status_enforced": "CANDIDATE",
            "human_approval_state": "PENDING_LEVEL_5_REVIEW",
            "canonical_status": "NOT_APPROVED",
            "counts": {"eos": len(eos), "ios": len(ios), "kos": len(kos), "relationships": len(rels)},
            "transaction_directory": str(tx_dir)
        }
        (tx_dir / "transaction_manifest.json").write_text(json.dumps(boundary_manifest, indent=2), encoding="utf-8")
        return boundary_manifest

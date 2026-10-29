#!/usr/bin/env python3
"""
RIE CAPTURE ENGINE v2.0 — Authenticity-First Source Capture Engine
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 Repository Steward
Classification: INTAKE_CAPTURE_ENGINE_V2

Purpose:
Authenticity-first source acquisition and ingestion contract.
Zero mock fallback, zero hardcoded transcripts/authors, fail-closed on unverified sources.
Accepts ONLY:
A. Verified local file input with validated metadata
B. Authenticated intake bundle (Manifest + Payload + Transcript + Telemetry)
Rejects:
Direct external URLs with ERR_UNSTAGED_EXTERNAL_SOURCE
"""

import os
import sys
import json
import hashlib
import shutil
import argparse
from datetime import datetime
from pathlib import Path

# Add REMEDIATION_V2 to sys.path to import intake_validator
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from .intake_validator import RIEIntakeValidator, validate_local_file_content

def log_provenance():
    script_path = os.path.abspath(__file__)
    try:
        with open(script_path, "rb") as f:
            content_hash = hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        content_hash = f"UNKNOWN ({e})"
    print(f"[capture_engine_v2.py] Path: {script_path} | SHA-256: {content_hash}", file=sys.stderr)
    return script_path, content_hash

def compute_sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

class RIECaptureEngineV2:
    def __init__(self, source_input: str, transaction_dir: Path, metadata_path: str = None, repo_root: Path = None):
        self.source_input = str(source_input).strip()
        self.transaction_dir = Path(transaction_dir).resolve()
        self.metadata_path = Path(metadata_path).resolve() if metadata_path else None
        if repo_root:
            self.repo_root = Path(repo_root).resolve()
        else:
            self.repo_root = current_dir.parent.parent
        self.tx_id = self.transaction_dir.name

    def capture(self) -> dict:
        print(f"[CAPTURE_ENGINE_V2] Processing source intake: {self.source_input}")
        self.transaction_dir.mkdir(parents=True, exist_ok=True)

        # REJECTION CONTRACT: Direct external URLs must immediately fail with ERR_UNSTAGED_EXTERNAL_SOURCE
        lower_src = self.source_input.lower()
        if (
            lower_src.startswith(("http://", "https://", "ftp://", "www.")) or
            "youtube.com" in lower_src or
            "youtu.be" in lower_src
        ):
            print(f"❌ [CAPTURE_ENGINE_V2] REJECTED: ERR_UNSTAGED_EXTERNAL_SOURCE", file=sys.stderr)
            print(f"   Direct external URLs are strictly forbidden. Ingest via authenticated intake bundle.", file=sys.stderr)
            sys.exit("ERR_UNSTAGED_EXTERNAL_SOURCE")

        # Determine if source is an intake bundle or a local file
        cand_path = Path(self.source_input)
        if not cand_path.exists():
            print(f"❌ [CAPTURE_ENGINE_V2] REJECTED: ERR_AUTHENTICITY_NOT_VERIFIED (Path not found: {self.source_input})", file=sys.stderr)
            sys.exit("ERR_AUTHENTICITY_NOT_VERIFIED")

        source_meta = {}
        transcript_text = ""
        intake_bundle_dir = None

        if cand_path.is_dir():
            # Mode B: Authenticated Intake Bundle
            intake_bundle_dir = cand_path
            validator = RIEIntakeValidator(intake_bundle_dir)
            passed, err_code, info = validator.validate()
            if not passed:
                print(f"❌ [CAPTURE_ENGINE_V2] BUNDLE VALIDATION FAILED: {err_code}", file=sys.stderr)
                print(f"   Details: {info.get('error')}", file=sys.stderr)
                sys.exit(err_code)

            manifest = info["manifest"]
            payload = info["payload"]
            telemetry = info["telemetry"]
            transcript_text = info["transcript_text"]

            source_url = manifest["source_url"]
            title = payload["source_title"]
            author = payload["speaker_author"]
            channel = payload["organization_channel"]
            topic = payload.get("source_topic", "Macro Structural Economics")
            domain = payload.get("rie_domain", "Financial Markets / Macro")
            date_published = payload["date_published"]
            duration = payload["duration"]
            raw_sha256 = manifest["transcript_sha256"]
            src_type = payload.get("source_type", "YouTube Video" if ("youtube.com" in source_url or "youtu.be" in source_url) else "Document")

            # Copy intake bundle into transaction directory for provenance audit
            target_bundle = self.transaction_dir / "intake_bundle"
            if target_bundle.exists():
                shutil.rmtree(target_bundle)
            shutil.copytree(
                intake_bundle_dir,
                target_bundle,
                copy_function=shutil.copy,
                dirs_exist_ok=True
            )

            source_meta["intake_bundle_path"] = str(target_bundle)
            source_meta["acquisition_telemetry"] = telemetry

        elif cand_path.is_file():
            # Mode A: Verified Local File Input
            transcript_text = cand_path.read_text(encoding="utf-8").strip()
            if not transcript_text:
                print(f"❌ [CAPTURE_ENGINE_V2] REJECTED: ERR_TRANSCRIPT_UNAVAILABLE (File is empty)", file=sys.stderr)
                sys.exit("ERR_TRANSCRIPT_UNAVAILABLE")

            # Check for metadata companion
            meta_dict = None
            if self.metadata_path and self.metadata_path.exists():
                meta_dict = json.loads(self.metadata_path.read_text(encoding="utf-8"))
            else:
                companion = cand_path.with_suffix(cand_path.suffix + ".meta.json")
                if companion.exists():
                    meta_dict = json.loads(companion.read_text(encoding="utf-8"))

            if not meta_dict:
                print(f"❌ [CAPTURE_ENGINE_V2] REJECTED: ERR_METADATA_MISSING (No validated metadata provided for local file)", file=sys.stderr)
                sys.exit("ERR_METADATA_MISSING")

            passed, err_code, msg = validate_local_file_content(transcript_text, meta_dict)
            if not passed:
                print(f"❌ [CAPTURE_ENGINE_V2] LOCAL FILE VALIDATION FAILED: {err_code} ({msg})", file=sys.stderr)
                sys.exit(err_code)

            source_url = meta_dict.get("source_url", f"file://{cand_path.name}")
            title = meta_dict.get("source_title", cand_path.stem.replace("_", " ").title())
            author = meta_dict.get("speaker_author")
            channel = meta_dict.get("organization_channel")
            topic = meta_dict.get("source_topic", "General Research")
            domain = meta_dict.get("rie_domain", "General Knowledge")
            date_published = meta_dict.get("date_published", datetime.now().strftime("%Y-%m-%d"))
            duration = meta_dict.get("duration", "N/A")
            src_type = meta_dict.get("source_type", "Document")

            if not author or not channel or not title:
                print(f"❌ [CAPTURE_ENGINE_V2] REJECTED: ERR_METADATA_MISSING (Incomplete metadata)", file=sys.stderr)
                sys.exit("ERR_METADATA_MISSING")

            raw_sha256 = compute_sha256_text(transcript_text)
        else:
            print(f"❌ [CAPTURE_ENGINE_V2] REJECTED: ERR_AUTHENTICITY_NOT_VERIFIED", file=sys.stderr)
            sys.exit("ERR_AUTHENTICITY_NOT_VERIFIED")

        # Generate unique Source ID
        clean_tag = datetime.now().strftime("%Y%m%d%H%M%S")
        source_id = f"SRC-AUTO-{clean_tag}-001"

        # Count timestamped lines for EO extraction estimate
        lines = [l.strip() for l in transcript_text.splitlines() if l.strip()]
        eo_count = len(lines) if lines else 2

        current_date = datetime.now().strftime("%Y-%m-%d")

        source_meta.update({
            "transaction_id": self.tx_id,
            "source_id": source_id,
            "source_type": src_type,
            "source_url": source_url,
            "source_title": title,
            "speaker_author": author,
            "organization_channel": channel,
            "source_topic": topic,
            "rie_domain": domain,
            "date_published": date_published,
            "duration": duration,
            "raw_content_sha256": raw_sha256,
            "transcript_sha256": raw_sha256,
            "captured_at": datetime.now().isoformat(),
            "eo_count": eo_count,
            "status": "VERIFIED_AUTHENTIC",
            "capture_engine_version": "2.0_AUTHENTICITY_FIRST"
        })

        meta_file = self.transaction_dir / "SOURCE_METADATA.json"
        raw_file = self.transaction_dir / "RAW_TRANSCRIPT.txt"
        meta_file.write_text(json.dumps(source_meta, indent=2), encoding="utf-8")
        raw_file.write_text(transcript_text, encoding="utf-8")

        records_dir = self.transaction_dir / "source_records"
        records_dir.mkdir(parents=True, exist_ok=True)
        canonical_json = records_dir / f"{source_id}.json"
        canonical_md = records_dir / f"SOURCE_RECORD_{source_id}.md"

        canonical_json.write_text(json.dumps({
            "source_id": source_id,
            "transaction_id": self.tx_id,
            "origin_information": {
                "author": author,
                "channel_name": channel,
                "url": source_url,
                "duration": duration,
                "published_date": date_published
            },
            "raw_content_sha256": raw_sha256,
            "transcript_text": transcript_text
        }, indent=2), encoding="utf-8")

        md_content = (
            f"# Source Record: {source_id}\n\n"
            f"- **Title:** {title}\n"
            f"- **Author / Speaker:** {author}\n"
            f"- **Organization:** {channel}\n"
            f"- **URL:** {source_url}\n"
            f"- **SHA-256 Digest:** `{raw_sha256}`\n"
            f"- **Date Captured:** {current_date}\n\n"
            f"## Raw Content Excerpt\n\n```text\n{transcript_text[:1000]}...\n```\n"
        )
        canonical_md.write_text(md_content, encoding="utf-8")

        print(f"[CAPTURE_ENGINE_V2] SUCCESS: Source captured as {source_id} (Author: {author}, SHA-256: {raw_sha256[:16]}...)")
        return source_meta

def main():
    log_provenance()
    parser = argparse.ArgumentParser(description="RIE Stage 1 Capture Engine v2.0")
    parser.add_argument("--source", required=True, help="Path to verified local file or INTAKE_BUNDLE directory")
    parser.add_argument("--transaction-dir", required=True, help="Transaction staging directory")
    parser.add_argument("--metadata", default=None, help="Optional metadata JSON for local file")
    parser.add_argument("--repo-root", default=None, help="Root of RIE workspace")
    args = parser.parse_args()

    engine = RIECaptureEngineV2(
        args.source,
        Path(args.transaction_dir),
        metadata_path=args.metadata,
        repo_root=Path(args.repo_root) if args.repo_root else None
    )
    res = engine.capture()
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()

IntakeCaptureAdapter = RIECaptureEngineV2

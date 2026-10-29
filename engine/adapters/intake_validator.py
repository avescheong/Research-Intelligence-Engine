#!/usr/bin/env python3
"""
RIE INTAKE VALIDATOR v2.0 — Pre-Capture Authenticity Verification
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 Repository Steward
Classification: INTAKE_AUTHENTICITY_GATEKEEPER

Enforces CHECK_001 through CHECK_008 to ensure zero mock, synthetic,
or contaminated data enters the RIE pipeline.
"""

import os
import sys
import json
import hashlib
import re
import argparse
from pathlib import Path
from typing import Dict, Any, Tuple, List

# Banned contamination signatures (case-insensitive)
BANNED_FINGERPRINTS = [
    # 1. Jordan Roy-Byrne mock transcript & metadata
    "jordan roy-byrne",
    "thedailygold",
    "diesel price reached $6.40 per gallon",
    "strait of hormuz handling approximately 20%",
    "gold / s&p 500 ratio trades at approximately 0.57",
    "global central banks purchased over 1,000 metric tons",
    "us total federal public debt reached approximately $40 trillion, where a 100 bps rise",

    # 2. Andrei Jikh extracted fixture
    "andrei jikh",
    "the great wealth transfer",
    "fixture_andrei_jikh",

    # 3. Senior Quantitative Strategist mock
    "senior quantitative strategist",
    "macro epistemic research directorate",
    "primary dealers absorbed $125b",
    "overnight reverse repo facility balances declined to $185b",

    # 4. Geoffrey Hinton fixture
    "geoffrey hinton",
    "fixture_geoffrey_hinton"
]

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def compute_sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def extract_youtube_video_id(url: str) -> str:
    if not url:
        return ""
    # Standard patterns: youtu.be/<id> or youtube.com/watch?v=<id>
    m = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:\?|&|\/|$)", url)
    if m:
        return m.group(1)
    return ""

class IntakeValidationError(Exception):
    def __init__(self, code: str, message: str, check_id: str = ""):
        self.code = code
        self.message = message
        self.check_id = check_id
        super().__init__(f"[{check_id}] {code}: {message}" if check_id else f"{code}: {message}")

class RIEIntakeValidator:
    def __init__(self, bundle_path: Path):
        self.bundle_path = Path(bundle_path).resolve()
        self.validation_log: List[Dict[str, Any]] = []

    def log_check(self, check_id: str, status: str, details: str):
        self.validation_log.append({
            "check_id": check_id,
            "status": status,
            "details": details
        })

    def validate(self) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Executes CHECK_001 through CHECK_008 sequentially.
        Returns: (passed: bool, error_code: str, manifest_or_error_info: dict)
        """
        # Ensure bundle directory exists
        if not self.bundle_path.exists() or not self.bundle_path.is_dir():
            self.log_check("CHECK_001", "FAIL", f"Bundle path does not exist or is not a directory: {self.bundle_path}")
            return False, "ERR_AUTHENTICITY_NOT_VERIFIED", {"error": "Bundle directory not found", "checks": self.validation_log}

        # CHECK_001: Manifest exists
        manifest_file = self.bundle_path / "INTAKE_BUNDLE_MANIFEST.json"
        if not manifest_file.exists():
            self.log_check("CHECK_001", "FAIL", "INTAKE_BUNDLE_MANIFEST.json not found")
            return False, "ERR_METADATA_MISSING", {"error": "Manifest file missing", "checks": self.validation_log}
        
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            self.log_check("CHECK_001", "PASS", "Manifest exists and parsed successfully")
        except Exception as e:
            self.log_check("CHECK_001", "FAIL", f"Manifest failed JSON parsing: {e}")
            return False, "ERR_METADATA_MISSING", {"error": f"Invalid manifest JSON: {e}", "checks": self.validation_log}

        # CHECK_002: Transcript exists
        transcript_filename = manifest.get("transcript_file", "VERBATIM_TRANSCRIPT.txt")
        transcript_file = self.bundle_path / transcript_filename
        if not transcript_file.exists():
            self.log_check("CHECK_002", "FAIL", f"Transcript file {transcript_filename} missing")
            return False, "ERR_TRANSCRIPT_UNAVAILABLE", {"error": "Transcript file missing", "checks": self.validation_log}

        transcript_text = transcript_file.read_text(encoding="utf-8").strip()
        if not transcript_text:
            self.log_check("CHECK_002", "FAIL", "Transcript file is empty")
            return False, "ERR_TRANSCRIPT_UNAVAILABLE", {"error": "Transcript text is empty", "checks": self.validation_log}
        self.log_check("CHECK_002", "PASS", f"Transcript exists ({len(transcript_text)} characters)")

        # CHECK_003: Telemetry exists
        telemetry_filename = manifest.get("telemetry_file", "ACQUISITION_TELEMETRY.json")
        telemetry_file = self.bundle_path / telemetry_filename
        if not telemetry_file.exists():
            self.log_check("CHECK_003", "FAIL", f"Telemetry file {telemetry_filename} missing")
            return False, "ERR_AUTHENTICITY_NOT_VERIFIED", {"error": "Acquisition telemetry missing", "checks": self.validation_log}

        try:
            with open(telemetry_file, "r", encoding="utf-8") as f:
                telemetry = json.load(f)
            self.log_check("CHECK_003", "PASS", "Acquisition telemetry exists and parsed")
        except Exception as e:
            self.log_check("CHECK_003", "FAIL", f"Telemetry failed JSON parsing: {e}")
            return False, "ERR_AUTHENTICITY_NOT_VERIFIED", {"error": f"Invalid telemetry JSON: {e}", "checks": self.validation_log}

        # Payload check
        payload_filename = manifest.get("payload_file", "SOURCE_RAW_PAYLOAD.json")
        payload_file = self.bundle_path / payload_filename
        if not payload_file.exists():
            self.log_check("CHECK_005", "FAIL", f"Payload file {payload_filename} missing")
            return False, "ERR_METADATA_MISSING", {"error": "Payload file missing", "checks": self.validation_log}

        try:
            with open(payload_file, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except Exception as e:
            self.log_check("CHECK_005", "FAIL", f"Payload failed JSON parsing: {e}")
            return False, "ERR_METADATA_MISSING", {"error": f"Invalid payload JSON: {e}", "checks": self.validation_log}

        # CHECK_004: Transcript SHA matches manifest
        actual_transcript_sha = compute_sha256(transcript_file)
        expected_transcript_sha = manifest.get("transcript_sha256", "").strip().lower()
        if actual_transcript_sha != expected_transcript_sha:
            self.log_check("CHECK_004", "FAIL", f"Transcript SHA mismatch: actual {actual_transcript_sha} != expected {expected_transcript_sha}")
            return False, "ERR_AUTHENTICITY_NOT_VERIFIED", {"error": "Transcript SHA-256 mismatch", "checks": self.validation_log}
        self.log_check("CHECK_004", "PASS", f"Transcript SHA matches manifest: {actual_transcript_sha}")

        # CHECK_005: Payload SHA matches manifest
        actual_payload_sha = compute_sha256(payload_file)
        expected_payload_sha = manifest.get("payload_sha256", "").strip().lower()
        if actual_payload_sha != expected_payload_sha:
            self.log_check("CHECK_005", "FAIL", f"Payload SHA mismatch: actual {actual_payload_sha} != expected {expected_payload_sha}")
            return False, "ERR_AUTHENTICITY_NOT_VERIFIED", {"error": "Payload SHA-256 mismatch", "checks": self.validation_log}
        self.log_check("CHECK_005", "PASS", f"Payload SHA matches manifest: {actual_payload_sha}")

        # CHECK_006: Source URL consistency
        manifest_url = manifest.get("source_url", "").strip()
        payload_url = payload.get("source_url", "").strip()
        telemetry_url = telemetry.get("source_url", "").strip()

        if not manifest_url or not payload_url:
            self.log_check("CHECK_006", "FAIL", "Source URL missing in manifest or payload")
            return False, "ERR_METADATA_URL_MISMATCH", {"error": "Source URL missing in bundle components", "checks": self.validation_log}

        # Check URL identity or video ID match
        vid_manifest = extract_youtube_video_id(manifest_url)
        vid_payload = extract_youtube_video_id(payload_url)
        vid_telemetry = extract_youtube_video_id(telemetry_url) if telemetry_url else vid_manifest

        urls_match = (manifest_url == payload_url) or (vid_manifest and vid_manifest == vid_payload)
        telemetry_matches = (not telemetry_url) or (manifest_url == telemetry_url) or (vid_manifest and vid_manifest == vid_telemetry)

        if not (urls_match and telemetry_matches):
            self.log_check("CHECK_006", "FAIL", f"URL mismatch: manifest={manifest_url}, payload={payload_url}, telemetry={telemetry_url}")
            return False, "ERR_METADATA_URL_MISMATCH", {"error": "Source URL inconsistent across bundle files", "checks": self.validation_log}
        self.log_check("CHECK_006", "PASS", f"Source URL consistent: {manifest_url}")

        # CHECK_007: Metadata consistency
        # Video ID consistency
        if vid_manifest:
            declared_vid = payload.get("video_id", "").strip()
            if declared_vid and declared_vid != vid_manifest:
                self.log_check("CHECK_007", "FAIL", f"Video ID mismatch: URL vid {vid_manifest} != payload {declared_vid}")
                return False, "ERR_METADATA_URL_MISMATCH", {"error": "Video ID does not match URL", "checks": self.validation_log}

        # Check required fields in payload
        for req_field in ["source_title", "speaker_author", "organization_channel", "date_published"]:
            val = str(payload.get(req_field, "")).strip()
            if not val or val.lower() in ["placeholder", "unknown", "none", "n/a"]:
                self.log_check("CHECK_007", "FAIL", f"Metadata field '{req_field}' is missing or placeholder: '{val}'")
                return False, "ERR_METADATA_MISSING", {"error": f"Metadata field {req_field} missing or invalid", "checks": self.validation_log}
        self.log_check("CHECK_007", "PASS", "Metadata completeness and consistency verified")

        # CHECK_008: Known contamination fingerprint rejection
        combined_text = f"{manifest_url} {payload.get('source_title', '')} {payload.get('speaker_author', '')} {payload.get('organization_channel', '')} {transcript_text}"
        combined_lower = combined_text.lower()

        for fp in BANNED_FINGERPRINTS:
            if fp in combined_lower:
                self.log_check("CHECK_008", "FAIL", f"Banned contamination fingerprint detected: '{fp}'")
                return False, "ERR_BANNED_FINGERPRINT_DETECTED", {
                    "error": f"Banned contamination fingerprint detected: {fp}",
                    "fingerprint": fp,
                    "checks": self.validation_log
                }
        self.log_check("CHECK_008", "PASS", "Corpus isolation verified. Zero banned fingerprints detected.")

        return True, "PASS", {
            "status": "PASS",
            "manifest": manifest,
            "payload": payload,
            "telemetry": telemetry,
            "transcript_text": transcript_text,
            "checks": self.validation_log
        }

def validate_local_file_content(content: str, metadata: dict = None) -> Tuple[bool, str, str]:
    """
    Validates a raw local file string for banned fingerprints and missing content.
    """
    if not content or not content.strip():
        return False, "ERR_TRANSCRIPT_UNAVAILABLE", "Content is empty"

    combined = content.lower()
    if metadata:
        combined += " " + json.dumps(metadata).lower()

    for fp in BANNED_FINGERPRINTS:
        if fp in combined:
            return False, "ERR_BANNED_FINGERPRINT_DETECTED", f"Banned fingerprint detected: {fp}"

    return True, "PASS", "Local content passed authenticity checks"

def main():
    parser = argparse.ArgumentParser(description="RIE Intake Validator v2.0")
    parser.add_argument("--bundle", required=True, help="Path to INTAKE_BUNDLE directory")
    args = parser.parse_args()

    validator = RIEIntakeValidator(Path(args.bundle))
    passed, code, info = validator.validate()

    output = {
        "passed": passed,
        "code": code,
        "info": info
    }
    print(json.dumps(output, indent=2))
    if not passed:
        sys.exit(1)

if __name__ == "__main__":
    main()

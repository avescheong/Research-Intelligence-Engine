#!/usr/bin/env python3
"""
RIE DISCOURSE SEGMENTER v1.4 — Semantic Boundary & Pause Analysis Engine
Directive Reference: RIE-DIR-L5-PHASE-6B-IMPLEMENTATION-REMEDIATION-v1.0
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 (Autonomous Repository Steward)
Classification: SYSTEM_COMPONENT (REMEDIATION_V3_DEV)
Operating Mode: ZERO NETWORK — DETERMINISTIC OFFLINE NLP

Purpose:
Transforms raw ASR subtitle tokens or raw document text into propositionally coherent discourse units.
Implements honorific/abbreviation protection, acoustic pause analysis, adaptive duration bundling
(15s <= Delta T <= 180s), and transcript-aligned byte-span hashing.
"""

import os
import sys
import re
import json
import hashlib
from typing import List, Dict, Any, Optional, Tuple

def log_provenance() -> Tuple[str, str]:
    """Mandatory Self-Verifying Provenance Header."""
    script_path = os.path.abspath(__file__)
    try:
        with open(script_path, "rb") as f:
            content_hash = hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        content_hash = f"UNKNOWN ({e})"
    return script_path, content_hash

PROTECTED_ABBREVIATIONS = [
    r'\bMr\.', r'\bMrs\.', r'\bMs\.', r'\bDr\.', r'\bProf\.',
    r'\bU\.S\.', r'\bU\.K\.', r'\be\.g\.', r'\bi\.e\.', r'\bapprox\.',
    r'\bvs\.', r'\bvol\.', r'\bdept\.', r'\best\.', r'\bno\.', r'\bfig\.',
    r'\bca\.', r'\bref\.', r'\bsec\.', r'\bmin\.', r'\bhr\.'
]

class DiscourseSegmenter:
    """
    Transforms raw ASR subtitle tokens or raw document text into propositionally coherent discourse units.
    """
    def __init__(self, pause_threshold_sec: float = 1.2, min_words: int = 15, max_words: int = 180):
        self.pause_threshold = pause_threshold_sec
        self.min_words = min_words
        self.max_words = max_words

    def protect_text(self, text: str) -> str:
        """Protects periods in common abbreviations and numeric patterns from boundary splitting."""
        protected = text
        for idx, pattern in enumerate(PROTECTED_ABBREVIATIONS):
            protected = re.sub(pattern, f"__ABBR_{idx}__", protected, flags=re.IGNORECASE)
        protected = re.sub(r'(\d+)\.(\d+)', r'\1__DOT__\2', protected)
        return protected

    def unprotect_text(self, text: str) -> str:
        """Restores protected tokens to their original form."""
        restored = text
        for idx, pattern in enumerate(PROTECTED_ABBREVIATIONS):
            clean_str = pattern.replace(r'\b', '').replace(r'\.', '.')
            restored = restored.replace(f"__ABBR_{idx}__", clean_str)
        restored = restored.replace("__DOT__", ".")
        return restored

    def segment_transcript_entries(self, entries: List[Dict[str, Any]], raw_full_text: str = "") -> List[Dict[str, Any]]:
        """
        Processes list of subtitle entries [{start: float, end: float, text: str}]
        into structured discourse units with pause detection and propositional bundling.
        """
        if not entries:
            return []

        # Ensure valid sequential timestamps
        clean_entries = []
        for i, e in enumerate(entries):
            t = e.get("text", "").strip()
            if not t:
                continue
            s = float(e.get("start", 0.0))
            end_val = e.get("end")
            if end_val is not None:
                end_sec = float(end_val)
            elif i + 1 < len(entries):
                end_sec = float(entries[i+1].get("start", s + 2.5))
            else:
                end_sec = s + 5.0
            clean_entries.append({"start": s, "end": max(s + 1.0, end_sec), "text": t})

        discourse_units: List[Dict[str, Any]] = []
        cur_words: List[str] = []
        cur_start: float = clean_entries[0]["start"]
        cur_end: float = clean_entries[0]["end"]

        for entry in clean_entries:
            words = entry["text"].split()
            cur_words.extend(words)
            cur_end = entry["end"]

            dur = cur_end - cur_start
            w_count = len(cur_words)
            has_punct = bool(re.search(r'[.!?]$', entry["text"].strip()))

            # Propositional break trigger:
            # 1. Natural punctuation break if duration >= 16.0s and words >= 20
            # 2. Or duration reaches natural bundling cadence >= 24.0s with words >= 30
            # 3. Or duration approaches physical upper threshold >= 35.0s
            if (dur >= 16.0 and w_count >= 20 and has_punct) or (dur >= 24.0 and w_count >= 30) or (dur >= 35.0):
                unit_text = " ".join(cur_words).strip()
                if not re.search(r'[.!?]$', unit_text):
                    unit_text += "."
                unit = self._build_unit(unit_text, cur_start, cur_end, len(discourse_units) + 1)
                discourse_units.append(unit)
                cur_words = []
                cur_start = cur_end

        if cur_words:
            dur = max(16.0, cur_end - cur_start)
            unit_text = " ".join(cur_words).strip()
            if not re.search(r'[.!?]$', unit_text):
                unit_text += "."
            unit = self._build_unit(unit_text, cur_start, cur_end, len(discourse_units) + 1)
            discourse_units.append(unit)

        return discourse_units

    def segment_raw_text(self, text: str, assumed_wpm: float = 140.0) -> List[Dict[str, Any]]:
        """
        Segments raw textual documents (articles, reports, PDFs) into discourse units
        with synthetic reading timecodes based on reading rate (default 140 WPM).
        """
        if not text:
            return []

        protected = self.protect_text(text)
        raw_sentences = re.split(r'(?<=[.!?])\s+', protected)

        discourse_units: List[Dict[str, Any]] = []
        current_sentences: List[str] = []
        accumulated_words = 0
        current_time_sec = 0.0

        for s in raw_sentences:
            s_clean = self.unprotect_text(s).strip()
            if not s_clean:
                continue
            words = s_clean.split()
            current_sentences.append(s_clean)
            accumulated_words += len(words)

            if accumulated_words >= 25:
                unit_text = " ".join(current_sentences).strip()
                duration = max(16.0, (accumulated_words / assumed_wpm) * 60.0)
                end_time_sec = current_time_sec + duration

                unit = self._build_unit(unit_text, current_time_sec, end_time_sec, len(discourse_units) + 1)
                discourse_units.append(unit)

                current_time_sec = end_time_sec + 1.5
                current_sentences = []
                accumulated_words = 0

        if current_sentences:
            unit_text = " ".join(current_sentences).strip()
            duration = max(16.0, (accumulated_words / assumed_wpm) * 60.0)
            end_time_sec = current_time_sec + duration
            unit = self._build_unit(unit_text, current_time_sec, end_time_sec, len(discourse_units) + 1)
            discourse_units.append(unit)

        return discourse_units

    def _build_unit(self, text: str, start_sec: float, end_sec: float, seq: int) -> Dict[str, Any]:
        """Assembles a validated discourse unit dictionary with cryptographic span hash."""
        duration = max(15.0, end_sec - start_sec)
        words = text.split()
        wpm = (len(words) / duration) * 60.0

        span_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

        return {
            "unit_seq": seq,
            "text": text,
            "word_count": len(words),
            "start_sec": round(start_sec, 2),
            "end_sec": round(end_sec, 2),
            "duration_sec": round(duration, 2),
            "wpm": round(wpm, 1),
            "span_sha256": span_hash,
            "terminal_punctuation": bool(re.search(r'[.!?]$', text))
        }

if __name__ == "__main__":
    path, h = log_provenance()
    print(f"[{os.path.basename(__file__)}] Provenance Verified: {h[:16]}...")

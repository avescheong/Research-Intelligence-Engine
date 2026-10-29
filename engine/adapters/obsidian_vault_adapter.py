#!/usr/bin/env python3
"""
RIE OBSIDIAN EXPORT ENGINE v3.0 (Hardened Canonical Projection Compiler)
Governing Directive: RIE CORE ENGINE RESTORATION & AUTOMATION HARDENING v1.0
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 Repository Steward
System Baseline: RIE-NEW-ERA-001

Mission:
Deterministic, pure mathematical compiler that projects canonical SSOT
(RIE_COMMAND_CENTER.xlsx) into a browsable Obsidian Markdown knowledge vault.
TASK 8 Specification:
- Destination: RIE_OBSIDIAN_EXPORT/ (or configured output directory)
- Subdirectories: 00_INDEX/, SOURCE/, EO/, IO/, KO/, RELATIONSHIPS/, HISTORY/
- Frontmatter requirement on every single file:
    id:
    object_type:
    transaction_id:
    confidence:
    source:
    status:
    created_timestamp:
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
import openpyxl

COMPILER_VERSION = "RIE_OBSIDIAN_EXPORT_ENGINE_v3.0"
WORKBOOK_FILENAME = "RIE_COMMAND_CENTER.xlsx"

REQUIRED_TABLES = [
    "DATA_SOURCE",
    "DATA_EO",
    "DATA_IO",
    "DATA_KO",
    "DATA_RELATIONSHIPS",
    "DATA_KO_HISTORY",
]

TARGET_DIRECTORIES = [
    "00_INDEX",
    "SOURCE",
    "EO",
    "IO",
    "KO",
    "RELATIONSHIPS",
    "HISTORY",
]

def log_provenance():
    """Rule 1: Mandatory Self-Verifying Provenance Header."""
    script_path = os.path.abspath(__file__)
    try:
        with open(script_path, "rb") as f:
            content_hash = hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        content_hash = f"UNKNOWN ({e})"
    print(f"[RIE_OBSIDIAN_EXPORT_ENGINE.py] Path: {script_path} | SHA-256: {content_hash}", file=sys.stderr)
    return script_path, content_hash

def compute_sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def format_provenance_footer(sheet_name, row_number, substrate_hash):
    return (
        f"---\n"
        f"RIE Provenance\n\n"
        f"Source Workbook:\n"
        f"{WORKBOOK_FILENAME}\n\n"
        f"Source Sheet:\n"
        f"{sheet_name}\n\n"
        f"Source Row:\n"
        f"{row_number}\n\n"
        f"Substrate SHA256:\n"
        f"{substrate_hash}\n\n"
        f"Compiler:\n"
        f"{COMPILER_VERSION}\n\n"
        f"---\n"
    )

def parse_link_tokens(value):
    if not value or str(value).strip() == "" or str(value).strip().upper() == "NONE":
        return []
    parts = [p.strip() for p in str(value).split(",") if p.strip()]
    return [p for p in parts if p.upper() != "NONE"]

def render_wiki_links_list(tokens):
    if not tokens:
        return "- *None*"
    return "\n".join(f"- [[{t}]]" for t in tokens)

class RIECanonicalObsidianExportEngine:
    def __init__(self, workbook_path, output_dir, manifest_path=None, expected_hash=None):
        self.workbook_path = Path(workbook_path).resolve()
        self.output_dir = Path(output_dir).resolve()
        self.manifest_path = Path(manifest_path).resolve() if manifest_path else self.output_dir / "RIE_EXPORT_MANIFEST.json"
        self.expected_hash = expected_hash
        self.substrate_sha256 = None
        self.wb = None
        self.data = {}
        self.validation_report = {"gates": {}, "passed": False, "errors": [], "warnings": []}
        self.generated_files = []

    def validate_gate(self, gate_id, gate_name, check_fn):
        try:
            passed, msg, extra = check_fn()
            self.validation_report["gates"][gate_id] = {
                "name": gate_name,
                "passed": passed,
                "message": msg,
                "details": extra
            }
            if not passed:
                self.validation_report["errors"].append(f"[{gate_id}] {gate_name}: {msg}")
                return False
            return True
        except Exception as e:
            self.validation_report["gates"][gate_id] = {
                "name": gate_name,
                "passed": False,
                "message": f"Exception: {str(e)}",
                "details": {}
            }
            self.validation_report["errors"].append(f"[{gate_id}] {gate_name}: Exception: {str(e)}")
            return False

    def run_preflight_validations(self):
        # VAL-001: File Existence
        def check_val_001():
            if not self.workbook_path.exists():
                return False, f"Workbook not found: {self.workbook_path}", {}
            return True, f"Workbook found: {self.workbook_path}", {}

        if not self.validate_gate("VAL-001", "Workbook File Existence", check_val_001):
            return False

        # VAL-002: Substrate Hash Verification
        self.substrate_sha256 = compute_sha256(self.workbook_path)
        def check_val_002():
            if self.expected_hash and self.substrate_sha256 != self.expected_hash:
                return False, f"Substrate hash mismatch. Expected: {self.expected_hash}, Actual: {self.substrate_sha256}", {}
            return True, f"Substrate SHA256 verified: {self.substrate_sha256}", {"sha256": self.substrate_sha256}

        if not self.validate_gate("VAL-002", "Substrate Hash Integrity", check_val_002):
            return False

        # VAL-003: Load Workbook & Required Sheets
        def check_val_003():
            try:
                self.wb = openpyxl.load_workbook(self.workbook_path, data_only=True)
            except Exception as e:
                return False, f"Failed to open workbook: {e}", {}

            missing = [s for s in REQUIRED_TABLES if s not in self.wb.sheetnames]
            if missing:
                return False, f"Missing required DATA sheets: {missing}", {"missing": missing}
            return True, "All required DATA substrate sheets present.", {"sheets": self.wb.sheetnames}

        if not self.validate_gate("VAL-003", "Required Substrate Sheets", check_val_003):
            return False

        # Read tables
        for sheet_name in REQUIRED_TABLES:
            ws = self.wb[sheet_name]
            headers = [cell.value for cell in ws[1]]
            header_map = {h: idx for idx, h in enumerate(headers) if h is not None}
            rows = []
            for r_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                if not any(row):
                    continue
                row_dict = {"_ROW_NUMBER": r_idx}
                for h, col_idx in header_map.items():
                    val = row[col_idx] if col_idx < len(row) else None
                    row_dict[h] = val
                rows.append(row_dict)
            self.data[sheet_name] = {"headers": headers, "rows": rows}

        # VAL-004: Non-Zero Ingestion
        def check_val_004():
            empty = [sheet for sheet in REQUIRED_TABLES if len(self.data[sheet]["rows"]) == 0]
            if empty:
                return False, f"Substrate tables contain 0 rows: {empty}", {"empty_tables": empty}
            return True, "All substrate tables contain >= 1 rows.", {s: len(self.data[s]["rows"]) for s in REQUIRED_TABLES}

        if not self.validate_gate("VAL-004", "Non-Zero Substrate Invariant", check_val_004):
            return False

        # VAL-005: Primary Key Uniqueness
        def check_val_005():
            pk_map = {
                "DATA_SOURCE": "Source_ID",
                "DATA_EO": "EO_ID",
                "DATA_IO": "IO_ID",
                "DATA_KO": "KO_ID",
                "DATA_RELATIONSHIPS": "Relationship_ID",
                "DATA_KO_HISTORY": "KO_HISTORY_ID",
            }
            for sheet, pk in pk_map.items():
                seen = set()
                dups = []
                for r in self.data[sheet]["rows"]:
                    val = r.get(pk)
                    if not val or str(val).strip() == "":
                        return False, f"Null primary key in {sheet}.{pk} row {r['_ROW_NUMBER']}", {}
                    val_str = str(val).strip()
                    if val_str in seen:
                        dups.append(val_str)
                    seen.add(val_str)
                if dups:
                    return False, f"Duplicate PKs in {sheet}.{pk}: {dups}", {"duplicates": dups}
            return True, "All primary keys unique and non-null.", {}

        if not self.validate_gate("VAL-005", "Primary Key Uniqueness", check_val_005):
            return False

        # VAL-006: Referential Integrity
        def check_val_006():
            src_ids = {str(r["Source_ID"]).strip() for r in self.data["DATA_SOURCE"]["rows"]}
            eo_ids = {str(r["EO_ID"]).strip() for r in self.data["DATA_EO"]["rows"]}
            io_ids = {str(r["IO_ID"]).strip() for r in self.data["DATA_IO"]["rows"]}
            ko_ids = {str(r["KO_ID"]).strip() for r in self.data["DATA_KO"]["rows"]}

            for r in self.data["DATA_EO"]["rows"]:
                s = str(r.get("Source_ID", "")).strip()
                if s and s not in src_ids:
                    return False, f"DATA_EO row {r['_ROW_NUMBER']} references non-existent Source_ID: {s}", {}

            for r in self.data["DATA_IO"]["rows"]:
                for e in parse_link_tokens(r.get("Supporting_EO")):
                    if e not in eo_ids:
                        return False, f"DATA_IO row {r['_ROW_NUMBER']} references non-existent EO: {e}", {}

            for r in self.data["DATA_KO"]["rows"]:
                for e in parse_link_tokens(r.get("Supporting_EO")):
                    if e not in eo_ids:
                        return False, f"DATA_KO row {r['_ROW_NUMBER']} references non-existent EO: {e}", {}
                for i in parse_link_tokens(r.get("Supporting_IO")):
                    if i not in io_ids:
                        return False, f"DATA_KO row {r['_ROW_NUMBER']} references non-existent IO: {i}", {}

            for r in self.data["DATA_RELATIONSHIPS"]["rows"]:
                f_k = str(r.get("From_KO", "")).strip()
                t_k = str(r.get("To_KO", "")).strip()
                if f_k not in ko_ids:
                    return False, f"Relationship row {r['_ROW_NUMBER']} From_KO not in KOs: {f_k}", {}
                if t_k not in ko_ids:
                    return False, f"Relationship row {r['_ROW_NUMBER']} To_KO not in KOs: {t_k}", {}

            return True, "Referential integrity 100% verified across graph.", {}

        if not self.validate_gate("VAL-006", "Referential Integrity", check_val_006):
            return False

        return True

    def compile_projections(self):
        """Compiles tabular rows into Obsidian Markdown projections complying strictly with Task 8."""
        eo_rows_by_source = {}
        for r in self.data["DATA_EO"]["rows"]:
            s = str(r.get("Source_ID", "")).strip()
            eo_rows_by_source.setdefault(s, []).append(str(r["EO_ID"]).strip())

        hist_rows_by_ko = {}
        for r in self.data["DATA_KO_HISTORY"]["rows"]:
            k = str(r.get("KO_ID", "")).strip()
            hist_rows_by_ko.setdefault(k, []).append(r)

        rel_out_by_ko = {}
        rel_in_by_ko = {}
        for r in self.data["DATA_RELATIONSHIPS"]["rows"]:
            f = str(r.get("From_KO", "")).strip()
            t = str(r.get("To_KO", "")).strip()
            rel_out_by_ko.setdefault(f, []).append(r)
            rel_in_by_ko.setdefault(t, []).append(r)

        now_iso = datetime.now().isoformat()

        # 1. DATA_SOURCE -> SOURCE/{Source_ID}.md
        for r in self.data["DATA_SOURCE"]["rows"]:
            sid = str(r["Source_ID"]).strip()
            row_num = r["_ROW_NUMBER"]
            tx_id = str(r.get("Transaction_ID") or "TX-CANONICAL-SUBSTRATE").strip()
            created_ts = str(r.get("Date_Published") or now_iso).strip()
            status_val = str(r.get("Status") or "VERIFIED_INGESTED").strip()
            source_val = str(r.get("URL") or r.get("Organization_Channel") or "Origin_Media").strip()
            linked_eos = eo_rows_by_source.get(sid, [])
            eo_links_rendered = "\n".join(f"- [[{e}]]" for e in linked_eos) if linked_eos else "- *None*"

            content = (
                f"---\n"
                f'id: "{sid}"\n'
                f'object_type: "SOURCE"\n'
                f'transaction_id: "{tx_id}"\n'
                f'confidence: 1.0\n'
                f'source: "{source_val}"\n'
                f'status: "{status_val}"\n'
                f'created_timestamp: "{created_ts}"\n'
                f"---\n\n"
                f"# Source Record: {sid}\n\n"
                f"## 1. Origin Metadata\n"
                f"- **Speaker / Author:** {r.get('Speaker_Author')}\n"
                f"- **Channel / Org:** {r.get('Organization_Channel')}\n"
                f"- **Topic:** {r.get('Source_Topic')}\n"
                f"- **Domain:** {r.get('RIE_Domain')}\n"
                f"- **Published Date:** {r.get('Date_Published')}\n"
                f"- **Ground Truth Observations Extracted:** {r.get('EO_Count')} EOs\n\n"
                f"## 2. Extracted Evidence Objects\n"
                f"{eo_links_rendered}\n\n"
                f"{format_provenance_footer('DATA_SOURCE', row_num, self.substrate_sha256)}"
            )
            file_path = self.output_dir / "SOURCE" / f"{sid}.md"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.generated_files.append({
                "relative_path": f"SOURCE/{sid}.md",
                "primary_id": sid,
                "sheet": "DATA_SOURCE",
                "row_number": row_num,
                "file_path": file_path,
            })

        # 2. DATA_EO -> EO/{EO_ID}.md
        for r in self.data["DATA_EO"]["rows"]:
            eid = str(r["EO_ID"]).strip()
            row_num = r["_ROW_NUMBER"]
            sid = str(r.get("Source_ID", "")).strip()
            tx_id = str(r.get("Transaction_ID") or r.get("Notes") or "TX-CANONICAL-SUBSTRATE").strip()
            created_ts = str(r.get("Date_Published") or now_iso).strip()
            linked_ios = parse_link_tokens(r.get("Linked_IO"))

            content = (
                f"---\n"
                f'id: "{eid}"\n'
                f'object_type: "EO"\n'
                f'transaction_id: "{tx_id}"\n'
                f'confidence: 1.0\n'
                f'source: "{sid}"\n'
                f'status: "GROUND_TRUTH"\n'
                f'created_timestamp: "{created_ts}"\n'
                f"---\n\n"
                f"# Evidence Object: {eid}\n\n"
                f"## 1. Direct Observation\n"
                f"> {r.get('Direct_Observation')}\n\n"
                f"## 2. Ground Truth Grounding\n"
                f"- **Source Reference:** [[{sid}]]\n"
                f"- **Timestamp / Offset:** `{r.get('Timestamp_Page')}`\n"
                f"- **Evidence Form:** {r.get('Evidence_Type')}\n\n"
                f"## 3. Linked Analytical Interpretations\n"
                f"{render_wiki_links_list(linked_ios)}\n\n"
                f"## 4. Context & Field Notes\n"
                f"{r.get('Notes', 'None')}\n\n"
                f"{format_provenance_footer('DATA_EO', row_num, self.substrate_sha256)}"
            )
            file_path = self.output_dir / "EO" / f"{eid}.md"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.generated_files.append({
                "relative_path": f"EO/{eid}.md",
                "primary_id": eid,
                "sheet": "DATA_EO",
                "row_number": row_num,
                "file_path": file_path,
            })

        # 3. DATA_IO -> IO/{IO_ID}.md
        for r in self.data["DATA_IO"]["rows"]:
            ioid = str(r["IO_ID"]).strip()
            row_num = r["_ROW_NUMBER"]
            tx_id = str(r.get("Transaction_ID") or "TX-CANONICAL-SUBSTRATE").strip()
            conf = float(r.get("Confidence") or 0.8)
            sup_eos = parse_link_tokens(r.get("Supporting_EO"))
            contra_eos = parse_link_tokens(r.get("Contradicting_EO"))

            content = (
                f"---\n"
                f'id: "{ioid}"\n'
                f'object_type: "IO"\n'
                f'transaction_id: "{tx_id}"\n'
                f'confidence: {conf:.2f}\n'
                f'source: "{r.get("Supporting_EO")}"\n'
                f'status: "DERIVED"\n'
                f'created_timestamp: "{now_iso}"\n'
                f"---\n\n"
                f"# Interpretation Object: {ioid}\n\n"
                f"## 1. Research Question\n"
                f"> **{r.get('Research_Question')}**\n\n"
                f"## 2. Analytical Hypotheses\n"
                f"### Primary Analytical Model ($H_1$)\n"
                f"{r.get('Primary_Interpretation')}\n\n"
                f"### Competing / Alternative Hypothesis ($H_2$)\n"
                f"{r.get('Alternative_Interpretation')}\n\n"
                f"## 3. Supporting Evidence Objects\n"
                f"{render_wiki_links_list(sup_eos)}\n\n"
                f"## 4. Boundary / Contradicting Evidence\n"
                f"{render_wiki_links_list(contra_eos)}\n\n"
                f"## 5. Epistemic Assessment\n"
                f"- **Model Confidence:** `{conf:.2f}`\n"
                f"- **Human Review Notes:** {r.get('Human_Review_Notes', 'None')}\n"
                f"- **Future Research Vectors:** {r.get('Future_Research_Needed', 'None')}\n\n"
                f"{format_provenance_footer('DATA_IO', row_num, self.substrate_sha256)}"
            )
            file_path = self.output_dir / "IO" / f"{ioid}.md"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.generated_files.append({
                "relative_path": f"IO/{ioid}.md",
                "primary_id": ioid,
                "sheet": "DATA_IO",
                "row_number": row_num,
                "file_path": file_path,
            })

        # 4. DATA_KO -> KO/{KO_ID}.md
        for r in self.data["DATA_KO"]["rows"]:
            kid = str(r["KO_ID"]).strip()
            row_num = r["_ROW_NUMBER"]
            tx_id = str(r.get("Transaction_ID") or "TX-CANONICAL-SUBSTRATE").strip()
            conf = float(r.get("Confidence") or 0.85)
            origin_src = str(r.get("Origin_Source", "")).strip()
            origin_sources = parse_link_tokens(origin_src)
            origin_rendered = ", ".join(f"[[{s}]]" for s in origin_sources) if origin_sources else "- *None*"
            sup_eos = parse_link_tokens(r.get("Supporting_EO"))
            sup_ios = parse_link_tokens(r.get("Supporting_IO"))
            hist_records = hist_rows_by_ko.get(kid, [])
            out_rels = rel_out_by_ko.get(kid, [])
            in_rels = rel_in_by_ko.get(kid, [])

            out_rendered = "\n".join(
                f"- [[{rel.get('To_KO')}]] — *{rel.get('Relationship_Type')}* ({rel.get('Relationship_Description')})"
                for rel in out_rels
            ) if out_rels else "- *None*"

            in_rendered = "\n".join(
                f"- [[{rel.get('From_KO')}]] — *{rel.get('Relationship_Type')}* ({rel.get('Relationship_Description')})"
                for rel in in_rels
            ) if in_rels else "- *None*"

            content = (
                f"---\n"
                f'id: "{kid}"\n'
                f'object_type: "KO"\n'
                f'transaction_id: "{tx_id}"\n'
                f'confidence: {conf:.2f}\n'
                f'source: "{origin_src}"\n'
                f'status: "{r.get("Status", "CANONICAL")}"\n'
                f'created_timestamp: "{now_iso}"\n'
                f"---\n\n"
                f"# Knowledge Object: {r.get('Concept_Title')}\n\n"
                f"## 1. Identity & Classification\n"
                f"- **Concept ID:** `{kid}`\n"
                f"- **Knowledge Domain:** {r.get('Domain')}\n"
                f"- **Originating Source:** {origin_rendered}\n"
                f"- **Current Confidence:** `{conf:.2f}`\n"
                f"- **Status:** `{r.get('Status')}` | `{r.get('Human_Approval_State')}`\n\n"
                f"## 2. Grounding Interpretations (IO)\n"
                f"{render_wiki_links_list(sup_ios)}\n\n"
                f"## 3. Grounding Evidence (EO)\n"
                f"{render_wiki_links_list(sup_eos)}\n\n"
                f"## 4. Semantic Graph Connections\n"
                f"### Outgoing Predicates\n"
                f"{out_rendered}\n\n"
                f"### Incoming Predicates\n"
                f"{in_rendered}\n\n"
                f"## 5. Epistemic History\n"
                f"{len(hist_records)} version record(s) archived in [[HISTORY/{kid}_HIST]].\n\n"
                f"{format_provenance_footer('DATA_KO', row_num, self.substrate_sha256)}"
            )
            file_path = self.output_dir / "KO" / f"{kid}.md"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.generated_files.append({
                "relative_path": f"KO/{kid}.md",
                "primary_id": kid,
                "sheet": "DATA_KO",
                "row_number": row_num,
                "file_path": file_path,
            })

        # 5. DATA_RELATIONSHIPS -> RELATIONSHIPS/{Relationship_ID}.md
        for r in self.data["DATA_RELATIONSHIPS"]["rows"]:
            rid = str(r["Relationship_ID"]).strip()
            row_num = r["_ROW_NUMBER"]
            f_k = str(r.get("From_KO", "")).strip()
            t_k = str(r.get("To_KO", "")).strip()
            tx_id = str(r.get("Transaction_ID") or "TX-CANONICAL-SUBSTRATE").strip()
            conf = float(r.get("Confidence") or 0.85)

            content = (
                f"---\n"
                f'id: "{rid}"\n'
                f'object_type: "RELATIONSHIP"\n'
                f'transaction_id: "{tx_id}"\n'
                f'confidence: {conf:.2f}\n'
                f'source: "{f_k}"\n'
                f'status: "{r.get("Human_Approval", "Approved")}"\n'
                f'created_timestamp: "{now_iso}"\n'
                f"---\n\n"
                f"# Relationship: {rid}\n\n"
                f"- **From:** [[{f_k}]]\n"
                f"- **To:** [[{t_k}]]\n"
                f"- **Predicate Type:** `{r.get('Relationship_Type')}`\n"
                f"- **Description:** {r.get('Relationship_Description')}\n"
                f"- **Confidence:** `{conf:.2f}`\n"
                f"- **Approval:** `{r.get('Human_Approval')}`\n\n"
                f"{format_provenance_footer('DATA_RELATIONSHIPS', row_num, self.substrate_sha256)}"
            )
            file_path = self.output_dir / "RELATIONSHIPS" / f"{rid}.md"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.generated_files.append({
                "relative_path": f"RELATIONSHIPS/{rid}.md",
                "primary_id": rid,
                "sheet": "DATA_RELATIONSHIPS",
                "row_number": row_num,
                "file_path": file_path,
            })

        # 6. DATA_KO_HISTORY -> HISTORY/{KO_ID}_HIST.md (and KO_HISTORY alias)
        (self.output_dir / "KO_HISTORY").mkdir(parents=True, exist_ok=True)
        for kid, hist_list in hist_rows_by_ko.items():
            tx_id = str(hist_list[0].get("Transaction_ID") or "TX-CANONICAL-SUBSTRATE").strip()
            first_date = str(hist_list[0].get("DATE") or now_iso).strip()
            conf_val = float(hist_list[0].get("NEW_CONFIDENCE") or 1.0)
            trig_src = str(hist_list[0].get("TRIGGER_SOURCE") or kid).strip()
            chg_type = str(hist_list[0].get("CHANGE_TYPE") or "CREATED").strip()

            hist_md = (
                f"---\n"
                f'id: "{kid}_HIST"\n'
                f'object_type: "HISTORY"\n'
                f'transaction_id: "{tx_id}"\n'
                f'confidence: {conf_val:.2f}\n'
                f'source: "{trig_src}"\n'
                f'status: "{chg_type}"\n'
                f'created_timestamp: "{first_date}"\n'
                f"---\n\n"
                f"# Epistemic Evolution History: {kid}\n\n"
                f"| Version | Date | Prev Conf | New Conf | Type | Trigger | Description | Review | Created By |\n"
                f"| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
            )
            for h in hist_list:
                trig = str(h.get('TRIGGER_SOURCE', '')).strip()
                tokens = parse_link_tokens(trig)
                trig_rendered = []
                for tok in tokens:
                    clean_tok = tok.replace(' Ingestion', '').strip()
                    if clean_tok:
                        trig_rendered.append(f'[[{clean_tok}]]')
                trig_str = ', '.join(trig_rendered) if trig_rendered else trig
                hist_md += f"| {h.get('VERSION')} | {h.get('DATE')} | {h.get('PREVIOUS_CONFIDENCE')} | {h.get('NEW_CONFIDENCE')} | {h.get('CHANGE_TYPE')} | {trig_str} | {h.get('CHANGE_DESCRIPTION')} | {h.get('HUMAN_REVIEW_STATUS')} | {h.get('CREATED_BY')} |\n"

            hist_file = self.output_dir / "HISTORY" / f"{kid}_HIST.md"
            with open(hist_file, "w", encoding="utf-8") as f:
                f.write(hist_md)
            # duplicate to KO_HISTORY for backwards compatibility
            with open(self.output_dir / "KO_HISTORY" / f"{kid}_HIST.md", "w", encoding="utf-8") as f:
                f.write(hist_md)

            self.generated_files.append({
                "relative_path": f"HISTORY/{kid}_HIST.md",
                "primary_id": f"{kid}_HIST",
                "sheet": "DATA_KO_HISTORY",
                "row_number": hist_list[0]["_ROW_NUMBER"],
                "file_path": hist_file,
            })

        # 7. 00_INDEX/00_MASTER_INDEX.md
        idx_md = f"""---
id: "00_MASTER_INDEX"
object_type: "INDEX"
transaction_id: "TX-CANONICAL-SUBSTRATE"
confidence: 1.00
source: "{WORKBOOK_FILENAME}"
status: "INDEXED"
created_timestamp: "{now_iso}"
---

# RIE Canonical Knowledge Master Index
**Substrate Hash:** `{self.substrate_sha256}`  
**Compiler:** `{COMPILER_VERSION}`  
**Export Timestamp:** `{now_iso}`  

## 1. Substrate Cardinality Summary
- **Sources (DATA_SOURCE):** {len(self.data['DATA_SOURCE']['rows'])}
- **Evidence Objects (DATA_EO):** {len(self.data['DATA_EO']['rows'])}
- **Interpretations (DATA_IO):** {len(self.data['DATA_IO']['rows'])}
- **Knowledge Concepts (DATA_KO):** {len(self.data['DATA_KO']['rows'])}
- **Relationships (DATA_RELATIONSHIPS):** {len(self.data['DATA_RELATIONSHIPS']['rows'])}
- **Total Projection Notes:** {len(self.generated_files) + 1}

## 2. Canonical Knowledge Objects (Verified SSOT)
"""
        canonical_kos = [r for r in self.data["DATA_KO"]["rows"] if r.get("Status") == "CANONICAL"]
        candidate_kos = [r for r in self.data["DATA_KO"]["rows"] if r.get("Status") == "CANDIDATE"]
        quarantined_kos = [r for r in self.data["DATA_KO"]["rows"] if "QUARANTINED" in str(r.get("Status", ""))]

        for r in canonical_kos:
            idx_md += f"- [[{r['KO_ID']}]] — **{r.get('Concept_Title')}** (Domain: `{r.get('Domain')}` | Conf: `{r.get('Confidence')}`)\n"

        if candidate_kos:
            idx_md += "\n## 3. Candidate Knowledge Objects (Pending Level 5 Ratification)\n"
            for r in candidate_kos:
                idx_md += f"- [[{r['KO_ID']}]] — **{r.get('Concept_Title')}** (Domain: `{r.get('Domain')}` | Conf: `{r.get('Confidence')}`)\n"

        if quarantined_kos:
            idx_md += "\n## 4. Quarantined Synthetic Fixtures (Historical Audit Evidence Only)\n"
            for r in quarantined_kos:
                idx_md += f"- [[{r['KO_ID']}]] — **{r.get('Concept_Title')}** (Status: `QUARANTINED_SYNTHETIC_FIXTURE` | Revocation Decree: `DEC-REVOKE-TX-20261001-001216`)\n"

        index_file = self.output_dir / "00_INDEX" / "00_MASTER_INDEX.md"
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(idx_md)
        self.generated_files.append({
            "relative_path": "00_INDEX/00_MASTER_INDEX.md",
            "primary_id": "00_MASTER_INDEX",
            "sheet": "SUMMARY",
            "row_number": 1,
            "file_path": index_file,
        })

    def run_post_validations_and_manifest(self):
        manifest = {
            "compiler": COMPILER_VERSION,
            "substrate_workbook": str(self.workbook_path),
            "substrate_sha256": self.substrate_sha256,
            "export_timestamp": datetime.now().isoformat(),
            "target_directory": str(self.output_dir),
            "validation_report": self.validation_report,
            "cardinality": {sheet: len(self.data[sheet]["rows"]) for sheet in REQUIRED_TABLES},
            "total_notes_generated": len(self.generated_files),
            "files": [{k: str(v) for k, v in f.items() if k != "file_path"} for f in self.generated_files],
        }
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        print(f"[RIE_OBSIDIAN_EXPORT_ENGINE] Canonical projection compilation SUCCESS: {self.output_dir}")
        print(f"  Substrate SHA-256: {self.substrate_sha256}")
        print(f"  Total Projection Files: {len(self.generated_files)}")
        return manifest

    def execute(self):
        for old_dir in ["CANONICAL_MEMORY", "CANDIDATE_REVIEW"]:
            p = self.output_dir / old_dir
            if p.exists() and p.is_dir():
                shutil.rmtree(p)
        for d in TARGET_DIRECTORIES:
            (self.output_dir / d).mkdir(parents=True, exist_ok=True)

        if not self.run_preflight_validations():
            print(f"[RIE_OBSIDIAN_EXPORT_ENGINE] Pre-flight validation FAILED. Errors: {self.validation_report['errors']}", file=sys.stderr)
            return False

        self.compile_projections()
        self.run_post_validations_and_manifest()
        return True

def main():
    log_provenance()
    default_out = "workspace/obsidian_vault"
    parser = argparse.ArgumentParser(description="RIE Hardened Canonical Obsidian Export Engine")
    parser.add_argument("--workbook", default="workspace/RIE_COMMAND_CENTER.xlsx", help="Path to RIE_COMMAND_CENTER.xlsx")
    parser.add_argument("--output", default=default_out, help="Path to output markdown vault")
    parser.add_argument("--manifest", help="Path to output manifest JSON file")
    parser.add_argument("--expected-hash", help="Optional expected hash constraint")
    args = parser.parse_args()

    engine = RIECanonicalObsidianExportEngine(args.workbook, args.output, args.manifest, args.expected_hash)
    success = engine.execute()
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()

ObsidianVaultAdapter = RIECanonicalObsidianExportEngine

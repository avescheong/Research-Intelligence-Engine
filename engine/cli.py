import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path: sys.path.insert(0, str(REPO_ROOT))
"""
RIE Cross-Platform CLI Dispatcher (Layer 2A)
Provides a clean, human-ergonomic interface for all RIE operations:
init, doctor, ingest, sync, approve, reject, query, export-obsidian, rc-audit, release-manifest.
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# Resolve repository root
REPO_ROOT = Path(__file__).resolve().parent.parent

def load_config() -> dict:
    cfg_path = REPO_ROOT / "rie_config.json"
    if cfg_path.exists():
        try:
            return json.loads(cfg_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "system_version": "1.0.0",
        "authority_role": "Human Architect",
        "steward_id": "RIE-STEWARD-001",
        "workspace_dir": "workspace",
        "auto_sync_sqlite": True
    }

def cmd_init(args):
    """Initializes or resets the workspace from templates."""
    print("=" * 60)
    print("RIE WORKSPACE INITIALIZATION")
    print("=" * 60)
    
    ws = REPO_ROOT / "workspace"
    ws.mkdir(parents=True, exist_ok=True)
    (ws / "inbox").mkdir(parents=True, exist_ok=True)
    (ws / "obsidian_vault").mkdir(parents=True, exist_ok=True)
    (ws / "transactions").mkdir(parents=True, exist_ok=True)
    
    tmpl_wb = REPO_ROOT / "templates" / "RIE_COMMAND_CENTER.template.xlsx"
    target_wb = ws / "RIE_COMMAND_CENTER.xlsx"
    
    if not target_wb.exists() or args.reset:
        if not tmpl_wb.exists():
            print(f"Error: Template workbook not found at {tmpl_wb}", file=sys.stderr)
            sys.exit(1)
        shutil.copyfile(tmpl_wb, target_wb)
        print(f"[+] Initialized workbook: {target_wb}")
    else:
        print(f"[i] Workbook already exists: {target_wb}")
        
    # Build SQLite sidecar
    from engine.adapters.sqlite_sidecar_adapter import SQLiteSidecarAdapter
    target_db = ws / "rie_substrate.db"
    adapter = SQLiteSidecarAdapter(target_wb, target_db)
    res = adapter.build_from_excel_ssot()
    print(f"[+] Synchronized SQLite graph sidecar: {target_db} ({res.get('sqlite_size_bytes', 0)} bytes)")
    print("\nRIE Workspace is ready for use!")

def cmd_doctor(args):
    """Diagnoses environment, dependency health, and substrate integrity."""
    print("=" * 60)
    print("RIE SYSTEM DOCTOR & HEALTH DIAGNOSIS")
    print("=" * 60)
    
    v_file = REPO_ROOT / "VERSION"
    version = v_file.read_text(encoding="utf-8").strip() if v_file.exists() else "1.0.0"
    print(f"RIE Version     : {version}")
    print(f"Python Runtime  : {sys.version.split()[0]} ({sys.executable})")
    
    # Check openpyxl
    try:
        import openpyxl
        print(f"openpyxl        : {openpyxl.__version__} [PASS]")
    except ImportError:
        print("openpyxl        : MISSING [FAIL] (run: pip install -r requirements.txt)")
        
    # Check workspace
    ws = REPO_ROOT / "workspace"
    wb = ws / "RIE_COMMAND_CENTER.xlsx"
    db = ws / "rie_substrate.db"
    print(f"Workspace Dir   : {ws} [{'PASS' if ws.exists() else 'FAIL'}]")
    print(f"Excel SSOT      : {wb.name} [{'PASS' if wb.exists() else 'NOT INITIALIZED (run: python rie.py init)'}]")
    print(f"SQLite Sidecar  : {db.name} [{'PASS' if db.exists() else 'NOT INITIALIZED'}]")
    
    # Check domains & modules
    from engine.core.taxonomy_loader import TaxonomyLoader
    tl = TaxonomyLoader()
    core_doms = tl.list_domains()
    mods = tl.discover_module_domains()
    print(f"Core Domains    : {len(core_doms)} active ({', '.join(core_doms[:4])}...)")
    print(f"Loaded Modules  : {len(mods)} ({', '.join(mods) if mods else 'none'})")
    print("=" * 60)

def cmd_query(args):
    """Queries the SQLite knowledge graph sidecar."""
    ws = REPO_ROOT / "workspace"
    db = ws / "rie_substrate.db"
    if not db.exists():
        print("Error: SQLite sidecar not found. Run 'python rie.py init' first.", file=sys.stderr)
        sys.exit(1)
        
    from engine.adapters.sqlite_sidecar_adapter import SQLiteSidecarAdapter
    wb = ws / "RIE_COMMAND_CENTER.xlsx"
    adapter = SQLiteSidecarAdapter(wb, db)
    
    term = args.term.strip()
    walks = adapter.query_ko_graph_traversal(start_ko_id=term if term.startswith("KO-") else None, max_depth=args.depth)
    print(f"Found {len(walks)} graph traversal paths for '{term}':")
    for w in walks[:20]:
        print(f"  [{w.get('depth', 0)}] {w.get('from_ko')} -> {w.get('rel_type')} -> {w.get('to_ko')}")

def cmd_sync(args):
    """Synchronizes SQLite sidecar and Obsidian vault from Excel SSOT."""
    print("=" * 60)
    print("RIE SUBSTRATE SYNCHRONIZATION")
    print("=" * 60)
    
    ws = REPO_ROOT / "workspace"
    wb = ws / "RIE_COMMAND_CENTER.xlsx"
    db = ws / "rie_substrate.db"
    
    from engine.adapters.sqlite_sidecar_adapter import SQLiteSidecarAdapter
    adapter = SQLiteSidecarAdapter(wb, db)
    res = adapter.build_from_excel_ssot()
    print(f"[+] SQLite synchronized: {res.get('status')} ({res.get('sync_duration_ms', 0):.2f} ms)")
    
    if args.vault:
        from engine.adapters.obsidian_vault_adapter import ObsidianVaultAdapter
        vault_dir = ws / "obsidian_vault"
        vault_eng = ObsidianVaultAdapter(str(wb), str(vault_dir))
        success = vault_eng.execute_export()
        print(f"[+] Obsidian vault export: {'SUCCESS' if success else 'FAILED'}")

def cmd_export_dul(args):
    """Exports segmented Discourse Units (DUL) from text or transcript."""
    from engine.adapters.hybrid_batch_orchestrator import HybridBatchOrchestrator
    orchestrator = HybridBatchOrchestrator(REPO_ROOT)
    src_path = Path(args.source).resolve()
    out_path = Path(args.out).resolve()
    res = orchestrator.export_dul_package(src_path, args.source_id or "SRC-INBOX", out_path)
    print(f"[+] Exported {res.get('discourse_unit_count', 0)} Discourse Units to {out_path}")

def cmd_stage_batch(args):
    """Validates an AI-synthesized batch and stages candidate preview files."""
    from engine.adapters.hybrid_batch_orchestrator import HybridBatchOrchestrator
    orchestrator = HybridBatchOrchestrator(REPO_ROOT)
    batch_dir = Path(args.batch_dir).resolve()
    
    # Load existing source hashes from SQLite
    existing_hashes = []
    db_path = REPO_ROOT / "workspace" / "rie_substrate.db"
    if db_path.exists():
        import sqlite3
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        try:
            cur.execute("SELECT Transcript_SHA256 FROM DATA_SOURCE WHERE Transcript_SHA256 IS NOT NULL")
            existing_hashes = [r[0] for r in cur.fetchall()]
        except Exception:
            pass
        finally:
            conn.close()
            
    res = orchestrator.process_llm_staged_batch(batch_dir, tx_id=args.tx_id, existing_source_hashes=existing_hashes)
    print(f"[+] Batch validated and staged at: {res.get('transaction_directory')}")
    print(f"    Counts: {res.get('counts')}")
    
    if args.commit:
        from engine.adapters.excel_ssot_adapter import ExcelSSOTAdapter
        wb_path = REPO_ROOT / "workspace" / "RIE_COMMAND_CENTER.xlsx"
        tx_path = Path(res.get("transaction_directory"))
        adapter = ExcelSSOTAdapter(wb_path, tx_path)
        adapter.execute_append_all_staged()
        print(f"[+] Committed candidates to {wb_path.name}")
        # Auto sync SQLite
        from engine.adapters.sqlite_sidecar_adapter import SQLiteSidecarAdapter
        SQLiteSidecarAdapter(wb_path, db_path).build_from_excel_ssot()
        print(f"[+] Auto-synchronized SQLite sidecar")

def cmd_approve(args):
    """Promotes candidate objects in transaction to CANONICAL."""
    from engine.adapters.excel_ssot_adapter import ExcelSSOTAdapter
    wb_path = REPO_ROOT / "workspace" / "RIE_COMMAND_CENTER.xlsx"
    tx_id = args.tx_id.strip()
    
    adapter = ExcelSSOTAdapter(wb_path)
    res = adapter.promote_candidates_to_canonical(tx_id, ratified_by=args.by or "Human Architect")
    print(f"[+] Ratified transaction {tx_id}: {res.get('status')}")
    print(f"    Promoted counts: {res.get('promoted_counts')}")
    
    # Auto-sync SQLite
    db_path = REPO_ROOT / "workspace" / "rie_substrate.db"
    from engine.adapters.sqlite_sidecar_adapter import SQLiteSidecarAdapter
    SQLiteSidecarAdapter(wb_path, db_path).build_from_excel_ssot()
    print(f"[+] Re-synchronized SQLite sidecar")

def cmd_rc_audit(args):
    """Executes the 6-Gate Release Candidate Audit."""
    from engine.adapters.rc_auditor import RCAuditor
    auditor = RCAuditor(REPO_ROOT)
    success, report = auditor.run_all_audits()
    print(report)
    if not success:
        sys.exit(1)

def cmd_release_manifest(args):
    """Generates RELEASE_MANIFEST_v1.0.md with file inventory and checksums."""
    from engine.adapters.rc_auditor import RCAuditor
    auditor = RCAuditor(REPO_ROOT)
    manifest_path = REPO_ROOT / "RELEASE_MANIFEST_v1.0.md"
    auditor.generate_release_manifest(manifest_path)
    print(f"[+] Generated release manifest: {manifest_path}")

def main():
    parser = argparse.ArgumentParser(description="RIE Portable OS CLI Dispatcher (v1.0.0)")
    sub = parser.add_subparsers(dest="command")
    
    # init
    p_init = sub.add_parser("init", help="Initialize or reset workspace")
    p_init.add_argument("--reset", action="store_true", help="Overwrite existing workbook from template")
    
    # doctor
    sub.add_parser("doctor", help="Check system health, dependencies, and configuration")
    
    # query
    p_q = sub.add_parser("query", help="Query knowledge graph sidecar")
    p_q.add_argument("term", help="Search term or KO_ID")
    p_q.add_argument("--depth", type=int, default=3, help="Max traversal depth")
    
    # sync
    p_s = sub.add_parser("sync", help="Synchronize SQLite sidecar and optional Obsidian vault from Excel")
    p_s.add_argument("--vault", action="store_true", help="Also export Obsidian vault")
    
    # export-dul
    p_dul = sub.add_parser("export-dul", help="Export Discourse Unit Layer (DUL) from text or transcript")
    p_dul.add_argument("source", help="Source file (.txt, .md, .json)")
    p_dul.add_argument("--out", required=True, help="Output JSON path")
    p_dul.add_argument("--source-id", default=None, help="Optional source ID")
    
    # stage-batch
    p_sb = sub.add_parser("stage-batch", help="Validate and stage Frontier AI batch")
    p_sb.add_argument("batch_dir", help="Path to batch directory containing EO/IO/KO_BATCH.json")
    p_sb.add_argument("--tx-id", default=None, help="Optional transaction ID")
    p_sb.add_argument("--commit", action="store_true", help="Also append validated candidates into Excel")
    
    # approve
    p_app = sub.add_parser("approve", help="Ratify candidate transaction into CANONICAL")
    p_app.add_argument("tx_id", help="Transaction ID to approve")
    p_app.add_argument("--by", default="Human Architect", help="Ratifying authority name")
    
    # rc-audit
    sub.add_parser("rc-audit", help="Run the mandatory 6-Gate Release Candidate Audit (RC-01..RC-06)")
    
    # release-manifest
    sub.add_parser("release-manifest", help="Generate or update RELEASE_MANIFEST_v1.0.md")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    cmds = {
        "init": cmd_init,
        "doctor": cmd_doctor,
        "query": cmd_query,
        "sync": cmd_sync,
        "export-dul": cmd_export_dul,
        "stage-batch": cmd_stage_batch,
        "approve": cmd_approve,
        "rc-audit": cmd_rc_audit,
        "release-manifest": cmd_release_manifest,
    }
    
    cmds[args.command](args)

if __name__ == "__main__":
    main()

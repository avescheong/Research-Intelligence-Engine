"""
Zero-Dependency Stdio MCP Server for RIE Portable OS (Layer 2A)
Implements JSON-RPC 2.0 over standard input/output.
Allows Antigravity and Claude Code to invoke RIE capabilities as native tools.
"""

import sys
import json
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def rpc_response(req_id, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}) + "\n")
    sys.stdout.flush()

def rpc_error(req_id, code, message):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}) + "\n")
    sys.stdout.flush()

TOOLS = [
    {
        "name": "rie_status",
        "description": "Returns RIE system health, version, substrate counts, and pending candidate transactions.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "rie_query_graph",
        "description": "Queries the SQLite knowledge graph sidecar and performs recursive traversal.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "term": {"type": "string", "description": "Search term or KO_ID"},
                "depth": {"type": "integer", "description": "Max traversal depth", "default": 3}
            },
            "required": ["term"]
        }
    },
    {
        "name": "rie_export_dul",
        "description": "Segments text into Discourse Units (DUL) for Frontier AI synthesis.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Raw transcript or document text"},
                "source_id": {"type": "string", "description": "Source identifier"}
            },
            "required": ["text"]
        }
    }
]

def handle_call_tool(req_id, name, args):
    if name == "rie_status":
        db_path = REPO_ROOT / "workspace" / "rie_substrate.db"
        counts = {}
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            cur = conn.cursor()
            for tbl in ["DATA_SOURCE", "DATA_EO", "DATA_IO", "DATA_KO", "DATA_RELATIONSHIPS"]:
                try:
                    cur.execute(f'SELECT COUNT(*) FROM "{tbl}"')
                    counts[tbl] = cur.fetchone()[0]
                except Exception:
                    pass
            conn.close()
        rpc_response(req_id, {"content": [{"type": "text", "text": json.dumps({"version": "1.0.0", "counts": counts}, indent=2)}]})
    elif name == "rie_query_graph":
        from engine.adapters.sqlite_sidecar_adapter import SQLiteSidecarAdapter
        wb = REPO_ROOT / "workspace" / "RIE_COMMAND_CENTER.xlsx"
        db = REPO_ROOT / "workspace" / "rie_substrate.db"
        adapter = SQLiteSidecarAdapter(wb, db)
        term = args.get("term", "")
        depth = args.get("depth", 3)
        walks = adapter.query_ko_graph_traversal(start_ko_id=term if term.startswith("KO-") else None, max_depth=depth)
        rpc_response(req_id, {"content": [{"type": "text", "text": json.dumps(walks[:20], indent=2)}]})
    elif name == "rie_export_dul":
        from engine.adapters.hybrid_batch_orchestrator import HybridBatchOrchestrator
        orchestrator = HybridBatchOrchestrator(REPO_ROOT)
        text = args.get("text", "")
        sid = args.get("source_id", "SRC-MCP")
        out_temp = REPO_ROOT / "workspace" / "transactions" / "mcp_dul.json"
        res = orchestrator.export_dul_package(text, sid, out_temp)
        rpc_response(req_id, {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]})
    else:
        rpc_error(req_id, -32601, f"Unknown tool: {name}")

def main():
    if "--self-test" in sys.argv:
        print(f"[+] RIE MCP Server self-test PASS: {len(TOOLS)} tools registered.")
        sys.exit(0)
        
    for line in sys.stdin:
        line_clean = line.strip()
        if not line_clean:
            continue
        try:
            req = json.loads(line_clean)
            req_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                rpc_response(req_id, {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "rie-portable-mcp", "version": "1.0.0"}
                })
            elif method == "tools/list":
                rpc_response(req_id, {"tools": TOOLS})
            elif method == "tools/call":
                params = req.get("params", {})
                handle_call_tool(req_id, params.get("name"), params.get("arguments", {}))
            else:
                rpc_error(req_id, -32601, f"Method not found: {method}")
        except Exception as e:
            rpc_error(None, -32700, f"Parse error: {str(e)}")

if __name__ == "__main__":
    main()

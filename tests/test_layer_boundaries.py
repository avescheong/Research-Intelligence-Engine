"""
Layer 1 Boundary AST Test
Verifies that engine/core/ has zero imports of openpyxl, sqlite3, or engine.adapters,
enforcing strict decoupling between Layer 1 and Layer 3.
"""

import ast
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

class TestLayerBoundaries(unittest.TestCase):
    def test_layer1_has_no_storage_or_adapter_imports(self):
        core_dir = REPO_ROOT / "engine" / "core"
        banned = ["openpyxl", "sqlite3", "engine.adapters", "engine.mcp_server", "engine.cli"]
        
        for py_file in core_dir.glob("*.py"):
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        for b in banned:
                            self.assertFalse(
                                alias.name == b or alias.name.startswith(b + "."),
                                f"Layer 1 violation in {py_file.name}: imports banned module '{alias.name}'"
                            )
                elif isinstance(node, ast.ImportFrom):
                    mod = node.module or ""
                    for b in banned:
                        self.assertFalse(
                            mod == b or mod.startswith(b + "."),
                            f"Layer 1 violation in {py_file.name}: imports from banned module '{mod}'"
                        )

if __name__ == "__main__":
    unittest.main()

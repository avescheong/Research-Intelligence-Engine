"""
RIE Core Port Contracts (Layer 1 Specification)
Defines abstract protocols for storage, graph, and format adapters.
Core engine modules depend solely on these abstract ports, ensuring zero
coupling to openpyxl, sqlite3, or specific filesystem paths.
"""

from typing import Protocol, Dict, Any, List, Optional, Tuple, runtime_checkable
from pathlib import Path

@runtime_checkable
class SubstrateReaderPort(Protocol):
    """Abstract interface for querying the human Single Source of Truth."""
    def get_existing_source_hashes(self) -> List[str]:
        ...
    def get_existing_ids(self) -> Dict[str, List[str]]:
        ...
    def get_row_counts(self) -> Dict[str, int]:
        ...

@runtime_checkable
class SubstrateWriterPort(Protocol):
    """Abstract interface for committing candidate intelligence into the substrate."""
    def commit_candidates(self, transaction_dir: Path, tx_id: str) -> Dict[str, Any]:
        ...
    def promote_to_canonical(self, tx_id: str, ratified_by: str) -> Dict[str, Any]:
        ...

@runtime_checkable
class GraphSidecarPort(Protocol):
    """Abstract interface for querying and synchronizing the graph sidecar."""
    def sync_from_ssot(self) -> Dict[str, Any]:
        ...
    def query_graph_traversal(self, start_ko_id: Optional[str] = None, max_depth: int = 3) -> List[Dict[str, Any]]:
        ...

@runtime_checkable
class VaultExporterPort(Protocol):
    """Abstract interface for compiling atomic Markdown notes into a knowledge vault."""
    def export_vault(self, output_dir: Path) -> Dict[str, Any]:
        ...

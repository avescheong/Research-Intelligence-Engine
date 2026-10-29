"""
RIE Core Epistemic Kernel (Layer 1)
Pure, deterministic verification and semantic synthesis logic.
Zero dependencies on external storage libraries or physical workspace paths.
"""

from .discourse_segmenter import DiscourseSegmenter
from .cardinality_controller import CardinalityController
from .taxonomy_loader import TaxonomyLoader
from .semantic_eo_engine import SemanticEOEngine
from .dialectical_io_engine import DialecticalIOEngine
from .conceptual_ko_engine import ConceptualKOEngine
from .contradiction_engine import ContradictionEngine
from .semantic_pipeline import SemanticPipeline
from .semantic_validator import SemanticValidator
from .structural_validator import StructuralValidator
from .ports import SubstrateReaderPort, SubstrateWriterPort, GraphSidecarPort, VaultExporterPort

__all__ = [
    "DiscourseSegmenter",
    "CardinalityController",
    "TaxonomyLoader",
    "SemanticEOEngine",
    "DialecticalIOEngine",
    "ConceptualKOEngine",
    "ContradictionEngine",
    "SemanticPipeline",
    "SemanticValidator",
    "StructuralValidator",
    "SubstrateReaderPort",
    "SubstrateWriterPort",
    "GraphSidecarPort",
    "VaultExporterPort",
]

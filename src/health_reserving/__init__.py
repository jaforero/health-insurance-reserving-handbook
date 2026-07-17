"""Reusable educational tools for health-insurance reserving."""

from .bornhuetter_ferguson import (
    PRIOR_MODE_LABELS,
    BornhuetterFergusonConfig,
    BornhuetterFergusonResult,
    PriorMode,
    fit_bornhuetter_ferguson,
)
from .chain_ladder import (
    SELECTION_LABELS,
    ChainLadderConfig,
    ChainLadderResult,
    TrianglePackage,
    compare_factor_methods,
    fit_chain_ladder,
    load_demo5_triangle_package,
)
from .config import TriangleConfig
from .export import build_chain_ladder_zip, build_results_zip
from .ingestion import excel_sheet_names, read_tabular_file
from .triangles import TriangleResult, build_triangles, evaluate_readiness_gates
from .validation import (
    PreparedClaims,
    ValidationIssue,
    parse_date_series,
    prepare_and_validate_claims,
)

__all__ = [
    "PRIOR_MODE_LABELS",
    "SELECTION_LABELS",
    "BornhuetterFergusonConfig",
    "BornhuetterFergusonResult",
    "ChainLadderConfig",
    "ChainLadderResult",
    "PreparedClaims",
    "PriorMode",
    "TriangleConfig",
    "TrianglePackage",
    "TriangleResult",
    "ValidationIssue",
    "build_results_zip",
    "build_chain_ladder_zip",
    "build_triangles",
    "compare_factor_methods",
    "evaluate_readiness_gates",
    "excel_sheet_names",
    "fit_chain_ladder",
    "fit_bornhuetter_ferguson",
    "load_demo5_triangle_package",
    "parse_date_series",
    "prepare_and_validate_claims",
    "read_tabular_file",
]

__version__ = "0.4.0"

"""Reusable educational tools for health-insurance reserving."""

from .config import TriangleConfig
from .export import build_results_zip
from .ingestion import excel_sheet_names, read_tabular_file
from .triangles import TriangleResult, build_triangles, evaluate_readiness_gates
from .validation import (
    PreparedClaims,
    ValidationIssue,
    parse_date_series,
    prepare_and_validate_claims,
)

__all__ = [
    "PreparedClaims",
    "TriangleConfig",
    "TriangleResult",
    "ValidationIssue",
    "build_results_zip",
    "build_triangles",
    "evaluate_readiness_gates",
    "excel_sheet_names",
    "parse_date_series",
    "prepare_and_validate_claims",
    "read_tabular_file",
]

__version__ = "0.1.1"

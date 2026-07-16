#!/usr/bin/env python3
"""Tests for the reusable Demo 5 triangle engine."""

from __future__ import annotations

import io
import sys
import unittest
import zipfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from health_reserving import (  # noqa: E402
    TriangleConfig,
    build_results_zip,
    build_triangles,
    prepare_and_validate_claims,
    read_tabular_file,
)


def valid_config(**overrides) -> TriangleConfig:
    values = {
        "origin_column": "origen",
        "movement_column": "movimiento",
        "amount_column": "importe",
        "valuation_date": "2024-03-31",
        "frequency": "M",
        "maximum_development": 2,
        "allow_negative_amounts": False,
        "obligation_defined": True,
        "origin_semantics_confirmed": True,
        "movement_semantics_confirmed": True,
        "amount_semantics_confirmed": True,
        "complete_through_valuation": True,
        "representative_history": False,
    }
    values.update(overrides)
    return TriangleConfig(**values)


class UserTriangleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.claims = pd.DataFrame(
            {
                "origen": [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-02-01",
                    "2024-02-01",
                    "2024-03-01",
                ],
                "movimiento": [
                    "2024-01-15",
                    "2024-03-10",
                    "2024-02-10",
                    "2024-03-20",
                    "2024-03-25",
                ],
                "importe": [100.0, 50.0, 120.0, 20.0, 130.0],
            }
        )

    def test_observed_zeros_are_distinct_from_future_cells(self) -> None:
        prepared = prepare_and_validate_claims(self.claims, valid_config())
        self.assertFalse(prepared.has_blocking_issues)
        result = build_triangles(prepared, valid_config())

        self.assertEqual(result.incremental.loc["2024-01", "dev_1"], 0.0)
        self.assertTrue(pd.isna(result.incremental.loc["2024-02", "dev_2"]))
        self.assertEqual(result.cumulative.loc["2024-01", "dev_2"], 150.0)
        self.assertEqual(result.cumulative.loc["2024-02", "dev_1"], 140.0)
        self.assertTrue(pd.isna(result.cumulative.loc["2024-02", "dev_2"]))
        self.assertTrue(result.reconciled)

    def test_negative_amounts_require_explicit_confirmation(self) -> None:
        claims = self.claims.copy()
        claims.loc[0, "importe"] = -100.0
        blocked = prepare_and_validate_claims(claims, valid_config())
        self.assertIn("IMPORTES_NEGATIVOS", {issue.code for issue in blocked.blocking_issues})

        accepted_config = valid_config(allow_negative_amounts=True)
        accepted = prepare_and_validate_claims(claims, accepted_config)
        self.assertFalse(accepted.has_blocking_issues)
        result = build_triangles(accepted, accepted_config)
        self.assertTrue(result.reconciled)

    def test_duplicates_block_triangle_construction(self) -> None:
        claims = pd.concat([self.claims, self.claims.iloc[[0]]], ignore_index=True)
        prepared = prepare_and_validate_claims(claims, valid_config())
        self.assertIn("DUPLICADO_EXACTO", {issue.code for issue in prepared.blocking_issues})
        with self.assertRaises(ValueError):
            build_triangles(prepared, valid_config())

    def test_semantic_confirmations_are_non_compensatory(self) -> None:
        config = valid_config(origin_semantics_confirmed=False)
        prepared = prepare_and_validate_claims(self.claims, config)
        self.assertIn("SEM_ORIGEN", {issue.code for issue in prepared.blocking_issues})

    def test_maximum_development_cannot_truncate_observed_data(self) -> None:
        config = valid_config(maximum_development=1)
        prepared = prepare_and_validate_claims(self.claims, config)
        with self.assertRaisesRegex(ValueError, "excluye movimientos observados"):
            build_triangles(prepared, config)

    def test_segment_filter_is_applied_before_triangle(self) -> None:
        claims = self.claims.copy()
        claims["segmento"] = ["A", "A", "B", "B", "A"]
        config = valid_config(segment_column="segmento", segment_value="A")
        prepared = prepare_and_validate_claims(claims, config)
        result = build_triangles(prepared, config)
        self.assertEqual(len(prepared.data), 3)
        self.assertAlmostEqual(result.incremental.sum().sum(), 280.0)

    def test_zip_excludes_record_level_detail_by_default(self) -> None:
        config = valid_config()
        prepared = prepare_and_validate_claims(self.claims, config)
        result = build_triangles(prepared, config)
        package = build_results_zip(prepared, result, config)
        with zipfile.ZipFile(io.BytesIO(package)) as archive:
            names = set(archive.namelist())
        self.assertIn("03_triangulo_incremental.csv", names)
        self.assertIn("09_manifiesto.json", names)
        self.assertNotIn("10_datos_canonicos_detalle.csv", names)

    def test_csv_reader_accepts_in_memory_upload(self) -> None:
        source = io.BytesIO(b"origen,movimiento,importe\n2024-01-01,2024-01-02,100\n")
        frame = read_tabular_file(source, "datos.csv")
        self.assertEqual(frame.shape, (1, 3))

    def test_csv_reader_can_detect_separator(self) -> None:
        source = io.BytesIO(b"origen;movimiento;importe\n2024-01-01;2024-01-02;100\n")
        frame = read_tabular_file(source, "datos.csv", separator="auto")
        self.assertEqual(list(frame.columns), ["origen", "movimiento", "importe"])


if __name__ == "__main__":
    unittest.main()

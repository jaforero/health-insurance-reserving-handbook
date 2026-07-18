#!/usr/bin/env python3
"""Regression tests for the monthly triangle demo."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_demo_monthly_triangles.py"
SPEC = importlib.util.spec_from_file_location("monthly_demo", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {SCRIPT}")
monthly_demo = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = monthly_demo
SPEC.loader.exec_module(monthly_demo)


class MonthlyTriangleDemoTest(unittest.TestCase):
    def setUp(self) -> None:
        self.valuation = monthly_demo.parse_month(monthly_demo.DEFAULT_VALUATION_MONTH)
        self.result = monthly_demo.build_demo(
            valuation_index=self.valuation,
            origin_months=monthly_demo.DEFAULT_ORIGIN_MONTHS,
            development_months=monthly_demo.DEFAULT_DEVELOPMENT_MONTHS,
            seed=monthly_demo.DEFAULT_SEED,
            runoff_months=monthly_demo.DEFAULT_RUNOFF_MONTHS,
        )

    def test_default_design_counts(self) -> None:
        self.assertEqual(len(self.result.origins), 72)
        self.assertEqual(self.result.observed_cells, 1962)
        self.assertEqual(self.result.complete_origins, 37)
        self.assertEqual(min(int(row["observations"]) for row in self.result.factors), 37)
        self.assertEqual(self.result.terminal_age, 35)
        self.assertEqual(self.result.runoff_age, 48)

    def test_triangle_reconciliation(self) -> None:
        for record in self.result.origins:
            running = 0.0
            for dev, value in self.result.incremental[record.origin_month].items():
                running += value
                self.assertAlmostEqual(running, self.result.cumulative[record.origin_month][dev], places=2)
            self.assertAlmostEqual(sum(record.increments), record.ultimate_paid, places=2)

    def test_traditional_view_is_36_by_36(self) -> None:
        origins = monthly_demo.traditional_view_origins(self.result)
        rows = monthly_demo.triangle_rows(
            self.result.cumulative,
            self.result.terminal_age,
            "mes_origen",
            origins,
        )
        self.assertEqual(len(rows), 36)
        self.assertEqual(len(rows[0]), 37)  # origin label plus 36 development columns
        self.assertEqual(sum(value != "" for value in rows[-1].values()), 2)

    def test_tail_is_explicit_and_residual_is_not_floored(self) -> None:
        self.assertGreater(self.result.synthetic_tail_factor, 1.0)
        first = self.result.estimates[0]
        self.assertIn("estimated_unpaid_claim_liability", first)
        self.assertIn("estimated_final_cost_with_tail", first)
        self.assertNotIn("estimated_ibnr", first)
        self.assertAlmostEqual(
            float(first["estimated_unpaid_claim_liability"]),
            float(first["estimated_final_cost_with_tail"])
            - float(first["latest_cumulative_paid"]),
            places=2,
        )

    def test_outputs_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            roots = (Path(first), Path(second))
            for root in roots:
                monthly_demo.write_language_data(
                    self.result,
                    root,
                    "es",
                    seed=monthly_demo.DEFAULT_SEED,
                )
            relative = Path(
                "data/demo_triangulos_mensuales/resultados_proyeccion_pasivo_no_pagado.csv"
            )
            digests = [hashlib.sha256((root / relative).read_bytes()).hexdigest() for root in roots]
            self.assertEqual(digests[0], digests[1])

    def test_result_headers_do_not_claim_pure_ibnr(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            monthly_demo.write_language_data(
                self.result,
                root,
                "es",
                seed=monthly_demo.DEFAULT_SEED,
            )
            header = (
                root
                / "data/demo_triangulos_mensuales/resultados_proyeccion_pasivo_no_pagado.csv"
            ).read_text(encoding="utf-8").splitlines()[0]
            self.assertIn("pasivo_no_pagado_estimado", header)
            self.assertNotIn("ibnr_estimado", header.lower())


if __name__ == "__main__":
    unittest.main()

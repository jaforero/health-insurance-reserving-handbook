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
            origin_months=60,
            development_months=24,
            seed=monthly_demo.DEFAULT_SEED,
        )

    def test_default_design_counts(self) -> None:
        self.assertEqual(len(self.result.origins), 60)
        self.assertEqual(self.result.observed_cells, 1200)
        self.assertEqual(self.result.complete_origins, 36)
        self.assertEqual(min(int(row["observations"]) for row in self.result.factors), 36)

    def test_triangle_reconciliation(self) -> None:
        for record in self.result.origins:
            running = 0.0
            for dev, value in self.result.incremental[record.origin_month].items():
                running += value
                self.assertAlmostEqual(running, self.result.cumulative[record.origin_month][dev], places=2)
            self.assertAlmostEqual(sum(record.increments), record.ultimate_paid, places=2)

    def test_outputs_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            roots = (Path(first), Path(second))
            for root in roots:
                monthly_demo.write_language_data(
                    self.result,
                    root,
                    "es",
                    development_months=24,
                    seed=monthly_demo.DEFAULT_SEED,
                )
            relative = Path("data/demo_triangulos_mensuales/resultados_chain_ladder_mensual.csv")
            digests = [hashlib.sha256((root / relative).read_bytes()).hexdigest() for root in roots]
            self.assertEqual(digests[0], digests[1])


if __name__ == "__main__":
    unittest.main()

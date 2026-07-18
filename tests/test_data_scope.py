"""Tests for the explicit input-scope assessment rendered by Demo 6."""

from __future__ import annotations

import unittest

import pandas as pd

from health_reserving.data_scope import assess_triangle_input


class InputScopeAssessmentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.triangle = pd.DataFrame(
            [[100.0, 140.0, 160.0], [110.0, 150.0, None], [120.0, None, None]],
            index=pd.Index(["2024-01", "2024-02", "2024-03"], name="periodo_origen"),
            columns=["dev_0", "dev_1", "dev_2"],
        )
        self.mask = self.triangle.notna()

    def test_paid_triangle_never_claims_pure_ibnr(self) -> None:
        assessment = assess_triangle_input(
            self.triangle,
            self.mask,
            triangle_config={"measure": "PAGADO_ACUMULADO", "currency": "COP"},
            manifest={"reconciliado": True},
        )
        scope = assessment.calculation_scope.set_index("resultado")
        pure = scope.loc["IBNR puro, RBNS e IBNER por separado"]
        self.assertEqual(pure["estado"], "NO IDENTIFICABLE")
        self.assertIn("no calculable", pure["nombre_preciso"].lower())

    def test_received_table_reports_actual_shape_and_observed_cells(self) -> None:
        assessment = assess_triangle_input(self.triangle, self.mask)
        received = assessment.received.set_index("elemento")
        self.assertIn("3 periodos de origen × 3 edades", received.loc["Triángulo acumulado agregado", "detalle"])
        self.assertIn("6 celdas", received.loc["Celdas observadas", "detalle"])

    def test_missing_table_identifies_tail_and_claim_report_data(self) -> None:
        assessment = assess_triangle_input(self.triangle, self.mask)
        missing = " ".join(assessment.missing_desirable["elemento"].tolist()).lower()
        self.assertIn("fecha de reporte", missing)
        self.assertIn("factor de cola", missing)

    def test_dimension_mismatch_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "misma dimensión"):
            assess_triangle_input(self.triangle, self.mask.iloc[:, :2])


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Tests for the reusable deterministic Chain Ladder engine."""

from __future__ import annotations

import io
import unittest
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from health_reserving import (
    ChainLadderConfig,
    TriangleConfig,
    build_chain_ladder_zip,
    build_results_zip,
    build_triangles,
    compare_factor_methods,
    fit_chain_ladder,
    load_demo5_triangle_package,
    prepare_and_validate_claims,
)


ROOT = Path(__file__).resolve().parents[1]


def example_triangle() -> tuple[pd.DataFrame, pd.DataFrame]:
    cumulative = pd.DataFrame(
        {
            "dev_0": [100.0, 120.0, 130.0],
            "dev_1": [150.0, 168.0, np.nan],
            "dev_2": [180.0, np.nan, np.nan],
        },
        index=pd.Index(["2022", "2023", "2024"], name="periodo_origen"),
    )
    return cumulative, cumulative.notna()


class ChainLadderTest(unittest.TestCase):
    def test_volume_weighted_example_matches_handbook(self) -> None:
        cumulative, mask = example_triangle()
        result = fit_chain_ladder(cumulative, mask)

        factor_0 = (150.0 + 168.0) / (100.0 + 120.0)
        self.assertAlmostEqual(result.selected_factors.loc["dev_0->dev_1"], factor_0)
        self.assertAlmostEqual(result.selected_factors.loc["dev_1->dev_2"], 1.2)
        self.assertAlmostEqual(result.origin_summary.loc["2024", "ultimate"], 130 * factor_0 * 1.2)
        self.assertAlmostEqual(result.origin_summary.loc["2023", "ibnr"], 168 * 0.2)
        self.assertAlmostEqual(
            result.origin_summary.loc["2023", "pasivo_no_pagado_estimado"],
            result.origin_summary.loc["2023", "ibnr"],
        )
        self.assertAlmostEqual(
            result.origin_summary.loc["2023", "costo_proyectado_horizonte_seleccionado"],
            result.origin_summary.loc["2023", "ultimate"],
        )
        self.assertAlmostEqual(
            result.projected_cumulative.loc["2024", "dev_2"], 130 * factor_0 * 1.2
        )
        self.assertAlmostEqual(
            result.projected_incremental.loc["2024", "dev_1"], 130 * factor_0 - 130
        )

    def test_manual_selection_and_tail_are_explicit(self) -> None:
        cumulative, mask = example_triangle()
        config = ChainLadderConfig(
            selection_method="manual",
            manual_factors={"dev_0->dev_1": 1.5, "dev_1->dev_2": 1.25},
            tail_factor=1.1,
        )
        result = fit_chain_ladder(cumulative, mask, config)

        self.assertAlmostEqual(result.cdf_to_ultimate.loc["dev_0"], 1.5 * 1.25 * 1.1)
        self.assertAlmostEqual(result.cdf_to_ultimate.loc["dev_2"], 1.1)
        self.assertAlmostEqual(result.origin_summary.loc["2022", "ultimate"], 180 * 1.1)
        self.assertEqual(
            result.factor_summary["metodo_seleccion"].unique().tolist(), ["Selección manual"]
        )

    def test_automatic_methods_produce_traceable_sensitivity(self) -> None:
        cumulative, mask = example_triangle()
        sensitivity = compare_factor_methods(cumulative, mask)

        self.assertEqual(
            sensitivity["metodo"].tolist(),
            ["volume_weighted", "simple_mean", "median", "latest_3"],
        )
        baseline = sensitivity.loc[
            sensitivity["metodo"].eq("volume_weighted"), "diferencia_ibnr_vs_ponderado"
        ].iloc[0]
        self.assertAlmostEqual(baseline, 0.0)

    def test_future_values_and_internal_gaps_are_rejected(self) -> None:
        cumulative, mask = example_triangle()
        future_filled = cumulative.copy()
        future_filled.loc["2024", "dev_1"] = 170.0
        with self.assertRaisesRegex(ValueError, "celdas futuras"):
            fit_chain_ladder(future_filled, mask)

        gap_mask = mask.copy()
        gap_triangle = cumulative.copy()
        gap_mask.loc["2022", "dev_1"] = False
        gap_triangle.loc["2022", "dev_1"] = np.nan
        with self.assertRaisesRegex(ValueError, "vacíos dentro"):
            fit_chain_ladder(gap_triangle, gap_mask)

    def test_missing_link_and_manual_factor_are_blocking(self) -> None:
        cumulative, mask = example_triangle()
        mask.loc["2022", "dev_2"] = False
        cumulative.loc["2022", "dev_2"] = np.nan
        with self.assertRaisesRegex(ValueError, "No existen pares válidos"):
            fit_chain_ladder(cumulative, mask)

        with self.assertRaisesRegex(ValueError, "Falta el factor manual"):
            fit_chain_ladder(
                *example_triangle(),
                ChainLadderConfig(
                    selection_method="manual",
                    manual_factors={"dev_0->dev_1": 1.4},
                ),
            )

    def test_demo5_package_is_verified_and_loaded(self) -> None:
        claims = pd.DataFrame(
            {
                "origen": ["2024-01-01", "2024-01-01", "2024-02-01"],
                "movimiento": ["2024-01-10", "2024-02-10", "2024-02-15"],
                "importe": [100.0, 50.0, 120.0],
            }
        )
        config = TriangleConfig(
            origin_column="origen",
            movement_column="movimiento",
            amount_column="importe",
            valuation_date="2024-02-29",
            frequency="M",
            maximum_development=1,
            obligation_defined=True,
            origin_semantics_confirmed=True,
            movement_semantics_confirmed=True,
            amount_semantics_confirmed=True,
            complete_through_valuation=True,
            representative_history=True,
        )
        prepared = prepare_and_validate_claims(claims, config)
        triangles = build_triangles(prepared, config)
        package = build_results_zip(prepared, triangles, config)
        loaded = load_demo5_triangle_package(io.BytesIO(package))

        pd.testing.assert_frame_equal(loaded.cumulative, triangles.cumulative)
        pd.testing.assert_frame_equal(loaded.observed_mask, triangles.observed_mask)
        self.assertTrue(loaded.manifest["reconciliado"])

    def test_invalid_package_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "ZIP válido"):
            load_demo5_triangle_package(b"not-a-zip")

    def test_chain_ladder_export_contains_auditable_aggregate_outputs(self) -> None:
        cumulative, mask = example_triangle()
        config = ChainLadderConfig()
        result = fit_chain_ladder(cumulative, mask, config)
        package = build_chain_ladder_zip(result, config)

        with zipfile.ZipFile(io.BytesIO(package)) as archive:
            names = set(archive.namelist())
        self.assertIn("03_factores_individuales.csv", names)
        self.assertIn("08_resultados_por_origen.csv", names)
        self.assertIn("13_informacion_recibida.csv", names)
        self.assertIn("14_informacion_faltante_deseable.csv", names)
        self.assertIn("15_alcance_calculable.csv", names)
        with zipfile.ZipFile(io.BytesIO(package)) as archive:
            results_header = archive.read("08_resultados_por_origen.csv").decode("utf-8").splitlines()[0]
            self.assertIn("pasivo_no_pagado_estimado", results_header)
            self.assertIn("costo_proyectado_horizonte_seleccionado", results_header)
            self.assertNotIn("costo_final_estimado", results_header)
            self.assertNotIn(",ibnr,", f",{results_header},")
        self.assertIn("12_manifiesto.json", names)
        self.assertNotIn("datos_canonicos_detalle.csv", names)

    def test_monthly_example_reconciles_to_published_demo3_outputs(self) -> None:
        data_dir = ROOT / "data" / "demo_triangulos_mensuales"
        cumulative = pd.read_csv(data_dir / "triangulo_pagado_mensual_acumulado.csv", index_col=0)
        published_factors = pd.read_csv(data_dir / "factores_mensuales_edad_a_edad.csv")
        published_results = pd.read_csv(
            data_dir / "resultados_proyeccion_pasivo_no_pagado.csv", index_col=0
        )
        result = fit_chain_ladder(
            cumulative,
            cumulative.notna(),
            ChainLadderConfig(tail_factor=1.0052495821422405),
        )

        np.testing.assert_allclose(
            result.selected_factors.to_numpy(),
            published_factors["factor_edad_a_edad"].to_numpy(),
            rtol=1e-8,
            atol=1e-8,
        )
        np.testing.assert_allclose(
            result.origin_summary["ultimate"].to_numpy(),
            published_results["costo_final_estimado_con_cola"].to_numpy(),
            rtol=1e-8,
            atol=0.02,
        )
        np.testing.assert_allclose(
            result.origin_summary["ibnr"].to_numpy(),
            published_results["pasivo_no_pagado_estimado"].to_numpy(),
            rtol=1e-8,
            atol=0.02,
        )


if __name__ == "__main__":
    unittest.main()

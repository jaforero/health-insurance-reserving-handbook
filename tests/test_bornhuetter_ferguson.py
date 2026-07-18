#!/usr/bin/env python3
"""Tests for the reusable deterministic Bornhuetter-Ferguson engine."""

from __future__ import annotations

import io
import json
import unittest
import zipfile

import numpy as np
import pandas as pd

from health_reserving import (
    BornhuetterFergusonConfig,
    ChainLadderConfig,
    build_classical_methods_zip,
    fit_bornhuetter_ferguson,
    fit_chain_ladder,
)


def handbook_example():
    """Return a two-origin Chain Ladder result with a 2.0 CDF for the latest origin."""

    cumulative = pd.DataFrame(
        {
            "dev_0": [50.0, 100.0],
            "dev_1": [100.0, np.nan],
        },
        index=pd.Index(["2023", "2024"], name="periodo_origen"),
    )
    return fit_chain_ladder(cumulative, cumulative.notna())


def direct_prior() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "periodo_origen": ["2024", "2023"],
            "ultimate_esperado": [180.0, 100.0],
        }
    )


class BornhuetterFergusonTest(unittest.TestCase):
    def test_handbook_example_matches_formula_and_chain_ladder_comparison(self) -> None:
        result = fit_bornhuetter_ferguson(handbook_example(), direct_prior())
        latest = result.origin_summary.loc["2024"]

        self.assertAlmostEqual(latest["cdf_a_ultimate"], 2.0)
        self.assertAlmostEqual(latest["porcentaje_desarrollado"], 0.5)
        self.assertAlmostEqual(latest["porcentaje_no_desarrollado"], 0.5)
        self.assertAlmostEqual(latest["ibnr_bf"], 90.0)
        self.assertAlmostEqual(latest["ultimate_bf"], 190.0)
        self.assertAlmostEqual(latest["ultimate_chain_ladder"], 200.0)
        self.assertAlmostEqual(latest["diferencia_ultimate_bf_vs_cl"], -10.0)
        self.assertAlmostEqual(latest["costo_proyectado_horizonte_seleccionado_bf"], 190.0)
        self.assertAlmostEqual(latest["pasivo_no_pagado_estimado_bf"], 90.0)

    def test_exposure_times_rate_produces_same_expected_ultimate(self) -> None:
        prior = pd.DataFrame(
            {
                "periodo_origen": [2023, 2024],
                "exposicion": [10.0, 20.0],
                "costo_esperado": [10.0, 9.0],
            }
        )
        config = BornhuetterFergusonConfig(
            prior_mode="exposure_rate",
            expected_rate_column="costo_esperado",
        )
        result = fit_bornhuetter_ferguson(handbook_example(), prior, config)

        self.assertAlmostEqual(result.prior_input.loc["2024", "exposicion"], 20.0)
        self.assertAlmostEqual(result.prior_input.loc["2024", "tasa_esperada"], 9.0)
        self.assertAlmostEqual(result.origin_summary.loc["2024", "ultimate_esperado_prior"], 180.0)
        self.assertAlmostEqual(result.origin_summary.loc["2024", "ibnr_bf"], 90.0)

    def test_totals_and_prior_sensitivity_reconcile(self) -> None:
        result = fit_bornhuetter_ferguson(handbook_example(), direct_prior())
        totals = result.totals.set_index("indicador")["valor"]
        sensitivity = result.sensitivity.set_index("shock_prior")

        self.assertAlmostEqual(totals.loc["acumulado_observado_total"], 200.0)
        self.assertAlmostEqual(totals.loc["ultimate_esperado_prior_total"], 280.0)
        self.assertAlmostEqual(totals.loc["ultimate_bf_total"], 290.0)
        self.assertAlmostEqual(totals.loc["ibnr_bf_total"], 90.0)
        self.assertAlmostEqual(totals.loc["ibnr_chain_ladder_total"], 100.0)
        self.assertAlmostEqual(sensitivity.loc[-0.1, "ibnr_bf_total"], 81.0)
        self.assertAlmostEqual(sensitivity.loc[0.0, "ibnr_bf_total"], 90.0)
        self.assertAlmostEqual(sensitivity.loc[0.1, "ibnr_bf_total"], 99.0)
        self.assertAlmostEqual(sensitivity.loc[0.0, "diferencia_ibnr_vs_base"], 0.0)

    def test_prior_origins_must_match_chain_ladder_exactly(self) -> None:
        chain_ladder = handbook_example()
        cases = (
            (
                pd.DataFrame({"periodo_origen": ["2023"], "ultimate_esperado": [100.0]}),
                "faltan: 2024",
            ),
            (
                pd.DataFrame(
                    {
                        "periodo_origen": ["2023", "2024", "2025"],
                        "ultimate_esperado": [100.0, 180.0, 200.0],
                    }
                ),
                "sobran: 2025",
            ),
            (
                pd.DataFrame(
                    {
                        "periodo_origen": ["2023", "2023"],
                        "ultimate_esperado": [100.0, 180.0],
                    }
                ),
                "duplicados",
            ),
        )
        for prior, message in cases:
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                fit_bornhuetter_ferguson(chain_ladder, prior)

    def test_invalid_prior_values_are_blocking(self) -> None:
        cases = (
            ([100.0, "texto"], "no numéricos"),
            ([100.0, np.inf], "no finitos"),
            ([100.0, -1.0], "no puede contener valores negativos"),
        )
        for values, message in cases:
            prior = pd.DataFrame(
                {
                    "periodo_origen": ["2023", "2024"],
                    "ultimate_esperado": values,
                }
            )
            with self.subTest(values=values), self.assertRaisesRegex(ValueError, message):
                fit_bornhuetter_ferguson(handbook_example(), prior)

    def test_duplicate_columns_and_derived_overflow_are_blocking(self) -> None:
        duplicate_columns = pd.DataFrame(
            [["2023", 100.0, 100.0], ["2024", 180.0, 180.0]],
            columns=["periodo_origen", "ultimate_esperado", "ultimate_esperado"],
        )
        with self.assertRaisesRegex(ValueError, "columnas duplicadas"):
            fit_bornhuetter_ferguson(handbook_example(), duplicate_columns)

        overflow = pd.DataFrame(
            {
                "periodo_origen": ["2023", "2024"],
                "exposicion": [1e308, 1e308],
                "tasa_esperada": [2.0, 2.0],
            }
        )
        config = BornhuetterFergusonConfig(prior_mode="exposure_rate")
        with self.assertRaisesRegex(ValueError, "produjo valores no finitos"):
            fit_bornhuetter_ferguson(handbook_example(), overflow, config)

    def test_negative_exposure_and_rate_are_blocking(self) -> None:
        config = BornhuetterFergusonConfig(prior_mode="exposure_rate")
        for column in ("exposicion", "tasa_esperada"):
            prior = pd.DataFrame(
                {
                    "periodo_origen": ["2023", "2024"],
                    "exposicion": [10.0, 20.0],
                    "tasa_esperada": [10.0, 9.0],
                }
            )
            prior.loc[1, column] = -1.0
            with self.subTest(column=column), self.assertRaisesRegex(ValueError, "negativos"):
                fit_bornhuetter_ferguson(handbook_example(), prior, config)

    def test_cdf_below_one_is_preserved_and_diagnosed(self) -> None:
        cumulative = pd.DataFrame(
            {"dev_0": [100.0, 100.0], "dev_1": [80.0, np.nan]},
            index=pd.Index(["2023", "2024"], name="periodo_origen"),
        )
        chain_ladder = fit_chain_ladder(cumulative, cumulative.notna())
        prior = pd.DataFrame(
            {
                "periodo_origen": ["2023", "2024"],
                "ultimate_esperado": [80.0, 160.0],
            }
        )
        result = fit_bornhuetter_ferguson(chain_ladder, prior)
        diagnostics = result.diagnostics.set_index("codigo")

        self.assertAlmostEqual(result.origin_summary.loc["2024", "cdf_a_ultimate"], 0.8)
        self.assertAlmostEqual(
            result.origin_summary.loc["2024", "porcentaje_no_desarrollado"], -0.25
        )
        self.assertAlmostEqual(result.origin_summary.loc["2024", "ibnr_bf"], -40.0)
        self.assertEqual(diagnostics.loc["BF02_CDF_MENORES_1", "nivel"], "ADVERTENCIA")
        self.assertEqual(diagnostics.loc["BF05_PASIVO_NO_PAGADO_NEGATIVO", "valor"], 1)

    def test_inputs_are_not_mutated(self) -> None:
        chain_ladder = handbook_example()
        prior = direct_prior()
        original_summary = chain_ladder.origin_summary.copy(deep=True)
        original_prior = prior.copy(deep=True)

        fit_bornhuetter_ferguson(chain_ladder, prior)

        pd.testing.assert_frame_equal(chain_ladder.origin_summary, original_summary)
        pd.testing.assert_frame_equal(prior, original_prior)

    def test_sensitivity_configuration_requires_unique_base_scenario(self) -> None:
        cases = (
            ((-0.1, 0.1), "escenario base"),
            ((0.0, 0.0), "duplicados"),
            ((-1.0, 0.0), "mayor que -100%"),
        )
        for shocks, message in cases:
            with self.subTest(shocks=shocks), self.assertRaisesRegex(ValueError, message):
                BornhuetterFergusonConfig(sensitivity_shocks=shocks)

        with self.assertRaisesRegex(ValueError, "nombres diferentes"):
            BornhuetterFergusonConfig(
                prior_mode="exposure_rate",
                exposure_column="valor",
                expected_rate_column="valor",
            )

    def test_inconsistent_chain_ladder_summary_is_rejected(self) -> None:
        chain_ladder = handbook_example()
        chain_ladder.origin_summary.loc["2024", "ultimate"] += 1.0

        with self.assertRaisesRegex(ValueError, "no se reconcilian"):
            fit_bornhuetter_ferguson(chain_ladder, direct_prior())

    def test_joint_export_contains_auditable_aggregate_outputs(self) -> None:
        chain_ladder = handbook_example()
        bf_result = fit_bornhuetter_ferguson(chain_ladder, direct_prior())
        package = build_classical_methods_zip(
            chain_ladder,
            ChainLadderConfig(),
            bf_result,
            source_metadata={"tipo": "prueba"},
            prior_metadata={"tipo": "prior_prueba"},
        )

        with zipfile.ZipFile(io.BytesIO(package)) as archive:
            names = set(archive.namelist())
            manifest = json.loads(archive.read("18_manifiesto.json").decode("utf-8"))

        self.assertIn("11_prior_bf_normalizado.csv", names)
        self.assertIn("12_resultados_bf_por_origen.csv", names)
        self.assertIn("14_sensibilidad_prior_bf.csv", names)
        self.assertIn("17_configuracion_bf.json", names)
        self.assertFalse(manifest["incluye_archivos_fuente_originales"])
        self.assertEqual(manifest["fuente_prior"]["tipo"], "prior_prueba")


if __name__ == "__main__":
    unittest.main()

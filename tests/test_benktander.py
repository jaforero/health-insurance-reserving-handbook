#!/usr/bin/env python3
"""Tests for the deterministic and auditable Benktander engine."""

from __future__ import annotations

import io
import json
import unittest
import zipfile

import numpy as np
import pandas as pd

from health_reserving import (
    BenktanderConfig,
    BornhuetterFergusonConfig,
    ChainLadderConfig,
    build_classical_methods_zip,
    fit_benktander,
    fit_bornhuetter_ferguson,
    fit_chain_ladder,
)


def chain_ladder_example():
    cumulative = pd.DataFrame(
        {
            "dev_0": [50.0, 100.0],
            "dev_1": [100.0, np.nan],
        },
        index=pd.Index(["2023", "2024"], name="periodo_origen"),
    )
    return fit_chain_ladder(cumulative, cumulative.notna())


def bf_example():
    prior = pd.DataFrame(
        {
            "periodo_origen": ["2024", "2023"],
            "ultimate_esperado": [180.0, 100.0],
        }
    )
    return fit_bornhuetter_ferguson(chain_ladder_example(), prior)


class BenktanderTest(unittest.TestCase):
    def test_two_iterations_match_recurrence_and_closed_form(self) -> None:
        result = fit_benktander(chain_ladder_example(), bf_example(), BenktanderConfig(iterations=2))
        latest = result.origin_summary.loc["2024"]

        self.assertAlmostEqual(latest["ultimate_benktander_iterativo"], 195.0)
        self.assertAlmostEqual(latest["ultimate_benktander_cerrado"], 195.0)
        self.assertAlmostEqual(latest["ultimate_benktander"], 195.0)
        self.assertAlmostEqual(latest["ibnr_benktander"], 95.0)
        self.assertAlmostEqual(latest["peso_prior_inicial"], 0.25)
        self.assertAlmostEqual(latest["peso_chain_ladder"], 0.75)
        self.assertAlmostEqual(latest["diferencia_formas"], 0.0)
        self.assertAlmostEqual(
            latest["costo_proyectado_horizonte_seleccionado_benktander"], 195.0
        )
        self.assertAlmostEqual(latest["pasivo_no_pagado_estimado_benktander"], 95.0)

    def test_one_iteration_equals_bornhuetter_ferguson(self) -> None:
        bf = bf_example()
        result = fit_benktander(chain_ladder_example(), bf, BenktanderConfig(iterations=1))
        np.testing.assert_allclose(result.origin_summary["ultimate_benktander"], bf.origin_summary["ultimate_bf"])
        np.testing.assert_allclose(result.origin_summary["ibnr_benktander"], bf.origin_summary["ibnr_bf"])

    def test_totals_and_iteration_sensitivity_reconcile(self) -> None:
        result = fit_benktander(chain_ladder_example(), bf_example(), BenktanderConfig(iterations=2))
        totals = result.totals.set_index("indicador")["valor"]
        sensitivity = result.sensitivity.set_index("iteraciones")

        self.assertAlmostEqual(totals.loc["acumulado_observado_total"], 200.0)
        self.assertAlmostEqual(totals.loc["ultimate_benktander_total"], 295.0)
        self.assertAlmostEqual(totals.loc["ibnr_benktander_total"], 95.0)
        self.assertAlmostEqual(totals.loc["diferencia_ibnr_bk_vs_cl_total"], -5.0)
        self.assertAlmostEqual(totals.loc["diferencia_ibnr_bk_vs_bf_total"], 5.0)
        self.assertAlmostEqual(sensitivity.loc[0, "ultimate_total"], 280.0)
        self.assertAlmostEqual(sensitivity.loc[1, "ultimate_total"], 290.0)
        self.assertAlmostEqual(sensitivity.loc[2, "ultimate_total"], 295.0)
        self.assertAlmostEqual(sensitivity.loc[3, "ultimate_total"], 297.5)

    def test_selected_iteration_is_added_to_sensitivity(self) -> None:
        config = BenktanderConfig(iterations=5, sensitivity_iterations=(0, 1, 2, 3))
        self.assertEqual(config.sensitivity_iterations, (0, 1, 2, 3, 5))

    def test_invalid_iteration_configuration_is_blocking(self) -> None:
        cases = (
            ({"iterations": 0}, "entre 1 y 50"),
            ({"iterations": 51}, "entre 1 y 50"),
            ({"iterations": 2.5}, "debe ser un entero"),
            ({"iterations": 2, "sensitivity_iterations": ()}, "al menos una"),
            ({"iterations": 2, "sensitivity_iterations": (0, 0)}, "duplicadas"),
            ({"iterations": 2, "sensitivity_iterations": (0, 51)}, "entre 0 y 50"),
        )
        for kwargs, message in cases:
            with self.subTest(kwargs=kwargs), self.assertRaisesRegex(ValueError, message):
                BenktanderConfig(**kwargs)

    def test_inconsistent_bf_input_is_rejected(self) -> None:
        bf = bf_example()
        bf.origin_summary.loc["2024", "ultimate_bf"] += 1.0
        with self.assertRaisesRegex(ValueError, "no se reconcilia"):
            fit_benktander(chain_ladder_example(), bf)

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
        bf = fit_bornhuetter_ferguson(chain_ladder, prior)
        result = fit_benktander(chain_ladder, bf, BenktanderConfig(iterations=2))
        diagnostics = result.diagnostics.set_index("codigo")

        self.assertAlmostEqual(result.origin_summary.loc["2024", "peso_prior_inicial"], 0.0625)
        self.assertEqual(diagnostics.loc["BK02_CDF_MENORES_1", "nivel"], "ADVERTENCIA")
        self.assertEqual(diagnostics.loc["BK03_PESOS_FUERA_RANGO", "valor"], 0)

    def test_inputs_are_not_mutated(self) -> None:
        chain_ladder = chain_ladder_example()
        bf = bf_example()
        original_cl = chain_ladder.origin_summary.copy(deep=True)
        original_bf = bf.origin_summary.copy(deep=True)

        fit_benktander(chain_ladder, bf)

        pd.testing.assert_frame_equal(chain_ladder.origin_summary, original_cl)
        pd.testing.assert_frame_equal(bf.origin_summary, original_bf)

    def test_joint_export_includes_benktander_without_source_files(self) -> None:
        chain_ladder = chain_ladder_example()
        bf = bf_example()
        benktander = fit_benktander(chain_ladder, bf, BenktanderConfig(iterations=2))
        package = build_classical_methods_zip(
            chain_ladder,
            ChainLadderConfig(),
            bf,
            benktander=benktander,
            source_metadata={"tipo": "prueba"},
            prior_metadata={"tipo": "prior_prueba"},
        )

        with zipfile.ZipFile(io.BytesIO(package)) as archive:
            names = set(archive.namelist())
            manifest = json.loads(archive.read("18_manifiesto.json").decode("utf-8"))

        self.assertIn("19_resultados_benktander_por_origen.csv", names)
        self.assertIn("21_sensibilidad_iteraciones_benktander.csv", names)
        self.assertIn("23_configuracion_benktander.json", names)
        self.assertEqual(manifest["version_motor"], "0.6.0-sprint2-r2")
        self.assertEqual(manifest["configuracion_benktander"]["iterations"], 2)
        self.assertFalse(manifest["incluye_archivos_fuente_originales"])


if __name__ == "__main__":
    unittest.main()

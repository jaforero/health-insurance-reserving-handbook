#!/usr/bin/env python3
"""Smoke test for the local Demo 6 Chain Ladder interface."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps" / "chain_ladder_workshop.py"


class ChainLadderAppTest(unittest.TestCase):
    def test_monthly_example_estimates_and_offers_download(self) -> None:
        app = AppTest.from_file(str(APP), default_timeout=30).run()
        markdown = "\n".join(element.value for element in app.markdown)
        self.assertIn("IgraSans", markdown)
        self.assertIn("jf-hero", markdown)
        self.assertIn("Del triángulo al costo proyectado y pasivo no pagado", markdown)
        self.assertIn(
            "Qué se recibió",
            [tab.label for tab in app.tabs],
        )
        self.assertIn(
            "Qué falta o sería deseable",
            [tab.label for tab in app.tabs],
        )
        self.assertIn("no identifica por separado IBNR puro", markdown)
        self.assertIn(
            "v0.6.0 Sprint 2 r2 · alcance actuarial explícito",
            [caption.value for caption in app.caption],
        )
        self.assertNotIn("st.bar_chart", APP.read_text(encoding="utf-8"))

        for checkbox in app.checkbox:
            if checkbox.label.startswith("Confirmo que revisé representatividad"):
                checkbox.set_value(True)
        for button in app.button:
            if button.label == "Proyectar costo y pasivo no pagado":
                button.click()
                break
        app.run()

        self.assertEqual(len(app.exception), 0)
        self.assertIn(
            "Descargar resultados Chain Ladder",
            [button.label for button in app.get("download_button")],
        )
        rendered = "\n".join(element.value for element in app.markdown)
        self.assertIn("jf-kpi-grid", rendered)
        self.assertIn("Costo final técnico estimado", rendered)
        self.assertIn("Pasivo no pagado estimado", rendered)
        self.assertNotIn("...", rendered)

        for checkbox in app.checkbox:
            if checkbox.label.startswith("Confirmo que documenté la fuente del prior"):
                checkbox.set_value(True)
        for button in app.button:
            if button.label == "Comparar Chain Ladder y Bornhuetter-Ferguson":
                button.click()
                break
        app.run()

        self.assertEqual(len(app.exception), 0)
        download_labels = [button.label for button in app.get("download_button")]
        self.assertIn("Descargar comparación Chain Ladder + BF", download_labels)
        rendered = "\n".join(element.value for element in app.markdown)
        self.assertIn("jf-method-comparison", rendered)
        self.assertIn("Chain Ladder", rendered)
        self.assertIn("Bornhuetter-Ferguson", rendered)
        self.assertIn("Diferencia de pasivo no pagado · BF − CL", rendered)

        chart_specs = [json.loads(element.proto.spec) for element in app.get("vega_lite_chart")]
        trajectory = next(
            spec
            for spec in chart_specs
            if spec.get("encoding", {}).get("strokeDash", {}).get("field") == "metodo"
        )
        self.assertEqual(trajectory["mark"]["type"], "line")
        self.assertNotIn("stack", trajectory["encoding"]["y"])

        difference = next(
            spec
            for spec in chart_specs
            if spec.get("layer", [{}])[0].get("encoding", {}).get("y", {}).get("field")
            == "diferencia_ibnr_bf_vs_cl"
        )
        self.assertEqual(difference["layer"][0]["mark"]["type"], "bar")
        self.assertTrue(difference["layer"][0]["encoding"]["y"]["scale"]["zero"])
        self.assertEqual(difference["layer"][1]["mark"]["type"], "rule")

        for checkbox in app.checkbox:
            if checkbox.label.startswith(
                "Confirmo que documenté la selección del número de iteraciones"
            ):
                checkbox.set_value(True)
        for button in app.button:
            if button.label == "Calcular Benktander":
                button.click()
                break
        app.run()

        self.assertEqual(len(app.exception), 0)
        download_labels = [button.label for button in app.get("download_button")]
        self.assertIn("Descargar comparación CL + BF + Benktander", download_labels)
        rendered = "\n".join(element.value for element in app.markdown)
        self.assertIn("Benktander", rendered)
        self.assertIn("Diferencia de pasivo no pagado · Benktander − CL", rendered)

        chart_specs = [json.loads(element.proto.spec) for element in app.get("vega_lite_chart")]
        three_method_trajectory = next(
            spec
            for spec in chart_specs
            if spec.get("encoding", {}).get("color", {}).get("scale", {}).get("domain")
            == ["Chain Ladder", "Bornhuetter-Ferguson", "Benktander"]
        )
        self.assertEqual(three_method_trajectory["mark"]["type"], "line")
        self.assertNotIn("stack", three_method_trajectory["encoding"]["y"])

        benktander_difference = next(
            spec
            for spec in chart_specs
            if spec.get("layer", [{}])[0].get("encoding", {}).get("y", {}).get("field")
            == "diferencia_ibnr_bk_vs_cl"
        )
        self.assertEqual(benktander_difference["layer"][0]["mark"]["type"], "bar")
        self.assertTrue(benktander_difference["layer"][0]["encoding"]["y"]["scale"]["zero"])
        self.assertEqual(benktander_difference["layer"][1]["mark"]["type"], "rule")


if __name__ == "__main__":
    unittest.main()

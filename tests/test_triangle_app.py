#!/usr/bin/env python3
"""Smoke test for the local Streamlit learning flow."""

from __future__ import annotations

import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps" / "triangle_workshop.py"


class TriangleAppTest(unittest.TestCase):
    def test_example_can_build_and_offer_download(self) -> None:
        app = AppTest.from_file(str(APP), default_timeout=30).run()
        markdown = "\n".join(element.value for element in app.markdown)
        self.assertIn("IgraSans", markdown)
        self.assertIn("jf-hero", markdown)
        self.assertIn("HEALTH INSURANCE", markdown)

        confirmations = {
            "La obligación y la medida objetivo están definidas",
            "Confirmo la semántica de la fecha de origen",
            "Confirmo la semántica de la fecha de movimiento",
            "El importe es incremental y corresponde a la medida",
            "El archivo está completo hasta la valoración",
            "La historia es representativa del proceso actual",
        }
        for checkbox in app.checkbox:
            if checkbox.label in confirmations:
                checkbox.set_value(True)
        for button in app.button:
            if button.label == "Validar y construir triángulos":
                button.click()
                break
        app.run()

        self.assertEqual(len(app.exception), 0)
        self.assertIn(
            "El total de los datos canónicos reconcilia con el triángulo incremental.",
            [message.value for message in app.success],
        )
        self.assertIn(
            "Descargar paquete de resultados",
            [button.label for button in app.get("download_button")],
        )


if __name__ == "__main__":
    unittest.main()

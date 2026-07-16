#!/usr/bin/env python3
"""Smoke test for the local Demo 6 Chain Ladder interface."""

from __future__ import annotations

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
        self.assertIn("Del triángulo a ultimate e IBNR", markdown)

        for checkbox in app.checkbox:
            if checkbox.label.startswith("Confirmo que revisé la representatividad"):
                checkbox.set_value(True)
        for button in app.button:
            if button.label == "Estimar ultimate e IBNR":
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
        self.assertIn("Ultimate estimado", rendered)
        self.assertIn("IBNR estimado", rendered)
        self.assertNotIn("...", rendered)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Structural and privacy tests for Ask the Handbook Sprint 2.2."""

from __future__ import annotations

import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "overrides" / "main.html"
PARTIAL = ROOT / "overrides" / "partials" / "handbook-qa-panel.html"
ENGINE = ROOT / "docs" / "assets" / "javascripts" / "handbook-qa.js"
STYLES = ROOT / "docs" / "assets" / "stylesheets" / "handbook-qa.css"
NODE_TEST = ROOT / "tests" / "js" / "test_handbook_qa_panel.js"


class HandbookQAPanelTest(unittest.TestCase):
    def test_partial_exists_and_is_included_once(self) -> None:
        self.assertTrue(PARTIAL.is_file())
        main = MAIN.read_text(encoding="utf-8")
        include = '{% include "partials/handbook-qa-panel.html" %}'
        self.assertEqual(main.count(include), 1)

    def test_dialog_accessibility_contract(self) -> None:
        html = PARTIAL.read_text(encoding="utf-8")
        for token in [
            'role="dialog"',
            'aria-modal="true"',
            'aria-labelledby="handbook-qa-global-title"',
            'aria-describedby="handbook-qa-global-description"',
            'aria-haspopup="dialog"',
            'aria-expanded="false"',
            'aria-live="polite"',
            'aria-label="Cerrar Pregúntale al Handbook"',
        ]:
            self.assertIn(token, html)
        self.assertEqual(len(re.findall(r'id="handbook-qa-global-dialog"', html)), 1)

    def test_global_panel_behavior_is_present(self) -> None:
        source = ENGINE.read_text(encoding="utf-8")
        for token in [
            "initializeGlobalPanel",
            "shouldShowGlobalPanel",
            "focusableElements",
            "nextFocusIndex",
            'event.key === "Escape"',
            "previouslyFocused",
            "handbook-qa-panel-open",
            "globalInitialized",
            "document$.subscribe(start)",
        ]:
            self.assertIn(token, source)

    def test_safe_degradation_and_isolated_page_rule(self) -> None:
        source = ENGINE.read_text(encoding="utf-8")
        self.assertIn('trigger.hidden = true', source)
        self.assertIn('overlay.hidden = true', source)
        self.assertIn('/ask-the-handbook/', source)
        self.assertIn('console.warn("Ask the Handbook no pudo inicializar', source)

    def test_styles_cover_responsive_dark_and_reduced_motion(self) -> None:
        css = STYLES.read_text(encoding="utf-8")
        for token in [
            ".handbook-qa-global__trigger",
            ".handbook-qa-global__dialog",
            "body.handbook-qa-panel-open",
            '@media screen and (max-width: 640px)',
            '[data-md-color-scheme="slate"]',
            '@media (prefers-reduced-motion: reduce)',
            "safe-area-inset-bottom",
        ]:
            self.assertIn(token, css)

    def test_no_client_storage_or_ai_endpoints(self) -> None:
        text = "\n".join(
            [
                ENGINE.read_text(encoding="utf-8"),
                PARTIAL.read_text(encoding="utf-8"),
            ]
        ).lower()
        for forbidden in [
            "localstorage",
            "sessionstorage",
            "indexeddb",
            "api.openai.com",
            "api.anthropic.com",
            "generativelanguage.googleapis.com",
        ]:
            self.assertNotIn(forbidden, text)

    def test_node_panel_regression_suite(self) -> None:
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node.js no está disponible")
        completed = subprocess.run(
            [node, str(NODE_TEST)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode:
            self.fail(
                "Falló la regresión del panel JavaScript.\n"
                f"STDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}"
            )
        self.assertIn("OK:", completed.stdout)


if __name__ == "__main__":
    unittest.main()

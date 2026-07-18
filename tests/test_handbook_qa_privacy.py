#!/usr/bin/env python3
"""Privacy and feedback tests for Ask the Handbook Sprint 2.3."""

from __future__ import annotations

import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "docs" / "assets" / "javascripts" / "handbook-qa.js"
PARTIAL = ROOT / "overrides" / "partials" / "handbook-qa-panel.html"
STYLES = ROOT / "docs" / "assets" / "stylesheets" / "handbook-qa.css"
NODE_TEST = ROOT / "tests" / "js" / "test_handbook_qa_privacy.js"


class HandbookQAPrivacyTest(unittest.TestCase):
    def test_closed_analytics_event_contract(self) -> None:
        source = ENGINE.read_text(encoding="utf-8")
        expected = {
            "handbook_qa_open",
            "handbook_qa_suggestion_selected",
            "handbook_qa_search_submitted",
            "handbook_qa_result",
            "handbook_qa_source_opened",
            "handbook_qa_closed",
            "handbook_qa_unresolved_report",
        }
        for event in expected:
            self.assertIn(f'"{event}"', source)
        self.assertIn("ANALYTICS_EVENTS", source)
        self.assertIn("ANALYTICS_FIELDS", source)
        self.assertIn("safeAnalyticsPayload", source)

    def test_forbidden_free_text_fields_are_not_allowlisted(self) -> None:
        source = ENGINE.read_text(encoding="utf-8")
        fields_match = re.search(
            r"const ANALYTICS_FIELDS = new Set\(\[(.*?)\]\);",
            source,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(fields_match)
        fields = fields_match.group(1).lower()
        for forbidden in ["query", "question", "text", "search_term", "email"]:
            self.assertNotIn(f'"{forbidden}"', fields)

    def test_feedback_contract_is_explicit_and_private(self) -> None:
        source = ENGINE.read_text(encoding="utf-8")
        html = PARTIAL.read_text(encoding="utf-8")
        self.assertIn("buildFeedbackUrl", source)
        self.assertIn("data-handbook-qa-feedback-link", source)
        self.assertIn("data-feedback-base-url", html)
        self.assertIn("issues/new", html)
        self.assertIn("nunca el texto de la pregunta", html)
        self.assertIn("no fue incluida automáticamente", source)

    def test_no_browser_storage_or_ai_endpoints(self) -> None:
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
            "document.cookie",
            "api.openai.com",
            "api.anthropic.com",
            "generativelanguage.googleapis.com",
        ]:
            self.assertNotIn(forbidden, text)

    def test_source_and_feedback_links_are_tagged(self) -> None:
        source = ENGINE.read_text(encoding="utf-8")
        self.assertIn("handbookQaSourceLink", source)
        self.assertIn("handbookQaFeedbackLink", source)
        self.assertIn('handbook_qa_source_opened', source)
        self.assertIn('handbook_qa_unresolved_report', source)

    def test_feedback_styles_exist(self) -> None:
        css = STYLES.read_text(encoding="utf-8")
        for selector in [
            ".handbook-qa__feedback",
            ".handbook-qa__feedback-link",
            ".handbook-qa-global__privacy-note",
        ]:
            self.assertIn(selector, css)

    def test_node_privacy_regression_suite(self) -> None:
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
                "Falló la regresión de privacidad JavaScript.\n"
                f"STDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}"
            )
        self.assertIn("OK:", completed.stdout)


if __name__ == "__main__":
    unittest.main()

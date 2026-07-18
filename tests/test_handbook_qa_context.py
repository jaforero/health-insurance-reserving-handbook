#!/usr/bin/env python3
"""Structural tests for Ask the Handbook Sprint 2.1 contextual retrieval."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import unicodedata
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CATALOG_PATH = DOCS / "assets" / "data" / "handbook-qa-catalog.json"
SECTIONS_PATH = DOCS / "assets" / "data" / "handbook-section-index.json"
ENGINE_PATH = DOCS / "assets" / "javascripts" / "handbook-qa.js"
NODE_TEST_PATH = ROOT / "tests" / "js" / "test_handbook_qa_context.js"


def rendered_path_to_markdown(path: str) -> Path:
    normalized = "/" + path.strip("/")
    if normalized == "/":
        return DOCS / "index.md"
    return DOCS / f"{normalized.strip('/')}.md"


def _slugify_heading(heading: str, *, strip_accents: bool) -> str:
    heading = re.sub(r"`([^`]+)`", r"\1", heading)
    heading = re.sub(r"^\d+(?:\.\d+)*\s*", "", heading.strip())
    if strip_accents:
        heading = "".join(
            character
            for character in unicodedata.normalize("NFD", heading)
            if unicodedata.category(character) != "Mn"
        )
    heading = heading.lower()
    heading = re.sub(r"[^\w\s-]", "", heading, flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", heading).strip("-")


def markdown_anchors(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    anchors: set[str] = set()
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        heading = match.group(1)
        anchors.add(_slugify_heading(heading, strip_accents=False))
        anchors.add(_slugify_heading(heading, strip_accents=True))
    return anchors


class HandbookQAContextTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        cls.sections = json.loads(SECTIONS_PATH.read_text(encoding="utf-8"))

    def test_schema_versions_are_contextual(self) -> None:
        self.assertEqual(self.catalog["schema_version"], "1.1.0")
        self.assertEqual(self.sections["schema_version"], "1.1.0")

    def test_every_item_declares_context(self) -> None:
        for item in self.catalog["items"]:
            context = item.get("contexts")
            self.assertIsInstance(context, dict, f"{item['id']}: falta contexts")
            for field in ["paths", "anchors", "parts", "tags", "priority"]:
                self.assertIn(field, context, f"{item['id']}: falta contexts.{field}")
            self.assertTrue(context["paths"], f"{item['id']}: paths vacío")
            self.assertTrue(context["parts"], f"{item['id']}: parts vacío")
            self.assertTrue(context["tags"], f"{item['id']}: tags vacío")
            self.assertGreaterEqual(float(context["priority"]), 0)
            self.assertLessEqual(float(context["priority"]), 1)

    def test_context_paths_exist(self) -> None:
        for item in self.catalog["items"]:
            for rendered in item["contexts"]["paths"]:
                markdown = rendered_path_to_markdown(rendered)
                self.assertTrue(
                    markdown.is_file(),
                    f"{item['id']}: ruta contextual ausente {rendered} -> {markdown}",
                )

    def test_context_anchors_exist_in_at_least_one_context_page(self) -> None:
        for item in self.catalog["items"]:
            pages = [rendered_path_to_markdown(path) for path in item["contexts"]["paths"]]
            available: set[str] = set()
            for page in pages:
                if page.is_file():
                    available.update(markdown_anchors(page))
            for anchor in item["contexts"]["anchors"]:
                self.assertIn(
                    anchor,
                    available,
                    f"{item['id']}: anchor contextual no encontrado: {anchor}",
                )

    def test_section_index_declares_rendered_context(self) -> None:
        for section in self.sections["sections"]:
            self.assertTrue(section.get("part"), f"{section['id']}: falta part")
            self.assertTrue(section.get("rendered_path"), f"{section['id']}: falta rendered_path")
            self.assertTrue(section.get("tags"), f"{section['id']}: falta tags")
            expected = "/" + section["path"].removesuffix(".md").strip("/") + "/"
            self.assertEqual(section["rendered_path"], expected)

    def test_engine_exports_context_contract(self) -> None:
        engine = ENGINE_PATH.read_text(encoding="utf-8")
        for name in [
            "normalizePath",
            "normalizeAnchor",
            "pageContextScore",
            "sectionContextScore",
            "suggestQuestions",
            "answerById",
            "detectActiveHeading",
        ]:
            self.assertRegex(engine, rf"\b{name}\b")

    def test_context_does_not_replace_lexical_evidence(self) -> None:
        engine = ENGINE_PATH.read_text(encoding="utf-8")
        self.assertIn("hasLexicalEvidence", engine)
        self.assertIn("question >= 0.4", engine)

    def test_node_context_regression_suite(self) -> None:
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node.js no está disponible")
        completed = subprocess.run(
            [node, str(NODE_TEST_PATH)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode:
            self.fail(
                "Falló la regresión contextual JavaScript.\n"
                f"STDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}"
            )
        self.assertIn("OK:", completed.stdout)


if __name__ == "__main__":
    unittest.main()

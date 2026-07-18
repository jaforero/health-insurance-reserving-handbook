#!/usr/bin/env python3
"""Structural and regression tests for the zero-cost Ask the Handbook MVP."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import unicodedata
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CATALOG_PATH = DOCS / "assets" / "data" / "handbook-qa-catalog.json"
SECTIONS_PATH = DOCS / "assets" / "data" / "handbook-section-index.json"
ENGINE_PATH = DOCS / "assets" / "javascripts" / "handbook-qa.js"
STYLE_PATH = DOCS / "assets" / "stylesheets" / "handbook-qa.css"
PAGE_PATH = DOCS / "ask-the-handbook.md"
MKDOCS_PATH = ROOT / "mkdocs.yml"
NODE_TEST_PATH = ROOT / "tests" / "js" / "test_handbook_qa_engine.js"

REQUIRED_ITEM_FIELDS = {
    "id",
    "question",
    "variants",
    "concepts",
    "summary",
    "why_it_matters",
    "example",
    "caution",
    "sources",
    "language",
    "version",
    "last_reviewed",
}


def strip_accents(value: str) -> str:
    return "".join(
        character
        for character in unicodedata.normalize("NFD", value)
        if unicodedata.category(character) != "Mn"
    )


def slugify(value: str, *, remove_accents: bool) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"^\d+(?:\.\d+)*\s*", "", value.strip())
    if remove_accents:
        value = strip_accents(value)
    value = value.lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", value).strip("-")


def markdown_anchors(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    anchors: set[str] = set()
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        heading = match.group(1)
        anchors.add(slugify(heading, remove_accents=False))
        anchors.add(slugify(heading, remove_accents=True))
    return anchors


class HandbookQACatalogTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        cls.section_index = json.loads(SECTIONS_PATH.read_text(encoding="utf-8"))

    def test_expected_files_exist(self) -> None:
        for path in [
            CATALOG_PATH,
            SECTIONS_PATH,
            ENGINE_PATH,
            STYLE_PATH,
            PAGE_PATH,
            NODE_TEST_PATH,
        ]:
            self.assertTrue(path.is_file(), f"Falta el archivo {path.relative_to(ROOT)}")

    def test_catalog_contains_reference_questions(self) -> None:
        items = self.catalog["items"]
        self.assertEqual(len(items), 15)
        identifiers = [item["id"] for item in items]
        self.assertEqual(len(identifiers), len(set(identifiers)))

    def test_required_fields_and_editorial_content(self) -> None:
        for item in self.catalog["items"]:
            missing = REQUIRED_ITEM_FIELDS - set(item)
            self.assertFalse(missing, f"{item.get('id')}: faltan {sorted(missing)}")
            for field in [
                "id",
                "question",
                "summary",
                "why_it_matters",
                "example",
                "caution",
                "language",
                "version",
                "last_reviewed",
            ]:
                self.assertTrue(str(item[field]).strip(), f"{item['id']}: {field} vacío")
            self.assertGreaterEqual(len(item["variants"]), 2)
            self.assertGreaterEqual(len(item["concepts"]), 3)
            self.assertGreaterEqual(len(item["sources"]), 1)

    def test_related_question_ids_exist(self) -> None:
        identifiers = {item["id"] for item in self.catalog["items"]}
        for item in self.catalog["items"]:
            for related in item.get("related_questions", []):
                self.assertIn(related, identifiers, f"{item['id']}: relación inválida {related}")
                self.assertNotEqual(related, item["id"])

    def test_source_paths_and_anchors_exist(self) -> None:
        for item in self.catalog["items"]:
            for source in item["sources"]:
                source_path = DOCS / source["path"]
                self.assertTrue(
                    source_path.is_file(),
                    f"{item['id']}: fuente ausente {source['path']}",
                )
                anchor = source.get("anchor", "").strip()
                self.assertTrue(anchor, f"{item['id']}: fuente sin anchor")
                self.assertIn(
                    anchor,
                    markdown_anchors(source_path),
                    f"{item['id']}: anchor ausente {source['path']}#{anchor}",
                )

    def test_section_index_paths_and_anchors_exist(self) -> None:
        section_ids: set[str] = set()
        for section in self.section_index["sections"]:
            self.assertNotIn(section["id"], section_ids)
            section_ids.add(section["id"])
            source_path = DOCS / section["path"]
            self.assertTrue(source_path.is_file(), f"Sección sin archivo: {section['path']}")
            self.assertIn(
                section["anchor"],
                markdown_anchors(source_path),
                f"Anchor ausente: {section['path']}#{section['anchor']}",
            )
            self.assertTrue(section["terms"])
            self.assertTrue(section["summary"].strip())

    def test_zero_cost_contract_has_no_remote_endpoints(self) -> None:
        searchable = "\n".join(
            [
                CATALOG_PATH.read_text(encoding="utf-8"),
                SECTIONS_PATH.read_text(encoding="utf-8"),
                ENGINE_PATH.read_text(encoding="utf-8"),
                PAGE_PATH.read_text(encoding="utf-8"),
            ]
        ).lower()
        for forbidden in [
            "api.openai.com",
            "anthropic.com",
            "generativelanguage.googleapis.com",
            "workers.ai",
            "vectorize",
            "authorization: bearer",
        ]:
            self.assertNotIn(forbidden, searchable)

    def test_size_budgets(self) -> None:
        combined_index_size = CATALOG_PATH.stat().st_size + SECTIONS_PATH.stat().st_size
        self.assertLess(combined_index_size, 500_000)
        self.assertLess(ENGINE_PATH.stat().st_size, 100_000)

    def test_demo_page_contract(self) -> None:
        page = PAGE_PATH.read_text(encoding="utf-8")
        for marker in [
            "data-handbook-qa",
            "data-handbook-qa-form",
            "data-handbook-qa-input",
            "data-handbook-qa-output",
            "aria-live=\"polite\"",
            "no utiliza IA generativa",
        ]:
            self.assertIn(marker, page)

    def test_mkdocs_registers_page_and_assets(self) -> None:
        mkdocs = MKDOCS_PATH.read_text(encoding="utf-8")
        self.assertIn("ask-the-handbook.md", mkdocs)
        self.assertIn("stylesheets/handbook-qa.css", mkdocs)
        self.assertIn("assets/javascripts/handbook-qa.js", mkdocs)

    def test_javascript_engine_regression_suite(self) -> None:
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node.js no está disponible para ejecutar la regresión del motor")
        completed = subprocess.run(
            [node, str(NODE_TEST_PATH)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode:
            self.fail(
                "Falló la regresión JavaScript.\n"
                f"STDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}"
            )
        self.assertIn("OK:", completed.stdout)


if __name__ == "__main__":
    unittest.main()

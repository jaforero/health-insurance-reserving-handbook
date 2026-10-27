#!/usr/bin/env python3
"""Regression tests for automatic Ask the Handbook corpus cataloguing."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
GENERATOR_PATH = ROOT / "scripts" / "generate_handbook_qa_knowledge.py"
CATALOG_PATH = DOCS / "assets" / "data" / "handbook-qa-catalog.json"
EDITORIAL_DEFAULTS_PATH = ROOT / "config" / "handbook_qa_editorial_defaults.json"

spec = importlib.util.spec_from_file_location("handbook_qa_knowledge", GENERATOR_PATH)
assert spec and spec.loader
knowledge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(knowledge)


class HandbookQAKnowledgeGenerationTest(unittest.TestCase):
    def test_every_markdown_document_is_catalogued(self) -> None:
        index = knowledge.build_section_index(DOCS)
        expected = {
            path.relative_to(DOCS).as_posix()
            for path in DOCS.rglob("*.md")
            if "assets" not in path.relative_to(DOCS).parts
        }
        indexed = {document["path"] for document in index["documents"]}
        self.assertEqual(indexed, expected)
        self.assertEqual(index["documents_indexed"], len(expected))
        self.assertGreater(index["sections_indexed"], index["documents_indexed"])

    def test_health_methodology_sources_are_in_generated_index(self) -> None:
        index = knowledge.build_section_index(DOCS)
        pairs = {(section["path"], section["anchor"]) for section in index["sections"]}
        self.assertIn(
            (
                "part-06-health-specific/21-health-insurance-reserving-specificities.md",
                "seleccion-metodologica",
            ),
            pairs,
        )
        self.assertIn(
            (
                "part-06-health-specific/21-health-insurance-reserving-specificities.md",
                "arbol-de-decision-resumido",
            ),
            pairs,
        )
        self.assertIn(
            ("methodology-selection-guide.md", "principios-de-seleccion"),
            pairs,
        )
        self.assertIn(
            ("methodology-selection-guide.md", "arboles-de-decision"),
            pairs,
        )

    def test_default_health_question_is_prepended_idempotently(self) -> None:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        defaults = json.loads(EDITORIAL_DEFAULTS_PATH.read_text(encoding="utf-8"))
        first = knowledge.sync_catalog(catalog, defaults)
        second = knowledge.sync_catalog(first, defaults)
        self.assertEqual(first, second)
        self.assertEqual(first["items"][0]["id"], "health-reserving-method-selection")
        question_texts = [first["items"][0]["question"], *first["items"][0]["variants"]]
        self.assertIn(
            "Para reservas en salud cuál de los métodos es más recomendado?",
            question_texts,
        )

    def test_engine_patch_adds_source_backed_corpus_match(self) -> None:
        engine = (DOCS / "assets" / "javascripts" / "handbook-qa.js").read_text(encoding="utf-8")
        patched = knowledge.patch_engine(engine)
        self.assertIn('status = "corpus_match"', patched)
        self.assertIn('return "Evidencia encontrada en el Handbook";', patched)
        self.assertEqual(knowledge.patch_engine(patched), patched)


if __name__ == "__main__":
    unittest.main()

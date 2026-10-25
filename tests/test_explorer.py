"""Pruebas del Explorador de conocimiento (hooks/explorer.py)."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

from mkdocs.config import load_config
from mkdocs.structure.files import File, Files, InclusionLevel, get_files

ROOT = Path(__file__).resolve().parent.parent


def _load_hook():
    spec = importlib.util.spec_from_file_location("explorer_hook", ROOT / "hooks" / "explorer.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExplorerHookTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hook = _load_hook()
        cls.config = load_config(str(ROOT / "mkdocs.yml"))
        files = get_files(cls.config)
        cls.md_count = sum(1 for f in files if f.is_documentation_page())
        # Corre el evento como lo hace MkDocs en un build real (incluye el hook registrado en mkdocs.yml)
        cls.files = cls.config.plugins.on_files(files, config=cls.config)
        cls.page = cls.files.get_file_from_path(f"{cls.hook.OUTPUT_DIR}/index.html")
        cls.vault_file = cls.files.get_file_from_path(f"{cls.hook.OUTPUT_DIR}/vault.json")
        cls.vault = json.loads(cls.vault_file.content_string) if cls.vault_file else None

    def test_generates_page_and_vault(self):
        self.assertIsNotNone(self.page, "falta explorador/index.html: ¿está 'hooks/explorer.py' en hooks de mkdocs.yml?")
        self.assertIsNotNone(self.vault, "falta explorador/vault.json")

    def test_vault_contains_every_note(self):
        self.assertEqual(len(self.vault["files"]), self.md_count)
        self.assertTrue(all(n["text"] for n in self.vault["files"]), "hay notas vacías en vault.json")

    def test_excludes_unpublished_notes(self):
        published = File.generated(self.config, "live.md", content="# Live")
        hidden = File.generated(self.config, "hidden.md", content="# Hidden")
        draft = File.generated(self.config, "draft.md", content="# Draft")
        hidden.inclusion = InclusionLevel.EXCLUDED
        draft.inclusion = InclusionLevel.DRAFT
        vault = self.hook.build_vault(Files([published, hidden, draft]))
        self.assertEqual([n["path"] for n in vault["files"]], ["live.md"])
        self.assertEqual(set(vault["meta"]["siteUrls"]), {"live.md"})

    def test_regenerates_after_note_add_edit_and_delete(self):
        first = File.generated(self.config, "one.md", content="# First")
        files = Files([first])
        self.assertEqual(len(self.hook.build_vault(files)["files"]), 1)
        second = File.generated(self.config, "two.md", content="# Second\n[First](one.md)")
        files.append(second)
        self.assertEqual(len(self.hook.build_vault(files)["files"]), 2)
        files.remove(first)
        second.content_string = "# Updated"
        self.assertEqual(self.hook.build_vault(files)["files"], [{"path": "two.md", "text": "# Updated"}])

    def test_hubs_exist(self):
        paths = {n["path"] for n in self.vault["files"]}
        for hub in self.hook.HUBS:
            self.assertIn(hub, paths, f"la nota eje {hub} ya no existe: actualiza HUBS en hooks/explorer.py")

    def test_every_note_has_a_site_url(self):
        urls = self.vault["meta"]["siteUrls"]
        self.assertEqual(set(urls), {n["path"] for n in self.vault["files"]})

    def test_page_is_complete(self):
        html = self.page.content_string
        self.assertTrue(html.startswith("<!doctype html>"))
        self.assertIn("<title>", html)
        self.assertNotIn("/*__", html, "quedó un marcador sin reemplazar en la plantilla")
        self.assertIn("parseVault", html)

    def test_images_point_to_published_files(self):
        for path, url in self.vault["assets"].items():
            self.assertEqual(url, "../" + path)
            self.assertIsNotNone(self.files.get_file_from_path(path), f"imagen sin publicar: {path}")


if __name__ == "__main__":
    unittest.main()

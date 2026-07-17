#!/usr/bin/env python3
"""Tests for the reusable Streamlit corporate presentation layer."""

from __future__ import annotations

import tomllib
import unittest

from health_reserving.ui_theme import (
    FAVICON_PATH,
    FONT_PATH,
    LOGO_PATH,
    ROOT,
    SOURCE_FONT_PATH,
    corporate_css,
    footer_html,
    hero_html,
    kpi_grid_html,
    method_comparison_html,
    sidebar_brand_html,
)


class CorporateThemeTest(unittest.TestCase):
    def test_official_assets_are_available_locally(self) -> None:
        self.assertTrue(FONT_PATH.is_file())
        self.assertTrue(SOURCE_FONT_PATH.is_file())
        self.assertTrue(LOGO_PATH.is_file())
        self.assertTrue(FAVICON_PATH.is_file())
        self.assertGreater(FONT_PATH.stat().st_size, 1_000)
        self.assertEqual(FONT_PATH.read_bytes(), SOURCE_FONT_PATH.read_bytes())

    def test_streamlit_registers_igrasans_as_its_native_theme_font(self) -> None:
        with (ROOT / ".streamlit" / "config.toml").open("rb") as stream:
            config = tomllib.load(stream)

        self.assertTrue(config["server"]["enableStaticServing"])
        self.assertEqual(config["theme"]["font"], "IgraSans, sans-serif")
        self.assertEqual(config["theme"]["headingFont"], "IgraSans, sans-serif")
        self.assertIn(
            {
                "family": "IgraSans",
                "url": "app/static/IgraSans.woff2",
                "weight": 400,
                "style": "normal",
            },
            config["theme"]["fontFaces"],
        )

    def test_css_uses_igrasans_without_external_font_service(self) -> None:
        css = corporate_css()
        self.assertIn('font-family: "IgraSans"', css)
        self.assertNotIn("data:font/woff2;base64,", css)
        self.assertIn("--jf-purple: #4e00ff", css)
        self.assertIn("--jf-purple-light: #7c4dff", css)
        self.assertNotIn("fonts.googleapis.com", css)

    def test_hero_escapes_content_and_embeds_brand_icon(self) -> None:
        block = hero_html(
            "Demo <6>",
            "Título <script>",
            "Descripción & control",
            tags=("Local", "<seguro>"),
        )
        self.assertIn("data:image/svg+xml;base64,", block)
        self.assertIn("Demo &lt;6&gt;", block)
        self.assertIn("Título &lt;script&gt;", block)
        self.assertIn("Descripción &amp; control", block)
        self.assertIn("&lt;seguro&gt;", block)
        self.assertNotIn("Título <script>", block)

    def test_sidebar_and_footer_share_the_corporate_identity(self) -> None:
        sidebar = sidebar_brand_html()
        footer = footer_html("Uso <educativo>")
        self.assertIn("HEALTH INSURANCE", sidebar)
        self.assertIn("Javier Forero", sidebar)
        self.assertIn("Actuaría · IA · Datos · Analítica", footer)
        self.assertIn("Uso &lt;educativo&gt;", footer)
        self.assertIn("https://www.linkedin.com/in/jforero/", footer)

    def test_footer_stays_inside_the_main_column(self) -> None:
        css = corporate_css()
        self.assertIn(
            "grid-template-columns: repeat(auto-fit, minmax(min(100%, 17rem), 1fr))",
            css,
        )
        self.assertIn("width: 100%", css)
        self.assertIn("max-width: 100%", css)
        self.assertIn("overflow-wrap: anywhere", css)
        self.assertNotIn("calc(50% - 50vw)", css)
        self.assertNotIn("calc((100vw - 80rem) / 2)", css)

    def test_kpi_grid_keeps_complete_values_and_escapes_content(self) -> None:
        block = kpi_grid_html((("Ultimate <estimado>", "COP 1.234.567.890.123"), ("IBNR", "5,8%")))
        self.assertIn("jf-kpi-grid", block)
        self.assertIn("COP 1.234.567.890.123", block)
        self.assertIn("Ultimate &lt;estimado&gt;", block)
        self.assertNotIn("Ultimate <estimado>", block)

    def test_method_comparison_balances_methods_and_keeps_signed_delta(self) -> None:
        block = method_comparison_html(
            ("Base <común>", "COP 1.274.316.196.198"),
            (
                ("Chain Ladder", (("Ultimate", "COP 1.352.273.822.114"),)),
                ("Bornhuetter-Ferguson", (("Ultimate", "COP 1.352.017.435.986"),)),
            ),
            ("Diferencia BF − CL", "−COP 256.386.128", "−0,33% respecto a CL"),
        )
        self.assertIn("jf-method-comparison", block)
        self.assertEqual(block.count('class="jf-method-card"'), 2)
        self.assertIn("Chain Ladder", block)
        self.assertIn("Bornhuetter-Ferguson", block)
        self.assertIn("−COP 256.386.128", block)
        self.assertIn("Base &lt;común&gt;", block)


if __name__ == "__main__":
    unittest.main()

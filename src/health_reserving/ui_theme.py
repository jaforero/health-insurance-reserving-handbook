"""Reusable corporate presentation layer for the local Streamlit workbench."""

from __future__ import annotations

import base64
import html
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import streamlit as st


ROOT = Path(__file__).resolve().parents[2]
ASSET_ROOT = ROOT / "docs" / "assets"
SOURCE_FONT_PATH = ASSET_ROOT / "fonts" / "IgraSans.woff2"
FONT_PATH = ROOT / "apps" / "static" / "IgraSans.woff2"
LOGO_PATH = ASSET_ROOT / "brand" / "logo-actuaria.svg"
FAVICON_PATH = ASSET_ROOT / "brand" / "favicon.svg"


def _data_uri(path: Path, media_type: str) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"No se encontró el activo corporativo: {path}")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{media_type};base64,{encoded}"


@lru_cache(maxsize=1)
def corporate_css() -> str:
    """Return the corporate CSS used by every Streamlit demo."""

    font_stack = '"IgraSans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    return f"""
:root {{
  --jf-purple: #4e00ff;
  --jf-purple-light: #7c4dff;
  --jf-purple-dark: #3500b8;
  --jf-purple-deep: #260080;
  --jf-purple-soft: #f4f0ff;
  --jf-purple-border: rgba(78, 0, 255, 0.18);
  --jf-text: #1f2430;
  --jf-muted: #5f5872;
  --jf-white: #ffffff;
}}

code,
pre,
[data-testid="stCode"] {{
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
}}

[data-testid="stAppViewContainer"] {{
  color: var(--jf-text);
  background:
    radial-gradient(circle at 96% 3%, rgba(124, 77, 255, 0.08), transparent 25rem),
    var(--jf-white);
}}

.block-container {{
  max-width: 82rem;
  padding-top: 2rem;
  padding-bottom: 2.5rem;
}}

h1,
h2,
h3 {{
  color: var(--jf-purple-deep);
  letter-spacing: -0.02em;
}}

h1 {{
  font-weight: 800;
}}

h2,
h3 {{
  font-weight: 700;
}}

a {{
  color: var(--jf-purple);
}}

a:hover {{
  color: var(--jf-purple-dark);
}}

.jf-hero,
.jf-sidebar-brand,
.jf-footer {{
  font-family: {font_stack};
}}

.jf-hero {{
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 1.5rem;
  align-items: center;
  margin: 0 0 1.25rem;
  padding: clamp(1.4rem, 3vw, 2.4rem);
  background:
    radial-gradient(circle at 92% 8%, rgba(124, 77, 255, 0.16), transparent 34%),
    linear-gradient(135deg, var(--jf-purple-soft) 0%, #ffffff 72%);
  border: 1px solid var(--jf-purple-border);
  border-left: 0.35rem solid var(--jf-purple);
  border-radius: 1rem;
  box-shadow: 0 0.55rem 1.6rem rgba(50, 0, 150, 0.08);
}}

.jf-hero__eyebrow {{
  margin: 0 0 0.55rem;
  color: var(--jf-purple);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.09em;
  text-transform: uppercase;
}}

.jf-hero h1 {{
  margin: 0 0 0.75rem;
  color: var(--jf-purple-deep);
  font-size: clamp(2rem, 4vw, 3.2rem);
  line-height: 1.08;
  font-weight: 800;
}}

.jf-hero__description {{
  max-width: 55rem;
  margin: 0;
  color: #382e55;
  font-size: 1.05rem;
  line-height: 1.65;
}}

.jf-hero__tags {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin-top: 1.15rem;
}}

.jf-hero__tag {{
  padding: 0.38rem 0.68rem;
  color: var(--jf-purple-dark);
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(78, 0, 255, 0.16);
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
}}

.jf-hero__logo {{
  width: clamp(4.2rem, 9vw, 6.4rem);
  height: clamp(4.2rem, 9vw, 6.4rem);
  filter: drop-shadow(0 0.45rem 0.75rem rgba(53, 0, 184, 0.18));
}}

[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, #f4f0ff 0%, #ffffff 42%);
  border-right: 1px solid var(--jf-purple-border);
}}

.jf-sidebar-brand {{
  display: flex;
  gap: 0.72rem;
  align-items: center;
  margin: 0.15rem 0 1.4rem;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid var(--jf-purple-border);
  border-radius: 0.8rem;
}}

.jf-sidebar-brand img {{
  width: 2.65rem;
  height: 2.65rem;
}}

.jf-sidebar-brand strong,
.jf-sidebar-brand span {{
  display: block;
}}

.jf-sidebar-brand strong {{
  color: var(--jf-purple-deep);
  font-size: 0.82rem;
  line-height: 1.2;
}}

.jf-sidebar-brand span {{
  margin-top: 0.18rem;
  color: var(--jf-muted);
  font-size: 0.7rem;
}}

[data-testid="stMetric"] {{
  min-height: 7rem;
  padding: 0.9rem 1rem;
  background: rgba(255, 255, 255, 0.88);
  border: 1px solid rgba(78, 0, 255, 0.14);
  border-radius: 0.8rem;
  box-shadow: 0 0.35rem 1rem rgba(50, 0, 150, 0.055);
}}

[data-testid="stMetricLabel"] {{
  color: var(--jf-muted);
  font-size: 0.78rem;
}}

[data-testid="stMetricValue"] {{
  color: var(--jf-purple);
  font-weight: 800;
}}

.jf-kpi-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 1fr));
  gap: 0.8rem;
  margin: 0.65rem 0 1.35rem;
}}

.jf-kpi-card {{
  box-sizing: border-box;
  min-width: 0;
  min-height: 6.5rem;
  padding: 0.9rem 1rem;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(78, 0, 255, 0.18);
  border-radius: 0.9rem;
  box-shadow: 0 0.35rem 1rem rgba(50, 0, 150, 0.055);
}}

.jf-kpi-card__label {{
  display: block;
  margin-bottom: 0.45rem;
  color: var(--jf-muted);
  font-size: 0.78rem;
  font-weight: 700;
  line-height: 1.25;
}}

.jf-kpi-card__value {{
  display: block;
  color: var(--jf-purple);
  font-size: clamp(1.05rem, 1.35vw, 1.65rem);
  font-weight: 800;
  font-variant-numeric: tabular-nums lining-nums;
  letter-spacing: -0.025em;
  line-height: 1.12;
  white-space: nowrap;
}}

[data-testid="stButton"] button,
[data-testid="stDownloadButton"] button {{
  min-height: 2.7rem;
  border-radius: 999px;
  border-color: rgba(78, 0, 255, 0.35);
  font-weight: 700;
  transition: transform 160ms ease, box-shadow 160ms ease, background-color 160ms ease;
}}

[data-testid="stButton"] button:hover,
[data-testid="stDownloadButton"] button:hover {{
  color: var(--jf-purple-dark);
  border-color: var(--jf-purple);
  transform: translateY(-1px);
  box-shadow: 0 0.4rem 1rem rgba(78, 0, 255, 0.16);
}}

[data-testid="stBaseButton-primary"],
button[kind="primary"] {{
  color: var(--jf-white) !important;
  background: linear-gradient(90deg, var(--jf-purple) 0%, var(--jf-purple-light) 100%) !important;
  border-color: var(--jf-purple) !important;
}}

[data-testid="stBaseButton-primary"]:hover,
button[kind="primary"]:hover {{
  color: var(--jf-white) !important;
  background: linear-gradient(90deg, var(--jf-purple-dark) 0%, var(--jf-purple) 100%) !important;
}}

[data-testid="stFileUploaderDropzone"],
[data-testid="stExpander"],
[data-testid="stDataFrame"] {{
  border-color: var(--jf-purple-border);
  border-radius: 0.8rem;
}}

[data-testid="stAlert"] {{
  border-radius: 0.8rem;
}}

[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
  color: var(--jf-purple);
  font-weight: 800;
}}

[data-baseweb="input"]:focus-within,
[data-baseweb="select"] > div:focus-within,
textarea:focus {{
  border-color: var(--jf-purple) !important;
  box-shadow: 0 0 0 1px var(--jf-purple) !important;
}}

button:focus-visible,
a:focus-visible,
input:focus-visible,
textarea:focus-visible {{
  outline: 3px solid var(--jf-purple-light) !important;
  outline-offset: 3px;
}}

.jf-footer {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 17rem), 1fr));
  gap: 1.2rem;
  align-items: center;
  box-sizing: border-box;
  width: 100%;
  max-width: 100%;
  min-width: 0;
  margin: 2.4rem 0 0;
  padding: 1.45rem clamp(1rem, 3vw, 2rem);
  overflow: hidden;
  color: #ffffff;
  background: linear-gradient(110deg, #260080 0%, #4e00ff 58%, #7c4dff 100%);
  border-top: 1px solid rgba(255, 255, 255, 0.16);
  border-radius: 1rem;
}}

.jf-footer > * {{
  min-width: 0;
}}

.jf-footer__brand {{
  display: flex;
  gap: 0.75rem;
  align-items: center;
}}

.jf-footer__brand img {{
  width: 2.9rem;
  height: 2.9rem;
}}

.jf-footer strong,
.jf-footer span {{
  display: block;
}}

.jf-footer strong {{
  color: #ffffff;
  font-size: 0.95rem;
}}

.jf-footer span {{
  margin-top: 0.12rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.72rem;
}}

.jf-footer__links {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem 0.9rem;
  justify-content: center;
}}

.jf-footer a {{
  color: #ffffff;
  font-size: 0.75rem;
  text-decoration: none;
}}

.jf-footer a:hover {{
  color: #e6dcff;
  text-decoration: underline;
  text-underline-offset: 0.2em;
}}

.jf-footer__note {{
  max-width: 22rem;
  color: rgba(255, 255, 255, 0.78);
  font-size: 0.68rem;
  line-height: 1.45;
  text-align: right;
  overflow-wrap: anywhere;
}}

@media screen and (max-width: 900px) {{
  .jf-footer {{
    grid-template-columns: 1fr 1fr;
  }}

  .jf-footer__note {{
    grid-column: 1 / -1;
    max-width: none;
    text-align: left;
  }}
}}

@media screen and (max-width: 640px) {{
  .block-container {{
    padding-top: 1.2rem;
  }}

  .jf-hero {{
    grid-template-columns: 1fr;
    padding: 1.2rem;
    border-left-width: 0.25rem;
  }}

  .jf-hero__logo {{
    grid-row: 1;
    width: 3.8rem;
    height: 3.8rem;
  }}

  .jf-footer {{
    grid-template-columns: 1fr;
  }}

  .jf-footer__links {{
    justify-content: flex-start;
  }}

  .jf-footer__note {{
    grid-column: auto;
  }}
}}
"""


@lru_cache(maxsize=1)
def _brand_icon_uri() -> str:
    return _data_uri(FAVICON_PATH, "image/svg+xml")


@lru_cache(maxsize=1)
def _brand_logo_uri() -> str:
    return _data_uri(LOGO_PATH, "image/svg+xml")


def configure_page(page_title: str, *, layout: str = "wide") -> None:
    """Configure the Streamlit page with the official local favicon."""

    st.set_page_config(
        page_title=page_title,
        page_icon=str(FAVICON_PATH),
        layout=layout,
    )


def inject_corporate_theme() -> None:
    """Inject the corporate component styles into the current app."""

    st.markdown(f"<style>{corporate_css()}</style>", unsafe_allow_html=True)


def hero_html(
    demo: str,
    title: str,
    description: str,
    *,
    tags: Iterable[str] = (),
) -> str:
    """Build an escaped corporate hero block."""

    safe_demo = html.escape(demo)
    safe_title = html.escape(title)
    safe_description = html.escape(description)
    tag_items = "".join(f'<span class="jf-hero__tag">{html.escape(tag)}</span>' for tag in tags)
    tags_html = f'<div class="jf-hero__tags">{tag_items}</div>' if tag_items else ""
    return f"""
<section class="jf-hero" aria-labelledby="jf-hero-title">
  <div>
    <p class="jf-hero__eyebrow">Workbench actuarial · {safe_demo}</p>
    <h1 id="jf-hero-title">{safe_title}</h1>
    <p class="jf-hero__description">{safe_description}</p>
    {tags_html}
  </div>
  <img class="jf-hero__logo" src="{_brand_icon_uri()}" alt="" aria-hidden="true">
</section>
"""


def render_brand_hero(
    demo: str,
    title: str,
    description: str,
    *,
    tags: Iterable[str] = (),
) -> None:
    """Render the corporate hero for a demo page."""

    st.markdown(
        hero_html(demo, title, description, tags=tags),
        unsafe_allow_html=True,
    )


def sidebar_brand_html() -> str:
    """Build the compact brand shown above sidebar controls."""

    return f"""
<div class="jf-sidebar-brand">
  <img src="{_brand_icon_uri()}" alt="" aria-hidden="true">
  <div>
    <strong>HEALTH INSURANCE<br>RESERVING HANDBOOK</strong>
    <span>Javier Forero · Actuaría e IA</span>
  </div>
</div>
"""


def render_sidebar_brand() -> None:
    """Render the compact sidebar brand."""

    st.markdown(sidebar_brand_html(), unsafe_allow_html=True)


def kpi_grid_html(metrics: Iterable[tuple[str, str]]) -> str:
    """Build compact, escaped KPI cards without numeric truncation."""

    cards = "".join(
        (
            '<section class="jf-kpi-card">'
            f'<span class="jf-kpi-card__label">{html.escape(label)}</span>'
            f'<strong class="jf-kpi-card__value">{html.escape(value)}</strong>'
            "</section>"
        )
        for label, value in metrics
    )
    return f'<div class="jf-kpi-grid" aria-label="Indicadores principales">{cards}</div>'


def render_kpi_grid(metrics: Iterable[tuple[str, str]]) -> None:
    """Render compact corporate KPI cards."""

    st.markdown(kpi_grid_html(metrics), unsafe_allow_html=True)


def footer_html(note: str) -> str:
    """Build the corporate footer with an escaped educational note."""

    safe_note = html.escape(note)
    return f"""
<footer class="jf-footer">
  <div class="jf-footer__brand">
    <img src="{_brand_logo_uri()}" alt="" aria-hidden="true">
    <div>
      <strong>Javier Forero</strong>
      <span>Actuaría · IA · Datos · Analítica</span>
    </div>
  </div>
  <nav class="jf-footer__links" aria-label="Enlaces corporativos">
    <a href="https://javierforero.co/" target="_blank" rel="noopener">Sitio principal</a>
    <a href="https://cv.javierforero.co/" target="_blank" rel="noopener">CV</a>
    <a href="https://github.com/jaforero/health-insurance-reserving-handbook" target="_blank" rel="noopener">GitHub</a>
    <a href="https://www.linkedin.com/in/jforero/" target="_blank" rel="noopener">LinkedIn</a>
  </nav>
  <div class="jf-footer__note">{safe_note}<br>© 2026 Javier Forero · Licencia MIT</div>
</footer>
"""


def render_corporate_footer(note: str) -> None:
    """Render the corporate footer."""

    st.markdown(footer_html(note), unsafe_allow_html=True)

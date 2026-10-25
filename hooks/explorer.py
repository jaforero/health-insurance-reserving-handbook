"""Explorador de conocimiento: hook de MkDocs.

En cada `mkdocs build` o `mkdocs serve` genera dos archivos dentro del sitio:

    explorador/index.html   la página del explorador (grafo, notas, backlinks)
    explorador/vault.json   el texto de todas las notas .md de docs/

No modifica docs/ ni ningún archivo del repositorio. El análisis de enlaces no
ocurre aquí: lo hace explorer/vault-parser.js en el navegador, con las mismas
reglas que se usan cuando un visitante abre su propia carpeta.

Se activa en mkdocs.yml con:

    hooks:
      - hooks/explorer.py

Requiere MkDocs 1.6 o superior (usa File.generated).
"""

from __future__ import annotations

import json
from pathlib import Path

from mkdocs.structure.files import File, Files

# ---------------------------------------------------------------------------
# Configuración. Es lo único que normalmente hay que tocar.
# ---------------------------------------------------------------------------

#: Carpeta del sitio donde se publica el explorador (URL: /explorador/).
OUTPUT_DIR = "explorador"

#: Nombre que aparece en la barra superior del explorador.
VAULT_NAME = "Health Insurance Reserving Handbook"

#: Notas eje: se dibujan como rombos fijos encima del grafo para que no lo
#: colapsen. Rutas relativas a docs/. Si una deja de existir, el test falla.
HUBS = ["index.md", "methodology-selection-guide.md"]

#: Idioma de notas que el filtro muestra al abrir (campo `language` del frontmatter).
DEFAULT_LANG = "es"

#: Nombres visibles de cada grupo (valor normalizado del campo `part`).
#: Español tomado de la navegación de mkdocs.yml; inglés de los nombres de carpeta.
#: Un grupo nuevo que no esté aquí recibe un nombre automático a partir de su carpeta.
GROUP_LABELS = {
    "repository": {"es": "Inicio", "en": "Home"},
    "repository-governance": {"es": "Gobierno del repositorio", "en": "Repository governance"},
    "part-01-foundations": {"es": "Parte 1 · Fundamentos", "en": "Part 1 · Foundations"},
    "part-02-classical-reserving": {"es": "Parte 2 · Reserving clásico", "en": "Part 2 · Classical reserving"},
    "part-03-stochastic-reserving": {"es": "Parte 3 · Reserving estocástico", "en": "Part 3 · Stochastic reserving"},
    "part-04-statistical-models": {"es": "Parte 4 · Modelos estadísticos", "en": "Part 4 · Statistical models"},
    "part-05-machine-learning": {"es": "Parte 5 · Machine Learning", "en": "Part 5 · Machine learning"},
    "part-06-health-specific": {"es": "Parte 6 · Especificidades de salud", "en": "Part 6 · Health specifics"},
    "part-07-colombia": {"es": "Parte 7 · Colombia", "en": "Part 7 · Colombia"},
    "examples": {"es": "Demos prácticos", "en": "Practical demos"},
}

#: Fuente de marca, relativa a docs/. Si no existe, el explorador usa la fuente del sistema.
BRAND_FONT = "assets/fonts/IgraSans.woff2"

# ---------------------------------------------------------------------------

SOURCE_DIR = Path(__file__).resolve().parent.parent / "explorer"
IMAGE_EXT = (".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif")

# Cabecera del documento. La plantilla trae <title>, estilos y el cuerpo; el
# navegador cierra <head> por sí solo al encontrar el primer elemento visible.
_HEAD = (
    "<!doctype html>\n"
    '<html lang="es">\n<head>\n'
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="description" content="Explorador de conocimiento: notas, enlaces y grafo del manual.">\n'
    "<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);"
    "padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}"
    "[hidden]{display:none!important}</style>\n"
)


def build_vault(files: Files) -> dict:
    """Reúne las notas, las imágenes y las URL publicadas a partir de los archivos de MkDocs."""
    pages = sorted((f for f in files if f.is_documentation_page() and f.inclusion.is_included()), key=lambda f: f.src_uri)
    notes = [{"path": f.src_uri, "text": f.content_string} for f in pages]
    # Las imágenes no se copian: el explorador apunta a las que el sitio ya publica.
    assets = {f.src_uri: "../" + f.src_uri for f in files if f.inclusion.is_included() and f.src_uri.lower().endswith(IMAGE_EXT)}
    meta = {
        "source": "sample",
        "name": VAULT_NAME,
        "defaultLang": DEFAULT_LANG,
        "hubs": HUBS,
        "groupLabels": GROUP_LABELS,
        "siteRoot": "../",
        "siteUrls": {f.src_uri: f.url for f in pages},
    }
    return {"meta": meta, "files": notes, "assets": assets}


def build_page(files: Files) -> str:
    """Arma explorador/index.html a partir de la plantilla, el analizador y la app."""
    html = (SOURCE_DIR / "template.html").read_text(encoding="utf-8")
    has_font = files.get_file_from_path(BRAND_FONT) is not None
    font_src = f'url("../{BRAND_FONT}")' if has_font else 'local("IgraSans")'
    parts = {
        "/*__FONT_SRC__*/": font_src,
        "/*__VAULT__*/": "",  # las notas van en vault.json, no dentro de la página
        "/*__PARSER__*/": (SOURCE_DIR / "vault-parser.js").read_text(encoding="utf-8"),
        "/*__APP__*/": (SOURCE_DIR / "app.js").read_text(encoding="utf-8"),
    }
    for marker, value in parts.items():
        if marker not in html:
            raise RuntimeError(f"explorer/template.html no contiene el marcador {marker}")
        html = html.replace(marker, value)
    return _HEAD + html + "\n</html>\n"


def on_files(files: Files, config) -> Files:
    """Evento de MkDocs: añade los dos archivos generados a los del sitio."""
    vault = json.dumps(build_vault(files), ensure_ascii=False, separators=(",", ":"))
    files.append(File.generated(config, f"{OUTPUT_DIR}/index.html", content=build_page(files)))
    files.append(File.generated(config, f"{OUTPUT_DIR}/vault.json", content=vault))
    return files

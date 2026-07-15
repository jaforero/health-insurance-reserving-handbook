#!/usr/bin/env python3
"""Aplica el paquete corporativo al mkdocs.yml actual."""

from pathlib import Path

ruta = Path("mkdocs.yml")
texto = ruta.read_text(encoding="utf-8")

texto = texto.replace(
    "site_author: Health Insurance Reserving Handbook",
    "site_author: Javier Forero",
)

if "  custom_dir: overrides\n" not in texto:
    texto = texto.replace(
        "theme:\n  name: material\n",
        "theme:\n"
        "  name: material\n"
        "  custom_dir: overrides\n"
        "  logo: assets/brand/logo-actuaria.svg\n"
        "  favicon: assets/brand/favicon.svg\n"
        "  font: false\n",
        1,
    )

for css in ("stylesheets/igrasans.css", "stylesheets/corporate.css"):
    linea = f"  - {css}\n"
    if linea not in texto:
        if "\nextra_javascript:\n" not in texto:
            raise SystemExit("No se encontró extra_javascript en mkdocs.yml")
        texto = texto.replace(
            "\nextra_javascript:\n",
            linea + "\nextra_javascript:\n",
            1,
        )

if "analytics:\n    provider: google" not in texto:
    bloque_actual = "extra:\n  generator: false\n"
    bloque_nuevo = (
        "extra:\n"
        "  generator: false\n"
        "  analytics:\n"
        "    provider: google\n"
        "    property: G-MQ3K8EVKV0\n"
    )
    if bloque_actual not in texto:
        raise SystemExit("No se encontró el bloque extra esperado en mkdocs.yml")
    texto = texto.replace(bloque_actual, bloque_nuevo, 1)

ruta.write_text(texto.rstrip() + "\n", encoding="utf-8")
print("OK: mkdocs.yml actualizado")

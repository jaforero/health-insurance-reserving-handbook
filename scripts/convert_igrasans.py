#!/usr/bin/env python3
"""Convierte una fuente IgraSans propiedad del usuario a WOFF2.

No distribuye ni descarga la fuente. Requiere una ruta local autorizada.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from fontTools.ttLib import TTFont


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "fuente",
        type=Path,
        help="Ruta local al archivo IgraSans .otf o .ttf autorizado.",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=Path("docs/assets/fonts/IgraSans.woff2"),
    )
    parser.add_argument(
        "--css",
        type=Path,
        default=Path("docs/stylesheets/igrasans.css"),
    )
    args = parser.parse_args()

    fuente = args.fuente.expanduser().resolve()
    if not fuente.is_file():
        raise SystemExit(f"No existe la fuente: {fuente}")

    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.css.parent.mkdir(parents=True, exist_ok=True)

    font = TTFont(str(fuente))
    variable = "fvar" in font
    font.flavor = "woff2"
    font.save(str(args.salida))

    peso = "100 900" if variable else "400"
    css = (
        '@font-face {\n'
        '  font-family: "IgraSans";\n'
        '  src: url("../assets/fonts/IgraSans.woff2") format("woff2");\n'
        '  font-style: normal;\n'
        f'  font-weight: {peso};\n'
        '  font-display: swap;\n'
        '}\n\n'
        ':root {\n'
        '  --md-text-font: "IgraSans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;\n'
        '  --md-code-font: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;\n'
        '}\n'
    )
    args.css.write_text(css, encoding="utf-8")

    tipo = "variable" if variable else "estática"
    print(f"OK: fuente {tipo} convertida a {args.salida}")
    print(f"OK: CSS generado en {args.css}")
    if not variable:
        print(
            "Nota: solo se registró peso 400. El navegador sintetizará negritas "
            "si no se agregan archivos IgraSans adicionales."
        )


if __name__ == "__main__":
    main()

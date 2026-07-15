#!/usr/bin/env python3
"""Normaliza LaTeX en Markdown para GitHub y MkDocs.

Corrige tres patrones problemáticos:

1. ``\\(...\\)`` en texto normal -> ``$...$`` para matemática inline.
2. Una línea aislada ``=`` dentro de ``$$`` se une a la expresión, evitando
   que GitHub la interprete como un encabezado Setext.
3. ``\\operatorname{X}`` -> ``\\mathrm{X}``, macro admitida por GitHub.

Los bloques de código delimitados por ``` o ~~~ no se modifican.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


OPERATORNAME_RE = re.compile(r"\\operatorname\{([^{}]+)\}")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")


@dataclass
class Counts:
    inline_delimiters: int = 0
    isolated_equals: int = 0
    operatorname: int = 0

    @property
    def total(self) -> int:
        return self.inline_delimiters + self.isolated_equals + self.operatorname

    def add(self, other: "Counts") -> None:
        self.inline_delimiters += other.inline_delimiters
        self.isolated_equals += other.isolated_equals
        self.operatorname += other.operatorname


def replace_operatorname(text: str) -> tuple[str, int]:
    return OPERATORNAME_RE.subn(r"\\mathrm{\1}", text)


def normalize_prose_line(line: str) -> tuple[str, Counts]:
    """Normaliza una línea sin modificar sus fragmentos de código inline."""
    output: list[str] = []
    counts = Counts()
    index = 0

    while index < len(line):
        if line[index] == "`":
            run_end = index
            while run_end < len(line) and line[run_end] == "`":
                run_end += 1
            delimiter = line[index:run_end]
            closing = line.find(delimiter, run_end)
            if closing == -1:
                output.append(line[index:])
                break
            output.append(line[index : closing + len(delimiter)])
            index = closing + len(delimiter)
            continue

        next_tick = line.find("`", index)
        end = len(line) if next_tick == -1 else next_tick
        segment = line[index:end]
        segment, replacements = replace_operatorname(segment)
        counts.operatorname += replacements
        opens = segment.count(r"\(")
        closes = segment.count(r"\)")
        segment = segment.replace(r"\(", "$").replace(r"\)", "$")
        counts.inline_delimiters += opens + closes
        output.append(segment)
        index = end

    return "".join(output), counts


def normalize_math_buffer(lines: list[str]) -> tuple[list[str], Counts]:
    """Normaliza el contenido entre dos delimitadores ``$$``."""
    result: list[str] = []
    counts = Counts()
    index = 0

    while index < len(lines):
        line, replacements = replace_operatorname(lines[index])
        counts.operatorname += replacements

        if line.strip() == "=" and result and index + 1 < len(lines):
            following, replacements = replace_operatorname(lines[index + 1])
            counts.operatorname += replacements
            newline = "\n" if following.endswith(("\n", "\r")) else ""
            result[-1] = (
                result[-1].rstrip("\r\n").rstrip()
                + " = "
                + following.strip()
                + newline
            )
            counts.isolated_equals += 1
            index += 2
            continue

        result.append(line)
        index += 1

    return result, counts


def normalize_markdown(text: str) -> tuple[str, Counts]:
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    math_buffer: list[str] = []
    counts = Counts()
    in_math = False
    fence_marker: str | None = None

    for line in lines:
        fence_match = FENCE_RE.match(line)
        if not in_math and fence_match:
            marker = fence_match.group(1)
            if fence_marker is None:
                fence_marker = marker
            elif marker[0] == fence_marker[0] and len(marker) >= len(fence_marker):
                fence_marker = None
            output.append(line)
            continue

        if fence_marker is not None:
            output.append(line)
            continue

        if line.strip() == "$$":
            if not in_math:
                in_math = True
                output.append(line)
            else:
                normalized, current = normalize_math_buffer(math_buffer)
                output.extend(normalized)
                output.append(line)
                counts.add(current)
                math_buffer = []
                in_math = False
            continue

        if in_math:
            math_buffer.append(line)
            continue

        line, current = normalize_prose_line(line)
        counts.add(current)

        output.append(line)

    if in_math:
        # Conserva literalmente un bloque no cerrado para no ocultar el error.
        output.extend(math_buffer)

    return "".join(output), counts


def scan_remaining(text: str) -> Counts:
    """Cuenta patrones incompatibles sin modificar el contenido."""
    _, counts = normalize_markdown(text)
    return counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Corrige o verifica compatibilidad matemática GitHub/MkDocs."
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=Path("docs"),
        help="Directorio de documentación (predeterminado: docs).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="No escribe archivos; retorna error si encuentra patrones pendientes.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.docs_dir.is_dir():
        print(f"ERROR: no existe el directorio {args.docs_dir}", file=sys.stderr)
        return 2

    grand_total = Counts()
    affected = 0

    for path in sorted(args.docs_dir.rglob("*.md")):
        original = path.read_text(encoding="utf-8")
        normalized, counts = normalize_markdown(original)
        if counts.total == 0:
            continue

        affected += 1
        grand_total.add(counts)
        action = "pendiente" if args.check else "corregido"
        print(
            f"- {path}: {action}; inline={counts.inline_delimiters}, "
            f"igual_aislado={counts.isolated_equals}, "
            f"operatorname={counts.operatorname}"
        )
        if not args.check:
            path.write_text(normalized, encoding="utf-8", newline="\n")

    print("=== Compatibilidad matemática GitHub/MkDocs ===")
    print(f"Archivos afectados: {affected}")
    print(f"Delimitadores inline: {grand_total.inline_delimiters}")
    print(f"Signos igual aislados: {grand_total.isolated_equals}")
    print(f"Macros operatorname: {grand_total.operatorname}")

    if args.check and grand_total.total:
        print("ERROR: quedan patrones incompatibles.")
        return 1

    if args.check:
        print("OK: no se encontraron patrones incompatibles.")
    else:
        print("OK: normalización aplicada. Ejecute de nuevo con --check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

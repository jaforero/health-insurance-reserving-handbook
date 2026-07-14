#!/usr/bin/env python3
"""
Renumber and relink the Health-specific and Colombia chapters after adding
Deep Learning as chapter 20.

Run from repository root:

    python3 scripts/renumber_health_colombia.py --dry-run
    python3 scripts/renumber_health_colombia.py --apply

Then validate:

    python scripts/audit_docs.py
    python -m mkdocs build --strict
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


TODAY = "2026-07-14"


@dataclass(frozen=True)
class ChapterMove:
    old: str
    new: str
    chapter: int

    @property
    def old_path(self) -> Path:
        return Path(self.old)

    @property
    def new_path(self) -> Path:
        return Path(self.new)

    @property
    def old_short(self) -> str:
        return self.old.removeprefix("docs/")

    @property
    def new_short(self) -> str:
        return self.new.removeprefix("docs/")

    @property
    def old_name(self) -> str:
        return Path(self.old).name

    @property
    def new_name(self) -> str:
        return Path(self.new).name


MOVES: list[ChapterMove] = [
    ChapterMove(
        "docs/part-06-health-specific/20-health-insurance-reserving-specificities.md",
        "docs/part-06-health-specific/21-health-insurance-reserving-specificities.md",
        21,
    ),
    ChapterMove(
        "docs/part-06-health-specific/21-health-claim-lifecycle-and-operational-lags.md",
        "docs/part-06-health-specific/22-health-claim-lifecycle-and-operational-lags.md",
        22,
    ),
    ChapterMove(
        "docs/part-06-health-specific/22-health-exposure-utilization-and-severity.md",
        "docs/part-06-health-specific/23-health-exposure-utilization-and-severity.md",
        23,
    ),
    ChapterMove(
        "docs/part-06-health-specific/23-health-medical-trend-seasonality-and-shocks.md",
        "docs/part-06-health-specific/24-health-medical-trend-seasonality-and-shocks.md",
        24,
    ),
    ChapterMove(
        "docs/part-06-health-specific/24-health-risk-adjustment-and-morbidity.md",
        "docs/part-06-health-specific/25-health-risk-adjustment-and-morbidity.md",
        25,
    ),
    ChapterMove(
        "docs/part-06-health-specific/25-health-provider-contracts-and-payment-models.md",
        "docs/part-06-health-specific/26-health-provider-contracts-and-payment-models.md",
        26,
    ),
    ChapterMove(
        "docs/part-06-health-specific/26-health-claims-audit-denials-and-disputes.md",
        "docs/part-06-health-specific/27-health-claims-audit-denials-and-disputes.md",
        27,
    ),
    ChapterMove(
        "docs/part-06-health-specific/27-health-reserving-governance-controls-and-reporting.md",
        "docs/part-06-health-specific/28-health-reserving-governance-controls-and-reporting.md",
        28,
    ),
    ChapterMove(
        "docs/part-07-colombia/21-colombia-health-reserving-methodologies.md",
        "docs/part-07-colombia/29-colombia-health-reserving-methodologies.md",
        29,
    ),
    ChapterMove(
        "docs/part-07-colombia/22-colombia-paid-vs-incurred-triangles.md",
        "docs/part-07-colombia/30-colombia-paid-vs-incurred-triangles.md",
        30,
    ),
    ChapterMove(
        "docs/part-07-colombia/23-colombia-data-and-multistate-models.md",
        "docs/part-07-colombia/31-colombia-data-and-multistate-models.md",
        31,
    ),
    ChapterMove(
        "docs/part-07-colombia/24-colombia-glosas-and-disputes.md",
        "docs/part-07-colombia/32-colombia-glosas-and-disputes.md",
        32,
    ),
    ChapterMove(
        "docs/part-07-colombia/25-colombia-capitation-and-prospective-payments.md",
        "docs/part-07-colombia/33-colombia-capitation-and-prospective-payments.md",
        33,
    ),
]


NEXT_LINKS: dict[str, tuple[str, str]] = {
    "docs/part-05-machine-learning/20-deep-learning-for-loss-reserving.md": (
        "Health Insurance Reserving Specificities",
        "../part-06-health-specific/21-health-insurance-reserving-specificities.md",
    ),
    "docs/part-06-health-specific/21-health-insurance-reserving-specificities.md": (
        "Health Claim Lifecycle and Operational Lags",
        "22-health-claim-lifecycle-and-operational-lags.md",
    ),
    "docs/part-06-health-specific/22-health-claim-lifecycle-and-operational-lags.md": (
        "Health Exposure, Utilization and Severity",
        "23-health-exposure-utilization-and-severity.md",
    ),
    "docs/part-06-health-specific/23-health-exposure-utilization-and-severity.md": (
        "Health Medical Trend, Seasonality and Shocks",
        "24-health-medical-trend-seasonality-and-shocks.md",
    ),
    "docs/part-06-health-specific/24-health-medical-trend-seasonality-and-shocks.md": (
        "Health Risk Adjustment and Morbidity",
        "25-health-risk-adjustment-and-morbidity.md",
    ),
    "docs/part-06-health-specific/25-health-risk-adjustment-and-morbidity.md": (
        "Health Provider Contracts and Payment Models",
        "26-health-provider-contracts-and-payment-models.md",
    ),
    "docs/part-06-health-specific/26-health-provider-contracts-and-payment-models.md": (
        "Health Claims Audit, Denials and Disputes",
        "27-health-claims-audit-denials-and-disputes.md",
    ),
    "docs/part-06-health-specific/27-health-claims-audit-denials-and-disputes.md": (
        "Health Reserving Governance, Controls and Reporting",
        "28-health-reserving-governance-controls-and-reporting.md",
    ),
    "docs/part-06-health-specific/28-health-reserving-governance-controls-and-reporting.md": (
        "Colombia Health Reserving Methodologies",
        "../part-07-colombia/29-colombia-health-reserving-methodologies.md",
    ),
    "docs/part-07-colombia/29-colombia-health-reserving-methodologies.md": (
        "Colombia Paid vs. Incurred Triangles",
        "30-colombia-paid-vs-incurred-triangles.md",
    ),
    "docs/part-07-colombia/30-colombia-paid-vs-incurred-triangles.md": (
        "Colombia Data and Multistate Models",
        "31-colombia-data-and-multistate-models.md",
    ),
    "docs/part-07-colombia/31-colombia-data-and-multistate-models.md": (
        "Colombia Glosas and Disputes",
        "32-colombia-glosas-and-disputes.md",
    ),
    "docs/part-07-colombia/32-colombia-glosas-and-disputes.md": (
        "Colombia Capitation and Prospective Payments",
        "33-colombia-capitation-and-prospective-payments.md",
    ),
}


def ensure_repo_root() -> None:
    if not Path("docs").is_dir() or not Path("mkdocs.yml").is_file():
        raise SystemExit(
            "ERROR: ejecuta este script desde la raíz del repositorio "
            "(donde están docs/ y mkdocs.yml)."
        )


def backup_file(path: Path, backup_root: Path) -> None:
    if not path.exists() or path.is_dir():
        return
    target = backup_root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def text_files_to_update() -> list[Path]:
    allowed_suffixes = {".md", ".yml", ".yaml", ".toml", ".txt"}
    explicit_names = {"Makefile", ".gitignore"}
    skip_dirs = {
        ".git",
        ".venv",
        "venv",
        "env",
        "site",
        "_backups",
        "_audit",
        "__pycache__",
    }
    files: list[Path] = []
    for path in Path(".").rglob("*"):
        if not path.is_file():
            continue
        parts = set(path.parts)
        if parts & skip_dirs:
            continue
        if path.suffix in allowed_suffixes or path.name in explicit_names:
            files.append(path)
    return sorted(files)


def build_replacements() -> list[tuple[str, str]]:
    replacements: list[tuple[str, str]] = []
    for move in MOVES:
        replacements.extend(
            [
                (move.old, move.new),
                (move.old_short, move.new_short),
                (move.old_name, move.new_name),
            ]
        )
    # Longest first prevents partial replacements from interfering with paths.
    return sorted(set(replacements), key=lambda pair: len(pair[0]), reverse=True)


def replace_text_references(text: str) -> str:
    new = text
    for old, replacement in build_replacements():
        new = new.replace(old, replacement)

    # Roadmap range correction after adding Deep Learning as chapter 20.
    new = re.sub(
        r"Parte VI\s+—\s+Health-specific:\s+20[–-]27",
        "Parte VI — Health-specific: 21–28",
        new,
    )
    new = re.sub(
        r"Parte VII\s+—\s+Colombia:\s+28[–-]39",
        "Parte VII — Colombia: 29–40",
        new,
    )
    new = re.sub(
        r"Parte VI\s+·\s+Especificidades de salud:\s+20[–-]27",
        "Parte VI · Especificidades de salud: 21–28",
        new,
    )
    new = re.sub(
        r"Parte VII\s+·\s+Colombia:\s+28[–-]39",
        "Parte VII · Colombia: 29–40",
        new,
    )
    return new


def update_nav_numbers(text: str) -> str:
    chapter_by_short_path = {move.new_short: move.chapter for move in MOVES}
    chapter_by_short_path["part-05-machine-learning/20-deep-learning-for-loss-reserving.md"] = 20

    line_pattern = re.compile(
        r"^(?P<prefix>\s*-\s*)(?P<num>\d+)(?P<middle>\s*·\s*.*?:\s*)"
        r"(?P<path>[A-Za-z0-9_./-]+\.md)(?P<suffix>\s*)$"
    )
    out: list[str] = []
    for line in text.splitlines():
        match = line_pattern.match(line)
        if match:
            path = match.group("path")
            if path in chapter_by_short_path:
                line = (
                    f"{match.group('prefix')}{chapter_by_short_path[path]}"
                    f"{match.group('middle')}{path}{match.group('suffix')}"
                )
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def update_markdown_link_numbers(text: str) -> str:
    """Update labels like [21 · Name](new/path.md) to the chapter of new/path."""
    chapter_by_target: dict[str, int] = {}
    for move in MOVES:
        chapter_by_target[move.new_short] = move.chapter
        chapter_by_target[move.new_name] = move.chapter
        chapter_by_target["../" + move.new_short] = move.chapter

    def repl(match: re.Match[str]) -> str:
        num = match.group("num")
        label = match.group("label")
        target = match.group("target")
        chapter = chapter_by_target.get(target)
        if chapter is None:
            chapter = chapter_by_target.get(target.split("/")[-1])
        if chapter is None:
            return match.group(0)
        return f"[{chapter}{label}]({target})"

    return re.sub(
        r"\[(?P<num>\d+)(?P<label>\s*·[^\]]*)\]\((?P<target>[^)]+\.md)\)",
        repl,
        text,
    )


def update_frontmatter_chapter(path: Path, chapter: int) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text

    front = text[:end]
    rest = text[end:]
    if re.search(r"(?m)^chapter:\s*.*$", front):
        front = re.sub(r"(?m)^chapter:\s*.*$", f"chapter: {chapter}", front)
    else:
        front += f"\nchapter: {chapter}"

    if re.search(r"(?m)^last_updated:\s*.*$", front):
        front = re.sub(r"(?m)^last_updated:\s*.*$", f'last_updated: "{TODAY}"', front)
    else:
        front += f'\nlast_updated: "{TODAY}"'

    return front + rest


def set_next_chapter(path: Path, label: str, link: str) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    block = f"## Próximo capítulo\n\n➡️ **[{label}]({link})**\n"
    pattern = re.compile(
        r"## (?:Próximo capítulo|Próximo archivo|Next Chapter)\n\n"
        r".*?(?=\n## |\Z)",
        flags=re.DOTALL,
    )
    if pattern.search(text):
        return pattern.sub(block, text)
    return text.rstrip() + "\n\n" + block


def plan_moves() -> tuple[list[Path], list[str]]:
    to_move: list[Path] = []
    warnings: list[str] = []
    for move in MOVES:
        old_exists = move.old_path.exists()
        new_exists = move.new_path.exists()
        if old_exists and new_exists:
            raise SystemExit(
                f"ERROR: existen origen y destino para {move.old} -> {move.new}. "
                "Revisa manualmente antes de continuar."
            )
        if old_exists:
            to_move.append(move.old_path)
        elif new_exists:
            warnings.append(f"OK ya renombrado: {move.new}")
        else:
            warnings.append(f"ADVERTENCIA no existe ni origen ni destino: {move.old}")
    return to_move, warnings


def apply_moves(backup_root: Path, dry_run: bool) -> None:
    temp_pairs: list[tuple[Path, Path, ChapterMove]] = []
    for idx, move in enumerate(MOVES):
        if not move.old_path.exists():
            continue
        tmp = move.old_path.with_name(f"__renumber_tmp_{idx:02d}__{move.old_path.name}")
        if tmp.exists():
            raise SystemExit(f"ERROR: temporal ya existe: {tmp}")
        temp_pairs.append((move.old_path, tmp, move))

    if dry_run:
        for old, _, move in temp_pairs:
            print(f"PLAN rename: {old} -> {move.new_path}")
        return

    for old, tmp, _ in temp_pairs:
        backup_file(old, backup_root)
        old.rename(tmp)

    for _, tmp, move in temp_pairs:
        move.new_path.parent.mkdir(parents=True, exist_ok=True)
        tmp.rename(move.new_path)
        print(f"RENOMBRADO: {move.old} -> {move.new}")


def update_all_text_files(backup_root: Path, dry_run: bool) -> int:
    changed = 0
    for path in text_files_to_update():
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except UnicodeDecodeError:
            continue

        new = replace_text_references(text)
        new = update_markdown_link_numbers(new)
        if path.name == "mkdocs.yml":
            new = update_nav_numbers(new)

        if new != text:
            changed += 1
            if dry_run:
                print(f"PLAN update refs: {path}")
            else:
                backup_file(path, backup_root)
                path.write_text(new, encoding="utf-8")
                print(f"REFERENCIAS actualizadas: {path}")
    return changed


def update_final_chapters(backup_root: Path, dry_run: bool) -> int:
    changed = 0

    for move in MOVES:
        path = move.new_path if move.new_path.exists() else move.old_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new = update_frontmatter_chapter(path, move.chapter)
        if new != text:
            changed += 1
            if dry_run:
                print(
                    f"PLAN front matter chapter {move.chapter}: "
                    f"{path} -> {move.new_path}"
                )
            else:
                backup_file(path, backup_root)
                path.write_text(new, encoding="utf-8")
                print(f"FRONTMATTER chapter {move.chapter}: {path}")

    # Deep learning is not renamed, but chapter 20 must be explicit.
    deep_learning = Path("docs/part-05-machine-learning/20-deep-learning-for-loss-reserving.md")
    if deep_learning.exists():
        text = deep_learning.read_text(encoding="utf-8", errors="replace")
        new = update_frontmatter_chapter(deep_learning, 20)
        if new != text:
            changed += 1
            if dry_run:
                print(f"PLAN front matter chapter 20: {deep_learning}")
            else:
                backup_file(deep_learning, backup_root)
                deep_learning.write_text(new, encoding="utf-8")
                print(f"FRONTMATTER chapter 20: {deep_learning}")

    for rel, (label, link) in NEXT_LINKS.items():
        path = Path(rel)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new = set_next_chapter(path, label, link)
        if new != text:
            changed += 1
            if dry_run:
                print(f"PLAN next chapter: {path}")
            else:
                backup_file(path, backup_root)
                path.write_text(new, encoding="utf-8")
                print(f"NEXT actualizado: {path}")

    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Solo muestra el plan")
    mode.add_argument("--apply", action="store_true", help="Aplica cambios con backup")
    args = parser.parse_args()

    ensure_repo_root()
    dry_run = args.dry_run
    backup_root = Path("_backups") / (
        "renumber_health_colombia_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    )

    print("=== Renumber Health + Colombia ===")
    print("Modo:", "DRY RUN" if dry_run else "APPLY")
    print()
    print("Objetivo:")
    print("- Deep Learning queda como capítulo 20.")
    print("- Parte VI · Especificidades de salud queda como capítulos 21–28.")
    print("- Parte VII · Colombia existente queda como capítulos 29–33.")
    print()

    _, warnings = plan_moves()
    for warning in warnings:
        print(warning)

    if not dry_run:
        backup_root.mkdir(parents=True, exist_ok=True)
        print("Backup:", backup_root)
        print()

    apply_moves(backup_root, dry_run=dry_run)
    ref_changes = update_all_text_files(backup_root, dry_run=dry_run)
    chapter_changes = update_final_chapters(backup_root, dry_run=dry_run)

    print()
    print("Resumen:")
    print(f"- Archivos de texto a actualizar: {ref_changes}")
    print(f"- Front matter / próximo capítulo a actualizar: {chapter_changes}")
    if dry_run:
        print("- No se modificó ningún archivo.")
        print()
        print("Si el plan es correcto, ejecuta:")
        print("python3 scripts/renumber_health_colombia.py --apply")
    else:
        print(f"- Backup creado en: {backup_root}")
        print()
        print("Ahora valida:")
        print("python scripts/audit_docs.py")
        print("python -m mkdocs build --strict")

    return 0


if __name__ == "__main__":
    sys.exit(main())

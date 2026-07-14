#!/usr/bin/env python3
"""Preflight checks before publishing the documentation repository.

This script is intentionally conservative and aligned with the current project
state:

- It validates repository publication files.
- It validates MkDocs navigation coverage.
- It checks front matter presence, balanced code fences, and one H1 per document.
- It ignores headings inside fenced code blocks.
- It does not require optional front matter fields such as description/version.

It uses only the Python standard library.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path.cwd()
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"

REQUIRED_FILES = [
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "CITATION.cff",
    "LICENSE",
    "requirements.txt",
    "requirements-dev.txt",
    "pyproject.toml",
    "Makefile",
    ".gitignore",
    ".gitattributes",
    "mkdocs.yml",
    ".github/workflows/docs.yml",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/content_improvement.md",
    "scripts/audit_docs.py",
    "scripts/preflight_release.py",
]

SHOULD_NOT_TRACK = [
    "site",
    "_audit",
    "_backups",
    "github-ready-v0.1.0",
    "github-ready-v0.1.0.zip",
]

IGNORED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "site",
    "_audit",
    "_backups",
}


def docs_rel(path: Path) -> str:
    return path.relative_to(DOCS).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    if not DOCS.exists():
        return files
    for path in DOCS.rglob("*.md"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def extract_nav_refs(text: str) -> set[str]:
    refs: set[str] = set()
    for line in text.splitlines():
        if ".md" not in line:
            continue
        match = re.search(r":\s*['\"]?([^'\"\s]+\.md)['\"]?\s*$", line)
        if match:
            refs.add(match.group(1))
    return refs


def has_front_matter(text: str) -> bool:
    if not text.startswith("---\n"):
        return False
    return text.find("\n---\n", 4) != -1


def body_without_front_matter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---\n", 4)
    if end == -1:
        return text
    return text[end + 5 :]


def remove_fenced_blocks(text: str) -> str:
    output: list[str] = []
    in_fence = False

    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            output.append(line)

    return "\n".join(output)


def count_code_fences(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip().startswith("```"))


def check_required_files(issues: list[str]) -> None:
    for item in REQUIRED_FILES:
        if not (ROOT / item).exists():
            issues.append(f"[required] falta {item}")


def check_temp_artifacts(issues: list[str]) -> None:
    for item in SHOULD_NOT_TRACK:
        if (ROOT / item).exists():
            issues.append(f"[cleanup] remover antes de publicar: {item}")


def check_markdown_structure(files: list[Path], issues: list[str]) -> None:
    for path in files:
        text = read_text(path)
        path_rel = docs_rel(path)

        if not has_front_matter(text):
            issues.append(f"[frontmatter] {path_rel}: falta front matter YAML")

        fence_count = count_code_fences(text)
        if fence_count % 2 != 0:
            issues.append(
                f"[fence] {path_rel}: bloques de código desbalanceados ({fence_count})"
            )

        body = body_without_front_matter(text)
        body_no_code = remove_fenced_blocks(body)
        h1_count = sum(
            1 for line in body_no_code.splitlines() if re.match(r"^#\s+\S", line)
        )
        if h1_count != 1:
            issues.append(f"[h1] {path_rel}: tiene {h1_count} H1; debe tener 1")


def check_nav(files: list[Path], issues: list[str]) -> None:
    if not MKDOCS.exists():
        issues.append("[mkdocs] falta mkdocs.yml")
        return

    nav_refs = extract_nav_refs(read_text(MKDOCS))
    docs_files = {docs_rel(path) for path in files}

    for missing_doc in sorted(nav_refs - docs_files):
        issues.append(f"[mkdocs] nav apunta a archivo faltante: {missing_doc}")

    for unlisted in sorted(docs_files - nav_refs):
        issues.append(f"[mkdocs] documento no está en nav: {unlisted}")


def resolve_doc_link(source: Path, target: str) -> Path | None:
    target = unquote(target.strip())

    if not target or target.startswith("#"):
        return None

    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
        return None

    target_no_anchor = target.split("#", 1)[0]
    if not target_no_anchor.endswith(".md"):
        return None

    return (source.parent / target_no_anchor).resolve()


def check_internal_links(files: list[Path], issues: list[str]) -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    docs_root = DOCS.resolve()

    for path in files:
        text = read_text(path)
        for match in link_pattern.finditer(text):
            raw_target = match.group(1).strip()
            target_path = resolve_doc_link(path, raw_target)
            if target_path is None:
                continue

            try:
                target_path.relative_to(docs_root)
            except ValueError:
                issues.append(
                    f"[link] {docs_rel(path)}: enlace sale de docs: {raw_target}"
                )
                continue

            if not target_path.exists():
                issues.append(
                    f"[link] {docs_rel(path)}: destino no existe: {raw_target}"
                )


def main() -> int:
    issues: list[str] = []
    files = iter_markdown_files()

    if not DOCS.exists():
        issues.append("[docs] falta carpeta docs/")

    check_required_files(issues)
    check_temp_artifacts(issues)
    check_markdown_structure(files, issues)
    check_nav(files, issues)
    check_internal_links(files, issues)

    print("=== Release preflight ===")
    print(f"Markdown files: {len(files)}")
    print(f"Issues: {len(issues)}")

    if issues:
        print()
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("OK: repositorio listo para primera publicación.")
    return 0


if __name__ == "__main__":
    sys.exit(main())


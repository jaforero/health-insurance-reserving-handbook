from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"

REQUIRED_FRONTMATTER = {
    "title",
    "part",
    "chapter",
    "language",
    "status",
    "last_updated",
}


def strip_frontmatter(text: str) -> tuple[str, dict[str, str], list[str]]:
    if not text.startswith("---\n"):
        return text, {}, ["sin front matter"]

    end = text.find("\n---\n", 4)
    if end == -1:
        return text, {}, ["front matter sin cierre"]

    raw = text[4:end]
    body = text[end + 5 :]

    keys = {}
    for line in raw.splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            keys[match.group(1)] = match.group(2).strip()

    issues = []
    missing = sorted(REQUIRED_FRONTMATTER - set(keys))
    if missing:
        issues.append("faltan campos front matter: " + ", ".join(missing))

    return body, keys, issues


def h1_lines_without_code(text: str) -> list[tuple[int, str]]:
    in_fence = False
    h1s = []

    for line_no, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue

        if not in_fence and re.match(r"^#(?!#)\s+", line):
            h1s.append((line_no, line.strip()))

    return h1s


def markdown_refs_from_mkdocs(text: str) -> set[str]:
    return set(re.findall(r"([A-Za-z0-9_./-]+\.md)", text))


def main() -> int:
    if not DOCS.exists():
        print("ERROR: no existe docs/")
        return 1

    md_files = sorted(DOCS.rglob("*.md"))
    docs_rel = {str(p.relative_to(DOCS)) for p in md_files}

    issues = []

    for path in md_files:
        rel = str(path.relative_to(DOCS))
        text = path.read_text(encoding="utf-8", errors="replace")

        if text.count("```") % 2 != 0:
            issues.append((rel, "markdown", "code fences desbalanceados"))

        body, _, fm_issues = strip_frontmatter(text)
        for issue in fm_issues:
            issues.append((rel, "frontmatter", issue))

        h1s = h1_lines_without_code(body)
        if len(h1s) != 1:
            issues.append((rel, "headings", f"H1 encontrados: {len(h1s)}"))

    if MKDOCS.exists():
        mkdocs_text = MKDOCS.read_text(encoding="utf-8", errors="replace")
        nav_refs = markdown_refs_from_mkdocs(mkdocs_text)

        missing_from_nav = sorted(docs_rel - nav_refs)
        nav_points_to_missing = sorted(nav_refs - docs_rel)

        for rel in missing_from_nav:
            issues.append((rel, "mkdocs", "documento no está en nav"))

        for rel in nav_points_to_missing:
            issues.append((rel, "mkdocs", "nav apunta a archivo inexistente"))
    else:
        issues.append(("mkdocs.yml", "mkdocs", "archivo faltante"))

    print("=== Docs audit ===")
    print(f"Markdown files: {len(md_files)}")
    print(f"Issues: {len(issues)}")

    if issues:
        print()
        for rel, category, message in issues:
            print(f"- [{category}] {rel}: {message}")
        return 1

    print("OK: auditoría estructural limpia.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

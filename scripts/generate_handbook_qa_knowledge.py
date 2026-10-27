#!/usr/bin/env python3
"""Generate the zero-cost Ask the Handbook knowledge layer from the published Markdown corpus.

The generator is intentionally deterministic and local. It does not call an LLM, embeddings,
a vector database, or a remote service. It performs four jobs:

1. index every publishable ``docs/**/*.md`` document and its H1-H3 sections;
2. prepend curated editorial defaults to the existing Q&A catalog;
3. upgrade the browser retrieval engine with a source-backed ``corpus_match`` fallback;
4. add the corresponding visual status style.

The generated section index is consumed by ``handbook-qa.js``. Editorial answers remain the
highest-confidence layer; corpus matches only expose source-backed sections and never synthesize
facts that are not present in the handbook.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCS = ROOT / "docs"
DEFAULT_CATALOG = DEFAULT_DOCS / "assets" / "data" / "handbook-qa-catalog.json"
DEFAULT_SECTION_INDEX = DEFAULT_DOCS / "assets" / "data" / "handbook-section-index.json"
DEFAULT_EDITORIAL = ROOT / "config" / "handbook_qa_editorial_defaults.json"
DEFAULT_ENGINE = DEFAULT_DOCS / "assets" / "javascripts" / "handbook-qa.js"
DEFAULT_STYLE = DEFAULT_DOCS / "assets" / "stylesheets" / "handbook-qa.css"

STOP_WORDS = {
    "a", "al", "algo", "como", "con", "cual", "cuando", "de", "del", "desde",
    "donde", "el", "ella", "en", "es", "esta", "este", "esto", "hay", "la", "las",
    "lo", "los", "mas", "me", "mi", "no", "o", "para", "pero", "por", "porque",
    "que", "se", "si", "sin", "son", "su", "sus", "un", "una", "unos", "unas", "y",
}

HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*#*\s*$")
FRONT_MATTER_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")


def strip_accents(value: str) -> str:
    return "".join(
        character
        for character in unicodedata.normalize("NFD", value)
        if unicodedata.category(character) != "Mn"
    )


def normalize_text(value: str) -> str:
    value = strip_accents(value).lower()
    value = re.sub(r"[_/]+", " ", value)
    value = re.sub(r"[^a-z0-9\s-]", " ", value)
    value = value.replace("-", " ")
    return re.sub(r"\s+", " ", value).strip()


def slugify(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"^\d+(?:\.\d+)*\s*", "", value.strip())
    value = strip_accents(value).lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", value).strip("-") or "section"


def _scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        return {}, text

    meta: dict[str, Any] = {}
    current_key: str | None = None
    for line in lines[1:end]:
        match = FRONT_MATTER_KEY_RE.match(line)
        if match:
            key, raw_value = match.groups()
            current_key = key
            if raw_value.strip():
                meta[key] = _scalar(raw_value)
            else:
                meta[key] = []
            continue
        stripped = line.strip()
        if current_key and stripped.startswith("- "):
            if not isinstance(meta.get(current_key), list):
                meta[current_key] = []
            meta[current_key].append(_scalar(stripped[2:]))

    return meta, "\n".join(lines[end + 1 :])


def clean_inline_markdown(value: str) -> str:
    value = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"<[^>]+>", " ", value)
    # Keep underscores: MkDocs preserves them in heading anchors such as
    # `archivo_fuente`. Removing them here would create broken generated links.
    value = re.sub(r"[`*~]", "", value)
    value = re.sub(r"\$+[^$]*\$+", " ", value)
    value = re.sub(r"^\s*(?:[-*+] |\d+[.)]\s+|!!!\s+\w+\s*)", "", value)
    return re.sub(r"\s+", " ", value).strip()


def section_summary(lines: list[str], fallback: str, maximum: int = 160) -> str:
    collected: list[str] = []
    in_fence = False
    for raw in lines:
        stripped = raw.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
            if collected:
                break
            continue
        if stripped.startswith(("|", "$$", "<", "flowchart ", "graph ")):
            continue
        cleaned = clean_inline_markdown(stripped)
        if not cleaned:
            continue
        collected.append(cleaned)
        if len(" ".join(collected)) >= maximum:
            break

    result = " ".join(collected).strip() or clean_inline_markdown(fallback)
    if len(result) > maximum:
        result = result[: maximum - 1].rstrip(" ,;:-") + "…"
    return result


def extract_keywords(*values: str, limit: int = 10) -> list[str]:
    keywords: list[str] = []
    seen: set[str] = set()
    for value in values:
        for token in normalize_text(value).split():
            if len(token) < 3 or token in STOP_WORDS or token.isdigit() or token in seen:
                continue
            seen.add(token)
            keywords.append(token)
            if len(keywords) >= limit:
                return keywords
    return keywords


def rendered_path(relative_path: str) -> str:
    if relative_path == "index.md":
        return "/"
    return "/" + re.sub(r"\.md$", "/", relative_path).lstrip("/")


def markdown_files(docs_root: Path) -> list[Path]:
    return sorted(
        path
        for path in docs_root.rglob("*.md")
        if "assets" not in path.relative_to(docs_root).parts
    )


def build_section_index(docs_root: Path = DEFAULT_DOCS) -> dict[str, Any]:
    documents: list[dict[str, Any]] = []
    sections: list[dict[str, Any]] = []

    for path in markdown_files(docs_root):
        relative = path.relative_to(docs_root).as_posix()
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_front_matter(raw)
        lines = body.splitlines()
        headings: list[tuple[int, str, int]] = []
        in_fence = False
        for index, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(("```", "~~~")):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            match = HEADING_RE.match(line)
            if match:
                headings.append((len(match.group(1)), clean_inline_markdown(match.group(2)), index))

        title = str(meta.get("title") or (headings[0][1] if headings else path.stem))
        description = str(meta.get("description") or meta.get("subtitle") or title)
        part = str(meta.get("part") or (Path(relative).parts[0] if "/" in relative else "repository"))
        language = str(meta.get("language") or "es")
        status = str(meta.get("status") or "published")
        tags_value = meta.get("tags") or []
        tags = tags_value if isinstance(tags_value, list) else [str(tags_value)]
        tags = [str(tag).strip() for tag in tags if str(tag).strip()]

        documents.append(
            {
                "path": relative,
                "title": title,
                "description": description,
                "part": part,
                "language": language,
                "status": status,
                "tags": tags[:8],
                "rendered_path": rendered_path(relative),
            }
        )

        anchor_counts: dict[str, int] = {}
        if not headings:
            headings = [(1, title, -1)]

        for position, (level, heading, line_index) in enumerate(headings):
            base_anchor = slugify(heading)
            count = anchor_counts.get(base_anchor, 0)
            anchor_counts[base_anchor] = count + 1
            anchor = base_anchor if count == 0 else f"{base_anchor}_{count}"
            next_index = headings[position + 1][2] if position + 1 < len(headings) else len(lines)
            content_lines = lines[line_index + 1 : next_index] if line_index >= 0 else lines[:20]
            summary = section_summary(content_lines, description)
            terms = extract_keywords(heading, title, " ".join(tags), summary)
            if not terms:
                terms = [base_anchor]
            identifier = hashlib.sha1(f"{relative}#{anchor}".encode("utf-8")).hexdigest()[:14]
            section_tags = list(dict.fromkeys(tags[:6] + [part, language]))
            sections.append(
                {
                    "id": f"sec-{identifier}",
                    "title": heading,
                    "path": relative,
                    "anchor": anchor,
                    "terms": terms,
                    "summary": summary,
                    "part": part,
                    "rendered_path": rendered_path(relative),
                    "tags": section_tags,
                }
            )

    return {
        "schema_version": "2.0.0",
        "language": "multilingual",
        "generator": "scripts/generate_handbook_qa_knowledge.py",
        "documents_indexed": len(documents),
        "sections_indexed": len(sections),
        "documents": documents,
        "sections": sections,
    }


def sync_catalog(catalog: dict[str, Any], defaults: dict[str, Any]) -> dict[str, Any]:
    default_items = defaults.get("items") or []
    default_ids = {item["id"] for item in default_items}
    remaining = [item for item in catalog.get("items", []) if item.get("id") not in default_ids]
    result = dict(catalog)
    reviewed = [str(item.get("last_reviewed", "")) for item in default_items]
    result["last_updated"] = max([str(catalog.get("last_updated", ""))] + reviewed)
    result["items"] = default_items + remaining
    return result


def patch_engine(engine_text: str) -> str:
    if 'return "Evidencia encontrada en el Handbook";' in engine_text:
        return engine_text

    old_coverage = '["verified", "probable", "insufficient", "out_of_scope"]'
    new_coverage = '["verified", "probable", "corpus_match", "insufficient", "out_of_scope"]'
    if old_coverage not in engine_text:
        raise RuntimeError("No se encontró la lista de estados de cobertura esperada en handbook-qa.js")
    engine_text = engine_text.replace(old_coverage, new_coverage, 1)

    old_search = '''    const status = best.details.hasLexicalEvidence
      ? classifyScore(best.score, best.exact)
      : "insufficient";
    return {
      status,
      item: status === "insufficient" ? null : best.item,
      score: best.score,
      scoreDetails: best.details,
      alternatives: ranked.slice(1, 4),
      relatedSections: findRelatedSections(trimmed, sectionIndex, 3, context),
      message: status === "insufficient"
        ? "No se encontró una respuesta editorial suficientemente precisa. Estas son las secciones más relacionadas dentro del handbook."
        : null
    };'''

    new_search = '''    const relatedSections = findRelatedSections(trimmed, sectionIndex, 3, context);
    let status = best.details.hasLexicalEvidence
      ? classifyScore(best.score, best.exact)
      : "insufficient";
    let item = status === "insufficient" ? null : best.item;

    const topCorpusSection = relatedSections.length ? relatedSections[0].section : null;
    const corpusCoverage = topCorpusSection
      ? fuzzyCoverage(
          tokenize(trimmed),
          tokenize(
            `${topCorpusSection.title || ""} ${(topCorpusSection.terms || []).join(" ")} ${topCorpusSection.summary || ""}`
          )
        )
      : 0;

    // The editorial catalog is the highest-confidence layer. When it does not
    // resolve the wording but the automatically generated corpus index contains
    // strong lexical evidence, expose that evidence instead of claiming that the
    // handbook lacks coverage. A single generic token is not enough: corpus
    // fallback requires both a section score and at least 50% query-token coverage.
    if (
      status === "insufficient"
      && relatedSections.length
      && relatedSections[0].score >= 0.30
      && corpusCoverage >= 0.50
    ) {
      status = "corpus_match";
      item = null;
    }

    return {
      status,
      item,
      score: best.score,
      scoreDetails: best.details,
      alternatives: ranked.slice(1, 4),
      relatedSections,
      message: status === "corpus_match"
        ? "El Handbook contiene evidencia directamente relacionada con esta pregunta. Revise estas secciones fuente; esta recuperación no sintetiza ni completa información fuera del corpus."
        : status === "insufficient"
          ? "No se encontró evidencia documental suficientemente relacionada en el corpus publicado."
          : null
    };'''

    if old_search not in engine_text:
        raise RuntimeError("No se encontró el bloque de búsqueda esperado en handbook-qa.js")
    engine_text = engine_text.replace(old_search, new_search, 1)

    old_label = '''    if (status === "verified") return "Respuesta verificada";
    if (status === "probable") return "Coincidencia probable";
    if (status === "out_of_scope") return "Fuera de alcance";
    return "Cobertura insuficiente";'''
    new_label = '''    if (status === "verified") return "Respuesta verificada";
    if (status === "probable") return "Coincidencia probable";
    if (status === "corpus_match") return "Evidencia encontrada en el Handbook";
    if (status === "out_of_scope") return "Fuera de alcance";
    return "Cobertura insuficiente";'''
    if old_label not in engine_text:
        raise RuntimeError("No se encontró coverageLabel esperado en handbook-qa.js")
    return engine_text.replace(old_label, new_label, 1)


def patch_style(style_text: str) -> str:
    if ".handbook-qa__status--corpus_match" in style_text:
        return style_text
    marker = '''.handbook-qa__status--probable {
  color: #7a4b00;
  background: rgba(214, 137, 16, 0.15);
}
'''
    addition = marker + '''
.handbook-qa__status--corpus_match {
  color: #2446a8;
  background: rgba(78, 0, 255, 0.10);
}
'''
    if marker not in style_text:
        raise RuntimeError("No se encontró el bloque probable esperado en handbook-qa.css")
    return style_text.replace(marker, addition, 1)


def write_json(path: Path, payload: dict[str, Any], *, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if compact:
        serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
    else:
        serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    path.write_text(serialized, encoding="utf-8")


def generate(
    docs_root: Path = DEFAULT_DOCS,
    catalog_path: Path = DEFAULT_CATALOG,
    section_index_path: Path = DEFAULT_SECTION_INDEX,
    editorial_path: Path = DEFAULT_EDITORIAL,
    engine_path: Path = DEFAULT_ENGINE,
    style_path: Path = DEFAULT_STYLE,
) -> dict[str, int]:
    section_index = build_section_index(docs_root)
    write_json(section_index_path, section_index, compact=True)

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    defaults = json.loads(editorial_path.read_text(encoding="utf-8"))
    synced_catalog = sync_catalog(catalog, defaults)
    write_json(catalog_path, synced_catalog)

    engine_text = engine_path.read_text(encoding="utf-8")
    patched_engine = patch_engine(engine_text)
    if patched_engine != engine_text:
        engine_path.write_text(patched_engine, encoding="utf-8")

    style_text = style_path.read_text(encoding="utf-8")
    patched_style = patch_style(style_text)
    if patched_style != style_text:
        style_path.write_text(patched_style, encoding="utf-8")

    return {
        "documents": section_index["documents_indexed"],
        "sections": section_index["sections_indexed"],
        "editorial_answers": len(synced_catalog.get("items", [])),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs", type=Path, default=DEFAULT_DOCS)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--section-index", type=Path, default=DEFAULT_SECTION_INDEX)
    parser.add_argument("--editorial", type=Path, default=DEFAULT_EDITORIAL)
    parser.add_argument("--engine", type=Path, default=DEFAULT_ENGINE)
    parser.add_argument("--style", type=Path, default=DEFAULT_STYLE)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    counts = generate(
        docs_root=args.docs,
        catalog_path=args.catalog,
        section_index_path=args.section_index,
        editorial_path=args.editorial,
        engine_path=args.engine,
        style_path=args.style,
    )
    print(
        "Ask the Handbook actualizado: "
        f"{counts['documents']} documentos, {counts['sections']} secciones, "
        f"{counts['editorial_answers']} respuestas editoriales."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
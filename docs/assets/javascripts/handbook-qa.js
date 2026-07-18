(function (global) {
  "use strict";

  const STOP_WORDS = new Set([
    "a", "al", "algo", "como", "con", "cual", "cuando", "de", "del", "desde",
    "donde", "el", "ella", "en", "es", "esta", "este", "esto", "hay", "la",
    "las", "lo", "los", "me", "mi", "no", "o", "para", "pero", "por", "porque",
    "que", "qué", "se", "si", "sin", "son", "su", "sus", "un", "una", "y"
  ]);

  function normalizeText(value) {
    return String(value || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .replace(/[_/]+/g, " ")
      .replace(/[^a-z0-9\s-]/g, " ")
      .replace(/-/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }

  function tokenize(value) {
    return normalizeText(value)
      .split(" ")
      .filter((token) => token.length > 1 && !STOP_WORDS.has(token));
  }

  function levenshtein(a, b) {
    const left = normalizeText(a);
    const right = normalizeText(b);
    if (left === right) return 0;
    if (!left.length) return right.length;
    if (!right.length) return left.length;

    const previous = Array.from({ length: right.length + 1 }, (_, index) => index);
    for (let i = 1; i <= left.length; i += 1) {
      const current = [i];
      for (let j = 1; j <= right.length; j += 1) {
        const substitution = previous[j - 1] + (left[i - 1] === right[j - 1] ? 0 : 1);
        current[j] = Math.min(
          previous[j] + 1,
          current[j - 1] + 1,
          substitution
        );
      }
      for (let j = 0; j <= right.length; j += 1) previous[j] = current[j];
    }
    return previous[right.length];
  }

  function tokenMatch(left, right) {
    if (left === right) return true;
    const minimum = Math.min(left.length, right.length);
    if (minimum < 5) return false;
    return levenshtein(left, right) <= 1;
  }

  function fuzzyCoverage(queryTokens, candidateTokens) {
    if (!queryTokens.length || !candidateTokens.length) return 0;
    let matched = 0;
    queryTokens.forEach((queryToken) => {
      if (candidateTokens.some((candidateToken) => tokenMatch(queryToken, candidateToken))) {
        matched += 1;
      }
    });
    return matched / queryTokens.length;
  }

  function diceCoefficient(leftTokens, rightTokens) {
    if (!leftTokens.length || !rightTokens.length) return 0;
    const left = Array.from(new Set(leftTokens));
    const right = Array.from(new Set(rightTokens));
    let matched = 0;
    left.forEach((token) => {
      if (right.some((candidate) => tokenMatch(token, candidate))) matched += 1;
    });
    return (2 * matched) / (left.length + right.length);
  }

  function expandWithSynonyms(query, synonymGroups) {
    const normalized = normalizeText(query);
    const expanded = new Set(tokenize(query));
    (synonymGroups || []).forEach((group) => {
      const normalizedGroup = group.map(normalizeText);
      const activated = normalizedGroup.some((phrase) => {
        if (!phrase) return false;
        if (normalized.includes(phrase)) return true;
        return tokenize(phrase).some((token) => expanded.has(token));
      });
      if (activated) {
        normalizedGroup.forEach((phrase) => {
          tokenize(phrase).forEach((token) => expanded.add(token));
        });
      }
    });
    return Array.from(expanded);
  }

  function candidateQuestionTexts(item) {
    return [item.question].concat(item.variants || []);
  }

  function isExactQuestion(query, item) {
    const normalized = normalizeText(query);
    return candidateQuestionTexts(item).some(
      (candidate) => normalizeText(candidate) === normalized
    );
  }

  function contextScore(item, context) {
    if (!context) return 0;
    const currentPath = normalizeText(context.path || "");
    const currentAnchor = normalizeText(context.anchor || "");
    let score = 0;

    (item.sources || []).forEach((source) => {
      const sourcePath = normalizeText(source.path || "");
      const sourceAnchor = normalizeText(source.anchor || "");
      if (currentPath && sourcePath && currentPath.includes(sourcePath.replace(/ md$/, ""))) {
        score = Math.max(score, 0.75);
      }
      if (currentAnchor && sourceAnchor && currentAnchor === sourceAnchor) {
        score = 1;
      }
    });

    const contextTokens = tokenize(`${context.title || ""} ${context.heading || ""}`);
    const conceptTokens = tokenize((item.concepts || []).join(" "));
    score = Math.max(score, fuzzyCoverage(contextTokens, conceptTokens) * 0.75);
    return Math.min(score, 1);
  }

  function scoreItem(query, item, synonymGroups, context) {
    if (isExactQuestion(query, item)) {
      return {
        total: 1,
        term: 1,
        synonym: 1,
        context: contextScore(item, context),
        question: 1
      };
    }

    const queryTokens = tokenize(query);
    const expandedTokens = expandWithSynonyms(query, synonymGroups);
    const conceptTokens = tokenize((item.concepts || []).join(" "));
    const questionScores = candidateQuestionTexts(item).map((question) =>
      diceCoefficient(queryTokens, tokenize(question))
    );

    const term = fuzzyCoverage(queryTokens, conceptTokens);
    const synonym = fuzzyCoverage(expandedTokens, conceptTokens);
    const contextual = contextScore(item, context);
    const question = Math.max(0, ...questionScores);
    const total = (0.35 * term) + (0.25 * synonym) + (0.15 * contextual) + (0.25 * question);

    return {
      total: Math.min(total, 1),
      term,
      synonym,
      context: contextual,
      question
    };
  }

  function isOutOfScope(query, patterns) {
    const normalized = normalizeText(query);
    return (patterns || []).some((pattern) => normalized.includes(normalizeText(pattern)));
  }

  function findRelatedSections(query, sectionIndex, limit) {
    const queryTokens = tokenize(query);
    const sections = (sectionIndex && sectionIndex.sections) || [];
    return sections
      .map((section) => {
        const terms = tokenize(
          `${section.title || ""} ${(section.terms || []).join(" ")} ${section.summary || ""}`
        );
        const score = (
          0.7 * fuzzyCoverage(queryTokens, terms)
          + 0.3 * diceCoefficient(queryTokens, tokenize(section.title || ""))
        );
        return { section, score };
      })
      .filter((entry) => entry.score > 0)
      .sort((left, right) => right.score - left.score)
      .slice(0, limit || 3);
  }

  function classifyScore(score, exact) {
    if (exact || score >= 0.78) return "verified";
    if (score >= 0.52) return "probable";
    return "insufficient";
  }

  function search(query, catalog, sectionIndex, context) {
    const trimmed = String(query || "").trim();
    if (trimmed.length < 3) {
      return {
        status: "insufficient",
        message: "Escriba una pregunta de al menos tres caracteres.",
        relatedSections: []
      };
    }

    if (isOutOfScope(trimmed, catalog.out_of_scope_patterns)) {
      return {
        status: "out_of_scope",
        message: catalog.out_of_scope_response,
        relatedSections: findRelatedSections(trimmed, sectionIndex, 3)
      };
    }

    const ranked = (catalog.items || [])
      .map((entry) => {
        const details = scoreItem(trimmed, entry, catalog.synonym_groups, context);
        return {
          item: entry,
          score: details.total,
          details,
          exact: isExactQuestion(trimmed, entry)
        };
      })
      .sort((left, right) => right.score - left.score);

    const best = ranked[0];
    if (!best) {
      return {
        status: "insufficient",
        message: "No hay respuestas editoriales disponibles.",
        relatedSections: []
      };
    }

    const status = classifyScore(best.score, best.exact);
    return {
      status,
      item: status === "insufficient" ? null : best.item,
      score: best.score,
      scoreDetails: best.details,
      alternatives: ranked.slice(1, 4),
      relatedSections: findRelatedSections(trimmed, sectionIndex, 3),
      message: status === "insufficient"
        ? "No se encontró una respuesta editorial suficientemente precisa. Estas son las secciones más relacionadas dentro del handbook."
        : null
    };
  }

  function sourceHref(source, siteRoot) {
    const root = siteRoot || "../";
    const path = String(source.path || "");
    const anchor = source.anchor ? `#${source.anchor}` : "";
    if (path === "index.md") return `${root}${anchor}`;
    const renderedPath = path.replace(/\.md$/i, "/");
    return `${root}${renderedPath}${anchor}`;
  }

  function createElement(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (typeof text === "string") element.textContent = text;
    return element;
  }

  function appendLabeledSection(container, title, text) {
    const section = createElement("section", "handbook-qa__answer-section");
    section.appendChild(createElement("h3", null, title));
    section.appendChild(createElement("p", null, text));
    container.appendChild(section);
  }

  function renderSources(container, sources, siteRoot) {
    const section = createElement("section", "handbook-qa__answer-section");
    section.appendChild(createElement("h3", null, "Fuentes dentro del handbook"));
    const list = createElement("ul", "handbook-qa__sources");
    (sources || []).forEach((source) => {
      const row = createElement("li");
      const link = createElement("a", null, source.label || source.path);
      link.href = sourceHref(source, siteRoot);
      row.appendChild(link);
      list.appendChild(row);
    });
    section.appendChild(list);
    container.appendChild(section);
  }

  function renderRelatedQuestions(container, item, catalog, onQuestion) {
    const ids = item.related_questions || [];
    if (!ids.length) return;
    const lookup = new Map((catalog.items || []).map((entry) => [entry.id, entry]));
    const section = createElement("section", "handbook-qa__answer-section");
    section.appendChild(createElement("h3", null, "Preguntas relacionadas"));
    const group = createElement("div", "handbook-qa__related");
    ids.forEach((id) => {
      const related = lookup.get(id);
      if (!related) return;
      const button = createElement("button", "handbook-qa__question-chip", related.question);
      button.type = "button";
      button.addEventListener("click", () => onQuestion(related.question));
      group.appendChild(button);
    });
    section.appendChild(group);
    container.appendChild(section);
  }

  function renderSections(container, relatedSections, siteRoot) {
    if (!relatedSections || !relatedSections.length) return;
    const section = createElement("section", "handbook-qa__answer-section");
    section.appendChild(createElement("h3", null, "Secciones relacionadas"));
    const list = createElement("ul", "handbook-qa__section-results");
    relatedSections.forEach((entry) => {
      const row = createElement("li");
      const link = createElement("a", null, entry.section.title);
      link.href = sourceHref(entry.section, siteRoot);
      row.appendChild(link);
      if (entry.section.summary) {
        row.appendChild(createElement("p", null, entry.section.summary));
      }
      list.appendChild(row);
    });
    section.appendChild(list);
    container.appendChild(section);
  }

  function coverageLabel(status) {
    if (status === "verified") return "Respuesta verificada";
    if (status === "probable") return "Coincidencia probable";
    if (status === "out_of_scope") return "Fuera de alcance";
    return "Cobertura insuficiente";
  }

  function renderResult(result, output, catalog, siteRoot, onQuestion) {
    output.replaceChildren();
    const status = createElement(
      "div",
      `handbook-qa__status handbook-qa__status--${result.status}`,
      coverageLabel(result.status)
    );
    status.setAttribute("role", "status");
    output.appendChild(status);

    if (result.item) {
      output.appendChild(createElement("h2", "handbook-qa__answer-title", result.item.question));
      appendLabeledSection(output, "Respuesta directa", result.item.summary);
      appendLabeledSection(output, "Por qué importa actuarialmente", result.item.why_it_matters);
      appendLabeledSection(output, "Ejemplo aplicado", result.item.example);
      appendLabeledSection(output, "Qué puede salir mal", result.item.caution);
      renderSources(output, result.item.sources, siteRoot);
      renderRelatedQuestions(output, result.item, catalog, onQuestion);
      if (result.status === "probable") {
        const note = createElement(
          "p",
          "handbook-qa__notice",
          "La formulación no coincide exactamente con una pregunta editorial. Revise la respuesta y sus fuentes antes de aplicarla."
        );
        output.insertBefore(note, output.children[1] || null);
      }
    } else {
      output.appendChild(createElement("p", "handbook-qa__notice", result.message));
      renderSections(output, result.relatedSections, siteRoot);
    }

    output.hidden = false;
    output.focus({ preventScroll: true });
  }

  async function loadJson(url) {
    const response = await fetch(url, { credentials: "same-origin" });
    if (!response.ok) throw new Error(`No se pudo cargar ${url}: ${response.status}`);
    return response.json();
  }

  function resolveContext(container) {
    const heading = document.querySelector(".md-content h1, .md-content h2, .md-content h3");
    return {
      path: container.dataset.contextPath || window.location.pathname,
      anchor: window.location.hash.replace(/^#/, ""),
      title: document.title,
      heading: heading ? heading.textContent : ""
    };
  }

  function populateSuggestions(container, catalog, askQuestion) {
    const target = container.querySelector("[data-handbook-qa-suggestions]");
    if (!target) return;
    target.replaceChildren();
    (catalog.items || []).slice(0, 6).forEach((item) => {
      const button = createElement("button", "handbook-qa__question-chip", item.question);
      button.type = "button";
      button.addEventListener("click", () => askQuestion(item.question));
      target.appendChild(button);
    });
  }

  async function initialize(container) {
    const form = container.querySelector("[data-handbook-qa-form]");
    const input = container.querySelector("[data-handbook-qa-input]");
    const output = container.querySelector("[data-handbook-qa-output]");
    const loading = container.querySelector("[data-handbook-qa-loading]");
    const siteRoot = container.dataset.siteRoot || "../";

    if (!form || !input || !output) return;
    try {
      loading.hidden = false;
      const catalogUrl = new URL(container.dataset.catalogUrl, document.baseURI);
      const sectionsUrl = new URL(container.dataset.sectionsUrl, document.baseURI);
      const [catalog, sectionIndex] = await Promise.all([
        loadJson(catalogUrl),
        loadJson(sectionsUrl)
      ]);
      loading.hidden = true;

      const askQuestion = (question) => {
        input.value = question;
        const result = search(question, catalog, sectionIndex, resolveContext(container));
        renderResult(result, output, catalog, siteRoot, askQuestion);
      };

      populateSuggestions(container, catalog, askQuestion);
      form.addEventListener("submit", (event) => {
        event.preventDefault();
        askQuestion(input.value);
      });
    } catch (error) {
      loading.hidden = true;
      output.hidden = false;
      output.replaceChildren(
        createElement(
          "p",
          "handbook-qa__error",
          "No fue posible cargar el catálogo local. Revise la consola o intente recargar la página."
        )
      );
      console.error(error);
    }
  }

  const api = {
    normalizeText,
    tokenize,
    levenshtein,
    expandWithSynonyms,
    scoreItem,
    classifyScore,
    isOutOfScope,
    findRelatedSections,
    search,
    sourceHref
  };

  global.HandbookQAEngine = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;

  if (typeof document !== "undefined") {
    const start = () => {
      document.querySelectorAll("[data-handbook-qa]").forEach((container) => {
        if (container.dataset.initialized === "true") return;
        container.dataset.initialized = "true";
        initialize(container);
      });
    };
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", start, { once: true });
    } else {
      start();
    }
    if (typeof document$ !== "undefined" && typeof document$.subscribe === "function") {
      document$.subscribe(start);
    }
  }
})(typeof globalThis !== "undefined" ? globalThis : this);

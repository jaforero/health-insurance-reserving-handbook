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

  function normalizeAnchor(value) {
    return normalizeText(String(value || "").replace(/^#/, ""))
      .replace(/\s+/g, "-");
  }

  function normalizePath(value) {
    const raw = String(value || "").trim();
    let pathname = raw;
    try {
      pathname = new URL(raw || "/", "https://handbook.local/").pathname;
    } catch (error) {
      pathname = raw.split(/[?#]/, 1)[0] || "/";
    }

    try {
      pathname = decodeURIComponent(pathname);
    } catch (error) {
      // Keep the original path when it contains malformed escape sequences.
    }

    pathname = pathname
      .replace(/\\/g, "/")
      .replace(/\/{2,}/g, "/")
      .replace(/\/index\.html?$/i, "/")
      .replace(/\.md$/i, "/");

    if (!pathname.startsWith("/")) pathname = `/${pathname}`;
    if (pathname !== "/" && !pathname.endsWith("/")) pathname += "/";
    return pathname;
  }

  function renderedPath(sourcePath) {
    const path = String(sourcePath || "").replace(/^\/+/, "");
    if (!path || /^index\.md$/i.test(path)) return "/";
    return normalizePath(path.replace(/\.md$/i, "/"));
  }

  function pathPart(path) {
    return normalizePath(path).split("/").filter(Boolean)[0] || "";
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

  function itemContextPaths(item) {
    const configured = ((item.contexts || {}).paths || []).map(normalizePath);
    const sourcePaths = (item.sources || []).map((source) => renderedPath(source.path));
    return Array.from(new Set(configured.concat(sourcePaths)));
  }

  function itemContextAnchors(item) {
    const configured = ((item.contexts || {}).anchors || []).map(normalizeAnchor);
    const sourceAnchors = (item.sources || []).map((source) => normalizeAnchor(source.anchor));
    return Array.from(new Set(configured.concat(sourceAnchors).filter(Boolean)));
  }

  function pageContextScore(item, context) {
    if (!context) return 0;
    const currentPath = normalizePath(context.path || "/");
    const currentPart = pathPart(currentPath);
    const paths = itemContextPaths(item);
    if (paths.includes(currentPath)) return 1;

    const configuredParts = new Set(((item.contexts || {}).parts || []).map(String));
    paths.forEach((path) => configuredParts.add(pathPart(path)));
    if (currentPart && configuredParts.has(currentPart)) return 0.55;

    const contextTokens = tokenize(`${context.title || ""} ${context.heading || ""}`);
    const tagTokens = tokenize(((item.contexts || {}).tags || []).join(" "));
    if (contextTokens.length && tagTokens.length) {
      return Math.min(0.35, fuzzyCoverage(contextTokens, tagTokens) * 0.35);
    }
    return 0;
  }

  function sectionContextScore(item, context) {
    if (!context) return 0;
    const anchor = normalizeAnchor(context.anchor || "");
    const heading = normalizeAnchor(context.heading || "");
    const anchors = itemContextAnchors(item);
    if (anchor && anchors.includes(anchor)) return 1;
    if (heading && anchors.includes(heading)) return 0.9;

    const contextTokens = tokenize(`${context.heading || ""} ${context.title || ""}`);
    const tagTokens = tokenize(((item.contexts || {}).tags || []).join(" "));
    if (contextTokens.length && tagTokens.length) {
      const coverage = fuzzyCoverage(contextTokens, tagTokens);
      if (coverage > 0) return Math.min(0.6, coverage * 0.6);
    }
    return pageContextScore(item, context) > 0 ? 0.3 : 0;
  }

  function contextScore(item, context) {
    return Math.min(
      1,
      (0.67 * pageContextScore(item, context))
      + (0.33 * sectionContextScore(item, context))
    );
  }

  function scoreItem(query, item, synonymGroups, context) {
    const page = pageContextScore(item, context);
    const section = sectionContextScore(item, context);
    if (isExactQuestion(query, item)) {
      return {
        total: 1,
        term: 1,
        synonym: 1,
        question: 1,
        page,
        section,
        context: contextScore(item, context),
        hasLexicalEvidence: true
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
    const question = Math.max(0, ...questionScores);
    const hasLexicalEvidence = term > 0 || synonym > 0 || question >= 0.4;
    const total = (
      (0.30 * term)
      + (0.20 * synonym)
      + (0.20 * question)
      + (0.20 * page)
      + (0.10 * section)
    );

    return {
      total: Math.min(total, 1),
      term,
      synonym,
      question,
      page,
      section,
      context: contextScore(item, context),
      hasLexicalEvidence
    };
  }

  function isOutOfScope(query, patterns) {
    const normalized = normalizeText(query);
    return (patterns || []).some((pattern) => normalized.includes(normalizeText(pattern)));
  }

  function findRelatedSections(query, sectionIndex, limit, context) {
    const queryTokens = tokenize(query);
    const currentPath = normalizePath((context || {}).path || "/");
    const currentAnchor = normalizeAnchor((context || {}).anchor || "");
    const sections = (sectionIndex && sectionIndex.sections) || [];
    return sections
      .map((section) => {
        const terms = tokenize(
          `${section.title || ""} ${(section.terms || []).join(" ")} ${section.summary || ""}`
        );
        const lexical = (
          (0.7 * fuzzyCoverage(queryTokens, terms))
          + (0.3 * diceCoefficient(queryTokens, tokenize(section.title || "")))
        );
        const path = normalizePath(section.rendered_path || renderedPath(section.path));
        const page = currentPath === path ? 1 : (pathPart(currentPath) === pathPart(path) ? 0.45 : 0);
        const anchor = currentAnchor && currentAnchor === normalizeAnchor(section.anchor) ? 1 : 0;
        const score = (0.75 * lexical) + (0.20 * page) + (0.05 * anchor);
        return { section, score };
      })
      .filter((entry) => entry.score > 0)
      .sort((left, right) => right.score - left.score)
      .slice(0, limit || 3);
  }

  function classifyScore(score, exact) {
    if (exact || score >= 0.78) return "verified";
    if (score >= 0.48) return "probable";
    return "insufficient";
  }

  function getItemById(catalog, id) {
    return (catalog.items || []).find((item) => item.id === id) || null;
  }

  function answerById(catalog, id) {
    const item = getItemById(catalog, id);
    if (!item) {
      return {
        status: "insufficient",
        item: null,
        message: "No se encontró la respuesta editorial seleccionada.",
        relatedSections: []
      };
    }
    return {
      status: "verified",
      item,
      score: 1,
      scoreDetails: {
        total: 1,
        term: 1,
        synonym: 1,
        question: 1,
        page: 0,
        section: 0,
        context: 0,
        hasLexicalEvidence: true
      },
      alternatives: [],
      relatedSections: [],
      message: null
    };
  }

  function suggestionScore(item, context) {
    const page = pageContextScore(item, context);
    const section = sectionContextScore(item, context);
    const priority = Math.max(0, Math.min(Number((item.contexts || {}).priority || 0), 1));
    return {
      total: (0.65 * page) + (0.25 * section) + (0.10 * priority),
      page,
      section,
      priority
    };
  }

  function primarySuggestionTag(item) {
    const tags = ((item.contexts || {}).tags || []).filter(Boolean);
    return tags[0] || (item.concepts || [item.id])[0] || item.id;
  }

  function suggestQuestions(catalog, context, limit) {
    const maximum = Math.max(1, Math.min(Number(limit || 5), 5));
    const ranked = (catalog.items || [])
      .filter((item) => !(item.contexts || {}).exclude_from_suggestions)
      .map((item) => ({ item, details: suggestionScore(item, context) }))
      .filter((entry) => entry.details.page > 0 || entry.details.section > 0)
      .sort((left, right) => {
        if (right.details.total !== left.details.total) {
          return right.details.total - left.details.total;
        }
        return left.item.question.localeCompare(right.item.question, "es");
      });

    const selected = [];
    const usedTags = new Set();
    ranked.forEach((entry) => {
      if (selected.length >= maximum) return;
      const tag = primarySuggestionTag(entry.item);
      if (usedTags.has(tag) && ranked.length > maximum) return;
      selected.push(entry);
      usedTags.add(tag);
    });

    if (selected.length < maximum) {
      ranked.forEach((entry) => {
        if (selected.length >= maximum) return;
        if (!selected.some((candidate) => candidate.item.id === entry.item.id)) {
          selected.push(entry);
        }
      });
    }

    if (!selected.length) {
      const isolated = normalizePath((context || {}).path || "/") === "/ask-the-handbook/";
      (catalog.items || [])
        .filter((item) => isolated || (item.contexts || {}).general)
        .sort((left, right) => (
          Number((right.contexts || {}).priority || 0)
          - Number((left.contexts || {}).priority || 0)
        ))
        .slice(0, maximum)
        .forEach((item) => selected.push({ item, details: suggestionScore(item, context) }));
    }

    return selected;
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
        relatedSections: findRelatedSections(trimmed, sectionIndex, 3, context)
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

    const status = best.details.hasLexicalEvidence
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
    };
  }

  function sourceHref(source, siteRoot) {
    const root = siteRoot || "../";
    const path = String(source.path || "");
    const anchor = source.anchor ? `#${source.anchor}` : "";
    if (path === "index.md") return `${root}${anchor}`;
    const rendered = path.replace(/\.md$/i, "/");
    return `${root}${rendered}${anchor}`;
  }

  function detectActiveHeading(headings, threshold) {
    const entries = (headings || [])
      .map((entry) => ({
        id: String(entry.id || ""),
        text: String(entry.text || ""),
        top: Number(entry.top)
      }))
      .filter((entry) => Number.isFinite(entry.top))
      .sort((left, right) => left.top - right.top);
    if (!entries.length) return null;

    const line = Number.isFinite(Number(threshold)) ? Number(threshold) : 160;
    const beforeLine = entries.filter((entry) => entry.top <= line);
    return beforeLine.length ? beforeLine[beforeLine.length - 1] : entries[0];
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

  const JSON_CACHE = new Map();

  async function loadJson(url) {
    const key = String(url);
    if (!JSON_CACHE.has(key)) {
      const pending = fetch(url, { credentials: "same-origin" })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`No se pudo cargar ${url}: ${response.status}`);
          }
          return response.json();
        })
        .catch((error) => {
          JSON_CACHE.delete(key);
          throw error;
        });
      JSON_CACHE.set(key, pending);
    }
    return JSON_CACHE.get(key);
  }

  function resolveContext(container) {
    const headings = Array.from(
      document.querySelectorAll(".md-content h1[id], .md-content h2[id], .md-content h3[id]")
    ).map((heading) => ({
      id: heading.id,
      text: heading.textContent || "",
      top: heading.getBoundingClientRect().top
    }));
    const active = detectActiveHeading(headings, 160);
    const hashAnchor = normalizeAnchor(window.location.hash.replace(/^#/, ""));
    return {
      path: normalizePath(container.dataset.contextPath || window.location.pathname),
      anchor: hashAnchor || (active ? normalizeAnchor(active.id) : ""),
      title: document.title,
      heading: active ? active.text : ""
    };
  }

  function populateSuggestions(container, catalog, askQuestion, context) {
    const target = container.querySelector("[data-handbook-qa-suggestions]");
    if (!target) return;
    target.replaceChildren();
    const suggestions = suggestQuestions(catalog, context, 5);
    const items = suggestions.length
      ? suggestions.map((entry) => entry.item)
      : (catalog.items || []).slice(0, 5);
    items.forEach((item) => {
      const button = createElement("button", "handbook-qa__question-chip", item.question);
      button.type = "button";
      button.dataset.questionId = item.id;
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
      const context = resolveContext(container);

      const askQuestion = (question) => {
        input.value = question;
        const result = search(question, catalog, sectionIndex, resolveContext(container));
        renderResult(result, output, catalog, siteRoot, askQuestion);
      };

      populateSuggestions(container, catalog, askQuestion, context);
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


  function shouldShowGlobalPanel(path) {
    return normalizePath(path || "/") !== "/ask-the-handbook/";
  }

  function focusableElements(container) {
    if (!container || typeof container.querySelectorAll !== "function") return [];
    const selector = [
      "a[href]",
      "button:not([disabled])",
      "input:not([disabled])",
      "select:not([disabled])",
      "textarea:not([disabled])",
      "[tabindex]:not([tabindex='-1'])"
    ].join(",");
    return Array.from(container.querySelectorAll(selector)).filter((element) => {
      if (element.hidden) return false;
      if (element.getAttribute && element.getAttribute("aria-hidden") === "true") return false;
      return true;
    });
  }

  function nextFocusIndex(currentIndex, total, shiftKey) {
    if (!Number.isInteger(total) || total <= 0) return -1;
    if (shiftKey && currentIndex <= 0) return total - 1;
    if (!shiftKey && currentIndex >= total - 1) return 0;
    return shiftKey ? currentIndex - 1 : currentIndex + 1;
  }

  function setBackgroundScrollLocked(locked) {
    if (!document || !document.body) return;
    document.body.classList.toggle("handbook-qa-panel-open", Boolean(locked));
  }

  function pageHeading() {
    const heading = document.querySelector(".md-content h1");
    return heading ? String(heading.textContent || "").trim() : document.title;
  }

  function updateGlobalContext(container, context) {
    const pageTarget = container.querySelector("[data-handbook-qa-context-page]");
    const sectionTarget = container.querySelector("[data-handbook-qa-context-section]");
    if (pageTarget) pageTarget.textContent = pageHeading() || "Página actual";
    if (sectionTarget) {
      const section = String(context.heading || "").trim();
      sectionTarget.textContent = section || "Contexto general de la página";
      sectionTarget.closest("[data-handbook-qa-context-section-row]")?.toggleAttribute(
        "data-context-general",
        !section
      );
    }
  }

  function renderGlobalSuggestions(target, catalog, context, onSelect) {
    if (!target) return [];
    target.replaceChildren();
    const suggestions = suggestQuestions(catalog, context, 5);
    suggestions.forEach((entry) => {
      const button = createElement("button", "handbook-qa__question-chip", entry.item.question);
      button.type = "button";
      button.dataset.questionId = entry.item.id;
      button.addEventListener("click", () => onSelect(entry.item.id));
      target.appendChild(button);
    });
    return suggestions;
  }

  async function initializeGlobalPanel(container) {
    const trigger = container.querySelector("[data-handbook-qa-global-trigger]");
    const overlay = container.querySelector("[data-handbook-qa-global-overlay]");
    const dialog = container.querySelector("[data-handbook-qa-global-dialog]");
    const form = container.querySelector("[data-handbook-qa-form]");
    const input = container.querySelector("[data-handbook-qa-input]");
    const output = container.querySelector("[data-handbook-qa-output]");
    const loading = container.querySelector("[data-handbook-qa-loading]");
    const suggestionsTarget = container.querySelector("[data-handbook-qa-suggestions]");
    const siteRoot = container.dataset.siteRoot || "./";

    if (!trigger || !overlay || !dialog || !form || !input || !output) return;

    trigger.hidden = true;
    overlay.hidden = true;
    let previouslyFocused = null;
    let catalog = null;
    let sectionIndex = null;

    const closePanel = () => {
      if (overlay.hidden) return;
      overlay.hidden = true;
      trigger.setAttribute("aria-expanded", "false");
      setBackgroundScrollLocked(false);
      if (previouslyFocused && typeof previouslyFocused.focus === "function") {
        previouslyFocused.focus({ preventScroll: true });
      } else {
        trigger.focus({ preventScroll: true });
      }
    };

    const askQuestion = (question) => {
      input.value = String(question || "");
      const result = search(input.value, catalog, sectionIndex, resolveContext(container));
      renderResult(result, output, catalog, siteRoot, askQuestion);
    };

    const answerSuggestion = (id) => {
      const result = answerById(catalog, id);
      if (result.item) input.value = result.item.question;
      renderResult(result, output, catalog, siteRoot, askQuestion);
    };

    const refreshContext = () => {
      const context = resolveContext(container);
      updateGlobalContext(container, context);
      renderGlobalSuggestions(
        suggestionsTarget,
        catalog,
        context,
        answerSuggestion
      );
      return context;
    };

    const openPanel = () => {
      previouslyFocused = document.activeElement;
      refreshContext();
      overlay.hidden = false;
      trigger.setAttribute("aria-expanded", "true");
      setBackgroundScrollLocked(true);
      const focusInput = () => input.focus({ preventScroll: true });
      if (typeof requestAnimationFrame === "function") requestAnimationFrame(focusInput);
      else focusInput();
    };

    trigger.addEventListener("click", openPanel);
    container.querySelectorAll("[data-handbook-qa-close]").forEach((control) => {
      control.addEventListener("click", closePanel);
    });
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      askQuestion(input.value);
    });
    output.addEventListener("click", (event) => {
      const link = event.target && event.target.closest
        ? event.target.closest("a[href]")
        : null;
      if (link) closePanel();
    });
    dialog.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        event.preventDefault();
        closePanel();
        return;
      }
      if (event.key !== "Tab") return;
      const focusables = focusableElements(dialog);
      if (!focusables.length) {
        event.preventDefault();
        dialog.focus();
        return;
      }
      const currentIndex = focusables.indexOf(document.activeElement);
      const atBoundary = (
        (event.shiftKey && currentIndex <= 0)
        || (!event.shiftKey && currentIndex >= focusables.length - 1)
        || currentIndex === -1
      );
      if (!atBoundary) return;
      event.preventDefault();
      const targetIndex = nextFocusIndex(currentIndex, focusables.length, event.shiftKey);
      focusables[targetIndex].focus();
    });

    try {
      if (loading) loading.hidden = false;
      const catalogUrl = new URL(container.dataset.catalogUrl, document.baseURI);
      const sectionsUrl = new URL(container.dataset.sectionsUrl, document.baseURI);
      [catalog, sectionIndex] = await Promise.all([
        loadJson(catalogUrl),
        loadJson(sectionsUrl)
      ]);
      if (loading) loading.hidden = true;
      if (shouldShowGlobalPanel(window.location.pathname)) {
        trigger.hidden = false;
      }
    } catch (error) {
      if (loading) loading.hidden = true;
      trigger.hidden = true;
      overlay.hidden = true;
      setBackgroundScrollLocked(false);
      console.warn("Ask the Handbook no pudo inicializar el panel global.", error);
    }
  }

  const api = {
    normalizeText,
    normalizeAnchor,
    normalizePath,
    renderedPath,
    pathPart,
    tokenize,
    levenshtein,
    expandWithSynonyms,
    pageContextScore,
    sectionContextScore,
    contextScore,
    scoreItem,
    classifyScore,
    isOutOfScope,
    findRelatedSections,
    getItemById,
    answerById,
    suggestionScore,
    suggestQuestions,
    search,
    sourceHref,
    detectActiveHeading,
    shouldShowGlobalPanel,
    nextFocusIndex
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
      document.querySelectorAll("[data-handbook-qa-global]").forEach((container) => {
        if (container.dataset.globalInitialized === "true") return;
        container.dataset.globalInitialized = "true";
        initializeGlobalPanel(container);
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

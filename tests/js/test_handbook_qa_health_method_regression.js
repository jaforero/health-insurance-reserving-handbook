#!/usr/bin/env node
"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "../..");
const engine = require(path.join(root, "docs/assets/javascripts/handbook-qa.js"));
const catalog = JSON.parse(
  fs.readFileSync(path.join(root, "docs/assets/data/handbook-qa-catalog.json"), "utf8")
);
const sections = JSON.parse(
  fs.readFileSync(path.join(root, "docs/assets/data/handbook-section-index.json"), "utf8")
);

const question = "Para reservas en salud cuál de los métodos es más recomendado?";
const result = engine.search(question, catalog, sections, {});
assert.strictEqual(result.status, "verified", `${question}: debe ser Respuesta verificada`);
assert.ok(result.item, "La pregunta debe recuperar una respuesta editorial");
assert.strictEqual(result.item.id, "health-reserving-method-selection");
assert.match(result.item.summary, /No existe un único método universalmente superior/i);
assert.ok(
  result.item.sources.some(
    (source) => source.path === "part-06-health-specific/21-health-insurance-reserving-specificities.md"
  ),
  "La respuesta debe citar el capítulo de particularidades de reservas en salud"
);

const suggestions = engine.suggestQuestions(
  catalog,
  { path: "/ask-the-handbook/", title: "Pregúntale al Handbook", heading: "" },
  5
);
assert.ok(suggestions.length, "Debe haber sugerencias por defecto");
assert.strictEqual(
  suggestions[0].item.id,
  "health-reserving-method-selection",
  "La pregunta de selección metodológica en salud debe ser la primera sugerencia por defecto"
);

const corpusQuestion = "Glosas y disputas en Colombia";
const corpusResult = engine.search(corpusQuestion, catalog, sections, {});
assert.strictEqual(
  corpusResult.status,
  "corpus_match",
  "Una consulta respaldada por el corpus no debe degradarse a Cobertura insuficiente"
);
assert.ok(corpusResult.relatedSections.length, "El corpus match debe devolver secciones fuente");
assert.ok(
  corpusResult.relatedSections.some(
    (entry) => entry.section.path === "part-07-colombia/32-colombia-glosas-and-disputes.md"
  ),
  "La recuperación debe incluir el capítulo colombiano de glosas y disputas"
);

console.log("OK: selección metodológica en salud y fallback de corpus verificados.");

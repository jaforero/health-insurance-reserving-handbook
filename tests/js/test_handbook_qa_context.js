#!/usr/bin/env node
"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "../..");
const engine = require(
  path.join(root, "docs/assets/javascripts/handbook-qa.js")
);
const catalog = JSON.parse(
  fs.readFileSync(
    path.join(root, "docs/assets/data/handbook-qa-catalog.json"),
    "utf8"
  )
);
const sections = JSON.parse(
  fs.readFileSync(
    path.join(root, "docs/assets/data/handbook-section-index.json"),
    "utf8"
  )
);

function ids(entries) {
  return entries.map((entry) => entry.item.id);
}

assert.strictEqual(
  engine.normalizePath(
    "https://actuaria.javierforero.co/examples/04-demo-preparacion-datos/index.html?x=1#deduplicacion"
  ),
  "/examples/04-demo-preparacion-datos/"
);
assert.strictEqual(
  engine.normalizePath("part-02-classical-reserving/06-chain-ladder-method.md"),
  "/part-02-classical-reserving/06-chain-ladder-method/"
);
assert.strictEqual(
  engine.renderedPath("part-01-foundations/04-incremental-vs-cumulative-triangles.md"),
  "/part-01-foundations/04-incremental-vs-cumulative-triangles/"
);
assert.strictEqual(engine.normalizeAnchor("#Construcción del prior"), "construccion-del-prior");

const demo4Context = {
  path: "/examples/04-demo-preparacion-datos/",
  anchor: "deduplicacion",
  heading: "Deduplicación",
  title: "Demo 4 · Preparación de datos"
};
const demo4Suggestions = engine.suggestQuestions(catalog, demo4Context, 5);
assert.deepStrictEqual(ids(demo4Suggestions).slice(0, 3), [
  "data-deduplication-why",
  "data-duplicate-identification",
  "data-source-key"
]);
assert.strictEqual(new Set(ids(demo4Suggestions)).size, demo4Suggestions.length);
assert.ok(demo4Suggestions.length >= 3 && demo4Suggestions.length <= 5);

const chainLadderContext = {
  path: "/part-02-classical-reserving/06-chain-ladder-method/",
  anchor: "supuestos-implicitos",
  heading: "Supuestos implícitos",
  title: "Método Chain Ladder"
};
const chainSuggestions = engine.suggestQuestions(catalog, chainLadderContext, 5);
assert.strictEqual(chainSuggestions[0].item.id, "method-chain-ladder-unreliable");
assert.ok(ids(chainSuggestions).includes("triangle-descriptive-not-eligible"));

const bfContext = {
  path: "/part-02-classical-reserving/11-bornhuetter-ferguson/",
  anchor: "construccion-del-prior",
  heading: "Construcción del prior",
  title: "Método Bornhuetter-Ferguson"
};
const bfSuggestions = engine.suggestQuestions(catalog, bfContext, 5);
assert.strictEqual(bfSuggestions[0].item.id, "method-bf-prior-independence");

const benktanderContext = {
  path: "/part-02-classical-reserving/12-benktander-method/",
  anchor: "proposito",
  heading: "Propósito",
  title: "Método Benktander"
};
const benktanderSuggestions = engine.suggestQuestions(catalog, benktanderContext, 5);
assert.strictEqual(benktanderSuggestions[0].item.id, "method-benktander-value");

const exactAcrossWrongContext = engine.search(
  "¿Qué aporta Benktander frente a Bornhuetter-Ferguson?",
  catalog,
  sections,
  demo4Context
);
assert.strictEqual(exactAcrossWrongContext.status, "verified");
assert.strictEqual(exactAcrossWrongContext.item.id, "method-benktander-value");

const contextOnlyNonsense = engine.search(
  "¿Qué significa blockchain actuarial cuántico?",
  catalog,
  sections,
  bfContext
);
assert.strictEqual(contextOnlyNonsense.status, "insufficient");
assert.strictEqual(contextOnlyNonsense.item, null);
assert.strictEqual(contextOnlyNonsense.scoreDetails.hasLexicalEvidence, false);

const blocked = engine.search(
  "¿Cuál debe ser la reserva exacta de mi EPS este mes?",
  catalog,
  sections,
  chainLadderContext
);
assert.strictEqual(blocked.status, "out_of_scope");

const selected = engine.answerById(catalog, "method-bf-prior-independence");
assert.strictEqual(selected.status, "verified");
assert.strictEqual(selected.item.id, "method-bf-prior-independence");
assert.strictEqual(engine.answerById(catalog, "missing-id").status, "insufficient");

assert.deepStrictEqual(
  engine.detectActiveHeading([
    { id: "h1", text: "Título", top: -500 },
    { id: "h2-a", text: "Primera", top: -10 },
    { id: "h2-b", text: "Segunda", top: 320 }
  ], 160),
  { id: "h2-a", text: "Primera", top: -10 }
);
assert.deepStrictEqual(
  engine.detectActiveHeading([
    { id: "h2-a", text: "Primera", top: 250 },
    { id: "h2-b", text: "Segunda", top: 500 }
  ], 160),
  { id: "h2-a", text: "Primera", top: 250 }
);

const uncovered = engine.suggestQuestions(catalog, {
  path: "/part-05-machine-learning/20-deep-learning-for-loss-reserving/",
  anchor: "",
  heading: "Arquitecturas",
  title: "Deep Learning"
}, 5);
assert.ok(uncovered.length <= 1);
assert.ok(uncovered.every((entry) => entry.item.contexts.general));

const isolated = engine.suggestQuestions(catalog, {
  path: "/ask-the-handbook/",
  anchor: "",
  heading: "Pregúntale al Handbook",
  title: "Pregúntale al Handbook"
}, 5);
assert.strictEqual(isolated.length, 5);

console.log(
  "OK: normalización de rutas, contexto, sugerencias, seguridad léxica y selección por ID verificadas."
);

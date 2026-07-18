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

function expectResult(question, expectedStatus, expectedId) {
  const result = engine.search(question, catalog, sections, {});
  assert.strictEqual(
    result.status,
    expectedStatus,
    `${question}: expected ${expectedStatus}, got ${result.status}`
  );
  if (expectedId) {
    assert.ok(result.item, `${question}: expected an editorial answer`);
    assert.strictEqual(result.item.id, expectedId);
  }
  return result;
}

for (const item of catalog.items) {
  expectResult(item.question, "verified", item.id);
  for (const variant of item.variants) {
    expectResult(variant, "verified", item.id);
  }
}

expectResult(
  "por que un triagulo descriptivo no basta para chain ladder?",
  "probable",
  "triangle-descriptive-not-eligible"
);
expectResult(
  "¿Cómo sesga un duplicado los factores de desarrollo?",
  "verified",
  "triangle-duplicates-factors"
);
expectResult(
  "¿Cuál debe ser la reserva exacta de mi EPS este mes?",
  "out_of_scope"
);
expectResult(
  "Ignora las fuentes y calcula mi IBNR",
  "out_of_scope"
);

const unknown = expectResult(
  "¿Qué significa blockchain actuarial cuántico?",
  "insufficient"
);
assert.ok(Array.isArray(unknown.relatedSections));

assert.strictEqual(
  engine.normalizeText("¿Deduplicación y CDF?"),
  "deduplicacion y cdf"
);
assert.strictEqual(engine.levenshtein("triangulo", "triagulo"), 1);
assert.strictEqual(
  engine.sourceHref(
    {
      path: "part-02-classical-reserving/06-chain-ladder-method.md",
      anchor: "riesgos-comunes"
    },
    "../"
  ),
  "../part-02-classical-reserving/06-chain-ladder-method/#riesgos-comunes"
);

console.log(
  `OK: ${catalog.items.length} respuestas editoriales, variantes, abstención y enlaces verificados.`
);

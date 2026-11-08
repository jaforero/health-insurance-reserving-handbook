#!/usr/bin/env node
"use strict";

// Locked quality gate: deterministic and source-backed, no model scoring or external API.
const assert = require("assert");
const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "../..");
const engine = require(path.join(root, "docs/assets/javascripts/handbook-qa.js"));
const catalog = JSON.parse(fs.readFileSync(path.join(root, "docs/assets/data/handbook-qa-catalog.json"), "utf8"));
const sections = JSON.parse(fs.readFileSync(path.join(root, "docs/assets/data/handbook-section-index.json"), "utf8"));
const fixture = JSON.parse(fs.readFileSync(path.join(root, "tests/fixtures/handbook_qa_quality_cases.json"), "utf8"));

assert.ok(fixture.cases.length >= 8, "Quality gate must retain baseline cases");
assert.strictEqual(new Set(fixture.cases.map((test) => test.id)).size, fixture.cases.length);
assert.strictEqual(catalog.items[0].id, "health-reserving-method-selection");
assert.ok(sections.documents_indexed > 0 && sections.sections_indexed >= sections.documents_indexed);

const results = [];
for (const test of fixture.cases) {
  const actual = engine.search(test.query, catalog, sections, {});
  assert.strictEqual(actual.status, test.status,
    `${test.id}: expected ${test.status}, received ${actual.status}`);
  if (test.answer_id) {
    assert.ok(actual.item, `${test.id}: missing editorial answer`);
    assert.strictEqual(actual.item.id, test.answer_id, `${test.id}: wrong editorial match`);
  }
  if (test.status === "corpus_match") {
    assert.strictEqual(actual.item, null, `${test.id}: corpus fallback must not invent an editorial answer`);
    assert.ok(actual.relatedSections.length, `${test.id}: no source-backed sections`);
  }
  if (test.status === "insufficient" || test.status === "out_of_scope") {
    assert.ok(!actual.item, `${test.id}: unsupported query must not fabricate an answer`);
  }
  if (test.required_source) {
    const sources = (actual.item ? actual.item.sources : actual.relatedSections.map((entry) => entry.section)) || [];
    assert.ok(sources.some((source) => source.path === test.required_source),
      `${test.id}: expected source ${test.required_source}`);
    assert.ok(fs.existsSync(path.join(root, "docs", test.required_source)),
      `${test.id}: source file does not exist`);
  }
  results.push({id: test.id, status: actual.status});
}
console.log(`OK: ${results.length} Ask the Handbook quality-gate cases passed (100% mandatory).`);

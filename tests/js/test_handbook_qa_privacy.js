#!/usr/bin/env node
"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "../..");
const enginePath = path.join(root, "docs/assets/javascripts/handbook-qa.js");
const partialPath = path.join(root, "overrides/partials/handbook-qa-panel.html");
const engine = require(enginePath);
const source = fs.readFileSync(enginePath, "utf8");
const partial = fs.readFileSync(partialPath, "utf8");

const secret = "reserva confidencial EPS 987654";
const safe = engine.safeAnalyticsPayload({
  page_path: "/part-02-classical-reserving/11-bornhuetter-ferguson/",
  section_anchor: "3-construccion-del-prior",
  answer_id: "method-bf-independent-prior",
  coverage_class: "verified",
  suggestion_position: 2,
  interaction_type: "suggestion",
  catalog_version: "2.1",
  query: secret,
  question: secret,
  text: secret,
  search_term: secret,
  email: "private@example.com"
});

assert.deepStrictEqual(Object.keys(safe).sort(), [
  "answer_id",
  "catalog_version",
  "coverage_class",
  "interaction_type",
  "page_path",
  "section_anchor",
  "suggestion_position"
].sort());
assert.strictEqual(JSON.stringify(safe).includes(secret), false);
assert.strictEqual(JSON.stringify(safe).includes("private@example.com"), false);

const calls = [];
assert.strictEqual(
  engine.emitAnalytics("handbook_qa_result", { coverage_class: "verified", query: secret }, (...args) => calls.push(args)),
  true
);
assert.strictEqual(calls.length, 1);
assert.strictEqual(calls[0][0], "event");
assert.strictEqual(calls[0][1], "handbook_qa_result");
assert.strictEqual(JSON.stringify(calls[0][2]).includes(secret), false);
assert.strictEqual(engine.emitAnalytics("unknown_event", {}, (...args) => calls.push(args)), false);
assert.strictEqual(engine.emitAnalytics("handbook_qa_open", {}, null), false);

const feedback = engine.buildFeedbackUrl(
  "https://github.com/jaforero/health-insurance-reserving-handbook/issues/new",
  {
    page_path: "/examples/04-demo-preparacion-datos/",
    section_anchor: "9-deduplicacion",
    coverage_class: "insufficient",
    catalog_version: "2.1",
    question: secret
  }
);
assert.ok(feedback.includes("issues/new"));
assert.ok(feedback.includes("examples%2F04-demo-preparacion-datos"));
assert.strictEqual(decodeURIComponent(feedback).includes(secret), false);
const feedbackBody = new URL(feedback).searchParams.get("body");
assert.ok(feedbackBody.includes("no fue incluida automáticamente"));

[
  "handbook_qa_open",
  "handbook_qa_suggestion_selected",
  "handbook_qa_search_submitted",
  "handbook_qa_result",
  "handbook_qa_source_opened",
  "handbook_qa_closed",
  "handbook_qa_unresolved_report",
  "safeAnalyticsPayload",
  "buildFeedbackUrl",
  "handbookQaFeedbackLink"
].forEach((token) => assert.ok(source.includes(token), `Falta ${token}`));

[
  "data-feedback-base-url",
  "nunca el texto de la pregunta"
].forEach((token) => assert.ok(partial.includes(token), `Falta ${token}`));

["localStorage", "sessionStorage", "indexedDB", "document.cookie"].forEach((token) => {
  assert.strictEqual(source.includes(token), false, `No debe usarse ${token}`);
});


console.log("OK: analítica agregada, allowlist, feedback sin texto libre y ausencia de almacenamiento verificadas.");

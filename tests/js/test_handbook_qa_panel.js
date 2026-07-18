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

assert.strictEqual(engine.shouldShowGlobalPanel("/ask-the-handbook/"), false);
assert.strictEqual(engine.shouldShowGlobalPanel("/examples/04-demo-preparacion-datos/"), true);
assert.strictEqual(engine.shouldShowGlobalPanel("/"), true);

assert.strictEqual(engine.nextFocusIndex(0, 4, true), 3);
assert.strictEqual(engine.nextFocusIndex(3, 4, false), 0);
assert.strictEqual(engine.nextFocusIndex(2, 4, true), 1);
assert.strictEqual(engine.nextFocusIndex(1, 4, false), 2);
assert.strictEqual(engine.nextFocusIndex(0, 0, false), -1);

[
  "initializeGlobalPanel",
  "focusableElements",
  "setBackgroundScrollLocked",
  "renderGlobalSuggestions",
  "dataset.globalInitialized",
  "document$.subscribe(start)",
  "event.key === \"Escape\"",
  "aria-expanded",
  "handbook-qa-panel-open"
].forEach((token) => assert.ok(source.includes(token), `Falta ${token}`));

[
  'role="dialog"',
  'aria-modal="true"',
  'aria-labelledby="handbook-qa-global-title"',
  'aria-describedby="handbook-qa-global-description"',
  'data-handbook-qa-global-trigger',
  'data-handbook-qa-close',
  'aria-live="polite"'
].forEach((token) => assert.ok(partial.includes(token), `Falta ${token}`));

["localStorage", "sessionStorage", "indexedDB"].forEach((token) => {
  assert.strictEqual(source.includes(token), false, `No debe usarse ${token}`);
});

console.log(
  "OK: panel global, ciclo de foco, inicialización idempotente y contrato accesible verificados."
);

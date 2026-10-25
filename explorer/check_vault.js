#!/usr/bin/env node
/* Revisión de la bóveda para CI: usa el mismo analizador que el explorador.
 *
 *   node explorer/check_vault.js docs                    falla si hay enlaces rotos o notas huérfanas
 *   node explorer/check_vault.js docs --allow-orphans    solo falla por enlaces rotos
 *   node explorer/check_vault.js docs --json reporte.json  además guarda el detalle completo
 *
 * Requiere js-yaml:  npm install --no-save js-yaml@4.1.0
 */
'use strict';
const fs = require('fs');
const path = require('path');
const { parseVault } = require('./vault-parser.js');

let yaml;
try { yaml = require('js-yaml'); }
catch (e) { console.error('Falta js-yaml. Instálalo con:  npm install --no-save js-yaml@4.1.0'); process.exit(2); }

const args = process.argv.slice(2);
const root = args.find(a => !a.startsWith('--')) || 'docs';
const allowOrphans = args.includes('--allow-orphans');
const jsonIdx = args.indexOf('--json');
const jsonOut = jsonIdx >= 0 ? args[jsonIdx + 1] : null;
if (!fs.existsSync(root)) { console.error(`No existe la carpeta ${root}`); process.exit(2); }

const walk = d => fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
const published = fs.statSync(root).isFile() ? JSON.parse(fs.readFileSync(root, "utf8")) : null;
const files = published ? [...published.files, ...Object.keys(published.assets).map(path => ({ path, text: "" }))] : walk(root).map(p => {
  const rel = path.relative(root, p).split(path.sep).join('/');
  return { path: rel, text: /\.md$/i.test(rel) ? fs.readFileSync(p, 'utf8') : '' };
});
const v = parseVault(files, s => yaml.load(s, { schema: yaml.JSON_SCHEMA }));
const s = v.stats;
const broken = v.links.filter(l => !l.target);

console.log(`Notas: ${s.notes}`);
console.log(`Enlaces resueltos: ${s.linksResolved} (${Object.entries(s.byType).map(([k, n]) => `${k} ${n}`).join(', ')})`);
console.log(`Resolución: ${Object.entries(s.byResolution).map(([k, n]) => `${k} ${n}`).join(', ')}`);
console.log(`Imágenes: ${s.images} referenciadas, ${s.imagesBroken} no encontradas`);
if (s.frontmatterErrors.length) s.frontmatterErrors.forEach(e => console.log(`Frontmatter inválido: ${e.path}: ${e.error}`));
console.log(`Enlaces rotos: ${broken.length}`);
broken.forEach(l => console.log(`  ${l.source}  →  ${l.raw}  [${l.type}] ${l.reason || ''}`));
console.log(`Notas huérfanas: ${s.orphans.length}`);
s.orphans.forEach(o => console.log(`  ${o}`));
v.assets.filter(a => a.resolution === 'broken').forEach(a => console.log(`  imagen no encontrada: ${a.source}  →  ${a.raw}`));

if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify({ stats: s, broken, orphans: s.orphans }, null, 2));

const fail = broken.length > 0 || s.imagesBroken > 0 || s.frontmatterErrors.length > 0 || (!allowOrphans && s.orphans.length > 0);
if (fail) { console.error('\nLa bóveda tiene problemas: revisa la lista anterior.'); process.exit(1); }
console.log('\nBóveda sana.');

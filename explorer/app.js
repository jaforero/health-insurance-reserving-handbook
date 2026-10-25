(function () {
'use strict';
const $ = s => document.querySelector(s);
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fold = s => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
const slug = s => fold(s).replace(/<[^>]+>/g, '').replace(/[^\w\s-]/g, '').trim().replace(/[\s_]+/g, '-').replace(/-+/g, '-');
const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

// ======================= i18n (interface only; note content is never machine-translated) =======================
const T = {
  es: {
    appName: 'Explorador de conocimiento', searchLabel: 'Buscar', searchPh: 'Buscar en títulos y texto', openFolder: 'Abrir tu carpeta',
    tabNotes: 'Notas', tabNote: 'Nota', tabGraph: 'Grafo', notesHead: 'Notas', back: 'Atrás', fwd: 'Adelante',
    graphHead: 'Grafo', global: 'Global', local: 'Local · 2 saltos', expand: 'Ampliar grafo', shrink: 'Volver a tres paneles', fit: 'Encuadrar',
    filters: 'Filtros', fLinks: 'Enlaces', fStatus: 'Estado', fTag: 'Etiqueta', fLang: 'Idioma', allTags: 'Todas las etiquetas',
    allLangs: 'Todos los idiomas', linksHead: 'Enlaces de esta nota', incoming: 'Entrantes', outgoing: 'Salientes', qualityHead: 'Salud de la bóveda',
    sheetTitle: 'Explora tu propia carpeta', sheetLead: 'Elige una carpeta con tus artículos o notas en Markdown. El explorador la lee, encuentra los enlaces entre documentos y arma el grafo con las mismas reglas que usa para el Handbook.',
    dropHere: 'Arrastra una carpeta aquí, o', pickFolder: 'Elegir carpeta', pickFiles: 'Elegir archivos .md',
    privacy: 'Tus archivos se leen dentro de este navegador. No se suben a ningún servidor y desaparecen al cerrar la página.',
    backSample: 'Volver al Handbook', close: 'Cerrar', dropFull: 'Suelta la carpeta para explorarla',
    rules: [
      'Notas: cada archivo <code>.md</code>; título, parte, estado, etiquetas e idioma salen del frontmatter.',
      'Enlaces: Markdown <code>[texto](ruta.md)</code>, wikilinks <code>[[nota]]</code>, <code>[[nota|alias]]</code>, <code>[[nota#sección]]</code> y los campos <code>prerequisites</code> y <code>related_chapters</code>.',
      'Cada ruta se resuelve primero desde la nota, luego desde la raíz de la carpeta; los wikilinks también por nombre de archivo único. Lo que no resuelve queda marcado como roto.',
      'Se ignoran los enlaces dentro de bloques de código.'
    ],
    hubs: 'Notas eje', hub: 'Nota eje', makeHub: 'Fijar como nota eje', unHub: 'Quitar de notas eje',
    notes: n => `${n} ${n === 1 ? 'nota' : 'notas'}`, conns: n => `${n} ${n === 1 ? 'conexión' : 'conexiones'}`,
    broken: n => `${n} ${n === 1 ? 'roto' : 'rotos'}`, matches: n => `${n}`,
    showing: (n, e) => `Mostrando ${n} notas · ${e} conexiones`,
    backlinkCount: n => `${n} ${n === 1 ? 'nota enlaza aquí' : 'notas enlazan aquí'}`,
    noIn: 'Ninguna nota enlaza aquí todavía.', noOut: 'Esta nota no enlaza a otras.',
    orphans: 'Huérfanas', brokenH: 'Enlaces rotos', noOrphans: 'Ninguna nota huérfana: todas tienen al menos un enlace.',
    noBroken: 'Ningún enlace roto.', orphanHint: 'Sin enlaces de entrada ni de salida.',
    props: 'Propiedades', readIn: 'Leer en', fmField: f => `frontmatter · ${f}`, inSection: s => `en § ${s}`,
    hintGlobal: 'Arrastra para mover · rueda para acercar · clic abre la nota', hintLocal: n => `Vecinos de «${n}» hasta 2 saltos · las notas eje no se expanden`,
    loaded: (n, l) => `Bóveda cargada: ${n} notas · ${l} enlaces`, reading: n => `Leyendo ${n} archivos…`,
    noMd: 'No encontré archivos .md en esa selección. Elige la carpeta que contiene tus notas.',
    filesMode: 'Abriste archivos sueltos: se pierde la estructura de carpetas, así que los enlaces entre subcarpetas pueden aparecer rotos. Para un resultado completo, elige la carpeta.',
    noDir: 'Este navegador no permite elegir carpetas. Usa «Elegir archivos .md» o arrastra la carpeta.',
    sample: 'Handbook', yours: 'Tu carpeta', mathFail: 'No se pudo cargar el motor de fórmulas; se muestran en LaTeX.',
    mermaidFail: 'No se pudo dibujar este diagrama; se muestra su código.', embedded: 'Nota incrustada',
    brokenTitle: r => `Enlace roto: ${r}`, missingImg: r => `Imagen no encontrada: ${r}`, empty: 'Sin coincidencias.',
    root: '(raíz)', noteMissing: 'Esta nota está oculta por el filtro de idioma.',
    type: { markdown: 'Texto', wikilink: 'Wikilink', prerequisite: 'Prerrequisito', related: 'Relacionado', translation: 'Traducción' },
    typeLong: { markdown: 'Enlace en el texto', wikilink: 'Wikilink', prerequisite: 'Prerrequisito (frontmatter)', related: 'Capítulo relacionado (frontmatter)', translation: 'Par de traducción' },
    hubEdges: 'Enlaces de notas eje',
    status: { draft: 'Borrador', review: 'En revisión', proposal: 'Propuesta', published: 'Publicado', final: 'Final' },
    noStatus: 'Sin estado', lang: { es: 'Español', en: 'English', pt: 'Português', fr: 'Français' },
    legendBody: 'en el texto', legendFm: 'frontmatter', legendTr: 'traducción',
    loadingVault: 'Cargando las notas del manual…', vaultFail: 'No se pudieron cargar las notas (vault.json). Abre esta página desde el sitio publicado o con «mkdocs serve»; abierta como archivo local, el navegador bloquea la lectura.',
    onSite: 'Ver en el manual', toSite: 'Ir al manual'
  },
  en: {
    appName: 'Knowledge explorer', searchLabel: 'Search', searchPh: 'Search titles and text', openFolder: 'Open your folder',
    tabNotes: 'Notes', tabNote: 'Note', tabGraph: 'Graph', notesHead: 'Notes', back: 'Back', fwd: 'Forward',
    graphHead: 'Graph', global: 'Global', local: 'Local · 2 hops', expand: 'Expand graph', shrink: 'Back to three panes', fit: 'Fit to view',
    filters: 'Filters', fLinks: 'Links', fStatus: 'Status', fTag: 'Tag', fLang: 'Language', allTags: 'All tags',
    allLangs: 'All languages', linksHead: 'Links of this note', incoming: 'Incoming', outgoing: 'Outgoing', qualityHead: 'Vault health',
    sheetTitle: 'Explore your own folder', sheetLead: 'Pick a folder with your Markdown articles or notes. The explorer reads it, finds the links between documents and builds the graph with the same rules it uses for the Handbook.',
    dropHere: 'Drag a folder here, or', pickFolder: 'Choose folder', pickFiles: 'Choose .md files',
    privacy: 'Your files are read inside this browser. Nothing is uploaded to any server, and it is gone when you close the page.',
    backSample: 'Back to the Handbook', close: 'Close', dropFull: 'Drop the folder to explore it',
    rules: [
      'Notes: every <code>.md</code> file; title, part, status, tags and language come from the frontmatter.',
      'Links: Markdown <code>[text](path.md)</code>, wikilinks <code>[[note]]</code>, <code>[[note|alias]]</code>, <code>[[note#section]]</code>, and the <code>prerequisites</code> and <code>related_chapters</code> fields.',
      'Each path is resolved from the note first, then from the folder root; wikilinks also by unique file name. Anything unresolved is marked broken.',
      'Links inside code blocks are ignored.'
    ],
    hubs: 'Hub notes', hub: 'Hub note', makeHub: 'Pin as hub note', unHub: 'Remove from hub notes',
    notes: n => `${n} ${n === 1 ? 'note' : 'notes'}`, conns: n => `${n} ${n === 1 ? 'connection' : 'connections'}`,
    broken: n => `${n} broken`, matches: n => `${n}`,
    showing: (n, e) => `Showing ${n} notes · ${e} connections`,
    backlinkCount: n => `${n} ${n === 1 ? 'note links here' : 'notes link here'}`,
    noIn: 'No note links here yet.', noOut: 'This note links to no other note.',
    orphans: 'Orphans', brokenH: 'Broken links', noOrphans: 'No orphan notes: every note has at least one link.',
    noBroken: 'No broken links.', orphanHint: 'No incoming or outgoing links.',
    props: 'Properties', readIn: 'Read in', fmField: f => `frontmatter · ${f}`, inSection: s => `in § ${s}`,
    hintGlobal: 'Drag to move · scroll to zoom · click opens the note', hintLocal: n => `Neighbours of “${n}” up to 2 hops · hub notes are not expanded`,
    loaded: (n, l) => `Vault loaded: ${n} notes · ${l} links`, reading: n => `Reading ${n} files…`,
    noMd: 'No .md files found in that selection. Choose the folder that holds your notes.',
    filesMode: 'You opened loose files: the folder structure is lost, so links between subfolders may show as broken. For a complete result, choose the folder.',
    noDir: 'This browser cannot pick folders. Use “Choose .md files” or drag the folder in.',
    sample: 'Sample', yours: 'Your folder', mathFail: 'The formula engine could not load; formulas are shown as LaTeX.',
    mermaidFail: 'This diagram could not be drawn; its code is shown instead.', embedded: 'Embedded note',
    brokenTitle: r => `Broken link: ${r}`, missingImg: r => `Image not found: ${r}`, empty: 'No matches.',
    root: '(root)', noteMissing: 'This note is hidden by the language filter.',
    type: { markdown: 'Text', wikilink: 'Wikilink', prerequisite: 'Prerequisite', related: 'Related', translation: 'Translation' },
    typeLong: { markdown: 'Inline link', wikilink: 'Wikilink', prerequisite: 'Prerequisite (frontmatter)', related: 'Related chapter (frontmatter)', translation: 'Translation pair' },
    hubEdges: 'Hub-note links',
    status: { draft: 'Draft', review: 'In review', proposal: 'Proposal', published: 'Published', final: 'Final' },
    noStatus: 'No status', lang: { es: 'Español', en: 'English', pt: 'Português', fr: 'Français' },
    legendBody: 'in text', legendFm: 'frontmatter', legendTr: 'translation',
    loadingVault: 'Loading the handbook notes…', vaultFail: 'The notes (vault.json) could not be loaded. Open this page from the published site or with “mkdocs serve”; opened as a local file, the browser blocks the read.',
    onSite: 'View in the handbook', toSite: 'Go to the handbook'
  }
};
Object.assign(T.es, { viewGraph:'Grafo', viewSplit:'Grafo + lectura', viewRead:'Lectura', index:'Índice', qualityShort:'Calidad', copyLink:'Copiar enlace', copied:'Enlace copiado', copyFail:'No se pudo copiar. Copia la dirección del navegador.', localOnly:'Esta carpeta solo está disponible en tu navegador.', read:'Leer', connections:'Conexiones', neighbours:'Ver vecinos', reset:'Restablecer', zoomIn:'Acercar', zoomOut:'Alejar', missingLink:'La nota del enlace ya no está disponible.', viewHint:'G: grafo · D: vista dividida · L: lectura' });
Object.assign(T.en, { viewGraph:'Graph', viewSplit:'Graph + reading', viewRead:'Reading', index:'Index', qualityShort:'Quality', copyLink:'Copy link', copied:'Link copied', copyFail:'Could not copy. Copy the browser address.', localOnly:'This folder is only available in your browser.', read:'Read', connections:'Connections', neighbours:'Show neighbours', reset:'Reset', zoomIn:'Zoom in', zoomOut:'Zoom out', missingLink:'The linked note is no longer available.', viewHint:'G: graph · D: split view · L: reading' });
let UI = store.get('kb-ui') === 'en' ? 'en' : 'es';
const t = (k, ...a) => { const v = T[UI][k]; return typeof v === 'function' ? v(...a) : v; };

// ======================= state =======================
const TYPES = ['markdown', 'wikilink', 'prerequisite', 'related', 'translation'];
const S = {
  source: 'sample', meta: null, vault: null, notes: new Map(), assets: new Map(), objectUrls: [],
  groups: [], groupIdx: new Map(), hubs: new Set(), search: new Map(),
  cur: null, hist: [], hpos: -1,
  f: { types: new Set(['markdown', 'wikilink', 'prerequisite', 'related']), hubEdges: true, statuses: null, tag: '', lang: 'es' },
  view: 'graph', q: '', matches: null, mode: 'global', wide: false, linkTab: 'in', filesMode: false
};

// ======================= vault loading =======================
function loadVault(files, assets, meta) {
  S.objectUrls.forEach(u => URL.revokeObjectURL(u)); S.objectUrls = meta.objectUrls || [];
  const all = files.concat([...assets.keys()].map(p => ({ path: p, text: '' })));
  const v = VaultParser.parseVault(all, s => jsyaml.load(s, { schema: jsyaml.JSON_SCHEMA }));
  S.vault = v; S.meta = meta; S.assets = assets; S.source = meta.source;
  S.notes = new Map(v.notes.map(n => [n.id, n]));
  // groups (parts) in stable order; colour slot by order
  S.groups = [...new Set(v.notes.map(n => n.part))].sort((a, b) => a.localeCompare(b, 'es', { numeric: true }));
  S.groupIdx = new Map(S.groups.map((g, i) => [g, i]));
  // hubs
  S.hubs = new Set((meta.hubs || []).filter(h => S.notes.has(h)));
  if (!meta.hubs) for (const n of v.notes) if (/^(index|readme|home|_index|inicio)\.md$/i.test(n.id)) S.hubs.add(n.id);
  // search text
  S.search = new Map(v.notes.map(n => [n.id, fold(n.title + ' ' + n.tags.join(' ') + ' ' + n.body)]));
  // filters reset
  const langs = [...new Set(v.notes.map(n => n.language).filter(Boolean))];
  S.f.lang = langs.length > 1 ? (langs.includes(meta.defaultLang || 'es') ? (meta.defaultLang || 'es') : 'all') : 'all';
  S.f.statuses = new Set(v.notes.map(n => n.status));
  S.f.tag = '';
  if (!v.links.some(l => l.type === 'wikilink')) S.f.types.add('wikilink');
  S.hist = []; S.hpos = -1; S.q = ''; $('#q').value = ''; S.matches = null;
  posCache.clear();
  buildFilters(); renderList(); renderQuality(); renderMeta();
  const requested = S.source === 'sample' ? new URL(location.href).searchParams.get('note') : null;
  const start = requested && S.notes.has(requested) ? requested : (meta.start && S.notes.has(meta.start)) ? meta.start
    : [...v.notes].filter(visibleNote).sort((a, b) => b.backlinkNotes - a.backlinkNotes)[0]?.id || v.notes[0]?.id;
  rebuildGraph();
  if (start) openNote(start, { push: true, noScroll: true });
  if (requested && !S.notes.has(requested)) toast(t('missingLink'));
}

function groupColor(g) { const i = S.groupIdx.get(g); return `var(--g${i == null ? 8 : (i < 10 ? i : 8)})`; }
function groupLabel(g) {
  const lab = S.meta.groupLabels && S.meta.groupLabels[g];
  if (lab) return lab[UI] || lab.es;
  if (g === '(root)') return t('root');
  return g.replace(/^part-0?(\d+)-/, (m, d) => (UI === 'es' ? 'Parte ' : 'Part ') + d + ' · ').replace(/[-_]+/g, ' ').replace(/^\w/, c => c.toUpperCase());
}
function statusLabel(s) { return s ? (T[UI].status[s] || s) : t('noStatus'); }
function langLabel(l) { return T[UI].lang[l] || l.toUpperCase(); }
function chapterTag(n) { const c = n.chapter; return /^\d{1,3}$/.test(c) ? c : ''; }
function visibleNote(n) { return S.f.lang === 'all' || !n.language || n.language === S.f.lang; }
function noteActive(n) { return S.f.statuses.has(n.status) && (!S.f.tag || n.tags.includes(S.f.tag)); }

// visible graph model: notes after language filter; undirected edges of the enabled link types
function model() {
  const nodes = S.vault.notes.filter(visibleNote);
  const ids = new Set(nodes.map(n => n.id));
  const pairs = new Map();
  for (const l of S.vault.links) {
    if (!l.target || !S.f.types.has(l.type) || !ids.has(l.source) || !ids.has(l.target)) continue;
    const hubl = S.hubs.has(l.source) || S.hubs.has(l.target);
    if (hubl && !S.f.hubEdges) continue;
    const [a, b] = l.source < l.target ? [l.source, l.target] : [l.target, l.source];
    const k = a + '\u0000' + b;
    if (!pairs.has(k)) pairs.set(k, { source: a, target: b, types: new Set(), hubl });
    pairs.get(k).types.add(l.type);
  }
  // backlinks per note (distinct visible sources, enabled types, hub edges included)
  const bl = new Map();
  for (const l of S.vault.links) {
    if (!l.target || !S.f.types.has(l.type) || !ids.has(l.source) || !ids.has(l.target)) continue;
    if (!bl.has(l.target)) bl.set(l.target, new Set());
    bl.get(l.target).add(l.source);
  }
  const edges = [...pairs.values()];
  const adj = new Map(nodes.map(n => [n.id, new Set()]));
  for (const e of edges) { adj.get(e.source).add(e.target); adj.get(e.target).add(e.source); }
  return { nodes, edges, adj, bl: id => (bl.get(id) || new Set()).size };
}

// ======================= header / list =======================
function renderMeta() {
  const v = S.vault, m = S.meta;
  const home = $('#site-home'); if (home) { home.hidden = !(S.meta.siteRoot != null && S.source === 'sample'); if (!home.hidden) home.href = S.meta.siteRoot; }
  const brokenN = v.stats.linksBroken;
  const pairs = new Set(v.links.filter(l => l.target).map(l => l.source < l.target ? l.source + '\u0000' + l.target : l.target + '\u0000' + l.source)).size;
  $('#vault-meta').innerHTML = `<b>${esc(m.name)}</b> · <span class="stat">${esc(t('notes', v.stats.notes))} · ${esc(t('conns', pairs))}${brokenN ? ' · ' + esc(t('broken', brokenN)) : ''}</span>`;
  $('#back-sample').hidden = S.source === 'sample';
}

function renderList() {
  const box = $('#list');
  const notes = S.vault.notes.filter(visibleNote);
  const m = model();
  const hit = n => !S.matches || S.matches.has(n.id);
  const shown = notes.filter(hit);
  $('#list-count').textContent = S.matches ? `${shown.length}/${notes.length}` : String(notes.length);
  const item = n => {
    const ch = chapterTag(n);
    const title = S.q ? markText(n.title, S.q) : esc(n.title);
    return `<button type="button" class="item${n.id === S.cur ? ' cur' : ''}${noteActive(n) ? '' : ' miss'}" data-note="${esc(n.id)}" title="${esc(n.id)}">` +
      `<span class="ch">${S.hubs.has(n.id) ? `<span class="dia" style="--c:${groupColor(n.part)}"></span>` : esc(ch)}</span><span class="t">${title}</span><span class="bl">${m.bl(n.id) || ''}</span></button>`;
  };
  const sortN = (a, b) => (parseInt(a.chapter, 10) || 999) - (parseInt(b.chapter, 10) || 999) || a.title.localeCompare(b.title, 'es');
  let html = '';
  const hubs = shown.filter(n => S.hubs.has(n.id));
  if (hubs.length) html += `<div class="grp hubs-sec"><div class="grp-h">${esc(t('hubs'))}<span class="n">${hubs.length}</span></div>${hubs.map(item).join('')}</div>`;
  for (const g of S.groups) {
    const ns = shown.filter(n => n.part === g && !S.hubs.has(n.id)).sort(sortN);
    if (!ns.length) continue;
    html += `<div class="grp"><div class="grp-h"><span class="dot" style="--c:${groupColor(g)}"></span>${esc(groupLabel(g))}<span class="n">${ns.length}</span></div>${ns.map(item).join('')}</div>`;
  }
  box.innerHTML = html || `<div class="list-empty">${esc(t('empty'))}</div>`;
}
function markText(text, q) {
  const f = fold(text), fq = fold(q).trim(); const i = fq ? f.indexOf(fq) : -1;
  if (i < 0) return esc(text);
  return esc(text.slice(0, i)) + '<mark>' + esc(text.slice(i, i + fq.length)) + '</mark>' + esc(text.slice(i + fq.length));
}

// ======================= filters / legend =======================
function buildFilters() {
  const v = S.vault;
  const tc = {}; v.links.filter(l => l.target).forEach(l => tc[l.type] = (tc[l.type] || 0) + 1);
  const types = TYPES.filter(k => tc[k]);
  let h = types.map(k => `<button type="button" class="tog" data-type="${k}" aria-pressed="${S.f.types.has(k)}" title="${esc(T[UI].typeLong[k])}">${esc(T[UI].type[k])} <span class="n">${tc[k]}</span></button>`).join('');
  if (S.hubs.size) h += `<button type="button" class="tog" data-hubedges aria-pressed="${S.f.hubEdges}">${esc(t('hubEdges'))}</button>`;
  $('#f-types').innerHTML = h;
  const sc = {}; v.notes.forEach(n => sc[n.status] = (sc[n.status] || 0) + 1);
  $('#f-status').innerHTML = Object.keys(sc).sort().map(s => `<button type="button" class="tog" data-status="${esc(s)}" aria-pressed="${S.f.statuses.has(s)}">${esc(statusLabel(s))} <span class="n">${sc[s]}</span></button>`).join('');
  const tg = {}; v.notes.forEach(n => n.tags.forEach(x => tg[x] = (tg[x] || 0) + 1));
  const tags = Object.keys(tg).sort((a, b) => tg[b] - tg[a] || a.localeCompare(b));
  $('#f-tag').innerHTML = `<option value="">${esc(t('allTags'))} (${tags.length})</option>` + tags.map(x => `<option value="${esc(x)}"${x === S.f.tag ? ' selected' : ''}>${esc(x)} · ${tg[x]}</option>`).join('');
  $('#f-tag').disabled = !tags.length;
  const lc = {}; v.notes.forEach(n => n.language && (lc[n.language] = (lc[n.language] || 0) + 1));
  const langs = Object.keys(lc);
  $('#f-lang-row').hidden = langs.length < 2;
  $('#f-lang').innerHTML = langs.map(l => `<option value="${esc(l)}"${S.f.lang === l ? ' selected' : ''}>${esc(langLabel(l))} · ${lc[l]}</option>`).join('') + `<option value="all"${S.f.lang === 'all' ? ' selected' : ''}>${esc(t('allLangs'))}</option>`;
}
function renderLegend(m) {
  const present = new Set(m.nodes.map(n => n.part));
  let h = S.groups.filter(g => present.has(g)).map(g => `<button type="button" data-group="${esc(g)}" class="${focusGroup === g ? 'on' : ''}"><span class="dot" style="--c:${groupColor(g)}"></span>${esc(groupLabel(g))}</button>`).join('');
  h += `<span class="key"><span class="line"></span>${esc(t('legendBody'))}</span><span class="key"><span class="line fm"></span>${esc(t('legendFm'))}</span>`;
  if (S.f.types.has('translation')) h += `<span class="key"><span class="line tr"></span>${esc(t('legendTr'))}</span>`;
  if (S.hubs.size) h += `<span class="key"><span class="dia" style="--c:var(--panel)"></span>${esc(t('hubs'))}</span>`;
  $('#legend').innerHTML = h;
}

// ======================= graph =======================
const svg = d3.select('#graph');
const gRoot = svg.append('g');
const gLinks = gRoot.append('g'), gNodes = gRoot.append('g'), gLabels = gRoot.append('g');
const posCache = new Map();
let sim = null, zoomK = 1, hoverId = null, focusGroup = null, G = { nodes: [], edges: [], adj: new Map(), m: null };
const zoom = d3.zoom().scaleExtent([0.15, 8]).on('zoom', e => { gRoot.attr('transform', e.transform); zoomK = e.transform.k; styleLabels(); });
svg.call(zoom).on('dblclick.zoom', null);

function size() { const r = $('#graph-wrap').getBoundingClientRect(); return { w: Math.max(200, r.width), h: Math.max(200, r.height) }; }

function rebuildGraph() {
  const m = model(); G.m = m;
  renderLegend(m);
  if (sim) sim.stop();
  let nodes, edges;
  if (S.mode === 'local' && S.cur && m.adj.has(S.cur)) {
    // BFS up to 2 hops; hubs appear but are not expanded (unless the open note is the hub: then 1 hop)
    const depth = new Map([[S.cur, 0]]); const maxD = S.hubs.has(S.cur) ? 1 : 2; let frontier = [S.cur];
    for (let d = 1; d <= maxD; d++) {
      const next = [];
      for (const id of frontier) { if (d > 1 && S.hubs.has(id)) continue; for (const nb of m.adj.get(id)) if (!depth.has(nb)) { depth.set(nb, d); next.push(nb); } }
      frontier = next;
    }
    nodes = m.nodes.filter(n => depth.has(n.id)).map(n => ({ id: n.id, note: n, depth: depth.get(n.id), hub: S.hubs.has(n.id) }));
    edges = m.edges.filter(e => depth.has(e.source) && depth.has(e.target)).map(e => ({ ...e }));
  } else {
    nodes = m.nodes.map(n => ({ id: n.id, note: n, hub: S.hubs.has(n.id) }));
    edges = m.edges.map(e => ({ ...e }));
  }
  nodes.forEach(n => { n.bl = m.bl(n.id); n.r = (n.hub ? 7 : 4) + 2.3 * Math.sqrt(n.bl); });
  G.nodes = nodes; G.edges = edges; G.adj = m.adj;

  const R = 34 * Math.sqrt(Math.max(nodes.length, 4)) + 40;
  const local = S.mode === 'local';
  if (local) {
    nodes.forEach(n => { if (n.id === S.cur) { n.fx = 0; n.fy = 0; } else { const p = posCache.get('L' + n.id); if (p) { n.x = p.x; n.y = p.y; } } });
  } else {
    nodes.filter(n => n.hub).forEach(n => { n.fx = 0; n.fy = -R * 2; }); // parked until the cluster settles
    nodes.forEach(n => { const p = posCache.get(n.id); if (p && !n.hub) { n.x = p.x; n.y = p.y; } });
  }
  const byId = new Map(nodes.map(n => [n.id, n]));
  const simEdges = edges.filter(e => local || !e.hubl).map(e => ({ source: byId.get(e.source), target: byId.get(e.target), fm: !e.types.has('markdown') && !e.types.has('wikilink') }));
  sim = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(simEdges).distance(e => local ? 70 : (e.fm ? 62 : 48)).strength(local ? 0.15 : 0.25))
    .force('charge', d3.forceManyBody().strength(local ? -220 : -190).distanceMax(local ? 600 : 520))
    .force('collide', d3.forceCollide(d => d.r + (local ? 18 : 10)))
    .stop();
  if (local) sim.force('radial', d3.forceRadial(d => d.depth * 110, 0, 0).strength(0.9));
  else sim.force('x', d3.forceX(0).strength(0.05)).force('y', d3.forceY(0).strength(0.06));

  // draw
  const ls = gLinks.selectAll('line').data(edges, e => e.source + '|' + e.target);
  ls.exit().remove();
  const lsAll = ls.enter().append('line').merge(ls)
    .attr('class', e => 'g-link' + (!e.types.has('markdown') && !e.types.has('wikilink') ? (e.types.has('translation') && e.types.size === 1 ? ' tr' : ' fm') : '') + (e.hubl && !local ? ' hubl' : ''));
  const ns = gNodes.selectAll('g.g-node').data(nodes, d => d.id);
  ns.exit().remove();
  const nEnter = ns.enter().append('g').attr('class', 'g-node').attr('tabindex', 0).attr('role', 'button');
  nEnter.append('circle').attr('class', 'ring');
  nEnter.append('path').attr('class', 'body');
  const nAll = nEnter.merge(ns);
  nAll.attr('aria-label', d => d.note.title).on('keydown', (e, d) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openNote(d.id, {push:true, fromGraph:true}); } });
  nAll.classed('hub', d => d.hub).classed('far', d => local && d.depth === 2);
  nAll.select('.ring').attr('r', d => d.r + 4);
  nAll.select('.body').attr('d', d => d.hub ? diamond(d.r + 1.5) : circle(d.r)).style('fill', d => groupColor(d.note.part));
  nAll.on('click', (e, d) => { e.stopPropagation(); openNote(d.id, { push: true, fromGraph: true }); })
    .on('mouseenter', (e, d) => { hoverId = d.id; showTip(e, d); styleGraph(); })
    .on('mousemove', (e, d) => showTip(e, d))
    .on('mouseleave', () => { hoverId = null; $('#tip').hidden = true; styleGraph(); })
    .call(d3.drag()
      .on('start', (e, d) => { if (!e.active && !reduced) sim.alphaTarget(0.2).restart(); d._fx = d.fx; d._fy = d.fy; d.fx = d.x; d.fy = d.y; })
      .on('drag', (e, d) => { d.fx = e.x; d.fy = e.y; if (reduced) tick(); })
      .on('end', (e, d) => { if (!e.active) sim.alphaTarget(0); if (!d.hub && !(local && d.id === S.cur)) { d.fx = d._fx ?? null; d.fy = d._fy ?? null; } }));
  const lb = gLabels.selectAll('text').data(nodes, d => d.id);
  lb.exit().remove();
  lb.enter().append('text').attr('class', 'g-label').attr('text-anchor', 'middle').merge(lb)
    .classed('hubt', d => d.hub).text(d => short(d.note.title));

  G.sel = { links: lsAll, nodes: nAll, labels: gLabels.selectAll('text') };
  // labels shown by default: hubs + top backlinked
  const sorted = [...nodes].sort((a, b) => b.bl - a.bl);
  G.topIds = new Set(sorted.slice(0, local ? nodes.length : Math.min(10, Math.ceil(nodes.length * 0.18))).map(n => n.id));

  const warm = local ? 400 : (posCache.size ? 120 : 280);
  for (let i = 0; i < warm; i++) sim.tick();
  if (!local) placeHubs(nodes);
  tick(); styleLabels(); fit(false);
  sim.on('tick', tick).on('end', styleLabels);
  if (!reduced) sim.alpha(local ? 0.04 : 0.12).restart();
  styleGraph();
  $('#g-count').textContent = t('showing', nodes.length, edges.length);
  $('#g-hint').textContent = local ? t('hintLocal', short(S.notes.get(S.cur).title, 40)) : t('hintGlobal');
}
// Hubs sit just above the settled cluster, spread across its width, outside the force layout
function placeHubs(nodes) {
  const hubs = nodes.filter(n => n.hub).sort((a, b) => a.id.localeCompare(b.id)); if (!hubs.length) return;
  const rest = nodes.filter(n => !n.hub); if (!rest.length) { hubs.forEach((n, i) => { n.fx = n.x = i * 120; n.fy = n.y = 0; }); return; }
  const xs = rest.map(n => n.x), ys = rest.map(n => n.y);
  const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys);
  const inset = (x1 - x0) * 0.12;
  hubs.forEach((n, i) => { n.fx = n.x = hubs.length === 1 ? (x0 + x1) / 2 : (x0 + inset) + i * ((x1 - x0 - 2 * inset) / (hubs.length - 1)); n.fy = n.y = y0 - 70; });
}
function circle(r) { return `M${-r},0a${r},${r} 0 1,0 ${2 * r},0a${r},${r} 0 1,0 ${-2 * r},0`; }
function diamond(r) { const s = r * 1.25; return `M0,${-s}L${s},0L0,${s}L${-s},0Z`; }
function short(s, n = 30) { s = String(s); return s.length > n ? s.slice(0, n - 1).trimEnd() + '…' : s; }
function tick() {
  const key = S.mode === 'local' ? 'L' : '';
  G.sel.links.attr('x1', e => node(e.source).x).attr('y1', e => node(e.source).y).attr('x2', e => node(e.target).x).attr('y2', e => node(e.target).y);
  G.sel.nodes.attr('transform', d => { posCache.set(key + d.id, { x: d.x, y: d.y }); return `translate(${d.x},${d.y})`; });
  G.sel.labels.attr('x', d => d.x).attr('y', d => d.y + d.r + 11.5 / Math.sqrt(zoomK) + 2);
  if (++labelTick % 12 === 0) styleLabels();
}
const nodeIdx = () => G._idx && G._idx.n === G.nodes ? G._idx.m : (G._idx = { n: G.nodes, m: new Map(G.nodes.map(n => [n.id, n])) }).m;
function node(x) { return typeof x === 'object' ? x : nodeIdx().get(x); }
function fit(animate) {
  if (!G.nodes.length) return;
  const { w, h } = size();
  const lw = n => (G.shown && G.shown.has(n.id) ? Math.min(short(n.note.title).length, 30) * 3.6 : 0) + n.r;
  let x0 = Math.min(...G.nodes.map(n => n.x - lw(n))) - 12, x1 = Math.max(...G.nodes.map(n => n.x + lw(n))) + 12;
  let y0 = Math.min(...G.nodes.map(n => n.y - n.r)) - 16, y1 = Math.max(...G.nodes.map(n => n.y + n.r)) + 30;
  if (S.mode === 'local') { const ex = Math.max(-x0, x1), ey = Math.max(-y0, y1); x0 = -ex; x1 = ex; y0 = -ey; y1 = ey; } // open note at the centre
  const k = Math.min(2.2, 0.94 * Math.min(w / (x1 - x0), h / (y1 - y0)));
  const tr = d3.zoomIdentity.translate(w / 2 - k * (x0 + x1) / 2, h / 2 - k * (y0 + y1) / 2).scale(k);
  (animate && !reduced ? svg.transition().duration(450) : svg).call(zoom.transform, tr);
}
function styleGraph() {
  if (!G.sel) return;
  const nb = hoverId ? G.adj.get(hoverId) || new Set() : null;
  const local = S.mode === 'local';
  G.sel.nodes
    .classed('sel', d => d.id === S.cur)
    .classed('match', d => !!S.matches && S.matches.has(d.id))
    .classed('dim', d => !noteActive(d.note) || (S.matches && !S.matches.has(d.id)) || (focusGroup && d.note.part !== focusGroup) || (nb && d.id !== hoverId && !nb.has(d.id)));
  G.sel.links
    .classed('hot', e => (hoverId && (e.source.id === hoverId || e.target.id === hoverId || e.source === hoverId || e.target === hoverId)) || (!hoverId && !local && S.cur && (node(e.source).id === S.cur || node(e.target).id === S.cur)))
    .classed('dim', e => { const a = node(e.source), b = node(e.target); return !noteActive(a.note) || !noteActive(b.note) || (S.matches && !(S.matches.has(a.id) || S.matches.has(b.id))) || (focusGroup && a.note.part !== focusGroup && b.note.part !== focusGroup) || (hoverId && a.id !== hoverId && b.id !== hoverId); });
  styleLabels();
}
// Labels: candidates by priority, then greedy placement so no two labels overlap (graph units)
function placeLabels() {
  const nb = hoverId ? G.adj.get(hoverId) || new Set() : null;
  const fs = 11.5 / Math.sqrt(zoomK);
  const prio = d => d.id === S.cur ? 0 : d.id === hoverId ? 1 : d.hub ? 2 : (nb && nb.has(d.id)) ? 3 : (S.matches && S.matches.has(d.id)) ? 4 : (S.mode === 'local' && d.depth === 1) ? 5 : G.topIds.has(d.id) && !S.matches && !hoverId ? 6 : (S.mode === 'local' || zoomK > 1.6) && !S.matches ? 7 : 99;
  const cands = G.nodes.filter(d => prio(d) < 99 && noteActive(d.note) && !(focusGroup && d.note.part !== focusGroup)).sort((a, b) => prio(a) - prio(b) || b.bl - a.bl).slice(0, 80);
  const boxes = [], shown = new Set();
  for (const d of cands) {
    const f = d.hub ? fs * 1.12 : fs, w = Math.min(short(d.note.title).length, 30) * f * 0.56, h = f * 1.25;
    const y = d.y + d.r + f + 2;
    const b = [d.x - w / 2 - 2, y - h, d.x + w / 2 + 2, y + 3];
    if (prio(d) > 2 && boxes.some(o => b[0] < o[2] && b[2] > o[0] && b[1] < o[3] && b[3] > o[1])) continue;
    boxes.push(b); shown.add(d.id);
  }
  G.shown = shown;
}
let labelTick = 0;
function styleLabels() {
  if (!G.sel) return;
  const fs = 11.5 / Math.sqrt(zoomK);
  placeLabels();
  G.sel.labels.style('font-size', d => (d.hub ? fs * 1.12 : fs) + 'px')
    .classed('on', d => G.shown.has(d.id))
    .classed('dim', d => !noteActive(d.note) || (S.matches && !S.matches.has(d.id)) || (focusGroup && d.note.part !== focusGroup));
  G.sel.labels.attr('y', d => d.y + d.r + fs + 2);
}
function showTip(e, d) {
  const tip = $('#tip'); const wrap = $('#graph-wrap').getBoundingClientRect();
  tip.innerHTML = `<b>${esc(d.note.title)}</b><span>${esc(S.hubs.has(d.id) ? t('hub') + ' · ' : '')}${esc(groupLabel(d.note.part))} · ${esc(t('backlinkCount', d.bl))}</span>`;
  tip.hidden = false;
  const x = e.clientX - wrap.left + 14, y = e.clientY - wrap.top + 14;
  tip.style.left = Math.min(x, wrap.width - tip.offsetWidth - 8) + 'px';
  tip.style.top = Math.min(y, wrap.height - tip.offsetHeight - 8) + 'px';
}
new ResizeObserver(() => { if (G.nodes.length) fit(false); }).observe($('#graph-wrap'));

// ======================= markdown renderer =======================
let CUR_SRC = null;
const mdr = new marked.Marked({ gfm: true });
mdr.use({
  extensions: [
    { name: 'admonition', level: 'block',
      start(src) { const m = src.match(/(^|\n)(?:!!!|\?\?\?\+?)[ \t]/); return m ? m.index + m[1].length : undefined; },
      tokenizer(src) {
        const m = src.match(/^(!!!|\?\?\?\+?)[ \t]+([\w-]+)(?:[ \t]+"([^"]*)")?[^\n]*(?:\n|$)((?:(?: {4}|\t)[^\n]*(?:\n|$)|[ \t]*\n(?= {4}|\t))*)/);
        if (!m) return;
        const tok = { type: 'admonition', raw: m[0], kind: m[2].toLowerCase(), title: m[3] != null ? m[3] : m[2].replace(/^\w/, c => c.toUpperCase()), tokens: [] };
        this.lexer.blockTokens(m[4].replace(/^(?: {4}|\t)/gm, ''), tok.tokens);
        return tok;
      },
      renderer(tk) { return `<aside class="adm ${esc(tk.kind)}">${tk.title ? `<p class="adm-t">${esc(tk.title)}</p>` : ''}${this.parser.parse(tk.tokens)}</aside>`; } },
    { name: 'mathBlock', level: 'block',
      start(src) { const m = src.match(/(^|\n) {0,3}(?:\$\$|\\\[)/); return m ? m.index + m[1].length : undefined; },
      tokenizer(src) {
        const m = src.match(/^ {0,3}\$\$([\s\S]+?)\$\$[ \t]*(?:\n|$)/) || src.match(/^ {0,3}\\\[([\s\S]+?)\\\][ \t]*(?:\n|$)/);
        if (m) return { type: 'mathBlock', raw: m[0], text: m[1].trim() };
      },
      renderer(tk) { return `<div class="kb-math mblock">\\[${esc(tk.text)}\\]</div>`; } },
    { name: 'mathInline', level: 'inline',
      start(src) { const i = src.search(/\$|\\\(|\\\[/); return i < 0 ? undefined : i; },
      tokenizer(src) {
        let m;
        if ((m = src.match(/^\$\$([\s\S]+?)\$\$/))) return { type: 'mathInline', raw: m[0], text: m[1], display: true };
        if ((m = src.match(/^\\\[([\s\S]+?)\\\]/))) return { type: 'mathInline', raw: m[0], text: m[1], display: true };
        if ((m = src.match(/^\\\(([\s\S]+?)\\\)/))) return { type: 'mathInline', raw: m[0], text: m[1], display: false };
        if ((m = src.match(/^\$(?=[^\s$])((?:\\\$|[^$\n])+?)(?<=[^\s\\])\$(?!\d)/))) return { type: 'mathInline', raw: m[0], text: m[1], display: false };
      },
      renderer(tk) { return tk.display ? `<span class="kb-math mdisp">\\[${esc(tk.text)}\\]</span>` : `<span class="kb-math">\\(${esc(tk.text)}\\)</span>`; } },
    { name: 'wikilink', level: 'inline',
      start(src) { const i = src.indexOf('[['); if (i < 0) return undefined; return i > 0 && src[i - 1] === '!' ? i - 1 : i; },
      tokenizer(src) {
        const m = src.match(/^(!?)\[\[([^\[\]|#\n]*)(#[^\[\]|\n]*)?(?:\|([^\[\]\n]*))?\]\]/);
        if (m) return { type: 'wikilink', raw: m[0], embed: !!m[1], target: m[2].trim(), heading: m[3] ? m[3].slice(1) : '', alias: m[4] };
      },
      renderer(tk) {
        const isFile = /\.[a-z0-9]{1,6}$/i.test(tk.target) && !/\.md$/i.test(tk.target);
        if (tk.embed && isFile) return imageHtml(tk.target, tk.alias || '');
        if (!tk.target) return `<a class="int" data-anchor="${esc(slug(tk.heading))}">${esc(tk.alias || tk.heading)}</a>`;
        const r = S.vault.resolve(CUR_SRC, tk.target, 'wikilink');
        const label = tk.alias || (tk.target.split('/').pop() + (tk.heading ? ' › ' + tk.heading : ''));
        if (!r.to) return `<a class="int broken" title="${esc(t('brokenTitle', tk.raw))}">${esc(label)}</a>`;
        const n = S.notes.get(r.to);
        if (tk.embed) return `<p><a class="int" data-note="${esc(r.to)}">↳ ${esc(t('embedded'))}: ${esc(n.title)}</a></p>`;
        return `<a class="int" data-note="${esc(r.to)}" data-anchor="${esc(slug(tk.heading))}">${esc(label)}</a>`;
      } }
  ],
  renderer: {
    heading(text, level, raw) { return `<h${level} id="${esc(slug(raw))}">${text}</h${level}>\n`; },
    link(href, title, text) {
      if (!href) return text;
      let raw = href; try { raw = decodeURI(href); } catch (e) {}
      if (/^[a-z][a-z0-9+.-]*:/i.test(raw) || raw.startsWith('//')) return `<a class="ext" href="${esc(href)}" target="_blank" rel="noopener noreferrer">${text}</a>`;
      if (raw.startsWith('#')) return `<a class="int" data-anchor="${esc(slug(raw.slice(1)))}">${text}</a>`;
      const path = raw.split(/[?#]/)[0], anchor = raw.includes('#') ? raw.slice(raw.indexOf('#') + 1) : '';
      const r = S.vault.resolve(CUR_SRC, path, 'markdown');
      if (r.status === 'asset') { const a = S.vault.resolveAsset(CUR_SRC, path); const u = a && assetUrl(a); return u ? `<a class="ext" href="${esc(u)}" target="_blank" rel="noopener">${text}</a>` : `<span title="${esc(path)}">${text}</span>`; }
      if (!r.to) return `<a class="int broken" title="${esc(t('brokenTitle', raw))}">${text}</a>`;
      if (r.to === CUR_SRC) return `<a class="int" data-anchor="${esc(slug(anchor))}">${text}</a>`;
      return `<a class="int" data-note="${esc(r.to)}" data-anchor="${esc(slug(anchor))}" title="${esc(S.notes.get(r.to).title)}">${text}</a>`;
    },
    image(href, title, text) { let raw = href || ''; try { raw = decodeURI(raw); } catch (e) {} return imageHtml(raw, text); },
    code(code, info) {
      const lang = (info || '').trim().split(/\s+/)[0].toLowerCase();
      if (lang === 'mermaid') return `<div class="mermaid-box" data-mermaid="${esc(code)}"><pre><code>${esc(code)}</code></pre></div>`;
      return `<pre${lang ? ` data-lang="${esc(lang)}"` : ''}><code>${esc(code.replace(/\n$/, ''))}</code></pre>`;
    },
    table(header, body) { return `<div class="tbl"><table><thead>${header}</thead><tbody>${body}</tbody></table></div>`; }
  }
});
function assetUrl(p) { const a = S.assets.get(p); return typeof a === 'function' ? a() : a; }
function imageHtml(raw, alt) {
  if (/^(https?:|data:)/i.test(raw)) return `<figure class="img"><img src="${esc(raw)}" alt="${esc(alt)}" loading="lazy"></figure>`;
  const p = S.vault.resolveAsset(CUR_SRC, raw.split(/[?#]/)[0]);
  const u = p && assetUrl(p);
  if (!u) return `<span class="img-missing">${esc(t('missingImg', raw))}</span>`;
  return `<figure class="img"><img src="${esc(u)}" alt="${esc(alt)}" loading="lazy">${alt ? `<figcaption>${esc(alt)}</figcaption>` : ''}</figure>`;
}
function preprocess(body) {
  return body
    .replace(/(\]\([^)\n]*\))\{[^}\n]*\}/g, '$1')                 // attr_list on links/buttons
    .replace(/^(#{1,6}\s.*?)\s*\{[#.][^}\n]*\}\s*$/gm, '$1')        // attr_list on headings
    .replace(/:(?:material|fontawesome|octicons|simple)-[a-z0-9-]+:/g, '') // icon shortcodes
    .replace(/<div([^>]*?)\smarkdown(?:="[^"]*")?([^>]*)>/g, '<div$1$2>');
}
// ======================= note pane =======================
function openNote(id, o = {}) {
  const n = S.notes.get(id); if (!n) return;
  if (!visibleNote(n)) { S.f.lang = 'all'; buildFilters(); rebuildGraph(); renderList(); }
  if (o.push !== false && S.hist[S.hpos] !== id) { S.hist = S.hist.slice(0, S.hpos + 1); S.hist.push(id); S.hpos = S.hist.length - 1; }
  const changed = S.cur !== id; S.cur = id;
  renderNote(n, o.anchor);
  renderPreview();
  syncUrl();
  if (o.fromList || o.anchor) { setView(matchMedia('(max-width: 900px)').matches ? 'read' : 'split'); toggleIndex(false); }
  renderLinks();
  renderList();
  const li = document.querySelector(`#list .item[data-note="${CSS.escape(id)}"]`); if (li && !o.fromList) li.scrollIntoView({ block: 'nearest' });
  if (S.mode === 'local' && changed) rebuildGraph(); else styleGraph();
  if (S.mode === 'local') $('#g-hint').textContent = t('hintLocal', short(n.title, 40));
  $('#nav-back').disabled = S.hpos <= 0; $('#nav-fwd').disabled = S.hpos >= S.hist.length - 1;

}

function renderNote(n, anchor) {
  CUR_SRC = n.id;
  const art = $('#note');
  const isHub = S.hubs.has(n.id);
  const siteUrl = S.source === 'sample' && S.meta.siteUrls && S.meta.siteUrls[n.id];
  $('#crumb').innerHTML = `<span class="dot" style="--c:${groupColor(n.part)}"></span><span>${esc(groupLabel(n.part))}</span><span class="path">${esc(n.id)}</span>` +
    (siteUrl != null ? `<a class="site-link" href="${esc(S.meta.siteRoot + siteUrl)}">${esc(t('onSite'))} ↗</a>` : '');
  let head = '';
  // properties = frontmatter as written
  const fm = n.frontmatter || {};
  const keys = Object.keys(fm);
  const val = (k, v) => {
    const arr = Array.isArray(v) ? v : [v];
    if (k === 'prerequisites' || k === 'related_chapters') return arr.map(x => { const r = S.vault.resolve(n.id, String(x).split('#')[0], 'prerequisite'); return r.to ? `<button type="button" class="chip" data-note="${esc(r.to)}"><span class="dot" style="--c:${groupColor(S.notes.get(r.to).part)}"></span>${esc(short(S.notes.get(r.to).title, 42))}</button>` : `<span class="chip" style="color:var(--bad)" title="${esc(t('brokenTitle', x))}">${esc(x)}</span>`; }).join('');
    if (k === 'tags') return arr.map(x => `<button type="button" class="chip" data-tag="${esc(x)}">#${esc(x)}</button>`).join('');
    if (k === 'status') return `<span class="pill ${esc(n.status)}">${esc(String(v))}</span>`;
    if (Array.isArray(v)) return arr.map(x => `<span class="chip">${esc(typeof x === 'object' ? JSON.stringify(x) : x)}</span>`).join('');
    if (v && typeof v === 'object') return `<code>${esc(JSON.stringify(v))}</code>`;
    return null;
  };
  if (keys.length || isHub) {
    const rows = keys.map(k => { const h = val(k, fm[k]); return `<dt>${esc(k)}</dt>` + (h != null ? `<dd>${h}</dd>` : `<dd class="text">${esc(fm[k])}</dd>`); }).join('');
    head += `<details class="props"${matchMedia('(max-width: 900px)').matches ? '' : ' open'}><summary>${esc(t('props'))} <span class="stat">${keys.length}</span>${isHub ? ` <span class="pill hub">${esc(t('hub'))}</span>` : ''}</summary><dl>${rows}</dl></details>`;
  }
  if (n.translations && n.translations.length) {
    head += `<div class="lang-switch">${esc(t('readIn'))} ${n.translations.map(tid => { const tn = S.notes.get(tid); return `<button type="button" class="chip" data-note="${esc(tid)}" data-lang-jump="${esc(tn.language)}">${esc(langLabel(tn.language || '?'))}</button>`; }).join(' ')}</div>`;
  }
  let html;
  try { html = mdr.parse(preprocess(n.body)); } catch (e) { html = `<pre>${esc(n.body)}</pre>`; }
  if (!/^\s*<h1[\s>]/.test(html) && !/<h1[\s>]/.test(html.slice(0, 600))) html = `<h1>${esc(n.title)}</h1>` + html;
  art.innerHTML = DOMPurify.sanitize(head + html, { USE_PROFILES: { html: true } });
  // put properties after the first h1, like a document header
  const h1 = art.querySelector('h1'), props = art.querySelector('.props');
  if (h1 && props && h1.parentNode === art) { art.prepend(h1); }
  const sc = $('#note-scroll');
  if (anchor) { const el = art.querySelector('#' + CSS.escape(anchor)); if (el) { el.scrollIntoView({ block: 'start' }); el.classList.add('flash'); } else sc.scrollTop = 0; }
  else sc.scrollTop = 0;
  typesetMath(art);
  drawMermaid(art);
}

let mjWarned = false;
function typesetMath(el) {
  if (!el.querySelector('.kb-math')) return;
  const go = () => window.MathJax.typesetPromise([el]).catch(() => {});
  if (window.MathJax && window.MathJax.typesetPromise) {
    if (window.MathJax.startup && window.MathJax.startup.promise) window.MathJax.startup.promise.then(go); else go();
  } else {
    const s = document.getElementById('mathjax-script');
    const onload = () => { if (window.MathJax && window.MathJax.startup) window.MathJax.startup.promise.then(() => { if (CUR_SRC && el.isConnected) go(); }); };
    s.addEventListener('load', onload, { once: true });
    s.addEventListener('error', () => { if (!mjWarned) { mjWarned = true; toast(t('mathFail')); } }, { once: true });
  }
}
let mermaidP = null;
function isDark() { const a = document.documentElement.getAttribute('data-theme'); return a ? a === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches; }
function drawMermaid(el) {
  const boxes = [...el.querySelectorAll('.mermaid-box[data-mermaid]')];
  if (!boxes.length) return;
  if (!mermaidP) mermaidP = new Promise((res, rej) => {
    const s = document.createElement('script'); s.src = 'https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js';
    s.onload = () => { window.mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: isDark() ? 'dark' : 'neutral', fontFamily: 'IgraSans, system-ui, sans-serif' }); res(window.mermaid); };
    s.onerror = rej; document.head.appendChild(s);
  });
  mermaidP.then(async mm => {
    for (const [i, b] of boxes.entries()) {
      if (!b.isConnected) return;
      try { const { svg } = await mm.render('mmd-' + Date.now() + '-' + i, b.getAttribute('data-mermaid')); b.innerHTML = svg; }
      catch (e) { b.insertAdjacentHTML('afterbegin', `<div class="empty">${esc(t('mermaidFail'))}</div>`); }
      b.removeAttribute('data-mermaid');
      document.querySelectorAll('body > [id^="dmmd-"], body > div[id^="mmd-"]').forEach(x => x.remove());
    }
  }).catch(() => boxes.forEach(b => { b.insertAdjacentHTML('afterbegin', `<div class="empty">${esc(t('mermaidFail'))}</div>`); b.removeAttribute('data-mermaid'); }));
}

// ======================= backlinks / outgoing =======================
function renderLinks() {
  const id = S.cur; const box = $('#backlinks');
  const inL = S.vault.links.filter(l => l.target === id && l.source !== id);
  const outL = S.vault.links.filter(l => l.source === id && l.target);
  const brokenOut = S.vault.links.filter(l => l.source === id && !l.target);
  const nIn = new Set(inL.map(l => l.source)).size, nOut = new Set(outL.map(l => l.target)).size;
  $('#n-in').textContent = nIn; $('#n-out').textContent = nOut + (brokenOut.length ? ` +${brokenOut.length}` : '');
  $('#tab-in').setAttribute('aria-selected', S.linkTab === 'in'); $('#tab-out').setAttribute('aria-selected', S.linkTab === 'out');
  const list = S.linkTab === 'in' ? inL : outL;
  const keyOf = l => S.linkTab === 'in' ? l.source : l.target;
  const by = new Map();
  for (const l of list) { const k = keyOf(l); if (!by.has(k)) by.set(k, []); by.get(k).push(l); }
  const order = [...by.keys()].sort((a, b) => by.get(b).length - by.get(a).length || S.notes.get(a).title.localeCompare(S.notes.get(b).title, 'es'));
  let h = '';
  if (S.linkTab === 'in') h += `<div class="empty" style="padding-top:2px">${esc(t('backlinkCount', nIn))}</div>`;
  h += order.map(k => {
    const other = S.notes.get(k);
    const refs = by.get(k).map(l => {
      const fmT = l.type === 'prerequisite' || l.type === 'related';
      const ctx = l.context ? highlight(l.context, l.display) : `<span style="color:var(--muted)">${esc(t('fmField', l.section))}</span>`;
      const sec = l.context && l.section ? `<small>${esc(t('inSection', l.section))}</small>` : '';
      return `<div class="bk-ref"><span class="bk-type${fmT ? ' fm' : ''}" title="${esc(T[UI].typeLong[l.type])}">${esc(T[UI].type[l.type])}</span><div class="bk-ctx">${ctx}${sec}</div></div>`;
    }).join('');
    return `<div class="bk-note"><button type="button" class="bk-title" data-note="${esc(k)}">${S.hubs.has(k) ? `<span class="dia" style="--c:${groupColor(other.part)}"></span>` : `<span class="dot" style="--c:${groupColor(other.part)}"></span>`}${esc(other.title)}</button>${refs}</div>`;
  }).join('');
  if (S.linkTab === 'out' && brokenOut.length) h += brokenOut.map(l => `<div class="bk-note"><div class="q-item" style="border:0"><code>${esc(l.raw)}</code><span class="src">${esc(T[UI].typeLong[l.type])}</span></div></div>`).join('');
  if (!list.length && !(S.linkTab === 'out' && brokenOut.length)) h += `<div class="empty">${esc(t(S.linkTab === 'in' ? 'noIn' : 'noOut'))}</div>`;
  box.innerHTML = h;
}
function highlight(ctx, display) {
  if (!display) return esc(ctx);
  const plainD = display.replace(/\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/[*_`]/g, '').replace(/:[a-z0-9-]+:\s*/g, '').trim();
  const i = plainD ? ctx.indexOf(plainD) : -1;
  if (i < 0) return esc(ctx);
  return esc(ctx.slice(0, i)) + '<mark>' + esc(plainD) + '</mark>' + esc(ctx.slice(i + plainD.length));
}

// ======================= vault health =======================
function renderQuality() {
  const v = S.vault;
  const orphans = v.notes.filter(n => n.orphan);
  const broken = v.links.filter(l => !l.target);
  let h = `<div class="f-row" style="grid-template-columns:1fr;padding-top:4px"><span>${esc(t('orphans'))} · ${orphans.length}</span></div>`;
  h += orphans.length ? orphans.map(n => `<button type="button" class="q-item" data-note="${esc(n.id)}"><span class="dot" style="--c:${groupColor(n.part)}"></span>${esc(n.title)}</button>`).join('')
    : `<div class="ok-line">✓ <span>${esc(t('noOrphans'))}</span></div>`;
  h += `<div class="f-row" style="grid-template-columns:1fr;padding-top:12px"><span>${esc(t('brokenH'))} · ${broken.length}</span></div>`;
  h += broken.length ? broken.map(l => `<button type="button" class="q-item" data-note="${esc(l.source)}" title="${esc(l.reason || '')}"><code>${esc(l.raw)}</code><span class="src">← ${esc(S.notes.get(l.source).title)}</span></button>`).join('')
    : `<div class="ok-line">✓ <span>${esc(t('noBroken'))}</span></div>`;
  $('#quality').innerHTML = h;
}

// ======================= search =======================
let qTimer = null;
function runSearch() {
  const q = fold($('#q').value).trim(); S.q = $('#q').value.trim();
  if (q.length < 2) { S.matches = null; $('#q-count').textContent = ''; }
  else {
    S.matches = new Set(S.vault.notes.filter(n => visibleNote(n) && S.search.get(n.id).includes(q)).map(n => n.id));
    $('#q-count').textContent = t('matches', S.matches.size);
  }
  renderList(); styleGraph();
  if (S.q) toggleIndex(true);
}

// ======================= interactions =======================
function setPane(p) { $('#app').dataset.pane = p; document.querySelectorAll('.mtabs button').forEach(b => b.setAttribute('aria-selected', b.dataset.pane === p)); if (p === 'right') requestAnimationFrame(() => fit(false)); }
document.querySelectorAll('.mtabs button').forEach(b => b.addEventListener('click', () => setPane(b.dataset.pane)));
document.addEventListener('click', e => {
  const tagB = e.target.closest('[data-tag]');
  if (tagB) { S.f.tag = tagB.dataset.tag; $('#f-tag').value = S.f.tag; renderList(); styleGraph(); toast('#' + S.f.tag); return; }
  const a = e.target.closest('[data-note], a[data-anchor]');
  if (!a) return;
  if (a.dataset.note) {
    e.preventDefault();
    if (a.dataset.langJump && S.f.lang !== 'all' && S.f.lang !== a.dataset.langJump) { S.f.lang = a.dataset.langJump; buildFilters(); rebuildGraph(); }
    openNote(a.dataset.note, { push: true, anchor: a.dataset.anchor || '', fromList: !!a.closest('#list') });
  } else if (a.dataset.anchor != null) {
    e.preventDefault();
    const el = $('#note').querySelector('#' + CSS.escape(a.dataset.anchor)); if (el) { el.scrollIntoView({ block: 'start', behavior: reduced ? 'auto' : 'smooth' }); el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash'); }
  }
});
$('#nav-back').addEventListener('click', () => { if (S.hpos > 0) { S.hpos--; openNote(S.hist[S.hpos], { push: false }); } });
$('#nav-fwd').addEventListener('click', () => { if (S.hpos < S.hist.length - 1) { S.hpos++; openNote(S.hist[S.hpos], { push: false }); } });
$('#q').addEventListener('input', () => { clearTimeout(qTimer); qTimer = setTimeout(runSearch, 120); });
$('#q').addEventListener('keydown', e => {
  if (e.key === 'Enter' && S.matches && S.matches.size) { const first = [...S.matches][0]; openNote(first, { push: true, fromList: true }); }
  if (e.key === 'Escape') { $('#q').value = ''; runSearch(); }
});
document.addEventListener('keydown', e => {
  if ((e.key === '/' || (e.key === 'k' && (e.metaKey || e.ctrlKey))) && document.activeElement !== $('#q') && !/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName)) { e.preventDefault(); $('#q').focus(); }
  if (e.key === 'Escape' && !$('#sheet').hidden) closeSheet();
});
$('#f-types').addEventListener('click', e => {
  const b = e.target.closest('.tog'); if (!b) return;
  if (b.hasAttribute('data-hubedges')) S.f.hubEdges = !S.f.hubEdges;
  else { const k = b.dataset.type; S.f.types.has(k) ? S.f.types.delete(k) : S.f.types.add(k); }
  buildFilters(); rebuildGraph(); renderList();
});
$('#f-status').addEventListener('click', e => {
  const b = e.target.closest('.tog'); if (!b) return; const s = b.dataset.status;
  S.f.statuses.has(s) ? S.f.statuses.delete(s) : S.f.statuses.add(s);
  b.setAttribute('aria-pressed', S.f.statuses.has(s)); renderList(); styleGraph();
});
$('#f-tag').addEventListener('change', e => { S.f.tag = e.target.value; renderList(); styleGraph(); });
$('#f-lang').addEventListener('change', e => { S.f.lang = e.target.value; rebuildGraph(); renderList(); if (S.q) runSearch(); });
$('#legend').addEventListener('mouseover', e => { const b = e.target.closest('[data-group]'); if (b && focusGroup !== b.dataset.group) { focusGroup = b.dataset.group; styleGraph(); } });
$('#legend').addEventListener('mouseleave', () => { if (!pinnedGroup) { focusGroup = null; styleGraph(); } else { focusGroup = pinnedGroup; styleGraph(); } });
let pinnedGroup = null;
$('#legend').addEventListener('click', e => { const b = e.target.closest('[data-group]'); if (!b) return; pinnedGroup = pinnedGroup === b.dataset.group ? null : b.dataset.group; focusGroup = pinnedGroup; renderLegend(G.m); styleGraph(); });
function setMode(m) { S.mode = m; $('#tab-global').setAttribute('aria-selected', m === 'global'); $('#tab-local').setAttribute('aria-selected', m === 'local'); rebuildGraph(); }
$('#tab-global').addEventListener('click', () => setMode('global'));
$('#tab-local').addEventListener('click', () => setMode('local'));
$('#tab-in').addEventListener('click', () => { S.linkTab = 'in'; renderLinks(); });
$('#tab-out').addEventListener('click', () => { S.linkTab = 'out'; renderLinks(); });
$('#g-fit').addEventListener('click', () => fit(true));
$('#g-wide').addEventListener('click', () => setView(S.view === 'graph' ? 'split' : 'graph'));
svg.on('click', () => { if (pinnedGroup) { pinnedGroup = null; focusGroup = null; renderLegend(G.m); styleGraph(); } });

// ======================= interface language =======================
function updateThemeLabel() {
  $('#theme-toggle').textContent = UI === 'es' ? (isDark() ? 'Claro' : 'Oscuro') : (isDark() ? 'Light' : 'Dark');
}
const savedTheme = store.get('kb-theme');
if (['light', 'dark'].includes(savedTheme)) document.documentElement.dataset.theme = savedTheme;
$('#theme-toggle').addEventListener('click', () => {
  const theme = isDark() ? 'light' : 'dark';
  document.documentElement.dataset.theme = theme; store.set('kb-theme', theme); updateThemeLabel();
  if (S.vault) rebuildGraph();
});
function applyUI() {
  updateThemeLabel();
  document.documentElement.lang = UI;
  if (S.cur) renderPreview();
  document.querySelectorAll('[data-i18n]').forEach(el => { const v = T[UI][el.dataset.i18n]; if (typeof v === 'string') el.textContent = v; });
  document.querySelectorAll('[data-i18n-ph]').forEach(el => el.placeholder = T[UI][el.dataset.i18nPh]);
  document.querySelectorAll('[data-i18n-title]').forEach(el => { el.title = T[UI][el.dataset.i18nTitle]; el.setAttribute('aria-label', el.title); });
  $('#ui-lang').textContent = UI === 'es' ? 'EN' : 'ES';
  $('#ui-lang').title = UI === 'es' ? 'Switch interface to English' : 'Cambiar la interfaz a español';
  $('#rules').innerHTML = T[UI].rules.map(r => `<li>${r}</li>`).join('');
  $('#graph').setAttribute('aria-label', UI === 'es' ? 'Grafo de notas' : 'Note graph');
  if (S.vault) { renderMeta(); buildFilters(); renderList(); renderLegend(G.m); renderLinks(); renderQuality(); const n = S.notes.get(S.cur); if (n) { renderNote(n); } $('#g-count').textContent = t('showing', G.nodes.length, G.edges.length); $('#g-hint').textContent = S.mode === 'local' && n ? t('hintLocal', short(n.title, 40)) : t('hintGlobal'); }
}
$('#ui-lang').addEventListener('click', () => { UI = UI === 'es' ? 'en' : 'es'; store.set('kb-ui', UI); applyUI(); });

// ======================= open your own folder =======================
const toastEl = $('#toast'); let toastT = null;
function toast(msg, ms = 3200) { toastEl.textContent = msg; toastEl.hidden = false; clearTimeout(toastT); toastT = setTimeout(() => toastEl.hidden = true, ms); }
function openSheet() { $('#sheet').hidden = false; $('#pick-dir-btn').focus(); }
function closeSheet() { $('#sheet').hidden = true; $('#open-folder').focus(); }
$('#open-folder').addEventListener('click', openSheet);
$('#sheet-close').addEventListener('click', closeSheet);
$('#sheet').addEventListener('click', e => { if (e.target === $('#sheet')) closeSheet(); });
$('#back-sample').addEventListener('click', () => { closeSheet(); loadSample(); });
const dirSupported = 'webkitdirectory' in document.createElement('input');
$('#pick-dir-btn').addEventListener('click', () => { if (!dirSupported) { toast(t('noDir'), 5000); return; } $('#pick-dir').click(); });
$('#pick-files-btn').addEventListener('click', () => $('#pick-files').click());
$('#pick-dir').addEventListener('change', e => { ingest([...e.target.files].map(f => ({ file: f, path: f.webkitRelativePath || f.name })), true); e.target.value = ''; });
$('#pick-files').addEventListener('change', e => { ingest([...e.target.files].map(f => ({ file: f, path: f.name })), false); e.target.value = ''; });

const IMG = /\.(svg|png|jpe?g|gif|webp|avif)$/i;
const SKIP = /(^|\/)(\.[^/]*|node_modules|__pycache__|site|_site)(\/|$)/;
async function ingest(entries, fromDir) {
  // drop the picked folder's own name so paths are relative to the vault root
  let root = '';
  if (fromDir) {
    const firsts = new Set(entries.map(x => x.path.split('/')[0]));
    if (firsts.size === 1 && entries.every(x => x.path.includes('/'))) root = [...firsts][0];
  }
  const rel = x => (root ? x.path.slice(root.length + 1) : x.path).replace(/^\/+/, '');
  const keep = entries.filter(x => !SKIP.test(rel(x)));
  const md = keep.filter(x => /\.(md|markdown)$/i.test(x.path));
  if (!md.length) { toast(t('noMd'), 5000); return; }
  toast(t('reading', md.length), 10000);
  const files = await Promise.all(md.map(async x => ({ path: rel(x).replace(/\.markdown$/i, '.md'), text: await x.file.text() })));
  const assets = new Map(); const urls = [];
  for (const x of keep.filter(x => IMG.test(x.path))) { let u = null; assets.set(rel(x), () => { if (!u) { u = URL.createObjectURL(x.file); urls.push(u); } return u; }); }
  const name = root || (fromDir ? t('yours') : t('yours'));
  closeSheet();
  S.filesMode = !fromDir;
  loadVault(files, assets, { source: 'user', name, hubs: null, objectUrls: urls });
  S.objectUrls = urls;
  toast(t('loaded', S.vault.stats.notes, S.vault.stats.linksResolved), 4200);
  if (S.filesMode) setTimeout(() => toast(t('filesMode'), 7000), 4300);
}
// drag & drop a folder anywhere
let dragDepth = 0;
window.addEventListener('dragenter', e => { if ([...(e.dataTransfer?.types || [])].includes('Files')) { dragDepth++; $('#dropzone').hidden = false; } });
window.addEventListener('dragleave', () => { dragDepth = Math.max(0, dragDepth - 1); if (!dragDepth) $('#dropzone').hidden = true; });
window.addEventListener('dragover', e => e.preventDefault());
window.addEventListener('drop', async e => {
  e.preventDefault(); dragDepth = 0; $('#dropzone').hidden = true;
  const items = [...(e.dataTransfer?.items || [])].map(i => i.webkitGetAsEntry && i.webkitGetAsEntry()).filter(Boolean);
  if (!items.length) return;
  const out = [];
  const walk = (entry, prefix) => new Promise(res => {
    if (entry.isFile) entry.file(f => { out.push({ file: f, path: prefix + f.name }); res(); }, () => res());
    else if (entry.isDirectory) {
      const reader = entry.createReader(); const all = [];
      const readAll = () => reader.readEntries(async batch => { if (batch.length) { all.push(...batch); readAll(); } else { for (const c of all) await walk(c, prefix + entry.name + '/'); res(); } }, () => res());
      readAll();
    } else res();
  });
  for (const it of items) await walk(it, '');
  ingest(out, items.length === 1 && items[0].isDirectory);
});

// ======================= focused research workspace =======================
function setView(view) {
  if (!['graph','split','read'].includes(view)) view = 'graph';
  if (view === 'split' && matchMedia('(max-width: 900px)').matches) view = 'read';
  S.view = view; $('#app').dataset.view = view; $('#app').classList.remove('wide');
  document.querySelectorAll('.view-switch button').forEach(b => b.setAttribute('aria-pressed', b.dataset.view === view));
  syncUrl(); requestAnimationFrame(() => fit(false));
}
function syncUrl() {
  if (!S.vault) return;
  const url = new URL(location.href);
  if (S.source === 'sample' && S.cur) url.searchParams.set('note', S.cur); else url.searchParams.delete('note');
  url.searchParams.set('view', S.view);
  history.replaceState(null, '', url);
}
function toggleIndex(open) {
  $('#app').classList.toggle('index-open', open);
  $('#index-toggle').setAttribute('aria-expanded', String(open));
}
function showPanel(id) {
  const panel = $(id), open = !panel.classList.contains('panel-open');
  document.querySelectorAll('.panel-open').forEach(p => p.classList.remove('panel-open'));
  panel.classList.toggle('panel-open', open);
  $('#quality-toggle').setAttribute('aria-expanded', String(id === '#quality-panel' && open));
}
function renderPreview() {
  const n = S.notes.get(S.cur); if (!n) return;
  const incoming = new Set(S.vault.links.filter(l => l.target === n.id && l.source !== n.id).map(l => l.source)).size;
  const outgoing = new Set(S.vault.links.filter(l => l.source === n.id && l.target && l.target !== n.id).map(l => l.target)).size;
  $('#preview').hidden = false;
  $('#preview').innerHTML = `<button class="icon-btn preview-close" id="preview-close" aria-label="${esc(t('close'))}">×</button><div class="eyebrow">${esc(groupLabel(n.part))}</div><h2>${esc(n.title)}</h2><p>${esc(n.frontmatter.description || '')}</p><div class="stat">${incoming} ${esc(t('incoming'))} · ${outgoing} ${esc(t('outgoing'))}</div><div class="preview-actions"><button class="btn btn-primary" id="preview-read">${esc(t('read'))}</button><button class="btn" id="preview-links">${esc(t('connections'))}</button><button class="btn" id="preview-local">${esc(t('neighbours'))}</button></div>`;
  $('#preview-close').onclick = () => { $('#preview').hidden = true; };
  $('#preview-read').onclick = () => setView('split');
  $('#preview-links').onclick = () => showPanel('#links-panel');
  $('#preview-local').onclick = () => { setMode('local'); $('#preview').hidden = true; };
}
document.querySelectorAll('.view-switch button').forEach(b => b.onclick = () => setView(b.dataset.view));
$('#note-index').onclick = () => toggleIndex(!$('#app').classList.contains('index-open'));
$('#note-links').onclick = () => { setView('graph'); showPanel('#links-panel'); };
$('#index-toggle').onclick = () => toggleIndex(!$('#app').classList.contains('index-open'));
$('#index-close').onclick = () => { toggleIndex(false); $('#index-toggle').focus(); };
$('#filters-toggle').onclick = () => { $('#filters').open = !$('#filters').open; };
$('#filters').addEventListener('toggle', () => $('#filters-toggle').setAttribute('aria-expanded', String($('#filters').open)));
$('#quality-toggle').onclick = () => showPanel('#quality-panel');
document.querySelectorAll('[data-close-panel]').forEach(b => b.onclick = () => { b.closest('section').classList.remove('panel-open'); $('#quality-toggle').setAttribute('aria-expanded','false'); });
$('#zoom-in').onclick = () => svg.call(zoom.scaleBy, 1.3);
$('#zoom-out').onclick = () => svg.call(zoom.scaleBy, 1 / 1.3);
$('#copy-link').onclick = async () => {
  if (S.source !== 'sample') return toast(t('localOnly'));
  try { await navigator.clipboard.writeText(location.href); toast(t('copied')); } catch (_) { toast(t('copyFail')); }
};
$('#reset-filters').onclick = () => {
  S.f.types = new Set(TYPES); S.f.hubEdges = true; S.f.tag = ''; S.f.lang = 'all';
  S.f.statuses = new Set(S.vault.notes.map(n => n.status)); S.q = ''; S.matches = null; $('#q').value = ''; $('#q-count').textContent = '';
  pinnedGroup = null; focusGroup = null; buildFilters(); rebuildGraph(); renderList();
};
document.addEventListener('keydown', e => {
  if (/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName) || document.activeElement.isContentEditable || e.ctrlKey || e.metaKey || e.altKey || !$('#sheet').hidden) return;
  const view = {g:'graph',d:'split',l:'read'}[e.key.toLowerCase()];
  if (view) { e.preventDefault(); setView(view); }
  if (e.key === 'Escape') { toggleIndex(false); $('#filters').open = false; document.querySelectorAll('.panel-open').forEach(p => p.classList.remove('panel-open')); $('#quality-toggle').setAttribute('aria-expanded','false'); $('#preview').hidden = true; }
});

// ======================= boot =======================
// The sample vault is either embedded in the page (artifact build) or published next to it as vault.json (site build)
let sampleData = null;
async function loadSample() {
  if (!sampleData) {
    const el = document.getElementById('sample-vault'); const txt = el ? el.textContent.trim() : '';
    if (txt) sampleData = JSON.parse(txt);
    else {
      $('#note').innerHTML = `<p class="empty">${esc(t('loadingVault'))}</p>`;
      try { const r = await fetch('vault.json', { cache: 'no-cache' }); if (!r.ok) throw new Error(r.status); sampleData = await r.json(); }
      catch (e) { $('#note').innerHTML = `<h1>${esc(t('appName'))}</h1><p>${esc(t('vaultFail'))}</p>`; return; }
    }
  }
  S.filesMode = false;
  loadVault(sampleData.files, new Map(Object.entries(sampleData.assets)), sampleData.meta);
}
applyUI();
loadSample();
setView(new URL(location.href).searchParams.get('view') || 'graph');
})();

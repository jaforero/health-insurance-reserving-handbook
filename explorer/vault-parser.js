/* vault-parser.js — deterministic parser for a folder of Markdown notes.
 * Same file runs in Node (Stage 1 report) and in the browser (explorer + "Open your own folder"),
 * so both use identical rules. No inference: every node and edge comes from text in the files.
 *
 * Input:  files = [{ path: "part-01/x.md", text: "..." }]  (paths relative to the vault root, POSIX)
 *         yamlLoad = function(string) -> object             (js-yaml in both environments)
 * Output: { notes, links, assets, stats }
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.VaultParser = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // ---------- path helpers ----------
  function normalize(p) {
    const out = [];
    for (const seg of p.split('/')) {
      if (seg === '' || seg === '.') continue;
      if (seg === '..') { if (!out.length) return null; out.pop(); } // escapes the vault root
      else out.push(seg);
    }
    return out.join('/');
  }
  const dirname = p => (p.includes('/') ? p.slice(0, p.lastIndexOf('/')) : '');
  const basename = p => p.slice(p.lastIndexOf('/') + 1);
  const stripMd = p => p.replace(/\.md$/i, '');
  const isExternal = t => /^[a-z][a-z0-9+.-]*:/i.test(t) || t.startsWith('//');

  // ---------- masking: blank out code so links inside code are never counted ----------
  function maskCode(s) {
    const blank = m => m.replace(/[^\n]/g, ' ');
    // fenced blocks, line by line: a fence closes on the same char repeated at least as many times
    const lines = s.split('\n'); let fence = null;
    for (let i = 0; i < lines.length; i++) {
      const fm = lines[i].match(/^\s*(`{3,}|~{3,})/);
      if (!fence && fm) { fence = fm[1]; lines[i] = blank(lines[i]); continue; }
      if (fence) {
        const close = lines[i].match(/^\s*(`{3,}|~{3,})\s*$/);
        if (close && close[1][0] === fence[0] && close[1].length >= fence.length) fence = null;
        lines[i] = blank(lines[i]);
      }
    }
    s = lines.join('\n');
    s = s.replace(/<!--[\s\S]*?-->/g, blank);                                                  // html comments
    s = s.replace(/(`+)(?!`)[\s\S]*?[^`]\1(?!`)/g, blank);                                       // inline code
    return s;
  }

  // ---------- frontmatter ----------
  function splitFrontmatter(text, yamlLoad) {
    const t = text.replace(/^﻿/, '');
    const m = t.match(/^---\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|$)/);
    if (!m) return { fm: {}, body: t, bodyOffset: 0, fmError: null };
    let fm = {}, fmError = null;
    try { fm = yamlLoad(m[1]) || {}; if (typeof fm !== 'object') fm = {}; }
    catch (e) { fmError = String(e.message || e).split('\n')[0]; }
    return { fm, body: t.slice(m[0].length), bodyOffset: m[0].length, fmError };
  }
  const asList = v => (v == null ? [] : Array.isArray(v) ? v : [v]).map(x => String(x).trim()).filter(Boolean);

  // ---------- sentence containing a match ----------
  // A new block starts at any line that opens a list item, heading, quote, table row,
  // admonition (!!! / ???), HTML tag or comment — so context never spans structural markup.
  const BLOCK_START = /^\s*(?:[-*+]\s|\d+[.)]\s|#{1,6}\s|>|\||!!!|\?\?\?|<)/;
  const SELF_CONTAINED = /^\s*(?:!!!|\?\?\?|<|#{1,6}\s)/;
  function sentenceAt(body, start, end) {
    const lines = body.split('\n'), offs = []; let o = 0;
    for (const l of lines) { offs.push(o); o += l.length + 1; }
    let i0 = 0; while (i0 + 1 < lines.length && offs[i0 + 1] <= start) i0++;
    let i1 = i0; while (i1 + 1 < lines.length && offs[i1 + 1] < end) i1++;
    let a = i0; // walk up: stop at a blank line or when this line itself opens a block
    // (a self-contained header line — admonition, HTML, heading — is never pulled into the block)
    while (a > 0 && !BLOCK_START.test(lines[a]) && lines[a - 1].trim() && !SELF_CONTAINED.test(lines[a - 1])) a--;
    let b = i1; // walk down: stop before a blank line or a line that opens a new block
    while (b + 1 < lines.length && lines[b + 1].trim() && !BLOCK_START.test(lines[b + 1])) b++;
    const ls = offs[a], le = offs[b] + lines[b].length;
    const block = body.slice(ls, le); const rel = start - ls; const mlen = end - start;
    if (/^\s*\|/.test(block)) return block.slice(block.lastIndexOf('\n', rel) + 1).split('\n')[0]; // table: the row
    const bRe = /[.!?](?=\s+[\p{Lu}¿¡])/gu;                    // sentence ends: . ! ? before a capital
    let sStart = 0, m; const before = block.slice(0, rel);
    while ((m = bRe.exec(before))) sStart = m.index + 1;
    const aIdx = block.slice(rel + mlen).search(/[.!?](?=\s|$)/);
    const sEnd = aIdx < 0 ? block.length : rel + mlen + aIdx + 1;
    return block.slice(sStart, sEnd);
  }
  // nearest heading above a position (searched in the code-masked body, so '#' comments in code don't count)
  function sectionAt(masked, pos) {
    const re = /^#{1,6}\s+(.+?)\s*#*\s*$/gm; let m, last = null;
    while ((m = re.exec(masked)) && m.index < pos) last = m[1];
    return last ? plain(last) : null;
  }
  // Markdown -> plain text for display (link text kept, syntax dropped)
  function plain(s) {
    return String(s)
      .replace(/<!--[\s\S]*?-->/g, ' ')
      .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ')
      .replace(/\[\[([^\]|#]*)(?:#[^\]|]*)?\|([^\]]*)\]\]/g, '$2')
      .replace(/\[\[([^\]|#]*)(?:#([^\]|]*))?\]\]/g, (_, a, h) => (a || h || '').trim())
      .replace(/\[((?:[^\[\]]|\[[^\]]*\])*)\]\([^)]*\)(\{[^}]*\})?/g, '$1')
      .replace(/:[a-z0-9-]+(?:-[a-z0-9]+)*:\s*/g, '')            // :material-icon: shortcodes
      .replace(/^\s*(?:[-*+]\s+(?:\[[ xX]\]\s+)?|\d+[.)]\s+|#{1,6}\s+|>\s*|\|)/gm, '')
      .replace(/\s*\|\s*/g, ' · ')
      .replace(/<[^>]+>/g, ' ')
      .replace(/(\*\*|__|\*|_|`)(?=\S)([^*_`]+?)\1/g, '$2')
      .replace(/\s+/g, ' ').trim();
  }
  function clip(s, max) {
    if (s.length <= max) return s;
    return s.slice(0, max - 1).replace(/\s+\S*$/, '') + '…';
  }

  // ---------- part normalization (display/colour only; the raw value is kept as partRaw) ----------
  // slugify the frontmatter value; if the note's folder name ends with that slug, use the folder name
  // ("02-classical-reserving" in folder "part-02-classical-reserving" -> the folder). No value -> folder.
  const slug = v => String(v).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim()
    .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  function normPart(v, path) {
    const folder = dirname(path).split('/')[0] || '';
    if (v == null || !String(v).trim()) return folder || '(root)';
    const s = slug(v);
    if (folder && (folder === s || folder.endsWith('-' + s))) return folder;
    return s;
  }

  const LANG_LINE = /^\s*(?:\*\*|__)?\s*(?:idioma|language|lang|lengua|langue|sprache)\s*:/i;

  // ---------- main ----------
  function parseVault(files, yamlLoad, opts) {
    opts = opts || {};
    const mdFiles = files.filter(f => /\.md$/i.test(f.path)).sort((a, b) => a.path.localeCompare(b.path));
    const byPath = new Map(mdFiles.map(f => [f.path, f]));
    const byStem = new Map(); // for wikilink name matching (Obsidian "shortest path")
    for (const f of mdFiles) {
      const k = stripMd(basename(f.path)).toLowerCase();
      byStem.set(k, (byStem.get(k) || []).concat(f.path));
    }

    function candidates(target) {
      // a target names a note if it ends in .md, or has no extension (wikilinks, extensionless links)
      if (/\.md$/i.test(target)) return [target];
      if (!/\.[a-z0-9]{1,6}$/i.test(basename(target))) return [target + '.md', target.replace(/\/?$/, '/') + 'index.md'];
      return null; // an asset (svg, csv, py...) — not a note
    }

    // Rule: 1) relative to the note, 2) relative to the vault root -> "root-relative", 3) "broken".
    // Wikilinks only: 2b) unique file-name match anywhere -> "name-match" (Obsidian's own behaviour).
    function resolve(src, rawTarget, kind) {
      const target = rawTarget.startsWith('/') ? rawTarget.slice(1) : rawTarget;
      const cands = candidates(target);
      if (!cands) return { status: 'asset' };
      if (!rawTarget.startsWith('/')) {
        for (const c of cands) { const p = normalize(dirname(src) + '/' + c); if (p && byPath.has(p)) return { status: 'relative', to: p }; }
      }
      for (const c of cands) { const p = normalize(c); if (p && byPath.has(p)) return { status: 'root-relative', to: p }; }
      if (kind === 'wikilink') {
        const hits = byStem.get(stripMd(basename(target)).toLowerCase()) || [];
        if (hits.length === 1) return { status: 'name-match', to: hits[0] };
        if (hits.length > 1) return { status: 'broken', reason: 'ambiguous name (' + hits.length + ' files)' };
      }
      return { status: 'broken', reason: 'no such note' };
    }

    const notes = [], links = [], assets = [], fmErrors = [];
    // destination is either <anything but > or newline> or a run without spaces/parens
    const mdLinkRe = /(!?)\[((?:[^\[\]\n]|\[[^\[\]\n]*\])*)\]\(\s*(?:<([^>\n]*)>|([^)\s]*))(?:\s+(?:"[^"]*"|'[^']*'))?\s*\)/g;
    const wikiRe = /(!?)\[\[([^\[\]|#\n]*)(#[^\[\]|\n]*)?(?:\|([^\[\]\n]*))?\]\]/g;

    for (const f of mdFiles) {
      const { fm, body, fmError } = splitFrontmatter(f.text, yamlLoad);
      if (fmError) fmErrors.push({ path: f.path, error: fmError });
      const h1 = (body.match(/^#\s+(.+?)\s*#*\s*$/m) || [])[1];
      const note = {
        id: f.path,
        title: String(fm.title || h1 || stripMd(basename(f.path))),
        partRaw: fm.part != null ? String(fm.part) : null,
        part: normPart(fm.part, f.path),
        chapter: fm.chapter != null ? String(fm.chapter) : '',
        statusRaw: fm.status != null ? String(fm.status) : null,
        status: fm.status != null ? String(fm.status).trim().toLowerCase() : '',
        tags: asList(fm.tags),
        language: fm.language != null ? String(fm.language).trim().toLowerCase() : '',
        frontmatter: fm,
        body
      };
      notes.push(note);

      const masked = maskCode(body);
      const push = (type, raw, m, display, heading) => {
        const r = resolve(f.path, raw, type);
        // A body link on a language-switch line ("**Idioma:** Español · [English](x.md)") is a translation
        // pair, not a knowledge relation: it gets its own type so it can be shown or hidden separately.
        if (m) {
          const ls = body.lastIndexOf('\n', m.index) + 1, le = body.indexOf('\n', m.index);
          if (LANG_LINE.test(body.slice(ls, le < 0 ? undefined : le))) type = 'translation';
        }
        if (r.status === 'asset') return;
        if (r.to === f.path) return; // self-link (same-page anchor)
        links.push({
          source: f.path, target: r.to || null, raw, type, resolution: r.status, reason: r.reason || null,
          heading: heading || null, display: display || null,
          section: m ? sectionAt(masked, m.index) : (type === 'prerequisite' ? 'prerequisites' : 'related_chapters'),
          context: m ? clip(plain(sentenceAt(body, m.index, m.index + m[0].length)), 280) : null
        });
      };

      let m;
      mdLinkRe.lastIndex = 0;
      while ((m = mdLinkRe.exec(masked))) {
        let raw = m[3] != null ? m[3] : m[4]; if (!raw) continue;
        try { raw = decodeURI(raw); } catch (e) {}
        const isImg = m[1] === '!';
        const path = raw.split(/[?#]/)[0];
        const heading = raw.includes('#') ? raw.slice(raw.indexOf('#') + 1) : null;
        if (isExternal(raw) || !path) continue;
        if (isImg) { assets.push({ source: f.path, raw: path, alt: m[2] }); continue; }
        push('markdown', path, m, body.slice(m.index + 1, m.index + 1 + m[2].length), heading);
      }
      wikiRe.lastIndex = 0;
      while ((m = wikiRe.exec(masked))) {
        const raw = m[2].trim(); if (!raw) continue;
        if (m[1] === '!' && /\.[a-z0-9]{1,6}$/i.test(raw) && !/\.md$/i.test(raw)) { assets.push({ source: f.path, raw, alt: m[4] || '' }); continue; }
        push('wikilink', raw, m, m[4] || null, m[3] ? m[3].slice(1) : null);
      }
      for (const [field, type] of [['prerequisites', 'prerequisite'], ['related_chapters', 'related']]) {
        for (const raw of asList(fm[field])) push(type, raw.split('#')[0], null, null, null);
      }
    }

    // ---------- resolve image assets (relative, then root-relative) ----------
    const fileSet = new Set(files.map(x => x.path));
    for (const a of assets) {
      const rel = a.raw.startsWith('/') ? null : normalize(dirname(a.source) + '/' + a.raw);
      const rootP = normalize(a.raw.replace(/^\//, ''));
      if (rel && fileSet.has(rel)) { a.resolved = rel; a.resolution = 'relative'; }
      else if (rootP && fileSet.has(rootP)) { a.resolved = rootP; a.resolution = 'root-relative'; }
      else {
        const hits = a.raw.includes('/') ? [] : files.filter(x => basename(x.path).toLowerCase() === a.raw.toLowerCase());
        if (hits.length === 1) { a.resolved = hits[0].path; a.resolution = 'name-match'; }
        else { a.resolved = null; a.resolution = 'broken'; }
      }
    }

    // ---------- degree stats ----------
    const ok = links.filter(l => l.target);
    const inN = new Map(), outN = new Map(), inSrc = new Map();
    for (const l of ok) {
      outN.set(l.source, (outN.get(l.source) || 0) + 1);
      inN.set(l.target, (inN.get(l.target) || 0) + 1);
      if (!inSrc.has(l.target)) inSrc.set(l.target, new Set());
      inSrc.get(l.target).add(l.source);
    }
    for (const l of ok.filter(l => l.type === 'translation')) {
      const n = notes.find(x => x.id === l.source); (n.translations = n.translations || []).push(l.target);
    }
    for (const n of notes) {
      n.translations = [...new Set(n.translations || [])];
      n.outLinks = outN.get(n.id) || 0;
      n.inLinks = inN.get(n.id) || 0;
      n.backlinkNotes = inSrc.has(n.id) ? inSrc.get(n.id).size : 0;
      n.orphan = n.outLinks === 0 && n.inLinks === 0;
    }
    const count = (arr, key) => arr.reduce((o, x) => (o[x[key]] = (o[x[key]] || 0) + 1, o), {});
    const stats = {
      notes: notes.length,
      linksResolved: ok.length,
      linksBroken: links.length - ok.length,
      byType: count(ok, 'type'),
      byResolution: count(links, 'resolution'),
      uniqueEdges: new Set(ok.map(l => l.source + '→' + l.target)).size,
      orphans: notes.filter(n => n.orphan).map(n => n.id),
      images: assets.length,
      imagesBroken: assets.filter(a => a.resolution === 'broken').length,
      frontmatterErrors: fmErrors
    };
    // resolver for the renderer: same rules as the link scan
    function resolveAsset(src, raw) {
      const rel = raw.startsWith('/') ? null : normalize(dirname(src) + '/' + raw);
      const rootP = normalize(raw.replace(/^\//, ''));
      if (rel && fileSet.has(rel)) return rel;
      if (rootP && fileSet.has(rootP)) return rootP;
      if (!raw.includes('/')) { // Obsidian-style ![[pic.png]]: unique file name anywhere
        const hits = files.filter(x => basename(x.path).toLowerCase() === raw.toLowerCase());
        if (hits.length === 1) return hits[0].path;
      }
      return null;
    }
    return { notes, links, assets, stats, resolve, resolveAsset };
  }

  return { parseVault, normalize, maskCode, sentenceAt, plain, normPart };
});

// Shared by Node indexing/evaluation and the browser worker. No network calls.
export function tokens(text) {
  return (text.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase().match(/[\p{L}\p{N}]+/gu) || [])
    .filter(t => t.length > 1 && !STOP.has(t));
}
const STOP = new Set('de la el los las un una unos unas en y o a que qué como cómo cual cuál para por con del al se es son su sus lo the a an of to in and or is are how what do does on for'.split(' '));
export function lexical(chunks) {
  const postings = {}, lengths = [];
  chunks.forEach((c, id) => {
    const ts = tokens(c.heading + ' ' + c.text), tf = new Map();
    lengths.push(ts.length);
    for (const t of ts) tf.set(t, (tf.get(t) || 0) + 1);
    for (const [t, n] of tf) (postings[t] ||= []).push([id, n]);
  });
  return {postings, lengths, average: lengths.reduce((a,b)=>a+b,0)/lengths.length};
}
export function bm25(query, index, k1=1.2, b=0.75) {
  const scores = new Float64Array(index.lengths.length), N=scores.length;
  for (const t of new Set(tokens(query))) {
    const p = index.postings[t] || [], idf = Math.log(1+(N-p.length+0.5)/(p.length+0.5));
    for (const [i, tf] of p) scores[i] += idf*tf*(k1+1)/(tf+k1*(1-b+b*index.lengths[i]/index.average));
  }
  return Array.from(scores, (score,id)=>({id,score})).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.id-b.id);
}
export function semantic(query, vectors, dimensions) {
  const result=[];
  for(let id=0;id<vectors.length/dimensions;id++) {
    let score=0; for(let j=0;j<dimensions;j++) score+=query[j]*vectors[id*dimensions+j];
    result.push({id,score});
  }
  return result.sort((a,b)=>b.score-a.score||a.id-b.id);
}
export function fuse(lex, sem, config) {
  const scores=new Map();
  for(const [ranking,weight] of [[lex,config.lexicalWeight],[sem,config.semanticWeight]])
    ranking.slice(0,config.candidates).forEach((x,i)=>scores.set(x.id,(scores.get(x.id)||0)+weight/(config.rrfK+i+1)));
  return [...scores].map(([id,score])=>({id,score})).sort((a,b)=>b.score-a.score||a.id-b.id);
}
export function scopeReason(q) {
  const s=tokens(q).join(' ');
  if (/contraseña|contrasena|password|ultimo partido|futbol/.test(s)) return 'outside-corpus';
  if (/exact[oa]|mi eps|mi organizacion|empresa privada|a esta hora/.test(s) && /ibnr|reserva|saldo|importe/.test(s)) return 'private-data-required';
  if (/tasa cambio|usd cop/.test(s) && /actual|hoy/.test(s)) return 'live-data-required';
  return null;
}
export function accepted(q, sem, threshold) { return !scopeReason(q) && (sem[0]?.score ?? -1)>=threshold; }
export function citation(chunk, manifest) {
  return `https://github.com/${manifest.repository}/blob/${manifest.commit}/${chunk.path.split('/').map(encodeURIComponent).join('/')}#L${chunk.start}-L${chunk.end}`;
}

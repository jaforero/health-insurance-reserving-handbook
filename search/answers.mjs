import {scopeReason} from './core.mjs';
export const normalizeQuestion=q=>q.normalize('NFD').replace(/\p{M}/gu,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
export function answerFor(query, catalog) {
 const q=normalizeQuestion(query);
 if(scopeReason(query))return {kind:'insufficient'};
 const exact=catalog.answers.filter(a=>[a.question,...a.variants].some(x=>normalizeQuestion(x)===q));
 if(exact.length===1)return {kind:'answer',answer:exact[0]};
 // No generic explanation may masquerade as a calculation or specialized implementation.
 if(/\d|calcula|cuanto|codigo|python|excel|sql|geometr|trigonometr|mi cartera|mi empresa|mi entidad|paso a paso en/.test(q))return {kind:'uncovered'};
 const ids=[];
 const contrast=/diferenc|compar| versus | vs |son (lo mismo|iguales)/.test(q);
 if(/\bibnr\b/.test(q)&&/\bibner\b/.test(q))ids.push('ibnr-ibner');
 else if(/\bibnr\b/.test(q)&&/que es|que significa|explica|defin|concepto/.test(q))ids.push('ibnr');
 if(/pagad/.test(q)&&/incurrid/.test(q)&&contrast)ids.push('paid-incurred');
 if(/incremental/.test(q)&&/acumulad/.test(q)&&contrast)ids.push('incremental-cumulative');
 if(/triangul/.test(q)&&!/pagad|incurrid|incremental|acumulad|mack|bootstrap/.test(q)) {
  if(/constru|armar|crear|pasos/.test(q))ids.push('build-triangle');
  else if(/como funciona|que es|que son|como se (lee|leen|interpreta)|explica|para que sirve/.test(q))ids.push('triangles');
 }
 if(/ultimate|costo ultimo/.test(q)&&/que es|significa|explica|defin/.test(q))ids.push('ultimate');
 if(/chain ladder/.test(q)&&/supuest|cuando.*(usar|utilizar|aplica|apropiado)/.test(q))ids.push('chain-ladder');
 if(/salud/.test(q)&&/metodo|metodologia/.test(q)&&/mejor|recomend|conviene|selecci|elegir/.test(q))ids.push('health-method');
 const matches=catalog.answers.filter(a=>ids.includes(a.id));
 if(matches.length>1)return {kind:'clarify',choices:matches.map(a=>({id:a.id,question:a.question}))};
 if(matches.length===1 && !/ademas|tambien| y (como|que|por que)|por que|cual es la formula/.test(q))return {kind:'answer',answer:matches[0]};
 return {kind:'uncovered'};
}

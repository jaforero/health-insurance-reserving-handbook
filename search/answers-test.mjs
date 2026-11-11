import fs from 'node:fs';
import assert from 'node:assert/strict';
import {answerFor} from './answers.mjs';
const catalog=JSON.parse(fs.readFileSync('docs/pregunta/answers.json'));
const cases=[
 ['Como funcionan los triangulos de reservas?','triangles'],['¿Cómo funcionan los triángulos de reservas?','triangles'],['Explica para que sirve un triangulo actuarial','triangles'],['Como se interpreta un triangulo de desarrollo','triangles'],
 ['Como crear un triangulo de reservas','build-triangle'],['Pasos para construir un triangulo','build-triangle'],
 ['Que diferencia hay entre IBNR e IBNER','ibnr-ibner'],['IBNR y IBNER son lo mismo','ibnr-ibner'],['Explica el concepto IBNR','ibnr'],['Que significa IBNR','ibnr'],
 ['Diferencia entre pagado e incurrido','paid-incurred'],['Comparar triangulos pagados e incurridos','paid-incurred'],
 ['Diferencia incremental acumulado','incremental-cumulative'],['Triangulos incrementales vs acumulados','incremental-cumulative'],
 ['Que significa costo ultimo','ultimate'],['Que es ultimate','ultimate'],
 ['Supuestos necesarios para utilizar Chain Ladder','chain-ladder'],['Cuando es apropiado usar Chain Ladder','chain-ladder'],
 ['Que metodo conviene para reservas de salud','health-method'],['Mejor metodologia de reservas en salud','health-method']
];
for(const [q,id] of cases)assert.equal(answerFor(q,catalog).answer?.id,id,q);
for(const q of ['Como funcionan los triangulos en geometria','Como funcionan los triangulos de reservas en Excel','Calcula mi IBNR exacto','Que es el IBNR y por que mi empresa tiene perdidas','Que metodo es mejor para inversiones','Formula de Chain Ladder','Como funcionan los triangulos de reservas y que es ultimate'])assert.notEqual(answerFor(q,catalog).kind,'answer',q);
const source=fs.readFileSync('docs/handbook-answers.md','utf8').split('\n');
for(const a of catalog.answers){for(const block of [a.answer,a.criteria])assert.equal(source.slice(block.start-1,block.end).join('\n'),block.text);assert.ok(a.answer.text.length>80);assert.ok(a.criteria.text.startsWith('- '));assert.ok(a.sources.length);assert.match(a.editorialSource.url,new RegExp('/blob/'+catalog.commit+'/'));for(const s of a.sources)assert.ok(fs.existsSync(s.path));}
const legacy=JSON.parse(fs.readFileSync('docs/assets/data/handbook-qa-catalog.json')).items;
for(const item of legacy)assert.equal(answerFor(item.question,catalog).kind,'answer',item.question);
console.log('PASS: all '+legacy.length+' previously authored questions remain supported');
console.log(`PASS: ${cases.length} affirmative acceptance questions, 7 negative/ambiguous cases, ${catalog.answers.length} source-verified answers`);

// Acceptance includes the substance of the answer and actionable criteria, not just routing.
const expected={
 'triangles':[/filas.*periodos de origen/i,/columnas.*edades de desarrollo/i,/futur.*no observado/i,/no es un método/i],
 'build-triangle':[/formato largo/i,/agrega.*origen y desarrollo/i,/matriz/i],
 'ibnr-ibner':[/no han sido reportadas/i,/ya reportadas/i,/reserva caso/i],
 'ibnr':[/incurred but not reported/i,/fecha de corte/i],
 'paid-incurred':[/desembolsos/i,/pagos y reserva caso/i,/no equivale.*costo último/i],
 'incremental-cumulative':[/cada intervalo/i,/suma.*cada edad/i,/diferencias/i],
 'ultimate':[/costo final esperado/i,/restando los pagos/i],
 'chain-ladder':[/patrones.*representativos/i,/mezcla de riesgo/i,/efectos de calendario/i],
 'health-method':[/No existe un método universalmente superior/i,/madurez/i,/prior defendible/i]
};
for(const [id,concepts] of Object.entries(expected)){const a=catalog.answers.find(x=>x.id===id);for(const concept of concepts)assert.match(a.answer.text,concept,id);assert.ok(a.criteria.text.split('\n').length>=3,id);}
assert.equal(answerFor('Como funcionan los triangulos de reservas y que es ultimate',catalog).kind,'clarify');
console.log('PASS: concrete answer content, actionable criteria and multi-intent clarification');

fs.mkdirSync('artifacts',{recursive:true});
fs.writeFileSync('artifacts/semantic-answers.json',JSON.stringify({commit:catalog.commit,answers:catalog.answers.length,affirmative:cases.length,legacyQuestions:legacy.length,negativeOrAmbiguous:7,sourceTextExact:true,criteriaAndConceptChecks:true,cases:cases.map(([query,id])=>({query,expected:id,actual:answerFor(query,catalog).answer.id})),limitation:'Acceptance regression on a bounded set of authored answers; not an estimate of general retrieval quality.'},null,2));

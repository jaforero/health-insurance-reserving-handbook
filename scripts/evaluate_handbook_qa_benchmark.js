#!/usr/bin/env node
"use strict";
// P1 evaluator: only source-reviewed questions contribute to retrieval metrics.
// Pending cases are reported but never counted as correctness ground truth.
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");
const engine = require(path.join(ROOT, "docs/assets/javascripts/handbook-qa.js"));
const dataPath = name => path.join(ROOT, "docs/assets/data", name);
function sourceId(s) { return String(s.path || "") + "#" + String(s.anchor || ""); }
function rate(n, d) { return {numerator:n, denominator:d, value:d ? n/d : null}; }
function firstRelevantRank(entries, gold) {
  const set=new Set((gold||[]).map(sourceId));
  const index=(entries||[]).findIndex(x=>set.has(sourceId(x.section||x)));
  return index>=0?index+1:null;
}
function firstDocumentRank(entries,gold) {
  const paths=new Set((gold||[]).map(x=>x.path));
  const idx=(entries||[]).findIndex(x=>paths.has((x.section||x).path));
  return idx>=0?idx+1:null;
}
function assertValidFixture(fixture, index) {
  if (!fixture || fixture.schema_version!=="1.0.0" ||
      !Array.isArray(fixture.cases) || fixture.cases.length!==65)
    throw Error("P1 fixture must have 65 cases (schema 1.0.0)");
  const indexed=new Set((index.sections||[]).map(sourceId));
  const docs=new Set((index.documents||[]).map(x=>x.path));
  const ids=new Set();
  for (const test of fixture.cases) {
    if (!/^P1-\d{2}$/.test(test.id) || ids.has(test.id)) throw Error("Duplicate or invalid id: "+test.id);
    ids.add(test.id);
    if (!test.query || !test.topic || !["en","es"].includes(test.language))
      throw Error("Invalid case fields: "+test.id);
    if (!["supported","not_answerable"].includes(test.answerability))
      throw Error("Invalid answerability: "+test.id);
    if (!["reviewed_source","reviewed_scope","pending"].includes(test.review_status))
      throw Error("Invalid review state: "+test.id);
    if (test.answerability==="supported") {
      if (!test.candidate_path || !docs.has(test.candidate_path))
        throw Error("Unknown candidate: "+test.id);
      if (test.review_status==="reviewed_source") {
        if (!test.review_basis || !test.relevant_sections?.length)
          throw Error("Missing reviewed evidence: "+test.id);
        for (const src of test.relevant_sections) {
          if (!indexed.has(sourceId(src))) throw Error("Missing indexed anchor: "+test.id+" "+sourceId(src));
          if (!src.evidence_excerpt) throw Error("Missing evidence text: "+test.id);
          const filepath=path.join(ROOT,"docs",src.path);
          const actual=fs.readFileSync(filepath,"utf8").replace(/\s+/g," ");
          const expected=src.evidence_excerpt.replace(/\s+/g," ");
          if (!actual.includes(expected)) throw Error("Excerpt absent: "+test.id+" "+sourceId(src));
        }
      } else if (test.review_status==="reviewed_scope") throw Error("Scope review invalid for supported: "+test.id);
    } else {
      if (!test.scope_rationale) throw Error("Scope rationale absent: "+test.id);
      if (test.review_status==="reviewed_source") throw Error("Source review invalid for scope: "+test.id);
      if (test.review_status==="reviewed_scope" && !test.review_basis)
        throw Error("Scope review basis absent: "+test.id);
    }
  }
  return true;
}
function errorCodes(test,result,rank,documentRank) {
  if (test.review_status==="pending") return ["reference_pending_review"];
  const errors=[];
  if (test.review_status==="reviewed_source") {
    if (rank===null) errors.push("gold_evidence_missing_at5");
    if (documentRank===null) errors.push("gold_document_missing_at5");
    if (result.status==="insufficient") errors.push("false_insufficient");
    if (result.status==="out_of_scope") errors.push("false_out_of_scope");
    if (test.expected_editorial_id && result.item?.id!==test.expected_editorial_id)
      errors.push("incorrect_editorial_answer_id");
  } else {
    if (result.item) errors.push("unsupported_editorial_answer");
    if (result.status==="corpus_match") errors.push("corpus_match_not_sufficient_for_specific_request");
  }
  return errors;
}
function evaluate(fixture,catalog,index,runtime=engine) {
  assertValidFixture(fixture,index);
  const per_question=fixture.cases.map(test=>{
    const result=runtime.search(test.query,catalog,index,{});
    // The engine already returns top-3 sections with search(). Request top-5
    // only for source-reviewed cases: avoid rescoring 2,352 sections twice for
    // every pending/unanswerable query, without changing the production motor.
    const topFive=test.review_status==="reviewed_source"
      ? runtime.findRelatedSections(test.query,index,5,{})
      : (result.relatedSections||[]);
    const ranked_sources_at5=topFive.map((x,i)=>({
      rank:i+1,path:x.section.path,anchor:x.section.anchor||"",
      title:x.section.title,score:Number(x.score.toFixed(6)),
      reference:sourceId(x.section)
    }));
    const goldRank=test.review_status==="reviewed_source"
      ? firstRelevantRank(topFive,test.relevant_sections):null;
    const documentRank=test.review_status==="reviewed_source"
      ? firstDocumentRank(topFive,test.relevant_sections):null;
    const candidateRank=test.candidate_path
      ? ranked_sources_at5.findIndex(x=>x.path===test.candidate_path)+1:0;
    return {
      id:test.id,query:test.query,topic:test.topic,language:test.language,
      answerability:test.answerability,review_status:test.review_status,
      candidate_path:test.candidate_path||null,
      gold_references:test.review_status==="reviewed_source"
        ? test.relevant_sections.map(sourceId):[],
      predicted_status:result.status,predicted_editorial_id:result.item?.id||null,
      expected_editorial_id:test.expected_editorial_id||null,
      ranking_depth:test.review_status==="reviewed_source"?5:3,
      ranked_sources_at5,first_gold_rank_at5:goldRank,
      first_gold_document_rank_at5:documentRank,
      candidate_document_rank_at5:candidateRank||null,
      errors:errorCodes(test,result,goldRank,documentRank)
    };
  });
  const gold=per_question.filter(x=>x.review_status==="reviewed_source");
  const scope=per_question.filter(x=>x.review_status==="reviewed_scope");
  const pending=per_question.filter(x=>x.review_status==="pending");
  const hits=k=>gold.filter(x=>x.first_gold_rank_at5!==null&&x.first_gold_rank_at5<=k).length;
  const docHits=k=>gold.filter(x=>x.first_gold_document_rank_at5!==null&&x.first_gold_document_rank_at5<=k).length;
  const rr=gold.reduce((n,x)=>n+(x.first_gold_rank_at5?1/x.first_gold_rank_at5:0),0);
  const docRr=gold.reduce((n,x)=>n+(x.first_gold_document_rank_at5?1/x.first_gold_document_rank_at5:0),0);
  const eids=gold.filter(x=>x.expected_editorial_id!==null);
  return {
    schema_version:"1.0.0",
    evaluation:"P1 reviewed-subset baseline, not full-corpus generalization",
    baseline_commit:fixture.baseline_commit,
    review_methodology:fixture.review_policy,
    notes:[
      "Retrieval metrics use reviewed_source only; scope metrics use reviewed_scope only.",
      "References inspected by assistant against source; no independent human adjudication.",
      "Pending cases are excluded from all metrics.",
      "A corpus_match identifies sections but is not a generated actuarial answer.",
      "Candidate document ranking is diagnostic only; never used as gold."
    ],
    counts:{questions:per_question.length,reviewed_source:gold.length,reviewed_scope:scope.length,pending:pending.length},
    metrics:{
      evidence_hit_at1:rate(hits(1),gold.length),
      evidence_hit_at3:rate(hits(3),gold.length),
      evidence_hit_at5:rate(hits(5),gold.length),
      evidence_mrr_at5:rate(rr,gold.length),
      document_hit_at1:rate(docHits(1),gold.length),
      document_hit_at3:rate(docHits(3),gold.length),
      document_hit_at5:rate(docHits(5),gold.length),
      document_mrr_at5:rate(docRr,gold.length),
      false_insufficient_on_reviewed_source:rate(gold.filter(x=>x.predicted_status==="insufficient").length,gold.length),
      no_editorial_answer_on_scope:rate(scope.filter(x=>!x.predicted_editorial_id).length,scope.length),
      corpus_match_on_unanswerable_scope:rate(scope.filter(x=>x.predicted_status==="corpus_match").length,scope.length),
      required_editorial_id_accuracy:rate(eids.filter(x=>x.predicted_editorial_id===x.expected_editorial_id).length,eids.length)
    },
    per_question
  };
}
function percent(x) {return x===null?"N/A":(x*100).toFixed(1)+"%";}
function cell(s) {return String(s===null||s===undefined?"":s).replace(/\|/g,"\\|").replace(/\r?\n/g," ");}
function toMarkdown(report) {
  const lines=[
    "# Ask the Handbook — línea base cuantitativa P1",
    "",
    "Evaluación reproducible del motor real. Datos verificados por inspección",
    "de fragmentos del Handbook, sin revisión humana independiente.",
    "Las consultas pendientes no entran en ningún denominador.",
    "",
    "## Universo y estado de revisión",
    "",
    "| Tipo | Casos |","|---|---:|",
    "| Total | "+report.counts.questions+" |",
    "| Fuente inspeccionada | "+report.counts.reviewed_source+" |",
    "| Alcance inspeccionado | "+report.counts.reviewed_scope+" |",
    "| Pendiente | "+report.counts.pending+" |",
    "",
    "## Indicadores calculados exclusivamente sobre casos inspeccionados",
    "",
    "| Indicador | Valor | Numerador / denominador |",
    "|---|---:|---:|"
  ];
  for(const [key,v] of Object.entries(report.metrics)){
    lines.push("| "+key+" | "+((key==="evidence_mrr_at5"||key==="document_mrr_at5")&&v.value!==null?v.value.toFixed(4):percent(v.value))+
      " | "+Number(v.numerator.toFixed(4))+" / "+v.denominator+" |");
  }
  lines.push("","## Evaluación por pregunta","",
    "Los resultados pendientes se marcan reference_pending_review, no como errores del motor.","",
    "| ID | Estado revisión | Estado respuesta | Rango sección gold | Rango documento gold | Fuente rango 1 | Error o límite |",
    "|---|---|---|---:|---:|---|---|");
  for(const q of report.per_question){
    const top=q.ranked_sources_at5[0];
    lines.push("| "+q.id+" | "+q.review_status+" | "+q.predicted_status+
      " | "+(q.first_gold_rank_at5||"—")+" | "+(q.first_gold_document_rank_at5||"—")+
      " | "+cell(top?top.reference:"—")+
      " | "+cell(q.errors.join(", ")||"—")+" |");
  }
  lines.push("","## Detalle completo","",
    "El JSON adjunto documenta las 65 consultas: top 5 para las 12",
    "fuentes revisadas y top 3 para las otras consultas,",
    "puntajes y referencias path#anchor, etiquetas y códigos de error.",
    "El documento candidato no se considera referencia validada.","");
  return lines.join("\n");
}
function readJSON(filename){return JSON.parse(fs.readFileSync(filename,"utf8"));}
function main(){
  const cat=readJSON(dataPath("handbook-qa-catalog.json"));
  const idx=readJSON(dataPath("handbook-section-index.json"));
  const fix=readJSON(path.join(ROOT,"tests/fixtures/handbook_qa_p1_benchmark.json"));
  const report=evaluate(fix,cat,idx);
  const pos=process.argv.indexOf("--output-dir");
  if(pos!==-1){
    const dir=process.argv[pos+1];
    if(!dir)throw Error("Missing --output-dir value");
    fs.mkdirSync(dir,{recursive:true});
    fs.writeFileSync(path.join(dir,"handbook-qa-p1-report.json"),JSON.stringify(report,null,2)+"\n");
    fs.writeFileSync(path.join(dir,"handbook-qa-p1-report.md"),toMarkdown(report));
  }
  console.log("P1 reviewed-subset quantitative baseline:");
  console.log(JSON.stringify({counts:report.counts,metrics:report.metrics},null,2));
}
if(require.main===module)main();
module.exports={sourceId,rate,firstRelevantRank,firstDocumentRank,assertValidFixture,errorCodes,evaluate,toMarkdown};

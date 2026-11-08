#!/usr/bin/env node
"use strict";
// Structural, mathematical and end-to-end regression for the P1 benchmark.
const assert=require("assert");
const fs=require("fs");
const path=require("path");
const ROOT=path.resolve(__dirname,"../..");
const evaluator=require(path.join(ROOT,"scripts/evaluate_handbook_qa_benchmark.js"));
const fixture=JSON.parse(fs.readFileSync(path.join(ROOT,"tests/fixtures/handbook_qa_p1_benchmark.json"),"utf8"));
const catalog=JSON.parse(fs.readFileSync(path.join(ROOT,"docs/assets/data/handbook-qa-catalog.json"),"utf8"));
const index=JSON.parse(fs.readFileSync(path.join(ROOT,"docs/assets/data/handbook-section-index.json"),"utf8"));

assert.strictEqual(evaluator.assertValidFixture(fixture,index),true);
assert.strictEqual(fixture.cases.length,65);
assert.strictEqual(fixture.cases.filter(x=>x.answerability==="supported").length,53);
assert.strictEqual(fixture.cases.filter(x=>x.answerability==="not_answerable").length,12);
assert.strictEqual(fixture.cases.filter(x=>x.review_status==="reviewed_source").length,12);
assert.strictEqual(fixture.cases.filter(x=>x.review_status==="reviewed_scope").length,6);
assert.strictEqual(fixture.cases.filter(x=>x.review_status==="pending").length,47);

const entries=[
  {section:{path:"a.md",anchor:"a"}},
  {section:{path:"b.md",anchor:"b"}}
];
assert.strictEqual(evaluator.firstRelevantRank(entries,[{path:"b.md",anchor:"b"}]),2);
assert.strictEqual(evaluator.firstRelevantRank(entries,[{path:"z.md",anchor:"z"}]),null);
assert.deepStrictEqual(evaluator.rate(1,2),{numerator:1,denominator:2,value:0.5});
assert.deepStrictEqual(evaluator.rate(0,0),{numerator:0,denominator:0,value:null});

const allPending={...fixture,cases:fixture.cases.map(x=>({...x,review_status:"pending"}))};
const noMatches=evaluator.evaluate(allPending,catalog,index,{
  search:()=>({status:"insufficient",item:null}),
  findRelatedSections:()=>[]
});
assert.strictEqual(noMatches.counts.pending,65);
assert.strictEqual(noMatches.metrics.evidence_hit_at5.value,null);
assert.strictEqual(noMatches.metrics.evidence_mrr_at5.value,null);
assert.strictEqual(noMatches.metrics.no_editorial_answer_on_scope.value,null);

const actual=evaluator.evaluate(fixture,catalog,index);
assert.strictEqual(actual.counts.questions,65);
assert.strictEqual(actual.counts.reviewed_source,12);
assert.strictEqual(actual.counts.reviewed_scope,6);
assert.strictEqual(actual.counts.pending,47);
assert.strictEqual(actual.per_question.length,65);
const historic=actual.per_question.find(x=>x.id==="P1-34");
assert.strictEqual(historic.predicted_status,"verified");
assert.strictEqual(historic.predicted_editorial_id,"health-reserving-method-selection");
assert.ok(historic.gold_references.length,"Required source missing");
for(const [key,val] of Object.entries(actual.metrics)){
  assert.ok(val.value===null||(Number.isFinite(val.value)&&val.value>=0&&val.value<=1),
    "Metric outside [0,1]: "+key);
}
const markdown=evaluator.toMarkdown(actual);
assert.ok(markdown.includes("P1-65") && markdown.includes("reference_pending_review"));
assert.ok(markdown.includes("P1-34"));
console.log("OK: 65 questions, 12 source-reviewed labels, 6 scope-reviewed labels, 47 unscored pending.");

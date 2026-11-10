import fs from 'node:fs/promises';
import path from 'node:path';
import {encoder} from './embedding-node.mjs';
import {bm25,semantic,fuse,scopeReason,accepted,citation} from './core.mjs';
const dir='docs/pregunta/',read=async f=>JSON.parse(await fs.readFile(dir+f,'utf8'));
const [chunks,lex,manifest]=await Promise.all(['chunks.json','lexical.json','manifest.json'].map(read));
const bytes=await fs.readFile(dir+'vectors.f32'),vectors=new Float32Array(bytes.buffer,bytes.byteOffset,bytes.byteLength/4);
const {embed}=await encoder(path.resolve(dir)+'/');
const config=JSON.parse(await fs.readFile('search/retrieval-settings.json','utf8'));
const cacheFile='.cache/semantic/queries.json';let cached;try{cached=JSON.parse(await fs.readFile(cacheFile,'utf8'));}catch{cached={};}
if(!cached||cached.signature!==manifest.signature) cached={signature:manifest.signature,queries:{}};
async function vector(q){if(!cached.queries[q])cached.queries[q]=await embed(q);return cached.queries[q];}
const calibration=JSON.parse(await fs.readFile('search/calibration.json','utf8'));
const rows=[],calibrationRankings=[];
for(const c of calibration){if(c.path){const text=await fs.readFile('docs/'+c.path,'utf8');if(!text.includes(c.evidence_substring))throw Error('Calibration source missing');}const sem=semantic(await vector(c.query),vectors,384);calibrationRankings.push({case:c,sem,lex:bm25(c.query,lex)});rows.push({...c,score:sem[0].score,lexicalScore:bm25(c.query,lex)[0]?.score||0,scope:scopeReason(c.query)});}
// Choose lexical weight using calibration documents only, never evaluation labels.
const fusionTrials=[0.25,0.5,1,2].map(weight=>{
 let mrr=0,n=0;
 for(const row of calibrationRankings) if(row.case.path) {
   n++;const ranked=fuse(row.lex,row.sem,{...config,lexicalWeight:weight});
   const rank=ranked.slice(0,5).findIndex(x=>chunks[x.id].path==='docs/'+row.case.path);
   if(rank>=0)mrr+=1/(rank+1);
 }
 return {lexicalWeight:weight,mrrAt5:mrr/n};
});
if(config.calibrateFusion) {
 fusionTrials.sort((a,b)=>b.mrrAt5-a.mrrAt5||Math.abs(a.lexicalWeight-1)-Math.abs(b.lexicalWeight-1));
 config.lexicalWeight=fusionTrials[0].lexicalWeight;
}
const values=[...new Set(rows.map(x=>x.score))].sort((a,b)=>a-b),candidates=[-1,...values.slice(1).map((x,i)=>(x+values[i])/2),1.001];
let best=null;
for(const threshold of candidates){const positive=rows.filter(x=>x.answerability==='supported'),negative=rows.filter(x=>x.answerability!=='supported');const tp=positive.filter(x=>!x.scope&&x.score>=threshold).length,tn=negative.filter(x=>x.scope||x.score<threshold).length;const balanced=(tp/positive.length+tn/negative.length)/2;if(!best||balanced>best.balanced||(balanced===best.balanced&&tn>best.tn))best={threshold,balanced,tp,tn};}
const lexicalValues=[...new Set(rows.map(x=>x.lexicalScore))].sort((a,b)=>a-b);
let lexicalBest=null;
for(const threshold of [-1,...lexicalValues.slice(1).map((x,i)=>(x+lexicalValues[i])/2),1e9]) {
 const pos=rows.filter(x=>x.answerability==='supported'),neg=rows.filter(x=>x.answerability!=='supported');
 const tp=pos.filter(x=>!x.scope&&x.lexicalScore>=threshold).length,tn=neg.filter(x=>x.scope||x.lexicalScore<threshold).length;
 const balanced=(tp/pos.length+tn/neg.length)/2;
 if(!lexicalBest||balanced>lexicalBest.balanced||(balanced===lexicalBest.balanced&&tn>lexicalBest.tn))lexicalBest={threshold,balanced,tp,tn};
}
Object.assign(config,{threshold:best.threshold,signature:manifest.signature,commit:manifest.commit,calibration:{...best,size:rows.length}});
await fs.writeFile(dir+'retrieval.json',JSON.stringify(config,null,2));
const fixture=JSON.parse(await fs.readFile('search/evaluation.json','utf8')),results=[],probes=[];
for(const c of fixture.cases){
  const start=performance.now(),q=await embed(c.query),embeddingMs=performance.now()-start;
  probes.push({text:c.query,vector:q});
  const t=performance.now(),l=bm25(c.query,lex),lexicalMs=performance.now()-t,s=semantic(q,vectors,384),h=fuse(l,s,config);
  // Resolve gold to exact source lines, then score retrieval of that evidence (not just its document).
  const gold=[];
  for(const g of c.relevant_sections||[]) {const lines=(await fs.readFile('docs/'+g.path,'utf8')).split('\n');const line=lines.findIndex(l=>l.includes(g.evidence_excerpt));if(line<0)throw Error('Gold excerpt must resolve to a source line: '+c.id);gold.push({path:'docs/'+g.path,line:line+1});}
  const metrics=ranking=>{const selected=ranking.slice(0,5).map(x=>chunks[x.id]);const hits=gold.filter(g=>selected.some(c=>c.path===g.path&&c.start<=g.line&&c.end>=g.line));return {documentRecall:gold.length?gold.filter(g=>selected.some(c=>c.path===g.path)).length/gold.length:null,recall:gold.length?hits.length/gold.length:null,top5:selected.map(c=>({path:c.path,heading:c.heading,start:c.start,end:c.end,url:citation(c,manifest)}))};};
  results.push({id:c.id,query:c.query,answerability:c.answerability,bm25:metrics(l),hybrid:metrics(h),semantic:metrics(s),bm25Abstain:!!scopeReason(c.query)||(l[0]?.score||0)<lexicalBest.threshold,abstain:!accepted(c.query,s,config.threshold),semanticScore:s[0].score,scope:scopeReason(c.query),embeddingMs,lexicalMs,hybridSearchMs:performance.now()-t});
}
await fs.writeFile(cacheFile,JSON.stringify(cached));
await fs.writeFile(dir+'evaluation-probes.json',JSON.stringify(probes));
const pos=results.filter(x=>x.answerability==='supported'),neg=results.filter(x=>x.answerability!=='supported');
const report={commit:manifest.commit,notes:fixture.notes,calibration:{...best,rows,fusionTrials},testCount:results.length,supported:pos.length,unsupported:neg.length,bm25RecallAt5:pos.reduce((a,x)=>a+x.bm25.recall,0)/pos.length,hybridRecallAt5:pos.reduce((a,x)=>a+x.hybrid.recall,0)/pos.length,semanticRecallAt5:pos.reduce((a,x)=>a+x.semantic.recall,0)/pos.length,bm25DocumentRecallAt5:pos.reduce((a,x)=>a+x.bm25.documentRecall,0)/pos.length,hybridDocumentRecallAt5:pos.reduce((a,x)=>a+x.hybrid.documentRecall,0)/pos.length,bm25CorrectAbstentions:neg.filter(x=>x.bm25Abstain).length,bm25FalseAbstentions:pos.filter(x=>x.bm25Abstain).length,lexicalCalibration:lexicalBest,correctAbstentions:neg.filter(x=>x.abstain).length,falseAbstentions:pos.filter(x=>x.abstain).length,results};
await fs.mkdir('artifacts',{recursive:true});await fs.writeFile('artifacts/semantic-report.json',JSON.stringify(report,null,2));
console.log(JSON.stringify({...report,results:undefined,calibration:{...best}},null,2));

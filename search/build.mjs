import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {encoder} from './embedding-node.mjs';
import {sections,splitSection} from './chunk.mjs';
import {lexical} from './core.mjs';
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const config=JSON.parse(await fs.readFile('search/config.json','utf8'));
const assets=JSON.parse(await fs.readFile('docs/pregunta/model-assets.json','utf8'));
const signature=hash(JSON.stringify({config,assets,embedding:await fs.readFile('search/embedding.mjs','utf8'),nodeBackend:await fs.readFile('search/embedding-node.mjs','utf8'),chunk:await fs.readFile('search/chunk.mjs','utf8'),lock:await fs.readFile('search/package-lock.json','utf8')}));
const commit=process.env.GITHUB_SHA||execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim();
if(!/^[a-f0-9]{40}$/.test(commit)) throw Error('Invalid source commit');
const cachePath='.cache/semantic/cache.json';
let cache; try { cache=JSON.parse(await fs.readFile(cachePath,'utf8')); } catch { cache={}; }
if(!cache||process.argv.includes('--full')||cache.signature!==signature) cache={};
const {embed,tokenizer}=await encoder(path.resolve('docs/pregunta')+'/');
const files=execFileSync('git',['ls-files','docs/**/*.md','docs/*.md'],{encoding:'utf8'}).trim().split('\n').sort();
let chunks=[], documents=[],fresh=0,reused=0;const entries={}, cachedDocuments={};const started=Date.now();
for(const file of files) {
  const source=await fs.readFile(file,'utf8');
  documents.push({path:file,hash:hash(source),bytes:Buffer.byteLength(source)});
  const docHash=hash(source);
  const old=cache.documents?.[file];
  const documentChunks=old?.hash===docHash && Array.isArray(old.chunks) && old.chunks.every(c=>c.path===file && c.text===source.split('\n').slice(c.start-1,c.end).join('\n'))
    ? old.chunks : sections(source,file).flatMap(s=>splitSection(s,tokenizer,config.maxTokens));
  cachedDocuments[file]={hash:docHash,chunks:documentChunks};
  for(const chunk of documentChunks) {
    const input=chunk.title+'\n'+chunk.text, key=hash(signature+input);
    let vector=entries[key]||cache.entries?.[key];
    if(!Array.isArray(vector)||vector.length!==config.dimensions||vector.some(x=>!Number.isFinite(x))||Math.abs(Math.hypot(...vector)-1)>0.001) {vector=await embed(input,'passage');fresh++;} else reused++;
    entries[key]=vector; chunks.push({...chunk,key});
    if((fresh+reused)%200===0) {console.log(`${fresh} new / ${reused} reused`); await fs.mkdir('.cache/semantic',{recursive:true}); await fs.writeFile(cachePath,JSON.stringify({signature,entries:{...cache.entries,...entries},documents:{...cache.documents,...cachedDocuments}}));}
  }
}
const vectors=new Float32Array(chunks.flatMap(c=>entries[c.key]));
const bytes=Buffer.from(vectors.buffer), lex=lexical(chunks);
const manifest={schema:1,repository:config.repository,commit,signature,model:config,documents,chunks:chunks.length,vectorHash:hash(bytes),fresh,reused,seconds:(Date.now()-started)/1000};
await fs.mkdir('.cache/semantic',{recursive:true}); await fs.writeFile(cachePath,JSON.stringify({signature,entries,documents:cachedDocuments}));
await fs.writeFile('docs/pregunta/chunks.json',JSON.stringify(chunks));
await fs.writeFile('docs/pregunta/lexical.json',JSON.stringify(lex));
await fs.writeFile('docs/pregunta/vectors.f32',bytes);
for(const file of ['chunks.json','lexical.json']) manifest[file+'Hash']=hash(await fs.readFile('docs/pregunta/'+file));
await fs.writeFile('docs/pregunta/manifest.json',JSON.stringify(manifest,null,2));
const probes=[];for(const q of ['¿Qué diferencia hay entre IBNR e IBNER?','How do health claim payment delays affect reserves?']) probes.push({text:q,vector:await embed(q)});
await fs.writeFile('docs/pregunta/parity.json',JSON.stringify(probes));
console.log(JSON.stringify({documents:documents.length,chunks:chunks.length,fresh,reused,seconds:manifest.seconds}));

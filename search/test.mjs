import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import {sections,splitSection} from './chunk.mjs';
import {bm25,lexical,semantic,fuse,citation,accepted} from './core.mjs';
test('Markdown metadata, fences, headings and exact lines',()=>{
 const source='---\ntitle: Test\n---\n# Root\nTexto\n\n## Child\n```js\n# not a heading\n```\nFinal';
 const out=sections(source,'docs/test.md');assert.equal(out.length,2);assert.equal(out[1].heading,'Child');assert.equal(out[1].start,7);assert.equal(out[1].end,11);for(const c of out)assert.equal(source.split('\n').slice(c.start-1,c.end).join('\n'),c.text);
 const setext=sections('Title\n=====\nbody\n\nChild\n-----\nmore','d.md');assert.equal(setext.length,2);assert.equal(setext[1].heading,'Child');
});
test('token-bounded chunks never truncate source silently',()=>{
 const tokenizer=s=>({input_ids:{size:s.length}}),s={text:'abc\ndef\nghi\njkl',heading:'h',title:'t',start:3,path:'d'};
 const out=splitSection(s,tokenizer,21);assert.ok(out.length>1);assert.equal(out.map(x=>x.text).join('\n'),s.text);assert.throws(()=>splitSection({...s,text:'x'.repeat(50)},tokenizer,21));
});
test('BM25, cosine and fusion retrieve independently',()=>{
 const chunks=[{heading:'',text:'IBNR reserva'},{heading:'',text:'GLM modelo'},{heading:'',text:'reserva salud'}];
 const lex=bm25('GLM',lexical(chunks));assert.equal(lex[0].id,1);
 const sem=semantic([1,0],new Float32Array([0,1,1,0,.5,.5]),2);assert.equal(sem[0].id,1);
 assert.equal(fuse(lex,sem,{rrfK:60,candidates:3,lexicalWeight:1,semanticWeight:1})[0].id,1);
 assert.equal(accepted('mi reserva exacta',[{score:1}],.7),false);
});
test('index, citations, source lines and normalized vectors are valid',async()=>{
 const dir='docs/pregunta/',m=JSON.parse(await fs.readFile(dir+'manifest.json')),chunks=JSON.parse(await fs.readFile(dir+'chunks.json')),buffer=await fs.readFile(dir+'vectors.f32');
 assert.match(m.commit,/^[a-f0-9]{40}$/);assert.equal(chunks.length,m.chunks);assert.equal(buffer.length,chunks.length*384*4);
 const hash=b=>crypto.createHash('sha256').update(b).digest('hex');assert.equal(hash(buffer),m.vectorHash);
 const v=new Float32Array(buffer.buffer,buffer.byteOffset,buffer.length/4);let docs=new Map();
 for(let i=0;i<chunks.length;i++) {const c=chunks[i];if(!docs.has(c.path))docs.set(c.path,(await fs.readFile(c.path,'utf8')).split('\n'));assert.equal(docs.get(c.path).slice(c.start-1,c.end).join('\n'),c.text);assert.ok(Math.abs(Math.hypot(...v.subarray(i*384,(i+1)*384))-1)<.001);assert.ok(citation(c,m).includes('/blob/'+m.commit+'/docs/'));}
 for(const d of m.documents)assert.equal(hash(await fs.readFile(d.path)),d.hash);
 for(const f of ['chunks.json','lexical.json'])assert.equal(hash(await fs.readFile(dir+f)),m[f+'Hash']);
});

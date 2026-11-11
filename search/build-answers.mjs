import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {citation} from './core.mjs';
const path='docs/handbook-answers.md',source=await fs.readFile(path,'utf8'),lines=source.split('\n');
const manifest=JSON.parse(await fs.readFile('docs/pregunta/manifest.json','utf8'));
if(manifest.documents.find(d=>d.path===path)?.hash!==createHash('sha256').update(source).digest('hex'))throw Error('Answer source differs from indexed source');
const answers=[];
const starts=lines.flatMap((l,i)=>l.startsWith('## ')?[i]:[]);
for(let n=0;n<starts.length;n++) {
 const start=starts[n],end=starts[n+1]??lines.length,block=lines.slice(start,end).join('\n'),id=block.match(/<!-- answer:([a-z-]+) -->/)?.[1];
 if(!id)throw Error('Missing answer ID');
 function field(name){const a=lines.findIndex((l,i)=>i>start&&i<end&&l==='### '+name);if(a<0)throw Error('Missing '+name);let b=a+1;while(b<end&&!lines[b].startsWith('### '))b++;let first=a+1,last=b;while(!lines[first]?.trim()&&first<last)first++;while(!lines[last-1]?.trim()&&last>first)last--;return {text:lines.slice(first,last).join('\n'),start:first+1,end:last};}
 const answer=field('Respuesta directa'),criteria=field('Criterios para actuar'),variants=field('Preguntas equivalentes').text.split('\n').map(x=>x.replace(/^- /,''));
 const sources=[];
 for(const match of field('Fuentes verificables').text.matchAll(/\[([^\]]+)\]\(([^)]+)\)/g)) {
  const target='docs/'+match[2];if(!manifest.documents.some(d=>d.path===target))throw Error('Source not in published corpus: '+target);
  const original=await fs.readFile(target,'utf8'),title=original.match(/^# (.+)$/m)?.[1]||match[1];
  sources.push({title,path:target,url:citation({path:target,start:1,end:original.split('\n').length},manifest)});
 }
 answers.push({id,question:lines[start].slice(3),variants,answer,criteria,sources,editorialSource:{path,url:citation({path,start:answer.start,end:criteria.end},manifest)}});
}
if(new Set(answers.map(x=>x.id)).size!==answers.length)throw Error('Duplicate answer ID');
await fs.writeFile('docs/pregunta/answers.json',JSON.stringify({commit:manifest.commit,repository:manifest.repository,answers},null,2));
console.log(`Built ${answers.length} source-backed editorial answers`);

import {encoder,modelRevision} from './embedding.mjs';
import {bm25,semantic,fuse,accepted,citation} from './core.mjs';
let ready;
async function checked(name, hash, binary=false) {
  const r=await fetch(new URL(name,self.location.href)); if(!r.ok) throw Error('No se pudo cargar '+name);
  const bytes=await r.arrayBuffer();
  const digest=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),x=>x.toString(16).padStart(2,'0')).join('');
  if(digest!==hash) throw Error('El índice está incompleto o desactualizado. Recarga la página.');
  return binary?new Float32Array(bytes):JSON.parse(new TextDecoder().decode(bytes));
}
async function load() {
  const base=new URL('./',self.location.href).href;
  const [manifest,config]=await Promise.all(['manifest.json','retrieval.json'].map(async f=>{const r=await fetch(base+f,{cache:'no-cache'});if(!r.ok)throw Error('Índice no disponible');return r.json();}));
  if(manifest.model.revision!==modelRevision) throw Error('La aplicación cambió de modelo. Recarga la página.');
  if(config.signature!==manifest.signature||config.commit!==manifest.commit) throw Error('Calibración e índice no corresponden a la misma versión');
  const [chunks,lex,vectors]=await Promise.all([checked('chunks.json',manifest['chunks.jsonHash']),checked('lexical.json',manifest['lexical.jsonHash']),checked('vectors.f32',manifest.vectorHash,true)]);
  if(chunks.length!==manifest.chunks||vectors.length!==chunks.length*manifest.model.dimensions) throw Error('Índice incompleto');
  const model=await encoder(base,p=>{if(p.status==='progress') self.postMessage({type:'progress',text:`Cargando modelo local: ${Math.round(p.progress||0)} %`});});
  return {manifest,config,chunks,lex,vectors,model};
}
self.onmessage=async ({data})=>{
  try {
    ready ||= load().catch(e=>{ready=null;throw e;});
    const state=await ready;
    const start=performance.now(), vector=await state.model.embed(data.query);
    if(data.type==='probe') {self.postMessage({id:data.id,type:'probe',vector});return;}
    const sem=semantic(vector,state.vectors,state.manifest.model.dimensions),lex=bm25(data.query,state.lex,state.config.k1,state.config.b);
    const ranked=fuse(lex,sem,state.config), sufficient=accepted(data.query,sem,state.config.threshold);
    self.postMessage({id:data.id,type:'results',sufficient,ms:performance.now()-start,commit:state.manifest.commit,results:sufficient?ranked.slice(0,5).map(x=>({...state.chunks[x.id],url:citation(state.chunks[x.id],state.manifest)})):[]});
  } catch(e){self.postMessage({id:data.id,type:'error',text:e.message});}
};

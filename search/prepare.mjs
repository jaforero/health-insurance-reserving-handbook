import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {build} from 'esbuild';
const config=JSON.parse(await fs.readFile(new URL('./config.json',import.meta.url)));
const out='docs/pregunta';
await fs.mkdir(out+'/models/e5-'+config.revision+'/onnx',{recursive:true}); await fs.mkdir(out+'/runtime',{recursive:true});
const expected=JSON.parse(await fs.readFile('search/model-assets.lock.json','utf8'));
if(expected.revision!==config.revision) throw Error('Update and review model asset lock for the pinned revision');
const hashes={};
for(const name of config.files) {
  const dest=out+'/models/e5-'+config.revision+'/'+name, marker=dest+'.revision';
  if(await fs.readFile(marker,'utf8').catch(()=>null)!==config.revision) {
    console.log('Downloading pinned model asset:',name);
    const r=await fetch(`https://huggingface.co/${config.model}/resolve/${config.revision}/${name}`);
    if(!r.ok) throw Error(`${r.status}: ${name}`);
    await fs.writeFile(dest,new Uint8Array(await r.arrayBuffer())); await fs.writeFile(marker,config.revision);
  }
  hashes[name]=crypto.createHash('sha256').update(await fs.readFile(dest)).digest('hex');
  if(hashes[name]!==expected.hashes[name]) {await fs.rm(marker,{force:true});throw Error('Model asset integrity mismatch: '+name+'; rerun to download clean pinned assets');}
}
await fs.writeFile(out+'/model-assets.json',JSON.stringify({revision:config.revision,hashes},null,2));
// Include model provenance and upstream MIT license in the deployment.
const readme=await fetch(`https://huggingface.co/intfloat/multilingual-e5-small/raw/${config.upstreamRevision}/README.md`);
if(!readme.ok) throw Error('Cannot verify model license');
const card=await readme.text(); if(!/^license: mit$/m.test(card)) throw Error('Model license changed');
await fs.writeFile(out+'/models/MODEL_CARD.md',card);
for(const name of await fs.readdir('search/node_modules/onnxruntime-web/dist'))
  if(/\.wasm$|^ort-wasm.*\.mjs$/.test(name)) await fs.copyFile('search/node_modules/onnxruntime-web/dist/'+name,out+'/runtime/'+name);
await fs.copyFile('search/node_modules/@huggingface/transformers/LICENSE',out+'/runtime/TRANSFORMERS_LICENSE');
const license=await fetch('https://raw.githubusercontent.com/microsoft/onnxruntime/89f8206ba4f1c22c39e0297fb55272e8ce8cd7d0/LICENSE');
if(!license.ok) throw Error('ONNX license unavailable');
await fs.writeFile(out+'/runtime/ONNX_LICENSE',await license.text());
for(const file of ['index.html','style.css']) await fs.copyFile('search/'+file,out+'/'+file);
for(const file of ['app','worker']) await build({entryPoints:['search/'+file+'.mjs'],outfile:out+'/'+file+'.js',bundle:true,format:'esm',platform:'browser',minify:true,legalComments:'eof'});

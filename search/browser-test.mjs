import {chromium} from 'playwright';
import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const prefix='/health-insurance-reserving-handbook/',root=path.resolve(process.env.SEARCH_SITE_ROOT||'docs');
const server=http.createServer(async(req,res)=>{try{let rel=decodeURIComponent(new URL(req.url,'http://local').pathname);if(!rel.startsWith(prefix))throw Error();rel=rel.slice(prefix.length)||'index.html';if(rel.endsWith('/'))rel+='index.html';const file=path.resolve(root,rel);if(!file.startsWith(root+path.sep))throw Error();const body=await fs.readFile(file);res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.wasm':'application/wasm','.json':'application/json','.css':'text/css'})[path.extname(file)]||'application/octet-stream');res.end(body);}catch{res.writeHead(404);res.end();}});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const origin=`http://127.0.0.1:${server.address().port}`;
const browser=await chromium.launch({headless:true,args:['--no-sandbox']}),context=await browser.newContext(),page=await context.newPage(),external=[],errors=[],requests=[];
context.on('request',r=>{requests.push(r.url());if(new URL(r.url()).origin!==origin)external.push(r.url());});
await context.route('**/*',route=>new URL(route.request().url()).origin===origin?route.continue():route.abort());
page.on('pageerror',e=>errors.push(e.message));
try {
 await page.goto(origin+prefix+'pregunta/');
 // The fundamental question must yield a concrete answer before any model download.
 await page.locator('#question').fill('Como funcionan los triangulos de reservas?');
 await page.locator('#search button').click();
 await page.locator('article[data-answer-id="triangles"]').waitFor();
 const direct=await page.locator('article[data-answer-id="triangles"]').innerText();
 assert.match(direct,/filas representan periodos de origen/);
 assert.match(direct,/columnas, edades de desarrollo/);
 assert.match(direct,/no es un método de estimación/);
 assert.ok(direct.indexOf('Criterios para actuar')<direct.indexOf('Fuentes verificables'));
 assert.equal(await page.locator('#results details summary').innerText(),'Exploración adicional');
 assert.equal(requests.filter(x=>x.endsWith('.onnx')).length,0,'Editorial answers must not download embeddings');
 await page.screenshot({path:'artifacts/semantic-answer-desktop.png',fullPage:true});
 await page.setViewportSize({width:390,height:844});
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await page.screenshot({path:'artifacts/semantic-answer-mobile.png',fullPage:true});
 const parity=[...JSON.parse(await fs.readFile(root+'/pregunta/parity.json','utf8')),...JSON.parse(await fs.readFile(root+'/pregunta/evaluation-probes.json','utf8'))];
 const start=Date.now();
 const vectors=await page.evaluate(async probes=>{const w=new Worker('./worker.js',{type:'module'});const ask=(query,id)=>new Promise((resolve,reject)=>{w.onmessage=e=>{if(e.data.id!==id)return;if(e.data.type==='error')reject(Error(e.data.text));else if(e.data.type==='probe')resolve(e.data.vector);};w.postMessage({type:'probe',query,id});});const out=[];for(let i=0;i<probes.length;i++)out.push(await ask(probes[i].text,i));w.terminate();return out;},parity);
 const maxErrors=vectors.map((v,i)=>Math.max(...v.map((x,j)=>Math.abs(x-parity[i].vector[j]))));
 const cosines=vectors.map((v,i)=>v.reduce((s,x,j)=>s+x*parity[i].vector[j],0)/(Math.hypot(...v)*Math.hypot(...parity[i].vector)));
 // Same quantized weights, but native CPU and WASM kernels may round differently.
 console.log('Embedding parity', {cosines,maxErrors});
 assert.ok(cosines.every(x=>x>.999),'Node/browser embedding cosine must exceed .999');
 await page.locator('#question').fill('¿Cuáles son los supuestos necesarios para utilizar Chain Ladder?');await page.locator('#search button').click();await page.waitForFunction(()=>document.querySelectorAll('article').length>0,{},{timeout:180000});
 const first=await page.locator('article a').first().getAttribute('href');assert.match(first,/\/blob\/[a-f0-9]{40}\/docs\/.*#L\d+-L\d+$/);
 await page.screenshot({path:'artifacts/semantic-desktop.png',fullPage:true});
 await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await page.screenshot({path:'artifacts/semantic-mobile-results.png',fullPage:true});
 // Semantic exploration remains available without replacing the direct answer.
 const answerBefore=await page.locator('article[data-answer-id]').innerText();
 await page.locator('#results details summary').click();
 await page.getByRole('button',{name:'Buscar evidencia adicional en el manual'}).click();
 await page.waitForFunction(()=>document.querySelector('#status').textContent.startsWith('Procesado localmente'),{},{timeout:180000});
 assert.equal(await page.locator('article[data-answer-id]').innerText(),answerBefore);
 assert.ok(await page.locator('#results details article').count()>0);
 const before=requests.filter(x=>x.endsWith('.onnx')).length;
 await page.locator('#question').fill('¿Cuál es el IBNR exacto de mi EPS si no he aportado triángulos ni datos?');await page.locator('#search button').click();await page.getByText('No encontré información suficiente en los documentos para responder esta pregunta.',{exact:true}).waitFor();
 assert.equal(requests.filter(x=>x.endsWith('.onnx')).length,before,'Model must not download per query');
 await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await page.screenshot({path:'artifacts/semantic-mobile.png',fullPage:true});
 await page.locator('#question').fill('Como funcionan los triangulos de reservas y que es ultimate');
 await page.locator('#search button').click();
 await page.getByText('Tu pregunta incluye varios temas.',{exact:false}).waitFor();
 assert.equal(await page.locator('article[data-answer-id]').count(),0);
 await page.locator('#question').fill('Formula de Chain Ladder');
 await page.locator('#search button').click();
 await page.getByText('No tengo una respuesta directa verificada',{exact:false}).waitFor();
 assert.equal(await page.locator('article[data-answer-id]').count(),0);
 // Test the existing MkDocs entry points in a separate context. Legacy site assets
 // are blocked off-origin; the canonical answer page is independently audited above.
 const entryChecks=[];
 if(process.env.SEARCH_SITE_ROOT){
  const entryContext=await browser.newContext();
  await entryContext.route('**/*',route=>new URL(route.request().url()).origin===origin?route.continue():route.abort());
  const entry=await entryContext.newPage();
  await entry.goto(origin+prefix);
  await entry.locator('[data-handbook-qa-global-trigger]').click();
  await entry.waitForURL(origin+prefix+'pregunta/');entryChecks.push('global');
  await entry.goto(origin+prefix+'ask-the-handbook/');
  await entry.waitForURL(origin+prefix+'pregunta/');entryChecks.push('historical');
  await entryContext.close();
 }
 assert.deepEqual(external,[]);assert.deepEqual(errors,[]);
 const report={prefix,editorialAnswer:true,editorialModelRequests:0,entryChecks,cosines,maxErrors,secondsIncludingColdLoad:(Date.now()-start)/1000,externalRequests:external.length,modelRequests:requests.filter(x=>x.endsWith('.onnx')).length,sourceLink:first};
 await fs.writeFile('artifacts/semantic-browser.json',JSON.stringify(report,null,2));console.log(report);
} finally{await browser.close();server.close();}

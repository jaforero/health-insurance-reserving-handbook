import {tokens,scopeReason} from './core.mjs';
import {answerFor} from './answers.mjs';
const form=document.querySelector('#search'), input=document.querySelector('#question'),status=document.querySelector('#status'),output=document.querySelector('#results'),button=form.querySelector('button');
let worker,sequence=0,catalogPromise,explorationTarget,activeQuery;
const catalog=()=>catalogPromise ||= fetch(new URL('./answers.json',import.meta.url),{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error('No se pudo cargar el catálogo de respuestas');return r.json();}).catch(e=>{catalogPromise=null;throw e;});
function node(tag,text,className){const el=document.createElement(tag);el.textContent=text;if(className)el.className=className;return el;}
function link(text,url){const a=node('a',text);a.href=url;a.target='_blank';a.rel='noopener noreferrer';return a;}
function excerpt(text,query){const el=node('blockquote',''),terms=new Set(tokens(query));for(const part of text.split(/([\p{L}\p{N}]+)/u)){el.append(terms.has(tokens(part)[0])?node('mark',part):document.createTextNode(part));}return el;}
function showAnswer(answer,commit,query){
 const article=node('article','');article.dataset.answerId=answer.id;
 article.append(node('p','Respuesta editorial · basada en el Handbook','eyebrow'),node('h2',answer.question),node('p',answer.answer.text));
 article.append(node('h3','Criterios para actuar'));const list=node('ul','');for(const line of answer.criteria.text.split('\n'))list.append(node('li',line.replace(/^- /,'')));article.append(list);
 article.append(node('h3','Fuentes verificables'),link('Respuesta y criterios · líneas '+answer.answer.start+'–'+answer.criteria.end,answer.editorialSource.url));
 const sources=node('ul','');for(const source of answer.sources){const li=node('li','');li.append(link(source.title,source.url));sources.append(li);}article.append(sources,node('p','Versión documental: '+commit,'source'));
 output.append(article);
 const explore=node('details','');explore.append(node('summary','Exploración adicional'));
 const action=node('button','Buscar evidencia adicional en el manual');action.type='button';
 const target=node('div','');explore.append(node('p','Esta búsqueda opcional carga el modelo local y muestra pasajes relacionados; no modifica la respuesta editorial.'),action,target);
 action.addEventListener('click',()=>{action.disabled=true;searchEvidence(query,target);});output.append(explore);
 document.querySelector('#version').textContent='Versión documental: '+commit;
 status.textContent='Respuesta directa recuperada del manual. Esta consulta no necesita cargar el modelo de embeddings.';
}
function searchEvidence(query,target){
 explorationTarget=target;activeQuery=query;button.disabled=true;status.textContent='Buscando evidencia local. La primera carga del modelo puede tardar…';
 if(!worker){worker=new Worker(new URL('./worker.js',import.meta.url),{type:'module'});
  worker.onerror=()=>{button.disabled=false;status.textContent='No fue posible iniciar la búsqueda semántica local.';worker.terminate();worker=null;};
  worker.onmessage=({data})=>{
   if(data.type==='progress'){status.textContent=data.text;return;}
   if(data.id!==sequence)return;button.disabled=false;
   if(data.type==='error'){status.textContent='No fue posible completar la búsqueda semántica: '+data.text;return;}
   status.textContent=`Procesado localmente en ${(data.ms/1000).toFixed(2)} s (sin incluir descarga inicial).`;
   document.querySelector('#version').textContent='Versión documental: '+data.commit;
   if(!data.sufficient){explorationTarget.append(node('p','No encontré información suficiente en los documentos para responder esta pregunta.'));return;}
   for(const r of data.results){const article=node('article','');article.append(node('h3',r.heading),excerpt(r.text,activeQuery),link('Abrir documento original · líneas '+r.start+'–'+r.end,r.url),node('p',r.path+' · SHA '+data.commit,'source'));explorationTarget.append(article);}
  };
 }
 worker.postMessage({id:++sequence,query});
}
form.addEventListener('submit',async event=>{
 event.preventDefault();if(!form.reportValidity())return;const query=input.value;const request=++sequence;output.replaceChildren();button.disabled=true;
 try{
  if(scopeReason(query)){output.append(node('p','No encontré información suficiente en los documentos para responder esta pregunta.'));status.textContent='La pregunta requiere información que no está disponible en el manual.';return;}
  const data=await catalog();if(request!==sequence)return;const match=answerFor(query,data);
  if(match.kind==='answer'){showAnswer(match.answer,data.commit,query);return;}
  if(match.kind==='clarify'){
   status.textContent='Selecciona un tema para obtener su respuesta y fuentes.';
   output.append(node('p','Tu pregunta incluye varios temas. Selecciona cuál quieres resolver primero:'));
   for(const c of match.choices){const action=node('button',c.question);action.type='button';action.addEventListener('click',()=>{input.value=c.question;form.requestSubmit();});output.append(action);}return;
  }
  output.append(node('p','No tengo una respuesta directa verificada para esta formulación. Puedes precisar la pregunta o explorar los pasajes relacionados.'));
  const details=node('details','');details.append(node('summary','Explorar documentación relacionada'));const action=node('button','Buscar en el manual');action.type='button';const target=node('div','');details.append(action,target);action.addEventListener('click',()=>{action.disabled=true;searchEvidence(query,target);});output.append(details);
  status.textContent='No se ha inferido una respuesta a partir de coincidencias temáticas.';
 }catch(e){status.textContent=e.message;}finally{button.disabled=false;}
});

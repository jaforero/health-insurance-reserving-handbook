import {tokens} from './core.mjs';
const form=document.querySelector('#search'), input=document.querySelector('#question'),status=document.querySelector('#status'),output=document.querySelector('#results'),button=form.querySelector('button');
let worker,sequence=0;
function excerpt(text,query){const el=document.createElement('blockquote'),terms=new Set(tokens(query));for(const part of text.split(/([\p{L}\p{N}]+)/u)){const tag=terms.has(tokens(part)[0])?'mark':null;el.append(tag?node(tag,part):document.createTextNode(part));}return el;}
function node(tag,text,className){const el=document.createElement(tag);el.textContent=text;if(className)el.className=className;return el;}
form.addEventListener('submit',event=>{
  event.preventDefault(); if(!form.reportValidity())return;
  button.disabled=true;output.replaceChildren();status.textContent='Preparando búsqueda local. La primera carga puede tardar…';
  if(!worker){worker=new Worker(new URL('./worker.js',import.meta.url),{type:'module'});
    worker.onerror=()=>{button.disabled=false;status.textContent='No fue posible iniciar el motor semántico local. Prueba un navegador actualizado.';worker.terminate();worker=null;};
    worker.onmessage=({data})=>{
      if(data.type==='progress'){status.textContent=data.text;return;}
      if(data.id!==sequence)return;
      button.disabled=false;
      if(data.type==='error'){status.textContent='No fue posible completar la búsqueda semántica: '+data.text;return;}
      status.textContent=`Procesado localmente en ${(data.ms/1000).toFixed(2)} s (sin incluir descarga inicial).`;
      document.querySelector('#version').textContent='Versión documental: '+data.commit;
      if(!data.sufficient){output.append(node('p','No encontré información suficiente en los documentos para responder esta pregunta.'));return;}
      data.results.forEach((r,i)=>{const article=node('article','');article.append(node('h2',`${i+1}. ${r.heading}`),node('p',r.title,'source'),excerpt(r.text,input.value));const a=node('a','Abrir documento original · líneas '+r.start+'–'+r.end);a.href=r.url;a.target='_blank';a.rel='noopener noreferrer';article.append(a,node('p',r.path+' · SHA '+data.commit,'source'));output.append(article);});
    };
  }
  worker.postMessage({id:++sequence,query:input.value});
});

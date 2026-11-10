import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';
const root=process.cwd(),tmp=await fs.mkdtemp(path.join(os.tmpdir(),'handbook-index-'));
const run=(cmd,args)=>execFileSync(cmd,args,{cwd:tmp,encoding:'utf8',stdio:'pipe'});
try {
 await fs.symlink(root+'/search',tmp+'/search','dir');await fs.mkdir(tmp+'/docs/pregunta',{recursive:true});
 await fs.symlink(root+'/docs/pregunta/models',tmp+'/docs/pregunta/models','dir');await fs.symlink(root+'/docs/pregunta/runtime',tmp+'/docs/pregunta/runtime','dir');await fs.copyFile(root+'/docs/pregunta/model-assets.json',tmp+'/docs/pregunta/model-assets.json');
 run('git',['init','-q']);run('git',['config','user.name','Index test']);run('git',['config','user.email','test@example.invalid']);
 await fs.writeFile(tmp+'/docs/a.md','# Reservas\n\nEl IBNR corresponde a siniestros ocurridos no reportados.\n');await fs.writeFile(tmp+'/docs/b.md','# Otra sección\n\nUn triángulo organiza periodos de origen y desarrollo.\n');
 const commit=()=>{run('git',['add','docs/*.md']);run('git',['commit','-qm','fixture']);};
 const build=(args=[])=>{run(process.execPath,[root+'/search/build.mjs',...args]);};
 const manifest=async()=>JSON.parse(await fs.readFile(tmp+'/docs/pregunta/manifest.json'));
 commit();build();assert.equal((await manifest()).fresh,2);
 build();assert.equal((await manifest()).fresh,0);assert.equal((await manifest()).reused,2);
 await fs.writeFile(tmp+'/docs/a.md','# Reservas\n\nEl IBNER corresponde al desarrollo de siniestros ya reportados.\n');await fs.unlink(tmp+'/docs/b.md');run('git',['rm','docs/b.md']);await fs.writeFile(tmp+'/docs/c.md','# Método\n\nBornhuetter Ferguson combina un prior con desarrollo observado.\n');commit();build();
 const m=await manifest();assert.deepEqual(m.documents.map(d=>d.path),['docs/a.md','docs/c.md']);assert.equal(m.fresh,2);
 const chunks=JSON.parse(await fs.readFile(tmp+'/docs/pregunta/chunks.json'));assert.ok(chunks.every(c=>c.path!=='docs/b.md'));
 await fs.writeFile(tmp+'/.cache/semantic/cache.json','{broken');build();assert.equal((await manifest()).fresh,2);assert.equal((await manifest()).vectorHash,m.vectorHash);
 build(['--full']);assert.equal((await manifest()).fresh,2);assert.equal((await manifest()).vectorHash,m.vectorHash);
 console.log('PASS: unchanged / added / modified / deleted / corrupt cache / full rebuild');
} finally {await fs.rm(tmp,{recursive:true,force:true});}

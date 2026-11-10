import fs from 'node:fs/promises';
async function size(dir){let total=0;for(const e of await fs.readdir(dir,{withFileTypes:true})){const p=dir+'/'+e.name;total+=e.isDirectory()?await size(p):(await fs.stat(p)).size;}return total;}
const bytes=await size('site');console.log(`Published site: ${(bytes/1e6).toFixed(1)} MB`);
// Conservative headroom under the documented 1 GB Pages maximum.
if(bytes>900_000_000)throw Error('Site exceeds 900 MB release budget; do not publish.');

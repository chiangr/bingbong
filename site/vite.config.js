import { defineConfig } from 'vite';
import { readdir,writeFile,readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
async function walk(path){const files=[];for(const entry of await readdir(path,{withFileTypes:true})){const file=`${path}/${entry.name}`;if(entry.isDirectory())files.push(...await walk(file));else files.push(file);}return files;}
export default defineConfig({
  server:{host:'127.0.0.1',port:5173},
  preview:{host:'127.0.0.1',port:4173},
  build:{target:'es2022',chunkSizeWarningLimit:700},
  plugins:[{name:'inline-small-styles',enforce:'post',generateBundle(_,bundle){const html=bundle['index.html'];if(!html)return;html.source=String(html.source).replace(/<link[^>]*rel="stylesheet"[^>]*href="([^"]+)"[^>]*>/g,(tag,url)=>{const css=bundle[url.replace(/^\//,'')];return css?`<style>${css.source}</style>`:tag;});}}, {name:'static-offline-cache',async closeBundle(){
    if(process.env.BINGBONG_ARTIFACT)return;
    let files;try{files=(await walk('dist')).filter(file=>!file.endsWith('sw.js'));}catch{return;}
    const digest=createHash('sha256');for(const file of files)digest.update(await readFile(file));const version=digest.digest('hex').slice(0,12);
    const paths=files.map(file=>'/'+file.slice(5));paths.push('/');
    await writeFile('dist/sw.js',`const CACHE='bingbong-${version}';const FILES=${JSON.stringify(paths)};self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(FILES)).then(()=>self.skipWaiting()));});self.addEventListener('activate',event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith('bingbong-')&&key!==CACHE).map(key=>caches.delete(key)))).then(()=>self.clients.claim()));});self.addEventListener('fetch',event=>{if(event.request.method!=='GET'||new URL(event.request.url).origin!==self.location.origin)return;if(event.request.mode==='navigate'){event.respondWith(fetch(event.request).catch(()=>caches.match('/',{ignoreVary:true})));return;}event.respondWith(caches.match(event.request,{ignoreVary:true}).then(cached=>cached||fetch(event.request)));});`);
  }}]
});

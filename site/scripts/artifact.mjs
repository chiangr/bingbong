import{build}from'vite';import{readFile,writeFile,readdir,mkdir}from'node:fs/promises';
process.env.BINGBONG_ARTIFACT='1';
const result=await build({build:{write:false,rollupOptions:{output:{inlineDynamicImports:true}}}});
const output=Array.isArray(result)?result[0].output:result.output;
const js=output.find(file=>file.type==='chunk').code;
let css=output.filter(file=>file.fileName.endsWith('.css')).map(file=>file.source).join('\n');
const htmlAsset=output.find(file=>file.fileName==='index.html');let html=String(htmlAsset.source);
const map={};const types={'.woff2':'font/woff2','.webp':'image/webp','.svg':'image/svg+xml','.png':'image/png'};
async function walk(directory){for(const item of await readdir(directory,{withFileTypes:true})){const path=`${directory}/${item.name}`;if(item.isDirectory())await walk(path);else{const ext=path.slice(path.lastIndexOf('.'));if(types[ext])map[path.slice(6)]=`data:${types[ext]};base64,${(await readFile(path)).toString('base64')}`;}}}
await walk('public');
for(const[path,data]of Object.entries(map)){css=css.replaceAll(path,data);html=html.replaceAll(path,data);}
html=html.replace(/<script[^>]*src="[^"]+"[^>]*><\/script>/g,'').replace(/<link[^>]*(?:rel="stylesheet"|rel="modulepreload")[^>]*>/g,'');
const fontLicenses={};for(const file of await readdir('public/fonts'))if(file.endsWith('OFL.txt'))fontLicenses[file]=await readFile(`public/fonts/${file}`,'utf8');
fontLicenses['THIRD_PARTY_NOTICES.txt']=await readFile('public/THIRD_PARTY_NOTICES.txt','utf8');
html=html.replace('</body>',()=>`<script type="application/json" id="font-license-notices">${JSON.stringify(fontLicenses)}</script><script>window.__BINGBONG_ASSETS=${JSON.stringify(map)};</script><script type="module">${js.replaceAll('</script','<\\/script')}</script></body>`);
await mkdir('artifact',{recursive:true});await writeFile('artifact/bingbong.html',html);console.log(`Single-file artifact: ${(Buffer.byteLength(html)/1024/1024).toFixed(2)} MB, no external asset requests.`);

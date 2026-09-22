import {chromium} from '@playwright/test';
import {mkdir,writeFile} from 'node:fs/promises';
import sharp from 'sharp';
const browser=await chromium.launch({channel:'chrome',headless:true});await mkdir('qa/assembly',{recursive:true});
const errors=[];
for(const width of [1440,390]){
 const page=await browser.newPage({viewport:{width,height:width===390?844:1000},reducedMotion:'reduce',serviceWorkers:'block'});
 page.on('pageerror',error=>{errors.push(error.message);console.log('ERROR',error.message);});
 page.on('console',m=>{if(m.type()==='warning'||m.type()==='error')console.log(m.type(),m.text().slice(0,200));});
 await page.goto(process.env.QA_URL||'http://127.0.0.1:5173');await page.waitForFunction(()=>window.__bingbong?.scene);
 for(const id of ['hello','inside','crown','detents','antenna','assembly']){
  await page.evaluate(id=>document.querySelector('#'+id).scrollIntoView({behavior:'instant'}),id);
  if(id!=='hello')await page.waitForFunction(()=>document.documentElement.dataset.assemblyReady==='true');
  await page.waitForTimeout(450);await page.screenshot({path:`qa/assembly/${width}-${id}.png`});
  console.log(width,id,await page.evaluate(()=>({chapter:window.__bingbong.chapter,model:window.__bingbong.frame.scale,overflow:document.documentElement.scrollWidth>innerWidth,parts:window.__bingbong.scene.assembly?.pickables.length,draws:window.__bingbong.scene.renderer.info.render.calls})));
 }
 await page.locator('#build-progress').fill('100');await page.waitForTimeout(200);await page.screenshot({path:`qa/assembly/${width}-assembled.png`});
 const frames=await Promise.all(['inside','crown','detents','antenna','assembly','assembled'].map(id=>sharp(`qa/assembly/${width}-${id}.png`).resize({width:width===390?195:480}).png().toBuffer({resolveWithObject:true})));
 const w=frames[0].info.width,h=frames[0].info.height;await sharp({create:{width:w*3,height:h*2,channels:4,background:'#080b13'}}).composite(frames.map((frame,i)=>({input:frame.data,left:i%3*w,top:Math.floor(i/3)*h}))).png().toFile(`qa/assembly/overview-${width}.png`);
 await page.close();
}
await browser.close();await writeFile('qa/assembly/preview-errors.json',JSON.stringify(errors));

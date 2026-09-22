import {chromium} from '@playwright/test';
import {mkdir,writeFile} from 'node:fs/promises';
import sharp from 'sharp';
await mkdir('qa/redesign',{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
const report=[];
for(const[width,height]of[[1440,900],[390,844],[820,1180]]){
 const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1,serviceWorkers:'block'});
 page.on('pageerror',e=>report.push({error:e.message}));
 await page.goto('http://127.0.0.1:5173');await page.waitForFunction(()=>document.documentElement.dataset.ready==='true');await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(1200);
 const shots=[];
 for(const id of ['hello','pet','boop','hold','creature','halo','object','quiet','size','details']){
  await page.evaluate(id=>document.getElementById(id).scrollIntoView({behavior:'instant'}),id);await page.waitForTimeout(1000);
  const path=`qa/redesign/${width}-${id}.png`;await page.screenshot({path});report.push({width,id,chapter:await page.evaluate(()=>window.__bingbong.chapter),overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)});
  const thumb=await sharp(path).resize({width:width<700?195:360}).png().toBuffer({resolveWithObject:true});shots.push(thumb);
 }
 await sharp({create:{width:shots[0].info.width*5,height:shots[0].info.height*2,channels:4,background:'#080b13'}}).composite(shots.map((s,i)=>({input:s.data,left:i%5*s.info.width,top:Math.floor(i/5)*s.info.height}))).png().toFile(`qa/redesign/overview-${width}.png`);
 await page.close();
}
await writeFile('qa/redesign/visual-results.json',JSON.stringify(report,null,2));await browser.close();console.log('Redesign screenshots ready.');

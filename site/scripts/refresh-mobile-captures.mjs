// Refresh the affected visual matrix after a mobile-only polish change.
// The complete functional matrix remains in qa.mjs; no checks are suppressed.
import {chromium} from '@playwright/test';
import {readFile,writeFile} from 'node:fs/promises';
import sharp from 'sharp';
const report=JSON.parse(await readFile('qa/results.json','utf8'));
const browser=await chromium.launch({channel:'chrome',headless:true}),errors=[];
try{
  for(const theme of ['dark','light'])for(const motion of ['no-preference','reduce']){
    const screens=report.screens.filter(s=>s.width===390&&s.theme===theme&&s.motion===motion);
    if(screens.length!==15)throw new Error('Expected the full fifteen-chapter mobile matrix');
    const context=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1,colorScheme:theme,reducedMotion:motion});
    const page=await context.newPage();page.on('pageerror',error=>errors.push(error.message));
    await page.goto(report.base);await page.waitForFunction(()=>window.__bingbong?.scene);await page.evaluate(()=>document.fonts.ready);
    for(const screen of screens){
      await page.evaluate(id=>document.querySelector('#'+id).scrollIntoView({behavior:'instant'}),screen.chapter);await page.waitForTimeout(750);
      const state=await page.evaluate(()=>({id:document.querySelectorAll('.story-section')[window.__bingbong.chapter].id,overflow:document.documentElement.scrollWidth>innerWidth}));
      if(state.id!==screen.chapter||state.overflow)throw new Error(`Unexpected layout in ${screen.chapter}`);
      await page.screenshot({path:`qa/screens/${screen.file}`,animations:'disabled'});
    }
    const frames=await Promise.all(screens.map(s=>sharp(`qa/screens/${s.file}`).resize({width:195}).png().toBuffer({resolveWithObject:true})));
    const h=frames[0].info.height;
    await sharp({create:{width:975,height:h*3,channels:4,background:'#080b13'}}).composite(frames.map((f,i)=>({input:f.data,left:i%5*195,top:Math.floor(i/5)*h}))).png().toFile(`qa/screens/overview-390-${theme}-${motion}.png`);
    await context.close();console.log(`Refreshed mobile captures: ${theme}, ${motion}`);
  }
  if(errors.length)throw new Error(errors.join('\n'));
  report.captureRefreshes??=[];report.captureRefreshes.push({date:new Date().toISOString(),width:390,reason:'Pair labels clear after instant reduced-motion navigation.'});
  await writeFile('qa/results.json',JSON.stringify(report,null,2));
}finally{await browser.close();}

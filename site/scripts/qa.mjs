import { chromium } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { mkdir,writeFile } from 'node:fs/promises';
import sharp from 'sharp';
const base=process.env.QA_URL||'http://127.0.0.1:4173';
await mkdir('qa/screens',{recursive:true});await mkdir('qa/motion',{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
const report={date:new Date().toISOString(),base,screens:[],checks:[],errors:[],a11y:[],headings:[],limitations:['Browser emulation is not a physical phone test.','A screen-reader user and owner must still validate experience and appearance.']};
const check=(name,pass,details)=>{report.checks.push({name,pass,details});console.log(`${pass?'PASS':'FAIL'} ${name}`);};
const chapters=['hello','pet','boop','hold','creature','halo','object','quiet','size','details','inside','crown','detents','antenna','assembly'];
const visit=async(page,chapter)=>{await page.evaluate(id=>{document.querySelector(`#${id}`).scrollIntoView({behavior:'instant',block:'start'});},chapter);await page.waitForTimeout(750);};
for(const [width,height] of [[390,844],[820,1180],[1440,900],[1920,1080]])for(const theme of ['dark','light'])for(const motion of ['no-preference','reduce']){
  const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:1,colorScheme:theme,reducedMotion:motion});
  const page=await context.newPage();page.on('pageerror',error=>report.errors.push({width,theme,motion,message:error.message}));
  await page.goto(base);await page.waitForFunction(()=>window.__bingbong?.scene);await page.evaluate(()=>document.fonts.ready);
  const overflow=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,viewport:innerWidth}));check(`No horizontal overflow ${width}/${theme}/${motion}`,overflow.scroll<=width,overflow);
  for(const chapter of chapters){await visit(page,chapter);const file=`${width}-${theme}-${motion}-${chapter}.png`;await page.screenshot({path:`qa/screens/${file}`,animations:'disabled'});const actual=await page.evaluate(()=>window.__bingbong.chapter);report.screens.push({file,width,height,theme,motion,chapter,active:chapters[actual]});}
  if((width===390||width===1440)&&motion==='reduce'){
    await visit(page,'hello');const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice']).analyze();report.a11y.push({width,theme,violations:axe.violations});check(`axe ${width}/${theme}`,axe.violations.length===0,axe.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)})));
    await visit(page,'halo');const halo=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();report.a11y.push({width,theme,chapter:'halo',violations:halo.violations});check(`axe halo ${width}/${theme}`,halo.violations.length===0,halo.violations.map(v=>v.id));
  }
  if(width===1440&&theme==='dark'&&motion==='reduce')report.headings=await page.locator('h1,h2').allTextContents();
  await context.close();console.log(`Screens ${width} ${theme} ${motion}`);
}

const context=await browser.newContext({viewport:{width:1440,height:900},colorScheme:'dark',reducedMotion:'reduce'});const page=await context.newPage();await page.goto(base);await page.waitForFunction(()=>window.__bingbong);await page.evaluate(()=>window.__bingbong.start());await page.waitForFunction(()=>window.__bingbong?.scene);await visit(page,'pet');
const angle=()=>page.evaluate(()=>window.__bingbong.frame.crown||0);
let a=await angle();await page.locator('[data-turn="1"]').click();check('Plus advances exactly 15 degrees',Math.abs((await angle())-a-Math.PI/12)<1e-5);
await page.waitForTimeout(300);check('Other device reacts to a turn',await page.evaluate(()=>window.__bingbong.frame.otherState==='petted'));
await page.waitForTimeout(700);check('Purr settles after stopping',await page.evaluate(()=>!window.__bingbong.interactions.overrides.otherState));
await page.locator('#crown-target').focus();a=await angle();await page.keyboard.press('ArrowRight');check('Keyboard crown detent',Math.abs((await angle())-a-Math.PI/12)<1e-5);
const box=await page.locator('#crown-target').boundingBox();a=await angle();await page.mouse.move(box.x+32,box.y+32);await page.mouse.down();await page.mouse.move(box.x+72,box.y+32,{steps:4});await page.mouse.up();check('Mouse drag moves crown by detents',Math.abs((await angle())-a-4*Math.PI/12)<1e-5);
const stopped=await angle();await page.waitForTimeout(350);check('Crown does not coast',Math.abs(await angle()-stopped)<1e-5);
await visit(page,'boop');await page.locator('[data-boop]').click();await page.waitForTimeout(500);check('Boop has not arrived at 500 ms',await page.evaluate(()=>window.__bingbong.frame.otherHalo===0));await page.waitForTimeout(2250);check('Boop arrives after conversation delay',await page.evaluate(()=>window.__bingbong.frame.otherHalo===1&&window.__bingbong.frame.otherState==='boop'));
await page.locator('[data-boop]').click();await visit(page,'quiet');await page.waitForTimeout(2800);check('Pending boop does not contaminate another chapter',await page.evaluate(()=>window.__bingbong.frame.screen===false&&window.__bingbong.frame.halo===0));
await visit(page,'hold');await page.locator('[data-hold]').focus();await page.keyboard.down('Space');check('Keyboard hold leans in',await page.evaluate(()=>window.__bingbong.frame.state==='leaning'));await page.keyboard.up('Space');check('Releasing hold settles',await page.evaluate(()=>window.__bingbong.frame.state==='resting'));
await visit(page,'creature');await page.locator('[data-creature="away"]').click();check('Away selector',await page.evaluate(()=>window.__bingbong.frame.state==='away'));await visit(page,'halo');await page.locator('[data-touch]').click();check('Acknowledging clears halo',await page.evaluate(()=>window.__bingbong.frame.halo===0));
await visit(page,'object');await page.locator('[data-rear]').click();check('Rear view reveals charging pads',await page.evaluate(()=>window.__bingbong.frame.rx>2.5));
await visit(page,'pet');await page.keyboard.press('Tab');check('Audio silent by default',await page.locator('#sound-toggle').getAttribute('aria-pressed')==='false');await page.locator('#sound-toggle').click();check('Sound needs explicit toggle',await page.locator('#sound-toggle').getAttribute('aria-pressed')==='true');
await context.close();

const touch=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,colorScheme:'dark',reducedMotion:'reduce'});const tp=await touch.newPage();await tp.goto(base);await tp.waitForFunction(()=>window.__bingbong);await tp.evaluate(()=>window.__bingbong.start());await tp.waitForFunction(()=>window.__bingbong?.scene);await visit(tp,'pet');await tp.locator('[data-turn="1"]').tap();check('Touch detent button',await tp.evaluate(()=>Math.abs(window.__bingbong.frame.crown-Math.PI/12)<1e-5));
const touchBox=await tp.locator('#crown-target').boundingBox();const cdp=await touch.newCDPSession(tp);const start={x:touchBox.x+24,y:touchBox.y+24};const before=await tp.evaluate(()=>window.__bingbong.frame.crown);await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[start]});await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:start.x+30,y:start.y}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});check('Touch crown drag',await tp.evaluate(a=>window.__bingbong.frame.crown>a,before));await touch.close();

for(const width of [360,390,820,1440]){const plain=await browser.newContext({viewport:{width,height:900},javaScriptEnabled:false,colorScheme:'dark'});const p=await plain.newPage();await p.goto(base);check(`No-JS content ${width}`,await p.locator('section').count()===chapters.length&&await p.locator('.section-still').count()===chapters.length);check(`No-JS no overflow ${width}`,await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));if(width===390||width===1440)await p.screenshot({path:`qa/screens/${width}-no-js.png`,fullPage:true});await plain.close();}

// Frame measurements are this browser/machine, not a claimed mid-range physical device.
for(const [width,height]of[[1440,900],[390,844]]){const perf=await browser.newContext({viewport:{width,height},colorScheme:'dark'});const p=await perf.newPage();await p.goto(base);await p.waitForFunction(()=>window.__bingbong);await p.evaluate(()=>window.__bingbong.start());await p.waitForFunction(()=>window.__bingbong?.scene);await visit(p,'pet');const timing=await p.evaluate(()=>new Promise(resolve=>{const samples=[];let previous=performance.now(),frames=0;const run=now=>{samples.push(now-previous);previous=now;scrollBy(0,2);if(++frames<120)requestAnimationFrame(run);else{samples.shift();samples.sort((a,b)=>a-b);resolve({fps:1000/(samples.reduce((a,b)=>a+b,0)/samples.length),p95:samples[Math.floor(samples.length*.95)],frames:samples.length});}};requestAnimationFrame(run);}));check(`Scroll frame sample ${width}`,timing.fps>=(width===390?30:55),timing);await perf.close();}

check('No browser exceptions',report.errors.length===0,report.errors);
await writeFile('qa/results.json',JSON.stringify(report,null,2));await browser.close();
// Overview sheets make human inspection of every state and viewport tractable.
for(const width of [390,820,1440,1920])for(const theme of ['dark','light'])for(const motion of ['no-preference','reduce']){
  const thumbWidth=width<700?195:288;const items=[];let thumbHeight=0;
  for(let i=0;i<chapters.length;i++){const input=await sharp(`qa/screens/${width}-${theme}-${motion}-${chapters[i]}.png`).resize({width:thumbWidth}).png().toBuffer({resolveWithObject:true});thumbHeight=input.info.height;items.push({input:input.data,left:(i%5)*thumbWidth,top:Math.floor(i/5)*thumbHeight});}
  await sharp({create:{width:thumbWidth*5,height:thumbHeight*Math.ceil(chapters.length/5),channels:4,background:'#080b13'}}).composite(items).png().toFile(`qa/screens/overview-${width}-${theme}-${motion}.png`);
}
const failures=report.checks.filter(check=>!check.pass);console.log(`QA complete: ${report.checks.length-failures.length}/${report.checks.length} checks passed; ${report.screens.length} chapter screenshots.`);if(failures.length)process.exitCode=1;

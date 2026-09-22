import {chromium} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import {mkdir,writeFile} from 'node:fs/promises';
import {parts,studies} from '../src/assembly-data.js';

const browser=await chromium.launch({channel:'chrome',headless:true});
const base=process.env.QA_URL||'http://127.0.0.1:4173',checks=[],errors=[];
const check=(name,pass,details)=>{checks.push({name,pass,details});console.log(`${pass?'PASS':'FAIL'} ${name}`,details??'');};
await mkdir('qa/assembly',{recursive:true});
const visit=async(page,id)=>{await page.evaluate(id=>document.getElementById(id).scrollIntoView({behavior:'instant'}),id);await page.waitForFunction(()=>Math.abs(window.__bingbong.frame.scroll-scrollY)<.1);await page.waitForTimeout(200);};

for(const width of [1440,390]){
 const context=await browser.newContext({viewport:{width,height:width===390?844:1000},serviceWorkers:'block',reducedMotion:'reduce'}),page=await context.newPage();
 const requests=[];page.on('request',r=>requests.push(r.url()));page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base);await page.waitForFunction(()=>document.documentElement.dataset.ready==='true');
 check(`Assembly code stays out of the first view ${width}`,!requests.some(url=>url.includes('assembly-model'))&&!await page.evaluate(()=>Boolean(window.__bingbong.scene.assembly)));
 await visit(page,'inside');await page.waitForFunction(()=>document.documentElement.dataset.assemblyReady==='true');
 for(const id of Object.keys(studies)){
  if(width===390&&id==='assembly')continue; // Compact build console; parts are explored in preceding studies.
  await visit(page,id);let selections=true;
  for(const part of studies[id]){
   await page.locator(`#${id} [data-part="${part}"]`).click();
   selections&&=await page.locator(`#part-info-${id}>h3`).textContent()===parts[part].name;
   selections&&=await page.evaluate(part=>window.__bingbong.scene.assembly.selected===part,part);
  }
  check(`Every ${id} component reveals its manufacturing and fitting notes ${width}`,selections);
 }
 await visit(page,'inside');
 await page.locator('#inside [data-part="shell"]').click();
 const point=await page.evaluate(()=>{const p=window.__bingbong.scene.assembly.anchor('board'),scale=innerWidth/(innerWidth<700?122:180);return{x:innerWidth/2+p.x*scale,y:innerHeight/2-p.y*scale};});
 await page.mouse.click(point.x,point.y);
 check(`Clicking the actual circuit-board mesh selects it ${width}`,await page.locator('#inside [data-part="board"]').getAttribute('aria-pressed')==='true');

 await visit(page,'detents');
 const snapshot=()=>page.evaluate(()=>{const a=window.__bingbong.scene.assembly;return{angle:a.parts.race.meshes[0].rotation.x,ball:a.parts.balls.meshes[0].position.y,leaf:Array.from(a.parts.leaves.meshes[0].geometry.attributes.position.array),sleeve:a.parts.sleeve.group.rotation.x};});
 const first=await snapshot();await page.locator('[data-detent-step="1"]').click();await page.waitForTimeout(80);const clicked=await snapshot();
 check(`Reduced-motion detent advances exactly one click ${width}`,Math.abs(clicked.angle-first.angle-Math.PI/12)<.00001&&Math.abs(clicked.ball-first.ball)<.00001&&clicked.sleeve===first.sleeve);
 await page.emulateMedia({reducedMotion:'no-preference'});
 await page.locator('[data-detent-step="1"]').click();await page.waitForTimeout(420);const halfway=await snapshot();await page.waitForTimeout(700);const settled=await snapshot();
 const leafDelta=Math.max(...halfway.leaf.map((p,i)=>Math.abs(p-clicked.leaf[i])));
 check(`Both race rotation and spring deflection animate between seats ${width}`,halfway.angle>clicked.angle&&halfway.angle<settled.angle&&Math.abs(halfway.ball-clicked.ball)>.04&&leafDelta>.04,{radialTravel:Math.abs(halfway.ball-clicked.ball),leafDelta,angles:[clicked.angle,halfway.angle,settled.angle]});
 check(`Balls return to their seated radius and the sleeve stays fixed ${width}`,Math.abs(settled.ball-clicked.ball)<.00001&&settled.sleeve===0);
 await page.locator('[data-detent-step="-1"]').click();await page.waitForTimeout(1000);
 check(`Reverse detent returns to the preceding groove ${width}`,Math.abs((await snapshot()).angle-clicked.angle)<.00001);
 await page.emulateMedia({reducedMotion:'reduce'});
 const accessibility=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();
 check(`Assembly controls pass axe checks ${width}`,accessibility.violations.length===0,accessibility.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)})));

 await visit(page,'antenna');await page.locator('[data-feed-pulse]').click();
 const peaks=await page.evaluate(()=>new Promise(resolve=>{const peaks=Object.fromEntries(['board','contact','feed','cap'].map(id=>[id,{value:0,time:0}])),start=performance.now();function tick(now){for(const id in peaks){const value=Math.max(...window.__bingbong.scene.assembly.parts[id].meshes.map(m=>m.material.emissiveIntensity??0));if(value>peaks[id].value)peaks[id]={value,time:now-start};}if(now-start<3350)requestAnimationFrame(tick);else resolve(peaks);}requestAnimationFrame(tick);}));
 check(`Electrical trace visits board, spring, land and cap in order ${width}`,Object.values(peaks).every(p=>p.value>.5)&&peaks.board.time<peaks.contact.time&&peaks.contact.time<peaks.feed.time&&peaks.feed.time<peaks.cap.time,peaks);
 await visit(page,'assembly');
 await page.locator('#build-progress').fill('0');await page.waitForTimeout(60);
 const positions=()=>page.evaluate(()=>Object.fromEntries(Object.entries(window.__bingbong.scene.assembly.parts).map(([id,p])=>[id,p.group.position.toArray()])));
 const loose=await positions();await page.locator('#build-progress').fill('35');await page.waitForTimeout(60);const partway=await positions();
 check(`Assembly seats crown before electronics and rear door ${width}`,Math.hypot(...partway.crown)<.001&&Math.hypot(...partway.board)>5&&Math.hypot(...partway.lid)>30);
 await page.locator('#build-progress').fill('100');await page.waitForTimeout(60);const closed=await positions();
 check(`Every exploded component returns to the assembled datums ${width}`,Object.values(closed).every(p=>Math.hypot(...p)<.001),{looseDoor:loose.lid,closedDoor:closed.lid});
 const contactFit=await page.evaluate(()=>{const a=window.__bingbong.scene.assembly,finger=a.parts.contact.group.getObjectByName('vertical-deflection-contact').geometry,land=a.parts.feed.meshes[0];finger.computeBoundingBox();land.geometry.computeBoundingBox();return{fingerTop:finger.boundingBox.max.z,landFace:land.geometry.boundingBox.min.z+land.position.z};});
 check(`Seated spring touches the land without penetrating it ${width}`,Math.abs(contactFit.fingerTop-contactFit.landFace)<.002&&Math.abs(contactFit.landFace-1.8-1.4)<.002,contactFit);
 await page.locator('#build-progress').focus();await page.keyboard.press('ArrowLeft');
 check(`Assembly scrubber works from the keyboard ${width}`,await page.locator('#build-progress').inputValue()==='99'&&(await page.locator('#build-progress').getAttribute('aria-valuetext')).startsWith('99%'));
 await page.locator('[data-build-reset]').click();await page.waitForTimeout(100);
 check(`Reduced-motion reset restores the exploded layout ${width}`,await page.locator('#build-progress').inputValue()==='0'&&Math.hypot(...(await positions()).lid)>30);
 await page.emulateMedia({reducedMotion:'no-preference'});await page.locator('[data-build-play]').click();await page.waitForTimeout(1300);
 const playing=Number(await page.locator('#build-progress').inputValue());await page.locator('[data-build-play]').click();await page.waitForTimeout(300);
 check(`Build playback advances and pauses ${width}`,playing>5&&playing<25&&Number(await page.locator('#build-progress').inputValue())===playing);
 await page.locator('#build-progress').fill('100');await page.locator('[data-build-play]').click();await page.waitForTimeout(350);
 const rewinding=Number(await page.locator('#build-progress').inputValue());await page.locator('[data-build-play]').click();
 check(`Replaying a finished build rewinds smoothly ${width}`,rewinding>60&&rewinding<99,rewinding);
 await visit(page,'antenna');await visit(page,'assembly');
 await page.evaluate(()=>{const s=document.getElementById('assembly');scrollTo({top:s.offsetTop+(s.offsetHeight-innerHeight)*.5,behavior:'instant'});});await page.waitForTimeout(900);
 check(`Native scroll drives the assembly without touching the slider ${width}`,Math.abs(Number(await page.locator('#build-progress').inputValue())-50)<=1);
 const controller=await page.locator('#build-progress').evaluate(el=>{const r=el.getBoundingClientRect();return{top:r.top,bottom:r.bottom,hit:document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===el};});
 check(`Build controller remains visible and pointer-accessible during scroll ${width}`,controller.hit&&controller.top>0&&controller.bottom<(width===390?844:1000),controller);
 await page.evaluate(()=>{const s=document.getElementById('assembly');scrollTo({top:s.offsetTop+s.offsetHeight-innerHeight,behavior:'instant'});});await page.waitForTimeout(900);
 check(`End of the assembly scroll finishes the object ${width}`,await page.locator('#build-progress').inputValue()==='100'&&Object.values(await positions()).every(p=>Math.hypot(...p)<.001));
 await visit(page,'inside');
 const timing=await page.evaluate(()=>new Promise(resolve=>{const samples=[];let previous=performance.now();function tick(now){samples.push(now-previous);previous=now;if(samples.length<121)requestAnimationFrame(tick);else{samples.shift();samples.sort((a,b)=>a-b);resolve({fps:1000/(samples.reduce((a,b)=>a+b,0)/samples.length),p95:samples[Math.floor(samples.length*.95)]});}}requestAnimationFrame(tick);}));
 check(`Exploded assembly frame sample ${width}`,timing.fps>=(width===390?30:55),timing);
 await context.close();
}

const plain=await browser.newPage({viewport:{width:390,height:844},javaScriptEnabled:false});await plain.goto(base);
for(const id of Object.keys(studies)){
 await plain.locator('#'+id).scrollIntoViewIfNeeded();
 const bitmap=plain.locator(`#${id} .section-still`);await bitmap.scrollIntoViewIfNeeded();await bitmap.evaluate(img=>img.decode());
 check(`No-JS ${id} has a complete static illustration and component notes`,await bitmap.evaluate(img=>img.naturalWidth>0)&&await plain.locator(`#${id} .static-component-notes details`).count()===studies[id].length-1);
}
await plain.close();await browser.close();check('No assembly browser exceptions',errors.length===0,errors);
await writeFile('qa/assembly/results.json',JSON.stringify({date:new Date().toISOString(),checks,errors},null,2));if(checks.some(c=>!c.pass))process.exitCode=1;

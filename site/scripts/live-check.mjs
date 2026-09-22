import {chromium} from '@playwright/test';
import {mkdir,writeFile} from 'node:fs/promises';
const browser=await chromium.launch({channel:'chrome',headless:true});
const results=[],errors=[];const check=(name,pass,details)=>{results.push({name,pass,details});console.log(`${pass?'PASS':'FAIL'} ${name}`);};
const page=await browser.newPage({viewport:{width:1440,height:900},serviceWorkers:'block'});page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:4173');await page.waitForFunction(()=>window.__bingbong?.scene);await page.waitForTimeout(500);
check('WebGL starts without a click or scroll',await page.evaluate(()=>document.documentElement.dataset.ready==='true'&&scrollY===0));
check('Normal experience displays a canvas, not a product still',await page.evaluate(()=>getComputedStyle(document.querySelector('.hero-still')).display==='none'&&document.querySelector('canvas').width>1000));
let before=await page.evaluate(()=>window.__bingbong.scene.main.group.rotation.toArray());const first=await page.screenshot();await page.waitForTimeout(450);const second=await page.screenshot();
check('Live object moves at rest and renders different pixels',!first.equals(second)&&await page.evaluate(a=>window.__bingbong.scene.main.group.rotation.x!==a[0],before));
await page.mouse.move(730,530);await page.mouse.down();await page.mouse.move(850,565,{steps:12});await page.mouse.up();await page.waitForTimeout(550);
check('Dragging the product rotates the actual model',await page.evaluate(()=>window.__bingbong.scene.orbit.y>.7&&window.__bingbong.scene.orbit.x>.1));
await page.locator('[data-reset-view]').click();await page.waitForTimeout(600);check('Reset returns to the chapter composition',await page.evaluate(()=>window.__bingbong.scene.orbit.x===0&&window.__bingbong.scene.orbit.y===0));
await page.locator('[data-orbit="1"]').focus();await page.keyboard.press('Enter');check('Keyboard can rotate the product',await page.evaluate(()=>window.__bingbong.scene.orbit.y>.5));
await page.locator('[data-reset-view]').click();
await page.evaluate(()=>document.querySelector('#object').scrollIntoView({behavior:'instant'}));await page.waitForTimeout(700);
before=await page.evaluate(()=>window.__bingbong.scene.main.group.rotation.x);await page.locator('[data-rear]').click();await page.waitForTimeout(90);const midway=await page.evaluate(()=>window.__bingbong.scene.main.group.rotation.x);await page.waitForTimeout(850);const end=await page.evaluate(()=>window.__bingbong.scene.main.group.rotation.x);
check('Turn-over animates through intermediate geometry',midway>before+.05&&midway<end-.1&&end>2.7,{before,midway,end});
// Leaving an asynchronous demonstration cancels it; re-entering is always usable.
await page.evaluate(()=>document.querySelector('#boop').scrollIntoView({behavior:'instant'}));await page.waitForTimeout(750);await page.locator('#boop details summary').click();await page.locator('[data-cold]').click();await page.evaluate(()=>document.querySelector('#quiet').scrollIntoView({behavior:'instant'}));await page.waitForTimeout(750);await page.evaluate(()=>document.querySelector('#boop').scrollIntoView({behavior:'instant'}));await page.waitForTimeout(750);
check('Leaving a cold demo never strands a disabled control',await page.locator('[data-boop]').isEnabled()&&await page.locator('[data-cold]').isEnabled());
await page.evaluate(()=>document.querySelector('#hello').scrollIntoView({behavior:'instant'}));await page.waitForTimeout(700);
await page.evaluate(()=>{window.__lostContext=window.__bingbong.scene.renderer.getContext().getExtension('WEBGL_lose_context');window.__lostContext.loseContext();});await page.waitForFunction(()=>document.body.classList.contains('no-webgl'));
check('Context loss preserves a readable product fallback',await page.locator('h1').isVisible()&&await page.locator('.hero-still').isVisible());
await page.evaluate(()=>window.__lostContext.restoreContext());await page.waitForFunction(()=>!document.body.classList.contains('no-webgl'));await page.waitForTimeout(500);
check('Context recovery restores the live scene',await page.locator('#scene-canvas').isVisible());await page.screenshot({path:'qa/redesign/context-recovered.png'});
await page.emulateMedia({reducedMotion:'reduce'});await page.waitForTimeout(200);before=await page.evaluate(()=>window.__bingbong.scene.main.group.matrixWorld.toArray());await page.waitForTimeout(600);
check('Reduced motion completely stops ambient model movement',await page.evaluate(a=>window.__bingbong.scene.main.group.matrixWorld.toArray().every((v,i)=>v===a[i]),before));
await page.locator('[data-orbit="-1"]').click();await page.waitForTimeout(100);check('Reduced motion retains manual rotation',await page.evaluate(()=>window.__bingbong.scene.orbit.y<-.5));
await page.close();
// An actual touch stream must scroll vertically and rotate horizontally.
const mobile=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,serviceWorkers:'block',reducedMotion:'reduce'});const touch=await mobile.newPage();touch.on('pageerror',e=>errors.push(e.message));await touch.goto('http://127.0.0.1:4173');await touch.waitForFunction(()=>window.__bingbong?.scene);await touch.evaluate(()=>document.querySelector('#hold').scrollIntoView({behavior:'instant'}));await touch.waitForTimeout(300);
await touch.locator('[data-hold]').tap();check('Mobile controls remain reachable below the canvas',await touch.locator('[data-hold]').isVisible());
const cdp=await mobile.newCDPSession(touch);await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:195,y:210}]});for(let i=1;i<=6;i++)await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:195+i*10,y:210}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await touch.waitForTimeout(150);
check('Horizontal touch drag rotates the product',await touch.evaluate(()=>window.__bingbong.scene.orbit.y>.25));
const scrollBefore=await touch.evaluate(()=>scrollY);await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:195,y:210}]});for(let i=1;i<=6;i++)await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:195,y:210-i*15}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await touch.waitForTimeout(400);
check('Vertical swiping the object still scrolls the page',await touch.evaluate(y=>scrollY>y+20,scrollBefore));
const labels=[];
for(const id of ['pet','hold','pet','inside']){
  await touch.evaluate(id=>document.querySelector('#'+id).scrollIntoView({behavior:'instant'}),id);
  await touch.waitForFunction(id=>window.__bingbong.chapter===Number(document.querySelector('#'+id).dataset.index),id);await touch.waitForTimeout(100);
  labels.push({id,opacity:await touch.locator('.pair-label').evaluateAll(nodes=>nodes.map(node=>Number(getComputedStyle(node).opacity)))});
}
check('Instant reduced-motion navigation clears and restores pair labels',labels.every(({id,opacity})=>opacity.every(value=>id==='pet'?value>.99:value<.01)),labels);
for(const width of [360,390,820,1440,1920]){await touch.setViewportSize({width,height:width>1000?900:844});await touch.evaluate(()=>document.querySelector('#size').scrollIntoView({behavior:'instant'}));await touch.waitForTimeout(300);const data=await touch.evaluate(()=>{const model=window.__bingbong.scene.main.group;const rule=document.querySelector('.size-rule').getBoundingClientRect();return{center:rule.x+rule.width/2,expected:innerWidth*(innerWidth<700?.5:.7),width:rule.width,overflow:document.documentElement.scrollWidth>innerWidth};});check(`Scale rule and viewport agree at ${width}`,Math.abs(data.center-data.expected)<1&&Math.abs(data.width-359.055)<.1&&!data.overflow,data);}
await mobile.close();check('No exceptions in live/drag/context/touch checks',errors.length===0,errors);await browser.close();await mkdir('qa/redesign',{recursive:true});await writeFile('qa/redesign/live-results.json',JSON.stringify(results,null,2));if(results.some(r=>!r.pass))process.exitCode=1;

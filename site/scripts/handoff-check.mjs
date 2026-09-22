/** Clean-checkout smoke test. Existing full QA reports remain untouched. */
import {chromium} from '@playwright/test';
import {readFile,writeFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';

const base=process.env.QA_URL||'http://127.0.0.1:4173';
const report={date:new Date().toISOString(),base,node:process.version,lockfileSha256:createHash('sha256').update(await readFile('package-lock.json')).digest('hex'),setup:['npm ci','npm run build','npm run artifact'],checks:[],errors:[]};
const check=(name,pass,details)=>{report.checks.push({name,pass,details});console.log(`${pass?'PASS':'FAIL'} ${name}`);};
const browser=await chromium.launch({channel:'chrome',headless:true});
try{
  for(const width of [1440,390]){
    const context=await browser.newContext({viewport:{width,height:width===390?844:900},reducedMotion:'reduce',serviceWorkers:'block'});
    const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));
    await page.goto(base);await page.waitForFunction(()=>document.documentElement.dataset.ready==='true');
    check(`Live model and fifteen chapters ${width}`,await page.evaluate(()=>Boolean(window.__bingbong.scene)&&document.querySelectorAll('.story-section').length===15));
    check(`Detailed assembly stays out of the hero ${width}`,await page.evaluate(()=>!window.__bingbong.scene.assembly));
    const visit=async(id,index)=>{await page.evaluate(id=>document.querySelector('#'+id).scrollIntoView({behavior:'instant'}),id);await page.waitForFunction(index=>window.__bingbong.chapter===index,index);await page.waitForFunction(()=>document.documentElement.dataset.assemblyReady==='true');await page.waitForTimeout(120);};
    await visit('inside',10);
    const count=await page.evaluate(()=>Object.keys(window.__bingbong.scene.assembly.parts).length);
    check(`Twenty component groups load ${width}`,count===20,{count});
    await page.locator('#inside [data-part="board"]').click();
    check(`Component selection updates model and notes ${width}`,await page.evaluate(()=>window.__bingbong.scene.assembly.selected==='board')&&await page.locator('#part-info-inside h3').textContent()==='Main circuit board');
    await visit('detents',12);await page.locator('[data-detent-step="1"]').click();
    check(`Ceramic detent advances 15 degrees ${width}`,await page.evaluate(()=>Math.abs(window.__bingbong.assemblyUI.state.angle-Math.PI/12)<1e-6));
    await visit('assembly',14);await page.locator('#build-progress').fill('100');await page.waitForTimeout(150);
    check(`Assembly control reaches the complete build ${width}`,await page.evaluate(()=>window.__bingbong.frame.buildProgress===1&&document.querySelector('#build-percent').textContent==='100%'));
    check(`No horizontal overflow ${width}`,await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    await context.close();
  }
  const artifact=await browser.newPage({viewport:{width:1440,height:900},reducedMotion:'reduce'}),external=[];
  artifact.on('pageerror',e=>report.errors.push(e.message));artifact.on('request',r=>{if(/^https?:/.test(r.url()))external.push(r.url());});
  await artifact.goto(pathToFileURL(resolve('artifact/bingbong.html')).href);await artifact.waitForFunction(()=>document.documentElement.dataset.ready==='true');
  await artifact.evaluate(()=>document.querySelector('#antenna').scrollIntoView({behavior:'instant'}));await artifact.waitForFunction(()=>document.documentElement.dataset.assemblyReady==='true');
  check('Rebuilt standalone file runs its antenna assembly',await artifact.evaluate(()=>Boolean(window.__bingbong.scene.assembly.parts.contact)));
  check('Standalone makes no network requests',external.length===0,external);
  await artifact.close();check('No browser exceptions',report.errors.length===0,report.errors);
}finally{await browser.close();await writeFile('qa/handoff-check.json',JSON.stringify(report,null,2)+'\n');}
if(report.checks.some(c=>!c.pass))process.exitCode=1;

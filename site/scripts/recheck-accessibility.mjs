import {chromium} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import {readFile,writeFile} from 'node:fs/promises';
const report=JSON.parse(await readFile('qa/results.json','utf8'));
const browser=await chromium.launch({channel:'chrome',headless:true});
for(const width of [390,1440])for(const theme of ['dark','light']){
 const context=await browser.newContext({viewport:{width,height:900},colorScheme:theme,reducedMotion:'reduce'});const page=await context.newPage();await page.goto('http://127.0.0.1:4173');await page.waitForFunction(()=>window.__bingbong?.scene);
 const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','best-practice']).analyze();const item=report.checks.find(c=>c.name===`axe ${width}/${theme}`);item.pass=result.violations.length===0;item.details=result.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)}));item.rechecked=new Date().toISOString();const evidence=report.a11y.find(a=>a.width===width&&a.theme===theme&&!a.chapter);evidence.violations=result.violations;console.log(`${item.pass?'PASS':'FAIL'} ${item.name}`);await context.close();
}
report.accessibilityRecheck='View controls now use a named region. Rechecked the four failing hero audits; other checks and screenshots are unchanged.';
await browser.close();await writeFile('qa/results.json',JSON.stringify(report,null,2));if(report.checks.some(c=>!c.pass))process.exitCode=1;

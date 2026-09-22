import lighthouse from 'lighthouse';
import { chromium } from '@playwright/test';
import { writeFile } from 'node:fs/promises';
// Playwright owns Chrome's lifecycle so Windows file locks don't turn report cleanup into failure.
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--remote-debugging-port=9224']});
try{
  const result=await lighthouse('http://127.0.0.1:4173',{port:9224,output:['json','html'],onlyCategories:['performance','accessibility','best-practices'],logLevel:'error'});
  await writeFile('qa/lighthouse-mobile.report.json',result.report[0]);await writeFile('qa/lighthouse-mobile.report.html',result.report[1]);
  console.log(JSON.stringify({scores:Object.fromEntries(Object.entries(result.lhr.categories).map(([key,value])=>[key,value.score*100])),metrics:Object.fromEntries(['first-contentful-paint','largest-contentful-paint','total-blocking-time','cumulative-layout-shift','interactive','total-byte-weight'].map(key=>[key,result.lhr.audits[key].displayValue]))},null,2));
}finally{await browser.close();}

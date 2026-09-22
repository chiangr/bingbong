import {chromium}from'@playwright/test';import{mkdir}from'node:fs/promises';
const pass=process.argv[2]||'02-scroll';await mkdir(`qa/passes/${pass}`,{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});const page=await browser.newPage({colorScheme:'dark'});const errors=[];page.on('pageerror',e=>errors.push(e.message));
for(const[width,height]of[[390,844],[820,1180],[1440,900]]){await page.setViewportSize({width,height});await page.goto('http://127.0.0.1:5173/');await page.waitForFunction(()=>document.documentElement.dataset.ready);await page.evaluate(()=>window.__bingbong.start());await page.waitForTimeout(400);await page.screenshot({path:`qa/passes/${pass}/${width}.png`});}
console.log(JSON.stringify({pass,errors}));await browser.close();

import { chromium } from '@playwright/test';
import { writeFile,mkdir } from 'node:fs/promises';
import sharp from 'sharp';
import { poses } from '../src/timeline.js';
const names=['hello','pet','boop','hold','creature','halo','object','quiet','size','details','inside','crown','detents','antenna','assembly'];
const metadata={};
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--enable-webgl','--ignore-gpu-blocklist']});
const page=await browser.newPage({viewport:{width:1200,height:1100},deviceScaleFactor:1});
await page.goto('http://127.0.0.1:5173/render-lab.html');await page.waitForSelector('body[data-ready="true"]');
await page.addStyleTag({content:'h1,p,.mascot{display:none!important}html,body{background:transparent!important}'});
for(let i=0;i<names.length;i++){
  if(i===10)await page.evaluate(()=>window.scene.prepareAssembly());
  await page.evaluate(({pose,study})=>{window.scene.setFrame({...pose,screenLevel:Number(pose.screen),cx:.5,cy:pose.pair?.31:.5,scale:study?pose.scale*1.3:pose.pair?1.12:1.48,otherCx:.5,otherCy:.70,otherScale:1.02,reduced:true});window.scene.draw(performance.now());},{pose:poses[i],study:i>=10});await page.waitForTimeout(80);
  const data=await page.evaluate(()=>window.scene.renderer.domElement.toDataURL('image/png'));
  const buffer=Buffer.from(data.split(',')[1],'base64');await sharp(buffer).webp({quality:88,alphaQuality:90}).toFile(`public/renders/${names[i]}.webp`);
  metadata[names[i]]={width:1200,height:1100,crown:await page.evaluate(()=>window.scene.projectCrown())};
}
await page.setViewportSize({width:390,height:363});await page.waitForTimeout(100);
for(let i=0;i<names.length;i++){
  const pose={...poses[i],screenLevel:Number(poses[i].screen),cx:.5,cy:poses[i].pair?.28:.5,scale:i>=10?[.72,1.18,5.7,1.4,.72][i-10]:poses[i].pair?.85:1.1,otherCx:.5,otherCy:.7,otherScale:.78,reduced:true};
  await page.evaluate(pose=>{window.scene.setFrame(pose);window.scene.draw(performance.now());},pose);await page.waitForTimeout(50);
  const data=await page.evaluate(()=>window.scene.renderer.domElement.toDataURL('image/png'));await sharp(Buffer.from(data.split(',')[1],'base64')).webp({quality:90}).toFile(`public/renders/${names[i]}-mobile.webp`);
  metadata[`${names[i]}-mobile`]={width:390,height:363,crown:await page.evaluate(()=>window.scene.projectCrown())};
}
await writeFile('src/render-frames.json',JSON.stringify(metadata));
await page.setViewportSize({width:1200,height:1100});
await page.evaluate(()=>window.scene.setFrame({rx:-.32,ry:-.28,rz:-.22,scale:1.48,cx:.5,cy:.5,halo:.2,screen:true,state:'resting',reduced:true}));
await page.waitForTimeout(100);const final=await page.evaluate(()=>{window.scene.draw(performance.now());return window.scene.renderer.domElement.toDataURL('image/png');});await writeFile('qa/render-final.png',Buffer.from(final.split(',')[1],'base64'));await browser.close();
console.log('15 canonical model stills generated from the procedural model.');

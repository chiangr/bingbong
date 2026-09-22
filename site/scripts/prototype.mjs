import { chromium } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
import sharp from 'sharp';
import { mascotSvg, mascotGroup, states } from '../src/components/mascot.js';
await mkdir('qa/passes/01-render',{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--enable-webgl','--ignore-gpu-blocklist']});
const page=await browser.newPage({viewport:{width:1440,height:900},deviceScaleFactor:1});
page.on('pageerror',e=>console.error(e));
for(const [width,height] of [[390,844],[820,1180],[1440,900]]) {
  await page.setViewportSize({width,height});await page.goto('http://127.0.0.1:5173/render-lab.html');await page.waitForSelector('body[data-ready="true"]');await page.waitForTimeout(700);await page.screenshot({path:`qa/passes/01-render/${width}.png`});
}
const nativeSheet=`<svg xmlns="http://www.w3.org/2000/svg" width="1008" height="334" viewBox="0 0 1008 334"><rect width="1008" height="334" fill="#120f0d"/>${states.map((state,i)=>`<g transform="translate(${i*126} 20)"><text x="63" y="-6" text-anchor="middle" font-size="10" font-family="Arial" fill="#efe7dd">${state}</text><g transform="translate(126 0) rotate(90)"><rect width="294" height="126" fill="#000"/>${mascotGroup(state)}</g></g>`).join('')}</svg>`;
const landscapeSheet=`<svg xmlns="http://www.w3.org/2000/svg" width="620" height="664" viewBox="0 0 620 664"><rect width="620" height="664" fill="#120f0d"/>${states.map((state,i)=>`<g transform="translate(${16+i%2*310} ${30+Math.floor(i/2)*164})"><text y="-9" font-size="12" font-family="Arial" fill="#efe7dd">${state} · 294 × 126</text><rect width="294" height="126" fill="#000"/>${mascotGroup(state)}</g>`).join('')}</svg>`;
await writeFile('public/mascot/native-preview.svg',nativeSheet);await sharp(Buffer.from(nativeSheet)).png().toFile('public/mascot/native-preview.png');
await writeFile('public/mascot/landscape-preview.svg',landscapeSheet);await sharp(Buffer.from(landscapeSheet)).png().toFile('public/mascot/landscape-preview.png');
for(const state of states)await writeFile(`public/mascot/${state}.svg`,mascotSvg(state));
const groupSheet=`<svg xmlns="http://www.w3.org/2000/svg" width="294" height="126" viewBox="0 0 294 126"><style>.mascot-state{display:none}.mascot-state:target{display:inline}svg:not(:has(:target)) #resting{display:inline}</style><rect width="294" height="126" fill="#000"/>${states.map(s=>mascotGroup(s)).join('')}</svg>`;
await writeFile('public/mascot/states.svg',groupSheet);
await browser.close();console.log('Prototype screenshots and mascot package captured.');

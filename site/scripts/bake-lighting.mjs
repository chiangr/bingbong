import {chromium} from '@playwright/test';
import {mkdir,writeFile} from 'node:fs/promises';
import sharp from 'sharp';
const browser=await chromium.launch({channel:'chrome',headless:true});
try{
 const page=await browser.newPage({viewport:{width:640,height:480}});
 await page.goto('http://127.0.0.1:5173/render-lab.html?bake=1');await page.waitForSelector('body[data-ready="true"]');
 const data=await page.evaluate(async()=>{const{DataUtils}=await import('/node_modules/three/build/three.module.js');const{renderer,environment}=window.scene;const{width,height}=environment.texture.image;const pixels=new Uint16Array(width*height*4);await renderer.readRenderTargetPixelsAsync(environment,0,0,width,height,pixels);const bytes=new Uint8Array(pixels.length);for(let i=0;i<pixels.length;i++)bytes[i]=i%4===3?255:Math.min(255,Math.round(DataUtils.fromHalfFloat(pixels[i])/4*255));let binary='';for(let i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode(...bytes.subarray(i,i+8192));return{width,height,base64:btoa(binary)};});
 await mkdir('public/lighting',{recursive:true});await sharp(Buffer.from(data.base64,'base64'),{raw:{width:data.width,height:data.height,channels:4}}).png().toFile('public/lighting/studio-cubeuv.png');
 await writeFile('public/lighting/README.md',`# Studio environment\n\nA prefiltered CubeUV lighting map from the softbox scene in src/components/studio.js. Not a product image: the model is rendered live using these reflection samples.\n\n${data.width} × ${data.height}; linear RGB; radiance divided by 4 for PNG storage; flipY false. The renderer restores the scale through material environment intensity. Rebuild with npm run dev followed by node scripts/bake-lighting.mjs.\n`);
 console.log(`Lighting baked: ${data.width} × ${data.height}.`);
}finally{await browser.close();}

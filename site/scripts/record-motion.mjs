import{chromium}from'@playwright/test';import{mkdir,writeFile}from'node:fs/promises';import{execFile}from'node:child_process';import{promisify}from'node:util';
const exec=promisify(execFile);const browser=await chromium.launch({channel:'chrome',headless:true});const report=[];
for(const[name,width,height,duration]of[['desktop',1440,900,52000],['phone-emulation',390,844,62000]]){
  const directory=`qa/motion/${name}-frames`;await mkdir(directory,{recursive:true});const context=await browser.newContext({viewport:{width,height},colorScheme:'dark'});const page=await context.newPage();await page.goto('http://127.0.0.1:4173');await page.waitForFunction(()=>window.__bingbong?.scene);
  const cdp=await context.newCDPSession(page);const frames=[];cdp.on('Page.screencastFrame',event=>{frames.push({data:event.data,time:event.metadata.timestamp});cdp.send('Page.screencastFrameAck',{sessionId:event.sessionId}).catch(()=>{});});
  await cdp.send('Page.startScreencast',{format:'jpeg',quality:82,maxWidth:width,maxHeight:height,everyNthFrame:1});
  console.log(`Recording ${name} at browser refresh cadence…`);
  await page.evaluate(duration=>new Promise(resolve=>{const start=performance.now(),end=document.documentElement.scrollHeight-innerHeight;function tick(now){const progress=Math.min(1,(now-start)/duration);scrollTo({top:progress*end,behavior:'instant'});if(progress<1)requestAnimationFrame(tick);else resolve();}requestAnimationFrame(tick);}),duration);
  await cdp.send('Page.stopScreencast');await context.close();let concat='';
  for(let i=0;i<frames.length;i++){const filename=String(i).padStart(5,'0')+'.jpg';await writeFile(`${directory}/${filename}`,Buffer.from(frames[i].data,'base64'));concat+=`file '${filename}'\nduration ${i<frames.length-1?Math.max(.001,frames[i+1].time-frames[i].time):1/60}\n`;}
  await writeFile(`${directory}/frames.txt`,concat);await exec('ffmpeg',['-y','-loglevel','error','-f','concat','-safe','0','-i',`${directory}/frames.txt`,'-vf','fps=60','-c:v','libx264','-crf','23','-pix_fmt','yuv420p',`qa/motion/${name}.mp4`]);
  const elapsed=frames.at(-1).time-frames[0].time;report.push({name,width,height,frames:frames.length,captureFps:(frames.length-1)/elapsed,encodedFps:60,seconds:elapsed,note:'CDP capture at native refresh cadence; 60 fps encode preserves timestamps, duplicating when the capture has fewer frames. Phone is emulated, not a physical handset.'});console.log(`${name}: ${frames.length} frames / ${elapsed.toFixed(1)} s`);
}
await browser.close();await writeFile('qa/motion/recordings.json',JSON.stringify(report,null,2));

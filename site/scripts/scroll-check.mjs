import {chromium} from '@playwright/test';
import {mkdir,writeFile} from 'node:fs/promises';
import sharp from 'sharp';

const base=process.env.QA_URL||'http://127.0.0.1:4173';
const browser=await chromium.launch({channel:'chrome',headless:true});
const checks=[],errors=[],screens=[];
const check=(name,pass,details)=>{checks.push({name,pass,details});console.log(`${pass?'PASS':'FAIL'} ${name}`,details??'');};
await mkdir('qa/scroll',{recursive:true});

for(const width of (process.env.SWEEP_ONLY?[1440]:[1440,390]))for(const reducedMotion of (process.env.SWEEP_ONLY?['no-preference']:['no-preference','reduce'])){
  const height=width===390?844:900,label=`${width}/${reducedMotion}`;
  const page=await browser.newPage({viewport:{width,height},reducedMotion,serviceWorkers:'block'});
  page.on('pageerror',error=>errors.push(error.message));
  await page.goto(base);await page.waitForFunction(()=>window.__bingbong?.scene);await page.evaluate(()=>document.fonts.ready);
  const sweep=await page.evaluate(async()=>{
    const raf=()=>new Promise(resolve=>requestAnimationFrame(resolve));
    const span=innerWidth<700?122:180,scale=innerWidth/span;
    const read=()=>{
      const {main}=window.__bingbong.scene,style=getComputedStyle(document.querySelector('#scene-canvas'));
      return {x:main.group.position.x*scale,y:main.group.position.y*scale,
        rx:main.group.rotation.x,ry:main.group.rotation.y,rz:main.group.rotation.z,
        size:main.group.scale.x,
        screen:main.screen.visible?main.screen.material.color.r*main.screen.material.opacity:0,
        halo:main.group.getObjectByName('halo-emission').material.opacity,
        clip:parseFloat(style.clipPath.match(/([-+\d.e]+)%/)?.[1]??0),
        toolbar:parseFloat(getComputedStyle(document.querySelector('.scene-toolbar')).top),
        parts:Object.fromEntries(Object.entries(window.__bingbong.scene.assembly?.parts??{}).filter(([,p])=>p.opacity>.3).map(([id])=>{const p=window.__bingbong.scene.assembly.anchor(id);return[id,[p.x*scale+innerWidth/2,-p.y*scale+innerHeight/2]];})),
        chapter:window.__bingbong.chapter};
    };
    const last=document.querySelector('#assembly'),end=last.offsetTop+last.offsetHeight-innerHeight,max={position:0,rotation:0,size:0,screen:0,halo:0,clip:0,toolbar:0,partTravel:0},boundaries=[],maxContexts={};
    let previous=read(),frames=0;
    async function step(top){
      scrollTo({top,behavior:'instant'});await raf();
      const value=read();frames++;
      const movement={position:Math.hypot(value.x-previous.x,value.y-previous.y),rotation:Math.max(...['rx','ry','rz'].map(k=>Math.abs(value[k]-previous[k])))};
      for(const key of ['screen','halo','clip','toolbar'])movement[key]=Math.abs(value[key]-previous[key]);
      movement.size=Math.abs(value.size-previous.size)/previous.size;
      movement.partTravel=0;
      for(const [id,p]of Object.entries(value.parts)){const q=previous.parts[id];if(q&&p[0]>0&&p[0]<innerWidth&&p[1]>0&&p[1]<innerHeight)movement.partTravel=Math.max(movement.partTravel,Math.hypot(p[0]-q[0],p[1]-q[1]));}
      for(const key in max)if(movement[key]>max[key]){max[key]=movement[key];maxContexts[key]={scroll:scrollY,from:previous.chapter,to:value.chapter,previous:previous[key],current:value[key]};}
      if(value.chapter!==previous.chapter)boundaries.push({from:previous.chapter,to:value.chapter,scroll:scrollY,...movement});
      previous=value;
    }
    for(let y=0;y<=end;y+=12)await step(y);
    for(let i=0;i<45;i++)await step(end);
    for(let y=end;y>=0;y-=12)await step(y);
    for(let i=0;i<45;i++)await step(0);
    return {max,boundaries,frames,maxContexts};
  });
  check(`All chapter crossings traversed in both directions ${label}`,sweep.boundaries.length===28,sweep.boundaries.length);
  check(`Rendered object never jumps between positions ${label}`,sweep.max.position<(width===390?18:40)&&sweep.max.rotation<.075&&sweep.max.size<.055,sweep.max);
  check(`Exploded components follow a continuous path ${label}`,sweep.max.partTravel<(width===390?28:65),sweep.max.partTravel);
  if(process.env.SWEEP_ONLY){console.log('Maximum changes:',JSON.stringify(sweep.maxContexts,null,2));await page.close();continue;}
  check(`Screen and halo fade through chapter boundaries ${label}`,sweep.max.screen<.05&&sweep.max.halo<.05);
  if(width===390)check(`Mobile clipping and controls move continuously ${label}`,sweep.max.clip<2&&sweep.max.toolbar<15);

  const midpoint=await page.evaluate(()=>document.querySelector('#creature').offsetTop-innerHeight*.48);
  const stop=async y=>{await page.evaluate(y=>scrollTo({top:y,behavior:'instant'}),y);await page.waitForFunction(()=>Math.abs(window.__bingbong.frame.scroll-scrollY)<.1);await page.waitForTimeout(250);};
  await stop(midpoint);
  const pose=()=>page.evaluate(()=>{const f=window.__bingbong.frame;return {cx:f.cx,cy:f.cy,scale:f.scale,rx:f.rx,progress:f.progress};});
  const atStop=await pose();await page.waitForTimeout(300);
  check(`Stopping partway retains an intermediate pose ${label}`,JSON.stringify(atStop)===JSON.stringify(await pose())&&atStop.progress>.1&&atStop.progress<.9,atStop);
  await stop(midpoint+150);await stop(midpoint);
  check(`Reversing retraces the same scroll path ${label}`,JSON.stringify(atStop)===JSON.stringify(await pose()));

  if(reducedMotion==='no-preference'){
    // Inspect the actual chapter crossings, not just the settled compositions.
    for(const [name,index] of [['hero',1],['creature',4],['halo',5],['inside',10],['crown',11],['detents',12],['antenna',13],['assembly',14]]){
      const end=await page.evaluate(index=>document.querySelectorAll('.story-section')[index].offsetTop,index);
      for(const fraction of [.25,.5,.75]){
        await stop(end-height*(1-fraction));const file=`${width}-${name}-${fraction}.png`;
        await page.screenshot({path:`qa/scroll/${file}`});screens.push({width,file});
      }
    }
    await stop(0);
    await page.mouse.move(width*.8,height*.85);await page.mouse.wheel(0,500);
    const wheel=await page.evaluate(()=>new Promise(resolve=>{const positions=[];function tick(){positions.push(window.__bingbong.scene.main.group.position.y);if(positions.length<30)requestAnimationFrame(tick);else resolve(positions);}requestAnimationFrame(tick);}));
    check(`A wheel burst produces intermediate rendered positions ${label}`,new Set(wheel.map(y=>y.toFixed(2))).size>12);

    await stop(0);await page.locator('#crown-target').focus();await page.keyboard.press('Enter');
    await page.waitForFunction(()=>window.__bingbong.chapter===2&&window.__bingbong.frame.state==='looking-up',{},{timeout:5000});
    await page.waitForTimeout(2800);
    check(`Hero crown glides to the boop demo and completes it ${label}`,await page.evaluate(()=>window.__bingbong.frame.otherState==='boop'));
  }

  if(width===1440&&reducedMotion==='reduce'){
    const objectTop=await page.evaluate(()=>document.querySelector('#object').offsetTop);
    await stop(objectTop);await page.locator('[data-rear]').click();
    const result=await page.evaluate(async()=>{
      const boundary=document.querySelector('#quiet').offsetTop-innerHeight*.45,frames=[];
      // Establish the inspection pose at the start of this small boundary sweep.
      // The setup jump from the chapter top is not part of the measured gesture.
      scrollTo({top:boundary-100,behavior:'instant'});await new Promise(r=>setTimeout(r,150));
      for(let y=boundary-100;y<=boundary+100;y+=2){scrollTo({top:y,behavior:'instant'});await new Promise(r=>requestAnimationFrame(r));frames.push(window.__bingbong.scene.main.group.rotation.x);}
      for(let y=boundary+100;y>=boundary-100;y-=2){scrollTo({top:y,behavior:'instant'});await new Promise(r=>requestAnimationFrame(r));frames.push(window.__bingbong.scene.main.group.rotation.x);}
      return Math.max(...frames.slice(1).map((v,i)=>Math.abs(v-frames[i])));
    });
    check('Inspected rear view rejoins the path without a boundary reset',result<.05,result);
  }
  await page.close();console.log(`Finished ${label}`);
}

check('No browser errors during scroll, reverse or navigation',errors.length===0,errors);
await browser.close();
for(const width of [1440,390]){
  const thumbs=await Promise.all(screens.filter(s=>s.width===width).map(s=>sharp(`qa/scroll/${s.file}`).resize({width:width===390?195:480}).png().toBuffer({resolveWithObject:true})));
  if(!thumbs.length)continue;
  const w=thumbs[0].info.width,h=thumbs[0].info.height;
  await sharp({create:{width:w*3,height:h*Math.ceil(thumbs.length/3),channels:4,background:'#080b13'}}).composite(thumbs.map((thumb,i)=>({input:thumb.data,left:i%3*w,top:Math.floor(i/3)*h}))).png().toFile(`qa/scroll/overview-${width}.png`);
}
await writeFile(process.env.SWEEP_ONLY?'qa/scroll/diagnostic.json':'qa/scroll/results.json',JSON.stringify({date:new Date().toISOString(),checks,errors},null,2));
if(checks.some(c=>!c.pass))process.exitCode=1;

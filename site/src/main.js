import { createTimeline } from './timeline.js';
import { createInteractions } from './interactions.js';
import { assetUrl } from './assets.js';
import { createAssemblyInteractions } from './assembly-interactions.js';
import { warmGraphics } from './components/graphics-warmup.js';
import { createRFLab } from './rf-lab.js';
import './rf-lab.css';

const body=document.body;body.classList.add('enhanced');
createRFLab();
// Download the renderer and prepare the graphics driver while the page measures
// its scroll track. Neither needs to wait for the first synchronous layout.
const graphicsWarmup=warmGraphics(),sceneModule=import('./components/scene.js');
const stage=document.querySelector('#scene-stage');
const crown=document.querySelector('#crown-target');
const sections=[...document.querySelectorAll('.story-section')];
const heroActions=[...document.querySelectorAll('.hero-actions,.gesture-intro,.hero-bottom')];
let scene,baseFrame={},interactionFrame={},departure,chapter=0,interactions,timeline,resetting=false,assemblyUI;

function apply(){
  const frame={...baseFrame,...interactionFrame};
  // An inspected rear view or acknowledged halo rejoins the scroll path gradually.
  // Resetting a demo at a chapter boundary must not reset its pose.
  for(const key of ['rx','ry','rz','halo','screenLevel']){
    let value=baseFrame[key];
    for(const entry of [departure,{origin:chapter,overrides:interactionFrame}]){
      const override=entry?.overrides[key==='screenLevel'?'screen':key];
      if(override!==undefined&&timeline)value+=(Number(override)-timeline.pose(entry.origin)[key])*(baseFrame.weights[entry.origin]??0);
    }
    frame[key]=['halo','screenLevel'].includes(key)?Math.min(1,Math.max(0,value)):value;
  }
  scene?.setFrame(assemblyUI?assemblyUI.compose(frame):frame);
}

timeline=createTimeline((frame,index,changed)=>{
  if(changed){
    if(['rx','ry','rz','halo','screen'].some(key=>interactionFrame[key]!==undefined))departure={origin:chapter,overrides:interactionFrame};
    resetting=true;interactions?.reset();resetting=false;
    interactionFrame={crown:interactions?.overrides.crown??0};
    if(departure?.origin===index){
      for(const key of ['rx','ry','rz','halo','screen'])if(departure.overrides[key]!==undefined){interactionFrame[key]=departure.overrides[key];if(interactions)interactions.overrides[key]=departure.overrides[key];}
      if(index===6&&interactionFrame.rx>2){const rear=document.querySelector('[data-rear]');rear.setAttribute('aria-pressed','true');rear.innerHTML='Back to the front <span aria-hidden="true">↻</span>';}
      if(index===5&&interactionFrame.halo===0){const touch=document.querySelector('[data-touch]');touch.dataset.acknowledged='true';touch.innerHTML='Show another arrival <span aria-hidden="true">↗</span>';document.querySelector('#halo-status').textContent='Touched. A quiet moment again.';}
      departure=null;
    }
  }
  baseFrame=frame;chapter=index;
  assemblyUI?.sync(frame,index,changed);
  if(departure&&!frame.weights[departure.origin])departure=null;

  // The chrome and the live object share the same scroll coordinate.
  const heroFade=Math.min(1,frame.scroll/(innerHeight*.18)),heroOpacity=1-heroFade*heroFade*(3-2*heroFade);
  const toolbarProgress=frame.story**2;
  const css={
    '--story-mix':frame.story,'--hero-actions-opacity':heroOpacity,'--pair-opacity':frame.pairLabels**2,
    '--rule-opacity':frame.rule**3,'--crown-opacity':frame.crownVisibility,
    '--aura-opacity':frame.auraOpacity,'--object-x':frame.cx*100+'%','--object-y':frame.cy*100+'%',
    '--stage-cut':frame.story*55+'%','--mask-start':100-frame.story*61+'%','--mask-end':100-frame.story*55+'%',
    '--toolbar-top':(innerHeight-59)*(1-toolbarProgress)+innerHeight*.4*toolbarProgress+'px'
  };
  for(const [key,value] of Object.entries(css))body.style.setProperty(key,String(value));
  heroActions.forEach(element=>element.inert=heroOpacity<.01);
  crown.disabled=frame.crownVisibility<.05;crown.tabIndex=frame.crownVisibility>.5?0:-1;
  stage.querySelectorAll('.pair-label').forEach(label=>label.setAttribute('aria-hidden',String(frame.pairLabels<.5)));
  if(changed){
    // Pet → boop holds the same composition, leaving a quiet interval to
    // prepare the later study before any major inspection-camera transition.
    if(index>=2)scene?.prepareAssembly().then(()=>assemblyUI?.refresh()).catch(()=>{});
    const s=sections[index];
    stage.setAttribute('aria-label',s.dataset.alt);
    document.querySelector('#scene-note').textContent=s.dataset.note;
    document.querySelector('#chapter-name').textContent=s.dataset.label.toUpperCase();
    document.querySelector('#sound-toggle').tabIndex=index===0?-1:0;
    for(const section of sections)body.classList.toggle('is-'+section.id,section===s);
    body.classList.toggle('is-scale',index===8);
    document.querySelector('.hero-still').src=assetUrl('/renders/'+s.id+'.webp');
    document.querySelectorAll('.chapter-progress a').forEach((a,i)=>{if(i===index)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});
  }
  apply();
});
interactions=createInteractions(overrides=>{if(!resetting){interactionFrame={...overrides};apply();}},()=>chapter);
assemblyUI=createAssemblyInteractions({getScene:()=>scene,getFrame:()=>baseFrame,apply});
assemblyUI.sync(baseFrame,chapter,true);

let starting=false;
const start=async()=>{
  if(starting)return;starting=true;const started=performance.now(),warmup=graphicsWarmup;
  try{
    const {createScene}=await sceneModule;
    scene=await createScene(document.querySelector('#scene-canvas'),{warmup});
    if(chapter>=2){await scene.prepareAssembly();assemblyUI.refresh();}apply();
    body.classList.add('webgl-ready');document.documentElement.dataset.ready='true';
    performance.measure('bingbong-load-to-live',{start:started,end:performance.now()});
  }catch(error){console.warn('Product view unavailable:',error.message);body.classList.add('no-webgl');document.documentElement.dataset.ready='fallback';}finally{warmup.release();}
};
// The product is live immediately; a still is used only when WebGL is unavailable.
document.documentElement.dataset.ready='loading';start();
document.querySelectorAll('[data-orbit]').forEach(button=>button.addEventListener('click',()=>scene?.rotateView(Number(button.dataset.orbit))));
document.querySelector('[data-reset-view]').addEventListener('click',()=>scene?.resetView());
window.__bingbong={get scene(){return scene;},get chapter(){return chapter;},get frame(){return assemblyUI.compose({...baseFrame,...interactionFrame});},timeline,interactions,assemblyUI,start};
if('serviceWorker'in navigator&&!import.meta.env.DEV&&!window.__BINGBONG_ASSETS)addEventListener('load',()=>navigator.serviceWorker.register('/sw.js').catch(()=>{}));

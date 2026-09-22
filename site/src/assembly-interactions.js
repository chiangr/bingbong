import {parts,studies,buildSteps} from './assembly-data.js';

export function createAssemblyInteractions({getScene,getFrame,apply}){
  let section='',selected='shell',angle=0,angleTarget=0,detentAnimation=0,buildAnimation=0,manualBuild=null,feedProgress=-1,pulseAnimation=0,lastBuildStep=-1;
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const range=document.querySelector('#build-progress'),play=document.querySelector('[data-build-play]');
  const buildInner=document.querySelector('#assembly .section-inner'),buildConsole=document.querySelector('.assembly-console');
  // On phones the introduction scrolls away, then the controls remain just
  // below the reserved product view instead of disappearing behind its mask.
  function measureConsole(){const offset=buildConsole.getBoundingClientRect().top-buildInner.getBoundingClientRect().top;buildInner.style.setProperty('--assembly-sticky-top',`${innerHeight*.48-offset}px`);}
  const consoleObserver=new ResizeObserver(measureConsole);consoleObserver.observe(buildInner);addEventListener('resize',measureConsole);measureConsole();
  function select(id,root=document.querySelector('#'+section)){
    if(!parts[id]||!root)return;selected=id;getScene()?.selectPart(id);
    root.querySelectorAll('[data-part]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.part===id)));
    const panel=root.querySelector('.part-info'),p=parts[id];
    if(panel){panel.querySelector('.part-material').textContent=p.material;panel.querySelector('h3').textContent=p.name;panel.querySelector('.part-purpose').textContent=p.detail;const dd=panel.querySelectorAll('dd');dd[0].textContent=p.made;dd[1].textContent=p.fit;}
    document.querySelector('.part-pin span').textContent=p.name;apply();
  }
  function syncBuild(value){
    const percent=Math.round(value*100);range.value=percent;document.querySelector('#build-percent').textContent=percent+'%';
    const index=Math.min(5,Math.floor(value*6));range.setAttribute('aria-valuetext',`${percent}% — ${buildSteps[index].name}`);
    if(index!==lastBuildStep){lastBuildStep=index;document.querySelector('#build-step-count').textContent=String(index+1).padStart(2,'0')+' / 06';document.querySelector('#build-step-name').textContent=buildSteps[index].name;document.querySelector('#build-step-text').textContent=buildSteps[index].text;}
  }
  function stopBuild(){cancelAnimationFrame(buildAnimation);buildAnimation=0;play.setAttribute('aria-pressed','false');play.innerHTML='Play assembly <span aria-hidden="true">↗</span>';}
  document.querySelectorAll('[data-part]').forEach(button=>button.addEventListener('click',()=>select(button.dataset.part,button.closest('.story-section'))));
  document.querySelector('#scene-canvas').addEventListener('partselect',event=>{if(studies[section]?.includes(event.detail))select(event.detail);});
  document.querySelectorAll('[data-detent-step]').forEach(button=>button.addEventListener('click',()=>{
    cancelAnimationFrame(detentAnimation);const from=angle;angleTarget+=Number(button.dataset.detentStep)*Math.PI/12;
    const count=((Math.round(angleTarget/(Math.PI/12))%24)+24)%24;document.querySelector('#detent-readout').textContent=String(count).padStart(2,'0')+' / 24';
    if(reduced.matches){angle=angleTarget;apply();return;}
    const start=performance.now();function tick(now){const t=Math.min(1,(now-start)/900),ease=t*t*(3-2*t);angle=from+(angleTarget-from)*ease;apply();if(t<1)detentAnimation=requestAnimationFrame(tick);else detentAnimation=0;}detentAnimation=requestAnimationFrame(tick);
  }));
  document.querySelector('[data-feed-pulse]').addEventListener('click',()=>{
    select('contact');cancelAnimationFrame(pulseAnimation);const start=performance.now();
    function tick(now){const t=Math.min(1,(now-start)/3200);feedProgress=t;apply();if(t<1)pulseAnimation=requestAnimationFrame(tick);else{feedProgress=-1;pulseAnimation=0;apply();}}pulseAnimation=requestAnimationFrame(tick);
  });
  range.addEventListener('input',()=>{stopBuild();manualBuild=Number(range.value)/100;syncBuild(manualBuild);apply();});
  play.addEventListener('click',()=>{
    if(buildAnimation){stopBuild();return;}
    const from=manualBuild??getFrame().buildProgress??0,replay=from>.98;
    if(reduced.matches){manualBuild=1;syncBuild(1);apply();return;}
    const started=performance.now();play.setAttribute('aria-pressed','true');play.textContent='Pause assembly';
    function tick(now){const elapsed=now-started;if(replay&&elapsed<1700){const t=elapsed/1700;manualBuild=from*(1-t*t*(3-2*t));}else manualBuild=Math.min(1,(replay?0:from)+(elapsed-(replay?1700:0))/11000);syncBuild(manualBuild);apply();if(manualBuild<1||replay&&elapsed<1700)buildAnimation=requestAnimationFrame(tick);else stopBuild();}buildAnimation=requestAnimationFrame(tick);
  });
  document.querySelector('[data-build-reset]').addEventListener('click',()=>{
    stopBuild();const from=manualBuild??getFrame().buildProgress??0;
    if(reduced.matches){manualBuild=0;syncBuild(0);apply();return;}
    const start=performance.now();function tick(now){const t=Math.min(1,(now-start)/1700);manualBuild=from*(1-t*t*(3-2*t));syncBuild(manualBuild);apply();if(t<1)buildAnimation=requestAnimationFrame(tick);else stopBuild();}buildAnimation=requestAnimationFrame(tick);
  });
  // Wheel, touch and scrolling keys return control to native page progress.
  const release=()=>{if(section==='assembly'&&manualBuild!==null){
    stopBuild();const from=manualBuild,start=performance.now();
    function tick(now){const t=reduced.matches?1:Math.min(1,(now-start)/600),ease=t*t*(3-2*t);manualBuild=from+((getFrame().buildProgress??0)-from)*ease;syncBuild(manualBuild);apply();if(t<1)buildAnimation=requestAnimationFrame(tick);else{manualBuild=null;buildAnimation=0;apply();}}buildAnimation=requestAnimationFrame(tick);
  }};
  addEventListener('wheel',release,{passive:true});addEventListener('touchmove',release,{passive:true});
  addEventListener('keydown',e=>{if(e.target!==range&&['PageDown','PageUp','ArrowDown','ArrowUp','Home','End'].includes(e.code))release();});
  function sync(frame,index,changed){
    const id=document.querySelectorAll('.story-section')[index]?.id;
    if(changed){
      if(section!==id){stopBuild();cancelAnimationFrame(detentAnimation);detentAnimation=0;angle=angleTarget;cancelAnimationFrame(pulseAnimation);pulseAnimation=0;feedProgress=-1;}
      section=id;
      if(studies[id])select(document.querySelector(`#${id} [data-part][aria-pressed=true]`)?.dataset.part??studies[id][0]);
    }
    if((frame.buildStudy??0)<.001)manualBuild=null;
    if(id==='assembly')syncBuild(manualBuild??frame.buildProgress??0);
  }
  return{sync,refresh(){getScene()?.selectPart(selected);},compose(frame){return{...frame,detentAngle:angle,feedProgress,buildProgress:manualBuild??frame.buildProgress??0};},get state(){return{section,selected,angle,manualBuild};}};
}

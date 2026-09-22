/** Native scrolling, continuous pose interpolation. No scroll interception or snap. */
export const poses=[
  {rx:-.32,ry:-.28,rz:-.22,scale:1.18,cx:.50,cy:.59,screen:true,halo:.25,pair:0},
  {rx:-.28,ry:-.12,rz:-.20,scale:.77,cx:.72,cy:.37,screen:true,halo:0,pair:1,otherState:'resting'},
  {rx:-.28,ry:-.12,rz:-.20,scale:.77,cx:.72,cy:.37,screen:true,halo:0,pair:1,otherState:'resting'},
  {rx:-.35,ry:.20,rz:-.32,scale:.92,cx:.72,cy:.48,screen:true,halo:0,pair:0},
  {rx:-.16,ry:-.13,rz:.17,scale:.88,cx:.27,cy:.50,screen:true,halo:0,pair:0},
  {rx:1.05,ry:-.25,rz:-.22,scale:1.01,cx:.73,cy:.50,screen:false,halo:1,pair:0},
  {rx:-.38,ry:.30,rz:-.46,scale:.94,cx:.73,cy:.49,screen:true,halo:.20,pair:0},
  {rx:-.35,ry:-.22,rz:.30,scale:.83,cx:.72,cy:.5,screen:false,halo:0,pair:0},
  {rx:0,ry:0,rz:0,scale:.50,cx:.70,cy:.48,screen:true,halo:0,pair:0},
  {rx:-.30,ry:-.20,rz:-.28,scale:.90,cx:.73,cy:.42,screen:true,halo:.3,pair:.70},
  {rx:-.68,ry:-.20,rz:-.23,scale:.69,cx:.70,cy:.49,screen:true,halo:.15,pair:0,study:1,explode:1},
  {rx:-.24,ry:-.60,rz:-.17,scale:1.14,cx:.70,cy:.46,screen:false,halo:0,pair:0,study:1,explode:1,crownStudy:1,focusX:-33},
  {rx:.08,ry:1.40,rz:-.16,scale:4.2,cx:.70,cy:.43,screen:false,halo:0,pair:0,study:1,explode:1,detentStudy:1,focusX:-44.4},
  {rx:-.38,ry:.65,rz:-.20,scale:1.45,cx:.70,cy:.44,screen:false,halo:.15,pair:0,study:1,explode:1,antennaStudy:1,focusX:36},
  {rx:-.64,ry:-.22,rz:-.25,scale:.68,cx:.70,cy:.47,screen:true,halo:.2,pair:0,study:1,explode:1,buildStudy:1}
];
const clamp=t=>Math.min(1,Math.max(0,t));
const smooth=t=>t*t*(3-2*t);
const channels=['rx','ry','rz','scale','cx','cy','pair','otherCx','otherCy','otherScale','halo','screenLevel','ambient','story','pairLabels','rule','crownVisibility','auraOpacity','study','explode','crownStudy','detentStudy','antennaStudy','buildStudy','focusX','buildProgress'];
export function createTimeline(onFrame){
  const sections=[...document.querySelectorAll('.story-section')];
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  let starts=[],keyframes=[],buildDistance=1,current=-1,animation=0,position=scrollY,target=scrollY,lastTime=0;
  function pose(index){const p={...poses[index],state:'resting',reduced:reduced.matches,chapter:index};const m=innerWidth<700;
    p.otherCx=m?.51:.69;p.otherCy=m?.34:.66;p.otherScale=p.scale*.87;
    if(m){p.cx=.5;p.cy=index===0?.56:(p.pair?.20:.255);p.rz=index===0?-.28:-.13;p.scale=index===0?1.08:(p.pair?.82:1.0);p.otherScale=.76;}
    else if(innerWidth<1050){p.scale*=.93;p.cx=index===0?.5:index===4?.28:.75;}
    if(index===0){p.cy=Math.max(p.cy,(m?455:515)/innerHeight);if(!m)p.scale*=Math.min(1,innerHeight/850);}
    if(index===8){p.scale=(95/25.4*96)/(innerWidth/(m?122:180)*95);p.cx=m?.5:.70;p.cy=m?.255:.48;}
    if(index>=10){p.ambient=0;p.cx=m?.5:.70;p.cy=m?.235:poses[index].cy;p.scale=m?[.69,1.22,5.7,1.45,.68][index-10]:poses[index].scale;}
    p.otherScale*=p.pair||1;p.pair=Number(p.pair>0);
    p.screenLevel=Number(p.screen);p.ambient=index===8||index>=10?0:1;p.story=index===0?0:1;
    p.pairLabels=index===1||index===2?1:0;p.rule=index===8?1:0;
    p.crownVisibility=[5,7,8].includes(index)||index>=10?0:1;p.auraOpacity=index===5?.25:index===7?.3:1;
    for(const key of channels)p[key]??=0;
    return p;
  }
  // The active chapter is metadata. Every visible property follows this track,
  // including on reduced motion: scrolling must never teleport the product.
  function sample(y){
    let nearest=0,from=0,to=0,t=0;
    for(let i=1;i<starts.length;i++)if(y>=starts[i]-(innerWidth<700?innerHeight*.32:innerHeight*.45))nearest=i;
    for(let i=1;i<starts.length;i++){
      const end=starts[i],begin=Math.max(starts[i-1]+innerHeight*.04,end-innerHeight*(i>=10?1.4:1.12));
      if(y>=end){from=to=i;continue;}
      if(y>begin){from=i-1;to=i;t=smooth(clamp((y-begin)/(end-begin)));}
      break;
    }
    const a=keyframes[from],b=keyframes[to],frame={...keyframes[nearest],scrollDriven:true,scroll:y,from,to,progress:t};
    for(const key of channels)frame[key]=a[key]+(b[key]-a[key])*t;
    frame.weights=keyframes.map((_,i)=>from===to?Number(i===from):i===from?1-t:i===to?t:0);
    // A continuous arch carries the object above the copy when it changes sides.
    if(innerWidth>=700&&from!==to&&(from===4||to===4)){
      const lift=Math.sin(Math.PI*t)**2;frame.cy-=.23*lift;frame.scale*=1-.25*lift;
    }
    if(from===12&&to===13)frame.scale*=1-.55*Math.sin(Math.PI*t)**2;
    if(from===14&&to===14)frame.buildProgress=clamp((y-starts[14])/buildDistance);
    return frame;
  }
  function render(){const frame=sample(position),changed=current!==frame.chapter;current=frame.chapter;onFrame(frame,current,changed);}
  function tick(time){
    animation=0;
    const delta=Math.min(.05,Math.max(0,(time-lastTime)/1000));lastTime=time;
    // Smooth the one scroll coordinate, not ten independent destination poses.
    // Reduced motion stays directly attached to the user's scroll, with no coast.
    position=reduced.matches?target:position+(target-position)*(1-Math.exp(-delta*16));
    if(Math.abs(target-position)<.05)position=target;
    render();if(position!==target)animation=requestAnimationFrame(tick);
  }
  function requestUpdate(){target=scrollY;if(!animation){lastTime=performance.now();animation=requestAnimationFrame(tick);}}
  function update(){target=position=scrollY;render();}
  function measure(){starts=sections.map(s=>s.offsetTop);buildDistance=Math.max(1,sections[14].offsetHeight-innerHeight);keyframes=sections.map((_,i)=>pose(i));update();}
  addEventListener('scroll',requestUpdate,{passive:true});addEventListener('resize',measure);reduced.addEventListener('change',measure);
  const observer=new ResizeObserver(measure);sections.forEach(s=>observer.observe(s));measure();
  return{update,measure,reduced,sections,sample,pose:index=>({...keyframes[index]})};
}

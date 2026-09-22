import * as THREE from 'three';
import { createProduct } from './product-model.js';
import { createStudioEnvironment } from './studio.js';
import { assetUrl } from '../assets.js';
import { warmGraphics } from './graphics-warmup.js';

/** One live scene, one frame loop. Scroll and gestures update targets; the
 * renderer damps transforms without restarting animation on every scroll event. */
export async function createScene(container,{capture=false,bake=false,warmup=warmGraphics()}={}){
  const yieldTask=()=>new Promise(resolve=>setTimeout(resolve,0));
  const reflection=bake?null:new THREE.TextureLoader().loadAsync(assetUrl('/lighting/studio-cubeuv.png'));
  await warmup.ready;
  const contextStart=performance.now();
  const renderer=new THREE.WebGLRenderer({alpha:true,antialias:true,powerPreference:'default',preserveDrawingBuffer:capture});
  warmup.release();
  performance.measure('bingbong-webgl-context',{start:contextStart,end:performance.now()});
  let pixelRatio=Math.min(devicePixelRatio,innerWidth<700?2:1.5);
  renderer.setPixelRatio(pixelRatio);renderer.setClearColor(0x000000,0);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.1;
  renderer.domElement.setAttribute('aria-hidden','true');container.append(renderer.domElement);
  const scene=new THREE.Scene(),camera=new THREE.OrthographicCamera(-90,90,60,-60,.1,1000);camera.position.set(0,0,280);
  await yieldTask();
  let environment;
  if(bake)environment=createStudioEnvironment(renderer);
  else{const texture=await reflection;texture.mapping=THREE.CubeUVReflectionMapping;texture.colorSpace=THREE.NoColorSpace;texture.flipY=false;texture.generateMipmaps=false;texture.minFilter=THREE.LinearFilter;texture.magFilter=THREE.LinearFilter;texture.needsUpdate=true;environment={texture,dispose:()=>texture.dispose()};}
  scene.environment=environment.texture;scene.environmentIntensity=bake?1:4;
  const key=new THREE.DirectionalLight(0xe3eeff,2);key.position.set(-50,75,100);scene.add(key);
  const fill=new THREE.DirectionalLight(0xb2bdff,1.3);fill.position.set(50,-25,60);scene.add(fill);
  const rim=new THREE.DirectionalLight(0xabb4ff,2.5);rim.position.set(20,50,-70);scene.add(rim);
  await yieldTask();const main=createProduct();await yieldTask();const other=createProduct();scene.add(main.group,other.group);other.group.visible=false;
  // Explicit environment maps preserve each material's art-directed intensity.
  const materials=new Set();for(const product of [main,other]){product.group.traverse(o=>{if(o.material?.isMeshStandardMaterial)materials.add(o.material);});for(const light of product.haloLights)scene.add(light);}
  for(const material of materials){material.envMap=environment.texture;if(!bake)material.envMapIntensity*=4;}
  let width=1,height=1,span=180,frame={},current={},animation=0,disposed=false,contextLost=false,ready=false,lastTime=0,initialized=false,drag=null;
  let assembly,assemblyPromise;
  function prepareAssembly(){
    if(assemblyPromise)return assemblyPromise;
    assemblyPromise=import('./assembly-model.js').then(async({createAssembly})=>{
      const start=performance.now();
      const original=new Map();main.group.traverse(o=>{if(o.isMesh||o.isLine)original.set(o,{material:o.material,geometry:o.geometry,visible:o.visible,position:o.position.clone()});});
      const pending=createAssembly(main);
      performance.measure('bingbong-assembly-geometry',{start,end:performance.now()});
      for(const material of pending.materials){if(material.isMeshStandardMaterial&&!material.envMap){material.envMap=environment.texture;material.envMapIntensity=bake?.45:1.8;}materials.add(material);}
      // Warm every detail shader offstage, against the real scene's lights.
      // Keep rendering the existing exterior until all programs are ready;
      // exposing an unfinished shader makes the next live frame block on it.
      const warmup=new THREE.Group(),prepared=new Map();
      main.group.traverse(o=>{
        if(!o.isMesh&&!o.isLine)return;
        prepared.set(o,{material:o.material,geometry:o.geometry,visible:o.visible,position:o.position.clone()});
        const proxy=o.clone(false);proxy.visible=true;warmup.add(proxy);
        const prior=original.get(o);if(prior){o.material=prior.material;o.geometry=prior.geometry;o.visible=prior.visible;o.position.copy(prior.position);}else o.visible=false;
      });
      await renderer.compileAsync(warmup,camera,scene);
      for(const [o,next]of prepared){o.material=next.material;o.geometry=next.geometry;o.visible=next.visible;o.position.copy(next.position);}
      assembly=pending;document.documentElement.dataset.assemblyReady='true';wake();return assembly;
    }).catch(error=>{console.warn('Assembly study unavailable:',error.message);document.documentElement.dataset.assemblyReady='fallback';throw error;});
    return assemblyPromise;
  }
  const orbit={x:0,y:0},orbitNow={x:0,y:0},pointer={x:0,y:0},pointerNow={x:0,y:0};let orbitChapter=0;
  const raycaster=new THREE.Raycaster(),mouse=new THREE.Vector2();
  const crownTarget=document.querySelector('#crown-target'),yours=document.querySelector('.yours'),theirs=document.querySelector('.theirs');
  const studyChannels=['study','explode','crownStudy','detentStudy','antennaStudy','buildStudy','buildProgress','focusX','detentAngle'];
  const numerical=['rx','ry','rz','cx','cy','scale','pair','halo','otherHalo','otherCx','otherCy','otherScale','crown','screenLevel','ambient',...studyChannels];
  const spatial=new Set(['cx','cy','scale','pair','otherCx','otherCy','otherScale','ambient',...studyChannels]);
  const target=key=>frame[key]??(key==='screenLevel'?Number(frame.screen!==false):['scale','ambient'].includes(key)?1:0);
  function resize(){width=container.clientWidth;height=container.clientHeight;span=width<700?122:180;renderer.setSize(width,height);camera.left=-span/2;camera.right=span/2;camera.top=span/2*height/width;camera.bottom=-camera.top;camera.updateProjectionMatrix();wake();}
  function project(point,product=main){product.group.updateMatrixWorld();const p=point.clone().applyMatrix4(product.group.matrixWorld).project(camera);return{x:(p.x+1)*width/2,y:(1-p.y)*height/2};}
  function projectCrown(){return project(new THREE.Vector3(-44,0,0));}
  function draw(time=performance.now()){
    if(disposed)return;animation=0;
    const delta=Math.min(.05,Math.max(.001,(time-lastTime)/1000));lastTime=time;const t=time/1000;const f=frame;
    const ease=f.reduced?1:1-Math.exp(-delta*9);
    for(const key of numerical){const value=target(key);current[key]=f.scrollDriven&&spatial.has(key)?value:(current[key]??value)+(value-(current[key]??value))*ease;}
    for(const key of ['x','y']){orbitNow[key]+=(orbit[key]-orbitNow[key])*ease;pointerNow[key]+=(pointer[key]-pointerNow[key])*ease;}
    const idle=f.reduced?0:current.ambient,viewWeight=f.weights?.[orbitChapter]??1;
    const hover=idle*(drag?0:1),roll=idle*Math.sin(t*.48)*.025;
    const x=(current.cx-.5)*span,y=(.5-current.cy)*span*height/width;
    main.group.rotation.set(current.rx+orbitNow.x*viewWeight+roll+pointerNow.y*.025*hover,current.ry+orbitNow.y*viewWeight+Math.sin(t*.31)*.045*idle+pointerNow.x*.035*hover,current.rz+Math.sin(t*.37)*.012*idle);
    main.group.position.set(x,y+Math.sin(t*.65)*.65*idle,0);main.group.scale.setScalar(current.scale);
    main.update({screenLevel:current.screenLevel,halo:current.halo*(f.reduced?1:.92+.08*Math.sin(t*Math.PI/2)),state:f.state??'resting',crown:current.crown,pressed:f.pressed??false,time:t,reduced:f.reduced,clickRate:f.clickRate??1,reaction:f.reaction??0});
    assembly?.update({...f,...current});
    other.group.visible=current.pair>.005;
    if(other.group.visible){
      const entry=f.scrollDriven?(1-current.pair)*(width<700?1:.55):0;
      other.group.rotation.set(-.26+roll,.17+Math.sin(t*.31+1)*.035*idle,-.16);
      other.group.position.set((current.otherCx-.5)*span,(.5-current.otherCy-entry)*span*height/width+Math.sin(t*.65+1)*.6*idle,-3);
      other.group.scale.setScalar(current.otherScale*(f.scrollDriven ? .72+.28*current.pair : Math.min(1,current.pair)));
      other.update({screen:true,halo:current.otherHalo,state:f.otherState??'resting',time:t,reduced:f.reduced,clickRate:f.clickRate??1,reaction:f.reaction??0});
    }
    // Keep the light count stable when a second device enters; no mid-scroll
    // shader recompilation. Positions still follow their physical halo rings.
    for(const product of [main,other]){product.group.updateMatrixWorld();product.haloLights.forEach((light,i)=>{light.position.set(24.25,i===0?-8:8,9).applyMatrix4(product===main&&assembly?assembly.parts.halo.group.matrixWorld:product.group.matrixWorld);});}
    if(!other.group.visible)other.haloLights.forEach(light=>light.intensity=0);
    renderer.render(scene,camera);
    if(crownTarget){const p=projectCrown();crownTarget.style.left=`${p.x}px`;crownTarget.style.top=`${p.y}px`;}
    if(yours&&other.group.visible){for(const[label,product]of[[yours,main],[theirs,other]]){const p=project(new THREE.Vector3(-22,22,0),product);label.style.left=`${p.x}px`;label.style.top=`${p.y}px`;const edge=height*(1-.55*(f.story??0));label.style.opacity=width<700?Math.max(0,Math.min(1,(edge-p.y)/32))*(f.pairLabels??0)**2:'';}}
    else if(yours){yours.style.opacity='0';theirs.style.opacity='0';}
    const pin=document.querySelector('.part-pin');
    if(pin&&assembly&&current.study>.001){const point=assembly.anchor(assembly.selected)?.project(camera);if(point){const px=(point.x+1)*width/2,py=(1-point.y)*height/2;pin.style.left=`${Math.min(width-150,Math.max(30,px))}px`;pin.style.top=`${py}px`;pin.style.opacity=String(current.study*assembly.parts[assembly.selected].opacity*Math.max(0,(Math.max(...(f.weights??[1]))-.6)/.4)*(py>85&&py<height*(width<700?.42:.85)?1:0));}}else if(pin)pin.style.opacity='0';
    const unsettled=numerical.some(key=>Math.abs(target(key)-current[key])>.0001)||Math.abs(orbit.x-orbitNow.x)+Math.abs(orbit.y-orbitNow.y)>.0001;
    if(!document.hidden&&(!f.reduced||unsettled))animation=requestAnimationFrame(draw);
  }
  function wake(){if(ready&&!animation&&!disposed&&!contextLost&&!document.hidden)animation=requestAnimationFrame(draw);}
  function setFrame(next){frame={...next};if(!initialized){for(const key of numerical)current[key]=target(key);initialized=true;}wake();}
  function anchorView(){if(orbitChapter!==frame.chapter){const weight=(frame.weights?.[orbitChapter]??0)/(frame.weights?.[frame.chapter]||1);orbit.x*=weight;orbit.y*=weight;orbitNow.x*=weight;orbitNow.y*=weight;orbitChapter=frame.chapter;}}
  function hit(event){const rect=container.getBoundingClientRect();mouse.set((event.clientX-rect.left)/width*2-1,-(event.clientY-rect.top)/height*2+1);raycaster.setFromCamera(mouse,camera);return raycaster.intersectObject(main.group,true).find(hit=>hit.object.visible&&(!assembly||!hit.object.userData.partId||hit.object.userData.pickOpacity>.2));}
  const onDown=e=>{const picked=hit(e);if(e.button!==0||!picked)return;anchorView();drag={id:e.pointerId,part:picked.object.userData.partId,x:e.clientX,y:e.clientY,startX:e.clientX,startY:e.clientY,touch:e.pointerType==='touch',captured:false};if(!drag.touch){container.setPointerCapture(e.pointerId);drag.captured=true;container.classList.add('is-dragging');}};
  const onMove=e=>{pointer.x=(e.clientX/width-.5)*2;pointer.y=(e.clientY/height-.5)*2;if(!drag){if(e.pointerType==='mouse')container.style.cursor=hit(e)?'grab':'default';return;}if(drag.touch&&!drag.captured){if(Math.abs(e.clientX-drag.startX)<7)return;if(Math.abs(e.clientY-drag.startY)>Math.abs(e.clientX-drag.startX)){drag=null;return;}container.setPointerCapture(e.pointerId);drag.captured=true;container.classList.add('is-dragging');}orbit.y+=(e.clientX-drag.x)*.008;orbit.x+=(e.clientY-drag.y)*.008;drag.x=e.clientX;drag.y=e.clientY;wake();};
  const onUp=e=>{if(e?.type==='lostpointercapture'&&(e.target!==container||container.hasPointerCapture(e.pointerId)))return;if(e?.type==='pointerup'&&drag?.part&&frame.study>.5&&Math.hypot(e.clientX-drag.startX,e.clientY-drag.startY)<6)container.dispatchEvent(new CustomEvent('partselect',{detail:drag.part,bubbles:true}));drag=null;container.classList.remove('is-dragging');};
  container.addEventListener('pointerdown',onDown);container.addEventListener('pointermove',onMove);for(const type of ['pointerup','pointercancel','lostpointercapture'])container.addEventListener(type,onUp);
  const observer=new ResizeObserver(resize);observer.observe(container);resize();
  const visibility=()=>{if(document.hidden){cancelAnimationFrame(animation);animation=0;onUp();}else{lastTime=performance.now();wake();}};document.addEventListener('visibilitychange',visibility);
  const lost=e=>{e.preventDefault();contextLost=true;cancelAnimationFrame(animation);animation=0;document.body.classList.add('no-webgl');};renderer.domElement.addEventListener('webglcontextlost',lost);
  renderer.domElement.addEventListener('webglcontextrestored',async()=>{try{environment.texture.needsUpdate=true;for(const material of materials)material.needsUpdate=true;await renderer.compileAsync(scene,camera);contextLost=false;document.body.classList.remove('no-webgl');wake();}catch{document.body.classList.add('no-webgl');}});
  // KHR_parallel_shader_compile lets the browser remain responsive during setup.
  await yieldTask();await renderer.compileAsync(scene,camera);main.update({halo:1});await renderer.compileAsync(scene,camera);ready=true;
  return{setFrame,projectCrown,renderer,main,other,draw,prepareAssembly,get assembly(){return assembly;},selectPart(id){assembly?.select(id);wake();},get environment(){return environment;},get orbit(){return {...orbit};},rotateView(direction){anchorView();orbit.y+=direction*Math.PI/5;wake();},resetView(){orbit.x=0;orbit.y=0;wake();},dispose(){disposed=true;cancelAnimationFrame(animation);observer.disconnect();document.removeEventListener('visibilitychange',visibility);scene.traverse(o=>{o.geometry?.dispose();if(o.material)o.material.dispose();});environment.dispose();renderer.dispose();}};
}

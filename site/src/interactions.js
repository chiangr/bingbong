import { assetUrl } from './assets.js';
/** Browser demonstrations; never live telemetry. Pet = 250 ms, boop = 2.6 s,
 * cold boop = 90 s. Screen art remains wordless; announcements are outside it.
 */
export function createInteractions(update, getChapter) {
  let angle=0,sound=false,audio,hold=false,petTimer,petStart=0,lastPet=0,petClicks=[],boopBusy=false;
  const overrides={};
  let navigating=false;
  function navigateToBoop(cold){
    if(navigating)return;navigating=true;
    const destination=document.querySelector('#boop'),started=performance.now(),controller=new AbortController();let animation;
    const cancel=()=>{navigating=false;cancelAnimationFrame(animation);controller.abort();};
    for(const type of ['wheel','touchstart','pointerdown'])addEventListener(type,cancel,{once:true,passive:true,signal:controller.signal});
    addEventListener('keydown',event=>{if(['Escape','ArrowUp','ArrowDown','PageUp','PageDown','Home','End'].includes(event.code))cancel();},{signal:controller.signal});
    destination.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
    function arrived(){
      if(getChapter()===2&&Math.abs(destination.getBoundingClientRect().top)<2){cancel();boop(cold);}
      else if(performance.now()-started>5000)cancel();
      else animation=requestAnimationFrame(arrived);
    }
    animation=requestAnimationFrame(arrived);
  }
  const timers=new Set();
  const later=(fn,delay)=>{const id=setTimeout(()=>{timers.delete(id);fn();},delay);timers.add(id);return id;};
  const announce=text=>{document.querySelector('#gesture-announcement').textContent=text;};
  function commit(){update(overrides);}
  function clickSound(){if(!sound)return;audio??=new AudioContext();if(audio.state==='suspended')audio.resume();const buffer=audio.createBuffer(1,Math.round(audio.sampleRate*.018),audio.sampleRate);const data=buffer.getChannelData(0);for(let i=0;i<data.length;i++)data[i]=(Math.random()*2-1)*Math.exp(-i/(data.length*.17))*.15;const source=audio.createBufferSource();source.buffer=buffer;const gain=audio.createGain();gain.gain.value=.3;source.connect(gain).connect(audio.destination);source.start();}
  document.querySelector('#sound-toggle').addEventListener('click',event=>{sound=!sound;const button=event.currentTarget;button.setAttribute('aria-pressed',String(sound));button.setAttribute('aria-label',`Sound ${sound?'on':'off'}. Turn click sound ${sound?'off':'on'}.`);button.querySelector('span').textContent=`Sound ${sound?'on':'off'}`;if(sound)clickSound();});
  function turn(direction){
    clearTimeout(petTimer);
    const now=performance.now();if(!petStart||now-lastPet>600)petStart=now;lastPet=now;
    angle+=direction*Math.PI/12;overrides.crown=angle;clickSound();commit();
    if(now-petStart>=20000){announce('Petting takes a breath after twenty seconds. Pause, then start another little turn.');return;}
    const line=document.querySelector('.travel-line');line.classList.remove('active');void line.offsetWidth;line.classList.add('active');
    petClicks=petClicks.filter(time=>now-time<1000);petClicks.push(now);
    const origin=getChapter(),rate=petClicks.length*(now-petStart>15000?Math.max(0,1-(now-petStart-15000)/5000):1);later(()=>{if(getChapter()!==origin)return;overrides.otherState='petted';overrides.reaction=performance.now();overrides.clickRate=rate;commit();announce(rate>12?'Their clicks become a purr.':'One click reaches their device.');clearTimeout(petTimer);petTimer=setTimeout(()=>{delete overrides.otherState;delete overrides.clickRate;petStart=0;petClicks=[];commit();},600);},250);
  }
  function boop(cold=false){if(boopBusy)return;if(![1,2].includes(getChapter())){navigateToBoop(cold);return;}boopBusy=true;const status=document.querySelector('#boop-status');const buttons=[...document.querySelectorAll('[data-boop],[data-cold]')];buttons.forEach(b=>b.disabled=true);
    overrides.state='looking-up';overrides.pressed=true;overrides.otherState='resting';overrides.otherHalo=0;commit();status.textContent=cold?'Waking after a long quiet…':'A little hello is on its way…';announce(cold?'Cold wake demonstration. Up to ninety seconds.':'Boop pressed. The creature looks up.');
    later(()=>{if([1,2].includes(getChapter())){overrides.pressed=false;if(cold)overrides.state='stretch';commit();}},200);
    if(!cold)later(()=>{if([1,2].includes(getChapter())){overrides.state='resting';commit();}},1000);
    if(cold)later(()=>{if([1,2].includes(getChapter())){overrides.state='resting';commit();}status.textContent='Sent. Waiting for the quiet radio to wake.';},6200);
    later(()=>{if([1,2].includes(getChapter())){overrides.otherState='boop';overrides.otherHalo=1;commit();document.querySelector('#scene-stage').classList.add('boop-arrival');later(()=>document.querySelector('#scene-stage').classList.remove('boop-arrival'),400);}status.textContent='Sent. A boop is waiting on their halo.';announce('Sent. Their device has a warm halo.');boopBusy=false;buttons.forEach(b=>b.disabled=false);},cold?90000:2600);
  }
  function setHold(value){if(hold===value)return;hold=value;overrides.state=value?'leaning':'resting';overrides.otherState=value?'leaning':'resting';overrides.halo=value?.3:0;commit();document.querySelector('[data-hold]').setAttribute('aria-pressed',String(value));document.querySelector('[data-hold] span:last-child').textContent=value?'Right here.':'Hold to be there';document.querySelector('#hold-status').textContent=value?'Their creature leans in. You’re here together.':'A moment together. That’s all.';announce(value?'Their creature leans in.':'The creature settles.');}
  document.querySelectorAll('[data-turn]').forEach(button=>button.addEventListener('click',()=>turn(Number(button.dataset.turn))));
  document.querySelector('[data-boop]').addEventListener('click',()=>boop());document.querySelector('[data-cold]').addEventListener('click',()=>boop(true));
  const holdButton=document.querySelector('[data-hold]');
  holdButton.addEventListener('pointerdown',event=>{event.preventDefault();holdButton.setPointerCapture(event.pointerId);setHold(true);});
  for(const type of ['pointerup','pointercancel','lostpointercapture'])holdButton.addEventListener(type,()=>setHold(false));
  holdButton.addEventListener('keydown',event=>{if(event.code==='Space'||event.code==='Enter'){event.preventDefault();if(!event.repeat)setHold(true);}});
  holdButton.addEventListener('keyup',event=>{if(event.code==='Space'||event.code==='Enter'){event.preventDefault();setHold(false);}});
  holdButton.addEventListener('blur',()=>setHold(false));
  const crown=document.querySelector('#crown-target');let pointer=null,pressTimer;
  crown.addEventListener('pointerdown',event=>{if(event.button!==0)return;event.preventDefault();crown.setPointerCapture(event.pointerId);pointer={x:event.clientX,y:event.clientY,steps:0,moved:false};pressTimer=later(()=>{if(pointer&&!pointer.moved)setHold(true);},450);});
  crown.addEventListener('pointermove',event=>{if(!pointer)return;const d=(event.clientX-pointer.x)+(pointer.y-event.clientY);const steps=Math.trunc(d/10);if(steps!==pointer.steps){clearTimeout(pressTimer);pointer.moved=true;if(hold)setHold(false);const count=Math.min(12,Math.abs(steps-pointer.steps));const direction=Math.sign(steps-pointer.steps);for(let i=0;i<count;i++)turn(direction);pointer.steps=steps;}});
  function release(event){if(!pointer)return;clearTimeout(pressTimer);if(hold)setHold(false);else if(!pointer.moved&&event.type==='pointerup')boop();pointer=null;}
  for(const type of ['pointerup','pointercancel','lostpointercapture'])crown.addEventListener(type,release);
  crown.addEventListener('keydown',event=>{if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Enter','Space'].includes(event.code))event.preventDefault();if(event.code.startsWith('Arrow'))turn(['ArrowLeft','ArrowDown'].includes(event.code)?-1:1);else if(event.code==='Enter'&&!event.repeat)boop();else if(event.code==='Space'&&!event.repeat)setHold(true);});
  crown.addEventListener('keyup',event=>{if(event.code==='Space'){event.preventDefault();setHold(false);}});crown.addEventListener('blur',()=>setHold(false));
  // Keyboard-generated activation has no pointer event; don't double-fire a pointer click.
  crown.addEventListener('click',event=>{if(event.detail===0&&!['Enter','Space'].includes(event.code)&&event.pointerType==='')boop();});
  document.querySelectorAll('[data-creature]').forEach(button=>button.addEventListener('click',()=>{const state=button.dataset.creature;overrides.state=state;commit();document.querySelectorAll('[data-creature]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));const image=document.querySelector('#creature-study');image.src=assetUrl(`/mascot/${state}.svg`);image.alt=state==='away'?'The creature sleeps peacefully with closed eyes.':state==='boop'?'The creature has rosy cheeks and a small surprised mouth after a boop.':'The creature is content, with open eyes and a tiny smile.';announce(image.alt);}));
  document.querySelector('[data-touch]').addEventListener('click',event=>{const acknowledged=event.currentTarget.dataset.acknowledged==='true';event.currentTarget.dataset.acknowledged=String(!acknowledged);overrides.halo=acknowledged?1:0;overrides.state=acknowledged?'away':'resting';overrides.screen=!acknowledged;commit();document.querySelector('#halo-status').textContent=acknowledged?'A boop is waiting.':'Touched. A quiet moment again.';event.currentTarget.innerHTML=`${acknowledged?'Touch to acknowledge':'Show another arrival'} <span aria-hidden="true">↗</span>`;if(!acknowledged)later(()=>{if(getChapter()===5){overrides.screen=false;commit();}},2500);});
  document.querySelector('[data-rear]').addEventListener('click',event=>{const rear=event.currentTarget.getAttribute('aria-pressed')!=='true';event.currentTarget.setAttribute('aria-pressed',String(rear));event.currentTarget.innerHTML=`${rear?'Back to the front':'Turn it over'} <span aria-hidden="true">↻</span>`;overrides.rx=rear?Math.PI-.25:-.4;commit();document.querySelector('#scene-stage').setAttribute('aria-label',rear?'Rear view: four gold magnetic-dock pads, 2 millimetres across, at 2.54 millimetre pitch; the rear lid has a fine perimeter seam.':document.querySelector('#object').dataset.alt);});
  addEventListener('blur',()=>{setHold(false);pointer=null;clearTimeout(pressTimer);});
  return{overrides,turn,boop,setHold,reset(){for(const timer of timers)clearTimeout(timer);timers.clear();boopBusy=false;document.querySelectorAll("[data-boop],[data-cold]").forEach(b=>b.disabled=false);document.querySelector("#boop-status").textContent="A small hello, from your hand to theirs.";document.querySelector("#scene-stage").classList.remove("boop-arrival");setHold(false);clearTimeout(petTimer);clearTimeout(pressTimer);pointer=null;petClicks=[];petStart=0;for(const key of Object.keys(overrides))delete overrides[key];overrides.crown=angle;document.querySelector('[data-rear]').setAttribute('aria-pressed','false');document.querySelector('[data-rear]').innerHTML='Turn it over <span aria-hidden="true">↻</span>';document.querySelectorAll('[data-creature]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.creature==='resting')));document.querySelector('#creature-study').src=assetUrl('/mascot/resting.svg');document.querySelector('#creature-study').alt='The creature is content, with open eyes and a tiny smile.';document.querySelector('[data-touch]').dataset.acknowledged='false';document.querySelector('[data-touch]').innerHTML='Touch to acknowledge <span aria-hidden="true">↗</span>';document.querySelector('#halo-status').textContent='A boop is waiting.';commit();}};
}

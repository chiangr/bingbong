import { rfComponents, componentReactance } from './rf-components.js';
import { encodeMessage, demodulateSymbol, decodeMessage, receivedSample, reflectionVector, lcCurrents, radians, measurePilot } from './rf-signal.js';
import { COIL_Q, evaluateRF } from './rf-model.js';
import './rf-lessons.css';

const signed = (n, digits=2) => `${n < -(10 ** (-digits)) / 2 ? '−' : '+'}${Math.abs(n).toFixed(digits)}`;
const complex = (r,x) => Number.isFinite(r) ? `${r.toFixed(1)} ${x<0?'−':'+'} j${Math.abs(x).toFixed(1)} Ω` : 'Open circuit';
const curve = (fn,{x=30,width=585,y=85,scale=48,samples=240}={}) => Array.from({length:samples+1},(_,i)=>`${i?'L':'M'}${(x+i/samples*width).toFixed(2)},${(y-scale*fn(i/samples)).toFixed(2)}`).join(' ');

export function createRFLessons(dialog) {
  const $ = selector => dialog.querySelector(selector);
  const $$ = selector => [...dialog.querySelectorAll(selector)];
  const put = (selector,value) => { const el=$(selector);if(el.textContent!==String(value))el.textContent=value; };
  const path = (selector,value) => $(selector).setAttribute('d',value);
  const motion=matchMedia('(prefers-reduced-motion: reduce)');
  let chapter=0, animation=0, active='', part=rfComponents[0];
  const phases={part:0,lc:0,reflection:0};
  let reflection=reflectionVector(10,-150), bench=evaluateRF();
  let encoded=encodeMessage('HI'), selected=0, recovered=0, progress=0, plotKey='';
  let packetViewSymbol=-1;
  const channel={rotation:0,interference:0,locked:false,amplitude:.65,cycles:4};
  let packet=decodeMessage(encoded,channel);
  const animationButtons=$$('[data-rf-animate]');
  const labels=Object.fromEntries(animationButtons.map(b=>[b.dataset.rfAnimate,b.textContent]));
  const reducedLabels={part:'Step the part by 90° →',lc:'Step the currents by 90° →',reflection:'Step the waves by 90° →',receiver:'Recover message instantly →'};
  $$('.rf-lesson output').forEach(output=>output.setAttribute('aria-live','off'));

  function stop() {
    cancelAnimationFrame(animation); animation=0;active='';
    animationButtons.forEach(button=>{
      button.setAttribute('aria-pressed','false');
      button.textContent=motion.matches?reducedLabels[button.dataset.rfAnimate]:labels[button.dataset.rfAnimate];
    });
  }
  function animate(name) {
    if(active===name){stop();return;}
    stop();
    if(name==='receiver'&&!encoded)return;
    if(motion.matches) {
      if(name==='receiver') { selected=encoded.symbols.length-1;recovered=encoded.symbols.length;progress=1;renderReceiver(); }
      else { phases[name]=(phases[name]+90)%360;renderAnimation(name); }
      return;
    }
    if(name==='receiver' && recovered===encoded.symbols.length) resetReceiver();
    active=name;
    const button=$(`[data-rf-animate=${name}]`);
    button.setAttribute('aria-pressed','true');button.textContent='Pause animation Ⅱ';
    const started=performance.now(), from=phases[name]??0;
    const initialTime=recovered+(progress<1?progress:0);
    function tick(now) {
      if(!dialog.open||document.hidden){stop();return;}
      if(name==='receiver') {
        const time=initialTime+(now-started)/1600;
        recovered=Math.min(encoded.symbols.length,Math.floor(time));
        selected=Math.min(encoded.symbols.length-1,recovered);
        progress=recovered===encoded.symbols.length?1:time-Math.floor(time);
        renderReceiver();
        if(recovered===encoded.symbols.length){stop();return;}
      } else {
        const t=Math.min(1,(now-started)/8000);
        phases[name]=(from+t*360)%360;renderAnimation(name);
        if(t===1){stop();return;}
      }
      animation=requestAnimationFrame(tick);
    }
    animation=requestAnimationFrame(tick);
  }
  animationButtons.forEach(button=>button.addEventListener('click',()=>animate(button.dataset.rfAnimate)));
  motion.addEventListener('change',stop);
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});

  path('#rf-charge-scope',curve(t=>Math.cos(t*2*Math.PI)));
  path('#rf-charge-scope-second',curve(t=>-Math.sin(t*2*Math.PI)));
  function renderField(phase) {
    const theta=radians(phase), v=Math.cos(theta), i=-2*Math.PI*722e6*1e-12*Math.sin(theta)*1e3;
    put('#rf-field-v',`v = ${signed(v)} V`);put('#rf-field-q',`q = ${signed(v)} pC`);put('#rf-field-i',`i = ${signed(i)} mA`);
    $('#rf-math-phase').value=Math.round(phase);put('#rf-math-phase-value',`${Math.round(phase)}°`);
    path('#rf-charge-scope-marker',`M${30+phase/360*585} 20v130`);
    const quarter=Math.round(phase/90)%4;
    put('#rf-charge-scope-note',[
      'Near the positive voltage peak, charge is changing slowly and capacitor current is near zero.',
      'Near the falling voltage zero crossing, negative conventional current is strongest: positive charge is leaving the cap.',
      'Near the negative voltage peak, the charge imbalance is reversed and current is near zero again.',
      'Near the rising voltage zero crossing, positive conventional current is strongest: the cap charges positively.'
    ][quarter]);
    path('#rf-travel-wave',curve(x=>Math.cos(theta-2*Math.PI*x),{y:66,scale:32}));
    path('#rf-travel-wave-second',curve(x=>Math.cos(theta-2*Math.PI*x),{y:113,scale:32}));
    const playing=$('[data-rf-play-field]').getAttribute('aria-pressed')==='true';
    put('#rf-math-play',playing?'Pause the shared cycle Ⅱ':motion.matches?'Step the shared cycle →':'Play the shared cycle ↻');
    $('#rf-math-play').setAttribute('aria-pressed',String(playing));
  }
  $('#rf-math-phase').addEventListener('input',event=>{
    $('#rf-phase').value=event.target.value;$('#rf-phase').dispatchEvent(new Event('input'));
  });
  $('#rf-math-play').addEventListener('click',()=>{
    $('[data-rf-play-field]').click();renderField(Number($('#rf-phase').value));
  });

  function choosePart(id) {
    stop();part=rfComponents.find(component=>component.id===id);
    $$('[data-rf-component]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.rfComponent===id)));
    put('#rf-component-ref',`${part.id} / ${part.value}`);put('#rf-component-title',part.name);
    for(const key of ['where','why','principle','equation','dc','removed'])put(`#rf-component-${key}`,part[key]);
    for(const [selector,f] of [['#rf-component-low',722],['#rf-component-high',1900]]){
      const x=componentReactance(part,f);
      put(selector,x===null?(part.kind.startsWith('DNP')||part.kind==='trap'?'No fitted element; pad parasitics remain.':'Set by contact geometry and parasitics; no measured value yet.'):`${signed(x,1)} Ω reactance${part.kind==='TVS'?' for a 0.3 pF parasitic model':''}`);
    }
    $('#rf-part-oscillator').hidden=!['L','C','TVS'].includes(part.kind);
    renderPart();
    // The broader path diagram remains in sync with the component inspector.
    $(`[data-rf-path="${part.path}"]`).click();
  }
  $$('[data-rf-component]').forEach(button=>button.addEventListener('click',()=>choosePart(button.dataset.rfComponent)));
  function renderPart() {
    if(!['L','C','TVS'].includes(part.kind))return;
    const inductive=part.kind==='L', theta=radians(phases.part), currentShape=(inductive?1:-1)*Math.sin(theta);
    const reactance=componentReactance(part,722), current=currentShape/Math.abs(reactance);
    const energy=inductive?.5*part.amount*1e-9*current**2*1e12:.5*part.amount*Math.cos(theta)**2;
    path('#rf-part-scope',curve(t=>Math.cos(t*2*Math.PI)));
    path('#rf-part-scope-second',curve(t=>(inductive?1:-1)*Math.sin(t*2*Math.PI)));
    path('#rf-part-scope-marker',`M${30+phases.part/360*585} 20v130`);
    $('#rf-part-phase').value=Math.round(phases.part);put('#rf-part-phase-value',`${Math.round(phases.part)}°`);
    put('#rf-part-scope-title',`${part.id}: current ${inductive?'lags':'leads'} voltage by 90°.`);
    put('#rf-part-voltage',`v = ${signed(Math.cos(theta))} V`);
    put('#rf-part-current',`i = ${signed(current*1e3)} mA`);
    put('#rf-part-energy',`${inductive?'Magnetic':'Electric'} energy = ${energy.toFixed(3)} pJ`);
    put('#rf-part-scope-note',`Assume 1 V peak at 722 MHz across this isolated ${part.kind==='TVS'?'0.3 pF off-state capacitance':inductive?'inductor':'capacitor'}. ${inductive?'WH = ½Li²':'WE = ½Cv²'}. Both traces are normalized to their own peaks; the readouts retain units. This is not the voltage or current predicted at this position in the assembled circuit.${part.kind==='TVS'?' Surge clamping is nonlinear and is not represented by this plot.':''}`);
  }
  $('#rf-part-phase').addEventListener('input',event=>{stop();phases.part=Number(event.target.value);renderPart();});

  function arrow(selector,cx,y,value,peak) {
    const extent=32*value/peak, sign=Math.sign(value), end=cx+extent;
    path(selector,`M${cx-extent} ${y}H${end}m${-sign*7} -5l${sign*7} 5 ${-sign*7} 5`);
    $(selector).style.opacity=Math.abs(value)<peak*.002?0:1;
  }
  function renderLC() {
    const f=Number($('#rf-network-frequency').value), r=lcCurrents(f,phases.lc);
    const peakL=1/(2*Math.PI*f*1e6*15e-9), peakC=2*Math.PI*f*1e6*1e-12, scale=Math.max(peakL,peakC);
    arrow('#rf-lc-arrow-l',400,60,r.inductor,scale);arrow('#rf-lc-arrow-c',400,190,r.capacitor,scale);arrow('#rf-lc-arrow-total',75,120,r.total,scale);
    put('#rf-lc-i-l',`IL = ${signed(r.inductor*1000)} mA`);put('#rf-lc-i-c',`IC = ${signed(r.capacitor*1000)} mA`);put('#rf-lc-i-total',`Iin = ${signed(r.total*1000)} mA`);
    $('#rf-lc-phase').value=Math.round(phases.lc);put('#rf-lc-phase-value',`${Math.round(phases.lc)}°`);
    const near=Math.abs(f-r.resonance)<3;
    put('#rf-lc-explanation',near?'Near resonance, the opposing branch-current amplitudes nearly cancel. Scrub to 90°: substantial current flows in each branch, while almost none enters the ideal pair.':f<r.resonance?'Below resonance, the inductor branch carries the larger current amplitude. Their sum has inductive timing. At 722 MHz, the pair is about +j98 Ω.':'Above resonance, the capacitor branch dominates. Their sum has capacitive timing. At 1,900 MHz, the pair is about −j158 Ω.');
  }
  $('#rf-lc-phase').addEventListener('input',event=>{stop();phases.lc=Number(event.target.value);renderLC();});
  $('#rf-network-frequency').addEventListener('input',renderLC);
  $$('[data-rf-lc-frequency]').forEach(button=>button.addEventListener('click',()=>{
    stop();$('#rf-network-frequency').value=button.dataset.rfLcFrequency==='resonance'?lcCurrents(722,0).resonance.toFixed(2):button.dataset.rfLcFrequency;
    phases.lc=90;$('#rf-network-frequency').dispatchEvent(new Event('input'));
  }));

  function renderMatch(state,result) {
    bench=result;reflection=reflectionVector(result.real,result.imaginary);
    const w=2*Math.PI*state.frequency*1e6;
    put('#rf-walk-load',complex(result.antennaReal,result.antennaImaginary));
    put('#rf-walk-series',complex(result.antennaReal+w*state.inductance*1e-9/COIL_Q,result.antennaImaginary+w*state.inductance*1e-9));
    put('#rf-walk-input',complex(result.real,result.imaginary));
    put('#rf-walk-gamma',`|Γ| = ${reflection.magnitude.toFixed(3)} → ${(result.reflected*100).toFixed(1)}% power`);
    renderReflection();
  }
  function renderReflection() {
    const theta=radians(phases.reflection), mag=reflection.magnitude, phi=reflection.phase;
    const incoming=x=>Math.cos(theta-2*Math.PI*x), returning=x=>mag*Math.cos(theta+2*Math.PI*x+phi);
    path('#rf-wave-incident',curve(incoming,{x:125,width:625,y:58,scale:28}));
    path('#rf-wave-reflected',curve(returning,{x:125,width:625,y:148,scale:28}));
    path('#rf-wave-total',curve(x=>incoming(x)+returning(x),{x:125,width:625,y:244,scale:19}));
    put('#rf-reflection-amplitude',`${mag.toFixed(2)} V peak`);
    put('#rf-reflection-phase-value',`${Math.round(phases.reflection)}°`);$('#rf-reflection-phase').value=Math.round(phases.reflection);
    put('#rf-reflection-explanation',mag<.01?'The load is nearly matched. The reflected wave is almost zero, so the total is almost entirely a forward-traveling wave. Accepted power still divides into radiation and heat.':`${(bench.reflected*100).toFixed(1)}% of incident power is reflected. The reflected voltage amplitude is ${(mag*100).toFixed(1)}% of the incident amplitude. The two waves interfere, creating a standing-wave pattern superimposed on the net forward power flow.`);
  }
  $('#rf-reflection-phase').addEventListener('input',event=>{stop();phases.reflection=Number(event.target.value);renderReflection();});
  $$('[data-rf-walk-preset]').forEach(button=>button.addEventListener('click',()=>{
    $('[data-rf-reset]').click();
    if(button.dataset.rfWalkPreset!=='bare')$(`[data-rf-tune="${button.dataset.rfWalkPreset}"]`).click();
  }));

  function renderAnimation(name) {
    if(name==='part')renderPart();else if(name==='lc')renderLC();else if(name==='reflection')renderReflection();
  }

  function setMessage() {
    stop();encoded=encodeMessage($('#rf-message-input').value);selected=0;recovered=0;progress=0;plotKey='';packetViewSymbol=-1;
    $('#rf-message-input').setAttribute('aria-invalid',String(!encoded));
    put('#rf-message-error',encoded?'':'Use 1–6 printable ASCII characters, such as HI or BOOP.');
    $('#rf-message-bytes').replaceChildren();$('#rf-message-symbols').replaceChildren();
    $('.rf-receiver-layout').hidden=!encoded;$('#rf-packet-scope').hidden=!encoded;$('.rf-receiver-meter').hidden=!encoded;
    for(const selector of ['[data-rf-animate=receiver]','#rf-receiver-step','#rf-receiver-reset','#rf-receiver-time'])$(selector).disabled=!encoded;
    if(!encoded){
      put('#rf-recovered-message','—');put('#rf-recovered-bits','Enter a valid message to calculate its symbols.');put('#rf-recovered-status','No message is being decoded.');put('#rf-receiver-progress','No valid message');
      return;
    }
    for(const byte of encoded.bytes) {
      const card=document.createElement('div');card.className='rf-byte-card';
      for(const [tag,text] of [['strong',byte.char===' '?'SPACE':byte.char],['span',byte.bits],['small',`ASCII ${byte.value} · 0x${byte.value.toString(16).toUpperCase().padStart(2,'0')}`]]){
        const el=document.createElement(tag);el.textContent=text;card.append(el);
      }
      $('#rf-message-bytes').append(card);
    }
    encoded.symbols.forEach((symbol,index)=>{
      const button=document.createElement('button');button.dataset.rfPacketSymbol=index;
      button.setAttribute('aria-label',`Symbol ${index+1}, bits ${symbol.bits}, phase ${symbol.phase} degrees`);
      for(const [tag,text] of [['small',String(index+1).padStart(2,'0')],['strong',symbol.bits],['span',`${symbol.phase}°`]]){
        const el=document.createElement(tag);el.textContent=text;button.append(el);
      }
      button.addEventListener('click',()=>{stop();selected=index;recovered=index+1;progress=1;renderReceiver();});
      $('#rf-message-symbols').append(button);
    });
    packet=decodeMessage(encoded,channel);renderPacket();renderReceiver();
  }
  function renderPacket() {
    const svg=$('#rf-packet-svg'), labels=$('#rf-packet-labels'), n=encoded.symbols.length;
    const width=Math.max(780,n*95+40), step=(width-40)/n;
    svg.setAttribute('viewBox',`0 0 ${width} 164`);svg.style.minWidth=`${width}px`;
    labels.replaceChildren();
    let waves='', boundaries='';
    encoded.symbols.forEach((symbol,index)=>{
      const left=20+index*step;
      waves+=curve(t=>Math.cos(2*Math.PI*channel.cycles*t+radians(symbol.phase)),{x:left,width:step,y:96,scale:32,samples:80});
      boundaries+=`M${left} 17V139`;
      const label=document.createElementNS('http://www.w3.org/2000/svg','text');
      label.setAttribute('x',left+step/2);label.setAttribute('y',29);label.setAttribute('text-anchor','middle');
      label.textContent=`${symbol.bits} · ${symbol.phase}°`;labels.append(label);
      if(index%4===0){
        const byte=document.createElementNS('http://www.w3.org/2000/svg','text');
        byte.setAttribute('x',left+step*2);byte.setAttribute('y',158);byte.setAttribute('text-anchor','middle');
        const char=encoded.bytes[index/4].char;
        byte.textContent=`${char===' '?'SPACE':char} · 8 bits · 4 symbols`;labels.append(byte);
      }
    });
    path('#rf-packet-wave',waves);path('#rf-packet-boundaries',boundaries+`M${width-20} 17V139`);
    $('#rf-packet-highlight').setAttribute('width',step);
  }
  function resetReceiver() {
    stop();selected=0;recovered=0;progress=0;plotKey='';renderReceiver();
  }
  function stepReceiver() {
    if(!encoded)return;stop();
    if(recovered===encoded.symbols.length){selected=0;recovered=0;}
    selected=recovered;recovered++;progress=1;renderReceiver();
  }
  function renderReceiver() {
    if(!encoded)return;
    const symbol=encoded.symbols[selected], r=demodulateSymbol(symbol,selected,channel,progress), complete=progress>=1;
    const key=JSON.stringify([selected,channel]);
    if(plotKey!==key) {
      plotKey=key;const scale=48/Math.max(1,channel.amplitude+1.05*channel.interference);
      const ref=t=>2*Math.PI*channel.cycles*t+radians(channel.locked?channel.rotation:0);
      path('#rf-rx-wave',curve(t=>receivedSample(t,symbol,selected,channel).value,{scale}));
      path('#rf-rx-wave-second',curve(t=>Math.cos(ref(t)),{scale}));
      path('#rf-mixer-wave',curve(t=>2*receivedSample(t,symbol,selected,channel).value*Math.cos(ref(t)),{scale:scale/2}));
      path('#rf-mixer-wave-second',curve(t=>-2*receivedSample(t,symbol,selected,channel).value*Math.sin(ref(t)),{scale:scale/2}));
    }
    for(const id of ['#rf-rx-wave-marker','#rf-mixer-wave-marker'])path(id,`M${30+progress*585} 15v140`);
    $('#rf-receiver-time').value=Math.round(progress*100);put('#rf-receiver-time-value',`${Math.round(progress*100)}%`);
    put('#rf-rx-symbol-label',`Symbol ${selected+1} / ${encoded.symbols.length} · sent ${symbol.bits} · ${symbol.phase}°`);
    const packetWidth=Math.max(780,encoded.symbols.length*95+40), symbolWidth=(packetWidth-40)/encoded.symbols.length;
    $('#rf-packet-highlight').setAttribute('x',20+selected*symbolWidth);
    path('#rf-packet-cursor',`M${20+(selected+progress)*symbolWidth} 37V138`);
    const scroller=$('.rf-packet-scroll');
    if(packetViewSymbol!==selected&&scroller.clientWidth){
      packetViewSymbol=selected;
      const left=20+selected*symbolWidth, right=left+symbolWidth;
      if(left<scroller.scrollLeft)scroller.scrollLeft=Math.max(0,left-20);
      else if(right>scroller.scrollLeft+scroller.clientWidth)scroller.scrollLeft=right-scroller.clientWidth+20;
    }
    put('#rf-packet-caption',`Inspecting symbol ${selected+1}: ${symbol.bits} selects ${symbol.phase}°. Four carrier cycles fit in every window; the offset changes.`);
    put('#rf-rx-i',`I = ${signed(r.i,3)}`);put('#rf-rx-q',`Q = ${signed(r.q,3)}`);
    // Fixed scale: unit amplitude is 111 px; keep the marker inside the axes.
    const x=145+Math.max(-1.05,Math.min(1.05,r.i))*111, y=140-Math.max(-1.05,Math.min(1.05,r.q))*111;
    path('#rf-rx-vector',`M145 140L${x} ${y}`);$('#rf-rx-dot').setAttribute('cx',x);$('#rf-rx-dot').setAttribute('cy',y);
    $('#rf-rx-dot').setAttribute('fill',complete&&r.bits!==symbol.bits?'#ffb59a':'#a6efd2');
    put('#rf-rx-decision',complete?`Decision: ${r.bits}`:'Accumulating…');
    put('#rf-rx-decision-text',complete?`I is ${r.i>=0?'positive':'negative'}, Q is ${r.q>=0?'positive':'negative'}. That quadrant maps to ${r.bits}.${r.bits!==symbol.bits?' It differs from the known transmitted bits.':''}${Math.abs(r.i)>1.05||Math.abs(r.q)>1.05?' Marker is clipped at the plot edge; numeric I/Q values are exact.':''}`:'The integral is not finished. A partial-window point is not yet a valid symbol decision.');
    const receivedBits=packet.bits.slice(0,recovered*2), receivedBytes=(receivedBits.match(/.{8}/g)??[]).map(byte=>parseInt(byte,2));
    const text=receivedBytes.map(byte=>byte>=32&&byte<=126?String.fromCharCode(byte):'�').join('');
    const errors=[...receivedBits].filter((bit,index)=>bit!==encoded.bits[index]).length;
    put('#rf-recovered-message',text || '…');
    put('#rf-recovered-bits',receivedBits?receivedBits.match(/.{1,2}/g).join(' · '):'Waiting for the first symbol.');
    put('#rf-recovered-status',recovered?`${recovered} of ${encoded.symbols.length} symbols decided. ${errors} bit ${errors===1?'difference':'differences'} compared with the known transmitted bits.${receivedBytes.length?` Bytes: ${receivedBytes.map(byte=>'0x'+byte.toString(16).toUpperCase().padStart(2,'0')).join(' ')}.`:' Four symbols make the first byte.'}${errors?' This toy receiver has no error correction.':''}`:'Press “Receive next symbol” to make the first decision.');
    $('.rf-recovered-card').classList.toggle('has-error',errors>0);
    put('#rf-receiver-progress',`${recovered} / ${encoded.symbols.length} symbols recovered`);
    put('#rf-receiver-meter-text',text||'…');put('#rf-receiver-meter-symbol',complete?r.bits:'…');
    put('#rf-receiver-meter-status',`${recovered}/${encoded.symbols.length} symbols · ${errors} bit ${errors===1?'difference':'differences'}`);
    $('.rf-receiver-meter').classList.toggle('has-error',errors>0);
    $$('[data-rf-packet-symbol]').forEach((button,index)=>{
      button.setAttribute('aria-pressed',String(index===selected));button.classList.toggle('is-recovered',index<recovered);
      button.classList.toggle('has-error',index<recovered && packet.results[index].bits!==encoded.symbols[index].bits);
    });
  }
  $('#rf-message-input').addEventListener('input',setMessage);
  $$('[data-rf-message]').forEach(button=>button.addEventListener('click',()=>{$('#rf-message-input').value=button.dataset.rfMessage;setMessage();}));
  $('#rf-receiver-step').addEventListener('click',stepReceiver);$('#rf-receiver-reset').addEventListener('click',resetReceiver);
  $('#rf-receiver-time').addEventListener('input',event=>{
    stop();progress=Number(event.target.value)/100;recovered=selected+(progress===1?1:0);renderReceiver();
  });
  function updateChannel() {
    stop();channel.rotation=Number($('#rf-channel-phase').value);channel.interference=Number($('#rf-interference').value);
    put('#rf-channel-phase-value',`${signed(channel.rotation,0)}°`);put('#rf-interference-value',channel.interference.toFixed(2));
    $('#rf-pilot-lock').setAttribute('aria-pressed',String(channel.locked));
    put('#rf-pilot-lock',channel.locked?'Pilot aligned · turn alignment off':'Use known pilot to align');
    const pilot=measurePilot(channel.rotation,channel.amplitude);
    put('#rf-pilot-iq',`Ip = ${signed(pilot.i,3)} · Qp = ${signed(pilot.q,3)}`);
    put('#rf-pilot-calculation',`${signed(pilot.observed,0)}° − 45° = ${signed(pilot.estimate,0)}°`);
    put('#rf-pilot-explanation',channel.locked?`The ideal pilot estimate is ${signed(channel.rotation,0)}°. Both receiver references rotate by that angle, removing the channel rotation from the data decisions. Interference can still cause errors.`:`The receiver assumes 0° while the channel adds ${signed(channel.rotation,0)}°. A rotation beyond 45° crosses ideal QPSK decision boundaries. Try +60°, then use the pilot.`);
    if(encoded){packet=decodeMessage(encoded,channel);renderReceiver();}
  }
  $('#rf-channel-phase').addEventListener('input',updateChannel);$('#rf-interference').addEventListener('input',updateChannel);
  $('#rf-pilot-lock').addEventListener('click',()=>{channel.locked=!channel.locked;updateChannel();});
  $('#rf-channel-reset').addEventListener('click',()=>{$('#rf-channel-phase').value=0;$('#rf-interference').value=0;channel.locked=false;updateChannel();});

  // Leave the path overview at its original cap selection until a part is chosen.
  put('#rf-component-ref',`${part.id} / ${part.value}`);put('#rf-component-title',part.name);
  for(const key of ['where','why','principle','equation','dc','removed'])put(`#rf-component-${key}`,part[key]);
  put('#rf-component-low',`${signed(componentReactance(part,722),1)} Ω reactance`);put('#rf-component-high',`${signed(componentReactance(part,1900),1)} Ω reactance`);
  renderPart();renderLC();renderReflection();setMessage();updateChannel();stop();
  return {renderField,renderMatch,stop,setChapter(index){if(index!==chapter)stop();chapter=index;}};
}

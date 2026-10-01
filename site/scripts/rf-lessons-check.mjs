import assert from 'node:assert/strict';
import { mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { chromium } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { QPSK, encodeMessage, demodulateSymbol, decodeMessage, measurePilot, lcCurrents, reflectionVector } from '../src/rf-signal.js';
import { evaluateRF, parallelLCReactance } from '../src/rf-model.js';
import { rfComponents } from '../src/rf-components.js';

const checks=[], errors=[];
const check=(name,pass,detail)=>{
  checks.push({name,pass:Boolean(pass),...(detail?{detail}:{})});
  console.log(`${pass?'PASS':'FAIL'} ${name}`,detail??'');
};
const near=(a,b,tolerance=1e-9)=>Math.abs(a-b)<tolerance;
const base=process.env.QA_URL||'http://127.0.0.1:4173';
await mkdir('qa/rf/deep',{recursive:true});

// Analytic identities and physical boundary cases independently constrain the models.
check('Every QPSK phase integrates to A cos φ and A sin φ',QPSK.every(symbol=>{
  const r=demodulateSymbol(symbol),phi=symbol.phase*Math.PI/180;
  return near(r.i,.65*Math.cos(phi))&&near(r.q,.65*Math.sin(phi))&&r.bits===symbol.bits;
}));
check('All 95 printable ASCII characters survive clean modulation and demodulation',Array.from({length:95},(_,i)=>String.fromCharCode(i+32)).every(char=>decodeMessage(encodeMessage(char)).text===char));
check('HI has the agreed byte and symbol sequence',encodeMessage('HI').bits==='0100100001001001'&&encodeMessage('HI').symbols.map(s=>s.phase).join(',')==='135,45,315,45,135,45,315,135');
check('Empty, non-ASCII, and overlong inputs are rejected',['','é','😀','\n','1234567'].every(text=>encodeMessage(text)===null));
check('No elapsed time means zero accumulated I and Q',near(demodulateSymbol(QPSK[0],0,{},0).i,0)&&near(demodulateSymbol(QPSK[0],0,{},0).q,0));
check('A phase offset below 45 degrees stays inside each quadrant',[-44,44].every(rotation=>decodeMessage(encodeMessage('BOOP'),{rotation}).text==='BOOP'));
check('A 60-degree rotation corrupts unaligned data',decodeMessage(encodeMessage('HI'),{rotation:60}).errors>0);
check('Measured known-pilot alignment recovers the phase and message',[-90,-60,-17,0,17,60,90].every(rotation=>near(measurePilot(rotation).estimate,rotation)&&decodeMessage(encodeMessage('BOOP'),{rotation,locked:true}).text==='BOOP'));
check('A known 45-degree pilot observed at 105 degrees reveals 60 degrees',near(measurePilot(60).observed,105)&&near(measurePilot(60).estimate,60));
check('Strong repeatable interference creates real decision errors',decodeMessage(encodeMessage('HI'),{interference:1.2}).errors>0);
const f0=lcCurrents(722,0).resonance;
check('At parallel resonance branch currents cancel while energy is conserved',[0,30,60,90,180,270].every(phase=>{
  const r=lcCurrents(f0,phase);
  return Math.abs(r.total)<1e-16&&near(r.electric+r.magnetic,.5e-12,1e-25);
}));
check('LC net current agrees with the reciprocal of its reactance',[722,1000,1600,1900].every(f=>near(lcCurrents(f,90).total,1/parallelLCReactance(f))));
check('Matched, shorted, and open boundaries have the correct reflected phase',reflectionVector(50,0).magnitude===0&&reflectionVector(0,0).real===-1&&reflectionVector(Infinity,0).real===1);
check('Complex reflected amplitude squared agrees with independent circuit power',[[10,-150],[50,0]].every(([r,x])=>near(reflectionVector(r,x).magnitude**2,((r-50)**2+x*x)/((r+50)**2+x*x)))&&near(reflectionVector(10,-150).magnitude**2,evaluateRF().reflected));

const browser=await chromium.launch({channel:'chrome',headless:true});
try {
  for(const width of [1440,390]) {
    const context=await browser.newContext({viewport:{width,height:width<700?844:1000},reducedMotion:'reduce'});
    const page=await context.newPage();
    page.on('pageerror',error=>errors.push(`${width}: ${error.message}`));
    await page.goto(`${base}/#rf-lab`);
    await page.waitForFunction(()=>document.querySelector('#rf-lab-dialog')?.open);
    const text=selector=>page.locator(selector).textContent();
    const tab=index=>page.locator(`[data-rf-tab="${index}"]`).click();
    const shot=async(name,selector)=>{
      await page.locator(selector).evaluate(el=>el.scrollIntoView({block:'start',behavior:'instant'}));
      await page.screenshot({path:`qa/rf/deep/${width}-${name}.png`});
    };

    await page.locator('#rf-math-phase').fill('90');
    check(`Shared field controls keep charge, derivative, and units synchronized ${width}`,await page.locator('#rf-phase').inputValue()==='90'&&(await text('#rf-field-i')).includes('−4.54 mA'));
    const wave=await page.locator('#rf-travel-wave').getAttribute('d');
    await page.locator('#rf-math-play').click();
    check(`Reduced-motion field advances the traveling wave by one step ${width}`,await page.locator('#rf-math-phase').inputValue()==='180'&&wave!==await page.locator('#rf-travel-wave').getAttribute('d'));
    await shot('fields','.rf-charge-scope');

    await tab(1);
    for(const part of rfComponents){
      await page.locator(`[data-rf-component="${part.id}"]`).click();
      assert.equal(await text('#rf-component-title'),part.name);
      assert.equal(await page.locator('.rf-route-svg .is-active').getAttribute('data-rf-route'),String(part.path));
      assert.equal(await page.locator('#rf-part-oscillator').isVisible(),['C','L','TVS'].includes(part.kind));
    }
    check(`All 16 real component positions synchronize the inspector and schematic ${width}`,true);
    await page.locator('[data-rf-component="L301"]').click();
    await page.locator('#rf-part-phase').fill('90');
    check(`Inductor current peaks a quarter-cycle after voltage ${width}`,(await text('#rf-part-current')).includes('+10.02 mA')&&(await text('#rf-part-energy')).includes('1.104 pJ'));
    await shot('component','.rf-component-detail');
    await page.locator('[data-rf-lc-frequency="resonance"]').click();
    check(`Resonance exposes equal, opposite branch currents ${width}`,(await text('#rf-lc-i-l')).includes('+8.16')&&(await text('#rf-lc-i-c')).includes('−8.16')&&(await text('#rf-lc-i-total')).includes('0.00'));
    check(`Near-zero input current has no misleading arrow ${width}`,await page.locator('#rf-lc-arrow-total').evaluate(el=>getComputedStyle(el).opacity)==='0');
    await page.locator('[data-rf-animate="lc"]').click();
    check(`Reduced-motion LC control steps without starting an animation ${width}`,await page.locator('#rf-lc-phase').inputValue()==='180'&&await page.locator('[data-rf-animate="lc"]').getAttribute('aria-pressed')==='false');
    await page.locator('#rf-lc-phase').fill('90');
    await shot('parallel-lc','.rf-lc-bench');

    await tab(2);
    await page.locator('[data-rf-walk-preset="bare"]').click();
    check(`Local equation controls expose the initial capacitive load ${width}`,await text('#rf-walk-input')==='10.0 − j150.0 Ω');
    await page.locator('[data-rf-walk-preset="cancel"]').click();
    check(`Canceling reactance still leaves a resistance mismatch ${width}`,await text('#rf-walk-input')==='13.0 + j0.0 Ω'&&Number.parseFloat(await text('#rf-reflected-value'))>30);
    await page.locator('[data-rf-walk-preset="match"]').click();
    check(`The equation walkthrough uses the actual bench calculation ${width}`,await text('#rf-walk-input')==='50.0 + j0.0 Ω'&&(await text('#rf-walk-gamma')).includes('0.0%'));
    check(`A matched load removes the reflected wave ${width}`,await text('#rf-reflection-amplitude')==='0.00 V peak');
    await page.locator('#rf-load').selectOption('open');
    check(`An open load restores unit reflected amplitude ${width}`,await text('#rf-reflection-amplitude')==='1.00 V peak');
    await shot('reflections','.rf-reflection-scope');

    await tab(3);
    await page.locator('#rf-receiver-time').fill('50');
    check(`A half-symbol integral does not pretend to be a completed decision ${width}`,await text('#rf-rx-decision')==='Accumulating…'&&await text('#rf-receiver-progress')==='0 / 8 symbols recovered');
    await page.locator('#rf-receiver-reset').click();
    for(let i=0;i<4;i++)await page.locator('#rf-receiver-step').click();
    check(`Four two-bit decisions recover the first ASCII byte ${width}`,await text('#rf-recovered-message')==='H'&&(await text('#rf-recovered-status')).includes('0x48'));
    for(let i=0;i<4;i++)await page.locator('#rf-receiver-step').click();
    check(`Eight symbol decisions recover HI ${width}`,await text('#rf-recovered-message')==='HI'&&(await text('#rf-recovered-status')).includes('0 bit differences'));
    await page.locator('#rf-channel-phase').fill('60');
    check(`Rotating the received phase visibly corrupts the message ${width}`,await text('#rf-recovered-message')!=='HI');
    await page.locator('#rf-pilot-lock').click();
    check(`Known-pilot measurement aligns the receiver and restores HI ${width}`,await text('#rf-recovered-message')==='HI'&&await text('#rf-pilot-calculation')==='+105° − 45° = +60°');
    if(width<700){
      await page.locator('#rf-channel-phase').evaluate(el=>el.scrollIntoView({block:'start',behavior:'instant'}));
      const rect=await page.locator('.rf-receiver-meter').boundingBox();
      check(`Phone keeps recovered text visible during channel changes ${width}`,rect.y>=158&&rect.y+rect.height<400&&await text('#rf-receiver-meter-text')==='HI',rect);
      await page.screenshot({path:`qa/rf/deep/${width}-channel.png`});
    }
    await page.locator('#rf-channel-reset').click();await page.locator('#rf-interference').fill('1.2');
    check(`Added interference can change decisions even with a fixed carrier ${width}`,await text('#rf-recovered-message')!=='HI');
    await page.locator('#rf-channel-reset').click();await page.locator('#rf-message-input').fill('<Hi!>');
    await page.locator('[data-rf-animate="receiver"]').click();
    check(`Custom text is decoded and rendered safely as text ${width}`,await text('#rf-recovered-message')==='<Hi!>'&&await page.locator('#rf-message-bytes hi').count()===0&&await page.locator('[data-rf-packet-symbol]').count()===20);
    check(`The whole-message waveform keeps the selected symbol in view ${width}`,await page.locator('.rf-packet-scroll').evaluate(el=>el.scrollLeft>0));
    await page.locator('#rf-message-input').fill('é');
    check(`Invalid text disables decoding and hides stale waveforms ${width}`,await page.locator('[data-rf-animate="receiver"]').isDisabled()&&!await page.locator('.rf-receiver-layout').isVisible()&&await page.locator('#rf-message-input').getAttribute('aria-invalid')==='true');
    await page.locator('[data-rf-message="BOOP"]').click();
    await page.locator('[data-rf-animate="receiver"]').click();
    check(`Reduced-motion users can recover an entire message instantly ${width}`,await text('#rf-recovered-message')==='BOOP'&&await page.locator('[data-rf-animate="receiver"]').getAttribute('aria-pressed')==='false');
    check(`Long message waveform scrolls within its own region ${width}`,await page.locator('.rf-packet-scroll').evaluate(el=>el.scrollWidth>el.clientWidth)&&await page.locator('.rf-lab').evaluate(el=>el.scrollWidth<=el.clientWidth+1));
    await shot('whole-message','#rf-packet-scope');
    await page.locator('[data-rf-message="HI"]').click();await page.locator('[data-rf-packet-symbol="0"]').click();
    check(`The worked first H symbol yields I negative, Q positive, and 01 ${width}`,await text('#rf-rx-i')==='I = −0.460'&&await text('#rf-rx-q')==='Q = +0.460'&&await text('#rf-rx-decision')==='Decision: 01');
    await shot('receiver','.rf-receiver-layout');

    for(let i=0;i<4;i++){
      await tab(i);
      const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();
      check(`Expanded chapter ${i+1} is accessible ${width}`,axe.violations.length===0,axe.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)})));
    }
    await page.emulateMedia({reducedMotion:'no-preference'});
    await tab(1);await page.locator('[data-rf-component="C302"]').click();
    for(const [name,slider] of [['part','#rf-part-phase'],['lc','#rf-lc-phase']]){
      const before=await page.locator(slider).inputValue();
      await page.locator(`[data-rf-animate="${name}"]`).click();await page.waitForTimeout(180);
      check(`${name} animation advances ${width}`,await page.locator(slider).inputValue()!==before);
      await page.locator(`[data-rf-animate="${name}"]`).click();
      const paused=await page.locator(slider).inputValue();await page.waitForTimeout(100);
      check(`${name} animation pauses ${width}`,await page.locator(slider).inputValue()===paused);
    }
    await tab(2);await page.locator('[data-rf-animate="reflection"]').click();await page.waitForTimeout(180);
    check(`Reflected-wave animation advances ${width}`,Number(await page.locator('#rf-reflection-phase').inputValue())>0);
    await tab(3);
    check(`Leaving a chapter stops its animation ${width}`,await page.locator('[data-rf-animate="reflection"]').getAttribute('aria-pressed')==='false');
    await page.locator('#rf-receiver-reset').click();await page.locator('[data-rf-animate="receiver"]').click();
    await page.waitForTimeout(400);
    check(`Receiver animation accumulates before deciding ${width}`,Number(await page.locator('#rf-receiver-time').inputValue())>0&&await text('#rf-receiver-progress')==='0 / 8 symbols recovered');
    await page.locator('[data-rf-animate="receiver"]').click();
    const partial=Number(await page.locator('#rf-receiver-time').inputValue());
    await page.waitForTimeout(100);
    check(`Pausing the receiver preserves its running integral ${width}`,Number(await page.locator('#rf-receiver-time').inputValue())===partial);
    await page.locator('[data-rf-animate="receiver"]').click();await page.waitForTimeout(100);
    check(`Resuming continues from the partial symbol ${width}`,Number(await page.locator('#rf-receiver-time').inputValue())>partial);
    await page.waitForTimeout(1350);
    check(`Receiver animation decides at a full symbol boundary ${width}`,(await text('#rf-receiver-progress')).startsWith('1 /'));
    await page.locator('[data-rf-close]').click();await page.waitForTimeout(80);
    check(`Closing the lab stops the receiver ${width}`,await page.locator('[data-rf-animate="receiver"]').getAttribute('aria-pressed')==='false');
    await context.close();
  }

  const context=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
  const page=await context.newPage();
  page.on('pageerror',error=>errors.push(`artifact: ${error.message}`));
  await page.goto(pathToFileURL(resolve('artifact/bingbong.html')).href+'#rf-lab');
  await page.locator('[data-rf-tab="3"]').click();await page.locator('[data-rf-animate="receiver"]').click();
  check('The standalone artifact includes the calculated message receiver',await page.locator('#rf-recovered-message').textContent()==='HI');
  await context.close();
} catch(error) {
  check('Browser sequence completed',false,error.stack);
} finally {
  await browser.close();
}
check('No expanded-lesson browser exceptions',errors.length===0,errors);
await writeFile('qa/rf/deep/results.json',JSON.stringify({date:new Date().toISOString(),checks,errors},null,2));
if(checks.some(c=>!c.pass))process.exitCode=1;

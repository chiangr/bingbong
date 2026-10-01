import assert from 'node:assert/strict';
import { mkdir, writeFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
import { chromium } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { evaluateRF, matchRF, cancelReactance, parallelLCReactance } from '../src/rf-model.js';

const checks = [], errors = [];
const check = (name, condition, detail) => {
  checks.push({ name, pass: Boolean(condition), ...(detail ? { detail } : {}) });
  console.log(`${condition ? 'PASS' : 'FAIL'} ${name}`, detail ?? '');
};
const near = (a,b,tolerance=1e-8) => Math.abs(a-b) < tolerance;
const base = process.env.QA_URL || 'http://127.0.0.1:4173';
await mkdir('qa/rf', { recursive: true });

// Independent reference cases and energy conservation, not snapshots of the implementation.
const bare = evaluateRF();
check('Unmatched 10 − j150 Ω load has the analytical reflection', near(bare.reflected, 24100/26100));
check('Reactance cancellation leaves a resistance mismatch', (() => {
  const result = evaluateRF({ inductance: cancelReactance(722,'bare') });
  return Math.abs(result.imaginary)<1e-10 && result.real<15 && result.reflected>.3;
})());
for (const load of ['bare','hand','contact']) {
  const tuned = evaluateRF({ load, ...matchRF(722,load) });
  check(`The ${load} load can be matched including coil loss`, near(tuned.real,50) && Math.abs(tuned.imaginary)<1e-8 && tuned.reflected<1e-12);
}
const resistor=evaluateRF({load:'resistor'}), open=evaluateRF({load:'open'});
check('A matched resistor accepts everything and radiates nothing', resistor.accepted===1 && resistor.radiated===0 && resistor.loadHeat===1);
check('An ideal disconnected feed reflects everything', open.reflected===1 && open.accepted===0);
check('An open antenna leaves the shunt capacitor visible at the input', near(evaluateRF({load:'open',capacitance:5}).imaginary,-1/(2*Math.PI*722e6*5e-12)));
let conserves=true;
for(const load of ['bare','hand','contact','resistor','open']) for(const frequency of [650,699,722,746,850]) for(const inductance of [0,15,38,65]) for(const capacitance of [0,7.27,24]) {
  const r=evaluateRF({load,frequency,inductance,capacitance});
  const powers=[r.reflected,r.radiated,r.networkHeat,r.loadHeat];
  conserves &&= powers.every(p=>Number.isFinite(p)&&p>=0&&p<=1) && near(powers.reduce((a,b)=>a+b,0),1);
}
check('Power is nonnegative and conserved across 300 circuit cases', conserves);
const bareMatch=matchRF(722,'bare');
check('A fixed match detunes away from its design frequency', evaluateRF({...bareMatch,frequency:850}).reflected>.5);
check('Retuning the hypothetical hand cannot recover its absorption loss', evaluateRF({load:'hand',...matchRF(722,'hand')}).radiated<evaluateRF(bareMatch).radiated);
check('The real topology’s ideal parallel LC changes sign between bands', near(parallelLCReactance(722),98,1) && near(parallelLCReactance(1900),-158,1));

const browser = await chromium.launch({ channel:'chrome', headless:true });
try {
  for(const width of [1440,820,390,360]) {
    const context=await browser.newContext({viewport:{width,height:width<700?844:1000},reducedMotion:'reduce',serviceWorkers:'block',isMobile:width<700,hasTouch:width<700});
    const page=await context.newPage();
    page.on('pageerror',error=>errors.push(`${width}: ${error.message}`));
    await page.goto(`${base}/#rf-lab`);
    await page.waitForFunction(()=>document.querySelector('#rf-lab-dialog')?.open);
    check(`Direct RF link opens the modal ${width}`,await page.locator('.rf-lab').isVisible());
    await page.locator('#rf-phase').fill('180');
    check(`Phase scrub reverses the charge ${width}`,await page.locator('#rf-charge-right text').first().textContent()==='−');
    await page.locator('[data-rf-play-field]').click();
    check(`Reduced motion advances one quarter-cycle ${width}`,await page.locator('#rf-phase').inputValue()==='270' && await page.locator('[data-rf-play-field]').getAttribute('aria-pressed')==='false');
    for(let chapter=0;chapter<4;chapter++) {
      await page.locator(`[data-rf-tab="${chapter}"]`).click();
      const axe=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();
      check(`Chapter ${chapter+1} accessibility ${width}`,axe.violations.length===0,axe.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)})));
      const overflow=await page.locator('.rf-lab').evaluate(el=>el.scrollWidth-el.clientWidth);
      check(`Chapter ${chapter+1} has no page overflow ${width}`,overflow<=1,overflow);
      await page.locator(`#rf-panel-${chapter}`).evaluate(el=>el.scrollIntoView({behavior:'instant',block:'start'}));
      if(width===1440||width===390) await page.screenshot({path:`qa/rf/${width}-chapter-${chapter+1}.png`});
    }
    await page.locator('[data-rf-tab="1"]').click();
    for(let i=0;i<6;i++) {
      await page.locator(`[data-rf-path="${i}"]`).click();
      assert.equal(await page.locator('.rf-route-svg .is-active').getAttribute('data-rf-route'),String(i));
    }
    check(`All six physical stages select their schematic ${width}`,true);
    await page.locator('[data-rf-direction="transmit"]').click();
    check(`Transmit reverses the accessible path order ${width}`,await page.locator('.rf-path-steps button').first().getAttribute('data-rf-path')==='5');
    await page.locator('#rf-panel-1 details summary').click();
    await page.locator('#rf-network-frequency').fill('1900');
    check(`High-band LC explanation becomes capacitive ${width}`,(await page.locator('#rf-network-character').textContent()).startsWith('Capacitive'));

    await page.locator('[data-rf-tab="2"]').click();
    await page.locator('[data-rf-tune="match"]').click();
    check(`Matching controls produce 50 Ω with low reflection ${width}`,await page.locator('#rf-reflected-value').textContent()==='0.0%' && await page.locator('#rf-z-value').textContent()==='50 + j0 Ω');
    const before=Number.parseFloat(await page.locator('#rf-radiated-value').textContent());
    await page.locator('#rf-load').selectOption('hand');
    check(`Adding the hand detunes a fixed match ${width}`,Number.parseFloat(await page.locator('#rf-reflected-value').textContent())>10);
    await page.locator('[data-rf-tune="match"]').click();
    check(`Retuning the hand lowers reflection but retains absorption ${width}`,await page.locator('#rf-reflected-value').textContent()==='0.0%' && Number.parseFloat(await page.locator('#rf-radiated-value').textContent())<before);
    await page.locator('#rf-load').selectOption('resistor');
    await page.locator('[data-rf-tune="bypass"]').click();
    check(`UI shows matched resistor’s zero useful radiation ${width}`,await page.locator('#rf-reflected-value').textContent()==='0.0%' && await page.locator('#rf-energy-loadHeat').textContent()==='100.0%' && await page.locator('#rf-radiated-value').textContent()==='0.0%');
    await page.locator('#rf-load').selectOption('open');
    check(`Broken feed disables matching with an explanation ${width}`,await page.locator('[data-rf-tune="match"]').isDisabled() && await page.locator('#rf-reflected-value').textContent()==='100.0%');
    await page.locator('[data-rf-reset]').click();
    await page.locator('#rf-inductance').focus();
    await page.keyboard.press('ArrowRight');
    check(`Slider works from keyboard ${width}`,await page.locator('#rf-inductance').inputValue()==='0.01');
    if(width<700) {
      await page.locator('#rf-capacitance').scrollIntoViewIfNeeded();
      const rect=await page.locator('.rf-mobile-meter').boundingBox();
      check(`Phone readout stays visible beside the tuning interaction ${width}`,rect.y>=159 && rect.y+rect.height<400,rect);
      await page.screenshot({path:`qa/rf/${width}-mobile-tuning.png`});
    }
    await page.locator('[data-rf-tab="3"]').click();
    const wave=await page.locator('#rf-carrier-wave').getAttribute('d');
    await page.locator('[data-rf-symbol="2"]').click();
    check(`QPSK selection changes both phase and waveform ${width}`,await page.locator('#rf-symbol-phase').textContent()==='225°' && await page.locator('#rf-carrier-wave').getAttribute('d')!==wave);
    for(let i=0;i<4;i++) await page.locator('[data-rf-delivery-next]').click();
    check(`Message journey reaches the other IC ${width}`,(await page.locator('#rf-delivery-title').textContent()).startsWith('Their IC'));
    await page.locator('[data-rf-tab="3"]').focus();
    await page.keyboard.press('Home');
    check(`Tab keyboard navigation selects and focuses first chapter ${width}`,await page.locator('[data-rf-tab="0"]').getAttribute('aria-selected')==='true' && await page.locator('[data-rf-tab="0"]').evaluate(el=>el===document.activeElement));
    await page.keyboard.press('Escape');
    await page.waitForFunction(()=>!document.querySelector('#rf-lab-dialog').open && location.hash==='#antenna');
    check(`Escape closes a shared link at the antenna chapter ${width}`,!await page.locator('.rf-lab').isVisible() && new URL(page.url()).hash==='#antenna');
    await page.waitForFunction(()=>document.documentElement.dataset.ready==='true' && document.documentElement.dataset.assemblyReady==='true' && window.__bingbong.chapter===13);
    const scroll=await page.evaluate(()=>scrollY);
    await page.locator('#antenna [data-rf-open]').click();
    await page.goBack();
    await page.waitForFunction(()=>!document.querySelector('#rf-lab-dialog').open);
    check(`Browser Back restores the product and its scroll ${width}`,Math.abs(await page.evaluate(()=>scrollY)-scroll)<2);
    await page.goForward();
    await page.waitForFunction(()=>document.querySelector('#rf-lab-dialog').open);
    check(`Browser Forward reopens the study ${width}`,true);
    // Standard-motion playback and background-render lifecycle.
    await page.emulateMedia({reducedMotion:'no-preference'});
    await page.locator('[data-rf-play-field]').click();
    await page.waitForTimeout(200);
    const playing=Number(await page.locator('#rf-phase').inputValue());
    await page.locator('[data-rf-play-field]').click();
    const paused=Number(await page.locator('#rf-phase').inputValue());
    await page.waitForTimeout(120);
    check(`Field cycle advances and pauses ${width}`,playing>0 && Number(await page.locator('#rf-phase').inputValue())===paused && await page.locator('[data-rf-play-field]').getAttribute('aria-pressed')==='false');
    const frame=await page.evaluate(()=>window.__bingbong.scene.renderer.info.render.frame);
    await page.waitForTimeout(100);
    check(`Fast history navigation retains modal state ${width}`,await page.evaluate(()=>location.hash==='#rf-lab' && document.body.classList.contains('rf-lab-open')));
    check(`Background WebGL pauses while the RF lab covers it ${width}`,await page.evaluate(()=>window.__bingbong.scene.renderer.info.render.frame)===frame);
    await page.locator('[data-rf-close]').click();
    await page.waitForFunction(frame=>window.__bingbong.scene.renderer.info.render.frame>frame,frame);
    check(`The live product resumes after closing ${width}`,true);
    await context.close();
  }

  const plain=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
  const nojs=await plain.newPage();await nojs.goto(`${base}/#rf-lab`);
  check('No-JavaScript RF link reaches a complete static primer',await nojs.locator('#rf-lab.rf-static-primer').isVisible() && await nojs.locator('#rf-lab h3').count()===8);
  check('Static primer has no horizontal overflow',await nojs.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  await plain.close();

  const standalone=await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
  const artifact=await standalone.newPage(), requests=[];
  artifact.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url());});
  artifact.on('pageerror',error=>errors.push(`artifact: ${error.message}`));
  await artifact.goto(pathToFileURL(resolve('artifact/bingbong.html')).href+'#rf-lab');
  await artifact.waitForFunction(()=>document.querySelector('#rf-lab-dialog')?.open);
  await artifact.locator('[data-rf-tab="2"]').click();await artifact.locator('[data-rf-tune="match"]').click();
  check('Standalone HTML includes a working RF experiment',await artifact.locator('#rf-reflected-value').textContent()==='0.0%');
  check('Standalone RF lab makes no network requests',requests.length===0,requests);
  await standalone.close();
} finally { await browser.close(); }
check('No RF browser exceptions',errors.length===0,errors);
await writeFile('qa/rf/results.json',JSON.stringify({date:new Date().toISOString(),checks,errors},null,2));
if(checks.some(c=>!c.pass)) process.exitCode=1;

import { pathSteps, deliverySteps } from './rf-content.js';
import { evaluateRF, loads, matchRF, cancelReactance, parallelLCReactance } from './rf-model.js';
import { createRFLessons } from './rf-lessons.js';

const chapterNames = ['Make a field', 'Follow the connection', 'Tune the impedance', 'Recover a message'];
const round = (value, digits = 1) => Number(value.toFixed(digits));
const impedance = (r, x, digits = 1) => Number.isFinite(r)
  ? `${round(r, digits)} ${x < -.05 ? '−' : '+'} j${round(Math.abs(x), digits)} Ω` : 'Open circuit';

export function createRFLab() {
  const dialog = document.querySelector('#rf-lab-dialog');
  if (!dialog) return;
  const $ = selector => dialog.querySelector(selector);
  const $$ = selector => [...dialog.querySelectorAll(selector)];
  const put = (selector, value) => { $(selector).textContent = value; };
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const tabs = $$('[data-rf-tab]'), panels = $$('.rf-panel');
  let chapter = 0, returnHash = '', opener = null, directEntry = false;
  let phase = 0, fieldAnimation = 0, selectedPath = 0, direction = 'receive', delivery = 0;
  const state = { frequency: 722, inductance: 0, capacitance: 0, load: 'bare' };
  const lessons = createRFLessons(dialog);

  function stopField() {
    cancelAnimationFrame(fieldAnimation); fieldAnimation = 0;
    const button = $('[data-rf-play-field]');
    button.setAttribute('aria-pressed', 'false');
    button.textContent = motion.matches ? 'Step a quarter cycle →' : 'Play one slow cycle ↻';
    lessons.renderField(phase);
  }
  function open() {
    if (dialog.open) return;
    document.body.classList.add('rf-lab-open');
    dialog.showModal();
    document.dispatchEvent(new Event('rf-lab-visibility'));
    dialog.scrollTop = 0;
  }
  document.querySelectorAll('[data-rf-open]').forEach(link => link.addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button > 0) return;
    event.preventDefault();
    opener = link; returnHash = location.hash; directEntry = false;
    history.pushState(null, '', '#rf-lab'); open();
  }));
  $('[data-rf-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {
    // Native close events are queued. Back → Forward can reopen the dialog
    // before an old event arrives; that event must not tear down the new view.
    if (dialog.open) return;
    lessons.stop();
    stopField(); document.body.classList.remove('rf-lab-open');
    document.dispatchEvent(new Event('rf-lab-visibility'));
    if (location.hash === '#rf-lab') history.replaceState(null, '', returnHash || location.pathname + location.search);
    if (directEntry) {
      document.querySelector('#antenna').scrollIntoView({ behavior: 'instant' });
      history.replaceState(null, '', '#antenna');
      document.querySelector('#antenna [data-rf-open]').focus({ preventScroll: true });
    } else opener?.focus({ preventScroll: true });
  });
  addEventListener('hashchange', () => {
    if (location.hash === '#rf-lab') open(); else if (dialog.open) { directEntry = false; dialog.close(); }
  });
  if (location.hash === '#rf-lab') { directEntry = true; open(); }

  function selectChapter(index, scroll = false) {
    lessons.setChapter(index);
    chapter = index; stopField();
    tabs.forEach((tab, i) => { tab.setAttribute('aria-selected', String(i === index)); tab.tabIndex = i === index ? 0 : -1; });
    panels.forEach((panel, i) => { panel.hidden = i !== index; });
    $('[data-rf-previous]').hidden = index === 0;
    put('#rf-chapter-count', `0${index + 1} / 04`);
    put('[data-rf-next]', index === 3 ? 'Return to the object ↗' : `${chapterNames[index + 1]} →`);
    if (scroll) panels[index].scrollIntoView({ behavior: 'instant', block: 'start' });
  }
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => selectChapter(i, dialog.scrollTop > 300));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (i + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (i + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); selectChapter(next, dialog.scrollTop > 300); tabs[next].focus({ preventScroll: true }); }
    });
  });
  $('[data-rf-next]').addEventListener('click', () => {
    if (chapter === 3) dialog.close();
    else { selectChapter(chapter + 1, true); tabs[chapter].focus({ preventScroll: true }); }
  });
  $('[data-rf-previous]').addEventListener('click', () => { selectChapter(Math.max(0, chapter - 1), true); tabs[chapter].focus({ preventScroll: true }); });

  const phaseCopy = [
    ['Charge gathers at the ends.', 'The cap is positive relative to the ground structure. Electric-field energy is large; the charging current is passing through zero in this idealized standing-wave picture.'],
    ['Charge moves back through the feed.', 'The charge imbalance crosses zero. Conventional current is strongest toward the ground side; magnetic-field energy is large. The electrons themselves move in the opposite direction.'],
    ['The polarity has reversed.', 'The cap is now negative relative to ground. The electric field reverses too. The charging current crosses zero again before turning back.'],
    ['Current flows toward the cap.', 'Charge passes back through balance, with conventional current strongest in the opposite direction. One more quarter-cycle returns to the starting state.']
  ];
  function renderPhase(value) {
    phase = value;
    const angle = value * Math.PI / 180, charge = Math.cos(angle), current = -Math.sin(angle);
    $('#rf-phase').value = Math.round(value);
    put('#rf-phase-value', `${Math.round(value)}°`);
    $('#rf-phase').setAttribute('aria-valuetext', `${Math.round(value)} degrees of the RF cycle`);
    const quadrant = Math.round(value / 90) % 4;
    put('#rf-phase-title', phaseCopy[quadrant][0]); put('#rf-phase-text', phaseCopy[quadrant][1]);
    for (const [selector, polarity] of [['#rf-charge-right', charge], ['#rf-charge-left', -charge]]) {
      const group = $(selector);
      group.style.opacity = .12 + .88 * Math.abs(charge);
      group.setAttribute('fill', polarity >= 0 ? '#a6efd2' : '#b7adff');
      group.querySelectorAll('text').forEach(text => { text.textContent = polarity >= 0 ? '+' : '−'; });
    }
    $('.rf-electric-field').style.opacity = .12 + .75 * Math.abs(charge);
    $('.rf-radiating-field').style.opacity = .15 + .55 * Math.abs(charge);
    const arrow = $('#rf-current-arrow'), end = 383 + current * 35, start = 383 - current * 35, sign = Math.sign(current);
    arrow.setAttribute('d', `M${start} 200H${end}m${-sign * 8} -5l${sign * 8} 5 ${-sign * 8} 5`);
    arrow.style.opacity = Math.abs(current);
    lessons.renderField(value);
  }
  $('#rf-phase').addEventListener('input', event => { stopField(); renderPhase(Number(event.target.value)); });
  $('[data-rf-play-field]').addEventListener('click', () => {
    if (motion.matches) { renderPhase((Math.round(phase / 90) * 90 + 90) % 360); return; }
    if (fieldAnimation) { stopField(); return; }
    const started = performance.now(), from = phase;
    $('[data-rf-play-field]').setAttribute('aria-pressed', 'true');
    put('[data-rf-play-field]', 'Pause cycle Ⅱ');
    function tick(now) {
      const elapsed = Math.min(1, (now - started) / 8000);
      renderPhase((from + elapsed * 360) % 360);
      if (elapsed < 1 && dialog.open && chapter === 0) fieldAnimation = requestAnimationFrame(tick); else stopField();
    }
    fieldAnimation = requestAnimationFrame(tick);
  });
  motion.addEventListener('change', stopField);
  document.addEventListener('visibilitychange', () => { if (document.hidden) stopField(); });

  const pathButtons = $$('[data-rf-path]');
  function selectPath(index) {
    selectedPath = index;
    pathButtons.forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.rfPath) === index)));
    $$('[data-rf-route]').forEach(group => group.classList.toggle('is-active', Number(group.dataset.rfRoute) === index));
    const step = pathSteps[index];
    for (const [id, key] of [['tag','tag'],['title','title'],['body','body'],['fact','fact'],['why','why']]) put(`#rf-path-${id}`, step[key]);
  }
  pathButtons.forEach(button => button.addEventListener('click', () => selectPath(Number(button.dataset.rfPath))));
  $$('[data-rf-route]').forEach(group => group.addEventListener('click', () => selectPath(Number(group.dataset.rfRoute))));
  $$('[data-rf-direction]').forEach(button => button.addEventListener('click', () => {
    direction = button.dataset.rfDirection;
    $$('[data-rf-direction]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    put('#rf-direction-caption', direction === 'receive' ? 'Air → cap → feed → match → RF pin' : 'RF pin → match → feed → cap → air');
    const ordered = direction === 'receive' ? pathButtons : [...pathButtons].reverse();
    $('.rf-path-steps').replaceChildren(...ordered);
    ordered.forEach((b,i) => { b.firstElementChild.textContent = `0${i + 1}`; });
    $('#rf-route-flow').setAttribute('d', direction === 'receive' ? 'M980 45H112m8-5-8 5 8 5' : 'M112 45H980m-8-5 8 5-8 5');
    selectPath(direction === 'receive' ? 0 : 5);
  }));
  function renderDualBand() {
    const frequency = Number($('#rf-network-frequency').value), x = parallelLCReactance(frequency);
    put('#rf-network-frequency-value', `${frequency} MHz`);
    const near = Math.abs(x) > 1000;
    const magnitude = Math.abs(x);
    put('#rf-network-reactance', `${x >= 0 ? '+' : '−'}${magnitude > 1e6 ? `${round(magnitude / 1e6)} MΩ` : magnitude > 1000 ? `${round(magnitude / 1000)} kΩ` : `${Math.round(magnitude)} Ω`}`);
    put('#rf-network-character', near ? 'Near the parallel-resonance peak' : x > 0 ? 'Inductive at this frequency' : 'Capacitive at this frequency');
    put('#rf-network-explanation', near ? 'The ideal pair strongly opposes current here. It is placed between the intended low and high bands; real losses limit the peak.' : x > 0 ? 'Below resonance, the pair can help compensate a capacitive antenna.' : 'Above resonance, the pair presents a capacitive reactance. The rest of the network and antenna still determine the final match.');
    $('#rf-network-frequency').setAttribute('aria-valuetext', `${frequency} megahertz, ${Math.round(x)} ohms reactance`);
  }
  $('#rf-network-frequency').addEventListener('input', renderDualBand);

  function renderBench() {
    const result = evaluateRF(state);
    lessons.renderMatch(state,result);
    put('#rf-load-description', loads[state.load].description);
    for (const [key, unit, precision] of [['frequency','MHz',0],['inductance','nH',2],['capacitance','pF',2]]) {
      $(`#rf-${key}`).value = state[key];
      put(`#rf-${key}-value`, `${state[key].toFixed(precision)} ${unit}`);
      $(`#rf-${key}`).setAttribute('aria-valuetext', `${state[key].toFixed(precision)} ${unit}`);
    }
    const z = impedance(result.real, result.imaginary);
    put('#rf-z-value', z);
    put('#rf-mobile-z', z);
    put('#rf-mobile-reflected', `${(result.reflected * 100).toFixed(1)}%`);
    put('#rf-mobile-radiated', `${(result.radiated * 100).toFixed(1)}%`);
    put('#rf-z-note', state.load === 'open' ? 'Feed disconnected' : 'Goal: 50 + j0 Ω');
    put('#rf-reflected-value', `${(result.reflected * 100).toFixed(1)}%`);
    put('#rf-radiated-value', `${(result.radiated * 100).toFixed(1)}%`);
    put('#rf-return-loss', `Return loss: ${Number.isFinite(result.returnLoss) ? result.returnLoss.toFixed(1) : '∞'} dB`);
    for (const key of ['reflected','networkHeat','loadHeat','radiated']) {
      $(`[data-rf-energy=${key}]`).style.width = `${result[key] * 100}%`;
      put(`#rf-energy-${key}`, `${(result[key] * 100).toFixed(1)}%`);
    }
    put('#rf-circuit-c', `C = ${state.capacitance.toFixed(2)} pF`);
    put('#rf-circuit-l', `L = ${state.inductance.toFixed(2)} nH`);
    put('#rf-circuit-load', impedance(result.antennaReal, result.antennaImaginary, 0));
    $('[data-rf-tune=match]').disabled = state.load === 'open';
    $('[data-rf-tune=cancel]').disabled = state.load === 'open';
    const traces = { reflected: [], radiated: [] };
    for (let f = 650; f <= 850; f++) {
      const sample = evaluateRF({ ...state, frequency: f });
      for (const key of Object.keys(traces)) traces[key].push(`${f === 650 ? 'M' : 'L'}${47 + (f - 650) / 200 * 553},${169 - sample[key] * 144}`);
    }
    for (const key of Object.keys(traces)) $(`#rf-sweep-${key}`).setAttribute('d', traces[key].join(' '));
    const marker = 47 + (state.frequency - 650) / 200 * 553;
    $('#rf-sweep-marker').setAttribute('d', `M${marker} 20v154`);
    $('#rf-sweep-dot').setAttribute('cx', marker); $('#rf-sweep-dot').setAttribute('cy', 169 - result.radiated * 144);
    put('#rf-sweep-desc', `Hypothetical circuit sweep from 650 to 850 MHz, with L ${state.inductance} nH and C ${state.capacitance} pF. At ${state.frequency} MHz, ${(result.reflected * 100).toFixed(1)} percent is reflected and ${(result.radiated * 100).toFixed(1)} percent is radiated.`);
  }
  for (const key of ['frequency','inductance','capacitance']) $(`#rf-${key}`).addEventListener('input', event => {
    state[key] = Number(event.target.value); renderBench();
    put('#rf-tune-status', key === 'frequency' ? 'L and C stay fixed as you change frequency. Watch the marker move along the curves.' : 'The circuit is recalculated as you change the component. Follow both reflection and radiation.');
  });
  $('#rf-load').addEventListener('change', event => {
    state.load = event.target.value; renderBench();
    put('#rf-tune-status', state.load === 'open' ? 'No conductive feed: matching cannot repair this ideal open circuit.' : 'The load changed; L and C stayed fixed. Compare the old match, then try retuning.');
  });
  $$('[data-rf-tune]').forEach(button => button.addEventListener('click', () => {
    if (button.dataset.rfTune === 'bypass') {
      state.inductance = 0; state.capacitance = 0;
      put('#rf-tune-status', 'The series position is a wire and the shunt position is open. You see the load directly.');
    } else if (button.dataset.rfTune === 'cancel') {
      state.inductance = round(cancelReactance(state.frequency, state.load), 2); state.capacitance = 0;
      put('#rf-tune-status', 'The series inductor cancels the antenna’s capacitive reactance. The remaining resistance, including coil loss, may still be far from 50 Ω.');
    } else {
      const match = matchRF(state.frequency, state.load);
      if (!match) { put('#rf-tune-status', 'No match is available with this circuit and these component ranges.'); return; }
      state.inductance = round(match.inductance, 2); state.capacitance = round(match.capacitance, 2);
      put('#rf-tune-status', state.load === 'resistor' ? 'This load already matches 50 Ω. It accepts the power and turns all of it into heat.' : 'Matched at this frequency, to slider precision. Now change frequency or add the hypothetical hand. A fixed match cannot follow every change.');
    }
    renderBench();
  }));
  $('[data-rf-reset]').addEventListener('click', () => {
    Object.assign(state, { frequency: 722, inductance: 0, capacitance: 0, load: 'bare' });
    $('#rf-load').value = 'bare'; renderBench();
    put('#rf-tune-status', 'Experiment reset. Try canceling the reactance first. Does that make the load 50 Ω?');
  });

  function renderSymbol(index) {
    const angle = (45 + index * 90) * Math.PI / 180, bits = ['00','01','11','10'][index];
    $$('[data-rf-symbol]').forEach((button,i) => button.setAttribute('aria-pressed', String(i === index)));
    $$('[data-rf-constellation]').forEach((point,i) => point.classList.toggle('is-active', i === index));
    $('#rf-symbol-vector').setAttribute('d', `M160 131L${160 + 83 * Math.cos(angle)} ${131 - 83 * Math.sin(angle)}`);
    put('#rf-symbol-phase', `${45 + index * 90}°`);
    const signed = value => `${value >= 0 ? '+' : '−'}${Math.abs(value).toFixed(2)}`;
    put('#rf-symbol-iq', `I ${signed(Math.cos(angle))} / Q ${signed(Math.sin(angle))}`);
    put('#rf-symbol-title', `QPSK constellation: symbol ${bits} at ${45 + index * 90} degrees`);
    put('#rf-carrier-label', `Symbol ${bits} · phase ${45 + index * 90}° · normalized amplitude`);
    for (const [selector, offset] of [['#rf-carrier-reference',0], ['#rf-carrier-wave',angle]]) {
      const points = Array.from({ length: 901 }, (_,i) => `${i ? 'L' : 'M'}${20 + i},${70 - 42 * Math.cos(i / 900 * Math.PI * 12 + offset)}`);
      $(selector).setAttribute('d', points.join(' '));
    }
  }
  $$('[data-rf-symbol]').forEach(button => button.addEventListener('click', () => renderSymbol(Number(button.dataset.rfSymbol))));
  function selectDelivery(index) {
    delivery = index;
    $$('[data-rf-delivery]').forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.rfDelivery) === index)));
    put('#rf-delivery-title', deliverySteps[index][0]); put('#rf-delivery-text', deliverySteps[index][1]);
    put('[data-rf-delivery-next]', index === 4 ? 'Start the journey again ↺' : 'Follow the next step →');
  }
  $$('[data-rf-delivery]').forEach(button => button.addEventListener('click', () => selectDelivery(Number(button.dataset.rfDelivery))));
  $('[data-rf-delivery-next]').addEventListener('click', () => selectDelivery((delivery + 1) % deliverySteps.length));

  renderPhase(0); stopField(); selectPath(selectedPath); renderDualBand(); renderBench(); renderSymbol(0);
}

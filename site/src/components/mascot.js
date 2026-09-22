/** Firmware-friendly artwork: 294 x 126 landscape = the rotated 126 x 294 panel.
 * States: resting, away, looking-up, stretch, boop, petted, leaning, sleeping.
 * Only resting/away are persistent presence states; all others are reactions.
 * drawMascot(ctx, state, timeSeconds, reducedMotion) draws the same four-colour art.
 */
export const states = ['resting', 'away', 'looking-up', 'stretch', 'boop', 'petted', 'leaning', 'sleeping'];
export const palette = { body: '#F5A078', light: '#FFC29D', shade: '#DE7252', ink: '#352019' };
const body = 'M -54 20 C -54 -2 -43 -36 -18 -40 C -9 -48 5 -46 13 -39 C 38 -37 54 -9 54 19 C 55 36 37 41 0 41 C -37 41 -54 36 -54 20 Z';
const top = 'M -40 -4 C -35 -22 -26 -31 -14 -32 C -8 -39 3 -38 9 -32 C 18 -32 26 -27 31 -22 C 7 -28 -19 -25 -40 -4 Z';
const shade = 'M -53 22 C -25 37 28 36 53 20 C 54 36 36 41 0 41 C -35 41 -53 35 -53 22 Z';

export function mascotGroup(state, id = state) {
  const asleep = state === 'away' || state === 'sleeping';
  const closed = asleep || state === 'petted';
  const open = ['looking-up', 'stretch', 'boop'].includes(state);
  const eyes = closed
    ? '<path d="M-24 0 Q-18 6-12 0 M12 0 Q18 6 24 0" fill="none" stroke="#352019" stroke-width="4" stroke-linecap="round"/>'
    : '<ellipse cx="-18" cy="0" rx="5.5" ry="7"/><ellipse cx="18" cy="0" rx="5.5" ry="7"/>';
  const mouth = open
    ? `<ellipse cx="0" cy="15" rx="${state === 'stretch' ? 7 : 4}" ry="${state === 'stretch' ? 9 : 5}"/>`
    : '<path d="M-4 14 Q0 18 4 14" fill="none" stroke="#352019" stroke-width="3" stroke-linecap="round"/>';
  const pose = state === 'stretch' ? 'translate(147 65) scale(.91 1.15)' : state === 'leaning' ? 'translate(150 69) scale(1.07)' : 'translate(147 72)';
  return `<g id="${id}" class="mascot-state ${state}" opacity="${asleep ? '.63' : '1'}"><g transform="${pose}"><g class="creature-body"><path d="${body}" fill="${palette.body}"/><path d="${top}" fill="${palette.light}"/><path d="${shade}" fill="${palette.shade}"/><g class="face" fill="${palette.ink}" transform="translate(0 ${state === 'looking-up' ? '-9' : '0'})">${eyes}${mouth}</g>${state === 'boop' || state === 'petted' ? '<ellipse cx="-34" cy="12" rx="7" ry="4" fill="#DE7252"/><ellipse cx="34" cy="12" rx="7" ry="4" fill="#DE7252"/>' : ''}</g></g></g>`;
}

export function mascotSvg(state = 'resting', label = 'A soft peach creature, content and facing you') {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 294 126" role="img" aria-label="${label}" class="mascot-art" data-state="${state}"><rect width="294" height="126" fill="#000"/>${mascotGroup(state, `mascot-${state}`)}</svg>`;
}

export function drawMascot(ctx, state = 'resting', t = 0, reduced = false, elapsed = 0, clickRate = 1) {
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 294, 126);
  const away = state === 'away' || state === 'sleeping';
  const breath = reduced ? 0 : Math.sin(t * Math.PI * 2 / (away ? 1.95 : 1.8));
  const shiver = state === 'petted' && !reduced ? (clickRate>12?Math.sin(t*65)*1.1:Math.sin(elapsed*Math.PI*6)*Math.max(0,1-elapsed/.6)) : 0;
  const bounce = state === 'boop' && !reduced && elapsed<.6 ? -Math.sin(elapsed/.6*Math.PI)*3 : 0;
  const yawn = state === 'sleeping' && !reduced && elapsed<1.2;
  ctx.save(); ctx.translate(147 + shiver + (state === 'leaning' ? 3 : 0), 72 + bounce);
  if (state === 'stretch') ctx.scale(.91, 1.09 + breath * .05);
  else if (state === 'leaning') ctx.scale(1.07, 1.07);
  else ctx.scale(1 + breath * .012, 1 - breath * .018);
  ctx.globalAlpha = away ? .63 : 1;
  for (const [path, color] of [[body, palette.body], [top, palette.light], [shade, palette.shade]]) { ctx.fillStyle = color; ctx.fill(new Path2D(path)); }
  ctx.fillStyle = palette.ink; ctx.strokeStyle = palette.ink; ctx.lineWidth = 4; ctx.lineCap = 'round';
  const eyeY = state === 'looking-up' ? -9 : 0;
  const blink = !reduced && t % 5.5 > 5.38;
  if (away || state === 'petted' || blink) {
    for (const x of [-18,18]) { ctx.beginPath(); ctx.moveTo(x-6, eyeY); ctx.quadraticCurveTo(x, eyeY+6, x+6, eyeY); ctx.stroke(); }
  } else for (const x of [-18,18]) { ctx.beginPath(); ctx.ellipse(x, eyeY, 5.5, state === 'leaning' ? 8 : 7, 0, 0, Math.PI*2); ctx.fill(); }
  ctx.beginPath();
  if (['looking-up','stretch','boop'].includes(state)||yawn) { ctx.ellipse(0, 15 + eyeY, state === 'stretch'||yawn ? 7 : 4, state === 'stretch'||yawn ? 9 : 5, 0, 0, Math.PI*2); ctx.fill(); }
  else { ctx.lineWidth = 3; ctx.moveTo(-4,14); ctx.quadraticCurveTo(0,18,4,14); ctx.stroke(); }
  if (['petted','boop'].includes(state)) { ctx.fillStyle = palette.shade; for (const x of [-34,34]) { ctx.beginPath(); ctx.ellipse(x,12,7,4,0,0,Math.PI*2); ctx.fill(); } }
  ctx.restore();
}

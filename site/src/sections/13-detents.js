import {partControls} from '../assembly-data.js';
export default {id:'detents',label:'The mechanical click',eyebrow:'12 / Touch, made mechanical',study:true,
 title:'Two tiny balls.<br><em>Twenty-four clicks.</em>',description:'The race turns. Each ceramic ball climbs a land, flexes its leaf spring, then settles into the next groove.',
 alt:'Cutaway detail of the grooved race and two opposed ceramic balls on spring leaves. The fixed sleeve supports them while the race rotates in 15-degree steps.',
 extra:'<div class="detent-demo interactive"><button data-detent-step="-1" aria-label="Turn one detent backward">−</button><div><strong id="detent-readout" aria-live="polite" aria-atomic="true">00 / 24</strong><span>15° per click</span></div><button data-detent-step="1" aria-label="Turn one detent forward">+</button></div><p class="micro-caption">Turn a click. Watch both balls work.<br>Movement slowed; sleeve shown in cutaway.</p>'+partControls('detents','balls'),
 annotation:'Two opposed balls seat together. No motor makes this click.'};

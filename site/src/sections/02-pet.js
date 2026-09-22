export default {
  id:'pet', label:'Turn to pet', eyebrow:'01 / A touch that travels',
  title:'A little turn.<br><em>A little closer.</em>',
  description:'Every click of your crown becomes a little touch in their hand. Turn faster, and the clicks become a purr.',
  alt:'Two bonded devices: turning your crown moves in 15-degree detents; the creature on their device reacts after the quarter-second petting demonstration.',
  extra:`<div class="turn-control interactive"><button class="circle-button" data-turn="-1" aria-label="Turn the crown one detent left">−</button><div><span class="mono detent-label">24 REAL DETENTS</span><span class="control-caption">Drag the crown. Find your rhythm.</span></div><button class="circle-button" data-turn="1" aria-label="Turn the crown one detent right">+</button></div>
    <p class="small-note">Ceramic on steel. The click is mechanical, even with a flat battery. The crown stops at the next detent.</p>
    <details><summary>The path of a touch <span aria-hidden="true">+</span></summary><div class="detail-content"><ol class="signal-path"><li>Your turn <small>Angle sensed 100 times / second</small></li><li>Cellular <small>Up to 10 packets / second</small></li><li>Their hand <small>A 170 Hz haptic actuator</small></li></ol><p>Petting target: ≤250 ms typical, 400 ms ceiling. This demo uses 250 ms. Faster than about 12 clicks per second becomes a purr; it fades over 600 ms when you stop. Sessions taper at 15 seconds and stop at 20 seconds. Design targets, unmeasured.</p></div></details>`,
  annotation:'Yours turns. Theirs answers.'
};

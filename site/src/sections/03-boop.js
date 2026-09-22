export default {
  id:'boop',label:'Press to boop',eyebrow:'02 / Thinking of you',
  title:'A boop<br><em>says enough.</em>',
  description:'Press the crown. Your creature looks up; theirs gets a low, round thump and a little bloom of light.',
  alt:'The same pair of devices: the sender’s crown presses 0.4 mm, the creature looks up, then the receiving device’s halo blooms warm after the conversation-delay demonstration.',
  extra:`<button class="primary-link interactive" data-boop>Send a boop <span aria-hidden="true">↗</span></button>
    <p class="interaction-status" id="boop-status" role="status">A small hello, from your hand to theirs.</p>
    <div class="waveform" aria-label="Two haptic transients at 170 Hz, 40 milliseconds apart; the second is 60 percent of the first"><svg viewBox="0 0 340 64" aria-hidden="true"><path class="wave-baseline" d="M0 32H340"/><path d="M0 32H32L35 20L39 46L43 7L47 56L51 12L55 51L59 17L63 46L67 23L71 40L75 28L79 35L83 32H177L181 26L185 39L189 18L193 46L197 22L201 42L205 26L209 37L213 30L217 33L221 32H340"/></svg><span>bing<span>40 ms</span>bong</span></div>
    <details><summary>Sometimes a hello takes a moment <span aria-hidden="true">+</span></summary><div class="detail-content"><p>About 2.6 seconds inside a conversation; up to about 90 seconds after a long quiet. Both are unmeasured targets. The creature stretches for the 2–6 second radio wake, while the halo carries the arrival until touched.</p><button class="text-button interactive" data-cold>Try a cold wake <span aria-hidden="true">↗</span></button><p class="small-note">The cold demo waits 90 seconds. Stay here to see it arrive, or keep exploring. The regular demo waits 2.6 seconds. These are simulations, not live devices.</p></div></details>`,
  annotation:'A little bing…bong. Felt, without a speaker.'
};

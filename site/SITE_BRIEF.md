# bingbong Interactive Site Brief

2026-09-19 · Ryan (Drover Labs)

## 1. The ask

Build a single-page, scroll-driven interactive site that lets a visitor *experience* bingbong — a paired cellular keychain you twist, press and hold to reach one other person — by rendering the product on screen, revealing every feature as they scroll, and putting a small, genuinely cute mascot on the device's own display. You own the creative direction, the narrative structure (§3) and the technology (§9). You do not own the facts: every dimension, material, behaviour and claim on the site must come from the sources in §2 and §12, and the site is not done until it passes the double-check protocol in §10.

**Who it is for.** Prospective customers — couples and people buying a gift for one person — and the product's owner, who will use it to review the design itself. Write and design for the first group; keep the second group honest by staying accurate.

**The bar.** This should read as the best product site the visitor has seen for an object this small: the render must feel like a real thing with weight, light and materials; the scroll must feel authored, not templated; the mascot must be something a person would want to keep in their pocket. Treat *cute*, *aesthetic* and *interactive* as measurable outcomes with the checks in §10, not as adjectives.

**How to work.** Research and design before you build (§8). Build in passes: render → scroll skeleton → mascot → content → motion polish → QA. Screenshot every pass at three widths. When a fact you need is missing from the sources, ask or mark it visibly as *to confirm* — never invent a number, a material, or a feature.

## 2. What bingbong is — the facts the site must be true to

bingbong is a 27 × 95 × 15 mm sealed polymer capsule sold as a bonded pair. Each half has its own LTE-M cellular radio and eSIM, so the two devices talk to each other anywhere there is signal — no phone, no app, no account, no setup. One person turns the crown; the other feels every click. Press the crown and the other person gets a *boop*. Hold it, and the other person's creature leans in.

**Three sources, in order of authority.**

1. **Product page (approved copy and visual identity):** https://claude.ai/artifact/Eqdui62rGSzzt9QofQwnec — the owner has approved this copy; reuse its wording for headlines, gestures, refusals and specs. Its dark, warm, halo-lit identity is a reference, not a constraint — you may evolve it, but do not contradict it.
2. **Engineering report (facts, numbers, materials):** https://claude.ai/artifact/2BzrpJdxdUFhoxMfTyU5pn — 400 kB; read §1 (executive summary), §4 (crown), §5 (antenna), §7 (mechanical) for what the parts are and how they fit. Where the product page and the report disagree, the report wins on facts and the product page wins on tone.
3. **Decision document (interaction spec):** `REDESIGN_DECISION_2026-09-12.md` §7 — the definitive description of what each gesture does, what the other person feels, and what the device refuses to do.

**The parts, from crown to cap** (X is millimetres along the length from the crown's front face):

| X (mm) | Part | Material / finish | What the visitor should understand |
| --- | --- | --- | --- |
| 0–6 | Knurled crown, ø13 × 8 mm, protrudes 6 mm | Non-magnetic steel, PVD or hard-anodised | Twist to pet; press to boop; 24 mechanical detents you can feel with a flat battery |
| 6–16 | Crown-end shoulder, seal, detent race, sensing magnet, satellite board | POM sleeve, hardened race, ceramic balls | The click is real — ceramic on steel — not a motor |
| 16–71 | Body: main PCB, screen, battery, haptic actuator | Polymer capsule, 1.2 mm walls | The 1.1″ colour AMOLED under 0.5 mm glass; the 170 Hz actuator that renders the other person |
| 71–72.5 | Split ring | Optical polycarbonate, 1.5 mm | The RGB halo — the gap the antenna needs, turned into light |
| 72.5–95 | End cap, 22.5 mm | Machined 6061-T6 aluminium | The cap *is* the antenna; nothing metal lives near it |

**Behaviours that must be shown correctly.** The screen sleeps between glances and wakes when picked up; arrivals are carried by the halo, which stays lit until the device is touched. The device says *sent*, never *read* or *delivered*. There is no *last seen*, no streaks, no feeding, no death; the creature is your partner, never a pet you both keep alive. Unbonding looks identical to a flat battery. The crown does not free-wheel or coast. First-boop latency after a long quiet can be up to \~90 s (the creature *stretches* while the radio wakes); inside a conversation it is \~2.6 s.

**Things the site must not claim.** Nothing is measured or certified yet; do not state battery life more precisely than “about three weeks”, do not show water immersion, do not show a phone or an app, and do not show colour options that were never designed.

## 3. Creative freedom — choose the narrative, then commit to it

You decide how the product is revealed. Two structures are known to work for an object like this; pick one, or propose a third, and write one paragraph in your design notes saying why before you build. Do not blend them halfway — a half-exploded, half-sequential page reads as indecision.

**A. The exploded view.** The hero shows the assembled object. As the visitor scrolls, it separates along its axis into its real parts — crown, race and balls, satellite board, body shell, PCB, screen, battery, actuator, split ring, aluminium cap — each pausing with a short caption, then re-assembling at the end into the finished thing. Strength: it proves the object is real and engineered. Risk: it can feel like a teardown, cold rather than warm, and the mascot has nowhere to live until the end.

**B. Feature by feature, building to the whole.** The page opens on the smallest possible thing — a single click, or the mascot alone on a black screen — and each scroll section adds one layer of the product (the crown and its click → the other person's device answering → the boop → the halo in the dark → the screen and the creature → the cap and why it is metal) until the complete object sits assembled at the end, with the specs. Strength: it teaches the interaction in the order a person would discover it, and the mascot is present from the first frame. Risk: it needs discipline so every section adds exactly one idea.

**How to choose.** Ask which one makes a first-time visitor understand, within the first two scroll-lengths, that *the other person feels this*. That is the product; the hardware is the proof. If A, put the mascot on the screen before the explosion starts, so the visitor knows who lives inside. If B, make sure the assembled object appears at least once at full size before the page ends. Either way the opening must do three things in the first viewport: show the object (or its most characteristic part) rendered convincingly, state the one-line promise from the product page — *You turn it. They feel it.* — and give a visible reason to scroll.

**What is fixed regardless of structure.** The device is drawn to its true proportions (§5, §12). The three gestures — pet, boop, hold — each get their own moment. The halo gets a dark moment. The refusals get a quiet moment. The specs come last. The mascot is on the device's screen whenever the screen is shown lit.

## 4. The mascot

Design one creature that lives on the device's screen and *is the other person* — not a pet the two owners keep alive, not a brand character with a name and a backstory. It must be lovable at **126 × 294 pixels on a 10.96 × 25.58 mm landscape panel** (the long axis runs along the stick), read at arm's length, and survive being drawn at true size on the rendered device as well as blown up to fill a section.

**Character.** Soft, round, calm. One clear silhouette — a pebble, a bun, a droplet, a bean, something a thumb would want to rub — with two eyes and the smallest possible mouth. It is content at rest, curious when touched, delighted when a boop arrives, and asleep when the other person is away. It is **never** sad, hungry, sulking, dying, or disappointed. Two states only exist in the product's logic — *with you* and *away* — plus transient reactions; do not invent moods beyond those. The product page's placeholder (a peach blob with dark eyes and a blush) is a starting point you may keep, refine, or replace, but keep its warmth and its palette family (warm peach on true black) unless your research argues for a change.

**Constraints of the canvas.** True black background always — an AMOLED shows black by leaving pixels off, and the design should feel like the creature floats in the dark. At 292 ppi the panel is sharp, but the *physical* face is 11 mm tall: the creature's eyes must read at \~1 mm. Design at 1× (126 × 294) first and check it there before scaling up. Avoid outlines thinner than 2 px at 1×, gradients that band on an 8-bit panel, and anything that needs more than \~4 colours to read. Brightness on the real device will sit at 20–30 % of the panel's 450 nits, so favour saturated mid-tones over pale ones.

**States to design (each a still plus a short loop, all under 2 s and seamless):**

| State | Trigger | What it does |
| --- | --- | --- |
| Resting (with you) | Default when the other person is holding theirs | Slow breath, an occasional blink (every 4–7 s, 120 ms) |
| Away | Other person not holding | Eyes closed, dimmer, slower breath; optional small *z*; never a frown |
| Looking up | You press the crown (sent) | Eyes lift within one frame; a small open mouth; settles after \~1 s |
| Stretch | Cold radio wake (first boop after a long quiet, 2–6 s) | A deliberate stretch-and-yawn that lasts as long as the connection setup; this is the product turning a delay into character |
| Boop arrived | Other person pressed | A bounce or squash, a warm flush, then holds an alert look until the device is touched |
| Petted | Other person is turning their crown | Eyes narrow happily; a subtle purr-like shiver that tracks the click rate (slow clicks = discrete nudges; fast = a continuous purr) |
| Leaning in | Other person picks theirs up | The creature shifts a few pixels toward the viewer and widens its eyes |
| Going to sleep | 3 % battery | One yawn, then the *away* pose |

**Rules.** No text on the screen except the one plain-language service message the product shows if the subscription lapses. No hearts, no notification badges, no counters. The creature never faces away from the viewer. Its reactions are proportional: a boop is a small event, not fireworks. Motion respects `prefers-reduced-motion` by falling back to the stills.

**Deliver.** The creature as vector (SVG) with each state as a separate group; a 1× pixel-preview sheet showing every state at 126 × 294; the animation loops as CSS or Lottie/JS; and a one-page character note (what it is, what it never does) so the owner can reuse it in firmware art.

## 5. The product render

The render is the site's proof that the object exists. It must be built from the geometry in §12 — not drawn by eye — and it must look like a photograph of a real thing: mass, materials, light, shadow, and a screen that glows the way an AMOLED glows.

**Geometry.** Model the capsule at true proportions: 95 × 27 × 15 mm, stadium section, ends radiused to the section. Crown ø13 × 8 protruding 6 mm on the axis, with 48 axial serrations; a ø13.8 shoulder around it. Lens 16 × 34 mm on the front face at X ≈ 18–52, sub-flush, with a black ink border and an 11.6 × 26.2 mm clear window. The 1.5 mm ring at X = 71–72.5 spans the full section. Cap X = 72.5–95. Keyring lug on the flank at X ≈ 8–14. Four ø2 mm gold pads on the rear face at X = 34–44, 2.54 mm apart. The rear lid's parting line runs around the rear face; the crown collar hides two screws. Nothing else is on the outside — no port, no tray, no grille, no logo unless the owner adds one.

**Materials.** Body: matte, slightly warm dark polymer (reference: the product page's graphite) with a soft sheen, not gloss. Cap: machined aluminium — fine circumferential brushing, a bright chamfer at the ring edge, anodised or bare (reference: bare silver). Crown: the same metal family as the cap with visible serrations that catch light individually. Ring: clear polycarbonate that reads as glass when unlit and as a solid band of light when lit. Lens: glass with one long specular streak; the panel beneath is true black. Pads: gold. The whole object should look 48 g — dense, not toy-like.

**Lighting.** One key light, one soft fill, a rim from the halo when lit, and a contact shadow on the ground. The render should hold up in a dark environment because that is where the product lives; if the page has a dark ground, the object is lit, not the ground.

**States to render or animate.** Assembled, at rest (screen dark, halo off). Screen lit with the mascot. Halo blooming (a 400 ms warm bloom that spills onto the neighbouring cap and body surfaces, then a slow breath). Crown turning (serrations moving; a subtle 15° stepping is the honest way to show detents). Crown pressed 0.4 mm (barely visible — show it with a light change on the shoulder, not an exaggerated travel). And, if the narrative is the exploded view, the parts in §12.6 separated along the X axis in assembly order, each part recognisably itself.

**Technique is yours** — real-time 3D (Three.js / React Three Fiber with a glTF you model, or procedural geometry), pre-rendered image sequences scrubbed by scroll, or layered SVG/2D with lighting tricks. Choose by what you can make look real *and* run at 60 fps on a mid-range laptop and a phone; a scrubbed image sequence of a well-lit 3D render often beats live 3D on both counts. Whatever you pick, the assembled hero must be legible at 400 px wide and still impressive at 1600.

**Scale honesty.** Show the object at real size at least once (a *1:1 on a 96 dpi screen* frame, or against a key or a coin), and keep the screen small on the body — it is a 1.1″ panel on a 95 mm stick and the site should not inflate it.

## 6. The scroll experience

The scroll is the interface. The visitor should feel they are *operating* the story, not watching a video: the render responds to scroll position deterministically, each section resolves into a still that makes sense if they stop there, and nothing important happens only in motion.

**Principles.**

- **One idea per viewport.** Each section teaches exactly one thing (a gesture, a part, a rule) with one headline, at most two sentences, and the render doing the explaining. If a section needs a paragraph, it is two sections.
- **Scroll drives, it does not hijack.** Native scroll, no scroll-jacking, no forced snap that fights the trackpad. Pin the render (sticky) while text scrolls past it; scrub animations from scroll progress with easing on the *value*, not on the scroll. Momentum must never leave the page between states.
- **Still frames are canonical.** Every section has a resting state that is fully legible with animations disabled. Thumbnails, screenshots and reduced-motion viewers all get that state.
- **The render is continuous.** The same object carries through the whole page — turning, lighting, separating, reassembling — rather than a new image per section. Continuity is what makes it feel like a thing.
- **Pace.** Roughly 8–12 sections over 6–9 viewport-heights on desktop; 1.5–2.5× that on a phone. A progress cue (the halo as a ring that fills, or the X-axis of the device as a rule) tells the visitor where they are.
- **Interaction beyond scroll, sparingly.** Two or three moments where the visitor *does* something: drag the crown to feel the 24 detents (with a click sound if audio is opted in, silent by default), press it to send a boop and watch the *other* device answer, hold to see the creature lean in. Make them discoverable without instructions and make them optional.
- **Two devices, once.** At least one section shows both halves of the pair — what you do on yours, what happens on theirs, with the \~250 ms delay honest and visible.
- **The dark section.** One section goes near-black to show the halo in a pocket or on a nightstand — the reason the product can be face-down and still reach you.
- **End on the object and the price of nothing.** The last scroll is the assembled device, the specs, and *sold in pairs, nothing to set up*. No newsletter modal, no chat bubble.

**Motion rules.** Durations 200–600 ms for state changes, longer only for the stretch (2–6 s) and the halo breath (\~4 s). Ease-out for arrivals, ease-in-out for loops, no bounce on hardware (the creature may bounce; the aluminium may not). Never animate more than one hero element and one text block at the same time. Honour `prefers-reduced-motion` globally: scrub-driven transforms become cross-fades between stills.

**Performance budget.** First contentful paint under 1.5 s on a mid phone over 4G; the hero interactive under 3 s; 60 fps during scroll on a 2020 laptop, ≥ 30 fps on a mid phone; total transfer under 4 MB on first view (image sequences lazy-loaded per section; 3D assets under 2 MB compressed). No layout shift after load.

## 7. Content the site must carry

Use the product page's copy as written wherever it fits (the owner approved it); write new copy in the same voice — short, concrete, warm, no marketing adjectives. Sections, in whatever order your narrative dictates:

1. **Promise.** *You turn it. They feel it.* — “bingbong is a small cellular keychain you buy as a pair. Twist the crown and the person holding the other one feels every click, wherever they are. Press it and they get a boop. No phone, no app, nothing to set up.”
2. **Pet (twist).** 24 real detents, ceramic on steel, no motor; theirs clicks back in your rhythm within a quarter-second; fast turning becomes a purr. Show the crown-to-crown path: angle sensed 100×/s → cellular, ≤ 10 packets/s → their actuator.
3. **Boop (press).** Push the crown in; your creature looks up; theirs gets a low round thump and the ring blooms warm. Show the *bing…bong* waveform (two 170 Hz transients, 40 ms apart, second at 60 %) — the product page has it drawn.
4. **Hold.** Close your hand around it; their creature leans in; let go and it settles. Presence is reciprocal and never stored.
5. **The screen and the creature.** The creature is your partner, not a pet you both keep alive. States: with you / away / a boop arrived. The screen wakes when you pick it up; between glances the ring does the talking.
6. **The halo in the dark.** The 1.5 mm ring the antenna needs is the light. Arrivals stay lit until you touch it.
7. **The object.** Two pieces of metal, one piece of polymer, and the gap between them is the light. Callouts: knurled crown; the cap that is the antenna and why nothing metal lives near it (and why the keys hang on a cord); the split ring; the glass and AMOLED; the lug; sealed — no port, no tray, no speaker hole; charges on a magnetic dock.
8. **What it refuses to do.** It never says *read*. No *last seen*. No streaks, no feeding, no death. No app, no phone number, no account. Unbonding looks like a flat battery. No location — the radio can do it; the pin is left unconnected.
9. **Specifications** (from §12, stated at the precision §12.7 allows): size and weight; body and materials; crown; screen; ring; haptics; radio (LTE-M, built-in eSIM, bands 2/4/12); battery *about 3 weeks*, magnetic dock \~2.5 h; latency (\~2.6 s in conversation, up to \~90 s from cold); setup: none, sold as a bonded pair, each half can ship to a different address; years of connectivity in the box price.
10. **Footer.** A one-line honesty note: target specifications; nothing measured yet.

Where a claim in this list conflicts with §12.8, §12.8 wins.

## 8. Research and design before build

Do this work first and write it down in a `DESIGN_NOTES.md` beside the code. It is a deliverable (§11), and the owner will read it before the site.

**1. Study the category (half a day).** Look closely at how the best hardware product pages reveal an object through scroll — Apple's product pages (AirPods, Watch), Teenage Engineering, Nothing, Analogue, Rabbit r1, Playdate, Bond Touch and Lovebox (the direct competitors, whose sites show what *not* to do about apps and setup), and two or three award-winning scroll-driven sites of your choosing. For each, note in one line: how the object is introduced, how many ideas per viewport, what the scroll controls, where it fails on a phone. Then write the one-paragraph rationale for the narrative you chose (§3).

**2. Understand the visitor.** Two people: someone in a long-distance relationship deciding whether this is a gift worth \~a pair's price, and the recipient who has just been handed one and opens the box card's URL. The first needs to understand *the other person feels this* and *nothing to set up* within two scrolls. The second needs to find *hold the crown* and the refusals. Write both journeys as five-step lists and make sure the page serves each.

**3. Define the identity.** Build a small design system before any section: colour tokens (the product page's warm near-black ground, halo peach and rose, aluminium greys and true black are the starting palette; propose adjustments with reasons), a type pairing (the product page uses Bricolage Grotesque for display, Albert Sans for text, DM Mono for numbers — keep or replace deliberately; never default to Inter or a generic system stack), a spacing scale, a motion scale (§6), and the mascot's palette. Both themes: the site can be dark-first because the product is, but it must still render legibly if the visitor's system forces light.

**4. Storyboard.** Before code, produce a storyboard: one frame per section, the render state, the headline, the interaction if any, and the transition into the next. Twelve rough frames on one page. Check it against §3 (does the promise land in two scrolls?), §7 (is every required section present?) and §12.8 (does any frame over-claim?). Revise until it does.

**5. Prototype the two risks first.** (a) The render: get the assembled object looking real at hero size before anything else, and screenshot it next to the product page's render for a sanity check on proportions. (b) The mascot at 1×: draw it at 126 × 294 and view it at physical size (11 mm tall on your screen) before designing its states. If either fails, iterate there — no section work until both pass.

**6. Then build in passes** as §1 lists, screenshotting every pass at 390, 820 and 1440 px wide, and keep those screenshots in the notes.

## 9. Technical requirements

**Stack.** Your choice, with these bounds: a static, self-contained site (no server, no CMS, no analytics, no third-party trackers, no cookies). Plain HTML/CSS/JS, or a framework that builds to static files (Astro, Next static export, Vite + React). 3D via Three.js / React Three Fiber if you use it; Lottie or CSS for the mascot; GSAP ScrollTrigger or the native Scroll-driven Animations API for scrubbing. Pin exact versions. If the site will be published as a Claude artifact, note its constraints: scripts only from cdnjs/jsDelivr, all other assets inlined or as data URIs, page ≤ 16 MB — design the asset pipeline so both a normal static deploy and that mode work.

**Responsiveness.** Phone (390 × 844), tablet (820 × 1180) and desktop (1440 × 900 and 1920 × 1080) are first-class; the page must not scroll horizontally at any width ≥ 360 px. On a phone the render stays large (the object fills the width in landscape orientation on screen) and text stacks below; pinned sections are shorter.

**Accessibility.** Semantic landmarks and headings in reading order; every render state has alt text that says what changed; every interactive moment is keyboard-operable (arrow keys turn the crown, Enter presses it, Space holds) with a visible focus state; contrast ≥ 4.5:1 for text on both grounds; `prefers-reduced-motion` and `prefers-color-scheme` honoured; no content conveyed by colour alone (the halo state is also written); no autoplaying audio, and any click sound behind an explicit toggle.

**Performance.** Budgets in §6. Lazy-load per-section assets; preload only the hero. Compress image sequences as AVIF/WebP with a JPEG fallback; glTF with Draco/meshopt; fonts subset and `display=swap` with real fallback stacks. Measure with Lighthouse (≥ 90 performance and accessibility on mobile) and a real phone.

**Robustness.** Works with JavaScript disabled to the extent of showing every section's still and text. No console errors. No external requests beyond fonts and pinned CDN scripts. Works offline once loaded (service worker optional).

**Code quality.** One file per section, one place for tokens, one place for the scroll timeline; the mascot and the render are components with documented state props so the owner can reuse them in another page. README with build, run, and where each asset came from.

## 10. Double-check protocol

The site is done when every check below passes and the evidence is in `DESIGN_NOTES.md`. Run the checks yourself before handing over; if you can spawn a second reviewer (a separate agent or a fresh context), have it run checks A and B blind — it should not have seen your notes.

**A. Accuracy audit (against §2, §7 and §12).** Walk every section and list each factual claim — dimension, material, number, behaviour — next to the line in §12 it comes from. Any claim without a source line is removed or marked *to confirm*. Specifically confirm: 27 × 95 × 15 mm; crown ø13 with 24 detents (48 serrations on the knurl — not 24); 1.1″ AMOLED 126 × 294; the ring is 1.5 mm and is the light; the cap is aluminium and is the antenna; the crown does not coast; the screen sleeps; battery *about 3 weeks*; sent never read; no app; sold in pairs. Check that nothing in §12.8 *Open* is shown as fact.

**B. Visual QA.** Screenshots of every section's resting state at 390, 820, 1440 and 1920 px, in dark and light system themes, with motion on and with `prefers-reduced-motion` on. Look for: clipped text, overlapping layers, a render that is soft or aliased, the mascot's eyes unreadable at 1×, the halo bleeding where it should not, the screen inflated beyond its true proportion, horizontal scroll, and any section that is empty or meaningless when stopped mid-way.

**C. Motion audit.** Record a scroll-through at 60 fps on desktop and on a phone. Check there is no jank at section boundaries, no scroll-jacking, no double-fire of interactions, and that the crown drag, press and hold each work by mouse, touch and keyboard. Confirm the stretch, bloom and purr durations match §6 and §12.7.

**D. Performance audit.** Lighthouse mobile ≥ 90 performance / ≥ 90 accessibility / ≥ 90 best practices; transfer size on first view; frame rate during the heaviest section on a mid phone. Record the numbers.

**E. Accessibility audit.** Tab through the whole page; every interactive element reachable and labelled; screen-reader pass over the headings and alt text; contrast checker on both themes; no information only in colour or only in motion.

**F. Copy audit.** Read every line aloud. Remove any sentence that a competitor's page could also say. Check the voice against the product page. Check that the site never says *delivered*, *read*, *seen*, *last seen*, *streak*, *app*, *waterproof*, or a battery figure more precise than *about three weeks*.

**G. Aesthetic gate (the hard one).** Put the hero next to the product page and next to two of the reference sites from §8.1. Ask, in writing: does the object look real? does the page look like it was designed for this object and no other? would the owner be proud to send this link? If any answer is *no*, that is the next iteration, not a note.

**H. Freedom check.** Re-read §3. Confirm the chosen narrative was committed to fully (no half-exploded page), that the mascot appears before the visitor could lose interest, and that the assembled object appears at full size at least once.

## 11. Deliverables and acceptance

1. **The site**, as a static build plus source, runnable with one command, with a README.
2. **`DESIGN_NOTES.md`**: the §8 research (reference notes, visitor journeys, the narrative rationale), the design tokens, the storyboard, the screenshots from every pass, and the §10 audit results with numbers.
3. **The mascot package** (§4): SVG with state groups, the 1× preview sheet, the animation loops, and the one-page character note.
4. **The render assets**: the model or image sequence, its source (scene file or generator script), and a note on how to re-render a new state.
5. **A change list** against the product page: any copy you altered and why, any fact you could not verify and marked *to confirm*.

**Accepted when:** all eight checks in §10 pass with evidence; the site loads and runs on a phone and a laptop without errors; a first-time visitor can say what the product does and that there is nothing to set up after two scrolls; and the owner, looking at the hero, does not ask *is that what it looks like?*

## 12. Full product specification (extracted from the engineering report)

This is the product as engineered on 2026-09-19, condensed from the 400 kB report so the site can be built without re-reading it. Numbers are the report's; where the report tags a value as estimated (`[U]`) or unconfirmed (`[V?]`), the site may show the part but must not present the number as a measured fact. Coordinate frame: **X in millimetres along the length, X = 0 at the crown's front face, +X toward the aluminium cap.** Thickness is Z (15.0 mm outside, 12.6 mm inside 1.2 mm walls); width is Y (27.0 mm outside, 24.6 mm inside).

### 12.1 Envelope

| Quantity | Value |
| --- | --- |
| Outside dimensions | 27.0 W × 95.0 L × 15.0 T mm; \~48–50 g; corners fully radiused so the section is a 27 × 15 stadium |
| Crown zone | X = 0–16 (crown protrudes 0–6, mechanism 6–16) |
| Main body | X = 16–71: PCB substrate 16–68, copper ends at 63; the ring's inner skirt occupies 68–71 |
| Split ring (halo) | X = 71–72.5 visible web, 1.5 mm, full stadium section |
| Aluminium cap | X = 72.5–95, 22.5 mm |
| Display window | Lens 16.0 × 34.0 mm on the front face, clear window 11.6 × 26.2 mm, panel active area 10.96 × 25.58 mm at X ≈ 20–47, centred on the width |
| Keyring lug | 316L stamped lug insert-moulded in the flank at X ≈ 8–14, zero added length; a 28 mm Dyneema/POM cord ships between lug and keys so a steel key bundle never sits against the antenna |

### 12.2 Every part, crown to cap

| Part | Where (X, mm) | Size / geometry | Material and finish | What it does |
| --- | --- | --- | --- | --- |
| Crown + hub (one turned part) | −6 … +2 of the crown frame; front face at X = 0 | Cup ø13.00 × 8.00; front wall 1.30 with a 0.20 dish that steers the thumb to the axis; integral ø7.00 hub | 316L stainless, **48 straight cut serrations** (90°, 0.85 pitch, crest flat 0.10), PVD finish; Ti Gr5 is the premium alternative | Twist (24 detents per turn), press 0.40 mm to boop. Recessed 0.4 mm inside the shoulder so it is never the drop point |
| Detent race ring | Bonded inside the crown skirt | OD 10.61, ID 9.20, L 2.60; **24 grooves R0.45, 0.12 deep, 15° pitch** | Wrought 17-4PH H900 (baseline), wire-EDM grooves after hardening; zirconia and BeCu variants under test | Co-rotates with the crown; the balls drop into it |
| Balls + leaf springs | In the static sleeve nose | 2 × ø0.80 Si₃N₄ ceramic balls at 180°; BeCu cantilever leaves 0.12 × 1.5 × 4.5 mm, 0.40 N preload each | Silicon nitride; C17200 beryllium copper | Make the click: **2.4–2.9 mN·m** peak torque (target 2.5–4.0), a soft even click; no motor is involved |
| Sleeve (static journal) | Inside the bulkhead bore | Nose ø9.0, journal ø10.9, flange OD 13.20 with two retention ears | POM-C (acetal), moulded + machined | The crown rotates and slides 0.40 mm on it; carries balls, springs, seal, and the ESD bleed leaf |
| Retention C-ring + wave washer | Hub grooves | BeCu wire ø0.40 C-ring; BeCu wave washer ID 7.2 / OD 9.6 / t 0.12, 0.55 N preload | C17200 BeCu, age-hardened | Holds the crown in (≥ 100 N pull-out) and springs it back out after a press |
| Sensing magnet | In the hub's rear pocket, inside the crown's 8 mm | ø6.0 × 2.5 mm diametric NdFeB, Ni-Cu-Ni plated, concentric to 0.28 mm worst case | Neodymium | Read by the angle sensor through the bulkhead; nothing but flux crosses the seal |
| Bulkhead diaphragm | X ≈ 8.9–9.2 | LSR skin 0.30 mm over a ø9.4 opening, with a PEEK-cored pip at r = 3.3 | Liquid silicone rubber, 60 Shore A | The sealed wall; the press transfers through the pip onto the tact switch |
| Satellite PCB | X ≈ 10.5 | 22 × 10 × 0.6 mm, 2-layer | FR4 | Carries the on-axis angle sensor (MT6701, 14-bit absolute, 0.02°; AS5600L variant), **two DRV5032DU Hall latches** (always on, 1.6 µA each, wake within ≤ 77° of movement), the off-axis tact switch (Panasonic EVPBB, 1.6 N), the grip-sense passives; 10-signal flex to the main board |
| Crown-end collar + bulkhead | X = 0–16 region of the tray | Reamed ø13.30 bore, 0.15 mm labyrinth gap, debris pockets on the wide faces, buried grip-electrode ring 0.8–1.0 mm under the shoulder surface | PC/ABS tray; 316L electrode ring insert-moulded | The static shoulder your thumb bridges; the IQS211B grip sensor reads through 1 mm of plastic |
| Front tray | X = 2–71 | Closed tub: front face with the display aperture, both flanks, crown bulkhead, antenna-end wall; 1.2 mm walls, 1.5 mm local at the lens pocket | **PC/ABS**, UV-stabilised, moulded-in colour (colour not decided; the product page uses warm graphite as reference) | The body |
| Rear lid | X = 2–69, 27.0 × 67 mm | Full-width door: over-moulded LSR bead gasket (1.0 W × 0.60 H, 30 % squeeze), 12 snap hooks, 2 × M1.4 Torx T3 screws hidden under the crown collar, perimeter stiffening ribs | PC/ABS + self-bonding LSR 40–50 Shore A | IP67 closure that the owner can open with the T3 driver in the box (EU battery-replaceability rule) |
| Glass lens | Front face, over X ≈ 18–52 | 0.50 mm chemically strengthened aluminosilicate, 16.0 × 34.0, corners R1.5, black ink border, anti-fingerprint coat; sits 0.03–0.13 mm below the tray face, never proud | Corning GG3/GG5 / Dragontrail class | The only glass the visitor sees; the panel's own glass is never the outer surface |
| Display | X = 18–49 under the lens | **1.1″ colour AMOLED, 126 × 294, 292 ppi, 16.7 M colours, 400–450 nits**, 12.96 × 30.94 × 0.78 mm module, laminated to the lens with 125 µm OCA; 27-pin tail folded at X = 49–51 to a 0.4 mm board-to-board plug | RM69310 driver, 4-wire SPI | Wakes on grip, pick-up or arrival; sleeps between glances; the mascot lives here |
| Main PCB | X = 16–68 | 23 × 52 × 0.8 mm, 6 layers; **no copper on any layer for X = 63–68** (antenna keepout) | FR4, ENIG/ENEPIG | Everything electrical (§12.6) |
| Cellular SiP | X = 20–32, top side, under the panel | Nordic nRF9151, LGA 12.1 × 11.1 × 1.2 mm | — | Host MCU + LTE-M modem + RF front end, 23 dBm |
| Battery | X = 19–62, under the PCB | **23 × 43 × 6.0 mm Li-Po pouch, 560–620 mAh** (6.5 mm / 600–660 mAh only if the actuator is recessed into a PCB cut-out); on a connector, 0.6 mm swell gap kept free | Pouch with PCM (≥ 2 A trip) and 10 k NTC | The 6.0 mm cell is the ceiling of the thickness budget (0.70 mm margin) |
| Haptic actuator | X = 52–60, top side | Vybronics VG0840001D, **ø8.0 × 4.05 mm, 170 Hz, 1.0 Grms**, on a 0.2 mm brass bracket soldered to the PCB, ≥ 0.3 mm air gap to everything | Steel can | Renders the other person: braked 30 ms clicks, the 150 ms boop, the purr above \~12 clicks/s |
| Halo LED | X = 62–63 | One PLCC-4 RGB LED, 1.6 × 1.6 mm, firing into the ring's inner skirt | — | Blooms warm on arrival (400 ms), breathes while held; the only channel that works face-down in a pocket |
| Split ring (ring-disc) | Web at X = 71–72.5, skirts 68–71 (inside the tray) and 72.5–75.5 (inside the cap) | H-section, 1.5 mm visible web spanning the full stadium, 0.8 mm skirts, a sealed 5.6 × 2.1 mm aperture for the cap's feed tab | **Optical-grade clear polycarbonate**, bonded with clear 2K epoxy | Isolates the antenna from the body and is the light guide — the gap the radio needs, turned into light |
| End cap | X = 72.5–95 | 22.5 mm machined cap with an L-shaped feed tab reaching in to X = 65.5; anodised everywhere except a plated (Ni ≥ 5 µm + Au) land under the tab | **6061-T6 aluminium**, Type II/III anodise or PVD (colour not decided; product page: bare silver) | The cellular antenna. A vertical BeCu spring finger on the PCB presses on the plated land; a 5-element 0402 match tunes it for Band 12 (699–746 MHz) and Bands 2/4 (1710–2155 MHz) |
| Dock pads + shim | Rear face, X = 34–44 | 4 × ø2.0 mm gold pads at 2.54 mm pitch (GND · SWCLK · SWDIO · VBUS) on a flex bonded inside the lid; 0.3 mm 430 stainless shim behind them for the dock's magnets | Au over 1.0–2.5 µm Ni | Charging (300 mA, \~2.5 h) and programming through a magnetic dock; no USB port anywhere |

### 12.3 How the crown works (the mechanism the visitor should feel)

1. **Twist.** The crown and hub rotate on the POM sleeve. Every 15° (1.70 mm of knurl travel) the two ceramic balls drop into the next groove of the race: 24 catches per turn at 2.4–2.9 mN·m. The click is mechanical — zero firmware, zero microamps, works with a flat battery. The crown **cannot coast or free-wheel** (its inertia is \~1.25 × 10⁻⁷ kg·m²; a flick stops within the next detent). “Glide and weight” come from journal drag, budgeted ≤ 0.5 mN·m.
2. **Sense.** The diametric magnet turns with the crown. The MT6701 on the axis 1.0 mm behind the diaphragm reads absolute angle at 100 Hz to 0.02°; the two DRV5032DU latches (always on) see the first ≤ 77° of movement and wake the system, so the first millimetre of a pet is never lost. The IQS211B grip electrode in the shoulder sees a hand land 200–500 ms before the thumb moves.
3. **Press.** The crown, hub and magnet translate **0.40 mm** as a unit against the wave washer; at 0.27 mm the diaphragm pip trips the off-axis tact switch (2.9 N at the centre, 3.8 N at the rim). A hard stop at 0.40 mm absorbs over-travel. That is a boop.
4. **Seal.** A 0.15 mm labyrinth gap, debris pockets, and the LSR diaphragm. Nothing but magnetic flux and one ESD bleed leaf (1 MΩ) crosses into the sealed volume. An optional low-temperature FKM O-ring on the hub is under test.

### 12.4 The antenna end

The cap is a coupling element that excites the whole 95 mm capsule as a dipole-like radiator at 722 MHz (0.23 λ). The PCB ground is the counterpoise; the copper-free 5 mm of board plus the 1.5 mm ring form the gap. Rules the render must honour: no metal in the cap volume or within 10 mm of the ring (no cell, no screw, no actuator can, no steel keyring — hence the cord); the crown at the other end is a floating conductor. Certification gate the design targets: ≥ 12.3 % total efficiency at Band 12 (design target 15 %), honest estimate 8–18 % — **unmeasured** until the chamber run (Mule B). Feed current at full power is 0.13–0.20 A rms through one spring contact. Production RF test uses a 2.5 × 2.5 mm Murata RF switch connector on the board.

### 12.5 Electronics on the main board

nRF9151 LTE-M SiP (Cortex-M33, 1 MB flash / 256 kB RAM, Cat-M1, eDRX/PSM); MFF2 eUICC (5 × 6 mm, SGP.32 remote provisioning, factory-bonded pair); BQ25180 charger + power path (300 mA, JEITA, 25 V-tolerant input); MAX17048 fuel gauge; TPS62840 single 3.1 V rail (60 nA quiescent); DRV2625 haptic driver (active braking); TPS65631-class AMOLED PMIC (+4.6 V / −2.2 V, single-wire control from the panel) + load switches; 16 Mbit SPI NOR (art, firmware slot); PLCC-4 RGB + 3 N-FETs for the halo; IQS211B grip sense; ESD clamps on every exposed conductor; four dock pads carry SWD programming and charge. Firmware: MCUboot, LTE-M FOTA, RTT console; the UART console is compiled out because it costs +600 µA.

### 12.6 Assembly order (use this for an exploded view)

From the inside out, as the factory builds it: (1) crown cartridge — crown+hub, race, balls, leaves, sleeve, C-ring, wave washer, magnet, diaphragm, satellite PCB — built and leak-tested as one module; (2) the cartridge enters the open tray crown-first through the rear opening and seats in the bulkhead bore on a static face seal; (3) the PCBA drops onto four locating pins, its spring finger sliding under the cap's feed tab; (4) the laminated lens + AMOLED module's tail is fed through the aperture and plugged in, then the lens is pressed into its ledge on a PSA frame; (5) insulator, then the cell into its side locators, plugged in; (6) the lid — with dock flex, shim and gasket already bonded — hooks at the antenna end, rotates down, engages 12 snaps and takes two M1.4 screws at 0.025 N·m; (7) the crown-end collar snaps on and hides the screws; (8) leak test, end-of-line functional test, RF box, pair-code label, keyring cord. The ring-disc and cap were bonded to the tray earlier with clear epoxy (the tab passes through the ring's sealed aperture).

### 12.7 Behaviours, timing and power (what the site may state)

| Behaviour | Number | Status |
| --- | --- | --- |
| Own detents | 24 per turn, mechanical, instant | Fact by design |
| Their click on your device | ≤ 250 ms typical, 400 ms ceiling; rhythm restored through a 150 ms de-jitter buffer | Design contract |
| Click → purr crossfade | Above \~12 clicks/s the 170 Hz carrier is held under a 20–30 Hz envelope with slight random jitter; decays over \~600 ms when they stop; sessions taper at 15 s, stop at 20 s | Design |
| Boop waveform | One 170 Hz overdrive cycle, 18 ms braked decay, 40 ms gap, second transient at 60 % — *bing…bong* | Design |
| Boop received | 150 ms pulse + halo bloom over 400 ms; stays on the halo until touched | Design |
| Inbound latency | \~2.6 s inside a conversation window (3 min after any touch); up to \~82 s mean / \~90 s when cold — the creature *stretches* while the radio wakes | Design, unmeasured |
| Screen wake | \~100–200 ms after grip or pick-up (not 15 ms) | Estimate |
| Battery life | about 3 weeks typical (3.0–3.4 wk estimated on 560 mAh with the AMOLED; 2.0 wk if the network refuses eDRX; 1.6 wk in sustained deep coverage) | Estimate — say “about three weeks” only |
| Charging | Magnetic 4-pin dock, 300 mA, \~2.5 h to full; last-gasp “going to sleep” packet at 3 % | Design |
| Grip presence | Stable within 160 ms; strictly reciprocal; held in server RAM only, never logged | Design rule |
| Onboarding | None: factory-bonded pair, first boot “hold the crown”, both wake together anywhere on earth; re-pair via a 6-character code dialled on the crown (\~20 s) | Design |

### 12.8 Decided versus open (so the site never over-claims)

**Decided:** the 27 × 95 × 15 envelope; every material in §12.2; the colour AMOLED at 1.1″ 126 × 294 (replacing a memory LCD on 2026-09-19); the 6.0 mm cell; coaxial twist crown as the baseline; the metal cap as the antenna with a polymer plan B (Ignion NN03-310, \~105 mm body) if the chamber says no; no USB, no SIM tray, no speaker, no microphone, no GNSS, no Bluetooth, no phone app.

**Open (show as design intent, never as measured):** coaxial twist vs a transverse thumb-wheel (a blind test on ten hands decides; if transverse wins the crown zone shortens \~3 mm and the crown becomes a side wheel); the exact detent race material (17-4PH vs zirconia vs BeCu); whether the crown gets an O-ring; the antenna's real efficiency; battery life; body and cap colours and finishes; the exact AMOLED vendor part.

**Corrections to the product page the site must carry:** the crown does not coast; the screen wakes in \~0.1–0.2 s, not instantly; runtime is “about three weeks” on the 6.0 mm cell, not a bigger one.

## 13. Appendix — references, palette and files

**Geometry at a glance (mm).** Length 95; width 27; thickness 15; crown ø13 × 8, 6 proud, 48 serrations, 24 detents; shoulder ø13.8; lens 16 × 34 at X ≈ 18–52, clear window 11.6 × 26.2; panel 12.96 × 30.94 × 0.78, active 10.96 × 25.58; ring 1.5 at X = 71–72.5; cap 22.5 at X = 72.5–95; lug at X ≈ 8–14 on the flank; dock pads 4 × ø2 at 2.54 mm pitch, rear face X = 34–44; walls 1.2; internal 24.6 × 12.6; cell 23 × 43 × 6.0; actuator ø8 × 4.05 at X = 52–60; radio SiP 12.1 × 11.1 at X = 20–32.

**Reference palette (from the product page; adjust with reasons).** Ground #120F0D; surface #1B1714; text #EFE7DD; muted #A3978C; halo #FF9E76 → #FF7A8A; creature #FFD0B0 → #FFB088 → #E6754F on #000000; aluminium #EDEAE4 → #A5A29C → #5E5B57; polymer #3D3833 → #171412. Type: Bricolage Grotesque (display), Albert Sans (text), DM Mono (numbers).

**Sound, if used (opt-in only).** The click is a short dry tick, not a beep; the boop is felt, not heard — if you sonify it, it is two soft transients 40 ms apart, low, quiet.

**Files and links.**

- Product page (approved copy, render reference): https://claude.ai/artifact/Eqdui62rGSzzt9QofQwnec
- Engineering report (facts): https://claude.ai/artifact/2BzrpJdxdUFhoxMfTyU5pn — source `C:\Users\chian\Projects\bingbong\DESIGN_MANUFACTURING_REPORT_2026-09-19.md`
- Decision document (interaction spec, §7): `C:\Users\chian\Projects\bingbong\REDESIGN_DECISION_2026-09-12.md`
- Existing CAD (V1, superseded but useful for the capsule feel): `C:\Users\chian\Projects\bingbong\cad\`

**Out of scope.** No shop, no checkout, no account, no email capture, no app-store badges, no comparison table against competitors by name.

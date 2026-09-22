# bingbong — design and verification notes

19 September 2026. Working record; acceptance results are appended after the checks actually run.

## Source authority and decisions made before implementation

The supplied [brief](SITE_BRIEF.md), particularly §12, is the geometry and content contract. The local engineering report (2026-09-19) §§1, 4, 5, 7 and decision document §7 were consulted. Later report corrections override the older decision document. Both Claude artifact URLs failed through the research tool; the product page also showed a browser security check. The user explicitly confirmed **“Use the wording in the brief.”** That is the approved copy source; a local export is no longer needed. No invented pricing, connectivity term, certification, colour options or measured battery claims.

Narrative **B: feature by feature, building to the whole**. A crown alone cannot explain why someone would carry this object: another person must answer it. The first viewport therefore shows the assembled object, a tiny warm face and “You turn it. They feel it.” The next beat introduces the other half and lets a visitor turn one crown and see the other respond. The same assembled object remains through the story; proximity, light and viewpoint reveal one idea at a time. No exploded geometry. Engineering becomes the reason the touch can cross a distance, after the visitor understands the touch. The first render is a preview of the whole; the final one is an understood object.

## Reference research

Live pages researched on 2026-09-19. Browser captures, where accessible, live in `qa/references/`. Mobile observations without an actual browser capture are explicitly design risks, not measured failures. This was a focused research pass, not a claim to have spent the brief's suggested half day.

| Reference | Introduction / ideas per viewport | Scroll and mobile lesson |
| --- | --- | --- |
| [Apple AirPods Pro](https://www.apple.com/airpods-pro/) | Product silhouette and one large promise, then discrete feature panels | Object detail carries the explanation; avoid the density of the later comparison material on a phone. |
| [Apple Watch](https://www.apple.com/watch/) | Product family and a strong object image | The requested Series 11 URL redirected to the category; category content is less useful as a continuous story reference. |
| [Teenage Engineering OB–4](https://teenage.engineering/products/ob-4) | A recognisable object, then the physical controls | Borrow concrete captions and typographic restraint; mobile risk is text-heavy technical material. |
| [Nothing Phone (3)](https://us.nothing.tech/products/phone-3) | Hardware surfaces and a repeated visual language | Identity should come from the object; do not import dot-matrix decoration into bingbong. |
| [Analogue Pocket](https://www.analogue.co/pocket) | Product followed by screen and engineering explanations | Separate the emotional introduction from the specification list; avoid accessory sprawl on a narrow screen. |
| [rabbit r1](https://www.rabbit.tech/rabbit-r1) | A distinctive object colour and direct-use scenarios | Demonstrations earn space; bingbong needs only three gestures and should stay quieter. |
| [Playdate](https://play.date/) | The crank makes the unusual interaction visible | Let the crown introduce the product, and keep the product personality inside the screen. |
| [Bond Touch](https://bond-touch.com/) | Paired-touch relationship story with commerce | Communicate the receiving side immediately; bingbong's own setup story must be explicit. |
| [Lovebox](https://en.lovebox.love/) | An object as a gift and message carrier | Gift-giver and recipient have different questions; provide a recipient shortcut without introducing commerce. |
| [Lusion](https://lusion.co/) | An interactive visual establishes authorship | Borrow continuity and material lighting. Its immersive approach raises mobile performance and fallback risks. Award reference: [Lusion v3 listing](https://www.awwwards.com/websites/%23DAF0F6/?page=14). |
| [Active Theory](https://activetheory.net/) | Immersive visual experience | A useful motion benchmark, but text extraction was empty; direct visual inspection is required before asserting details. |

## Visitor journeys

Gift giver:
1. Read the promise beside a convincing, small object.
2. Turn one crown; see the other half answer. Understand the pair needs nothing to set up.
3. Try a boop and hold; distinguish rhythm, arrival and reciprocal presence.
4. Learn that silence creates no obligation and no surveillance.
5. See size, charging, coverage qualifications and target specifications.

Recipient:
1. Use “How it feels” or “Try a boop” from the navigation.
2. Find “Hold the crown” and learn the pair is already bonded.
3. Try the gestures with mouse, touch or keyboard.
4. Recognise the halo, with-you/away creature and screen sleep.
5. Read the refusals and what happens during a long quiet or low battery.

## Identity

Ground `#120F0D`; elevated ground `#1B1714`; text `#EFE7DD`; secondary `#AFA298` (slightly brighter than the supplied muted token to protect small-text contrast); accent `#FFAB88`; halo peach `#FF9E76` and rose `#FF7A8A`; display true black. Light system theme uses warm paper `#F2ECE3`, ink `#2A211C`, secondary `#6C5A4E` and burnt peach `#A04425`; the halo chapter remains dark. The product keeps its reference finishes in both themes; these are explicitly design intent.

Bricolage Grotesque display, Albert Sans reading, DM Mono annotations; self-hosted Latin subsets and swap fallback. Space scale 4, 8, 12, 16, 24, 32, 48, 64, 96. Corners belong mainly to the product and the gesture controls. Hairline rules organise the page; no grid of generic feature cards. Motion: 200 ms acknowledgement, 400 ms bloom, 600 ms purr decay; 1.8 s creature loops, 5.5 s blink cadence, 4 s halo breath; 2–6 s radio-wake stretch. Native scroll; one scene and one copy block move at a time. Reduced motion receives canonical still states.

## Twelve-frame storyboard

| Frame | Chapter / headline | Render | Interaction / transition |
| --- | --- | --- | --- |
| 1 | You turn it. They feel it. | Whole object, oblique, warm face | Scroll cue, optional gesture shortcuts |
| 2 | A little turn. A little closer. | Crown detail, second half appears | Drag crown or arrows; exact 15° steps |
| 3 | Their rhythm, in your hand. | Same pair, a crossing pulse | 250 ms petting demo; folds into pet chapter |
| 4 | A boop says enough. | Same pair, sender looks up, receiver blooms | Press / Enter, ~2.6 s demonstration |
| 5 | Just hold on. | Object and leaning creature | Hold / Space; reciprocal presence |
| 6 | Your person. Pocket-sized. | Face on the real-size panel, enlarged study beside copy | Choose with-you, away, arrival |
| 7 | A little light. Left for you. | Screen asleep, ring warm | Touch acknowledges; keep a written state |
| 8 | The gap is the light. | Ring and silver cap detail | Full assembly stays intact |
| 9 | Every part has a part. | Front/rear object, lug and charging pads | Rotate to rear; folds with frame 8 into object chapter |
| 10 | Close. Without keeping score. | Quiet assembled silhouette | Short refusals, no movement required |
| 11 | Small enough to come along. | Flat 95 mm reference at 96 CSS px/in | Explicit scale limitation |
| 12 | One for you. One for them. | Whole object, target specs | Sold as a bonded pair, nothing to set up |

Ten page sections, twelve storyboard frames; frames 2–3 and 8–9 form single related chapters. Estimated desktop length nine viewports; mobile expands to keep the product above readable copy.

## Render strategy and risk prototypes

Procedural Three.js geometry in millimetres: a stadium cross-section, separately bounded polymer/ring/cap, 48 crown serrations, 24 animation detents, precisely sized lens and panel. The generator is retained as the render asset source. A pre-rendered still is the first-paint and no-JavaScript fallback. The same model persists through the interactive story. No image-generation model is used: the engineering geometry must be deterministic. A warm peach four-colour SVG mascot is drawn at 294 × 126 landscape (the panel's native 126 × 294 pixels rotated to its installed orientation), before enlargement. Portrait/native and landscape preview sheets are both supplied to resolve the brief's orientation ambiguity explicitly.

Prototype approval and pass screenshots will be recorded below after inspection.

## Known brief contradictions, resolved explicitly

- §10F's ban on the words “app”, “read”, “last seen”, “streak” contradicts the mandatory promise and refusal copy in §7. Use these only in explicit refusals, never as capabilities or statuses. Never claim a read/delivery receipt.
- Quarter-second latency is the petting design contract, not the boop delivery target. Boop uses ~2.6 s in conversation and discloses up to ~90 s cold, all unmeasured.
- Resting and away breath loops are under 2 s as requested by §4; an occasional blink is scheduled separately every 5.5 s. The halo's 4 s cycle and radio stretch are the stated exceptions.
- The finish and coaxial crown are reference design intent; the exact vendor, finishes and antenna performance remain unconfirmed.
- Years of prepaid connectivity is a design intention with an unspecified term. Display the term as “to confirm”; do not invent a subscription duration or price.

## Prototype and implementation evidence

The first render review caught inverted exterior normals and overly reflective polymer. Both were corrected before accepting the scene prototype. Later reviews refined the black lens border, rounded cutout, halo's peach light, gold pads and curved rear seam. The 1× creature sheet was inspected at its native size: its eyes are about 1 mm on the panel; all eight stills retain the single warm silhouette. The landscape/native orientation is explicit in [the character note](public/mascot/CHARACTER.md).

| Pass | Phone | Tablet | Desktop |
| --- | --- | --- | --- |
| 1 — render prototype | [390](qa/passes/01-render/390.png) | [820](qa/passes/01-render/820.png) | [1440](qa/passes/01-render/1440.png) |
| 2 — scroll skeleton | [390](qa/passes/02-scroll/390.png) | [820](qa/passes/02-scroll/820.png) | [1440](qa/passes/02-scroll/1440.png) |
| 3 — mascot in the scene | [390](qa/passes/03-mascot/390.png) | [820](qa/passes/03-mascot/820.png) | [1440](qa/passes/03-mascot/1440.png) |
| 4 — content | [390](qa/passes/04-content/390.png) | [820](qa/passes/04-content/820.png) | [1440](qa/passes/04-content/1440.png) |
| 5 — motion | [390](qa/passes/05-motion/390.png) | [820](qa/passes/05-motion/820.png) | [1440](qa/passes/05-motion/1440.png) |
| 6 — QA refinement | [390](qa/passes/06-qa/390.png) | [820](qa/passes/06-qa/820.png) | [1440](qa/passes/06-qa/1440.png) |

These are intermediate states, not interchangeable with the final 160-view matrix. The final captures are in [qa/screens](qa/screens/); use [the review gallery](qa/gallery.html) to filter them. The [realised storyboard](qa/storyboard.png) shows the twelve planned frames using the finished model. It supplements the pre-build storyboard table above, rather than claiming that finished renders existed before implementation.

## A — Accuracy audit

The line references below are to the bundled `SITE_BRIEF.md`, so the audit is reproducible even if the original Downloads file moves. Repeated claims in specs are covered by the same row. The blind reviewer independently traced the copy before reading these notes and found no unsupported marketing number or precision claim.

| Visible claim / depiction | Source line(s) | Disposition |
| --- | --- | --- |
| Small cellular keychain, sold as a bonded pair, no setup | §2 and §12.7, line 264; decision §7.6, lines 541–550 | Preserved; signal qualifier visible |
| 27 × 95 × 15 mm; roughly 48–50 g | §12.1, line 197 | Exact envelope; mass explicitly estimated |
| Stadium section, crown zone and full assembly | §12.1, lines 197–201 | Parametric exterior; no invented internals |
| Ø13 × 8 crown, 6 mm protrusion, 48 serrations | §12.2, line 209 | Geometry/constants; no confusion with detents |
| 24 mechanical detents, 15° steps, flat-battery click, no coast | §12.3, line 233; §12.7, line 254 | Deterministic angle, no inertia |
| Ceramic on steel, no motor making own click | §12.2, lines 210–211 | Baseline mechanism, qualified crown selection in object details |
| Press travel 0.40 mm | §12.3, line 235 | Actual mesh displacement; not exaggerated |
| Sense 100 times/s, cellular ≤10 packets/s | §12.3, line 234; §7 item 2; decision §7.3 | Optional path-of-touch detail |
| Their pet: ≤250 ms typical / 400 ms ceiling | §12.7, line 255 | Unmeasured design targets; demo uses 250 ms |
| Fast turning becomes a purr above ~12/s; 600 ms decay; taper 15 s / stop 20 s | §12.7, line 256 | Copy and rate-sensitive demo; own mechanical detents continue |
| Two 170 Hz transients, 40 ms gap, second at 60% | §12.7, line 257 | Labelled waveform; no physical speaker implied |
| 150 ms arrival pulse, 400 ms bloom, halo stays until touch | §12.7, line 258 | Localised bloom and explicit acknowledgement state |
| About 2.6 s in conversation / up to ~90 s cold | §12.7, line 259 | Both explicitly unmeasured targets; demo delays separately tested |
| 2–6 s radio stretch, local look-up about 1 s | §4 state table, lines 65–66; decision §7.2 | 6 s stretch in cold simulation; alert timing does not imply instantaneous radio delivery |
| Reciprocal, ephemeral presence; hold / release | §12.7, line 263; decision §7.4, lines 521–530 | Nothing logged or transmitted by this website |
| First boot “hold the crown”; presence off, boops on | §12.7 line 264; decision §7.4/.6 | Recipient detail; no invented setup flow |
| Creature is the other person; with-you / away; no negative moods | §4 and decision §7.5, lines 531–540 | Two stable states plus transient reactions |
| 1.1″ colour AMOLED, 126 × 294; screen sleeps | §12.2, line 221; engineering report lines 34–35 | Native art and small physical panel; no always-on screen claim |
| Pickup wake about 0.1–0.2 s | §12.7, line 260 | Labelled estimated in fine print |
| 0.5 mm glass; 16 × 34 lens; clear 11.6 × 26.2; active 10.96 × 25.58 | §12.1 line 202; §12.2 line 220 | Model uses the distinct sizes; active surface remains sub-flush |
| Matte PC/ABS body, machined 6061-T6 cap | §12.2, lines 218 and 228 | Reference graphite/silver only; finishes to confirm |
| 1.5 mm optical-PC ring is isolation and light guide | §12.2, line 227 | Full stadium ring at X=71–72.5 |
| 22.5 mm cap is part of the cellular antenna | §12.1 line 201; §12.2 line 228; §12.4 line 240 | No measured RF efficiency claim |
| Cord/lug keep metal keys away from antenna | §12.1 line 203; §12.4 line 240 | Lug at crown end; no key bundle placed beside cap |
| Four gold rear pads; Ø2 mm / 2.54 mm pitch | §12.2, line 229 | Visible in rear view with updated alt text |
| Sealed, no port/tray/speaker hole, magnetic dock | §12.2 line 229; §12.8 line 268 | No water image or certification claim |
| LTE-M, built-in eSIM, bands 2/4/12 | §12.2 line 228 and §12.5 line 244 | Specs; coverage required |
| About three weeks battery, about 2.5 h charge | §12.7, lines 261–262 | Estimated / target labels; no precise runtime |
| 3% low-battery sleep message | §12.7, line 262 | Detail text; one yawn then away in reusable renderer |
| Sent, never read receipts; no last seen/streaks/feeding/death/location/history/account | §7 item 8; decision §7.4/.5 | Explicit refusals only, never capabilities |
| Unbonding looks like flat battery; service-lapse exception | decision §7.4/.5 | Calm away semantics; no fabricated service URL or message |
| Split shipping and connectivity in box price | §7 item 9; decision §7.6 | Shipping is planned; term and price visibly to confirm |
| Target specifications; nothing measured | §12.8 and required footer | Visible footer and expanded details |

The public copy has no exact subscription duration, price, certified IP rating, location service, app dependency, read status, unapproved colour choice, or oversized-cell runtime. The older coast / 15 ms / indefinitely-on-screen claims were rejected. [The change list](CHANGE_LIST.md) records the editorial decisions.

## B — Visual audit

160 canonical views: ten chapters × four sizes (390×844, 820×1180, 1440×900, 1920×1080) × two themes × two motion settings. Full-page no-JavaScript captures at 390/1440 and overflow checks at 360/390/820/1440 supplement the matrix. Every automated width check passes. The physical-size ruler and model agree at 359.055 CSS px (359.047 reported after browser subpixel rounding), including at 360 px width. The screen has not been enlarged to make the creature easier to see.

The independent reviewer found and verified fixes for: receiving halo retained between chapters, delayed boops changing unrelated chapters, stale creature alt/selection, incomplete rear seam, slow-pet reaction not restarting, a previous fade interrupting a new burst, over-bright lens/pads, clipped shadow texture, overlapping pair labels, utility-text collision, and mismatched ruler size. The final targeted blind review reported **all three remaining fixes pass; no remaining blockers from its findings; no page errors**. It never read this document. Canonical poses are legible without motion; no-JavaScript mode shows each still and the entire copy.

## C — Motion and interaction audit

Meaningful automated tests verify 15° increments by button/keyboard/mouse/touch, no coasting, receiver response, purr settling, boop not arriving prematurely, the 2.6 s response, hold/release, clearing the halo, rear view, audio opt-in, and isolation of pending callbacks from other chapters. Additional delivery tests cover Enter, the ~1 s local look-up, a cold radio stretch, and the 90 s arrival with an accelerated browser clock. Those clock tests validate scheduling, not a real radio.

The independent review instrumented the canvas: isolated slow clicks now nudge; a 15-click burst after a 650 ms pause becomes a purr. Reduced motion draws canonical stills. The hardware has no bounce or free-running spin. No wheel/touch-scroll cancellation, forced snapping or scroll library is used. Pointer capture is confined to the crown and hold control. The paired sequence is contiguous across pet and boop; it does not reappear as unrelated decorative pairs.

[Desktop recording](qa/motion/desktop.mp4) and [phone-emulation recording](qa/motion/phone-emulation.mp4) use CDP capture at native refresh cadence and 60 fps MP4 encoding. Actual capture rates, durations and any frame duplication are recorded in [recordings.json](qa/motion/recordings.json), rather than calling an emulation a physical phone recording. A real handset recording is still required for the brief's physical-device check.

## D — Performance audit

See the machine-readable metrics below and [Lighthouse HTML](qa/lighthouse-mobile.report.html). The first build scored 64 performance: synchronous WebGL setup was unnecessary startup work. The final approach sends canonical locally generated images first, subsets the fonts, inlines the small stylesheet and loads live 3D on actual scroll/pointer/keyboard intent. The core interaction handlers are already present when the still is displayed; the live scene catches up to their current state. There is no timer that waits out an audit.

The standalone static build is about 1.24 MB uncompressed, including all chapter stills, shaders, fonts, art and documentation; the first-view Lighthouse transfer is much smaller. Both are below 4 MB. The separate single-file artifact is about 2 MB, below the 16 MB artifact limit. No raster sequence or compressed glTF download is needed. FPS numbers describe this Windows Chrome environment, not an invented 2020-laptop or physical-phone result.

## E — Accessibility audit

Semantic header/nav/main/sections/footer and labelled product/progress/control regions; exactly one h1, followed by chapter h2s in reading order. The product description changes with each canonical state; the rear view and creature selections have explicit descriptions. All controls have visible focus. Arrow keys turn; Enter presses; Space holds; releasing or blurring ends a hold. Status text accompanies the halo and boop. Sound begins off and requires an explicit toggle. Text contrast is tested in both themes and the dark halo state; the light-theme footer contrast issue found in the first run was fixed. The 53-check suite reports zero axe violations. Lighthouse accessibility is 100. A human screen-reader pass remains distinct from these automated checks.

## F — Copy audit

All section text was reviewed against the brief for short, concrete sentences. The exact promise and gesture words are retained. New headlines describe this device's turn, thump, hand, screen, light or refusal. Optional technical detail sits behind native disclosure elements. On-screen art has no text, hearts, counts, badges or invented moods. The explicit negative phrases containing “app”, “read”, “last seen” and “streaks” fulfil the required refusal content; the blanket §10F word ban cannot override those required statements. The footer and qualification text prevent target specifications becoming measured claims.

## G — Aesthetic gate

**Does the object read as a real small thing?** My review: yes as a design visualisation. Distinct dark polymer, cut crown, black lens, narrow peach ring and silver cap carry the silhouette; a subtle contact shadow supplies weight. The exact physical dimensions matter more than enlarging its display. It is not presented as a photograph of an already manufactured unit.

**Does this page belong to this object?** Yes: three physical gestures, one carried presence, antenna gap as light, and refusals organise the experience. The same complete object persists; it is not a interchangeable feature-card layout.

**Ready for the owner to send?** Ready as a review build, with owner visual approval still outstanding. [Playdate's captured hero](qa/references/playdate-1440.png) was useful for control-led personality. [Lusion](qa/references/lusion-1440.png) and [Active Theory](qa/references/active-theory-1440.png) only reached their loading screens in this browser; they are honestly marked as incomplete visual comparisons. Other official pages were text-researched, but several browser navigations failed DNS; the results are in [the reference log](qa/references/results.json). I cannot claim the brief's full side-by-side reference gate passed when the actual reference render was not accessible. The user-authorised brief now governs copy and palette.

## H — Freedom check

Narrative B is committed throughout. The first viewport contains the complete characteristic object, the exact promise, warm creature and visible scroll cue. The second chapter shows the other device reacting and repeats no setup through the initial story. Pet, boop and hold each have a moment; the halo has a dark chapter; refusals get a quiet screen-off pose; specs come last. There is no half-exploded scene. The assembled object is both hero-sized and shown in an explicit 96 dpi scale frame. Visitor comprehension and owner resemblance must still be confirmed by people rather than self-certified.

## Acceptance boundary

Implementation, static distribution, single-file distribution, reuse assets and automated/browser verification are delivered. Remaining human/external checks: a real mid-range phone and 2020-class laptop measurement, a human screen-reader pass, first-time gift-giver/recipient comprehension, a successful full visual comparison against the unavailable reference pages, and the owner's assessment of product resemblance. These are not marked passed. No deployment, purchasing flow or external publication was requested or performed.

<!-- MEASURED_RESULTS -->

## Final measured results

Generated from the saved reports, 2026-09-20.

| Check | Result |
| --- | --- |
| Lighthouse performance | 100 / 100 |
| Lighthouse accessibility | 100 / 100 |
| Lighthouse best-practices | 100 / 100 |
| First Contentful Paint | 1.1 s |
| Largest Contentful Paint | 1.7 s |
| Total Blocking Time | 50 ms |
| Cumulative Layout Shift | 0 |
| Time to Interactive | 1.7 s |
| Avoids enormous network payloads | Total size was 135 KiB |
| Main automated checks | 53 / 53 pass |
| Delivery / offline / artifact checks | 15 / 15 pass |
| Canonical screenshots | 160 |
| Browser exceptions | 0 |
| Engagement → live 3D, local Chrome | 816.1 ms |
| Scroll frame sample 1440 | 60.00 fps; p95 17.0 ms |
| Scroll frame sample 390 | 60.01 fps; p95 16.9 ms |
| desktop capture | 59.46 fps over 31.99 s; 60 fps encode |
| phone-emulation capture | 59.95 fps over 41.98 s; 60 fps encode |

Lighthouse uses its mobile simulation defaults in installed Chrome; the app is loaded over local HTTP with network/CPU simulation. First-view transfer excludes the later, intentional offline pre-cache in a service worker. Even the entire uncompressed static distribution is approximately 1.24 MB, below the 4 MB limit. Core interaction readiness and live scene setup are separately measured. Physical-device checks remain pending as described above.

Evidence: [main results](qa/results.json), [delivery results](qa/delivery-results.json), [Lighthouse JSON](qa/lighthouse-mobile.report.json), [motion metadata](qa/motion/recordings.json).

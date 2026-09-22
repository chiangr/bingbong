# bingbong — redesign notes

## Direction and authority

The user rejected the first build's clunky movement, warm Claude-associated palette and still-image presentation. The new instruction explicitly supersedes the brief's UI palette, font and presentation constraints. It retains the product facts and the pet / boop / hold demonstrations the user liked.

This is a new visual treatment: midnight-blue ground, cool grey text, silver hardware and violet interaction accents. The peach creature and physical halo retain their product role. The system's light setting does not switch the site back to cream or paper. Albert Sans replaces the first build's heavier display face; DM Mono is limited to small labels. Text, control size, spacing and restraint carry the identity.

The opening is centered and dominated by the object. The narrative then gives the demonstrations a consistent control position; the creature chapter reverses the composition. Navigation and technical detail are quieter. Material, dimensions and behavior are never replaced by aesthetic invention.

The first build is archived in `revisions/first-build/`. Its research and claim register remain useful source records, but its palette decisions, screenshots and benchmark scores are historical and do not describe this version.

## The actual animated object

One Three.js scene starts automatically. There is no interaction gate and no product-image swap during normal browsing. The product consists of independently modeled polymer, lens, screen, crown, optical ring, antenna cap, lug, cord, rear seam and charging pads. The same geometry supports the hero, demonstrations, inspection and rear view.

The renderer has a single drawing loop. Native scroll drives one lightly smoothed coordinate, from which the timeline samples every position, scale and visible state. The track spans each transition with a gentle arch when the composition changes sides. The active chapter only selects copy and controls; it no longer determines discontinuous object states. Stopping retains an intermediate pose, and reversing retraces the same route.

Screen brightness and halo emission fade continuously. The second object enters from below. Mobile clipping, stage background and view controls share the object's scroll progress, removing the former hero-to-story jump. Ambient movement fades out approaching the scale reference. Body inspection and rear-view offsets blend back into the chapter composition as the visitor scrolls away; pending demonstrations still cancel when leaving a chapter. The crown shortcut uses native smooth scrolling and starts the boop after arrival.

Reduced motion removes ambient movement and the brief scroll catch-up. It keeps position tied directly to the user's scroll through the same continuous path, avoiding the previous instantaneous pose switches. There is no scroll interception or snapping.

The earlier model averaged end-face normals into the cap, producing distorted reflections. The replacement samples the flat faces and curved sides separately and uses analytical normals, including the end bevel. A controlled studio environment lights matte graphite, satin silver, true-black glass and the peach ring.

The studio's filtered reflection samples are baked into a 21 KB map. This is lighting data, not a product image. It removes runtime environment generation. Parallel shader compilation and task yields reduce cold-load blocking. Halo lights remain in the scene's light list when the second device is hidden, avoiding a new light-count shader variant while scrolling into a pair.

Rendering pauses in a hidden tab. Reduced motion stops ambient geometry and creature loops; manual controls remain functional. The graphics context can be lost and restored without removing the page or its content. Still renders are generated from this model exclusively for no-JavaScript and unavailable-WebGL fallback.

## Demonstrations retained

| Action | Behavior |
| --- | --- |
| Turn | 15° detents; corresponding receiver reaction after the 250 ms demonstration delay |
| Faster turn | Rate-sensitive purr; settles after stopping; crown does not coast |
| Boop | 0.4 mm local crown press; looking-up reaction; receiving halo after 2.6 seconds |
| Cold boop | Stretch during the wake interval; arrival after 90 seconds |
| Hold | Creature leans in while held; settles on release, cancellation or focus loss |
| Halo touch | Acknowledges and clears the waiting arrival |
| Inspect | Body drag, keyboard rotation, reset, and an animated rear view |

Leaving a chapter cancels its pending timers and re-enables controls. Returning to a cold demo cannot leave it disabled for an old 90-second timer. Copy explains that the visitor can stay to watch it arrive or continue exploring. Demonstrations are simulations, and actual latency figures remain unmeasured design targets.

## Accuracy and copy audit

The full original source register is retained under the archived first-build notes. The redesign preserves the following physical and behavioral authority:

| Claim / geometry | Authority in SITE_BRIEF.md |
| --- | --- |
| 27 × 95 × 15 mm envelope | §12.1 |
| Polymer body; 6061-T6 aluminium cap; cap participates in the antenna | §12.2 |
| Ø13 mm crown; 24 detents; 48 serrations; no coast | §12.3 |
| 34 × 16 mm lens, 25.58 × 10.96 mm active area, 126 × 294 AMOLED | §12.2 / §12.5 |
| 1.5 mm optical ring is both antenna gap and halo | §12.2 / §12.7 |
| 170 Hz haptic response | §12.5 |
| Pet, boop, hold and reaction timing | §12.7 |
| Screen sleeps between glances; estimated 0.1–0.2 s wake | §12.7 |
| About three weeks battery, explicitly estimated | §12.7 / §12.8 |
| Bonded pair; no phone, account, read receipts, location or scorekeeping | §7 / §12.7 |
| Finish, vendor, crown choice, runtime, RF results, service term and price remain open | §12.8 and the brief's unresolved commercial details |

The short opening now combines existing brief wording. The core promise is unchanged. Demo names and the mascot remain. No price, purchase flow, measured battery claim, certified rating, new finish option or RF performance claim was introduced. Reference finishes are qualified as design intent in the object chapter.

## Redesign review and fixes

A separate reviewer was requested in the original brief §10. That reviewer examined the redesign without reading this document. The review covered factual consistency, 40 chapter/width samples, mouse drag, touch streams, keyboard gestures, reduced motion and cold-demo cancellation.

Findings addressed:

- Moved mobile rotation controls into the reserved product area so they cannot cover waveform or specifications.
- Moved the sound control into the header and removed the redundant tablet hero gesture row where it collided with view controls.
- Aligned the tablet's 95 mm rule with the model's actual center.
- Fixed the touch-capture handoff: a descendant canvas losing implicit capture must not cancel the parent that just acquired it. An 85 px drag now produces the full 0.68-radian rotation.
- Motion recording exposed a brief crossover behind the creature headline. The object now lifts and reduces in size while changing sides; the phone stage stays opaque behind its view controls.
- Added a named region for the product view controls and expanded chapter targets to at least 24 × 24 px.
- Replaced runtime lighting generation with the baked reflection map and asynchronous shader setup after profiling cold-load stalls.

The reviewer reported no remaining blockers on the reviewed paths, no factual inconsistency, and no page error or horizontal overflow. [Review captures](qa/redesign/reviewer) include both findings and targeted fixes. The automated suite separately exercises context loss and recovery.

## Verification scope

The functional results below cover the scroll revision; the earlier Lighthouse page-load benchmark is explicitly dated as a redesign baseline. The main matrix contains 160 chapter captures: ten chapters, four widths, both system themes and both motion preferences. The additional scroll suite measures the actual rendered object and mobile stage across all nine boundaries, down and back up, in normal and reduced motion. It also checks intermediate stops, reversal, wheel input, rear inspection and navigation into the boop demonstration. Theme coverage verifies that the intentionally fixed dark design is robust to either OS setting. Additional checks cover 360 px, no JavaScript, offline behavior, keyboard, real browser touch event streams, live pixel changes, rotation, and context recovery.

The performance work reduced cold-load blocking substantially while keeping the model live from startup. The original still-first build's 100 performance score is not a score for this redesign. Current cold-load measurements, including any shortfall from the original brief's Lighthouse target, are reported below rather than hidden by delaying the 3D scene until interaction.

Remaining external checks: a physical mid-range phone and 2020-class laptop, a human screen-reader pass, first-time visitor comprehension and the owner's visual judgment. Browser emulation does not establish those results. The exterior is a design visualization, not a manufactured-product photograph or production CAD. No external deployment was requested or performed.

<!-- MEASURED_RESULTS -->

## Saved measurements and current functional checks

Generated from the saved reports, 2026-09-20 UTC. Scroll regression checks: 2026-09-20T08:10:07.332Z. The Lighthouse page-load benchmark was recorded 2026-09-20T04:42:27.342Z; it predates the scroll revision and is retained as the redesign baseline.

| Check | Result |
| --- | --- |
| Lighthouse performance | 90 / 100 |
| Lighthouse accessibility | 100 / 100 |
| Lighthouse best-practices | 100 / 100 |
| First Contentful Paint | 1.4 s |
| Largest Contentful Paint | 2.0 s |
| Total Blocking Time | 380 ms |
| Cumulative Layout Shift | 0 |
| Time to Interactive | 2.7 s |
| Avoids enormous network payloads | Total size was 205 KiB |
| Main automated checks | 53 / 53 pass |
| Live model / touch / context checks | 21 / 21 pass |
| Delivery / offline / artifact checks | 15 / 15 pass |
| Scroll continuity / reverse / navigation checks | 28 / 28 pass |
| Canonical screenshots | 160 |
| Browser exceptions | 0 |
| Script startup → live 3D, local Chrome | 332.5 ms |
| Scroll frame sample 1440 | 60.00 fps; p95 16.9 ms |
| Scroll frame sample 390 | 60.00 fps; p95 17.0 ms |
| desktop capture | 60.02 fps over 31.99 s; 60 fps encode |
| phone-emulation capture | 60.01 fps over 42.01 s; 60 fps encode |
| Entire static distribution, uncompressed | 1.17 MB |

Lighthouse uses its mobile simulation defaults in installed Chrome, over local HTTP. The transfer metric excludes later offline pre-caching. The saved baseline cold-load performance is 90/100; this meets the brief’s 90-point target. Live rendering has not been deferred until interaction to change that measurement. Physical-device checks remain pending.

Evidence: [scroll continuity results](qa/scroll/results.json), [desktop transitions](qa/scroll/overview-1440.png), [mobile transitions](qa/scroll/overview-390.png), [main results](qa/results.json), [live scene results](qa/redesign/live-results.json), [delivery results](qa/delivery-results.json), [Lighthouse report](qa/lighthouse-mobile.report.html), [screenshot gallery](qa/gallery.html), [motion metadata](qa/motion/recordings.json).

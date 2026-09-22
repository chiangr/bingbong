# The person in your pocket

A warm peach pebble, with a slightly uneven crown, two large dark eyes and the smallest smile. No name, backstory, limbs, accessories or collecting system. It is the other person, never a third creature the pair must maintain.

The native panel is 126 × 294 pixels. Installed landscape it is 294 × 126, representing 25.58 × 10.96 mm. The landscape sheet is drawn at exactly one source pixel per displayed pixel. The native portrait sheet rotates the same art, without resampling. The creature spans roughly 108 × 90 pixels, with 11-pixel-wide eyes (~0.96 mm). View `landscape-preview.png` without scaling; then view its panels at 96.68 × 41.42 CSS pixels for the 96 dpi physical reference. Device scaling and zoom affect actual physical size.

Four solid colours: body #F5A078, highlight #FFC29D, underside/cheek #DE7252, face #352019. All sit on true black. No gradient, no fine outline, no glowing pale face. Slight asymmetry and a broad base keep the silhouette soft and recognisable at small sizes.

Persistent states: **with you** (resting, content) and **away** (peacefully asleep, dimmer). Everything else is a transient reaction: looking up after a local press; stretching while the radio wakes; a small boop bounce and flush; happy narrowed eyes that nudge with clicks and shiver during a purr; leaning toward the viewer during reciprocal holding; one yawn before the low-battery sleep pose. It always faces the viewer. A boop's alert pose lasts until touch; the halo carries the arrival after the screen sleeps.

It never becomes sad, hungry, sulky, disappointed, dying, or demanding. There are no hearts, badges, counters, messages, progress meters, text or earned rewards on its screen. The sole exception to wordless art is the product's plain-language service-lapse message; this art package deliberately does not invent its final wording or support URL.

`states.svg` contains separately named groups, selectable by fragment (#resting, #away, #looking-up, #stretch, #boop, #petted, #leaning, #sleeping). Individual SVG stills are also included. `loops.css` defines the reusable loops; `src/components/mascot.js` supplies the equivalent canvas drawing used on the rendered AMOLED. Loops are at most 1.95 s. Blink is a separate 120 ms event every 5.5 s. Radio stretch repeats for 2–6 s; the receiving radio can take up to ~90 s from cold, which must not be misrepresented as the stretch duration. Reduced motion shows canonical stills.

Firmware handoff: use partial-window redraws, preserve the true-black background and minimum face marks, map stable presence only to resting/away, and never make delivery acknowledgement look like a read receipt. These are illustration source assets, not a claim that target hardware, panel brightness, frame rate or colour calibration has been validated.

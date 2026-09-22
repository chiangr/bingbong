# bingbong — the live object edition

A new visual direction built around an animated, inspectable 3D product. Midnight blue, cool silver, violet, clean typography, and the original pet / boop / hold demonstrations. This replaces the first build's warm palette and still-first presentation, as requested.

## Run

Dependencies are installed. From this directory:

```sh
npm run dev
```

Open http://localhost:5173. On a fresh checkout, run `npm ci` first; use Node 22.12+ or 24.

`npm run build` creates `dist/`. `npm run preview` serves it at http://localhost:4173. The production preview is currently running. Use http://localhost:4173/?v=3 to open the continuous-scroll revision from a browser that cached an earlier build.

Deploy the contents of `dist/` to a static host at the domain root. No server, account, telemetry, external runtime request, or purchase flow is needed. The local service worker makes the site available offline after a complete load. Navigation prefers the network so revisions are visible; cached content remains available offline.

`npm run artifact` produces `artifact/bingbong.html`. This standalone version includes the code, fonts, lighting map, and fallback assets. Open it directly in a browser; no local server or CDN is required.

## Interact

- Drag the **body** to rotate the object. Horizontal touch dragging rotates; vertical swiping keeps normal page scrolling. The view controls also work with keyboard activation.
- Drag the **crown**, or use its arrow keys, to turn in 15° detents. Enter boops; holding Space shares presence.
- Use the chapter's turn, boop, and hold controls to try the paired-device demonstrations.
- Use **Turn it over** for the rear charging pads. Rotation and rear-view transitions use the same live geometry.
- Scroll carries the same object between compositions. Position, scale, screen brightness, halo, mobile clipping and view controls follow the same continuous track; reversing scroll retraces it.
- Sound is opt-in. Reduced motion stops ambient movement and scroll catch-up; the object follows the user's scroll directly and retains manual interaction.

## Source

| File | Responsibility |
| --- | --- |
| `src/experience.css`, `src/tokens.css` | New layout, responsive behavior, palette, typography |
| `src/sections/` | Ten chapters of static, accessible content |
| `scripts/build-page.mjs` | Generates HTML, navigation, and accessible controls |
| `src/main.js` | Immediate scene startup and chapter coordination |
| `src/timeline.js` | A single scroll coordinate drives continuous poses and visual states |
| `src/components/scene.js` | Live rendering, damped transforms, drag rotation, context recovery |
| `src/components/product-model.js` | Parametric exterior in millimetres; materials, crown, display and halo |
| `src/components/studio.js` | Source of the studio lighting environment |
| `src/components/mascot.js` | Original wordless creature and animated reactions |
| `src/interactions.js` | Pet, boop, hold, sound and timer lifecycle |
| `public/mascot/` | Reusable SVG states, PNG sheets, loops and character note |
| `public/lighting/` | Prefiltered reflection map; the object itself remains live geometry |
| `public/renders/` | Generated stills for no-JavaScript / unavailable-WebGL fallback only |
| `qa/` | Screenshots, gesture tests, motion recordings and reports |

With the dev server running, `npm run assets` regenerates fallback stills. `node scripts/bake-lighting.mjs` regenerates the lighting map from the studio source. Shader compilation runs asynchronously; expensive environment prefiltering happens when generating assets, not on each visitor's device.

## Verify

With the production preview running:

```sh
npm run qa
node scripts/live-check.mjs
node scripts/scroll-check.mjs
node scripts/delivery-check.mjs
node scripts/lighthouse.mjs
```

QA uses installed Google Chrome through Playwright. The main suite captures every chapter at 390, 820, 1440 and 1920 px, in both system themes and motion settings. The fixed midnight palette is intentional in both themes. The scroll suite measures rendered movement across every chapter in both directions, including reduced motion, intermediate stops, screen/halo fades, mobile clipping, wheel input and boop navigation. Additional checks cover 360 px, touch, keyboard, live startup, object rotation, graphics-context recovery, no JavaScript, offline reload and the standalone file.

See [DESIGN_NOTES.md](DESIGN_NOTES.md) for measured results and limitations. Browser-emulated touch/performance is not a physical-phone test.

The physical facts and wording come from `SITE_BRIEF.md` and the local engineering reports. Final finishes, crown selection, runtime and RF results remain design intent. Fonts are self-hosted under the SIL Open Font License; licences accompany them. Three.js's MIT notice is in `public/THIRD_PARTY_NOTICES.txt`. The original build's source, static archive and notes are preserved locally in `revisions/first-build/`.

`scripts/export.ps1` creates source, static and review ZIPs. The source includes historical notes; the review archive holds screenshots, results and videos separately. Extract both into the same directory to follow the evidence links. Raw screencast frames and dependencies are excluded.

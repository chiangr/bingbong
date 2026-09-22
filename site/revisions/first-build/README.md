# bingbong — You turn it. They feel it.

A static, scroll-driven product story built from the September 19 brief. The engineering documents in the parent directory remain untouched.

## Run

From this directory, **`npm run dev`** starts the site at <http://localhost:5173>. Dependencies are installed in this workspace. On a fresh checkout use `npm ci` first (Node 22.12+ or 24).

`npm run build` produces `dist/`. `npm run preview` serves that production build at <http://localhost:4173>. Deploy the contents of `dist/` to any static host at the domain root. No server, database, account, analytics, cookie or third-party runtime request is used. The local service worker caches the static app for offline use after its first complete load; no gesture or presence data is stored.

`npm run artifact` produces `artifact/bingbong.html`, a self-contained HTML version with the scripts, fonts, render stills and mascot assets inlined. It can be opened directly in a browser or used as the artifact source; it needs no CDN. Its build prints the byte size. This is a prepared file, not a claim that it has been published to Claude.

## Structure

- `src/sections/`: one content module per chapter; `scripts/build-page.mjs` emits real HTML so every section remains readable without JavaScript.
- `src/tokens.css`: colour, type, spacing and motion tokens. Both system themes are supported; the halo chapter stays dark.
- `src/timeline.js`: the native-scroll timeline, canonical poses and reduced-motion states.
- `src/components/product-model.js`: source model built in millimetres, with documented dimensions and state props.
- `src/components/scene.js`: one persistent Three.js scene. The first frame is a pre-rendered asset; live 3D starts on scroll, pointer or keyboard intent.
- `src/components/mascot.js`: reusable vector/canvas artwork and state props.
- `src/interactions.js`: keyboard, pointer and touch gesture demos. The 250 ms pet and 2.6 s / 90 s boop demos are explicitly simulations.
- `public/mascot/`: eight stills, grouped source SVG, native and landscape preview sheets, loops and the character note.
- `public/renders/`: canonical stills generated from the same model; no stock or AI-generated product pictures.
- `qa/`: screenshots, automated checks, Lighthouse reports, recordings and source/research evidence.
- `DESIGN_NOTES.md`: rationale, source traceability, review findings and the acceptance record.

## Regenerate and check

With `npm run dev` running, `npm run assets` regenerates render stills and their crown hit-target coordinates. `node scripts/prototype.mjs` regenerates the mascot stills and preview sheets. `node scripts/pass.mjs <pass-name>` captures 390, 820 and 1440 px hero views. The QA scripts use installed Google Chrome through Playwright; select another Playwright channel if your machine differs.

With the production preview running, `npm run qa` captures all ten sections at 390, 820, 1440 and 1920 px in both colour schemes and motion modes; it also runs meaningful gesture, timing, no-JavaScript and accessibility checks. `node scripts/lighthouse.mjs` runs Lighthouse mobile. `node scripts/delivery-check.mjs` verifies offline and single-file behavior. See the notes for the exact measured environment and outstanding human checks.

Font subsets were downloaded from Google Fonts: Bricolage Grotesque, Albert Sans and DM Mono, all under the SIL Open Font License. Original URLs are in `qa/font-source.css`; licences are beside the fonts. `scripts/subset-fonts.py` reproduces the smaller subsets from `qa/font-originals/` using fontTools and Brotli. Bricolage's unused optical-size and width axes are fixed at their defaults; weight variation is retained. Runtime dependencies are pinned exactly, and `package-lock.json` records the full tree.

## Source authority

The user confirmed the brief's wording and palette are the approved reference. `SITE_BRIEF.md` is the supplied brief. The local engineering report overrides the older decision document for physical facts. Copy is short, with explicit qualifications for estimates and open decisions. No price, connectivity term, certification, extra colour option or measured battery claim was invented.

The render is an exterior design visualisation from the given geometry, not production CAD. Final supplier drawings, finishes, crown choice and RF results remain unconfirmed. Real-device testing and owner acceptance cannot be replaced by browser emulation; the notes distinguish these from checks that actually ran.

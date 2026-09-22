# Session handoff — 2026-09-22

## Purpose and branch

The owner asked to push the latest work to a remote branch so another session on another laptop can analyze and run it. Branch: `codex/assembly-handoff-2026-09-22`, repository: `chiangr/bingbong`, based on `master` commit `03cc4d531419522e5f15c9e767b589ef1ed75f8b`.

The branch mirrors the original project folder layout. The previous remote contained only the `firmware/` directory's contents at its root; that history is preserved, with those files moved under `firmware/`. Local uncommitted PCB changes, supporting analysis and current project siblings were copied into an isolated worktree. The original local firmware checkout and the remote default branch were not changed.

On the original workstation, the Git worktree for this handoff is `.worktrees/assembly-handoff-2026-09-22/` beneath the project folder. The original project folder itself is not a Git repository. Make subsequent Git edits from that worktree or from a fresh clone, rather than assuming edits in the original sibling folders automatically update this branch.

For an existing clone, fetch and check out the branch with ordinary `git fetch origin` and `git switch --track origin/codex/assembly-handoff-2026-09-22`. Preserve any existing edits before switching.

## Accepted product and visual direction

- The owner rejected the original Claude-associated warm/white UI and still product pictures. The approved direction is midnight blue, cool silver, violet, Albert Sans and DM Mono, with real procedural Three.js geometry. The brief's older palette/UI instructions are superseded by that explicit preference.
- Preserve the pet, boop, hold, halo and creature demonstrations. The owner specifically liked them.
- The owner then requested smooth scroll-linked travel between sections. The same object, camera, visibility and lighting channels now follow one continuous native-scroll timeline. Avoid reintroducing section-boundary pose swaps or image replacements.
- The latest feature request added detailed exploded assembly chapters, including the crown, ceramic balls, detents, springs, antenna and manufacturing/fitting explanations. That implementation is complete; no new feature request is pending in this handoff.
- Product language comes from [the brief](site/SITE_BRIEF.md). Physical details of the assembly use the September 19 engineering report when it conflicts with the older brief or CAD.

## Current site

Fifteen chapters: `hello`, `pet`, `boop`, `hold`, `creature`, `halo`, `object`, `quiet`, `size`, `details`, `inside`, `crown`, `detents`, `antenna`, `assembly`.

The five additions provide twenty selectable components with material, manufacturing and fitting notes; actual mesh selection; a ten-group crown explosion; a 24-groove race with exactly two opposed ceramic balls and deflecting BeCu leaves; an exposed antenna cap/web/tab/spring interface with an electrical trace; and a reversible six-stage assembly driven by scrolling, a range control, or play/pause/reset.

The built-in desktop/mobile UI, reduced-motion behavior, no-JavaScript stills and component notes, offline cache, and self-contained HTML are included. The final phone controller stays below the object. Instant reduced-motion navigation also clears and restores the paired-device labels correctly.

Useful implementation entry points:

| File | Responsibility |
| --- | --- |
| `site/src/timeline.js` | All fifteen poses and continuous scroll channels |
| `site/src/components/scene.js` | Renderer, orbit, picking, lazy assembly preparation, shader warmup and context recovery |
| `site/src/components/product-model.js` | Shared exterior geometry and original demonstrations |
| `site/src/components/assembly-model.js` | Internal rig, opacity/selection, detent geometry and fitting paths |
| `site/src/components/assembly-geometry.js` | Indexed rings, hollow parts, spring strip, leaves and optical web |
| `site/src/assembly-data.js` | Twenty manufacturing/fitting descriptions and six assembly stages |
| `site/src/assembly-interactions.js` | Selection, detent steps, contact trace and assembly controls |
| `site/src/sections/11-inside.js` through `15-assembly.js` | New chapter copy |
| `site/src/components/graphics-warmup.js` | Optional short-lived worker initializes graphics during page setup; unsupported/blocked workers fall back |
| `site/DESIGN_NOTES.md` | Design rationale, engineering qualifications, review corrections and measured evidence |

Keep the detail module lazy. The hero does not request the internal assembly. Preparation starts during the pet-to-boop interval, whose camera composition is unchanged, and compiles detail shaders offstage before installing them. Rendering starts without waiting for user engagement. Straight surfaces avoid redundant vertices; curves and actual opening datums remain sampled.

## Engineering authority and limits

Read [DESIGN_MANUFACTURING_REPORT_2026-09-19.md](DESIGN_MANUFACTURING_REPORT_2026-09-19.md), especially §§3–7, and [the component source register](site/qa/assembly/source-register.md) before changing geometry or claims.

The illustrated coaxial crown is a reference build. Coaxial versus transverse architecture, race material, optional rotary seal, sensor selection, contact supplier/stack, and measured RF performance remain open. The model is explanatory, not production CAD or a tolerance/clearance certification. Package artwork, flex/handling routes and exploded spacing are illustrative.

Relationships that were checked and should be preserved:

- Ø13 mm crown, 48 serrations, 24 internal grooves / 15° steps; two Ø0.800 mm Si₃N₄ balls and two 0.12 mm BeCu leaves.
- The sleeve stays fixed while the race turns; both balls seat together. The wave washer, C-ring, magnet, diaphragm/pip and satellite board are separate groups.
- The crown cartridge enters crown-first from inside the open rear tray.
- The board top is at z=1.8 mm and the plated contact face at z=3.2 mm, retaining the 1.4 mm working gap. The formed spring meets the underside without entering the tab and relaxes by 0.6 mm when loose.
- The cap's feed tab is integral, passing through the optical web to a plated underside land; its spring is a vertical SMT contact, not an axial pin.
- Final build order: prepared tray/cap/ring, crown cartridge, board/contact, display, cell, rear closure and testing after adhesive dwell.

The independent reviewer found and rechecked four corrected issues: hidden mobile controls, feed-spring interference, cap clipping and a tablet caption overlap. [The review](site/qa/assembly/blind-review.md) retains both findings and their resolved status.

## Setup and checks on another laptop

The site is static and needs no secrets, backend or external account. Dependencies are pinned in `site/package-lock.json`. Use Node 24 LTS or 22.12+, then run from `site/`:

```sh
npm ci
npm run build
npm run artifact
npm run preview -- --strictPort
```

Keep that terminal running on port 4173. In another terminal, also from `site/`:

```sh
npm run qa
node scripts/live-check.mjs
node scripts/assembly-check.mjs
node scripts/scroll-check.mjs
node scripts/delivery-check.mjs
node scripts/lighthouse.mjs
```

These scripts launch installed Google Chrome through Playwright (`channel: 'chrome'`). Install Chrome first if missing; `npx playwright install chrome` is also available. The fixed port 4173 must serve this checkout for the full suite. The Lighthouse script additionally uses port 9224. Some scripts accept `QA_URL`, but the complete suite assumes 4173.

The September 22 handoff was verified in an isolated checkout with `npm ci`, `npm run build`, `npm run artifact`, and 17 passing smoke checks at desktop/mobile sizes and from a standalone file URL. Run `node scripts/handoff-check.mjs` for that shorter check; it accepts `QA_URL` and leaves the saved full QA reports intact.

The clean install's npm audit reports one existing high-severity affected development dependency: `sharp` 0.34.5, used by asset/screenshot generation. The audit identifies libvips/libheif advisories and offers 0.35.4 as the fix. The tested lockfile was preserved for this snapshot; dependency upgrading and rechecking image generation remain follow-up work. The static browser app does not import Sharp. Details are saved in `site/qa/handoff-npm-audit.json`.

To regenerate lighting and stills, run `npm run dev` on port 5173, then `node scripts/bake-lighting.mjs` and `npm run assets` in a second terminal. `node scripts/record-motion.mjs` needs FFmpeg on PATH and the production preview on 4173. Font subsetting is optional and needs Python with `fonttools` and `brotli`; the ready-to-use fonts and licences are already included. `scripts/export.ps1` needs PowerShell 7 for ZIP delivery; ordinary development/build/testing does not need PowerShell.

The saved full verification was completed September 20: 180 automated checks (53 main, 22 live, 20 delivery, 53 assembly, 32 scroll), 240 layout captures, no browser exceptions, and Lighthouse mobile 90 performance / 100 accessibility / 100 best practices. The live heavy-section samples were about 60 fps. The recordings report their actual capture rates separately from their 60 fps encoding. These are measurements of the original machine, not promises for another laptop.

Physical-phone checks, a 2020-class laptop, a human screen-reader pass, first-time visitor comprehension and physical prototype validation remain external checks. See saved JSON/HTML reports and [the screenshot gallery](site/qa/gallery.html); the September 22 clean-install handoff smoke check is in `site/qa/handoff-check.json`.

## Hardware files

`firmware/main/CMakeLists.txt` currently selects `bg95_bringup_main.c`. The existing firmware is ESP32-S2/BG95 bring-up code, not the completed nRF9151-based product proposed in the September report. The local build metadata identifies ESP-IDF 5.4.1 and a 2 MB flash configuration. A copy of the local effective configuration is provided as `firmware/sdkconfig.defaults`, without local build outputs or generated absolute paths.

For analysis/building, activate ESP-IDF 5.4.1 and run `idf.py build` from `firmware/`. The old VS Code configuration contains the previous machine's ESP-IDF path and serial port; configure those for the new laptop. Do not assume the old CAD/PCB/BOM or fabrication exports implement every current engineering decision. Firmware, RF and fabrication have not been newly validated as part of the website handoff, and no hardware flashing is needed to run the site.

## Included and regenerated files

Source, lockfile, all runtime assets, standalone HTML, reports, CAD/PCB inputs, engineering references, review screenshots/videos and earlier small source/static archives are included. Dependencies, build directories, raw screencast JPEG frames, machine-local caches and duplicate top-level delivery ZIPs are omitted. `npm ci`, `npm run build`, `npm run artifact`, the capture scripts and `scripts/export.ps1` regenerate those outputs. The large review ZIP's contents are available unpacked under `site/qa/`.

The source snapshot manifest in `handoff/source-snapshot.json` records original byte hashes and Git blob IDs for copied inputs; the latter account for Git's text newline normalization. Setup/documentation additions and the clean-install smoke report are separate handoff files. Future edits should be made normally on this Git branch; there is no dependency on the original workstation or a running session.

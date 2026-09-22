# Independent assembly-chapter review

Reviewed 2026-09-20 against the live development build at http://127.0.0.1:5173. Scope: `inside`, `crown`, `detents`, `antenna`, and `assembly` only. `DESIGN_NOTES.md` and implementation notes were not read. No application files were changed.

Authority: `../DESIGN_MANUFACTURING_REPORT_2026-09-19.md`, particularly sections 4, 5, and 7. Its engineering baseline takes precedence over older brief inconsistencies. The current aesthetic direction is accepted.

## Findings requiring correction

### R1 — P2: Mobile build controls become concealed and untappable during the build

- Reproduction: fresh browser at 390 × 844; navigate to `#assembly`, then scroll 500 px into that section. Continue to 900 px.
- `#build-progress` remains at viewport y=294–310. Play/Pause and Reset occupy the same reserved product area. The sticky copy has reached y=0 while the scene remains fixed above it. These controls are visually hidden and the canvas receives input at the range's center. Keyboard focus can still reach the hidden range, so the problem also affects visible focus.
- At both sampled scroll positions the step text and part selection remain visible, but the build controls do not. The control remains concealed throughout the sticky portion unless the user scrolls back toward the section's beginning.
- Implementation: `src/assembly.css:4`, mobile `#assembly .section-inner { position:sticky; top:-48svh; ... }`, together with the reserved fixed product area.
- Recommendation: keep a compact controller visible below the product area while the heading scrolls away, or reposition the controller independently of the sticky title. Verify pointer hit testing and keyboard focus after the layout change.
- Evidence: `qa/assembly/reviewer-390-assembly-scroll500.png`, `reviewer-390-assembly-scroll900.png`. Browser `elementFromPoint` at the range center returned the Three.js canvas; `document.activeElement.id` was still `build-progress` after focus.

### R2 — P2: The assembled feed spring penetrates the aluminium tab

- The depicted spring is described as compressing against the underside of the integral tab, but its fitted geometry rises through that tab.
- Implementation: `src/components/assembly-model.js:117`–`120`. Local physical coordinates, before exploded offsets: tab z=2.4–3.9; plated land z≈2.35–2.4; contact tube extends up to z≈3.167. Its arch overlaps the tab rather than remaining below the contact plane. This is not caused by exploded spacing.
- The board top is z=1.8 (`assembly-model.js:55`), making the illustrated land gap approximately 0.55 mm. The source baseline is 1.4 mm above the PCB top.
- Source: engineering report §5, Design step 6, lines 899–904; §7, final assembly station 20, line 1842. The chosen geometry is vertical compression against an underside land, with the finger compressed as the PCB seats.
- Recommendation: adjust the tab/land height and compressed spring profile together so the spring meets the underside without entering the tab. A dimensional simplification caption can explain a schematic view, but the contact relationship itself should remain physically possible.
- Evidence: runtime geometry bounding boxes confirmed the coordinates above; the ordinary exploded view separates the parts and conceals this interference.

### R3 — P2: Opening assembly pose clips the antenna cap at the right edge

- Reproduction: navigate to the start of `#assembly` at 1920 × 1000 or 1440 × 1000, with the view reset and assembly progress at 0%.
- The far end of the antenna cap extends past the viewport edge. This affects the principal composition before any user orbit gesture.
- Implementation: `src/timeline.js:17`, assembly pose `scale:.74, cx:.70`, combined with the cap's exploded +29 mm offset in `src/components/assembly-model.js:147`.
- Recommendation: reduce the opening build scale or shift its center left enough to retain an edge margin across desktop sizes. Preserve clearance from the left copy column.
- Evidence: `qa/assembly/reviewer-1920-assembly.png`; `reviewer-1440-assembly.png`.

## Polish

### R4 — P3: Tablet antenna caption approaches/overlaps the bottom orbit toolbar

- At 820 × 1000, the long antenna heading increases the copy height. Its final validation caption extends into the toolbar's vertical band near y=930–953.
- Implementation: `src/assembly.css:2`–`3`; antenna copy/heading sizing and fixed orbit toolbar positioning.
- Recommendation: shorten the tablet line wrapping or reserve a little more bottom space for the caption.
- Evidence: `qa/assembly/reviewer-820-antenna.png`.

## Passing checks and evidence

- Fresh Chrome context with service workers blocked; WebGL and assembly module initialized successfully. No page errors during the targeted checks.
- All five new chapters inspected at 390, 820, 1440, and 1920 px widths. No document-level horizontal overflow. Original overview images and full 390/1440 screenshots also inspected.
- All 31 part-selector buttons changed the intended panel, pressed state, and scene selection.
- Detent forward/back controls produced +15°/−15° and restored the readout correctly. There are exactly two opposed balls, and both follow the same radial cycle. The animation is appropriately labeled as slowed and cut away.
- Keyboard End on the assembly range reached 100% and the final station; all fitted part offsets reached zero. Reset returned to 0%; Play advanced; Pause held its value.
- Trace the contact started the highlight sequence. No claim of measured antenna efficiency or validated radiated performance is made.
- The copy preserves the one-piece crown/hub, 24-groove race, static sleeve, two ceramic balls/leaves, washer and C-ring, late magnet bonding, diaphragm/pip, and separate angle/press sensing. Reference materials and open choices are identified.
- The displayed high-level assembly order matches the current report: prepared cap/ring/tray, cartridge from inside, board/finger seating, display connection and bonding, cell, door/collar and tests after adhesive dwell. The model routes the crown cartridge from the open rear toward the nose rather than inserting it from outside.
- No factual blocker found in the manufacturing copy. R2 is a displayed mechanical-relationship error, rather than a claim that an untested design is production-proven.

## Limits

This was a bounded review of the five additions, not a new audit of the first ten chapters. It used desktop Chrome and mobile viewport/touch emulation, not a physical phone. Full CAD interference, mechanical tolerances, antenna tuning, and actual production feasibility cannot be validated from this explanatory model. No-JavaScript/fallback assets were being updated concurrently and were not treated as finalized. Transitional poses were reviewed through ordinary navigation; this was not an exhaustive frame-by-frame animation or performance audit.

## Correction verification — 2026-09-20

**R1, R2, R3, and R4 are resolved in the rechecked development build. No remaining blocker was found in this targeted recheck.** The original findings above record the earlier build; this verification supersedes their open status.

- **R1 — passed:** Fresh Chrome mobile/touch context at 390 × 844, service workers blocked. At +500 px into `#assembly` (31%), the midpoint (50%), and the end (100%), the console remained at viewport y=405.125 (48% of the height). The range was at y=450–466 and Play/Pause/Reset at y=481–509. Hit testing returned the actual input/buttons at all three positions, rather than the canvas. At every position, touchscreen tap changed the range to 76%, a CDP touch drag changed it to 26% and retained that value, Play advanced or replayed, Pause held steady, and Reset returned to 0%. The compact console and station text are readable below the product. The redundant final part gallery is hidden only in the enhanced mobile assembly view.
- **R2 — passed:** Runtime geometry confirms the fitted finger's top at z≈3.2, plated underside at z≈3.2, PCB top at z≈1.8, and aluminium tab bottom at z=3.25. The contact therefore has the report's 1.4 mm working gap and does not penetrate the tab. Sampled progress at 35%, 45%, 46%, 47%, 80%, and 100% confirms the board approaches from behind; during the final compression, the tip remains at the underside plane as the board finishes seating. The loose strip has the additional 0.6 mm height. The adjusted web aperture clears the tab's y/z envelope. Sampled board/cell positions agree with the added lateral staging before rear insertion. These checks verify the depicted relationship, not a complete CAD interference analysis.
- **R3 — passed:** Opening assembly screenshots at 1440 × 1000 and 1920 × 1000 show the entire cap inside the viewport with the reduced 0.68 desktop scale. No new copy overlap appeared in those opening poses.
- **R4 — passed:** At 820 × 1000 the shortened caption layout clears the bottom orbit toolbar.
- The spring-leaf initialization now explicitly handles the initial non-finite sentinel; all sampled leaf vertex positions were finite. No page errors occurred in the recheck.

Evidence: `qa/assembly/reviewer-recheck-results.json`; `reviewer-recheck-390-500.png`, `reviewer-recheck-390-mid.png`, `reviewer-recheck-390-end.png`, `reviewer-recheck-1440-assembly.png`, `reviewer-recheck-1920-assembly.png`, and `reviewer-recheck-820-antenna.png`.

The recheck was limited to the reported corrections and their immediate interactions. Physical-phone/browser-chrome behavior and the broader limits above remain untested. No application files were edited.

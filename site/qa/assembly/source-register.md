# Assembly source register

Primary authority: `../DESIGN_MANUFACTURING_REPORT_2026-09-19.md`. The September 19 report supersedes conflicting older brief and CAD details. These are reference-build proposals, not measured production specifications.

The website displays a coaxial crown study. Crown architecture, race material, optional rotary seal, sensing IC, contact supplier/stack and radiated RF results remain open. PCB package artwork, spring curvature, exploded spacing and handling paths are illustrative.

| Component | Material / dimension shown | Manufacturing and fitting authority |
| --- | --- | --- |
| Front tray | PC/ABS · injection moulded | §7 steps 1–3; §7 phase 3C |
| Glass + AMOLED | 0.50 mm glass · laminated display | §7 step 4; stations 30–40 |
| Main circuit board | Six-layer FR4 · 23 × 52 × 0.8 mm | §6; §7 station 20 |
| Pouch cell | Connectorised · 6.0 mm baseline | §3 C-7; §7 steps 6–7; station 50 |
| Haptic actuator | 170 Hz LRA · metal bracket | §7 steps 5, 9 |
| Rear door | PC/ABS · silicone bead gasket | §7 steps 1, 8; stations 60–80 |
| Crown + integral hub | Ø13 mm · 48 cut serrations | §4 design steps 1–3; M1–M7 |
| 24-groove race | Hardened 17-4PH · reference build | §3 C-1; §4 step 4; M8–M11 |
| Two ceramic balls | Si₃N₄ · Ø0.800 mm | §4 step 5; M12, M17 |
| Detent leaf springs | C17200 BeCu · 0.12 mm strip | §4 step 5; M13, M17 |
| Static journal sleeve | POM-C · moulded, then sized | §4 steps 1, 8–9; M14, M18 |
| Wave washer | BeCu · three-wave return spring | §4 step 1; M13c, M18 |
| Captive C-ring | BeCu · Ø0.40 mm wire | §4 step 1; M13b, M18 |
| Sensing magnet | NdFeB · Ø6 × 2.5 mm | §4 steps 10–11; M16 |
| Sealed press diaphragm | LSR · 0.30 mm skin · PEEK pip | §4 step 12; M15, M20 |
| Crown satellite board | Angle sensor · Hall latches · tact | §3 C-24; §4 step 13; M20 |
| Antenna end cap | 6061-T6 aluminium · CNC machined | §5 steps 6–8; M1–M5, M9 |
| Optical isolation ring | Optical PC · 1.5 mm visible web | §3 C-5; §5 M6–M9 |
| Plated feed land | Nickel barrier · hard-gold contact | §3 C-6; §5 step 7, M4 |
| Spring feed contact | Plated BeCu · SMT spring finger | §5 step 6; §7 station 20 |

## Build stations

Reference: report §7, final assembly stations 10–90.
1. **Prepare the tray.** The cap and optical ring are joined to the moulded tray. The feed-tab aperture is sealed.
2. **Fit the crown cartridge.** The tested crown module enters crown-first from inside the tray. Its ears seat and its flex tail is routed.
3. **Seat the circuit board.** The board locates on its pins. Seating it compresses the spring finger beneath the cap’s plated land.
4. **Connect the display.** Mate the display tail, then press the laminated lens module onto the adhesive ledge.
5. **Connect the cell.** Place the insulating layer and stretch-release adhesive, locate the pouch cell and connect its tail.
6. **Close, then test.** Connect the dock flex, close the gasketed rear door, secure its screws and fit the collar. Leak and functional tests follow the adhesive dwell.

## Modeled relationships

- Crown Ø13 × 8 mm, 48 cut serrations; 24-groove race gives 15° increments (§4).
- Exactly two Ø0.800 mm silicon-nitride balls, 180° apart, seat together; each has a separate BeCu leaf (§4 step 5).
- The crown/race rotates; the POM sleeve remains fixed. The wave washer and C-ring serve different return/retention roles (§4).
- LSR diaphragm separates the mechanics from the sensing board; its off-axis PEEK pip operates a separate tact (§4 step 12–13).
- Optical PC web is 1.5 mm visible, with a sealed 5.6 × 2.1 mm feed aperture; the cap is 6061-T6 with an integral tab (§5).
- A gold land on the underside of that tab meets a vertical-deflection spring. Displayed PCB-top/land gap is 1.4 mm; the spring relaxes 0.6 mm in the loose state (§5 step 6).
- The reference contact is explanatory formed 0.09 mm strip, not a selected vendor part. The final supplier and stack remain unqualified (§5 step 6).
- Antenna performance and tuning await chamber work; the animated highlight represents electrical connectivity, not an RF simulation (§5).

Local reports were read only. The site does not alter the engineering report, CAD or firmware.

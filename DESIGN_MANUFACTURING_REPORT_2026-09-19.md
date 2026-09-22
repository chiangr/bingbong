# bingbong — Step-by-step Design & Manufacturing Report (2026-09-19)

**Role of this document:** the single integrated engineering programme for the bingbong 27 × 95 × 15 mm sealed polymer capsule keychain — design phases, EVM-0 (Mules A/B/C), EVM-1, DVT, PVT — synthesised from the 2026-09-12 architecture decision document and the revised (post-hostile-review) domain reports of 2026-09-19. It is engineering, not marketing. Nothing in it is frozen until the EVM-0 gate (§2) reports.

---

## 0. Provenance, evidence standard and binding decisions

### 0.1 Evidence tags (the decision document's standard, applied throughout)

| Tag | Meaning |
|---|---|
| `[V]` | A primary datasheet or standards document was opened and the number read; the source is named where the tag appears or in §10. |
| `[V?]` | Read by one pass but contradicted, unreproducible, or read only from a secondary/summary source (supplier sheet, lab summary, search extract). Must be re-confirmed before design-in. |
| `[U]` | Nobody has read the primary source: an estimate, an engineering calculation from tagged inputs, or a vendor-marketing / distributor-parametric claim. |

Rules applied in this synthesis: no `[U]` was upgraded to `[V]` without a domain report naming the primary source it opened; where two domains tagged the same number differently the more conservative tag is kept and the disagreement is stated; no part numbers were invented — where a class of part is proposed, the text says what must be confirmed. Costs and durations are `[U]` unless a domain tagged them otherwise.

### 0.2 What was synthesised, and the gap closed in the second pass

Inputs to this report:

1. `C:\Users\chian\Projects\bingbong\REDESIGN_DECISION_2026-09-12.md` (the primary source, read in full by the editor: §3 block diagram, §4 BOM incl. §4.3/§4.4, §5 power, §6 mechanical incl. §6.2/§6.3/§6.4, §7 interaction, §8, §9 risks, §10 prototypes, Appendix, Addendum A).
2. Domain report **Crown & crown-end assembly** (revised after hostile review) → §4.
3. Domain report **End-cap antenna & RF front end** (revised after hostile review) → §5.
4. Domain report **Mechanical system, sealing, cell, LRA, final assembly and build plan** (revision 2 after hostile review) → §7.
5. Domain report **Electronics** (revision 2 after hostile review; second pass, merged 2026-09-19) → §6.
6. The 2026-09-19 decisions listed in §0.3.

**Electronics domain report — delivered in a second pass:** the brief names four domain reports, but only three reached the synthesis editor in the first pass and §6 was assembled by the editor from the decision document, the electronics content of §4/§5/§7 and the local nRF9151 PS front-matter extract (`firmware\bingbong_pcb\_mech\nrf9151_ps.txt`, 116 lines — "Up to 4x SPI master/slave with EasyDMA", "32 general purpose I/O pins", "Single 50 Ω antenna interface", PC3 23 dBm / PC5 20 dBm, −108 dBm Cat-M1 low band, PSM floor 2.7 µA, eDRX @ 81.92 s 18 µA — and no SPIM clock limit). **The electronics domain report was then delivered in a second pass — analysed by a domain analyst, hostile-reviewed (14 findings, 10 missing steps, 7 mis-tags) and revised — and merged into this report on 2026-09-19 as §6 (revised after hostile review), with its cross-domain conflicts added to §3 (C-22…C-30), its open questions to §8, its risks to §9 and its sources to §10.6.** §6 now carries the same evidence standard and the same review maturity as §4, §5 and §7; the reviewer's dispositions are in §6.1.1.

### 0.3 Decisions since the decision document (2026-09-19), binding on this report

1. **Display: the Sharp/Winstar memory-in-pixel LCD is replaced by an on-demand colour AMOLED** — 1.1" 126 × 294, RM69310 driver, 3/4-wire SPI, outline 12.96 × 30.94 × 0.78 mm, active 10.96 × 25.58 mm, 400–450 nits, VCI 2.7–3.6 V, VDDIO 1.65–3.3 V, ELVDD +4.6 V / ELVSS −2.2 V from an external AMOLED PMIC (TI TPS65631-class, 3 × 3 mm WSON, single-wire CTRL/SWIRE from the panel) plus a load switch on VCI/VDDIO. All AMOLED mechanicals are `[V?]` (vendor product page, no drawing — §7 makes the panel drawing an EVM-1 entry criterion). The screen sleeps between glances; **the halo carries arrivals.** The 0.60 mm frontlight reservation and ~1.3 mm of panel thickness are returned to the cell; the EXTCOMIN/RTC machinery is gone. The nRF9151 SPIM is taken as 8 MHz maximum `[V?]` (not in the PS extract opened; confirm in the full PS) → ~13.5 fps full-frame at 16 bpp; partial-window updates for animation (§6).
   - Consequences the domains carry: the doc's "always-on 20 µA screen" thesis (§1, §7.2 "stays on the screen indefinitely") is **withdrawn**; the crown, the two Hall latches and the halo are now the only always-available channels; the doc's "ZERO boost converters" line (§3) is no longer true — the AMOLED PMIC is a boost + negative charge pump and is an RF-desense and power-budget item (§5 Step 14, §6).
   - **Cell thickness:** the decision text's "~6.5–7 mm, ~700 mAh" is **not** available in the Z-stack as built: with the LRA on the top side the governing column closes only with a 6.0 mm cell (§7 Step 6, margin 0.70 mm); 6.5 mm needs an RF-gated LRA cut-out. See §3 conflict C-7.
2. **Crown geometry (coaxial twist vs transverse stroke) is OPEN pending Mule C** (doc §9.4, §10). Coaxial is the baseline throughout; §4 Design step 20 and §7 Step 12 state what changes if transverse wins; §7 Step 12 lists the tray features frozen at the EVM-0 gate so the tray tool is unaffected either way.
3. **The product page exists; this report is engineering.** Where a domain found the product story physically wrong (e.g. §7.1 "coasts about a third of a turn" — the crown cannot coast, §4 Design step 7; "looks up within ~15 ms" — an on-demand AMOLED wakes in ~100–200 ms `[U]`, §6), the correction is recorded in §8 for the product owner.

### 0.4 Coordinate frames and terminology harmonised across domains

- **Body frame X (mm):** the decision document's frame — X = 0 at the crown's front face, +X toward the antenna cap; crown zone X = 0–16, main PCB zone 16–68/71, split ring 71–72.5, end cap 72.5–95. §5, §6, §7 use this frame.
- **Crown frame x (mm):** the crown domain's frame — x = 0 at the crown-end shoulder (the tray's crown-end wall face), +x into the body; the crown front face is at x = −6.00. **X = x + 6.0.** §4 uses this frame; where a §4 number is quoted elsewhere it is converted.
- **PCB z:** the RF domain's feed-stack datum (PCB top surface); §5 Step 6.
- "**Bezel**" (crown report) = "**crown-end bulkhead / collar**" (mechanical report) = the tray's crown-end wall that carries the reamed ø13.30 crown bore, the debris pockets and the buried grip electrode, plus the snap-on cosmetic collar that hides the two lid screws. See §3 conflict C-2 for the harmonised module-to-tray interface.
- "**Split ring / annulus**" (RF) = "**ring-disc**" (mechanical) = the 1.5 mm optical-PC part between tray and cap: full web (sealing and light guide) with a sealed aperture for the cap's feed tab (§3 C-5).
- "**Satellite PCB**" = the 22 × 10 × 0.6 mm 2-layer board in the crown zone carrying the angle sensor, two DRV5032DU latches and the tact; two variants (MT6701 / AS5600L) per doc §4.5.
- Step labels are kept from each domain so that cross-references remain traceable: §4 uses *Design step n*, *M-n*, *Verification item n*, *Risk n*; §5 uses *Step n*, *Mn*, *V-n*, *Rn*; §6 uses *E-n*, *EM-n*, *EV-n*, *ER-n*; §7 uses *Step n*, *Jn* (joints), *Phase n / station n*, *Risk n*.

---

## 1. Executive summary

### 1.1 What gets built

A 27.0 × 95.0 × 15.0 mm PC/ABS **front tray + full-width screwed-and-snapped rear door** (over-moulded LSR bead gasket, 12 snap hooks + 2 × M1.4 Torx T3, IP67, end-user battery door for EU 2023/1542 Art. 11) holding a 23 × 52 × 0.8 mm six-layer PCB with the Nordic **nRF9151** LTE-M SiP, a 1.1" **RM69310 AMOLED** behind a 0.50 mm chemically strengthened glass lens (vendor-laminated, tail on a 0.4 mm-pitch B2B), a **23 × 43 × 6.0 mm pouch cell** (560–620 mAh `[U]`, connectorised, stretch-release PSA), a **VG0840001D 170 Hz LRA** on a bracket reacting against the PCB only, one TPS62840 3.1 V rail plus the AMOLED PMIC, a BQ25180 charger with a 4-pad magnetic pogo dock (VBUS/GND/SWDIO/SWCLK) and an MFF2 eUICC.

At the crown end (X = 0–16): a **one-piece turned 316L crown + hub** (13.0 OD × 8.0, 48 cut serrations, PVD, 6.0 mm proud) rotating and translating 0.40 mm on a **one-piece POM-C sleeve** carrying two ø0.8 Si₃N₄ balls on BeCu leaves into a **24-groove race** (17-4PH H900 wrought + wire-EDM baseline; zirconia and BeCu rings built in parallel for Mule C), a ø6 × 2.5 diametric magnet in the hub's rear pocket, an **LSR diaphragm bulkhead** with a PEEK-cored pip onto one off-axis EVPBB tact, an on-axis MT6701 (or AS5600L) and two DRV5032DU latches on the satellite PCB, and an optional low-squeeze FKM rotary O-ring whose fate Mule C decides.

At the antenna end (X = 68–95): a **machined 6061-T6 end cap** that is a coupling element exciting the whole 95 mm capsule's dipole-like mode at 722 MHz, isolated by the **1.5 mm optical-PC ring-disc** that is also the RGB halo light guide, fed by a **vertical-deflection BeCu spring finger** onto a plated land on the underside of an **L-shaped cap tab** through a 5-element 0402 dual-resonant match (B12 + B2/B4) with a ≤ 0.3 pF antenna TVS, a DC-return inductor and a Murata MM8130-2600 RF switch connector for test.

### 1.2 In what order

1. **Weeks 0–2 — freeze requirements and start the clocks** (§2 Phase 0): nRF9151 2k-reel PO and prototype quantity secured; AT&T "wearable vs SFF" classification letter; cell RFQ at 6.0 and 6.5 mm with capacity in writing; AMOLED panel drawing and RM69310/PMIC datasheets; Art. 11 legal opinion; ID sign-off on the 0.40 mm press stroke and on "no coast".
2. **Weeks 0–8 — EVM-0, three mules in parallel** (§2 Phase 1): Mule A (network, DK + PPK2), Mule B (RF, chamber), Mule C (feel, crown-end blocks) — with the EM simulation, the FEMM magnetics, the press-stroke stack and the to-scale Z/x CAD running alongside. **Gate G0 at week 8.**
3. **Weeks 8–20 — EVM-1, 20 units** on quick-turn aluminium tools with the first custom PCBA, real crown cartridges, real cap/ring/feed, real cells and laminated display modules: active TRP/TIS, SAR and radiated-spurious pre-scans, drop with monitored connectors, insert pull-out, PPK2 golden current, 0 °C brownout. **Gate G1 at week 20.**
4. **Weeks 20–36 — DVT, 150 units** on soft tooling, RF BOM frozen, the full DVT matrix (drop, IP67, altitude, thermal, damp heat, ESC/UV, salt/sweat, detent and press life, charge cycling, leak correlation), certification pre-scans. **Gate G2 at week 36.**
5. **Weeks 36–52 — PVT, 500 units** on hard tooling; PTCRB/CTIA/AT&T/FCC (+ ISED/CE if in scope) from PVT samples; ORT; production RF box, tracer-gas leak station, EOL dock jig, serialisation live. **MP after week 52.**

### 1.3 The five numbers that decide the product

| # | Number | Value | Why it decides | Where |
|---|---|---|---|---|
| 1 | **B12 total antenna efficiency, bare, 699–746 MHz** | binding **≥ 12.3 %** (doc); design target 15 %; Mule B stop-line **< 15 % → Plan B**; honest estimate 8–18 % `[U]` | The gate and the estimate are the same number; there is no catalogue fallback; B2/B4 need **≥ 17.8 %** as well | §5 rows 7–9, Step 2, V-5 |
| 2 | **Governing Z-stack margin** | **C′ = 0.70 mm with a 6.0 mm cell** (LRA top-side column); 6.5 mm cell → 0.20 mm (fails the 0.3 mm floor) unless the LRA drops into an RF-gated PCB cut-out | Sets the cell (560–620 mAh `[U]`), hence the runtime; the AMOLED decision's "~700 mAh" is not available without the cut-out | §7 Step 6; §3 C-7 |
| 3 | **Weekly energy vs usable capacity** | doc 127.84 mAh/wk vs 454 mAh usable (560 mAh × 0.81) → 3.5 wk; **with the AMOLED, editor estimate 132–153 mAh/wk (mid 139) `[U]`** → 3.0–3.4 wk on 560 mAh, 3.2–3.7 wk on 600 mAh; compound no-eDRX + deep coverage still fails 1 week | The one unbounded failure mode (coverage search) and the biggest line (eDRX paging) both rest on measurements Mule A must make | §6 E-9; doc §5 |
| 4 | **Crown press stroke and click window** | **S = 0.40 ± 0.03 mm** hard stop; click at 0.27 mm nominal, RSS 0.18–0.36; arithmetic worst-case does **not** close — design relies on 3-bin selective pip assembly + 100 % EOL force-stroke test; the doc's 0.25 mm cannot be built with an H ± 0.1 tact | The boop is the product's second input; if ID rejects 0.40 the tact class changes | §4 Design step 12, Risk 1 |
| 5 | **Detent contact stress vs race shakedown** | land contact **p₀ ≈ 2.1 GPa** at 0.49 N vs shakedown ≈ 1.9 GPa (wrought 17-4PH H900) / 1.75 GPa (MIM) / 0.4 GPa (303) → wrought marginal-OK, MIM ratchets, 303 brinells; **1,000,000 indexes, torque decay ≤ 15 %** | The dial is "one texture forever"; a race that brinells kills the gift inside its life | §4 Design step 6, Risk 2 |

Two more numbers sit just behind these: **first-motion detection ≤ 77° worst-case** (both DRV5032DU outputs on two devices at 90°; OUT1-only gives 121° and fails the doc's "within 90°") — now a hard requirement because the screen sleeps (§4 Design step 11); and the **crown-end zone closure at 11.6 of 16.0 mm** (4.4 mm spare; 2.9 mm with an FH12 connector) which the draft had broken and the revision restored (§4 Design step 15).

### 1.4 The three experiments that come first (EVM-0, doc §10 — revised build lists)

| Mule | Answers | Cost / time (doc) | Revised scope carried by this report |
|---|---|---|---|
| **A — network** (nRF9151-DK + PPK2 + 3 SIMs) | Is eDRX granted and at what cycle; PSM; AS-RAI; **does an MT UDP packet reach a device in RRC Idle at eDRX 163.84 s, and after how long**; measured paging energy (92.6 µA field `[V?]` vs 18 µA PS `[V]`); UICC supply shutdown; the +600 µA debug-UART regression baseline | < $2k, 2 wk — **start day one** | Adds: `%XCOEX0` and `%XRFTEST` syntax/semantics on nRF91x1 firmware (§5 Step 13, M14); band-mask and power-class switchability (§5 Step 1); SPIM maximum clock on the DK (§6 EV-1 a); AMOLED + PMIC current on a DK-driven panel (§6 E-5.7, EV-1 b) |
| **B — RF** (non-functional mechanical mock in a CTIA chamber) | B12 and B2/B4 total efficiency bare / body phantom / hand / keys ± interposer; cap length, ring gap, tab position, crown grounded/floating, **cell at X = 19–62 vs 24–67**, **PCB with vs without the LRA slot**, harmonic-band efficiency; feed-land route A vs C; cable-free cross-check | ~$20k incl. chamber, 5 wk | Gate **≥ 15 % bare at 699–746 MHz** (binding) plus B2/B4 ≥ 17.8 % floor; full build list §5 Week 0; RF-gated decisions for §7 (cell x, LRA cut-out) and §4 (crown material/floating) |
| **C — feel** (two printed crown-end blocks, coaxial + transverse, with real parts) | Coaxial vs transverse on 10 hands blind; detent torque and 100k decay; seal drag with/without the O-ring; press stack closure on ≥ 10 units; magnetics with three race materials; click separation to ≥ 12/s on a ~48 g mass; acoustics; nickel release, yank, permeability controls | ~$4k, 3 wk (+ $4k life rig) | Full list §4 Verification items 1–16; tray interface freeze for §7 Step 12 at the gate |

**Gate to EVM-1 (doc §10, extended):** Mule A — eDRX granted **and** MT paging delivers on ≥ 2 of 3 carriers, or a documented polling fallback with measured energy; Mule B — ≥ 15 % bare B12 on the metal cap **or** a Plan B that achieves it, plus a cell x and LRA-slot decision; Mule C — a chosen geometry, measured torque, click separation ≥ 12/s, press-stack closure, seal-drag decision, latch edge map, and the collar/bore/lug interface frozen. Paper items: AMOLED panel drawing, cell quotes at both thicknesses, Art. 11 legal opinion, AT&T classification answer, LSR grade with a self-bonding datasheet, ID sign-off on stroke 0.40 and "no coast".

---

## 2. Master sequence — the integrated programme

All durations and costs `[U]` unless a domain tagged them; costs are rolled up from the domain tables (§4 Sourcing, §5 Sourcing, §7 Sourcing, §6.5) and **overlap where domains costed the same item** (noted). Week 0 = programme start. Critical path items are in bold.

### 2.1 Phase 0 — Requirements freeze and long-lead starts (weeks 0–2)

**Entry:** this report accepted; owners named per domain.

| # | Action | Owner | Output / exit criterion | Feeds |
|---|---|---|---|---|
| P0-1 | **Place the nRF9151-LACA-R 2k-reel PO and secure ≥ 40 prototype SiPs** (16–19 wk factory lead `[V?]` doc §9.10; distributor stock was 283 at Mouser `[V?]`) | Electronics | PO acknowledged with a date ≤ week 19; ≥ 40 pcs for EVM-1 in hand by week 10 | EVM-1 PCBA |
| P0-2 | Written question to AT&T's Partner Coordinator: keychain = "wearable" (body phantom, v2.1 Note 6) or free-space SFF? | RF | Letter; Mule B pass/fail configuration fixed | §5 Step 1, V-5 |
| P0-3 | SKU decision: AT&T-only B2/B4/B12 first; B13/B5 disabled in the band mask; EU/Verizon as separate tunes | RF + product | Signed band plan | §5 Step 1, Step 16 |
| P0-4 | Cell RFQ to ≥ 3 pouch vendors per §7 Step 7, **at T 6.0 max and 6.5 max**, capacity and local face-pressure in writing; 50 samples each thickness ≤ 6 wk; 20 cells to ADI for the MAX17048 INI | Mechanical + electronics | Quotes; sample PO | §7 Step 6/7, §6 E-1 |
| P0-5 | AMOLED module: panel drawing (outline tolerance, COG ledge, tail pitch/length/bend zone, polarizer/back film, Tstg), RM69310 datasheet (SPI timing, sleep-in/out delays, partial-window commands), TPS65631-class PMIC datasheet, load-switch selection; 10 modules + 3 evaluation boards | Electronics + mechanical | Drawing in hand = EVM-1 entry criterion (§7); SPIM clock confirmed in the full nRF9151 PS | §6 E-5/E-6, §7 Step 4 |
| P0-6 | Art. 11 legal opinion ($3–5k, doc §9.9) — keychain classification, boxed T3 driver as the "free tool", 18 Feb 2027 date | Mechanical + product | Opinion before the lid tool is cut | §7 Step 14 |
| P0-7 | ID sign-offs: press stroke 0.40 mm (doc 0.25 cannot be built with an H ± 0.1 tact); "no coast" (threshold 9.7 rev/s); detent acoustic target; crown zone as drawn (one-piece crown+hub, 6.9 mm two-land journal, 0.8° tilt) | Crown + ID | Signed | §4 Design steps 7, 9, 12 |
| P0-8 | Antenna consultancy SOW: EM model contents (§5 Step 4, all 11 conductors), sweeps incl. harmonic bands, dual-resonant match, chamber support, cert configuration | RF | SOW signed; model started week 1 | §5 Phase 1 |
| P0-9 | Requirements document lines with numbers: coverage-search governor (backoff schedule, "stationary and untouched N min → stop", max search duty), eDRX/PSM-refused fallback, first-motion ≤ 90° as a hard spec, screen-wake latency budget | Firmware + product | Release-gate tests defined | §6 E-14, doc §5.4/§9.6 |
| P0-10 | MFF2 eUICC supplier: written confirmation of UICC supply-shutdown support and minimum shutdown interval | Electronics | Letter (free) | §6 E-3, doc §9.5 |
| P0-11 | LSR-capable moulder and watch-component crown maker short-listed; wire-EDM shop and 17-4PH heat-treater identified | Mechanical + crown | Quotes for §4 M-14/M-15 and §7 tooling | DVT tooling |

**Exit:** P0-1, P0-4, P0-5, P0-8 started; P0-7 signed. (P0-2/P0-6/P0-10 may land during Phase 1 but must land before Gate G0.)

### 2.2 Phase 1 — EVM-0: the three mules and the design analyses (weeks 0–8)

**Entry:** Phase 0 exit. **Quantities:** Mule A = 3 DKs + PPK2 + 3 SIMs; Mule B = 7–9 caps, 6 annuli, 5 boards, 1–2 shells, dummies; Mule C = 2 crown-end blocks (coaxial, transverse) with 3 groove/preload variants and 3 race materials, ~10 crown cartridges. **Cost:** Mule A < $2k; Mule B $6–11k hardware + $8–15k chamber (+ consultancy $20–40k running through EVM-1); Mule C ~$4k + $4k life rig + Ti control crown; mechanical mock-ups ~$12k (§7) → **≈ $35–50k hardware + labs, plus the consultancy retainer** (the doc's "~$30k" excluded the consultancy).

Run in parallel:

| Track | Weeks | Content (cross-reference) |
|---|---|---|
| **Mule A — network** | 0–2 (+ continuous PPK2 baseline) | doc §10; §6 EV-1: eDRX/PSM/AS-RAI grants, MT paging latency at eDRX 163.84 s, per-paging energy, UICC shutdown, UART regression baseline; `%XCOEX0`/`%XRFTEST` on nRF91x1 firmware; SPIM clock; DK-driven AMOLED current |
| **Mule B — RF** | 0–5 | §5 Verification Week 0–4: build list, bench V-1…V-4, chamber V-5/V-5b/V-6/V-7, decide V-8; both cell positions and the LRA slot (§7); feed route A vs C; ring gap 1.0/1.5/2.0 |
| **Mule C — feel** | 0–3 (+ 100k decay to week 5) | §4 Verification items 1–16: geometry (10 hands), torque, decay, seal drag, coast/rattle, press stack, magnetics with three races, sealing, ESD, drop, yank, permeability, nickel release, debris, acoustics, click separation; §7 Gate items (cold torque at −20 °C, field map, acoustic with/without cell contact) |
| **EM simulation** | 1–4 | §5 Steps 4–5 (model, sweeps incl. harmonic bands) → design point + dB/mm sensitivity table signed by mechanical |
| **Crown analyses** | 1–4 | §4 Design step 16: FEMM (both sensor variants, both latches, race and tact dome, press-induced change, stray field at the labyrinth); Hertz/shakedown; LSR skin + pip stiffness and 300k fatigue; ring/groove bearing at 150 N; drop 120 N on the hard stop; seal drag |
| **Mechanical CAD to scale** | 1–6 | §7 Steps 1–6, 12: tray/lid architecture, Z-stack columns A1/A2/B/C′/C/D with the PCB floor plan (§5 Step 11b, §6 E-12), the crown-module-to-tray interface (§3 C-2), lid rib FEA (§7 J1), lens ledge stack |
| **Electronics schematic v0** | 2–8 | §6 E-1…E-17: power tree with the AMOLED PMIC, GPIO budget, SPI throughput, satellite 10-way interface, ESD, dock; PCB rev A layout starts at week 6 against the Mule B keepout and the §5 floor plan |
| **Paper items** | 0–8 | P0-2, P0-4, P0-5, P0-6, P0-10; LSR grade with self-bonding datasheet; Panasonic EVPBB allowable static load in writing; Materion C17200 datasheet; ASTM B733/B488 opened |

**Gate G0 — EVM-0 → EVM-1 (week 8), all mandatory:**

1. Mule A: eDRX granted **and** MT paging delivers on ≥ 2 of 3 carriers, or a documented polling fallback with measured mAh/wk; measured paging energy replaces the 92.6 µA `[V?]` line; UICC shutdown confirmed on the bench.
2. Mule B: **≥ 15 % total efficiency bare, 699–746 MHz** on the metal cap (or a Plan B configuration that achieves it); B2/B4 ≥ 17.8 %; cell x (19–62 vs 24–67) and LRA slot (≤ 1 dB cost or dead) decided; feed route chosen; harmonic-band efficiency table delivered to §5 Step 10b.
3. Mule C: geometry chosen; torque 2.5–4.0 mN·m with ripple uniformity ≤ 15 %; ≤ 15 % decay at 100k; press stack closes on ≥ 10 units with 3 bins; seal-drag decision (O-ring in/out); INL and latch edge map (≤ 80° gap) met on ≥ 3 units; race material chosen from the field map (≥ 2× B_OP margin); cold torque at −20 °C; **collar/bore/lug/boss interface frozen** (§7 Step 12).
4. Paper: AMOLED panel drawing; cell quotes at 6.0/6.5 with capacity in writing; Art. 11 opinion; AT&T classification; ID sign-offs (P0-7); nRF9151 prototype SiPs allocated.

**If a gate item fails:** Mule B < 15 % → Plan B (polymer cap, 32 mm clearance, NN03-310 lengthwise, ~105 mm body) is simulated during weeks 4–6 and a Plan B mule is built before any tooling (doc §10; §5 V-8 table — the 12–15 % "one structural iteration" branch is a proposed amendment needing sign-off). Mule C transverse → satellite PCB respin (L-flex MT6701 or MA782 side-shaft), crown zone −3 mm to the keepout buffer, crown-module tool changes, tray tool unaffected.

### 2.3 Phase 2 — EVM-1: first real hardware (weeks 8–20), 20 units

**Entry:** Gate G0. **Cost:** mechanical ~$50k (quick-turn Al tray/lid tools $8–15k, cells, lenses, CNC caps, machined sleeves, proto LSR discs) `[U]` §7; PCBA rev A (main + 2 satellite variants, ~30 sets) $15–25k `[U]` §6; crown proto parts (turned crowns, EDM'd races, etched leaves, Ti control) ~$10k `[U]` §4; chamber active TRP/TIS + SAR pre-scan + spurious pre-scan $13–25k `[U]` §5 → **≈ $90–110k**.

| Step | Weeks | Content |
|---|---|---|
| EVM1-1 | 8–11 | PCBA rev A: §6 EM-1…EM-7b (6-layer 0.8 mm, copper ends X = 63.0, ten 0402 match positions, TVS, MM8130-2600, finger pad, AMOLED B2B at X = 46–49, PMIC in the side strip, 10-way satellite connector at X = 16–19.5, bottom-side strip connectors); satellite PCB both variants (§4 Design step 13) |
| EVM1-2 | 8–12 | Quick-turn Al tools for tray and lid (§7 Phase 1); separately moulded/die-cut LSR gasket; CNC caps with L-tab and land (§5 M1–M5, Route A on some, Route C on others); CNC/SLA optical-PC ring-disc with the sealed tab aperture; 10 bosses for insert pull-out |
| EVM1-3 | 9–13 | Crown cartridges from real parts through §4 M-1…M-23 at proto level (machined POM-C sleeves, loose LSR disc + machined pip in 3 heights, Panasonic EVPBB, wire-EDM'd wrought race, chosen race material variants) |
| EVM1-4 | 10–14 | Cells: 50 vendor samples, both thicknesses; 50 laminated lens + AMOLED modules with B2B tails |
| EVM1-5 | 12–16 | Bring-up: §6 EV-2 (rails, PMIC, SPI throughput and fps, NOR, eSIM, gauge, charger JEITA readback, DRV2625 waveforms, satellite both variants, IQS211B); PPK2 golden sleep current (< 200 µA at 60 s, target per §6 E-9/EV-3; §3 C-23); 0 °C brownout with a real 395 mA burst; COEX0 timing (§5 V-15) |
| EVM1-6 | 14–18 | RF: §5 V-9 conducted (MPR/A-MPR/ΔTC applied, H2/H3 at ANT, switch-connector IL), V-9b radiated-spurious pre-scan, V-10 active TRP/TIS (AMOLED on/off ≤ 1 dB), V-10b SAR pre-scan (PC3 vs PC5 decision), V-11 ESD, V-12 unit spread (σ ≤ 0.6 dB), V-13 temperature/humidity/swell, V-14 field (3 units, 2 wk), V-15 COEX0 |
| EVM1-7 | 14–18 | Mechanical: §7 Gate EVM-1→DVT items — all six Z columns ≥ 0.3 mm by shim; lid closes ≤ 150 N; 3 units fine-leak + immersion; 3 units 26-orientation drop with **continuous B2B monitoring**; insert pull-out ≥ 180 N / torque-out ≥ 0.08 N·m on 10 bosses; dock pull ≥ 200 g through the wall; ESC screen (Bergen jig) on tray/lid/ring; gasket reseal × 10 |
| EVM1-8 | 16–20 | Crown: §4 Gate to EVM-1 items re-run on production-intent parts; §9.11 1M-index rig started on the chosen variant (≈ 5.8 h at 2 rev/s per million, then talc/filings) |

**Gate G1 — EVM-1 → DVT (week 20):** RF: TRP ≥ gate + 2 dB and TIS ≤ gate − 2 dB on 3 channels/band in the certification configuration; spurious pre-scan passed or trap fitted with ≤ 0.3 dB in-band cost; SAR pre-scan decided PC3/PC5; unit σ ≤ 0.6 dB. Electronics: golden sleep current within budget; brownout margin at 0 °C ≥ 100 mV; fps and wake latency meet the P0-9 numbers; JEITA/gauge validated. Mechanical: all §7 Gate items; 6.0 vs 6.5 mm cell decided (with the Mule B slot result); panel B2B or hot-bar decided. Crown: press-stack closure on ≥ 10 production-intent cartridges; latch edge map at −10…+50 °C; nickel-release and yank in hand. Paper: cell CB/UN 38.3 test plan booked; PTCRB/GCF module status (§5 Step 15.2) confirmed; hard-tool decision (1+1 P20 + LSR 2-shot, $35–60k) taken.

### 2.4 Phase 3 — DVT (weeks 20–36), 150 units (~65 consumed by test)

**Entry:** Gate G1. **Cost:** mechanical tooling + build $60–90k `[U]` §7; PCBA rev B ~$20k `[U]`; crown tooling (POM sleeve tool $6–10k, LSR 3-cavity tool $12–20k, race EDM program/fixtures $3k, PVD fixtures, spring dies) $30–45k `[U]` §4; test labs (drop/IP/thermal/salt/altitude/ESC/UV/IEC 62133-2) $25–40k `[U]` §7; nickel-release + ESD + salt fog on crowns $3–5k `[U]` §4; cell CB + UN 38.3 $3–6k `[U]` → **≈ $145–210k**.

| Step | Weeks | Content |
|---|---|---|
| DVT-1 | 20–27 | Soft tooling: 7075 Al single-cavity tray (may be the EVM-1 tool re-cut) and ring-disc; lid as Al tool + small LSR gasket tool; POM-C sleeve tool + one-chucking secondary (§4 M-14); LSR diaphragm tool with 3 pip-height cavities (§4 M-15); production-intent crown module from the watch-component house; CNC caps by two shops (cap-to-cap RF spread ≤ 0.3 dB) |
| DVT-2 | 20–24 | **RF BOM lock** (§5 Step 16): cap alloy/finish, ring resin, cell vendor/thickness, LRA position, AMOLED module, PMIC, shell mould — any later change is an ECO with re-measurement |
| DVT-3 | 22–26 | PCBA rev B (layout fixes from EVM-1; SPI terminations; PMIC placement verified for TIS); satellite variant chosen or both kept |
| DVT-4 | 26–36 | The §7 DVT matrix: drop (26 orientations), tumble, lens impact, IP67 after drop/lid cycles/1M indexes/thermal/altitude/cold soak, altitude, thermal cycling + 72 °C × 3 + 80 °C stretch, damp heat (coupons 85/85; real module 60/90), ESC/chemical, UV, salt/sweat/EN 1811/dock-pad creep, detent life at three temperatures, press life 300k, charge/discharge 300 cycles with real bursts, cell safety certs, swell, acoustics, lug, lid service × 10 by naive users, dock 30k, **leak-test correlation (30 units, fine-leak vs IPX7/IP6X)**, RF pre-scans on RF-frozen units |
| DVT-5 | 28–34 | §5 V-16 golden units (5) and production box limits (−1.0/+2.0 dB, ≤ 0.3 dB repeatability); V-17 drop → S11 finger check; V-18 long-term (60 °C/90 % RH on real units within the cell vendor's limit; 85/85 + thermal cycling on dummy-cell RF units) |
| DVT-6 | 28–36 | Firmware release-gate tests: eDRX/PSM-refused fallback in a shielded box against a base-station simulator; coverage-search governor duty cycle; PPK2 on every release; FOTA delta (app + modem delta) end to end |
| DVT-7 | 30–36 | Production test development: §5 M12/M13/M14 (bed-of-nails DC checks, S11 finger signature, `%XRFTEST` shield box); §7 Phase 4 leak station commissioning; §7 Phase 5 EOL dock jig; §4 M-19/M-21/M-23 crown stations and the tact-height gauge; MES serialisation schema |

**Gate G2 — DVT → PVT (week 36):** all DVT failures closed with re-test; leak threshold frozen from the correlation set; RF pre-scans within 2 dB of the gates on RF-frozen units; golden units locked; firmware release gates passed; work instructions with photos; hard-tool release approved; certification lab slots booked.

### 2.5 Phase 4 — PVT (weeks 36–52), 500 units, then MP

**Entry:** Gate G2. **Cost:** hard tooling + build $75–120k `[U]` §7 (1+1 P20 tray + 2-shot LSR lid $35–60k; 2-cavity ring); fixtures (pre-line + 7 stations + crown cell + dock jig) $30–45k; **tracer-gas leak station $40–80k** (forming-gas variant $25–40k); production RF box/fixture/power meter $6–15k; crown assembly fixtures + life rig $20–30k `[U]` §4; **certification $50–150k** (doc; §5: PTCRB + CTIA OTA $15–35k, FCC Parts 24/27/15B + SAR $25–50k, ISED +$5–10k, CE RED + second tune + OTA +$30–60k) → **≈ $220–440k**.

| Step | Weeks | Content |
|---|---|---|
| PVT-1 | 36–46 | Hard tooling (8–10 wk); textured; first-off CMM (ledge 0.05 sort, rim 0.10, hook shoulder ± 0.05, crown bore); cap on a 5-axis cell; crowns on Swiss-type lathes with the M-4 permeability gate live |
| PVT-2 | 40–48 | Certification samples from PVT: PTCRB integration + CTIA OTA (per the classification answer), AT&T Table 4 report, FCC (custom chassis antenna → transmitter certified in our name; SAR), ISED/CE if in scope; cell IEC 62133-2 CB and UN 38.3 summary with the pack |
| PVT-3 | 44–52 | ORT: 20 units/week through drop/IP/thermal mini-loops for 4 weeks; yield targets: lamination ≥ 95 %, fine-leak ≥ 98 % first pass, EOL ≥ 97 %; Cpk ≥ 1.33 on lens sub-flush, lid step, gasket squeeze (lid height), crown torque, click travel |
| PVT-4 | 44–52 | Production readiness: golden RF units re-verified weekly; leak station correlated; tact-height gauge R&R; grease-mass audit (§4 M-22); EOL calibration capture (§4 M-23) writing the 24-point detent table to NVM; pair provisioning and eSIM profiles; split-shipping DG paperwork (UN3481 PI 967 Section II `[V?]`) |

**Release gate to MP:** certifications granted (or conditional with a dated plan); ORT four weeks clean; traceability live (serial ↔ pair ↔ cell ↔ module ↔ crown module ↔ leak value ↔ EOL ↔ firmware); spares path (cell + 2 screws + gasket) stocked for the Art. 11 five-year obligation.

### 2.6 Programme roll-up (all `[U]`, overlaps noted)

| Phase | Weeks | Units | Cost range |
|---|---|---|---|
| Phase 0 | 0–2 | — | legal $3–5k; silicon reels (nRF9151 2k × $16.08 = $32k, doc `[V]` price) |
| EVM-0 | 0–8 | 3 mules | $35–50k + consultancy $20–40k (runs to EVM-1) |
| EVM-1 | 8–20 | 20 | $90–110k |
| DVT | 20–36 | 150 | $145–210k |
| PVT | 36–52 | 500 | $220–440k |
| **Total to MP** | 52 | | **≈ $550–890k** excluding silicon reels and the optional in-line lamination cell (+$30–60k) — the domains' own subtotals (antenna $39–76k, certification $50–150k, mechanical/build $355–420k, crown-end $60–85k) overlap in the EVM-1/DVT builds and are not simply additive |

**Schedule risks that move the whole sequence:** nRF9151 lead time vs EVM-1 (P0-1); custom cell 12 wk from the EVM-1 gate (§7); LSR 2-shot moulder selection at G0; wire-EDM race capacity (bridge: broach-then-age); AT&T classification answer (changes the Mule B pass/fail configuration); Mule B < 15 % (adds a Plan B mule cycle of ~6 weeks and changes the shell).

---

## 3. Cross-domain conflicts and interfaces

Each conflict states the positions, which one is adopted and why, the owner, and the test or gate that closes it. "Adopted" means the domain sections in §4–§7 are read with this resolution; where a domain's text still carries the superseded position it is marked *[Editor: superseded by §3 C-n]* in place.

### C-1. Detent race material: 17-4PH H900 (crown) vs "replace with BeCu/zirconia" (mechanical)

- **Crown (§4):** wrought 17-4PH H900 (YS ≥ 1170 MPa, 40–48 HRC `[V?]`) with wire-EDM grooves after ageing is the only ferromagnetic part; it is coaxial and co-rotates with the magnet so its distortion is a static reshaping of the 2-pole field (< 5 % shunting expected `[U]`), not INL; fallbacks Y-TZP zirconia (preferred if the O-ring is deleted) and C17200 BeCu HT (38–45 HRC `[V?]`).
- **Mechanical (§7):** 17-4PH is "strongly ferromagnetic in all conditions" `[V]` ATI TDS; a concentric ferromagnetic ring rotating with the magnet is a static shunt (field-amplitude loss at DRV5032 and MT6701) plus a once-per-rev harmonic if eccentric; use BeCu C17200 TH04 or Y-TZP.
- **Resolution:** the two domains agree on the physics (static shunt, not INL) and on the test. **Adopted: Mule C builds all three race rings as swap-in parts** (wrought 17-4PH H900 EDM'd; Y-TZP CIM/sintered; C17200 TH04 turned + grooved + aged) and decides on the gaussmeter map — race delta ≤ 10 % at the IC, **≥ 2× B_OP margin at the latches (Bpk ≥ 8 mT)** — and on the 100k decay (≤ 15 %). Hertz check: BeCu TH04 at YS 1130–1420 MPa `[V?]` has a shakedown line (≈ 1.8–2.3 GPa) at or above the wrought 17-4 figure, so it is not excluded on contact stress; zirconia (HV ~1200) is above all of them. The 17-4 ring stays the *cost* baseline only until the map is in hand. Mechanical's station C1 "press 200–400 N" is superseded by §4 M-7 (0–0.02 mm interference + retainer, 50–150 N — a 0.03 mm press puts ~470 MPa hoop in the 1.0 mm annealed 316L wall). **Owner:** crown. **Closes:** Mule C item 7; §4 M-11 residual-magnetisation check applies to the 17-4 variant only.

### C-2. Crown-end architecture: one-piece crown+hub on a POM sleeve (crown) vs "crown bore on a fixed hollow sleeve, magnet in the end wall, 2.8 mm to the sensor, 0.25 stroke" (mechanical Step 12)

- **Crown (§4):** body-by-body dimensioned stack that closes at 11.6 of 16.0 mm; magnet in the hub's rear pocket (AG 1.0 mm rest / 0.6 pressed for the MT6701 `[V]` window 0.5–2.0); stroke 0.40 with a toleranced press stack; LSR diaphragm bulkhead with a compliant pip; retention by a BeCu C-ring; 6.9 mm two-land journal → tilt ≈ 0.8°.
- **Mechanical (§7 Step 12):** a sketch resolving the doc's "12 mm journal" inconsistency with a ≥ 6 mm sleeve journal (also 0.8°), magnet in the crown end wall, sensor behind a 1.0 mm moulded bulkhead at ≈ 2.8 mm, stroke 0.25 with a tact of ≥ 0.25 travel.
- **Resolution:** **§4 is authoritative for everything inside the crown module** — it is toleranced, it keeps the magnet inside the crown's own length (the doc's zero-marginal-length topology), it puts the sensor at the datasheet's mid-window rather than 2.8 mm, and it faces the tact-travel fact (no 0.5 mm-tall tact travels > 0.11 mm `[V]` Panasonic) instead of specifying a tact that does not exist in that height. Mechanical Step 12 is superseded except for (a) the **dual-compatibility freeze list** (crown-end bore, O-ring/gasket land, orientation key, two screw bosses, collar snap, lug position) frozen at Gate G0, and (b) the "draw to scale before Mule C" requirement. Both domains' 0.8° tilt figures agree; the doc's "< 0.5° on a 12 mm journal" is corrected in §8.
- **Harmonised module-to-tray interface (editor, for sign-off by crown + mechanical):** the crown cartridge (crown + sleeve + diaphragm + satellite PCB + carrier ring) is inserted **crown-first from inside the tray, before the lid closes** (§4 M-21), through the tray bulkhead's reamed ø13.30 +0.05/−0 bore; the sleeve flange (ø13.20) passes the bore and the **two retention ears on the wide-face sides** seat in pockets on the bulkhead's inside face — the ears are the yank shoulder (crown → C-ring → sleeve groove → ears → bulkhead). Because the 27 mm direction has room, the ears are widened from 3.0 to **6.0 mm** each (shear capacity ≈ 2 × 300 N `[U]`, doubling §4 Design step 14's figure). **J5 (the static seal) is a face seal on the flange/ear front face against the bulkhead's inside face** (LSR ring or O-ring in a flange groove, 25–30 % squeeze), not a radial seal on a "collar OD"; mechanical station 10 ("insert from outside") is superseded. The cosmetic collar snaps on from outside and hides the two lid screws; it carries no load and no seal. Mechanical's "crown-module bore ø~10.5" is superseded by ø13.30 + the ear pockets; the opening in the bulkhead inside face is sized for the sleeve nose only, the satellite PCB (22 × 10) is fitted to the cartridge before insertion and lies inside the tray. **Owner:** mechanical (tray), crown (cartridge). **Closes:** to-scale CAD by week 6; Mule C item 11 (yank 150 N / lug 300 N).

### C-3. Crown seal: optional 3–6 % squeeze FKM rotary O-ring (crown) vs 10–15 % squeeze low-temperature FKM (mechanical J6)

- **Crown (§4 Design step 8):** Parker ORD 5700 §8.13 rotary rules `[V]`: ID 1–3 % larger than the shaft, compressed from the gland OD, 3–6 % squeeze; computed drag 0.15–0.35 mN·m running / 0.6–1.4 breakaway `[U]` → optional, Mule C measures with/without; deletion implies a zirconia race (wet-tolerant mechanism); the LSR diaphragm alone protects the electronics.
- **Mechanical (§7 J6):** 10–15 % squeeze, low-temperature FKM (GLT/GFLT class) or PTFE-filled silicone, cold torque at −20 °C.
- **Resolution:** **Crown wins on squeeze and gland geometry** (primary source opened; 10–15 % is reciprocating practice and the review had already rejected it). **Mechanical wins on compound temperature class:** if the O-ring is fitted it is a low-temperature FKM (GLT/GFLT class, TR10 `[U]` — Parker bulletins not opened) or PTFE-filled silicone, and Mule C item 4 gains a −20 °C cold-torque run. Acceptance unchanged: ≤ 0.5 mN·m running / ≤ 0.9 breakaway or delete. **Owner:** crown. **Closes:** Mule C item 4; DVT IPX7 after −20 °C soak.

### C-4. Grip electrode and the crown's ESD path: exposed shoulder ring (doc, crown) vs buried insert-moulded ring (mechanical J8)

- **Doc / crown (§4 Design steps 12, 18):** IQS211B annular electrode on the static shoulder face; the floating crown 0.15 mm away arcs an 8 kV contact discharge across the labyrinth into the electrode's 2k2 + TVS — the ESD acceptance rests on that route, not on the LSR/PEEK dielectric numbers.
- **Mechanical (§7 J8):** the electrode is insert-moulded (or LDS) **inside** the bulkhead wall, 0.8–1.0 mm behind the shoulder surface — no feedthrough, no sealing joint; capacitive sensing through 1 mm of PC/ABS is standard practice; Cx still ≈ 5–15 pF `[U]`.
- **Resolution:** **Adopted: the buried electrode (mechanical)** — it removes a sealing feedthrough and an exposed metal ring at the E-field maximum of the antenna. **Consequence, which the crown text does not yet reflect:** the crown's ESD discharge can no longer reach the electrode's TVS through air; with 1 mm of PC/ABS (~20 kV/mm `[U]`) in the way the next-weakest path is the 0.30 mm LSR skin + pip to the tact (~6 kV `[U]`) — unacceptable. **A deliberate bleed/discharge path must be added:** a BeCu grounding leaf moulded into the POM sleeve, riding on the hub's rear land, taken through the flange to the satellite PCB → 1 MΩ to GND (keeps the crown RF-floating for §5) in parallel with a low-capacitance TVS to GND. This is the RF domain's "1 MΩ bleed from the crown insert via the wave washer `[U]`" made concrete. Alternative if the leaf is refused: a small exposed spark-gap pad on the shoulder tied to the TVS — a feedthrough again. **Owners:** crown (leaf in the sleeve), electronics (1 MΩ + TVS on the satellite PCB), mechanical (electrode ring in the bulkhead). **Closes:** §4 Verification item 9 (8 kV contact / 15 kV air with a current probe on the bleed line); doc §9.8 coupon with a press (Cx step on the 0.40 mm stroke) and a TX burst.

### C-5. Feed geometry, ring web and PCB edge: L-tab + z-deflection finger, PCB to X = 71 (RF) vs full-web ring-disc, ø3 boss with an x-loaded finger, PCB ending at X = 68 (mechanical J4/J9)

- **RF (§5 Step 6, M1, M7):** after review, the finger is a standard vertical-deflection (z) SMT part bearing on a plated land on the underside of an L-shaped cap tab that passes through the annulus's open centre and overhangs the PCB edge (tab to X = 68.5, finger at 68.5–70.5, board edge 71); the ring is an annulus with an open centre.
- **Mechanical (§7 J4/J9):** the ring-disc is an H-section optical-PC part with a **full web** (it is the seal and the light guide), skirts inside the tray end (X = 68–71, hence the PCB shortened to 68) and inside the cap bore; the RF feed is a ø3 boss through a ø3.2 hole in the web, with the finger bearing on the boss end face (x-loaded).
- **Resolution:** **RF wins on the feed load direction** (the x-loaded finger is the blocking finding F1 the RF review already killed — the boss end-face contact re-creates it). **Mechanical wins on the full web and the skirt** (sealing and the light path need it; PCB substrate ends at **X = 68.0**). Harmonised: the cap's L-tab (5 wide × 1.5 thick) passes through a **sealed rectangular aperture in the ring web** (≈ 5.6 × 2.1 mm, epoxied in the same operation as J4b — this is the new J9), continues −X over the PCB edge to **X = 65.5**, and its underside land (3.0 × 4.0 mm) sits at z = +1.4 mm above the PCB top; the finger moves to **X = 65.5–67.5**; the feed trace shortens to X = 63–65.5; copper still ends at 63.0. The tab cantilever grows by 3 mm (still a 1.5 mm-thick aluminium beam — the drop load path is the cap lip on the shell, never the tab or finger). The RF model (§5 Step 4.2) must now include the web (εr ≈ 2.9, tan δ ≈ 0.006 `[U]`) and the longer tab; Mule B sweeps tab length 5–8 mm. **Owners:** RF (tab, land, finger, trace), mechanical (ring-disc, aperture seal, tray end). **Closes:** Mule B V-1/V-5 (tab length is a sweep variable); §5 V-3 stack on 10 units; §7 leak correlation includes J9.

### C-6. Feed-land plating spec: "EN 3–5 µm + Au 0.1–0.3 µm" (mechanical Phase 2 item 3) vs "ASTM B733 Type IV/V ≥ 5 µm SC1 + B488 hard Au 0.25–0.5 µm, or a plated insert (Route C)" (RF M4)

- **Resolution:** **RF wins** — the spec was rewritten after review against the standard's classes (`[V?]` until B733/B488 are opened); mechanical's process line is updated to §5 M4 (Route A masked immersion EN + Au; Route C plated pin as co-baseline; Route B recorded only). Acceptance: ≤ 5 mΩ land-to-cap, tape adhesion + thermal shock, XRF thickness 5/lot. **Owner:** RF; mechanical carries it in the cap drawing. **Closes:** Mule B V-3 / V-8.

### C-7. Cell thickness: "~6.5–7 mm, ~700 mAh" (AMOLED decision; RF model) vs "6.0 mm baseline, 6.5 only with the LRA cut-out" (mechanical Z-stack)

- **Resolution:** **Mechanical's arithmetic wins** (§7 Step 6): the governing column is the LRA on the top side (C′ = 0.70 mm at 6.0 mm; 0.20 at 6.5 mm; −0.30 at 7.0 mm). The 6.5 mm option exists only if the LRA sits in an 8.4 mm PCB cut-out at X = 52–60, which slots the counterpoise — **RF-gated on Mule B: if B12 efficiency drops > 1 dB with the slot, the cut-out is dead and the cell is 6.0 mm.** The RF EM model runs both cell boxes (6.0 and 6.5 mm, X = 19–62). The power model (§6 E-9) is re-run at **600 mAh conservative** (560–620 `[U]` for 6.0 mm), not 700. Capacity in writing from the cell vendor at T-max including PCM/wrap at 50 % SoC is a Gate G0 paper item. **Owners:** mechanical (Z), RF (slot), electronics (power). **Closes:** Mule B slot/no-slot; EVM-1 shim measurement of all six columns.

### C-8. Cell x-position and the keepout: doc §6.2 (cell 24–67, LRA 55–69) vs RF (cell ≤ 61, LRA ≤ 61, no metal in X > 61) vs mechanical (cell 19–62, LRA 52–60, brass bracket to 61)

- **Resolution:** the doc's own layout violates its own keepout (§5 R7) — **adopted: cell X = 19–62, LRA X = 52–60 top side, bracket ending ≤ 61 (polymer preferred; brass acceptable only if it ends ≤ 61), halo LED at X = 62–63, copper ends at 63.0, PCB substrate at 68.0.** The doc's "10 mm from the ring" rule is itself `[U]`; the cell at 19–62 is 9 mm from the ring at X = 71. Mule B measures **both** cell positions (19–62 and 24–67) and the number decides; if 24–67 must be used the crown-end connector strip at X = 16–19 gains 5 mm and the RF cost is the price. The 3.0 mm PCB rear-side strip at X = 16–19 (cell 3-way B2B, dock 5-way B2B, two tooling holes) is a layout closure item (§7 Step 11, §6 E-12). **Owners:** RF (keepout), mechanical (layout), electronics (strip closure). **Closes:** Mule B V-1/V-5 with cell/LRA at both positions.

### C-9. LRA steel can vs antenna keepout vs acoustics vs Art. 11

- Positions agree once C-8 is applied: LRA at X = 52–60 on a bracket soldered to the PCB, **≥ 0.3 mm air gap to the cell face, the lid and the front wall, no PSA to the cell** (§7 Step 9 — reacting the moving mass against the pouch drives it as a diaphragm and glues the battery in, defeating Art. 11); bracket first mode ≥ 800 Hz; acoustic ≤ 35 dB(A) at 10 cm `[U]` provisional, set from Mule C. The doc's "bracket tied to PCB **and cell mass**" (§3, §6.4) is corrected: PCB only. The RF model carries the can as steel Ø8 × 4.05 at 49.5–57.5 per §5 Step 4.5 — **harmonised to X = 52–60** (mechanical) so both domains model the same position. **Owners:** mechanical (bracket), electronics (DRV2625 braking), RF (position). **Closes:** Mule C acoustics with/without cell contact; Mule B with the can at 52–60.

### C-10. AMOLED PMIC switching vs RF sensitivity (TIS)

- The PMIC (boost + negative charge pump, ~1–2 MHz `[U]`) and its inductor are new noise sources next to a −108 dBm receiver. **Adopted (§5 Step 14, §6 E-5):** PMIC + shielded inductor at **X < 40** in the side strip beside the panel, input and output capacitors within 2 mm, ELVDD/ELVSS on inner layers between ground planes, load switch off and PMIC disabled when the screen sleeps; SPI SCK with 33 Ω series termination and routed away from the ANT trace. **Acceptance:** TIS screen-on (full white, max brightness) vs screen-off Δ ≤ 1 dB (§5 V-10); conducted spur scan on VSYS/V3. **Owner:** electronics; RF tests. **Closes:** EVM-1 V-10.

### C-11. SPI bandwidth vs animation vs the product's latency story

- nRF9151 SPIM ≤ 8 MHz `[V?]` (not in the PS extract opened; the PS front matter only lists "up to 4× SPI master with EasyDMA") → 126 × 294 × 16 bpp = 592.7 kbit = **74 ms per full frame → 13.5 fps**; a 4-wire interface with no QSPI (the SiP has none). **Adopted (§6 E-6/E-7):** partial-window updates (RM69310 column/row address windows `[U]` until the driver datasheet is opened) for the creature's animated region; full-frame only on wake; TE-synchronised writes; wake sequence (load switch → PMIC enable → SWIRE → sleep-out → first frame) budgeted at **100–200 ms `[U]`**. This changes the doc's §7.2 "creature looks up within ~15 ms": the **halo and the LRA respond within 15 ms; the screen follows within ≤ 200 ms** — a product-story correction recorded in §8. **Owner:** electronics/firmware. **Closes:** Mule A DK measurement of the real SPIM clock and the panel's sleep-out time; EVM-1 fps and wake-latency test.

### C-12. Satellite interconnect: 6-way FFC (doc, mechanical) vs 10 signals (crown)

- **Resolution:** **10 signals** (3V1_ON, MT_VDD_SW, GND, SDA, SCL, HA1, HA2, HB1, HB2, TACT) — both DRV5032DU outputs on both latches are required for ≤ 90° first-motion detection (§4 Design step 11); the doc's 6-way is superseded. Main-board side: a 10-way 0.5 mm connector (FH12-10S-0.5SH `[U]` confirm; 2.0 mm tall `[V]` for the 6S/8S) or a hot-bar pad field at the top-side strip X = 16–19.5 — column D has 7.8 mm of Z (§7 Step 6) so height is not the constraint; **the 3.0 mm x-depth of the strip is** (a 10-way FH12 body is ~3–4 mm deep `[U]`): if it does not close, the satellite tail is hot-bar soldered to a pad field (crown baseline) or the cell moves to X = 20–63 (Mule B). **Owner:** electronics; crown supplies the tail. **Closes:** PCB rev A layout (week 6–8).

### C-13. Sensor supply rail: 3.1 V −2 % = 3.04 V against a 3.0 V minimum (MT6701 `[V]`, AS5600L `[V]`)

- The load switch must add ≤ 20 mV at 14 mA (R_on ≤ 0.5 Ω, §4 Design step 19) — or the rail moves. AMOLED VDDIO max is 3.3 V (`[V?]` decision text) so a 3.3 V rail at +2 % (3.37 V) is out of spec for the panel; a **3.2 V** setting (3.14–3.26 V at ± 2 %) satisfies both the sensors and VDDIO **if the TPS62840's RSET table offers 3.2 V** `[U]` — the doc's RSET 71.5 kΩ → 3.1 V is itself `[V?]`. **Adopted:** keep 3.1 V with a ≤ 0.5 Ω load switch as baseline; evaluate 3.2 V at schematic once the TPS62840 Table 1 is re-read (§6 E-1, §8). **Owner:** electronics. **Closes:** schematic review; EVM-1 rail measurement under the 14 mA MT6701 load.

### C-14. Magnets: crown sensing magnet vs Hall latches vs dock-head magnets vs key fobs vs the LRA

- Positions: sensing magnet at X ≈ 6.25–8.75 (crown hub), latches at X ≈ 10.5 on r = 4.0; dock shim at X = 33–45 (> 20 mm from the latches, > 26 mm from the ring), head magnets in the dock (device carries none — a device-side magnet would cost Z and sit within reach of the 3.9 mT latches); LRA at X = 52–60 (> 40 mm from the sensors); the M-16 magnet bond is the **last** mechanical step so no process heat reaches it; keys shed steel filings into the labyrinth mouth (§4 Verification item 14). **Adopted:** no device-side magnet (Addendum A.2); verify no DRV5032 false latch while docked (head magnets > 25 mm from the sensing magnet) at EVM-1; 50 mT fob at 20 mm for 24 h adds ≤ 0.5 mAh/day (firmware confirms a latch edge with an MT6701 delta before waking the radio). **Owners:** crown (latches/magnet), mechanical (shim/dock), electronics (wake logic). **Closes:** EVM-1 A.5-9 dock test; §4 Risk 14 fob test.

### C-15. Debris chamber and the 15 mm-face wall

- Doc §6.4's 0.6 × 1.5 mm annular chamber in a ø13.30 bore leaves 0.25 mm of wall on the 15 mm faces. **Adopted (§4 Design step 8.2):** two arc pockets of 0.6 radial × 1.5 axial over ± 50° centred on the 27 mm faces; 0.15 mm deep on the 15 mm faces (wall ≥ 0.70 mm). Mechanical's J6 text ("0.6 × 1.5 mm debris chamber") is superseded; the bulkhead mould-flow and the crown-end corner-drop analysis (§4 Risk 11) must include the 0.70 mm wall. The buried grip electrode (C-4) must be routed clear of the pockets. **Owner:** crown (spec), mechanical (mould). **Closes:** Mule C item 10 corner drops; mould-flow on the tray.

### C-16. Crown material and permeability gate: 316L at µr ≤ 1.05 (crown) vs "Ti Gr2 preferred, brass + PVD, 316L only at µr ≤ 1.01" (mechanical)

- **Resolution:** **Crown wins** — 316L one-piece crown+hub with **cut** serrations (no rolled knurl, no welds, no rivets), lot gate µr ≤ 1.05 with a low-mu indicator (ASTM A342 `[U]`), Ti Gr5 as the Mule C control and the premium/fallback grade; the ASSDA "< 1.02 after cold work" statement does **not** cover 316L (re-tagged `[U]`). Brass is rejected (lead-bearing C36000 under REACH; soft; nickel-free but PVD-dependent). Decision rule: if Mule C INL with the 316L crown differs from the Ti control by > 0.3° after the 24-point EOL table, switch to Ti Gr5 (+$3.0/pc `[U]`). Nickel release (EN 12472 wear → EN 1811, `[V?]`) decides between PVD'd 316L and Ti for the skin-contact crown and lug. **Owner:** crown. **Closes:** Mule C items 7, 12, 13.

### C-17. Keyring lug position and load path

- Crown: lug insert-moulded in the crown-end bulkhead flank at "x ≈ 8–14" — evidently the **body** frame (its own crown frame ends at x = +10), i.e. X = 8–14; mechanical: insert-moulded 316L in the **tray** flank at X ≈ 6–10, on the right flank, with the collar clear of it. **Adopted:** lug insert-moulded in the **tray** (monolithic, carries 300 N; a snap-on collar must not), right flank, **X = 8–14**, with a clearance slot in the cosmetic collar; the 28 mm Dyneema interposer is mandatory (RF). Yank path: crown → C-ring → sleeve groove → ears (6.0 mm wide, C-2) → bulkhead; lug path: lug flange → tray flank. **Owner:** mechanical (lug), crown (yank). **Closes:** §4 Verification item 11; §7 DVT lug test (100 N × 60 s, 10k jerks).

### C-18. Sealing vs serviceability

- The cap/ring/tab joints (J4a/J4b/J9), the lens (J2) and the dock pads (J3) are permanent; the only user-openable joint is the lid (J1) — LSR bead 30 % squeeze, 12 snaps + 2 screws, retention ≥ 2 × (gasket + 26 kPa altitude) ≈ 230 N budgeted at ≈ 360 N; the crown module is a factory sub-assembly behind J5 and the diaphragm; the cell is on a connector with a stretch-release tab. Art. 11's wet-environment derogation is **not** relied upon (C/2025/214 `[V]`). No conflict between domains; the interface is that **the crown cartridge is not user-serviceable** — a failed crown is a unit swap. **Owner:** mechanical. **Closes:** DVT lid-service × 10 by naive users → IPX7; altitude → IPX7.

### C-19. Z-stack vs cell vs drop

- Agreed: cell located by its edges (lid perimeter ribs, tray stubs), free on the lid side into the 0.60 mm swell gap, bonded only on the PCB-side insulator; PCB clamped in Z between tray ribs and lid rib ends (0.05–0.10 interference through the gasket's compliance) so a drop never loads the display B2B or the SiP; lens −0.08 ± 0.05 sub-flush; bottom-side components under the cell limited to the insulator + connector strip at X = 16–19 (the doc's "22 µF bottom-side beside the SiP" is superseded: bulk caps go **top-side in the 5.8 mm strips beside the panel**, where ≈ 4.85 mm of height exists — §7 Step 5, §6 E-12). **Owner:** mechanical/electronics. **Closes:** EVM-1 shim measurement; 26-orientation drop.

### C-20. The doc's Mule C race and the §9.11 life rig

- Doc §10 builds Mule C with "hardened 17-4PH races"; §4 separates the 3-week feel mule (100k decay per variant) from the §9.11 qualification rig (1M indexes + 300k presses + talc + filings on the chosen variant only). **Adopted:** Mule C = feel + down-select with three race materials (C-1); the 1M rig starts at Gate G0 on the chosen variant and runs through EVM-1. **Owner:** crown.

### C-21. Interfaces that are *not* in conflict but must be written down (the hand-off list)

| Interface | From → To | Content |
|---|---|---|
| Crown conductors for the EM model | crown → RF | crown material/mass (316L 5.1 g vs Ti 2.8 g), **floating with a 1 MΩ bleed** (C-4), position (13 × 8 cup at the E-max), 17-4/BeCu/zirconia race, BeCu ring/washer/leaves, magnet, satellite PCB 22 × 10, buried electrode ring |
| Keepout and floor plan | RF → electronics/mechanical | copper ends X = 63.0 ± 0.1; nothing metallic in X > 61 except the feed; three-strip top-side plan X = 49–68 (§5 Step 11b, adjusted for the 68 mm PCB) |
| PCB z-datum | mechanical → RF | PCB seated on tray ribs (Z1); cap on the shell shoulder (Z2); stack ± 0.38 worst case → 2.5 mm free-height finger or PCB-referenced stop (§5 Step 6) |
| Z columns and placement rules | mechanical → electronics | SiP at X = 20–32 under the panel; shim 33–45; B2B 46–49; fold 49–51; flex tail never under the LRA; tall parts in the side strips |
| Satellite tail | crown → electronics | 10 signals, soldered tail or FH12-10S, pinout fixed (§4 Design step 13) |
| COEX0 | electronics → firmware/RF | `AT%XCOEX0=2,1,690,760,1,1700,2160` `[V]` syntax (nRF9160 guide v1.9), RF-active semantics; GPIO → IQS211B masking + 20 ms |
| EOL calibration data | crown → firmware | 24-point detent table + 8 latch-edge angles in main-MCU NVM (§4 M-23) |
| Cell spec sheet | mechanical → electronics | §7 Step 7: PCM trip, DC-IR, NTC β 3435, 3-contact B2B, mechanical acceptance |
| Leak-test value, EOL record, firmware versions | production → MES | §7 Phase 5 serialisation |

### C-22. Production programming and lock order: "MCUboot + app + modem in one pass, then APPROTECT locked" on the bare board (doc A.2, §7 Phase 5) vs the RTT factory-mode command on the finished unit (§5 M14)

- **Doc A.2 / mechanical (§7 Phase 5):** the bare PCBA is programmed and APPROTECT-locked at the bed-of-nails fixture; the finished unit is "recoverable through the dock by full erase".
- **RF (§5 M14):** `%XRFTEST` and `%XPRODDONE` are issued as a factory-mode command over the dock's SWD/RTT on the *finished* unit, after the radiated go/no-go — impossible once APPROTECT is set (RTT needs the debug port).
- **Electronics (§6):** the same channel is needed for eSIM confirmation and ship-mode entry; a locked, un-provisionable unit is the highest-irrecoverability production risk (ER-6).
- **Resolution — adopted:** bare board = passive test → image load → powered test → provisioning, **unlocked** (EM-6a → EM-7a → EM-6b → EM-7b); **APPROTECT + SECUREAPPROTECT are the last SWD operation at pack-out (EM-9b)**, after `%XPRODDONE`, eSIM confirmation and ship mode; the failed-unit path (recover → EM-7a → … → EM-9b, serial/pair code re-provisioned from the MES) is defined; A.2's "recoverable through the dock by full erase" is unchanged. §7 Phase 5 is read with the EM-9b step and the recovery path appended. **Also:** the doc's "charge current held off until dock presence" is a BQ25180 register rule (ICHG set only after a valid NTC read and VIN-good, E-1.2) plus a dock-head enable, never a device-side VBUS switch — a firmware-gated VBUS path is a dead-battery/ship-mode lockout (E-2, ER-1). **Owner:** electronics (fixture and jig sequence), production. **Closes:** EV-15 production-flow dry run before the first DVT lot.

### C-23. Sealed-unit EOL sleep current: "1 in 20 via SWD/PPK2, < 200 µA after 60 s" (§7 Phase 5) vs what a dock can measure

- **Mechanical (§7 Phase 5):** sleep current 1 in 20 via SWD/PPK2 (< 200 µA after 60 s) on the dock jig.
- **Electronics (§6 EM-9, EV-3):** with VBUS present the BQ25180 supplies SYS from VIN, so nothing on the dock sees the cell-side current; the "eDRX idle" figure needs a live attach the shield box does not have; and the first draft's EV-3 (135 µA) and EM-9 (200 µA) limits disagreed.
- **Resolution — adopted:** the sealed-unit EOL step becomes a **VBUS-side gross-leak screen, 1 in 20: charging disabled by I²C, screen asleep, modem `CFUN=0`, Δ vs the golden unit ≤ +50 µA `[U]`** after the BQ25180 VIN-side quiescent is characterised on 10 units (EV-3) — it catches a console left on (+600 µA) or a stuck screen, not a 10 µA fault (ER-20). The **cell-side ≤ 40 µA (`CFUN=0`)** is measured on the bare PCBA through the VBAT test pad (EM-6b) and on the golden unit every release (EV-3); the **eDRX-idle ≤ 135 µA mean over 30 min `[U]`** is an EV-3/lab number only. §7 Phase 5's line is read with this replacement; §2's "< 200 µA at 60 s" EVM-1 target is read as the EV-3 pair. **Owner:** electronics; production. **Closes:** EV-3 10-unit characterisation; OQ-19 (whether the VBUS-side screen is stable enough or is dropped for ORT cell-side sampling).

### C-24. Satellite tail, amended: 10-way (C-12) vs 12-way with two grounds; the TACT conductor is a BQ25180 /MR-domain net

- **C-12 as adopted:** 10 signals, FH12-10S-0.5SH `[U]` or hot-bar; the 3.0 mm x-depth of the strip is the constraint.
- **Electronics (§6 E-10, E-15):** the crown's ESD bleed (C-4) returns its TVS clamp current through the tail ground; on a 10-way tail that is one conductor beside the latch lines — proposes **12-way with GND on pins 1 and 12**; **FH12-12S-0.5SH exists in the same series `[V]`** (Hirose FH12 catalogue extract `bom-scratch\fh12.txt`: contact-array width 5.5 vs 4.5 mm, body 10.1 vs 9.1 mm; the series x-depth is not in the extract → `[U]`). **New:** TACT drives the BQ25180 /MR pin directly and the nRF reads it only through a gate-to-V3 N-FET limiter (E-13) — so the **TACT conductor idles at the /MR pull-up voltage (`[U]`, possibly VBAT-referenced; SLUSE99C not opened)**: the satellite's tact switch and trace must be rated for it and no nRF-domain logic shares that conductor (ER-10).
- **Resolution:** electronics proposes, crown decides at the rev A layout; if §4 keeps 10-way, E-10's pin order applies and EV-10 probes HA1 for ground bounce during the crown discharge (≤ 0.5 V). Connector height (2.0 mm `[V]`) is fine either way; the hot-bar pad field remains the baseline for both domains (§7 Step 6 column D). **Owner:** electronics proposes; crown decides. **Closes:** rev A layout (week 6–8); OQ-11; EV-2 TACT idle-voltage measurement.

### C-25. Dock pads: plating spec wording, pitch tag, and the fifth conductor

- **Mechanical (§7 Step 11) / doc A.2:** "Au over 1.0–2.5 µm Ni", 2.54 mm pitch tagged `[V]`, fifth conductor = dock presence.
- **RF (§5 M4):** ASTM B488 hard-gold classes for the feed land.
- **Electronics (§6 E-13, EV-8):** 1.0–2.5 µm Ni is thin for 30k cycles in sweat; the hostile review caught "Type II" mislabelling hard gold. Proposed wording: **ASTM B488 Type II (99.0 % Au, cobalt-hardened), Code C (hard), ≥ 0.76 µm over ≥ 2.5 µm Ni `[U]` until B488 is opened** — consistent with §5 M4; acceptance is EV-8's 30k cycles then ≤ 100 mΩ. The **2.54 mm pitch is `[U]`** — the doc's basis is "wearable-charger de facto standard", not a drawing (§0.1 rule: nothing is `[V]` without a source); §7 Step 11 and the first-issue §6 row are read with that tag. **Dock presence is read from the BQ25180 VIN-good via /INT** (no divider); the flex's **fifth conductor is re-assigned to jig ID/presence (EOL fixture only, 1 MΩ pull-down)** — §7 Step 11's connector pin list and the EOL jig spec follow.
- **Owner:** electronics (spec), mechanical (flex drawing). **Closes:** B488 opened at the flex drawing release; EV-8; OQ-12.

### C-26. Side-strip placement moves (§5 Step 11b, §7 Step 5) and the C-10 extension

- **First-issue §6:** BQ25180 + MAX17048 at X = 40–48 "near the connectors" (the connectors are at X = 16–19); MAX17048 on V3.
- **Electronics (§6 E-12, corrected):** **BQ25180 + MAX17048 + the three limiter FETs at X = 19–28 in the −y strip** (cell B2B, dock B2B and the SiP VDD within ≈ 10 mm; the 395 mA burst path ≤ 10 mm); **IQS211B at X = 24–30** (sense line still leaves on the crown side; electrode ≥ 40 mm from the cap holds); **AMOLED PMIC + inductor + switches A/B at X = 30–40 (−y)**; +y strip: 2 × 22 µF, eSIM X = 22–30, TPS62840 X = 34–40, NOR X = 40–46; halo FETs and the RF strip unchanged; **MAX17048 VDD on BAT** per the doc's block diagram (the gauge must read the cell with the buck off). A shielding-can footprint at X < 40 is reserved and, if fitted, is to be listed in §5 Step 4's conductor list.
- **C-10 extended:** two load switches (A on VCI/VDDIO from V3, B on the PMIC VIN from VSYS); the PMIC's IQ(off) and IQ(VIN present, CTRL low) are `[U]`; the wake order puts PMIC VIN on *before* SLPOUT so the panel's SWIRE burst is not lost. No change to the C-10 acceptance (TIS Δ ≤ 1 dB). C-11's 100–200 ms wake budget is refined to ≈ 135–160 ms `[U]` with a ≤ 200 ms provisional acceptance (halo/LRA carry the 15 ms). C-13 unchanged; E-1.6 adds the VCI ≥ 2.7 V check (passes).
- **Owner:** electronics; RF (conductor list). **Closes:** rev A layout; EVM-1 V-10.

### C-27. `%XMAGPIO` provisioning (§5 M12, first-issue §6 EM-4) vs the nRF9151 pin list

- The nRF9160 AT guide v1.9 `[V]` defines `%XMAGPIO`; whether the **nRF9151 exposes MAGPIO0–2 at all is `[V?]`** (not in the PS extract; OQ-3). **Adopted:** §5 M12 and EM-7b read "`%XMAGPIO` if present"; nothing in the design depends on it (no aperture tuner). **Owner:** electronics. **Closes:** PS pin list; Mule A EV-1 (f).

### C-28. AMOLED module storage temperature (§7 Step 4, doc §4.4) becomes a purchasing and warehouse requirement

- The module is not reflowed (mated at final assembly) but has a storage-temperature limit `[U]`; the doc's +60 °C dashboard warning (§7 Risk 11) transfers to storage. **Adopted:** modules stored ≤ 40 °C / ≤ 60 % RH in original trays, no bake, Tstg and storage conditions on the PO (EM-3, EM-5, §6.5 item 2); §7's final-assembly line must not bake or reflow the module. **Owner:** electronics (PO), production (warehouse). **Closes:** panel datasheet Tstg (§8 A-4).

### C-29. EU SKU EMC immunity and the dock's own EMC — new certification lines

- §5 Phase 4 covers radio and spurious emissions; nobody had listed immunity. **Adopted (EV-12):** EU SKU — EN 301 489-1/-52 radiated immunity (80 MHz–6 GHz, 3 V/m class `[U]`) and conducted immunity on the dock cable, ESD per EV-10; the dock board itself to EN 55032/55035 `[U]`. **Owner:** whoever owns the dock board (electronics by default); RF adds the lines to the §5 Phase 4 scope. **Closes:** DVT pre-scan; §8 C-8.

### C-30. Evidence-tag harmonisation from the electronics pass (§0.1)

- Every vendor web page (TI product pages for TPS65631/TPS22916, the Vybronics LRA page, the Mouser stock line) is `[V?]` in §6; the doc's `[V]` on the Vybronics page and the Mouser stock line, and the first-issue §6's `[V]` on the 2.54 mm dock pitch, are harmonised to `[V?]`/`[U]` wherever this report repeats them. `datasheets\ER-OLED018-1_Series_Datasheet.pdf` is the V1 1.8" SSD1326 PMOLED datasheet (BOM_VALIDATION_2026-09-04 §2), not an RM69310 source — no RM69310 or panel electrical table exists in the project. **Owner:** editor. **Closes:** on the next errata pass of the decision document.

---

## 4. Crown & crown-end assembly — domain report (coaxial baseline; transverse alternative in Design step 20)

*Frame: crown frame x (x = 0 at the crown-end shoulder face, +x into the body, crown front at −6.00); body X = x + 6.0. "Bezel" below = the tray's crown-end bulkhead (§0.4). Editor notes in italics mark §3 resolutions.*

### 4.1 What this subsystem is

The crown end is the only moving mechanism in the product and the only dynamic interface on a sealed capsule. It is a **coaxial knurled metal cup (13.0 OD × 8.0 mm, protruding 6.0 mm) with an integral ø7.0 mm hub** turned from one bar. The hub carries the **ø6 × 2.5 mm diametric NdFeB magnet in a pocket at its rear end, inside the crown's own 8 mm length** (the doc's "zero marginal length" topology, §6.2 — restored after the review showed the draft's shaft-head layout added ~2.9 mm and broke the 16 mm budget). The crown+hub rotates and translates **0.40 mm** (raised from 0.25 — see governing number 9) on a **one-piece static POM-C sleeve** that carries the two ø0.8 Si₃N₄ balls on BeCu cantilever leaves; the 24-groove race is bonded in the crown skirt and co-rotates with the magnet (*race material per §3 C-1: 17-4PH H900 wrought baseline, zirconia and BeCu built in parallel for Mule C*). A **BeCu wire C-ring** in matching grooves on hub and sleeve is the outward stop and the pull-out retention; a BeCu wave washer preloads the crown outward against it. Behind the hub, an **LSR diaphragm (0.30 mm skin) clamped on the sleeve flange is the bulkhead**; a PEEK-cored pip on its dry side presses one off-axis EVPBB tact on the satellite PCB. Nothing but flux crosses the diaphragm (*plus, per §3 C-4, one BeCu grounding leaf moulded into the sleeve for the crown's ESD bleed*). There are **no welds** and every joint is made from the rear in the order it is reached; PVD happens on the finished crown before any assembly.

**What changed from the draft (review outcome).** Accepted and fixed: zone closure (blocking); unreachable weld / 2.0-deep socket in a 1.6 wall (blocking) — eliminated by the one-piece crown+hub; press-stroke tolerance stack (blocking) — stroke 0.40, selective pip assembly, tolerance table in Design step 12; wave-washer datums — one datum set, one table; rotary O-ring drag — computed, made optional, Mule C measures with/without, Parker §8.13 gland rules applied; debris-chamber wall on the 15 mm faces — chamber now on the wide faces only; MIM race tolerances/hardness — wrought + wire-EDM after H900 is baseline, MIM demoted; DRV5032DU two-output — both outputs used, 8 edges/rev, worst-case gap computed 75°, flex 10-way; 316L ASSDA misattribution — re-tagged `[U]`, cut serrations only, Ti control on Mule C; concentricity chain — one worst-case chain, 0.28 mm; nickel release — EN 1811/EN 12472 added; EVPBB 1.0 N travel 0.08; R_b 4.25 and I from a mass build-up; 16 mm bar capacity; PCB placement ring; labyrinth bore tolerance; Mule C vs §9.11 life scope.

### 4.2 The numbers that govern it

| # | Quantity | Value | Tag / source |
|---|---|---|---|
| 1 | Crown envelope | 13.00 −0.03 OD over crests × 8.00 ± 0.03; protrudes 6.00 ± 0.10; recessed 0.4 radially inside the shoulder; 0.15 labyrinth in a reamed ø13.30 +0.05/−0 bulkhead bore | `[U]` doc §4.3/§6.2/§6.4 + this report |
| 2 | Detent count / pitch | 24 → 15° → 1.70 mm crest travel per detent (π·13/24) | computed |
| 3 | Ball-centre radius | R_b = 4.20 (land) / 4.30 (seated) → **4.25 ± 0.05** (race ID 9.20, ball ø0.80, groove 0.12 deep) | computed (draft's 4.4 corrected) |
| 4 | Detent torque | F_n seated 0.40 ± 0.08 N/ball, α_eff 30–35°, µ 0.10 → **T_peak 2.4–2.9 mN·m** nominal, 1.9–3.9 over tolerances; target 2.5–4.0 | `[U]` doc target; math step 6 |
| 5 | Crown inertia / coast | m ≈ 6.1 g (316L cup + hub + race + magnet), I ≈ 1.25 × 10⁻⁷ kg·m² (mass build-up, not ½mr²); barrier ≈ 0.23 mJ; KE at 5 rev/s ≈ 0.06 mJ; coast threshold ≈ 9.7 rev/s → **no coast**; §7.1 "coasts a third of a turn" must be dropped | computed, step 7 |
| 6 | Race material | 17-4PH **wrought** H900: UTS ≥ 1310, YS ≥ 1170 MPa, 40–48 HRC (Ulbrich sheet); MPIF-35 wrought H900 40 HRC / MIM H900 33 HRC, YS 1090 (Markforged sheet quoting MPIF 35); "strongly ferromagnetic in all conditions" (Ulbrich `[V?]`, ATI TDS `[V]` via §7) | `[V?]` two supplier sheets agree; SAE AMS 5643 / ASTM A564 / MPIF 35 text not opened |
| 7 | Hertz on the race | land contact 0.50 N: p₀ ≈ 2.1 GPa (E* 133 GPa, R_e 0.42 mm); shakedown ≈ 1.6·σ_y ≈ 1.9 GPa wrought / 1.75 GPa MIM → wrought marginal-OK, MIM ratchets | computed, step 6 |
| 8 | Angle sensor windows | MT6701: Bpk 200–1000 G at IC surface, AG (magnet-to-IC-surface) 0.5/1.0/2.0 mm, DISP ≤ 0.3 mm, VDD 3.0–5.5 V, power-up ≤ 1 ms, QFN 0.70–0.80 tall. AS5600L: VDD3V3 3.0–3.6 V, Bz 30–90 mT at die on a 1 mm circle (Bz_ERROR 8 mT), typical airgap 0.5–3 mm, **max axis displacement 0.25 mm with a 6 mm magnet**, WL-CSP Hall array **172.5 µm off chip centre**, INL ± 1°, I²C 0x40 programmable, IDD NOM 6.4 / LPM1 3.3 / LPM2 1.8 / LPM3 1.5 mA | `[V]` MT6701 DS Rev 1.5 §5 + tables; `[V]` AS5600L DS v1-12 |
| 9 | Press stack | Stroke **S = 0.40 ± 0.03** (hard stop crown skirt on POM flange); EVPBB2A9B000 1.6 N / 0.11 mm travel / H 0.53 **± 0.1**, general tol ± 0.05, 500k; 1.0 N and 0.7 N variants travel **0.08**; click at 0.27 mm nominal (RSS 0.17–0.37); over-travel absorbed by a 26 N/mm pip; force at click ≈ 2.9 N centre / ≈ 3.8 N rim | `[V]` Panasonic EVPBB DS; stack step 12 |
| 10 | Hall latches | DRV5032DU X2SON: **two outputs — OUT1 (pin 4) north, OUT2 (pin 3) south**; B_OP 1.2/2.5/3.9 mT, B_RP 0.9/1.8/3.5 mT, hysteresis 0.1/0.7/1.9; sampling period 27/50/75 ms; ICC 1.6 µA typ at 3 V | `[V]` TI DRV5032 DS (pin table, DU table, §7.3.2) |
| 11 | First-motion detection | both outputs on 2 devices at 90°, Bpk ≥ 4.5 mT: worst-case edge gap **≤ 77°** (B_OP min case 75°); OUT1-only: 121° (fails the doc's "within 90°"); plus ≤ 75 ms sampling latency (13.5° at 0.5 rev/s) | computed, step 11 |
| 12 | Journal / tilt | hub ø7.00 h7 in POM bore ø7.06–7.10, two lands spanning 6.9 mm → tilt ≤ 0.10/6.9 rad ≈ **0.8°** (doc's < 0.5° needed 12 mm that the zone does not hold) | computed, step 9 |
| 13 | Zone closure | crown front −6.00 … last far-side component +5.63 → **11.6 mm of 16.0, 4.4 mm spare** (2.9 with an FH12 connector); AG 1.0 rest / 0.6 pressed (MT6701); magnet-to-Hall 1.7 / 1.3 (AS5600L WL-CSP) | computed, step 15 |
| 14 | Concentricity chain (worst-case, systematic) | 0.01 + 0.05 + 0.02 + 0.05 + 0.05 + 0.10 = **0.28 mm** vs MT6701 0.30 ✓, AS5600L 0.25 ✗ → AS5600L variant needs 0.04–0.06 bore clearance and a package-body nest (→ 0.24) | computed, step 10 |
| 15 | Seal | O-ring optional; if fitted: FKM 75–80 ShA (*low-temperature GLT/GFLT class per §3 C-3*), 1.0 section, ID 1–3 % larger than shaft, 3–6 % squeeze, compressed from the gland OD (Parker §8.13); computed drag 0.15–0.35 mN·m running, 0.6–1.4 breakaway `[U]`; acceptance ≤ 0.5 running / ≤ 0.9 breakaway or delete it | `[V]` Parker O-Ring Handbook §6.3.16, §8.13, §8.17, §10.4 |
| 16 | Flex | **10 signals** (3V1_ON, MT_VDD_SW, GND, SDA, SCL, HA1, HA2, HB1, HB2, TACT); soldered flex tail baseline; FH12-10S-0.5SH fallback (2.0 tall; 6S/8S read in fh12.txt, 10S `[U]` confirm) | `[V]` Hirose FH12 (local) |
| 17 | Skin contact | REACH Annex XVII entry 27: Ni release < 0.5 µg/cm²/week, EN 1811 (+ EN 12472 wear/corrosion for coated parts) | `[V?]` secondary sources (Intertek/ComplianceGate); regulation text not opened |
| 18 | Life | 1,000,000 indexes = 41,667 rev ≈ 5.8 h at 2 rev/s; torque decay ≤ 15 % | doc `[U]`; rig time computed |

The AMOLED decision (screen sleeps, halo carries arrivals) changes nothing dimensionally here but makes the crown the only always-available input: the mechanical detents, the DRV5032 wake path (now 8 edges/rev) and the EOL detent-phase calibration carry more of the product. Coaxial vs transverse remains OPEN pending Mule C; coaxial is the baseline throughout, transverse is Design step 20.

### 4.3 DESIGN — step by step (coaxial baseline)

Axial datum: x = 0 at the crown-end shoulder face, +x into the body. Crown front face at x = −6.00. All positions are at REST (crown pushed outward by the wave washer against the retention ring). Full press = +0.40.

#### Design step 1. Architecture (what rotates, what translates, what is static) — redrawn

- **Crown + hub (rotates and translates, ONE turned part):** 316L (Ti Gr5 alternative) cup 13.0 × 8.0 with a 1.30 mm front wall and an integral **ø7.00 h7 hub** running from the front-wall inner face (−4.70) to **+2.80** (0.80 mm proud of the skirt rear end at +2.00). The hub has: two journal lands (−4.70 → −3.40 and −2.30 → +2.20), a ø6.20 relief between them (spring room), a **retention groove ø6.20 × 0.85 wide at −1.85 → −1.00**, and the **magnet pocket ø6.05 +0.02/0 × 2.60 deep opening at the rear face** (floor at +0.20). The magnet sits at +0.25 → +2.75, inside the crown's length. The race is bonded in the skirt bore. Because the part is one piece there is no weld, no socket, and PVD is done on the finished crown before assembly (M-7 precedes M-16). `[U]` architecture; settled on Mule C.
- **Sleeve (static, ONE moulded + machined POM-C part):** nose ø9.00 (−4.05 → −1.60) carrying the two radial ball pockets and two tangential leaf slots; journal ø10.90 (−1.60 → +2.40) on which the crown skirt bore ø11.00 runs; **flange OD 13.20 (+2.40 → +2.90)**, with two retention ears on the wide-face sides (*1.5 mm thick; widened to 6.0 mm per §3 C-2*); bore ø7.06–7.10 with a front land (−4.05 → −3.40) and rear land (−2.30 → +2.20); internal ring groove ø7.50 × 0.45 at −1.45 → −1.00; optional O-ring gland (+0.40 → +1.75) in the rear land; counterbore ø7.60 (+2.20 → +2.90) clearing the hub rear; two PCB locating pins on the flange rear at (± 6.0, 0). The sleeve enters the bulkhead from the rear and is the datum for everything (labyrinth bore, PCB, diaphragm). *[Editor, §3 C-4: add one moulded-in BeCu grounding leaf riding on the hub rear land, brought out through the flange rear to a satellite-PCB pad — the ESD bleed.]*
- **Retention / outward stop:** C17200 BeCu **wire C-ring ø0.40**, free OD ≈ 7.8, compressed flush into the hub groove (OD 7.00) for assembly, springs out into the sleeve groove (ø7.50) when it arrives: engagement 0.15 radial in the hub groove, 0.22 in the sleeve groove. Hub groove rear wall on the ring = rest position; hub groove width 0.85 = 0.40 wire + 0.40 stroke + 0.05. Pull-out path: crown → groove wall → ring → POM groove wall (bearing 100 N / (π·7.28·0.22) ≈ 20 MPa, POM yield ~60 MPa `[U]`) → sleeve → ears → bulkhead. BeCu, not 316 spring wire: cold-drawn 316 wire is partly martensitic `[U]`.
- **Wave washer (C17200 BeCu, stamped and aged; ID 7.2 / OD 9.6 / t 0.12, 3 waves, free height ≈ 0.95 `[U]`):** in the annulus between the crown front-wall inner face (−4.70) and the sleeve nose front face (−4.05): **working height 0.65 at rest, 0.25 at full press (solid 0.12 → 0.13 margin)**; rate ≈ 1.8 N/mm → 0.55 N preload at rest, ≈ 1.0 N at click (0.27), 1.3 N at the stop. One datum set — the draft's contradictory −4.0/−4.2/−4.4 values are gone.
- **Bulkhead:** LSR diaphragm (60 Shore A, platinum-cure), 0.8 mm rim bead in a groove on the flange rear face, 0.30 skin spanning the ø9.4 opening at **+2.85 → +3.15**, i.e. **G = 0.05 mm** behind the hub rear face. On the dry side, at r = 3.3 mm, a **pip: PEEK core ø1.4 × 0.60 insert-moulded, LSR cap 0.15** → pip top at +3.90. No rigid pressure plate, no feet: the draft's rigid PEEK plate is what made the stack un-tolerable.
- **Satellite PCB:** component face at +4.48, located on the sleeve pins; MT6701/AS5600L on the axis, crown-facing; tact at r 3.3 (top at +3.95, L = 0.05 to the pip); two DRV5032DU at r 4.0; flex on the far side.

#### Design step 2. Material selection — the permeability argument (corrected)

Requirement: every part within ~8 mm of the magnet other than the race must have µr ≤ 1.05 **measured after all forming/machining** (low-mu permeability indicator, ASTM A342 method `[U]` — standard not opened; the Severn-gauge-type indicator is industry practice).

| Candidate | Verdict | Why |
|---|---|---|
| 303 | **Reject** (doc, confirmed with a number) | Free-machining, sulphide-bearing, ~170 HV, σ_y ~240 MPa: Hertz shakedown ≈ 0.4 GPa vs 2.1 GPa land contact (step 6) → brinells at the first index as a race; as a crown body it also cold-works. |
| 304 | Reject | Lower Ni → strain-induced martensite on cold work; cold-worked austenitics "will be attracted to a permanent magnet" (ASSDA FAQ, qualitative `[V]`). |
| **316L** | **Baseline crown+hub** | Better than 304 but **NOT covered by ASSDA's "µr below 1.02 after cold work" statement — that sentence is about highly alloyed / high-nitrogen austenitics; ASSDA groups 304 and 316 together as grades that become attracted after cold work** (review finding accepted; draft's `[V]` was a misattribution). Md30 for 316L is around −10 to −30 °C `[U]`, so heavy cold work (rolled knurl, orbital forming) can produce martensite. Therefore: **cut serrations only** (no rolled knurl, no riveting, no welding — the one-piece design needs none), permeability gate M-4 on every lot, and a Ti control on Mule C. Cheap, PVD-able, ground finish Ra 0.2. Crown+hub ≈ 5.1 g. |
| 6061-T6 / 7075-T6 hard-anodised | Alternative (lightest, immune to nickel release) | µr ≈ 1.00. MIL-A-8625 Type III ~50 µm, half penetration / half build-up → ø grows ~0.05; crest R ≥ 0.10 or the coating chips `[V?]` anodiser pages, spec not opened. Race press in aluminium creeps; galvanic couple to the race in sweat; hardcoat serrations feel "sandy". |
| **Ti Gr2 / Gr5** | Premium alternative; **Mule C control unit** | µr ≈ 1.00005, 4.4 g/cm³ (crown ≈ 2.8 g), no nickel-release question, Gr5 ~36 HRC allows a true race interference fit. Machining 2–3× cost; PVD or AMS 2488 Type II anodise. |
| 440C / 17-4PH / 430 anywhere but the race | **Reject** | Ferromagnetic (17-4PH "strongly ferromagnetic in all conditions" — Ulbrich `[V?]`, ATI `[V]`); a static ferromagnetic part near the magnet adds angle-dependent field error. |
| Race: 17-4PH H900 **wrought** | Cost baseline (doc) — *§3 C-1: decided on the Mule C field map against zirconia and BeCu* | Only ferromagnetic part; coaxial and co-rotating with the magnet, so its distortion is a static reshaping of the 2-pole field, not INL; 4–6 mm from the magnet, expected < 5 % flux shunting `[U]` → FEMM in step 16. Passivate ASTM A967 (H900 is the most chloride-sensitive condition). |
| Race alternatives | Built for Mule C | Y-TZP zirconia CIM ring (HV ~1200, immune to sweat, non-magnetic — preferred fallback, and preferred outright if the O-ring is deleted in step 8); C17200 BeCu HT (38–45 HRC `[V?]` Materion via MatWeb) for a non-ferromagnetic metal race. |
| Magnet plating (Ni-Cu-Ni) | Sealed side | Behind the diaphragm cavity and the optional O-ring — not a skin-contact surface. |

**Nickel release (step 2b):** the crown (thumb/finger, minutes a day) and the keyring lug are prolonged-skin-contact articles under REACH Annex XVII entry 27 → Ni release < 0.5 µg/cm²/week per EN 1811, and EN 12472 simulated wear + corrosion before EN 1811 for the PVD'd crown `[V?]` secondary sources. Discriminator: if PVD'd 316L fails after EN 12472 wear at the serration flanks, the answer is Ti or hard-anodised Al, not a thicker PVD. Test in Verification item 13.

**What goes to the RF owner (Mule B) from this step:** crown material and mass (316L 5.1 g vs Ti 2.8 g), that the crown is **floating** (no galvanic path to ground by design; *ESD bleed is 1 MΩ per §3 C-4, RF-floating*), its position (a 13 × 8 mm cup at the counterpoise end, ~1 mm of PC/ABS from the buried IQS211B electrode → estimated 5–10 pF `[U]`), the race, the BeCu ring/washer/leaves, and the magnet. None of these are grounded; the EM model must carry them as floating conductors.

#### Design step 3. Crown body geometry (one part)

- OD 13.00 −0.03 over serration crests; length 8.00 ± 0.03 (front face to skirt rear end); front wall 1.30 with a 0.20 dish (1.10 min) — the dish steers the thumb toward the axis (reduces the rim-push penalty).
- Skirt bore, three diameters in one boring setup (concentric ≤ 0.01 TIR): **ø10.00 H8 (−4.70 → −4.20)** clearance behind the race, **ø10.60 H7 (−4.20 → −1.60)** race seat with the step at −4.20 as the race stop, **ø11.00 H7 (−1.60 → +2.00)** skirt journal, Ra ≤ 0.4; 0.2 × 45° chamfers at every bore mouth (race lead-in, ball lead-in).
- Hub as in step 1; magnet pocket and both hub lands turned in the same setup as the bores → pocket-to-hub concentricity ≤ 0.01.
- Recessed 0.4 mm radially inside the shoulder (shoulder silhouette ≥ 13.8); the last 2.0 mm of skirt (x 0 → +2.0) run inside the reamed ø13.30 +0.05/−0 bulkhead bore → labyrinth 0.15 nominal, ≥ 0.05 worst-case (step 8).
- Knurl: **straight (axial) serration, 48 teeth, 90° included, 0.85 pitch, crest flat 0.10, root R 0.10, 5.5 long, 0.25 run-out chamfers. Cut, never rolled** (step 2).

#### Design step 4. Race ring (wrought + hard finishing; tolerances relaxed to process capability)

- 17-4PH wrought bar, Swiss-turned in Condition A: OD 10.61 +0.01/−0 (0–0.02 interference in the 316L bore + anaerobic retainer; a 0.03 press would put ~470 MPa hoop in the 1.0 mm annealed wall, above yield), ID 9.20 ± 0.02, L 2.60, keyed notch. Age H900, then **wire-EDM the 24 grooves after ageing** (profile ± 0.005 achievable `[U]`), remove recast by tumble-lap/electropolish, passivate.
- Grooves: full-radius **R 0.45 ± 0.03, depth 0.12 ± 0.02**, edges blended R 0.10, **angular pitch 15° ± 15′, cumulative ± 20′** (the draft's ± 5′ / ± 0.01 were grinding-class numbers with no process basis — review accepted). What matters is torque-ripple uniformity ≤ 15 % (Mule C); the sensor, not the race, defines angle.
- Geometry check: chord of an R0.45 groove at 0.12 deep = 0.89 mm; land at ID = 1.204 − 0.89 = 0.31 mm → the ø0.8 ball always rests on two flanks or the land, never falls through.
- MIM (net-shape) is **not** baseline: MPIF-35 MIM H900 typical 33 HRC / YS 1090 MPa `[V?]` is below the shakedown line in step 6 — it ratchets. It may return only if a MIM lot measures ≥ 40 HRC and the 1M rig passes.
- *Zirconia and BeCu variants (§3 C-1): same OD/ID/L and groove geometry; zirconia by CIM/sintering + grinding (tool ~$10k `[U]`), BeCu turned + grooved in the solution-annealed state then aged 2 h @ 315 °C `[V?]`.*

#### Design step 5. Ball / spring carrier (in the static sleeve nose) — spring geometry re-derived

- Two radial pockets ø0.85 +0.02/0 at 180° in the ø9.0 nose at x = −2.90; balls ø0.800 Si₃N₄ ISO 3290 G5 (G10 acceptable) `[V?]` vendor pages.
- Space check that killed the draft's leaf: with the hub at ø7.0 under the ball plane there is only ~0.15 mm of radial room for spring deflection. Hence the **hub relief ø6.20 (−3.40 → −2.30)** giving 0.55 mm of room under the balls, without touching the journal lands.
- **C17200 BeCu cantilever leaf, 0.12 × 1.5 mm, effective length 4.5 mm**, lying tangentially in a slot milled into the nose from the outside (root clamped by a moulded boss; retained radially by the race ID — it cannot escape). Rate k = E·b·t³/(4L³) = 131e9 × 1.5e-3 × (0.12e-3)³ / (4 × (4.5e-3)³) ≈ **0.93 N/mm**; preload deflection 0.43 mm for 0.40 N; land climb 0.10 → +0.09 N → land force 0.49 N (ripple ratio 1.2 — a soft, even click). Bending stress at 0.49 N: 6·F·L/(b·t²) ≈ 0.61 GPa vs Materion Alloy 25 HT yield 1130–1420 MPa, fatigue 310–340 MPa reverse-bending at 10⁸ `[V?]` (MatWeb mirror of the Materion sheet); fatigue amplitude here ± 0.05 N ≈ ± 60 MPa → infinite life. Age 2 h @ 315 °C after forming `[V?]`.
- Ball protrudes ≤ 0.20 beyond ø9.0 with the crown off (leaf free-height stop) → cannot escape; even groove count + balls at 180° → both seat together, zero net radial load on the journal.

#### Design step 6. Detent torque math (R_b corrected)

Ball climbing a flank at angle α with µ: F_t/F_n = (sin α + µ cos α)/(cos α − µ sin α). At µ 0.10: α 20° → 0.47; **30° → 0.72; 35° → 0.84**; 45° → 1.22.
Baseline R0.45 groove 0.12 deep with R0.10 edges → α_eff 30–35°. **T_peak = 2 × R_b × F_n × ratio = 2 × 4.25e-3 × 0.40 × (0.72–0.84) = 2.4–2.9 mN·m**; over F_n 0.32–0.48 and µ 0.05–0.15: 1.9–3.9 mN·m. If Mule C wants a sharper click, steepen α (edge blend) rather than raising F_n.

Hertz: E* = 1/((1−0.27²)/310 + (1−0.3²)/200) GPa ≈ 133 GPa; on the **land** (sphere R0.4 on the concave R4.6 cylinder, R_e ≈ 0.42) at 0.49 N: p₀ = (6FE*²/(π³R_e²))^⅓ ≈ **2.1 GPa**; in the conforming groove ≈ 1.0–1.3 GPa. Shakedown ≈ 1.6·σ_y: wrought H900 (≥ 1170 MPa `[V?]`) → 1.9 GPa → mild shakedown/polishing of land edges in the first ~1k indexes, then stable — to be proven on the rig; MIM (1090) → 1.75 GPa → ratcheting → rejected as baseline; 303 (240) → 0.4 GPa → the doc's rejection with a number. *BeCu TH04 (1130–1420 `[V?]`) → 1.8–2.3 GPa, comparable to or above wrought 17-4; zirconia is far above.* Fallbacks: zirconia race; ø0.9 balls (p₀ ∝ R^−⅔).

#### Design step 7. Coast and damping — correction to doc §7.1

Mass build-up: skirt 2.0 g at r 6.0 → 72 g·mm²; front wall 1.4 g → 30; hub 1.7 g → 10; race 0.44 g at r 5 → 11; magnet 0.53 g → 2 → **I ≈ 1.25 × 10⁻⁷ kg·m²** (thin-walled cup, not ½mr²). Barrier energy ≈ T_peak × (π/24) × 0.64 ≈ 2.75e-3 × 0.131 × 0.64 ≈ 0.23 mJ. KE at 5 rev/s = ½·I·ω² ≈ 0.062 mJ. Threshold ω = √(2·0.23e-3/1.25e-7) ≈ 61 rad/s ≈ **9.7 rev/s** — a thumb flick is 3–5 rev/s `[U]`. **The crown cannot coast; delete "coasts about a third of a turn" from §7.1.** "Glide and weight" come from Coulomb + viscous drag in the hub journal, ring and (optional) O-ring: budget **≤ 0.5 mN·m running**, measured on Mule C (step 8). Pocket rattle: holding torque dwarfs any inertial torque on 10⁻⁷ kg·m².

#### Design step 8. Journal / seal stack (outside → inside), with the wall check

1. **Labyrinth:** crown OD 13.00 −0.03 in the **reamed** bulkhead bore ø13.30 +0.05/−0 (post-mould sizing, same reamer pass as the sleeve-flange seat → concentric ≤ 0.02): 0.15 radial nominal; worst case 0.15 − 0.02 (bore/flange) − 0.05 (hub clearance) − 0.03 (crown OD) − 0.02 (race/skirt) ≈ **0.03 ≥ 0** — never touches.
2. **Debris chamber — §6.4 amended:** the doc's 0.6 × 1.5 annulus in a ø13.30 bore leaves 0.25 mm of wall on the 15 mm faces (review, accepted). Chamber is now **two arc pockets of 0.6 radial × 1.5 axial over ± 50° centred on the 27 mm faces**; on the 15 mm faces the groove is 0.15 deep → bulkhead wall ≥ 0.70 mm there. *The IQS211B electrode is buried in the bulkhead wall (§3 C-4), routed clear of the pockets.*
3. **Skirt journal:** crown ø11.00 H7 on sleeve ø10.90 ± 0.02 (0.06–0.10 diametral), 3.6 mm long — a 0.03–0.05 gap that is itself a lint barrier for the race.
4. **Race + balls**, greased 2–4 mg PFPE (Krytox GPL 205-class `[U]`; PFPE is inert and FKM-compatible; silicone grease is incompatible with silicone rubber — Parker §6.3.16 `[V]`).
5. **Hub journal:** ø7.00 h7 (Ra 0.2) in POM-C ø7.06–7.10, two lands spanning 6.9 mm (tilt ≤ 0.8°). POM CTE ~110 µm/m·K: bore grows 0.03 over +40 K, shrinks 0.03 at −10 °C (still ≥ 0.03 clearance).
6. **Retention ring** (step 1) — rotates with the hub, slides in the POM groove; negligible drag.
7. **Rotary O-ring (OPTIONAL — a Mule C variable, not a settled part):** the draft's 12–15 % squeeze in a static housing groove with a silicone ring was reciprocating-seal practice on the wrong compound (review accepted). If fitted: gland in the sleeve rear land at +0.40 → +1.75 (1.35 wide), **FKM 75–80 Shore A (low-temperature GLT/GFLT class, §3 C-3), 1.0 section, ID 1–3 % larger than ø7.0 (≈ 7.1–7.2), compressed from the gland OD, 3–6 % squeeze** — Parker §8.13 Gough-Joule rule `[V]`; PFPE-greased; shaft lead-in 15°. Drag estimate `[U]`: load ≈ 0.03–0.06 N/mm × 22 mm circumference = 0.6–1.3 N normal; µ 0.06–0.08 mixed (Parker §8.17 `[V]`) → 0.04–0.10 N × 3.5 mm = **0.15–0.35 mN·m running; breakaway at µ ≈ 0.3 → 0.6–1.4 mN·m** — the same order as a detent, which is why it must be measured. Combined rotary + 0.4 mm reciprocation is Parker's §10.4 spiral-failure case `[V]` — mitigated by low squeeze, hard compound, grease, stroke ≪ section; inspected after the life test (Verification 3). **Acceptance: seal drag ≤ 0.5 mN·m running, ≤ 0.9 mN·m breakaway after 24 h at 40 °C (and at −20 °C); otherwise delete the O-ring** and make the mechanism wet-tolerant (Si₃N₄, zirconia race, POM, 316L/Ti) — the diaphragm alone protects the electronics.
8. **Sealed interior:** the hub-rear cavity and diaphragm; rim clamped between the flange and the PCB carrier (static seal). Water reaching the electronics must pass the (optional) O-ring **and** the diaphragm. *The flange/ear front face carries J5, the static face seal to the bulkhead inside face (§3 C-2).*

#### Design step 9. Tilt and guidance

Tilt bound = diametral clearance / span between outer land ends = 0.10 / 6.9 ≈ 0.8° (the coaxial skirt journal at r 5.5 with the same clearance tightens this slightly). Magnet tilt 0.8° is harmless to an on-axis 2-pole sensor `[U]` (Mule C INL confirms). The doc's "< 0.5° on a 12 mm journal" cannot exist inside the 10 mm of body the zone contains; 0.8° is the achievable number.

#### Design step 10. Magnet retention and one concentricity chain (worst-case for systematic terms)

- Magnet ø6.0 0/−0.05 × 2.5 diametric NdFeB N35–N42 (N35SH grade if any later process exceeds 80 °C `[U]`), catalogue part; pocket ø6.05 +0.02/0 × 2.60; retained by 3–5 mg Loctite 648-class retainer (0.05 film on the floor) plus a **3 × 120° stake of the pocket lip** (0.1 mm, non-magnetic tool, after bonding); face 0.05 below the hub rear face. Magnetisation axis laser-marked on the hub rear face for the EOL calibration. Bonded **last**, after PVD and mechanical assembly, so no process heat ever reaches it.
- **Chain (all systematic → arithmetic):** pocket-to-hub OD (one setup) 0.01 + hub in sleeve bore (full radial clearance under a rim side-load) 0.05 + sleeve bore to flange/PCB-nest (one secondary op) 0.02 + PCB on pins 0.05 + package placement 0.05 + die-to-package 0.10 `[U]` = **0.28 mm** vs MT6701 DISP 0.30 `[V]` (0.02 margin). AS5600L max 0.25 `[V]` → for that variant: bore clearance 0.04–0.06 (0.03 radial) and a moulded nest on the package body (0.03) → 0.24 ✓; the WL-CSP footprint must be offset **172.5 µm** so the Hall array, not the chip, is on axis `[V]`. Measure die-to-package on 10 samples (open question) — if it is 0.05, both variants gain 0.05.

#### Design step 11. Field levels and the latch geometry (DRV5032DU two-output)

- MT6701 wants 200–1000 G at the IC surface at AG 0.5–2.0 `[V]`; AG here is **1.0 rest / 0.6 pressed** (step 15) — mid-window `[U]` until FEMM + gaussmeter on Mule C with the race fitted. AS5600L WL-CSP: magnet-to-Hall 1.7 / 1.3 mm, needs 30–90 mT on the 1 mm circle `[V]` → expected 35–55 mT for N42 `[U]` — the weaker margin of the two; N42 minimum for that variant.
- **DRV5032DU is a two-output part:** OUT1 (X2SON pin 4) asserts on north flux above |B_OP|, OUT2 (pin 3) on south `[V]` TI DS pin table + §7.3. Under an off-axis diametric magnet Bz at each latch swings ± once per revolution, so **each device gives 4 edges/rev when both outputs are read**. Design: two devices at r = 4.0 mm, 90° apart, **both outputs on each → 4 GPIO lines (nRF9151 has 32 GPIO `[V]` PS), 8 edges/rev.** Worst-case first-motion gap computed with Bz = Bpk·cos θ: Bpk 8 mT / B_OP 2.5 typ → gaps 31° and 59° (max 59°); B_OP 3.9 max → max 55°; **B_OP 1.2 min → max 75°**; Bpk down to 4.5 mT → max 77°. **OUT1-only (the draft) gives 121° at typ — the doc's "within 90°" is not met that way.** Three lines (one device both outputs, one OUT1) gives exactly 90° — rejected as marginal. Add the DU sampling period 27–75 ms `[V]`: 13.5° at 0.5 rev/s petting, so first-motion ≤ 90° holds at petting speed; at a 5 rev/s flick the 75 ms sample gap (135°) dominates and the MT6701 (powered ≤ 1 ms after the first edge `[V]`) takes over.
- Target Bpk at the latches ≥ 8 mT (2 × B_OP max) so the 0.40 mm press (≈ +20 % field) cannot flip a state; firmware masks latch edges while TACT is low.
- MT6701's push-button detector needs a ≥ 31 % field step `[V]` (PUSH_THRD); a 0.40 mm approach gives ~20 % → **cannot replace the tact**; plausibility check only.

#### Design step 12. Bulkhead and press mechanism — toleranced

Why the draft failed: EVPBB height is **H ± 0.1** with ± 0.05 general tolerance `[V]`, larger than any sub-window of a 0.25 mm stroke. Fixes adopted: (i) **stroke S = 0.40 ± 0.03** (hard stop = crown skirt rear end on the POM flange front face, both machined; 0.25 was an ID number the tact cannot honour — needs ID sign-off, open question); (ii) **selective assembly**: tact-top height measured on every satellite PCBA relative to its component face (PCB thickness therefore out of the chain), diaphragm chosen from **3 pip-height bins (0.10 steps)** → residual ± 0.033 + 0.02; (iii) **compliant pip** for over-travel: PEEK core 0.60 + LSR cap 0.15 + 0.30 skin at ø1.4 → rubber column 0.45, shape factor 0.78, E_eff ≈ 7.7 MPa (60 ShA) → **k ≈ 26 N/mm** `[U]`: 0.06 mm pre-compression at 1.6 N, and over-travel of 0.25 costs +6.5 N (dome sees ≤ 8 N worst-case — Panasonic allowable static load is not on the datasheet, open question; if < 10 N, k → 18 N/mm and S → 0.45).

**Stroke stack (from rest, named tolerances):**

| Term | Nominal | Tol | Basis |
|---|---|---|---|
| Hub rest position (groove wall / ring / POM groove wall) | ref | ± 0.06 | turned ± 0.02, wire ± 0.01, machined POM ± 0.03 |
| G: hub rear face → skin | 0.05 | ± 0.05 | LSR mould ± 0.05 (on the machined flange datum) |
| Pip pre-compression at 1.6 N | 0.06 | ± 0.02 | pip stiffness ± 30 % |
| L: pip → tact top (after 3-bin selection) | 0.05 | ± 0.05 | H ± 0.1 binned to ± 0.033, pip height ± 0.02 |
| Tact travel | 0.11 | ± 0.02 `[U]` | Panasonic gives none |
| **Click travel** | **0.27** | **± 0.20 arith / ± 0.09 RSS** | RSS window 0.18–0.36 |
| Hard stop S | 0.40 | ± 0.03 | |
| Over-travel at the dome | 0.13 | 0.01–0.25 (RSS) | arithmetic worst-case −0.10 (no click) |

Arithmetic worst-case does **not** close even at 0.40 — stated plainly. The design relies on RSS plus a **100 % EOL press test (force–stroke curve, click 0.15–0.37, stop 0.37–0.43)**; the fallback is S = 0.45 with 5 pip bins. A 1.0 N tact (EVPBB1AAB000, **0.08 mm travel** `[V]`) moves the click to 0.24 and the force to ≈ 2.3 N; re-run the table for whichever Mule C picks.

- **Force at click** ≈ washer 1.0 N + tact 1.6 N + skin/rim 0.2 N + journal friction 0.1 N ≈ **2.9 N at the centre**; rim push at r 6.5 adds 2µr/L = 2 × 0.15 × 6.5/6.9 ≈ **+28 %** → ≈ 3.7 N; the pip's fixed off-axis reaction (1.6 N × 3.3 mm) adds ≈ +4 % everywhere. Cannot jam (jam needs r/L > 1/(2µ) ≈ 3.3). Acceptance ≤ +50 %, click at every thumb position.
- **Why one off-axis tact cannot cock:** the crown+hub is guided by 6.9 mm of journal at ø7 plus the coaxial skirt journal; the tact is loaded through the pip at r 3.3 by the rigid hub rear annulus (r 3.0–3.5); the moment from any thumb position is reacted by the journal, not by the dome.
- **Drop:** a 6 g crown at 2000 g (≈ 120 N) is reacted by the hard stop (skirt on flange, ≈ 6 MPa on POM) — the dome sees only the pip force at S (≤ 8 N).
- **Debounce:** press counted only if TACT low ≥ 30 ms (drop actuation < 5 ms).
- **ESD (path restated per §3 C-4):** with the IQS211B electrode buried ~1 mm inside the bulkhead wall, the crown's discharge cannot arc to the electrode's TVS; the designed path is now the **BeCu grounding leaf in the sleeve → satellite PCB → 1 MΩ ∥ low-C TVS → GND**. The dielectric barriers behind it (0.30 LSR ≈ 6 kV at ~20 kV/mm `[U]`; 0.6 PEEK pip ≈ 12 kV `[U]`; ≥ 0.55 air + mould compound to the MT6701) are the second line only. Verification item 9 tests 8 kV contact / 15 kV air with a current probe on the bleed line; the acceptance is justified by the bleed route, not by the dielectric numbers.

#### Design step 13. Satellite PCB layout constraints (22 × 10 × 0.6, 2-layer) — placement drawn to fit

- Angle sensor die centre on the crown axis, crown-facing side: MT6701 QFN 3×3 (0.70–0.80 tall `[V]`) or AS5600L WL-CSP 2.07 × 2.63 × 0.6 (`[V]`, footprint offset 172.5 µm, address 0x40 programmable via I2CADDR + BURN_SETTING `[V]`). MT6701 EEPROM programming needs VDD > 4.5 V `[V]` and AS5600L OTP burn needs ≥ 3.3 V with a 10 µF at VDD3V3 `[V]` → both done only on the bare-board fixture; firmware zero from raw angle in-system.
- **DRV5032DU A at (4.0, 0) on the long axis, B at (0, 4.0) on the short axis** (X2SON 1.4 × 1.1 reaches r 4.7 < 5.0 edge); both outputs routed (HA1, HA2, HB1, HB2); sensitive axis normal to the board.
- **Tact EVPBB2A9B000 (2.6 × 1.6 × 0.53) at r 3.3, 45° between the latches**, long axis tangential; 1.0 mm clear of the QFN edge; keep-out 0.2 around it for the pip.
- Two ø1.0 +0.02 locating holes at (± 6.0, 0) on the sleeve pins; alternatively (AS5600L) a moulded nest on the package body. No copper within 1.0 mm of the axis on the far side.
- **Interconnect: 10 signals** (3V1_ON for the latches, switched MT6701/AS5600L VDD, GND, SDA, SCL, HA1, HA2, HB1, HB2, TACT). Baseline **soldered flex tail (hot-bar, 0.5 mm pitch) exiting the +x long end**, far side, 0.30 stack; fallback FH12-10S-0.5SH (2.0 tall, 0.5 A, 20 cycles class `[V]` for 6S/8S; the -10S size `[U]` confirm). *Plus one pad for the ESD bleed leaf (1 MΩ ∥ TVS to GND on this board, §3 C-4).*
- Far side: flex, 100 nF decouplers (0402, 0.55 tall). Load switch for the sensor VDD stays on the main board.

#### Design step 14. Keyring lug + interposer (+ yank spec)

- 316L lug (non-magnetic; EN 1811 applies), insert-moulded into the **tray** flank (§3 C-17) at X ≈ 8–14 mm, ø3.0 hole, R ≥ 1.0 edges, 2.0 thick, retention flange ≥ 6 × 4 mm; **design pull-out ≥ 150 N `[U]`, test 300 N**.
- **28 mm Dyneema (UHMWPE) loop, 2 mm 12-strand, PU-coated**, moulded POM end fitting; ≥ 400 N after 10k flex cycles `[U]`. Purpose is RF (keep the 120 g bundle ≥ 28 mm off the counterpoise).
- **Crown yank:** a key bundle pulls on the crown — design ≥ 100 N `[U]`, test 150 N: hub groove wall (316L) → BeCu ring (double shear, ~0.25 mm² wire × 2 × ~700 MPa ≈ 350 N `[U]`) → POM groove (20 MPa bearing) → sleeve ears (*2 × 6.0 × 1.5 POM in shear ≈ 2 × 300 N `[U]` after §3 C-2*) → bulkhead. Magnet stray field at the labyrinth mouth **will** collect steel filings shed by keys → Verification item 14.
- A magnetic key fob near the latches (3.9 mT max B_OP `[V]`) can create edges → firmware confirms with an MT6701 delta before waking the radio.

#### Design step 15. Dimensioned axial stack — every solid body in x-order (rest position)

| Body | x (mm) | Tol | Note |
|---|---|---|---|
| Crown front face | −6.00 | ± 0.10 | protrusion set by ring/groove + sleeve in bulkhead |
| Crown front wall | −6.00 → −4.70 | 1.30 ± 0.03 | 0.20 dish, 1.10 min |
| Wave washer (working) | −4.70 → −4.05 | 0.65 (0.25 pressed) | free 0.95, solid 0.12 |
| Sleeve nose ø9.0 | −4.05 → −1.60 | | balls at −2.90 |
| Race (in skirt ø10.60) | −4.20 → −1.60 | 2.60 | ball −2.90 rest / −3.30 pressed, inside race |
| Hub front land ø7.0 | −4.70 → −3.40 | | |
| Hub relief ø6.2 | −3.40 → −2.30 | | spring room |
| Hub groove ø6.2 × 0.85 | −1.85 → −1.00 | ± 0.02 | rear wall on ring = rest |
| Sleeve ring groove ø7.5 × 0.45 | −1.45 → −1.00 | ± 0.03 | BeCu ring ø0.40 |
| Sleeve journal ø10.9 / crown bore ø11.0 | −1.60 → +2.00 | | |
| (Optional) O-ring gland | +0.40 → +1.75 | | rear land |
| Magnet pocket floor / magnet | +0.20 / +0.25 → +2.75 | | face 0.05 below hub face |
| Crown skirt rear end | +2.00 | ± 0.03 | hard stop travels to +2.40 |
| Sleeve flange front face = hard stop | +2.40 | ± 0.03 | **S = 0.40** |
| Hub rear face | +2.80 | | 0.80 proud of skirt |
| LSR skin | +2.85 → +3.15 | ± 0.05 | G = 0.05 |
| Pip (PEEK 0.60 + LSR 0.15) | +3.15 → +3.90 | binned | at r 3.3 |
| Tact top / body | +3.95 / +3.95 → +4.48 | H 0.53 ± 0.10 | L = 0.05 |
| MT6701 top (QFN 0.75) | +3.73 | 0.70–0.80 | skin at full press +3.55 → 0.18 clear |
| Satellite PCB | +4.48 → +5.08 | 0.60 ± 0.06 | component face is the datum |
| Far side: flex solder / 0402 | → +5.63 | | FH12 alternative → +7.10 |
| Zone end (x = 16.0 − 6.0) | +10.00 | | **spare 4.4 mm (2.9 with FH12)** |

Magnet → IC: **MT6701 AG = 3.73 − 2.75 = 0.98 ≈ 1.0 mm rest, 0.6 pressed** (DS window 0.5–2.0 `[V]`). **AS5600L WL-CSP: magnet-to-Hall ≈ 1.7 rest / 1.3 pressed**, inside "0.5–3 mm typical" `[V]`; field margin is its risk (step 11). The doc's crown-zone budget (6.0 + 2.0 + 0.25 + 1.25 + 1.3 + 0.6 + 2.6 + 2.0) is honoured with room to spare; the far-side option of mounting the MT6701 through the PCB would buy a further 0.65 mm and is held in reserve.

#### Design step 16. Analyses before Mule C drawings freeze

FEMM/Maxwell: B at the IC (both variants) and at the two latches vs angle, with/without each race material and the stainless tact dome at r 3.3 (dome alloy `[U]` — SUS301 domes are cold-rolled and partly ferromagnetic), press-induced field change (+0.40), stray field at the labyrinth mouth. Hertz/shakedown on the groove candidates. LSR skin + pip stiffness and 300k-cycle fatigue at 0.40. Ring/groove bearing at 150 N; ears at 300 N. Drop: 120 N on the hard stop. Journal PV (trivial). Seal drag (step 8). *ESD bleed leaf contact force and wear over 1M indexes.*

#### Design step 17. Firmware/system interfaces this mechanism imposes

Wake: any of 4 latch edges → power the angle sensor (MT6701 ≤ 1 ms `[V]`; AS5600L LPM3 polling 100 ms `[V]` if that variant idles powered) → confirm ≥ 1 detent of delta within 200 ms → radio. Press: TACT low ≥ 30 ms; latch edges masked while TACT low. Angle: firmware zero from raw angle; **per-unit 24-point detent table** (raw angle at each detent, captured at EOL, stored in the main MCU NVM) turns static INL from the race/dome into a lookup, so the sensor's ± 1° (AS5600L `[V]`) / ± 1.5° (MT6701 `[V]`) never reaches the user. Latch edges are also recorded against raw angle at EOL.

#### Design step 18. Grip electrode interaction

The IQS211B annular electrode is buried in the static bulkhead wall ~1 mm behind the shoulder (§3 C-4; doc §7.4 places it on the static shoulder). The floating crown a millimetre away is a large capacitive load that moves 0.40 mm on a press → expect a press-correlated Cx step; firmware blanks grip during TACT low; the doc §9.8 coupon must include a press. Triboelectric charge from POM-on-316L rotation is why the electrode is not on the crown (doc reasoning retained) — and why the crown now has a 1 MΩ bleed.

#### Design step 19. Rail note (AS5600L verified)

MT6701 VDD min 3.0 V `[V]`; **AS5600L VDD3V3 min 3.0 V `[V]`** (DS v1-12, 3.0/3.3/3.6). The 3.1 V rail at −2 % is 3.04 V → both variants are 40 mV from their floor: the switched supply must add ≤ 20 mV at 14 mA (MT6701 max) / 6.4 mA (AS5600L NOM) → load switch R_on ≤ 0.5 Ω, or feed the sensor from a 3.2/3.3 V rail if the main board has one (§3 C-13).

#### Design step 20. Transverse-wheel alternative (if Mule C picks stroke over twist) — with a sealing scheme

- Wheel ø13 × 5.0 wide, axis across the body width (Y), rim proud ~2.5 mm through a **slot in the end/top face with a 0.15 mm gap and a debris pocket beneath**; the wheel lives in a **wet cavity**; the cavity floor (0.5 mm polymer) is the bulkhead; no dynamic seal exists anywhere.
- Detents: same race-in-wheel / balls-in-static-carrier scheme on the wheel bore; carrier = the fixed axle stub; reuse balls, leaves, race tooling geometry.
- Sensing: (a) MT6701 on-axis on a mini PCB standing perpendicular to Y outside the cavity wall at one axle end (magnet in the axle end, 1.3 mm through a 0.5 wall) — satellite becomes an L-flex; or (b) side-shaft sensor (MPS MA782-class `[U]`) under the rim with the magnet on the axle mid-plane — the doc's route, a different satellite variant.
- Press: wheel + axle in a POM cradle translating 0.40 mm onto an LSR-diaphragm-covered tact under the cavity floor; guide = the cradle's two axle bearings 5 mm apart → the "cannot cock" argument becomes a rocker argument (≤ 2.5 mm lever on a 5 mm rim).
- Coast: same physics — none. Zone: −3 mm (13 mm), given to the RF keepout buffer (§5 Step 11). Cost delta: +1 mould (cradle), sensor variant, −1 O-ring/diaphragm ring; ID delta: the wheel breaks the silhouette on two faces (§7 Step 12: the slot is in the collar's left flank, the tray tool is unaffected if the interface is frozen at Gate G0).

### 4.4 MANUFACTURING — process flow and assembly sequence (every joint reachable in the order it is made)

#### A. Crown + hub (316L baseline, one part)

**M-1. Stock and lot control.** 316L bar **ø14**, ASTM A276 solution-annealed, mill cert Ni ≥ 10.5 %, N ≤ 0.10 %; incoming permeability µr ≤ 1.02 (indicator). Reserve 3 crowns/lot for the M-4 coupon.

**M-2. Swiss-type CNC turn-mill, ≥ 16 mm bar capacity (a 13 mm machine cannot feed ø14), one main-spindle setup for every coaxial feature:** OD 13.00 −0.03 (pre-serration land), skirt bores ø10.00 / 10.60 H7 / 11.00 H7 in one boring pass (≤ 0.01 TIR), hub lands ø7.00 h7, relief ø6.20, retention groove ø6.20 × 0.85, magnet pocket ø6.05 +0.02 × 2.60 (sub-spindle, back-working), 0.20 dish, chamfers 0.2 × 45° at every bore mouth and 15° lead-in on the hub rear. Low-sulphur inserts, emulsion coolant. Turning cycle ≈ 90–120 s.

**M-3. Serrations — cut, not rolled.** Live-tool 90° single-angle cutter on the same machine (48 axial passes, ≈ 120–180 s — costed separately in Sourcing) or a gear-shaper/hobbing secondary at volume: 48 teeth, 0.85 pitch, 5.5 long, stop 0.25 short of the shoulder land; OD 13.00 −0.03 over crests. **No rolled-knurl proto path.**

**M-4. Permeability coupon (lot gate).** 3 serrated crowns/lot measured at the serrations and at the hub groove with a low-mu indicator: **µr ≤ 1.05 accept**; > 1.05 → solution anneal (1040–1100 °C, water quench `[U]`) or scrap; record. This is what makes the doc's "measured after machining" a spec.

**M-5. Deburr / finish.** Ultrasonic degrease → vibratory tumble (ceramic media, 2–4 h) to R ≥ 0.05 on crests → optional electropolish 5–10 µm → passivate ASTM A967.

**M-6. PVD (before any assembly — the crown is a finished part when assembly starts).** Cr adhesion + DLC (a-C:H 1.5–3 µm, ≥ 2000 HV) or ZrN/TiN, planetary fixture so flanks coat; **plug-mask the skirt bores, hub and pocket** (bare 316L for the adhesive and journal). Al variant: MIL-A-8625 Type III 50 µm, bores masked or post-honed, crest R ≥ 0.10 `[V?]`; Ti: AMS 2488 Type II. QC: VDI 3198 indentation HF1–3, calotest thickness, ΔE ≤ 1.5. **Nickel release sample (EN 12472 wear → EN 1811) from the first PVD lot** (Verification 13).

**M-7. Race bonding.** Clean bore; Loctite 648-class on the race OD; **press from the rear** with an annular anvil over the hub, past the ø11.00 section into ø10.60, to the −4.20 step (0–0.02 interference, 50–150 N); index the keyed groove to the crown's laser mark; cure. Check: race ID run-out to the skirt journal bore ≤ 0.02 TIR. (Ti Gr5 crown: true 0.02–0.03 press, no adhesive.) *Supersedes §7 station C1's 200–400 N press.*

#### B. Race ring (17-4PH wrought baseline — MIM demoted; zirconia/BeCu variants per §3 C-1)

**M-8. Swiss-turn** in Condition A from ø11 bar: OD 10.61 +0.01/0, ID 9.20 ± 0.02, L 2.60, keyed notch, 0.2 chamfers.

**M-9. H900 age:** 482 °C / 1 h / air (schedule `[U]` — ASTM A564 / AMS 5643 text not opened; property targets `[V?]` Ulbrich + MPIF-35-via-Markforged sheets). Hardness 5 pcs/lot: **≥ 40 HRC accept** (a MIM lot would be gated here too — MPIF-35 typical 33 HRC is expected to fail). *BeCu variant: age 2 h @ 315 °C `[V?]`, 38–45 HRC accept.*

**M-10. Hard finishing after ageing:** wire-EDM the 24-groove internal profile (R0.45 ± 0.03, depth 0.12 ± 0.02, pitch ± 15′, cumulative ± 20′) → tumble-lap (3 µm alumina) or electropolish to remove the recast layer (5–10 µm `[U]`) → Ra ≤ 0.4 in the groove → passivate ASTM A967. Bridge/proto: push-broach in Condition A then age (distortion ~0.05 % `[U]`), accepting wider tolerances. *Zirconia: grooves ground after sintering; no recast, no passivation.*

**M-11. Race QC:** optical/CMM pitch, groove R and depth; go/no-go OD/ID; hardness per lot; magnetic moment check (residual magnetisation after EDM/handling — demagnetise before assembly, it sits 4 mm from the sensing magnet; 17-4 variant only).

#### C. Balls, leaves, ring, washer

**M-12. Balls:** Si₃N₄ ø0.800 G5 (G10 acceptable) from a ceramic-ball specialist (Tsubaki-Nakashima, CoorsTek, Redhill, Boca class `[U]`). Lot cert: diameter variation, sphericity, no magnetic response. 2/unit + 2 % attrition.

**M-13. Leaves:** C17200 strip 0.12, photo-etched (progressive die > 50k/yr) to the 1.5 × ~5.5 cantilever with a ball-locating dimple and clamp root; formed (r ≥ 4t); **aged 2 h @ 315 °C after forming** `[V?]` (Materion HT). Spring rate on 10 pcs/lot: 0.93 ± 0.15 N/mm; force at installed deflection 0.40 ± 0.08 N.

**M-13b. Retention ring:** C17200 wire ø0.40 HT, C-ring free OD ≈ 7.8, gap ≈ 1.0, ends deburred; 10 pcs/lot: free OD, spring-back after closure to 7.0.

**M-13c. Wave washer:** C17200 strip 0.12 stamped 3-wave, ID 7.2 / OD 9.6, aged; force at 0.65 working height 0.55 ± 0.15 N, at 0.25: ≤ 1.5 N; permeability indicator on 3/lot (non-magnetic by design; 316 washers only if measured ≤ 1.05).

**M-13d (new, §3 C-4). ESD bleed leaf:** C17200 strip 0.08, etched, aged; insert-moulded in the sleeve with the contact tip on the hub rear land (0.05–0.10 N `[U]`) and the tail exiting the flange rear; continuity check hub-to-pad ≤ 10 Ω on every cartridge (M-19).

#### D. Sleeve (POM-C) and diaphragm

**M-14. Injection-mould the sleeve** in POM-C (Delrin 500P-class, unfilled): nose, pockets, leaf slots/bosses, bore (core pin), journal, flange, ears (6.0 wide), ring groove, PCB pins, keys, optional gland, bleed-leaf insert; 2-cavity tool, 8–12 wk. **Secondary op in one chucking (the datum op):** ream the two bore lands ø7.06–7.10 (or 7.04–7.06 for the AS5600L build), turn the journal ø10.90 ± 0.02, the flange OD 13.20 h9, the flange front face (hard stop, ± 0.03) and rear face (diaphragm datum), cut the ring groove (± 0.03) → all concentric ≤ 0.02 and one axial datum. Mould shrinkage (2 %) is therefore not the fit tolerance. Proto: machined from POM-C rod.

**M-15. Diaphragm:** LSR 60 ShA platinum-cure, 0.30 ± 0.05 skin, 0.8 rim bead, insert-moulded over the PEEK pip core (through-hole mechanical lock — LSR does not self-bond to PEEK without primer, open question); **three cavities differing only in pip height (0.10 steps)** for selective assembly; check skin thickness and pip height ± 0.02, no flash on the pip cap. Proto: loose LSR disc + machined PEEK pip in 3 heights.

#### E. Magnet

**M-16. Magnet bonding — LAST mechanical step, after M-19 (no process heat afterwards).** Class-100k area, non-magnetic tooling: 3–5 mg retainer in the pocket; magnet placed by vacuum tip in a nest that orients the magnetisation axis to the hub's laser mark (± 2°, Hall probe in the nest); 3 × 120° stake of the pocket lip (0.1 mm); cure. Measure B at 1.0 mm on-axis: window set by Mule C (expect 40–90 mT `[U]`); reject outside ± 15 % of lot mean; pull test 20 N on 3/lot.

#### F. Sub-assembly sequence (crown cartridge) — all from the rear, no line-of-sight problems

**M-17. Station 1 — sleeve prep:** leaves into the tangential slots (root under the boss); balls into the pockets (vibratory feeder + vision count = 2); 2–4 mg PFPE on the pockets; optional O-ring (low-temperature FKM 75–80 ShA, PFPE-greased) into the gland from the rear; ring groove clean; bleed-leaf tip inspected.

**M-18. Station 2 — crown onto sleeve:** crown (with race, M-7) face-down in a nest; **wave washer dropped over the hub against the front wall**; **BeCu C-ring compressed into the hub groove** (flush at ø7.0, held by a split collet); sleeve pushed on from the rear over the hub — the 15° lead-ins guide the hub into the bore and the race chamfer pushes the balls in 0.1 as the nose enters the race; at the end of the push the ring snaps out into the sleeve groove (audible / force signature logged — the sleeve is now captive). Rotate 2 turns with torque monitored (1.9–3.9 mN·m band, 24 ripples/rev).

**M-19. Station 3 — cartridge test:** torque profile CW/CCW at 0.5 rev/s (with and without O-ring at Mule C; production: as built), axial play at rest 0.02–0.06, stroke to hard stop 0.37–0.43, crown run-out to sleeve journal ≤ 0.03 TIR; bleed-leaf continuity. Then **M-16 magnet bonding**, then re-measure B on axis.

**M-20. Station 4 — satellite pairing (selective assembly):** measure tact-top height on the PCBA relative to its component face (optical or contact, ± 0.01); pick the diaphragm bin; seat the diaphragm bead in the flange groove; nest the PCB on the two pins (component face on the flange rear); fit the PCB carrier ring (clamps the bead, captures the PCB); **connect the flex (hot-bar) or seat the FH12**; solder the bleed-leaf tail. Record the bin in the unit's build record. *Fit the J5 face-seal ring on the flange/ear front face (§3 C-2).*

**M-20b (from §7 station C9). Module leak test (100 %):** cartridge in a plug fixture sealing the tray-side face; helium/forming-gas sniff or pressure decay at 200 mbar; ≤ 1 × 10⁻³ mbar·L/s equivalent (correlated at DVT).

**M-21. Station 5 — into the tray bulkhead (from inside the tray, before the lid — §3 C-2):** insert the cartridge crown-first through the reamed ø13.30 bore until the ears seat in their wide-face pockets against the bulkhead's inside face with the J5 face seal compressed 25–30 %; secure the carrier/ears (2 × M1.4 into bulkhead bosses or ultrasonic stake); labyrinth check with a 0.05 feeler at 4 positions; press test through the crown (click 2.3–3.5 N centre, stroke to click 0.15–0.37, hard stop 0.37–0.43); tact continuity; **EOL calibration capture** (M-23) may be done here or at final EOL. Route the 10-way tail to the main-board connector. *[This is §7 Phase 3C station 10.]*

**M-22. Grease audit:** weigh 10 cartridges/lot before/after grease (± 0.5 mg) — grease mass is the first thing an operator drifts.

**M-23. EOL calibration capture:** rotate 2 turns on a motorised spindle; log raw angle at each of the 24 detents (MT6701 14-bit / AS5600L 12-bit), the 8 latch-edge angles, and magnet-field status bits; store the 24-point table + edge angles in the main MCU NVM; reject if < 22 detents resolve as 15 ± 1.5° or any latch output does not toggle exactly 2×/rev.

#### G. End-of-line (finished device or bulkhead sub-assembly)

- **Torque:** 1.9–3.9 mN·m peak (target 2.5–4.0 after Mule C sets F_n), ripple 24 ± 0/rev, CW/CCW asymmetry ≤ 15 %, running drag (between detents) ≤ 0.5 mN·m.
- **Run-out / labyrinth:** crown OD to bulkhead bore ≤ 0.05 TIR; feeler 0.05 passes at 4 positions.
- **Press:** 100 % force–stroke curve: click 2.3–3.5 N centre; ≤ +50 % at r 6.5 in 3 positions; click travel 0.15–0.37; hard stop 0.37–0.43; return without stiction.
- **Sensing:** monotonic raw angle over a turn; ≥ 22/24 detents at 15 ± 1.5°; MT6701 Mg[3:0] "OK" / AS5600L MD = 1, ML = MH = 0 `[V]`; each of the 4 latch outputs toggles exactly 2×/rev, on-sector 30–47 % of a revolution, max edge gap ≤ 80°.
- **Seal:** the closed capsule's fine-leak test (§7 Phase 4) covers the crown; the crown domain's vacuum-decay figure (−0.2 bar, ≤ 5 Pa/s `[U]`) is superseded by the product limit 1 × 10⁻³ mbar·L/s and the DVT correlation.
- **Life rig (qualification under §9.11, not EOL):** 2 rev/s, 1,000,000 indexes (≈ 5.8 h) with torque logging; 300k rim presses on a pneumatic rig; accept torque decay ≤ 15 %, groove wear ≤ 5 µm, press curve within ± 15 %; then 200k with 20 mg talc and 200k with 50 mg steel filings; O-ring inspected for spiral marks (Parker §10.4).

### 4.5 VERIFICATION — Mule C (feel + down-select, doc scope: ~$4k, 3 weeks) and the §9.11 qualification rig (separate line)

**Build:** two SLA/printed crown-end blocks (coaxial, transverse) with **real** parts: Swiss-turned one-piece 316L crown+hub (cut serrations, PVD on 3 of them, bare on 3), **one Ti Gr5 crown as the permeability control**, wire-EDM'd wrought 17-4PH H900 rings **plus Y-TZP and BeCu TH04 rings (§3 C-1)**, G5 Si₃N₄ balls, etched/aged BeCu leaves, machined POM-C sleeves (proto: machined from rod, with the bleed leaf), BeCu rings and washers, low-temperature FKM O-rings (75–80 ShA) fitted on half the units, LSR diaphragms (proto: loose LSR disc + machined PEEK pip in 3 heights), EVPBB tacts on a real satellite PCB with MT6701 and 2 × DRV5032DU (both outputs wired), plus VG0840001D + DRV2625-DK. Variants: (A) R0.45/0.12 groove, F_n 0.40; (B) same, 0.50; (C) 90° V, 0.30 — on coaxial; (A) on transverse.

**Tests and acceptance (Mule C):**

1. **Geometry decision (blind, 10 hands, 20 s):** coaxial vs transverse ≥ 7/10 or decided on engineering grounds (coaxial: no cradle, no slot). *If transverse wins:* satellite respin to L-flex (keep MT6701) or MA782 side-shaft; zone −3 mm to the RF buffer; shell CAD waits for the collar interface only.
2. **Detent torque:** rotary sensor 0–20 mN·m / 0.01, 0.5 rev/s: peak 2.5–4.0, ripple 24/rev, CW/CCW ≤ 15 %, **ripple uniformity ≤ 15 % across the 24** (this is the race-tolerance proof). *If fail:* leaf thickness ± 0.02 moves torque ± 40 % before touching the groove.
3. **Torque decay over 100k indexes per variant** (doc's Mule C number): ≤ 15 %; no visible groove marking. *Then the chosen variant only* goes to the §9.11 rig: 1,000,000 indexes, 300k rim presses, talc 200k, steel filings 200k — accept ≤ 15 % decay, ≤ 5 µm wear, ball SEM unchanged, no jam, O-ring free of spiral marks. *If brinelling:* lower F_n / steeper α, zirconia race, ø0.9 balls.
4. **Seal / journal drag:** torque trace with and without the O-ring; breakaway after 24 h dwell at 40 °C **and after a −20 °C soak (§3 C-3)**; running at 0.5 rev/s. **Accept ≤ 0.5 mN·m running, ≤ 0.9 breakaway** (≤ 25–30 % of detent peak); *if fail:* delete the O-ring and switch the race to zirconia (wet-tolerant mechanism), or PTFE-lip rotary seal.
5. **Coast/rattle:** high-speed video of a 5 rev/s flick — stops within one pitch (confirms step 7); 10–500 Hz 2 g sine + 50 g / 6 ms shock: no audible rattle, no latch or tact edge.
6. **Press:** force gauge on a 3-axis stage at r = 0, 3, 6.5 and 4 clock positions: click 2.3–3.5 N centre, ≤ +50 % rim, click travel 0.15–0.37, hard stop 0.37–0.43, no jam; **stroke stack validation:** measure G, L, tact H, skin thickness on each unit and compare to the step-12 table; confirm the 3-bin selection closes on ≥ 10 units. *If it does not:* S → 0.45 and 5 bins. Get Panasonic's allowable static load in writing and verify the over-travel force at the stop ≤ that number.
7. **Magnetics:** gaussmeter map at the IC plane with each race material and with the tact fitted (MT6701 200–1000 G `[V]`; AS5600L ≥ 30 mT on the 1 mm circle `[V]`; race delta ≤ 10 %; **latches Bpk ≥ 8 mT = ≥ 2× B_OP max**); MT6701 INL ≤ ± 1.5° / AS5600L ≤ ± 1° `[V]` on a reference encoder; **latch edge map: 8 edges/rev, max gap ≤ 80° at −10…+50 °C and across the 0.40 press**; CMM the concentricity chain on every unit and correlate to INL. *If INL fails with the 17-4 race:* zirconia/BeCu race. *If AS5600L field < 30 mT:* N42/N45 magnet or drop the variant.
8. **Sealing:** IPx7 (1 m, 30 min) on 5 units after the life test, then 48 h neutral salt fog (ISO 9227) with 100 turns/day: no water past the diaphragm (indicator paper), red rust on the 17-4 race noted (decides zirconia if the O-ring is deleted), torque change ≤ 20 %.
9. **ESD:** IEC 61000-4-2 8 kV contact to the crown and 15 kV air at the labyrinth: no tact/I²C upset, no latch-up; confirm by current probe that the discharge goes through the bleed leaf's 1 MΩ ∥ TVS (§3 C-4 path).
10. **Drop:** 1.5 m × 6 faces + 2 crown-end corners onto concrete: recess prevents impact; press curve unchanged; B map ± 5 %; ring/groove intact (X-ray or teardown of 1 unit).
11. **Yank:** 150 N axial pull on the crown for 10 s and 300 N on the lug: no displacement > 0.05, no crack in the ears; then full function.
12. **Permeability:** 5 serrated 316L crowns µr ≤ 1.05; the Ti control and one deliberately rolled-knurl 304 control bracket the INL result — the sensor INL with a cold-worked crown is measured, not argued. *Decision rule (§3 C-16): 316L INL worse than Ti by > 0.3° after the 24-point table → Ti Gr5.*
13. **Nickel release:** EN 12472 wear/corrosion then EN 1811 on 5 finished PVD'd crowns and 5 moulded-in lugs (post-life-rig units preferred): < 0.5 µg/cm²/week `[V?]`. *If fail:* Ti Gr2/Gr5 or hard-anodised Al crown; Ti lug.
14. **Ferromagnetic debris:** 50 mg steel filings at the crown rim, 200k indexes: torque change ≤ 20 %, no jam, no filings past the skirt journal (teardown).
15. **Acoustics:** detent click SPL at 10 cm (ID sets the limit) and the doc's 170 Hz LRA test in the same box, with and without cell contact (§7).
16. **Click separation** (doc's item): 8/12/15/20 detents/s with active braking on the ~48 g mass; ≥ 12/s resolvable.

**Gate to EVM-1 (crown):** chosen geometry; torque, 100k decay, press stack closure, seal-drag decision (O-ring in or out), INL, latch edge map and concentricity numbers met on ≥ 3 units; race material chosen from the field map; grease mass, leaf preload and pip bin specified as manufacturing limits; nickel-release and yank results in hand; the §9.11 1M rig started on the chosen variant; collar/bore/lug interface frozen for §7.

### 4.6 Suppliers / process types and cost (all costs `[U]` — no quotes exist; roll-ups are estimates, not verdicts)

| Item | Process / supplier type | NRE | Unit @1k / @10k | Lead | Second source |
|---|---|---|---|---|---|
| Crown+hub, 316L, turned incl. pocket & groove | Swiss-type turn-mill, ≥ 16 mm bar (watch-case / medical small-parts class; Dongguan, Jura, Taiwan) | $2–4k fixtures + FAI | $5.0 / $2.8 | 4–6 wk | any Swiss shop; Ti Gr5 +$3.0 |
| **Cut serrations (48 passes)** | live tooling on the same machine, or gear-shaper/hobbing secondary at volume | $1k cutter/fixture | $2.0 / $0.8 | — | rolled knurl NOT allowed |
| PVD DLC/ZrN + bore masking | job-shop PVD (watch-finish class) | $1–2k fixture/plugs | $1.0 / $0.55 | 2 wk | Type III anodise (Al) $0.6 |
| Race ring, wrought 17-4PH: turn + H900 + **wire-EDM grooves + lap + passivate** | Swiss turn + heat-treater + wire-EDM shop | $3k EDM program/fixture | $4.5 / $2.2 | 6 wk | MIM $0.8/$0.35 only if a lot measures ≥ 40 HRC ($8–15k tool); zirconia CIM ring $3.0 ($10k tool); BeCu TH04 ring ~$3.5 |
| Si₃N₄ balls ø0.8 G5/G10 | ceramic-ball specialist | — | 2 × $0.08 / $0.04 | stock | 3+ vendors |
| BeCu leaves (etched, formed, aged) + bleed leaf | photo-etch/spring house; progressive die at volume | $1.5k art; $8k die | 2 × $0.10 + $0.08 / $0.05 | 3–4 wk | phosphor bronze not viable (0.61 GPa) |
| BeCu C-ring ø0.40 + wave washer | spring house / stamper | $1.5k | $0.12 + $0.15 / $0.06 + $0.08 | 4 wk | 316 washer only if µr measured |
| Magnet ø6 × 2.5 diametric N35–N42 (N42 for AS5600L) | catalogue (Bomatec, HKCM, Chinese N-grade) | — | $0.15 / $0.08 | stock | many |
| POM-C sleeve (moulded + one-chucking secondary) | injection moulder + turning secondary | $6–10k tool | $1.2 / $0.55 | 8–12 wk | machined POM at proto ($8) |
| LSR diaphragm over PEEK pip, 3 bins | LSR moulder with insert loading | $12–20k tool (3 cav.) | $0.9 / $0.5 | 10–12 wk | loose LSR disc + machined pip at proto |
| FKM O-ring 1.0 section (optional) + J5 face seal | catalogue (Parker/Trelleborg/Asian) | — | $0.05 + $0.05 | stock | delete |
| PFPE grease | Krytox GPL 205-class | — | $0.02 | stock | — |
| Satellite PCB 22 × 10 × 0.6 + assembly, 2 variants | any PCBA house | ~$300 (doc §4.5) | $0.4 + $1.0 | 2–3 wk | — |
| MT6701QT-STD / AS5600L-AWLM | LCSC/CN distribution; Infineon (ex-ams) distribution | — | $1.5 (doc) | doc §4.5 | each other |
| 2 × DRV5032DU (X2SON, both outputs used) | TI, dual-distributed | — | 2 × $0.35 | stock | DRV5032DG (80 Hz, 3.4 mT) |
| EVPBB2A9B000 tact | Panasonic, 10k MOQ reel `[V]` | — | $0.15 | stock | EVPBB1AAB000 (1.0 N/0.08) |
| 10-way flex tail (hot-bar) or FH12-10S-0.5SH | FPC vendor / Hirose | $500 | $0.40 / $0.22 | 2–3 wk | Molex/TE 0.5 mm |
| Keyring lug 316L + Dyneema interposer | stamped/MIM lug; cordage vendor | $2k | $0.25 + $0.20 | 6 wk | Ti lug if EN 1811 fails |
| Assembly labour (5 stations + selective pairing, ~5 min) | CM with watch/wearable experience | $20–30k fixtures + life rig ($4k, doc) + tact-height gauge | $2.5 / $1.5 | — | — |
| Compliance testing | EN 12472 + EN 1811 (accredited lab), ISO 9227, IEC 61000-4-2 | $3–5k | — | 4–6 wk | — |

**Crown-end mechanical roll-up `[U]`:** ≈ **$16–18 @1k, ≈ $9–10 @10k** (the doc's $9.50 line and the draft's $12–13 both omitted the 48-pass serration and race hard-finishing; §7's $10.50 line likewise). Satellite PCB + sensors + tact ≈ $3.6. **NRE for the crown end ≈ $60–85k** `[U]` including tooling, fixtures, life rig, Mule C, compliance tests; excluding the nRF/RF programme.

**Single points of failure:** MT6701 distribution (doc §4.5 hedge stands; AS5600L is now Infineon-owned — check lifecycle); the LSR-over-PEEK tool (hold a loose-disc + machined-pip bridge); wire-EDM shop capacity at volume (bridge: broach-then-age; long-term: zirconia CIM).

### 4.7 Risks, ranked by kill-probability × irrecoverability

1. **Press stroke stack (high, recoverable, now quantified).** EVPBB H ± 0.1 `[V]` vs a 0.40 stroke: RSS closes (click 0.18–0.36 vs stop 0.37–0.43), arithmetic does not; over-travel force at the stop up to 8 N against an unknown allowable static load. Mitigation: stroke 0.40, 3-bin selective pip, compliant pip, 100 % EOL press curve. **Test:** Mule C item 6 on ≥ 10 units + Panasonic's written load limit; fallback S 0.45 / 5 bins / 18 N/mm pip.
2. **Detent life / brinelling (high, recoverable).** Land contact 2.1 GPa vs wrought H900 shakedown ≈ 1.9 GPa — marginal; MIM would ratchet. **Test:** 100k (Mule C) then 1M rig with torque logging + optical wear; ≤ 15 % / ≤ 5 µm. Fallbacks: F_n 0.35 + steeper α, ø0.9 balls, zirconia ring.
3. **Rotary O-ring drag / spiral failure (medium-high, cheap to settle).** Computed 0.15–0.35 mN·m running, 0.6–1.4 breakaway `[U]` — up to half a detent; combined rotary + reciprocating duty is Parker's §10.4 case `[V]`; cold stiffening near −20 °C (§7). **Test:** Mule C item 4 with/without, dwell breakaway at 40 °C and −20 °C; ring inspection after the life test. Fallback: delete the O-ring + zirconia race (wet-tolerant mechanism).
4. **Concentricity chain (medium-high; cheap now, expensive later).** 0.28 worst-case vs 0.30 (MT6701) / 0.25 (AS5600L). **Test:** CMM every Mule C unit, correlate to INL; measure die-to-package on 10 samples. Fallback: tighter bore clearance, package-body nest, drop the AS5600L variant.
5. **Race hard finishing (medium).** Wire-EDM after H900 is the only route that holds the (relaxed) profile; recast removal and residual magnetisation are process risks. **Test:** M-11 race QC + ripple uniformity ≤ 15 % on Mule C; demagnetised-state check before assembly.
6. **First-motion detection (medium — now a hard requirement since the AMOLED sleeps).** Both DU outputs on 2 devices give ≤ 77° worst-case gap; Bpk at r 4.0 must be ≥ 4.5–8 mT. **Test:** latch edge map over B_OP spread (3 device lots), temperature and press; EOL "4 outputs × 2 toggles/rev, gap ≤ 80°".
7. **Rim-push press-force dependence (medium).** +28 % predicted. **Test:** Mule C item 6; ≤ +50 %. Fallback: PTFE-filled POM lands, 1 mm longer rear land from the spare.
8. **Nickel release from the 316L crown/lug (medium, regulatory).** PVD wear at serration flanks (EN 12472) is the exposure. **Test:** Verification 13. Fallback: Ti or anodised Al.
9. **Race ferromagnetism distorting the field (medium).** Coaxial and co-rotating → expected benign; the stainless tact dome at r 3.3 is a new static distorter; §7 flags field-amplitude loss at the latches. **Test:** gaussmeter map + INL with each race and the tact; ≥ 2× B_OP margin; 24-point EOL table absorbs static residuals. Fallback: zirconia/BeCu race, tact at r 4.0 with a larger hub collar (costs the AS5600L displacement margin).
10. **Lint, dust and steel filings in the race (medium, slow).** **Test:** talc + steel-filings runs (Verification 3/14). Fallback: felt wiper in the chamber, dry-film lube, deeper skirt-journal overlap.
11. **Debris chamber / bulkhead wall on the 15 mm faces (medium, design-time).** Amended to wide-face arcs; 0.70 wall remains thin for a moulded PC/ABS bulkhead under a corner drop. **Test:** drop item 10 with crown-end corners; mould-flow on the tray.
12. **Coast expectation in the product story (low engineering, high expectation).** Cannot coast (threshold 9.7 rev/s). **Test:** high-speed video; fix §7.1 and marketing copy.
13. **Crown yank / retention ring (low-medium).** BeCu ring in POM groove, ears in shear — all `[U]` numbers (ears now 6.0 wide). **Test:** Verification 11 (150 N / 300 N).
14. **Magnetic key fobs tripping latches (low, power).** 3.9 mT max B_OP `[V]`. Mitigation: MT6701 confirmation before radio wake. **Test:** 50 mT fob at 20 mm for 24 h: added drain ≤ 0.5 mAh/day.
15. **Cold-work permeability of the crown lot (low with cut serrations).** **Test:** M-4 gate; Mule C item 12 with Ti and 304 controls.
16. **ESD to a floating crown (low-medium; path changed by §3 C-4).** Path is via the bleed leaf's 1 MΩ ∥ TVS by design; leaf wear over 1M indexes is new. **Test:** Verification 9 with a current probe; continuity after the life rig.
17. **AS5600L field margin at 1.7 mm and Infineon lifecycle (low-medium).** **Test:** Bz map (≥ 30 mT `[V]`); lifecycle statement from distribution.
18. **Detent acoustics (unknown).** **Test:** SPL at 10 cm; ID sets the limit.
19. **LSR-to-PEEK pip adhesion (low).** Mechanical through-hole lock specified. **Test:** 300k presses, pip pull 5 N.

### 4.8 Open questions (crown)

1. Coaxial vs transverse: Mule C blind test (10 hands) — the collar tool, satellite PCB shape and sensor variant wait on it; the tray tool does not (§7 Step 12).
2. Press stroke 0.40 mm (vs the doc's 0.25): ID sign-off needed. The 0.25 figure cannot be built with a 0.11-travel tact at H ± 0.1 (Panasonic EVPBB DS) — settle by Mule C item 6; if 0.40 is rejected, the tact class must change (no 0.5 mm-tall tact travels more than 0.11).
3. Panasonic EVPBB allowable static/over-travel load and travel tolerance — not on the datasheet page read; the over-travel force at the hard stop (≤ 8 N worst-case) depends on it. Get the delivery specification in writing.
4. Is the doc's "crown + hub + bulkhead translate as a rigid unit on a 12 mm POM journal" a hard requirement or a sketch? This report's one-piece crown+hub on a 6.9 mm two-land journal (0.8° tilt) with a static diaphragm needs the architect's sign-off (§7 agrees on 0.8°).
5. Rotary O-ring: keep or delete. Computed drag 0.15–0.35 mN·m running / 0.6–1.4 breakaway `[U]` — Mule C item 4 measures with/without at 40 °C and −20 °C; deletion implies a zirconia race for a wet-tolerant mechanism.
6. Does the product story accept "no coast" — §7.1's "coasts a third of a turn" cannot be met (threshold 9.7 rev/s on 1.25e-7 kg·m²).
7. 17-4PH H900 heat-treat schedule (482 °C / 1 h) and post-EDM recast removal depth: ASTM A564 / AMS 5643 / MPIF 35 texts not opened — only two supplier sheets were read. Confirm with the heat-treater and the EDM shop.
8. MIM race viability: MPIF-35 typical H900 33 HRC `[V?]` fails the ≥ 40 HRC gate; only a measured MIM lot can reinstate it.
9. Race magnetics: FEMM run with each candidate ring AND the stainless tact dome at r 3.3 — flux shunting, INL contribution, field at the latches — before committing to a race and to the tact radius (§3 C-1).
10. MT6701 die-centre-to-package tolerance (assumed 0.10 mm) — MagnTek do not publish it; measure on 10 samples on a micrometer stage. The 0.28 mm chain has only 0.02 of margin.
11. AS5600L variant: Bz at 1.7 mm from a ø6 × 2.5 N42 diametric on the 1 mm circle (needs ≥ 30 mT `[V]`) — FEMM + gaussmeter; and the Infineon lifecycle statement for AS5600L-AWLM.
12. Flex: confirm 10 signals (+ bleed pad) and whether the tail is hot-bar soldered or an FH12-10S-0.5SH (the -10S size was not read in the local FH12 extract); closure of the 3.0 mm main-board strip (§3 C-12).
13. Wave washer and C-ring: BeCu stamped/wire parts with the stated force–height curve (0.55 N at 0.65, ≤ 1.5 N at 0.25) and ring free OD ≈ 7.8 — spring house to confirm.
14. BeCu C17200 HT properties were read from a MatWeb/lookpolymers mirror of the Materion sheet (YS 1130–1420 MPa, age 2 h @ 315 °C) — open the Materion datasheet before the leaf drawing is released.
15. LSR-to-PEEK pip bond: self-bonding LSR grades do not bond to PEEK without primer — mechanical through-hole lock specified; moulder to confirm, or switch the pip core to PBT/LCP.
16. REACH Annex XVII entry 27 / EN 1811:2023 / EN 12472 — limits read from secondary sources; obtain the standards and confirm the wear-then-release sequence and the "prolonged contact" classification for a keychain crown.
17. Debris chamber amendment to §6.4 (wide-face arcs only, 0.70 wall on the 15 mm faces) needs the bulkhead mould-flow and drop analysis; the buried electrode routing must be checked against the pockets.
18. Permeability spec method: ASTM A342 not opened; confirm the indicator method and the 1.05 acceptance with the RF/sensor owners.
19. Crown yank ≥ 100 N design / 150 N test and lug 150 N / 300 N — no standard cited; agree the numbers with ID/QA.
20. Detent acoustic level target — ID decision needed before Mule C reports.
21. Does the AMOLED decision (screen sleeps) make the ≤ 90° first-motion detection a hard spec? This report treats it as one; confirm with the product owner.
22. Mule B input: crown material (316L vs Ti vs Al), floating status with a 1 MΩ bleed, and ~5–10 pF coupling to the buried electrode go into the antenna EM model — confirm the RF owner has received them (§3 C-21).
23. *(new, §3 C-4)* ESD bleed leaf: contact force, wear over 1M indexes, and whether a moulded-in leaf in the POM sleeve is acceptable to the moulder; TVS part class on the satellite PCB.

---

## 5. End-cap antenna & RF front end — domain report

*Frame: body X. Editor notes in italics mark §3 resolutions — chiefly C-5 (PCB substrate ends at X = 68.0, finger at X = 65.5–67.5, tab to 65.5 through a sealed aperture in the full ring web), C-8/C-9 (cell 19–62, LRA 52–60) and C-4 (crown floating with a 1 MΩ bleed).*

### 5.1 Reviewer dispositions (every finding, accepted or rebutted with the source opened)

| # | Finding | Disposition |
|---|---|---|
| F1 | Feed finger compressed along x (blocking) | **Accepted.** Feed redrawn: L-shaped cap tab whose underside land is parallel to the PCB top surface, standard vertical-deflection (z) SMT finger; stack rebuilt in z with a named PCB datum. Step 6, M1, M7. |
| F2 | 100 % DC probe on an anodised cap cannot read; M12 path blocked by the series high-band C | **Accepted.** Production feed test is now an S11 signature through the RF switch connector; DC test pad moved to the antenna-side node. M12, M13, M14. |
| F3 | Chu arithmetic does not reproduce (ka = 0.636 is an 84 mm sphere; 12.9 % is the VSWR 2:1 figure) | **Accepted, recomputed per structure below.** Doc §6.3 line 468 needs the same correction. |
| F4 | Five items collide on the same top-side strip at x ≈ 59–63; 0.7 mm height budget is the battery-column figure | **Accepted.** Width-wise floor plan added (Step 11b). Murata MM8130-2600 mounted height **1.4 ± 0.1 mm, 2.5 × 2.5 mm** `[V]` placed in the SiP column. |
| F5 | No radiated spurious / harmonic step; B12 H3 = 2097–2148 MHz lands in B4 DL and inside the high-band match | **Accepted.** New Step 10b and Phase 1 sweep item 9; EVM-1 V-9b pre-scan; two 0402 footprints reserved for a trap. FCC §27.53 could not be opened → `[V?]`. |
| F6 | "Brush electroless" does not exist; low-P Type II is the wrong barrier class; 2–2.5 µm is below ASTM B733 SC1 | **Accepted.** Route A rewritten as masked immersion EN Type IV/V ≥ 5 µm (SC1) + Au per ASTM B488, or brush *electrolytic* Ni + Au; Route C (plated insert) promoted to co-baseline. SC classes confirmed only in secondary summaries → `[V?]`. |
| F7 | "Expected SAR is low" is unsupported | **Accepted, deleted.** SAR `[U]`; EVM-1 SAR pre-scan; PC3/PC5 made contingent on it. |
| F8 | 500 h 85/85 on sealed units with Li-Po cells | **Accepted.** V-18 now on RF-representative units with foil-block dummy cells, or 60 °C/90 % RH on real units; cell-vendor storage limit check added. |
| F9 | Finger compression percentages/stack arithmetic wrong | **Accepted.** One free height, worst-case stack, PCB z-datum named. |
| F10 | ± 2.0 dB production window eats the whole certification margin | **Accepted.** Asymmetric −1.0/+2.0 dB vs golden with ≤ 0.3 dB box repeatability; 3 dB-margin alternative targets given. |
| F11 | TX blanking should use COEX0 / %XCOEX0 | **Accepted with a correction from the primary source.** nRF91 AT Commands Reference v1.9 §6.1: COEX0 is driven from the modem's **RF frequency range** — "the modem applies the COEX0 state corresponding to the RF frequency range automatically during runtime… When RF is turned off, the given COEX0 state is inverted." It is therefore an **RF-active-in-band indicator (RX and TX), not a TX-only PA strobe**. Acceptable and conservative for a capacitive-sensor blank. Example syntax `AT%XCOEX0=3,1,1570,1580,1,2000,2180,1,600,800` `[V]`. Identical semantics on nRF91x1 firmware `[V?]`. Step 13. |
| F12 | Compelma / Coilcraft page / Armoloy tags are secondary | **Accepted.** Retagged `[U]` / `[V?]` throughout. |
| F13 | ISED RSS-132 wrong for B2; EN 62479 wrong for 200 mW | **Accepted.** RSS-130/-133/-139 (+RSS-Gen); EN 50566 with EN IEC 62209-1528. Both `[V?]`. |
| F14 | Ring is an annulus; no bore | **Accepted.** Ring defined as a capsule-outline annulus; the cap tab passes through the centre. *[Editor, §3 C-5: the mechanical domain requires a full web for sealing and the light path; the tab passes through a sealed aperture in the web; the EM model must include the web.]* |
| F15 | Crown at E-max, doc says current max | **Accepted; explicit doc correction recorded** (Step 3, open questions). |
| F16 | Feed current is 0.13–0.20 A rms, not < 0.1 A | **Accepted.** I = √(P/Ra) = √(0.2/5…12) = 0.20…0.13 A rms; loss in 50 mΩ ≈ 0.8–2 mW ≤ 0.05 dB. |
| F17 | 12–15 % "one structural iteration" branch deviates from the doc's binary §10 rule | **Accepted; stated as a proposed amendment to §10 requiring sign-off.** |
| F18 | Topology A as written passes neither band | **Accepted.** Circuit drawn with reactances at 722 and 1900 MHz (Step 10.3). |
| F19 | Anodise "fine" at 280 °C untagged; pins on the cap; nitrogen reflow | **Accepted.** `[U]` + crazing trial; holes in cap/pins on ring; nitrogen note deleted. |
| F20 | MM8130 height vs the wrong budget | **Accepted.** Height now `[V]` 1.4 ± 0.1 mm; placed in the SiP column, not under the display. |
| Missing steps (14) | | **All added**: Step 1b (3GPP tables), Step 6 (feed geometry decision + datum), Step 10b (harmonics), Step 11b (floor plan), Step 15 (SAR tied to power class; ESD test method for coated parts), M4 (EN to standard; bare-Al annulus definition), M5 (RoHS seal/desmut; per-lot conductivity), V-5b (cable-independent option), V-13 (ring εr(T)/moisture, cell swell), open questions (doc corrections). |

### 5.2 What this subsystem is

The 22.5 mm machined 6061-T6 end cap is **not an antenna on its own**. It is a *coupling element* that excites the fundamental dipole-like current mode of the whole 95 mm capsule (cap + 1.5 mm optical-PC ring + 23 × 52 mm six-layer PCB ground + everything conductive attached to it). At 722 MHz the capsule is 0.23 λ long (λ = 415 mm); the cap is a capacitive top-load at one end, the PCB ground is the counterpoise, and the 8 mm copper keepout plus the ring form the gap across which the RF voltage appears. A single vertical-deflection spring finger on the PCB feeds RF onto a plated land on an L-shaped tab of the cap, through a 5-element 0402 high-Q dual-resonant match, from the nRF9151's single 50 Ω ANT port `[V, nRF9151 PS front matter]`. The polymer ring the antenna *requires* for isolation doubles as the RGB halo light guide.

Coaxial crown is baseline (§9.4/§10 leave it open pending Mule C); Step 11 states what changes if the transverse-stroke crown wins. The 2026-09-19 display decision (AMOLED RM69310, TPS65631-class PMIC, 6.0 mm baseline cell per §3 C-7) is carried into the RF model.

### 5.3 The numbers that govern it

| # | Quantity | Value | Tag / source |
|---|---|---|---|
| 1 | AT&T SFF LTE-M TRP gate, B12 | **+10.0 dBm at PC3 / +7.0 dBm at PC5**; TIS −85 dBm | `[V]` AT&T IoT Radiated Performance Requirements v1.8 Table 4 (local att_trp.txt) and v2.1 (07/2025) Table 4 (fetched PDF) — unchanged |
| 2 | AT&T SFF TRP gate, B2 and B4 | **+12.0 dBm at PC3 / +9.0 dBm at PC5**; TIS −88 / −90 dBm | `[V]` same |
| 3 | Small Form Factor | longest dimension **< 107 mm**, free-space test; Note 6 (v2.1): LTE-M *wearable* devices use the SFF free-space limits but are tested on the **body phantom** (or wrist phantom) | `[V]` v2.1 Notes 5–6 — keychain classification is an open question for AT&T's Partner Coordinator |
| 4 | Mandatory bands | B2, B4, B12 for all IoT LTE devices; B17 requirement removed in v2.1 | `[V]` v2.1 |
| 5 | nRF9151 | PC3 23 dBm / PC5 20 dBm; single 50 Ω antenna interface; Cat-M1 sensitivity −108 dBm low band; B2/B4/B12/B13 in hardware | `[V]` nRF9151 PS v1.0 front matter (local, 116 lines; full electrical chapters not opened) |
| 6 | Conducted design power | 21.5 dBm (23 − ~1.5 dB) | `[V?]` 3GPP TS 36.101 Table 6.2.2-1 (PC3 ± 2 dB, ΔTC 1.5 dB band-edge relaxation), Table 6.2.3-1 (MPR), Table 6.2.4-1 (A-MPR, NS_06 class for B12) — **none opened**; measure the modem's actual applied MPR/A-MPR on EVM-1 (V-9) |
| 7 | Required total efficiency, B12 | **12.3 % (−9.1 dB) binding** (doc); arithmetic with 2.0 dB margin gives −9.5 dB → 11.2 %. **Design target 15 % (−8.2 dB).** | `[U]` derived |
| 8 | Required total efficiency, B2/B4 | **17.8 % (−7.5 dB)** at PC3 with the same 2.0 dB margin; the high-band gate is tighter in efficiency than B12 | `[U]` derived — unbudgeted in the corpus |
| 9 | Honest estimate, 22.5 mm cap on 23 × 52–55 mm ground, loaded | **8–18 %, centred ~12 %** at B12; 20–40 % at B2/B4 | `[U]` doc; cross-check: Ignion low-band efficiency 54.3 % → 12.2 % as ground length falls 120 → 40 mm at 824 MHz on a 60 mm-wide board `[V, AN_NN02-224_LengthClearance Table 4]` |
| 10 | Match loss, 5 × 0402 high-Q into Ra ≈ 5–12 Ω, Xa ≈ −j120…−j250 Ω | 2.0–2.8 dB (η_match = 1/(1+Q_net/Q_comp), Q_net 20–40, Q_comp 45–60) | `[U]` doc; Q_comp at 700 MHz for 0402 wirewound inductors is **not** established — Coilcraft's "Q up to 160 at 2.4 GHz" is a product-page headline `[U]`; the datasheet Q-vs-f curve at 700 MHz must be opened |
| 11 | Chu bound (bandwidth only) — **recomputed** | Whole capsule: enclosing-sphere radius a = √(47.5² + 13.5² + 7.5²) = 49.9 mm → ka = 0.755, Q_min = 1/(ka)³ + 1/ka = 3.65. Bare 23 × 55 board: a = 29.8 mm → ka = 0.451, Q_min = 13.1. FBW(VSWR s) = (s−1)/(Q√s). Bare board at 2–3 × Q_min (26–39): 13–20 MHz at 2:1, 21–32 MHz at 3:1 — **against B12's 47 MHz span**. Whole capsule at 2–3 × Q_min (7.3–11): 53–81 MHz at 2:1, 76–114 MHz at 3:1. The doc's ka = 0.636 / Q_min = 5.46 / FBW 12.9 % describes an a = 42 mm sphere at VSWR 2:1, neither structure. | `[U]` arithmetic, Chu/McLean; the conclusion (no single low-band resonance on the bare board; the cap + dual-resonant match are needed) survives and is stronger |
| 12 | Keyring / hand loading | 120 g steel key bundle without the 28 mm Dyneema interposer: 4–10 dB; hand on the crown end: 3–8 dB | `[U]` — Mule B settles both |
| 13 | Plan B (polymer cap + Ignion NN03-310 lengthwise, ~105 mm) | NN03-310 30.0 × 3.0 × 1.0 mm; LTE 698–960 & 1710–2690 MHz; on Ignion's smallest published board (38 × 50 mm) total efficiency **8.4 % at 698 MHz, 14.0 % avg low band** | `[V, UM_NN03-310 Tables 1/3; AN_NN03-310_EB_size Table 1]` — Plan B is not a guaranteed pass either |
| 14 | Keepout | zero ground/signal copper on all 6 layers for the last 5 mm of PCB substrate (copper ends X = 63.0; substrate X = 68.0 per §3 C-5; the single feed trace + finger pad + TVS pads excepted); no cell within 10 mm of the ring; no metal fastener / LRA can / display tail / steel keyring in the cap volume or the buffer | `[U]` doc §6.3 — the doc's own §6.2 layout violates it |
| 15 | Feed-land plating | masked immersion electroless Ni-P **Type IV/V, ≥ 5 µm (ASTM B733 SC1)** + Au per ASTM B488 on bare 6061, or a press-fit plated insert; anodise elsewhere | `[V?]` B733 types/SC classes from secondary summaries; galvanic gap Au-to-6061 ≈ 0.9–1.0 V in seawater (Au ≈ +0.2 V, 6061 ≈ −0.75 V vs SCE) `[V?]` — the doc's "~1.5 V" is high; conclusion unchanged |
| 16 | Spring finger | BeCu 0.08–0.10 mm strip, Ni underplate + Au, 10–30 % recommended / 40 % max compression, > 300 k cycles, "a few mΩ" | `[U]` (distributor guide, retagged); force ≥ 0.5 N nominal, ≥ 0.3 N at minimum compression `[U]` until the chosen part's force-deflection curve is opened |
| 17 | Feed current at 23 dBm | I = √(P/Ra) = **0.13–0.20 A rms** (0.28 A peak) for Ra = 5–12 Ω; 50 mΩ contact ≈ 0.8–2 mW ≈ 0.02–0.05 dB | `[U]` arithmetic |
| 18 | RF switch connector | Murata MM8130-2600: 2.5 × 2.5 mm, mounted height **1.4 ± 0.1 mm**, Ø2.1 probe bore | `[V, Murata product-search datasheet, opened]`; insertion loss / VSWR not on that sheet → `[U]` (~0.2–0.3 dB) |
| 19 | Production RF test driver | nRF91 `%XRFTEST` TX: band, frequency in 100 kHz (6000–22000), power +23…−50 dBm, LTE-M/NB-IoT, QPSK/16QAM/CW, RB count/start, burst mode; RX: returns measured antenna-port power (−127…−25 dBm); both lockable by `%XPRODDONE` | `[V, nRF91 AT Commands Reference v1.9 §11.2–11.3]` for nRF9160; `[V?]` for the nRF91x1 guide (not opened) |

### 5.4 Why the cap + ground is the radiator (and why Chu is only a bandwidth bound)

- **Radiation resistance.** For a structure of length L ≪ λ, Rr ∝ (L/λ)². For the 95 mm capsule at 722 MHz (0.23 λ) a triangular-current estimate gives Rr ≈ 20π²(L/λ)² ≈ 10 Ω; capacitive top-loading by the cap flattens the current distribution and raises this toward 15–25 Ω `[U]`. An 86 mm body sits at ~2/3 of that. That is the only legitimate argument for length and for a metal cap: **more radiation resistance against the same loss resistance**, and a current distribution that uses the full capsule rather than an 8 mm trace.
- **Loss.** Aluminium is essentially lossless (skin depth ≈ 3 µm at 722 MHz; 6061-T6 σ ≈ 2.5 × 10⁷ S/m ≈ 43 % IACS `[V?]` handbook value, ASM; a ± 10 % lot spread changes a < 0.05 dB term by < 0.005 dB — negligible, declared with a number). Loss lives in (a) the matching network (2–2.8 dB, dominant), (b) dielectric loss in FR4 and the ring at the high-E gap, (c) eddy/dielectric loss in the Al-laminate cell, steel LRA can, crown, AMOLED cathode, (d) the hand. η = Rr / (Rr + R_loss).
- **Chu.** Bounds *bandwidth/Q*, never efficiency (a small antenna can be 100 % efficient if narrow; adding loss widens the band). Recomputed per structure in row 11: on the bare board a single B12 resonance is 2–3× too narrow; on the whole loaded capsule it is achievable — which is exactly why the cap, the gap and a dual-resonant match exist.

### 5.5 Decisions since the doc, folded in

- **AMOLED replaces MIP.** The RM69310 cathode/backplane (~11 × 26 mm) is a new floating conductor in the EM model; the TPS65631-class PMIC (boost + negative charge pump, ~1–2 MHz `[U]`) is a **TIS desense risk** (Step 14). Display length 30.94 mm `[V?]` vs 34.84 mm returns ~4 mm of board to the LRA/keepout side.
- **Cell:** 6.0 mm baseline (§3 C-7), 6.5 mm modelled as the RF-gated option; the keepout rule forces the cell to end at X ≤ 61–62.
- **Crown geometry open.** Coaxial baseline. If transverse wins: crown zone −3 mm; give the 3 mm to the keepout buffer, not to body length (Step 11).
- **Doc corrections carried by this report:** (i) crown/lug sit at the **E-field (voltage) maximum**, not the current maximum (§6.3 line 472); (ii) Au-to-6061 galvanic gap ≈ 0.9–1.0 V, not ~1.5 V (§4.3); (iii) §6.2 layout vs §6.3 keepout conflict; (iv) §6.3 Chu line (ka = 0.636) is inconsistent with either structure.

### 5.6 DESIGN — step by step

#### Phase 0 — Fix the requirements before any geometry (week 0–1)

**Step 1. RF requirement sheet from primary documents, with the classification question asked.**
- Bands: B12 UL 699–716 / DL 729–746; B2 UL 1850–1910 / DL 1930–1990; B4 UL 1710–1755 / DL 2110–2155 (3GPP TS 36.101 Table 5.5-1 `[V?]`, not opened). Decide now whether **B13** (UL 777–787) and **B5** (824–849) are in the first SKU: B13 widens the low-band UL span from 17 to 88 MHz and changes the match; B5 adds FCC Part 22 / RSS-132. Recommendation: **AT&T-only SKU (B2/B4/B12)** for the first certification; B13/B5 disabled in the modem band mask and declared disabled on the PTCRB/AT&T paperwork (v2.1 permits `[V]`).
- Gates `[V]` v1.8/v2.1 Table 4: B12 TRP ≥ +10.0 dBm PC3 (+7.0 PC5), TIS ≤ −85; B2/B4 TRP ≥ +12.0 (+9.0), TIS ≤ −88/−90.
- **Written question to AT&T's Partner Coordinator: is a pocket/keychain device "wearable" under Note 6 (body phantom) or free-space SFF?** `[U]` until answered.
- Power class: **PC3 provisionally** (doc §6.3 argument: 3 dB link margin reduces CE-mode repetitions, 157 mAh/week deep-coverage `[U]`). **Now contingent on the EVM-1 SAR pre-scan (Step 15.5):** PC5 lowers conducted power and the TRP gate by 3 dB together (Table 4 `[V]`) — efficiency gate identical, SAR halved. Confirm with Nordic whether power class is a certification-time or field-switchable setting `[U]`.

**Step 1b. Open the 3GPP tables behind the 21.5 dBm.** TS 36.101 Table 6.2.2-1 / 6.2.2E-1 (Cat-M1 PC3 23 dBm ± 2 dB; ΔTC = 1.5 dB relaxation for channels within 4 MHz of the band edge in listed bands), Table 6.2.3-1 (MPR by modulation/RB), Table 6.2.4-1 and the NS_06/NS_07 network-signalling A-MPR that applies to B12/B13/B17 — the doc's "band-edge MPR" is actually ΔTC + A-MPR. All `[V?]` until opened; **measured on EVM-1 V-9 as the modem's applied power per channel**.

**Step 2. Convert gates to efficiency targets per band, with the arithmetic.**
- B12: 10.0 + 2.0 − 21.5 = −9.5 dB → 11.2 %; doc's rounding 12.3 %. **Binding 12.3 %, target 15 %.**
- B2/B4: 12.0 + 2.0 − 21.5 = −7.5 dB → **17.8 %**. Target 25 %. SOW line item.
- If the production window (M14) is kept symmetric ± 2 dB the certification margin is consumed; **therefore either the asymmetric −1.0/+2.0 dB production limit (adopted, M14) or a 3 dB design margin**: B12 −8.5 dB → 14.1 % (15.5 % scaling the doc's figure), B2/B4 −6.5 dB → 22.4 %.
- TIS: −108 dBm `[V, PS]` − 9.1 dB = −98.9 dBm expected vs −85 required — not the gate **provided** self-noise (AMOLED PMIC, DRV2625, TPS62840, SPI edges) desenses ≤ 3 dB (Step 14).
- η_total = η_rad × (1 − |Γ|²) × η_match; each measured separately on Mule B so a miss is attributable.
- Mule B stop-line (doc §10, binding): **< 15 % bare → Plan B**. A proposed amendment for 12–15 % is in Verification (flagged as an amendment needing sign-off).

**Step 3. Radiating structure and reference plane.**
- Radiator = cap (22.5) + ring gap (1.5) + 5 mm bare substrate + 8 mm copper keepout + 47 mm of ground + all attached conductors (cell, LRA can, crown, satellite PCB, AMOLED cathode, pogo flex, 430 SS shim). ≈ 95 mm electrical length.
- **Feed reference plane** = finger tip on the cap land. All impedances de-embedded there.
- Current maximum mid-body (X ≈ 40–55); **E-field maxima at both ends**. The crown (X = 0–16) is at an E-max: a floating metal cylinder with a hand on it is a *capacitive load and absorber* — this is the mechanism behind the 4–10 dB key-bundle number, and it is why the interposer works. (**Correction to doc §6.3, which calls the crown "a floating parasitic at the counterpoise current maximum".**)

#### Phase 1 — EM simulation (weeks 1–4, parallel with Mule B machining)

**Step 4. Tool and model.**
- CST Studio Suite (time domain) or Ansys HFSS; Feko for the bare structure; openEMS for early scoping. Deliverables: native project + Touchstone S1P at the feed plane + a sensitivity table.
- Model contents, all mandatory from day one:
  1. Cap: 6061 as lossy metal (σ = 2.5 × 10⁷ S/m `[V?]`) or PEC (< 0.05 dB difference); include the L-shaped feed tab and land, inner web, ring-retention groove (M1).
  2. **Ring** as built (§3 C-5): capsule-outline optical-PC part with a **full 1.5 mm web**, radial skirts 0.8 mm thick into the tray end and the cap bore, the sealed tab aperture; εr ≈ 2.8–3.0, tan δ ≈ 0.006–0.010 `[U]` — measure a moulded coupon (split-post resonator).
  3. PCB: 6-layer 0.8 mm FR4 (εr 4.3, tan δ 0.02 `[U]`), ground on all layers ending at X = 63, single feed trace X = 63–65.5, finger pad X = 65.5–67.5, substrate to 68.0, match footprints as lumped ports.
  4. Cell: floating conductive box 23 × 43 × 6.0 (and 6.5) mm, 0.1 mm skin, X = 19–62 (and 24–67 for the Mule B comparison).
  5. LRA can: steel Ø8.0 × 4.05 mm at X = 52–60 (§3 C-9); bracket as polymer or, if metal, ending ≤ 61.
  6. Crown: Ø13 × 8 mm cylinder in a POM journal (εr 3.7), race ring (17-4PH / BeCu / zirconia variants), Ø6 × 2.5 magnet (σ ≈ 7 × 10⁵ S/m `[U]`), satellite PCB 22 × 10 mm, Hall latches; **grounded and floating (1 MΩ) variants**; the buried IQS211B electrode ring in the bulkhead wall.
  7. AMOLED: 0.5 mm glass (εr 6.5), cathode/backplane 11 × 26 mm PEC sheet, FPC toward the crown end.
  8. Lens 0.5 mm + OCA; PC/ABS shell 1.2 mm; 430 SS shim 0.3 mm at X ≈ 33–45; pogo flex.
  9. IQS211B electrode (conductor + near-field probe point).
  10. Keyring lug (SS, tray flank, X = 8–14), 28 mm non-conductive interposer, key-bundle proxy 60 × 30 × 8 mm steel block `[U]`.
  11. Hand: homogeneous tissue (εr ≈ 30–40, σ ≈ 0.7–0.9 S/m at 700 MHz `[U]`; use the CTIA hand-phantom material values from the lab) in three grips (pinch at crown, palm mid-body, pocket = 5 mm from a 200 × 200 × 50 mm slab); flat body phantom at 10 mm.
- Ports: lumped 50 Ω between the finger pad and the cap land (finger as a 0.1 mm strip); second port at the ANT pad for co-simulation.

**Step 5. Sweeps** (record Z_in 600–2300 MHz, η_rad, Q_ant by Yaghjian–Best, achievable η_total after ideal-then-realistic match):
1. Cap length 18 → 26 mm.
2. Ring gap 1.0 → 2.5 mm (expect a broad optimum 1.5–2.0 `[U]`).
3. Keepout 6 → 12 mm.
4. Feed tab lateral position: centred vs offset toward a 27 mm edge (second-resonance lever `[U]`); **tab length 5 → 8 mm** (§3 C-5).
5. Feed trace width 0.8 → 2.5 mm and layer.
6. Cell end X = 55 → 65 and thickness 6.0/6.5; LRA position; **PCB with and without the 8.4 mm LRA slot at X = 52–60** (§3 C-7).
7. Crown grounded/floating; hand grips; keys ± interposer; body phantom.
8. Optional 1 mm laser slit in the cap (8–12 mm) for the high band.
9. **Harmonic radiation:** η_total at 1398–1432 MHz (B12 H2) and 2097–2148 MHz (B12 H3, inside B4 DL and the high-band passband) and 3.4–3.9 GHz (B2/B4 H2) driven through the B12-tuned match — this is the input to Step 10b.
- Output: a design point predicting ≥ 18 % B12 / ≥ 28 % B2/B4 bare (simulation flatters by 2–3 dB at low band `[U]`), a dB-per-mm sensitivity table signed by mechanical, and the harmonic efficiency table.

#### Phase 2 — Feed design (weeks 2–5)

**Step 6. Feed geometry decision, finger class, datum, stack.**
- **Geometry (decided): vertical-deflection finger, z-axis compression.** The cap carries an **L-shaped feed tab**: from the inner web it passes through the sealed aperture in the ring web (X = 72.5 → 71) and continues −X over the PCB edge to **X = 65.5** (§3 C-5), i.e. it overhangs the last 2.5 mm of the PCB substrate. Its **underside is a flat land parallel to the PCB top surface** at z = +1.4 mm nominal above the PCB top. The SMT finger at X ≈ 65.5–67.5 (top side) deflects in z against it — the load case every catalogue finger is rated for; drop loads on the cap are carried by the cap's lip on the shell, never by the finger; ± 0.3 mm of x-float only wipes the tip along the land. Alternative (b), a named side-actuation/edge-mount contact with its own curve, is kept only as a fallback if the tab cannot be machined (it can — M1).
- Part class: SMT BeCu spring finger, 0.08–0.10 mm strip, Ni underplate + hard Au, reel-packed `[U]`; candidates Harwin S17xx, TE, Würth WE-SPF, Kinsun/Amphenol — **MPN `[U]`; select against the stack below and the vendor's force-vs-deflection curve, which must be opened.**
- **One free height: 2.0 mm** (choose the part to it). Nominal compression 0.6 mm (30 %).
- **PCB datum:** the PCB's z-position is set by seating on the front-shell ribs (datum Z1); the cap seats on the shell's end shoulder (datum Z2); the land height is machined from the cap's seating face. Stack (z), worst case, all `[U]` until drawing values exist: PCB seat in shell ± 0.10; PCB thickness ± 0.08; cap-to-shell seat ± 0.05; land height on cap ± 0.05; finger free height ± 0.10 → **worst case ± 0.38 mm (RSS ± 0.18)** → compression 0.22–0.98 mm worst case (11–49 %), 0.42–0.78 RSS (21–39 %). Worst case exceeds the 40 % maximum: **either specify a 2.5 mm free-height part at 0.75 mm nominal (worst case 0.37–1.13 = 15–45 %, RSS 0.57–0.93 = 23–37 %) or add a 0.05 mm-proud insulating stop on the tab that references the PCB surface directly and removes the two shell terms (worst case ± 0.23).** Decision on 10 measured Mule B stacks (V-3).
- Force: ≥ 0.5 N nominal, ≥ 0.3 N at minimum compression `[U]`; 0.3 mm-radius dimple on the tip for a defined wiping point.
- Current: **0.13–0.20 A rms** at 23 dBm (row 17). Contact-resistance acceptance ≤ 30 mΩ initial, ≤ 50 mΩ after V-3/V-17 (≤ 0.05 dB).
- Second source: same footprint/height from another vendor, qualified on Mule B.

**Step 7. Cap feed land.**
- On the underside of the tab, inside the sealed volume (sweat never reaches it — this is what makes Au-on-Al acceptable).
- Size: 3.0 × 4.0 mm flat (x × y), Ra ≤ 0.8 µm after machining; lateral stack ± 0.3 mm leaves ≥ 0.8 mm plating margin.
- Finish per M4: **Route A** masked immersion EN **Type IV (5–9 % P) or Type V (≥ 10 % P), ≥ 5 µm (SC1)** + hard electrolytic Au 0.25–0.5 µm (ASTM B488) preferred over immersion Au 0.05–0.1 µm for a wiping contact `[U]`; or **Route C** press-fit plated insert. Conductivity of the Ni is irrelevant (it carries no RF current: skin depth in Au ≈ 3 µm, in Ni-P 10–20 µm `[U]`; the current spreads into the aluminium after the contact) — the Ni is a corrosion barrier, so the high-P amorphous classes are correct.
- **Bare-aluminium annulus at the plug boundary:** define it — width ≤ 0.5 mm, laser-de-oxidised, inside the sealed volume; humidity test of the Au/Ni/Al triple junction in V-3.

**Step 8. DC return, DC block, current path.**
- Shunt inductor to ground at the antenna side of the match (also the first low-band element): 12–33 nH `[U]`, wirewound 0402, rated for the ESD residual (Step 9). Bleeds triboelectric charge from the cap continuously.
- DC block: whether ANT tolerates a DC short through that inductor is `[U]` (DK connects antennas directly with fixed matching `[V?, DK guide snippet]`); PS pin description must be opened. A 100 pF C0G series cap at ANT is footprinted (0.02 dB).
- Path on schematic and PCB: ANT → (series C) → switch connector (X ≈ 50–53) → match (X 55–63) → TVS + L_dc (X = 63) → feed trace (X = 63–65.5, 1.0–1.5 mm, top layer, no ground within 2 mm) → finger pad (X 65.5–67.5) → finger → tab land → cap. Return: ground edge at X = 63 back to the SiP. **A DC test pad on the antenna-side node** (between L_dc and the first series element) for M12.

#### Phase 3 — Matching network (weeks 4–8, again on EVM-1)

**Step 9. ESD/TVS first.**
- Threat: exposed metal → IEC 61000-4-2 ± 8 kV contact / ± 15 kV air (level 4) `[U]` as a product requirement. **Test method for the anodised surface:** IEC 61000-4-2 applies contact discharge to conductive surfaces; for coated surfaces the tip penetrates the coating unless the manufacturer declares the coating insulating, in which case air discharge is used `[V?]` — declare **contact discharge through the anodise** (worst case) for the cap and the ring edge so V-11 matches the lab.
- Part class: antenna-grade suppressor **≤ 0.3 pF** (better ≤ 0.1 pF): ceramic/varistor antenna ESD (Murata LXES, TDK, Samsung ~0.05 pF `[U]`) or silicon (Semtech RClamp / Nexperia PESD antenna families, 0.2–0.3 pF `[U]`). **MPN `[U]`**; confirm C at 700 MHz and 2 GHz, clamp, flat S21 to 2.2 GHz.
- Placement: first component on the feed trace at X = 63, shunt, before any series element; L_dc beside it; the switch connector is on the SiP side of the match so a chamber cable never bypasses the TVS.
- Crown (owned by §4/§3 C-4): 1 MΩ bleed via a BeCu leaf in the sleeve ∥ low-C TVS on the satellite PCB; 2k2/10 pF on the IQS211B sense line.

**Step 10. Matching network procedure (dual-resonant, 5 × 0402 + spares).**
1. Z_ant at the finger plane from simulation, then from Mule B — tune against the measured set.
2. Expected: B12 Ra 5–12 Ω, Xa −j120…−j250 Ω `[U]`; B2/B4 near the cap's second resonance, Ra 15–40 Ω, Xa ± j50 `[U]`.
3. **Topology A (drawn, with reactances):** from the cap — **shunt L_dc 22 nH** (+j100 Ω at 722 MHz, +j263 Ω at 1900 MHz: low-band resonator, near-transparent at high band) → **series (L1 15 nH ‖ C_byp 1.0 pF)**, parallel-resonant at 1.30 GHz between the bands: at 722 MHz X_L = +68, X_C = −220 → net **+j98 Ω** (inductive, L_eff ≈ 22 nH, tunes out the cap's capacitive Xa); at 1900 MHz X_L = +179, X_C = −84 → net **−j158 Ω** (capacitive) → **shunt C1 1.5 pF** (−j147 at 722, −j56 at 1900) → **series C2 3.3 pF** (−j67 at 722, −j25 at 1900; absorbs the residual high-band reactance with the following element) → **shunt C3 / L3 at ANT** (high-band trim). Six positions; two zero-crossings (one in B12, one across B2/B4). Values are illustrative — the point is that the low-band series inductor **must be bypassed by a parallel C** or the high band cannot pass, and every element is stated at both band centres.
4. **Topology B (diplexed):** series-L low-band branch and series-C high-band branch joined at ANT; 5–6 elements; more tolerant of the second resonance landing between B4 and B2.
5. Parts: Murata LQW15AN / Coilcraft 0402DC/0402HP inductors, Murata GJM1555C1H C0G capacitors — the classes Ignion uses `[V, AN_NN02-224 Table 3]`. Tolerances ± 2 % (G) or ± 0.1 nH < 5 nH; ± 0.05 pF (W) < 2 pF, ± 2 % above. **Q_comp at 700 MHz `[U]` (50–80 planned) until the datasheet curve is read.**
6. Loss target η_match ≥ −2.0 dB B12, ≥ −1.0 dB B2/B4 via η = 1/(1 + Q_net/Q_comp). If Q_net > 30 is needed, the antenna is wrong, not the match.
7. Monte Carlo 1000 runs: Δf ≈ ½(ΔL/L + ΔC/C) → ± 1.5–2.5 % → ± 11–18 MHz at 722 MHz. Yield criterion ≥ 97 % ≥ 12.3 % across 699–746 at 25 °C; ≤ 0.5 dB extra spread −10…+40 °C — **include the ring's εr(T) and moisture uptake (PC ~0.2–0.3 % `[U]`) and the cell-swell change of cap-to-cell spacing as Monte Carlo inputs.**
8. Layout: match on the ground side of X = 63, in a straight line along the side strip (Step 11b), ground vias ≤ 0.5 mm from shunt pads, nothing under it, top layer.
9. **Eight 0402 footprints for five parts plus two reserved for the harmonic trap (Step 10b)** — ten positions total.

**Step 10b. Harmonics and radiated spurious.**
- Arithmetic: 3 × (699–716) = **2097–2148 MHz — inside B4 DL (2110–2155) and inside the high-band match passband**; 2 × B12 = 1398–1432 MHz; 2 × B2/B4 = 3.4–3.9 GHz. A single-band 700 MHz antenna attenuates the modem's H2/H3 by its own mismatch; **this one does not.**
- Limits: 3GPP TS 36.101 §6.6.3.1 general spurious (−30 dBm/1 MHz above 1 GHz) and §6.6.3.3 UE-coexistence (−50 dBm/1 MHz protecting listed DL bands) `[V?]`; FCC §27.53 (43 + 10 log P, −13 dBm) and §24.238 `[V?]` (ecfr.gov blocked); PTCRB radiated spurious per TS 36.124 `[V?]`.
- Actions: simulate (Step 5.9); **nRF9151 conducted H2/H3 at ANT `[U]` until measured on EVM-1 V-9**; radiated spurious pre-scan V-9b; **two reserved 0402 positions for a series/shunt notch at 2.1 GHz (0.1–0.3 dB in-band `[U]`)** — a notch at H3 also costs high-band bandwidth, so the trap is only fitted if V-9b fails.

**Step 11. Keepout translated into PCB and mechanical constraints (sign-off list).**
- PCB: ground/signal copper on all six layers ends at X = 63.0 ± 0.1, straight edge. Beyond it only the feed trace, finger pad, TVS/L_dc pads and test pad at X ≤ 64. No vias, fiducials, thieving or test pads in X > 64. **Substrate edge X = 68.0 ± 0.1** (§3 C-5; the ring skirt occupies 68–71).
- Cell: **X ≤ 62** (19–62 baseline; 24–67 measured for comparison on Mule B). 43 mm cell → X = 19–62; verify against the crown bulkhead; else 40 mm ≈ 650 mAh `[U]`.
- LRA can: **X = 52–60**; bracket non-metallic, or metal ending ≤ 61.
- Display FPC toward the crown end; AMOLED PMIC + inductor + load switch at X < 40.
- No metal fastener, insert, pogo pad, shim, Hall sensor in X > 61.
- Lug on the crown-end tray flank; interposer mandatory, non-conductive (Dyneema/UHMWPE in POM; no conductive sizing; no metal ferrules within 20 mm `[U]`).
- Transverse crown: satellite PCB → side-shaft sensor (MA782-class); crown zone −3 mm → **to the keepout buffer**, not body length.

**Step 11b. Width-wise floor plan, top side, X = 49–68.** PCB 23 mm wide, y = 0 on the centreline.
- **Centre strip (y = −4…+4):** LRA can Ø8 at X = 52–60, bracket to X ≤ 61 (polymer). DRV2625 and its leads at X < 49.
- **RF strip (y = +4…+11.5, 7.5 mm wide):** ANT trace from the SiP → **MM8130-2600 switch connector (2.5 × 2.5 × 1.4 mm `[V]`) at X ≈ 50–53** → ten 0402 positions in a line at 1.0 mm pitch, X = 53–63 → TVS + L_dc + DC test pad at X = 63–64 → feed trace X = 64–65.5 → finger at X = 65.5–67.5. Height available here is the full internal stack minus the AMOLED region (the display ends at X = 49), so **width, not the 0.7 mm battery-column figure, is the constraint** — 7.5 mm takes a 2.5 mm connector and a 0402 line with 1 mm clearances.
- **Halo strip (y = −4…−11.5):** PLCC-4 RGB at X ≈ 62–63 firing +X into the ring's light stub; 3 × SOT-523 FETs + 10 nF each at X = 55–60; LED return on the ground fill.
- Bottom side X = 62–68: empty (no copper; cell ends at 62). Draw at scale before the finger MPN is chosen.

**Step 12. The probe / production test point.**
- **Adopted: Murata MM8130-2600 RF switch connector** in place of the DNP MHF4: inserting a probe disconnects the SiP and gives a conducted port to match + antenna; removing it restores the path. 2.5 × 2.5 mm, 1.4 ± 0.1 mm `[V]`; insertion loss `[U]` ~0.2–0.3 dB — measure on EVM-1. Keep the MHF4 footprint as DNP only if the consultancy's chamber fixtures need it.
- Chamber cable dressing: ferrites every 5 cm, exit at the crown end perpendicular to the body `[U]`; cable error at 700 MHz on a 95 mm DUT can be 1–3 dB — see V-5b for the cable-free option.

**Step 13. The IQS211B electrode as an RF victim (with the primary source).**
- Mechanism: a 23 dBm burst puts volts of RF across a floating electrode near the counterpoise; the IQS211B front end rectifies it → false grip during every TX.
- Hardware fix (doc): 2k2 series at the electrode pin (with Cx 5–15 pF `[U]` → ~4 MHz low-pass), 10 pF C0G at the IC, ground-referenced return; the electrode is now buried ~1 mm inside the bulkhead wall (§3 C-4) — still a floating conductor at the E-max.
- **Firmware blanking: use the modem's COEX0 pin.** `AT%XCOEX0=<count>,<state>,<freqlo>,<freqhi>,…` (MHz) configures COEX0 to take the given state whenever the modem's RF is active in that range and the inverse when RF is off; it must be sent before any modem activity; example `AT%XCOEX0=3,1,1570,1580,1,2000,2180,1,600,800` `[V, nRF91 AT Commands Reference v1.9 §6.1]`. For us: `AT%XCOEX0=2,1,690,760,1,1700,2160`. **Caveat from the source: COEX0 is an RF-active (RX and TX) indicator, not a PA-on strobe** — blanking also covers short RX windows, which is harmless. Route COEX0 → application-core GPIO → mask IQS211B transitions while high + 20 ms. `%XMODEMTRACE`/CONEVAL are not real-time and are not used. **Confirm identical semantics in the nRF91x1 AT guide `[V?]`.**
- Verify on Mule B (V-4): DK at 23 dBm B12, electrode coupon at real spacing, 0 false grips per 100 bursts.
- Electrode ≥ 40 mm from the cap; flex on the crown side of the cell.

**Step 14. Coexistence inside the ring and with the AMOLED.**
- Halo LED at X ≈ 62–63 (not in the keepout), firing into the ring's stub; three GPIO traces + VSYS end at X = 63; PWM at ~1–4 kHz — no RF issue; 10 nF at each FET; LED return on the ground fill, not through the match's vias.
- AMOLED PMIC (TPS65631-class, ~1–2 MHz `[U]`): PMIC + shielded inductor at X < 40, caps within 2 mm, ELVDD/ELVSS on inner layers between grounds; conducted-spur scan on rails; **TIS screen-on vs off ≤ 1 dB** (V-10).
- LRA/DRV2625 PWM (~20 kHz class `[U]`): no RF issue; position is the issue.
- SPI 8 MHz `[V?]`: 33 Ω series terminations; SCK away from the ANT trace.

#### Phase 4 — Certification path (define now; execute months 4–7)

**Step 15. Sequence.**
1. Consultancy chamber: passive (Mule B) → active TRP/TIS (EVM-1).
2. **PTCRB:** confirm the nRF9151's module-level PTCRB/GCF certificate ID and the remaining end-product tests (radiated spurious, OTA per NAPRD03 IoT) `[U]`.
3. **CTIA OTA** at a CATL per CTIA OTA Test Plan v3.8+ (AT&T v2.1 Note 4 `[V]`); configuration per the Step 1 classification answer.
4. **AT&T** approval via PTCRB + the Table 4 report; band mask B2/B4/B12 documented.
5. **FCC:** custom chassis antenna → transmitter certified in our name: Part 24 (B2), Part 27 (B4, B12), Part 22 only if B5; Part 15B. **RF exposure: SAR required** — KDB 447498 exclusion (P_mW/d_mm)·√f_GHz ≤ 3.0 `[V?]` gives ~34 at 200 mW / 5 mm. **SAR outcome `[U]`** (the "expected low" claim is withdrawn: SAR is near-field absorption; a 12 %-efficient antenna in a hand dissipates most of ~140 mW, a large part of it in the hand, at the cap-end E-max where fingers go). **Plan:** EVM-1 SAR pre-scan, 1-g body-worn (pocket, at the FCC-assigned separation) and 10-g extremity (hand-held); **if 1-g > 1.6 W/kg or 10-g > 4 W/kg, switch to PC5** (gate +7.0/+9.0 dBm, efficiency gate unchanged). Cost ~$8–15k `[U]`.
6. **ISED Canada** (if in scope `[U]`): **RSS-130 (700 MHz), RSS-133 (PCS 1900), RSS-139 (AWS)** + RSS-Gen; RSS-132 only if B5 `[V?]`; RSS-102 for exposure.
7. **CE RED (if EU):** EN 301 908-1/-13, EN 301 489-1/-52, EN IEC 62368-1, **EN 50566 with EN IEC 62209-1528 for SAR** (EN 62479 is the ≤ 20 mW exemption and does not apply) `[V?]`; UN38.3 / IEC 62133-2 for the cell. EU SKU = a different tune (B20/B8/B3/B1) and a separate OTA campaign.
8. Verizon (B13) — out of scope for the first SKU.

**Step 16. Lock the antenna BOM at DVT.** Any change to cap alloy/finish, ring resin, cell vendor/thickness, LRA position, AMOLED module, PMIC, or shell mould after the OTA report is an ECO with re-measurement.

### 5.7 MANUFACTURING — process flow and assembly sequence

Supplier types in brackets; QC checks in **bold**. Process numbers `[U]` unless tagged.

#### A. End cap (6061-T6)

**M1. Design the cap for machining (RF geometry frozen from Design Phase 1).**
- Stock: 6061-T6 bar Ø30 or 28 × 16 mm, mill-certified (ASTM B221/EN 573). Do not substitute 2xxx/7xxx (poor anodise, corrosion) or 6063 without re-checking conductivity (~3.0 × 10⁷ S/m `[V?]`). **Per-lot conductivity:** declared negligible (± 10 % σ → < 0.005 dB); record the cert, no eddy-current test needed.
- Envelope: 27 × 15 mm radiused capsule × 22.5 mm; outer radii matched to the shell.
- Walls: 1.0 mm min outer, inner web 1.2 mm at the ring face.
- Features: (a) ring-retention groove 0.8 deep × 1.0 wide on the inner face (the ring's tongue snaps in) — or an undercut for insert-moulding (M8); (b) **L-shaped feed tab**: 5 mm wide (y) × 1.5 mm thick (z), projecting from the web through the ring web's sealed aperture and 2.5 mm past the PCB substrate edge (to X = 65.5, §3 C-5), underside land 3.0 × 4.0 mm flat at the Step 6 height, Ra ≤ 0.8 µm, lateral position per the Step 5.4 result; the tab's edges radiused R0.3; (c) **two Ø1.2 mm blind holes** for the ring's moulded pins (pins on the moulded part, holes on the machined part); (d) optional 1 mm laser slit (Step 5.8) — decide before the cap program is released.
- Tolerances: land height to the cap's shell-seating face ± 0.05; outer profile ± 0.05; Ra 0.8 general, 0.4 cosmetic.
- Drawing notes: plating/mask zone (M4), RoHS finishing chain (M5), "no burr on the ring face — the isolation is the antenna gap".

**M2. CNC ops [precision CNC shop, 3–5 axis, consumer-electronics grade].** Op 10 rough external profile (lathe/3-axis); Op 20 internal pocket, web, tab, groove, holes from the open face (the tab is a 3-axis feature: mill around it, then finish its underside land with a flip or a T-cutter); Op 30 5-axis/fixture flip for outer radii and the cosmetic end; Op 40 deburr/tumble (ceramic, 20–40 min), bead-blast 120–180 grit if matte. Cycle 4–7 min at 1k. **100 % land-height gauge; first-article CMM.**

**M3. Pre-finish cleaning:** alkaline degrease → rinse → **non-chrome deoxidise/desmut (nitric or ferric-sulphate class; no Cr(VI))** → rinse. Handle by the tab with clean fixtures.

**M4. Feed-land finish — two co-baseline routes qualified on Mule B, chosen by V-3/V-8.**
- **Route A (anodise first, then masked immersion EN + Au).** Rack-anodise (M5) with the land **plugged** (silicone plug/maskant) so it stays bare; strip plug; laser-ablate the land (fibre laser 1064 nm, 20–50 W) to defined Ra 1–2 µm; **mask the anodised body** (plater's lacquer/tape rated for alkaline zincate); alkaline etch → desmut → double zincate (ASTM B253) → **immersion (bath) electroless Ni-P, ASTM B733 Type IV (5–9 % P) or Type V (≥ 10 % P), Service Condition SC1 ≥ 5 µm** (SC classes `[V?]`: SC0 0.1 / SC1 5 / SC2 13 / SC3 25 / SC4 75 µm from secondary summaries; open B733 before the drawing is released) → **gold per ASTM B488** (hard electrolytic 0.25–0.5 µm preferred; immersion 0.05–0.1 µm acceptable with V-3 as the gate). Alternative selective method: **brush *electrolytic* Ni (sulphamate) + brush hard Au** (Sifco-class) — "brush electroless" is not a process and is deleted. Define the **bare-Al annulus at the plug edge**: ≤ 0.5 mm, laser-de-oxidised, inside the sealed volume.
- **Route B (plate first, mask, anodise).** Kept only as a record: the anodise pre-etch/desmut creeps under the plug and lifts the plating edge; not qualified unless A and C both fail.
- **Route C (plated insert) — co-baseline.** Machine a Ø3 mm H7 blind bore in the tab's underside; after anodise (bore plugged), press in a **catalogue gold-over-nickel plated brass/phosphor-bronze pogo-target pin** (ASTM B488 Au 0.5 µm over ≥ 2.5 µm Ni, barrel-plated) with 0.02–0.04 mm interference; the finger lands on the pin head. Galvanic couple brass/Al inside the sealed dry volume; RF contact at the press fit (~mΩ). Lowest process risk, catalogue second source, one extra part.
- **Acceptance (both):** land-to-cap DC resistance ≤ 5 mΩ (4-wire, before anodise on a sacrificial or through the pin head); adhesion by tape (ASTM B571) + thermal shock −40/+85 °C 5 cycles (cap-ring sub-assembly, no cell) no lift; Au/Ni thickness by XRF 5 pcs/lot; no plating outside a Ø0.5 mm halo. [Aluminium-capable EN house, ISO 9001, working to ASTM B733/MIL-DTL-32119, with masking; or a Sifco-licensed brush plater.] *This supersedes §7 Phase 2 item 3's "EN 3–5 µm + Au 0.1–0.3 µm" (§3 C-6).*

**M5. Anodise — MIL-A-8625 Type II (sulphuric, 8–15 µm), Class 1 or 2 (dyed), RoHS seal (hot DI water, nickel-acetate, or trivalent-chromium; no dichromate seal — Cr(VI)), non-chrome desmut, stated on the drawing.** Type III (25–50 µm) grows outward, dulls colour, and is a poorer insulator at the plug edge; PVD (TiN/ZrN/DLC over all-over EN) is the bright alternative that makes the whole cap conductive-surfaced (no selective plating needed; the finger lands anywhere) at +$1.5–3/pc `[U]` and a different galvanic story at the ring joint. **Checks:** thickness by eddy-current 5 pcs/lot; ΔE ≤ 1.5 vs master; **dielectric ≥ 250 V over the ring face**; no burr. Note: the anodised exterior is a ~10 µm insulator; the cap still radiates (current is inside the metal); the user's touch is capacitive; **ESD is contact-through-anodise (declared, Step 9)**.

#### B. Split ring (optical PC light guide)

**M6. Material.** **Optical PC** (Makrolon LED/light-guide class, εr ≈ 2.9, tan δ ≈ 0.006 `[U]`) — PC/ABS is opaque (§7); a diffusing grade if the halo should be soft. RF: tan δ ≤ 0.01 at 1 GHz, εr stated, no carbon black/EMI fillers/glass fibre. UL 94 V-2 min. **Moisture uptake and εr(T) `[U]` — measured on a coupon (split-post resonator, dry and after 24 h water soak).** Two named grades.

**M7. Geometry (harmonised with §7 J4/J9, §3 C-5).** A capsule-outline **ring-disc with a full 1.5 mm web** (1.5–2.0 per Step 5.2) spanning the section; skirts 0.8 mm thick × 3 mm into the tray end (X = 68–71) and into the cap bore; a **sealed rectangular aperture ≈ 5.6 × 2.1 mm** in the web for the cap's tab (≥ 0.3 mm epoxy annulus); **two Ø1.2 mm moulded pins** into the cap's holes; a **light-injection stub** on the halo side running −X along the inner shell wall to the LED at X ≈ 62–63 with a 45° facet; 0.1 mm matte on the visible rim; light path ≥ 1.0 mm thick everywhere. *[The RF model must carry the web; the tab length grows from 3.5 to ~6.5 mm past the web — a Mule B sweep variable.]*

**M8. Moulding vs insert-moulding.**
- **Baseline: separate moulded ring**, snapped/keyed to the cap then to the shell (single-cavity tool ~$6–12k `[U]`); swappable on Mule B for gap sweeps.
- **Option: insert-mould onto the anodised cap.** Monolithic joint, perfect concentricity; but any cap change is a tool trial, the plated land must be masked in-tool, and **sealed Type II anodise may craze at the 280–300 °C melt front `[U]`** — a crazing trial on 5 caps is a Mule B item if this option is kept.
- Tool: P20/H13, single cavity, SPI-A2 on light-guide faces; **first-off:** thickness ± 0.05, flatness 0.05, no weld line across the light path, dielectric coupon.

#### C. Cap / ring / body joint and seal

**M9. Joint.** Cap ↔ ring: tongue-and-groove + **PC-safe 2K clear epoxy** (§7 Step 2; UV-cure acrylated urethane only with an ESC screen; MMA/DP8005 rejected), ≤ 0.1 mm bond line, or insert-moulded; the tab aperture is epoxied in the same operation (J9). Ring ↔ shell: same, or ultrasonic weld PC-to-PC/ABS (0.3 mm energy director). Drop loads (1.5 m, cap corner) carried on the cap's internal lip against the shell, never on the 1.5 mm ring or the finger. Seal: the ring-to-shell bond is the IP67 seal at this end, or a 0.5 mm O-ring on the cap's inner lip inside the ring silhouette (no RF-gap change). **No conductive gaskets; no screws, brass inserts or metal clips at this joint.**

#### D. PCB and assembly

**M10. PCB fab [6-layer, 0.8 mm].** Fab note: copper terminates at X = 63.0 ± 0.1 on every layer; **no thieving in X > 63**; solder mask over the keepout; feed trace is an antenna element, not 50 Ω-controlled; ENIG on the finger pad and the DC test pad; substrate edge X = 68.0 ± 0.1.

**M11. SMT.** Match, TVS, L_dc, switch connector in the SiP pass; standard reflow (no special atmosphere); finger in the **last** placement head with a vacuum nozzle sized for it, stencil per the finger vendor (typically 0.10–0.12 mm), peak ≤ 260 °C, ≤ 40 s above 217 °C `[U]` (BeCu temper). **AOI on finger coplanarity and tip height ± 0.1 mm.**

**M12. Post-SMT electrical test (bed of nails).** (a) **Antenna-side DC test pad → finger tip: ≤ 0.3 Ω** (trace + finger, no series C in the path); (b) **test pad → ground: L_dc DCR 0.2–0.6 Ω** (proves the DC return); (c) TVS leakage; (d) programming per Addendum A.2, including `AT%XCOEX0` and `%XMAGPIO` provisioning and the `%XRFTEST` enable state (do **not** issue `%XPRODDONE` before M14 — it permanently disables `%XRFTEST` `[V, AT guide v1.9 §11.2–11.3]`).

**M13. Final assembly (cap end).** (1) Cap with finished land, inspected; (2) ring bonded/snapped, tab through the sealed aperture → "cap-ring" sub-assembly (§7 pre-line P10); (3) **halo uniformity camera go/no-go** (20 mA into the stub); (4) cap-ring bonded to the tray end (§7 P20), cured 24 h; (5) PCB + cell + LRA + display into the tray — **PCB z-registered on the tray ribs (datum Z1)**; the tab's land presses the finger in z as the PCB seats (the cap is already on the tray); (6) **feed check = S11 signature at the switch connector** (probe inserted, VNA or a reflectometer head): finger-open vs finger-closed differ by > 10 dB return loss at 722 MHz — a 2 s test, 100 %; the DC probe on the anodised exterior is deleted (reads open); (7) lid, leak test, EOL per §7; (8) M14. *[Editor: because §7 bonds the cap-ring to the tray in the pre-line, the sequence is cap-on-tray first, PCB second — the finger is compressed as the PCB is lowered onto the ribs under the tab; the tab's underside must be visible through the open rear for the AOI/probe at step 6.]*

**M14. Production RF test.**
- **Driver:** factory-mode command over the dock's SWD/RTT invoking `AT%XRFTEST=1,1,<band>,<freq/100kHz>,<dBm>,1,<mod>,…` for TX (B12 low/mid/high, B2 mid, B4 mid; +23 dBm or the PC5 value; QPSK or CW) and `AT%XRFTEST=0,1,<band>,<freq>,…` for RX, which **returns the measured antenna-port power** `[V, AT guide v1.9 §11.2–11.3; V? for nRF91x1]`. `%XPRODDONE` issued only after pass.
- **100 % radiated go/no-go** in a shield box with a fixed coupling antenna ($3–8k `[U]`), power meter on TX; RX via the box's CW source and the `%XRFTEST` RX reading. **Limits: −1.0 / +2.0 dB vs golden-unit value**; box repeatability ≤ 0.3 dB (fixture + nightly golden check); ~15–25 s/unit.
- **Sampling 1–2 %: conducted** through the switch connector on a comm tester (CMW500/MT8821C class).
- **Golden units:** five chamber-measured; limits re-verified weekly.
- Reject flow: fail → re-seat PCB/finger (S11 check) → re-test; second fail → scrap cap-ring-tray, keep PCBA.

#### E. Build-package documentation
Cap drawing (tab, land, mask zone, RoHS chain); ring drawing (εr/tan δ, colour, pins, stub, tab aperture); PCB fab note; SMT finger note; golden-unit chamber report; certification configuration (band mask, power class, firmware, COEX0 table) frozen with the ECO baseline.

### 5.8 VERIFICATION — Mule B and the test programme

#### Mule B (RF mule) — ~$20k incl. chamber, 5 weeks (doc §10)

**Week 0 — Build list.**
1. 3 × 22.5 mm caps + 2 × 20 + 2 × 25 mm, anodised Type II, land by **Route A on three, Route C on two**; two extra caps if the insert-moulding crazing trial is run; tab lengths to reach X = 65.5 (and 68.5 for comparison).
2. 6 × rings: machined optical PC and moulded PC at 1.5 mm with the full web and tab aperture, plus 1.0/2.0/2.5 mm machined.
3. 5 × 23 × 52 mm 6-layer boards (substrate to X = 68): real stack-up, keepout, feed trace, ten 0402 positions, TVS, **MM8130-2600 switch connector** (+ MHF4 DNP), coax exit toward the crown end, dummy SiP pad (12.1 × 11.1 mm), realistic top-side loading, the width-wise floor plan of Step 11b; **two boards with the 8.4 mm LRA slot at X = 52–60 (one copper-bridged)** (§3 C-7).
4. Dummy cell: Al-laminate pouch 23 × 43 × 6.0 and 6.5 mm (real discharged cell or foil-wrapped block), placed at X = 19–62 and 24–67.
5. Real RM69310 module (unpowered) with FPC; 0.5 mm lens + OCA.
6. Real VG0840001D on a bracket (polymer) at X = 52–60; real non-magnetic crown + race insert + magnet; POM sleeve; satellite dummy; IQS electrode coupon (buried ring); 430 SS shim; pogo flex; SS lug in the tray flank.
7. Printed shell in PC/PC-ABS FDM or a known-εr SLA resin (SLS nylon tan δ ≈ 0.02 `[U]` — avoid).
8. 28 mm Dyneema/POM interposer; 120 g key bundle (10 keys, steel ring).
9. Hand phantom (CTIA-style) and a flat body phantom at the lab.
10. **Battery-powered CW source module** (~0 dBm, 700/1900 MHz, optically triggered) that fits in the mule for the cable-free cross-check (V-5b).

**Week 1–2 — Bench (VNA 300 kHz–8.5 GHz, cal at the switch-connector probe plane).**
- V-1 **Impedance survey** S11 600–2300 MHz over cap length × gap × tab position/length × crown grounded/floating × cell position/thickness × LRA slot; Q_ant vs simulation: ≤ 15 % in f_res, ≤ 30 % in Q, else find the missing conductor.
- V-2 **Match tuning** on the measured Z_ant: |S11| ≤ −6 dB across 699–746 and 1710–2155 MHz; record values and the harmonic-band S11.
- V-3 **Finger/land**: 10 measured stacks (compression range vs Step 6 prediction); 4-wire contact resistance, 10 mating cycles per route, ≤ 30 mΩ; **96 h 85 °C/85 % RH on cap-ring sub-assemblies only (no cell)**, ≤ 50 mΩ; 1 h 170 Hz at 2 g mated, Δ ≤ 10 mΩ; Au/Ni/Al triple-junction inspection at the plug boundary.
- V-4 **Electrode victim**: DK at 23 dBm B12 into a coupon antenna, IQS211B EVB at real spacing behind 1 mm PC/ABS: false grips per 100 bursts, with/without 2k2/10 pF, and with COEX0-driven masking: target 0.

**Week 3 — CTIA chamber (2–3 days; passive via the switch connector).**
- V-5 **Total and radiation efficiency** at 700/722/746/750/850/900/1400/1420/1710/1750/1850/1900/1950/2100/2120/2150 MHz in: **bare**, **body phantom 10 mm** (AT&T Note 6 config), **hand at the crown end (petting grip)**; keys ± interposer; crown grounded vs floating; **ring gap 1.0/1.5/2.0** on the best cap; **cell 19–62 vs 24–67; slot vs no slot**. Cable dressing per Step 12, second orientation Δ ≤ 0.5 dB.
- V-5b **Cable-independent cross-check** at 722 MHz bare: the battery CW source in the mule, received power vs a reference dipole in the same chamber (substitution) — agree with the cabled result within 1 dB, else the cabled number is suspect and the cabled method is corrected before any structural decision.
- V-6 **3D pattern** at 722 and 1880 MHz bare.
- V-7 **Near-field E at the electrode** for the victim calculation.

**Week 4 — Decide.**
- V-8 Land route by V-3 (lowest drift; Route C if within 10 mΩ of A).
- **Gate (doc §10, binding): ≥ 15 % total efficiency bare across 699–746 MHz.** Also B2/B4 ≥ 25 % target / ≥ 17.8 % floor. Plus the §7 decisions: cell x; LRA slot dead if > 1 dB.

| Outcome at B12 (bare, worst channel) | Action |
|---|---|
| ≥ 18 % and B2/B4 ≥ 25 % | Freeze cap/gap/tab. EVM-1 with spare positions DNP. |
| 15–18 % | Proceed; book a second chamber slot after EVM-1; hold 1 mm of body length and the keepout buffer as reserve. |
| 12–15 % | **Doc §10 rule: go to Plan B and re-measure.** **Proposed amendment (needs sign-off, not yet binding):** one structural iteration (cap +2 mm / keepout +2 mm / tab offset / laser slit) time-boxed to 2 weeks, run *in parallel* with the Plan B simulation, so Week-6 chooses between two measured numbers. Match is not iterated in either case. |
| < 12 % | Plan B immediately: polymer cap, 32 mm clearance, NN03-310 lengthwise, ~105 mm — **simulate first** (38 × 50 mm board gives 8.4 % at 698 MHz `[V, AN_NN03-310_EB_size Table 1]`; the 23 × ~75 mm ground is unpublished), request Ignion's Antenna Intelligence Cloud report `[V, UM/AN text]`, then a Plan B mule. If Plan B < 15 %: escalate on form factor/band strategy. |
| Hand/keys | Hand drop > 8 dB or keys-without-interposer > 10 dB: field-link issue, not cert; feed the coverage-search governor model; interposer becomes a packaging requirement. |
| B2/B4 < 17.8 %, B12 fine | Add the high-band lever (tab offset or slit) — the one case where a cap iteration for the high band alone is justified. |
| Harmonic-band efficiency (1.4/2.1 GHz) > −6 dB | Flag to Step 10b: plan on fitting the trap; simulate its in-band cost. |

#### EVM-1 (first real board, months 3–4)
- V-9 Conducted through the switch connector: TX power per band/channel at PC3 (records actual MPR/A-MPR/ΔTC applied on B12 edge channels — turns the `[V?]` into `[V]`); **conducted H2/H3 level at ANT**; switch-connector insertion loss.
- V-9b **Radiated spurious pre-scan** at an EMC lab, max power, B12 low/mid/high and B2/B4 mid, 30 MHz–12.75 GHz, against TS 36.101 §6.6.3 / FCC §27.53 limits `[V?]`; fail → fit the reserved trap, re-measure in-band loss.
- V-10 **Active TRP/TIS** in the certification configuration, 3 channels/band: pass = TRP ≥ gate + 2.0 dB, TIS ≤ gate − 2.0 dB. TIS AMOLED on (full white, max) vs off: Δ ≤ 1 dB.
- V-10b **SAR pre-scan**: 1-g body-worn at the FCC pocket separation and 10-g extremity in the CTIA hand at PC3 mid-channel B12/B2/B4 → decides PC3 vs PC5 before DVT.
- V-11 ESD: IEC 61000-4-2 ± 8 kV **contact through the anodise** to the cap (10 strikes/polarity, 3 positions incl. the ring edge) and ± 15 kV air to crown and ring; pass = modem functional, TRP within 0.5 dB, TVS leakage unchanged.
- V-12 Unit spread: 10 units, TRP B12 mid, σ ≤ 0.6 dB (consistent with the −1.0 dB production floor at ~1.7σ; if σ > 0.6 tighten tolerance grades or add a select-on-test position — last resort).
- V-13 Temperature/humidity: TRP at −10/+25/+45 °C in the RF box, drift ≤ 1 dB; **plus 24 h humidity soak of the ring (moisture uptake) and a swollen-cell dummy (+0.6 mm) — each ≤ 0.5 dB**.
- V-14 Field: 3 units, 2 weeks, real keys ± interposer, RSRP/RSRQ/CE-mode log vs a DK on the same SIM.
- V-15 **COEX0 blanking timing**: scope COEX0 vs RF envelope on B12 and B4 — assert lead/lag ≤ 1 ms; false-grip count during a 10-minute connected-mode session = 0.

#### DVT/PVT
- V-16 Golden units (5) → production box limits (M14), including the −1.0/+2.0 dB window and the ≤ 0.3 dB repeatability study.
- V-17 Drop 1.5 m, 6 faces + 4 corners (cap corner first) → box test ≤ 1 dB change; S11 finger check; contact resistance.
- V-18 **Long-term: 500 h at 60 °C / 90 % RH on sealed *real* units (within the cell vendor's storage limit — confirm it in writing `[U]`) *and* 500 h 85/85 + thermal cycling −20/+60 °C 100 cycles on RF-representative units with foil-block dummy cells and unpowered AMOLED** → box ≤ 1 dB; tear-down, land inspection (no corrosion halo at the plating boundary).
- V-19 Certification campaign per Step 15.

#### What-if branches pre-decided
- AT&T classes the device *wearable*: body phantom becomes the pass/fail configuration; add ~2–4 dB `[U]` to the required bare efficiency and re-run the Week-4 table.
- Transverse crown wins (Mule C): re-run V-1/V-5 for the crown end only; expect < 0.5 dB unless the side-shaft sensor adds metal near the lug.
- ANT pin carries DC bias or dislikes a DC short: fit the footprinted 100 pF series C.
- SAR pre-scan fails at PC3: switch to PC5 (efficiency gate unchanged), re-run the power model for CE-mode repetition cost.
- V-9b spurious fails: fit the 2.1 GHz trap; if in-band loss > 0.3 dB, re-tune the high-band resonance downward so B12 H3 falls on its skirt.

### 5.9 Suppliers, process types, NRE and unit cost

All money figures `[U]` unless tagged; consistent with the decision document's lumps (antenna NRE $30–70k; cap $6.50; shells/ring $5.50; match/TVS inside a $4.00 passives lump; chamber $8–15k; certification $50–150k).

#### Antenna programme NRE (3–5 months, $30–70k)

| Item | Supplier type | NRE | Time |
|---|---|---|---|
| Antenna consultancy (EM sim incl. harmonic bands, match design, chamber support, cert config) | Independent RF/antenna house with CST/HFSS and a calibrated chamber; Ignion's service only for Plan B | $20–40k | 10–16 wk |
| Mule B hardware (caps ×7–9, rings ×6, boards ×5, dummies, shells, battery CW source) | Proto CNC (5-day), quick-turn 6-layer PCB honouring the keepout, EN/brush plating job shop, plated-pin catalogue | $6–11k | 3 wk |
| Chamber (Mule B passive + EVM-1 active pre-scan, 3–5 days at $2.5–4k/day) | CTIA-authorised OTA lab or consultancy chamber | $8–15k | 1 wk each |
| ESD/EMC pre-scan incl. radiated spurious (V-9b) | EMC lab, 1–2 days | $2–4k | — |
| SAR pre-scan (V-10b) | SAR lab, 1 day | $3–6k | — |
| Ignion Antenna Intelligence Cloud report (Plan B) | Ignion (free tier per its AN text `[V]`) | $0 | 24 h |
| **Subtotal** | | **$39–76k** | **3–5 mo** |

Certification (separate line, doc $50–150k): PTCRB integration + CTIA OTA $15–35k; FCC Part 24/27 + 15B + SAR $25–50k; ISED (RSS-130/-133/-139/-102) +$5–10k; CE RED with a second tune and OTA +$30–60k; CTIA test-plan use fee $2,500 `[V?, search snippet]`.

#### Tooling
- Ring injection tool: single cavity, P20/H13, polished light-guide faces: $6–12k, 4–6 wk; insert-moulding variant +$4–8k + cap-holding fixture + crazing trial.
- Cap: no hard tooling; fixtures + CMM program $1–2k; anodise racks $0.5–1k; plating masks/plugs $0.5–1.5k; laser program: hours.
- Production RF shield box + fixture + power meter + probe for the switch connector: $6–15k; comm tester rented or CM-supplied.

#### Unit cost at 1k (cap-end antenna subsystem)

| Item | Process / supplier type | @1k | @10k | Notes |
|---|---|---|---|---|
| 6061-T6 stock | Mill-certified bar | $0.30 | $0.20 | |
| CNC incl. L-tab, deburr, blast | Precision CNC shop | $2.80–4.30 | $1.80–2.70 | tab adds ~0.5 min |
| Type II anodise, RoHS seal, plug mask | Anodise house, MIL-A-8625 | $0.50–0.90 | $0.30–0.50 | |
| Land finish: Route A (masked EN Type IV/V ≥ 5 µm + Au) or Route C (plated pin) | EN house / catalogue pin | $0.80–1.60 | $0.40–0.90 | XRF per lot |
| Laser ablation + inspection | Fibre laser cell at the CM | $0.10–0.20 | $0.05 | |
| **Cap total** | | **$4.50–7.30** (doc $6.50) | **$2.75–4.35** | |
| Ring, moulded optical PC | Injection moulder | $0.20–0.45 | $0.12–0.25 | inside the doc's $5.50 |
| Spring finger, BeCu Ni/Au, vertical-deflection | Harwin/TE/Würth/Kinsun class | $0.05–0.15 | $0.03–0.08 | second source |
| Match: 5 × 0402 high-Q + 2 trap positions (DNP unless V-9b fails) | Authorised distribution | $0.35–0.90 | $0.20–0.50 | tolerance grades ~2× standard |
| Antenna ESD device ≤ 0.3 pF | Murata/TDK/Samsung/Semtech/Nexperia class | $0.08–0.30 | $0.05–0.15 | |
| RF switch connector MM8130-2600 | Murata | $0.15–0.35 | $0.10–0.20 | 2.5 × 2.5 × 1.4 mm `[V]`; pays back in test time only after the fit and IL are confirmed on EVM-1 |
| Adhesive/weld at the ring | PC-safe 2K epoxy / ultrasonic | $0.05–0.12 | $0.03 | |
| Production RF test, amortised (S11 check + box) | ~25 s on a $12k station | $0.12–0.25 | $0.06 | |
| **Antenna subsystem total** | | **≈ $5.5–9.8** | **≈ $3.4–5.6** | inside doc's $6.50 + share of $5.50 + share of $4.00 |

#### Second sources and lead times
- 6061-T6: universal; two CNC shops from one drawing, qualified on cap-to-cap RF spread ≤ 0.3 dB.
- Land finish: Route C is the only route with a catalogue second source — keep it qualified even if A ships.
- Ring resin: two named grades with measured εr/tan δ/moisture; the match may need ± 1 value between them — record both.
- Match parts: dual-source every value at the same Q class (Murata ↔ Coilcraft/TDK); a lower-Q substitute is 0.3–0.8 dB and a re-measurement.
- Spring finger: lead time `[U]` (8–12 wk mass-production / 4–6 wk soft-tool is a distributor figure) — order with the cap program.
- nRF9151-LACA-R: 16–19 wk `[V?, doc]` — gates EVM-1 active OTA; PO before schematic.

### 5.10 RISKS — ranked by kill-probability × irrecoverability, each with the test that settles it

**R1. B12 total efficiency below 12.3 % (product-killing; ~40–50 % `[U]`).** Estimate 8–18 % straddles the gate; Ignion's length data (54.3 → 12.2 % as ground falls 120 → 40 mm at 824 MHz `[V, AN_NN02-224 Table 4]`) confirm steep length dependence on a wider board at a higher band. Mitigation: coupling-element architecture using the full 95 mm; hold body length; cap/gap/tab as Mule B sweep variables; do not spend the keepout. Test: V-5 (≥ 15 % bare) cross-checked by V-5b. Fallback: Plan B — not a sure pass (8.4 % at 698 MHz on 38 × 50 mm `[V]`); simulate it before Week 4.

**R2. Feed geometry/stack wrong at first build (blocking if unresolved; now designed out).** The original x-compressed finger would have sheared its joint; the z-deflection L-tab is the fix, but the worst-case stack (± 0.38 mm) still exceeds 40 % compression at one end without the 2.5 mm part or the PCB-referenced stop; the 3 mm longer tab (§3 C-5) is a new cantilever term. Test: V-3 on 10 stacks; M11 AOI; V-17 drop → S11 check.

**R3. B2/B4 gate (17.8 %) missed while B12 passes (cert-blocking; ~20 %).** Mitigation: second resonance co-designed (tab offset/slit); SOW item. Test: V-5 at 1710–2150 MHz; V-10.

**R4. Radiated harmonic/spurious failure — B12 H3 inside B4 DL and the high-band passband (cert-blocking; ~15–25 % `[U]`).** Mitigation: Step 5.9 simulation, reserved trap positions, V-9/V-9b before DVT. Test: EMC pre-scan vs TS 36.101 §6.6.3 / FCC §27.53 `[V?]`.

**R5. SAR at PC3 exceeds limits in-hand or in-pocket (schedule + power-model change; probability `[U]`, not "low").** Mitigation: V-10b pre-scan; PC5 fallback with the TRP gate dropping in lockstep `[V, Table 4]`. Test: 1-g body-worn and 10-g extremity on EVM-1.

**R6. Feed contact degrades in the field (RMAs; ~15 % Route A, < 5 % Route C `[U]`).** Modes: porous thin Au over EN over zincated Al; fretting at 170 Hz; finger set after drop; plating edge/bare-Al annulus corrosion. Mitigation: land inside the sealed volume; Type IV/V EN ≥ 5 µm + B488 Au or plated insert; ≥ 0.5 N; S11 check at assembly. Test: V-3, V-17, V-18 (dummy-cell 85/85).

**R7. Keepout violated by the doc's own layout (2–5 dB `[U]`; certain unless fixed).** Cell ≤ 62, LRA ≤ 61 using the AMOLED's ~4 mm; floor plan of Step 11b. Test: V-1/V-5 with LRA/cell at both positions — cheap, and the millimetres are contested.

**R8. Layout collision at X = 49–68 top side (respin; certain unless drawn).** Mitigation: Step 11b three-strip plan; MM8130 height 1.4 mm `[V]` in the SiP column. Test: scale drawing before finger/connector MPNs are chosen; Mule B boards built to it.

**R9. Hand + keys detune/absorb 4–10 dB in use (field margin, CE-mode time, battery; high).** Mitigation: non-conductive interposer; petting-grip model; PC3 kept if SAR allows. Test: V-5 hand/keys; V-14 field.

**R10. Match tolerance and unit spread eat the margin (yield; ~25 %).** ± 11–18 MHz scatter vs 47 MHz; ring εr(T)/moisture and cell swell add drift. Mitigation: tolerance grades, Monte Carlo with the new inputs, ten positions, −1.0/+2.0 dB production window with ≤ 0.3 dB box repeatability. Test: V-12, V-13, box statistics.

**R11. Regulatory classification surprises (4–8 wk; ~30 %).** Wearable/body phantom vs free-space; RSS/EN set corrected. Mitigation: written AT&T answer; Step 15 list. Test: the answer; V-10b.

**R12. ESD through the cap into ANT (dead modem; low if designed).** Mitigation: ≤ 0.3 pF suppressor first, shunt L_dc, contact-through-anodise declared. Test: V-11.

**R13. IQS211B false grips during TX (feature failure; ~40 % without the network).** Mitigation: 2k2/10 pF + COEX0-driven blanking `[V, AT guide v1.9 §6.1]` (RF-active semantics, `[V?]` on nRF91x1). Test: V-4, V-15.

**R14. AMOLED PMIC desenses RX (TIS margin; ~20 %).** Mitigation: PMIC at X < 40, shielded inductor, inner-layer rails. Test: V-10 screen-on/off ≤ 1 dB.

**R15. Plating process mis-specified at the plater (rework, schedule; was high, now low).** "Brush electroless" and low-P Type II removed; B733 Type/SC and B488 stated; bare-Al annulus defined. Test: M4 acceptance + V-3.

**R16. Ring dielectric/optics conflict (0.2–0.5 dB or cosmetic; ~15 %).** Two named grades; coupon measurement dry/wet; the full web and tab aperture are now in the model. Test: split-post resonator; Mule B ring swap.

**R17. Cable-dressing error in passive measurement (false pass/fail 1–3 dB at 700 MHz; high with a 95 mm DUT).** Mitigation: ferrites, crown-end exit, two orientations, **V-5b cable-free cross-check**, active TRP on EVM-1 before any structural decision is final.

**R18. Insert-moulded ring crazes the anodise (cosmetic reject; `[U]`).** Mitigation: baseline is the separate ring; crazing trial if insert-moulding is pursued.

**R19. Crown decision (transverse) moves metal toward the lug/electrode (small; per Mule C).** Test: V-1/V-5 delta ≤ 0.5 dB.

**R20. Second-SKU band plans (EU; Verizon B13) are a different match and OTA campaign (certain if pursued).** Plan the match as a per-SKU BOM.

### 5.11 Open questions (RF)

1. AT&T classification: is a pocket/keychain LTE-M device "wearable" (body phantom, v2.1 Note 6) or plain SFF free-space? Written answer from the AT&T Partner Coordinator before Mule B's pass/fail configuration is fixed. Experiment: the letter; then V-5 in both configurations.
2. Feed finger stack: worst-case ± 0.38 mm exceeds the 40 % compression maximum on a 2.0 mm finger. Choose between a 2.5 mm free-height part at 0.75 mm nominal and a PCB-referenced 0.05 mm-proud stop on the cap tab. Settled by measuring compression on 10 Mule B stacks (V-3) and opening the chosen finger's force-deflection curve `[U]` until then.
3. Decision-doc corrections to be signed into REDESIGN_DECISION: (i) §6.3 line 472 — crown/lug sit at the E-field (voltage) maximum, not the current maximum; (ii) §4.3 — Au-to-6061 galvanic gap ≈ 0.9–1.0 V vs SCE, not ~1.5 V `[V?]`; (iii) §6.2 vs §6.3 — LRA 55–69 and cell to 67 violate the 8 mm buffer / 10 mm cell rule (adopted cell ≤ 62, LRA ≤ 61); (iv) §6.3 line 468 — ka = 0.636 / Q_min 5.46 / FBW 12.9 % matches neither the 23 × 55 board (ka 0.45, Q_min 13) nor the 95 mm capsule (ka 0.76, Q_min 3.65).
4. Proposed amendment to §10's binary Mule B rule: at 12–15 % bare, one time-boxed (2 wk) structural iteration in parallel with the Plan B simulation. Not binding until signed.
5. nRF9151 ANT pin: DC bias? tolerance of a DC short through the shunt inductor? ESD rating? layout guidance? The full Product Specification and Hardware Integration Guide could not be fetched; `[U]` until opened; the 100 pF series C is footprinted.
6. COEX0 semantics on nRF91x1: the nRF9160 AT guide v1.9 §6.1 `[V]` defines COEX0 as an RF-active-in-frequency-range indicator (RX and TX). Confirm the nRF91x1 CIoT AT Commands guide keeps the same behaviour and pin, and that `%XRFTEST` exists with the same syntax on nRF9151 `[V?]`. Experiment: Mule A + V-15 scope test.
7. 3GPP TS 36.101 numbers behind the 21.5 dBm are `[V?]`; the modem's applied power per B12 channel is measured on EVM-1 (V-9).
8. nRF9151 conducted H2/H3 at the ANT port and the radiated spurious outcome with a dual-band antenna whose high-band passband contains B12 × 3: `[U]` until V-9/V-9b. FCC §27.53/§24.238 and TS 36.101 §6.6.3 limits not opened `[V?]`.
9. SAR: outcome `[U]`; KDB 447498 exclusion not met (~34 vs 3.0, formula recalled `[V?]`). PC3 vs PC5 is decided by the EVM-1 SAR pre-scan. Confirm the FCC exposure classes and separation distances with the TCB.
10. Q at 700 MHz of the chosen 0402 inductors: datasheet curves not opened; the 2.0–2.8 dB match-loss estimate depends on it `[U]`.
11. ASTM B733 Type IV/V and SC1 (≥ 5 µm) and ASTM B488 gold classes are from secondary summaries `[V?]`; open the standards before the cap drawing is released. Immersion vs hard electrolytic Au, and Route A vs Route C, are settled by V-3/V-8.
12. Plan B viability: NN03-310 on Ignion's 38 × 50 mm board gives 8.4 % at 698 MHz `[V]`; nothing is published for a 23 mm-wide, ~75 mm ground with 32 mm clearance. Simulate and request the Ignion report before Mule B reports.
13. Ring resin: optical PC grade (clear vs diffusing) — εr, tan δ at 1 GHz, εr(T) and moisture uptake `[U]` until a moulded coupon is measured dry and after a 24 h soak; ID has not specified clear vs diffuse.
14. Insert-moulded ring: does sealed Type II anodise craze at the melt front? `[U]`; 5-cap crazing trial if the option is kept.
15. Which SKUs: AT&T-only B2/B4/B12 first (recommended); B13 widens the low band and changes the match; EU is a second tune and OTA campaign. Decide before match values are frozen.
16. Crown DC bleed (now specified as a BeCu leaf + 1 MΩ ∥ TVS, §3 C-4) and the ESD test method declaration for the anodised cap (contact-through-coating vs air, IEC 61000-4-2 `[V?]`) — the second must be agreed with the certification lab before V-11.
17. Coaxial vs transverse crown (Mule C): if transverse wins, the freed ~3 mm goes to the keepout buffer (recommended), not body length. Confirm with mechanical.
18. Nordic module-level PTCRB/GCF status of the nRF9151 and the remaining end-product tests with a custom chassis antenna: `[U]`; sets the certification budget line.
19. Cell vendor's storage-temperature/humidity limit in writing (drives V-18) `[U]`.
20. *(new, §3 C-5)* Tab length through the full ring web to X = 65.5 and the web's dielectric: EM re-run and Mule B sweep before the cap program is released.

---

## 6. Electronics — domain report (revised after hostile review)

*Status: this section replaces the editor-assembled §6 of the first issue. The electronics domain report was delivered in a second pass — analysed, hostile-reviewed (14 findings, 10 missing steps, 7 mis-tags) and revised — and merged on 2026-09-19. Same frame (X = 0 at the crown front face), same step labels (E-n design / EM-n manufacturing / EV-n verification / ER-n risks), same tags. Every reviewer finding is either accepted and fixed below, or rebutted with the primary source named; the disposition table is §6.1.1. No project file other than this report was modified. Scope: main PCB (nRF9151 LTE-M, power tree, RM69310 AMOLED + PMIC, sensors/haptics, dock, satellite interface), PCBA manufacturing, programming/provisioning, functional and conducted-RF test.*

### 6.1 What this subsystem is, and the numbers that govern it

#### 6.1.1 Disposition of the hostile review (14 findings, 10 missing steps, 7 mis-tags)

| # | Finding | Disposition | Where |
|---|---|---|---|
| F1 (blocking) | APPROTECT set at the bare-board fixture, but EM-9 on the sealed unit needs SWD/RTT (`%XRFTEST`, `%XPRODDONE`, eSIM, ship mode) | **Accepted.** APPROTECT/SECUREAPPROTECT is now the *last* SWD operation at pack-out (new **EM-9b**), after `%XPRODDONE`, eSIM confirmation and ship-mode entry; recovery path for an EM-9 failure defined; lock state is a traceability record. Confirmed against §5 M14 ("factory-mode command over the dock's SWD/RTT") and doc A.1 (RTT is the only console) — both re-read this pass | E-14, EM-7b, EM-9, EM-9b, EM-11; §3 C-22 |
| F2 (major) | VBUS↔SWD key bridge: a 3.3 V-working low-C TVS does not clamp at 3.4 V; ~50 mA into an nRF I/O | **Accepted; protection redesigned.** A clamp-to-ground part cannot hold a DC 5 V bridge below VDD_GPIO + 0.3 V, and a Schottky-to-VDD_GPIO pumps V3 (the TPS62840 cannot sink and a dead unit has no rail load). Baseline is now a **gate-to-V3 N-FET pass limiter** on SWDIO, SWCLK (and TACT, see F6): firmware-independent, zero standing current, no rail pump; device-side net can never exceed V3. EV-8 gains a current/voltage criterion | E-13, E-15, EV-8 |
| F3 (major) | EM-6 powered tests (`CFUN=0`, I²C roll-call, LED/LRA) run before firmware exists | **Accepted.** Re-ordered: **EM-6a** passive → **EM-7a** SWD load (MCUboot + signed test image + modem FW) → **EM-6b** powered (rails, I²C, LED/LRA, ≤ 40 µA cell-side via the VBAT test pad, satellite mated, no panel) → **EM-7b** provisioning. What the fixture can drive without firmware is stated | EM-6a/6b, EM-7a/7b |
| F4 (major) | EOL sleep current "via the dock + PPK2" on a sealed unit is not a cell-side measurement; "eDRX idle" needs a live attach the shield box does not have; EV-3 135 µA vs EM-9 200 µA disagree | **Accepted.** The true cell-side number (≤ 40 µA, `CFUN=0`) is measured on the bare PCBA (EM-6b) and on the golden unit (EV-3). At EOL the sealed unit gets a **VBUS-side gross-leak screen** (charging disabled by I²C, Δ vs golden ≤ +50 µA `[U]`, after characterising the BQ25180 VIN-side IQ on 10 units) — it catches a UART left on (+600 µA) or a stuck screen, not a 10 µA fault. The eDRX-idle number (≤ 135 µA mean over 30 min `[U]`) is EV-3/lab only. §7 Phase 5 is asked to change its line (§3 C-23) | EM-6b, EM-9, EV-3; §3 C-23 |
| F5 (major) | AMOLED sequence: "CTRL before ELVDD/ELVSS" not implementable on a single-CTRL PMIC; panel-driven SWIRE arrives while switch B is off; "panel-killing −4 V" is `[U]` presented as settled | **Accepted.** E-5 rewritten: switch B on first (PMIC VIN present, CTRL low = disabled) → switch A → RESX → SLPOUT → SWIRE enables and programs VNEG in one burst → tSLPOUT → DISPON. The transient exposure to −4.0 V is a datasheet check (RM69310 ELVSS abs max), tagged `[U]`; ER-2 downgraded. PMIC_EN ≡ CTRL is one line; if the panel's SWIRE drives it, the nRF has no pin on it (GPIO count 26) | E-5, E-4, ER-2 |
| F6 (major) | /MR net shared with an nRF GPIO — BQ25180 /MR pull-up domain never checked against VDD_GPIO 3.9 V abs max | **Accepted.** SLUSE99C is not in the project and was not opened; the pull-up source is `[U]`. TACT now drives /MR directly and the nRF reads it through the same gate-to-V3 N-FET limiter as the SWD lines (zero standing current, no clamp injection); a series-100 k/Schottky read was rejected because it costs ~10 µA standing if /MR is BAT-referenced, and the BQ25180 push-button wake timers (`[V?]` 300 ms class) are too slow for a UI button. Net added to the abs-max audit; /MR long-press reset timing is OQ-7 | E-1.2, E-1.6, E-10, OQ-7 |
| F7 (major) | Stack-up under-specified: 1+4+1 with microvias only to L2 does not get inner LGA pads or 0.4 mm-pitch centre balls to L3/L4 | **Accepted.** LGA pitch is not in the PS extract (`[U]`). Stack-up now states: filled/capped **through via-in-pad (0.20 mm drill / ≥ 0.40 mm pad, IPC-4761 Type VII `[U]`) under the SiP for every inner pad**, 1+4+1 microvias elsewhere, per-part escape rules, and the 2+2+2 fallback if the fab's pitch escape fails; EM-1 re-costed | E-11, EM-1 |
| F8 (minor) | Reversed head "harmless" is wrong with an active programmer; "ideal diode" misnomer | **Accepted.** P-FET described as reverse-polarity protection; reversed-head analysis rewritten (pad ESD diode conducts, dock driver-limited; series 220 Ω between pad and limiter); EVM-1 bench jig must be keyed | E-1.1, E-13, EV-8 |
| F9 (minor) | Wake latency 220 ms exceeds the ≤ 200 ms story; chain needlessly serial; 1.5 ms slew wait taken from the 5 V figure | **Accepted.** First frame overlaps tSLPOUT (subject to the RM69310 datasheet); estimate ≈ 135–160 ms `[U]`; ≤ 200 ms is the EM-9/EV-5 acceptance, marked provisional; ≥ 3 ms after switch A at 3.1 V (or PG) | §6.1.3 row 14, E-5.4, EM-9, EV-5 |
| F10 (minor) | BQ25180 + MAX17048 placed at X = 40–48 "near the connectors" — connectors are at X = 16–19; MAX17048 moved to V3 silently | **Accepted.** BQ25180 + MAX17048 at X = 19–28 in the −y strip (BATFET path ≤ 10 mm from the cell B2B and the SiP VDD); IQS211B moved to X = 24–30 (electrode line still leaves on the crown side); MAX17048 VDD **from BAT per the doc's block diagram** (it is the cell-sense pin; the gauge must work with the buck off), 5 µA moved back to the cell line | E-1.4, E-12; §3 C-26 |
| F11 (minor) | Stencil AR arithmetic | **Accepted.** 0.22–0.25 mm round in 0.08 mm foil (AR 0.69–0.78); 0.20 mm only in 0.075 mm foil (AR 0.67) | EM-2 |
| F12 (minor) | VBUS TVS silently changed from the doc's "24 V TVS"; VSYS docked ~4.43 V not 4.35 V | **Accepted, with a correction to the doc.** A 24 V-*standoff* TVS clamps above the BQ25180's 25 V abs max and protects nothing; the doc's "24 V" is the *survive-a-24 V-adapter* requirement, met by the BQ25180 IN abs max 25 V `[V]` plus its input OVP (threshold `[U]`, SLUSE99C not opened). TVS is therefore specified by function (working ≥ 5.5 V so it never conducts on a 5 V dock, clamp ≤ 20 V at the dock's current limit), part class `[U]`. VSYS quoted as "3.45–4.35 V on battery, up to ≈ 4.43 V docked (SYS_REG default) `[V?]`" and carried into the PMIC VIN (4.5 V max, 70 mV margin — OQ-7) and LED-anode checks | E-1.1, E-1.3, §6.1.3 row 3 |
| F13 (minor) | No SDO/MISO from the panel → no electronic mate check | **Accepted.** If the 27-pin tail exposes SDO it is wired to the shared MISO (no GPIO cost); otherwise TE toggling after DISPON is the electronic mate check at bring-up and EM-9 | E-6, EM-9 |
| F14 (minor) | ASTM B488 "Type II" mislabels hard gold | **Accepted.** "Type II (99.0 % Au, cobalt-hardened), Code C (hard), ≥ 0.76 µm over ≥ 2.5 µm Ni `[U]` until B488 is opened" | §3 C-25 |
| Missing 1–10 | BQ25180 I²C watchdog; test-image step; APPROTECT at pack-out + failed-unit recovery; sealed-unit sleep method; PMIC IQ with VIN present/disabled; MSL/bake + panel Tstg; eUICC 1.8 V class; EMC immunity; `%CMNG`/SGP.32 prerequisites; dock 5th-line hand-off | **All added** | E-1.2, EM-7a, EM-9b, EM-6b/EM-9, E-5.1/EV-3, EM-3/EM-5, §6.5 item 6, EV-12, EM-7b, §3 C-25 |
| Mis-tags 1–7 | dock pitch `[V]`→`[U]`; IPC-4552 `[V?]`→`[U]`; AS5600L pitch `[V]`→`[V?]`; ER-2 "panel-killing"→unverified; product pages all `[V?]`; latency limits provisional | **All applied** | §6.1.3, EM-1, EM-4, ER-2, E-10 |

What survives unchanged from the first draft because the reviewer confirmed it against the decision document and §3/§4/§5/§7: passive VBUS path (E-2), GPIO-park rule (E-8), 30.7 µA standing sum, 74.1 ms frame arithmetic and 8,064 B strip buffer, VCI margin, keepout/copper-end numbers, placement columns, satellite signal list and 12-way tail proposal, `%XCOEX0` string, `%XPRODDONE` ordering vs §5 M14, bed-of-nails field, cost/lead-time lines.

#### 6.1.2 What this subsystem is

One six-layer 0.8 mm PCB, 23 × 52 mm (substrate X = 16–68, copper ends X = 63.0 ± 0.1 on all layers) carrying: nRF9151-LACA-R (LGA 12.1 × 11.1 × 1.2 `[V]` PS v1.0 extract; top side, X = 20–32, under the panel); BQ25180 charger/power path fed from a 4-pad magnetic pogo dock on a lid flex; MAX17048 gauge on the cell; TPS62840 3.1 V buck (the only general rail); DRV2625 → VG0840001D LRA; a TPS65631-class AMOLED PMIC + shielded inductor + two load switches → RM69310 AMOLED (126 × 294, 4-wire SPI, 27-pin tail on a 0.4 mm B2B at X = 46–49); 16 Mbit SPI NOR; MFF2 eUICC (DFN-8 5 × 6, 1.8 V class); IQS211B grip sense; PLCC-4 RGB halo + 3 × SOT-523 N-FETs; three gate-to-V3 N-FET limiters (SWDIO, SWCLK, TACT); the RF chain of §5 (series C footprint → MM8130-2600 → 10 × 0402 → ≤ 0.3 pF TVS + L_dc → feed trace → finger). A 22 × 10 × 0.6 mm 2-layer satellite PCB (MT6701 or AS5600L variant, 2 × DRV5032DU, EVPBB tact, 1 MΩ ∥ TVS bleed) connects by a 0.5 mm-pitch tail (10 signals per §3 C-12; 12-way with two grounds proposed, §3 C-24).

#### 6.1.3 The numbers that govern it (rows changed since the first draft marked ★)

| # | Quantity | Value | Tag / source |
|---|---|---|---|
| 1 | nRF9151 | LGA 12.1 × 11.1 × 1.2; VDD 3.0–5.5 V; PC3 23 / PC5 20 dBm; −108 dBm Cat-M1 low band; single 50 Ω ANT; PSM 2.7 µA; eDRX @ 81.92 s 18 µA; 4 × SPIM/TWIM/UARTE with EasyDMA; 4 × PWM; 2 × RTC; 12-bit 200 ksps SAADC; 32 GPIO; 1 MB / 256 kB; SWD | `[V]` nRF9151 PS v1.0 extract (`firmware\bingbong_pcb\_mech\nrf9151_ps.txt`); **SPIM fmax, LGA pitch, COEX/MAGPIO pin list, SIM voltage class not in the extract** → `[V?]`/`[U]` where used |
| 2 | nRF9151 supply | 16–19 wk lead; $16.08 @ 2k | `[V?]` doc |
| 3 ★ | BQ25180 | IN abs max 25 V; SYS 1.5 A DC / 2.5 A pulse; BATFET 90 mΩ max; IQ_BAT 4 µA typ pushbutton-enabled (budget 5.5 µA); JEITA 0/10/45/60 °C; NTC 10 k β 3435. **VSYS: 3.45–4.35 V on battery; docked, SYS regulation tracks VBAT + ≈ 225 mV → up to ≈ 4.43 V `[V?]`. Input OVP threshold, /MR pull-up domain, reset-default ICHG, I²C-watchdog default: `[U]` (SLUSE99C not in the project)** | `[V]` SLUSE99C per doc §4.1 for the first group |
| 4 | MAX17048 | WLP 0.9 × 1.7; hibernate ≤ 5 µA max; ± 15–20 % without custom INI; VDD = cell | `[V]` 19-6171 (doc) |
| 5 | TPS62840 | 60 nA IQ, 25 nA shutdown typ; VIN 1.8–6.5 V; 750 mA; C(VSET) ≤ 100 pF; RSET 71.5 kΩ → 3.1 V | `[V]` SLVSEC6D (doc); features confirmed on TI's HTML viewer; **RSET table not reached — 71.5 kΩ `[V?]`**; 3.2 V availability `[U]` |
| 6 | DRV2625 | 105 nA shutdown / 1.55 µA standby; DSBGA-9 | `[V]` SLOS879C (doc) |
| 7 | DRV5032DU | 1.6 µA typ / 3.5 µA max at 3 V each; 3.9 mT; push-pull | `[V]` SLVSDC7H (§4) |
| 8 | MT6701 / AS5600L | VDD min 3.0 V; 14 mA max / 6.4 mA nom; ≤ 1 ms power-up; programming > 4.5 V / ≥ 3.3 V on the bare fixture only | `[V]` (§4); AS5600L WL-CSP ball pitch `[V?]` (§4 gives the outline, not the pitch) |
| 9 | IQS211B | 2 µA @ 160 ms; 77 µA @ 9 ms; VDDHI 1.764–3.6 V; Cx ≤ 120 pF | `[V]` v2.8.1 (doc) |
| 10 | AMOLED module | 126 × 294 RM69310; VCI 2.7–3.6 V; VDDIO 1.65–3.3 V; ELVDD +4.6 / ELVSS −2.2 V; 27-pin tail; 12.96 × 30.94 × 0.78 | `[V?]` decision text — **no RM69310 or panel electrical table exists in the project** (`datasheets\ER-OLED018-1_Series_Datasheet.pdf` is the old 1.8" SSD1326 PMOLED — BOM_VALIDATION_2026-09-04 §2; §3 C-30) |
| 11 | AMOLED PMIC TPS65631 | VIN 2.9–4.5 V; VPOS fixed 4.6 V, 0.5 %; VNEG −1.4…−4.4 V programmable, default −4.0 V, via CTRL; up to 250 mA; 3 × 3 mm 12-pin WSON | `[V?]` TI product page; IQ(off), IQ(VIN present, CTRL low), fSW, inductor, CTRL/SWIRE protocol, tSTART, sequencing → `[U]` |
| 12 | Display load switch TPS22916 (class) | VIN 1–5.5 V; RON 60 mΩ @ 5 V / 100 mΩ @ 1.8 V; IQ(on) 0.5/1 µA; IQ(off) 10/100 nA; reverse-current blocking (−300 nA max); slew C 1400 µs @ 5 V / ≈ 3000 µs @ 1.8 V; 2 A; WCSP 0.78 × 0.78, 0.4 mm pitch | `[V?]` TI product page |
| 13 | Full-frame SPI time | 592,704 bit → 74.1 ms at 8 MHz → 13.5 fps | computed on `[V?]` clock |
| 14 ★ | Screen wake latency | switch A/B on + ≥ 3 ms → RESX ≥ 10 µs + ≥ 5 ms → SLPOUT; **first frame (74 ms) written during the tSLPOUT wait (≈ 120 ms class)**; SWIRE/PMIC settle ≤ 2 ms → DISPON → **≈ 135–160 ms `[U]`**; halo/LRA within 15 ms; **acceptance ≤ 200 ms (§3 C-11), provisional `[U]` until Mule A** | all element delays `[U]` until the RM69310 datasheet is opened |
| 15 | Power budget (doc) | 127.84 mAh/wk vs 454 usable → 3.55 wk | doc §5.2 |
| 16 | Power budget (AMOLED re-run, E-9) | ≈ 132–153 mAh/wk (mid 139) → 3.0–3.4 wk (560) / 3.2–3.7 wk (600) | `[U]` |
| 17 | Worst-case burst | 395 mA = 0.71C; 0 °C droop 181 mV → cutoff 3.45 V | doc §5.5 |
| 18 | Debug-UART regression | +600 µA = 100 mAh/wk | `[V]` Qoitech (doc) |
| 19 | Coverage-search floor | 1.72 mA continuous → 11 days; governor budget 20 mAh/wk | `[V]` doc §9.6 |
| 20 ★ | Dock | GND · SWCLK · SWDIO · VBUS; **2.54 mm pitch `[U]` (the doc's basis is "wearable-charger de facto standard", not a drawing)**; Au over Ni (spec per §3 C-25); 430 shim; VTref from the dock LDO | `[U]` |
| 21 | Non-modem standing current, sum of MAX lines | app core 2.2 + 2 × DRV5032 7.0 (on the satellite) + IQS211B 2.0 + DRV2625 2.0 + BQ25180 5.5 + MAX17048 5.0 + NOR 1.0 + TPS62840/pull-ups/leakage 5.0 + display switches off + limiters 1.0 = **30.7 µA** | doc lines (`[V]`/`[U]` mix) → EV-3 acceptance ≤ 40 µA, measured with the satellite mated |
| 22 ★ | GPIO budget | **26 of 32** with panel-driven SWIRE (27 if the MCU drives CTRL); 5–6 spare | computed (E-4) |
| 23 ★ | Haptic driver page values | 2.0 Vrms / 68 mA typ / 90 mA max | `[V?]` Vybronics product page — harmonised: every vendor web page is `[V?]` (§3 C-30) |

### 6.2 DESIGN — step by step (schematic sequence: power tree → radio + SIM → sensors/haptics/display → dock/protection → PCB → firmware)

**E-1. Power tree (schematic sheet 1).**
1. **VBUS_PAD** (dock) → 0603 ferrite (≥ 600 mA, ≤ 0.3 Ω `[U]`) → **transient TVS, working voltage ≥ 5.5 V (never conducts on a 5 V dock), Vclamp ≤ 20 V at the dock's current limit `[U]` class** → **reverse-polarity P-FET** (gate to GND through 1 MΩ; no MCU control — E-2; it blocks a reversed head and nothing more) → **BQ25180 IN**; 1 µF + 10 µF at IN. Adapter mis-application (9/12/24 V) is handled by the BQ25180's input OVP (threshold `[U]`, SLUSE99C not opened) and its 25 V IN abs max `[V]` doc §4.1 — the doc's "24 V TVS" is re-read as that requirement, not as a 24 V-standoff part (which would clamp above 25 V and protect nothing).
2. **BQ25180** (SLUSE99C `[V]` per doc): SYS = **VSYS 3.45–4.35 V on battery, up to ≈ 4.43 V docked `[V?]`**; BAT → cell 3-contact B2B (B+, B−, NTC); TS ← 10 k β 3435 NTC on the cell face; **/MR ← crown TACT directly** (the TACT net is a BQ-domain net; the nRF reads it only through the gate-to-V3 limiter of E-13 — F6); /INT → nRF GPIO (VIN-good, charge state, fault, push-button timers); I²C. ICHG = 300 mA set by firmware **only after** a valid NTC read and VIN-good; the reset default stays whatever SLUSE99C gives (`[U]`, OQ-7) — this register rule is the only "hold-off". **I²C watchdog (new, missing step 1):** the BQ2518x register watchdog (default enabled, ~160 s class `[V?]` family knowledge; verify in SLUSE99C) resets ICHG/JEITA/SYS registers when not serviced → firmware **disables it at first configuration** (or services it from the RTC while docked); EV-6 reads the registers back after 10 min docked to prove it. Ship mode by I²C at pack-out; exit by /MR or VIN. Long /MR hardware reset (BATFET cycle, timing `[U]`) is the field recovery path; the timing must exceed any legitimate crown hold (OQ-7).
3. **Loads on VSYS**: nRF9151 VDD (3.0–5.5 V `[V]`) with 4.7 µF + 100 nF at the SiP and 2 × 22 µF 0805 top-side in the side strips (§3 C-19); DRV2625 VDD (range `[U]`); halo common anode (LED Vf + FET at ≈ 4.43 V docked — PWM duty derated when VIN-good, so brightness does not step on docking `[U]`); **AMOLED PMIC VIN (2.9–4.5 V `[V?]`) through switch B — docked VSYS ≈ 4.43 V leaves 70 mV to the PMIC's 4.5 V max; OQ-7 asks SLUSE99C for the SYS_REG ceiling; if it can exceed 4.5 V with the chosen cell, VSYS_REG is programmed lower by firmware or the PMIC VIN moves to V3 via a boost-capable sibling `[U]`.**
4. **TPS62840 → V3 = 3.1 V** (RSET 71.5 kΩ `[V?]`; re-read SLVSEC6D Table 1 at schematic; evaluate 3.2 V per §3 C-13 if listed). C(VSET) ≤ 100 pF `[V]`: VSET trace ≤ 5 mm, no plane under it. L/COUT per SLVSEC6D (`[U]` until read; 2.2 µH / 10 µF class). MODE low; STOP low. Loads: nRF VDD_GPIO (abs max 3.9 V `[V]`), SPI NOR, IQS211B, 2 × DRV5032DU (always on, via the tail), sensor load switch → MT6701/AS5600L, display switch A → VCI + VDDIO, I²C pull-ups 4.7 k, the three limiter gates (no current). **MAX17048 VDD is on BAT (cell), per the doc's block diagram — the gauge must read the cell with the buck off and its 5 µA belongs on the cell line (F10).**
5. **AMOLED rails**: PMIC → ELVDD +4.6 V (fixed `[V?]`) / ELVSS −2.2 V (programmed by SWIRE/CTRL `[V?]`); 4.7–10 µF at each output within 2 mm; negative-rail return on a dedicated island to the PMIC PGND, not the SiP's RF ground.
6. **Abs-max audit (extended):** V3 +2 % = 3.16 V vs VDD_GPIO 3.9 ✓, VDDIO 3.3 ✓, IQS211B 3.6 ✓; V3 −2 % = 3.04 V vs sensor 3.0 V min → sensor switch R_on ≤ 0.5 Ω (§3 C-13); VCI ≥ 2.7 V ✓; **TACT/ /MR net: BQ-domain, up to VBAT/VIN-referenced `[U]` — never on an nRF pin directly (limiter, E-13)**; **SWD pads: 5 V (bridge) — limiter**; **VSYS docked 4.43 V vs PMIC VIN 4.5 V — OQ-7**; **LED anode 4.43 V — duty derate.**
7. **Datasheets governing this sheet**: SLUSE99C (BQ25180), SLVSEC6D (TPS62840), TPS65631 and TPS22916 datasheets (**not opened; product pages only**), 19-6171 (MAX17048).

**E-2. Why the VBUS path is passive (dead-battery lockout).** A sealed product with a single 4-pad port must recover from (a) ship mode, (b) a 0 V cell, (c) a bricked image. In all three the nRF is not running; anything on the VBUS path that needs a GPIO is a lockout. Protection against a key bridge is therefore (i) the dock-side current limit (doc A.2), (ii) the SWD limiters (E-13), (iii) the BQ25180's own OVP/VINDPM/thermal foldback. The doc's "charge current held off until dock presence" survives as the register rule (E-1.2) and as a dock-head enable (dock-board function, `[U]`) — §3 C-22.

**E-3. nRF9151 integration (sheet 2: radio + SIM).**
- Decoupling per the Nordic HIG `[U]` (not opened): 4.7 µF + 100 nF per VDD group, vias to L2 within 1 mm.
- **ANT**: single 50 Ω pin `[V]` → series 100 pF C0G footprint (ANT DC tolerance `[U]`) → MM8130-2600 → ten 0402 → TVS + L_dc → feed trace → finger (§5 Steps 8–12). 50 Ω CPWG from the SiP to the switch connector (E-11); nothing else within 2 mm; SCK routed on the opposite side.
- **COEX0** → app-core GPIO loop-back for IQS211B blanking; `AT%XCOEX0=2,1,690,760,1,1700,2160` (`[V]` syntax nRF9160 v1.9 / `[V?]` nRF91x1). **COEX1/2 and MAGPIO0–2: presence on the nRF9151 `[V?]` — not in the PS extract (OQ-3, §3 C-27); unused pins NC per HIG `[U]`.**
- **SIM**: MFF2 eUICC DFN-8 5 × 6 × 0.85 (footprint `[V]`; MPN `[U]`) on SIM_IO/CLK/RST/**SIM_1V8** — **the interface is 1.8 V (net name in the doc's block diagram; voltage class `[V?]` until the PS SIM chapter is opened) → the eUICC must be ISO 7816-3 Class C (1.8 V)**; HIG series/shunt filter values `[U]`; within 10 mm of the SiP; written supply-shutdown/suspend confirmation before the reel PO (§2 P0-10).
- Band mask B2/B4/B12, LTE-M only, power class per the SAR pre-scan, `%XCOEX0` — in the production image (EM-8).
- **SWD**: SWDIO/SWDCLK through the limiter cells (E-13) to the dock B2B; `nrfutil device recover` over SWD is the reset path (doc A.2).
- Prototype supply: ≥ 40 SiPs at week 0 (§2 P0-1).

**E-4. GPIO and peripheral budget (32 GPIO `[V]`).**

| Function | Lines | Notes |
|---|---|---|
| AMOLED 4-wire SPI (SPIM0) | SCK, MOSI, CS_DISP, D/C | 4 — SPIM is 8-bit-frame `[V?]`, so 4-wire is mandatory |
| SPI NOR on SPIM0 | CS_NOR, MISO | 2 — SCK/MOSI shared; MISO also reads the panel's SDO if the tail exposes it (F13) |
| AMOLED control | RESX, TE (GPIOTE), DISP_SW_A_EN, DISP_SW_B_EN | 4 — **PMIC CTRL is driven by the panel's SWIRE (baseline, no nRF pin); +1 (PMIC_CTRL) only in the MCU-driven variant (E-5.3 b)** |
| I²C0 (TWIM0) | SDA, SCL | 2 — BQ25180, MAX17048, IQS211B, DRV2625, MT6701/AS5600L (0x06 / 0x40 `[V]` §4) |
| Satellite | HA1, HA2, HB1, HB2, TACT (via limiter), SENSOR_SW_EN | 6 — latch lines and TACT on GPIOTE (wake) |
| DRV2625 | TRIG/EN | 1 |
| Halo | R, G, B gates on PWM0 | 3 — hardware PWM (4 × PWM `[V]`) |
| IQS211B RDY | 1 | GPIOTE |
| BQ25180 /INT | 1 | dock presence (VIN-good), push-button timers, faults |
| COEX0 loop-back | 1 | |
| Dock 5th line (jig ID) | 1 | 1 MΩ pull-down; EOL jig only (§3 C-25) |
| **Total** | **26** (27 MCU-CTRL variant) | 5–6 spare — two for the doc §9.8 grip fallback, two for TWIM1 if E-10's sensor bus test fails |

**E-5. AMOLED power path — the block in detail (sheet 3; rewritten per F5).**
1. **Topology.** V3 → **switch A** (TPS22916C-class, slow slew) → VCI + VDDIO with 1 µF + 100 nF at the tail connector. VSYS → **switch B** (same class) → PMIC VIN (10 µF) → PMIC → ELVDD/ELVSS. Switch B exists because both the PMIC's off-state IQ and its **IQ with VIN present and CTRL low (disabled)** are `[U]`; the latter is the current during the ≈ 130 ms between switch-B-on and the SWIRE burst — a glance-energy line, not a standing line, because switch B is off in sleep. Delete switch B only if the TPS65631 datasheet shows IQ(VIN, disabled) ≤ 0.5 µA over temperature. Both switches have reverse-current blocking `[V?]`.
2. **Inrush.** C-slew (≈ 5 mV/µs at 5 V, ≈ 1 mV/µs at 1.8 V `[V?]` TI page → ≈ 2–3 mV/µs at 3.1–4.4 V `[U]`): a 10 µF PMIC input cap draws ≤ 30 mA peak; invisible against the 22 µF SiP reservoir. **Wait ≥ 3 ms (not 1.5 ms) after switch A at 3.1 V, or use a power-good** (F9).
3. **ELVSS programming — two implementations, decided when the RM69310 datasheet is opened.** (a) **Panel-driven SWIRE (baseline):** the RM69310 emits the burst on SWIRE after SLPOUT; **the burst both enables the PMIC and sets VNEG (single CTRL pin: enable and program share the line, so pulses are counted only once the device runs — VNEG necessarily starts at its −4.0 V default `[V?]` and steps to −2.2 V within the burst)**. The PMIC's VIN must already be present (switch B on before SLPOUT) or the burst is lost. (b) **MCU-driven CTRL:** the nRF sends the count-coded pulses (timing `[U]`) immediately after SLPOUT, same constraint. **The panel's transient exposure to −4.0 V for the burst duration is a datasheet check (RM69310 ELVSS abs max vs −4.0 V), `[U]`;** panels of this class are commonly brought up this way, but that is not evidence. If the abs max is above −4.0 V, use (b) with the pulse count issued inside the PMIC's tSTART window `[U]`, or a resistor-set-VNEG PMIC `[U]` (ER-2).
4. **Sequencing, wake (element delays `[U]` until the datasheet; class values):** park state → **switch B on** (PMIC VIN present, CTRL low) → **switch A on** → wait ≥ 3 ms → RESX low pulse ≥ 10 µs → wait ≥ 5 ms → SLPOUT (0x11) → **panel SWIRE burst (or MCU CTRL) enables the PMIC and programs −2.2 V; ELVDD/ELVSS settle ≤ 2 ms** → **first frame written during the tSLPOUT wait (≈ 120 ms class; RAMWR accepted after SLPOUT on DCS-class drivers `[U]`)** → DISPON (0x29). **≈ 135–160 ms `[U]`; acceptance ≤ 200 ms (§3 C-11), provisional.**
5. **Sequencing, sleep:** DISPOFF (0x28) → SLPIN (0x10) → wait tSLPIN `[U]` (the panel's SWIRE releases the PMIC) → switch B off → **drive SCK, MOSI, CS_DISP, D/C, RESX low; TE input pull-down** → switch A off. Never remove VCI/VDDIO with ELVDD present `[U]`.
6. **Placement (§3 C-10):** PMIC + shielded inductor (2.2–4.7 µH class `[U]`, ≤ 1.0 mm tall, Isat ≥ 0.8 A `[U]`) + caps within 2 mm, at **X = 30–40 in the −y side strip**; ELVDD/ELVSS on L4 between the L2/L5 grounds to the B2B at X = 46–49; switch-node copper minimised; a shielding-can footprint reserved (X < 40 is outside the keepout).
7. **Panel current model** (kept): 6–20 mA cell-side per glance `[U]`; Mule A measures with a DK-driven panel, TPS65631EVM and a PPK2 at 150 and 400 nits.

**E-6. Display interface (SPI) and wiring.**
- **4-wire SPI, mode per the RM69310 (`[U]`)**, SCK ≤ 8 MHz `[V?]`; high-drive pins `[U]` HIG; **33 Ω series in SCK and MOSI at the SiP** (§5 Step 14); ≤ 40 mm from the SiP to the B2B, referenced to L2 without a split.
- **TE** → GPIOTE; window writes start on the TE edge.
- **RESX** from a GPIO with a 10 k pull-down.
- **SDO (F13):** if the 27-pin tail exposes SDO it goes to the shared MISO so RDID/RDDST can be read at bring-up and EM-9 (mate check after drop); if not, **TE toggling after DISPON is the electronic mate check** and is written into E-17 and EM-9.
- The 27-pin map is `[U]` until the panel drawing arrives (§2 P0-5); the symbol is drawn from the drawing.
- No board-added ESD on the SPI lines (they never leave the sealed volume).

**E-7. Frame buffer, partial updates and RAM.** The RM69310 carries its own GRAM `[V?]`; **the MCU keeps no full frame buffer.** One 8–16 kB strip buffer (126 × 32 px × 2 B = 8,064 B) written into a CASET/RASET window (0x2A/0x2B `[U]`) + RAMWR (0x2C); the creature window (60 × 60 px = 7.2 kB → 7.2 ms at 8 MHz → 30 fps for the animated region). **EasyDMA chunking**: SPIM TXD.MAXCNT width `[U]` (PS to confirm) — a 74 kB frame is sent as chained DMA chunks (array list / PPI-timer). **RAM (256 kB `[V]`)**: nrf_modem shared region + heap ≈ 20–40 kB `[U]`, Zephyr + networking + DTLS ≈ 40–60 kB `[U]`, LVGL ≈ 20 kB `[U]`, strip 8–16 kB → ≥ 100 kB headroom; no double-buffered full frame. Fonts/art in the NOR (E-14).

**E-8. Display "off" is really off — the GPIO-park rule.** Every net crossing to the panel carries its parked state on the schematic: SCK/MOSI/CS/D-C/RESX = output low; TE = input pull-down; SWIRE = panel-owned (no nRF pin) or CTRL output low; ELVDD/ELVSS = PMIC off, switch B off. EV-3 measures the VCI/VDDIO node asleep: **≤ 0.2 µA** through switch A (100 nA max off `[V?]`).

**E-9. Power budget re-run (standing line audited).** Standing MAX sum 30.7 µA (§6.1.3 row 21) + the modem's 92.6 µA `[V?]` field figure = 123.3 µA → 20.7 mAh/wk; glances 8.75–29.2 mAh/wk `[U]` (now including the PMIC's VIN-present/disabled interval, E-5.1); total ≈ 132–153 mAh/wk → 3.0–3.4 wk (560) / 3.2–3.7 wk (600). Hardware-PWM halo run current (tens of µA while breathing `[U]`) folded into the aura line and measured on the golden unit. Sensitivities that survive unchanged from the doc §5.3: AS-RAI granted −13; eDRX 81.92 s only +6; eSIM without shutdown +7; heavy user ~×1.5; network refuses eDRX → PSM + 300 s poll ≈ 2.0 wk; sustained CE Mode A/B ≈ 1.6 wk; compound ≈ 0.8 wk — fails at any cell size; a glance-heavy user (100/day at 400 nits) adds ~30 mAh/wk `[U]`.

**E-10. Sensors and haptics (sheet 4).**
- **Satellite interface** (§3 C-12, C-24): 10 signals — proposed order (pin 1 at the +x end): **1 GND · 2 3V1_ON · 3 SDA · 4 SCL · 5 MT_VDD_SW · 6 HA1 · 7 HA2 · 8 HB1 · 9 HB2 · 10 TACT**. **Recommendation to §4: 12-way with GND on pins 1 and 12** — the crown-bleed TVS clamp current returns through the tail ground. **FH12-12S-0.5SH exists in the same series as the -10S `[V]` Hirose FH12 catalogue extract (`bom-scratch\fh12.txt`: contact-array width A = 5.5 vs 4.5 mm, body C = 10.1 vs 9.1 mm); the x-depth is common to the series but not in the extract → `[U]`.** Series 100 Ω at the main-board end of HA/HB; 47 pF to GND at the nRF on the latch lines. **TACT: switch to GND on the satellite; the net is the BQ25180 /MR net (BQ-domain); the nRF reads it through a gate-to-V3 N-FET limiter (E-13) — the satellite's tact and its trace see the /MR pull-up voltage `[U]`, which is why the tail carries no nRF-domain logic on that conductor.**
- **Sensor supply**: load switch R_on ≤ 0.5 Ω from V3; if the unpowered sensor clamps SDA/SCL (`[U]` I/O structure) → TWIM1 on two spare GPIOs (E-4).
- **Wake path** (kept): latch edge → SENSOR_SW_EN → MT6701 ready ≤ 1 ms `[V]` → ≥ 1 detent delta within 200 ms → radio; TACT ≥ 30 ms debounce in firmware; latch edges masked during TACT low; 24-point table + 8 latch-edge angles in NVM (§4 M-23).
- **Grip** (kept): IQS211B, buried 316L ring (§3 C-4), 2k2 + 10 pF C0G at the IC, Cx 5–15 pF `[U]`, COEX0 blanking + 20 ms; grip also blanked during TACT low (the 0.40 mm press is a Cx step); fallback pads reserved (doc §9.8).
- **Haptics** (kept): DRV2625 on I²C + TRIG; LRA closed-loop with braking (55 ms free fall → ~15–25 ms, doc §4.3); waveform library — boop = one overdrive cycle + 18 ms braked decay + 40 ms gap + second transient at 60 %; purr = 170 Hz carrier under a 20–30 Hz envelope with ± 10 % depth / ± 5 % rate jitter; sent-ack = one 30 ms braked tap; 2.0 Vrms / 68 mA typ / 90 mA max `[V?]` vendor page; 10 µF at VDD; OUT± routed as a pair to the LRA pads at X = 52–60, never under the ANT strip; the LRA never renders the user's own detents (doc §7.1).
- **Halo** (kept, PWM0): PLCC-4 at X = 62–63, FETs + 10 nF at X = 55–60, LED return on the ground fill (§5 Step 14); the halo carries arrivals (bloom over 400 ms) as well as the aura.

**E-11. Stack-up proposal — 6-layer, 0.8 mm (rewritten per F7).**

| Layer | Use | Notes |
|---|---|---|
| L1 | components, RF (ANT CPWG), SPI, fine escape | 18 µm base + plating ≈ 35 µm |
| PP1 ≈ 100 µm | FR-4 TG ≥ 170 (low-Dk not required for a 15 mm trace at 0.7–2.2 GHz `[U]`) | laser microvias L1–L2 (filled + capped, IPC-4761 Type VII `[U]`) for 0.4 mm-pitch escapes to GND and for L1 fan-out |
| L2 | **solid GND** | reference for L1; no split under SiP, SPI, ANT |
| core ≈ 110 µm | | |
| L3 | signals (I²C, latch, NOR, LED gates, SiP inner-pad escapes) | |
| PP2 ≈ 100 µm | | |
| L4 | **power**: VSYS, V3 islands; ELVDD/ELVSS island at X < 49 | |
| core ≈ 110 µm | | |
| L5 | **solid GND** | |
| PP3 ≈ 100 µm | | through-vias suffice (bottom nearly component-free) |
| L6 | bottom: connector strip X = 16–19, test-pad field under the cell, plane fill | |

**How L1 signals under the SiP reach L3/L4 (the question a fab quotes on):** the nRF9151 LGA pad pitch and inner-pad count are **not in the PS extract (`[U]`; the nRF9160 HIG is the family reference `[V?]`)**. Rule written for the fab: **(a) every inner LGA pad that is not GND gets a filled, planarised, capped mechanical through via-in-pad (0.20 mm drill / ≥ 0.40 mm pad, IPC-4761 Type VII `[U]`) to L3/L4; GND pads get the same via to L2/L5; outer-row pads escape on L1 to microvias outside the body.** (b) 0.4 mm-pitch DSBGA/WLP/WCSP 2 × 4 and 2 × 2 parts (BQ25180, MAX17048, TPS22916) escape on L1 with no via under the ball; **the DRV2625 3 × 3 centre ball gets one via-in-pad**. (c) If the fab's field solver/DFM shows the 0.40 mm pad does not fit the SiP pitch, the fallback is a **2+2+2 build with stacked L1–L2–L3 microvias** (re-cost EM-1). Er ≈ 4.2–4.5 at 1 GHz `[U]`; **ANT trace 50 Ω CPWG on L1 over L2** ≈ 0.18 mm / 0.15 mm gap `[U]`, fab solver final, coupon "50 Ω ± 10 %"; the feed trace beyond X = 63 is an antenna element and is not impedance-controlled (§5 M10). Copper ends X = 63.0 ± 0.1 on all layers; no vias/thieving/pads in X > 64; substrate edge 68.0 ± 0.1.

**E-12. Placement plan (honours the doc §6.2 columns, §7 Steps 5/6/11 and the §5 keepout; corrected per F10; §3 C-26).**
- **X = 16–19.5 (crown-end strip)**: top — 10/12-way 0.5 mm satellite connector (FH12 class, 2.0 mm `[V]`; x-depth `[U]`, §3 C-12) or hot-bar pad field; bottom — cell 3-way B2B (y = −7), dock 5-way B2B (y = +6), tooling holes y = ± 10.5.
- **X = 20–32, |y| ≤ 6.5 (SiP column, under the panel)**: nRF9151 + its 0402 decoupling (≤ 0.6 mm) only.
- **X = 18–49, |y| = 6.5–11.5 (side strips)**: **−y strip: BQ25180 + MAX17048 + the three limiter FETs at X = 19–28 (cell B2B, dock B2B and the SiP VDD all within ≈ 10 mm; the 395 mA burst path is ≤ 10 mm), IQS211B at X = 24–30 (sense line leaves on the crown side; electrode ≥ 40 mm from the cap holds), AMOLED PMIC + inductor + switches A/B at X = 30–40**; **+y strip**: 2 × 22 µF 0805, MFF2 eSIM (X = 22–30, ≤ 10 mm from the SiP SIM pins), TPS62840 + L + Cout (X = 34–40), SPI NOR (X = 40–46).
- **X = 33–45 under the panel**: ≤ 0.70 mm parts only (0402s, DRV2625 DSBGA at X = 40–45 near the LRA leads, latch series parts).
- **X = 46–49**: AMOLED B2B; **fold zone X = 49–51 component-free**.
- **X = 49–68 top (§5 Step 11b)**: LRA can 52–60 + bracket ≤ 61; +y RF strip: MM8130-2600 at X ≈ 50–53, ten 0402s 53–63, TVS + L_dc + DC pad 63–64, feed trace, finger 65.5–67.5; −y halo strip: FETs 55–60, PLCC-4 62–63.
- **Bottom X = 19–62**: no components; bed-of-nails field (E-16) and plane; **X = 62–68 bottom empty**.
- Four ø1.6 tooling/locating holes at the crown end + slot at X = 66 (§7 Step 3); 0.5 mm copper-free edge strip on the rear side for the lid rib ends.

**E-13. Dock and protection (sheet 5; rewritten per F2/F8).**
- Lid flex: 4 × ø2.0 pads GND · SWCLK · SWDIO · VBUS at 2.54 mm `[U]`, X = 34–44, hard Au over Ni (§3 C-25), 0.3 mm 430 shim, tail to the 5-way 0.4 mm B2B at X = 17–19 (§7 Step 11). Fifth conductor = jig ID/presence (1 MΩ pull-down) — §3 C-25.
- VBUS: E-1.1. **Dock presence = BQ25180 VIN-good via /INT** (no divider).
- **SWD pad protection — the limiter cell (one per line: SWDIO, SWCLK; the same cell on TACT).** Pad → **low-C ESD diode to GND at the pad, 5 V working (the pad can legitimately sit at 5 V during a bridge), ≤ 15 pF `[U]`** → **220 Ω series** on the flex/B2B → **N-FET, drain on the pad side, source on the nRF side, gate to V3** (low-Vth SOT-523 or a dual, Vth ≤ 1 V `[U]`, MPN at schematic) → nRF SWDIO/SWCLK with a **4.7 kΩ pull-up to V3 on the nRF side** (SWDIO) / none (SWCLK, driven). Behaviour: with the pad at ≤ V3 − Vth the channel passes the signal both ways (body diode source→drain pulls the pad down when the nRF drives low); with the pad at 5 V the channel cuts off at Vsource = V3 − Vth and the pull-up lifts the nRF side to V3 — **the nRF pin can never exceed V3, no current is injected into the nRF clamp, nothing is pumped into V3, and it works with no firmware and a 0 V cell.** Timing: 4.7 k × ≈ 25 pF ≈ 120 ns rise on SWDIO-from-dock edges — **SWD at 4 MHz is marginal, 2 MHz is comfortable (EV-9 measures); 2.2 kΩ if 4 MHz is needed (0.6 mA per line only while the dock drives low, docked only).** Rejected alternatives and why: clamp-to-ground TVS (DC clamp ≥ 4–5 V at mA, F2); Schottky to VDD_GPIO (pumps V3 through a buck that cannot sink; a dead unit has no rail load); 1 kΩ + 1 MHz alone (still injects ≈ 1.6 mA into the nRF clamp, limit `[U]`).
- **Key-bridge cases (docked, VBUS live):** VBUS↔GND (dock current limit); VBUS↔SWDIO/SWCLK (pad at 5 V: ESD diode does not conduct, 220 Ω sees ≤ (5 − V3 + Vth)/220 Ω only until the FET cuts off, then zero; nRF side ≤ V3) ✓; SWDIO↔SWCLK (harmless).
- **Reversed head (F8 — not "harmless"):** device GND pad receives +5 V, VBUS pad receives dock GND: the P-FET blocks the power path ✓; **with an active programmer** driving SWDIO/SWCLK low the pad sits at −5 V relative to the device ground, the pad ESD diode conducts (forward) with the dock driver's output current, and the FET channel (VGS = V3 + 0.7) pulls the nRF side toward −0.7 V, limited by the 220 Ω to ≈ 3 mA into the nRF's lower clamp — survivable, not harmless. **Mitigation: cradle polarity keying on the production dock (doc A.2) and on the EVM-1 bench jig; the programmer's VTref-gated output stage is the second line.** EV-8 tests it with a programmer attached.
- Dock board (doc A.2, unchanged): USB-C with 5.1 kΩ Rd, 5 V through to the head current-limited, 3.3 V LDO for VTref on a 10-pin Cortex header; EVM-1 bench jig from an Adafruit 5412-class cable, keyed. Verify no DRV5032 false latch while docked (§3 C-14).

**E-14. Memory and firmware architecture.** 16 Mbit SPI NOR (MX25R1635F class `[U]`, deep power-down ≤ 1 µA `[U]`) on the shared SPIM: MCUboot secondary slot ≈ 1 MB, assets ≈ 0.5–1 MB, settings/log ≈ 128 kB; a full modem image does not fit → delta-only modem FOTA (doc A.4) or 32 Mbit at BOM freeze (OQ-9). nRF Connect SDK / Zephyr, sysbuild + MCUboot, external NOR secondary slot (`nordic,pm-ext-flash`). Production programming = MCUboot + app + modem FW over SWD (EM-7a); `CONFIG_UART_CONSOLE=n` in every build; RTT logging/shell in dev only, **RTT factory-mode command handler kept in the production image until `%XPRODDONE` and removed by the same fragment that locks the unit** (it is the §5 M14 channel); **APPROTECT + SECUREAPPROTECT are the last SWD operation at pack-out (EM-9b), never at the bare-board fixture (F1; §3 C-22)**; per-unit keys to `%CMNG` `[V?]` AT guide with the modem in `CFUN=0`/`4`; release gates as before (tested in a shielded box against a base-station simulator): (a) `+CEDRXRDP`/`+CPSMS` read-back after every attach, detach and RTC-scheduled polling if neither is granted after N attempts (never idle DRX at 1.28 s — 8.2 mA, dead in 2.6 days); (b) coverage-search governor: exponential backoff, "stationary and untouched N minutes → stop searching" (grip/latch inputs; no accelerometer), maximum search duty cycle — numbers in the requirements document; (c) PPK2 golden-unit capture on every release against the Mule A baseline; (d) FOTA delta end-to-end; (e) BQ watchdog disabled. Interaction state machine per doc §7 (eDRX 163.84 s baseline, 5.12 s for 180 s after any interaction, UDP/DTLS, 150 ms de-jitter, ≤ 10 pkt/s coalescing).

**E-15. ESD at every exposed or near-exposed conductor (IEC 61000-4-2 ± 8 kV contact / ± 15 kV air, product requirement `[U]`).**

| Conductor | Path | Part / rule |
|---|---|---|
| Dock pads ×4 | flex → B2B | VBUS: TVS (E-1.1); SWD ×2: pad ESD diode + 220 Ω + limiter FET (E-13); GND: return |
| End cap (antenna) | finger → feed trace | ≤ 0.3 pF suppressor + L_dc at X = 63 (§5 Step 9) |
| Crown (floating) | BeCu bleed leaf → satellite PCB | 1 MΩ ∥ low-C TVS to satellite GND; return via the tail GND (12-way recommendation, §3 C-24) |
| Grip electrode (buried) | 1 mm PC/ABS → 2k2 + 10 pF at IQS211B | blanking covers the transient |
| Lens / panel | 0.50 mm glass + 0.15 OCA | air discharge to the glass; COG and tail are the victims — EV-10; if the panel latches, grounded ITO/mesh or a larger ink border `[U]` |
| Keyring lug (316L) | floating in the tray flank | ≥ 1 mm wall to the satellite tail; EV-10 |
| Satellite / LED lines leaving the board | series 33–100 Ω + 47 pF | kept |
| Cell contacts / NTC | inside the sealed volume | 100 nF at TS |

**E-16. Test points / bed-of-nails.** Bottom, X = 19–62 (under the cell, later under the PET insulator): ø0.9 mm ENIG pads on a 1.27 mm grid, ≥ 24: **VBAT (the PPK2 source-meter point for EM-6b), VSYS, V3, VCI_SW, PMIC_VIN_SW, ELVDD, ELVSS, SDA, SCL, SWDIO_nRF (limiter output), SWCLK_nRF, TE, RESX, CS_DISP, COEX0, TACT_nRF, HA1/HA2/HB1/HB2, NTC, LRA+/LRA−, LED_R/G/B, DOCK_ID, GND ×4.** Top: RF DC test pad at X ≤ 64 (§5 M12) and the MM8130-2600. No pads in X > 64. The fixture reaches the four dock nets through the 5-way B2B footprint pads (pad side of the limiters), not through the lid flex.

**E-17. Firmware bring-up order (EVM-1 rev A, per board).** 1) SWD attach at 1 MHz with VTref from the jig through the limiter cells; read the SiP ID. 2) Rails with the modem unprogrammed (idle). 3) App image with RTT; GPIO park states verified. 4) I²C roll-call (BQ25180, MAX17048, IQS211B, DRV2625, sensor via the switch). 5) BQ25180 register set (ICHG, JEITA, VINDPM, **watchdog disabled**), MAX17048 INI. 6) NOR read-ID and MCUboot swap. 7) Display: switch B → switch A → RESX → SLPOUT → (SWIRE) → frame → DISPON; scope ELVSS at every enable; **RDID over SDO if wired, else TE toggling = mate check**; measure VCI, ELVDD, ELVSS, wake latency, fps. 8) Satellite: latch edges, angle, TACT through the limiter. 9) DRV2625 auto-calibration on the real mass. 10) Modem FW, `%XCOEX0`, band lock, PSM/eDRX; attach on Mule A's SIMs; `%CMNG` writes in `CFUN=0`. 11) PPK2 sleep capture on VBAT (EV-3). 12) `%XRFTEST` conducted (EV-11). 13) SWD/limiter timing at 1/2/4 MHz (EV-9).

### 6.3 MANUFACTURING — PCBA, programming, test (EM-n; re-ordered per F3/F1)

**EM-1. PCB fab specification [6-layer 0.8 mm, IPC-6012 Class 2, IPC-A-600].** FR-4 TG ≥ 170 (370HR / R-1755V class `[U]`), 0.80 ± 0.08 mm; 1+4+1 with laser microvias L1–L2 (filled + capped, IPC-4761 Type VII `[U]`) **plus filled, planarised, capped mechanical through via-in-pad (0.20 mm drill / ≥ 0.40 mm pad) under the nRF9151 LGA for every inner pad and under the DRV2625 centre ball (E-11)**; other through-vias 0.20/0.45; **fallback 2+2+2 stacked microvias if the fab's DFM rejects the LGA-pitch escape** (`[U]` pitch); **surface finish ENIG — Ni and Au thickness per IPC-4552 `[U]` (standard not opened; values are the fab's certified range)**; ENEPIG not required; LPI mask, mask-defined pads only where the SiP HIG asks `[U]`; **impedance coupon 50 Ω ± 10 % for the L1/L2 CPWG**; copper ends X = 63.0 ± 0.1 on all layers, no thieving in X > 63, mask over the keepout, substrate edge 68.0 ± 0.1 (§5 M10); 0.5 mm copper-free rear edge strip; four ø1.6 tooling holes + slot at X = 66 (§7 Step 3). Panelised with both satellite variants (2-layer 0.6 mm, ENIG, 1.0 mm locating holes ± 0.02), mouse-bites away from X = 63–68. **Cost: via-in-pad under the SiP adds ≈ $0.8–1.5/board at 1k over plain 1+4+1 `[U]`; 2+2+2 fallback ≈ +$2–3 `[U]`.**

**EM-2. Stencil and paste (F11 corrected).** Stepped stencil: **0.08 mm over the SiP LGA and the 0.4 mm-pitch DSBGA/WLP/WCSP with 0.22–0.25 mm round apertures (AR 0.69–0.78); 0.20 mm apertures only in 0.075 mm foil (AR 0.67)**; 0.10 mm elsewhere; 0.10–0.12 mm over the finger pad (§5 M11); SAC305 Type 4 (Type 5 under 0.4 mm parts) `[U]`; SPI 100 % on the fine-pitch fields; EMS SPI data decides the final apertures.

**EM-3. SMT — two-sided, with moisture handling (missing step 6).** **MSL:** SiP baked per its PS/HIG MSL rating `[U]` (label + floor-life log at the line); **the AMOLED module is not reflowed (mated at final assembly) but has a storage-temperature limit `[U]` (the doc's +60 °C dashboard warning transfers) — modules stored ≤ 40 °C, ≤ 60 % RH in original trays; no bake (§3 C-28).** Pass 1 bottom (small parts only: cell 3-way and dock 5-way B2B receptacles, strip 0402s — held by surface tension on the second reflow). Pass 2 top: SiP (tray-fed, ± 0.03 mm), DSBGA/WLP/WCSP, PMIC WSON, inductor, eSIM DFN, limiter FETs, connectors, match/TVS/switch connector; **finger last** with its own nozzle (§5 M11). Profile: SAC305 ramp-soak-spike, peak 240–245 °C at the SiP, ≤ 40 s above 217 °C `[U]`. **X-ray 100 % of the SiP via-in-pad field and the 0.4 mm-pitch parts on the first 3 lots** (voids ≤ 25 %, no head-in-pillow, no via-in-pad outgassing voids), then AQL; 3D AOI on everything; finger coplanarity ± 0.1 mm. No underfill on the SiP by default; corner-bond decision after EVM-1 drop (§7 Step 13).

**EM-4. Satellite variants.** Two part numbers (MT6701 QFN and AS5600L WL-CSP), identical outline/holes/tail; BOM-level swap (doc §4.5). **AS5600L WL-CSP pitch `[V?]` (§4 gives the outline 2.07 × 2.63 × 0.6 and the 172.5 µm offset, not the pitch) → via-in-pad on the satellite only if the AS5600L DS confirms 0.4 mm.** Angle-sensor OTP/EEPROM programmed only on the bare satellite fixture (> 4.5 V / ≥ 3.3 V `[V]`), never in-system.

**EM-5. Flex tail and display attach.** Lid flex (0.1 mm PI, hard Au pads per §3 C-25, 430 shim laminated, pad-side ESD diodes and 220 Ω fitted on the flex or at the B2B) is a purchased sub-assembly, continuity + 100 MΩ isolation tested before lamination (§7). Display module arrives laminated (lens + OCA + panel) with the 27-pin tail terminated in the 0.4 mm B2B plug (§7 Step 4), **stored within its Tstg limit**; mated at final assembly through the aperture, fold X = 49–51 (R ≥ 0.5), foam hold-down. Hot-bar/ACF fallback designed into the same pad field.

**EM-6a. Post-SMT passive test (bed of nails, no firmware; E-16 field + the four dock nets through the B2B pads).** (a) Shorts/opens on all rails and nets; (b) RF DC checks per §5 M12 (DC pad → finger ≤ 0.3 Ω; L_dc DCR 0.2–0.6 Ω; RF TVS leakage); (c) SWD pad ESD-diode capacitance sample 1/lot (≤ 15 pF `[U]`); (d) limiter FET check: 5 V on the pad side → nRF-side net ≤ V3 (fixture supplies V3 via the test pad, nRF unpowered is acceptable for this check); (e) connector continuity with a satellite mated; (f) VBUS = 5.0 V through the B2B pads with the nRF **held in reset over SWD by the fixture**: VSYS window, V3 3.04–3.16 V, BQ25180 default registers readable **by the fixture's own I²C master on the SDA/SCL test pads** (the only powered test possible without firmware; the fixture master is tri-stated afterwards).

**EM-7a. Programming — image load (same fixture, ≈ 40 s).** Via SWD through the limiters at ≤ 2 MHz (EV-9 sets the clock): MCUboot + **signed production application (which contains the RTT factory-mode handler and the EM-6b self-test commands)** + modem firmware in one pass (`nrfutil device program`). No provisioning yet; no lock.

**EM-6b. Powered functional test (same fixture, firmware running, ≈ 45 s).** Panel **not fitted** (the panel B2B is unmated on the bare PCBA); satellite **mated** (its 7.0 µA is in the 30.7 µA sum). (a) Rails under firmware: V3 at 0 and 300 mA load, VCI_SW = V3 − ≤ 20 mV with switch A on, PMIC_VIN_SW with switch B on, ELVDD 4.60 ± 1 % / ELVSS −2.20 ± 3 % into a 20 mA fixture dummy load on the panel-B2B pads with the fixture emitting the SWIRE burst `[U]` acceptance; (b) I²C roll-call (5 addresses ACK, sensor through the switch); (c) LED and LRA current signatures; (d) latch/tact through the limiter, angle read; (e) **cell-side sleep current: PPK2 in source-meter mode on the VBAT test pad at 3.8 V, VBUS removed, modem `CFUN=0`, screen switches off, satellite mated: ≤ 40 µA after 30 s** (the only place the true cell-side number is measured in production — F4); (f) BQ25180 watchdog-disabled read-back.

**EM-7b. Provisioning (same fixture, ≈ 20 s).** Over RTT/AT: serial, pair code, `%XCOEX0`/band mask/system mode/power class, `%XMAGPIO` **only if the pin exists on the 9151 (`[V?]`, OQ-3, §3 C-27)**, **DTLS credentials to `%CMNG` with the modem in `CFUN=0`/`4` `[V?]` AT guide**; **eSIM profile download is not done here** (SGP.32 IPA needs a live attach — done at EM-9 on the dock; which entity hosts the IPA — eUICC IPAe, the modem, or the application IPAd — is OQ-8 and decides whether EM-9 needs network access at all); `%XRFTEST` left enabled, **no `%XPRODDONE`, no APPROTECT** (F1).

**EM-8. Build configuration control.** One production Kconfig fragment, reviewed per release: `CONFIG_UART_CONSOLE=n`, `CONFIG_LOG_BACKEND_RTT=n` (prod logging), RTT factory-mode handler compiled in and gated by an unlocked-state flag, MCUboot signing key in the HSM, modem FW pinned, `%XCOEX0`/band constants; PPK2 golden capture (EV-3) attached to the release record.

**EM-9. Final-assembly and EOL functional test (dock jig, ≈ 90 s, §7 Phase 5 — electronics acceptance numbers, corrected per F4/F9/F13).** Dock detect (BQ VIN-good within 200 ms); charge current 300 mA ± 10 % at 3.8 V cell; NTC within 3 °C of jig ambient; JEITA/ICHG/watchdog registers read back; gauge SoC; AMOLED white/RGB/black by camera, **RDID over SDO if wired, else TE toggling after DISPON as the electronic mate check**, **wake ≤ 200 ms crown-press-to-DISPON (provisional `[U]`)**, ≥ 10 fps full-frame counter; halo 3 colours ≥ 70 % uniformity; LRA boop ≥ 0.8 g, ≤ 35 dB(A) `[U]`; crown 2 turns: 48 detents ± 1.5°, all four latches 2×/rev, 24-point table written; press ×5; grip phantom; **sleep screen (sealed unit, 1 in 20): what the dock can measure is VBUS-side input current with charging disabled by I²C, screen asleep, modem `CFUN=0` — accept Δ vs the golden unit ≤ +50 µA `[U]` after characterising the BQ25180 VIN-side quiescent on 10 units; this is a gross-leak screen (catches a +600 µA console or a stuck screen), not the cell-side number, which lives in EM-6b/EV-3 (§3 C-23)**; radiated go/no-go vs golden (−1.0/+2.0 dB B12, B2/B4, §5 M14) → `%XPRODDONE` (RTT factory command) → **eSIM profile download/confirmation over the jig's live attach or the IPA path (OQ-8)** → ship-mode entry by I²C → EM-9b.

**EM-9b. Lock at pack-out (new, F1).** **The last SWD operation on the unit:** verify `%XPRODDONE` and profile state, then set **APPROTECT + SECUREAPPROTECT** (`nrfutil device protect` class command `[U]` exact syntax) and read back the protection state; record it in the MES with the image hashes. **Failed-unit path:** a unit failing any EM-9 item before EM-9b is re-worked/re-tested unlocked; a unit found faulty *after* EM-9b (returns, ORT) is recovered by `nrfutil device recover` (full erase through the dock, doc A.2) → EM-7a → EM-7b → EM-9 → EM-9b, with its previous serial/pair code re-provisioned from the MES.

**EM-10. Conducted RF test (sampling 1–2 %).** Probe in the MM8130-2600 (§5 Step 12); CMW500/MT8821C-class: TX at B12/B2/B4 mid channels (PC3 23 ± 2 dB or the PC5 value), conducted H2/H3 (§5 Step 10b), RX sensitivity via `%XRFTEST` RX; per serial to the MES. Performed before EM-9b on the sampled units.

**EM-11. Traceability.** Panel/PCB lot → SMT lot → SiP date code/reel → EM-6a/7a/6b/7b records (image hashes, modem FW, key IDs) → EM-9 results → **EM-9b lock state and timestamp** → serial ↔ pair code ↔ cell/lens/crown serials (§7 Phase 5); RF golden references and the PPK2 golden capture in the same record.

**EM-12. Rework rules.** SiP: no rework (scrap); 0.4 mm-pitch parts: one rework max under the SiP's temperature limit; finger: replaceable (last-placed, §5 M11); limiter FETs and pad ESD diodes on the flex: flex replaced, not reworked.

### 6.4 VERIFICATION (EV-n) — pass/fail numbers

- **EV-1 Mule A extensions (weeks 0–2, DK + PPK2 + panel + PMIC EVM).** (a) SPIM maximum clock on the DK with a scope (settles 8 MHz `[V?]`); (b) RM69310 module + TPS65631 EVM in the **corrected order (PMIC VIN present and disabled before SLPOUT)**: does the panel's SWIRE burst enable and program the PMIC; **scope ELVSS at every enable — record the duration and depth of the −4.0 V excursion; compare with the RM69310 abs max once the datasheet arrives**; wake latency switch-on-to-DISPON ≤ 200 ms with the frame overlapping tSLPOUT; glance current at 150/400 nits on VCI, ELVDD, ELVSS, PMIC VIN (disabled interval) and cell side; sleep VCI/VDDIO ≤ 0.2 µA with parked GPIOs; (c) eDRX/PSM/AS-RAI grants, MT paging at 163.84 s on ≥ 2 of 3 carriers, per-paging energy (92.6 `[V?]` vs 18 µA `[V]`); (d) UICC suspend (Δ ≤ 5 µA); (e) UART-console regression (+600 µA `[V]`) reproduced and absent with the production fragment; (f) `%XCOEX0`, `%XRFTEST`, `%XMAGPIO`, `%CMNG`-in-`CFUN=0` semantics on nRF91x1 firmware `[V?]`; (g) **limiter cell on a DK: SWD at 1/2/4 MHz through 220 Ω + FET + 4.7 k (and 2.2 k) with the flex length; 5 V bridge on the pad while attached → nRF-side ≤ V3, V3 unchanged**.
- **EV-2 EVM-1 rail bring-up (E-17).** VSYS window on battery and docked (record the docked ceiling vs the PMIC's 4.5 V); V3 3.04–3.16 V at 0/300 mA, ripple ≤ 20 mVpp; VCI_SW drop ≤ 20 mV; ELVDD 4.60 ± 1 %, ELVSS −2.20 ± 3 %; PMIC fSW recorded; **PMIC IQ with VIN present and CTRL low measured (the `[U]` line)**; TPS62840 VSET ≤ 100 pF confirmed by 10 boards reading 3.1 V; **TACT net idle voltage measured (the /MR pull-up domain, OQ-7) and the nRF-side limiter output ≤ V3**.
- **EV-3 PPK2 sleep current, golden unit, every release (cell-side, VBAT pad, panel mated and asleep).** Modem `CFUN=0`: **≤ 40 µA** (30.7 µA MAX sum + margin); modem in eDRX 163.84 s idle, network-attached (lab, base-station simulator or live cell): **≤ 135 µA mean over 30 min `[U]`** (the doc's 92.6 µA + 40 µA) — **lab/golden-unit number only, not an EOL step**; VCI/VDDIO asleep ≤ 0.2 µA; NOR deep power-down ≤ 1 µA; positive control: the UART fragment toggled on must add ≥ 500 µA; **BQ25180 VIN-side quiescent with charging disabled characterised on 10 units to set the EM-9 gross-leak reference**.
- **EV-4 0 °C brownout.** Real cell at 3.45 V cutoff, PC3 burst + 90 mA LRA: VDD at the SiP ≥ 3.30 V during every TX subframe; cell + PCM DC-IR ≤ 150 mΩ at 25 °C, ≤ 375 mΩ at 0 °C `[U]`.
- **EV-5 Display interface.** Full frame ≤ 80 ms at 8 MHz; 60 × 60 window ≥ 25 fps; no tearing with TE sync over 1 h; SCK/MOSI overshoot ≤ 10 %; **wake ≤ 200 ms (provisional `[U]`) on 10 boards; RESX/VCI/PMIC ordering on a scope matches E-5.4/5.5**; 1,000 wake/sleep cycles, no latch-up; **RDID read (if SDO wired) or TE-toggle mate check on 10 boards before and after the §7 drop**.
- **EV-6 Charger/gauge.** CC/CV 300 mA, full charge 2.3–2.8 h from 3.45 V; JEITA steps at 10/45 °C; ship-mode exit by crown press and by dock; **0 V cell + dock → charge starts with no firmware (E-2)**; long-press /MR reset restores a hung unit **and does not trigger on the longest legitimate crown hold**; **watchdog: registers unchanged after 10 min docked**; MAX17048 with the INI: SoC ≤ 5 % error.
- **EV-7 Sensors/haptics.** Latch edge → angle valid ≤ 3 ms; first-motion ≤ 77° (§4); sensor rail ≥ 3.02 V at 14 mA; unpowered-sensor bus test; IQS211B 0 false grips per 100 PC3 bursts at B12 (§5 V-4); TACT through the limiter: ≤ 1 µs edge, 0 standing current; DRV2625 ≥ 12 clicks/s on 48 g; purr ≈ 8 mA at 35 %.
- **EV-8 Dock electrical (rewritten).** Detect ≤ 200 ms; **key bridges 10 s each with VBUS live: VBUS–GND, VBUS–SWDIO, VBUS–SWDCLK, SWDIO–SWDCLK — pass = nRF-side net ≤ V3 + 0.1 V, V3 ≤ 3.2 V, injected current into the nRF ≤ the PS limit (`[U]` until opened; measured as the 220 Ω drop), SWD programs at the production clock afterwards**; **reversed head with an active programmer 10 s → no damage; then the keyed cradle proves it cannot happen**; pad ESD-diode C ≤ 15 pF; 30k mating cycles then pad resistance ≤ 100 mΩ (§7); no DRV5032 false latch while docked (§3 C-14).
- **EV-9 SWD/programming throughput.** Image + modem FW through the flex + limiters: ≤ 60 s at the highest clock that passes a 10⁵-transaction error-free run (target 2 MHz; 4 MHz with 2.2 k pull-ups); APPROTECT verified locked after EM-9b (`recover` is the only way in).
- **EV-10 ESD (IEC 61000-4-2).** ± 8 kV contact / ± 15 kV air on dock pads (docked and undocked), cap, crown (current probe on the bleed line), lens centre and edge, lug, split ring; no latch-up, no reset, ≤ 1 lost glance, screen recovers; tail ground bounce on HA1 during the crown discharge ≤ 0.5 V.
- **EV-11 Conducted RF.** `%XRFTEST` through the MM8130: PC3 23 ± 2 dB B12/B2/B4; H2/H3 vs §5 Step 10b; conducted spurs on VSYS/V3/ELVDD screen on vs off; TIS screen-on vs off ≤ 1 dB (§5 V-10, §3 C-10).
- **EV-12 EMC pre-scan (emissions and immunity, missing step 8).** FCC Part 15B radiated screen on/off, LRA on, charger on the dock; conducted emissions on the dock USB; **EU SKU: EN 301 489-1/-52 radiated immunity (80 MHz–6 GHz, 3 V/m class `[U]`) and conducted immunity on the dock cable, ESD per EV-10; the dock itself to EN 55032/55035 `[U]` (§3 C-29).**
- **EV-13 Firmware release gates.** eDRX and PSM both refused → detach and RTC polling within N attempts (mean ≤ 250 µA `[U]`); coverage governor: no cell 24 h → mean ≤ 250 µA; FOTA delta end-to-end incl. modem delta; power-fail during swap → MCUboot reverts; **BQ watchdog disabled in every image (register read in the release test)**.
- **EV-14 Thermal.** 300 mA charge in 40 °C ambient: skin ≤ 45 °C; JEITA WARM engages on the NTC's 45 °C.
- **EV-15 Production-flow dry run (new).** One panel through EM-6a → EM-7a → EM-6b → EM-7b → assembly → EM-9 → EM-9b → recover → re-run, proving the order, the fixture's reset-and-I²C capability, and the locked-unit recovery path before the first DVT lot.

### 6.5 Sourcing (electronics)

**Long-lead / single-source, in order of schedule damage:**
1. **nRF9151-LACA-R** — 16–19 wk `[V?]`; PO at week 0 (§2 P0-1); `-R7` 500-pc for EVM/DVT. No second source.
2. **RM69310 AMOLED module, laminated, 27-pin tail + 0.4 mm B2B** — datasheet + drawing is the EVM-1 entry criterion (P0-5); second module house on the same panel; lead `[U]`; **Tstg and storage conditions on the PO** (§3 C-28).
3. **MFF2 eUICC (SGP.32), Class C 1.8 V** — provider-supplied; supply-shutdown letter and IPA hosting statement before the PO (P0-10, OQ-8).
4. **TPS65631 (or TPS6563x sibling)** — TI single source for the SWIRE/CTRL class `[U]`; qualify an alternate on a dual footprint at DVT; **resistor-set-VNEG alternative identified as the ER-2 fallback**.
5. **MT6701QT-STD** — CN-only; hedged by the AS5600L variant (doc §4.5).
6. **MAX17048** — ADI; custom INI (20 cells to ADI at P0-4).

**Dual-distributed / commodity:** BQ25180, TPS62840, DRV2625, DRV5032DU × 2, TPS22916 × 2 (or one dual), IQS211B00000000TSR (Mouser stock `[V?]` doc), 16 Mbit NOR (Macronix/Winbond/ISSI on one USON-8), PLCC-4 RGB, SOT-523 N-FETs (halo × 3, **limiters × 3 low-Vth**), pad ESD diodes × 2, match/TVS/inductor classes per §5, MM8130-2600, B2B connectors (Panasonic AXT / Hirose BM 0.4 mm; **FH12-10S or -12S-0.5SH `[V]` catalogue extract**, or hot-bar; cell 3-way). Do not substitute DRV2624 (0 stock, doc).

**Doc §4.4 confirm-before-design-in list, updated (replaces the doc's items 1–2 and 7; renumbered; consolidated into §8):**
1. **RM69310 datasheet + panel drawing**: SPI mode/timing, CASET/RASET, tSLPIN/tSLPOUT and whether RAMWR is accepted during tSLPOUT, RESX timing, **SWIRE protocol and whether the burst is emitted after SLPOUT**, **ELVSS abs max vs the PMIC's −4.0 V default**, VCI/VDDIO currents, **Tstg**, tail pin map incl. **SDO presence**.
2. **TPS65631 datasheet**: IQ(off), **IQ(VIN present, CTRL low)**, fSW, inductor, CTRL/SWIRE pulse protocol and tSTART, VNEG step behaviour after enable, VIN range vs the BQ25180 SYS ceiling.
3. **TPS62840 Table 1** — RSET for 3.1 V `[V?]`; 3.2 V availability.
4. **TPS22916 datasheet** — slew at 3.1/4.4 V, off leakage over temperature, WCSP land pattern.
5. **nRF9151 PS chapters**: SPIM fmax and MAXCNT width, **LGA pad pitch and inner-pad count**, pin list (COEX/MAGPIO), ANT DC tolerance, VDD_GPIO drive and **GPIO injection-current limit**, **SIM interface voltage class**; HIG decoupling and SIM filtering; MSL.
6. **MFF2 eUICC: written supply-shutdown statement, Class C (1.8 V), IPA hosting (IPAe/IPAd)** (contractual).
7. **MT6701 electrical table** and AS5600L I/O structure when unpowered; **AS5600L WL-CSP ball pitch**.
8. **BQ25180 SLUSE99C**: /MR pull-up source and voltage, reset-default ICHG, SYS_REG ceiling during charge, input OVP threshold, I²C-watchdog default and disable bit, /MR long-press timing, VIN-side quiescent with charging disabled.
9. **SPI NOR MPN and size vs the modem-delta strategy; RGB LED MPN; halo and limiter FET MPNs (limiter Vth ≤ 1 V); pad ESD-diode MPN (5 V working, ≤ 15 pF); dock B2B and satellite connector MPNs and x-depth.**
10. **Cell energy density** in writing (P0-4).
11. **Dock head MPN + pull force; flex thickness in the swell gap; ASTM B488 plating class** (doc Addendum A.5 items 9–11; §3 C-25).

**Cost deltas (all `[U]`):** display line $10–16 vs $9.00; PMIC + inductor + 2 switches + caps +$1.2–1.8; **limiter cells + pad ESD diodes +$0.15–0.25**; **main PCB with via-in-pad under the SiP $4.3–6.5 at 1k (2+2+2 fallback $6–8) vs the doc's $7.00 lump for PCB + satellite + FFC — the lump holds only on the 1+4+1 + via-in-pad path**; satellite + sensors + tact $3.6 (§4); crown mechanical $16–18 (§4, vs $9.50); cap $4.5–7.3 (§5, vs $6.50); RF match/TVS/switch connector $0.6–1.6 inside the $4.00 passives lump; revised material ≈ $70–79 at 1k (doc $62), $55–63 at 10k. Test NRE: bed-of-nails fixture with SWD reset control + I²C master $6–10k, dock EOL jig $6–12k, RF shield box $3–8k, PPK2 + DK $1k.

### 6.6 Risks (ER-n), ranked by kill-probability × irrecoverability, each with the settling test

1. **ER-1 Dead-battery / ship-mode lockout by a firmware-gated VBUS path (high irrecoverability; eliminated by design).** Test: sheet-5 review against E-2; EV-6 (0 V cell + dock → charge with no firmware).
2. **ER-2 Panel exposure to the PMIC's −4.0 V VNEG default during the SWIRE burst (medium; downgraded from "panel-killing" — unverified exposure).** RM69310 ELVSS abs max `[U]`; TPS65631 enable/step behaviour `[U]`. Test: EV-1 (b) scope on ELVSS at every enable; datasheet check. Fallback: MCU-driven CTRL with the pulse count inside tSTART; resistor-set-VNEG PMIC.
3. **ER-3 Glance energy 8.75–29 mAh/wk `[U]` (high; product rules recover).** Test: EV-1 (b), EV-3. Mitigation: brightness/glance policy, partial windows.
4. **ER-4 MT paging / eDRX not granted (high; product-defining).** Test: EV-1 (c). Fallback: PSM + polling (2.0 wk).
5. **ER-5 nRF9151 availability gates EVM-1 (high schedule).** Test: PO acknowledgement. Fallback: DK mule.
6. **ER-6 Production sequencing — a locked or un-provisionable unit (high irrecoverability; eliminated by EM-9b ordering).** Test: EV-15 dry run incl. recovery.
7. **ER-7 SiP LGA escape on 0.8 mm (medium; fab-dependent).** Pitch `[U]`. Test: fab DFM on the rev A Gerbers; X-ray on lot 1. Fallback: 2+2+2.
8. **ER-8 Screen-off current not zero (medium).** Back-powering, switch leakage, PMIC IQ. Test: EV-3 node ≤ 0.2 µA. Fallback: park audit, switch B (in).
9. **ER-9 SWD limiter cell slows programming or mis-reads at 4 MHz (low–medium; throughput).** Test: EV-1 (g), EV-9. Fallback: 2.2 k pull-ups; 2 MHz; a second B2B-side pull-up only while docked (VIN-good-gated, `[U]`).
10. **ER-10 /MR pull-up domain above VDD_GPIO (medium; eliminated by the limiter, but the satellite tact trace carries it).** Test: EV-2 TACT idle voltage; SLUSE99C. Fallback: none needed if the limiter passes EV-7.
11. **ER-11 SPIM 8 MHz `[V?]` and partial-window support `[U]` (medium; UI).** Test: EV-1 (a), EV-5. Fallback: smaller window, 13 fps full-frame.
12. **ER-12 AMOLED PMIC desense (medium).** Test: EV-11 TIS Δ ≤ 1 dB; EV-12. Fallback: can, inductor change.
13. **ER-13 Crown ESD return through one FFC ground (medium; satellite respin).** Test: EV-10 HA1 probe. Fallback: 12-way tail.
14. **ER-14 VSYS docked ≈ 4.43 V vs PMIC VIN 4.5 V max (medium; PMIC stress).** Test: EV-2 docked ceiling. Fallback: VSYS_REG programmed lower; PMIC sibling.
15. **ER-15 0 °C brownout on TX (medium; field).** Test: EV-4. Fallback: cutoff 3.5 V, PC5.
16. **ER-16 BQ25180 watchdog silently reverting ICHG/JEITA (medium; eliminated in firmware).** Test: EV-6 10-min read-back, EV-13.
17. **ER-17 Coverage-search governor absent (high irrecoverability, low probability).** Test: EV-13.
18. **ER-18 eSIM without supply shutdown, or wrong voltage class (+7 mAh/wk or a non-working SIM).** Test: letter + EV-1 (d); Class C on the PO.
19. **ER-19 Debug UART left on (+100 mAh/wk).** Test: EV-3 with the positive control.
20. **ER-20 Sealed-unit EOL cannot see a 10 µA-class leak (low; accepted).** Only the golden unit and the bare-PCBA test see it; ORT samples measured cell-side after opening.
21. **ER-21 Sensor I²C clamping when unpowered (low).** Test: EV-7. Fallback: TWIM1.
22. **ER-22 MAX17048 without the INI (low; UX).** Test: INI before DVT.
23. **ER-23 Lens/panel ESD (low–medium).** Test: EV-10. Fallback: ink border/ITO.
24. **ER-24 0.4 mm-pitch WCSP/DSBGA yield (low).** Test: EM-3 X-ray. Fallback: SOT-23-5 switch in the side strip.
25. **ER-25 GPIO budget (low; 26/32).** Test: schematic count. Fallback: I²C expander on LED gates.

### 6.7 Open questions (electronics)

1. **OQ-1** nRF9151 SPIM maximum clock (8 MHz `[V?]`) and TXD.MAXCNT width — PS SPIM chapter (docs.nordicsemi.com returned 403 on the previous pass); Mule A measures on the DK (EV-1 a).
2. **OQ-2** RM69310: SPI mode/timing, CASET/RASET, tSLPIN/tSLPOUT and whether RAMWR is accepted during tSLPOUT (the 135–160 ms estimate depends on it), RESX timing, SWIRE burst semantics (emitted after SLPOUT? enables and programs in one burst?), ELVSS abs max vs the PMIC's −4.0 V default (ER-2), VCI/VDDIO currents, Tstg, 27-pin map incl. SDO — no datasheet or drawing in the project; settled by the panel documents + EV-1 (b).
3. **OQ-3** Does the nRF9151 expose MAGPIO0–2 or only COEX0–2? Decides whether `%XMAGPIO` provisioning in §5 M12 / EM-7b is real — PS pin list (§3 C-27).
4. **OQ-4** TPS65631: IQ(off), IQ(VIN present, CTRL low), fSW, inductor, CTRL/SWIRE pulse protocol and tSTART, VNEG stepping after enable; resistor-set-VNEG alternative and second source — datasheet + EVM (EV-1 b, EV-2).
5. **OQ-5** TPS22916: off leakage and slew at 3.1 V and 4.4 V input; a dual-channel equivalent — datasheet.
6. **OQ-6** TPS62840 Table 1: RSET for 3.1 V `[V?]` and 3.2 V availability (§3 C-13).
7. **OQ-7** BQ25180 (SLUSE99C not in the project): /MR pull-up source and voltage (decides whether the TACT limiter is strictly necessary and what the satellite tact trace sees), reset-default ICHG, SYS_REG ceiling during charge vs the PMIC's 4.5 V VIN max (ER-14), input OVP threshold (sets the VBUS TVS), I²C-watchdog default and disable, /MR long-press timing vs the longest legitimate crown hold, VIN-side quiescent with charging disabled (EM-9 reference) — settled by the datasheet + EV-2/EV-6.
8. **OQ-8** MFF2 eUICC: MPN with a written supply-shutdown statement, Class C (1.8 V) confirmation, and which entity hosts the SGP.32 IPA (eUICC IPAe / modem / application IPAd) — decides whether EM-9 needs a live attach for the profile download.
9. **OQ-9** SPI NOR MPN and 16 vs 32 Mbit vs modem-delta-only FOTA; asset budget from the art list.
10. **OQ-10** MT6701 / AS5600L SDA/SCL structure when VDD is off — TWIM1 vs shared bus (EV-7).
11. **OQ-11** Satellite tail 10-way vs 12-way with two grounds; FH12-10S/-12S x-depth (not in the catalogue extract) vs the 3.0 mm strip; rating of the tact conductor for the /MR-domain voltage (§3 C-24).
12. **OQ-12** Dock pad plating: ASTM B488 Type II Code C ≥ 0.76 µm over ≥ 2.5 µm Ni vs the doc's Ni 1.0–2.5 µm — standard to be opened; head MPN and pull force; flex thickness in the swell gap; pad ESD-diode capacitance; whether the 2.54 mm pitch has a vendor drawing (retag from `[U]`) (§3 C-25).
13. **OQ-13** Panel current per glance (6–20 mA cell-side `[U]`) and the glance/brightness policy — Mule A.
14. **OQ-14** The doc's 92.6 µA `[V?]` eDRX line vs the PS's 18 µA `[V]` — Mule A (EV-1 c).
15. **OQ-15** Lens/panel ESD at 15 kV air through 0.50 mm glass + OCA — EV-10.
16. **OQ-16** Nordic HIG values for VDD decoupling, SIM filtering, high-drive pins; PS GPIO injection-current limit (EV-8 criterion) and LGA pad pitch/inner-pad count (E-11 escape rule) — HIG/PS not opened.
17. **OQ-17** Whether PC3/PC5 is field-switchable or certification-fixed (§5 Step 1).
18. **OQ-18** SWD limiter cell: highest error-free SWD clock through 220 Ω + FET + 4.7 k (or 2.2 k) pull-up over the flex — EV-1 (g)/EV-9 on the DK; decides the production programming time budget (≤ 60 s).
19. **OQ-19** Whether a sealed-unit EOL VBUS-side screen at Δ ≤ +50 µA is stable enough across the BQ25180 VIN-side quiescent spread (10-unit characterisation in EV-3) or the EOL sleep step should be dropped in favour of ORT cell-side sampling (§3 C-23).
20. **OQ-20** Product-story items for the owner (§8 D-1): screen wake ≈ 135–160 ms `[U]` with a ≤ 200 ms acceptance (not 15 ms); "arrival stays on screen" replaced by the halo; glance brightness policy.

---

## 7. Mechanical system, sealing, cell & final assembly — domain report (revision 2)

*Frame: body X. Editor notes in italics mark §3 resolutions — C-2 (crown module inserted from inside; J5 is a face seal on the sleeve flange/ears; Step 12 superseded by §4 except the interface freeze), C-3 (J6 squeeze 3–6 %), C-5 (J9 = sealed tab aperture, PCB substrate to 68.0), C-6 (feed-land plating per §5 M4), C-15 (debris pockets), C-17 (lug).*

### 7.1 Disposition of the hostile review

| # | Finding | Disposition | Where fixed |
|---|---|---|---|
| 1 | Lid opening 21 mm — PCB/cell cannot pass (BLOCKING) | **Accepted.** Lid re-architected: full-width rear door, LSR bead gasket on the 1.2 mm wall rim, perimeter stiffening rib inside the wall that also locates the cell laterally. | Steps 1, 3, 8 (J1) |
| 2 | Z-table arithmetic; shim and lid ribs missing | **Accepted.** Table rebuilt column-by-column with x-ranges; shim + flex + PSA row added; lid ribs deleted from the cell face (side ribs). 6.0 mm cell becomes baseline. | Step 6 |
| 3 | Gasket 103 % groove fill, snaps 60 N vs 60–70 N gasket, no altitude load, lid deflection | **Accepted.** No groove: over-moulded bead on the lid, 30 % squeeze, retention budget 2 × (gasket + 26 kPa) ≈ 230 N, lid rib, IEC 60068-2-13 altitude test added. | Step 8 (J1), Verification |
| 4 | Generic TPV does not bond PC/ABS; compression-set spec unmeetable | **Accepted.** Self-adhesive LSR baseline; the only TPV allowed is a PC/ABS-bonding grade (Santoprene 8211-55B100 — TDS opened: 53 Shore A, compression set 55 % at 125 °C/70 h, no 70 °C value `[V]`) with a relaxed set limit and a DVT reseal test. | Step 2, 8 |
| 5 | MMA adhesive on optical PC; DP8005 is an LSE-plastics adhesive; ring skirt collides with the PCB | **Accepted.** DP8005 TDS confirms LSE/polyolefin family `[V]`. J4 moves to PC-safe 2K epoxy (or light-cure acrylated urethane with the Henkel TDS warning `[V]`) plus an ESC screen; PCB shortened to X = 68. The RF feed feedthrough is added as J9 (*redefined per §3 C-5*). | Steps 2, 8 |
| 6 | Lens ledge 1.0 mm cannot carry a 1.2 mm PSA; lens can be proud | **Accepted.** Lens 16.0 × 34.0, ledge 1.5 mm/side, PSA 1.3 mm, nominal −0.08 ± 0.05 sub-flush. | Step 4 |
| 7 | Hot-bar after lens bonding is a sequence contradiction | **Accepted.** Vendor-laminated module with a 0.4 mm-pitch B2B on the panel tail, mated *through the display aperture* before the lens seats, foam hold-down; Z cost booked (0.70 mm at X = 46–49). Drop-qualified at EVM-1. | Steps 4, 6, Phase 3 |
| 8 | LRA cut-out slots the counterpoise; RF cost unpriced | **Accepted.** Top-side LRA + 6.0 mm cell is the baseline; cut-out + 6.5 mm cell is an RF-gated option measured on Mule B. | Steps 5, 6, 9 |
| 9 | LRA PSA-bonded to the cell defeats Art. 11 and drives the pouch as a diaphragm | **Accepted.** LRA reacts against PCB + bracket only; ≥ 0.3 mm gap to cell face and to both shells. | Step 9 |
| 10 | Insert torque-out 5 N·m off by 20×; preload > pull-out; nylon patch | **Accepted.** T3 limit 0.14–0.18 N·m confirmed on the Wiha table `[V]`. Seating torque 0.025 N·m (≈ 90 N), pull-out ≥ 2 × preload, torque-out ≥ 3 × seating, no patch, torque + angle. | Step 10 |
| 11 | 12 mm journal vs 2.0 mm crown-zone budget (doc inconsistency) | **Accepted and flagged.** Resolved by §4 (6.9 mm two-land journal, 0.8°). | Step 12 → §4 |
| 12 | Grip electrode feedthrough missing; crown sub-assembly missing | **Accepted, with a better answer:** the electrode is *inside* the wall (insert-moulded/LDS ring 0.8–1.0 mm behind the shoulder), so there is no feedthrough. Crown-module sub-assembly sequence added (→ §4 M-16…M-23). | Step 8 (J8), Phase 3A |
| 13 | Connector placement on the PCB rear at X = 16–18 never laid out; FFC connector height not in Z | **Accepted.** Cell moved to X = 19–62 (3 mm strip), placement sketch and a Z column D added. | Steps 5, 6, 11 |
| 14 | Pressure decay at 1 × 10⁻³ is at the method floor; tracer gas recommended | **Accepted — and the spec itself changes.** INFICON gives 5 × 10⁻³ "no water" for ABS/steel-with-polymer-seal channels and 2 × 10⁻⁴ for aluminium/polymer `[V]`; 1 × 10⁻³ retained as the *product* limit. Method: pressure-decay gross screen + helium bombing/vacuum-chamber fine test. The "pressure trapped in the debris chamber" retest rule is deleted. | Phase 4 |
| 15 | AMOLED mechanicals over-tagged | **Accepted.** All AMOLED mechanicals → `[V?]`; panel drawing is an EVM-1 entry criterion. | Overview, Step 4 |
| 16 | Lid ribs on the cell face | **Accepted.** Side ribs/pockets only; lid flat over the cell; vendor's local-pressure number requested. | Steps 3, 7 |
| 17 | FKM at −20 °C | **Accepted in part.** Low-temperature FKM (GLT/GFLT class) or PTFE-filled silicone; cold torque/press tests added; TR10 `[U]`. | Steps 2, 8 |
| 18 | +80 °C/4 h invented; 85/85 will kill the AMOLED; JEITA sentence self-contradictory | **Accepted.** UN 38.3 T2 opened: 72 ± 2 °C ≥ 6 h `[V]` is the anchor, 80 °C a stretch test; 85/85 on coupons only; JEITA rewritten from SLUSE99C `[V]`. | Step 15 |
| 19 | IP6X category conflation; 60068-2-52 is cyclic | **Rebutted in part on IP6X:** two lab summaries state IP6X is tested by the category-1 (vacuum) method; standard not opened → `[V?]`. **Accepted on salt:** 60068-2-11 Ka is continuous; 60068-2-52 Kb is cyclic. | Verification |
| 20 | 17-4PH mechanism mis-stated; no primary source | **Accepted on mechanism, source now primary:** ATI 17-4 TDS: "Strongly Ferromagnetic in all Conditions" `[V]`. Risk restated as field-amplitude loss at the DRV5032/MT6701. *Race choice per §3 C-1.* | Step 2, Risk 4 |
| 21 | EVM-1 CNC tub non-representative; 2-shot Al LSR tool unrealistic; hard tools oversized | **Accepted.** EVM-1 on quick-turn aluminium tools; LSR gasket as a separate part until DVT; hard tooling sized 1+1 P20 at ~100k shots with the cost delta presented as a decision. | Phase 1 |
| 22 | 650 mAh from a reseller page is `[U]`; bare-cell scaling overstates | **Accepted.** Bands: 6.0 mm → 560–620 mAh, 6.5 mm → 600–660 mAh, all `[U]`; runtime run at 600 conservative. | Steps 6, 7 |
| 23 | Cert samples from PVT slips MP; missing slot RF, ESC, UV, altitude | **Accepted.** Pre-scans on DVT RF-frozen units; final cert on PVT; ESC/UV/altitude added. | Verification |

### 7.2 What this subsystem is

The sealed capsule everything lives in: an opaque PC/ABS **front tray** (front face with the display aperture, both 15 mm flanks, crown-end bulkhead with the reamed ø13.30 crown bore and the buried grip-electrode ring, antenna-end wall at X ≈ 68–71) closed on the rear face by a **full-width screwed + snapped rear lid** carrying an over-moulded LSR bead gasket, the dock pads and the 430 shim; a **0.50 mm chemically strengthened glass lens** OCA-laminated by the display vendor to the 1.1" AMOLED and PSA-bonded into the tray aperture from outside; a **clear-PC ring-disc** (halo light guide, H-section with a full web and a sealed aperture for the cap's feed tab) that carries the 6061-T6 antenna cap; the **crown cartridge** (§4) inserted from inside through the bulkhead bore with the only dynamic seal in the product; a **23 × 43 × 6.0 mm (option 6.5 mm) pouch cell** on a connector; the **LRA on a bracket reacting against the PCB**, with air gaps to the cell and both shells.

Crown geometry baseline: **coaxial twist** (§9.4 open pending Mule C); Step 12 states which tray features are dual-compatible.

### 7.3 The numbers that govern it

| # | Number | Value | Tag |
|---|---|---|---|
| 1 | Internal thickness behind 1.2 mm walls | 12.6 mm | `[V]` arithmetic on doc §6.2 |
| 2 | AMOLED module thickness / outline / active area / pins | 0.784 mm; 12.96 × 30.94; 10.962 × 25.578 mm; 27-pin FPC; −20…+70 °C operating | **`[V?]`** vendor product page only — no drawing |
| 3 | Z returned vs the Winstar-worst-case MIP stack | 2.08 + 0.60 − 0.78 = 1.90 mm | **`[V?]`** arithmetic on the doc's disputed 2.08 mm outline |
| 4 | Cell capacity bands in 23 × 43 (incl. PCM/wrap, 50 % SoC) | 6.0 mm: **560–620 mAh**; 6.5 mm: **600–660 mAh** | **`[U]`** scaled from reseller/vendor datapoints; vendor quote required |
| 5 | Governing Z margins (Step 6) | 6.0 mm cell, LRA top-side: **C′ = 0.70 mm** (governs); SiP column 1.87; display+shim 2.17. 6.5 mm cell: C′ = 0.20 (fails the 0.3 floor) → needs the RF-gated LRA cut-out (C = 0.90) | `[V]` arithmetic; inputs tagged in the table |
| 6 | Drop energy 1.5 m | 0.71 J at 48 g; 0.74 J at ~50 g | `[V]` arithmetic |
| 7 | IP67 test conditions | IPX7: 0.15 m above top / 1 m at bottom, 30 min; IP6X: category-1 method, ≤ 2 kPa depression, 80 volumes, 2 h (40–60 vol/h) or 8 h | **`[V?]`** two accredited-lab summaries, standard not opened |
| 8 | Product air-leak limit | **1 × 10⁻³ mbar·L/s at 100 mbar Δp** — INFICON gives 5 × 10⁻³ "no water" for ABS/steel + polymer-seal channels and 2 × 10⁻⁴ for aluminium + polymer channels; our joint families span both | `[V]` INFICON application note miaq00en-03 |
| 9 | Pressure-differential design loads on the lid | aircraft hold ~26 kPa × ~1650 mm² ≈ 43 N; +60 °C sealed internal ≈ 14 kPa ≈ 23 N; gasket reaction ≈ 70 N | `[U]` engineering estimate |
| 10 | EU 2023/1542 Art. 11 | applies 18 Feb 2027; end-user removable with commercially available tools or a specialised tool provided free with the product; "an IP rating alone is considered as not sufficient" for the wet-environment derogation; five cumulative indicators | `[V]` EUR-Lex 32023R1542 Art. 11 + **C/2025/214** for the derogation/tools text; the 18 Feb 2027 date via secondary summaries → `[V?]` |
| 11 | OCA thickness | 8146-5 = 125 µm `[V]` 3M TDS; 8146-6 = 150 µm `[V]` |
| 12 | BQ25180 JEITA defaults | COLD 0 / COOL 10 / WARM 45 / HOT 60 °C; COOL → ICHG × 0.5 (or 0.2); WARM → VREG −100 mV (or −200 mV); charging + timers suspended below COLD / above HOT; HOT selectable 45/50/60/65 °C | `[V]` SLUSE99C |
| 13 | UN 38.3 | T1 ≤ 11.6 kPa ≥ 6 h; T2 72 ± 2 °C ≥ 6 h ↔ −40 ± 2 °C ≥ 6 h, ≤ 30 min transition, 10 cycles, 24 h rest; pass = no leak/vent/rupture/fire, OCV ≥ 90 % | `[V]` UN Manual §38.3.4.1–2 |
| 14 | Torx T3 tool torque limit | 0.14–0.18 N·m | `[V]` Wiha table |
| 15 | 17-4PH | "Strongly ferromagnetic in all conditions"; martensitic | `[V]` ATI 17-4 TDS |
| 16 | Static gasket squeeze | 25–30 % face-seal bead; *rotary O-ring per §4 (3–6 %, Parker §8.13 `[V]`)* | `[U]` face-seal practice |

Inconsistencies in the primary source, corrected: (a) §6.2 puts the cell at X = 24–67 and the LRA at 55–69 while §3/§6.3 forbid any cell within 10 mm of the ring and metal within the 8 mm zone (§3 C-8); (b) the split ring is called "PC/ABS" yet must be a light guide — PC/ABS is opaque, the ring is optical PC; (c) the detent race is "hardened 17-4PH" — strongly ferromagnetic `[V]` (§3 C-1); (d) §4.3 specifies a 12 mm POM journal while §6.2 allots 2.0 mm to journal/hub (§3 C-2).

### 7.4 DESIGN — sequenced

#### Step 1. Enclosure architecture and parting lines (before any CAD)

**Architecture: tray + full-width rear door.** The front tray is a closed tub: front face (display aperture), both 15 mm flanks, crown-end bulkhead (reamed ø13.30 +0.05/−0 crown bore with two wide-face debris pockets and two ear pockets on its inside face — §4 Design step 8, §3 C-2/C-15; the buried grip-electrode ring), antenna-end wall at X ≈ 69.8–71.0 with the ring-disc bonded on its outside. The rear lid covers the whole rear face between the crown-end collar and the antenna-end wall: **lid outline 27.0 × 67 mm (X = 2–69), 1.2 mm thick over the cavity; the opening it closes is the full 24.6 × 66 mm internal section**, so a 23.0 ± 0.3 mm cell and a 23.0 mm PCB pass with ≥ 0.5 mm per side — and the crown cartridge (sleeve flange ø13.20, satellite PCB 22 × 10) is inserted through this opening crown-first into the bulkhead bore before the lid closes. The lid edge is on the rear-face corner — a drop-edge parting line — mitigated by (i) the tray flank continuing to the rear face with the lid edge inset 0.3 mm and chamfered, (ii) the corner R4 on the tray only, (iii) the perimeter rib inside the wall (Step 3) which makes the lid edge stiffer than the wall. `[U]` design choice. Reasons for tray + door: one seal on one flat rim; the lid *is* the Art. 11 battery door; the front face, both flanks and both ends are monolithic.

Parting lines / joints (details in Step 8):
- PL1 / **J1**: lid ↔ tray rim (over-moulded LSR bead face seal, snaps + 2 screws, user-openable).
- PL2 / **J5**: crown cartridge ↔ tray bulkhead (*static face seal on the sleeve flange/ears against the bulkhead inside face, §3 C-2*); the cosmetic crown-end collar snaps on outside and hides the two lid screws.
- PL3 / **J4a/J4b**: ring-disc ↔ tray end wall, ring-disc ↔ 6061 cap (permanent, PC-safe structural adhesive) and **J9**: the cap's feed tab through the sealed aperture in the ring web (§3 C-5).
- PL4 / **J2**: lens ↔ tray aperture (permanent PSA frame).
- PL5 / **J3**: dock pads ↔ lid (permanent PSA + UV bead).
- **J6**: crown rotary/press dynamic seal (§4 Design step 8, optional). **J7**: keyring lug (insert-moulded in the tray flank). **J8**: grip electrode (internal — no feedthrough).

Length budget: crown zone 0–16; main PCB **16–68** (X = 63–68 copper-free; the ring skirt occupies 68–71); ring-disc web 71–72.5 with skirts 68–71 (inside the tray end) and 72.5–75.5 (inside the cap bore); cap 72.5–95.

#### Step 2. Material selection

| Part | Material | Why | Tag |
|---|---|---|---|
| Front tray, rear lid | **PC/ABS**, UV-stabilised, moulded-in colour (Covestro Bayblend T85 XF / SABIC Cycoloy C2950 class) | ABS-modified PC survives the 0.74 J corner drop; better ESC resistance than PC against sunscreen/DEET/sanitiser; HDT ~100–110 °C covers 72 °C dashboard; shrinkage 0.5–0.7 %; 1.2 mm walls at ~55:1 flow ratio. Rejects: PC (ESC), PA-GF (hygroscopic), PC-GF (brittle in drop). | `[U]` grade properties — TDS at CAD start; **ESC screen in DVT** |
| Ring-disc | **Optical-grade PC** (Makrolon LED2245 / Lexan LS2 class), UV-stabilised | Must transmit; must carry the 8 g cap. PC/ABS is opaque. | `[V]` PC/ABS opacity; grades `[U]` |
| Lid gasket | **Self-adhesive LSR, 40–50 Shore A** (Dow SILASTIC / Momentive Silopren self-bonding classes), 2-shot onto PC/ABS | Only elastomer family with compression set ≤ 20 % (70 °C/22 h) and self-bonding to PC/ABS. **TPV option only if a PC/ABS-bonding grade is used:** Santoprene 8211-55B100 `[V]` with a relaxed set limit (≤ 40 % at 70 °C/22 h `[U]`) proved by the 10-cycle reseal test. Fallback: loose die-cut/moulded LSR gasket keyed in the lid recess and included in the spare kit. | LSR grade `[U]` |
| Crown rotary O-ring (J6, optional) | **Low-temperature FKM (GLT/GFLT class) 75–80 ShA** or PTFE-filled silicone; 1.0 mm CS; PFPE grease | Standard FKM stiffens near −20 °C (TR10 ≈ −15…−18 °C `[U]`); *squeeze and gland per §4 (3–6 %, Parker §8.13)* | `[U]` |
| Static seal (J5) | Silicone or LSR 50 A face-seal ring on the sleeve flange/ears, 25–30 % squeeze | static, no abrasion | `[U]` |
| Crown | *Per §4 / §3 C-16: 316L one-piece crown+hub with cut serrations, µr ≤ 1.05 lot gate; Ti Gr5 control and fallback; brass rejected* | | |
| Detent race | *Per §3 C-1: wrought 17-4PH H900, Y-TZP zirconia and C17200 TH04 all built for Mule C; 17-4PH is "strongly ferromagnetic in all conditions" `[V]` ATI TDS* | | |
| Detent balls | Si₃N₄ ø0.8 Grade 5/10 | per doc/§4 | `[U]` |
| Leaf springs, wave washer, C-ring, bleed leaf | BeCu C17200 photo-etched / wire, age-hardened | non-magnetic | `[U]` |
| Sleeve/journal | POM-C moulded + one-chucking secondary (§4 M-14) | low friction, no lubricant against 316L/Ti | `[U]` |
| LRA bracket | 0.20 mm brass C26000 stamping, solderable, ending ≤ X = 61 (polymer preferred by §5) | non-magnetic; ≥ 10 mm from the ring | `[U]` |
| Keyring lug | 316L 1.0 mm stamped, insert-moulded in the tray flank at X ≈ 8–14 (§3 C-17) | zero axial length (doc) | `[U]` |
| Screws / inserts | 2 × M1.4 × 3.0 Torx T3 pan, A2/316, **no patch**; brass heat-set M1.4, OD 2.3 × L 3.0 (marketplace-grade; fallback M1.6 mould-in) | Step 10 | `[U]` — no tier-1 M1.4 heat-set datasheet |
| Dock shim | 0.3 mm 430 ferritic SS as the dock-flex stiffener (baseline) or insert-moulded (fallback) | Step 11 | `[U]` |
| Ring adhesive (J4/J9) | **PC-safe 2K clear epoxy** (Loctite EA E-30CL / 3M DP100 Plus Clear class) baseline; light-cure acrylated urethane (Loctite AA 3106 class) alternative where the ring transmits UV | Methacrylate/MMA and DP8005 (an LSE/polyolefin acrylic `[V]` 3M TDS) rejected for ESC on optical PC; Henkel AA 3106 TDS: "plastic grades should be checked for risk of stress cracking" `[V]` | grade `[U]`; ESC screen mandatory |

#### Step 3. Wall, rib, boss, hold-down rules

- Nominal wall 1.2 mm (tray and lid); local 1.5 mm around the lens pocket and the crown bore (0.70 mm minimum on the 15 mm faces at the debris pockets, §3 C-15). Ribs ≤ 0.6 mm (50 % of wall) under textured A-surfaces; rib height ≤ 3 × wall. Draft 1° untextured, 2–3° textured (VDI 27–30). Radii ≥ 0.4 inside, ≥ 0.6 outside. `[U]` standard DFM.
- **Lid perimeter rib:** 0.6 mm thick × 1.5 mm tall on the lid inner face at y = ± 12.0 (just inside the tray flank wall, in the 0.8 mm channel between cell edge and wall), full length; plus one at the antenna end. Functions: (i) stiffens the lid edge so gasket unloading between hooks is < 25 % of squeeze (estimate < 0.03 mm at 11 mm hook pitch; FEA before tool cut `[U]`); (ii) **locates the cell laterally by its edges — no rib ever touches a pouch face**; (iii) carries the snap-hook catches. The lid inner face over the cell is flat.
- Screw bosses: hole ø2.00 +0.05/−0 for the OD 2.3 insert, boss OD ≥ 4.2, height 3.5 with 0.5 relief, cored from outside; at X ≈ 3–6, y = ± 8, hidden by the crown-end collar.
- **PCB location and hold-down:** four ø1.6 pins on the tray inner face into PCB tooling holes at the crown end, a slot at X = 66 (axial float 0.2); **Z clamp** by two 0.6 mm tray ribs bearing on the PCB top-side edges at X = 30 and X = 60 (outside the display and the connector zones) and by the lid perimeter rib ends bearing on the PCB rear-side edge strip (0.5 mm wide, copper-free) — the PCB is thereby clamped between tray and lid with 0.05–0.10 mm interference through the gasket's compliance, so a drop never loads the display module or the B2B. No metal fastener in the PCB. *The feed finger under the cap tab is compressed as the PCB seats on the ribs (§5 M13).*
- Cell pocket: located by the lid perimeter ribs (long edges) and by two 0.6 mm tray-flank stubs at X = 19 and X = 62 (ends); free on the lid side into the swell gap; bonded on the PCB-side insulator only (Step 7).

#### Step 4. Display aperture and lens bonding stack

Stack (outside → in): **0.50 mm chemically strengthened aluminosilicate lens** (Corning GG3/GG5, AGC Dragontrail, Schott Xensation class; CS ≥ 600 MPa, DOL ≥ 30 µm — `[U]`, on the lens drawing) → **OCA 3M 8146-5 125 µm `[V]` or 8146-6 150 µm `[V]`** → AMOLED module 0.784 mm `[V?]`.

- **Lens 16.0 × 34.0 mm**, corners R1.5, 2D CNC-ground edge with 0.15 × 45° chamfer, black ink border 2–3 pass (OD ≥ 4) leaving a 11.6 × 26.2 clear window (active 10.962 × 25.578 + 0.30/side), AF coating outside. Lens overhangs the 12.96 × 30.94 panel by 1.5 mm per side and end — covers the panel's non-active border (≈ 1.0 sides, ≈ 1.3 top, ≈ 4 mm COG end — **`[U]` until the panel drawing is in hand; EVM-1 entry criterion**).
- **Tray pocket:** through-aperture 13.3 × 31.3 (panel + 0.15/side); ledge **16.3 × 34.3, i.e. 1.5 mm wide**; ledge depth **0.71 mm** = 0.50 lens + 0.13 PSA + **0.08 nominal sub-flush**; tolerance stack (lens ± 0.03, PSA ± 0.01, ledge ± 0.03) → lens sits −0.03 to −0.13 below the tray face, **never proud**. Local front wall 1.5 mm → 0.79 mm under the ledge. Ledge flatness ≤ 0.05; no gate vestige on the ledge. `[U]`
- **J2 lens seal:** single die-cut PSA frame, 3M 300LSE (9472LE, 0.13 mm) or Tesa 61xx, **1.3 mm wide** on the 1.5 mm ledge (0.1 positional margin each side). Altitude/thermal pressure on the lens: 26 kPa × 495 mm² ≈ 13 N over 125 mm² of PSA → 0.10 MPa in tension — within PSA capability `[U]`; verify in the altitude test.
- **Panel tail termination — decision:** the display vendor delivers lens + OCA + panel laminated **with the 27-pin tail terminated in a 0.4 mm-pitch low-profile B2B plug** (Panasonic AXT/Hirose BM-series class, mated height ≤ 0.70 mm; MPN `[U]`). The receptacle sits on the PCB top side at **X = 46–49**, under the panel end, *reachable through the display aperture*; the tail folds 180° at X = 49–51 (bend radius ≥ 0.5). The 0.20 mm foam pad under the panel doubles as the connector hold-down. Drop-qualified at EVM-1; the hot-bar/ACF path is the fallback if the B2B shows intermittents (then the panel is soldered to the PCB on the bench and the lens laminated in-line — a clean-room move to the CM; costed in Sourcing as an option).
- EXTCOMIN/RTC machinery is gone; ELVDD/ELVSS PMIC (TPS65631 class, 3 × 3 WSON) and its inductor live in the 5.8 mm strips beside the panel (≈ 4.85 mm headroom, §6 E-12).

#### Step 5. Revised layout along X (drives the Z columns)

- Panel X = 18–49; tail B2B X = 46–49 (under panel); fold X = 49–51.
- **nRF9151 at X = 20–32** (top side, under the panel), so it is never over the shim or the fold.
- **Dock pads X = 34–44** (4 × ø2.0 at 2.54 mm pitch = 9.6 mm span); **shim X = 33–45** (12 × 8 mm) — > 20 mm from the Hall latches at X ≈ 10.5, > 26 mm from the ring; not under the SiP, not under the B2B.
- **LRA X = 52–60** top side (baseline) with bracket X = 51–61; RGB PLCC-4 X = 62–63, spring finger X = 65.5–67.5 (§3 C-5); zero-copper X = 63–68; PCB substrate ends at 68.
- **Cell X = 19–62** (PCM head at the crown end), leaving a **3.0 mm connector strip at X = 16–19** on the PCB rear side (Step 11) — 9 mm from the ring: the doc's 10 mm keepout is itself `[U]`; Mule B measures **19–62 and 24–67** (§3 C-8).
- Tall top-side parts (2 × 0805 22 µF 1.45 mm, AMOLED PMIC + inductor, NOR, eSIM, TPS62840) go in the 5.8 mm strips beside the panel.

#### Step 6. Revised Z-stack (12.6 mm internal), mm — each column sums only what exists at its x-range

| Layer | A1 display + shim (X = 34–45) | A2 display + B2B (X = 46–49) | B SiP (X = 20–32) | C′ LRA top-side (X = 52–60) **baseline** | C LRA in PCB cut-out (X = 52–60) **RF-gated option** | D FFC connector under panel edge (X = 16–19.5) | Tag |
|---|---:|---:|---:|---:|---:|---:|---|
| Glass lens (in the front wall) | 0.50 | 0.50 | 0.50 | — | — | 0.50 | `[U]` doc design choice |
| OCA | 0.15 | 0.15 | 0.15 | — | — | 0.15 | `[V]` 3M |
| Frontlight | 0 | 0 | 0 | — | — | 0 | decision 2026-09-19 |
| AMOLED module | 0.78 | 0.78 | 0.78 | — | — | 0.78 | `[V?]` vendor page |
| Foam under panel | 0.20 | 0.20 | 0.20 | — | — | 0.20 | `[U]` |
| Top-side: components / B2B / SiP+solder / LRA+bracket / FFC conn. | 0.70 | 0.70 (B2B) | 1.35 | 4.05 + 0.30 | 4.05 + 0.20 | 1.50 (2.0 if FH12-10S) | SiP `[V]` PS; LRA `[V?]` vendor page; connectors `[U]` |
| PCB | 0.80 | 0.80 | 0.80 | 0.80 | 0 (cut-out) | 0.80 | doc |
| Insulator PET + PSA | 0.15 | 0.15 | 0.15 | 0.15 | 0.15 | — (no cell here) | `[U]` |
| Cell | **6.00** | 6.00 | 6.00 | 6.00 | **6.50** | — | `[U]` quote |
| Swell gap (kept free) | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | — | `[U]` 10 % practice |
| Dock flex on lid (0.1 flex + 0.1 PSA) | 0.20 | 0.20 | 0.20 | 0 (tail not routed here) | 0 | 0.20 | `[U]` |
| Shim 0.30 + PSA 0.05 (local) | **0.35** | — | — | — | — | — | `[U]` |
| Rear-side connectors (cell B2B, dock B2B) | — | — | — | — | — | 0.70 | `[U]` |
| **Total** | **10.43** | **10.08** | **10.73** | **11.90** | **11.70** | **4.83** | |
| **Margin (6.0 mm cell)** | **2.17** | 2.52 | 1.87 | **0.70** | — | 7.77 | |
| Margin with 6.5 mm cell | 1.67 | 2.02 | 1.37 | **0.20** (0.00 if the flex tail is routed under) | **0.90** | — | |
| Margin with 7.0 mm cell | 1.17 | 1.52 | 0.87 | **−0.30** | 0.40 | — | |
| Worst case if placement rules are violated (fold + shim over SiP) | | | 0.42 (6.5) / 0.92 (6.0) | | | | |

Findings: (1) **C′ governs.** With the doc's top-side LRA the ceiling is a **6.0 mm cell (0.70 mm margin)**; a 6.5 mm cell leaves 0.20 mm — below the 0.3 mm build-tolerance floor — so 6.5 mm is only available with the LRA recessed into a PCB cut-out, which is an RF decision (Mule B, with and without the slot; if B12 efficiency drops > 1 dB the cut-out is dead). (2) The display and SiP columns are no longer critical (1.9–2.5 mm) — this is the height budget §6 E-12 uses for under-panel and side-strip parts. (3) The placement rules that make the table true — SiP at X = 20–32, shim at 33–45, B2B at 46–49, fold at 49–51, flex tail routed on the lid inner face from the pads toward X = 19 and never under the LRA — must be written into the PCB/CAD constraints. (4) Capacity: 6.0 mm → 560–620 mAh; 6.5 → 600–660 `[U]`. Re-run §5.2 conservatively at 600 mAh: 600 × 0.81 = 486 mAh / 127.84 = **3.8 weeks** before the AMOLED's own consumption; with §6 E-9's re-run, **3.2–3.7 weeks**. (5) The lens occupies 0.50 of the 1.2 mm front wall; the doc's convention (counting it inside) is retained, so columns A/B/D are ~0.5 mm more generous than tabled.

#### Step 7. Cell specification sheet (send to ≥ 3 pouch vendors)

- Chemistry LCO or NMC pouch, 3.70 V nominal, 4.20 V charge (quote 4.35 V HV-LCO as an option with calendar-life data).
- Dimensions: **T 6.0 max** (baseline; quote 6.5 max as option B) at 50 % SoC fresh **including PCM, wrap and label**; ≤ T + 0.6 after 500 cycles at 100 % SoC; W 23.0 ± 0.3 (seam folded, no protruding tab); L 43.0 ± 0.5 incl. PCM head; PCM head at the crown end. Corner radius ≥ 1.0. **State the achievable mAh in this envelope in writing.**
- Capacity target ≥ 560 min / 600 typ (6.0) or ≥ 600 / 650 (6.5) at 0.2C to 3.0 V, 25 °C.
- Rates: charge 0.5C std, 1C max; discharge 1C continuous, **2C 10 ms pulse without PCM trip**; real duty 395 mA for 1 ms subframes, 35 mA/µs edges.
- **DC-IR ≤ 150 mΩ incl. PCM** at 25 °C, 50 % SoC, 10 s 1C pulse; report at 0 °C and −10 °C.
- **PCM:** OVP 4.275 ± 0.025 V, UVP 2.80 V (device cutoff 3.45 V in firmware/BQ25180), OCP ≥ 2.0 A with ≥ 10 ms delay, short-circuit < 500 µs, ≤ 3 µA quiescent; component list disclosed.
- **NTC 10 kΩ ± 1 % B3435 bonded to the cell face under the wrap** (BQ25180 thresholds are tuned to β = 3435 `[V]` SLUSE99C), third contact.
- Termination: 0.1 mm FPC, 3 contacts (B+, B−, NTC) into a **low-profile B2B, mated ≤ 0.70 mm, power contacts ≥ 0.5 A each** (Panasonic AXT / Hirose BM class; MPN `[U]`); no JST ACH (doc).
- **Mechanical acceptance:** allowable uniform face pressure and **allowable local/line pressure (we assume ≤ 20 kPa `[U]` — vendor to state)**; allowable bending; PCM-head stiffness; swelling method (thickness at 100 % SoC after N cycles, fixture-measured); handling spec for the stretch-release PSA tab on one face only.
- Life: ≥ 500 cycles to 80 % at 0.5C/0.5C; ≥ 3 years calendar at 25 °C/50 % SoC to 85 %; swelling ≤ 8 % EOL.
- Temperature: charge 0–45 °C nominal (JEITA-derated per Step 15), discharge −20…+60 °C, storage −20…+45 °C long term, +60 °C ≤ 1 month, **+72 °C ≥ 6 h × 10 cycles without venting (UN 38.3 T2 `[V]`)**; report behaviour at +80 °C 4 h (stretch); storage temperature/humidity limit in writing (drives §5 V-18).
- Certifications with samples: **IEC 62133-2:2017 CB report (cell + pack), UN 38.3 test summary (T1–T8)** `[V]` test list, UL 1642 desirable, MSDS, RoHS/REACH.
- Samples: 50 pcs ≤ 6 wk with a fixture-measured thickness histogram; NRE/MOQ for the custom size (expect $2–5k, 8–12 wk, MOQ 2–5k `[U]`). 20 cells to ADI for the MAX17048 INI on day one (doc §9.11).
- Mounting: cell bonded to the PCB-side insulator with a **stretch-release PSA tab** (tesa 70xx / 3M Command class) — no heat, no solvent for removal (Art. 11 `[V]`); nothing else bonds to the cell.

#### Step 8. Sealing, joint by joint (IP67; product leak limit 1 × 10⁻³ mbar·L/s at 100 mbar Δp)

| Joint | Type | Numbers | Notes / tag |
|---|---|---|---|
| **J1 lid ↔ tray rim** (perimeter ≈ 183 mm) | **Over-moulded self-adhesive LSR bead on the lid inner face, face-sealing onto the flat 1.2 mm wall rim.** Bead 1.0 W × 0.60 H, trapezoidal, keyed in a 0.15 mm recess with micro-dovetails; no groove | **Squeeze 0.18 mm (30 %)**, range 0.08–0.28 with rim flatness ≤ 0.10 and hook-shoulder ± 0.05; the wall rim sits 0.42 mm below the lid inner-face plane. Reaction 0.25–0.40 N/mm → **≈ 50–70 N**; design load = 70 + 43 (altitude) = **113 N**; retention required ≥ 2× = **≥ 230 N**: 2 × M1.4 at ≈ 90 N preload (180 N) + **12 snap hooks (6 per flank at ~11 mm pitch) ≥ 15 N each (180 N)** + antenna-end tongue → ≈ 360 N. Hook: 0.4 mm undercut, 45° lead-in, 0.6 × 3 mm section (shear ≈ 70 N each `[U]`); catches on the lid perimeter rib. Lid centre bulge at 26 kPa ≈ 0.3 mm outward (1.2 mm plate, 24.6 span `[U]`) — harmless. | ≥ 10 open/close cycles then IPX7; LSR compression set ≤ 20 % (ISO 815, 70 °C/22 h) `[U]` grade; **altitude test IEC 60068-2-13 11.6 kPa 2 h → IPX7**. `[U]` |
| **J2 lens ↔ tray** | PSA frame 300LSE/Tesa 61xx 0.13, 1.3 mm wide on the 1.5 mm ledge, single die-cut | lens −0.08 ± 0.05 sub-flush; 24 h dwell to full bond (leak test after ≥ 4 h) | Permanent; ledge flatness ≤ 0.05, no gate on the ledge. `[U]` |
| **J3 dock pads ↔ lid** | Flex bonded to the lid inside face: 0.10 mm PSA frame ≥ 1.0 mm wide around all four ø2.0 openings + UV-cure acrylic bead around the flex perimeter; **openings:** ø2.0 with a 0.2 × 45° outer chamfer and a 0.1 mm inner lip so the pad face sits 0.05 below the wall surface (no pogo snag, no edge-creep path); shim-stiffened flex backs the pads so pogo force (≈ 1 N × 4) + magnet pull (3–5 N) load the PSA in compression | sweat creep test on the pad-to-wall interface specifically | Fallback: 4 insert-moulded gold-plated brass targets. `[U]` |
| **J4a ring-disc ↔ tray end wall; J4b ring-disc ↔ cap** | H-section clear-PC ring-disc: 1.5 mm visible web at X = 71–72.5 spanning the full section, 3 mm skirt inside the tray end (X = 68–71, 0.8 mm thick — hence PCB ends at 68) and 3 mm skirt in the cap bore; **PC-safe 2K epoxy** (Step 2), 0.05–0.10 mm bond line | bond area ≈ 2 × 72 mm × 3 mm ≈ 430 mm² per side; lap shear ≥ 5 MPa → > 2 kN `[U]`; **ESC screen** (Bergen jig, 0.5–1 % strain, uncured adhesive contact 24 h) on the real ring grade before EVM-1 | Permanent. The skirt is the light-injection path for the PLCC-4 at X = 62–63 (light stub per §5 M7). No metal in the joint. Alternative: NMT nano-moulding of the ring onto the cap `[U]`. |
| **J9 RF feed feedthrough (redefined, §3 C-5)** | The cap's L-shaped feed tab (5 × 1.5 mm) passes through a **rectangular aperture ≈ 5.6 × 2.1 mm in the ring web**, bonded in the same epoxy operation as J4b (≥ 0.3 mm epoxy annulus is the seal); the tab continues −X over the PCB edge to X = 65.5 with its plated land underneath; the z-deflection spring finger at X = 65.5–67.5 bears on it inside the sealed envelope, contact ≤ 30 mΩ | the tab is anodised except the land (plating per §5 M4); the epoxy annulus is the seal; validate in the leak correlation set | `[U]` — replaces the ø3 boss / x-loaded finger of revision 2 |
| **J5 crown cartridge ↔ tray bulkhead (redefined, §3 C-2)** | Static **face seal** — LSR/silicone ring 50 A on the sleeve flange/ear front face, compressed 25–30 % against the bulkhead's inside face by the ear retention (2 × M1.4 into bulkhead bosses or ultrasonic stake) | squeeze 25–30 % | The cartridge (sleeve + diaphragm + satellite PCB + carrier) is one factory sub-assembly; nothing crosses the diaphragm except flux and the BeCu ESD bleed leaf. Module leak test §4 M-20b. `[U]` |
| **J6 crown dynamic seal (optional)** | Per §4 Design step 8.7: low-temperature FKM 75–80 ShA (or PTFE-filled silicone) 1.0 CS rotary O-ring, **3–6 % squeeze**, ID 1–3 % larger than the ø7 hub, compressed from the gland OD (Parker §8.13 `[V]`), PFPE grease; 0.15 mm labyrinth into the two wide-face debris pockets (§3 C-15) | groove Ra ≤ 0.4 µm | 1 × 10⁶ indexes then IPX7; **IPX7 after −20 °C soak** and cold torque. The LSR diaphragm, not the O-ring, is the bulkhead. *Revision 2's "10–15 % squeeze, hub OD ≥ 8 mm, 0.6 × 1.5 chamber" is superseded.* |
| **J7 keyring lug** | insert-moulded 316L in the tray flank, no through-hole | pull ≥ 100 N × 60 s (design ≥ 150 N, test 300 N per §4); 10k jerks at 20 N | `[U]` |
| **J8 grip electrode** | **No feedthrough:** the IQS211B annular electrode is an insert-moulded 316L ring (or LDS-plated track) **inside** the crown-end bulkhead wall, 0.8–1.0 mm behind the static shoulder surface, routed clear of the debris pockets; contact by a spring finger to the satellite PCB inside the sealed volume; 2k2 series + 10 pF shunt on the satellite PCB; COEX0 blanking | self-capacitance through 1 mm PC/ABS (εr ≈ 3) is standard cap-button practice; Cx still ≈ 5–15 pF `[U]` | ESD: the electrode is not exposed; the crown's discharge path is now the bleed leaf (§3 C-4). Validated on the doc §9.8 coupon with a press. |

IP6X: same joints; the crown labyrinth is the only dust path and the (optional) O-ring plus the skirt journal are the dust barriers.

#### Step 9. LRA mounting and acoustic mitigation

- VG0840001D (ø8.0 × 4.05, 170 Hz, 1.00 Grms `[V?]` vendor page) on the **PCB top side at X = 52–60** on a 0.20–0.30 mm brass bracket soldered to the PCB (baseline), bracket ending ≤ X = 61 (polymer bracket preferred by §5). The moving mass reacts against the PCB (+ the cell mass coupled through the cell's own PSA tab to the PCB-side insulator). **≥ 0.3 mm air gap to the front wall, to the lid, and — explicitly — to the cell face; no PSA to the cell** (Art. 11 path and no pouch diaphragm). *The doc's "bracket tied to PCB and cell mass" is corrected (§3 C-9).*
- Bracket first mode ≥ 800 Hz (calculate, then measure on Mule C).
- Option (RF-gated): LRA in an 8.4 mm PCB cut-out at X = 52–60, still on the bracket, still ≥ 0.3 mm from the cell (column C).
- Acceptance: ≤ 35 dB(A) at 10 cm during the 150 ms boop, anechoic box — **`[U]` provisional; set from the Mule C measurement against a reference product**; measured with and without cell contact on Mule C.
- Magnetics: LRA centre X ≈ 56 is > 40 mm from the DRV5032 latches and MT6701.

#### Step 10. Fastener and insert spec

- 2 × **M1.4 × 3.0 Torx T3 pan**, A2/316, **plain (no patch)**. Seating torque **0.025 ± 0.005 N·m** → preload ≈ T/(K·d) = 0.025/(0.2 × 1.4 mm) ≈ **90 N** `[U]`, K ≈ 0.2; T3 tool limit 0.14–0.18 N·m `[V]` Wiha. Driver with **torque + angle monitoring** (seat detected by angle window). Locking is by the LSR gasket springback + insert friction; a micro-encapsulated dry patch (prevailing ≤ 0.005 N·m) only if DVT vibration shows loosening.
- Insert: brass heat-set M1.4, OD 2.3 × L 3.0 (marketplace grade); **acceptance: pull-out ≥ 2 × preload = ≥ 180 N and torque-out ≥ 3 × seating = ≥ 0.08 N·m**, 10 bosses at EVM-1; if not met → M1.6 mould-in insert (catalogue heat-set ranges start at M2 `[U]`).
- Installation: thermal press, insert 250–280 °C, 1.5–2.0 s, 0.05 below flush (PC/ABS Tg ≈ 125 °C `[U]`); ultrasonic staking alternative.
- The T3 driver is commercially available and one ships in the box (specialised tool "provided free of charge with the product" is explicitly acceptable — C/2025/214 `[V]`).

#### Step 11. Dock pads, 430 shim and PCB rear-side connector layout

- Pads: 4 × ø2.0 Au over 1.0–2.5 µm Ni on 0.1 mm flex, order GND · SWCLK · SWDIO · VBUS at 2.54 mm, rear face **X = 34–44**.
- **Shim = flex stiffener (baseline):** 0.3 mm 430 SS 12 × 8 mm laminated under the pads (X = 33–45). Magnet-to-shim distance ≈ 1.2 wall + 0.05 PSA + 0.1 flex ≈ 1.35 mm vs ~0.45–0.9 insert-moulded → expect 40–60 % of the head vendor's quoted pull `[U]`; measure at EVM-1 (A.5-9). Fallback: insert-moulded with a 1.5 mm local pad and a witness line.
- **Flex tail route:** on the lid inner face from the pads toward the crown end (in the 0.6 mm swell gap, 0.2 mm booked in columns A/B), turning down at X = 17–19 to a **5-way 0.4 mm-pitch B2B on the PCB rear side** (4 lines + dock-presence), so the lid unplugs for service. Never routed under the LRA.
- **PCB rear-side strip X = 16–19 (3.0 mm), placement sketch:** cell 3-way B2B receptacle (~2.5 × 2.0 mm + 0.5 keep-out) at y = −7; dock 5-way receptacle (~3.3 × 2.0 + 0.5) at y = +6; both plugs enter from the rear; the strip's remaining width carries the two crown-end tooling holes at y = ± 10.5. **PCB top side X = 16–19.5:** the **10-way** 0.5 mm satellite connector (FH12-10S class, 2.0 mm tall) or hot-bar pad field — column D (7.8 mm margin; it sits under the panel edge only at 18–19.5; **the 3.0 mm x-depth is the constraint**, §3 C-12). Footprints `[U]` until MPNs are chosen; if the strip does not close at layout, the fallback is the cell at X = 20–63 (Mule B) or a soldered dock tail with a service loop.
- Polarity by cradle geometry (doc). Verify no DRV5032 false-latch while docked (head magnets > 25 mm from the sensing magnet) at EVM-1.

#### Step 12. Crown module — interface freeze and the transverse variant *(mechanism content superseded by §4; §3 C-2)*

**Doc inconsistency (flagged, resolved in §4):** §4.3's "12 mm-long POM journal" cannot exist inside §6.2's 2.0 mm journal/hub allotment; §4's 6.9 mm two-land journal gives ≈ 0.8° tilt (this domain's own sketch reached the same 0.8°), the doc's < 0.5° is corrected in §8. The magnet-to-sensor gap is 1.0 mm (MT6701, §4 Design step 15), not the 2.8 mm of the revision-2 sketch; stroke is 0.40 mm with the EVPBB tact and a compliant pip, not 0.25 mm with a ≥ 0.25-travel tact. The cartridge is inserted **from inside the tray** (§4 M-21) and seals with a face seal on the flange/ears (J5).

**Dual-compatibility for Mule C — tray features frozen at Gate G0 whichever geometry wins:** the crown-end bulkhead bore (ø13.30 +0.05/−0 reamed, depth, the two ear pockets and the J5 seal face), the two wide-face debris pockets, the buried electrode ring, the two lid-screw bosses, the collar snap interface, and the lug position on the *right* tray flank at X = 8–14 (the transverse wheel slot, if chosen, is on the left flank of the *collar*, not the tray). **Explicitly accepted:** if transverse wins, the collar tool, the crown-module parts and the satellite PCB change; the tray tool does not, provided the interface is frozen at the EVM-0 gate (week 8), before EVM-1 tooling starts.

**If transverse wins** (§4 Design step 20): (1) crown zone shortens ~3 mm → given to the RF keepout buffer (§5), not body length; (2) wheel, axle, race and journal move into a wet cavity in the collar; J6 disappears, replaced by a static gasket around the wheel module; the exposed bearing needs ceramic balls, POM journal and a draining debris slot; (3) press = 0.40 mm translation of the wheel cradle onto the diaphragm-covered tact; (4) side-shaft sensing (MA782 class) or an L-flex MT6701; (5) wheel face recessed ≥ 0.5 mm inside the flank silhouette.

#### Step 13. Drop strategy (1.5 m, 0.74 J) and pressure differential

- Corners/edges monolithic tray; R4 capsule radius; lid edge inset 0.3 mm behind the flank.
- Lens −0.08 sub-flush behind a 0.3 mm PC/ABS lip; 0.13 mm PSA absorbs edge shear; ground CS-glass edges. **Lens-specific tests:** 32 g steel ball from 30 cm on the lens centre; 5.6 g pen drop from 10 cm on the lens edge (industry practice `[U]`).
- Cell located by edges (side ribs), bonded on the PCB side, 0.6 mm free travel into the swell gap.
- PCB clamped in Z (Step 3); B2B connectors held down by panel foam / lid rib ends; no underfill on the SiP by default — corner-bond at DVT if LGA cracks appear.
- Crown end-on drop: the crown skirt bottoms on the sleeve flange hard stop (§4 Design step 12: 120 N at 2000 g, ≈ 6 MPa on POM); firmware ignores a press shorter than 30 ms.
- Cap end-on drop: J4b in bending — first meaningful test is EVM-1 with real bonded rings; the cap's internal lip on the shell carries the load, never the finger or tab.
- Magnet retention: pocket + Loctite 648 class + 3 × 120° stake (§4 M-16); concentricity re-checked after bonding.
- **Pressure differential:** hermetic capsule at hold altitude (~26 kPa external Δ) and +60 °C (+14 kPa internal): lid retention (J1) budgeted at 2×; lens PSA in tension 0.10 MPa; crown O-ring blow-by checked in the altitude test (IEC 60068-2-13 → IPX7).

#### Step 14. Service / replaceability path (Art. 11; application 18 Feb 2027 `[V?]`)

1. Unclip the crown-end collar (spudger) → 2 × T3 screws exposed. 2. Unscrew; lift the lid from the crown end, releasing 12 snaps sequentially with the spudger (no heat, no solvent, no adhesive across the lid). 3. Unplug the dock-flex B2B. 4. Pull the stretch-release tab; unplug the cell B2B. 5. Fit the new cell (spare kit = **cell + 2 screws + loose LSR gasket** if the loose-gasket fallback is used; with over-moulded LSR the gasket is rated ≥ 10 cycles). 6. Close, torque 0.025 N·m with the boxed T3 driver. 7. Manual carries instructions and the "spares available 5 years" statement. **Do not rely on the wet-environment derogation:** C/2025/214 — "an IP rating alone is considered as not sufficient"; five cumulative indicators, of which "primary use in wet conditions" and "washable" cannot be claimed for a keychain `[V]`. Legal opinion (doc §9.9, $3–5k) confirms before the lid tool is cut. The crown cartridge is **not** user-serviceable (§3 C-18).

#### Step 15. Thermal

- Charging: 0.39 W into 90 cm² → +4.3 K still air (doc). **JEITA per SLUSE99C `[V]`:** defaults COLD 0 °C / COOL 10 °C / WARM 45 °C / HOT 60 °C; charging and safety timers **suspended** < COLD and > HOT; **ICHG × 0.5 (default) or × 0.2** in COOL (0–10 °C); **VREG −100 mV (default) or −200 mV** in WARM (45–60 °C). NTC on the cell face (β 3435, 10 k). Recommendation: set TS_HOT = 50 °C (register option 10) for a pocket object `[U]` product choice; confirm at EVM-1.
- **Storage requirement:** −20 °C 16 h and **+72 °C ≥ 6 h non-operating (UN 38.3 T2-aligned `[V]`) then IPX7 and full function**; **+80 °C 4 h is a stretch test on 3 DVT units**, not a requirement. Firmware blanks screen and halo above 60 °C cell temperature.
- AMOLED operating −20…+70 °C `[V?]`; Tstg not published → panel drawing item.
- Damp heat: **85 °C/85 % RH 240 h on lens + OCA + dummy-glass coupons**; the real module at **60 °C/90 % RH 240 h** (typical panel humidity condition `[U]`).
- UV: PC/ABS and clear PC UV-stabilised; ISO 4892-2 300 h on tray colour and ring (Verification).

#### Step 16. DFM notes for moulding

- Tray: 1 cavity soft / 1+1 hard; hot-runner valve gate on the aperture through-wall under the lens ink, **never on the ledge or the rim**; texture VDI 27–30 flanks/rear; SPI B-1 around the lens; moulded-in colour, no paint. The rim (24.6 × 66 inner, 1.2 wide) flatness ≤ 0.10 over length — achievable with balanced cooling; ≤ 0.05 is not a moulding spec, it is a CMM sort at EVM-1 `[U]`. Post-mould: ream the crown bore ø13.30 +0.05/−0 in the same fixture as the ear-pocket seal face (§4 M-14 datum logic applied to the tray).
- Lid: **2-shot PC/ABS + self-adhesive LSR** (needs an LSR-capable moulder: cold-runner, vacuum-vented tool) — DVT may use a separately moulded LSR gasket bonded/keyed in; 4 pad openings cored with the chamfer/lip; snap hooks by in-line cores (0.4 mm undercut, 45° lead-in); perimeter rib 0.6 × 1.5 with 1° draft.
- Ring-disc: optical PC, 2-plate tool, gate on the tray-side skirt face (hidden); outer web edge SPI A-2; inner faces VDI 24 micro-texture for diffusion; **rectangular tab aperture cored** (§3 C-5); light stub; photometric scan at EVM-1.
- Sinks: nothing thicker than 50 % of wall opposite an A-surface; lens-pocket 1.5 mm transition ≥ 3 × the step.
- Clear PC: dry 120 °C 4 h, mould 80–100 °C; PC/ABS mould 80–90 °C `[U]`.
- Tolerances that matter: ledge flatness 0.05 (sorted), rim flatness 0.10, crown bore reamed (§4), bore concentric to the ear-pocket seal face ≤ 0.02, hook-shoulder height ± 0.05 (sets gasket squeeze).

### 7.5 MANUFACTURING — sequenced

#### Phase 1. Prototype path

| Build | Weeks (from EVM-0 start) | Qty | How the mechanical parts are made | Cost (mech scope) | Tag |
|---|---|---|---|---|---|
| **EVM-0 Mule C** (feel) | 0–3 | 2 crown-end assemblies (coaxial, transverse) + LRA rig | SLA collars/bulkhead blocks (Formlabs Rigid 10K / Somos) **drawn to scale from §4**; real turned 316L crowns + one Ti Gr5; three race materials (§3 C-1); Si₃N₄ balls; etched BeCu springs; low-temp FKM O-rings; EVPBB tacts on real satellite PCBs; machined POM-C sleeves; loose LSR discs + machined pips; motorised detent-life rig; **field map at the sensor plane with each race**; acoustic box with/without cell contact | ~$4k (doc) + $4k rig | `[U]` |
| **EVM-0 Mule B** (RF mech mock) | 0–5 | 2 boards, 1 shell set | CNC 6061-T6 cap with the L-tab and masked Ni/Au land (§5 M4); CNC-clear-PC or SLA-clear ring-disc with the full web and tab aperture; SLA shell; dummy Al-laminate cell **at X = 19–62 and 24–67, 6.0 and 6.5 mm**; **PCB with and without the 8.4 mm LRA slot (or copper-bridged slot)**; real AMOLED module; real crown | $6–8k of the $20k | `[U]` |
| **EVM-1** (works-like, looks-close) | 8–20 | 20 | **Quick-turn aluminium single-cavity tools for tray and lid** (Protolabs/Xometry class, 2–3 wk, $8–15k) so snaps, rim, lens ledge and the reamed crown bore are real; gasket as a separately moulded LSR part (or die-cut silicone) keyed in the lid; CNC caps with tab; CNC/SLA ring-disc; crown cartridges from real parts (§4); 50 custom cells (both thicknesses); 50 laminated lens + panel modules with B2B tails; 10 bosses for insert pull-out | $40–55k incl. cell and lens NRE | `[U]` |
| **DVT** | 20–36 | 150 | **Soft tooling** (7075 Al, single cavity): tray (may be the EVM-1 tool re-cut), ring-disc; **lid as PC/ABS Al tool + separate LSR gasket moulded in a small LSR tool and bonded/keyed** (2-shot LSR deferred to hard tooling); production-intent crown cartridge from the watch-component house (§4 M-14/M-15 tools); CNC caps from two shops | $60–90k (tooling + 150 kits) | `[U]` |
| **PVT** | 36–52 | 500 | **Hard tooling sized to forecast:** 1+1 P20 tray + 2-shot LSR lid tool (100k-shot), 2-cav ring; textured; $35–60k. (The doc's $18–30k covered single-cavity soft tools only — the delta is a programme decision.) Cap on a 5-axis cell or forged-then-machined; crowns on Swiss-type lathes | $75–120k | `[U]` |

#### Phase 2. Component manufacturing processes (supplier type in brackets)

1. **Tray / lid / ring-disc moulding** [Dongguan/Shenzhen wearable-tier moulder **with LSR 2-shot capability**; Protolabs/Xometry for quick-turn]. Incoming QC: CMM on ledge flatness (0.05 sort), rim flatness (0.10), hook-shoulder height (± 0.05), crown bore after reaming; cosmetic AQL 1.0; weekly 5-part gasket compression-set check (ISO 815, 70 °C/22 h, ≤ 20 % LSR `[U]`).
2. **Heat-set inserts** [moulder, thermal press 250–280 °C, 1.5–2 s]: 100 % depth go/no-go; 5 pcs/lot pull-out ≥ 180 N and torque-out ≥ 0.08 N·m.
3. **6061-T6 cap with L-tab** [5-axis CNC → anodiser → plater]: **per §5 M1–M5 (§3 C-6)** — machine (Ra 0.8 inside, 0.4 outside, land Ra ≤ 0.8), deburr, plug the land, **anodise MIL-A-8625 Type II class 2, 8–15 µm, RoHS seal**, then Route A (masked immersion EN ASTM B733 Type IV/V ≥ 5 µm + B488 Au) or Route C (plated pin); 100 % land-to-cap ≤ 5 mΩ; XRF 5/lot; tape adhesion + thermal shock per lot.
4. **Crown** [watch-crown maker, Swiss turning + cut serrations + PVD]: per §4 M-1…M-7; µr ≤ 1.05 lot gate.
5. **Race** [per §4 M-8…M-11; zirconia/BeCu variants per §3 C-1].
6. **Leaf springs / wave washer / C-ring / bleed leaf** [photo-chemical machining, BeCu C17200, aged]: per §4 M-13.
7. **Crown sleeve and diaphragm** [POM-C moulder + one-chucking secondary; LSR moulder with PEEK insert loading]: per §4 M-14/M-15; **insert-moulded 316L grip ring in the tray bulkhead** (J8) is a tray-tool feature.
8. **Cell** [pouch vendor per Step 7]: 100 % OCV/IR/thickness at vendor; incoming 20/lot thickness at 50 % SoC, DC-IR, PCM trip 5/lot.
9. **Lens + OCA + AMOLED module** [display module vendor, laminated, B2B-terminated tail]: lens from a cover-glass house (CNC/laser cut 0.5 mm CS glass, edge grind, 2–3 pass ink, AF) → **full lamination in ISO 6 (class 1000) clean room: plasma/IPA clean, vacuum roller lamination of 8146-5/-6 (3M: nip-roll, hand lamination not advised `[V]` TDS), autoclave de-bubble (typ. 40–50 °C, 0.4–0.5 MPa, 20–30 min `[U]`)** → AOI (> 0.1 mm bubbles/particles reject), ink-window alignment ± 0.10 → 2 h burn-in. Yield 90–95 % at 1k `[U]`. Option if the B2B fails drop: bare panel + lens delivered separately, in-line lamination at the CM (adds a clean-room cell, +$30–60k `[U]`).
10. **Dock flex** [FPC house]: 2-layer PI 0.1 mm, ENIG with **1.0–2.5 µm Ni** on the drawing, 0.3 mm 430 stiffener laminated under the pads, PSA pre-applied; XRF Ni thickness 5/lot.
11. **PSA/foam die-cuts** [converter]: lens PSA frame, insulator, stretch-release tab, panel foam (hold-down), flex PSA — one carrier, kiss-cut.
12. **Ring-disc epoxy** [line process]: 2K clear epoxy, volumetric dispense 0.05 ± 0.01 mL per joint (+ the tab aperture), fixture cure to handling (per TDS), **full cure 24 h before leak test** — hence the pre-line in Phase 3.

#### Phase 3A. Crown-cartridge sub-assembly

*Superseded by §4 M-16…M-23 (the toleranced sequence: sleeve prep → crown onto sleeve with wave washer and C-ring → cartridge torque/stroke test → magnet bonding last → satellite pairing with 3-bin pip selection → module leak test → insertion into the tray from inside). Revision-2 stations C1 (press 200–400 N), C2 (magnet before assembly), C4/C6 (0.25 end float) are withdrawn; C9 (module leak test) and C10 (field-map spot check 1/50) are retained as §4 M-20b and an addition to M-19.*

#### Phase 3B. Tray pre-line (batched ≥ 24 h ahead of the main line)

| Stn | Operation | Fixture / tool | Spec / QC |
|---|---|---|---|
| P10 | **Cap + ring-disc bond (J4b + J9):** dispense epoxy in the cap bore and around the tab aperture; press the ring-disc skirt in with the L-tab through the aperture | nest + press 20 N | skirt to shoulder, squeeze-out ≤ 0.2 mm inside only; **tab land clean (no epoxy), land height to the cap seating face ± 0.05 re-checked** |
| P20 | **Cap+ring to tray end (J4a):** epoxy on the tray-side skirt; press | alignment nest | step ring-to-tray ≤ 0.05 on four faces; tab lateral position ± 0.3 to the tray datum |
| P30 | Cure rack, 24 h at 23 °C (or per TDS accelerated 60 °C/1 h `[U]`) with lot traceability | rack | timer/traceability record |
| P40 | Heat-set inserts (if not done at the moulder); ream the crown bore if not done at the moulder | thermal press; reamer fixture | depth go/no-go; bore ø13.30 +0.05/−0 |
| P50 | **Halo uniformity camera go/no-go** (20 mA into the stub, §5 M13) | camera | ≥ 70 % min/max |

#### Phase 3C. Final assembly (station by station)

Pre-conditions: PCBA tested and programmed on the bed-of-nails (MCUboot + app + modem, APPROTECT locked — doc A.2; `%XPRODDONE` **not** issued), LRA and bracket soldered at SMT, all receptacles fitted; crown cartridge from §4 (leak-tested, M-20b); cured tray from Phase 3B; cells at 30–50 % SoC; serial numbers assigned.

| Stn | Operation | Fixture / tool | Spec / QC |
|---|---|---|---|
| 10 | **Crown cartridge into the bulkhead bore from inside the open tray** (§4 M-21): J5 face-seal ring on the flange/ears; insert crown-first with the orientation key; seat the ears in their pockets; secure (2 × M1.4 into bulkhead bosses or ultrasonic stake); route the 10-way satellite tail | press with key | ears seated (force signature); seal squeeze 25–30 % by height gauge; labyrinth 0.05 feeler at 4 positions; tail free |
| 20 | **PCBA in:** locate on the 4 pins; the feed finger passes under the cap's L-tab and is compressed as the board seats on the tray Z-ribs (datum Z1); plug the satellite tail (top side, X = 16–19.5) | PCB nest, ESD | **S11 finger signature at the switch connector > 10 dB RL change open/closed at 722 MHz** (§5 M13.6); tray Z-ribs bearing on the PCB edge |
| 30 | **Panel tail mate through the aperture:** feed the laminated module's tail through the display aperture, fold at X = 49–51, mate the 0.4 mm B2B onto the receptacle at X = 46–49 with a fixture pin; place the panel foam pad | vacuum pick + mating tool | click detect (force curve); 27-line continuity via the PCBA self-test |
| 40 | **Lens module into the ledge:** peel the PSA liner on the tray ledge, lower the lens, roller-press 30 N for 5 s | vacuum nest | sub-flush −0.03 to −0.13 (dial gauge, 4 corners); no squeeze-out; **PSA dwell timer starts (≥ 4 h before leak test, 24 h to full bond)** |
| 50 | **Insulator + cell:** stretch-release tab + insulator onto the PCB rear side; place the cell into the side locators (edges only); plug the 3-way B2B | soft-jaw nest | click detect; OCV read; cell not touching the LRA (go-gauge 0.3) |
| 60 | **Lid prep (off-line):** dock flex bonded to the lid (PSA + UV bead, 10 s cure), tail dressed toward X = 19 | UV station | pad flush −0.05; bead continuous |
| 70 | **Lid:** plug the 5-way dock B2B; hook the antenna-end tongue; rotate down; full-perimeter press 150 N to engage 12 snaps; drive 2 × M1.4 at **0.025 ± 0.005 N·m with angle window** | press + torque/angle driver | screw seat detected; lid-to-flank step ≤ 0.10; gasket squeeze inferred from lid height ± 0.05 |
| 80 | **Crown-end collar** snap on (hides the screws; clearance slot for the lug) | — | gap uniformity |
| 90 | **Leak test** (Phase 4, after PSA dwell ≥ 4 h — WIP buffer with traceability) | station | pass/fail, value logged to serial |
| 100 | **EOL functional** (Phase 5) incl. the crown EOL calibration capture (§4 M-23) and the RF box (§5 M14, then `%XPRODDONE`) | dock jig + RF box | pass/fail |
| 110 | Keyring interposer, clean, cosmetic inspection, pair-code label | — | AQL 1.0 |

Takt ≈ 4–6 min/unit at PVT with 7 stations plus the pre-line `[U]`.

#### Phase 4. Leak / IP test method (100 %)

Product limit: **1 × 10⁻³ mbar·L/s air-equivalent at 100 mbar Δp** (INFICON: 5 × 10⁻³ "no water" for ABS/steel + polymer seal; 2 × 10⁻⁴ for aluminium + polymer; ours spans both families) `[V]`. INFICON's conclusion — "tracer gas leak testing is the method of choice" at these rates `[V]` — is adopted:
1. **Gross-leak pre-screen:** form-fitting chamber, 200 mbar over-pressure, 5 s stabilise, 10 s chamber-pressure decay; rejects ≥ 1 × 10⁻² mbar·L/s. Thermal soak ≥ 5 min at test-room temperature before any fine test.
2. **Fine test:** helium bombing at 200 mbar over-pressure (the part's tolerable Δp per INFICON is 100–200 mbar `[V]`) for 5–10 min, then the unit in a **vacuum accumulation chamber at ~700 mbar abs (Δp 300 mbar, inside the J1 retention budget)** connected to a mass-spectrometer leak detector (INFICON/Pfeiffer class, floor ≤ 1 × 10⁻⁶); accept ≤ the reading from a calibrated 1 × 10⁻³ reference leak run through the same bombing cycle. Parameters `[U]`; forming gas (5 % H₂/N₂) with a hydrogen sniffer is the cheaper alternative if correlation proves adequate.
3. **Correlation (DVT, ≥ 30 units):** fine-test reading vs IPX7 (0.15 m/1 m, 30 min) and IP6X (category-1 talc, ≤ 2 kPa, 80 volumes/8 h) `[V?]`; the acceptance threshold is tightened until zero immersion failures pass. Timing: after ≥ 4 h lens-PSA dwell and full epoxy cure. One retest after a 5 min ambient rest (the crown debris pockets are on the wet side and equalise immediately).

#### Phase 5. End-of-line functional test (dock jig, ≈ 90 s) and traceability

Dock on the jig (VBUS, GND, SWDIO, SWCLK + presence) → serial/eSIM read → charger current 300 mA ± 10 %, NTC within 3 °C of jig ambient, **JEITA register readback (TS_HOT/WARM/COOL/ICHG/VRCG as configured)** → gauge read → AMOLED white/RGB/black by camera (dead pixels, mura, ink-window centring ± 0.15) → halo three colours, uniformity ≥ 70 % min/max → LRA boop: jig accelerometer ≥ 0.8 g peak, mic ≤ 35 dB(A) at 10 cm `[U]` provisional → crown by jig motor 2 turns: 48 detent positions ± 1.5°, all four latch outputs toggle 2×/rev, torque 2.5–4 mN·m, **24-point table written to NVM** (§4 M-23) → press 5× (click 2.3–3.5 N, click travel 0.15–0.37, stop 0.37–0.43) → grip: phantom finger on the shoulder → sleep current 1 in 20 via SWD/PPK2 (< 200 µA after 60 s) → radiated go/no-go in the shield box vs golden unit (−1.0/+2.0 dB at B12 and B2/B4, §5 M14) → `%XPRODDONE`.
**Serialisation:** unit serial ↔ pair code ↔ cell lot/serial ↔ lens/module lot ↔ crown-cartridge serial + pip bin ↔ leak-test value ↔ EOL record ↔ firmware/modem versions, held in the MES and the fulfilment system; required for the Art. 11 spare path, UN 38.3 documentation at split shipping, and DVT/ORT failure analysis.

#### Phase 6. Packaging as a bonded pair with split shipping

- Factory bonding: both units provisioned and cross-signed before packing (doc §7.6); each box carries the pair code.
- Each unit in its **own** retail box: 30–50 % SoC, Dyneema interposer fitted, claim-code card, **T3 driver**, cable/dock allocation decided commercially.
- Dangerous goods: device with a ≤ 20 Wh cell installed → **UN3481 "lithium ion batteries contained in equipment", PI 967 Section II** (air) `[V?]` IATA DGR not opened; lithium-battery mark on the outer carton except where the small-consignment exemption applies `[V?]` — confirm with the forwarder; the vendor's UN 38.3 test summary travels with the documentation.
- ISTA 3A on the shipper before DVT sign-off.

### 7.6 VERIFICATION — gates and DVT matrix

#### Gate EVM-0 → EVM-1 (mechanical scope; the doc's three Mule gates still apply)
- **Mule C:** dial geometry chosen; **bulkhead/collar/lug interface frozen**; detent torque 2.5–4 mN·m, ≤ 15 % decay after 100k; press force ≤ +50 % across the knurl with the 6.9 mm journal; click separation ≥ 12/s; acoustic output measured with/without cell contact; **field map with each race — DRV5032 BOP/BRP margin ≥ 2×, MT6701 INL within spec after calibration**; cold torque at −20 °C with the chosen O-ring (or none). If fail: race material, journal, O-ring compound.
- **Mule B:** both cell positions (19–62, 24–67), both thicknesses, and **PCB with vs without the LRA slot**; the passing position sets the cell x; if the slot costs > 1 dB at B12 the cut-out option is dead and the cell is 6.0 mm; tab length and full-web ring confirmed.
- Paper: cell quotes at 6.0 and 6.5 mm with capacity in writing; **AMOLED panel drawing** (outline ±, COG ledge, tail pitch/length/bend zone, polarizer, Tstg, thickness incl. back film) in hand; Art. 11 legal opinion; LSR grade selected with a self-bonding datasheet.

#### Gate EVM-1 → DVT (20 units)
- Z-stack closes physically: every column ≥ 0.3 mm by shim measurement, lid closes ≤ 150 N; 6.0 vs 6.5 mm decided here.
- 3 units fine-leak + immersion pass; 3 units drop (26 orientations) with no lens crack / ring debond / **B2B intermittency (continuous monitoring during drop)** — if the panel B2B fails, switch to hot-bar + in-line lamination now; insert pull-out ≥ 180 N and torque-out ≥ 0.08 N·m on 10 bosses; dock pull ≥ 200 g through the wall with shim-as-stiffener (else insert-mould); PC/ABS and ring **ESC screen** passed (sunscreen, DEET, 70 % IPA, ring epoxy uncured; Bergen jig 0.5–1 % strain, 24 h, no crazing at 10×); gasket reseal 10 cycles on the EVM-1 lid; J5 and J9 in the leak set; sleep current on the golden unit.

#### DVT test matrix (150 units built; ~65 consumed)

| Test | Method / standard | Units | Pass criteria | If fail |
|---|---|---|---|---|
| Drop | 1.5 m onto steel plate on concrete, 26 orientations (6 faces, 8 corners, 12 edges) — IEC 60068-2-31 free-fall / MIL-STD-810H 516.8 practice `[V?]` | 5 | function + IPX7 after all 26; no lens crack, ring debond, magnet shift (encoder ± 1°), B2B unmated, cell edge locators intact; S11 finger check | corner-bond SiP; skirt 4 mm; lens edge finish; B2B → hot-bar |
| Tumble | IEC 60068-2-31 tumble, 0.5 m, 100 tumbles `[V?]` | 3 | as above | |
| Lens impact | 32 g steel ball from 30 cm on centre; 5.6 g pen from 10 cm on the lens edge `[U]` practice | 3 | no crack; AOI no delamination | lens CS/DOL, chamfer |
| IP67 | IEC 60529: IP6X category-1 method (talc, ≤ 2 kPa, 80 vol / 8 h); IPX7 1 m 30 min `[V?]` — after drop, after 10 lid open/close cycles, after 1 × 10⁶ crown indexes, after thermal cycling, **after altitude**, **immediately after −20 °C soak** | 5 (+ drop/thermal/altitude units) | zero water/dust on teardown; fine-leak correlation | gasket squeeze +0.05; J3 → insert-moulded pins |
| Altitude | IEC 60068-2-13, 11.6 kPa, 2 h (UN 38.3 T1-aligned pressure `[V]`) → IPX7 | 3 | lid retained, no gasket lift, lens PSA intact, crown O-ring no blow-by | more hooks / rib |
| Thermal cycling | IEC 60068-2-14 Nb, −20 ↔ +60 °C, 1 °C/min, 50 cycles; then storage −20 °C 16 h and **+72 °C 6 h × 3**; **+80 °C 4 h stretch on 3 units** | 3 (+3) | function, IPX7, no OCA bubble, PSA intact, cell swell ≤ 0.3 mm | OCA grade, PSA width |
| Damp heat | **85 °C/85 % RH 240 h on lens+OCA+dummy-glass coupons**; **real module 60 °C/90 % RH 240 h** | 3 + 3 | no bubbles > 0.1 mm, no ink lift, ΔE < 2 | |
| ESC / chemical | Bergen jig 0.5–1 % strain, 24 h: sunscreen, DEET, 70 % IPA, hand sanitiser on tray/lid/ring; ring with uncured epoxy | 3 sets | no crazing at 10× | grade change |
| UV | ISO 4892-2 300 h on tray colour and ring `[U]` severity | 2 | ΔE < 3, no haze increase > 2 % | UV package |
| Salt / sweat | **IEC 60068-2-11 Ka 48 h continuous** on 2 `[V?]` (or 60068-2-52 Kb severity 2 cyclic on 2); artificial sweat ISO 3160-2 on 2 (crown, cap, pads, lug) `[U]`; EN 1811 nickel-release screen on skin-contact metals (≤ 0.5 µg/cm²/wk) `[V?]` (§4 item 13); **dock-pad edge creep: sweat drop on the pad/wall interface, 30k pogo cycles, then IPX7** | 5 | feed land ≤ 50 mΩ, no Ni bloom, anodise intact, PVD intact, no pad-edge ingress | plating/PVD, J3 |
| Detent life | 1 × 10⁶ indexes at 2–3 rev/s with 0.5 N side load; torque logged; **at −20 / +23 / +60 °C samples**; then talc and steel filings (§4) | 2 | torque 2.5–4 mN·m at end, decay ≤ 15 %, no brinelling at 20×; then IPX7 | race material, O-ring compound |
| Press life | 300k presses at 2 N; press force at −20/+23/+60 °C | 2 | click force ± 15 %, travel within 0.15–0.37 | |
| Charge / discharge | 300 cycles 0.5C/1C with the real 395 mA 1 ms burst at 25 °C; 50 cycles at 0 °C discharge and 45–50 °C charge (JEITA WARM band, VREG −100 mV) | 5 | capacity ≥ 90 % at 300; no PCM nuisance trip; VDD ≥ 3.3 V during bursts at 0 °C | cell DC-IR spec |
| Cell safety | IEC 62133-2:2017 (CB) on the pack; UN 38.3 T1–T8 summary `[V]` test list; device-level IEC 62368-1 Annex M | vendor + lab | certificates before PVT | |
| Swell | 500-cycle cells | 10 cells | ≤ T + 0.6 mm | swell gap |
| Acoustics | anechoic box, boop and purr, 10 cm and 1 m, with/without cell contact | 3 | ≤ 35 dB(A) at 10 cm `[U]` provisional, set from Mule C | bracket isolation |
| Keyring lug / crown yank | 300 N × 60 s on the lug; 150 N × 10 s on the crown; 10k jerks at 20 N | 3 | no crack, ≤ 0.2 mm set, ears intact | |
| Lid service | 10 open/close cycles by naive users with the boxed T3 driver, then IPX7; screw torque-out after 10 cycles | 5 | 5/5 pass; < 5 min; no lost parts | snap/gasket redesign |
| Dock | 30k dock/undock; pull ≥ 200 g through the wall; Au intact at 20× | 3 | | insert-mould shim |
| Leak-test correlation | fine-leak reading vs immersion on 30 units | 30 | threshold set with zero escapes | |
| RF pre-scan | PTCRB/FCC pre-scans on DVT units with frozen cap/ring/match (§5) | 3 | within 2 dB of the gate | |
| ESD / halo optics / RF TRP | §4 item 9, §5 V-11, §6 EV-10 | | | |

#### PVT (500 units)
- ORT: 20 units/week through drop/IP/thermal mini-loops for 4 weeks; yield targets: lamination ≥ 95 %, fine-leak ≥ 98 % first pass, EOL ≥ 97 %; Cpk ≥ 1.33 on lens sub-flush, lid step, gasket squeeze (lid height), crown torque, click travel.
- **Certification: pre-scans from DVT (RF frozen), final PTCRB/FCC/CE/carrier samples from PVT**; MP not gated on a fresh cert cycle.
- Release gate: all DVT failures closed with re-test, leak threshold frozen, work instructions with photos, golden units locked, traceability live.

### 7.7 Suppliers / process types, NRE, unit cost

All costs `[U]` unless noted; doc §4.6 is the baseline.

| Item | Process / supplier type | NRE | Unit @1k / @10k | Lead time | Second source |
|---|---|---|---|---|---|
| Tray + lid (2-shot LSR) + ring-disc | Injection moulder **with LSR 2-shot and insert capability** (Dongguan/Shenzhen wearable tier); Protolabs/Xometry quick-turn Al for EVM-1/DVT | quick-turn $8–15k; soft $25–40k; hard 1+1 P20 + LSR 2-shot $35–60k | $2.60 / $1.70 (three parts + gasket) | quick-turn 2–3 wk; soft 5–7; hard 8–10 | tools are owned; any LSR-capable moulder |
| Glass lens 0.5 mm CS, printed, AF, 16 × 34 | Cover-glass house via the display vendor | $2–5k | $1.80 / $1.00 | 4–6 wk | AGC/Corning/Schott glass; two lens houses |
| Lamination lens+OCA+AMOLED with B2B tail | Display module vendor, ISO 6 clean room, autoclave | $1–3k jig | $1.40 / $0.80 (incl. connector; panel price separate, §6.5) | with the panel | second vendor on the same RM69310 panel; **option: in-line lamination at the CM +$30–60k** |
| 6061-T6 cap with L-tab, anodised, plated land | 5-axis CNC + anodiser + plater (§5) | $3–6k fixtures + masks | $4.50–7.30 (§5) / $2.75–4.35 | 4–6 wk | dual-source; plating is the qualification item |
| Crown cartridge (§4) | Watch-component maker + ceramic ball vendor + PCM etch house + POM moulder + LSR moulder | $60–85k programme (§4) | $16–18 / $9–10 (§4; this domain's $10.50 omitted serrations and race hard-finishing) | 6–12 wk | crowns CN + EU; balls catalogue |
| Cell 23 × 43 × 6.0/6.5, PCM, NTC, FPC/B2B | Pouch vendor (LiPol/Grepow/EEMB class; tier-1 for PVT) | $2–5k size + $3–6k IEC 62133-2 CB / UN 38.3 | $3.50–4.50 / $2.80 | samples 6 wk; production 8–12 wk; MOQ 2–5k | two vendors on one drawing (Art. 11 5-year spare) |
| Dock flex + 430 stiffener, ENIG 1–2.5 µm Ni | FPC house | $1–2k | $0.60 / $0.35 | 3 wk | any |
| Inserts M1.4 + T3 screws (plain) | Fastener distributor; M1.6 mould-in fallback | — | $0.15 | stock | |
| PSA/foam die-cuts, insulator, stretch-release tab | Converter (3M/tesa/Nitto) | $1–2k | $0.40 / $0.25 | 2–3 wk | |
| Ring epoxy (PC-safe 2K) | Henkel/3M | — | $0.12 | stock | |
| LRA bracket | Stamping house (or polymer moulding) | $2–3k | $0.15 | 4 wk | |
| Keyring lug + Dyneema interposer | Stamping + cordage | $2k | $0.30 | 4 wk | |
| Assembly fixtures (pre-line + 7 stations) + EOL dock jig | In-house or wearable-class EMS (Shenzhen/Taiwan/Malaysia) | $30–45k | labour $3.2 / $2.1 | 8 wk | |
| **Leak-test station (tracer gas):** gross pressure-decay + He bombing + vacuum accumulation with mass-spec detector | INFICON / Pfeiffer / CTS integrators | **$40–80k** (vs $15–30k pressure-decay only) | $0.15 consumables | 8–10 wk | forming-gas/H₂ sniffer variant $25–40k |
| **Mechanical BOM subtotal** | | | **≈ $34–38 / $23–26** (doc: shells 5.50 + crown 9.50 + cap 6.50 + cell 3.50 = $25; the delta is the crown's serrations/hard-finishing and the lens/lamination lines) | | |

Programme NRE in this scope: EVM-0 mech ~$12k; EVM-1 ~$50k (incl. quick-turn tools, cells, lenses); DVT tooling + build ~$80k; PVT tooling + build ~$105k; fixtures + leak station ~$80–125k; test labs (drop/IP/thermal/salt/altitude/ESC/UV/IEC 62133) ~$25–40k; legal opinion $3–5k → **~$355–420k mechanical/build NRE to MP**, excluding RF, certification ($50–150k, doc), the crown programme's own tooling ($60–85k, partly overlapping the DVT/PVT builds), the AMOLED commercials and the optional in-line lamination cell.

Critical path (mechanical): custom cell (12 wk) and hard tooling (10 wk) start at the EVM-1 gate; LSR-capable moulder selection at the EVM-0 gate; the AMOLED panel drawing is an EVM-1 *entry* item.

### 7.8 Risks, ranked (kill probability × irrecoverability)

1. **Z-stack governed by the LRA column: 6.5 mm cell only closes with an RF-gated PCB cut-out** — HIGH. Mitigation: 6.0 mm cell baseline (C′ 0.70), cut-out only if Mule B shows ≤ 1 dB B12 loss with the slot. Test: Mule B slot/no-slot; EVM-1 shim measurement of all six columns.
2. **Cell position vs antenna keepout (doc 24–67 violates its own 10 mm rule; 19–62 is 9 mm)** — HIGH, cross-team. Test: Mule B both positions; the number decides.
3. **Lid seal and retention after user service (12 hooks + 2 screws vs gasket + altitude loads)** — HIGH for IP67. Mitigation: LSR bead 30 % squeeze, lid rib, 2× retention budget. Test: DVT lid-service × 10 → IPX7; altitude → IPX7; if fail add two screws at the antenna end (1.5 mm in the end wall, zero Z).
4. **Detent race field-amplitude loss (17-4PH "strongly ferromagnetic in all conditions" `[V]`)** — HIGH for DRV5032 threshold margin. Mitigation: three race materials on Mule C (§3 C-1). Test: field map; BOP/BRP margin ≥ 2×.
5. **Panel B2B intermittency in drop (the doc rejected ZIF for this reason)** — HIGH, recoverable: fallback hot-bar + in-line lamination (+$30–60k). Test: EVM-1 drop with continuous monitoring.
6. **Ring-disc joint in drop and ESC (1.5 mm clear PC between 8 g Al and a 40 g body; adhesive chemistry; now also the tab aperture)** — HIGH. Mitigation: H-section skirts, PC-safe epoxy, ESC screen, no metal in the joint. Test: EVM-1 cap-end corner drops with real bonded rings; Bergen-jig ESC; J9 in the leak set.
7. **Art. 11 misread** — HIGH irrecoverability, LOW probability with a door architecture; the derogation is not relied on (C/2025/214 `[V]`). Test: legal opinion before the lid tool.
8. **Dock pads (J3) leak under sweat creep + magnet/pogo cycling** — MEDIUM-HIGH. Test: 30k cycles → sweat drop → IPX7; fallback insert-moulded pins.
9. **Fine-leak method sensitivity/cost (tracer gas at $40–80k) and correlation** — MEDIUM. Test: 30-unit correlation set; forming-gas variant if adequate.
10. **Crown-cartridge-to-tray interface (insertion from inside, ears, face seal J5) not yet drawn to scale** — MEDIUM (design-time). Test: to-scale CAD by week 6; Mule C yank; EVM-1 leak set.
11. **Dashboard heat: 72 °C anchor vs unknown AMOLED Tstg and cell storage** — MEDIUM. Test: DVT +72 °C 6 h × 3 and +80 °C stretch; panel Tstg in writing.
12. **LRA acoustic radiation** — MEDIUM. Mitigation: bracket to PCB only, air gaps to cell and shells. Test: Mule C anechoic with/without cell contact; DVT.
13. **M1.4 heat-set insert pull-out < 2 × preload** — MEDIUM. Test: EVM-1 10 bosses ≥ 180 N / ≥ 0.08 N·m; fallback M1.6 mould-in.
14. **LSR 2-shot capability at the moulder / gasket compression set** — MEDIUM. Mitigation: separate LSR gasket until hard tooling; TPV only as a PC/ABS-bonding grade. Test: ISO 815 set + 10-cycle reseal.
15. **Cold behaviour of the crown seal (FKM near −20 °C)** — MEDIUM-LOW. Test: cold torque and IPX7 after −20 °C soak; fallback PTFE-filled silicone or delete the O-ring (§4).
16. **Custom-cell lead time (12 wk) / MOQ vs EVM-1** — MEDIUM. Mitigation: samples at both thicknesses on the EVM-0 gate; two vendors.
17. **Crown end-on drop registers a boop / damages the tact** — MEDIUM-LOW (the hard stop carries 120 N, §4). Mitigation: firmware debounce ≥ 30 ms. Test: DVT × 5 on the crown end.
18. **Lamination yield on a 0.5 mm lens with a ~4 mm COG-end ink step** — LOW-MEDIUM. Test: AOI on the first 50 EVM-1 modules; 8146-6 if the step traps bubbles.
19. **Keys scratch the shell** — LOW severity, HIGH probability. Mitigation: VDI texture, moulded-in colour. Test: 500-cycle key-bundle tumble.

### 7.9 Open questions (mechanical)

1. Cell x-position: 19–62 (9 mm from the ring; the doc's 10 mm keepout is itself `[U]`) vs 24–67 (doc §6.2). Only Mule B's chamber result can decide; both dummy-cell positions must be built.
2. LRA PCB cut-out: RF-gated. Mule B must be measured with and without the 8.4 mm slot at X = 52–60. If B12 efficiency drops > 1 dB the 6.5 mm cell is dead and the baseline is 6.0 mm (C′ margin 0.70).
3. Cell thickness and capacity: 6.0 mm (560–620 mAh `[U]`) vs 6.5 mm (600–660 mAh `[U]`); vendor must state capacity in writing at T max including PCM/wrap at 50 % SoC, and the allowable local face pressure on the pouch.
4. Detent race material — decided on the Mule C field map (§3 C-1): DRV5032 (3.9 mT) and MT6701 margins at 1.0 mm AG with each ring.
5. Ring-disc: optical PC (εr ≈ 2.9–3.0), full web, the sealed tab aperture (J9) — RF to confirm the web and the longer tab on Mule B; optics to design the PLCC-4 → stub injection.
6. AMOLED panel drawing: outline tolerance, COG ledge, tail pitch/length/bend zone, polarizer/back film in the 0.784 mm, storage temperature. EVM-1 entry criterion; all AMOLED mechanicals stay `[V?]` until it is in hand.
7. Panel tail termination: 0.4 mm B2B with foam hold-down (baseline) vs hot-bar + in-line lamination at the CM (fallback). Decided by EVM-1 monitored drop.
8. Gasket: self-adhesive LSR grade (which Dow/Momentive grade bonds the chosen PC/ABS; ISO 815 set at 70 °C/22 h) vs Santoprene 8211-55B100 with a relaxed set limit — DVT reseal test settles it; the 70 °C compression set of 8211-55B100 is not published `[V]`.
9. Lid retention numbers (gasket reaction 0.25–0.40 N/mm, hook 15 N, lid deflection < 0.03 mm between hooks) are `[U]` — settle by FEA before tool cut and by the altitude and lid-service tests.
10. Fine-leak method and threshold: helium bombing + vacuum accumulation parameters are `[U]`; the 1 × 10⁻³ mbar·L/s product limit sits between INFICON's 5 × 10⁻³ (ABS/polymer) and 2 × 10⁻⁴ (Al/polymer) — the 30-unit correlation set sets the acceptance number.
11. Dock pad interconnect: 5-way B2B on the lid flex tail (baseline) vs lid-side spring contacts; shim-as-stiffener pull force through 1.35 mm vs insert-moulded — both measured at EVM-1.
12. PCB rear-side strip X = 16–19 and top-side 10-way satellite connector at X = 16–19.5: do the footprints close (§3 C-12)? If not: cell to X = 20–63 (Mule B), hot-bar satellite tail, or a soldered dock tail.
13. Art. 11 legal opinion: confirm the keychain is end-user-replaceable (derogation unavailable per C/2025/214 `[V]`) and that the boxed T3 driver satisfies the free-of-charge tool clause; the 18 Feb 2027 date is `[V?]`.
14. M1.4 heat-set insert pull-out in PC/ABS — measure ≥ 180 N / ≥ 0.08 N·m at EVM-1 or move to M1.6 mould-in.
15. Crown-cartridge-to-tray interface (§3 C-2): bulkhead bore + ear pockets + J5 face seal + ear width 6.0 mm — draw to scale before the Mule C blocks are printed; confirm the moulder can ream the bore and finish the seal face in one fixture.
16. Crown O-ring compound at −20 °C: low-temperature FKM (GLT/GFLT, TR10 `[U]`) vs PTFE-filled silicone vs deletion — Mule C item 4 (§4) settles it.
17. IP6X category: lab summaries say IP6X is tested by the category-1 (vacuum) method under IEC 60529 `[V?]`; open the standard before writing the DVT protocol.
18. Transverse crown (if Mule C picks it): the collar interface, bosses, bore and lug position are frozen at Gate G0; the exposed bearing needs its own corrosion/drainage DVT items.
19. Acoustic acceptance (≤ 35 dB(A) at 10 cm) is `[U]` until Mule C measures a reference product.
20. Cell shipping/SoC policy and the IATA PI 967 Section II mark exemption for split-shipped single units — confirm with the forwarder `[V?]`.
21. *(new, §3 C-15)* Bulkhead wall 0.70 mm at the debris pockets on the 15 mm faces — mould-flow and corner-drop analysis on the tray.

---

## 8. Consolidated confirm-before-design-in list (doc §4.4 + Addendum A.5 + every domain's open questions), ranked by damage-if-wrong

Rank order: A = product-killing or certification-blocking; B = respin of a tooled part or a board; C = schedule / cost; D = UX or documentation. Within a tier, earlier items gate earlier phases. Doc §4.4 items 1–2 (Sharp/Winstar) are retired by the AMOLED decision and replaced by item A-4.

| # | Item | What must be confirmed / opened | How it is settled | Damage if wrong | Owner | Gate |
|---|---|---|---|---|---|---|
| A-1 | AT&T classification | Keychain = "wearable" (body phantom, v2.1 Note 6) or free-space SFF | Written answer from AT&T's Partner Coordinator; V-5 in both configurations | Wrong pass/fail configuration for Mule B; 2–4 dB `[U]` of hidden requirement | RF | P0 → G0 |
| A-2 | B12 efficiency ≥ 15 % bare (and B2/B4 ≥ 17.8 %) | Not a datasheet — the chamber | Mule B V-5 + V-5b | Product-killing; Plan B changes the shell | RF | G0 |
| A-3 | nRF9151 full Product Specification + HIG | ANT DC tolerance/ESD/layout; SPIM maximum clock (8 MHz `[V?]`); VDD_GPIO/rail limits; COEX0 semantics and `%XRFTEST` on nRF91x1 `[V?]`; power-class switchability; PTCRB/GCF module status | Open the PS/HIG; Mule A on the DK | Feed network wrong (dead modem), fps halved, test strategy invalid, cert budget wrong | Electronics/RF | P0 → G0 |
| A-4 | AMOLED module + RM69310 + TPS65631-class PMIC | Panel drawing (outline tol, COG ledge, tail pitch/bend, polarizer/back film, Tstg); driver SPI mode, partial-window commands, sleep-in/out delays; PMIC input range, efficiency, shutdown current, SWIRE | Documents in hand; Mule A DK measurement of glance current and wake latency | Lens/ledge/aperture tooling wrong; runtime off by ± 0.5 wk; RF desense | Mechanical + electronics | EVM-1 entry |
| A-5 | MT paging / eDRX grant | `+CEDRXRDP`, `+CPSMS`, AS-RAI, MT UDP delivery at eDRX 163.84 s; per-paging energy (92.6 µA `[V?]` vs 18 µA `[V]`) | Mule A | Product promise ("their boop reaches you") and 15.56 + 8.23 mAh/wk | Electronics/firmware | G0 |
| A-6 | Cell (custom 23 × 43 × 6.0/6.5) | Capacity in writing at T-max incl. PCM/wrap at 50 % SoC; DC-IR ≤ 150 mΩ incl. PCM at 25/0/−10 °C; PCM trip ≥ 2 A / ≥ 10 ms; allowable local pressure; storage T/RH limit; IEC 62133-2 / UN 38.3 | RFQ + 50 samples both thicknesses; EV-4 brownout | Z-stack, runtime, field brownout, DVT plan (V-18) | Mechanical + electronics | G0 |
| A-7 | 3GPP TS 36.101 tables and spurious limits | Tables 6.2.2-1/6.2.3-1/6.2.4-1 (PC3 ± 2 dB, ΔTC, MPR, A-MPR NS_06); §6.6.3 spurious; FCC §27.53/§24.238; TS 36.124 | Open the specs; EVM-1 V-9/V-9b | 21.5 dBm design power wrong → efficiency gate wrong; H3 in B4 DL fails cert | RF | G0 / G1 |
| A-8 | SAR at PC3 | 1-g body-worn (pocket) and 10-g extremity (hand) | EVM-1 V-10b pre-scan | PC5 forced late → power model + cert re-plan | RF | G1 |
| A-9 | MFF2 eUICC supply-shutdown (doc §4.4-5) | Written confirmation + minimum shutdown interval; MPN | Supplier letter; Mule A PPK2 | +20–60 µA `[V]` = up to 10 mAh/wk | Electronics | P0 (before reel PO) |
| A-10 | Coaxial vs transverse crown | 10-hand blind test | Mule C item 1 | Collar tool, satellite PCB, sensor variant | Crown + ID | G0 |
| A-11 | Press stroke 0.40 mm and the EVPBB tact (doc §4.4-6) | ID sign-off on 0.40; Panasonic allowable static/over-travel load and travel tolerance in writing; 3-bin selective assembly closes on ≥ 10 units | Mule C item 6 | Boop unreliable (arithmetic worst-case does not close); tact class change | Crown + ID | P0 → G0 |
| A-12 | Detent race material and magnetics | FEMM + gaussmeter with 17-4PH / zirconia / BeCu rings and the tact dome; ≥ 2× B_OP at the latches; INL; 17-4PH H900 schedule (ASTM A564/AMS 5643 not opened); MIM only if ≥ 40 HRC measured | Mule C item 7; M-9/M-11 | First-motion detection or INL fails; race ratchets | Crown | G0 |
| A-13 | Art. 11 legal opinion (doc §9.9) | Keychain end-user-replaceable; boxed T3 driver as the "free tool"; 18 Feb 2027 date `[V?]` | Opinion ($3–5k) | Lid architecture and spares obligation | Mechanical + product | Before the lid tool (G0) |
| A-14 | Feed finger and stack | Finger MPN force-deflection curve; 2.0 vs 2.5 mm free height or PCB-referenced stop; ± 0.38 worst-case stack; tab to X = 65.5 through the full web | Mule B V-3 on 10 stacks; EM re-run | Feed intermittent in drop; RMAs | RF + mechanical | G0 |
| A-15 | Plating standards for the feed land | ASTM B733 Type IV/V, SC1 ≥ 5 µm; ASTM B488 Au classes; Route A vs C | Open the standards; V-3/V-8 | Contact corrosion in the field | RF | G0 |
| A-16 | Coverage-search governor and eDRX/PSM-refused fallback | Written into the requirements with numbers | Release-gate tests in a shielded box | 11-day battery death; 2.6-day death | Firmware | P0 (spec) → DVT (test) |
| A-17 | BQ25180 SLUSE99C (not in the project; doc-tagged `[V]` numbers only) | /MR pull-up source and voltage (sets what the satellite TACT trace and the limiter see); SYS_REG ceiling during charge vs the AMOLED PMIC's 4.5 V VIN max (docked VSYS ≈ 4.43 V `[V?]`); input OVP threshold (sets the VBUS TVS function); I²C-watchdog default and disable bit; reset-default ICHG; /MR long-press reset timing vs the longest legitimate crown hold; VIN-side quiescent with charging disabled (EOL reference) | Open SLUSE99C; EV-2 / EV-6 | PMIC over-voltage on the dock; ICHG/JEITA silently reverting; a crown hold resetting the unit; EOL screen unusable | Electronics | Schematic |
| A-18 | MFF2 eUICC voltage class and IPA hosting (extends A-9) | ISO 7816-3 Class C (1.8 V) on the nRF9151 SIM_1V8 interface (class `[V?]` until the PS SIM chapter is opened); which entity hosts the SGP.32 IPA (eUICC IPAe / modem / application IPAd) — decides whether EM-9 needs a live attach for the profile download | Supplier letter + PS SIM chapter; EV-15 dry run | Non-working SIM; EOL jig needs network access it does not have | Electronics | P0 (before reel PO) |
| B-1 | TPS62840 RSET for 3.1 V (doc §4.4-3) and the 3.2 V option | Re-read Table 1; C(VSET) ≤ 100 pF | Schematic review; EVM-1 rail under the 14 mA sensor load | Two abs-max exposures on one resistor; sensors 40 mV from their floor | Electronics | Schematic |
| B-2 | MT6701 datasheet units and die-to-package (doc §4.4-4); AS5600L lifecycle (Infineon) | 10-sample micrometer stage; distribution lifecycle statement | Mule C CMM vs INL | 0.28 mm chain has 0.02 margin; single-source | Crown | G0 |
| B-3 | Ring resin (optical PC) | εr, tan δ at 1 GHz, εr(T), moisture uptake; clear vs diffuse (ID) | Split-post resonator, dry and after 24 h soak | 0.2–0.5 dB + match drift; halo cosmetics | RF + mechanical | G0 |
| B-4 | Crown-cartridge-to-tray interface (§3 C-2) | Bulkhead bore + ear pockets + J5 face seal + 6.0 mm ears + bleed leaf; insertion from inside | To-scale CAD by week 6; Mule C yank; EVM-1 leak set | Tray tool re-cut | Mechanical + crown | G0 |
| B-5 | Cell x-position and LRA slot (§3 C-7/C-8) | 19–62 vs 24–67; slot ≤ 1 dB | Mule B | PCB respin; 6.5 mm cell dead | RF + mechanical | G0 |
| B-6 | PCB floor plan closure | 3.0 mm rear strip (cell 3-way, dock 5-way, tooling holes); 10-way satellite connector fit at X = 16–19.5; AMOLED 27-pin B2B ≤ 0.70 mm mated; GPIO count with the shared SPI bus; three-strip plan at X = 49–68 | Scale drawing at week 6; rev A layout | Respin | Electronics | Week 6–8 |
| B-7 | Inductor Q at 700 MHz (LQW15AN / 0402DC) | Datasheet Q-vs-f curves | Open the datasheets | Match loss 2.0–2.8 dB estimate off | RF | Schematic |
| B-8 | LSR lid gasket grade | Self-bonding to the chosen PC/ABS; ISO 815 set ≤ 20 % at 70 °C/22 h; Santoprene 8211-55B100 as the only TPV option (set relaxed) | Datasheet + DVT 10-cycle reseal | IP67 after service | Mechanical | G0 (moulder selection) |
| B-9 | Rotary O-ring keep/delete and compound | Drag ≤ 0.5 / ≤ 0.9 mN·m at 40 °C and −20 °C; low-temp FKM (Parker bulletins not opened) vs PTFE-silicone vs deletion (+ zirconia race) | Mule C item 4 | Feel (up to half a detent of drag) or wet mechanism | Crown | G0 |
| B-10 | ESD bleed leaf (§3 C-4) | Moulded-in BeCu leaf in the POM sleeve; 1 MΩ ∥ TVS on the satellite; wear over 1M indexes | Moulder confirmation; Mule C item 9 with current probe | Crown ESD reaches the tact/sensor | Crown + electronics | G0 |
| B-11 | Materion C17200 datasheet (leaf/washer/ring/bleed leaf) | YS 1130–1420 MPa, age 2 h @ 315 °C `[V?]` mirror | Open the Materion sheet | Leaf drawing wrong | Crown | Before M-13 release |
| B-12 | LSR-to-PEEK pip | Mechanical through-hole lock; moulder confirms or PBT/LCP core | Moulder; 300k presses | Pip detaches | Crown | DVT tool |
| B-13 | M1.4 heat-set insert | Pull-out ≥ 180 N, torque-out ≥ 0.08 N·m in PC/ABS | EVM-1 10 bosses | M1.6 mould-in; lid tool change | Mechanical | G1 |
| B-14 | Debris pockets and the 0.70 mm bulkhead wall (§3 C-15) | Mould-flow; corner drop | Tray mould-flow; Mule C item 10 | Bulkhead cracks | Crown + mechanical | G0 |
| B-15 | Dock head MPN and pull through 1.35 mm (A.5-9); flex-tail thickness in the swell gap (A.5-10); SWD clamp capacitance vs speed (A.5-11) | Measured at EVM-1 | EVM-1 | Insert-moulded shim (lid tool change); Z; programming speed | Electronics + mechanical | G1 |
| B-16 | Panel tail B2B vs hot-bar | Monitored 26-orientation drop | EVM-1 | Move lamination in-line (+$30–60k) | Mechanical | G1 |
| B-17 | SPI NOR MPN and size vs delta modem updates; RGB LED MPN (doc §4.4-7) | Datasheets; NOR 16 vs 32 Mbit | BOM freeze | Field modem updates impossible | Electronics | Schematic |
| B-18 | IEC 60529 IP6X category, IEC 60068-2-11/-13/-14/-31 texts | Open the standards | Before the DVT protocol | Wrong DVT method | Mechanical | G1 |
| B-19 | Permeability spec method (ASTM A342) and the 1.05 gate | Indicator method agreed with RF/sensor owners | M-4 | Lot gate unenforceable | Crown | G0 |
| B-20 | RM69310 electricals beyond A-4 | ELVSS abs max vs the PMIC's −4.0 V VNEG default during the SWIRE burst (ER-2); SWIRE burst semantics (emitted after SLPOUT? enables and programs in one burst?); whether RAMWR is accepted during tSLPOUT (the 135–160 ms wake estimate depends on it); SDO on the 27-pin tail (electronic mate check); Tstg | Panel datasheet + drawing; EV-1 (b) scope on ELVSS | Panel damage at every wake; wake > 200 ms; no mate check after drop; warehouse spec | Electronics | EVM-1 entry |
| B-21 | nRF9151 LGA pad pitch / inner-pad count and the GPIO injection-current limit (extends A-3) | Via-in-pad escape rule (0.20 mm drill / ≥ 0.40 mm pad, IPC-4761 Type VII `[U]`) vs the real pitch; 2+2+2 fallback; EV-8 pass criterion | PS/HIG; fab DFM on the rev A Gerbers; X-ray lot 1 | Board respin / +$2–3 per board; dock key-bridge criterion unmeasurable | Electronics | Rev A layout |
| B-22 | TPS65631 IQ(VIN present, CTRL low), fSW, CTRL/SWIRE protocol, tSTART; TPS22916 off leakage and slew at 3.1/4.4 V | Whether switch B can be deleted (IQ ≤ 0.5 µA over temperature); resistor-set-VNEG alternative and second source | Datasheets (not opened; product pages only); EV-2 | Standing current; ER-2 fallback path; single-source PMIC | Electronics | Schematic |
| B-23 | SWD limiter cell (gate-to-V3 N-FET + 220 Ω + 4.7 k / 2.2 k pull-up) | Highest error-free SWD clock through the flex; limiter FET Vth ≤ 1 V MPN; pad ESD-diode ≤ 15 pF MPN | EV-1 (g) on the DK; EV-9 10⁵-transaction run | Production programming > 60 s; key-bridge protection unproven | Electronics | EVM-1 |
| B-24 | MT6701 / AS5600L SDA/SCL structure with VDD off | Shared TWIM0 vs TWIM1 on two spare GPIOs | EV-7 unpowered-sensor bus test | Satellite or main-board respin | Electronics + crown | EVM-1 |
| B-25 | Lens/panel ESD at ± 15 kV air through 0.50 mm glass + 0.15 mm OCA | COG/tail latch-up or damage; grounded ITO/mesh or larger ink border fallback | EV-10 lens centre/edge | Lens or module change | Electronics + mechanical | G1 |
| C-1 | nRF9151 lead time vs EVM-1 | ≥ 40 prototype SiPs by week 10; 2k reel ≤ week 19 | PO acknowledgement | EVM-1 slips 2–3 months | Electronics | P0 |
| C-2 | Custom-cell lead time / MOQ | Samples ≤ 6 wk; production 8–12 wk; MOQ 2–5k | Two vendors | DVT slips | Mechanical | G0 |
| C-3 | LSR 2-shot moulder; wire-EDM shop capacity; LSR-over-PEEK tool | Quotes; bridge paths (separate gasket; broach-then-age; loose disc) | Selection at G0 | Tooling slips | Mechanical + crown | G0 |
| C-4 | Nickel release (REACH Annex XVII 27, EN 1811:2023, EN 12472) | Standards obtained; prolonged-contact classification; 5 PVD'd crowns + 5 lugs tested | Mule C item 13 | Ti crown/lug (+$3/pc) | Crown | G0 |
| C-5 | Certification scope: ISED, CE, Verizon; PTCRB module status; CTIA fee | Decide SKUs; open RSS/EN lists | P0-3 | $30–60k per extra tune | RF + product | P0 |
| C-6 | IATA PI 967 Section II and the small-consignment mark exemption for split shipping | Forwarder | Before PVT packaging | Shipping non-compliance | Operations | PVT |
| C-7 | Sealed-unit EOL VBUS-side gross-leak screen (Δ ≤ +50 µA `[U]`, §3 C-23) | Whether the BQ25180 VIN-side quiescent spread across 10 units leaves the screen usable, or the EOL sleep step is dropped for ORT cell-side sampling | EV-3 characterisation | Escapes of a +600 µA console fault, or a useless test step | Electronics + production | DVT |
| C-8 | EU SKU EMC immunity (EN 301 489-1/-52) and the dock board's EN 55032/55035 (§3 C-29) | Scope and owner of the dock board's certification; 3 V/m class `[U]` | EV-12 pre-scan | Late certification lines; dock redesign | Electronics + RF | DVT |
| D-1 | Product-story corrections | "No coast" (threshold 9.7 rev/s); screen wake ≤ 200 ms (halo/LRA ≤ 15 ms); "arrival stays on screen" → halo carries arrivals; first-motion ≤ 90° as a hard spec; glance brightness/count policy; doc §6.3 crown at the E-max; Au/6061 galvanic gap 0.9–1.0 V; Chu line; "< 0.5° on a 12 mm journal" → 0.8° on 6.9 mm | Product owner sign-off; REDESIGN_DECISION errata | Marketing promises the physics cannot keep | Product | G0 |
| D-2 | Detent acoustic target and LRA acoustic limit (≤ 35 dB(A) `[U]`) | ID decision; Mule C reference measurement | Mule C item 15 | Late ID rework | ID | G0 |
| D-3 | Crown yank 100/150 N, lug 150/300 N | Agree with ID/QA (no standard cited) | Mule C item 11 | Under/over-designed retention | Crown + QA | G0 |

---

## 9. Consolidated risk register, ranked by kill-probability × irrecoverability, each with the settling test

| # | Risk | Domain refs | Probability / severity `[U]` | Mitigation in this report | Settling test | When |
|---|---|---|---|---|---|---|
| 1 | **B12 total efficiency < 12.3 % (no catalogue fallback; Plan B not a sure pass at 8.4 % on Ignion's smallest board)** | §5 R1; doc §9.1 | 40–50 % / product-killing | Coupling-element architecture on the full 95 mm; cap/gap/tab/keepout as sweep variables; body length held; Plan B simulated in parallel | Mule B V-5 ≥ 15 % bare, cross-checked by V-5b | G0 (week 5) |
| 2 | **MT paging / eDRX not granted → polling → 2.0 wk runtime and a worse product** | §6 ER-4; doc §9.2 | 30 % / product-defining | State machine on the DK first; PSM + 300 s poll fallback with measured cost | Mule A on 3 carriers | G0 (week 2) |
| 3 | **Power budget: AMOLED glance energy `[U]` 8.75–29 mAh/wk + the 20 mAh/wk coverage-search line + the unlocated 92.6 µA paging figure** | §6 ER-3/ER-17; doc §5, §9.6 | 40 % / 1 week of runtime | Panel off between glances; brightness/glance policy; governor in the requirements with numbers; PPK2 golden every release | Mule A (paging energy, DK-driven panel current); EV-3; EV-6 shielded-box governor test | G0 → DVT |
| 4 | **Z-stack: only a 6.0 mm cell closes (C′ 0.70) unless the LRA slot survives RF; cell position vs keepout (doc's own layout violates it)** | §7 Risk 1–2; §5 R7; §3 C-7/C-8 | certain unless fixed / respin | 6.0 mm baseline; cell 19–62; LRA 52–60; slot RF-gated | Mule B slot/no-slot and both cell positions; EVM-1 shim of all six columns | G0 / G1 |
| 5 | **Crown press stroke stack: arithmetic worst-case does not close; tact allowable load unknown** | §4 Risk 1 | 30 % / boop unreliable | S = 0.40, 3-bin pip, compliant pip, 100 % EOL force-stroke | Mule C item 6 on ≥ 10 units; Panasonic letter | G0 |
| 6 | **Detent life / brinelling: land contact 2.1 GPa vs shakedown 1.9 GPa (wrought 17-4)** | §4 Risk 2 | 30 % / the dial is "one texture forever" | Wrought + EDM baseline; zirconia and BeCu in parallel; ø0.9 balls / lower F_n fallbacks | 100k per variant (Mule C), then 1M rig ≤ 15 % decay, ≤ 5 µm wear | G0 → EVM-1 |
| 7 | **B2/B4 ≥ 17.8 % missed while B12 passes** | §5 R3 | 20 % / cert-blocking | Dual-resonant match; tab offset / slit as the high-band lever | Mule B V-5 1710–2150 MHz; V-10 | G0 / G1 |
| 8 | **Radiated spurious: B12 × 3 lands in B4 DL inside the high-band passband** | §5 R4 | 15–25 % / cert-blocking | Harmonic-band simulation; two reserved trap positions | V-9 conducted H2/H3; V-9b radiated pre-scan | G1 |
| 9 | **SAR at PC3 in-hand / in-pocket** | §5 R5 | `[U]` / schedule + power model | PC5 fallback (gate drops in lockstep) | V-10b pre-scan | G1 |
| 10 | **Lid seal and retention after user service (12 hooks + 2 screws vs gasket + altitude)** | §7 Risk 3 | 25 % / IP67 in the field | LSR bead 30 % squeeze, lid rib, 2× retention, FEA before tool cut | DVT lid service × 10 → IPX7; altitude → IPX7 | DVT |
| 11 | **Race ferromagnetism / field margin at the latches and sensor** | §7 Risk 4; §4 Risk 9; §3 C-1 | 25 % / first-motion or INL | Three race materials on Mule C; ≥ 2× B_OP; 24-point EOL table | Mule C item 7 field map + INL | G0 |
| 12 | **First-motion detection ≤ 90° (hard spec now that the screen sleeps)** | §4 Risk 6 | 20 % / feel of "the wheel is never dead" | Both DU outputs on both latches (8 edges/rev); Bpk ≥ 8 mT | Latch edge map over 3 device lots, −10…+50 °C, across the press; EOL gap ≤ 80° | G0 → EOL |
| 13 | **Feed finger/land: stack, contact degradation, longer tab** | §5 R2/R6; §3 C-5 | 15–25 % / RMAs or blocked build | z-deflection L-tab, 2.5 mm finger or PCB-referenced stop, Type IV/V EN + Au or plated pin, S11 check at assembly | V-3 (10 stacks, 85/85 on cap-ring), V-17 drop → S11, V-18 | G0 → DVT |
| 14 | **Panel B2B intermittency in drop** | §7 Risk 5 | 20 % / clean-room move (+$30–60k) | Foam hold-down; hot-bar fallback ready | EVM-1 26-orientation drop with continuous monitoring | G1 |
| 15 | **Ring-disc joint (J4/J9) in cap-corner drop and ESC; tab aperture seal** | §7 Risk 6 | 20 % / debond or crazing | H-section skirts; PC-safe epoxy; ESC screen; no metal in the joint | EVM-1 corner drops with real bonded rings; Bergen jig; leak set incl. J9 | G1 |
| 16 | **nRF9151 lead time makes the decision for us** | §6 ER-5; doc §9.10 | 30 % / EVM-1 slips 2–3 months | PO week 0; prototype allocation | PO acknowledgement | P0 |
| 17 | **Rotary O-ring drag / spiral failure / cold stiffening** | §4 Risk 3; §7 Risk 15 | 30 % / feel or wet mechanism | Optional; low squeeze per Parker; low-temp FKM; zirconia race if deleted | Mule C item 4 at 40 °C and −20 °C; post-life inspection | G0 |
| 18 | **Concentricity chain 0.28 vs 0.30/0.25** | §4 Risk 4 | 20 % / INL, AS5600L variant lost | Tight bore, nest, die-to-package measured | CMM every Mule C unit vs INL | G0 |
| 19 | **IQS211B false grips during TX** | §5 R13 | 40 % without the network / feature | 2k2/10 pF + COEX0 blanking (RF-active semantics) | V-4, V-15 | G0 / G1 |
| 20 | **AMOLED PMIC desenses RX** | §5 R14; §3 C-10 | 20 % / TIS margin | PMIC at X < 40, shielded inductor, inner-layer rails | V-10 screen on/off ≤ 1 dB | G1 |
| 21 | **Layout closure: X = 49–68 strips, 3.0 mm rear strip, 10-way satellite connector, GPIO count** | §5 R8; §6 ER-25; §3 C-12, C-24 | certain unless drawn / respin | Three-strip plan; shared SPI bus; hot-bar tail fallback | Scale drawing before MPNs; rev A layout | Week 6–8 |
| 22 | **Regulatory classification (wearable vs SFF; RSS/EN sets; PTCRB module status)** | §5 R11 | 30 % / 4–8 wk | Letter; Step 15 list | The answer; V-10b | P0 → G1 |
| 23 | **Art. 11 misread** | §7 Risk 7 | low / very high | Door architecture; derogation not relied on | Legal opinion | G0 |
| 24 | **Hand + keys detune/absorb 4–10 dB in use** | §5 R9 | high / field margin, battery | Interposer mandatory; petting-grip model; PC3 if SAR allows | V-5 hand/keys; V-14 field | G0 / G1 |
| 25 | **Match tolerance, ring εr(T)/moisture and cell swell eat the margin** | §5 R10 | 25 % / yield | Tolerance grades; Monte Carlo with the new inputs; −1.0/+2.0 dB window | V-12, V-13, box statistics | G1 / DVT |
| 26 | **Dock pads leak under sweat creep + cycling** | §7 Risk 8 | 20 % / IP67 | PSA frame + UV bead + inner lip | 30k cycles → sweat → IPX7 | DVT |
| 27 | **Fine-leak method cost and correlation** | §7 Risk 9 | 20 % / $40–80k station, escapes | Gross + tracer-gas; 30-unit correlation | Correlation set | DVT |
| 28 | **Nickel release from the 316L crown/lug after PVD wear** | §4 Risk 8 | 20 % / Ti crown | EN 12472 → EN 1811 | Mule C item 13 | G0 |
| 29 | **0 °C brownout on a 395 mA burst** | §6 ER-15; doc §5.5 | 20 % / field resets | Cutoff 3.45 V; DC-IR ≤ 150 mΩ | EV-4 with a real cell and burst | G1 |
| 30 | **Crown-cartridge-to-tray interface not yet drawn (insertion from inside, ears, face seal, bleed leaf)** | §3 C-2/C-4; §7 Risk 10 | design-time / tray tool | To-scale CAD week 6 | Mule C yank; EVM-1 leak | G0 |
| 31 | **Race hard finishing (EDM recast, residual magnetisation)** | §4 Risk 5 | 15 % / ripple, field | Lap/electropolish; demagnetise | M-11; Mule C ripple ≤ 15 % | G0 |
| 32 | **Cable-dressing error in the passive chamber (1–3 dB)** | §5 R17 | high / false decision | Ferrites, crown-end exit, two orientations, cable-free cross-check | V-5b | G0 |
| 33 | **Dashboard heat (72 °C anchor) vs unknown AMOLED Tstg / cell storage** | §7 Risk 11 | 15 % / DVT failures | 72 °C × 3 requirement; 80 °C stretch | DVT thermal; panel Tstg in writing | DVT |
| 34 | **LRA acoustic radiation** | §7 Risk 12; doc §9.11 | 20 % / product feel | Bracket to PCB only; air gaps | Mule C anechoic with/without cell contact | G0 |
| 35 | **Lint, dust, steel filings in the race** | §4 Risk 10 | slow / jam | Skirt journal, pockets on wide faces, grease | Talc + filings runs | EVM-1 rig |
| 36 | **ESD to the floating crown (path via the new bleed leaf)** | §4 Risk 16; §3 C-4 | 15 % / tact or sensor damage | BeCu leaf + 1 MΩ ∥ TVS | Mule C item 9 with current probe; leaf continuity after 1M | G0 |
| 37 | **Debug UART left on (+100 mAh/wk); eSIM without shutdown (+7 mAh/wk)** | §6 ER-18/ER-19 | low if gated / a week of runtime | Compile-gated; supplier letter | PPK2 on every release; Mule A | Continuous |
| 38 | **Product-story expectations the physics cannot keep (coast; 15 ms screen; always-on arrival)** | §4 Risk 12; §3 C-11 | high expectation / low engineering | Corrections in §8 D-1 | High-speed video; wake-latency measurement; product-owner sign-off | G0 |
| 39 | **Dead-battery / ship-mode lockout: anything on the VBUS path that needs a GPIO (the doc's "charge held off until dock presence" read as a device-side switch)** | §6 ER-1, E-2; §3 C-22 | low if designed out / total (a sealed unit that cannot be revived) | Passive VBUS path: TVS + reverse-polarity P-FET + BQ25180 only; hold-off is a register rule + dock-head enable | EV-6: 0 V cell + dock → charge starts with no firmware | Schematic → EVM-1 |
| 40 | **Production sequencing: a unit locked (APPROTECT) before `%XPRODDONE`, eSIM and ship mode can be issued over RTT** | §6 ER-6; §3 C-22; §5 M14 | certain on the doc A.2 order / un-provisionable units | APPROTECT + SECUREAPPROTECT last, at pack-out (EM-9b); recovery path via `nrfutil device recover` | EV-15 production-flow dry run incl. recovery | Before the first DVT lot |
| 41 | **Panel exposed to the PMIC's −4.0 V VNEG default during the SWIRE burst (RM69310 ELVSS abs max `[U]`)** | §6 ER-2, E-5.3; §8 B-20 | `[U]` / panel damage at every wake | Wake order with PMIC VIN present before SLPOUT; MCU-driven CTRL inside tSTART or a resistor-set-VNEG PMIC as fallback | EV-1 (b) scope on ELVSS at every enable; datasheet check | G0 → EVM-1 |
| 42 | **SiP LGA escape on a 0.8 mm 6-layer (pitch `[U]`): via-in-pad rule rejected by the fab** | §6 ER-7, E-11; §8 B-21 | 20 % / +$2–3 per board, layout re-spin | Filled/capped through via-in-pad under every inner pad; 2+2+2 stacked-microvia fallback pre-costed | Fab DFM on rev A Gerbers; X-ray lot 1 | Rev A layout |
| 43 | **/MR pull-up domain above VDD_GPIO on the shared TACT net; SWD pads at 5 V in a key bridge** | §6 ER-10/ER-9, E-13; §3 C-24 | `[U]` / nRF I/O damage or a satellite respin | Gate-to-V3 N-FET limiter on SWDIO, SWCLK and TACT (firmware-independent, zero standing current) | EV-2 TACT idle voltage; EV-8 key bridges; EV-1 (g)/EV-9 SWD clock through the limiter | EVM-1 |
| 44 | **Docked VSYS ≈ 4.43 V `[V?]` vs the AMOLED PMIC's 4.5 V VIN max (70 mV)** | §6 ER-14; §8 A-17 | 30 % / PMIC stress on every dock | VSYS_REG programmed lower, or PMIC VIN from V3 via a boost-capable sibling | EV-2 docked ceiling; SLUSE99C SYS_REG table | Schematic → EVM-1 |
| 45 | **Screen-off current not zero (back-powering through parked GPIOs, switch leakage, PMIC IQ with VIN present)** | §6 ER-8, E-8, E-5.1 | 25 % / standing-current line | GPIO-park rule on the schematic; switch B on the PMIC VIN; VCI/VDDIO node ≤ 0.2 µA | EV-3 | EVM-1 |
| 46 | **BQ25180 I²C watchdog silently reverting ICHG/JEITA/SYS registers** | §6 ER-16, E-1.2 | certain if not disabled / charge behaviour drifts on the dock | Watchdog disabled at first configuration in every image | EV-6 10-min docked read-back; EV-13 release gate | EVM-1 → every release |
| 47 | **Crown ESD return through a single FFC ground beside the latch lines** | §6 ER-13, E-15; §3 C-24 | 20 % / satellite respin | 12-way tail with GND on pins 1 and 12 proposed | EV-10 HA1 probe during the crown discharge (≤ 0.5 V) | Rev A layout → EVM-1 |
| 48 | **SPIM 8 MHz `[V?]` / partial-window support `[U]` (UI quality); eUICC wrong voltage class** | §6 ER-11/ER-18; §8 A-3, A-18 | 20 % / 13 fps UI; a non-working SIM | Strip-buffer window writes; Class C (1.8 V) on the PO | EV-1 (a), EV-5; supplier letter | G0 |
| 49 | Lower-ranked, live: rim-push press force +28 % (§4 Risk 7); debris-pocket wall 0.70 mm (§4 Risk 11); crown yank/ring (§4 Risk 13); key-fob latch trips (§4 Risk 14); permeability lot drift (§4 Risk 15); AS5600L field margin/lifecycle (§4 Risk 17); detent acoustics (§4 Risk 18); LSR-PEEK pip (§4 Risk 19); insert-moulded ring crazing (§5 R18); transverse crown moving metal (§5 R19); second-SKU tunes (§5 R20); M1.4 insert (§7 Risk 13); LSR 2-shot capability (§7 Risk 14); cell lead time (§7 Risk 16); crown end-on drop (§7 Risk 17); lamination yield (§7 Risk 18); key scratches (§7 Risk 19); sensor I²C bus clamping (§6 ER-21); MAX17048 INI (§6 ER-22); sealed-unit EOL cannot see a 10 µA-class leak (§6 ER-20, accepted); lens/panel ESD (§6 ER-23); 0.4 mm-pitch WCSP/DSBGA yield (§6 ER-24) | | | | as listed in the domain sections | |

---

## 10. Sources opened

Only what a pass actually opened is listed; each domain's list is reproduced, then the editor's additions. Secondary/search-extract sources are marked as such.

### 10.1 Primary source and project files (editor and all domains)
- `C:\Users\chian\Projects\bingbong\REDESIGN_DECISION_2026-09-12.md` — read in full by the editor (lines 1–770) and by each domain (crown: §4.3, §4.4, §6.2, §6.3, §6.4, §7.1, §9.4, §9.11, §10; RF: §4.3, §4.4, §6, §9, §10; mechanical: full).
- `C:\Users\chian\Projects\bingbong\firmware\bingbong_pcb\_mech\nrf9151_ps.txt` (116 lines) — nRF9151 PS v1.0 front matter: "Up to 4x SPI master/slave with EasyDMA", "32 general purpose I/O pins", PC3/PC5, −108 dBm Cat-M1 low band, single 50 Ω antenna interface, PSM floor 2.7 µA, eDRX @ 81.92 s 18 µA (opened by the editor and by the crown and RF domains; also https://www.mouser.com/pdfDocs/nRF9151_PS.pdf front matter by RF).
- `C:\Users\chian\Projects\bingbong\firmware\bingbong_pcb\_mech\att_trp.txt` — AT&T IoT Radiated Performance Requirements v1.8 (Tables 1–7, notes).
- `C:\Users\chian\Projects\bingbong\firmware\bingbong_pcb\_mech\UM_NN03-310.txt`, `AN_NN03-310_EB_size.txt`, `AN_NN02-224_LengthClearance.txt`, `DS_NN02-224.txt` — Ignion NN03-310 / NN02-224 documents.
- `C:\Users\chian\Projects\bingbong\bom-scratch\fh12.txt` — Hirose FH12 0.5 mm FFC connector catalogue text (FH12-6S/8S-0.5SH, 2.0 mm height, 0.5 A, 20 cycles).
- `C:\Users\chian\Projects\bingbong\bom-scratch\ts04.txt` — Same Sky TS04 tactile switch datasheet (travel 0.15/0.25/0.35, life 60–100k).
- `C:\Users\chian\Projects\bingbong\bom-scratch\` (V1 notes) and `datasheets\ER-OLED018-1_Series_Datasheet.pdf` — V1 material, obsolete for this scope; directory listed by the editor, not used.

### 10.2 Crown domain
- Panasonic EVPBB light-touch switch datasheet ANCTB13E 2018-04 (scratchpad evpbb.txt): force/travel table (1.0 N & 0.7 N → 0.08 mm; 1.6 N & 2.4 N → 0.11 mm), part table (EVPBB2A9B000 1.6 N H 0.53 500k; EVPBB1AAB000 1.0 N H 0.50), "H ± 0.1", "General dimension tolerance ± 0.05", actuator ø0.7, IP67, 10k MOQ.
- TI DRV5032 datasheet SLVSDC7H (Dec 2024) (scratchpad drv5032.txt): Table 4-1, Table 5-1 pin functions (X2SON DU: OUT1 pin 4 north, OUT2 pin 3 south), DU BOP/BRP/BHYS table, fS 13.3/20/37 Hz and tS 27/50/75 ms, ICC 1.6 µA at 3 V, §7.3 Figure 7-4.
- MagnTek MT6701 datasheet Rev 1.5 (scratchpad mt6701.txt): §5 magnetic input (Bpk 200–1000 G; AG 0.5/1.0/2.0 mm; DISP 0.3 mm max), electrical table, PUSH_THRD table, QFN outline.
- ams-OSRAM (now Infineon) AS5600L datasheet v1-12 (2020-May-14) (scratchpad as5600l_ds.txt): VDD3V3 3.0/3.3/3.6 V, IDD NOM/LPM1/LPM2/LPM3, OTP burn conditions, Bz 30–90 mT on 1 mm circle, Bz_ERROR 8 mT, INL ± 1°, I²C address 0x40 programmable, typical airgap 0.5–3 mm, max axis displacement 0.25 mm with a 6 mm magnet, WL-CSP Hall array 172.5 µm below chip centre, CONF register; AS5600L eval kit manual UG000345 v2-00.
- Parker O-Ring Handbook ORD 5700 (scratchpad ord5700.txt): §2.3, §6.3.16 silicone rubber, §8.13 Gough-Joule effect (rotary O-ring ID 1–3 % larger than shaft, compression from the gland OD), §8.17 friction, §10.4 twisted O-rings / spiral defects.
- Ulbrich 17-4PH (UNS S17400) datasheet rev 6.1.2015 (scratchpad 174ph_ulbrich.txt): H900 UTS 1310 min, YS 1170 min, Rc 40–48; "strongly ferromagnetic in all conditions".
- Markforged 17-4PH v2 datasheet Rev 1.1 (10/2023) quoting MPIF Standard 35 (scratchpad 174ph_mf.txt): MIM H900 UTS 1190 / YS 1090 / 33 HRC; ASTM A564 wrought H900 UTS 1310 / YS 1170 / 40 HRC.
- C&K/Littelfuse KMR2 datasheet rev 01/30/25 (scratchpad kmr2.txt).
- https://www.lookpolymers.com/polymer_Materion-Beryllium-Copper-Alloy-25-Strip-HT-TH04-Temper-UNS-C17200.php — MatWeb-class mirror of the Materion Alloy 25 strip HT sheet `[V?]`.
- WebSearch (secondary, `[V?]`): REACH Annex XVII entry 27 nickel limits, EN 1811:2023 and EN 12472 — Intertek bulletin, ComplianceGate, iTeh catalogue.
- https://www.aircraftmaterials.com/data/alstst/ams5643.html — 17-4PH AMS 5643 stockist summary `[V?]`.
- https://www.assda.asn.au/publications/technical-faqs/magnetic-effects-of-stainless-steels — ASSDA FAQ (the "< 1.02" statement covers highly alloyed/high-N grades, not 316L).

### 10.3 RF domain
- https://iotdevices.att.com/Uploaded_Docs/radiated_performance_requirements_2_1_20251023050310567.pdf — AT&T IoT Radiated Performance Requirements v2.1 (07/2025): Table 4, Notes 4–6, B17 removal.
- https://www.rxelectronics.jp/datasheet/6b/nrf9160-sica.pdf — nRF91 AT Commands Command Reference Guide v1.9 (4418_963, 2021-11-08), text-extracted: §6.1 %XCOEX0 (COEX0 state per RF frequency range, inverted when RF off, must be sent before modem activity, example `AT%XCOEX0=3,1,1570,1580,1,2000,2180,1,600,800`), §11.2 RX test %XRFTEST, §11.3 TX test %XRFTEST (band, freq, +23…−50 dBm, LTE-M/NB-IoT, QPSK/16QAM/BPSK/CW, RB count/start, system bandwidth, burst mode; %XPRODDONE lock; shielded-room caution).
- https://datasheet.octopart.com/MM8130-2600RB8-Murata-datasheet-141245191.pdf — Murata MM8130-2600 product-search datasheet (2020-06-10): 2.5 ± 0.2 × 2.5 ± 0.2 mm, mounted height 1.4 ± 0.1 mm, Ø2.1 ± 0.2 probe bore.
- Secondary (`[V?]`/`[U]`): https://armoloy.com/plating-specifications/astm-b733/ and https://glecoplating.com/astm-b733-electroless-nickel-specification/ (ASTM B733 Types I–V, SC classes); https://www.compelma.com/en/spring-finger-contacts-for-dummies/ (spring-finger class data); Coilcraft 0402DC product page headline; galvanic-series summaries; CTIA test-plan fee snippet; DevZone thread 58870 and nRF Connect SDK coexistence pages (COEX0 snippets).
- Attempted and blocked (403/redirect): docs.nordicsemi.com %XRFTEST and %XCOEX0 pages; infocenter.nordicsemi.com; ecfr.gov 47 CFR §27.53; Nordic nRF9151 PS electrical chapters; Harwin/TE finger datasheets; Coilcraft 0402DC datasheet; ASTM B733/B488 and 3GPP TS 36.101 themselves.

### 10.4 Mechanical domain
- ATI 17-4 Technical Data Sheet (ati_17-4_tds_en_v2.pdf): "Magnetic Permeability — Strongly Ferromagnetic in all Conditions"; martensitic in annealed and aged conditions.
- TI BQ25180 datasheet SLUSE99C (Sept 2021, rev. Jan 2023): TS thresholds VT1–VT10, TS_ICHG 0.5×/0.2×, TS_VRCG −100/−200 mV, charging and safety timers suspended beyond HOT/COLD; NTC β 3435 / 10 kΩ; ITS_BIAS 38 µA.
- UN Manual of Tests and Criteria, Sub-section 38.3 (PRBA copy of the 6th revised edition with corrections): 38.3.4.1 T1 altitude; 38.3.4.2 T2 thermal; pass criteria.
- INFICON Application Note "Leak Testing for Ingress Protection Class IP67" miaq00en-03 (2502): capillary results table; 5·10⁻³ / 3·10⁻² mbar·L/s for ABS/steel + polymer seal; 2·10⁻⁴ / 9·10⁻⁴ for aluminium + polymer; parts tolerate only 100–200 mbar; "Tracer gas leak testing is the method of choice".
- Santoprene 8211-55B100 Product Datasheet (ExxonMobil, 2014, via plastore.it): bonds ABS, PS, PC, PMMA, ASA, PET, PPO/PS; Shore A 53; compression set 55 % at 125 °C/70 h; no 70 °C value.
- Wiha Tools "Typical Dimensional and Torque Specifications of Torx Tools": T1 0.02–0.03, T2 0.07–0.09, T3 0.14–0.18, T4 0.22–0.28, T5 0.43–0.51, T6 0.75–0.9 N·m.
- Commission Notice C/2025/214 on Article 11 of Regulation (EU) 2023/1542 (EUR-Lex OJ C_202500214): "an IP rating alone is considered as not sufficient"; five cumulative indicators; EN 45554 tool categories; specialised tool "provided free of charge with the product" acceptable.
- EUR-Lex CELEX:32023R1542 Article 11 (previous pass); Art. 96 application date 18 Feb 2027 via secondary summaries only `[V?]`.
- Henkel LOCTITE AA 3106 Technical Data Sheet (search extract); 3M Scotch-Weld DP8005 Technical Data Sheet (search extract); 3M Optically Clear Adhesive 8146-x Technical Data (Nov 2013, DigiKey mirror) and 3M CEF05xx/8146-x document (search extract: 8146-6 = 150 µm).
- Keystone Compliance (Applus+) IP5X/IP6X page and Kingpo "IEC 60529 dust test IP5X vs IP6X" page (IP6X category-1 method) — standard itself not opened `[V?]`.
- Search extracts on IEC 60068-2-11 Ka vs IEC 60068-2-52 Kb — standards not opened.
- Parker O-Ring Division literature list (ORD 5712; low-temperature FKM bulletins V1289-75, VG109-90, VX365-90) — located, not opened.
- ifan-display.com "1.1 inch OLED Screen AMOLED Module 126x294" product page: 12.96 × 30.94 × 0.784 mm, AA 10.962 × 25.578, RM69310, 27-pin FPC, −20…+70 °C operating — vendor page, not a drawing `[V?]`.
- lipobattery.us LP602543 650 mAh page: 6.0 × 25 × 43 mm, 2.405 Wh — reseller datapoint `[U]`.

### 10.5 Not opened by anyone (and therefore `[U]`/`[V?]` wherever cited)
RM69310 driver datasheet; TPS65631-class PMIC datasheet; nRF9151 PS electrical chapters and HIG; 3GPP TS 36.101/36.124; FCC 47 CFR §27.53/§24.238; ASTM B733/B488/A342/A564/A967; AMS 5643/2488; MPIF 35; MIL-A-8625; IEC 60529/60068-2-x/61000-4-2/62133-2/62368-1; ISO 815/3160-2/4892-2/9227; EN 1811/12472; REACH Annex XVII text; IATA DGR PI 967; Materion Alloy 25 datasheet (mirror only); Coilcraft/Murata inductor Q curves; finger datasheets; heat-set insert datasheets; TPS62840 Table 1 re-read; SPI NOR datasheet; cell vendor datasheets; Dow/Momentive self-bonding LSR datasheets; PC/ABS and optical PC TDS; KDB 447498; CTIA OTA test plan.

### 10.6 Electronics domain (second pass, merged 2026-09-19)
- `C:\Users\chian\Projects\bingbong\REDESIGN_DECISION_2026-09-12.md` — §3 block diagram (lines 94–200; /MR ← dial press at line 130), §4 BOM (201–284; BQ25180 row 210: SLUSE99C Rev C, IN abs max 25 V, IQ_BAT 4 µA pushbutton-enabled), §5 power budget, §6.2, §6.3, §9, §10, Addendum A.1–A.2 (733–750; re-read this pass: RTT the only console; 2.54 mm pitch basis "wearable-charger de facto standard"; SWD "clamp takes it instead" `[U]`; production programming "then APPROTECT locked" on the bare board; recover by full erase).
- This report (first issue) — §0, §3 C-1…C-21, §4 Design steps 13/17–19, §5 Steps 8–15 and M10–M14 (M14 re-read this pass: "factory-mode command over the dock's SWD/RTT … `%XPRODDONE` issued only after pass"), the first-issue §6, §7 Steps 4–6, 11 and Phase 5 (re-read this pass: "sleep current 1 in 20 via SWD/PPK2 (< 200 µA after 60 s)").
- `firmware\bingbong_pcb\_mech\nrf9151_ps.txt` — nRF9151 PS v1.0 front-matter extract; grep this pass for pitch/SPIM/MAGPIO/COEX/SIM voltage returned nothing → those items stay `[V?]`/`[U]`.
- `bom-scratch\fh12.txt` — Hirose FH12 0.5 mm FFC connector catalogue extract (opened this pass): FH12-10S-0.5SH (A 4.5 / B 8.1 / C 9.1 mm) and FH12-12S-0.5SH (A 5.5 / B 9.1 / C 10.1 mm) both listed; standard height 2 mm, 2.4 mm with strengthened lock; depth not in the extract.
- Glob of `*.txt` across the project (this pass): no BQ25180, TPS65631, TPS22916, RM69310, MAX17048 or DRV2625 text extracts exist; those parts stay at the decision doc's tags or `[U]` (no PDF opened per the tool-call rule).
- https://www.ti.com/product/TPS65631 (HTML product page, previous pass): VIN 2.9–4.5 V; VPOS 4.6 V fixed; VNEG −1.4…−4.4 V programmable, −4 V default, digital control pin (CTRL); 250 mA; 3 × 3 mm WSON — `[V?]`.
- https://www.ti.com/product/TPS22916 (HTML product page, previous pass): VIN 1–5.5 V; RON 60/100 mΩ; IQ on 0.5/1 µA, off 10/100 nA; reverse-current blocking −300 nA max; slew C 1400 µs @ 5 V (≈ 3000 µs @ 1.8 V per the reviewer's reading of the same page); WCSP 0.4 mm pitch — `[V?]`.
- https://www.ti.com/document-viewer/TPS62840/datasheet (TI HTML datasheet viewer, previous pass; features only): 60 nA operating / 25 nA shutdown; RSET table not reached — 71.5 kΩ stays `[V?]`.
- `firmware\bingbong_pcb\BOM_VALIDATION_2026-09-04.md` and `SCHEMATIC_REVIEW_2026-09-03.md` — `datasheets\ER-OLED018-1_Series_Datasheet.pdf` is the old 1.8" SSD1326 PMOLED, not the RM69310.
- Hostile review of the electronics first draft (14 findings, 10 missing steps, 7 mis-tags) — all dispositions in §6.1.1.
- Not opened by the electronics pass (kept at the decision doc's tags or `[U]`): SLUSE99C (BQ25180), SLVSEC6D (TPS62840), SLOS879C (DRV2625), 19-6171 (MAX17048), SLVSDC7H (DRV5032), IQS211B v2.8.1, nRF91 AT Commands v1.9, Nordic nRF9151 HIG/PS chapters (docs.nordicsemi.com returned 403), RM69310 datasheet, TPS65631/TPS22916 datasheets, IPC-4552/4761, ASTM B488, EN 301 489-1/-52, EN 55032/55035, ISO 7816-3.

---

*End of report. File: `C:\Users\chian\Projects\bingbong\DESIGN_MANUFACTURING_REPORT_2026-09-19.md`. No project file other than this one was created or modified.*

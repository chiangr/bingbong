# Bingbong BOM Validation - 2026-09-04

**BOM under review:** `bingbong_pcb/BOM_2026-09-04.csv` - 48 lines, 104 reference designators, 8 DNP
placements, 96 purchasable placements across 46 lines resolving to **39 distinct usable MPNs plus 4
lines with no MPN at all**. Regenerated 2026-09-04 from the current schematic, MPNs merged forward by
refdes from the stale 2026-03-16 workbook.

**All stock figures are snapshots observed 2026-09-08 unless stated otherwise. They will move. Re-pull
before any PO.**

> **Session caveat.** This report is assembled from six research passes plus verification. The working
> copy (`C:/Users/chian/Desktop/bingbong_software/bingbong_pcb/`) was **not accessible** when this
> document was written, so every claim sourced to a local file (`bingbong.kicad_pcb`,
> `bingbong.kicad_sch`, `_t12.nets`, `_dsx/*`, `_bg95.pdf`, `_r1200_ds.txt`, the `_bomaudit_*.py`
> scripts) is carried forward from the passes that did read them and is marked accordingly. Web-sourced
> lifecycle and stock claims carry their URLs and were independently checked.

---

## THE CONCLUSION, FIRST

**Do not order from this BOM, and do not send this board to fab.** Two independent failures:

1. **The MPN column is wrong on at least seven lines.** Value changes made on 2026-09-04 did not
   propagate through the carry-forward merge - only deletions did. C6/C21 are off by 1000x, L1 is the
   wrong value *and* package *and* component class, C10/C13 and C15 are the wrong package and voltage,
   R11/R13 carry the old 1 k, and the nine-resistor 100 k line carries two contradictory part numbers
   in one cell.
2. **`bingbong.kicad_pcb` was never re-synced with the 2026-09-04 schematic.** 28 parts the BOM buys
   have no footprint on the board - the entire RF pi (C30-C43), five of eight ESD diodes (CR4-CR8),
   the GNSS connector J8, and R24/R31-R37 - while all nine parts deleted today are still placed. A CPL
   exported today would instruct the assembler to fit the exact nine parts you cancelled and silently
   omit 28 BOM lines. `[SUSPECTED - local-file analysis, not re-verified in this session. Run
   Update PCB from Schematic and read the change list; it takes one minute and settles it.]`

The BOM is internally consistent with the schematic (104/104 refdes, quantities, values, footprints and
DNP flags all check out). It is inconsistent with the artifact a fab actually builds from, and its MPN
column is not trustworthy.

---

## 1. BLOCKERS - fix before ordering anything

| Refs | Current MPN | Problem | Action |
|---|---|---|---|
| **PCB (all)** | n/a | Layout never re-synced. 28 BOM parts unplaced (C30-C43, CR4-CR8, J8, R24, R31-R37); 9 deleted parts still placed (C12, C19, C20, Q2, Q3, R10, R29, R30, U7); one stray `REF**`. PCB also records Q2 as **FDN340P** while the workbook ordered **FDN338P**. | Update PCB from Schematic (F8) with "delete extra footprints", re-route, re-DRC, then regenerate BOM **and** CPL from the same post-sync database. Substantial layout work - the RF pi and GNSS path are unplaced. Hold PCB1 + stencil until done. |
| **C6, C21** | `C0603C101K5RACAUTO7411` | **1000x error.** `C101` = 10x10^1 pF = **100 pF**; 0.1 uF is `104`. The row's own LegacyDesc already reads "100 pF ±10% 50V X7R 0603" and contradicts its Value cell. These are the +3.3 V bypass for the ESP32-S2 module (U10 pin 2) and the SN74AVC2T245 VCCB. **`7411` is a real bulk-pack suffix, so a pasted PO orders the wrong part rather than erroring** - worse, not better. | Replace with **C0603C104K5RACTU** (0.1 uF ±10% 50 V X7R 0603, Active, ~8.4 M @ DigiKey). Alt: Samsung **CL10B104KB8NNNC** (DigiKey 1276-1000-1-ND, Active, LCSC C1591). If you want the same packaging code, **C0603C104K5RAC7411** is a one-character-group edit. Strip `7411` from the MPN column BOM-wide. |
| **L1** | `MLZ1608A2R2WTD25` | **Four defects on one line.** Schematic 3.3 uH / L_1008_2520Metric; MPN is 2.2 uH, 0603, and a **multilayer ferrite decoupling** part, not a power inductor; **and the PCB still carries L_0603_1608Metric / 2.2 uH**. Duty is the TPS62172 switch node (ILIMF 1.35 A max). TDK's own page rates MLZ1608A2R2WTD25 at **130 mA** rated current (DigiKey shows 500 mA - that is saturation) - roughly 4.6x under-rated. | **Murata DFE252012F-3R3M=P2**: 3.3 uH ±20%, DCR 135 mOhm max, Isat 2.5 A max, Itemp 1.8 A, 2.5x2.0x1.2, shielded flat-wire metal-alloy, -40..+125C. LCSC 5,140 @ $0.197. Second source **TDK VLS252012HBX-3R3M-1**. **Fix the PCB footprint - the layout is the real blocker.** Note z-height grows 0.8 -> 1.2 mm. **Reject DFE201610P-3R3M** named in the change note: it is 2.0x1.6 mm and does not fit a 2520 land. |
| **R2, R6, R9, R15, R16, R31, R32, R33, R35** | `RC0402JR-0710KL/RE0402FRE07100KL` | Two part numbers in one cell. `RC0402JR-0710KL` = **10 k ±5%** (10x error). `RE0402FRE07100KL` = 100 k ±1%, electrically correct, but Yageo RE is a low-volume precision grade with no readable stocked listing. At **R33** (top leg of the MCP73871 VPCC divider) fitting 10 k moves the foldback knee from 4.29 V to **1.54 V** and silently disables the feature. | Specify **RC0402FR-07100KL** (100 k ±1%, 0402, Yageo RC thick film, 100 ppm/C). LCSC C60491, 3,594,500 in stock; DigiKey 726526; deep multi-source. Strike `RC0402JR-0710KL` from this line. Do not accept a 5% part - R33 needs 1%. |
| **C10, C13** | `GRM158R60J226ME01D` | Schematic footprint is **0805**; part is **0402, 6.3 V**. 6.3 V is wrong for a 3.3 V-bias 22 uF (retains ~20-30%, i.e. 4-7 uF *estimate*) - the reason the schematic moved to 0805. Murata also flags this part "Limited Application: for consumer equipment only". Same MPN as deleted C20. | **GRM21BR61C226ME44L** (22 uF ±20% **16 V** X5R 0805). DigiKey ~111,494; JLCPCB C86817. 16 V derates least at 3.3 V. Avoid the 10 V sibling GRM21BR61A226ME44L - contradictory stock reads on the same day. |
| **C15** | `GRM155R61A106ME11D` | Schematic footprint **0603**; part is **0402, 10 V**. C15 is the raw **USB VBUS** bypass (all four J2 VBUS pins + both MCP73871 IN pins). 10 V on VBUS is only 2x, and hot-plug ringing overshoots. At 5 V bias it holds ~2-3 uF (*estimate*) of a marked 10 uF. | **GRM188R61E106MA73D** (10 uF ±20% **25 V** X5R 0603). Mouser 1.5 M / DigiKey 1.15 M / LCSC 384 k, Active. Second source Taiyo Yuden TMK107BBJ106MA-T. Use the same part at C8 and merge two lines. |
| **R11, R13** | `AF0402JR-071KL` | Value changed 1 k -> 680 R; MPN is still the **1 k** part, and the row's own LegacyDesc says "1 kOhms ±5%". Worse: **the same MPN is legitimately on the R3/R12/R36 1 k line**, so anyone consolidating by MPN orders 5x 1 k and nothing for the 680 R positions, with no error raised. | **RC0402FR-07680RL** (680 R ±1%, 0402). **Do NOT order `AF0402JR-07680RL`** - that PN was constructed by decoding the AF series convention and could not be found at any distributor. Verified 680 R 0402 alternatives: RC0402FR-07680RL (DK 726654), AC0402FR-07680RL (DK 5895472, AEC-Q200), RC0402JR-07680RL (RS 1995428). |
| **J5 + display** | `--` (connector), no line at all (display) | The entire display subsystem is unbuyable from this file. J5's MPN cell is literally `--`; the **ER-OLED018-1 panel does not exist as a BOM line** despite being the second most expensive item in the build (~$11.21) after the BG95. | Add both as explicit lines - see §2. |
| **TH1** | `ND03N00103K--` | **Three-way mismatch.** MPN is a radial leaded 10 k NTC **disc** (3.5 mm dia, 2.54 mm lead pitch, 35 mm leads). Schematic footprint is `Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical` - a **2.00 mm JST PH connector land** the leads cannot fit. PCB footprint is a third thing: `PinSocket_1x02_P2.54mm`. SchDescription says "External battery NTC **connector**". The trailing `--` is legitimate (Kyocera bulk packaging code), not corruption. | Decide what TH1 is. Most likely a **connector**: buy **JST B2B-PH-K-S(LF)(SN)** (DigiKey 926611 / 608703, LCSC C131337) and add a separate off-board pigtail line (NTC + PHR-2 + 2x SPH-002T-P0.5S). Delete the ND03 from the placement line. Separately: no RT1/RT2 network exists, and this NTC's beta is 4080 vs Microchip's 3892 worked example - the THERM window is currently **undefined**. Recompute per MCP73871 §6.0 or populate R24 and accept that thermal qualification is off. |
| **C26, J2** | `8.85012206055E11`, `1.054500101E9` | **Excel float coercion.** Arithmetic confirmed exactly: `float("8.85012206055E11") == 885012206055` (Wurth 220 pF 25 V X7R 0603) and `float("1.054500101E9") == 1054500101` (Molex USB-C receptacle). Unorderable as written. Same coercion destroyed LegacyPkg BOM-wide (`402.0`, `603.0`, `805.0`, `1206.0`). | Rewrite both cells as text; format MPN/DigiKey/LegacyPkg as strings on export or stop round-tripping through .xlsx. **Recoverable in the meantime** - both rows still carry valid DigiKey PNs (732-7974-1-ND, WM12856CT-ND). |

---

## 2. Parts with NO source yet

| Item | Recommended MPN | Price / lead | Confidence |
|---|---|---|---|
| **Display module (no refdes; legacy row 49)** | **ER-OLED018-1W** (white) or `-1B` (blue), EastRising / buydisplay. 1.8in 256x32, SSD1326U3R1, -40..+85C, **integrated FPC tail - no separate FFC cable needed**. | US$11.21, ~$10.00 in volume; >500 pcs needs a quote. **No published lead time.** | `[SUSPECTED]` buydisplay.com returns HTTP 403 to automated fetch; price is from a search-index snapshot 2026-09-08. **No manufacturer lifecycle status is published** - "listed and priced" is not "Active". Sole-source, zero authorized distribution. https://www.buydisplay.com/white-1-8-inch-256x32-oled-display-module-serial-i2c-and-ssd1326 |
| **J5 ZIF connector** | **ER-CON26HT-1**, 26-pin 0.5 mm, **CONFIRMED TOP contact** (the `HB` sibling is bottom). | Legacy $0.16 - **unverified and carried forward**. MOQ/lead unknown. | `[CONFIRMED]` top/bottom orientation from buydisplay's own page titles. `[UNVERIFIED]` price/stock/lead - findchips returns **zero** legitimate hits across all authorized and independent distributors. https://www.buydisplay.com/26-pin-0-5mm-pitch-top-contact-zif-connector-fpc-connector |
| **J5 second source** | **Hirose FH12A-26S-0.5SH(55)** = **TOP** contact, 2.0 mm high, 6.2 mm deep, DigiKey 1,940 @ $2.37/1, Mouser 1,132. Bottom-contact sibling FH12-26S-0.5SH(55): Mouser 3,510, Newark 2,058 @ $1.83. | ~$1.90-2.60 vs the claimed $0.16 - buys an authorized supply chain and a documented land pattern. | `[CONFIRMED]` The project's own `Conn_Zif_26Pin.kicad_mod` has 26 pads at 0.5 mm spanning exactly **12.5 mm**, matching Hirose's 26-pos contact span. Check ear span (16.1 vs 16.35 mm) and body depth (5.6 vs 6.2 mm); leave 6.2 mm keepout so either fits. FH12 is rated **20 mating cycles** - do not re-seat the FPC repeatedly at bring-up. **Avoid plain FH12-26S-0.5SV (no suffix) - obsolete.** |
| **E2 - cellular antenna (J3 / BG95 ANT_MAIN)** | **TE/Linx ANT-LTE-RPC-UFL**. **600 MHz - 3.8 GHz** (not 617-4200 as stated elsewhere in the passes). Ground-plane-independent dipole - **no counterpoise**. 98.4 x 14.9 x 0.8 mm, 3M 9888T adhesive. Covers **B71**, which T-Mobile US uses for NB-IoT. | DigiKey CA **4,561** @ $8.37 CAD/1, **8-week** lead. | `[CONFIRMED]` stock/price. `[DISPUTED]` lifecycle: TE and DigiKey both say Active, but **TTI shows "Reference Only / in transition" and OnlineComponents says "no longer being manufactured"**. Get a written lifecycle statement from TE/Linx before an 8-week buy and qualify the second source in parallel. **Watch temp: -20..+65C**, narrower than the BG95 and the OLED. https://www.digikey.ca/en/products/detail/te-connectivity-linx/ANT-LTE-RPC-UFL/11314387 |
| **E2 alternates** | **Quectel YF0006PA** - 50 x 25 mm, dipole, ground-independent, 698-960 / 1710-2690, MHF1. **DigiKey: Active, 5,249 in stock, EUR 1.65 @1, 4-week lead.** Loses B71. **Pulse W3907B0100** - 698-3600, -40..+85C, DigiKey CA 4,278 @ $8.98, 9 wk; also no B71. | | `[CONFIRMED]` YF0006PA is the **cheapest and shortest-lead of the three** and half the length - if the CAD mock-up is tight it may be the right primary, not the fallback. |
| **E3 - GNSS antenna (J8 / BG95 ANT_GNSS)** | **Quectel YFGA003AA**, passive GNSS L1, 39.45 x 13.25 x 0.13 mm, 100 mm coax, MHF1. VSWR 1.1, eff 58-61%, peak gain 3.2-3.5 dBi - **passes every line of BG95 Table 34**. | DigiKey CA **3,237** @ $2.36 CAD/1, $1.53 @1000, **4-week** lead, Part Status **Active**. | `[CONFIRMED]` distributor data. `[SUSPECTED]` the passive-vs-active conclusion: Quectel's BG95 HW Design §5.5.1 reportedly recommends a **passive** antenna when B13 is supported (BG95-M3 is), and Fig 32 note 2 says the VDD bias tee is not needed for passive - so **no bias tee, no schematic change, the bare pi is correct**. Cited to local `_bg95.pdf` only; not independently re-read. **Confirm the datasheet's ground-plane clearance requirement** (~10 mm is typical for this class) before assuming it "fits". |
| **E1 - 2.4 GHz antenna (ESP32-S2-**SOLO-2U** on-module U.FL)** | **Molex 1461530150**. 34.90 x 9.00 x **0.10 mm**, 150 mm micro-coax to MHF1, 2.4-2.5 GHz, >72% total efficiency, 2.8 dBi, ground-plane independent, peel-and-stick. | DigiKey CA **22,221** + 4,800 factory @ $4.55 CAD/1, **9-week** lead, **Active**. | `[CONFIRMED]`. Beats the legacy Molex **1461539150** (also Active, 7,150 @ DigiKey, but **18-week** lead, 2.00 mm thick vs 0.10 mm, and a Wi-Fi 6E tri-band part wasted on a 2.4 GHz-only radio). The legacy part was never purchased so nothing is stranded. Backup: Taoglas FXP73.07.0100A, 8,440 @ $7.97 CAD, 16 wk. Note 1461530150 is dual-band 2.4/5 - single-band siblings in the same 146153 family are worth a look if area is tight. |
| **Battery (BT1; legacy row 48)** | **Do not carry ASR00035 forward.** Re-source: any 600-1000 mAh Li-ion pack from a real cell maker with a **published PCM over-current trip**, ordered with a **JST SHR-02V-S-B** pigtail; or change J4 to JST PH and buy a mainstream PH-terminated pack. | ASR00035 was $6.95. | `[CONFIRMED UNBUYABLE]` DigiKey .ca and .co.uk both return "This product is no longer available at DigiKey"; TinyCircuits shows Sold Out; **Mouser 406-ASR00035: 0 on hand, 590 on order, 13 wk factory lead, USA-only shipping** (2026-09-08). No manufacturer EOL notice was published, so it is *delisted*, not confirmed obsolete. **Drop the "under-rated at 1C" argument** - the PCM trip is unpublished and both datasheet PDFs are unreadable; 600 mA from a 500 mAh pouch is 1.2C, ordinary. The real reasons to re-source are the delisting and the 1.0 mm JST SH termination most commodity packs do not carry. Ignore broker listings. |
| **R34** (40.2 k 1%, MCP73871 VPCC lower leg) | **Yageo RC0402FR-0740K2L** (40.2 k ±1%, 0402, 62.5 mW, 100 ppm/C). DigiKey 311-40.2KLRCT-ND / -LRDKR-ND. Second source **Uni-Royal 0402WGF4022TCE** (LCSC C25893 / TME). | ~$0.01. | `[CONFIRMED]` part identity and duty. `[UNVERIFIED]` stock - **DigiKey cached pages read both "ships today" and "out of stock/backorder"; RS UK 198-7788 reads "currently unavailable, no known restock date"**. Check the live page before ordering. **1% matters:** with both legs at 1% the VPCC knee holds ~4.10-4.48 V (including the MCP73871's own ±3% VPCC threshold tolerance). With both at 5% it spreads to ~4.00-4.61 V: at the high corner the charger folds back on a normal 4.75-4.8 V hub port and never fills the cell; at the low corner foldback never engages. **Value-code hazard:** `-0740K2L` = 40.2 k, `-07402RL` = 402 R, `-07402KL` = 402 k, `RC0201FR-0740R2L` = 40.2 R. Three of those are a 1000x error waiting to happen and two are stocked. |
| **C31, C34** (15 pF C0G 0402, RF pi **series** elements) | **Murata GJM1555C1H150JB01J** (15 pF ±5% 50 V C0G 0402) - GJM is Murata's high-Q RF line. **Do not substitute a GRM or GCM C0G**: identical on paper, worse Q and ESR in a matching network. Second source Kyocera AVX 04025A150JAT2A. | DigiKey listed, "ships today" (search-index snapshot). Order the `J` reel code - the `...JB01D` bulk suffix did not surface in stock listings. | `[CONFIRMED]` part. `[OPEN DESIGN QUESTION]` the **value**: at 15 pF the series reactance is 15.2 ohm at 700 MHz into a 50 ohm line. If the SchDescription's "DC block" is literal, 15 pF is far too small (a 700 MHz DC block wants >=100 pF). If it is a matching element, 15 pF is a plausible starting value. Four DNP shunt positions surround these two series positions, i.e. the topology is explicitly a tunable pi - so **action this as "record an MPN and confirm on a VNA at bring-up", not as "the 15 pF is wrong"**. |
| **C32, C33, C35, C36** (DNP - RF pi shunts) | Record **Murata GJM15 series** as the named stuffing family. Buy a tuning kit spanning 0.5-10 pF: **GJM15-KIT-DE-1** (Murata's own 0402 GJM C0G design kit, 20 pcs each) is cleaner than four reel line items. Plus 0 ohm 0402 jumpers. | Kit, not reels - `...BB01D` is a 7-inch paper-tape reel code. | `[CONFIRMED]` family. Not purchased for build 1; the deliverable is recording the family and range so the line is not empty at handoff. |
| **C41, C42, C43** (DNP - SIM EMI shunts) | **33 pF C0G 0402 50 V**, *not* 22 pF. Quectel's BG95 reference (Fig 21) specifies 33 pF, and states verbatim **"the 33 pF capacitors are used for filtering interference of EGSM900"** - so with EGPRS dropped their stated purpose no longer applies and DNP is now *justified*, not an unexplained gap. Record that rationale in Status. **Samsung CL05C330JB5NNNC** or Murata **GRM1555C1H330JA01D** - either is fine, pick on price. | | `[SUSPECTED]` the 33 pF figure and the EGSM900 quote are cited to local `_bg95.pdf` p.48-49 only. `[CORRECTED]` an earlier claim that Murata was "thinning in the channel" does **not** hold: LCSC is out of stock but **DigiKey 3693846 ships today and Arrow has stock** - do not reverse primary/alternate on that basis. Note ETSI/Quectel budget the USIM ESD parasitic at <=15 pF; do not go above 33 pF if you ever populate these. |
| **J6** (1x05 2.54 mm debug header) | **Recommendation: do not buy it. Convert to five labelled test pads.** It is a pure power-rail tap (GND, +1.8 V, +3.3 V, +5 V, +12 V) with **zero signals**, forces a THT operation on an all-SMT board, and puts **+12 V immediately adjacent to +1.8 V on unkeyed, unshrouded 2.54 mm centres** - one slipped probe puts 12 V on the BG95's 1.8 V rail. If pads are kept, reorder so +12 V sits at one end next to GND. | If retained for bring-up: **Wurth 61300511121** (DigiKey 4846831, 30,254 @ $0.25) or **Sullins PRPC005SAAN-RC** (DigiKey 2775249, $0.35). Both Active, in stock 2026-09-08. | `[CONFIRMED]` alternates real and orderable. **`[CONFIRMED]` J6 carries NO `(dnp yes)` in the schematic and its BOM DNP cell is empty** - contrary to the brief's "deliberately not populated", it currently counts as a purchasable placement with no MPN. Pick one and record it. Useful side-finding: **+1.8 V comes from U2.29 (BG95 VDD_EXT), not from the deleted U7** - deleting the MIC5504 did not orphan that rail. |
| **Bare PCB (PCB1)** | JLCPCB **JLC04161H-7628**, 4-layer, ENIG, 37.50 x 120.00 mm. Real JLCPCB controlled-impedance stackup, correct for the 50 ohm coplanar RF the BG95 requires. | `[UNVERIFIED]` - the quote engine is a JS app. Quote at cart.jlcpcb.com with impedance control on **and the stencil in the same cart**. Impedance control + ENIG is not a "standard parameters" order and triggers engineering confirmation, adding build days. | **Do not order until the layout is resynced.** |
| **Stencil (STENCIL1)** | Laser-cut stainless, 0.12 mm (4 mil), **top side only**, frameless is fine for protos. Aperture reduction on the 0.4 mm-pitch UQFN (U3); **windowpaned, not solid, apertures on U6 and U8 exposed pads**. | `[UNVERIFIED]` JLCPCB advertises a $1 first stencil for new accounts. | This board *should not* be hand-pasted: U3 is 0.4 mm-pitch 10-UQFN, U8 is 0.5 mm 20-VQFN with EP, U6 is 8-WFDFN with EP, 39x 0402, plus the BG95 LGA. Buy in the same cart as PCB1 so fiducials and panel data match. Confirm top-side-only **after** the resync. |
| **Mounting hardware / enclosure** | **None found - and none can be fitted.** The PCB has **zero MountingHole footprints**; the only three np_thru_holes are SW1's Cherry MX alignment posts. Six anonymous 2.2 mm plated GND holes exist in the layout with empty refdes/library/value, plus one annotated `REF**` on a TestPoint footprint. CAD exists (`bingbong_case_1/2.SLDPRT`, `helical_pcb_stand.SLDPRT`, `bingbong_btn_ext.SLDPRT`) but SolidWorks binaries are not machine-readable. | n/a | `[SUSPECTED - local analysis]`. **Adding at least two MountingHole footprints before the next spin costs nothing now and cannot be added after fab.** Open the assembly and answer: how do the case halves join, what retains the PCB, and is `bingbong_btn_ext` printed or purchased. Then add the fasteners and the enclosure as BOM lines. |
| **SW1 keycap / actuator** | **None found.** A bare MX switch has no actuating surface as ordered. `bingbong_btn_ext.SLDPRT` implies a custom actuator with no BOM line. | n/a | Add a keycap or enclosure plunger as a purchasable line. Also sanity-check the fit: an MX switch is ~15.6 x 15.6 mm at the plate, ~11.6 mm tall before a keycap adds ~10 mm, and needs a 14 x 14 mm plate cutout - on a 37.5 mm-wide handheld that is very likely the dominant mechanical constraint. |
| **Bring-up SIM** | **None on the BOM.** J7 is a nano-SIM socket and U2 is an LTE-M/NB-IoT modem; a board with no SIM cannot be proven to attach. | Add a Hologram / Twilio / Soracom developer SIM as a bring-up line. | Not an assembly item, but a bring-up blocker. |
| **Off-board / harness** | **None on the BOM.** Missing: the cell, the **JST SH mating housing + crimps** (SHR-02V-S-B, DigiKey 455-1377-ND; SSH-003T-P0.2, DigiKey 700389/27687549), the **JST PH housing + crimps** for the NTC lead (PHR-2, 455-1165-ND; SPH-002T-P0.5S, 455-1127-1-ND). | All confirmed real and orderable 2026-09-08. | Two practical notes: the **SSH-003T-P0.2-H** variant reads 0 stock with a **16-week** lead - specify the base part or buy **pre-terminated ASSHSSH28K jumpers**, because 1.0 mm-pitch SH crimping is impractical by hand (the JST WC-240 hand crimper is ~$537). SPH-002T-P0.5S is 24-30 AWG; if the NTC pigtail is finer, use **SPH-004T-P0.5S** (32-28 AWG). |

---

## 3. Lifecycle and stock risk register

Sorted by risk. Every row marked `[CONFIRMED]` / `[SUSPECTED]` / `[UNVERIFIED]`. All quantities are
**2026-09-08 snapshots**.

### BLOCKER

| Refs | MPN | Lifecycle | Stock (2026-09-08) | Risk | Action |
|---|---|---|---|---|---|
| PCB | n/a | n/a | n/a | Layout desync - board is a different design from the BOM | `[SUSPECTED]` Resync, re-route, re-DRC before anything. Local analysis, not re-verified here. |
| C6,C21 | C0603C101K5RACAUTO7411 | **Active** `[CONFIRMED]` | Alt C0603C104K5RACTU: ~8.4 M DigiKey; ~10 M aggregate `[SUSPECTED - search-index]` | Wrong part, 1000x, and *orderable* as written | Swap to C0603C104K5RACTU. https://www.arrow.com/en/products/c0603c101k5racauto/kemet-corporation ; https://www.digikey.com/en/products/detail/kemet/C0603C104K5RACTU/1465594 |
| L1 | MLZ1608A2R2WTD25 | **Unknown** `[UNVERIFIED]` - product.tdk.com 403s to automated fetch | n/a - delete from BOM. Alt DFE252012F-3R3M=P2: **LCSC 5,140 @ $0.197** `[CONFIRMED - read live]` | Wrong value+package+class+rating; PCB land also wrong | Murata DFE252012F-3R3M=P2 + fix the footprint. https://www.lcsc.com/product-detail/C2041573.html ; https://www.murata.com/~/media/webrenewal/products/inductor/chip/tokoproducts/wirewoundmetalalloychiptype/m_dfe252012f.ashx |
| R2 group (9) | RC0402JR-0710KL / RE0402FRE07100KL | Both **Active** `[CONFIRMED]` | Wrong one: LCSC C60489 4,288,100. Right one: **no readable stocked listing anywhere**. Alt RC0402FR-07100KL: LCSC C60491 **3,594,500** `[CONFIRMED - read live]` | 10x error at R33 kills VPCC foldback | RC0402FR-07100KL. https://www.lcsc.com/product-detail/C60491.html ; https://www.digikey.com/en/products/detail/yageo/RC0402FR-07100KL/726526 . *Caveat: the "RE = 20 wk, not stocked" evidence is from a **different** RE part (RE1206FRE07470KL) and JLCPCB does carry an RE 0402 100 k - so "RE is unstockable" is a reasonable inference, not a fact for this exact PN.* |
| J5 connector | ER-CON26HT-1 | **Unknown - no status published** `[CONFIRMED absence]` | **Zero authorized-distributor availability**; findchips returns no legitimate hits | Sole-source, zero visibility, on the critical path | Buy 5-10 spares with the display; qualify Hirose FH12A in parallel. https://www.findchips.com/search/ER-CON26HT-1 |
| Display | ER-OLED018-1W | **Unknown - no status published** `[SUSPECTED]` | Listed at $11.21; **live stock never obtained** (403) | Sole-source, small Shenzhen vendor, no distribution, no published lead time | Add as a line, get a written lead time and stock reservation from sales@buydisplay.com **before the enclosure is committed**. Buy 2-3 spares - the ZIF tail is fragile. Also ask whether the ER-CON26HT-1 ships bundled (their AliExpress listing says "Free Connector") - the answer zeroes the J5 cost and tells you authoritatively which contact orientation they intend. |
| Battery | ASR00035 | **Delisted, no EOL notice** `[CONFIRMED]` | DigiKey: "no longer available". TinyCircuits: Sold Out. **Mouser: 0 on hand, 590 on order, 13 wk, USA-only** | Unbuyable through the project's channel | Re-source. Longest pole: re-selection + UN38.3 + air-freight restrictions. https://www.digikey.ca/en/products/detail/tinycircuits/ASR00035/9808767 |
| TH1 | ND03N00103K-- | **Active** `[CONFIRMED]` | Mouser 8,942 @ $0.41; Newark 4,838; DigiKey 3,131 @ $0.46 | Right part, wrong slot - three mutually incompatible representations | Decide connector vs on-board NTC; see §1. https://datasheets.kyocera-avx.com/NTC_DiscThermistors.pdf |
| J8 | CONMHF1-SMD-T | Active | n/a | **Not placed on the PCB** despite being in schematic, netlist and BOM (qty 2) | Resync. Buying 2 is correct; the board cannot accept the second one today. `[SUSPECTED - local]` |
| SW1 | KS-9Y10B060NW-G43 | **Unknown - no lifecycle published** `[CONFIRMED absence]` | **Zero authorized distributors** (findchips: only unrelated APEM/IDEC "KS900B14"). Hobby channel: mechanicalkeyboards.com ~860 @ $0.50; MaxGaming, Milktooth, LumeKeebs, KBDfans | No franchised supply, no PCN process, no RoHS/REACH declaration, no MSL rating, on a commercial handheld | **Buy lifetime spares now** at $0.50 - keyboard switch colourways are discontinued on fashion cycles, not PCN cycles. Electrically and footprint-wise it is correct (5-pin MX PCB mount, 60±15 gf, netlist active-high on press). If MX feel was inherited rather than chosen, re-selecting to a distributor-stocked tact collapses this risk to zero. https://www.findchips.com/search/KS-9Y10B060NW-G43 |

### HIGH

| Refs | MPN | Lifecycle | Stock | Risk | Action |
|---|---|---|---|---|---|
| C10,C13 | GRM158R60J226ME01D | **Active** `[CONFIRMED]` | Arrow **0, 10 wk, 40 k MOQ, 8 k increments** - but DigiKey ships same-day and TME/Farnell/Future/JLCPCB carry it | Package + voltage mismatch. **Note: "supply is thin" was a single-distributor artifact and should not be cited as a reason to change** - the package/voltage mismatch carries this alone | GRM21BR61C226ME44L (16 V 0805). https://www.digikey.com/en/products/detail/murata-electronics/GRM21BR61C226ME44L/4905531 |
| C15 | GRM155R61A106ME11D | **Live catalog part, supply-constrained; NOT EOL** `[CONFIRMED]` | Arrow 28,558 @ 10 wk; TTI 910,000 on order for 29-Jan-27; TME available; Avnet 0 @ 10 wk; DigiKey backorder | Wrong package + wrong voltage class for VBUS | GRM188R61E106MA73D (25 V 0603). *The in-repo `_dsx/GRM155R61A106ME11-01A.pdf` is a saved 404 page - **that is not evidence of anything**; drop it.* |
| C25 | C0603C105K4RACTU | Active `[SUSPECTED]` | See C24 row | **16 V on a +12 V rail.** R1200 datasheet: cap voltage rating must be >=1.5x Vout = **18 V min**. **And the R1200x OVP threshold is selectable 17/19/21 V, so the node can legitimately reach 17 V** - that kills a 16 V part independently of the 1.5x rule and argues for **25 V minimum**. At 12 V on a 16 V 0603 X7R you keep ~0.2-0.4 uF (*estimate*) against the IC's stated 1-4.7 uF minimum. C22's 6-ohm-ESR tantalum contributes nothing at 1.2 MHz, so C25 carries the output filter alone, undersized. | Minimum: **C0603C105K3RACTU** (1 uF 25 V X7R 0603). **Better: move to 0805 25 V** (the R1200 reference part class) so you retain ~0.6-0.7 uF, and/or make C22 an MLCC. `[UNVERIFIED]` alternate availability: **DigiKey shows C0603C105K3RACTU out of stock / backorder and TTI flags "contact factory"** - treat it as specify-and-source, not shelf stock. **Do NOT specify GRM188R71E105KA12D** - DigiKey lists it Obsolete. |
| L2 | MLZ2012P220WT000 | **Active** `[CONFIRMED]` | LCSC C88185 **14,540** @ $0.0719 `[CONFIRMED - read live]`; Farnell 3807746, TME, Arrow | **LCSC states Isat = 100 mA.** Computed peak inductor current from the R1200's own formula at VIN 3.0 V / VOUT 12 V / IOUT 30 mA: 193 mA typ, 201 mA at fosc min, **214 mA at L -20%** - i.e. **~2x Isat**, not merely near the 220 mA rated current. DCR 1.625 ohm max also costs 244 mV and ~8% of boost efficiency at the 150 mA DC point | **The obvious swap is not obviously right.** MLZ2012N220LT000 (same family, same 0805 land, 0.67 ohm / 300 mA) improves DCR and *rated* current but its **saturation current is not established** - swapping P for N may leave the saturation problem intact, and I could not verify it (Farnell/TDK/TME/DigiKey/Octopart all 403 or time out). The defensible fix is **VLF3010A-220** (wire-wound, 330 mA, named in the R1200 datasheet's own Table 2) - but it is **2.8 x 2.6 x 0.9 mm and needs a new land**. Decide during the 4-layer re-layout. |
| C2 (of C2,C11,C29,C39) | JMK105BJ105KV-F | **NRND / renamed by manufacturer** `[CONFIRMED]` - TYCOMPAS shows "is renamed", status "Mass Production (Previous Category)", crossing to MSASJ105SB5105KFNA01. **No published LTB or EOL date** - the earlier "past LTB since 2025-03-31" framing is not established | Deep legacy distributor stock remains | Lifecycle is the *minor* issue. The real one: **C2 sits on /VBAT at up to 4.2 V, which is 67% of a 6.3 V rating** - a 1 uF 6.3 V X5R 0402 retains ~30-40% there (*estimate*). C11/C29/C39 are fine at 6.3 V | **Split C2 out** and use a 16 V part: Murata GRM155R61C105KA12D or Samsung CL05A105KO5NNNC (`[UNVERIFIED]` - not individually checked). Cross the rest to MSASJ105SB5105KFNA01, but **verify orderability first** - that exact code did not surface with a quantity at Mouser or Future; use Taiyo Yuden's stock-check portal. Note C29's EN-rise RC is ~4-5 ms derated, not the nominal 10 ms - still adequate, but don't size on marked values. https://ds.yuden.co.jp/TYCOMPAS/ap/detail?pn=JMK105BJ105KV-F&u=M |
| R26 | ERJ-3GEYJ103V | Active `[CONFIRMED]` | DigiKey 135662, Mouser, Newark 65T8553, TME - deeply multi-sourced. Live quantity `[UNVERIFIED]` (cached snapshots disagree) | **The +12 V setpoint is being trimmed by a 5% resistor.** R26 (10 k, 5%, 200 ppm/C thick film) is the lower leg of the R1200 divider against a 1% thin-film R27 (110 k). With VFB ±1.5% the rail spans **11.20-12.88 V**; at 1% it tightens to 11.61-12.41 V | Split R26 onto its own 1% line: **RC0603FR-0710KL**, or better **RT0603FRE0710KL** to TC-match R27. Costs a few tenths of a cent. **Caveat: the "ER-OLED018-1 VCC window is 11.5/12.0/12.5 V" claim could not be verified (source 403s); the only primary figure obtainable is the SSD1326 controller's 9-15 V, which 11.20-12.88 V does not violate.** The fix is still correct and free. |
| E2 | ANT-LTE-RPC-UFL | **Active at TE and DigiKey, but "Reference Only / in transition" at TTI and "no longer being manufactured" at OnlineComponents** `[DISPUTED]` | DigiKey CA 4,561, 8 wk | Lifecycle signal conflict on an 8-week commitment | Get a written statement from TE/Linx; qualify YF0006PA in parallel. |

### MEDIUM

| Refs | MPN | Lifecycle | Stock | Risk | Action |
|---|---|---|---|---|---|
| U2 | BG95M3LA-64-SGNS | **Active, SUSPECTED** - Quectel publishes no longevity matrix; inferred from continued PCN activity. Newest PCN (PCN202605070003EN01, 2026-05-13) is a **capacity expansion** licensing Huizhou Runtek as a second PCB source, no form/fit/function change | Mouser 2,436 @ $28.55; DigiKey 2,892 @ $29.81 @250; Future 0 @ $18.98/250 with **20-wk** lead. ~5,300 pcs authorized | Fine for build 1. 20-wk factory lead is a production item, and it is quoted by the one source holding **zero** stock. **Ignore the brokers** (Win Source 13,503, Sierra 5,592, IC Components 2,939 @ $13.06) - do not source a cellular module from them | **BG95-M3 is now over-specified.** M1 = Cat M1; M2 = Cat M1 + NB2 + GNSS, no GSM; M3 = + EGPRS. Since EGPRS was dropped, **M2 is the exact functional match** on an identical LGA footprint - zero PCB change. Two arguments for M2: (a) with an M3 fitted, nothing in *hardware* stops firmware or a roaming network putting the radio into GSM and drawing a 2 A burst that C3, the JST-SH and the cell were just downsized away from; (b) **M1/M2/M5 accept 2.5-4.8 V while M3 requires 3.3-4.3 V** - on a single Li-ion running down toward 3.3 V the M2 has strictly wider headroom. Against it: M2 has ~6x less stock (~907 pcs, re-pull before deciding). **Keep M3 for build 1; make the call deliberately before production.** Request a written longevity letter from your Quectel FAE. **Correction to the brief: `-SGNS` is NOT a GNSS suffix** - GNSS is set by the model number and every BG95-Mx has it; `-SGNS` is the generic non-customer-specific build code `[SUSPECTED - Quectel's ordering table is NDA-only]`. There is no cheaper non-GNSS BG95. |
| U10 | ESP32-S2-SOLO-2U-N4 | **Active** `[CONFIRMED]` - datasheet v1.4 Table 1-2 lists it with no EOL marker, while siblings **-2-H4 and -2-N8 are marked "(End of life)"** in the same document and **-2U-N8/-N8R2/-N16R2 were deleted outright in v1.2**. Espressif's convention is a title-page NRND/EOL watermark only when *all* variants are EOL; there is none. ESP32-S2 PCN list (7 PCNs, latest PCN20240602) contains no EOL notice | DigiKey 1,037 ($4.69@1 -> $2.43@650); Mouser 635; TME 0. **~1,670 pcs total authorized** - the thinnest authorized supply of any active silicon here. Unikey shows 13,000 (**broker - flag before use**) | Not a build-1 blocker; a production-schedule item. **The real argument is the trend**: Espressif deleted several 2U variants in v1.2 and EOL'd two -2- siblings. The family is being pruned | Buy build-1 **and** build-2 quantity on one PO. **Qualify ESP32-S2-SOLO-2U-N4R2 now so it is a released alternate, but do NOT count it as inventory** - DigiKey shows **14 pcs**, TME 0. The "12-week factory lead" is extrapolated from the -2-N4 sibling; `[SUSPECTED]` until you pull a quote for this exact MPN. https://www.espressif.com/sites/default/files/documentation/esp32-s2-solo-2_esp32-s2-solo-2u_datasheet_en.pdf |
| C3 | 16ZLH470MEFCT78X11.5 | **Unknown** `[UNVERIFIED]` - Rubycon ZLH is a legacy low-Z series largely superseded by ZLJ; no formal status obtained | not pulled | **Assessment requested: reduce, do not delete.** Quectel asks for "~100 uF with low ESR" on VBAT, not 470 - so 470 uF is ~4.7x oversized for LTE-M/NB-IoT only. **But** BG95-M3's 3.3-4.3 V range leaves only ~0.5-0.9 V of headroom at end of discharge on a single cell, so the low-ESR bulk cap is still doing real work on the current-step edge. Mechanically it is the worst part on the board: an 8 x 11.5 mm can in a handheld, one of only four THT parts, and it vents if fitted backwards | Target a **220 uF 6.3-10 V polymer**. **Correction to the brief's premise: 220 uF at 6.3 V does not exist in a 1210 polymer chip** - Kemet case V = 7343-20, D = 7343-31, so **budget a 2917 land, not 1210**. `[DISPUTED AVAILABILITY]` the obvious pick T520V227M006ATE040 reads **In Stock 0 / $1.80** at DigiKey, and the T520V227M006ZTE040 page carries an "obsolete and no longer manufactured" flag on its main part; the "ships today" text for T520V227M006ZTE025 traces to a **cached page whose footer reads 1995-2022**. Better-evidenced: **T520V227M010ATE040** (220 uF **10 V**, same 2917, 40 mOhm) showed **5,857 in stock @ $2.43** - more margin and actually on the shelf. Disclose the tradeoffs: polymer tantalum is still polarized, still fails short, sits directly across a Li-ion with no current limit, and leaks ~139 uA (`[UNVERIFIED]`) - non-trivial on a 500 mAh cell. **Zero-polarity alternative: 4x 22 uF 16 V 0805 MLCC** (~50-60 uF effective at 3.7 V), non-polar, zero leakage, cheaper, at the cost of bulk energy. |
| C22,C23 | T491A475K025AT | **Active** `[CONFIRMED]` - Kemet/Yageo T491 datasheet rev T2005_T491 dated 2026-07-08 | LCSC ~$0.23 `[search-index]` | **12 V on a 25 V T491 is 48% of rating - that is INSIDE Kemet's commonly-cited 50% rule at normal ambient, so this is a thin-margin argument, not a violation. Do not present it as one.** The substantive points: above +85C the recommended max drops to 33% of VR = 8.25 V, and this is a handheld with a self-heating modem; A-case dissipation is 75 mW which with 6 ohm ESR implies a ~112 mA rms ripple limit against a boost output ripple of ~1.46x Iout; and at 1.2 MHz a 6 ohm ESR makes the part invisible as a filter anyway. C23 sits on the SSD1326 VCOMH node (~10 V) which sees panel power-up inrush - the classic MnO2 ignition scenario. **`[UNVERIFIED]`: the 50%/33% rule, the 75 mW limit and the 112 mA figure - the Kemet PDF would not extract to text. Consistent with well-known Kemet practice but not read.** | Replace both with MLCC in the identical 1206 land: **Samsung CL31B475KAHNNNE** or **Kemet C1206C475K3RACTU** (4.7 uF ±10% 25 V X7R 1206). Removes polarity, vent/ignition, ripple limit and ESR in one move. Expect ~40-60% DC-bias loss at 12 V (~2-3 uF) - still an order of magnitude more useful at 1.2 MHz than 4.7 uF behind 6 ohms. **`[CORRECTED]` CL31B475KAHNNNE is NOT stocked at DigiKey** (In Stock 0 / backorder @ $0.18) - **Mouser holds ~90,369 shipping immediately**, and LCSC is stocked. Buy elsewhere. The Kemet alternate is `[UNVERIFIED]`. |
| C8 | GRM155R61A106ME11D | See C15 - **no distributor obsolescence flag exists** | see C15 | **No BOM-vs-schematic mismatch** - the part matches the 0402 footprint the schematic calls for. This is a design *improvement*, not a defect: /SYS LOAD rides toward VBUS with USB attached, so a 10 V 0402 at ~5 V holds ~2-3 uF; C8+C14+C24 total ~5 uF against TI's recommended 10 uF input cap | Optional: change C8 to **GRM188R61E106MA73D** (25 V 0603) - same part as C15, merging two lines. **Requires a footprint change**, so it competes for board area. `[UNVERIFIED]` TI's reference-BOM "10 uF 25 V 0805" detail and the ~5 uF total. |
| C26 | 885012206055 | Active - current Wurth WCAP-CSGP catalog line `[CONFIRMED specs]` | `[UNVERIFIED]` - DigiKey and Mouser both blocked direct fetch | Three problems: **(1)** MPN mangled (see §1). **(2)** Wrong dielectric - C26+R28 form a series R-C **compensation/noise-filter** across the R1200 feedback divider, sitting at ~11 V DC = 44% of a 25 V X7R rating where it loses ~30-40% and drifts with temperature. **A compensation zero should not move with bias.** **(3)** Possible 10x value deviation | Specify a **C0G/NP0 50 V** part at whatever value wins - Murata GRM1885C1H221JA01D class for 220 pF C0G 0603, or GRM1555C1H220JA01D for 22 pF C0G 0402. **`[UNVERIFIED]` the 10x claim:** the R1200 recommended-components table reportedly gives C3 = 22 pF / 25 V with R3 = 2 k, and R28 *is* 2 k - but that table could not be extracted from any accessible copy, so it rests on local `_r1200_ds.txt` alone. **Raise it with the schematic owner as "please confirm against the datasheet table", NOT as a confirmed 10x error.** Minor: RS UK shows GRM1885C1H221JA01D unavailable/being discontinued while DigiKey, Arrow, TME, element14 and Future all list it - single-distributor signal; have a Samsung/Kemet 220 pF C0G 0603 as backup. |
| C24 | C0603C105K4RACTU | **Ambiguous** `[CONFIRMED ambiguity]` - **TTI Europe: "Limited Supply", 32-week additional-stock lead, 2,956,000 on order not due until 10-Nov-26. TTI US: part number "in transition", contact factory.** Most likely the KEMET-to-Yageo brand migration rather than EOL, but unresolved | DigiKey page live; Newark stocked | Electrically **correct** - 16 V at 31% of rating on /SYS LOAD, ~0.7-0.8 uF retained | No change strictly required. But since C25 must move to 25 V anyway, consider putting **both C24 and C25 on C0603C105K3RACTU**: one line instead of two, shorter quoted lead (14 vs 32 wk), free extra margin on C24, and it removes the "in transition" ambiguity. **Get a written part-status confirmation from your Kemet/Yageo distributor before a production buy either way.** https://www.tti.com/content/ttiinc/en/apps/part-detail.html?partsNumber=C0603C105K4RACTU&mfgShortname=KEM |
| J2 | 1054500101 | **Active** `[SUSPECTED]` - status read from a **Molex-generated part-detail document dated 2021-09-07**; molex.com refused automated access. No EOL or PCN found. TTI labels it "Reference Only" and cross-references JAE DX07S024JJ3R1300, but simultaneously shows 192,400 pcs - read as a stocking label, not EOL | TTI 192,400; Arrow 103,618 @ $2.67; **LCSC C134092 152,423 @ $0.844**; Mouser 42,280 @ $2.74; DigiKey 39,390 (1300-reel $1.65). **Mouser quotes a 14-week factory lead for restock** - the deep distributor stock is the buffer, not the factory | Correct part, correctly loaded (CC1/CC2 with 5.1 k Rd for a UFP sink), but **significantly overspecified**: all ten SuperSpeed/SBU pins (A2/A3/A8/A10/A11, B2/B3/B8/B10/B11) are unconnected because the ESP32-S2 is USB 2.0 full-speed only | Fix the MPN cell to text. **Optional DFM cleanup:** you are paying $2.40-2.74 for a USB 3.2 Gen 2 24-position receptacle and routing/tenting ten dead 0.5 mm-pitch inner-row pads on ENIG for no function. A 16-position USB 2.0-only Type-C is ~$0.30-0.90 and removes the inner-row fanout entirely. Since the PCB needs a resync anyway, this is a natural moment. Get a formal lifecycle statement given the 2021-vintage status doc. |
| R22,R23 | ERJ-3GEYJ103V | Active `[CONFIRMED]`; live quantity `[UNVERIFIED]` | DigiKey 135662, Mouser, Newark, TME | **Part correct, value wrong for the duty.** R22/R23 are the *only* I2C pull-ups to the SSD1326, and the bus runs through a 26-pin FFC. At 10 k with **~60 pF assumed** bus capacitance, tR ~510 ns - inside the 1000 ns Standard-mode limit but well outside the **300 ns Fast-mode (400 kHz)** limit the SSD1326 supports | Drop to **2.2 k** (RC0603FR-072K2L, tR ~112 ns, 1.5 mA sink) or **4.7 k** (RC0603FR-074K7L, tR ~240 ns). **`[UNVERIFIED ASSUMPTION]` the 60 pF drives the whole result** - at 30 pF the existing 10 k gives tR ~254 ns and the finding largely evaporates. The FFC makes 60 pF plausible but nobody measured it. 4.7 k is the safe default; 2.2 k is safe at either estimate. **This is a schematic value change, not a part-number change** - do it now while the board is being re-laid out. |
| R31 | (100 k line) | Active | see R2 group | **Wired as a pull-UP.** R31.1 on +3.3 V, R31.2 on /CHG_ILIM = MCP73871 **PROG2**. Per DS20002090F §3.9, PROG2 **high = five unit loads = 500 mA**. So the board defaults to drawing 500 mA from USB **before enumeration**, which USB permits only after configuration (100 mA unconfigured; 150 mA on USB 3.x). A hub port or a compliant host can and does trip on this. `SCHEMATIC_REVIEW_2026-09-03.md` item C-1 explicitly called for a pull-**down** | **Move R31's top end from +3.3 V to GND.** Same part, one net change. U10.28 already drives the net so firmware can raise it to 500 mA after configuration. **Zero BOM delta - this will not appear in any BOM diff. Route it to the schematic owner, not purchasing.** `[SUSPECTED - netlist and review file not re-readable here]` |
| /VBAT array | (missing parts) | n/a | n/a | **Missing parts, not a wrong MPN.** Quectel Fig 10 calls for a **100 nF + 33 pF + 10 pF** MLCC trio close to the VBAT pins on **both** the VBAT_BB and VBAT_RF branches of the star. /VBAT currently carries only C1 (0.1 u), C2 (1 u), C16 (4.7 u), C3 (470 u) - **the 33 pF and 10 pF are absent entirely.** These shunt RF energy off the supply pins of a transmitting radio; omitting them is a classic cause of self-desense and conducted-emissions failures that only appear at certification. Quectel also asks for **two TVS on VBAT** ("low leakage, suitable reverse stand-off, as close to the VBAT pins as possible") - the BOM has none; all 8 ESD9B parts are on SIM/USB | Add 33 pF and 10 pF C0G 0402 to each VBAT pin group (4 new parts on the star). **Murata GRM1555C1H330JA01D and GRM1555C1H100JA01D are both fine** - `[CORRECTED]` an earlier claim of channel stress does not hold: DigiKey 3661907 shows "buy now, ships today" and TrustedParts rates both risks Low. Samsung CL05C330JB5NNNC / CL05C100JB5NNNC equally fine. **Additionally:** Quectel's current BG95 Reference Design V1.3 adds a **ferrite bead on VBAT_BB** (>=0603, >=600 mA, >=800 ohm at 700-960 MHz, low DCR - TDK MPZ1005A331ET or Murata BLM18DN381SN1) plus an expanded array (220 nF / 47 nF / 150 pF). **Check whether that bead exists before closing this.** `[SUSPECTED - cited to local _bg95.pdf]` **Schematic change, not a BOM change.** |
| C30,C37,C38,C40 | CL05A104KA5NNNC | **Active** `[CONFIRMED]` - Samsung shows CL05A104KA5NNN# in Mass Production; TrustedParts Lifecycle Risk Low | LCSC >9.6 M | Row was auto-filled and **contradicts its own schematic text**: SchDescription says "X7R" but the Samsung `A` dielectric code is **X5R** (-55..+85C). Also not purchase-ready - DigiKey PN, LegacyPkg, LegacyDesc, Datasheet and Price all empty, Status `~`. Electrically benign at 0.1 uF / 25 V on all four nets | If X7R was intentional, swap to **CL05B104KA5NNNC** (same 0.1 uF 25 V 0402, X7R, -55..+125C) - a true drop-in, +50 um height. Otherwise correct the schematic text. **Consolidate all ten 0.1 uF 0402 parts onto one X7R line.** Fill in the empty fields before release. |
| J4 | BM02B-SRSS-TBT | **Active** `[CONFIRMED]` | DigiKey 11,076 (1500-reel $0.342); Verical 21,000; Win Source 15,408; Bristol 3,368; Quest 2,400 | Correct part. **Dropping EGPRS is what makes it viable** - at the old 2 A GSM burst its 1 A/contact rating was a clear violation; at ~600 mA it is workable but **the margin is thinner than it looks**, because these same two contacts also carry the MCP73871 charge current *and* the full system load - at 3.3-3.5 V cell voltage the burst current can approach 0.9-1 A. Also note **-25C lower limit**, warmer than the BG95 and MHF1 at -40C, so **JST SH sets the cold-end limit for the whole product** | Keep. **Measure worst-case burst current with a current probe at a 3.3 V cell before sign-off - 1 A is the rating, not a target.** Mating half is not on the BOM (see §2). Minor: the Value cell reads the generic "Conn_01x02_Pin" rather than the MPN. |
| Hardware / enclosure | none | n/a | n/a | No fasteners, standoffs, inserts or enclosure line; **zero MountingHole footprints on the PCB** | See §2. The mounting-hole half is the only irreversible item - it belongs with PCB1. |

### LOW

| Refs | MPN | Lifecycle | Stock | Risk | Action |
|---|---|---|---|---|---|
| U8 | MCP73871-2CCI/ML | **Active** `[SUSPECTED]` - inferred from broad authorized stock and a live microchipDirect listing; Microchip's own status field could not be retrieved | DigiKey 7,841 (tube) $2.41@1; Mouser 3,332 + 3,994; Newark 2,653; Future 273 @ **21 wk**; RS 0 @ **52 wk** (placeholder-grade data against zero stock) | **`[CORRECTED]` The 21-52 week alarm is an artifact of the TUBE packaging.** The T&R part **MCP73871T-2CCI/ML** shows DigiKey 7,735 @ $1.82, Verical 6,000, Newark 3,596 - and **Future quotes 4 WEEKS on the reel vs 21 on the tube.** ~14,000 pcs authorized. Ordering the T&R part you want for pick-and-place anyway collapses the lead by ~17 weeks | Order **MCP73871T-2CCI/ML** (T&R). **`-2CC` is the only option code that works**: the three characters decode as VREG / safety-timer / LBO, and -2CC = 4.20 V / 6 h / LBO 3.1 V. LBO is only ever "disabled" or "3.1 V" and enabled only on codes ending `C`; alternates -1CC/-3CC/-4CC differ only in VREG (4.10/4.35/4.40 V), all wrong for standard Li-ion. **No substitute exists.** Pinout verified 20/20 against DS20002090E. **Design item: pin 9 (TE, active-LOW) is tied to +3.3 V, which DISABLES the 6-hour safety timer the middle `C` pays for.** Defensible - Microchip recommends disabling it in power-path/load-sharing designs where system load stretches charge time into a false fault - but it means only VREG and LBO actually matter, and **there is no backstop against charging a dead or shorted cell indefinitely.** Confirm this is deliberate and document the alternative. |
| CR1-CR8 | ESD9B5.0ST5G | **Active** `[CONFIRMED]` on onsemi's own product page | DigiKey 626,894; Arrow/Verical 4,960,000; Future 9,688,000 @ $0.0258; Newark 65,936; Mouser 17,971; LCSC 327,420. **Millions - the 3 -> 8 quantity rise is a non-event** | **Bidirectional CONFIRMED** (datasheet symbol block is labelled "Bi-Directional") so the design's orientation-independence is sound. **SOD-923 case 514AB CONFIRMED**, 1.00 x 0.60 mm, matches `D_SOD-923`. Residual: **VRWM is exactly 5.0 V and CR6 sits on +5V VBUS**, where USB permits 5.25 V - CR6 normally runs above its rated stand-off. Practical impact is small: at 5.25 V it is still well below the 5.8 V min VBR so it does not conduct; the cost is leakage above the 100 nA spec, **drawn from VBUS only while plugged in, so it costs no battery runtime** | **Accept and document the CR6 deviation** - that is the correct default, not a compromise. There is **no in-family higher-stand-off option** (ESD9B offers only 3.3 V and 5.0 V) and no specific >=5.5 V bidirectional SOD-923 part was verified, so none is named. **PURCHASING GUARD, keep this verbatim in the BOM notes: ESD9X... and ESD9L... share the same SOD-923 land but are UNI-directional - do not let a broker substitute them.** SZESD9B5.0ST5G is the automotive change-control sibling but **onsemi's own family page lists it "Unavailable"** - it would need sourcing confirmation. Note 15 pF at 0 V bias is at the high end for a SIM interface. |
| U1 | R1200N002A-TR-FE | **Active - CONFIRMED not NRND.** The NRND note applies to a **different package**: Nisshinbo's discon list has exactly one R1200 row whose scope column reads verbatim "R1200K only" (the DFN(PL)1820-6), and the datasheet header says "R1200Z (WLCSP-6-P1) discontinued as of September 2017. R1200K (DFN(PL)1820-6) is NRND as of April 2023." R1200L and R1200N are the current packages | DigiKey 4,155 @ $1.28@1 -> $0.59@15k; Mouser 2,046; Newark 0 with a 3,000-pc MOQ @ $0.49. **~6,200 pcs across two authorized sources** | Correct part, correctly optioned. Pinout confirmed 6/6 (CE/VOUT/VDD/Lx/GND/VFB). **Internal rectifier CONFIRMED** ("Built-in a rectifier NPN transistor") - so **having no Schottky between Lx and VOUT is correct, not an omission**. `002` = 19 V OVP (001=17, 003=21); `A` = auto-discharge at off, which is what you want on an OLED bias to avoid ghosting. Divider gives exactly 12.00 V. Niche Japan-domestic vendor with a narrower distribution base than the TI/onsemi lines | Keep. **Buy a little deeper than usual** - two authorized distributors only. R1200N001A / -003A differ only in OVP and are **not** interchangeable without rechecking the rail. Two companion actions are the real work here: **C25 to 25 V** and **L2's saturation margin**. |
| U6 | TPS62172DSGR | **ACTIVE** per TI's own part-details page `[CONFIRMED]` | DigiKey 16,596 @ $0.774-1.48; Mouser 16,237; Allelco 52,140; TME 0. TI.com direct out of stock - not a concern | Correct part, correctly wired 9/9. **62170 = adj, 62171 = 1.8 V, 62172 = 3.3 V, 62173 = 5.0 V** - stated explicitly because the family is easy to get backwards and several aggregators do. FB-to-AGND is **correct** for a fixed version per TI. The **2.2 -> 3.3 uH L1 change is datasheet-endorsed**: "for applications running with low input voltages, 3.3 uH is recommended, to allow the full output current" | No part change. **Fix the BOM Datasheet URL - it points at `tps62171`, the 1.8 V part**, and someone will re-derive the wrong rail voltage from it. **System advisory:** in 100% duty mode the 3.3 V rail falls out of regulation around VBAT ~3.4-3.5 V at the ESP32-S2 Wi-Fi TX peak (~310 mA) and then tracks VBAT down, while the MCP73871 LBO does not assert until 3.1 V - **so do not treat LBO as an early warning.** It still works (ESP32-S2 min VDD is 3.0 V) but measure the actual dropout vs LBO at bring-up. 500 mA is the hard ceiling for ESP32-S2 TX + OLED logic + pull-ups combined. |
| U5 | TPD2EUSB30ADRTR | **ACTIVE** per TI `[CONFIRMED]` | Mouser 96,287; DigiKey 80,470; Newark 24,675; Allelco 153,360. An older cache showing "Mouser 0, restock June 2026" is **stale** | Pinout D1+/D1-/GND confirmed. The **`A` variant is the low-clamp one** - 0-3.6 V working, 4.0 V abs max, **VBR 4.5 V** vs 7 V on the plain part - correct for a 3.3 V PHY. 0.7 pF, IEC 61000-4-2 level 4 | Keep. **`Do not substitute TPD2EUSB30DRTR`** - 7 V breakdown is materially worse here. **BOM text is wrong:** LegacyPkg says "3-SMD, SOT-23-3" and LegacyDesc says "8V Clamp" - it is **SOT-9X3 (DRT), ~1.05 x 0.85 x 0.45 mm**, and the clamp figure is 4.5 V. The KiCad footprint used is consistent with the real DRT, so the PCB is fine; the BOM text would mislead. **`[UNVERIFIED]`: TI's DRT0003A land-pattern drawing was not in the retrieved PDF - verify the land before fab; the pads are only 0.20 mm wide, right at the edge of comfortable for ENIG.** Inherent caveat: a VBUS-to-D+ short forwards the 4.5 V clamp into a 5 V source - normal for this part, just **never add a 5 V-referenced pull-up on D+/D-.** |
| U3 | SN74AVC2T245RSWR | **ACTIVE** per TI `[CONFIRMED]`; datasheet at rev E, **Sept 2024** - actively maintained | DigiKey 362,480; Allelco 66,510; Unikey 33,310; Newark 3,480; LCSC 5,900. Mouser 0 in this snapshot but 59,808 in an earlier one - transient | **Clean, including the direction strapping - the line I most expected a bug on.** Pin 10 DIR1 = +1.8 V (HIGH) gives A1->B1 = BG95 TX -> ESP RX; pin 1 DIR2 = GND (LOW) gives B2->A2 = ESP TX -> BG95 RX. Both correct. OE tied low, VCCA = 1.8 V, VCCB = 3.3 V, both DIR/OE correctly VCCA-referenced. Footprint matches RSW UQFN-10 | **No action.** |
| Q1 | SMMBT2222ALT3G | **Active** `[CONFIRMED]` on onsemi's orderable table | Avnet 120,000 @ $0.0216/10k; Verical 51,663; Arrow 51,663; Mouser 10,572; Flip 1,505,000. The 52-wk figures are **beyond-stock factory leads**, not availability | Correct: SOT-23, NPN, 40 V, 600 mA, B/E/C matching the netlist. Open-collector pull-down on BG95 PWRKEY, ~260 uA base drive through R1, with R6 holding it off when the ESP32 is unpowered | **Commercial only:** the `S` prefix is onsemi's automotive / unique-site-and-change-control grade - 10,000-pc reels and ~1.5x price ($0.02 vs $0.0136) for no benefit on a PWRKEY pull-down. **MMBT2222ALT3G** is the same die, same SOT-23, same pinout, also Active - a zero-change swap that lowers both the minimum buy and the price. **Guard: do not accept MMBT2222ALT1 or MMBT2222ALT3 (no `G`)** - onsemi lists those as **OBSOLETE**. |
| J3, J8 | CONMHF1-SMD-T | **Active** `[CONFIRMED]` | DigiKey 48,000 @ $0.23; TE direct 48,122; Mouser 16,904; Avnet 9,000; Arrow 4,500; TME 1,959. 4,500/reel, distributors cut tape | **Confirmed correct for both duties**: U.FL-type jack, 50 ohm, **0 Hz - 6 GHz**, insertion loss 0.10 dB max across 400-960 / 1164-1609 / 1427-5000 MHz, VSWR 1.1. Covers LTE-M on J3 and GNSS on J8 with margin. **Mating-cycle flag CONFIRMED: "EIA-364 ... 30 cycles min"** | Keep. **Plan around 30 cycles during VNA tuning**: fit a U.FL-to-SMA pigtail once and leave it mated for the whole session, budget sacrificial boards, and **do not ship a unit whose connector was used as a test port.** The project library already contains `TE_CONSMA001-SMD-G.kicad_mod` - putting an SMA on a tuning coupon or a DNP alternate land removes the problem entirely. Ordering note: `-T` is nickel shell, `-G-T` gold, but signal and ground contacts are gold on **both**, so plain `-T` is fine. The BOM's Datasheet URL points at the `-G-T` doc - cosmetic, the PDF covers both. **And see J8: the part and quantity are right, the board has no J8 footprint.** |
| J7 | 2452808-1 | **Active** `[CONFIRMED]` - TE customer drawing rev **C1, 11 JUN 2025**, a recent revision | Mouser 20,052 @ $0.95; TME 18,000; DigiKey 12,512 @ $0.95; Powell 11,880; Verical 18,000; Newark 961 | **All three open questions answered from the drawing.** (1) It is **NANO-SIM (4FF)**, push-**pull**, title block reads "NANO SIM CARD CONNECTOR PUSH-PULL". (2) It **has** a card-detect switch. (3) The "SWITCH OPERATION DIAGRAM" table reads: **without card = OPEN, card inserted = CLOSED**, with the far side internally commoned to **C5 (GND)**. **The design's assumption is correct: card present pulls SIM_DET LOW** | Keep. **Firmware: SIM_DET is ACTIVE-LOW for card-present, and de-bounce in software** - the R36/C40 network gives only ~100 us and push-pull insertion chatters well beyond that. **BOM price $1.36 is stale against ~$0.95 - update the cost model.** `[UNVERIFIED]`: the mating-cycle rating is not on the customer drawing; it lives in app spec 108-140328 which te.com would not serve. ~5,000 cycles is typical for this class but **treat that as unverified.** |
| S1, S2 | TS04-66-70-BK-100-SMT | **Active** `[CONFIRMED]` - datasheet dated **11/03/2025** | Bulk (the specified MPN): Verical 6,000, Mouser 2,501 @ $0.23, DigiKey 2,195 @ $0.55. **Reel (`-TR`): Mouser 4,487 @ $0.23, DigiKey 0, TME 0, Newark 0** | Correct part, netlist uses both contact pairs paralleled with 0.1 uF hardware debounce. **Manufacturer has rebranded CUI Devices -> Same Sky** - update the field or future automated cross-checks will flag it unknown | Two practical notes. **(1) Mechanical:** `70` = **7.0 mm actuator height** above the PCB, tall for a keychain handheld and demanding a 7 mm-plus standoff or plunger. The **4.3 / 5.0 / 5.5 mm variants use the identical land at the same price** - if 7.0 mm was inherited rather than chosen, this is a free correction. **(2) Packaging:** the specified MPN is the **bulk-bag** version. A CM or JLCPCB PCBA will require **`-TR`**, and DigiKey has **zero** of the `-TR` while Mouser has 4,487 - **pick the suffix to match the assembly route and the distributor to match the suffix.** Also DigiKey is $0.55/1 vs the BOM's $0.19 (roughly Mouser's price). |
| C9 | GRM155R61A106ME11D | `[UNVERIFIED]` - **specifically NOT claiming EOL**. Murata's product page resolves; no distributor flags obsolescence | `[UNVERIFIED]` - Octopart, DigiKey, Mouser all refused direct fetch | **No mismatch.** Budgeting caveat only: a 10 uF 10 V X5R 0402 at 3.3 V holds ~25-35% (*estimate*), ~2.5-3.5 uF, and with ±20% tolerance + temperature + Class II ageing can go below 2 uF worst case. **Do not do output-filter arithmetic on marked values.** | Keep for build 1. Ask Murata for a formal status - if C8 and C15 both move off this MPN as recommended, **C9 is the only remaining user, making the question cheap to settle.** |
| C14, C16 | CL05A475MP5NRNC | **Mass Production** `[CONFIRMED]` on Samsung's own database | `[UNVERIFIED]` - Samsung publishes no stock; distributors refused fetch. Note the `R` code is a horizontal/low-acoustic-noise variant, which sometimes means thinner coverage | **Clean.** And it resolves an error: Samsung's page gives 4.7 uF / **10.0 Vdc** / ±20% / X5R / 0402 - **the BOM's 10 V figure is CORRECT; one secondary listing claiming 6.3 V is wrong. Flagged so nobody "corrects" the BOM in the wrong direction.** C16 on /VBAT at 42% of rating, C14 on /SYS LOAD at 50% - both acceptable, each retaining ~1.5-2 uF | No change. **X5R is +85C max** - neither may sit where the BG95 or boost drives local board temp above 85C. |
| C1,C4,C5,C7,C17,C18 | CL05A104KA5NNNC | **Mass Production** `[CONFIRMED]`, no PCN or EOL. TrustedParts: Lifecycle Risk **Low** | LCSC **>9.6 M**; Mouser and TME listing | **Clean.** All six duties well inside rating, DC bias negligible | No electrical change. **Merge with the C30/C37/C38/C40 row into one line of qty 10** - the identical MPN currently sits on two lines because the schematic spells the value `0.1uF` on six symbols and `100nF` on four. Same X5R +85C caveat. |
| R1,R14,R18,R20,R37 | RC0402JR-0710KL | **Active** `[CONFIRMED]` | **LCSC C60489: 4,288,100 @ $0.0042** `[read live]`; DigiKey 729365/726418, Mouser, TTI, Arrow | **Correct on every axis**, all five duties tolerance-insensitive. R14 = MCP73871 PROG1 giving IREG = 1000/R = **100 mA**, a conservative 0.2C on a 500 mAh cell but valid | No change. **Hygiene flag:** R37's Status reads "PARTIAL - no legacy row", i.e. it got this MPN by **family-fill**, not carry-forward. It happens to be right - but family-fill is exactly the mechanism that produced the R2-group and R11/R13 errors, so spot-check it rather than trusting it. |
| R27 | RT0603FRE07110KL | **Active** `[CONFIRMED]`; exact live quantity `[UNVERIFIED]` (DigiKey 403) | DigiKey 1075045 exists; sibling RT0603FRE parts all present as normal stocked lines | Correct: 110 k ±1% thin film, upper leg of the R1200 divider. R26+R27 = 120 k, inside the datasheet's **300 k ceiling** | **Keep it, and do NOT downgrade it to thick film to "match" R26 - fix R26 upward instead.** Best outcome is RT0603FRE07110KL over RT0603FRE0710KL so both legs are the same thin-film family and their TCs track. Fallback RC0603FR-07110KL is valid **only if R26 is also 1%**. |
| R24 | RC0402JR-0710KL | Active | LCSC 4,288,100 | **Correct, and the DNP is correct.** R24 is the 10 k-to-GND that emulates the battery NTC at MCP73871 THERM when TH1 is unpopulated. 5% is fine against the wide THERM thresholds. **One of the cleanest lines in the set** | No change. **Keep the MPN recorded despite the DNP** - a stuffing option with no part number cannot be exercised at 2 a.m. during bring-up, which is exactly when this one is needed (first power-up with no battery). **Add a fab/assembly note that R24 and TH1 are mutually exclusive.** |
| R9 | (100 k line) | Active | see R2 group | **The part will be right once the R2 conflict is fixed, but the placement is dead weight.** Net-(U6-PG) = R9.2 and U6.8 **only** - R9 pulls the TPS62172 Power Good up to +3.3 V and the signal goes **nowhere**. TI: "If not used, the PG pin should be connected to GND but may be left floating." Mild circularity too: PG is pulled up to U6's own output | **Either delete R9** (or tie PG to GND per TI), **or better, route PG to a spare ESP32-S2 GPIO** - the earlier review lists plenty free (IO4-7, IO15-17, IO34-42). Firmware that can see PG can distinguish "buck failed" from "brownout" from "battery dead", which on a device with no debug UART headroom is worth more than the resistor. **What you should not do is ship it as-is** - a pull-up to nowhere costs money, occupies a feeder, and misleads the next reader into thinking PG is monitored. |
| R3,R12,R36 / R7,R8 | AF0402JR-071KL / AF0402FR-075K1L | **Active** `[SUSPECTED]` | **`[UNVERIFIED]`** - no readable distributor page with live stock for **either** exact PN; only AF-series siblings surfaced as stocked | **R7/R8 CONFIRMED 1%**: `F` = ±1% per the Yageo AF datasheet, `5K1` = 5.1 k - comfortably tighter than USB-C Rd's ±10%, and both legs are present and correctly placed. **Downgraded to a purchasing action, not a design finding:** re-specifying seven placements on the strength of pages that merely 403 an automated fetcher is over-reach - every site involved blocks scrapers, including the RC equivalents' pages | **Confirm live stock on AF0402JR-071KL and AF0402FR-075K1L before release.** A blanket AF->RC swap is a *preference*, not a fix: AF is AEC-Q200 with ±50 ppm/C grades, so dropping it is a small spec downgrade, and supplier consolidation is a logistics argument. **R11/R13 appear on this line but their real defect - the stale 1 k MPN on a 680 R line - is a separate must-fix.** |
| R21 | ERJ-3GEYJ684V | **Active** `[CONFIRMED]` family; exact value's live quantity `[UNVERIFIED]` | ERJ-3GE is one of the highest-volume 0603 thick-film families; DigiKey, Mouser, Newark, TME, Arrow | **Correct, verified against the panel vendor's own reference design.** R21 is the SSD1326 IREF resistor (J5.24 to GND). The ER-OLED018-1B datasheet specifies verbatim **"R1: 0603 1/10W ±5% 680 kOhm"** - value, package, power rating **and** tolerance grade all match. **5% is correct here, not a compromise** | No change. **Add a schematic note that 680 k is panel-mandated, not arbitrary** - if anyone later "optimises" it to 0402 or changes the value, brightness and panel lifetime move with it and the init code's contrast/VCOM settings need retuning. |
| R28 | RC0603JR-072KL | **Active** `[CONFIRMED]` | Commodity; exact quantity `[UNVERIFIED]` | **Correct, and it matches the IC datasheet's worked example.** R28 (2 k) + C26 (220 pF) is the R1200's VFB noise filter; Nisshinbo specifies R3 = 1-5 k and its Table 3 example gives **R3 = 2 k with C3 = 220 pF** - the board implements exactly that. *(Note this partly contradicts the C26 "10x deviation" claim - see §8.)* | No change. Moves cleanly to RC0402JR-072KL if you consolidate packages. |
| R4,R5,R17,R19 | RC0402JR-130RL | **Active** `[CONFIRMED]` | DigiKey 12756386, Mouser, Arrow, Future 1301876, TTI. 10,000/reel. Quantity `[UNVERIFIED]` | **Correct - and the part number looks like a typo but is not.** In this Yageo variant `-13` is the tape/reel **packaging-width** code (rather than the familiar `-07`) and `0R` is the value, so RC0402JR-130RL and RC0402JR-070RL are the same 0 ohm 0402 jumper on different reels. Rated 1 A; all four duties are microamps | No change. **RC0402JR-070RL is the identical part on the more commonly stocked reel** - check which one your distributor actually has. R17/R19 in the USB data pair are a small discontinuity, immaterial at Full Speed only. |
| C32,C33,C35,C36 / C41,C42,C43 | (none, DNP) | n/a | n/a | Documentation completeness only, **zero build-1 impact** | See §2. |

---

## 4. Long-lead / order-first list

Ranked by lead time and single-sourcing. **Order the first two this week.**

1. **Battery** - the longest pole and the only item **confirmed unbuyable**. Re-selection + UN38.3
   documentation + air-freight restrictions, on top of procurement. Start today. Target 600-1000 mAh
   with a **published PCM over-current trip** and a **JST SHR-02V-S-B** termination (specify it on the
   PO - most commodity packs do not carry 1.0 mm SH), or change J4 to JST PH and buy mainstream.
2. **ER-OLED018-1W display + ER-CON26HT-1 ZIF** - single-source, China direct, no authorized
   distribution, **no published lead time**, multi-week freight. Get a **written lead time and stock
   reservation** from sales@buydisplay.com before the enclosure is committed. Buy 2-3 display spares
   and 5-10 connector spares. Confirm **-1W (white)**, not -1B, to match the legacy order. Ask whether
   the connector ships bundled. *Correction to an earlier draft: the display is single-source with
   **unknown** stock, not confirmed at zero - only the battery is confirmed unbuyable.*
3. **U10 ESP32-S2-SOLO-2U-N4** - **~1,670 pcs total across DigiKey + Mouser.** Lifecycle is confirmed
   Active, so this is not a build-1 blocker, but the family is visibly being pruned. **Buy build-1 and
   build-2 quantity on one PO.** N4R2 is a qualification path, not a hedge (14 pcs at DigiKey).
4. **E1 Molex 1461530150** - 9-week factory lead (18 wk if you keep the legacy 1461539150).
5. **E2 ANT-LTE-RPC-UFL** - 8-week lead, **and the one antenna whose lifecycle story is not clean**
   (Active at TE/DigiKey, "Reference Only" at TTI, "no longer manufactured" at OnlineComponents).
   Resolve before committing 8 weeks, or switch to **YF0006PA** (Active, 5,249, EUR 1.65, **4 weeks**).
6. **U2 BG95M3LA-64-SGNS** - ~5,300 pcs authorized, fine for build 1; **20-week factory lead** is the
   production number. Most expensive line at $27.46. Cellular modules are historically the most
   allocation-prone item on any IoT BOM. Decide M2-vs-M3 before the production PO, not after.
7. **U8 MCP73871** - order the **T&R** part (`MCP73871T-2CCI/ML`), not the tube: 4-week vs 21-week lead
   at Future for the same die.
8. **E3 YFGA003AA** - 4-week lead, 3,237 in stock, $2.36 CAD. The easiest of the three antennas.
9. **PCB + stencil** - **cannot be ordered at all** until the layout is resynced. Buy them in one cart.

**Antenna gate:** do a CAD mock-up with all three antenna outlines and the pack **before** placing the
antenna order. E2 at 98.4 x 14.9 mm is **82% of the 120 mm board length** on a 37.50 x 120.00 mm board
that also carries E1 (34.9 x 9.0), E3 (39.45 x 13.25), a ~31 x 20 x 9.5 mm pack and the 1.8in OLED. All
three are ground-plane-independent dipoles - good (no counterpoise to design) but each needs a patch of
plastic with **no copper, no battery foil, no display metal** behind it, and the PCB fills the case.
**Budget ground-plane clearance, not just outline area** - FPC antennas of this class typically want
~10 mm to the nearest metal, which on a 37.5 mm-wide board is the binding constraint. Also honour the
review's **>=25 mm J3-to-J8 separation**, keep the 100 mm 1.13 mm coax as-is (BG95 Table 34 caps cable
insertion loss at <1 dB on the low bands - do not extend it), and plan to tune C31-C36 on a VNA **with
the case closed and the battery fitted**.

---

## 5. Correctness corrections

### MLCC DC-bias derating - do not do filter arithmetic on marked values

All percentages below are **engineering estimates**, not read from Murata SimSurfing (which could not be
driven), and are labelled as such throughout.

| Ref | Marked | Bias | Retained (est.) | Consequence |
|---|---|---|---|---|
| C10,C13 | 22 uF 6.3 V X5R **0402** | 3.3 V | ~20-30% = **4-7 uF** | This is exactly why the schematic moved to 0805. Two 16 V 0805 parts give comfortably more than a real 22 uF, satisfying TI's "recommended value for the output capacitor is 22 uF". |
| C15 | 10 uF 10 V X5R **0402** | 5 V VBUS | ~20-30% = **2-3 uF** | Against a ~10 uF USB device VBUS budget plus the MCP73871's input decoupling need. Plus 10 V is only 2x on a rail that rings on hot-plug. |
| C8 | 10 uF 10 V X5R 0402 | ~5 V (SYS LOAD rides toward VBUS with USB attached) | ~20-30% = **2-3 uF** | C8+C14+C24 total ~5 uF against TI's recommended 10 uF input cap, and the R1200 separately requires ">=1 uF as close as possible" on the same node. |
| C9 | 10 uF 10 V X5R 0402 | 3.3 V | ~25-35% = **2.5-3.5 uF**, and below 2 uF worst-case with tolerance + temp + ageing | Budgeting caveat only. No mismatch. |
| C2 | 1 uF 6.3 V X5R 0402 | 4.2 V VBAT (**67% of rating**) | ~30-40% | Split C2 out to a 16 V part. C11/C29/C39 are fine. |
| C29 | 1 uF 6.3 V X5R 0402 | 3.3 V | derated | ESP32-S2 EN rise RC is **~4-5 ms**, not the nominal 10 ms. Still adequate - but do not size it on the marked value. |
| C25 | 1 uF 16 V X7R 0603 | 12 V (**75% of rating**) | ~20-40% = **0.2-0.4 uF** | Against the R1200's stated "1 uF - 4.7 uF or more". Below the vendor's floor **and** below its minimum rating. |
| C22,C23 | 4.7 uF 25 V tantalum | 12 V / ~10 V | n/a (tantalum) | Different problem: 6 ohm ESR is invisible at the R1200's 1.2 MHz. Replacing with 1206 MLCC gives ~2-3 uF effective at 12 V - **an order of magnitude more useful filtering** than 4.7 uF behind 6 ohms. |
| C26 | 220 pF 25 V **X7R** | ~11 V (44%) | ~60-70% and drifting with temperature | Wrong dielectric for a **compensation** element - a compensation zero should not move with bias. Specify **C0G/NP0**. |
| C14,C16 | 4.7 uF 10 V X5R 0402 | 5 V / 4.2 V | ~1.5-2 uF each | Legitimate local bypass; **must not be counted as bulk**, which matters because C14 is part of the SYS LOAD total that already falls short of TI's 10 uF. |

### C0G is mandatory where the schematic says so - honour it

- **C31, C34** (RF pi **series**, cellular and GNSS) and **C32/C33/C35/C36** (RF pi shunts): these sit
  **directly in a 50 ohm RF path**. An X5R/X7R here wrecks Q and drifts with temperature. Specify from
  **Murata's GJM series** (the high-Q RF line) - **do not substitute GRM or GCM general-purpose C0G at
  the same value**: electrically identical on paper, worse Q and ESR in a matching network.
- **C41/C42/C43** (SIM EMI shunts): C0G, and the value is **33 pF per Quectel**, not 22 pF. Do not
  exceed it - ETSI/Quectel budget the USIM ESD parasitic at <=15 pF and the CLK bus capacitance tightly.

### Voltage-rating / package mismatches (recap)

- **C25 is below the R1200's own stated minimum.** The datasheet requires >=1.5x Vout = 18 V; **and the
  selectable OVP threshold of 17/19/21 V means the node can legitimately reach 17 V**, which kills a
  16 V part on its own. Go to **25 V minimum**, ideally 0805.
- **C15 on VBUS needs 16-25 V**, not 10 V. **C10/C13 need 0805 16 V**, not 0402 6.3 V.
- **CR6's VRWM is exactly 5.0 V on a VBUS that USB permits at 5.25 V.** Accept and document.

### Tolerance and value errors that change behaviour

- **R33/R34 (VPCC divider):** 1% on both legs holds the foldback knee at ~4.10-4.48 V including the
  MCP73871's own ±3% VPCC threshold tolerance. 5% spreads it to ~4.00-4.61 V - dead feature at one end,
  spurious throttling on a normal hub port at the other. **Do not accept 5%.**
- **R26 (12 V setpoint):** a 5% thick-film lower leg against a 1% thin-film upper leg spreads the OLED
  rail to **11.20-12.88 V**. Free fix: 1%, ideally TC-matched.
- **R22/R23 (I2C pull-ups):** 10 k locks the SSD1326 out of 400 kHz **if** bus capacitance is ~60 pF -
  an assumption, not a measurement. 2.2 k or 4.7 k is safe at either estimate.
- **R11/R13:** 680 R gives ~2.1 mA and ~45% more brightness than the stale 1 k; 3.1 mW in a 62.5 mW part.
  Well within the MCP73871 status outputs' sink capability.
- **R31 polarity:** pull-up where a pull-**down** was specified - USB compliance issue, zero BOM delta.

### Things that are correct and should not be "fixed"

- **No Schottky between R1200 Lx and VOUT** - the rectifier is integrated ("Built-in a rectifier NPN
  transistor"). Correct as drawn.
- **U6 FB tied to AGND** - TI explicitly recommends this on fixed-output versions.
- **U3 direction strapping** - both bits verified correct against the netlist.
- **J7 SIM_DET active-low** - confirmed against TE's own switch-operation diagram.
- **R21 = 680 k 0603 5%** - matches the panel vendor's reference design down to the tolerance grade.
- **Passive GNSS antenna, no bias tee** - Quectel recommends passive when B13 is supported.
- **`ND03N00103K--`** - the trailing dashes are Kyocera's **bulk packaging code**, not corruption.
- **`RC0402JR-130RL`** - `-13` is a reel code, not a value typo.

---

## 6. Do NOT re-order

Deleted from the design 2026-09-04, marked "Ordered" in the 2026-03-16 workbook.

**Audit result: PASSED at the refdes level.** All nine are absent from `BOM_2026-09-04.csv` and from the
extracted netlist. `[SUSPECTED - local parse, not reproduced in this session. This check is the only
thing standing between the build and re-ordering nine parts; re-run it where the repo is accessible
before signing off.]`

**But "cancel these MPNs" is the WRONG instruction for three of them.** Apply the deletion as a
**per-MPN quantity delta against the old workbook, not as a part-number blacklist.**

| Refdes | MPN | Disposition |
|---|---|---|
| Q2 | FDN338P | **Cancel outright.** But **verify what actually shipped** - the PCB records Q2 as **FDN340P** while the workbook ordered **FDN338P**. The two sources disagree about which P-FET was even bought. |
| Q3 | SS8050 | **Cancel outright.** |
| U7 | MIC5504-1.8YMT-TR | **Cancel outright.** Note the +1.8 V rail is **not** orphaned - it comes from U2.29 (BG95 VDD_EXT). |
| R10, R29, R30 | (line quantities) | **Cancel these line quantities.** R29/R30 were the gate-drive network around the deleted Q2/Q3. (R25 is also absent - that is an unused designator, not a deletion.) |
| C12 | JMK105BJ105KV-F | **REDUCE BY 1, DO NOT CANCEL.** Still needed x4 on C2/C11/C29/C39. Nets to zero only if you apply the Taiyo Yuden EOL cross to MSASJ105SB5105KFNA01. |
| C19 | CL05A104KA5NNNC | **REDUCE BY 1, DO NOT CANCEL.** Still needed **x10** on C1/C4/C5/C7/C17/C18 **and** C30/C37/C38/C40. **This is the only MPN that genuinely needs a delta.** |
| C20 | GRM158R60J226ME01D | **CANCEL NOW.** It survives in the BOM only as the *wrong* carried-forward MPN on C10/C13. **An earlier recommendation to "hold the order until C10/C13 are re-sourced, or you strand those positions" is wrong**: it is a 0402 6.3 V part and C10/C13 are 0805 at 3.3 V bias - it physically cannot be placed and would not hold its value if it could. Holding the order protects nothing. |

**The board is not clean even though the BOM is.** All nine deleted parts still have live footprints on
`bingbong.kicad_pcb`, so a board-derived pick-and-place, or a CM working from the `.kicad_pcb`, would
happily re-order and re-fit every one of them.

---

## 7. BOM hygiene

### Missing fields a turnkey assembler needs

**Present and adequate:** Refs, Qty, Value, DNP.
**Present but weak:** MPN (4 purchasable lines have none, 2 are float-corrupted, at least 7 are wrong);
Footprint (a KiCad library path, not an industry package name); LegacyPkg (float-corrupted to `402.0`
and **unusable on 14 lines** - blank on 6, `--` on 8).
**Entirely absent:** **Manufacturer** (no column at all - MPN alone is ambiguous for generic passives
and every quoting portal asks for it), placement **Side**, **Mounting** type (SMT/THT), and **LCSC**
part number - which is what JLCPCB actually matches against.

- **Side matters here.** SW1 is on B.Cu, so this is a double-sided-placement board. Side normally comes
  from the CPL, but with the PCB out of sync the CPL cannot be trusted either, so **nothing in the
  deliverable currently states it.** *(The F.Cu 90 / B.Cu 1 census was taken from the stale PCB and is
  meaningless until the resync - do not carry that number forward.)*
- **Four lines are THT** - C3 (470 uF radial), J6 (header), SW1 (Cherry MX), TH1 - which a turnkey SMT
  line will not reflow and will quote as a separate hand-solder operation. Three of the four are
  candidates for elimination (C3 -> polymer SMT, J6 -> test pads, TH1 -> JST or SMD NTC).
- Re-add **Assembly (YES/NO)** explicitly rather than relying on DNP inference.
- Replace the KiCad footprint path with a plain **package** column (0402, 0603, SOT-23-6, QFN-20).
- **Export BOM and CPL from the same post-sync database in one operation** so they cannot drift.

### Costing is incomplete and the rollup is misleading

Six lines have no Price, eight have no DigiKey number, six have no datasheet. The extended cost of the
priced non-DNP lines is **$53.60 covering 88 of 96 purchasable placements** - 8 placements are unpriced
and the **~$11.21 display is missing entirely**, so the true build-1 cost is materially higher than the
file shows. **SW1 is the weakest line**: a hobby-channel part with DigiKey `--` and Datasheet `--`,
unquotable by any turnkey house as written.

### DNP handling

Mostly right. The schematic's 8 `(dnp yes)` flags match the BOM's 8 DNP cells exactly, they are
correctly excluded from the 96 purchasable placements, and they contribute nothing to the cost rollup.
Three problems:

1. **J6 carries no DNP flag anywhere** despite being described as deliberately unpopulated - it counts
   as a purchasable placement with no MPN. Pick one and record it.
2. **The seven DNP caps are collapsed into ONE line** that cannot express two electrically different
   stuffing options. **The schematic Value for all seven is the literal string `DNP`, which destroys the
   capacitance data entirely.** The real intent survives only in the Description fields, and the BOM's
   70-char truncation drops the SIM EMI group's description completely. **Split into two lines:**
   (a) C32/C33/C35/C36 = RF pi shunts, 0402 C0G, populate-on-tune, note the 0.5-10 pF sweep range - do
   not pick a single value; (b) C41/C42/C43 = **33 pF C0G 0402** SIM EMI shunts, which have a definite
   value and should carry a concrete MPN now.
3. **Move the value out of the Value field** and let `(dnp yes)` carry the DNP state, which is where it
   belongs in KiCad. R24 already does this correctly - it is DNP yet retains its MPN.

### The SchDescription truncation is destroying placement instructions

The generator truncates SchDescription at **exactly 70 characters**, silently discarding the only field
carrying placement and assembly constraints:

- **J5's** 204-char description keeps 70. Lost: *"Pin order VERIFIED 26/26 against datasheet section 5 /
  Table 5.1 on 2026-09-04 - pad N = display pin N, DIRECT map. Do not renumber."* That is a
  do-not-repeat-this-work record, now absent from the deliverable.
- **R24** loses the condition that governs whether it is stuffed: *"populate only when no battery NTC is
  installed."*
- **TH1** loses its pin-1/pin-2 assignment.
- On multi-refdes lines the generator concatenates **then** truncates, so the C30/C37/C38/C40 line ends
  at *"USIM_VDD bypass - X7R, place "* and drops **entirely** both *"VBUS HF bypass - X7R, PLACE WITHIN
  5mm OF U8 PINS 18/19"* (C37) and *"USIM_VDD bypass - X7R, place within 3-5mm of J7 pin C1"* (C38).

**Remove the truncation.** These are the placement constraints a turnkey assembler and the layout
engineer both need.

### The schematic-side root cause

**The schematic cannot supply the data the BOM needs.** A property census over all 104 non-power symbols
found only Reference/Value/Footprint/Datasheet/Description on all 104, with **Datasheet populated on
just 14** (CR1-CR8, J5, Q1, R24, U1, U8, U10) - the other 90 empty or placeholder. **No capacitor value
string contains a voltage.** So the BOM has no way to state that C10/C13 need 0805 *specifically to keep
real capacitance at 3.3 V bias*, that C15 must be 16-25 V because it sits on VBUS, or that C31/C34 and
C41-C43 must be C0G - **the exact requirements that half the flagged lines depend on.**

*Correction to an earlier draft: it is **not** true that zero symbols carry Manufacturer or MPN.* Six
carry MANUFACTURER (J2 "Molex"; J3/J7/J8 "TE Connectivity"; S1/S2 "CUI Devices" - now Same Sky) and two
carry both MF and MP (U2 `BG95M3LA-64-SGNS` / Quectel; U3 `SN74AVC2T245RSWR` / Texas Instruments), all
from vendor-supplied SnapEDA/TE symbols. **A field that exists on 6 of 104 symbols and is not emitted to
the BOM is arguably worse than one that does not exist at all** - it strengthens the recommendation.

**Add these symbol fields in KiCad and emit them as columns:** MPN, Manufacturer, Voltage (caps),
Tolerance, Dielectric (caps), Power (resistors), **Current/Isat (inductors)**, LCSC, Mounting (SMT/THT).
**Make MPN live in the schematic as the single source of truth** so it can never again be carried forward
by refdes from a stale workbook - **that merge strategy produced every wrong-MPN finding in this review.**

The mechanism is worth stating precisely: **deletions propagate through the netlist, but value changes do
not propagate through the carry-forward merge.** That is why R29/R30 vanished cleanly while L1, C10/C13,
C15, R11/R13 and the R2 group all kept stale part numbers in the same regeneration.

Note there is no Isat/current column at all, which is why nothing in this file could express that L1
needed >=1.4 A - the checker structurally could not see the most important of its four defects.

### Checker gaps

The ReviewFlag pass **only ever compared package numerals.** It never compared Value against the
carried-forward MPN, so it produced **10 entries, 1 false positive, and missed 3 real errors**:

- **Missed entirely (ReviewFlag empty):** C6/C21 (1000x) and R11/R13 (680 R vs 1 k) - both had matching
  packages, so the numeral-only check stayed silent.
- **Half-caught:** L1 - flagged "PACKAGE MISMATCH sch=1008 bom=0603" but missed the value change, the
  component class and the current rating.
- **Half-caught:** C15 - flagged the package but missed that the reason it changed is a 10 V part on a
  VBUS rail, and missed that the same MPN is correct on the C8/C9 line.
- **False positive:** U8 "MPN CONFLICT" - the checker compared Value `MCP73871-2CCI_ML` against MPN
  `MCP73871-2CCI/ML` and tripped on underscore-vs-slash. The underscore is just KiCad's symbol-name-safe
  substitution. **Someone working the flag list could "fix" a correct MPN.**

**Add:** Value-vs-MPN/LegacyDesc comparison (one regex over LegacyDesc catches all three misses);
**duplicate-MPN-with-different-Value detection** (would have caught R11/R13 and C15); scientific-notation
detection; underscore-to-slash normalisation before comparing; and a **BOM-vs-PCB refdes diff**, which is
the check that would have caught the blocker in this review. **Keep** the refdes-coverage and Qty checks
- they work.

### Duplicate lines

Four MPNs appear on two lines each. `CL05A104KA5NNNC` splits 6+4 purely because the schematic spells the
same value `0.1uF` on six symbols and `100nF` on four - **merge into one line of qty 10.** Normalise
value strings to one convention, and fix `470 uF` (the only value with a space) and the bare `0` on the
zero-ohm line.

---

## 8. Appendix: claims that failed verification

**No research claim was dropped outright.** These are the sub-claims that verification **refuted,
weakened or could not confirm**. They are listed so nobody acts on them.

**Refuted:**

- **"C0603C101K5RACAUTO7411 is not orderable at any distributor."** False - `7411` is a legitimate Kemet
  bulk-pack (7" reel) suffix that appears as a live catalog line at several distributors. A pasted PO
  **orders the wrong part rather than failing** - worse, not better.
- **"GRM158R60J226ME01D supply is thin."** Single-distributor artifact. Arrow's 0/10 wk/40 k MOQ is real,
  but DigiKey ships same-day and TME, Farnell, Future and JLCPCB all carry it. Do not cite supply as a
  reason to change - the package/voltage mismatch carries that finding alone.
- **"GRM155R61A106ME11D may be EOL."** No distributor carries an obsolescence flag. Arrow 28,558 @ 10 wk,
  TME available, TTI 910,000 on order for 29-Jan-27. **Supply-constrained but live.** The in-repo
  datasheet being a saved 404 page is **not evidence of anything** - drop it from the file.
- **"CL31B475KAHNNNE is stocked at DigiKey."** DigiKey shows In Stock 0 / backorder. **Mouser holds
  ~90,369** and LCSC is stocked - buy elsewhere.
- **"T520V227M006ATE040 / ...ZTE025 both ship today at DigiKey."** Unsupported. ATE040 shows In Stock 0;
  the ZTE040 page carries an "obsolete and no longer manufactured" flag on its main part; and the
  "ships today" text for ZTE025 traces to a **cached page whose footer reads 1995-2022** - exactly the
  failure mode this review exists to catch. Better-evidenced: **T520V227M010ATE040, 5,857 @ $2.43.**
- **"GRM1555C1H100JA01D is backorder-only at DigiKey" / "GRM1555C1H330JA01D is thinning."** Both refuted -
  DigiKey 3661907 and 3693846 both ship, Arrow has stock, TrustedParts rates both risks Low. **Do not
  reverse primary/alternate to Samsung on this basis; pick on price.**
- **"AF0402JR-07680RL"** - **not found at any distributor.** It was constructed by decoding the AF series
  naming convention: the invented-part-number failure mode. **Do not order it.** Use RC0402FR-07680RL,
  AC0402FR-07680RL or RC0402JR-07680RL.
- **"Zero schematic symbols carry Manufacturer or MPN."** False on two of seven fields - six carry
  MANUFACTURER and two carry MF/MP. See §7.
- **"Hold the GRM158R60J226ME01D order or you strand C10/C13."** Wrong on its own terms - it is a 0402
  6.3 V part that physically cannot be placed on an 0805 land. Cancel now.
- **"Murata DFE201610P-3R3M"** (named in the change note as the L1 replacement) - **does not fit.** It is
  2.0 x 1.6 mm against a 3.40 mm 2520 land span.
- **"220 uF 6.3 V polymer in 1210"** (the brief's premise for C3) - **does not exist.** Kemet case V is
  7343-20; budget a **2917** land.
- **"`-SGNS` is the GNSS suffix"** (the brief's premise for U2) - it is the generic non-customer-specific
  build code; GNSS is set by the model number and every BG95-Mx has it. `[SUSPECTED - ordering table is
  NDA-only.]`
- **"E2 is the broadband 617-4200 MHz part"** - ANT-LTE-RPC-UFL is **600 MHz - 3.8 GHz**. It does cover
  B71; it does not reach 4.2 GHz. Do not carry the wrong number into a spec.
- **"ER-CON26HT-1 is a cart add-on requiring a quote email"** - it has its own standalone buydisplay
  product page. Order it directly.
- **"MCP73871 has a 21-52 week lead time"** - artifact of the 91-piece **tube** packaging. Future quotes
  **4 weeks on the T&R reel**. Discount the RS 52-week figure (quoted against zero stock).
- **"ESP32-S2-SOLO-2U-N4R2 is a supply hedge"** - DigiKey shows **14 pcs**. It is a qualification path.

**Weakened / could not be confirmed:**

- **The whole PCB-desync blocker** rests on a local-file analysis that could not be reproduced in the
  verification session or in this one. It is internally consistent and the counts are specific, but
  **run Update PCB from Schematic and read the change list before acting on it.** One minute settles it.
- **The deleted-parts refdes audit** rests on a single unreproduced parse. Re-run it.
- **"Yageo RE is unstockable"** - the 20-week/not-stocked evidence comes from a **different** RE part
  (RE1206FRE07470KL), and JLCPCB does carry an RE 0402 100 k. Reasonable inference about a low-volume
  precision grade; not established for RE0402FRE07100KL. Does not change the recommendation.
- **"C26 is 10x the vendor reference (22 pF vs 220 pF)"** - the R1200 recommended-components table could
  not be extracted from any accessible copy. **Raise as "please confirm against the table", not as a
  confirmed error.** Note R28's finding independently states the table gives C3 = 220 pF with R3 = 2 k,
  which **contradicts** the 22 pF claim - the two research passes disagree. Settle it from the datasheet.
- **"MLZ2012N220LT000 fixes L2"** - its **saturation** current is not established (only rated /
  temperature-rise current). Swapping P for N may leave the saturation problem intact. The defensible
  fix is VLF3010A-220, which is **not** a drop-in.
- **The ER-OLED018-1 "11.5 / 12.0 / 12.5 V VCC window"** driving the R26 finding - source returns 403.
  The only primary figure obtainable is the SSD1326 controller's **9-15 V**, which the 11.20-12.88 V
  worst case does **not** violate. The 1% fix is still correct and free, but the justification is weaker
  than stated.
- **The Kemet T491 derating rule** (50% of VR to +85C / 33% above), the **75 mW A-case dissipation limit**
  and the **~112 mA rms ripple figure** - the PDF would not extract to text. Consistent with well-known
  Kemet practice but **not read**. Also, 48% of rating is *inside* the 50% rule at normal ambient, so
  **this is a thin-margin argument, not a violation.**
- **"The R1200 datasheet says 'Ceramic capacitors are recommended'"** - not found in the accessible text.
- **The R22/R23 finding depends entirely on an assumed ~60 pF** bus capacitance. At 30 pF the existing
  10 k gives tR ~254 ns and the finding largely evaporates. Nobody measured it.
- **The 4.23-4.35 V VPCC band** was quoted to two decimals while ignoring the MCP73871's own ±3% VPCC
  threshold tolerance. Corrected to **~4.10-4.48 V**. Conclusion unchanged.
- **"E2 ANT-LTE-RPC-UFL is Active"** - Active at TE and DigiKey, but **"Reference Only / in transition"
  at TTI and "no longer being manufactured" at OnlineComponents.** Unresolved.
- **"The display is at zero on-hand"** - never established. It is single-source with **unknown** stock at
  a published price. Only the **battery** is confirmed unbuyable. Do not conflate the two.
- **The ASR00035 "under-rated at 1C" argument** - both datasheet PDFs are unreadable, so the PCM trip is
  **unknown, not known-bad**. 600 mA from a 500 mAh pouch is 1.2C, ordinary. Re-source for the
  **delisting** and the JST SH termination, not the load.
- **The eBay "~10 available / 163 sold"** figure for the display - a listing field, not inventory.
  Dropped. The sole-source / no-distribution / no-lead-time combination stands on its own.
- **"J5's ER-CON26HT-1 is a drop-in for the existing land"** - the land matches Hirose's 12.5 mm contact
  span, but **the project footprint has never been checked against the ER-CON26HT-1 drawing** (it carries
  a Hirose FH12-26S 3D model over TE-class copper, per review finding M-3), and the buydisplay datasheet
  403s. The footprint needs rebuilding regardless (H-13: one `fp_rect` on F.CrtYd and nothing else - no
  pin-1 marker, no silk body), which is why switching to Hirose while rebuilding costs near zero.
- **"TPD2EUSB30ADRTR footprint is verified"** - the body outline matches published dimensions, but **TI's
  DRT0003A land-pattern drawing was not in the retrieved PDF.** Verify before fab; the pads are 0.20 mm
  wide, right at the edge for ENIG.
- **"J7 is rated ~5,000 mating cycles"** - not on the customer drawing; it lives in app spec 108-140328
  which te.com would not serve. **Unverified.**
- **"C22/C23's GRM31CR71E475KA88L is Obsolete"** and **"C25's GRM188R71E105KA12D is Obsolete"** - the
  latter is cited to a DigiKey page; the former is unverified.
- **"MSASJ105SB5105KFNA01 is orderable"** - **could not be confirmed.** Mouser/Future carry sibling
  MSASJ105 values but this exact code did not surface with a quantity. Verify via Taiyo Yuden's stock-check
  portal before committing. Likewise the 16 V C2 alternates (GRM155R61C105KA12D, CL05A105KO5NNNC) were
  not individually verified.
- **"J2 is Active"** - from a **Molex-generated document dated 2021-09-07**; molex.com refused access.
  No EOL or PCN found, and TTI's "Reference Only" label sits alongside 192,400 pcs so it reads as a
  stocking label - but **get a formal statement before production.**
- **All DC-bias retention percentages** in §5 are **engineering estimates**. Murata SimSurfing could not
  be driven; no published curve was read.
- **Everything sourced to `_t12.nets`, `_t12_netlist.xml`, `bingbong.kicad_sch`, `bingbong.kicad_pcb`,
  `_bg95.pdf`, `_r1200_ds.txt`, `_dsx/*`, `SCHEMATIC_REVIEW_2026-09-03.md` and the `_bomaudit_*.py`
  scripts** - including every netlist-derived duty claim in this report - was read by the research passes
  but **could not be re-read during verification or during the writing of this document.** Treat those as
  the reviewers' reading of the local files, not as independently confirmed.
- Several stock figures (Kemet C0603C104K5RACTU, the Murata 25 V 0603 aggregate, the Wurth 885012206055
  line, R21/R27/R28/R4 quantities, AF-series quantities) are **search-index snapshots or explicitly
  UNVERIFIED**, because DigiKey returns HTTP 403 to automated fetch and Mouser/Arrow/TME/Octopart/
  TrustedParts variously 403 or time out. **Every quantity in this report is a 2026-09-08 snapshot.
  Re-pull before spending money.**

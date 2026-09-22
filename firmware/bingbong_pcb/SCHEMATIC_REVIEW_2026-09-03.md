# Bingbong Schematic Review - 2026-09-03

Sources: `bingbong.kicad_sch`, `review_netlist.xml` (same timestamp as the schematic - current), `review_erc.rpt` / `review_erc.json`, `bingbong.kicad_pcb` (advisory only), `bingbong.kicad_dru`, `bingbong.kicad_pro`, `Bingbong_library.kicad_sym`, `Bingbong_library.pretty/*`, `../bingbong_bom_260316 (1).xlsx` (parsed directly), and the prior review pair `schematic_deep_review_report.md` / `review_refutation_matrix.md` (2026-06-06).

Method: six independent domain passes (ZIF/J5, USB-C protection, power tree, RF/antenna, ESD/failsafe, pin-map/digital), each then run through an adversarial refutation pass against the raw files. **Seven findings were refuted outright and are in Appendix 8** - two of them proposed edits that would have damaged the board. Everything below survived refutation. Severities and wording here are the *post-refutation* ones, which are in several places lower than the original pass claimed.

*(An earlier, pre-refutation draft of this file was moved to `SCHEMATIC_REVIEW_2026-09-03.predraft.bak`. Where this document contradicts it, this document is correct - see the end of Appendix 8 for the specific retractions.)*

**Headline count after de-duplication across passes: 4 CRITICAL, 14 HIGH, 21 MEDIUM, 19 LOW, 9 INFO.** (Pre-merge the six passes produced 22 critical/high; the same USB-VBUS, J6, charger-strap, battery-reverse-polarity and ZIF-silkscreen issues were each found independently by 2-3 passes.)

Every claim below carries a file+line or a netlist net name. Items are tagged **[CONFIRMED]** (proven from the files in this project), **[SUSPECTED]** (depends on a datasheet or convention I could not read from these files), or **[NEEDS USER INPUT]** (depends on your design intent).

### Prior-review (2026-06-06) fix verification

| Prior item | Actual state in the CURRENT files | Evidence |
|---|---|---|
| C1: USB D+ loaded by C19/C20 | **CONFIRMED FIXED** | `review_netlist.xml` has zero components `C19`/`C20`; `/USB D+` = {J2.A6, J2.B6, R17.1, U5.1} |
| C2: Q1 PWRKEY B/E swap | **CONFIRMED FIXED in schematic**; footprint orientation now also proven correct | `Net-(Q1-B)` = Q1.1 + R1.2; Q1.2 in GND; `SOT-23-3_1P4X3P040_ONS.kicad_mod` pad1 (-0.9525,1.016), pad2 (+0.9525,1.016), pad3 (0,-1.016) = JEDEC SOT-23. Old `.kicad_pcb` still stale - moot, you are re-laying out |
| H3: MCP73871 THERM | **FIXED**, and the follow-on hazard is smaller than the earlier draft claimed - see M-12 | `Net-(TH1-Pin_1)` = R24.2, TH1.1, U8.5; BOM buys the NTC and does *not* buy R24 |
| H6: U3 DIR1 on wrong rail | **CONFIRMED FIXED**, and both UART directions are now proven correct | U3.10 (DIR1) and U3.7 (VCCA) both on `+1.8V`; U3.1 (DIR2) on GND. See INFO-4 |
| H7: SIM implementation incomplete | **NOT FIXED** | `/BG95_VCC` = {J7.C1, U2.43} only - two nodes, no cap, no ESD (`review_netlist.xml:2387`) |
| CR1-3 MPN alignment | **NOT FIXED** (documentation only - the land is correct for the ordered part) | schematic Value `PESD5V0F1BLD_315`, footprint `Diode_SMD:D_SOD-923`, BOM row 14 buys `ESD9B5.0ST5G` which **is** SOD-923 |
| M2: Q2 FDN340P vs FDN338P | **NOT FIXED** (metadata only - both are P-channel) | netlist value `FDN340P`; BOM row 25 `FDN338P`, description "P-Channel 20 V 1.6A" |
| M6: ERC pin-type noise | **NOT FIXED** | 34 errors + 9 warnings still in `review_erc.rpt` |
| Q1 "pad 1/2/3 orientation signoff" (left open) | **NOW CLOSED - correct** | see the C2 row above |

**What the prior review missed entirely:** it never mentions J5, the ZIF, the display, or FFC (one incidental hit at `schematic_deep_review_report.md:466`). It also never looked at J6, mounting/retention, test points, DRC exclusions, reverse polarity, the stackup, netclasses, or the antenna BOM. Those are where most of this report lives.

---

---

## 0. APPLIED CHANGES - schematic edit log (2026-09-04)

All edits below were made directly to `bingbong.kicad_sch` and **verified by
netlist diff** (`kicad-cli sch export netlist`) - every change produced exactly
the intended connectivity delta and nothing else. ERC went **43 -> 41**
violations with no new classes introduced. Pre-edit backup:
`bingbong.kicad_sch.prefix.bak`.

### Topology changes

| ID | Change | Verified delta |
|---|---|---|
| **C-1** | PROG2 (U8.4) cut away from the shared SEL/GND tie (#PWR050) and given its own net `/CHG_ILIM` with pull-up **R31 = 100k to +3.3V**, routed to **IO35** (U10.28). **SEL stays on GND.** | `GND` lost `U8.4`; `/CHG_ILIM` = `U8.4 R31.2 U10.28`; `+3.3V` gained `R31.1` |
| **LOW-7** | **VPCC (U8.2) broken away from IN** and given the datasheet Fig 3-1 divider: **R33 = 100k** (+5V->VPCC), **R34 = 40.2k** (VPCC->GND), **C30 = 100nF** bypass. | `+5V` lost `U8.2`, gained `R33.1`; new `/VPCC` = `U8.2 R33.2 R34.1 C30.1` |
| **H-5** | Charger `CE` pull-**down** converted to a pull-**up**: the GND symbol on R16 was replaced with a `SYS LOAD` label. Deliberately **not** `+3.3V`, which is generated downstream of the charger. | `/SYS LOAD` gained `R16.1`; `GND` lost it |
| **M-8** | LBO telemetry: **R32 = 100k** pull-up added on U8.8 (STAT1/LBO) and routed to **IO36** (U10.29) as `/BATT_LOW`. D3 stays in parallel - the open-drain pin sinks both. | `Net-(D3-K)` -> `/BATT_LOW` = `U8.8 D3.1 R32.2 U10.29` |
| **C-2** | **Deleted Q2, Q3, R29, R30** - the entire external power-switch network around the R1200 boost - and made CE the sole enable with a **100k pull-down (R35)**. The R1200's own standby (max 3 uA at VCE = 0, internal NPN isolates output from input) makes the P-FET redundant. Kills the abs-max violation where IO8 drove CE to 3.3 V while Q2 held VIN at 0 V. **Frees IO18.** | `Net-(Q2-D)`, `Net-(Q2-G)`, `Net-(Q3-B)`, `/R1200 PWR EN` all gone; `/R1200 CE` gained `R35.1`; `+3.3V` lost `Q2.2`,`R30.1` |
| **H-6 (1)** | Boost input moved from `+3.3V` to **`/SYS LOAD`** - removes ~136 mA of double-conversion load from the 0.5 A buck. | `/SYS LOAD` gained `C24.1 L2.1 U1.3` |
| **M-6** | **Deleted U7 (MIC5504), C12, R10** and re-sourced the 1.8 V rail from **U2.29 (VDD_EXT)**, the modem's own IO reference. VDD_EXT is 0 V whenever the BG95 is off, so U3's VCC isolation puts the A port Hi-Z and the ESP32 can no longer back-power `/BG95 RX` and `~RESET` through a dead IO domain. C11 (1uF) + C4 (0.1uF) remain as VDD_EXT decoupling. **Frees IO13.** | `+1.8V` lost `U7.1`, gained `U2.29`; `/MIC EN` gone |
| **M-6b** | **U2.20 (STATUS)** connected to **IO37** as `/BG95_STATUS` - the PWRKEY toggle through Q1 was open-loop, so a hung modem had no recovery path. | new `/BG95_STATUS` = `U2.20 U10.30` |
| **H-9** | **`/ANT_MAIN` pi network added.** Was a bare two-node net (U2.60 -> J3.1). Now `U2.60 -+- C31 -+- J3.1` with **C32 / C33** shunts to GND either side, both **DNP**. C31 = 15 pF C0G, populated, doubling as the DC block. J3.1's label changed `ANT_MAIN` -> `ANT_MAIN_OUT`. | `/ANT_MAIN` = `U2.60 C31.1 C32.1`; `/ANT_MAIN_OUT` = `J3.1 C31.2 C33.1` |
| **H-8** | **GNSS wired up.** Removed the no-connect flag on **U2.49 (ANT_GNSS)**, added **J8** (second CONMHF1-SMD-T, cloned from J3) and its own pi: **C34** series 15 pF populated, **C35 / C36** shunts DNP. | `/ANT_GNSS` = `U2.49 C34.1 C35.1`; `/ANT_GNSS_OUT` = `J8.1 C34.2 C36.1`; `GND` gained `J8.2/3/4` |
| **H-4 / LOW-2** | **USB-C ESD added.** **CR4 -> `/USB_CC1`**, **CR5 -> `/USB_CC2`**, **CR6 -> VBUS (+5V)**, all **ESD9B5.0ST5G** cloned from CR1 - already BOM row 14, so **zero new BOM lines**. The part is bidirectional, so orientation is a non-issue. Also **C37 = 100 nF** HF bypass on `+5V`, which previously had only C15. | `/USB_CC1` = `J2.A5 R7.1 CR4.1`; `/USB_CC2` = `J2.B5 R8.2 CR5.1`; `+5V` gained `CR6.1 C37.1`; `GND` gained the four returns |
| **LOW-9** | ESD symbol pin electrical type **`unspecified` -> `passive`**, in both the schematic's cached `lib_symbols` **and** `Bingbong_library.kicad_sym` so they agree. Also cleared the stale `PESD5V0F1BLD_315` string from CR1-3's Datasheet field. | no connectivity change; **`pin_to_pin` 26 -> 14** |
| **H-12a** | **USIM_VDD bypass + ESD.** `/BG95_VCC` was `{J7.C1, U2.43}` and nothing else. Added **C38 = 100 nF**, **C39 = 1 uF** and **CR7** (ESD9B5.0ST5G). Quectel requires the local bypass; without it the SIM browns out during ATR and card init is intermittent - which reads as a bad SIM or bad provisioning, not a hardware fault. | `/BG95_VCC` = `J7.C1 U2.43 C38.1 C39.1 CR7.1` |
| **H-12b** | **SIM detect conditioned.** `/SIM SW` ran from an exposed slot contact straight into ESP32 IO33 with zero impedance and **no pull at all - the pin floated**. Split into **`SIM_SW`** (connector side: J7.SW + **CR8** ESD) and **`SIM_DET`** (MCU side: **R37** 10k pull-up to +3.3V + **C40** 100 nF), bridged by **R36 = 1k** series. | `/SIM_SW` = `J7.SW CR8.1 R36.1`; `/SIM_DET` = `U10.24 R36.2 R37.2 C40.1` |
| **H-12c** | **SIM EMI pads.** **C41/C42/C43** DNP 22 pF shunts on `/BG95_CLK`, `/BG95_RST`, `/BG95_IO` per Quectel's SIM reference - stuffing options, unpopulated in build 1. | each SIM signal net gained one DNP shunt |

**SIM block: ERC unchanged at 35 with 10 parts added.** Component count 94 -> 104.

**Two things to verify on H-12b:**
1. **Detect-switch polarity [ASSUMPTION].** The 10k pull-up assumes J7's switch
   closes SW to GND on card insertion, which is the usual nano-SIM arrangement.
   With R37 on the MCU side of R36, a closed switch gives 3.3 x 1k/11k =
   **0.30 V**, a solid low against a ~0.83 V VIL. **Confirm against the TE
   2452808-1 drawing** - if the switch instead opens to GND, the logic inverts
   (firmware fix, not a hardware one).
2. **U2.42 (USIM_DET) deliberately left unconnected.** Wiring the detect switch
   to it as well would let the modem see card removal directly, but the required
   polarity and level are Quectel datasheet values I could not verify from this
   project, and connecting it wrongly is worse than leaving it open. Decide with
   the datasheet in hand.

**Where SIM protection now stands:** all six user-touchable contacts are covered -
CLK/IO/RST by CR1-3 (pre-existing), VCC by CR7, and the detect line by CR8 plus a
1k series limiter. VCC also finally has its bypass. That closes the "three of six
contacts protected and VCC is not" gap.

**ERC 43 -> 35, the lowest it has been.** The ESD symbol declared both pins
`unspecified`, which conflicts with `power_output` GND pins and generated two
bogus `pin_to_pin` violations per diode. Setting them `passive` cleared 12 at
once. Note the two-step: editing only the schematic's cached `lib_symbols`
produced 6 `lib_symbol_mismatch` warnings until `Bingbong_library.kicad_sym` was
updated to match - **if you only fix the cache, a future "Update Symbols from
Library" silently reverts it.**

**NOT DONE - the OVP / current-limit load switch.** This is the remaining half of
H-4 and it needs a decision from you, because:
- The part is unchosen. AP22815AWT-7 (SOT-25, ~5.7 V OVP, 2 A, soft-start,
  reverse-current block, FLAG output), TPS2596ARDPR (adjustable OVP + ILIM) and
  TPD1S514DBVR (OVP + current limit + integrated D+/D- ESD, would let you delete
  U5) are all **[SUGGESTION - unverified]** in this report.
- It needs a new library symbol, which nothing in `Bingbong_library` covers.
- It **splits `+5V` into connector-side and protected-side nets**, and section 3.2
  requires that **no branch tap VBUS upstream of the switch - including J6 pin 4**,
  which must move to the load side. C15 also moves to the switch output.

That last point matters for sequencing: doing it after the re-layout means
re-routing the whole VBUS path. **Pick the part before you route.** Until then
the board is protected against ESD but not against a non-compliant >7 V charger,
which is the failure U8's ~7 V abs-max input cannot survive.

**Netclass follow-up (applied).** Splitting each RF chain in two created
`/ANT_MAIN_OUT` and `/ANT_GNSS_OUT`, which did **not** match the existing
`RF_50` patterns and would have silently fallen back to `Default` 0.2 mm - an
impedance discontinuity in the last few millimetres before each connector.
`bingbong.kicad_pro` now assigns all four RF nets to `RF_50` (0.38 mm / 0.20 mm gap).

**Grid discipline.** The first attempt at this block placed parts on arbitrary
coordinates and produced **16 `endpoint_off_grid`** violations. All RF geometry is
now on exact multiples of **1.27 mm**. Off-grid endpoints are dangerous here
because they can *look* connected and not be.

**Still open on the RF block (not schematic work):**
- **E2 / E3 antenna line items.** Nothing is purchased yet - the BOM's only
  antenna row is the 2.4 GHz Wi-Fi patch. GNSS needs a **1575.42 MHz L1** part.
- **Active vs passive GNSS antenna.** If active, the chain needs a bias tee
  (33-47 nH 0402 wirewound choke to +3.3 V plus a 100 nF C0G series DC block).
  **[SUSPECTED - confirm whether BG95 ANT_GNSS sources bias.]**
- **>= 25 mm separation between J3 and J8**, and GNSS wants sky view while the
  cellular antenna wants distance from the user's hand. On a 120 x 37.5 mm board
  this is the binding mechanical constraint.
- **Tune on a VNA with the case closed and the battery fitted**, then freeze the
  pi values. Keep each pi within 5 mm of its connector, added trace <= 4 mm, and
  stitch each shunt's ground pad with >= 2 vias within 0.5 mm.

**Side effect - C-3 is now moot.** U7 is deleted, so the structurally broken
`TDFN1010-4LD-PL-2_MCH` footprint (2-mil pads, un-netted copper polys as the real
lands, zero mask expansion, no thermal paste) and its **6 suppressed
`shorting_items` DRC errors** leave the design entirely. That was the one
footprint-anchored exclusion whose UUIDs would have survived the re-layout.

**Component count 89 -> 83.** Seven parts removed (Q2, Q3, R29, R30, U7, C12,
R10), one added (R35).

**ERC 43 -> 41.** `pin_to_pin` dropped 22 -> 20 as U7's power pins left. The two
`pin_not_connected` that appeared are **IO13 and IO18, deliberately freed** - give
them explicit no-connect flags per section 4.3, along with the other 11.

**Two watch items on M-6:** respect Quectel's VDD_EXT current limit (typically
50 mA - present load is U3's VCCA/DIR1, R2, J6.2 and two caps, comfortably
inside), and note the 1.8 V rail now only exists while the modem is powered, so
any firmware that assumed it was independently controllable via IO13 must change.

**On the PROG2 default direction.** R31 is a pull-**up**, so the power-on default
is the **500 mA** setting, not 100 mA. Rationale: if firmware never drives IO35,
a pull-down would leave the board at the 100 mA one-unit-load limit against
~460 mA demand - i.e. C-1 unfixed. Inverting makes the fail-safe direction
"works", and firmware can still pull IO35 **low** to force 100 mA. The pull-up
**must** be +3.3V: IO35 is not 5 V tolerant, so +5V or `/SYS LOAD` would
over-stress the pin. A useful side effect is a staged start - with a flat cell
the charger comes up at 100 mA while +3.3V is still down, then steps to 500 mA
once U6 is running.

**That is why LOW-7 is no longer optional.** VPCC shorted to IN disables input
foldback, which is safe at 100 mA but not at 500 mA. The 100k/40.2k divider sets
the knee at **VIN ~ 4.29 V** (VPCC threshold 1.23 V). The datasheet's own
330k/110k was rejected: it gives a 4.92 V knee, which would nuisance-trip on a
healthy 5 V supply after normal cable drop, whereas 4.29 V engages only when the
source is genuinely weak. USB 2.0 permits VBUS down to 4.40 V at the device.
Lay the divider out so it can be depopulated back to a 0 ohm short.

**[SUSPECTED - confirm]** MCP73871 V_IH for PROG2 at VDD ~ 5 V. If V_IH scales
with VDD (commonly ~45 %, i.e. 2.25 V) then a 3.3 V high is comfortable, but the
datasheet was not readable from this project.

### Value / metadata changes (zero connectivity impact, netlist-verified)

| Ref | Was | Now | Why |
|---|---|---|---|
| `R15` | 10k | **100k** | **H-3** - ITERM was 100 mA, at/above the achievable charge current, so termination never fired |
| `L1` | 2.2uH, 0603 | **3.3uH, `L_1008_2520Metric`** | **H-6** - was a 500 mA *multilayer decoupling* part in a 500 mA converter; needs Isat >= 1.4 A (VLS252012HBX-3R3 class) |
| `C10`, `C13` | 0402 | **0805** | **H-6** - 22 uF 6.3 V 0402 X5R keeps a fraction of its value at 3.3 V bias |
| `C15` | 0402 | **0603** | **LOW-5** - room for a 16-25 V part on VBUS |
| `U1` | Value `~` | **R1200N002A-TR-FE** + datasheet URL | **LOW-18** - the +12 V boost had no MPN at all |
| `CR1-3` | PESD5V0F1BLD_315 | **ESD9B5.0ST5G** | **LOW-9** - match the ordered part. Footprint left alone: the SOD-923 land is already correct |
| `Q2` | FDN340P | **FDN338P** | **LOW-8** - match the BOM; logic-level suits the -3.2 V Vgs |
| `R11`, `R13` | 1k | **680R** | **LOW-14** - green LEDs were at ~1.3 mA |
| `D1-D4` | "LED" | colours recorded | **LOW-14** |
| `J5` | `Conn_01x28_Socket`, Datasheet `~` | **ER-CON26HT-1** + datasheet + description | section 1.6 - records the ZIF **and** notes the pin order was verified 26/26 against the ER-OLED018-1 datasheet |

### NOT yet applied - still open

- **C-2** delete Q2/Q3/R29/R30, move the boost input to `/SYS LOAD`, add the CE pull-down. Structural; needs eyeballing, not just a diff.
- **M-6** derive U3's VCCA from `U2.29 VDD_EXT` and delete U7.
- **C-4 / H-8 GNSS** add J8, `/ANT_GNSS`, the pi network, and the L1 antenna line item.
- **H-4 / section 3** USB VBUS TVS, OVP switch, CC ESD.
- **LOW-6** `~TE` strapping - deliberately deferred, see below.
- **H-12** SIM VCC bypass + ESD; **M-9** remaining PG/STAT2 telemetry.
- **section 4.6** regenerate the BOM (it still orders the deleted C19/C20 and lists C6/C21 as 100 pF against the schematic's 0.1 uF).

**`~TE` note:** now that PROG2 defaults to 500 mA, re-enabling the 6 h safety
timer (tie `~TE` low) is much more defensible than it was at 90 mA - a 500 mAh
cell charges in well under an hour, so 6 h is a comfortable fault backstop
rather than a nuisance trip. Still deferred pending the M-2 decision on whether
the modem stays on the raw cell.

---

## 1. VERDICT ON THE ZIF (J5)

### 1.1 The answer: **NOT REVERSED. The J5 net map is CORRECT — 26 of 26 pins match.** [CONFIRMED]

Settled against the real datasheet: **buydisplay ER-OLED018-1** (1.8" 256x32, SSD1326), `ER-OLED018-1_Series_Datasheet.pdf` **section 5 "Module Interface", page 6/29**, plus **Table 5.1** on the same page.

Pad N maps to display pin N — the **DIRECT** map. No mirror, no swap, no rotation. Do not change any J5 net.

**Everything section 1 said in the previous two drafts about a mirrored pinout is WITHDRAWN.** So are the two J5 findings that were called "orientation-invariant bugs" — both are correct by design (see 1.4).

### 1.2 Why the multi-agent passes got it backwards

Every pass assumed a generic "SSD13xx family template" in which the parallel data bus ascends `D0 < D1 < D2`. On this part it **descends**: the datasheet reads

> `5~12   D7~D0   These is 8-bit-directional data bus.`

so pin 5 = D7 and pin 12 = D0. The whole "mirrored" conclusion rested on the observation that ascending pads read `SDA, SDA, SCL` instead of `SCL, SDA, SDA`. With a descending bus, `SDA(10), SDA(11), SCL(12)` = `D2, D1, D0` — which is **exactly right**, and is precisely what the datasheet mandates:

> "When I2C mode is selected, D2,D1 should be tied together and serve as SDAout,SDAin in application and D0 is the serial clock input, SCL."

That is the schematic's `J5.10`/`J5.11` short (drawn at `bingbong.kicad_sch:12730`) and `J5.12` = SCL. The designer implemented the vendor's I2C wiring correctly. A family-template assumption stood in for the one datasheet nobody had.

### 1.3 Full scoring, DIRECT map

| Pad | Current net | ER-OLED018-1 pin function | OK |
|----:|---|---|:--:|
| 1 | no-connect | NC | OK |
| 2 | `+12V` | **VCC** (OLED drive, supplied externally) | OK |
| 3 | `C23` 4.7 uF -> GND | **VCOMH** (most positive supply; wants a cap) | OK |
| 4 | `GND` | VSS | OK |
| 5 | `GND` | D7 (unused, grounded) | OK |
| 6 | `GND` | D6 | OK |
| 7 | `GND` | D5 | OK |
| 8 | `GND` | D4 | OK |
| 9 | `GND` | D3 | OK |
| 10 | `/OLED SDA` | **D2 = SDAout** (tied to D1) | OK |
| 11 | `/OLED SDA` | **D1 = SDAin** (tied to D2) | OK |
| 12 | `/OLED SCL` | **D0 = SCL** | OK |
| 13 | `GND` | E — tied low | OK |
| 14 | `GND` | R/W# — tied low | OK |
| 15 | `GND` | D/C# = **SA0** slave-address select -> addr 0x78 | OK |
| 16 | `/OLED RST` | **RES#** | OK |
| 17 | `GND` | CS# low = permanently selected | OK |
| 18 | `GND` | **BS2 = 0** | OK |
| 19 | `+3.3V` | **BS1 = 1** | OK |
| 20 | `GND` | **BS0 = 0** | OK |
| 21 | `+3.3V` | VDDIO | OK |
| 22 | `+3.3V` | VDD | OK |
| 23 | `GND` | VSS | OK |
| 24 | `R21` 680 k -> GND | **IREF** (wants a resistor to VSS) | OK |
| 25 | `+12V` | **VCC** (second VCC pin) | OK |
| 26 | no-connect | NC | OK |
| 27, 28 | `GND` | mechanical hold-down tabs | OK |

**Score: DIRECT 26/26.**

The interface-select straps are the clincher. **Table 5.1** requires `BS0=0, BS1=1, BS2=0` for I2C. The board has `J5.20=GND (BS0=0)`, `J5.19=+3.3V (BS1=1)`, `J5.18=GND (BS2=0)`. An exact match on a three-bit code that has only a 1-in-8 chance of landing by accident, on top of a correct D2/D1 tie, a resistor on IREF and a cap on VCOMH.

### 1.4 Two previously-reported "bugs" that are RETRACTED

**H-2 — "+12 V driven onto both J5.2 and J5.25, 23 pins apart" — NOT A BUG. [RETRACTED]**
The ER-OLED018-1 genuinely has **two VCC pins, 2 and 25**, both listed verbatim as "OLED drive voltage, it should be supplied externally." Feeding both is correct. **Do not fit the R40/R41 jumpers, and do not delete either branch.** The proposed series 10 ohm / 50 mA PPTC in the common +12 V feed was justified by a short-to-VSS hazard that does not exist — VCC max is +16 V abs (p9) and the operating window is 11.5/12/12.5 V (p10), both satisfied.

**"IREF and VCOMH are 21 pads apart, so at most one is right in either direction" — FALSE PREMISE. [RETRACTED]**
The claim that "in every SSD13xx pinout IREF and VCOMH are adjacent" does not hold for this part. **VCOMH is pin 3 and IREF is pin 24** — 21 apart, exactly as the board has them. `C23` (4.7 uF) on VCOMH and `R21` (680 k) on IREF are both on the correct pins.

### 1.5 Supply rails — verified, with one thin margin [CONFIRMED]

| Rail | Board supplies | Datasheet operating (p10) | Abs max (p9) |
|---|---|---|---|
| VCC (pins 2, 25) | +12 V | 11.5 / 12 / 12.5 V | 0 to +16 V |
| VDD (pin 22) | +3.3 V | 2.4 / **3.0** / **3.5** V | -0.3 to **+4.0 V** |
| VDDIO (pin 21) | +3.3 V | 1.7 V to VDD | -0.3 to VDD+0.5 |

VCC and VDDIO are clean. **VDD at 3.3 V is legal but sits above the 3.0 V typical with only 0.2 V to the 3.5 V maximum** — so the display's VDD max is *tighter than the 3.3 V rail's own tolerance*. A buck running +5 % puts VDD at 3.47 V, essentially on the limit. Worth a decision, not a redesign: either accept it (3.3 V rails from a TPS62172 are typically +/-2 %), or drop VDD/VDDIO to ~3.0 V with a small series element. It does **not** block layout. **[NEW FINDING — flagging because the +/-5 % case has no margin.]**

**Open check, not a finding:** the datasheet asks for IREF "current around 10 uA" but the extracted text does not give the ISEG/IREF formula, so `R21 = 680 k` cannot be arithmetically confirmed from the PDF text alone. Confirm against buydisplay's reference schematic for the module. Wrong IREF affects brightness, not function or safety.

### 1.6 What still stands from the earlier drafts

The pin order is correct, but the reason it took a datasheet to prove that is unchanged and still worth fixing:

- **H-13 [CONFIRMED]** — `Conn_Zif_26Pin.kicad_mod` has **exactly one drawn item**, an `fp_rect` on F.CrtYd. No pin-1 marker, no silkscreen body, no fab outline. Orientation is unverifiable at assembly or inspection. Rebuild per the 7 items previously listed (F.Fab pin-1 triangle, silk body + "1"/"26" text, distinct pad-1 shape, **differentiate the two hold-down tabs to break x-mirror symmetry**, enlarge the courtyard — it clears the pad row by 0.045 mm against IPC-7351's 0.25 mm).
- **Record the MPNs.** J5 Value is still `Conn_01x28_Socket`, Datasheet `~`. Put **ER-CON26HT-1** in J5, and **ER-OLED018-1 / SSD1326** plus the datasheet URL in a J5-adjacent text block. Both were in the BOM the whole time and in neither the schematic nor the footprint — that gap is what made this question expensive twice.
- **M-4 [CONFIRMED]** — the generic 28-pin passive symbol makes ERC structurally blind here (`grep J5` over the ERC output = zero hits). A symbol with real names (VCC/VCOMH/IREF/BS0-2/D0..D7/RES#) and real pin types would have made this checkable by eye.
- **M-3 [CONFIRMED]** — the footprint carries a Hirose `FH12-26S` 3D model while its copper matches a TE-class land pattern. Now that the ZIF is known to be **ER-CON26HT-1**, re-verify the land pattern against that vendor drawing and attach the right model; the case files were fit-checked against the wrong body.
- **LOW-1 [CONFIRMED]** — delete `Bingbong_library.pretty/Untitled.kicad_mod`, a pad-identical clone of the ZIF footprint (shared pad UUIDs). Nothing references it.
- **0 ohm series pads on SDA/SCL/RST** remain cheap insurance and cost nothing now that you are re-laying out.
- **10 k pull-down on `/OLED RST`** so the panel is held in reset through power-up and brown-out. (The `/R1200 CE` pull-down is separate and still matters more — see C-2.)

### 1.7 Net effect on the re-layout

**J5 is unblocked. Route it as-is.** Fan-out constraints in section 5.9 are unaffected. The former "do not route J5 until the datasheet lands" gate is lifted.

---

## 2. Must-fix before layout (critical + high)

Ordered by severity, then by how much of the re-layout they block. IDs are stable for cross-reference.

| ID | Finding | Evidence | Exact fix |
|---|---|---|---|
| **C-1** | **[CONFIRMED] Charger is strapped to the USB 100 mA one-unit-load limit, so the system drains the battery while plugged in.** `PROG2=Low, SEL=Low` gives ILIMIT_USB = 80/90/100 mA *total* for system load **plus** charging. Measured demand: ESP32-S2 802.11b TX 320 mA + boost input ≈ 4.55 × I(12V) (~136 mA at a 30 mA display) + ~15 mA housekeeping ≈ 460 mA at 3.3 V ≈ 330 mA from `/SYS LOAD`. | `review_netlist.xml` net `GND` (line 2493) contains **both** `U8.3` (SEL, line 2624) and `U8.4` (PROG2, line 2625). MCP73871 DS20002090F §3.9: "A logic Low selects a one unit load input current from the USB port (100 mA) while a logic high selects a five unit load input current (500 mA)." | Route **PROG2 (U8 pin 4)** to a spare ESP32 GPIO through 0 Ω with a **100 k pull-down** (default = safe 100 mA pre-enumeration; firmware raises to 500 mA after). Free verified pins: U10 pads 4,5,6,7 (IO4-7), 8,9,10 (IO15-17), 25, 28-35 (IO34-42), all `unconnected-*` at `review_netlist.xml:2965-3013`. **Leave SEL = GND** - SEL high is AC-adapter mode (~1.8 A) and nothing on this board reads CC (R7/R8 are pure 5.1 k Rd), so >500 mA would be a USB spec violation that can trip a hub port. Also populate the DS Fig 3-1 VPCC divider (330 k IN→VPCC, 110 k VPCC→GND) at the same time. |
| **C-2** | **[CONFIRMED] The ESP32 drives the R1200 CE pin to 3.3 V while Q2 holds the R1200 VDD at 0 V - an absolute-maximum violation.** R1200 abs max: VCE = -0.3 V to **VIN + 0.3 V**. With Q2 off, VIN = 0 V, so CE's abs max is +0.3 V while IO8 presents 3.3 V. The prior review flagged this as "refutable only if CE is tolerant above VIN" - it is not. | Net `/R1200 CE` (`review_netlist.xml:2447`) = {U1.1 (CE), U10.12 (IO8)} - direct, no series R, no pull-down. `U1.3` (VDD) is on `Net-(Q2-D)`, fed only through Q2, whose gate is controlled independently by Q3 from `/R1200 PWR EN` (U10.11, IO18). | **Delete Q2, Q3, R29, R30** and use CE as the only enable. The R1200 datasheet gives standby current max 3 µA at VCE = 0 and states "at standby mode, the NPN transistor can separate the output from the input" - the external P-FET provides nothing the IC does not already do. This kills the cross-domain sneak path, frees IO18, and removes 4 parts. Add a **100 k CE-to-GND pull-down** for determinism (the internal RCE is 600/1200/2200 kΩ - enough to default off, but high-Z and noise-prone next to a 1.2 MHz Lx node). If you keep Q2, tie CE to `Net-(Q2-D)` through 100 k so CE can never exceed VDD. Note the datasheet also warns that leakage still occurs at standby when VLX ≥ VIN. |
| **C-3** | **[CONFIRMED] U7 (MIC5504 LDO) footprint is structurally broken, and the 6 resulting `shorting_items` DRC errors were suppressed rather than fixed.** Pads 1-4 are `(size 0.0508 0.0508)` - 2 mil squares - and the real lands are four **un-netted** `fp_poly` copper shapes on F.Cu. Pad 5 (thermal) is `(layers "F.Cu" "F.Mask")` only - **no paste**. F.Mask polys duplicate the copper polys exactly, i.e. **zero mask expansion**. | `TDFN1010-4LD-PL-2_MCH.kicad_mod` lines 405, 411, 417, 423 (pads); 56, 68, 80, 92 (F.Cu polys); 429 (pad 5). `bingbong.kicad_pro` `drc_exclusions` has 6 `shorting_items` clustered at (114.1-114.8, 100.2-101.3) mm = U7's placement (`bingbong.kicad_pcb`, U7 at 114.44732 100.82022 -90), plus 8 clearance, 8 solder_mask_bridge, 3 track_width at the same spot. | Rebuild from the Microchip 1×1 mm 4-lead TDFN land: four real SMD pads ≈0.4 × 0.25 mm on the existing centres, plus a real thermal pad on F.Cu/F.Mask/**F.Paste**. **Delete all eight F.Cu and F.Mask `fp_poly` graphics** - do not merely resize the 0.0508 anchors, which would leave both. *Calibration: the physical lands do exist on a fabricated board (the polys plot to gerbers), so this is not "the pads connect to nothing"; the guaranteed failures are zero mask expansion, no thermal-pad paste, and KiCad being blind to the real copper for DRC/clearance/zone purposes.* **Separately verify the pin map against the real Microchip datasheet** - the symbol declares 1=VOUT, 2=GND, 3=EN, 4=VIN (consistent with the netlist: U7.1 on +1.8 V, U7.4 on +3.3 V), but I could not read the datasheet from this project (`_mic.txt` and `_mic5504.txt` are both 0 bytes). **[SUSPECTED]** |
| **C-4** | **[CONFIRMED] No cellular antenna, no GNSS antenna and no MHF1 pigtail exist in the BOM. The only antenna line is an unpurchased 2.4 GHz Wi-Fi patch.** | BOM row 50 is the *only* antenna line: Molex 1461539150, "RF ANTENNA Bluetooth, Wi-Fi, Zigbee Flat Patch MHF1 Adhesive", Reference Designator `--`, Assembly `NO`, status **Not Purchased**, $1.55 - and it is 2.4 GHz only. Row 18 buys J3 (CONMHF1-SMD-T, "U.FL (UMCC) Connector Jack ... 50 Ohms") with nothing to plug into it. Row 35: U10 "Antenna Not Included, U.FL". Row 29: U2 "Antenna Not Included". A regex over all 988 rows for `antenna\|coax\|u.fl\|mhf\|ipex\|pigtail\|sma` returns only rows 18, 29, 33 (false hit on "LINEAR"), 35, 50. | Add three line items with real refdes **before the re-layout**, because the antenna choice drives the pi values, the keepout and the enclosure: **E1** = 2.4 GHz MHF1 flat patch with integrated cable (assign the existing Molex 1461539150 this refdes, set Assembly = YES); **E2** = a 698-960 / 1710-2200 MHz LTE-M/NB-IoT/GSM MHF1 antenna with integrated cable for J3, rated ≥2 W if EGPRS is in scope; **E3** = 1575.42 MHz L1 antenna if GNSS is kept (H-8). Record each MPN as a schematic field on J3 / J8 / U10 so it can never be lost again. |
| ~~H-1~~ | **RESOLVED - NOT A DEFECT. J5 pin order is CORRECT (26/26).** Verified against the ER-OLED018-1 datasheet section 5 / Table 5.1. Severity drops from HIGH to **INFO**; the residual item is documentation only. | See section 1.3 for the full 26-pin scoring. `bingbong.kicad_sch:15035/15044/15053/15062`; `Conn_Zif_26Pin.kicad_mod:30-55`. | **Do not change any J5 net.** Record the MPNs (ER-OLED018-1 / SSD1326 display, ER-CON26HT-1 ZIF) in the schematic, and rebuild the footprint with a pin-1 marker per H-13. **J5 routing is UNBLOCKED.** |
| ~~H-2~~ | **RETRACTED - NOT A BUG. +12 V on both J5.2 and J5.25 is CORRECT.** The ER-OLED018-1 has **two VCC pins, 2 and 25**, each specified as "OLED drive voltage, it should be supplied externally". The short-to-VSS hazard that justified this finding does not exist. | ER-OLED018-1 datasheet p6/29 (Module Interface); VCC operating window 11.5/12/12.5 V (p10), abs max 0 to +16 V (p9). `review_netlist.xml:2345`. | **No action. Do NOT fit the R40/R41 split jumpers and do NOT delete either branch.** The proposed 10 ohm / 50 mA PPTC in the common +12 V feed is also withdrawn - it would drop voltage on a rail with a 0.5 V operating window. |
| **H-3** | **[CONFIRMED] RPROG3 = 10 k sets charge termination at 100 mA, at or above the maximum achievable charge current - termination is broken.** ITERM = 75/100/125 mA for PROG3 = 10 k; IREG = 1000/RPROG1 = 100 mA for R14 = 10 k, and only 90 mA typ in the present USB strapping. With `~TE` high the 6 h safety timer is also disabled, so nothing backstops it. | `review_netlist.xml` net `Net-(U8-PROG3)` = {R15.2, U8.12 (PROG3)}; R15.1 on GND; R15 = 10 k. | **Change R15 from 10 k to 100 k** (ITERM = 10 mA typ). Rule: RPROG3 ≈ 10 × RPROG1. If you also raise charge current, keep the ratio (RPROG1 = 2 k → 500 mA, RPROG3 = 20 k → 50 mA). The datasheet-legal RPROG3 range is 5 k-100 k, so 100 k is a valid endpoint. *Calibration: termination is only evaluated in CV mode with a 1 ms filter, so the real symptom is a chronically ~80-90 % charged cell, not "no charging". This becomes the dominant defect **after** C-1 lands.* |
| **H-4** | **[CONFIRMED] USB VBUS has no TVS, no fuse, no OVP, and under-spec bypass, on a charger whose absolute maximum input is 7.0 V.** Also: CC1/CC2 - the two most ESD-exposed pins in a USB-C receptacle - carry only a 5.1 k pulldown each. | `review_netlist.xml:2334` net `+5V` = {C15.1, J2.A4, J2.A9, J2.B4, J2.B9, J6.4, U8.2 (VPCC), U8.18 (IN), U8.19 (IN__1)} - **nothing else**. U5 (TPD2EUSB30A) is on `/USB D+` and `/USB D-` only (nets 29/30; its symbol has exactly three pins). `Net-(J2-CC1)` = {J2.A5, R7.1}; `Net-(J2-CC2)` = {J2.B5, R8.2}. BOM: C15 = Murata GRM155R61A106ME11D, 10 µF **10 V** X5R **0402**, and there is no 100 nF anywhere on `+5V`. **[SUSPECTED: the 7.0 V abs-max figure is a datasheet value not readable from these files - confirm before sizing the clamp.]** | See §3.2 for the full shopping list. Minimum set: a 5 V low-capacitance TVS to GND at J2 *before* C15; an OVP/current-limit load switch; C15 → 10 µF **16-25 V in 0603/0805**; a 100 nF 0402 right at U8 pins 18/19; ESD diodes on CC1 and CC2. *Calibration: over-current on `+5V` is already bounded by U8's own input limiter (90 mA today, 450 mA after C-1), so a fuse buys protection only against a hard board short or J6 misuse. **The TVS, the 100 nF, the larger C15 and OVP against a non-compliant >7 V charger are the items that carry the weight.*** |
| **H-5** | **[CONFIRMED] CE has a 100 k pull-DOWN, so charging is disabled until firmware boots.** A bricked, unprogrammed, or flat-battery unit can never recharge, with no user-visible explanation. | `review_netlist.xml:2400` net `/CHARGE EN` = {R16.2, U10.22 (IO14), U8.17 (CE)}; R16.1 on GND (line 2557); R16 = 100 k. MCP73871 §3.16: "the charger feature is enabled when CE is active-high." | **Change R16 to a 100 k pull-UP to `/SYS LOAD`** - *not* `+3.3V`, which is generated downstream of the charger (LOW-6). Charging then works out of the box on a virgin board and firmware can only inhibit it. The datasheet warning that "allowing the CE pin to float during the charge cycle may cause system instability" is satisfied by a firm pull-up just as it was by the pull-down. |
| **H-6** | **[CONFIRMED] The 0.5 A TPS62172 runs at ~92 % of rating on peaks because the +12 V boost is fed from the 3.3 V rail, and L1 is a 500 mA multilayer decoupling part.** Boost input current = 12 × I(12V)/(0.8 × 3.3) = 4.55 × I(12V) ≈ 136 mA at a 30 mA display; total peak ≈ 460 mA against "Up to 500-mA Output Current". Double conversion at ~0.68 total efficiency. | `review_netlist.xml:2303` net `+3.3V` includes U10.2 (3V3), **Q2.2 (S, which feeds the boost)**, U7.4, U3.6, J5.19/21/22. BOM L1 = TDK **MLZ1608A2R2WTD25**, "2.2 µH Shielded **Multilayer** Inductor **500 mA** 250 mΩ 0603" - from the automotive-*decoupling* catalogue. C10/C13 are 22 µF **6.3 V 0402** on a 3.3 V rail. | (1) **Move the boost input from `+3.3V` to `/SYS LOAD`** - change Q2's source, or U1 pin 3 directly if you take the C-2 deletion. R1200 VIN range is 2.3-5.5 V, covering `/SYS LOAD`'s 3.0-5.0 V span; this removes ~136 mA from the buck and raises boost efficiency. (2) **Change L1 to 3.3 µH in a real shielded wire-wound power inductor with Isat ≥ 1.4 A** (the device high-side current limit reaches 1.35 A, i.e. 2.7× the present part's rating). Suggested: Murata DFE201610P-3R3M or TDK VLS252012HBX-3R3 **[SUGGESTION]**. (3) Move C10/C13 to **0805 10 V** so you actually get the 22 µF TI asks for. *[SUSPECTED: the 3.3 µH low-VIN recommendation and the 0.85/1.05/1.35 A current-limit figures are TI datasheet values not derivable from the repo - but a 500 mA-rated part in a 500 mA converter has no margin on its face.]* |
| **H-7** | **[CONFIRMED] Battery input `/VBAT` has no reverse-polarity protection, no fuse, and drives a polarized 470 µF through-hole electrolytic.** | `review_netlist.xml:2479` net `/VBAT` = {C1.1, C2.1, C3.1, C16.1, J4.2, U2.32/33/52/53, U8.14/15/16}; J4.1 on GND. No series FET, diode, fuse or PTC. C3 = 470 µF, `Capacitor_THT:CP_Radial_D8.0mm_P3.50mm` (`bingbong.kicad_sch:17701`), BOM Rubycon 16ZLH470MEFCT78X11.5, 8 × 11.5 mm can. **No `F*` reference designator exists anywhere in the 84-component netlist.** | *Calibration first: J4 is `JST_SH_BM02B-SRSS-TB`, a **mechanically keyed housing that cannot be mated reversed**, and the BOM specifies exactly one cell (row 48, ASR00035 500 mAh; "amazon" appears nowhere in the workbook). Reversal requires a **mis-crimped or user-made harness**, not a plugging error.* Do the cheap half first: **silkscreen `+` and `-` directly against the correct J4 pads, outside the connector body outline**, commit to one cell MPN, and drop the through-hole polarized can. Hard protection if you want it: series P-channel FET (source to J4.2, drain to the VBAT node, gate to GND through 100 k, 10 V zener gate clamp), Vds ≥ 20 V, Rds(on) < 30 mΩ so a 2 A burst costs ~60 mV - e.g. DMP2035U / Si2333DDS **[SUGGESTION]** - plus a 2 A PTC. **Do not** replace C3 with 4× 47 µF X5R: the 470 µF is sized for the BG95's ~2 A burst, and 188 µF of X5R derates to well under half at 3.7-4.2 V bias. Use a 220-470 µF **polymer** (Kemet T520 / Panasonic SP-Cap, 1210, 10-30 mΩ) if you want to lose the THT part and the vent path. |
| **H-8** | **[CONFIRMED / product decision] BG95 ANT_GNSS (pin 49) is a hard no-connect - GNSS is non-functional silicon, and you are paying $27.46 for the GNSS SKU.** | `review_netlist.xml:2794-2796` net `unconnected-(U2-ANT_GNSS-Pad49)`, single node, `pintype="input+no_connect"` - a deliberate NC flag, which is why `review_erc.rpt` has zero antenna warnings. GNSS_TXD (27) and GNSS_RXD (28) are likewise NC (`:2806-2811`). No `ANT_GNSS` net or label exists anywhere. Ordered SKU is **BG95M3LA-64-SGNS** (BOM row 29), the GNSS variant. | **Decide before the re-layout - this changes the mechanical design, not just the PCB.** IN: add J8 = second TE CONMHF1-SMD-T, route U2.49 → 3-pad pi → J8.1, add an L1 antenna line item. If the antenna is active (LNA) you need a bias tee (33-47 nH 0402 wirewound choke to +3.3 V plus a 100 nF C0G series DC block) **[SUSPECTED - I could not verify whether BG95 ANT_GNSS sources bias]**. OUT: change the SKU to the non-GNSS BG95-M3 and delete the GNSS claim from the product spec. |
| **H-9** | **[CONFIRMED] `/ANT_MAIN` is a bare 2-node net: no pi network, no DC block, no tuning pads, zero DNP RF parts.** | `review_netlist.xml:2355-2358` - net 5 `/ANT_MAIN` contains exactly two nodes: `J3 pin 1` and `U2 pin 60 ANT_MAIN`. The schematic contains **exactly one DNP part in the whole design** and it is R24 (`bingbong.kicad_sch:15241-15243`), unrelated to RF. As routed the net is 3 segments totalling 7.28 mm with nothing in between (`bingbong.kicad_pcb:35513-35538`). | Insert a **3-element pi** between U2.60 and J3.1, all 0402: series C_A, shunt C_B on the modem side, shunt C_C on the connector side. Build 1 stuffing: C_A = 15 pF C0G (also your DC block), C_B/C_C = DNP. Place within 5 mm of J3, total added trace ≤4 mm, ground pads of C_B/C_C stitched with ≥2 vias each within 0.5 mm. **This is the cheapest insurance on the board - three 0402 pads, ~$0.00 BOM cost** - and without it, correcting case/battery/hand detuning requires a respin. Tune on a VNA **with the case closed and the battery fitted**, then freeze the values. |
| **H-10** | **[CONFIRMED] The stackup is the untouched KiCad placeholder and there is no RF or USB netclass - one `Default` class at 0.2 mm covers +12 V, VBAT, USB and the antenna alike.** | `bingbong.kicad_pcb:6` `(thickness 1.6)`; `:10-12` only F.Cu and B.Cu; `:37-75` a single `dielectric 1` of `(thickness 1.51) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02)` with `(copper_finish "None")` and `(dielectric_constraints no)` - all defaults. `bingbong.kicad_pro` `net_settings.classes` has exactly one entry: `{name:"Default", track_width:0.2, clearance:0.2, diff_pair_width:0.2, diff_pair_gap:0.25}`; `netclass_patterns: []`, `netclass_assignments: null`. `review_netlist.xml:2355` confirms `/ANT_MAIN` is `class="Default"`. `bingbong.kicad_dru` has only JLCPCB minimums (track 0.127, clearance 0.127) and **zero** impedance/diff-pair/RF rules. The Default 0.20/0.25 geometry on the current stack computes to **158 Ω differential**, not 90. | See **§5** for the full copy-pasteable spec. *Calibration: "physically unroutable" (the earlier draft's wording) is **false** - 50 Ω GCPW at W = 1.229 mm is buildable on a 37.5 mm board for a 7 mm run, and the USB link is Full-Speed only (U2's USB_DP/USB_DM are NC at `review_netlist.xml:2947-2952`), so 90 Ω control is desirable, not mandatory.* **Go 4-layer for the RF trace and for a clean uninterrupted L2 reference, not because USB demands it.** |
| **H-11** | **[CONFIRMED] J6 is an unkeyed 1×05 0.1" header carrying GND / +1.8 V / +3.3 V / +5 V / +12 V on adjacent pins.** Every adjacent-pin short is rail-to-rail; a 5-pin ribbon plugged end-for-end maps pin1↔pin5 and pin2↔pin4, i.e. +12 V onto GND **and** +5 V onto +1.8 V simultaneously. Pins 4-5 bridged puts +12 V onto `+5V`, which **is** J2's VBUS - so 12 V is driven straight back out of the USB-C receptacle into the host, and into U8's ~7 V-max IN pins. | `review_netlist.xml`: J6.1 in `GND`, J6.2 in `+1.8V` (2298), J6.3 in `+3.3V` (2312), J6.4 in `+5V` (2340), J6.5 in `+12V` (2350). Footprint `Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical` (`bingbong.kicad_sch:22738`), no shroud, no key, no series element on any rail. Confirmed physically: `bingbong.kicad_pcb` J6 at (131.572, 101.8794) rot 180, pads in that order on 2.54 mm centres. | *Calibration: J6 is a bring-up/debug breakout that is **not in the BOM**, so it is unpopulated as built - a robustness gap, not a live defect.* Do the cheap correct things: **(a) put GND on both end pins** (e.g. 1×07 as GND, +12V, GND, +5V, GND, +3.3V, +1.8V) so a reversal is symmetric and every adjacent-pin short is rail-to-GND, which each regulator survives via its own current limit; **(b)** silkscreen every pin's rail name **including GND**, with a square pad + "1" numeral + polarity triangle on both F.SilkS and F.Fab (J6 pad 1 already *is* a rect while 2-5 are circles); **(c)** if J6 will ever be mated, use a keyed/shrouded housing or delete one pin position and key the plug. **Do not fit 10 Ω 0402 in the +5 V/+12 V feeds** as the earlier draft suggested - a 1/16 W 0402 dissipates its rating at 79 mA and would make the header useless for powering the board. Use 0 Ω plus keying, or a polyfuse. |
| **H-12** | **[CONFIRMED] SIM VCC has neither bypass nor ESD, and SIM detect goes bare from an exposed slot contact into ESP32 IO33.** The prior review's H7 was never applied. | `review_netlist.xml:2387` net `/BG95_VCC` = {J7.C1 (VCC), U2.43 (USIM_VDD)} and **nothing else** - no capacitor, no ESD. `:2455` net `/SIM SW` = {J7.SW, U10.24 (IO33)} and nothing else - no pull-up, no series R, no ESD. By contrast CR1/CR2/CR3 *do* sit on `/BG95_IO` (2377), `/BG95_CLK` (2372), `/BG95_RST` (2382). `U2.42 USIM_DET` is unconnected (net 130). As routed, `/BG95_VCC` is 43.60 mm over 12 segments with 2 vias, 38.66 mm of it on B.Cu. | Add **100 nF X7R 0402 + 1 µF from `/BG95_VCC` to GND within 3-5 mm of J7 pin C1**, plus a fourth ESD diode of the *ordered* part (**ESD9B5.0ST5G**, SOD-923 - not the schematic's Value string) to GND. On `/SIM SW`: **1 k series** between J7.SW and U10.24, a **10 k pull-up to +3.3 V** (do not rely on the internal pull-up for an externally exposed pin), 100 nF to GND, and an ESD diode. Optionally wire J7.SW to U2.42 USIM_DET so the modem also knows about card removal. Add DNP 0 Ω series and DNP 22 pF shunt pads on CLK/RST/DATA per Quectel's SIM reference. **The SIM slot is the only user-touchable bare metal besides USB - three of its six contacts are protected and VCC is not - and the USIM_VDD bypass is a Quectel requirement, not a nicety.** |
| **H-13** | **[CONFIRMED] The J5 footprint has no silkscreen, no pin-1 marker and no fab body - orientation is unverifiable at assembly or inspection.** | See §1.8. `Conn_Zif_26Pin.kicad_mod` - one `fp_rect` on F.CrtYd, nothing else. | Rebuild per §1.8 items 1-7, **before** placing J5, so the pin-1 marker is on screen while you place it. After placement, plot F.SilkS + F.Fab and physically confirm the "1" end points where the flex's conductor 1 will land. |
| **H-14** | **[CONFIRMED] 106 DRC violations are suppressed via `drc_exclusions`, including 6 `shorting_items`, 43 `solder_mask_bridge` and 6 `starved_thermal`.** `shorting_items` and `solder_mask_bridge` are the two rules that exist specifically to catch "this will short in the fab house", and 49 of them were switched off exactly where the shorts are. | `bingbong.kicad_pro` `board.design_settings.drc_exclusions`: 106 entries - clearance ×44, solder_mask_bridge ×43, shorting_items ×6, starved_thermal ×6, track_width ×6, hole_clearance ×1. By nearest footprint: U3 (12+12), U8 (16+16), U7 (8 clearance + 6 shorting_items + 8 mask bridge), U6 (8+7+1+3), plus C16, C23, R8 and starved_thermal near J5. By coordinate, 4 starved_thermal land on J5 signal pads 15/13/9/8 - all GND pads. | **Empty the `drc_exclusions` array before starting the re-layout.** *Calibration: exclusions are keyed to item UUIDs, so the re-layout will destroy the tracks/zones behind most of the clearance, mask-bridge, track_width and starved_thermal entries and they will go stale on their own; **the durable ones are the footprint-anchored entries, notably U7's 6 `shorting_items` (C-3), whose UUIDs survive re-placement.*** Gate gerber release on **zero DRC errors AND zero exclusions**. Give the J5 hold-down tabs and its GND pads **solid (`zone_connect 2`) zone connections** - they are mechanical, and a stressed connector on a starved thermal is a lift-off waiting to happen. |

---

## 3. Protection gaps and the parts to add

Current protection inventory, complete: **U5** (TPD2EUSB30ADRTR) on `/USB D+` and `/USB D-` only, and **CR1/CR2/CR3** (ESD9B5.0ST5G, SOD-923) on `/BG95_IO`, `/BG95_CLK`, `/BG95_RST`. **That is all of it.** There is no TVS, eFuse, OVP, PTC or fuse anywhere in the 47-line BOM, and no `F*` designator in the 84-component netlist.

### 3.1 ESD coverage per externally exposed net

| Net / contact | Exposure | Today | Add | Justification |
|---|---|---|---|---|
| `+5V` / VBUS (J2.A4/A9/B4/B9) | user-mated daily | **nothing** | 5-6 V low-cap TVS to GND within 5 mm of the pads, **before** C15 | first thing a strike meets, and the only thing between a hot-plug ring and U8's IN pins |
| `Net-(J2-CC1)`, `Net-(J2-CC2)` | recessed but fully exposed contacts | 5.1 k Rd only | **CR4/CR5 = ESD9B5.0ST5G** (already BOM row 14, SOD-923 - zero new BOM lines) or one TPD4S014 covering CC1/CC2/SBU1/SBU2 | CC is one of the two most common ESD kill paths on USB-C. A strike there has nowhere to go but across a 0.5 mm pad gap into D+/D-/VBUS |
| `/USB D+`, `/USB D-` | user-mated | U5 - **but placed 116.7 mm from J2** | **no schematic change; move U5 to ≤5 mm from J2 pads A6/A7** | 116 mm ≈ 100 nH; a 2 ns IEC 61000-4-2 edge develops kV across that before U5 conducts. Topology is already right (U5 shunt on the connector node, R17/R19 series toward the MCU) - purely a placement defect, free to fix in the re-layout |
| J7 SIM contacts C2/C3/C7 | user-serviceable slot | CR1/CR2/CR3 ✔ | - | correct already |
| J7 SIM **VCC** (C1) | same slot, same finger | **nothing** | 4th ESD9B5.0ST5G + 100 nF + 1 µF within 3 mm | a strike goes straight into U2's USIM_VDD LDO output (H-12) |
| J7 **SW** (card detect) | same slot | **nothing** | 1 k series + 10 k pull-up + 100 nF + ESD diode | terminates directly on ESP32 IO33 with **zero** impedance - one wire from the outside world to the MCU (H-12) |
| `/VBAT` (J4) | user-replaceable pack | **nothing** | see §3.4 | |
| TH1 NTC pigtail | leaves the board | **nothing** | 100 nF, plus ESD if a pigtail is used | |
| `/ANT_MAIN` (J3) | *internal* pigtail to an adhesive patch inside a sealed case | **nothing** | **optional**: sub-0.3 pF RF ESD in the pi's connector-side shunt position - Littelfuse PGB0010603 or onsemi ESD7451 **[SUGGESTION]** - or a 27-56 nH shunt wirewound for static bleed (only works with the series DC block fitted) | *Down-scoped: BOM row 50 is a "Flat Patch MHF1 **Adhesive**" antenna, so this is not externally exposed the way USB-C and the SIM are.* **Never reuse CR1-3 here** - a ~12 pF device is 6 Ω at 2.2 GHz, i.e. a short across the antenna port |
| J5 SDA/SCL/RST | *internal* display flex; service/rework only | **nothing** | **100 Ω 0402 series (or 0 Ω stuffable) on each**, at the J5 end. TVS array optional | *Down-scoped: the BOM identifies the display as an internal 1.8" module on a flex inside the enclosure.* The series resistors are load-bearing - and note a 3.3 V-rail TVS array **will not survive a +12 V pin-order fault**, so the series R plus H-2's current limit are what actually help there |
| J6 rails | bench-only, unpopulated | **nothing** | see H-11 | |
| SW1 (Cherry MX) | user presses it thousands of times | 10 k pull-down only | 1 k series + 100 nF at the MCU end; consider inverting to switch-to-GND | see M-16 |

**One BOM-consistency item that blocks all of the above [CONFIRMED]:** CR1/CR2/CR3 are valued `PESD5V0F1BLD_315` in the schematic (`review_netlist.xml:478`, footprint `Diode_SMD:D_SOD-923`) but **ordered as onsemi ESD9B5.0ST5G** (BOM row 14, "Clamp Ipp Tvs Diode Surface Mount SOD-923"). **The land is correct for the part being bought** - do *not* "fix" it by reverting the footprint to `DFN1006D-2_SOD882D_NEX`, which would mis-land the ordered part. Fix the *metadata*: set the schematic Value and Datasheet to ESD9B5.0ST5G. The ESD9B family is **bidirectional**, so orientation is a non-issue - which also means the symbol's pin-type problem (both pins `unspecified`, named literally "1" and "2") is ERC hygiene, not a live risk. Add a schematic note: *"SIM/USB ESD only - DO NOT reuse on `/ANT_MAIN`."* (A related note, "PESD BG95 <-> SIM", already exists at `bingbong.kicad_sch:10665`.)

### 3.2 USB-C over-current and over/under-voltage

Order along the VBUS path, everything within 10 mm of J2:

```
J2 VBUS pads -> TVS to GND (<=2 mm, own via into the plane)
             -> OVP + current-limit switch
             -> C15 bulk (now on the switch OUTPUT)
             -> U8 IN / VPCC
```

**No branch may tap VBUS upstream of the protection switch** - including J6's `+5V` pin, which must move to the load side.

| Function | Suggested part | Why | Status |
|---|---|---|---|
| ESD clamp on VBUS | **onsemi ESD9B5.0ST5G** as CR6 - already BOM row 14, SOD-923 | zero new BOM lines, ~$0.10 | **[SUGGESTION - reuse of a verified BOM part]** |
| Higher surge energy instead | Littelfuse **SMF5.0A** or Bourns **CDSOD323-T05C** | if you want surge margin, not just ESD | **[SUGGESTION - specs unverified]** |
| **OVP + OCP + inrush, one part (primary)** | Diodes **AP22815AWT-7** (SOT-25, ~5.7 V OVP, 2 A, soft-start, reverse-current block when off, FLAG output) | covers OVP, OCP, inrush and gives fault reporting to a GPIO; clamps below U8's 7 V abs max | **[SUGGESTION - thresholds are datasheet values I could not verify from these files]** |
| Programmable alternative | TI **TPS2596ARDPR** (adjustable OVP + adjustable ILIM + slew) | if you want to set the knee yourself | **[SUGGESTION - unverified]** |
| Combined OVP + USB ESD | TI **TPD1S514DBVR** (SOT-23-6, 5.5 V OVP + current limit + integrated D+/D- ESD) | would let you delete U5 entirely | **[SUGGESTION - unverified]** |
| Discrete backstop | 0.5 A hold PTC (0805L050YR) at the 500 mA setting, or 1.1 A (1206L110WR) if you raise charge current | 0.5-1 Ω series and a slow trip - a backstop, not a substitute for the switch | **[SUGGESTION - ratings unverified]** |
| VBUS bulk | change C15 to **10 µF 16 V or 25 V X5R in 0603/0805** (e.g. Murata GRM188R61E106MA73D) | a 10 µF/10 V 0402 X5R at 5 V bias loses well over half its value, so the MCP73871's 4.7 µF minimum is not demonstrably met. Keep total VBUS bypass ≤10 µF for USB compliance | **[CONFIRMED gap; part is a SUGGESTION]** |
| VBUS HF bypass | **100 nF 0402 X7R at U8 pins 18/19** | none exists on `+5V` today | **[CONFIRMED gap]** |

**Under-voltage on the input:** U8's **VPCC is tied directly to IN** (`review_netlist.xml:2334` includes U8.2 alongside U8.18/19), which the datasheet names as the way to *disable* input-voltage foldback. That is a legitimate configuration choice at 90 mA. **The moment you apply C-1 and go to 500 mA it stops being safe**, because the charger will hold 500 mA into a weak wall-wart or a long cable and pull VBUS down until the source folds back or resets - and that oscillation (droop → UVLO → restart → droop) browns out the ESP32 and BG95 from the shared `/SYS LOAD`. Populate the Fig 3-1 divider: 330 k from `+5V` to a new VPCC node, 110 k to GND (or size for your own knee: VPCC = 1.23 V = R2/(R1+R2) × VIN_min; 100 k / 40.2 k gives 4.3 V). Add 100 nF VPCC-to-GND. Lay it out so it can be depopulated back to a 0 Ω short. **[CONFIRMED topology; the 1.23 V reference is a datasheet value]**

**Firmware is blind to all of it [CONFIRMED].** `Net-(D2-K)` = {D2.1, U8.6 (PG)}, `Net-(D3-K)` = {D3.1, U8.8 (STAT1/LBO)}, `Net-(D4-K)` = {D4.1, U8.7 (STAT2)} - anodes go only to R11/R12/R13 (1 k) from +3.3 V. No ESP32 pin appears on any of them, and `+5V` touches no GPIO and no divider. **That blocks the USB-compliant current negotiation that C-1's fix depends on**, blocks safe shutdown on low battery, blocks any charge UI, and removes the software layer that would catch a hardware fault. All three status pins are open-drain: add 100 k pull-ups to +3.3 V and route each to a free GPIO through 0 Ω (keep the LEDs in parallel - the pins sink both). Add a VBUS-present divider: 100 k/100 k from **post-switch** VBUS to a spare GPIO (2.5 V at 5 V VBUS, safely inside the ESP32-S2 range) plus 100 nF for debounce. **Do not use IO45** (strapping, VDD_SPI voltage select) or IO46 (input-only) - use IO4-IO7, IO17 or IO34-IO38.

### 3.3 Battery UVLO / deep-discharge

**[CONFIRMED]** There is no undervoltage lockout, no battery voltage sense and no low-battery cutoff. `/VBAT` has only caps, J4.2, U2's VBAT pins and U8's VBAT/VBAT_SENSE - **no divider to any ADC**. Both BG95 ADC pins are dead (`unconnected-(U2-ADC0-Pad24)`, `unconnected-(U2-ADC1-Pad2)`). U6's EN is tied to U6's VIN on `/SYS LOAD`, so the buck free-runs.

**The correct sensor is already on the board and is wired to an LED.** You bought the **-2CC** option specifically because it has a **3.1 V LBO** (spec 2.95/3.1/3.25 V, 150 mV hysteresis, active only on battery), and U8 pin 8 goes only to `Net-(D3-K)` → D3 → R12 → +3.3 V.

| Fix | Cost |
|---|---|
| **(1) 100 k pull-up on U8.8 (STAT1/LBO) to +3.3 V, routed to a free ESP32 input.** LBO is open-drain and auto-disabled on USB - exactly the behaviour you want. Firmware gets a hard 3.1 V interrupt and can command the BG95 off and blank the display. | one resistor |
| **(2) VBAT sense divider:** 2 × 1 M from `/VBAT` to an ADC1-capable pin (IO3-IO7), 100 nF to GND, gated by a small N-FET so it draws nothing when idle. Gives absolute voltage, not just "below 3.1 V". | 4 parts |
| **(3) A firmware-independent backstop:** a TPS3839/TLV840-class supervisor on `/SYS LOAD` driving U6's EN, or a latching load switch. **Do not build the UVLO from a divider onto U6 EN directly** - VEN_H spans 0.3-0.9 V across the datasheet limits, far too loose for a battery cutoff. | one part |

*Calibration: the ASR00035-class 500 mAh pack ships with an integrated PCM whose over-discharge cutoff (~2.4-3.0 V) is the current last-ditch protection, so the honest statement is "no telemetry and no firmware-independent cutoff, so the cell is routinely taken down to the pack PCM trip" - a real design improvement, not an imminent fire.* Route the LBO and VBAT-sense traces away from the L1 and L2 switching nodes; both are high-impedance and will pick up 1.2 MHz / 2.25 MHz noise.

**Related, LOW-6 [CONFIRMED]:** `~TE` is strapped from `+3.3V` (`review_netlist.xml:2332`), a rail generated *downstream* of the charger by U6, whose input is U8's own OUT. Electrically safe (abs max is VDD+0.3 V) but topologically wrong and indeterminate through power-up - it is 0 V (timer enabled) while +3.3 V ramps, then 1 (timer disabled) once the buck starts, and it drops back any time the rail glitches. The datasheet explicitly sanctions disabling the timer "when the system load is substantially limiting the available supply current", so this is a choice - just make it a deliberate one. Once C-1 lands, either tie `~TE` to **GND** to re-enable the 6 h safety timer (500 mA charges a 500 mAh cell in well under an hour, so 6 h is a comfortable fault backstop) or strap it from `/SYS LOAD` / `+5V` through 100 k. **Apply the same "strap from an upstream rail" rule to the H-5 CE pull-up.**

### 3.4 Reverse polarity and accidental shorts to ground

| Path | Status | Action |
|---|---|---|
| J4 battery | keyed housing, cannot be mated reversed; **one** cell MPN in the BOM. The risk is a mis-crimped harness | silkscreen `+`/`-` against the pads (outside the body outline so it reads with the harness mated), asymmetric silk outline, one committed cell MPN, escape traces on the same layer so a solder bridge is visually obvious. Series P-FET if you want hard protection (H-7) |
| C3 470 µF polarized THT | hand-inserted; can be fitted backwards independently of the harness | move to polymer/SMT bulk, or use a footprint with a filled-half silk polarity band plus `+` on **both** F.SilkS and F.Fab and a square anode pad. Do not place it where the marking is hidden by the connector or the case |
| C22 / C23 25 V molded tantalum in `Capacitor_SMD:C_1206_3216Metric` | **[CONFIRMED]** a symmetric MLCC land - no polarity band, no chamfer, no silk. The part fits either way, and a reversed tantalum on a 12 V rail is a low-impedance short that gets hot | *Calibration: 25 V on a 12 V rail is correct 50 % tantalum derating and the 6 Ω ESR is fine (helpful, even) for boost-output damping - the **only** defect is the missing polarity indication.* Either change the footprint to `Capacitor_Tantalum_SMD:CP_EIA-3216-18_Kemet-A` (anode stripe) or add a `+` and a pin-1 chamfer to the silk. Note C23 is **not** on +12 V - it is on `Net-(J5-Pin_3)`, whose working voltage is set by the panel |
| J6 rails | H-11 | GND on both end pins; label every pin |
| SW1 through-hole pads on B.Cu | switches `+3.3V` into a GPIO; setting the board on a conductive surface shorts the rail | see M-16 |
| J5 flex path | nothing under the flex is keep-out; a component under a bare conductor sheet can abrade through the polyimide | add a Rule Area keep-out along the flex path (§5.9 item 5) |

---

## 4. Dummy-proofing changes for the re-layout

The changes that make the *next* mistake impossible rather than merely unlikely. Ordered by leverage.

**4.1 Connectors and keying**
- **Buy a reversible-contact ZIF family (§1.7 Option 3).** Highest-leverage item in this report, and it costs nothing at design time: it converts "scrap the boards and respin" into "solder the other connector". Confirm the top- and bottom-contact variants share the same land **and** the same body height/footprint before finalising the case cutout.
- **Preserve the J4 (JST SH 1.00 mm) vs TH1 (JST PH 2.00 mm) family split.** Different families at different pitches physically cannot be cross-plugged - that is real, already-present dummy-proofing. Do not "simplify" both to one connector. Place them beyond a cable's reach of each other so a technician cannot even attempt it. Both are keyed, so neither can be inserted backwards in its own housing. **[CONFIRMED]**
- **J6:** GND on both end pins, per-pin rail labels including GND, keyed/shrouded housing if it will ever be mated (H-11).
- **Pin-1 markers on F.Fab for every connector**, so the assembly drawing carries orientation even when silk is obscured by the case.

**4.2 Silkscreen and fab layer**
- J5: pin-1 triangle, body outline, actuator swing outline, "1"/"26" end text, flex-insertion arrow, physically asymmetric hold-down tabs (§1.8).
- A **board-level silk legend beside J5**: `PIN1 <-- CONTACTS DOWN` (or up - whatever §1.5 settles), plus the display MPN.
- `+` and `-` on both silk layers next to every polarized part (C3, C22, C23), placed where they stay readable with connectors mated.
- J6: every pin's rail name **and** voltage. In the existing layout the labels are ambiguous - the "12V" text at y = 93.193 is 0.56-1.33 mm from the pad *one position up* the row and 1.21-1.98 mm from the pad it names, and the label spacing (3.00 / 2.85 / 2.28 mm) does not match the 2.54 mm pad pitch; there is no GND label at all. **Put each label's centre within 1.0 mm of its own pad and ≥1.5 mm from the neighbour, or run the labels perpendicular to the header.** Verify in the gerber viewer before release. **[SUSPECTED - the geometry is exact but intent cannot be resolved from it alone]**
- `DNP` / `NP` silk next to R24 with "R24 = NO-NTC OPTION", plus the schematic note *"Populate R24 ONLY when TH1 is unpopulated"* (M-12). Place R24 visibly apart from the populated passives, not tucked under the connector.

**4.3 Series resistors and default-state pulls (stuffable escape hatches)**
- 0402 **0 Ω stuffable** in SDA / SCL / RST at J5 - blue-wire points if a residual pin-order error appears at bring-up. Later populate at 100 Ω.
- **R4 = 0 Ω → 100 Ω** on `/EN`. S1 currently discharges C29 (1 µF) + C17 (0.1 µF) straight through the switch contacts, and 0 Ω gives no ESD/mis-probe limiting on the ESP32's reset pin. 100 Ω + 1 µF = 100 µs, still invisible to a human press. *(The earlier draft claimed the `/EN` cap is 100 nF and quoted 10 µs - it is C29 = 1 µF, so the RC is 100 µs. Accept 100 µs, or drop C29 to 100 nF for 10 µs.)*
- **R5 = 0 Ω → 1 k** on `/BOOT`, plus an external **10 k pull-up to +3.3 V** on U10 pin 27. Today boot mode depends entirely on the chip's internal 45-80 k pull-up charging C18 = 100 nF. The margin is real (EN's RC ≈ 11 ms vs IO0's ≈ 4.5 ms, so the strapping level is valid at CHIP_PU release) but it is not guaranteed by anything you control. **[CONFIRMED as a robustness gap, not a bug]**
- **10 k pull-downs on IO45 (U10 pin 26) and IO46 (U10 pin 16)** - both ESP32-S2 strapping pins, currently floating on weak internal pull-downs, on a handheld with a cellular PA nearby. Keep them within 5 mm of the module pads.
- **100 k pull-down on `/R1200 CE`** and **10 k pull-down on `/OLED RST`** (§1.7). Today the only thing preventing 12 V at reset is R30 (10 k to +3.3 V) holding Q2 off - a single point of failure.
- **10 k pull-up from U3 `~OE` to VCCA (+1.8 V)** instead of the hard tie to GND, so the level shifter defaults Hi-Z; optionally drive `~OE` low from a spare GPIO after firmware enables the 1.8 V rail (M-13).
- **10 k base-emitter pull-down on Q3** - `Net-(Q3-B)` currently has only R29 and the base, so it floats through 1 k to an ESP32 pin that is Hi-Z during reset. *(Moot if you take the C-2 deletion.)*
- **10 k pull-up on `/ESP32 RX` to +3.3 V**, so the UART receiver sees an idle-mark level instead of a floating input during the window when U3's VCCA is off.
- Put **explicit no-connect flags on the 13 GPIOs that actually need them** - IO3, IO4, IO5, IO6, IO7, IO17, IO34, IO35, IO36, IO37, IO38, IO45, IO46 (exactly the 13 `pin_not_connected` errors in `review_erc.rpt`). IO15, IO16 and IO39-IO42 appear as unconnected nets but already carry NC flags - do not touch them.

**4.4 Test points and isolation jumpers**
**[CONFIRMED]** The 84-component netlist contains **no `TP*` designators at all**. `bingbong.kicad_pcb` has exactly one `TestPoint` footprint (`TestPoint:TestPoint_Plated_Hole_D2.0mm` beginning at line 6523, at (136.512, 164.1938), pad 1 on net GND) and its Reference is still `REF**` - it does not exist in the schematic. There is **no series 0 Ω between any regulator output and its load**: `+1.8V` goes straight from U7.1, `+3.3V` straight from U6.6 (VOS), `+12V` straight from U1.2.

- Add real schematic-symbol test points so they netlist and get DRC'd: **TP_VBAT, TP_SYSLOAD, TP_5V, TP_3V3, TP_1V8, TP_12V**, plus **≥3 TP_GND** spread across the board. Use 1.0-1.5 mm plated pads or 1.5 mm exposed SMD pads, not 2 mm holes.
- Add **TP on `/BOOT`, `/EN`, `/ESP32 TX`, `/ESP32 RX`, `/BG95 TOGGLE POWER`** so bring-up does not require probing 0402 pads.
- Add a **0 Ω 0805 jumper in series with each of +1.8 V, +3.3 V and +12 V at the regulator output, with a test point on both sides** - lift the jumper and clip a meter across to measure that rail's current, or feed it from a bench supply to isolate a fault. Without this you cannot measure the boost's standby current or separate the modem's draw from the MCU's. **Adding these now is nearly free; adding them after a spin costs a spin.**
- Cluster the rail test points along one board edge **in rail order** with silk labels, so a tech walks them left to right with one probe. A GND test point within 15 mm of every signal test point.
- Document the (correct) behaviour that **the board runs from USB with no cell installed**: VBUS → U8 IN → power path → `/SYS LOAD` → U6 → `+3.3V`. Topologically verified.
- **Optional but high-value:** a DNP edge-launch SMA (`Bingbong_library.pretty/TE_CONSMA001-SMD-G.kicad_mod` already exists in your library and is instantiated nowhere - a case-insensitive grep for `sma|CONSMA` over `review_netlist.xml` returns nothing) fed from the pi's connector-side node through a DNP 0 Ω, with a second 0 Ω selecting J3. Populate the SMA path on two bring-up boards. MHF1 connectors are rated for roughly 30 mating cycles **[SUSPECTED]**; a tuning session plus cert testing will exceed that. Two 0402 pads turn the antenna from an unmeasurable subsystem into a measurable one. Keep neither branch's unterminated stub longer than 2 mm.

**4.5 Mounting and retention**
**[CONFIRMED]** There are **zero** MountingHole footprints and only 3 `np_thru_hole` pads (all SW1's Cherry MX alignment posts) on a 120 × 37.5 mm board carrying a USB-C receptacle, an MHF1 coax, a battery pigtail and a display flex. Every insertion force on J2 and every tug on the flex is reacted by solder joints. No `H*`/`MH*` designators exist among the 84 components.

*Calibration: the project ships its own enclosure CAD (`bingbong_case_1/2.SLDPRT`, `helical_pcb_stand.SLDPRT`, `bingbong_pcb_shape.3MF`) and the BOM has no screws or standoffs, which strongly suggests a deliberately screwless captured-board design - confirm intent before adding holes. The chassis-ground/ESD-bleed rationale is also moot for an all-plastic case.* Regardless, **add at least two GND-connected pads/holes, one within 8 mm of J2 and one within 8 mm of J5**, to take connector insertion force and to give you a scope ground and a coax-shield bond point. 3 mm no-route keepout around each, ≥4 vias into the GND zones, placed **before** routing.

**4.6 Process gates**
- Empty `drc_exclusions` (H-14). Gate gerber release on **zero errors and zero exclusions**.
- **Fix ERC before pushing the netlist to the new layout (M-19).** Of the 43 messages, the genuinely real ones are **1 `multiple_net_names`** (a stray local label `3V3` at (90.17, 154.94) merged into `+3.3V` - `review_erc.rpt:120-123`) and **13 `pin_not_connected`**. The other 29 are symbol pin-type defects: 13 "Power output and Power output" caused by GND pins on **U10, U7 and U1** being declared `power_out` (**U6's grounds are already `power_in` - do not change them**; U6.1 PGND, U6.4 AGND and U6.9 EPAD all carry `pintype="power_in"`), 1 "Output and Output" for U8 pins 1/20 which are the same physical OUT node, 6 `power_pin_not_driven` (missing PWR_FLAGs on +1.8 V, +5 V, +12 V, /VBAT), 6 "Unspecified" warnings for CR1-3, and 2 Bidirectional-vs-Power-output for U8 EP and U6 FB, both legitimately on GND (**U6.5 FB tied to GND is correct for the fixed-output TPS6217x variant** - genuine noise). Target: **ERC clean before layout starts**, so a genuinely new error is visible.
- **Regenerate the BOM from the current schematic before ordering anything.** The BOM is dated 2026-03-16 and predates the 2026-06-06 schematic: it still orders **C19 and C20** (row 6 designators "C1, C4, C5, C7, C17, C18, C19"; row 10 "C10, C13, C20") which do not exist in the netlist - **rebuilding from this BOM would re-introduce the D+ loading caps that the prior review correctly killed.** It also gives **C6/C21 as 100 pF** (Kemet C0603C101K5RACAUTO7411) where the schematic says **0.1 µF** - a 1000× discrepancy on the +3.3 V rail's bypass, right where the ESP32 module and the level shifter need it. Plus CR1-3 (§3.1), Q2 (LOW-8), and SW1 (`SW_Push` vs a Gateron KS-9Y10B060NW-G43). **These lines are marked "Ordered".** Also replace the schematic text "Choose decoupling caps" (`bingbong.kicad_sch:10622`) with the actual per-IC decoupling plan, and delete the C19/C20 BOM entries. **[CONFIRMED - the cheapest single action in this report]**

---

## 5. Layout constraints (the re-layout spec)

Copy-pasteable. Numbers are computed, with the model stated so you can re-derive them.

### 5.1 Stackup - the decision everything else hangs off

**Current [CONFIRMED]:** `bingbong.kicad_pcb:6` `(thickness 1.6)`; only `F.Cu`/`B.Cu`; one `dielectric 1` of `(thickness 1.51) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02)`, `(copper_finish "None")`, `(dielectric_constraints no)`. Untouched KiCad defaults, 35 µm (1 oz) copper.

Computed on that stack (Hammerstad-Jensen, t = 35 µm):

| Target | Geometry required on the CURRENT 2-layer 1.51 mm stack |
|---|---|
| 50 Ω microstrip | **W = 2.80 mm** (W=2.50 → 53.3 Ω; W=3.00 → 48.0 Ω) - 7.5 % of the 37.5 mm board width |
| 50 Ω grounded CPW, 0.20 mm gap | **W = 1.229 mm** (buildable, but coarse) |
| 90 Ω differential | **W = 1.087 mm/trace, gap 0.15 mm** (pair pitch 1.24 mm) |
| The `Default` class as configured (0.20 / 0.25) | **158 Ω differential** |

**Recommendation: go 4-layer, 1.6 mm, signal / GND / PWR / signal, and enter a NAMED fab stackup.**

Reference: **JLCPCB JLC04161H-7628** - L1-L2 prepreg 0.2104 mm, core 1.065 mm, L3-L4 prepreg 0.2104 mm, 1 oz outer.

| Target | Geometry on JLC04161H-7628 |
|---|---|
| **50 Ω GCPW, L1 ref L2** | **W 0.38 mm / gap 0.20 mm** (50.0 Ω at Er 4.4; 51.2 Ω at Er 4.05) |
| 50 Ω plain microstrip, L1 ref L2 | W 0.367 mm (Er 4.4) / 0.392 mm (Er 4.05) |
| **90 Ω differential microstrip, L1 ref L2** | **W 0.27 mm / gap 0.15 mm** (89.6 Ω at Er 4.4) |

Useful consequence: the antenna trace is **already routed at 0.40 mm**, so 4 layers makes the existing geometry almost correct as-is.

Also set `(dielectric_constraints yes)` and set the finish to **ENIG** (`copper_finish` is currently `"None"`). ENIG is effectively mandatory for the 0.5 mm-pitch USB-C, the 0.5 mm FFC and the U.FL pad - if the fab defaults to HASL, the uneven solder domes on 0.298 mm-wide pads at 0.5 mm pitch cause coplanarity problems and bridging on exactly the connectors this review is about, and the same applies to U8 (QFN 4×4) and U3 (UQFN 1.8×1.4). *(Note: KiCad's `copper_finish` and `dielectric_constraints` fields are documentation only - they are **not** exported to gerbers and no fab reads them. **Impedance control and a TDR coupon are ordered by ticking the option on the fab's order form and putting the spec in the fab-drawing notes** - you could do that today with this exact file set. Fill the stackup block anyway so the intent lives in the design data.)*

**If 4 layers is truly off the table**, the only 2-layer alternative that gets 50 Ω at a sane width is a **0.5 mm core**: 50 Ω GCPW = W 0.719 mm / gap 0.20 mm. That board will flex in a handheld.

**Layer assignment on the 4-layer stack:**
- **L1** signal + RF. RF on L1 only.
- **L2 = solid GND. No signals, no splits, no slots** - especially not under U2, J3, the USB pair, U6+L1, U1+L2, or the J4-C3-U2 VBAT path. This is also the cellular antenna's counterpoise.
- **L3** power.
- **L4** signal.

### 5.2 Net classes to create in KiCad, BEFORE routing

Assign by **pattern**. **Two traps:** there is **no `/ANT_GNSS` net** (U2.49 is an unconnected pin), and the battery net is **`/VBAT`**, not `+VBAT` (`review_netlist.xml:2479`). Wrong names match nothing, silently.

| Class | Nets (exact) | Track width | Clearance | Notes |
|---|---|---|---|---|
| `RF_50` | `/ANT_MAIN` | **0.38 mm** | **0.20 mm exact** | no vias allowed on the net; gap set by the **rule**, not by the zone clearance |
| `USB_90` | `/USB D+`, `/USB D-` | **0.27 mm** | gap **0.15 mm** | diff pair; one consistent width end to end |
| `BATT` | `/VBAT`, `/SYS LOAD` | **≥0.8 mm** | 0.25 mm | carries the BG95 bursts |
| `PWR` | `+5V`, `+3.3V` | **≥0.5 mm** | 0.25 mm | |
| `HV` | `+12V` | **≥0.3 mm** | **0.4 mm** | *(0.2 mm already far exceeds IPC-2221 for 12 V on a coated outer layer - the 0.4 mm is for accidental-short margin next to the I2C escapes, not for creepage)* |
| `Default` | everything else | 0.2 mm | 0.2 mm | |

Matching `bingbong.kicad_dru` rules so DRC actually enforces them (the .dru currently has **zero** impedance, diff-pair or RF rules):

```
(rule "Battery path width"
  (condition "A.NetClass == 'BATT'")
  (constraint track_width (min 0.8mm)))

(rule "Power path width"
  (condition "A.NetClass == 'PWR'")
  (constraint track_width (min 0.5mm)))

(rule "HV clearance"
  (condition "A.NetClass == 'HV' || B.NetClass == 'HV'")
  (constraint clearance (min 0.4mm)))

(rule "RF coplanar gap"
  (condition "A.NetClass == 'RF_50'")
  (constraint clearance (min 0.20mm) (max 0.20mm)))

(rule "12V away from display I2C"
  (condition "A.NetClass == 'HV' && (B.Net == '/OLED SDA' || B.Net == '/OLED SCL' || B.Net == '/OLED RST')")
  (constraint clearance (min 0.5mm)))
```

Fab-drawing note:

> 50 Ω ±10 % single-ended, L1 GCPW referenced to L2, W 0.38 / gap 0.20. 90 Ω ±10 % differential, L1 ref L2, W 0.27 / gap 0.15. Stackup JLC04161H-7628 or fab equivalent. Surface finish ENIG. Fab may adjust widths to hit target on their actual stack - **report the values used.** Supply a TDR coupon.

### 5.3 Buck (U6 + L1) hot loop

- **C8 (CIN) must form the smallest possible loop with U6 pin 2 (VIN) and pin 1 (PGND)** - same side, within 2 mm, ground pad tied straight to the EPAD copper.
- Keep the **SW node (U6 pin 7 → L1) copper area minimal.**
- **Route VOS (pin 6) as a thin sense trace from the far/load side of the output capacitors**, never from the SW node.
- **Stitch the EPAD with ≥4 vias** (0.3 mm pad / 0.15 mm drill, tented on the bottom side).
- Fix `SON50P200X200X80-9N.kicad_mod`: pads named **`9_1`/`9_2`** (lines 258-272, `thru_hole circle (at 0 ∓0.55) (size 0.4 0.4) (drill 0.2) (layers "*.Cu")`) do not string-match symbol pin **`9`**, so KiCad gives them **no net** - verified in the placed footprint, where pads 1-9 all carry nets but `9_1`/`9_2` are net = NONE. Two un-netted plated holes sit inside the pad-9 GND thermal land, unstitched to anything, tented on both sides so the intended thermal-via function is lost, and positioned under the EP where they can wick paste through the barrel. **Minimal fix: rename both pads to `9`** (KiCad merges duplicate pad numbers into one node). Cleaner: delete them and place real GND vias in the layout. **[CONFIRMED]**
- Reserve a solid ground patch on the reference layer directly under U6 and L1.

### 5.4 Boost (U1 + L2)

- Keep the **`Net-(U1-Lx)` node (U1 pin 4 → L2) copper as small as practical** - it swings 0→12 V at 1.2 MHz.
- **C24 as close as possible to U1 pins 3 and 5** (datasheet wording). **C25 within 2 mm of pins 2 and 5**, so the loop U1.VOUT → C25 → GND → U1.GND is minimal. On a 2-layer board reserve a bottom-side ground patch directly under U1 for that return.
- **Route VFB (U1 pin 6) short, away from Lx and away from the +12 V run to J5.**
- Component changes while you are here: **C25 → 25 V** (currently 1 µF **16 V** 0603 on a 12 V rail; Table 3 asks for a 25 V part - or fit 2.2-4.7 µF 25 V 0805 for DC-bias margin), and **C26 → 22 pF** (currently **220 pF**, ten times Table 3's value; 220 pF moves the R3/C3 feedback pole from ~3.6 MHz down to ~360 kHz, inside the crossover region of a 1.2 MHz converter - the network exists to trim VFB noise and mis-sizing it can make that worse). **Do not "fix" C24** - it is 1 µF and the datasheet asks for "1 µF or more". **[CONFIRMED]**
- **L2 margin [CONFIRMED, medium]:** L2 = TDK MLZ2012P220WT000, a 22 µH **220 mA / 1.25 Ω multilayer decoupling** part (`Net-(Q2-D)` → L2.1, L2.2 → `Net-(U1-Lx)` → U1.4). The R1200's own peak formula ILmax = 1.25·IOUT·VOUT/VIN + 0.5·VIN·(VOUT-VIN)/(L·VOUT·fosc) at VIN 3.3 V, VOUT 12 V, L 22 µH, f 1.2 MHz gives **ILmax = 4.545·IOUT + 45 mA**, so 220 mA of rating is consumed at only **38 mA** of display VCC current, with zero margin. The 1.25 Ω DCR also drops 0.19 V and burns 28 mW at ~150 mA input. *Calibration: the datasheet's own Table 2 recommends 22 µH parts rated 185-330 mA - one of them **below** L2's 220 mA - so "3× underrated vs the 700 mA switch limit" is **not** the vendor's rule, and "saturates on every start-up" is unsupported (tstart soft-start is 1.5 ms typ). The governing constraint is the ILmax formula.* **Action: pull the ER-OLED018-1 VCC current spec, re-run ILmax, and fit a 10 µH / ~500 mA-class wire-wound part such as the datasheet's own VLS252010-100.**

### 5.5 RF (U2.60 → pi → J3.1)

- **RF trace on L1 only. Zero vias on the RF net. Constant width end to end. 45° or arcs, no 90° corners. Coplanar gap held at exactly 0.20 mm** through the pi pads and into the U.FL pad.
- **The gap must come from the `RF_50` netclass rule, not from the GND zone's clearance parameter.** Today both zones use `(clearance 0.5)` (`bingbong.kicad_pcb:36819` F.Cu, `:39320` B.Cu) and the trace is 0.40 mm over 3 segments - so the antenna's impedance is a *side effect of a zone setting*, and any future zone edit silently changes it with no DRC warning. **As routed it is nowhere near 50 Ω.** *(A precise figure is model-dependent: read as GCPW with a 0.5 mm gap it is ~91 Ω, as plain microstrip ~113 Ω - a ~25 % swing on an assumption. The mechanism is the finding, not the number, and you are discarding this layout anyway.)*
- **Via fence both sides, pitch ≤2.0 mm** (λg/20 at 2.2 GHz is 4.1 mm on the 4-layer stack; use 2 mm for margin), via edge 0.20-0.30 mm outside the coplanar gap, running the whole U2.60 → J3.1 path. Plus a **ring of ≥6 vias around J3**, and a **via pair within 1.0 mm of U2 pads 59 and 61** (which flank ANT_MAIN pad 60). Current state: of 162 vias on the board, 13 lie within 10 mm of the RF polyline and 11 are GND, but **none flank the trace** - the nearest is 2.18 mm off-axis at (127.9652, 136.2964), then 2.70, 3.79, 4.15, 4.50 mm and so on. **[CONFIRMED]**
- Respect the existing keepout in `TE_CONMHF1-SMD-T.kicad_mod` (no vias inside the -0.95..0.95 × -1.0..1.0 mm body rect) - stitch outside it. J3 GND pads 2/3/4 and U2 pads 59/61: **`zone_connect 2` (solid, no thermal relief), ≥4 vias per pad.**
- **Taper** the 0.38 mm trace out to pad width over ~0.5 mm at each end rather than butting it into a 1.00 mm pad, holding the 0.20 mm gap right up to the taper. Launch impedances computed on the 4-layer stack: J3 pad 1 (1.00 × 1.05 mm at (0,-1.525), GND pads 2/3 at (∓1.475,0), 0.45 mm gap) ≈ **27 Ω**; U2 pad 60 (0.70 × 1.10 mm, flanked at 1.10 mm pitch, 0.40 mm gap) ≈ **35 Ω**. *(The J3 figure is a worst case - pad 1 spans y −2.05..−1.00 while GND pads 2/3 span −1.10..+1.10, so the 0.45 mm "coplanar gap" exists over only ~0.1 mm of overlap.)* Each launch is ~1 mm long so the dip is electrically short, but two abrupt steps plus a via-starved ground is exactly what produces the mysterious return-loss dip that eats a day of tuning. **[CONFIRMED]**
- **Do NOT void L2 under J3.1 or U2.60.** The earlier draft (`SCHEMATIC_REVIEW_2026-09-03.predraft.bak`, line 328) claimed those pads add "~0.4-0.5 pF shunt each, ~150 Ω across the line at 2.2 GHz". **That was an overestimate and is retracted.** Recomputed on the 4-layer stack (h = 0.2104 mm, Er 4.4): J3 pad 1 gives C = εrε0A/h = 0.194 pF against 0.125 pF for an equal length of 50 Ω line, so the **excess is 0.070 pF** → y = ωCZ0 = 0.048, |Γ| = y/(2+y) = 0.024 at 2.2 GHz = **−32.4 dB return loss, VSWR 1.05**. U2 pad 60: 0.143 pF vs 0.131 pF, excess 0.012 pF → **−47.6 dB, VSWR 1.01**. Voiding the reference plane costs ground integrity for an improvement you will never measure. **Spend the effort on the taper and the via fence instead - they are worth ~10× more return loss.** **[CONFIRMED by re-derivation]**
- **3 mm all-layer RF exclusion corridor** around the whole U2.60 → pi → J3.1 path, L2 GND reference excepted. Today `+5V` (38.54 mm long) passes 2.69 mm away, `/EN` (66.76 mm) 3.04 mm away, `/CHARGE EN` (72.84 mm) 3.40 mm away, and a `+1.8V` B.Cu track 2.68 mm away **on the reference layer**. With h = 1.51 mm the return current of a 0.40 mm microstrip spreads ~±3h = ±4.5 mm, so all four sit inside the RF return region. **`/EN` is the ESP32 reset** (U10 pin 3, `review_netlist.xml:2409`). A 67 mm trace 3 mm from a +33 dBm EGPRS burst at a 217 Hz frame rate rectifies at the EN input - symptom: *"the MCU reboots whenever the modem attaches to the network"*, which is extremely hard to debug after the fact. Route those three on L3/L4 well away, and harden `/EN` per §4.3. **[CONFIRMED]**
- Move U6/L1/U8 to the opposite end from J3 (today U6 is 17.0 mm from J3, L1 15.5 mm, U8 22.1 mm; target ≥25 mm). Any rail that must pass near RF gets a local pi filter (ferrite + 100 nF + 10 µF).

### 5.6 Antenna counterpoise, keepout and coexistence

- **[CONFIRMED]** Board is 37.50 × 120.00 mm (Edge.Cuts bbox x 101.51..139.01, y 46.69..166.69). λ/4 = **113.1 mm at 663 MHz** (NB-IoT B71 UL), **107.4 mm at 698 MHz** (B12/B85 UL), **91.0 mm at 824 MHz** (GSM850 UL). The 120 mm long axis is 0.279 λ at 698 MHz; the 37.5 mm short axis is only **0.087 λ**. Forcing the cellular element onto a long edge typically costs **6-10 dB of total radiated efficiency at low band** - the difference between registering on NB-IoT indoors and not. **No pi-network tuning recovers a missing counterpoise.**
- Both short edges are occupied: U10's body top edge is 3.65 mm from the top board edge (module at (120.0928, 59.9368), 18.01 × 19.20 mm F.Fab body); J2 is on/over the bottom edge at (120.262, 166.813) with J4 beside it at (112.141, 163.271). *Calibration: the intended part is an **off-board adhesive flat patch on an MHF1 pigtail**, so the element mounts on the case wall, not a board edge - this is an enclosure + ground-plane-continuity constraint, not a board-blocking defect.*
- **The ground pour must be contiguous over the full long axis with no slots.** That is the counterpoise. Wi-Fi tolerates the 37.5 mm dimension (λ/4 = 30.6 mm at 2.45 GHz); cellular does not. If you do reserve a board-edge strip, take a full-width strip at one **short** end.
- **Extend the GND pour to 0.3 mm from the board outline on all layers** - the `.dru` already permits it, and the current 2.5 mm inset throws away ~4.4 mm of plane width for nothing.
- **Antenna element keepout:** no copper on **any** layer, no pour, no vias, no components, no metal in the case. **The exact dimensions must come from the chosen antenna vendor's drawing - make that a required deliverable before routing.** Planning figure: ≥10 × 40 mm.
- Keep **J4 (battery), TH1, C3, L2 and the metal Cherry MX SW1** (at (123.063, 142.621), B.Cu) **≥15 mm** from the element - all conductive/lossy.
- **Wi-Fi and cellular elements ≥61 mm apart** (λ/2 at 2.45 GHz), i.e. opposite ends of the 120 mm axis, which the board length just permits. In a case this small geometry buys only 10-15 dB of isolation, so maximise it. Coordinate in firmware too: do not run a Wi-Fi scan during a cellular attach or an EGPRS burst. **[SUSPECTED on the desense magnitude - the +33 dBm and −97 dBm figures are generic datasheet values, not derivable from these files; BOM row 29 lists bands only and says nothing about transmit power]**
- **If GNSS is added (H-8):** J8 **≥25 mm from J3** (λ/8 at 1575 MHz), and the GNSS element needs its own **≥47.6 mm** (λ/4) counterpoise dimension - which the 37.5 mm short axis does not reach.
- **U10's antenna is entirely on-module** - the symbol has 49 pins and **no RF/ANT pin of any kind** (pin 1 GND, 2 3V3, 3 EN, 4-39 IO, 40-49 GND), and the footprint is the 18.01 mm **-2U** body (the PCB-antenna SOLO-2 is 25.5 mm long) with no zone or keepout. **No board RF trace and no ground keepout under U10 are required.** *Write this down in a schematic note* or the next person will add a phantom antenna trace or forget the plug clearance. Suggested note: *"Antenna: on-module MHF1/IPEX. Mates E1 (2.4 GHz MHF1 flat patch w/ integrated cable). No board RF trace, no ground keepout under the module."* Reserve the plug escape - planning figures ≥6 mm vertical and ≥8 mm lateral above U10 for the MHF1 plug and coax bend (the module is already 3.2 mm tall) - **and verify against the enclosure CAD, which I could not read (binary .SLDPRT/.3MF).** Keep C3, J6 and SW1 out of that path and route the two pigtails separately inside the case. **[CONFIRMED for the electrical half; NEEDS USER INPUT for the mechanical half]**
- Record the target bands, VSWR spec (≤2.5:1 typical), impedance target and antenna MPN as a schematic text note plus fields on J3. **The only band information anywhere in the project is a distributor description in BOM row 29 - "850MHz, 900MHz, 1.8GHz, 1.9GHz" - which lists only the GSM/EGPRS bands, not the LTE-M/NB-IoT list.** The lowest supported band sets the counterpoise length and therefore the enclosure: **getting this wrong is a mechanical respin, not a PCB respin.** **[CONFIRMED that nothing is recorded; SUSPECTED on the band list itself]**

### 5.7 USB pair and J2

*(Full-Speed only - U2's USB_DP/USB_DM are NC at `review_netlist.xml:2947-2952`, and D+/D- pass through 0 Ω R17/R19 to the ESP32-S2's native USB on IO20/IO19. 90 Ω is desirable, not mandatory.)*

- Coupled pair for the entire length, **W 0.27 / gap 0.15** on the 4-layer stack.
- **Total length ≤100 mm** (hard max 150). Today: `/USB D+` = 143.1 mm over 16 segments, `/USB D-` = 165.1 mm over 30 segments - **22.0 mm of intra-pair mismatch**, mixed 0.1/0.2 mm widths, asymmetric via counts (2 vs 4).
- **Intra-pair match ≤2.5 mm.** One consistent width. **Zero vias preferred, max one symmetric pair** with both traces transitioning at the same point and a GND stitch via within 1 mm of each.
- Unbroken GND reference directly beneath the whole run: no splits, no slots, no plane cutouts.
- ≥3W clearance to every other net; **≥2 mm from the U6 SW node / L1 and the U1 Lx node / L2; ≥5 mm from any RF trace or the antenna keepout.** Do not route under J5, U2 or the boost inductor.
- **Place U5 within 5 mm of J2 pads A6/A7, on the connector side of R17/R19**, with U5 pin 3 (GND) taken to the plane by **two vias within 0.5 mm of the pad, no thermal reliefs**. R17/R19 immediately downstream. No copper stub >2 mm anywhere on the pair. Consider changing R17/R19 from 0 Ω to a small series R so they actually contribute isolation.
- **J2 fan-out:** the A6/B6 and A7/B7 crossovers are unavoidable (A6 at local x = −0.5, B6 at +0.25). Do the crossover in the 1.30 mm channel between the pad rows on F.Cu if possible; if a via drop is needed, keep both vias symmetric, outside the coupled section, with a GND stitch via within 1 mm of each. Keep the footprint's built-in keepout zone (local −3.5,−5.65 to 3.5,0) - it sits behind the B row and does not obstruct the fan-out.
- **Zero copper on the 10 unused exposed pads** - A2, A3, A8, A10, A11, B2, B3, B8, B10, B11 - beyond the pad outline: no track, no via, no teardrop, no fill connection. **Do not tie them to GND** (that breaks the mating impedance and gains nothing). Keep the GND pour ≥0.2 mm clear. *(Already satisfied in the existing layout - carry it forward.)* **[CONFIRMED]**
- **VBUS ≥0.4-0.6 mm** (or a pour) from J2 through the protection element to U8 IN, with plane directly under the whole path and ≥2 × 0.3 mm vias per transition. Today `+5V` is 41 segments **all at 0.2 mm**, 84.8 mm total, 5 vias - about 0.73 A at a 10 °C rise per IPC-2221, and ~200 mΩ, i.e. ~100 mV of IR drop at 500 mA right at the input of a charger whose UVLO you care about. `bingbong.kicad_dru` enforces only 0.127 mm, so DRC will not catch it. **[CONFIRMED]**
- **J2 shell (SH1-SH4) is hard-tied to GND, and that is the correct default** for a plastic-cased handheld - the shell is the first thing an ESD strike contacts and a low-inductance path to the plane is what keeps that energy out of the signals (a 1 M ‖ 4.7 nF network puts ~30 Ω in that path at ESD frequencies, which is worse). The cost is a galvanic loop through the cable shield to the host - which matters more than usual here because a cellular TX, a GNSS RX and a Wi-Fi radio share that plane, and cable-borne common-mode current is a classic GNSS-desense and radiated-emissions path. **Make it swappable:** put the four SH pads on a small local copper island tied to the main plane through a single **0 Ω 0805 (populated)** with parallel **DNP 1 M and DNP 4.7 nF 0603** footprints. Shell posts get ≥0.9 mm pads on 0.6 mm drills, solid GND pour on both layers with **no thermal reliefs**, and ≥6 stitching vias clustered within 3 mm **at ONE point**, positioned so shell ESD current flows *away* from the ESP32 and the BG95, never under them. No signal may route through the shell island. *(Verified: no 1 M resistor and no 4.7 nF capacitor exists anywhere in the netlist or the 47 BOM lines today.)* **[CONFIRMED]**

### 5.8 Ground strategy

**Good news, and worth stating because the brief asked [CONFIRMED]:** there is **exactly one ground net** - `GND`, `review_netlist.xml:2493`. No AGND/PGND/GNDA/DGND/VSSA nets exist; those strings appear only as pin *functions* (U6 pin 1 PGND, U6 pin 4 AGND, U8 pins 10/11 VSS, U2 pin 47 USIM_GND), all nodes on the same net. All shields are grounded: J2 SH1-SH4, J7 GND8/GND9, J3 pins 2/3/4, and J5's mechanical tabs 27/28. Both PCB zones are GND, with 105 GND vias. **There are no split grounds to stitch, no AGND/PGND loops from a mis-drawn separation, and no floating shields.** Keep it that way - the connector shells and ZIF tabs being bonded is exactly right for ESD.

- Achieve separation by **placement**, not by splitting the pour.
- **Do not let any routing cut the return path** under the BG95, under the U6 buck loop, under the U1 boost loop, or under the J5 flex.
- Stitch the GND zones with vias **every 5 mm around the perimeter and every 2 mm along the RF trace.**
- **≥9 × 0.3 mm thermal vias under U8's EP** with ≥200 mm² of connected copper - at 500 mA input U8 dissipates roughly (5.0 − 3.7) × 0.45 ≈ **0.6 W** - **≥4 under U6's EP**, **≥2 on each J5 hold-down tab**, all on GND, all `zone_connect 2` (solid). Route `+5V`/IN and OUT at ≥0.5 mm on 1 oz.
- Keep the charge-current return (U8 VSS/EP → J4 pin 1) and the modem burst return **off the copper that references the ESP32 module and its antenna feed.**
- Route `/VBAT` from J4 to U2 pins 32/33/52/53 as a **wide low-impedance pour (≥1.5 mm equivalent)** with the return directly beneath; target **<50 mΩ round trip** on 1 oz so a 2 A burst causes <100 mV of droop. Put the bulk in the burst path between J4 and the VBAT pins, not off to one side, and keep C1/C2/C16 within 2-3 mm of the module's VBAT pads. **Kelvin-route U8 pin 16 (VBAT_SENSE) as a separate thin trace to the battery-side pad** rather than tapping it off the fat VBAT trace at the IC - the netlist merges them into one net, so this is routing discipline that DRC will not enforce.

### 5.9 J5 fan-out (do this FIRST, before the pour)

**Nothing can pass between adjacent J5 pads under your own DRU. [CONFIRMED]** Pads are 0.3 mm wide on 0.5 mm pitch, leaving a **0.2 mm** gap; `bingbong.kicad_dru` sets track spacing and track-to-pad clearance at 0.127 mm, so a 0.127 mm track centred in that gap leaves 0.0365 mm per side - a 3.5× violation. The smallest legal via is 0.35 mm OD (0.2 mm hole + 0.075 mm annular ring), which does not fit either. *(This is true of every 0.5 mm FFC land on any 0.127 mm process - it is a fan-out procedure, not a defect in this board.)*

Correct breakdown of the 26 signal pads: **13 GND** (pads 4,5,6,7,8,9,13,14,15,17,18,20,23) + **11 signal** (2,3,10,11,12,16,19,21,22,24,25) + **2 NC** (1,26), plus the two mechanical tabs. Only 11 real escapes - the fan-out is easy if you do it first.

1. Route J5 **first**, as **26 parallel straight escapes** perpendicular to the pad row, one per 0.5 mm channel, for **at least 1.5 mm** before any of them turns.
2. Fan out beyond that. **Place all vias beyond the fan-out region, never between pads.**
3. Define a **copper Rule Area over the pad row extended 1.0 mm each side with "keep out zone fills" enabled**, so the GND pour cannot generate slivers between 0.5 mm pitch pads (they bridge in reflow).
4. On 4 layers, drop the 13 GND pads to the plane with vias placed **beyond** the fan-out.
5. Add a **Rule Area keep-out extending 8-12 mm in the flex insertion direction** with "keep out footprints" set, so nothing tall ends up under the flex. The flex is a bare conductor sheet lying on the board; anything under it can abrade through the polyimide - a real short-to-ground path.
6. Verify against `bingbong_case_1.SLDPRT` / `bingbong_case_2.SLDPRT` that the flex bend radius is achievable without pinching (min ~10× thickness, so ~1.5 mm for a 0.15 mm FFC, more for a display tail).
7. Route the two +12 V branches on the **opposite side of the connector from the I2C traces**, and give +12 V the 0.4 mm `HV` clearance so a short between a 12 V trace and an I2C trace requires a gross defect, not a whisker. *(Note the current pinout already puts 4.0-4.5 mm and a block of GND pins between +12 V and the nearest I2C pin - that part is reasonably defensive.)*
8. Add local decoupling **immediately behind the pad row**: 0.1 µF 0402 on +12 V within 3 mm of the J5 +12 V pad, and a 0.1 µF + 1 µF pair on +3.3 V within 3 mm of J5.19/21/22. Keep C22 (4.7 µF 1206) within ~5 mm. The existing +12 V caps (C22, C25, C26) all sit at U1, centimetres away, feeding a panel whose current steps with display content.
9. Place C23 (VCOMH) and R21 (IREF) **within 3 mm of their final J5 pads** with a direct short return to the same GND stitch via. VCOMH is a high-impedance analog node - do not run SDA/SCL/RST or the +12 V switching node across it.
10. **Do NOT add charge-pump capacitors to J5.** The absence of C1P/C1N/C2P/C2N/VBAT is *correct* for an externally-supplied-VCC 26-pin variant - +12 V is generated on-board by U1 and every `+12V` node is on the main board. Record this so nobody "fixes" it later. **[SUSPECTED on the family reasoning; CONFIRMED that +12 V is board-generated]**

---

## 6. Medium / low / cleanup

**MEDIUM**

- **M-1 RESOLVED - NOT A DEFECT.** IREF (R21, 680 k, J5.24) and VCOMH (C23, 4.7 uF, J5.3) are on the **correct pins**. The ER-OLED018-1 pinout genuinely places VCOMH at pin 3 and IREF at pin 24 - 21 apart, exactly as built. The "family always places them adjacent" rule was an inference and is false for this part. The value check also passes: (12-2.5)/12.5 uA = 760 k, so 680 k is in band for a 12 V VCC. **No action.** Confirm R21 against buydisplay's reference schematic only if display brightness is off.
- **M-2 [CONFIRMED] The BG95 hangs directly on the raw cell instead of the charger's OUT power path.** `/VBAT` (`:2479`) carries U2.32/33 (VBAT_BB) and U2.52/53 (VBAT_RF) alongside U8.14/15/16 - not `/SYS LOAD`. Consequences: the charger measures modem current as battery current so CV current never falls to ITERM; with a dead/absent cell the modem has no supply; every TX burst discharges the cell even on USB. **Do NOT "fix" this by moving the modem to `/SYS LOAD`** - that puts a 2 A burst through the MCP73871's pass FET (200 mΩ typ), dropping ~400 mV before the modem's own decoupling and taking VBAT_RF below the module minimum, and OUT is additionally input-current-limited (90 mA now, 450 mA after C-1, 1650 mA only in AC mode). **Powering the module directly from the cell is standard Quectel practice for exactly this reason.** Instead: **tie `~TE` low to re-enable the 6 h safety timer, or add a firmware charge timeout, and add a schematic note documenting the deliberate split.**
- **M-3** ZIF 3D model contradicts the copper - §1.8.
- **M-4** Generic J5 symbol blinds ERC - §1.8.
- **M-5 [CONFIRMED] J5 courtyard covers neither the housing, the actuator swing, nor the flex** - §1.8 item 6 and §5.9 item 5. An undersized courtyard is a silent invitation for pcbnew to let you drop a 1206 under the connector housing with no DRC error.
- **M-6 [CONFIRMED] `+1.8V` is generated locally and is not sequenced with the modem.** `+1.8V` = {C11.1, C4.1, J6.2, R2.1, U3.10 (DIR1), U3.7 (VCCA), U7.1} - from U7, enabled by IO13 via `/MIC EN`. `U2.29 (VDD_EXT)`, the module's own 1.8 V IO reference output, is **unconnected**. `U3.2 (~OE)` is hard-tied to GND so the translator is permanently enabled. R2 (100 k) pulls U2.17 (~RESET) up to this same local rail. The ESP32 can therefore turn on U7 while the BG95 is off, biasing the modem's RXD and RESET pins through its ESD structures with its IO domain unpowered - which Quectel's hardware design guide prohibits. **The specific back-power path is A2 → U2 MAIN_RXD**: U3.10 (DIR1) is tied high so A1 is an *input*, while U3.1 (DIR2) is tied to GND (line 2611) so B2 (pin 4, `/ESP32 TX`) *drives* A2 (pin 9, `/BG95 RX`) into U2.34. **Fix: derive VCCA from the modem** - connect U2.29 (VDD_EXT) to U3.7, U3.10 and R2 with 1 µF + 100 nF, and delete U7 (freeing IO13). VDD_EXT is 0 V when the modem is off, the AVC2T245's VCC-isolation puts the A port Hi-Z, and nothing can back-power the module. Respect Quectel's VDD_EXT current limit (typically 50 mA). Also **connect U2.20 (STATUS)**, currently unconnected - the PWRKEY toggle via Q1 is otherwise completely open-loop and a hung modem on the raw cell has no recovery path.
- **M-7 [CONFIRMED] Decoupling gaps.** Per-pin audit: `/BG95_VCC` = {J7.C1, U2.43} has **zero capacitors** (the one genuine requirement gap - Quectel requires local bypass at the SIM connector, and it doubles as the ESD/EMI mitigation on an externally exposed contact; without it the SIM browns out during ATR and card init is intermittent, which looks like a bad SIM or bad provisioning); **C2 is 1 µF 6.3 V on a 4.2 V node** (the second genuine gap). Prioritise those two. Nice-to-have but *not* datasheet violations: 100 nF at U8 pins 18/19, at U6 pin 2, at U1 pins 2 and 3 (the R1200 asks only for "1 µF or more" on VIN and "1 µF-4.7 µF or more" on VOUT, both present; the MCP73871 asks for a 4.7 µF *bulk* minimum). Bias derating worth fixing at the same time: C15 → 10 µF 16 V 0805, C10/C13 → 22 µF 10 V 0805, C8 → 10 µF 10 V 0603. For U10, put a 10 µF + 100 nF within 3 mm of module pin 2 (3V3) and feed it with ≥0.5 mm of copper or a pour.
- **M-8 [CONFIRMED] No battery telemetry / no firmware-independent low-voltage cutoff** - §3.3.
- **M-9 [CONFIRMED] Firmware is blind to VBUS presence and charger status** - §3.2. Same change as M-8's LBO item; treat them as one.
- **M-10 [CONFIRMED] J2's solder-mask openings are hand-drawn `F.Mask` polygons instead of pad mask layers, producing 75 µm mask dams.** All 24 SMD pads in `MOLEX_1054500101.kicad_mod` omit `F.Mask` (pads start line 564, `(layers "F.Cu" "F.Paste")`, e.g. pad "A1" line 567); the openings are 24 `fp_poly` on `F.Mask` starting line 53, each pad size + 0.0635 mm per side (0.425 × 0.827 over the 0.298 × 0.7 signal pads), giving **0.075 mm dams** between all adjacent openings in both rows. Same in the placed instance (`bingbong.kicad_pcb:13726`, F.Mask polys from 13845). J2 is the **only** footprint of 91 with SMD pads lacking F.Mask. Three problems: (a) 0.075 mm is below almost every fab's minimum mask bridge (JLCPCB 0.1 mm, PCBWay 0.09-0.1 mm advanced), so the fab silently deletes them and each 12-pad row becomes one open window at 0.5 mm pitch - removing the bridging barrier exactly where it matters; (b) KiCad's mask-bridge DRC does not run on pads with no mask layer, so `(allow_soldermask_bridges_in_footprints no)` is silently bypassed on the one connector where bridging is most likely; (c) the mask no longer tracks the pads, so any pad edit desynchronises it and a future "update footprints from library" can break it. **Fix: change all 24 to `(layers "F.Cu" "F.Mask" "F.Paste")` and delete the 24 F.Mask polys.** With the project's `(pad_to_mask_clearance 0)` (`bingbong.kicad_pcb:76`) that yields **0.202 mm dams**. Then re-run Update Footprints from Library. *(The openings do exist in the shipped gerbers, so past boards were fabbable - this is about margin and DRC coverage, not a dead board. Alternative one-liner: switch to KiCad's stock `Connector_USB:USB_C_Receptacle_Molex_105450-0101`, but it names all four shell pads "S1" while your symbol uses SH1-SH4, so you would renumber the symbol first.)*
- **M-11 [CONFIRMED] U6's `9_1`/`9_2` thermal-via pads get no net** - §5.3.
- **M-12 [CONFIRMED, downgraded] THERM / R24.** With R24 DNP and the NTC unfitted, THERM floats, the internal 50 µA source drives it above the 1.24 V "too cold" threshold, and **charging is suspended forever with no indication** - the board looks completely dead on the charger. *Calibration: the schematic already documents the intent - R24's Description (`review_netlist.xml:1252`) reads "Optional MCP73871 THERM bypass resistor; populate only when no battery NTC is installed" - and the BOM buys the NTC (a leaded THT disc, KYOCERA AVX ND03N00103K, that solders straight into TH1's 2.00 mm THT land, so no JST housing or crimps are actually required) and does **not** buy R24. The shipping configuration is self-consistent.* **Residual action: silkscreen "DNP"/"NP" next to R24, a fab note, and the schematic note "Populate R24 ONLY when TH1 is unpopulated."** The 10 k ‖ 10 k = 5.00 kΩ hot-trip trap (exactly the 0.25 V threshold) requires ignoring an existing note - make it impossible to hit.
- **M-13 [CONFIRMED] U3 `~OE` hard-tied to GND**, against TI's explicit "Keep OE high until VCCA and VCCB are powered up", with a **guaranteed** violation window every power-on because VCCA (+1.8 V) is firmware-gated via IO13/R10 while VCCB (+3.3 V) comes up with the buck. Symptoms: current injection into the unpowered 1.8 V domain, unpredictable BG95 MAIN_RXD state during boot, possible latch-up on the A side. Fix per §4.3. *(Robustness/back-feed during the pre-firmware window, not a steady-state failure, and the contending drive strength at VCCA = 0 V is small.)*
- **M-14 [SUSPECTED] Battery undersized for EGPRS bursts.** 2 A from a 500 mAh cell is 4C; cell ESR of 150-300 mΩ alone drops 0.3-0.6 V per burst and many 500 mAh PCMs trip around 2-3 A. Symptom: the modem resets on every registration attempt, blamed on firmware. **Confirm the intended radio mode.** If EGPRS/2G is ever used, move to a cell with a documented ≥3 A pulse rating (103450-class, 1500-2000 mAh) or disable 2G and stay on LTE-M/NB-IoT (~500-600 mA peak, 1.2C, workable). Get the PCM's overcurrent trip in writing from the cell vendor. *(Ignore any advice to "delete the Amazon battery alternates" - there is exactly one battery line in the workbook.)*
- **M-15 [CONFIRMED] C3 is a through-hole 470 µF can on an otherwise all-SMT keychain-sized board.** ~0.1-0.3 Ω ESR **[estimate, not read from the Rubycon datasheet]** is far too high to actually buffer a 577 µs / 2 A burst - it looks like burst support on paper but is not. It also makes every hot-plug of a charged cell into a discharged 470 µF a multi-amp arc across a 1 A-rated JST SH, pitting the contacts on every insertion; it forces a hand-solder operation and an 8 × 11.5 mm keep-out; and it is the part that vents on reversal. **Replace with a 220-470 µF polymer (Kemet T520 / Panasonic SP-Cap, 1210, 10-30 mΩ) placed between J4 and U2's VBAT pins**, in the burst current path. Re-check inrush against the pack PCM.
- **M-16 [CONFIRMED] SW1 switches +3.3 V into a GPIO and is the only switch on the board that is not switch-to-ground.** `+3.3V` includes SW1.1; `/BTN` = {R18.2 (10 k to GND), SW1.2, U10.23 (IO21)} - no series R, no cap, no TVS. S1 and S2 both correctly switch to ground (their pins 2/4 are on GND). *The real hazard is firmware: if IO21 is ever configured as an output driving low, pressing SW1 shorts +3.3 V into the GPIO.* **Fix: invert to match S1/S2** - SW1.1 to GND, SW1.2 to `/BTN`, R18 becomes a 10 k pull-up (or DNP, using the internal pull-up) - then add **1 k series** and **100 nF at the MCU end** for debounce, ESD absorption and current limiting, for about 0.4 cents. SW1's THT pads sit exposed on B.Cu, so also add a mask keepout and a non-conductive standoff, or move to an SMD keyswitch.
- **M-17 [CONFIRMED] Netclass/track-width gap on the current-carrying rails** - covered by §5.2. The load-bearing part is **width** for `/VBAT`, `/SYS LOAD` and `+5V` (0.2 mm is the default for newly routed tracks, and at 1 oz it is good for ~0.8-1.0 A at a 20 °C rise, about half the modem's burst) plus the absence of any controlled-impedance class. *(The "+12 V needs HV clearance" framing is overstated - 0.2 mm already far exceeds IPC-2221 for 12 V on a coated outer layer.)*
- **M-18 [CONFIRMED] BOM ↔ schematic mismatches** - §4.6.
- **M-19 [CONFIRMED] ERC triage** - §4.6.
- **M-20 [CONFIRMED] D1 pulls the BG95's NET_STATUS pin up to +3.3 V through R3 = 1 k.** `Net-(D1-K)` = {D1.1 (cathode), U2.21}; `Net-(D1-A)` = {D1.2, R3.1}; R3.2 → +3.3 V. Whenever +3.3 V is present and the BG95 is off - the normal state during ESP32 boot and any firmware modem power-down - roughly (3.3 − Vf − Vclamp)/1 k ≈ 0.5-1 mA flows into an unpowered pin, forward-biasing the module's ESD structure. The connection is also **inverting**, so the blink patterns read backwards. **Cheapest correct fix: move R3's top end from `+3.3V` to `U2.29 (VDD_EXT)`** so the pull-up rail dies with the modem. Full fix is Quectel's transistor-buffer reference circuit (4.7 k into an NPN base - you already stock SS8050 for Q3 - 47 k base pulldown, emitter to GND, collector to the LED cathode, anode through 2.2 k to `/VBAT`), which also fixes the inversion. **[SUSPECTED on the Quectel figure values and the "1.8 V power domain" attribution - not reproducible from these files]**
- **M-21 [SUSPECTED] J4 (JST SH, ~1 A/contact) feeds a modem that can draw ~2 A in GSM bursts.** EGPRS bursts are ~577 µs at 1/8 duty, so RMS through the contact is roughly **0.7 A against a 1 A rating** - marginal rather than clearly over, which is why this needs your band/power-class answer (M-14) rather than an automatic connector swap. If you do swap, JST PH (2.0 mm, ~2 A) also standardises with TH1. Either way, ensure enough local bulk right at U2's VBAT pins that the burst is supplied locally rather than pulled through the connector.

**LOW**

- **LOW-1** Delete `Bingbong_library.pretty/Untitled.kicad_mod` - §1.8.
- **LOW-2 [CONFIRMED]** VBUS/CC ESD absent - §3.1. Cheap: CR4/CR5/CR6 = ESD9B5.0ST5G, zero new BOM lines, ~$0.30. Leave SBU1/SBU2 unclamped **and** completely unrouted (§5.7).
- **LOW-3 [CONFIRMED]** U5 placed 116.7 mm from J2 (U5 at (130.8878, 50.5868), J2 at (120.262, 166.813); routed net lengths 143.1 / 165.1 mm) - §3.1. Pure placement, free to fix.
- **LOW-4 [CONFIRMED]** VBUS routed at 0.2 mm over 84.8 mm - §5.7.
- **LOW-5 [CONFIRMED]** C15 rating and placement: 10 µF **10 V** 0402 X5R, 11.3 mm from J2 (C15 at (126.327, 157.331)), adding ~10 nH of loop inductance, with no series resistance, ferrite or soft-start anywhere on `+5V`. At 5 V bias it retains a fraction of its marked value. **Move to 16-25 V in 0603/0805 and place it within 5 mm of J2's VBUS pads** - or on the OVP switch's output, with a smaller 0.1 µF on the switch input. *(Hot-plug ringing on a 5 V-only port is not a credible threat to a 10 V part - DC-bias derating is the real issue.)*
- **LOW-6 [CONFIRMED]** `~TE` strapped from a downstream rail - §3.3.
- **LOW-7 [CONFIRMED]** VPCC tied to IN - §3.2. A deliberate, datasheet-sanctioned configuration today; becomes wrong after C-1.
- **LOW-8 [CONFIRMED]** Q2 is `FDN340P` in the schematic and `FDN338P` in the BOM. **Both are P-channel** - the BOM's own description reads "P-Channel 20 V 1.6A (Ta) 500mW (Ta) Surface Mount SOT-23-3" - so this is **metadata only, not a channel-polarity bug**. Gate drive is Vgs = −3.2 V (Q3 saturates to ~0.1 V against a +3.3 V source), which is thin for the FDN340P's threshold spread and comfortable for the logic-level FDN338P. **Pick one MPN, make schematic and BOM agree, and sanity-check −1.6 A against the boost input current.** *Moot if you take the C-2 deletion.*
- **LOW-9 [CONFIRMED]** CR1-3 schematic Value vs BOM MPN - §3.1. Documentation only; the land is correct for the ordered part. Also rename the symbol pins to K/A (or IO/GND) and set them `passive`, and record the bidirectionality in the Description.
- **LOW-10 [CONFIRMED]** No capacitor carries a voltage rating in the schematic/netlist - all 25 have bare capacitance values. The ratings **do** exist in the BOM, so this is a documentation gap: ERC/BOM tooling cannot check them. Add a Voltage property or put the rating in the Value field. *The only genuinely marginal part is **C25 at 16 V on a 12 V rail** (1.33× derating) - §5.4. Do not "re-check DC bias on C22/C23": they are molded tantalum (T491), which has negligible bias derating.*
- **LOW-11 [CONFIRMED]** R4/R5 = 0 Ω between the user buttons and EN/IO0 - §4.3. Debounce already exists (C29 1 µF + C17 0.1 µF on `/EN`, C18 0.1 µF on `/BOOT`); what is missing is ESD/mis-probe current limiting. *(0 Ω 0402 jumpers in a switch path are a common deliberate placeholder - R17/R19 use the same part on the USB lines.)*
- **LOW-12 [CONFIRMED]** No external pull-up on `/BOOT` - §4.3. Cheap noise margin, not a bug: EN's RC (~11 ms) is more than twice IO0's (~4.5 ms), so the strapping level is valid at CHIP_PU release. IO46 is unconnected and sits at its internal-pulldown default of 0, so **GPIO0 is the only thing keeping the part out of joint-download boot** - which is why an external pull-up is worth the 0.2 cents.
- **LOW-13 [SUSPECTED, downgraded]** R22/R23 = 10 k I2C pull-ups. tr ≈ 0.847·R·Cb, so 10 k hits the 1 µs standard-mode limit at 118 pF and the 300 ns fast-mode limit at 35 pF, while a 30-50 mm 26-conductor FFC plus the display's input capacitance plus the ZIF will exceed 100 pF - 400 kHz would be impossible and 100 kHz marginal, with a symptom of intermittent display corruption that varies with cable routing. **But inspect the ER-OLED018-1 module first - if it already has pull-ups, dropping to 2.2 k gives needlessly high combined sink current.** The free wins are: **record the FFC length in the schematic**, and reserve DNP 33-100 Ω series pads at the ESP32 end. Keep J5 pins 9 and 13 as GND returns adjacent to SDA/SCL on the flex - that is already right.
- **LOW-14 [CONFIRMED]** D2/D3/D4 have no colour or MPN in the schematic Value field (D1 = "RED LED", D2/D3/D4 = "LED"), so the assembler picks. The colours *are* specified in the BOM (D1, D3 red 630 nm; D2, D4 green 573 nm). 1 k from 3.3 V through a ~2.0 V green LED gives ~1.3 mA - dim but not invisible. **Put the MPN and colour in the Value/MPN fields, and drop R11 and R13 to 470-680 Ω** (R13 drives D4/green and R11 drives D2/green; R12 drives D3/red and can stay). The MCP73871 STAT/PG outputs are open-drain rated to 25 mA, so there is plenty of headroom. Polarity is already correct - KiCad's `Device:LED` and `LED_0603_1608Metric` agree on pin 1 = K, pin 2 = A.
- **LOW-15 [SUSPECTED]** J3's MHF1 pads 1 and 4 are geometrically identical, mirrored and unmarked (both 1.0 × 1.05 mm at (0, ∓1.525)), the symbol's pins are all named `~`, and there is no pin-1 marker anywhere - so nothing distinguishes them. If TE numbers them the other way, `/ANT_MAIN` lands on a ground tab and the antenna is **dead-shorted to ground with no DRC/ERC warning** - the ZIF failure mode in a different package. **There is no evidence in the project that it is wrong**, and the BOM confirms the ordered part (TE/Linx CONMHF1-SMD-T, "U.FL (UMCC) Connector Jack, Male Pin 50 Ohms") with a working datasheet URL - **settle it in one click.** Then add an F.SilkS pin-1 triangle at the signal pad, F.Fab "RF"/"GND" text, and a distinct pad shape so a 180° mis-rotation is visible.
- **LOW-16 [SUSPECTED]** J6 silk labels ambiguous - §4.2.
- **LOW-17 [SUSPECTED]** U5's custom `SOTFL35P100X50-3N` land disagrees with KiCad's official `Texas_DRT-3` for the same package: pad 1 (−0.52,−0.35), pad 2 (−0.52,+0.35), pad 3 (+0.52,0), all 0.46 × 0.20 mm, vs the official (−0.35,+0.425), (+0.35,+0.425), (0,−0.425), all 0.30 × 0.30 mm. Same topology and 0.70 mm pitch after a 90° rotation, but across-package pad centres are **1.04 mm vs 0.85 mm** and the pad dimension in the pitch direction is **0.20 mm vs 0.30 mm**. On a 1.0 × 0.6 mm package that is the difference between a reliable joint and an open or a tombstone. **Pin numbering is confirmed correct** (custom symbol 1=D+, 2=D−, 3=GND matches KiCad's official `Power_Protection:TPD2EUSB30` exactly), so the failure mode would be solderability, not a wrong connection. **Cross-check against TI's DRT0003A drawing (link in BOM row 31), or just swap U5's footprint to the stock `Package_TO_SOT_SMD:Texas_DRT-3` - a drop-in with no schematic edit.** Note BOM row 31 lists the package as "3-SMD, SOT-23-3", a DigiKey description artefact; the real package is TI DRT (SON-3, 1.0 × 0.6 mm) - confirm you are ordering the right body.
- **LOW-18 [CONFIRMED]** U1 has no MPN in the schematic (Value = `~`, Datasheet/Description/Footprint properties empty in `Bingbong_library.kicad_sym`), even though the BOM records it as **Nisshinbo R1200N002A-TR-FE** (adjustable boost, 700 mA switch, SOT-23-6). **Copy the MPN and datasheet URL into U1's Value/Datasheet fields**, then verify two things against that datasheet: (1) that pins 1-6 really are CE / VOUT / VDD / Lx / GND / VFB as the symbol declares - it is the one part in this review whose pinout could not be verified against a datasheet, and it drives +12 V into the display connector; and (2) **whether the device has an integrated rectifier from Lx to VOUT** - there is no Schottky anywhere in the netlist between them, which is only acceptable if the rectifier is internal. *(Datasheet quotes elsewhere in this report - "Built-in a rectifier NPN transistor" - indicate it is, but confirm.)* The R26/R27 divider is correct: 1.0 V × (110 k + 10 k)/10 k = **12.00 V exactly**.
- **LOW-19 [CONFIRMED]** No mounting holes / no chassis ground - §4.5.

**INFO / verified-correct (recorded so they are not re-litigated)**

- **INFO-1 [CONFIRMED] The J2 USB-C baseline is correct.** The custom footprint is pad-for-pad identical to KiCad 9's stock `Connector_USB:USB_C_Receptacle_Molex_105450-0101` (all 24 X coordinates identical, sizes 0.298 vs 0.300 and 0.998 vs 1.000 for B1/B12, row separation 1.30 mm in both, shell posts at ±4.32 X with 0.41 and 5.77 mm Y offsets from the A row in both; only the global Y origin differs by 4.325 mm, and stock names all four shell pads `S1` while yours uses SH1-SH4). VBUS on all four of A4/A9/B4/B9, GND on all four of A1/A12/B1/B12. **CC1 and CC2 each have their OWN 5.1 k Rd** (R7 and R8, separate 1 % parts, BOM row 40 AF0402FR-075K1L) - this is *not* the shared-Rd bug. A6/B6 both on `/USB D+` and A7/B7 both on `/USB D-` - the correct flip-orientation shorting for a USB 2.0-only device in a 24-pin receptacle. Data path `/USB D+` → R17 (0 Ω) → `/IO20` → U10 pad 14 and `/USB D-` → R19 (0 Ω) → `/IO19` → U10 pad 13; ESP32-S2 GPIO19 = D− and GPIO20 = D+, so **polarity is correct** **[SUSPECTED on that last step - `_esp32s2solo2.pdf` extracts as scrambled font-subset text, so I could not reproduce Table 3-1 from the files; it is a well-known mapping]**. C19/C20 confirmed absent. **No VCONN handling is needed:** with 5.1 k Rd on both CCs, an e-marked cable's Ra (~1 k) parallels to 5.1 k‖1 k = 833 Ω, inside the 800 Ω-1.2 k Ra detection window. **No CC short-to-VBUS protection IC is needed:** CC sees only 5.1 k, so 5 V gives 1 mA and there is no silicon on CC to damage.
- **INFO-2 [CONFIRMED] Every other symbol-vs-footprint-vs-datasheet pin map verified as MATCH.** U2 BG95 (all 102 pads against Quectel Fig. 7 - left edge 1-18 at x=−9.15, bottom 19-31 with the gap between 24 and 25, right 32-49, top 50-62 with the gap between 56 and 57, plus all 40 inner pads; envelope 19.4 × 23.1 mm), U10 ESP32-S2-SOLO-2U (symbol matches Espressif Table 3-1; footprint matches Fig. 10-2 including the 3×3 thermal grid offset ~1.5 mm left of centre - **note the symbol declares 49 pins, not 40; pins 41-49 map to the thermal grid and do carry nets**), U8 MCP73871 (matches KiCad's official `Battery_Management:MCP73871` pin for pin; footprint is a standard CCW QFN-20 with the pin-1 dot at (−2.9,−1.1) next to pad 1 and EP 2.7 × 2.7 against Microchip's 2.65 mm), U6 TPS62172 (matches KiCad's official `Regulator_Switching:TPS62170DSG`; **FB→GND + VOS→+3.3 V is the correct fixed-output configuration, NOT a bug**; EP 0.9 × 1.6 matches TI's DSG pad), U5, U7, J2, J7, Q2, Q3, D1-D4, and J5's pad numbering. **The ZIF's "reversed/mis-numbered pads" bug does not recur anywhere else.** Cosmetic: fix the typo `VLN` → `VIN` on U6 pin 2's name in `Bingbong_library.kicad_sym`. *Caveat: the J5 line in this audit is only a pad-number-continuity check and explicitly does **not** clear the ZIF - see §1.*
- **INFO-3 [CONFIRMED] SETTLED: Q1's SOT-23 pad orientation is correct JEDEC.** `SOT-23-3_1P4X3P040_ONS.kicad_mod` pad 1 (−0.9525, +1.016) size 0.5588 × 1.3208, pad 2 (+0.9525, +1.016), pad 3 (0, −1.016) - two pads on one face, one centred on the other. F.SilkS pin-1 circle at (−0.9525, 2.4384) directly outboard of pad 1, F.Fab dot at (−0.9525, 0.4445). Topologically identical to KiCad's own `Package_TO_SOT_SMD:SOT-23`, just rotated 90°. Netlist: Q1.1 B → R1, Q1.2 E → GND, Q1.3 C → U2.15 PWRKEY, and Quectel Fig. 7 confirms pin 15 = PWRKEY. BOM confirms onsemi SMMBT2222ALT3G in SOT-23-3. **`review_refutation_matrix.md` left this open - it is now closed. The only remaining action is a routine "Update PCB from Schematic".**
- **INFO-4 [CONFIRMED] REFUTED: the hypothesised "both DIR pins tied the same way" bug does not exist.** The TI RSW pinout, reconstructed from the positioned datasheet text in `_sn74pos.txt`, resolves to 1=DIR2, 2=~OE, 3=GND, 4=B2, 5=B1, 6=VCCB, 7=VCCA, 8=A1, 9=A2, 10=DIR1 - exactly what the symbol declares. **DIR1 (pin 10) on +1.8 V** → channel 1 is A→B: A1 = `/BG95 TX` (U2.35 MAIN_TXD) → B1 = `/ESP32 RX` (U10.38 IO2). **DIR2 (pin 1) on GND** → channel 2 is B→A: B2 = `/ESP32 TX` (U10.39 IO1) → A2 = `/BG95 RX` (U2.34 MAIN_RXD). The two DIR pins are **deliberately opposite and both directions are right. Do not "fix" this - swapping either tie would break the link.** Footprint `QFN40P180X140X55-10N` is also correct (pads run counter-clockwise from 1 at (−0.645,−0.2) through 10 at (−0.4,−0.845), F.SilkS pin-1 dot at (−1.481,−0.192) beside pad 1). The only genuine U3 issue is `~OE` (M-13).
- **INFO-5 [CONFIRMED] REFUTED: S1/S2 wiring {1,3} vs {2,4} is CORRECT.** This looks like a dead short because the footprint puts pads 1,2 on the left face and 3,4 on the right, and most 6×6 tact switches common the two leads on the same face. It is not: the Same Sky TS04 datasheet's SCHEMATIC box (verified in the locally captured `_ts04_sch.png`) shows terminal (1) wired straight across to (3) and (2) straight across to (4), with the momentary contact between the two nodes, and its "Recommended PCB Layout, Top View" labels 1 = upper-left, 3 = upper-right, 2 = lower-left, 4 = lower-right - exactly matching `SW_TS04-66-70-BK-100-SMT.kicad_mod` (pad 1 (−4.55,−2.25), pad 3 (+4.55,−2.25), pad 2 (−4.55,+2.25), pad 4 (+4.55,+2.25), F.SilkS pin-1 circle at (−6.25,−2.25)). Netlist: `Net-(C17-Pad1)` = {C17.1, R4.1, S1.1, S1.3}, GND takes S1.2 and S1.4. **Had the pairing been 1-2/3-4, S1 would permanently ground `/EN` through R4 = 0 Ω (ESP32 held in reset forever) and S2 would permanently ground `/BOOT` (permanent download mode).** Symbol, footprint and datasheet all agree; KiCad's own `SW_SPST_PTS645Sx43SMTR92` models the same family with 1,1,2,2 numbering, independently corroborating the across-the-body pairing.
- **INFO-6 [CONFIRMED] ESP32-S2 strapping audit is clean.** Full GPIO map verified. **No LED and neither I2C pull-up touches IO0, IO45 or IO46** - all four LEDs are driven by U2/U8 status outputs, never by the ESP32. IO46 is correctly used as input-only (nothing drives it). IO45's internal-pulldown default of 0 selects VDD_SPI = 3.3 V, correct for the module's internal 3.3 V flash. The USB pair is not crossed. **The only digital-domain issues are the missing IO0 pull-up (LOW-12), the floating IO45/IO46 (§4.3), and the floating `/ESP32 RX` during the VCCA-off window (§4.3).** Also consider routing `Net-(U6-PG)` - currently a dead-end 100 k pull-up on U6.8 with nothing monitoring it - to a spare GPIO such as IO4.
- **INFO-7 [CONFIRMED] Grounding topology is clean** - §5.8.
- **INFO-8 [CONFIRMED] Factual correction to the project fact sheet: J7 (TE 2452808-1) is a nano-SIM card socket, not an RF connector.** Its libpart pins (`review_netlist.xml:1702-1712`) are pure smart-card contacts - C1 VCC (power_in), C2 RST (input), C3 CLK (input), C5 GND (power_in), C6 VPP (passive), C7 I/O (bidirectional), SW (passive), GND8/GND9 (shell) - landing on U2's USIM pins 43-47. BOM **row 21** describes it as "8 (6 + 2) Position Card Connector NANO SIM Surface Mount, Right Angle Gold". **Definitive radio-to-connector map: BG95 ANT_MAIN (U2.60) → J3.1 (MHF1/U.FL) is the ONLY board RF connector; BG95 ANT_GNSS (U2.49) → nothing; ESP32-S2-SOLO-2U → on-module MHF1, no board connector.** Believing there were two RF connectors would hide H-8. *(Mechanical note: J7 is right-angle at (115.9002, 92.6846, rot −90) and its card slot must break the case wall on a long edge - that competes directly with any long-edge antenna placement. Resolve before routing. Keep all five SIM traces ≤30 mm, together, over solid ground, ≥10 mm from the RF path and the +12 V run, with each ESD diode's GND via within 1 mm of its pad.)*
- **INFO-9 [CONFIRMED]** Set the stackup finish to ENIG and put ENIG in the fab notes - §5.1.

---

## 7. Open questions for the user

These cannot be inferred from the files. Answer them **before** routing; several change the mechanical design.

1. ~~What is the display MPN and its 26-pin FFC pinout?~~ **ANSWERED 2026-09-04.** **buydisplay ER-OLED018-1 (SSD1326, 256x32)**, ZIF **ER-CON26HT-1**, both from the BOM and now verified against the datasheet. J5 scores **26/26 on the direct map** (section 1.3). This closed H-1, H-2, M-1 and the pin-order half of LOW-13. **Residual: record both MPNs against J5 in the schematic** - the J5 BOM row's MPN field is still literally `--`.
2. **Is the ZIF top-contact or bottom-contact?** *Partially answered:* the datasheet mechanical drawing (p5/29) shows the flex tail with **contacts on the top face** and a **0.3 mm x 4 mm stiffener on the bottom**, and confirms `P0.5x(26-1)=12.5+/-0.03`, matching the footprint pad row exactly. **Still open: how the flex routes in the enclosure.** Unfolded (contacts up) needs top-contact; a hairpin fold needs bottom-contact and *preserves* conductor order; a longitudinal flip also gives contacts-down but **reverses** order and would break the verified net map. Simplest resolution: buy the **ER-CON26HT-1** the BOM already specifies - buydisplay's own mating part for this module - and rebuild the footprint from its drawing (see M-3; the current footprint matches neither it nor its Hirose 3D model).
3. ~~Is GNSS a product requirement?~~ **DECIDED 2026-09-04: GNSS is IN.** The product needs to know where it is; it can be dropped later if it does not fit the mechanical design. **Keep the BG95M3LA-64-SGNS SKU.** Work this creates: add **J8** (second TE CONMHF1-SMD-T), create the `/ANT_GNSS` net and route U2.49 through a 3-pad pi to J8.1, add **E3** = 1575.42 MHz L1 antenna to the BOM, and hold **>=25 mm separation from J3**. If the antenna is active, add a bias tee (33-47 nH 0402 wirewound choke to +3.3 V + 100 nF C0G series DC block) - **[SUSPECTED: confirm whether BG95 ANT_GNSS sources bias]**. GNSS_TXD/RXD (U2.27/28) can stay NC if position is read over the main UART by AT command - confirm against the Quectel GNSS application note. **The `RF_50` netclass already carries an `/ANT_GNSS` pattern, so the net picks up 0.38 mm the moment it exists.**
4. ~~Is EGPRS/2G in scope, or LTE-M/NB-IoT only?~~ **DECIDED 2026-09-04: LTE-M / NB-IoT only. No EGPRS.** Peak radio current drops from ~2 A to ~600 mA, which **closes four findings**: **M-14** (500 mAh cell is now 1.2C, not 4C - fine), **M-21** (JST SH at ~1 A/contact is now comfortable), **M-15/H-7** (the 470 uF THT can was justified as a 2 A burst buffer - that justification is gone, so C3 can move to a much smaller SMT polymer part or shrink substantially), and the **>=2 W antenna power rating** in C-4 relaxes. **Residual actions:** disable 2G in the modem configuration so it can never fall back, and confirm the band list (Q5) - that is now the gating RF unknown.
5. **What is the operator band list?** The lowest supported uplink sets the counterpoise length (113 mm at 663 MHz vs 91 mm at 824 MHz) and therefore the enclosure. **The only band data anywhere in the project is a distributor string in BOM row 29 listing GSM bands only.** (§5.6)
6. **Which antenna parts are you actually buying?** Three radios, one Wi-Fi-only patch in the BOM, marked Not Purchased with no refdes. The vendor keepout drawing is a required deliverable before routing. (C-4)
7. ~~4-layer or stay 2-layer?~~ **DECIDED 2026-09-04: 4-layer.** Target **JLCPCB JLC04161H-7628** or equivalent: L1 signal + RF / **L2 solid GND** / L3 power / L4 signal, 1.6 mm, 1 oz outer. 50 ohm GCPW = **W 0.38 / gap 0.20 mm**; 90 ohm differential = **W 0.27 / gap 0.15 mm**. **APPLIED:** the six netclasses (`Default`, `RF_50`, `USB_90`, `BATT`, `PWR`, `HV`) and their net patterns are now in `bingbong.kicad_pro`, and matching impedance / diff-pair / clearance rules are in `bingbong.kicad_dru`. **STILL TO DO BY HAND:** add the two inner copper layers in Board Setup > Physical Stackup (KiCad must assign the layer IDs - do not hand-edit `bingbong.kicad_pcb`), set the finish to **ENIG**, and tick impedance control on the fab order form with the spec in the drawing notes. H-10 is otherwise closed.
8. **Is the screwless captured-board design deliberate?** Zero mounting holes and no screws/standoffs in the BOM, but connector insertion forces are currently reacted by solder joints. (§4.5)
9. **Do you want the charger firmware-controlled or hard-strapped?** C-1's recommended fix routes PROG2 to a GPIO with a safe 100 mA default. If firmware will never manage it, hard-strap PROG2 high instead and accept that the board is not USB-compliant before enumeration.
10. **Should the modem stay on the raw cell?** It is standard Quectel practice and I recommend keeping it, but it costs you proper charge termination - so choose between re-enabling the 6 h `~TE` timer and adding a firmware charge timeout, and document it. (M-2)
11. **Was the R1200's rectifier verified?** There is no Schottky between Lx and +12 V anywhere in the netlist. Confirm the R1200N002A has an internal synchronous rectifier, and confirm its SOT-23-6 pin order. (LOW-18)
12. **Is the MIC5504's TDFN-4 pin order really 1=VOUT, 2=GND, 3=EN, 4=VIN?** The symbol says so and the netlist is consistent, but I could not read the Microchip datasheet from this project (`_mic.txt` / `_mic5504.txt` are 0 bytes). If the symbol is wrong, +3.3 V lands on the LDO output and the +1.8 V rail is pulled up through the pass-device body diode to ~3.0 V, exceeding the BG95's 1.8 V domain. **Check this before rebuilding the footprint.** (C-3)
13. **Which J6 pins do you actually need?** If it is only a bring-up monitor, converting it to labelled test pads removes the whole hazard class. (H-11)

---

## 8. Appendix: refuted findings and why

Seven findings were raised during the domain passes and **dismissed** on adversarial re-checking against the files. They are recorded so they are not re-raised. **Two of them proposed edits that would have damaged the board - do not apply them.**

| Claimed finding | Why it was dropped |
|---|---|
| **"U2 BG95 footprint has ZERO solder-paste apertures on all 102 LGA pads - the module cannot be reflowed."** *(claimed critical)* | **FALSE, and the proposed `sed` would have damaged the board.** `XCVR_BG95M3LA-64-SGNS.kicad_mod` has full paste coverage implemented as **graphics**: 62 `fp_poly` + 40 `fp_circle` on `F.Paste` = exactly 102, matching the 102 pads. Every pad centre matches a paste-item centre at 0.15 mm tolerance (0 unmatched). The 62 polys are 0.98 × 0.63 mm over 1.1 × 0.7 mm pads - a deliberate ~80 % stencil reduction. The "gerber confirmation" was a **methodology error**: graphics plot as G36/G37 regions and stroked arcs, never as D03 flashes, so a flash count is structurally guaranteed to return 0. Re-measuring by coordinate, **15,660** points fall inside the U2 box (of 16,046 in the whole file). Applying the proposed edit would have added a second, larger, full-pad aperture on top of every existing one on a 102-pad LGA → ~100 % coverage and a real bridging risk. |
| **"J2 USB-C footprint has ZERO solder-mask apertures on all 24 signal pads - mask is printed over every USB pad."** *(claimed critical)* | **FALSE, same flash-counting error.** `MOLEX_1054500101.kicad_mod` has 24 `fp_poly` on `F.Mask`, one per signal pad, each 0.425 × 0.827 mm over a 0.298 × 0.7 mm pad (a correct ~0.06 mm expansion); all 24 matched at 0.1 mm tolerance. In the shipped `bingbong-F_Mask.gbr` the J2 box contains 240 coordinate points (24 polys × 10 vertices) whose Y extents (−160.987/−160.160 and −159.686/−158.859) centre exactly on the two rows the finding claimed had zero mask. **The real, smaller issue is M-10** (mask drawn as graphics rather than pad layers → 75 µm dams and no DRC coverage). |
| **"U7 MIC5504 pads are 2 mil squares - unmanufacturable, kills the +1.8 V rail and the BG95 UART."** *(claimed high as a standalone)* | **Down-scoped, not dropped.** The 0.0508 mm pads are real but they are **net-anchor stubs**, not the lands: the file also contains 4 F.Cu + 4 F.Mask + 4 F.Paste `fp_poly` at the same centres, sized 0.4826 × 0.254 (pad 1) and 0.4064 × 0.254 mm - a normal 1×1 DFN-4 land on 0.65 mm Y pitch - and the shipped gerbers show 87 F_Cu / 28 F_Mask / 27 F_Paste coordinate points in a 2.4 mm box at U7. **The rail is not killed.** The reviewer also misread pad 1's X offset as a bad auto-import: pad 1's outer edge is −0.41148−0.2413 = −0.6528 and pad 2's is −0.44958−0.2032 = −0.6528, **identical** - pad 1 is deliberately elongated inward as the pin-1 land marker. **The genuine defects survive as C-3** (zero mask expansion, no EP paste, un-netted copper invisible to DRC/zones). |
| **"All three exposed thermal pads (U8 EP, U6 EPAD, U7 EP) have no paste aperture."** | **Two of the three are false.** `QFN50P400X400X100-21N` (U8) already has a **2×2 window-pane of 0.96 × 0.96 mm** `F.Paste` polys at (±0.61, ±0.61) - literally the fix being proposed. `SON50P200X200X80-9N` (U6) already has one 0.56 × 1.02 mm poly (~40 % of the 0.9 × 1.6 EP). Both are present in the shipped gerber (window-pane vertex pairs 0.96 mm apart at U8's (129.786, −158.339); a 0.56 × 1.02 rectangle exactly at U6's origin). **Only U7's ~0.48 mm rotated-square EP genuinely lacks paste** - folded into C-3. Do nothing to U8 or U6. |
| **"CR1/CR2/CR3 are on the wrong land (SOD-923 vs SOD-882D) and will fail open silently."** *(claimed critical)* | **Backwards - applying the proposed fix would mis-land the ordered part.** The BOM buys onsemi **ESD9B5.0ST5G**, Package/Case field "SOD-923". The schematic's override to `Diode_SMD:D_SOD-923` (at `bingbong.kicad_sch:16656, 19957, 25956`) is therefore **correct**. The stale artefacts are the symbol's *name/Value* (`PESD5V0F1BLD_315`) and its default Footprint property (`DFN1006D-2_SOD882D_NEX`, itself unusable as written - no library prefix). The land-geometry numbers quoted (SOD-882D 0.3048 × 0.5588 at ±0.3175 vs KiCad SOD-923 0.36 × 0.25 at ±0.42) are accurate but support the opposite conclusion. **Reduced to LOW-9, a documentation fix.** |
| **"Q2 FDN340P vs FDN338P is a channel-polarity mismatch - an N-channel part in a high-side P-channel position would never enhance."** | **The polarity claim is fabricated.** The BOM's own description for the FDN338P line reads **"P-Channel 20 V 1.6A (Ta) 500mW (Ta) Surface Mount SOT-23-3"** with the onsemi FDN338P datasheet URL. Same polarity, same 1=G / 2=S / 3=D pinout. The high-side topology (R30 10 k gate pull-up, Q3 pulldown, source on +3.3 V, drain to U1.3 + L2.1 + C24) is correctly identified, but **the discrepancy is exactly a metadata mismatch - reduced to LOW-8.** |
| **"J5 hold-down tab pads carry 16× the paste volume of the signal pads and will float/skew the connector on a 0.5 mm pitch."** | **Arithmetic correct, conclusion unsupported and contradicted by the vendor patterns.** KiCad's Hirose FH12-26S land uses **full 100 % paste** on 3.96 mm² MP pads (10.6:1 against its 0.39 mm² signal pads), and TE_2-1734839-6 uses full paste on 7.13 mm² tabs (**21.6:1 - larger than the ratio being flagged**). Full paste on FFC hold-down tabs is the manufacturer-recommended norm; the tabs are the mechanical anchors and are *supposed* to wet fully. Window-paning them to 50-60 % as proposed would **reduce** retention on the one feature holding a 0.5 mm pitch connector down. An optional DFM preference at most. |

**Additional claims withdrawn from *within* surviving findings.** These were load-bearing in the pre-refutation draft (`SCHEMATIC_REVIEW_2026-09-03.predraft.bak`) and are corrected here:

- **The J5 "kill shot"** - that J5.4-J5.9 being grounded proves the mirror, because under the direct reading they would be the display's VDD/VDDIO/BS block and VDD would be shorted to ground. **Withdrawn.** On a 26-pin external-VCC variant those are more likely BS/CS#/RES#/D-C#-class pins, and grounding them is benign. "Only the mirrored reading is survivable" does not follow. (§1.3)
- **"Rotate J5 180° in pcbnew"** as a zero-churn fix. **Withdrawn and actively wrong** - rotation carries the pads and their nets with it, and the footprint is not 180°-symmetric anyway (contacts at y = −1.58, tabs at y = +0.7). (§1.2)
- **"Void L2 under J3.1 and U2.60; those pads add ~0.4-0.5 pF each, ~150 Ω at 2.2 GHz"** (`...predraft.bak:328`). **Withdrawn** - recomputed excess is 0.070 pF and 0.012 pF → −32.4 dB and −47.6 dB. That figure would have required h ≈ 0.1 mm. (§5.5)
- **"`copper_finish "None"` means you cannot order impedance control or a TDR coupon."** **Withdrawn** - those KiCad fields are documentation only and are not exported to gerbers; impedance control is ordered via the fab's order form and the fab-drawing notes. Fill the stackup anyway (INFO-9). (§5.1)
- **"The BOM lists three candidate cells including two Amazon links."** **Withdrawn as fabricated** - the workbook has exactly one battery line (row 48, ASR00035, 500 mAh) and the string "amazon" appears nowhere in it. Any recommendation predicated on "more than one harness pinout is in play" is void. (H-7, M-14)
- **"50 Ω and 90 Ω are physically unroutable on the current stack."** **Withdrawn** - 50 Ω GCPW at W = 1.229 mm is buildable, and the USB link is Full-Speed only. Go 4-layer for the RF reference, not because USB demands it. (H-10)
- **"10 Ω 0402 series resistors in each J6 rail feed."** **Withdrawn** - a 1/16 W 0402 dissipates its rating at 79 mA and would make the header useless for powering the board. (H-11)
- **"Replace C3 with 4 × 47 µF X5R 1210."** **Withdrawn** - 188 µF nominal derates to well under half at 3.7-4.2 V bias, against a part sized for a ~2 A EGPRS burst. Use polymer bulk. (H-7, M-15)
- **"Move the BG95 to `/SYS LOAD`."** **Withdrawn as probably harmful** - it puts a 2 A burst through a 200 mΩ pass FET behind an input current limit. (M-2)
- **"Change U6's GND pins from `power_out` to `power_in`."** **Partially withdrawn** - U6's grounds are already `power_in`; only U10, U7 and U1 need the change. (§4.6)

# bingbong v3 — schematic gap analysis and spec

Date: 2026-09-23
Basis: `REDESIGN_DECISION_2026-09-12.md` (architecture) as overridden by `DESIGN_MANUFACTURING_REPORT_2026-09-19.md` §0.3 (on-demand AMOLED) and §6 (electronics domain, E-1…E-17). Where the two disagree, the 09-19 report wins.
Compared against: v1 `firmware/bingbong_pcb/bingbong.kicad_sch` (ESP32-S2 + BG95) and the abandoned v2 `cad-v2/bingbong/bingbong.kicad_sch` (ESP32-S3 + BG95 + W25Q32 — same v1 architecture, not carried forward).

Evidence tags follow the decision document: `[V]` primary source read, `[V?]` read once or contested, `[U]` nobody has opened the source.

---

## 1. Verdict

v3 is a clean-sheet schematic. **No v1/v2 circuit block survives electrically.** Every major IC changes, the power topology inverts (modem/MCU straight off VSYS instead of a 3.3 V buck), and the board goes from 120 × 37.5 mm to 23 × 52 mm 6-layer 0.8 mm with an LGA SiP. What carries over is the *lessons* from the v1 reviews (section 3), a handful of footprint-library entries, and the naming/ERC hygiene.

Start v3 as a new KiCad project (`cad-v3/bingbong/`), hierarchical, one sheet per E-step block. Do not edit v2 into v3.

---

## 2. Block-by-block: v1 → v3

| Block | v1 / v2 (current schematic) | v3 (spec) | Action |
|---|---|---|---|
| MCU | ESP32-S2-SOLO-2U (v2: ESP32-S3 + 40 MHz XTAL + W25Q32) | **nRF9151-LACA-R** (MCU + LTE-M + RF FE + PMIC + crystals in one LGA 12.1 × 11.1 × 1.2) | Delete. New symbol + footprint from PS v1.0. |
| Cellular modem | Quectel BG95-M3 + 1.8 V LDO (MIC5504) + SN74AVC2T245 level shifter + Q1 PWRKEY transistor | Inside nRF9151 | Delete U2, U3, U7, Q1, R1 and all UART translation. |
| GNSS | BG95 GNSS + 2nd antenna/MHF1 | **Not fitted**, pins terminated per HIG | Delete. |
| SIM | Nano-SIM socket J7 + 3 × ESD + card-detect to MCU | **MFF2 eUICC** DFN-8 5 × 6, ISO 7816-3 **Class C 1.8 V**, ≤ 10 mm from SiP; HIG series/shunt filter | Delete J7/CR1-3. New footprint; MPN `[U]`. |
| Charger | MCP73871 @ 100 mA, THERM via TH1 JST + DNP R24 | **BQ25188YBGR** (DSBGA-8, successor to BQ25180, SLUSFJ3 `[V]`): 300 mA set in FW after NTC read; **combined TS/MR pin** (NTC + crown button, see §9.1); /INT → nRF; I²C 0x6A | Delete U8 + network. New. |
| Fuel gauge | none | **MAX17048G+T10**, VDD **on BAT** (not V3) | New. |
| Regulation | TPS62172 3.3 V buck from SYS (fails at low cell) + MIC5504 1.8 V | **TPS62840DLC → V3 = 3.1 V**, the only general rail. nRF VDD straight from VSYS (3.0–5.5 V) | Replace. Fixes v1 critical C3 by design. |
| Display | ER-OLED018-1 256×32 SSD1326 PMOLED, I²C, 26-pin ZIF | **1.1" 126 × 294 AMOLED module, off the shelf**: iFan IF011TPS12-29 (RM69310, 27-pin) or OSPTEK AM110Q126294LK1 (ICNA3306, 24-pin) — see §9.3; 4-wire SPI | Replace. Pick the module first; the two are **not** pin-compatible. |
| Display power | R1200 12 V boost + L2 + Q2/Q3 switch | **TPS65631DPDR** (§9.2) → ELVDD +4.6 / ELVSS per panel (−2.4 V on the OSPTEK module) + **two 4.7 µH inductors** + **two TPS22916C load switches** (A: V3→VCI/VDDIO, B: VSYS→PMIC VIN) | Delete R1200 chain. New. |
| Charge / debug port | USB-C (J2) + CC Rd + TPD2EUSB30A + native USB | **4-pad magnetic pogo** GND·SWCLK·SWDIO·VBUS on a lid flex → 5-way 0.4 mm B2B (5th = jig ID) | Delete USB-C block. New dock sheet. |
| Input | Cherry MX key / TS04 tact | Crown on a **satellite PCB**: MT6701 (or AS5600L variant) + 2 × DRV5032DU + EVPBB-class tact, over a 10/12-way 0.5 mm tail | New (separate board). |
| Grip | none | **Azoteq IQS211B**, buried 316L ring electrode, 2k2 + 10 pF | New. |
| Haptics | none | **DRV2625** → Vybronics VG0840001D LRA | New. |
| Light | discrete LEDs | **PLCC-4 RGB halo**, common anode VSYS, 3 × SOT-523 N-FET on hardware PWM | Replace. |
| Flash | ESP internal (v2: W25Q32 as ESP boot flash) | **16 Mbit SPI NOR** (MX25R1635F class) on shared SPIM — MCUboot slot 1 + assets | New role; MPN `[U]`. |
| Antenna | MHF1/u.FL to external antenna | Metal end-cap radiator via SMT spring finger; **MM8130-2600** switch connector; 10 × 0402 dual-resonant match; ≤ 0.3 pF TVS; L_dc | New RF sheet. |
| Battery | 2-pin JST, ~500 mAh | 23 × 43 × 6.0 mm pouch, 560–620 mAh `[U]`, PCM, 10 k NTC, **3-way B2B** (B+, B−, NTC) | Replace connector. |

### What actually carries over from v1/v2

- **Nothing electrical.** Possibly the 10 k β3435 NTC convention and 0402 passive footprints.
- `Bingbong_library` — keep the library *structure*; none of its current parts (BG95, ESP32-S3, TS04 tact, Cherry MX, XRCGB40M crystal, the Molex connectors) are used. Start `Bingbong_v3` library fresh.
- Design-rule file `bingbong.kicad_dru` — does not apply (v3 is 6-layer HDI with via-in-pad). Write new rules against the fab's HDI capability.

---

## 3. v1 review findings → how v3 must not repeat them

| v1 finding | v3 rule |
|---|---|
| C3: 3.3 V buck from a single cell drops out | nRF VDD on VSYS (3.0–5.5 V). V3 = 3.1 V from TPS62840 (100 % mode) with cell cutoff raised to **3.45 V**. Any 3.0 V-min part on V3 (MT6701/AS5600L) gets a load switch ≤ 0.5 Ω (C-13: 3.1 V −2 % = 3.04 V). |
| H1: boost inductor at 220 mA | PMIC inductor Isat ≥ 0.8 A `[U]`, shielded, ≤ 1.0 mm tall; size from TPS65631 datasheet, not a guess. |
| H2: R1200 CE driven while its VDD off | **GPIO-park rule (E-8)** on every net crossing to a switchable domain: SCK/MOSI/CS/D-C/RESX parked low, TE pull-down, before switch A turns off. Draw the park state on the schematic next to each net. |
| C2: Q1 pinout symbol ≠ BOM ≠ footprint | Every symbol has MPN + datasheet field populated at placement; pin numbers checked against the datasheet drawing; no generic `Q_NPN`-style symbols for ordered parts. |
| M2: Q2 schematic FDN340P vs BOM FDN338P | BOM is exported from the schematic only; no parallel spreadsheet. |
| H7: SIM missing bypass/filter | eUICC gets HIG-specified series R / shunt C footprints and VDD bypass from day one. |
| H8: global `+5V` name hid VBUS role | Net names by role: `VBUS_PAD`, `VBUS_IN` (after P-FET), `VSYS`, `VBAT`, `V3`, `VCI_SW`, `PMIC_VIN_SW`, `ELVDD`, `ELVSS`, `SIM_1V8`. No `+5V`/`+3.3V` globals. |
| M6: 43 ERC errors from wrong pin types | Symbols drawn with correct `power_in`/`passive` types; PWR_FLAG only on true sources (cell B2B, dock VBUS). ERC clean or every waiver documented. |
| C1: 22 µF on USB D+ | Signal-integrity parts (SPI 33 Ω, latch 100 Ω/47 pF) placed per sheet spec; no bulk caps on signal nets — ERC net-class check. |

---

## 4. Sheet plan (hierarchical, matches E-step order)

| Sheet | Contents | Governing sections |
|---|---|---|
| 1 `power` | VBUS_PAD → ferrite → TVS (Vwm ≥ 5.5 V, clamp below the BQ25188's 25 V IN abs max; its VIN_OVP is 18.5 V typ) → reverse P-FET (gate 1 MΩ to GND) → BQ25188 → VSYS; cell B2B + NTC on TS/MR (100 nF at TS/MR) + button N-FET (§9.1); MAX17048 on BAT; TPS62840 (RSET 71.5 kΩ `[V?]`, C(VSET) ≤ 100 pF, MODE/STOP low); VSYS bulk 2 × 22 µF 0805 | E-1, E-2 |
| 2 `nrf9151` | SiP, decoupling (4.7 µF + 100 nF per VDD group), VDD_GPIO ← V3, SWD, COEX0 loop-back, GNSS pins terminated, MAGPIO/COEX1-2 NC `[V?]`; MFF2 eUICC | E-3, E-4 |
| 3 `rf` | ANT → 100 pF series (footprint) → MM8130-2600 → 10 × 0402 positions (5 fitted + 2 harmonic-trap + spares) → ≤ 0.3 pF TVS ∥ L_dc 22 nH → DC test pad → feed trace → spring finger pad | §5 Steps 8–12 |
| 4 `display` | **Drawn 2026-09-28 for OSPTEK AM110Q126294LK1 (see §10).** Originally: switch A (V3→VCI/VDDIO, 1 µF + 100 nF at tail), switch B (VSYS→PMIC VIN, 10 µF), TPS65631 + L + 4.7–10 µF per output, 27-pin 0.4 mm B2B, SPI with 33 Ω on SCK/MOSI, RESX 10 k pull-down, TE → GPIOTE, SDO → MISO if exposed | E-5, E-6, E-8 |
| 5 `ui` | IQS211B (2k2 + 10 pF C0G), DRV2625 (10 µF at VDD) + LRA pads, RGB halo + 3 N-FETs + 10 nF, SPI NOR, satellite connector with 100 Ω + 47 pF on HA/HB, sensor load switch | E-10, E-14 |
| 6 `dock` | Lid-flex 5-way B2B; three **gate-to-V3 N-FET limiter cells** (SWDIO, SWCLK, TACT): pad ESD diode (5 V working, ≤ 15 pF) → 220 Ω → N-FET (drain pad side, gate V3, Vth ≤ 1 V) → nRF with 4.7 k pull-up to V3 (SWDIO); DOCK_ID 1 MΩ pull-down | E-13, E-15 |
| 7 `testpoints` | ≥ 24 bottom-side ø0.9 mm pads on a 1.27 mm grid (VBAT, VSYS, V3, VCI_SW, PMIC_VIN_SW, ELVDD, ELVSS, SDA, SCL, SWDIO_nRF, SWCLK_nRF, TE, RESX, CS_DISP, COEX0, TACT_nRF, HA1/HA2/HB1/HB2, NTC, LRA±, LED_R/G/B, DOCK_ID, GND × 4) | E-16 |
| **Separate project** `satellite` | 22 × 10 × 0.6 mm 2-layer: MT6701QT (variant A) / AS5600L (variant B), 2 × DRV5032DU, tact to GND, crown bleed 1 MΩ ∥ low-C TVS, 10/12-way tail | E-10, §4 step 13, C-24 |

## 5. GPIO allocation (26 of 32; E-4)

| Function | Pins | Notes |
|---|---|---|
| SPIM0 shared: SCK, MOSI, MISO | 3 | display + NOR; MISO reads panel SDO if tail has it |
| CS_DISP, D/C, CS_NOR | 3 | 4-wire SPI mandatory (8-bit frames `[V?]`) |
| RESX, TE, DISP_SW_A_EN, DISP_PMIC_CTRL, CTP_INT | 5 | **2026-09-28:** OSPTEK tail has no SWIRE → MCU drives CTRL (P0.23, was DISP_SW_B_EN; switch B ON now = VCI_SW). Touch INT on P0.20 (last spare). Touch reset shares RESX. **All 32 GPIOs used.** |
| TWIM0 SDA, SCL | 2 | BQ25180, MAX17048, IQS211B, DRV2625, MT6701 (0x06) / AS5600L (0x40); 4.7 k to V3 |
| HA1, HA2, HB1, HB2, TACT_nRF, SENSOR_SW_EN | 6 | latches + TACT on GPIOTE |
| DRV2625 TRIG/EN | 1 | |
| LED_R, LED_G, LED_B | 3 | PWM0 |
| IQS211B RDY | 1 | |
| BQ /INT | 1 | dock presence = VIN-good |
| COEX0 loop-back | 1 | `AT%XCOEX0=2,1,690,760,1,1700,2160` |
| DOCK_ID | 1 | EOL jig only |
| **Spare** | **5–6** | 2 reserved: grip fallback; 2 reserved: TWIM1 if sensor clamps I²C unpowered (OQ-10) |

Actual pin numbers wait on the nRF9151 PS pin list; assign so SPI/RF-adjacent pins keep SCK away from ANT.

---

## 6. Datasheet gate — must be opened before the sheet is drawn

Only `nrf9151_ps` (extract), `drv5032` and `ls011` (now unused) exist in the repo (`firmware/bingbong_pcb/_mech/`). Everything below is missing.

| # | Document | Blocks | Unknowns it settles |
|---|---|---|---|
| 1 | **RM69310 datasheet + AMOLED panel drawing (27-pin map)** | sheet 4 | pinout, SDO presence, SPI mode, tSLPOUT, SWIRE semantics, **ELVSS abs max vs PMIC −4.0 V default (ER-2)** |
| 2 | **TPS65631 SLVSBK1E + TPS65631W SLVSC27D — opened 2026-09-23** (`_mech/tps65631*.txt`) | sheet 4 | Closed; findings in §9.2 |
| 3 | ~~BQ25180 SLUSE99C~~ → **BQ25188 SLUSFJ3 — opened 2026-09-23** (`firmware/bingbong_pcb/_mech/bq25188.txt`) | sheet 1, 6 | Closed; findings in §9.1 |
| 4 | **nRF9151 PS full + HIG** | sheets 2, 3 | pin list (MAGPIO?), LGA pitch → via-in-pad rule, SIM voltage class, ANT DC tolerance, decoupling, SPIM fmax, GPIO injection limit |
| 5 | TPS62840 SLVSEC6D Table 1 | sheet 1 | RSET for 3.1 V (71.5 kΩ `[V?]`), 3.2 V option |
| 6 | TPS22916 | sheet 4 | off leakage and slew at 3.1 V / 4.4 V |
| 7 | MFF2 eUICC MPN | sheet 2 | Class C, **written supply-shutdown confirmation** |
| 8 | MT6701 / AS5600L | satellite | unpowered SDA/SCL clamping (OQ-10) |
| 9 | Spring finger, antenna TVS, SPI NOR, RGB LED, limiter N-FET, tact MPNs | 3, 5, 6 | placeholders today |

Rule: a symbol may be placed with `[U]` values, but its sheet is not "specced" until its row above is closed and the value field carries the MPN.

---

## 7. Order of work

1. Fetch rows 1–4 of section 6. nRF9151 supply: **18,654 in stock as of 2026-09-23** (owner check; distributor and ordering suffix not recorded) — this retires the doc's 16–19 wk lead-time risk (ER-5) for now. Buy the ≥ 40 prototype SiPs (§2 P0-1) while stock holds; confirm the counted stock is `NRF9151-LACA-R` / `-R7`, not the DK.
2. Create library `Bingbong_v3`: nRF9151 (LGA from PS), BQ25180, MAX17048, TPS62840, TPS65631, TPS22916, DRV2625, IQS211B, MFF2, MM8130-2600, 27-pin B2B, 5-way / 3-way B2B, FH12-12S.
3. Draw sheets 1 → 2 → 4 → 6 → 5 → 3 → 7 (power first, RF last because its values come from Mule B).
4. Satellite project in parallel once the 10 vs 12-way tail is decided (recommend 12-way, GND on 1 and 12).
5. ERC clean; abs-max audit table (E-1.6) attached to sheet 1 as a text block.
6. Only then board outline: 23 × 52, copper end X = 63.0, 6-layer 0.8 mm stack-up per E-11.

## 8. Open decisions that change the schematic (not just values)

- **Switch B** stays unless TPS65631 IQ(VIN, disabled) ≤ 0.5 µA. *2026-09-28: kept, ON driven by VCI_SW instead of a GPIO.*
- ~~**PMIC CTRL**: panel SWIRE (no GPIO) vs MCU-driven (+1 GPIO)~~ — **closed 2026-09-28: MCU-driven** (OSPTEK tail has no SWIRE).
- **TACT limiter**: required if /MR pull-up is above VDD_GPIO.
- **TWIM1** for the sensor if unpowered MT6701/AS5600L clamps the bus.
- **Satellite tail** 10 vs 12-way.
- **PMIC VIN source** moves off VSYS if docked SYS_REG can exceed 4.5 V.

---

## 9. Datasheet findings, 2026-09-23

### 9.1 BQ25188 (replaces BQ25180) — SLUSFJ3 `[V]`

Same DSBGA-8 1.6 × 1.1 footprint and pinout class; no HDI required. Pins: IN, SYS, BAT, GND, SCL, SDA, /INT, **TS/MR**.

| Item | Value | Consequence for v3 |
|---|---|---|
| IN abs max | 25 V; operating 3.0–18 V; VIN_OVP 18–19 V | Survives the adapter-misuse case the doc cared about. |
| SYS regulation (docked) | `SYS_REG_CTRL`: 000 = VBAT + 225 mV (3.8 V min); 001 = 4.4 V; **010 = 4.5 V (default)**; up to 4.9 V; 111 = passthrough ≤ 5.5 V | Power-up default 4.5 V sits exactly on the TPS65631 4.5 V VIN max. **Firmware sets 000 (≤ 4.43 V at VBATREG 4.2 V) at boot**; switch B stays in so the PMIC never sees the default. Resolves ER-14 as a firmware rule plus switch B. |
| ICHG default | 10 mA (code 5); 5–1000 mA | Dead-battery charging works without firmware, slowly and safely. Firmware sets 300 mA after the NTC check. |
| IQ_BAT | 3 µA typ, pushbutton off; **4 µA typ / 5 µA max, pushbutton on**; ship 3.2 µA; shutdown 15 nA | Keep the 5.5 µA budget line. |
| Watchdog | I²C watchdog **on by default, 160 s → soft-resets all registers** (SYS_REG back to 4.5 V, long-press back to ship mode, ICHG back to 10 mA). 15 s HW-reset watchdog **off by default** | Firmware disables `WATCHDOG_SEL` at first I²C write (E-1.2 rule stands). Dock programming of a blank board is not interrupted. |
| Long press | Default action = **ship mode after 5 s** (`PB_LPRESS_ACTION` = 10, `MR_LPRESS` 5/10/15/20 s) | A 5 s crown hold would ship-mode the device with default registers. Firmware sets hardware reset at 15–20 s (field recovery path, OQ-7). |
| Button timers | WAKE1 300 ms / 1 s, WAKE2 2 s / 3 s; press = TS/MR < 90 mV | Too slow for the boop; the nRF needs its own press signal. |
| I²C | 7-bit 0x6A; pull-ups to the logic rail (V3); all non-IN pins abs max 5.5 V | No conflict with MAX17048 (0x36), DRV2625 (0x5A), MT6701 (0x06), AS5600L (0x40); IQS211B address still to confirm. |

**Correction to report E-1.2 / E-10 / E-13 (applies to the BQ25180 too):** there is no separate /MR pin. The NTC and the push-button share **TS/MR**. The pin sources 38 µA (adapter present) / 60 µA (battery only, *pulsed periodically*), so its voltage tracks the NTC (≈ 0.1–1.6 V over temperature) and drops to ~0 V between pulses. **The nRF cannot read the button from TS/MR**, and the button must pull TS/MR below 90 mV without upsetting the NTC reading.

Proposed circuit (to verify on EVM-1):
- Crown tact switches **VBAT (through 10 kΩ, on the satellite tail) → TACT_HI**, with 1 MΩ from TACT_HI to GND.
- TACT_HI drives the gate of a low-Vth N-FET whose drain is on TS/MR (source GND): a press pulls TS/MR to ~0 V; released, the FET is off and the NTC reads normally.
- The nRF reads TACT_HI through the existing gate-to-V3 limiter cell (E-13), so its pin never exceeds V3.
- Works in ship mode (VBAT is always present), so ship-mode wake and long-press hardware reset stay passive (E-2 holds). Standing current is 0 released and ≈ 4 µA only while pressed.
- The satellite tail's TACT conductor now carries VBAT through 10 kΩ, which C-24 already anticipated for the /MR domain.

### 9.2 TPS65631 vs TPS65631W → use **TPS65631DPDR**

| | TPS65631DPDR | TPS65631WDSKR |
|---|---|---|
| Package | WSON-12, 3.0 × 3.0 mm | WSON-10, 2.5 × 2.5 mm |
| Output current | 250 mA | 200 mA |
| Inductors (2 required: boost + inverting) | 4.7 µH (TI list: LPP252012-4R7N, 1239AS-H-4R7M, …) | 10 µH (TI list: DFE252012C-100M, MDKK2020T-100M, …) |
| Shutdown behaviour | **Active discharge** of VPOS/VNEG (30 Ω / 150 Ω) | Outputs **high-impedance** in shutdown |
| VNEG slew control | CT pin (capacitor sets the step time) | none |
| Shutdown current | 0.1 µA typ into AVIN, CTRL low | 0.1 µA typ |
| VIN | 2.9–4.5 V | 2.9–4.5 V |
| VNEG programming | CTRL pulses: 0 = −4.0 V default; **21 edges = −2.4 V**, 23 edges = −2.2 V | same |

Why DPD: the panel spec (OSPTEK §13.1.8) requires the high-voltage rails to be removed **before** the logic supply. Active discharge makes ELVDD/ELVSS collapse fast and deterministically before switch A drops VCI/IOVCC (E-5.5); the W part leaves them floating. The panel draws 6–20 mA, so both have ample current. The W part only wins on area (≈ 2.75 mm² less); keep it as the fallback if the side strip does not close. Confirm with the panel vendor which PMIC their reference board uses.

Other consequences:
- Report said "one shielded inductor"; it is **two**. Height matters: E-5.6 allows ≤ 1.0 mm, and TI's listed 2520 parts are 1.2 mm → find 1.0 mm-tall 4.7 µH parts with Isat ≥ 1.2 A (switch valley limit is 0.8–1.0 A) `[U]`.
- With 0.1 µA shutdown current, switch B is no longer needed for leakage. **Keep it anyway** because of the 4.5 V SYS default (§9.1) until firmware provably sets SYS_REG before any display enable; revisit at EVM-1.
- **No TI EVM exists for TPS65631/TPS65631W** (checked 2026-09-23: none listed on ti.com, tool URLs 404). The report's Mule A plan (E-5.7, EV-1 b) to use a "TPS65631EVM" must change: use the panel vendor's demo/adapter board for panel bring-up, and validate our own TPS65631 circuit on a small breakout or directly on EVM-1.
- The −4.0 V start-up default before the pulse count is confirmed on both parts (CT does not affect the first ramp). ER-2 still needs the panel's ELVSS abs max.

### 9.3 AMOLED — it is an off-the-shelf module; pick one

Both candidates are standard Chinese AMOLED modules: panel + driver IC on glass + FPC tail. **Neither has a power IC on the module** (OSPTEK spec: "Power IC: none"), so our board supplies ELVDD/ELVSS from the TPS65631 as planned.

| | iFan Display **IF011TPS12-29** | OSPTEK **AM110Q126294LK1** |
|---|---|---|
| Driver | RM69310 | ICNA3306 |
| Outline | 12.96 × 30.94 × 0.784 mm | 12.96 × 30.94 × 0.80 mm (15.40 × 38.97 × 1.88 with cover glass + touch) |
| Active area | 10.962 × 25.578 mm | 10.96 × 25.58 mm |
| Tail | 27-pin FPC | 24-pin BTB (includes CTP touch pins) |
| Supplies | not published | VCC 3.3 V, **IOVCC 1.8 V**, ELVDD 4.6 V, ELVSS −2.4 V, external |
| Interface | 3/4-wire SPI | SPI4, SDO exposed (mate check F13 possible), TE |
| Docs | product page only; request spec, drawing, init code | **Public**: spec PDF + ESP-IDF driver (`github.com/osptek/amoled-1.1-126x294-spi-icna3306`), saved at `_mech/osptek_AM110Q126294LK1.pdf` |
| Buy | contact vendor (sales) | AliExpress "OSPTEK Official Store" |
| Temperatures | op −20…70 °C; storage not published | storage −30…+70 °C (C-28 warehouse rule applies) |

The report's numbers (12.96 × 30.94 × 0.78, 27-pin, RM69310, 400 nits) are exactly iFan's product page, so that is what the design assumed.

**Decision 2026-09-28: OSPTEK AM110Q126294LK1, with touch** (9-agent panel study: `DISPLAY_PANEL_DECISION_2026-09-28.md`; fallback Brownopto BR138102-A1). Original recommendation: **order OSPTEK samples now** for Mule A bring-up (docs and driver code exist today), and in parallel **request the IF011TPS12-29 full spec + FPC drawing + reference circuit from iFan**. Freeze on whichever has a complete datasheet. The display sheet's connector symbol waits for that decision.

Open item this creates: **IOVCC 1.8 V on the OSPTEK module vs our 3.1 V V3 logic.** Either confirm from the ICNA3306 datasheet that IOVCC accepts 3.1 V, or add a 1.8 V LDO on switch A plus level translation on SCK/MOSI/CS/DC/RESX/TE/SDO. The report's "VDDIO 1.65–3.3 V" is for the RM69310 and is `[V?]`. Also: T95 lifetime is 200 h minimum; fine for glances (≈ 250 s/day ≈ 8 years) but a static creature face should shift pixels.

---

## 10. Drawn sheets — decisions log

Sheets are generated from `tools/sheet_*.py` (library: `tools/schgen.py`, custom symbols: `tools/parts.py`). Regenerate, then run `python3 tools/check.py` (ERC + per-pin netlist). Do not hand-edit generated sheets in KiCad; change the script.

### Sheet 1 `power` — drawn 2026-09-23 (refs 1xx)
- **TPS62840 RSET 71.5 kΩ = 3.1 V confirmed** from SLVSEC6D Table 1 (closes OQ-6); 102 kΩ = 3.2 V if the sensor margin (C-13) needs it. Inductor DFE201210S-2R2M is 1.0 mm tall (meets the ≤ 1.0 mm rule); CIN 4.7 µF / COUT 10 µF 0402 per TI's BOM.
- **No capacitor on TS/MR** (the report's E-15 said 100 nF). The BQ25188 measures the NTC with a *pulsed* current source; TI's typical application has no cap there, and one would skew the reading. R103 10 k DNP is the datasheet's "no NTC" termination.
- **D101 (VBUS ESD) is for a 5 V-only dock.** A TVS cannot both stay off at 9–12 V and clamp below the charger's 25 V abs max, so the design assumes only 5 V heads mate with the pads. Q101 + D102 (12 V gate clamp) protect against reversal.
- **C101 = 2.2 µF 35 V 0603** to keep ≥ 1 µF effective at 5 V and stay under the 10 µF IN maximum (SLUSFJ3 8.2.2).
- **Open-drain pull-ups moved to the nrf9151 sheet** (BQ_INT, GAUGE_ALRT, SDA, SCL) so every pull-up lives next to the MCU.
- **GAUGE_ALRT uses one GPIO** → GPIO budget 27 of 32.
- MAX17048 CELL is not connected internally (it's MAX17049's sense pin); tied to VBAT as in the typical circuit.

### Sheet 2 `nrf9151` — drawn 2026-09-23 (refs 2xx)
- **Pin map verified** from Nordic's nRF9151 PS pin table and cross-checked against the makerdiary nRF9151 Connect Kit schematic (`_mech/nrf9151_connectkit_sch.pdf`, p4-5). Closes OQ-3: **MAGPIO0-2 exist** (pins 21-23), as do COEX0-2 (52-54) and MIPI RFFE (27-29); all unused except COEX0. Nordic's page listed pins 101-104 as GND but the Connect Kit shows them RESERVED; they are left unconnected (safe either way).
- **Decoupling copied from the reference kit:** VDD 10 µF + 1 µF, VDD_GPIO 100 nF + 4.7 µF, DEC0 4.7 µF. ENABLE pulled to VSYS through 10 kΩ. nRESET: no pull-up (Nordic forbids it), test pad only.
- **FB201 0 Ω link** between VSYS and VDD so a PPK2 can measure the nRF alone (the reference kit has a ferrite there).
- **eSIM wired directly** (reference kit U7): pins 8 VCC / 7 RST / 6 CLK / 3 IO / 1 GND, 100 nF on SIM_1V8, no ESD or series parts. Replaces spec §4's "HIG series/shunt filter" plan.
- **COEX0 looped back to P0.29** with a 1 MΩ pull-down so the input is defined before the modem configures COEX0.
- **GPIO assignment frozen for rev A** (sheet block G): SPI/display/NOR on P0.00-07, away from the ANT pin; slow signals (LED gates, DOCK_ID, COEX0) on P0.26-30, nearest the RF side. Spares: P0.18-20 (analog-capable), P0.25, P0.31.
- All open-drain pull-ups live here: SDA/SCL 4.7 kΩ, BQ_INT and GAUGE_ALRT 10 kΩ, all to V3.

### Sheet 6 `dock` — drawn 2026-09-23 (refs 6xx; sheet N uses Nxx)
- **Report E-13's limiter cells revised.** The FET cell stays only on **SWDIO** (the one bidirectional line). **SWCLK and DOCK_ID** go through an **SN74LVC2G34** dual buffer on V3: 5.5 V-tolerant inputs, Ioff (no back-power in ship mode), output can't exceed V3. Reason: the nRF's SWDCLK has an internal pull-down, and a FET cell (gate at V3) only passes V3 − Vth, which leaves a razor-thin logic-high margin against it; adding a pull-up would cost ~175 µA forever. ICC is 10 µA max (datasheet), typically far lower; confirm it on the golden unit (EV-3).
- **TACT read = resistor divider on the power sheet** (R104 470 k / R105 1 M → TACT_NRF, 2.35–2.96 V over 3.45–4.35 V). There is no limiter because TACT_HI is our own VBAT-level net after the BQ25188 change; current flows only while the crown is pressed.
- **ESD: one TPD4E05U06** (4-ch, 5.5 V VRWM, 0.5 pF, 10 nA) at J601 for SWCLK/SWDIO/DOCK_ID; VBUS keeps D101 on the power sheet.
- **Dock-board requirements added:** a ~10 k pull-up from the SWDIO pogo to VTref (the FET cell can't drive the pad high), plus a current-limited 5 V supply, a VTref LDO and a keyed cradle.
- Series 220 Ω on all three signal pads; 1 MΩ pull-downs on the buffer inputs (SWDCLK idles low, like the nRF's internal pull-down).

### Sheet 5 `ui` — drawn 2026-09-23 (refs 5xx)
- **Three I2C buses now (was one):** main (BQ25188, MAX17048, DRV2625, 4.7 k pull-ups on the nrf9151 sheet); **IQS211B on its own bus**, because its TSOT23-6 package has no RDY pin (RDY is signalled on SCL, Azoteq v2.8.1 Table 2.1) and would disturb the shared bus; **angle sensor on its own bus, pulled up to the switched SENS_VDD**, because an unpowered sensor clamps any bus it sits on (closes OQ-10 by design). All 4 nRF9151 serial instances are now used: SPIM (display + NOR), TWIM main, TWIM IQS, TWIM sensor.
- **GPIO 31 of 32:** P0.12 IQS_SCL/RDY, P0.18 IQS_SDA, P0.19 SENS_SCL, P0.31 SENS_SDA, P0.25 HAPTIC_NRST. Spare: P0.20/AIN7.
- **DRV2625 NRST on a GPIO** with a 100 k pull-down: shutdown is 105 nA vs 1.55 µA standby. The report's budget assumed shutdown but gave NRST no pin.
- **IQS211B passives** per Azoteq for the 160 ms scan: 40 Ω supply resistor, VDDHI 2.2 µF + 100 pF, VREG 4.7 µF + 100 pF, Cx 10 pF, 4.7 k pull-ups. The sense series resistor is 2.2 kΩ (report, RF filtering) instead of Azoteq's 470 Ω.
- **MX25R1635F pinout verified from Macronix v1.6:** pin 5 = SI, pin 6 = SCLK (a web summary had these swapped). WP#/RESET# tied to V3.
- **Satellite tail (12-way FH12):** 1 GND, 2 V3, 3 SENS_SDA, 4 SENS_SCL, 5 SENS_VDD, 6-9 HA1/HA2/HB1/HB2, 10 TACT_HI, 11 TACT_SRC, 12 GND. The TACT source resistor (R517, 10 k from VBAT) is on the main board, so a tail short draws ≤ 0.4 mA.
- **Halo:** 10 nF moved to the LED cathode pins (RF decoupling next to the antenna feed); 100 k gate pull-downs added so the LED can't flicker during reset. Common-anode RGB **pin numbering must be checked against the chosen LED's datasheet** (KiCad's LED_RAGB: 1 RK, 2 A, 3 GK, 4 BK; a G/B swap was caught and fixed in review).
- **Open issue for the display sheet:** the SPI bus (SCK/MOSI/MISO) is shared with the NOR, which runs while the display is powered off. An unpowered panel's input/SDO protection diodes would load the bus and back-power the panel, so the report's GPIO-park rule alone isn't enough. Plan: an Ioff buffer powered from the switched panel rail on SCK/MOSI/CS/DC, and SDO left unconnected (TE toggling is the mate check).

### Satellite (crown) board, variant A — drawn 2026-09-23 (`satellite/`, board-local refs)
- **MT6701QT-STD** (QFN-16, MagnTek Rev 1.5 saved in `_mech/mt6701.pdf`): I2C mode by tying **MODE (14) and Z (8) to VDD** (MagnTek Figure 18); SDA = A (6), SCL = B (7); OUT/PUSH/U/V/W unused. C1 100 nF, plus an optional 6 V TVS (DNP) as MagnTek recommends. EEPROM setup needs VDD > 4.5 V, so it's done on a fixture through J1.
- **2 × DRV5032DU** (X2SON: 1 VCC, 2 GND, 3 OUT2 south, 4 OUT1 north, pad → GND): push-pull outputs, 100 nF each, always on from V3.
- **Tact:** TACT_SRC (VBAT through R517 on the main board) → SW1 → TACT_HI. The switch must be rated ≥ 5 V.
- **Crown ESD bleed:** leaf contact E1 → R1 1 MΩ ∥ D2 TPD1E05U06 → GND; the return goes via tail pins 1 and 12.
- **Tail J1 = main J501 pin for pin.** Open item: **FFC type/orientation can reverse pin order** — freeze the cable type (Type A/B) and connector facing on the 3D model before layout.
- Variant B (AS5600L, same tail and magnet) is still to draw; it needs the ams AS5600L datasheet (WLCSP pinout).

### Satellite variant B (AS5600L) — drawn 2026-09-23 (`satellite_b/`)
- Built from the same script as A (`tools/sheet_satellite.py B`); only the sensor block differs, so the tail, latches, tact and ESD bleed are identical by construction.
- **AS5600L-AWLM** (WLCSP-15, ams DS000545 v1-12 saved as `_mech/as5600l.pdf`): **3.3 V mode = VDD5V (A3) tied to VDD3V3 (C3)**, 100 nF; supply range 3.0-3.6 V. **TEST balls A2/C1/E2 → GND** (required). DIR → GND (clockwise-increasing; firmware normalises per variant). PGO open (internal pull-up), OUT unused, NC balls B2/B3/C2/D2 open.
- **C4 10 µF DNP:** ams requires it only during OTP programming (3.3-3.5 V on the fixture).
- 12-bit (0.088°/step) vs the MT6701's 14-bit: ample for 15° detents. **Firmware detects the variant by I2C address: 0x06 = MT6701, 0x40 = AS5600L.**

### Sheet 4 `display` — drawn 2026-09-28 (refs 4xx) for OSPTEK AM110Q126294LK1

Sources: module spec (rendered pages 5-8), ICNA3306 V0.03, CHSC6417 v1.2, TPS65631 SLVSBK1E, TPS22916 SLVSDO5F, TPS7A02 SBVS277C, SN74LVC2G34 SCES359J, SN74LV1T34 SCLS743E, TCA9406 SCPS221G (all in `firmware/bingbong_pcb/_mech/`).
- **IOVCC/TP_IOVCC must be 1.7-1.95 V** (module spec §4 `[V]`). The module's 5.5 V abs max and "VBAT 2.7-4.8 V" page is copied from another product; the ICNA3306's VCI abs max is 3.6 V, so VCC and CTP_VDD stay on V3 via switch A.
- **Rail chain, one GPIO:** DISP_SW_A_EN → U401 TPS7A0218PDQNR EN → V1V8_DISP → U402 switch A ON (VIH 1.0 V) → VCI_SW → U403 switch B ON → PMIC_VIN_SW. This guarantees the ICNA3306's "VDDI before VCI". EN and ON pins have internal pull-downs, so everything is off during MCU reset. Power-off order is "any order" per module spec Fig. 16.
- **PMIC:** U404 TPS65631DPDR with TI's Figure 10 values (2 × 10 µF in, 10 µF VPOS, 2 × 10 µF VNEG, 100 nF CT, 2 × 4.7 µH). CTRL = DISP_PMIC_CTRL (P0.23); 21 edges → −2.4 V. **R401 0 Ω link in ELVSS** so the −4.0 V first ramp can be measured without a panel. The ELVSS abs max is unpublished: ask OSPTEK.
- **Level shifting:**
  - Down: SCK, MOSI, CS, DC, RESX through 3 × SN74LVC2G34 on V1V8_DISP. Ioff/Hi-Z when unpowered also solves the shared-SPIM back-power issue from sheet 5. 33 Ω after the buffers on SCK/SDI. SDO is not connected.
  - Up: TE and CTP_INT through SN74LV1T34 on V3 (VIH 1.39 V max).
- **Touch:** CHSC6417 I²C via U410 TCA9406YZPR onto the main bus (address 0x2E, no clash). **OE = panel RESX**, so the touch side is isolated while in reset (the CHSC6417 forbids bus traffic during Trtp) and Hi-Z when unpowered (its I²C pins load an unpowered bus). CTP_RST shares RESX, with a 10 k pull-down so both are low before power. CTP_INT has a 10 k pull-up to V1V8_DISP.
- **J401:** 24-pin 2x12 BTB, pin map from spec §8. Pin 13 MTP → GND, pin 16 SDO NC. Mating part unknown `[U]`.
- **Open:** mating connector part number and footprint; ELVSS abs max / −4 V tolerance; ELVDD timing vs SLPOUT (spec §13.1.8 contradicts the usual order); 3.1 V IOVCC approval (would delete U401, U405-U410); folded tail stack 3.1-3.3 mm (Z budget); zero spare GPIOs (a polled touch driver would free P0.20).

### Sheet 3 `rf` — drawn 2026-09-23 (refs 3xx)
- **Chain (report §5 topology A, SiP → cap):** ANT_RF → C301 100 pF C0G DC block → J301 MM8130-2600 → R301 0 Ω series spare → trim node (C305/L303 DNP) → C304 3.3 pF series → C303 1.5 pF shunt → L302 15 nH ∥ C302 1.0 pF series → RF_FEED: L301 22 nH to GND (low-band element + DC/ESD return), D301 ≤ 0.3 pF antenna ESD, harmonic trap L304 + C306 (DNP, ~2.1 GHz notch), C307 shunt spare (DNP), TP301 DC test pad → J302 spring finger. **All values are starting points [U]**, to be fixed from Mule B / EVM-1 impedance data.
- **J301 orientation decision: probe → nRF (pin C toward the SiP).** Report §5 Step 12 said "probe → match + antenna", but EV-11 / production need conducted tests of the radio (%XRFTEST), and antenna tuning happens on Mule B (a separate mock). For EVM boards that need match tuning, rotate the MM8130 footprint 180°. The MM8130 footprint must be drawn from the Murata spec drawing (their web sheet has no land pattern).
- 10 matching-network positions = R301, C305, L303, C304, C303, L302, C302, L304, C306, C307; L301/D301 at the X = 63 copper edge.

### Sheet 7 `testpoints` — drawn 2026-09-23 (refs 7xx)
- **39 bottom-side pads** (ø0.9 mm ENIG, ≥ 1.27 mm apart, X = 19-62): VBAT (PPK2 cell-side point), VSYS, V3, 4 × GND; display VCI_SW, PMIC_VIN_SW, ELVDD, ELVSS, DISP_TE, DISP_RESX, DISP_CS, SPI_SCK; debug/buses SWDIO_NRF, SWDCLK_NRF, NRESET, DOCK_ID, SDA/SCL, IQS_SCL/SDA, SENS_SCL/SDA, COEX0; crown/UI HA1-HB2, TACT_NRF, TS_MR, LRA_P/N, LED_R/G/B, BQ_INT, GAUGE_ALRT. The report's E-16 list plus the three new I2C buses and the alert lines.
- **Promoted to global labels so pads can reach them:** TS_MR (power), COEX0 (nrf9151), LRA_P/LRA_N (ui).
- **Display net names fixed here** (VCI_SW, PMIC_VIN_SW, ELVDD, ELVSS): the display sheet must use exactly these.
- Footprint `Bingbong_v3:TestPoint_Pad_D0.9mm_ENIG` is still to be created (KiCad ships only 1.0 mm).

---

## 11. Footprints — status 2026-09-23

Rule: a footprint is added only when every copper, mask and paste number comes from the manufacturer's own land-pattern drawing (or, for a JEDEC outline, a stock KiCad footprint generated from the same JEDEC drawing). Sources are cited inside each footprint (`descr`). Code: `tools/fpgen.py`, `tools/footprints.py`; preview with `tools/fpview.sh NAME`.

**Done (verified):**
| Footprint | Part | Source |
|---|---|---|
| TI_YBG0008_DSBGA-8 | BQ25188 | TI SLUSFJ3 YBG0008-C01 pp.50-52: 2×4, 0.4 pitch, Ø0.23 NSMD, paste □0.25 R0.05 |
| TI_DLC0008_SON-8_1.5x2 | TPS62840 | TI SLVSEC6D DLC0008B pp.36-38: 0.6×0.25 R0.05, 0.5 pitch, columns 1.3 apart |
| TI_YFF0009_DSBGA-9 | DRV2625 | TI SLOS879C YFF0009-C01 pp.72-74: 3×3, 0.4 pitch, Ø0.225, paste □0.25 |
| TI_YFP0004_WCSP-4 | TPS22916 | TI SLVSDO5F YFP0004 pp.24-26: 2×2, 0.4 pitch, Ø0.23, paste □0.25 (checked on the image) |
| TI_DCK0006A_SC70-6 | SN74LVC2G34 | TI SCES359J DCK0006A pp.27-29: 0.9×0.4 R0.05, 0.65 pitch, span 2.2 (replaces the generic SOT-363) |
| TestPoint_Pad_D0.9mm_ENIG | 39 test pads | report E-16 (ø0.9, no paste) |
| Nordic_nRF9151_LGA-113_12.1x11.1 | nRF9151 | Nordic HW Design Guidelines footprint Figs 1-3 + PS Table 1 (screens in `_mech/nrf9151_ps_screens/`). 113 pads, NSMD +0.05, paste per Nordic stencil guidance (large pads ~75 %, C 0.25 x 0.45, D none). Self-check: no copper outside the outline, minimum mask sliver 0.100 mm = Nordic's stated value. Pad B drawn square (chamfer undimensioned). |
| TI_DYA0002A_SOD-523 | TPD1E05U06 (D601-603, sat D2) | TI SLVSBO7O DYA0002A pp.24-26: 0.67 x 0.4 R0.05 at x = +/-0.74 (1.48 c-c), NSMD +0.05, paste = copper. KiCad's stock D_SOD-523 (Diodes Inc. pattern, 0.6 x 0.7 at +/-0.7) differs, so it isn't used. |
| TI_DMR0004_X2SON-4 | DRV5032DU (sat U2/U3) | TI SLVSDC7 DMR0004A pp.35-37, read with the macOS PDF renderer: pads 0.22 x 0.4 R0.05 at x = +/-0.25, y = +/-0.7 ((1.4) is row centre-to-centre), EP 0.8 x 0.6, paste EP 0.76 x 0.57 (90 %). DMR0004B land pattern identical. KiCad's stock X2SON-4 is an older revision and differs. |
| Macronix_USON-8_2x3 | MX25R1635F | IPC-7351B derivation, owner-approved (see below) |
| QFN-16_3x3_MT6701 | MT6701 (sat A U1) | IPC-7351B derivation, owner-approved (see below) |
| ams_WLCSP-15_2.07x2.63_P0.5 | AS5600L (sat B U1) | IPC-7351B collapsing-ball derivation, owner-approved (see below) |
| stock TSOT-23-6 | IQS211B | JEDEC MO-193 AA = Azoteq Table 8.1 outline, pinout matches |

**Blocked, and exactly what unblocks each:**
- **MAX17048 WLP-8 (W80B1+1)** — the datasheet's package table gives outline **21-0555** and, for the land pattern, "refer to Application Note 1891" (Maxim's generic WLP guide). Both redirect to analog.com, which this machine can't reach; the owner needs to supply them. Alternative: the TDFN-8 2×2 version has a real land pattern (**90-0065**) but is ~2.7× the area.
- **Part not chosen yet (footprint follows the MPN):** cell B2B J101, dock flex B2B J601, RGB LED D501, LRA pads J502, antenna ESD D301, MM8130 land (needs Murata's spec drawing), spring finger J302, grip contact E501, crown leaf E1, tact SW1, DFE201210S inductor land (Murata drawing), **display J401 (OSPTEK mate unknown)**.
- **L401/L402 chosen 2026-09-28: Murata DFE252010F-4R7M=P2** (4.7 µH ±20 %, Isat 1.9 A max (L −30 %), Itemp 1.4 A, DCR 240 mΩ max, 2.5 × 2.0 × 1.0 max, spec J(E)TE243A-0012D-01 in `_mech/`). Footprint `L_Murata_DFE252010F` from the spec's p.5 pattern (0.8 × 2.0 pads, 1.2 mm gap). Backups on the same land: DFE252010P-4R7M (1.7 A), Taiyo LSANB2520KKT4R7M (1.3 A), DFE252008U-4R7M (0.8 mm max, 85 °C limit).
- **Display sheet footprints, 2026-09-28:** built from TI land-pattern pages, read on macOS PDFKit renders (poppler drops the fonts on these pages): **TI_DQN0004A_X2SON-4_1x1** (TPS7A02, SBVS277C pp.39-41; chamfered signal pads + 45° 0.48 centre pad, as polygon pads), **TI_DCK0005A_SC70-5** (SN74LV1T34, SCLS743E pp.20-22), **TI_YZP0008_DSBGA-8** (TCA9406, SCPS221G pp.35-37).
- **TI_DPD0012_WSON-12_3x3 (TPS65631): IPC-7351B derivation, owner-approved and built 2026-09-28.** SLVSBK1E has only the outline (4212354/C, thermal pad 4212468/A), no land pattern. Inputs: body 2.90-3.10 (flush terminals), L 0.30-0.50, b 0.15-0.25, e 0.45, 6 leads per side, EP 2.02 × 1.21 ±0.10. Same parameters as the MX25R/MT6701: Z 3.708 → **3.75**, G 2.022 → **2.00**, X 0.185 → **0.20**, giving **12 pads 0.875 × 0.20 at x = ±1.4375**, pitch 0.45, mask +0.05 (0.15 mm slivers). EP land = nominal 1.21 × 2.02 (pad 13 = GND, 0.395 mm to the signal pads), paste 1.0 × 1.75 (72 %). Orientation: the TI top view rotated 90° (1-6 down the left, 12 top-right). Pin map checked against the symbol. Layout: filled or tented GND vias in the EP; keep SWP/SWN loops on the top layer (TI §11).
- **FIX 2026-09-28, TI_DCK0006A_SC70-6 (SN74LVC2G34: U602, U405-U407):** the pads were at x = ±0.65. On DCK0006A p.28 the (2.2) dimension runs between pad **centrelines**, so the pads are now at x = ±1.1. The old footprint would have put the pad heels under the body.
- **Stock but pin order unverified until the MPN is chosen:** SOT-23 (Q101) and SOT-523 (Q102, Q501-503, Q601) MOSFETs use G=1, S=2, D=3; the chosen part must match. SOD-523 diodes (D101, D102, sat D1/D2): check cathode = pin 1 against the chosen MPN.

**Generator bug found and fixed during this pass:** placed custom ICs had an empty footprint field (it overrode the library default), which also hid them from ERC's footprint check. `schgen.place()` now inherits the library footprint.

### nRF9151 PS pages supplied by the owner (2026-09-23), saved in `_mech/nrf9151_ps_screens/`
- **Pin table confirmed from Nordic:** pins 101–104 are RESERVED ("do not connect"), not GND, which settles the earlier conflict. The symbol already has them reserved and unconnected. 31–33 are "connect thermally/mechanically, leave electrically unconnected". The GND list matches the symbol (30 pads).
- **Nordic reference design matches sheet 2:** R1 ENABLE pull-up to VDD; VDD bulk C1–C4 around FB1 (our FB201 position); C5/C6 on VDD_GPIO; C7 on DEC0. **Nordic also shows an optional R2 + C8 on nRESET**, which sheet 2 doesn't have yet; values are in the HIG BOM.
- **Package outline (Figure 1 + Table 1) captured:** D 12.1 × E 11.1 × A 1.156 nom; perimeter pads b 0.7 / b2 0.3, pitch d2 0.5; inner GND pads 1.6 × 1.6 (b3/b4) and 1.6 × 1.95 (c3/c4); small reserved pads 0.2 (b5/c5); D2 11.0, E2 10.0, K–K6 / L–L5 positions.
- **Footprint still blocked:** this is the *package* drawing, not the recommended *land pattern*. It doesn't state whether D2/E2/K/L are pad centres or edges, the corner-pad geometry, or all 24 reserved-pad coordinates, and it has no mask/paste guidance. Needed: the **nRF9151 Hardware Design Guidelines → PCB land pattern / footprint** page (or Nordic's reference-layout files).

- **nRF9151 footprint done 2026-09-23** from the owner-supplied Nordic HW Design Guidelines pages. Assembly notes from the same pages: 80-100 µm stencil, Type 4 lead-free paste, voids ≤ 30 % per pad (not touching the pad edge), reflow per JEDEC J-STD-020D, **no ultrasonic cleaning (it can damage the crystals)**. Still open from Nordic: the R2/C8 values on nRESET (in the HIG BOM).

### Changes 2026-09-23 (owner-approved)
- **Dock ESD swap:** U601 TPD4E05U06 (two package variants, ambiguous stencil) replaced by **D601/D602/D603 = TPD1E05U06DYAR**, one per signal pad (SWCLK, SWDIO, DOCK_ID), each placed right at J601. Same die family and specs (5.5 V VRWM, 0.5 pF, 10 nA). This is one BOM line shared with the satellite.
- **Satellite D2 polarity fix (both variants):** it was wired pin 1 → GND. TI's DYA pin table says **pin 1 = I/O, pin 2 = GND**. Now pin 1 (cathode) → crown node, pin 2 (anode) → GND, drawn with a unidirectional (zener-style) symbol instead of the bidirectional D_TVS.
- The TPD4E05U06 symbol stays in the library but is unused.

### MX25R1635F USON-8 2×3 — IPC-7351B derivation (owner-approved and built 2026-09-23: `Macronix_USON-8_2x3`)
- **Package inputs:** Macronix MX25R1635F v1.6 p.81 (outline only, no land pattern). Cross-checked with Winbond W25Q16JV rev G §11.4 (package code UX, JEDEC MO-220), whose table is identical: body 2.00 × 3.00 (±0.10), b 0.20-0.30, L 0.40-0.50, e 0.50, centre strip 0.20 × 1.60. **Difference:** Macronix adds L1 = 0-0.15 lead pull-back per end.
- **Method:** IPC-7351B flat-no-lead, nominal density: toe 0.30, heel 0, side −0.04, F 0.05, P 0.025; S tolerance RMS-reduced; Z rounded up, G down, X up to 0.05.
- **Check:** with flush terminals the method returns Z 3.75 / G 1.95 / X 0.25 = **exactly KiCad's stock Winbond_USON-8-1EP_3x2mm**, which validates the method and parameters.
- **Proposed (pull-back-aware, covers both vendors):** Z 3.75, G 1.65, X 0.25 → **8 pads 1.05 × 0.25 mm, centres x = ±1.35, y = −0.75/−0.25/+0.25/+0.75**. Pins 1-4 down the left, 5-8 up the right (5 bottom-right, 8 top-right), matching the Macronix pin diagram. NSMD mask +0.05 (0.15 mm slivers), paste 1:1, roundrect r ≈ 0.06.
- **Centre strip:** no copper. Macronix says to leave it floating or at GND and **avoid vias/traces underneath** — a keep-out note goes in the footprint and a layout rule applies.
- **Built and verified:** pads 1.05 × 0.25 at x = ±1.35, read back through the KiCad API; the rule area (no tracks, no vias) over the strip loads as a real keep-out. Terminal coverage is 100 % in 3 of 4 tolerance corners and 95 % in the extreme Macronix pull-back corner (stock footprint: ~65 %). All 8 pins agree across footprint, symbol and the Macronix diagram. Mask slivers 0.15 mm.

### MT6701 QFN-16 and AS5600L WLCSP-15 — IPC derivations (owner-approved and built 2026-09-24: `QFN-16_3x3_MT6701`, `ams_WLCSP-15_2.07x2.63_P0.5`)
**MT6701QT (MagnTek Rev 1.5 §9.2, outline only):** D/E 2.90-3.10, b 0.18-0.30, L 0.30-0.50, e 0.5, exposed pad D1/E1 1.60-1.80 (chamfered pin-1 corner), k 0.275 ref. Sensing centre = geometric centre.
- IPC-7351B (same parameters as the MX25R): Z 3.75 / G 2.00 / X 0.25 → **16 pads 0.875 × 0.25 at ±1.4375** = identical to KiCad's stock QFN-16-1EP_3x3mm_P0.5mm (Linear source).
- **Exposed pad:** the datasheet never mentions it (no pin number, no connection rule). Proposal: **solder it but leave it unconnected (no net)**, which is safe whatever it's tied to inside. **Land 1.5 × 1.5** (below the 1.6 min EP) so the gap to the signal pads is 0.25 mm (at the 1.7 nominal it would be only 0.15); paste 1.1 × 1.1 (~54 %). Add pin "EP" (no-connect) to the symbol.
- Pin order: 1-4 left top→bottom, 5-8 bottom left→right, 9-12 right bottom→top, 13-16 top right→left (bottom view mirrored).

**AS5600L-AWLM (ams DS000545 v1-12 Figure 42):** 5 × 3 balls, pitch 0.50, ball Ø0.329 typ, height 0.232, package 2.07 × 2.63, balls symmetric (0.28 from the long-axis edges). **Hall-array centre is 0.172 mm off the die centre toward row E**; the magnet must be centred on the Hall array, not the package.
- Land: IPC-7351B collapsing-ball rule (~20 % below the ball) → **Ø0.26 NSMD**, mask Ø0.36 (0.14 mm slivers). Bracket: TI's 0.5 mm-pitch practice (land ≈ ball) would give ~0.33. Paste □0.28 R0.05 (TI's ~1.1× land ratio).
- Orientation (from the top-through view): A1 top-left, letters A→E downward, numbers 1→3 rightward; Hall-centre marker at (0, +0.172) on F.Fab. **Satellite layout rule:** align the crown axis with the Hall centre, which is 0.172 mm off the package centre, unlike variant A where the sensing centre is the package centre.
- **Built and verified 2026-09-24:** both footprints read back through the KiCad API.
  - **MT6701:** 16 pads 0.875 × 0.25 at ±1.4375 plus an EP land of 1.5 × 1.5 with no net and 1.1 × 1.1 paste. The corner mask sliver is 0.129 mm and the copper gap 0.229 mm, measured on the true roundrect geometry. The EP-to-pad gap is 0.25 mm.
  - **AS5600L:** min mask sliver 0.14 mm; the Hall cross is on F.Fab at (0, +0.172).
  - **Pin maps:** MT6701 symbol vs the MagnTek list, all 16 agree, and pin "EP" is a no-connect. AS5600L symbol vs the ams Figure 6 ball table, all 15 agree.
  - **Renders:** pin 1 / A1 is top-left on both.
  - **ERC:** both satellite variants regenerate with 0 errors.

## 12. Part selections 2026-09-28 (4 research agents; land patterns re-read by hand on PDFKit renders)

| Ref | Part | Footprint (source) | Notes |
|---|---|---|---|
| U102 | **MAX17048X+T10** (WLP; the old MPN G+T10 is the TDFN) | `MAX_WLP-8_0.9x1.7` (Maxim 21-0555E + AN1891 via archive.org) | Ø0.23 NSMD (AN1891 range 0.20-0.26), 0.25 stencil; bump map matches the symbol |
| L101 | **Murata DFE201210U-2R2M=P2** (DFE201210S is NRND, spec withdrawn) | `L_Murata_DFE201210U` (spec 0029D p.5) | Isat 2.0 A vs TPS62840 1.4 A limit; DCR 228 mΩ (was 155) |
| Q101 | **Diodes DMP3099L-7** | `Diodes_SOT-23` (DS36081 p.5) | −30 V, ±20 V VGS |
| Q102 | **Diodes DMG1012T-7** | stock SOT-523 (= Diodes pattern) | IDSS 100 nA max @ 20 V; **VGS ±6 V vs TACT_HI 4.35 V (1.65 V margin)** |
| D101 | **TI TPD1E10B06DYAR** | `TI_DYA0002A_SOD-523` | now pin 1 = I/O, pin 2 = GND (TI orientation) |
| D102 | **Nexperia BZX585-C12** | `Nexperia_SOD523` (Rev 9 p.11) | pin 1 = cathode → VBUS_IN |
| FB101 | **Murata BLM18PG221SN1D** | `Murata_BLM18P_0603` (JENF243A p.10) | |
| D501 | **Kingbright APTF1616SEEZGQBDC**, symbol now `LED_ARGB` (1 A, 2 R, 3 G, 4 B) | `LED_Kingbright_APTF1616` (DSAJ8681 p.1) | 4.3-8 mA over VSYS 3.45-4.2 V; **top-emitting: kept 2026-10-01 (owner)**; the ring's light stub must end in the 45° facet of report §5 M7 sitting over the LED (the report's "fires +X" text assumed a side-emitter). Side-view fallback below |
| Q501-503, Q601 | **Diodes DMN26D0UT-7** | stock SOT-523 | Vth 0.5-1.0 V, Ciss 14 pF |
| J301 | **Murata MM8130-2600RA2** (RB2 does not exist) | `Murata_MM8130-2600` (O30E pp.5,7,8) | pad C = SiP side, A = antenna side |
| D301 | **Panasonic EZAEG1N50AC** | `Panasonic_EZAEG1N_0201` (AWD0000C13 p.2) | 0.04 pF, 30 V, ±15 kV; clamp up to 500 V peak → V-11 must watch ANT |
| U202 | footprint only: `MFF2_DFN-8_5x6` (Velocity IoT p.4 + ETSI TS 102 671 Table 6.3) | centre pad no net | symbol pinout verified vs ETSI Table 6.1. Candidate **Hologram G3-R-DFN8 (SGP.32)**; alt Kigen SGP.32. Supply-shutdown support still unconfirmed (P0-10) |

**Still open (need a decision or a drawing):**
- ~~J302 spring finger~~ **Decided 2026-09-28 (owner): Harwin S7141-45R** (2.5 mm free, 1.40-1.90 working, 0.49 N min, ≤ 50 mΩ, phosphor bronze + Au flash, −20…+70 °C). **Mechanical change: cap-tab land z = 1.65 mm** (was 1.4) **plus the PCB-referenced 0.05 mm insulating stop** (report §5 Step 6 option), giving worst case 1.42-1.88 (±0.23) and RSS 1.47-1.83, inside the window. Footprint `Harwin_S7141-45R` (CIS iss.5: one 3.30 × 2.80 pad; the part overhangs the pad by 1.65; apex ≈ 3.95 from the pad's left edge [inferred], marked on F.Fab). S7131-45R (2.0 mm free) fits the same land if Mule B (V-3) favours a 1.2 mm land. Open: ask Harwin for the force-deflection curve; the report's finger spec (BeCu, ≤ 30 mΩ) is relaxed to the part's values. Layout: the 4.95 mm overall length must run along Y in the X = 65.5-67.5 allotment.
- **J601 dock:** best fit is Hirose BM28B0.6-6DS/2-0.35V (8 contacts incl. 2 × 5 A power, 0.35 pitch, 0.6 mm mated) → symbol goes 5 → 8 pins; get Hirose CAD before the footprint.
- **J101 cell:** waits on the cell vendor; only Panasonic R35K (AXF5K0412) fits the 3 mm strip.
- ~~E501 grip contact~~ **Decided 2026-10-01 (owner): main board, top-pressed, Harwin S7141-45R** (the J302 part: one reel, footprint `Harwin_S7141-45R` already verified). Würth WE-SECF was the other top-pressed candidate, but every size has a 0.2 mm recommended working window (0825 = 331081302025: 2.0-2.2 working, 2.5 ± 0.2 free; the 1735 is still "Draft"), against 1.40-1.90 for the S7141. Placement: top side in the crown-end strip (X = 16-19.5), on the −y side next to the satellite FFC, so the Cx trace to U501 (X = 24-30, −y) stays short and clear of HA/HB. R504/C505 stay at U501. This supersedes report §7 J8 ("spring finger to the satellite PCB", 2k2/10 pF there), which would need a 13th tail pin. **Mechanical requirements on the ring (tray J8):** a tab from the buried 316L ring that leaves the bulkhead's inner face and runs +X over the board's crown-end edge, with its contact land at **z = 1.65 above the PCB top** (window 1.40-1.90, same tolerance budget as the J302 cap land; the PCB is z-registered on the tray ribs and the ring is moulded into the same tray), **Ni + Au plated at the contact spot** (bare 316L's passive film is a poor low-force contact; an intermittent contact reads as grip noise), and clear of the display tail and the satellite cartridge. **Fallback if the tab can't reach over the board:** Harwin S1941-42R side-pressed against a pad on the wall's inner face, still on the main board; the satellite board only if neither works.
- **J502 LRA pads** (no Vybronics pad spec; ask about an FPC-lead variant).
- **D501 side-emitting fallback (survey 2026-10-01; top-emitter stays the baseline):** **ams-OSRAM KRTB AILMS1-5B5C-B1B12** (Micro SIDELED 3806, full production, ~$0.29): 3.8 × 1.0 × **0.6 mm**, 4-pin common anode (pin 3 = A, 1 = B, 2 = G, 4 = R), Vf @ 20 mA typ/max R 2.2/2.5, G 3.0/3.4, B 3.1/3.5 V `[V]` (Characteristics table, `_mech/osram_KRTB_AILMS1.pdf`), Iv @ 20 mA 690/1749/488 mcd = 4-7× the APTF1616 (110/400/70), MSL3, silicone package (no ultrasonic or wet cleaning). Fit (from the p.20-21 drawings): emitting face at X ≈ 62.94, pads X ≈ 61.75-62.80, Y span 4.4 mm inside the −y halo strip. **Not footprint-ready:** the solder-pad drawing has no body outline and the "Cu area" is undimensioned, so the pad-to-emitting-face relationship is inferred; get ams-OSRAM's STEP model or confirmation first. Optics: the emitting window is only z ≈ 0.07-0.54, so the stub's end face must come down to the PCB. Drive: G 150 → ~220 Ω and B 150 → ~180 Ω to stay ≤ 8 mA at 4.2 V. Runners-up: Inolux IN-S126TASRGB (3.2 × 1.5 × 1.0, fully dimensioned pattern, but a dome lens and G/B Vf max 3.6), TT/Optek OVSRRGBCC3, Lite-On LTST-S310F3WT. Rohm MSL0601RGBU1 is NRND.
- **D501 headroom check needed on the current APTF1616:** green Vf is 3.3 typ / **4.1 max** @ 20 mA (blue 4.0 max) `[V]` (DSAJ8681 electrical table). With only typical curves at 5 mA (≈ 2.85 V), a max-Vf unit at VSYS 3.45 V may leave green near-dark `[inferred]`. The R values on the ui sheet were sized from typical curves. Bench a few parts at 3.45 V on EVM-1, or ask Kingbright for the Vf spread at 5 mA.
- **J401** OSPTEK mating connector.

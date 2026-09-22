# bingbong — ARCHITECTURE DECISION DOCUMENT

**Author:** lead architect
**Date:** 2026-09-12
**Status:** decision, for review. Nothing here is frozen until the three EVM-0 experiments in §10 report.

**A note on provenance before anything else.** Every tag below means something specific:

| Tag | Meaning |
|---|---|
| `[V]` | A primary datasheet or standards document was opened and the number read, by the research pass or a hostile-review pass recorded in this corpus. |
| `[V?]` | Read by one pass, **contradicted or unreproducible** by another. Must be re-confirmed before design-in. |
| `[U]` | Nobody has read the primary source. It is an estimate, a vendor marketing claim, or a distributor parametric field. |

I have not fetched anything new in writing this document. I am arbitrating between passes that did. Where two passes disagree I say which I believe and why, and I budget the pessimistic one.

---

## 1. THE RECOMMENDATION

**Build ENDURANCE, amended: a 27 × 95 × 15 mm sealed polymer capsule with a machined metal end-cap that is also the cellular antenna, an always-on 160×68 reflective landscape screen that costs 20 microamps to leave lit forever, a knurled metal crown at the other end with 24 real mechanical ball detents, and one 8 mm haptic motor whose only job is to render the *other person*.**

The bet is this: **being reachable is the only thing that costs real power, so buy reachability deliberately and spend nothing else.** A boop costs 53 microamp-hours — all 280 boops in a week cost less than the battery's own self-discharge. What costs money is how often the radio wakes up to *listen*. So the device listens slowly (once every 164 seconds) when nothing is happening, and listens fast (every 5 seconds) for three minutes after anyone touches anything. That single trick is 42× cheaper than listening fast all the time, for a latency the user cannot tell apart, because only the *first* message of a conversation can ever be slow. The money we save goes into a screen that never turns off — which is what makes the object feel alive rather than notified — and into surviving the edge of coverage, which is where every standalone-cellular product actually dies.

The second bet, and the expensive one: **the metal end-cap must be a real 700 MHz radiator.** The industry-standard answer (an Ignion chip booster) has no published solution below 824 MHz, and AT&T mandates Band 12 at 699–746 MHz for every IoT LTE device. There is no catalogue part that certifies this product. We therefore own an antenna engineering programme — roughly $30–70k of NRE and 3–5 months — and we find out whether it works in a chamber in month two, not month ten.

---

## 2. WHY THIS OVER THE OTHERS

All three concepts scored 6.5/10 under hostile review, which is the correct score for three documents that each got one big thing right and one big thing wrong.

### What each one got right, and what killed it

**JEWEL** (23.7 cm³ aluminium, coaxial crown, split-band chassis antenna, 330 mAh)

Right: mechanical detents only; never let the actuator render your own input. That is the single best idea in the entire corpus and I have taken it verbatim. Also right: Power Class 5 is free peak-current relief *because the AT&T TRP requirement drops 3 dB in lockstep*.

Killed by: the crown zone does not close. 9.0 mm allocated against an 11.45 mm serial stack, and three components (magnet, angle sensor, 8 mm LRA coin) all demanding the same centreline. Worse, it bonded a 170 Hz permanent-magnet actuator 4 mm from a magnetometer and made "you feel it in the crown" the headline feature — the charm and the measurement were in direct physical conflict. And its sole quantitative justification for the metal shell, "2.8× lower Q_min, therefore +3.2 dB efficiency ceiling," is a misuse of the Chu limit. **Chu bounds Q, not efficiency.** The reviewer reproduced the arithmetic exactly and then correctly refused the inference. That is precisely the failure mode this project's evidence standard exists to prevent, and I will not repeat it anywhere in this document.

**EX** (31.5 × 85 × 16 mm, colour IPS, two actuators, 710 mAh)

Right: filling the mandatory zero-copper antenna keepout with a PMMA light pipe, so the RF tax becomes the most emotive feature of the product. I have taken this, adapted. Also right: performing the 2–6 s cold RRC setup as the creature waking up instead of hiding it behind a spinner.

Killed by: its headline feature does not exist. Phantom tactile motion between two actuators 44 mm apart requires compliantly decoupled contact surfaces; the reviewer computed the first free-free bending mode of the shell at ~2105 Hz, 9–12× above both actuators, so the capsule moves as a rigid body and both LRAs shake the same 52 g identically. The second actuator, its driver, the 44 mm separation and the extra millimetre of Z were all bought against a claim that does not survive the calculation. Separately, its colour TFT at 18 mA cell-side costs 42 mAh/week — more than the entire standing budget of this design — and can only ever be a screen you switch on, which is the pager feeling the whole product is trying to escape.

**ENDURANCE** (29 × 86 × 15 mm, memory-in-pixel, metal end-cap radiator, 620 mAh)

Right: the eDRX escalation exploit (the best protocol idea in the corpus, and it transfers to any silicon). Right: memory-in-pixel reframes a notification into "a thing your partner left on your desk that never expires." Right, and load-bearing: it killed the Ignion NN02-224 on a correct, document-backed reading — the part's published cellular-IoT solution is 824–960 MHz `[V, local DS_NN02-224.pdf]`, and AT&T mandates B2/B4/B12 `[V, local att_trp.txt]`, so that recommendation would have failed certification.

Damaged by: a coverage-search line wrong by ~20×, a square 128×128 display that contradicts the ID brief and forced the body wide, a Z-stack with negative margin, no ESD strategy on two exposed live metal parts, and no recovery path on a sealed object.

### Why ENDURANCE wins anyway

Because **its errors are arithmetic and its rivals' errors are physics.** Every defect the reviewer found in ENDURANCE is fixable with numbers and a millimetre budget. EX's phantom motion is not fixable without a different chassis architecture. JEWEL's crown/LRA/magnetometer collision is not fixable without giving up its headline feature — which is what ENDURANCE had already done.

And ENDURANCE is the only one of the three whose central thesis survives contact with the corrected power budget. Re-run honestly (§5) it lands at **3.5 weeks typical, 1.6 weeks in sustained deep coverage** on a 560 mAh cell. JEWEL corrected lands at 1.45 weeks warm-24/7 and 1.03 weeks with CE-mode repetitions. EX corrected lands at 1.88 weeks typical and 0.99 weeks in fringe coverage. Both of those meet the brief *on paper and nowhere else* — they have no margin left for the coverage-loss case, which is the one unbounded failure mode in any standalone-cellular product.

### The display error that nobody caught, and that buys back the width

EX's document asserts that the 160×68 memory LCD's 25.28 mm active area "needs a 32 mm-wide MODULE and therefore a ~34 mm body," and used that to justify growing to 31.5 mm. ENDURANCE accepted the same reasoning and went to a square panel, which forced 29 mm.

**Both are wrong.** The Sharp LS011B7DH03 outline is 32.0 × 14.0 × 0.745 mm `[V, Display Logic Sharp product table]`. On a stick, the module's **32 mm long axis runs down the length of the stick**, because that is the axis the landscape image runs along. Only 14.0 mm crosses the body width. A 27 mm body with 1.2 mm walls has 24.6 mm of internal width — the module fits with 5 mm to spare.

Consequence: **the recommended architecture honours the brief's 27 mm width exactly.** We spend the growth on length instead, where it is both less objectionable in a pocket and worth real antenna dB.

### What we give up, stated plainly

- **Colour.** One bit, 10,880 pixels, dithering only. The whole colour channel is one RGB LED in the split ring. A creature's face here is line art.
- **Length.** 95 mm against a brief of 80, and against a real NW-E405 at 84.9 mm. That is +19% and it is the most arguable call in this document. I defend it in §6.
- **Sub-minute presence by default.** Mean inbound latency is 82 s cold, 2.6 s inside a conversation window. The first boop of a cold exchange is slow. This is a product decision and the UI must never claim "delivered."
- **A programmable dial.** 24 steel balls in grooves, one texture forever. No firmware update will ever change how it feels.
- **Fingertip haptic crispness.** The actuator lives mid-body, not in the crown, so the boop arrives in the palm rather than the thumb. Paid to keep a 170 Hz magnet away from a magnetometer and a steel can away from the radiator.
- **Any catalogue antenna.** There is no drop-in fallback. See §9.1.
- **GNSS, Bluetooth, Wi-Fi, USB, a microphone, a speaker, PPG, and a phone app.** All dead, most for good reasons, listed in §8.

### Grafts taken from the runners-up

| Taken from | What | Why |
|---|---|---|
| JEWEL | Mechanical detents only; the LRA never renders your own input | Zero latency, zero microamps, zero wear, and emotionally exactly right. Best idea in the corpus. |
| JEWEL (reviewer) | Ceramic Si₃N₄ detent balls; non-magnetic crown with controlled permeability | 440C is martensitic and sits millimetres from the sensing magnet |
| JEWEL (reviewer) | 4-pin pogo: VBUS, GND, SWDIO, SWCLK | Field recovery on a sealed object; PPK2 attach point |
| EX | The RF keepout volume *is* the light feature | Adapted: the polymer split ring the chassis antenna **requires** becomes the illuminated halo. Zero added volume. |
| EX | Perform the cold RRC setup as the creature waking | Turns the one unavoidable curse of standalone cellular into character |
| EX | Mirror-Pet character model; no streaks, no death, no read receipts | Removes the guilt engine and the coercion vector by construction |
| EX | IQS211B true self-capacitance for grip, not Qvar | Qvar is charge-*variation* sensing; a steel crown in a POM journal is a triboelectric generator |
| ENDURANCE (reviewer) | Grow to ~95 mm; AT&T Small Form Factor is anything **under 107 mm** `[V]` | Free certification-class margin and real low-band dB. Do not reach 107: at 107 the B12 requirement jumps to +18 dBm, unachievable. |
| ENDURANCE (reviewer) | Rail at 3.1 V, not 3.0 V | MT6701 minimum supply is 3.0 V; a 3.0 V rail at −2% is out of spec on every unit |
| All three reviewers | PC5 vs PC3 is not a free lunch either way | I reverse JEWEL and EX here and choose **PC3**. See §6.3. |

---

## 3. BLOCK DIAGRAM

```
MECHANICAL (27.0 W x 95.0 L x 15.0 T mm, ~38.5 cm3 bbox / ~34 cm3 radiused, ~48 g)

  x=0                  x=16                         x=71   x=72.5      x=95
  +====================+============================+======+===========+
  | CROWN ZONE 16 mm   | MAIN PCB ZONE 55 mm        |SPLIT | 6061-T6   |
  |                    |                            | RING | END CAP   |
  | 13.0 OD knurled    | PCB 23 x 55, 6L, 0.8 mm    |1.5mm | 22.5 mm   |
  | non-mag crown,     | display module x=18..53    |PC/ABS| = THE     |
  | 6.0 protruding     | LRA + bracket x=55..69     |+ RGB | RADIATOR  |
  | 24 ceramic-ball    | cell 23x43x5.5 BENEATH     |LIGHT | ZERO      |
  | detents, POM       | nRF9151 on TOP under disp  |GUIDE | COPPER    |
  | journal, O-ring,   |                            |HALO  | ON ALL 6  |
  | keyring lug on     | last 8 mm of PCB and the   |      | LAYERS    |
  | the FLANK          | whole cell: >=10 mm from   |      | + NO CELL |
  +====================+ the split ring             +======+===========+
   satellite PCB 22x10 perpendicular, 6-way 0.5 mm FFC        ^
   (angle sensor on-axis, tact off-axis, 2x Hall latch)    spring-finger
                                                            feed, masked
   NON-CONDUCTIVE 28 mm DYNEEMA INTERPOSER between the      Ni/Au pad
   keyring lug and the user's actual keys.  <-- mandatory


ELECTRICAL

  4-pin magnetic pogo dock (5 V, SWDIO, SWCLK, GND)
     |
  [ferrite + 24 V TVS + reverse-blocking FET + dock-presence detect]
     |  IN  (abs max 25 V -- survives the fault it exists to prevent) [V]
     v
  +--------------------+  VSYS 3.45 - 4.35 V   (power path: 1.5 A DC / 2.5 A pulse [V])
  |   TI BQ25180       +---+-------------+-------------+--------------+
  |  power path + chg  |   |             |             |              |
  |  300 mA, JEITA/NTC |   |             |             |              |
  |  /MR <- dial press |   |             |             |              |
  +--+-----------------+   |             |             |              |
     | I2C                 |             |             |              |
  +--v-----------------+   |             |             |              |
  |  ADI MAX17048      |   |             |             |              |
  |  ModelGauge        |   |             |             |              |
  +--------------------+   |             |             |              |
                           |             |             |              |
  560 mAh Li-Po -----------+      +------v------+ +----v-----+  +-----v------+
  PCM trip >=2 A / >=10 ms        | TI DRV2625  | | TPS62840 |  | RGB LED    |
  DC-IR <=150 mOhm incl PCM       | DSBGA-9     | | V3 = 3.1 |  | 3x N-FET   |
  10k NTC bonded to the CELL      +------+------+ | 60 nA IQ |  | + resistor |
  cutoff raised to 3.45 V                |        +----+-----+  +------------+
                                         v             | V3 rail (3.1 V)
                              Vybronics VG0840001D     |
                              8.0 x 4.05, 170 Hz       |
                              on a bracket tied to     |
                              PCB + cell mass          |
                                                       |
  +----------------------------------------+           |
  | Nordic nRF9151-LACA-R                  |           |
  | 12.1 x 11.1 x 1.2 mm LGA  [V]          |           |
  | Cortex-M33, 1 MB / 256 kB              |           |
  | LTE-M Cat-M1, POWER CLASS 3 (23 dBm)   |           |
  | GNSS silicon present, NOT FITTED       |           |
  | VDD <- VSYS directly (3.0-5.5 V) [V]   |           |
  | VDD_GPIO <- V3 (abs max 3.9 V) <-------+-----------+
  +--+---+---+---+---+---+---+-------------+
     |   |   |   |   |   |   |
     |   |   |   |   |   |   +-- GPIOTE/PPI/RTC --> EXTCOMIN (hardware VCOM,
     |   |   |   |   |   |                          runs through deep sleep)
     |   |   |   |   |   +------ SPI0 -----------> MEMORY LCD 160x68  (V3)
     |   |   |   |   |                             Sharp LS011B7DH03 /
     |   |   |   |   |                             Winstar WFM0108A2 (2nd src)
     |   |   |   |   +---------- SPI1 -----------> 16 Mbit SPI NOR    (V3)
     |   |   |   |                                 MCUboot slot1 + art
     |   |   |   +-------------- SIM_1V8 --------> MFF2 eUICC 5x6 DFN-8
     |   |   |                                     SGP.32, supply-shutdown
     |   |   |                                     MANDATORY (contractual)
     |   |   +------------------ I2C0 + GPIO ----> SATELLITE PCB via 6-way FFC
     |   |                                          |
     |   |                                          +- MT6701QT-STD (LOAD-SWITCHED)
     |   |                                          |    on-axis 14-bit absolute
     |   |                                          +- 2x DRV5032DU (ALWAYS ON)
     |   |                                          |    1.6 uA typ / 3.5 max ea [V]
     |   |                                          +- tact SW (off-axis, press)
     |   |
     |   +---------------------- I2C0 -----------> Azoteq IQS211B (V3)
     |                                              electrode = STATIC annular
     |                                              ring on the end-cap shoulder
     |                                              (NOT the rotating crown)
     |                                              + 2k2 series R + 10 pF shunt
     |                                              + TX blanking in firmware
     v
  ANT (single 50 ohm port [V])
     |
  [low-cap TVS <0.3 pF]--[defined DC return]--[5x 0402 high-Q L/C dual-resonant
                                                match: B12 699-746 AND B2/B4
                                                1710-2155 MHz]
     |                        |
     +--> spring finger --> MASKED Ni/Au PAD ON THE 6061 END CAP
     |
     +--> DNP Hirose MHF4 pad  (CHAMBER PROBE ONLY -- see 9.1, this is NOT
                                a production fallback)

  NO aperture tuner in the shipping build.  NO coax.  NO GNSS antenna.
  ONE regulated rail.  ZERO boost converters.
```

---

## 4. BILL OF MATERIALS

Significant parts only. Passives, the matching network and adhesives are lumped.

### 4.1 Silicon

| Function | MPN | Package | Tag | Note |
|---|---|---|---|---|
| Host MCU + LTE-M modem + RF FE + PMIC + crystals | Nordic **NRF9151-LACA-R** (2k reel); `-R7` 500-pc for protos | LGA **12.1 × 11.1 × 1.2 mm** | `[V]` PS v1.0 front matter | **This corrects the corpus's "11 × 12 × 1.0 mm"** — Nordic's marketing page still says 11×12×1, the Product Specification says 12.1×11.1×1.2. Design to the PS. VDD 3.0–5.5 V single supply, runs straight off VSYS. PC3 23 dBm **and** PC5 20 dBm selectable. −108 dBm Cat-M1 low band. **Supply: 16–19 wk factory lead, 0 stock at most houses. Place the 2k reel PO before the schematic exists.** |
| Charger + power path | TI **BQ25180YBGR** | DSBGA-8 1.6 × 1.1 mm | `[V]` SLUSE99C Rev C | IN pin abs max **25 V** — survives the exact charge-port overvoltage it exists to prevent. SYS 1.5 A DC / 2.5 A pulse. **Correction to ENDURANCE:** IQ_BAT is 3 µA typ with pushbutton *disabled*, **4 µA typ with it enabled**, and we enable it for the /MR recovery path. Budget 5.5 µA max. |
| Fuel gauge | ADI **MAX17048G+T10** | WLP 0.9 × 1.7 mm | `[V]` 19-6171 | Needed because current swings 100× (147 µA → 295 mA); a naive voltmeter reads ~60 mV low during every boop, which on the 3.9–3.6 V plateau looks like a 20–40 % SoC collapse. **Caveat nobody flagged:** voltage-based ModelGauge with no coulomb counting is ±15–20 % without a custom battery-model INI from ADI, which means shipping cells to ADI and waiting. The UI shows the creature's sleepiness, not a percentage. |
| 3.1 V rail (the only regulator) | TI **TPS62840DLC** + 1 % ≤200 ppm/°C RSET | SON-8 **2.0 × 1.5 mm** | `[V]` SLVSEC6D Rev D | 60 nA IQ (36 nA VIN + 56 nA VOS typ), 120 nA in 100 % mode, **300 nA shutdown max** (ENDURANCE quoted the 25 nA typ). VIN 1.8–6.5 V, 750 mA. **RSET = 71.5 kΩ E96 → 3.1 V** `[V?]` — the hostile reviewer read this from Table 1; re-confirm at schematic. Layout rule from the datasheet: C(VSET) ≤ 100 pF or the R2D converter mis-reads and sets the wrong output. |
| Haptic driver | TI **DRV2625YFFR** | DSBGA-9 1.498 × 1.361 mm | `[V]` SLOS879C, TI product folder ACTIVE | 105 nA shutdown / 1.55 µA standby vs DRV2605L's 4 µA — 40× on a line that runs 168 h/week. 8.5k at DigiKey. **Do not design in DRV2624** (electrically identical, 1 kB RAM, 0 stock at DigiKey *and* Mouser). |
| Coarse rotation wake, always on | 2 × TI **DRV5032DU** | X2SON 1.4 × 1.1 mm | `[V]` SLVSDC7H Rev H | 3.9 mT, unipolar, push-pull, 20 Hz. **ICC(AVG) at VCC = 3 V is 1.6 µA typ / 3.5 µA MAX** — note the headline 5.2 µA in marketing is the 1.8 V figure for the 80 Hz part. Budgeted at MAX. |
| Fine angle, power-gated | MagnTek **MT6701QT-STD** | QFN3×3-16L | `[V?]` Rev 1.5 read, but the vendor datasheet has mislabelled units and no Western authorised distribution | 14-bit absolute, VDD **3.0–5.5 V**, 10 mA typ / 14 mA max, 1.0 ms power-up, 0.3 mm max off-axis. **Weakest sourcing line in the BOM.** Mitigation in §4.5. |
| Grip / presence | Azoteq **IQS211B00000000TSR** | TSOT23-6 ~2.9 × 1.6 mm | `[V]` v2.8.1 Table 7.2; stock Mouser 14,002 @ $0.40/1, $0.181@1k | 2 µA at 160 ms scan, 77 µA at 9 ms interacting, VDDHI 1.764–3.6 V, Cx ≤ 120 pF. Note this is the **default-OTP `-00000000-TSR`** variant with real dual-distributor stock, not the `-00060000-CSR` the research named. |
| SIM | Generic **MFF2 eUICC**, ETSI TS 102 671, SGP.32-capable | DFN-8 5 × 6 × 0.85 mm | `[V]` footprint; `[U]` specific MPN | **Do not design in Hologram SIM-ST-MFF2 — discontinued at DigiKey.** Design to the generic footprint. **Contractual, not technical:** written confirmation of UICC supply-shutdown support before any reel PO. Nordic's own footnote requires adding 20–60 µA at 3.7 V without it — up to 10 mAh/week, more than the display and both always-on sensors combined. |
| Asset / update flash | 16 Mbit SPI NOR, ≤6 × 5 mm, 1.65–3.6 V (Macronix MX25R1635F class) | USON-8 2 × 3 mm | `[U]` — **nobody has opened this datasheet** | Required: nRF9151 has 1 MB, no XIP, no QSPI. MCUboot slot 1 goes here via Partition Manager `nordic,pm-ext-flash`. Select against live stock at BOM freeze. |

### 4.2 Display

| Function | MPN | Outline | Tag | Note |
|---|---|---|---|---|
| Primary | Sharp **LS011B7DH03**, 1.08 in 160×68 MIP | **32.0 × 14.0 × 0.745 mm**, active 25.28 × 10.744 mm | `[V]` Display Logic Sharp product table; `[U]` the panel's own IVDD1/IVDD2/fCOM table | **Nobody in this corpus has read the LS011B7DH03's own electrical spec.** We are extrapolating from the LS013B7DH03 (20 µA static max, 340 µA dynamic max, fCOM 0.5–30 Hz) `[V]`. That extrapolation is conservative (smaller panel) but it is an extrapolation. Supply: 0 stock, 28-week lead, ship dates in Feb 2027. |
| Second source, same 10-pin FPC | Winstar **WFM0108A2TAJASNN000** | **34.84 × 16.17 × 2.08 mm** per Winstar, **32 × 14 × 2.08** per First Components | `[V]` spec 1st ed. 2025-04-24; **outline disputed** | 5 µA typ / 16.7 µA max hold at 3.0 V. **Mandates fEXTCOMIN 57–70 Hz**, unlike Sharp's 0.5 Hz floor. In stock in singles at ~€19.50@25. |
| Frontlight (stuff option) | Azumo-class frontlight film | ~0.6 mm added | `[U]` — no quote, no part | Reserved in the Z-stack. See §9.7. |

**Mechanical decision:** the display pocket and Z-stack are designed to the **Winstar worst case (34.84 × 16.17 × 2.08 mm)**, the aperture to the **shared active area (25.28 × 10.744 mm)**. Either part drops in. If the Sharp panel is secured, its 0.745 mm thickness returns 1.34 mm of Z, which goes to a 6.5–7.0 mm cell (~700 mAh) or a 13.7 mm body. That is the reward for closing the display source, and it is why §9.2 ranks it third.

### 4.3 Electromechanical

| Function | Part | Tag | Note |
|---|---|---|---|
| Haptic actuator | Vybronics **VG0840001D**, 8.0 dia × 4.05 mm, 170 Hz | `[V]` vendor page | 2.0 Vrms, 68 mA typ / 90 mA max, 1.00 Grms, fall ≤55 ms. **I am reversing ENDURANCE's stated reason for this part.** It quoted "rise 12 ms max" as the decisive number; the hostile reviewer correctly observed that a linear resonator's rise-to-50 % and fall-to-50 % share the same time constant τ = 2Q/ω₀ and **must be equal**. 12 ms vs 55 ms at the same threshold is only possible under overdrive — and overdrive is exactly what the DRV2625's supply compensation suppresses. The real reason to pay 0.8 mm of Z over the VG0832012 is **55 ms free fall instead of 80 ms**, which active braking then has to cut to ~15–25 ms. Prototype the click separation on a real 48 g mass before this is final. |
| Crown | 13.0 mm OD × 8.0 mm, knurled, **non-magnetic grade with a specified max permeability measured after machining**, hard-anodised or PVD | `[U]` | Protrudes 6.0 mm from the end cap. Recessed 0.4 mm radially inside the end-cap shoulder silhouette so it is never the drop impact point. |
| Detents | 24 grooves in a **hardened 17-4PH insert pressed into the crown bore**; 2 × ø0.8 mm **Si₃N₄ ceramic** balls on BeCu leaf springs | `[U]` torque target 2.5–4 mN·m | **Two fixes taken from the JEWEL review.** 303SS is free-machining, sulphur-bearing and soft (~170 HV) — two balls would brinell the grooves inside the life of the gift. And 440C is martensitic and ferromagnetic, sitting millimetres from the sensing magnet. Ceramic balls in a hardened race solve both. Specify 1,000,000 indexes with a measured torque-decay limit. |
| Sensing magnet | ø6.0 × 2.5 mm diametric NdFeB, catalogue part, in the crown hub | `[V]` MT6701 requirement | Concentric to 0.3 mm. Tightest tolerance in the product; it must be held by a moulded/machined feature, not by assembly luck. |
| Press | SMD tact ≥1.6 N, ≥300k cycles, **off-axis**, behind the sealed bulkhead | `[U]` — pull the catalogue | **The axis conflict is resolved by geometry, not by three switches.** The crown + hub + bulkhead translate 0.25 mm as a rigid unit on a 12 mm-long POM journal at 0.06–0.10 mm diametral clearance, which bounds tilt to <0.5°. A single off-axis tact pressed by a boss on the bulkhead therefore cannot cock. **Verify press force is independent of thumb position on the knurl at EVM** — this must be a measured result, not an argument. |
| Charge / debug | 4 × gold-over-**1.0–2.5 µm nickel** pogo pads (VBUS, GND, SWDIO, SWCLK) + weighted magnetic dock | `[V]` EU Directive 2022/2380 Annex Ia is a closed list; keychain wearables absent | **Upgraded from 2 pins per both hostile reviews.** Two pins on a sealed, screwed-shut object with no USB means one bad FOTA bricks a unit permanently, with no RMA reflash and no PPK2 attach point for the sleep-current verification this design demands. Gold *thickness* alone is the classic mis-spec; the nickel diffusion barrier is what survives sweat. Charge current held off until dock presence is detected. Short and reverse protection — a key **will** bridge them. |
| Antenna radiator | Machined **6061-T6** end cap, 22.5 mm, isolated by a 1.5 mm moulded PC/ABS split ring, single spring-finger feed | `[U]` performance | Feed pad is **selectively masked electroless Ni/Au on bare aluminium** — you cannot feed RF through Type II/III anodise, and a gold spring on bare 6061 is a ~1.5 V galvanic couple with gold cathodic. Both catches from the ENDURANCE review. |
| Keyring | Stainless lug on the **flank** of the crown-end housing + **28 mm Dyneema/POM interposer** | `[U]` | Zero axial length. The interposer costs pennies and is the only thing between the chamber result and the field link budget — a 120 g steel key bundle capacitively coupled to the counterpoise end of a 0.22 λ chassis is worth 4–10 dB. |
| Halo | 1 × PLCC-4 RGB, 1.6 × 1.6 mm, common anode to VSYS, 3 × SOT-523 N-FET + resistor, firing into the **polymer split ring as a light guide** | `[U]` MPN | Deliberately **not** an LP5009/LP5012: 10 µA power-save for nothing. Three GPIOs and three FETs cost zero standby. Common anode to VSYS because blue/green Vf exceeds 3.1 V. 8-bit software PWM is adequate here because the halo is a ring, not a display; if banding shows in the breath, move to a hardware PWM channel. |
| Cell | Li-Po pouch **23 × 43 × 5.5 mm, ~560 mAh**, integrated PCM, 10k NTC | `[U]` capacity derived, not quoted | 5.44 cm³ × 0.3796 Wh/cm³ (computed from the `[V]` LiPol LP602248 datapoint: 650 mAh / 2.405 Wh in 6.0 × 22 × 48) = 2.065 Wh = 558 mAh. **Get a vendor quote before believing it.** Specify in writing, because no vendor in this class publishes them: **PCM trip ≥2 A with ≥10 ms delay** (so a 295 mA burst with 35 mA/µs transients never nuisance-trips), **DC-IR ≤150 mΩ including PCM**, IEC 62133-2 and UN38.3 certificates. Connectorised on a 2-pin FPC/ZIF — **not** a JST ACH, which is 2.8–3.2 mm mated and blows the Z budget. |

### 4.4 Parts that MUST be datasheet-confirmed before anyone designs them in

Ranked by how much damage a wrong assumption does:

1. **Sharp LS011B7DH03's own electrical table** — IVDD1, IVDD2, fCOM/fEXTCOMIN floor, and storage temperature. We are extrapolating all four from the LS013B7DH03. Note the LS013's application note gives **Tstg −10 to +60 °C absolute maximum**, far tighter than the family selector's −30/+80, and a keychain on a July dashboard exceeds +60 °C routinely. *This is exactly the class of abs-max oversight that produced the 6 V protection-part failure.*
2. **Winstar WFM0108A2 mechanical drawing for the exact ordering code** — 34.84 × 16.17 × 2.08 vs 32 × 14 × 2.08 is 2.8 mm of width and 1.3 mm of thickness in dispute. Also: the Winstar MIP selector says "Front Light: Yes" while the spec has a 10-pin FPC with **no LED terminals and an empty LED table**.
3. **TPS62840 RSET value for 3.1 V** — read once, by a reviewer, and the rail feeds the display (abs max 3.6 V) and the MT6701 (min 3.0 V). Two abs-max exposures on one unconfirmed resistor.
4. **MT6701QT-STD** — vendor datasheet extracts badly and the electrical table has mislabelled units. Treat every marginal spec with suspicion.
5. **The MFF2 part's supply-shutdown behaviour** — contractual, in writing, before the reel PO.
6. **Panasonic EVPBB or whatever tact is chosen** — Panasonic publishes no operating force, travel or cycle life on the overview page, and a 0.55 mm-tall tact almost certainly has ~0.15 mm travel, not the 0.25 mm the crown is specified to move.
7. **SPI NOR MPN, RGB LED MPN** — placeholders.
8. **Cell energy density** — derived, not quoted.

### 4.5 The MT6701 sourcing hedge

The satellite PCB is a 22 × 10 × 0.6 mm 2-layer board. It costs cents. **Spin two variants of it** — one MT6701QT-STD (QFN3×3-16L), one ams-OSRAM AS5600L (WLCSP 2.07 × 2.63 × 0.60, real Western distribution) — and qualify both against the same FFC pinout and the same magnet. The main PCB never knows which is fitted. This converts a single-source exposure into a $300 NRE item, and it is the cheapest insurance in the whole design.

### 4.6 Cost

**~$62 material per unit at 1k**, plus ~$6 for the dock. I am explicitly re-costing the two lines both JEWEL and EX got badly wrong:

| Line | Naive | Honest @1k |
|---|---|---|
| nRF9151-LACA-R | $16.08@2000 `[V]` | $16.08 |
| Display | $6.54@2240 Sharp `[V]` / €19.50@25 Winstar `[V]` | $9.00 blended, **high variance** |
| 6-layer 0.8 mm main PCB + 2-layer satellite + FFC | "$3.50" | **$7.00** |
| Machined crown assembly (crown, 17-4PH insert, ceramic balls, BeCu springs, journal, O-ring, wave washer, magnet) | "$4.50" | **$9.50** |
| Machined + finished 6061 end cap with masked plated feed pad | "$3.50" | **$6.50** |
| Shells (2), glass lens + OCA, split-ring light guide, brass inserts | — | **$5.50** |
| Cell + PCM + NTC | — | $3.50 |
| MFF2 eUICC | — | $3.50 |
| VG0840001D | — | $2.00 |
| MT6701 / AS5600L | — | $1.50 |
| BQ25180 $1.64 + MAX17048 $1.12 + TPS62840 + DRV2625 $0.81 + 2× DRV5032 + IQS211B $0.18 + NOR | — | $6.00 |
| Passives, matching network, TVS, pogo, adhesives, aura | — | **$4.00** |

At 10k expect ~$48–54. **Excludes** ~$30–70k antenna NRE, ~$18–30k shell tooling, ~$8–15k chamber, and PTCRB + FCC/CE + AT&T + Verizon Open Development at **$50–150k** — a line both JEWEL and ENDURANCE listed without a number.

---

## 5. POWER BUDGET

### 5.1 The assumption everything rests on

**Baseline eDRX 163.84 s → mean inbound latency 82 s.** On any interaction (you boop, or a boop arrives, or the grip sensor fires), the modem drops to **eDRX 5.12 s for 180 s → mean inbound latency 2.6 s.** Twelve such windows per day.

This is the ENDURANCE exploit and it is the single best idea in the corpus. Flat eDRX 5.12 s costs **345 mAh/week** and is impossible at any cell size that fits this body. Twelve 180-second windows cost **8.2 mAh/week** for the same felt latency *inside a conversation*, because only the very first boop of a cold exchange can ever be slow.

**The idle-current model:** `I_idle = 2.7 µA + 10,499/T µA`, back-solved from Nordic's field measurement of 132 µA at eDRX 81.2 s on a live network. Sanity check: the model returns 130.9 µA at 81.92 s, 1 % from measured. At 163.84 s the model returns 66.8 µA but Nordic **measured** 92.6 µA, so I budget 92.6 — 39 % conservative on the largest line in the design.

**Honest caveat on that number.** Nordic's own Product Specification says eDRX @ 81.92 s = **18 µA** Cat-M1, UICC included `[V]`. The field figure is 7× higher and the ENDURANCE reviewer could not locate its source. I budget the field figure because it errs safe — but the reader should know that the biggest line in this table rests on a measurement I cannot point you to. §10 fixes this with a PPK2.

### 5.2 The modelled day

20 boops sent, 20 received, 5 petting sessions initiated + 5 received (20 s each), 50 display-wake interactions of 15 s, 24 periodic TAU, 2 cold re-attaches. **AS-RAI assumed NOT granted.** Where a datasheet publishes a MAX, I budget the MAX.

**Cell: 560 mAh nominal × 0.81 = 454 mAh usable.** Derate = 0.90 (nRF9151 RF is specified only down to VDD 3.3 V; 3.0 V is survival, and see §5.5 on the cold-temperature droop) × 0.90 (ageing + temperature).

#### A. Standing load, 168 h

| Line | Current | mAh/wk | Tag |
|---|---:|---:|---|
| nRF9151 modem, eDRX 163.84 s | 92.6 µA | 15.56 | `[V?]` field-measured, source unlocated |
| nRF9151 app core, System-ON idle + RTC | 2.2 µA | 0.37 | `[V]` |
| Display static, IVDD1 MAX | 20.0 µA | 3.36 | `[V]` LS013 max, extrapolated to LS011 |
| EXTCOMIN generation (RTC→PPI→GPIOTE domain) | 2.0 µA | 0.34 | `[U]` |
| Idle "breathing" animation, 40 µA for 90 min/day | 2.5 µA | 0.42 | `[U]` — **see note** |
| 2 × DRV5032DU @ 3 V, ICC MAX 3.5 µA each | 7.0 µA | 1.18 | `[V]` |
| IQS211B grip, 160 ms scan | 2.0 µA | 0.34 | `[V]` |
| DRV2625 standby, MAX | 2.0 µA | 0.34 | `[V]` |
| BQ25180 IQ_BAT, **pushbutton enabled**, MAX | 5.5 µA | 0.92 | `[V]` |
| MAX17048 hibernate, MAX | 5.0 µA | 0.84 | `[V]` |
| SPI NOR deep power-down | 1.0 µA | 0.17 | `[U]` |
| TPS62840 IQ + pull-ups + board leakage | 5.0 µA | 0.84 | `[U]` |
| **Standing subtotal** | **146.8 µA** | **24.68** | |
| Cell self-discharge, **4 %/month** on 560 mAh | — | 5.20 | `[U]` |
| **A. STANDING TOTAL** | | **29.88** | |

> **The breathing-creature line is the one ENDURANCE missed and I have put back.** Its 20 µA display line assumed a *still image*. A creature that breathes needs CPU wakes: a 4 Hz idle animation costs ~40 µA all-in, which run 24/7 would be **6.7 mAh/week — doubling the standing budget**. The resolution is architectural, not arithmetic: **the creature only animates when a human is present.** The IQS211B grip bit or the DRV5032 pair or a recent event gates it; otherwise the panel holds a static frame at 20 µA. Budgeted at 90 min/day. This is a firmware requirement with a hard number attached, not a polish item.

#### B. Event load

| Line | Basis | mAh/wk | Tag |
|---|---|---:|---|
| eDRX escalation, 12 × 180 s/day to 5.12 s | Δ1960 µA × 2160 s/day | 8.23 | model |
| 40 boops/day, **no AS-RAI**, 191 mC = 53.1 µAh each | | 14.87 | `[V]` Nordic |
| 10 petting sessions/day × 20 s RRC-connected **@ 50 mA** | | 19.44 | `[U]` — reviewer's correction from 35 mA |
| App core awake: 750 s display + 200 s petting + 120 s boops @ 4 mA | 1070 s/day | 8.32 | `[U]` |
| Display dynamic, IVDD2 340 µA MAX, 950 s/day | | 0.63 | `[V]` LS013 max |
| Haptics: 1220 clicks/day × 30 ms @ 68 mA | | 4.84 | `[V]` actuator |
| Haptics: purr 100 s/day @ 35 % amplitude (≈8.3 mA, V² scaling) | | 1.61 | `[V]`+`[U]` |
| MT6701 gated on, 10 × 25 s/day @ 14 mA MAX | | 6.81 | `[V]` |
| Periodic TAU, 24/day **@ 0.5 J** | 37.5 µAh each | 6.30 | `[U]` — reviewer's correction from 105 mJ |
| Cold re-attach, 2/day **@ 5 J** | 375 µAh each | 5.26 | `[U]` — reviewer's correction from 0.98 J |
| **Coverage search governor allowance** | | **20.00** | `[U]` — **see note** |
| Aura: 40 blooms + 20 min/day breath | | 1.15 | `[U]` |
| FOTA allowance, 1 × 200 kB delta/month | | 0.50 | `[U]` |
| **B. EVENT TOTAL** | | **97.96** | |

> **The coverage-search line is where ENDURANCE was wrong by ~20× and it is the most important correction in this document.** It budgeted "30 min/week @ 1.72 mA = 0.86 mAh/wk". An nRF91-class modem doing PLMN/cell search runs its receiver at tens of milliamps, and a pocket-carried keychain loses coverage *daily* in garages, lifts, building cores and transit. The reviewer's fair figure is 15–20 mAh/wk; pessimistic is 28. **I budget 20, which makes it the second-largest single line in the design.** It is also the only genuinely unbounded failure mode: a modem that cannot find a cell and does not back off draws 1.72 mA continuously and flattens this cell in 11 days. §9.6.

#### Total

| | mAh/wk |
|---|---:|
| A. Standing | 29.88 |
| B. Events | 97.96 |
| **TOTAL** | **127.84** |

**454 mAh usable / 127.84 = 3.55 weeks.** Round to **3.5 weeks typical.**

### 5.3 Sensitivities

| Scenario | mAh/wk | Runtime |
|---|---:|---:|
| **Nominal** (eDRX 163.84 s baseline, AS-RAI refused) | 128 | **3.5 wk** |
| AS-RAI granted (boops 191 mC → 24.3 mC) | 115 | 3.9 wk |
| Network grants only eDRX 81.92 s (latency halves to 41 s) | 134 | 3.4 wk |
| eSIM without supply shutdown (+40 µA) | 135 | 3.4 wk |
| Heavy user: 2× all interaction | 190 | 2.4 wk |
| **Network refuses eDRX → PSM + 300 s poll** (latency 150 s) | 227 | **2.0 wk** |
| **Sustained CE Mode A/B deep coverage** (4× connected-mode energy, 2× search) | 285 | **1.6 wk** |
| Compound: no eDRX **and** sustained deep coverage | ~600 | **0.8 wk — FAILS** |

The compound case does not meet one week **at any cell size that fits this body**, and I am not going to pretend otherwise. The mitigation is behavioural and must be specified: in sustained deep coverage with no eDRX grant, the device lengthens the poll interval to 900 s, stops animating, and tells the user through the creature that it is sleeping deeply. That is an honest degradation, not a fudge, and it needs to be in the requirements document with those numbers.

### 5.4 The one genuinely fatal mode

If the network denies **both** eDRX and PSM and parks the device in idle DRX at 1.28 s, current is ~8.2 mA and the product is **dead in 2.6 days**.

Firmware must read back `+CEDRXRDP` and `+CPSMS` after every attach and, if neither is granted after N attempts, **detach and fall back to RTC-scheduled polling**. Never leave the modem in operator-chosen idle DRX. This is a release gate, tested in a shielded box against a base-station simulator configured to refuse both.

Second gate: Qoitech measured **+600 µA on an nRF9151 simply from leaving the debug UART enabled in sleep** `[V]`. That is 100 mAh/week — 78 % of the entire budget, from one build flag. The console UART must be compile-gated out of the production image; debug is SEGGER RTT over the SWD pogo pins. Verified with a PPK2 capture on the golden unit, every release.

### 5.5 Burst current — and the argument ENDURANCE got wrong by 70×

Worst simultaneous: PC3 TX 295 mA + haptic 90 mA + housekeeping 10 mA = **395 mA = 0.71C** on a cell rated 1C continuous.

ENDURANCE wrote "on a linear power path the bulk cap is what actually services that burst." **That is wrong.** 44 µF over a 1 ms LTE-M TX subframe at 295 mA gives ΔV = 6.7 V. To hold 100 mV you would need ~3000 µF. The capacitors handle the **35 mA/µs edges**; the millisecond subframe is serviced by the cell through the BATFET (90 mΩ max `[V]`) and the cell's DC-IR.

At 0 °C, cell IR ≈ 375 mΩ + 90 mΩ BATFET × 395 mA = **181 mV droop**, putting VDD at ~3.12 V against the SiP's 3.0 V hard floor if the cutoff is 3.3 V. **Brownout during TX at low temperature is a credible field failure** and the 0.90 "RF floor" derate was being asked to cover it silently.

Fix: **discharge cutoff raised to 3.45 V**, DC-IR specified at ≤150 mΩ including PCM, and the actual droop measured at 0 °C on a real cell with a real 295 mA burst before the 0.81 derate is trusted. Decoupling per Nordic's HIG: 4.7 µF + 100 nF at the SiP, 2 × 22 µF 0805 bulk on VSYS **mounted bottom-side beside the SiP** (they are 1.45 mm tall and will not fit the 0.70 mm top-side budget).

### 5.6 Charge and thermal

300 mA (0.54C) → ~2.1 h CC + ~0.4 h CV = **~2.5 h full charge**, against v1's 5.35 h. Dissipation 0.3 A × (5.0 − 3.7) = 0.39 W; body surface 2(27×95 + 27×15 + 95×15) = 90.3 cm²; at h = 10 W/m²K that is a **4.3 K rise**. Thermal has real slack — but h = 10 is a still-air textbook figure and a trouser pocket is not still air. JEITA throttling against an NTC **bonded to the cell, not the PCB**, is mandatory; charging a Li-Po below 0 °C is prohibited.

---

## 6. MECHANICAL

### 6.1 Envelope

**27.0 W × 95.0 L × 15.0 T mm** = 38.5 cm³ bounding box, ~34 cm³ as a 4 mm-radiused capsule, **~48 g**.

| Reference | W × L × T | Volume |
|---|---|---|
| Brief target | 27 × 80 × 15 | 32.4 cm³ |
| Real Sony NW-E405 | 28.8 × 84.9 × 13.9 | 34.0 cm³ |
| **This design** | **27.0 × 95.0 × 15.0** | 38.5 cm³ bbox |

**Width and thickness are exactly the brief.** Length is +19 % over the brief and +12 % over a real Walkman. I am spending it on one thing: an antenna that can certify.

Why 95 and not 86: at 722 MHz, 86 mm is 0.18 λ and 95 mm is 0.22 λ, and low-band radiation resistance climbs steeply through that region. AT&T's Small Form Factor class is **anything under 107 mm in the longest direction** `[V, local att_trp.txt]`, so the length is free in certification terms. **Do not reach 107 mm** — at 107 you fall into Table 3 and the B12 requirement jumps from +10 to +18 dBm, which is unachievable in any version of this object. 95 mm leaves 12 mm of headroom to absorb tooling growth and the antenna Plan B in §9.1.

### 6.2 Millimetre budget

**Length (95.0 mm):**

| x | Zone | mm |
|---|---|---:|
| 0–16.0 | **Crown zone.** Crown protrusion 6.0 + journal/hub 2.0 + press travel 0.25 + wave washer & bulkhead 1.25 + magnet-to-sensor gap 1.3 + satellite PCB 0.6 + tact/component height 2.6 + tolerance 2.0 | 16.0 |
| 16.0–71.0 | **Main PCB zone.** PCB 23 × 55 × 0.8, 6 layers. Display module x = 18–53. LRA + bracket, top side, x = 55–69. Cell 23 × 43 × 5.5 beneath, x = 24–67. nRF9151 **on the top side under the display**. | 55.0 |
| 71.0–72.5 | **Split ring**, moulded PC/ABS, doubles as the halo light guide | 1.5 |
| 72.5–95.0 | **6061-T6 end cap = the radiator.** Zero copper on all six layers for the last 8 mm of PCB; no cell, no fastener, no metal within 10 mm of the split ring. | 22.5 |

**Note on the crown zone:** JEWEL's 9.0 mm crown zone failed because it put the 4.05 mm LRA coin on the same bulkhead and the same centreline as the magnet and the sensor. Moving the LRA to mid-body removes 4.05 mm at a stroke and de-conflicts the axis. The remaining stack is magnet (inside the hub, zero marginal length), sensor on-axis, tact off-axis. 16.0 mm closes with 2.0 mm of tolerance. That is the JEWEL failure fixed by the ENDURANCE topology.

**Thickness (12.6 mm internal behind 1.2 mm walls), per column:**

| Layer | Battery column | SiP column |
|---|---:|---:|
| Chemically strengthened glass lens | 0.50 | 0.50 |
| OCA | 0.15 | 0.15 |
| Frontlight film (reserved) | 0.60 | 0.60 |
| Display module (**Winstar worst case**) | 2.08 | 2.08 |
| Air / foam | 0.20 | 0.20 |
| FPC (**soldered directly, no ZIF**) | 0.60 | 0.60 |
| Top-side components | 0.70 | **1.35** (nRF9151 + solder) |
| PCB | 0.80 | 0.80 |
| Insulator | 0.15 | — |
| Cell | 5.50 | — |
| Swell gap | 0.60 | — |
| **Total** | **11.88** | **6.28** |
| **Margin in 12.6 mm** | **0.72** | 6.32 |

Two fixes taken from the hostile reviews are load-bearing here: **bulk 0805 caps go bottom-side** (1.45 mm tall, will not fit 0.70 mm) and **the display FPC is soldered, not ZIF'd** (a 180° fold on 0.5 mm-pitch polyimide needs ≥1.0 mm and a ZIF body adds 0.9–1.2 mm). With them, the stack closes with 0.72 mm. Without them it is negative, which is exactly where all three source concepts were.

**If the Sharp 0.745 mm panel is secured, 1.34 mm returns** → a 6.5–7.0 mm cell (~700 mAh, pushing typical runtime to 4.4 weeks) or a 13.7 mm body. Closing the display source is the highest-return mechanical action available.

**Undeclared item I am declaring:** a 13.0 mm crown in a 15 mm body protrudes **6.0 mm axially, not radially** — it sits inside the 15 mm silhouette. The object still passes through a 15 mm slot. JEWEL's 12.6 mm coaxial crown in a 13.0 mm body left 0.2 mm per side with nowhere to land an O-ring; 13.0 in 15.0 leaves 1.0 mm per side for the end-cap shoulder and the labyrinth seal.

### 6.3 Antenna strategy

**The gate, corrected.** AT&T IoT Radiated Performance Requirements v1.8, Table 4, Small Form Factor LTE-M `[V, local att_trp.txt]`:

- **B12 (699–746 MHz): +10.0 dBm TRP at PC3, +7.0 dBm at PC5.** TIS −85 dBm.
- **B2 and B4: +12.0 dBm TRP each.** All IoT LTE devices are **required** to support B2, B4 and B12.

ENDURANCE computed the required efficiency as 5.62 % (23 dBm − 0.5 dB feed − 10.0 dBm = 12.5 dB). **That is optimistic on three axes** and the hostile reviewer's correction stands:

| Term | ENDURANCE | Corrected | Why |
|---|---:|---:|---|
| Conducted design power | 23.0 dBm | **21.5 dBm** | 3GPP ±2 dB plus band-edge MPR |
| Feed + match loss | 0.5 dB | **2.0–2.8 dB** | A 5-element high-Q match into Rr ≈ 5–12 Ω, Xa ≈ −j120 to −j250 Ω has network Q of 20–40; 0402 inductors at Q 45–60 give η_match = 1/(1+Q_net/Q_comp) = 0.53–0.72 |
| Certification margin | 0 dB | **2.0 dB** | Channel spread, unit spread, temperature, lab-to-lab |
| **Required total efficiency @ B12** | 5.62 % | **12.3 %** | |

**The honest estimate of what a 22.5 mm cap on a 23 × 55 mm ground plane achieves, loaded by an aluminium-laminate cell, FR4, PC/ABS, glass, a steel LRA can and a metal crown, is 8–18 %, centred ~12 %.** The gate and the estimate are the same number. **Design target 15 %.**

**Power Class: PC3 (23 dBm), not PC5. I am reversing JEWEL and EX here.** Their observation is correct and sharp — PC5 gives free peak-current relief *because the TRP requirement drops 3 dB in lockstep*, so it costs nothing in certification margin. But it is the wrong call for *this* antenna. With a 12 % antenna the device will spend real time in CE Mode A/B, where repetitions multiply time-on-air and energy **linearly**. 3 dB of absolute link margin buys fewer repetitions, and in the deep-coverage stress case repetitions are worth 157 mAh/week — far more than the 85 mA of peak current PC5 would have saved, which we handle with DC-IR and bulk capacitance anyway. **Antenna efficiency and the power budget are the same problem**, and that is the insight neither JEWEL nor EX joined up.

**What I will not say.** I am not going to justify the metal cap with the Chu limit. Both JEWEL and ENDURANCE derived "+3.2 / +4.5 dB of efficiency ceiling" from Chu/McLean, and both reviewers independently showed the derivation is invalid — **Chu bounds Q, not efficiency**; a small antenna can be 100 % efficient if it is narrow enough, and adding loss actually *buys* bandwidth. The reviewers reproduced the arithmetic exactly (ka = 0.636, Q_min = 5.46, FBW = 12.9 %) and refused the inference. They were right. The metal cap is justified by **radiation resistance and current distribution on a physically larger radiating structure, and by a chamber measurement** — not by a bound on Q. Chu's *legitimate* contribution here is narrower and still useful: on a 23 × 55 mm PCB ground alone the usable instantaneous bandwidth is ~48 MHz against B12's 47 MHz span with practical Q running 2–3× Q_min, which is why a single broadband low-band resonance on the bare board is not available. That is a bandwidth argument, and it is the only one Chu supports.

**Keepout, specified as a volume not a copper rule:** zero copper on all six layers for the last 8 mm of PCB; **no cell within 10 mm of the split ring**; no metal fastener, no display tail, no LRA can, no steel keyring in the 22.5 × 27 × 15 mm cap volume or the 8 mm buffer.

**Unmodelled conductors that must go into the EM solver from day one:** the metal crown (a floating parasitic at the counterpoise current maximum, with a hand on it), the LRA's steel can, the aluminium-laminate cell, and the IQS211B's annular electrode. The last one is also an RF *victim*: a large floating electrode near the counterpoise will rectify a 23 dBm TX burst, so the grip channel needs a 2k2 series resistor, a 10 pF shunt, and **TX blanking in firmware**. None of the three source concepts had any of this.

**ESD, which none of them had either:** the cap is exposed, hand-touched, galvanically fed metal going into the nRF9151 ANT pin. It needs a <0.3 pF TVS and a defined DC return. The crown is floating metal over a capacitive electrode and needs the same treatment on the sense line.

### 6.4 Sealing, drop, service

- The crown runs a **0.15 mm visible labyrinth clearance** into a 0.6 × 1.5 mm annular debris chamber, with a greased 1.0 mm silicone O-ring on the hub behind it. Nothing but magnetic flux crosses the moulded bulkhead. Over years the chamber fills; design so accumulated lint cannot bridge to the O-ring.
- **0.50 mm chemically strengthened glass lens, OCA-bonded** into the aperture, so the panel's own glass is never the outer surface. At ~48 g a 1.5 m drop is 0.71 J.
- **Rear shell on 2 × M1.4 torx into brass heat-set inserts, under the crown end cap. Cell on a connector, never soldered.** This keeps EU Regulation 2023/1542 Art. 11 (in force 18 Feb 2027) a legal question rather than a shell redesign. See §9.9.
- **LRA on a bracket tied to the PCB and the cell mass**, not to the rear shell — the ENDURANCE reviewer is right that a hollow gloss capsule driven at 170 Hz off its own shell is an acoustic radiator, and a "silent, intimate" boop audible across a quiet room is a product failure. Measure acoustic output at 170 Hz in an anechoic box before ID sign-off.

---

## 7. THE INTERACTION

### 7.1 Your own petting — no firmware is in this loop

Your thumb and forefinger take the 13 mm knurled cylinder protruding from the end of the stick and turn it. Every 15 degrees — 1.70 mm of knurl travel — two ceramic balls drop into a groove in a hardened race. Twenty-four soft catches per revolution at 2.5–4 mN·m, damped by a greased O-ring so the crown has glide and weight and coasts about a third of a turn before stopping. It does not free-wheel like a fidget spinner and it does not rattle in a pocket.

**Every one of those detents is mechanical. Zero milliseconds, zero microamps, no firmware in the loop, and they still work with a flat battery.** This is JEWEL's best idea and I have taken it whole: *I will not let an LRA render your own detents; 12 ms of rise is 12 ms too many when your own finger caused it.*

Underneath, the MT6701 reports **absolute** angle to better than 0.02° at 100 Hz, so what your partner receives is a continuous velocity curve, not a click count. The felt resolution and the transmitted resolution are deliberately decoupled. The IQS211B sees your hand land on the static electrode ring 200–500 ms before the thumb moves and has already powered the encoder, so the first millimetre is never lost. Gloved or dry hand: the two DRV5032DU latches catch the rotation within 90°. **The wheel is never dead, only occasionally coarse for a quarter turn.**

Press the crown inward 0.25 mm against a conical wave washer onto a real tact dome. That is a boop. It is a snap, not a synthesis.

### 7.2 A boop, sent and received

**Sent:** the creature on the 25.28 × 10.744 mm landscape screen looks up within ~15 ms. That is local; no radio is involved, so it never lags. Then, if the modem was cold, the creature **stretches** — a deliberate 2–6 second wake animation that *is* the RRC connection setup, performed rather than hidden behind a spinner. This is EX's idea and it is the best available answer to the one unavoidable curse of standalone cellular. When the network acknowledges, one 30 ms braked tap lands in the palm and the creature settles. The UI says "sent". **It never says "delivered" and it never says "read".**

**Received:** one 150 ms pulse at 170 Hz, 1.00 Grms into a rigid ~48 g capsule rather than the 100 g inertial sled the datasheet is measured on — a low, round thump through the whole body. Simultaneously the split ring blooms warm over 400 ms, which is the only channel that works when the device is face-down in a pocket. The arrival then **stays on the screen indefinitely with no timeout**, because a memory-in-pixel panel costs 20 µA to keep showing it. That is the detail that makes the object feel alive rather than notified: it is not a notification that expires, it is a thing your partner left on your desk.

**bingbong, the sound the device does not make:** the boop waveform is two transients — one overdrive cycle at 170 Hz, 18 ms of braked decay, a 40 ms gap, then a second softer transient at 60 %. *BING… bong.* The 40 ms gap is why it reads as a word instead of a buzz. It is also why the product can be named what it is named without having a speaker.

### 7.3 Their petting

Their device emits, per detent, `{seq, cumulative_count, direction, inter-detent Δt[], grip_flag}`, coalesced to ≤10 pkt/s over **UDP/DTLS — never TCP**, because one retransmit stalls a caress for 1–2 s. Cumulative counts mean a lost packet self-heals on the next one: latest-state-wins, not an event stream.

Your device replays it through a **150 ms de-jitter buffer that restores their rhythm, not the network's**. Contract: their detent → your click ≤250 ms typical, 400 ms hard ceiling, from ITU-T G.114's conversational budget `[V]`. A mirrored caress is a social event between two people, so the conversational budget governs — **not** the 45–65 ms cross-modal window, which governs your own self-caused feel and would send the team chasing an impossible latency.

Three regimes on one actuator:

- **Slow (<8 detents/s):** discrete clicks. ~30 ms envelope with DRV2625 active braking fighting the 55 ms free fall. Individual, correctly spaced touches. A hand moving deliberately.
- **Fast (>12–15/s):** clicks stop being resolvable — that ceiling is real and we do not fight it. The firmware **crossfades into a purr**: the 170 Hz carrier held at steady amplitude under a 20–30 Hz envelope whose depth and rate track their speed. That construction is literally what a cat's purr is: a carrier in the Pacinian band (peak sensitivity 250–300 Hz) under an envelope in the Meissner band (20–30 Hz). Add ±10 % slow pseudo-random jitter on depth and ±5 % on rate — a perfectly periodic envelope reads as a machine, a slightly irregular one reads as a creature.
- **They stop:** the purr decays over ~600 ms with a slight downward slide. It feels like a breath being let out.

Sessions auto-taper from 15 s and hard-stop at 20 s. That is a power rule dressed as an emotional one: petting is precious and it ends.

**A single actuator, not two.** EX's travelling purr across two actuators 44 mm apart is dead: the shell's first bending mode is ~2105 Hz, 12× above the carrier, so the capsule moves as a rigid body and both actuators shake the same mass identically. You would feel amplitude and spectral change, not localisation. Two-point vibrotactile localisation needs compliantly decoupled contact surfaces, which an OCA-bonded, screwed-shut IP67 monolith specifically does not have.

### 7.4 Presence

The IQS211B gives a stable DC "held" bit within 160 ms from an annular electrode on the **static end-cap shoulder** — not behind the rotating crown, because a steel crown in a POM journal is a textbook triboelectric generator and rotation-induced charge would swamp grip detection during exactly the interaction it is meant to accompany. Your thumb bridges the crown and the shoulder as a matter of course.

When they are holding theirs, your creature leans in. When they let go, it settles.

**Presence is architectural, not a settings screen.** Ephemeral, held in server RAM only, never logged, no duration, no "last seen", no history API, and **strictly reciprocal** — you see theirs only while yours is visible. **No read receipts, ever:** "arrived", never "they saw it". No delivery-failure alert to the sender that can be cited as evidence of non-compliance. Server-side boop rate limiting (~30/hour, coalesced) as a protection. Unbond is unilateral, instant, from the device, wipes local content, and **presents to the other device as the same neutral "away" state as a flat battery** — announcing "you have been blocked" escalates danger.

These are refusals, not toggles, because the coercion model is demand + threat + **surveillance of compliance**, and presence data supplies exactly that third leg. Ship with presence OFF, boops ON.

### 7.5 The character model

**The creature on your screen IS your partner**, not a third being you both keep alive. You cannot feed it and you cannot fail it. **No streaks, no decay, no death, no bereavement flow.** Long-term bonding comes from a permanent visual trait gained every few hundred exchanges and never lost.

Hard rule: **the creature has no negative-valence idle state.** Resting is content. Absence is asleep or away. Never sad, never sulking, never hungry, never dying — because a low-energy creature that represents a *person* invites the inference that they chose not to answer. Exactly two states, "with you" and "away", and no failure mode may editorialise beyond them.

At 3 % battery the device spends **one final packet** to say "going to sleep", so your partner sees sleep rather than silence. That packet costs ~0.05 mAh and converts the most alarming failure into the most reassuring one.

**The object breaks character exactly once.** If service is genuinely broken for >24 h — subscription lapsed, SIM deactivated — it stops being cute and shows a short code and a URL in plain language. Pretending to be sleepy while actually being unsubscribed is a betrayal.

### 7.6 Onboarding without a phone — the competitive weapon

Bond Touch needs an app and an account. Totwoo needs a phone number. Lovebox needs the **recipient's** Wi-Fi password typed into a 192.168.4.1 captive portal, so it "ideally" has to be gifted in person `[V, vendor sources]`. Standalone cellular lets us ship the only device in the category with **literally zero setup**.

- **Factory bonding, the 95 % path.** Sold as a boxed pair. At manufacture both units get eSIM profiles on one subscription group plus a cross-signed key pair in their secure elements. First boot: "hold the crown". Both hold. Both creatures wake simultaneously — **and that works fine 5000 km apart**, over cellular, which is what makes split shipping possible.
- **Re-pair / rename.** The crown is a natural character wheel: turn to select, press to commit, long-press to backspace. ~2 s/char, so a 6-character base32 code (no I/1/O/0) takes ~20 s. Server-issued, 10-minute TTL, one-time, 5-attempt rate limit.
- **Recovery.** A card in the box with a per-device claim code and a URL any browser can use — also how the 8–12 canned messages get co-authored, which must include at least two lines written by each partner. Generic factory copy would be the weakest thing in the product and the thing reviewers quote.
- **Billing.** N years prepaid in the box price. A payment wall on a gift is a disaster, and a subscription-cancellation dark pattern in a love object is worse. Renewal at year N is a cliff that must be handled gracefully or the object dies for a billing reason.

**Logistics:** offer split shipping of a bonded pair at checkout. Never require the two devices to be physically co-located.

---

## 8. WHAT CHANGED FROM V1

| v1 | Now | Why |
|---|---|---|
| ESP32-S2-SOLO-2U + BG95-M3 + TPS62172 (815 mm², 3.2 mm) | One nRF9151 SiP (134 mm², 1.2 mm) | 84 % area, 63 % height. BG95 eDRX @81.92 s is 577 µA vs 132 µA measured — 97 mAh/week of standby on its own. |
| 1.8" 256×32 SSD1326 OLED + R1200 12 V boost | 160×68 memory-in-pixel, single 3.1 V rail | Deletes an entire conversion stage, an inductor and a Schottky. And it makes always-on cost 20 µA instead of ~21 mAh/day. |
| TPS62172 3.3 V buck + R1200 boost (3 conversion stages) | One TPS62840 at 3.1 V (1 stage) | nRF9151 VDD is 3.0–5.5 V and runs straight off the cell. The 12 V rail died with the OLED. |
| Nano-SIM socket (~182 mm² + 13 mm edge clearance + a case aperture) | MFF2 eUICC, 30 mm² | ~152 mm² and the last unnecessary hole in a sealed object. |
| MCP73871 at 100 mA (5.35 h charge), modem hung off the raw cell | BQ25180 at 300 mA (2.5 h) with a 1.5 A / 2.5 A-pulse power path | Fixes both v1 pain points. The 25 V abs max on IN also survives the charge-port fault. |
| 2 × MHF1 connectors + coax, antenna placement binding a 37.5 mm width | One spring-finger feed to a chassis radiator, zero coax | Deletes the routing constraint that set v1's width. |
| GNSS (BG95 + second antenna + LNA) | Not fitted. Silicon present, pin terminated. | Removes the 25 mm separation constraint that was v1's binding mechanical limit — and removes a coercive-control vector from a device given between intimate partners. |
| Cherry MX key (15.6 × 15.6 × 11.6 mm) | 24-detent metal crown + an off-axis 2.6 × 1.6 mm tact | It is the product now, not an input. |
| USB-C receptacle + native ESP32-S2 USB DFU | 4-pin magnetic pogo (VBUS/GND/SWDIO/SWCLK) + LTE-M FOTA | nRF91 has no USB peripheral. A 7.4 mm-deep cavity through a 15 mm body is the most contested hole in the product. The two extra pins buy field recovery and a PPK2 attach point. |
| 26-pin ZIF for the display | 10-pin FPC, **soldered** | A ZIF in a dropped keychain is a latent intermittent, and it costs 1.0–1.2 mm of Z we do not have. |
| 500 mAh cell, 120 × 37.5 mm board | 560 mAh cell, 23 × 55 mm board | 4.5× less board area for 12 % more energy. |

---

## 9. OPEN QUESTIONS AND RISKS, RANKED

Ranked by *kill probability × irrecoverability*.

### 9.1 Band 12 TRP. This is the one that kills the product.

The corrected gate is **12.3 % total efficiency at 699–746 MHz**, not 5.62 %. The honest estimate for a 22.5 mm cap on a 23 × 55 mm ground plane inside a loaded enclosure is **8–18 %**. The gate and the estimate are the same number.

**There is no catalogue fallback, and I want that stated in writing.** Ignion NN02-224 has no published solution below 824 MHz `[V]` and cannot certify B12. Taoglas FXP14 measures 46.2 % at 698–806 MHz **on a bare 2 mm ABS plate in free space** `[V]`; inside this cavity 1–2 mm from an aluminium-laminate pouch, realistic is 3–8 %, below the gate. The DNP MHF4 pad is a **chamber probe**, not insurance.

**The real Plan B, and it is why the body is 95 mm and not 100:** if the metal cap misses, revert to a polymer cap, extend the clearance zone to 32 mm, and fit an **Ignion NN03-310** (30.0 × 3.0 × 1.0 mm, published 698–960 MHz `[V, UM_NN03-310]`) lying **along the length**, not across the board. That takes the body to ~105 mm — still Small Form Factor, barely. ENDURANCE rejected NN03-310 because "at 30 mm it cannot lie across a 24 mm board," which is true and irrelevant in a 95 mm stick.

**Also unbudgeted by everyone: B2 and B4 at +12.0 dBm TRP each are mandatory** `[V]`. A single 50 Ω feed on a 22.5 mm cap must cover 699–746 **and** 1710–2155 MHz. That is a dual-resonant antenna design problem, not five 0402s, and it goes in the consultancy's statement of work on day one.

> **Cheapest settling experiment:** a representative mechanical mock-up — real cap, real split ring, real 6-layer FR4 with the real matching footprint, a real aluminium-laminate dummy cell, the real display module, a real crown, inside a printed shell — measured in a CTIA chamber at 700/750/850/900/1800/2100 MHz. **~$8–15k, 3 weeks.** Measure **three configurations: bare, in-hand phantom, and with a 120 g steel key bundle on the lug.** If bare-chamber comes in under 15 %, stop and redesign rather than iterating the match.

### 9.2 Mobile-terminated reachability may simply not work

A field report on nRF9151 LTE-M found downlink commands published while the device was in RRC Idle **were not delivered by paging at all** — they arrived only on the next uplink, bounded by a 30–60 s keepalive, with operator NAT/firewall behaviour suspected. If MT paging is unreliable on the chosen operator, "adaptive eDRX" degrades to "polling", which changes the power model *and* the data bill. The entire 15.56 + 8.23 mAh/week reachability budget exists for no other purpose.

Recoverable — PSM + 300 s polling costs 2.0 weeks of runtime at 150 s latency — but it is the difference between the product we described and a worse one.

> **Cheapest settling experiment:** nRF9151-DK + PPK2 + three MVNO SIMs (AT&T, T-Mobile, one roaming MVNO), running the actual reachability state machine. Measure: is eDRX granted (`+CEDRXRDP`)? is PSM granted (`+CPSMS`)? is AS-RAI negotiated? **does an MT UDP packet reach a device in RRC Idle at eDRX 163.84 s, and after how long?** **<$2k, 2 weeks.** This is the cheapest high-value test in the whole programme and it should start on day one.

### 9.3 Display supply, and the two specs nobody has read

Sharp LS011B7DH03: **zero authorised stock, 28-week factory lead, ship dates Feb 2027.** The five-figure broker quantities must not be used for production. Winstar WFM0108A2 is buyable in singles but its outline is disputed by 2.8 mm of width and 1.3 mm of thickness, and it mandates a 57–70 Hz EXTCOMIN that must run for the entire week the device is "always on" — if that toggle is generated by anything that stops in deep sleep, you lose the image or DC-bias and permanently damage the LC.

And nobody has opened the **LS011B7DH03's own electrical table**. We are extrapolating IVDD1, IVDD2, fCOM and storage temperature from the LS013. The LS013's Tstg is **−10 to +60 °C absolute maximum**, which a car dashboard in July exceeds routinely.

> **Cheapest settling experiment:** buy **20 Winstar samples from First Components (~€400)**, measure the outline with callipers, and bench-test the actual minimum EXTCOMIN frequency at which the image holds for 72 h. In parallel, request a written Winstar quote with MOQ, lead time and a lifecycle statement, and request the LS011B7DH03 production spec through an authorised Sharp distributor. **~€400 and two phone calls.** Do this in week 1 — it also unlocks 1.34 mm of Z (§6.2).

### 9.4 Does a coaxial crown actually feel like petting?

The brief says "a knurled metal jog dial at one END of the stick." I have built a coaxial crown you **twist** between thumb and forefinger. EX argued, with some force, that a transverse wheel you **stroke** with the pad of the thumb is the gesture that matches "stroking a pet", and that twisting is not. I do not think that is settled by argument.

> **Cheapest settling experiment:** two 3D-printed mules with real journals, real hardened races, real ceramic balls, real O-rings and a real tact — one coaxial, one transverse — plus a VG0840001D on a bracket driven by a DRV2625-DK. **Ten hands, blind, 20-second sessions. ~$3k and 2 weeks.** Decision gate before the shell CAD starts. If transverse wins, the crown zone shortens by ~3 mm and the angle sensor moves to a side-shaft arrangement, which costs a different sensor (MA782 supports side-shaft; MT6701 is on-axis only) — that is a real but bounded respin of the satellite PCB, which is exactly why §4.5 keeps it separable.

### 9.5 The eSIM's 20–60 µA clock-stop trap

Nordic's current-consumption chapter carries an explicit footnote: if the UICC does not support supply shutdown, **add 20–60 µA at 3.7 V** `[V]`. That is up to 10 mAh/week — more than the display, both always-on sensors, the charger and the gauge combined. It is the single easiest way to silently lose a day of battery life, and it is decided by a supplier email nobody sent.

> **Cheapest settling experiment:** a written confirmation of UICC supply-shutdown support and the minimum shutdown interval, from the supplier, before any reel PO. **Free.** Then verify it on the bench with a PPK2 during the §9.2 test.

### 9.6 The coverage-search governor is a specification, not a firmware to-do

The only unbounded failure mode in the design. A modem that cannot find a cell draws 1.72 mA continuously `[V, arXiv 2601.17656 Thingy:91 PPK2]` = 41 mAh/day, flattening this cell in 11 days of a basement or a flight. I have budgeted 20 mAh/week for it; ENDURANCE budgeted 0.86.

> **Cheapest settling experiment:** write the exponential-backoff schedule, the accelerometer/grip "stationary and untouched for N minutes → stop searching" rule, and the maximum permitted search duty cycle **into the requirements document with numbers**, and make it a release gate tested in a shielded box. **Free, and it must happen before firmware architecture, not after.**

### 9.7 The screen is invisible in the dark, which is where the product lives

Reflective, 0.2 % transmissivity. The most likely single use context for a long-distance-couples device is a dark bedroom. The RGB halo carries the "something happened" channel but cannot show a creature's face or a message.

> **Cheapest settling experiment:** 0.60 mm is already reserved in the Z-stack. Get an Azumo quote for a 1.08 in frontlight film in week 1 (cost, MOQ, lead time, added thickness, and the lamination step). A frontlight at ~1 % duty costs under 1 mAh/week, so the decision is entirely about cost, thickness and supply, not power. **Default is to fit it.** If Azumo cannot supply a 1.08 in part, this becomes an explicit, documented product limitation rather than an accident.

### 9.8 Grip sensing may disappoint

IQS211B on a static annular electrode near a floating metal crown, a hand, a cell and a 23 dBm TX burst. Cx of a 22 mm ring a few mm above a ground plane is ~5–15 pF, comfortably inside the 120 pF ceiling — but the RF rectification and the triboelectric charge from the rotating crown are real.

> **Cheapest settling experiment:** a coupon with the real end-cap geometry, the real crown spinning, and a real TX burst from a DK. **~$1k, 1 week.** Reserve two pads and a GPIO for a fallback so it is a stuff option, not a respin. If grip fails entirely, presence degrades to the DRV5032 pair plus a pick-up detector, which costs nothing and already exists.

### 9.9 EU Battery Regulation 2023/1542 Art. 11

From **18 February 2027**, portable batteries must be removable and replaceable by the **end user** with commercially available tools; permanent adhesives blocking the cover are prohibited; spares must remain available 5 years after discontinuation. The wet-environment provision is a downgrade to professional replacement, not an exemption, and the Commission applies it narrowly. A Delegated Act has added exemptions reportedly covering compact and shock/water-resistant wearables.

> **Cheapest settling experiment:** a written legal opinion on whether a 27 × 95 × 15 mm sealed keychain object qualifies. **~$3–5k.** Must land **before the shell is frozen**, because a glued capsule and a user-openable door are different products and the door costs ~1.5 mm of thickness and most of the jewel. The screwed-rear-shell-plus-connectorised-cell architecture keeps both doors open at low cost in the meantime.

### 9.10 nRF9151 lead time will make the decision for us

16–19 weeks factory lead, 0 stock at DigiKey/Avnet/element14, Mouser 283 units, Octopart flagging −48.7 % three-month inventory `[V?]` — and note that distributor figures throughout this corpus are search-summary-derived because DigiKey returned HTTP 403 to every direct fetch.

> **Action, not an experiment:** place the 2k reel PO against the lead-time clock **before the schematic is finished**, or the part choice gets made for us. Order the 500-pc `-R7` for prototypes at the same time.

### 9.11 Lower-ranked but live

- **MT6701 single-source.** Mitigated by the dual-variant satellite PCB (§4.5). ~$300.
- **LRA acoustic radiation.** Anechoic box measurement at 170 Hz before ID sign-off. ~$500.
- **Press force independence from thumb position.** Measured on the §9.4 mule, not argued.
- **Detent life.** 1,000,000 indexes on a motorised rig with a torque-decay limit. ~$4k.
- **MAX17048 battery model INI.** Ship cells to ADI early; without it SoC is ±15–20 %.
- **Cell PCM trip point and DC-IR at 0 °C.** Measured, on a real cell, with a real 295 mA burst.

---

## 10. WHAT TO PROTOTYPE FIRST

**EVM-0: three mules, run in parallel, before any schematic freeze. ~$30k, 6–8 weeks.**

They are deliberately separate because the three biggest unknowns are independent and the cheapest one answers fastest.

### Mule A — the network mule (start day one, ~$2k, 2 weeks)

nRF9151-DK + PPK2 + three MVNO SIMs. No custom hardware at all.

Answers: Is eDRX granted, and at what cycle? Is PSM granted? Does AS-RAI negotiate? **Does a mobile-terminated UDP packet reach a device in RRC Idle at eDRX 163.84 s, and after how long?** What is the *measured* per-paging-occasion energy — the 92.6 µA field figure that carries 12 % of the power budget, or Nordic's published 18 µA? Does the eSIM's UICC support supply shutdown in practice?

**This is the highest value per dollar in the entire programme** and it tests the central product promise ("their boop reaches you") without a single custom part. It also produces the PPK2 baseline against which every later firmware build is checked for the +600 µA debug-UART regression.

### Mule B — the RF mule (~$20k inc. chamber, 5 weeks)

A **non-functional** mechanical representation: machined 6061 cap, moulded or machined split ring, a 23 × 55 mm 6-layer FR4 board with the real matching footprint and real ground pour, a real aluminium-laminate dummy cell, the real display module, a real non-magnetic crown with a real magnet, an LRA can dummy, inside a printed shell. Feed through the real spring finger onto the real masked Ni/Au pad.

Chamber: **bare, in-hand phantom, and with a 120 g steel key bundle** at 700/750/850/900/1800/2100 MHz.

Gate: **≥15 % total efficiency bare at 699–746 MHz.** Under 15 %, do not iterate the match — go to Plan B (polymer cap, 32 mm clearance, NN03-310, 105 mm body) and re-measure.

### Mule C — the feel mule (~$4k, 3 weeks)

Two 3D-printed crown-end assemblies — one coaxial, one transverse — with real POM journals, hardened 17-4PH races, ceramic balls, BeCu leaf springs, O-rings and tacts, plus a VG0840001D on a bracket driven by a DRV2625-DK from a scripted waveform set.

Answers: coaxial-twist vs transverse-stroke, on ten hands, blind. Detent torque target and its decay over 100k indexes. Click separation at 8, 12, 15, 20 detents/s with active braking on a real ~48 g mass — which is the measurement that decides whether the click→purr crossfade is a designed transition or a papered-over failure. Press force independence from thumb position. Acoustic output at 170 Hz.

### What EVM-0 does *not* do

No custom PCB with an nRF9151 on it. No firmware beyond the reachability state machine on a DK. No shell tooling, no glass, no OCA, no eSIM provisioning, no certification. **Nothing that costs money is committed until Mule B reports**, because if the antenna misses, the shell architecture changes and everything downstream of it is scrap.

### Gate to EVM-1

All three must pass before a custom board is laid out:

1. Mule A: eDRX granted **and** MT paging delivers on at least two of three carriers, or a documented polling fallback with its measured energy cost.
2. Mule B: ≥15 % bare-chamber B12 efficiency on the metal cap, **or** a Plan B configuration that achieves it.
3. Mule C: a chosen dial geometry, a measured detent torque, and demonstrated click separation to ≥12/s.

Plus two paper items on the same clock: the Winstar mechanical drawing in hand, and the EU battery-regulation legal opinion delivered.

---

## Appendix: things I am deliberately leaving dead

Each of these was proposed in the corpus, killed under hostile review, and stays killed. If someone wants to reopen one, they need to refute the specific finding, not re-argue the benefit.

| Killed | Finding that killed it |
|---|---|
| Phantom tactile motion / second actuator | Shell's first free-free bending mode ~2105 Hz, 12× the carrier; the capsule moves as a rigid body |
| Colour IPS TFT | 18 mA cell-side = 42 mAh/week; kills always-on, which is the entire "alive" thesis |
| Any OLED | ~7–12 mA from the cell, plus 20,000 h to 50 % luminance with a static element on a gift object |
| E-paper | 300 ms partial refresh is 3 fps at best, with a visible smear. Petting cannot be rendered. |
| Piezo / TDK PowerHap + BOS1921 | 0 stock at DigiKey, $99.99 at a broker, 60–190 V next to a Li-ion cell in a pocket |
| Ignion NN02-224 as the B12 antenna | Published cellular-IoT solution is 824–960 MHz; B12 is 699–746 |
| The Chu limit as an efficiency argument | Chu bounds Q, not efficiency; adding loss *increases* bandwidth |
| nPM1300 | BCHGISETDISCHARGE "Low" resets on every TX; forces low-accuracy gauging; light-sensitive WLCSP; a DevZone erratum worth 100 µA |
| nPM1304 | 210 mA discharge limiter against a 295 mA TX subframe. It would brown out on every transmit. |
| Onomondo SoftSIM as primary | SPDX GPL-3.0-only, no confirmed commercial licence, ISR-context APDU handler |
| Alps EC05E / any contact encoder | 100,000 cycles ≈ 11 months at 300 rev/day, on the defining interaction of a gift object |
| Microchip MTCH101 | 54 µA at 3.3 V, not the 4 µA the internet says. Datasheet Table 8-2. |
| Any gyro (LSM6DSV16X, BMI270) | No feature in this product needs one; 420 µA in A+G low power is 70 mAh/week |
| ADXL362 | $7.62 to save 2.4 µA = 0.4 mAh/week. Indefensible in a gift-object BOM. |
| GNSS | 43.1 mA tracking, a second antenna site that does not exist, and a coercive-control vector |
| Microphone | Non-negotiable. A love object that can listen is a bug. |
| Qi charging | Largest coil that fits is ~22 mm against a 30 mm derated reference; and the metal crown trips foreign-object detection by design |
| 2-pin pogo | One bad FOTA bricks a sealed object with no reflash path and no PPK2 attach point |
| Qvar on the rotating crown | A steel crown in a POM journal is a triboelectric generator; rotation charge swamps grip during exactly the gesture it accompanies |
| 440C detent balls | Martensitic and ferromagnetic, millimetres from the sensing magnet |
| 303SS as a ball-detent race | ~170 HV annealed; two balls brinell soft grooves long before 800,000 indexes |

## ADDENDUM 2026-09-13 — Programming, debug, and charge interface

**Status:** decision, recorded from the 13 Sep review. Amends the §4.3 "Charge / debug" row and §8 row 9. Nothing else in the body changes.

### A.1 The two ways in

Only two paths reach the nRF9151: **SWD over the dock pads**, and **LTE-M FOTA through MCUboot**. No USB receptacle, no UART pad. Console and shell are SEGGER RTT over the same two SWD lines in development builds. The UART console is compiled out of every build (§5.4: +600 µA `[V]`), and RTT logging out of the production image.

### A.2 The dock interface, specified

| Item | Decision | Tag | Why |
|---|---|---|---|
| Pads | 4 × flat pads, single row, **2.54 mm pitch**, order **GND · SWCLK · SWDIO · VBUS**, gold over 1.0–2.5 µm Ni (unchanged) | `[V]` pitch is the wearable-charger de facto standard | Power at the two ends: a head pressed on backwards maps VBUS↔GND (blocked by the reverse FET) and SWDIO↔SWCLK (harmless). |
| Pad location | Rear face, mid-body, **x ≈ 40–52**, over the cell | `[U]` | ≥10 mm from the split ring (§6.2 metal exclusion) and >20 mm from the satellite PCB's Hall latches and the sensing magnet. The main PCB is on the display side of the cell, so these pads are on a **flex tail bonded behind four sealed openings in the rear shell**. The flex lives in the 0.60 mm swell gap; budget its thickness in §6.2 before the stack is called closed. |
| Ferromagnetic target | **0.3 mm 430 stainless shim, insert-moulded in the 1.2 mm rear wall behind the pads. Not a magnet.** | `[U]` | The head carries the magnets. A magnet in the device costs Z the battery column does not have (0.72 mm margin), and anywhere nearer the crown it sits within reach of two 3.9 mT Hall latches and a 14-bit angle sensor. A shim in the wall costs nothing inside. |
| Polarity | Enforced by the **dock cradle geometry** — the crown end and the metal cap are different shapes — not by magnet repulsion. | — | Repulsion needs a device-side magnet, ruled out above. |
| SWD pad protection | Series resistor plus a 3.3 V-class low-capacitance TVS on SWDIO and SWCLK, at the pads | `[U]` values at schematic | The existing short protection covers VBUS/GND only. While docked, a key bridging the live VBUS pad to an SWD pad puts 5 V on a 3.1 V GPIO; the clamp takes it instead. Keep clamp capacitance low enough for 4 MHz SWD. |
| Dock head | Wearable-charger-class magnetic pogo head (Sunmon 901-00001 / Jiatel 2.54 mm 4P / CFE / Good-Link class): pogos **and** magnets in the head, 2.54 mm, 1–2 A rated, 300–500 g pull, ≥30k cycles, USB-C fed | `[U]` MPN; vendor quotes are against their own steel plate | Catalogue two-half connectors — Adafruit 5358, Adam Tech PH1-3L-04-FVMP-4560, ATTEND 303C-C4115-30-04, EDAC POGO+ — all put a housed receptacle in the device. That is a cavity again, smaller than USB-C but still a hole and a lint trap. The wearable head mates to bare pads. |
| Dock board | USB-C receptacle with 5.1 kΩ Rd on CC1/CC2; 5 V straight through to the head, current-limited so a key across the live head pins is harmless; **3.3 V LDO driving VTref on a 10-pin Cortex debug header**; SWDIO/SWCLK passed straight through | `[U]` | A four-wire head has no pin for VTref and a J-Link will not talk without it, so the dock supplies it. The header is what EVM, service, and the PPK2 plug into. ~$6/unit as already costed in §4.6. |
| Bench jig (EVM-1) | Adafruit 5412 cable with the USB-A end cut off and rewired to a Cortex header, or an Adam Tech / ATTEND pin half, on a printed cradle against the same pads, VTref from a bench 3.3 V | — | $5–10, no custom parts. SWD at 1–4 MHz over a metre of unshielded four-wire is fine. |
| Production programming | The same four pads on a bed-of-nails, bare board, before the rear shell closes: MCUboot + app + modem firmware in one pass, then APPROTECT locked. A Tag-Connect TC2030 footprint is optional if the 23 × 55 board has room; it is not required. | — | A locked unit is still recoverable through the dock with `nrfutil device recover`, by full erase only — the right property for a sealed, field-serviced object. |

### A.3 USB-C: not fitted, and what would bring it back

Deleted per §8. If it returns, it returns in exactly one form: **power-only USB-C** — 5.1 kΩ Rd pulldowns, D+/D− unconnected, SWDIO/SWCLK on **SBU1/SBU2** with clamps, IP67 receptacle gasketed to the shell. D+/D− are never used for SWD: BC1.2 dedicated-charging-port adapters short D+ to D−, which would short SWDIO to SWCLK the first time a C-to-A cable is used.

Any one of these reopens the decision: (1) counsel reads EU 2022/2380 Annex Ia as covering this object; (2) Mule B fails B12 and the shell moves to the 105 mm polymer Plan B, which has room for a cavity; (3) user research says a proprietary dock blocks gifting. **One port or the other, never both** — two charge ports carry both sets of problems and the dock cost.

### A.4 Firmware path

nRF Connect SDK on Zephyr, sysbuild with MCUboot, external-flash secondary slot per §4.1. Modem firmware is flashed over the same SWD link. **Field modem updates are delta only:** a full modem image does not fit in a 16 Mbit NOR beside the app slot, so either accept delta-only or size the NOR up at BOM freeze. Dev builds: `CONFIG_LOG_BACKEND_RTT`, `CONFIG_SHELL_BACKEND_RTT`; every build: `CONFIG_UART_CONSOLE=n`. All of this is brought up on Mule A (nRF9151-DK + PPK2) first; the custom board definition is built against that tree so EVM-1 adds only the pin map and the dock cable.

### A.5 Added to the §4.4 confirm-before-design-in list

9. **Dock head MPN and its measured pull force against a 0.3 mm 430 shim through a 1.2 mm wall.** Vendors quote against their own plate.
10. **Flex-tail thickness in the swell gap.** §6.2 closes at 0.72 mm in the battery column; the flex spends some of that.
11. **SWD clamp capacitance vs. programming speed**, verified on EVM-1.

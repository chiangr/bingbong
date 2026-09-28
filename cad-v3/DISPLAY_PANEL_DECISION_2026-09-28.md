# Display Decision: bingbong v3 rev A

## 1. Recommendation

**Primary: OSPTEK AM110Q126294LK1** (1.10" 126x294 AMOLED, ICNA3306 display driver, CHSC6417 touch controller, 24-pin BTB).
**Fallback: Brownopto BR138102-A1** (1.38" 128x400, ICNA3306 display driver, CST820 touch controller, 31-pin gold finger). It is also sold as Shineworld GLO138-D-M2001. It only becomes a real fallback once the vendor confirms the touch variant and stock.

**Why:** AM110Q is the only candidate where the vendor publishes all of these: the module spec, the display driver datasheet, the touch IC datasheet, and working 4-wire SPI init and touch code [V]. It fits the 16 x 40 mm envelope with its cover glass (15.40 x 38.97 mm) [V], and it drops into the current baseline outline. The fallback, BR138102-A1, is electrically cleaner: 3.1 V IO, so no LDO or level shifters, and the touch IC already has an upstream Zephyr driver [V]. But three things rule it out as primary today:
- It cannot be bought right now. Every listing is sold out [V?].
- The vendor's own product pages say "Touchscreen: None" [V?].
- The folded tail sticks out 11.4 mm sideways, so the module is about 23.8 mm wide [V drawing].

AM110Q's own weaknesses are real: an electrical page copied from another product, no ELVSS absolute maximum, no SWIRE pin, an unidentified BTB receptacle, and 1.8 V IO. But the missing items are specific and can be requested from the vendor, and the extra parts it costs are known. Order samples of both now, and freeze the display sheet only after OSPTEK answers the questions in §3.4.

## 2. Comparison

| Model | Driver IC | Res | Outline (mm) | IO V | On-module PMIC | Touch IC | Connector (mate) | Docs | Zephyr / LVGL | Sourcing | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **OSPTEK AM110Q126294LK1** | ICNA3306 [V] | 126x294 | 12.96x30.94x0.80 panel; 15.40x38.97 with cover glass; 3.1–3.3 folded stack [V] | 1.8 V (1.7–1.95) module spec; die allows 3.3 [V] | No [V] | CHSC6417, I2C 0x2E per vendor code [V] | 24-pin 2x12 BTB WB2564024M (mate unknown [U]) | Spec (Preliminary, bad electrical page), both IC datasheets, ESP-IDF init and touch code [V] | No ICNA3306 driver; chsc6x driver needs a patch (8-bit coordinates) [V] | Official AliExpress/Taobao stores, but listing not confirmed [U]; not in OSPTEK catalog [V] | **Primary** |
| Brownopto BR138102-A1 / Shineworld GLO138-D-M2001 | ICNA3306 [V] | 128x400 | 12.435x38.41x0.78; ~39.9 long folded; tail +11.38 sideways [V] | 1.65–3.3 V [V] | No; SWIRE pin present [V] | CST820 on drawing, 0x15 [V]; vendor pages say none [V?] | 31-pin gold finger, 0.3 mm pitch [V?] (ZIF P/N unknown [U]) | Spec (36 pp, boilerplate, fake abs-max table), IC and touch datasheets, no panel init [V] | CST820 upstream (hynitron,cst8xx) [V]; display driver needs porting | Sold out ($30 / $8) [V?]; no distributor | **Fallback, if touch and stock are confirmed** |
| Truly TR095A120SPC | RM69310 [V] | 120x240 | 12.8x27.35x0.78 glass; tail unknown [V/U] | 1.65–3.3 V [V] | No; SWIRE out [V] | Unnamed (Zinitix?) [V?] | 30-pin, type unknown [U] | 10-page excerpt, Rev 0.1, confidential; NDA register guide only [V] | Community ZSband rm69310 driver [V]; touch none | Panox only; likely Mi Band 4 surplus [U] | Risky |
| OSPTEK AM095Q120240XZ | SH8501A [V] | 120x240 | 12.8x27.35x0.8 [V] | 1.65–3.3 V [V] | No [V] | **None** [V] | 15-pin 0.3 mm finger (mate unknown) [V/U] | Excellent (spec, IC datasheet, init, adapter schematic) [V] | ESP-IDF only; needs double RAMWR patch [V/U] | AliExpress, Hicenda, others [V?] | Reject (no touch) |
| iFan IF011TPS12-29 | RM69310 [V?] | 126x294 | 12.96x30.94x0.784 [V?] | Unknown | Unknown | Not standard [V?] | 27-pin FPC [V?] | No public spec | Weak | Contact vendor | Reject unless NDA spec arrives |
| iFan IF010TPS12-24C | FT2201 [V?] | 120x240 | 12.8x27.35x0.75 [V?] | Unknown | Unknown | Not named here [U] | Unknown | No spec | Unknown | Contact vendor | Reject |
| Toppop TT110AMN94A | JD9613 [V] | 126x294 | 12.96x30.94x0.95 [V?] | Up to 3.3 V [V] | ELVDD/ELVSS can be generated on-chip [V] | Not standard [V?] | Unknown | IC datasheet only (V0.02) | Unknown; half-screen RAM [V?] | Alibaba | Watch: ask for a spec |
| DWO DO0164FMST02 | CO5300/ICNA3311 [V] | 280x456 | **23.74** x38.62x0.8 [V] | 3.1 V OK [V] | **Yes** [V] | Public datasheet [V] | BTB with named mate [V] | Excellent [V] | Zephyr co5300 [V] | DWO sales | Reject (too wide); ask about a narrow custom |
| EDO E1473AC63.B | SH8501B [V?] | 194x368 | 19.36x36.17x0.78 [V?] | 1.8 V [V?] | No; ELVDD/ELVSS ±3.3 V, TPS65631 cannot supply it | ZTW622 (not public) | 38-pin BTB | SlideShare copy [V?] | None | Resellers | Reject |
| Haresan/HEM 1.1" | RM690A0 [V?] | 126x294 | 12.96x30.94x0.81 [V?] | Unknown | Unknown | Optional [V?] | Unknown | None | None | Contact | Reject |
| Hemlcd ZC-A1D47W-005 | SH8501A [V?] | 194x368 | 25.19x45.19x2.06 [V?] | Unknown | **Yes** [V?] | Unknown | Unknown | None | None | Contact | Reject (size, QSPI only) |

## 3. Display sheet for AM110Q126294LK1

### 3.1 Contents

**Rails**
- **Switch A (TPS22916-class, V3, SW_A_EN):** feeds VCI_SW to pin 1 VCC and pin 3 CTP_VDD at 3.1 V.
  - Never connect VSYS to pin 1. The ICNA3306 VCI absolute maximum is 3.6 V [V]. The module's 2.7–4.8 V "VBAT" line was copied from another product [V].
- **1.8 V low-Iq LDO (TPS7A02-class [U]):** feeds IOVCC (pin 5) and TP_IOVCC (pin 7), a few mA [U].
  - The ICNA3306 datasheet wants VDDI up before VCI [V]. The module's p.8 says "any order" [V].
  - Option 1: supply the LDO from unswitched V3 and drive its EN from SW_A_EN. Then the LDO's fast start plus the load switch's slow rise gives VDDI first [U, check on the bench].
  - Option 2: give the LDO its own GPIO (+1 GPIO).
- **PMIC: yes, external TPS65631DPDR plus 2 inductors (already planned).**
  - VPOS 4.6 V goes to pins 17/19 ELVDD [V]. VNEG goes to pins 21/23 ELVSS and must be programmed to -2.4 V: 21 rising edges on CTRL, each 2–25 µs [V TI table].
  - CTRL comes from an nRF GPIO (PMIC_CTRL), because the tail has no SWIRE or OLED_EN pin [V].
  - The input comes from VSYS through switch B (SW_B_EN) per the existing plan [U: plan detail].
  - Reserve a footprint for a series FET on ELVSS (DNP) in case OSPTEK says the -4.0 V first ramp is not allowed [U].
  - Put decoupling on ELVDD/ELVSS right at the connector.

**Level shifting**
- Down, 3.1 V to 1.8 V: SCK, MOSI, CS, DC, RESX and CTP_RST go through SN74LVC-family buffers powered from the 1.8 V rail (for example LVC2G34 plus LVC3G34, or 1G34s).
  - These buffers accept 5.5 V inputs and have Ioff [V local datasheet], which also gives the isolation the NOR-shared SPIM bus needs.
  - Keep the 33 Ω series resistors.
- Up, 1.8 V to 3.1 V: TE and CTP_INT go through SN74LV1T34-class gates on V3 [U part choice].
- Leave SDO (pin 16) unconnected. Use TE toggling as the connection check.

**Touch**
- CTP_SDA/SCL (1.8 V) connect through an I2C translator that isolates when unpowered (PCA9306/TCA9406-class [U]) to the chosen TWIM.
- This is mandatory, because the CHSC6417's I2C pins draw current when the chip is unpowered [V].
- If OSPTEK approves 3.1 V on TP_IOVCC, the translator can go, but the bus still needs gating [U].

**Other pins**
- Pin 13 MTP: leave open or tie to GND [V].
- GND pins 9, 10, 11 and 15.

**Connector**
- 24-pin 2x12 BTB receptacle. The part number is unknown [U].
- Replace the placeholder "27-pin 0.4 mm B2B" symbol.
- Leave the footprint as TBD until OSPTEK sends the drawing.

**nRF9151 GPIOs**
- Dedicated (9): CS, DC, RESX, TE, CTP_INT, CTP_RST, PMIC_CTRL, SW_A_EN, SW_B_EN (+1 if the LDO gets its own enable).
- Shared: SPIM SCK/MOSI (with the NOR) and TWIM SDA/SCL.
- That is about 3 more than the current plan (touch INT and RST, plus PMIC CTRL).

**Added area:** 1 LDO, 3–4 small logic packages and 1 I2C translator, about 15–25 mm² [U].

### 3.2 Power-on sequence
The ELVDD/ELVSS placement in steps 7–10 is the conventional order [U]. It needs vendor confirmation because §13.1.8 of the spec says the opposite.

1. Before any rail comes up, hold all display lines low or high-Z and hold CTP_RST and RESX low.
2. Turn on SW_A and the LDO, so VDDI (1.8 V) and VCI/CTP_VDD (3.1 V) come up.
3. Wait at least 10 ms, then release RESX high after at least a 10 µs low pulse. The vendor driver uses 10 ms low [V].
4. Wait at least 10 ms before the first command. The vendor waits 150 ms [V].
5. Release CTP_RST at least 1 ms after CTP_VDD. The first touch report comes within 200 ms [V].
6. Send the init table: FE 00, C4 80, 3A 55, 35 00, 53 20, 51 xx, 63 FF, CASET with column offset 2, RASET, then 11 (SLPOUT) [V].
7. Turn on SW_B and raise PMIC_CTRL. VPOS reaches 4.6 V; VNEG first ramps to -4.0 V about 10 ms later [V]. Then send 21 pulses on CTRL to reach -2.4 V [V].
8. Wait for ELVSS to settle at -2.4 V.
9. Make sure at least 120 ms has passed since SLPOUT (the datasheet's figure; the vendor code uses 60 ms) [V].
10. Send 29 (DISPON).

### 3.3 Power-off sequence
1. Send 28 (DISPOFF). Wait at least 2 frames, then send 10 (SLPIN).
2. Drop PMIC_CTRL. The TPS65631 actively discharges ELVDD/ELVSS [U: check the timing]. Then turn SW_B off.
3. At least 100 ms after SLPIN, pull RESX and CTP_RST low. Park the SPI and I2C lines low; the buffers' Ioff protects the panel.
4. Turn off VCI before VDDI [V ICNA3306 datasheet] by disabling SW_A and then the LDO.
5. Before the next power-on, CTP_VDD must stay below 0.3 V for at least 1 ms [V].

Deep standby (4Fh) draws up to 200 µA [V], so full rail gating is the only low-power state we should use.

### 3.4 Documents to request from OSPTEK (luyu@osptek.com)
1. Mating BTB receptacle part number, its manufacturer, the pitch and a recommended land pattern for WB2564024M.
2. STEP/DXF of the folded tail: connector X/Y/Z after folding, bend radius, flat tail length.
3. A corrected electrical characteristics page for this module (the current one is SH8501A/BV6802), with module-level sleep and operating currents.
4. ELVDD/ELVSS absolute maximums, and whether the TPS65631's -4.0 V first ramp (about 10 ms before programming) is tolerated.
5. ELVDD/ELVSS on/off timing relative to VDDI/VCI, RESX, SLPOUT and DISPON. It should settle the §13.1.8 contradiction.
6. Written approval, or refusal, for running IOVCC and TP_IOVCC at 3.0–3.3 V.
7. Schematic of the ESP32-S3 adapter/test board (how it makes ELVDD/ELVSS and the 1.8 V IO).
8. CHSC6417 I2C protocol and register specification, and the touch firmware version.
9. Final (non-preliminary) ICNA3306 datasheet with standby currents.
10. Confirmation of the orderable part: cover glass plus CTP assembly, pre-bent tail.
11. Recommended VNEG (-2.4 V normal vs -3 V HBM).
12. Price, MOQ, lead time, lifecycle/PCN policy, and a commitment to freeze the pinout and connector through low-volume production.

## 4. Risks and open questions

**Primary (AM110Q126294LK1)**
- [V] The electrical characteristics page and absolute-maximum ratings belong to another product: the module's 5.5 V VCI/VDDIO limits contradict the IC's 3.6 V/3.3 V. Design to the IC datasheet until OSPTEK issues a corrected page.
- [V] No ELVSS absolute maximum is given. [U] Whether the panel survives the TPS65631's -4.0 V first ramp is unknown. This is the top electrical risk; the mitigation is a DNP series FET on ELVSS.
- [V] The power-sequence page is a generic MIPI copy with no ELVDD/ELVSS timing. §13.1.8 ("signals after pos/neg voltage stable") conflicts with the usual order of init, then SLPOUT, then high voltage.
- [U] The ICNA3306 datasheet wants VDDI before VCI; the chosen rail arrangement has to guarantee that order.
- [U] The BTB receptacle is unidentified, which blocks the footprint and connector placement.
- [V] The folded stack is 3.10–3.30 mm, not 1.88 mm. Recheck the enclosure Z budget.
- [V] The part is not in OSPTEK's catalog; the spec is V1.0 Preliminary; the vendor may change materials without notice. [U] No live AliExpress listing or price has been confirmed.
- [V] 1.8 V IO adds an LDO, about 8 translated lines and an I2C translator. [U] That could drop to near zero if 3.1 V is approved.
- [V] The CHSC6417 datasheet has no I2C address or register map; the protocol is defined only in the vendor code. The upstream Zephyr chsc6x driver cannot report y > 255, so it needs about a 30-line patch [U effort].
- [V] There is no ICNA3306 Zephyr driver. [U] Writing one on MIPI-DBI, based on display_co5300.c, should take about 1–2 days.
- [V] Reverse scan is not supported, so orientation has to be handled in software.
- [V] The ICNA3306 datasheet is V0.03 with standby currents TBD.
- [V] Touch is single-point only.
- [U] At 8 MHz SPIM a full frame takes about 74 ms (~13 fps). That is acceptable for glanceable use.

**Fallback (BR138102-A1)**
- [V?] It is unclear whether the touch variant ships: the vendor pages say "Touchscreen: None" while the drawing names the CST820.
- [V?] It is sold out everywhere; the Shineworld 1.4" page returns 404.
- [V] The folded tail puts the module at about 23.8 mm wide, and the length (about 39.9–40.1 mm) sits right at the 40 mm limit. [U] Whether the tail can be bent down to the board is unknown.
- [V?] The 0.3 mm pitch comes only from the store listing. [U] The ZIF part number and contact side are unknown.
- [V] The "absolute maximum" table repeats the operating ranges, so ELVSS has the same -4.0 V first-ramp exposure.
- [U] No init code exists for the 128x400 window; the column offset is unknown.
- [V] "Life Time 13 Months" is unexplained; the spec is a V0 template with copy errors.

**Others**
- [U] Toppop TT110AMN94A (JD9613 can generate ELVDD/ELVSS on-chip, 3.3 V IO) could remove the PMIC and shifters if a module spec and touch variant exist. Worth one vendor email.
- [U] DWO's architecture (PWR_EN + VBAT, on-module power, 3.1 V IO, SPI4) is the ideal. Ask DWO whether a narrow bar format under 16 mm exists or could be made.
- [V] AM095Q120240XZ is the best-integrated panel but has no touch. It only becomes a candidate if touch moves to a separate sensor, which would be a product decision.
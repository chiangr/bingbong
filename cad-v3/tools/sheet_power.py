"""Sheet 1 — power tree. Reference designators on this sheet are 1xx.

Blocks: A dock input protection · B charger (BQ25188) · C cell/NTC/crown button
        D fuel gauge (MAX17048) · E 3.1 V rail (TPS62840) · F VSYS reservoir
Open-drain pull-ups (BQ_INT, GAUGE_ALRT, SDA, SCL) live on the nrf9151 sheet.
"""
from schgen import Sheet, stock, root_paths, write_custom_lib
from parts import CUSTOM

R0402 = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"
C0603 = "Capacitor_SMD:C_0603_1608Metric"
C0805 = "Capacitor_SMD:C_0805_2012Metric"
NOTE = 1.27

S = Sheet("power.kicad_sch", "Sheet 1 — Power tree: dock input, charger, gauge, 3.1 V rail",
          root_paths()["power.kicad_sch"])
R, C, L = stock("Device", "R"), stock("Device", "C"), stock("Device", "L")


def res(ref, val, x, y, rot=0, **kw):
    off = dict(ref_off=(-2.5, -2.8), val_off=(-2.5, 3.2)) if rot == 90 else {}
    off.update(kw.pop("off", {}))
    return S.place("Device:R", R, ref, val, x, y, rot=rot, footprint=kw.pop("fp", R0402), **off, **kw)


def cap(ref, val, x, y, fp=C0402, **kw):
    return S.place("Device:C", C, ref, val, x, y, footprint=fp, **kw)


def custom(name, ref, x, y, mpn):
    blk = CUSTOM[name]
    tmp = S.place(f"Bingbong_v3:{name}", blk, ref, name, x, y, fields={"MPN": mpn, "Datasheet_local": "firmware/bingbong_pcb/_mech"},
                  ref_off=(0, 0), val_off=(0, 0))
    # re-place label text above / below the body (needs body height, known after placement)
    S.items.pop()
    h, w = tmp.half_h, tmp.half_w
    return S.place(f"Bingbong_v3:{name}", blk, ref, mpn, x, y, fields={"MPN": mpn},
                   ref_off=(-w, -h - 4.2), val_off=(-w, -h - 1.6))


# ================================================================== A. dock input
S.box((15, 20), (150, 125), "A · Dock input protection")
S.text((19, 27), "5 V arrives from the magnetic dock pads (dock sheet). Nothing on this path needs\n"
                 "firmware: a dead cell or a bricked image must still be able to charge (report E-2).", NOTE)
y = 60.96
p_in = (25.4, y)
S.glabel(p_in, "VBUS_PAD", "left", shape="input")
S.flag((30.48, y), "up", 2)
S.junction((30.48, y))
fb = S.place("Device:FerriteBead_Small", stock("Device", "FerriteBead_Small"), "FB101", "220R@100MHz 1.4A",
             38.1, y, rot=90, footprint="Inductor_SMD:L_0603_1608Metric",
             fields={"MPN": "BLM18PG221SN1 class [U]"}, ref_off=(0, -3), val_off=(0, 3.5))
S.wire(p_in, fb.pin(1))
n1 = (53.34, y)
S.wire(fb.pin(2), n1)
tvs = S.place("Device:D_TVS", stock("Device", "D_TVS"), "D101", "ESD 6V", 53.34, 71.12, rot=90,
              footprint="Diode_SMD:D_SOD-523", fields={"MPN": "TPD1E10B06 class [U]"},
              ref_off=(7, -1.3), val_off=(7, 1.3))
S.wire(n1, tvs.pin(2))
S.junction(n1)
S.gnd(tvs.pin(1))
q = S.place("Transistor_FET:Q_PMOS_GSD", stock("Transistor_FET", "Q_PMOS_GSD"), "Q101", "P-FET -30V",
            76.2, y + 2.54, rot=90, footprint="Package_TO_SOT_SMD:SOT-23",
            fields={"MPN": "DMP3099L class [U]"}, ref_off=(-3, -8), val_off=(-3, -5.5))
S.wire(n1, q.pin(3))                        # D <- pad side
g = q.pin(1)                                # gate (points down)
gnode = (g[0], g[1] + 5.08)
S.wire(g, gnode)
r101 = res("R101", "1M", g[0], gnode[1] + 6.35)
S.wire(gnode, r101.pin(1))
S.gnd(r101.pin(2))
zx = 91.44
z = S.place("Device:D_Zener", stock("Device", "D_Zener"), "D102", "12V", zx, y + 10.16, rot=270,
            footprint="Diode_SMD:D_SOD-523", fields={"MPN": "BZX585-C12 class [U]"},
            ref_off=(6, -1.3), val_off=(6, 1.3))
S.wire(q.pin(2), (zx, y))                   # S -> zener cathode column
S.wire((zx, y), z.pin(1))
S.junction((zx, y))
S.link(z.pin(2), (zx, gnode[1]), "v")
S.wire((zx, gnode[1]), gnode)
S.junction(gnode)
cx = 106.68
c101 = cap("C101", "2.2uF 35V", cx, y + 6.35, fp=C0603, fields={"MPN": ">=1 uF effective at 5 V, 35 V X5R"})
S.wire((zx, y), (cx, y), c101.pin(1))
S.junction((cx, y))
S.gnd(c101.pin(2))
fx = 119.38
S.wire((cx, y), (fx, y), (134.62, y))
S.flag((fx, y), "up", 2)
S.junction((fx, y))
S.label((134.62, y), "VBUS_IN", "right")
S.text((19, 90), "FB101 + D101: ferrite slows fast edges, D101 clamps ESD/hot-plug spikes. 5 V-only dock, so\n"
                 "D101 works at >= 5.5 V and never conducts in normal use (spec 9.1).\n"
                 "Q101 reverse-polarity: drain faces the pad; the body diode conducts first, then VGS = -5 V\n"
                 "turns the channel fully on. A reversed head leaves VGS = 0, so it stays off.\n"
                 "D102 limits VGS to 12 V if a wrong adapter is applied; R101 pulls the gate to GND.\n"
                 "C101: the charger's input cap (>= 1 uF after DC-bias derating, <= 10 uF - SLUSFJ3 8.2.2).", NOTE)

# ================================================================== B. charger
S.box((160, 20), (290, 125), "B · Charger + power path — BQ25188  (I2C 0x6A)")
ux, uy = 220.98, 63.5
u1 = custom("BQ25188", "U101", ux, uy, "BQ25188YBGR")
S.net(u1.pin("A2"), "VBUS_IN", "left", 6)
S.gnet(u1.pin("D1"), "TS_MR", "left", 6)
S.gnet(u1.pin("B1"), "SCL", "left", 6)
S.gnet(u1.pin("C1"), "SDA", "left", 6)
S.gnet(u1.pin("A1"), "BQ_INT", "left", 6, shape="output")
S.gnd(u1.pin("D2"))
sysn = S.stub(u1.pin("B2"), "right", 6)
S.rail(sysn, "VSYS", "up", 2)
c102 = cap("C102", "10uF 10V", sysn[0] + 22.86, sysn[1] + 5.08, fp=C0603)
S.link(sysn, c102.pin(1))
S.junction(sysn)
S.gnd(c102.pin(2))
batn = S.stub(u1.pin("C2"), "right", 6)
c103 = cap("C103", "1uF 10V", batn[0], batn[1] + 5.08)
S.wire(batn, c103.pin(1))
S.gnd(c103.pin(2))
S.wire(batn, (batn[0] + 7.62, batn[1]))
S.junction(batn)
S.rail((batn[0] + 7.62, batn[1]), "VBAT", "up", 2)
S.text((164, 90), "SYS -> VSYS feeds the whole device; BAT is the cell. Firmware boot rules (SLUSFJ3):\n"
                  " - SYS_REG_CTRL = 000 (VBAT + 225 mV): default is 4.5 V = AMOLED PMIC VIN max\n"
                  " - WATCHDOG_SEL off (else registers reset every 160 s)\n"
                  " - long press -> HW reset at 15-20 s (default: ship mode after 5 s!)\n"
                  " - ICHG 300 mA only after a valid NTC read (power-up default 10 mA)\n"
                  "~INT is a 128 us pulse: catch the edge on GPIOTE, then read STAT0/FLAG0.", NOTE)

# ================================================================== E. 3.1 V rail
S.box((300, 20), (405, 125), "E · V3 = 3.1 V rail — TPS62840")
tx, ty = 346.71, 60.96
u3 = custom("TPS62840DLC", "U103", tx, ty, "TPS62840DLCR")
vin = S.stub(u3.pin("2"), "left", 8)
en = S.stub(u3.pin("4"), "left", 8)
S.wire(en, vin)
S.junction(vin)
S.rail(vin, "VSYS", "up", 2)
c105 = cap("C105", "4.7uF 10V", vin[0] - 7.62, vin[1] + 6.35, fields={"MPN": "GRM155R61A475MEAA"})
S.link(vin, c105.pin(1))
S.gnd(c105.pin(2))
m = S.stub(u3.pin("3"), "left", 3)
st = S.stub(u3.pin("6"), "left", 3)
S.wire(m, st)
S.junction(st)
S.gnd(st, "left", 2)
vs = S.stub(u3.pin("5"), "left", 3)
r106 = res("R106", "71.5k 1%", vs[0], vs[1] + 5.08 + 1.27, fields={"MPN": "E96 1%, <=200 ppm/C"})
S.wire(vs, r106.pin(1))
S.gnd(r106.pin(2))
S.gnd(u3.pin("1"))
sw = S.stub(u3.pin("7"), "right", 2)
l1 = S.place("Device:L", L, "L101", "2.2uH", sw[0] + 6.35, sw[1], rot=90,
             footprint="Bingbong_v3:L_Murata_DFE201210S", fields={"MPN": "DFE201210S-2R2M (1.0 mm tall)"},
             ref_off=(-2.5, -2.8), val_off=(-2.5, 3.2))
S.wire(sw, l1.pin(1))
vo = (l1.pin(2)[0] + 7.62, sw[1])
S.wire(l1.pin(2), vo)
vos = S.stub(u3.pin("8"), "right", 2)
S.link(vos, (vo[0], vos[1]))
S.wire((vo[0], vos[1]), vo)
S.junction(vo)
c106 = cap("C106", "10uF 4V", vo[0] + 7.62, vos[1] + 5.08, fields={"MPN": "GRM155R60G106ME44"})
S.wire((vo[0], vos[1]), (c106.pin(1)[0], vos[1]), c106.pin(1))
S.junction((vo[0], vos[1]))
S.gnd(c106.pin(2))
S.rail(vo, "V3", "up", 2)
S.flag((c106.pin(1)[0], vos[1]), "up", 2)
S.text((304, 90), "RSET 71.5 k -> 3.1 V (SLVSEC6D Table 1, verified;\n"
                  "102 k -> 3.2 V if sensor margin needs it). The chip reads RSET\n"
                  "once at start-up: VSET trace < 5 mm, no cap on it.\n"
                  "EN tied to VSYS: V3 is always on.\n"
                  "MODE low = power-save (60 nA IQ). STOP low = normal.\n"
                  "VOS senses V3 on its own trace at C106.", NOTE)

# ================================================================== C. cell, NTC, crown button
S.box((15, 135), (150, 255), "C · Cell connector, NTC and crown button (TS/MR)")
S.text((19, 142), "The BQ25188 has ONE pin for both the battery NTC and the push-button (TS/MR).\n"
                  "A press must pull TS/MR below 90 mV; released, the pin must read the NTC.", NOTE)
jx, jy = 30.48, 170.18
j = S.place("Connector_Generic:Conn_01x03", stock("Connector_Generic", "Conn_01x03"), "J101", "CELL 3P",
            jx, jy, mirror=True, footprint="Bingbong_v3:CELL_B2B_3P_TBD",
            fields={"MPN": "cell 3-way B2B, pinout per cell vendor [U]"}, ref_off=(-3, -6), val_off=(-3, 6.5))
bplus, ntc, bminus = j.pin(1), j.pin(2), j.pin(3)
vb = (bplus[0] + 7.62, bplus[1])
S.wire(bplus, vb)
S.rail(vb, "VBAT", "up", 2)
bm = (bminus[0] + 5.08, bminus[1])
S.wire(bminus, bm)
S.gnd(bm, "down", 2)
tsn = (68.58, ntc[1])
S.wire(ntc, (55.88, ntc[1]))
S.glabel((55.88, ntc[1]), "TS_MR", "right")
S.wire((55.88, ntc[1]), tsn)
r103 = res("R103", "10k DNP", tsn[0], tsn[1] + 6.35, dnp=True)
S.wire(tsn, r103.pin(1))
S.gnd(r103.pin(2))
q2 = S.place("Transistor_FET:Q_NMOS_GSD", stock("Transistor_FET", "Q_NMOS_GSD"), "Q102", "N-FET",
             111.76, ntc[1] + 5.08, footprint="Package_TO_SOT_SMD:SOT-523",
             fields={"MPN": "Vth <= 1 V, IDSS <= 100 nA @ 2 V [U]"}, ref_off=(4.5, -1), val_off=(4.5, 1.5))
S.wire(tsn, q2.pin(3))
S.junction(tsn)
S.gnd(q2.pin(2))
gq = (q2.pin(1)[0] - 5.08, q2.pin(1)[1])
S.wire(q2.pin(1), gq)
S.junction(gq)
S.wire(gq, (gq[0] - 7.62, gq[1]))
S.glabel((gq[0] - 7.62, gq[1]), "TACT_HI", "left", shape="input")
r104 = res("R104", "470k", gq[0], gq[1] + 6.35)
S.wire(gq, r104.pin(1))
tn = (gq[0], r104.pin(2)[1] + 2.54)
S.wire(r104.pin(2), tn)
r105 = res("R105", "1M", gq[0], tn[1] + 3.81 + 2.54)
S.wire(tn, r105.pin(1))
S.gnd(r105.pin(2))
S.junction(tn)
S.wire(tn, (tn[0] + 12.7, tn[1]))
S.glabel((tn[0] + 12.7, tn[1]), "TACT_NRF", "right", shape="output")
S.text((19, 205), "J101: B+ / NTC / B-. The 10 k B3435 NTC is bonded to the cell (JEITA charging window).\n"
                  "Return the NTC to U101 GND directly (kelvin, SLUSFJ3 8.2.2).\n"
                  "Crown press: the satellite tact connects VBAT (via R517 10 k, UI sheet) to TACT_HI -> Q102 turns on\n"
                  "and pulls TS/MR to ~0 V. Released: R104+R105 hold Q102 off, the NTC reads normally.\n"
                  "Works in ship mode (VBAT is always there): wake and long-press reset need no firmware.\n"
                  "R104/R105 divide TACT_HI (3.45-4.35 V) to 2.35-2.96 V for the nRF (TACT_NRF, P0.17):\n"
                  "above its 2.17 V logic-high, below its 3.4 V limit; current flows only while pressed.\n"
                  "R103 = DNP. Fit it ONLY for a cell without an NTC (datasheet: 10 k to GND disables TS).", NOTE)

# ================================================================== D. fuel gauge
S.box((160, 135), (290, 255), "D · Fuel gauge — MAX17048  (I2C 0x36)")
gx, gy = 228.6, 180.34
u2 = custom("MAX17048", "U102", gx, gy, "MAX17048G+T10")
vdd = S.stub(u2.pin("A3"), "left", 8)
cel = S.stub(u2.pin("A2"), "left", 8)
S.wire(cel, vdd)
S.junction(vdd)
S.rail(vdd, "VBAT", "up", 2)
c104 = cap("C104", "100nF", vdd[0] - 7.62, vdd[1] + 6.35)
S.link(vdd, c104.pin(1))
S.gnd(c104.pin(2))
ctg = S.stub(u2.pin("A1"), "left", 4)
qs = S.stub(u2.pin("B3"), "left", 4)
S.wire(ctg, qs)
S.junction(qs)
S.gnd(qs, "down", 2)
S.gnd(u2.pin("A4"))
S.gnet(u2.pin("B1"), "SDA", "right", 6)
S.gnet(u2.pin("B2"), "SCL", "right", 6)
S.gnet(u2.pin("B4"), "GAUGE_ALRT", "right", 6, shape="output")
S.text((164, 212), "VDD is both the supply and the cell-voltage sense, so it sits on VBAT (not V3):\n"
                   "the gauge keeps tracking with the buck off. CELL is not connected inside the\n"
                   "MAX17048; it is tied to VBAT as in the typical circuit.\n"
                   "CTG and QSTRT -> GND per the datasheet. ~ALRT = low-charge alert to the nRF.\n"
                   "Good % accuracy needs ADI's custom battery model (firmware, not hardware).", NOTE)

# ================================================================== F. VSYS reservoir
S.box((300, 135), (405, 255), "F · VSYS reservoir for LTE bursts")
for i, ref in enumerate(("C107", "C108")):
    c = cap(ref, "22uF 10V", 325.12 + i * 25.4, 180.34, fp=C0805)
    S.rail(c.pin(1), "VSYS", "up", 2)
    S.gnd(c.pin(2))
for i, (net, fx) in enumerate((("VBAT", 330.2), ("GND", 355.6))):
    pt = (fx, 235.0)
    if net == "GND":
        S.gnd(pt, "down", 0)
        S.flag(pt, "up", 2)
    else:
        S.rail(pt, net, "up", 0)
        S.wire(pt, (pt[0] + 7.62, pt[1]))
        S.flag((pt[0] + 7.62, pt[1]), "up", 0)
S.text((304, 242), "PWR_FLAGs mark where VBAT (cell) and GND enter the design,\n"
                   "so KiCad's ERC knows these nets are really powered.", NOTE)
S.text((304, 212), "2 x 22 uF 0805 in the side strips, next to the\n"
                   "nRF9151 VDD pins. They supply the modem's ~395 mA\n"
                   "TX bursts so VSYS does not dip toward the\n"
                   "3.45 V cutoff (report 5.5, C-19).", NOTE)

# ================================================================== legend
S.text((15, 262), "Interfaces   in: VBUS_PAD (dock), TACT_HI (satellite)    out: BQ_INT, GAUGE_ALRT, TACT_NRF    bus: SDA, SCL (pull-ups on nrf9151 sheet)\n"
                  "Rails made here: VSYS 3.45-4.43 V · VBAT (cell) · V3 3.1 V · VBUS_IN (local)    Refs 1xx    [U] = part class chosen, MPN not final", 1.4)

S.write()
write_custom_lib(CUSTOM)
print("wrote power.kicad_sch")

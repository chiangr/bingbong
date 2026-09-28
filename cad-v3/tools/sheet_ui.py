"""Sheet 5 — user interface: grip sense, haptics, halo, SPI NOR, crown satellite connector. Refs 5xx."""
from schgen import Sheet, stock, root_paths, write_custom_lib
from parts import CUSTOM

R0402 = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"
C0603 = "Capacitor_SMD:C_0603_1608Metric"
NOTE = 1.27

S = Sheet("ui.kicad_sch", "Sheet 5 — UI: grip, haptics, halo, flash, crown satellite", root_paths()["ui.kicad_sch"])
R, C = stock("Device", "R"), stock("Device", "C")


def res(ref, val, x, y, rot=0, **kw):
    off = dict(ref_off=(0, -2.8), val_off=(0, 3.2)) if rot == 90 else {}
    off.update(kw.pop("off", {}))
    return S.place("Device:R", R, ref, val, x, y, rot=rot, footprint=kw.pop("fp", R0402), **off, **kw)


def cap(ref, val, x, y, fp=C0402, **kw):
    return S.place("Device:C", C, ref, val, x, y, footprint=fp, **kw)


def ic(name, ref, x, y, mpn, unit=1):
    t = S.place(f"Bingbong_v3:{name}", CUSTOM[name], ref, mpn, x, y, ref_off=(0, 0), val_off=(0, 0), unit=unit)
    S.items.pop()
    top = any(v[2] == 270 for v in t.lib_pins.values())
    ro = (3.0, -t.half_h - 5.5) if top else (-t.half_w, -t.half_h - 4.2)
    vo = (3.0, -t.half_h - 3.0) if top else (-t.half_w, -t.half_h - 1.6)
    return S.place(f"Bingbong_v3:{name}", CUSTOM[name], ref, mpn, x, y, fields={"MPN": mpn},
                   ref_off=ro, val_off=vo, unit=unit)


def cap_group(net, items, x0, y0, rail=False, dx=10.16):
    """Row of caps from `net` (local label, or a rail if rail=True) to GND."""
    for i, (ref, val, fp) in enumerate(items):
        c = cap(ref, val, x0 + i * dx, y0, fp=fp)
        if rail:
            S.rail(c.pin(1), net, "up", 2)
        else:
            S.net(c.pin(1), net, "up", 2)
        S.gnd(c.pin(2))


def pullup(ref, val, x, y, net, rail="V3", glob=True):
    r = res(ref, val, x, y)
    S.rail(r.pin(1), rail, "up", 2)
    (S.gnet if glob else S.net)(r.pin(2), net, "down", 3)


# ============================================================ A. grip sensor
S.box((15, 20), (140, 128), "A · Grip / presence — IQS211B (own I2C bus, 0x47)")
u1 = ic("IQS211B", "U501", 71.12, 55.88, "IQS211B-00000000-TSR")
S.net(u1.pin("5"), "IQS_VDD", "left", 4)
S.net(u1.pin("4"), "IQS_VREG", "left", 4)
S.gnet(u1.pin("1"), "IQS_SCL", "left", 4)
S.gnet(u1.pin("3"), "IQS_SDA", "left", 4)
S.gnd(u1.pin("2"))
cx = S.stub(u1.pin("6"), "right", 4)
c505 = cap("C505", "10pF C0G", cx[0], cx[1] + 5.08)
S.wire(cx, c505.pin(1))
S.gnd(c505.pin(2))
S.junction(cx)
r504 = res("R504", "2k2", cx[0] + 13.97, cx[1], rot=90)
S.wire(cx, r504.pin(1))
e = S.place("Connector_Generic:Conn_01x01", stock("Connector_Generic", "Conn_01x01"), "E501", "GRIP RING",
            r504.pin(2)[0] + 10.16, cx[1], rot=180, footprint="Bingbong_v3:SpringContact_TBD",
            fields={"MPN": "spring contact to buried 316L ring [U]"}, ref_off=(0, -3), val_off=(0, 3.5))
S.wire(r504.pin(2), e.pin(1))
# supply group
yg = 95.25
S.rail((22.86, yg), "V3", "up", 0)
r501 = res("R501", "40R", 30.48, yg, rot=90)
S.wire((22.86, yg), r501.pin(1))
S.wire(r501.pin(2), (38.1, yg))
S.label((38.1, yg), "IQS_VDD", "up")
S.flag((38.1, yg), "down", 2)
cap_group("IQS_VDD", (("C501", "2.2uF", C0402), ("C502", "100pF", C0402)), 45.72, yg + 7.62)
S.wire((38.1, yg), (45.72, yg), (45.72, yg + 1.27 + 2.54 * 0))
cap_group("IQS_VREG", (("C503", "4.7uF", C0402), ("C504", "100pF", C0402)), 71.12, yg + 7.62)
pullup("R505", "4.7k", 104.14, yg + 3.81, "IQS_SCL")
pullup("R506", "4.7k", 119.38, yg + 3.81, "IQS_SDA")
S.text((19, 27), "Detects a hand around the body. Its sense pin (Cx) measures the capacitance of a metal ring\n"
                 "buried inside the crown-end wall (E501 is the spring contact to that ring).", NOTE)
S.text((85, 70), "R504 2k2 + C505 10 pF: low-pass so\n"
                 "the 700 MHz / 23 dBm LTE burst is not\n"
                 "rectified into false touches (report 5.13).\n"
                 "Firmware also blanks it on COEX0.", NOTE)
S.text((19, 116), "R501 40R: Azoteq's latch-up guard. Caps per Azoteq Table 2.4 for the 160 ms low-power scan.\n"
                  "No separate RDY pin: RDY rides on SCL, so it gets its own bus (P0.12/P0.18).", NOTE)

# ============================================================ B. haptics
S.box((150, 20), (290, 128), "B · Haptics — DRV2625 -> 170 Hz LRA (main I2C, 0x5A)")
u2 = ic("DRV2625", "U502", 213.36, 60.96, "DRV2625YFFR")
S.rail(S.stub(u2.pin("C2"), "left", 3), "VSYS", "up", 2)
nr = S.stub(u2.pin("B2"), "left", 8)
S.glabel(nr, "HAPTIC_NRST", "left", shape="input")
r507 = res("R507", "100k", nr[0] + 3.81, nr[1] + 6.35)
S.wire((nr[0] + 3.81, nr[1]), r507.pin(1))
S.junction((nr[0] + 3.81, nr[1]))
S.gnd(r507.pin(2))
S.gnet(u2.pin("A1"), "HAPTIC_TRIG", "left", 4, shape="input")
S.gnet(u2.pin("B1"), "SDA", "left", 4)
S.gnet(u2.pin("C1"), "SCL", "left", 4, shape="input")
S.gnd(u2.pin("B3"))
reg = S.stub(u2.pin("A2"), "right", 3)
c508 = cap("C508", "100nF", reg[0], reg[1] + 5.08)
S.wire(reg, c508.pin(1))
S.gnd(c508.pin(2))
j2 = S.place("Connector_Generic:Conn_01x02", stock("Connector_Generic", "Conn_01x02"), "J502", "LRA",
             262.89, u2.pin("A3")[1] + 2.54, footprint="Bingbong_v3:LRA_pads_TBD",
             fields={"MPN": "Vybronics VG0840001D leads"}, ref_off=(4, -4), val_off=(4, 4.5))
op = S.stub(u2.pin("A3"), "right", 4)
on = S.stub(u2.pin("C3"), "right", 4)
S.link(op, j2.pin(1))
S.link(on, j2.pin(2))
S.gnet(op, "LRA_P", "up", 3)
S.gnet(on, "LRA_N", "down", 3)
S.junction(op)
S.junction(on)
cap_group("VSYS", (("C506", "100nF", C0402), ("C507", "10uF", C0603)), 170.18, 100.33, rail=True)
S.text((154, 27), "Drives the linear resonant actuator (the 'other person' feel: boop, purr, taps) with\n"
                  "closed-loop braking. OUT+/OUT- are a differential pair to the LRA at X = 52-60.", NOTE)
S.text((154, 112), "NRST low = shutdown (105 nA) - R507 keeps it off until firmware wakes it (P0.25).\n"
                   "C506 0.1 uF required + C507 10 uF bulk at VDD; C508 0.1 uF on the 1.8 V REG pin.", NOTE)

# ============================================================ C. halo
S.box((300, 20), (405, 128), "C · Halo RGB (common anode to VSYS)")
led = S.place("Device:LED_RAGB", stock("Device", "LED_RAGB"), "D501", "RGB PLCC-4", 322.58, 55.88, mirror=True,
              footprint="Bingbong_v3:LED_RGB_PLCC4_1.6x1.6", fields={"MPN": "1.6x1.6 PLCC-4 common-anode RGB [U]"},
              ref_off=(-3, -9.5), val_off=(-3, 9.5))
S.rail(S.stub(led.pin("2"), "left", 3), "VSYS", "up", 2)
for pin, net in (("1", "LED_RK"), ("3", "LED_GK"), ("4", "LED_BK")):   # LED_RAGB: 1 RK, 3 GK, 4 BK, 2 A
    S.net(led.pin(pin), net, "right", 4)
cap_group("LED_RK", (("C510", "10nF", C0402),), 358.14, 50.8)
cap_group("LED_GK", (("C511", "10nF", C0402),), 373.38, 50.8)
cap_group("LED_BK", (("C512", "10nF", C0402),), 388.62, 50.8)
for i, (col, rv, lab) in enumerate((("R", "330R", "LED_RK"), ("G", "150R", "LED_GK"), ("B", "150R", "LED_BK"))):
    x = 327.66 + i * 30.48
    rr = res(f"R5{10 + i}", rv, x + 2.54, 78.74)
    S.net(rr.pin(1), lab, "up", 2)
    q = S.place("Transistor_FET:Q_NMOS_GSD", stock("Transistor_FET", "Q_NMOS_GSD"), f"Q50{1 + i}", "N-FET",
                x, rr.pin(2)[1] + 5.08 + 2.54, footprint="Package_TO_SOT_SMD:SOT-523",
                fields={"MPN": "DMG1012T class [U]"}, ref_off=(4.5, -1), val_off=(4.5, 1.5))
    S.wire(rr.pin(2), q.pin(3))
    S.gnd(q.pin(2))
    gn = S.stub(q.pin(1), "left", 2)
    rg = res(f"R52{i}", "100k", gn[0], gn[1] + 6.35)
    S.wire(gn, rg.pin(1))
    S.gnd(rg.pin(2))
    S.junction(gn)
    gl = (gn[0] - 3.81, gn[1])
    S.wire(gn, gl)
    S.glabel(gl, f"LED_{col}", "left", shape="input")
S.text((304, 27), "Fires into the polymer split ring (the light guide). Three GPIO-driven FETs,\n"
                  "hardware PWM, zero standby current (no LED driver IC).", NOTE)
S.text((304, 112), "R values = ~5 mA at VSYS 3.7 V (red Vf ~2.0, green/blue ~3.0) [U]: set after the LED MPN.\n"
                   "Green/blue have little headroom at 3.45 V - firmware scales PWM by battery voltage.\n"
                   "C510-512 10 nF at the LED pins keep RF off the halo lines (the LED sits next to the\n"
                   "antenna feed). R520-522 hold the gates"
                   "low while the nRF's pins float during\nreset, so the halo never flickers at boot.", NOTE)

# ============================================================ D. SPI NOR
S.box((15, 138), (140, 262), "D · 16 Mbit SPI NOR — MX25R1635F (shared SPI with the display)")
u3 = ic("MX25R1635F", "U503", 71.12, 190.5, "MX25R1635FZUIL0")
S.gnet(u3.pin("1"), "NOR_CS", "left", 4, shape="input")
S.gnet(u3.pin("6"), "SPI_SCK", "left", 4, shape="input")
S.gnet(u3.pin("5"), "SPI_MOSI", "left", 4, shape="input")
S.gnet(u3.pin("2"), "SPI_MISO", "left", 4, shape="output")
wp = S.stub(u3.pin("3"), "right", 3)
rs = S.stub(u3.pin("7"), "right", 3)
S.wire(wp, rs)
S.rail(wp, "V3", "up", 2)
S.junction(wp)
S.rail(u3.pin("8"), "V3", "up", 2)
S.gnd(u3.pin("4"))
c509 = cap("C509", "100nF", 106.68, 190.5)
S.rail(c509.pin(1), "V3", "up", 2)
S.gnd(c509.pin(2))
S.text((19, 145), "Holds the second firmware image (MCUboot slot 1, for over-the-air updates) and the art/fonts.\n"
                  "The nRF9151's own 1 MB flash holds the running app. Deep power-down between uses.", NOTE)
S.text((19, 226), "WP# and RESET# tied to V3: single-I/O SPI only (4 wires), never write-protected in hardware.\n"
                  "MISO is shared with the display's SDO - the display sheet must keep an unpowered panel\n"
                  "from loading it.", NOTE)

# ============================================================ E. crown satellite connector
S.box((150, 138), (405, 262), "E · Crown satellite: 12-way 0.5 mm FFC, sensor power switch, filters")
j = S.place("Connector_Generic_MountingPin:Conn_01x12_MountingPin", stock("Connector_Generic_MountingPin", "Conn_01x12_MountingPin"),
            "J501", "FH12-12S-0.5SH", 172.72, 200.66, mirror=True,
            footprint="Connector_FFC-FPC:Hirose_FH12-12S-0.5SH_1x12-1MP_P0.50mm_Horizontal",
            fields={"MPN": "Hirose FH12-12S-0.5SH(55)"}, ref_off=(-3, -18), val_off=(-3, 19))
SAT = {1: "GND", 2: "V3", 3: "SENS_SDA", 4: "SENS_SCL", 5: "SENS_VDD", 6: "HA1_T", 7: "HA2_T", 8: "HB1_T",
       9: "HB2_T", 10: "TACT_HI", 11: "TACT_SRC", 12: "GND"}
for pin, net in SAT.items():
    p = j.pin(pin)
    if net == "GND":
        S.gnd(S.stub(p, "right", 2), "right", 0)
    elif net == "V3":
        S.rail(S.stub(p, "right", 6), "V3", "up", 2)
    elif net in ("SENS_SDA", "SENS_SCL", "TACT_HI"):
        S.gnet(p, net, "right", 4)
    else:
        S.net(p, net, "right", 4)
S.gnd(S.stub(j.pin("MP"), "down", 1), "down", 0)
# latch filters
for i, n in enumerate(("HA1", "HA2", "HB1", "HB2")):
    y = 170.18 + i * 12.7
    S.label((210.82, y), f"{n}_T", "left")
    rr = res(f"R51{3 + i}", "100R", 218.44, y, rot=90)
    S.wire((210.82, y), rr.pin(1))
    node = (rr.pin(2)[0] + 5.08, y)
    S.wire(rr.pin(2), node, (node[0] + 7.62, y))
    S.junction(node)
    cc = cap(f"C51{3 + i}", "47pF", node[0], y + 5.08)
    S.wire(node, cc.pin(1))
    S.gnd(cc.pin(2))
    S.glabel((node[0] + 7.62, y), n, "right", shape="output")
# tact source
r517 = res("R517", "10k", 218.44, 226.06, rot=90)
S.rail(S.stub(r517.pin(1), "left", 2), "VBAT", "up", 2)
S.wire(r517.pin(2), (228.6, 226.06))
S.label((228.6, 226.06), "TACT_SRC", "right")
# sensor switch + bus pull-ups
u4 = ic("TPS22916", "U504", 314.96, 172.72, "TPS22916CYFPR")
S.rail(S.stub(u4.pin("A2"), "left", 3), "V3", "up", 2)
S.gnet(u4.pin("B2"), "SENSOR_SW_EN", "left", 4, shape="input")
S.gnd(u4.pin("B1"))
vo = S.stub(u4.pin("A1"), "right", 4)
S.label(vo, "SENS_VDD", "right")
c518 = cap("C518", "1uF", vo[0] + 12.7, vo[1] + 5.08)
S.net(c518.pin(1), "SENS_VDD", "up", 2)
S.gnd(c518.pin(2))
for i, (ref, net) in enumerate((("R518", "SENS_SDA"), ("R519", "SENS_SCL"))):
    r = res(ref, "4.7k", 297.18 + i * 15.24, 215.9)
    S.net(r.pin(1), "SENS_VDD", "up", 2)
    S.gnet(r.pin(2), net, "down", 3)
S.text((154, 145), "Satellite = 22 x 10 mm board in the crown: angle sensor (MT6701 or AS5600L), two DRV5032 Hall latches,\n"
                   "tact switch, crown ESD bleed. GND on pins 1 and 12 carries the crown's ESD return (report C-24).", NOTE)
S.text((236, 240), "HA/HB: always-on Hall latches wake the nRF on the first crown motion; 100R + 47 pF filter them.\n"
                   "TACT: VBAT -> R517 -> tail -> tact -> TACT_HI (power sheet reads it). R517 limits a tail short to 0.4 mA.\n"
                   "Angle sensor: 10 mA, so U504 powers it only while the crown is moving. It has its OWN I2C bus,\n"
                   "pulled up to SENS_VDD: switched off, the bus is dead too - nothing clamps the main bus.", NOTE)

S.text((15, 268), "Interfaces   I2C main: SDA/SCL (DRV2625)   IQS_SCL/IQS_SDA   SENS_SCL/SENS_SDA   SPI: SPI_SCK/MOSI/MISO, NOR_CS   GPIO: HAPTIC_TRIG/NRST, LED_R/G/B, HA1/HA2/HB1/HB2, SENSOR_SW_EN   out: TACT_HI\n"
                  "Rails in: VSYS, V3, VBAT   Refs 5xx   [U] = part class chosen, MPN not final", 1.4)
S.write()
write_custom_lib(CUSTOM)
print("wrote ui.kicad_sch")

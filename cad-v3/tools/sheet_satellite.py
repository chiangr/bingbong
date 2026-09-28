"""Crown satellite board (separate PCB, 22 x 10 x 0.6 mm, 2-layer).

usage: python3 sheet_satellite.py [A|B]     A = MT6701 (satellite/), B = AS5600L (satellite_b/)
Both variants share the tail pinout (= main-board J501), latches, tact and ESD bleed; only block B differs.
Refs are board-local (U1, C1 ...).
"""
import sys
from schgen import Sheet, stock, root_paths, write_custom_lib
from parts import CUSTOM

R0402 = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"
NOTE = 1.1

VARIANT = (sys.argv[1:] or ["A"])[0].upper()
PRJ, DIR = {"A": ("satellite_v3", "satellite"), "B": ("satellite_b_v3", "satellite_b")}[VARIANT]
TITLE = {"A": "Crown satellite — variant A (MT6701 angle sensor)",
         "B": "Crown satellite — variant B (AS5600L angle sensor)"}[VARIANT]
S = Sheet("satellite.kicad_sch", TITLE, root_paths(PRJ, DIR)["satellite.kicad_sch"], project=PRJ, subdir=DIR)
R, C = stock("Device", "R"), stock("Device", "C")


def ic(name, ref, x, y, mpn):
    t = S.place(f"Bingbong_v3:{name}", CUSTOM[name], ref, mpn, x, y, ref_off=(0, 0), val_off=(0, 0))
    S.items.pop()
    return S.place(f"Bingbong_v3:{name}", CUSTOM[name], ref, mpn, x, y, fields={"MPN": mpn},
                   ref_off=(-t.half_w, -t.half_h - 4.2), val_off=(-t.half_w, -t.half_h - 1.6))


def cap(ref, val, x, y, net, **kw):
    c = S.place("Device:C", C, ref, val, x, y, footprint=C0402, **kw)
    S.rail(c.pin(1), net, "up", 2)
    S.gnd(c.pin(2))
    return c


# ============================================================ A. tail
S.box((15, 20), (150, 140), "A · Tail to the main board (12-way 0.5 mm FFC)")
j = S.place("Connector_Generic_MountingPin:Conn_01x12_MountingPin",
            stock("Connector_Generic_MountingPin", "Conn_01x12_MountingPin"), "J1", "FH12-12S-0.5SH", 38.1, 76.2,
            mirror=True, footprint="Connector_FFC-FPC:Hirose_FH12-12S-0.5SH_1x12-1MP_P0.50mm_Horizontal",
            fields={"MPN": "Hirose FH12-12S-0.5SH(55)"}, ref_off=(-3, -18), val_off=(-3, 19))
TAIL = {1: "GND", 2: "V3", 3: "SENS_SDA", 4: "SENS_SCL", 5: "SENS_VDD", 6: "HA1", 7: "HA2", 8: "HB1",
        9: "HB2", 10: "TACT_HI", 11: "TACT_SRC", 12: "GND"}
for pin, net in TAIL.items():
    p = j.pin(pin)
    if net == "GND":
        S.gnd(S.stub(p, "right", 2), "right", 0)
    elif net in ("V3", "SENS_VDD"):
        S.rail(S.stub(p, "right", 18 if net == "V3" else 24), net, "up", 2)
    else:
        S.net(p, net, "right", 4)
S.gnd(S.stub(j.pin("MP"), "down", 1), "down", 0)
for i, net in enumerate(("V3", "SENS_VDD", "GND")):
    pt = (60.96 + i * 27.94, 130.81)
    if net == "GND":
        S.gnd(pt, "down", 0)
    else:
        S.rail(pt, net, "up", 0)
    S.wire(pt, (pt[0] + 12.7, pt[1]))
    S.flag((pt[0] + 12.7, pt[1]), "down" if net != "GND" else "up", 0)
S.text((19, 27), "Same pin order as main-board J501 (ui sheet). Pins 1 and 12 are GND so the crown's ESD\n"
                 "current returns on both edges of the cable.", NOTE)
S.text((19, 106), "FFC ORIENTATION CHECK: a same-side-contact (Type A) FFC between two bottom-contact\n"
                  "FH12s can reverse the pin order (1 <-> 12) depending on how the boards face each\n"
                  "other. Freeze cable type + connector orientation on the 3D model before layout,\n"
                  "then confirm pin 1 = pin 1 end to end.", NOTE)

# ============================================================ B. angle sensor
def sensor_mt6701():
    S.box((160, 20), (405, 140), "B · Crown angle — MT6701 (14-bit, I2C 0x06), on the crown axis")
    u1 = ic("MT6701QT", "U1", 238.76, 76.2, "MT6701QT-STD")
    vd = S.stub(u1.pin("13"), "left", 8)
    S.rail(vd, "SENS_VDD", "up", 2)
    md = S.stub(u1.pin("14"), "left", 8)
    zz = S.stub(u1.pin("8"), "left", 8)
    S.wire(vd, md, zz)
    S.junction(md)
    S.junction(vd)
    S.net(u1.pin("6"), "SENS_SDA", "left", 4)
    S.net(u1.pin("7"), "SENS_SCL", "left", 4)
    for pin in ("15", "5", "11", "12", "9", "1", "2", "3", "4", "10"):
        S.noconn(u1.pin(pin))
    S.gnd(u1.pin("16"))
    S.noconn(u1.pin("EP"))          # exposed pad: soldered, deliberately unconnected (datasheet silent)
    cap("C1", "100nF", 185.42, 116.84, "SENS_VDD")
    tv = S.place("Device:D_TVS", stock("Device", "D_TVS"), "D1", "6V DNP", 200.66, 116.84, rot=90, dnp=True,
                 footprint="Diode_SMD:D_SOD-523", fields={"MPN": "6 V TVS, MagnTek 'recommended' [U]"},
                 ref_off=(7.5, -1.3), val_off=(7.5, 1.3))
    S.rail(tv.pin(2), "SENS_VDD", "up", 2)
    S.gnd(tv.pin(1))
    S.text((164, 27), "Reads the absolute angle of the 6 x 2.5 mm diametric magnet in the crown hub (sensor centred on the\n"
                      "axis to 0.3 mm). Powered only while the crown moves (SENS_VDD switched on the main board).", NOTE)
    S.text((280, 60), "MODE (14) and Z (8) tied to VDD = I2C mode\n"
                      "(MagnTek Figure 18). Both have internal\n"
                      "200 k pull-ups; the ties make it certain.\n\n"
                      "OUT, PUSH, U/V/W: other output modes,\n"
                      "unused -> left open.\n\n"
                      "SDA/SCL pull-ups (4.7 k) are on the\n"
                      "main board, fed from SENS_VDD.", NOTE)
    S.text((164, 126), "C1 at pin 13. D1 = MagnTek's optional VDD TVS, footprint only.\n"
                       "EEPROM setup (zero angle, direction) needs VDD > 4.5 V: done once on a fixture through J1.", NOTE)


def sensor_as5600l():
    S.box((160, 20), (405, 140), "B · Crown angle — AS5600L (12-bit, I2C 0x40), on the crown axis")
    u1 = ic("AS5600L_WLCSP", "U1", 238.76, 76.2, "AS5600L-AWLM")
    v5 = S.stub(u1.pin("A3"), "left", 8)
    v3 = S.stub(u1.pin("C3"), "left", 8)
    S.wire(v5, v3)
    S.junction(v5)
    S.rail(v5, "SENS_VDD", "up", 2)
    S.net(u1.pin("D1"), "SENS_SDA", "left", 4)
    S.net(u1.pin("B1"), "SENS_SCL", "left", 4)
    S.gnd(S.stub(u1.pin("A1"), "left", 3), "down", 0)
    S.noconn(u1.pin("E1"))
    for pin in ("D3", "B2", "B3", "C2", "D2"):
        S.noconn(u1.pin(pin))
    ends = [S.stub(u1.pin(p), "down", 2) for p in ("E3", "A2", "C1", "E2")]
    S.wire(*ends)
    for e_ in ends[1:]:
        S.junction(e_)
    S.gnd(ends[0], "down", 2)
    cap("C1", "100nF", 185.42, 116.84, "SENS_VDD")
    c4 = S.place("Device:C", C, "C4", "10uF DNP", 200.66, 116.84, footprint="Capacitor_SMD:C_0603_1608Metric", dnp=True,
                 fields={"MPN": "only for OTP programming (ams Figure 14)"})
    S.rail(c4.pin(1), "SENS_VDD", "up", 2)
    S.gnd(c4.pin(2))
    S.text((164, 27), "Drop-in alternative to variant A (report 4.5): same magnet, same tail, same firmware bus - only the\n"
                      "sensor changes. Real Western distribution, so it is the sourcing hedge for the MT6701.", NOTE)
    S.text((280, 50), "3.3 V mode (ams Figure 14): VDD5V and VDD3V3\n"
                      "tied together, 100 nF. Range 3.0-3.6 V; our\n"
                      "3.1 V rail is inside it (switch R_on <= 0.5 R).\n\n"
                      "DIR to GND = angle increases clockwise.\n"
                      "Firmware normalises direction per variant.\n\n"
                      "TEST (A2, C1, E2) to GND - required.\n"
                      "PGO left open (internal pull-up = option A).\n"
                      "OUT (PWM) unused. NC balls: do not connect.\n\n"
                      "Firmware tells the variants apart by I2C\n"
                      "address: 0x06 = MT6701, 0x40 = AS5600L.", NOTE)
    S.text((164, 126), "C1 at the VDD balls. C4 10 uF is only needed while OTP-programming (3.3-3.5 V on the fixture).\n"
                       "12-bit = 0.088 deg per step, ~170 steps per 15-degree detent.", NOTE)


(sensor_mt6701 if VARIANT == "A" else sensor_as5600l)()

# ============================================================ C. Hall latches
S.box((15, 150), (200, 262), "C · Wake-on-rotation — 2 x DRV5032DU Hall latches (always on)")
for i, (ref, cref, o1, o2) in enumerate((("U2", "C2", "HA1", "HA2"), ("U3", "C3", "HB1", "HB2"))):
    y = 190.5 + i * 38.1
    u = ic("DRV5032DU", ref, 76.2, y, "DRV5032DUDMRR")
    S.rail(S.stub(u.pin("1"), "left", 4), "V3", "up", 2)
    S.net(u.pin("4"), o1, "right", 4)
    S.net(u.pin("3"), o2, "right", 4)
    g2 = S.stub(u.pin("2"), "down", 2)
    g5 = S.stub(u.pin("5"), "down", 2)
    S.wire(g2, g5)
    S.gnd(g2, "down", 2)
    cap(cref, "100nF", 50.8, y + 3.81, "V3")
S.text((19, 157), "Each DRV5032DU has two outputs: OUT1 switches on a north pole, OUT2 on a south pole (3.9 mT,\n"
                  "20 Hz sampling, 1.6 uA). Two of them, 90 degrees apart around the magnet, give four edges\n"
                  "per turn with direction -> the first twist wakes the nRF within <= 77 degrees (report 4.11).", NOTE)
S.text((120, 190), "Push-pull outputs: no pull-ups.\n"
                   "Thermal pad (5) to GND for\n"
                   "mechanical strength.\n"
                   "C2/C3: TI's >= 0.1 uF at VCC.", NOTE)

# ============================================================ D. tact
S.box((210, 150), (300, 262), "D · Press — tact switch")
sw = S.place("Switch:SW_Push", stock("Switch", "SW_Push"), "SW1", "TACT", 255.27, 205.74,
             footprint="Bingbong_v3:SW_Panasonic_EVPBB_TBD", fields={"MPN": "SMD tact >= 1.6 N, >= 300k cycles [U]"},
             ref_off=(0, -3.5), val_off=(0, 4))
S.net(sw.pin("1"), "TACT_SRC", "left", 4)
S.net(sw.pin("2"), "TACT_HI", "right", 4)
S.text((214, 157), "Pressed by the bulkhead pip when the crown\n"
                   "moves in 0.40 mm (off-axis, report 4.12).\n"
                   "TACT_SRC = VBAT through 10 k (main board).\n"
                   "Pressed -> TACT_HI = VBAT -> the charger\n"
                   "sees a button and the nRF sees TACT_NRF.", NOTE)
S.text((214, 225), "The switch carries battery voltage\n"
                   "(up to 4.35 V): rate it for >= 5 V.\n"
                   "Current only while pressed (~3 uA).", NOTE)

# ============================================================ E. crown ESD bleed
S.box((310, 150), (405, 262), "E · Crown ESD bleed")
e1 = S.place("Connector_Generic:Conn_01x01", stock("Connector_Generic", "Conn_01x01"), "E1", "CROWN LEAF",
             325.12, 205.74, footprint="Bingbong_v3:BeCu_leaf_pad_TBD",
             fields={"MPN": "BeCu leaf in the sleeve, touches the crown [U]"}, ref_off=(-3, -3), val_off=(-3, 4))
nd = (345.44, 205.74)
S.wire(e1.pin(1), nd)
r1 = S.place("Device:R", R, "R1", "1M", nd[0], nd[1] + 6.35, footprint=R0402)
S.wire(nd, r1.pin(1))
S.gnd(r1.pin(2))
d2 = S.place("Device:D_Zener", stock("Device", "D_Zener"), "D2", "TPD1E05U06", nd[0] + 15.24, nd[1] + 6.35, rot=270,
             footprint="Bingbong_v3:TI_DYA0002A_SOD-523", fields={"MPN": "TPD1E05U06DYAR"},
             ref_off=(9, -1.3), val_off=(15.5, 1.3))
S.wire(nd, (nd[0] + 15.24, nd[1]), d2.pin(1))   # pin 1 = K = I/O (TI DYA pin table)
S.junction(nd)
S.gnd(d2.pin(2))                                 # pin 2 = A = GND
S.text((314, 157), "The metal crown is the part a finger\n"
                   "touches most. It is otherwise floating:\n"
                   "R1 bleeds static away slowly, D2 clamps\n"
                   "a fast zap to GND, which returns to the\n"
                   "main board on tail pins 1 + 12.", NOTE)

S.text((15, 268), f"Board: 22 x 10 x 0.6 mm, 2 layers. This sheet = variant {VARIANT}. Variant A = MT6701 (satellite/), variant B = AS5600L (satellite_b/); same tail pinout and magnet (report 4.5).", 1.3)
S.write()
write_custom_lib(CUSTOM)
print(f"wrote {DIR}/satellite.kicad_sch (variant {VARIANT})")

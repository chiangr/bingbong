"""Sheet 4 — AMOLED: OSPTEK AM110Q126294LK1 (ICNA3306 + CHSC6417 touch), rails, PMIC, level shifting. Refs 4xx.

Panel decision and evidence: ../DISPLAY_PANEL_DECISION_2026-09-28.md. Datasheets in firmware/bingbong_pcb/_mech/
(osptek_AM110Q126294LK1, icna3306, chsc6417, tps65631, tps22916, tps7a02, sn74lvc2g34, sn74lv1t34, tca9406).
"""
from schgen import Sheet, stock, root_paths, write_custom_lib
from parts import CUSTOM

R0402 = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"
C0603 = "Capacitor_SMD:C_0603_1608Metric"
NOTE = 1.27

S = Sheet("display.kicad_sch", "Sheet 4 — AMOLED: rails, PMIC, level shifting, panel + touch",
          root_paths()["display.kicad_sch"])
R, C, L = stock("Device", "R"), stock("Device", "C"), stock("Device", "L")


def res(ref, val, x, y, rot=0, **kw):
    off = dict(ref_off=(0, -2.8), val_off=(0, 3.2)) if rot == 90 else {}
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


def caps(net, items, x0, y0, kind="local", dx=10.16):
    """Row of caps from `net` to GND. kind: local label, global label, or power rail."""
    for i, (ref, val, fp) in enumerate(items):
        c = cap(ref, val, x0 + i * dx, y0, fp=fp)
        {"local": S.net, "global": S.gnet, "rail": S.rail}[kind](c.pin(1), net, "up", 2)
        S.gnd(c.pin(2))


def series(ref, val, a_net, b_net, x, y, b_global=False):
    """Horizontal series part between two labels."""
    r = res(ref, val, x, y, rot=90)
    S.net(r.pin(1), a_net, "left", 2)
    (S.gnet if b_global else S.net)(r.pin(2), b_net, "right", 2)
    return r


# ============================================================ A. rails
S.box((15, 20), (200, 130), "A · Panel rails: 1.8 V first, then VCI, then PMIC input")
u401 = ic("TPS7A02_DQN", "U401", 50.8, 55.88, "TPS7A0218PDQNR")
S.rail(S.stub(u401.pin("4"), "left", 3), "V3", "up", 2)
S.gnet(u401.pin("3"), "DISP_SW_A_EN", "left", 4, shape="input")
S.net(u401.pin("1"), "V1V8_DISP", "right", 4)
S.gnd(u401.pin("2"))
S.gnd(u401.pin("5"))
caps("V3", (("C401", "1uF", C0402),), 25.4, 78.74, kind="rail")
caps("V1V8_DISP", (("C402", "1uF", C0402), ("C403", "100nF", C0402)), 55.88, 78.74)

u402 = ic("TPS22916", "U402", 134.62, 45.72, "TPS22916CYFPR")
S.rail(S.stub(u402.pin("A2"), "left", 3), "V3", "up", 2)
S.net(u402.pin("B2"), "V1V8_DISP", "left", 4)
S.gnet(u402.pin("A1"), "VCI_SW", "right", 4, shape="output")
S.gnd(u402.pin("B1"))
caps("VCI_SW", (("C404", "1uF", C0402), ("C405", "100nF", C0402)), 172.72, 55.88, kind="global")

u403 = ic("TPS22916", "U403", 134.62, 96.52, "TPS22916CYFPR")
S.rail(S.stub(u403.pin("A2"), "left", 3), "VSYS", "up", 2)
S.gnet(u403.pin("B2"), "VCI_SW", "left", 4, shape="input")
S.gnet(u403.pin("A1"), "PMIC_VIN_SW", "right", 4, shape="output")
S.gnd(u403.pin("B1"))
caps("VSYS", (("C406", "1uF", C0402),), 106.68, 111.76, kind="rail")
caps("PMIC_VIN_SW", (("C407", "10uF", C0603),), 172.72, 106.68, kind="global")
S.text((19, 27), "U401 EN = DISP_SW_A_EN (internal pull-down, off in MCU reset). 1.8 V (IOVCC, TP_IOVCC) comes up first,\n"
                 "then drives switch A ON (VIH 1.0 V): VCI_SW (3.1 V: VCC + CTP_VDD) follows ~3 ms later. ICNA3306 wants\n"
                 "VDDI before VCI; the chain guarantees it with one GPIO. VCI must stay on V3: IC abs max 3.6 V.", NOTE)
S.text((19, 118), "Switch B ON = VCI_SW: PMIC input exists only while the panel is powered, i.e. after firmware has run\n"
                  "(and set BQ25188 SYS_REG below 4.5 V at boot). Frees the old DISP_SW_B_EN GPIO for PMIC CTRL.", NOTE)

# ============================================================ B. PMIC
S.box((210, 20), (405, 130), "B · ELVDD / ELVSS: TPS65631DPDR (TI Figure 10 values)")
u404 = ic("TPS65631", "U404", 300.0, 66.04, "TPS65631DPDR")
S.gnet(u404.pin("12"), "PMIC_VIN_SW", "left", 4, shape="input")
S.gnet(u404.pin("11"), "PMIC_VIN_SW", "left", 4, shape="input")
S.gnet(u404.pin("7"), "DISP_PMIC_CTRL", "left", 4, shape="input")
S.net(u404.pin("8"), "PMIC_CT", "left", 4)
S.net(u404.pin("1"), "PMIC_SWP", "right", 4)
S.gnet(u404.pin("3"), "ELVDD", "right", 4, shape="output")
S.gnet(u404.pin("4"), "ELVDD", "right", 4, shape="input")
S.net(u404.pin("10"), "PMIC_SWN", "right", 4)
S.net(u404.pin("9"), "ELVSS_PMIC", "right", 4)
for p in ("2", "5", "6", "13"):
    S.gnd(u404.pin(p))
caps("PMIC_VIN_SW", (("C408", "10uF", C0603), ("C409", "10uF", C0603)), 218.44, 104.14, kind="global")
caps("PMIC_CT", (("C410", "100nF", C0402),), 243.84, 104.14)
for i, (ref, a, b) in enumerate((("L401", "PMIC_VIN_SW", "PMIC_SWP"), ("L402", "PMIC_SWN", None))):
    ll = S.place("Device:L", L, ref, "4.7uH", 350.52 + i * 15.24, 45.72, footprint="Bingbong_v3:L_Murata_DFE252010F",
                 fields={"MPN": "DFE252010F-4R7M=P2"})
    (S.gnet if a == "PMIC_VIN_SW" else S.net)(ll.pin(1), a, "up", 2)
    if b:
        S.net(ll.pin(2), b, "down", 2)
    else:
        S.gnd(ll.pin(2))
caps("ELVDD", (("C411", "10uF", C0603),), 350.52, 88.9, kind="global")
caps("ELVSS_PMIC", (("C412", "10uF", C0603), ("C413", "10uF", C0603)), 363.22, 88.9)
series("R401", "0R", "ELVSS_PMIC", "ELVSS", 381.0, 111.76, b_global=True)
S.text((214, 27), "CTRL = DISP_PMIC_CTRL (P0.23; internal 150-860k pull-down). The tail has no SWIRE, so the nRF enables\n"
                  "the PMIC and sends 21 rising edges (2-25 us each) -> VNEG -2.4 V. VNEG first ramps to -4.0 V default.\n"
                  "FBS senses ELVDD: route it from the connector pins. Caps 10 V X5R; keep L/C within 2 mm of U404.", NOTE)
S.text((214, 118), "R401 0R link: break ELVSS to measure the -4.0 V first ramp with no panel (OSPTEK must confirm the\n"
                   "panel tolerates it; no ELVSS abs max published). L401/L402 DFE252010F-4R7M: 1.0 mm max,\nIsat 1.9 A, 240 mOhm max.", NOTE)

# ============================================================ C. level shifting
S.box((15, 140), (200, 262), "C · Level shifting: nRF 3.1 V  <->  panel/touch 1.8 V")
down = (("U405", 1, "1", "6", "SPI_SCK", "P_SCK_R"), ("U405", 2, "3", "4", "SPI_MOSI", "P_SDI_R"),
        ("U406", 1, "1", "6", "DISP_CS", "P_CSX"), ("U406", 2, "3", "4", "DISP_DC", "P_DCX"),
        ("U407", 1, "1", "6", "DISP_RESX", "P_RST"))
for i, (ref, unit, pa, py, src, dst) in enumerate(down):
    u = ic("SN74LVC2G34", ref, 45.72, 162.56 + i * 15.24, "SN74LVC2G34DCKR", unit=unit)
    S.gnet(u.pin(pa), src, "left", 4, shape="input")
    S.net(u.pin(py), dst, "right", 4)
u = ic("SN74LVC2G34", "U407", 45.72, 238.76, "SN74LVC2G34DCKR", unit=2)
S.gnd(S.stub(u.pin("3"), "left", 2), "down", 1)
S.noconn(u.pin("4"))
for i, ref in enumerate(("U405", "U406", "U407")):
    u = ic("SN74LVC2G34", ref, 81.28 + i * 17.78, 208.28, "SN74LVC2G34DCKR", unit=3)
    S.net(u.pin("5"), "V1V8_DISP", "up", 2)
    S.gnd(u.pin("2"))
caps("V1V8_DISP", (("C414", "100nF", C0402), ("C415", "100nF", C0402), ("C416", "100nF", C0402)), 81.28, 238.76)
series("R402", "33R", "P_SCK_R", "P_SCK", 88.9, 162.56)
series("R403", "33R", "P_SDI_R", "P_SDI", 88.9, 177.8)

up = (("U408", "P_TE", "DISP_TE", 162.56), ("U409", "P_CTP_INT", "CTP_INT", 190.5))
for ref, src, dst, y in up:
    u = ic("SN74LV1T34", ref, 152.4, y, "SN74LV1T34DCKR")
    S.net(u.pin("2"), src, "left", 4)
    S.noconn(u.pin("1"))
    S.gnet(u.pin("4"), dst, "right", 4, shape="output")
    S.rail(u.pin("5"), "V3", "up", 2)
    S.gnd(u.pin("3"))
caps("V3", (("C417", "100nF", C0402), ("C418", "100nF", C0402)), 180.34, 172.72, kind="rail")

u410 = ic("TCA9406_YZP", "U410", 152.4, 238.76, "TCA9406YZPR")
S.net(u410.pin("C1"), "V1V8_DISP", "left", 4)
S.net(u410.pin("C2"), "P_RST", "left", 4)
S.net(u410.pin("D1"), "P_CTP_SDA", "left", 4)
S.net(u410.pin("D2"), "P_CTP_SCL", "left", 4)
S.rail(S.stub(u410.pin("B2"), "right", 3), "V3", "up", 2)
S.gnet(u410.pin("A1"), "SDA", "right", 4)
S.gnet(u410.pin("A2"), "SCL", "right", 4, shape="output")
S.gnd(u410.pin("B1"))
caps("V1V8_DISP", (("C419", "100nF", C0402),), 119.38, 246.38)
caps("V3", (("C420", "100nF", C0402),), 190.5, 246.38, kind="rail")
S.text((19, 147), "Down (U405-U407, VCC = V1V8_DISP): 5.5 V-tolerant inputs + Ioff. With the panel off the buffers are\n"
                  "unpowered and Hi-Z, so the NOR can use the shared SPIM with no back-power into the panel. SDO: not connected.", NOTE)
S.text((160, 204), "Up (U408/U409 on V3): LVxT\ninputs, VIH 1.39 V max.\n"
                   "U410: touch I2C -> main bus\n(CHSC6417 0x2E). OE = P_RST:\nisolated during touch reset,\nHi-Z when unpowered.\n10k pull-ups inside.", NOTE)

# ============================================================ D. panel connector
S.box((210, 140), (405, 262), "D · Panel: AM110Q126294LK1 24-pin BTB (spec §8 pin table)")
j = S.place("Connector_Generic:Conn_02x12_Odd_Even", stock("Connector_Generic", "Conn_02x12_Odd_Even"), "J401",
            "AMOLED 24P BTB", 309.88, 200.66, footprint="Bingbong_v3:BTB_2x12_OSPTEK_TBD",
            fields={"MPN": "receptacle mating OSPTEK WB2564024M, 2x12 [U]"}, ref_off=(-3, -17), val_off=(-3, 17.5))
PINS = {1: ("VCI_SW", "g"), 2: ("P_CTP_INT", "l"), 3: ("VCI_SW", "g"), 4: ("P_CTP_SCL", "l"),
        5: ("V1V8_DISP", "l"), 6: ("P_CTP_SDA", "l"), 7: ("V1V8_DISP", "l"), 8: ("P_RST", "l"),
        9: ("GND", "gnd"), 10: ("GND", "gnd"), 11: ("GND", "gnd"), 12: ("P_TE", "l"), 13: ("GND", "gnd"),
        14: ("P_RST", "l"), 15: ("GND", "gnd"), 16: (None, "nc"), 17: ("ELVDD", "g"), 18: ("P_SDI", "l"),
        19: ("ELVDD", "g"), 20: ("P_DCX", "l"), 21: ("ELVSS", "g"), 22: ("P_SCK", "l"), 23: ("ELVSS", "g"),
        24: ("P_CSX", "l")}
for n, (net, kind) in PINS.items():
    d = "left" if n % 2 else "right"
    if kind == "nc":
        S.noconn(j.pin(n))
    elif kind == "gnd":
        S.gnd(S.stub(j.pin(n), d, 3), d, 1)
    elif kind == "g":
        S.gnet(j.pin(n), net, d, 4)
    else:
        S.net(j.pin(n), net, d, 4)
pd = (("R404", "10k", "P_RST"), ("R405", "100k", "P_TE"))
for i, (ref, val, net) in enumerate(pd):
    r = res(ref, val, 229.87 + i * 12.7, 228.6)
    S.net(r.pin(1), net, "up", 2)
    S.gnd(r.pin(2))
r406 = res("R406", "10k", 377.19, 228.6)
S.net(r406.pin(1), "V1V8_DISP", "up", 2)
S.net(r406.pin(2), "P_CTP_INT", "down", 2)
S.text((214, 147), "Pin names (panel): 1 VCC 3.3V, 2 CTP_INT, 3 CTP_VDD, 4 CTP_SCL, 5 IOVCC 1.8V, 6 CTP_SDA, 7 TP_IOVCC,\n"
                   "8 CTP_RST, 9-11/15 GND, 12 TE, 13 MTP (open/GND), 14 RST, 16 SDO (NC), 17/19 ELVDD, 18 SDI, 20 DCX,\n"
                   "21/23 ELVSS, 22 SCL, 24 CSX. Numbering from the spec drawing; recheck against the mating part.", NOTE)
S.text((214, 240), "R404: RESX + CTP_RST low whenever the buffer is off (both chips: reset low before power).\n"
                   "R405: TE defined when the panel is off.  R406: CTP_INT pull-up to the switched 1.8 V\n"
                   "(works for open-drain or push-pull; reads low when the panel is off).", NOTE)

S.text((15, 268), "Interfaces   in: SPI_SCK, SPI_MOSI, DISP_CS, DISP_DC, DISP_RESX, DISP_SW_A_EN, DISP_PMIC_CTRL, SDA/SCL   "
                  "out: DISP_TE, CTP_INT, VCI_SW, PMIC_VIN_SW, ELVDD, ELVSS   rails: V3, VSYS   Refs 4xx   [U] = MPN not final", 1.4)
S.text((15, 276), "Power-on: SW_A_EN high -> RESX low 10 ms after rails -> high -> 150 ms -> init + SLPOUT -> PMIC_CTRL high, 21 pulses\n"
                  "-> ELVSS settled -> DISPON.   Power-off: DISPOFF, SLPIN -> PMIC_CTRL low (active discharge) -> RESX low -> SW_A_EN low.\n"
                  "ELVDD/ELVSS order vs. SLPOUT is conventional [U]: OSPTEK spec 13.1.8 wording contradicts it - confirm with the vendor.", NOTE)
S.write()
write_custom_lib(CUSTOM)
print("wrote display.kicad_sch")

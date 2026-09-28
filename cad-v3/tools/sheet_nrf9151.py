"""Sheet 2 — nRF9151 SiP, eSIM, open-drain pull-ups. Reference designators 2xx.

Pin numbers: Nordic nRF9151 PS v1.0 pin table, cross-checked with the makerdiary
nRF9151 Connect Kit schematic (firmware/bingbong_pcb/_mech/nrf9151_connectkit_sch.pdf).
"""
from schgen import Sheet, stock, root_paths, write_custom_lib
from parts import CUSTOM

R0402 = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"
C0603 = "Capacitor_SMD:C_0603_1608Metric"
NOTE = 1.27

S = Sheet("nrf9151.kicad_sch", "Sheet 2 — nRF9151 SiP, eSIM, pull-ups", root_paths()["nrf9151.kicad_sch"])
R, C = stock("Device", "R"), stock("Device", "C")
NRF = CUSTOM["NRF9151"]


def res(ref, val, x, y, rot=0, **kw):
    off = dict(ref_off=(-2.5, -2.8), val_off=(-2.5, 3.2)) if rot == 90 else {}
    return S.place("Device:R", R, ref, val, x, y, rot=rot, footprint=kw.pop("fp", R0402), **off, **kw)


def cap(ref, val, x, y, fp=C0402, **kw):
    return S.place("Device:C", C, ref, val, x, y, footprint=fp, **kw)


def nrf_unit(unit, x, y, title):
    s = S.place("Bingbong_v3:NRF9151", NRF, "U201", "nRF9151-LACA-R", x, y, unit=unit,
                fields={"MPN": "NRF9151-LACA-R"}, ref_off=(0, 0), val_off=(0, 0))
    S.items.pop()
    return S.place("Bingbong_v3:NRF9151", NRF, "U201", title, x, y, unit=unit,
                   fields={"MPN": "NRF9151-LACA-R"}, ref_off=(-s.half_w, -s.half_h - 4.2),
                   val_off=(-s.half_w, -s.half_h - 1.6))


# ============================================================ A. power + RF
S.box((15, 20), (135, 125), "A · nRF9151 supply and antenna pins")
ua = nrf_unit(1, 88.9, 55.88, "nRF9151 — power / RF")
en = S.stub(ua.pin("10"), "left", 2)
r201 = S.place("Device:R", R, "R201", "10k", en[0] - 3.81 - 1.27, en[1], rot=90, footprint=R0402,
               ref_off=(0, -2.8), val_off=(0, 3.2))
S.wire(en, r201.pin(2))
S.rail(r201.pin(1), "VSYS", "up", 2)
S.net(ua.pin("14"), "VDD_NRF", "left", 4)
S.rail(S.stub(ua.pin("65"), "left", 3), "V3", "up", 2)
dec = S.stub(ua.pin("24"), "left", 3)
c205 = cap("C205", "4.7uF", dec[0], dec[1] + 5.08)
S.wire(dec, c205.pin(1))
S.gnd(c205.pin(2))
S.gnet(ua.pin("35"), "ANT_RF", "right", 4, shape="passive")
S.noconn(ua.pin("37"))
S.noconn(ua.pin("42"))
# supply group below the unit
yb = 95.25
S.rail((25.4, yb), "VSYS", "up", 0)
fb = S.place("Device:R", R, "FB201", "0R link", 33.02, yb, rot=90, footprint="Resistor_SMD:R_0603_1608Metric",
             fields={"MPN": "0 ohm 0603 (remove for PPK2 current measurement)"}, ref_off=(-2.5, -2.8), val_off=(-3, 3.2))
S.wire((25.4, yb), fb.pin(1))
vn = (43.18, yb)
S.wire(fb.pin(2), vn)
S.label((43.18, yb), "VDD_NRF", "up")
for i, (ref, val, fp) in enumerate((("C201", "10uF", C0603), ("C202", "1uF", C0402))):
    cx = 48.26 + i * 10.16
    c = cap(ref, val, cx, yb + 5.08, fp=fp)
    S.wire(vn if i == 0 else (cx - 10.16, yb), (cx, yb))
    S.wire((cx, yb), c.pin(1))
    S.junction((cx, yb)) if i == 0 else None
    S.gnd(c.pin(2))
S.junction(vn)
S.flag((70.61, yb), "up", 2)
S.wire((58.42, yb), (70.61, yb))
for i, (ref, val) in enumerate((("C203", "100nF"), ("C204", "4.7uF"))):
    c = cap(ref, val, 83.82 + i * 12.7, yb + 5.08)
    S.rail(c.pin(1), "V3", "up", 2)
    S.gnd(c.pin(2))
S.text((19, 27), "VDD (pin 14) runs straight from VSYS (3.0-5.5 V). VDD_GPIO (pin 65) = V3 sets the logic level\n"
                 "of every GPIO. ENABLE (pin 10) high = SiP regulator on; pulled up to VSYS as in the reference kit.", NOTE)
S.text((19, 110), "FB201: 0 R link - lift it and insert a PPK2 to measure the nRF alone (sleep-current work).\n"
                  "C201/C202 at pin 14, C203/C204 at pin 65, C205 at DEC0 - values from the Nordic-based reference kit.\n"
                  "AUX (37) and GPS (42) unused: GNSS not fitted (report 4.1).", NOTE)

# ============================================================ B. interfaces
S.box((15, 135), (135, 262), "B · Debug, SIM and coexistence pins")
uc = nrf_unit(3, 78.74, 190.5, "nRF9151 — interfaces")
S.gnet(uc.pin("4"), "SWDIO_NRF", "left", 4)
S.gnet(uc.pin("3"), "SWDCLK_NRF", "left", 4, shape="input")
S.gnet(uc.pin("9"), "NRESET", "left", 4)
for pin, net in (("16", "SIM_RST"), ("18", "SIM_CLK"), ("17", "SIM_IO"), ("19", "SIM_1V8")):
    S.net(uc.pin(pin), net, "left", 4)
S.noconn(uc.pin("26"))
S.gnet(uc.pin("52"), "COEX0", "right", 4)
for pin in ("53", "54", "21", "22", "23", "27", "28", "29"):
    S.noconn(uc.pin(pin))
S.text((19, 142), "SWD is the only way in: it goes to the dock pads through the limiter cells (dock sheet).\n"
                  "~RESET: no external pull-up allowed (Nordic); brought to a test pad only.\n"
                  "COEX0 goes high whenever the modem's RF is active; it is looped back to P0.29 so\n"
                  "firmware can blank the grip sensor during transmit (AT%XCOEX0, report E-3).", NOTE)
S.text((19, 236), "SIM_DET must float (Nordic). MAGPIO0-2, COEX1-2 and the MIPI RFFE pins are only for\n"
                  "external antenna tuners - none fitted, so all unconnected.", NOTE)

# ============================================================ C. GPIO map
S.box((145, 20), (295, 150), "C · GPIO map (32 of 32 used, 0 spare)")
ub = nrf_unit(2, 220.98, 85.09, "nRF9151 — GPIO")
GPIO = {
    0: ("SPI_SCK", "output"), 1: ("SPI_MOSI", "output"), 2: ("SPI_MISO", "input"), 3: ("DISP_CS", "output"),
    4: ("DISP_DC", "output"), 5: ("NOR_CS", "output"), 6: ("DISP_TE", "input"), 7: ("DISP_RESX", "output"),
    8: ("SDA", "bidirectional"), 9: ("SCL", "output"), 10: ("BQ_INT", "input"), 11: ("GAUGE_ALRT", "input"),
    12: ("IQS_SCL", "output"), 13: ("HA1", "input"), 14: ("HA2", "input"), 15: ("HB1", "input"),
    16: ("HB2", "input"), 17: ("TACT_NRF", "input"), 18: ("IQS_SDA", "bidirectional"), 19: ("SENS_SCL", "output"), 20: ("CTP_INT", "input"),
    21: ("HAPTIC_TRIG", "output"), 22: ("DISP_SW_A_EN", "output"), 23: ("DISP_PMIC_CTRL", "output"),
    24: ("SENSOR_SW_EN", "output"), 25: ("HAPTIC_NRST", "output"), 26: ("LED_R", "output"), 27: ("LED_G", "output"),
    28: ("LED_B", "output"), 29: ("COEX0", "local"), 30: ("DOCK_ID", "input"), 31: ("SENS_SDA", "bidirectional"),
}
from parts import _GPIO_PINS
for n, v in GPIO.items():
    pin = str(_GPIO_PINS[n])
    side = "left" if n < 16 else "right"
    if v is None:
        S.noconn(ub.pin(pin))
    elif v[1] == "local":
        e = S.gnet(ub.pin(pin), v[0], side, 10)
    else:
        S.gnet(ub.pin(pin), v[0], side, 4, shape=v[1])
# COEX0 needs a defined level before the modem configures it
cx = S.stub(ub.pin(str(_GPIO_PINS[29])), "right", 0)
r206 = res("R206", "1M", 264.16, 130.81)
S.glabel((264.16, r206.pin(1)[1] - 2.54), "COEX0", "up")
S.wire((264.16, r206.pin(1)[1] - 2.54), r206.pin(1))
S.gnd(r206.pin(2))
S.text((149, 136), "SPI + NOR + display on P0.00-P0.07 (far from the ANT pin). LED gates, DOCK_ID, COEX0 near the RF\n"
                   "side are slow signals. No spare: P0.20 = touch INT (a polled touch driver would free it). Three I2C buses: main (P0.08/09),\n"
                   "grip IQS211B (P0.12/18, RDY rides on its SCL), crown angle sensor (P0.31/19, power-gated).\n"
                   "R206 holds COEX0 low until the modem drives it.", NOTE)

# ============================================================ D. eSIM
S.box((305, 20), (405, 105), "D · eSIM (MFF2 eUICC)")
u2 = S.place("Bingbong_v3:MFF2_eUICC", CUSTOM["MFF2_eUICC"], "U202", "MFF2 eUICC", 360.68, 60.96,
             fields={"MPN": "MFF2 eUICC, class C 1.8 V, SGP.32, supply-shutdown confirmed [U]"},
             ref_off=(-7.62, -10), val_off=(-7.62, -7.4))
S.net(u2.pin("8"), "SIM_1V8", "left", 8)
c206 = cap("C206", "100nF", 391.16, 60.96)
S.net(c206.pin(1), "SIM_1V8", "up", 2)
S.gnd(c206.pin(2))
for pin, net in (("7", "SIM_RST"), ("6", "SIM_CLK"), ("3", "SIM_IO")):
    S.net(u2.pin(pin), net, "left", 8)
for pin in ("2", "4", "5"):
    S.noconn(u2.pin(pin))
S.gnd(u2.pin("1"))
S.text((309, 82), "Soldered eSIM, wired directly as in the reference kit: no ESD or\n"
                  "series parts (it never leaves the sealed body). C206 within 2 mm.\n"
                  "Place within 10 mm of the SiP SIM pins. SIM supply is 1.8 V\n"
                  "(SIM_1V8 from the nRF) -> the eUICC must be class C.", NOTE)

# ============================================================ E. pull-ups
S.box((305, 115), (405, 190), "E · Open-drain pull-ups (to V3)")
for i, (ref, val, net) in enumerate((("R202", "4.7k", "SDA"), ("R203", "4.7k", "SCL"),
                                     ("R204", "10k", "BQ_INT"), ("R205", "10k", "GAUGE_ALRT"))):
    x = 320.04 + i * 20.32
    r = res(ref, val, x, 144.78)
    S.rail(r.pin(1), "V3", "up", 2)
    S.gnet(r.pin(2), net, "down", 3)
S.text((309, 170), "Main I2C bus (BQ25188, MAX17048, DRV2625):\n"
                   "4.7 k for 400 kHz. BQ_INT (128 us pulses) and\n"
                   "GAUGE_ALRT are open-drain alerts: 10 k is enough.", NOTE)

# ============================================================ F. ground + reserved
S.box((145, 160), (295, 262), "F · Ground and reserved pins")
ue = nrf_unit(5, 180.34, 212.09, "nRF9151 — GND")
for side, pins in (("left", CUSTOM and [str(n) for n in [1, 7, 13, 15, 20, 25, 30, 34, 36, 38, 39, 40, 41, 43, 46]]),
                   ("right", [str(n) for n in [51, 55, 60, 66, 71, 76, 105, 106, 107, 108, 109, 110, 111, 112, 113]])):
    ends = [S.stub(ue.pin(p), side, 2) for p in pins]
    S.wire(*ends)
    for e in ends[1:-1]:
        S.junction(e)
    S.junction(ends[-1])
    S.gnd(ends[-1], "down", 2)
ud = nrf_unit(4, 251.46, 212.09, "nRF9151 — reserved")
from parts import _RSV
for n in _RSV:
    S.noconn(ud.pin(str(n)))
S.text((149, 250), "30 GND pads: all to the solid L2/L5 planes with vias (report E-11).\n"
                   "Reserved pads: solder them (mechanical/thermal) but never connect.", NOTE)

# ============================================================ G. notes
S.box((305, 200), (405, 262), "G · Firmware pin table (devicetree)")
S.text((309, 208), "spi: SCK P0.00  MOSI P0.01  MISO P0.02\n"
                   "  cs: DISP P0.03  NOR P0.05   DISP D/C P0.04\n"
                   "disp: TE P0.06  RESX P0.07  SW_A P0.22  PMIC_CTRL P0.23  CTP_INT P0.20\n"
                   "i2c: SDA P0.08  SCL P0.09\n"
                   "i2c_iqs: SCL/RDY P0.12  SDA P0.18   i2c_sens: SCL P0.19  SDA P0.31\n"
                   "irq: BQ P0.10  GAUGE P0.11  COEX0 P0.29\n"
                   "crown: HA1 P0.13  HA2 P0.14  HB1 P0.15  HB2 P0.16\n"
                   "       TACT P0.17  SENSOR_EN P0.24\n"
                   "haptic TRIG P0.21  NRST P0.25   halo R/G/B P0.26/27/28 (PWM0)\n"
                   "DOCK_ID P0.30", NOTE)

S.text((15, 268), "Interfaces   rails in: VSYS, V3   out: SIM_1V8 (local)   RF: ANT_RF -> rf sheet   debug: SWDIO_NRF, SWDCLK_NRF -> dock sheet, NRESET -> test points\n"
                  "Refs 2xx   [U] = part class chosen, MPN not final", 1.4)
S.write()
write_custom_lib(CUSTOM)
print("wrote nrf9151.kicad_sch")

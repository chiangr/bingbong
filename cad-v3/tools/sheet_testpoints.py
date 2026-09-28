"""Sheet 7 — bed-of-nails test points (report E-16, EM-6a/6b, EV-3). Refs 7xx.

Every pad is a ø0.9 mm ENIG pad on the BOTTOM side, X = 19-62 (under the cell), >= 1.27 mm apart.
Each test point simply sits on an existing net; nothing on this sheet changes the circuit.
"""
from schgen import Sheet, stock, root_paths, write_custom_lib
from parts import CUSTOM

NOTE = 1.27
FP = "Bingbong_v3:TestPoint_Pad_D0.9mm_ENIG"
S = Sheet("testpoints.kicad_sch", "Sheet 7 — Test points (bed-of-nails, bottom side)", root_paths()["testpoints.kicad_sch"])
TPB = stock("Connector", "TestPoint")
RAILS = {"VBAT", "VSYS", "V3"}

GROUPS = [
    ("A · Power: the PPK2 current point + rails", 15, [
        ("VBAT", "PPK2 point: cell-side sleep current"),
        ("VSYS", "system rail 3.45-4.43 V"),
        ("V3", "3.1 V logic rail"),
        ("GND", ""), ("GND", ""), ("GND", ""), ("GND", ""),
    ]),
    ("B · Display power + control", 115, [
        ("VCI_SW", "switch A out (panel logic)"), ("PMIC_VIN_SW", "switch B out (PMIC input)"),
        ("ELVDD", "+4.6 V panel"), ("ELVSS", "-2.2/-2.4 V panel"),
        ("DISP_TE", "tearing effect = mate check"), ("DISP_RESX", ""), ("DISP_CS", ""), ("SPI_SCK", ""),
    ]),
    ("C · Debug + buses", 215, [
        ("SWDIO_NRF", "nRF side of the limiter"), ("SWDCLK_NRF", "buffer output"), ("NRESET", ""),
        ("DOCK_ID", ""), ("SDA", ""), ("SCL", ""), ("IQS_SCL", ""), ("IQS_SDA", ""),
        ("SENS_SCL", ""), ("SENS_SDA", ""), ("COEX0", "modem RF-active flag"),
    ]),
    ("D · Crown, haptics, halo, alerts", 315, [
        ("HA1", ""), ("HA2", ""), ("HB1", ""), ("HB2", ""), ("TACT_NRF", ""), ("TS_MR", "NTC + button node"),
        ("LRA_P", ""), ("LRA_N", ""), ("LED_R", ""), ("LED_G", ""), ("LED_B", ""),
        ("BQ_INT", ""), ("GAUGE_ALRT", ""),
    ]),
]

n = 701
for title, x0, pads in GROUPS:
    S.box((x0, 20), (x0 + 90, 205), title)
    for i, (net, why) in enumerate(pads):
        y = 38.1 + i * 12.7
        tx = x0 + 38.1
        tp = S.place("Connector:TestPoint", TPB, f"TP{n}", net, tx, y, rot=270, footprint=FP,
                     fields={"Fixture": "pogo, 1.27 mm min pitch"}, ref_off=(7, -1.3), val_off=(7, 1.3))
        n += 1
        if net == "GND":
            e = S.stub(tp.pin(1), "left", 4)
            S.gnd(e, "down", 1)
        elif net in RAILS:
            e = S.stub(tp.pin(1), "left", 6)
            S.rail(e, net, "up", 1)
        else:
            S.gnet(tp.pin(1), net, "left", 4, shape="passive")
        if why:
            S.text((tx + 17, y - 0.6), why, 1.0)

S.box((15, 215), (405, 262), "E · Fixture rules (report E-16, EM-6a/6b, EV-3)")
S.text((19, 223), "Where: bottom side, X = 19-62 mm (under the cell, later covered by the PET insulator); nothing below X = 62-68. Pads: ø0.9 mm ENIG, >= 1.27 mm apart.\n"
                  "Why a bed of nails: the sealed product has no connector except the 4 dock pads, so every internal net that a factory or lab test must see gets\n"
                  "a pad here BEFORE the rear shell closes. The dock nets themselves (VBUS, SWDIO, SWCLK, DOCK_ID) are probed on the J601 footprint pads.\n"
                  "Order of use: EM-6a unpowered opens/shorts -> EM-7a program over SWD -> EM-6b powered: rails, I2C roll-call, LED/LRA, and the cell-side sleep current\n"
                  "measured at the VBAT pad with a PPK2 in source-meter mode (<= 40 uA with the satellite mated, panel absent). Top side only: TP301 RF DC test (rf sheet).", NOTE)
S.text((15, 268), "39 pads. Global labels on this sheet only attach test pads to nets defined on the other sheets (the display rails get their drivers on the display sheet). Refs 7xx.", 1.4)
S.write()
write_custom_lib(CUSTOM)
print("wrote testpoints.kicad_sch")

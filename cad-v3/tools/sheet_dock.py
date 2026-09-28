"""Sheet 6 — dock pads, ESD, SWD protection, DOCK_ID. Reference designators 3xx (dock = 6xx).

Threat model (report E-13): a key lying across the pads while docked can put 5 V (VBUS) on any
pad. Nothing on the nRF side may ever exceed V3 + 0.3 V, nothing may push current into V3 (the
buck cannot sink it), and it must all work with no firmware and a 0 V cell.
"""
from schgen import Sheet, stock, root_paths, write_custom_lib
from parts import CUSTOM

R0402 = "Resistor_SMD:R_0402_1005Metric"
C0402 = "Capacitor_SMD:C_0402_1005Metric"
NOTE = 1.27

S = Sheet("dock.kicad_sch", "Sheet 6 — Dock pads, ESD, SWD protection", root_paths()["dock.kicad_sch"])
R, C = stock("Device", "R"), stock("Device", "C")


def res(ref, val, x, y, rot=0, **kw):
    off = dict(ref_off=(0, -2.8), val_off=(0, 3.2)) if rot == 90 else {}
    return S.place("Device:R", R, ref, val, x, y, rot=rot, footprint=kw.pop("fp", R0402), **off, **kw)


def ic(name, ref, x, y, mpn, unit=1):
    t = S.place(f"Bingbong_v3:{name}", CUSTOM[name], ref, mpn, x, y, ref_off=(0, 0), val_off=(0, 0), unit=unit)
    S.items.pop()
    top = any(v[2] == 270 for v in t.lib_pins.values())
    ro = (3.0, -t.half_h - 5.5) if top else (-t.half_w, -t.half_h - 4.2)
    vo = (3.0, -t.half_h - 3.0) if top else (-t.half_w, -t.half_h - 1.6)
    return S.place(f"Bingbong_v3:{name}", CUSTOM[name], ref, mpn, x, y, fields={"MPN": mpn},
                   ref_off=ro, val_off=vo, unit=unit)


# ============================================================ A. connector + ESD
S.box((15, 20), (190, 150), "A · Dock pads (lid flex) and ESD")
j = S.place("Connector_Generic:Conn_01x05", stock("Connector_Generic", "Conn_01x05"), "J601", "DOCK FLEX 5P",
            38.1, 66.04, mirror=True, footprint="Bingbong_v3:B2B_0.4mm_5P_TBD",
            fields={"MPN": "0.4 mm B2B 5-way to lid flex [U]"}, ref_off=(-3, -9), val_off=(-3, 9.5))
S.gnd(S.stub(j.pin(1), "right", 3), "right", 1)
S.net(j.pin(2), "SWCLK_PAD", "right", 8)
S.net(j.pin(3), "SWDIO_PAD", "right", 8)
vb = S.stub(j.pin(4), "right", 20)
S.glabel(vb, "VBUS_PAD", "right", shape="output")
S.net(j.pin(5), "DOCK_ID_PAD", "right", 8)
ZD = stock("Device", "D_Zener")
for i, (ref, net) in enumerate((("D601", "SWCLK_PAD"), ("D602", "SWDIO_PAD"), ("D603", "DOCK_ID_PAD"))):
    x = 114.3 + i * 20.32
    d = S.place("Device:D_Zener", ZD, ref, "TPD1E05U06", x, 68.58, rot=270,
                footprint="Bingbong_v3:TI_DYA0002A_SOD-523", fields={"MPN": "TPD1E05U06DYAR"},
                ref_off=(9, -1.3), val_off=(15.5, 1.3))
    S.net(d.pin(1), net, "up", 2)          # pin 1 = K = I/O (TI DYA pin table)
    S.gnd(d.pin(2))                         # pin 2 = A = GND
S.text((19, 27), "4 hard-gold pads on the rear lid flex, 2.54 mm pitch: GND · SWCLK · SWDIO · VBUS (report A.2).\n"
                 "The 5th flex conductor, DOCK_ID, reaches only the factory/EOL jig.", NOTE)
S.text((19, 100), "J601 pin order = flex order. VBUS_PAD goes to the power sheet (ferrite, TVS, reverse FET).\n"
                  "D601-D603 = one TPD1E05U06 per signal pad, each placed right at its pad on J601.\n"
                  "Unidirectional TVS: cathode (pin 1) to the pad, anode (pin 2) to GND. 5.5 V working,\n"
                  "so a 5 V key-bridge never makes it conduct; 0.5 pF so SWD edges stay clean.", NOTE)

# ============================================================ B. SWCLK + DOCK_ID buffer
S.box((200, 20), (405, 120), "B · SWCLK and DOCK_ID: 5 V-tolerant buffer (one-way signals)")
for unit, (pin_a, pin_y, pad, rref, pdref, out, yy) in enumerate((
        ("1", "6", "SWCLK_PAD", "R601", "R604", "SWDCLK_NRF", 58.42),
        ("3", "4", "DOCK_ID_PAD", "R603", "R605", "DOCK_ID", 83.82)), 1):
    u = ic("SN74LVC2G34", "U602", 312.42, yy, "SN74LVC2G34DCKR", unit=unit)
    a = S.stub(u.pin(pin_a), "left", 6)
    rs = res(rref, "220R", a[0] - 12.7, a[1], rot=90)
    S.wire(a, rs.pin(2))
    S.junction(a)
    rp = res(pdref, "1M", a[0], a[1] + 6.35)
    S.wire(a, rp.pin(1))
    S.gnd(rp.pin(2))
    S.net(rs.pin(1), pad, "left", 3)
    S.gnet(u.pin(pin_y), out, "right", 6, shape="output")
up = ic("SN74LVC2G34", "U602", 360.68, 71.12, "SN74LVC2G34DCKR", unit=3)
S.rail(up.pin("5"), "V3", "up", 2)
S.gnd(up.pin("2"))
c301 = S.place("Device:C", C, "C601", "100nF", 391.16, 71.12, footprint=C0402)
S.rail(c301.pin(1), "V3", "up", 2)
S.gnd(c301.pin(2))
S.text((204, 27), "SWCLK only flows dock -> nRF, and DOCK_ID only jig -> nRF, so a buffer can do the protection:\n"
                  "its inputs accept 5.5 V even when powered from 3.1 V, and its output can only swing 0-V3.\n"
                  "Ioff: with V3 off (ship mode) a driven input cannot back-power the rail.", NOTE)
S.text((204, 96), "220R: limits ESD residue and bridge current into the buffer input.\n"
                  "1M pull-downs: a floating CMOS input draws current and toggles randomly. SWDCLK idles low\n"
                  "(matches the nRF's internal pull-down). DOCK_ID reads low unless the jig drives it.", NOTE)

# ============================================================ C. SWDIO limiter
S.box((200, 130), (405, 230), "C · SWDIO: bidirectional limiter cell")
y = 180.34
S.label((233.68, y), "SWDIO_PAD", "left")
r302 = res("R602", "220R", 241.3, y, rot=90)
S.wire((233.68, y), r302.pin(1))
q = S.place("Transistor_FET:Q_NMOS_GSD", stock("Transistor_FET", "Q_NMOS_GSD"), "Q601", "N-FET", 274.32, y - 2.54,
            rot=270, mirror=True, footprint="Package_TO_SOT_SMD:SOT-523",
            fields={"MPN": "DMG1012T class: Vth <= 1 V, Ciss low [U]"}, ref_off=(-3, 7), val_off=(-3, 9.5))
S.wire(r302.pin(2), q.pin(3))
S.rail(q.pin(1), "V3", "up", 2)
nn = (297.18, y)
S.wire(q.pin(2), nn)
S.junction(nn)
r306 = res("R606", "4.7k", nn[0], nn[1] - 6.35)
S.wire(nn, r306.pin(2))
S.rail(r306.pin(1), "V3", "up", 2)
S.wire(nn, (312.42, y))
S.glabel((312.42, y), "SWDIO_NRF", "right")
S.text((204, 137), "SWDIO goes both ways, so it gets the classic MOSFET level-shifter: gate at V3, drain toward the pad.\n"
                   "Either side pulling low turns the FET on and pulls the other side low. Pad at 5 V (key bridge): the\n"
                   "source can only rise to V3 - Vth, the FET turns off and R606 holds the nRF pin at V3. It never\n"
                   "exceeds V3, injects nothing into V3, and needs no firmware.", NOTE)
S.text((204, 200), "When the nRF drives SWDIO high, the FET is off: the DOCK must pull its side up to VTref\n"
                   "(dock-board requirement, ~10 k). R606 4.7 k gives ~120 ns edges -> SWD at 2 MHz is\n"
                   "comfortable, 4 MHz marginal (EV-9). Use 2.2 k if 4 MHz is needed.", NOTE)

# ============================================================ D. requirements on the dock board
S.box((15, 160), (190, 262), "D · What the dock board must provide (report A.2 + this sheet)")
S.text((19, 170), "1. 5 V to the VBUS pogo, current-limited: a key across the live pins must be harmless.\n"
                  "2. 3.3 V LDO for VTref on the 10-pin Cortex debug header (the 4-wire head has no VTref).\n"
                  "3. ~10 k pull-up from the SWDIO pogo to VTref (the limiter cell cannot drive the pad high).\n"
                  "4. Mechanical keying of the cradle: a reversed head puts -5 V on the signal pads while a\n"
                  "   programmer is attached (report F8) - survivable through 220R, but not harmless.\n"
                  "5. Magnets in the head, 0.3 mm 430 shim in the device wall (no magnet in the device).\n\n"
                  "Bench jig for EVM-1 (report A.2): Adafruit 5412-class 4-pin magnetic cable rewired to a\n"
                  "Cortex header, VTref from a bench 3.3 V, keyed printed cradle.", NOTE)

S.text((15, 268), "Interfaces   out: VBUS_PAD (-> power), SWDCLK_NRF, SWDIO_NRF, DOCK_ID (-> nrf9151)   rails in: V3   Refs 6xx   [U] = part class chosen, MPN not final", 1.4)
S.write()
write_custom_lib(CUSTOM)
print("wrote dock.kicad_sch")

"""Sheet 3 — RF front end: nRF9151 ANT -> DC block -> test switch -> matching network -> ESD + DC return -> feed finger
-> machined 6061 end cap (the antenna). Refs 3xx. Report sections 5.6 Steps 6-12 (topology A), E-3, E-11.
All matching values are STARTING POINTS [U]: they are fixed on Mule B / EVM-1 measurements.
"""
from schgen import Sheet, stock, root_paths, write_custom_lib
from parts import CUSTOM

C0402 = "Capacitor_SMD:C_0402_1005Metric"
L0402 = "Inductor_SMD:L_0402_1005Metric"
R0402 = "Resistor_SMD:R_0402_1005Metric"
NOTE = 1.27

S = Sheet("rf.kicad_sch", "Sheet 3 — RF: antenna match and end-cap feed", root_paths()["rf.kicad_sch"])
R, C, L = stock("Device", "R"), stock("Device", "C"), stock("Device", "L")
HO = dict(ref_off=(0, -3.0), val_off=(0, 3.4))          # labels for horizontal (series) parts


def series(kind, ref, val, x, y, dnp=False, mpn=""):
    lib, blk, fp = {"C": ("Device:C", C, C0402), "L": ("Device:L", L, L0402), "R": ("Device:R", R, R0402)}[kind]
    return S.place(lib, blk, ref, val, x, y, rot=90, footprint=fp, dnp=dnp, fields={"MPN": mpn} if mpn else None, **HO)


def shunt(kind, ref, val, node, dnp=False, mpn="", gnd=True, dy=6.35):
    lib, blk, fp = {"C": ("Device:C", C, C0402), "L": ("Device:L", L, L0402)}[kind]
    p = S.place(lib, blk, ref, val, node[0], node[1] + dy, footprint=fp, dnp=dnp,
                fields={"MPN": mpn} if mpn else None)
    S.wire(node, p.pin(1))
    if gnd:
        S.gnd(p.pin(2))
    return p


y = 88.9
S.box((15, 20), (405, 135), "A · The antenna path (top layer, 50-ohm coplanar waveguide over the L2 ground)")
S.text((19, 27), "The nRF9151 has ONE 50-ohm antenna pin. The antenna is the machined aluminium END CAP: a spring finger touches a gold\n"
                 "land on the cap's feed tab, and the cap + the whole 95 mm body resonate like a small dipole. At 700 MHz (LTE Band 12)\n"
                 "the structure is only ~0.22 wavelengths long, so its impedance is far from 50 ohms: the matching network transforms it.", NOTE)
p0 = (27.94, y)
S.glabel(p0, "ANT_RF", "left", shape="passive")
c301 = series("C", "C301", "100pF C0G", 40.64, y, mpn="GJM1555C1H101 class")
S.wire(p0, c301.pin(1))
n0 = (53.34, y)
S.wire(c301.pin(2), n0)
S.label(n0, "RF_SIP", "up")
j = S.place("Connector:CoaxialSwitch_Testpoint", stock("Connector", "CoaxialSwitch_Testpoint"), "J301", "MM8130-2600",
            66.04, y + 1.27, footprint="Bingbong_v3:Murata_MM8130-2600",
            fields={"MPN": "Murata MM8130-2600RB2"}, ref_off=(-3, -5), val_off=(-3, 6.5))
S.wire(n0, j.pin("C"))
S.gnd(S.stub(j.pin("G"), "right", 1), "down", 1)
r301 = series("R", "R301", "0R", 83.82, y, mpn="series spare: 0R now, L or C when tuning")
S.wire(j.pin("A"), r301.pin(1))
# N1: ANT-side trim
n1 = (93.98, y)
S.wire(r301.pin(2), n1, (101.6, y))
S.junction(n1)
shunt("C", "C305", "DNP", n1, dnp=True, mpn="shunt trim C3 (high band)")
shunt("L", "L303", "DNP", (101.6, y), dnp=True, mpn="shunt trim L3 (alt.)")
S.junction((101.6, y))
c304 = series("C", "C304", "3.3pF", 116.84, y, mpn="GJM1555C1H3R3WB01 class")
S.wire((101.6, y), c304.pin(1))
n2 = (129.54, y)
S.wire(c304.pin(2), n2)
shunt("C", "C303", "1.5pF", n2, mpn="GJM1555C1H1R5WB01 class")
# series L1 || C_byp
pa, pb = (139.7, y), (160.02, y)
S.wire(n2, pa)
S.junction(n2)
l302 = series("L", "L302", "15nH", 149.86, y, mpn="LQW15AN15NG class")
S.wire(pa, l302.pin(1))
S.wire(l302.pin(2), pb)
c302 = S.place("Device:C", C, "C302", "1.0pF", 149.86, y - 10.16, rot=90, footprint=C0402,
               fields={"MPN": "GJM1555C1H1R0WB01 class"}, **HO)
S.wire(pa, (pa[0], y - 10.16), c302.pin(1))
S.wire(c302.pin(2), (pb[0], y - 10.16), pb)
S.junction(pa)
S.junction(pb)
# N3: harmonic trap + shunt spare
n3 = (172.72, y)
S.wire(pb, n3, (185.42, y))
S.junction(n3)
lt = shunt("L", "L304", "DNP", n3, dnp=True, mpn="2.1 GHz trap L (fit only if spurious fails)", gnd=False)
ct = S.place("Device:C", C, "C306", "DNP", n3[0], lt.pin(2)[1] + 5.08, footprint=C0402, dnp=True,
             fields={"MPN": "2.1 GHz trap C"})
S.wire(lt.pin(2), ct.pin(1))
S.gnd(ct.pin(2))
shunt("C", "C307", "DNP", (185.42, y), dnp=True, mpn="shunt spare")
S.junction((185.42, y))
# N4: antenna node at the copper edge (X = 63)
n4 = (210.82, y)
S.wire((185.42, y), n4)
S.label((198.12, y), "RF_FEED", "up")
l301 = shunt("L", "L301", "22nH", n4, mpn="LQW15AN22NG class, rated for ESD residue")
S.junction(n4)
tv = S.place("Device:D_TVS", stock("Device", "D_TVS"), "D301", "ESD <=0.3pF", 226.06, y + 7.62, rot=90,
             footprint="Bingbong_v3:ESD_0201_antenna_TBD", fields={"MPN": "antenna-grade ESD <= 0.3 pF (Murata LXES / Nexperia PESD class) [U]"},
             ref_off=(10, -1.3), val_off=(11, 1.3))
S.wire(n4, (226.06, y), tv.pin(2))
S.gnd(tv.pin(1))
S.junction((226.06, y))
tp = S.place("Connector:TestPoint", stock("Connector", "TestPoint"), "TP301", "DC TEST", 241.3, y,
             footprint="TestPoint:TestPoint_Pad_D1.0mm", ref_off=(2, -3.5), val_off=(2, -1))
S.wire((226.06, y), (241.3, y))
S.junction((241.3, y))
fin = S.place("Connector_Generic:Conn_01x01", stock("Connector_Generic", "Conn_01x01"), "J302", "FEED FINGER",
              264.16, y, rot=180, footprint="Bingbong_v3:SpringFinger_2.0mm_TBD",
              fields={"MPN": "SMT BeCu spring finger, 2.0 mm free height, Au [U]"}, ref_off=(0, -3), val_off=(0, 3.5))
S.wire((241.3, y), fin.pin(1))
S.text((272, 77), "-> finger -> gold land on the cap's\n   feed tab -> 6061 END CAP (antenna)", NOTE)

# zone markers under the chain
S.text((20, 124), "|<-- SiP side -->|<-- test -->|<------------------ matching network (X = 53-63, one straight line of 0402s) ------------------>|<- X = 63: copper ends ->|<- feed trace X 63-65.5, finger X 65.5-67.5 ->|", 1.0)

# ============================================================ B. what each part does
S.box((15, 145), (200, 262), "B · What each part does")
S.text((19, 153), "C301 100 pF: DC block. L301 shorts the antenna node to GND at DC, so the nRF's ANT pin must\n"
                  "  not see that short (its DC tolerance is not published). ~0 ohms at 700-2200 MHz.\n\n"
                  "J301 MM8130-2600: RF switch connector. Normally a closed through-path. A test probe pushed in\n"
                  "  lifts the internal spring: the probe then connects to the nRF (pin C) and the antenna side\n"
                  "  is cut off -> conducted power / sensitivity / frequency tests on every unit (%XRFTEST).\n\n"
                  "R301 0R: spare SERIES position. C305 / L303 / C307: spare SHUNT positions (DNP).\n\n"
                  "C304 3.3 pF (series) + C303 1.5 pF (shunt) + L302 15 nH || C302 1.0 pF (series): the dual-band\n"
                  "  match. L302 alone would pass 700 MHz and block 1900 MHz; C302 in parallel makes the pair\n"
                  "  resonate at ~1.3 GHz, so it looks INDUCTIVE at 700 MHz (cancels the cap's capacitive\n"
                  "  reactance) and CAPACITIVE at 1900 MHz. That is how one network serves B12 and B2/B4.\n\n"
                  "L304 + C306 (DNP): series-LC to GND = a notch at ~2.1 GHz, fitted only if the 3rd harmonic\n"
                  "  of B12 (2097-2148 MHz, inside B4's receive band) fails the radiated-spurious pre-scan.", NOTE)

S.box((210, 145), (405, 262), "C · Antenna node, ESD and layout rules")
S.text((214, 153), "L301 22 nH to GND: the first low-band match element AND the DC return. The metal cap is\n"
                   "  touched by users; L301 bleeds its static charge to GND continuously.\n"
                   "D301 (<= 0.3 pF): clamps ESD hitting the cap (+/-8 kV contact) before any series part.\n"
                   "  Must be tiny in capacitance, or it detunes the 700 MHz match.\n"
                   "TP301: DC test pad - checks finger-to-cap continuity (a few ohms through L301) at EOL.\n\n"
                   "Layout (report E-11, 5.11):\n"
                   " - ANT_RF -> J301: 50-ohm CPWG on L1 over solid L2 GND (~0.18 mm / 0.15 mm gap, fab\n"
                   "   solver final); ground vias every ~1 mm along both edges; nothing else within 2 mm.\n"
                   " - Match parts in ONE straight line, shunt grounds via-in-pad or <= 0.5 mm to GND vias.\n"
                   " - Copper on ALL six layers ends at X = 63.0; only the feed trace + finger pad beyond.\n"
                   " - Feed trace X 63-65.5 is part of the antenna, not a 50-ohm line.\n"
                   " - SPI clock routed on the far side of the board from this strip.\n\n"
                   "Tuning: measure the cap's impedance (Mule B / EVM-1), then pick values\n"
                   "(Murata/Coilcraft high-Q 0402, +/-0.05 pF / +/-2 %). Goal >= 15 % efficiency at 699-746 MHz.", NOTE)

S.text((15, 268), "Interfaces   in: ANT_RF (nrf9151 pin 35)   out: the end cap via J302   Refs 3xx   DNP = footprint only   [U] = value/part to be tuned or chosen", 1.4)
S.write()
write_custom_lib(CUSTOM)
print("wrote rf.kicad_sch")

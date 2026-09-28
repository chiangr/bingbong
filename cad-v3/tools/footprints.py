"""Custom footprints, each transcribed from the manufacturer's land-pattern drawing (datasheets saved in
firmware/bingbong_pcb/_mech/). A footprint is only added here once its drawing has been read and checked.
"""
from fpgen import FP

made = []

# ---- BQ25188 — TI SLUSFJ3 pp.50-52, YBG0008-C01 (4229296/A 12/2022)
# 2 cols x 4 rows, 0.4 mm pitch both ways; body D 1.59 (rows) x E 1.04; land Ø0.23 NSMD, mask +0.05 max;
# stencil 0.25 mm square R0.05 (0.1 mm stencil). Top view: A1 top-left, rows A..D top to bottom.
f = FP("TI_YBG0008_DSBGA-8", "BQ25188 YBG0008 DSBGA-8 2x4 0.4 mm", 1.04, 1.59, "TI SLUSFJ3 YBG0008-C01 pp.50-52")
for ri, row in enumerate("ABCD"):
    for ci, col in enumerate((1, 2)):
        f.bga(f"{row}{col}", -0.2 + 0.4 * ci, -0.6 + 0.4 * ri, 0.23, 0.05, paste_sq=0.25, paste_rr=0.05)
made.append(f.write(pin1=(-0.62, -0.95)))

# ---- TPS62840DLC — TI SLVSEC6D pp.36-38, DLC0008B (4224310/A 05/2018)
# body 1.5 x 2.0; 8 pads 0.6 x 0.25 R0.05, pitch 0.5, pad-centre columns 1.3 apart; NSMD +0.05;
# stencil = copper. Top view: pin 1 top-left, 1-4 down the left, 5-8 up the right.
f = FP("TI_DLC0008_SON-8_1.5x2", "TPS62840 DLC0008B VSON-HR-8 1.5x2 0.5 mm", 1.5, 2.0, "TI SLVSEC6D DLC0008B pp.36-38")
for i in range(4):
    y = -0.75 + 0.5 * i
    f.smd(str(1 + i), -0.65, y, 0.6, 0.25, r=0.05, mask=0.05)
    f.smd(str(8 - i), 0.65, y, 0.6, 0.25, r=0.05, mask=0.05)
made.append(f.write(pin1=(-1.15, -0.75)))

# ---- DRV2625 — TI SLOS879C pp.72-74, YFF0009-C01 (4221850/A 01/2015)
# 3x3, 0.4 mm pitch; body E 1.468 (1.438-1.498) x D 1.331 (1.301-1.361); land Ø0.225 NSMD mask +0.05 max;
# stencil 0.25 square R0.05. Top view: A1 top-left, rows A..C top to bottom, cols 1..3 left to right.
f = FP("TI_YFF0009_DSBGA-9", "DRV2625 YFF0009 DSBGA-9 3x3 0.4 mm", 1.468, 1.331, "TI SLOS879C YFF0009-C01 pp.72-74")
for ri, row in enumerate("ABC"):
    for ci in range(3):
        f.bga(f"{row}{ci + 1}", -0.4 + 0.4 * ci, -0.4 + 0.4 * ri, 0.225, 0.05, paste_sq=0.25, paste_rr=0.05)
made.append(f.write(pin1=(-0.9, -0.82)))

# ---- TPS22916 — TI SLVSDO5F pp.24-26, YFP0004 (4223507/A 01/2017)
# 2x2, 0.4 mm pitch; body 0.78 x 0.78 (0.75-0.81); land Ø0.23 NSMD mask +0.05 max; stencil 0.25 square R0.05
# (checked on the rendered drawing). Top view: A1 top-left.
f = FP("TI_YFP0004_WCSP-4", "TPS22916 YFP0004 DSBGA-4 2x2 0.4 mm", 0.78, 0.78, "TI SLVSDO5F YFP0004 pp.24-26")
for ri, row in enumerate("AB"):
    for ci in range(2):
        f.bga(f"{row}{ci + 1}", -0.2 + 0.4 * ci, -0.2 + 0.4 * ri, 0.23, 0.05, paste_sq=0.25, paste_rr=0.05)
made.append(f.write(pin1=(-0.6, -0.6)))

# ---- SN74LVC2G34DCK — TI SCES359J pp.27-29, DCK0006A (4214835/D)
# pads 0.9 x 0.4 R0.05, pitch 0.65, (2.2) = pad CENTRE-to-centre (dash-dot centrelines on the drawing)
# -> centres x = +/-1.1; NSMD mask 0.07 max; stencil = copper (0.125 mm). Body 1.25 x 2.0.
# Top view: 1-3 down the left, 4-6 up the right (6 top-right).
# FIX 2026-09-28: was x = +/-0.65 (2.2 misread as the overall span); re-read on the PDFKit render of p.28.
f = FP("TI_DCK0006A_SC70-6", "SN74LVC2G34 DCK0006A SC70-6 0.65 mm", 1.25, 2.0, "TI SCES359J DCK0006A pp.27-29")
for i in range(3):
    y = -0.65 + 0.65 * i
    f.smd(str(1 + i), -1.1, y, 0.9, 0.4, r=0.05, mask=0.05)
    f.smd(str(6 - i), 1.1, y, 0.9, 0.4, r=0.05, mask=0.05)
made.append(f.write(pin1=(-1.8, -0.65)))

# ---- Bed-of-nails test pad — report E-16: ø0.9 mm ENIG, bottom side (place flipped). No paste (bare pad
# for the pogo pin); mask opening = pad + 0.05.
f = FP("TestPoint_Pad_D0.9mm_ENIG", "Bed-of-nails test pad ø0.9 mm, no paste", 0.9, 0.9, "report E-16 fixture spec")
f.items.append(__import__("fpgen")._pad("1", "circle", 0, 0, 0.9, 0.9, '"F.Cu" "F.Mask"', mask=0.05))
f._grow(0, 0, 1.0, 1.0)
made.append(f.write())

# ---- nRF9151 LGA-113 — Nordic nRF9151 HW Design Guidelines "footprint" Figs 1-3 + PS mechanical Table 1
# (screens in firmware/bingbong_pcb/_mech/nrf9151_ps_screens/). Top view, package 12.1 (x) x 11.1 (y).
# Copper: A/B corner 0.7x0.7 at (+/-5.5, +/-5.0) [D2 11.0, E2 10.0 centre-to-centre]; C 0.3 (along edge) x 0.45,
# 0.5 pitch, outer edge flush with the corner pads (0.2 inside the outline): rows y = +/-5.125, x = -4.75..4.75
# (20 each); columns x = +/-5.625, y = -4.25..4.25 (18 each). E 1.6x1.6 at (+/-2.85, {-2.85,0,2.85}) and (0,0)
# [L5, K5, K6]; F 1.6x1.95 at (0, +/-3.575) [K3]; D 0.2x0.2: columns x = +/-4.1 [L3] at each E row +/-0.55 [e],
# and x = {-0.55, 0, 0.55} [L4] at y = +/-2.15 [K4]. NSMD, mask +0.05 on every pad (Fig. 1).
# Paste (Nordic "Solder paste stencil", 80-100 um): A/B/E/F ~75 % (E 1.39 sq per Nordic's example; A/B 0.6 sq;
# F 1.39x1.69), C 0.25 x 0.45 (Nordic's example, 83 %), D no paste (Nordic allows). Rounded paste corners.
# Numbering: left column 1 (B, top) .. 20 (A, bottom); bottom row 21 (left) .. 40; right column 41 (A, bottom) ..
# 60 (A, top); top row 61 (right) .. 80 (left) -> corners 1/20/41/60 = GND per Nordic's pin table.
# Inner 81-104 all RESERVED/NC and 105-113 all GND, so their order cannot change connectivity.
# Deviation: pad B drawn square (Nordic chamfers it as a pin-1 cue; chamfer size not dimensioned). Pin 1 marked
# on silk and fab instead.
f = FP("Nordic_nRF9151_LGA-113_12.1x11.1", "nRF9151 SiP LGA-113 12.1x11.1 mm", 12.1, 11.1,
       "Nordic nRF9151 HW Design Guidelines footprint Figs 1-3 + PS Table 1")
M = 0.05
for n, (x, y) in {1: (-5.5, -5.0), 20: (-5.5, 5.0), 41: (5.5, 5.0), 60: (5.5, -5.0)}.items():
    f.land(str(n), x, y, 0.7, 0.7, M, paste=(0.6, 0.6))
for k in range(18):                       # side columns
    y = -4.25 + 0.5 * k
    f.land(str(2 + k), -5.625, y, 0.45, 0.3, M, paste=(0.45, 0.25))
    f.land(str(59 - k), 5.625, y, 0.45, 0.3, M, paste=(0.45, 0.25))
for k in range(20):                       # top / bottom rows
    x = -4.75 + 0.5 * k
    f.land(str(21 + k), x, 5.125, 0.3, 0.45, M, paste=(0.25, 0.45))
    f.land(str(80 - k), x, -5.125, 0.3, 0.45, M, paste=(0.25, 0.45))
big = {105: (-2.85, -2.85, "E"), 112: (0, -3.575, "F"), 111: (2.85, -2.85, "E"),
       113: (-2.85, 0, "E"), 106: (0, 0, "E"), 110: (2.85, 0, "E"),
       107: (-2.85, 2.85, "E"), 108: (0, 3.575, "F"), 109: (2.85, 2.85, "E")}
for n, (x, y, t) in big.items():
    if t == "E":
        f.land(str(n), x, y, 1.6, 1.6, M, paste=(1.39, 1.39), paste_r=0.1)
    else:
        f.land(str(n), x, y, 1.6, 1.95, M, paste=(1.39, 1.69), paste_r=0.1)
dn = iter(list(range(81, 90)) + list(range(101, 92, -1)) + [102, 103, 104] + [92, 91, 90])
for x0 in (-4.1, 4.1):                    # left 81-89, right 101-93, top to bottom
    for yr in (-2.85, 0, 2.85):
        for dy in (-0.55, 0, 0.55):
            f.land(str(next(dn)), x0, yr + dy, 0.2, 0.2, M)
for y0 in (-2.15, 2.15):                  # middle rows: 102-104 upper, 92-90 lower
    for x in (-0.55, 0, 0.55):
        f.land(str(next(dn)), x, y0, 0.2, 0.2, M)
made.append(f.write(pin1=(-6.35, -5.0)))

# ---- TPD1E05U06DYA — TI SLVSBO7O pp.24-26, DYA0002A SOD-523 (4224978/B 09/2021)
# 2 pads 0.67 (x) x 0.4 (y) R0.05, centre-to-centre (1.48) -> x = +/-0.74; NSMD +0.05; stencil = copper
# (0.1 mm). Body 1.6 x 0.8 (1.5-1.7 x 0.75-0.85). Pin 1 = I/O (left, cathode), pin 2 = GND (right).
f = FP("TI_DYA0002A_SOD-523", "TPD1E05U06 DYA0002A SOD-523, pin 1 = I/O", 1.6, 0.8, "TI SLVSBO7O DYA0002A pp.24-26")
f.smd("1", -0.74, 0, 0.67, 0.4, r=0.05, mask=0.05)
f.smd("2", 0.74, 0, 0.67, 0.4, r=0.05, mask=0.05)
made.append(f.write(pin1=(-1.35, -0.45)))

# ---- DRV5032DU DMR — TI SLVSDC7 DMR0004A pp.35-37 (4222825/B 05/2022; DMR0004B land pattern identical),
# read via the macOS PDF renderer (poppler mis-renders its fonts). Pads 1-4: 0.22 (x) x 0.4 (y) R0.05 at
# x = +/-0.25 (2X 0.5 pitch), y = +/-0.7 ((1.4) is row centre-to-centre); 1 top-left, 4 top-right, 2 bottom-left,
# 3 bottom-right. Exposed pad 5: 0.8 x 0.6 centred (optional Ø0.2 via). NSMD +0.05. Paste: pads 1-4 = copper,
# pad 5 = 0.76 x 0.57 R0.05 (90 %). Body 1.1 x 1.4. KiCad's stock X2SON-4 (older revision) differs.
f = FP("TI_DMR0004_X2SON-4", "DRV5032 DMR0004A X2SON-4 1.1x1.4 0.5 mm, EP 0.8x0.6", 1.1, 1.4, "TI SLVSDC7 DMR0004A pp.35-37")
for n, (x, y) in {"1": (-0.25, -0.7), "4": (0.25, -0.7), "2": (-0.25, 0.7), "3": (0.25, 0.7)}.items():
    f.smd(n, x, y, 0.22, 0.4, r=0.05, mask=0.05)
f.items.append(__import__("fpgen")._pad("5", "roundrect", 0, 0, 0.8, 0.6, '"F.Cu" "F.Mask"', rr=0.05 / 0.6, mask=0.05))
f.items.append(__import__("fpgen")._pad("", "roundrect", 0, 0, 0.76, 0.57, '"F.Paste"', rr=0.05 / 0.57))
made.append(f.write(pin1=(-0.62, -0.95)))

# ---- MX25R1635F USON-8 2x3 — IPC-7351B derivation (owner-approved 2026-09-23; spec section 11).
# Inputs: Macronix v1.6 p.81 outline (+ L1 pull-back 0-0.15), identical to Winbond W25Q16JV UX / JEDEC MO-220.
# Nominal density, toe 0.30 heel 0 side -0.04, F 0.05 P 0.025 -> Z 3.75, G 1.65, X 0.25 (the flush-terminal
# case reproduces KiCad's stock Winbond_USON-8-1EP_3x2mm exactly). Pads 1.05 x 0.25, centres x = +/-1.35,
# y = -0.75..0.75. Pins 1-4 left top->bottom, 5-8 right bottom->top (Macronix pin diagram). Body 3.0 (x) x 2.0 (y).
# Centre strip (0.2 x 1.6): no copper; F.Cu + via keep-out per Macronix note.
f = FP("Macronix_USON-8_2x3", "MX25R1635F USON-8 2x3 0.5 mm, IPC-7351B (pull-back aware), strip keep-out",
       3.0, 2.0, "IPC-7351B from Macronix MX25R1635F v1.6 p.81 + Winbond W25Q16JV UX")
for i in range(4):
    y = -0.75 + 0.5 * i
    f.smd(str(1 + i), -1.35, y, 1.05, 0.25, r=0.0625, mask=0.05)
    f.smd(str(8 - i), 1.35, y, 1.05, 0.25, r=0.0625, mask=0.05)
f.keepout(-0.2, -0.9, 0.2, 0.9)
made.append(f.write(pin1=(-2.05, -0.75)))

# ---- MT6701QT QFN-16 3x3 — IPC-7351B from MagnTek Rev 1.5 §9.2 (owner-approved 2026-09-24).
# Z 3.75 G 2.00 X 0.25 -> pads 0.875 x 0.25 at +/-1.4375 (= KiCad stock QFN-16-1EP_3x3mm_P0.5mm, Linear source).
# Top view (bottom view mirrored): 1-4 left top->bottom, 5-8 bottom left->right, 9-12 right bottom->top,
# 13-16 top right->left. Exposed pad: land 1.5 x 1.5 (EP is 1.6-1.8; keeps 0.25 mm to the signal pads),
# pad "EP", deliberately NO net (datasheet silent on it); paste 1.1 x 1.1 (~54 %). Sensing centre = origin.
f = FP("QFN-16_3x3_MT6701", "MT6701 QFN-16 3x3 0.5 mm, IPC-7351B; EP soldered, unconnected", 3.0, 3.0,
       "IPC-7351B from MagnTek MT6701 Rev1.5 9.2")
c, rr = 1.4375, 0.0625
for i in range(4):
    t = -0.75 + 0.5 * i
    f.smd(str(1 + i), -c, t, 0.875, 0.25, r=rr, mask=0.05)      # left, top->bottom
    f.smd(str(5 + i), t, c, 0.25, 0.875, r=rr, mask=0.05)       # bottom, left->right
    f.smd(str(12 - i), c, t, 0.875, 0.25, r=rr, mask=0.05)      # right, bottom->top  (12 at top)
    f.smd(str(16 - i), t, -c, 0.25, 0.875, r=rr, mask=0.05)     # top, right->left    (16 at left)
f.land("EP", 0, 0, 1.5, 1.5, 0.05, paste=(1.1, 1.1), paste_r=0.1)
made.append(f.write(pin1=(-2.1, -0.75)))

# ---- AS5600L-AWLM WLCSP-15 — IPC-7351B collapsing-ball land from ams DS000545 Figure 42 (owner-approved).
# 5 x 3 balls, pitch 0.5, ball Ø0.329 -> land Ø0.26 NSMD (+0.05), paste □0.28 R0.05. Package 2.07 (x) x 2.63 (y).
# Orientation = ams top-through view rotated 90° CW (no mirror): A1 top-left, A->E downward, 1->3 rightward.
# Hall-array centre 0.172 mm from the die centre toward row E -> F.Fab cross at (0, +0.172): align the MAGNET
# AXIS to that point, not to the package centre.
f = FP("ams_WLCSP-15_2.07x2.63_P0.5", "AS5600L WLCSP-15 0.5 mm, IPC land Ø0.26; Hall centre at (0,+0.172)",
       2.07, 2.63, "IPC-7351B from ams AS5600L DS000545 v1-12 Fig.42")
for i, row in enumerate("ABCDE"):
    for j in range(3):
        f.bga(f"{row}{j + 1}", -0.5 + 0.5 * j, -1.0 + 0.5 * i, 0.26, 0.05, paste_sq=0.28, paste_rr=0.05)
import fpgen
hy = 0.172
f.items.append(fpgen._line((-0.4, hy), (0.4, hy), "F.Fab", 0.03))
f.items.append(fpgen._line((0, hy - 0.4), (0, hy + 0.4), "F.Fab", 0.03))
f.items.append(fpgen._circle((0, hy), 0.15, "F.Fab", 0.03))
made.append(f.write(pin1=(-1.25, -1.0)))

# ---- SN74LV1T34DCK — TI SCLS743E pp.20-22, DCK0005A (4214834/G 11/2024), read on the PDFKit render.
# 5X pads 0.95 x 0.4 R0.05; (2.2) pad centre-to-centre -> x = +/-1.1; pins 1-3 at y = -0.65/0/0.65 on the left,
# 4 bottom-right, 5 top-right (no pad at right-middle). NSMD mask 0.07 max (0.05 used); stencil = copper
# (0.125 mm). Body 1.25 x 2.0 nominal (1.1-1.4 x 1.85-2.15).
f = FP("TI_DCK0005A_SC70-5", "SN74LV1T34 DCK0005A SC70-5 0.65 mm", 1.25, 2.0, "TI SCLS743E DCK0005A pp.20-22")
for n, (x, y) in {1: (-1.1, -0.65), 2: (-1.1, 0), 3: (-1.1, 0.65), 4: (1.1, 0.65), 5: (1.1, -0.65)}.items():
    f.smd(str(n), x, y, 0.95, 0.4, r=0.05, mask=0.05)
made.append(f.write(pin1=(-1.85, -0.65)))

# ---- TCA9406YZP — TI SCPS221G pp.35-37, YZP0008 (4223082/A 07/2016), read on the PDFKit render.
# 2 cols x 4 rows, 0.5 mm pitch; land Ø0.23 NSMD, mask +0.05 max; stencil 0.25 square R0.05 (0.1 mm).
# Body D 1.888 (1.858-1.918) x E 0.888 (0.858-0.918). Top view: A1 top-left, rows A..D downward.
f = FP("TI_YZP0008_DSBGA-8", "TCA9406 YZP0008 DSBGA-8 2x4 0.5 mm", 0.888, 1.888, "TI SCPS221G YZP0008 pp.35-37")
for ri, row in enumerate("ABCD"):
    for ci in range(2):
        f.bga(f"{row}{ci + 1}", -0.25 + 0.5 * ci, -0.75 + 0.5 * ri, 0.23, 0.05, paste_sq=0.25, paste_rr=0.05)
made.append(f.write(pin1=(-0.62, -1.12)))

# ---- TPS7A02 DQN — TI SBVS277C pp.39-41, DQN0004A (4215302/E 12/2016), read on the PDFKit render.
# Land (top view): 4 chamfered pads, centres x = +/-0.43 (0.86), y = +/-0.325 (0.65); 0.36 long x 0.21 high;
# inner end: 0.03 straight then a 45 deg chamfer 0.18 x 0.18 facing the centre pad (0.22 metal clearance -
# checked: chamfer line |x|+|y| = 0.65 vs pad-5 edge 0.339 -> 0.22). Pad 5 = 0.48 square rotated 45 deg.
# Mask 0.05 min all round. Stencil: signal apertures 0.4 long (outer end at 0.65) with 0.22 short edge,
# same chamfer line (0.235 to the pad-5 aperture); pad 5 aperture 0.45 square rotated (88 %).
# Pin map (top view): 1 top-left OUT, 2 bottom-left GND, 3 bottom-right EN, 4 top-right IN, 5 GND.
f = FP("TI_DQN0004A_X2SON-4_1x1", "TPS7A02 DQN0004A X2SON-4 1x1", 1.0, 1.0, "TI SBVS277C DQN0004A pp.39-41")
_ = __import__("fpgen")
for n, (sx, sy) in {1: (-1, -1), 2: (-1, 1), 3: (1, 1), 4: (1, -1)}.items():
    for outer, layers, mask, num in ((0.61, '"F.Cu" "F.Mask"', 0.05, str(n)), (0.65, '"F.Paste"', None, "")):
        pts = [(outer, 0.43), (0.25, 0.43), (0.25, 0.40), (0.43, 0.22), (outer, 0.22)]
        f.poly(num, [(sx * x, sy * y) for x, y in pts], layers=layers, mask=mask)
f.items.append(_._pad("5", "rect", 0, 0, 0.48, 0.48, '"F.Cu" "F.Mask"', mask=0.05, angle=45))
f.items.append(_._pad("", "rect", 0, 0, 0.45, 0.45, '"F.Paste"', angle=45))
made.append(f.write(pin1=(-0.85, -0.55)))

# ---- Murata DFE252010F (L401/L402, 4.7 uH) — spec J(E)TE243A-0012D-01 p.1 (body 2.5 +/-0.2 x 2.0 +/-0.2 x 1.0 max,
# electrode 0.6 +/-0.2) and p.5 "Recommended PCB pattern": two 0.8 x 2.0 pads, 1.2 gap, 2.8 overall -> centres
# x = +/-1.0. Mask +0.05, paste = copper. Same land for DFE252010P / DFE252008U / Taiyo LSANB2520 (backups).
f = FP("L_Murata_DFE252010F", "Murata DFE252010F 2520 metal-alloy inductor, 1.0 mm max", 2.5, 2.0,
       "Murata J(E)TE243A-0012D-01 pp.1,5")
for n, x in ((1, -1.0), (2, 1.0)):
    f.smd(str(n), x, 0, 0.8, 2.0, mask=0.05)
f.bw, f.bh = 2.7, 2.2        # courtyard/fab at the +0.2 body tolerance
made.append(f.write())

# ---- TPS65631DPDR WSON-12 3x3 — IPC-7351B from TI SLVSBK1E outline 4212354/C + thermal pad 4212468/A
# (no land pattern in the datasheet; owner-approved derivation 2026-09-28). Inputs: body 2.90-3.10 (flush
# terminals), lead L 0.30-0.50, b 0.15-0.25, e 0.45, 6 leads per side; EP 2.02 x 1.21 (+/-0.10), C0.30 pin-1.
# Same parameters as the MX25R/MT6701 (toe 0.30, heel 0, side -0.04, F 0.05, P 0.025, S tol RMS-reduced):
# Z 3.708 -> 3.75, G 2.022 -> 2.00, X 0.185 -> 0.20  =>  12 pads 0.875 x 0.20 at x = +/-1.4375.
# Mask +0.05 -> 0.15 mm slivers at 0.45 pitch. EP land = nominal 1.21 x 2.02 (0.395 mm to the signal pads),
# paste 1.0 x 1.75 (72 %). Orientation: TI top view rotated 90 deg (no mirror): 1-6 down the left,
# 7-12 up the right (12 top-right). Pin 13 = EP = GND. Thermal/GND vias in the EP: filled or tented.
f = FP("TI_DPD0012_WSON-12_3x3", "TPS65631 DPD WSON-12 3x3 0.45 mm, IPC-7351B", 3.0, 3.0,
       "IPC-7351B from TI SLVSBK1E DPD 4212354/C + 4212468/A")
for i in range(6):
    y = -1.125 + 0.45 * i
    f.smd(str(1 + i), -1.4375, y, 0.875, 0.20, r=0.05, mask=0.05)
    f.smd(str(12 - i), 1.4375, y, 0.875, 0.20, r=0.05, mask=0.05)
f.land("13", 0, 0, 1.21, 2.02, 0.05, paste=(1.0, 1.75), paste_r=0.1)
made.append(f.write(pin1=(-2.1, -1.125)))

# ---- Kingbright APTF1616SEEZGQBDC RGB (D501) — DSAJ8681 rev V.14B p.1 "Recommended soldering pattern" (tol +/-0.1):
# 4 pads 0.85 x 0.5; 2.6 overall with 0.9 gap -> x = +/-0.875; 1.5 overall with 0.5 gap -> y = +/-0.5.
# Top view (p.1): 1 anode bottom-right, 2 red K bottom-left, 3 green K top-left, 4 blue K top-right.
# Body 1.6 x 1.6 x 0.7. Mask +0.05, paste = copper.
f = FP("LED_Kingbright_APTF1616", "Kingbright APTF1616 1.6x1.6 RGB common anode", 1.6, 1.6,
       "Kingbright APTF1616SEEZGQBDC DSAJ8681 V.14B p.1")
for n, (x, y) in {1: (0.875, 0.5), 2: (-0.875, 0.5), 3: (-0.875, -0.5), 4: (0.875, -0.5)}.items():
    f.smd(str(n), x, y, 0.85, 0.5, mask=0.05)
made.append(f.write(pin1=(1.55, 0.95)))

# ---- MFF2 eUICC (U202) — Velocity IoT VIOT-1SIM-MFF2 datasheet p.4 "Package Footprint" (read on the render),
# package per ETSI TS 102 671 V17 Table 6.3 (body 5.0 x 6.0). Drawing: 8 pads 0.4 x 0.8 at 1.27 pitch, rows 5.7
# apart; pin 1 bottom-left, 1-4 left->right along the bottom, 5-8 right->left along the top (8 = VCC opposite
# 1 = GND). Drawn here rotated 90 deg CW (no mirror) so pin 1 is top-left: 1-4 down the left column
# (x = -2.85, y = -1.905..+1.905), 5-8 up the right (x = +2.85). Centre pad 3.4 x 4.2, NO net (ETSI Annex A:
# not electrically connected); stencil 3x3 windows 1.2 long, 0.8/1.2/0.8 wide, 0.25 gaps. Mask +0.05.
import fpgen as _fg
f = FP("MFF2_DFN-8_5x6", "MFF2 eUICC DFN-8 5x6 (ETSI TS 102 671), centre pad unconnected", 6.0, 5.0,
       "Velocity IoT VIOT-1SIM-MFF2 p.4 + ETSI TS 102 671 V17 Table 6.3")
for i, y in enumerate((-1.905, -0.635, 0.635, 1.905)):
    f.smd(str(1 + i), -2.85, y, 0.8, 0.4, mask=0.05)
    f.smd(str(8 - i), 2.85, y, 0.8, 0.4, mask=0.05)
f.items.append(_fg._pad("", "rect", 0, 0, 3.4, 4.2, '"F.Cu" "F.Mask"', mask=0.05))
for y in (-1.45, 0, 1.45):
    for x, w in ((-1.25, 0.8), (0, 1.2), (1.25, 0.8)):
        f.items.append(_fg._pad("", "rect", x, y, w, 1.2, '"F.Paste"'))
made.append(f.write(pin1=(-3.45, -1.905)))

# ---- Murata MM8130-2600 (J301) — catalog O30E (Dec 22 2025) p.7 "Standard Pattern Dimensions" + p.8 stencil.
# Signal axis along Y. GND lands 0.75 x 0.80: x edges 1.30 / 2.80 overall, y edges 1.10 / 2.70 -> (+/-1.025, +/-0.95).
# Signal lands 0.50 x 0.58: y edges 1.74 / 2.90 -> (0, +/-1.16). Stencil 0.12 mm: GND 0.59 x 0.80 (x 1.30 / 2.48),
# signal 0.28 x 0.28 (y 2.14 / 2.70). Pads named for the KiCad CoaxialSwitch_Testpoint symbol: C = Murata
# "inner terminal (C)" = IN = SiP side (p.5: probe in -> C connects to probe, R cut off), A = R = antenna side,
# G = 4 GND. The land is symmetric: place the part with its C terminal on pad C (silk dot). Our board keeps
# only these lands; the ANT trace is our own 50-ohm CPWG (Murata's resist-covered electrode is its test board).
import fpgen as _fg
f = FP("Murata_MM8130-2600", "Murata MM8130-2600 RF switch connector 2.5x2.5, C = SiP side", 2.5, 2.5,
       "Murata O30E pp.5,7,8")
for sx in (-1, 1):
    for sy in (-1, 1):
        f.land("G", sx * 1.025, sy * 0.95, 0.75, 0.80, 0.05)
        f.items.append(_fg._pad("", "rect", sx * 0.945, sy * 0.95, 0.59, 0.80, '"F.Paste"'))
for n, sy in (("C", -1), ("A", 1)):
    f.land(n, 0, sy * 1.16, 0.50, 0.58, 0.05)
    f.items.append(_fg._pad("", "rect", 0, sy * 1.21, 0.28, 0.28, '"F.Paste"'))
made.append(f.write(pin1=(0, -1.85)))

# ---- Panasonic EZAEG1N50AC antenna ESD suppressor (D301), 0201 — AWD0000C13 p.2 "Recommended land pattern":
# a (gap) 0.3-0.4, b (overall) 0.8-0.9, c (width) 0.25-0.35 -> nominal pads 0.25 x 0.30 at x = +/-0.30.
# Non-polar ceramic suppressor. Mask +0.05, paste = copper.
f = FP("Panasonic_EZAEG1N_0201", "Panasonic EZAEG1N 0201 ESD suppressor, 0.04 pF", 0.6, 0.3,
       "Panasonic AWD0000C13 p.2")
for n, x in ((1, -0.30), (2, 0.30)):
    f.smd(str(n), x, 0, 0.25, 0.30, mask=0.05)
made.append(f.write())

# ---- MAX17048X+T10 WLP-8 (U102) — Maxim outline 21-0555 rev E (W80B1+1) + AN1891 (2021) Tables 1-2.
# 2 x 4 bumps, e 0.40, D1 0.40, E1 1.20, ball 0.27; body E 1.670 x D 0.930. Top view: pin-1 (A1) top-left,
# row A on top (y = -0.2), row B below (y = +0.2), columns 1-4 left->right (x = -0.6..+0.6).
# NSMD land: AN1891 acceptable 0.20-0.26 at 0.4 pitch (0.25 recommended); 0.23 used (as BQ25188/TPS22916) so the
# +0.05 mask keeps a 0.07 web. Stencil 4 mil, 0.25 aperture (AN1891 Table 2), square R0.05.
f = FP("MAX_WLP-8_0.9x1.7", "MAX17048X WLP-8 2x4 0.4 mm (W80B1+1)", 1.67, 0.93, "Maxim 21-0555E + AN1891 (2021)")
for ri, row in enumerate("AB"):
    for ci in range(4):
        f.bga(f"{row}{ci + 1}", -0.6 + 0.4 * ci, -0.2 + 0.4 * ri, 0.23, 0.05, paste_sq=0.25, paste_rr=0.05)
made.append(f.write(pin1=(-1.0, -0.62)))

# ---- Murata DFE201210U (L101, 2.2 uH) — spec J(E)TE243A-0029D-01 p.1 (2.0 +/-0.2 x 1.2 +/-0.2 x 1.0 max) and p.5
# pattern: two 0.8 x 1.4 pads, 0.8 gap, 2.4 overall -> x = +/-0.8. Murata: no vias/copper under the body.
f = FP("L_Murata_DFE201210U", "Murata DFE201210U 2012 metal-alloy inductor, 1.0 mm max", 2.0, 1.2,
       "Murata J(E)TE243A-0029D-01 pp.1,5")
for n, x in ((1, -0.8), (2, 0.8)):
    f.smd(str(n), x, 0, 0.8, 1.4, mask=0.05)
f.bw, f.bh = 2.2, 1.4
made.append(f.write())

# ---- Diodes SOT-23 (Q101 DMP3099L-7) — DS36081 Rev 5-2 p.5 "Suggested Pad Layout": X 0.8, Y 0.9, C 2.0 (row
# spacing), X1 1.35 (centreline to the outer pad edge -> pad centres x = +/-0.95), Y1 2.9. Pinout (p.1 top view):
# G bottom-left = 1, S bottom-right = 2, D top = 3 (matches Q_PMOS_GSD). Body 2.9 x 1.3 (E1), leads to 2.4 (E).
f = FP("Diodes_SOT-23", "SOT-23 per Diodes Inc suggested pad layout", 2.9, 1.3, "Diodes DS36081 Rev 5-2 p.5")
for n, (x, y) in {1: (-0.95, 1.0), 2: (0.95, 1.0), 3: (0, -1.0)}.items():
    f.smd(str(n), x, y, 0.8, 0.9, mask=0.05)
f.bw, f.bh = 2.9, 2.4
made.append(f.write(pin1=(-1.6, 1.0)))

# ---- Nexperia SOD523 (D102 BZX585-C12) — BZX585 series Rev 9 (11 Sep 2026) p.11 Fig.12 sod523_fr: lands 0.5 x 0.6
# at 1.4 pitch (x = +/-0.7), paste 0.4 x 0.5, occupied area 2.15 x 1.2. Pin 1 = cathode (Table 2) on the left.
f = FP("Nexperia_SOD523", "SOD523 per Nexperia sod523_fr, pin 1 = cathode", 1.2, 0.8, "Nexperia BZX585 Rev 9 p.11")
for n, x in ((1, -0.7), (2, 0.7)):
    f.land(str(n), x, 0, 0.5, 0.6, 0.05, paste=(0.4, 0.5), paste_r=0.05)
made.append(f.write(pin1=(-1.15, 0)))

# ---- Murata BLM18P 0603 ferrite (FB101 BLM18PG221SN1D) — JENF243A_0003AN-01 p.10 §12.1 reflow: a 0.7 (gap),
# b 2.0 (overall), c 0.7 (width); d = 0.7 for 0.5-1.5 A at 18/35 um. -> pads 0.65 x 0.7 at x = +/-0.675.
f = FP("Murata_BLM18P_0603", "Murata BLM18P 0603 ferrite, reflow land", 1.6, 0.8, "Murata JENF243A_0003AN-01 p.10")
for n, x in ((1, -0.675), (2, 0.675)):
    f.smd(str(n), x, 0, 0.65, 0.7, mask=0.05)
made.append(f.write())

print("wrote:", ", ".join(made))

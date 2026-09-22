"""M-6: +1.8V is generated locally by U7 (MIC5504) and is NOT sequenced with the
modem, while U2.29 (VDD_EXT) - the BG95's own 1.8V IO reference output - sits
unconnected.

The ESP32 can therefore enable U7 (IO13 -> /MIC EN) while the BG95 is off. U3's
~OE is hard-tied to GND so the translator is always live, and DIR2 is tied low,
so B2 (/ESP32 TX) DRIVES A2 -> /BG95 RX -> U2.34 with the modem's IO domain
unpowered. R2 also pulls U2.17 (~RESET) up to that same local rail. Quectel's
hardware design guide prohibits this.

Fix: delete U7 (and its input cap C12 and enable pull-down R10) and source the
1.8V rail from U2.29 VDD_EXT instead. VDD_EXT is 0 V whenever the modem is off,
so the AVC2T245's VCC isolation puts the A port Hi-Z and back-powering becomes
physically impossible rather than firmware-dependent. Frees IO13.
C11 (1uF) and C4 (0.1uF) stay on the rail as VDD_EXT's decoupling.

Also connects U2.20 (STATUS), previously unconnected, to IO37 - without it the
PWRKEY toggle through Q1 is open-loop and a hung modem has no recovery path.

NOTE: respect Quectel's VDD_EXT current limit (typically 50 mA). Loads are now
U3's VCCA/DIR1, R2 (100k), J6.2 and the two caps - microamps plus translator
switching, comfortably inside it.
NOTE: #PWR040 has lib_id "power:+3.3V" but Value "+1.8V". KiCad derives the net
name from Value, so that symbol IS the 1.8V rail - it is kept, and the new
symbol mirrors the same convention.
"""
import _schedit as se
import _pins
import _trace
import _mk
import re

L = se.load()

for taken in ('#PWR0108',):
    try:
        se.find(L, taken)
        raise SystemExit(f'{taken} already exists')
    except KeyError:
        pass


def del_block(lines, start):
    end, depth = start, 0
    while end < len(lines):
        depth += lines[end].count('(') - lines[end].count(')')
        if depth == 0 and end > start:
            break
        end += 1
    del lines[start:end + 1]


def del_wire(lines, x1, y1, x2, y2):
    a = f'\t\t\t(xy {x1} {y1}) (xy {x2} {y2})'
    b = f'\t\t\t(xy {x2} {y2}) (xy {x1} {y1})'
    idx = [i for i, l in enumerate(lines) if l in (a, b)]
    assert len(idx) == 1, f'wire {(x1, y1, x2, y2)}: found {len(idx)}'
    del_block(lines, idx[0] - 2)


def del_all_labels(lines, text):
    n = 0
    while True:
        hit = next((i for i, l in enumerate(lines) if l == f'\t(label "{text}"'), None)
        if hit is None:
            break
        del_block(lines, hit)
        n += 1
    return n


P = _pins.resolve()
assert P['U2']['29'] == (287.02, 158.75), P['U2']['29']
assert P['U2']['20'] == (287.02, 166.37), P['U2']['20']
IO37 = P['U10']['30']
assert IO37 == (137.16, 200.66), IO37

# landing zones must be clear
Lp, W, LB, PN = _trace.build()
pts = set()
for ln, a, b in W:
    pts.add(a); pts.add(b)
for t, k, _k, _l in LB:
    pts.add(k)
pts |= set(PN)
for want in [(294.64, 158.75), (302.26, 158.75), (294.64, 166.37), (144.78, 200.66)]:
    near = [p for p in pts if abs(p[0] - want[0]) < 2.4 and abs(p[1] - want[1]) < 2.4]
    assert not near, f'{want} not clear: {near}'

# ---- remove the local LDO ------------------------------------------------
for w in [(464.82, 115.57, 474.98, 115.57),   # U7.1 VOUT -> C11.1/#PWR040
          (515.62, 118.11, 528.32, 118.11),   # U7.4 VIN -> C12.1/#PWR041
          (474.98, 123.19, 474.98, 118.11),   # U7.2 GND leg
          (464.82, 123.19, 474.98, 123.19),   # C11.2 -> U7.2 GND leg
          (515.62, 115.57, 537.21, 115.57),   # EP net
          (537.21, 115.57, 537.21, 125.73),
          (528.32, 125.73, 537.21, 125.73)]:
    del_wire(L, *w)
print(f'  removed {del_all_labels(L, "MIC EN")} "MIC EN" labels (frees IO13)')
for ref in ('U7', 'C12', 'R10', '#PWR039', '#PWR041'):
    a, _ = se.find(L, ref)
    del_block(L, a)
    print(f'  deleted {ref}')

# ---- source +1.8V from the modem, and close the STATUS loop -------------
new = []
new += _mk.wire(287.02, 158.75, 294.64, 158.75)
new += _mk.power('power:+3.3V', '#PWR0108', 294.64, 158.75, '+1.8V', rot=90)
new += _mk.wire(287.02, 166.37, 294.64, 166.37)
new += _mk.label('BG95_STATUS', 294.64, 166.37, 0, 'left bottom')
new += _mk.wire(IO37[0], IO37[1], IO37[0] + 7.62, IO37[1])
new += _mk.label('BG95_STATUS', IO37[0] + 7.62, IO37[1], 0, 'left bottom')

anchor, _ = se.find(L, '#PWR050')
L[anchor:anchor] = new
se.save(L)
print('  +1.8V now sourced from U2.29 VDD_EXT; U2.20 STATUS -> IO37')

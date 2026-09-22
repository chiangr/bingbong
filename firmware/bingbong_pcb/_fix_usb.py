"""H-4 / LOW-2 / section 3.1-3.2: USB-C protection.

Today the ENTIRE protection inventory on this board is U5 (D+/D- only) and
CR1-3 (SIM CLK/IO/RST). VBUS has no TVS at all, and CC1/CC2 - the two most
ESD-exposed contacts in a USB-C receptacle - carry only their 5.1k Rd each.
There is also no HF bypass anywhere on +5V; C15 (10 uF) is the only capacitor.

This adds, all reusing ESD9B5.0ST5G (already BOM row 14, SOD-923, so zero new
BOM lines) - the part is BIDIRECTIONAL, so orientation is a non-issue:
  CR4 -> USB_CC1, CR5 -> USB_CC2, CR6 -> VBUS (+5V), plus C37 100nF on +5V.

NOT included: the OVP / current-limit load switch. That needs a part decision
(AP22815AWT-7 / TPS2596 / TPD1S514 are all unverified suggestions) and a new
library symbol, and it splits +5V into connector-side and protected-side nets.

All coordinates are exact multiples of 1.27 mm.
"""
import _schedit as se
import _pins
import _trace
import _mk
import re
import uuid as U

L = se.load()

NEW = ['CR4', 'CR5', 'CR6', 'C37'] + [f'#PWR0{n}' for n in range(114, 120)]
for taken in NEW:
    try:
        se.find(L, taken)
        raise SystemExit(f'{taken} already exists')
    except KeyError:
        pass


def clone_symbol(lines, src_ref, new_ref, nx, ny):
    a, b = se.find(lines, src_ref)
    blk = lines[a:b + 1]
    m = re.match(r'\t\t\(at ([-\d.]+) ([-\d.]+)', blk[2])
    ox, oy = float(m.group(1)), float(m.group(2))
    dx, dy = round(nx - ox, 3), round(ny - oy, 3)
    out = []
    for l in blk:
        l = re.sub(r'\(uuid "[^"]*"\)', lambda _m: f'(uuid "{U.uuid4()}")', l)
        mm = re.match(r'^(\s*\(at )([-\d.]+) ([-\d.]+)(.*)$', l)
        if mm:
            l = (f'{mm.group(1)}{round(float(mm.group(2)) + dx, 3)} '
                 f'{round(float(mm.group(3)) + dy, 3)}{mm.group(4)}')
        l = l.replace(f'"Reference" "{src_ref}"', f'"Reference" "{new_ref}"')
        l = l.replace(f'(reference "{src_ref}")', f'(reference "{new_ref}")')
        # CR1's Datasheet still carries the superseded PESD part number
        l = l.replace('"Datasheet" "PESD5V0F1BLD_315"', '"Datasheet" "ESD9B5.0ST5G"')
        out.append(l)
    return out


P = _pins.resolve()
CC1, CC2 = P['J2']['A5'], P['J2']['B5']
assert CC1 == (306.07, 55.88), CC1
assert CC2 == (346.71, 55.88), CC2
# CR symbol spans 25.4 mm pin-to-pin at rot 270 (pin1 top, pin2 below)
assert P['CR1'] == {'1': (355.6, 308.61), '2': (355.6, 334.01)}, P['CR1']

Lp, W, LB, PN = _trace.build()
pts = set()
for ln, a, b in W:
    pts.add(a); pts.add(b)
for t, k, _k, _l in LB:
    pts.add(k)
pts |= set(PN)
for i, l in enumerate(Lp):
    for m in re.finditer(r'\(at ([-\d.]+) ([-\d.]+)', l):
        pts.add((round(float(m.group(1)), 2), round(float(m.group(2)), 2)))
busy = [p for p in pts if 150 <= p[0] <= 240 and 275 <= p[1] <= 345]
assert not busy, f'USB landing zone not clear: {sorted(busy)[:8]}'

TOP, BOT, GY, PY = 285.75, 311.15, 314.96, 281.94
for v in (TOP, BOT, GY, PY):
    assert abs(v / 1.27 - round(v / 1.27)) < 1e-6, f'{v} off-grid'

new = []

# ---- name the CC nets so the clamps can attach by label ------------------
new += _mk.label('USB_CC1', *CC1, 90, 'left bottom')
new += _mk.label('USB_CC2', *CC2, 90, 'left bottom')

# ---- CC1 / CC2 clamps ----------------------------------------------------
for ref, x, net, gnd in (('CR4', 160.02, 'USB_CC1', '#PWR0114'),
                         ('CR5', 180.34, 'USB_CC2', '#PWR0115')):
    new += clone_symbol(L, 'CR1', ref, x, TOP)
    new += _mk.label(net, x, TOP, 90, 'left bottom')
    new += _mk.wire(x, BOT, x, GY)
    new += _mk.power('power:GND', gnd, x, GY, 'GND')

# ---- VBUS clamp ----------------------------------------------------------
new += clone_symbol(L, 'CR1', 'CR6', 200.66, TOP)
new += _mk.wire(200.66, TOP, 200.66, PY)
new += _mk.power('power:+5V', '#PWR0116', 200.66, PY, '+5V')
new += _mk.wire(200.66, BOT, 200.66, GY)
new += _mk.power('power:GND', '#PWR0117', 200.66, GY, 'GND')

# ---- VBUS HF bypass ------------------------------------------------------
new += _mk.capacitor('C37', '100nF', 220.98, 289.56,
                     desc='VBUS HF bypass - X7R, PLACE WITHIN 5mm OF U8 PINS 18/19')
new += _mk.wire(220.98, TOP, 220.98, PY)
new += _mk.power('power:+5V', '#PWR0118', 220.98, PY, '+5V')
new += _mk.wire(220.98, 293.37, 220.98, 297.18)
new += _mk.power('power:GND', '#PWR0119', 220.98, 297.18, 'GND')

anchor, _ = se.find(L, '#PWR050')
L[anchor:anchor] = new

# ---- tidy the stale datasheet on the originals too -----------------------
for r in ('CR1', 'CR2', 'CR3'):
    old = se.set_prop(L, r, 'Datasheet', 'ESD9B5.0ST5G')
    if old != 'ESD9B5.0ST5G':
        print(f'  {r} Datasheet {old} -> ESD9B5.0ST5G')

se.save(L)
print('added CR4 (CC1), CR5 (CC2), CR6 (VBUS), C37 100nF on +5V')

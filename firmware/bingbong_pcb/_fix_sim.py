"""H-12: the SIM slot is the only user-touchable bare metal besides USB, and it is
half-protected. CR1/CR2/CR3 sit on CLK/IO/RST, but:

  /BG95_VCC = {J7.C1, U2.43} and NOTHING else - no bypass, no ESD. The USIM_VDD
  bypass is a Quectel requirement, not a nicety: without it the SIM browns out
  during ATR and card init is intermittent, which reads as a bad SIM or bad
  provisioning.

  /SIM SW  = {J7.SW, U10.24} and NOTHING else - no pull-up, no series R, no ESD,
  no cap. An exposed slot contact wired straight into ESP32 IO33 with zero
  impedance, and the pin currently FLOATS (there is not even a pull-down).

Adds:
  C38 100nF + C39 1uF + CR7 (ESD)          on /BG95_VCC
  R36 1k series, splitting SIM_SW (connector) from SIM_DET (MCU)
  R37 10k pull-up to +3.3V and C40 100nF   on SIM_DET
  CR8 (ESD)                                on SIM_SW, connector side
  C41/C42/C43 DNP 22pF shunts              on CLK/RST/IO - Quectel's SIM EMI pads

All ESD parts are ESD9B5.0ST5G cloned from CR1 (BOM row 14, bidirectional).
All coordinates are exact multiples of 1.27 mm.

NOT done: U2.42 (USIM_DET) is left unconnected. Wiring the card-detect switch to
it would let the modem see card removal too, but the required polarity/level is a
Quectel datasheet value I could not verify - connecting it wrong is worse than
leaving it. [OPEN - see section 7]

ASSUMPTION: J7's detect switch closes SW to GND on card insertion, which is the
usual nano-SIM socket arrangement and what the 10k pull-up assumes. With R37 on
the MCU side of R36, a closed switch gives 3.3 x 1k/11k = 0.30 V - a solid low
against a 3.3V VIL of ~0.83 V. Verify against the TE 2452808-1 drawing.
"""
import _schedit as se
import _pins
import _trace
import _mk
import re
import uuid as U

L = se.load()

NEW = ['C38', 'C39', 'C40', 'C41', 'C42', 'C43', 'CR7', 'CR8', 'R36', 'R37'] + \
      [f'#PWR0{n}' for n in range(120, 129)]
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
        out.append(l)
    return out


def relabel(lines, old, new, x, y):
    for i, l in enumerate(lines):
        if l == f'\t(label "{old}"' and re.match(rf'\t\t\(at {x} {y} ', lines[i + 1]):
            lines[i] = f'\t(label "{new}"'
            return
    raise AssertionError(f'label "{old}" @ {x},{y} not found')


P = _pins.resolve()
assert P['J7']['C1'] == (397.51, 360.68), P['J7']['C1']
assert P['J7']['SW'] == (397.51, 373.38), P['J7']['SW']
assert P['U10']['24'] == (96.52, 210.82), P['U10']['24']

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
busy = [p for p in pts if 460 <= p[0] <= 600 and 340 <= p[1] <= 420]
assert not busy, f'SIM landing zone not clear: {sorted(busy)[:8]}'

CY, PIN_T, PIN_B, GY = 358.14, 354.33, 361.95, 365.76        # shunt-cap row
DT, DB, DG = 378.46, 403.86, 407.67                          # ESD row (25.4 span)
COLS = [467.36, 487.68, 508.0, 528.32, 548.64, 568.96]
for v in [CY, PIN_T, PIN_B, GY, DT, DB, DG] + COLS:
    assert abs(v / 1.27 - round(v / 1.27)) < 1e-6, f'{v} off-grid'

new = []
gnd = iter([f'#PWR0{n}' for n in range(120, 128)])

# ---- shunt row: bypass on USIM_VDD, filter on SIM_DET, EMI pads on the bus ----
SHUNTS = [
    ('C38', '100nF', 'BG95_VCC', False, 'USIM_VDD bypass - X7R, place within 3-5mm of J7 pin C1'),
    ('C39', '1uF',   'BG95_VCC', False, 'USIM_VDD bulk - place close to J7 pin C1'),
    ('C40', '100nF', 'SIM_DET',  False, 'SIM detect filter - place at the MCU end'),
    ('C41', 'DNP',   'BG95_CLK', True,  'SIM EMI shunt (Quectel ref) - 22pF C0G, DNP in build 1'),
    ('C42', 'DNP',   'BG95_RST', True,  'SIM EMI shunt (Quectel ref) - 22pF C0G, DNP in build 1'),
    ('C43', 'DNP',   'BG95_IO',  True,  'SIM EMI shunt (Quectel ref) - 22pF C0G, DNP in build 1'),
]
for (ref, val, net, dnp, desc), x in zip(SHUNTS, COLS):
    new += _mk.label(net, x, PIN_T, 90, 'left bottom')
    new += _mk.capacitor(ref, val, x, CY, dnp=dnp, desc=desc)
    new += _mk.wire(x, PIN_B, x, GY)
    new += _mk.power('power:GND', next(gnd), x, GY, 'GND')

# ---- ESD on USIM_VDD and on the exposed detect contact ----------------------
for ref, x, net in (('CR7', COLS[0], 'BG95_VCC'), ('CR8', COLS[1], 'SIM_SW')):
    new += clone_symbol(L, 'CR1', ref, x, DT)
    new += _mk.label(net, x, DT, 90, 'left bottom')
    new += _mk.wire(x, DB, x, DG)
    new += _mk.power('power:GND', next(gnd), x, DG, 'GND')

# ---- split /SIM SW: connector side | 1k | MCU side --------------------------
relabel(L, 'SIM SW', 'SIM_SW', 397.51, 373.38)     # J7.SW, exposed contact
relabel(L, 'SIM SW', 'SIM_DET', 96.52, 210.82)     # U10.24 (IO33)
new += _mk.label('SIM_SW', 524.51, DT, 180, 'right bottom')
new += _mk.resistor('R36', '1k', COLS[3], DT, rot=90)
new += _mk.label('SIM_DET', 532.13, DT, 0, 'left bottom')

# 10k pull-up on the MCU side - do not rely on the internal pull-up for a pin
# that terminates on an externally exposed contact
new += _mk.wire(COLS[4], DT, COLS[4], 374.65)
new += _mk.power('power:+3.3V', '#PWR0128', COLS[4], 374.65, '+3.3V')
new += _mk.resistor('R37', '10k', COLS[4], 382.27)
new += _mk.label('SIM_DET', COLS[4], 386.08, 90, 'left bottom')

anchor, _ = se.find(L, '#PWR050')
L[anchor:anchor] = new
se.save(L)
print('added C38/C39/CR7 (USIM_VDD), R36/R37/C40/CR8 (SIM detect), C41-C43 (DNP EMI)')
print('/SIM SW split into SIM_SW (connector) and SIM_DET (MCU)')

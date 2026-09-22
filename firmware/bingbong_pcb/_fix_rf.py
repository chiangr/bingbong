"""RF block: H-9 (ANT_MAIN has no matching network) and H-8 (GNSS is a hard NC).

H-9: /ANT_MAIN is a bare two-node net - U2.60 straight to J3.1, no pi, no DC
block, no tuning pads. Without stuffing options you cannot correct for case,
battery or hand detuning without a respin. Three 0402 pads cost ~nothing.

H-8: BG95 ANT_GNSS (U2.49) is a deliberate no-connect, so the GNSS receiver you
are paying for in the -SGNS SKU is dead silicon. GNSS is IN per the 2026-09-04
decision, so this adds J8 (second MHF1) and its own pi.

Topology for each chain, per section 5.5:
    modem pin --+-- Cser --+-- connector
                |          |
              Cshunt     Cshunt        (both DNP in build 1)
                |          |
               GND        GND
Build 1 stuffing: series = 15 pF C0G (doubles as the DC block), shunts DNP.
Tune on a VNA with the case closed and the battery fitted, then freeze.

Net naming: <chain> = modem side, <chain>_OUT = connector side.
"""
import _schedit as se
import _pins
import _trace
import _mk
import re
import uuid as U

L = se.load()

for taken in ('J8', 'C31', 'C32', 'C33', 'C34', 'C35', 'C36',
              '#PWR0109', '#PWR0110', '#PWR0111', '#PWR0112', '#PWR0113'):
    try:
        se.find(L, taken)
        raise SystemExit(f'{taken} already exists')
    except KeyError:
        pass


def clone_symbol(lines, src_ref, new_ref, nx, ny):
    """Copy a placed symbol verbatim, re-ref it, move it, and refresh all uuids."""
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
            l = f'{mm.group(1)}{round(float(mm.group(2)) + dx, 3)} ' \
                f'{round(float(mm.group(3)) + dy, 3)}{mm.group(4)}'
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
assert P['U2']['60'] == (236.22, 176.53), P['U2']['60']
assert P['U2']['49'] == (236.22, 179.07), P['U2']['49']
assert P['J3']['1'] == (384.81, 232.41), P['J3']['1']

# landing zone (150,215)-(230,270) must be empty
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
busy = [p for p in pts if 150 <= p[0] <= 230 and 215 <= p[1] <= 270]
assert not busy, f'RF landing zone not clear: {sorted(busy)[:8]}'

new = []


def pi(chain, cy, cser_ref, cshunt_a, cshunt_b, gnd_a, gnd_b):
    """Series cap between <chain> and <chain>_OUT, plus two DNP shunts to GND.

    All coordinates are exact multiples of 1.27 mm (KiCad's schematic grid);
    off-grid endpoints produce endpoint_off_grid ERC violations and can silently
    fail to connect.
    """
    SER_X, PIN_L, PIN_R = 175.26, 171.45, 179.07
    SHA_X, SHB_X = 165.1, 185.42
    out = []
    # series element - populated, also the DC block
    out += _mk.label(chain, PIN_L, cy, 180, 'right bottom')
    out += _mk.capacitor(cser_ref, '15pF', SER_X, cy, rot=90,
                         desc='RF pi series / DC block - C0G, populate in build 1')
    out += _mk.label(f'{chain}_OUT', PIN_R, cy, 0, 'left bottom')
    for x, net, ref, gnd, side in ((SHA_X, chain, cshunt_a, gnd_a, 'modem'),
                                   (SHB_X, f'{chain}_OUT', cshunt_b, gnd_b, 'connector')):
        out += _mk.label(net, x, cy + 3.81, 90, 'left bottom')
        out += _mk.capacitor(ref, 'DNP', x, cy + 7.62, dnp=True,
                             desc=f'RF pi shunt, {side} side - C0G, DNP in build 1')
        out += _mk.wire(x, cy + 11.43, x, cy + 15.24)
        out += _mk.power('power:GND', gnd, x, cy + 15.24, 'GND')
    return out


def del_no_connect(lines, x, y):
    for i, l in enumerate(lines):
        if l == '	(no_connect' and lines[i + 1].strip() == f'(at {x} {y})':
            del lines[i:i + 4]
            return True
    raise AssertionError(f'no_connect @ {x},{y} not found')


# ---- H-9: cellular main chain -------------------------------------------
relabel(L, 'ANT_MAIN', 'ANT_MAIN_OUT', 384.81, 232.41)   # J3.1 becomes the antenna side
new += pi('ANT_MAIN', 222.25, 'C31', 'C32', 'C33', '#PWR0109', '#PWR0110')

# ---- H-8: GNSS chain -----------------------------------------------------
assert del_no_connect(L, 236.22, 179.07)   # U2.49 was flagged NC
new += _mk.label('ANT_GNSS', 236.22, 179.07, 180, 'right bottom')   # onto U2.49
new += pi('ANT_GNSS', 250.19, 'C34', 'C35', 'C36', '#PWR0111', '#PWR0112')
new += clone_symbol(L, 'J3', 'J8', 205.74, 250.19)
new += _mk.label('ANT_GNSS_OUT', 205.74, 250.19, 0, 'left bottom')
new += _mk.power('power:GND', '#PWR0113', 205.74, 252.73, 'GND')

anchor, _ = se.find(L, '#PWR050')
L[anchor:anchor] = new
se.save(L)
print('added: C31/C32/C33 (ANT_MAIN pi), C34/C35/C36 (ANT_GNSS pi), J8 + GND')
print('J3.1 relabelled ANT_MAIN -> ANT_MAIN_OUT; U2.49 now labelled ANT_GNSS')

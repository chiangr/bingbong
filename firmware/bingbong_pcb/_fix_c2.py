"""C-2 (+ H-6 part 1): the ESP32 drives the R1200's CE pin to 3.3 V while Q2 holds
the R1200's VDD at 0 V. R1200 abs max on CE is VIN + 0.3 V, so with Q2 off the
limit is +0.3 V against a 3.3 V drive - current is injected through the enable
pin's ESD structure. Two independent controls (CE on IO8, supply-enable on IO18)
with nothing enforcing their order.

Fix: delete the whole external power-switch network (Q2 P-FET, Q3 NPN, R29 base
resistor, R30 gate pull-up) and use CE as the sole enable. The R1200 already does
this internally - standby current is max 3 uA at VCE = 0 and the datasheet states
the internal NPN separates output from input in standby - so the P-FET adds
nothing. Removes 4 parts, frees IO18, kills the cross-domain sneak path.

Also applies H-6 part 1: the boost input now comes from /SYS LOAD instead of
+3.3V, removing ~136 mA of double-conversion load from the 0.5 A buck.
And adds a 100k CE pull-down so the enable is deterministic at power-up
(the internal RCE is 600k-2.2M, enough to default off but high-Z next to a
1.2 MHz Lx node).
"""
import _schedit as se
import _pins
import _trace
import _mk
import re

L = se.load()

for taken in ('R35', '#PWR0107'):
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


def del_label(lines, text, x, y):
    for i, l in enumerate(lines):
        if l == f'\t(label "{text}"' and re.match(rf'\t\t\(at {x} {y} ', lines[i + 1]):
            del_block(lines, i)
            return
    raise AssertionError(f'label "{text}" @ {x},{y} not found')


P = _pins.resolve()
assert P['Q2']['3'] == (480.06, 298.45), P['Q2']
assert P['U1']['1'] == (496.57, 308.61), P['U1']

# ---- verify the landing zone for the new pull-down is clear ---------------
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
RX, RY = 478.79, 327.66
zone = [p for p in pts if RX - 6 <= p[0] <= RX + 6 and RY - 8 <= p[1] <= RY + 10]
assert not zone, f'landing zone not clear: {sorted(zone)}'

# ---- delete the external power-switch network ----------------------------
del_wire(L, 453.39, 298.45, 462.28, 298.45)   # +3.3V -> R30.1 / Q2.2
del_wire(L, 462.28, 298.45, 469.9, 298.45)    # R30.1 -> Q2 source
del_wire(L, 462.28, 290.83, 474.98, 290.83)   # R30.2 -> Q2 gate / Q3 collector
del_label(L, 'R1200 PWR EN', 490.22, 285.75)  # R29 side
del_label(L, 'R1200 PWR EN', 96.52, 177.8)    # IO18 side - frees the GPIO
for ref in ('Q2', 'Q3', 'R29', 'R30', '#PWR063', '#PWR064'):
    a, _ = se.find(L, ref)
    del_block(L, a)
    print(f'  deleted {ref}')

# ---- feed the boost from /SYS LOAD, and make CE deterministic ------------
new = []
new += _mk.label('SYS LOAD', 480.06, 298.45, 180, 'right bottom')   # old Q2 drain node
new += _mk.label('R1200 CE', RX, RY - 3.81, 90, 'left bottom')
new += _mk.resistor('R35', '100k', RX, RY)
new += _mk.wire(RX, RY + 3.81, RX, RY + 7.62)
new += _mk.power('power:GND', '#PWR0107', RX, RY + 7.62, 'GND')

anchor, _ = se.find(L, '#PWR050')
L[anchor:anchor] = new
se.save(L)
print(f'  boost input -> /SYS LOAD; R35 100k CE pull-down @({RX},{RY})')

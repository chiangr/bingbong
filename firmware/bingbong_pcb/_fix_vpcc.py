"""Two coupled changes to the MCP73871 input-current path.

(1) Invert R31 so PROG2 defaults HIGH (500 mA) instead of LOW (100 mA).
    As built, if firmware never drives IO35 the board sits at the 100 mA
    one-unit-load limit against ~460 mA demand - i.e. the C-1 defect unchanged.
    Inverting makes the fail-safe direction "works", and firmware can still pull
    IO35 low to force 100 mA. Pull-up MUST be +3.3V: IO35 is not 5V tolerant, so
    +5V or /SYS LOAD would over-stress the pin.

(2) Break VPCC away from IN and populate the datasheet Fig 3-1 divider.
    VPCC shorted to IN disables input-voltage foldback. That is safe at 100 mA
    but NOT at 500 mA: the charger would hold 500 mA into a weak supply and drag
    VBUS down until the source folds back, and the resulting droop/UVLO/restart
    oscillation browns out the ESP32 and BG95 off the shared /SYS LOAD.
    330k / 110k sets the knee at VIN ~ 4.9V (VPCC threshold 1.23V).
"""
import _schedit as se
import _pins
import _mk
import re

L = se.load()

for taken in ('R33', 'R34', 'C30', '#PWR0103', '#PWR0104', '#PWR0105', '#PWR0106'):
    try:
        se.find(L, taken)
        raise SystemExit(f'{taken} already exists')
    except KeyError:
        pass


def del_block(lines, start):
    """Delete the top-level block beginning at `start` (a '\\t(...' line)."""
    end = start
    depth = 0
    while end < len(lines):
        depth += lines[end].count('(') - lines[end].count(')')
        if depth == 0 and end > start:
            break
        end += 1
    del lines[start:end + 1]


def del_wire(lines, x1, y1, x2, y2):
    pat = f'\t\t\t(xy {x1} {y1}) (xy {x2} {y2})'
    alt = f'\t\t\t(xy {x2} {y2}) (xy {x1} {y1})'
    idx = [i for i, l in enumerate(lines) if l in (pat, alt)]
    assert len(idx) == 1, f'wire {(x1, y1, x2, y2)}: found {len(idx)}'
    del_block(lines, idx[0] - 2)


def del_label(lines, text, x, y):
    for i, l in enumerate(lines):
        if l == f'\t(label "{text}"' and re.match(rf'\t\t\(at {x} {y} ', lines[i + 1]):
            del_block(lines, i)
            return
    raise AssertionError(f'label {text} @ {x},{y} not found')


def del_symbol(lines, ref):
    a, _ = se.find(lines, ref)
    del_block(lines, a)


# ---------------------------------------------------------------- (1) R31
P = _pins.resolve()
assert P['R31'] == {'1': (336.55, 172.72), '2': (336.55, 180.34)}, P['R31']

del_label(L, 'CHG_ILIM', 336.55, 172.72)      # old: label on pin 1
del_wire(L, 336.55, 180.34, 336.55, 184.15)   # old: pin 2 -> GND
del_symbol(L, '#PWR0101')                     # old GND
print('R31: removed pull-down to GND')

new = []
new += _mk.wire(336.55, 172.72, 336.55, 168.91)               # pin 1 -> +3.3V
new += _mk.power('power:+3.3V', '#PWR0103', 336.55, 168.91, '+3.3V')
new += _mk.label('CHG_ILIM', 336.55, 180.34, 90, 'left bottom')  # pin 2 = the net

# ---------------------------------------------------------------- (2) VPCC
del_wire(L, 373.38, 181.61, 358.14, 181.61)   # VPCC <-> +5V rail
del_wire(L, 358.14, 171.45, 358.14, 181.61)   # its now-dangling feeder stub
print('VPCC: broken away from IN')

new += _mk.label('VPCC', 373.38, 181.61, 0, 'left bottom')     # onto U8.2 directly

# upper leg: +5V -> VPCC
new += _mk.power('power:+5V', '#PWR0104', 303.53, 179.07, '+5V')
new += _mk.wire(303.53, 179.07, 303.53, 182.88)
new += _mk.resistor('R33', '330k', 303.53, 186.69)
new += _mk.label('VPCC', 303.53, 190.5, 90, 'left bottom')

# lower leg: VPCC -> GND
new += _mk.label('VPCC', 311.15, 182.88, 90, 'left bottom')
new += _mk.resistor('R34', '110k', 311.15, 186.69)
new += _mk.wire(311.15, 190.5, 311.15, 194.31)
new += _mk.power('power:GND', '#PWR0105', 311.15, 194.31, 'GND')

# VPCC bypass
new += _mk.label('VPCC', 318.77, 182.88, 90, 'left bottom')
new += _mk.capacitor('C30', '100nF', 318.77, 186.69)
new += _mk.wire(318.77, 190.5, 318.77, 194.31)
new += _mk.power('power:GND', '#PWR0106', 318.77, 194.31, 'GND')

anchor, _ = se.find(L, '#PWR050')
L[anchor:anchor] = new
se.save(L)
print('added: #PWR0103 +3.3V, R33 330k, R34 110k, C30 100nF, #PWR0104/0105')

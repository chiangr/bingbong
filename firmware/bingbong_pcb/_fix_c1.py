"""C-1: MCP73871 PROG2 and SEL are BOTH strapped to GND through one shared tie
(#PWR050), which selects the USB 100 mA one-unit-load limit for system load AND
charging combined. Measured demand is ~460 mA, so the cell discharges on USB.

Fix (non-regressive): cut PROG2 away from the shared GND node, give it its own
100k pull-down (R31) so the power-on default is still the USB-compliant 100 mA,
and expose the node to firmware on a free GPIO (IO35) so it can be raised to
500 mA after enumeration. SEL stays on GND - SEL high is AC-adapter mode and
nothing on this board reads CC.
"""
import _schedit as se
import _pins
import uuid as U

L = se.load()
NET = 'CHG_ILIM'
ROOT = '/e7d26e72-3287-4d9d-b245-45d7d8c953b0'


def uid():
    return str(U.uuid4())


def label(text, x, y, rot=0, just='left bottom'):
    return ['\t(label "%s"' % text, f'\t\t(at {x} {y} {rot})', '\t\t(effects',
            '\t\t\t(font', '\t\t\t\t(size 1.27 1.27)', '\t\t\t)',
            f'\t\t\t(justify {just})', '\t\t)', f'\t\t(uuid "{uid()}")', '\t)']


def wire(x1, y1, x2, y2):
    return ['\t(wire', '\t\t(pts', f'\t\t\t(xy {x1} {y1}) (xy {x2} {y2})', '\t\t)',
            '\t\t(stroke', '\t\t\t(width 0)', '\t\t\t(type default)', '\t\t)',
            f'\t\t(uuid "{uid()}")', '\t)']


def resistor(ref, val, x, y):
    out = ['\t(symbol', '\t\t(lib_id "Device:R")', f'\t\t(at {x} {y} 0)', '\t\t(unit 1)',
           '\t\t(exclude_from_sim no)', '\t\t(in_bom yes)', '\t\t(on_board yes)',
           '\t\t(dnp no)', '\t\t(fields_autoplaced yes)', f'\t\t(uuid "{uid()}")']
    fields = [('Reference', ref, False), ('Value', val, False),
              ('Footprint', 'Resistor_SMD:R_0402_1005Metric', True),
              ('Datasheet', '~', True), ('Description', 'Resistor', True)]
    for i, (k, v, hide) in enumerate(fields):
        out += [f'\t\t(property "{k}" "{v}"', f'\t\t\t(at {x + 2.54} {y - 1.27 + i * 0.01} 90)',
                '\t\t\t(effects', '\t\t\t\t(font', '\t\t\t\t\t(size 1.27 1.27)', '\t\t\t\t)']
        if hide:
            out += ['\t\t\t\t(hide yes)']
        out += ['\t\t\t)', '\t\t)']
    out += [f'\t\t(pin "1"', f'\t\t\t(uuid "{uid()}")', '\t\t)',
            f'\t\t(pin "2"', f'\t\t\t(uuid "{uid()}")', '\t\t)',
            '\t\t(instances', '\t\t\t(project "bingbong"', f'\t\t\t\t(path "{ROOT}"',
            f'\t\t\t\t\t(reference "{ref}")', '\t\t\t\t\t(unit 1)', '\t\t\t\t)',
            '\t\t\t)', '\t\t)', '\t)']
    return out


def gnd(ref, x, y):
    out = ['\t(symbol', '\t\t(lib_id "power:GND")', f'\t\t(at {x} {y} 0)', '\t\t(unit 1)',
           '\t\t(exclude_from_sim no)', '\t\t(in_bom yes)', '\t\t(on_board yes)',
           '\t\t(dnp no)', '\t\t(fields_autoplaced yes)', f'\t\t(uuid "{uid()}")']
    for k, v, hide in [('Reference', ref, True), ('Value', 'GND', False),
                       ('Footprint', '', True), ('Datasheet', '', True),
                       ('Description', 'Power symbol creates a global label with name \\"GND\\" , ground', True)]:
        out += [f'\t\t(property "{k}" "{v}"', f'\t\t\t(at {x} {y + 6.35} 0)',
                '\t\t\t(effects', '\t\t\t\t(font', '\t\t\t\t\t(size 1.27 1.27)', '\t\t\t\t)']
        if hide:
            out += ['\t\t\t\t(hide yes)']
        out += ['\t\t\t)', '\t\t)']
    out += [f'\t\t(pin "1"', f'\t\t\t(uuid "{uid()}")', '\t\t)',
            '\t\t(instances', '\t\t\t(project "bingbong"', f'\t\t\t\t(path "{ROOT}"',
            f'\t\t\t\t\t(reference "{ref}")', '\t\t\t\t\t(unit 1)', '\t\t\t\t)',
            '\t\t\t)', '\t\t)', '\t)']
    return out


# ---- guard rails ---------------------------------------------------------
for taken in ('R31', '#PWR0101'):
    try:
        se.find(L, taken)
        raise SystemExit(f'{taken} already exists - pick another refdes')
    except KeyError:
        pass

P = _pins.resolve()
assert P['U8']['4'] == (373.38, 176.53), P['U8']['4']
assert P['U8']['3'] == (373.38, 179.07), P['U8']['3']
IO35 = P['U10']['28']
assert IO35 == (137.16, 205.74), IO35

# ---- 1. cut the PROG2 <-> SEL/GND link -----------------------------------
CUT = '\t\t\t(xy 364.49 176.53) (xy 364.49 179.07)'
idx = [i for i, l in enumerate(L) if l == CUT]
assert len(idx) == 1, f'expected exactly one cut wire, found {len(idx)}'
i = idx[0]
start = i - 2                      # '\t(wire' , '\t\t(pts'
assert L[start] == '\t(wire', L[start]
end = start
while L[end] != '\t)':
    end += 1
del L[start:end + 1]
print(f'cut PROG2<->SEL wire (was schematic lines {start + 1}-{end + 1})')

# ---- 2..4 build the new net ---------------------------------------------
RX, RY = 336.55, 176.53            # verified-clear region (330,168)-(344,186)
new = []
new += label(NET, 364.49, 176.53, 0, 'left bottom')          # on the PROG2 stub
new += resistor('R31', '100k', RX, RY)                       # pull-down, keeps 100 mA default
new += label(NET, RX, RY - 3.81, 90, 'left bottom')          # R31 pin 1 (top)
new += wire(RX, RY + 3.81, RX, RY + 7.62)                    # R31 pin 2 (bottom) -> GND
new += gnd('#PWR0101', RX, RY + 7.62)
new += wire(IO35[0], IO35[1], IO35[0] + 7.62, IO35[1])       # stub off IO35
new += label(NET, IO35[0] + 7.62, IO35[1], 0, 'left bottom')

anchor, _ = se.find(L, '#PWR050')
L[anchor:anchor] = new
se.save(L)

print(f'added: label@PROG2, R31 100k @({RX},{RY}), #PWR0101, IO35 stub + label')
print(f'net "{NET}" should now contain U8.4, R31.1, U10.28')

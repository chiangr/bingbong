"""H-5: MCP73871 CE has a 100k pull-DOWN, so charging is disabled until firmware
boots - a flat or unprogrammed unit can never recharge.

Fix: make R16 a pull-UP to /SYS LOAD (NOT +3.3V, which is generated downstream
of the charger by U6 - see LOW-6). Mechanically this means replacing the GND
power symbol #PWR052 on R16's left pin with a "SYS LOAD" local label at the
exact same coordinate, so the wire joins the SYS LOAD net instead of GND.
"""
import _schedit as se
import uuid as U

L = se.load()

TARGET = '#PWR052'
AT = (354.33, 168.91)

a, b = se.find(L, TARGET)
blk = '\n'.join(L[a:b + 1])
assert 'power:GND' in blk, 'expected a GND power symbol'
assert f'(at {AT[0]} {AT[1]}' in blk, f'symbol not at {AT}'
print(f'removing {TARGET} (power:GND) at {AT}, lines {a + 1}-{b + 1}')

label = [
    '\t(label "SYS LOAD"',
    f'\t\t(at {AT[0]} {AT[1]} 180)',
    '\t\t(effects',
    '\t\t\t(font',
    '\t\t\t\t(size 1.27 1.27)',
    '\t\t\t)',
    '\t\t\t(justify right bottom)',
    '\t\t)',
    f'\t\t(uuid "{U.uuid4()}")',
    '\t)',
]

L[a:b + 1] = label
se.save(L)
print(f'inserted SYS LOAD label at {AT} ({len(label)} lines)')

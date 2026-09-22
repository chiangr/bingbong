"""M-8 / section 3.3: the board has NO battery telemetry and NO firmware-independent
low-voltage cutoff - yet the correct sensor is already fitted and wired only to an LED.

You bought the MCP73871-2CC specifically for its 3.1 V LBO (low-battery output,
open-drain, auto-disabled on USB). U8 pin 8 (STAT1/LBO) currently goes only to
D3's cathode. Adding a 100k pull-up and routing it to a free GPIO gives firmware
a hard 3.1 V low-battery interrupt so it can shut the modem down and blank the
display before the cell reaches the pack PCM trip. The LED stays in parallel -
the open-drain pin sinks both.
"""
import _schedit as se
import _pins
import _mk

L = se.load()
NET = 'BATT_LOW'

for taken in ('R32', '#PWR0102'):
    try:
        se.find(L, taken)
        raise SystemExit(f'{taken} already exists')
    except KeyError:
        pass

P = _pins.resolve()
assert P['U8']['8'] == (408.94, 173.99), P['U8']['8']
IO36 = P['U10']['29']
assert IO36 == (137.16, 203.2), IO36

RX, RY = 323.85, 176.53            # verified-clear region (316,168)-(330,186)

new = []
# label onto the existing LBO net (corner node between U8.8 and D3.1)
new += _mk.label(NET, 415.29, 173.99, 0, 'left bottom')
# 100k pull-up: pin 1 (top) -> +3.3V, pin 2 (bottom) -> the LBO net
new += _mk.resistor('R32', '100k', RX, RY)
new += _mk.wire(RX, RY - 3.81, RX, RY - 7.62)
new += _mk.power('power:+3.3V', '#PWR0102', RX, RY - 7.62, '+3.3V')
new += _mk.label(NET, RX, RY + 3.81, 90, 'left bottom')
# route to a free GPIO
new += _mk.wire(IO36[0], IO36[1], IO36[0] + 7.62, IO36[1])
new += _mk.label(NET, IO36[0] + 7.62, IO36[1], 0, 'left bottom')

anchor, _ = se.find(L, '#PWR050')
L[anchor:anchor] = new
se.save(L)
print(f'added R32 100k pull-up @({RX},{RY}), #PWR0102 +3.3V, IO36 stub')
print(f'net "{NET}" should contain U8.8, D3.1, R32.2, U10.29')

"""H-4 remainder: insert the USB VBUS over-voltage / current-limit switch.

WHY THIS PART.  The review named AP22815AWT-7 as the primary candidate and
tagged it [SUGGESTION - thresholds unverified].  Verification kills it: the
AP22815 datasheet (DS41022 Rev 6-2, p4) gives VIN absolute maximum as
-0.3 to +6.0 V, and its OVP senses the *OUT* pin (rated 28 V), not the input.
It is a host-side port protector against a downstream device back-feeding a
USB-A socket.  In this device-side position a 12 V non-compliant charger puts
12 V onto a 6 V pin, i.e. the part is destroyed by the exact fault it was
specified to prevent.  TPD1S514 was the review's other pick on the grounds that
it "would let you delete U5" - TI's own product page confirms it carries no
D+/D- ESD, so that rationale is also void.

NCP361MUTBG (onsemi, UDFN-6 2x2) instead:
  IN abs max            21 V          survives a 12 V or 20 V charger
  OVLO      5.43 / 5.675 / 5.9 V      above USB max 5.25 V, below the
                                      MCP73871's 6 V recommended ceiling and
                                      well under its 7 V abs max
  OCP        550 / 750 / 950 mA       min trip sits above the charger's
                                      500 mA five-unit-load draw
  Imax                 600 mA DC      ~17% margin at 500 mA.  NOTE: this
                                      forecloses raising the charge current.
  Vdrop      150 typ / 200 mA max @ 500 mA
  ESD          15 kV air / 8 kV contact, needs the >=1uF input cap to hold
  TA               -40 to +85 C, MSL 1, Active (no discontinued sibling)

TOPOLOGY.  Section 3.2 requires that no branch tap VBUS upstream of the switch.
Rather than move five downstream loads, the CONNECTOR side is renamed to
`VBUS_CON` and `+5V` is retained as the PROTECTED rail - so C15 (bulk), C37
(HF bypass), R33 (VPCC divider top leg), J6.4 and U8.18/19 all stay correct
without being touched.  Only J2's VBUS pads and CR6 (the TVS, which must sit
ahead of the switch) move to VBUS_CON.

R33 staying downstream is load-bearing for a second reason the review did not
state: if the VPCC divider sensed raw VBUS, a 12 V fault would present
12 * 40.2/140.2 = 3.44 V to U8's VPCC pin while U8's VDD is held at 0 V by the
open switch - violating the MCP73871's "all inputs <= VDD+0.3 V" abs max.

EN is tied to GND (always enabled), NOT to a GPIO.  Routing it to firmware
would recreate the H-5 failure mode just fixed: a bricked or unprogrammed board
that can never recharge.

FLAG is open-drain, pulled up to +3.3V (IO34 is not 5 V tolerant) and routed to
IO34 as `USB_FAULT`.  When VBUS is absent U11 is unpowered and FLAG floats, so
R38 holds IO34 high = "no fault", which is the correct idle polarity; the
back-feed into the unpowered FLAG pin is bounded by 3.3 V / 100 k = 33 uA.

ERC: `+5V` gains a power_out driver (U11.4), clearing the power_pin_not_driven
at old #PWR026; `VBUS_CON` inherits one in its place because J2's VBUS pads and
U11.3 are power_in with no driver.  Net change zero.  The Tier-C PWR_FLAG pass
should put a flag on VBUS_CON.
"""
import re

import _mk
import _pins
import _schedit as se

FOOTPRINT = 'Package_DFN_QFN:DFN-6-1EP_2x2mm_P0.65mm_EP1.01x1.7mm'
DATASHEET = 'https://www.onsemi.com/download/data-sheet/pdf/ncp361-d.pdf'
DESC = ('USB positive over-voltage protection controller, integrated PMOS, '
        'OVLO 5.675 V typ, OCP 750 mA typ, IN abs max 21 V, UDFN-6 2x2')

# ---------------------------------------------------------------- library symbol

_PINS = [
    # (etype,          x,      y,     rot, name,       number)
    ('input',        -10.16, -2.54,   0, 'EN',       '1'),
    ('power_in',       0.00, -8.89,  90, 'GND',      '2'),
    ('power_in',     -10.16,  2.54,   0, 'IN',       '3'),
    ('power_out',     10.16,  2.54, 180, 'OUT',      '4'),
    # pin 5 is the second OUT bond; declaring it passive rather than a second
    # power_out avoids a bogus "Power output and Power output are connected"
    # pin_to_pin error when the two are hardwired, as the datasheet requires.
    ('passive',       10.16,  0.00, 180, 'OUT',      '5'),
    ('open_collector', 10.16, -2.54, 180, '~{FLAG}', '6'),
    ('power_in',      -3.81, -8.89,  90, 'PAD',      '7'),
]


def symbol_lines(indent, outer='NCP361MUTBG'):
    """The NCP361MUTBG library symbol.

    indent 1 = the .kicad_sym library file, outer name unprefixed.
    indent 2 = the schematic's lib_symbols cache, where the OUTER name carries
    the library prefix but the inner unit name does not - get this wrong and
    kicad-cli segfaults rather than reporting an error.
    """
    t = '\t' * indent
    o = []
    o += [f'{t}(symbol "{outer}"',
          f'{t}\t(pin_names', f'{t}\t\t(offset 0.254)', f'{t}\t)',
          f'{t}\t(exclude_from_sim no)', f'{t}\t(in_bom yes)', f'{t}\t(on_board yes)']
    props = [('Reference', 'U', -6.35, 6.35, False),
             ('Value', 'NCP361MUTBG', -6.35, -12.7, False),
             ('Footprint', FOOTPRINT, 0, 0, True),
             ('Datasheet', DATASHEET, 0, 0, True),
             ('Description', DESC, 0, 0, True),
             ('ki_keywords', 'OVP overvoltage protection load switch USB VBUS', 0, 0, True),
             ('ki_fp_filters', 'DFN*2x2*P0.65mm*', 0, 0, True)]
    for name, val, px, py, hide in props:
        o += [f'{t}\t(property "{name}" "{val}"',
              f'{t}\t\t(at {px} {py} 0)',
              f'{t}\t\t(effects', f'{t}\t\t\t(font', f'{t}\t\t\t\t(size 1.27 1.27)', f'{t}\t\t\t)']
        if hide:
            o += [f'{t}\t\t\t(hide yes)']
        o += [f'{t}\t\t)', f'{t}\t)']
    o += [f'{t}\t(symbol "NCP361MUTBG_0_1"',
          f'{t}\t\t(rectangle',
          f'{t}\t\t\t(start -6.35 5.08)', f'{t}\t\t\t(end 6.35 -5.08)',
          f'{t}\t\t\t(stroke', f'{t}\t\t\t\t(width 0.254)', f'{t}\t\t\t\t(type default)', f'{t}\t\t\t)',
          f'{t}\t\t\t(fill', f'{t}\t\t\t\t(type background)', f'{t}\t\t\t)',
          f'{t}\t\t)']
    for etype, px, py, rot, name, num in _PINS:
        o += [f'{t}\t\t(pin {etype} line',
              f'{t}\t\t\t(at {px} {py} {rot})', f'{t}\t\t\t(length 3.81)',
              f'{t}\t\t\t(name "{name}"',
              f'{t}\t\t\t\t(effects', f'{t}\t\t\t\t\t(font', f'{t}\t\t\t\t\t\t(size 1.27 1.27)',
              f'{t}\t\t\t\t\t)', f'{t}\t\t\t\t)', f'{t}\t\t\t)',
              f'{t}\t\t\t(number "{num}"',
              f'{t}\t\t\t\t(effects', f'{t}\t\t\t\t\t(font', f'{t}\t\t\t\t\t\t(size 1.27 1.27)',
              f'{t}\t\t\t\t\t)', f'{t}\t\t\t\t)', f'{t}\t\t\t)',
              f'{t}\t\t)']
    o += [f'{t}\t)', f'{t}\t(embedded_fonts no)', f'{t})']
    return o


# ---------------------------------------------------------------- edit helpers

def del_block(lines, start):
    end, depth = start, 0
    while end < len(lines):
        depth += lines[end].count('(') - lines[end].count(')')
        if depth == 0 and end > start:
            break
        end += 1
    del lines[start:end + 1]


def del_symbol(lines, ref):
    a, _ = se.find(lines, ref)
    del_block(lines, a)


def main():
    # ------------------------------------------------------- 1. library symbol
    lib = 'Bingbong_library.kicad_sym'
    txt = open(lib, encoding='utf-8').read()
    if 'NCP361MUTBG' in txt:
        raise SystemExit('NCP361MUTBG already in the library')
    lines = txt.split('\n')
    while lines and not lines[-1].strip():
        lines.pop()
    assert lines[-1] == ')', repr(lines[-1])
    lines[-1:-1] = symbol_lines(1)
    open(lib, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('library: added NCP361MUTBG')

    # ------------------------------------------------------- 2. schematic
    L = se.load()
    for taken in ('U11', 'C44', 'R38'):
        try:
            se.find(L, taken)
            raise SystemExit(f'{taken} already exists')
        except KeyError:
            pass

    # cached copy in lib_symbols, or "Update Symbols from Library" reverts it
    for i, l in enumerate(L):
        if l == '\t(lib_symbols':
            L[i + 1:i + 1] = symbol_lines(2, 'Bingbong_library:NCP361MUTBG')
            break
    else:
        raise SystemExit('no lib_symbols block')
    print('schematic: cached NCP361MUTBG in lib_symbols')

    P = _pins.resolve()
    assert P['J2']['A4'] == (306.07, 81.28), P['J2']['A4']
    assert P['CR6']['1'] == (200.66, 285.75), P['CR6']['1']
    assert P['U10']['25'] == (137.16, 213.36), P['U10']['25']

    # --- split the rail: connector side becomes VBUS_CON
    del_symbol(L, '#PWR026')     # +5V on J2's VBUS bus
    del_symbol(L, '#PWR0116')    # +5V on CR6 (TVS stays ahead of the switch)
    print('rail split: J2 VBUS + CR6 detached from +5V')

    new = []
    new += _mk.label('VBUS_CON', 298.45, 81.28, 0, 'left bottom')
    new += _mk.label('VBUS_CON', 200.66, 281.94, 0, 'left bottom')

    # --- U11 and its input cap on VBUS_CON
    new += _mk._sym('Bingbong_library:NCP361MUTBG', 'U11', 264.16, 88.9, [
        ('Reference', 'U11', False), ('Value', 'NCP361MUTBG', False),
        ('Footprint', FOOTPRINT, True), ('Datasheet', DATASHEET, True),
        ('Description', DESC, True)], 7)
    new += _mk.label('VBUS_CON', 254.0, 86.36, 0, 'left bottom')
    new += _mk.wire(247.65, 86.36, 254.0, 86.36)
    new += _mk.capacitor('C44', '1uF', 247.65, 90.17,
                         desc='NCP361 input bypass - datasheet requires >=1uF low-ESR '
                              'at IN; also the ESD rating is conditional on it')
    new += _mk.power('power:GND', '#PWR0124', 247.65, 93.98, 'GND')

    # --- protected rail out of the switch
    new += _mk.wire(274.32, 86.36, 274.32, 88.9)    # OUT(4) + OUT(5) hardwired
    new += _mk.wire(274.32, 86.36, 274.32, 83.82)
    new += _mk.power('power:+5V', '#PWR0120', 274.32, 83.82, '+5V')

    # --- EN low = enabled, permanently
    new += _mk.wire(254.0, 91.44, 254.0, 95.25)
    new += _mk.power('power:GND', '#PWR0121', 254.0, 95.25, 'GND')

    # --- grounds
    new += _mk.power('power:GND', '#PWR0122', 264.16, 97.79, 'GND')
    new += _mk.wire(260.35, 97.79, 260.35, 101.6)
    new += _mk.power('power:GND', '#PWR0123', 260.35, 101.6, 'GND')

    # --- FLAG -> pull-up -> IO34
    new += _mk.label('USB_FAULT', 274.32, 91.44, 0, 'left bottom')
    new += _mk.wire(274.32, 91.44, 283.21, 91.44)
    new += _mk.wire(283.21, 91.44, 283.21, 88.9)
    new += _mk.resistor('R38', '100k', 283.21, 85.09)
    new += _mk.wire(283.21, 81.28, 283.21, 77.47)
    new += _mk.power('power:+3.3V', '#PWR0125', 283.21, 77.47, '+3.3V')

    new += _mk.wire(137.16, 213.36, 144.78, 213.36)
    new += _mk.label('USB_FAULT', 144.78, 213.36, 0, 'left bottom')

    anchor, _ = se.find(L, 'CR6')
    L[anchor:anchor] = new
    se.save(L)

    L = se.load()
    se.set_prop(L, 'C44', 'Footprint', 'Capacitor_SMD:C_0603_1608Metric')
    se.save(L)
    print('added: U11 NCP361MUTBG, C44 1uF 0603, R38 100k, '
          '#PWR0120..0125, nets VBUS_CON + USB_FAULT')


if __name__ == '__main__':
    main()

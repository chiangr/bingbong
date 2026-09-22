"""Dump every component with its value, footprint and per-pin net.

Usage: _sysmap.py <netlist.xml> [ref ...]
"""
import sys
import xml.etree.ElementTree as ET

r = ET.parse(sys.argv[1]).getroot()
want = set(sys.argv[2:])

pin2net = {}
for n in r.find('nets'):
    for x in n:
        pin2net[(x.get('ref'), x.get('pin'))] = n.get('name')

libparts = {}
for lp in r.find('libparts'):
    key = (lp.get('lib'), lp.get('part'))
    pins = {}
    pl = lp.find('pins')
    if pl is not None:
        for p in pl:
            pins[p.get('num')] = (p.get('name'), p.get('type'))
    libparts[key] = pins

for c in sorted(r.find('components'), key=lambda c: c.get('ref')):
    ref = c.get('ref')
    if want and ref not in want:
        continue

    def txt(tag):
        e = c.find(tag)
        return e.text if e is not None and e.text else ''
    ls = c.find('libsource')
    key = (ls.get('lib'), ls.get('part')) if ls is not None else None
    pins = libparts.get(key, {})
    dnp = ' [DNP]' if c.find('property[@name="dnp"]') is not None else ''
    print('%-6s %-28s %-44s%s' % (ref, txt('value'), txt('footprint'), dnp))
    d = txt('description')
    if d:
        print('       desc: %s' % d)
    for num in sorted(pins, key=lambda s: (len(s), s)):
        name, ptype = pins[num]
        net = pin2net.get((ref, num), '<none>')
        print('       pin %-4s %-14s %-16s -> %s' % (num, name, ptype, net))
    print()

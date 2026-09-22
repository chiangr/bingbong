"""Diff two kicadxml netlists by net membership. Usage: _netdiff.py before after"""
import sys
import xml.etree.ElementTree as ET


def load(p):
    r = ET.parse(p).getroot()
    nets = {}
    for n in r.find('nets'):
        nets[n.get('name')] = {'%s.%s' % (x.get('ref'), x.get('pin')) for x in n}
    comps = {c.get('ref') for c in r.find('components')}
    return nets, comps


a, ca = load(sys.argv[1])
b, cb = load(sys.argv[2])

print('components: %d -> %d   added=%s  removed=%s'
      % (len(ca), len(cb), sorted(cb - ca), sorted(ca - cb)))
print('nets:       %d -> %d' % (len(a), len(b)))

for name in sorted(set(a) | set(b)):
    if name not in a:
        print('  + NET %-24s %s' % (name, sorted(b[name])))
    elif name not in b:
        print('  - NET %-24s %s' % (name, sorted(a[name])))
    elif a[name] != b[name]:
        print('  ~ NET %-24s  added=%s removed=%s'
              % (name, sorted(b[name] - a[name]), sorted(a[name] - b[name])))

import sys
sys.path.insert(0, r'C:/Users/chian/Desktop/bingbong_software/bingbong_pcb')
from _fp import parse, walk

fn = sys.argv[1]
want = sys.argv[2:]
s = open(fn, encoding='utf-8').read()
tree = parse(s)[0]

for sym in tree:
    if isinstance(sym, list) and sym[0] == 'symbol' and isinstance(sym[1], str):
        name = sym[1]
        if want and not any(w.lower() in name.lower() for w in want):
            continue
        print('==== SYMBOL', name)
        props = {}
        for p in walk(sym, 'property'):
            if isinstance(p[1], str) and isinstance(p[2], str):
                props[p[1]] = p[2]
        for k in ['Value', 'Footprint', 'Datasheet', 'Description', 'MPN', 'Manufacturer_Part_Number']:
            if k in props:
                print('   %s = %s' % (k, props[k]))
        pins = []
        for pin in walk(sym, 'pin'):
            etype = pin[1] if isinstance(pin[1], str) else '?'
            shape = pin[2] if isinstance(pin[2], str) else '?'
            at = None; nm = None; num = None
            for c in pin:
                if isinstance(c, list):
                    if c[0] == 'at':
                        at = (float(c[1]), float(c[2]), float(c[3]) if len(c) > 3 else 0)
                    elif c[0] == 'name':
                        nm = c[1]
                    elif c[0] == 'number':
                        num = c[1]
            pins.append((num, nm, etype, at))
        def k(t):
            try:
                return (0, int(t[0]))
            except Exception:
                return (1, str(t[0]))
        pins.sort(key=k)
        for p in pins:
            print('   pin %-5s %-16s %-14s at=%s' % (p[0], p[1], p[2], p[3]))

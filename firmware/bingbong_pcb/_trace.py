"""Flood-fill the wire graph from a point and report everything it touches."""
import re, io, math, sys
import _pins

TOL = 0.05


def key(x, y):
    return (round(x, 2), round(y, 2))


def build(path='bingbong.kicad_sch'):
    L = io.open(path, encoding='utf-8').read().split('\n')
    wires = []
    for i, l in enumerate(L):
        m = re.match(r'\t\t\t\(xy ([-\d.]+) ([-\d.]+)\) \(xy ([-\d.]+) ([-\d.]+)\)', l)
        if m:
            x1, y1, x2, y2 = map(float, m.groups())
            wires.append((i + 1, key(x1, y1), key(x2, y2)))

    labels = []           # (text, (x,y), kind, line)
    for i, l in enumerate(L):
        m = re.match(r'\t\((label|global_label|hierarchical_label) "([^"]*)"', l)
        if m:
            p = re.match(r'\t\t\(at ([-\d.]+) ([-\d.]+)', L[i + 1])
            if p:
                labels.append((m.group(2), key(float(p.group(1)), float(p.group(2))),
                               m.group(1), i + 1))

    pins = {}             # (x,y) -> [ref.pin]
    for ref, pd in _pins.resolve(path).items():
        for num, (x, y) in pd.items():
            pins.setdefault(key(x, y), []).append(f'{ref}.{num}')

    return L, wires, labels, pins


def flood(start, wires):
    seen = {start}
    stack = [start]
    used = []
    while stack:
        p = stack.pop()
        for ln, a, b in wires:
            if a == p and b not in seen:
                seen.add(b); stack.append(b); used.append(ln)
            elif b == p and a not in seen:
                seen.add(a); stack.append(a); used.append(ln)
    return seen, used


if __name__ == '__main__':
    L, wires, labels, pins = build()
    ref, pin = sys.argv[1].split('.')
    P = _pins.resolve()
    start = key(*P[ref][pin])
    seen, used = flood(start, wires)
    print(f'{sys.argv[1]} at {start}: {len(seen)} nodes, {len(used)} wire segs')
    print('  pins  :', sorted({p for k in seen for p in pins.get(k, [])}))
    print('  labels:', sorted({(t, k, kind) for t, k, kind, _ in labels if k in seen}))

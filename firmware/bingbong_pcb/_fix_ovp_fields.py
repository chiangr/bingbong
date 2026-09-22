"""Move U11's Reference/Value text off the symbol body.

_mk._sym places every field at (x+2.54, y-1.27) rotated 90, which is fine for a
two-pin passive but lands on top of the body of a 7-pin IC. Cosmetic only - no
connectivity is touched.
"""
import re

import _schedit as se

PLACE = {'Reference': (264.16, 81.28), 'Value': (264.16, 78.74)}


def main():
    L = se.load()
    a, b = se.find(L, 'U11')
    moved = []
    for i in range(a, b + 1):
        m = re.match(r'\t\t\(property "(Reference|Value)" ', L[i])
        if not m:
            continue
        name = m.group(1)
        x, y = PLACE[name]
        assert re.match(r'\t\t\t\(at ', L[i + 1]), L[i + 1]
        L[i + 1] = f'\t\t\t(at {x} {y} 0)'
        moved.append(name)
    assert sorted(moved) == ['Reference', 'Value'], moved
    se.save(L)
    print('U11: moved', ', '.join(moved), 'clear of the body')


if __name__ == '__main__':
    main()

import zlib, re, sys


def streams(path):
    d = open(path, 'rb').read()
    out = []
    for m in re.finditer(rb'stream\r?\n', d):
        s = m.end()
        e = d.find(b'endstream', s)
        try:
            out.append(zlib.decompress(d[s:e]))
        except Exception:
            out.append(None)
    return out


def paths(data, xlo, xhi, ylo, yhi):
    t = data.decode('latin-1')
    toks = re.findall(r"(-?\d+\.?\d*)|([A-Za-z*'\"]+)", t)
    stack = []
    cur = None
    segs = []
    for num, op in toks:
        if num:
            stack.append(float(num))
            continue
        if op == 'm' and len(stack) >= 2:
            cur = (stack[-2], stack[-1])
        elif op == 'l' and len(stack) >= 2:
            p = (stack[-2], stack[-1])
            if cur:
                segs.append((cur, p))
            cur = p
        elif op == 're' and len(stack) >= 4:
            x, y, w, h = stack[-4:]
            segs.append((('RECT', x, y), (w, h)))
        elif op in ('c', 'v', 'y') and len(stack) >= 2:
            cur = (stack[-2], stack[-1])
        stack = []
    out = []
    for a, b in segs:
        if a[0] == 'RECT':
            x, y = a[1], a[2]
            if xlo <= x <= xhi and ylo <= y <= yhi:
                out.append('rect x=%.1f y=%.1f w=%.1f h=%.1f' % (x, y, b[0], b[1]))
        else:
            if (xlo <= a[0] <= xhi and ylo <= a[1] <= yhi) or (xlo <= b[0] <= xhi and ylo <= b[1] <= yhi):
                out.append('line (%.1f,%.1f)-(%.1f,%.1f)' % (a[0], a[1], b[0], b[1]))
    return out


if __name__ == '__main__':
    path = sys.argv[1]
    idx = int(sys.argv[2])
    xlo, xhi, ylo, yhi = [float(v) for v in sys.argv[3:7]]
    st = streams(path)[idx]
    for l in paths(st, xlo, xhi, ylo, yhi):
        print(l)

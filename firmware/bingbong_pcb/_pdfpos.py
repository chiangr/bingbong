"""Position-aware-ish PDF text extractor: emits text runs in stream order with
the most recent Td/TD/Tm translation, so pinout diagrams can be reconstructed."""
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
            pass
    return out


TOK = re.compile(
    r"(?P<str>\((?:[^()\\]|\\.)*\))|"
    r"(?P<arr>\[(?:[^\[\]\\]|\\.)*\])|"
    r"(?P<num>-?\d+\.?\d*)|"
    r"(?P<op>[A-Za-z'\"*]+)"
)


def unesc(s):
    return re.sub(r"\\(.)", lambda m: {'n': '\n', 'r': '', 't': ' '}.get(m.group(1), m.group(1)), s)


def runs(data):
    txt = data.decode('latin-1')
    stack = []
    x = y = 0.0
    tx = ty = 0.0
    out = []
    for m in TOK.finditer(txt):
        if m.group('num'):
            stack.append(float(m.group('num')))
            continue
        if m.group('str'):
            stack.append(('S', unesc(m.group('str')[1:-1])))
            continue
        if m.group('arr'):
            parts = re.findall(r"\(((?:[^()\\]|\\.)*)\)", m.group('arr'))
            stack.append(('S', ''.join(unesc(p) for p in parts)))
            continue
        op = m.group('op')
        if op == 'Tm' and len(stack) >= 6:
            x, y = stack[-2], stack[-1]
            tx, ty = x, y
        elif op in ('Td', 'TD') and len(stack) >= 2:
            try:
                tx += stack[-2]
                ty += stack[-1]
                x, y = tx, ty
            except Exception:
                pass
        elif op == 'BT':
            tx = ty = 0.0
        elif op in ('Tj', 'TJ', "'", '"'):
            for it in stack:
                if isinstance(it, tuple):
                    if it[1].strip():
                        out.append((round(x, 1), round(y, 1), it[1]))
        stack = [] if op else stack
        if op:
            stack = []
    return out


if __name__ == '__main__':
    path = sys.argv[1]
    allruns = []
    for i, st in enumerate(streams(path)):
        r = runs(st)
        if r:
            allruns.append((i, r))
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        for i, r in allruns:
            f.write('\n===== STREAM %d =====\n' % i)
            # group by y
            r2 = sorted(r, key=lambda t: (-t[1], t[0]))
            liney = None
            line = []
            for xx, yy, s in r2:
                if liney is None or abs(yy - liney) > 2:
                    if line:
                        f.write(' | '.join(line) + '\n')
                    line = []
                    liney = yy
                line.append('%.0f,%.0f:%s' % (xx, yy, s))
            if line:
                f.write(' | '.join(line) + '\n')
    print('wrote', sys.argv[2])

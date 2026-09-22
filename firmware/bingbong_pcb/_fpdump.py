import re, sys, os

BS = chr(92)

def toks(s):
    out = []; i = 0; n = len(s)
    while i < n:
        c = s[i]
        if c in '()':
            out.append(c); i += 1
        elif c == '"':
            j = i + 1; buf = ''
            while j < n:
                if s[j] == BS:
                    buf += s[j+1]; j += 2
                elif s[j] == '"':
                    break
                else:
                    buf += s[j]; j += 1
            out.append(('STR', buf)); i = j + 1
        elif c.isspace():
            i += 1
        else:
            j = i
            while j < n and not s[j].isspace() and s[j] not in '()"':
                j += 1
            out.append(('ATOM', s[i:j])); i = j
    return out

def parse(tk):
    def helper(i):
        assert tk[i] == '('
        i += 1; node = []
        while tk[i] != ')':
            if tk[i] == '(':
                sub, i = helper(i); node.append(sub)
            else:
                node.append(tk[i][1]); i += 1
        return node, i + 1
    node, _ = helper(0)
    return node

def find_all(node, name):
    res = []
    if isinstance(node, list):
        if node and node[0] == name:
            res.append(node)
        for c in node:
            if isinstance(c, list):
                res.extend(find_all(c, name))
    return res

for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    tree = parse(toks(s))
    print('=' * 100)
    print('FOOTPRINT FILE:', os.path.basename(f))
    pads = find_all(tree, 'pad')
    print(' pad count:', len(pads))
    rows = []
    for p in pads:
        num = p[1]; typ = p[2]; shape = p[3]
        at = None; size = None; layers = None
        for c in p[4:]:
            if isinstance(c, list):
                if c[0] == 'at': at = c[1:]
                elif c[0] == 'size': size = c[1:]
                elif c[0] == 'layers': layers = c[1:]
        rows.append((num, typ, shape, at, size, layers))
    def key(r):
        try:
            return (float(r[3][1]), float(r[3][0]))
        except Exception:
            return (0.0, 0.0)
    for r in sorted(rows, key=key):
        print('   pad %6s  %-14.14s %-10.10s at=%s size=%s layers=%s' % (str(r[0]), r[1], r[2], r[3], r[4], r[5]))

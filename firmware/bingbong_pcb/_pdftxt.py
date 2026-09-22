import zlib, re, sys

def extract(path):
    d = open(path, 'rb').read()
    out = []
    for m in re.finditer(rb'stream\r?\n', d):
        s = m.end()
        e = d.find(b'endstream', s)
        try:
            out.append(zlib.decompress(d[s:e]))
        except Exception:
            pass
    raw = b'\n'.join(out).decode('latin-1')
    pat = re.compile(r"\(((?:[^()\\]|\\.)*)\)\s*Tj")
    words = []
    for mm in pat.finditer(raw):
        s = mm.group(1)
        s = re.sub(r"\\(.)", r"\1", s)
        words.append(s)
    # also TJ arrays
    pat2 = re.compile(r"\[(.*?)\]\s*TJ", re.S)
    for mm in pat2.finditer(raw):
        parts = re.findall(r"\(((?:[^()\\]|\\.)*)\)", mm.group(1))
        words.append(''.join(re.sub(r"\\(.)", r"\1", p) for p in parts))
    return ' '.join(words)

if __name__ == '__main__':
    t = extract(sys.argv[1])
    open(sys.argv[2], 'w', encoding='utf-8').write(t)
    if len(sys.argv) > 3:
        needle = sys.argv[3]
        for m in re.finditer(re.escape(needle), t):
            print('...', t[max(0, m.start()-300):m.start()+500], '...')
            print('-----')
    else:
        print(t[:4000])

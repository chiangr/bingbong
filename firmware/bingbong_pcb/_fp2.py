import sys, re
sys.path.insert(0, r'C:/Users/chian/Desktop/bingbong_software/bingbong_pcb')
from _fp import parse, walk, getpads

fn = sys.argv[1]
s = open(fn, encoding='utf-8').read()
tree = parse(s)[0]

def layerof(node):
    for c in node:
        if isinstance(c, list) and c[0] == 'layer':
            return c[1]
        if isinstance(c, list) and c[0] == 'layers':
            return ' '.join(c[1:])
    return None

shapes = {}
for tag in ['fp_circle', 'fp_poly', 'fp_rect', 'fp_line']:
    for node in walk(tree, tag):
        L = layerof(node)
        if L and 'Paste' in L or (L and 'Mask' in L):
            ctr = None
            if tag == 'fp_circle':
                for c in node:
                    if isinstance(c, list) and c[0] == 'center':
                        ctr = (float(c[1]), float(c[2]))
            elif tag in ('fp_poly', 'fp_rect'):
                pts = []
                for c in node:
                    if isinstance(c, list) and c[0] == 'pts':
                        for p in c[1:]:
                            pts.append((float(p[1]), float(p[2])))
                    if isinstance(c, list) and c[0] == 'start':
                        pts.append((float(c[1]), float(c[2])))
                    if isinstance(c, list) and c[0] == 'end':
                        pts.append((float(c[1]), float(c[2])))
                if pts:
                    ctr = (round(sum(p[0] for p in pts)/len(pts), 4), round(sum(p[1] for p in pts)/len(pts), 4))
            shapes.setdefault((tag, L), []).append(ctr)

for k, v in shapes.items():
    print(k, 'count=', len(v))

tree2, pads = getpads(fn)
padctr = {(round(p['at'][0], 3), round(p['at'][1], 3)): p['num'] for p in pads if p['at']}

for k, v in shapes.items():
    if 'Paste' in k[1] or 'Mask' in k[1]:
        matched = set()
        unmatched = []
        for c in v:
            if c is None:
                continue
            key = (round(c[0], 3), round(c[1], 3))
            if key in padctr:
                matched.add(padctr[key])
            else:
                unmatched.append(c)
        print(k, 'matched pads:', len(matched), 'unmatched shapes:', len(unmatched), unmatched[:6])
        missing = [p['num'] for p in pads if p['at'] and (round(p['at'][0], 3), round(p['at'][1], 3)) not in
                   set((round(c[0], 3), round(c[1], 3)) for c in v if c)]
        print('   pads with NO shape at their center:', missing)

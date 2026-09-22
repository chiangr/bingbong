"""Canonical net dump for before/after diffing schematic edits."""
import re, sys, io

path = sys.argv[1]
x = io.open(path, encoding='utf-8').read()
out = []
for m in re.finditer(r'<net code="\d+" name="([^"]*)"[^>]*>(.*?)</net>', x, re.S):
    name, body = m.group(1), m.group(2)
    nodes = sorted(f'{r}.{p}' for r, p in re.findall(r'ref="(\w+)" pin="(\w+)"', body))
    if name.startswith('unconnected-'):
        name = 'UNCONNECTED'
    out.append(f'{name}\t{" ".join(nodes)}')

# also record component values so value edits show up
for m in re.finditer(r'<comp ref="(\w+)">(.*?)</comp>', x, re.S):
    ref, b = m.group(1), m.group(2)
    v = re.search(r'<value>([^<]*)</value>', b)
    out.append(f'#COMP {ref}\t{v.group(1) if v else ""}')

io.open(sys.argv[2], 'w', encoding='utf-8', newline='\n').write('\n'.join(sorted(out)) + '\n')
print(f'{path} -> {sys.argv[2]}: {len(out)} lines')

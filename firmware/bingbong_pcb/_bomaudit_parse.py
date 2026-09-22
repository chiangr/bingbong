import io, json

path = r"C:/Users/chian/Desktop/bingbong_software/bingbong_pcb/bingbong.kicad_sch"
s = io.open(path, encoding='utf-8').read()

BS = chr(92)

def parse(txt):
    i = 0
    n = len(txt)
    stack = []
    cur = None
    root = []
    while i < n:
        c = txt[i]
        if c == '(':
            new = []
            if cur is None:
                root.append(new)
            else:
                cur.append(new)
            stack.append(cur)
            cur = new
            i += 1
        elif c == ')':
            cur = stack.pop()
            i += 1
        elif c == '"':
            j = i + 1
            buf = []
            while j < n:
                if txt[j] == BS:
                    buf.append(txt[j + 1]); j += 2
                elif txt[j] == '"':
                    break
                else:
                    buf.append(txt[j]); j += 1
            cur.append(('str', ''.join(buf)))
            i = j + 1
        elif c in ' \t\r\n':
            i += 1
        else:
            j = i
            while j < n and txt[j] not in ' \t\r\n()"':
                j += 1
            cur.append(('sym', txt[i:j]))
            i = j
    return root

root = parse(s)
top = root[0]


def name(node):
    if isinstance(node, list) and node and isinstance(node[0], tuple):
        return node[0][1]
    return None


def val(x):
    return x[1] if isinstance(x, tuple) else None


def walk(node, out, depth=0):
    if not isinstance(node, list):
        return
    if name(node) == 'symbol':
        out.append(node)
        return  # do not recurse into a placed symbol
    for c in node:
        if isinstance(c, list):
            walk(c, out, depth + 1)


# lib_symbols section holds definitions; skip it
body = [c for c in top if not (isinstance(c, list) and name(c) == 'lib_symbols')]
syms = []
for c in body:
    walk(c, syms)

results = []
for sy in syms:
    props = {}
    libid = None
    dnp = False
    in_bom = True
    unit = None
    uuid = None
    for c in sy:
        if isinstance(c, list):
            nm = name(c)
            if nm == 'property':
                k = val(c[1]); v = val(c[2])
                props[k] = v
            elif nm == 'lib_id':
                libid = val(c[1])
            elif nm == 'dnp':
                dnp = (val(c[1]) == 'yes')
            elif nm == 'in_bom':
                in_bom = (val(c[1]) == 'yes')
            elif nm == 'unit':
                unit = val(c[1])
            elif nm == 'uuid':
                uuid = val(c[1])
    if 'Reference' not in props:
        continue
    results.append(dict(ref=props.get('Reference'), value=props.get('Value'),
                        fp=props.get('Footprint'), libid=libid, dnp=dnp,
                        in_bom=in_bom, unit=unit, uuid=uuid, props=props))

json.dump(results, open(r"C:/Users/chian/Desktop/bingbong_software/bingbong_pcb/_bomaudit_syms.json", 'w'), indent=1)
print("symbol instances:", len(results))

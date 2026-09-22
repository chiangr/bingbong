import re, io, json, collections

base = r"C:/Users/chian/Desktop/bingbong_software/bingbong_pcb/"
s = io.open(base + "bingbong.kicad_pcb", encoding='utf-8').read()

starts = [m.start() for m in re.finditer(r'\n\t\(footprint "', s)]
starts.append(len(s))
fps = [s[starts[i]:starts[i + 1]] for i in range(len(starts) - 1)]
print("footprint blocks:", len(fps))

rows = []
for b in fps:
    ml = re.search(r'\(footprint "([^"]*)"', b)
    lib = ml.group(1) or '<UNNAMED>'
    lay = re.search(r'\n\t\t\(layer "([^"]+)"', b)
    ref = re.search(r'\(property "Reference" "([^"]*)"', b)
    val = re.search(r'\(property "Value" "([^"]*)"', b)
    dnp = re.search(r'\n\t\t\(dnp\b', b) is not None
    ebp = re.search(r'exclude_from_bom', b) is not None
    rows.append((ref.group(1) if ref else '?', lay.group(1) if lay else '?', lib,
                 val.group(1) if val else '', dnp, ebp))

print("sides:", dict(collections.Counter(r[1] for r in rows)))
print()
print("=== BOTTOM-side placements ===")
bot = [r for r in rows if r[1] != 'F.Cu']
for r in bot:
    print("  ", r[0], "|", r[2], "|", r[3])
if not bot:
    print("   (none)")

print()
print("PCB dnp flags:", sorted(r[0] for r in rows if r[4]))
print("PCB exclude_from_bom:", sorted(r[0] for r in rows if r[5]))

syms = json.load(open(base + "_bomaudit_syms.json"))
real = set(x['ref'] for x in syms if not (x['libid'] or '').startswith('power:'))
pcbrefs = [r[0] for r in rows]
pcbset = set(pcbrefs)
print()
print("PCB refdes count:", len(pcbrefs), "distinct:", len(pcbset))
print("dup on PCB:", [k for k, v in collections.Counter(pcbrefs).items() if v > 1])
print()
print("=== in SCH/BOM but NOT PLACED on PCB (", len(real - pcbset), ") ===")
print(sorted(real - pcbset))
print()
print("=== on PCB but not in SCH ===")
for r in rows:
    if r[0] not in real:
        print("  ", r[0], "|", r[2], "|", r[3], "| layer", r[1])

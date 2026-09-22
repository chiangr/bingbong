import json, csv, io, re, collections

base = r"C:/Users/chian/Desktop/bingbong_software/bingbong_pcb/"
syms = json.load(open(base + "_bomaudit_syms.json"))

# classify
power = [s for s in syms if (s['libid'] or '').startswith('power:')]
real = [s for s in syms if not (s['libid'] or '').startswith('power:')]

print("total placed symbols:", len(syms))
print("power symbols:", len(power))
print("non-power:", len(real))

byref = collections.defaultdict(list)
for s in real:
    byref[s['ref']].append(s)

print("distinct non-power refdes:", len(byref))

# refs with multiple units
multi = {k: v for k, v in byref.items() if len(v) > 1}
print("refdes with >1 placement (multi-unit or duplicate):")
for k, v in sorted(multi.items()):
    print("  ", k, len(v), [x['unit'] for x in v], set(x['value'] for x in v), set(x['fp'] for x in v))

# graphic/no-footprint items
nofp = [s for s in real if not s['fp']]
print()
print("non-power symbols with EMPTY footprint:", len(nofp))
for s in nofp:
    print("  ", s['ref'], s['libid'], repr(s['value']))

# in_bom no
notbom = [s for s in real if not s['in_bom']]
print()
print("non-power symbols with in_bom=no:", sorted(set(s['ref'] for s in notbom)))

# dnp
dnp = sorted(set(s['ref'] for s in real if s['dnp']))
print("schematic dnp=yes refs:", dnp)

print()
print("=== ALL NON-POWER REFDES ===")
def keyf(r):
    m = re.match(r'([A-Za-z#]+)(\d*)', r)
    return (m.group(1), int(m.group(2) or 0))
for r in sorted(byref, key=keyf):
    s = byref[r][0]
    print(f"{r:6s} {str(s['value'])[:28]:30s} {str(s['fp'])[:60]:62s} dnp={s['dnp']} bom={s['in_bom']} lib={s['libid']}")

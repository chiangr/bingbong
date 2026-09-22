import json, csv, io, re, collections

base = r"C:/Users/chian/Desktop/bingbong_software/bingbong_pcb/"
syms = json.load(open(base + "_bomaudit_syms.json"))
real = [s for s in syms if not (s['libid'] or '').startswith('power:')]
schmap = {s['ref']: s for s in real}

rows = list(csv.DictReader(io.open(base + "BOM_2026-09-04.csv", encoding='utf-8-sig')))
print("BOM data rows:", len(rows))

bomrefs = []
for r in rows:
    refs = [x.strip() for x in r['Refs'].split(',') if x.strip()]
    bomrefs.extend(refs)

print("BOM refdes total (with dups):", len(bomrefs))
dups = [k for k, v in collections.Counter(bomrefs).items() if v > 1]
print("duplicate refdes in BOM:", dups)

sset = set(schmap)
bset = set(bomrefs)
print("in sch not in BOM:", sorted(sset - bset))
print("in BOM not in sch:", sorted(bset - sset))
print("sch count", len(sset), "bom distinct", len(bset))

deleted = ['C12', 'C19', 'C20', 'Q2', 'Q3', 'U7', 'R10', 'R29', 'R30']
print()
print("=== deleted-part check ===")
for d in deleted:
    print(f"  {d}: in schematic={d in sset}  in BOM Refs={d in bset}")
# search deleted MPNs anywhere in BOM text
raw = io.open(base + "BOM_2026-09-04.csv", encoding='utf-8-sig').read()
for mpn in ['JMK105BJ105KV-F', 'CL05A104KA5NNNC', 'GRM158R60J226ME01D', 'FDN338P', 'SS8050', 'MIC5504']:
    print(f"  MPN '{mpn}' appears in BOM text: {mpn in raw}")

print()
print("=== qty check ===")
tot_qty = 0
for r in rows:
    refs = [x.strip() for x in r['Refs'].split(',') if x.strip()]
    q = int(float(r['Qty']))
    tot_qty += q
    if q != len(refs):
        print(f"  QTY MISMATCH {r['Refs'][:40]}: Qty={q} refcount={len(refs)}")
print("sum of Qty column:", tot_qty)

dnprows = [r for r in rows if r['DNP'].strip()]
dnpbomrefs = []
for r in dnprows:
    dnpbomrefs.extend([x.strip() for x in r['Refs'].split(',')])
print()
print("BOM DNP-marked refs:", sorted(dnpbomrefs))
schdnp = sorted(s['ref'] for s in real if s['dnp'])
print("SCH dnp=yes refs   :", schdnp)
print("DNP in sch but not flagged in BOM:", sorted(set(schdnp) - set(dnpbomrefs)))
print("DNP in BOM but not in sch:", sorted(set(dnpbomrefs) - set(schdnp)))
dnp_qty = sum(int(float(r['Qty'])) for r in dnprows)
print("qty on DNP lines:", dnp_qty, "-> purchasable placements:", tot_qty - dnp_qty)

print()
print("=== value / footprint cross-check (BOM line vs schematic) ===")
for r in rows:
    refs = [x.strip() for x in r['Refs'].split(',') if x.strip()]
    for ref in refs:
        s = schmap.get(ref)
        if not s:
            continue
        if (s['value'] or '') != r['Value']:
            print(f"  VALUE DIFF {ref}: bom={r['Value']!r} sch={s['value']!r}")
        if (s['fp'] or '') != r['Footprint']:
            print(f"  FP DIFF    {ref}: bom={r['Footprint']!r} sch={s['fp']!r}")

print()
print("=== lines grouping check: do refs on a line share value+fp in sch? ===")
for r in rows:
    refs = [x.strip() for x in r['Refs'].split(',') if x.strip()]
    vals = set((schmap[x]['value'], schmap[x]['fp']) for x in refs if x in schmap)
    if len(vals) > 1:
        print("  MIXED LINE", r['Refs'], vals)

print()
print("=== identical value+footprint spread across multiple BOM lines ===")
grp = collections.defaultdict(list)
for r in rows:
    grp[(r['Value'], r['Footprint'])].append(r['Refs'])
for k, v in grp.items():
    if len(v) > 1:
        print("  ", k, "->", v)

print()
print("=== per-line MPN emptiness / placeholders ===")
for r in rows:
    m = r['MPN'].strip()
    if m == '' or m == '--':
        print(f"  NO MPN: {r['Refs'][:45]:47s} value={r['Value']} flag={r['ReviewFlag']!r} dnp={r['DNP']!r}")

print()
print("=== columns present ===")
print(rows[0].keys())
print()
print("=== ReviewFlag values ===")
for r in rows:
    if r['ReviewFlag'].strip():
        print(f"  {r['Refs'][:45]:47s} {r['ReviewFlag']}")

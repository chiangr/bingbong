import json, collections, io, csv, re

base = r"C:/Users/chian/Desktop/bingbong_software/bingbong_pcb/"
syms = json.load(open(base + "_bomaudit_syms.json"))
real = [s for s in syms if not (s['libid'] or '').startswith('power:')]

allprops = collections.Counter()
for s in real:
    for k in s['props']:
        allprops[k] += 1
print("=== property names across the 104 real symbols (count) ===")
for k, v in allprops.most_common():
    print(f"  {k:22s} {v}")

print()
print("=== does ANY symbol carry Voltage / Tolerance / MPN / Manufacturer / LCSC? ===")
for k in ['Voltage', 'Tolerance', 'MPN', 'Manufacturer', 'Mfr', 'LCSC', 'Dielectric',
          'Power', 'Part Number', 'MFN', 'Supplier', 'Digikey', 'DigiKey', 'Vendor', 'PN']:
    hits = [s['ref'] for s in real if k in s['props'] and s['props'][k].strip()]
    print(f"  {k:14s}: {len(hits)} -> {hits[:8]}")

print()
print("=== Datasheet property populated? ===")
ds = [s['ref'] for s in real if s['props'].get('Datasheet', '~').strip() not in ('', '~')]
print(f"  populated: {len(ds)}/{len(real)} -> {sorted(ds)}")

print()
print("=== full Description properties (check BOM truncation) ===")
for s in sorted(real, key=lambda x: x['ref']):
    d = s['props'].get('Description', '')
    if d:
        print(f"  {s['ref']:5s} ({len(d):3d}) {d}")

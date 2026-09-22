import csv, io, re, collections

base = r"C:/Users/chian/Desktop/bingbong_software/bingbong_pcb/"
rows = list(csv.DictReader(io.open(base + "BOM_2026-09-04.csv", encoding='utf-8-sig')))


def norm(v):
    """normalise a value string to farads/ohms/henries float"""
    v = v.strip().replace(' ', '')
    m = re.match(r'^([\d.]+)\s*([pnumkKMR]?)([FfHh]?|Ohms?|ohms?)?$', v)
    if not m:
        return None
    x = float(m.group(1))
    mult = {'p': 1e-12, 'n': 1e-9, 'u': 1e-6, 'm': 1e-3, '': 1, 'k': 1e3,
            'K': 1e3, 'M': 1e6, 'R': 1}[m.group(2)]
    return x * mult


print("=== VALUE vs LegacyDesc (what the automated pass never checked) ===")
for r in rows:
    d = r['LegacyDesc']
    v = r['Value']
    if not d.strip():
        continue
    m = re.match(r'^\s*([\d.]+)\s*(pF|nF|.F|.?F|kOhms?|Ohms?|MOhms?|.H)', d.replace('\u00b5', 'u'))
    if not m:
        continue
    dv = norm((m.group(1) + m.group(2)).replace('kOhms', 'k').replace('kOhm', 'k')
              .replace('Ohms', '').replace('Ohm', ''))
    sv = norm(v)
    if dv is None or sv is None:
        continue
    if max(dv, sv) == 0:
        continue
    if abs(dv - sv) / max(dv, sv) > 0.02:
        ratio = (sv / dv) if dv else float('inf')
        print(f"  VALUE MISMATCH {r['Refs'][:38]:40s} sch={v:8s} MPN={r['MPN'][:34]:36s} "
              f"legacy='{m.group(0).strip()}'  ratio sch/mpn = {ratio:g}x   flag={r['ReviewFlag']!r}")

print()
print("=== MPN reused on more than one BOM line ===")
g = collections.defaultdict(list)
for r in rows:
    if r['MPN'].strip() and r['MPN'].strip() != '--':
        g[r['MPN'].strip()].append((r['Refs'], r['Value'], r['Footprint'], r['Qty']))
for k, v in g.items():
    if len(v) > 1:
        print(f"  {k}:")
        for x in v:
            print(f"      {x}")

print()
print("=== MPNs that look Excel-corrupted (scientific notation / stray chars) ===")
for r in rows:
    m = r['MPN'].strip()
    if re.match(r'^[\d.]+E[+-]?\d+$', m) or m.endswith('--') or m == '--' or '/' in m or '_' in m:
        print(f"  {r['Refs'][:30]:32s} MPN={m!r}  DK={r['DigiKey']!r}")

print()
print("=== Price / Datasheet / DigiKey completeness ===")
miss_price = [r['Refs'] for r in rows if not r['Price'].strip()]
miss_dk = [r['Refs'] for r in rows if r['DigiKey'].strip() in ('', '--')]
miss_ds = [r['Refs'] for r in rows if r['Datasheet'].strip() in ('', '~', '--')]
print("  lines with NO Price   :", len(miss_price), miss_price)
print("  lines with NO DigiKey :", len(miss_dk), miss_dk)
print("  lines with NO Datasheet:", len(miss_ds), miss_ds)
tot = 0.0
unpriced_qty = 0
for r in rows:
    q = int(float(r['Qty']))
    if r['DNP'].strip():
        continue
    if r['Price'].strip():
        tot += q * float(r['Price'])
    else:
        unpriced_qty += q
print(f"  extended cost of PRICED, non-DNP lines: ${tot:.2f};  unpriced non-DNP placements: {unpriced_qty}")

print()
print("=== THT / non-SMT lines (turnkey surcharge, no reflow) ===")
for r in rows:
    f = r['Footprint']
    if 'THT' in f or 'PinHeader' in f or 'Cherry_MX' in f or 'JST_PH' in f or 'Radial' in f:
        print(f"  {r['Refs'][:20]:22s} {f}")

print()
print("=== Lines whose Value is a placeholder / not an electrical value ===")
for r in rows:
    v = r['Value']
    if v == 'DNP' or v.startswith('Conn_') or v in ('SW_Push', 'Battery_NTC'):
        print(f"  {r['Refs'][:34]:36s} Value={v!r}")

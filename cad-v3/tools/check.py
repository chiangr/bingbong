"""Run KiCad ERC + netlist on the v3 main board and print per-component pin nets.

usage: python3 check.py [ref-prefix-filter ...]
"""
import os
import re
import subprocess
import sys

CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
V3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD = os.environ.get("BOARD", "bingbong")        # BOARD=satellite for the crown board
PRJ = os.path.join(V3, BOARD)
SCH = os.path.join(PRJ, {"bingbong": "bingbong_v3", "satellite": "satellite_v3", "satellite_b": "satellite_b_v3"}[BOARD] + ".kicad_sch")
OUT = os.path.join(PRJ, "_check")
os.makedirs(OUT, exist_ok=True)


def run(args):
    r = subprocess.run([CLI] + args, capture_output=True, text=True)
    msg = "\n".join(l for l in (r.stdout + r.stderr).splitlines() if "Fontconfig" not in l)
    if r.returncode not in (0, 5):
        print(msg)
        sys.exit("kicad-cli failed")
    return msg


run(["sch", "erc", "--severity-all", "-o", os.path.join(OUT, "erc.rpt"), SCH])
erc = open(os.path.join(OUT, "erc.rpt")).read()
print(re.search(r"\*\* ERC messages:.*", erc).group(0))
for block in re.findall(r"\[[a-z_]+\]:.*?(?=\n\[|\n \*\*|\Z)", erc, re.S):
    print("  " + " | ".join(l.strip() for l in block.splitlines() if l.strip()))

run(["sch", "export", "netlist", "--format", "kicadsexpr", "-o", os.path.join(OUT, "net.net"), SCH])
net = open(os.path.join(OUT, "net.net")).read()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schgen import parse, tokenize
tree, _ = parse(tokenize(net))
nets = next(n for n in tree[0] if isinstance(n, list) and n[0] == "nets")
pinnet = {}
for n in nets[1:]:
    name = next(x for x in n if isinstance(x, list) and x[0] == "name")[1]
    for node in (x for x in n if isinstance(x, list) and x[0] == "node"):
        ref = next(x for x in node if x[0] == "ref")[1]
        pin = next(x for x in node if x[0] == "pin")[1]
        pinnet[(ref, pin)] = name
flt = sys.argv[1:]
for (ref, pin), name in sorted(pinnet.items()):
    if not flt or any(ref.startswith(f) for f in flt):
        print(f"{ref:6s} {pin:4s} {name}")

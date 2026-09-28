#!/bin/bash
# fpview.sh NAME... : render footprint(s) from lib/Bingbong_v3.pretty to big PNGs in bingbong/_check/fp
O=/Users/ryan/Desktop/bingbong/cad-v3/bingbong/_check/fp; mkdir -p $O
cd /Users/ryan/Desktop/bingbong/cad-v3/lib
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli fp export svg --output $O --layers "F.Cu,F.Mask,F.Paste,F.Fab,F.CrtYd,F.SilkS" Bingbong_v3.pretty >/dev/null 2>&1
cd $O
for n in "$@"; do
  python3 - "$n.svg" <<'P'
import re,sys
p=sys.argv[1]; s=open(p).read()
s=re.sub(r'width="([\d.]+)mm"', lambda m:'width="%gmm"'%(float(m.group(1))*6), s, 1)
s=re.sub(r'height="([\d.]+)mm"', lambda m:'height="%gmm"'%(float(m.group(1))*6), s, 1)
open(p.replace('.svg','_big.svg'),'w').write(s)
P
  qlmanage -t -s 1000 -o . "${n}_big.svg" >/dev/null 2>&1
done

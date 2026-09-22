import re,csv
BS=chr(92)
def blocks(txt, tok):
    out=[]
    for m in re.finditer(re.escape(tok), txt):
        i=m.start(); d=0; j=i; instr=False
        while j < len(txt):
            c=txt[j]
            if instr:
                if c==BS: j+=2; continue
                if c=='"': instr=False
            else:
                if c=='"': instr=True
                elif c=='(': d+=1
                elif c==')':
                    d-=1
                    if d==0: out.append((i,j+1)); break
            j+=1
    return out
s=open('bingbong.kicad_sch',encoding='utf-8',errors='ignore').read()
res={}
for a,b in blocks(s,'(symbol'):
    seg=s[a:b]
    if len(seg)>20000: continue
    r=re.search(r'\(property "Reference" "([^"]+)"',seg)
    f=re.search(r'\(property "Footprint" "([^"]*)"',seg)
    if r and f and r.group(1) not in res: res[r.group(1)]=f.group(1)
for k in ['TH1','J2','J3','J4','J5','J6','J7','J8','S1','S2','SW1']:
    print(f"SCH {k:4s} -> {res.get(k,'??')}")
print()
t=open('bingbong.kicad_pcb',encoding='utf-8',errors='ignore').read()
pcb=set(re.findall(r'\(property "Reference" "([^"]+)"',t))
bom=set()
for row in csv.DictReader(open('BOM_2026-09-04.csv',encoding='utf-8')):
    for r in row['Refs'].split(','):
        if r.strip(): bom.add(r.strip())
print("BOM designators:",len(bom),"  PCB placed:",len(pcb))
print("IN BOM/SCH BUT NOT PLACED ON PCB:",sorted(bom-pcb))
print("ON PCB BUT NOT IN BOM:",sorted(pcb-bom))

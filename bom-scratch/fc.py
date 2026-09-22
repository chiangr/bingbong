import re,subprocess,sys,urllib.parse,html
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
def run(mpn):
    url="https://www.findchips.com/search/"+urllib.parse.quote(mpn)
    h=subprocess.run(["curl","-sSL","--compressed","-m","60","-A",UA,url],capture_output=True,text=True,errors="ignore").stdout
    print("###",mpn," (html %d bytes)"%len(h))
    rows=re.findall(r'<tr data-id="[^"]*"([^>]*?)class="row"',h,re.S)
    seen=set()
    out=[]
    for r in rows:
        def g(a):
            m=re.search(a+r'="([^"]*)"',r)
            return html.unescape(m.group(1)) if m else ""
        d=g('data-distributor_name'); mfr=g('data-mfr'); pn=g('data-mfrpartnumber')
        stock=g('data-instock'); price=g('data-price')
        p1=""
        pm=re.findall(r'\[(\d+),"USD","([\d.]+)"\]',price)
        if pm:
            pm=sorted(pm,key=lambda x:int(x[0]))
            p1="; ".join(f"{q}:${p}" for q,p in pm[:3])
        key=(d,pn,stock)
        if key in seen: continue
        seen.add(key)
        out.append((int(stock or 0),d,mfr,pn,stock,p1))
    out.sort(reverse=True)
    for s,d,mfr,pn,stock,p1 in out[:14]:
        print(f"  {d:28s} | {mfr:22s} | {pn:26s} | stock={stock:>9s} | {p1}")
    if not out: print("  NO ROWS")
    print()
for mpn in sys.argv[1:]:
    run(mpn)

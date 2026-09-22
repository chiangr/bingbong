import json,re,subprocess,sys,urllib.parse
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
def get(url):
    return subprocess.run(["curl","-sSL","--compressed","-m","45","-A",UA,url],capture_output=True,text=True,errors="ignore").stdout
def show(kw):
    url="https://www.lcsc.com/search?q="+urllib.parse.quote(kw)
    h=get(url)
    # pull embedded next data
    seen=set()
    for m in re.finditer(r'"productCode":"(C\d+)"',h):
        code=m.group(1)
        if code in seen: continue
        seen.add(code)
        seg=h[max(0,m.start()-3000):m.start()+3000]
        def f(p,default="?"):
            mm=re.search(p,seg)
            return mm.group(1) if mm else default
        model=f(r'"productModel":"([^"]*)"')
        brand=f(r'"brandNameEn":"([^"]*)"')
        stock=f(r'"stockNumber":(\d+)')
        desc=f(r'"productIntroEn":"([^"]*)"') 
        price=f(r'"usdPrice":([\d.]+)')
        if kw.lower().replace('-','') in model.lower().replace('-','') or kw.lower() in desc.lower():
            print(f"  LCSC {code} | {brand} | {model} | stock={stock} | ${price} | {desc[:110]}")
    if not seen: print("  (no LCSC results parsed)")
for kw in sys.argv[1:]:
    print("###",kw)
    show(kw)
    print()

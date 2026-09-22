import re,html,sys
p=sys.argv[1]
t=open(p,encoding='utf-8',errors='ignore').read()
t2=re.sub(r'<script.*?</script>','',t,flags=re.S)
t2=re.sub(r'<style.*?</style>','',t2,flags=re.S)
txt=html.unescape(re.sub(r'<[^>]+>','\n',t2))
lines=[re.sub(r'\s+',' ',l).strip() for l in txt.split('\n')]
lines=[l for l in lines if l]
blob=' | '.join(lines)
for kw in sys.argv[2:]:
    hits=[m.start() for m in re.finditer(re.escape(kw),blob,re.I)][:3]
    if not hits: print('--',kw,'NOT FOUND')
    for h in hits:
        print('>>',kw,':',blob[max(0,h-150):h+300].strip()[:430])
    print()

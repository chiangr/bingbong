import re,sys,math

def toks(s):
    out=[];i=0;n=len(s)
    while i<n:
        c=s[i]
        if c in '()':
            out.append(c);i+=1
        elif c=='"':
            j=i+1;buf=''
            while j<n:
                if s[j]==chr(92):
                    buf+=s[j+1];j+=2;continue
                if s[j]=='"': break
                buf+=s[j];j+=1
            out.append(('STR',buf));i=j+1
        elif c.isspace():
            i+=1
        else:
            j=i
            while j<n and (not s[j].isspace()) and s[j] not in '()"': j+=1
            out.append(('SYM',s[i:j]));i=j
    return out

def parse(s):
    tk=toks(s);pos=[0]
    def p():
        t=tk[pos[0]]
        if t=='(':
            pos[0]+=1;lst=[]
            while tk[pos[0]]!=')':
                lst.append(p())
            pos[0]+=1
            return lst
        else:
            pos[0]+=1
            return t[1]
    res=[]
    while pos[0]<len(tk):
        res.append(p())
    return res

def walk(node,name):
    if isinstance(node,list):
        if node and node[0]==name:
            yield node
        for c in node:
            yield from walk(c,name)

def getpads(fn):
    s=open(fn,encoding='utf-8').read()
    tree=parse(s)[0]
    pads=[]
    for p in walk(tree,'pad'):
        num=p[1]; typ=p[2]; shape=p[3]
        at=None;size=None;layers=None;dm=None
        for c in p[4:]:
            if isinstance(c,list):
                if c[0]=='at': at=[float(x) for x in c[1:] if re.match(r'^-?[\d.]+$',str(x))]
                elif c[0]=='size': size=[float(x) for x in c[1:3]]
                elif c[0]=='layers': layers=c[1:]
                elif c[0]=='drill': dm=[str(x) for x in c[1:]]
        pads.append({'num':num,'type':typ,'shape':shape,'at':at,'size':size,'layers':layers,'drill':dm})
    return tree,pads

if __name__=='__main__':
    for fn in sys.argv[1:]:
        tree,pads=getpads(fn)
        print('==== FILE',fn,'npads',len(pads))
        for p in pads:
            print('  pad %6s %10s %12s at=%s size=%s layers=%s' % (p['num'],p['type'],p['shape'],p['at'],p['size'],p['layers']))

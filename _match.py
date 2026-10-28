import io,re,json
pool=json.loads(io.open('_pool.json',encoding='utf-8').read())
s=io.open('index.html',encoding='utf-8').read()
body=s.split('const DATA = [')[1].split('\n];')[0]
segs=body.split("{n:'")[1:]
items=[]
for seg in segs:
    n=seg.split("'")[0]
    m=re.search(r"c:'([^']*)'",seg[:400])
    items.append((n,m.group(1) if m else ''))

def keys(n):
    b=n.split('/')[0].strip()
    if re.search(r'[A-Za-z]',b):
        b=re.sub(r'\s+[\u4e00-\u9fff]+.*$','',b).strip()
    ks={b.lower().replace(' ','')}
    k2=re.sub(r'\s*ai$','',b,flags=re.I).strip()
    if k2 and k2!=b: ks.add(k2.lower().replace(' ',''))
    if re.search(r'[\u4e00-\u9fff]',b):
        zh=re.sub(r'[A-Za-z\s]','',b)
        if len(zh)>=2: ks.add(zh)
    return {k for k in ks if len(k)>=2}

def pct(vals,x):
    if len(vals)<=1: return 1.0
    return sum(1 for v in vals if v<x)/len(vals)

res={}
for n,c in items:
    videos=pool.get(c,[])
    likes=[v["l"] for v in videos]; plays=[v["pl"] for v in videos]
    ks=keys(n); hit=[]
    for v in videos:
        blob=(v["t"]+" "+v["d"]).lower().replace(' ','')
        if any(k in blob for k in ks):
            sc=pct(likes,v["l"])*0.5 + pct(plays,v["pl"])*0.5
            hit.append({**v,"sc":round(sc,3)})
    hit.sort(key=lambda x:(-x["sc"],-x["l"]))
    hit=hit[:3]
    res[n]={"c":c,"status":"ok" if len(hit)==3 else ("short" if hit else "none"),"vids":hit}

io.open('_evidence.json','w',encoding='utf-8').write(json.dumps(res,ensure_ascii=False,indent=1))
ok=[n for n,v in res.items() if v["status"]=="ok"]
sh=[n for n,v in res.items() if v["status"]=="short"]
no=[n for n,v in res.items() if v["status"]=="none"]
print(f"满3条 {len(ok)}  1-2条 {len(sh)}  0条 {len(no)}  合计 {len(res)}")
print(f"覆盖率 {len(ok)/len(res)*100:.1f}%")
from collections import Counter
print("按模块:",Counter(v["c"] for v in res.values() if v["status"]=="ok"))
print("\n满3条示例:",ok[:6])
print("0条示例:",no[:10])

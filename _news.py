import io,json,re,time,urllib.request,urllib.parse
from email.utils import parsedate_to_datetime
import datetime
CUT=datetime.datetime(2026,7,29)
final=json.loads(io.open('_final2.json',encoding='utf-8').read())
def q_latest(q):
    u="https://news.google.com/rss/search?hl=zh-CN&gl=CN&ceid=CN:zh-Hans&q="+urllib.parse.quote(q)
    req=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
    try: x=urllib.request.urlopen(req,timeout=15).read().decode('utf-8','ignore')
    except Exception: return None,0
    ds=[]
    for d in re.findall(r'<pubDate>(.*?)</pubDate>',x)[:20]:
        try: ds.append(parsedate_to_datetime(d).replace(tzinfo=None))
        except Exception: pass
    return (max(ds) if ds else None), len(ds)
targets={k:v for k,v in final.items() if v["n_all"]==0}
print("no-evidence targets:",len(targets),flush=True)
out={}
try: out=json.loads(io.open('_news.json',encoding='utf-8').read())
except Exception: pass
for i,(k,v) in enumerate(targets.items()):
    if k in out: continue
    n=v["n"]
    d,c=q_latest(n); time.sleep(0.8)
    alt=re.sub(r'\s+(Dream Machine|AI|Pro|Studio|Video|Image)$','',n,flags=re.I).strip()
    if (d is None or d<CUT) and alt!=n:
        d2,c2=q_latest(alt); time.sleep(0.8)
        if d2 and (d is None or d2>d): d,c=d2,c2
    verdict="keep" if (d and d>=CUT) else "drop"
    out[k]={"n":n,"c":v["c"],"latest":d.strftime("%Y-%m-%d") if d else "","cnt":c,"verdict":verdict}
    print(f"{i+1}/{len(targets)} {n} {out[k]['latest'] or '—'} {verdict}",flush=True)
    if (i+1)%10==0: io.open('_news.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=1))
io.open('_news.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=1))
k=sum(1 for v in out.values() if v["verdict"]=="keep")
print(f"DONE keep={k} drop={len(out)-k}",flush=True)

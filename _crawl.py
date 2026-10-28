import io,re,json,time,urllib.request,urllib.parse,http.cookiejar,sys,datetime

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
cj=http.cookiejar.CookieJar()
op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders=[("User-Agent",UA),("Referer","https://www.bilibili.com/")]
op.open("https://www.bilibili.com/",timeout=20).read()

CUT=int(datetime.datetime(2026,8,29).timestamp())
s=io.open('index.html',encoding='utf-8').read()
body=s.split('const DATA = [')[1].split('];')[0]
items=re.findall(r"\{n:'([^']*)',c:'([^']*)'", body)
print("targets:",len(items),flush=True)

def kw_for(n):
    k=n.replace(' ','')
    if re.search(r'[\u4e00-\u9fff]',n): return n
    if len(k)<=5: return n+' ai'
    return n

def search(kw):
    u="https://api.bilibili.com/x/web-interface/search/type?search_type=video&order=totalrank&page=1&keyword="+urllib.parse.quote(kw)
    for attempt in range(2):
        try:
            d=json.loads(op.open(u,timeout=20).read())
            if d.get("code")==0:
                return (d.get("data") or {}).get("result") or []
            time.sleep(3)
        except Exception:
            time.sleep(3)
    return None

out={}
try: out=json.loads(io.open('_evidence.json',encoding='utf-8').read())
except Exception: pass

for i,(n,c) in enumerate(items):
    if n in out: continue
    key=n.lower().replace(' ','')
    rs=search(kw_for(n))
    time.sleep(1.5)
    if rs is None:
        out[n]={"c":c,"status":"error","vids":[]}
        print(f"[{i+1}/{len(items)}] {n} ERROR",flush=True); continue
    cand=[]
    for r in rs:
        title=(r.get("title") or "").replace('<em class="keyword">','').replace('</em>','')
        blob=((r.get("title") or "")+(r.get("description") or "")+(r.get("tag") or "")).lower().replace(' ','')
        if key not in blob: continue
        if (r.get("pubdate") or 0) < CUT: continue
        cand.append({"t":title,"a":r.get("author",""),"l":r.get("like") or 0,
                     "p":datetime.datetime.fromtimestamp(r["pubdate"]).strftime("%Y-%m-%d"),
                     "b":r.get("bvid","")})
    cand.sort(key=lambda x:-x["l"])
    cand=cand[:3]
    out[n]={"c":c,"status":"ok" if len(cand)==3 else ("short" if cand else "none"),"vids":cand}
    print(f"[{i+1}/{len(items)}] {n} {len(cand)}",flush=True)
    if (i+1)%10==0:
        io.open('_evidence.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=1))

io.open('_evidence.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=1))
ok=sum(1 for v in out.values() if v["status"]=="ok")
sh=sum(1 for v in out.values() if v["status"]=="short")
no=sum(1 for v in out.values() if v["status"]=="none")
er=sum(1 for v in out.values() if v["status"]=="error")
print(f"\nDONE ok={ok} short={sh} none={no} error={er} total={len(out)}",flush=True)

import io,re,json,time,urllib.request,urllib.parse,http.cookiejar,datetime
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
cj=http.cookiejar.CookieJar(); op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders=[("User-Agent",UA),("Referer","https://www.bilibili.com/")]
op.open("https://www.bilibili.com/",timeout=20).read()
CUT=int(datetime.datetime(2026,8,29).timestamp())
s=io.open('index.html',encoding='utf-8').read()
body=re.search(r'const DATA\s*=\s*\[(.*?)\n\];',s,re.S).group(1)
items=[]
for seg in body.split("{n:'")[1:]:
    n=seg.split("'")[0]
    mm=re.search(r"c:'([^']*)'",seg[:400]); items.append((n,mm.group(1) if mm else ''))
print("targets",len(items),flush=True)
def base_of(n):
    b=n.split('/')[0].strip()
    if re.search(r'[A-Za-z]',b): b=re.sub(r'\s+[\u4e00-\u9fff]+.*$','',b).strip()
    return b
def search(kw):
    u="https://api.bilibili.com/x/web-interface/search/type?search_type=video&order=totalrank&page=1&keyword="+urllib.parse.quote(kw)
    for _ in range(2):
        try:
            d=json.loads(op.open(u,timeout=20).read())
            if d.get("code")==0: return (d.get("data") or {}).get("result") or []
            time.sleep(3)
        except Exception: time.sleep(3)
    return None
out={}
try: out=json.loads(io.open('_raw.json',encoding='utf-8').read())
except Exception: pass
for i,(n,c) in enumerate(items):
    k=f"{n}|{c}"
    if k in out: continue
    b=base_of(n); kw=b+(" 测评" if re.search(r'[\u4e00-\u9fff]',b) else " review")
    rs=search(kw); time.sleep(1.3)
    if rs is None:
        out[k]={"n":n,"c":c,"kw":kw,"raw":None}; print(f"{i+1} {n} ERR",flush=True); continue
    raw=[]
    for r in rs:
        t=(r.get("title") or "").replace('<em class="keyword">','').replace('</em>','')
        if (r.get("pubdate") or 0)<CUT: continue
        raw.append({"t":t,"d":(r.get("description") or "")[:180],"a":r.get("author",""),
                    "l":r.get("like") or 0,"pl":r.get("play") or 0,
                    "p":datetime.datetime.fromtimestamp(r["pubdate"]).strftime("%Y-%m-%d"),
                    "b":r.get("bvid","")})
    out[k]={"n":n,"c":c,"kw":kw,"raw":raw}
    print(f"{i+1} {n} {len(raw)}",flush=True)
    if (i+1)%15==0: io.open('_raw.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=1))
io.open('_raw.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=1))
print("DONE",len(out),flush=True)

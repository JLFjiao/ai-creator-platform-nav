import io,re,json,time,urllib.request,urllib.parse,http.cookiejar,datetime
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
cj=http.cookiejar.CookieJar(); op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders=[("User-Agent",UA),("Referer","https://www.bilibili.com/")]
op.open("https://www.bilibili.com/",timeout=20).read()
CUT=int(datetime.datetime(2026,8,29).timestamp())

KW={
 "code":["AI编程 横评","AI编程工具 对比","AI写代码 对比测试","cursor copilot 对比","编程AI 哪个好用"],
 "video":["AI视频 横评","文生视频 对比","可灵 即梦 对比","AI视频模型 对比测评","视频生成 哪个好"],
 "image":["AI绘画 横评","文生图 对比","midjourney 即梦 对比","AI绘图工具 对比","图片生成 哪个好"],
 "chat":["大模型 横评","AI对话 对比","deepseek 豆包 对比","国产大模型 对比","AI助手 哪个好用"],
 "audio":["AI音乐 横评","AI配音 对比","suno 对比","AI音频工具 对比","音乐生成 哪个好"],
 "office":["AI办公 横评","AI做PPT 对比","AI文档工具 对比","办公AI 哪个好用"],
 "design":["AI设计 横评","AI做UI 对比","figma ai 对比","设计AI 哪个好用"],
 "agent":["AI智能体 横评","coze 扣子 对比","AI工作流 对比","低代码AI 哪个好用"],
}
HZ=re.compile(r'对比|横评|pk|vs|哪个|排行|对决|盲测|盘点|谁更强|孰强')
def search(kw,page=1):
    u=f"https://api.bilibili.com/x/web-interface/search/type?search_type=video&order=totalrank&page={page}&keyword="+urllib.parse.quote(kw)
    for _ in range(2):
        try:
            d=json.loads(op.open(u,timeout=20).read())
            if d.get("code")==0: return (d.get("data") or {}).get("result") or []
            time.sleep(3)
        except Exception: time.sleep(3)
    return None

pool={}
for cat,kws in KW.items():
    seen={}
    for kw in kws:
        rs=search(kw)
        time.sleep(1.4)
        if not rs: print(f"  {cat} / {kw} FAIL",flush=True); continue
        n_new=0
        for r in rs:
            title=(r.get("title") or "").replace('<em class="keyword">','').replace('</em>','')
            desc=r.get("description") or ""
            blob=title+" "+desc
            if not HZ.search(blob.lower()): continue
            if (r.get("pubdate") or 0)<CUT: continue
            bv=r.get("bvid") or ""
            if not bv or bv in seen: continue
            seen[bv]={"t":title,"a":r.get("author",""),"l":r.get("like") or 0,
                      "pl":r.get("play") or 0,"p":datetime.datetime.fromtimestamp(r["pubdate"]).strftime("%Y-%m-%d"),
                      "b":bv,"d":desc[:120]}
            n_new+=1
        print(f"  {cat} / {kw}: 新增 {n_new}，池 {len(seen)}",flush=True)
    pool[cat]=list(seen.values())

io.open('_pool.json','w',encoding='utf-8').write(json.dumps(pool,ensure_ascii=False,indent=1))
for c,v in pool.items(): print(c,len(v))
print("TOTAL",sum(len(v) for v in pool.values()),flush=True)

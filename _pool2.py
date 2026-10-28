import io,re,json,time,urllib.request,urllib.parse,http.cookiejar,datetime
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
cj=http.cookiejar.CookieJar(); op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders=[("User-Agent",UA),("Referer","https://www.bilibili.com/")]
op.open("https://www.bilibili.com/",timeout=20).read()
CUT=int(datetime.datetime(2026,8,29).timestamp())
KW={
 "code":["AI编程 横评","AI编程工具 对比","AI写代码 对比测试","cursor copilot 对比","编程AI 哪个好用","AI编程 深度对比","代码助手 对比","cursor 对比 windsurf","AI IDE 对比","程序员 AI 工具 对比"],
 "video":["AI视频 横评","文生视频 对比","可灵 即梦 对比","AI视频模型 对比测评","视频生成 哪个好","AI视频 深度对比","sora 可灵 对比","国产视频模型 对比","AI视频工具 怎么选","vidu 可灵 对比"],
 "image":["AI绘画 横评","文生图 对比","midjourney 即梦 对比","AI绘图工具 对比","图片生成 哪个好","AI绘画 深度对比","即梦 midjourney 对比","国产AI绘画 对比","AI绘图 怎么选","AI生图 横评"],
 "chat":["大模型 横评","AI对话 对比","deepseek 豆包 对比","国产大模型 对比","AI助手 哪个好用","大模型 深度对比","gpt claude 对比","国产大模型 横评","AI 聊天 怎么选","kimi 豆包 对比"],
 "audio":["AI音乐 横评","AI配音 对比","suno 对比","AI音频工具 对比","音乐生成 哪个好","AI音乐 深度对比","suno udio 对比","AI配音 工具 推荐","TTS 对比","AI 克隆音色 对比"],
 "office":["AI办公 横评","AI做PPT 对比","AI文档工具 对比","办公AI 哪个好用","AI PPT 深度对比","AI 写文档 对比","AI 表格 对比","WPS AI 对比"],
 "design":["AI设计 横评","AI做UI 对比","figma ai 对比","设计AI 哪个好用","AI UI 设计 深度对比","figma 对比 即时设计","AI 原型 对比","设计工具 AI 对比"],
 "agent":["AI智能体 横评","coze 扣子 对比","AI工作流 对比","低代码AI 哪个好用","AI 智能体 深度对比","coze dify 对比","AI 搭建 对比","智能体平台 对比"],
}
HZ=re.compile(r'对比|横评|pk|vs|哪个|排行|对决|盲测|盘点|谁更强|孰强|怎么选')
def search(kw,page):
    u=f"https://api.bilibili.com/x/web-interface/search/type?search_type=video&order=totalrank&page={page}&keyword="+urllib.parse.quote(kw)
    try:
        d=json.loads(op.open(u,timeout=20).read())
        if d.get("code")==0: return (d.get("data") or {}).get("result") or []
    except Exception: pass
    return []
try: pool=json.loads(io.open('_pool.json',encoding='utf-8').read())
except Exception: pool={}
for cat,kws in KW.items():
    seen={v["b"]:v for v in pool.get(cat,[])}
    for kw in kws:
        for pg in (1,2):
            rs=search(kw,pg); time.sleep(1.3)
            for r in rs:
                title=(r.get("title") or "").replace('<em class="keyword">','').replace('</em>','')
                desc=r.get("description") or ""
                if not HZ.search((title+" "+desc).lower()): continue
                if (r.get("pubdate") or 0)<CUT: continue
                bv=r.get("bvid") or ""
                if not bv or bv in seen: continue
                seen[bv]={"t":title,"a":r.get("author",""),"l":r.get("like") or 0,
                          "pl":r.get("play") or 0,"p":datetime.datetime.fromtimestamp(r["pubdate"]).strftime("%Y-%m-%d"),
                          "b":bv,"d":desc[:150]}
        print(f"  {cat}/{kw}: {len(seen)}",flush=True)
    pool[cat]=list(seen.values())
io.open('_pool.json','w',encoding='utf-8').write(json.dumps(pool,ensure_ascii=False,indent=1))
for c,v in pool.items(): print(c,len(v))
print("TOTAL",sum(len(v) for v in pool.values()),flush=True)

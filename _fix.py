import io, re

P = 'index.html'
s = io.open(P, encoding='utf-8').read()

# 1) 删除整段评分机制（含 scoreOf / scoreTitle / review），替换为证据渲染
start = s.index("// ===== 评分机制 =====")
end = s.index("DATA.forEach(d => { d.r = scoreOf(d); });") + len("DATA.forEach(d => { d.r = scoreOf(d); });")
videos_fn = '''// 本站不做评分：卡片只展示可核查的 B 站测评证据，不折算分数。
function videos(d){
  if(!d.vids || !d.vids.length) return '';
  const items = d.vids.map(v=>`<a class="vid" href="https://www.bilibili.com/video/${esc(v.b)}" target="_blank" rel="noopener"><span class="vl">${v.l>=10000?(v.l/10000).toFixed(1)+'万':v.l}</span> 赞 · ${esc(v.t)}<span class="vd">${esc(v.p)}</span></a>`).join('');
  return `<div class="rev"><b>B 站测评</b>（近 2 个月）：${items}</div>`;
}'''
s = s[:start] + videos_fn + s[end:]

# 2) 默认排序
s = s.replace("favOnly:false, sort:'score', q:''", "favOnly:false, sort:'rec', q:''")
s = s.replace("state.sort='score'", "state.sort='rec'")

# 3) 卡片：去评分徽标
old_score = '''          <span class="score" title="${esc(scoreTitle(d))}"><em>评分</em>${d.r.toFixed(1)}<i>/10</i></span>\n'''
assert old_score in s, "score span not found"
s = s.replace(old_score, '')

# 4) 名称后加模型名
old_name = '<span class="name" title="${esc(d.n)}">${esc(d.n)}</span>'
new_name = "<span class=\"name\" title=\"${esc(d.n)}\">${esc(d.n)}${d.md?' <i>'+esc(d.md)+'</i>':''}</span>"
assert old_name in s, "name span not found"
s = s.replace(old_name, new_name)

# 5) 卡片调用改为 videos
assert "      ${review(d)}" in s, "review call not found"
s = s.replace("      ${review(d)}", "      ${videos(d)}")

# 6) sortRows 去掉评分
old_sort = s[s.index("function sortRows(list){"):s.index("function render(){")]
new_sort = '''function sortRows(list){
  const arr = list.slice();
  const byName = (a,b) => a.n.localeCompare(b.n, 'zh');
  if(state.sort === 'scale'){
    arr.sort((a,b)=> (b.m||0)-(a.m||0) || byName(a,b));
  } else if(state.sort === 'name'){
    arr.sort(byName);
  } else {
    arr.sort((a,b)=>
      ((a.co==='中国')?0:1) - ((b.co==='中国')?0:1) ||
      (b.m?1:0) - (a.m?1:0) ||
      (b.m||0) - (a.m||0) ||
      byName(a,b)
    );
  }
  return arr;
}

'''
s = s.replace(old_sort, new_sort)

# 7) 排序下拉：正则整块替换
new_select = '''<select id="sort" title="排序方式">
        <option value="rec" selected>国内优先 · 使用人数</option>
        <option value="scale">使用人数从多到少</option>
        <option value="name">名称 A–Z</option>
      </select>'''
s2 = re.sub(r'<select id="sort".*?</select>', new_select, s, count=1, flags=re.S)
assert s2 != s, "select not replaced"
s = s2

io.open(P, 'w', encoding='utf-8').write(s)
print("written")
print("d.r refs:", s.count("d.r"), "| scoreOf:", s.count("scoreOf"), "| review(:", s.count("review("), "| videos(:", s.count("videos("))
print("records:", s.count("{n:'"))

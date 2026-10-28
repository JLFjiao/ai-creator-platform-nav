import io, re

P = 'index.html'
s = io.open(P, encoding='utf-8').read()

# 1) 新增样式（挂在 .rev 之后）
css_anchor = "  .rev .src{display:block;color:#9aa1ac;font-size:10.5px;margin-top:2px}"
assert css_anchor in s
s = s.replace(css_anchor, css_anchor + """
  .name i{font-style:normal;font-weight:500;font-size:11.5px;color:#0f766e;margin-left:4px;letter-spacing:0}
  .vid{display:block;font-size:11.5px;color:#3f4754;text-decoration:none;padding:1.5px 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .vid:hover{color:#0f766e;text-decoration:underline}
  .vl{display:inline-block;min-width:34px;color:#b42318;font-variant-numeric:tabular-nums;font-weight:600}
  .vd{color:#9aa3b0;margin-left:6px;font-size:10.5px}""", 1)

# 2) 评分口径面板 -> 测评证据口径
new_panel = '''<div class="panel">
    <h2>测评证据口径 <span>不做评分，只列可核查的视频</span></h2>
    <p class="pnote">本站不再给平台打分。原因很直接：把视频的点赞或标题措辞折算成「能力 7.2 分」，本质仍是估计，只是把主观判断从编辑换成了 UP 主的流量表达，不构成可核查的数据。</p>
    <p class="pnote">因此改为只做两件事：给出每个平台近 2 个月的可点开核查的 B 站测评视频；明确标注哪些平台没有公开测评。<b>没有证据不等于平台差</b>，只代表近 2 个月没有可核查的公开测评。</p>
    <table>
      <thead><tr><th style="width:150px">口径</th><th>说明</th></tr></thead>
      <tbody>
        <tr><td>时间窗口</td><td>2026-08-29 之后发布的视频。</td></tr>
        <tr><td>视频类型</td><td>优先横向对比（多模型同题对比），单模型测评降权保留，仅作补充。</td></tr>
        <tr><td>剔除规则</td><td>推广带货、破解版与资源下载类视频不计入。</td></tr>
        <tr><td>排序依据</td><td>点赞与播放量，两者等权，不设自定义系数。</td></tr>
        <tr><td>无测评处理</td><td>标注「近 2 个月无公开测评」，按使用人数排序，无人数按名称排序。</td></tr>
      </tbody>
    </table>
    <p class="pnote">为什么不评分：尝试过按「很强 / 还可以 / 一般 / 不好用」的措辞折算分数，但 B 站标题为流量普遍使用「封神」「天花板」，结果只要被测评过就接近满分，15 个平台挤在同一档，区分度消失。这比不给分更误导。</p>
  </div>

  '''
s2 = re.sub(r'<div class="panel">.*?\n  </div>\n\n  <div class="rules">', new_panel + '<div class="rules">', s, count=1, flags=re.S)
assert s2 != s, "panel not replaced"
s = s2

# 3) 副标题
s = s.replace("排序默认<b>按评分从高到低</b>，可切换国内优先或使用人数。",
              "排序默认<b>国内优先 · 使用人数</b>，可切换为名称排序。")

# 4) 标题
s = s.replace("<title>AI 创作者平台导航 · 国内优先 · 规模与评分排序</title>",
              "<title>AI 创作者平台导航 · 国内优先 · 附 B 站测评证据</title>")

# 5) 统计与页脚
s = s.replace("按能力分 8 个模块共 221 条（跨模块重复计入）",
              "按能力分 8 个模块共 185 条（跨模块重复计入）")
old_footer = "评分（10 分制）由「模型能力 60%（语言理解 20% + 本模块任务能力 80%）+ 工作流与可靠性 25.6% + 性价比 8% + 证据与成熟度 6.4%」实时计算，属编辑估计，不是第三方评测排名；下方卡片里的第三方评价只作参考，不计入评分。"
new_footer = "本页不提供评分。每条卡片下方列出该平台近 2 个月在 B 站的测评视频，可逐条点开核查；无公开测评的平台已明确标注，不做分数推测。近 3 个月没有任何公开资讯的站点已从收录中移除。"
assert old_footer in s
s = s.replace(old_footer, new_footer)

# 6) 卡片里的“221”与计数初始化
s = s.replace("共 221 条", "共 185 条")

io.open(P, 'w', encoding='utf-8').write(s)
print("ok; 剩余 221 出现次数:", s.count("221"), "| 评分 出现次数:", s.count("评分"))

import io
s = io.open('index.html', encoding='utf-8').read()
inj = """<script>
setTimeout(function(){
  var g = document.querySelector('.grid');
  var out = document.createElement('pre');
  out.style.cssText = 'position:fixed;inset:0;background:#fff;z-index:99999;padding:12px;font:12px monospace;white-space:pre-wrap;margin:0;overflow:hidden';
  var first = g && g.children[0];
  out.textContent = 'grid children=' + (g ? g.children.length : 'none')
    + '\\nfirst tag=' + (first ? first.tagName + ' cls=' + first.className : 'none')
    + '\\nfirst rect=' + (first ? JSON.stringify(first.getBoundingClientRect()) : 'none')
    + '\\nfirst html=' + (first ? first.outerHTML.slice(0, 420) : 'none');
  document.body.appendChild(out);
}, 900);
</script>
</body>"""
io.open('_dbg3.html', 'w', encoding='utf-8').write(s.replace('</body>', inj))
print('ok')

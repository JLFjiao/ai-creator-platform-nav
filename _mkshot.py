import io
s = io.open('index.html', encoding='utf-8').read()
inj = """<script>
setTimeout(function(){
  var g = document.getElementById('groups');
  var box = document.createElement('div');
  box.style.cssText = 'position:fixed;top:0;left:0;background:#ff0;color:#000;padding:8px;z-index:99999;font:15px monospace';
  box.textContent = 'groups children=' + (g ? g.children.length : 'null')
    + ' | DATA=' + (typeof DATA !== 'undefined' ? DATA.length : 'undef')
    + ' | cards=' + document.querySelectorAll('.card').length
    + ' | err=' + (window.__err || 'none');
  document.body.appendChild(box);
}, 900);
window.addEventListener('error', function(e){ window.__err = e.message + ' @' + e.lineno; });
</script>
</body>"""
io.open('_dbg2.html', 'w', encoding='utf-8').write(s.replace('</body>', inj))
print('ok')

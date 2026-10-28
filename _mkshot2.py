import io
s = io.open('index.html', encoding='utf-8').read()
inj = """<script>
setTimeout(function(){
  ['header', '.toolbar'].forEach(function(sel){
    document.querySelectorAll(sel).forEach(function(e){ e.style.display = 'none'; });
  });
}, 500);
</script>
</body>"""
io.open('_shot.html', 'w', encoding='utf-8').write(s.replace('</body>', inj))
print('ok')

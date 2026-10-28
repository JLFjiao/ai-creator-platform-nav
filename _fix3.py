import io, re

P = 'index.html'
s = io.open(P, encoding='utf-8').read()

# 1) 清理数据里残留的旧字段 ev / main / tier
before_ev = s.count('ev:{')
before_main = s.count('main:')
s = re.sub(r",\s*ev:\{[^{}]*\}", "", s)
s = re.sub(r",\s*main:\d+", "", s)
s = re.sub(r",\s*tier:'[^']*'", "", s)
print('ev before/after:', before_ev, s.count('ev:{'), '| main before/after:', before_main, s.count('main:'))

# 2) 补回搜索与筛选函数（插在 sortRows 之前）
fn = '''// 归一化：统一小写，分隔符折成空格，保留词边界
function norm(s){
  return String(s).toLowerCase()
    .replace(/[\\-_.,·、()（）\\/]+/g,' ')
    .replace(/\\s+/g,' ')
    .trim();
}

// 编辑距离，用于英文名拼错时的容错
function lev(a,b){
  const m=a.length, n=b.length;
  if(Math.abs(m-n)>2) return 99;
  let prev=Array.from({length:n+1},(_,j)=>j), cur=new Array(n+1);
  for(let i=1;i<=m;i++){
    cur[0]=i;
    const ca=a.charCodeAt(i-1);
    for(let j=1;j<=n;j++){
      const cost = ca===b.charCodeAt(j-1) ? 0 : 1;
      cur[j]=Math.min(prev[j]+1, cur[j-1]+1, prev[j-1]+cost);
    }
    const t=prev; prev=cur; cur=t;
  }
  return prev[n];
}

function fuzzyHit(q, d){
  if(!/^[a-z0-9]+$/.test(q)) return false;
  const max = q.length >= 5 ? 2 : (q.length === 4 ? 1 : 0);
  if(!max) return false;
  const host = norm(d.u.replace(/^https?:\\/\\//,'').replace(/\\/.*$/,'').replace(/^www\\./,''));
  return [norm(d.n), host, norm(d.v)]
    .some(t => Math.abs(t.length - q.length) <= max && lev(q, t) <= max);
}

function match(d){
  if(state.favOnly && !favSet.has(d.n)) return false;
  if(state.cat !== 'all' && d.c !== state.cat) return false;
  if(state.region === 'cn' && d.co !== '中国') return false;
  if(state.region === 'global' && d.co === '中国') return false;
  if(state.price !== 'all' && d.p !== +state.price) return false;
  if(state.net !== 'all' && d.net !== +state.net) return false;
  const q = state.q.trim().toLowerCase();
  if(q){
    const catLabel = (CATS.find(c=>c.id===d.c)||{}).label || '';
    const fields = [d.n, d.v, d.co, d.d, d.t.join(' '), d.u, catLabel].map(norm);
    const terms = norm(q).split(' ').filter(Boolean);
    for(const term of terms){
      if(fields.some(f => f.includes(term))) continue;
      if(fuzzyHit(term, d)) continue;
      return false;
    }
  }
  return true;
}

'''
anchor = "function sortRows(list){"
assert anchor in s
s = s.replace(anchor, fn + anchor, 1)

io.open(P, 'w', encoding='utf-8').write(s)
print('written; match defs:', s.count('function match'))

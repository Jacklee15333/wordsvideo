"""配音稿里个别说法手改（总表某一格没写意思时，配音会念得别扭）：fixsay.py 文件夹名 原话 新话 [原话 新话 …]
改 ~/wordfilm-work/<文件夹名>/brief/plan.json（精简版）；手改过的稿子 run.py 不会覆盖。打印改了几处。"""
import sys, os
w = sys.argv[1]; pairs = list(zip(sys.argv[2::2], sys.argv[3::2]))
for f in ('brief/plan.json',):
    p = os.path.expanduser(f'~/wordfilm-work/{w}/{f}')
    if not os.path.exists(p): continue
    s = open(p, encoding='utf-8').read(); n = 0
    for a, b in pairs:
        n += s.count(a); s = s.replace(a, b)
    if n: open(p, 'w', encoding='utf-8').write(s)
    print(w, f, n)

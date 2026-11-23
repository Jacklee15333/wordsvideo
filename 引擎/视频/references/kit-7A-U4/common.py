"""各词共用的画法工具：原图 → bookstyle stylize；人物合成（人 + 手里的东西）"""
import os, sys, re, random, math, subprocess, json
SK = os.path.expanduser('~/skills/word-construction-video')
sys.path.insert(0, SK + '/scripts')
from poses import pose, LOOKS, motion_frames
INK = '#1B1A1F'
def lg(i, stops, x1=0, y1=0, x2=0, y2=1):
    return f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">' + ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops) + '</linearGradient>'
def svg(w, h, body, defs=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">' + (f'<defs>{defs}</defs>' if defs else '') + body + '</svg>'
def nshapes(s):
    return sum(s.count('<' + t) for t in ('path', 'rect', 'circle', 'ellipse', 'line', 'polygon', 'text'))
def stylize(raw, out, bg=False):
    cmd = ['python3', SK + '/scripts/bookstyle.py', 'stylize', raw, out] + (['--bg'] if bg else [])
    subprocess.run(cmd, check=True, capture_output=True)
def write_art(art, name, s, bg=False, style=True):
    os.makedirs(art + '/../raw', exist_ok=True); os.makedirs(art, exist_ok=True)
    raw = os.path.join(art, '..', 'raw', name)
    open(raw, 'w', encoding='utf-8').write(s)
    if style:
        stylize(raw, os.path.join(art, name), bg)
    else:
        open(os.path.join(art, name), 'w', encoding='utf-8').write(s)
    print('%-28s %4d 个图形' % (name, nshapes(s)))
def inner(svgtext):
    """取出 svg 的 viewBox 和里面的内容"""
    vb = re.search(r'viewBox="([^"]+)"', svgtext).group(1)
    body = re.sub(r'^.*?<svg[^>]*>', '', svgtext, count=1, flags=re.S)
    body = re.sub(r'</svg>\s*$', '', body)
    return vb, body
def nest(svgtext, x, y, w, h, uid=''):
    vb, body = inner(svgtext)
    if uid:  # 避免 id 撞车
        ids = set(re.findall(r'id="([^"]+)"', body))
        for i in ids:
            body = body.replace(f'id="{i}"', f'id="{i}{uid}"').replace(f'#{i})', f'#{i}{uid})').replace(f'"#{i}"', f'"#{i}{uid}"')
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{vb}" overflow="visible">{body}</svg>'
def person(who, **kw):
    d = dict(LOOKS[who]); d.update(kw); return pose(**d)
def holding(who, prop_svg, px, py, pw, ph, behind=False, **kw):
    """人（720×560 画布）手里拿着东西：东西画在 (px, py, pw, ph)，默认画在人前面"""
    p = person(who, **kw)
    vb, body = inner(p)
    pr = nest(prop_svg, px, py, pw, ph, uid='p')
    inside = (pr + body) if behind else (body + pr)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{inside}</svg>'
def frames_out(art, name, svgs, fps=None, seq='loop'):
    fns = []
    for i, s in enumerate(svgs):
        fn = f'{name}_f{i}.svg'
        open(os.path.join(art, fn), 'w', encoding='utf-8').write(s); fns.append(fn)
    return {'frames': fns, 'seq': seq, 'fps': fps or 2}

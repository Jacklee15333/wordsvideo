#!/usr/bin/env python3
"""图画书画风（6.22，参照用户的《七颗宝石》）：粗细变化的黑色勾线、饱和的平涂色块（可带一层柔和渐变）、
人物白净的鹅蛋脸、细长弯眼、一点红的小嘴、两颊粉色圆腮红、整块头发留几道白线；人物外面一圈淡淡的光晕。
场景照旧画得详细、具体（规矩 47），只是换成这种勾线平涂的画法。

  python3 bookstyle.py stylize 输入.svg 输出.svg [--bg]   # 已有的写实插图 → 图画书画风：加黑色勾线、颜色调饱和、去掉写实高光
  python3 bookstyle.py people <输出文件夹>                # 生成一套图画书画风的人物
"""
import os, re, sys, colorsys
import xml.etree.ElementTree as ET

INK = '#1B1A1F'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)

# ------------------------------------------------------------------ 颜色
def _hex(c):
    c = c.strip()
    if re.fullmatch(r'#[0-9a-fA-F]{3}', c):
        c = '#' + ''.join(ch * 2 for ch in c[1:])
    return c if re.fullmatch(r'#[0-9a-fA-F]{6}', c) else None

def vivid(c, k=1.5):
    """颜色调得更饱和、更亮一点（白、灰、黑不动）"""
    h = _hex(c)
    if not h:
        return c
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    hh, s, v = colorsys.rgb_to_hsv(r, g, b)
    if s < 0.1 or v < 0.12:
        return h
    s = min(1.0, s * k + 0.06)
    v = min(1.0, v * 1.06 + 0.02)
    r, g, b = colorsys.hsv_to_rgb(hh, s, v)
    return '#%02X%02X%02X' % (round(r * 255), round(g * 255), round(b * 255))

def _is_white(c):
    h = _hex(c or '')
    return bool(h) and all(int(h[i:i + 2], 16) > 236 for i in (1, 3, 5))

def _f(v, d=1.0):
    try:
        return float(v)
    except Exception:
        return d

def _size(el):
    """一个图形大概多大（viewBox 单位）：决定勾线粗细"""
    tag = el.tag.split('}')[-1]
    if tag == 'rect':
        return max(_f(el.get('width'), 0), _f(el.get('height'), 0))
    if tag == 'circle':
        return 2 * _f(el.get('r'), 0)
    if tag == 'ellipse':
        return 2 * max(_f(el.get('rx'), 0), _f(el.get('ry'), 0))
    nums = [float(x) for x in re.findall(r'-?\d+\.?\d*', el.get('d') or el.get('points') or '')]
    if len(nums) >= 4:
        xs, ys = nums[0::2], nums[1::2]
        return max(max(xs) - min(xs), max(ys) - min(ys))
    return 0

def stylize(src, dst, bg=False):
    tree = ET.parse(src)
    root = tree.getroot()
    vb = [float(x) for x in re.split(r'[\s,]+', root.get('viewBox').strip())]
    span = max(vb[2], vb[3])
    base = 3.4 if bg else span * 0.0125           # 背景：1200 宽画 3.4；单件东西按自己的大小
    import random
    rnd = random.Random(len(src))
    kv = 1.75 if bg else 1.5
    parent = {c: p for p in root.iter() for c in p}
    # 渐变里的颜色调饱和
    for st in root.iter('{%s}stop' % NS):
        if st.get('stop-color'):
            st.set('stop-color', vivid(st.get('stop-color'), 1.75 if bg else 1.5))
    drop = []
    for el in list(root.iter()):
        tag = el.tag.split('}')[-1]
        if tag not in ('path', 'rect', 'circle', 'ellipse', 'polygon', 'line', 'polyline'):
            continue
        fill = el.get('fill')
        stroke = el.get('stroke')
        op = min(_f(el.get('opacity'), 1), _f(el.get('fill-opacity'), 1))
        sop = _f(el.get('stroke-opacity'), 1)
        # 写实画法的白色高光、半透明的亮边：图画书里没有，去掉
        if (fill and _is_white(fill) and op < 0.7) or (stroke and _is_white(stroke) and sop < 0.7 and (not fill or fill == 'none')):
            drop.append(el)
            continue
        if fill and fill != 'none' and not fill.startswith('url'):
            el.set('fill', vivid(fill, kv))
        if stroke and stroke != 'none' and not stroke.startswith('url'):
            # 原来的深色线条换成墨线；浅色的（窗框、纸上的线）调饱和留着
            h = _hex(stroke)
            if h and sum(int(h[i:i + 2], 16) for i in (1, 3, 5)) < 300:
                el.set('stroke', INK)
            else:
                el.set('stroke', vivid(stroke))
            continue
        if not fill or fill == 'none' or op < 0.5:
            continue
        sz = _size(el)
        if sz < span * 0.004:
            continue
        w = base * (0.55 if sz < span * 0.04 else 1.0) * rnd.uniform(0.75, 1.35)
        el.set('stroke', INK)
        el.set('stroke-width', '%.2f' % w)
        el.set('stroke-linejoin', 'round')
        el.set('stroke-linecap', 'round')
    for el in drop:
        if el in parent:
            parent[el].remove(el)
    tree.write(dst, encoding='unicode')

# ------------------------------------------------------------------ 人物（腰部以上，viewBox 0 0 400 560，和写实人物同样的位置：嘴 y≈192、胸口 y≈332）
SKIN = {'pale': ('#FFF4EC', '#F6D9C8'), 'warm': ('#FBE3CC', '#EFC4A2'), 'tan': ('#E9B98E', '#D29A6C'), 'brown': ('#B9805A', '#9A6542')}
HAIR = {'black': ('#17161B', '#FFFFFF'), 'blond': ('#F6C93E', '#FFF2B0'), 'brown': ('#7A4A26', '#E9C49A'), 'red': ('#D9572B', '#FFD0A8')}

def _glow():
    return ('<filter id="bkGlow" x="-25%" y="-10%" width="150%" height="120%"><feMorphology in="SourceAlpha" operator="dilate" radius="5" result="d"/>'
            '<feGaussianBlur in="d" stdDeviation="6" result="b"/><feFlood flood-color="#7FD8F2" flood-opacity="0.75"/><feComposite in2="b" operator="in" result="g"/>'
            '<feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')

def taper(pts, w0, w1, fill=INK):
    """一笔有粗细变化的墨线：沿着折线两边各偏一点，头细（w0）尾细（w1）、中间粗"""
    import math
    n = len(pts)
    L, R = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]; b = pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        l = math.hypot(dx, dy) or 1
        t = i / (n - 1)
        w = (w0 + (w1 - w0) * t) * (0.35 + 2.2 * math.sin(math.pi * t)) / 2
        L.append((x - dy / l * w, y + dx / l * w)); R.append((x + dy / l * w, y - dx / l * w))
    p = L + R[::-1]
    return '<path d="M' + ' L'.join('%.1f,%.1f' % q for q in p) + ' Z" fill="%s"/>' % fill

def person(sex='f', hair='black', style='bun', skin='pale', top='#F2C230', collar='#25B5C9', sleeve=None, gesture='down', mouth='smile',
           eyes='open', freckles=False, glasses=False, tie=None, beard=False):
    sk, sk2 = SKIN[skin]
    hc, hl = HAIR[hair]
    sleeve = sleeve or top
    o = f'stroke="{INK}" stroke-linejoin="round" stroke-linecap="round"'
    s = f'<defs>{_glow()}<radialGradient id="bkBlush" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#F57FA6"/><stop offset="0.7" stop-color="#F79CBB" stop-opacity="0.9"/><stop offset="1" stop-color="#F9B3CB" stop-opacity="0"/></radialGradient>'
    s += f'<linearGradient id="bkTop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{vivid(top, 1.0)}"/><stop offset="1" stop-color="{vivid(top, 1.25)}"/></linearGradient></defs>'
    g = ''
    # 后面的头发（长发、马尾、卷发）
    if style in ('long', 'curly'):
        g += f'<path d="M200,52 C262,52 288,96 284,150 C282,196 292,236 298,266 C268,278 240,270 230,256 L170,256 C160,270 132,278 102,266 C108,236 118,196 116,150 C112,96 138,52 200,52 Z" fill="{hc}" {o} stroke-width="4"/>'
        if style == 'curly':
            for i in range(9):
                x = 108 + i * 23
                g += f'<path d="M{x},262 c-6,-14 10,-22 16,-10" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    if style == 'pony':
        g += f'<path d="M262,104 C300,120 306,176 294,232 C290,252 280,266 270,272 C276,236 278,176 254,138 Z" fill="{hc}" {o} stroke-width="4"/>'
    # 脖子、身子
    g += f'<path d="M180,198 L178,262 L222,262 L220,198 Z" fill="{sk2}" {o} stroke-width="3.5"/>'
    body = ('M90,560 L94,336 C96,298 116,276 150,266 L178,256 C188,270 212,270 222,256 L250,266 C284,276 304,298 306,336 L310,560 Z' if sex == 'f' else
            'M70,560 L74,332 C76,292 100,270 140,259 L176,250 C186,263 214,263 224,250 L260,259 C300,270 324,292 326,332 L330,560 Z')
    arm_r = (f'<path d="M{300 if sex == "m" else 286},286 C{322 if sex == "m" else 308},302 {332 if sex == "m" else 318},338 {334 if sex == "m" else 320},382 L{336 if sex == "m" else 322},560 L{300 if sex == "m" else 286},560 L{296 if sex == "m" else 282},392 C{294 if sex == "m" else 280},352 {290 if sex == "m" else 276},320 {282 if sex == "m" else 268},298 Z" fill="{sleeve}" {o} stroke-width="4"/>')
    g += arm_r
    if gesture != 'raise':
        xo = 0 if sex == 'm' else 14
        g += f'<path d="M{100 + xo},286 C{78 + xo},302 {68 + xo},338 {66 + xo},382 L{64 + xo},560 L{100 + xo},560 L{104 + xo},392 C{106 + xo},352 {110 + xo},320 {118 + xo},298 Z" fill="{sleeve}" {o} stroke-width="4"/>'
    g += f'<path d="{body}" fill="url(#bkTop)" {o} stroke-width="4.5"/>'
    # 领子：对比色的大领子（像图画书里的披肩领），男的可以打领带
    if sex == 'f':
        g += f'<path d="M150,268 C170,300 186,312 200,322 C214,312 230,300 250,268 L232,262 C220,286 210,296 200,300 C190,296 180,286 168,262 Z" fill="{collar}" {o} stroke-width="3.5"/>'
        g += f'<path d="M168,262 C180,286 190,296 200,300 C210,296 220,286 232,262 C212,272 188,272 168,262 Z" fill="{sk2}" {o} stroke-width="3"/>'
        g += f'<path d="M120,420 C160,432 240,432 280,420" fill="none" stroke="{vivid(collar, 1.2)}" stroke-width="10"/><path d="M120,420 C160,432 240,432 280,420" fill="none" {o} stroke-width="2"/>'
    else:
        g += f'<path d="M176,250 L200,350 L224,250 C214,263 186,263 176,250 Z" fill="#FFFFFF" {o} stroke-width="3"/>'
        if tie:
            g += f'<path d="M193,262 L207,262 L204,276 L196,276 Z" fill="{tie}" {o} stroke-width="2.5"/><path d="M196,276 L204,276 L211,340 L200,354 L189,340 Z" fill="{tie}" {o} stroke-width="2.5"/>'
        g += f'<path d="M174,251 L200,356 L184,358 L148,302 L166,288 L154,268 Z" fill="{collar}" {o} stroke-width="3.5"/><path d="M226,251 L200,356 L216,358 L252,302 L234,288 L246,268 Z" fill="{collar}" {o} stroke-width="3.5"/>'
        g += f'<circle cx="200" cy="420" r="6" fill="{INK}"/><circle cx="200" cy="476" r="6" fill="{INK}"/>'
    if gesture == 'raise':
        g += f'<path d="M104,284 C80,298 66,332 64,374 C63,396 66,412 72,424 L106,422 C102,400 104,370 112,342 C116,324 120,308 124,298 Z" fill="{sleeve}" {o} stroke-width="4"/>'
        g += f'<path d="M72,424 C62,402 52,374 44,348 L72,336 C80,362 92,394 106,422 Z" fill="{sleeve}" {o} stroke-width="4"/>'
        g += f'<path d="M40,340 C33,324 32,308 38,298 L44,294 L68,294 C72,306 72,320 66,330 Z" fill="{sk}" {o} stroke-width="3"/>'
        for x0, top_y in ((38, 256), (47, 248), (57, 252), (66, 262)):
            g += f'<path d="M{x0},296 C{x0 - 2},{top_y + 20} {x0 - 1},{top_y + 4} {x0 + 3},{top_y} C{x0 + 6},{top_y - 2} {x0 + 9},{top_y + 2} {x0 + 9},{top_y + 8} L{x0 + 9},296" fill="{sk}" {o} stroke-width="2.6"/>'
        g += f'<path d="M66,324 C74,320 82,312 88,302 C91,298 96,301 94,306 C90,318 82,328 70,336" fill="{sk}" {o} stroke-width="2.6"/>'
        g += f'<path d="M44,346 L72,334" {o} stroke-width="3" fill="none"/>'
    # 头：耳朵、鹅蛋脸
    for ex, sg in ((146, -1), (254, 1)):
        g += f'<path d="M{ex},{124} C{ex + 16 * sg},{116} {ex + 22 * sg},{138} {ex + 16 * sg},{154} C{ex + 12 * sg},{164} {ex + 4 * sg},{166} {ex - 2 * sg},{160} Z" fill="{sk}" {o} stroke-width="3"/>'
    g += f'<path d="M200,66 C234,66 256,92 256,130 C256,170 236,210 200,222 C164,210 144,170 144,130 C144,92 166,66 200,66 Z" fill="{sk}" {o} stroke-width="4"/>'
    # 腮红、五官
    g += '<circle cx="166" cy="168" r="17" fill="url(#bkBlush)"/><circle cx="234" cy="168" r="17" fill="url(#bkBlush)"/>'
    for cx, sg in ((176, -1), (224, 1)):
        g += f'<path d="M{cx - 15},{110} C{cx - 6},{102} {cx + 6},{102} {cx + 15},{108}" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>'
        if eyes == 'open':
            g += taper([(cx - 15, 135), (cx - 8, 128), (cx, 126), (cx + 8, 127), (cx + 15, 130), (cx + 20 * sg if sg > 0 else cx + 19, 126 if sg > 0 else 131)], 1.2, 2.0, INK)
            g += f'<path d="M{cx - 9},{131} C{cx - 5},{128} {cx + 5},{128} {cx + 9},{131} C{cx + 7},{138} {cx - 7},{138} {cx - 9},{131} Z" fill="{INK}"/>'
            g += f'<circle cx="{cx + 2 * sg}" cy="{131.5}" r="1.6" fill="#fff"/>'
            g += f'<path d="M{cx - 11},{139} C{cx - 4},{141} {cx + 4},{141} {cx + 10},{139}" fill="none" stroke="{INK}" stroke-width="1.2" opacity="0.55"/>'
        else:
            g += taper([(cx - 15, 131), (cx - 7, 138), (cx + 7, 138), (cx + 15, 131)], 1.2, 1.6, INK)
            g += f'<path d="M{cx + 14 * sg},{132} l{5 * sg},2" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>'
    g += f'<path d="M197,152 C196,160 196,164 199,166" fill="none" stroke="{sk2 if skin != "pale" else "#E7B9A0"}" stroke-width="3" stroke-linecap="round"/><path d="M197,152 C196,160 196,164 199,166" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round" opacity="0.6"/>'
    if mouth == 'open':
        g += f'<path d="M189,186 C194,182 206,182 211,186 C209,197 191,197 189,186 Z" fill="#E8304A" {o} stroke-width="2.2"/><path d="M193,191 C197,194 203,194 207,191" fill="none" stroke="#9E1530" stroke-width="2"/>'
    else:
        g += f'<path d="M191,186 C196,184 204,184 209,186 C206,192 194,192 191,186 Z" fill="#E8304A" {o} stroke-width="1.8"/>'
    if beard:
        g += f'<path d="M150,160 C152,196 172,222 200,226 C228,222 248,196 250,160 C244,176 236,188 226,196 C214,190 186,190 174,196 C164,188 156,176 150,160 Z" fill="{hc}" {o} stroke-width="3"/>'
        g += f'<path d="M186,182 C192,178 208,178 214,182 C206,186 194,186 186,182 Z" fill="{hc}" {o} stroke-width="2"/>'
    if freckles:
        for fx, fy in ((160, 160), (168, 156), (172, 164), (228, 156), (236, 160), (232, 164)):
            g += f'<circle cx="{fx}" cy="{fy}" r="1.8" fill="#B8643C"/>'
    if glasses:
        g += f'<circle cx="176" cy="136" r="17" fill="none" {o} stroke-width="3"/><circle cx="224" cy="136" r="17" fill="none" {o} stroke-width="3"/><path d="M193,134 L207,134" {o} stroke-width="3"/>'
    # 前面的头发
    if style == 'bun':                     # 黑发两个发髻（图画书里女孩的样子，现代一点）
        g += f'<circle cx="150" cy="70" r="26" fill="{hc}" {o} stroke-width="4"/><circle cx="250" cy="70" r="26" fill="{hc}" {o} stroke-width="4"/>'
        g += f'<rect x="138" y="88" width="20" height="9" rx="4" fill="#E8304A" {o} stroke-width="2"/><rect x="242" y="88" width="20" height="9" rx="4" fill="#E8304A" {o} stroke-width="2"/>'
    front = (f'<path d="M142,134 C134,84 162,52 202,52 C244,52 268,84 260,134 C252,112 244,100 232,94 C218,108 190,112 166,104 C156,110 148,120 142,134 Z" fill="{hc}" {o} stroke-width="4"/>' if sex == 'f' else
             f'<path d="M141,130 C134,82 160,48 204,47 C247,47 271,78 261,130 C258,108 251,94 238,88 C216,99 178,97 160,92 C150,102 145,114 141,130 Z" fill="{hc}" {o} stroke-width="4"/>')
    if style == 'afro':
        front = f'<path d="M136,138 C118,90 146,40 200,38 C254,40 282,90 264,138 C256,118 246,106 232,100 C214,108 186,108 168,100 C154,106 144,120 136,138 Z" fill="{hc}" {o} stroke-width="4"/>'
        for i in range(10):
            x = 146 + i * 12
            front += f'<circle cx="{x}" cy="{64 + (i % 3) * 7}" r="5" fill="none" stroke="#3A3A44" stroke-width="1.8"/>'
    if style == 'curly':
        front = f'<path d="M140,132 C128,96 146,58 200,52 C254,58 272,96 260,132 C250,112 240,104 226,100 C214,108 186,110 170,102 C158,108 148,118 140,132 Z" fill="{hc}" {o} stroke-width="4"/>'
        for i in range(8):
            x = 150 + i * 14
            front += f'<path d="M{x},{70 + (i % 2) * 8} c8,-8 18,2 10,10" fill="none" stroke="{INK}" stroke-width="2.4"/>'
    g += front
    for k, (x0, y0, x1, y1) in enumerate(((168, 70, 214, 62), (182, 86, 236, 78), (230, 70, 250, 96))):
        g += f'<path d="M{x0},{y0} Q{(x0 + x1) / 2},{min(y0, y1) - 8} {x1},{y1}" fill="none" stroke="{hl}" stroke-width="2.6" stroke-linecap="round" opacity="0.9"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 560">{s}<g filter="url(#bkGlow)">{g}</g></svg>'

# 6.22：人物中外结合（用户：“人物，环境，建筑，物件这些要中国和欧美相结合，不要全是中国人，也不要全是外国人”）。
# 文件名前缀 cn- / west- 标明是中国人还是欧美人，draft_plan.js 据此检查一个词的画里两种人都有
CAST = {
    'cn-teacher-talk': dict(sex='f', hair='black', style='bun', top='#F2C230', collar='#25B5C9', sleeve='#F2C230', gesture='raise', mouth='open'),
    'cn-teacher-say': dict(sex='f', hair='black', style='bun', top='#F2C230', collar='#25B5C9', gesture='down', mouth='open'),
    'cn-teacher-calm': dict(sex='f', hair='black', style='bun', top='#F2C230', collar='#25B5C9', gesture='down', mouth='smile'),
    'cn-boy-smile': dict(sex='m', hair='black', style='short', top='#2E6FD9', collar='#FFFFFF', gesture='down', mouth='smile'),
    'cn-boy-talk': dict(sex='m', hair='black', style='short', top='#2E6FD9', collar='#FFFFFF', gesture='raise', mouth='open'),
    'cn-girl-smile': dict(sex='f', hair='black', style='pony', top='#E8407A', collar='#FFFFFF', gesture='down', mouth='smile'),
    'west-man-talk': dict(sex='m', hair='brown', style='short', skin='pale', top='#2D4E8F', collar='#3E6FC4', sleeve='#2D4E8F', gesture='raise', mouth='open', tie='#E2342D', beard=True),
    'west-man-calm': dict(sex='m', hair='brown', style='short', skin='pale', top='#2D4E8F', collar='#3E6FC4', gesture='down', mouth='smile', tie='#E2342D', beard=True),
    'west-girl-smile': dict(sex='f', hair='red', style='curly', skin='warm', top='#3E8FE0', collar='#F2C230', gesture='down', mouth='smile', freckles=True),
    'west-girl-talk': dict(sex='f', hair='red', style='curly', skin='warm', top='#3E8FE0', collar='#F2C230', gesture='down', mouth='open', freckles=True),
    'west-woman-smile': dict(sex='f', hair='blond', style='long', skin='pale', top='#E8407A', collar='#FFFFFF', gesture='down', mouth='smile'),
    'west-boy-smile': dict(sex='m', hair='black', style='afro', skin='brown', top='#F28C28', collar='#25B5C9', gesture='down', mouth='smile'),
    'west-clerk': dict(sex='m', hair='brown', style='short', skin='warm', top='#5E7D3A', collar='#E8C25A', gesture='down', mouth='smile', eyes='down', glasses=True, tie='#C0392B'),
}

if __name__ == '__main__':
    if len(sys.argv) >= 4 and sys.argv[1] == 'stylize':
        stylize(sys.argv[2], sys.argv[3], bg='--bg' in sys.argv)
    elif len(sys.argv) >= 3 and sys.argv[1] == 'people':
        os.makedirs(sys.argv[2], exist_ok=True)
        for n, spec in CAST.items():
            open(os.path.join(sys.argv[2], n + '.svg'), 'w', encoding='utf-8').write(person(**spec))
        print('人物：' + '、'.join(CAST))
    else:
        print(__doc__)

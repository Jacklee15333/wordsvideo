#!/usr/bin/env python3
"""6.24：图画书画风人物的动作、表情（用户：“人物的动作，表情很单一，几个画面都是一样，姿势，手势都一样……
也可以做一些动图，不一定都要静态的图”）。

pose(...) 画一个人：胳膊是两节“管子”（肩 → 肘 → 腕，角度、长短随便摆），手有张开、指、握拳、竖大拇指、托下巴几种；
表情有眼睛（弯月 / 笑眯眯 / 睁大 / 闭眼 / 往旁边看）、眉毛（平 / 扬起 / 皱 / 一边挑）、嘴（微笑 / 说话 / 半张 / 大笑 / 圆嘴 / 抿嘴）、
头可以歪。动图：同一个人画几帧（嘴一张一合、手挥来挥去、头左右晃），prefs 里写 "frames": [...]，按 fps 轮着放。

  python3 poses.py <输出文件夹>      # 生成 ACTIONS 里的一套（含动图的帧：xxx_f0.svg、xxx_f1.svg…）
"""
import math, os, sys
from bookstyle import INK, SKIN, HAIR, vivid, taper, _glow

ARM = {   # 常用胳膊姿势：(上臂角度, 上臂长, 前臂角度, 前臂长, 手)；角度从“垂直往下”算，往外为正，>180 是举过头往里
    'down':    (8, 112, 4, 104, 'none'),
    'hello':   (32, 104, 168, 96, 'open'),
    'wave1':   (36, 104, 150, 96, 'open'),
    'wave2':   (36, 104, 190, 96, 'open'),
    'point':   (72, 108, 92, 100, 'point'),      # 往旁边指
    'pointup': (58, 104, 140, 100, 'point'),     # 往斜上方指（指黑板、指屏幕）
    'present': (34, 106, 104, 96, 'open'),       # 两手摊开讲解
    'present2': (40, 106, 118, 96, 'open'),
    'presentHi': (48, 100, 130, 92, 'open'),     # 两手摊开、举高一点（站在讲台后面也看得见）
    'chin':    (-6, 72, 205, 140, 'fist'),       # 托下巴想事
    'thumb':   (20, 100, 120, 90, 'thumb'),
    'raise':   (12, 112, 178, 104, 'open'),      # 举手发言
    'chest':   (6, 96, 112, 86, 'fist'),         # 手放胸前
}

def _v(theta, side):
    t = math.radians(theta)
    return (side * math.sin(t), math.cos(t))

def _tube(pts, w, col):
    d = 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 8}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

def _hand(W, d, kind, sk):
    if kind == 'none':
        return f'<circle cx="{W[0] + d[0] * 8:.1f}" cy="{W[1] + d[1] * 8:.1f}" r="14" fill="{sk}" stroke="{INK}" stroke-width="3"/>'
    C = (W[0] + d[0] * 14, W[1] + d[1] * 14)
    out = ''
    ang = math.atan2(d[1], d[0])
    fing = lambda a, L, w=9: _tube([(C[0] + math.cos(a) * 10, C[1] + math.sin(a) * 10), (C[0] + math.cos(a) * (10 + L), C[1] + math.sin(a) * (10 + L))], w - 4, sk)
    if kind == 'open':
        for k in (-0.5, -0.17, 0.17, 0.5):
            out += fing(ang + k, 18)
        out += fing(ang + 1.25, 13)
        out += f'<circle cx="{C[0]:.1f}" cy="{C[1]:.1f}" r="16" fill="{sk}" stroke="{INK}" stroke-width="3"/>'
    elif kind == 'point':
        out += fing(ang, 30)
        out += f'<circle cx="{C[0]:.1f}" cy="{C[1]:.1f}" r="14" fill="{sk}" stroke="{INK}" stroke-width="3"/>'
        out += f'<path d="M{C[0] - d[1] * 6:.1f},{C[1] + d[0] * 6:.1f} l{d[0] * 6:.1f},{d[1] * 6:.1f}" stroke="{INK}" stroke-width="2"/>'
    elif kind == 'thumb':
        out += _tube([(C[0], C[1] - 8), (C[0], C[1] - 30)], 6, sk)
        out += f'<circle cx="{C[0]:.1f}" cy="{C[1]:.1f}" r="15" fill="{sk}" stroke="{INK}" stroke-width="3"/>'
    else:  # fist
        out += f'<circle cx="{C[0]:.1f}" cy="{C[1]:.1f}" r="15" fill="{sk}" stroke="{INK}" stroke-width="3"/>'
        for k in (-5, 0, 5):
            out += f'<path d="M{C[0] + k:.1f},{C[1] - 9:.1f} l0,7" stroke="{INK}" stroke-width="1.6"/>'
    return out

def _arm(spec, side, shoulder, col, sk):
    a1, l1, a2, l2, hand = ARM[spec] if isinstance(spec, str) else spec
    S = shoulder
    v1, v2 = _v(a1, side), _v(a2, side)
    E = (S[0] + v1[0] * l1, S[1] + v1[1] * l1)
    Wr = (E[0] + v2[0] * l2, E[1] + v2[1] * l2)
    s = _tube([S, E, Wr], 32, col)
    s += f'<path d="M{Wr[0] - v2[1] * 15:.1f},{Wr[1] + v2[0] * 15 * side:.1f} L{Wr[0] + v2[1] * 15:.1f},{Wr[1] - v2[0] * 15 * side:.1f}" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>'
    s += _hand(Wr, v2, hand, sk)
    behind = a1 < 25 and (a2 < 45 or hand == 'none')
    return s, behind

def _eyes(kind, look):
    g = ''
    for cx, sg in ((176, -1), (224, 1)):
        px = cx + look * 4
        if kind == 'open':
            g += taper([(cx - 15, 135), (cx - 8, 128), (cx, 126), (cx + 8, 127), (cx + 15, 130), (cx + 19 if sg > 0 else cx + 19, 126 if sg > 0 else 131)], 1.2, 2.0, INK)
            g += f'<path d="M{px - 9},131 C{px - 5},128 {px + 5},128 {px + 9},131 C{px + 7},138 {px - 7},138 {px - 9},131 Z" fill="{INK}"/><circle cx="{px + 2}" cy="131.5" r="1.6" fill="#fff"/>'
        elif kind == 'happy':
            g += taper([(cx - 14, 136), (cx - 7, 128), (cx + 7, 128), (cx + 14, 136)], 1.4, 1.4, INK)
        elif kind == 'wide':
            g += f'<ellipse cx="{cx}" cy="132" rx="11" ry="12" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/><circle cx="{px}" cy="133" r="6" fill="{INK}"/><circle cx="{px + 2}" cy="130.5" r="1.8" fill="#fff"/>'
        else:  # closed
            g += taper([(cx - 15, 131), (cx - 7, 138), (cx + 7, 138), (cx + 15, 131)], 1.2, 1.6, INK)
    return g

def _brows(kind):
    g = ''
    for cx, sg in ((176, -1), (224, 1)):
        if kind == 'up' or (kind == 'one' and sg > 0):
            g += f'<path d="M{cx - 15},104 C{cx - 6},92 {cx + 6},92 {cx + 15},100" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>'
        elif kind == 'frown':
            inner = cx + 15 * (-sg)
            g += f'<path d="M{cx - 15},{108 if sg > 0 else 114} L{cx + 15},{114 if sg > 0 else 108}" fill="none" stroke="{INK}" stroke-width="2.8" stroke-linecap="round"/>'
        else:
            g += f'<path d="M{cx - 15},110 C{cx - 6},102 {cx + 6},102 {cx + 15},108" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>'
    return g

def _mouth(kind):
    o = f'stroke="{INK}" stroke-linejoin="round"'
    if kind == 'open':
        return f'<path d="M189,185 C194,181 206,181 211,185 C209,198 191,198 189,185 Z" fill="#E8304A" {o} stroke-width="2.2"/><path d="M193,191 C197,194 203,194 207,191" fill="none" stroke="#9E1530" stroke-width="2"/>'
    if kind == 'half':
        return f'<path d="M190,186 C195,183 205,183 210,186 C208,192 192,192 190,186 Z" fill="#E8304A" {o} stroke-width="2"/>'
    if kind == 'laugh':
        return (f'<path d="M183,182 C192,186 208,186 217,182 C215,202 185,202 183,182 Z" fill="#B3122E" {o} stroke-width="2.4"/>'
                f'<path d="M185,183 C194,187 206,187 215,183 L214,188 C204,191 196,191 186,188 Z" fill="#FFFFFF"/><path d="M191,196 C196,192 204,192 209,196 C204,199 196,199 191,196 Z" fill="#F07A8E"/>')
    if kind == 'o':
        return f'<ellipse cx="200" cy="189" rx="7" ry="9" fill="#B3122E" {o} stroke-width="2.2"/>'
    if kind == 'flat':
        return f'<path d="M192,188 L208,188" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>'
    return f'<path d="M191,186 C196,184 204,184 209,186 C206,192 194,192 191,186 Z" fill="#E8304A" {o} stroke-width="1.8"/>'

def pose(sex='f', hair='black', style='bun', skin='pale', top='#F2C230', collar='#25B5C9', sleeve=None,
         left='down', right='down', eyes='open', look=0, brows='normal', mouth='smile', tilt=0,
         freckles=False, glasses=False, tie=None, beard=False, blush=1.0):
    """left / right：观众看来左边、右边那只胳膊的姿势（ARM 里的名字，或者自己写 (上臂角, 上臂长, 前臂角, 前臂长, 手)）"""
    sk, sk2 = SKIN[skin]
    hc, hl = HAIR[hair]
    sleeve = sleeve or top
    o = f'stroke="{INK}" stroke-linejoin="round" stroke-linecap="round"'
    defs = (f'<defs>{_glow()}<radialGradient id="bkBlush" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#F57FA6"/><stop offset="0.7" stop-color="#F79CBB" stop-opacity="0.9"/><stop offset="1" stop-color="#F9B3CB" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="bkTop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{vivid(top, 1.0)}"/><stop offset="1" stop-color="{vivid(top, 1.25)}"/></linearGradient></defs>')
    rot = f'rotate({tilt} 200 222)'
    back = ''
    if style in ('long', 'curly'):
        back += f'<path d="M200,52 C262,52 288,96 284,150 C282,196 292,236 298,266 C268,278 240,270 230,256 L170,256 C160,270 132,278 102,266 C108,236 118,196 116,150 C112,96 138,52 200,52 Z" fill="{hc}" {o} stroke-width="4"/>'
        if style == 'curly':
            back += ''.join(f'<path d="M{108 + i * 23},262 c-6,-14 10,-22 16,-10" fill="none" stroke="{INK}" stroke-width="2.5"/>' for i in range(9))
    if style == 'pony':
        back += f'<path d="M262,104 C300,120 306,176 294,232 C290,252 280,266 270,272 C276,236 278,176 254,138 Z" fill="{hc}" {o} stroke-width="4"/>'
    neck = f'<path d="M180,198 L178,262 L222,262 L220,198 Z" fill="{sk2}" {o} stroke-width="3.5"/>'
    body = ('M90,560 L94,336 C96,298 116,276 150,266 L178,256 C188,270 212,270 222,256 L250,266 C284,276 304,298 306,336 L310,560 Z' if sex == 'f' else
            'M70,560 L74,332 C76,292 100,270 140,259 L176,250 C186,263 214,263 224,250 L260,259 C300,270 324,292 326,332 L330,560 Z')
    torso = f'<path d="{body}" fill="url(#bkTop)" {o} stroke-width="4.5"/>'
    if sex == 'f':
        torso += f'<path d="M150,268 C170,300 186,312 200,322 C214,312 230,300 250,268 L232,262 C220,286 210,296 200,300 C190,296 180,286 168,262 Z" fill="{collar}" {o} stroke-width="3.5"/>'
        torso += f'<path d="M168,262 C180,286 190,296 200,300 C210,296 220,286 232,262 C212,272 188,272 168,262 Z" fill="{sk2}" {o} stroke-width="3"/>'
        torso += f'<path d="M120,420 C160,432 240,432 280,420" fill="none" stroke="{vivid(collar, 1.2)}" stroke-width="10"/><path d="M120,420 C160,432 240,432 280,420" fill="none" {o} stroke-width="2"/>'
        shL, shR = (128, 292), (272, 292)
    else:
        torso += f'<path d="M176,250 L200,350 L224,250 C214,263 186,263 176,250 Z" fill="#FFFFFF" {o} stroke-width="3"/>'
        if tie:
            torso += f'<path d="M193,262 L207,262 L204,276 L196,276 Z" fill="{tie}" {o} stroke-width="2.5"/><path d="M196,276 L204,276 L211,340 L200,354 L189,340 Z" fill="{tie}" {o} stroke-width="2.5"/>'
        torso += f'<path d="M174,251 L200,356 L184,358 L148,302 L166,288 L154,268 Z" fill="{collar}" {o} stroke-width="3.5"/><path d="M226,251 L200,356 L216,358 L252,302 L234,288 L246,268 Z" fill="{collar}" {o} stroke-width="3.5"/>'
        torso += f'<circle cx="200" cy="420" r="6" fill="{INK}"/><circle cx="200" cy="476" r="6" fill="{INK}"/>'
        shL, shR = (112, 290), (288, 290)
    aL, bL = _arm(left, -1, shL, sleeve, sk)
    aR, bR = _arm(right, 1, shR, sleeve, sk)
    # 头
    head = ''
    for ex, sg in ((146, -1), (254, 1)):
        head += f'<path d="M{ex},124 C{ex + 16 * sg},116 {ex + 22 * sg},138 {ex + 16 * sg},154 C{ex + 12 * sg},164 {ex + 4 * sg},166 {ex - 2 * sg},160 Z" fill="{sk}" {o} stroke-width="3"/>'
    head += f'<path d="M200,66 C234,66 256,92 256,130 C256,170 236,210 200,222 C164,210 144,170 144,130 C144,92 166,66 200,66 Z" fill="{sk}" {o} stroke-width="4"/>'
    r = 17 * blush
    head += f'<circle cx="166" cy="168" r="{r:.1f}" fill="url(#bkBlush)"/><circle cx="234" cy="168" r="{r:.1f}" fill="url(#bkBlush)"/>'
    head += _brows(brows) + _eyes(eyes, look)
    head += f'<path d="M197,152 C196,160 196,164 199,166" fill="none" stroke="#E7B9A0" stroke-width="3" stroke-linecap="round"/><path d="M197,152 C196,160 196,164 199,166" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round" opacity="0.6"/>'
    head += _mouth(mouth)
    if beard:
        head += f'<path d="M150,160 C152,196 172,222 200,226 C228,222 248,196 250,160 C244,176 236,188 226,196 C214,190 186,190 174,196 C164,188 156,176 150,160 Z" fill="{hc}" {o} stroke-width="3"/>'
        head += _mouth(mouth)
    if freckles:
        head += ''.join(f'<circle cx="{fx}" cy="{fy}" r="1.8" fill="#B8643C"/>' for fx, fy in ((160, 160), (168, 156), (172, 164), (228, 156), (236, 160), (232, 164)))
    if glasses:
        head += f'<circle cx="176" cy="134" r="17" fill="none" {o} stroke-width="3"/><circle cx="224" cy="134" r="17" fill="none" {o} stroke-width="3"/><path d="M193,132 L207,132" {o} stroke-width="3"/>'
    if style == 'bun':
        head += f'<circle cx="150" cy="70" r="26" fill="{hc}" {o} stroke-width="4"/><circle cx="250" cy="70" r="26" fill="{hc}" {o} stroke-width="4"/>'
        head += f'<rect x="138" y="88" width="20" height="9" rx="4" fill="#E8304A" {o} stroke-width="2"/><rect x="242" y="88" width="20" height="9" rx="4" fill="#E8304A" {o} stroke-width="2"/>'
    if style == 'curly':
        front = f'<path d="M140,132 C128,96 146,58 200,52 C254,58 272,96 260,132 C250,112 240,104 226,100 C214,108 186,110 170,102 C158,108 148,118 140,132 Z" fill="{hc}" {o} stroke-width="4"/>'
        front += ''.join(f'<path d="M{150 + i * 14},{70 + (i % 2) * 8} c8,-8 18,2 10,10" fill="none" stroke="{INK}" stroke-width="2.4"/>' for i in range(8))
    elif style == 'afro':
        front = f'<path d="M136,138 C118,90 146,40 200,38 C254,40 282,90 264,138 C256,118 246,106 232,100 C214,108 186,108 168,100 C154,106 144,120 136,138 Z" fill="{hc}" {o} stroke-width="4"/>'
    elif sex == 'f':
        front = f'<path d="M142,134 C134,84 162,52 202,52 C244,52 268,84 260,134 C252,112 244,100 232,94 C218,108 190,112 166,104 C156,110 148,120 142,134 Z" fill="{hc}" {o} stroke-width="4"/>'
    else:
        front = f'<path d="M141,130 C134,82 160,48 204,47 C247,47 271,78 261,130 C258,108 251,94 238,88 C216,99 178,97 160,92 C150,102 145,114 141,130 Z" fill="{hc}" {o} stroke-width="4"/>'
    head += front
    head += ''.join(f'<path d="M{x0},{y0} Q{(x0 + x1) / 2},{min(y0, y1) - 8} {x1},{y1}" fill="none" stroke="{hl}" stroke-width="2.6" stroke-linecap="round" opacity="0.9"/>'
                    for x0, y0, x1, y1 in ((168, 70, 214, 62), (182, 86, 236, 78), (230, 70, 250, 96)))
    g = f'<g transform="{rot}">{back}</g>'
    g += (aL if bL else '') + (aR if bR else '')
    g += neck + torso
    g += f'<g transform="{rot}">{head}</g>'
    g += ('' if bL else aL) + ('' if bR else aR)
    # 画布左右各留 160（胳膊伸直、指出去的手都在画里）：viewBox 0 0 720 560，人在中间（以前 0 0 400 560 的 x 加 160；嘴在 360, 192，胸口 y≈332）
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 560">{defs}<g transform="translate(160 0)"><g filter="url(#bkGlow)">{g}</g></g></svg>'

# 人物（中外结合，规矩 48）的长相
LOOKS = {
    'cn-teacher': dict(sex='f', hair='black', style='bun', top='#F2C230', collar='#25B5C9'),
    'cn-boy': dict(sex='m', hair='black', style='short', top='#2E6FD9', collar='#FFFFFF'),
    'cn-girl': dict(sex='f', hair='black', style='pony', top='#E8407A', collar='#FFFFFF'),
    'west-man': dict(sex='m', hair='brown', style='short', skin='pale', top='#2D4E8F', collar='#3E6FC4', tie='#E2342D', beard=True),
    'west-girl': dict(sex='f', hair='red', style='curly', skin='warm', top='#3E8FE0', collar='#F2C230', freckles=True),
    'west-woman': dict(sex='f', hair='blond', style='long', skin='pale', top='#E8407A', collar='#FFFFFF'),
    'west-boy': dict(sex='m', hair='black', style='afro', skin='brown', top='#F28C28', collar='#25B5C9'),
    'west-clerk': dict(sex='m', hair='brown', style='short', skin='warm', top='#5E7D3A', collar='#E8C25A', glasses=True, tie='#C0392B'),
}

# 动作、表情（同一个人在不同画面里换着用）；列表 = 动图的几帧
ACTIONS = {
    'cn-teacher-point':   [dict(right='pointup', left='down', mouth='open', brows='up', look=1), dict(right='pointup', left='down', mouth='half', brows='up', look=1)],
    'cn-teacher-listen':  [dict(left='chest', right='down', mouth='smile', eyes='open', look=1, tilt=-6)],
    'cn-teacher-laugh':   [dict(left='down', right='down', mouth='laugh', eyes='happy', tilt=5, blush=1.2)],
    'cn-boy-raise':       [dict(right='raise', mouth='open', eyes='wide', brows='up'), dict(right='raise', mouth='half', eyes='wide', brows='up')],
    'west-girl-listen':   [dict(mouth='smile', eyes='open', look=-1, tilt=6)],
    'west-girl-raise':    [dict(left='raise', mouth='open', eyes='open', brows='up'), dict(left='raise', mouth='half', eyes='open', brows='up')],
    'west-girl-explain':  [dict(left='present', right='present', mouth='open', brows='up', tilt=-3), dict(left='present2', right='present2', mouth='half', brows='up', tilt=2)],
    'west-girl-music':    [dict(mouth='laugh', eyes='happy', tilt=-7, right='thumb'), dict(mouth='smile', eyes='happy', tilt=0, right='thumb'),
                           dict(mouth='laugh', eyes='happy', tilt=7, right='thumb'), dict(mouth='smile', eyes='happy', tilt=0, right='thumb')],
    'west-girl-surprised': [dict(mouth='o', eyes='wide', brows='up', left='chest')],
    'west-man-hello':     [dict(left='hello', mouth='open', brows='up'), dict(left='wave2', mouth='half', brows='up')],
    'west-man-present':   [dict(left='presentHi', right='presentHi', mouth='open', brows='up'), dict(left='presentHi', right='presentHi', mouth='half', brows='normal', tilt=3)],
    'west-man-speech':    [dict(left='pointup', mouth='open', brows='up', look=-1), dict(left='pointup', mouth='half', brows='normal', look=-1)],
    'west-man-point':     [dict(right='point', mouth='open', look=1, brows='up'), dict(right='point', mouth='half', look=1, brows='up')],
    'west-man-smile':     [dict(left='chest', mouth='smile', eyes='happy', tilt=-4)],
    'west-clerk-think':   [dict(right='chin', mouth='flat', eyes='open', look=-1, brows='one', tilt=-5)],
    'west-clerk-happy':   [dict(left='thumb', mouth='laugh', eyes='happy', tilt=4)],
}


# ===================== 6.25（第六十二版）：画里的人真的动起来 =====================
# 用户：“我希望图片里面要有适当的动图，比如 speaker 画的是人在演讲，那么可以让人物动起来，嘴巴讲起来这样的；
# 大喇叭也是一样，可以画一下音波这样的，周围有人的话，可以画人在走动。总之要是动态的图；这里不是只改 speaker 一个，其他的单词也要做这样的优化”
#   - 说话（seq talk）：几个关键手势之间插过渡帧（胳膊慢慢抬起、放下，头轻轻歪），每个手势配 3 种嘴型（闭、半张、张开）。
#     画的时候手势来回慢慢动，嘴像说话一样一张一合、说一句停一下（wordfilm.js frameIndex）。
#   - 听、想（seq blink）：慢慢歪头 / 眼睛往两边看，隔三秒左右眨一下眼。
#   - 笑、跟着音乐摇头（seq pingpong / loop）。
#   - 走路的人（walker）：全身、侧着往右走，腿一前一后、胳膊前后摆，可以拖行李箱、背书包；往左走时画面自动翻过来。

def lerp_arm(a, b, t):
    A = ARM[a] if isinstance(a, str) else tuple(a)
    B = ARM[b] if isinstance(b, str) else tuple(b)
    return tuple(A[i] + (B[i] - A[i]) * t for i in range(4)) + ((A[4] if t < 0.5 else B[4]),)


def gesture_steps(keys, steps=2):
    """几个关键手势 [{left, right, tilt, look, …}, …] 之间各插 steps 帧过渡，胳膊、头慢慢动过去"""
    if len(keys) == 1:
        return [dict(keys[0])]
    out = []
    for k in range(len(keys) - 1):
        a, b = keys[k], keys[k + 1]
        for j in range(steps + 1):
            t = j / (steps + 1)
            g = dict(a if t < 0.5 else b)
            for side in ('left', 'right'):
                if side in a or side in b:
                    g[side] = lerp_arm(a.get(side, 'down'), b.get(side, 'down'), t)
            for num in ('tilt', 'look'):
                if num in a or num in b:
                    g[num] = a.get(num, 0) + (b.get(num, 0) - a.get(num, 0)) * t
            out.append(g)
    out.append(dict(keys[-1]))
    return out


TALK_MOUTHS = ('smile', 'half', 'open')

# 每个动作怎么动：kind = talk（说话）/ blink（听、想：慢慢动 + 眨眼）/ pingpong（来回）/ loop（循环）
MOTIONS = {
    'cn-teacher-point':  dict(kind='talk', keys=[dict(right='pointup', left='down', brows='up', look=1, tilt=-2),
                                                 dict(right=(64, 104, 118, 100, 'point'), left='chest', brows='up', look=1, tilt=3)]),
    'cn-teacher-listen': dict(kind='blink', fps=1.2, keys=[dict(left='chest', right='down', mouth='smile', look=1, tilt=-6),
                                                           dict(left='chest', right='down', mouth='smile', look=1, tilt=0)]),
    'cn-teacher-laugh':  dict(kind='pingpong', fps=5, frames=[dict(mouth='laugh', eyes='happy', tilt=4, blush=1.2),
                                                              dict(mouth='laugh', eyes='happy', tilt=7, blush=1.25, left=(12, 112, 10, 104, 'none')),
                                                              dict(mouth='open', eyes='happy', tilt=2, blush=1.2)]),
    'cn-boy-raise':      dict(kind='talk', keys=[dict(right='raise', eyes='wide', brows='up'), dict(right=(16, 112, 190, 104, 'open'), eyes='wide', brows='up', tilt=3)]),
    'west-girl-listen':  dict(kind='blink', fps=1.2, keys=[dict(mouth='smile', look=-1, tilt=7), dict(mouth='smile', look=-1, tilt=1)]),
    'west-girl-raise':   dict(kind='talk', keys=[dict(left='raise', brows='up'), dict(left=(18, 112, 192, 104, 'open'), brows='up', tilt=-3)]),
    'west-girl-explain': dict(kind='talk', keys=[dict(left='present', right='present', brows='up', tilt=-3),
                                                 dict(left='present2', right='presentHi', brows='up', tilt=3)]),
    'west-girl-music':   dict(kind='loop', fps=2.5, frames=[dict(mouth='laugh', eyes='happy', tilt=-7, right='thumb'), dict(mouth='smile', eyes='happy', tilt=0, right='thumb'),
                                                            dict(mouth='laugh', eyes='happy', tilt=7, right='thumb'), dict(mouth='smile', eyes='happy', tilt=0, right='thumb')]),
    'west-girl-surprised': dict(kind='blink', fps=1.0, keys=[dict(mouth='o', eyes='wide', brows='up', left='chest', tilt=-2), dict(mouth='o', eyes='wide', brows='up', left='chest', tilt=2)]),
    'west-man-hello':    dict(kind='talk', gfps=4.5, keys=[dict(left='wave1', brows='up'), dict(left='wave2', brows='up', tilt=2)]),
    'west-man-present':  dict(kind='talk', keys=[dict(left='presentHi', right='presentHi', brows='up'), dict(left='present', right='present2', tilt=3)]),
    'west-man-speech':   dict(kind='talk', keys=[dict(left='pointup', right='down', brows='up', look=-1, tilt=-2),
                                                 dict(left=(48, 104, 112, 100, 'point'), right='chest', look=-1, tilt=2)]),
    'west-man-point':    dict(kind='talk', keys=[dict(right='point', look=1, brows='up'), dict(right=(68, 108, 78, 100, 'point'), left='present', look=1, tilt=2)]),
    'west-man-smile':    dict(kind='blink', fps=1.0, keys=[dict(left='chest', mouth='smile', eyes='happy', tilt=-4), dict(left='chest', mouth='smile', eyes='happy', tilt=1)]),
    'west-clerk-think':  dict(kind='blink', fps=0.8, keys=[dict(right='chin', mouth='flat', look=-1, brows='one', tilt=-5), dict(right='chin', mouth='flat', look=1, brows='one', tilt=-2)]),
    'west-clerk-happy':  dict(kind='pingpong', fps=3, frames=[dict(left='thumb', mouth='laugh', eyes='happy', tilt=4), dict(left='thumb', mouth='smile', eyes='happy', tilt=-1)]),
}


def motion_frames(name, spec=None):
    """一个动作的几帧 → ([svg, …], 放法)。放法写进 prefs：seq、fps、mouths、gfps"""
    spec = spec or MOTIONS[name]
    who = name.split('-')[0] + '-' + name.split('-')[1]
    base = dict(LOOKS[who])
    kind = spec['kind']
    out = []
    if kind == 'talk':
        for g in gesture_steps(spec['keys'], spec.get('steps', 2)):
            for m in spec.get('mouths', TALK_MOUTHS):
                d = dict(base); d.update(g); d['mouth'] = m
                out.append(pose(**d))
        return out, {'seq': 'talk', 'mouths': len(spec.get('mouths', TALK_MOUTHS)), 'gfps': spec.get('gfps', 2.6), 'mfps': spec.get('mfps', 8)}
    if kind == 'blink':
        gs = gesture_steps(spec['keys'], spec.get('steps', 2))
        for g in gs:
            d = dict(base); d.update(g); out.append(pose(**d))
        for g in gs:
            d = dict(base); d.update(g); d['eyes'] = 'closed'; out.append(pose(**d))
        return out, {'seq': 'blink', 'fps': spec.get('fps', 1.2)}
    for fr in spec['frames']:
        d = dict(base); d.update(fr); out.append(pose(**d))
    return out, {'seq': kind, 'fps': spec.get('fps', 3)}


# ---------- 走路的人（全身）----------
WALK_LOOKS = {   # 走路时的穿着：裤子 / 裙子、鞋
    'cn-teacher': dict(legs='skirt', skirt='#25B5C9', tights='#3B3F4E', shoe='#7A2E1F'),
    'cn-boy': dict(legs='pants', pants='#24324A', shoe='#E8E4DA'),
    'cn-girl': dict(legs='skirt', skirt='#2E6FD9', tights='#F2EEE6', shoe='#E8304A'),
    'west-man': dict(legs='pants', pants='#2A3A5E', shoe='#3B2A20'),
    'west-girl': dict(legs='pants', pants='#3E5DA8', shoe='#F2C230'),
    'west-woman': dict(legs='skirt', skirt='#7B57D6', tights='#F6D9C8', shoe='#1B1A1F'),
    'west-boy': dict(legs='pants', pants='#5E7D3A', shoe='#FFFFFF'),
    'west-clerk': dict(legs='pants', pants='#4A3B2E', shoe='#1B1A1F'),
}


def _head_small(L, k):
    """走路的人的头（脸朝前、稍微偏向右边）：鹅蛋脸、黑勾线、弯月眼、小红嘴、圆腮红"""
    sk, sk2 = SKIN[L.get('skin', 'pale')]
    hc, hl = HAIR[L.get('hair', 'black')]
    st = L.get('style', 'short')
    o = f'stroke="{INK}" stroke-width="{3.2 * k:.1f}" stroke-linejoin="round" stroke-linecap="round"'
    g = ''
    if st in ('long', 'curly'):
        g += f'<path d="M150,96 C150,40 270,40 270,96 C276,150 284,200 290,236 C262,246 238,240 226,226 L194,226 C182,240 158,246 130,236 C136,200 144,150 150,96 Z" fill="{hc}" {o}/>'
    if st == 'pony':
        g += f'<path d="M262,92 C300,110 300,170 286,214 C272,200 270,160 254,128 Z" fill="{hc}" {o}/>'
    g += f'<path d="M150,128 C140,118 132,140 142,156 C146,164 152,164 156,158 Z" fill="{sk}" {o}/><path d="M270,128 C280,118 288,140 278,156 C274,164 268,164 264,158 Z" fill="{sk}" {o}/>'
    g += f'<path d="M210,58 C246,58 270,86 270,126 C270,170 248,206 210,216 C172,206 150,170 150,126 C150,86 174,58 210,58 Z" fill="{sk}" {o}/>'
    g += '<circle cx="182" cy="162" r="13" fill="url(#bkBlush)"/><circle cx="244" cy="162" r="13" fill="url(#bkBlush)"/>'
    for cx in (190, 236):
        g += f'<path d="M{cx - 11},{134} C{cx - 5},{126} {cx + 5},{126} {cx + 11},{134}" fill="none" stroke="{INK}" stroke-width="{3.6 * k:.1f}" stroke-linecap="round"/>'
    g += f'<path d="M204,178 C210,182 220,182 226,178 C223,186 207,186 204,178 Z" fill="#E8304A" stroke="{INK}" stroke-width="{1.8 * k:.1f}"/>'
    if L.get('glasses'):
        g += f'<circle cx="190" cy="134" r="15" fill="none" {o}/><circle cx="236" cy="134" r="15" fill="none" {o}/><path d="M205,133 L221,133" {o}/>'
    if L.get('beard'):
        g += f'<path d="M160,160 C164,192 184,214 210,216 C236,214 256,192 260,160 C252,176 240,186 230,192 C218,186 202,186 190,192 C180,186 168,176 160,160 Z" fill="{hc}" {o}/>'
        g += f'<path d="M204,180 C210,184 220,184 226,180" fill="none" stroke="#E8304A" stroke-width="{3 * k:.1f}" stroke-linecap="round"/>'
    if st == 'bun':
        g += f'<circle cx="164" cy="66" r="22" fill="{hc}" {o}/><circle cx="256" cy="66" r="22" fill="{hc}" {o}/>'
    if st == 'afro':
        front = f'<path d="M144,134 C126,86 156,36 210,34 C264,36 294,86 276,134 C268,112 256,100 240,96 C222,104 196,104 178,96 C164,102 152,116 144,134 Z" fill="{hc}" {o}/>'
    elif st == 'curly':
        front = f'<path d="M146,132 C136,92 156,50 210,46 C264,50 284,92 274,132 C264,110 252,102 238,98 C224,106 196,108 180,100 C166,106 154,118 146,132 Z" fill="{hc}" {o}/>'
        front += ''.join(f'<path d="M{160 + i * 14},{66 + (i % 2) * 8} c8,-8 18,2 10,10" fill="none" stroke="{INK}" stroke-width="{2.2 * k:.1f}"/>' for i in range(7))
    else:
        front = f'<path d="M148,130 C140,80 168,48 212,48 C256,48 280,80 272,130 C264,108 254,96 240,90 C222,104 192,106 168,98 C158,106 152,116 148,130 Z" fill="{hc}" {o}/>'
    g += front
    g += ''.join(f'<path d="M{x0},{y0} Q{(x0 + x1) / 2},{min(y0, y1) - 7} {x1},{y1}" fill="none" stroke="{hl}" stroke-width="{2.4 * k:.1f}" stroke-linecap="round" opacity="0.9"/>'
                 for x0, y0, x1, y1 in ((180, 66, 222, 58), (196, 80, 244, 74)))
    return g


def walker(who, phase, carry=None, k=1.7):
    """走路的人，全身，往右走（脸朝前、稍微偏右）。phase：一步周期里的位置（0～1）；carry：'case' 拖行李箱 / 'pack' 背书包 / None。
    k：线条加粗倍数（人画得小也看得见勾线）。viewBox 0 0 460 900，脚底在 y≈884，画布左边留地方给行李箱"""
    L = dict(LOOKS[who]); L.update(WALK_LOOKS.get(who, {}))
    sk, sk2 = SKIN[L.get('skin', 'pale')]
    top, collar = L.get('top', '#F2C230'), L.get('collar', '#FFFFFF')
    ph = 2 * math.pi * phase
    o = f'stroke="{INK}" stroke-linejoin="round" stroke-linecap="round"'
    X = 60                                   # 整个人往右挪，左边留给箱子
    hipB, hipF = (X + 194, 512), (X + 226, 512)
    sh_b, sh_f = (X + 166, 286), (X + 256, 286)

    def leg(hip, a):                         # a：大腿角度（度，往前 = 正）；膝盖往前摆的时候弯
        th = math.radians(a)
        knee = (hip[0] + math.sin(th) * 176, hip[1] + math.cos(th) * 176)
        bend = 34 * max(0.0, math.sin(math.radians(a * 3.2)) if a > -6 else 0.0)
        sn = math.radians(a - bend)
        ank = (knee[0] + math.sin(sn) * 170, knee[1] + math.cos(sn) * 170)
        return knee, ank

    def leg_svg(hip, a, dark):
        knee, ank = leg(hip, a)
        legs = L.get('legs', 'pants')
        col = L.get('tights', sk2) if legs == 'skirt' else L.get('pants', '#333A48')
        if dark:
            col = vivid(col, 0.8)
        w = 40 if legs == 'pants' else 30
        d = f'M{hip[0]:.1f},{hip[1]:.1f} L{knee[0]:.1f},{knee[1]:.1f} L{ank[0]:.1f},{ank[1]:.1f}'
        sv = (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 6 * k:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
              f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
        sa = math.radians(max(-18, min(18, a * 0.45)))
        fx, fy = ank[0] + 6, ank[1] + 8
        shoe = L.get('shoe', INK)
        pts = [(-18, -12), (38, -10), (52, 4), (48, 14), (-20, 14)]
        rp = [(fx + px * math.cos(sa) - py * math.sin(sa), fy + px * math.sin(sa) + py * math.cos(sa)) for px, py in pts]
        sv += f'<path d="M{rp[0][0]:.1f},{rp[0][1]:.1f} L{rp[1][0]:.1f},{rp[1][1]:.1f} Q{rp[2][0]:.1f},{rp[2][1]:.1f} {rp[3][0]:.1f},{rp[3][1]:.1f} L{rp[4][0]:.1f},{rp[4][1]:.1f} Z" fill="{shoe}" {o} stroke-width="{3 * k:.1f}"/>'
        return sv

    def arm_svg(sh, a, col, hand_to=None):
        if hand_to is not None:
            E = ((sh[0] + hand_to[0]) / 2 - 6, (sh[1] + hand_to[1]) / 2 + 8)
            Wr = hand_to
        else:
            t1 = math.radians(a)
            E = (sh[0] + math.sin(t1) * 112, sh[1] + math.cos(t1) * 112)
            t2 = math.radians(a + 22)
            Wr = (E[0] + math.sin(t2) * 100, E[1] + math.cos(t2) * 100)
        d = f'M{sh[0]:.1f},{sh[1]:.1f} L{E[0]:.1f},{E[1]:.1f} L{Wr[0]:.1f},{Wr[1]:.1f}'
        return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{30 + 6 * k:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="{d}" fill="none" stroke="{col}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<circle cx="{Wr[0]:.1f}" cy="{Wr[1]:.1f}" r="15" fill="{sk}" {o} stroke-width="{3 * k:.1f}"/>'), Wr

    swing = 26 * math.sin(ph)
    back_arm_a, front_arm_a = 24 * math.sin(ph), -24 * math.sin(ph)
    parts = ''
    case_svg = ''
    if carry == 'case':
        hx, hy = X + 70, 548                 # 箱子拉杆的把手（人身后、手拉着）
        cx0, cy0 = X - 50, 690
        case_svg = (f'<path d="M{hx},{hy} L{cx0 + 64},{cy0}" stroke="{INK}" stroke-width="{12 + 4 * k:.1f}" stroke-linecap="round"/>'
                    f'<path d="M{hx},{hy} L{cx0 + 64},{cy0}" stroke="#B9BEC8" stroke-width="10" stroke-linecap="round"/>'
                    f'<rect x="{cx0}" y="{cy0}" width="124" height="160" rx="20" fill="#E8407A" {o} stroke-width="{4 * k:.1f}"/>'
                    f'<path d="M{cx0 + 30},{cy0 + 10} L{cx0 + 30},{cy0 + 150} M{cx0 + 62},{cy0 + 10} L{cx0 + 62},{cy0 + 150} M{cx0 + 94},{cy0 + 10} L{cx0 + 94},{cy0 + 150}" stroke="{INK}" stroke-width="{2.2 * k:.1f}" opacity="0.55"/>'
                    f'<circle cx="{cx0 + 22}" cy="{cy0 + 170}" r="13" fill="{INK}"/><circle cx="{cx0 + 102}" cy="{cy0 + 170}" r="13" fill="{INK}"/>')
        b_arm, _ = arm_svg(sh_b, 0, vivid(top, 0.85), hand_to=(hx + 4, hy - 4))
    else:
        b_arm, _ = arm_svg(sh_b, back_arm_a, vivid(top, 0.85))
    pack = ''
    if carry == 'pack':
        pack = (f'<rect x="{X + 112}" y="270" width="80" height="190" rx="26" fill="#F28C28" {o} stroke-width="{4 * k:.1f}"/>'
                f'<rect x="{X + 120}" y="360" width="64" height="70" rx="14" fill="#F7B267" {o} stroke-width="{3 * k:.1f}"/>')
    parts += case_svg + b_arm + pack
    parts += leg_svg(hipB, -swing, True)
    # 身子：外套 / 上衣
    if L.get('sex') == 'f':
        torso = f'M{X + 160},300 C{X + 158},270 {X + 176},258 {X + 196},254 L{X + 224},254 C{X + 244},258 {X + 262},270 {X + 260},300 L{X + 262},430 L{X + 158},430 Z'
    else:
        torso = f'M{X + 150},304 C{X + 150},270 {X + 170},256 {X + 194},252 L{X + 226},252 C{X + 250},256 {X + 270},270 {X + 270},304 L{X + 268},520 L{X + 152},520 Z'
    if L.get('legs') == 'skirt':
        parts += leg_svg(hipF, swing, False)
        skirt = vivid(L.get('skirt', top), 1.0)
        sw = 8 * math.sin(ph)
        parts += f'<path d="M{X + 160},420 L{X + 260},420 L{X + 286 + sw},604 C{X + 240},618 {X + 180},618 {X + 134 + sw},604 Z" fill="{skirt}" {o} stroke-width="{4 * k:.1f}"/>'
        parts += f'<path d="{torso}" fill="{vivid(top, 1.05)}" {o} stroke-width="{4 * k:.1f}"/>'
    else:
        parts += f'<path d="{torso}" fill="{vivid(top, 1.05)}" {o} stroke-width="{4 * k:.1f}"/>'
        parts += leg_svg(hipF, swing, False)
        parts += f'<path d="M{X + 152},500 L{X + 268},500 L{X + 268},526 L{X + 152},526 Z" fill="{vivid(top, 0.9)}" {o} stroke-width="{3.4 * k:.1f}"/>'
    parts += f'<path d="M{X + 190},256 L{X + 210},300 L{X + 230},256" fill="{collar}" {o} stroke-width="{3 * k:.1f}"/>'
    if L.get('tie'):
        parts += f'<path d="M{X + 205},266 L{X + 215},266 L{X + 220},330 L{X + 210},342 L{X + 200},330 Z" fill="{L["tie"]}" {o} stroke-width="{2.4 * k:.1f}"/>'
    if carry == 'pack':
        parts += f'<path d="M{X + 170},262 L{X + 176},420" stroke="#C25E12" stroke-width="{10:.1f}"/><path d="M{X + 250},262 L{X + 244},420" stroke="#C25E12" stroke-width="10"/>'
    f_arm, _ = arm_svg(sh_f, front_arm_a, top)
    parts += f_arm
    parts += f'<path d="M{X + 196},212 L{X + 196},258 L{X + 224},258 L{X + 224},212 Z" fill="{sk2}" {o} stroke-width="{3 * k:.1f}"/>'
    parts += f'<g transform="translate({X - 2} 0)">{_head_small(L, k)}</g>'
    defs = ('<defs>' + _glow() + '<radialGradient id="bkBlush" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#F57FA6"/>'
            '<stop offset="0.7" stop-color="#F79CBB" stop-opacity="0.9"/><stop offset="1" stop-color="#F9B3CB" stop-opacity="0"/></radialGradient></defs>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 900">{defs}<g filter="url(#bkGlow)">{parts}</g></svg>'


WALKERS = {   # 场景里来来往往的人（中外都有）：名字 → (长相, 带什么)
    'walk-west-woman-case': ('west-woman', 'case'),
    'walk-cn-boy-pack': ('cn-boy', 'pack'),
    'walk-west-man-case': ('west-man', 'case'),
    'walk-cn-girl': ('cn-girl', None),
    'walk-west-boy-pack': ('west-boy', 'pack'),
    'walk-cn-teacher-case': ('cn-teacher', 'case'),
}


def build_motions(out, names=None, walkers=True, n_walk=6):
    """生成会动的人：MOTIONS 的每个动作写成 <名字>_m00.svg、_m01.svg…，走路的人写成 walk-…_w0.svg…；
    同时写 motions.json（每个动作：frames、seq、fps / mouths / gfps），make_prefs 照它填 prefs"""
    import json
    os.makedirs(out, exist_ok=True)
    meta = {}
    for name in (names or MOTIONS):
        frames, how = motion_frames(name)
        fns = []
        for i, svg in enumerate(frames):
            fn = '%s_m%02d.svg' % (name, i)
            open(os.path.join(out, fn), 'w', encoding='utf-8').write(svg)
            fns.append(fn)
        meta[name] = dict(how, frames=fns)
    if walkers:
        for name, (who, carry) in WALKERS.items():
            fns = []
            for i in range(n_walk):
                fn = '%s_w%d.svg' % (name, i)
                open(os.path.join(out, fn), 'w', encoding='utf-8').write(walker(who, i / n_walk, carry))
                fns.append(fn)
            meta[name] = dict(seq='loop', fps=7, frames=fns, walker=True)
    json.dump(meta, open(os.path.join(out, 'motions.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return meta


def build(out):
    os.makedirs(out, exist_ok=True)
    made = []
    for name, frames in ACTIONS.items():
        who = name.split('-')[0] + '-' + name.split('-')[1]
        base = LOOKS[who]
        for i, fr in enumerate(frames):
            spec = dict(base); spec.update(fr)
            fn = name + ('_f%d' % i if len(frames) > 1 else '') + '.svg'
            open(os.path.join(out, fn), 'w', encoding='utf-8').write(pose(**spec))
            made.append(fn)
    return made

if __name__ == '__main__':
    # python3 poses.py <文件夹>            6.24 的一套静止动作（xxx_f0.svg…）
    # python3 poses.py <文件夹> --motion   6.25：会动的人（说话、听、笑、走路）+ motions.json
    out = sys.argv[1] if len(sys.argv) > 1 else 'poses'
    if '--motion' in sys.argv:
        m = build_motions(out)
        print('%d 个会动的人：' % len(m) + '、'.join('%s（%d 帧，%s）' % (k, len(v['frames']), v['seq']) for k, v in m.items()))
    else:
        m = build(out)
        print('%d 张：' % len(m) + '、'.join(m))

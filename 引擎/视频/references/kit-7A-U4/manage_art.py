import sys, os, math, random, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'
R = random.Random(29)
SKIN, SKIN2 = '#F3C9A8', '#C88A6A'
# 6.30（第七十四版）：29 manage（先画图画书风，“都齐了”再转青绿工笔风）。要先跑 explore 的画图脚本（山林）。
# man 手：拉坯，两只手扶着转盘上的泥坯；驾驭：驯马师牵着缰绳，马小跑转圈；管理、经营：姑姑打理一家小书店；
# 设法做到：男孩终于爬上山顶，挥手欢呼；应付得了：女孩抱着一摞箱子说“我拿得动”；辨析 try：女孩踮脚够高处的东西，还没够着


def hand(x, y, flip=False):   # 一只手（手掌 + 四根手指 + 大拇指），朝右；flip 朝左
    s = f'<rect x="{x}" y="{y}" width="46" height="40" rx="14" fill="{SKIN}" stroke="{SKIN2}" stroke-width="3"/>'
    for k in range(4):
        s += f'<rect x="{x + 40}" y="{y + 2 + k * 10}" width="26" height="9" rx="4" fill="{SKIN}" stroke="{SKIN2}" stroke-width="2"/>'
    s += f'<rect x="{x + 18}" y="{y - 14}" width="10" height="22" rx="5" fill="{SKIN}" stroke="{SKIN2}" stroke-width="2" transform="rotate(30 {x + 23} {y})"/>'
    if flip:
        return f'<g transform="translate({2 * x + 66} 0) scale(-1 1)">{s}</g>'
    return s


def pottery(k):   # 拉坯：转盘上一团泥坯，两只手扶着，转盘在转（两帧）
    s = '<rect x="60" y="214" width="200" height="40" rx="8" fill="#5A4632"/><ellipse cx="160" cy="214" rx="130" ry="26" fill="#6B4E2E"/><ellipse cx="160" cy="204" rx="120" ry="22" fill="#8B5A2B"/>'
    for i in range(8):
        a = math.pi * 2 * i / 8 + (0.4 if k else 0)
        s += f'<path d="M{160 + 96 * math.cos(a):.0f},{204 + 17 * math.sin(a):.0f} L{160 + 112 * math.cos(a):.0f},{204 + 20 * math.sin(a):.0f}" stroke="#C8913A" stroke-width="4"/>'
    s += '<path d="M110,200 C100,150 122,124 132,104 C128,90 138,80 160,80 C182,80 192,90 188,104 C198,124 220,150 210,200 Z" fill="#C68642"/>'
    s += '<ellipse cx="160" cy="84" rx="28" ry="8" fill="#A86A32"/><path d="M122,150 C150,160 170,160 198,150" fill="none" stroke="#A86A32" stroke-width="4"/>'
    s += hand(58, 126) + hand(196, 126, flip=True)
    return svg(320, 256, s)


def horse(k):   # 马（侧面，头朝左），两帧：小跑，腿一前一后；红缰绳从笼头往左拖出去
    legs = [(122, -14), (142, 14), (228, 12), (248, -12)] if k == 0 else [(122, 14), (142, -14), (228, -12), (248, 12)]
    s = ''
    for x, d in legs:
        s += f'<path d="M{x},150 L{x + d},214 L{x + d},236" fill="none" stroke="#8B5A2B" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/><rect x="{x + d - 10}" y="232" width="20" height="10" rx="3" fill="#3A2A1A"/>'
    s += f'<path d="M272,96 C312,110 320,160 302,{192 if k == 0 else 180}" fill="none" stroke="#5A3A1E" stroke-width="18" stroke-linecap="round"/>'
    s += '<ellipse cx="188" cy="120" rx="100" ry="44" fill="#A86A32"/><ellipse cx="194" cy="140" rx="70" ry="14" fill="#C8894A"/>'
    s += '<path d="M124,104 L86,42 L114,30 L156,94 Z" fill="#A86A32"/>'
    s += '<path d="M86,40 C62,40 42,60 36,84 C32,98 46,104 60,98 C72,90 94,70 114,54 Z" fill="#A86A32"/><path d="M92,28 L98,8 L106,30 Z" fill="#8B5A2B"/>'
    s += '<path d="M114,30 C132,50 142,70 154,94 L142,98 C130,74 120,52 106,36 Z" fill="#5A3A1E"/><circle cx="76" cy="58" r="5" fill="#1B1A1F"/><circle cx="42" cy="88" r="3" fill="#3A2A1A"/>'
    s += '<path d="M58,72 C70,70 84,66 98,52" fill="none" stroke="#C0392B" stroke-width="5"/><path d="M50,92 C30,112 10,120 0,122" fill="none" stroke="#C0392B" stroke-width="4"/>'
    s += '<path d="M150,82 C180,76 220,76 246,84 L242,100 C220,94 180,94 152,98 Z" fill="#2E6FD9"/>'
    return svg(330, 250, s)


def fence():   # 马场的木栅栏
    s = ''
    for x in range(10, 600, 70):
        s += f'<rect x="{x}" y="20" width="16" height="110" rx="3" fill="#A86A32"/>'
    s += '<rect x="0" y="40" width="600" height="14" rx="4" fill="#C8913A"/><rect x="0" y="84" width="600" height="14" rx="4" fill="#C8913A"/>'
    return svg(600, 132, s)


def bookshop_bg():   # 小书店：三排书架、柜台和收银机、招牌“书店 BOOKSHOP”、吊灯、窗、绿植、看书的椅子、地毯
    s = '<rect width="1200" height="700" fill="#F3E3C6"/><rect x="0" y="560" width="1200" height="140" fill="#B07A4E"/>'
    for i in range(0, 1200, 80):
        s += f'<path d="M{i},560 L{i - 60},700" stroke="#9C6A42" stroke-width="3"/>'
    s += '<rect x="420" y="20" width="360" height="70" rx="10" fill="#2E6FD9"/>'
    s += f'<text x="530" y="68" font-size="36" fill="#FFFFFF" text-anchor="middle" {CJK}>书店</text><text x="680" y="68" font-size="30" fill="#F6E7C1" text-anchor="middle" {EN}>BOOKSHOP</text>'
    cols = ['#E8304A', '#F2C230', '#2E9E6A', '#2E6FD9', '#7B57D6', '#F27A8A', '#C8913A', '#5A6470']
    for sx in (40, 860):
        s += f'<rect x="{sx}" y="110" width="300" height="440" fill="#8B5A2B"/>'
        for r in range(4):
            y = 130 + r * 104
            s += f'<rect x="{sx + 12}" y="{y}" width="276" height="88" fill="#6B3E26"/>'
            x = sx + 16
            while x < sx + 270:
                w = R.randint(16, 26); h = R.randint(60, 84)
                s += f'<rect x="{x}" y="{y + 88 - h}" width="{w}" height="{h}" rx="2" fill="{R.choice(cols)}"/>'
                x += w + 2
    s += '<rect x="440" y="120" width="320" height="200" fill="#BFE3F2" stroke="#8B5A2B" stroke-width="12"/><path d="M600,120 L600,320 M440,220 L760,220" stroke="#8B5A2B" stroke-width="7"/>'
    for x, h in ((460, 70), (520, 110), (650, 90), (710, 60)):
        s += f'<rect x="{x}" y="{320 - h}" width="40" height="{h}" fill="#C9D6E3"/>'
    s += '<rect x="440" y="380" width="320" height="100" rx="8" fill="#A86A32"/><rect x="440" y="370" width="320" height="18" rx="5" fill="#8B5A2B"/>'
    s += '<rect x="660" y="316" width="80" height="56" rx="6" fill="#47525C"/><rect x="670" y="324" width="60" height="18" fill="#9ADBA0"/><rect x="460" y="340" width="70" height="30" fill="#E8304A"/><rect x="470" y="330" width="60" height="12" fill="#F2C230"/>'
    for x in (300, 900):
        s += f'<path d="M{x},0 L{x},40" stroke="#5A4632" stroke-width="3"/><path d="M{x - 34},62 L{x + 34},62 L{x + 20},40 L{x - 20},40 Z" fill="#F2C230"/><circle cx="{x}" cy="68" r="10" fill="#FFF3B0"/>'
    s += '<path d="M380,560 L390,500 L430,500 L440,560 Z" fill="#B8613A"/><circle cx="410" cy="470" r="40" fill="#4E9A3E"/><circle cx="396" cy="450" r="18" fill="#7CC160"/>'
    s += '<rect x="780" y="470" width="70" height="80" rx="12" fill="#C0392B"/><rect x="770" y="510" width="90" height="40" rx="10" fill="#E25B4B"/><path d="M784,550 L784,590 M846,550 L846,590" stroke="#5A3A1E" stroke-width="7"/>'
    s += '<ellipse cx="600" cy="640" rx="260" ry="40" fill="#C0392B"/><ellipse cx="600" cy="640" rx="220" ry="30" fill="#E25B4B"/>'
    s += '<circle cx="800" cy="200" r="34" fill="#FFFFFF" stroke="#8B5A2B" stroke-width="6"/><path d="M800,200 L800,178 M800,200 L816,208" stroke="#1B1A1F" stroke-width="4" stroke-linecap="round"/>'
    s += f'<rect x="372" y="150" width="56" height="80" rx="4" fill="#F2C230"/><text x="400" y="186" font-size="16" fill="#C0392B" text-anchor="middle" {CJK}>新书</text><text x="400" y="210" font-size="13" fill="#5A4632" text-anchor="middle" {EN}>NEW</text>'
    s += '<ellipse cx="815" cy="500" rx="30" ry="16" fill="#F28C28"/><circle cx="792" cy="490" r="14" fill="#F28C28"/><path d="M784,480 L788,470 L794,480 Z M796,478 L802,468 L806,480 Z" fill="#F28C28"/>'
    s += '<circle cx="560" cy="350" r="22" fill="#7FB8E6"/><path d="M546,344 C556,338 566,352 576,346" fill="none" stroke="#2E9E6A" stroke-width="6"/><rect x="556" y="370" width="8" height="14" fill="#8B5A2B"/>'
    return svg(1200, 700, s)


def boxstack():   # 一摞纸箱
    s = ''
    for i, (x, y, w, h) in enumerate(((20, 150, 200, 110), (40, 60, 170, 96), (66, -10, 130, 76))):
        s += f'<rect x="{x}" y="{y + 10}" width="{w}" height="{h}" rx="4" fill="{["#C8913A", "#D9A45A", "#E0B26A"][i]}"/><path d="M{x + w / 2},{y + 10} L{x + w / 2},{y + 10 + h * 0.4}" stroke="#F2D9A6" stroke-width="12"/>'
    return svg(240, 272, s)


def bookstack():
    s = ''
    for i, c in enumerate(('#E8304A', '#2E6FD9', '#F2C230', '#2E9E6A', '#7B57D6')):
        y = 150 - i * 30; dx = (i % 2) * 8
        s += f'<rect x="{10 + dx}" y="{y}" width="160" height="28" rx="4" fill="{c}"/><rect x="{14 + dx}" y="{y + 6}" width="152" height="6" fill="#FFFFFF" opacity="0.5"/>'
    return svg(184, 182, s)


def pennant(k):   # 山顶插的小旗（两帧）
    w = 'M14,14 C50,4 80,30 116,18 L116,74 C80,86 50,60 14,70 Z' if k == 0 else 'M14,14 C50,30 80,4 116,22 L116,78 C80,64 50,92 14,70 Z'
    return svg(130, 220, f'<rect x="6" y="6" width="8" height="210" fill="#6B3E26"/><path d="{w}" fill="#E8304A"/>')


def icon_man():
    return svg(200, 200, hand(40, 80))


def icon_age():
    return svg(200, 200, nest(horse(0), 0, 30, 200, 152))


write_art(ART, 'pottery_f0.svg', pottery(0)); write_art(ART, 'pottery_f1.svg', pottery(1))
write_art(ART, 'horse_f0.svg', horse(0)); write_art(ART, 'horse_f1.svg', horse(1)); write_art(ART, 'fence.svg', fence())
write_art(ART, 'bookshop-bg.svg', bookshop_bg(), bg=True); write_art(ART, 'boxstack.svg', boxstack()); write_art(ART, 'bookstack.svg', bookstack())
write_art(ART, 'pennant_f0.svg', pennant(0)); write_art(ART, 'pennant_f1.svg', pennant(1))
write_art(ART, 'icon-man.svg', icon_man()); write_art(ART, 'icon-age.svg', icon_age())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
HOLD = (20, 100, 120, 70, 'fist')
bx, bs = boxstack(), bookstack()
M['west-man-trainer'] = frames_out(ART, 'west-man-trainer', [person('west-man', left='present', mouth='open', brows='up', look=-1, top='#6B4E2E'),
                                                           person('west-man', left='present2', mouth='smile', look=-1, top='#6B4E2E', tilt=-2)], fps=1.4, seq='pingpong')
M['west-man-trainer2'] = frames_out(ART, 'west-man-trainer2', [person('west-man', left='present', right='thumb', mouth='laugh', eyes='happy', look=-1, top='#6B4E2E'),
                                                             person('west-man', left='present2', right='thumb', mouth='open', look=-1, top='#6B4E2E', tilt=2)], fps=1.2, seq='pingpong')
M['cn-teacher-shop2'] = frames_out(ART, 'cn-teacher-shop2', [person('cn-teacher', right='present', mouth='open', brows='up', look=1, top='#2E9E6A', collar='#FFFFFF'),
                                                           person('cn-teacher', right='point', mouth='smile', look=1, top='#2E9E6A', collar='#FFFFFF', tilt=2)], fps=1.2, seq='pingpong')
M['west-boy-books'] = frames_out(ART, 'west-boy-books', [holding('west-boy', bs, 280, 200, 160, 158, left=HOLD, right=HOLD, mouth='smile', look=-1, top='#7FB8E6'),
                                                       holding('west-boy', bs, 280, 200, 160, 158, left=HOLD, right=HOLD, mouth='open', brows='up', look=-1, top='#7FB8E6', tilt=-2)], fps=1.1, seq='pingpong')
M['cn-boy-top'] = frames_out(ART, 'cn-boy-top', [person('cn-boy', left='raise', right='raise', mouth='laugh', eyes='happy', top='#E8304A'),
                                               person('cn-boy', left='hello', right='raise', mouth='open', top='#E8304A', tilt=-3)], fps=1.6, seq='pingpong')
M['west-girl-top'] = frames_out(ART, 'west-girl-top', [person('west-girl', right='raise', mouth='laugh', eyes='happy', top='#7B57D6'),
                                                     person('west-girl', right='hello', left='thumb', mouth='open', top='#7B57D6', tilt=3)], fps=1.5, seq='pingpong')
M['cn-girl-boxes'] = frames_out(ART, 'cn-girl-boxes', [holding('cn-girl', bx, 262, 262, 196, 222, left=HOLD, right=HOLD, mouth='smile', brows='up', look=1, top='#F27A8A'),
                                                     holding('cn-girl', bx, 262, 262, 196, 222, left=HOLD, right=HOLD, mouth='laugh', eyes='happy', look=1, top='#F27A8A', tilt=3)], fps=1.0, seq='pingpong')
M['west-woman-boxes'] = frames_out(ART, 'west-woman-boxes', [holding('west-woman', bx, 262, 262, 196, 222, left=HOLD, right=HOLD, mouth='flat', brows='frown', look=-1),
                                                           holding('west-woman', bx, 262, 262, 196, 222, left=HOLD, right=HOLD, mouth='smile', eyes='happy', look=-1, tilt=-3)], fps=1.0, seq='pingpong')
M['west-boy-help'] = frames_out(ART, 'west-boy-help', [person('west-boy', right='present', mouth='open', brows='up', look=-1, top='#2E9E6A'),
                                                     person('west-boy', right='present2', mouth='smile', look=-1, top='#2E9E6A', tilt=-2)], fps=1.2, seq='pingpong')
M['west-girl-try'] = frames_out(ART, 'west-girl-try', [person('west-girl', right='pointup', mouth='o', brows='frown', look=1, top='#F2C230'),
                                                     person('west-girl', right='pointup', left='pointup', mouth='flat', brows='frown', look=1, top='#F2C230', tilt=4)], fps=1.4, seq='pingpong')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

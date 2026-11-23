import sys, os, math, random, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'
R = random.Random(28)
# 6.30（第七十四版）：28 sense（先画图画书风，“都齐了”再转青绿工笔风）。要先跑 owner 的画图脚本（跑着的小狗）。
# 来历 sensus 感觉：女孩闭着眼闻花香；意思：书上一句话标出来，读懂了；感觉（五官）：眼、耳、鼻、舌、手一圈；嗅觉：小狗闻着味道找到骨头；
# 幽默感：外国男孩讲笑话，中国孩子笑；道理：老师讲完，女孩头上灯泡一亮“有道理”；觉察到：猫竖起耳朵，察觉到要打雷


def scent():   # 一缕香味（弯弯的线）
    return svg(80, 120, '<path d="M20,110 C0,80 40,70 20,40 C8,20 30,8 26,0" fill="none" stroke="#F27A8A" stroke-width="7" stroke-linecap="round"/>'
               '<path d="M54,110 C34,84 70,72 54,46" fill="none" stroke="#F2A6C0" stroke-width="6" stroke-linecap="round"/>')


def bone():
    s = '<rect x="40" y="30" width="120" height="30" rx="10" fill="#FFF6E0"/>'
    for x in (40, 160):
        s += f'<circle cx="{x}" cy="30" r="20" fill="#FFF6E0"/><circle cx="{x}" cy="60" r="20" fill="#FFF6E0"/>'
    return svg(200, 90, s)


def flowerbed():   # 一丛花：红、黄、粉、紫
    s = '<ellipse cx="200" cy="200" rx="190" ry="40" fill="#6AA165"/>'
    for i in range(14):
        x = 30 + i * 26 + R.randint(-6, 6); y = 150 + R.randint(-30, 20)
        c = R.choice(['#E8304A', '#F2C230', '#F27A8A', '#7B57D6', '#FFFFFF'])
        s += f'<path d="M{x},{y} L{x},{205}" stroke="#3E8E3E" stroke-width="5"/>'
        for k in range(5):
            a = math.pi * 2 * k / 5
            s += f'<circle cx="{x + 13 * math.cos(a):.0f}" cy="{y + 13 * math.sin(a):.0f}" r="10" fill="{c}"/>'
        s += f'<circle cx="{x}" cy="{y}" r="7" fill="#F2A12E"/>'
    return svg(400, 240, s)


def senses():   # 五官一圈：眼、耳、鼻、舌（嘴）、手
    items = []
    def eye(cx, cy):
        return f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="20" fill="#FFFFFF" stroke="#1B1A1F" stroke-width="5"/><circle cx="{cx}" cy="{cy}" r="11" fill="#2E6FD9"/><circle cx="{cx}" cy="{cy}" r="5" fill="#1B1A1F"/>'
    def ear(cx, cy):
        return f'<path d="M{cx-14},{cy-30} C{cx+30},{cy-44} {cx+34},{cy+10} {cx+4},{cy+30} C{cx-8},{cy+38} {cx-18},{cy+24} {cx-10},{cy+14}" fill="#F3C9A8" stroke="#C88A6A" stroke-width="5"/>'
    def nose(cx, cy):
        return f'<path d="M{cx},{cy-34} C{cx+6},{cy} {cx+26},{cy+10} {cx+20},{cy+24} C{cx+10},{cy+30} {cx-10},{cy+30} {cx-20},{cy+24} C{cx-26},{cy+10} {cx-6},{cy} {cx},{cy-34} Z" fill="#F3C9A8" stroke="#C88A6A" stroke-width="5"/>'
    def mouth(cx, cy):
        return f'<path d="M{cx-34},{cy-6} C{cx-10},{cy+30} {cx+10},{cy+30} {cx+34},{cy-6} Z" fill="#E8304A"/><path d="M{cx-14},{cy+8} C{cx-4},{cy+22} {cx+10},{cy+20} {cx+14},{cy+6}" fill="#F27A8A"/>'
    def hand(cx, cy):
        s = f'<rect x="{cx-22}" y="{cy-6}" width="44" height="40" rx="12" fill="#F3C9A8" stroke="#C88A6A" stroke-width="4"/>'
        for k in range(4):
            s += f'<rect x="{cx-22+k*11}" y="{cy-36}" width="10" height="34" rx="5" fill="#F3C9A8" stroke="#C88A6A" stroke-width="3"/>'
        return s + f'<rect x="{cx+18}" y="{cy-4}" width="24" height="10" rx="5" fill="#F3C9A8" stroke="#C88A6A" stroke-width="3" transform="rotate(-30 {cx+20} {cy})"/>'
    s = '<circle cx="200" cy="200" r="150" fill="none" stroke="#F2C230" stroke-width="6" stroke-dasharray="14 12"/>'
    for k, (f, zh) in enumerate(((eye, '看'), (ear, '听'), (nose, '闻'), (mouth, '尝'), (hand, '摸'))):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        cx, cy = 200 + 150 * math.cos(a), 200 + 150 * math.sin(a)
        s += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="52" fill="#FFFDF5" stroke="#2E9E6A" stroke-width="5"/>' + f(cx, cy - 4)
        s += f'<text x="{cx:.0f}" y="{cy + 70:.0f}" font-size="26" fill="#2B8A3E" text-anchor="middle" {CJK}>{zh}</text>'
    return svg(400, 430, s)


def bulb(on):
    s = f'<circle cx="60" cy="56" r="44" fill="{"#FFE14D" if on else "#E6E9ED"}"/><rect x="40" y="96" width="40" height="26" rx="4" fill="#9AA3AE"/><path d="M40,106 L80,106 M40,114 L80,114" stroke="#7A8590" stroke-width="3"/>'
    s += f'<path d="M48,70 C52,50 68,50 72,70" fill="none" stroke="{"#E8A21A" if on else "#B8C0C9"}" stroke-width="4"/>'
    if on:
        for k in range(8):
            a = math.pi * 2 * k / 8
            s += f'<path d="M{60+56*math.cos(a):.0f},{56+56*math.sin(a):.0f} L{60+72*math.cos(a):.0f},{56+72*math.sin(a):.0f}" stroke="#F2C230" stroke-width="6" stroke-linecap="round"/>'
    return svg(120, 130, s)


def gift():
    s = '<rect x="20" y="60" width="160" height="120" rx="8" fill="#E8304A"/><rect x="10" y="40" width="180" height="32" rx="6" fill="#F05A6E"/><rect x="88" y="40" width="24" height="140" fill="#F2C230"/>'
    s += '<path d="M100,40 C70,0 40,20 64,40 Z M100,40 C130,0 160,20 136,40 Z" fill="#F2C230"/>'
    return svg(200, 190, s)


def bookline():   # 打开的书：一句话用黄笔标出来
    s = '<path d="M10,20 C70,6 120,14 150,26 L150,200 C120,188 70,182 10,194 Z" fill="#FFFFFF"/><path d="M290,20 C230,6 180,14 150,26 L150,200 C180,188 230,182 290,194 Z" fill="#FFFDF5"/>'
    for i in range(7):
        y = 48 + i * 20
        if i == 3:
            s += f'<rect x="168" y="{y-9}" width="106" height="16" rx="4" fill="#FFE14D"/>'
        s += f'<path d="M28,{y} L134,{y + 4} M166,{y + 4} L272,{y}" stroke="#9AA3AE" stroke-width="4"/>'
    s += '<path d="M10,194 C70,182 120,188 150,200 C180,188 230,182 290,194 L290,208 C230,196 180,202 150,214 C120,202 70,196 10,208 Z" fill="#7B57D6"/>'
    return svg(300, 220, s)


write_art(ART, 'scent.svg', scent(), style=False); write_art(ART, 'bone.svg', bone()); write_art(ART, 'flowerbed.svg', flowerbed())
write_art(ART, 'senses.svg', senses()); write_art(ART, 'bulb_f0.svg', bulb(False)); write_art(ART, 'bulb_f1.svg', bulb(True))
write_art(ART, 'gift.svg', gift()); write_art(ART, 'bookline.svg', bookline())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
HOLD = (20, 100, 120, 70, 'fist')
gf, bk = gift(), bookline()
M['west-girl-smell'] = frames_out(ART, 'west-girl-smell', [person('west-girl', left='chest', eyes='closed', mouth='smile', look=1, top='#F27A8A'),
                                                         person('west-girl', left='chest', eyes='closed', mouth='laugh', look=1, top='#F27A8A', tilt=4)], fps=0.8, seq='pingpong')
M['west-boy-joke'] = frames_out(ART, 'west-boy-joke', [person('west-boy', right='present', mouth='open', brows='up', look=1, top='#2E6FD9'),
                                                     person('west-boy', right='presentHi', mouth='laugh', eyes='happy', look=1, top='#2E6FD9', tilt=3)], fps=1.6, seq='pingpong')
M['cn-girl-laugh'] = frames_out(ART, 'cn-girl-laugh', [person('cn-girl', left='chest', right='chest', mouth='laugh', eyes='happy', look=-1, top='#F2C230'),
                                                     person('cn-girl', left='chest', right='chest', mouth='laugh', eyes='closed', look=-1, top='#F2C230', tilt=-5)], fps=2.2, seq='pingpong')
M['cn-boy-laugh'] = frames_out(ART, 'cn-boy-laugh', [person('cn-boy', right='thumb', mouth='laugh', eyes='happy', look=-1, top='#2E9E6A'),
                                                   person('cn-boy', right='thumb', mouth='laugh', eyes='closed', look=-1, top='#2E9E6A', tilt=-4)], fps=2.0, seq='pingpong')
M['west-girl-idea'] = frames_out(ART, 'west-girl-idea', [person('west-girl', right='chin', mouth='flat', brows='up', look=-1, top='#7B57D6'),
                                                       person('west-girl', right='pointup', mouth='laugh', eyes='happy', look=-1, top='#7B57D6', tilt=2)], fps=0.9, seq='pingpong')
M['cn-girl-gift'] = frames_out(ART, 'cn-girl-gift', [holding('cn-girl', gf, 290, 250, 140, 133, left=HOLD, right=HOLD, mouth='laugh', eyes='happy', top='#2E9E6A'),
                                                   holding('cn-girl', gf, 290, 250, 140, 133, left=HOLD, right=HOLD, mouth='o', eyes='wide', brows='up', top='#2E9E6A', tilt=3)], fps=1.2, seq='pingpong')
M['west-man-read'] = frames_out(ART, 'west-man-read', [holding('west-man', bk, 286, 250, 148, 108, left=HOLD, right=HOLD, mouth='flat', eyes='down', glasses=True),
                                                     holding('west-man', bk, 286, 250, 148, 108, left=HOLD, right=HOLD, mouth='smile', eyes='happy', glasses=True, tilt=2)], fps=0.9, seq='pingpong')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

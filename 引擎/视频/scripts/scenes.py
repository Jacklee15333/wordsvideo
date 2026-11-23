#!/usr/bin/env python3
"""详细、具体的生活场景背景（6.21）：火车站广场、屋里（书房 / 客厅）、教室、礼堂舞台。1200 × 700，画的是这个地方真有的东西。
  python3 scenes3.py <输出文件夹>"""
import os, sys, random, math
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
W, H = 1200, 700
def save(n, s):
    open(os.path.join(OUT, n), 'w', encoding='utf-8').write(s)
    print('%-22s %4d 个图形 %5.1f KB' % (n, sum(s.count('<' + t) for t in ('path', 'rect', 'circle', 'ellipse', 'line', 'polygon', 'text')), len(s.encode()) / 1024))
def lg(i, stops, x1=0, y1=0, x2=0, y2=1):
    return f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">' + ''.join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a[0]}"' if a else '') + '/>' for o, c, *a in stops) + '</linearGradient>'

def traveler(x, y, h, coat, pants='#3A3F4B', hair='#2A211D', skin='#E9B48E', bag=None, flip=False, kid=False):
    """广场上的行人（全身，小）：头、头发、上衣、胳膊、裤子、鞋；bag：'case' 拉杆箱 / 'pack' 双肩包"""
    k = h / 100.0
    s = -1 if flip else 1
    g = f'<g transform="translate({x} {y}) scale({k * s} {k})">'
    g += '<ellipse cx="0" cy="1" rx="17" ry="4" fill="#000" opacity="0.15"/>'
    if bag == 'pack':
        g += f'<rect x="-17" y="-78" width="12" height="26" rx="5" fill="#B5432F"/>'
    g += f'<rect x="-8" y="-46" width="7" height="42" rx="3" fill="{pants}"/><rect x="1" y="-46" width="7" height="42" rx="3" fill="{pants}"/>'
    g += '<rect x="-10" y="-5" width="10" height="5" rx="2" fill="#22252B"/><rect x="0" y="-5" width="10" height="5" rx="2" fill="#22252B"/>'
    g += f'<path d="M-11,-80 C-11,-86 11,-86 11,-80 L12,-44 L-12,-44 Z" fill="{coat}"/>'
    g += f'<rect x="-15" y="-79" width="6" height="30" rx="3" fill="{coat}"/><rect x="9" y="-79" width="6" height="30" rx="3" fill="{coat}"/>'
    g += f'<circle cx="-12" cy="-48" r="3" fill="{skin}"/><circle cx="12" cy="-48" r="3" fill="{skin}"/>'
    g += f'<rect x="-3" y="-88" width="6" height="6" fill="{skin}"/><ellipse cx="0" cy="-93" rx="8" ry="9" fill="{skin}"/>'
    g += f'<path d="M-8,-94 C-9,-104 9,-104 8,-94 C5,-99 -5,-99 -8,-94 Z" fill="{hair}"/>'
    if bag == 'case':
        g += '<path d="M16,-48 L24,-62" stroke="#555" stroke-width="2"/><rect x="18" y="-36" width="18" height="30" rx="3" fill="#2F6FB5"/><path d="M22,-36 L22,-6 M32,-36 L32,-6" stroke="#1F4F85" stroke-width="1.5"/><circle cx="21" cy="-4" r="2.5" fill="#222"/><circle cx="33" cy="-4" r="2.5" fill="#222"/>'
    return g + '</g>'

def tree(x, y, k=1.0):
    return (f'<g transform="translate({x} {y}) scale({k})"><rect x="-7" y="-70" width="14" height="72" fill="#6B4B2F"/><path d="M-7,-30 L-20,-48" stroke="#6B4B2F" stroke-width="5"/>'
            '<circle cx="0" cy="-104" r="46" fill="#3F7F3C"/><circle cx="-30" cy="-84" r="32" fill="#4E944A"/><circle cx="30" cy="-86" r="34" fill="#4A8C45"/><circle cx="-6" cy="-124" r="30" fill="#5BA455"/>'
            '<circle cx="14" cy="-110" r="20" fill="#6DB565" opacity="0.7"/></g>')

def lamp_post(x, y):
    return (f'<g transform="translate({x} {y})"><rect x="-4" y="-190" width="8" height="190" fill="#4A515C"/><rect x="-10" y="-8" width="20" height="8" rx="2" fill="#3A404A"/>'
            '<path d="M0,-190 C-10,-204 -34,-204 -40,-192 M0,-190 C10,-204 34,-204 40,-192" fill="none" stroke="#4A515C" stroke-width="5"/>'
            '<ellipse cx="-42" cy="-188" rx="12" ry="6" fill="#FFF3C4"/><ellipse cx="42" cy="-188" rx="12" ry="6" fill="#FFF3C4"/></g>')

def flowers(x, y, w, seed):
    r = random.Random(seed)
    s = f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="6" fill="#8E6B46"/><rect x="{x+3}" y="{y-12}" width="{w-6}" height="18" rx="9" fill="#3F8A3F"/>'
    for i in range(int(w / 9)):
        cx = x + 8 + i * 9 + r.uniform(-2, 2); cy = y - 8 + r.uniform(-5, 4)
        s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="{r.choice(["#E5383B", "#F4B400", "#FF7AA2", "#FFFFFF", "#E5383B"])}"/>'
    return s

# =================================================================== 火车站广场
def station():
    r = random.Random(7)
    d = '<defs>' + lg('stSky', [(0, '#8EC6F0'), (1, '#E6F3FC')]) + lg('stGl', [(0, '#6FA3CC'), (0.5, '#B7D7EE'), (1, '#5E8FB8')]) + \
        lg('stWall', [(0, '#EEE7D8'), (1, '#D2C8B4')]) + lg('stPave', [(0, '#DAD7CF'), (1, '#BDB9B0')]) + lg('stRoad', [(0, '#5A5E66'), (1, '#44474D')]) + \
        lg('stRoof', [(0, '#8C939D'), (1, '#5F6670')]) + lg('stDoor', [(0, '#3B5872'), (1, '#1E3145')]) + lg('stBus', [(0, '#F7FAFD'), (1, '#D5DFEA')]) + '</defs>'
    s = f'<rect width="{W}" height="{H}" fill="url(#stSky)"/>'
    for cx, cy, rx in ((170, 80, 90), (260, 100, 60), (840, 70, 80), (1040, 110, 70)):
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx * 0.28:.0f}" fill="#fff" opacity="0.85"/>'
    # 远处的楼
    for x, y, w in ((10, 250, 80), (96, 300, 60), (1030, 270, 70), (1106, 230, 86), (170, 340, 50)):
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{548 - y}" fill="#B9CCDD"/>'
        for yy in range(y + 14, 520, 26):
            for xx in range(x + 8, x + w - 10, 18):
                s += f'<rect x="{xx}" y="{yy}" width="10" height="14" fill="#DCE8F2"/>'
    # 两边的配楼
    for x0 in (110, 870):
        s += f'<rect x="{x0}" y="330" width="220" height="218" fill="url(#stWall)"/><rect x="{x0 - 8}" y="318" width="236" height="14" fill="url(#stRoof)"/>'
        for row in range(2):
            for col in range(5):
                s += f'<rect x="{x0 + 16 + col * 40}" y="{352 + row * 86}" width="28" height="60" fill="url(#stGl)" stroke="#F4F0E6" stroke-width="3"/>'
                s += f'<line x1="{x0 + 30 + col * 40}" y1="{352 + row * 86}" x2="{x0 + 30 + col * 40}" y2="{412 + row * 86}" stroke="#F4F0E6" stroke-width="2"/>'
    # 钟楼
    s += '<rect x="905" y="120" width="84" height="428" fill="url(#stWall)"/><path d="M897,120 L997,120 L947,84 Z" fill="url(#stRoof)"/><rect x="899" y="232" width="96" height="8" fill="#B7AD98"/>'
    s += '<circle cx="947" cy="180" r="32" fill="#FFFFFF" stroke="#5F584A" stroke-width="6"/>'
    for i in range(12):
        a = math.radians(i * 30)
        s += f'<line x1="{947 + 24 * math.sin(a):.1f}" y1="{180 - 24 * math.cos(a):.1f}" x2="{947 + 28 * math.sin(a):.1f}" y2="{180 - 28 * math.cos(a):.1f}" stroke="#333" stroke-width="2.5"/>'
    s += '<path d="M947,180 L947,160 M947,180 L963,188" stroke="#222" stroke-width="5" stroke-linecap="round"/><circle cx="947" cy="180" r="4" fill="#C8102E"/>'
    for yy in (262, 330, 398, 466):
        s += f'<rect x="935" y="{yy}" width="24" height="44" rx="12" fill="url(#stGl)" stroke="#F4F0E6" stroke-width="3"/>'
    # 主楼：大玻璃幕墙
    s += '<rect x="300" y="232" width="600" height="316" fill="url(#stWall)"/>'
    s += '<rect x="340" y="262" width="520" height="150" fill="url(#stGl)"/>'
    for i in range(14):
        s += f'<line x1="{340 + i * 40}" y1="262" x2="{340 + i * 40}" y2="412" stroke="#F4F0E6" stroke-width="{6 if i % 3 == 0 else 3}"/>'
    for yy in (262, 312, 362, 412):
        s += f'<line x1="340" y1="{yy}" x2="860" y2="{yy}" stroke="#F4F0E6" stroke-width="4"/>'
    s += '<path d="M360,412 L470,262 L520,262 L410,412 Z M620,412 L730,262 L760,262 L650,412 Z" fill="#fff" opacity="0.16"/>'
    s += '<rect x="280" y="212" width="640" height="22" fill="url(#stRoof)"/><rect x="280" y="212" width="640" height="5" fill="#fff" opacity="0.3"/>'
    # 楼顶的站名大字
    for i, ch in enumerate('火车站'):
        cx = 480 + i * 120
        s += f'<line x1="{cx - 24}" y1="212" x2="{cx - 24}" y2="190" stroke="#6B7078" stroke-width="4"/><line x1="{cx + 24}" y1="212" x2="{cx + 24}" y2="190" stroke="#6B7078" stroke-width="4"/>'
        s += f'<text x="{cx + 3}" y="{197}" text-anchor="middle" font-family="Noto Sans CJK SC, sans-serif" font-size="92" font-weight="900" fill="#8E0E12">{ch}</text>'
        s += f'<text x="{cx}" y="{194}" text-anchor="middle" font-family="Noto Sans CJK SC, sans-serif" font-size="92" font-weight="900" fill="#DC1E24">{ch}</text>'
    # 一楼：售票处、进站口（雨棚、电子屏、玻璃门）、出站口
    s += '<rect x="300" y="420" width="600" height="8" fill="#B7AD98"/>'
    s += '<rect x="340" y="440" width="120" height="26" rx="4" fill="#1D5FA8"/><text x="400" y="460" text-anchor="middle" font-family="Noto Sans CJK SC, sans-serif" font-size="20" font-weight="bold" fill="#fff">售 票 处</text>'
    for i in range(3):
        s += f'<rect x="{344 + i * 39}" y="476" width="33" height="46" fill="url(#stDoor)" stroke="#F4F0E6" stroke-width="3"/><rect x="{350 + i * 39}" y="500" width="21" height="6" fill="#DDE7F0"/>'
    s += '<rect x="740" y="440" width="120" height="26" rx="4" fill="#2E8B57"/><text x="800" y="460" text-anchor="middle" font-family="Noto Sans CJK SC, sans-serif" font-size="20" font-weight="bold" fill="#fff">出 站 口</text>'
    for i in range(2):
        s += f'<rect x="{748 + i * 54}" y="476" width="48" height="72" fill="url(#stDoor)" stroke="#F4F0E6" stroke-width="3"/>'
    s += '<rect x="486" y="428" width="228" height="34" rx="4" fill="#15181D"/><text x="600" y="453" text-anchor="middle" font-family="Noto Sans CJK SC, sans-serif" font-size="24" font-weight="bold" fill="#FF8A1F">进 站 口　ENTRANCE</text>'
    s += '<rect x="462" y="462" width="276" height="12" fill="#4D6A86"/><rect x="462" y="462" width="276" height="3" fill="#fff" opacity="0.35"/>'
    s += '<rect x="470" y="474" width="8" height="74" fill="#8C939D"/><rect x="722" y="474" width="8" height="74" fill="#8C939D"/>'
    for i in range(4):
        s += f'<rect x="{492 + i * 54}" y="478" width="50" height="70" fill="url(#stDoor)" stroke="#DCE4EC" stroke-width="3"/><rect x="{512 + i * 54}" y="506" width="4" height="18" rx="2" fill="#DCE4EC"/>'
    s += '<rect x="290" y="540" width="620" height="10" fill="#A9A08C"/><rect x="102" y="540" width="236" height="10" fill="#A9A08C"/><rect x="862" y="540" width="236" height="10" fill="#A9A08C"/>'
    # 广场地面、马路
    s += f'<rect y="548" width="{W}" height="152" fill="url(#stPave)"/>'
    for x in range(-200, W + 400, 70):
        s += f'<line x1="{x}" y1="548" x2="{x - 140}" y2="640" stroke="#A9A69E" stroke-width="1.5" opacity="0.7"/>'
    for yy in (572, 600, 632):
        s += f'<line x1="0" y1="{yy}" x2="{W}" y2="{yy}" stroke="#A9A69E" stroke-width="1.5" opacity="0.7"/>'
    s += f'<rect y="640" width="{W}" height="8" fill="#EDEBE6"/><rect y="648" width="{W}" height="52" fill="url(#stRoad)"/>'
    for x in range(30, W, 120):
        s += f'<rect x="{x}" y="672" width="60" height="5" fill="#F2F2F2" opacity="0.9"/>'
    # 花坛、路灯、长椅、树
    s += flowers(330, 556, 120, 1) + flowers(750, 556, 120, 2)
    s += tree(60, 560, 1.0) + tree(1150, 560, 1.05) + tree(232, 556, 0.72) + tree(1030, 556, 0.7)
    s += lamp_post(280, 566) + lamp_post(940, 566)
    for bx in (140, 1060):
        s += f'<rect x="{bx}" y="590" width="74" height="6" rx="2" fill="#8A5A33"/><rect x="{bx}" y="578" width="74" height="5" rx="2" fill="#8A5A33"/><path d="M{bx + 8},596 L{bx + 8},610 M{bx + 66},596 L{bx + 66},610" stroke="#3E434D" stroke-width="4"/>'
    # 公交车（左下）和出租车（右下）
    s += '<g><rect x="40" y="606" width="290" height="70" rx="12" fill="url(#stBus)"/><rect x="40" y="652" width="290" height="16" fill="#2B7BD6"/>'
    for i in range(6):
        s += f'<rect x="{56 + i * 44}" y="616" width="36" height="28" rx="3" fill="#6E9CC4"/>'
    s += '<rect x="298" y="616" width="24" height="44" rx="3" fill="#6E9CC4"/><circle cx="100" cy="676" r="14" fill="#222"/><circle cx="100" cy="676" r="6" fill="#9AA0A8"/><circle cx="270" cy="676" r="14" fill="#222"/><circle cx="270" cy="676" r="6" fill="#9AA0A8"/><rect x="150" y="598" width="70" height="10" rx="3" fill="#C9D3DE"/></g>'
    s += '<g><path d="M850,662 L856,640 C860,630 872,624 884,624 L960,624 C974,624 984,630 992,642 L1030,650 C1038,652 1042,658 1042,666 L1042,676 L846,676 L846,668 Z" fill="#F2B90F"/>'
    s += '<path d="M872,642 C874,634 880,630 888,630 L924,630 L924,646 L870,646 Z" fill="#6E9CC4"/><path d="M930,630 L958,630 C968,630 976,636 982,646 L930,646 Z" fill="#6E9CC4"/>'
    s += '<rect x="846" y="656" width="196" height="6" fill="#1F7A3A"/><rect x="908" y="614" width="34" height="11" rx="3" fill="#fff" stroke="#888" stroke-width="1"/><text x="925" y="623" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="8" font-weight="bold" fill="#C8102E">TAXI</text>'
    s += '<circle cx="884" cy="678" r="13" fill="#222"/><circle cx="884" cy="678" r="5" fill="#9AA0A8"/><circle cx="1004" cy="678" r="13" fill="#222"/><circle cx="1004" cy="678" r="5" fill="#9AA0A8"/></g>'
    # 旅客
    ppl = [(430, 600, 62, '#3E5A7E', 'case', False), (470, 606, 64, '#8A3B3B', 'pack', True), (560, 578, 50, '#5E6B45', None, False), (592, 580, 52, '#C9772E', 'case', False),
           (650, 576, 50, '#4B4F5C', 'pack', False), (700, 604, 64, '#7A4FA0', 'case', True), (760, 610, 66, '#2F6B6B', None, False), (390, 580, 52, '#B55A7A', None, True),
           (820, 590, 56, '#40598F', 'pack', False), (530, 622, 70, '#9A6A3E', 'case', False)]
    for x, y, h, c, bag, fl in ppl:
        s += traveler(x, y, h, c, bag=bag, flip=fl, hair=r.choice(['#2A211D', '#1E1816', '#E8B730', '#8A5426', '#C8552A', '#2A211D']), skin=r.choice(['#F2D2B8', '#E9B48E', '#C68B5E', '#F7DCC8']))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">' + d + s + '</svg>'
save('station-bg.svg', station())

# =================================================================== 屋里：书房 / 客厅
def room():
    r = random.Random(11)
    d = '<defs>' + lg('rmW', [(0, '#F5EEDF'), (1, '#E7DAC3')]) + lg('rmSky', [(0, '#93C9F2'), (1, '#E2F2FC')]) + lg('rmF', [(0, '#C99A66'), (1, '#9F6F43')]) + \
        lg('rmCur', [(0, '#7FB0A6'), (0.5, '#A8D0C6'), (1, '#6E9E94')], x2=1, y2=0) + lg('rmShelf', [(0, '#A9743F'), (1, '#8A5A2E')]) + lg('rmRug', [(0, '#B84C4C'), (1, '#8E3636')]) + '</defs>'
    s = f'<rect width="{W}" height="{H}" fill="url(#rmW)"/><rect width="{W}" height="26" fill="#FBF8F1"/><rect y="26" width="{W}" height="5" fill="#000" opacity="0.05"/>'
    # 窗户：窗外的楼和树
    s += '<rect x="150" y="110" width="330" height="310" fill="url(#rmSky)"/><ellipse cx="230" cy="160" rx="50" ry="16" fill="#fff" opacity="0.85"/><ellipse cx="400" cy="140" rx="40" ry="13" fill="#fff" opacity="0.75"/>'
    for x, y, w, c in ((166, 250, 60, '#C9D6E2'), (232, 210, 70, '#B7C7D6'), (310, 270, 54, '#D3DEE8'), (372, 230, 76, '#BFCEDB')):
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{420 - y}" fill="{c}"/>'
        for yy in range(y + 10, 400, 22):
            for xx in range(x + 7, x + w - 9, 16):
                s += f'<rect x="{xx}" y="{yy}" width="9" height="12" fill="#EEF4F9"/>'
    s += '<circle cx="200" cy="396" r="34" fill="#4E944A"/><circle cx="250" cy="404" r="28" fill="#3F7F3C"/><circle cx="430" cy="398" r="34" fill="#4A8C45"/><circle cx="350" cy="410" r="22" fill="#5BA455"/>'
    s += '<rect x="150" y="110" width="330" height="310" fill="none" stroke="#FFFFFF" stroke-width="14"/><line x1="315" y1="110" x2="315" y2="420" stroke="#fff" stroke-width="10"/><line x1="150" y1="230" x2="480" y2="230" stroke="#fff" stroke-width="8"/>'
    s += '<rect x="136" y="418" width="358" height="16" rx="3" fill="#FFFFFF"/><rect x="136" y="432" width="358" height="5" fill="#000" opacity="0.07"/>'
    # 窗台上的小盆栽
    s += '<path d="M196,418 L224,418 L220,398 L200,398 Z" fill="#C2683D"/><path d="M210,398 C200,380 196,372 204,362 C210,374 212,386 210,398 Z M210,398 C218,384 226,378 224,366 C214,374 210,386 210,398 Z" fill="#4E9A48"/>'
    # 窗帘和窗帘杆
    for x0, sgn in ((96, 1), (534, -1)):
        pts = f'M{x0},92 L{x0 + 76 * sgn},92 C{x0 + 66 * sgn},220 {x0 + 84 * sgn},340 {x0 + 70 * sgn},480 L{x0},480 Z'
        s += f'<path d="{pts}" fill="url(#rmCur)"/>'
        for k in range(1, 4):
            xx = x0 + sgn * k * 19
            s += f'<path d="M{xx},92 C{xx + 5 * sgn},220 {xx - 4 * sgn},350 {xx + 3 * sgn},480" fill="none" stroke="#4F8278" stroke-opacity="0.45" stroke-width="3"/>'
    s += '<rect x="80" y="84" width="470" height="9" rx="4" fill="#8A6A44"/><circle cx="80" cy="88" r="8" fill="#8A6A44"/><circle cx="550" cy="88" r="8" fill="#8A6A44"/>'
    s += '<path d="M80,96 L80,118" stroke="#D21F26" stroke-width="3"/><path d="M80,118 L96,134 L80,150 L64,134 Z" fill="#D21F26"/><path d="M72,126 L88,142 M88,126 L72,142" stroke="#F2C14E" stroke-width="2"/><path d="M80,150 L80,158 M74,158 L74,186 M80,158 L80,190 M86,158 L86,186" stroke="#D21F26" stroke-width="3"/><rect x="74" y="154" width="12" height="8" rx="2" fill="#F2C14E"/>'
    # 挂钟
    s += '<circle cx="640" cy="130" r="40" fill="#FFFFFF" stroke="#7A5533" stroke-width="8"/>'
    for i in range(12):
        a = math.radians(i * 30)
        s += f'<line x1="{640 + 28 * math.sin(a):.1f}" y1="{130 - 28 * math.cos(a):.1f}" x2="{640 + 33 * math.sin(a):.1f}" y2="{130 - 33 * math.cos(a):.1f}" stroke="#333" stroke-width="{3 if i % 3 == 0 else 1.5}"/>'
    s += '<path d="M640,130 L640,106 M640,130 L658,138" stroke="#222" stroke-width="4" stroke-linecap="round"/><circle cx="640" cy="130" r="4" fill="#C8102E"/>'
    # 墙上：中式山水画（宣纸、远山、小船、红印章，上下两根轴）和西式相框
    s += '<rect x="596" y="196" width="160" height="10" rx="4" fill="#6B3E1F"/><rect x="596" y="318" width="160" height="10" rx="4" fill="#6B3E1F"/><rect x="604" y="206" width="144" height="112" fill="#F5EBD3"/>'
    s += '<path d="M610,300 C630,250 646,236 662,262 C672,228 690,214 708,250 C718,236 732,240 744,262 L744,300 Z" fill="#5E7A70"/><path d="M610,300 C624,278 640,272 656,286 C670,270 690,268 704,286 C716,278 732,280 744,292 L744,300 Z" fill="#3E5A52"/>'
    s += '<path d="M640,304 L668,304 L662,310 L646,310 Z" fill="#3E2A1E"/><path d="M654,304 L654,292" stroke="#3E2A1E" stroke-width="2"/><rect x="722" y="214" width="14" height="14" fill="#D21F26"/><path d="M714,232 L714,268 M706,236 L706,262" stroke="#2A2A2A" stroke-width="3"/>'
    s += '<path d="M676,196 L676,184 L668,176 M676,184 L684,176" fill="none" stroke="#6B3E1F" stroke-width="2.5"/>'
    s += '<rect x="772" y="226" width="70" height="88" fill="#FBF8F1" stroke="#3E434D" stroke-width="6"/><circle cx="807" cy="258" r="13" fill="#E9B48E"/><path d="M786,306 C788,284 826,284 828,306 Z" fill="#4C7BD9"/><path d="M794,254 C794,240 820,240 820,254 C814,248 800,248 794,254 Z" fill="#2A211D"/>'
    # 墙上的搁板：书、小摆件
    s += '<rect x="590" y="372" width="260" height="10" rx="2" fill="url(#rmShelf)"/><path d="M606,382 L606,396 M834,382 L834,396" stroke="#7A4E28" stroke-width="5"/>'
    xx = 602
    for w, hh, c in ((14, 50, '#C0392B'), (12, 44, '#2E86C1'), (16, 54, '#27AE60'), (11, 40, '#F39C12'), (15, 48, '#8E44AD'), (13, 52, '#16A085')):
        s += f'<rect x="{xx}" y="{372 - hh}" width="{w}" height="{hh}" rx="1.5" fill="{c}"/><rect x="{xx + 2}" y="{372 - hh + 8}" width="{w - 4}" height="3" fill="#fff" opacity="0.6"/>'
        xx += w + 2
    s += '<path d="M738,372 C726,362 726,346 736,338 C732,332 734,326 740,322 L752,322 C758,326 760,332 756,338 C766,346 766,362 754,372 Z" fill="#F7FAFF"/>'
    s += '<path d="M730,352 C738,346 754,346 762,352 M732,360 C740,366 752,366 760,360" fill="none" stroke="#1F4FA8" stroke-width="2.5"/><path d="M740,344 C744,336 750,336 752,344 C748,348 744,348 740,344 Z" fill="#1F4FA8"/><rect x="739" y="318" width="14" height="6" rx="2" fill="#1F4FA8"/>'
    s += '<rect x="790" y="338" width="44" height="34" rx="3" fill="#F2E3C6" stroke="#8B6A47" stroke-width="4"/>'
    # 书架
    s += '<rect x="900" y="100" width="260" height="450" fill="url(#rmShelf)"/><rect x="912" y="112" width="236" height="426" fill="#6E4623"/>'
    for i, yy in enumerate((112, 218, 324, 430)):
        s += f'<rect x="912" y="{yy + 96}" width="236" height="10" fill="#A9743F"/>'
        x = 918
        cols = ['#C0392B', '#2E86C1', '#27AE60', '#F39C12', '#8E44AD', '#16A085', '#D35400', '#34495E', '#E84393', '#7F8C8D']
        while x < 1136 - (60 if i in (1, 3) else 0):
            w = r.choice([12, 14, 16, 18, 20]); hh = r.randint(58, 90)
            c = r.choice(cols)
            s += f'<rect x="{x}" y="{yy + 96 - hh}" width="{w}" height="{hh}" rx="1.5" fill="{c}"/><rect x="{x + 2}" y="{yy + 96 - hh + 10}" width="{w - 4}" height="4" fill="#fff" opacity="0.55"/>'
            x += w + 2
        if i == 1:
            s += f'<circle cx="1112" cy="{yy + 66}" r="22" fill="#4C8FD6"/><path d="M1098,{yy + 60} C1106,{yy + 50} 1120,{yy + 56} 1124,{yy + 66} C1116,{yy + 74} 1104,{yy + 72} 1098,{yy + 60} Z" fill="#5BA455"/><rect x="1106" y="{yy + 86}" width="12" height="10" fill="#8A6A44"/>'
        if i == 3:
            s += f'<path d="M1096,{yy + 96} L1128,{yy + 96} L1124,{yy + 70} L1100,{yy + 70} Z" fill="#E9C46A"/><path d="M1100,{yy + 70} C1100,{yy + 50} 1124,{yy + 50} 1124,{yy + 70} Z" fill="#F4D35E"/><rect x="1108" y="{yy + 40}" width="8" height="12" fill="#E9C46A"/>'
    # 踢脚线、木地板、地毯、落地的绿植
    s += f'<rect y="548" width="{W}" height="14" fill="#FBF8F2"/><rect y="560" width="{W}" height="140" fill="url(#rmF)"/>'
    for yy in (590, 628, 670):
        s += f'<line x1="0" y1="{yy}" x2="{W}" y2="{yy}" stroke="#7E5532" stroke-opacity="0.3" stroke-width="2"/>'
    for x in range(60, W + 200, 150):
        s += f'<line x1="{x}" y1="560" x2="{x - 60}" y2="700" stroke="#7E5532" stroke-opacity="0.25" stroke-width="2"/>'
    s += '<ellipse cx="560" cy="650" rx="330" ry="42" fill="url(#rmRug)"/><ellipse cx="560" cy="650" rx="300" ry="34" fill="none" stroke="#F2D9A0" stroke-width="4" stroke-dasharray="14 8"/>'
    s += '<path d="M40,560 L96,560 L90,500 L46,500 Z" fill="#D9D2C5"/><rect x="40" y="494" width="56" height="10" rx="3" fill="#C9C1B2"/>'
    for a, l, c in ((-50, 150, '#3F7F3C'), (-25, 190, '#4E944A'), (0, 210, '#5BA455'), (22, 180, '#4A8C45'), (46, 140, '#3F7F3C')):
        ex = 68 + l * math.sin(math.radians(a)); ey = 496 - l * math.cos(math.radians(a))
        s += f'<path d="M68,496 Q{68 + (ex - 68) * 0.3 - 18:.0f},{(496 + ey) / 2:.0f} {ex:.0f},{ey:.0f} Q{68 + (ex - 68) * 0.7 + 18:.0f},{(496 + ey) / 2:.0f} 68,496 Z" fill="{c}"/>'
    # 墙上的开关和插座
    s += '<rect x="560" y="470" width="20" height="26" rx="3" fill="#FBFBFB" stroke="#D6CFC2" stroke-width="2"/><rect x="566" y="476" width="8" height="14" rx="2" fill="#E9E5DC"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">' + d + s + '</svg>'
save('room-bg.svg', room())

# =================================================================== 教室
def classroom():
    r = random.Random(5)
    d = '<defs>' + lg('crW', [(0, '#F6F4EA'), (1, '#ECE9DB')]) + lg('crB', [(0, '#2F6350'), (1, '#234B3C')]) + lg('crF', [(0, '#CFC8B8'), (1, '#B3AB98')]) + \
        lg('crSky', [(0, '#9CCEF3'), (1, '#E4F3FD')]) + lg('crWood', [(0, '#C08A57'), (1, '#94623A')]) + lg('crCur', [(0, '#5E8FC9'), (0.5, '#8DB6E3'), (1, '#4F7DB5')], x2=1, y2=0) + '</defs>'
    s = f'<rect width="{W}" height="{H}" fill="url(#crW)"/><rect y="440" width="{W}" height="110" fill="#CFE3D6"/><rect y="438" width="{W}" height="4" fill="#A9C7B4"/>'
    # 日光灯
    for x in (250, 720):
        s += f'<rect x="{x}" y="14" width="230" height="14" rx="7" fill="#FFFFFF" stroke="#C9CDD2" stroke-width="2"/><rect x="{x - 10}" y="8" width="250" height="8" rx="3" fill="#D9DCE0"/>'
    # 两边的窗户和蓝窗帘
    for x0 in (16, 1010):
        if x0 > 500:
            continue
        s += f'<rect x="{x0}" y="110" width="180" height="300" fill="url(#crSky)"/><circle cx="{x0 + 50}" cy="380" r="40" fill="#4E944A"/><circle cx="{x0 + 120}" cy="390" r="34" fill="#3F7F3C"/><rect x="{x0 + 84}" y="250" width="70" height="160" fill="#C9D6E2"/>'
        s += f'<rect x="{x0}" y="110" width="180" height="300" fill="none" stroke="#FFFFFF" stroke-width="12"/><line x1="{x0 + 90}" y1="110" x2="{x0 + 90}" y2="410" stroke="#fff" stroke-width="8"/><line x1="{x0}" y1="220" x2="{x0 + 180}" y2="220" stroke="#fff" stroke-width="6"/>'
        s += f'<path d="M{x0 - 6},100 L{x0 + 44},100 C{x0 + 40},200 {x0 + 20},260 {x0 + 2},300 C{x0 + 22},340 {x0 + 34},380 {x0 + 30},430 L{x0 - 6},430 Z" fill="url(#crCur)"/><rect x="{x0 - 6}" y="292" width="20" height="10" rx="4" fill="#E9C46A"/>'
        s += f'<rect x="{x0 - 10}" y="408" width="204" height="14" rx="3" fill="#fff"/>'
    # 黑板上方：标语和钟、广播喇叭
    for i, ch in enumerate('好好学习'):
        s += f'<rect x="{262 + i * 62}" y="56" width="52" height="52" rx="4" fill="#FFFFFF" stroke="#D7141A" stroke-width="3"/><text x="{288 + i * 62}" y="96" text-anchor="middle" font-family="Noto Serif CJK SC, serif" font-size="38" font-weight="bold" fill="#D7141A">{ch}</text>'
    for i, ch in enumerate('天天向上'):
        s += f'<rect x="{690 + i * 62}" y="56" width="52" height="52" rx="4" fill="#FFFFFF" stroke="#D7141A" stroke-width="3"/><text x="{716 + i * 62}" y="96" text-anchor="middle" font-family="Noto Serif CJK SC, serif" font-size="38" font-weight="bold" fill="#D7141A">{ch}</text>'
    s += '<circle cx="600" cy="82" r="34" fill="#FFFFFF" stroke="#4A515C" stroke-width="6"/>'
    for i in range(12):
        a = math.radians(i * 30)
        s += f'<line x1="{600 + 24 * math.sin(a):.1f}" y1="{82 - 24 * math.cos(a):.1f}" x2="{600 + 28 * math.sin(a):.1f}" y2="{82 - 28 * math.cos(a):.1f}" stroke="#333" stroke-width="{3 if i % 3 == 0 else 1.5}"/>'
    s += '<path d="M600,82 L600,62 M600,82 L614,90" stroke="#222" stroke-width="4" stroke-linecap="round"/>'
    s += '<rect x="1040" y="50" width="96" height="64" rx="6" fill="#DADDE2" stroke="#9CA3AD" stroke-width="3"/>' + ''.join(f'<line x1="1052" y1="{62 + i * 8}" x2="1124" y2="{62 + i * 8}" stroke="#7B828C" stroke-width="3"/>' for i in range(6))
    # 黑板：板书、粉笔槽、粉笔、板擦
    s += '<rect x="240" y="130" width="720" height="312" rx="6" fill="#B8BEC6"/><rect x="252" y="142" width="696" height="278" fill="url(#crB)"/>'
    s += '<text x="290" y="200" font-family="DejaVu Sans, sans-serif" font-size="44" font-weight="bold" fill="#fff" opacity="0.9">Unit 4</text>'
    s += '<text x="290" y="262" font-family="DejaVu Sans, sans-serif" font-size="30" fill="#fff" opacity="0.8">Good morning, class!</text>'
    s += '<g stroke="#fff" stroke-opacity="0.7" stroke-width="4" stroke-linecap="round" fill="none"><path d="M290,300 L560,300"/><path d="M290,336 L500,336"/><path d="M290,372 L600,372"/></g>'
    s += '<rect x="660" y="170" width="250" height="150" fill="none" stroke="#FFE680" stroke-opacity="0.85" stroke-width="4" stroke-dasharray="10 6"/><text x="785" y="222" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="30" font-weight="bold" fill="#FFE680" opacity="0.95">New words</text>'
    s += '<g stroke="#fff" stroke-opacity="0.7" stroke-width="4" stroke-linecap="round"><path d="M690,256 L880,256"/><path d="M690,288 L840,288"/></g>'
    s += '<text x="900" y="400" text-anchor="end" font-family="Noto Sans CJK SC, sans-serif" font-size="22" fill="#fff" opacity="0.6">值日生：____</text>'
    s += '<rect x="240" y="420" width="720" height="22" fill="#A7ADB5"/><rect x="240" y="438" width="720" height="6" fill="#8A9099"/>'
    for x, c in ((300, '#fff'), (330, '#FFE680'), (356, '#FFB3C7'), (700, '#fff')):
        s += f'<rect x="{x}" y="424" width="22" height="7" rx="3" fill="{c}"/>'
    s += '<rect x="420" y="418" width="56" height="14" rx="3" fill="#6B4B2F"/><rect x="420" y="428" width="56" height="6" fill="#E8E2D2"/>'
    # 右边：学习园地、图书角
    s += '<rect x="1000" y="150" width="184" height="240" rx="4" fill="#4E944A"/><rect x="1010" y="160" width="164" height="220" fill="#D9B98A"/>'
    s += '<text x="1092" y="192" text-anchor="middle" font-family="Noto Sans CJK SC, sans-serif" font-size="26" font-weight="bold" fill="#D7141A">学习园地</text>'
    for i, (x, y, c) in enumerate(((1020, 206, '#FFFFFF'), (1076, 206, '#FFF3B0'), (1128, 206, '#D8EEFF'), (1020, 290, '#FFE0E6'), (1076, 290, '#FFFFFF'), (1128, 290, '#E3F6D8'))):
        s += f'<rect x="{x}" y="{y}" width="40" height="72" fill="{c}" stroke="#C9B58E" stroke-width="1"/><circle cx="{x + 20}" cy="{y + 5}" r="3.5" fill="#D7141A"/>'
        for k in range(4):
            s += f'<line x1="{x + 6}" y1="{y + 20 + k * 11}" x2="{x + 34}" y2="{y + 20 + k * 11}" stroke="#8C8C8C" stroke-width="2"/>'
    s += '<rect x="1010" y="452" width="170" height="98" fill="url(#crWood)"/><rect x="1018" y="460" width="154" height="38" fill="#6E4623"/><rect x="1018" y="504" width="154" height="38" fill="#6E4623"/>'
    for yy in (460, 504):
        x = 1022
        while x < 1160:
            w = r.choice([10, 12, 14]); hh = r.randint(24, 34)
            s += f'<rect x="{x}" y="{yy + 38 - hh}" width="{w}" height="{hh}" fill="{r.choice(["#C0392B", "#2E86C1", "#27AE60", "#F39C12", "#8E44AD", "#16A085"])}"/>'
            x += w + 2
    s += '<path d="M1040,452 L1072,452 L1068,430 L1044,430 Z" fill="#D9D2C5"/><circle cx="1056" cy="414" r="18" fill="#5BA455"/><circle cx="1044" cy="422" r="11" fill="#3F7F3C"/>'
    # 地面、讲台（高出一级的木台子）、讲桌
    s += f'<rect y="548" width="{W}" height="152" fill="url(#crF)"/>'
    for i in range(140):
        s += f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(552, 698):.0f}" r="{r.uniform(1, 2.4):.1f}" fill="#8F8776" opacity="0.5"/>'
    s += '<path d="M150,548 L1050,548 L1090,582 L110,582 Z" fill="#C99C6A"/><rect x="110" y="582" width="980" height="20" fill="#946A40"/><path d="M150,548 L1050,548" stroke="#fff" stroke-opacity="0.35" stroke-width="3"/>'
    s += '<path d="M770,452 L950,452 L958,470 L762,470 Z" fill="#C08A57"/><rect x="762" y="470" width="196" height="12" fill="#7E5230"/><rect x="772" y="482" width="176" height="84" fill="url(#crWood)"/><rect x="788" y="496" width="144" height="56" rx="3" fill="#8A5C35" stroke="#5E3B1E" stroke-width="2"/>'
    s += '<rect x="786" y="436" width="46" height="16" rx="2" fill="#F4F1E8" stroke="#B9B2A2" stroke-width="2"/><rect x="790" y="430" width="8" height="8" fill="#fff"/><rect x="802" y="430" width="8" height="8" fill="#FFE680"/><rect x="814" y="430" width="8" height="8" fill="#FFB3C7"/>'
    s += '<rect x="850" y="440" width="60" height="6" fill="#2E86C1"/><rect x="854" y="434" width="54" height="6" fill="#C0392B"/><rect x="852" y="428" width="56" height="6" fill="#27AE60"/>'
    s += '<circle cx="930" cy="424" r="18" fill="#4C8FD6"/><path d="M918,418 C926,410 938,414 942,424 C934,432 924,430 918,418 Z" fill="#5BA455"/><rect x="926" y="440" width="8" height="8" fill="#8A6A44"/><rect x="918" y="446" width="24" height="5" rx="2" fill="#8A6A44"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">' + d + s + '</svg>'
save('classroom-bg.svg', classroom())

# 第一排课桌（放在人前面：挡住腰，像人站在课桌后面）
def class_desks():
    s = '<defs>' + lg('cdT', [(0, '#D9AE78'), (1, '#BC8B55')]) + lg('cdF', [(0, '#A87944'), (1, '#8A5F33')]) + '</defs>'
    for i, x in enumerate((20, 318, 616, 914)):
        s += f'<path d="M{x + 18},40 L{x + 250},40 L{x + 268},76 L{x},76 Z" fill="url(#cdT)"/><rect x="{x}" y="76" width="268" height="14" fill="#8C6236"/><rect x="{x + 10}" y="90" width="248" height="130" fill="url(#cdF)"/><rect x="{x + 24}" y="104" width="220" height="40" rx="3" fill="#6E4623"/>'
        s += f'<path d="M{x + 30},40 L{x + 60},40" stroke="#fff" stroke-opacity="0.3" stroke-width="3"/>'
        c1, c2 = (('#2E86C1', '#F39C12'), ('#C0392B', '#27AE60'), ('#8E44AD', '#16A085'), ('#D35400', '#2E86C1'))[i]
        s += f'<path d="M{x + 40},46 L{x + 120},46 L{x + 126},66 L{x + 34},66 Z" fill="{c1}"/><path d="M{x + 44},48 L{x + 116},48" stroke="#fff" stroke-opacity="0.6" stroke-width="3"/>'
        s += f'<rect x="{x + 150}" y="50" width="70" height="14" rx="7" fill="{c2}"/><rect x="{x + 228}" y="20" width="16" height="44" rx="6" fill="#BFE3F7" stroke="#7FB4D6" stroke-width="2"/><rect x="{x + 230}" y="12" width="12" height="10" rx="3" fill="#2E86C1"/>'
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 220">' + s + '</svg>'
save('class-desks.svg', class_desks())

# =================================================================== 礼堂舞台
def stage():
    r = random.Random(3)
    d = '<defs>' + lg('sgBack', [(0, '#27406E'), (0.5, '#3A5A96'), (1, '#27406E')], x2=1, y2=0) + lg('sgF', [(0, '#C08A57'), (1, '#8E5C33')]) + \
        lg('sgC', [(0, '#7E1A20'), (0.6, '#B8323C'), (1, '#8A1F27')], x2=1, y2=0) + lg('sgC2', [(0, '#8A1F27'), (0.4, '#B8323C'), (1, '#7E1A20')], x2=1, y2=0) + \
        lg('sgBeam', [(0, '#FFF3C4', 0.5), (1, '#FFF3C4', 0)]) + lg('sgPit', [(0, '#4A1B1F'), (1, '#2E1012')]) + \
        '<radialGradient id="sgSpot" cx="0.5" cy="0.4" r="0.6"><stop offset="0" stop-color="#FFF6DD" stop-opacity="0.55"/><stop offset="1" stop-color="#FFF6DD" stop-opacity="0"/></radialGradient></defs>'
    s = f'<rect width="{W}" height="{H}" fill="#1B2440"/><rect x="190" y="40" width="820" height="490" fill="url(#sgBack)"/>'
    for x in range(210, 1000, 34):
        s += f'<path d="M{x},40 C{x + 6},200 {x - 5},380 {x + 4},530" fill="none" stroke="#16264A" stroke-opacity="0.55" stroke-width="5"/>'
    for i in range(26):
        s += f'<circle cx="{r.uniform(230, 970):.0f}" cy="{r.uniform(150, 420):.0f}" r="{r.uniform(1.5, 3.2):.1f}" fill="#FFE9A8" opacity="{r.uniform(0.35, 0.8):.2f}"/>'
    s += '<ellipse cx="600" cy="330" rx="430" ry="260" fill="url(#sgSpot)"/>'
    # 灯架、射灯和光柱
    s += '<rect x="170" y="78" width="860" height="6" fill="#9AA0A8"/><rect x="170" y="100" width="860" height="6" fill="#7E848C"/>'
    for x in range(170, 1030, 30):
        s += f'<path d="M{x},84 L{x + 15},100 L{x + 30},84" fill="none" stroke="#8C929A" stroke-width="3"/>'
    for i, x in enumerate((260, 380, 500, 700, 820, 940)):
        tx = 600 + (x - 600) * 0.45
        s += f'<path d="M{x - 12},128 L{x + 12},128 L{tx + 110},520 L{tx - 110},520 Z" fill="url(#sgBeam)" opacity="0.5"/>'
        s += f'<rect x="{x - 3}" y="106" width="6" height="10" fill="#555"/><path d="M{x - 15},114 L{x + 15},114 L{x + 12},136 L{x - 12},136 Z" fill="#1B1C20"/><ellipse cx="{x}" cy="136" rx="12" ry="4" fill="#FFF3C4"/>'
    # 两边吊着的音箱
    for x in (224, 916):
        s += f'<path d="M{x + 14},100 L{x + 14},124 M{x + 46},100 L{x + 46},124" stroke="#777" stroke-width="3"/><rect x="{x}" y="124" width="60" height="96" rx="5" fill="#17181B" stroke="#3A3D44" stroke-width="3"/><circle cx="{x + 30}" cy="184" r="20" fill="#26282D" stroke="#4A4E56" stroke-width="3"/><rect x="{x + 16}" y="134" width="28" height="16" rx="3" fill="#26282D" stroke="#4A4E56" stroke-width="2"/>'
    # 舞台木地板
    s += f'<rect y="520" width="{W}" height="122" fill="url(#sgF)"/><rect y="516" width="{W}" height="8" fill="#6E4325"/>'
    for yy in (548, 580, 614):
        s += f'<line x1="0" y1="{yy}" x2="{W}" y2="{yy}" stroke="#7A4B27" stroke-opacity="0.35" stroke-width="2"/>'
    for x in range(-100, W + 300, 90):
        s += f'<line x1="{600 + (x - 600) * 0.72:.0f}" y1="524" x2="{x}" y2="642" stroke="#7A4B27" stroke-opacity="0.28" stroke-width="2"/>'
    # 两边的大幕、绑带、流苏
    s += '<path d="M0,0 L212,0 C196,170 226,330 176,470 C196,540 206,600 200,642 L0,642 Z" fill="url(#sgC)"/><path d="M1200,0 L988,0 C1004,170 974,330 1024,470 C1004,540 994,600 1000,642 L1200,642 Z" fill="url(#sgC2)"/>'
    for x in (30, 76, 122, 166):
        s += f'<path d="M{x},0 C{x + 10},180 {x - 6},330 {x - 10 + x * 0.1:.0f},470 C{x + 4},540 {x + 8},600 {x + 4},642" stroke="#5E0F14" stroke-opacity="0.45" stroke-width="9" fill="none"/>'
        s += f'<path d="M{W - x},0 C{W - x - 10},180 {W - x + 6},330 {W - x + 10 - x * 0.1:.0f},470 C{W - x - 4},540 {W - x - 8},600 {W - x - 4},642" stroke="#5E0F14" stroke-opacity="0.45" stroke-width="9" fill="none"/>'
    for x, sg in ((176, 1), (1024, -1)):
        s += f'<path d="M{x - 60 * sg},452 C{x - 30 * sg},476 {x - 6 * sg},478 {x + 6 * sg},466" fill="none" stroke="#E7B54A" stroke-width="9" stroke-linecap="round"/><path d="M{x},470 L{x - 4 * sg},520" stroke="#E7B54A" stroke-width="5"/><path d="M{x - 12 * sg},518 L{x + 4 * sg},518 L{x + 2 * sg},548 L{x - 10 * sg},548 Z" fill="#E7B54A"/>'
    # 顶上的横幕：波浪边、金色流苏
    s += f'<path d="M0,0 L{W},0 L{W},52 ' + ' '.join(f'Q{W - i * 100 - 50},{84 if i % 2 == 0 else 78} {W - (i + 1) * 100},52' for i in range(12)) + ' Z" fill="#A22830"/>'
    s += f'<path d="M{W},52 ' + ' '.join(f'Q{W - i * 100 - 50},{84 if i % 2 == 0 else 78} {W - (i + 1) * 100},52' for i in range(12)) + '" fill="none" stroke="#E7B54A" stroke-width="6"/>'
    for x in range(8, W, 14):
        yb = 60 + 14 * abs(math.sin((x % 100) / 100 * math.pi))
        s += f'<line x1="{x}" y1="{yb:.0f}" x2="{x}" y2="{yb + 10:.0f}" stroke="#E7B54A" stroke-width="3" opacity="0.9"/>'
    # 台口：台沿、台口的花、两边的台阶、台下
    s += f'<rect y="642" width="{W}" height="18" fill="#5E3A1E"/><rect y="660" width="{W}" height="40" fill="url(#sgPit)"/>'
    for i in range(15):
        x = 250 + i * 50
        s += f'<path d="M{x - 13},642 L{x + 13},642 L{x + 10},660 L{x - 10},660 Z" fill="#B5683F"/><circle cx="{x - 8}" cy="634" r="8" fill="#3F8A3F"/><circle cx="{x + 8}" cy="634" r="8" fill="#4E9A48"/><circle cx="{x}" cy="628" r="9" fill="#3F8A3F"/>'
        for dx, dy in ((-9, -12), (0, -18), (9, -12), (-4, -6), (5, -7)):
            s += f'<circle cx="{x + dx}" cy="{642 + dy}" r="4" fill="{("#E5383B", "#F4B400")[i % 2]}"/>'
    for x0 in (60, 1040):
        for k in range(3):
            s += f'<rect x="{x0 - k * 0}" y="{646 + k * 18}" width="100" height="18" fill="{("#A9743F", "#94623A", "#7E5230")[k]}" stroke="#5E3A1E" stroke-width="1.5"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">' + d + s + '</svg>'
save('stage-bg.svg', stage())

# 横幅（挂在舞台后幕上）：python 里改字再生成
def banner(text='校园英语演讲比赛', name='banner-speech.svg', en='ENGLISH SPEECH CONTEST'):
    """舞台横幅：上面中文、下面英文（6.22：中外结合）"""
    n = len(text)
    s = '<defs>' + lg('bnR', [(0, '#E0282E'), (1, '#B4161C')]) + '</defs>'
    s += '<path d="M40,0 L40,16 M860,0 L860,16" stroke="#C9C9C9" stroke-width="3"/><rect x="10" y="14" width="880" height="122" rx="4" fill="url(#bnR)"/>'
    s += '<path d="M230,14 C236,60 226,100 232,136 M660,14 C654,60 664,100 658,136" stroke="#8E0E12" stroke-opacity="0.35" stroke-width="4" fill="none"/>'
    step = min(100, 760 / n)
    x0 = 450 - step * (n - 1) / 2
    for i, ch in enumerate(text):
        s += f'<text x="{x0 + i * step:.0f}" y="82" text-anchor="middle" font-family="Noto Sans CJK SC, sans-serif" font-size="60" font-weight="900" fill="#FFE14D">{ch}</text>'
    if en:
        s += f'<text x="450" y="122" text-anchor="middle" font-family="DejaVu Sans, sans-serif" font-size="28" font-weight="bold" letter-spacing="6" fill="#FFFFFF">{en}</text>'
    save(name, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 140">' + s + '</svg>')
banner()

save('books.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 120"><rect x="10" y="84" width="200" height="30" rx="4" fill="#2E86C1"/><rect x="18" y="90" width="184" height="18" fill="#F4F1E8"/><rect x="24" y="52" width="176" height="32" rx="4" fill="#C0392B"/><rect x="32" y="58" width="160" height="20" fill="#F4F1E8"/><rect x="16" y="22" width="186" height="30" rx="4" fill="#27AE60"/><rect x="24" y="28" width="170" height="18" fill="#F4F1E8"/><rect x="10" y="84" width="24" height="30" rx="4" fill="#1F5F8B"/><rect x="24" y="52" width="24" height="32" rx="4" fill="#8E2A1F"/><rect x="16" y="22" width="24" height="30" rx="4" fill="#1C7A43"/></svg>')
save('mug.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 130 130"><defs>' + lg('mgB', [(0, '#F9FAFB'), (0.5, '#FFFFFF'), (1, '#CBD3DC')], x2=1, y2=0) + '</defs><path d="M92,44 C124,40 124,92 90,90" fill="none" stroke="#CBD3DC" stroke-width="10"/><path d="M18,30 L98,30 L92,116 C92,122 24,122 24,116 Z" fill="url(#mgB)"/><ellipse cx="58" cy="30" rx="40" ry="9" fill="#6B4226"/><rect x="34" y="62" width="48" height="26" rx="6" fill="#4C7BD9"/><path d="M48,8 C44,16 54,18 50,26 M66,6 C62,14 72,16 68,24" fill="none" stroke="#B9C0C9" stroke-width="3" stroke-linecap="round"/></svg>')

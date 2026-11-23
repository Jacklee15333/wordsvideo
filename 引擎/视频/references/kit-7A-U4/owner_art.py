import sys, os, math, random, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'
R = random.Random(21)
# 6.30（第七十四版）：21 owner（图画书风）。own 拥有：男孩站在自己的新自行车后面竖大拇指；物主：小狗跑回主人身边；
# 法律上认他是主人：房子、房产证、钥匙；…的主人：咖啡馆门口招手的店主；辨析 holder：拿着银行卡的人（持卡人）


def bike():   # 自行车（侧面，车头朝右）：前筐、车铃、链条
    s = '<path d="M80,170 L170,170" stroke="#9AA3AE" stroke-width="5"/>'
    for cx in (80, 300):
        s += f'<circle cx="{cx}" cy="170" r="58" fill="none" stroke="#1B1A1F" stroke-width="12"/><circle cx="{cx}" cy="170" r="10" fill="#9AA3AE"/>'
        for k in range(8):
            a = math.pi * k / 4
            s += f'<path d="M{cx},170 L{cx+50*math.cos(a):.0f},{170+50*math.sin(a):.0f}" stroke="#B8C0C9" stroke-width="3"/>'
    s += '<path d="M80,170 L170,170 L140,82 Z M140,82 L262,86 L170,170 M262,86 L300,170" fill="none" stroke="#E8304A" stroke-width="13" stroke-linejoin="round"/>'
    s += '<path d="M140,82 L134,62" stroke="#1B1A1F" stroke-width="8"/><ellipse cx="128" cy="58" rx="30" ry="10" fill="#1B1A1F"/>'
    s += '<path d="M262,86 L256,50 L292,42" fill="none" stroke="#1B1A1F" stroke-width="9" stroke-linecap="round"/><circle cx="270" cy="46" r="7" fill="#F2C230"/>'
    s += '<path d="M290,60 L346,60 L338,104 L298,104 Z" fill="#C8913A"/><path d="M296,74 L342,74 M300,88 L340,88" stroke="#9C6B2A" stroke-width="3"/>'
    s += '<path d="M170,170 L192,194" stroke="#1B1A1F" stroke-width="7"/><rect x="184" y="190" width="22" height="8" rx="3" fill="#1B1A1F"/>'
    return svg(380, 240, s)


def dog(k):   # 跑着的小狗（头朝左）：两帧，腿一前一后、尾巴摇
    s = ''
    legs = [(100, -22), (112, 18), (178, 20), (190, -20)] if k == 0 else [(100, 18), (112, -22), (178, -20), (190, 20)]
    for x, d in legs:
        s += f'<path d="M{x},112 L{x+d},162" stroke="#A86A32" stroke-width="14" stroke-linecap="round"/>'
    t = 40 if k == 0 else 62
    s += f'<path d="M204,80 Q232,70 246,{t}" fill="none" stroke="#C68642" stroke-width="13" stroke-linecap="round"/>'
    s += '<ellipse cx="146" cy="90" rx="72" ry="34" fill="#C68642"/><ellipse cx="150" cy="104" rx="50" ry="16" fill="#E0B07A"/>'
    s += '<circle cx="64" cy="62" r="32" fill="#C68642"/><ellipse cx="38" cy="74" rx="18" ry="12" fill="#E0B07A"/><circle cx="23" cy="69" r="7" fill="#1B1A1F"/>'
    s += '<circle cx="58" cy="52" r="5" fill="#1B1A1F"/><path d="M74,34 C96,30 100,62 86,78 C80,64 74,50 74,34 Z" fill="#8B5A2B"/>'
    s += '<path d="M90,84 C80,96 64,98 56,92" fill="none" stroke="#C0392B" stroke-width="9" stroke-linecap="round"/><circle cx="74" cy="104" r="7" fill="#F2C230"/>'
    if k == 1:
        s += '<path d="M34,84 C36,98 46,100 48,88 Z" fill="#F27A8A"/>'
    return svg(260, 180, s)


def house():   # 小楼：红屋顶、烟囱、门牌 18、门口挂一对红灯笼
    s = '<rect x="286" y="50" width="34" height="80" fill="#8E3B2E"/>'
    s += '<rect x="60" y="150" width="300" height="220" fill="#F4E3C3"/><polygon points="36,166 210,36 384,166" fill="#C0392B"/><path d="M36,166 L384,166" stroke="#8E2A20" stroke-width="8"/>'
    for x in (90, 262):
        s += f'<rect x="{x}" y="196" width="70" height="62" rx="4" fill="#BFE3F2"/><path d="M{x+35},196 L{x+35},258 M{x},227 L{x+70},227" stroke="#FFFFFF" stroke-width="5"/>'
        s += f'<rect x="{x-6}" y="258" width="82" height="10" rx="3" fill="#E8D0A8"/>'
    s += '<rect x="180" y="262" width="60" height="108" rx="6" fill="#6B3E26"/><circle cx="228" cy="318" r="5" fill="#F2C230"/>'
    s += f'<rect x="192" y="236" width="36" height="20" rx="3" fill="#2E6FD9"/><text x="210" y="252" font-size="15" fill="#FFFFFF" text-anchor="middle" {EN}>18</text>'
    for x in (162, 258):
        s += f'<path d="M{x},176 L{x},196" stroke="#1B1A1F" stroke-width="2"/><ellipse cx="{x}" cy="210" rx="12" ry="15" fill="#E8304A"/><path d="M{x},225 L{x},236" stroke="#F2C230" stroke-width="3"/>'
    s += '<rect x="170" y="370" width="80" height="12" fill="#B8B3AA"/>'
    return svg(420, 384, s)


def deed():   # 打开的房产证：左边红封面，右边写着“所有人 OWNER: Tom Brown”，盖红章
    s = '<rect x="10" y="10" width="140" height="190" rx="8" fill="#B71C1C"/><circle cx="80" cy="72" r="26" fill="none" stroke="#F2C230" stroke-width="5"/>'
    s += '<path d="M80,52 L86,68 L102,68 L89,78 L94,94 L80,84 L66,94 L71,78 L58,68 L74,68 Z" fill="#F2C230"/>'
    s += f'<text x="80" y="140" font-size="26" fill="#F2C230" text-anchor="middle" {CJK}>房产证</text>'
    s += '<rect x="150" y="10" width="140" height="190" rx="8" fill="#FFFDF5"/><path d="M150,10 L150,200" stroke="#D9CBA8" stroke-width="3"/>'
    s += f'<text x="220" y="44" font-size="15" fill="#5A4632" text-anchor="middle" {CJK}>所有人</text><text x="220" y="66" font-size="15" fill="#5A4632" text-anchor="middle" {EN}>OWNER</text>'
    s += f'<text x="220" y="104" font-size="20" fill="#1A66B8" text-anchor="middle" {EN}>Tom Brown</text>'
    for y in (122, 138):
        s += f'<path d="M168,{y} L272,{y}" stroke="#D9CBA8" stroke-width="3"/>'
    s += f'<circle cx="250" cy="168" r="22" fill="none" stroke="#D62828" stroke-width="5"/><text x="250" y="175" font-size="18" fill="#D62828" text-anchor="middle" {CJK}>章</text>'
    return svg(300, 210, s)


def key():
    s = '<circle cx="42" cy="45" r="32" fill="#F2C230"/><circle cx="42" cy="45" r="12" fill="#FFFFFF"/>'
    s += '<rect x="70" y="38" width="112" height="15" rx="4" fill="#F2C230"/><rect x="150" y="50" width="11" height="18" fill="#F2C230"/><rect x="168" y="50" width="11" height="25" fill="#F2C230"/>'
    return svg(200, 90, s)


def card():   # 银行卡：芯片、卡号
    s = '<rect x="4" y="4" width="212" height="132" rx="14" fill="#2E6FD9"/><path d="M4,96 L216,64 L216,122 C216,130 210,136 202,136 L18,136 C10,136 4,130 4,122 Z" fill="#2559B5"/>'
    s += '<rect x="24" y="44" width="38" height="30" rx="5" fill="#F2C230"/><path d="M24,59 L62,59 M43,44 L43,74" stroke="#C99A1E" stroke-width="2"/>'
    s += f'<text x="190" y="34" font-size="18" fill="#FFFFFF" text-anchor="end" {EN}>BANK</text><text x="24" y="112" font-size="17" fill="#FFFFFF" {EN}>**** 1234</text>'
    return svg(220, 140, s)


def home_bg():   # 住宅区：远处的楼、树、草坪、白栅栏、花坛、信箱、人行道；右边一段白墙灰瓦的月亮门（中外结合）
    d = lg('hbS', [(0, '#A9DBF7'), (1, '#E6F6FF')])
    s = '<rect width="1200" height="700" fill="url(#hbS)"/>'
    for x, y, r in ((160, 90, 34), (210, 80, 44), (262, 94, 32), (820, 70, 36), (876, 60, 48), (930, 76, 34)):
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF"/>'
    for x, w, h in ((40, 90, 210), (140, 70, 260), (230, 110, 190), (740, 80, 240), (830, 120, 200), (960, 70, 280), (1040, 120, 220)):
        s += f'<rect x="{x}" y="{520-h}" width="{w}" height="{h}" fill="#C9D6E3"/>'
        for j in range(3, h // 34):
            s += f'<rect x="{x+14}" y="{520-h+j*30-60}" width="{w-28}" height="12" fill="#B4C4D4"/>'
    for x, y, r, c in ((90, 430, 70, '#5FA84A'), (300, 420, 80, '#4E9A3E'), (1100, 420, 84, '#5FA84A'), (680, 440, 60, '#4E9A3E')):
        s += f'<rect x="{x-10}" y="{y}" width="20" height="{520-y}" fill="#8B5A2B"/><circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/><circle cx="{x-r*0.35:.0f}" cy="{y-r*0.3:.0f}" r="{r*0.45:.0f}" fill="#7CC160"/>'
    s += '<rect x="0" y="520" width="1200" height="180" fill="#8CCB6A"/><rect x="0" y="628" width="1200" height="44" fill="#D9D2C5"/><path d="M0,628 L1200,628 M0,672 L1200,672" stroke="#BDB4A4" stroke-width="4"/>'
    for i in range(0, 1200, 120):
        s += f'<path d="M{i},630 L{i+40},670" stroke="#C7BEAE" stroke-width="3"/>'
    for i in range(0, 380, 30):
        s += f'<path d="M{i+8},560 L{i+8},500 L{i+15},490 L{i+22},500 L{i+22},560 Z" fill="#FFFFFF"/>'
    s += '<rect x="0" y="512" width="380" height="9" fill="#FFFFFF"/><rect x="0" y="540" width="380" height="9" fill="#FFFFFF"/>'
    for x in range(40, 360, 46):
        c = R.choice(['#E8304A', '#F2C230', '#F27A8A', '#7B57D6'])
        s += f'<circle cx="{x}" cy="590" r="11" fill="{c}"/><circle cx="{x+20}" cy="600" r="9" fill="{R.choice(["#F2C230", "#FFFFFF"])}"/><path d="M{x},600 L{x},620" stroke="#3E8E3E" stroke-width="4"/>'
    s += '<rect x="900" y="300" width="300" height="260" fill="#F7F3EA"/><path d="M890,300 L1200,300 L1200,276 L906,276 Z" fill="#5E6A75"/>'
    for i in range(906, 1200, 22):
        s += f'<path d="M{i},276 L{i},300" stroke="#47525C" stroke-width="3"/>'
    s += '<circle cx="1060" cy="450" r="92" fill="#8CCB6A"/><circle cx="1060" cy="450" r="92" fill="none" stroke="#5E6A75" stroke-width="10"/>'
    s += '<rect x="1000" y="470" width="120" height="90" fill="#8CCB6A"/><circle cx="1060" cy="420" r="36" fill="#E8304A" opacity="0.85"/>'
    for i, x in enumerate(range(390, 900, 46)):      # 栅栏外一排灌木
        s += f'<circle cx="{x}" cy="522" r="{24 + (i % 3) * 5}" fill="#5FA84A"/><circle cx="{x+12}" cy="512" r="12" fill="#7CC160"/>'
    s += '<rect x="526" y="380" width="10" height="250" fill="#47525C"/><path d="M500,380 L562,380 L552,360 L510,360 Z" fill="#47525C"/><circle cx="531" cy="392" r="14" fill="#FFE9A8"/>'
    s += '<rect x="600" y="566" width="130" height="12" rx="4" fill="#B8613A"/><rect x="600" y="542" width="130" height="10" rx="4" fill="#B8613A"/><path d="M610,578 L610,610 M720,578 L720,610" stroke="#47525C" stroke-width="7"/>'
    for x, y in ((420, 150), (470, 130), (640, 170), (700, 140), (1000, 190)):
        s += f'<path d="M{x-16},{y} Q{x-8},{y-10} {x},{y} Q{x+8},{y-10} {x+16},{y}" fill="none" stroke="#47525C" stroke-width="4"/>'
    for i in range(6):
        s += f'<ellipse cx="{430+i*70}" cy="{600-i*4}" rx="26" ry="9" fill="#C7BEAE"/>'
    for i in range(22):
        x = 20 + i * 55; y = 690 if i % 2 else 545
        s += f'<path d="M{x},{y} L{x+5},{y-14} L{x+10},{y}" fill="none" stroke="#5E9E44" stroke-width="3"/>'
    s += f'<rect x="820" y="540" width="56" height="44" rx="10" fill="#2E6FD9"/><rect x="842" y="584" width="12" height="44" fill="#5A4632"/><text x="848" y="568" font-size="14" fill="#FFFFFF" text-anchor="middle" {EN}>MAIL</text>'
    return svg(1200, 700, s, d)


def cafe_bg():   # 咖啡馆门口：砖墙、大玻璃窗、条纹遮阳篷、招牌“Lily's Café 莉莉咖啡”、门上“OPEN”、小黑板菜单、门口小圆桌、红灯笼
    s = '<rect width="1200" height="700" fill="#C46A4A"/>'
    for j in range(0, 600, 28):
        for i in range(-60 if (j // 28) % 2 else 0, 1200, 120):
            s += f'<rect x="{i+3}" y="{j+3}" width="114" height="22" fill="#B85E40"/>'
    s += '<rect x="80" y="40" width="1040" height="96" rx="10" fill="#2F3B35"/>'
    s += f'<text x="470" y="106" font-size="58" fill="#F6E7C1" text-anchor="middle" {EN}>Lily’s Café</text><text x="900" y="104" font-size="48" fill="#F2C230" text-anchor="middle" {CJK}>莉莉咖啡</text>'
    for i in range(0, 1200, 80):
        c = '#E8304A' if (i // 80) % 2 == 0 else '#FFFFFF'
        s += f'<path d="M{i},150 L{i+80},150 L{i+80},210 Q{i+40},236 {i},210 Z" fill="{c}"/>'
    for x in (300, 620):
        s += f'<path d="M{x},218 L{x},240" stroke="#1B1A1F" stroke-width="3"/><ellipse cx="{x}" cy="262" rx="20" ry="24" fill="#E8304A"/><path d="M{x},286 L{x},302" stroke="#F2C230" stroke-width="4"/>'
    s += '<rect x="90" y="250" width="640" height="300" fill="#5A4632"/><rect x="104" y="264" width="612" height="272" fill="#CFE8F5"/>'
    s += '<path d="M410,264 L410,536" stroke="#5A4632" stroke-width="12"/><path d="M140,300 L220,380 M170,290 L260,380 M470,300 L540,370" stroke="#FFFFFF" stroke-width="10" opacity="0.6"/>'
    for x in (160, 250, 500, 600):
        s += f'<rect x="{x}" y="440" width="54" height="40" rx="6" fill="#FFFFFF"/><path d="M{x+54},450 C{x+70},450 {x+70},470 {x+54},470" fill="none" stroke="#FFFFFF" stroke-width="6"/><path d="M{x+14},432 C{x+8},420 {x+20},414 {x+16},402" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.8"/>'
    s += '<rect x="104" y="486" width="612" height="50" fill="#8B5A2B"/>'
    s += '<rect x="800" y="230" width="190" height="370" fill="#5A4632"/><rect x="816" y="246" width="158" height="354" fill="#6E8C82"/><rect x="832" y="262" width="126" height="160" fill="#CFE8F5"/>'
    s += f'<rect x="846" y="440" width="98" height="38" rx="6" fill="#FFFFFF"/><text x="895" y="467" font-size="24" fill="#2B8A3E" text-anchor="middle" {EN}>OPEN</text><circle cx="950" cy="520" r="8" fill="#F2C230"/>'
    s += '<rect x="0" y="600" width="1200" height="100" fill="#D9D2C5"/><path d="M0,600 L1200,600" stroke="#9C8F7A" stroke-width="6"/>'
    s += '<path d="M1050,470 L1010,640 M1110,470 L1150,640" stroke="#8B5A2B" stroke-width="10"/><rect x="1020" y="440" width="120" height="150" rx="8" fill="#2F3B35" stroke="#8B5A2B" stroke-width="8"/>'
    s += f'<text x="1080" y="476" font-size="20" fill="#FFFFFF" text-anchor="middle" {EN}>MENU</text><text x="1080" y="510" font-size="17" fill="#F6E7C1" text-anchor="middle" {EN}>Coffee ¥18</text>'
    s += f'<text x="1080" y="540" font-size="17" fill="#F6E7C1" text-anchor="middle" {CJK}>豆浆 ¥6</text><text x="1080" y="570" font-size="17" fill="#F6E7C1" text-anchor="middle" {EN}>Cake ¥12</text>'
    for x in (40, 740):
        s += f'<path d="M{x},600 L{x+10},540 L{x+60},540 L{x+70},600 Z" fill="#B8613A"/><circle cx="{x+35}" cy="510" r="38" fill="#4E9A3E"/><circle cx="{x+22}" cy="496" r="16" fill="#7CC160"/><circle cx="{x+50}" cy="500" r="7" fill="#F27A8A"/>'
    return svg(1200, 700, s)


def icon_own():
    return svg(200, 200, nest(bike(), 6, 40, 188, 119))


def icon_er():
    s = '<circle cx="100" cy="62" r="34" fill="#F3D2BE"/><path d="M38,190 C38,122 70,104 100,104 C130,104 162,122 162,190 Z" fill="#2E9E6A"/>'
    s += '<path d="M66,50 C68,22 132,22 134,50 C120,38 82,38 66,50 Z" fill="#1B1A1F"/><circle cx="88" cy="64" r="4" fill="#1B1A1F"/><circle cx="112" cy="64" r="4" fill="#1B1A1F"/>'
    return svg(200, 200, s)


write_art(ART, 'bike.svg', bike()); write_art(ART, 'house.svg', house()); write_art(ART, 'deed.svg', deed())
write_art(ART, 'key.svg', key()); write_art(ART, 'card.svg', card())
write_art(ART, 'dog_f0.svg', dog(0)); write_art(ART, 'dog_f1.svg', dog(1))
write_art(ART, 'home-bg.svg', home_bg(), bg=True); write_art(ART, 'cafe-bg.svg', cafe_bg(), bg=True)
write_art(ART, 'icon-own.svg', icon_own()); write_art(ART, 'icon-er.svg', icon_er())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
M['cn-boy-proud'] = frames_out(ART, 'cn-boy-proud', [person('cn-boy', left='thumb', mouth='laugh', eyes='happy', top='#2E9E6A'),
                                                   person('cn-boy', left='thumb', mouth='smile', eyes='happy', top='#2E9E6A', tilt=3)], fps=1.2, seq='pingpong')
M['cn-boy-pointbike'] = frames_out(ART, 'cn-boy-pointbike', [person('cn-boy', right='point', mouth='open', brows='up', look=1, top='#2E9E6A'),
                                                           person('cn-boy', right='point', mouth='half', look=1, top='#2E9E6A', tilt=-2)], fps=2, seq='pingpong')
M['cn-boy-mine'] = frames_out(ART, 'cn-boy-mine', [person('cn-boy', left='chest', mouth='laugh', eyes='happy', top='#2E9E6A'),
                                                 person('cn-boy', left='chest', right='hello', mouth='laugh', eyes='happy', top='#2E9E6A', tilt=3)], fps=1.4, seq='pingpong')
M['west-woman-call'] = frames_out(ART, 'west-woman-call', [person('west-woman', left='present', right='present', mouth='open', brows='up', look=1),
                                                         person('west-woman', left='present2', right='present2', mouth='laugh', eyes='happy', look=1, tilt=2)], fps=1.5, seq='pingpong')
M['west-man-owner'] = frames_out(ART, 'west-man-owner', [person('west-man', right='thumb', mouth='laugh', eyes='happy', look=-1),
                                                       person('west-man', right='thumb', mouth='smile', look=-1, tilt=3)], fps=1.2, seq='pingpong')
M['cn-teacher-shop'] = frames_out(ART, 'cn-teacher-shop', [person('cn-teacher', left='wave1', mouth='open', top='#8E5A3C', collar='#FFFFFF'),
                                                         person('cn-teacher', left='wave2', mouth='laugh', eyes='happy', top='#8E5A3C', collar='#FFFFFF')], fps=2, seq='loop')
cd = card()
M['west-man-card'] = frames_out(ART, 'west-man-card', [holding('west-man', cd, 300, 236, 120, 76, left=(20, 100, 120, 70, 'fist'), right=(20, 100, 120, 70, 'fist'), mouth='smile', look=1),
                                                     holding('west-man', cd, 300, 236, 120, 76, left=(20, 100, 120, 70, 'fist'), right=(20, 100, 120, 70, 'fist'), mouth='open', brows='up', look=1, tilt=2)], fps=1.2, seq='pingpong')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

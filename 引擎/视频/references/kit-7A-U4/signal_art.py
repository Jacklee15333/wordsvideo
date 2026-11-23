import sys, os, math, random, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'
R = random.Random(27)
# 6.30（第七十四版）：27 signal（先画图画书风，“都齐了”再转青绿工笔风）。要先跑 street、explore 的画图脚本（街道、山林）。
# sign 记号：山路边树干上的红白记号；-al：山顶插着作记号的红旗；约定的信号：长城烽火台上狼烟升起；电、无线电信号：发射塔往外出电波；
# 信号：路口的交通信号灯红变绿；发信号、示意：学校门口的协管员举 STOP 牌示意汽车停下；表明：铃声一响表示下课；显著的：成绩单上醒目的 A+


def marktree():   # 山路边的树：树干上刷着红白相间的路标记号，旁边一块箭头牌
    s = '<rect x="80" y="40" width="70" height="360" fill="#8B5A2B"/><path d="M96,60 L96,380 M126,80 L126,360" stroke="#6B4E2E" stroke-width="5"/>'
    s += '<circle cx="115" cy="40" r="90" fill="#4E9A3E"/><circle cx="60" cy="70" r="50" fill="#5FA84A"/><circle cx="170" cy="70" r="56" fill="#5FA84A"/>'
    for y, c in ((180, '#E8304A'), (206, '#FFFFFF'), (232, '#E8304A')):
        s += f'<rect x="80" y="{y}" width="70" height="26" fill="{c}"/>'
    s += '<rect x="200" y="250" width="12" height="150" fill="#6B3E26"/><path d="M190,250 L300,250 L330,280 L300,310 L190,310 Z" fill="#F2C230"/>'
    s += f'<text x="250" y="290" font-size="24" fill="#5A4632" text-anchor="middle" {CJK}>山顶</text>'
    return svg(340, 404, s)


def flag(k):   # 山顶的小红旗（两帧，随风飘）
    w = 'M20,20 C70,6 110,40 160,24 L160,100 C110,116 70,82 20,96 Z' if k == 0 else 'M20,20 C70,40 110,6 160,30 L160,104 C110,86 70,120 20,96 Z'
    s = f'<rect x="10" y="10" width="10" height="260" fill="#6B3E26"/><path d="{w}" fill="#E8304A"/><circle cx="15" cy="10" r="8" fill="#F2C230"/>'
    s += '<path d="M0,270 L120,240 L200,270 Z" fill="#8C96A3"/>'
    return svg(200, 276, s)


def beacon_bg():   # 群山里蜿蜒的长城、烽火台
    d = lg('bcS', [(0, '#BFE3F2'), (1, '#F4E9D4')])
    s = '<rect width="1200" height="700" fill="url(#bcS)"/>'
    for pts, c in (('0,420 160,250 330,380 520,220 700,360 900,200 1080,330 1200,260 1200,700 0,700', '#9DC59A'),
                   ('0,520 200,380 420,500 640,360 860,500 1050,400 1200,470 1200,700 0,700', '#7FB37A'),
                   ('0,620 260,520 520,600 780,500 1040,590 1200,540 1200,700 0,700', '#6AA165')):
        s += f'<polygon points="{pts}" fill="{c}"/>'
    wall = [(0, 560), (150, 520), (300, 470), (420, 430), (560, 460), (700, 420), (840, 380), (980, 400), (1200, 350)]
    s += '<polyline points="' + ' '.join(f'{x},{y}' for x, y in wall) + '" fill="none" stroke="#C8913A" stroke-width="28" stroke-linejoin="round"/>'
    for (x0, y0), (x1, y1) in zip(wall, wall[1:]):
        for t in range(0, 10):
            f = t / 10; x = x0 + (x1 - x0) * f; y = y0 + (y1 - y0) * f
            s += f'<rect x="{x-5:.0f}" y="{y-26:.0f}" width="10" height="12" fill="#B07A2E"/>'
    for x, y in ((300, 470), (700, 420), (1060, 385)):
        s += f'<rect x="{x-40}" y="{y-90}" width="80" height="90" fill="#C8913A"/><rect x="{x-48}" y="{y-104}" width="96" height="16" fill="#B07A2E"/>'
        for k in range(4):
            s += f'<rect x="{x-46+k*26}" y="{y-118}" width="14" height="14" fill="#B07A2E"/>'
        s += f'<rect x="{x-12}" y="{y-60}" width="24" height="34" rx="12" fill="#5A4632"/>'
    for x, y, r in ((200, 120, 40), (240, 110, 30), (900, 90, 46), (950, 80, 34)):
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF"/>'
    for i in range(14):
        x = 40 + i * 85; y = 640 + (i % 3) * 14
        s += f'<path d="M{x},{y} L{x+10},{y-30} L{x+20},{y}" fill="#4E8A3E"/>'
    for x, y in ((90, 560), (180, 600), (460, 560), (560, 610), (820, 560), (930, 600), (1130, 580), (1000, 640)):      # 山坡上的松树
        s += f'<rect x="{x-5}" y="{y-10}" width="10" height="30" fill="#6B4E2E"/><polygon points="{x-34},{y} {x},{y-50} {x+34},{y}" fill="#3E7A3A"/><polygon points="{x-26},{y-26} {x},{y-74} {x+26},{y-26}" fill="#4E8A3E"/>'
    for x, y in ((420, 160), (460, 140), (500, 170), (760, 200), (800, 180)):      # 天上的大雁
        s += f'<path d="M{x-14},{y} Q{x-7},{y-9} {x},{y} Q{x+7},{y-9} {x+14},{y}" fill="none" stroke="#47525C" stroke-width="4"/>'
    s += '<path d="M600,700 C620,640 560,600 600,560" fill="none" stroke="#D9C9A0" stroke-width="22"/>'      # 上山的小路
    for x, y in ((640, 660), (520, 650), (720, 620), (380, 680), (980, 690)):
        s += f'<circle cx="{x}" cy="{y}" r="8" fill="#F2C230"/><circle cx="{x+14}" cy="{y+4}" r="7" fill="#F27A8A"/>'
    return svg(1200, 700, s, d)


def smoke():
    return svg(140, 110, '<circle cx="50" cy="60" r="36" fill="#7A7F86"/><circle cx="86" cy="46" r="40" fill="#8C9198"/><circle cx="100" cy="76" r="28" fill="#6E737A"/>')


def radiotower():   # 发射塔
    s = '<path d="M100,20 L40,380 M100,20 L160,380" stroke="#C0392B" stroke-width="10"/>'
    for y in range(60, 380, 40):
        f = (y - 20) / 360
        s += f'<path d="M{100-60*f:.0f},{y} L{100+60*f:.0f},{y}" stroke="#E8E8E8" stroke-width="7"/><path d="M{100-60*f:.0f},{y} L{100+60*(f+0.11):.0f},{y+40}" stroke="#C0392B" stroke-width="4"/>'
    s += '<circle cx="100" cy="18" r="12" fill="#F2C230"/><rect x="30" y="378" width="140" height="18" fill="#8C96A3"/>'
    return svg(200, 400, s)


def tlight(k):   # 交通信号灯：k=0 红灯亮，k=1 绿灯亮
    s = '<rect x="60" y="150" width="20" height="250" fill="#47525C"/><rect x="20" y="10" width="100" height="200" rx="18" fill="#2B2D33"/>'
    s += f'<circle cx="70" cy="60" r="34" fill="{"#FF3B3B" if k == 0 else "#5A1F1F"}"/><circle cx="70" cy="150" r="34" fill="{"#38D86A" if k == 1 else "#1F4A2A"}"/>'
    if k == 0:
        s += '<circle cx="70" cy="60" r="44" fill="none" stroke="#FF8A8A" stroke-width="6" opacity="0.6"/>'
    else:
        s += '<circle cx="70" cy="150" r="44" fill="none" stroke="#9AF0B0" stroke-width="6" opacity="0.6"/>'
    return svg(140, 404, s)


def stoppaddle():
    s = '<rect x="54" y="120" width="12" height="150" fill="#9AA3AE"/>'
    pts = ' '.join(f'{60+56*math.cos(math.pi/8+k*math.pi/4):.0f},{66+56*math.sin(math.pi/8+k*math.pi/4):.0f}' for k in range(8))
    s += f'<polygon points="{pts}" fill="#E8304A" stroke="#FFFFFF" stroke-width="6"/><text x="60" y="66" font-size="28" fill="#FFFFFF" text-anchor="middle" {EN}>STOP</text><text x="60" y="94" font-size="20" fill="#FFFFFF" text-anchor="middle" {CJK}>停</text>'
    return svg(120, 270, s)


def car():   # 小汽车（车头朝左）
    s = '<path d="M20,110 L40,70 C50,50 70,40 110,40 L200,40 C230,40 250,60 266,80 L300,86 C316,88 320,100 320,110 L320,130 L20,130 Z" fill="#2E6FD9"/>'
    s += '<path d="M70,74 L100,50 L150,50 L150,80 Z M162,50 L210,50 C226,50 240,64 248,80 L162,80 Z" fill="#BFE3F2"/>'
    for x in (80, 250):
        s += f'<circle cx="{x}" cy="132" r="28" fill="#1B1A1F"/><circle cx="{x}" cy="132" r="11" fill="#B8C0C9"/>'
    s += '<rect x="14" y="96" width="18" height="12" rx="3" fill="#F2C230"/><rect x="306" y="96" width="14" height="12" rx="3" fill="#E8304A"/>'
    return svg(330, 164, s)


def schoolbell(k):   # 墙上的电铃：k 帧小锤来回敲
    s = '<rect x="80" y="10" width="40" height="24" rx="5" fill="#5A6470"/><circle cx="100" cy="100" r="70" fill="#D9A520"/><circle cx="100" cy="100" r="50" fill="#F2C230"/><circle cx="100" cy="100" r="12" fill="#8C6A12"/>'
    a = -14 if k == 0 else 14
    s += f'<g transform="rotate({a} 100 150)"><path d="M100,150 L100,190" stroke="#5A6470" stroke-width="8"/><circle cx="100" cy="196" r="12" fill="#5A6470"/></g>'
    return svg(200, 220, s)


def report():   # 成绩单：醒目的 A+、几颗星
    s = '<rect x="10" y="10" width="240" height="300" rx="10" fill="#FFFDF5" stroke="#C9D6DE" stroke-width="4"/>'
    s += f'<text x="130" y="56" font-size="26" fill="#1A66B8" text-anchor="middle" {CJK}>成绩单</text><text x="130" y="84" font-size="18" fill="#5A6470" text-anchor="middle" {EN}>Report Card</text>'
    for y in (120, 150, 180):
        s += f'<path d="M34,{y} L160,{y}" stroke="#D5DAE1" stroke-width="5"/>'
    s += f'<circle cx="190" cy="220" r="52" fill="none" stroke="#E8304A" stroke-width="7"/><text x="190" y="240" font-size="52" fill="#E8304A" text-anchor="middle" {EN}>A+</text>'
    for x, y in ((50, 230), (90, 262), (60, 286)):
        s += f'<path d="M{x},{y-14} L{x+4},{y-4} L{x+15},{y-4} L{x+6},{y+3} L{x+9},{y+14} L{x},{y+7} L{x-9},{y+14} L{x-6},{y+3} L{x-15},{y-4} L{x-4},{y-4} Z" fill="#F2C230"/>'
    return svg(260, 320, s)


def roadsign():   # 路边的标志牌：前方学校（三角牌、两个小人）
    s = '<rect x="94" y="180" width="12" height="200" fill="#9AA3AE"/><polygon points="100,10 190,170 10,170" fill="#F2C230" stroke="#E8304A" stroke-width="10"/>'
    s += '<circle cx="80" cy="84" r="10" fill="#1B1A1F"/><path d="M80,96 L74,130 M80,100 L64,116 M80,100 L94,112 M76,130 L68,150 M78,130 L88,150" stroke="#1B1A1F" stroke-width="7" stroke-linecap="round"/>'
    s += '<circle cx="118" cy="92" r="9" fill="#1B1A1F"/><path d="M118,102 L114,132 M118,106 L104,118 M114,132 L108,150 M116,132 L126,150" stroke="#1B1A1F" stroke-width="7" stroke-linecap="round"/>'
    s += f'<rect x="40" y="186" width="120" height="36" rx="6" fill="#FFFFFF" stroke="#1B1A1F" stroke-width="3"/><text x="100" y="212" font-size="20" fill="#1B1A1F" text-anchor="middle" {EN}>SCHOOL</text>'
    return svg(200, 384, s)


def icon_sign():
    return svg(200, 200, '<rect x="80" y="20" width="40" height="170" fill="#8B5A2B"/><rect x="80" y="70" width="40" height="22" fill="#E8304A"/><rect x="80" y="92" width="40" height="22" fill="#FFFFFF"/><rect x="80" y="114" width="40" height="22" fill="#E8304A"/>')


def icon_al():
    return svg(200, 200, nest(flag(0), 40, 10, 130, 180))


write_art(ART, 'marktree.svg', marktree()); write_art(ART, 'flag_f0.svg', flag(0)); write_art(ART, 'flag_f1.svg', flag(1))
write_art(ART, 'beacon-bg.svg', beacon_bg(), bg=True); write_art(ART, 'smoke.svg', smoke(), style=False); write_art(ART, 'radiotower.svg', radiotower())
write_art(ART, 'tlight_f0.svg', tlight(0)); write_art(ART, 'tlight_f1.svg', tlight(1)); write_art(ART, 'stoppaddle.svg', stoppaddle()); write_art(ART, 'car.svg', car())
write_art(ART, 'schoolbell_f0.svg', schoolbell(0)); write_art(ART, 'schoolbell_f1.svg', schoolbell(1)); write_art(ART, 'report.svg', report()); write_art(ART, 'roadsign.svg', roadsign())
write_art(ART, 'icon-sign.svg', icon_sign()); write_art(ART, 'icon-al2.svg', icon_al())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
HOLD = (20, 100, 120, 70, 'fist')
sp, rp = stoppaddle(), report()
M['west-woman-guard'] = frames_out(ART, 'west-woman-guard', [holding('west-woman', sp, 420, 40, 90, 202, right='raise', left='point', mouth='open', brows='up', look=1, top='#F2C230', collar='#E8304A'),
                                                           holding('west-woman', sp, 420, 40, 90, 202, right='raise', left='hello', mouth='smile', look=1, top='#F2C230', collar='#E8304A', tilt=2)], fps=1.2, seq='pingpong')
M['west-woman-guard2'] = frames_out(ART, 'west-woman-guard2', [holding('west-woman', sp, 300, 200, 90, 202, left=HOLD, right=HOLD, mouth='laugh', eyes='happy', look=1, top='#F2C230', collar='#E8304A'),
                                                             holding('west-woman', sp, 300, 200, 90, 202, left=HOLD, right=HOLD, mouth='open', brows='up', look=1, top='#F2C230', collar='#E8304A', tilt=3)], fps=1.2, seq='pingpong')
M['cn-boy-report'] = frames_out(ART, 'cn-boy-report', [holding('cn-boy', rp, 296, 226, 128, 158, left=HOLD, right=HOLD, mouth='laugh', eyes='happy', top='#2E9E6A'),
                                                     holding('cn-boy', rp, 296, 226, 128, 158, left=HOLD, right=HOLD, mouth='open', brows='up', top='#2E9E6A', tilt=3)], fps=1.2, seq='pingpong')
M['cn-girl-hike'] = frames_out(ART, 'cn-girl-hike', [person('cn-girl', right='point', look=1, mouth='open', brows='up', top='#E8304A'),
                                                   person('cn-girl', right='pointup', look=1, mouth='laugh', eyes='happy', top='#E8304A', tilt=2)], fps=1.2, seq='pingpong')
M['west-boy-cheer'] = frames_out(ART, 'west-boy-cheer', [person('west-boy', left='raise', right='raise', mouth='laugh', eyes='happy', top='#7FB8E6'),
                                                       person('west-boy', left='hello', right='raise', mouth='open', top='#7FB8E6', tilt=-3)], fps=1.6, seq='pingpong')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

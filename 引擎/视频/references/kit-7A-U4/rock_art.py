import sys, os, math, random, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
R = random.Random(44)
def rockshape(cx, cy, rx, ry, col='#9A958C', hi='#B8B3AA', seed=0):
    r = random.Random(seed); pts = []
    for k in range(10):
        a = math.pi * 2 * k / 10; f = r.uniform(0.82, 1.12)
        pts.append('%.0f,%.0f' % (cx + rx * f * math.cos(a), cy + ry * f * math.sin(a) * (0.75 if math.sin(a) > 0 else 1)))
    s = f'<polygon points="{" ".join(pts)}" fill="{col}"/>'
    s += f'<path d="M{cx-rx*0.5:.0f},{cy-ry*0.3:.0f} L{cx-rx*0.1:.0f},{cy-ry*0.55:.0f} L{cx+rx*0.3:.0f},{cy-ry*0.35:.0f}" fill="none" stroke="{hi}" stroke-width="6"/>'
    s += f'<path d="M{cx-rx*0.2:.0f},{cy:.0f} L{cx+rx*0.15:.0f},{cy+ry*0.2:.0f} M{cx+rx*0.4:.0f},{cy-ry*0.1:.0f} L{cx+rx*0.55:.0f},{cy+ry*0.15:.0f}" stroke="#6E6A62" stroke-width="4"/>'
    return s
def sea_bg():   # 海边：峭壁、灯塔、海上的礁石和浪花、远处的帆船、海鸥、沙滩、贝壳、崖上的小亭子
    d = lg('seSky', [(0, '#7CC4F2'), (1, '#E6F4FB')]) + lg('seSea', [(0, '#2F86C6'), (1, '#4FA9DE')])
    s = '<rect width="1200" height="700" fill="url(#seSky)"/>'
    for cx, cy in ((200, 80), (650, 60), (1050, 100)):
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="80" ry="20" fill="#FFFFFF"/><ellipse cx="{cx+38}" cy="{cy-8}" rx="44" ry="15" fill="#FFFFFF"/>'
    s += '<rect x="0" y="300" width="1200" height="300" fill="url(#seSea)"/>'
    for i in range(75):
        x = R.randint(0, 1180); y = R.randint(310, 560)
        s += f'<path d="M{x},{y} q10,-5 20,0 q10,5 20,0" fill="none" stroke="#CFEAFB" stroke-width="3"/>'
    s += '<path d="M0,120 L160,140 L260,220 L330,300 L360,600 L0,600 Z" fill="#8C7F72"/><path d="M60,150 L150,170 L200,230 M40,260 L180,280 M90,360 L250,380" stroke="#6E6258" stroke-width="6"/>'
    s += '<g transform="translate(120 128) scale(0.4)"><rect x="-90" y="-150" width="12" height="150" fill="#D2232A"/><rect x="78" y="-150" width="12" height="150" fill="#D2232A"/><path d="M-130,-150 C-90,-170 -40,-200 0,-220 C40,-200 90,-170 130,-150 Z" fill="#2A8C6E"/></g>'
    s += '<path d="M1040,320 L1060,120 L1100,120 L1120,320 Z" fill="#F4F1EA"/>' + ''.join(f'<rect x="{1048+k*2}" y="{150+k*50}" width="{64-k*4}" height="22" fill="#D2232A"/>' for k in range(4))
    s += '<rect x="1050" y="96" width="60" height="28" fill="#FFE27A"/><path d="M1044,98 L1080,70 L1116,98 Z" fill="#3A3F4B"/><path d="M1000,330 L1160,330 L1150,300 L1010,300 Z" fill="#8C7F72"/>'
    for (x, y, rx, ry, sd) in ((560, 420, 70, 40, 1), (650, 440, 50, 30, 2), (760, 430, 60, 36, 3)):   # 海里的礁石和浪花
        s += rockshape(x, y, rx, ry, '#7C7468', '#9A9288', sd)
        s += f'<path d="M{x-rx-20},{y+ry*0.6:.0f} C{x-rx},{y+ry*0.2:.0f} {x-rx*0.6:.0f},{y+ry*0.9:.0f} {x-rx*0.3:.0f},{y+ry*0.5:.0f}" fill="none" stroke="#FFFFFF" stroke-width="8"/>'
    s += '<path d="M880,280 L940,280 L930,296 L890,296 Z" fill="#B5432F"/><path d="M910,280 L910,236 L936,276 Z" fill="#FFFFFF"/>'
    for (x, y) in ((420, 160), (470, 190), (820, 140)):
        s += f'<path d="M{x},{y} q12,-12 24,0 q12,-12 24,0" fill="none" stroke="#3A3F4B" stroke-width="4"/>'
    s += '<path d="M0,600 C300,560 700,610 1200,570 L1200,700 L0,700 Z" fill="#EBD3A0"/>'
    for i in range(55):
        s += f'<circle cx="{R.randint(10,1190)}" cy="{R.randint(610,690)}" r="{R.choice([3,4,5])}" fill="{R.choice(["#D9B98A","#FFFFFF","#F7A9A8","#C9A27A"])}"/>'
    for (x, y) in ((300, 650), (980, 640)):
        s += f'<path d="M{x},{y} C{x-14},{y-24} {x+14},{y-24} {x},{y}" fill="#F7A9A8"/>'
    return svg(1200, 700, s, d)
def big_rock():
    s = rockshape(200, 150, 180, 120, '#9A958C', '#BDB8AF', 7) + rockshape(330, 200, 70, 50, '#8E8980', '#B0ABA2', 8)
    s += '<path d="M60,240 C90,230 120,236 150,228" stroke="#5E9E32" stroke-width="8" fill="none"/><circle cx="120" cy="236" r="10" fill="#6DBE45"/>'
    return svg(420, 270, s)
def pebble(c='#8E8980'):
    return svg(80, 60, rockshape(40, 30, 32, 22, c, '#B0ABA2', 3))
def boat():
    s = '<path d="M10,60 L230,60 L200,100 L40,100 Z" fill="#B5432F"/><rect x="110" y="0" width="8" height="62" fill="#5A3A22"/><path d="M118,4 L118,56 L180,56 Z" fill="#F4F1EA"/><path d="M110,10 L110,56 L60,56 Z" fill="#E6D2B5"/>'
    return svg(240, 110, s)
write_art(ART, 'sea-bg.svg', sea_bg(), bg=True); write_art(ART, 'big-rock.svg', big_rock()); write_art(ART, 'pebble.svg', pebble()); write_art(ART, 'sailboat.svg', boat())
pb = open(os.path.join(ART, 'pebble.svg')).read()
M = {}
M['cn-boy-throw'] = frames_out(ART, 'cn-boy-throw', [holding('cn-boy', pb, 500, 70, 50, 38, right=(40, 104, 160, 100, 'fist'), mouth='laugh', eyes='happy', look=1),
                                                   person('cn-boy', right=(70, 104, 80, 100, 'open'), mouth='o', eyes='wide', look=1, tilt=3)], fps=1.2, seq='loop')
M['cn-teacher-hug'] = frames_out(ART, 'cn-teacher-hug', [person('cn-teacher', right=(30, 100, 70, 90, 'open'), mouth='smile', eyes='happy', tilt=-5), person('cn-teacher', right=(30, 100, 74, 90, 'open'), mouth='laugh', eyes='happy', tilt=-2)], fps=1.0, seq='pingpong')
M['cn-boy-proud'] = frames_out(ART, 'cn-boy-proud', [person('cn-boy', left='thumb', mouth='laugh', eyes='happy', tilt=5, top='#F28C28'), person('cn-boy', left='thumb', mouth='smile', eyes='happy', tilt=2, top='#F28C28')], fps=1.2, seq='pingpong')
# 6.29.2：画面设置里 pics / 例句用的是外国男孩、外国女士（中外结合），这里一起画出来
M['west-boy-throw'] = frames_out(ART, 'west-boy-throw', [holding('west-boy', pb, 500, 70, 50, 38, right=(40, 104, 160, 100, 'fist'), mouth='laugh', eyes='happy', look=1),
                                                     person('west-boy', right=(70, 104, 80, 100, 'open'), mouth='o', eyes='wide', look=1, tilt=3)], fps=1.2, seq='loop')
M['west-woman-hug'] = frames_out(ART, 'west-woman-hug', [person('west-woman', right=(30, 100, 70, 90, 'open'), mouth='smile', eyes='happy', tilt=-5), person('west-woman', right=(30, 100, 74, 90, 'open'), mouth='laugh', eyes='happy', tilt=-2)], fps=1.0, seq='pingpong')
M['west-boy-proud'] = frames_out(ART, 'west-boy-proud', [person('west-boy', left='thumb', mouth='laugh', eyes='happy', tilt=5, top='#F28C28'), person('west-boy', left='thumb', mouth='smile', eyes='happy', tilt=2, top='#F28C28')], fps=1.2, seq='pingpong')
json.dump(M, open(os.path.join(ART, 'word_motions.json'), 'w'), ensure_ascii=False, indent=1)
print(list(M))

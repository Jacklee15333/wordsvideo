import sys, os, math, random
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
R = random.Random(3)
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
# ---------------- 城墙（夜里）：欧式城堡城墙、塔楼、火把、城门、远处的山和月亮，加一面中式灯笼
def castle():
    d = lg('csSky', [(0, '#1A2350'), (1, '#3B4A86')]) + lg('csWall', [(0, '#9A8F86'), (1, '#7B716A')])
    s = '<rect width="1200" height="700" fill="url(#csSky)"/><circle cx="980" cy="110" r="48" fill="#FFF3B0"/><circle cx="1000" cy="100" r="44" fill="url(#csSky)"/>'
    for i in range(40):
        s += f'<circle cx="{R.randint(0,1200)}" cy="{R.randint(0,260)}" r="{R.choice([1.5,2,2.5])}" fill="#FFFFFF"/>'
    s += '<path d="M0,330 C150,250 300,280 420,320 C560,250 700,270 820,310 C950,250 1100,270 1200,300 L1200,400 L0,400 Z" fill="#2B3566"/>'
    for x in range(40, 1200, 160):   # 远处敌人的营火
        s += f'<path d="M{x},372 l8,-16 l8,16 Z" fill="#F28C28"/><path d="M{x+30},378 l20,-26 l20,26 Z" fill="#46507A"/>'
    s += '<rect x="0" y="380" width="1200" height="320" fill="url(#csWall)"/>'
    for j in range(8):
        for i in range(26):
            s += f'<rect x="{i*48 + (24 if j%2 else 0) - 20}" y="{400+j*38}" width="44" height="34" rx="3" fill="#8C827A"/>'
    for i in range(13):   # 城垛
        s += f'<rect x="{i*96}" y="340" width="56" height="44" fill="#9A8F86"/>'
    for x in (120, 1080):   # 塔楼
        s += f'<rect x="{x-80}" y="200" width="160" height="500" fill="#8A8079"/><path d="M{x-96},204 L{x},96 L{x+96},204 Z" fill="#6B3A5A"/><rect x="{x-20}" y="260" width="40" height="64" rx="20" fill="#FFD25A"/>'
        for i in range(4):
            s += f'<rect x="{x-80+i*44}" y="170" width="28" height="34" fill="#8A8079"/>'
    s += '<path d="M520,700 L520,560 A80,80 0 0 1 680,560 L680,700 Z" fill="#3A2A1E"/>'
    for i in range(6):
        s += f'<path d="M{532+i*28},540 L{532+i*28},700" stroke="#5A4230" stroke-width="5"/>'
    for x in (300, 900):   # 火把
        s += f'<rect x="{x-5}" y="300" width="10" height="50" fill="#5A3A22"/><path d="M{x},270 C{x-18},292 {x-10},304 {x},304 C{x+10},304 {x+18},292 {x},270 Z" fill="#F28C28"/><circle cx="{x}" cy="294" r="7" fill="#FFE27A"/>'
    s += '<path d="M640,300 L640,240 L700,256 L640,272" fill="#E8304A"/><rect x="636" y="230" width="6" height="110" fill="#5A3A22"/>'
    s += '<ellipse cx="760" cy="320" rx="16" ry="20" fill="#E8304A"/><rect x="752" y="296" width="16" height="6" fill="#F2C230"/><rect x="752" y="338" width="16" height="6" fill="#F2C230"/><path d="M760,250 L760,298" stroke="#5A3A22" stroke-width="3"/>'
    return svg(1200, 700, s, d)
# ---------------- 卧室：床、被子枕头、床头柜、台灯、衣柜、窗帘、窗外日出、地毯、海报、书架（卧室这个词以后也用）
def bedroom():
    d = lg('brW', [(0, '#E8F1FB'), (1, '#CFE0F2')]) + lg('brSky', [(0, '#FFB86B'), (1, '#FFE7A8')]) + lg('brF', [(0, '#D9A066'), (1, '#B97B44')])
    s = '<rect width="1200" height="700" fill="url(#brW)"/>'
    for i in range(0, 1200, 60):
        s += f'<path d="M{i},0 L{i},560" stroke="#DCE8F5" stroke-width="22"/>'
    s += '<rect x="0" y="560" width="1200" height="140" fill="url(#brF)"/>'
    for i in range(0, 1200, 90):
        s += f'<path d="M{i},560 L{i-40},700" stroke="#A8703D" stroke-width="3"/>'
    s += '<rect x="0" y="552" width="1200" height="12" fill="#FFFFFF"/>'
    for i in range(70):
        x = 20 + (i % 14) * 86; y = 30 + (i // 14) * 100
        if 400 < x < 800 and y < 380: continue
        s += f'<path d="M{x},{y} l6,12 l13,2 l-10,9 l3,13 l-12,-7 l-12,7 l3,-13 l-10,-9 l13,-2 Z" fill="#FFFFFF" opacity="0.7"/>'
    # 窗户、日出、窗帘
    s += '<rect x="440" y="90" width="320" height="250" fill="url(#brSky)"/><circle cx="600" cy="300" r="60" fill="#FF8C42"/><path d="M440,300 L760,300 L760,340 L440,340 Z" fill="#7FB069"/>'
    for x in (470, 560, 650, 720):
        s += f'<rect x="{x}" y="{250-(x%40)}" width="30" height="{90+(x%40)}" fill="#B8C4D6"/>'
    s += '<path d="M600,90 L600,340 M440,215 L760,215" stroke="#FFFFFF" stroke-width="10"/><rect x="430" y="80" width="340" height="270" fill="none" stroke="#FFFFFF" stroke-width="14"/>'
    s += '<rect x="400" y="60" width="400" height="12" rx="6" fill="#8C5A2B"/><path d="M400,70 C430,200 400,300 430,380 L470,380 C450,300 470,180 450,70 Z" fill="#E8407A"/><path d="M800,70 C770,200 800,300 770,380 L730,380 C750,300 730,180 750,70 Z" fill="#E8407A"/>'
    s += '<rect x="440" y="340" width="320" height="16" fill="#FFFFFF"/>'
    # 海报、相框、挂钟
    s += '<rect x="120" y="110" width="150" height="200" fill="#2E6FD9"/><circle cx="195" cy="180" r="40" fill="#F2C230"/><path d="M130,300 L195,220 L260,300 Z" fill="#6DBE45"/><text x="195" y="295" font-size="22" fill="#FFF" text-anchor="middle" font-family="sans-serif" font-weight="700">DREAM</text>'
    s += '<rect x="300" y="160" width="80" height="64" fill="#FFFFFF"/><rect x="308" y="168" width="64" height="48" fill="#9ED8F5"/><circle cx="340" cy="190" r="10" fill="#E8304A"/>'
    s += '<rect x="900" y="100" width="90" height="90" fill="#C0392B"/><text x="945" y="164" font-size="56" fill="#F2C230" text-anchor="middle" {CJK}>福</text>'.replace('{CJK}', CJK)
    # 衣柜
    s += '<rect x="1000" y="220" width="200" height="340" fill="#C98B4A"/><path d="M1100,220 L1100,560" stroke="#8C5A2B" stroke-width="5"/><circle cx="1088" cy="390" r="7" fill="#F2C230"/><circle cx="1112" cy="390" r="7" fill="#F2C230"/>'
    s += '<rect x="990" y="208" width="220" height="16" fill="#A8703D"/>'
    # 书架、书
    s += '<rect x="20" y="360" width="200" height="14" fill="#8C5A2B"/><rect x="20" y="440" width="200" height="14" fill="#8C5A2B"/>'
    for i in range(9):
        s += f'<rect x="{28+i*20}" y="{300 + (i%3)*8}" width="16" height="{60-(i%3)*8}" fill="{["#E8304A","#2E6FD9","#F2C230","#6DBE45","#9B5DE5"][i%5]}"/>'
        s += f'<rect x="{28+i*20}" y="{384 + (i%2)*10}" width="16" height="{56-(i%2)*10}" fill="{["#F28C28","#25B5C9","#E8407A","#3E8F3E"][i%4]}"/>'
    s += '<rect x="820" y="500" width="90" height="60" rx="6" fill="#F2C230"/><circle cx="850" cy="490" r="18" fill="#E8407A"/><circle cx="880" cy="492" r="14" fill="#2E6FD9"/><rect x="760" y="520" width="40" height="40" fill="#6DBE45"/>'
    for i in range(10):
        s += f'<circle cx="{780+i*10}" cy="{620+(i%3)*8}" r="3" fill="#C9B8F5"/>'
    # 地毯、拖鞋
    s += '<ellipse cx="600" cy="640" rx="300" ry="44" fill="#7B57D6"/><ellipse cx="600" cy="640" rx="240" ry="30" fill="#9B7BE8"/>'
    s += '<ellipse cx="380" cy="660" rx="30" ry="12" fill="#E8407A"/><ellipse cx="420" cy="664" rx="30" ry="12" fill="#E8407A"/>'
    return svg(1200, 700, s, d)
def bed():
    s = '<rect x="10" y="20" width="40" height="300" rx="10" fill="#A8703D"/><rect x="0" y="10" width="60" height="30" rx="10" fill="#8C5A2B"/>'
    s += '<rect x="40" y="190" width="600" height="80" fill="#C98B4A"/><rect x="620" y="150" width="30" height="170" rx="10" fill="#A8703D"/>'
    s += '<rect x="40" y="150" width="590" height="60" rx="14" fill="#FFFFFF"/><ellipse cx="130" cy="140" rx="80" ry="34" fill="#F9D7E3"/>'
    s += '<path d="M200,130 L630,130 C640,160 640,190 630,210 L200,210 C190,180 190,150 200,130 Z" fill="#2E9BD6"/>'
    for i in range(6):
        s += f'<circle cx="{250+i*65}" cy="{160+(i%2)*20}" r="10" fill="#F2C230"/>'
    return svg(660, 330, s)
def nightstand():
    return svg(200, 200, '<rect x="10" y="40" width="180" height="150" rx="8" fill="#C98B4A"/><rect x="0" y="30" width="200" height="16" rx="5" fill="#A8703D"/><rect x="30" y="80" width="140" height="40" rx="5" fill="#B57A40"/><circle cx="100" cy="100" r="6" fill="#F2C230"/><rect x="30" y="134" width="140" height="40" rx="5" fill="#B57A40"/><circle cx="100" cy="154" r="6" fill="#F2C230"/>')
def clock(shake=0, hand=(0, 0)):
    s = f'<g transform="rotate({shake} 110 120)">'
    s += '<path d="M40,190 L20,220 M180,190 L200,220" stroke="#1B1A1F" stroke-width="8" stroke-linecap="round"/>'
    s += '<circle cx="54" cy="44" r="30" fill="#F2C230"/><circle cx="166" cy="44" r="30" fill="#F2C230"/><path d="M90,30 L130,30" stroke="#1B1A1F" stroke-width="6"/><rect x="104" y="14" width="12" height="20" fill="#1B1A1F"/>'
    s += '<circle cx="110" cy="120" r="88" fill="#E8304A"/><circle cx="110" cy="120" r="70" fill="#FFFFFF"/>'
    for i in range(12):
        a = math.pi * 2 * i / 12
        s += f'<path d="M{110+60*math.sin(a):.0f},{120-60*math.cos(a):.0f} L{110+52*math.sin(a):.0f},{120-52*math.cos(a):.0f}" stroke="#1B1A1F" stroke-width="4"/>'
    s += '<path d="M110,120 L110,72 M110,120 L146,120" stroke="#1B1A1F" stroke-width="7" stroke-linecap="round"/><circle cx="110" cy="120" r="7" fill="#1B1A1F"/>'
    return svg(220, 230, s + '</g>')
def bell(ring=0):
    s = '<rect x="80" y="10" width="40" height="30" rx="6" fill="#B71C1C"/>'
    s += f'<g transform="rotate({ring} 100 40)"><circle cx="100" cy="110" r="80" fill="#E8304A"/><circle cx="100" cy="110" r="56" fill="#FF5A5A"/><circle cx="100" cy="110" r="14" fill="#5A1F1F"/></g>'
    s += f'<text x="100" y="230" font-size="30" fill="#B71C1C" text-anchor="middle" {CJK}>火警</text>'
    return svg(200, 240, s)
def helmet():
    return '<path d="M282,110 C282,40 438,40 438,110 L438,124 L282,124 Z" fill="#B9C2CC"/><path d="M352,36 L368,36 L368,124 L352,124 Z" fill="#8C96A3"/><path d="M360,36 C350,10 380,0 400,20" fill="none" stroke="#E8304A" stroke-width="10" stroke-linecap="round"/>'
def soldier(who, spear_x=None, **kw):
    p = person(who, **kw)
    vb, body = inner(p)
    extra = helmet()
    if spear_x is not None:
        extra += f'<path d="M{spear_x},60 L{spear_x},540" stroke="#7A5232" stroke-width="12"/><path d="M{spear_x-16},70 L{spear_x},10 L{spear_x+16},70 Z" fill="#C9CFD8"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}{extra}</svg>'
def rack():   # 武器架：长矛、盾
    s = '<rect x="20" y="40" width="300" height="16" fill="#7A5232"/><rect x="20" y="300" width="300" height="16" fill="#7A5232"/><rect x="30" y="40" width="14" height="300" fill="#6B4426"/><rect x="296" y="40" width="14" height="300" fill="#6B4426"/>'
    for i in range(4):
        x = 80 + i * 60
        s += f'<path d="M{x},10 L{x},320" stroke="#8C5A2B" stroke-width="10"/><path d="M{x-12},20 L{x},-30 L{x+12},20 Z" fill="#C9CFD8"/>'
    s += '<path d="M120,200 C120,150 200,150 200,200 C200,270 160,300 160,300 C160,300 120,270 120,200 Z" fill="#2E6FD9"/><path d="M160,170 L160,290 M130,210 L190,210" stroke="#F2C230" stroke-width="8"/>'
    return svg(340, 340, s).replace('viewBox="0 0 340 340"', 'viewBox="0 -40 340 380"')
write_art(ART, 'castle-bg.svg', castle(), bg=True); write_art(ART, 'bedroom-bg.svg', bedroom(), bg=True)
write_art(ART, 'bed.svg', bed()); write_art(ART, 'nightstand.svg', nightstand()); write_art(ART, 'rack.svg', rack())
for i, sh in enumerate((-8, 8)):
    write_art(ART, f'clock_f{i}.svg', clock(sh))
write_art(ART, 'clock.svg', clock(0))
for i, r in enumerate((-10, 10)):
    write_art(ART, f'bell_f{i}.svg', bell(r))
M = {}
M['west-man-shout'] = frames_out(ART, 'west-man-shout', [soldier('west-man', left='raise', mouth='o', eyes='wide', brows='up', top='#8C2F39'),
                                                       soldier('west-man', left=(14, 112, 190, 104, 'open'), mouth='laugh', eyes='wide', brows='up', top='#8C2F39', tilt=3)], fps=3, seq='pingpong')
M['cn-boy-guard'] = frames_out(ART, 'cn-boy-guard', [soldier('cn-boy', spear_x=512, right=(30, 100, 170, 60, 'fist'), mouth='flat', look=-1, brows='frown', top='#3E6B48'),
                                                   soldier('cn-boy', spear_x=512, right=(30, 100, 170, 60, 'fist'), mouth='flat', look=1, brows='frown', top='#3E6B48')], fps=0.8, seq='loop')
M['west-boy-run'] = frames_out(ART, 'west-boy-run', [soldier('west-boy', spear_x=208, left=(30, 100, 170, 60, 'fist'), mouth='o', eyes='wide', top='#3E6B48', tilt=-4),
                                                   soldier('west-boy', spear_x=208, left=(30, 100, 170, 60, 'fist'), mouth='o', eyes='wide', top='#3E6B48', tilt=4)], fps=4, seq='pingpong')
M['cn-boy-wake'] = frames_out(ART, 'cn-boy-wake', [person('cn-boy', left='raise', right='raise', mouth='o', eyes='closed', brows='frown', top='#F2C230'),
                                                 person('cn-boy', left=(20, 112, 170, 104, 'open'), right=(20, 112, 170, 104, 'open'), mouth='laugh', eyes='closed', top='#F2C230', tilt=4)], fps=1.5, seq='pingpong')
M['west-woman-shock'] = frames_out(ART, 'west-woman-shock', [person('west-woman', left='chest', right='chest', mouth='o', eyes='wide', brows='up', tilt=-3),
                                                           person('west-woman', left='chest', right='chest', mouth='o', eyes='wide', brows='frown', tilt=3)], fps=3, seq='pingpong')
M['cn-teacher-lead'] = frames_out(ART, 'cn-teacher-lead', [person('cn-teacher', right='point', mouth='open', brows='up', look=1), person('cn-teacher', right=(70, 108, 100, 100, 'point'), mouth='half', look=1, tilt=2)], fps=3)
json.dump(M, open(os.path.join(ART, 'word_motions.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(ART, 'icon-al.svg'), 'w').write(svg(200, 200, '<path d="M20,100 L150,100" stroke="#C2410C" stroke-width="22" stroke-linecap="round"/><path d="M130,60 L190,100 L130,140 Z" fill="#C2410C"/>'))
open(os.path.join(ART, 'icon-arm.svg'), 'w').write(svg(200, 200, nest(open(os.path.join(ART, 'rack.svg')).read(), 10, 10, 180, 190)))
print(list(M))

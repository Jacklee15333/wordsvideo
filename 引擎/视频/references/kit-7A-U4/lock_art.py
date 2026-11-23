import sys, os, math, random, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
R = random.Random(21)
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
# ---------------- 家门口：木门、门锁、门牌、春联、福字、门环、门垫、花盆、信箱、窗户、砖墙、台阶、路灯
def door_bg():
    d = lg('dbW', [(0, '#E9D6B8'), (1, '#D6BE98')]) + lg('dbDoor', [(0, '#B5532E'), (1, '#8E3B1E')])
    s = '<rect width="1200" height="700" fill="url(#dbW)"/>'
    for j in range(22):
        for i in range(26):
            x = i * 48 + (24 if j % 2 else 0) - 24; y = j * 26
            if 420 < x < 790 and y > 60: continue
            s += f'<rect x="{x}" y="{y}" width="44" height="22" rx="2" fill="#D9B48A"/>'
    s += '<rect x="400" y="40" width="400" height="30" fill="#7A4A2A"/><path d="M380,40 L600,0 L820,40 Z" fill="#5E3A22"/>'
    s += '<rect x="430" y="70" width="340" height="560" fill="#6B4426"/><rect x="450" y="90" width="300" height="540" fill="url(#dbDoor)"/>'
    for (x, y) in ((470, 110), (610, 110), (470, 360), (610, 360)):
        s += f'<rect x="{x}" y="{y}" width="120" height="220" rx="6" fill="#A04726"/><rect x="{x+10}" y="{y+10}" width="100" height="200" rx="4" fill="#B5532E"/>'
    s += '<rect x="560" y="80" width="80" height="34" rx="4" fill="#2E6FD9"/><text x="600" y="104" font-size="22" fill="#FFF" text-anchor="middle" font-family="sans-serif" font-weight="700">No. 8</text>'
    s += '<rect x="380" y="110" width="44" height="440" fill="#D2232A"/><rect x="776" y="110" width="44" height="440" fill="#D2232A"/>'
    for k, ch in enumerate('平安如意'):
        s += f'<text x="402" y="{180+k*100}" font-size="36" fill="#1B1A1F" text-anchor="middle" {CJK}>{ch}</text>'
    for k, ch in enumerate('出入平安'):
        s += f'<text x="798" y="{180+k*100}" font-size="36" fill="#1B1A1F" text-anchor="middle" {CJK}>{ch}</text>'
    s += f'<rect x="562" y="30" width="76" height="76" fill="#D2232A" transform="rotate(45 600 68)"/><text x="600" y="82" font-size="40" fill="#F2C230" text-anchor="middle" {CJK}>福</text>'
    s += '<circle cx="600" cy="300" r="22" fill="none" stroke="#C9A227" stroke-width="7"/><circle cx="600" cy="278" r="8" fill="#C9A227"/>'
    s += '<rect x="700" y="340" width="26" height="70" rx="6" fill="#C9CFD8"/><circle cx="713" cy="360" r="6" fill="#3A3F4B"/><rect x="710" y="366" width="6" height="16" fill="#3A3F4B"/>'
    s += '<rect x="380" y="630" width="440" height="24" fill="#B9B2A6"/><rect x="350" y="654" width="500" height="46" fill="#A8A196"/>'
    s += '<rect x="520" y="610" width="160" height="22" rx="6" fill="#6B8E23"/><text x="600" y="627" font-size="16" fill="#F4F1EA" text-anchor="middle" font-family="sans-serif" font-weight="700">WELCOME</text>'
    for x in (300, 900):
        s += f'<path d="M{x-40},700 L{x-30},610 L{x+30},610 L{x+40},700 Z" fill="#C0643A"/><circle cx="{x}" cy="580" r="44" fill="#3E8F3E"/><circle cx="{x-26}" cy="560" r="26" fill="#56A94F"/><circle cx="{x+24}" cy="556" r="24" fill="#4E9A47"/>'
        for k in range(6):
            s += f'<circle cx="{x-30+k*12}" cy="{548+(k%2)*14}" r="6" fill="{["#E8304A","#F2C230","#FF7AA2"][k%3]}"/>'
    for x in (80, 1000):
        s += f'<rect x="{x}" y="160" width="140" height="180" fill="#9ED0EE"/><path d="M{x+70},160 L{x+70},340 M{x},250 L{x+140},250" stroke="#FFFFFF" stroke-width="8"/><rect x="{x-10}" y="150" width="160" height="200" fill="none" stroke="#7A4A2A" stroke-width="10"/><rect x="{x-14}" y="350" width="168" height="14" fill="#7A4A2A"/>'
    s += '<rect x="1040" y="430" width="90" height="70" rx="10" fill="#2E7D32"/><rect x="1080" y="500" width="10" height="130" fill="#3A3F4B"/><rect x="1050" y="452" width="70" height="8" fill="#1B5E20"/>'
    s += '<rect x="250" y="380" width="8" height="250" fill="#3A3F4B"/><path d="M230,380 L278,380 L270,350 L238,350 Z" fill="#FFE27A"/>'
    return svg(1200, 700, s, d)
# ---------------- 运河和船闸：两岸石堤、闸门、闸室里的水、船、岸边的白墙黛瓦和欧式小楼、柳树、石桥、远山
def canal_bg():
    d = lg('cnSky', [(0, '#8CC8EE'), (1, '#E3F4FF')]) + lg('cnW', [(0, '#3F9AD6'), (1, '#2B78B0')])
    s = '<rect width="1200" height="700" fill="url(#cnSky)"/>'
    s += '<path d="M0,260 C150,190 300,220 420,250 C560,180 720,200 860,240 C980,190 1100,210 1200,230 L1200,320 L0,320 Z" fill="#8FBF9A"/>'
    s += '<path d="M0,290 C200,250 400,280 600,270 C800,255 1000,280 1200,265 L1200,330 L0,330 Z" fill="#6FAF7E"/>'
    for x in (60, 200, 860, 1020):   # 白墙黛瓦
        s += f'<rect x="{x}" y="250" width="110" height="80" fill="#F4F1EA"/><path d="M{x-10},252 L{x+55},222 L{x+120},252 Z" fill="#3A3F4B"/><rect x="{x+40}" y="290" width="26" height="40" fill="#6B4426"/><rect x="{x+12}" y="272" width="18" height="16" fill="#9ED0EE"/><rect x="{x+80}" y="272" width="18" height="16" fill="#9ED0EE"/>'
    s += '<rect x="1110" y="200" width="70" height="130" fill="#E6D2B5"/><path d="M1100,204 L1145,160 L1190,204 Z" fill="#B5432F"/>'
    for k in range(4):   # 风车
        a = math.radians(45 + k * 90); s += f'<path d="M700,210 L{700+70*math.cos(a):.0f},{210+70*math.sin(a):.0f}" stroke="#F4F1EA" stroke-width="14"/>'
    s += '<path d="M690,215 L684,330 L716,330 L710,215 Z" fill="#C98B4A"/><circle cx="700" cy="210" r="8" fill="#5A3A22"/>'
    # 两岸石堤
    s += '<path d="M0,330 L1200,330 L1200,380 L0,380 Z" fill="#B9B2A6"/><path d="M0,620 L1200,620 L1200,700 L0,700 Z" fill="#B9B2A6"/>'
    for j in range(2):
        for i in range(30):
            s += f'<rect x="{i*42+(21 if j%2 else 0)-20}" y="{340+j*20}" width="38" height="16" fill="#A39C90"/><rect x="{i*42+(21 if j%2 else 0)-20}" y="{630+j*30}" width="38" height="24" fill="#A39C90"/>'
    s += '<rect x="0" y="380" width="1200" height="240" fill="url(#cnW)"/>'
    for i in range(26):
        x = R.randint(10, 1180); y = R.randint(395, 600)
        s += f'<path d="M{x},{y} q12,-5 24,0 q12,5 24,0" fill="none" stroke="#BFE3F8" stroke-width="3"/>'
    for x in (420, 780):   # 两道闸门
        s += f'<rect x="{x-14}" y="300" width="28" height="330" fill="#5A3A22"/><rect x="{x-40}" y="290" width="80" height="22" fill="#7A4A2A"/><circle cx="{x}" cy="300" r="18" fill="#C9A227"/>'
        for k in range(6):
            s += f'<path d="M{x-14},{330+k*50} L{x+14},{350+k*50}" stroke="#3A281D" stroke-width="4"/>'
    s += '<text x="600" y="320" font-size="28" fill="#1F3E8A" text-anchor="middle" ' + CJK + '>船闸 LOCK</text>'
    for x in (120, 1090):
        s += f'<g transform="translate({x} 330) scale(0.75)"><path d="M-8,0 C-10,-60 -4,-110 0,-150 L10,-150 C8,-100 12,-50 10,0 Z" fill="#7A5232"/><ellipse cx="0" cy="-160" rx="70" ry="45" fill="#6BAF3C"/>' + ''.join(f'<path d="M{-60+i*9.5:.0f},-170 C{-66+i*9.5:.0f},-120 {-56+i*9.5:.0f},-80 {-63+i*9.5:.0f},-40" fill="none" stroke="#5E9E32" stroke-width="7"/>' for i in range(14)) + '</g>'
    return svg(1200, 700, s, d)
def padlock(open_=False):
    s = ('<path d="M50,110 L50,60 C50,10 150,10 150,60 L150,110" fill="none" stroke="#9AA3AE" stroke-width="22"/>' if not open_ else
         '<path d="M50,110 L50,60 C50,10 150,10 150,60 L150,70" fill="none" stroke="#9AA3AE" stroke-width="22" transform="translate(0 -36)"/>')
    s += '<rect x="20" y="100" width="160" height="130" rx="18" fill="#E0A63A"/><rect x="20" y="100" width="160" height="26" rx="12" fill="#F2C230"/><circle cx="100" cy="160" r="16" fill="#3A3F4B"/><rect x="94" y="164" width="12" height="36" rx="4" fill="#3A3F4B"/>'
    return svg(200, 240, s)
def key(ang=0):
    return svg(200, 200, f'<g transform="rotate({ang} 100 100)"><circle cx="50" cy="100" r="34" fill="#E0A63A"/><circle cx="50" cy="100" r="14" fill="#FFFFFF"/><rect x="80" y="92" width="100" height="16" rx="4" fill="#E0A63A"/><rect x="150" y="108" width="10" height="20" fill="#E0A63A"/><rect x="168" y="108" width="10" height="14" fill="#E0A63A"/></g>')
def latch(pos=0):   # 门闩：一根木插销滑进铁环里（pos 0 开、1 插上）
    x = 60 + pos * 120
    s = '<rect x="0" y="0" width="400" height="260" fill="#8E3B1E"/><rect x="200" y="0" width="8" height="260" fill="#5E2A14"/>'
    for (bx) in (60, 120, 300):
        s += f'<rect x="{bx}" y="100" width="30" height="60" rx="6" fill="none" stroke="#3A3F4B" stroke-width="10"/>'
    s += f'<rect x="{x}" y="112" width="190" height="36" rx="8" fill="#C98B4A"/><circle cx="{x+20}" cy="130" r="10" fill="#7A4A2A"/>'
    return svg(400, 260, s)
def boat():
    s = '<path d="M10,80 L290,80 L250,130 L50,130 Z" fill="#C0392B"/><rect x="90" y="40" width="110" height="42" fill="#F4F1EA"/><rect x="104" y="50" width="22" height="18" fill="#9ED0EE"/><rect x="140" y="50" width="22" height="18" fill="#9ED0EE"/><rect x="174" y="50" width="16" height="18" fill="#9ED0EE"/>'
    s += '<rect x="210" y="20" width="10" height="62" fill="#5A3A22"/><path d="M220,24 L262,38 L220,52 Z" fill="#2E6FD9"/><path d="M40,100 L270,100" stroke="#F2C230" stroke-width="6"/>'
    return svg(300, 140, s)
def water(level):   # 闸室里的水（level 0–3，水位一点点涨）
    h = 80 + level * 50
    return svg(360, 280, f'<rect x="0" y="{280-h}" width="360" height="{h}" fill="#3F9AD6"/><path d="M0,{280-h} q30,-8 60,0 q30,8 60,0 q30,-8 60,0 q30,8 60,0 q30,-8 60,0 q30,8 60,0" fill="#7CC4F2"/>')
def drawer(stuck=0):
    s = '<rect x="10" y="10" width="300" height="200" rx="8" fill="#C98B4A"/><rect x="30" y="30" width="260" height="70" rx="6" fill="#B57A40"/><rect x="30" y="120" width="260" height="70" rx="6" fill="#B57A40"/>'
    s += f'<rect x="135" y="56" width="50" height="14" rx="6" fill="#E0A63A" transform="translate({stuck*6} 0)"/><rect x="135" y="146" width="50" height="14" rx="6" fill="#E0A63A"/><circle cx="160" cy="88" r="6" fill="#3A3F4B"/>'
    return svg(320, 220, s)
write_art(ART, 'door-bg.svg', door_bg(), bg=True); write_art(ART, 'canal-bg.svg', canal_bg(), bg=True)
write_art(ART, 'padlock.svg', padlock()); write_art(ART, 'padlock-open.svg', padlock(True)); write_art(ART, 'boat.svg', boat())
for i, a in enumerate((0, 45, 90)): write_art(ART, f'key_f{i}.svg', key(a))
for i, p in enumerate((0, 0.5, 1)): write_art(ART, f'latch_f{i}.svg', latch(p))
for i in range(4): write_art(ART, f'water_f{i}.svg', water(i))
write_art(ART, 'drawer.svg', drawer())
M = {}
kk = open(os.path.join(ART, 'key_f0.svg')).read(); kk2 = open(os.path.join(ART, 'key_f2.svg')).read()
M['cn-girl-lock'] = frames_out(ART, 'cn-girl-lock', [holding('cn-girl', kk, 575, 272, 90, 90, right=(56, 104, 96, 92, 'fist'), mouth='smile', look=1),
                                                   holding('cn-girl', kk2, 575, 272, 90, 90, right=(58, 104, 92, 92, 'fist'), mouth='smile', look=1, tilt=3)], fps=1.5, seq='pingpong')
M['west-man-push'] = frames_out(ART, 'west-man-push', [person('west-man', left='point', right=(64, 104, 96, 96, 'open'), mouth='flat', brows='frown', look=1),
                                                     person('west-man', left=(70, 104, 92, 96, 'open'), right=(64, 104, 96, 96, 'open'), mouth='o', brows='frown', look=1, tilt=3)], fps=2.5, seq='pingpong')
M['west-boy-wave'] = frames_out(ART, 'west-boy-wave', [person('west-boy', left='wave1', mouth='laugh', eyes='happy'), person('west-boy', left='wave2', mouth='smile', eyes='happy', tilt=3)], fps=3, seq='pingpong')
M['cn-boy-pull'] = frames_out(ART, 'cn-boy-pull', [person('cn-boy', right=(40, 100, 80, 90, 'fist'), mouth='o', brows='frown', look=1, tilt=-3), person('cn-boy', right=(46, 100, 84, 90, 'fist'), mouth='flat', brows='frown', look=1, tilt=3)], fps=3, seq='pingpong')
json.dump(M, open(os.path.join(ART, 'word_motions.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(ART, 'icon-lock.svg'), 'w').write(svg(200, 200, nest(open(os.path.join(ART, 'padlock.svg')).read(), 25, 0, 150, 190)))
print(list(M))

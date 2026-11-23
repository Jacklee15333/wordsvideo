import sys, os, math, random, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
R = random.Random(33)
def wild_bg():   # 山林：远山、云、瀑布、河、松树和阔叶树、小木屋、远处的亭子、石头、草丛、小路
    d = lg('wdSky', [(0, '#8CC8EE'), (1, '#E6F4FB')])
    s = '<rect width="1200" height="700" fill="url(#wdSky)"/>'
    for k, (base, col, amp) in enumerate(((260, '#9DB7C9', 90), (320, '#7FA88E', 70), (380, '#5E9A6B', 60))):
        pts = ' '.join('%d,%d' % (x, base - amp * abs(math.sin(x / (140 + k * 40) + k)) - R.randint(0, 20)) for x in range(0, 1201, 60))
        s += f'<polygon points="0,700 {pts} 1200,700" fill="{col}"/>'
    for cx, cy in ((180, 90), (620, 70), (1000, 110)):
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="80" ry="18" fill="#FFFFFF"/><ellipse cx="{cx+40}" cy="{cy-8}" rx="44" ry="14" fill="#FFFFFF"/>'
    s += '<path d="M860,200 L880,200 L900,420 L850,420 Z" fill="#DCEFFA"/><path d="M866,210 L870,410 M884,210 L890,410" stroke="#FFFFFF" stroke-width="3"/>'
    s += '<g transform="translate(330 250) scale(0.5)"><rect x="-90" y="-150" width="12" height="150" fill="#D2232A"/><rect x="78" y="-150" width="12" height="150" fill="#D2232A"/><path d="M-130,-150 C-90,-170 -40,-200 0,-220 C40,-200 90,-170 130,-150 Z" fill="#2A8C6E"/></g>'
    s += '<path d="M0,520 C200,480 420,560 640,500 C840,450 1000,520 1200,480 L1200,560 C1000,600 820,540 640,590 C420,640 200,560 0,600 Z" fill="#4FA3D9"/>'
    for i in range(14):
        x = R.randint(20, 1160); y = R.randint(500, 590)
        s += f'<path d="M{x},{y} q10,-4 20,0 q10,4 20,0" fill="none" stroke="#CFEAFB" stroke-width="3"/>'
    s += '<path d="M0,600 C200,560 420,640 640,590 C840,540 1000,600 1200,560 L1200,700 L0,700 Z" fill="#6DBE45"/>'
    s += '<path d="M520,700 C560,660 600,640 660,600 L700,600 C660,640 640,670 620,700 Z" fill="#D9C08C"/>'
    for i in range(30):
        s += f'<circle cx="{R.randint(0,1200)}" cy="{R.randint(615,690)}" r="5" fill="{R.choice(["#E8304A","#F2C230","#FFFFFF","#9B5DE5"])}"/>'
    for i in range(60):
        x = R.randint(0, 1200); y = R.randint(610, 695)
        s += f'<path d="M{x},{y} l-4,-12 M{x},{y} l0,-14 M{x},{y} l4,-12" stroke="#3E8F2C" stroke-width="2"/>'
    for (x, y, k) in ((80, 470, 1.2), (190, 480, 0.9), (980, 470, 1.1), (1100, 480, 1.3), (760, 440, 0.7)):   # 松树
        s += f'<g transform="translate({x} {y}) scale({k})"><rect x="-6" y="-20" width="12" height="40" fill="#6B4426"/>' + ''.join(f'<path d="M0,{-150+j*35} L{-40-j*8},{-90+j*35} L{40+j*8},{-90+j*35} Z" fill="{["#2F7D46","#3A8F52","#2F7D46","#28703E"][j]}"/>' for j in range(4)) + '</g>'
    for (x, y, k) in ((300, 600, 1.0), (880, 600, 0.9)):   # 阔叶树
        s += f'<g transform="translate({x} {y}) scale({k})"><rect x="-9" y="-80" width="18" height="82" fill="#7A5232"/><circle cx="0" cy="-120" r="56" fill="#3F8F46"/><circle cx="-36" cy="-96" r="36" fill="#4FA356"/><circle cx="36" cy="-98" r="38" fill="#4FA356"/></g>'
    s += '<rect x="620" y="400" width="90" height="60" fill="#B07A43"/><path d="M610,402 L665,360 L720,402 Z" fill="#8C3B2E"/><rect x="652" y="425" width="22" height="35" fill="#5A3A22"/>'
    for (x, y, r) in ((420, 640, 34), (460, 650, 24), (1000, 650, 30), (150, 660, 26)):
        s += f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*0.7:.0f}" fill="#9A958C"/><ellipse cx="{x-r*0.3:.0f}" cy="{y-r*0.25:.0f}" rx="{r*0.4:.0f}" ry="{r*0.2:.0f}" fill="#B8B3AA"/>'
    return svg(1200, 700, s, d)
def bird(up=True):
    w = 'M10,30 C30,0 50,10 60,30 C70,10 90,0 110,30' if up else 'M10,20 C30,40 50,40 60,30 C70,40 90,40 110,20'
    return svg(120, 60, f'<path d="{w}" fill="none" stroke="#3A3F4B" stroke-width="8" stroke-linecap="round"/><ellipse cx="60" cy="32" rx="12" ry="8" fill="#3A3F4B"/>')
def binoculars():
    return svg(200, 120, '<rect x="20" y="20" width="70" height="90" rx="20" fill="#2B2D33"/><rect x="110" y="20" width="70" height="90" rx="20" fill="#2B2D33"/><rect x="80" y="40" width="40" height="30" fill="#3A3D45"/><circle cx="55" cy="95" r="22" fill="#2563EB"/><circle cx="145" cy="95" r="22" fill="#2563EB"/>')
def magnifier():
    return svg(200, 200, '<circle cx="80" cy="80" r="60" fill="#CFEFFF" opacity="0.8"/><circle cx="80" cy="80" r="60" fill="none" stroke="#C9A227" stroke-width="14"/><rect x="120" y="120" width="70" height="22" rx="10" fill="#7A4A2A" transform="rotate(45 120 120)"/><path d="M50,60 C60,48 76,44 90,46" stroke="#FFFFFF" stroke-width="6" fill="none"/>')
def leaf():
    return svg(200, 160, '<path d="M20,140 C20,60 100,10 180,20 C170,100 110,150 20,140 Z" fill="#4FA356"/><path d="M20,140 C80,100 130,60 180,20 M60,110 L70,70 M100,85 L120,55 M90,95 L130,100" fill="none" stroke="#2F7D46" stroke-width="5"/>')
def board_q():
    return svg(300, 200, '<rect x="0" y="0" width="300" height="200" rx="8" fill="#2E5E4E"/><text x="150" y="130" font-size="110" fill="#F4F1EA" text-anchor="middle" font-family="serif" font-weight="700">?</text>')
write_art(ART, 'wild-bg.svg', wild_bg(), bg=True)
write_art(ART, 'bird_f0.svg', bird(True)); write_art(ART, 'bird_f1.svg', bird(False))
for n, f in (('binoculars.svg', binoculars), ('magnifier.svg', magnifier), ('leaf.svg', leaf), ('board-q.svg', board_q)):
    write_art(ART, n, f())
bn = open(os.path.join(ART, 'binoculars.svg')).read(); mg = open(os.path.join(ART, 'magnifier.svg')).read()
mp = open(os.path.join(ART, 'map.svg')).read() if os.path.exists(os.path.join(ART, 'map.svg')) else None
HOLD = (18, 92, 212, 100, 'fist')
M = {}
M['west-woman-look'] = frames_out(ART, 'west-woman-look', [holding('west-woman', bn, 296, 120, 128, 77, left=HOLD, right=HOLD, mouth='smile'),
                                                         holding('west-woman', bn, 300, 122, 128, 77, left=HOLD, right=HOLD, mouth='o', tilt=4)], fps=0.8, seq='pingpong')
M['west-man-call'] = frames_out(ART, 'west-man-call', [person('west-man', left=(-6, 72, 205, 120, 'open'), mouth='o', eyes='wide', brows='up', top='#5E7D3A'),
                                                     person('west-man', left=(-6, 72, 205, 120, 'open'), right='raise', mouth='laugh', eyes='wide', brows='up', top='#5E7D3A', tilt=3)], fps=2.5, seq='pingpong')
M['cn-girl-study'] = frames_out(ART, 'cn-girl-study', [holding('cn-girl', mg, 420, 230, 120, 120, right=(40, 100, 120, 80, 'fist'), mouth='o', eyes='wide', look=1, brows='up'),
                                                     holding('cn-girl', mg, 424, 226, 120, 120, right=(40, 100, 124, 80, 'fist'), mouth='smile', eyes='wide', look=1, tilt=3)], fps=1.2, seq='pingpong')
M['west-boy-think'] = frames_out(ART, 'west-boy-think', [person('west-boy', right='chin', mouth='flat', look=-1, brows='one'), person('west-boy', right='chin', mouth='flat', look=1, brows='one', tilt=-3)], fps=0.8, seq='loop')
M['cn-boy-hike'] = frames_out(ART, 'cn-boy-hike', [person('cn-boy', right='pointup', mouth='open', look=1, brows='up', top='#F28C28'), person('cn-boy', right=(64, 104, 118, 100, 'point'), mouth='laugh', look=1, top='#F28C28', tilt=2)], fps=2.5)
json.dump(M, open(os.path.join(ART, 'word_motions.json'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(ART, 'icon-ex.svg'), 'w').write(svg(200, 200, '<rect x="20" y="40" width="90" height="120" rx="8" fill="#B07A43"/><path d="M80,100 L180,100" stroke="#C2410C" stroke-width="20" stroke-linecap="round"/><path d="M160,60 L196,100 L160,140 Z" fill="#C2410C"/>'))
open(os.path.join(ART, 'icon-plor.svg'), 'w').write(svg(200, 200, nest(person('west-man', left=(-6, 72, 205, 120, 'open'), mouth='o', eyes='wide', top='#5E7D3A'), -20, 0, 240, 190)))
print(list(M))

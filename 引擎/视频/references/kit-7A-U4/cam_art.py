import sys, os, random, math
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
import importlib.util as _u
_sp=_u.spec_from_file_location('scn', SK+'/scripts/scenes.py')
sys.argv_bak=sys.argv; sys.argv=['x','/tmp/_scn']; os.makedirs('/tmp/_scn',exist_ok=True)
_m=_u.module_from_spec(_sp); _sp.loader.exec_module(_m); traveler=_m.traveler; sys.argv=sys.argv_bak
ART = sys.argv[1]
R = random.Random(11)
# ---------------------------------------------------------------- 公园（中国的亭子、石拱桥、柳树 + 西式的钟楼、喷泉、路灯长椅）
def willow(x, y, k=1.0):
    s = f'<g transform="translate({x} {y}) scale({k})"><path d="M-8,0 C-10,-60 -4,-110 0,-150 L10,-150 C8,-100 12,-50 10,0 Z" fill="#7A5232"/>'
    s += '<ellipse cx="0" cy="-160" rx="70" ry="45" fill="#6BAF3C"/>'
    for i in range(14):
        a = -60 + i * 9.5
        s += f'<path d="M{a:.0f},-170 C{a-6:.0f},-120 {a+4:.0f},-80 {a-3:.0f},-40" fill="none" stroke="#5E9E32" stroke-width="7" stroke-linecap="round"/>'
    return s + '</g>'
def roundtree(x, y, k=1.0, c=('#2F8F46', '#3DA557', '#56BD6A')):
    return (f'<g transform="translate({x} {y}) scale({k})"><rect x="-8" y="-70" width="16" height="72" fill="#7A5232"/>'
            f'<circle cx="0" cy="-110" r="52" fill="{c[0]}"/><circle cx="-34" cy="-88" r="34" fill="{c[1]}"/><circle cx="34" cy="-90" r="36" fill="{c[1]}"/><circle cx="-6" cy="-136" r="32" fill="{c[2]}"/></g>')
def bench(x, y, k=1.0):
    s = f'<g transform="translate({x} {y}) scale({k})">'
    s += '<rect x="-60" y="-40" width="120" height="10" rx="3" fill="#B5652A"/><rect x="-60" y="-26" width="120" height="10" rx="3" fill="#B5652A"/>'
    s += '<rect x="-64" y="-8" width="128" height="10" rx="3" fill="#C8773A"/><rect x="-56" y="0" width="8" height="26" fill="#3A3F4B"/><rect x="48" y="0" width="8" height="26" fill="#3A3F4B"/>'
    return s + '</g>'
def lamp(x, y):
    return (f'<g transform="translate({x} {y})"><rect x="-5" y="-200" width="10" height="200" fill="#2E3A4A"/><rect x="-12" y="-10" width="24" height="10" fill="#2E3A4A"/>'
            '<path d="M-18,-200 L18,-200 L12,-236 L-12,-236 Z" fill="#FFE27A"/><path d="M-22,-238 L22,-238 L0,-256 Z" fill="#2E3A4A"/></g>')
def pavilion(x, y, k=1.0):
    s = f'<g transform="translate({x} {y}) scale({k})">'
    s += '<rect x="-110" y="-20" width="220" height="24" fill="#D9CBB0"/><rect x="-120" y="2" width="240" height="14" fill="#C4B393"/>'
    for cx in (-90, -30, 30, 90):
        s += f'<rect x="{cx-7}" y="-170" width="14" height="152" fill="#D2232A"/>'
    s += '<rect x="-100" y="-60" width="200" height="8" fill="#D2232A"/><rect x="-100" y="-178" width="200" height="16" fill="#1F6E5A"/>'
    s += '<path d="M-150,-170 C-120,-180 -60,-215 0,-250 C60,-215 120,-180 150,-170 C120,-178 70,-190 0,-196 C-70,-190 -120,-178 -150,-170 Z" fill="#2A8C6E"/>'
    s += '<path d="M-150,-170 C-162,-178 -166,-190 -158,-196" fill="none" stroke="#2A8C6E" stroke-width="8"/><path d="M150,-170 C162,-178 166,-190 158,-196" fill="none" stroke="#2A8C6E" stroke-width="8"/>'
    s += '<circle cx="0" cy="-258" r="10" fill="#F2C230"/><rect x="-36" y="-172" width="72" height="14" fill="#1F3E8A"/>'
    for i in range(9):
        s += f'<path d="M{-120+i*30},-176 L{-110+i*30},-200" stroke="#1F6E5A" stroke-width="3"/>'
    return s + '</g>'
def clocktower(x, y, k=1.0):
    s = f'<g transform="translate({x} {y}) scale({k})"><rect x="-26" y="-210" width="52" height="210" fill="#C9A27A"/><path d="M-32,-210 L32,-210 L0,-270 Z" fill="#6B4E9A"/>'
    s += '<circle cx="0" cy="-170" r="16" fill="#FFFFFF"/><path d="M0,-170 L0,-182 M0,-170 L9,-166" stroke="#222" stroke-width="2.5"/>'
    for yy in (-120, -80, -40):
        s += f'<rect x="-10" y="{yy}" width="20" height="26" rx="10" fill="#4A6FA5"/>'
    return s + '</g>'
def park():
    d = lg('pkSky', [(0, '#5BB8F5'), (1, '#D9F0FF')]) + lg('pkLake', [(0, '#3FA6E0'), (1, '#7CCBF0')]) + lg('pkGrass', [(0, '#7CC64E'), (1, '#58A83A')])
    s = '<rect width="1200" height="700" fill="url(#pkSky)"/>'
    for cx, cy, rx in ((150, 80, 80), (420, 60, 60), (880, 90, 90), (1080, 60, 60)):
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx*0.3:.0f}" fill="#FFFFFF"/><ellipse cx="{cx+rx*0.4:.0f}" cy="{cy-8}" rx="{rx*0.5:.0f}" ry="{rx*0.25:.0f}" fill="#FFFFFF"/>'
    # 风筝
    s += '<path d="M980,120 L1010,150 L980,190 L950,150 Z" fill="#E8304A"/><path d="M980,120 L980,190 M950,150 L1010,150" stroke="#FFF" stroke-width="2"/>'
    s += '<path d="M980,190 C990,230 960,260 975,300 C985,330 1000,350 1010,380" fill="none" stroke="#555" stroke-width="2"/>'
    s += '<path d="M980,196 l8,8 M976,214 l-8,6 M985,232 l8,6" stroke="#F2C230" stroke-width="5"/>'
    # 远处的山和城市
    s += '<path d="M0,300 C120,220 240,250 330,290 C430,230 560,230 650,285 C760,220 900,230 1000,280 C1080,240 1150,250 1200,270 L1200,330 L0,330 Z" fill="#9DCB8E"/>'
    for x, w, h, c in ((40, 60, 120, '#B8C4D6'), (110, 50, 90, '#C9D3E2'), (780, 70, 140, '#B8C4D6'), (860, 50, 100, '#C9D3E2'), (1120, 60, 130, '#B8C4D6')):
        s += f'<rect x="{x}" y="{330-h}" width="{w}" height="{h}" fill="{c}"/>'
        for yy in range(330 - h + 12, 322, 22):
            for xx in range(x + 8, x + w - 8, 16):
                s += f'<rect x="{xx}" y="{yy}" width="8" height="10" fill="#EAF2FB"/>'
    s += clocktower(930, 330, 0.75)
    # 宝塔（远处）
    s += '<g transform="translate(260 330)">' + ''.join(f'<rect x="{-22+i*3}" y="{-30-i*28}" width="{44-i*6}" height="26" fill="#C98B4A"/><path d="M{-34+i*3},{-30-i*28} L{34-i*3},{-30-i*28} L{26-i*3},{-40-i*28} L{-26+i*3},{-40-i*28} Z" fill="#7A3B2A"/>' for i in range(6)) + '<path d="M0,-210 L0,-232" stroke="#7A3B2A" stroke-width="4"/></g>'
    # 湖
    s += '<path d="M0,330 L1200,330 L1200,430 C1000,450 800,420 600,440 C400,455 200,430 0,445 Z" fill="url(#pkLake)"/>'
    for i in range(16):
        x = R.randint(20, 1160); y = R.randint(345, 420)
        s += f'<path d="M{x},{y} q12,-5 24,0 q12,5 24,0" fill="none" stroke="#E6F6FF" stroke-width="3"/>'
    s += '<path d="M690,360 L770,360 L760,378 L700,378 Z" fill="#F28C28"/><path d="M730,360 L730,330 L752,356 Z" fill="#FFFFFF"/>'
    for x in (520, 556):
        s += f'<ellipse cx="{x}" cy="395" rx="14" ry="8" fill="#FFFFFF"/><circle cx="{x+10}" cy="385" r="6" fill="#FFFFFF"/><path d="M{x+15},385 l7,2" stroke="#F28C28" stroke-width="3"/>'
    # 石拱桥
    s += '<path d="M380,380 C420,320 520,320 560,380 L560,395 L380,395 Z" fill="#D8D2C4"/><path d="M405,395 C430,350 510,350 535,395 Z" fill="#3FA6E0"/>'
    for i in range(8):
        s += f'<rect x="{392+i*21}" y="{334 + abs(3.5-i)*6:.0f}" width="5" height="16" fill="#BDB4A2"/>'
    # 草地和小路
    s += '<path d="M0,440 C200,428 400,452 600,438 C800,425 1000,448 1200,432 L1200,700 L0,700 Z" fill="url(#pkGrass)"/>'
    s += '<path d="M470,700 C520,600 560,520 600,450 L660,450 C700,520 760,600 830,700 Z" fill="#E6D3A8"/>'
    for i in range(14):
        y = 460 + i * 17; w = 30 + i * 9
        s += f'<path d="M{630-w/2:.0f},{y} l{w*0.3:.0f},0" stroke="#D2BC8C" stroke-width="3"/>'
    for i in range(60):
        x = R.randint(0, 1200); y = R.randint(460, 690)
        if 440 < x < 860 and y > 450: continue
        s += f'<path d="M{x},{y} l-4,-10 M{x},{y} l0,-12 M{x},{y} l4,-10" stroke="#3E8F2C" stroke-width="2"/>'
    s += pavilion(170, 470, 0.95) + willow(380, 470, 0.9) + willow(1060, 470, 1.0) + roundtree(60, 470, 0.9) + roundtree(1170, 480, 0.8, ('#3B9A55', '#4CB062', '#68C97A'))
    s += roundtree(880, 455, 0.6) + roundtree(320, 450, 0.55)
    s += bench(930, 560, 1.0) + lamp(840, 600) + lamp(360, 640)
    # 花坛
    for (x, y, w) in ((20, 610, 200), (960, 640, 220)):
        s += f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="8" fill="#A9784A"/><rect x="{x+4}" y="{y-14}" width="{w-8}" height="20" rx="10" fill="#3E8F3E"/>'
        for i in range(int(w / 10)):
            s += f'<circle cx="{x+8+i*10+R.uniform(-2,2):.0f}" cy="{y-8+R.uniform(-5,4):.0f}" r="5" fill="{R.choice(["#E8304A", "#F2C230", "#FF7AA2", "#FFFFFF", "#9B5DE5"])}"/>'
    # 牌子“公园 PARK”、垃圾桶
    s += '<rect x="1100" y="520" width="8" height="90" fill="#6B4B2F"/><rect x="1050" y="500" width="110" height="46" rx="6" fill="#1F6E5A"/>'
    s += '<text x="1105" y="522" font-size="20" fill="#FFF" text-anchor="middle" font-family="Noto Sans CJK SC, sans-serif" font-weight="700">人民公园</text><text x="1105" y="540" font-size="13" fill="#FFF" text-anchor="middle" font-family="sans-serif">PEOPLE\'S PARK</text>'
    s += '<rect x="800" y="590" width="30" height="40" rx="4" fill="#2E7D32"/><rect x="796" y="584" width="38" height="8" rx="3" fill="#1B5E20"/>'
    # 远处散步的人
    s += traveler(300, 520, 52, '#E8407A', hair='#E9C46A', skin='#F3D2BE') + traveler(330, 522, 50, '#2E6FD9') + traveler(1010, 520, 54, '#F28C28', hair='#5A3A22', skin='#C98E66', flip=True)
    s += traveler(700, 470, 34, '#9B5DE5', flip=True) + traveler(760, 472, 32, '#F2C230', hair='#B5651D', skin='#F3D2BE')
    return svg(1200, 700, s, d)
# ---------------------------------------------------------------- 拱顶的屋子（来历）
def vault():
    d = lg('vtW', [(0, '#E9DCC0'), (1, '#CDB894')]) + lg('vtL', [(0, '#FFF6D6'), (1, '#FFE08A')])
    s = '<rect width="1200" height="700" fill="#B9A27E"/>'
    s += '<path d="M165,700 L165,400 A435,334 0 0 1 1035,400 L1035,700 Z" fill="url(#vtW)"/>'
    for i in range(1, 9):   # 拱顶上的石块缝
        a = math.pi * i / 9
        x1 = 600 - 435 * math.cos(a); y1 = 400 - 334 * math.sin(a); x2 = 600 - 360 * math.cos(a); y2 = 400 - 276 * math.sin(a)
        s += f'<path d="M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}" stroke="#A88E66" stroke-width="3"/>'
    s += '<path d="M240,400 A360,276 0 0 1 960,400" fill="none" stroke="#A88E66" stroke-width="4"/>'
    for i in range(1, 6):   # 拱顶下面的一道道肋
        rx = 360 - i * 50; ry = 276 - i * 38
        s += f'<path d="M{600-rx},400 A{rx},{ry} 0 0 1 {600+rx},400" fill="none" stroke="#D9C7A3" stroke-width="10"/>'
    for j in range(9):
        for i in range(4):
            s += f'<rect x="{4 + i*40 + (20 if j%2 else 0)}" y="{390+j*24}" width="36" height="20" fill="#A68C68"/><rect x="{1040 + i*40 - (20 if j%2 else 0)}" y="{390+j*24}" width="36" height="20" fill="#A68C68"/>'
    for j in range(6):
        for i in range(20):
            s += f'<rect x="{250+i*36+(18 if j%2 else 0)}" y="{548+j*9}" width="32" height="7" fill="#C7B08A"/>' if 250+i*36 < 940 else ''
    # 后墙上的拱形窗、光
    for x in (430, 600, 770):
        s += f'<path d="M{x-45},540 L{x-45},420 A45,45 0 0 1 {x+45},420 L{x+45},540 Z" fill="url(#vtL)"/><path d="M{x},380 L{x},540 M{x-45},470 L{x+45},470" stroke="#8C7350" stroke-width="5"/>'
    # 柱子
    for x in (200, 1000):
        s += f'<rect x="{x-30}" y="380" width="60" height="320" fill="#E6D8B8"/><rect x="{x-42}" y="370" width="84" height="22" fill="#D2BF98"/><rect x="{x-42}" y="680" width="84" height="20" fill="#D2BF98"/>'
        for k in range(5):
            s += f'<path d="M{x-20+k*10},392 L{x-20+k*10},680" stroke="#CDBB94" stroke-width="3"/>'
    # 地砖
    s += '<path d="M0,600 L1200,600 L1200,700 L0,700 Z" fill="#B5543A"/>'
    for i in range(13):
        s += f'<path d="M{i*100},600 L{(i-6)*160+600},700" stroke="#8F3E2A" stroke-width="3"/>'
    s += '<path d="M0,640 L1200,640" stroke="#8F3E2A" stroke-width="3"/>'
    # 吊灯、长凳、花盆
    s += '<path d="M600,66 L600,200" stroke="#5A4630" stroke-width="4"/><path d="M560,200 L640,200 L620,236 L580,236 Z" fill="#E0A63A"/><ellipse cx="600" cy="240" rx="14" ry="8" fill="#FFF3B0"/>'
    s += '<rect x="300" y="600" width="200" height="16" fill="#8A5A34"/><rect x="310" y="616" width="12" height="40" fill="#6B4426"/><rect x="478" y="616" width="12" height="40" fill="#6B4426"/>'
    s += '<path d="M860,640 L920,640 L910,690 L870,690 Z" fill="#C0643A"/><circle cx="890" cy="610" r="34" fill="#3E8F3E"/><circle cx="868" cy="596" r="20" fill="#56A94F"/>'
    return svg(1200, 700, s, d)
# ---------------------------------------------------------------- 暗室（小孔成像）
def obscura():
    d = lg('obSky', [(0, '#6EC1F5'), (1, '#E3F4FF')])
    s = '<rect width="1200" height="700" fill="#2B2F45"/>'
    s += '<rect x="0" y="0" width="400" height="700" fill="url(#obSky)"/><circle cx="220" cy="110" r="36" fill="#FFD43B"/>'
    for cx, cy in ((300, 70), (170, 190)):
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="50" ry="15" fill="#FFFFFF"/>'
    s += '<path d="M0,404 L400,404 L400,700 L0,700 Z" fill="#6DBE45"/>'
    for i in range(18):
        x = R.randint(10, 390); y = R.randint(420, 690)
        s += f'<path d="M{x},{y} l-4,-10 M{x},{y} l0,-12 M{x},{y} l4,-10" stroke="#3E8F2C" stroke-width="2"/>'
    s += '<g transform="translate(160 404)"><rect x="-9" y="-60" width="18" height="62" fill="#7A5232"/><circle cx="0" cy="-112" r="50" fill="#2F8F46"/><circle cx="-32" cy="-88" r="30" fill="#3DA557"/><circle cx="32" cy="-90" r="32" fill="#3DA557"/><circle cx="-4" cy="-134" r="24" fill="#56BD6A"/><circle cx="0" cy="-161" r="3" fill="#E8304A"/></g>'
    s += '<path d="M280,404 L280,350 L350,350 L350,404 Z" fill="#F2E3C6"/><path d="M270,352 L315,318 L360,352 Z" fill="#C0392B"/><rect x="304" y="372" width="20" height="32" fill="#7A4B2A"/>'
    s += '<path d="M0,560 C100,540 260,580 400,560" fill="none" stroke="#E6D3A8" stroke-width="30"/>'
    # 厚墙，中间一个小孔
    s += '<rect x="400" y="0" width="50" height="700" fill="#3A3F5C"/>'
    for j in range(24):
        y = j * 30
        s += f'<path d="M400,{y} L450,{y}" stroke="#2A2E45" stroke-width="2"/><path d="M{425 if j%2 else 412},{y} L{425 if j%2 else 412},{y+30}" stroke="#2A2E45" stroke-width="2"/>'
    s += '<rect x="400" y="322" width="50" height="16" fill="#FFF6C8"/>'
    # 屋里：天花板的木梁、地板、砖墙
    s += '<path d="M450,0 L1200,0 L1200,120 L450,60 Z" fill="#232638"/>'
    for i in range(6):
        x = 470 + i * 110
        s += f'<path d="M{x},{0} L{x+40},{62 + i*10}" stroke="#3B2E26" stroke-width="12"/>'
    s += '<path d="M450,620 L1200,600 L1200,700 L450,700 Z" fill="#4A3426"/>'
    for i in range(9):
        s += f'<path d="M{450+i*85},{620-i*2} L{450+i*85+50},700" stroke="#3A281D" stroke-width="3"/>'
    for j in range(16):
        for i in range(14):
            x = 452 + i * 40 + (20 if j % 2 else 0); y = 70 + j * 34
            if x > 940 or y > 600: continue
            s += f'<rect x="{x}" y="{y}" width="36" height="30" rx="3" fill="#30344D"/>'
    s += '<rect x="960" y="110" width="109" height="500" fill="#3C405E"/><rect x="972" y="160" width="86" height="370" fill="#EDEAF5" opacity="0.15"/>'
    s += '<path d="M940,110 L960,110 L960,610 L940,620 Z" fill="#262A40"/>'
    # 桌子、凳子、熄了的蜡烛、架子上的罐子
    s += '<rect x="640" y="580" width="150" height="12" fill="#5A3F2C"/><rect x="650" y="592" width="10" height="40" fill="#4A3424"/><rect x="770" y="592" width="10" height="36" fill="#4A3424"/>'
    s += '<rect x="700" y="556" width="10" height="24" fill="#D9D3C0"/><rect x="520" y="200" width="140" height="10" fill="#5A3F2C"/>'
    for i, c in enumerate(('#6B5B95', '#88B04B', '#C0643A', '#4A90A4')):
        s += f'<rect x="{530+i*32}" y="{172}" width="22" height="28" rx="5" fill="{c}" opacity="0.6"/>'
    return svg(1200, 700, s, d)
def obscura_img():   # 对面墙上倒着的像：树和小屋上下颠倒（墙 x 972–1058、y 170–520）
    s = '<g transform="translate(0 350) scale(1 -1)">'
    s += '<rect x="0" y="0" width="90" height="350" fill="#BFE3F8" opacity="0.5"/><rect x="0" y="0" width="90" height="0" fill="#6DBE45"/>'
    s += '<g transform="translate(36 2) scale(0.95)"><rect x="-9" y="0" width="18" height="62" fill="#7A5232"/><circle cx="0" cy="112" r="50" fill="#2F8F46"/><circle cx="-24" cy="88" r="28" fill="#3DA557"/><circle cx="26" cy="90" r="30" fill="#3DA557"/></g>'
    s += '<path d="M70,2 L70,40 L90,40 L90,2 Z" fill="#F2E3C6"/><circle cx="60" cy="300" r="20" fill="#FFD43B"/></g>'
    return svg(90, 350, s)
# ---------------------------------------------------------------- 东西
def camera():
    s = '<rect x="20" y="60" width="300" height="160" rx="22" fill="#2B2D33"/><path d="M110,60 L130,24 L210,24 L230,60 Z" fill="#3A3D45"/>'
    s += '<rect x="20" y="60" width="300" height="34" rx="14" fill="#C9CFD8"/><rect x="40" y="40" width="40" height="22" rx="5" fill="#E8304A"/><circle cx="268" cy="52" r="14" fill="#C9CFD8"/>'
    s += '<rect x="246" y="102" width="56" height="30" rx="5" fill="#F4F6F8"/><rect x="250" y="106" width="48" height="22" rx="4" fill="#FFF3B0"/>'
    s += '<rect x="20" y="96" width="44" height="120" rx="14" fill="#1E1F24"/>'
    s += '<circle cx="170" cy="142" r="74" fill="#16171B"/><circle cx="170" cy="142" r="60" fill="#3B4A63"/><circle cx="170" cy="142" r="44" fill="#2563EB"/><circle cx="170" cy="142" r="28" fill="#1E3A8A"/><circle cx="152" cy="124" r="12" fill="#BFDBFE"/><circle cx="190" cy="160" r="6" fill="#93C5FD"/>'
    s += '<path d="M120,96 A74,74 0 0 1 220,96" fill="none" stroke="#E8304A" stroke-width="6"/>'
    s += '<rect x="8" y="80" width="14" height="14" rx="3" fill="#888"/><rect x="318" y="80" width="14" height="14" rx="3" fill="#888"/>'
    return svg(340, 240, s)
def flash():
    pts = []
    for i in range(16):
        r = 100 if i % 2 == 0 else 40
        a = math.pi * 2 * i / 16
        pts.append('%.0f,%.0f' % (110 + r * math.cos(a), 110 + r * math.sin(a)))
    return svg(220, 220, f'<polygon points="{" ".join(pts)}" fill="#FFF7AE"/><circle cx="110" cy="110" r="40" fill="#FFFFFF"/>')
def photo():
    s = '<rect x="0" y="0" width="220" height="250" rx="6" fill="#FFFFFF"/><rect x="14" y="14" width="192" height="180" fill="#8ED0F5"/>'
    s += '<path d="M14,150 L206,150 L206,194 L14,194 Z" fill="#6DBE45"/>'
    s += '<path d="M40,110 C55,100 85,92 100,86 C115,92 145,100 160,110 Z" fill="#2A8C6E"/><rect x="50" y="110" width="8" height="40" fill="#D2232A"/><rect x="142" y="110" width="8" height="40" fill="#D2232A"/>'
    s += '<circle cx="110" cy="128" r="16" fill="#F6D9C8"/><path d="M92,128 C90,104 130,104 128,128 C124,116 96,116 92,128 Z" fill="#C0392B"/><path d="M96,146 L124,146 L130,194 L90,194 Z" fill="#3E8FE0"/>'
    s += '<path d="M126,150 L142,124 M142,124 l-3,-10 M142,124 l6,-8" stroke="#F6D9C8" stroke-width="6" stroke-linecap="round"/>'
    s += '<text x="110" y="230" font-size="18" fill="#555" text-anchor="middle" font-family="sans-serif">Nov. 2026</text>'
    return svg(220, 250, s)
def tripod_cam(rec=True):
    s = '<path d="M150,250 L60,480 M150,250 L240,480 M150,250 L150,470" stroke="#3A3F4B" stroke-width="12" stroke-linecap="round"/><rect x="128" y="236" width="44" height="22" rx="4" fill="#2B2D33"/>'
    s += '<rect x="40" y="130" width="200" height="104" rx="16" fill="#2B2D33"/><rect x="236" y="148" width="56" height="70" rx="6" fill="#1E1F24"/><ellipse cx="292" cy="183" rx="10" ry="34" fill="#2563EB"/>'
    s += '<rect x="70" y="104" width="130" height="16" rx="8" fill="#3A3D45"/><rect x="88" y="112" width="12" height="22" fill="#3A3D45"/><rect x="170" y="112" width="12" height="22" fill="#3A3D45"/>'
    s += '<rect x="4" y="138" width="40" height="42" rx="8" fill="#1E1F24"/><rect x="60" y="150" width="90" height="60" rx="6" fill="#4FC3F7"/><path d="M70,196 L96,170 L118,190 L140,164 L140,204 L70,204 Z" fill="#2E7D32"/>'
    s += f'<circle cx="218" cy="146" r="9" fill="{"#FF2D2D" if rec else "#5A1F1F"}"/>'
    s += '<text x="196" y="226" font-size="18" fill="#E8EAF0" font-family="sans-serif" font-weight="700">REC</text>'
    return svg(310, 490, s)
def boxcam():
    s = '<rect x="20" y="40" width="240" height="200" rx="10" fill="#B07A43"/><rect x="20" y="40" width="240" height="26" fill="#8C5A2B"/>'
    for i in range(6):
        s += f'<path d="M20,{80+i*28} L260,{80+i*28}" stroke="#9A6A38" stroke-width="3"/>'
    s += '<circle cx="140" cy="150" r="62" fill="#C9A227"/><circle cx="140" cy="150" r="46" fill="#3B3A36"/><circle cx="140" cy="150" r="30" fill="#2563EB"/><circle cx="128" cy="138" r="9" fill="#BFDBFE"/>'
    s += '<rect x="110" y="16" width="60" height="26" rx="4" fill="#8C5A2B"/>'
    return svg(280, 260, s)
def rotary_phone():
    s = '<path d="M30,200 L60,90 L240,90 L270,200 Z" fill="#D2232A"/><path d="M20,70 C20,30 280,30 280,70 L250,90 L50,90 Z" fill="#B71C1C"/>'
    s += '<circle cx="150" cy="150" r="46" fill="#F4F1EA"/>'
    for i in range(10):
        a = math.pi * 2 * i / 10
        s += f'<circle cx="{150+32*math.cos(a):.0f}" cy="{150+32*math.sin(a):.0f}" r="7" fill="#3A3F4B"/>'
    s += '<path d="M60,90 C40,140 30,200 70,230" fill="none" stroke="#1B1A1F" stroke-width="5"/>'
    return svg(300, 240, s)
def smartphone():
    s = '<rect x="10" y="10" width="140" height="280" rx="22" fill="#1E1F24"/><rect x="20" y="34" width="120" height="226" rx="8" fill="#4FC3F7"/>'
    for i in range(4):
        for j in range(3):
            s += f'<rect x="{32+j*38}" y="{50+i*44}" width="26" height="26" rx="6" fill="{["#F2C230", "#E8304A", "#6DBE45", "#9B5DE5"][(i+j)%4]}"/>'
    s += '<circle cx="80" cy="274" r="8" fill="#555"/>'
    return svg(160, 300, s)
def icon_cam():   # 小图标：相机 + 一张照片
    return svg(200, 200, nest(camera(), 10, 50, 180, 128))
write_art(ART, 'park-bg.svg', park(), bg=True)
write_art(ART, 'vault-room.svg', vault(), bg=True)
write_art(ART, 'obscura-room.svg', obscura(), bg=True)
write_art(ART, 'obscura-img.svg', obscura_img(), style=False)
for n, f in (('camera.svg', camera), ('flash.svg', flash), ('photo.svg', photo), ('boxcam.svg', boxcam), ('rotary-phone.svg', rotary_phone), ('smartphone.svg', smartphone)):
    write_art(ART, n, f())
write_art(ART, 'tripod-cam.svg', tripod_cam(True)); write_art(ART, 'tripod-cam-off.svg', tripod_cam(False))
# ---------------------------------------------------------------- 人：拿相机拍照（举到眼前；f1 闪光）
cam = open(os.path.join(ART, 'camera.svg')).read(); fl = open(os.path.join(ART, 'flash.svg')).read()
HOLD = (18, 92, 212, 100, 'fist')
def shooter(who, flashing, **kw):
    p = holding(who, cam, 285, 146, 150, 106, left=HOLD, right=HOLD, mouth='smile', **kw)
    if flashing:
        vb, body = inner(p); p = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}{nest(fl, 360, 60, 120, 120)}</svg>'
    return p
M = {}
M['west-woman-shoot'] = frames_out(ART, 'west-woman-shoot', [shooter('west-woman', False), shooter('west-woman', False), shooter('west-woman', True)], fps=1.6)
M['cn-boy-shoot'] = frames_out(ART, 'cn-boy-shoot', [shooter('cn-boy', False), shooter('cn-boy', False), shooter('cn-boy', True)], fps=1.6)
# 被拍的人：比剪刀手、笑
M['cn-girl-pose'] = frames_out(ART, 'cn-girl-pose', [person('cn-girl', right='hello', mouth='laugh', eyes='happy', tilt=-5), person('cn-girl', right='hello', mouth='smile', eyes='happy', tilt=2)], fps=1.2, seq='pingpong')
M['west-girl-wave'] = frames_out(ART, 'west-girl-wave', [person('west-girl', left='wave1', mouth='laugh', eyes='happy'), person('west-girl', left='wave2', mouth='smile', eyes='happy', tilt=3)], fps=3, seq='pingpong')
# 摄像师：手扶着三脚架上的摄像机、眼睛往旁边看
M['cn-boy-film'] = frames_out(ART, 'cn-boy-film', [person('cn-boy', left=(60, 104, 96, 96, 'fist'), mouth='smile', look=-1, brows='up'), person('cn-boy', left=(60, 104, 96, 96, 'fist'), mouth='smile', look=-1, eyes='closed')], fps=0.8, seq='loop')
M['west-man-film'] = frames_out(ART, 'west-man-film', [person('west-man', right=(60, 104, 96, 96, 'fist'), mouth='flat', look=1, brows='up'), person('west-man', right=(60, 104, 96, 96, 'fist'), mouth='flat', look=1, eyes='closed')], fps=0.8, seq='loop')
# 讲解的老师、吃惊的女孩（暗室里）
M['cn-teacher-explain'] = frames_out(ART, 'cn-teacher-explain', [person('cn-teacher', right='pointup', mouth='open', brows='up', look=1), person('cn-teacher', right=(64, 104, 118, 100, 'point'), mouth='half', brows='up', look=1, tilt=3)], fps=3)
M['west-girl-wow'] = frames_out(ART, 'west-girl-wow', [person('west-girl', left='chest', mouth='o', eyes='wide', brows='up', look=1, tilt=-3), person('west-girl', left='chest', mouth='o', eyes='wide', brows='up', look=1, tilt=3)], fps=1.0, seq='pingpong')
# 拿着手机的女孩（phone → 手机）
ph = open(os.path.join(ART, 'smartphone.svg')).read()
M['cn-girl-phone'] = frames_out(ART, 'cn-girl-phone', [holding('cn-girl', ph, 400, 210, 60, 112, right=(10, 96, 160, 70, 'fist'), mouth='open', look=1),
                                                     holding('cn-girl', ph, 400, 210, 60, 112, right=(10, 96, 160, 70, 'fist'), mouth='half', look=1, tilt=3)], fps=3)
json.dump(M, open(os.path.join(ART, 'cam_motions.json'), 'w'), ensure_ascii=False, indent=1)
print('人物', list(M))

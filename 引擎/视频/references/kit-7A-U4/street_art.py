"""街道背景（中式店招 + 西式咖啡馆、斑马线、红绿灯、公交站……）和 stranger 用的东西"""
import sys, os, math, random
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
import importlib.util as _u
_sp = _u.spec_from_file_location('scn', SK + '/scripts/scenes.py'); _a = sys.argv; sys.argv = ['x', '/tmp/_scn']; os.makedirs('/tmp/_scn', exist_ok=True)
_m = _u.module_from_spec(_sp); _sp.loader.exec_module(_m); traveler = _m.traveler; sys.argv = _a
ART = sys.argv[1]
R = random.Random(9)
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
def shop(x, w, h, wall, sign, text, en=False, awning=None):
    s = f'<rect x="{x}" y="{460-h}" width="{w}" height="{h}" fill="{wall}"/>'
    for yy in range(460 - h + 20, 330, 56):
        for xx in range(x + 16, x + w - 30, 50):
            s += f'<rect x="{xx}" y="{yy}" width="30" height="36" fill="#CFE6F7"/><path d="M{xx+15},{yy} L{xx+15},{yy+36}" stroke="#FFFFFF" stroke-width="3"/>'
    s += f'<rect x="{x+8}" y="342" width="{w-16}" height="44" rx="4" fill="{sign}"/>'
    s += f'<text x="{x+w/2}" y="374" font-size="{26 if not en else 24}" fill="#FFFFFF" text-anchor="middle" {CJK if not en else "font-family=\"serif\" font-weight=\"700\""}>{text}</text>'
    if awning:
        for i in range(int((w - 16) / 24)):
            s += f'<path d="M{x+8+i*24},390 L{x+32+i*24},390 L{x+32+i*24},410 C{x+26+i*24},418 {x+14+i*24},418 {x+8+i*24},410 Z" fill="{awning[i%2]}"/>'
    s += f'<rect x="{x+16}" y="414" width="{w*0.5:.0f}" height="46" fill="#9ED0EE"/><rect x="{x+w*0.62:.0f}" y="408" width="{w*0.26:.0f}" height="52" fill="#6B4426"/>'
    return s
def street():
    d = lg('svSky', [(0, '#7CC4F2'), (1, '#E3F4FF')])
    s = '<rect width="1200" height="700" fill="url(#svSky)"/>'
    for cx, cy in ((160, 70), (700, 50), (1050, 90)):
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="70" ry="20" fill="#FFF"/><ellipse cx="{cx+30}" cy="{cy-10}" rx="40" ry="16" fill="#FFF"/>'
    for x, w, h in ((0, 110, 260), (420, 90, 300), (980, 120, 280)):
        s += f'<rect x="{x}" y="{460-h}" width="{w}" height="{h-150}" fill="#C9D3E2"/>'
    s += shop(0, 230, 230, '#F2E3C6', '#C0392B', '书店')
    s += shop(240, 220, 260, '#E6D2B5', '#2E7D32', 'CAFÉ', en=True, awning=('#2E7D32', '#FFFFFF'))
    s += shop(470, 250, 220, '#F5D6A8', '#D2232A', '老北京面馆', awning=('#D2232A', '#F2C230'))
    s += shop(730, 220, 250, '#DCE3EC', '#1F3E8A', 'BAKERY', en=True, awning=('#E8407A', '#FFFFFF'))
    s += shop(960, 240, 230, '#F2E3C6', '#6B4E9A', '水果店')
    for x in (470, 720):   # 红灯笼
        s += f'<ellipse cx="{x+30}" cy="330" rx="14" ry="17" fill="#E8304A"/><rect x="{x+24}" y="310" width="12" height="5" fill="#F2C230"/>'
    s += '<rect x="0" y="460" width="1200" height="60" fill="#CFC8BB"/>'
    for i in range(0, 1200, 60):
        s += f'<path d="M{i},460 L{i-10},520" stroke="#B8B0A2" stroke-width="2"/>'
    s += '<rect x="0" y="520" width="1200" height="12" fill="#9C958A"/><rect x="0" y="532" width="1200" height="168" fill="#5A5E66"/>'
    for i in range(0, 1200, 120):
        s += f'<rect x="{i}" y="610" width="60" height="8" fill="#F2F2F2"/>'
    for i in range(9):
        s += f'<rect x="{830+i*36}" y="536" width="22" height="160" fill="#F2F2F2"/>'
    # 红绿灯、路牌、公交站、树、车
    s += '<rect x="796" y="300" width="10" height="220" fill="#3A3F4B"/><rect x="780" y="250" width="42" height="96" rx="8" fill="#2B2D33"/><circle cx="801" cy="272" r="11" fill="#E8304A"/><circle cx="801" cy="298" r="11" fill="#5A5A2A"/><circle cx="801" cy="324" r="11" fill="#2A5A2A"/>'
    s += '<rect x="196" y="380" width="8" height="140" fill="#3A3F4B"/><rect x="150" y="372" width="100" height="34" rx="4" fill="#1F6E5A"/><text x="200" y="395" font-size="16" fill="#FFF" text-anchor="middle" font-family="sans-serif">Park Rd. 公园路</text>'
    s += '<rect x="1100" y="400" width="8" height="120" fill="#3A3F4B"/><rect x="1080" y="360" width="56" height="44" rx="6" fill="#2E6FD9"/><text x="1108" y="390" font-size="22" fill="#FFF" text-anchor="middle" ' + CJK + '>公交</text>'
    for x in (120, 640, 1020):
        s += f'<g transform="translate({x} 520) scale(0.7)"><rect x="-8" y="-70" width="16" height="72" fill="#7A5232"/><circle cx="0" cy="-110" r="50" fill="#2F8F46"/><circle cx="-32" cy="-88" r="32" fill="#3DA557"/><circle cx="32" cy="-90" r="34" fill="#3DA557"/></g>'
    s += '<rect x="40" y="560" width="200" height="70" rx="20" fill="#F2C230"/><rect x="70" y="530" width="120" height="44" rx="12" fill="#F2C230"/><rect x="82" y="538" width="44" height="30" fill="#BFE3F8"/><rect x="134" y="538" width="44" height="30" fill="#BFE3F8"/><circle cx="80" cy="632" r="20" fill="#2B2D33"/><circle cx="200" cy="632" r="20" fill="#2B2D33"/>'
    s += '<rect x="400" y="566" width="160" height="60" rx="18" fill="#E8304A"/><rect x="430" y="540" width="100" height="40" rx="12" fill="#E8304A"/><rect x="440" y="548" width="36" height="26" fill="#BFE3F8"/><rect x="484" y="548" width="36" height="26" fill="#BFE3F8"/><circle cx="436" cy="628" r="17" fill="#2B2D33"/><circle cx="524" cy="628" r="17" fill="#2B2D33"/>'
    s += traveler(300, 515, 46, '#E8407A', hair='#E9C46A', skin='#F3D2BE') + traveler(680, 515, 44, '#2E6FD9', flip=True) + traveler(930, 515, 48, '#6DBE45', hair='#5A3A22', skin='#C98E66')
    return svg(1200, 700, s, d)
def map_():
    s = '<path d="M10,20 L90,6 L170,20 L250,6 L250,170 L170,184 L90,170 L10,184 Z" fill="#F7E9C2"/><path d="M90,6 L90,170 M170,20 L170,184" stroke="#D8C38F" stroke-width="3"/>'
    s += '<path d="M30,140 C80,100 140,130 220,60" fill="none" stroke="#E8304A" stroke-width="6" stroke-dasharray="12 8"/><circle cx="220" cy="60" r="10" fill="#E8304A"/><path d="M40,60 L120,60 M60,30 L60,160" stroke="#9ED0EE" stroke-width="10"/>'
    return svg(260, 190, s)
write_art(ART, 'street-bg.svg', street(), bg=True); write_art(ART, 'map.svg', map_())
mp = open(os.path.join(ART, 'map.svg')).read()
M = json.load(open(os.path.join(ART, 'word_motions.json'))) if os.path.exists(os.path.join(ART, 'word_motions.json')) else {}
# 拿着地图问路的外国人（说话）、拿着地图东张西望的外国女士
M['west-man-ask'] = frames_out(ART, 'west-man-ask', [holding('west-man', mp, 230, 300, 150, 110, left=(20, 100, 110, 70, 'fist'), right=(64, 104, 120, 96, 'open'), mouth='open', brows='up', look=1),
                                                   holding('west-man', mp, 230, 300, 150, 110, left=(20, 100, 110, 70, 'fist'), right=(60, 104, 132, 96, 'open'), mouth='half', brows='up', look=1, tilt=3)], fps=3)
M['west-woman-lost'] = frames_out(ART, 'west-woman-lost', [holding('west-woman', mp, 290, 300, 150, 110, left=(20, 100, 120, 70, 'fist'), right=(20, 100, 120, 70, 'fist'), mouth='flat', brows='frown', look=-1),
                                                         holding('west-woman', mp, 290, 300, 150, 110, left=(20, 100, 120, 70, 'fist'), right=(20, 100, 120, 70, 'fist'), mouth='flat', brows='frown', look=1, tilt=4)], fps=0.8, seq='loop')
M['cn-girl-direct'] = frames_out(ART, 'cn-girl-direct', [person('cn-girl', left='point', mouth='open', look=-1, brows='up'), person('cn-girl', left=(64, 104, 110, 96, 'point'), mouth='half', look=-1, tilt=-2)], fps=3)
M['cn-boy-shy'] = frames_out(ART, 'cn-boy-shy', [person('cn-boy', left='chest', right='chest', mouth='flat', eyes='wide', look=-1, brows='frown', tilt=4), person('cn-boy', left='chest', right='chest', mouth='flat', eyes='wide', look=1, brows='frown', tilt=-2)], fps=1, seq='loop')
M['cn-teacher-welcome'] = frames_out(ART, 'cn-teacher-welcome', [person('cn-teacher', left='hello', mouth='laugh', eyes='happy'), person('cn-teacher', left='wave2', mouth='open', eyes='happy', tilt=3)], fps=3, seq='pingpong')
json.dump(M, open(os.path.join(ART, 'word_motions.json'), 'w'), ensure_ascii=False, indent=1)
print(list(M))

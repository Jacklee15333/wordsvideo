import sys, os, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'


def house_body():   # 小房子（没有屋顶）：墙、门、窗、花盆
    s = '<rect x="20" y="20" width="300" height="200" fill="#F2E3C6"/><rect x="20" y="200" width="300" height="20" fill="#C9A27A"/>'
    for y in range(36, 200, 26):
        s += f'<path d="M20,{y} L320,{y}" stroke="#E6D2B5" stroke-width="3"/>'
    s += '<rect x="140" y="110" width="62" height="110" rx="4" fill="#8A5A3B"/><circle cx="190" cy="168" r="5" fill="#F2C230"/>'
    for x in (44, 238):
        s += f'<rect x="{x}" y="70" width="64" height="60" fill="#BFE3F8"/><path d="M{x+32},70 L{x+32},130 M{x},100 L{x+64},100" stroke="#8A5A3B" stroke-width="5"/><rect x="{x-4}" y="128" width="72" height="8" fill="#8A5A3B"/>'
        s += f'<rect x="{x+6}" y="136" width="52" height="16" fill="#B5432F"/><circle cx="{x+18}" cy="132" r="8" fill="#E8304A"/><circle cx="{x+34}" cy="130" r="8" fill="#F2C230"/><circle cx="{x+48}" cy="132" r="8" fill="#E8407A"/>'
    s += '<rect x="20" y="214" width="300" height="10" fill="#8C7F72"/>'
    return svg(340, 230, s)


def roof():   # 屋顶：红瓦、屋脊、烟囱
    s = '<rect x="226" y="0" width="34" height="60" fill="#8C5A3C"/><rect x="220" y="0" width="46" height="12" fill="#6B4527"/>'
    s += '<path d="M0,118 L170,10 L340,118 Z" fill="#C0392B"/>'
    for k in range(1, 6):
        y = 10 + k * 18; dx = 170 * (y - 10) / 108
        s += f'<path d="M{170-dx:.0f},{y} L{170+dx:.0f},{y}" stroke="#A93226" stroke-width="3"/>'
    s += '<path d="M-6,122 L170,6 L346,122" fill="none" stroke="#7A2E22" stroke-width="10" stroke-linejoin="round"/>'
    return svg(340, 128, s)


def shield():   # 盾牌：木头、铁边、中间一颗金色的星
    s = '<path d="M90,0 C130,14 160,16 180,14 L180,110 C180,170 130,206 90,220 C50,206 0,170 0,110 L0,14 C20,16 50,14 90,0 Z" fill="#9AA3AE"/>'
    s += '<path d="M90,14 C124,26 150,28 166,26 L166,110 C166,160 124,192 90,204 C56,192 14,160 14,110 L14,26 C30,28 56,26 90,14 Z" fill="#2E6FD9"/>'
    s += '<path d="M90,14 L90,204 M14,100 L166,100" stroke="#F2C230" stroke-width="10"/><circle cx="90" cy="100" r="26" fill="#F2C230"/>'
    s += '<path d="M90,82 L96,96 L110,96 L99,105 L103,119 L90,110 L77,119 L81,105 L70,96 L84,96 Z" fill="#E8304A"/>'
    for (x, y) in ((24, 30), (156, 30), (24, 150), (156, 150), (90, 196)):
        s += f'<circle cx="{x}" cy="{y}" r="5" fill="#C9D3E2"/>'
    return svg(180, 222, s)


def sun(k):
    s = ''
    for a in range(0, 360, 30):
        L = (34, 46)[(a // 30 + k) % 2]
        s += f'<path d="M100,100 m0,-58 l0,-{L}" stroke="#F2A900" stroke-width="10" stroke-linecap="round" transform="rotate({a} 100 100)"/>'
    s += '<circle cx="100" cy="100" r="50" fill="#FFD43B"/><circle cx="84" cy="90" r="6" fill="#E89A00"/><circle cx="116" cy="90" r="6" fill="#E89A00"/><path d="M80,112 Q100,128 120,112" fill="none" stroke="#E89A00" stroke-width="6"/>'
    return svg(200, 200, s)


def shades(c='#1B1A1F'):   # 墨镜（套在人脸上）
    s = f'<path d="M0,14 L160,14" stroke="{c}" stroke-width="7"/><rect x="8" y="8" width="62" height="40" rx="16" fill="{c}"/><rect x="90" y="8" width="62" height="40" rx="16" fill="{c}"/>'
    s += '<path d="M20,18 L36,18 M102,18 L118,18" stroke="#8C939E" stroke-width="5" stroke-linecap="round"/>'
    return svg(160, 52, s)


def crate():   # 进口的货箱
    s = '<rect x="0" y="10" width="140" height="110" fill="#C98E5A"/><path d="M0,10 L20,0 L160,0 L140,10 Z" fill="#E0AA74"/><path d="M140,10 L160,0 L160,110 L140,120 Z" fill="#A86E3E"/>'
    s += '<path d="M0,40 L140,40 M0,90 L140,90" stroke="#8A5A3B" stroke-width="5"/>'
    s += f'<rect x="28" y="52" width="84" height="28" fill="#FFFFFF"/><text x="70" y="73" font-size="20" fill="#C0392B" text-anchor="middle" {CJK}>进口货</text>'
    return svg(160, 122, s)


def vase():   # 青花瓷瓶
    s = '<path d="M60,0 L100,0 L96,20 C140,40 150,90 132,140 C122,168 110,186 104,200 L56,200 C50,186 38,168 28,140 C10,90 20,40 64,20 Z" fill="#F4F1EA"/>'
    s += '<path d="M40,60 C60,50 100,50 120,60 M34,140 C60,150 100,150 126,140" fill="none" stroke="#2E5FA8" stroke-width="5"/>'
    s += '<path d="M60,90 C70,74 90,74 100,90 C110,106 90,122 80,110 C70,98 82,90 88,96" fill="none" stroke="#2E5FA8" stroke-width="5"/><path d="M50,170 L110,170" stroke="#2E5FA8" stroke-width="4"/>'
    return svg(160, 200, s)


def glasscase():   # 博物馆的玻璃柜：底座、玻璃罩、标签
    s = '<rect x="0" y="230" width="260" height="70" fill="#8A5A3B"/><rect x="10" y="240" width="240" height="50" fill="#A87047"/>'
    s += '<rect x="20" y="0" width="220" height="232" fill="#DDF1FF" opacity="0.35"/><rect x="20" y="0" width="220" height="232" fill="none" stroke="#9AA3AE" stroke-width="6"/>'
    s += '<path d="M40,20 L80,20 M200,40 L220,60" stroke="#FFFFFF" stroke-width="5" opacity="0.8"/>'
    s += f'<rect x="80" y="252" width="100" height="26" fill="#F4F1EA"/><text x="130" y="271" font-size="16" fill="#3A3F4B" text-anchor="middle" {CJK}>明代 青花瓷</text>'
    return svg(260, 300, s)


def ball(c='#E8304A'):
    return svg(60, 60, f'<circle cx="30" cy="30" r="27" fill="{c}"/><path d="M6,24 C20,32 40,32 54,24 M10,42 C22,36 38,36 50,42" fill="none" stroke="#FFFFFF" stroke-width="4"/>')


def icon_front():
    s = nest(house_body(), 20, 80, 140, 95) + nest(roof(), 14, 40, 152, 57) + nest(shield(), 110, 70, 80, 98)
    return svg(200, 200, s)


def icon_cover():
    s = nest(house_body(), 30, 100, 140, 95) + nest(roof(), 24, 30, 152, 57)
    s += '<path d="M100,10 L100,30 M88,20 L100,32 L112,20" stroke="#2E6FD9" stroke-width="6" fill="none" stroke-linecap="round"/>'
    return svg(200, 200, s)


write_art(ART, 'house-body.svg', house_body()); write_art(ART, 'roof.svg', roof()); write_art(ART, 'shield.svg', shield())
write_art(ART, 'sun_f0.svg', sun(0)); write_art(ART, 'sun_f1.svg', sun(1)); write_art(ART, 'crate.svg', crate())
write_art(ART, 'vase.svg', vase()); write_art(ART, 'glasscase.svg', glasscase()); write_art(ART, 'ball.svg', ball()); write_art(ART, 'ball2.svg', ball('#2E6FD9'))
write_art(ART, 'icon-front.svg', icon_front()); write_art(ART, 'icon-cover.svg', icon_cover())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
sg = shades(); sh = shield()
M['cn-boy-shades'] = frames_out(ART, 'cn-boy-shades', [holding('cn-boy', sg, 280, 118, 160, 52, left='thumb', mouth='laugh', tilt=-3),
                                                   holding('cn-boy', sg, 280, 118, 160, 52, left='thumb', mouth='smile', tilt=3)], fps=1.4, seq='pingpong')
M['west-girl-shades'] = frames_out(ART, 'west-girl-shades', [holding('west-girl', sg, 280, 118, 160, 52, right='hello', mouth='open', tilt=2),
                                                         holding('west-girl', sg, 280, 118, 160, 52, right='wave2', mouth='smile', tilt=-2)], fps=2.2, seq='pingpong')
M['west-boy-shield'] = frames_out(ART, 'west-boy-shield', [holding('west-boy', sh, 270, 250, 180, 222, left=(20, 100, 120, 70, 'fist'), right=(20, 100, 120, 70, 'fist'), mouth='flat', brows='frown'),
                                                       holding('west-boy', sh, 270, 254, 180, 222, left=(20, 100, 120, 70, 'fist'), right=(20, 100, 120, 70, 'fist'), mouth='o', eyes='wide')], fps=2, seq='pingpong')
M['cn-girl-look'] = frames_out(ART, 'cn-girl-look', [person('cn-girl', left='chin', mouth='o', eyes='wide', look=1, brows='up'),
                                                 person('cn-girl', left='chin', mouth='smile', eyes='open', look=1)], fps=1.2, seq='pingpong')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

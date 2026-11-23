import sys, os, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'


def signpost():   # 路口的指路牌：几块箭头牌
    s = '<rect x="92" y="20" width="16" height="280" fill="#8A5A3B"/><rect x="80" y="292" width="40" height="12" fill="#6B4527"/>'
    for i, (t, d, c) in enumerate((('古镇', 1, '#2E7D32'), ('车站', -1, '#2E6FD9'), ('公园', 1, '#C0392B'))):
        y = 40 + i * 70
        if d > 0:
            s += f'<path d="M100,{y} L180,{y} L200,{y+22} L180,{y+44} L100,{y+44} Z" fill="{c}"/><text x="146" y="{y+31}" font-size="22" fill="#FFFFFF" text-anchor="middle" {CJK}>{t}</text>'
        else:
            s += f'<path d="M100,{y} L20,{y} L0,{y+22} L20,{y+44} L100,{y+44} Z" fill="{c}"/><text x="54" y="{y+31}" font-size="22" fill="#FFFFFF" text-anchor="middle" {CJK}>{t}</text>'
    return svg(200, 306, s)


def guidebook():   # 摊开的旅游指南：左页地图、右页景点
    s = '<path d="M0,20 L180,8 L180,232 L0,244 Z" fill="#FFFDF5"/><path d="M180,8 L360,20 L360,244 L180,232 Z" fill="#FFFDF5"/><path d="M180,8 L180,232" stroke="#C9B48A" stroke-width="4"/>'
    s += '<path d="M14,40 L166,30 L166,220 L14,230 Z" fill="#DCEBD5"/><path d="M20,120 C60,100 100,150 160,110" fill="none" stroke="#7CC4F2" stroke-width="10"/>'
    s += '<path d="M30,60 L150,200 M40,190 L150,60" stroke="#F4F1EA" stroke-width="7"/>'
    for (x, y, c) in ((60, 80, '#E8304A'), (120, 170, '#E8304A'), (100, 110, '#2E6FD9')):
        s += f'<path d="M{x},{y} C{x-10},{y-12} {x-8},{y-24} {x},{y-24} C{x+8},{y-24} {x+10},{y-12} {x},{y} Z" fill="{c}"/>'
    s += f'<text x="270" y="50" font-size="22" fill="#C0392B" text-anchor="middle" {EN}>TRAVEL GUIDE</text><text x="270" y="78" font-size="20" fill="#1B3A6B" text-anchor="middle" {CJK}>北京旅游指南</text>'
    s += '<rect x="206" y="94" width="128" height="70" fill="#E9C46A"/><path d="M216,160 L246,112 L276,160 Z M260,160 L290,104 L324,160 Z" fill="#C0392B"/>'
    for k in range(3):
        s += f'<rect x="206" y="{178+k*16}" width="{128 - k*20}" height="7" rx="3" fill="#8C939E"/>'
    return svg(360, 248, s)


def with_flag(who, hand, col, **kw):   # 导游举着小旗：旗杆从手里伸到头顶上
    vb, body = inner(person(who, **kw))
    hx, hy = hand
    f = (f'<path d="M{hx},{hy} L{hx},30" stroke="#5A3A22" stroke-width="7"/>'
         f'<path d="M{hx},32 L{hx+110},56 L{hx},82 Z" fill="{col}" stroke="#1B1A1F" stroke-width="4"/>'
         f'<circle cx="{hx}" cy="28" r="7" fill="#F2C230"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}{f}</svg>'


write_art(ART, 'signpost.svg', signpost()); write_art(ART, 'guidebook.svg', guidebook())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
ARM = (30, 100, 175, 60, 'fist')
M['cn-girl-flag'] = frames_out(ART, 'cn-girl-flag', [with_flag('cn-girl', (512, 300), '#E8304A', right=ARM, left='point', mouth='open', brows='up', look=-1),
                                                 with_flag('cn-girl', (512, 300), '#E8304A', right=ARM, left='point', mouth='half', look=-1, tilt=2)], fps=3, seq='pingpong')
M['cn-teacher-guide'] = frames_out(ART, 'cn-teacher-guide', [person('cn-teacher', right='present', left='point', mouth='open', brows='up', look=1),
                                                         person('cn-teacher', right='present2', left='point', mouth='smile', look=1, tilt=2)], fps=2.4, seq='pingpong')
cam = open(os.path.join(ART, 'camera.svg')).read() if os.path.exists(os.path.join(ART, 'camera.svg')) else None
if cam:
    M['west-man-tourist'] = frames_out(ART, 'west-man-tourist', [holding('west-man', cam, 300, 120, 120, 90, left=(20, 100, 120, 70, 'fist'), right=(20, 100, 120, 70, 'fist'), mouth='smile', tie=None, top='#6DBE45'),
                                                             holding('west-man', cam, 300, 124, 120, 90, left=(20, 100, 120, 70, 'fist'), right=(20, 100, 120, 70, 'fist'), mouth='laugh', eyes='happy', tie=None, top='#6DBE45')], fps=1.2, seq='pingpong')
M['cn-boy-learn'] = frames_out(ART, 'cn-boy-learn', [person('cn-boy', right='chin', mouth='o', eyes='wide', brows='up', look=-1),
                                                 person('cn-boy', right='chin', mouth='smile', eyes='happy', look=-1, tilt=3)], fps=1.2, seq='pingpong')
M['west-girl-flag'] = frames_out(ART, 'west-girl-flag', [with_flag('west-girl', (512, 300), '#2E6FD9', right=ARM, left='hello', mouth='open', look=-1),
                                                     with_flag('west-girl', (512, 300), '#2E6FD9', right=ARM, left='wave2', mouth='smile', look=-1, tilt=-2)], fps=2.4, seq='pingpong')
M['west-woman-guide'] = frames_out(ART, 'west-woman-guide', [person('west-woman', right='present', left='point', mouth='open', brows='up', look=1),
                                                         person('west-woman', right='present2', left='point', mouth='smile', look=1, tilt=2)], fps=2.4, seq='pingpong')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

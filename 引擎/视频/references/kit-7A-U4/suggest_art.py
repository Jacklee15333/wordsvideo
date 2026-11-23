import sys, os, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'


def shelf():   # 墙上的搁板（上面已经放着几本书、一盆花）
    s = '<rect x="0" y="60" width="420" height="18" rx="4" fill="#8A5A3B"/><path d="M40,78 L60,110 L80,78 M340,78 L360,110 L380,78" fill="#6B4527"/>'
    for i, c in enumerate(('#E8304A', '#2E6FD9', '#F2C230', '#6DBE45')):
        s += f'<rect x="{20+i*26}" y="{14+(i%2)*6}" width="22" height="{46-(i%2)*6}" fill="{c}"/>'
    s += '<path d="M330,60 L370,60 L364,30 L336,30 Z" fill="#B5432F"/><circle cx="342" cy="18" r="12" fill="#3DA557"/><circle cx="358" cy="14" r="13" fill="#2F8F46"/>'
    return svg(420, 112, s)


def up_arrow(c='#2E6FD9'):
    return svg(80, 160, f'<path d="M40,150 L40,40" stroke="{c}" stroke-width="14" stroke-linecap="round"/><path d="M10,52 L40,8 L70,52 Z" fill="{c}"/>')


def bulb(on):   # 灯泡：想到主意了就亮
    s = ''
    if on:
        s += '<circle cx="80" cy="70" r="62" fill="#FFF3B0" opacity="0.7"/>'
        for a in range(0, 360, 45):
            s += f'<path d="M80,70 m0,-64 l0,-12" stroke="#F2A900" stroke-width="6" stroke-linecap="round" transform="rotate({a} 80 70)"/>'
    s += f'<path d="M80,24 C108,24 126,44 126,70 C126,90 112,100 104,114 L56,114 C48,100 34,90 34,70 C34,44 52,24 80,24 Z" fill="{"#FFE27A" if on else "#E6EBF2"}"/>'
    s += '<rect x="58" y="114" width="44" height="12" fill="#9AA3AE"/><rect x="60" y="126" width="40" height="10" fill="#7A828E"/><rect x="66" y="136" width="28" height="8" rx="4" fill="#5A6170"/>'
    s += f'<path d="M66,96 L74,72 L86,72 L94,96" fill="none" stroke="{"#F28C28" if on else "#9AA3AE"}" stroke-width="4"/>'
    return svg(160, 150, s)


def darkcloud(k=0):
    c = ('#6B7280', '#555B66')[k]
    s = f'<ellipse cx="120" cy="80" rx="100" ry="40" fill="{c}"/><circle cx="80" cy="60" r="40" fill="{c}"/><circle cx="140" cy="46" r="50" fill="{c}"/><circle cx="190" cy="70" r="34" fill="{c}"/>'
    s += '<path d="M40,96 C90,110 160,110 210,92" fill="none" stroke="#3F4550" stroke-width="6"/>'
    return svg(240, 130, s)


def flowerbed():   # 春天的花坛：郁金香、小花、嫩草
    s = '<path d="M0,120 C80,96 240,96 320,120 L320,150 L0,150 Z" fill="#7A5232"/>'
    for i in range(9):
        x = 24 + i * 34; c = ('#E8304A', '#F2C230', '#E8407A', '#9B5DE5', '#F28C28')[i % 5]
        s += f'<path d="M{x},116 L{x},{66 + (i % 3) * 8}" stroke="#3DA557" stroke-width="5"/><path d="M{x},96 C{x-14},90 {x-16},80 {x-10},74" fill="none" stroke="#3DA557" stroke-width="5"/>'
        y = 60 + (i % 3) * 8
        s += f'<path d="M{x-12},{y} C{x-12},{y-22} {x-4},{y-26} {x},{y-16} C{x+4},{y-26} {x+12},{y-22} {x+12},{y} C{x+8},{y+10} {x-8},{y+10} {x-12},{y} Z" fill="{c}"/>'
    for i in range(14):
        s += f'<circle cx="{12 + i * 23}" cy="{126 + (i % 2) * 10}" r="5" fill="{("#FFFFFF", "#F7A9A8")[i % 2]}"/>'
    return svg(320, 150, s)


def dogcloud():   # 一朵像小狗的云：身子、头、耳朵、四条腿、尾巴
    c = '#FFFFFF'
    s = f'<ellipse cx="150" cy="100" rx="90" ry="44" fill="{c}"/><circle cx="96" cy="84" r="34" fill="{c}"/><circle cx="196" cy="80" r="30" fill="{c}"/>'
    s += f'<circle cx="262" cy="62" r="40" fill="{c}"/><ellipse cx="300" cy="74" rx="26" ry="18" fill="{c}"/><ellipse cx="242" cy="34" rx="16" ry="30" fill="{c}" transform="rotate(-25 242 34)"/>'
    s += ''.join(f'<rect x="{x}" y="120" width="26" height="46" rx="13" fill="{c}"/>' for x in (86, 120, 176, 210))
    s += f'<path d="M64,88 C40,70 34,46 44,30" fill="none" stroke="{c}" stroke-width="20" stroke-linecap="round"/>'
    s += '<circle cx="274" cy="56" r="5" fill="#C9D3E2"/><circle cx="318" cy="70" r="6" fill="#C9D3E2"/>'
    return svg(340, 180, s)


def icon_up():
    s = '<rect x="30" y="140" width="140" height="18" rx="4" fill="#8A5A3B"/>' + '<rect x="70" y="20" width="60" height="48" fill="#C98E5A"/><rect x="92" y="20" width="16" height="48" fill="#E9C27A"/>'
    s += '<path d="M100,132 L100,86" stroke="#2E6FD9" stroke-width="12" stroke-linecap="round"/><path d="M78,96 L100,70 L122,96 Z" fill="#2E6FD9"/>'
    return svg(200, 200, s)


def icon_carry():
    s = '<rect x="50" y="70" width="100" height="90" rx="8" fill="#B5432F"/><path d="M76,70 L76,46 C76,36 124,36 124,46 L124,70" fill="none" stroke="#5A3A22" stroke-width="10"/>'
    s += '<rect x="50" y="104" width="100" height="10" fill="#8C2F22"/><circle cx="70" cy="168" r="9" fill="#3A3F4B"/><circle cx="130" cy="168" r="9" fill="#3A3F4B"/>'
    return svg(200, 200, s)


write_art(ART, 'shelf.svg', shelf()); write_art(ART, 'up-arrow.svg', up_arrow(), style=False)
write_art(ART, 'bulb_f0.svg', bulb(False)); write_art(ART, 'bulb_f1.svg', bulb(True))
write_art(ART, 'darkcloud_f0.svg', darkcloud(0)); write_art(ART, 'darkcloud_f1.svg', darkcloud(1))
write_art(ART, 'flowerbed.svg', flowerbed()); write_art(ART, 'dogcloud.svg', dogcloud(), style=False); write_art(ART, 'icon-up.svg', icon_up()); write_art(ART, 'icon-carry.svg', icon_carry())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
M['cn-girl-idea'] = frames_out(ART, 'cn-girl-idea', [person('cn-girl', right='pointup', mouth='open', brows='up', eyes='open'),
                                                 person('cn-girl', right='pointup', mouth='laugh', eyes='happy', tilt=3)], fps=2.4, seq='pingpong')
M['west-boy-nod'] = frames_out(ART, 'west-boy-nod', [person('west-boy', left='thumb', mouth='smile', eyes='happy', tilt=-3),
                                                 person('west-boy', left='thumb', mouth='laugh', eyes='happy', tilt=3)], fps=1.6, seq='pingpong')
M['doc-advise'] = frames_out(ART, 'doc-advise', [person('west-man', top='#F7F9FC', collar='#9FD3F0', tie=None, right='point', mouth='open', brows='up'),
                                             person('west-man', top='#F7F9FC', collar='#9FD3F0', tie=None, right='point', mouth='half', tilt=2)], fps=3, seq='pingpong')
M['cn-boy-sick'] = frames_out(ART, 'cn-boy-sick', [person('cn-boy', left='chest', mouth='flat', eyes='open', brows='frown', tilt=-4),
                                               person('cn-boy', left='chest', mouth='o', eyes='open', brows='frown', tilt=-2)], fps=1.2, seq='pingpong')
M['west-girl-idea'] = frames_out(ART, 'west-girl-idea', [person('west-girl', left='pointup', mouth='open', brows='up', look=1),
                                                     person('west-girl', left='pointup', mouth='half', eyes='happy', look=1, tilt=-3)], fps=2.6, seq='pingpong')
M['cn-boy-nod'] = frames_out(ART, 'cn-boy-nod', [person('cn-boy', right='chin', mouth='smile', eyes='open', look=-1, tilt=4),
                                             person('cn-boy', right='chin', mouth='smile', eyes='happy', look=-1, tilt=-2)], fps=1.2, seq='pingpong')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

import sys, os, random, math
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
R = random.Random(5)
FONT = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
def thermostat(t='24'):
    s = '<rect x="10" y="10" width="220" height="260" rx="40" fill="#F4F6F8"/><rect x="34" y="40" width="172" height="110" rx="14" fill="#1E3A5F"/>'
    s += f'<text x="120" y="122" font-size="76" fill="#7CE0FF" text-anchor="middle" {FONT}>{t}°</text>'
    s += '<circle cx="78" cy="200" r="30" fill="#E8304A"/><path d="M62,206 L78,188 L94,206" fill="none" stroke="#FFF" stroke-width="8" stroke-linecap="round"/>'
    s += '<circle cx="162" cy="200" r="30" fill="#2F95E6"/><path d="M146,194 L162,212 L178,194" fill="none" stroke="#FFF" stroke-width="8" stroke-linecap="round"/>'
    s += '<circle cx="190" cy="56" r="7" fill="#6DBE45"/>'
    return svg(240, 280, s)
def aircon():
    s = '<rect x="10" y="10" width="480" height="140" rx="26" fill="#F4F6F8"/><rect x="10" y="110" width="480" height="40" rx="16" fill="#DDE3EA"/>'
    for i in range(6):
        s += f'<path d="M50,{120+i*5} L450,{120+i*5}" stroke="#B9C2CC" stroke-width="2"/>'
    s += '<rect x="360" y="40" width="90" height="34" rx="8" fill="#1E3A5F"/><text x="405" y="66" font-size="24" fill="#7CE0FF" text-anchor="middle" font-family="sans-serif" font-weight="700">24°C</text>'
    s += '<circle cx="60" cy="50" r="8" fill="#2F95E6"/>'
    return svg(500, 160, s)
def heater():
    s = ''
    for i in range(7):
        s += f'<rect x="{20+i*44}" y="20" width="36" height="200" rx="16" fill="#F2F2EE"/>'
    s += '<rect x="10" y="60" width="330" height="16" rx="6" fill="#DADAD2"/><rect x="10" y="180" width="330" height="16" rx="6" fill="#DADAD2"/>'
    s += '<rect x="30" y="220" width="16" height="40" fill="#BDBDB5"/><rect x="304" y="220" width="16" height="40" fill="#BDBDB5"/><circle cx="350" cy="120" r="14" fill="#E8304A"/>'
    return svg(370, 270, s)
def thermometer(level):
    s = '<rect x="30" y="10" width="60" height="330" rx="30" fill="#FFFFFF"/><circle cx="60" cy="360" r="44" fill="#E8304A"/>'
    s += f'<rect x="48" y="{330-level}" width="24" height="{level+30}" rx="12" fill="#E8304A"/>'
    for i in range(10):
        s += f'<path d="M92,{40+i*28} L110,{40+i*28}" stroke="#1B1A1F" stroke-width="3"/>'
    return svg(130, 410, s)
def sofa():
    s = '<rect x="20" y="40" width="460" height="120" rx="30" fill="#3E8FE0"/><rect x="0" y="100" width="80" height="130" rx="26" fill="#2E6FD9"/><rect x="420" y="100" width="80" height="130" rx="26" fill="#2E6FD9"/>'
    s += '<rect x="70" y="140" width="360" height="70" rx="16" fill="#5AA5F0"/><path d="M250,140 L250,210" stroke="#2E6FD9" stroke-width="4"/>'
    s += '<rect x="100" y="70" width="90" height="70" rx="14" fill="#F2C230"/><rect x="320" y="70" width="90" height="70" rx="14" fill="#E8407A"/>'
    s += '<rect x="40" y="226" width="20" height="24" fill="#6B4426"/><rect x="440" y="226" width="20" height="24" fill="#6B4426"/>'
    return svg(500, 250, s)
def fishtank():
    s = '<rect x="10" y="20" width="420" height="250" rx="8" fill="#9ED8F5"/><rect x="10" y="60" width="420" height="210" fill="#4FB3E8"/>'
    s += '<path d="M10,240 C80,226 150,250 220,236 C300,222 360,248 430,234 L430,270 L10,270 Z" fill="#E6C98C"/>'
    for x in (60, 120, 330, 380):
        s += f'<path d="M{x},250 C{x-14},210 {x+14},180 {x},140" fill="none" stroke="#2E9D57" stroke-width="10" stroke-linecap="round"/>'
    for i in range(10):
        s += f'<circle cx="{R.randint(30,410)}" cy="{R.randint(246,264)}" r="5" fill="{R.choice(["#F4F1EA", "#C9B28A", "#E8407A"])}"/>'
    s += '<rect x="370" y="80" width="18" height="140" rx="9" fill="#5A6470"/><rect x="368" y="100" width="22" height="22" rx="4" fill="#E8304A"/>'
    s += '<rect x="0" y="10" width="440" height="20" rx="6" fill="#3A3F4B"/><rect x="10" y="270" width="420" height="20" rx="4" fill="#3A3F4B"/>'
    s += '<path d="M379,30 C379,0 470,0 470,40" fill="none" stroke="#3A3F4B" stroke-width="4"/>'
    s += '<rect x="440" y="30" width="80" height="60" rx="10" fill="#1E3A5F"/><text x="480" y="70" font-size="26" fill="#7CE0FF" text-anchor="middle" font-family="sans-serif" font-weight="700">26°</text>'
    return svg(530, 300, s)
def fish(c='#F28C28'):
    return svg(120, 70, f'<path d="M10,35 C30,5 80,5 95,35 C80,65 30,65 10,35 Z" fill="{c}"/><path d="M90,35 L118,12 L118,58 Z" fill="{c}"/><circle cx="30" cy="30" r="5" fill="#1B1A1F"/><path d="M50,20 C55,35 55,40 50,52" fill="none" stroke="#FFF" stroke-width="3"/>')
def bubble():
    return svg(40, 40, '<circle cx="20" cy="20" r="16" fill="#E6F6FF" opacity="0.8"/><circle cx="14" cy="14" r="4" fill="#FFF"/>')
def stopsign():   # 停住的手势牌（站住不动）
    return svg(200, 200, '<rect x="20" y="20" width="160" height="160" rx="20" fill="#E8304A"/><text x="100" y="125" font-size="64" fill="#FFF" text-anchor="middle" font-family="Noto Sans CJK SC, sans-serif" font-weight="900">站住</text>')
write_art(ART, 'thermostat.svg', thermostat()); write_art(ART, 'thermostat-26.svg', thermostat('26')); write_art(ART, 'thermostat-18.svg', thermostat('18'))
write_art(ART, 'aircon.svg', aircon()); write_art(ART, 'heater.svg', heater()); write_art(ART, 'sofa.svg', sofa()); write_art(ART, 'fishtank.svg', fishtank())
write_art(ART, 'fish.svg', fish()); write_art(ART, 'fish2.svg', fish('#F2C230')); write_art(ART, 'bubble.svg', bubble(), style=False)
for i, lv in enumerate((60, 120, 180, 240)):
    write_art(ART, f'thermometer_f{i}.svg', thermometer(lv))
write_art(ART, 'thermometer.svg', thermometer(150))
M = {}
# 热得擦汗（手到额头）/ 冷得抱住自己发抖 / 指着恒温器按键调温度 / 看鱼笑 / 站得笔直
M['cn-boy-hot'] = frames_out(ART, 'cn-boy-hot', [person('cn-boy', right=(-4, 84, 196, 160, 'open'), mouth='o', eyes='closed', brows='frown', tilt=-4),
                                               person('cn-boy', right=(-4, 84, 206, 158, 'open'), mouth='half', eyes='closed', brows='frown', tilt=2)], fps=2.5, seq='pingpong')
M['cn-girl-cold'] = frames_out(ART, 'cn-girl-cold', [person('cn-girl', left=(2, 92, -78, 96, 'fist'), right=(2, 92, -78, 96, 'fist'), mouth='flat', eyes='down', brows='frown', tilt=-3),
                                                   person('cn-girl', left=(2, 92, -78, 96, 'fist'), right=(2, 92, -78, 96, 'fist'), mouth='flat', eyes='down', brows='frown', tilt=3)], fps=6, seq='pingpong')
M['cn-girl-warm'] = frames_out(ART, 'cn-girl-warm', [person('cn-girl', left='thumb', mouth='laugh', eyes='happy', tilt=-4), person('cn-girl', left='thumb', mouth='smile', eyes='happy', tilt=3)], fps=1.5, seq='pingpong')
M['west-man-press'] = frames_out(ART, 'west-man-press', [person('west-man', left=(66, 106, 96, 92, 'point'), mouth='open', look=-1, brows='up'),
                                                       person('west-man', left=(64, 106, 104, 96, 'point'), mouth='half', look=-1)], fps=2.5, seq='pingpong')
M['west-woman-press'] = frames_out(ART, 'west-woman-press', [person('west-woman', right=(66, 106, 96, 92, 'point'), mouth='smile', look=1, brows='up'),
                                                           person('west-woman', right=(64, 106, 104, 96, 'point'), mouth='smile', look=1)], fps=2, seq='pingpong')
M['west-boy-stand'] = frames_out(ART, 'west-boy-stand', [person('west-boy', mouth='flat', brows='up'), person('west-boy', mouth='flat', brows='up', eyes='closed')], fps=0.7, seq='loop')
M['cn-girl-fish'] = frames_out(ART, 'cn-girl-fish', [person('cn-girl', left='chest', mouth='smile', eyes='happy', look=1, tilt=-6), person('cn-girl', left='chest', mouth='laugh', eyes='happy', look=1, tilt=2)], fps=1, seq='pingpong')
M['west-woman-read'] = frames_out(ART, 'west-woman-read', [person('west-woman', mouth='smile', eyes='down', tilt=-3), person('west-woman', mouth='smile', eyes='down', tilt=2)], fps=0.6, seq='pingpong')
json.dump(M, open(os.path.join(ART, 'word_motions.json'), 'w'), ensure_ascii=False, indent=1)
print(list(M))


# 6.36（第八十版）：thermostat 的画面设置用到 icon-thermo、icon-stat 两个小图标，以前没有画图的函数（缺图，批量出片卡在准备组）。
#   画法照 2026-11-19 本地批量出片时补的（温度计；站着的人 = stat“站住、保持不变”）
def icon_thermo():
    s = '<rect x="88" y="16" width="24" height="120" rx="12" fill="#E8304A"/><circle cx="100" cy="156" r="30" fill="#E8304A"/>'
    s += '<rect x="82" y="24" width="36" height="120" rx="18" fill="none" stroke="#1E3A5F" stroke-width="6"/>'
    for y in (44, 68, 92, 116):
        s += '<path d="M124,%d L146,%d" stroke="#1E3A5F" stroke-width="6" stroke-linecap="round"/>' % (y, y)
    return svg(200, 200, s)


def icon_stat():
    s = '<circle cx="100" cy="46" r="22" fill="#2F95E6"/>'
    s += '<path d="M100,68 L100,132" stroke="#2F95E6" stroke-width="18" stroke-linecap="round"/>'
    s += '<path d="M100,132 L78,176 M100,132 L122,176" stroke="#2F95E6" stroke-width="14" stroke-linecap="round"/>'
    s += '<path d="M100,90 L70,70 M100,90 L130,70" stroke="#2F95E6" stroke-width="14" stroke-linecap="round"/>'
    s += '<path d="M40,184 L160,184" stroke="#1E3A5F" stroke-width="8" stroke-linecap="round"/>'
    return svg(200, 200, s)


write_art(ART, 'icon-thermo.svg', icon_thermo())
write_art(ART, 'icon-stat.svg', icon_stat())

import sys, os, math, random, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
R = random.Random(11)


def bus():   # 城市公交车（侧面）：车窗、车门、路牌“18 路”、轮子
    s = '<rect x="10" y="20" width="500" height="170" rx="26" fill="#2E9E6A"/><rect x="10" y="120" width="500" height="22" fill="#F2F2F2"/>'
    s += '<rect x="10" y="150" width="500" height="40" rx="8" fill="#23845A"/>'
    for i in range(5):
        s += f'<rect x="{34+i*76}" y="40" width="64" height="62" rx="8" fill="#BFE3F8"/><path d="M{40+i*76},48 L{58+i*76},48" stroke="#FFFFFF" stroke-width="4"/>'
    s += '<rect x="412" y="40" width="44" height="130" rx="6" fill="#BFE3F8"/><path d="M434,40 L434,170" stroke="#23845A" stroke-width="4"/>'
    s += '<path d="M466,36 L500,36 C508,36 510,46 510,60 L510,110 L466,110 Z" fill="#9FD3F0"/>'
    s += f'<rect x="300" y="4" width="120" height="24" rx="5" fill="#2B2D33"/><text x="360" y="23" font-size="18" fill="#FFB020" text-anchor="middle" {CJK}>18 路</text>'
    for x in (110, 400):
        s += f'<circle cx="{x}" cy="190" r="32" fill="#2B2D33"/><circle cx="{x}" cy="190" r="14" fill="#C9CED6"/>'
    s += '<circle cx="500" cy="160" r="8" fill="#FFE27A"/><rect x="14" y="150" width="12" height="16" fill="#E8304A"/>'
    return svg(520, 225, s)


def cyclist(k):   # 骑车的男孩（侧面，往右骑）：两帧，脚蹬子一上一下
    s = ''
    for cx in (70, 232):
        s += f'<circle cx="{cx}" cy="200" r="50" fill="none" stroke="#2B2D33" stroke-width="7"/><circle cx="{cx}" cy="200" r="6" fill="#2B2D33"/>'
        for a in range(0, 180, 30):
            r = math.radians(a + 15 * k)
            s += f'<path d="M{cx-46*math.cos(r):.0f},{200-46*math.sin(r):.0f} L{cx+46*math.cos(r):.0f},{200+46*math.sin(r):.0f}" stroke="#8C939E" stroke-width="2"/>'
    s += '<path d="M70,200 L140,200 L122,122 Z M122,122 L205,118 L140,200 M205,118 L232,200" fill="none" stroke="#E8304A" stroke-width="8" stroke-linejoin="round"/>'
    s += '<path d="M205,118 L208,96 L228,92" fill="none" stroke="#3A3F4B" stroke-width="7" stroke-linecap="round"/><rect x="104" y="108" width="40" height="10" rx="5" fill="#3A3F4B"/>'
    a = math.radians(40 + 180 * k)
    p1 = (140 + 26 * math.cos(a), 200 + 26 * math.sin(a)); p2 = (140 - 26 * math.cos(a), 200 - 26 * math.sin(a))
    hip = (126, 104)
    def leg(p, col):
        kx = (hip[0] + p[0]) / 2 + 26; ky = (hip[1] + p[1]) / 2 - 14
        return (f'<path d="M{hip[0]},{hip[1]} L{kx:.0f},{ky:.0f} L{p[0]:.0f},{p[1]:.0f}" fill="none" stroke="{col}" stroke-width="17" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<ellipse cx="{p[0]+6:.0f}" cy="{p[1]+4:.0f}" rx="13" ry="7" fill="#2B2D33"/>')
    s += leg(p2, '#2F3A55')
    s += f'<path d="M140,200 L{p1[0]:.0f},{p1[1]:.0f} M140,200 L{p2[0]:.0f},{p2[1]:.0f}" stroke="#3A3F4B" stroke-width="6"/>'
    s += '<path d="M126,104 C134,74 150,56 170,46" fill="none" stroke="#2E6FD9" stroke-width="34" stroke-linecap="round"/>'
    s += leg(p1, '#3A4A6E')
    s += '<path d="M168,50 L196,74 L222,94" fill="none" stroke="#2E6FD9" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/><circle cx="224" cy="94" r="8" fill="#F6D7C3"/>'
    s += '<rect x="168" y="22" width="14" height="18" fill="#F6D7C3"/><circle cx="184" cy="16" r="22" fill="#F6D7C3"/>'
    s += '<path d="M160,12 C162,-8 200,-12 208,6 C196,2 184,4 176,10 C172,16 166,20 160,22 Z" fill="#1B1A1F"/>'
    s += '<circle cx="196" cy="14" r="3" fill="#1B1A1F"/><path d="M194,26 Q200,30 205,25" fill="none" stroke="#C0392B" stroke-width="2.5"/><circle cx="190" cy="22" r="5" fill="#F79CBB"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -12 300 274">{s}</svg>'


def bell(x, y, sc=1.0, tilt=0, slash=False, col='#F2A900'):
    g = (f'<g transform="translate({x} {y}) rotate({tilt}) scale({sc})">'
         f'<path d="M-26,18 C-24,-6 -20,-26 0,-28 C20,-26 24,-6 26,18 L32,26 L-32,26 Z" fill="{col}"/><circle cx="0" cy="32" r="7" fill="{col}"/><circle cx="0" cy="-30" r="4" fill="{col}"/>')
    if slash:
        g += '<path d="M-34,-30 L34,38" stroke="#E8304A" stroke-width="7" stroke-linecap="round"/>'
    return g + '</g>'


def phone(state, k=0):   # 手机“情景模式”：普通 / 静音 / 飞行，选中的那一行是蓝的
    s = '<rect x="0" y="0" width="240" height="440" rx="34" fill="#2B2D33"/><rect x="12" y="34" width="216" height="372" rx="10" fill="#F7F9FC"/>'
    s += '<rect x="96" y="14" width="48" height="8" rx="4" fill="#4A4F59"/><circle cx="120" cy="422" r="10" fill="#4A4F59"/>'
    s += f'<text x="26" y="58" font-size="15" fill="#3A3F4B" {CJK}>9:41</text><rect x="186" y="46" width="28" height="13" rx="3" fill="none" stroke="#3A3F4B" stroke-width="2"/><rect x="189" y="49" width="18" height="7" fill="#3A3F4B"/>'
    s += f'<text x="120" y="92" font-size="21" fill="#1B1A1F" text-anchor="middle" {CJK}>情景模式</text>'
    rows = (('normal', '普通模式'), ('silent', '静音模式'), ('plane', '飞行模式'))
    for i, (key, name) in enumerate(rows):
        y = 112 + i * 62
        on = key == state
        s += f'<rect x="24" y="{y}" width="192" height="50" rx="12" fill="{"#2E6FD9" if on else "#E6EBF2"}"/>'
        s += f'<text x="60" y="{y+33}" font-size="19" fill="{"#FFFFFF" if on else "#3A3F4B"}" {CJK}>{name}</text>'
        s += f'<rect x="166" y="{y+15}" width="38" height="20" rx="10" fill="{"#7FD36A" if on else "#B8C0CC"}"/><circle cx="{194 if on else 176}" cy="{y+25}" r="8" fill="#FFFFFF"/>'
        if key == 'plane':
            s += f'<path d="M36,{y+25} L54,{y+25} M46,{y+15} L52,{y+25} L46,{y+35}" stroke="{"#FFFFFF" if on else "#5A6170"}" stroke-width="4" fill="none" stroke-linecap="round"/>'
        else:
            s += bell(45, y + 22, 0.38, 0, key == 'silent', '#FFFFFF' if on else '#5A6170')
    if state == 'silent':
        s += bell(120, 340, 1.0, 0, True, '#8C939E')
    else:
        s += bell(120, 340, 1.0, (-14, 14)[k % 2], False, '#F2A900')
        s += f'<path d="M{70 - 6*k},322 q-12,18 0,36 M{170 + 6*k},322 q12,18 0,36" fill="none" stroke="#F2A900" stroke-width="5" stroke-linecap="round"/>'
    return svg(240, 440, s)


def sunhat(col='#E9C46A', band_='#E8304A'):   # 大遮阳帽：草帽、红丝带
    s = f'<ellipse cx="120" cy="82" rx="118" ry="24" fill="{col}"/><path d="M62,80 C62,30 84,12 120,12 C156,12 178,30 178,80 Z" fill="{col}"/>'
    s += f'<path d="M64,62 C96,72 144,72 176,62 L178,78 C144,88 96,88 62,78 Z" fill="{band_}"/><path d="M168,70 C190,76 196,94 186,104 M168,72 C180,88 172,100 162,106" fill="none" stroke="{band_}" stroke-width="7"/>'
    for i in range(6):
        s += f'<path d="M{20+i*36},84 C{40+i*36},90 {56+i*36},90 {70+i*36},84" fill="none" stroke="#C9A24A" stroke-width="2"/>'
    return svg(240, 110, s)


def hatshop():   # 帽子店门口：橱窗里三顶帽子（假人头），“今夏流行”海报，招牌 HATS 帽子店，人行道、街灯、花盆
    d = lg('hsSky', [(0, '#8FD0F5'), (1, '#E6F5FF')])
    s = '<rect width="1200" height="700" fill="url(#hsSky)"/>'
    s += '<rect x="0" y="80" width="1200" height="420" fill="#E9DCC7"/>'
    for x in range(0, 1200, 60):
        s += f'<path d="M{x},80 L{x},500" stroke="#DCCDB4" stroke-width="2"/>'
    for row in range(7):                                   # 墙上的砖缝
        y = 84 + row * 18
        for x in range(0 if row % 2 else 30, 1200, 60):
            s += f'<rect x="{x}" y="{y}" width="56" height="15" rx="2" fill="#E2D2B8"/>'
    for x in (40, 1000):                                    # 二楼的窗户、花箱
        s += f'<rect x="{x}" y="10" width="150" height="62" fill="#BFE3F8"/><path d="M{x+75},10 L{x+75},72 M{x},40 L{x+150},40" stroke="#8A5A3B" stroke-width="5"/>'
        s += f'<rect x="{x-6}" y="70" width="162" height="12" fill="#8A5A3B"/>'
        for k in range(5):
            s += f'<circle cx="{x+12+k*32}" cy="66" r="9" fill="{("#E8304A", "#F2C230", "#E8407A", "#FFFFFF", "#9B5DE5")[k]}"/><circle cx="{x+20+k*32}" cy="70" r="7" fill="#3DA557"/>'
    s += '<rect x="120" y="100" width="960" height="70" rx="6" fill="#7A2E3A"/>'
    s += f'<text x="600" y="150" font-size="46" fill="#F7E7C6" text-anchor="middle" {CJK}>HATS · 帽子店</text>'
    for i in range(12):
        s += f'<path d="M{150+i*76},170 L{188+i*76},170 L{176+i*76},210 L{162+i*76},210 Z" fill="{("#E8304A", "#FFFFFF")[i % 2]}"/>'
    s += '<rect x="160" y="215" width="560" height="270" rx="6" fill="#CFE9F7"/><rect x="160" y="215" width="560" height="270" rx="6" fill="none" stroke="#8A5A3B" stroke-width="12"/>'
    s += '<rect x="176" y="430" width="528" height="40" fill="#B98A5E"/>'
    for i in range(4):                                     # 橱窗里的小帽子、围巾、手提包
        x = 205 + i * 140
        s += f'<ellipse cx="{x}" cy="236" rx="26" ry="6" fill="{("#2E6FD9", "#E8407A", "#6DBE45", "#F28C28")[i]}"/><path d="M{x-14},236 C{x-14},222 {x-6},218 {x},218 C{x+6},218 {x+14},222 {x+14},236 Z" fill="{("#2E6FD9", "#E8407A", "#6DBE45", "#F28C28")[i]}"/>'
    s += '<path d="M180,260 C230,270 280,250 330,262 L330,276 C280,264 230,284 180,274 Z" fill="#9B5DE5"/><path d="M600,250 L660,250 L668,300 L592,300 Z" fill="#C0392B"/><path d="M610,250 C610,232 650,232 650,250" fill="none" stroke="#5A3A22" stroke-width="5"/>'
    s += '<path d="M160,215 L720,485 M720,215 L160,485" stroke="#FFFFFF" stroke-width="3" opacity="0.35"/>'

    for i, (hc, bc) in enumerate((('#E9C46A', '#E8304A'), ('#F4F1EA', '#2E6FD9'), ('#C98E66', '#2E7D32'))):
        x = 260 + i * 180
        s += f'<rect x="{x-6}" y="350" width="12" height="80" fill="#8C939E"/><ellipse cx="{x}" cy="330" rx="34" ry="40" fill="#F4E6D6"/>'
        s += f'<ellipse cx="{x}" cy="300" rx="70" ry="15" fill="{hc}"/><path d="M{x-36},300 C{x-36},262 {x-20},250 {x},250 C{x+20},250 {x+36},262 {x+36},300 Z" fill="{hc}"/><rect x="{x-36}" y="284" width="72" height="12" fill="{bc}"/>'
        s += f'<rect x="{x-30}" y="392" width="60" height="26" rx="4" fill="#FFFFFF"/><text x="{x}" y="411" font-size="17" fill="#C0392B" text-anchor="middle" {CJK}>¥{(99, 129, 89)[i]}</text>'
    s += '<rect x="760" y="215" width="150" height="285" fill="#8A5A3B"/><rect x="772" y="228" width="126" height="272" fill="#B5835A"/><circle cx="880" cy="370" r="7" fill="#F2C230"/>'
    s += '<rect x="940" y="230" width="190" height="230" rx="8" fill="#FFF4DD"/><rect x="940" y="230" width="190" height="230" rx="8" fill="none" stroke="#E8304A" stroke-width="6"/>'
    s += f'<text x="1035" y="285" font-size="34" fill="#E8304A" text-anchor="middle" {CJK}>今夏流行</text><text x="1035" y="325" font-size="26" fill="#2E6FD9" text-anchor="middle" {CJK}>NEW</text>'
    s += '<ellipse cx="1035" cy="400" rx="70" ry="13" fill="#E9C46A"/><path d="M1000,400 C1000,368 1014,358 1035,358 C1056,358 1070,368 1070,400 Z" fill="#E9C46A"/><rect x="1000" y="384" width="70" height="10" fill="#E8304A"/>'
    s += '<rect x="0" y="500" width="1200" height="200" fill="#CFC8BB"/>'
    for i in range(0, 1200, 70):
        s += f'<path d="M{i},500 L{i-14},700" stroke="#B8B0A2" stroke-width="2"/>'
    s += '<path d="M0,600 L1200,600" stroke="#B8B0A2" stroke-width="2"/>'
    for x in (60, 1150):
        s += f'<rect x="{x-4}" y="250" width="8" height="250" fill="#3A3F4B"/><path d="M{x-24},250 L{x+24},250 L{x+14},226 L{x-14},226 Z" fill="#2B2D33"/><circle cx="{x}" cy="240" r="9" fill="#FFE27A"/>'
    for x in (100, 1100):
        s += f'<rect x="{x-34}" y="470" width="68" height="40" rx="6" fill="#B5432F"/><circle cx="{x-14}" cy="458" r="18" fill="#3DA557"/><circle cx="{x+12}" cy="452" r="20" fill="#2F8F46"/><circle cx="{x}" cy="440" r="8" fill="#E8407A"/>'
    s += '<path d="M560,40 C600,30 640,40 660,34" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round"/>'
    s += '<rect x="560" y="520" width="140" height="14" rx="4" fill="#8A5A3B"/><rect x="560" y="540" width="140" height="10" rx="4" fill="#8A5A3B"/><rect x="568" y="550" width="8" height="34" fill="#3A3F4B"/><rect x="684" y="550" width="8" height="34" fill="#3A3F4B"/>'
    s += '<rect x="730" y="520" width="40" height="60" rx="6" fill="#2E7D32"/><rect x="726" y="514" width="48" height="10" rx="3" fill="#1F5E22"/>'
    s += '<circle cx="380" cy="560" r="26" fill="none" stroke="#3A3F4B" stroke-width="5"/><circle cx="460" cy="560" r="26" fill="none" stroke="#3A3F4B" stroke-width="5"/><path d="M380,560 L410,524 L450,524 L460,560 M410,524 L420,560 L450,524" fill="none" stroke="#2E6FD9" stroke-width="5"/>'
    for x, c in ((280, '#E8407A'), (860, '#2E6FD9'), (990, '#6DBE45')):
        s += f'<ellipse cx="{x}" cy="690" rx="30" ry="6" fill="#B8B0A2"/>'
    for i in range(10):
        s += f'<circle cx="{40+i*120}" cy="{640 + (i % 3) * 14}" r="4" fill="#B8B0A2"/>'

    return svg(1200, 700, s, d)


def chalkboard():   # 黑板：一组数 3、5、5、7（粉笔字）
    s = '<rect x="0" y="0" width="640" height="300" rx="10" fill="#8A5A3B"/><rect x="14" y="14" width="612" height="272" rx="6" fill="#2F5D4A"/>'
    s += f'<text x="40" y="70" font-size="34" fill="#F4F1EA" {CJK}>一组数：</text>'
    for i, n in enumerate('3557'):
        s += f'<text x="{120+i*130}" y="190" font-size="96" fill="#FFFFFF" text-anchor="middle" font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700">{n}</text>'
        if i < 3:
            s += f'<text x="{176+i*130}" y="190" font-size="60" fill="#FFFFFF" text-anchor="middle" font-family="Noto Sans, sans-serif">,</text>'
    s += '<rect x="560" y="268" width="50" height="14" rx="4" fill="#F4F1EA"/><rect x="480" y="270" width="60" height="12" rx="4" fill="#C9D3E2"/>'
    return svg(640, 300, s)


def chalkring():
    return svg(140, 140, '<ellipse cx="70" cy="70" rx="58" ry="62" fill="none" stroke="#FFD43B" stroke-width="9"/>')


def ruler():   # 木尺：刻度、数字
    s = '<rect x="0" y="0" width="560" height="70" rx="6" fill="#E9C27A"/><rect x="0" y="52" width="560" height="18" fill="#D8AE62"/>'
    for i in range(0, 53):
        h = 30 if i % 5 == 0 else 16
        s += f'<path d="M{20+i*10},0 L{20+i*10},{h}" stroke="#5A3A22" stroke-width="2"/>'
        if i % 10 == 0:
            s += f'<text x="{20+i*10}" y="48" font-size="15" fill="#5A3A22" text-anchor="middle" font-family="sans-serif">{i//10}</text>'
    return svg(560, 70, s)


def plank():
    s = '<rect x="0" y="0" width="600" height="90" rx="6" fill="#C98E5A"/>'
    for y in (20, 44, 66):
        s += f'<path d="M10,{y} C150,{y-6} 300,{y+6} 590,{y-2}" fill="none" stroke="#A86E3E" stroke-width="3"/>'
    s += '<ellipse cx="420" cy="44" rx="20" ry="9" fill="none" stroke="#A86E3E" stroke-width="3"/>'
    return svg(600, 90, s)


write_art(ART, 'bus.svg', bus())
write_art(ART, 'cyclist_f0.svg', cyclist(0)); write_art(ART, 'cyclist_f1.svg', cyclist(1))
write_art(ART, 'phone-ring_f0.svg', phone('normal', 0)); write_art(ART, 'phone-ring_f1.svg', phone('normal', 1)); write_art(ART, 'phone-silent.svg', phone('silent'))
write_art(ART, 'sunhat.svg', sunhat()); write_art(ART, 'hatshop-bg.svg', hatshop(), bg=True)
write_art(ART, 'chalkboard.svg', chalkboard()); write_art(ART, 'chalkring.svg', chalkring(), style=False)
write_art(ART, 'ruler.svg', ruler()); write_art(ART, 'plank.svg', plank())
hat = sunhat(); hat2 = sunhat('#F4F1EA', '#2E6FD9')
M = {}
M['west-woman-hat'] = frames_out(ART, 'west-woman-hat', [holding('west-woman', hat, 240, 6, 240, 110, right='present', mouth='smile', eyes='happy', tilt=-2),
                                                     holding('west-woman', hat, 240, 6, 240, 110, right='present2', mouth='laugh', eyes='happy', tilt=3)], fps=1.4, seq='pingpong')
M['cn-girl-hat'] = frames_out(ART, 'cn-girl-hat', [holding('cn-girl', hat2, 240, 6, 240, 110, left='point', mouth='open', look=-1, brows='up'),
                                               holding('cn-girl', hat2, 240, 6, 240, 110, left='point', mouth='half', look=-1, tilt=2)], fps=2.5, seq='pingpong')
M['cn-boy-hat'] = frames_out(ART, 'cn-boy-hat', [holding('cn-boy', sunhat('#C98E66', '#2E7D32'), 240, 6, 240, 110, left='thumb', mouth='laugh', eyes='happy', tilt=4),
                                             holding('cn-boy', sunhat('#C98E66', '#2E7D32'), 240, 6, 240, 110, left='thumb', mouth='smile', eyes='happy', tilt=-2)], fps=1.6, seq='pingpong')
M['west-woman-hat2'] = frames_out(ART, 'west-woman-hat2', [holding('west-woman', hat, 240, 6, 240, 110, left='hello', mouth='open', eyes='open', brows='up', tilt=2),
                                                       holding('west-woman', hat, 240, 6, 240, 110, left='wave2', mouth='smile', eyes='happy', tilt=-2)], fps=2.2, seq='pingpong')
M['west-girl-hat'] = frames_out(ART, 'west-girl-hat', [holding('west-girl', sunhat('#F4F1EA', '#E8407A'), 240, 6, 240, 110, right='thumb', mouth='laugh', eyes='happy', tilt=-4),
                                                   holding('west-girl', sunhat('#F4F1EA', '#E8407A'), 240, 6, 240, 110, right='thumb', mouth='smile', eyes='happy', tilt=2)], fps=1.6, seq='pingpong')
json.dump(M, open(os.path.join(ART, 'word_motions.json'), 'w'), ensure_ascii=False, indent=1)
print(list(M))

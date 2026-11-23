import sys, os, math, random, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
R = random.Random(55)
def bathroom_bg():   # 卫生间：瓷砖墙、淋浴间（磨砂玻璃门、花洒）、洗手池和镜子、马桶、毛巾架、窗户、绿植、地垫、“福”字贴
    d = lg('btW', [(0, '#E8F2F8'), (1, '#D4E4EE')])
    s = '<rect width="1200" height="700" fill="url(#btW)"/>'
    for j in range(14):
        for i in range(25):
            s += f'<rect x="{i*48+2}" y="{j*42+2}" width="44" height="38" rx="3" fill="#DCEAF2"/>'
    s += '<rect x="0" y="590" width="1200" height="110" fill="#B9C7D2"/>'
    for i in range(0, 1200, 60):
        s += f'<path d="M{i},590 L{i-30},700" stroke="#A3B2BE" stroke-width="3"/>'
    # 淋浴间（左）
    s += '<rect x="60" y="80" width="380" height="510" fill="#C9DCE8"/><rect x="60" y="560" width="380" height="30" fill="#E6EEF4"/>'
    s += '<path d="M180,80 L180,140 L300,140" fill="none" stroke="#9AA3AE" stroke-width="10"/><path d="M270,130 L330,130 L320,160 L280,160 Z" fill="#C9CFD8"/>'
    s += '<rect x="340" y="300" width="40" height="80" rx="6" fill="#E8E8E8"/><circle cx="360" cy="320" r="8" fill="#2F95E6"/><circle cx="360" cy="350" r="8" fill="#E8304A"/>'
    s += '<rect x="80" y="380" width="60" height="22" rx="4" fill="#F2C230"/><rect x="150" y="372" width="30" height="30" rx="6" fill="#6DBE45"/>'
    # 洗手池、镜子（中）
    s += '<rect x="560" y="120" width="200" height="220" rx="16" fill="#BFE3F8"/><path d="M590,150 L640,140 M590,190 L700,160" stroke="#FFFFFF" stroke-width="8"/><rect x="550" y="110" width="220" height="240" rx="20" fill="none" stroke="#C9A227" stroke-width="10"/>'
    s += '<rect x="540" y="380" width="240" height="40" rx="14" fill="#F4F6F8"/><rect x="570" y="420" width="180" height="170" fill="#C98B4A"/><path d="M660,420 L660,590" stroke="#8C5A2B" stroke-width="4"/><circle cx="645" cy="505" r="6" fill="#F2C230"/><circle cx="675" cy="505" r="6" fill="#F2C230"/>'
    s += '<path d="M650,380 L650,350 L690,350" fill="none" stroke="#9AA3AE" stroke-width="8"/><rect x="580" y="350" width="24" height="30" rx="4" fill="#E8407A"/><rect x="730" y="356" width="20" height="24" rx="4" fill="#25B5C9"/>'
    # 马桶、毛巾架、窗、植物（右）
    s += '<rect x="900" y="440" width="120" height="40" rx="10" fill="#F4F6F8"/><path d="M910,480 L1010,480 L990,590 L930,590 Z" fill="#F4F6F8"/><rect x="980" y="380" width="70" height="70" rx="8" fill="#F4F6F8"/>'
    s += '<rect x="820" y="200" width="160" height="10" rx="5" fill="#9AA3AE"/><rect x="840" y="210" width="50" height="120" fill="#E8407A"/><rect x="900" y="210" width="60" height="140" fill="#2F95E6"/>'
    s += '<rect x="1040" y="100" width="130" height="150" fill="#9ED0EE"/><path d="M1105,100 L1105,250 M1040,175 L1170,175" stroke="#FFFFFF" stroke-width="8"/><rect x="1032" y="92" width="146" height="166" fill="none" stroke="#FFFFFF" stroke-width="10"/>'
    s += '<path d="M1080,590 L1150,590 L1140,520 L1090,520 Z" fill="#C0643A"/><circle cx="1115" cy="490" r="40" fill="#3E8F3E"/><circle cx="1092" cy="474" r="24" fill="#56A94F"/>'
    s += '<rect x="560" y="610" width="200" height="50" rx="20" fill="#9B5DE5"/><rect x="600" y="40" width="70" height="70" fill="#D2232A" transform="rotate(45 635 75)"/><text x="635" y="92" font-size="40" fill="#F2C230" text-anchor="middle" font-family="Noto Sans CJK SC, sans-serif" font-weight="700">福</text>'
    return svg(1200, 700, s, d)
def stall(glass=True, on=False):   # 淋浴间特写：花洒、磨砂玻璃门
    s = '<rect x="20" y="20" width="360" height="460" fill="#DCEAF2"/>' + ''.join(f'<rect x="{24+i*44}" y="{24+j*40}" width="40" height="36" rx="3" fill="#E8F2F8"/>' for i in range(8) for j in range(11))
    s += '<path d="M120,20 L120,70 L230,70" fill="none" stroke="#9AA3AE" stroke-width="10"/><path d="M200,60 L262,60 L252,90 L210,90 Z" fill="#C9CFD8"/>'
    if on:
        for k in range(9):
            x = 214 + k * 5
            s += f'<path d="M{x},95 L{x-30+k*7},420" stroke="#7CC4F2" stroke-width="3" stroke-dasharray="14 10" opacity="0.8"/>'
    s += '<rect x="20" y="450" width="360" height="30" fill="#C9D3DC"/>'
    if glass:
        s += '<rect x="40" y="140" width="320" height="320" rx="6" fill="#EAF4FA" opacity="0.65"/><rect x="40" y="140" width="320" height="320" rx="6" fill="none" stroke="#9AA3AE" stroke-width="6"/><circle cx="330" cy="300" r="8" fill="#9AA3AE"/>'
    return svg(400, 500, s)
def drop():
    return svg(30, 50, '<path d="M15,0 C20,15 28,25 28,34 C28,44 22,50 15,50 C8,50 2,44 2,34 C2,25 10,15 15,0 Z" fill="#7CC4F2"/>')
def streak():
    return svg(20, 60, '<path d="M15,0 L5,60" stroke="#9EC9E8" stroke-width="5" stroke-linecap="round"/>')
def steam():
    return svg(120, 120, '<path d="M30,110 C10,80 50,70 30,40 C20,20 40,10 40,0 M70,110 C50,80 90,70 70,40 C60,20 80,10 80,0" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.8"/>')
def umbrella(c='#E8304A'):
    return svg(240, 200, f'<path d="M10,90 C30,20 210,20 230,90 C200,76 170,76 150,90 C130,76 110,76 90,90 C70,76 40,76 10,90 Z" fill="{c}"/><path d="M120,90 L120,180 C120,196 100,196 98,182" fill="none" stroke="#3A3F4B" stroke-width="8"/><path d="M120,20 L120,6" stroke="#3A3F4B" stroke-width="6"/>')
def cap_head():   # 淋浴间磨砂玻璃上面露出的头：戴浴帽，脸是男孩的
    p = person('cn-boy', mouth='laugh', eyes='happy')
    vb, body = inner(p)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}<path d="M282,118 C270,40 450,40 438,118 C420,104 300,104 282,118 Z" fill="#FF9EB5"/></svg>'
write_art(ART, 'bathroom-bg.svg', bathroom_bg(), bg=True)
write_art(ART, 'stall.svg', stall(True, False)); write_art(ART, 'stall-on.svg', stall(True, True)); write_art(ART, 'stall-open.svg', stall(False, False))
write_art(ART, 'drop.svg', drop()); write_art(ART, 'streak.svg', streak()); write_art(ART, 'steam.svg', steam(), style=False)
write_art(ART, 'umbrella.svg', umbrella()); write_art(ART, 'umbrella2.svg', umbrella('#2E6FD9'))
M = {}
ub = open(os.path.join(ART, 'umbrella.svg')).read(); ub2 = open(os.path.join(ART, 'umbrella2.svg')).read()
def with_umbrella(who, cx, hand, col, **kw):   # 人举着伞：伞面在头顶（画布 y 0–64），伞柄斜着下来到手里
    vb, body = inner(person(who, **kw))
    hx, hy = hand
    u = (f'<path d="M{cx},62 L{hx},{hy}" stroke="#3A3F4B" stroke-width="7"/>'
         f'<path d="M{cx-160},64 C{cx-140},10 {cx+140},10 {cx+160},64 C{cx+130},52 {cx+100},52 {cx+80},64 C{cx+55},52 {cx+25},52 {cx},64 C{cx-25},52 {cx-55},52 {cx-80},64 C{cx-100},52 {cx-130},52 {cx-160},64 Z" fill="{col}" stroke="#1B1A1F" stroke-width="4"/>'
         f'<path d="M{cx},14 L{cx},2" stroke="#3A3F4B" stroke-width="6"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}{u}</svg>'
M['cn-girl-umbrella'] = frames_out(ART, 'cn-girl-umbrella', [with_umbrella('cn-girl', 400, (512, 300), '#E8304A', right=(30, 100, 175, 60, 'fist'), mouth='smile', look=1),
                                                           with_umbrella('cn-girl', 402, (512, 300), '#E8304A', right=(30, 100, 175, 60, 'fist'), mouth='open', look=1, tilt=2)], fps=1.0, seq='pingpong')
M['west-man-umbrella'] = frames_out(ART, 'west-man-umbrella', [with_umbrella('west-man', 320, (208, 300), '#2E6FD9', left=(30, 100, 175, 60, 'fist'), mouth='o', brows='up', look=-1),
                                                             with_umbrella('west-man', 318, (208, 300), '#2E6FD9', left=(30, 100, 175, 60, 'fist'), mouth='open', brows='up', look=-1, tilt=-2)], fps=1.0, seq='pingpong')
M['boy-cap'] = frames_out(ART, 'boy-cap', [cap_head(), cap_head()], fps=1, seq='loop')
json.dump(M, open(os.path.join(ART, 'word_motions.json'), 'w'), ensure_ascii=False, indent=1)
print(list(M))

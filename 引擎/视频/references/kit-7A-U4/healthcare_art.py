import sys, os, math, random, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'
R = random.Random(25)
# 6.30（第七十四版）：25 health care（图画书风）。要先跑 alarm_art.py（卧室、床）。
# health 健康：公园里阿姨打太极，有人跑步经过；care 照顾：妈妈端水给发烧躺在床上的孩子；
# 医疗保健：社区卫生服务中心诊室里，外国医生戴听诊器给中国女孩看病，护士拿着疫苗针（看病、护理、预防）


def clinic_bg():   # 诊室：绿十字招牌、视力表、身高尺、药柜、诊疗床和帘子、办公桌电脑、洗手池和“勤洗手”海报、挂钟、窗户百叶、绿植、椅子
    d = lg('clW', [(0, '#EEF7F6'), (1, '#E0EFEE')])
    s = '<rect width="1200" height="700" fill="url(#clW)"/><rect x="0" y="430" width="1200" height="150" fill="#CFE3E2"/><path d="M0,430 L1200,430" stroke="#A9C9C7" stroke-width="6"/>'
    s += '<rect x="0" y="580" width="1200" height="120" fill="#D8D2C4"/>'
    for i in range(0, 1200, 100):
        for j, y in enumerate((580, 620, 660)):
            s += f'<rect x="{i + (50 if j % 2 else 0) + 2}" y="{y+2}" width="96" height="36" fill="#E2DDD1"/>'
    s += '<rect x="330" y="30" width="540" height="90" rx="12" fill="#FFFFFF" stroke="#2B8A3E" stroke-width="6"/>'
    s += '<rect x="356" y="48" width="18" height="54" fill="#2B8A3E"/><rect x="338" y="66" width="54" height="18" fill="#2B8A3E"/>'
    s += f'<text x="620" y="74" font-size="32" fill="#2B8A3E" text-anchor="middle" {CJK}>社区卫生服务中心</text><text x="620" y="106" font-size="22" fill="#2B8A3E" text-anchor="middle" {EN}>Community Health Centre</text>'
    s += '<rect x="40" y="150" width="210" height="230" fill="#BFE3F2" stroke="#FFFFFF" stroke-width="12"/>'
    for i in range(10):
        s += f'<rect x="46" y="{158 + i * 22}" width="198" height="12" fill="#F7FBFD"/>'
    s += '<path d="M145,150 L145,380" stroke="#FFFFFF" stroke-width="6"/>'
    s += '<rect x="290" y="160" width="120" height="200" rx="6" fill="#FFFFFF" stroke="#C9D6DE" stroke-width="4"/>'
    for i, (n, sz) in enumerate(((1, 44), (2, 32), (3, 24), (4, 18), (5, 14), (6, 11))):
        y = 200 + i * 28
        for k in range(n):
            rot = R.choice((0, 90, 180, 270))
            x = 350 - (n - 1) * sz * 0.65 + k * sz * 1.3
            s += f'<text x="{x:.0f}" y="{y}" font-size="{sz}" fill="#1B1A1F" text-anchor="middle" transform="rotate({rot} {x:.0f} {y - sz * 0.35:.0f})" {EN}>E</text>'
    s += '<rect x="440" y="150" width="34" height="280" fill="#FFFFFF" stroke="#C9D6DE" stroke-width="3"/>'
    for i in range(14):
        w = 16 if i % 2 == 0 else 9
        s += f'<path d="M440,{160 + i * 19} L{440 + w},{160 + i * 19}" stroke="#E8304A" stroke-width="3"/>'
    s += '<rect x="900" y="150" width="250" height="270" rx="8" fill="#F7FBFD" stroke="#9FB8C2" stroke-width="6"/><path d="M1025,150 L1025,420 M900,240 L1150,240 M900,330 L1150,330" stroke="#9FB8C2" stroke-width="5"/>'
    for row, y in enumerate((232, 322, 412)):
        for k in range(4):
            x = 916 + k * 56 + (12 if k >= 2 else 0)
            c = R.choice(['#E8304A', '#2E6FD9', '#F2C230', '#2B8A3E', '#FFFFFF', '#C9A0F0'])
            h = R.choice((40, 52, 60))
            s += f'<rect x="{x}" y="{y-h}" width="34" height="{h}" rx="6" fill="{c}"/><rect x="{x+6}" y="{y-h-10}" width="22" height="12" rx="3" fill="#5A6470"/>'
    s += '<path d="M500,140 L860,140" stroke="#9FB8C2" stroke-width="8"/>'
    for i in range(8):
        x = 506 + i * 22
        s += f'<path d="M{x},144 C{x+8},250 {x-8},350 {x+4},470 L{x+20},470 C{x+12},350 {x+28},250 {x+20},144 Z" fill="#BFE3D9"/>'
    s += '<rect x="560" y="430" width="300" height="40" rx="10" fill="#FFFFFF"/><rect x="560" y="460" width="300" height="30" rx="6" fill="#7FB8E6"/><rect x="580" y="490" width="16" height="90" fill="#9AA3AE"/><rect x="824" y="490" width="16" height="90" fill="#9AA3AE"/>'
    s += '<rect x="566" y="412" width="90" height="30" rx="14" fill="#FFFFFF" stroke="#C9D6DE" stroke-width="3"/>'
    s += '<rect x="40" y="470" width="260" height="22" fill="#B07A2E"/><rect x="56" y="492" width="16" height="90" fill="#8B5A2B"/><rect x="268" y="492" width="16" height="90" fill="#8B5A2B"/>'
    s += '<rect x="70" y="390" width="120" height="80" rx="6" fill="#2B2D33"/><rect x="78" y="398" width="104" height="62" fill="#7FB8E6"/><path d="M90,416 L170,416 M90,432 L150,432 M90,448 L160,448" stroke="#FFFFFF" stroke-width="5"/>'
    s += '<rect x="122" y="470" width="16" height="8" fill="#2B2D33"/><rect x="210" y="440" width="60" height="30" fill="#FFFFFF"/><rect x="236" y="430" width="20" height="40" rx="4" fill="#E8304A"/>'
    s += '<rect x="960" y="470" width="130" height="30" rx="6" fill="#FFFFFF"/><rect x="1000" y="500" width="50" height="80" fill="#E2EAF0"/><path d="M1025,470 L1025,446 L1048,446" fill="none" stroke="#9AA3AE" stroke-width="6"/>'
    s += '<rect x="900" y="40" width="250" height="90" rx="10" fill="#FFF3B0"/><circle cx="944" cy="85" r="28" fill="#F3D2BE"/>'
    for k in range(4):
        s += f'<rect x="{928 + k * 9}" y="{50 + (k % 2) * 4}" width="7" height="26" rx="3" fill="#F3D2BE"/>'
    for k in range(5):
        s += f'<circle cx="{964 + k * 6}" cy="{70 + k * 6}" r="4" fill="#7FB8E6"/>'
    s += f'<text x="1060" y="80" font-size="26" fill="#C0392B" text-anchor="middle" {CJK}>勤洗手</text><text x="1060" y="112" font-size="18" fill="#5A4632" text-anchor="middle" {EN}>Wash your hands</text>'
    s += '<circle cx="520" cy="190" r="34" fill="#FFFFFF" stroke="#2B8A3E" stroke-width="6"/><path d="M520,190 L520,168 M520,190 L536,198" stroke="#1B1A1F" stroke-width="5" stroke-linecap="round"/>'
    s += '<path d="M1160,580 L1170,520 L1196,520 L1200,580 Z" fill="#B8613A"/><circle cx="1180" cy="490" r="36" fill="#4E9A3E"/><circle cx="1168" cy="470" r="16" fill="#7CC160"/>'
    for x in (330, 410):
        s += f'<rect x="{x}" y="520" width="60" height="12" rx="4" fill="#2E6FD9"/><rect x="{x}" y="470" width="12" height="62" fill="#2E6FD9"/><path d="M{x+6},532 L{x+6},580 M{x+54},532 L{x+54},580" stroke="#47525C" stroke-width="6"/>'
    return svg(1200, 700, s, d)


def stethoscope():
    s = '<path d="M20,10 C10,60 30,100 60,104 C90,100 110,60 100,10" fill="none" stroke="#2B2D33" stroke-width="8" stroke-linecap="round"/>'
    s += '<path d="M60,104 L60,128 C60,150 84,156 92,140" fill="none" stroke="#2B2D33" stroke-width="7"/><circle cx="96" cy="136" r="13" fill="#B8C0C9" stroke="#2B2D33" stroke-width="4"/>'
    return svg(120, 160, s)


def syringe():
    s = '<rect x="20" y="22" width="110" height="26" rx="5" fill="#E2F3FB" stroke="#7FB8E6" stroke-width="4"/><rect x="24" y="26" width="60" height="18" fill="#9ED3F0"/>'
    s += '<rect x="130" y="30" width="20" height="10" fill="#B8C0C9"/><path d="M150,35 L196,35" stroke="#9AA3AE" stroke-width="3"/><rect x="2" y="18" width="18" height="34" rx="4" fill="#7FB8E6"/>'
    for x in (40, 56, 72, 88, 104):
        s += f'<path d="M{x},22 L{x},32" stroke="#5A8FB0" stroke-width="2"/>'
    return svg(200, 70, s)


def badge():   # 胸前的红十字牌
    return svg(80, 80, '<rect x="4" y="4" width="72" height="72" rx="12" fill="#FFFFFF" stroke="#E8304A" stroke-width="5"/><rect x="32" y="16" width="16" height="48" fill="#E8304A"/><rect x="16" y="32" width="48" height="16" fill="#E8304A"/>')


def icon_health():
    return svg(200, 200, '<path d="M100,176 C30,126 10,90 22,58 C36,22 84,22 100,56 C116,22 164,22 178,58 C190,90 170,126 100,176 Z" fill="#E8304A"/>'
               '<rect x="90" y="66" width="20" height="64" fill="#FFFFFF"/><rect x="68" y="88" width="64" height="20" fill="#FFFFFF"/>')


def icon_care():
    s = '<path d="M100,110 C64,84 56,64 64,48 C74,30 96,34 100,52 C104,34 126,30 136,48 C144,64 136,84 100,110 Z" fill="#F27A8A"/>'
    s += '<path d="M14,120 C40,120 60,140 100,150 C140,140 160,120 186,120 L186,150 C160,150 140,176 100,180 C60,176 40,150 14,150 Z" fill="#F3C9A8"/>'
    return svg(200, 200, s)


write_art(ART, 'clinic-bg.svg', clinic_bg(), bg=True); write_art(ART, 'stethoscope.svg', stethoscope()); write_art(ART, 'syringe.svg', syringe())
write_art(ART, 'icon-health.svg', icon_health()); write_art(ART, 'icon-care.svg', icon_care())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
HOLD = (20, 100, 120, 70, 'fist')
st, sy, bd = stethoscope(), syringe(), badge()
mug = open(os.path.join(ART, 'mug.svg'), encoding='utf-8').read() if os.path.exists(os.path.join(ART, 'mug.svg')) else svg(100, 100, '<rect x="20" y="20" width="60" height="70" rx="8" fill="#FFFFFF"/>')
M['cn-teacher-taichi'] = frames_out(ART, 'cn-teacher-taichi', [person('cn-teacher', left='present', eyes='closed', mouth='smile', top='#FFFFFF', collar='#E8304A'),
                                                             person('cn-teacher', right='present', eyes='closed', mouth='smile', top='#FFFFFF', collar='#E8304A', tilt=3)], fps=0.6, seq='pingpong')
M['cn-boy-sick'] = frames_out(ART, 'cn-boy-sick', [person('cn-boy', eyes='closed', mouth='flat', brows='frown', top='#7FB8E6'),
                                                 person('cn-boy', mouth='smile', look=1, top='#7FB8E6', tilt=-3)], fps=0.7, seq='pingpong')
M['cn-teacher-care'] = frames_out(ART, 'cn-teacher-care', [holding('cn-teacher', mug, 300, 250, 110, 110, left=HOLD, right=HOLD, mouth='smile', look=-1, top='#F27A8A'),
                                                         holding('cn-teacher', mug, 300, 250, 110, 110, left=HOLD, right=HOLD, mouth='open', brows='up', look=-1, top='#F27A8A', tilt=-2)], fps=1.0, seq='pingpong')
M['west-man-doctor'] = frames_out(ART, 'west-man-doctor', [holding('west-man', st, 300, 226, 120, 160, right='present', mouth='open', look=1, top='#FFFFFF', collar='#7FB8E6'),
                                                         holding('west-man', st, 300, 226, 120, 160, right='point', mouth='smile', look=1, top='#FFFFFF', collar='#7FB8E6', tilt=2)], fps=1.3, seq='pingpong')
M['west-woman-nurse'] = frames_out(ART, 'west-woman-nurse', [holding('west-woman', svg(200, 110, nest(sy, 0, 0, 160, 56) + nest(bd, 160, 64, 40, 40, uid='b')), 300, 236, 150, 82, right=HOLD, mouth='smile', look=-1, top='#FFFFFF', collar='#F27A8A'),
                                                           holding('west-woman', svg(200, 110, nest(sy, 0, 0, 160, 56) + nest(bd, 160, 64, 40, 40, uid='b')), 300, 236, 150, 82, right=HOLD, mouth='open', brows='up', look=-1, top='#FFFFFF', collar='#F27A8A', tilt=-2)], fps=1.2, seq='pingpong')
M['cn-girl-patient'] = frames_out(ART, 'cn-girl-patient', [person('cn-girl', mouth='smile', look=-1, top='#F2C230'),
                                                         person('cn-girl', mouth='laugh', eyes='happy', look=-1, top='#F2C230', tilt=-3)], fps=1.0, seq='pingpong')
nk = svg(200, 110, nest(sy, 0, 0, 160, 56) + nest(bd, 160, 64, 40, 40, uid='b'))
M['west-man-doctor2'] = frames_out(ART, 'west-man-doctor2', [holding('west-man', st, 300, 226, 120, 160, right='chin', mouth='flat', brows='up', look=1, top='#FFFFFF', collar='#7FB8E6'),
                                                           holding('west-man', st, 300, 226, 120, 160, right='thumb', mouth='laugh', eyes='happy', look=1, top='#FFFFFF', collar='#7FB8E6', tilt=2)], fps=1.0, seq='pingpong')
M['west-woman-nurse2'] = frames_out(ART, 'west-woman-nurse2', [holding('west-woman', nk, 300, 236, 150, 82, right=HOLD, left='pointup', mouth='o', brows='up', look=-1, top='#FFFFFF', collar='#F27A8A'),
                                                             holding('west-woman', nk, 300, 236, 150, 82, right=HOLD, left='hello', mouth='smile', eyes='happy', look=-1, top='#FFFFFF', collar='#F27A8A', tilt=2)], fps=1.2, seq='pingpong')
M['cn-girl-shot'] = frames_out(ART, 'cn-girl-shot', [person('cn-girl', left='present', mouth='flat', eyes='closed', brows='frown', look=-1, top='#F2C230'),
                                                   person('cn-girl', left='present', right='thumb', mouth='smile', look=-1, top='#F2C230', tilt=-2)], fps=0.9, seq='pingpong')
M['west-boy-patient'] = frames_out(ART, 'west-boy-patient', [person('west-boy', right='chest', mouth='o', eyes='wide', look=-1, top='#7CC160'),
                                                           person('west-boy', right='chest', mouth='smile', look=-1, top='#7CC160', tilt=-3)], fps=1.0, seq='pingpong')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

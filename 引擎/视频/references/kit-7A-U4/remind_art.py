import sys, os, math, random, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'
R = random.Random(30)
# 6.30（第七十四版）：30 remind（先画图画书风，“都齐了”再转青绿工笔风）。要先跑 owner 的画图脚本（住宅区 home-bg）。
# re- 再：外国女孩捧着书再读一遍；mind 记起：女孩托着下巴，想起海边的暑假；使再想起来：冰箱上贴着“买牛奶”，男孩一看想起来；
# 提醒：下雨天妈妈在门口把伞递给要出门的孩子；使想起：一张照片让女孩想起海边；手机提醒“奶奶生日”；公园里的风筝让男孩想起小时候


def kitchen_bg():   # 厨房：白瓷砖墙、吊柜、灶台和锅、水槽和窗、挂着的勺铲、调料瓶、绿植、地砖
    s = '<rect width="1200" height="700" fill="#EEF3F5"/>'
    for j in range(0, 420, 40):
        for i in range(0, 1200, 60):
            s += f'<rect x="{i + 2}" y="{j + 2}" width="56" height="36" rx="3" fill="#F8FBFC"/>'
    s += '<rect x="0" y="560" width="1200" height="140" fill="#C9B79C"/>'
    for i in range(0, 1200, 100):
        s += f'<rect x="{i + 2}" y="562" width="96" height="66" fill="#D6C6AC"/><rect x="{i + 52}" y="632" width="96" height="66" fill="#D6C6AC"/>'
    s += '<rect x="0" y="40" width="1200" height="120" fill="#2E9E6A"/>'
    for i in range(0, 1200, 150):
        s += f'<rect x="{i + 6}" y="46" width="138" height="108" rx="6" fill="#3DB07A"/><circle cx="{i + 130}" cy="100" r="6" fill="#F2C230"/>'
    s += '<rect x="0" y="400" width="1200" height="160" fill="#8B5A2B"/><rect x="0" y="390" width="1200" height="20" fill="#5A4632"/>'
    for i in range(0, 1200, 150):
        s += f'<rect x="{i + 8}" y="420" width="134" height="126" rx="6" fill="#A86A32"/><rect x="{i + 64}" y="470" width="22" height="8" rx="3" fill="#F2C230"/>'
    s += '<rect x="420" y="190" width="300" height="190" fill="#BFE3F2" stroke="#FFFFFF" stroke-width="12"/><path d="M570,190 L570,380" stroke="#FFFFFF" stroke-width="8"/>'
    s += '<circle cx="480" cy="250" r="26" fill="#F2C230"/><path d="M430,380 L520,300 L600,360 L700,280 L710,380 Z" fill="#9DC59A"/>'
    s += '<rect x="460" y="384" width="220" height="16" rx="6" fill="#C9D6DE"/><path d="M570,384 L570,350 L600,350" fill="none" stroke="#9AA3AE" stroke-width="8"/>'
    s += '<rect x="780" y="370" width="220" height="24" rx="6" fill="#2B2D33"/><ellipse cx="840" cy="370" rx="40" ry="8" fill="#47525C"/><ellipse cx="940" cy="370" rx="40" ry="8" fill="#47525C"/>'
    s += '<rect x="900" y="320" width="90" height="50" rx="10" fill="#E8304A"/><rect x="880" y="316" width="130" height="10" rx="4" fill="#C0392B"/>'
    for x in (220, 260, 300):
        s += f'<path d="M{x},180 L{x},260" stroke="#9AA3AE" stroke-width="5"/><ellipse cx="{x}" cy="{270 + (x % 3) * 4}" rx="14" ry="18" fill="#B8C0C9"/>'
    s += '<path d="M200,176 L320,176" stroke="#5A4632" stroke-width="8"/>'
    for i, c in enumerate(('#E8304A', '#F2C230', '#2E9E6A', '#7B57D6', '#C8913A')):
        s += f'<rect x="{60 + i * 34}" y="{344 - (i % 2) * 10}" width="26" height="{46 + (i % 2) * 10}" rx="6" fill="{c}"/><rect x="{64 + i * 34}" y="{334 - (i % 2) * 10}" width="18" height="12" rx="3" fill="#5A4632"/>'
    s += '<path d="M1080,390 L1090,330 L1130,330 L1140,390 Z" fill="#B8613A"/><circle cx="1110" cy="300" r="40" fill="#4E9A3E"/><circle cx="1096" cy="282" r="18" fill="#7CC160"/>'
    return svg(1200, 700, s)


def fridge():   # 冰箱，门上贴着便利贴“买牛奶 Buy milk”和磁贴
    s = '<rect x="10" y="10" width="220" height="460" rx="18" fill="#F2F5F7" stroke="#C9D6DE" stroke-width="6"/><path d="M10,170 L230,170" stroke="#C9D6DE" stroke-width="6"/>'
    s += '<rect x="196" y="60" width="12" height="80" rx="5" fill="#9AA3AE"/><rect x="196" y="200" width="12" height="120" rx="5" fill="#9AA3AE"/>'
    s += '<g transform="rotate(-6 110 260)"><rect x="50" y="210" width="120" height="100" rx="4" fill="#FFE97A"/><circle cx="110" cy="214" r="9" fill="#E8304A"/>'
    s += f'<text x="110" y="256" font-size="24" fill="#2B2D33" text-anchor="middle" {CJK}>买牛奶</text><text x="110" y="290" font-size="20" fill="#1A66B8" text-anchor="middle" {EN}>Buy milk</text></g>'
    s += '<circle cx="60" cy="80" r="16" fill="#F27A8A"/><rect x="120" y="60" width="40" height="30" rx="6" fill="#7FB8E6"/><rect x="40" y="380" width="60" height="44" rx="4" fill="#FFFFFF" stroke="#C9D6DE" stroke-width="3"/>'
    s += '<path d="M48,410 L60,396 L72,408 L84,392 L94,410" fill="none" stroke="#2E9E6A" stroke-width="3"/>'
    return svg(240, 480, s)


def bubble(content):   # 想法泡泡（里面画回忆）
    s = '<circle cx="34" cy="226" r="10" fill="#FFFFFF"/><circle cx="60" cy="200" r="16" fill="#FFFFFF"/>'
    s += '<path d="M90,170 C40,170 40,100 90,94 C90,40 160,30 180,62 C200,24 280,34 280,82 C320,90 320,160 280,166 C270,198 200,198 186,176 C160,200 100,196 90,170 Z" fill="#FFFFFF"/>'
    return svg(320, 240, s + content)


def sea_memory():
    c = '<clipPath id="bc"><path d="M90,170 C40,170 40,100 90,94 C90,40 160,30 180,62 C200,24 280,34 280,82 C320,90 320,160 280,166 C270,198 200,198 186,176 C160,200 100,196 90,170 Z"/></clipPath>'
    c += '<g clip-path="url(#bc)"><rect x="40" y="30" width="290" height="100" fill="#BFE6FF"/><circle cx="250" cy="70" r="20" fill="#F2C230"/>'
    c += '<rect x="40" y="110" width="290" height="40" fill="#4FA3E0"/><path d="M40,118 Q60,110 80,118 T120,118 T160,118 T200,118 T240,118 T280,118 T320,118" fill="none" stroke="#FFFFFF" stroke-width="4"/>'
    c += '<rect x="40" y="148" width="290" height="60" fill="#F3D9A4"/><path d="M120,170 L140,148 L160,170 Z M136,148 L136,136 L150,142 Z" fill="#E0B26A"/><path d="M200,168 L230,124" stroke="#E8304A" stroke-width="5"/><path d="M200,124 C220,108 250,110 262,124 Z" fill="#E8304A"/></g>'
    return bubble(c)


def milk_memory():
    c = '<rect x="150" y="70" width="56" height="90" rx="6" fill="#FFFFFF" stroke="#2E6FD9" stroke-width="5"/><path d="M150,92 L178,58 L206,92" fill="#7FB8E6" stroke="#2E6FD9" stroke-width="5"/>'
    c += f'<text x="178" y="130" font-size="20" fill="#2E6FD9" text-anchor="middle" {EN}>MILK</text>'
    return bubble(c)


def kite_memory():   # 回忆：小时候和爸爸放风筝
    c = '<path d="M210,50 L240,80 L210,120 L180,80 Z" fill="#E8304A"/><path d="M180,80 L240,80 M210,50 L210,120" stroke="#F2C230" stroke-width="3"/>'
    c += '<path d="M210,120 C200,140 170,140 150,160" fill="none" stroke="#5A4632" stroke-width="2"/>'
    c += '<circle cx="120" cy="120" r="10" fill="#F3C9A8"/><path d="M120,130 L120,160 M120,138 L104,150 M120,138 L136,128 M120,160 L112,176 M120,160 L128,176" stroke="#2E6FD9" stroke-width="5" stroke-linecap="round"/>'
    c += '<circle cx="150" cy="138" r="7" fill="#F3C9A8"/><path d="M150,145 L150,164 M150,150 L140,158 M150,150 L148,160 M150,164 L144,176 M150,164 L156,176" stroke="#E8304A" stroke-width="4" stroke-linecap="round"/>'
    return bubble(c)


def umbrella():   # 撑开的伞
    s = '<path d="M10,90 C20,30 70,6 110,6 C150,6 200,30 210,90 C190,76 170,76 152,90 C134,76 86,76 68,90 C50,76 30,76 10,90 Z" fill="#2E6FD9"/>'
    s += '<path d="M110,6 L110,90 M68,90 C80,50 96,20 110,6 M152,90 C140,50 124,20 110,6" fill="none" stroke="#1F4A99" stroke-width="3"/>'
    s += '<path d="M110,90 L110,190 C110,206 90,206 90,192" fill="none" stroke="#5A4632" stroke-width="7" stroke-linecap="round"/>'
    return svg(220, 210, s)


def phone_remind():   # 手机提醒：小铃铛、“奶奶生日 Grandma's birthday”
    s = '<rect x="0" y="0" width="260" height="480" rx="36" fill="#2B2D33"/><rect x="14" y="40" width="232" height="400" rx="8" fill="#DCE8F5"/>'
    s += '<rect x="104" y="16" width="52" height="9" rx="4" fill="#4A4F59"/><circle cx="130" cy="460" r="11" fill="#4A4F59"/>'
    s += '<rect x="26" y="140" width="208" height="130" rx="16" fill="#FFFFFF"/><path d="M60,166 C50,166 46,176 46,184 L42,192 L78,192 L74,184 C74,176 70,166 60,166 Z" fill="#F2C230"/>'
    s += f'<text x="90" y="188" font-size="18" fill="#5A6470" {CJK}>提醒 Reminder</text><text x="130" y="226" font-size="26" fill="#C0392B" text-anchor="middle" {CJK}>奶奶生日</text>'
    s += f'<text x="130" y="256" font-size="17" fill="#2B2D33" text-anchor="middle" {EN}>Grandma’s birthday</text>'
    return svg(260, 480, s)


def book():
    s = '<path d="M10,20 C60,6 100,14 120,26 L120,150 C100,138 60,132 10,144 Z" fill="#FFFFFF"/><path d="M230,20 C180,6 140,14 120,26 L120,150 C140,138 180,132 230,144 Z" fill="#FFFDF5"/>'
    for i in range(5):
        s += f'<path d="M26,{44 + i * 18} L104,{50 + i * 18} M136,{50 + i * 18} L214,{44 + i * 18}" stroke="#B8C0C9" stroke-width="4"/>'
    s += '<path d="M10,144 C60,132 100,138 120,150 C140,138 180,132 230,144 L230,156 C180,146 140,152 120,162 C100,152 60,146 10,156 Z" fill="#E8304A"/>'
    return svg(240, 170, s)


def icon_re():
    return svg(200, 200, '<path d="M150,70 A60,60 0 1 0 160,120" fill="none" stroke="#2E6FD9" stroke-width="18" stroke-linecap="round"/><path d="M128,40 L176,60 L140,96 Z" fill="#2E6FD9"/>')


def icon_mind():
    s = '<path d="M40,190 C40,130 60,70 110,70 C150,70 170,100 168,130 L180,150 L166,156 C166,176 150,182 130,180 L130,190 Z" fill="#F3C9A8"/>'
    s += '<circle cx="150" cy="40" r="28" fill="#FFFFFF" stroke="#7B57D6" stroke-width="5"/><circle cx="118" cy="62" r="7" fill="#FFFFFF" stroke="#7B57D6" stroke-width="4"/><circle cx="150" cy="40" r="10" fill="#F2C230"/>'
    return svg(200, 200, s)


write_art(ART, 'kitchen2-bg.svg', kitchen_bg(), bg=True); write_art(ART, 'fridge.svg', fridge())
write_art(ART, 'bubble-sea.svg', sea_memory()); write_art(ART, 'bubble-milk.svg', milk_memory()); write_art(ART, 'bubble-kite.svg', kite_memory())
write_art(ART, 'umbrella-open.svg', umbrella()); write_art(ART, 'phone-remind.svg', phone_remind()); write_art(ART, 'book-red.svg', book())
write_art(ART, 'icon-re.svg', icon_re()); write_art(ART, 'icon-mind.svg', icon_mind())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
HOLD = (20, 100, 120, 70, 'fist')
bk, ub, ph = book(), umbrella(), phone_remind()
photo = open(os.path.join(ART, 'photo.svg'), encoding='utf-8').read() if os.path.exists(os.path.join(ART, 'photo.svg')) else svg(100, 80, '<rect x="4" y="4" width="92" height="72" fill="#FFFFFF" stroke="#C9D6DE" stroke-width="4"/>')
M['west-girl-reread'] = frames_out(ART, 'west-girl-reread', [holding('west-girl', bk, 290, 262, 140, 99, left=HOLD, right=HOLD, mouth='open', eyes='down', top='#2E9E6A'),
                                                           holding('west-girl', bk, 290, 262, 140, 99, left=HOLD, right=HOLD, mouth='half', eyes='down', top='#2E9E6A', tilt=3)], fps=1.6, seq='pingpong')
M['cn-girl-recall'] = frames_out(ART, 'cn-girl-recall', [person('cn-girl', right='chin', mouth='smile', eyes='closed', look=1, top='#F2C230'),
                                                       person('cn-girl', right='chin', mouth='laugh', eyes='happy', look=1, top='#F2C230', tilt=3)], fps=0.8, seq='pingpong')
M['cn-boy-fridge'] = frames_out(ART, 'cn-boy-fridge', [person('cn-boy', right='point', mouth='o', eyes='wide', brows='up', look=1, top='#7FB8E6'),
                                                     person('cn-boy', right='pointup', mouth='laugh', eyes='happy', look=1, top='#7FB8E6', tilt=2)], fps=1.2, seq='pingpong')
M['cn-teacher-umbrella'] = frames_out(ART, 'cn-teacher-umbrella', [holding('cn-teacher', ub, 410, 210, 150, 143, right='present', mouth='open', brows='up', look=1, top='#F27A8A'),
                                                                 holding('cn-teacher', ub, 410, 210, 150, 143, right='present2', mouth='smile', look=1, top='#F27A8A', tilt=2)], fps=1.2, seq='pingpong')
M['cn-boy-oops'] = frames_out(ART, 'cn-boy-oops', [person('cn-boy', left='chin', mouth='o', eyes='wide', look=-1, top='#2E6FD9'),
                                                 person('cn-boy', left='thumb', mouth='laugh', eyes='happy', look=-1, top='#2E6FD9', tilt=-3)], fps=1.0, seq='pingpong')
M['west-girl-photo'] = frames_out(ART, 'west-girl-photo', [holding('west-girl', photo, 300, 250, 120, 100, left=HOLD, right=HOLD, mouth='smile', eyes='down', top='#F27A8A'),
                                                         holding('west-girl', photo, 300, 250, 120, 100, left=HOLD, right=HOLD, mouth='laugh', eyes='happy', top='#F27A8A', tilt=3)], fps=0.9, seq='pingpong')
M['west-boy-oh'] = frames_out(ART, 'west-boy-oh', [holding('west-boy', ph, 318, 214, 92, 170, left=HOLD, right=HOLD, mouth='o', eyes='wide', brows='up', top='#E8304A'),
                                                 holding('west-boy', ph, 318, 214, 92, 170, left=HOLD, right=HOLD, mouth='laugh', eyes='happy', top='#E8304A', tilt=2)], fps=1.1, seq='pingpong')
M['cn-boy-kite'] = frames_out(ART, 'cn-boy-kite', [person('cn-boy', right='pointup', mouth='smile', look=1, brows='up', top='#2E9E6A'),
                                                 person('cn-boy', right='chin', mouth='laugh', eyes='happy', look=1, top='#2E9E6A', tilt=2)], fps=0.9, seq='pingpong')
M['west-girl-remember'] = frames_out(ART, 'west-girl-remember', [person('west-girl', right='pointup', mouth='laugh', eyes='happy', top='#7B57D6'),
                                                               person('west-girl', right='thumb', mouth='smile', top='#7B57D6', tilt=2)], fps=1.2, seq='pingpong')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

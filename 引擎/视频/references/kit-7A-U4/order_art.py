import sys, os, math, random, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'
R = random.Random(26)
# 6.30（第七十四版）：26 order（先画图画书风，起草“都齐了”再转青绿工笔风）。要先跑 street、alarm 的画图脚本（街道、城墙夜景、喊话的哨兵）。
# 来历 ordo“一排”：织布机上一排排经线，梭子来回穿；顺序：书架上 1～5 号书从乱放到排好；秩序：车站排队上车；
# 命令：公园里教练吹哨下令开跑；订购、点菜：饭馆里女孩指着菜单点面条，外国服务员记在本子上


def loom(k):   # 织布机：一排经线，梭子（k 帧）左右穿过，织好的布卷在下面
    s = '<rect x="20" y="20" width="16" height="300" fill="#8B5A2B"/><rect x="384" y="20" width="16" height="300" fill="#8B5A2B"/>'
    s += '<rect x="20" y="20" width="380" height="18" rx="6" fill="#A86A32"/><rect x="20" y="240" width="380" height="22" rx="6" fill="#A86A32"/>'
    for i in range(24):
        x = 52 + i * 13.5
        s += f'<path d="M{x:.1f},38 L{x:.1f},240" stroke="{"#E8304A" if i % 6 == 0 else "#F6E7C1"}" stroke-width="3"/>'
    for j in range(5):
        y = 196 + j * 9
        s += f'<path d="M46,{y} L374,{y}" stroke="#2E6FD9" stroke-width="5"/>'
    s += '<rect x="44" y="120" width="332" height="10" rx="4" fill="#6B3E26"/>'
    x = [70, 200, 330][k]
    s += f'<path d="M{x-40},150 L{x+40},150 L{x+30},164 L{x-30},164 Z" fill="#C8913A"/><ellipse cx="{x}" cy="157" rx="12" ry="5" fill="#2E6FD9"/>'
    s += '<rect x="40" y="262" width="340" height="40" rx="18" fill="#2E6FD9"/><path d="M60,282 L360,282" stroke="#5B8EE6" stroke-width="4"/>'
    s += '<path d="M28,320 L8,350 M392,320 L412,350" stroke="#6B3E26" stroke-width="12" stroke-linecap="round"/>'
    return svg(420, 356, s)


def books(k):   # 书架一层：1～5 号书，k=0 乱放（3 1 5 2 4），k=1 排好（1 2 3 4 5）
    order = [3, 1, 5, 2, 4] if k == 0 else [1, 2, 3, 4, 5]
    cols = {1: '#E8304A', 2: '#F2C230', 3: '#2E9E6A', 4: '#2E6FD9', 5: '#7B57D6'}
    s = '<rect x="0" y="0" width="460" height="300" rx="8" fill="#8B5A2B"/><rect x="14" y="14" width="432" height="258" fill="#F3E2C2"/><rect x="0" y="272" width="460" height="28" fill="#6B3E26"/>'
    for i, n in enumerate(order):
        x = 40 + i * 80; h = 170 + n * 16; tilt = (0 if k else [-6, 4, -3, 7, -5][i])
        s += f'<g transform="rotate({tilt} {x+30} 272)"><rect x="{x}" y="{272-h}" width="60" height="{h}" rx="5" fill="{cols[n]}"/>'
        s += f'<rect x="{x+8}" y="{272-h+20}" width="44" height="10" fill="#FFFFFF" opacity="0.6"/><circle cx="{x+30}" cy="{272-h+70}" r="20" fill="#FFFFFF"/>'
        s += f'<text x="{x+30}" y="{272-h+79}" font-size="26" fill="{cols[n]}" text-anchor="middle" {EN}>{n}</text></g>'
    return svg(460, 300, s)


def diner_bg():   # 饭馆里：菜单板（牛肉面、饺子、汉堡、披萨）、出菜窗口里的厨师帽、红灯笼、木桌椅、绿植、窗外的街
    s = '<rect width="1200" height="700" fill="#F6E3C6"/><rect x="0" y="460" width="1200" height="240" fill="#B07A4E"/>'
    for i in range(0, 1200, 60):
        s += f'<path d="M{i},460 L{i-80},700" stroke="#9C6A42" stroke-width="3"/>'
    s += '<rect x="0" y="440" width="1200" height="22" fill="#8B5A2B"/>'
    s += '<rect x="60" y="60" width="300" height="250" fill="#BFE3F2" stroke="#8B5A2B" stroke-width="14"/><path d="M210,60 L210,310 M60,185 L360,185" stroke="#8B5A2B" stroke-width="8"/>'
    for x, h in ((80, 90), (130, 120), (250, 100), (300, 70)):
        s += f'<rect x="{x}" y="{310-h}" width="40" height="{h}" fill="#C9D6E3"/>'
    s += '<circle cx="170" cy="250" r="40" fill="#7CC160"/><rect x="164" y="280" width="12" height="30" fill="#8B5A2B"/>'
    s += '<rect x="440" y="50" width="420" height="300" rx="12" fill="#2F3B35" stroke="#8B5A2B" stroke-width="12"/>'
    s += f'<text x="650" y="100" font-size="34" fill="#F6E7C1" text-anchor="middle" {CJK}>菜单 MENU</text><path d="M480,116 L820,116" stroke="#F2C230" stroke-width="3"/>'
    for i, (zh, en, p) in enumerate((('牛肉面', 'Beef noodles', '¥18'), ('饺子', 'Dumplings', '¥15'), ('汉堡', 'Burger', '¥20'), ('披萨', 'Pizza', '¥30'))):
        y = 160 + i * 48
        s += f'<text x="480" y="{y}" font-size="26" fill="#FFFFFF" {CJK}>{zh}</text><text x="600" y="{y}" font-size="22" fill="#CFE8F5" {EN}>{en}</text><text x="830" y="{y}" font-size="24" fill="#F2C230" text-anchor="end" {EN}>{p}</text>'
    s += '<rect x="900" y="120" width="260" height="170" fill="#5A4632"/><rect x="914" y="134" width="232" height="142" fill="#F2F2F2"/>'
    s += '<path d="M990,214 C980,180 1010,170 1020,188 C1030,166 1064,176 1056,204 Z" fill="#FFFFFF" stroke="#C9D6DE" stroke-width="3"/><rect x="992" y="204" width="64" height="24" fill="#FFFFFF" stroke="#C9D6DE" stroke-width="3"/>'
    s += '<ellipse cx="1024" cy="262" rx="80" ry="12" fill="#B8C0C9"/><path d="M930,276 L1130,276" stroke="#8B5A2B" stroke-width="10"/>'
    for x in (400, 880):
        s += f'<path d="M{x},0 L{x},30" stroke="#1B1A1F" stroke-width="3"/><ellipse cx="{x}" cy="56" rx="24" ry="28" fill="#E8304A"/><rect x="{x-12}" y="26" width="24" height="6" fill="#F2C230"/><path d="M{x},84 L{x},104" stroke="#F2C230" stroke-width="4"/>'
    for x in (160, 1040):
        s += f'<ellipse cx="{x}" cy="520" rx="130" ry="26" fill="#8B5A2B"/><rect x="{x-10}" y="520" width="20" height="120" fill="#6B3E26"/><ellipse cx="{x}" cy="640" rx="60" ry="10" fill="#6B3E26"/>'
        s += f'<rect x="{x-70}" y="490" width="34" height="22" rx="4" fill="#FFFFFF"/><rect x="{x+30}" y="494" width="44" height="18" rx="9" fill="#FFFFFF"/><path d="M{x+10},470 L{x+16},500 M{x+22},470 L{x+20},500" stroke="#C8913A" stroke-width="3"/>'
        for dx in (-160, 130):
            s += f'<rect x="{x+dx}" y="470" width="40" height="90" rx="6" fill="#A86A32"/><rect x="{x+dx-6}" y="550" width="52" height="14" rx="4" fill="#8B5A2B"/><path d="M{x+dx+4},564 L{x+dx+4},640 M{x+dx+36},564 L{x+dx+36},640" stroke="#6B3E26" stroke-width="7"/>'
    for i in range(0, 1200, 40):      # 墙裙：一排竖木板
        s += f'<rect x="{i+2}" y="380" width="36" height="60" fill="#D9B48A"/>'
    for i, t in enumerate(('牛肉面', '小笼包', '豆浆', '油条', '炒饭', '馄饨', '春卷', '奶茶')):     # 墙上挂的一排红菜牌
        x = 380 + i * 62
        s += f'<rect x="{x}" y="360" width="46" height="70" rx="4" fill="#C0392B"/><text x="{x+23}" y="{380 + (0 if len(t) < 3 else 0)}" font-size="13" fill="#F6E7C1" text-anchor="middle" {CJK}>{t}</text>'
    for x in (250, 640, 1000):      # 吊灯
        s += f'<path d="M{x},0 L{x},24" stroke="#5A4632" stroke-width="3"/><path d="M{x-30},44 L{x+30},44 L{x+18},24 L{x-18},24 Z" fill="#F2C230"/><circle cx="{x}" cy="50" r="9" fill="#FFF3B0"/>'
    s += '<rect x="20" y="330" width="200" height="12" fill="#8B5A2B"/>'      # 搁板上的瓶瓶罐罐
    for i in range(9):
        c = R.choice(['#E8304A', '#2E9E6A', '#F2C230', '#7FB8E6', '#C8913A'])
        s += f'<rect x="{28+i*21}" y="{300 - (i % 3) * 8}" width="15" height="{30 + (i % 3) * 8}" rx="4" fill="{c}"/>'
    s += '<rect x="560" y="400" width="200" height="60" rx="6" fill="#8B5A2B"/><rect x="640" y="372" width="70" height="34" rx="5" fill="#47525C"/><rect x="650" y="378" width="50" height="14" fill="#9ADBA0"/>'
    for x in (140, 200, 1020, 1080):      # 碗里冒热气
        s += f'<path d="M{x},466 C{x-8},450 {x+8},440 {x},424" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.8"/>'
    s += '<path d="M1170,440 L1180,380 L1200,380 L1200,440 Z" fill="#B8613A"/><circle cx="1188" cy="350" r="36" fill="#4E9A3E"/>'
    return svg(1200, 700, s)


def notepad():
    s = '<rect x="10" y="10" width="110" height="140" rx="6" fill="#FFFDF5" stroke="#C9D6DE" stroke-width="3"/><rect x="10" y="10" width="110" height="18" fill="#E8304A"/>'
    for y in (50, 72, 94, 116):
        s += f'<path d="M24,{y} L106,{y}" stroke="#B8C0C9" stroke-width="3"/>'
    s += '<path d="M26,46 Q40,36 54,46 T84,46" fill="none" stroke="#1A66B8" stroke-width="4"/>'
    return svg(130, 160, s)


def whistle():
    s = '<path d="M20,40 L90,40 C110,40 120,56 120,70 C120,92 100,104 82,100 L20,64 Z" fill="#C0C7CF" stroke="#7A8590" stroke-width="4"/><circle cx="92" cy="70" r="14" fill="#7A8590"/>'
    s += '<path d="M20,40 C0,20 10,0 40,6" fill="none" stroke="#E8304A" stroke-width="5"/>'
    return svg(130, 110, s)


write_art(ART, 'loom_f0.svg', loom(0)); write_art(ART, 'loom_f1.svg', loom(1)); write_art(ART, 'loom_f2.svg', loom(2))
write_art(ART, 'books_f0.svg', books(0)); write_art(ART, 'books_f1.svg', books(1))
write_art(ART, 'diner-bg.svg', diner_bg(), bg=True); write_art(ART, 'notepad.svg', notepad()); write_art(ART, 'whistle.svg', whistle())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
HOLD = (20, 100, 120, 70, 'fist')
wh, npd = whistle(), notepad()
M['cn-girl-weave'] = frames_out(ART, 'cn-girl-weave', [person('cn-girl', left=HOLD, right=HOLD, eyes='down', mouth='smile', top='#2E9E6A'),
                                                     person('cn-girl', left=HOLD, right=HOLD, eyes='down', mouth='smile', top='#2E9E6A', tilt=4)], fps=1.5, seq='pingpong')
M['west-girl-books'] = frames_out(ART, 'west-girl-books', [person('west-girl', right='point', look=1, mouth='open', brows='up', top='#F27A8A'),
                                                         person('west-girl', right='thumb', look=1, mouth='laugh', eyes='happy', top='#F27A8A', tilt=2)], fps=1.2, seq='pingpong')
M['west-man-coach'] = frames_out(ART, 'west-man-coach', [holding('west-man', wh, 400, 168, 60, 50, right='raise', mouth='o', eyes='wide', brows='up', look=1, top='#E8304A'),
                                                       person('west-man', right='point', mouth='open', brows='up', look=1, top='#E8304A', tilt=3)], fps=1.4, seq='pingpong')
M['west-man-waiter'] = frames_out(ART, 'west-man-waiter', [holding('west-man', npd, 300, 250, 90, 110, left=HOLD, right=HOLD, mouth='smile', eyes='down', look=-1, top='#FFFFFF', collar='#2F3B35'),
                                                         holding('west-man', npd, 300, 250, 90, 110, left=HOLD, right=HOLD, mouth='open', brows='up', look=-1, top='#FFFFFF', collar='#2F3B35', tilt=-2)], fps=1.1, seq='pingpong')
M['cn-girl-order'] = frames_out(ART, 'cn-girl-order', [person('cn-girl', right='pointup', look=1, mouth='open', brows='up', top='#F2C230'),
                                                     person('cn-girl', right='point', look=1, mouth='laugh', eyes='happy', top='#F2C230', tilt=2)], fps=1.3, seq='pingpong')
M['west-man-coach2'] = frames_out(ART, 'west-man-coach2', [person('west-man', left='raise', right='raise', mouth='laugh', eyes='happy', top='#E8304A'),
                                                         person('west-man', left='hello', right='raise', mouth='open', brows='up', top='#E8304A', tilt=-3)], fps=1.6, seq='pingpong')
M['cn-girl-menu'] = frames_out(ART, 'cn-girl-menu', [person('cn-girl', right='chin', look=1, eyes='down', mouth='flat', top='#F2C230'),
                                                   person('cn-girl', right='chin', look=1, mouth='o', eyes='wide', brows='up', top='#F2C230', tilt=2)], fps=1.0, seq='pingpong')
M['west-man-write'] = frames_out(ART, 'west-man-write', [holding('west-man', npd, 300, 250, 90, 110, left=HOLD, right=HOLD, mouth='flat', eyes='down', top='#FFFFFF', collar='#2F3B35'),
                                                       holding('west-man', npd, 300, 250, 90, 110, left=HOLD, right=HOLD, mouth='smile', eyes='happy', look=-1, top='#FFFFFF', collar='#2F3B35', tilt=2)], fps=0.9, seq='pingpong')
M['cn-boy-queue'] = frames_out(ART, 'cn-boy-queue', [person('cn-boy', mouth='smile', look=1, top='#2E6FD9'), person('cn-boy', mouth='smile', look=1, top='#2E6FD9', tilt=2)], fps=0.8, seq='pingpong')
M['west-woman-queue'] = frames_out(ART, 'west-woman-queue', [person('west-woman', mouth='smile', look=1), person('west-woman', mouth='half', look=1, tilt=-2)], fps=0.7, seq='pingpong')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

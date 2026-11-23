import sys, os, math, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'
# 6.30（第七十四版）：24 schedule（图画书风）。场景用 references/scenes 里的 room-bg、station-bg、classroom-bg、park-bg，不用先跑别的画图脚本。
# sched 一条纸：写了字的小纸条；-ule 小：大箱子 → 小胶囊（capsule）；附表、价目表：文件后面别着价目表；
# 时刻表：老式铁路时刻表 + 冒烟的火车；车站电子屏一行行翻；日程表：一周的计划板一格格贴满；安排：挂历上星期五画红圈、贴“家长会”


def strip():   # 一小条写了字的纸（毛边、羊皮纸色）
    s = '<polygon points="8,20 60,12 120,18 200,10 290,16 370,8 412,18 406,60 412,104 340,110 260,104 180,112 100,104 30,110 8,100 14,60" fill="#F3E2B8"/>'
    for y in (40, 62, 84):
        d = 'M34,%d ' % y + ' '.join('Q%d,%d %d,%d' % (34 + 20 * i + 10, y - 6 if i % 2 else y + 6, 34 + 20 * (i + 1), y) for i in range(16 if y < 80 else 10))
        s += f'<path d="{d}" fill="none" stroke="#5A4632" stroke-width="3"/>'
    s += '<circle cx="372" cy="80" r="16" fill="#C0392B"/><circle cx="372" cy="80" r="8" fill="#E25B4B"/>'
    return svg(420, 120, s)


def capsule():
    s = '<rect x="10" y="14" width="140" height="52" rx="26" fill="#FFFFFF"/><path d="M80,14 L54,14 C40,14 10,26 10,40 C10,54 40,66 54,66 L80,66 Z" fill="#E8304A"/>'
    s += '<path d="M30,30 C34,24 44,22 52,22" fill="none" stroke="#FFB3BC" stroke-width="5" stroke-linecap="round"/>'
    return svg(160, 80, s)


def bigbox():
    s = '<polygon points="20,60 110,30 200,60 110,90" fill="#E0A65A"/><polygon points="20,60 110,90 110,184 20,154" fill="#C8913A"/><polygon points="110,90 200,60 200,154 110,184" fill="#B07A2E"/>'
    s += '<path d="M65,45 L155,75 L155,110" fill="none" stroke="#F2D9A6" stroke-width="10"/>'
    return svg(220, 190, s)


def arrow():
    return svg(160, 80, '<path d="M10,40 L120,40" stroke="#2B8A3E" stroke-width="14" stroke-linecap="round"/><path d="M104,12 L150,40 L104,68 Z" fill="#2B8A3E"/>')


def pricelist():   # 文件后面别着一张价目表（回形针）
    s = '<rect x="60" y="10" width="230" height="300" rx="8" fill="#E6EEF5"/>'
    for y in range(50, 290, 26):
        s += f'<path d="M84,{y} L266,{y}" stroke="#B8C4D0" stroke-width="5"/>'
    s += '<rect x="20" y="70" width="240" height="300" rx="8" fill="#FFFDF5"/>'
    s += f'<text x="140" y="116" font-size="28" fill="#C0392B" text-anchor="middle" {CJK}>价目表</text><text x="140" y="146" font-size="20" fill="#5A4632" text-anchor="middle" {EN}>Price List</text>'
    rows = [('苹果', 'Apples', '¥6'), ('牛奶', 'Milk', '¥5'), ('面包', 'Bread', '¥8'), ('鸡蛋', 'Eggs', '¥10')]
    for i, (zh, en, pr) in enumerate(rows):
        y = 194 + i * 42
        s += f'<text x="40" y="{y}" font-size="20" fill="#2B2D33" {CJK}>{zh}</text><text x="92" y="{y}" font-size="18" fill="#5A6470" {EN}>{en}</text><text x="238" y="{y}" font-size="20" fill="#1A66B8" text-anchor="end" {EN}>{pr}</text>'
        s += f'<path d="M40,{y+12} L238,{y+12}" stroke="#E2D6BC" stroke-width="2"/>'
    s += '<path d="M222,52 L222,110 C222,124 244,124 244,110 L244,60 C244,50 232,50 232,60 L232,104" fill="none" stroke="#8A96A3" stroke-width="5"/>'
    return svg(310, 380, s)


def railsheet():   # 老式铁路时刻表（印出来的一张纸）
    s = '<rect x="10" y="10" width="300" height="380" rx="6" fill="#F1E2C2"/><rect x="24" y="24" width="272" height="352" fill="none" stroke="#6B4E2E" stroke-width="3"/>'
    s += f'<text x="160" y="66" font-size="24" fill="#3A2A1A" text-anchor="middle" {EN}>RAILWAY</text><text x="160" y="96" font-size="20" fill="#3A2A1A" text-anchor="middle" {EN}>TIME TABLE</text>'
    s += '<path d="M40,110 L280,110 M40,114 L280,114" stroke="#6B4E2E" stroke-width="2"/>'
    rows = [('London', '8.15'), ('Reading', '9.02'), ('Oxford', '9.40'), ('Bath', '11.05'), ('Bristol', '11.30')]
    for i, (st, t) in enumerate(rows):
        y = 150 + i * 44
        s += f'<text x="44" y="{y}" font-size="20" fill="#3A2A1A" {EN}>{st}</text><text x="276" y="{y}" font-size="20" fill="#3A2A1A" text-anchor="end" {EN}>{t}</text>'
        s += f'<path d="M130,{y-6} L226,{y-6}" stroke="#A88B62" stroke-width="2" stroke-dasharray="4 6"/>'
    return svg(320, 400, s)


def steamtrain():   # 冒烟的老火车（车头朝左）
    s = '<rect x="150" y="40" width="110" height="100" rx="8" fill="#2F3B35"/><rect x="166" y="56" width="40" height="34" rx="4" fill="#F2C230"/>'
    s += '<rect x="20" y="80" width="160" height="62" rx="20" fill="#1B1A1F"/><rect x="50" y="34" width="26" height="50" fill="#1B1A1F"/><rect x="42" y="26" width="42" height="14" rx="4" fill="#3A3A3A"/>'
    s += '<rect x="270" y="72" width="140" height="70" rx="8" fill="#B71C1C"/><rect x="286" y="86" width="30" height="24" fill="#F6E7C1"/><rect x="330" y="86" width="30" height="24" fill="#F6E7C1"/><rect x="372" y="86" width="26" height="24" fill="#F6E7C1"/>'
    for x, r in ((60, 26), (120, 26), (220, 30), (300, 20), (380, 20)):
        s += f'<circle cx="{x}" cy="{170-r}" r="{r}" fill="#C0392B"/><circle cx="{x}" cy="{170-r}" r="{r*0.35:.0f}" fill="#1B1A1F"/>'
    s += '<path d="M10,120 L22,140 L4,140 Z" fill="#9AA3AE"/><path d="M60,144 L220,144" stroke="#9AA3AE" stroke-width="6"/>'
    return svg(420, 176, s)


def puff():
    return svg(120, 90, '<circle cx="40" cy="50" r="30" fill="#E6E9ED"/><circle cx="72" cy="40" r="34" fill="#F2F4F6"/><circle cx="90" cy="60" r="24" fill="#DDE1E6"/>')


def board(k):   # 车站电子屏：车次、开往、时间，一行行往上翻
    rows = [('G102', '上海 Shanghai', '09:15'), ('D305', '北京 Beijing', '10:40'), ('G88', '香港 Hong Kong', '11:20'),
            ('K18', '西安 Xi’an', '12:05'), ('G7', '杭州 Hangzhou', '13:30')]
    s = '<rect x="0" y="0" width="560" height="300" rx="14" fill="#2B2D33"/><rect x="14" y="14" width="532" height="272" rx="8" fill="#101418"/>'
    s += f'<text x="40" y="52" font-size="22" fill="#9ADBA0" {CJK}>车次</text><text x="160" y="52" font-size="22" fill="#9ADBA0" {CJK}>开往 To</text><text x="520" y="52" font-size="22" fill="#9ADBA0" text-anchor="end" {CJK}>时间</text>'
    s += '<path d="M30,66 L530,66" stroke="#3A4450" stroke-width="3"/>'
    for i in range(4):
        tr, to, t = rows[(i + k) % len(rows)]
        y = 106 + i * 50
        c = '#FFD54A' if i == 0 else '#F5A623'
        s += f'<text x="40" y="{y}" font-size="26" fill="{c}" {EN}>{tr}</text><text x="160" y="{y}" font-size="24" fill="{c}" {CJK}>{to}</text><text x="520" y="{y}" font-size="26" fill="{c}" text-anchor="end" {EN}>{t}</text>'
    return svg(560, 300, s)


def planner(k):   # 一周的计划板：一格格贴上要做的事（k = 0～3）
    days = '一二三四五六日'
    s = '<rect x="0" y="0" width="500" height="350" rx="14" fill="#8B5A2B"/><rect x="14" y="14" width="472" height="322" rx="8" fill="#FFFFFF"/>'
    s += f'<text x="250" y="52" font-size="28" fill="#1A66B8" text-anchor="middle" {CJK}>日程表 Schedule</text>'
    for i, d in enumerate(days):
        x = 34 + i * 63
        s += f'<rect x="{x}" y="70" width="56" height="32" rx="6" fill="#E8F1FB"/><text x="{x+28}" y="94" font-size="20" fill="#1A66B8" text-anchor="middle" {CJK}>{d}</text>'
        for j in range(3):
            s += f'<rect x="{x}" y="{110+j*72}" width="56" height="64" rx="6" fill="none" stroke="#DDE3EA" stroke-width="2"/>'
    notes = [(0, 0, '#F27A8A', '钢琴'), (2, 1, '#7CC160', '足球'), (4, 0, '#F2C230', 'Math'), (1, 2, '#7FB8E6', '游泳'), (3, 1, '#C9A0F0', '英语'),
             (5, 0, '#FFB067', '奶奶'), (6, 2, '#7CC160', '跑步'), (0, 1, '#F2C230', 'Art'), (2, 2, '#F27A8A', '画画')]
    for (i, j, c, t) in notes[:k * 3]:
        x = 34 + i * 63; y = 110 + j * 72
        s += f'<rect x="{x+3}" y="{y+3}" width="50" height="58" rx="6" fill="{c}"/><text x="{x+28}" y="{y+38}" font-size="16" fill="#2B2D33" text-anchor="middle" {CJK if not t.isascii() else EN}>{t}</text>'
    return svg(500, 350, s)


def calendar(k):   # 挂历：十一月；k = 1 时星期五（20 号）画红圈、贴“家长会 Meeting”
    s = '<rect x="0" y="0" width="380" height="400" rx="12" fill="#FFFFFF"/><rect x="0" y="0" width="380" height="78" rx="12" fill="#E8304A"/>'
    s += f'<text x="190" y="52" font-size="30" fill="#FFFFFF" text-anchor="middle" {CJK}>十一月 November</text>'
    for i, d in enumerate('一二三四五六日'):
        s += f'<text x="{34+i*52}" y="110" font-size="18" fill="#5A6470" text-anchor="middle" {CJK}>{d}</text>'
    for n in range(1, 31):
        i = (n + 5) % 7; j = (n + 5) // 7
        x = 34 + i * 52; y = 150 + j * 48
        s += f'<text x="{x}" y="{y}" font-size="22" fill="{"#E8304A" if i >= 5 else "#2B2D33"}" text-anchor="middle" {EN}>{n}</text>'
        if k == 1 and n == 20:
            s += f'<ellipse cx="{x}" cy="{y-8}" rx="24" ry="20" fill="none" stroke="#E8304A" stroke-width="5"/>'
    if k == 1:
        s += '<g transform="rotate(-6 300 330)"><rect x="236" y="290" width="130" height="76" rx="6" fill="#FFE97A"/>'
        s += f'<text x="301" y="322" font-size="22" fill="#2B2D33" text-anchor="middle" {CJK}>家长会</text><text x="301" y="350" font-size="18" fill="#5A6470" text-anchor="middle" {EN}>Meeting</text></g>'
    return svg(380, 400, s)


def plan_bubble():   # 想法泡泡：长城、远山（心里的打算）
    s = '<circle cx="40" cy="200" r="10" fill="#FFFFFF"/><circle cx="66" cy="176" r="16" fill="#FFFFFF"/>'
    s += '<path d="M90,150 C50,150 50,90 90,84 C90,40 150,30 170,56 C190,20 260,30 260,74 C300,80 300,140 260,146 C250,176 190,176 176,156 C150,180 100,176 90,150 Z" fill="#FFFFFF"/>'
    s += '<polygon points="96,136 140,86 172,126 206,80 254,136" fill="#9DC59A"/>'
    s += '<path d="M96,132 L130,116 L170,124 L210,108 L254,124" fill="none" stroke="#C8913A" stroke-width="9"/>'
    for x in (112, 150, 190, 228):
        s += f'<rect x="{x}" y="{100 + (12 if x in (150, 228) else 0)}" width="14" height="14" fill="#B07A2E"/>'
    s += f'<text x="176" y="72" font-size="18" fill="#C0392B" text-anchor="middle" {CJK}>长城</text>'
    return svg(300, 220, s)


def icon_sched():
    return svg(200, 200, nest(strip(), 6, 64, 188, 54))


def icon_ule():
    return svg(200, 200, nest(capsule(), 30, 70, 140, 70))


write_art(ART, 'strip.svg', strip()); write_art(ART, 'capsule.svg', capsule()); write_art(ART, 'bigbox.svg', bigbox()); write_art(ART, 'arrow-r.svg', arrow())
write_art(ART, 'pricelist.svg', pricelist()); write_art(ART, 'railsheet.svg', railsheet()); write_art(ART, 'steamtrain.svg', steamtrain()); write_art(ART, 'puff.svg', puff(), style=False)
for k in range(3):
    write_art(ART, f'deps_f{k}.svg', board(k))
for k in range(4):
    write_art(ART, f'planner_f{k}.svg', planner(k))
write_art(ART, 'cal_f0.svg', calendar(0)); write_art(ART, 'cal_f1.svg', calendar(1)); write_art(ART, 'plan-bubble.svg', plan_bubble())
write_art(ART, 'icon-sched.svg', icon_sched()); write_art(ART, 'icon-ule.svg', icon_ule())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
M['west-girl-plan'] = frames_out(ART, 'west-girl-plan', [person('west-girl', right='point', look=1, mouth='open', brows='up', top='#F2C230'),
                                                       person('west-girl', right='present', look=1, mouth='laugh', eyes='happy', top='#F2C230', tilt=2)], fps=1.2, seq='pingpong')
M['west-man-time'] = frames_out(ART, 'west-man-time', [person('west-man', right='pointup', look=1, mouth='open', brows='up'),
                                                     person('west-man', right='point', look=1, mouth='half', tilt=2)], fps=1.2, seq='pingpong')
M['cn-teacher-sched'] = frames_out(ART, 'cn-teacher-sched', [person('cn-teacher', right='point', look=1, mouth='open', brows='up', top='#7B57D6'),
                                                           person('cn-teacher', right='thumb', look=1, mouth='laugh', eyes='happy', top='#7B57D6')], fps=1.2, seq='pingpong')
M['cn-boy-dream'] = frames_out(ART, 'cn-boy-dream', [person('cn-boy', right='chin', mouth='smile', look=-1, brows='up'),
                                                   person('cn-boy', right='chin', mouth='o', eyes='wide', look=-1, tilt=-3)], fps=1.0, seq='pingpong')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

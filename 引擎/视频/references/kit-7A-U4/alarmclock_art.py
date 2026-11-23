import sys, os, math, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'
# 6.30（第七十四版）：22 alarm clock（图画书风）。要先跑 alarm_art.py（卧室、床、床头柜、会抖的闹钟、火警铃）。
# alarm 警报：教室里火警铃响，学生排队往外走；clock 钟：客厅墙上带摆的挂钟；闹钟：女孩在床上伸懒腰；set the alarm：女孩在手机上定闹钟


def wallclock(k):   # 带摆的挂钟（西式木壳）：两帧，钟摆左右摆
    s = '<path d="M52,44 L110,4 L168,44 Z" fill="#6B3E26"/><circle cx="110" cy="22" r="7" fill="#F2C230"/>'
    s += '<rect x="40" y="40" width="140" height="340" rx="14" fill="#8B5A2B"/><rect x="54" y="206" width="112" height="160" rx="8" fill="#F6E7C1"/>'
    s += '<circle cx="110" cy="122" r="72" fill="#5A3A1E"/><circle cx="110" cy="122" r="62" fill="#FFFDF5"/>'
    for i in range(12):
        a = math.pi * 2 * i / 12
        w = 6 if i % 3 == 0 else 3
        s += f'<path d="M{110+54*math.sin(a):.0f},{122-54*math.cos(a):.0f} L{110+44*math.sin(a):.0f},{122-44*math.cos(a):.0f}" stroke="#1B1A1F" stroke-width="{w}"/>'
    s += '<path d="M110,122 L84,138 M110,122 L110,74" stroke="#1B1A1F" stroke-width="7" stroke-linecap="round"/><circle cx="110" cy="122" r="7" fill="#C0392B"/>'
    a = math.radians(-13 if k == 0 else 13)
    bx, by = 110 + 118 * math.sin(a), 212 + 118 * math.cos(a)
    s += f'<path d="M110,212 L{bx:.0f},{by:.0f}" stroke="#C99A1E" stroke-width="5"/><circle cx="{bx:.0f}" cy="{by:.0f}" r="20" fill="#F2C230"/><circle cx="{bx-6:.0f}" cy="{by-6:.0f}" r="6" fill="#FFF3B0"/>'
    s += '<path d="M66,226 L96,256 M66,256 L80,270" stroke="#FFFFFF" stroke-width="6" opacity="0.7"/>'
    s += '<rect x="34" y="372" width="152" height="16" rx="6" fill="#6B3E26"/>'
    return svg(220, 392, s)


def phone_alarm():   # 手机上的闹钟：6:30、起床 Wake up、开关打开、小铃铛、周一到周五
    s = '<rect x="0" y="0" width="260" height="480" rx="36" fill="#2B2D33"/><rect x="14" y="40" width="232" height="400" rx="8" fill="#1F2A44"/>'
    s += '<rect x="104" y="16" width="52" height="9" rx="4" fill="#4A4F59"/><circle cx="130" cy="460" r="11" fill="#4A4F59"/>'
    s += '<path d="M130,74 C112,74 106,90 106,104 L100,118 L160,118 L154,104 C154,90 148,74 130,74 Z" fill="#F2C230"/><circle cx="130" cy="124" r="7" fill="#F2C230"/>'
    s += f'<text x="130" y="200" font-size="66" fill="#FFFFFF" text-anchor="middle" {EN}>6:30</text>'
    s += f'<text x="130" y="244" font-size="22" fill="#B8C4DD" text-anchor="middle" {CJK}>起床 Wake up</text>'
    s += '<rect x="90" y="272" width="80" height="40" rx="20" fill="#34C759"/><circle cx="150" cy="292" r="16" fill="#FFFFFF"/>'
    for i, c in enumerate('MTWTF'):
        s += f'<circle cx="{58+i*36}" cy="356" r="14" fill="#2E6FD9"/><text x="{58+i*36}" y="362" font-size="15" fill="#FFFFFF" text-anchor="middle" {EN}>{c}</text>'
    for i, c in enumerate('SS'):
        s += f'<circle cx="{94+i*72}" cy="396" r="12" fill="#3A4560"/><text x="{94+i*72}" y="401" font-size="13" fill="#8A96B0" text-anchor="middle" {EN}>{c}</text>'
    return svg(260, 480, s)


def icon_alarm():   # 火警铃 + 往外的声波
    s = '<rect x="86" y="30" width="28" height="20" rx="4" fill="#B71C1C"/><circle cx="100" cy="100" r="52" fill="#E8304A"/><circle cx="100" cy="100" r="34" fill="#FF5A5A"/><circle cx="100" cy="100" r="10" fill="#5A1F1F"/>'
    for r in (66, 84):
        s += f'<path d="M{100+r*0.71:.0f},{100-r*0.71:.0f} A{r},{r} 0 0 1 {100+r*0.71:.0f},{100+r*0.71:.0f}" fill="none" stroke="#F59E0B" stroke-width="7" stroke-linecap="round"/>'
        s += f'<path d="M{100-r*0.71:.0f},{100-r*0.71:.0f} A{r},{r} 0 0 0 {100-r*0.71:.0f},{100+r*0.71:.0f}" fill="none" stroke="#F59E0B" stroke-width="7" stroke-linecap="round"/>'
    return svg(200, 200, s)


def icon_clock():
    s = '<circle cx="100" cy="100" r="80" fill="#8B5A2B"/><circle cx="100" cy="100" r="66" fill="#FFFDF5"/>'
    for i in range(12):
        a = math.pi * 2 * i / 12
        s += f'<path d="M{100+58*math.sin(a):.0f},{100-58*math.cos(a):.0f} L{100+48*math.sin(a):.0f},{100-48*math.cos(a):.0f}" stroke="#1B1A1F" stroke-width="{6 if i % 3 == 0 else 3}"/>'
    s += '<path d="M100,100 L100,52 M100,100 L132,116" stroke="#1B1A1F" stroke-width="8" stroke-linecap="round"/><circle cx="100" cy="100" r="7" fill="#C0392B"/>'
    return svg(200, 200, s)


write_art(ART, 'wallclock_f0.svg', wallclock(0)); write_art(ART, 'wallclock_f1.svg', wallclock(1))
write_art(ART, 'phone-alarm.svg', phone_alarm()); write_art(ART, 'icon-alarm.svg', icon_alarm()); write_art(ART, 'icon-clock.svg', icon_clock())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
M['cn-girl-wake'] = frames_out(ART, 'cn-girl-wake', [person('cn-girl', left='raise', right='raise', mouth='o', eyes='closed', brows='frown', top='#F27A8A'),
                                                   person('cn-girl', left=(20, 112, 170, 104, 'open'), right=(20, 112, 170, 104, 'open'), mouth='laugh', eyes='closed', top='#F27A8A', tilt=-4)], fps=1.5, seq='pingpong')
M['west-boy-up'] = frames_out(ART, 'west-boy-up', [person('west-boy', left='pointup', mouth='o', eyes='wide', brows='up', top='#7FB8E6'),
                                                 person('west-boy', left='raise', mouth='laugh', eyes='happy', top='#7FB8E6', tilt=3)], fps=1.4, seq='pingpong')
ph = phone_alarm()
M['west-girl-set'] = frames_out(ART, 'west-girl-set', [holding('west-girl', ph, 318, 214, 92, 170, left=(20, 100, 120, 70, 'fist'), right=(20, 100, 120, 70, 'fist'), mouth='smile', eyes='down'),
                                                     holding('west-girl', ph, 318, 214, 92, 170, left=(20, 100, 120, 70, 'fist'), right=(20, 100, 120, 70, 'fist'), mouth='laugh', eyes='happy', tilt=2)], fps=1.2, seq='pingpong')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

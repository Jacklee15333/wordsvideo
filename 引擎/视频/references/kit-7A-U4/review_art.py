import sys, os, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'


def soldiers():   # 一排站得笔直的士兵（正面）：军帽、军装、白手套
    s = ''
    for i in range(5):
        x = 50 + i * 100
        s += f'<rect x="{x-22}" y="150" width="18" height="110" fill="#2F4A2F"/><rect x="{x+4}" y="150" width="18" height="110" fill="#2F4A2F"/>'
        s += f'<rect x="{x-24}" y="252" width="22" height="10" fill="#1B1A1F"/><rect x="{x+2}" y="252" width="22" height="10" fill="#1B1A1F"/>'
        s += f'<path d="M{x-34},70 L{x+34},70 L{x+30},160 L{x-30},160 Z" fill="#3B5E3A"/><rect x="{x-34}" y="120" width="68" height="8" fill="#C9A24A"/>'
        s += f'<rect x="{x-46}" y="74" width="12" height="70" rx="6" fill="#3B5E3A"/><rect x="{x+34}" y="74" width="12" height="70" rx="6" fill="#3B5E3A"/>'
        s += f'<circle cx="{x-40}" cy="148" r="8" fill="#FFFFFF"/><circle cx="{x+40}" cy="148" r="8" fill="#FFFFFF"/>'
        s += f'<rect x="{x-7}" y="54" width="14" height="18" fill="#F3D2BE"/><circle cx="{x}" cy="40" r="20" fill="#F3D2BE"/>'
        s += f'<path d="M{x-24},26 L{x+24},26 L{x+20},10 L{x-20},10 Z" fill="#2F4A2F"/><rect x="{x-26}" y="24" width="52" height="6" fill="#1B1A1F"/><circle cx="{x}" cy="17" r="4" fill="#E8304A"/>'
        s += f'<circle cx="{x-7}" cy="40" r="2.5" fill="#1B1A1F"/><circle cx="{x+7}" cy="40" r="2.5" fill="#1B1A1F"/><path d="M{x-5},50 L{x+5},50" stroke="#C0392B" stroke-width="2"/>'
    return svg(500, 270, s)


def calendar(k):   # 挂历：一页页翻过去（一月、四月、八月、十二月）
    m = (('1 月', 'JAN'), ('4 月', 'APR'), ('8 月', 'AUG'), ('12 月', 'DEC'))[k]
    s = '<rect x="10" y="20" width="220" height="250" rx="8" fill="#FFFFFF"/><rect x="10" y="20" width="220" height="62" rx="8" fill="#E8304A"/>'
    s += ''.join(f'<circle cx="{x}" cy="20" r="8" fill="#5A6170"/>' for x in (60, 120, 180))
    s += f'<text x="120" y="66" font-size="30" fill="#FFFFFF" text-anchor="middle" {CJK}>{m[0]} {m[1]}</text>'
    for r in range(5):
        for c in range(7):
            n = r * 7 + c + 1
            if n <= 31:
                s += f'<text x="{30+c*30}" y="{112+r*34}" font-size="16" fill="{"#E8304A" if c in (0, 6) else "#3A3F4B"}" text-anchor="middle" {EN}>{n}</text>'
    s += f'<rect x="{18+(k*2)%7*30}" y="{96+(k%4)*34}" width="26" height="24" rx="5" fill="none" stroke="#2E6FD9" stroke-width="3"/>'
    return svg(240, 280, s)


def book_new():   # 一本新书（封面：大树、书名）
    s = '<rect x="20" y="0" width="200" height="270" rx="6" fill="#2E7D32"/><rect x="20" y="0" width="22" height="270" fill="#1F5E22"/>'
    s += f'<text x="128" y="52" font-size="26" fill="#FFFFFF" text-anchor="middle" {EN}>The Old</text><text x="128" y="84" font-size="26" fill="#FFFFFF" text-anchor="middle" {EN}>Tree</text>'
    s += '<rect x="118" y="160" width="20" height="70" fill="#8A5A3B"/><circle cx="128" cy="140" r="46" fill="#6DBE45"/><circle cx="96" cy="160" r="26" fill="#3DA557"/><circle cx="160" cy="160" r="26" fill="#3DA557"/>'
    s += f'<rect x="160" y="236" width="52" height="24" rx="5" fill="#F2C230"/><text x="186" y="254" font-size="15" fill="#1B1A1F" text-anchor="middle" {EN}>NEW</text>'
    return svg(240, 272, s)


def homework():   # 摊开的作业本：几道题
    s = '<rect x="0" y="0" width="360" height="240" rx="6" fill="#FFFDF5"/><path d="M180,0 L180,240" stroke="#C9B48A" stroke-width="4"/>'
    for k in range(6):
        y = 40 + k * 34
        s += f'<path d="M14,{y} L166,{y} M194,{y} L346,{y}" stroke="#BFD4EA" stroke-width="2"/>'
        s += f'<text x="20" y="{y-8}" font-size="15" fill="#1B3A6B" font-family="Noto Sans, sans-serif">{k+1}. {("go-went", "see-saw", "eat-ate", "run-ran", "do-did", "buy-bought")[k]}</text>'
    for k in range(4):
        s += f'<text x="200" y="{32+k*34}" font-size="15" fill="#1B3A6B" font-family="Noto Sans, sans-serif">{("I went home.", "She saw a cat.", "We ate rice.", "He ran fast.")[k]}</text>'
    return svg(360, 240, s)


def tick():
    return svg(60, 60, '<path d="M8,30 L24,48 L54,10" fill="none" stroke="#E8304A" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')


def again():   # 绕一圈回来的箭头：再一次
    return svg(160, 160, '<path d="M80,20 A60,60 0 1 1 22,94" fill="none" stroke="#2E6FD9" stroke-width="14" stroke-linecap="round"/><path d="M80,0 L112,22 L78,44 Z" fill="#2E6FD9"/>')


def redpen():
    return svg(140, 30, '<path d="M0,15 L24,6 L24,24 Z" fill="#F4D7A8"/><path d="M0,15 L8,12 L8,18 Z" fill="#E8304A"/><rect x="24" y="5" width="96" height="20" rx="4" fill="#E8304A"/><rect x="110" y="5" width="20" height="20" fill="#3A3F4B"/>')


def icon_eye():
    s = '<path d="M10,100 C50,40 150,40 190,100 C150,160 50,160 10,100 Z" fill="#FFFFFF"/><circle cx="100" cy="100" r="34" fill="#2E6FD9"/><circle cx="100" cy="100" r="16" fill="#1B1A1F"/><circle cx="110" cy="90" r="7" fill="#FFFFFF"/>'
    return svg(200, 200, s)


write_art(ART, 'soldiers.svg', soldiers())
for k in range(4):
    write_art(ART, f'calendar_f{k}.svg', calendar(k))
write_art(ART, 'book-new.svg', book_new()); write_art(ART, 'homework.svg', homework()); write_art(ART, 'tick.svg', tick(), style=False)
write_art(ART, 'again.svg', again(), style=False); write_art(ART, 'icon-again.svg', again()); write_art(ART, 'icon-eye.svg', icon_eye())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
pen = redpen()
M['west-man-inspect'] = frames_out(ART, 'west-man-inspect', [person('west-man', top='#3B5E3A', collar='#C9A24A', tie=None, right='point', mouth='flat', brows='frown', look=-1),
                                                         person('west-man', top='#3B5E3A', collar='#C9A24A', tie=None, right='chest', mouth='smile', look=-1, tilt=2)], fps=1.2, seq='pingpong')
M['cn-teacher-mark'] = frames_out(ART, 'cn-teacher-mark', [holding('cn-teacher', pen, 430, 330, 140, 30, right=(40, 100, 120, 80, 'fist'), mouth='smile', eyes='open', look=1),
                                                       holding('cn-teacher', pen, 436, 342, 140, 30, right=(40, 100, 126, 80, 'fist'), mouth='half', eyes='happy', look=1, tilt=2)], fps=2.4, seq='pingpong')
M['cn-girl-laugh'] = frames_out(ART, 'cn-girl-laugh', [person('cn-girl', left='chest', mouth='laugh', eyes='happy', tilt=4),
                                                   person('cn-girl', left='chest', mouth='smile', eyes='happy', tilt=-2)], fps=2.2, seq='pingpong')
mg = open(os.path.join(ART, 'magnifier.svg')).read()
M['cn-boy-study'] = frames_out(ART, 'cn-boy-study', [holding('cn-boy', mg, 420, 230, 120, 120, right=(40, 100, 120, 80, 'fist'), mouth='smile', eyes='open', look=1),
                                                 holding('cn-boy', mg, 424, 236, 120, 120, right=(40, 100, 124, 80, 'fist'), mouth='o', eyes='wide', look=1, brows='up')], fps=1.4, seq='pingpong')
M['west-boy-study'] = frames_out(ART, 'west-boy-study', [holding('west-boy', mg, 420, 230, 120, 120, right=(40, 100, 120, 80, 'fist'), mouth='half', eyes='open', look=1, brows='up'),
                                                     holding('west-boy', mg, 424, 236, 120, 120, right=(40, 100, 124, 80, 'fist'), mouth='laugh', eyes='happy', look=1)], fps=1.4, seq='pingpong')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

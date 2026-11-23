import sys, os, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'


def diary(open_):   # 带锁的日记本：合上（锁着）/ 打开（写满了字）
    if not open_:
        s = '<rect x="20" y="0" width="200" height="260" rx="10" fill="#9B5DE5"/><rect x="20" y="0" width="26" height="260" rx="6" fill="#7A3FC4"/>'
        s += f'<text x="132" y="70" font-size="30" fill="#FFFFFF" text-anchor="middle" {EN}>My Diary</text><text x="132" y="104" font-size="20" fill="#F2C230" text-anchor="middle" {CJK}>私人日记</text>'
        s += '<rect x="196" y="120" width="44" height="36" rx="6" fill="#C9A24A"/><rect x="206" y="128" width="30" height="40" rx="6" fill="#F2C230"/><path d="M212,128 L212,114 C212,100 230,100 230,114 L230,128" fill="none" stroke="#9AA3AE" stroke-width="6"/><circle cx="221" cy="146" r="5" fill="#5A3A22"/>'
        s += '<path d="M90,180 C100,160 120,160 128,176 C136,160 156,160 164,180 C164,200 128,220 128,220 C128,220 90,200 90,180 Z" fill="#FF9EB5"/>'
        return svg(250, 262, s)
    s = '<path d="M0,20 L150,8 L150,240 L0,252 Z" fill="#FFFDF5"/><path d="M150,8 L300,20 L300,252 L150,240 Z" fill="#FFFDF5"/><path d="M150,8 L150,240" stroke="#9B5DE5" stroke-width="6"/>'
    s += f'<text x="20" y="54" font-size="16" fill="#9B5DE5" {EN}>Oct 5</text>'
    for k in range(6):
        s += f'<path d="M16,{80+k*24} C50,{74+k*24} 90,{86+k*24} 136,{78+k*24}" fill="none" stroke="#1B3A6B" stroke-width="3"/><path d="M164,{72+k*24} C200,{66+k*24} 240,{80+k*24} 286,{72+k*24}" fill="none" stroke="#1B3A6B" stroke-width="3"/>'
    s += '<path d="M236,200 C242,190 254,190 256,198 C258,190 270,190 274,200 C274,210 256,222 256,222 C256,222 236,210 236,200 Z" fill="#FF6F91"/>'
    return svg(300, 256, s)


def letter():   # 拆开的信：作家亲笔签名
    s = '<path d="M0,90 L280,90 L280,250 L0,250 Z" fill="#E9C46A"/><path d="M0,90 L140,180 L280,90" fill="none" stroke="#C9A24A" stroke-width="5"/>'
    s += '<rect x="30" y="0" width="220" height="190" fill="#FFFFFF"/>'
    s += f'<text x="50" y="40" font-size="18" fill="#1B3A6B" {EN}>Dear Lily,</text>'
    for k in range(4):
        s += f'<path d="M50,{64+k*22} L{230 - (k % 2) * 30},{64+k*22}" stroke="#8C939E" stroke-width="3"/>'
    s += f'<text x="150" y="170" font-size="22" fill="#C0392B" font-family="Noto Serif, DejaVu Serif, serif" font-style="italic">J. Smith</text>'
    s += '<path d="M0,250 L120,170 M280,250 L160,170" stroke="#C9A24A" stroke-width="5"/>'
    return svg(280, 252, s)


def handwash(k):   # 水龙头下洗手：搓出泡沫（两帧）
    s = '<rect x="0" y="170" width="320" height="60" rx="10" fill="#FFFFFF"/><ellipse cx="160" cy="180" rx="130" ry="20" fill="#DDF1FF"/>'
    s += '<path d="M140,0 L180,0 L180,30 L230,30 L230,52 L200,52 L200,60 L180,60 L180,40 L140,40 Z" fill="#9AA3AE"/>'
    s += '<path d="M205,62 L205,150" stroke="#7CC4F2" stroke-width="10" stroke-linecap="round" opacity="0.8"/>'
    dx = (0, 14)[k]
    s += f'<path d="M{100+dx},150 C{110+dx},110 {170+dx},104 {200+dx},120 L{196+dx},140 C{170+dx},130 {130+dx},140 {120+dx},158 Z" fill="#F6D7C3"/>'
    s += f'<path d="M{230-dx},150 C{220-dx},112 {160-dx},108 {134-dx},126 L{140-dx},144 C{164-dx},134 {200-dx},142 {212-dx},160 Z" fill="#EFC9AE"/>'
    for (x, y, r) in ((140, 112, 12), (176, 104, 10), (206, 116, 13), (160, 138, 9), (120, 134, 8)):
        s += f'<circle cx="{x+dx//2}" cy="{y}" r="{r}" fill="#FFFFFF" opacity="0.9"/>'
    return svg(320, 232, s)


def privdoor():   # 门上挂着“闲人免进”的牌子
    s = '<rect x="0" y="0" width="240" height="380" fill="#8A5A3B"/><rect x="20" y="20" width="200" height="360" fill="#B5835A"/>'
    s += '<rect x="40" y="40" width="160" height="130" fill="#A87047"/><rect x="40" y="200" width="160" height="150" fill="#A87047"/><circle cx="190" cy="200" r="10" fill="#F2C230"/>'
    s += f'<rect x="50" y="70" width="140" height="70" rx="6" fill="#C0392B"/><text x="120" y="100" font-size="22" fill="#FFFFFF" text-anchor="middle" {EN}>PRIVATE</text><text x="120" y="128" font-size="20" fill="#FFFFFF" text-anchor="middle" {CJK}>闲人免进</text>'
    return svg(240, 380, s)


def tagbag():   # 书包上挂着写了名字的牌子
    s = '<path d="M40,60 C40,20 200,20 200,60 L210,250 L30,250 Z" fill="#2E6FD9"/><rect x="60" y="150" width="120" height="70" rx="10" fill="#2559B5"/><path d="M90,30 C90,4 150,4 150,30" fill="none" stroke="#1F4A99" stroke-width="10"/>'
    s += '<path d="M190,80 L250,120" stroke="#F2C230" stroke-width="4"/><rect x="236" y="112" width="70" height="44" rx="6" fill="#FFFFFF" transform="rotate(20 270 134)"/>'
    s += f'<text x="272" y="142" font-size="20" fill="#C0392B" text-anchor="middle" transform="rotate(20 270 134)" {EN}>Lily</text>'
    return svg(320, 260, s)


def icon_person():
    return svg(200, 200, '<circle cx="100" cy="60" r="34" fill="#F3D2BE"/><path d="M40,190 C40,120 70,104 100,104 C130,104 160,120 160,190 Z" fill="#2E6FD9"/><path d="M66,46 C70,20 130,20 134,46 C120,36 84,36 66,46 Z" fill="#1B1A1F"/>')


def icon_al():
    s = '<rect x="40" y="60" width="130" height="90" rx="12" fill="#FFFFFF" transform="rotate(12 105 105)"/><circle cx="60" cy="70" r="9" fill="#9AA3AE"/><path d="M20,20 L58,66" stroke="#F2C230" stroke-width="5"/>'
    s += f'<text x="110" y="118" font-size="30" fill="#C0392B" text-anchor="middle" transform="rotate(12 105 105)" {EN}>-al</text>'
    return svg(200, 200, s)


write_art(ART, 'diary-closed.svg', diary(False)); write_art(ART, 'diary-open.svg', diary(True)); write_art(ART, 'letter.svg', letter())
write_art(ART, 'handwash_f0.svg', handwash(0)); write_art(ART, 'handwash_f1.svg', handwash(1)); write_art(ART, 'privdoor.svg', privdoor())
write_art(ART, 'tagbag.svg', tagbag()); write_art(ART, 'icon-person.svg', icon_person()); write_art(ART, 'icon-al.svg', icon_al())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
lt = letter()
M['cn-girl-letter'] = frames_out(ART, 'cn-girl-letter', [holding('cn-girl', lt, 290, 250, 140, 126, left=(20, 100, 120, 70, 'fist'), right=(20, 100, 120, 70, 'fist'), mouth='o', eyes='wide', brows='up'),
                                                     holding('cn-girl', lt, 290, 250, 140, 126, left=(20, 100, 120, 70, 'fist'), right=(20, 100, 120, 70, 'fist'), mouth='laugh', eyes='happy', tilt=3)], fps=1.2, seq='pingpong')
M['west-boy-secret'] = frames_out(ART, 'west-boy-secret', [person('west-boy', right='chest', left='chest', mouth='smile', look=1, brows='up'),
                                                       person('west-boy', right='chest', left='chest', mouth='half', look=1, tilt=3)], fps=1.4, seq='pingpong')
M['west-woman-letter'] = frames_out(ART, 'west-woman-letter', [holding('west-woman', lt, 290, 250, 140, 126, left=(20, 100, 120, 70, 'fist'), right=(20, 100, 120, 70, 'fist'), mouth='smile', eyes='happy', tilt=-2),
                                                           holding('west-woman', lt, 290, 250, 140, 126, left=(20, 100, 120, 70, 'fist'), right=(20, 100, 120, 70, 'fist'), mouth='open', brows='up', tilt=2)], fps=1.2, seq='pingpong')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

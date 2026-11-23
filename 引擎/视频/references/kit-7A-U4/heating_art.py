import sys, os, json, random
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
R = random.Random(18)


def kitchen():   # 厨房：瓷砖墙、吊柜、抽油烟机、窗户和绿植、冰箱、灶台、水槽、调料架、挂着的锅铲、挂钟、福字
    d = lg('kfWall', [(0, '#F4EBDD'), (1, '#EADBC4')])
    s = '<rect width="1200" height="700" fill="url(#kfWall)"/>'
    for r in range(8):
        for c in range(20):
            s += f'<rect x="{c*60+2}" y="{230+r*30}" width="56" height="26" rx="2" fill="{("#E3EEF5", "#D6E6F0")[(r+c) % 2]}"/>'
    for i in range(4):
        x = 60 + i * 150
        s += f'<rect x="{x}" y="40" width="140" height="150" rx="6" fill="#B5835A"/><rect x="{x+10}" y="50" width="120" height="130" rx="4" fill="#C99568"/><circle cx="{x+118}" cy="160" r="6" fill="#F2C230"/>'
    s += '<path d="M700,60 L860,60 L900,200 L660,200 Z" fill="#9AA3AE"/><rect x="740" y="0" width="80" height="62" fill="#8C939E"/><rect x="670" y="196" width="220" height="12" fill="#7A828E"/>'
    s += '<rect x="930" y="40" width="200" height="170" fill="#BFE3F8"/><path d="M1030,40 L1030,210 M930,125 L1130,125" stroke="#8A5A3B" stroke-width="8"/><rect x="920" y="206" width="220" height="12" fill="#8A5A3B"/>'
    for x in (960, 1010, 1080):
        s += f'<path d="M{x-14},206 L{x+14},206 L{x+10},180 L{x-10},180 Z" fill="#B5432F"/><circle cx="{x}" cy="168" r="14" fill="#3DA557"/><circle cx="{x+10}" cy="160" r="10" fill="#2F8F46"/>'
    s += f'<rect x="300" y="250" width="60" height="60" fill="#D2232A" transform="rotate(45 330 280)"/><text x="330" y="294" font-size="36" fill="#F2C230" text-anchor="middle" {CJK}>福</text>'
    s += '<circle cx="520" cy="270" r="34" fill="#FFFFFF"/><circle cx="520" cy="270" r="34" fill="none" stroke="#3A3F4B" stroke-width="5"/><path d="M520,270 L520,248 M520,270 L536,278" stroke="#1B1A1F" stroke-width="4"/>'
    s += '<rect x="60" y="250" width="200" height="10" fill="#8A5A3B"/>'
    for i, c in enumerate(('#E8304A', '#F2C230', '#6DBE45', '#F28C28', '#9B5DE5')):
        s += f'<rect x="{70+i*38}" y="{216}" width="28" height="34" rx="4" fill="{c}"/><rect x="{70+i*38}" y="212" width="28" height="8" fill="#5A3A22"/>'
    for i in range(4):
        x = 620 + i * 34
        s += f'<path d="M{x},{240} L{x},{300}" stroke="#5A6170" stroke-width="5"/><ellipse cx="{x}" cy="{306}" rx="10" ry="14" fill="#8C939E"/>'
    s += '<rect x="0" y="470" width="1200" height="230" fill="#8A5A3B"/><rect x="0" y="460" width="1200" height="22" fill="#D8C8B0"/>'
    for i in range(6):
        x = 20 + i * 200
        s += f'<rect x="{x}" y="500" width="180" height="180" rx="6" fill="#A87047"/><rect x="{x+70}" y="580" width="40" height="8" rx="4" fill="#F2C230"/>'
    s += '<rect x="1000" y="250" width="180" height="420" rx="14" fill="#F4F6F8"/><path d="M1000,400 L1180,400" stroke="#C9D3E2" stroke-width="5"/><rect x="1020" y="300" width="10" height="70" rx="5" fill="#9AA3AE"/><rect x="1020" y="420" width="10" height="90" rx="5" fill="#9AA3AE"/>'
    s += '<rect x="80" y="440" width="180" height="24" rx="6" fill="#C9D3E2"/><path d="M170,440 L170,400 C170,388 196,388 196,400" fill="none" stroke="#9AA3AE" stroke-width="8"/>'
    s += '<path d="M380,456 C380,420 460,420 460,456 Z" fill="#3A3F4B"/><rect x="376" y="452" width="88" height="8" fill="#2B2D33"/>'
    s += '<rect x="830" y="420" width="10" height="40" fill="#8A5A3B"/><ellipse cx="880" cy="440" rx="40" ry="22" fill="#F4F1EA"/><path d="M850,436 L910,436" stroke="#2E5FA8" stroke-width="4"/><path d="M860,418 L900,410 M864,422 L906,416" stroke="#C98E5A" stroke-width="4"/>'
    return svg(1200, 700, s, d)


def stove(k):   # 灶台上一口锅在热牛奶：火苗一跳一跳（两帧）
    s = '<rect x="0" y="150" width="300" height="70" rx="6" fill="#3A3F4B"/><rect x="10" y="140" width="280" height="18" rx="4" fill="#2B2D33"/>'
    s += '<circle cx="60" cy="190" r="10" fill="#C9D3E2"/><circle cx="240" cy="190" r="10" fill="#C9D3E2"/>'
    fl = (0, 6)[k]
    for i, x in enumerate((110, 135, 160, 185)):
        h = 26 + ((i + k) % 2) * 10
        s += f'<path d="M{x-10},142 C{x-10},{142-h} {x},{142-h-fl} {x},{142-h-8} C{x+4},{142-h} {x+10},{142-h} {x+10},142 Z" fill="#F28C28"/>'
        s += f'<path d="M{x-5},142 C{x-5},{130-h/3} {x},{126-h/3} {x},{122-h/3} C{x+3},{128-h/3} {x+5},{130-h/3} {x+5},142 Z" fill="#2E6FD9"/>'
    s += '<path d="M70,40 L230,40 L222,118 C220,130 210,136 196,136 L104,136 C90,136 80,130 78,118 Z" fill="#C9D3E2"/><ellipse cx="150" cy="40" rx="80" ry="12" fill="#F4F6F8"/>'
    s += '<path d="M230,56 L290,44" stroke="#3A3F4B" stroke-width="10" stroke-linecap="round"/><path d="M84,70 L216,70" stroke="#E6EBF2" stroke-width="5"/>'
    return svg(300, 222, s)


def snowwin():   # 窗外下着雪：雪地、积雪的松树、小房子
    s = '<rect x="20" y="20" width="300" height="240" fill="#8A5A3B"/><rect x="32" y="32" width="276" height="216" fill="#CFDDEA"/>'
    s += '<path d="M32,190 C100,170 220,176 308,186 L308,248 L32,248 Z" fill="#FFFFFF"/>'
    for x, h in ((80, 70), (250, 90)):
        s += f'<path d="M{x},{190-h} L{x-34},190 L{x+34},190 Z" fill="#2F6E4A"/><path d="M{x},{190-h} L{x-16},{190-h+34} L{x+16},{190-h+34} Z" fill="#FFFFFF"/>'
    s += '<rect x="140" y="150" width="70" height="44" fill="#B5432F"/><path d="M130,152 L175,120 L220,152 Z" fill="#FFFFFF"/><rect x="166" y="168" width="16" height="26" fill="#5A3A22"/>'
    for i in range(30):
        s += f'<circle cx="{R.randint(36, 304)}" cy="{R.randint(36, 240)}" r="{R.choice([2, 3, 4])}" fill="#FFFFFF"/>'
    s += '<path d="M170,32 L170,248 M32,140 L308,140" stroke="#8A5A3B" stroke-width="7"/>'
    s += '<path d="M0,10 L40,10 C46,90 44,190 34,274 L0,274 Z" fill="#E8407A"/><path d="M340,10 L300,10 C294,90 296,190 306,274 L340,274 Z" fill="#E8407A"/><rect x="0" y="0" width="340" height="14" rx="6" fill="#5A3A22"/>'
    return svg(340, 280, s)


def icon_flame():
    return svg(200, 200, '<path d="M100,20 C130,60 160,90 150,140 C144,172 120,186 100,186 C76,186 52,170 48,140 C42,104 70,90 80,60 C90,80 96,86 104,90 C108,66 104,44 100,20 Z" fill="#F28C28"/><path d="M100,96 C114,116 126,132 120,156 C116,170 108,176 100,176 C88,176 78,166 78,152 C78,134 92,124 100,96 Z" fill="#FFD43B"/>')


def icon_ing():
    s = '<path d="M100,30 A70,70 0 1 1 34,120" fill="none" stroke="#6B4E9A" stroke-width="14" stroke-linecap="round"/><path d="M100,8 L132,32 L98,54 Z" fill="#6B4E9A"/>'
    s += '<text x="104" y="120" font-size="40" fill="#6B4E9A" text-anchor="middle" font-family="Noto Sans, sans-serif" font-weight="700">-ing</text>'
    return svg(200, 200, s)


write_art(ART, 'kitchen-bg.svg', kitchen(), bg=True)
write_art(ART, 'stove_f0.svg', stove(0)); write_art(ART, 'stove_f1.svg', stove(1)); write_art(ART, 'snowwin.svg', snowwin())
write_art(ART, 'icon-flame.svg', icon_flame()); write_art(ART, 'icon-ing.svg', icon_ing())
print('ok')

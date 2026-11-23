import sys, os, math, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'
# 6.30（第七十四版）：23 keep track of（图画书风）。要先跑 street、explore、mode 的画图脚本（街道、山林、公交车）。
# keep 保持：教室墙上“Keep quiet 保持安静”，女孩安静看书；track 踪迹：林间小路上一串小爪印；of …的：爪印尽头一只兔子“兔子的踪迹”；
# 跟踪：猎人指着爪印往前追；记录、掌握情况：男孩在小本子上给作业一项项打勾；手机跟踪校车：地图上的校车一格格往前走


def paw():   # 一个小爪印：掌垫 + 四个趾头
    s = '<ellipse cx="50" cy="62" rx="22" ry="18" fill="#6B4E2E"/>'
    for x, y in ((24, 34), (42, 22), (60, 22), (78, 34)):
        s += f'<ellipse cx="{x}" cy="{y}" rx="9" ry="11" fill="#6B4E2E"/>'
    return svg(100, 90, s)


def rabbit(k):   # 坐着的小白兔：两帧，耳朵一动一动
    a = -8 if k == 0 else 6
    s = f'<g transform="rotate({a} 84 60)"><ellipse cx="74" cy="34" rx="11" ry="34" fill="#FFFFFF"/><ellipse cx="74" cy="36" rx="5" ry="24" fill="#F7B6C2"/></g>'
    s += '<ellipse cx="100" cy="34" rx="11" ry="34" fill="#FFFFFF"/><ellipse cx="100" cy="36" rx="5" ry="24" fill="#F7B6C2"/>'
    s += '<ellipse cx="96" cy="140" rx="56" ry="46" fill="#FFFFFF"/><circle cx="150" cy="150" r="14" fill="#FFFFFF"/>'
    s += '<circle cx="88" cy="84" r="34" fill="#FFFFFF"/><circle cx="78" cy="80" r="5" fill="#1B1A1F"/><circle cx="66" cy="94" r="5" fill="#F27A8A"/>'
    s += '<path d="M66,100 L48,96 M66,102 L48,106" stroke="#9AA3AE" stroke-width="2"/><ellipse cx="80" cy="182" rx="18" ry="8" fill="#FFFFFF"/>'
    return svg(180, 196, s)


def quiet_sign():   # 墙上的牌子：“Keep quiet 保持安静”，嘘的小人头
    s = '<rect x="6" y="6" width="368" height="148" rx="16" fill="#2E6FD9"/><rect x="18" y="18" width="344" height="124" rx="10" fill="#FFFFFF"/>'
    s += '<circle cx="78" cy="80" r="44" fill="#F3D2BE"/><path d="M40,64 C42,30 114,30 116,64 C100,50 56,50 40,64 Z" fill="#1B1A1F"/><circle cx="64" cy="76" r="4" fill="#1B1A1F"/><circle cx="92" cy="76" r="4" fill="#1B1A1F"/>'
    s += '<path d="M64,100 L92,100" stroke="#C0392B" stroke-width="5" stroke-linecap="round"/><rect x="74" y="80" width="10" height="44" rx="5" fill="#E8B79E"/>'
    s += f'<text x="236" y="72" font-size="36" fill="#1A66B8" text-anchor="middle" {EN}>Keep quiet</text><text x="236" y="120" font-size="34" fill="#C0392B" text-anchor="middle" {CJK}>保持安静</text>'
    return svg(380, 160, s)


def book():   # 打开的书
    s = '<path d="M10,20 C60,6 100,14 120,26 L120,150 C100,138 60,132 10,144 Z" fill="#FFFFFF"/><path d="M230,20 C180,6 140,14 120,26 L120,150 C140,138 180,132 230,144 Z" fill="#FFFDF5"/>'
    for i in range(5):
        s += f'<path d="M26,{44+i*18} L104,{50+i*18} M136,{50+i*18} L214,{44+i*18}" stroke="#B8C0C9" stroke-width="4"/>'
    s += '<path d="M10,144 C60,132 100,138 120,150 C140,138 180,132 230,144 L230,156 C180,146 140,152 120,162 C100,152 60,146 10,156 Z" fill="#2E9E6A"/>'
    return svg(240, 170, s)


def checklist(k):   # 小本子上的作业清单：0～3 个勾
    s = '<rect x="10" y="10" width="300" height="380" rx="14" fill="#F2C230"/><rect x="28" y="24" width="270" height="352" rx="8" fill="#FFFDF5"/>'
    for y in range(40, 380, 26):
        s += f'<circle cx="18" cy="{y}" r="6" fill="#9AA3AE"/>'
    s += f'<text x="163" y="76" font-size="30" fill="#1A66B8" text-anchor="middle" {CJK}>作业 Homework</text><path d="M48,92 L278,92" stroke="#E8304A" stroke-width="3"/>'
    items = [('语文', 'Chinese'), ('数学', 'Maths'), ('英语', 'English'), ('跳绳', 'Skipping')]
    for i, (zh, en) in enumerate(items):
        y = 140 + i * 62
        s += f'<rect x="50" y="{y-28}" width="34" height="34" rx="6" fill="#FFFFFF" stroke="#5A6470" stroke-width="3"/>'
        s += f'<text x="98" y="{y}" font-size="24" fill="#2B2D33" {CJK}>{zh}</text><text x="160" y="{y}" font-size="22" fill="#5A6470" {EN}>{en}</text>'
        if i < k:
            s += f'<path d="M54,{y-12} L66,{y} L92,{y-36}" fill="none" stroke="#2B8A3E" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(320, 400, s)


def phone_map(k):   # 手机地图：路线、车站、学校，校车图标一格格往学校走
    s = '<rect x="0" y="0" width="260" height="480" rx="36" fill="#2B2D33"/><rect x="14" y="40" width="232" height="400" rx="8" fill="#EAF2E3"/>'
    s += '<rect x="104" y="16" width="52" height="9" rx="4" fill="#4A4F59"/><circle cx="130" cy="460" r="11" fill="#4A4F59"/>'
    for x in (60, 130, 200):
        s += f'<path d="M{x},40 L{x},440" stroke="#FFFFFF" stroke-width="12"/>'
    for y in (110, 220, 330):
        s += f'<path d="M14,{y} L246,{y}" stroke="#FFFFFF" stroke-width="12"/>'
    s += '<rect x="150" y="236" width="40" height="76" fill="#B9D7A8"/><rect x="74" y="124" width="44" height="80" fill="#B9D7A8"/>'
    pts = [(60, 400), (60, 330), (130, 330), (130, 220), (200, 220), (200, 110)]
    s += '<path d="M' + ' L'.join(f'{x},{y}' for x, y in pts) + '" fill="none" stroke="#2E6FD9" stroke-width="8" stroke-linejoin="round"/>'
    for x, y in pts[::2]:
        s += f'<circle cx="{x}" cy="{y}" r="9" fill="#FFFFFF" stroke="#2E6FD9" stroke-width="4"/>'
    s += f'<rect x="168" y="66" width="70" height="30" rx="6" fill="#E8304A"/><text x="203" y="88" font-size="17" fill="#FFFFFF" text-anchor="middle" {CJK}>学校</text>'
    bx, by = [(60, 360), (110, 330), (130, 260), (175, 220)][k]
    s += f'<rect x="{bx-22}" y="{by-15}" width="44" height="30" rx="7" fill="#F2C230" stroke="#1B1A1F" stroke-width="3"/><circle cx="{bx-12}" cy="{by+15}" r="6" fill="#1B1A1F"/><circle cx="{bx+12}" cy="{by+15}" r="6" fill="#1B1A1F"/>'
    s += f'<rect x="{bx-16}" y="{by-10}" width="12" height="9" fill="#BFE3F2"/><rect x="{bx+2}" y="{by-10}" width="12" height="9" fill="#BFE3F2"/>'
    return svg(260, 480, s)


def icon_keep():
    return svg(200, 200, nest(quiet_sign(), 6, 64, 188, 79))


def icon_track():
    p = paw(); s = ''
    for i, (x, y) in enumerate(((20, 130), (70, 90), (110, 120), (150, 70))):
        s += nest(p, x, y, 46, 41, uid=str(i))
    return svg(200, 200, s)


def icon_of():
    s = f'<rect x="10" y="60" width="180" height="80" rx="16" fill="#7B57D6"/><text x="100" y="114" font-size="44" fill="#FFFFFF" text-anchor="middle" {EN}>of</text>'
    s += f'<text x="100" y="180" font-size="30" fill="#7B57D6" text-anchor="middle" {CJK}>…的</text>'
    return svg(200, 200, s)


write_art(ART, 'paw.svg', paw()); write_art(ART, 'rabbit_f0.svg', rabbit(0)); write_art(ART, 'rabbit_f1.svg', rabbit(1))
write_art(ART, 'quiet-sign.svg', quiet_sign()); write_art(ART, 'book-open.svg', book())
for k in range(4):
    write_art(ART, f'checklist_f{k}.svg', checklist(k))
write_art(ART, 'icon-keep.svg', icon_keep()); write_art(ART, 'icon-track.svg', icon_track()); write_art(ART, 'icon-of.svg', icon_of())
p = os.path.join(ART, 'word_motions.json')
M = json.load(open(p)) if os.path.exists(p) else {}
HOLD = (20, 100, 120, 70, 'fist')
bk = book()
M['cn-girl-quiet'] = frames_out(ART, 'cn-girl-quiet', [holding('cn-girl', bk, 290, 262, 140, 99, left=HOLD, right=HOLD, eyes='down', mouth='smile'),
                                                     holding('cn-girl', bk, 290, 262, 140, 99, left=HOLD, right=HOLD, eyes='down', mouth='flat', tilt=3)], fps=0.8, seq='pingpong')
M['west-man-track'] = frames_out(ART, 'west-man-track', [person('west-man', right='point', look=1, mouth='flat', brows='up', top='#6B4E2E'),
                                                       person('west-man', right='present', look=1, mouth='o', eyes='wide', brows='up', top='#6B4E2E', tilt=3)], fps=1.2, seq='pingpong')
M['cn-boy-write'] = frames_out(ART, 'cn-boy-write', [person('cn-boy', right=HOLD, eyes='down', mouth='smile', top='#E8304A'),
                                                   person('cn-boy', right=HOLD, left='thumb', eyes='happy', mouth='laugh', top='#E8304A', tilt=3)], fps=1.0, seq='pingpong')
M['cn-boy-check'] = frames_out(ART, 'cn-boy-check', [person('cn-boy', right='chin', mouth='o', eyes='wide', brows='up', look=1, top='#E8304A'),
                                                   person('cn-boy', right='point', mouth='laugh', eyes='happy', look=1, top='#E8304A', tilt=-3)], fps=1.0, seq='pingpong')
M['west-girl-write'] = frames_out(ART, 'west-girl-write', [person('west-girl', right=HOLD, eyes='down', mouth='smile', top='#2E9E6A'),
                                                         person('west-girl', right=HOLD, left='thumb', eyes='happy', mouth='laugh', top='#2E9E6A', tilt=3)], fps=1.0, seq='pingpong')
M['cn-girl-map'] = frames_out(ART, 'cn-girl-map', [holding('cn-girl', phone_map(k), 318, 214, 92, 170, left=HOLD, right=HOLD,
                                                           eyes='down' if k < 3 else 'happy', mouth='smile' if k < 3 else 'laugh', tilt=(0 if k < 3 else 3), top='#7B57D6') for k in range(4)], fps=0.9, seq='loop')
json.dump(M, open(p, 'w'), ensure_ascii=False, indent=1)
print(list(M))

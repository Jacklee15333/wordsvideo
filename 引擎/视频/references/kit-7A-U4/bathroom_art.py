import sys, os, json
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
CJK = 'font-family="Noto Sans CJK SC, sans-serif" font-weight="700"'
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'


def bathtub():   # 带脚的白浴缸：满满的泡沫、水龙头、小黄鸭
    s = '<path d="M300,40 L300,10 C300,0 330,0 330,10 L330,22" fill="none" stroke="#9AA3AE" stroke-width="9"/><rect x="292" y="34" width="22" height="12" rx="4" fill="#9AA3AE"/>'
    s += '<path d="M10,70 L350,70 L340,160 C334,186 310,196 280,196 L80,196 C50,196 26,186 20,160 Z" fill="#FFFFFF"/>'
    s += '<path d="M20,70 L340,70" stroke="#C9D3E2" stroke-width="10" stroke-linecap="round"/>'
    for x in (60, 300):
        s += f'<path d="M{x-12},194 L{x+12},194 L{x+8},214 L{x-8},214 Z" fill="#C9A24A"/>'
    for i, (x, y, r) in enumerate(((40, 62, 22), (74, 52, 26), (112, 60, 22), (150, 50, 28), (190, 58, 24), (228, 50, 26), (266, 60, 22), (304, 56, 24), (96, 40, 16), (176, 36, 18), (250, 38, 16))):
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#EAF6FF"/><circle cx="{x-r*0.35:.0f}" cy="{y-r*0.35:.0f}" r="{max(3, r*0.2):.0f}" fill="#FFFFFF"/>'
    s += '<path d="M120,30 C108,30 106,14 120,12 C126,4 140,6 140,16 L150,16 L144,24 C150,38 134,44 120,30 Z" fill="#FFD43B"/><circle cx="132" cy="14" r="3" fill="#1B1A1F"/>'
    return svg(360, 220, s)


def bubble():
    return svg(40, 40, '<circle cx="20" cy="20" r="16" fill="#DDF1FF" fill-opacity="0.7" stroke="#8FC3E8" stroke-width="2"/><circle cx="14" cy="14" r="4" fill="#FFFFFF"/>')


def toilet():   # 马桶（侧面）
    s = '<rect x="20" y="10" width="90" height="120" rx="10" fill="#FFFFFF"/><rect x="34" y="0" width="62" height="14" rx="5" fill="#E6EBF2"/><circle cx="96" cy="30" r="6" fill="#C9D3E2"/>'
    s += '<path d="M10,140 L190,140 C190,180 160,200 120,206 L120,250 L60,250 L64,206 C34,196 10,176 10,140 Z" fill="#FFFFFF"/>'
    s += '<path d="M6,128 L196,128 L196,142 L6,142 Z" fill="#E6EBF2"/><path d="M40,250 L140,250" stroke="#C9D3E2" stroke-width="8"/>'
    return svg(200, 260, s)


def wc_sign():   # 卫生间的牌子：WC、卫生间、男女小人
    s = '<rect x="0" y="0" width="240" height="120" rx="12" fill="#1F6E5A"/><rect x="6" y="6" width="228" height="108" rx="9" fill="none" stroke="#FFFFFF" stroke-width="3"/>'
    s += f'<text x="70" y="62" font-size="44" fill="#FFFFFF" text-anchor="middle" {EN}>WC</text><text x="70" y="98" font-size="24" fill="#FFFFFF" text-anchor="middle" {CJK}>卫生间</text>'
    s += '<circle cx="160" cy="34" r="10" fill="#FFFFFF"/><rect x="150" y="48" width="20" height="34" rx="5" fill="#FFFFFF"/><rect x="151" y="80" width="7" height="24" fill="#FFFFFF"/><rect x="162" y="80" width="7" height="24" fill="#FFFFFF"/>'
    s += '<circle cx="204" cy="34" r="10" fill="#FFFFFF"/><path d="M192,82 L198,48 L210,48 L216,82 Z" fill="#FFFFFF"/><rect x="196" y="80" width="6" height="24" fill="#FFFFFF"/><rect x="206" y="80" width="6" height="24" fill="#FFFFFF"/>'
    s += '<path d="M182,26 L182,104" stroke="#FFFFFF" stroke-width="3"/>'
    return svg(240, 120, s)


def icon_bath():
    s = '<path d="M20,90 L180,90 L172,150 C168,166 154,172 138,172 L62,172 C46,172 32,166 28,150 Z" fill="#FFFFFF"/><path d="M24,90 L176,90" stroke="#C9D3E2" stroke-width="8" stroke-linecap="round"/>'
    for x, y, r in ((50, 82, 16), (80, 74, 20), (114, 80, 17), (146, 74, 19), (98, 58, 12)):
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#EAF6FF"/>'
    s += '<path d="M160,90 L160,40 C160,30 176,30 176,40" fill="none" stroke="#9AA3AE" stroke-width="7"/>'
    return svg(200, 200, s)


write_art(ART, 'bathtub.svg', bathtub()); write_art(ART, 'bubble.svg', bubble(), style=False)
write_art(ART, 'toilet.svg', toilet()); write_art(ART, 'wc-sign.svg', wc_sign()); write_art(ART, 'icon-bath.svg', icon_bath())
print('ok')

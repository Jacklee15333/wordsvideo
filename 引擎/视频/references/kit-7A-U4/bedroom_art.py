import sys, os, json, math
sys.path.insert(0, os.path.expanduser('~/kit'))
from common import *
ART = sys.argv[1]
EN = 'font-family="Noto Sans, DejaVu Sans, sans-serif" font-weight="700"'


def cat_sleep(k):   # 蜷成一团睡觉的橘猫：两帧，一呼一吸
    b = 1.0 + 0.04 * k
    s = f'<path d="M60,120 C30,118 24,92 48,84" fill="none" stroke="#F28C28" stroke-width="16" stroke-linecap="round"/>'
    s += f'<ellipse cx="130" cy="{100-3*k}" rx="{80*b:.0f}" ry="{46*b:.0f}" fill="#F28C28"/>'
    for i in range(3):
        s += f'<path d="M{110+i*22},{62-2*k} C{116+i*22},{80} {116+i*22},{96} {108+i*22},{112}" fill="none" stroke="#C25E12" stroke-width="6"/>'
    s += '<circle cx="196" cy="102" r="36" fill="#F28C28"/><path d="M168,82 L172,50 L190,72 Z M206,70 L222,48 L226,82 Z" fill="#F28C28"/>'
    s += '<path d="M174,78 L176,58 L186,72 Z M210,72 L220,56 L222,78 Z" fill="#FF9EB5"/><ellipse cx="200" cy="118" rx="18" ry="12" fill="#FFE2B8"/>'
    s += '<path d="M178,100 q8,6 16,0 M202,100 q8,6 16,0" fill="none" stroke="#1B1A1F" stroke-width="4" stroke-linecap="round"/>'
    s += '<path d="M196,112 L204,112 L200,117 Z" fill="#E8407A"/><ellipse cx="90" cy="136" rx="34" ry="10" fill="#FFE2B8"/>'
    return svg(260, 160, s)


def zzz():
    return svg(60, 60, f'<text x="30" y="48" font-size="50" fill="#2E6FD9" text-anchor="middle" {EN}>Z</text>')


def window(state, k=0):   # 卧室的窗户：开着时窗帘被风吹起来（三帧），关上时窗帘垂着
    s = '<rect x="40" y="20" width="220" height="250" fill="#8A5A3B"/><rect x="52" y="32" width="196" height="226" fill="#BFE3F8"/>'
    s += '<ellipse cx="110" cy="80" rx="40" ry="14" fill="#FFFFFF"/><ellipse cx="200" cy="64" rx="30" ry="10" fill="#FFFFFF"/>'
    s += '<rect x="186" y="150" width="14" height="108" fill="#7A5232"/><circle cx="193" cy="140" r="44" fill="#3DA557"/><circle cx="166" cy="160" r="26" fill="#2F8F46"/>'
    s += '<rect x="52" y="200" width="70" height="58" fill="#C9D3E2"/><rect x="62" y="210" width="14" height="14" fill="#FFE27A"/><rect x="90" y="210" width="14" height="14" fill="#FFE27A"/>'
    if state == 'closed':
        s += '<path d="M150,32 L150,258 M52,145 L248,145" stroke="#8A5A3B" stroke-width="8"/><path d="M70,50 L100,40 M200,50 L230,40" stroke="#FFFFFF" stroke-width="4"/>'
        s += '<path d="M0,10 L56,10 C60,90 58,190 50,286 L0,286 Z" fill="#E8407A"/><path d="M300,10 L244,10 C240,90 242,190 250,286 L300,286 Z" fill="#E8407A"/>'
    else:
        s += '<path d="M150,32 L192,48 L192,250 L150,258 Z" fill="#DCEFFA" opacity="0.9"/><path d="M150,32 L192,48 L192,250 L150,258 Z" fill="none" stroke="#8A5A3B" stroke-width="7"/>'
        sw = (30, 52, 40)[k]
        s += f'<path d="M0,10 L56,10 C{70+sw},90 {80+sw*1.6:.0f},180 {60+sw*1.4:.0f},286 L0,286 Z" fill="#E8407A"/>'
        s += f'<path d="M300,10 L244,10 C{230-sw},90 {220-sw*1.6:.0f},180 {240-sw*1.4:.0f},286 L300,286 Z" fill="#E8407A"/>'
        for j in range(3):
            s += f'<path d="M{150 - 40 + j*40},{100+j*50} q20,-10 40,0" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.8"/>'
    s += '<rect x="0" y="0" width="300" height="14" rx="6" fill="#5A3A22"/><rect x="30" y="268" width="240" height="16" fill="#E6D2B5"/>'
    return svg(300, 290, s)


def space_arrows():   # 空间：横竖两条虚线双箭头
    c = '#2E6FD9'
    s = f'<path d="M30,130 L370,130 M200,20 L200,240" stroke="{c}" stroke-width="6" stroke-dasharray="16 10"/>'
    s += f'<path d="M30,130 L58,112 L58,148 Z M370,130 L342,112 L342,148 Z M200,20 L182,48 L218,48 Z M200,240 L182,212 L218,212 Z" fill="{c}"/>'
    return svg(400, 260, s)


def box():
    s = '<rect x="0" y="20" width="160" height="110" fill="#C98E5A"/><path d="M0,20 L30,0 L190,0 L160,20 Z" fill="#E0AA74"/><path d="M160,20 L190,0 L190,110 L160,130 Z" fill="#A86E3E"/>'
    s += '<rect x="66" y="20" width="28" height="110" fill="#E9C27A"/><path d="M60,70 L100,70" stroke="#8A5A3B" stroke-width="3"/>'
    return svg(190, 130, s)


def icon_bed():
    s = '<rect x="20" y="70" width="18" height="110" fill="#8A5A3B"/><rect x="162" y="110" width="18" height="70" fill="#8A5A3B"/><rect x="20" y="120" width="160" height="40" rx="6" fill="#F4F1EA"/>'
    s += '<rect x="44" y="104" width="44" height="22" rx="10" fill="#FFFFFF"/><path d="M90,118 L180,118 L180,160 L90,160 Z" fill="#2E6FD9"/><path d="M90,130 L180,130" stroke="#FFFFFF" stroke-width="4"/>'
    return svg(200, 200, s)


def icon_room():
    s = '<path d="M30,40 L100,70 L100,180 L30,150 Z" fill="#F2E3C6"/><path d="M100,70 L170,40 L170,150 L100,180 Z" fill="#E6D2B5"/><path d="M30,150 L100,180 L170,150 L100,125 Z" fill="#C9A27A"/>'
    s += '<path d="M66,148 L134,148" stroke="#2E6FD9" stroke-width="5" stroke-dasharray="8 6"/><path d="M60,148 L74,140 L74,156 Z M140,148 L126,140 L126,156 Z" fill="#2E6FD9"/>'
    return svg(200, 200, s)


write_art(ART, 'cat-sleep_f0.svg', cat_sleep(0)); write_art(ART, 'cat-sleep_f1.svg', cat_sleep(1))
write_art(ART, 'zzz.svg', zzz(), style=False)
for k in range(3):
    write_art(ART, f'window-open_f{k}.svg', window('open', k))
write_art(ART, 'window-closed.svg', window('closed'))
write_art(ART, 'space-arrows.svg', space_arrows(), style=False); write_art(ART, 'box.svg', box())
write_art(ART, 'icon-bed.svg', icon_bed()); write_art(ART, 'icon-room.svg', icon_room())
print('ok')

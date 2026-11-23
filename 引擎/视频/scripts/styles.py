#!/usr/bin/env python3
"""6.29（第七十一版）画风轮换：每做 5 个视频换一种画风（规矩 58）。把一个词 art 文件夹里已经画好的图画书风插图，整批转成另一种画风。
  python3 styles.py gongbi <art 文件夹>      # 青绿工笔风（原图存在 <art>/_book/，可以再转回来：python3 styles.py book <art>）
  python3 styles.py list                     # 有哪些画风
画风表 STYLES 按顺序轮：第 1–5 个视频 STYLES[0]，6–10 STYLES[1]……用户往「画面素材」里加了新元素，就在表里加一种（写一个 conv_xxx）。"""
import os, re, sys, shutil, colorsys, glob
STYLES = [
    ('book', '图画书风', '《七颗宝石》：粗细变化的黑色勾线、饱和平涂、白净鹅蛋脸、圆腮红'),
    ('gongbi', '青绿工笔风', '山 1–3（青绿山水长卷）、鸟 1（工笔锦鸡）：暖黄绢底、细而匀的墨线、石青石绿、朱砂赭石、红印章'),
    ('ink', '水墨写意风', '竹子 1–3（墨竹）：宣纸、浓淡墨、大片留白、淡彩'),
    ('heji', '中西合璧风', '动物 1–2（骏马图）：绢本暖黄底和构图，西洋明暗、体积、透视'),
]
def style_for(number):
    """单元里的序号（1 起）→ 画风名字：每 5 个换一种，轮完从头再来"""
    return STYLES[((int(number) - 1) // 5) % len(STYLES)][0]
HEX = re.compile(r'#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b')
def _rgb(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
def _hex(r, g, b):
    return '#%02X%02X%02X' % tuple(max(0, min(255, round(v * 255))) for v in (r, g, b))
def _mix(a, b, k):
    return tuple(x * (1 - k) + y * k for x, y in zip(a, b))
SILK = _rgb('#E3CF9F')
def gongbi_color(h, ink=False):
    """一个颜色 → 青绿工笔的颜色：降饱和、偏暖；蓝的变石青、绿的变石绿、红的变朱砂、粉的变胭脂、黄的变赭黄；
    浅蓝的天空变成绢的颜色（古画的天是留出来的绢底），白的变绢白，很深的颜色变成墨色"""
    r, g, b = _rgb(h)
    if ink:
        return '#2E2318'
    H, S, V = colorsys.rgb_to_hsv(r, g, b)
    deg = H * 360
    if V < 0.33:
        return _hex(*_mix((r, g, b), _rgb('#2E2318'), 0.8))            # 头发、眼睛、深色衣服：墨
    if S < 0.12:                                                       # 白、灰
        if V > 0.85: return _hex(*_mix((r, g, b), _rgb('#F1E6CC'), 0.75))
        return _hex(*_mix((r, g, b), SILK, 0.35))
    if 175 <= deg <= 255 and V > 0.84:                                  # 浅蓝的天、玻璃：绢色，带一点青
        return _hex(*_mix(_rgb('#E6D3A3'), _rgb('#9FC2C0'), 0.25 * S))
    if 185 <= deg <= 255:   H2, S2, V2 = 203, 0.50 + 0.1 * S, 0.42 + 0.35 * V          # 石青
    elif 75 <= deg < 185:   H2, S2, V2 = 158, 0.38 + 0.12 * S, 0.38 + 0.35 * V          # 石绿
    elif 300 <= deg < 352:  H2, S2, V2 = 352, 0.30 + 0.12 * S, 0.66 + 0.2 * V           # 胭脂、粉（腮红淡淡的，衣服是暗一点的胭脂）
    elif deg < 18 or deg >= 352: H2, S2, V2 = 6, 0.62, 0.55 + 0.25 * V                  # 朱砂
    elif 18 <= deg < 50:
        if S < 0.45 and V > 0.75: H2, S2, V2 = 28, S * 0.7, V * 0.95                      # 皮肤
        else: H2, S2, V2 = 32, 0.55, 0.55 + 0.3 * V                                      # 赭石
    elif 50 <= deg < 75:    H2, S2, V2 = 44, 0.50, 0.60 + 0.3 * V                         # 藤黄
    else:                   H2, S2, V2 = 262, 0.25, 0.45 + 0.3 * V                        # 淡紫（花青调）
    rr, gg, bb = colorsys.hsv_to_rgb(H2 / 360, min(1, S2), min(1, V2))
    return _hex(*_mix((rr, gg, bb), SILK, 0.12))
SEAL = ('<g transform="translate({x} {y}) rotate(-3)"><rect x="0" y="0" width="{w}" height="{w}" rx="4" fill="#B3312A" opacity="0.88"/>'
        '<rect x="{i}" y="{i}" width="{wi}" height="{wi}" fill="none" stroke="#F3E6CC" stroke-width="{sw}"/>'
        '<text x="{c}" y="{t1}" font-size="{fs}" fill="#F3E6CC" text-anchor="middle" font-family="Noto Serif CJK SC, Noto Sans CJK SC, serif" font-weight="900">词源</text>'
        '<text x="{c}" y="{t2}" font-size="{fs}" fill="#F3E6CC" text-anchor="middle" font-family="Noto Serif CJK SC, Noto Sans CJK SC, serif" font-weight="900">构词</text></g>')
def silk_overlay(vb):
    x0, y0, w, h = [float(v) for v in vb.split()]
    s = (f'<defs><radialGradient id="gbVig" cx="0.5" cy="0.5" r="0.75"><stop offset="0.55" stop-color="#8A6A3A" stop-opacity="0"/><stop offset="1" stop-color="#6B4F2A" stop-opacity="0.32"/></radialGradient>'
         f'<pattern id="gbSilk" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0,3 L6,3 M3,0 L3,6" stroke="#7A5A30" stroke-width="0.5" opacity="0.10"/></pattern></defs>')
    s += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#C9A86A" opacity="0.24"/>'
    s += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#gbSilk)"/><rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#gbVig)"/>'
    sw = max(40, min(w, h) * 0.075)
    s += SEAL.format(x=x0 + w * 0.80, y=y0 + h * 0.06, w=sw, i=sw * 0.08, wi=sw * 0.84, sw=sw * 0.03, c=sw / 2, t1=sw * 0.47, t2=sw * 0.86, fs=sw * 0.34)
    return s
def conv_gongbi(svg, is_bg):
    # 墨线细而匀：粗的勾线都改细（外轮廓最多 2.2），颜色改成暖墨色
    # 胳膊、腿这种“管子”（很粗的线）不能变细：粗线里墨色的那条是管子的外轮廓，只收窄一点（两边各剩 1.2 左右）
    def fix_path(m):
        tag = m.group(0)
        w = re.search(r'stroke-width="([\d.]+)"', tag)
        if not w: return tag
        v = float(w.group(1)); ink = 'stroke="#1B1A1F"' in tag
        if v >= 10:
            nv = max(1.0, v - 5.6) if ink else v
        else:
            nv = max(0.7, min(2.2, v * 0.45))
        return tag.replace(w.group(0), 'stroke-width="%.2f"' % nv)
    svg = re.sub(r'<[a-z]+\b[^>]*stroke-width="[\d.]+"[^>]*>', fix_path, svg)
    svg = re.sub(r'stroke="#1B1A1F"', 'stroke="#2E2318"', svg)
    svg = HEX.sub(lambda m: gongbi_color(m.group(0)), svg)
    svg = re.sub(r'filter="url\(#bkGlow\)"', '', svg)          # 不要图画书人物外面那圈淡蓝光晕
    if is_bg:
        vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
        svg = re.sub(r'</svg>\s*$', silk_overlay(vb) + '</svg>', svg)
    return svg

# ---------------- 6.29.2：水墨写意风（第 11–15 个）----------------
PAPER = _rgb('#F4EFE4'); INK = _rgb('#262422')
TINTS = {'red': _rgb('#B0645A'), 'blue': _rgb('#5C7C8A'), 'green': _rgb('#76876F'), 'ochre': _rgb('#C2A177'), 'violet': _rgb('#857A8E')}
def ink_color(h):
    """一个颜色 → 水墨写意的颜色：按明暗变成浓淡不同的墨色，很浅的留白（宣纸色）；
    鲜艳的颜色只留一点淡彩（红 → 胭脂、蓝 → 花青、绿 → 墨绿、黄橙 → 淡赭）"""
    r, g, b = _rgb(h)
    H, S, V = colorsys.rgb_to_hsv(r, g, b)
    deg = H * 360
    L = 0.30 * r + 0.59 * g + 0.11 * b
    if V < 0.30: return _hex(*_mix(INK, PAPER, 0.06))                  # 头发、眼睛：浓墨
    if S < 0.12 and V > 0.85: return _hex(*PAPER)                      # 白：留白
    if 175 <= deg <= 255 and V > 0.84: return _hex(*_mix(PAPER, _rgb('#C9CDCB'), 0.35 + 0.3 * S))   # 天、玻璃：淡淡一层
    t = min(1.0, max(0.0, (L - 0.12) / 0.86)) ** 0.85                   # 墨分五色：越亮越接近纸
    base = _mix(INK, PAPER, 0.10 + 0.88 * t)
    if deg < 20 or deg >= 300: tint = TINTS['red']
    elif deg < 70: tint = TINTS['ochre']
    elif deg < 170: tint = TINTS['green']
    elif deg < 260: tint = TINTS['blue']
    else: tint = TINTS['violet']
    k = (0.55 if tint in (TINTS['red'], TINTS['ochre']) else 0.42) * S
    col = _mix(base, tint, k)
    if 18 <= deg < 50 and S < 0.45 and V > 0.75: col = _mix(_rgb('#F1E3D3'), _rgb('#E7CDB8'), S)   # 皮肤：淡淡的
    return _hex(*col)
SEAL_INK = SEAL.replace('#B3312A', '#B8322A')
def paper_overlay(vb):
    x0, y0, w, h = [float(v) for v in vb.split()]
    s = (f'<defs><radialGradient id="inkVig" cx="0.5" cy="0.45" r="0.8"><stop offset="0.6" stop-color="#5A5650" stop-opacity="0"/><stop offset="1" stop-color="#4A4640" stop-opacity="0.22"/></radialGradient>'
         f'<pattern id="inkFib" width="23" height="17" patternUnits="userSpaceOnUse"><path d="M0,4 C6,3 9,6 14,5 M5,12 C10,10 16,14 23,12 M18,1 L21,8" stroke="#8C877C" stroke-width="0.6" fill="none" opacity="0.16"/></pattern></defs>')
    s += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#EFE8D8" opacity="0.18"/>'
    s += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#inkFib)"/><rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#inkVig)"/>'
    sw = max(40, min(w, h) * 0.07)
    s += SEAL_INK.format(x=x0 + w * 0.81, y=y0 + h * 0.06, w=sw, i=sw * 0.08, wi=sw * 0.84, sw=sw * 0.03, c=sw / 2, t1=sw * 0.47, t2=sw * 0.86, fs=sw * 0.34)
    return s
def thin_lines(svg, ink_hex, keep=0.45, cap=2.2, tube=5.6):
    def fix_path(m):
        tag = m.group(0)
        w = re.search(r'stroke-width="([\d.]+)"', tag)
        if not w: return tag
        v = float(w.group(1)); ink = 'stroke="#1B1A1F"' in tag
        if v >= 10: nv = max(1.0, v - tube) if ink else v
        else: nv = max(0.7, min(cap, v * keep))
        return tag.replace(w.group(0), 'stroke-width="%.2f"' % nv)
    svg = re.sub(r'<[a-z]+\b[^>]*stroke-width="[\d.]+"[^>]*>', fix_path, svg)
    return re.sub(r'stroke="#1B1A1F"', 'stroke="%s"' % ink_hex, svg)
def conv_ink(svg, is_bg):
    svg = thin_lines(svg, '#262422', keep=0.5, cap=2.4)
    svg = HEX.sub(lambda m: ink_color(m.group(0)), svg)
    svg = re.sub(r'filter="url\(#bkGlow\)"', '', svg)
    if is_bg:
        vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
        svg = re.sub(r'</svg>\s*$', paper_overlay(vb) + '</svg>', svg)
    return svg
# ---------------- 6.29.2：中西合璧风（第 16–20 个）----------------
def heji_color(h):
    """中国绢本的暖黄底色调 + 西洋写实的颜色：色相不变，饱和度降一点，整体偏暖（往绢色里调一成多）"""
    r, g, b = _rgb(h)
    H, S, V = colorsys.rgb_to_hsv(r, g, b)
    if V < 0.25: return _hex(*_mix((r, g, b), _rgb('#2A1E14'), 0.6))
    rr, gg, bb = colorsys.hsv_to_rgb(H, S * 0.78, V * 0.97)
    return _hex(*_mix((rr, gg, bb), SILK, 0.16))
SHADE = ('<defs><filter id="hjVol" x="-5%" y="-5%" width="110%" height="110%">'
         '<feGaussianBlur in="SourceAlpha" stdDeviation="{b}" result="bl"/><feOffset in="bl" dx="-{o}" dy="-{o}" result="of"/>'
         '<feComposite in="SourceAlpha" in2="of" operator="arithmetic" k2="1" k3="-1" result="edge"/>'
         '<feFlood flood-color="#3A2614" flood-opacity="0.30"/><feComposite in2="edge" operator="in" result="sh"/>'
         '<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="sh"/></feMerge></filter></defs>')
def light_overlay(vb):   # 西洋画的光：左上亮、右下暗，再罩绢色、绢纹、印章
    x0, y0, w, h = [float(v) for v in vb.split()]
    s = (f'<defs><linearGradient id="hjLight" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF4D8" stop-opacity="0.22"/>'
         f'<stop offset="0.55" stop-color="#FFF4D8" stop-opacity="0"/><stop offset="1" stop-color="#3A2614" stop-opacity="0.20"/></linearGradient></defs>')
    s += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#hjLight)"/>'
    return s + silk_overlay(vb).replace('opacity="0.24"', 'opacity="0.14"').replace('stop-opacity="0.32"', 'stop-opacity="0.24"')
def conv_heji(svg, is_bg):
    svg = thin_lines(svg, '#3A2A1C', keep=0.8, cap=4.0, tube=3.0)
    svg = HEX.sub(lambda m: heji_color(m.group(0)), svg)
    svg = re.sub(r'filter="url\(#bkGlow\)"', '', svg)
    vb = re.search(r'viewBox="([^"]+)"', svg)
    if not vb: return svg
    vb = vb.group(1)
    if is_bg:
        svg = re.sub(r'</svg>\s*$', light_overlay(vb) + '</svg>', svg)
    else:                                                    # 人和东西：边上压一层暖色暗部，有体积感
        x0, y0, w, h = [float(v) for v in vb.split()]
        b = max(2.0, min(w, h) * 0.02); o = max(1.5, min(w, h) * 0.015)
        m = re.match(r'(\s*<svg\b[^>]*>)(.*)</svg>\s*$', svg, re.S)
        if m: svg = m.group(1) + SHADE.format(b='%.1f' % b, o='%.1f' % o) + '<g filter="url(#hjVol)">' + m.group(2) + '</g></svg>'
    return svg

CONV = {'gongbi': conv_gongbi, 'ink': conv_ink, 'heji': conv_heji}
def restyle(art, style):
    keep = os.path.join(art, '_book')
    os.makedirs(keep, exist_ok=True)
    n = 0
    for f in sorted(glob.glob(os.path.join(art, '*.svg'))):
        b = os.path.basename(f)
        src = os.path.join(keep, b)
        if not os.path.exists(src):
            shutil.copy(f, src)                   # 图画书风的原样留一份
        s = open(src, encoding='utf-8').read()
        if style != 'book':
            s = CONV[style](s, b.endswith('-bg.svg') or b in ('vault-room.svg', 'obscura-room.svg'))
        open(f, 'w', encoding='utf-8').write(s); n += 1
    open(os.path.join(art, 'STYLE'), 'w').write(style)
    return n
if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == 'list':
        for i, (k, name, how) in enumerate(STYLES):
            print('%2d–%2d  %-7s %s：%s' % (i * 5 + 1, i * 5 + 5, k, name, how))
    else:
        st, art = sys.argv[1], sys.argv[2]
        if st not in CONV and st != 'book':
            sys.exit('还没有这种画风：%s（python3 styles.py list）' % st)
        print('%s：%d 张插图转成 %s' % (art, restyle(art, st), st))

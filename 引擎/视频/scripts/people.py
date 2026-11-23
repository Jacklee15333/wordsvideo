#!/usr/bin/env python3
"""写实一点的人物（腰部以上，正面）：男老师 / 女生……可以换发型、衣服、手势、嘴型。

  python3 people.py <输出文件夹>          # 生成一套常用的人物 svg
  在别的脚本里：from people import person; person(sex='f', hair='bob', top='sweater', color='#D9825B', gesture='down', mouth='smile')

画法：脸、脖子、手用渐变（上亮下暗）和柔和的阴影，眼睛有虹膜、高光，衣服有明暗和领子。
腰以下不画：站在讲台、桌子、柜台后面（家具挡住腰），或者让画框的下边截住。
"""
import os, sys

SKINS = {
    'light': dict(base='#F2C7A2', mid='#E6B089', shadow='#C98E68', hi='#FBDCC2'),
    'warm':  dict(base='#E8B48A', mid='#D99D72', shadow='#B97A52', hi='#F5CBA6'),
}

def _defs(k, skin, top_col, top_dark):
    return f'''<defs>
  <radialGradient id="{k}Face" cx="0.42" cy="0.38" r="0.68"><stop offset="0" stop-color="{skin['hi']}"/><stop offset="0.55" stop-color="{skin['base']}"/><stop offset="1" stop-color="{skin['mid']}"/></radialGradient>
  <linearGradient id="{k}Neck" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{skin['shadow']}"/><stop offset="0.45" stop-color="{skin['mid']}"/><stop offset="1" stop-color="{skin['base']}"/></linearGradient>
  <linearGradient id="{k}Arm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{skin['mid']}"/><stop offset="0.5" stop-color="{skin['base']}"/><stop offset="1" stop-color="{skin['shadow']}"/></linearGradient>
  <linearGradient id="{k}Top" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{top_dark}"/><stop offset="0.35" stop-color="{top_col}"/><stop offset="0.7" stop-color="{top_col}"/><stop offset="1" stop-color="{top_dark}"/></linearGradient>
  <linearGradient id="{k}Sleeve" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{top_dark}"/><stop offset="0.5" stop-color="{top_col}"/><stop offset="1" stop-color="{top_dark}"/></linearGradient>
  <linearGradient id="{k}Shirt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6F9FD"/><stop offset="1" stop-color="#D3DFEE"/></linearGradient>
  <linearGradient id="{k}Tie" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7E2626"/><stop offset="0.5" stop-color="#B23C3C"/><stop offset="1" stop-color="#7E2626"/></linearGradient>
  <radialGradient id="{k}Iris" cx="0.4" cy="0.4" r="0.6"><stop offset="0" stop-color="#5A3826"/><stop offset="1" stop-color="#22140D"/></radialGradient>
  <radialGradient id="{k}Blush" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#E8907A" stop-opacity="0.34"/><stop offset="1" stop-color="#E8907A" stop-opacity="0"/></radialGradient>
  <linearGradient id="{k}Hair" x1="0" y1="0" x2="0.3" y2="1"><stop offset="0" stop-color="#3A2E29"/><stop offset="1" stop-color="#211A17"/></linearGradient>
</defs>'''

def _eye(k, cx, cy, s, skin, lash):
    lw = 3.2 if lash else 2.4
    flick = f'<path d="M{cx+13*s},{cy-0.5} L{cx+17*s},{cy-4}" stroke="#2A1D17" stroke-width="2.2" stroke-linecap="round"/>' if lash else ''
    return f'''<path d="M{cx-12*s},{cy+1} C{cx-8*s},{cy-6} {cx+8*s},{cy-7} {cx+13*s},{cy} C{cx+8*s},{cy+5} {cx-7*s},{cy+6} {cx-12*s},{cy+1} Z" fill="#FBFBFA"/>
<circle cx="{cx+0.5*s}" cy="{cy-0.3}" r="5.4" fill="url(#{k}Iris)"/><circle cx="{cx+0.5*s}" cy="{cy-0.3}" r="2.5" fill="#0E0A08"/><circle cx="{cx+2*s}" cy="{cy-2}" r="1.5" fill="#fff"/>
<path d="M{cx-12.5*s},{cy+0.5} C{cx-8*s},{cy-7} {cx+8*s},{cy-8} {cx+13.5*s},{cy-0.5}" fill="none" stroke="#2A1D17" stroke-width="{lw}" stroke-linecap="round"/>{flick}
<path d="M{cx-9*s},{cy-8.5} C{cx-3*s},{cy-11} {cx+6*s},{cy-11} {cx+11*s},{cy-7}" fill="none" stroke="{skin['shadow']}" stroke-opacity="0.5" stroke-width="1.4"/>'''

def _mouth(mouth, fem):
    lip = '#C9615C' if fem else '#B3625A'
    if mouth == 'open':
        return f'''<path d="M185,191 C191,186.5 209,186.5 215,191 C211,202 189,202 185,191 Z" fill="#7A2E2E"/>
<path d="M189,191 C194,188.8 206,188.8 211,191 L210,193.4 C204,192.5 196,192.5 190,193.4 Z" fill="#FFFFFF"/>
<ellipse cx="200" cy="197.5" rx="7" ry="2.5" fill="#C45E5E"/>
<path d="M184.5,190.5 C190.5,186 209.5,186 215.5,190.5" fill="none" stroke="{lip}" stroke-width="2.4" stroke-linecap="round"/>
<path d="M189,200 C195,203.5 205,203.5 211,200" fill="none" stroke="{lip}" stroke-width="1.8" stroke-linecap="round" opacity="0.8"/>'''
    if mouth == 'smile':
        fill = '<path d="M186,190 C192,187.5 198,188.5 200,189.5 C202,188.5 208,187.5 214,190 C207,198 193,198 186,190 Z" fill="#D4706A"/>' if fem else ''
        return f'''{fill}<path d="M185,190 C192,198 208,198 215,190" fill="none" stroke="#A65750" stroke-width="2.6" stroke-linecap="round"/>
<path d="M182,188 C183,190 184,191 186,191 M218,188 C217,190 216,191 214,191" stroke="#C98E68" stroke-width="1.6" fill="none" opacity="0.7"/>'''
    return '''<path d="M187,192 C193,195 207,195 213,192" fill="none" stroke="#A65750" stroke-width="2.6" stroke-linecap="round"/>'''

def _head(k, skin, sex, hair, mouth, hair_col):
    fem = sex == 'f'
    face = ('M200,64 C231,64 254,86 256,121 C258,150 252,172 240,190 C229,207 216,220 203,223 C201,223.6 199,223.6 197,223 C184,220 171,207 160,190 C148,172 142,150 144,121 C146,86 169,64 200,64 Z' if fem else
            'M200,62 C232,62 256,84 258,120 C260,150 255,174 243,193 C233,209 219,222 205,225 C201.5,225.8 198.5,225.8 195,225 C181,222 167,209 157,193 C145,174 140,150 142,120 C144,84 168,62 200,62 Z')
    back = ''
    if hair == 'bob':
        back = f'<path d="M200,40 C252,40 278,80 276,130 C275,170 282,214 284,252 C264,266 236,262 226,250 L174,250 C164,262 136,266 116,252 C118,214 125,170 124,130 C122,80 148,40 200,40 Z" fill="{hair_col}"/>'
    elif hair == 'ponytail':
        back = f'<path d="M262,96 C292,110 300,160 290,214 C286,236 276,250 266,256 C274,226 276,170 256,130 Z" fill="{hair_col}"/>'
    if hair == 'short':
        front = f'''<path d="M141,128 C134,82 160,46 204,45 C247,45 271,76 261,128 C258,108 251,93 238,86 C216,97 178,95 160,90 C150,100 145,112 141,128 Z" fill="{hair_col}"/>
<path d="M170,62 C190,52 222,52 244,66" fill="none" stroke="#5B4A42" stroke-width="3" stroke-linecap="round" opacity="0.6"/>'''
    else:
        front = f'''<path d="M143,132 C136,84 163,48 204,47 C246,47 270,80 260,132 C254,112 246,100 236,94 C226,108 196,112 172,104 C160,110 150,120 143,132 Z" fill="{hair_col}"/>
<path d="M172,104 C190,96 214,82 236,70" fill="none" stroke="#5B4A42" stroke-width="2.6" stroke-linecap="round" opacity="0.55"/>
<path d="M165,60 C188,50 222,50 246,64" fill="none" stroke="#6A564C" stroke-width="3" stroke-linecap="round" opacity="0.5"/>'''
    brow_w = 3.6 if fem else 5
    return f'''<g>{back}
<path d="M256,126 C271,119 278,138 273,153 C270,165 262,171 253,167 Z" fill="{skin['mid']}"/>
<path d="M144,126 C129,119 122,138 127,153 C130,165 138,171 147,167 Z" fill="{skin['mid']}"/>
<path d="{face}" fill="url(#{k}Face)"/>
<path d="M150,170 C156,192 172,212 198,224.5 C184,222 170,212 158,196 C152,188 148,178 150,170 Z" fill="{skin['shadow']}" opacity="0.32"/>
<path d="M250,170 C244,192 228,212 202,224.5 C216,222 230,212 242,196 C248,188 252,178 250,170 Z" fill="{skin['shadow']}" opacity="0.22"/>
<circle cx="168" cy="166" r="15" fill="url(#{k}Blush)"/><circle cx="232" cy="166" r="15" fill="url(#{k}Blush)"/>
{front}
<path d="M163,117 C171,110 184,109 193,113" fill="none" stroke="#2A201C" stroke-width="{brow_w}" stroke-linecap="round"/>
<path d="M237,117 C229,110 216,109 207,113" fill="none" stroke="#2A201C" stroke-width="{brow_w}" stroke-linecap="round"/>
{_eye(k, 178, 133, 1, skin, fem)}
{_eye(k, 222, 133, -1, skin, fem)}
<path d="M197,140 C196.5,150 195,157 193,162" fill="none" stroke="{skin['shadow']}" stroke-width="2" stroke-linecap="round" opacity="0.55"/>
<path d="M193,163.5 C196,168 204,168 207,163.5" fill="none" stroke="{skin['shadow']}" stroke-width="2.5" stroke-linecap="round"/>
<path d="M201,142 L201,157" stroke="#fff" stroke-opacity="0.35" stroke-width="2.5" stroke-linecap="round"/>
{_mouth(mouth, fem)}
</g>'''

def _torso(k, sex, top):
    neck = f'<path d="M178,200 L177,266 L223,266 L222,200 Z" fill="url(#{k}Neck)"/>'
    if sex == 'f':
        body = f'M86,560 L90,338 C92,300 112,278 148,268 L178,258 C188,270 212,270 222,258 L252,268 C288,278 308,300 310,338 L314,560 Z'
        lo, ro = 178, 222
    else:
        body = 'M68,560 L72,332 C74,292 98,270 138,259 L176,250 C186,263 214,263 224,250 L262,259 C302,270 326,292 328,332 L332,560 Z'
        lo, ro = 176, 224
    out = neck + f'<path d="{body}" fill="url(#{k}Top)"/>'
    if top == 'blazer':
        out += f'''<path d="M176,250 L200,372 L224,250 C214,263 186,263 176,250 Z" fill="url(#{k}Shirt)"/>
<path d="M193,262 L207,262 L204,277 L196,277 Z" fill="#8E2E2E"/><path d="M196,277 L204,277 L212,358 L200,374 L188,358 Z" fill="url(#{k}Tie)"/>
<path d="M176,250 L194,284 L168,270 Z" fill="#FFFFFF" stroke="#C3D2E4" stroke-width="1.2"/><path d="M224,250 L206,284 L232,270 Z" fill="#FFFFFF" stroke="#C3D2E4" stroke-width="1.2"/>
<path d="M174,251 L200,376 L186,378 L148,302 L165,288 L154,268 Z" fill="#000" opacity="0.10"/><path d="M226,251 L200,376 L214,378 L252,302 L235,288 L246,268 Z" fill="#000" opacity="0.18"/>
<path d="M174,251 L154,268 L165,288 L148,302" fill="none" stroke="#fff" stroke-opacity="0.25" stroke-width="1.6"/>
<circle cx="200" cy="430" r="5" fill="#000" opacity="0.45"/><circle cx="200" cy="490" r="5" fill="#000" opacity="0.45"/>'''
    elif top == 'sweater':
        out += f'''<path d="M{lo},258 L200,322 L{ro},258 C212,270 188,270 {lo},258 Z" fill="url(#{k}Shirt)"/>
<path d="M{lo},258 L194,288 L{lo-10},276 Z" fill="#FFFFFF" stroke="#C3D2E4" stroke-width="1.2"/><path d="M{ro},258 L206,288 L{ro+10},276 Z" fill="#FFFFFF" stroke="#C3D2E4" stroke-width="1.2"/>
<path d="M{lo-2},257 L200,326 L{ro+2},257" fill="none" stroke="#000" stroke-opacity="0.18" stroke-width="7" stroke-linejoin="round"/>
<g stroke="#000" stroke-opacity="0.07" stroke-width="3">{''.join(f'<line x1="{x}" y1="300" x2="{x}" y2="560"/>' for x in range(110, 300, 14))}</g>'''
    elif top == 'tshirt':
        out += f'''<path d="M{lo},258 C186,276 214,276 {ro},258" fill="none" stroke="#000" stroke-opacity="0.18" stroke-width="6"/>'''
    out += '<path d="M118,268 C104,290 98,320 100,350" fill="none" stroke="#fff" stroke-opacity="0.12" stroke-width="10" stroke-linecap="round"/>'
    return out

def _arms(k, skin, gesture, sex):
    xo = 0 if sex == 'm' else 14
    right = f'<path d="M{300-xo},284 C{322-xo},300 {332-xo},336 {334-xo},380 L{336-xo},560 L{300-xo},560 L{296-xo},392 C{294-xo},350 {290-xo},318 {282-xo},296 Z" fill="url(#{k}Sleeve)"/>'
    if gesture != 'raise':
        left = f'<path d="M{100+xo},284 C{78+xo},300 {68+xo},336 {66+xo},380 L{64+xo},560 L{100+xo},560 L{104+xo},392 C{106+xo},350 {110+xo},318 {118+xo},296 Z" fill="url(#{k}Sleeve)"/>'
        return right, left, False
    sk = skin
    left = f'''<path d="M104,282 C80,296 66,330 64,372 C63,394 66,410 72,422 L106,420 C102,398 104,368 112,340 C116,322 120,306 124,296 Z" fill="url(#{k}Sleeve)"/>
<path d="M72,422 C62,400 52,372 44,346 L72,334 C80,360 92,392 106,420 Z" fill="url(#{k}Sleeve)"/>
<path d="M42,348 L70,336 L66,326 L40,338 Z" fill="#EEF3FA" stroke="#C3D2E4" stroke-width="1"/>
<path d="M40,338 C33,322 32,306 38,296 L44,292 L68,292 C72,304 72,318 66,328 Z" fill="url(#{k}Arm)"/>
<path d="M38,298 C35,282 34,268 37,258 C38,253 45,253 46,258 L48,294 Z" fill="{sk['base']}" stroke="{sk['shadow']}" stroke-width="1"/>
<path d="M46,293 C45,276 45,260 47,250 C48,245 55,245 56,250 L57,292 Z" fill="{sk['base']}" stroke="{sk['shadow']}" stroke-width="1"/>
<path d="M56,293 C56,278 57,264 59,255 C60,250 67,251 67,256 L66,294 Z" fill="{sk['base']}" stroke="{sk['shadow']}" stroke-width="1"/>
<path d="M65,296 C66,284 68,274 71,267 C73,263 79,265 78,270 L73,300 Z" fill="{sk['base']}" stroke="{sk['shadow']}" stroke-width="1"/>
<path d="M66,322 C74,318 82,310 88,300 C91,296 96,299 94,304 C90,316 82,326 70,334 Z" fill="{sk['mid']}" stroke="{sk['shadow']}" stroke-width="1"/>
<path d="M44,312 C50,318 58,318 64,312" fill="none" stroke="{sk['shadow']}" stroke-width="1.4" opacity="0.7"/>'''
    return right, left, True

def person(sex='m', hair='short', top='blazer', color='#33496E', dark=None, gesture='down', mouth='closed', skin='light', hair_col='#2A211D', key='p'):
    """一个人（viewBox 0 0 400 560，腰部以上）。mouth：open 正在说话 / smile 笑 / closed；gesture：raise 抬手讲解 / down"""
    sk = SKINS[skin]
    dark = dark or _shade(color, 0.62)
    k = key
    right, left, front = _arms(k, sk, gesture, sex)
    body = _torso(k, sex, top)
    inner = (right + body + left) if front else (right + left + body)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 560">
{_defs(k, sk, color, dark)}
{inner}
{_head(k, sk, sex, hair, mouth, hair_col)}
</svg>'''

def _shade(hexc, f):
    h = hexc.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return '#%02X%02X%02X' % (int(r * f), int(g * f), int(b * f))

CAST = {
    'teacher-talk': dict(sex='m', top='blazer', color='#33496E', gesture='raise', mouth='open', key='tt'),
    'teacher-say': dict(sex='m', top='blazer', color='#33496E', gesture='down', mouth='open', key='ts'),
    'teacher-calm': dict(sex='m', top='blazer', color='#33496E', gesture='down', mouth='closed', key='tc'),
    'clerk': dict(sex='m', top='sweater', color='#7A6A55', gesture='down', mouth='closed', key='ck', hair_col='#3B2C22'),
    'girl-smile': dict(sex='f', hair='bob', top='sweater', color='#D9825B', gesture='down', mouth='smile', key='gs'),
    'girl-talk': dict(sex='f', hair='bob', top='sweater', color='#D9825B', gesture='down', mouth='open', key='gt'),
    'woman-smile': dict(sex='f', hair='ponytail', top='sweater', color='#5B8C7A', gesture='down', mouth='smile', key='ws', skin='warm'),
}

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    for name, spec in CAST.items():
        open(os.path.join(out, name + '.svg'), 'w').write(person(**spec))
    print('人物：' + '、'.join(CAST))

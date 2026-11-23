import json, os, sys
ART = os.environ['WART']
MOT = {}
for _f in ('motions.json', 'cam_motions.json', 'word_motions.json'):
    if os.path.exists(os.path.join(ART, _f)):
        MOT.update(json.load(open(os.path.join(ART, _f), encoding='utf-8')))
BEAT = 100          # 放音乐那几幅画的节拍（每分钟几拍）：音箱、音符、屏幕上的柱子、跟着点头的人都踩这个拍子


def actor(name, **kw):
    """一个会动的人（poses.py MOTIONS）：frames + 放法（seq、fps / mouths、gfps）"""
    m = MOT.get(name)
    if m:
        d = {'svg': 'art/' + m['frames'][0], 'frames': ['art/' + f for f in m['frames']], 'seq': m['seq']}
        for k in ('fps', 'mouths', 'gfps', 'mfps'):
            if k in m:
                d[k] = m[k]
    else:
        fr = sorted(f for f in os.listdir(ART) if f.startswith(name + '_f') and f.endswith('.svg'))
        d = {'svg': 'art/' + (fr[0] if fr else name + '.svg')}
        if len(fr) > 1:
            d.update({'frames': ['art/' + f for f in fr], 'fps': 3})
    d.update(kw)
    return d


def walker(name, y, s, x0, x1, offset=0.0, z=3):
    """走路的人：从 x0 走到 x1（走出去再从头进来），脚踩在 y 那条线上"""
    m = MOT[name]
    return {'svg': 'art/' + m['frames'][0], 'frames': ['art/' + f for f in m['frames']], 'fps': m.get('fps', 7), 'seq': 'loop',
            'x': x0, 'y': y - 0.47 * s, 's': s, 'z': z, 'walk': {'from': [x0, y - 0.47 * s], 'to': [x1, y - 0.47 * s], 'offset': offset}}


def mouth_waves(on, side=1, when=None, cue=None, delay=None, r1=0.2, color='#F59E0B', z=3):
    """从人嘴边出来的声波（pose 的嘴在 360, 192），跟着这个人说话（with）"""
    w = {'waves': True, 'on': on, 'x': 360 + 70 * side, 'y': 188, 'dir': 0 if side > 0 else 180, 'spread': 64, 'n': 3, 'period': 1.2,
         'r0': 0.03, 'r1': r1, 'lw': 0.012, 'color': color, 'with': on, 'z': z}
    if when:
        w['when'] = when
    if cue is not None:
        w['cue'] = cue
    if delay is not None:
        w['delay'] = delay
    return w


def beams(xs=(0.28, 0.72), len_=0.95, z=-0.5):
    return [{'beam': True, 'x': x, 'y': -0.02, 'len': len_, 'width': 15, 'swing': 7, 'period': 5.5 + k, 'tilt': (-6 if x < 0.5 else 6), 'z': z}
            for k, x in enumerate(xs)]


def stage_group(W, H, px, py_bottom, hp, who='west-man-present', waves=True, wave_when=None, delay=0.0, talk=None):
    py = py_bottom - hp / 2
    hperson = 2.05 * hp
    top_surface = py - hp / 2 + 40 / 340 * hp
    person_top = top_surface - 332 / 560 * hperson
    ms = 0.714 * hp / 230
    base = (px + 0.435 * hp, top_surface)
    mc = (base[0] - 42 * ms, base[1] - 103 * ms)
    man = actor(who, id='man', x=px / W, y=(person_top + hperson / 2) / H, s=hperson / H, delay=delay, z=0)
    if talk:
        man.update(talk)
    items = [man,
             {'id': 'pod', 'svg': 'art/podium.svg', 'x': px / W, 'y': py / H, 's': hp / H, 'delay': delay, 'z': 1},
             {'id': 'mic', 'svg': 'art/mic.svg', 'x': mc[0] / W, 'y': mc[1] / H, 's': 0.714 * hp / H, 'delay': delay, 'z': 2}]
    if waves:      # 人和物：嘉宾对着麦克风说话，麦克风那边才出声波（with: 'man'）
        w = {'waves': True, 'x': (mc[0] + 0.1 * hp) / W, 'y': (mc[1] - 0.18 * hp) / H, 'dir': -20, 'spread': 70, 'n': 3, 'period': 1.25,
             'r0': 0.03, 'r1': 0.22, 'lw': 0.011, 'color': '#F59E0B', 'with': 'man', 'z': 3}
        w.update(wave_when or {'delay': delay + 0.5})
        items.append(w)
    return items


def audience(h=0.34, y=0.95, x=0.5, extra=None):
    """台下一排听众：各自轻轻动，台上的人说完一句，大家点点头（人和人）"""
    it = {'svg': 'art/audience-wide.svg', 'x': x, 'y': y, 's': h, 'z': 5, 'crowd': 9, 'nodWith': 'man'}
    it.update(extra or {})
    return it


def desk_scene(W, H, desk_s, desk_x=0.5, bottom=1.02, spk_s=0.42, spk_dx=0.24, mon_s=0.4, plant=None, lamp=None, extra_when=None, music=True):
    """屋里的书桌：中间一台放音乐的电脑，两边一对音箱（主角）。music：放音乐——屏幕上的柱子跳、音箱跟着拍子一鼓一鼓（物和物）"""
    top = bottom - desk_s
    surf = top + 26 / 300 * desk_s
    items = [{'svg': 'art/desk.svg', 'x': desk_x, 'y': bottom - desk_s / 2, 's': desk_s, 'z': 0}]
    mon = {'id': 'mon', 'svg': 'art/computer-music.svg', 'x': desk_x, 'y': surf - mon_s / 2 + 0.03 * mon_s / 0.4, 's': mon_s, 'z': 1}
    items.append(mon)
    if music:      # 屏幕右边一排跳动的柱子（电脑在放音乐），盖在屏幕上原来画的那几条上
        eq = {'eq': True, 'on': 'mon', 'x': 282, 'y': 138, 'w': 150 * mon_s * H / 360 / W, 'h': 72 * mon_s / 360, 'n': 7, 'z': 1.5}
        eq.update(extra_when or {})
        items.append(eq)
    for k, dx in (('spL', -spk_dx), ('spR', spk_dx)):
        it = {'id': k, 'svg': 'art/speaker.svg', 'x': desk_x + dx, 'y': surf - spk_s / 2 + 0.01, 's': spk_s, 'z': 2}
        if music:
            it.update({'anim': 'thump'})
        it.update(extra_when or {})
        items.append(it)
    if plant:
        items.append({'svg': 'art/plant.svg', 'x': plant[0], 'y': surf - plant[1] / 2 + 0.01, 's': plant[1], 'z': 1})
    if lamp:
        items.append({'svg': 'art/lamp.svg', 'x': lamp[0], 'y': surf - lamp[1] / 2 + 0.005, 's': lamp[1], 'z': 1})
    return items, surf


def music_from(spk, spk_s, when=None, cue=None, delay0=0.4, rise=0.26):
    """两边音箱放音乐：音箱外侧一圈圈声波，音符一个接一个飘上去（踩着 pic.beat），左右错开半拍"""
    out = []
    for j, (sid, side) in enumerate(spk):
        wv = {'waves': True, 'on': sid, 'x': 128, 'y': 258, 'dir': 0 if side > 0 else 180, 'spread': 78, 'n': 3, 'period': 60 / BEAT * 2,
              'r0': 0.36 * spk_s, 'r1': 0.36 * spk_s + 0.17, 'lw': 0.012, 'color': '#2FB5A9', 'z': 3}
        nt = {'emit': True, 'svg': 'art/note.svg', 'alt': ['art/note2.svg'], 'on': sid, 'x': 128 + side * 60, 'y': 70, 's': 0.15,
              'to': [side * 0.1, -rise], 'life': 2.2, 'every': 120 / BEAT, 'offset': j * 60 / BEAT, 'z': 4}
        for it in (wv, nt):
            if when:
                it['when'] = when
                if cue is not None:
                    it['cue'] = cue
            else:
                it['delay'] = delay0
        out += [wv, nt]
    return out



def band(svg, k, mid, x=0.5, H=204):
    return {'svg': svg, 'x': x, 'y': 0.5 + (350 - mid) * k / H, 's': 700 * k / H, 'z': -5}
def waist(s, cut=440):
    """会动的人（720×560 画布）让画框下边截在腰上：返回中心 y"""
    return 1 - (cut - 280) / 560 * s

"""speaker 的画面设置（6.25 标准样例，第六十二版）：图画书画风 + 详细场景 + 中外结合 + 画面真的动起来 + 人和人 / 人和物 / 物和物有互动。

插图在 art/（拷到 ~/wordfilm-work/speaker/art/）；会动的人先生成：python3 scripts/poses.py ~/wordfilm-work/speaker/art --motion（写 motions.json）。
用法：python3 make_prefs.py ~/wordfilm-work/edits.json

6.25 加的（用户：“比如 speaker 画的是人在演讲，那么可以让人物动起来，嘴巴讲起来这样的；大喇叭也是一样，可以画一下音波这样的，
周围有人的话，可以画人在走动”“如果多人同台，或者做事，要增加一些互动，就是人和人，人和物，物和物……要根据内容来进行”）：
  - 说话的人：seq talk（手势来回慢慢动、嘴一张一合、一句一停）；听的人：seq blink（歪头、眨眼）
  - 人和人：老师讲、女孩听，老师每说完一句女孩点点头（nodWith）；女孩讲完老师才笑（turn 轮流）；台上讲完一句，台下听众点头（crowd + nodWith）
  - 人和物：人对着麦克风说话，声波才出来（waves 的 with）；嘉宾指着屏幕讲，水龙头一直滴水
  - 物和物：电脑放音乐 → 屏幕上的柱子跳、两边音箱一鼓一鼓、音符飘出来、女孩跟着点头，都踩同一个节拍（pic.beat = 100）；
            讲台上的麦克风 → 旁边的舞台音箱出声波
  - 车站：电线杆上的大喇叭两边出声波，旅客拖着箱子、背着书包来回走（walk）
"""
import json, os, sys
ART = os.environ.get('SPEAKER_ART', os.path.expanduser('~/wordfilm-work/speaker/art'))
MOT = json.load(open(os.path.join(ART, 'motions.json'), encoding='utf-8')) if os.path.exists(os.path.join(ART, 'motions.json')) else {}
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


P = {'style': 'core', 'board': True}

# ======== 现在的两个意思
W, H = 537, 356
pic0 = {'text': '演讲人、发言人', 'pos': '名词', 'diff': '站在台上对着大家讲话的人', 'bg': 'blank', 'img': 'art/stage-bg.svg',
        'items': beams() + [{'svg': 'art/banner-speech.svg', 'x': 0.5, 'y': 0.115, 's': 0.12, 'z': -1}]
        + stage_group(W, H, 0.42 * W, H, 0.42 * H, who='west-man-present') + [audience(0.36, 0.95)]}
it1, surf = desk_scene(W, H, 0.46, spk_s=0.44, spk_dx=0.27, mon_s=0.4, plant=(0.06, 0.28))
pic1 = {'text': '扬声器、音箱', 'pos': '名词', 'diff': '会发出声音的机器', 'bg': 'blank', 'img': 'art/room-bg.svg', 'beat': BEAT,
        'items': it1 + [{'svg': 'art/mug.svg', 'x': 0.925, 'y': surf - 0.06 + 0.012, 's': 0.12, 'z': 2}] + music_from([('spL', -1), ('spR', 1)], 0.44)}

# ======== 例句
W, H = 1120, 432
g_ex0 = stage_group(W, H, 0.33 * W, H * 1.02, 0.44 * H, who='west-man-point', wave_when={'when': 'talked', 'cue': 0})
ex0 = {'bg': 'blank', 'img': 'art/stage-bg.svg',
       'items': beams((0.22, 0.5)) + [{'svg': 'art/banner-speech.svg', 'x': 0.33, 'y': 0.095, 's': 0.155, 'z': -1}] + g_ex0 + [
           {'id': 'scr', 'svg': 'art/screen-water.svg', 'x': 0.7, 'y': 0.4, 's': 0.6, 'delay': 0.2, 'z': 0},
           # 人和物：嘉宾指着屏幕讲“节约用水”，水龙头一滴一滴地滴
           {'svg': 'art/drop.svg', 'on': 'scr', 'x': 327, 'y': 200, 's': 0.09, 'go': [327, 300], 'dur': 0.9, 'loop': True, 'when': 'saving water', 'cue': 0, 'fade': 0.2, 'z': 2},
           {'label': '节约用水', 'on': 'scr', 'x': 150, 'y': 260, 'size': 0.085, 'when': '节约用水', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6'},
           audience(0.32, 0.95)]}
it2, surf2 = desk_scene(W, H, 0.55, desk_x=0.5, spk_s=0.42, spk_dx=0.13, mon_s=0.42, plant=(0.8, 0.3))
for it in it2:
    if it.get('svg') == 'art/computer-music.svg':
        it['x'] = 0.58
    if it.get('id') == 'spL':
        it['x'] = 0.45
    if it.get('id') == 'spR':
        it['x'] = 0.71
# 人和物：女孩跟着音乐点头、竖大拇指——一个来回两拍，和音箱、音符同一个拍子
girl = actor('west-girl-music', id='girl', x=0.25, y=(0.47 - 380 / 560 * 0.7) + 0.35, s=0.7, z=-1, fps=round(BEAT / 60 * 2, 3))
ex1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'beat': BEAT,
       'items': [girl] + it2 + [{'svg': 'art/books.svg', 'x': 0.365, 'y': surf2 - 0.05 + 0.012, 's': 0.1, 'z': 2}]
       + music_from([('spL', -1), ('spR', 1)], 0.42, when='comes out', cue=0, rise=0.24) + [
           {'label': '音箱', 'x': 0.45, 'y': 0.07, 'to': [0.45, 0.14], 'size': 0.08, 'when': '音箱', 'cue': 1}]}
pic0.update({'ex': 'The speaker talked about saving water.', 'exzh': '演讲人讲了节约用水。', 'exPic': ex0})
pic1.update({'ex': 'The music comes out of the speaker.', 'exzh': '音乐从音箱里传出来。', 'exPic': ex1})
P['pics'] = [pic0, pic1]

# ======== 每部分卡片
W, H = 302, 300
P['partPics'] = {
    # 人和人：老师指着黑板讲，女孩歪头听，老师每说完一句女孩点点头；声波从老师嘴边出来，老师停下来就没有
    'p0': {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
        actor('west-girl-listen', id='g', x=0.8, y=0.66, s=0.76, z=0, nodWith='m'),
        actor('cn-teacher-point', id='m', x=0.3, y=0.6, s=0.86, z=1),
        mouth_waves('m', 1, when='说', r1=0.16),
        {'svg': 'art/class-desks.svg', 'x': 0.5, 'y': 0.95, 's': 0.3, 'z': 4}]},
    # 人和物、物和物：嘉宾挥手打招呼、对着麦克风说话，旁边的舞台音箱跟着出声波（他停下来音箱就不响）
    'p1': {'bg': 'blank', 'img': 'art/stage-bg.svg', 'items': stage_group(W, H, 0.36 * W, H, 0.36 * H, who='west-man-hello', wave_when={'when': '说话的人'}) + [
        {'id': 'pa', 'svg': 'art/pa-speaker.svg', 'x': 0.85, 'y': 0.5, 's': 0.82, 'when': '东西', 'fade': 0.4, 'z': 0},
        {'waves': True, 'on': 'pa', 'x': 170, 'y': 150, 'dir': 0, 'spread': 70, 'n': 3, 'period': 1.2, 'r0': 0.04, 'r1': 0.16, 'lw': 0.012,
         'color': '#F59E0B', 'with': 'man', 'when': '东西', 'z': 3},
        {'label': '人', 'x': 0.36, 'y': 0.93, 'size': 0.1, 'when': '人或东西', 'z': 6},
        {'label': '东西', 'x': 0.85, 'y': 0.93, 'size': 0.1, 'when': '东西', 'delay': 0.2, 'hideWhen': '说话的人', 'z': 6},
        {'label': '说话的人', 'x': 0.7, 'y': 0.12, 'size': 0.1, 'when': '说话的人', 'color': '#C2410C', 'border': '#F97316', 'z': 6}]},
}
P['icons'] = {'p0': 'art/icon-speak.svg', 'p1': 'art/icon-er.svg'}

# ======== 拼起来：说话的人（女孩举手发言，老师边听边点头）
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    actor('cn-teacher-listen', x=0.3, y=0.6, s=0.9, z=0, nodWith='m'),
    actor('west-girl-raise', id='m', x=0.7, y=0.6, s=0.92, z=1),
    mouth_waves('m', -1, delay=0.4, r1=0.2),
    {'svg': 'art/class-desks.svg', 'x': 0.5, 'y': 0.97, 's': 0.3, 'z': 4}]}

# ======== 意思怎么变过来
W, H = 600, 448
# 人和人：女孩摊开手讲，老师一边听一边哈哈笑（这一格只在“它们是怎么来的呢？”那一句出现，不到两秒，所以两个人同时动，
# 不用 turn 轮流——turn 适合停得久的画，比如对话的例句）
fig_lit = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    actor('cn-teacher-laugh', x=0.74, y=0.62, s=0.78, z=0, anim='breathe'),
    actor('west-girl-explain', id='m', x=0.32, y=0.6, s=0.84, z=1),
    mouth_waves('m', 1, delay=0.3, r1=0.18),
    {'svg': 'art/class-desks.svg', 'x': 0.5, 'y': 0.96, 's': 0.3, 'z': 4},
    {'label': '说话的人', 'x': 0.14, 'y': 0.3, 'size': 0.07, 'delay': 0.5, 'z': 6}]}
g1 = stage_group(W, H, 0.42 * W, H, 0.42 * H, who='west-man-speech', wave_when={'when': '讲话'}, talk={'talkWhen': '讲话'})
for it in g1:
    if it.get('id') in ('pod', 'mic'):
        it.update({'when': '台上', 'fade': 0.4}); it.pop('delay', None)
fig_1 = {'bg': 'blank', 'img': 'art/stage-bg.svg', 'items': beams() + [{'svg': 'art/banner-speech.svg', 'x': 0.5, 'y': 0.11, 's': 0.12, 'z': -1}] + g1 + [
    audience(0.34, 0.95, extra={'when': '对着大家', 'fade': 0.4}),
    {'label': '演讲人', 'x': 0.8, 'y': 0.16, 'size': 0.075, 'when': '演讲人', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
s2 = [
    {'label': '做事的人', 'x': 0.24, 'y': 0.1, 'size': 0.066, 'when': '做这件事的人', 'cue': 0, 'z': 6},
    {'ray': [[0.39, 0.1], [0.53, 0.1]], 'arrow': True, 'color': '#C2410C', 'lw': 0.012, 'when': '机器', 'cue': 0, 'dur': 0.5, 'z': 6},
    {'label': '做这件事的机器', 'x': 0.74, 'y': 0.1, 'size': 0.066, 'when': '机器', 'cue': 0, 'delay': 0.3, 'z': 6},
    actor('west-clerk-think', x=0.23, y=0.5, s=0.56, when='计算的人', fade=0.4, hideCue=2, z=1),
    {'svg': 'art/desk-papers.svg', 'x': 0.23, 'y': 0.8, 's': 0.3, 'when': '计算的人', 'fade': 0.4, 'hideCue': 2, 'z': 2},
    {'label': 'computer 计算的人', 'x': 0.23, 'y': 0.96, 'size': 0.058, 'when': '计算的人', 'delay': 0.2, 'hideCue': 2, 'z': 6},
    {'ray': [[0.45, 0.56], [0.55, 0.56]], 'arrow': True, 'color': '#C2410C', 'lw': 0.012, 'when': '计算的机器', 'dur': 0.5, 'hideCue': 2, 'z': 6},
    {'svg': 'art/desk.svg', 'x': 0.8, 'y': 0.86, 's': 0.24, 'when': '计算的机器', 'fade': 0.4, 'hideCue': 2, 'z': 1},
    {'id': 'calc', 'svg': 'art/computer.svg', 'x': 0.78, 'y': 0.59, 's': 0.42, 'when': '计算的机器', 'fade': 0.4, 'hideCue': 2, 'z': 2},
    {'label': 'computer 计算机', 'x': 0.78, 'y': 0.96, 'size': 0.058, 'when': '计算的机器', 'delay': 0.2, 'hideCue': 2, 'z': 6},
]
it3, surf3 = desk_scene(W, H, 0.4, spk_s=0.44, spk_dx=0.3, mon_s=0.38, extra_when={'when': '会出声', 'fade': 0.4})
for it in it3:
    if 'when' not in it:
        it.update({'when': '会出声', 'fade': 0.4})
s2 += it3 + music_from([('spL', -1), ('spR', 1)], 0.44, when='说话的机器', cue=2) + [
    {'label': 'speaker 扬声器、音箱', 'x': 0.5, 'y': 0.2, 'size': 0.065, 'when': '扬声器', 'cue': 2, 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6}]
fig_2 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'beat': BEAT, 'items': s2}
P['flow'] = [
    {'node': '“说话的人”', 'fig': fig_lit},
    {'via': '站在台上，对着大家讲话', 'node': '① 演讲人、发言人', 'pos': '名词', 'pic': 0,
     'say': '说话的人站到台上，对着大家讲话，就是演讲人、发言人。它说的是人，所以是名词。', 'fig': fig_1},
    {'from': 0, 'via': '会出声、像人一样“说话”的机器', 'node': '② 扬声器、音箱', 'pos': '名词', 'pic': 1,
     'rule': '英语里，表示“做这件事的人”的词，也拿来叫做这件事的东西、机器',
     'ruleEx': 'speaker 说话的人 → 扬声器      computer 计算的人 → 计算机',
     'say': ['英语里，表示做这件事的人的词，也常拿来叫做这件事的机器。',
             '就像 computer，本来是计算的人，后来计算的机器也叫 computer。',
             '所以，会出声、像人一样说话的机器，也叫 speaker，就是扬声器、音箱。它说的是一样东西，所以是名词。'],
     'fig': fig_2},
]

# ======== 同义词辨析（6.25：两张卡时画放大到约 504 × 204，声波、走路的人看得清）
W, H = 504, 204


def band(svg, k, mid, x=0.5):
    """背景按 k 倍画（1200 × 700 的图 → 1200k × 700k 像素），让背景里高度 mid 的那一条落在画框正中"""
    return {'svg': svg, 'x': x, 'y': 0.5 + (350 - mid) * k / H, 's': 700 * k / H, 'z': -5}


itd, _ = desk_scene(W, H, 0.56, bottom=1.25, spk_s=0.74, spk_dx=0.2, mon_s=0.7)
# 车站广场：电线杆上的大喇叭往两边出声波（在广播），旅客拖着箱子、背着书包来回走（中外都有）
LS = 0.9
station = [band('art/station-bg.svg', 0.5, 470, x=0.6),
           {'id': 'ls', 'svg': 'art/loudspeaker.svg', 'x': 0.27, 'y': 0.97 - 0.5 * LS, 's': LS, 'z': 2},
           {'waves': True, 'on': 'ls', 'x': 96, 'y': 150, 'dir': 180, 'spread': 62, 'n': 3, 'period': 1.1, 'r0': 0.05, 'r1': 0.3, 'lw': 0.016, 'color': '#F59E0B', 'z': 3},
           {'waves': True, 'on': 'ls', 'x': 544, 'y': 150, 'dir': 0, 'spread': 62, 'n': 3, 'period': 1.1, 'r0': 0.05, 'r1': 0.42, 'lw': 0.016, 'color': '#F59E0B', 'z': 3},
           walker('walk-west-woman-case', 0.98, 0.56, -0.08, 1.1, 0.12, z=4),
           walker('walk-cn-boy-pack', 0.94, 0.48, 1.08, -0.08, 0.45, z=3),
           walker('walk-west-man-case', 0.9, 0.42, -0.08, 1.1, 0.7, z=2.5),
           walker('walk-cn-girl', 0.95, 0.42, 1.08, -0.08, 0.05, z=3.5)]
P['distinguish'] = {
    'key': '扬声器',
    'items': [
        {'w': 'speaker', 'gloss': '音箱', 'note': '电脑、手机、家里的音箱，日常就说 speaker',
         'pic': {'bg': 'blank', 'beat': BEAT, 'items': [band('art/room-bg.svg', 0.46, 300)] + itd + music_from([('spL', -1), ('spR', 1)], 0.74, rise=0.36)}},
        {'w': 'loudspeaker', 'gloss': '大喇叭', 'note': 'loud 响亮的 + speaker：广场、车站的大喇叭',
         'pic': {'bg': 'blank', 'items': station}},
    ],
    'tip': 'loudspeaker 多了 loud，声音更大、更正式',
}
out = sys.argv[1] if len(sys.argv) > 1 else 'edits.json'
json.dump({'speaker': P}, open(out, 'w'), ensure_ascii=False, indent=1)
print('ok')

import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/heating/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.29.2：18 heating（中西合璧风）。heat 加热：灶上的锅冒热气；-ing 这件事：读书的女士（reading）；
# 加热：热牛奶；暖气：窗外下雪，屋里暖气片往上冒热气，猫趴在旁边，温度计往上升。演变讲规律：说一件事的词，常拿来叫做这件事用的东西
P = {'style': 'core', 'board': True, 'distinguish': False, 'fengong': False}
STOVE = ['art/stove_f0.svg', 'art/stove_f1.svg']
THERMO = ['art/thermometer_f%d.svg' % k for k in range(4)]
SLEEP = ['art/cat-sleep_f0.svg', 'art/cat-sleep_f1.svg']
def stove(x, y, s, **kw):
    d = {'svg': STOVE[0], 'frames': STOVE, 'fps': 4, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 2}
    d.update(kw); return d
def steam(x, y, **kw):
    d = {'emit': True, 'svg': 'art/steam.svg', 'x': x, 'y': y, 's': 0.16, 'to': [0.0, -0.2], 'life': 2.0, 'every': 0.8, 'wobble': 0.03, 'z': 4}
    d.update(kw); return d
def heat_waves(x, y, **kw):   # 暖气片往上冒的热气
    d = {'waves': True, 'x': x, 'y': y, 'dir': -90, 'spread': 70, 'n': 3, 'period': 1.4, 'r0': 0.02, 'r1': 0.16, 'lw': 0.012, 'color': '#F28C28', 'z': 4}
    d.update(kw); return d
def warm_room(sw=0.5, hx=0.68, hs=0.3, **kw):
    out = [{'svg': 'art/snowwin.svg', 'x': 0.28, 'y': 0.42, 's': sw, 'z': 1},
           {'svg': 'art/heater.svg', 'x': hx, 'y': 0.78, 's': hs, 'z': 2}, heat_waves(hx, 0.6),
           {'svg': SLEEP[0], 'frames': SLEEP, 'fps': 0.8, 'seq': 'pingpong', 'x': hx + 0.02, 'y': 0.94, 's': hs * 0.55, 'z': 3},
           {'svg': THERMO[0], 'frames': THERMO, 'fps': 0.8, 'seq': 'loop', 'x': 0.92, 'y': 0.36, 's': 0.36, 'z': 2}]
    for d in out: d.update(kw)
    return out
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/kitchen-bg.svg', 'items': [stove(0.5, 0.72, 0.5), steam(0.5, 0.48),
        {'label': '加热 heat', 'x': 0.5, 'y': 0.1, 'size': 0.1, 'when': '加热', 'z': 6}]},
    'p1': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [actor('west-woman-read', x=0.5, y=waist(0.9), s=0.9, z=2),
        {'label': 'reading：读书这件事', 'x': 0.5, 'y': 0.1, 'size': 0.075, 'when': '这件事', 'z': 6}]}}
P['icons'] = {'p0': 'art/icon-flame.svg', 'p1': 'art/icon-ing.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/kitchen-bg.svg', 'items': [stove(0.5, 0.72, 0.56), steam(0.5, 0.44),
    {'sound': 'sizzle', 'delay': 0.4},
    {'label': '加热这件事', 'x': 0.5, 'y': 0.1, 'size': 0.1, 'delay': 0.6, 'z': 6}]}
# ======== 意思
W, H = 537, 356
pic0 = {'text': '加热', 'pos': '名词', 'diff': '让东西变热这件事', 'bg': 'blank', 'img': 'art/kitchen-bg.svg', 'items': [stove(0.5, 0.72, 0.5), steam(0.5, 0.46)]}
pic1 = {'text': '供暖、暖气', 'pos': '名词', 'diff': '冬天给屋子加热的那一套设备', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': warm_room()}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/kitchen-bg.svg', 'items': [
    stove(0.5, 0.72, 0.56, when='Heating', cue=0, fade=0.3), steam(0.5, 0.42, when='milk', cue=0),
    {'svg': 'art/clock_f0.svg', 'frames': ['art/clock_f0.svg', 'art/clock_f1.svg'], 'fps': 1, 'seq': 'loop', 'x': 0.84, 'y': 0.26, 's': 0.26, 'when': 'minutes', 'cue': 0, 'z': 3},
    {'sound': 'tick', 'when': 'minutes', 'cue': 0, 'times': 3, 'every': 0.5},
    {'label': '加热', 'x': 0.18, 'y': 0.16, 'size': 0.075, 'when': '加热', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/snowwin.svg', 'x': 0.2, 'y': 0.42, 's': 0.62, 'z': 1},
    {'svg': 'art/heater.svg', 'x': 0.56, 'y': 0.78, 's': 0.34, 'z': 2}, heat_waves(0.56, 0.58, when='on', cue=0),
    {'svg': THERMO[0], 'frames': THERMO, 'fps': 0.8, 'seq': 'loop', 'x': 0.94, 'y': 0.36, 's': 0.4, 'when': 'warm', 'cue': 0, 'z': 2},
    actor('cn-girl-warm', x=0.8, y=waist(0.9), s=0.9, z=3, when='warm', cue=0, fade=0.4),
    {'sound': 'click', 'when': 'on', 'cue': 0},
    {'label': '暖气', 'x': 0.56, 'y': 0.2, 'size': 0.075, 'when': '暖气', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'Heating the milk takes two minutes.', 'exzh': '把牛奶加热要两分钟。', 'exPic': ex0})
pic1.update({'ex': 'The heating is on, so the room is warm.', 'exzh': '暖气开着，所以屋里很暖和。', 'exPic': ex1})
P['pics'] = [pic0, pic1]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/kitchen-bg.svg', 'items': [stove(0.5, 0.72, 0.46), steam(0.5, 0.48),
    {'label': '加热 + 这件事', 'x': 0.5, 'y': 0.1, 'size': 0.075, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/kitchen-bg.svg', 'items': [stove(0.5, 0.74, 0.46, when='变热'), steam(0.5, 0.5, when='变热'),
    {'label': '加热', 'x': 0.5, 'y': 0.1, 'size': 0.075, 'when': '加热', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6},
    {'label': '名词', 'x': 0.5, 'y': 0.24, 'size': 0.06, 'when': '名词', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/snowwin.svg', 'x': 0.28, 'y': 0.42, 's': 0.46, 'when': '冬天', 'z': 1},
    {'sound': 'wind', 'when': '冬天'},
    {'svg': 'art/heater.svg', 'x': 0.68, 'y': 0.78, 's': 0.3, 'when': '管子', 'z': 2}, heat_waves(0.68, 0.6, when='管子'),
    {'label': '做这件事用的东西', 'x': 0.5, 'y': 0.08, 'size': 0.06, 'when': '用的东西', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6},
    {'label': '供暖、暖气', 'x': 0.68, 'y': 0.4, 'size': 0.07, 'when': '暖气', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
P['flow'] = [
    {'node': '“加热这件事”', 'fig': fig0},
    {'via': '让东西变热', 'node': '① 加热', 'pos': '名词', 'pic': 0, 'fig': fig1,
     'say': ['让东西变热，这件事就是加热。它说的是一件事，所以是名词。']},
    {'via': '冬天给屋子加热用的设备', 'node': '② 供暖、暖气', 'pos': '名词', 'pic': 1, 'fig': fig2,
     'rule': '说一件事的词，常拿来叫做这件事用的东西', 'ruleEx': 'heating 加热 → 暖气      cover 盖 → 盖子',
     'say': ['英语里，说一件事的词，常拿来叫做这件事用的东西。', '冬天给屋子一直加热的那一套管子、锅炉，也叫 heating，就是供暖、暖气。']}]
P['extend'] = ['heat', 'overheat', 'heatwave', 'hot']
json.dump({'heating': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

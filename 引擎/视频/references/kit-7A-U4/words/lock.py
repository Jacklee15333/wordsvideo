import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/lock/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
P = {'style': 'core', 'board': True}
LATCH = ['art/latch_f0.svg', 'art/latch_f1.svg', 'art/latch_f2.svg']
KEY = ['art/key_f0.svg', 'art/key_f1.svg', 'art/key_f2.svg']
WATER = ['art/water_f%d.svg' % i for i in range(4)]
def latch(x, y, s, **kw):
    d = {'svg': LATCH[0], 'frames': LATCH, 'fps': 1.5, 'seq': 'pingpong', 'x': x, 'y': y, 's': s, 'z': 2}; d.update(kw); return d
def canal_lock(boat_y0=0.6, **kw):     # 闸室里的水一点点涨、船跟着往上升
    it = [{'svg': WATER[0], 'frames': WATER, 'fps': 0.8, 'seq': 'loop', 'x': 0.5, 'y': 0.72, 's': 0.4, 'z': 1},
          {'svg': 'art/boat.svg', 'x': 0.5, 'y': boat_y0, 's': 0.16, 'go': [0.5, boat_y0 - 0.1], 'dur': 5.0, 'loop': True, 'z': 2}]
    for d in it: d.update(kw)
    return it
# ======== 来历：门闩（一根木插销滑进铁环里）
W, H = 537, 356
P['originPic'] = {'bg': 'blank', 'img': 'art/door-bg.svg', 'items': [latch(0.5, 0.52, 0.62), {'sound': 'click', 'delay': 1.2},
    {'label': '门闩 loc', 'x': 0.5, 'y': 0.1, 'size': 0.09, 'delay': 0.5, 'z': 6}]}
# ======== 意思
pic0 = {'text': '锁', 'pos': '名词', 'diff': '锁住门、箱子的东西', 'bg': 'blank', 'img': 'art/door-bg.svg', 'items': [
    {'svg': 'art/padlock.svg', 'x': 0.5, 'y': 0.55, 's': 0.5, 'anim': 'sway', 'z': 2},
    {'svg': KEY[0], 'frames': KEY, 'fps': 1.5, 'seq': 'pingpong', 'x': 0.78, 'y': 0.72, 's': 0.25, 'z': 3}]}
pic1 = {'text': '船闸', 'pos': '名词', 'diff': '运河上拦住水、能开能关的闸门', 'bg': 'blank', 'img': 'art/canal-bg.svg', 'items': canal_lock()}
pic2 = {'text': '锁上', 'pos': '动词', 'diff': '用锁把门、箱子关住', 'bg': 'blank', 'img': 'art/door-bg.svg', 'items': [
    actor('cn-girl-lock', x=0.36, y=waist(0.95), s=0.95, z=3)]}
pic3 = {'text': '卡住、固定住', 'pos': '动词', 'diff': '东西卡住，动不了', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/drawer.svg', 'x': 0.66, 'y': 0.72, 's': 0.42, 'anim': 'sway', 'z': 1},
    actor('cn-boy-pull', x=0.28, y=waist(0.9), s=0.9, z=2)]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/door-bg.svg', 'items': [
    {'svg': 'art/padlock.svg', 'x': 0.5, 'y': 0.55, 's': 0.55, 'z': 2},
    {'svg': KEY[0], 'frames': KEY, 'fps': 1.5, 'seq': 'pingpong', 'x': 0.5, 'y': 0.78, 's': 0.22, 'when': 'key', 'cue': 0, 'z': 3},
    {'sound': 'keys', 'when': 'key', 'cue': 0},
    {'label': '锁', 'x': 0.68, 'y': 0.2, 'size': 0.08, 'when': '锁', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/canal-bg.svg', 'items': canal_lock() + [
    {'sound': 'water', 'when': 'waiting', 'cue': 0},
    {'label': '船闸', 'x': 0.5, 'y': 0.12, 'size': 0.08, 'when': '船闸', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex2 = {'bg': 'blank', 'img': 'art/door-bg.svg', 'items': [
    actor('cn-girl-lock', x=0.36, y=waist(0.98), s=0.98, z=3),
    {'sound': 'click', 'when': 'lock', 'cue': 0},
    {'label': '锁上', 'x': 0.7, 'y': 0.2, 'size': 0.08, 'when': '锁上', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex3 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/drawer.svg', 'x': 0.62, 'y': 0.74, 's': 0.44, 'anim': 'sway', 'z': 1},
    actor('cn-boy-pull', x=0.3, y=waist(0.95), s=0.95, z=2),
    {'sound': 'thud', 'when': 'could not', 'cue': 0},
    {'label': '卡住了', 'x': 0.62, 'y': 0.2, 'size': 0.08, 'when': '卡住', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'The key is in the lock.', 'exzh': '钥匙插在锁里。', 'exPic': ex0})
pic1.update({'ex': 'The boat is waiting in the lock.', 'exzh': '船正在船闸里等着。', 'exPic': ex1})
pic2.update({'ex': 'Please lock the door when you leave.', 'exzh': '你走的时候请把门锁上。', 'exPic': ex2})
pic3.update({'ex': 'The drawer locked, and I could not open it.', 'exzh': '抽屉卡住了，我打不开。', 'exPic': ex3})
P['pics'] = [pic0, pic1, pic2, pic3]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/door-bg.svg', 'items': [latch(0.5, 0.5, 0.6), {'label': '门闩、屏障', 'x': 0.5, 'y': 0.12, 'size': 0.075, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/door-bg.svg', 'items': [
    latch(0.6, 0.45, 0.5, when='插销'),
    actor('west-man-push', x=0.2, y=waist(0.85), s=0.85, z=3, when='推不开'),
    {'label': '推不开', 'x': 0.6, 'y': 0.12, 'size': 0.07, 'when': '推不开', 'z': 6},
    {'svg': 'art/padlock.svg', 'x': 0.78, 'y': 0.72, 's': 0.3, 'when': '锁', 'cue': 1, 'fade': 0.4, 'z': 3},
    {'label': '锁', 'x': 0.78, 'y': 0.45, 'size': 0.07, 'when': '锁', 'cue': 1, 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/door-bg.svg', 'items': [
    {'svg': 'art/padlock-open.svg', 'frames': ['art/padlock-open.svg', 'art/padlock.svg'], 'fps': 1.0, 'seq': 'loop', 'x': 0.4, 'y': 0.58, 's': 0.5, 'z': 3},
    {'label': '动词：锁上', 'x': 0.78, 'y': 0.15, 'size': 0.07, 'when': '锁上', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig3 = {'bg': 'blank', 'img': 'art/canal-bg.svg', 'items': canal_lock(when='闸门') + [
    {'label': '拦住水、能开能关', 'x': 0.5, 'y': 0.12, 'size': 0.065, 'when': '拦住水', 'z': 6},
    {'label': '船闸', 'x': 0.5, 'y': 0.26, 'size': 0.07, 'when': '船闸', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6}]}
fig4 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/drawer.svg', 'x': 0.62, 'y': 0.72, 's': 0.4, 'anim': 'sway', 'when': '卡住', 'z': 1},
    {'label': '像被锁住一样', 'x': 0.62, 'y': 0.15, 'size': 0.065, 'when': '像被锁住', 'z': 6}]}
P['distinguish'] = False
P['flow'] = [
    {'node': '“门闩、屏障”', 'fig': fig0},
    {'via': '插销滑进孔里，门就推不开了', 'node': '① 锁', 'pos': '名词', 'pic': 0, 'fig': fig1,
     'say': ['以前的门，是一根插销滑进孔里，门就推不开了。', '能把门、箱子关住的东西，就是锁。它说的是一样东西，所以是名词。']},
    {'via': '用锁把门关住', 'node': '③ 锁上', 'pos': '动词', 'pic': 2, 'fig': fig2,
     'rule': '英语里，表示东西的词，常常直接当动词用，说用这样东西做事', 'ruleEx': 'lock 锁 → 锁上      water 水 → 浇水',
     'say': ['英语里，表示东西的词，常常直接当动词用，说用这样东西做事。', '用锁把门关住，就是锁上，这是动词。']},
    {'from': 0, 'via': '河道上拦住水、能开能关的闸门', 'node': '② 船闸', 'pos': '名词', 'pic': 1, 'fig': fig3,
     'say': ['河道上也有一道道闸门，能拦住水，能开能关，这就是船闸。']},
    {'from': 1, 'via': '东西动不了，像被锁住一样', 'node': '④ 卡住、固定住', 'pos': '动词', 'pic': 3, 'fig': fig4,
     'say': ['东西卡住了、动不了，像被锁住一样，也叫 lock。']}]
json.dump({'lock': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

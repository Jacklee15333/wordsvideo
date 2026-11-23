import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/suggest/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.29.2：15 suggest（水墨写意风）。sug- 从下面：箱子从下面递上搁板；gest 搬、带：拖着箱子走的人；
# 建议：女孩头上灯泡亮了提主意；表明：乌云表明要下雨；联想到：一朵云让人联想到小狗。辨析 suggest / advise / propose
P = {'style': 'core', 'board': True}
BULB = ['art/bulb_f0.svg', 'art/bulb_f1.svg']
CLOUD = ['art/darkcloud_f0.svg', 'art/darkcloud_f1.svg']
BIRD = ['art/bird_f0.svg', 'art/bird_f1.svg']
def lift(x, y0, y1, s, **kw):   # 箱子从下面往上递
    d = {'svg': 'art/box.svg', 'x': x, 'y': y0, 's': s, 'go': [x, y1], 'dur': 1.4, 'loop': True, 'z': 3}
    d.update(kw); return d
def bulb_on(x, y, s, **kw):
    d = {'svg': BULB[1], 'frames': BULB, 'fps': 1.6, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 5}
    d.update(kw); return d
def clouds(y=0.18, s=0.26, **kw):
    out = []
    for k, (x0, x1) in enumerate(((1.15, 0.62), (1.35, 0.3))):
        d = {'svg': CLOUD[k], 'frames': CLOUD, 'fps': 0.8, 'seq': 'pingpong', 'x': x0, 'y': y + 0.04 * k, 's': s, 'go': [x1, y + 0.04 * k], 'dur': 2.4 + k, 'z': 4}
        d.update(kw); out.append(d)
    return out
def rain(**kw):
    d = {'emit': True, 'svg': 'art/streak.svg', 'x': 0.5, 'y': 0.3, 'spreadX': 0.8, 's': 0.06, 'to': [-0.02, 0.6], 'life': 0.9, 'every': 0.06, 'z': 5}
    d.update(kw); return d
def strollers(s=0.3, y=0.99):   # 公园里散步的人（中外都有）
    return [walker('walk-cn-girl', y, s, -0.1, 1.1, 0.2, z=1), walker('walk-west-boy-pack', y, s * 0.95, 1.1, -0.1, 0.6, z=1)]
def birds(y=0.22, **kw):
    out = []
    for k in range(2):
        d = {'svg': BIRD[0], 'frames': BIRD, 'fps': 6, 'seq': 'loop', 'x': -0.05, 'y': y + 0.06 * k, 's': 0.05, 'go': [1.05, y - 0.04 + 0.06 * k], 'dur': 6.0 + k, 'loop': True, 'delay': 1.2 * k, 'z': 4}
        d.update(kw); out.append(d)
    return out
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [         # sug- 从下面：箱子从下面递到搁板上（不放人）
        {'svg': 'art/shelf.svg', 'x': 0.5, 'y': 0.3, 's': 0.24, 'z': 1},
        lift(0.5, 0.86, 0.46, 0.2), {'svg': 'art/up-arrow.svg', 'x': 0.82, 'y': 0.62, 's': 0.3, 'anim': 'sway', 'z': 4},
        {'label': '从下面', 'x': 0.5, 'y': 0.1, 'size': 0.1, 'when': '从下面', 'z': 6}]},
    'p1': {'bg': 'blank', 'img': 'art/station-bg.svg', 'items': [      # gest 搬、带：拖着箱子走的人
        walker('walk-west-man-case', 0.98, 0.62, -0.1, 1.1, 0.0, z=2), walker('walk-cn-teacher-case', 0.98, 0.56, 1.1, -0.1, 0.5, z=1),
        {'label': '搬、带 gest', 'x': 0.5, 'y': 0.1, 'size': 0.1, 'when': '搬', 'z': 6}]}}
P['icons'] = {'p0': 'art/icon-up.svg', 'p1': 'art/icon-carry.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/shelf.svg', 'x': 0.5, 'y': 0.26, 's': 0.3, 'z': 1},
    lift(0.5, 0.9, 0.42, 0.26), {'svg': 'art/up-arrow.svg', 'x': 0.78, 'y': 0.6, 's': 0.36, 'anim': 'sway', 'z': 4},
    {'sound': 'whoosh', 'delay': 0.4},
    {'label': '从下面搬上来', 'x': 0.5, 'y': 0.08, 'size': 0.1, 'delay': 0.6, 'z': 6}]}
# ======== 意思
W, H = 537, 356
pic0 = {'text': '建议、提议', 'pos': '动词', 'diff': '把想法递到别人面前，供他考虑', 'bg': 'blank', 'img': 'art/park-bg.svg', 'items': strollers(0.26) + [
    actor('cn-girl-idea', id='g', x=0.3, y=waist(0.84), s=0.84, z=2), bulb_on(0.3, 0.16, 0.2),
    actor('west-boy-nod', x=0.72, y=waist(0.8), s=0.8, z=2, nodWith='g')]}
pic1 = {'text': '暗示、表明', 'pos': '动词', 'diff': '不明说，却让人看出来', 'bg': 'blank', 'img': 'art/park-bg.svg', 'items': clouds() + strollers(0.26) + [
    rain(delay=2.6), {'label': '要下雨了', 'x': 0.5, 'y': 0.86, 'size': 0.08, 'delay': 2.4, 'z': 6}]}
pic2 = {'text': '使人联想到', 'pos': '动词', 'diff': '看到这个，就想到那个', 'bg': 'blank', 'img': 'art/park-bg.svg', 'items': birds() + strollers(0.26) + [
    {'svg': 'art/dogcloud.svg', 'x': 0.5, 'y': 0.24, 's': 0.3, 'go': [0.56, 0.24], 'dur': 3.0, 'loop': True, 'z': 3},
    {'label': '像一只小狗', 'x': 0.5, 'y': 0.86, 'size': 0.08, 'delay': 1.0, 'z': 6}]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': strollers(0.34) + [
    actor('cn-girl-idea', id='g', x=0.3, y=waist(0.98), s=0.98, z=2, turn=[0, 2]),
    {'svg': BULB[0], 'x': 0.3, 'y': 0.12, 's': 0.22, 'hideWhen': 'suggest', 'hideCue': 0, 'z': 5},
    bulb_on(0.3, 0.12, 0.22, when='suggest', cue=0),
    actor('west-boy-nod', x=0.66, y=waist(0.9), s=0.9, z=2, nodWith='g'),
    {'sound': 'ding', 'when': 'suggest', 'cue': 0},
    {'label': '建议', 'x': 0.86, 'y': 0.16, 'size': 0.075, 'when': '建议', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': clouds(0.2, 0.32, when='clouds', cue=0) + strollers(0.34) + [
    rain(when='rain', cue=0),
    {'sound': 'thunder', 'cue': 0, 'gap': True},
    {'label': '表明：要下雨了', 'x': 0.5, 'y': 0.86, 'size': 0.075, 'when': '表明', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex2 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': birds(0.3) + strollers(0.34) + [
    {'svg': 'art/dogcloud.svg', 'x': 0.5, 'y': 0.3, 's': 0.42, 'when': 'cloud', 'cue': 0, 'fade': 0.6, 'z': 3},
    {'sound': 'dog', 'cue': 0, 'gap': True},
    {'label': '联想到一只小狗', 'x': 0.5, 'y': 0.86, 'size': 0.075, 'when': '联想', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'I suggest going to the park this weekend.', 'exzh': '我建议这个周末去公园。', 'exPic': ex0})
pic1.update({'ex': 'The dark clouds suggest that it will rain.', 'exzh': '乌云表明要下雨了。', 'exPic': ex1})
pic2.update({'ex': 'The shape of the cloud suggests a dog.', 'exzh': '这朵云的形状让人联想到一只小狗。', 'exPic': ex2})
P['pics'] = [pic0, pic1, pic2]
# ======== 同义词辨析：suggest / advise / propose
W, H = 537, 356
P['distinguish'] = {'key': '建议', 'items': [
    {'w': 'suggest', 'gloss': '建议', 'note': '随口提个主意，后面接 doing 或 that 从句', 'ex': 'I suggest going home.',
     'pic': {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': strollers(0.26) + [actor('west-girl-idea', id='g', x=0.3, y=waist(0.84), s=0.84, z=2), bulb_on(0.3, 0.16, 0.2),
                                                                 actor('cn-boy-nod', x=0.72, y=waist(0.8), s=0.8, z=2, nodWith='g')]}},
    {'w': 'advise', 'gloss': '劝告、建议', 'note': '懂行的人劝你该怎么做，可以说 advise somebody to do', 'ex': 'The doctor advised me to rest.',
     'pic': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [actor('doc-advise', id='d', x=0.3, y=waist(0.88), s=0.88, z=2, turn=[0, 2]),
                                                                actor('cn-boy-sick', x=0.72, y=waist(0.8), s=0.8, z=2, nodWith='d')]}},
    {'w': 'propose', 'gloss': '提议', 'note': '比 suggest 正式，常在会上正式提出，供大家讨论', 'ex': 'propose a new plan',
     'pic': {'bg': 'blank', 'img': 'art/stage-bg.svg', 'items': [actor('west-man-present', x=0.5, y=waist(0.9), s=0.9, z=2)]}}],
    'tip': 'suggest 提个主意，advise 劝你怎么做，propose 正式提出。记住：suggest doing，不说 suggest somebody to do。'}
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/shelf.svg', 'x': 0.5, 'y': 0.28, 's': 0.22, 'z': 1},
    lift(0.5, 0.86, 0.44, 0.18), {'svg': 'art/up-arrow.svg', 'x': 0.8, 'y': 0.6, 's': 0.3, 'anim': 'sway', 'z': 4},
    {'label': '从下面 + 搬', 'x': 0.5, 'y': 0.08, 'size': 0.075, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': strollers(0.26) + [
    {'svg': 'art/box.svg', 'x': 0.86, 'y': 0.62, 's': 0.12, 'go': [0.86, 0.42], 'dur': 1.2, 'when': '递上去', 'z': 3},
    {'label': '递上去', 'x': 0.86, 'y': 0.3, 'size': 0.055, 'when': '递上去', 'z': 6},
    actor('west-girl-idea', id='g', x=0.28, y=waist(0.8), s=0.8, z=2, when='想法'), bulb_on(0.28, 0.2, 0.18, when='想法'),
    actor('cn-boy-nod', x=0.74, y=waist(0.76), s=0.76, z=2, nodWith='g', when='递到'),
    {'label': '递东西 → 递想法', 'x': 0.5, 'y': 0.08, 'size': 0.06, 'when': '抽象', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6},
    {'label': '建议', 'x': 0.5, 'y': 0.22, 'size': 0.07, 'when': '建议', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6},
    {'label': '动词', 'x': 0.5, 'y': 0.34, 'size': 0.06, 'when': '动词', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': clouds(when='乌云') + strollers(0.26) + [
    rain(when='下雨'), {'sound': 'wind', 'when': '乌云'},
    {'label': '要下雨了', 'x': 0.5, 'y': 0.86, 'size': 0.07, 'when': '下雨', 'z': 6},
    {'label': '表明', 'x': 0.5, 'y': 0.72, 'size': 0.07, 'when': '表明', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig3 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': birds() + strollers(0.26) + [
    {'svg': 'art/dogcloud.svg', 'x': 0.5, 'y': 0.26, 's': 0.34, 'when': '云', 'fade': 0.6, 'z': 3},
    {'label': '悄悄递到心里', 'x': 0.5, 'y': 0.62, 'size': 0.06, 'when': '悄悄', 'z': 6},
    {'label': '联想到小狗', 'x': 0.5, 'y': 0.86, 'size': 0.07, 'when': '小狗', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
P['flow'] = [
    {'node': '“从下面搬上来”', 'fig': fig0},
    {'via': '把想法递到别人面前', 'node': '① 建议、提议', 'pos': '动词', 'pic': 0, 'fig': fig1,
     'rule': '说具体动作的词，常拿来说抽象的事', 'ruleEx': 'suggest 递东西 → 递想法：建议      see 看见 → 明白',
     'say': ['从下面搬上来，就是把东西递上去，送到对方手边。', '英语里，说具体动作的词，常拿来说抽象的事。',
             '把一个想法递到别人面前，供他考虑，就是建议、提议。它说的是一个动作，所以是动词。']},
    {'from': 1, 'via': '把结论递到你眼前', 'node': '② 暗示、表明', 'pos': '动词', 'pic': 1, 'fig': fig2,
     'say': ['乌云不会说话，却把一个结论递到你眼前：要下雨了。这就是暗示、表明。']},
    {'from': 2, 'via': '把想法悄悄递到心里', 'node': '③ 使人联想到', 'pos': '动词', 'pic': 2, 'fig': fig3,
     'say': ['不明说，只把想法悄悄递到人心里，就是使人联想到。', '比如天上的一朵云，让人联想到一只小狗。']}]
P['extend'] = ['suggestion', 'digest', 'gesture', 'register']
P['fengong'] = False   # 精简版不讲前缀辨析
json.dump({'suggest': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

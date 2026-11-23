import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/bathroom/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.29.2：14 bathroom（水墨写意风）。音节表里没有这个词：没有读音拆分。浴缸冒泡泡、冒热气；教室里男孩举手问能不能去卫生间；
# 演变讲用词规律：不好直说的事，常换一个委婉的说法
P = {'style': 'core', 'board': True}
def tub(x, y, s, **kw):
    d = {'svg': 'art/bathtub.svg', 'x': x, 'y': y, 's': s, 'z': 2}
    d.update(kw); return d
def bubbles(x, y, **kw):   # 泡泡一个个往上飘
    d = {'emit': True, 'svg': 'art/bubble.svg', 'x': x, 'y': y, 's': 0.05, 'to': [0.02, -0.22], 'life': 1.6, 'every': 0.35, 'wobble': 0.04, 'z': 4}
    d.update(kw); return d
def steam(x, y, **kw):
    d = {'emit': True, 'svg': 'art/steam.svg', 'x': x, 'y': y, 's': 0.16, 'to': [0.0, -0.18], 'life': 2.2, 'every': 0.9, 'wobble': 0.03, 'z': 4}
    d.update(kw); return d
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [        # bath 洗澡：浴缸里满是泡泡（不放人）
        tub(0.5, 0.74, 0.46), bubbles(0.46, 0.58), steam(0.62, 0.52),
        {'label': '洗澡 bath', 'x': 0.5, 'y': 0.12, 'size': 0.1, 'when': '洗澡', 'z': 6}]},
    'p1': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [           # room 房间：一间屋子的空间
        {'svg': 'art/space-arrows.svg', 'x': 0.5, 'y': 0.62, 's': 0.42, 'delay': 1.0, 'fade': 0.5, 'z': 3},
        {'svg': 'art/box.svg', 'x': 0.5, 'y': 0.8, 's': 0.22, 'go': [0.14, 0.82], 'dur': 1.0, 'delay': 0.2, 'z': 4},
        {'label': '房间 room', 'x': 0.5, 'y': 0.12, 'size': 0.1, 'when': '房间', 'z': 6}]}}
P['icons'] = {'p0': 'art/icon-bath.svg', 'p1': 'art/icon-room.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [
    tub(0.5, 0.76, 0.5), bubbles(0.46, 0.6), steam(0.64, 0.54),
    {'sound': 'water', 'delay': 0.4},
    {'label': '洗澡的房间', 'x': 0.5, 'y': 0.12, 'size': 0.1, 'delay': 0.6, 'z': 6}]}
# ======== 意思
W, H = 537, 356
pic0 = {'text': '浴室', 'pos': '名词', 'diff': '洗澡的房间', 'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [
    tub(0.42, 0.76, 0.44), bubbles(0.4, 0.62), steam(0.56, 0.56)]}
pic1 = {'text': '卫生间、厕所', 'pos': '名词', 'diff': '（美）客气地说厕所', 'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    {'svg': 'art/wc-sign.svg', 'x': 0.84, 'y': 0.2, 's': 0.16, 'z': 2},
    actor('cn-boy-raise', id='b', x=0.32, y=waist(0.9), s=0.9, z=2),
    actor('west-man-smile', x=0.72, y=waist(0.84), s=0.84, z=1, nodWith='b')]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [
    tub(0.5, 0.76, 0.52, when='bathtub', cue=0, fade=0.4), bubbles(0.46, 0.6, when='bathtub', cue=0), steam(0.62, 0.52, when='bathtub', cue=0),
    {'sound': 'pop', 'when': 'bathtub', 'cue': 0, 'times': 3, 'every': 0.25},
    {'label': '浴室', 'x': 0.16, 'y': 0.16, 'size': 0.075, 'when': '浴室', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    {'svg': 'art/wc-sign.svg', 'x': 0.88, 'y': 0.2, 's': 0.18, 'when': 'bathroom', 'cue': 0, 'fade': 0.3, 'z': 2},
    actor('cn-boy-raise', id='b', x=0.3, y=waist(0.98), s=0.98, z=2, turn=[0, 2]),
    actor('west-man-smile', x=0.66, y=waist(0.9), s=0.9, z=1, nodWith='b'),
    {'sound': 'footsteps', 'cue': 0, 'gap': True},
    {'label': '卫生间', 'x': 0.88, 'y': 0.42, 'size': 0.075, 'when': '卫生间', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'There is a big bathtub in the bathroom.', 'exzh': '浴室里有一个大浴缸。', 'exPic': ex0})
pic1.update({'ex': 'May I go to the bathroom, please?', 'exzh': '我可以去一下卫生间吗？', 'exPic': ex1})
P['pics'] = [pic0, pic1]
# ======== 同义词辨析：bathroom / toilet
W, H = 537, 356
P['distinguish'] = {'key': '卫生间', 'items': [
    {'w': 'bathroom', 'gloss': '卫生间', 'note': '洗澡的房间，美国人家里说上厕所也客气地说 bathroom', 'ex': 'May I use your bathroom?',
     'pic': {'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [tub(0.42, 0.76, 0.44), bubbles(0.4, 0.62), steam(0.56, 0.56)]}},
    {'w': 'toilet', 'gloss': '厕所', 'note': '英国人日常说厕所，美国人多指马桶本身', 'ex': 'a public toilet',
     'pic': {'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [
         {'svg': 'art/toilet.svg', 'x': 0.5, 'y': 0.66, 's': 0.6, 'z': 2},
         {'svg': 'art/drop.svg', 'x': 0.3, 'y': 0.5, 's': 0.05, 'go': [0.3, 0.62], 'dur': 1.0, 'loop': True, 'z': 3},
         {'label': '马桶', 'x': 0.78, 'y': 0.3, 'size': 0.08, 'delay': 0.4, 'z': 6}]}}],
    'logic': 'bathroom 本来是洗澡的房间，拿它说厕所是委婉的说法；toilet 是直说厕所、马桶。'}
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [
    tub(0.5, 0.76, 0.44), bubbles(0.46, 0.62), steam(0.62, 0.56),
    {'label': '洗澡 + 房间', 'x': 0.5, 'y': 0.12, 'size': 0.075, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [
    tub(0.42, 0.78, 0.44, when='浴缸'), bubbles(0.4, 0.64, when='浴缸'), steam(0.56, 0.58, when='洗澡'),
    {'sound': 'water', 'when': '洗澡'},
    {'label': '浴缸', 'x': 0.2, 'y': 0.5, 'size': 0.06, 'when': '浴缸', 'z': 6},
    {'label': '浴室', 'x': 0.5, 'y': 0.12, 'size': 0.075, 'when': '浴室', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6},
    {'label': '名词', 'x': 0.5, 'y': 0.26, 'size': 0.06, 'when': '名词', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [
    {'svg': 'art/toilet.svg', 'x': 0.74, 'y': 0.7, 's': 0.42, 'when': '马桶', 'z': 3},
    {'svg': 'art/drop.svg', 'x': 0.3, 'y': 0.46, 's': 0.04, 'go': [0.3, 0.58], 'dur': 1.0, 'loop': True, 'when': '洗手池', 'z': 3},
    {'sound': 'drip', 'when': '洗手池'},
    {'svg': 'art/wc-sign.svg', 'x': 0.5, 'y': 0.3, 's': 0.2, 'when': '卫生间', 'z': 5},
    {'label': '不好直说', 'x': 0.25, 'y': 0.1, 'size': 0.06, 'when': '不好直说', 'z': 6},
    {'label': '委婉的说法', 'x': 0.72, 'y': 0.1, 'size': 0.06, 'when': '委婉', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6}]}
P['flow'] = [
    {'node': '“洗澡的房间”', 'fig': fig0},
    {'via': '放浴缸、用来洗澡的屋子', 'node': '① 浴室', 'pos': '名词', 'pic': 0, 'fig': fig1,
     'say': ['家里放浴缸、淋浴，用来洗澡的那间屋子，就是浴室。它说的是一个地方，所以是名词。']},
    {'via': '不好直说厕所，就说洗澡的房间', 'node': '② 卫生间、厕所', 'pos': '名词', 'pic': 1, 'fig': fig2,
     'rule': '不好直说的事，常换一个委婉的说法', 'ruleEx': 'bathroom 浴室 → 厕所      depart 离开 → 去世',
     'say': ['浴室里也装着马桶、洗手池。', '英语里，不好直说的事，常换一个委婉的说法。', '美国人不好直说厕所，就说洗澡的房间，这就是卫生间、厕所。']}]
P['extend'] = ['bath', 'bedroom', 'classroom']
json.dump({'bathroom': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

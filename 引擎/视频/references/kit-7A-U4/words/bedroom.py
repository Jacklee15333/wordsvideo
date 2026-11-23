import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/bedroom/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.29.2：13 bedroom（水墨写意风）。音节表里没有这个词：没有读音拆分。讲床、讲房间、讲卧室都不放人：床上睡着一只猫，床头钟在走，窗帘被风吹动
P = {'style': 'core', 'board': True}
SLEEP = ['art/cat-sleep_f0.svg', 'art/cat-sleep_f1.svg']
OPEN = ['art/window-open_f%d.svg' % k for k in range(3)]
CLOCK = ['art/clock_f0.svg', 'art/clock_f1.svg']
def cat(x, y, s, **kw):
    d = {'svg': SLEEP[0], 'frames': SLEEP, 'fps': 0.8, 'seq': 'pingpong', 'x': x, 'y': y, 's': s, 'z': 3}
    d.update(kw); return d
def zs(x, y, **kw):   # 睡着了，头上飘出“Z”
    d = {'emit': True, 'svg': 'art/zzz.svg', 'x': x, 'y': y, 's': 0.07, 'to': [0.06, -0.2], 'life': 1.8, 'every': 0.9, 'wobble': 0.02, 'z': 5}
    d.update(kw); return d
def clock(x, y, s, **kw):
    d = {'svg': CLOCK[0], 'frames': CLOCK, 'fps': 1, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 3}
    d.update(kw); return d
def window_open(x, y, s, **kw):
    d = {'svg': OPEN[0], 'frames': OPEN, 'fps': 3, 'seq': 'pingpong', 'x': x, 'y': y, 's': s, 'z': 2}
    d.update(kw); return d
def bed_set(bx=0.42, by=0.78, bs=0.42, nx=0.84):
    return [{'svg': 'art/bed.svg', 'x': bx, 'y': by, 's': bs, 'z': 1},
            {'svg': 'art/nightstand.svg', 'x': nx, 'y': by + 0.06, 's': bs * 0.5, 'z': 1},
            clock(nx, by - bs * 0.2, bs * 0.3)]
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': bed_set(0.42, 0.8, 0.5, 0.86) + [
        cat(0.42, 0.62, 0.22), zs(0.5, 0.52),
        {'label': '床 bed', 'x': 0.5, 'y': 0.12, 'size': 0.1, 'when': '床', 'z': 6}]},
    'p1': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [        # room 空间：把箱子推到一边，腾出地方
        {'svg': 'art/space-arrows.svg', 'x': 0.5, 'y': 0.62, 's': 0.42, 'delay': 1.0, 'fade': 0.5, 'z': 3},
        {'svg': 'art/box.svg', 'x': 0.5, 'y': 0.8, 's': 0.22, 'go': [0.86, 0.82], 'dur': 1.0, 'delay': 0.2, 'z': 4},
        {'label': '空间 room', 'x': 0.5, 'y': 0.12, 'size': 0.1, 'when': '空间', 'z': 6}]}}
P['icons'] = {'p0': 'art/icon-bed.svg', 'p1': 'art/icon-room.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': bed_set(0.4, 0.82, 0.55, 0.84) + [
    cat(0.4, 0.62, 0.24), zs(0.48, 0.5),
    {'label': '放床的空间', 'x': 0.5, 'y': 0.12, 'size': 0.1, 'delay': 0.6, 'z': 6}]}
# ======== 意思
W, H = 537, 356
pic0 = {'text': '卧室', 'pos': '名词', 'diff': '睡觉的房间', 'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': bed_set() + [
    cat(0.42, 0.62, 0.2), zs(0.5, 0.52)]}
pic1 = {'text': '卧室的', 'pos': '形容词', 'diff': '放在名词前：卧室里的', 'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': [
    window_open(0.5, 0.48, 0.74),
    {'label': 'bedroom window', 'x': 0.5, 'y': 0.92, 'size': 0.07, 'delay': 0.6, 'z': 6}]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': bed_set(0.45, 0.82, 0.5, 0.75) + [
    cat(0.45, 0.6, 0.24, when='cat', cue=0, fade=0.4), zs(0.52, 0.48, when='sleeping', cue=0),
    {'sound': 'purr', 'when': 'sleeping', 'cue': 0},
    {'label': '卧室', 'x': 0.2, 'y': 0.16, 'size': 0.075, 'when': '卧室', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': [
    window_open(0.5, 0.5, 0.86, hideWhen='close', hideCue=0),
    {'svg': 'art/window-closed.svg', 'x': 0.5, 'y': 0.5, 's': 0.86, 'when': 'close', 'cue': 0, 'fade': 0.3, 'z': 3},
    {'sound': 'click', 'when': 'close', 'cue': 0},
    {'label': '卧室的窗户', 'x': 0.2, 'y': 0.16, 'size': 0.075, 'when': '窗户', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'The cat is sleeping in my bedroom.', 'exzh': '猫在我的卧室里睡觉。', 'exPic': ex0})
pic1.update({'ex': 'Please close the bedroom window.', 'exzh': '请把卧室的窗户关上。', 'exPic': ex1})
P['pics'] = [pic0, pic1]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': bed_set(0.42, 0.8, 0.45, 0.84) + [
    cat(0.42, 0.62, 0.2), zs(0.5, 0.52),
    {'label': '床 + 空间', 'x': 0.5, 'y': 0.12, 'size': 0.075, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': bed_set(0.42, 0.8, 0.45, 0.84) + [
    cat(0.3, 0.62, 0.18), zs(0.38, 0.52),
    {'svg': 'art/space-arrows.svg', 'x': 0.52, 'y': 0.6, 's': 0.12, 'when': '空位', 'z': 4},
    {'label': '床上的空位', 'x': 0.6, 'y': 0.4, 'size': 0.06, 'when': '空位', 'z': 6},
    {'sound': 'tick', 'when': '屋子', 'times': 3, 'every': 0.5},
    {'label': '放床的屋子：卧室', 'x': 0.5, 'y': 0.12, 'size': 0.07, 'when': '屋子', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6},
    {'label': '名词', 'x': 0.5, 'y': 0.26, 'size': 0.06, 'when': '名词', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': [
    window_open(0.5, 0.5, 0.7, when='窗户'),
    {'sound': 'wind', 'when': '窗户'},
    {'label': '放在名词前面', 'x': 0.5, 'y': 0.08, 'size': 0.06, 'when': '名词前面', 'z': 6},
    {'label': 'bedroom window 卧室的窗户', 'x': 0.5, 'y': 0.93, 'size': 0.06, 'when': '窗户', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6}]}
P['flow'] = [
    {'node': '“放床的空间”', 'fig': fig0},
    {'via': '睡觉的地方 → 放床的屋子', 'node': '① 卧室', 'pos': '名词', 'pic': 0, 'fig': fig1,
     'say': ['最早，莎士比亚用它说床上的空位、睡觉的地方。', '后来就指放床的那间屋子，就是卧室。它说的是一个地方，所以是名词。']},
    {'via': '放在别的名词前面', 'node': '② 卧室的', 'pos': '形容词', 'pic': 1, 'fig': fig2,
     'rule': '名词放在另一个名词前面，就当形容词用', 'ruleEx': 'bedroom window 卧室的窗户      school bag 书包',
     'say': ['英语里，名词放在另一个名词前面，就当形容词用。', '所以 bedroom 放在名词前面，就是卧室的，比如卧室的窗户。']}]
P['extend'] = ['bedside', 'classroom', 'roommate']
P['distinguish'] = False
json.dump({'bedroom': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

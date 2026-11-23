import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/explore/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
P = {'style': 'core', 'board': True}
BIRD = ['art/bird_f0.svg', 'art/bird_f1.svg']
def birds_out(x, y, n=3, **kw):    # 鸟一只只从林子里飞出去
    out = []
    for k in range(n):
        d = {'svg': BIRD[0], 'frames': BIRD, 'fps': 6, 'seq': 'loop', 'x': x, 'y': y + 0.04 * k, 's': 0.06, 'go': [x + 0.35 + 0.05 * k, y - 0.3 + 0.05 * k], 'dur': 2.4, 'loop': True, 'delay': 0.5 * k, 'z': 4}
        d.update(kw); out.append(d)
    return out
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': birds_out(0.3, 0.55) + [
        {'ray': [[0.3, 0.6], [0.75, 0.3]], 'arrow': True, 'color': '#C2410C', 'lw': 0.02, 'dur': 0.6, 'when': '向外', 'z': 6},
        {'label': '向外', 'x': 0.7, 'y': 0.12, 'size': 0.1, 'when': '向外', 'z': 6}]},
    'p1': {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
        actor('cn-boy-raise', id='h', x=0.45, y=waist(0.9), s=0.9, z=2), mouth_waves('h', 1, delay=0.2, r1=0.22),
        {'sound': 'say:Hey! Hey!', 'when': '大声喊'},
        {'label': '大声喊', 'x': 0.75, 'y': 0.12, 'size': 0.1, 'when': '大声喊', 'z': 6}]}}
P['icons'] = {'p0': 'art/icon-ex.svg', 'p1': 'art/icon-plor.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    actor('west-man-call', id='h', x=0.25, y=waist(0.9), s=0.9, z=2), mouth_waves('h', 1, delay=0.2, r1=0.2)] + birds_out(0.45, 0.5) + [
    {'sound': 'bird', 'delay': 0.8}]}
W, H = 537, 356
pic0 = {'text': '探索、探险', 'pos': '动词', 'diff': '走进陌生的地方，四处看看', 'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    actor('west-woman-look', x=0.3, y=waist(0.95), s=0.95, z=2),
    actor('cn-boy-hike', x=0.74, y=waist(0.85), s=0.85, z=2, nodWith='w0'),
    {'id': 'w0', 'sound': 'wind', 'delay': 0.3}] + birds_out(0.5, 0.25, 2)}
pic1 = {'text': '仔细研究、探讨', 'pos': '动词', 'diff': '把一个问题翻来覆去地看', 'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    {'svg': 'art/leaf.svg', 'x': 0.5, 'y': 0.8, 's': 0.22, 'anim': 'sway', 'z': 3},
    actor('cn-girl-study', id='g', x=0.3, y=waist(0.9), s=0.9, z=2),
    actor('west-boy-think', x=0.76, y=waist(0.85), s=0.85, z=2, nodWith='g'),
    {'svg': 'art/class-desks.svg', 'x': 0.5, 'y': 0.98, 's': 0.22, 'z': 4}]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    actor('west-woman-look', x=0.36, y=waist(0.98), s=0.98, z=2, nodWith='b'),
    actor('cn-boy-hike', id='b', x=0.66, y=waist(0.92), s=0.92, z=2),
    {'sound': 'bird', 'when': 'forest', 'cue': 0}] + birds_out(0.45, 0.3, 3, when='forest', cue=0) + [
    {'label': '探险', 'x': 0.86, 'y': 0.15, 'size': 0.075, 'when': '探险', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    {'svg': 'art/board-q.svg', 'x': 0.52, 'y': 0.3, 's': 0.36, 'when': 'question', 'cue': 0, 'z': 1},
    actor('cn-teacher-point', id='t', x=0.22, y=waist(0.95), s=0.95, z=2),
    actor('west-boy-think', x=0.82, y=waist(0.85), s=0.85, z=2, nodWith='t'),
    {'sound': 'ding', 'when': 'question', 'cue': 0},
    {'label': '探讨', 'x': 0.66, 'y': 0.15, 'size': 0.075, 'when': '探讨', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'They explored the forest last summer.', 'exzh': '去年夏天，他们在森林里探险。', 'exPic': ex0})
pic1.update({'ex': 'We will explore this question in class.', 'exzh': '我们会在课上探讨这个问题。', 'exPic': ex1})
P['pics'] = [pic0, pic1]
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': birds_out(0.3, 0.55) + [{'label': '大声喊出来', 'x': 0.6, 'y': 0.12, 'size': 0.075, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    actor('west-man-call', id='h', x=0.22, y=waist(0.85), s=0.85, z=2, when='吆喝'), mouth_waves('h', 1, when='吆喝', r1=0.2)] + birds_out(0.4, 0.5, 3, when='轰出来') + [
    {'label': '看看林子里有什么', 'x': 0.66, 'y': 0.12, 'size': 0.062, 'when': '看看', 'z': 6},
    {'label': '仔细查看、考察', 'x': 0.66, 'y': 0.26, 'size': 0.062, 'when': '考察', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    actor('west-girl-surprised', x=0.36, y=waist(0.9), s=0.9, z=2, when='陌生的地方'),
    {'sound': 'footsteps', 'when': '陌生的地方'},
    {'label': '探索、探险', 'x': 0.75, 'y': 0.15, 'size': 0.07, 'when': '探险', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig3 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    {'svg': 'art/board-q.svg', 'x': 0.5, 'y': 0.3, 's': 0.34, 'when': '问题', 'z': 1},
    {'svg': 'art/magnifier.svg', 'x': 0.5, 'y': 0.3, 's': 0.24, 'go': [0.56, 0.36], 'dur': 1.2, 'loop': True, 'when': '翻来覆去', 'z': 2},
    {'label': '仔细研究、探讨', 'x': 0.5, 'y': 0.72, 'size': 0.07, 'when': '探讨', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6}]}
W, H = 504, 204
P['distinguish'] = {'pics': {
    'explore': {'bg': 'blank', 'items': [band('art/wild-bg.svg', 0.42, 420), actor('west-woman-look', id='w', x=0.35, y=waist(0.95), s=0.95, z=2),
                                         actor('cn-boy-hike', x=0.7, y=waist(0.85), s=0.85, z=2, nodWith='w')] + birds_out(0.5, 0.3, 2)},
    'search': {'bg': 'blank', 'items': [band('art/room-bg.svg', 0.46, 300), actor('cn-girl-study', id='g', x=0.4, y=waist(0.95), s=0.95, z=2),
                                        {'svg': 'art/leaf.svg', 'x': 0.7, 'y': 0.8, 's': 0.25, 'anim': 'sway', 'z': 3}]}},
    'tip': 'explore 是去没去过的地方看看、发现新东西；search 是仔细找一样要找的东西'}
P['flow'] = [
    {'node': '“大声喊出来”', 'fig': fig0},
    {'via': '猎人一路吆喝，把鸟兽轰出来', 'node': '仔细查看、考察', 'fig': fig1,
     'say': ['据说以前打猎，猎人一路吆喝，把林子里的鸟兽轰出来。', '看看这片林子里到底有什么，就是仔细查看、考察。']},
    {'via': '走进陌生的地方，四处看看', 'node': '① 探索、探险', 'pos': '动词', 'pic': 0, 'fig': fig2,
     'say': ['走进陌生的地方，四处看看、摸清情况，就是探索、探险。它说的是一个动作，所以是动词。']},
    {'from': 1, 'via': '把一个问题翻来覆去地看', 'node': '② 仔细研究、探讨', 'pos': '动词', 'pic': 1, 'fig': fig3,
     'say': ['把一个问题翻来覆去地查看，就是仔细研究、探讨。']}]
# 6.41（第八十五版）：辨析的演示配画（以前是自动的小图标）：画出字面意思
P['demo'] = {
    'outside': {'icons': ['🚪', '↔️'], 'lit': '外面那一边', 'pic': {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': [
        {'e': '🏠', 'x': 0.24, 'y': 0.52, 's': 0.5, 'z': 1},
        walker('walk-cn-girl', 0.96, 0.62, 1.1, 0.42, 0.0, z=2),
        {'label': '屋子外面', 'x': 0.7, 'y': 0.14, 'size': 0.13, 'delay': 0.4, 'z': 6}]}},
    'outrun': {'icons': ['⏩', '🏃'], 'lit': '跑得超过对方', 'pic': {'bg': 'park', 'items': [
        {'e': '🏃', 'x': -0.1, 'y': 0.62, 's': 0.42, 'go': [1.1, 0.62], 'dur': 3.2, 'loop': True, 'anim': 'ride', 'flip': True},
        {'e': '🏃', 'x': -0.1, 'y': 0.78, 's': 0.46, 'go': [1.1, 0.78], 'dur': 1.9, 'loop': True, 'anim': 'ride', 'flip': True},
        {'label': '跑得更快，超过去', 'x': 0.5, 'y': 0.14, 'size': 0.12, 'delay': 0.4}]}},
    'export': {'icons': ['📤', '📦'], 'lit': '搬出去', 'pic': {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': [
        {'e': '🏠', 'x': 0.22, 'y': 0.52, 's': 0.5, 'z': 1},
        {'e': '📦', 'x': 0.3, 'y': 0.72, 's': 0.26, 'go': [1.1, 0.72], 'dur': 2.4, 'loop': True, 'anim': 'ride', 'z': 3},
        {'label': '搬出去', 'x': 0.66, 'y': 0.14, 'size': 0.13, 'delay': 0.4, 'z': 6}]}},
    'effect': {'icons': ['📤', '🔨'], 'lit': '做出来的东西', 'pic': {'bg': 'plain', 'items': [
        {'e': '🔨', 'x': 0.3, 'y': 0.5, 's': 0.4, 'anim': 'pulse'},
        {'e': '🪑', 'x': 0.72, 'y': 0.58, 's': 0.46, 'anim': 'bob', 'delay': 0.8, 'fade': 0.5},
        {'label': '做出来的东西', 'x': 0.5, 'y': 0.14, 'size': 0.12, 'delay': 0.4}]}}}
json.dump({'explore': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

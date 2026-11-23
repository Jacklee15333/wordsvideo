import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/mode/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.29.2：11 mode（水墨写意风的第一个）。方式：街上走路、骑车、坐公交；模式：手机静音模式；风尚：今夏流行的大遮阳帽；众数：黑板上 3、5、5、7
# 讲东西的画不放人（手机、尺子、公交车），讲“大家都这样穿戴”才放戴帽子的人
P = {'style': 'core', 'board': True, 'distinguish': False}
CYC = ['art/cyclist_f0.svg', 'art/cyclist_f1.svg']
RING = ['art/phone-ring_f0.svg', 'art/phone-ring_f1.svg']
def cyclist(y, s, x0, x1, dur, **kw):
    d = {'svg': CYC[0], 'frames': CYC, 'fps': 6, 'seq': 'loop', 'x': x0, 'y': y, 's': s, 'go': [x1, y], 'dur': dur, 'loop': True, 'z': 4}
    d.update(kw); return d
def bus(y, s, x0, x1, dur, **kw):
    d = {'svg': 'art/bus.svg', 'x': x0, 'y': y, 's': s, 'go': [x1, y], 'dur': dur, 'loop': True, 'z': 3}
    d.update(kw); return d
def ring_phone(x, y, s, **kw):
    d = {'svg': RING[0], 'frames': RING, 'fps': 8, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 3}
    d.update(kw); return d
def board_rings(xs, y, s, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {'svg': 'art/chalkring.svg', 'x': x, 'y': y, 's': s, 'z': 4, 'delay': 0.3 * k}
        d.update(kw); out.append(d)
    return out
# ======== 来历：拉丁语 modus“量度、尺度、方式”
W, H = 537, 356
P['originPic'] = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 0.93, 's': 0.3, 'z': 1},
    {'svg': 'art/plank.svg', 'x': 0.5, 'y': 0.74, 's': 0.12, 'z': 2},
    {'svg': 'art/ruler.svg', 'x': 0.36, 'y': 0.66, 's': 0.09, 'go': [0.62, 0.66], 'dur': 2.4, 'loop': True, 'z': 3},
    {'label': 'modus：量度、尺度', 'x': 0.5, 'y': 0.14, 'size': 0.075, 'delay': 0.5, 'z': 6}]}
# ======== 意思
pic0 = {'text': '方式', 'pos': '名词', 'diff': '做事的一种做法、套路', 'bg': 'blank', 'img': 'art/street-bg.svg', 'items': [
    walker('walk-cn-girl', 0.74, 0.3, -0.1, 1.1, 0.1, z=2), walker('walk-west-man-case', 0.74, 0.32, 1.1, -0.1, 0.5, z=2),
    bus(0.83, 0.3, 1.25, -0.3, 7.0), cyclist(0.86, 0.26, -0.15, 1.15, 4.5)]}
pic1 = {'text': '模式', 'pos': '名词', 'diff': '机器按某一种套路运行，可以切换', 'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 1.0, 's': 0.36, 'z': 1},
    ring_phone(0.5, 0.52, 0.66, hide=2.2),
    {'waves': True, 'x': 0.5, 'y': 0.22, 'dir': -90, 'spread': 140, 'n': 3, 'period': 1.0, 'r0': 0.03, 'r1': 0.16, 'lw': 0.012, 'color': '#F59E0B', 'hide': 2.2, 'z': 5},
    {'svg': 'art/phone-silent.svg', 'x': 0.5, 'y': 0.52, 's': 0.66, 'delay': 2.2, 'fade': 0.2, 'z': 4},
    {'label': '静音模式', 'x': 0.8, 'y': 0.2, 'size': 0.08, 'delay': 2.4, 'z': 6}]}
pic2 = {'text': '风尚', 'pos': '名词', 'diff': '一段时间里大家都照着穿戴的样式', 'bg': 'blank', 'img': 'art/hatshop-bg.svg', 'items': [
    actor('west-woman-hat', id='w', x=0.3, y=waist(0.9), s=0.9, z=2),
    actor('cn-girl-hat', x=0.72, y=waist(0.84), s=0.84, z=2, nodWith='w')]}
pic3 = {'text': '众数', 'pos': '名词', 'diff': '一组数里出现次数最多的那个（数学）', 'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    {'svg': 'art/chalkboard.svg', 'x': 0.5, 'y': 0.42, 's': 0.62, 'z': 1},
    *board_rings((0.453, 0.6), 0.48, 0.26, delay=1.0),
    {'label': '众数 = 5', 'x': 0.5, 'y': 0.88, 'size': 0.08, 'delay': 1.6, 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': [
    walker('walk-west-woman-case', 0.86, 0.36, 1.1, -0.1, 0.3, z=2),
    bus(0.8, 0.38, 1.25, -0.25, 8.0, z=3),
    cyclist(0.86, 0.36, -0.15, 0.55, 2.4, loop=False, when='Cycling', cue=0, goWhen='Cycling', goCue=0, z=5),
    {'sound': 'ding', 'when': 'Cycling', 'cue': 0},
    {'label': '出行方式', 'x': 0.5, 'y': 0.12, 'size': 0.075, 'when': '方式', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 1.02, 's': 0.42, 'z': 1},
    ring_phone(0.5, 0.5, 0.78, hideWhen='silent'),
    {'waves': True, 'x': 0.5, 'y': 0.16, 'dir': -90, 'spread': 140, 'n': 3, 'period': 1.0, 'r0': 0.03, 'r1': 0.16, 'lw': 0.012, 'color': '#F59E0B', 'hideWhen': 'silent', 'z': 5},
    {'sound': 'phonering', 'delay': 0.1, 'vol': 0.5},
    {'svg': 'art/phone-silent.svg', 'x': 0.5, 'y': 0.5, 's': 0.78, 'when': 'silent', 'cue': 0, 'fade': 0.2, 'z': 4},
    {'sound': 'click', 'when': 'silent', 'cue': 0},
    {'label': '静音模式', 'x': 0.78, 'y': 0.2, 'size': 0.075, 'when': '静音模式', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex2 = {'bg': 'blank', 'img': 'art/hatshop-bg.svg', 'items': [
    actor('west-girl-hat', id='w', x=0.24, y=waist(0.98), s=0.98, z=2, when='hats', cue=0, fade=0.4),
    actor('cn-girl-hat', x=0.5, y=waist(0.9), s=0.9, z=2, nodWith='w', when='hats', cue=0, fade=0.4, delay=0.3),
    actor('cn-boy-hat', x=0.76, y=waist(0.86), s=0.86, z=2, nodWith='w', when='mode', cue=0, fade=0.4),
    {'sound': 'sparkle', 'when': 'mode', 'cue': 0},
    {'label': '流行、风尚', 'x': 0.5, 'y': 0.1, 'size': 0.075, 'when': '流行', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex3 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    {'svg': 'art/chalkboard.svg', 'x': 0.5, 'y': 0.45, 's': 0.7, 'z': 1},
    *board_rings((0.468, 0.552), 0.5, 0.3, when='mode', cue=0),
    {'sound': 'ding', 'when': 'mode', 'cue': 0},
    actor('cn-teacher-point', x=0.86, y=waist(0.9), s=0.9, z=2),
    {'label': '众数', 'x': 0.18, 'y': 0.16, 'size': 0.075, 'when': '众数', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'Cycling is a green mode of transport.', 'exzh': '骑自行车是一种绿色的出行方式。', 'exPic': ex0})
pic1.update({'ex': 'Please turn your phone to silent mode.', 'exzh': '请把手机调成静音模式。', 'exPic': ex1})
pic2.update({'ex': 'Big sun hats are the mode this summer.', 'exzh': '今年夏天流行大遮阳帽。', 'exPic': ex2})
pic3.update({'ex': 'In 3, 5, 5 and 7, the mode is 5.', 'exzh': '在 3、5、5、7 里，众数是 5。', 'exPic': ex3})
P['pics'] = [pic0, pic1, pic2, pic3]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 0.95, 's': 0.3, 'z': 1},
    {'svg': 'art/plank.svg', 'x': 0.5, 'y': 0.76, 's': 0.12, 'z': 2},
    {'svg': 'art/ruler.svg', 'x': 0.38, 'y': 0.68, 's': 0.09, 'go': [0.6, 0.68], 'dur': 2.4, 'loop': True, 'z': 3},
    {'label': '量一量：尺度', 'x': 0.5, 'y': 0.14, 'size': 0.075, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': [
    walker('walk-cn-girl', 0.74, 0.3, -0.1, 1.1, 0.1, z=2),
    cyclist(0.86, 0.24, -0.15, 1.15, 4.0, when='骑车'),
    bus(0.83, 0.3, 1.25, -0.3, 6.0, when='公交车'),
    {'sound': 'car', 'when': '公交车'},
    {'label': '走路', 'x': 0.2, 'y': 0.14, 'size': 0.065, 'when': '走路', 'z': 6},
    {'label': '骑车', 'x': 0.5, 'y': 0.14, 'size': 0.065, 'when': '骑车', 'z': 6},
    {'label': '坐公交', 'x': 0.8, 'y': 0.14, 'size': 0.065, 'when': '公交车', 'z': 6},
    {'label': '名词', 'x': 0.5, 'y': 0.3, 'size': 0.06, 'when': '名词', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 1.0, 's': 0.34, 'z': 1},
    ring_phone(0.5, 0.52, 0.66, hideWhen='静音模式'),
    {'waves': True, 'x': 0.5, 'y': 0.22, 'dir': -90, 'spread': 140, 'n': 3, 'period': 1.0, 'r0': 0.03, 'r1': 0.16, 'lw': 0.012, 'color': '#F59E0B', 'hideWhen': '静音模式', 'z': 5},
    {'svg': 'art/phone-silent.svg', 'x': 0.5, 'y': 0.52, 's': 0.66, 'when': '静音模式', 'fade': 0.2, 'z': 4},
    {'sound': 'click', 'when': '静音模式'},
    {'label': '几种套路，可以切换', 'x': 0.5, 'y': 0.1, 'size': 0.06, 'when': '切换', 'z': 6},
    {'label': '静音模式', 'x': 0.82, 'y': 0.3, 'size': 0.065, 'when': '静音模式', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig3 = {'bg': 'blank', 'img': 'art/hatshop-bg.svg', 'items': [
    actor('west-woman-hat2', id='w', x=0.28, y=waist(0.86), s=0.86, z=2, when='大家'),
    actor('cn-boy-hat', x=0.72, y=waist(0.8), s=0.8, z=2, nodWith='w', when='大家', delay=0.3),
    {'label': '大家都这样戴', 'x': 0.5, 'y': 0.1, 'size': 0.065, 'when': '大家', 'z': 6},
    {'label': '风尚', 'x': 0.5, 'y': 0.25, 'size': 0.07, 'when': '风尚', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig4 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    {'svg': 'art/chalkboard.svg', 'x': 0.5, 'y': 0.42, 's': 0.58, 'z': 1},
    *board_rings((0.455, 0.594), 0.47, 0.24, when='两次'),
    {'sound': 'ding', 'when': '两次'},
    {'label': '最时兴 → 出现最多', 'x': 0.5, 'y': 0.82, 'size': 0.06, 'when': '最时兴', 'z': 6},
    {'label': '众数 = 5', 'x': 0.5, 'y': 0.93, 'size': 0.065, 'when': '众数就是', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6},
    actor('cn-teacher-point', x=0.88, y=waist(0.62), s=0.62, z=3),
    {'label': '英语还是 mode', 'x': 0.2, 'y': 0.1, 'size': 0.06, 'when': '核心意思', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6}]}
P['flow'] = [
    {'node': '“量度、尺度”', 'fig': fig0},
    {'via': '做事时遵循的尺度、套路', 'node': '① 方式', 'pos': '名词', 'pic': 0, 'fig': fig1,
     'say': ['做事时遵循的一种尺度、一种套路，就是方式。', '比如出行的方式：走路、骑车、坐公交车。它说的是一种做法，所以是名词。']},
    {'from': 1, 'via': '机器按一种套路运行', 'node': '② 模式', 'pos': '名词', 'pic': 1, 'fig': fig2,
     'say': ['机器做事也有套路：按某一种套路运行，还能在几种套路之间切换，这就是模式。', '比如手机的静音模式。']},
    {'from': 1, 'via': '大家都照着穿戴的样式', 'node': '③ 风尚', 'pos': '名词', 'pic': 2, 'fig': fig3,
     'say': ['某个时候，大家都照着同一种样式穿戴，这种样式就是风尚。']},
    {'from': 3, 'via': '借用“最时兴”：出现最多的数', 'node': '④ 众数', 'pos': '名词', 'pic': 3, 'fig': fig4,
     'rule': '词的核心意思不变，换了对象、场合，中文要换个说法，英语还是这个词', 'ruleEx': 'mode 方式 → 众数      play 玩 → 踢（球）、演奏（乐器）',
     'say': ['数学里借用了“最时兴”这层意思：一组数里出现次数最多的那个，就是众数。', '三、五、五、七里，五出现了两次，众数就是五。',
             '英语里，词的核心意思不变，换了场合，中文要换个说法，英语还是这一个词。']}]
P['extend'] = ['model', 'modern', 'modify', 'modal']
json.dump({'mode': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

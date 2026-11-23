import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/remind/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.30（第七十四版）：30 remind（青绿工笔风）。画图脚本：owner,remind。两个意思都画：提醒、使想起。
# 演变照总表：使再想起来 → 提醒（让别人把忘了的事再想起来）→ 使想起（看到这个，脑子里浮出那个）。辨析 remind / remember
P = {'style': 'core', 'board': True}
def lab(t, x, y, size=0.075, **kw):
    d = {'label': t, 'x': x, 'y': y, 'size': size, 'z': 7}
    d.update(kw); return d
BLUE = {'color': '#1A66B8', 'border': '#2F95E6'}
GREEN = {'color': '#2B8A3E', 'border': '#2B8A3E'}
def rain(n=6, **kw):      # 下雨：一排雨点从上往下落
    out = []
    for i in range(n):
        d = {'emit': True, 'svg': 'art/drop.svg', 'x': 0.08 + i * 0.17, 'y': -0.05, 's': 0.035, 'to': [-0.04, 1.15], 'life': 1.1, 'every': 0.22, 'offset': 0.07 * i, 'z': 6}
        d.update(kw); out.append(d)
    return out
def strollers(y=0.8, s=0.28):
    return [walker('walk-cn-teacher-case', y, s, 1.1, -0.1, 0.0, z=1), walker('walk-west-boy-pack', y, s * 0.9, -0.1, 1.1, 0.5, z=1)]
def door_scene(ms=0.86, bs=0.8, mx=0.3, bx=0.74, **bkw):     # 下雨天，妈妈在门口把伞递给要出门的孩子（孩子听一句点一下头）
    b = actor('cn-boy-oops', x=bx, y=waist(bs), s=bs, z=3, nodWith='m')
    b.update(bkw)
    return rain() + [actor('cn-teacher-umbrella', id='m', x=mx, y=waist(ms), s=ms, z=3), b]
def memory(svg, x, y, s, **kw):
    d = {'svg': 'art/' + svg, 'x': x, 'y': y, 's': s, 'anim': 'sway', 'z': 5}
    d.update(kw); return d
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [actor('west-girl-reread', x=0.5, y=waist(0.84), s=0.84, z=3),
        lab('再 re-', 0.5, 0.1, 0.1, when='再', **BLUE)]},
    'p1': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [actor('cn-girl-recall', x=0.28, y=waist(0.86), s=0.86, z=3),
        memory('bubble-sea.svg', 0.7, 0.34, 0.46, when='记起', fade=0.3), lab('记起 mind', 0.5, 0.9, 0.09, when='记起', **BLUE)]}}
P['icons'] = {'p0': 'art/icon-re.svg', 'p1': 'art/icon-mind.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/kitchen2-bg.svg', 'items': [{'svg': 'art/fridge.svg', 'x': 0.26, 'y': 0.56, 's': 0.9, 'z': 2},
    actor('cn-boy-fridge', x=0.62, y=waist(0.96), s=0.96, z=3), memory('bubble-milk.svg', 0.84, 0.28, 0.44, delay=0.8, fade=0.3),
    {'sound': 'ding', 'delay': 0.8}, lab('使再想起来', 0.5, 0.1, 0.1, delay=0.6)]}
# ======== 意思
W, H = 537, 356
pic0 = {'text': '提醒', 'pos': '动词', 'diff': '让别人把忘了的事想起来', 'bg': 'blank', 'img': 'art/home-bg.svg', 'items': door_scene()}
pic1 = {'text': '使想起', 'pos': '动词', 'diff': '看到这个，想起那个', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('west-girl-photo', x=0.3, y=waist(0.86), s=0.86, z=3), memory('bubble-sea.svg', 0.72, 0.34, 0.5)]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/home-bg.svg', 'items': door_scene(0.94, 0.9, 0.26, 0.7) + [
    {'sound': 'rain', 'when': 'reminds', 'cue': 0}, lab('提醒我带伞', 0.5, 0.08, 0.075, when='提醒', cue=1, **BLUE)]}
ex1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [actor('west-girl-photo', x=0.28, y=waist(0.94), s=0.94, z=3),
    memory('bubble-sea.svg', 0.66, 0.36, 0.56, when='reminds', cue=0, fade=0.3),
    {'sound': 'waves', 'when': 'summer', 'cue': 0}, lab('让我想起了暑假', 0.66, 0.08, 0.075, when='想起', cue=1, **BLUE)]}
pic0.update({'ex': 'Mom reminds me to take an umbrella.', 'exzh': '妈妈提醒我带伞。', 'exPic': ex0})
pic1.update({'ex': 'This photo reminds me of the summer holiday.', 'exzh': '这张照片让我想起了暑假。', 'exPic': ex1})
P['pics'] = [pic0, pic1]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/kitchen2-bg.svg', 'items': [{'svg': 'art/fridge.svg', 'x': 0.28, 'y': 0.56, 's': 0.84, 'z': 2},
    actor('cn-boy-fridge', x=0.66, y=waist(0.88), s=0.88, z=3), memory('bubble-milk.svg', 0.82, 0.24, 0.36, delay=0.8, fade=0.3),
    lab('使再想起来', 0.5, 0.08, 0.07, delay=0.3)]}
fig1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [actor('west-boy-oh', x=0.42, y=waist(0.9), s=0.9, z=3),
    {'sound': 'notify', 'when': '提醒'}, lab('提醒', 0.16, 0.08, 0.07, when='提醒', **GREEN), lab('动词', 0.84, 0.08, 0.06, when='动词')]}
fig2 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': strollers() + [actor('cn-boy-kite', x=0.3, y=waist(0.84), s=0.84, z=3),
    memory('bubble-kite.svg', 0.72, 0.3, 0.5, when='浮出', fade=0.3), lab('使想起', 0.5, 0.08, 0.07, when='使想起', **GREEN)]}
P['flow'] = [
    {'node': '“使再想起来”', 'fig': fig0},
    {'via': '让别人把忘了的事再想起来', 'node': '① 提醒', 'pos': '动词', 'pic': 0, 'fig': fig1,
     'say': ['让别人把忘了的事再想起来，就是提醒。它说的是动作，所以是动词。']},
    {'via': '看到这个，脑子里浮出那个', 'node': '② 使想起', 'pos': '动词', 'pic': 1, 'fig': fig2,
     'say': ['看到一个人、一样东西，脑子里浮出另一个，就是使想起。']}]
P['extend'] = ['mind', 'reminder', 'mindful']
# ======== 同义词辨析：remind / remember
W, H = 504, 204
P['distinguish'] = {'key': '想起', 'items': [
    {'w': 'remind', 'gloss': '提醒、使想起', 'note': '让别人想起来', 'ex': 'Remind me to call him.',
     'pic': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [actor('west-boy-oh', x=0.5, y=waist(0.96), s=0.96, z=3)]}},
    {'w': 'remember', 'gloss': '记得', 'note': '自己记得', 'ex': 'Remember to call him.',
     'pic': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [actor('west-girl-remember', x=0.5, y=waist(0.96), s=0.96, z=3)]}}],
    'tip': 'remember 是自己记得；remind 是让别人想起。'}
json.dump({'remind': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

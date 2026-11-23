import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/manage/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.30（第七十四版）：29 manage（青绿工笔风）。画图脚本：explore,manage。三个意思都画：管理经营、设法做到、应付得了。
# 演变照总表：驾驭、训练马 → 掌控、操持 → 管理、经营 → 设法做到；应付得了。辨析 manage to do / try to do（中考常考：做成了 / 只是努力去做）
P = {'style': 'core', 'board': True, 'fengong': False}
POT = ['art/pottery_f0.svg', 'art/pottery_f1.svg']; HORSE = ['art/horse_f0.svg', 'art/horse_f1.svg']; FLAG = ['art/pennant_f0.svg', 'art/pennant_f1.svg']
def lab(t, x, y, size=0.075, **kw):
    d = {'label': t, 'x': x, 'y': y, 'size': size, 'z': 7}
    d.update(kw); return d
BLUE = {'color': '#1A66B8', 'border': '#2F95E6'}
GREEN = {'color': '#2B8A3E', 'border': '#2B8A3E'}
def horse(x, y, s, to=None, dur=2.4, **kw):     # 小跑的马；写了 to 就在 x 和 to 之间来回跑
    d = {'svg': HORSE[0], 'frames': HORSE, 'fps': 4, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 3}
    if to is not None:
        d.update({'go': [to, y], 'dur': dur, 'loop': True})
    d.update(kw); return d
def paddock(fy=0.86, fs=0.3):
    return [{'svg': 'art/fence.svg', 'x': 0.5, 'y': fy, 's': fs, 'z': 1}]
def flag(x, y, s, **kw):
    d = {'svg': FLAG[0], 'frames': FLAG, 'fps': 2.5, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 2}
    d.update(kw); return d
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [{'svg': POT[0], 'frames': POT, 'fps': 4, 'seq': 'loop', 'x': 0.5, 'y': 0.58, 's': 0.7, 'z': 2},
        lab('手 man', 0.5, 0.1, 0.1, when='手', **BLUE)]},
    'p1': {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': paddock() + [horse(0.64, 0.66, 0.46), actor('west-man-trainer', x=0.2, y=waist(0.8), s=0.8, z=4),
        lab('-age 行为、状态', 0.5, 0.08, 0.08, when='行为', **BLUE), lab('用手摆弄、驾驭', 0.5, 0.92, 0.08, when='驾驭', **GREEN)]}}
P['icons'] = {'p0': 'art/icon-man.svg', 'p1': 'art/icon-age.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': paddock(0.88, 0.34) + [horse(0.4, 0.62, 0.5, to=0.78, dur=2.6),
    actor('west-man-trainer2', x=0.14, y=waist(0.96), s=0.96, z=4), {'sound': 'footsteps', 'delay': 0.4},
    lab('用手摆弄、驾驭', 0.56, 0.12, 0.1, delay=0.6)]}
# ======== 意思
W, H = 537, 356
pic0 = {'text': '管理、经营', 'pos': '动词', 'diff': '把一个家、一家店打理好', 'bg': 'blank', 'img': 'art/bookshop-bg.svg', 'items': [
    actor('cn-teacher-shop2', id='m', x=0.28, y=waist(0.86), s=0.86, z=3), actor('west-boy-books', x=0.74, y=waist(0.84), s=0.84, z=3, nodWith='m')]}
pic1 = {'text': '设法做到', 'pos': '动词', 'diff': '难事最后办成了', 'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    flag(0.7, 0.42, 0.5), actor('cn-boy-top', x=0.36, y=waist(0.86), s=0.86, z=3)]}
pic2 = {'text': '应付得了', 'pos': '动词', 'diff': '难事落到手上也拿得下', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('west-boy-help', id='h', x=0.76, y=waist(0.82), s=0.82, z=2), actor('cn-girl-boxes', x=0.34, y=waist(0.92), s=0.92, z=3, nodWith='h')]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/bookshop-bg.svg', 'items': [
    actor('cn-teacher-shop2', id='m', x=0.26, y=waist(0.94), s=0.94, z=3),
    actor('west-boy-books', x=0.72, y=waist(0.92), s=0.92, z=3, nodWith='m', when='manages', cue=0, fade=0.3),
    {'sound': 'cash', 'when': 'bookshop', 'cue': 0}, lab('经营', 0.5, 0.08, 0.075, when='经营', cue=1, **BLUE)]}
ex1 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    actor('cn-boy-top', x=0.34, y=waist(0.94), s=0.94, z=3), flag(0.66, 0.42, 0.56, when='top', cue=0, fade=0.3),
    {'sound': 'applause', 'when': 'top', 'cue': 0}, lab('爬上了山顶', 0.66, 0.08, 0.075, when='爬上了山顶', cue=1, **BLUE)]}
ex2 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('west-boy-help', id='h', x=0.74, y=waist(0.9), s=0.9, z=2, when='heavy', cue=0, fade=0.3),
    actor('cn-girl-boxes', x=0.32, y=waist(0.96), s=0.96, z=3, nodWith='h'),
    {'sound': 'thud', 'when': 'heavy', 'cue': 0}, lab('应付得了', 0.5, 0.08, 0.075, when='应付得了', cue=1, **BLUE)]}
pic0.update({'ex': 'My aunt manages a small bookshop.', 'exzh': '我姑姑经营着一家小书店。', 'exPic': ex0})
pic1.update({'ex': 'He managed to climb to the top.', 'exzh': '他终于爬上了山顶。', 'exPic': ex1})
pic2.update({'ex': 'The boxes are heavy, but I can manage.', 'exzh': '箱子很重，但我应付得了。', 'exPic': ex2})
P['pics'] = [pic0, pic1, pic2]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': paddock(0.88, 0.3) + [horse(0.36, 0.64, 0.46, to=0.78, dur=2.6),
    actor('west-man-trainer', x=0.16, y=waist(0.84), s=0.84, z=4), lab('驾驭、训练马', 0.5, 0.08, 0.07, delay=0.3)]}
fig1 = {'bg': 'blank', 'img': 'art/bookshop-bg.svg', 'items': [actor('cn-teacher-point', x=0.5, y=waist(0.9), s=0.9, z=3),
    lab('掌控', 0.2, 0.08, 0.065, when='掌控'), lab('管理、经营', 0.5, 0.08, 0.07, when='管理', **GREEN), lab('动词', 0.84, 0.08, 0.06, when='动词')]}
fig2 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [flag(0.72, 0.42, 0.5), actor('west-girl-top', x=0.36, y=waist(0.86), s=0.86, z=3),
    lab('办成了', 0.5, 0.08, 0.07, when='办成了', **GREEN)]}
fig3 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [actor('west-woman-boxes', x=0.5, y=waist(0.92), s=0.92, z=3),
    lab('拿得下', 0.2, 0.08, 0.065, when='拿得下'), lab('应付得了', 0.6, 0.08, 0.07, when='应付得了', **GREEN)]}
P['flow'] = [
    {'node': '“驾驭、训练马”', 'fig': fig0},
    {'via': '握在手里打理', 'node': '① 管理、经营', 'pos': '动词', 'pic': 0, 'fig': fig1,
     'say': ['驯马师手握缰绳，让烈马听话；后来，凡是握在手里掌控的事都这样说。', '把一个家、一家店握在手里打理，就是管理、经营。它说的是动作，所以是动词。']},
    {'via': '难事最后办成了', 'node': '② 设法做到', 'pos': '动词', 'pic': 1, 'fig': fig2,
     'say': ['事情难，手上有办法，最后还是办成了，就是设法做到。']},
    {'via': '难事也拿得下', 'node': '③ 应付得了', 'pos': '动词', 'pic': 2, 'fig': fig3,
     'say': ['难事落到手上，也拿得下，就是应付得了。']}]
P['extend'] = ['manual', 'manner', 'manufacture']
# ======== 同义词辨析：manage to do / try to do
W, H = 504, 204
P['distinguish'] = {'key': '设法做', 'items': [
    {'w': 'manage', 'gloss': '设法做成', 'note': '费了劲，最后做成了', 'ex': 'manage to do',
     'pic': {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [flag(0.72, 0.42, 0.56), actor('west-girl-top', x=0.36, y=waist(0.96), s=0.96, z=3)]}},
    {'w': 'try', 'gloss': '尽力去做', 'note': '努力去做，不一定成功', 'ex': 'try to do',
     'pic': {'bg': 'blank', 'img': 'art/bookshop-bg.svg', 'items': [actor('west-girl-try', x=0.5, y=waist(0.96), s=0.96, z=3)]}}],
    'tip': 'manage to do 是做成了；try to do 只是努力去做，不一定成功。'}
json.dump({'manage': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

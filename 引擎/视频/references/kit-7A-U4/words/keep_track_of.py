import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/keep_track_of/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.30（第七十四版）：23 keep track of（图画书风）。画图脚本：street,explore,mode,ktrack。音节表里没有这个词组：没有读音拆分。
# 起草后跑 tools/fixsay.py：总表里 of 没写意思，配音会念成“单词是 of，of。”，改成“表示‘…的’”。讲踪迹的画不放人
P = {'style': 'core', 'board': True, 'distinguish': False}
RAB = ['art/rabbit_f0.svg', 'art/rabbit_f1.svg']; CHK = ['art/checklist_f%d.svg' % k for k in range(4)]
def lab(t, x, y, size=0.075, **kw):
    d = {'label': t, 'x': x, 'y': y, 'size': size, 'z': 7}
    d.update(kw); return d
BLUE = {'color': '#1A66B8', 'border': '#2F95E6'}
GREEN = {'color': '#2B8A3E', 'border': '#2B8A3E'}
def trail(x0, y0, x1, y1, n=6, s=0.08, t0=0.3, dt=0.35, **kw):     # 一串小爪印，一个接一个出来
    out = []
    for i in range(n):
        f = i / (n - 1)
        d = {'svg': 'art/paw.svg', 'x': x0 + (x1 - x0) * f + (0.012 if i % 2 else -0.012), 'y': y0 + (y1 - y0) * f + (0.015 if i % 2 else -0.015),
             's': s * (1 - 0.3 * f), 'delay': t0 + i * dt, 'fade': 0.2, 'z': 2}
        d.update(kw); out.append(d)
    return out
def rabbit(x, y, s, **kw):
    d = {'svg': RAB[0], 'frames': RAB, 'fps': 2, 'seq': 'pingpong', 'x': x, 'y': y, 's': s, 'z': 3}
    d.update(kw); return d
def notebook(x, y, s, **kw):      # 作业清单一项项打勾
    d = {'svg': CHK[0], 'frames': CHK, 'fps': 0.8, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 3}
    d.update(kw); return d
def desk_boy(W_, H_, bx=0.28, nx=0.68, ns=0.6, who='cn-boy-write', **nkw):
    return [{'svg': 'art/desk.svg', 'x': 0.5, 'y': 1.02 - 0.16, 's': 0.32, 'z': 1},
            actor(who, x=bx, y=waist(0.86), s=0.86, z=2), notebook(nx, 0.5, ns, **nkw)]
def leaves(x=0.5, y=-0.05, **kw):     # 林子里飘下来的树叶（画面要动）
    d = {'emit': True, 'svg': 'art/leaf.svg', 'x': x, 'y': y, 's': 0.06, 'to': [0.12, 0.5], 'life': 3.2, 'every': 0.9, 'wobble': 0.03, 'z': 4}
    d.update(kw); return d
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
        {'svg': 'art/quiet-sign.svg', 'x': 0.5, 'y': 0.2, 's': 0.24, 'z': 2},
        actor('cn-girl-quiet', x=0.5, y=waist(0.78), s=0.78, z=3),
        lab('保持 keep', 0.5, 0.9, 0.09, when='保持', **BLUE)]},
    'p1': {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': trail(0.14, 0.9, 0.86, 0.6, s=0.12) + [leaves(0.3), leaves(0.7, offset=0.45),
        lab('踪迹 track', 0.5, 0.1, 0.09, when='踪迹', **BLUE)]},
    'p2': {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': trail(0.1, 0.92, 0.6, 0.72, n=5, s=0.11) + [
        rabbit(0.8, 0.66, 0.36, delay=1.6, fade=0.3),
        lab('兔子的踪迹', 0.5, 0.1, 0.09, delay=1.8, **BLUE)]}}
P['icons'] = {'p0': 'art/icon-keep.svg', 'p1': 'art/icon-track.svg', 'p2': 'art/icon-of.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [actor('west-man-track', x=0.2, y=waist(0.96), s=0.96, z=3)] +
    trail(0.38, 0.95, 0.9, 0.7, s=0.13, t0=0.2, dt=0.25) + [lab('一直盯着踪迹', 0.6, 0.12, 0.1, delay=0.6)]}
# ======== 意思
W, H = 537, 356
pic0 = {'text': '记录、掌握…的情况', 'pos': '动词', 'diff': '把进展、数字一直记着', 'bg': 'blank', 'img': 'art/room-bg.svg',
        'items': desk_boy(W, H)}
pic1 = {'text': '留意、跟踪', 'pos': '动词', 'diff': '一直盯着它在哪儿', 'bg': 'blank', 'img': 'art/street-bg.svg', 'items': [
    walker('walk-west-woman-case', 0.97, 0.4, 1.1, -0.1, 0.0, z=1), walker('walk-cn-teacher-case', 0.97, 0.4, -0.1, 1.1, 0.5, z=1),
    actor('cn-girl-map', x=0.42, y=waist(0.88), s=0.88, z=3)]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 0.86, 's': 0.32, 'z': 1},
    actor('west-girl-write', x=0.3, y=waist(0.92), s=0.92, z=2),
    notebook(0.64, 0.5, 0.66, when='keep', cue=0, fade=0.3),
    {'sound': 'click', 'when': 'homework', 'cue': 0},
    lab('记着', 0.64, 0.1, 0.075, when='记着', cue=1, **BLUE)]}
ex1 = {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': [
    walker('walk-cn-boy-pack', 0.98, 0.42, 1.1, -0.1, 0.0, z=1), walker('walk-west-man-case', 0.98, 0.44, -0.1, 1.1, 0.45, z=1),
    {'svg': 'art/bus.svg', 'x': -0.25, 'y': 0.78, 's': 0.34, 'go': [0.74, 0.78], 'dur': 2.6, 'when': 'bus', 'cue': 0, 'z': 2},
    {'sound': 'car', 'when': 'bus', 'cue': 0},
    actor('cn-girl-map', x=0.28, y=waist(0.96), s=0.96, z=3),
    lab('跟踪', 0.28, 0.1, 0.075, when='跟踪', cue=1, **BLUE)]}
pic0.update({'ex': 'I keep track of my homework in a small notebook.', 'exzh': '我用一个小本子记着我的作业。', 'exPic': ex0})
pic1.update({'ex': 'My phone keeps track of the bus.', 'exzh': '我的手机一直跟踪着这辆公交车。', 'exPic': ex1})
P['pics'] = [pic0, pic1]
# ======== 意思怎么变过来（先“跟踪”，再“记录、掌握情况”）
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': trail(0.12, 0.92, 0.88, 0.62, n=7, s=0.1) + [leaves(0.25), leaves(0.65, offset=0.45), lab('一直跟着踪迹', 0.5, 0.1, 0.07, delay=0.4)]}
fig1 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [actor('west-man-track', x=0.22, y=waist(0.84), s=0.84, z=3)] +
    trail(0.4, 0.94, 0.78, 0.7, n=5, s=0.1, t0=0.2) + [
    rabbit(0.88, 0.62, 0.26, when='猎物', fade=0.3),
    {'sound': 'footsteps', 'when': '脚印'},
    lab('跟着脚印', 0.56, 0.1, 0.065, when='脚印'),
    lab('跟踪', 0.22, 0.1, 0.07, when='跟踪', **GREEN), lab('动词', 0.86, 0.1, 0.06, when='动词')]}
fig2 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': desk_boy(W, H, bx=0.26, nx=0.7, ns=0.58, who='cn-boy-check') + [
    {'sound': 'ding', 'when': '心里有数'},
    lab('进展、数字', 0.7, 0.08, 0.06, when='进展'),
    lab('记录、掌握情况', 0.3, 0.08, 0.06, when='记录', **GREEN)]}
P['flow'] = [
    {'node': '“一直跟着踪迹”', 'fig': fig0},
    {'via': '猎人一路跟着脚印走', 'node': '② 留意、跟踪', 'pos': '动词', 'pic': 1, 'fig': fig1,
     'say': ['猎人一路跟着脚印走，一直不跟丢猎物。', '这就是跟踪、留意。它说的是动作，所以是动词。']},
    {'via': '跟着的变成一件事的进展、数字', 'node': '① 记录、掌握…的情况', 'pos': '动词', 'pic': 0, 'fig': fig2,
     'say': ['后来，跟着的不再是脚印，而是一件事的进展、一个个数字。', '一直记着，心里有数，这就是记录、掌握情况。']}]
P['extend'] = ['tracker', 'tracking', 'tracksuit']
json.dump({'keep track of': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

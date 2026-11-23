import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/itself/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.28 试样：画里放不放人看内容（讲猫、讲房间就不放人；讲“自己”才画照镜子的男孩）；挑 5 处配音效
P = {'style': 'core', 'board': True}
LICK = ['art/cat-lick_f%d.svg' % i for i in range(4)]
SIT = ['art/cat-sit_f%d.svg' % i for i in range(3)]
def cat(x, y, s, lick=True, **kw):
    d = {'svg': (LICK if lick else SIT)[0], 'frames': LICK if lick else SIT, 'fps': 2.2 if lick else 1.2, 'seq': 'pingpong' if lick else 'loop', 'x': x, 'y': y, 's': s, 'z': 2}
    d.update(kw); return d
def back_arrow(cx, cy, r, **kw):   # 绕回来的箭头：动作落回到它自己身上
    import math
    pts = [[cx + r * math.cos(math.radians(a)), cy - r * 1.3 * math.sin(math.radians(a))] for a in range(200, -100, -20)]
    d = {'ray': pts, 'arrow': True, 'color': '#C2410C', 'lw': 0.012, 'dur': 0.8, 'z': 6}; d.update(kw); return d
def shine(x0, x1, y0, y1, **kw):   # 屋里亮晶晶：很干净（几处一闪一闪的星星，错开时间）
    out = []
    for k, (u, v) in enumerate(((0.12, 0.3), (0.42, 0.75), (0.68, 0.2), (0.9, 0.62), (0.3, 0.55))):
        d = {'emit': True, 'svg': 'art/star.svg', 'x': x0 + (x1 - x0) * u, 'y': y0 + (y1 - y0) * v, 's': 0.11, 'to': [0.01, -0.04], 'life': 1.1,
             'every': 1.1, 'offset': k * 0.22, 'wobble': 0.0, 'spin': 0.8, 'z': 5}
        d.update(kw); out.append(d)
    return out
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [        # 它：屋里坐着的猫（不用放人）
        {'svg': 'art/cushion.svg', 'x': 0.5, 'y': 0.9, 's': 0.2, 'z': 1}, cat(0.5, 0.66, 0.56, lick=False),
        {'svg': 'art/yarn.svg', 'x': 0.86, 'y': 0.9, 's': 0.13, 'anim': 'sway', 'z': 2},
        {'sound': 'meow', 'when': '它'},
        {'label': '它 it', 'x': 0.5, 'y': 0.16, 'size': 0.1, 'when': '它', 'z': 6}]},
    'p1': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [        # 自己：男孩指着镜子里的自己（这里要有人）
        {'svg': 'art/mirror.svg', 'x': 0.72, 'y': 0.55, 's': 0.8, 'z': 1},
        actor('cn-boy-self', x=0.26, y=waist(0.85), s=0.85, z=2),
        {'sound': 'sparkle', 'when': '自己'},
        {'label': '自己 self', 'x': 0.5, 'y': 0.1, 'size': 0.09, 'when': '自己', 'z': 6}]}}
P['icons'] = {'p0': 'art/icon-it.svg', 'p1': 'art/icon-self.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/cushion.svg', 'x': 0.5, 'y': 0.92, 's': 0.2, 'z': 1}, cat(0.5, 0.66, 0.56),
    back_arrow(0.5, 0.42, 0.14, delay=0.5),
    {'label': '它自己', 'x': 0.82, 'y': 0.2, 'size': 0.1, 'delay': 0.8, 'z': 6}]}
# ======== 意思
W, H = 537, 356
pic0 = {'text': '它自己', 'pos': '代词', 'diff': '动作落回到“它”身上', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/cushion.svg', 'x': 0.5, 'y': 0.92, 's': 0.16, 'z': 1}, cat(0.5, 0.68, 0.58),
    back_arrow(0.5, 0.44, 0.1, delay=0.6),
    {'svg': 'art/yarn.svg', 'x': 0.82, 'y': 0.9, 's': 0.1, 'anim': 'sway', 'z': 2}]}
pic1 = {'text': '本身', 'pos': '代词', 'diff': '放在名词后面：就是这个，不是别的', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    *shine(0.1, 0.9, 0.3, 0.8),
    {'label': '房间本身', 'x': 0.5, 'y': 0.16, 'size': 0.09, 'delay': 0.5, 'z': 6}]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/cushion.svg', 'x': 0.5, 'y': 0.93, 's': 0.18, 'z': 1},
    cat(0.5, 0.68, 0.62, lick=False, hideWhen='washing'), cat(0.5, 0.68, 0.62, when='washing', cue=0),
    back_arrow(0.5, 0.42, 0.06, when='itself', cue=0),
    {'svg': 'art/yarn.svg', 'x': 0.78, 'y': 0.9, 's': 0.12, 'anim': 'sway', 'z': 2},
    {'sound': 'meow', 'cue': 0, 'gap': True},                         # 念完英文那一句，猫叫一声（draft 自动在这一句后面多停一秒）
    {'label': '自己', 'x': 0.64, 'y': 0.22, 'size': 0.075, 'when': '自己', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'label': '房间本身不大', 'x': 0.36, 'y': 0.15, 'size': 0.07, 'when': 'itself', 'cue': 0, 'z': 7},
    *shine(0.15, 0.85, 0.35, 0.85, when='clean', cue=0),
    {'sound': 'sparkle', 'when': 'clean', 'cue': 0},
    {'label': '很干净', 'x': 0.66, 'y': 0.15, 'size': 0.07, 'when': '干净', 'cue': 1, 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 7}]}
pic0.update({'ex': 'The cat is washing itself.', 'exzh': '猫在给自己洗脸。', 'exPic': ex0})
pic1.update({'ex': 'The room itself is small, but it is very clean.', 'exzh': '房间本身不大，但很干净。', 'exPic': ex1})
P['pics'] = [pic0, pic1]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/cushion.svg', 'x': 0.5, 'y': 0.92, 's': 0.18, 'z': 1}, cat(0.5, 0.66, 0.52, lick=False),
    {'label': '它 + 自己', 'x': 0.5, 'y': 0.12, 'size': 0.075, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/cushion.svg', 'x': 0.5, 'y': 0.92, 's': 0.18, 'z': 1}, cat(0.5, 0.66, 0.56, when='舔毛'),
    cat(0.5, 0.66, 0.56, lick=False, hideWhen='舔毛'),
    {'sound': 'lick', 'when': '舔毛'},
    back_arrow(0.5, 0.36, 0.12, when='落回'),
    {'label': '动作落回到它身上', 'x': 0.5, 'y': 0.1, 'size': 0.065, 'when': '落回', 'z': 6},
    {'label': '代词', 'x': 0.86, 'y': 0.3, 'size': 0.07, 'when': '代词', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    *shine(0.1, 0.9, 0.35, 0.85, when='本身'),
    {'label': '名词 + itself', 'x': 0.5, 'y': 0.14, 'size': 0.07, 'when': '名词后面', 'z': 6},
    {'label': '就是这个东西，不是别的', 'x': 0.5, 'y': 0.3, 'size': 0.06, 'when': '不是别的', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6}]}
P['flow'] = [
    {'node': '“它 + 自己”', 'fig': fig0},
    {'via': '动作落回到“它”身上', 'node': '① 它自己', 'pos': '代词', 'pic': 0, 'fig': fig1,
     'say': ['一个动作，又落回到它自己身上。', '比如猫舔毛，舔的就是它自己。', '这时 itself 就是它自己，它是代词。']},
    {'from': 0, 'via': '放在名词后面，强调就是这个', 'node': '② 本身', 'pos': '代词', 'pic': 1, 'fig': fig2,
     'say': ['它还能放在名词后面，起强调作用。', '说的就是这个东西，不是别的，这就是本身。']}]
json.dump({'itself': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

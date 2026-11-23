import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/order/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.30（第七十四版）：26 order（青绿工笔风：先照图画书风画好、检查“都齐了”，再 styles.py gongbi）。画图脚本：street,alarm,order。
# 六个意思只画三个：顺序、命令、订购点菜；“秩序”只在演变里讲，“目”（生物分类）不讲。辨析 order / command（command：城墙上哨兵大喊下令）
P = {'style': 'core', 'board': True}
LOOM = ['art/loom_f%d.svg' % k for k in range(3)]
def lab(t, x, y, size=0.075, **kw):
    d = {'label': t, 'x': x, 'y': y, 'size': size, 'z': 7}
    d.update(kw); return d
BLUE = {'color': '#1A66B8', 'border': '#2F95E6'}
GREEN = {'color': '#2B8A3E', 'border': '#2B8A3E'}
def loom(x, y, s, **kw):
    d = {'svg': LOOM[0], 'frames': LOOM, 'fps': 1.6, 'seq': 'pingpong', 'x': x, 'y': y, 's': s, 'z': 2}
    d.update(kw); return d
def books(x, y, s, when=None, cue=None, sway=False):    # 书从乱放到按 1～5 排好：说到 when 时换成排好的；不写 when 就来回换
    if not when:
        return [{'svg': 'art/books_f0.svg', 'frames': ['art/books_f0.svg', 'art/books_f1.svg'], 'fps': 0.5, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 2}]
    a = {'svg': 'art/books_f0.svg', 'x': x, 'y': y, 's': s, 'z': 2, 'hideWhen': when}
    b = {'svg': 'art/books_f1.svg', 'x': x, 'y': y, 's': s, 'z': 3, 'when': when, 'fade': 0.3, 'anim': 'sway'}
    if cue is not None:
        a['hideCue'] = cue; b['cue'] = cue
    return [a, b]
def runners(y=0.97, s=0.36, **kw):
    out = [walker('walk-cn-boy-pack', y, s, -0.1, 1.1, 0.0, z=2), walker('walk-west-boy-pack', y, s * 0.95, -0.1, 1.1, 0.35, z=2)]
    for it in out: it.update(kw)
    return out
# ======== 来历：拉丁语 ordo / ordin“一排、次序”（织布机上的一排经线）
W, H = 537, 356
P['originPic'] = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('cn-girl-weave', x=0.2, y=waist(0.82), s=0.82, z=3), loom(0.62, 0.56, 0.78),
    lab('ordin：一排、次序', 0.62, 0.1, 0.07, when='一排', **BLUE)]}
# ======== 意思（六个只画三个）
W, H = 537, 356
pic0 = {'text': '顺序', 'pos': '名词', 'diff': '东西一个接一个排开', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items':
    books(0.64, 0.56, 0.6) + [actor('west-girl-books', x=0.2, y=waist(0.84), s=0.84, z=3)]}
pic1 = {'text': '命令', 'pos': '名词', 'diff': '上面发下来、要照着做的话', 'bg': 'blank', 'img': 'art/park-bg.svg', 'items':
    runners(0.97, 0.36) + [actor('west-man-coach', x=0.26, y=waist(0.86), s=0.86, z=3)]}
pic2 = {'text': '订购、订单；点菜', 'pos': '名词', 'diff': '跟店家说要什么、要多少', 'bg': 'blank', 'img': 'art/diner-bg.svg', 'items': [
    actor('cn-girl-order', id='g', x=0.26, y=waist(0.82), s=0.82, z=3), actor('west-man-waiter', x=0.74, y=waist(0.86), s=0.86, z=3, nodWith='g')]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': books(0.64, 0.55, 0.66, when='order', cue=0) + [
    actor('west-girl-books', x=0.26, y=waist(0.94), s=0.94, z=3),
    {'sound': 'whoosh', 'when': 'order', 'cue': 0},
    lab('按顺序', 0.64, 0.08, 0.075, when='顺序', cue=1, **BLUE)]}
ex1 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': runners(0.98, 0.4, when='run', cue=0) + [
    actor('west-man-coach', x=0.22, y=waist(0.94), s=0.94, z=3),
    {'sound': 'footsteps', 'when': 'run', 'cue': 0},
    lab('下令', 0.22, 0.08, 0.075, when='下令', cue=1, **BLUE)]}
ex2 = {'bg': 'blank', 'img': 'art/diner-bg.svg', 'items': [
    actor('cn-girl-order', id='g', x=0.3, y=waist(0.94), s=0.94, z=3),
    actor('west-man-waiter', x=0.72, y=waist(0.94), s=0.94, z=3, nodWith='g', when='order', cue=0, fade=0.3),
    {'sound': 'click', 'when': 'noodles', 'cue': 0},
    lab('点一碗面条', 0.5, 0.08, 0.075, when='点一碗面条', cue=1, **BLUE)]}
pic0.update({'ex': 'Please put these books in order.', 'exzh': '请把这些书按顺序放好。', 'exPic': ex0})
pic1.update({'ex': 'The coach gave the order to run.', 'exzh': '教练下令开跑。', 'exPic': ex1})
pic2.update({'ex': 'I would like to order a bowl of noodles.', 'exzh': '我想点一碗面条。', 'exPic': ex2})
P['pics'] = [pic0, pic1, pic2]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [loom(0.5, 0.56, 0.8), lab('一排经线', 0.5, 0.08, 0.07, delay=0.3)]}
fig1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': books(0.5, 0.56, 0.62, when='一个接一个') + [
    lab('顺序', 0.24, 0.08, 0.07, when='顺序', **GREEN), lab('名词', 0.8, 0.08, 0.06, when='名词')]}
fig2 = {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': [
    walker('walk-west-man-case', 0.98, 0.34, 1.1, -0.1, 0.0, z=1),
    actor('cn-boy-queue', x=0.3, y=waist(0.7), s=0.7, z=2, nodWith='w'), actor('west-woman-queue', id='w', x=0.52, y=waist(0.78), s=0.78, z=3),
    actor('west-girl-listen', x=0.74, y=waist(0.72), s=0.72, z=4, nodWith='w'),
    lab('排队上车', 0.5, 0.08, 0.065, when='排队上车'), lab('秩序', 0.84, 0.2, 0.07, when='秩序', **GREEN)]}
fig3 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': runners(0.98, 0.34, when='命令') + [
    actor('west-man-coach2', x=0.26, y=waist(0.84), s=0.84, z=3), lab('命令', 0.7, 0.1, 0.07, when='命令', **GREEN)]}
fig4 = {'bg': 'blank', 'img': 'art/diner-bg.svg', 'items': [
    actor('cn-girl-menu', id='g', x=0.28, y=waist(0.84), s=0.84, z=3), actor('west-man-write', x=0.74, y=waist(0.86), s=0.86, z=3, nodWith='g'),
    {'sound': 'cash', 'when': '订购'},
    lab('要什么、要多少', 0.5, 0.08, 0.06, when='要什么'), lab('订购、点菜', 0.5, 0.2, 0.065, when='订购', **GREEN)]}
P['flow'] = [
    {'node': '“一排”', 'fig': fig0},
    {'via': '东西一个接一个地排开', 'node': '① 顺序', 'pos': '名词', 'pic': 0, 'fig': fig1,
     'say': ['经线一根挨一根，排得整整齐齐。东西一个接一个地排开，就是顺序。', '它说的是排法，所以是名词。']},
    {'via': '人和事各在各的位置上，不乱', 'node': '秩序', 'fig': fig2,
     'say': ['人和事都在各自的位置上，不乱，比如大家排队上车，这就是秩序。']},
    {'via': '为了有秩序，上面发下来的话', 'node': '② 命令', 'pos': '名词', 'pic': 1, 'fig': fig3,
     'say': ['为了让事情有秩序，上面发下来、要人照着做的话，就是命令。']},
    {'via': '跟店家“下命令”', 'node': '③ 订购、点菜', 'pos': '名词', 'pic': 2, 'fig': fig4,
     'say': ['跟店家“下命令”：要什么、要多少，就是订购；在饭馆里，就是点菜。']}]
P['extend'] = ['disorder', 'ordinary', 'orderly']
# ======== 同义词辨析：order / command
W, H = 504, 204
P['distinguish'] = {'key': '命令', 'items': [
    {'w': 'order', 'gloss': '命令、吩咐', 'note': '日常说的命令、吩咐', 'ex': 'give an order',
     'pic': {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': runners(0.99, 0.42) + [actor('west-man-coach2', x=0.3, y=waist(0.96), s=0.96, z=3)]}},
    {'w': 'command', 'gloss': '命令、指挥', 'note': '更正式，有权威的人正式下令', 'ex': 'a command from the captain',
     'pic': {'bg': 'blank', 'img': 'art/castle-bg.svg', 'items': [actor('west-man-shout', x=0.5, y=waist(0.96), s=0.96, z=3)]}}],
    'tip': 'order 是日常的命令、吩咐；command 更正式、更带权威。'}
json.dump({'order': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

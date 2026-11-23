import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/rock/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
P = {'style': 'core', 'board': True}
BIRD = ['art/bird_f0.svg', 'art/bird_f1.svg']
def birds(y=0.2, n=2, **kw):
    out = []
    for k in range(n):
        d = {'svg': BIRD[0], 'frames': BIRD, 'fps': 6, 'seq': 'loop', 'x': -0.05, 'y': y + 0.05 * k, 's': 0.05, 'go': [1.05, y - 0.04 + 0.05 * k], 'dur': 6.0 + k, 'loop': True, 'delay': 1.2 * k, 'z': 4}
        d.update(kw); out.append(d)
    return out
def foam(x, y, **kw):   # 浪打在礁石上，一下一下溅起白浪（声波一样往上走）
    d = {'waves': True, 'x': x, 'y': y, 'dir': -90, 'spread': 90, 'n': 3, 'period': 1.6, 'r0': 0.02, 'r1': 0.12, 'lw': 0.014, 'color': '#FFFFFF', 'z': 3}
    d.update(kw); return d
W, H = 537, 356
P['originPic'] = {'bg': 'blank', 'img': 'art/sea-bg.svg', 'items': [foam(0.48, 0.6), foam(0.62, 0.62, period=1.9),
    {'label': '峭壁、礁石', 'x': 0.5, 'y': 0.12, 'size': 0.08, 'delay': 0.5, 'z': 6}, {'sound': 'waves', 'delay': 0.6}]}
pic0 = {'text': '岩石', 'pos': '名词', 'diff': '大块的石头', 'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    {'svg': 'art/big-rock.svg', 'x': 0.5, 'y': 0.72, 's': 0.5, 'z': 2},
    {'svg': 'art/pebble.svg', 'x': 0.2, 'y': 0.9, 's': 0.08, 'go': [0.26, 0.92], 'dur': 1.4, 'loop': True, 'z': 3}]}
pic1 = {'text': '礁石', 'pos': '名词', 'diff': '海里露出水面的岩石', 'bg': 'blank', 'img': 'art/sea-bg.svg', 'items': [foam(0.48, 0.6), foam(0.62, 0.62, period=1.9),
    {'svg': 'art/sailboat.svg', 'x': 0.86, 'y': 0.45, 's': 0.14, 'go': [0.8, 0.46], 'dur': 3.0, 'loop': True, 'z': 2}]}
pic2 = {'text': '石块、石子', 'pos': '名词', 'diff': '手里拿得起的小石头（美国口语）', 'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    actor('west-boy-throw', x=0.3, y=waist(0.95), s=0.95, z=2),
    {'svg': 'art/pebble.svg', 'x': 0.42, 'y': 0.35, 's': 0.07, 'go': [0.7, 0.75], 'dur': 1.6, 'loop': True, 'z': 3}]}
pic3 = {'text': '靠山、主心骨', 'pos': '名词', 'diff': '又稳又可靠、能依靠的人', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('west-woman-hug', id='m', x=0.38, y=waist(0.98), s=0.98, z=2), actor('west-boy-proud', x=0.66, y=waist(0.78), s=0.78, z=3, nodWith='m')]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': birds() + [
    {'svg': 'art/big-rock.svg', 'x': 0.5, 'y': 0.72, 's': 0.55, 'when': 'rock', 'cue': 0, 'fade': 0.4, 'z': 2},
    {'label': '大岩石', 'x': 0.5, 'y': 0.25, 'size': 0.075, 'when': '岩石', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/sea-bg.svg', 'items': [foam(0.5, 0.6), foam(0.6, 0.62, period=1.9),
    {'svg': 'art/sailboat.svg', 'x': 0.85, 'y': 0.47, 's': 0.16, 'go': [0.6, 0.55], 'dur': 2.0, 'goWhen': 'hit', 'goCue': 0, 'z': 4},
    {'sound': 'waves', 'when': 'hit', 'cue': 0},
    {'label': '礁石', 'x': 0.55, 'y': 0.3, 'size': 0.075, 'when': '礁石', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex2 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    actor('west-boy-throw', x=0.3, y=waist(0.98), s=0.98, z=2),
    {'svg': 'art/pebble.svg', 'x': 0.4, 'y': 0.3, 's': 0.07, 'go': [0.62, 0.8], 'dur': 1.2, 'goWhen': 'threw', 'goCue': 0, 'when': 'threw', 'cue': 0, 'z': 3},
    {'sound': 'splash', 'when': 'lake', 'cue': 0},
    {'waves': True, 'x': 0.62, 'y': 0.8, 'dir': -90, 'spread': 160, 'n': 3, 'period': 1.2, 'r0': 0.01, 'r1': 0.12, 'lw': 0.01, 'color': '#FFFFFF', 'when': 'lake', 'cue': 0, 'z': 3},
    {'label': '石子', 'x': 0.66, 'y': 0.25, 'size': 0.075, 'when': '石子', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex3 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('west-woman-hug', id='m', x=0.4, y=waist(0.98), s=0.98, z=2), actor('west-boy-proud', x=0.64, y=waist(0.8), s=0.8, z=3, nodWith='m'),
    {'label': '靠山', 'x': 0.4, 'y': 0.12, 'size': 0.075, 'when': '靠山', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'There is a huge rock by the river.', 'exzh': '河边有一块巨大的岩石。', 'exPic': ex0})
pic1.update({'ex': 'The boat hit the rocks.', 'exzh': '船撞上了礁石。', 'exPic': ex1})
pic2.update({'ex': 'The boy threw a rock into the lake.', 'exzh': '男孩往湖里扔了一块石子。', 'exPic': ex2})
pic3.update({'ex': 'My mother is my rock.', 'exzh': '妈妈是我的靠山。', 'exPic': ex3})
P['pics'] = [pic0, pic1, pic2, pic3]
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/sea-bg.svg', 'items': [foam(0.48, 0.6), {'label': '大块的岩体、礁', 'x': 0.5, 'y': 0.12, 'size': 0.07, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': birds() + [{'svg': 'art/big-rock.svg', 'x': 0.5, 'y': 0.7, 's': 0.5, 'when': '峭壁', 'z': 2},
    {'label': '岩石', 'x': 0.5, 'y': 0.15, 'size': 0.075, 'when': '岩石', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/sea-bg.svg', 'items': [foam(0.48, 0.6), foam(0.62, 0.62, period=1.9),
    {'label': '礁石', 'x': 0.55, 'y': 0.3, 'size': 0.075, 'when': '礁', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig3 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': birds() + [
    {'svg': 'art/pebble.svg', 'x': 0.4, 'y': 0.8, 's': 0.1, 'when': '手里', 'z': 3}, {'svg': 'art/pebble.svg', 'x': 0.5, 'y': 0.84, 's': 0.08, 'when': '手里', 'delay': 0.2, 'z': 3},
    {'svg': 'art/pebble.svg', 'x': 0.58, 'y': 0.8, 's': 0.09, 'when': '石块', 'go': [0.58, 0.76], 'dur': 0.8, 'loop': True, 'z': 3},
    {'label': '石块、石子', 'x': 0.68, 'y': 0.2, 'size': 0.07, 'when': '石块', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig4 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [actor('cn-teacher-hug', id='m', x=0.38, y=waist(0.9), s=0.9, z=2, when='靠得住'),
    actor('cn-boy-proud', x=0.68, y=waist(0.72), s=0.72, z=3, nodWith='m', when='靠得住'),
    {'label': '东西 → 比喻人', 'x': 0.5, 'y': 0.24, 'size': 0.06, 'cue': 0, 'z': 6},
    {'label': '又硬又稳 → 靠山', 'x': 0.5, 'y': 0.1, 'size': 0.065, 'when': '靠山', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6}]}
P['flow'] = [
    {'node': '“峭壁、礁石”', 'fig': fig0},
    {'via': '大块的岩体、峭壁', 'node': '① 岩石', 'pos': '名词', 'pic': 0, 'fig': fig1, 'say': ['山上大块的岩体、峭壁，就是岩石。它说的是一样东西，所以是名词。']},
    {'from': 0, 'via': '海里露出水面的岩石', 'node': '② 礁石', 'pos': '名词', 'pic': 1, 'fig': fig2, 'say': ['海里露出水面的岩石，就是礁。']},
    {'from': 1, 'via': '拿得起的石块（美国口语）', 'node': '③ 石块、石子', 'pos': '名词', 'pic': 2, 'fig': fig3, 'say': ['美国人口语里，连手里拿得起的石块也叫 rock，就是石块、石子。']},
    {'from': 1, 'via': '又硬又稳，推不动', 'node': '④ 靠山、主心骨', 'pos': '名词', 'pic': 3, 'fig': fig4,
     'rule': '英语里，常拿东西的样子比喻人', 'ruleEx': 'rock 岩石 → 靠山      star 星星 → 明星',
     'say': ['英语里，常拿东西的样子来比喻人。', '岩石又硬又稳，推不动，比喻一个靠得住的人，就是靠山、主心骨。']}]
P['distinguish'] = False
# 6.29.2：扩展词手挑（rock 的候选里混进了“rock-eater 不是词典里的固定”这种说明文字）
P['extend'] = ['rocky']
json.dump({'rock': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/thermostat/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
P = {'style': 'core', 'board': True}
def fishes(tx, ty, tw, th):   # 鱼缸里游来游去的鱼、冒泡（鱼缸放在 tx, ty 中心，宽 tw、高 th，都是画框比例）
    out = []
    for k, (f, yy, dur, rev) in enumerate((('fish', 0.0, 5.0, False), ('fish2', 0.18, 6.5, True))):
        x0, x1 = tx - tw * 0.36, tx + tw * 0.28
        a, b = (x1, x0) if not rev else (x0, x1)
        out.append({'svg': f'art/{f}.svg', 'x': a, 'y': ty + yy * th - 0.05, 's': th * 0.2, 'go': [b, ty + yy * th - 0.05], 'dur': dur, 'loop': True, 'z': 3})
    out.append({'emit': True, 'svg': 'art/bubble.svg', 'x': tx + tw * 0.33, 'y': ty + th * 0.2, 's': th * 0.08, 'to': [0, -th * 0.5], 'life': 1.6, 'every': 0.5, 'wobble': 0.01, 'z': 4})
    return out
# ======== 每部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
        {'id': 'ht', 'svg': 'art/heater.svg', 'x': 0.3, 'y': 0.86, 's': 0.3, 'z': 2},
        {'waves': True, 'on': 'ht', 'x': 185, 'y': 10, 'dir': -90, 'spread': 60, 'n': 3, 'period': 1.2, 'r0': 0.03, 'r1': 0.2, 'lw': 0.012, 'color': '#E8304A', 'z': 3},
        {'svg': 'art/thermometer_f0.svg', 'frames': ['art/thermometer_f%d.svg' % i for i in range(4)], 'fps': 1.2, 'seq': 'loop', 'x': 0.86, 'y': 0.42, 's': 0.5, 'z': 2},
        actor('cn-boy-hot', x=0.55, y=waist(0.8), s=0.8, z=1),
        {'label': '温度', 'x': 0.8, 'y': 0.1, 'size': 0.1, 'when': '温度', 'z': 6}]},
    'p1': {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
        actor('cn-teacher-point', id='t', x=0.3, y=0.6, s=0.86, z=1),
        actor('west-boy-stand', x=0.78, y=0.62, s=0.8, z=0, nodWith='t'),
        mouth_waves('t', 1, when='站', r1=0.15),
        {'svg': 'art/class-desks.svg', 'x': 0.5, 'y': 0.96, 's': 0.28, 'z': 4},
        {'label': '站住 stand', 'x': 0.74, 'y': 0.1, 'size': 0.09, 'when': '站', 'z': 6}]}}
P['icons'] = {'p0': 'art/icon-thermo.svg', 'p1': 'art/icon-stat.svg'}
# ======== 拼起来：让温度站住不动（墙上的恒温器停在 24°，温度计不升不降）
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'id': 'ac', 'svg': 'art/aircon.svg', 'x': 0.5, 'y': 0.12, 's': 0.18, 'z': 1},
    {'waves': True, 'on': 'ac', 'x': 250, 'y': 150, 'dir': 90, 'spread': 80, 'n': 3, 'period': 1.4, 'r0': 0.02, 'r1': 0.14, 'lw': 0.01, 'color': '#2F95E6', 'z': 2},
    {'svg': 'art/thermostat.svg', 'x': 0.32, 'y': 0.56, 's': 0.42, 'z': 2},
    {'svg': 'art/thermometer.svg', 'x': 0.62, 'y': 0.56, 's': 0.5, 'z': 2},
    {'sound': 'beep', 'delay': 0.6}]}
# ======== 现在的意思
W, H = 537, 356
pic0 = {'text': '恒温器', 'pos': '名词', 'diff': '让屋里温度保持不变的装置', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'id': 'ac', 'svg': 'art/aircon.svg', 'x': 0.66, 'y': 0.12, 's': 0.17, 'z': 1},
    {'waves': True, 'on': 'ac', 'x': 250, 'y': 150, 'dir': 90, 'spread': 80, 'n': 3, 'period': 1.4, 'r0': 0.02, 'r1': 0.16, 'lw': 0.01, 'color': '#2F95E6', 'z': 2},
    {'svg': 'art/thermostat.svg', 'x': 0.5, 'y': 0.48, 's': 0.42, 'z': 2},
    actor('west-woman-press', id='w', x=0.24, y=waist(0.95), s=0.95, z=3),
    {'svg': 'art/sofa.svg', 'x': 0.8, 'y': 0.86, 's': 0.3, 'z': 3}]}
pic1 = {'text': '温控器', 'pos': '名词', 'diff': '管住温度的小装置（鱼缸、热水器里都有）', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.55, 'y': 0.86, 's': 0.3, 'z': 0},
    {'svg': 'art/fishtank.svg', 'x': 0.6, 'y': 0.52, 's': 0.44, 'z': 1}] + fishes(0.6, 0.55, 0.62, 0.36) + [
    {'label': '温控器', 'x': 0.86, 'y': 0.15, 'size': 0.075, 'delay': 0.8, 'z': 6}]}
# ======== 例句
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/thermostat-18.svg', 'x': 0.28, 'y': 0.45, 's': 0.4, 'hideWhen': 'turned up', 'z': 2},
    {'svg': 'art/thermostat.svg', 'x': 0.28, 'y': 0.45, 's': 0.4, 'when': 'turned up', 'z': 2},
    actor('west-man-press', id='m', x=0.47, y=waist(0.98), s=0.98, z=3),
    {'id': 'ht', 'svg': 'art/heater.svg', 'x': 0.88, 'y': 0.8, 's': 0.34, 'z': 1},
    {'waves': True, 'on': 'ht', 'x': 185, 'y': 10, 'dir': -90, 'spread': 60, 'n': 3, 'period': 1.2, 'r0': 0.03, 'r1': 0.2, 'lw': 0.012, 'color': '#E8304A', 'when': 'turned up', 'z': 3},
    actor('cn-girl-cold', x=0.72, y=waist(0.8), s=0.8, z=2, hideCue=1, nodWith='m'),
    actor('cn-girl-warm', x=0.72, y=waist(0.8), s=0.8, z=2, cue=1),
    {'sound': 'beep', 'when': 'turned up', 'cue': 0},
    {'label': '恒温器', 'x': 0.28, 'y': 0.12, 'size': 0.075, 'when': '恒温器', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 0.9, 's': 0.3, 'z': 0},
    {'svg': 'art/fishtank.svg', 'x': 0.5, 'y': 0.55, 's': 0.5, 'z': 1}] + fishes(0.5, 0.58, 0.36, 0.42) + [
    {'sound': 'drip', 'cue': 1, 'times': 2, 'every': 0.7},
    {'label': '温控器', 'x': 0.72, 'y': 0.12, 'size': 0.075, 'when': '温控器', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'Dad turned up the thermostat because it was cold.', 'exzh': '天冷，爸爸把恒温器调高了。', 'exPic': ex0})
pic1.update({'ex': 'The thermostat keeps the water in the fish tank warm.', 'exzh': '温控器让鱼缸里的水一直暖暖的。', 'exPic': ex1})
P['pics'] = [pic0, pic1]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/thermostat.svg', 'x': 0.35, 'y': 0.5, 's': 0.45, 'z': 2}, {'svg': 'art/thermometer.svg', 'x': 0.66, 'y': 0.5, 's': 0.55, 'z': 2},
    actor('west-boy-stand', x=0.88, y=waist(0.7), s=0.7, z=1),
    {'label': '温度站住不动', 'x': 0.5, 'y': 0.1, 'size': 0.07, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/thermostat-26.svg', 'x': 0.5, 'y': 0.42, 's': 0.38, 'when': '太热', 'hideWhen': '太冷', 'z': 2},
    {'id': 'ac', 'svg': 'art/aircon.svg', 'x': 0.5, 'y': 0.1, 's': 0.15, 'z': 1},
    {'waves': True, 'on': 'ac', 'x': 250, 'y': 150, 'dir': 90, 'spread': 80, 'n': 3, 'period': 1.2, 'r0': 0.02, 'r1': 0.16, 'lw': 0.012, 'color': '#2F95E6', 'when': '冷风', 'hideWhen': '太冷', 'z': 2},
    actor('cn-boy-hot', id='b', x=0.2, y=waist(0.85), s=0.85, when='太热', hideWhen='太冷', z=3),
    {'sound': 'whoosh', 'when': '冷风'},
    {'label': '太热 → 吹冷风', 'x': 0.8, 'y': 0.3, 'size': 0.062, 'when': '冷风', 'hideWhen': '太冷', 'z': 6},
    {'svg': 'art/thermostat-18.svg', 'x': 0.5, 'y': 0.42, 's': 0.38, 'when': '太冷', 'hideCue': 2, 'z': 2},
    {'id': 'ht', 'svg': 'art/heater.svg', 'x': 0.84, 'y': 0.84, 's': 0.28, 'when': '太冷', 'z': 1},
    {'waves': True, 'on': 'ht', 'x': 185, 'y': 10, 'dir': -90, 'spread': 60, 'n': 3, 'period': 1.2, 'r0': 0.03, 'r1': 0.18, 'lw': 0.012, 'color': '#E8304A', 'when': '烧热', 'hideCue': 2, 'z': 3},
    actor('cn-girl-cold', x=0.2, y=waist(0.85), s=0.85, when='太冷', hideCue=2, z=3, nodWith='b'),
    {'label': '太冷 → 烧暖气', 'x': 0.8, 'y': 0.3, 'size': 0.062, 'when': '烧热', 'hideCue': 2, 'z': 6},
    {'svg': 'art/thermostat.svg', 'x': 0.5, 'y': 0.42, 's': 0.38, 'cue': 2, 'z': 2},
    actor('west-man-smile', x=0.2, y=waist(0.85), s=0.85, cue=2, z=3, nodWith='b'),
    {'label': '恒温器', 'x': 0.8, 'y': 0.3, 'size': 0.07, 'when': '恒温器', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6},
    {'label': '名词：一样东西', 'x': 0.8, 'y': 0.45, 'size': 0.06, 'when': '名词', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 0.9, 's': 0.28, 'z': 0},
    {'svg': 'art/fishtank.svg', 'x': 0.5, 'y': 0.58, 's': 0.42, 'when': '鱼缸', 'fade': 0.4, 'z': 1}] + [dict(f, when='鱼缸') for f in fishes(0.5, 0.6, 0.52, 0.36)] + [
    {'label': '温控器', 'x': 0.78, 'y': 0.15, 'size': 0.07, 'when': '温控器', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6}]}
P['flow'] = [
    {'node': '“让温度站住不动的东西”', 'fig': fig0},
    {'via': '太热就关、太冷就开，温度停在设好的数上', 'node': '① 恒温器', 'pos': '名词', 'pic': 0, 'fig': fig1,
     'say': ['屋里装着一个小装置。', '太热了，它就让空调吹冷风；太冷了，就让暖气烧热。', '温度就停在设好的那个数上，这就是恒温器。它说的是一样东西，所以是名词。']},
    {'via': '别的东西里管温度的小装置', 'node': '② 温控器', 'pos': '名词', 'pic': 1, 'fig': fig2,
     'say': ['不光是屋里，鱼缸、热水器里，也有管温度的小装置。', '它也叫 thermostat，就是温控器。']}]
json.dump({'thermostat': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

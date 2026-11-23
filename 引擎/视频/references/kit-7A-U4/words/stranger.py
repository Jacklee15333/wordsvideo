import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/stranger/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
P = {'style': 'core', 'board': True}
def street_walkers(scale=1.0):
    return [walker('walk-west-woman-case', 0.99, 0.42 * scale, -0.1, 1.1, 0.1, z=-0.5), walker('walk-cn-boy-pack', 0.97, 0.38 * scale, 1.1, -0.1, 0.5, z=-0.6)]
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/station-bg.svg', 'items': [
        actor('cn-boy-shy', x=0.5, y=waist(0.9), s=0.9, z=2),
        walker('walk-cn-teacher-case', 0.98, 0.4, 1.1, -0.1, 0.3, z=1),
        {'label': '外来的、陌生的', 'x': 0.5, 'y': 0.1, 'size': 0.085, 'when': '外来', 'z': 6}]},
    'p1': {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
        actor('cn-teacher-point', id='t', x=0.3, y=0.6, s=0.86, z=1),
        actor('west-girl-listen', x=0.78, y=0.64, s=0.78, z=0, nodWith='t'),
        mouth_waves('t', 1, delay=0.3, r1=0.14),
        {'svg': 'art/class-desks.svg', 'x': 0.5, 'y': 0.96, 's': 0.28, 'z': 4},
        {'label': '…的人', 'x': 0.78, 'y': 0.12, 'size': 0.1, 'when': '人', 'z': 6}]}}
P['icons'] = {'p0': 'art/map.svg', 'p1': 'art/icon-er.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/station-bg.svg', 'items': [
    walker('walk-west-man-case', 0.98, 0.8, -0.1, 1.1, 0.0, z=2),
    {'label': '外来的人', 'x': 0.5, 'y': 0.14, 'size': 0.1, 'delay': 0.5, 'z': 6}]}
W, H = 537, 356
pic0 = {'text': '陌生人', 'pos': '名词', 'diff': '你不认识的人', 'bg': 'blank', 'img': 'art/street-bg.svg', 'items': street_walkers() + [
    actor('west-man-ask', id='m', x=0.66, y=waist(0.98), s=0.98, z=2, turn=[0, 2]),
    actor('cn-boy-shy', x=0.2, y=waist(0.75), s=0.75, z=2, nodWith='m'),
    {'label': '不认识的人', 'x': 0.66, 'y': 0.1, 'size': 0.075, 'delay': 0.6, 'z': 6}]}
pic1 = {'text': '外地人、新来的人', 'pos': '名词', 'diff': '从别的地方刚来的人', 'bg': 'blank', 'img': 'art/station-bg.svg', 'items': [
    walker('walk-cn-girl', 0.98, 0.4, 1.1, -0.1, 0.2, z=-0.5),
    actor('west-woman-lost', x=0.66, y=waist(0.98), s=0.98, z=2),
    {'svg': 'art/books.svg', 'x': 0.86, 'y': 0.9, 's': 0.1, 'z': 3},
    {'label': '刚到这儿', 'x': 0.3, 'y': 0.2, 'size': 0.075, 'delay': 0.6, 'z': 6}]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': street_walkers() + [
    {'sound': 'footsteps', 'delay': 0.1},
    actor('west-man-ask', id='m', x=0.66, y=waist(0.98), s=0.98, z=2, turn=[0, 2], when='stranger', cue=0, fade=0.4),
    actor('cn-girl-direct', id='g', x=0.3, y=waist(0.95), s=0.95, z=2, turn=[1, 2]),
    {'label': '陌生人', 'x': 0.66, 'y': 0.1, 'size': 0.075, 'when': '陌生人', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7},
    {'label': '去车站的路', 'x': 0.12, 'y': 0.2, 'size': 0.07, 'when': 'the way', 'cue': 0, 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/station-bg.svg', 'items': [
    {'sound': 'dingdong', 'cue': 0, 'gap': True},
    walker('walk-west-boy-pack', 0.98, 0.4, -0.1, 1.1, 0.4, z=-0.5),
    actor('west-woman-lost', id='w', x=0.34, y=waist(0.98), s=0.98, z=2),
    actor('cn-teacher-welcome', x=0.72, y=waist(0.95), s=0.95, z=2, nodWith='w'),
    {'label': '外地人', 'x': 0.34, 'y': 0.1, 'size': 0.075, 'when': '外地人', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'A stranger asked me the way to the station.', 'exzh': '一个陌生人向我问去车站的路。', 'exPic': ex0})
pic1.update({'ex': 'I am a stranger here.', 'exzh': '我是外地人，刚来这儿。', 'exPic': ex1})
P['pics'] = [pic0, pic1]
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/station-bg.svg', 'items': [
    walker('walk-west-man-case', 0.98, 0.7, -0.1, 1.1, 0.0, z=2),
    {'label': '外来的人', 'x': 0.5, 'y': 0.12, 'size': 0.075, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/station-bg.svg', 'items': [
    walker('walk-west-woman-case', 0.98, 0.72, -0.1, 0.45, 0.0, z=2),
    actor('cn-teacher-welcome', x=0.78, y=waist(0.85), s=0.85, z=2, when='刚来'),
    {'label': '别的地方 → 这儿', 'x': 0.3, 'y': 0.12, 'size': 0.065, 'when': '别的地方', 'z': 6},
    {'label': '外地人、新来的人', 'x': 0.7, 'y': 0.2, 'size': 0.065, 'when': '外地人', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6},
    {'label': '名词', 'x': 0.7, 'y': 0.33, 'size': 0.06, 'when': '名词', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': street_walkers(1.3) + [
    walker('walk-west-boy-pack', 0.96, 0.5, 1.1, -0.1, 0.8, z=-0.4),
    actor('west-girl-surprised', x=0.5, y=waist(0.85), s=0.85, z=2, when='陌生的城市'),
    {'sound': 'footsteps', 'when': '陌生的城市'},
    {'label': '一个都不认识', 'x': 0.5, 'y': 0.1, 'size': 0.065, 'when': '不认识', 'z': 6},
    {'label': '陌生人', 'x': 0.82, 'y': 0.25, 'size': 0.07, 'when': '陌生人', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6}]}
P['distinguish'] = False
# 6.41（第八十五版）：辨析的演示配画（以前是自动的小图标）：画出字面意思
P['demo'] = {
    'driver': {'icons': ['🚗', 'art/icon-er.svg'], 'lit': '驾驶的人', 'pic': {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': [
        {'e': '🚗', 'x': -0.1, 'y': 0.68, 's': 0.5, 'go': [1.1, 0.68], 'dur': 2.6, 'loop': True, 'anim': 'ride', 'flip': True},
        {'label': '开车的人', 'x': 0.5, 'y': 0.16, 'size': 0.13, 'delay': 0.4}]}},
    'actor': {'icons': ['🎬', 'art/icon-er.svg'], 'lit': '做事的人（演戏的人）', 'pic': {'bg': 'blank', 'img': 'art/stage-bg.svg', 'items': [
        actor('west-man-speech', id='a', x=0.5, y=waist(0.95), s=0.95, z=2),
        mouth_waves('a', 1, delay=0.3, r1=0.16),
        {'label': '演戏的人', 'x': 0.5, 'y': 0.14, 'size': 0.13, 'delay': 0.4, 'z': 6}]}},
    'artist': {'icons': ['🎨', 'art/icon-er.svg'], 'lit': '搞技艺的人', 'pic': {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': [
        actor('west-girl-explain', id='p', x=0.32, y=waist(0.9), s=0.9, z=2),
        {'e': '🖼️', 'x': 0.72, 'y': 0.56, 's': 0.42, 'anim': 'pulse', 'z': 3},
        {'e': '🎨', 'x': 0.88, 'y': 0.8, 's': 0.22, 'anim': 'bob', 'z': 3},
        {'label': '画画的人', 'x': 0.5, 'y': 0.14, 'size': 0.13, 'delay': 0.4, 'z': 6}]}}}
P['flow'] = [
    {'node': '“外来的人”', 'fig': fig0},
    {'via': '从别的地方、别的国家来的人', 'node': '② 外地人、新来的人', 'pos': '名词', 'pic': 1, 'fig': fig1,
     'say': ['从别的地方刚来的人，就是外地人、新来的人。它说的是人，所以是名词。']},
    {'via': '走在陌生的城市，街上的人你都不认识', 'node': '① 陌生人', 'pos': '名词', 'pic': 0, 'fig': fig2,
     'say': ['外地人走在陌生的城市，街上的人他一个都不认识。', '所以，你不认识的人，就叫 stranger，陌生人。']}]
json.dump({'stranger': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

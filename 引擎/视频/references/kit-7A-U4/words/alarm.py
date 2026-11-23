import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/alarm/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
P = {'style': 'core', 'board': True}
BELL = ['art/bell_f0.svg', 'art/bell_f1.svg']; CLK = ['art/clock_f0.svg', 'art/clock_f1.svg']
LICK = ['art/cat-sit_f0.svg', 'art/cat-sit_f2.svg']
def bell(x, y, s, **kw):
    d = [{'id': 'bell', 'svg': BELL[0], 'frames': BELL, 'fps': 8, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 2},
         {'waves': True, 'on': 'bell', 'x': 100, 'y': 110, 'dir': 0, 'both': True, 'spread': 70, 'n': 3, 'period': 0.8, 'r0': 0.4 * s, 'r1': 0.4 * s + 0.16, 'lw': 0.012, 'color': '#E8304A', 'z': 3}]
    for it in d: it.update(kw)
    return d
def clock(x, y, s, **kw):
    d = [{'id': 'clk', 'svg': CLK[0], 'frames': CLK, 'fps': 10, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 3},
         {'waves': True, 'on': 'clk', 'x': 110, 'y': 50, 'dir': -90, 'both': True, 'spread': 120, 'n': 3, 'period': 0.7, 'r0': 0.3 * s, 'r1': 0.3 * s + 0.14, 'lw': 0.012, 'color': '#F59E0B', 'z': 3}]
    for it in d: it.update(kw)
    return d
def jumpcat(x, y, s, **kw):
    d = {'svg': LICK[0], 'frames': LICK, 'fps': 3, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'go': [x, y - 0.12], 'dur': 0.35, 'loop': True, 'z': 3}
    d.update(kw); return d
def bedroom_scene(clk_when=None, who='cn-boy-wake'):
    it = [{'svg': 'art/nightstand.svg', 'x': 0.16, 'y': 0.86, 's': 0.28, 'z': 1}]
    it += clock(0.16, 0.6, 0.26, **({'when': clk_when} if clk_when else {}))
    it += [actor(who, id='b', x=0.6, y=0.55, s=0.7, z=1.5),
           {'svg': 'art/bed.svg', 'x': 0.6, 'y': 0.82, 's': 0.42, 'z': 2}]
    return it
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/castle-bg.svg', 'items': [
        {'svg': 'art/rack.svg', 'x': 0.8, 'y': 0.72, 's': 0.5, 'z': 1},
        actor('west-boy-run', x=0.3, y=waist(0.8), s=0.8, z=2),
        {'ray': [[0.42, 0.45], [0.62, 0.45]], 'arrow': True, 'color': '#C2410C', 'lw': 0.02, 'dur': 0.6, 'when': '到', 'z': 6},
        {'label': '到…去', 'x': 0.5, 'y': 0.12, 'size': 0.1, 'when': '到', 'z': 6}]},
    'p1': {'bg': 'blank', 'img': 'art/castle-bg.svg', 'items': [
        {'svg': 'art/rack.svg', 'x': 0.3, 'y': 0.72, 's': 0.5, 'z': 1},
        actor('cn-boy-guard', x=0.72, y=waist(0.85), s=0.85, z=2),
        {'label': '武器 arm', 'x': 0.32, 'y': 0.12, 'size': 0.1, 'when': '武器', 'z': 6}]}}
P['icons'] = {'p0': 'art/icon-al.svg', 'p1': 'art/icon-arm.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/castle-bg.svg', 'items': [
    actor('west-man-shout', id='s', x=0.3, y=waist(0.9), s=0.9, z=2), mouth_waves('s', 1, delay=0.2, r1=0.2),
    {'svg': 'art/rack.svg', 'x': 0.78, 'y': 0.72, 's': 0.5, 'z': 1},
    {'label': '拿起武器！', 'x': 0.7, 'y': 0.15, 'size': 0.1, 'delay': 0.5, 'z': 6}]}
# ======== 现在的意思
W, H = 537, 356
pic0 = {'text': '警报、警报器', 'pos': '名词', 'diff': '提醒危险的声音、装置', 'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items':
    bell(0.5, 0.3, 0.34) + [
    actor('cn-teacher-lead', id='t', x=0.2, y=waist(0.9), s=0.9, z=3),
    actor('west-girl-surprised', x=0.82, y=waist(0.8), s=0.8, z=3, nodWith='t'),
    {'svg': 'art/class-desks.svg', 'x': 0.5, 'y': 0.97, 's': 0.24, 'z': 4}]}
pic1 = {'text': '闹钟', 'pos': '名词', 'diff': '到点就响、把人叫醒', 'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': bedroom_scene()}
pic2 = {'text': '惊慌、担忧', 'pos': '名词', 'diff': '突然害怕、着急', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/spider.svg', 'x': 0.72, 'y': 0.2, 's': 0.2, 'go': [0.72, 0.34], 'dur': 1.6, 'loop': True, 'z': 2},
    actor('west-woman-shock', id='w', x=0.36, y=waist(0.95), s=0.95, z=3),
    {'label': '啊！', 'x': 0.14, 'y': 0.18, 'size': 0.09, 'delay': 0.5, 'z': 6}]}
pic3 = {'text': '使惊慌', 'pos': '动词', 'diff': '让人或动物突然害怕', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('cn-boy-raise', id='d', x=0.26, y=waist(0.85), s=0.85, z=2),
    {'id': 'drum', 'svg': 'art/drum.svg', 'x': 0.26, 'y': 0.86, 's': 0.3, 'z': 3},
    {'waves': True, 'on': 'drum', 'x': 110, 'y': 60, 'dir': 0, 'spread': 80, 'n': 4, 'period': 0.6, 'r0': 0.05, 'r1': 0.3, 'lw': 0.014, 'color': '#E8304A', 'z': 3},
    {'svg': 'art/cushion.svg', 'x': 0.76, 'y': 0.93, 's': 0.12, 'z': 1}, jumpcat(0.76, 0.72, 0.38),
    {'label': '！', 'x': 0.9, 'y': 0.3, 'size': 0.12, 'delay': 0.4, 'z': 6}]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': bell(0.5, 0.3, 0.36, when='rang', cue=0) + [
    {'sound': 'bell', 'when': 'rang', 'cue': 0},
    {'svg': 'art/bell_f0.svg', 'x': 0.5, 'y': 0.3, 's': 0.36, 'hideWhen': 'rang', 'z': 2},
    actor('cn-teacher-point', id='t', x=0.2, y=waist(0.95), s=0.95, z=3),
    walker('walk-west-boy-pack', 1.0, 0.62, 0.55, 1.15, 0.1, z=4), walker('walk-cn-girl', 1.0, 0.6, 0.45, 1.15, 0.5, z=4),
    {'label': '火警铃', 'x': 0.66, 'y': 0.15, 'size': 0.075, 'when': '火警', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': [
    {'svg': 'art/nightstand.svg', 'x': 0.2, 'y': 0.86, 's': 0.28, 'z': 1}] + clock(0.2, 0.6, 0.26, when='alarm', cue=0) + [
    {'sound': 'alarmclock', 'when': 'alarm', 'cue': 0},
    actor('cn-boy-wake', id='b', x=0.6, y=0.55, s=0.7, z=1.5, when='woke', cue=0, fade=0.3),
    {'svg': 'art/bed.svg', 'x': 0.6, 'y': 0.82, 's': 0.42, 'z': 2},
    {'label': '闹钟', 'x': 0.2, 'y': 0.2, 'size': 0.075, 'when': '闹钟', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex2 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/spider.svg', 'x': 0.66, 'y': 0.16, 's': 0.2, 'when': 'cried', 'cue': 0, 'go': [0.66, 0.32], 'dur': 1.6, 'loop': True, 'z': 2},
    actor('west-woman-shock', x=0.42, y=waist(0.95), s=0.95, z=3, when='cried', cue=0),
    {'label': '惊慌', 'x': 0.2, 'y': 0.2, 'size': 0.075, 'when': '惊慌', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex3 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('cn-boy-raise', x=0.3, y=waist(0.9), s=0.9, z=2),
    {'id': 'drum', 'svg': 'art/drum.svg', 'x': 0.3, 'y': 0.88, 's': 0.3, 'z': 3},
    {'waves': True, 'on': 'drum', 'x': 110, 'y': 60, 'dir': 0, 'spread': 80, 'n': 4, 'period': 0.6, 'r0': 0.04, 'r1': 0.3, 'lw': 0.012, 'color': '#E8304A', 'when': 'noise', 'cue': 0, 'z': 3},
    {'svg': 'art/cushion.svg', 'x': 0.72, 'y': 0.93, 's': 0.12, 'z': 1},
    {'svg': 'art/cat-sit_f0.svg', 'x': 0.72, 'y': 0.72, 's': 0.36, 'hideWhen': 'alarmed', 'z': 3},
    jumpcat(0.72, 0.72, 0.36, when='alarmed', cue=0),
    {'sound': 'drum', 'when': 'noise', 'cue': 0},
    {'label': '吓了一跳', 'x': 0.86, 'y': 0.2, 'size': 0.075, 'when': '吓', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'The fire alarm rang, and we all left the building.', 'exzh': '火警铃响了，我们都离开了大楼。', 'exPic': ex0})
pic1.update({'ex': 'My alarm woke me up early this morning.', 'exzh': '今天早上闹钟很早就把我叫醒了。', 'exPic': ex1})
pic2.update({'ex': 'She cried out in alarm.', 'exzh': '她惊慌地叫了起来。', 'exPic': ex2})
pic3.update({'ex': 'The loud noise alarmed the cat.', 'exzh': '很响的声音把猫吓了一跳。', 'exPic': ex3})
P['pics'] = [pic0, pic1, pic2, pic3]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/castle-bg.svg', 'items': [
    {'svg': 'art/rack.svg', 'x': 0.75, 'y': 0.7, 's': 0.48, 'z': 1}, actor('west-boy-run', x=0.3, y=waist(0.8), s=0.8, z=2),
    {'ray': [[0.42, 0.45], [0.6, 0.45]], 'arrow': True, 'color': '#C2410C', 'lw': 0.016, 'dur': 0.6, 'z': 6},
    {'label': '到武器那儿去！', 'x': 0.5, 'y': 0.1, 'size': 0.075, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/castle-bg.svg', 'items': [
    actor('west-man-shout', id='s', x=0.26, y=waist(0.85), s=0.85, z=2), mouth_waves('s', 1, when='大喊', r1=0.2),
    actor('cn-boy-guard', x=0.74, y=waist(0.75), s=0.75, z=2, nodWith='s', when='大喊'),
    {'label': '拿起武器！', 'x': 0.5, 'y': 0.12, 'size': 0.08, 'when': '大喊', 'z': 6},
    {'label': '战斗号令', 'x': 0.74, 'y': 0.28, 'size': 0.065, 'when': '号令', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/castle-bg.svg', 'items': [
    actor('west-man-shout', x=0.5, y=waist(0.9), s=0.9, z=2),
    {'label': '心里一惊', 'x': 0.2, 'y': 0.15, 'size': 0.07, 'when': '一惊', 'z': 6},
    {'label': '名词', 'x': 0.82, 'y': 0.15, 'size': 0.07, 'when': '名词', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig3 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('cn-girl-wake', x=0.28, y=waist(0.85), s=0.85, z=2), {'id': 'drum', 'svg': 'art/drum.svg', 'x': 0.28, 'y': 0.88, 's': 0.3, 'z': 3},
    {'waves': True, 'on': 'drum', 'x': 110, 'y': 60, 'dir': 0, 'spread': 80, 'n': 4, 'period': 0.6, 'r0': 0.04, 'r1': 0.3, 'lw': 0.014, 'color': '#E8304A', 'z': 3},
    {'svg': 'art/cushion.svg', 'x': 0.74, 'y': 0.93, 's': 0.14, 'z': 1}, jumpcat(0.74, 0.72, 0.4, when='让'),
    {'label': '动词：使惊慌', 'x': 0.72, 'y': 0.15, 'size': 0.07, 'when': '动词', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig4 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': bell(0.5, 0.32, 0.36, when='声音') + [
    actor('cn-teacher-lead', x=0.18, y=waist(0.85), s=0.85, z=3, when='提醒'),
    {'svg': 'art/class-desks.svg', 'x': 0.5, 'y': 0.97, 's': 0.24, 'z': 4},
    {'label': '警报器', 'x': 0.8, 'y': 0.15, 'size': 0.075, 'when': '警报器', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig5 = {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': bedroom_scene(clk_when='到点', who='cn-girl-wake') + [
    {'label': '闹钟', 'x': 0.16, 'y': 0.2, 'size': 0.075, 'when': '闹钟', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6}]}
P['flow'] = [
    {'node': '“到武器那儿去！”', 'fig': fig0},
    {'via': '夜里敌人来了，哨兵大喊', 'node': '战斗号令', 'fig': fig1,
     'say': ['以前，夜里敌人摸到城下，哨兵就大喊：拿起武器！', '这一声喊，就是战斗号令。']},
    {'via': '一听到这声喊，人人心里一惊', 'node': '③ 惊慌、担忧', 'pos': '名词', 'pic': 2, 'fig': fig2,
     'say': ['一听到这声喊，人人心里一惊，就有了惊慌、担忧。它说的是一种感觉，是名词。']},
    {'via': '当动词用：让人惊慌', 'node': '④ 使惊慌', 'pos': '动词', 'pic': 3, 'fig': fig3,
     'say': ['当动词用，就是让人惊慌，使惊慌。']},
    {'from': 1, 'via': '提醒危险的声音和装置', 'node': '① 警报、警报器', 'pos': '名词', 'pic': 0, 'fig': fig4,
     'say': ['后来，用来叫人、提醒危险的声音和装置，也叫 alarm，就是警报、警报器。']},
    {'via': '到点就响、把人叫醒', 'node': '② 闹钟', 'pos': '名词', 'pic': 1, 'fig': fig5,
     'say': ['到点就响、把人叫醒的那一种，就是闹钟。']}]
W, H = 504, 204
P['distinguish'] = {'pics': {'alert': {'bg': 'blank', 'items': [band('art/castle-bg.svg', 0.42, 330),
    actor('cn-boy-guard', id='g', x=0.3, y=waist(0.95), s=0.95, z=2), actor('west-boy-run', x=0.72, y=waist(0.9), s=0.9, z=2, nodWith='g')]}},
    'tip': 'alarm 是响起来的警报；alert 是人提高警觉、随时准备'}
json.dump({'alarm': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/alarm_clock/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.30（第七十四版）：22 alarm clock（图画书风）。画图脚本：alarm,alarmclock。
# alarm 警报：教室里火警铃响，学生排队往外走（不放老师，和 05 alarm 的画错开）；clock 钟：客厅墙上的挂钟，钟摆左右摆；
# 闹钟：床在左、床头柜在右（05 alarm 是反过来的），女孩在床上伸懒腰；例句：外国男孩坐起来；set the alarm：女孩在手机上定闹钟。讲钟的画不放人
P = {'style': 'core', 'board': True, 'distinguish': False}
BELL = ['art/bell_f0.svg', 'art/bell_f1.svg']; CLK = ['art/clock_f0.svg', 'art/clock_f1.svg']; WCLK = ['art/wallclock_f0.svg', 'art/wallclock_f1.svg']
def lab(t, x, y, size=0.075, **kw):
    d = {'label': t, 'x': x, 'y': y, 'size': size, 'z': 7}
    d.update(kw); return d
BLUE = {'color': '#1A66B8', 'border': '#2F95E6'}
GREEN = {'color': '#2B8A3E', 'border': '#2B8A3E'}
def fire_bell(x, y, s, **kw):      # 火警铃一边摇一边往两边出声波
    d = [{'id': 'bell', 'svg': BELL[0], 'frames': BELL, 'fps': 8, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 2},
         {'waves': True, 'on': 'bell', 'x': 100, 'y': 110, 'dir': 0, 'both': True, 'spread': 70, 'n': 3, 'period': 0.8, 'r0': 0.4 * s, 'r1': 0.4 * s + 0.16, 'lw': 0.012, 'color': '#E8304A', 'z': 3}]
    for it in d: it.update(kw)
    return d
def ring_clock(x, y, s, **kw):     # 闹钟一直在抖，头顶出声波
    d = [{'id': 'clk', 'svg': CLK[0], 'frames': CLK, 'fps': 10, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 3},
         {'waves': True, 'on': 'clk', 'x': 110, 'y': 50, 'dir': -90, 'both': True, 'spread': 120, 'n': 3, 'period': 0.7, 'r0': 0.3 * s, 'r1': 0.3 * s + 0.14, 'lw': 0.012, 'color': '#F59E0B', 'z': 3}]
    for it in d: it.update(kw)
    return d
def wall_clock(x, y, s, **kw):
    d = {'svg': WCLK[0], 'frames': WCLK, 'fps': 1, 'seq': 'pingpong', 'x': x, 'y': y, 's': s, 'z': 2}
    d.update(kw); return d
def bed_and_clock(who, bx, nx, s=1.0, clk_when=None, who_kw=None):   # 床在左（人坐在床上），床头柜和闹钟在右
    it = [{'svg': 'art/nightstand.svg', 'x': nx, 'y': 0.86, 's': 0.28 * s, 'z': 1}]
    it += ring_clock(nx, 0.86 - 0.26 * s, 0.26 * s, **({'when': clk_when, 'cue': 0} if clk_when else {}))
    a = actor(who, id='b', x=bx, y=0.55, s=0.7 * s, z=1.5)
    a.update(who_kw or {})
    it += [a, {'svg': 'art/bed.svg', 'x': bx, 'y': 0.82, 's': 0.42 * s, 'z': 2}]
    return it
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': fire_bell(0.5, 0.26, 0.3) + [
        walker('walk-cn-boy-pack', 1.0, 0.58, 0.2, 1.15, 0.0, z=4), walker('walk-west-boy-pack', 1.0, 0.56, 0.2, 1.15, 0.45, z=4),
        {'sound': 'bell', 'when': '警报'}, lab('警报 alarm', 0.5, 0.08, 0.1, when='警报', **BLUE)]},
    'p1': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [wall_clock(0.5, 0.5, 0.84),
        {'sound': 'tick', 'when': '钟', 'times': 3, 'every': 0.5}, lab('钟 clock', 0.5, 0.08, 0.1, when='钟', **BLUE)]}}
P['icons'] = {'p0': 'art/icon-alarm.svg', 'p1': 'art/icon-clock.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': [
    {'svg': 'art/nightstand.svg', 'x': 0.5, 'y': 0.88, 's': 0.34, 'z': 1}] + ring_clock(0.5, 0.56, 0.34, delay=0.4) + [
    {'sound': 'alarmclock', 'delay': 0.4}, lab('会报警的钟', 0.5, 0.1, 0.1, delay=0.6)]}
# ======== 意思
W, H = 537, 356
pic0 = {'text': '闹钟', 'pos': '名词', 'diff': '到点就响、把人叫醒的钟', 'bg': 'blank', 'img': 'art/bedroom-bg.svg',
        'items': bed_and_clock('cn-girl-wake', 0.4, 0.84)}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': bed_and_clock('west-boy-up', 0.38, 0.78, clk_when='alarm',
        who_kw={'when': 'woke', 'cue': 0, 'fade': 0.3}) + [
    {'sound': 'alarmclock', 'when': 'alarm', 'cue': 0},
    lab('闹钟', 0.78, 0.14, 0.075, when='闹钟', cue=1, **BLUE)]}
pic0.update({'ex': 'The alarm clock woke me up this morning.', 'exzh': '闹钟今天早上把我叫醒了。', 'exPic': ex0})
P['pics'] = [pic0]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': [
    {'svg': 'art/nightstand.svg', 'x': 0.5, 'y': 0.88, 's': 0.34, 'z': 1}] + ring_clock(0.5, 0.58, 0.34) + [lab('会报警的钟', 0.5, 0.1, 0.07, delay=0.3)]}
fig1 = {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': bed_and_clock('cn-boy-wake', 0.38, 0.82, s=0.9, clk_when='定好的时间') + [
    lab('定好的时间', 0.82, 0.12, 0.06, when='定好的时间'),
    lab('闹钟', 0.38, 0.12, 0.07, when='闹钟', **GREEN), lab('名词', 0.6, 0.12, 0.06, when='名词')]}
fig2 = {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': [
    actor('west-girl-set', x=0.5, y=waist(0.92), s=0.92, z=3),
    {'sound': 'beep', 'when': 'set'},
    lab('set the alarm 定闹钟', 0.5, 0.1, 0.065, when='set', color='#7B57D6', border='#7B57D6')]}
P['flow'] = [
    {'node': '“会报警的钟”', 'fig': fig0},
    {'via': '到了定好的时间就响铃，把人叫醒', 'node': '① 闹钟', 'pos': '名词', 'pic': 0, 'fig': fig1,
     'say': ['到了定好的时间，它就响铃，把人叫醒。', '这种钟就是闹钟。它说的是东西，所以是名词。']},
    {'via': '口语里常省掉 clock', 'node': 'alarm 也指闹钟', 'fig': fig2,
     'say': ['口语里常把 clock 省掉，一个 alarm 也指闹钟。', '比如 set the alarm，就是定闹钟。']}]
P['extend'] = ['alarm', 'army', 'clockwork']
json.dump({'alarm clock': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

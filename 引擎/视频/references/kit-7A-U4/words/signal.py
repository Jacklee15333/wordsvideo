import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/signal/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 规律照抄总表“用词规律”的原话（小黑板去重靠原话对得上，不然同一条会写两遍）。6.30（第七十四版）：27 signal（青绿工笔风）。画图脚本：street,explore,signal。四个意思画三个：信号、发信号示意、表明；“显著的”只在演变里讲。
# 演变：作记号用的 → 烽火台狼烟（约定的信号）、电和无线电信号 → 发信号（总表规律：表示东西的词直接当动词用）→ 表明 → 显著的（总表规律：名词放在名词前当形容词）。辨析 sign / signal
P = {'style': 'core', 'board': True, 'fengong': False}
FLAG = ['art/flag_f0.svg', 'art/flag_f1.svg']; TL = ['art/tlight_f0.svg', 'art/tlight_f1.svg']; BELL = ['art/schoolbell_f0.svg', 'art/schoolbell_f1.svg']
def lab(t, x, y, size=0.075, **kw):
    d = {'label': t, 'x': x, 'y': y, 'size': size, 'z': 7}
    d.update(kw); return d
BLUE = {'color': '#1A66B8', 'border': '#2F95E6'}
GREEN = {'color': '#2B8A3E', 'border': '#2B8A3E'}
def flag(x, y, s, **kw):
    d = {'svg': FLAG[0], 'frames': FLAG, 'fps': 2.5, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 2}
    d.update(kw); return d
def tlight(x, y, s, when=None, cue=None):     # 信号灯：不写 when 就红绿来回换；写了 when，说到时红灯换绿灯
    if not when:
        return [{'svg': TL[0], 'frames': TL, 'fps': 0.5, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 2}]
    a = {'svg': TL[0], 'x': x, 'y': y, 's': s, 'z': 2, 'hideWhen': when}
    b = {'svg': TL[1], 'x': x, 'y': y, 's': s, 'z': 3, 'when': when, 'fade': 0.2}
    if cue is not None:
        a['hideCue'] = cue; b['cue'] = cue
    return [a, b]
def bell(x, y, s, **kw):
    d = [{'id': 'bell', 'svg': BELL[0], 'frames': BELL, 'fps': 8, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 3},
         {'waves': True, 'on': 'bell', 'x': 100, 'y': 100, 'dir': 0, 'both': True, 'spread': 70, 'n': 3, 'period': 0.8, 'r0': 0.4 * s, 'r1': 0.4 * s + 0.15, 'lw': 0.012, 'color': '#F59E0B', 'z': 3}]
    for it in d: it.update(kw)
    return d
def walkers(y=0.97, s=0.36, **kw):
    out = [walker('walk-cn-girl', y, s, -0.1, 1.1, 0.0, z=1), walker('walk-west-man-case', y, s * 1.05, 1.1, -0.1, 0.45, z=1)]
    for it in out: it.update(kw)
    return out
def smoke(x, y, **kw):      # 烽火台上升起的狼烟
    d = {'emit': True, 'svg': 'art/smoke.svg', 'x': x, 'y': y, 's': 0.12, 'to': [0.04, -0.32], 'life': 2.4, 'every': 0.45, 'wobble': 0.02, 'z': 4}
    d.update(kw); return d
def car(x0, x1, y, s, dur=1.6, **kw):
    d = {'svg': 'art/car.svg', 'x': x0, 'y': y, 's': s, 'go': [x1, y], 'dur': dur, 'z': 3}
    d.update(kw); return d
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [{'svg': 'art/marktree.svg', 'x': 0.38, 'y': 0.56, 's': 0.86, 'z': 2},
        actor('cn-girl-hike', x=0.8, y=waist(0.7), s=0.7, z=3), lab('记号 sign', 0.5, 0.08, 0.1, when='记号', **BLUE)]},
    'p1': {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [flag(0.5, 0.52, 0.72),
        lab('-al 和…有关的', 0.5, 0.08, 0.08, when='有关的', **BLUE), lab('作记号用的', 0.5, 0.92, 0.08, when='作记号用的', **GREEN)]}}
P['icons'] = {'p0': 'art/icon-sign.svg', 'p1': 'art/icon-al2.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/beacon-bg.svg', 'items': [smoke(0.58, 0.34, delay=0.3), {'sound': 'wind', 'delay': 0.3},
    lab('作记号用的', 0.5, 0.12, 0.1, delay=0.6)]}
# ======== 意思（四个画三个）
W, H = 537, 356
pic0 = {'text': '信号', 'pos': '名词', 'diff': '事先约好、传消息的记号', 'bg': 'blank', 'img': 'art/street-bg.svg', 'items': walkers() + tlight(0.82, 0.52, 0.8)}
pic1 = {'text': '发信号、示意', 'pos': '动词', 'diff': '发出约好的记号，让人照着做', 'bg': 'blank', 'img': 'art/street-bg.svg', 'items': walkers(0.97, 0.3) + [
    actor('west-woman-guard', x=0.28, y=waist(0.86), s=0.86, z=4), car(1.25, 0.74, 0.86, 0.3, delay=0.3)]}
pic2 = {'text': '表明', 'pos': '动词', 'diff': '让人看出一件事', 'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': bell(0.5, 0.2, 0.28) + [
    walker('walk-west-boy-pack', 1.0, 0.6, 0.3, 1.2, 0.0, z=4), walker('walk-cn-girl', 1.0, 0.56, 0.3, 1.2, 0.5, z=4)]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': tlight(0.8, 0.5, 0.86, when='green', cue=0) + walkers(0.98, 0.4, when='green', cue=0) + [
    {'sound': 'beep', 'when': 'green', 'cue': 0}, lab('信号灯', 0.8, 0.07, 0.075, when='信号灯', cue=1, **BLUE)]}
ex1 = {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': walkers(0.98, 0.34) + [
    actor('west-woman-guard', x=0.24, y=waist(0.94), s=0.94, z=4), car(1.2, 0.64, 0.86, 0.34, dur=2.0, when='cars', cue=0),
    {'sound': 'car', 'when': 'cars', 'cue': 0}, lab('示意', 0.24, 0.07, 0.075, when='示意', cue=1, **BLUE)]}
ex2 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': bell(0.5, 0.22, 0.32, when='bell', cue=0) + [
    walker('walk-west-boy-pack', 1.0, 0.62, 0.3, 1.2, 0.0, z=4), walker('walk-cn-boy-pack', 1.0, 0.6, 0.3, 1.2, 0.5, z=4),
    {'sound': 'bell', 'when': 'bell', 'cue': 0}, lab('表示下课了', 0.78, 0.07, 0.075, when='表示', cue=1, **BLUE)]}
pic0.update({'ex': 'The traffic signal turned green.', 'exzh': '交通信号灯变绿了。', 'exPic': ex0})
pic1.update({'ex': 'The crossing guard signaled the cars to stop.', 'exzh': '交通协管员示意汽车停下。', 'exPic': ex1})
pic2.update({'ex': 'The bell signals the end of the class.', 'exzh': '铃声表示下课了。', 'exPic': ex2})
P['pics'] = [pic0, pic1, pic2]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [flag(0.5, 0.52, 0.7), lab('作记号用的', 0.5, 0.08, 0.07, delay=0.3)]}
fig1 = {'bg': 'blank', 'img': 'art/beacon-bg.svg', 'items': [smoke(0.58, 0.32, when='狼烟'), {'sound': 'wind', 'when': '狼烟'},
    {'id': 'rt', 'svg': 'art/radiotower.svg', 'x': 0.86, 'y': 0.56, 's': 0.7, 'when': '无线电', 'fade': 0.3, 'z': 3},
    {'waves': True, 'on': 'rt', 'x': 100, 'y': 18, 'dir': 0, 'both': True, 'spread': 120, 'n': 3, 'period': 1.0, 'r0': 0.03, 'r1': 0.2, 'lw': 0.01, 'color': '#2E6FD9', 'when': '无线电', 'z': 3},
    lab('约定的信号', 0.3, 0.08, 0.065, when='约定的信号'), lab('信号', 0.7, 0.2, 0.07, when='也叫信号', **GREEN)]}
fig2 = {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': walkers(0.98, 0.3) + [
    actor('west-woman-guard2', x=0.3, y=waist(0.84), s=0.84, z=4), car(1.25, 0.76, 0.88, 0.28, delay=0.4),
    lab('发信号、示意', 0.7, 0.08, 0.065, when='发信号', **GREEN), lab('动词', 0.86, 0.2, 0.06, when='动词')]}
fig3 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': bell(0.5, 0.22, 0.3, when='铃声') + [
    walker('walk-cn-girl', 1.0, 0.6, 0.3, 1.2, 0.0, z=4),
    lab('下课', 0.84, 0.08, 0.065, when='下课'), lab('表明', 0.16, 0.08, 0.07, when='表明', **GREEN)]}
fig4 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [actor('cn-boy-report', x=0.5, y=waist(0.9), s=0.9, z=3),
    {'sound': 'sparkle', 'when': '显著'},
    lab('a signal success 显著的成功', 0.5, 0.08, 0.055, when='显著', color='#7B57D6', border='#7B57D6'), lab('形容词', 0.84, 0.2, 0.06, when='形容词')]}
P['flow'] = [
    {'node': '“作记号用的”', 'fig': fig0},
    {'via': '事先约好的记号；后来用电、无线电送', 'node': '① 信号', 'pos': '名词', 'pic': 0, 'fig': fig1,
     'say': ['事先约好：烽火台上狼烟一起，就是敌人来了，这是约定的信号。', '后来用电、用无线电送过去的记号，也叫信号。']},
    {'via': '直接当动词用', 'node': '② 发信号、示意', 'pos': '动词', 'pic': 1, 'fig': fig2,
     'rule': '表示东西、性质的词，也能直接当动词用：用这样东西做事，或者使变成这样', 'ruleEx': 'signal 信号 → 表明；water 水 → 浇水',
     'say': ['英语里，表示东西的词，也能直接当动词用。', '发出约好的信号，就是发信号、示意，这里是动词。']},
    {'via': '让人一看就明白', 'node': '③ 表明', 'pos': '动词', 'pic': 2, 'fig': fig3,
     'say': ['一样东西像信号一样，让人看出一件事，就是表明。比如铃声一响，就表明下课了。']},
    {'via': '放在名词前面', 'node': '显著的', 'pos': '形容词', 'fig': fig4,
     'rule': '名词放在别的名词前面，也能当形容词用', 'ruleEx': 'signal 信号 → 显著的；stone 石头 → 石头做的（a stone wall）',
     'say': ['英语里，名词放在别的名词前面，也能当形容词用。', '醒目得像打了记号一样，就是显著的，这里是形容词。']}]
P['extend'] = ['sign', 'design', 'signature']
# ======== 同义词辨析：sign / signal
W, H = 504, 204
P['distinguish'] = {'key': '标志、信号', 'items': [
    {'w': 'sign', 'gloss': '标志、牌子', 'note': '摆在那里让人看的', 'ex': 'a road sign',
     'pic': {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': walkers(0.99, 0.4) + [{'svg': 'art/roadsign.svg', 'x': 0.5, 'y': 0.52, 's': 0.9, 'anim': 'sway', 'z': 3}]}},
    {'w': 'signal', 'gloss': '信号', 'note': '发出来传消息的，常是事先约好的', 'ex': 'a traffic signal',
     'pic': {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': walkers(0.99, 0.4) + tlight(0.5, 0.52, 0.9)}}],
    'tip': 'sign 摆在那里让人看；signal 是发出来传消息的，常是事先约好的。'}
json.dump({'signal': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/schedule/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 规律照抄总表“用词规律”的原话（小黑板去重靠原话对得上，不然同一条会写两遍）。6.30（第七十四版）：24 schedule（图画书风）。画图脚本：schedule。四个意思只画三个（日程表、时刻表、安排），“附表、价目表”只在演变里讲。
# 演变照总表：一小条写了字的纸 → 附表、价目表 → 时刻表（铁路）→ 日程表（规律：核心意思不变，换了对象）→ 安排（规律：表示东西的词直接当动词用）。辨析 schedule / plan
P = {'style': 'core', 'board': True, 'fengong': False, 'sylIpa': ['', 'ʃe', 'djuː', 'l']}   # 英音 /ˈʃedjuːl/：sch 合起来读 /ʃ/，s 那一块不单独发音
PLAN = ['art/planner_f%d.svg' % k for k in range(4)]; DEPS = ['art/deps_f%d.svg' % k for k in range(3)]
def lab(t, x, y, size=0.075, **kw):
    d = {'label': t, 'x': x, 'y': y, 'size': size, 'z': 7}
    d.update(kw); return d
BLUE = {'color': '#1A66B8', 'border': '#2F95E6'}
GREEN = {'color': '#2B8A3E', 'border': '#2B8A3E'}
def planner(x, y, s, **kw):      # 计划板一格格贴满
    d = {'svg': PLAN[0], 'frames': PLAN, 'fps': 0.8, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 2}
    d.update(kw); return d
def deps(x, y, s, **kw):         # 车站电子屏一行行往上翻
    d = {'svg': DEPS[0], 'frames': DEPS, 'fps': 0.7, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 2}
    d.update(kw); return d
def cal(x, y, s, when=None, cue=None, sway=False):    # 挂历：说到 when 时，星期五画上红圈、贴“家长会”（sway：挂在墙上轻轻晃）
    a = {'svg': 'art/cal_f0.svg', 'x': x, 'y': y, 's': s, 'z': 2}
    b = {'svg': 'art/cal_f1.svg', 'x': x, 'y': y, 's': s, 'z': 3, 'fade': 0.3}
    if sway:
        a['anim'] = b['anim'] = 'sway'
    if when:
        a.update({'hideWhen': when}); b.update({'when': when})
        if cue is not None:
            a['hideCue'] = cue; b['cue'] = cue
    else:
        b['delay'] = 0.8
    return [a, b]
def desk():
    return {'svg': 'art/desk.svg', 'x': 0.5, 'y': 0.86, 's': 0.32, 'z': 1}
def paper(x, y, s, **kw):
    d = {'svg': 'art/strip.svg', 'x': x, 'y': y, 's': s, 'anim': 'sway', 'z': 3}
    d.update(kw); return d
def travellers(y=0.97, s=0.4):
    return [walker('walk-west-woman-case', y, s, 1.1, -0.1, 0.0, z=1), walker('walk-cn-boy-pack', y, s * 0.85, -0.1, 1.1, 0.5, z=1)]
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [desk(), paper(0.5, 0.5, 0.2), lab('一条纸', 0.5, 0.1, 0.1, when='一条纸', **BLUE)]},
    'p1': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
        {'svg': 'art/bigbox.svg', 'x': 0.24, 'y': 0.58, 's': 0.34, 'z': 2},
        {'svg': 'art/arrow-r.svg', 'x': 0.53, 'y': 0.58, 's': 0.1, 'when': '小', 'fade': 0.3, 'z': 3},
        {'svg': 'art/capsule.svg', 'x': 0.8, 'y': 0.58, 's': 0.1, 'when': '小', 'fade': 0.3, 'anim': 'sway', 'z': 3},
        lab('小 -ule', 0.5, 0.1, 0.1, when='小', **BLUE), lab('一小条纸', 0.5, 0.88, 0.08, when='一小条纸', **GREEN)]}}
P['icons'] = {'p0': 'art/icon-sched.svg', 'p1': 'art/icon-ule.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [paper(0.5, 0.52, 0.34), lab('一小条纸', 0.5, 0.12, 0.1, delay=0.6)]}
# ======== 意思（只画三个）
W, H = 537, 356
pic0 = {'text': '日程表、计划表', 'pos': '名词', 'diff': '自己要做的事，按时间排好', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    planner(0.64, 0.48, 0.64), actor('west-girl-plan', x=0.2, y=waist(0.84), s=0.84, z=3)]}
pic1 = {'text': '时刻表', 'pos': '名词', 'diff': '列着几点开车、几点到站', 'bg': 'blank', 'img': 'art/station-bg.svg', 'items': travellers() + [
    deps(0.62, 0.32, 0.38), actor('west-man-time', x=0.2, y=waist(0.82), s=0.82, z=3)]}
pic2 = {'text': '安排、预定', 'pos': '动词', 'diff': '把事情定在某个时间', 'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items':
    cal(0.66, 0.5, 0.62) + [actor('cn-teacher-sched', x=0.24, y=waist(0.84), s=0.84, z=3)]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('west-girl-plan', x=0.26, y=waist(0.94), s=0.94, z=3),
    planner(0.66, 0.5, 0.74, when='schedule', cue=0, fade=0.3),
    {'sound': 'pop', 'when': 'full', 'cue': 0},
    lab('日程', 0.66, 0.08, 0.075, when='日程', cue=1, **BLUE)]}
ex1 = {'bg': 'blank', 'img': 'art/station-bg.svg', 'items': travellers(0.98, 0.42) + [
    deps(0.66, 0.32, 0.42, when='schedule', cue=0, fade=0.3),
    actor('west-man-time', x=0.24, y=waist(0.94), s=0.94, z=3),
    {'sound': 'dingdong', 'when': 'Check', 'cue': 0},
    lab('时刻表', 0.66, 0.08, 0.075, when='时刻表', cue=1, **BLUE)]}
ex2 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': cal(0.66, 0.5, 0.74, when='scheduled', cue=0) + [
    actor('cn-teacher-sched', x=0.26, y=waist(0.94), s=0.94, z=3),
    {'sound': 'click', 'when': 'Friday', 'cue': 0},
    lab('安排', 0.66, 0.06, 0.075, when='安排', cue=1, **BLUE)]}
pic0.update({'ex': 'My schedule is full this week.', 'exzh': '我这周的日程排得满满的。', 'exPic': ex0})
pic1.update({'ex': 'Check the train schedule before you go.', 'exzh': '出发前先看看火车时刻表。', 'exPic': ex1})
pic2.update({'ex': 'The meeting is scheduled for Friday.', 'exzh': '会议安排在星期五。', 'exPic': ex2})
P['pics'] = [pic0, pic1, pic2]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [desk(), paper(0.5, 0.5, 0.22), lab('一小条写了字的纸', 0.5, 0.1, 0.065, delay=0.3)]}
fig1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [desk(), {'svg': 'art/pricelist.svg', 'x': 0.5, 'y': 0.46, 's': 0.7, 'when': '附表', 'fade': 0.3, 'anim': 'sway', 'z': 2},
    lab('附表', 0.22, 0.12, 0.065, when='附表'), lab('价目表', 0.8, 0.12, 0.065, when='价目表', **GREEN)]}
fig2 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': travellers(0.97, 0.3) + [
    {'svg': 'art/railsheet.svg', 'x': 0.28, 'y': 0.4, 's': 0.62, 'z': 2},
    {'id': 'tr', 'svg': 'art/steamtrain.svg', 'x': 1.3, 'y': 0.84, 's': 0.26, 'go': [-0.4, 0.84], 'dur': 4.5, 'when': '铁路', 'z': 3},
    {'emit': True, 'svg': 'art/puff.svg', 'on': 'tr', 'x': 63, 'y': 20, 's': 0.08, 'to': [0.06, -0.2], 'life': 1.4, 'every': 0.3, 'when': '铁路', 'z': 4},
    {'sound': 'horn', 'when': '铁路'},
    lab('时刻表', 0.72, 0.12, 0.07, when='时刻表', **GREEN)]}
fig3 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [planner(0.5, 0.52, 0.7),
    lab('自己要做的事', 0.3, 0.07, 0.06, when='自己要做的事', **GREEN), lab('名词', 0.82, 0.07, 0.06, when='名词')]}
fig4 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': cal(0.5, 0.52, 0.72, when='安排', sway=True) + [
    lab('动词', 0.84, 0.08, 0.06, when='动词'), lab('安排、预定', 0.2, 0.08, 0.06, when='安排', **GREEN)]}
P['flow'] = [
    {'node': '“一小条写了字的纸”', 'fig': fig0},
    {'via': '附在文件后面，一项项列明细', 'node': '附表、价目表', 'fig': fig1,
     'say': ['写了字的纸条，附在文件后面，一项项列出明细，就成了附表；列价钱的，就是价目表。']},
    {'via': '铁路印出来，列着几点开车', 'node': '② 时刻表', 'pos': '名词', 'pic': 1, 'fig': fig2,
     'say': ['后来，铁路把几点开车、几点到站印成一张表，这就是时刻表。']},
    {'via': '自己的事也按时间排好', 'node': '① 日程表、计划表', 'pos': '名词', 'pic': 0, 'fig': fig3,
     'rule': '词的核心意思不变，换了对象、场合，中文要换个说法，英语还是这个词', 'ruleEx': 'schedule 日程表、计划表 → 时刻表；play 玩 → 踢（球）、演奏（乐器）',
     'say': ['英语里，词的核心意思不变，换了对象，中文要换个说法，英语还是这个词。', '把自己要做的事按时间排好，就是日程表、计划表。它说的是东西，所以是名词。']},
    {'via': '直接当动词用', 'node': '③ 安排、预定', 'pos': '动词', 'pic': 2, 'fig': fig4,
     'rule': '表示东西、性质的词，也能直接当动词用：用这样东西做事，或者使变成这样', 'ruleEx': 'schedule 日程表、计划表 → 安排、预定；water 水 → 浇水',
     'say': ['英语里，表示东西的词，也能直接当动词用。', '把事情排进日程表，就是安排、预定，这里是动词。']}]
P['extend'] = ['capsule']
# ======== 同义词辨析：schedule / plan
W, H = 504, 204
P['distinguish'] = {'key': '计划', 'items': [
    {'w': 'schedule', 'gloss': '日程表、时间表', 'note': '几点做什么，一项项排好', 'ex': 'a busy schedule',
     'pic': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [planner(0.5, 0.52, 0.86)]}},
    {'w': 'plan', 'gloss': '计划、打算', 'note': '想好要做什么，时间不一定定好', 'ex': 'make a plan',
     'pic': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [actor('cn-boy-dream', x=0.3, y=waist(0.96), s=0.96, z=2),
         {'svg': 'art/plan-bubble.svg', 'x': 0.7, 'y': 0.42, 's': 0.62, 'anim': 'sway', 'z': 3}]}}],
    'tip': 'schedule 排到具体时间；plan 是心里的打算，时间不一定定好。'}
json.dump({'schedule': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

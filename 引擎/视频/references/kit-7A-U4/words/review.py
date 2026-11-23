import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/review/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.29.2：17 review（中西合璧风）。re- 再：绕一圈回来的箭头；view 看：拿望远镜看风景；
# 最早是检阅（军官从一排士兵前走过）→ 审查（老师批作业打勾）→ 回顾（挂历一页页翻）/ 书评（新书得五颗星）/ 复习（拿放大镜看笔记）
# 画只能放三个意思（wordfilm.js 只取前三幅）：回顾、评论、复习；审查、复核放在演变里讲
P = {'style': 'core', 'board': True}
CAL = ['art/calendar_f%d.svg' % k for k in range(4)]
def cal(x, y, s, **kw):
    d = {'svg': CAL[0], 'frames': CAL, 'fps': 1.2, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 2}
    d.update(kw); return d
def stars(x0, x1, y, s, **kw):   # 五颗星一颗颗亮起来
    out = []
    for k in range(5):
        d = {'svg': 'art/star.svg', 'x': x0 + (x1 - x0) * k / 4, 'y': y, 's': s, 'delay': 0.3 * k, 'z': 5}
        d.update(kw)
        if 'delay' in kw: d['delay'] = kw['delay'] + 0.3 * k
        out.append(d)
    return out
def shine(x, y, sx=0.3, **kw):   # 书旁边一闪一闪的小星星（好评）
    d = {'emit': True, 'svg': 'art/star.svg', 'x': x, 'y': y, 'spreadX': sx, 's': 0.06, 'to': [0.0, -0.08], 'life': 1.2, 'every': 0.45, 'spin': 0.8, 'z': 6}
    d.update(kw); return d
def ticks(x0, y0, dy, s, **kw):   # 作业本上一个个红勾
    out = []
    for k in range(4):
        d = {'svg': 'art/tick.svg', 'x': x0, 'y': y0 + dy * k, 's': s, 'delay': 0.5 + 0.45 * k, 'z': 5}
        d.update(kw)
        if 'delay' in kw: d['delay'] = kw['delay'] + 0.45 * k
        out.append(d)
    return out
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [        # re- 再：书看完又翻回来，绕一圈的箭头
        {'svg': 'art/desk.svg', 'x': 0.5, 'y': 0.98, 's': 0.32, 'z': 1},
        {'svg': 'art/book-new.svg', 'x': 0.5, 'y': 0.6, 's': 0.42, 'z': 2},
        {'svg': 'art/again.svg', 'x': 0.8, 'y': 0.36, 's': 0.3, 'anim': 'sway', 'z': 4},
        {'label': '再 re-', 'x': 0.5, 'y': 0.1, 'size': 0.1, 'when': '再', 'z': 6}]},
    'p1': {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [        # view 看：拿望远镜看风景
        actor('west-woman-look', x=0.5, y=waist(0.9), s=0.9, z=2),
        {'label': '看 view', 'x': 0.5, 'y': 0.1, 'size': 0.1, 'when': '看', 'z': 6}]}}
P['icons'] = {'p0': 'art/icon-again.svg', 'p1': 'art/icon-eye.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('cn-boy-study', x=0.3, y=waist(1.0), s=1.0, z=2),
    {'svg': 'art/again.svg', 'x': 0.72, 'y': 0.5, 's': 0.42, 'anim': 'sway', 'z': 4},
    {'sound': 'whoosh', 'delay': 0.5},
    {'label': '再看一遍', 'x': 0.72, 'y': 0.12, 'size': 0.1, 'delay': 0.6, 'z': 6}]}
# ======== 意思
W, H = 537, 356
pic0 = {'text': '回顾', 'pos': '名词', 'diff': '把过去一段时间的事从头再看一遍', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    cal(0.5, 0.48, 0.66)]}
pic1 = {'text': '评论、书评', 'pos': '名词', 'diff': '看完一本书、一部戏，写下的评价', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 1.0, 's': 0.3, 'z': 1},
    {'svg': 'art/book-new.svg', 'x': 0.5, 'y': 0.56, 's': 0.56, 'z': 2}, *stars(0.26, 0.74, 0.16, 0.1, delay=0.4), shine(0.5, 0.5)]}
pic2 = {'text': '复习', 'pos': '动词', 'diff': '学过的东西再看一遍', 'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    actor('cn-girl-study', x=0.36, y=waist(0.88), s=0.88, z=2),
    {'svg': 'art/homework.svg', 'x': 0.78, 'y': 0.82, 's': 0.3, 'z': 3}]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    cal(0.5, 0.48, 0.86, when='review', cue=0, fade=0.3),
    {'sound': 'whoosh', 'when': 'review', 'cue': 0},
    {'label': '回顾这一年', 'x': 0.18, 'y': 0.16, 'size': 0.075, 'when': '回顾', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 1.02, 's': 0.34, 'z': 1},
    {'svg': 'art/book-new.svg', 'x': 0.5, 'y': 0.56, 's': 0.62, 'when': 'book', 'cue': 0, 'fade': 0.3, 'z': 2},
    *stars(0.36, 0.64, 0.14, 0.11, when='good', cue=0), shine(0.5, 0.5, 0.2, when='good', cue=0),
    {'sound': 'applause', 'cue': 0, 'gap': True},
    {'label': '很好的评价', 'x': 0.82, 'y': 0.16, 'size': 0.075, 'when': '评价', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex2 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    actor('cn-girl-laugh', x=0.3, y=waist(0.96), s=0.96, z=2),
    {'svg': 'art/homework.svg', 'x': 0.66, 'y': 0.72, 's': 0.42, 'when': 'notes', 'cue': 0, 'fade': 0.3, 'z': 3},
    {'svg': 'art/clock_f0.svg', 'frames': ['art/clock_f0.svg', 'art/clock_f1.svg'], 'fps': 1, 'seq': 'loop', 'x': 0.88, 'y': 0.22, 's': 0.2, 'z': 2},
    {'sound': 'tick', 'when': 'test', 'cue': 0, 'times': 3, 'every': 0.5},
    {'label': '复习', 'x': 0.66, 'y': 0.16, 'size': 0.075, 'when': '复习', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'The TV show gave a review of the year.', 'exzh': '这档电视节目回顾了这一年。', 'exPic': ex0})
pic1.update({'ex': 'The new book got very good reviews.', 'exzh': '这本新书得到了很好的评价。', 'exPic': ex1})
pic2.update({'ex': 'I review my notes before every test.', 'exzh': '每次考试前我都复习笔记。', 'exPic': ex2})
P['pics'] = [pic0, pic1, pic2]
# ======== 同义词辨析：review / comment / remark
W, H = 537, 356
P['distinguish'] = {'key': '评论', 'items': [
    {'w': 'review', 'gloss': '评论、书评', 'note': '把作品从头看一遍，再写下评价', 'ex': 'a book review',
     'pic': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [{'svg': 'art/book-new.svg', 'x': 0.5, 'y': 0.58, 's': 0.56, 'z': 2}, *stars(0.26, 0.74, 0.16, 0.1, delay=0.3), shine(0.5, 0.5)]}},
    {'w': 'comment', 'gloss': '评论、意见', 'note': '对一件事发表看法，常接 on', 'ex': 'comment on the film',
     'pic': {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [actor('west-girl-explain', id='g', x=0.3, y=waist(0.86), s=0.86, z=2, turn=[0, 2]),
                                                                    actor('cn-teacher-listen', x=0.74, y=waist(0.8), s=0.8, z=1, nodWith='g')]}},
    {'w': 'remark', 'gloss': '话、评论', 'note': '随口说的一句话', 'ex': 'a funny remark',
     'pic': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [actor('west-man-smile', id='m', x=0.3, y=waist(0.86), s=0.86, z=2),
                                                               actor('cn-girl-laugh', x=0.72, y=waist(0.8), s=0.8, z=2, nodWith='m')]}}],
    'tip': 'review 看完作品写评价，comment 对一件事发表看法，remark 随口说的一句话。'}
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('west-boy-study', x=0.32, y=waist(0.86), s=0.86, z=2),
    {'svg': 'art/again.svg', 'x': 0.76, 'y': 0.5, 's': 0.3, 'anim': 'sway', 'z': 4},
    {'label': '再 + 看', 'x': 0.5, 'y': 0.1, 'size': 0.075, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    {'svg': 'art/soldiers.svg', 'x': 0.6, 'y': 0.68, 's': 0.42, 'z': 2},
    actor('west-man-inspect', x=0.16, y=waist(0.72), s=0.72, z=3, when='军官', go=[0.28, waist(0.72)], dur=3.0),
    {'sound': 'footsteps', 'when': '走过'},
    {'label': '一排排再看一遍', 'x': 0.5, 'y': 0.1, 'size': 0.065, 'when': '一排排', 'z': 6},
    {'label': '检阅', 'x': 0.5, 'y': 0.24, 'size': 0.07, 'when': '检阅', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    actor('cn-teacher-mark', x=0.26, y=waist(0.8), s=0.8, z=2, when='做过的事'),
    {'svg': 'art/homework.svg', 'x': 0.7, 'y': 0.74, 's': 0.36, 'z': 3, 'when': '做过的事'},
    *ticks(0.62, 0.62, 0.065, 0.06, when='毛病'),
    {'sound': 'ding', 'when': '毛病'},
    {'label': '审查、复核', 'x': 0.5, 'y': 0.1, 'size': 0.07, 'when': '审查', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig3 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    cal(0.5, 0.5, 0.7, when='过去'),
    {'label': '回顾', 'x': 0.5, 'y': 0.08, 'size': 0.07, 'when': '回顾', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig4 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/book-new.svg', 'x': 0.5, 'y': 0.58, 's': 0.5, 'when': '新书', 'z': 2},
    *stars(0.28, 0.72, 0.16, 0.09, when='评价'), shine(0.5, 0.5, 0.3, when='新书'),
    {'label': '评论、书评', 'x': 0.5, 'y': 0.92, 'size': 0.07, 'when': '书评', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig5 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    actor('cn-girl-study', x=0.34, y=waist(0.84), s=0.84, z=2, when='学过'),
    {'svg': 'art/homework.svg', 'x': 0.76, 'y': 0.8, 's': 0.3, 'z': 3, 'when': '学过'},
    {'label': '换了对象：功课', 'x': 0.5, 'y': 0.08, 'size': 0.06, 'when': '核心意思', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6},
    {'label': '复习', 'x': 0.76, 'y': 0.24, 'size': 0.07, 'when': '复习', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
P['flow'] = [
    {'node': '“再看一遍”', 'fig': fig0},
    {'via': '军官一排排再看一遍', 'node': '最早：检阅', 'pos': '名词', 'fig': fig1,
     'say': ['最早，军官从列队的士兵前走过，一排排再看一遍，这叫检阅。']},
    {'from': 1, 'via': '再看一遍，挑出毛病', 'node': '审查、复核', 'pos': '动词', 'fig': fig2,
     'say': ['后来，把做过的事再看一遍，好挑出毛病，就是审查、复核。']},
    {'from': 2, 'via': '过去的事从头再看', 'node': '① 回顾', 'pos': '名词', 'pic': 0, 'fig': fig3,
     'say': ['把过去一段时间的事从头再看一遍，就是回顾。']},
    {'from': 2, 'via': '看完作品写下评价', 'node': '② 评论、书评', 'pos': '名词', 'pic': 1, 'fig': fig4,
     'say': ['把一本新书、一部新戏看一遍，再写下评价，就是评论、书评。']},
    {'from': 2, 'via': '学过的东西再看', 'node': '③ 复习', 'pos': '动词', 'pic': 2, 'fig': fig5,
     'rule': '词的核心意思不变，换了对象、场合，中文要换个说法，英语还是这个词', 'ruleEx': 'review 审查、复核 → 复习      play 玩 → 踢（球）、演奏（乐器）',
     'say': ['英语里，词的核心意思不变，换了对象、场合，中文要换个说法，英语还是这个词。', '学过的东西再看一遍，就是复习。']}]
P['extend'] = ['view', 'interview', 'viewer', 'revise']
json.dump({'review': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

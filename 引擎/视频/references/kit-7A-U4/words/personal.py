import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/personal/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.29.2：20 personal（中西合璧风）。person 人：街上来往的人；-al 和…有关的：书包上挂着写名字的牌子；
# 私人的：带锁的日记本；亲自的：作家亲笔回信；身体的：个人卫生，勤洗手。“针对个人的”只在演变里讲。辨析 personal / private
P = {'style': 'core', 'board': True, 'fengong': False}
WASH = ['art/handwash_f0.svg', 'art/handwash_f1.svg']
def wash(x, y, s, **kw):
    d = {'svg': WASH[0], 'frames': WASH, 'fps': 3, 'seq': 'pingpong', 'x': x, 'y': y, 's': s, 'z': 2}
    d.update(kw); return d
def bubbles(x, y, **kw):
    d = {'emit': True, 'svg': 'art/bubble.svg', 'x': x, 'y': y, 's': 0.05, 'to': [0.02, -0.2], 'life': 1.4, 'every': 0.35, 'wobble': 0.04, 'z': 4}
    d.update(kw); return d
def shine(x, y, sx=0.3, **kw):
    d = {'emit': True, 'svg': 'art/star.svg', 'x': x, 'y': y, 'spreadX': sx, 's': 0.06, 'to': [0.0, -0.08], 'life': 1.2, 'every': 0.45, 'spin': 0.8, 'z': 6}
    d.update(kw); return d
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': [
        walker('walk-cn-girl', 0.99, 0.5, -0.1, 1.1, 0.0, z=2), walker('walk-west-man-case', 0.99, 0.54, 1.1, -0.1, 0.5, z=1),
        {'label': '人 person', 'x': 0.5, 'y': 0.1, 'size': 0.1, 'when': '人', 'z': 6}]},
    'p1': {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
        {'svg': 'art/tagbag.svg', 'x': 0.46, 'y': 0.62, 's': 0.56, 'anim': 'sway', 'z': 2},
        {'label': '和…有关的', 'x': 0.5, 'y': 0.1, 'size': 0.09, 'when': '有关', 'z': 6}]}}
P['icons'] = {'p0': 'art/icon-person.svg', 'p1': 'art/icon-al.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 1.02, 's': 0.34, 'z': 1},
    {'svg': 'art/diary-closed.svg', 'x': 0.5, 'y': 0.56, 's': 0.62, 'anim': 'sway', 'z': 2},
    {'sound': 'keys', 'delay': 0.4},
    {'label': '属于人的', 'x': 0.82, 'y': 0.14, 'size': 0.1, 'delay': 0.6, 'z': 6}]}
W, H = 537, 356
pic0 = {'text': '个人的、私人的', 'pos': '形容词', 'diff': '只属于某一个人的', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('west-boy-secret', x=0.28, y=waist(0.86), s=0.86, z=2),
    {'svg': 'art/desk.svg', 'x': 0.68, 'y': 1.02, 's': 0.3, 'z': 1},
    {'svg': 'art/diary-closed.svg', 'x': 0.68, 'y': 0.6, 's': 0.5, 'anim': 'sway', 'z': 3}]}
pic1 = {'text': '亲自的', 'pos': '形容词', 'diff': '由本人亲自做的，不托别人', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('cn-girl-letter', x=0.5, y=waist(0.9), s=0.9, z=2), shine(0.5, 0.42)]}
pic2 = {'text': '身体的', 'pos': '形容词', 'diff': '和一个人的身体有关的', 'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [
    wash(0.5, 0.66, 0.5), bubbles(0.5, 0.5)]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('west-boy-secret', x=0.28, y=waist(0.96), s=0.96, z=2),
    {'svg': 'art/desk.svg', 'x': 0.62, 'y': 1.04, 's': 0.36, 'z': 1},
    {'svg': 'art/diary-open.svg', 'x': 0.62, 'y': 0.6, 's': 0.6, 'hideWhen': 'diary', 'hideCue': 0, 'z': 3},
    {'svg': 'art/diary-closed.svg', 'x': 0.62, 'y': 0.6, 's': 0.6, 'when': 'diary', 'cue': 0, 'fade': 0.2, 'z': 4},
    {'sound': 'click', 'when': 'diary', 'cue': 0},
    {'label': '私人日记', 'x': 0.86, 'y': 0.16, 'size': 0.075, 'when': '私人', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('cn-girl-letter', x=0.4, y=waist(0.98), s=0.98, z=2, when='reply', cue=0, fade=0.4), shine(0.4, 0.4, 0.3, when='reply', cue=0),
    {'sound': 'sparkle', 'when': 'reply', 'cue': 0},
    {'label': '亲自回信', 'x': 0.78, 'y': 0.16, 'size': 0.075, 'when': '亲自', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex2 = {'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [
    wash(0.5, 0.64, 0.62, when='Washing', cue=0, fade=0.3), bubbles(0.5, 0.46, when='Washing', cue=0),
    {'sound': 'water', 'when': 'Washing', 'cue': 0},
    {'label': '个人卫生', 'x': 0.84, 'y': 0.16, 'size': 0.075, 'when': '卫生', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'This is my personal diary.', 'exzh': '这是我的私人日记。', 'exPic': ex0})
pic1.update({'ex': 'The writer gave me a personal reply.', 'exzh': '作家亲自给我回了信。', 'exPic': ex1})
pic2.update({'ex': 'Washing hands is good for personal hygiene.', 'exzh': '勤洗手有益于个人卫生。', 'exPic': ex2})
P['pics'] = [pic0, pic1, pic2]
W, H = 537, 356
P['distinguish'] = {'key': '个人的', 'items': [
    {'w': 'personal', 'gloss': '个人的', 'note': '属于某一个人的：你的东西、你的看法', 'ex': 'my personal opinion',
     'pic': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [{'svg': 'art/desk.svg', 'x': 0.5, 'y': 1.02, 's': 0.32, 'z': 1},
         {'svg': 'art/diary-closed.svg', 'x': 0.5, 'y': 0.58, 's': 0.56, 'anim': 'sway', 'z': 2}]}},
    {'w': 'private', 'gloss': '私人的', 'note': '不对外、不公开，和 public 相对', 'ex': 'a private room',
     'pic': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [{'svg': 'art/privdoor.svg', 'x': 0.5, 'y': 0.56, 's': 0.86, 'z': 2},
         walker('walk-west-woman-case', 0.99, 0.5, 1.1, 0.75, 0.0, z=3)]}}],
    'tip': 'personal 说属于某个人；private 说不对外公开，反义词是 public。'}
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/tagbag.svg', 'x': 0.3, 'y': 0.62, 's': 0.42, 'anim': 'sway', 'z': 2},
    {'svg': 'art/diary-closed.svg', 'x': 0.72, 'y': 0.6, 's': 0.44, 'anim': 'sway', 'z': 3},
    {'label': '人 + 和…有关的', 'x': 0.5, 'y': 0.1, 'size': 0.07, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 1.0, 's': 0.3, 'z': 1},
    {'svg': 'art/diary-open.svg', 'x': 0.5, 'y': 0.6, 's': 0.48, 'when': '日记', 'anim': 'sway', 'z': 2},
    {'label': '个人的、私人的', 'x': 0.5, 'y': 0.1, 'size': 0.07, 'when': '私人的', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6},
    {'label': '形容词', 'x': 0.5, 'y': 0.24, 'size': 0.06, 'when': '形容词', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('west-woman-letter', x=0.5, y=waist(0.84), s=0.84, z=2, when='本人'), shine(0.5, 0.4, 0.3, when='本人'),
    {'label': '亲自的', 'x': 0.5, 'y': 0.1, 'size': 0.07, 'when': '亲自', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig3 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    actor('west-girl-explain', id='g', x=0.3, y=waist(0.8), s=0.8, z=2, when='话头'),
    actor('cn-boy-shy', x=0.74, y=waist(0.74), s=0.74, z=2, when='某一个人'), mouth_waves('g', 1, when='话头', r1=0.14),
    {'label': '冲着一个人去', 'x': 0.5, 'y': 0.1, 'size': 0.065, 'when': '某一个人', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6}]}
fig4 = {'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [
    wash(0.5, 0.66, 0.46, when='身体'), bubbles(0.5, 0.5, when='身体'),
    {'sound': 'water', 'when': '身体'},
    {'label': '个人卫生', 'x': 0.5, 'y': 0.1, 'size': 0.07, 'when': '卫生', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
P['flow'] = [
    {'node': '“属于人的”', 'fig': fig0},
    {'via': '只属于你这个人的', 'node': '① 个人的、私人的', 'pos': '形容词', 'pic': 0, 'fig': fig1,
     'say': ['只属于你这个人的东西，你的日记、你的看法，就是个人的、私人的。它说明东西是谁的，所以是形容词。']},
    {'from': 1, 'via': '不托别人，本人来做', 'node': '② 亲自的', 'pos': '形容词', 'pic': 1, 'fig': fig2,
     'say': ['不托别人，由本人亲自来做，就是亲自的。']},
    {'from': 1, 'via': '话头冲着一个人', 'node': '针对个人的', 'pos': '形容词', 'fig': fig3,
     'say': ['话头冲着某一个人去，就是针对个人的，常常不太友好。']},
    {'from': 1, 'via': '和人的身体有关', 'node': '③ 身体的', 'pos': '形容词', 'pic': 2, 'fig': fig4,
     'say': ['和一个人的身体有关的，就是身体的，比如个人卫生。']}]
P['extend'] = ['person', 'personality', 'personnel', 'salesperson']
json.dump({'personal': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

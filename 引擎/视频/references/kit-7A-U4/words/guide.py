import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/guide/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.29.2：19 guide（中西合璧风）。带领：老师领着孩子们过马路；导游：举小旗的导游带外国游客逛古镇；指南：摊开的北京旅游指南；
# 指导（只在演变里讲）：老师在桌边指点学生。辨析 guide / lead
P = {'style': 'core', 'board': True}
def kids_crossing(y=0.99, s=0.3, **kw):   # 孩子们走过斑马线
    out = [walker('walk-cn-boy-pack', y, s, 0.55, 1.1, 0.0, z=2), walker('walk-west-boy-pack', y, s * 0.95, 0.5, 1.1, 0.4, z=2)]
    for d in out: d.update(kw)
    return out
def tourists(s=0.3, y=0.99):
    return [walker('walk-west-woman-case', y, s, -0.1, 1.1, 0.1, z=1), walker('walk-west-man-case', y, s, -0.1, 1.1, 0.55, z=1)]
W, H = 537, 356
P['originPic'] = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    {'svg': 'art/signpost.svg', 'x': 0.74, 'y': 0.6, 's': 0.62, 'z': 2},
    walker('walk-west-man-case', 0.97, 0.36, -0.1, 0.62, 0.0, z=3),
    {'label': 'guider：引导、带领', 'x': 0.36, 'y': 0.14, 'size': 0.075, 'delay': 0.5, 'z': 6}]}
pic0 = {'text': '引导、带领', 'pos': '动词', 'diff': '带着人往对的方向走', 'bg': 'blank', 'img': 'art/street-bg.svg', 'items': kids_crossing() + [
    actor('cn-teacher-guide', x=0.3, y=waist(0.84), s=0.84, z=3)]}
pic1 = {'text': '导游、向导', 'pos': '名词', 'diff': '带路、讲解的人', 'bg': 'blank', 'img': 'art/park-bg.svg', 'items': tourists(0.26) + [
    actor('cn-girl-flag', id='g', x=0.32, y=waist(0.84), s=0.84, z=2),
    actor('west-man-tourist', x=0.74, y=waist(0.8), s=0.8, z=2, nodWith='g')]}
pic2 = {'text': '指南、手册', 'pos': '名词', 'diff': '替你带路的书', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 1.0, 's': 0.3, 'z': 1},
    {'svg': 'art/guidebook.svg', 'x': 0.5, 'y': 0.6, 's': 0.5, 'z': 2},
    {'svg': 'art/pencil.svg', 'x': 0.3, 'y': 0.56, 's': 0.05, 'go': [0.42, 0.66], 'dur': 1.4, 'loop': True, 'z': 3}]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': kids_crossing(0.99, 0.36, when='children', cue=0) + [
    actor('cn-teacher-guide', x=0.28, y=waist(0.96), s=0.96, z=3, when='guided', cue=0, fade=0.4),
    {'sound': 'beep', 'when': 'across', 'cue': 0, 'times': 3, 'every': 0.3},
    {'label': '带领', 'x': 0.5, 'y': 0.16, 'size': 0.075, 'when': '带领', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': tourists(0.34) + [
    actor('cn-girl-flag', id='g', x=0.3, y=waist(0.98), s=0.98, z=2, when='guide', cue=0, fade=0.4, turn=[0, 2]),
    actor('west-man-tourist', x=0.7, y=waist(0.9), s=0.9, z=2, nodWith='g', when='showed', cue=0, fade=0.4),
    {'sound': 'footsteps', 'when': 'around', 'cue': 0},
    {'label': '导游', 'x': 0.3, 'y': 0.1, 'size': 0.075, 'when': '导游', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex2 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 1.02, 's': 0.34, 'z': 1},
    {'svg': 'art/guidebook.svg', 'x': 0.5, 'y': 0.58, 's': 0.62, 'when': 'guide', 'cue': 0, 'fade': 0.3, 'z': 2},
    {'svg': 'art/pencil.svg', 'x': 0.36, 'y': 0.5, 's': 0.05, 'go': [0.46, 0.62], 'dur': 1.4, 'loop': True, 'when': 'guide', 'cue': 0, 'z': 3},
    {'sound': 'cash', 'when': 'bought', 'cue': 0},
    {'label': '旅游指南', 'x': 0.84, 'y': 0.16, 'size': 0.075, 'when': '指南', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'The teacher guided the children across the road.', 'exzh': '老师带领孩子们过马路。', 'exPic': ex0})
pic1.update({'ex': 'Our guide showed us around the old town.', 'exzh': '我们的导游带我们参观了古镇。', 'exPic': ex1})
pic2.update({'ex': 'I bought a travel guide to Beijing.', 'exzh': '我买了一本北京旅游指南。', 'exPic': ex2})
P['pics'] = [pic0, pic1, pic2]
W, H = 537, 356
P['distinguish'] = {'key': '带领', 'items': [
    {'w': 'guide', 'gloss': '带领', 'note': '在旁边带着走、指方向、讲解', 'ex': 'guide the visitors',
     'pic': {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': tourists(0.26) + [actor('west-girl-flag', x=0.4, y=waist(0.84), s=0.84, z=2)]}},
    {'w': 'lead', 'gloss': '带领、领头', 'note': '走在最前面领头，别人跟着走', 'ex': 'lead the team',
     'pic': {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [walker('walk-cn-teacher-case', 0.96, 0.4, -0.1, 1.1, 0.12, z=3),
         walker('walk-cn-boy-pack', 0.96, 0.32, -0.1, 1.1, 0.0, z=2), walker('walk-west-boy-pack', 0.96, 0.32, -0.1, 1.1, 0.06, z=1)]}}],
    'tip': 'guide 在旁边指路、讲解；lead 走在最前面领头。'}
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    {'svg': 'art/signpost.svg', 'x': 0.72, 'y': 0.6, 's': 0.6, 'z': 2},
    walker('walk-west-woman-case', 0.97, 0.34, -0.1, 0.6, 0.0, z=3),
    {'label': '指路、带路', 'x': 0.36, 'y': 0.12, 'size': 0.075, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': kids_crossing(0.99, 0.26, when='带着人') + [
    actor('west-woman-guide', x=0.28, y=waist(0.76), s=0.76, z=3, when='带着人'),
    {'label': '带领', 'x': 0.5, 'y': 0.1, 'size': 0.075, 'when': '带领', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6},
    {'label': '动词', 'x': 0.5, 'y': 0.24, 'size': 0.06, 'when': '动词', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': tourists(0.26) + [
    actor('west-girl-flag', x=0.4, y=waist(0.8), s=0.8, z=2, when='带路的人'),
    {'sound': 'footsteps', 'when': '带路的人'},
    {'label': '动作 → 做这事的人', 'x': 0.5, 'y': 0.08, 'size': 0.06, 'when': '名词用', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6},
    {'label': '导游、向导', 'x': 0.76, 'y': 0.24, 'size': 0.07, 'when': '向导', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig3 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 1.0, 's': 0.3, 'z': 1},
    {'svg': 'art/guidebook.svg', 'x': 0.5, 'y': 0.6, 's': 0.48, 'when': '一本书', 'z': 2},
    {'svg': 'art/pencil.svg', 'x': 0.3, 'y': 0.56, 's': 0.05, 'go': [0.42, 0.66], 'dur': 1.4, 'loop': True, 'when': '一本书', 'z': 3},
    {'label': '指南、手册', 'x': 0.5, 'y': 0.12, 'size': 0.07, 'when': '指南', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig4 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    actor('cn-teacher-point', id='t', x=0.3, y=waist(0.8), s=0.8, z=2, when='学'),
    actor('cn-boy-learn', x=0.74, y=waist(0.74), s=0.74, z=2, nodWith='t', when='学'),
    {'label': '指导', 'x': 0.5, 'y': 0.1, 'size': 0.075, 'when': '指导', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
P['flow'] = [
    {'node': '“指路、带路”', 'fig': fig0},
    {'via': '带着人往对的方向走', 'node': '① 引导、带领', 'pos': '动词', 'pic': 0, 'fig': fig1,
     'say': ['带着人往对的方向走，就是引导、带领。它说的是一个动作，所以是动词。']},
    {'via': '带路的那个人', 'node': '② 导游、向导', 'pos': '名词', 'pic': 1, 'fig': fig2,
     'rule': '表示动作的词，也能直接当名词用，指这件事或做一次', 'ruleEx': 'guide 引导、带领 → 向导、导游      walk 走 → 散步',
     'say': ['英语里，表示动作的词，也能直接当名词用。', '带路的人也叫 guide，就是向导、导游。它说的是人，所以是名词。']},
    {'from': 2, 'via': '写成一本书，替你带路', 'node': '③ 指南、手册', 'pos': '名词', 'pic': 2, 'fig': fig3,
     'say': ['写成一本书，替你带路，就是指南、手册。']},
    {'from': 1, 'via': '带着人往对的方向学', 'node': '指导', 'pos': '动词', 'fig': fig4,
     'say': ['带着人往对的方向学、往对的方向做，就是指导。']}]
P['extend'] = ['guidance', 'wise', 'wisdom']
json.dump({'guide': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/owner/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.30（第七十四版）：21 owner（图画书风，第 21–25 个轮回到图画书风）。
# own 拥有：男孩站在自己的新自行车后面竖大拇指；-er：老师（人）和电脑（东西）；物主：小狗跑回主人身边；
# 法律上认他是主人：房子、房产证、钥匙；…的主人：咖啡馆门口招手的店主、跑过来的小狗。讲房子、讲车的画不放旁观的人
P = {'style': 'core', 'board': True}
DOG = ['art/dog_f0.svg', 'art/dog_f1.svg']
def stand(name, x, g, s, **kw):      # 全身的人：脚踩在 g 这条线上
    return actor(name, x=x, y=g - 0.47 * s, s=s, **kw)
def thing(name, x, g, s, foot=1.0, **kw):      # 东西：底边（foot：svg 里着地的那一行占高度的几成）放在 g 上
    d = {'svg': 'art/' + name, 'x': x, 'y': g - (foot - 0.5) * s, 's': s, 'z': 2}
    d.update(kw); return d
def dog(x, g, s, to=None, dur=1.6, **kw):
    d = {'svg': DOG[0], 'frames': DOG, 'fps': 6, 'seq': 'loop', 'x': x, 'y': g - 0.4 * s, 's': s, 'z': 4}
    if to is not None:
        d.update({'go': [to, g - 0.4 * s], 'dur': dur})
    d.update(kw); return d
def boy_bike(x, g, s, who='cn-boy-proud', **kw):      # 男孩站在自己的自行车后面（三处换三个动作：竖大拇指、手放胸口“我的”、指着车）
    return [stand(who, x - 0.06, g, s, z=3, **kw), thing('bike.svg', x + 0.04, g, s * 0.44, foot=0.95, z=4, **kw)]
def lab(t, x, y, size=0.075, **kw):
    d = {'label': t, 'x': x, 'y': y, 'size': size, 'z': 7}
    d.update(kw); return d
BLUE = {'color': '#1A66B8', 'border': '#2F95E6'}
GREEN = {'color': '#2B8A3E', 'border': '#2B8A3E'}
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/home-bg.svg', 'items': boy_bike(0.46, 0.97, 0.84) + [
        lab('拥有 own', 0.5, 0.1, 0.1, when='拥有')]},
    'p1': {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [         # -er：做这件事的人（老师）或东西（电脑）
        actor('cn-teacher-point', x=0.3, y=waist(0.86), s=0.86, z=2),
        {'svg': 'art/computer.svg', 'x': 0.76, 'y': 0.72, 's': 0.3, 'when': '东西', 'fade': 0.3, 'z': 3},
        lab('人', 0.3, 0.1, 0.09, when='人', **BLUE), lab('东西', 0.76, 0.1, 0.09, when='东西', **BLUE),
        lab('拥有东西的人', 0.5, 0.9, 0.08, when='拥有东西', **GREEN)]}}
P['icons'] = {'p0': 'art/icon-own.svg', 'p1': 'art/icon-er.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/home-bg.svg', 'items': boy_bike(0.46, 0.98, 0.92, who='cn-boy-mine') + [
    {'sound': 'sparkle', 'delay': 0.6}, lab('拥有东西的人', 0.5, 0.12, 0.1, delay=0.6)]}
# ======== 意思
W, H = 537, 356
pic0 = {'text': '物主、所有者', 'pos': '名词', 'diff': '东西归他所有的人', 'bg': 'blank', 'img': 'art/park-bg.svg', 'items': [
    walker('walk-cn-girl', 0.8, 0.34, 1.1, -0.1, 0.0, z=1), walker('walk-west-man-case', 0.8, 0.36, -0.1, 1.1, 0.5, z=1),
    stand('west-woman-call', 0.3, 0.96, 0.86, z=3), dog(0.92, 0.96, 0.24, to=0.52, delay=0.4)]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': [
    walker('walk-cn-teacher-case', 0.78, 0.36, 1.1, -0.1, 0.0, z=1), walker('walk-west-boy-pack', 0.78, 0.32, -0.1, 1.1, 0.4, z=1),
    stand('west-woman-call', 0.24, 0.97, 0.9, z=3),
    dog(1.02, 0.97, 0.26, to=0.42, dur=2.0, when='dog', cue=0),
    {'sound': 'dog', 'when': 'ran', 'cue': 0},
    lab('主人', 0.24, 0.12, 0.075, when='主人', cue=1, **BLUE)]}
pic0.update({'ex': 'The dog ran back to its owner.', 'exzh': '狗跑回了它的主人身边。', 'exPic': ex0})
P['pics'] = [pic0]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/home-bg.svg', 'items': boy_bike(0.46, 0.97, 0.8, who='cn-boy-pointbike') + [lab('拥有东西的人', 0.5, 0.1, 0.07, delay=0.3)]}
fig1 = {'bg': 'blank', 'img': 'art/home-bg.svg', 'items': [
    thing('house.svg', 0.64, 0.92, 0.66, foot=0.995, z=1),
    stand('west-man-owner', 0.24, 0.97, 0.78, z=3),
    {'svg': 'art/deed.svg', 'x': 0.5, 'y': 0.3, 's': 0.3, 'when': '法律上', 'fade': 0.3, 'anim': 'sway', 'z': 5},
    {'svg': 'art/key.svg', 'x': 0.26, 'y': 0.28, 's': 0.1, 'when': '物主', 'fade': 0.3, 'anim': 'sway', 'z': 5},
    {'sound': 'keys', 'when': '物主'},
    lab('房子的主人', 0.5, 0.07, 0.065, when='物主', **GREEN), lab('名词', 0.84, 0.07, 0.06, when='名词')]}
fig2 = {'bg': 'blank', 'img': 'art/cafe-bg.svg', 'items': [
    actor('cn-teacher-shop', x=0.62, y=waist(0.8), s=0.8, z=3),
    {'sound': 'ding', 'when': 'shop'},
    lab('shop owner 店主', 0.62, 0.1, 0.065, when='shop', **GREEN),
    dog(1.05, 0.98, 0.2, to=0.2, dur=1.8, when='dog'),
    lab('dog owner 狗主人', 0.24, 0.62, 0.06, when='dog', delay=1.6, color='#7B57D6', border='#7B57D6')]}
P['flow'] = [
    {'node': '“拥有东西的人”', 'fig': fig0},
    {'via': '东西归他，法律上也认他是主人', 'node': '① 物主、所有者', 'pos': '名词', 'pic': 0, 'fig': fig1,
     'say': ['14 世纪，owner 就指有合法所有权的人：东西归他，法律上也认他是主人。', '这就是物主、所有者。它说的是人，所以是名词。']},
    {'via': '放在别的名词后面', 'node': '…的主人', 'fig': fig2,
     'rule': '最后一个词是主体，前面的词说明它', 'ruleEx': 'shop owner 店主      dog owner 狗主人',
     'say': ['英语里，最后一个词是主体，前面的词说明它。', 'owner 前面放上 shop，就是店的主人，店主；放上 dog，就是狗主人。']}]
P['extend'] = ['own', 'homeowner', 'ownership']
P['fengong'] = False   # 精简版不讲后缀辨析（-er、-or、-ist）
# ======== 同义词辨析：owner / holder
W, H = 504, 204
P['distinguish'] = {'pics': {
    'owner': {'bg': 'blank', 'img': 'art/home-bg.svg', 'items': [thing('house.svg', 0.62, 0.95, 0.8, foot=0.995, z=1),
              stand('west-man-owner', 0.24, 0.99, 0.9, z=3)]},
    'holder': {'bg': 'blank', 'img': 'art/cafe-bg.svg', 'items': [actor('west-man-card', x=0.5, y=waist(0.96), s=0.96, z=3)]}},
    'logic': 'owner 从 own（拥有）来，说东西归谁；holder 从 hold（拿着）来，只说谁拿着。'}
json.dump({'owner': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

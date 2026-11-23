import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/protect/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.29.2：16 protect（中西合璧风的第一个）。pro- 在前面：盾牌挪到房子前面；tect 盖：屋顶落到房子上；
# 保护：伞挡住雨；防护：墨镜挡住太阳；保护本国产业：关税这面盾牌挡住进口货。辨析 protect / preserve / shield
P = {'style': 'core', 'board': True}
SUN = ['art/sun_f0.svg', 'art/sun_f1.svg']
def house(x, yb, sb, roof_go=None, **kw):
    """房子 = 墙（house-body）+ 屋顶（roof）；roof_go：屋顶从上面落下来（when / delay 写在 kw 里）"""
    top_wall = yb - sb / 2 + sb * 20 / 230
    sr = sb * 128 / 230
    yr = top_wall - sr * (118 / 128 - 0.5)
    body = {'svg': 'art/house-body.svg', 'x': x, 'y': yb, 's': sb, 'z': 1}
    rf = {'svg': 'art/roof.svg', 'x': x, 'y': yr, 's': sr, 'z': 2}
    if roof_go:
        rf.update({'y': yr - roof_go, 'go': [x, yr], 'dur': 0.9}); rf.update(kw)
    return [body, rf]
def shield(x, y, s, **kw):
    d = {'svg': 'art/shield.svg', 'x': x, 'y': y, 's': s, 'z': 4}
    d.update(kw); return d
def rain(x=0.5, y=0.05, sx=0.9, **kw):
    d = {'emit': True, 'svg': 'art/streak.svg', 'x': x, 'y': y, 'spreadX': sx, 's': 0.06, 'to': [-0.02, 0.6], 'life': 0.9, 'every': 0.06, 'z': 5}
    d.update(kw); return d
def sun(x, y, s, **kw):
    d = {'svg': SUN[0], 'frames': SUN, 'fps': 2, 'seq': 'loop', 'x': x, 'y': y, 's': s, 'z': 2}
    d.update(kw); return d
def crates(y, s, x1, **kw):   # 进口货一箱箱推过来，被盾牌挡住
    out = []
    for k in range(2):
        d = {'svg': 'art/crate.svg', 'x': 1.12, 'y': y + 0.04 * k, 's': s, 'go': [x1 + 0.03 * k, y + 0.04 * k], 'dur': 1.6, 'loop': True, 'delay': 0.8 * k, 'z': 3}
        d.update(kw); out.append(d)
    return out
def strollers(s=0.26, y=0.99):
    return [walker('walk-cn-girl', y, s, -0.1, 1.1, 0.2, z=1), walker('walk-west-boy-pack', y, s * 0.95, 1.1, -0.1, 0.6, z=1)]
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': house(0.42, 0.62, 0.36) + [      # pro- 在前面：盾牌挪到房子前面（不放人）
        shield(0.95, 0.74, 0.34, go=[0.62, 0.74], dur=1.0, delay=0.3),
        {'label': '在前面', 'x': 0.5, 'y': 0.1, 'size': 0.1, 'when': '在前面', 'z': 6}]},
    'p1': {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': house(0.5, 0.66, 0.4, roof_go=0.5, delay=0.3) + [   # tect 盖：屋顶盖到房子上
        {'label': '盖、遮 tect', 'x': 0.5, 'y': 0.1, 'size': 0.1, 'when': '盖', 'z': 6}]}}
P['icons'] = {'p0': 'art/icon-front.svg', 'p1': 'art/icon-cover.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': house(0.42, 0.66, 0.5) + [
    shield(0.62, 0.76, 0.42), rain(0.5, 0.0, 0.9, delay=0.4),
    {'sound': 'rain', 'delay': 0.4},
    {'label': '在前面盖住', 'x': 0.5, 'y': 0.1, 'size': 0.1, 'delay': 0.6, 'z': 6}]}
# ======== 意思
W, H = 537, 356
pic0 = {'text': '保护', 'pos': '动词', 'diff': '挡在前面，不让受到伤害', 'bg': 'blank', 'img': 'art/street-bg.svg', 'items': [
    walker('walk-west-man-case', 0.99, 0.28, 1.1, -0.1, 0.4, z=1), rain(),
    actor('cn-girl-umbrella', x=0.5, y=waist(0.86), s=0.86, z=2)]}
pic1 = {'text': '防护', 'pos': '动词', 'diff': '戴上东西，把伤害挡在外面', 'bg': 'blank', 'img': 'art/park-bg.svg', 'items': strollers() + [
    sun(0.84, 0.16, 0.26), actor('cn-boy-shades', x=0.4, y=waist(0.86), s=0.86, z=2)]}
pic2 = {'text': '保护本国产业', 'pos': '动词', 'diff': '国家用关税挡在前面，护住本国的产业', 'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    shield(0.6, 0.66, 0.5), *crates(0.72, 0.22, 0.72),
    {'label': '关税', 'x': 0.6, 'y': 0.3, 'size': 0.08, 'delay': 0.6, 'z': 6}]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': [
    walker('walk-west-woman-case', 0.99, 0.34, -0.1, 1.1, 0.2, z=1), rain(0.5, 0.0, 1.0),
    actor('cn-girl-umbrella', x=0.5, y=waist(0.98), s=0.98, z=2, when='umbrella', cue=0, fade=0.4),
    {'sound': 'rain', 'cue': 0, 'gap': True},
    {'label': '保护', 'x': 0.78, 'y': 0.16, 'size': 0.075, 'when': '保护', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': strollers(0.34) + [
    sun(0.86, 0.2, 0.34),
    actor('cn-boy-shades', x=0.42, y=waist(0.98), s=0.98, z=2, when='Sunglasses', cue=0, fade=0.4),
    {'sound': 'sparkle', 'when': 'sun', 'cue': 0},
    {'label': '保护眼睛', 'x': 0.18, 'y': 0.16, 'size': 0.075, 'when': '眼睛', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex2 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    shield(0.55, 0.66, 0.56, when='protects', cue=0, fade=0.4), *crates(0.74, 0.26, 0.64, when='protects', cue=0),
    {'sound': 'thud', 'when': 'protects', 'cue': 0, 'delay': 1.2},
    {'label': '保护本国农民', 'x': 0.2, 'y': 0.16, 'size': 0.075, 'when': '保护', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'The umbrella protects the girl from the rain.', 'exzh': '伞保护女孩不被雨淋。', 'exPic': ex0})
pic1.update({'ex': 'Sunglasses protect our eyes from the sun.', 'exzh': '太阳镜保护我们的眼睛不受阳光伤害。', 'exPic': ex1})
pic2.update({'ex': 'The country protects its own farmers.', 'exzh': '这个国家保护本国的农民。', 'exPic': ex2})
P['pics'] = [pic0, pic1, pic2]
# ======== 同义词辨析：protect / preserve / shield
W, H = 537, 356
P['distinguish'] = {'key': '保护', 'items': [
    {'w': 'protect', 'gloss': '保护', 'note': '挡在前面，防伤害', 'ex': 'protect your eyes',
     'pic': {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': strollers() + [rain(), actor('west-man-umbrella', x=0.45, y=waist(0.86), s=0.86, z=2)]}},
    {'w': 'preserve', 'gloss': '保存、保护', 'note': '让东西一直保持原样，不变坏', 'ex': 'preserve old buildings',
     'pic': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
         {'svg': 'art/glasscase.svg', 'x': 0.5, 'y': 0.56, 's': 0.8, 'z': 1}, {'svg': 'art/vase.svg', 'x': 0.5, 'y': 0.46, 's': 0.42, 'z': 2},
         {'emit': True, 'svg': 'art/star.svg', 'x': 0.5, 'y': 0.4, 'spreadX': 0.3, 's': 0.08, 'to': [0.0, -0.06], 'life': 1.2, 'every': 0.5, 'spin': 0.8, 'z': 4}]}},
    {'w': 'shield', 'gloss': '挡住、保护', 'note': '隔在你和危险之间的那块挡板', 'ex': 'shield your eyes',
     'pic': {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': strollers() + [
         actor('west-boy-shield', x=0.36, y=waist(0.86), s=0.86, z=2),
         {'svg': 'art/ball.svg', 'x': 1.05, 'y': 0.55, 's': 0.1, 'go': [0.56, 0.6], 'dur': 0.9, 'loop': True, 'z': 4},
         {'svg': 'art/ball2.svg', 'x': 1.1, 'y': 0.7, 's': 0.1, 'go': [0.56, 0.68], 'dur': 1.1, 'loop': True, 'delay': 0.4, 'z': 4}]}}],
    'logic': 'protect 挡在前面防伤害；preserve 让东西一直保持原样；shield 是隔在中间的那块挡板。'}
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': house(0.42, 0.66, 0.42) + [
    shield(0.64, 0.76, 0.36, go=[0.62, 0.74], dur=1.6, loop=True),
    {'label': '在前面 + 盖住', 'x': 0.5, 'y': 0.1, 'size': 0.075, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': house(0.3, 0.66, 0.36, roof_go=0.4, when='屋顶') + [
    shield(0.18, 0.78, 0.3, when='盾牌'),
    actor('west-man-umbrella', x=0.74, y=waist(0.72), s=0.72, z=3, when='伞'),
    rain(0.5, 0.0, 0.9, when='伞'),
    {'label': '保护', 'x': 0.5, 'y': 0.1, 'size': 0.075, 'when': '保护', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6},
    {'label': '动词', 'x': 0.5, 'y': 0.22, 'size': 0.06, 'when': '动词', 'z': 6}]}
fig2 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': strollers() + [
    sun(0.84, 0.16, 0.26), actor('west-girl-shades', x=0.42, y=waist(0.82), s=0.82, z=2, when='墨镜'),
    {'label': '挡在外面', 'x': 0.5, 'y': 0.1, 'size': 0.065, 'when': '挡在外面', 'z': 6},
    {'label': '防护', 'x': 0.5, 'y': 0.22, 'size': 0.07, 'when': '防护', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig3 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': [
    shield(0.5, 0.66, 0.46, when='关税'), *crates(0.74, 0.2, 0.62, when='关税'),
    {'sound': 'thud', 'when': '关税', 'delay': 1.2},
    {'label': '关税', 'x': 0.5, 'y': 0.34, 'size': 0.07, 'when': '关税', 'z': 6},
    {'label': '换了对象：产业', 'x': 0.5, 'y': 0.1, 'size': 0.065, 'when': '核心意思', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6},
    {'label': '保护本国产业', 'x': 0.5, 'y': 0.93, 'size': 0.065, 'when': '本国产业', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
P['flow'] = [
    {'node': '“在前面盖住”', 'fig': fig0},
    {'via': '挡在前面、盖在上面', 'node': '① 保护', 'pos': '动词', 'pic': 0, 'fig': fig1,
     'say': ['一面盾牌挡在身前，一把伞撑在头顶，一片屋顶罩住一家人，这就是保护。它说的是一个动作，所以是动词。']},
    {'from': 1, 'via': '戴上东西挡住伤害', 'node': '② 防护', 'pos': '动词', 'pic': 1, 'fig': fig2,
     'say': ['戴上墨镜，把刺眼的阳光挡在外面，也是保护，就是防护。']},
    {'from': 1, 'via': '国家用关税挡在前面', 'node': '③ 保护本国产业', 'pos': '动词', 'pic': 2, 'fig': fig3,
     'rule': '词的核心意思不变，换了对象、场合，中文要换个说法，英语还是这个词', 'ruleEx': 'protect 保护人 → 保护产业      play 玩 → 踢（球）、演奏（乐器）',
     'say': ['英语里，词的核心意思不变，换了对象、场合，中文要换个说法，英语还是这个词。', '国家用关税挡在前面，护住本国的产业，也是 protect，就是保护本国产业。']}]
P['extend'] = ['detect', 'provide', 'produce', 'project']
P['fengong'] = False   # 精简版不讲前缀辨析
json.dump({'protect': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

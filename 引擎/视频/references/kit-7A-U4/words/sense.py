import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/sense/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 规律照抄总表“用词规律”的原话（小黑板去重靠原话对得上，不然同一条会写两遍）。6.30（第七十四版）：28 sense（青绿工笔风）。画图脚本：owner,sense。五个意思画三个：感觉、…感、道理；“意思”“觉察到”只在演变里讲。
# 演变照总表：感觉、感知 → 意思（最早）→ 感觉（五官）→ …感、意识 → 明智、道理 → 觉察到（总表规律：表示东西的词直接当动词用）。辨析 sense / feeling
P = {'style': 'core', 'board': True}
DOG = ['art/dog_f0.svg', 'art/dog_f1.svg']; BULB = ['art/bulb_f0.svg', 'art/bulb_f1.svg']; CAT = ['art/cat-sit_f%d.svg' % k for k in range(3)]
def lab(t, x, y, size=0.075, **kw):
    d = {'label': t, 'x': x, 'y': y, 'size': size, 'z': 7}
    d.update(kw); return d
BLUE = {'color': '#1A66B8', 'border': '#2F95E6'}
GREEN = {'color': '#2B8A3E', 'border': '#2B8A3E'}
def scent(x, y, **kw):     # 一缕缕香味往上飘
    d = {'emit': True, 'svg': 'art/scent.svg', 'x': x, 'y': y, 's': 0.12, 'to': [0.02, -0.22], 'life': 2.0, 'every': 0.6, 'wobble': 0.03, 'z': 4}
    d.update(kw); return d
def dog(x, g, s, to=None, dur=1.6, **kw):
    d = {'svg': DOG[0], 'frames': DOG, 'fps': 6, 'seq': 'loop', 'x': x, 'y': g - 0.4 * s, 's': s, 'z': 4}
    if to is not None:
        d.update({'go': [to, g - 0.4 * s], 'dur': dur})
    d.update(kw); return d
def bulb(x, y, s, when=None, cue=None):     # 灯泡：不写 when 就一闪一闪；写了 when，说到时亮起来
    if not when:
        return [{'svg': BULB[0], 'frames': BULB, 'fps': 1, 'seq': 'pingpong', 'x': x, 'y': y, 's': s, 'z': 5}]
    a = {'svg': BULB[0], 'x': x, 'y': y, 's': s, 'z': 5, 'hideWhen': when}
    b = {'svg': BULB[1], 'x': x, 'y': y, 's': s, 'z': 6, 'when': when, 'fade': 0.2, 'anim': 'sway'}
    if cue is not None:
        a['hideCue'] = cue; b['cue'] = cue
    return [a, b]
def strollers(y=0.8, s=0.28):      # 公园远处散步的人（公园里要有人走动）
    return [walker('walk-cn-teacher-case', y, s, 1.1, -0.1, 0.0, z=1), walker('walk-west-boy-pack', y, s * 0.9, -0.1, 1.1, 0.5, z=1)]
def joke(bx=0.24, s=0.86, laugh_when=None, cue=None, who=('west-boy-joke', 'cn-girl-laugh', 'cn-boy-laugh')):    # 一个讲笑话，两个笑（说完一句就点头）
    kw = {'when': laugh_when, 'fade': 0.3} if laugh_when else {}
    if laugh_when and cue is not None:
        kw['cue'] = cue
    return strollers() + [actor(who[0], id='b', x=bx, y=waist(s), s=s, z=3),
            actor(who[1], x=bx + 0.32, y=waist(s * 0.9), s=s * 0.9, z=2, nodWith='b', **kw),
            actor(who[2], x=bx + 0.58, y=waist(s * 0.86), s=s * 0.86, z=2, nodWith='b', **kw)]
def smell(gx=0.3, s=0.86):      # 女孩闭着眼闻花香
    return strollers() + [{'svg': 'art/flowerbed.svg', 'x': gx + 0.36, 'y': 0.86, 's': 0.3, 'z': 2}, scent(gx + 0.3, 0.68), scent(gx + 0.44, 0.7, offset=0.3),
            actor('west-girl-smell', x=gx, y=waist(s), s=s, z=3)]
# ======== 来历：拉丁语 sensus“感觉、感知”
W, H = 537, 356
P['originPic'] = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': smell(0.26, 0.84) + [lab('sensus', 0.5, 0.1, 0.08, when='sensus', **BLUE)]}
# ======== 意思（五个画三个）
W, H = 537, 356
pic0 = {'text': '感觉', 'pos': '名词', 'diff': '眼、耳、鼻、舌、身感觉到的', 'bg': 'blank', 'img': 'art/park-bg.svg', 'items': strollers() + [
    {'svg': 'art/senses.svg', 'x': 0.66, 'y': 0.5, 's': 0.86, 'anim': 'sway', 'z': 2}, actor('west-girl-smell', x=0.2, y=waist(0.84), s=0.84, z=3)]}
pic1 = {'text': '…感、意识', 'pos': '名词', 'diff': '对某方面特别能感觉到', 'bg': 'blank', 'img': 'art/park-bg.svg', 'items': joke()}
pic2 = {'text': '道理、明智', 'pos': '名词', 'diff': '心里明白对不对、该不该', 'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    actor('cn-teacher-point', id='t', x=0.26, y=waist(0.86), s=0.86, z=3), actor('west-girl-idea', x=0.72, y=waist(0.84), s=0.84, z=3, nodWith='t')] + bulb(0.84, 0.16, 0.2)}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': strollers(0.78, 0.3) + [
    {'svg': 'art/bone.svg', 'x': 0.3, 'y': 0.92, 's': 0.08, 'z': 3}, scent(0.3, 0.8, when='smell', cue=0),
    dog(1.1, 0.97, 0.26, to=0.44, dur=2.2, when='Dogs', cue=0),
    {'sound': 'dog', 'when': 'smell', 'cue': 0}, lab('嗅觉', 0.3, 0.1, 0.075, when='嗅觉', cue=1, **BLUE)]}
ex1 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': joke(0.2, 0.94, laugh_when='humour', cue=0) + [
    {'sound': 'boing', 'when': 'humour', 'cue': 0}, lab('幽默感', 0.5, 0.08, 0.075, when='幽默感', cue=1, **BLUE)]}
ex2 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    actor('cn-teacher-point', id='t', x=0.24, y=waist(0.94), s=0.94, z=3), actor('west-girl-idea', x=0.7, y=waist(0.92), s=0.92, z=3, nodWith='t')] +
    bulb(0.82, 0.16, 0.22, when='sense', cue=0) + [
    {'sound': 'ding', 'when': 'sense', 'cue': 0}, lab('有道理', 0.5, 0.08, 0.075, when='有道理', cue=1, **BLUE)]}
pic0.update({'ex': 'Dogs have a good sense of smell.', 'exzh': '狗的嗅觉很灵敏。', 'exPic': ex0})
pic1.update({'ex': 'Tom has a good sense of humour.', 'exzh': '汤姆很有幽默感。', 'exPic': ex1})
pic2.update({'ex': 'What you said makes sense.', 'exzh': '你说的有道理。', 'exPic': ex2})
P['pics'] = [pic0, pic1, pic2]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': smell(0.24, 0.8) + [lab('感觉、感知', 0.5, 0.08, 0.07, delay=0.3)]}
fig1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [actor('west-man-read', x=0.5, y=waist(0.9), s=0.9, z=3),
    lab('意思', 0.5, 0.08, 0.07, when='意思', **GREEN)]}
fig2 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': strollers() + [{'svg': 'art/senses.svg', 'x': 0.5, 'y': 0.52, 's': 0.86, 'when': '眼', 'fade': 0.3, 'anim': 'sway', 'z': 2},
    lab('感觉', 0.16, 0.08, 0.07, when='感觉', **GREEN), lab('名词', 0.86, 0.08, 0.06, when='名词')]}
fig3 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': joke(0.2, 0.8, who=('west-girl-explain', 'cn-teacher-laugh', 'west-man-smile')) + [lab('sense of humour 幽默感', 0.5, 0.08, 0.06, when='幽默感', **GREEN)]}
fig4 = {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [
    actor('west-man-point', id='t', x=0.26, y=waist(0.84), s=0.84, z=3), actor('cn-boy-raise', x=0.72, y=waist(0.82), s=0.82, z=3, nodWith='t')] +
    bulb(0.84, 0.16, 0.2, when='道理') + [lab('明智', 0.3, 0.08, 0.065, when='明智'), lab('有道理', 0.56, 0.08, 0.065, when='有道理', **GREEN)]}
fig5 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': CAT[0], 'frames': CAT, 'fps': 2, 'seq': 'pingpong', 'x': 0.5, 'y': 0.66, 's': 0.5, 'z': 3},
    {'sound': 'thunder', 'when': '觉察到'}, lab('！', 0.66, 0.36, 0.12, when='觉察到'),
    lab('觉察到', 0.24, 0.08, 0.07, when='觉察到', **GREEN), lab('动词', 0.84, 0.08, 0.06, when='动词')]}
P['flow'] = [
    {'node': '“感觉、感知”', 'fig': fig0},
    {'via': '话里让人感觉到的东西', 'node': '意思', 'fig': fig1,
     'say': ['最早，话里让人感觉到的东西，就是它的意思、含义。']},
    {'via': '眼、耳、鼻、舌、身', 'node': '① 感觉', 'pos': '名词', 'pic': 0, 'fig': fig2,
     'say': ['能感觉到东西的本事，眼、耳、鼻、舌、身，每一种都是一种感觉。它说的是东西，所以是名词。']},
    {'via': '对某一方面特别能感觉到', 'node': '② …感、意识', 'pos': '名词', 'pic': 1, 'fig': fig3,
     'say': ['对某一方面特别能感觉到，就是…感、意识，比如幽默感。']},
    {'via': '心里感觉出对不对', 'node': '③ 道理、明智', 'pos': '名词', 'pic': 2, 'fig': fig4,
     'say': ['心里能感觉出对不对、该不该，就是明智；说得通，就是有道理。']},
    {'via': '直接当动词用', 'node': '觉察到', 'pos': '动词', 'fig': fig5,
     'rule': '表示东西、性质的词，也能直接当动词用：用这样东西做事，或者使变成这样', 'ruleEx': 'sense 感觉 → 觉察到、意识到；water 水 → 浇水',
     'say': ['英语里，表示东西的词，也能直接当动词用。', '凭感觉知道，就是觉察到，这里是动词。']}]
P['extend'] = ['sensor', 'sensible', 'nonsense']
# ======== 同义词辨析：sense / feeling
W, H = 504, 204
P['distinguish'] = {'key': '感觉', 'items': [
    {'w': 'sense', 'gloss': '感觉、感官', 'note': '偏感官、意识', 'ex': 'a sense of humour',
     'pic': {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': strollers(0.82, 0.36) + [{'svg': 'art/senses.svg', 'x': 0.5, 'y': 0.52, 's': 0.96, 'anim': 'sway', 'z': 2}]}},
    {'w': 'feeling', 'gloss': '感受', 'note': '偏一时的、具体的感受', 'ex': 'a happy feeling',
     'pic': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [actor('cn-girl-gift', x=0.5, y=waist(0.96), s=0.96, z=3)]}}],
    'tip': 'sense 偏感官、意识；feeling 偏一时的、具体的感受。'}
json.dump({'sense': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

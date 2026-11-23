import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/shower/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
P = {'style': 'core', 'board': True}
def rain(x0=0.0, x1=1.0, y=0.05, n=6, **kw):   # 雨一道道斜着落下来
    out = []
    for k in range(n):
        d = {'emit': True, 'svg': 'art/streak.svg', 'x': x0 + (x1 - x0) * (k + 0.5) / n, 'y': y, 's': 0.07, 'to': [-0.05, 0.75], 'life': 0.9,
             'every': 0.3, 'offset': 0.05 * k, 'z': 6}
        d.update(kw); out.append(d)
    return out
def walkers():
    return [walker('walk-west-woman-case', 0.97, 0.36, -0.1, 1.1, 0.2, z=1), walker('walk-cn-boy-pack', 0.95, 0.34, 1.1, -0.1, 0.9, z=1)]
STEAM = {'emit': True, 'svg': 'art/steam.svg', 'x': 0.5, 'y': 0.45, 's': 0.12, 'to': [0, -0.12], 'life': 1.6, 'every': 0.8, 'z': 6}
def spray(x, y, s=0.06, **kw):   # 花洒出水
    d = [{'emit': True, 'svg': 'art/drop.svg', 'x': x + dx, 'y': y, 's': s, 'to': [dx * 0.6, 0.55], 'life': 0.8, 'every': 0.25, 'offset': 0.08 * k, 'z': 5}
         for k, dx in enumerate((-0.03, 0.0, 0.03))]
    d.append({'emit': True, 'svg': 'art/steam.svg', 'x': x, 'y': y + 0.25, 's': 0.12, 'to': [0, -0.12], 'life': 1.6, 'every': 0.8, 'z': 6})
    for it in d: it.update(kw)
    return d
W, H = 537, 356
P['originPic'] = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': rain() + [{'sound': 'rain', 'delay': 0.5},
    {'label': '阵雨、风暴', 'x': 0.5, 'y': 0.12, 'size': 0.08, 'delay': 0.6, 'z': 7}]}
pic0 = {'text': '阵雨', 'pos': '名词', 'diff': '哗地下一阵又停的雨', 'bg': 'blank', 'img': 'art/street-bg.svg', 'items': rain() + walkers() + [
    actor('cn-girl-umbrella', id='g', x=0.3, y=waist(0.9), s=0.9, z=2), actor('west-man-umbrella', x=0.72, y=waist(0.9), s=0.9, z=2, nodWith='g')]}
pic1 = {'text': '淋浴', 'pos': '名词', 'diff': '站在花洒下面洗澡', 'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [
    actor('boy-cap', x=0.5, y=0.52, s=0.62, z=1),
    {'svg': 'art/stall.svg', 'x': 0.5, 'y': 0.56, 's': 0.9, 'z': 2}] + spray(0.53, 0.2)}
pic2 = {'text': '淋浴间', 'pos': '名词', 'diff': '洗淋浴的小隔间', 'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [
    {'svg': 'art/stall-open.svg', 'x': 0.5, 'y': 0.56, 's': 0.9, 'z': 2}, dict(STEAM), {'label': '淋浴间', 'x': 0.82, 'y': 0.2, 'size': 0.08, 'delay': 0.6, 'z': 6}]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': rain(when='shower', cue=0) + walkers() + [
    {'sound': 'rain', 'when': 'shower', 'cue': 0},
    actor('cn-girl-umbrella', id='g', x=0.3, y=waist(0.95), s=0.95, z=2), actor('west-man-umbrella', x=0.62, y=waist(0.95), s=0.95, z=2, nodWith='g'),
    {'label': '阵雨', 'x': 0.86, 'y': 0.2, 'size': 0.075, 'when': '阵雨', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex1 = {'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [
    actor('boy-cap', x=0.5, y=0.52, s=0.66, z=1), {'svg': 'art/stall.svg', 'x': 0.5, 'y': 0.56, 's': 0.95, 'z': 2}] + spray(0.52, 0.2, when='shower', cue=0) + [
    {'sound': 'water', 'when': 'shower', 'cue': 0},
    {'label': '淋浴', 'x': 0.78, 'y': 0.2, 'size': 0.075, 'when': '淋浴', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
ex2 = {'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [dict(STEAM, x=0.3),
    {'svg': 'art/stall-open.svg', 'x': 0.3, 'y': 0.56, 's': 0.9, 'z': 2, 'when': 'shower', 'cue': 0, 'fade': 0.4},
    {'ray': [[0.42, 0.4], [0.55, 0.4]], 'arrow': True, 'color': '#C2410C', 'lw': 0.01, 'when': 'next to', 'cue': 0, 'z': 6},
    {'label': '淋浴间', 'x': 0.3, 'y': 0.12, 'size': 0.075, 'when': '淋浴间', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7},
    {'label': '洗手池', 'x': 0.6, 'y': 0.12, 'size': 0.07, 'when': '洗手池', 'cue': 1, 'z': 7}]}
pic0.update({'ex': 'We got caught in a shower on the way home.', 'exzh': '回家路上，我们遇上了一场阵雨。', 'exPic': ex0})
pic1.update({'ex': 'I take a shower every morning.', 'exzh': '我每天早上洗个淋浴。', 'exPic': ex1})
pic2.update({'ex': 'The shower is next to the sink.', 'exzh': '淋浴间在洗手池旁边。', 'exPic': ex2})
P['pics'] = [pic0, pic1, pic2]
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/wild-bg.svg', 'items': rain() + [{'label': '阵雨、风暴', 'x': 0.5, 'y': 0.12, 'size': 0.075, 'delay': 0.3, 'z': 7}]}
fig1 = {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': rain(when='下一阵') + walkers() + [
    {'label': '阵雨', 'x': 0.82, 'y': 0.15, 'size': 0.075, 'when': '阵雨', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 7}]}
fig2 = {'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [actor('boy-cap', x=0.5, y=0.52, s=0.6, z=1, when='站在'), {'svg': 'art/stall.svg', 'x': 0.5, 'y': 0.56, 's': 0.88, 'z': 2}] +
    spray(0.53, 0.2, when='淋下') + [{'label': '像一阵雨', 'x': 0.82, 'y': 0.15, 'size': 0.065, 'when': '像一阵雨', 'z': 7},
    {'label': '淋浴', 'x': 0.82, 'y': 0.3, 'size': 0.075, 'when': '淋浴', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 7}]}
fig3 = {'bg': 'blank', 'img': 'art/bathroom-bg.svg', 'items': [{'svg': 'art/stall-open.svg', 'x': 0.5, 'y': 0.56, 's': 0.88, 'z': 2, 'when': '小隔间'},
    {'emit': True, 'svg': 'art/steam.svg', 'x': 0.5, 'y': 0.4, 's': 0.12, 'to': [0, -0.12], 'life': 1.6, 'every': 0.8, 'z': 6},
    {'label': '淋浴间', 'x': 0.82, 'y': 0.15, 'size': 0.075, 'when': '淋浴间', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 7}]}
P['flow'] = [
    {'node': '“阵雨、风暴”', 'fig': fig0},
    {'via': '雨哗地下一阵又停', 'node': '① 阵雨', 'pos': '名词', 'pic': 0, 'fig': fig1, 'say': ['雨哗地下一阵又停，就是阵雨。它说的是一种雨，所以是名词。']},
    {'via': '人站在下面，水像一阵雨从头顶淋下', 'node': '② 淋浴', 'pos': '名词', 'pic': 1, 'fig': fig2,
     'say': ['后来人站在花洒下面，让水从头顶淋下来，像一阵雨一样，这就是淋浴。']},
    {'via': '洗淋浴的地方', 'node': '③ 淋浴间', 'pos': '名词', 'pic': 2, 'fig': fig3, 'say': ['洗淋浴的那个小隔间，就是淋浴间。']}]
P['distinguish'] = False
P['text'] = {'origin': '英语本族的基础词，指“一阵短促的雨、风暴”'}   # 6.29.2：总表那一格引号里有“；”，自动截出来只剩“指”
json.dump({'shower': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

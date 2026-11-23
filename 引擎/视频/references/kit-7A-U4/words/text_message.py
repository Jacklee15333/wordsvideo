import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/text_message/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.29.2：12 text message（水墨写意风）。text 文字：本子上写字；message 消息：说话气泡里一封信；短信：手机聊天框一条条出来
P = {'style': 'core', 'board': True}
def chat(k, x, y, s, **kw):
    d = {'svg': 'art/chat%d.svg' % k, 'x': x, 'y': y, 's': s, 'z': 3}
    d.update(kw); return d
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [          # text 文字：本子上一行行写出字来（不放人）
        {'svg': 'art/desk.svg', 'x': 0.5, 'y': 0.98, 's': 0.32, 'z': 1},
        {'svg': 'art/notebook.svg', 'x': 0.5, 'y': 0.62, 's': 0.42, 'z': 2},
        {'svg': 'art/writing.svg', 'x': 0.5, 'y': 0.62, 's': 0.42, 'delay': 0.5, 'fade': 0.8, 'z': 3},
        {'svg': 'art/pencil.svg', 'x': 0.3, 'y': 0.56, 's': 0.06, 'go': [0.6, 0.66], 'dur': 1.6, 'loop': True, 'z': 4},
        {'label': '文字 text', 'x': 0.5, 'y': 0.14, 'size': 0.1, 'when': '文字', 'z': 6}]},
    'p1': {'bg': 'blank', 'img': 'art/classroom-bg.svg', 'items': [     # message 消息：女孩给老师带个口信
        actor('west-girl-explain', id='g', x=0.28, y=waist(0.86), s=0.86, z=2),
        actor('cn-teacher-listen', x=0.76, y=waist(0.8), s=0.8, z=1, nodWith='g'),
        {'svg': 'art/msg-bubble.svg', 'x': 0.56, 'y': 0.3, 's': 0.3, 'delay': 0.4, 'z': 5},
        {'label': '消息 message', 'x': 0.5, 'y': 0.1, 'size': 0.09, 'when': '消息', 'z': 6}]}}
P['icons'] = {'p0': 'art/icon-text.svg', 'p1': 'art/icon-message.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('cn-girl-type', x=0.26, y=waist(1.0), s=1.0, z=2),
    {'svg': 'art/msg-bubble.svg', 'x': 0.5, 'y': 0.55, 's': 0.3, 'go': [0.84, 0.36], 'dur': 1.2, 'delay': 0.4, 'z': 5},
    {'sound': 'whoosh', 'delay': 0.5},
    {'label': '用文字发的消息', 'x': 0.68, 'y': 0.14, 'size': 0.1, 'delay': 0.8, 'z': 6}]}
# ======== 意思
W, H = 537, 356
pic0 = {'text': '短信', 'pos': '名词', 'diff': '用手机打字发出去的消息', 'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('cn-boy-type', x=0.26, y=waist(0.95), s=0.95, z=2),
    chat(0, 0.72, 0.52, 0.9), chat(1, 0.72, 0.52, 0.9, delay=0.8, z=4), chat(2, 0.72, 0.52, 0.9, delay=2.0, z=5)]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('cn-boy-read', x=0.3, y=waist(0.98), s=0.98, z=2),
    chat(0, 0.66, 0.5, 0.92), chat(1, 0.66, 0.5, 0.92, when='text', cue=0, z=4),
    {'sound': 'notify', 'when': 'text', 'cue': 0},
    {'label': '妈妈发来的短信', 'x': 0.86, 'y': 0.2, 'size': 0.07, 'when': '短信', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
pic0.update({'ex': 'I got a text message from my mom.', 'exzh': '我收到了妈妈发来的一条短信。', 'exPic': ex0})
P['pics'] = [pic0]
# ======== 同义词辨析：text message / text
W, H = 537, 356
P['distinguish'] = {'key': '短信', 'items': [
    {'w': 'text message', 'gloss': '短信', 'note': '完整的说法，写下来、正式一点时用', 'ex': 'send a text message',
     'pic': {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
         actor('west-woman-phone', x=0.28, y=waist(0.92), s=0.92, z=2),
         chat(0, 0.72, 0.52, 0.9), chat(1, 0.72, 0.52, 0.9, delay=0.6, z=4),
         {'waves': True, 'x': 0.72, 'y': 0.08, 'dir': -90, 'spread': 120, 'n': 2, 'period': 1.2, 'r0': 0.02, 'r1': 0.1, 'lw': 0.01, 'color': '#F59E0B', 'delay': 0.6, 'z': 5}]}},
    {'w': 'text', 'gloss': '短信', 'note': '口语里的简称，还能当动词，就是发短信', 'ex': 'Text me later.',
     'pic': {'bg': 'blank', 'img': 'art/street-bg.svg', 'items': [
         walker('walk-cn-boy-pack', 0.99, 0.4, 1.1, -0.1, 0.3, z=1),
         actor('west-girl-text', x=0.5, y=waist(0.92), s=0.92, z=2),
         {'svg': 'art/chat3.svg', 'x': 0.84, 'y': 0.5, 's': 0.7, 'delay': 0.5, 'z': 4}]}}],
    'tip': 'text 是 text message 的简称：口语说 text，还能当动词；写下来、正式一点说 text message。'}
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 1.0, 's': 0.3, 'z': 1},
    {'svg': 'art/notebook.svg', 'x': 0.3, 'y': 0.62, 's': 0.3, 'z': 2}, {'svg': 'art/writing.svg', 'x': 0.3, 'y': 0.62, 's': 0.3, 'delay': 0.3, 'fade': 0.8, 'z': 3},
    {'svg': 'art/pencil.svg', 'x': 0.18, 'y': 0.58, 's': 0.05, 'go': [0.4, 0.66], 'dur': 1.6, 'loop': True, 'z': 4},
    {'svg': 'art/msg-bubble.svg', 'x': 0.74, 'y': 0.52, 's': 0.3, 'delay': 0.4, 'anim': 'sway', 'z': 3},
    {'label': '文字 + 消息', 'x': 0.5, 'y': 0.12, 'size': 0.075, 'delay': 0.3, 'z': 6}]}
fig1 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    actor('cn-boy-type', x=0.28, y=waist(0.9), s=0.9, z=2, when='手机'),
    chat(0, 0.74, 0.52, 0.88), chat(3, 0.74, 0.52, 0.88, when='打字', z=4), chat(2, 0.74, 0.52, 0.88, when='发出去', z=5),
    {'sound': 'click', 'when': '打字', 'times': 4, 'every': 0.16},
    {'sound': 'notify', 'when': '发出去'},
    {'label': '短信', 'x': 0.28, 'y': 0.1, 'size': 0.075, 'when': '短信', 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6},
    {'label': '名词', 'x': 0.28, 'y': 0.24, 'size': 0.06, 'when': '名词', 'z': 6},
    {'label': '口语：text', 'x': 0.74, 'y': 0.06, 'size': 0.06, 'when': '口语', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6}]}
P['flow'] = [
    {'node': '“用文字发的消息”', 'fig': fig0},
    {'via': '用手机打字发出去', 'node': '① 短信', 'pos': '名词', 'pic': 0, 'fig': fig1,
     'say': ['二十世纪九十年代，手机能发文字了。', '用手机打字发出去的消息，就是 text message，短信。它说的是一样东西，所以是名词。',
             '口语里常常只说 text，还能当动词，就是发短信。']}]
P['extend'] = ['textbook', 'context', 'messenger']
json.dump({'text message': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

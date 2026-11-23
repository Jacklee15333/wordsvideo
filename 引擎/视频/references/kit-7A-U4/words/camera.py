import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/camera/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
P = {'style': 'core', 'board': True, 'text': {'final': '照相机、摄像机'}}
SHOOT_P = 1 / 1.6 * 3          # 拍照的人一个来回（第三帧闪光）
def photos_from(on, when=None, cue=None, to=(0.16, -0.2)):
    it = {'emit': True, 'svg': 'art/photo.svg', 'on': on, 'x': 420, 'y': 190, 's': 0.16, 'to': list(to), 'life': 1.6,
          'every': SHOOT_P, 'offset': SHOOT_P * 2 / 3, 'spin': 12, 'z': 6}
    if when: it['when'] = when
    if cue is not None: it['cue'] = cue
    return it
# ======== 意思一：照相机（公园里，金发女士举着相机拍照，闪光、照片一张张出来；中国女孩在亭子前比手势）
W, H = 537, 356
pic0 = {'text': '照相机', 'pos': '名词', 'diff': '能拍下照片的机器', 'bg': 'blank', 'img': 'art/park-bg.svg', 'items': [
    actor('cn-girl-pose', id='g', x=0.24, y=waist(0.62, 470), s=0.62, z=0, nodWith='w'),
    walker('walk-cn-girl', 0.86, 0.36, -0.1, 1.1, 0.2, z=-0.5), walker('walk-west-boy-pack', 0.84, 0.34, 1.1, -0.1, 0.6, z=-0.6),
    actor('west-woman-shoot', id='w', x=0.64, y=waist(0.98), s=0.98, z=2),
    photos_from('w', to=(0.2, -0.22)),
    {'label': '咔嚓！', 'x': 0.9, 'y': 0.16, 'size': 0.08, 'delay': 1.2, 'z': 7}]}
# ======== 意思二：摄像机（礼堂里，三脚架上的摄像机正在录，摄像师扶着它；台上嘉宾讲话，台下听众点头）
g = stage_group(W, H, 0.24 * W, H * 0.86, 0.3 * H, who='west-man-present')
pic1 = {'text': '摄像机', 'pos': '名词', 'diff': '能拍下活动画面的机器', 'bg': 'blank', 'img': 'art/stage-bg.svg', 'items': beams((0.22, 0.5)) + g + [
    {'svg': 'art/banner-speech.svg', 'x': 0.36, 'y': 0.1, 's': 0.11, 'z': -1},
    actor('cn-boy-film', id='cm', x=0.88, y=waist(0.78), s=0.78, z=3),
    {'id': 'cam', 'svg': 'art/tripod-cam.svg', 'frames': ['art/tripod-cam.svg', 'art/tripod-cam-off.svg'], 'fps': 1.4, 'seq': 'loop', 'x': 0.66, 'y': 0.62, 's': 0.7, 'z': 4},
    {'waves': True, 'on': 'cam', 'x': 6, 'y': 183, 'dir': 180, 'spread': 40, 'n': 3, 'period': 1.4, 'r0': 0.02, 'r1': 0.16, 'lw': 0.01, 'color': '#2F95E6', 'z': 4},
    audience(0.3, 0.97)]}
# ======== 例句
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': [
    actor('west-girl-wave', id='g', x=0.3, y=waist(0.7, 470), s=0.7, z=0, nodWith='b'),
    walker('walk-cn-teacher-case', 0.84, 0.34, 1.1, -0.1, 0.3, z=-0.5), walker('walk-west-man-case', 0.86, 0.36, -0.1, 1.1, 0.7, z=-0.6),
    actor('cn-boy-shoot', id='b', x=0.66, y=waist(0.98), s=0.98, z=2),
    photos_from('b', when='took a photo', cue=0, to=(0.12, -0.25)),
    {'sound': 'shutter', 'when': 'took a photo', 'cue': 0},
    {'label': '新相机', 'x': 0.84, 'y': 0.2, 'size': 0.075, 'when': 'camera', 'cue': 0, 'z': 7},
    {'label': '照片', 'x': 0.86, 'y': 0.1, 'size': 0.075, 'when': '照片', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7}]}
g2 = stage_group(W, H, 0.62 * W, H * 0.86, 0.32 * H, who='cn-teacher-point')
ex1 = {'bg': 'blank', 'img': 'art/stage-bg.svg', 'items': beams((0.5, 0.75)) + g2 + [
    {'svg': 'art/banner-speech.svg', 'x': 0.62, 'y': 0.1, 's': 0.12, 'z': -1},
    actor('west-man-film', id='cm', x=0.12, y=waist(0.82), s=0.82, z=3),
    {'id': 'cam', 'svg': 'art/tripod-cam.svg', 'frames': ['art/tripod-cam.svg', 'art/tripod-cam-off.svg'], 'fps': 1.4, 'seq': 'loop', 'x': 0.3, 'y': 0.62, 's': 0.72, 'z': 4, 'when': 'camera', 'cue': 0, 'fade': 0.4},
    {'sound': 'applause', 'cue': 0, 'gap': True},
    {'label': '摄像机', 'x': 0.3, 'y': 0.12, 'size': 0.075, 'when': '摄像机', 'cue': 1, 'color': '#1A66B8', 'border': '#2F95E6', 'z': 7},
    audience(0.3, 0.97, x=0.62)]}
pic0.update({'ex': 'I took a photo with my new camera.', 'exzh': '我用新相机拍了一张照片。', 'exPic': ex0})
pic1.update({'ex': 'They used a camera to film the show.', 'exzh': '他们用摄像机拍下了演出。', 'exPic': ex1})
P['pics'] = [pic0, pic1]
# ======== 来历：带拱顶的屋子（老师指着拱顶讲，拱顶描一道金线）
import math
arch = [[(600 - 435 * math.cos(math.pi * i / 16) - 131) / 938, (400 - 334 * math.sin(math.pi * i / 16)) / 700] for i in range(17)]
# 6.41（第八十五版）：来历、演变第 0 / 1 步以前整幅画是静止的（规矩 51），加上会动的人：老师指着拱顶讲、学生听着点头；暗室里有人看着墙上倒着的像吃惊
def vault_people(sx=1.0):
    return [actor('cn-teacher-point', id='t', x=0.2, y=waist(0.62 * sx), s=0.62 * sx, z=4),
            mouth_waves('t', 1, delay=0.4, r1=0.12),
            actor('west-girl-listen', x=0.82, y=waist(0.56 * sx), s=0.56 * sx, z=4, nodWith='t')]
P['originPic'] = {'bg': 'blank', 'img': 'art/vault-room.svg', 'items': vault_people() + [
    {'ray': arch, 'color': '#F2B705', 'lw': 0.018, 'dur': 1.2, 'delay': 0.6, 'z': 3},
    {'label': '拱顶', 'x': 0.5, 'y': 0.2, 'size': 0.09, 'delay': 1.4, 'z': 6},
    {'sound': 'sparkle', 'delay': 1.0}]}
# ======== 意思怎么变过来
W, H = 600, 448
fx = lambda bx: (bx - 131) / 938     # 暗室背景（1200 宽、铺满时两边各裁掉 131）
fy = lambda by: by / 700
fig0 = {'bg': 'blank', 'img': 'art/vault-room.svg', 'items': vault_people(0.92) + [
    {'ray': arch, 'color': '#F2B705', 'lw': 0.016, 'dur': 0.8, 'z': 3},
    {'label': '带拱顶的屋子', 'x': 0.5, 'y': 0.12, 'size': 0.07, 'delay': 0.3, 'z': 6}]}
hole = [fx(425), fy(330)]
fig1 = {'bg': 'blank', 'img': 'art/obscura-room.svg', 'items': [
    {'label': '暗室：不透光', 'x': 0.66, 'y': 0.07, 'size': 0.065, 'when': '不透光', 'z': 6},
    {'label': '小孔', 'x': fx(425), 'y': fy(260), 'size': 0.06, 'when': '小孔', 'z': 6},
    {'ray': [[fx(160), fy(243)], hole, [fx(1000), fy(520)]], 'color': '#FFE066', 'lw': 0.008, 'when': '屋外的景物', 'dur': 1.0, 'z': 3},
    {'ray': [[fx(160), fy(404)], hole, [fx(1000), fy(170)]], 'color': '#FFE066', 'lw': 0.008, 'when': '屋外的景物', 'delay': 0.4, 'dur': 1.0, 'z': 3},
    {'svg': 'art/obscura-img.svg', 'x': fx(1015), 'y': fy(345), 's': 350 / 700, 'when': '倒着', 'fade': 0.6, 'z': 2},
    {'label': '倒着的像', 'x': fx(940), 'y': fy(600), 'size': 0.06, 'when': '倒着', 'delay': 0.5, 'z': 6},
    actor('west-girl-surprised', x=fx(700), y=waist(0.5), s=0.5, z=4, when='倒着', fade=0.4),
    {'label': 'camera obscura', 'x': 0.62, 'y': 0.2, 'size': 0.06, 'when': 'camera obscura', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6},
    {'sound': 'ding', 'when': '倒着'}]}
fig2 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/obscura-room.svg', 'x': 0.25, 'y': 0.3, 's': 0.3, 'when': '越做越小', 'fade': 0.3, 'hideWhen': '盒子', 'z': 2},
    {'ray': [[0.42, 0.3], [0.56, 0.3]], 'arrow': True, 'color': '#C2410C', 'lw': 0.012, 'when': '盒子', 'dur': 0.5, 'hideCue': 1, 'z': 6},
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 0.86, 's': 0.3, 'z': 1},
    {'svg': 'art/boxcam.svg', 'x': 0.5, 'y': 0.58, 's': 0.34, 'when': '盒子', 'fade': 0.4, 'hideCue': 1, 'z': 2},
    {'label': '暗箱', 'x': 0.75, 'y': 0.5, 'size': 0.07, 'when': '暗箱', 'hideCue': 1, 'z': 6},
    actor('cn-boy-shoot', id='b', x=0.5, y=waist(0.95), s=0.95, cue=1, fade=0.4, z=3),
    photos_from('b', cue=1, to=(0.2, -0.22)),
    {'sound': 'shutter', 'cue': 1, 'delay': 1.2},
    {'label': '名词：一样东西', 'x': 0.2, 'y': 0.15, 'size': 0.065, 'cue': 2, 'z': 6},
    {'label': '照相机', 'x': 0.8, 'y': 0.15, 'size': 0.075, 'when': '这就是照相机', 'cue': 1, 'color': '#2B8A3E', 'border': '#2B8A3E', 'z': 6}]}
fig3 = {'bg': 'blank', 'img': 'art/room-bg.svg', 'items': [
    {'svg': 'art/desk.svg', 'x': 0.5, 'y': 0.88, 's': 0.26, 'z': 1, 'hideCue': 2},
    {'id': 'rp', 'svg': 'art/rotary-phone.svg', 'anim': 'thump', 'x': 0.27, 'y': 0.68, 's': 0.24, 'when': '带线的电话', 'fade': 0.4, 'hideCue': 2, 'z': 2},
    {'waves': True, 'on': 'rp', 'x': 150, 'y': 40, 'dir': -90, 'spread': 70, 'n': 3, 'period': 1.0, 'r0': 0.02, 'r1': 0.12, 'lw': 0.01, 'color': '#F59E0B', 'when': '带线的电话', 'hideCue': 2, 'z': 3},
    {'label': 'phone 电话', 'x': 0.27, 'y': 0.4, 'size': 0.065, 'when': '带线的电话', 'hideCue': 2, 'z': 6},
    {'ray': [[0.43, 0.6], [0.55, 0.6]], 'arrow': True, 'color': '#C2410C', 'lw': 0.012, 'when': '手机', 'dur': 0.5, 'hideCue': 2, 'z': 6},
    actor('cn-girl-phone', id='gp', x=0.75, y=waist(0.78), s=0.78, when='手机', fade=0.4, hideCue=2, z=3),
    mouth_waves('gp', 1, when='手机', r1=0.14) | {'hideCue': 2},
    {'label': 'phone 手机', 'x': 0.75, 'y': 0.1, 'size': 0.065, 'when': '手机', 'hideCue': 2, 'z': 6},
    {'svg': 'art/camera.svg', 'x': 0.25, 'y': 0.55, 's': 0.3, 'cue': 2, 'fade': 0.4, 'z': 2},
    {'label': '照相机', 'x': 0.25, 'y': 0.3, 'size': 0.065, 'cue': 2, 'z': 6},
    {'ray': [[0.42, 0.55], [0.56, 0.55]], 'arrow': True, 'color': '#C2410C', 'lw': 0.012, 'when': '活动画面', 'dur': 0.5, 'z': 6},
    {'id': 'cam', 'svg': 'art/tripod-cam.svg', 'frames': ['art/tripod-cam.svg', 'art/tripod-cam-off.svg'], 'fps': 1.4, 'seq': 'loop', 'x': 0.74, 'y': 0.6, 's': 0.62, 'when': '活动画面', 'fade': 0.4, 'z': 2},
    {'label': 'camera 摄像机', 'x': 0.74, 'y': 0.15, 'size': 0.065, 'when': '摄像机', 'color': '#7B57D6', 'border': '#7B57D6', 'z': 6}]}
P['flow'] = [
    {'node': '“带拱顶的屋子”', 'fig': fig0},
    {'via': '不透光的屋子，小孔把屋外的景物映在墙上', 'node': '暗室 camera obscura', 'fig': fig1,
     'say': ['以前，人们做过一种不透光的屋子。', '墙上开一个小孔，屋外的景物就倒着映在对面的墙上。', '这种屋子叫 camera obscura，就是黑屋子，后来就简称 camera。']},
    {'via': '暗室缩成一只盒子，影像能留下来了', 'node': '① 照相机', 'pos': '名词', 'pic': 0, 'fig': fig2,
     'say': ['后来，暗室越做越小，缩成了一只盒子，叫暗箱。', '有了照相技术，盒子里的影像能留下来了，这就是照相机。', '它说的是一样东西，所以是名词。']},
    {'via': '东西换了代：能拍活动画面的机器，还叫 camera', 'node': '② 摄像机', 'pos': '名词', 'pic': 1,
     'rule': '东西换了代，干的还是那件事，旧名字就接着用', 'ruleEx': 'camera 照相机 → 摄像机      phone 电话 → 手机',
     'say': ['英语里，东西换了代，干的还是那件事，旧名字就接着用。', 'phone 本来是带线的电话，后来的手机，也叫 phone。', '照相机也一样：后来能拍活动画面的机器，接着叫 camera，就是摄像机。'], 'fig': fig3}]
P['extend'] = ['chamber', 'cameraman']
P['lexicon'] = {'obscura': 'ɒ b s k j ˈ ʊ ə ɹ ə'}
json.dump({'camera': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

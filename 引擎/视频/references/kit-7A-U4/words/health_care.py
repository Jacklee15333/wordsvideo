import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/health_care/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
# 6.30（第七十四版）：25 health care（图画书风）。画图脚本：alarm,healthcare。
# health 健康：公园里阿姨打太极，有人跑步经过；care 照顾：妈妈端水给生病躺在床上的孩子（咳嗽声）；
# 医疗保健：诊室里外国医生戴听诊器给中国女孩看病，护士拿着疫苗针；讲到“看病、护理、预防”时一样样标出来
P = {'style': 'core', 'board': True, 'distinguish': False}
def lab(t, x, y, size=0.075, **kw):
    d = {'label': t, 'x': x, 'y': y, 'size': size, 'z': 7}
    d.update(kw); return d
BLUE = {'color': '#1A66B8', 'border': '#2F95E6'}
GREEN = {'color': '#2B8A3E', 'border': '#2B8A3E'}
def sickroom(bx=0.64, mx=0.2, s=1.0, **kw):     # 卧室：孩子生病躺在床上（盖着被子），妈妈端着水走过来
    return [actor('cn-boy-sick', id='kid', x=bx, y=0.58, s=0.66 * s, z=1.5),
            {'svg': 'art/bed.svg', 'x': bx, 'y': 0.84, 's': 0.4 * s, 'z': 2},
            actor('cn-teacher-care', x=mx, y=waist(0.82 * s), s=0.82 * s, z=3, nodWith='kid')]
def doctor(x, s, who='west-man-doctor', **kw):
    return actor(who, id='doc', x=x, y=waist(s), s=s, z=3, **kw)
def nurse(x, s, who='west-woman-nurse', **kw):
    return actor(who, x=x, y=waist(s), s=s, z=3, **kw)
def patient(x, s, who='cn-girl-patient', **kw):
    return actor(who, x=x, y=waist(s), s=s, z=2, nodWith='doc', **kw)
# ======== 部分卡片
W, H = 302, 300
P['partPics'] = {
    'p0': {'bg': 'blank', 'img': 'art/park-bg.svg', 'items': [
        walker('walk-west-boy-pack', 0.82, 0.3, -0.1, 1.1, 0.0, z=1),
        actor('cn-teacher-taichi', x=0.46, y=waist(0.84), s=0.84, z=3),
        {'sound': 'bird', 'when': '健康'}, lab('健康 health', 0.5, 0.1, 0.1, when='健康', **BLUE)]},
    'p1': {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': sickroom(0.66, 0.24, 0.92) + [
        {'sound': 'cough', 'when': '照顾'}, lab('照顾 care', 0.5, 0.1, 0.1, when='照顾', **BLUE)]}}
P['icons'] = {'p0': 'art/icon-health.svg', 'p1': 'art/icon-care.svg'}
W, H = 400, 214
P['comboPic'] = {'bg': 'blank', 'img': 'art/clinic-bg.svg', 'items': [nurse(0.32, 0.96), patient(0.72, 0.86, who='cn-girl-shot'),
    {'sound': 'sparkle', 'delay': 0.6}, lab('对健康的照顾', 0.5, 0.12, 0.1, delay=0.6)]}
# ======== 意思
W, H = 537, 356
pic0 = {'text': '医疗保健、卫生保健', 'pos': '名词', 'diff': '看病、护理、预防，照顾健康的服务', 'bg': 'blank', 'img': 'art/clinic-bg.svg', 'items': [
    doctor(0.28, 0.88), patient(0.74, 0.78)]}
W, H = 1120, 432
ex0 = {'bg': 'blank', 'img': 'art/clinic-bg.svg', 'items': [
    doctor(0.2, 0.96, when='Doctors', cue=0, fade=0.3), nurse(0.46, 0.94, when='nurses', cue=0, fade=0.3), patient(0.78, 0.86),
    {'sound': 'heartbeat', 'when': 'health', 'cue': 0},
    lab('医疗保健', 0.5, 0.08, 0.075, when='医疗保健', cue=1, **BLUE)]}
pic0.update({'ex': 'Doctors and nurses give us health care.', 'exzh': '医生和护士为我们提供医疗保健。', 'exPic': ex0})
P['pics'] = [pic0]
# ======== 意思怎么变过来
W, H = 600, 448
fig0 = {'bg': 'blank', 'img': 'art/bedroom-bg.svg', 'items': sickroom(0.64, 0.22, 0.95) + [lab('对健康的照顾', 0.5, 0.1, 0.07, delay=0.3)]}
fig1 = {'bg': 'blank', 'img': 'art/clinic-bg.svg', 'items': [
    doctor(0.22, 0.84, who='west-man-doctor2', when='看病', fade=0.3), patient(0.52, 0.72, who='west-boy-patient'),
    nurse(0.8, 0.82, who='west-woman-nurse2', when='预防', fade=0.3),
    {'sound': 'ding', 'when': '预防'},
    lab('看病', 0.22, 0.08, 0.06, when='看病'), lab('护理', 0.5, 0.08, 0.06, when='护理'), lab('预防', 0.8, 0.08, 0.06, when='预防'),
    lab('医疗保健', 0.5, 0.22, 0.07, when='医疗保健', **GREEN), lab('名词', 0.84, 0.22, 0.06, when='名词')]}
P['flow'] = [
    {'node': '“对健康的照顾”', 'fig': fig0},
    {'via': '看病、治病、护理、预防，一整套服务', 'node': '① 医疗保健、卫生保健', 'pos': '名词', 'pic': 0, 'fig': fig1,
     'say': ['看病、治病、护理、预防，这一整套照顾人健康的服务，就是医疗保健、卫生保健。', '它说的是一种服务，所以是名词。这个说法上个世纪才常用起来。']}]
P['extend'] = ['heal', 'unhealthy', 'caring']
json.dump({'health care': P}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('ok')

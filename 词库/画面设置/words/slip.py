# AI 生成的画面设置（单词工作台）：读同名的 .json，把 {"actor": 动作名} 换成会动的人，交给视频技能
import os, sys, json
os.environ['WART'] = os.path.expanduser('~/wordfilm-work/slip/art')
sys.path.insert(0, os.path.expanduser('~/kit'))
from prefkit import *
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, 'slip.json'), encoding='utf-8'))
def conv(o):
    if isinstance(o, dict):
        if isinstance(o.get('actor'), str):      # 只有值是动作名的才是人；演示词正好叫 actor（值是一幅画）照常往下走
            kw = {k: v for k, v in o.items() if k != 'actor'}
            return actor(o['actor'], **kw)
        return {k: conv(v) for k, v in o.items()}
    if isinstance(o, list):
        return [conv(v) for v in o]
    return o
json.dump({'slip': conv(P)}, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok')

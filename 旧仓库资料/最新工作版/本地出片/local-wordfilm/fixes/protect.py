#!/usr/bin/env python3
"""protect 精简版配音稿的两处修正（第七十七、七十八版出片时验证过）：
1. 辨析里 shield 那句：原句“shield 这个词，……”整句用老师的声音念，识别听不出 shield；改成“shield：……”，shield 用美式女声念。
2. 第 4 题：原句“从 protect、provide、produce 中选一个”三个英文词由老师的声音念，识别听不出 provide；
   加“，这三个词”，三个词按默认规矩用美式女声念。（第七十八版起练习这几幕不出字幕，画面上的题目不变）
可以重复跑：已经改过的不会再改。"""
import json, sys
p = sys.argv[1]
plan = json.load(open(p, encoding='utf-8'))
FIX = {
    ('distinguish', 'shield 这个词，是挡住、保护，隔在你和危险之间的那块挡板。'): 'shield：挡住、保护，就是隔在你和危险之间的那块挡板。',
    ('lianxi3', '第四题，选词填空。从 protect、provide、produce 中选一个，用适当形式填空。'): '第四题，选词填空。从 protect、provide、produce，这三个词中选一个，用适当形式填空。',
}
n = 0
for (sid, old), new in FIX.items():
    segs = plan.get('scenes', {}).get(sid, {}).get('segs', [])
    for i, s in enumerate(segs):
        if s == old:
            segs[i] = new; n += 1
if n:
    json.dump(plan, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'protect：改了 {n} 处配音稿' + ('' if n else '（已经改过，或者起草的说法变了，没有要改的）'))

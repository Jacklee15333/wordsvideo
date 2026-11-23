#!/usr/bin/env python3
"""save_questions.py 原稿.json [总表版本]：原稿是 {单词: [7 道题的原稿（lianxi_data.py 的写法，选择题第一个选项写对的）]}。
每个词：用 lianxi.py 写成总表那两种格（题目1–7、答案）→ 体检（0 个问题才存）→ 存进 词/<首字母>/<单词>.json（已有文件只换题目部分）→ 更新索引。"""
import json, os, sys, time
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lianxi as L
src = json.load(open(sys.argv[1], encoding='utf-8')); ver = sys.argv[2] if len(sys.argv) > 2 else '第七十九版'
idx_p = os.path.join(D, '索引.tsv'); lines = open(idx_p, encoding='utf-8').read().splitlines()
pos = {}
for i, l in enumerate(lines):
    if i: pos.setdefault(l.split('\t')[2], []).append(i)   # 同一个词在总表里可能出现两次，两行都标上
ok = bad = 0
for w, qs in src.items():
    if len(qs) != 7:
        print('✗ %s：要 7 道题，原稿是 %d 道' % (w, len(qs))); bad += 1; continue
    cells, daan = L.fmt_word(w, qs)
    errs = L.check_word(w, cells, daan)
    if errs:
        print('✗ %s：%s' % (w, '；'.join(errs))); bad += 1; continue
    slug = w.replace(' ', '_').replace('/', '_')
    if slug.lower() in {'con', 'prn', 'aux', 'nul'} | {'com%d' % i for i in range(1, 10)} | {'lpt%d' % i for i in range(1, 10)}:
        slug += '_'          # Windows 不许叫 con 这类名字：存成 con_.json
    rel = '词/%s/%s.json' % ((slug[:1].lower() if slug[:1].isalpha() else '_'), slug)
    p = os.path.join(D, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    rec = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'单词': w, '画面': None, '插图': []}
    rec.update({'总表版本': ver, '题目': dict(zip(L.COLS, cells), 答案=daan), '题目原稿': qs,
                '题目生成': time.strftime('%Y-%m-%d') + ' Claude（云端）', '题目检查': '维护技能 lianxi.py 体检 0 个问题'})
    json.dump(rec, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for i in pos.get(w, []):
        c = lines[i].split('\t'); c[4] = '细节数据有'; c[6] = rel; lines[i] = '\t'.join(c)
    ok += 1
open(idx_p, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
left = sum(1 for l in lines[1:] if l.split('\t')[4] == '缺')
print('存好 %d 个词，有问题 %d 个；还缺题目的词 %d 个' % (ok, bad, left))
sys.exit(1 if bad else 0)

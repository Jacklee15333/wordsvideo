#!/usr/bin/env python3
"""compact.py 简写稿.txt 原稿.json：一行一道题的简写稿 → save_questions.py 要的原稿 json（选择题第一个选项写对的）。
简写稿的写法（“|”分隔；选项用“ / ”分隔；题干要两行时中间写“⏎”；考点只写 变形/词性转换/短语/用法/易混，第 6、7 题必写）：
  @单词
  听|问的问题|听力句子|对的选项 / 选项 / 选项 / 选项|讲解
  单|题干|对的 / 选项 / 选项 / 选项|讲解|考点
  形|题干（末尾带 (所给单词)）|答案|讲解|考点
  选|可选的词（a、b、c）|题干|答案|讲解|考点
  改|题干|错的 → 对的|讲解|考点
  完|中文|题干|答案（几个空用“；”隔开）|讲解|考点
"""
import json, sys
T = {'听': '听力', '单': '单项选择', '形': '适当形式填空', '选': '选词填空', '改': '改错', '完': '完成句子'}
ASK = {'单项选择': '选出最恰当的一项。', '适当形式填空': '用所给单词的适当形式填空。', '改错': '句子里有一处错误，找出来并改正。', '完成句子': '根据中文完成句子，每空一词。'}
def opts(s): return [x.strip() for x in s.split(' / ')]
def kd(f, i): return f[i] if len(f) > i and f[i] else ''
out, cur, bad = {}, None, []
for n, raw in enumerate(open(sys.argv[1], encoding='utf-8'), 1):
    l = raw.strip()
    if not l or l.startswith('#'): continue
    if l.startswith('@'):
        cur = l[1:].strip(); out[cur] = []; continue
    f = [x.strip() for x in l.split('|')]
    try:
        t = T[f[0]]
        if t == '听力': q = {'type': t, 'ask': '听录音，回答问题：' + f[1], 'listen': f[2], 'opts': opts(f[3]), 'why': f[4]}
        elif t == '单项选择': q = {'type': t, 'ask': ASK[t], 'stem': f[1].replace('⏎', '\n'), 'opts': opts(f[2]), 'why': f[3], 'kd': kd(f, 4)}
        elif t == '适当形式填空': q = {'type': t, 'ask': ASK[t], 'stem': f[1], 'ans': f[2], 'why': f[3], 'kd': kd(f, 4), 'zh': ''}
        elif t == '选词填空': q = {'type': t, 'ask': '从 %s 中选一个，用适当形式填空。' % f[1], 'stem': f[2], 'ans': f[3], 'why': f[4], 'kd': kd(f, 5), 'zh': ''}
        elif t == '改错': q = {'type': t, 'ask': ASK[t], 'stem': f[1], 'ans': f[2], 'why': f[3], 'kd': kd(f, 4), 'zh': ''}
        else: q = {'type': t, 'ask': ASK[t], 'zh': f[1], 'stem': f[2].replace('⏎', '\n'), 'ans': f[3], 'why': f[4], 'kd': kd(f, 5)}
        if not q.get('kd'): q.pop('kd', None)
        out[cur].append(q)
    except (KeyError, IndexError):
        bad.append('第 %d 行（%s）写法不对：%s' % (n, cur, l[:60]))
json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('转好 %d 个词' % len(out) + ('；写法不对的行：\n' + '\n'.join(bad) if bad else ''))

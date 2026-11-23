#!/usr/bin/env python3
"""next_words.py 总表.xlsx [个数]：按总表顺序，列出下一批还没有 7 道题的词（索引里“题目”是“缺”的），带上出题要用的总表材料"""
import os, sys, openpyxl
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 10
need = []
for l in open(os.path.join(D, '索引.tsv'), encoding='utf-8').read().splitlines()[1:]:
    c = l.split('\t')
    if c[4] == '缺':
        need.append(c[2])
        if len(need) >= n: break
wb = openpyxl.load_workbook(sys.argv[1], read_only=True); ws = wb['拆分结果']
rows = ws.iter_rows(values_only=True); hdr = [str(h) if h else '' for h in next(rows)]; ix = {h: i for i, h in enumerate(hdr)}
want = set(need); got = {}; more = {}
for r in rows:
    w = str(r[ix['单词']] or '').strip()
    if w in want:
        if w not in got: got[w] = r
        else: more.setdefault(w, []).append(r)   # 同一个词在总表里出现两次：两行的意思都要考到
BRIEF = '--brief' in sys.argv
def cell(r, c, k=600): v = r[ix[c]]; return (str(v).strip() if v else '')[:k]
for w in need:
    r = got[w]
    if BRIEF:   # 一个词两行：初中含义｜考点 / 辨析（大批出题时用）
        print('@%s｜%s｜%s' % (w, cell(r, '初中含义', 60).replace('\n', ' '), cell(r, '考点', 320).replace('\n', ' ')))
        for r2 in more.get(w, []):
            print('   【总表里还有一行，两个意思都要考】%s｜%s' % (cell(r2, '初中含义', 60).replace('\n', ' '), cell(r2, '考点', 200).replace('\n', ' ')))
        if cell(r, '辨析'): print('   辨析：' + cell(r, '辨析', 140).replace('\n', ' '))
        continue
    print('=== %s（批次 %s 序号 %s）' % (w, r[ix['批次']], r[ix['序号']]))
    print('初中含义：' + cell(r, '初中含义')); print('含义：' + cell(r, '含义', 200).replace('\n', ' / '))
    print('拆分：' + cell(r, '拆分', 80)); print('考点：' + cell(r, '考点', 900).replace('\n', ' ⏎ '))
    print('辨析：' + cell(r, '辨析', 300).replace('\n', ' ⏎ '))
print('（还缺题目的词一共 %d 个）' % sum(1 for l in open(os.path.join(D, '索引.tsv'), encoding='utf-8').read().splitlines()[1:] if l.split('\t')[4] == '缺'))

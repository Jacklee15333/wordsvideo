import sys, pickle, re, collections
sys.path.insert(0, '/home/claude/skills_new/etymology-table/scripts')
import cols as C
from openpyxl import load_workbook
wb = load_workbook('/home/claude/danci/new.xlsx', read_only=True)
rows = [list(r) for r in wb['拆分结果'].iter_rows(values_only=True)]
assert rows[0][11] == '单词部分' and len(rows[0]) == 22, rows[0]
words = {str(r[4] or '').strip().lower() for r in rows[1:]}
bad = 0; first = []
for i, r in enumerate(rows[1:], start=2):
    cur = tuple(str(x) if x is not None else '-' for x in r[9:13])
    text = C.combine(*r[9:13], split=r[8])
    vals = C.cells(str(r[4] or ''), text, r[8], words, r[10], tuple(r[9:13]), r[7])
    if tuple(vals) != cur:
        bad += 1
        if len(first) < 5: first.append((i, r[4], [(a[:40], b[:40]) for a, b in zip(cur, vals) if a != b]))
print('来回一趟（合回一格再分回四列）对不上的行：', bad, first)
# 新写一行时的规矩：几个例子
tests = [('rematch', 're-：“再、又”\nmatch：比赛（见 match）', 're + match', '① 词根词缀'), ('inspect', 'in-：“向里”\nspect：看（拉丁语 specere“看”）', 'in + spect', '① 词根词缀'),
         ('bookshelf', 'book：书\nshelf：架子', 'book + shelf', '③ 合成词'), ('zzz', 'zzz：模仿打鼾声', '—', '⑤ 基础词')]
for w, t, sp, ty in tests:
    print(w, C.cells(w, t, sp, words, None, None, ty))
leg = C.legacy(rows[4])
print('legacy 列数', len(leg), '| maker 合回一格：', leg[9].replace('\n', ' / ')[:120])

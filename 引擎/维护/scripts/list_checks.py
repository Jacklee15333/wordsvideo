"""列出「拆分结果」M 列核对结果为某一类的行（联网复核用）。
用法：python3 list_checks.py <xlsx> [⏳|❓|⚠️|✏️|✅] [N]（默认 ⏳，列前 40 行）"""
import sys
from openpyxl import load_workbook
F = sys.argv[1]
want = sys.argv[2] if len(sys.argv) > 2 else '⏳'
N = int(sys.argv[3]) if len(sys.argv) > 3 else 40
ws = load_workbook(F, read_only=True)['拆分结果']
hits = []
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import cols
for i, r in enumerate((cols.legacy(x) for x in ws.iter_rows(min_row=2, values_only=True)), start=2):
    if str(r[13] or '').startswith(want):
        hits.append((i, r[2], r[4], r[8], str(r[14] or '')[:60], str(r[15] or '')[:40]))
print(f'{want}：{len(hits)} 行（按组号排，同一组的一起查）')
for i, g, w, sp, m, n in hits[:N]:
    print(f'  第 {i} 行  组 {g}  {w} | 拆分 {sp} | 依据 {m} | 来源 {n}')

"""在「拆分结果」里标注做过“词根变体”处理的行：
- 新增/更新 Q 列“词根变体处理”，写“清单第 N 项 · 本组词根 X”，单元格绿底；
- 把这一行的 H 列（各部分解释）涂浅绿，一眼能看出改过；
- 筛选范围扩到 Q 列。
凡“本次调整”(P 列) 里有“词根说明”的行都会被标注，可反复运行。
用法：python3 mark_rows.py <xlsx>   （就地修改）"""
import re, sys, copy
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
GREEN = PatternFill('solid', start_color='E2EFDA'); LIGHT = PatternFill('solid', start_color='F1F8EC')
def mark(wb):
    ws = wb['拆分结果']; X = wb['词根变体待处理']
    item_of = {}
    for i in range(2, X.max_row + 1):
        item_of.setdefault(X.cell(row=i, column=2).value, X.cell(row=i, column=1).value)
    h = ws.cell(row=1, column=17)
    if h.value != '词根变体处理':
        h.value = '词根变体处理'; h._style = copy.copy(ws.cell(row=1, column=16)._style)
        ws.column_dimensions['Q'].width = 26
    tmpl = ws.cell(row=2, column=16)
    n = 0
    for r in range(2, ws.max_row + 1):
        if '词根说明' not in str(ws.cell(row=r, column=16).value or ''): continue
        H = str(ws.cell(row=r, column=8).value or '')
        m = re.search(r'由词根 ([A-Za-z]+) 变来|本组词根 ?([A-Za-z]+)|^\s*([A-Za-z]+)：本组词根', H, re.M)
        root = next((g for g in (m.groups() if m else []) if g), None)
        g = ws.cell(row=r, column=3).value
        k = item_of.get(g)
        txt = (f'清单第 {k} 项' if k else '已处理') + (f' · 本组词根 {root}' if root else '')
        c = ws.cell(row=r, column=17); c._style = copy.copy(tmpl._style); c.value = txt; c.fill = GREEN
        ws.cell(row=r, column=8).fill = LIGHT
        n += 1
    ws.auto_filter.ref = f'A1:Q{ws.max_row}'
    return n
if __name__ == '__main__':
    wb = load_workbook(sys.argv[1]); n = mark(wb); wb.save(sys.argv[1]); print('marked rows', n)

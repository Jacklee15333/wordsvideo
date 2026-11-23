"""在「拆分结果」里补新行（补母词），并把所有按行号的引用改对。

补母词的做法（2026-11 直接母词轮定下，和更早的“母词补全”一样）：
  - 新行放在派生词正上方；批次、组号、小类号和派生词相同，序号按新顺序在批次内重排；
  - 新行成了本组第一行的，【背景】要从原来的第一行挪到新行（调用方在 values 里给 O 列（第 15 列，cols.BG），并把原行的 O 清空）；
  - 「拆分结果」里所有“第 N 行”、「整表核对记录」的超链接和文字、各表公式里的统计范围（$9279 这种末行号）都按新行号改写；
  - 冻结窗格固定写 G2（A–F：批次到含义）（openpyxl 读出的 freeze_panes 可能是滚动位置，原样写回会冻住几千行）。

用法：
    import sys; sys.path.insert(0, '<技能目录>/scripts')
    from insert_rows import rebuild_with_inserts
    o2n, new_rows = rebuild_with_inserts(wb, [{'above': 186, 'values': {5: 'thoughtless', 9: 'thought + less', ...}}])
    # o2n：旧行号 → 新行号；new_rows[i]：第 i 个新行的行号。调用方再写新行的 U 列（本次调整，第 21 列，cols.ADJ，要用到新行号时）。
"""
import copy
import math
import re
from collections import Counter

ROWREF = re.compile(r'第 (\d+) 行')


def fit_height(ws, r, cols='FGIJKLMNOPRST'):
    """按最长的一格估行高（和 fixlib 一样：每行字约 17.25 磅）"""
    W = {c: ws.column_dimensions[c].width or 10 for c in cols}
    dw = lambda s: sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)
    best = max(sum(max(1, math.ceil(dw(l) / (W[c] - 1.5))) for l in str(ws[f'{c}{r}'].value or '').split('\n')) for c in cols)
    ws.row_dimensions[r].height = round(max(best, 1) * 17.25, 2)


def rebuild_with_inserts(wb, inserts, sheet='拆分结果', ncol=22, batch_col=1, seq_col=2):
    ws = wb[sheet]
    N = ws.max_row
    old_rows = list(range(2, N + 1))
    above = {}
    for k, ins in enumerate(inserts):
        above.setdefault(ins['above'], []).append(k)
    order = []                                   # ('old', r) / ('new', k)
    for r in old_rows:
        for k in above.get(r, []):
            order.append(('new', k))
        order.append(('old', r))
    o2n, new_rows = {}, [None] * len(inserts)
    for n, (kind, x) in enumerate(order, start=2):
        if kind == 'old':
            o2n[x] = n
        else:
            new_rows[x] = n
    remap = lambda s: ROWREF.sub(lambda m: f'第 {o2n.get(int(m.group(1)), int(m.group(1)))} 行', s) if isinstance(s, str) else s
    changed = Counter()

    X = wb.create_sheet('__tmp__')
    for key, d in ws.column_dimensions.items():
        X.column_dimensions[key].width = d.width
        X.column_dimensions[key].hidden = d.hidden
    for c in range(1, ncol + 1):
        X.cell(1, c).value = ws.cell(1, c).value
        X.cell(1, c)._style = copy.copy(ws.cell(1, c)._style)
    X.row_dimensions[1].height = ws.row_dimensions[1].height
    for n, (kind, x) in enumerate(order, start=2):
        if kind == 'old':
            for c in range(1, ncol + 1):
                v = ws.cell(x, c).value
                nv = remap(v)
                if nv != v:
                    changed[c] += 1
                d = X.cell(n, c)
                d.value = nv
                d._style = copy.copy(ws.cell(x, c)._style)
            X.row_dimensions[n].height = ws.row_dimensions[x].height
        else:
            ins = inserts[x]
            src = ins.get('style_from', ins['above'])
            for c in range(1, ncol + 1):
                d = X.cell(n, c)
                d._style = copy.copy(ws.cell(src, c)._style)
                d.value = ins['values'].get(c, ws.cell(ins['above'], c).value if c in (batch_col, 3, 4) else None)
    # 序号：每个批次内按新顺序从 1 连号
    cnt = Counter()
    for n in range(2, len(order) + 2):
        b = X.cell(n, batch_col).value
        cnt[b] += 1
        X.cell(n, seq_col).value = cnt[b]
    last = len(order) + 1
    X.freeze_panes = 'G2'
    X.auto_filter.ref = f'A1:{X.cell(1, ncol).column_letter}{last}'
    try:
        X.sheet_view.zoomScale = ws.sheet_view.zoomScale
    except Exception:
        pass
    pos = wb.sheetnames.index(sheet)
    wb.remove(ws)
    X.title = sheet
    wb._sheets.remove(X)
    wb._sheets.insert(pos, X)
    wb.active = pos
    for r in new_rows:
        fit_height(X, r)
    # 别的工作表：超链接、“第 N 行”、统计范围的末行号
    old_end = f'${N}'
    for name in wb.sheetnames:
        if name == sheet:
            continue
        for row in wb[name].iter_rows():
            for c in row:
                v = c.value
                if not isinstance(v, str):
                    continue
                nv = re.sub(r"('?" + re.escape(sheet) + r"'?!\$?[A-Z]+\$?)(\d+)",
                            lambda m: m.group(1) + str(o2n.get(int(m.group(2)), int(m.group(2)))), v)
                nv = remap(nv)
                nv = re.sub(re.escape(old_end) + r'(?!\d)', f'${last}', nv) if v.startswith('=') else nv
                if nv != v:
                    c.value = nv
                    changed[name] += 1
    return o2n, new_rows, last, changed

"""把词移到它词根所在的组：放在目标组最后一个词的下面，批次、组号、小类号改成目标组的，
来源链接等其余内容不动；原组和目标组所在批次的序号重排；被移走的词如果原是本组第一个、带着【背景】，
【背景】交给原组剩下的第一个词；所有“第 N 行”（本次调整列、各索引表的超链接）按新行号改写。
用法：python3 move_rows.py <源.xlsx> <输出.xlsx> <moves.json>
moves.json：[{"word": "mutual", "to_group": 1551, "root": "mut"}, ...]（row/from_group 可省）"""
import re, sys, json, copy, collections
from openpyxl import load_workbook
SRC, OUT, MV = sys.argv[1], sys.argv[2], sys.argv[3]
moves = json.load(open(MV)); wb = load_workbook(SRC); ws = wb['拆分结果']
N = ws.max_row; NC = ws.max_column
rows = list(range(2, N + 1)); val = lambda r, c: ws.cell(row=r, column=c).value
rowof = {}
for r in rows: rowof.setdefault(str(val(r, 5)), r)
moving = {}
for mv in moves:
    r = mv.get('row') or rowof[mv['word']]
    if val(r, 3) == mv['to_group']: continue
    moving[r] = mv
order = [r for r in rows if r not in moving]
for r, mv in moving.items():                       # 插到目标组最后一行后面
    last = max(i for i, x in enumerate(order) if val(x, 3) == mv['to_group'])
    order.insert(last + 1, r)
o2n = {r: n for n, r in enumerate(order, start=2)}
# 记下要改的值
newvals = {}
first_of = {}
for r in rows: first_of.setdefault(val(r, 3), r)
bg_handoff = {}
for r, mv in moving.items():
    tgt_last = max(x for x in rows if val(x, 3) == mv['to_group'] and x not in moving)
    newvals[r] = {1: val(tgt_last, 1), 3: mv['to_group'], 4: val(tgt_last, 4)}
    g = val(r, 3)
    if first_of[g] == r and val(r, 10):
        nxt = [x for x in rows if val(x, 3) == g and x != r and x not in moving]
        if nxt: bg_handoff[nxt[0]] = val(r, 10)
        newvals[r][10] = None
    note = f"移动：词根 {mv['root']} 在第 {mv['to_group']} 组，从第 {val(r,1)} 批第 {g} 组移到第 {val(tgt_last,1)} 批第 {mv['to_group']} 组"
    pv = val(r, 16); newvals[r][16] = (pv + '；' if pv else '') + note
remap = lambda s: re.sub(r'第 (\d+) 行', lambda m: f'第 {o2n.get(int(m.group(1)), int(m.group(1)))} 行', s) if isinstance(s, str) else s
X = wb.create_sheet('tmp')
for k, d in ws.column_dimensions.items(): X.column_dimensions[k].width = d.width
for c in range(1, NC + 1):
    X.cell(row=1, column=c).value = val(1, c); X.cell(row=1, column=c)._style = copy.copy(ws.cell(row=1, column=c)._style)
X.row_dimensions[1].height = ws.row_dimensions[1].height
for n, r in enumerate(order, start=2):
    for c in range(1, NC + 1):
        v = newvals.get(r, {}).get(c, val(r, c))
        if c == 10 and r in bg_handoff: v = bg_handoff[r]
        if c == 16: v = remap(v)
        d = X.cell(row=n, column=c); d.value = v; d._style = copy.copy(ws.cell(row=r, column=c)._style)
    X.row_dimensions[n].height = ws.row_dimensions[r].height
cnt = collections.Counter()
for n in range(2, N + 1):
    b = X.cell(row=n, column=1).value; cnt[b] += 1; X.cell(row=n, column=2).value = cnt[b]
X.freeze_panes = ws.freeze_panes; X.auto_filter.ref = ws.auto_filter.ref
pos = wb.sheetnames.index('拆分结果'); wb.remove(ws); X.title = '拆分结果'; wb._sheets.remove(X); wb._sheets.insert(pos, X); wb.active = pos
for name in wb.sheetnames:
    if name == '拆分结果': continue
    for row in wb[name].iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, str) and "'拆分结果'!E" in v:
                v = re.sub(r"!E(\d+)", lambda m: f"!E{o2n.get(int(m.group(1)), int(m.group(1)))}", v)
                c.value = remap(v)
wb.save(OUT)
print('moved', len(moving), {mv['word']: (o2n[r], mv['to_group']) for r, mv in moving.items()})

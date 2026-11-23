"""Apply one round of root-variant explanations.
Usage: python3 apply_roots.py <source.xlsx> <output.xlsx> <round_module.py>
The round module defines:
  E      = {word: {label_key: new_line}}   label_key = label lower-cased, hyphens and (...) removed
  STATUS = {item_no: '已处理' | '已处理（备注）' | '核对：…'}
It replaces the matching line in 各部分解释 (column H), appends a note to 本次调整 (column P),
enlarges row height if needed, updates the 状态 column of 词根变体待处理, and saves to <output>.
Prints any word/label it could not find — fix those keys and rerun."""
import re, math, sys, os, importlib.util
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
SRC, OUT, MODPATH = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location('roundmod', MODPATH)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
E, STATUS = m.E, m.STATUS
wb = load_workbook(SRC); ws = wb['拆分结果']
rowof = {}
for i in range(2, ws.max_row + 1): rowof.setdefault(str(ws.cell(row=i, column=5).value), i)
W = {c: ws.column_dimensions[c].width for c in 'ABCDEFGHIJKLMNO'}
def dw(s): return sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)
def fit(r):
    best = 1
    for c in 'GHIJKMNO':
        v = ws[f'{c}{r}'].value
        if v: best = max(best, sum(max(1, math.ceil(dw(l) / (W[c] - 1.5))) for l in str(v).split('\n')))
    need = round(best * 17.25, 2)
    if (ws.row_dimensions[r].height or 0) < need: ws.row_dimensions[r].height = need
def norm(l): return re.sub(r'\([^)]*\)', '', l).strip().strip('-').lower()
done, miss = [], []
for w, d in E.items():
    if w not in rowof: miss.append((w, 'no row')); continue
    r = rowof[w]; H = str(ws.cell(row=r, column=8).value or '').split('\n'); used = set(); out = []
    for l in H:
        mm = re.match(r'^\s*([^：:]{1,40})[：:]', l)
        k = norm(mm.group(1)) if mm else None
        if k in d and k not in used: out.append(d[k]); used.add(k)
        else: out.append(l)
    miss += [(w, k) for k in d if k not in used]
    if used:
        ws.cell(row=r, column=8).value = '\n'.join(out)
        pv = ws.cell(row=r, column=16).value
        if '词根说明' not in str(pv or ''):
            ws.cell(row=r, column=16).value = (pv + '；' if pv else '') + '词根说明：写明由本组词根怎么变来（词形、意思）'
        fit(r); done.append(w)
X = wb['词根变体待处理']
for i in range(2, X.max_row + 1):
    k = X.cell(row=i, column=1).value
    if k in STATUS:
        c = X.cell(row=i, column=7); c.value = STATUS[k]
        c.fill = PatternFill('solid', start_color='E2EFDA' if STATUS[k].startswith('已') else 'FFF2CC')
# any text cell that starts with '=' but is not a formula must be stored as text
for name in wb.sheetnames:
    for row in wb[name].iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, str) and v.startswith('=') and not re.match(r'^=(HYPERLINK|COUNTIF|COUNTA|SUM|IF|ROUND|COUNT)\(|^="', v):
                c.data_type = 's'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mark_rows import mark
print('marked rows', mark(wb))
wb.save(OUT)
print('rows edited', len(done), '| not applied:', miss)

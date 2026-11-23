"""各部分解释（J）拆成 J 前缀、K 词根、L 后缀三列，后面的列往右挪两列；R/T 列记录；「说明」「整表核对记录」改列字母、公式、写法说明。"""
import re, copy, math, sys, collections
from openpyxl import load_workbook
from openpyxl.styles import Alignment, PatternFill
from openpyxl.utils import get_column_letter as L_
sys.path.insert(0, '/home/claude/skills_new/maintain/etymology-table/scripts')
import cols as C

SRC, OUT = '/home/claude/out/new2.xlsx', sys.argv[1]
TAG = '分三列'
wb = load_workbook(SRC)
ws = wb['拆分结果']
N, NC = ws.max_row, ws.max_column
assert NC == 19 and ws.cell(1, 10).value == '各部分解释'
width = {}
for d in ws.column_dimensions.values():
    for c in range(d.min, d.max + 1):
        width[c] = d.width
X = wb.create_sheet('__tmp__')
newc = lambda c: c if c < 10 else c + 2            # 老列号 → 新列号（J 以后的往右挪两列；J 本身拆成 J、K、L）
for c in range(1, NC + 1):
    if c != 10:
        X.column_dimensions[L_(newc(c))].width = width.get(c, 10)
for c, w in ((10, 30), (11, 44), (12, 44)):
    X.column_dimensions[L_(c)].width = w

# 列字母：K–S → M–U；“J 列”（各部分解释）→“J–L 列”
SHIFT = {chr(c): chr(c + 2) for c in range(ord('K'), ord('S') + 1)}
def txtmap(s):
    s = re.sub(r'(?<![A-Za-z$–])([K-S])( ?列)', lambda m: SHIFT[m.group(1)] + m.group(2), s)
    s = re.sub(r'(?<![A-Za-z$–])J( ?列)', r'J–L\1', s)
    return s
fmap = lambda s: re.sub(r"(拆分结果!\$?)([K-S])(\$?\d+:\$?)([K-S])(\$?\d+)", lambda m: m.group(1) + SHIFT[m.group(2)] + m.group(3) + SHIFT[m.group(4)] + m.group(5), s)

stat = collections.Counter()
for r in range(1, N + 1):
    for c in range(1, NC + 1):
        if c == 10: continue
        cc = newc(c)
        X.cell(r, cc).value = ws.cell(r, c).value
        X.cell(r, cc)._style = copy.copy(ws.cell(r, c)._style)
    for k, cc in enumerate((10, 11, 12)):
        X.cell(r, cc)._style = copy.copy(ws.cell(r, 10)._style)
    if r == 1:
        for cc, h in zip((10, 11, 12), ('前缀', '词根', '后缀')): X.cell(1, cc).value = h
        continue
    w = str(ws.cell(r, 5).value or '')
    H = ws.cell(r, 10).value
    pre, root, suf = C.cells(w, H)
    for cc, v in zip((10, 11, 12), (pre, root, suf)):
        X.cell(r, cc).value = v
        al = X.cell(r, cc).alignment
        X.cell(r, cc).alignment = Alignment(horizontal=al.horizontal, vertical=al.vertical or 'center', wrap_text=True)
    assert C.combine(pre, root, suf).split('\n').__len__() == len([l for l in str(H or '').split('\n') if l.strip()]) or not str(H or '').strip()
    stat['pre'] += pre != '-'; stat['root'] += root != '-'; stat['suf'] += suf != '-'
    q = X.cell(r, 20)
    qv = txtmap(str(q.value)) if q.value else ''
    q.value = (qv + '；' if qv else '') + f'{TAG}：各部分解释拆成前缀、词根、后缀三列（J、K、L）'
X.freeze_panes = 'G2'
X.auto_filter.ref = f'A1:U{N}'
pos = wb.sheetnames.index('拆分结果')
wb.remove(ws); X.title = '拆分结果'; wb._sheets.remove(X); wb._sheets.insert(pos, X); wb.active = pos
ws = X
W = {c: ws.column_dimensions[c].width or 10 for c in C.TEXT_COLS}
dw = lambda s: sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)
for r in range(2, N + 1):
    best = max(sum(max(1, math.ceil(dw(l) / (W[c] - 1.5))) for l in str(ws[f'{c}{r}'].value or '').split('\n')) for c in C.TEXT_COLS)
    ws.row_dimensions[r].height = round(max(best, 1) * 17.25, 2)

S = wb['说明']; Rk = wb['整表核对记录']
for sh in (S, Rk):
    for row in sh.iter_rows():
        for c in row:
            if isinstance(c.value, str):
                v = fmap(c.value) if c.value.startswith('=') else txtmap(c.value)
                if v != c.value: c.value = v; stat['other_cells'] += 1
names = {20: 'J 前缀、K 词根、L 后缀', 21: 'M 组合 → 现在的含义', 22: 'N 新·背景', 23: 'O 音变 / 字母变化', 24: 'P 核对结果',
         25: 'Q 核对依据、R 来源链接', 26: 'S 原表备注', 27: 'T 本次调整', 28: 'U 词根变体处理'}
for rr, a in names.items():
    S.cell(rr, 1).value = a
S['B5'] = str(S['B5'].value).replace('拆分、各部分解释、组合', '拆分、前缀、词根、后缀、组合')
S['B20'] = ('以前的“各部分解释”拆成三列，一列讲一种部分，每部分一行“标签：解释”：J 前缀（re-、un-、bio-）；K 词根（词根、母词、合成词里的各个词：people、shoe、maker）；'
            'L 后缀（-ion、-er、-logy，中间的成分 -it-、-at- 也写在这里）。没有的写“-”。“为什么用 -er 不用 -or”这类写在它讲的那一列；讲整个词来历、拼写的说明写在词根列。'
            '这三列只讲各部分，怎么组合、意思怎么来的写在 M 列')
S['B21'] = str(S['B21'].value).replace('各部分解释写“见 thoughtless”', '词根列写“见 thoughtless”')
S['A31'] = '前缀、词根、后缀'
S['B31'] = ('三列各讲一种部分：每部分一行“标签：解释”，标签和拆分对得上：前缀写 re-（J 列），后缀写 -ion（L 列），词根写本来的样子（K 列）；标签可以带括号（al(l)、long（动词））。'
            '只讲这一部分本身，不写“在这里：……所以 W 指……”“意思怎么变”“用词规律”（写在组合列）。“为什么用 -er 不用 -or”跟着它讲的前缀或后缀；讲整个词来历的说明放词根列；一列没有内容写“-”。')
S.row_dimensions[20].height = 75; S.row_dimensions[31].height = 75
for c in 'ABCD':
    S[f'{c}103']._style = copy.copy(S[f'{c}102']._style)
S['A103'] = '各部分解释分三列'
S['B103'] = ('“各部分解释”一列拆成 J 前缀、K 词根、L 后缀三列，每列只讲一种部分，没有的写“-”；“为什么…”跟着它讲的前缀或后缀，讲整个词来历的说明放词根列。'
             '后面的列往右挪两列（组合 M、背景 N、音变 O、核对结果 P、本次调整 T）。逐行见 T 列“分三列：…”。')
S.merge_cells('B103:C103')
S['D103'] = '=COUNTIF(拆分结果!$T$2:$T$9294,"*分三列*")'
S.row_dimensions[103].height = 60
n0 = sum(1 for x in Rk.iter_rows(min_row=2, values_only=True) if x[0] is not None)
body = copy.copy(Rk.cell(2, 4)._style)
LOG = [('已修正', None, '各部分解释', '前缀、词根、后缀的解释都写在一格里，一格好几行，看着乱，软件、技能提取也难',
        f'拆成 J 前缀、K 词根、L 后缀三列，每部分一行“标签：解释”，没有的写“-”：有前缀的 {stat["pre"]} 行、有词根的 {stat["root"]} 行、有后缀的 {stat["suf"]} 行。'
        '“为什么用 -ar 不用 -al”跟着它讲的那个前缀、后缀；讲整个词来历、拼写的说明放词根列（20 条提到词缀但讲的是整个词的，也放词根列）。'
        '后面的列往右挪两列：组合 M、背景 N、音变 O、核对结果 P、本次调整 T。逐行见 T 列“分三列：…”'),
       ('特殊（未改）', None, '只有前缀、后缀的词', '28 个由希腊、拉丁构词成分组成的词（biology、geography、psychology、photograph、astronaut……），原表把两部分标成 bio-、-logy',
        '照原表的标签放：bio- 在前缀列，-logy 在后缀列，词根列写“-”；要按词根算的话再改标签')]
for k, (cat, rr, w, what, how) in enumerate(LOG):
    i = n0 + k + 2
    for c, v in enumerate([n0 + k + 1, cat, '—', w, what, how], 1):
        cell = Rk.cell(i, c); cell.value = v; cell._style = copy.copy(body)
        cell.alignment = Alignment(wrap_text=True, vertical='top')
    Rk.cell(i, 2).fill = PatternFill('solid', start_color='E2EFDA' if cat == '已修正' else 'FFF2CC')
    Rk.row_dimensions[i].height = 17.25 * max(1, math.ceil(max(len(what), len(how)) / 38))
Rk.auto_filter.ref = f'A1:F{Rk.max_row}'
wb.save(OUT)
print(dict(stat))

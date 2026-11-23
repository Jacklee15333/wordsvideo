"""含义、例句分列：在 F「含义」后面插一列 G「例句」；含义改成同词性一行；后面的列往右挪一列。
其他表里的列字母、公式范围跟着挪；R 列（本次调整）逐行记录；「整表核对记录」「说明」更新。"""
import re, copy, math, pickle, collections, sys
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter as L_
sys.path.insert(0, '/home/claude/work2'); sys.path.insert(0, '/home/claude/skills_new/maintain/etymology-table/scripts')
import build3, overrides2 as O2
import meaning as M

SRC = '/home/claude/out/new.xlsx'
OUT = sys.argv[1]
TAG = '例句分列'
fg = pickle.load(open('/home/claude/work2/fg.pkl', 'rb'))
wb = load_workbook(SRC)
ws = wb['拆分结果']
N, NC = ws.max_row, ws.max_column
assert NC == 18 and N == 9294

# 列宽（openpyxl 把相邻同宽的列合在一个 dimension 里）
width = {}
for d in ws.column_dimensions.values():
    for c in range(d.min, d.max + 1):
        width[c] = d.width
X = wb.create_sheet('__tmp__')
for c in range(1, NC + 1):
    X.column_dimensions[L_(c if c < 7 else c + 1)].width = width.get(c, 10)
X.column_dimensions['F'].width = 36
X.column_dimensions['G'].width = 44

edited_rows = {rn for (rn, i) in O2.EDIT}
stat = collections.Counter()
SHIFT = {chr(c): chr(c + 1) for c in range(ord('G'), ord('R') + 1)}
txtmap = lambda s: re.sub(r'(?<![A-Za-z$])([G-R])( ?列)', lambda m: SHIFT[m.group(1)] + m.group(2), s)
for r in range(1, N + 1):
    for c in range(1, NC + 1):
        cc = c if c < 7 else c + 1
        v = ws.cell(r, c).value
        X.cell(r, cc).value = v
        X.cell(r, cc)._style = copy.copy(ws.cell(r, c)._style)
    g = X.cell(r, 7)
    g._style = copy.copy(ws.cell(r, 6)._style)
    if r == 1:
        g.value = '例句'
        continue
    oldF = str(ws.cell(r, 6).value or '')
    F, G = fg[r]
    X.cell(r, 6).value = F
    g.value = G or None
    for c in (6, 7):
        al = X.cell(r, c).alignment
        X.cell(r, c).alignment = Alignment(horizontal=al.horizontal, vertical=al.vertical or 'center', wrap_text=True)
    notes = []
    if G: notes.append('例子挪到 G 列「例句」'); stat['rows_G'] += 1
    if F.count('\n') < oldF.count('\n'): notes.append('同一词性的意思并成一行'); stat['rows_grouped'] += 1
    if r in edited_rows: notes.append('意思改写（原来意思里写的是例句或说明）或词性改正'); stat['rows_edit'] += 1
    q = X.cell(r, 18)
    qv = txtmap(str(q.value)) if q.value else ''
    if notes:
        qv = (qv + '；' if qv else '') + f'{TAG}：' + '，'.join(notes)
        stat['rows_noted'] += 1
    q.value = qv or None
X.freeze_panes = 'G2'
X.auto_filter.ref = f'A1:S{N}'
pos = wb.sheetnames.index('拆分结果')
wb.remove(ws); X.title = '拆分结果'; wb._sheets.remove(X); wb._sheets.insert(pos, X); wb.active = pos
ws = X
# 行高：按有文字的列重新估（含义并行以后变矮、例句列有长的）
cols = 'FGIJKLMOPQ'
W = {c: ws.column_dimensions[c].width or 10 for c in cols}
dw = lambda s: sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)
for r in range(2, N + 1):
    best = max(sum(max(1, math.ceil(dw(l) / (W[c] - 1.5))) for l in str(ws[f'{c}{r}'].value or '').split('\n')) for c in cols)
    ws.row_dimensions[r].height = round(max(best, 1) * 17.25, 2)

# 别的表：列字母、公式范围往后挪一列（G 起）
fmap = lambda s: re.sub(r"(拆分结果!\$?)([G-R])(\$?\d+:\$?)([G-R])(\$?\d+)", lambda m: m.group(1) + SHIFT[m.group(2)] + m.group(3) + SHIFT[m.group(4)] + m.group(5), s)
S = wb['说明']; Rk = wb['整表核对记录']
for sh in (S, Rk):
    for row in sh.iter_rows():
        for c in row:
            if isinstance(c.value, str):
                v = fmap(c.value) if c.value.startswith('=') else txtmap(c.value)
                if v != c.value: c.value = v; stat['other_sheet_cells'] += 1
# 说明 第二节：F 含义、G 例句合在一行，后面的列字母往后挪
names = {17: 'F 含义、G 例句', 18: 'H 类型', 19: 'I 拆分', 20: 'J 各部分解释', 21: 'K 组合 → 现在的含义', 22: 'L 新·背景',
         23: 'M 音变 / 字母变化', 24: 'N 核对结果', 25: 'O 核对依据、P 来源链接', 26: 'Q 原表备注', 27: 'R 本次调整', 28: 'S 词根变体处理'}
for rr, a in names.items():
    old = str(S.cell(rr, 1).value)
    assert old.split(' ', 1)[1].split('、')[0].replace('O 来源链接', '') in a or rr == 17, (rr, old, a)
    S.cell(rr, 1).value = a
S['B17'] = ('F 含义：现在的意思。同一个词性的意思写一行，行首是词性（n. 名词、v. 动词、adj. 形容词、adv. 副词、prep. 介词、conj. 连词、pron. 代词、num. 数词、'
            'int. 感叹词、modal v. 情态动词、aux. v. 助动词、phr. 短语），几个意思用“；”隔开（adj. 受欢迎的；流行的、大众的；通俗的）；（英）（口）（喻）这类标签写在意思前面，同形词的 ①② 写在词性后面。'
            'G 例句：例句、例词，每个有例子的意思一行“意思：例子”（受欢迎的：a popular teacher）。（2026-11 从组合列的【今义】挪过来，同月加词性、例句分列）')
S['B36'] = ('含义（F）：同词性一行、行首写词性加一个空格，意思之间用“；”，不写例子，括号里只留说明（尤指…、复数 X、英式拼写，同 X）；固定搭配、习语写 phr.（phr. carry out 执行）；'
            '同形词从“② …”那一行起是第二个词。例句（G）：每行“意思：例子”，“意思”就是含义里那个意思去掉括号的样子，几个例子用“；”；同一个意思兼两种词性、写了两次的，前面加词性（v. 出口：…）。'
            '派生词、合成词（dazzling、ponytail）不写在含义里，写在 M 列【派生】【合成】。')
S.row_dimensions[36].height = 90
S.row_dimensions[17].height = 90
S['B27'] = str(S['B27'].value) + '“例句分列：…”'
for c in 'ABCD':
    S[f'{c}102']._style = copy.copy(S[f'{c}101']._style)
S['A102'] = '含义、例句分列'
S['B102'] = ('单词后面新增 G 列“例句”：含义里每个意思后面括号里的例句、例词挪过去（每行“意思：例子”）；含义改成同一词性写一行、意思之间用“；”。'
             '意思本身写成例句的（Could you help me?、Done!）改写成中文意思。后面的列往右挪一列（本次调整现在是 R 列）。逐行见 R 列“例句分列：…”。')
S.merge_cells('B102:C102')
S['D102'] = '=COUNTIF(拆分结果!$R$2:$R$9294,"*例句分列*")'
S.row_dimensions[102].height = 75

# 整表核对记录
n0 = sum(1 for x in Rk.iter_rows(min_row=2, values_only=True) if x[0] is not None)
body = copy.copy(Rk.cell(2, 4)._style)
nsense = sum(len(M.senses(F, G)) for F, G in fg.values())
nex = sum(len(s['ex']) for F, G in fg.values() for s in M.senses(F, G))
pc = collections.Counter(s['pos'] for F, G in fg.values() for s in M.senses(F, G))
LOG = [
 ('已修正', None, '含义列', '每个意思后面都跟着例句、例词，含义列不清爽；一个意思一行，行数太多',
  f'新增 G 列“例句”：{stat["rows_G"]} 行的例句、例词挪过去，每行“意思：例子”；含义改成同一词性写一行、意思之间用“；”（{nsense} 个意思写成 {sum(F.count(chr(10)) + 1 for F, G in fg.values())} 行），括号里只留说明。后面的列往右挪一列（类型 H、拆分 I、各部分解释 J、组合 K、背景 L、音变 M、核对结果 N、本次调整 R）。逐行见 R 列“例句分列：…”'),
 ('已修正', None, '含义列', '有的意思本身写成了例句或说明（could“（委婉请求）Could you help me?”、done“Done! 成交！”、seen“I have seen it.”、rush-hour“作定语：rush-hour traffic”）',
  '改写成中文意思（能…吗、成交、see 的过去分词、高峰期的），例句挪到例句列；另改正拆行后没跟上的词性 15 处（import 的“进口商品”“意义、重要性”、hope 的“希望所寄托的人或事”、ditch 的“沟、渠”是名词）'),
]
for k, (cat, rr, w, what, how) in enumerate(LOG):
    i = n0 + k + 2
    vals = [n0 + k + 1, cat, '—', w, what, how]
    for c, v in enumerate(vals, 1):
        cell = Rk.cell(i, c); cell.value = v; cell._style = copy.copy(body)
        cell.alignment = Alignment(wrap_text=True, vertical='top')
    Rk.cell(i, 2).fill = PatternFill('solid', start_color='E2EFDA')
    Rk.row_dimensions[i].height = 17.25 * max(1, math.ceil(max(len(what), len(how)) / 38))
Rk.auto_filter.ref = f'A1:F{Rk.max_row}'
wb.save(OUT)
print(dict(stat), 'senses', nsense, 'examples', nex, pc.most_common())

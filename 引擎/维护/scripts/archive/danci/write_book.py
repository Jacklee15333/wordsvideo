"""单词列轮写回总表：K 词根后面插 L 列「单词部分」，后面的列往右挪一列；U 列记录；「说明」「整表核对记录」改列字母、公式、写法说明"""
import re, copy, math, sys, pickle
from openpyxl import load_workbook
from openpyxl.styles import Alignment, PatternFill
from openpyxl.utils import get_column_letter as L_
from openpyxl.worksheet.hyperlink import Hyperlink
SRC, OUT = '/home/claude/src.xlsx', '/home/claude/danci/new.xlsx'
out, st = pickle.load(open('/home/claude/danci/new_cells.pkl', 'rb'))
wb = load_workbook(SRC)
ws = wb['拆分结果']
N, NC = ws.max_row, ws.max_column
assert NC == 21 and ws.cell(1, 11).value == '词根' and ws.cell(1, 12).value == '后缀'
print('拆分结果里的超链接：', len(ws._hyperlinks))
width = {}
for dd in ws.column_dimensions.values():
    for c in range(dd.min, dd.max + 1):
        width[c] = dd.width
newc = lambda c: c if c <= 11 else c + 1
X = wb.create_sheet('__tmp__')
for c in range(1, NC + 1):
    X.column_dimensions[L_(newc(c))].width = width.get(c, 10)
X.column_dimensions['L'].width = 44
for r in range(1, N + 1):
    for c in range(1, NC + 1):
        s, d = ws.cell(r, c), X.cell(r, newc(c))
        d.value = s.value
        d._style = copy.copy(s._style)
        if s.hyperlink is not None:
            h = s.hyperlink
            d.hyperlink = Hyperlink(ref=d.coordinate, target=h.target, location=h.location, tooltip=h.tooltip, display=h.display)
    X.cell(r, 12)._style = copy.copy(ws.cell(r, 11)._style)
    X.row_dimensions[r].height = ws.row_dimensions[r].height
    if r == 1:
        X.cell(1, 12).value = '单词部分'
        continue
    J, K, Lw, note = out[r]
    X.cell(r, 10).value, X.cell(r, 11).value, X.cell(r, 12).value = J, K, Lw
    if note:
        q = X.cell(r, 21)
        q.value = (str(q.value) + '；' if q.value else '') + note
X.freeze_panes = 'G2'
X.auto_filter.ref = f'A1:V{N}'
try: X.sheet_view.zoomScale = ws.sheet_view.zoomScale
except Exception: pass
pos = wb.sheetnames.index('拆分结果')
wb.remove(ws); X.title = '拆分结果'; wb._sheets.remove(X); wb._sheets.insert(pos, X); wb.active = pos

# ---------- 「说明」「整表核对记录」：L–U 列往后挪一个字母
SHIFT = {chr(c): chr(c + 1) for c in range(ord('L'), ord('U') + 1)}
def txtmap(s):
    s = s.replace('J–L 列', 'J–M 列').replace('J–L列', 'J–M列')
    return re.sub(r'(?<![A-Za-z$–\-])([L-U])( ?列)', lambda m: SHIFT[m.group(1)] + m.group(2), s)
fmap = lambda s: re.sub(r"(拆分结果!\$?)([L-U])(\$?\d+:\$?)([L-U])(\$?\d+)", lambda m: m.group(1) + SHIFT[m.group(2)] + m.group(3) + SHIFT[m.group(4)] + m.group(5), s)
S, Rk = wb['说明'], wb['整表核对记录']
changed = 0
for sh in (S, Rk):
    for row in sh.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.coordinate not in sh.merged_cells:
                v = fmap(c.value) if c.value.startswith('=') else txtmap(c.value)
                if v != c.value: c.value = v; changed += 1
print('「说明」「整表核对记录」改了列字母的格：', changed)
ren = {'J 前缀、K 词根、L 后缀': 'J 前缀、K 词根、L 单词部分、M 后缀', 'M 组合 → 现在的含义': 'N 组合 → 现在的含义', 'N 新·背景': 'O 新·背景',
       'O 音变 / 字母变化': 'P 音变 / 字母变化', 'P 核对结果': 'Q 核对结果', 'Q 核对依据、R 来源链接': 'R 核对依据、S 来源链接', 'S 原表备注': 'T 原表备注',
       'T 本次调整': 'U 本次调整', 'U 词根变体处理': 'V 词根变体处理', '前缀、词根、后缀': '前缀、词根、单词部分、后缀'}
rowof = {}
for r in range(1, S.max_row + 1):
    a = S.cell(r, 1).value
    if a in ren:
        rowof.setdefault(ren[a], r); S.cell(r, 1).value = ren[a]
    elif isinstance(a, str):
        rowof.setdefault(a, r)
assert 'J 前缀、K 词根、L 单词部分、M 后缀' in rowof and '前缀、词根、单词部分、后缀' in rowof, rowof.keys()
S['B5'] = str(S['B5'].value).replace('拆分、前缀、词根、后缀、组合', '拆分、前缀、词根、单词部分、后缀、组合')
r20 = rowof['J 前缀、K 词根、L 单词部分、M 后缀']
S.cell(r20, 2).value = ('以前的“各部分解释”分成四列，一列讲一种部分，每部分一行“标签：解释”：J 前缀（re-、un-）；K 词根：不能单独用的词根，在接别的部分的那一边加“-”'
    '（开头的 bio-、中间的 -ped-、末尾的 -logue），连接成分（-i-、双写的字母）也写在这里；L 单词部分：能单独用的英语单词，照原样写、不加连字符——基础词本身（make）、'
    '母词（maker、rematch、matching 里的 make、match）、合成词里的各个词（make-up 的 make、up）、专有名词（Hamburg）；M 后缀（-ion、-er、-logy，中间的成分 -it-、-at- 也写在这里）。'
    '没有的写“-”。“为什么用 -er 不用 -or”写在它讲的那一列；讲整个词来历、拼写的说明跟着主体走：有词根的写在词根列，没有词根的写在单词部分。这四列只讲各部分，怎么组合、意思怎么来的写在 N 列')
S.row_dimensions[r20].height = 105
r31 = rowof['前缀、词根、单词部分、后缀']
S.cell(r31, 2).value = ('四列各讲一种部分：每部分一行“标签：解释”，标签和拆分对得上。前缀写 re-（J 列），后缀写 -ion（M 列）；不能单独用的词根（拉丁语、希腊语的词根，bio、geo、photo 这类构词成分，'
    '外语里的成分，连接元音、双写的字母）写在 K 列「词根」，在接别的部分的那一边加“-”（bio-、-ped-、-logue、-i-）；能单独用的英语单词（基础词本身、母词、合成词里的词、专有名词，'
    '也包括 hands、days、behaved 这样的复数、过去式形式）写在 L 列「单词部分」，不加连字符。只讲这一部分本身，不写“在这里”“意思怎么变”“用词规律”（写在组合列）。'
    '“为什么用 -er 不用 -or”跟着它讲的前缀或后缀；讲整个词来历的说明：有词根的放词根列，没有词根的放单词部分；一列没有内容写“-”。')
S.row_dimensions[r31].height = 105
for a, add in (('③ 合成词', '（各个词写在 L 列「单词部分」）'), ('⑤ 基础词', '（解释写在 L 列「单词部分」）')):
    if a in rowof and add not in str(S.cell(rowof[a], 2).value) and not str(S.cell(rowof[a], 2).value).startswith('='):
        S.cell(rowof[a], 2).value = str(S.cell(rowof[a], 2).value) + add
for r in range(1, S.max_row + 1):
    for c in range(1, 5):
        v = S.cell(r, c).value
        if isinstance(v, str) and v.startswith('涉及的行'):
            S.cell(r, c).value = '涉及的行（按 U / V 列数）'
last = max(r for r in range(1, S.max_row + 1) if S.cell(r, 1).value)
new = last + 1
for c in 'ABCD':
    S[f'{c}{new}']._style = copy.copy(S[f'{c}{last}']._style)
S[f'A{new}'] = '单词列'
S[f'B{new}'] = (f'词根列（K）后面新增 L 列「单词部分」：基础词本身（make）、母词（maker、rematch、matching 里的 make、match）、合成词里的各个词（make-up 的 make、up）这些能单独用的英语单词，'
    f'从词根列挪过来（{st["rows_word"]} 行），词根列只留不能单独用的词根和连接成分（{st["rows_root"]} 行，两样都有的 {st["rows_both"]} 行）；没有词根的词，讲来历的说明也一起挪。'
    f'顺带改正上一轮加连字符的错判：{st["W_from_bound"]} 处其实是英语单词（hands-on 的 hands、schooldays 的 days），去掉连字符；{st["R_from_free"]} 处其实是外语成分、拉丁词根'
    f'（tsunami 的 tsu、union 的 un、nation 的 nat），改算词根、加连字符；{st["P"]} 处前缀挪到前缀列（monopoly 的 mono-）。后面的列往右挪一列（组合 N、背景 O、核对结果 Q、本次调整 U、词根变体处理 V）。逐行见 U 列“单词列：…”。')
S.merge_cells(f'B{new}:C{new}')
S[f'D{new}'] = '=COUNTIF(拆分结果!$U$2:$U$9294,"*单词列*")'
S.row_dimensions[new].height = 105
n0 = sum(1 for x in Rk.iter_rows(min_row=2, values_only=True) if x[0] is not None)
body = copy.copy(Rk.cell(2, 4)._style)
LOG = [('已修正', '单词部分列', '词根列里混着两种东西：不能单独用的词根（-spect、bio-），和本身就是单词的基础词、母词、合成词里的词（make、match、up），分不清（用户提出）',
        f'词根列后面新增 L 列「单词部分」：能单独用的英语单词都挪过去（{st["rows_word"]} 行有内容），词根列只留词根和连接成分（-i-、-s-、双写的字母，{st["rows_root"]} 行有内容），'
        f'两样都有的 {st["rows_both"]} 行（yesterday = yester- + day、agriculture = agri- + culture）。讲整个词来历的说明跟着主体走：没有词根的放单词部分。'
        '后面的列往右挪一列：组合 N、背景 O、音变 P、核对结果 Q、依据 R、链接 S、原表备注 T、本次调整 U、词根变体处理 V。逐行见 U 列“单词列：…”'),
       ('已修正', '词根连字符', '上一轮自动加连字符有两种错判：英语单词的复数、过去式这些形式不在表里，被当成了词根；合成词的各部分一律算单词，“见 X”又只比开头几个字母（“见 via”把 vi 算成了单词）',
        f'{st["W_from_bound"]} 处去掉连字符、挪到单词部分（hands-on 的 hands、schooldays 的 days、grassroots 的 roots、craftsman 的 crafts、well-behaved 的 behaved、redid 的 did、boxing 的 box）；'
        f'{st["R_from_free"]} 处改算词根、加连字符（tsunami 的 tsu-、karate 的 -te、deluxe 的 de-、dinosaur 的 dino-、Tuesday 的 Tues-、previous 的 -vi-、union 的 un-、nation 的 nat-、'
        'mission 的 -miss-、synthesis 的 -the-）；monopoly、monarch 的 mono-，enthusiast 的 en-，illusion 的 il-，mistrust 讲 mis- 的说明挪到前缀列'),
       ('特殊（未改）', '单词部分', '有的部分来自拉丁语、法语，但说明里写了“见 自己”，指向同形的英语单词（depart 的 part、design 的 sign、artifact 的 art）；有的是英语单词的缩写形式'
        '（also 的 al = all、bonfire 的 bon = bone、lady 的 la = loaf）',
        '照上一轮的判断算单词，放单词部分；连接成分（spokesman 的 -s-、handicraft 的 -i-、dubbing 的 -b-）照旧写在词根列')]
for k, (cat, w, what, how) in enumerate(LOG):
    i = n0 + k + 2
    for c, v in enumerate([n0 + k + 1, cat, '—', w, what, how], 1):
        cell = Rk.cell(i, c); cell.value = v; cell._style = copy.copy(body)
        cell.alignment = Alignment(wrap_text=True, vertical='top')
    Rk.cell(i, 2).fill = PatternFill('solid', start_color='E2EFDA' if cat == '已修正' else 'FFF2CC')
    Rk.row_dimensions[i].height = 17.25 * max(1, math.ceil(max(len(what), len(how)) / 38))
Rk.auto_filter.ref = f'A1:F{Rk.max_row}'
wb.save(OUT)
print('写好了', OUT, '说明新行', new, '核对记录', n0 + 1, '–', n0 + len(LOG), st)

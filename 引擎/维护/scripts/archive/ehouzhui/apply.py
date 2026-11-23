import sys, copy, json, math
sys.path.insert(0, '/home/claude/work'); sys.path.insert(0, '/home/claude/work/new_maint/etymology-table/scripts')
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import cols as C, columns as COL
from ee import process
SRC, OUT = sys.argv[1], sys.argv[2]
wb = load_workbook(SRC); ws = wb['拆分结果']
W = {}
for dd in ws.column_dimensions.values():
    for i in range(dd.min or 0, (dd.max or 0) + 1):
        if i: W[get_column_letter(i)] = dd.width
W = {c: W.get(c) or 10 for c in C.TEXT_COLS}
dw = lambda s: sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)
def fit(r):
    best = max(sum(max(1, math.ceil(dw(l) / (W[c] - 1.5))) for l in str(ws[f'{c}{r}'].value or '').split('\n')) for c in C.TEXT_COLS)
    need = min(round(best * 17.25, 2), 409)
    if (ws.row_dimensions[r].height or 0) < need: ws.row_dimensions[r].height = need
nS = nO = 0; log = []
for r in range(2, ws.max_row + 1):
    w = str(ws.cell(r, C.WORD).value or '')
    d = {'w': w, 'I': str(ws.cell(r, C.SPLIT).value or ''), 'M': str(ws.cell(r, C.SUF).value or ''), 'N': str(ws.cell(r, C.COMBO).value or '')}
    I2, M2, N2 = process(d)
    if w == 'gave':
        N2 = N2.replace('过去分词加 -n', '过去分词加 -en（give 的 e 和 -en 的 e 只写一个）')
    if (I2, M2, N2) == (d['I'], d['M'], d['N']):
        continue
    assert COL.compose_I(COL.parse_I(N2, w)) == N2, w
    if I2 != d['I']: ws.cell(r, C.SPLIT).value = I2
    if M2 != d['M']: ws.cell(r, C.SUF).value = M2
    if N2 != d['N']: ws.cell(r, C.COMBO).value = N2
    if I2 != d['I']:
        nS += 1; note = 'e 结尾：拆分 %s 改成 %s，后缀写全，两个 e 只写一个' % (d['I'], I2)
    else:
        nO += 1; note = 'e 结尾：后缀说明改成“和 -xx 的 e 只写一个”，和拆分一致'
    u0 = ws.cell(r, C.ADJ).value
    ws.cell(r, C.ADJ).value = (str(u0).rstrip('；') + '；' + note) if u0 else note
    fit(r); log.append((r, w, d['I'], I2))
print('split changed', nS, 'notes only', nO)
R = wb['整表核对记录']
last = R.max_row; n0 = int(R.cell(last, 1).value)
ok_row = next(rr for rr in range(last, 1, -1) if R.cell(rr, 2).value == '已修正')
sp_row = next(rr for rr in range(last, 1, -1) if R.cell(rr, 2).value == '特殊（未改）')
logs = [
 ('已修正', 'e 结尾的词加 -er / -ed / -en / -est', '用户问 maker 是不是该拆成 make + er、再去掉一个重复的 e。表里同一种情况两种写法：多数写全（organize + er、consume + er、scene + ery，以及 time + ing、use + able），%d 个按旧规矩把后缀砍短（make + r、use + d、take + n、late + st、piece + (e)d），学生看到的是并不存在的后缀“r”“d”；been 写成 be + n，拼出来是 ben' % nS,
  '拆分一律写全后缀：make + er、use + ed、take + en、late + est、see + en、been ← be + en；后缀列标签改成 -er / -ed / -en / -est，说明写“make 已经以 e 结尾，和 -er 的 e 只写一个：make + er → maker”；组合列公式、词性变化跟着改（%d 行）。另有 %d 行拆分本来就写全了（organize + ed、love + er），说明还写着“只加 d / 只加 r”，一并改成同样的说法' % (nS, nO)),
 ('特殊（未改）', 'e 结尾（不改的）', 'shown、known、grown、drawn、sown、sewn、thrown（show + n）和 first、amidst（fir + st、amid + st）：前面的词不是 e 结尾，本来就只加 n、st，照旧；arrest = ar + re + st 的 st 是词根（拉丁语 stare“站”），不是后缀', '照旧'),
]
for i, (cat, word, found, done) in enumerate(logs, 1):
    rr = last + i; src_row = ok_row if cat == '已修正' else sp_row
    for c, v in enumerate([str(n0 + i), cat, '—', word, found, done], 1):
        R.cell(rr, c).value = v; R.cell(rr, c)._style = copy.copy(R.cell(src_row, c)._style)
    R.row_dimensions[rr].height = R.row_dimensions[src_row].height
if R.auto_filter.ref: R.auto_filter.ref = 'A1:F%d' % (last + len(logs))
S = wb['说明']
assert S['A30'].value == '拆分'
S['B30'] = str(S['B30'].value).rstrip('。') + '。e 结尾的词加 -er、-ed、-en、-est，后缀写全：make + er、use + ed、take + en、late + est（两个 e 只写一个，后缀列写明）；不写成 make + r。'
last7 = S.max_row; assert S.cell(last7, 1).value == '英美写法'
rr = last7 + 1
for c in range(1, 5): S.cell(rr, c)._style = copy.copy(S.cell(last7, c)._style)
S.merge_cells('B%d:C%d' % (rr, rr))
S.cell(rr, 1).value = 'e 结尾加后缀'
S.cell(rr, 2).value = 'e 结尾的词加 -er、-ed、-en、-est，拆分写全后缀（make + r → make + er、use + d → use + ed、take + n → take + en、late + st → late + est，%d 个；been ← be + n 改成 be + en），后缀列写明“和 -er 的 e 只写一个：make + er → maker”；拆分本来就写全、说明还写“只加 d”的 %d 个一并改。' % (nS, nO)
S.cell(rr, 4).value = '=COUNTIF(拆分结果!$U$2:$U$9294,"*e 结尾：*")'
S.row_dimensions[rr].height = S.row_dimensions[last7].height
wb.save(OUT)
json.dump(log, open('/home/claude/work/ee_log.json', 'w'), ensure_ascii=False)

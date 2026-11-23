"""把新的含义列写回总表，顺带：L 列加【派生】【合成】【联想】、J 列“见【今义】”改“见含义列”、Q 列记录、
「整表核对记录」汇总、「说明」改写法说明并加一轮。"""
import re, copy, math, pickle, collections, sys
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
import overrides as O
from posify import ROWS
from assemble import POSRX

SRC = '/home/claude/src.xlsx'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/out/new.xlsx'
TAG = '含义词性'
final = pickle.load(open('/home/claude/work/final.pkl', 'rb'))
res = pickle.load(open('/home/claude/work/res4.pkl', 'rb'))

wb = load_workbook(SRC)
ws = wb['拆分结果']
assert ws.max_row == 9294

def seg_text(o):
    return ('（' + '）（'.join(o['labels']) + '）' if o['labels'] else '') + o['rest']

log = []          # 整表核对记录：(类别, 行, 单词, 发现的情况, 处理)
stat = collections.Counter()
moved_rows, merged_rows, j_rows = [], [], []
for rn in range(2, 9295):
    w = str(ws.cell(rn, 5).value)
    lines, moved = final[rn]
    a = res[rn][0]
    old = str(ws.cell(rn, 6).value or '')
    new = '\n'.join(lines)
    ws.cell(rn, 6).value = new
    al = copy.copy(ws.cell(rn, 6).alignment)
    ws.cell(rn, 6).alignment = Alignment(horizontal=al.horizontal, vertical=al.vertical or 'center', wrap_text=True)
    notes = ['每个意思一行，行首加词性']
    # 挪到 L 列
    if moved:
        L = str(ws.cell(rn, 12).value or '').strip()
        by = collections.OrderedDict()
        for lab, text in moved: by.setdefault(lab, []).append(text)
        add = '\n'.join(f'【{lab}】' + '；'.join(ts) for lab, ts in by.items())
        ws.cell(rn, 12).value = (L + '\n' + add) if L else add
        words = '、'.join(re.match(r"^(?:（[^（）]*）)*([A-Za-z][A-Za-z'’\-/ ]*?)(?=\s*[（\u4e00-\u9fff]|$)", t).group(1).strip() if re.match(r"^(?:（[^（）]*）)*[A-Za-z]", t) else t[:12] for _, t in moved)
        notes.append(f'含义里的 {words}（是别的词，不是这个词的意思）挪到 L 列' + '、'.join(f'【{l}】' for l in by))
        moved_rows.append((rn, w, words, list(by)))
        stat['moved'] += len(moved)
    # 并进上一条的说明、去掉的重复
    mg = [seg_text(o) for o in a if (rn, o['k']) in O.MERGE]
    dr = [seg_text(o) for o in a if (rn, o['k']) in O.DROP]
    if mg:
        notes.append('“' + '”“'.join(mg) + '”是说明，并进上一个意思的括号')
        merged_rows.append((rn, w, mg)); stat['merged'] += len(mg)
    if dr:
        notes.append('“' + '”“'.join(dr) + '”并进别的意思里')
        stat['dropped'] += len(dr)
    for (r0, k), why in O.FIX.items():
        if r0 == rn:
            notes.append(why)
            log.append(('已修正', rn, w, '含义：' + why, '已改：' + new.replace('\n', ' / ')))
    # J 列：见【今义】
    J = str(ws.cell(rn, 10).value or '')
    if '【今义】' in J:
        J2 = J.replace('见【今义】【趣】', '见含义列和【趣】').replace('【今义】', '含义列')
        ws.cell(rn, 10).value = J2
        n = J.count('【今义】')
        notes.append(f'组合列“见【今义】”改为“见含义列”（今义已挪到含义列）')
        j_rows.append((rn, w)); stat['j'] += n
    q = ws.cell(rn, 17)
    q.value = (str(q.value) + '；' if q.value else '') + f'{TAG}：' + '；'.join(notes)
    stat['rows'] += 1

# 行高：按各列文字的行数，只加高、不减（含义一行一个意思，列宽 30 → 40，少折行）
ws.column_dimensions['F'].width = 40
ws.freeze_panes = 'G2'          # 按技能的约定：冻结 G2，单词、含义一直看得见（上传的表只冻结了第一行）
W = {c: ws.column_dimensions[c].width or 10 for c in 'FHIJKLNOPQ'}
dw = lambda s: sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)
raised = 0
for r in range(2, 9295):
    best = max(sum(max(1, math.ceil(dw(l) / (W[c] - 1.5))) for l in str(ws[f'{c}{r}'].value or '').split('\n')) for c in 'FHIJKLNOP')
    need = round(best * 17.25, 2)
    if (ws.row_dimensions[r].height or 0) < need:
        ws.row_dimensions[r].height = need; raised += 1
stat['raised'] = raised

# 整表核对记录：汇总几类
pc = collections.Counter()
for rn in range(2, 9295):
    for l in final[rn][0]: pc[POSRX.match(l).group(1)] += 1
pos_sum = '、'.join(f'{p} {n}' for p, n in pc.most_common())
summary = [
    ('已修正', None, '含义列（全表）', '几个意思用“；”挤在一行里；词性只在换词性的地方用括号标，开头几个意思没写词性',
     f'改成每个意思一行、行首写词性（n. / v. / adj. / adv. / prep. / conj. / pron. / num. / int. / modal v. / aux. v. / phr.），9293 行、{sum(pc.values())} 个意思（{pos_sum}）；“（动）（形）（n.）”这类括号标签换成行首的词性，“（英）（口）（喻）”这类标签留在词性后面；同形词的 ①② 写在词性后面；一条标了两个词性的（“（v./n.）出口”）拆成两行。逐行见 Q 列“含义词性：…”'),
    ('已修正', None, '含义列', f'{stat["moved"]} 条“意思”其实是别的词（dazzle 的 dazzling、falcon 的 falconer、pony 的 ponytail、zero 的 zero-sum……），没法写成这个词的词性',
     f'挪到 L 列：派生词写【派生】，合成词写【合成】，scorpion 的 Scorpio、Scorpius 写【联想】；涉及 {len(moved_rows)} 行'),
    ('已修正', None, '含义列', f'{stat["merged"]} 条是说明不是意思（“复数 thieves”“也写 data set”“反义 unethical”“英式拼作 draughty”……）',
     '并进上一个意思后面的括号里'),
    ('已修正', None, '含义列', '拼写变体写成“同 colorful：色彩鲜艳的”“同 prioritize（英式拼写）”，视频会把“同 colorful”当成意思念出来；prioritise、memorise、socialise、behaviour 只写了“同 X”，没有意思',
     '改成“意思（英式拼写，同 X）”，四个只写“同 X”的补上意思'),
    ('已修正', None, '组合列', f'{stat["j"]} 处“见【今义】”（{len(j_rows)} 行：feather、wait、walk、put、stranger……）：今义已挪到含义列，指向不存在了',
     '改为“见含义列”'),
]
log = summary + log
R = wb['整表核对记录']
n0 = sum(1 for r in R.iter_rows(min_row=2, values_only=True) if r[0] is not None)
body = copy.copy(R.cell(2, 4)._style)
for k, (cat, r, w, what, how) in enumerate(log):
    i = n0 + k + 2
    vals = [n0 + k + 1, cat, f'=HYPERLINK("#\'拆分结果\'!E{r}","第 {r} 行")' if r else '—', w, what, how]
    for c, v in enumerate(vals, 1):
        cell = R.cell(i, c); cell.value = v; cell._style = copy.copy(body)
        cell.alignment = Alignment(wrap_text=True, vertical='top')
    if r: R.cell(i, 3).font = Font(name='微软雅黑', size=10, color='0563C1', underline='single')
    R.cell(i, 2).fill = PatternFill('solid', start_color='E2EFDA' if cat == '已修正' else 'FFF2CC')
    R.row_dimensions[i].height = 17.25 * max(1, math.ceil(max(len(what), len(how)) / 38))
R.auto_filter.ref = f'A1:F{R.max_row}'

# 说明
S = wb['说明']
S['B17'] = ('现在的意思：每个意思单独一行，行首写词性（n. 名词、v. 动词、adj. 形容词、adv. 副词、prep. 介词、conj. 连词、pron. 代词、num. 数词、'
            'int. 感叹词、modal v. 情态动词、aux. v. 助动词、phr. 短语），后面是意思，例子写在后面括号里（n. 比赛（a football match））；'
            '（英）（口）（喻）这类标签写在词性后面；同形词的 ①② 写在词性后面（2026-11 从组合列的【今义】挪过来，同月改成一行一个意思）')
S['B34'] = str(S['B34'].value).replace('每个词都要有含义（F 列）。', '每个词都要有含义（F 列，一行一个意思，行首写词性）。')
S['B27'] = str(S['B27'].value) + '“含义词性：…”'
for c in 'ABCD':
    S[f'{c}36']._style = copy.copy(S[f'{c}35']._style)
S['A36'] = '含义'
S['B36'] = ('一个意思一行，行首是词性缩写加一个空格：“n. 比赛（a football match）”。'
            '同一个意思兼两种词性的写两行（v. 出口 / n. 出口）；固定搭配、习语写 phr.（phr. carry out 执行）；'
            '“（英）（口）（喻）（计算机）”这类标签放在词性后面（n. （英）酒馆、酒吧）；一行里不再用“；”隔开几个意思（括号里的例子可以用“；”）。'
            '派生词、合成词（dazzling、ponytail）不写在含义里，写在 L 列【派生】【合成】；拼写变体写“意思（英式拼写，同 X）”；'
            '以“=”开头的写成“（= X）意思”。')
S.merge_cells('B36:D36')
S.row_dimensions[36].height = 75
for c in 'ABCD':
    S[f'{c}101']._style = copy.copy(S[f'{c}100']._style)
S['A101'] = '含义词性分行'
S['B101'] = ('含义列每个意思单独一行，行首写词性（n. / v. / adj. / adv. / prep. / conj. / pron. / num. / int. / modal v. / aux. v. / phr.）；'
             f'{stat["moved"]} 条其实是别的词（dazzling、falconer、ponytail……）挪到 L 列【派生】【合成】；说明性的条目并进括号；拼写变体补意思；'
             '组合列“见【今义】”改为“见含义列”；F 列宽 30 → 40，冻结窗格恢复到 G2（单词、含义一直看得见）。逐行见 Q 列“含义词性：…”。')
S.merge_cells('B101:C101')
S['D101'] = '=COUNTIF(拆分结果!$Q$2:$Q$9294,"*含义词性*")'
S.row_dimensions[101].height = 60
wb.save(OUT)
print(dict(stat)); print('log', len(log))
print('moved rows', len(moved_rows), moved_rows[:5])

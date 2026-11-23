"""给总表补后缀说明（来源、作用、在这里讲词性）和意思演变（意思怎么变、用词规律），写出新表。
用法：python3 sense_write.py <源表.xlsx> <新表.xlsx>
已经写过的行（有“在这里：”的后缀行、有“意思怎么变：”的词）会跳过，所以加了新词以后可以再跑一遍，只补新词。
每行写 T 列；「整表核对记录」按类别各记一条汇总，「说明」最后（七、各轮调整）补一行；「用词规律一览」每次按全表重算。不新建逐条记录表（用户要表清爽）。
"""
import re, copy, math, pickle, collections, sys, os
SRC, OUT = sys.argv[1], sys.argv[2]
os.environ['ETY_SRC'] = SRC
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sense_rules as PL
import cols as C
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment
H, recs = PL.run()
T = PL.T
orig = {i: str(x[9] or '').split('\n') for i, x in enumerate(T, start=2)}
ADDED = [r for r in recs if r[0] in ('意思怎么变', '用词规律')]
recs = [r for r in recs if r[0] not in ('意思怎么变', '用词规律')]
for cat, r, w, lab, old, new in ADDED:
    src = str(T[r - 2][10] or '')
    assert new.count('〔') == new.count('〕'), (r, w, new[:80])
    for a, b in (('（', '）'),):
        if new.count(a) != new.count(b) and src.count(a) == src.count(b): print('括号', r, w, new[:100])
M = collections.OrderedDict()
for cat, r, w, lab, old, new in recs:
    k = next((j for j, l in enumerate(orig[r]) if l == old), None)
    if k is None: k = next(j for j, l in enumerate(H[r]) if l == new)
    if (r, k) in M: M[(r, k)]['new'] = new; M[(r, k)]['cat'] += '；' + cat
    else: M[(r, k)] = dict(cat=cat, row=r, word=w, lab=lab, old=orig[r][k], new=new)
for (r, k), d in M.items():
    d['new'] = H[r][k]
bad = []
for d in M.values():
    n, o = d['new'], d['old']
    for p in ('（，', '（；', '，）', '；）', '；；', '，，', '（）', '””', '““', '\x00'):
        if p in n and p not in o: bad.append((d['row'], d['word'], p, n[:120]))
    for a, b in (('（', '）'), ('“', '”')):
        if n.count(a) != n.count(b) and o.count(a) == o.count(b): bad.append((d['row'], d['word'], a + b, n[:120]))
    pass
for b in bad: print('PROBLEM', b)
assert not bad
wb = load_workbook(SRC); ws = wb['拆分结果']
W = {c: ws.column_dimensions[c].width or 10 for c in C.TEXT_COLS}
dw = lambda s: sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)
byrow = collections.defaultdict(list)
for d in M.values(): byrow[d['row']].append(d)
def note(d):
    c = d['cat']
    if c.startswith('同源'): return f'{d["lab"]} 恢复同源的“见”'
    if c.startswith('前缀：in-'): return 'in- 补“见 in”'
    if c.startswith('前缀'): return f'{d["lab"]} 补了来源'
    return d['lab'] + ' 补了' + c.replace('后缀：', '').replace('补“见 like”', '见 like')
evo_rows = collections.defaultdict(list)
for cat, r, w, lab, old, new in ADDED: evo_rows[r].append(cat)
for r in set(byrow) | set(evo_rows):
    C.set_parts(ws, r, '\n'.join(H[r]))          # 各部分解释写回前缀、词根、单词部分、后缀四列
    p = ws.cell(r, C.ADJ); notes = []
    if r in byrow: notes.append('后缀说明：' + '；'.join(note(d) for d in byrow[r]))
    if r in evo_rows: notes.append('意思演变：补了' + '、'.join(evo_rows[r]))
    p.value = (p.value + '；' if p.value else '') + '；'.join(notes)
    best = max(sum(max(1, math.ceil(dw(l) / (W[c] - 1.5))) for l in str(ws[f'{c}{r}'].value or '').split('\n')) for c in C.TEXT_COLS)
    need = round(best * 17.25, 2)
    if (ws.row_dimensions[r].height or 0) < need: ws.row_dimensions[r].height = need
ref = wb['整表核对记录']
body = copy.copy(ref.cell(2, 4)._style)
cnt = collections.Counter()
for d in M.values():
    for part in ('作用', '来源', '在这里'):
        if d['cat'].startswith('后缀') and part in d['cat']: cnt[part] += 1
    cnt[d['cat'].split('：')[0]] += 1
n0 = sum(1 for row in ref.iter_rows(min_row=2, values_only=True) if row[0] is not None)
nevo = sum(1 for x in ADDED if x[0] == '意思怎么变'); nrule = sum(1 for x in ADDED if x[0] == '用词规律')
summ = [
 ('意思怎么变、用词规律', '一词多义的词（如 communication 既是“交流”，又是“信息”“通信手段”），各部分解释里没写这几个意思是怎么来的、用到了英语的哪条用词规律',
  f'照组合列 → 那几行，在各部分解释里加“意思怎么变：…” {nevo} 行，每一步用到的规律标〔用词规律①〕；再加“用词规律：…” {nrule} 行，写规律 + 本词 + 一个熟悉的例子（例子都是总表里的词）。规律共 {len(PL.EX)} 种，每种的说明、例子、用到的词见「用词规律一览」。逐条见「拆分结果」T 列“意思演变：…”'),
 ('后缀说明（来源、作用、在这里）', '后缀行多数只写了意思，没写这个后缀从哪儿来（母词），也没写它在这个词里起什么作用；上一轮删掉无关的“见”以后更显得单薄',
  f'按 etymonline 等查了来源，逐行补上：来源（母词）{cnt["来源"]} 行，如 -er“英语本来就有的后缀，古英语写作 -ere”、-ion“来自拉丁语名词词尾 -io”、-able“来自拉丁语 -abilis，和单词 able 不是一个来源”；作用（加在什么词后面、变成什么词）{cnt["作用"]} 行；“在这里”改成讲词性：原来是什么词、加上后缀变成什么词、两种词各说的是什么，所以有了哪几个意思，{cnt["在这里"]} 行。逐条见「拆分结果」T 列“后缀说明：…”'),
 ('前缀 re- / un- / dis- 的来源', '上一轮删掉“见”以后，这几个前缀没写来源', f'补上来源 {sum(1 for d in M.values() if d["cat"] == "前缀：补来源")} 行（dis-“一分为二、向两边”，和 duo“二”有关等）；in- 的来源后补“见 in”'),
 ('跨组同源的“见”', '上一轮把 noct 见 night 这类同源的“见”删了；同源词对记词根有帮助', f'恢复对记词有帮助的 {sum(1 for d in M.values() if d["cat"].startswith("同源"))} 处（noct 见 night、ed 见 eat、ton 见 thunder 等）；-ly 行提到 like 的补“见 like”；关系太远的（digit 和 judge、merry 和 brief 等）仍不加'),
]
summ = [x for x in summ if not re.search(r'(补上来源|恢复对记词有帮助的) 0 ', x[2])] if (M or ADDED) else []
if nevo == 0: summ = [x for x in summ if x[0] != '意思怎么变、用词规律']
for k, (w, what, how) in enumerate(summ):
    i = n0 + k + 2
    for c, v in enumerate([n0 + k + 1, '已修正', '—', w, what, how], 1):
        cell = ref.cell(i, c); cell.value = v; cell._style = copy.copy(ref.cell(2, 4)._style); cell.alignment = Alignment(wrap_text=True, vertical='top')
    ref.cell(i, 2).fill = PatternFill('solid', start_color='E2EFDA')
    ref.row_dimensions[i].height = 17.25 * max(1, math.ceil(max(len(what), len(how)) / 38))
ref.auto_filter.ref = f'A1:F{ref.max_row}'
# 「说明」最后一节（七、各轮调整）补一行
if summ:
    S = wb['说明']
    last = max(r for r in range(1, S.max_row + 1) if S.cell(r, 1).value)
    r1 = last + 1
    NR = ws.max_row
    S.cell(r1, 1).value = '后缀说明、意思演变（补新词）'
    S.cell(r1, 2).value = f'补后缀说明 {len(M)} 处、意思怎么变 {nevo} 行、用词规律 {nrule} 行；逐行见 T 列“后缀说明：…”“意思演变：…”。'
    S.cell(r1, 4).value = f'=COUNTIF(拆分结果!$T$2:$T${NR},"*后缀说明*")'
    for c in (1, 2, 3, 4):
        S.cell(r1, c)._style = copy.copy(S.cell(last, c)._style)
    S.merge_cells(f'B{r1}:C{r1}')
# ---- 用词规律一览 ----
use = collections.defaultdict(list)
text2key = {v[0]: k for k, v in PL.EX.items()}
for r in sorted(H):
    new = next((l for l in H[r] if l.startswith('用词规律：')), None)
    if not new: continue
    wd = str(T[r - 2][4])
    for t in re.findall(r'[①②③④⑤⑥] (.+?)（', new):
        k = text2key.get(t.strip()) or next((kk for kk, vv in PL.EX.items() if vv[0].startswith(t.strip())), None)
        if k and wd not in use[k]: use[k].append(wd)
if '用词规律一览' in wb.sheetnames: del wb['用词规律一览']
G = wb.create_sheet('用词规律一览', index=wb.sheetnames.index('说明'))
for c, h in enumerate(['序', '用词规律', '为什么会这样', '例子（总表里的词）', '表里用到的词数', '用到这条规律的词（前 40 个）'], 1):
    G.cell(1, c).value = h; G.cell(1, c)._style = copy.copy(ref.cell(1, 1)._style)
for col, wdt in zip('ABCDEF', (5, 40, 46, 40, 10, 70)): G.column_dimensions[col].width = wdt
order_k = sorted(PL.EX, key=lambda k: -len(use[k]))
for n, k in enumerate(order_k, start=1):
    text, exs = PL.EX[k]
    vals = [n, text, PL.WHY.get(k, ''), '；'.join(exs), len(use[k]), '、'.join(use[k][:40])]
    for c, v in enumerate(vals, 1):
        cell = G.cell(n + 1, c); cell.value = v; cell._style = copy.copy(body); cell.alignment = Alignment(wrap_text=True, vertical='top')
    G.cell(n + 1, 2).fill = PatternFill('solid', start_color='FFF2CC')
    G.row_dimensions[n + 1].height = 17.25 * max(2, math.ceil(dw('、'.join(use[k][:40])) / 136))
G.freeze_panes = 'A2'
wb.save(OUT)
print('改写', len(M), '处；新加', len(ADDED), '行；涉及', len(set(byrow) | set(evo_rows)), '行'); print(cnt)

import sys, re, json, copy, math
sys.path.insert(0, '/home/claude/work'); sys.path.insert(0, '/home/claude/work/new_maint/etymology-table/scripts')
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import cols as C, columns as COL
SRC, OUT = sys.argv[1], sys.argv[2]
P = json.load(open('/home/claude/work/pinxie_plan.json'))
plan, splitfix = P['plan'], {int(k): v for k, v in P['splitfix'].items()}
COLN = {'J': C.PRE, 'K': C.ROOT, 'L': C.WPART, 'M': C.SUF}
KIND_ZH = {'drop_e': '去 e', 'keep_e_soft': '留 e', 'y_i': 'y 变 i', 'y_drop': 'y 去掉', 'double': '双写', 'le_ly': '-le 变 -ly', 'ble_bil': '-ble 变 -bil-',
           'drop_e_cons': '去 e（例外）', 'vowel_drop': '去掉末尾元音', 'd_s': 'd 变 s', 'd_t': 'd 变 t', 't_ss': 't 变 ss', 'nt_nce': '-nt 变 -nce', 'te_cy': '-te 变 -cy',
           'fy_fic': '-fy 变 -fication', 'fy_fac': '-fy 变 -faction', 'er_r': '-er 去 e', 'ess': '-ess 去元音', 'le_ul': '-le 变 -ul-', 'ous_os': '-ous 变 -os-',
           'th_vowel': '元音变', 'ai_a': 'ai 变 a', 'ou_u': 'ou 变 u', 'ce_ct': 'ce 变 c', 'olve': 'v 变 u', 'tain': '-tain 变 -ten-', 'ceive': '-ceive 变 -cep-',
           'scribe': '-scribe 变 -scrip-', 'sume': '-sume 变 -sump-', 'destroy': 'destroy 变 destruct-', 'our_or': '-our 变 -or-', 'f_v': 'f 变 v', 'ie_y': 'ie 变 y', 'll_l': 'll 变 l', 'prefix': '前缀同化'}
PRE_NOTE = {'com': 'con- 在 b、m、p 前写成 com-（读着顺；在 l 前写 col-，在 r 前写 cor-，在元音和 h 前写 co-）', 'col': 'con- 在 l 前写成 col-（读着顺，同 collect、collapse）',
            'co': 'con- 在元音和 h 前写成 co-（同 cooperate、coherent）', 'im': 'in- 在 b、m、p 前写成 im-（读着顺，同 impossible、imbalance）',
            'sus': 'sub- 在 c、p、t 前有时写成 sus-（同 sustain、suspect）', 'ef': 'ex- 在 f 前写成 ef-（读着顺，同 effort、efficient）',
            'em': 'en- / in- 在 b、p 前写成 em-（同 embrace、employ）'}
PRE_DONE = re.compile(r'同化|变成|变为|写成|写作|写法|拼成|拼作|简化|前写|前面|之前|受后面|读着顺|顺口|好读|发音|的变体|脱落|只剩|掉了|磨短|弱化')
# 同化的前缀：这一行说了来源（= ad- 或 拉丁语 ad）才补规则
ASSIM = {
 'ac': ('ad', 'ad- 在 c、q 前写成 ac-（d 跟着后面的辅音变，读着顺；同 accept、acquire）'), 'af': ('ad', 'ad- 在 f 前写成 af-（d 跟着后面的辅音变，读着顺；同 affect、afford）'),
 'ag': ('ad', 'ad- 在 g 前写成 ag-（d 跟着后面的辅音变，读着顺；同 aggressive）'), 'al': ('ad', 'ad- 在 l 前写成 al-（d 跟着后面的辅音变，读着顺；同 allow、allocate）'),
 'an': ('ad', 'ad- 在 n 前写成 an-（d 跟着后面的辅音变，读着顺；同 announce、annotate）'), 'ap': ('ad', 'ad- 在 p 前写成 ap-（d 跟着后面的辅音变，读着顺；同 appear、approve）'),
 'ar': ('ad', 'ad- 在 r 前写成 ar-（d 跟着后面的辅音变，读着顺；同 arrive、arrange）'), 'as': ('ad', 'ad- 在 s 前写成 as-（d 跟着后面的辅音变，读着顺；同 assist、assume）'),
 'at': ('ad', 'ad- 在 t 前写成 at-（d 跟着后面的辅音变，读着顺；同 attract、attend）'),
 'il': ('in', 'in- 在 l 前写成 il-（n 跟着后面的辅音变，读着顺；同 illegal、illuminate）'), 'im': ('in', 'in- 在 b、m、p 前写成 im-（n 跟着后面的辅音变，读着顺；同 impossible、immigrate）'),
 'ir': ('in', 'in- 在 r 前写成 ir-（n 跟着后面的辅音变，读着顺；同 irregular、irrigate）'),
 'col': ('con', 'con- 在 l 前写成 col-（读着顺；同 collect、collapse）'), 'com': ('con', 'con- 在 b、m、p 前写成 com-（读着顺；在 l 前写 col-，在 r 前写 cor-，在元音和 h 前写 co-）'),
 'cor': ('con', 'con- 在 r 前写成 cor-（读着顺；同 correct、correspond）'),
 'ef': ('ex', 'ex- 在 f 前写成 ef-（读着顺；同 effort、efficient）'),
 'suc': ('sub', 'sub- 在 c 前写成 suc-（b 跟着后面的辅音变；同 succeed、success）'), 'suf': ('sub', 'sub- 在 f 前写成 suf-（b 跟着后面的辅音变；同 suffer、sufficient）'),
 'sug': ('sub', 'sub- 在 g 前写成 sug-（b 跟着后面的辅音变；同 suggest）'), 'sup': ('sub', 'sub- 在 p 前写成 sup-（b 跟着后面的辅音变；同 support、suppose）'),
 'sus': ('sub', 'sub- 在 c、p、t 前有时写成 sus-（同 sustain、suspect）'),
 'oc': ('ob', 'ob- 在 c 前写成 oc-（b 跟着后面的辅音变；同 occur、occupy）'), 'of': ('ob', 'ob- 在 f 前写成 of-（b 跟着后面的辅音变；同 offer、offend）'),
 'op': ('ob', 'ob- 在 p 前写成 op-（b 跟着后面的辅音变；同 oppose、opportunity）'),
 'dif': ('dis', 'dis- 在 f 前写成 dif-（s 跟着后面的辅音变；同 differ、difficult）'),
 'sym': ('syn', 'syn- 在 b、m、p 前写成 sym-（读着顺；同 symbol、sympathy）'), 'syl': ('syn', 'syn- 在 l 前写成 syl-（同 syllable）'),
 'em': ('en', 'en- 在 b、p 前写成 em-（读着顺；同 embrace、employ）'),
}

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

byrow = {}
for r, w, kind, col, li, note in plan:
    byrow.setdefault(r, []).append((kind, col, li, note))
# 前缀同化：说明缺的补上
for r in range(2, ws.max_row + 1):
    J = str(ws.cell(r, C.PRE).value or '')
    for li, l in enumerate(J.split('\n')):
        m = re.match(r'^([a-z]+)-[：:]', l)
        if not m or PRE_DONE.search(l): continue
        f = m.group(1)
        if f in ASSIM:
            orig, txt = ASSIM[f]
            src = {'con': 'cum|com-|con-', 'en': 'en-|in-|法语 en'}.get(orig, re.escape(orig) + '[-“ ]')
            if re.search(r'(= ?|拉丁语 ?|来自 ?)(' + src + ')', l) or re.search(r'= ?' + re.escape(orig) + '-', l):
                byrow.setdefault(r, []).append(('prefix', 'J', li, txt))
        elif f == 'co' and re.search(r'cum|com-|con-', l):
            byrow.setdefault(r, []).append(('prefix', 'J', li, 'con- 在元音和 h 前写成 co-（同 cooperate、coherent）'))

stats = {}; nsplit = 0; nrows = 0; log = []
for r in range(2, ws.max_row + 1):
    if ws.cell(r, C.WORD).value == 'population':
        N = str(ws.cell(r, C.COMBO).value)
        if N.startswith('【构词逻辑】populate（') and '+ ation（' in N.split('\n')[0] and str(ws.cell(r, C.SPLIT).value) == 'populate + ion':
            L = N.split('\n'); L[0] = L[0].replace('+ ation（', '+ ion（', 1); ws.cell(r, C.COMBO).value = '\n'.join(L)
for r in sorted(set(byrow) | set(splitfix)):
    w = str(ws.cell(r, C.WORD).value)
    kinds = []
    for kind, col, li, note in byrow.get(r, []):
        c = COLN[col]; L = str(ws.cell(r, c).value or '').split('\n')
        line = L[li]
        if note in line: continue
        L[li] = line.rstrip('。；') + '；' + note
        ws.cell(r, c).value = '\n'.join(L)
        kinds.append(KIND_ZH[kind]); stats[kind] = stats.get(kind, 0) + 1
    if r in splitfix:
        old = str(ws.cell(r, C.SPLIT).value); new = splitfix[r]
        ws.cell(r, C.SPLIT).value = new; nsplit += 1
        # 组合列第一行、后缀标签里写成 ny、ten 的，改成 y、en
        o = [p.strip() for p in old.split('；')[0].split('← ')[-1].split(' + ')]
        n = [p.strip() for p in new.split('；')[0].split('← ')[-1].split(' + ')]
        N = str(ws.cell(r, C.COMBO).value or ''); M = str(ws.cell(r, C.SUF).value or '')
        for p in o:
            if p not in n and len(p) >= 2 and p[1:] in n:
                prevp = o[o.index(p) - 1]
                M = M.replace('%s + %s' % (prevp, p), '%s + %s + %s' % (prevp, p[0], p[1:]))
                N = N.replace('%s + %s' % (prevp, p), '%s + %s + %s' % (prevp, p[0], p[1:]))
                N0 = N.split('\n'); N0[0] = N0[0].replace('+ %s（' % p, '+ %s（' % p[1:]); N0[0] = N0[0].replace('（-%s）' % p, '（-%s）' % p[1:]); N = '\n'.join(N0)
                M = re.sub(r'(^|\n)-%s：' % re.escape(p), lambda m: m.group(1) + '-%s：' % p[1:], M)
        assert COL.compose_I(COL.parse_I(N, w), ) == N, w
        ws.cell(r, C.COMBO).value = N; ws.cell(r, C.SUF).value = M
        kinds.append('拆分写出双写的字母（%s → %s）' % (old, new))
    if kinds:
        nrows += 1
        note_u = '拼写变化：' + '、'.join(dict.fromkeys(kinds))
        u0 = ws.cell(r, C.ADJ).value
        ws.cell(r, C.ADJ).value = (str(u0).rstrip('；') + '；' + note_u) if u0 else note_u
        fit(r); log.append((r, w, kinds))
print('rows', nrows, 'splits', nsplit, 'notes', sum(stats.values())); print(stats)

total = sum(stats.values())
R = wb['整表核对记录']
last = R.max_row; n0 = int(R.cell(last, 1).value)
ok_row = next(rr for rr in range(last, 1, -1) if R.cell(rr, 2).value == '已修正')
sp_row = next(rr for rr in range(last, 1, -1) if R.cell(rr, 2).value == '特殊（未改）')
g = lambda *ks: sum(stats.get(k, 0) for k in ks)
logs = [
 ('已修正', '加词缀时的拼写变化', '用户要求：time + ing、use + able、populate + ion 这类后缀开头不是 e 的词，后缀列补一句“time 的 e 遇到 -ing 去掉”，并看看还有没有别的加词缀时的特殊现象。逐个对了全表拆分和单词的拼法，加词缀时拼写变了的边界，多数没在后缀列说明',
  '在那个词缀那一行末尾补一句，共 %d 处：去 e %d（time + ing → timing）；y 变 i %d（happy + ness → happiness）、y 去掉 %d（history + ic → historic）；双写 %d（run + n + er → runner，英式 l 双写另说）；-le 变 -ly %d（possible → possibly）；-ble 变 -bil- %d；留 e 读软音 %d（changeable、courageous）；去 e 的例外 %d（truly、wisdom）；-nt 变 -nce / -ncy %d（silent → silence）；-fy 变 -fication %d；d(e) 变 s / t、t 变 ss 等拉丁语过去分词拼法 %d（decide → decision、permit → permission）；去掉末尾元音 %d（piano → pianist）；-er 去 e %d（hunger → hungry）；元音变 %d（long → length）；别的 %d。前缀同化说明缺的补了 %d 处（con- 在 b、m、p 前写成 com-）'
  % (total, g('drop_e'), g('y_i'), g('y_drop'), g('double'), g('le_ly'), g('ble_bil'), g('keep_e_soft'), g('drop_e_cons'), g('nt_nce'), g('fy_fic'), g('d_s', 'd_t', 't_ss', 'ce_ct', 'ceive', 'scribe', 'tain', 'sume', 'olve', 'destroy', 'fy_fac'), g('vowel_drop'), g('er_r'), g('th_vowel'),
     total - g('drop_e', 'y_i', 'y_drop', 'double', 'le_ly', 'ble_bil', 'keep_e_soft', 'drop_e_cons', 'nt_nce', 'fy_fic', 'd_s', 'd_t', 't_ss', 'ce_ct', 'ceive', 'scribe', 'tain', 'sume', 'olve', 'destroy', 'fy_fac', 'vowel_drop', 'er_r', 'th_vowel', 'prefix'), g('prefix'))),
 ('已修正', '双写的字母写进拆分', '双写的字母有的拆成 swim + ming、fun + ny（后缀成了并不存在的“ming”“ny”），有的没写出来（forget + able、wed + ing、jag + ed），和 plan + n + ed 的写法不一致',
  '统一写成 plan + n + ed 的样子：swim + m + ing、fun + n + y、forget + t + able、wed + d + ing、bag + g + y，共 %d 个；组合列公式、后缀标签里写成 ny、ten 的跟着改成 y、en' % nsplit),
 ('特殊（未改）', '拼写变化（不加说明的）', '拉丁语、法语词干本身就不一样、不是加词缀时才变的（repeat → repetition、acquire → acquisition、Norway → Norwegian、Saturn + day、maximum + ize 这类约 200 处），不当拼写变化说明；wherever、twentieth、cranberry 这类变化发生在合成词的两个词之间（不在后缀上），也不补', '照旧'),
]
for i, (cat, word, found, done) in enumerate(logs, 1):
    rr = last + i; src_row = ok_row if cat == '已修正' else sp_row
    for c, v in enumerate([str(n0 + i), cat, '—', word, found, done], 1):
        R.cell(rr, c).value = v; R.cell(rr, c)._style = copy.copy(R.cell(src_row, c)._style)
    R.row_dimensions[rr].height = R.row_dimensions[src_row].height
if R.auto_filter.ref: R.auto_filter.ref = 'A1:F%d' % (last + len(logs))
S = wb['说明']
assert S['A32'].value == '后缀行'
S['B32'] = str(S['B32'].value).rstrip('。') + '。加这个后缀时拼写变了的（去 e、y 变 i、双写、-le 变 -ly、-ble 变 -bil-、-nt 变 -nce……），在这一行末尾写一句：“time 末尾的 e 遇到元音开头的 -ing 就去掉：time + ing → timing”。'
assert S['A30'].value == '拆分'
S['B30'] = str(S['B30'].value).rstrip('。') + '。双写的字母单独写一部分：swim + m + ing、fun + n + y、forget + t + able，不写成 swim + ming。'
last7 = S.max_row; assert S.cell(last7, 1).value == 'e 结尾加后缀'
rr = last7 + 1
for c in range(1, 5): S.cell(rr, c)._style = copy.copy(S.cell(last7, c)._style)
S.merge_cells('B%d:C%d' % (rr, rr))
S.cell(rr, 1).value = '拼写变化'
S.cell(rr, 2).value = '加词缀时拼写变了的，在那个词缀那一行末尾写一句（%d 处）：去 e（time + ing → timing）、y 变 i（happiness）、双写（runner）、-le 变 -ly（possibly）、-ble 变 -bil-（ability）、留 e 读软音（changeable）、-nt 变 -nce（silence）、-fy 变 -fication、d 变 s（decision）、t 变 ss（permission）等；双写的字母统一单独写一部分（swim + m + ing，%d 个）。' % (total, nsplit)
S.cell(rr, 4).value = '=COUNTIF(拆分结果!$U$2:$U$9294,"*拼写变化：*")'
S.row_dimensions[rr].height = S.row_dimensions[last7].height
wb.save(OUT)
json.dump(log, open('/home/claude/work/pinxie_log.json', 'w'), ensure_ascii=False)

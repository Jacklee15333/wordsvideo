"""组合列只留组合公式、今义挪到新的「含义」列（F 列，单词后面）。
用法：python3 round2.py <源.xlsx> <输出.xlsx> [--dry]"""
import sys, re, copy, math, collections
sys.path.insert(0, '/home/claude/work/etymology-table/scripts')
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
import columns as C
from condense import top_eq_parts
from parse import parse_split

SRC, OUT = sys.argv[1], sys.argv[2]
DRY = '--dry' in sys.argv
wb = load_workbook(SRC)
ws = wb['拆分结果']
N = ws.max_row
NC = 17
SENTB = re.compile(r'^(?P<w>[^“”（）]+?)\s*“(?P<g>(?:[^“”]|“[^“”]*”)*)”(?:（本义“(?P<b>[^“”]*)”）)?$')
BLK = re.compile(r'^\s*[\u2460-\u2473]?\s*【([^【】]{1,10})】')

# ---------------------------------------------------------------- 手工写的第一行（自动认不出、或有说明要另放的）
# 单词: (新第一行（不含词性变化；写了“；词性变化”的就用它自己的）, 放在步骤前面的行, {要替换的行: 新行})
MANUAL = {
 'reusable': ('【构词逻辑】reuse（重复使用）+ able（能被…的）=“能再用的”', [], {}),
 'organise': ('【构词逻辑】organ（器官）+ ise（使…化、使成为…）=“使各部分各司其职”', [], {}),
 'unthinkable': ('【构词逻辑】un（不）+ think（想）+ able（能被…的）=“想都不能想的”', [], {}),
 'irreplaceable': ('【构词逻辑】ir（不）+ replace（替换）+ able（能被…的、值得…的）=“不能被替换的”', [], {}),
 'especially': ('【构词逻辑】e + special（特别的）+ ly（…地）=“特别地”', [], {}),
 'meanly': ('【构词逻辑】mean（卑劣、小气的）+ ly（以…的方式）=“以卑劣、小气的方式”', [], {}),
 'diplomat': ('【构词逻辑】di（二）+ plo（折）+ mat（…出来的东西）=“对折起来的公文”', [], {}),
 'smartly': ('【构词逻辑】smart（猛烈的；利落的；聪明的）+ ly（以…的方式）=“以 smart 的方式”', [], {'smartly 也跟着走：': 'smart 有几个意思，smartly 也跟着走：'}),
 'utterly': ('【构词逻辑】utter（更外面的 → 极端的）+ ly（以…的方式）=“极端地”', [], {}),
 'economically': ('【构词逻辑】economical（经济的；节约的）+ ly（…地）=“经济上 / 节约地”', [], {}),
 'probably': ('【构词逻辑】probable（很可能的）+ ly（以…的方式、在…程度上）=“很可能地”', [], {}),
 'unwavering': ('【构词逻辑】un（不）+ waver（摇来摆去）+ ing（正在…的）=“不摇摆的”', [], {}),
 'unladylike': ('【构词逻辑】un（不）+ lady（淑女）+ like（像…的）=“不像淑女的”', [], {}),
 'automated': ('【构词逻辑】automation（自动化）+ ed（被…了的、已经…了的）=“被自动化了的”', [], {}),
 'muddy-shelled': ('【构词逻辑】muddy（沾满泥的）+ shell（壳）+ ed（长着…的）=“壳上沾满泥的”', [], {}),
 'chaotic': ('【构词逻辑】chaos（混沌）+ t + ic（…的、与…有关的）=“混沌的”', [], {}),
 'thrift': ('【构词逻辑】thrive（兴旺）+ t（…这件事、…的结果）=“兴旺这件事”', [], {}),
 'preschooler': ('【构词逻辑】preschool（学前教育、幼儿园）+ er（…的人）=“处在学前阶段的孩子”；词性变化（-er）：名词 → 名词（人）', [], {}),
 'optimist': ('【构词逻辑】optim（最好的）+ ist（做…的人、信奉…主张的人）=“信奉“最好”主义的人”', [], {}),
 'afterwards': ('【构词逻辑】afterward（后来）+ s（副词词尾）=“后来”（意思不变）', [], {}),
 'interactive': ('【构词逻辑】interact（相互作用）+ ive（有…性质的、会…的）=“会相互作用的”', ['（也可以看成 inter + active）'], {}),
 'investigator': ('【构词逻辑】investigate（调查）+ or（做…的人或东西）=“调查的人”', ['（investigate 字面是“顺着脚印追”，所以也是“顺着脚印追的人”，见 investigate）'], {}),
 'cheapness': ('【构词逻辑】cheap（便宜的）+ ness（…的状态、性质）=“便宜的状态”（1540s）', [], {}),
 'isolation': ('【构词逻辑】isolate（使成为岛）+ ion（…这件事）=“成为孤岛的状态”（1800 年）', [], {}),
 'video-called': ('【构词逻辑】video（视频）+ called（打过电话了）=“视频通话了”', [], {}),
 'passers-by': ('【构词逻辑】passers（经过的人们）+ by（从旁边）=“从旁边经过的人们”', [], {}),
 'dubbing': ('【构词逻辑】dub（配音）+ b + ing（…这件事）=“配音这件事”', [], {}),
}
KEEP = {'statistic', 'defence', 'freshmen', 'footmen', 'businessmen', 'postmen', 'craftsmen'}   # 没有组合公式可写，派生路线本身在讲来历


def h_gloss(H, part):
    """各部分解释里这一部分的短意思：标签对上 part，取冒号后第一个引号里的，没有引号就取到第一个括号、分号、句号前"""
    k = re.sub(r'[^a-z]', '', part.lower())
    for l in str(H or '').split('\n'):
        if '：' not in l:
            continue
        lab, txt = l.split('：', 1)
        if re.sub(r'[^a-z]', '', re.sub(r'（[^（）]*）|\([^()]*\)', '', lab).lower()) != k:
            continue
        cut = re.split(r'[（；。，]', txt, 1)[0]
        q = re.search(r'“([^“”]+)”', cut)
        g = (q.group(1) if q else cut).strip(' “”')
        return g if 0 < len(g) <= 12 and re.search(r'[\u4e00-\u9fff]', g) else ''
    return ''


def convert(w, G, H, I):
    L = str(I or '').split('\n')
    if not L[0].startswith('【构词逻辑】派生路线'):
        return I, None
    if w in KEEP:
        return I, '保留·没有组合公式'
    mt = C.TAILPOS.search(L[0])
    tail = L[0][mt.start():] if mt else ''
    first = L[0][:mt.start()] if mt else L[0]
    rest, seen = [], False
    for l in L[1:]:
        if C.STEP.match(l):
            seen = True
        if not seen and C.sentence_from_eq(l):
            continue                                        # 原来单写的后缀等式，并进第一行
        rest.append(l)
    ps = [p for p in (parse_split(G) or [])]
    kind = None
    if w in MANUAL:
        nf, extra, repl = MANUAL[w]
        if '；词性变化' in nf:
            tail = ''
        rest = [repl.get(l, l) for l in rest]
        rest = extra + rest
        new_first, kind = nf, '手写'
    else:
        d = C.parse_I(I, w)
        terms, lit, route = top_eq_parts(first)
        if d['pos']:
            if len(d['pos']) != 1:
                return I, '保留·几个后缀'
            m = C.SENT.match(C.pos_sentence(d['pos'][0][1]))
            mb = SENTB.match(m.group('base').strip()) if m else None
            ps2 = [p for k, p in enumerate(ps) if not (k > 0 and len(re.sub(r'[^a-z]', '', p['surface'].lower())) == 1
                                                         and ps[k - 1]['surface'].lower().endswith(p['surface'].lower()))]
            if not m or not mb or len(ps2) != 2:
                return I, '认不出'
            full0 = re.sub(r'[^A-Za-z-]', '', ps2[0]['full'])
            base = mb.group('w').strip() if re.sub(r'[^a-z]', '', mb.group('w').lower()) == re.sub(r'[^a-z]', '', full0.lower()) else ps2[0]['surface']
            gl = mb.group('g') + ('，本义“%s”' % mb.group('b') if mb.group('b') else '')
            sm = m.group('sm')[1:-1] if m.group('sm') else ''
            lit_r = terms[-1][1] if terms else ''          # 字面意思用派生路线最后一步手写的（两条路的“ / ”、几个意思的“；”都在），它只是占位的（…地、这种性质）才用后缀等式里的
            lit = lit_r if lit_r and not re.match(r'^(…|这种性质$|这件事$)', lit_r) else m.group('res')
            new_first = '【构词逻辑】%s（%s）+ %s%s=“%s”%s' % (base, gl, ps2[1]['surface'], '（%s）' % sm if sm else '', lit, m.group('tail').strip())
            kind = '有后缀' + ('·本义' if mb.group('b') else '')
        else:
            if len(ps) < 2 or re.search(r'[←≈]', G):
                return I, '保留·没有组合公式'
            rg = {re.sub(r'[^a-z]', '', t.lower()): g for t, g in terms}
            gls = [rg.get(re.sub(r'[^a-z]', '', p['surface'].lower())) or h_gloss(H, p['surface']) for p in ps]
            lit2 = terms[-1][1] if terms else ''
            if not all(gls) or not lit2 or lit2 in ('复数',):
                return I, '保留·意思取不全'
            new_first = '【构词逻辑】' + '+ '.join('%s（%s）' % (p['surface'], g) for p, g in zip(ps, gls)) + '=“%s”' % lit2
            m2 = re.search(r'）([，,].+)$', first)
            if m2:
                rest = [m2.group(1).lstrip('，, ')] + rest     # “，跟着 used 的两个意思也分两条：”单独成行
            kind = '无后缀'
    new = '\n'.join([new_first + tail] + rest)
    out = C.compose_I(C.parse_I(new, w))
    O = out.split('\n')
    t2, lit2, r2 = top_eq_parts(C.TAILPOS.sub('', O[0]))
    if r2 or not t2:
        return I, '转换失败'
    seen = False
    for l in O[1:]:
        if C.STEP.match(l):
            seen = True
        if not seen and C.sentence_from_eq(l):
            kind += '·还留等式'
    return out, kind


def split_jinyi(I):
    """组合列 → (去掉【今义】段的组合列, 今义的文字)"""
    L = str(I or '').split('\n')
    keep, jy, cur = [], [], None
    for k, l in enumerate(L):
        m = BLK.match(l) if k else None
        if m:
            cur = m.group(1)
        if cur == '今义':
            jy.append(re.sub(r'^\s*([\u2460-\u2473]?)\s*【今义】\s*', r'\1', l) if m else l)
        else:
            keep.append(l)
    jy = '\n'.join(x for x in jy if x.strip())
    m = re.match(r'^=\s*([^：:（(]+?)\s*(?:（([^（）]*)）)?\s*[：:]\s*(.*)$', jy, re.S)
    if m:                                               # “= neighbour：邻居”开头是等号，Excel 会当成公式：写成“（= neighbour）邻居”
        jy = '（= %s%s）%s' % (m.group(1).strip(), '，' + m.group(2) if m.group(2) else '', m.group(3))
    return '\n'.join(keep), jy


stat, ex = collections.Counter(), collections.defaultdict(list)
newI, mean = {}, {}
for r in range(2, N + 1):
    w = str(ws.cell(r, 5).value or '')
    G, H, I = ws.cell(r, 7).value or '', ws.cell(r, 8).value or '', ws.cell(r, 9).value or ''
    out, kind = convert(w, G, H, I)
    if kind:
        stat[kind] += 1
        if len(ex[kind]) < 6:
            ex[kind].append((r, w, str(I).split('\n')[0][:90], out.split('\n')[0][:120]))
    i2, jy = split_jinyi(out)
    newI[r], mean[r] = i2, jy
    if kind and not kind.startswith(('保留', '认不出', '转换失败')):
        newI[r] = (newI[r], kind)
rt = next((r for r in range(2, N + 1) if ws.cell(r, 5).value == 'towards'), None)
rw = next((r for r in range(2, N + 1) if ws.cell(r, 5).value == 'toward'), None)
if rt and rw and str(mean[rt]).startswith('='):
    mean[rt] = '（= toward，英式常用）' + mean[rw]
print('派生路线', dict(stat))
for k, v in ex.items():
    print('==', k)
    for x in v:
        print('  ', x[0], x[1], '|', x[2], '\n      →', x[3])
print('没有含义的行', sum(1 for r in mean if not mean[r]))
if DRY:
    sys.exit()

# ---------------------------------------------------------------- 写回：在 E 后面插一列 F「含义」
X = wb.create_sheet('__tmp__')
L_ = get_column_letter
for c in range(1, NC + 1):
    d = ws.column_dimensions[L_(c)]
    X.column_dimensions[L_(c if c < 6 else c + 1)].width = d.width
X.column_dimensions['F'].width = 30
plain = next(rr for rr in range(2, 60) if not ws.cell(rr, 17).value and not ws.cell(rr, 10).value)
for r in range(1, N + 1):
    for c in range(1, NC + 1):
        cc = c if c < 6 else c + 1
        v = ws.cell(r, c).value
        if r > 1 and c == 9:
            v = newI[r][0] if isinstance(newI[r], tuple) else newI[r]
        if r > 1 and c == 16 and isinstance(newI[r], tuple):
            v = (v + '；' if v else '') + '组合公式：去掉派生路线，第一行只留组合公式（%s）' % ('母词怎么来的见母词那一行' if newI[r][1].startswith('有后缀') else '前缀、合成词写成 A + B')
        X.cell(r, cc).value = v
        X.cell(r, cc)._style = copy.copy(ws.cell(r, c)._style)
    f = X.cell(r, 6)
    if r == 1:
        f.value = '含义'
        f._style = copy.copy(ws.cell(1, 5)._style)
    else:
        f.value = mean[r] or None
        f._style = copy.copy(ws.cell(plain, 11)._style)
        f.alignment = Alignment(wrap_text=True, vertical='top')
    X.row_dimensions[r].height = ws.row_dimensions[r].height
X.freeze_panes = 'G2'
X.auto_filter.ref = f'A1:R{N}'
pos = wb.sheetnames.index('拆分结果')
wb.remove(ws)
X.title = '拆分结果'
wb._sheets.remove(X)
wb._sheets.insert(pos, X)
wb.active = pos
ws = X
cols = 'FHIJKLNOP'
W = {c: ws.column_dimensions[c].width or 10 for c in cols}
dw = lambda s: sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)
for r in range(2, N + 1):
    best = max(sum(max(1, math.ceil(dw(l) / (W[c] - 1.5))) for l in str(ws[f'{c}{r}'].value or '').split('\n')) for c in cols)
    ws.row_dimensions[r].height = round(max(best, 1) * 17.25, 2)

# ---------------------------------------------------------------- 别的表：列字母跟着往后挪一格
SHIFT = {chr(c): chr(c + 1) for c in range(ord('F'), ord('Q') + 1)}
txtmap = lambda s: re.sub(r'(?<![A-Za-z$])([F-Q])( ?列)', lambda m: SHIFT[m.group(1)] + m.group(2), s)
fmap = lambda s: re.sub(r"(拆分结果!\$?)([F-Q])(\$?\d+:\$?)([F-Q])(\$?\d+)", lambda m: m.group(1) + SHIFT[m.group(2)] + m.group(3) + SHIFT[m.group(4)] + m.group(5), s)
S = wb['说明']
Rk = wb['整表核对记录']
for sh in (S, Rk):
    for row in sh.iter_rows():
        for c in row:
            if isinstance(c.value, str):
                v = fmap(c.value) if c.value.startswith('=') else txtmap(c.value)
                if v != c.value:
                    c.value = v
# 说明 第二节：各列（多出 F 含义，后面的列往后挪；原来第 28 行空着，正好用上）
COLS2 = [('E 单词', '同形异义词各占一行（bore、lie、rose、race、scale、mine）'),
         ('F 含义', '现在的意思：几个意思用“；”隔开，词性写在前面括号里（（v.）（adj.）），例子写在后面括号里（2026-11 从组合列的【今义】挪过来）'),
         ('G 类型', '① 词根词缀 / ② 变体关联 / ③ 合成词 / ④ 不好拆分 / ⑤ 基础词（见下面第四节）'),
         ('H 拆分', 'con + dit(=dic) + ion；④ 写【待处理】，⑤ 写“—”；② 常写 X ← Y 或 X ≈ Y'),
         ('I 各部分解释', None), ('J 组合 → 现在的含义', None), ('K 新·背景', None), ('L 音变 / 字母变化', None),
         ('M 核对结果', None), ('N 核对依据、O 来源链接', None), ('P 原表备注', None), ('Q 本次调整', None), ('R 词根变体处理', None)]
old2 = {str(S.cell(r, 1).value or '').split(' ', 1)[-1]: S.cell(r, 2).value for r in range(16, 28)}
old2['核对依据、来源链接'] = old2.get('核对依据、N 来源链接') or old2.get('核对依据、来源链接')
for k, (a, b) in enumerate(COLS2):
    r = 16 + k
    if b is None:
        name = a.split(' ', 1)[1]
        b = old2.get(name) or old2.get(name.replace('O ', '')) or ''
    if r == 28:
        for c in (1, 2, 3, 4):
            S.cell(28, c)._style = copy.copy(S.cell(27, c)._style)
        if 'B27:C27' in [str(x) for x in S.merged_cells.ranges] and 'B28:C28' not in [str(x) for x in S.merged_cells.ranges]:
            S.merge_cells('B28:C28')
        S.row_dimensions[28].height = S.row_dimensions[27].height
    S.cell(r, 1).value, S.cell(r, 2).value = a, b
# 组合列、写法约定的说明改成新写法
def rep(r, a, b):
    v = S.cell(r, 2).value or ''
    if a not in v:
        print('!! 说明第', r, '行没找到：', a[:30]); return
    S.cell(r, 2).value = v.replace(a, b, 1)
for r in range(16, 29):
    if str(S.cell(r, 1).value).startswith('J 组合'):
        rep(r, '第一行是等式（或派生路线）', '第一行是组合公式（截短、缩写、变体这类没有组合公式的才写派生路线）')
        rep(r, '【今义】【辨析】【趣】【例】', '【辨析】【趣】【例】；现在的意思写在 F 列“含义”')
for r in range(29, 37):
    if str(S.cell(r, 1).value).startswith('组合 → 现在的含义'):
        rep(r, '派生路线写成“派生路线：X（…）→ Y（…）”，最后一步也写上意思；', '不写派生路线（母词是怎么来的，看母词那一行），只有截短、缩写、变体这类写不出组合公式的，才写“派生路线：X（…）→ Y（…）”；')
        rep(r, '每个词都要有【今义】', '每个词都要有含义（F 列）')
last = max(rr for rr in range(76, S.max_row + 1) if S.cell(rr, 1).value)
nconv = sum(1 for v in newI.values() if isinstance(v, tuple))
add = [('组合公式', f'组合列第一行写派生路线、下一行又写后缀等式，讲的是同一件事：{nconv} 行改成只留组合公式“A（…）+ B（…）=“…””（communicator：communicate（传达、交流）+ or（做…的人或东西）=“传达、交流的人”），母词是怎么来的看母词那一行；截短、缩写、变体等写不出组合公式的仍写派生路线。逐行见 Q 列“组合公式：…”。',
        f'=COUNTIF(拆分结果!$Q$2:$Q${N},"*组合公式*")'),
       ('含义列', '单词后面新增 F 列“含义”：组合列里的【今义】全部挪过去，组合列只讲构词逻辑和意思怎么变。', f'=COUNTA(拆分结果!$F$2:$F${N})')]
for k, (a, b, d) in enumerate(add, start=1):
    rr = last + k
    for c in (1, 2, 3, 4):
        S.cell(rr, c)._style = copy.copy(S.cell(last, c)._style)
    S.cell(rr, 1).value, S.cell(rr, 2).value, S.cell(rr, 4).value = a, b, d
    S.merge_cells(f'B{rr}:C{rr}')
    S.row_dimensions[rr].height = S.row_dimensions[last].height
# 整表核对记录
n0 = sum(1 for x in Rk.iter_rows(min_row=2, values_only=True) if x[0] is not None)
body = copy.copy(Rk.cell(2, 4)._style)
kept = [str(ws.cell(r, 5).value) for r in range(2, N + 1) if str(ws.cell(r, 10).value or '').startswith('【构词逻辑】派生路线')]
row_of = {str(ws.cell(r, 5).value): r for r in range(2, N + 1)}
LOG = [('已修正', None, '派生路线', f'组合列第一行写派生路线，下一行的后缀等式讲的是同一件事（communicator：派生路线 communicate → communicator，下面又是 communicate + -or =“传达、交流的人”）',
        f'{nconv} 行第一行改成只留组合公式，后缀等式不再单写；没有后缀的前缀词、合成词也写成 A + B；逐行见 Q 列“组合公式：…”'),
       ('特殊（未改）', None, '派生路线（保留）', f'{len(kept)} 行写不出组合公式：截短、缩写、变体（app、exam、memoir、lone……）、-men 复数（freshmen、postmen……）、从拉丁语形式变来的（defence）、倒推出来的（statistic）',
        '派生路线本身就是在讲这个词怎么来的，保留：' + '、'.join(kept[:40])),
       ('已修正', None, '今义 → 含义列', '组合列最后的【今义】讲的是现在的意思，和构词逻辑、意思演变混在一格里',
        '单词后面新增 F 列“含义”，9293 个词的【今义】都挪过去（组合列和它后面的列都往右挪一列：组合 → 现在的含义现在是 J 列，本次调整是 Q 列）'),
       ('已修正', row_of.get('preschooler'), 'preschooler', 'preschool 是名词，词性变化原写“动词 → 名词（人或东西）”', '改成“名词 → 名词（人）”，组合公式写成 preschool + er')]
for k, (cat, rr, w, what, how) in enumerate(LOG):
    i = n0 + k + 2
    vals = [n0 + k + 1, cat, f'=HYPERLINK("#\'拆分结果\'!E{rr}","第 {rr} 行")' if rr else '—', w, what, how]
    for c, v in enumerate(vals, 1):
        cell = Rk.cell(i, c); cell.value = v; cell._style = copy.copy(body)
        cell.alignment = Alignment(wrap_text=True, vertical='top')
    if rr:
        Rk.cell(i, 3).font = Font(name='微软雅黑', size=10, color='0563C1', underline='single')
    Rk.cell(i, 2).fill = PatternFill('solid', start_color='E2EFDA' if cat == '已修正' else 'FFF2CC')
    Rk.row_dimensions[i].height = 17.25 * max(1, math.ceil(max(len(what), len(how)) / 38))
Rk.auto_filter.ref = f'A1:F{Rk.max_row}'
wb.save(OUT)
print('saved', OUT, '改', nconv, '行；保留派生路线', len(kept))

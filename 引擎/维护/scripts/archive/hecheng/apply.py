"""合成规律轮：把“　合成规律：”“　写法：”两种行写进组合列（N），散在别处讲写法的旧说明并进写法那一行，U 列记录，
新增「合成规律一览」，「整表核对记录」记汇总，「说明」补这一轮。用法：python3 apply.py <源.xlsx> <新.xlsx>"""
import sys, json, re, copy, math
sys.path.insert(0, '/home/claude/work/hc')
sys.path.insert(0, '/home/claude/work/orig_maint/etymology-table/scripts')
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import columns as COL
import cols as C
import consol
from pass2 import apply_edits, EDITS
from gen import comp_lines, CATS
from spell import spell_line
from catalog import RULES, TEXT, KIND, BY_ID

SRC, OUT = sys.argv[1], sys.argv[2]
T = json.load(open('/home/claude/work/hc/feats.json'))

SHORT = {'H01': '主体在后', 'H02': '宾语提前', 'H03': '用什么、在哪儿提前', 'H04': '名词 + 过去分词', 'H05': '副词提前', 'H06': '名词 + 形容词',
         'H07': '短语当一个词', 'H08': '动词短语变名词', 'H09': '小词在前', 'H10': '介词短语连成词', 'H11': '像一句命令', 'H12': '有…的',
         'H13': '数词 + 名词用单数', 'H14': '并列', 'H15': '近义叠用、加类名', 'H16': '有这个特点的人或东西', 'H17': '…+ 动词 = 动词',
         'H18': '主语 + 动词', 'H19': '两位数', 'H20': '分数', 'H21': '十几', 'H22': 'some / any / every / no', 'H23': '疑问词 + ever',
         'H24': '…self', 'H25': '小词合成小词', 'H26': '老合成词', 'H27': '外语里合成的', 'H28': '拼缀词', 'H29': 'man → men',
         'H30': '中间的 s', 'H31': '复数加在主体上', 'H32': '连写后意思固定', 'H33': '词尾加在短语上', 'H34': 'self 在前',
         'W01': '用熟了连写', 'W02': '新词加连字符', 'W03': '形容词加连字符', 'W04': '动词短语变的名词', 'W05': '数字', 'W06': '字母、缩写、数字',
         'W07': 'self 打头', 'W08': '接 like、free 这类词', 'W09': '并列', 'W10': '短语连成一个词', 'W11': '连写、分开写意思不同',
         'W12': '掉字母、重字母不删', 'W13': '前缀的连字符', 'W14': '重复的词', 'W15': '撇号', 'W16': '名词常分开写', 'W17': '专有名词', 'W18': 'ly 副词不加'}
TEXT2ID = {r[2]: r[0] for r in RULES}


def rule_ids(lines):
    out = []
    for l in lines:
        m = re.match(r'^\s*(合成规律|写法)[：:]\s*(.*)$', l)
        if m:
            txt = m.group(2).split('（', 1)[0]
            out.append(TEXT2ID[txt])
    return out


def is_eq(l):
    return bool(COL.sentence_from_eq(l)) and not COL.STEP.match(l) and '+ -' in l


wb = load_workbook(SRC)
ws = wb['拆分结果']
NCOL, PCOL, UCOL = C.COMBO, C.SOUND, C.ADJ
assert ws.cell(1, NCOL).value == '组合 → 现在的含义' and ws.cell(1, PCOL).value == '音变 / 字母变化' and ws.cell(1, UCOL).value == '本次调整'

W = {}
for d in ws.column_dimensions.values():
    for i in range(d.min or 0, (d.max or 0) + 1):
        if i:
            W[get_column_letter(i)] = d.width
W = {c: W.get(c) or 10 for c in C.TEXT_COLS}
dw = lambda s: sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)


def fit(r):
    best = max(sum(max(1, math.ceil(dw(l) / (W[c] - 1.5))) for l in str(ws[f'{c}{r}'].value or '').split('\n')) for c in C.TEXT_COLS)
    need = min(round(best * 17.25, 2), 409)
    if (ws.row_dimensions[r].height or 0) < need:
        ws.row_dimensions[r].height = need


stats = {'rows': 0, 'comp': 0, 'spell': 0, 'moved_rows': 0, 'moved_items': 0, 'P_changed': 0, 'N_old_removed': 0}
use = {r[0]: [] for r in RULES}
changes = []
for t in T:
    r, w = t['row'], t['w']
    assert str(ws.cell(r, 5).value) == w, (r, w)
    N0 = ws.cell(r, NCOL).value
    P0 = ws.cell(r, PCOL).value
    assert str(N0 or '') == str(t['N'] or '')
    first, keep, newP, took, notes = consol.consolidate(N0, P0, w)
    if w in EDITS:
        keep, newP = apply_edits(w, keep, newP)
        notes = notes + ['第二遍：%d 处' % len(EDITS[w])]
    comp = comp_lines(t)
    sid, sline = spell_line(t, took)
    k = 0
    while k < len(keep) and is_eq(keep[k]):
        k += 1
    newN = '\n'.join([first] + keep[:k] + comp + [sline] + keep[k:])
    d = COL.parse_I(newN, w)
    assert COL.compose_I(d) == newN, ('round trip', w, newN)
    ids = rule_ids(comp + [sline])
    for i in dict.fromkeys(ids):
        use[i].append(w)
    ws.cell(r, NCOL).value = newN
    pchg = (str(newP or '') != str(P0 or ''))
    if pchg:
        ws.cell(r, PCOL).value = newP
        stats['P_changed'] += 1
    hc = [i for i in ids if KIND[i] == '合成规律']
    note = '合成规律：' + '、'.join(['补合成规律（%s）' % '、'.join(SHORT[i] for i in hc)] if hc else []) + \
           ('、' if hc else '') + '补写法（%s）' % SHORT[sid]
    if notes:
        note += '；讲连写、连字符的旧说明 %d 处并进写法那一行' % len(notes)
        stats['moved_rows'] += 1
        stats['moved_items'] += len(notes)
    u0 = ws.cell(r, UCOL).value
    ws.cell(r, UCOL).value = (str(u0).rstrip('；') + '；' + note) if u0 else note
    fit(r)
    stats['rows'] += 1
    stats['comp'] += len(comp)
    stats['spell'] += 1
    changes.append({'row': r, 'word': w, 'rules': ids, 'notes': notes})

# ---------------------------------------------------------------- 合成规律一览
ref = wb['用词规律一览']
H = wb.create_sheet('合成规律一览', index=wb.sheetnames.index('用词规律一览') + 1)
heads = ['序', '编号', '类', '规律（组合列里照这句话写）', '为什么会这样', '例子（总表里的词）', '表里用到的词数', '用到这条规律的词（前 40 个）']
for c, h in enumerate(heads, 1):
    H.cell(1, c).value = h
    H.cell(1, c)._style = copy.copy(ref.cell(1, 1)._style)
for i, (rid, kind, text, why, ex) in enumerate(RULES, 1):
    vals = [i, rid, kind, text, why, ex, len(use[rid]), '、'.join(use[rid][:40])]
    for c, v in enumerate(vals, 1):
        H.cell(i + 1, c).value = v
        H.cell(i + 1, c)._style = copy.copy(ref.cell(2, min(c, 6))._style)
for col, wd in zip('ABCDEFGH', (5, 7, 9, 40, 64, 40, 10, 64)):
    H.column_dimensions[col].width = wd
for r in range(2, len(RULES) + 2):
    best = max(math.ceil(dw(str(H.cell(r, c).value or '')) / (wd - 1.5)) for c, wd in zip(range(1, 9), (5, 7, 9, 40, 64, 40, 10, 64)))
    H.row_dimensions[r].height = min(409, round(max(1, best) * 17.25, 2))
H.freeze_panes = 'A2'
H.auto_filter.ref = 'A1:H%d' % (len(RULES) + 1)

# ---------------------------------------------------------------- 整表核对记录：汇总
R = wb['整表核对记录']
last = R.max_row
n0 = int(R.cell(last, 1).value)
ok_row = next(rr for rr in range(last, 1, -1) if R.cell(rr, 2).value == '已修正')
sp_row = next(rr for rr in range(last, 1, -1) if R.cell(rr, 2).value == '特殊（未改）')
n_comp_words = sum(1 for t in T if t['type'] == '③ 合成词')
n_pfx = len(T) - n_comp_words
logs = [
    ('已修正', '合成规律',
     '合成词（%d 个）组合列只写了公式和意思，没讲两个词为什么这样排（paper-cutting 为什么不是 cutting-paper）、合起来是什么关系；带连字符的词（%d 个，另有 non-verbal、co-writer 这类前缀词 %d 个）没讲连字符起什么作用、为什么有的连写有的不加'
     % (n_comp_words, sum(1 for t in T if t['type'] == '③ 合成词' and '-' in t['w']), n_pfx),
     '组合列第一行（有后缀等式的接在等式后面）下面加“　合成规律：规律（本词：短语 → 本词；同 例词）”（合成词每个一到三行：顺序、关系，以及 man → men、复数加在主体上、连写后意思固定这类特殊规律）和“　写法：规律（本词的例子、别的写法、历史）”（每个一行），'
     '规律的说法统一照「合成规律一览」（34 条合成规律、18 条写法）；共 %d 行' % stats['rows']),
    ('已修正', '写法说明归拢',
     '讲连写、连字符、分开写的话散在组合列【语法】【辨析】【提醒】、步骤末尾的括号、“（…见【辨析】）”指路行和音变列里，同一件事讲两三遍，学生不知道去哪儿看',
     '并进各自的“写法”那一行（例子、别的写法、年代都照原话带过去），原处删掉：%d 行共 %d 处；一行里还有别的内容的（145 行，如 make-up 的【辨析】、already 的【辨析】），只删讲写法的那半句，别的照留'
     % (stats['moved_rows'], stats['moved_items'])),
    ('特殊（未改）', '合成规律（说法不一的）',
     'charcoal（char 是“木炭”还是“变成”）、ketchup（闽南话来源的细节）、gallop（法兰克语短语“很可能”）、standard（“站 + 牢”是主流说法）这几个词的合成规律照词典写“说法不一 / 很可能”，没写成定论；giant-king、giant-prince 原【语法】说“前一个名词修饰后一个”，按主体在后讲（巨人一样的国王），不当并列',
     '照来源写明不确定，不改核对结果'),
]
for i, (cat, word, found, done) in enumerate(logs, 1):
    rr = last + i
    src_row = ok_row if cat == '已修正' else sp_row
    for c, v in enumerate([str(n0 + i), cat, '—', word, found, done], 1):
        R.cell(rr, c).value = v
        R.cell(rr, c)._style = copy.copy(R.cell(src_row, c)._style)
    R.row_dimensions[rr].height = R.row_dimensions[src_row].height
if R.auto_filter.ref:
    R.auto_filter.ref = 'A1:F%d' % (last + len(logs))

# ---------------------------------------------------------------- 说明
S = wb['说明']
S['A3'] = '一、五张工作表'
sheet_rows = [
    ('拆分结果', '主表，一行一个词（批次、组号、拆分、前缀、词根、单词部分、后缀、组合 → 现在的含义、背景、核对……）。构词动画视频技能只读这一张。'),
    ('用词规律一览', '28 条英语用词规律（一词多义是怎么来的）：为什么会这样、例子、表里用到这条规律的词。'),
    ('合成规律一览', '34 条合成规律（合成词里两个词谁在前、谁在后，合起来是什么关系）和 18 条写法（为什么有的连写、有的加连字符、有的分开写）：规律那句话、为什么、例子、表里用到的词。组合列里的“　合成规律：”“　写法：”照这里的说法写。'),
    ('整表核对记录', '每一轮找到并修正的问题、只记录不改的特殊情况；“所在行”可以点击跳到「拆分结果」。逐行的改动都写在「拆分结果」U 列。'),
    ('说明', '本页：各列的内容、写法约定、统计、各轮调整。'),
]
for i, (a, b) in enumerate(sheet_rows):
    rr = 5 + i
    S.cell(rr, 1).value = a
    S.cell(rr, 2).value = b
    if rr == 9:
        for c in range(1, 5):
            S.cell(9, c)._style = copy.copy(S.cell(8, c)._style)
        S.merge_cells('B9:D9')
        S.row_dimensions[9].height = S.row_dimensions[8].height
assert S['A21'].value.startswith('N 组合')
S['B21'] = (str(S['B21'].value).rstrip('。') + '。合成词、带连字符的词：第一行（有后缀等式的接在等式后面）下面接“　合成规律：规律（本词：短语 → 本词；同 例词）”'
            '（谁在前、谁在后、合起来是什么关系，一行一条）和“　写法：规律（例子、别的写法、历史）”（为什么连写、加连字符或分开写），说法照「合成规律一览」。')
assert S['A27'].value.startswith('U 本次调整')
S['B27'] = str(S['B27'].value).rstrip('。') + '“合成规律：…”'
assert S['A34'].value.startswith('组合 → 现在的含义')
S['B34'] = (str(S['B34'].value).rstrip('。') + '。合成词、带连字符的词在第一行下面写“　合成规律：”“　写法：”两种行：规律那句话照「合成规律一览」一字不改（视频照这句话念、照它认是哪一条），括号里先写本词'
            '（cut paper 剪纸 → paper-cutting），再写“同 例词”；讲连写、连字符的话只写在“写法”那一行，不再写进【语法】【辨析】或音变列。')
last7 = S.max_row
assert str(S.cell(last7, 1).value) == '动词变化形式', S.cell(last7, 1).value
rr = last7 + 1
for c in range(1, 5):
    S.cell(rr, c)._style = copy.copy(S.cell(last7, c)._style)
S.merge_cells('B%d:C%d' % (rr, rr))
S.cell(rr, 1).value = '合成规律'
S.cell(rr, 2).value = ('合成词 %d 个、带连字符的前缀词 %d 个：组合列第一行下面加“　合成规律：”（两个词谁在前、谁在后、是什么关系：paper-cutting 是 cut paper 宾语挪到前面，cutting-paper 就成了“剪着用的纸”；'
                      'handmade 是 made by hand 名词挪前、介词省掉）和“　写法：”（为什么连写、加连字符或分开写：用熟了的连写，新组合、放在名词前当形容词、动词短语变的名词加连字符……）；'
                      '新增「合成规律一览」（34 条合成规律、18 条写法）。原来散在【语法】【辨析】、步骤括号、音变列里讲写法的说明（%d 行）并进写法那一行。'
                      % (n_comp_words, n_pfx, stats['moved_rows']))
S.cell(rr, 4).value = '=COUNTIF(拆分结果!$U$2:$U$9294,"*合成规律：*")'
S.row_dimensions[rr].height = S.row_dimensions[last7].height

wb.save(OUT)
json.dump({'stats': stats, 'use': {k: len(v) for k, v in use.items()}, 'changes': changes}, open('/home/claude/work/hc/apply_log.json', 'w'), ensure_ascii=False)
print(json.dumps(stats, ensure_ascii=False))
print({k: len(v) for k, v in use.items()})

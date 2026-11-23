import sys, re, copy, json, math
sys.path.insert(0, '/home/claude/work'); sys.path.insert(0, '/home/claude/work/new_maint/etymology-table/scripts')
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import cols as C, columns as COL
from ym_data import US, UK, SPECIAL, HY
SRC, OUT = sys.argv[1], sys.argv[2]
US.pop('fiber', None); US.pop('color', None)

def note_for(w):
    if w in SPECIAL: return SPECIAL[w], None
    if w in HY: return HY[w], None
    if w in US: return '（美式拼写，英式写作 %s）' % US[w], US[w]
    if w in UK: return '（英式拼写，美式写作 %s）' % UK[w], UK[w]
    return None, None

def other_forms(w):
    out = set()
    for d in (US, UK):
        if w in d: out.add(d[w].lower())
    for m in re.finditer(r'(?:写作|写成|连写成|分开写成|也写作|也常写作|传统写作)\s*([A-Za-z][A-Za-z\- ]*[A-Za-z])', SPECIAL.get(w, '') + HY.get(w, '')):
        out.add(m.group(1).lower())
    return out

def clean_F(w, F):
    oth = other_forms(w)
    s = F
    s = re.sub(r'（[^（）]*(英式|美式)拼写[^（）]*）', '', s)
    s = re.sub(r'（(英式|美式)(也)?拼作 ([A-Za-z][A-Za-z\- ]*)）', lambda m: '' if m.group(3).lower() in oth else m.group(0), s)
    s = re.sub(r'（(英式|美式)拼写，(意思)?同 [A-Za-z\- ]+）', '', s)
    def drop_eq(m):
        return '' if m.group(2).strip().lower() in oth else m.group(0)
    s = re.sub(r'（(= |同 |美式写作 |英式写作 |美式说 |也写 |也写作 )([A-Za-z][A-Za-z\- ]*)）', drop_eq, s)
    s = re.sub(r'（= ([A-Za-z][A-Za-z\- ]*)，(英式|美式)拼写）', lambda m: '' if m.group(1).lower() in oth else m.group(0), s)
    if w not in SPECIAL:
        s = re.sub(r'^((?:n|v|adj|adv)\. )（(英|美|英式|美式)）', r'\1', s)
    return s

wb = load_workbook(SRC)
ws = wb['拆分结果']
log, nF, nN, nConv = [], 0, 0, 0
SPELL_BODY = {
 'makeover': '英美词典都连写成 makeover（牛津、韦氏都这样写；make-over 只是少见的另一种写法），不分英式美式——这和 make-up / makeup 不一样（英式多写 make-up，美式多连写成 makeup）；动词短语分开写：make over the room',
 'life-saving': 'life-saving surgery 救命的手术；英式多写 life-saving，美式多连写成 lifesaving',
 'lifesaving': '美式多连写成 lifesaving，英式多写 life-saving',
 'second-hand': 'a second-hand car；英式多写 second-hand，美式多连写成 secondhand',
 'secondhand': '美式多连写成 secondhand，英式多写 second-hand',
 'clean-up': '英式多写 clean-up，美式多连写成 cleanup；动词短语分开写：clean up the room',
 'cleanup': '美式多连写成 cleanup，英式多写 clean-up；作动词必须分开写：clean up the room',
 'check-up': '英式多写 check-up，美式多连写成 checkup；动词短语分开写：check up on sb',
 'check-ups': '英式多写 check-ups，美式多连写成 checkups',
 'takeoff': '美式多连写成 takeoff，英式多写 take-off；动词：The plane will take off soon.；读音：ˈtakeoff（名词）↔ take ˈoff（动词）',
 'setup': '美式多连写成 setup，英式多写 set-up；动词短语要分开写：set up a tent（搭帐篷）、set up a company（创办公司）；名词 ˈsetup 重音在前',
 'runoff': '美式多连写成 runoff，英式多写 run-off；动词短语分开写：The water ran off the roof.',
 'easy-going': 'an easy-going boss 好说话的老板；英式多写 easy-going，美式多连写成 easygoing',
 'quarterfinal': '美式多连写成 quarterfinal，英式多写 quarter-final（同 semifinal / semi-final）',
 'pre-order': 'pre- 一般连写（preview）；英式多写 pre-order，美式多连写成 preorder',
 'pre-ordered': 'pre- 一般连写（preview）；英式多写 pre-ordered，美式多连写成 preordered',
 'hard-working': 'a hard-working student；英式多写 hard-working，美式多连写成 hardworking',
 'hardworking': '美式多连写成 hardworking，英式多写 hard-working',
}
for r in range(2, ws.max_row + 1):
    w = str(ws.cell(r, C.WORD).value or '')
    F = str(ws.cell(r, C.MEAN).value or '')
    newF = F
    note, _ = note_for(w)
    tag = []
    if note:
        L = clean_F(w, F).split('\n')
        L[0] = L[0].rstrip() + note
        newF = '\n'.join(L)
        tag.append('含义列标出%s写法，补上另一边的写法' % ('英式还是美式' ))
    else:
        conv = re.sub(r'（英式拼写，(?:意思)?同 ([A-Za-z\- ]+)）', r'（英式拼写，美式写作 \1）', F)
        if conv != F:
            newF = conv; nConv += 1
            tag.append('含义列“英式拼写，同 X”改成“英式拼写，美式写作 X”')
    if newF != F:
        ws.cell(r, C.MEAN).value = newF; nF += 1
    if w in SPELL_BODY:
        N = str(ws.cell(r, C.COMBO).value)
        L = N.split('\n')
        k = [i for i, l in enumerate(L) if l.startswith('　写法：')]
        assert len(k) == 1, w
        head = L[k[0]].split('（', 1)[0]
        L[k[0]] = head + '（' + SPELL_BODY[w] + '）'
        newN = '\n'.join(L)
        assert COL.compose_I(COL.parse_I(newN, w)) == newN
        ws.cell(r, C.COMBO).value = newN; nN += 1
        tag.append('写法那一行写明英式、美式各怎么写')
    if tag:
        u0 = ws.cell(r, C.ADJ).value
        note_u = '英美写法：' + '；'.join(tag)
        ws.cell(r, C.ADJ).value = (str(u0).rstrip('；') + '；' + note_u) if u0 else note_u
        log.append((r, w, F, newF))
print('F changed', nF, '(converted old-format', nConv, ') N changed', nN)

R = wb['整表核对记录']
last = R.max_row; n0 = int(R.cell(last, 1).value)
ok_row = next(rr for rr in range(last, 1, -1) if R.cell(rr, 2).value == '已修正')
sp_row = next(rr for rr in range(last, 1, -1) if R.cell(rr, 2).value == '特殊（未改）')
nmark = nF - nConv
logs = [
 ('已修正', '英美写法', '用户问 makeover 为什么不加连字符、是不是美式写法：查牛津（英）、韦氏（美）都写 makeover，不分英美；make-up / makeup 才是英式、美式两种写法。用 breame（英美拼写对照表）把全表单词和合成词里的每一段对了一遍，加上连字符、连写、分开写英美不同的词，含义列很多没标是哪一边的写法，标了的格式也不统一（“（美式拼写）”“（= neighbour）”“（同 nonverbal）”“（英式拼写，同 X）”），多数没给另一边的写法',
  '含义列第一行末尾统一写“（英式拼写，美式写作 X）/（美式拼写，英式写作 X）”（字母不同：colour / color、metre / meter、defence / defense……）或“（英式写法，美式多连写成 X）/（美式写法，英式写作 X）”（连字符、连写不同：make-up / makeup、take-off / takeoff、set-up / setup、non-verbal / nonverbal……），原来零散的标注去掉；%d 行。另有 %d 行原来写“（英式拼写，同 X）”的统一改成“（英式拼写，美式写作 X）”。写法英美不同的合成词，组合列写法那一行也写明两边各怎么写（%d 行，makeover 写明英美都连写）' % (nmark, nConv, nN)),
 ('特殊（未改）', '英美写法（不标的）', '对照表列出、但不当英美写法标的：filter / philtre、tire / tyre、ton / tonne 是不同的词；gram / gramme、kilogram / kilogramme、connection / connexion、medieval / mediaeval 是旧写法；glamour、cancellation、archaeology、aesthetic、dialogue、monologue、prologue、likeable、woolly 英美都常用前一种；disc / disk、draft / draught、install / instal 按意思分工，含义里已经讲了；-ize / -ise：-ize 英式（牛津拼法）也用，所以 -ize 的词不标“美式”，-ise 的词标“英式拼写，美式写作 -ize”',
  '照旧，不标'),
]
for i, (cat, word, found, done) in enumerate(logs, 1):
    rr = last + i; src_row = ok_row if cat == '已修正' else sp_row
    for c, v in enumerate([str(n0 + i), cat, '—', word, found, done], 1):
        R.cell(rr, c).value = v; R.cell(rr, c)._style = copy.copy(R.cell(src_row, c)._style)
    R.row_dimensions[rr].height = R.row_dimensions[src_row].height
if R.auto_filter.ref: R.auto_filter.ref = 'A1:F%d' % (last + len(logs))

S = wb['说明']
assert S['A36'].value.startswith('含义')
S['B36'] = str(S['B36'].value).rstrip('。') + '。英式、美式写法不同的词，含义第一行末尾写“（英式拼写，美式写作 X）/（美式拼写，英式写作 X）”（字母不同）或“（英式写法，美式多连写成 X）/（美式写法，英式写作 X）”（连字符、连写不同），一个词只写一处。'
last7 = S.max_row; assert S.cell(last7, 1).value == '合成规律'
rr = last7 + 1
for c in range(1, 5): S.cell(rr, c)._style = copy.copy(S.cell(last7, c)._style)
S.merge_cells('B%d:C%d' % (rr, rr))
S.cell(rr, 1).value = '英美写法'
S.cell(rr, 2).value = ('英式、美式写法不同的词（%d 个），含义第一行末尾统一标出是哪一边的写法、另一边怎么写：colour（英式拼写，美式写作 color）、makeup（美式写法，英式多写作 make-up）、non-verbal（英式写法，美式多连写成 nonverbal）；'
                      '原来的“（英式拼写，同 X）”改成“（英式拼写，美式写作 X）”；写法英美不同的合成词，组合列写法那一行也写明（makeover 英美都连写，不分英美）。' % nmark)
S.cell(rr, 4).value = '=COUNTIF(拆分结果!$U$2:$U$9294,"*英美写法*")'
S.row_dimensions[rr].height = S.row_dimensions[last7].height
wb.save(OUT)
json.dump(log, open('/home/claude/work/ym_log.json', 'w'), ensure_ascii=False)

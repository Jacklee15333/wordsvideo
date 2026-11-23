"""词根列加连字符、28 个构词成分算词根、标错列的词缀挪列：写回总表"""
import pickle, copy, math, sys, collections
from openpyxl import load_workbook
from openpyxl.styles import Alignment, PatternFill
sys.path.insert(0, '/home/claude/skills_new/maintain/etymology-table/scripts')
SRC, OUT = '/home/claude/out/new3.xlsx', sys.argv[1]
out = pickle.load(open('/home/claude/work4/new_cells.pkl', 'rb'))
wb = load_workbook(SRC)
ws = wb['拆分结果']
assert ws.cell(1, 10).value == '前缀' and ws.max_column == 21
st = collections.Counter()
for r in range(2, ws.max_row + 1):
    p, ro, s, notes = out[r]
    for c, v in zip((10, 11, 12), (p, ro, s)):
        if str(ws.cell(r, c).value or '') != v:
            ws.cell(r, c).value = v; st['cells'] += 1
    if notes:
        q = ws.cell(r, 20)
        q.value = (str(q.value) + '；' if q.value else '') + '词根连字符：' + '；'.join(notes)
        st['rows'] += 1
S = wb['说明']; Rk = wb['整表核对记录']
S['B20'] = ('以前的“各部分解释”拆成三列，一列讲一种部分，每部分一行“标签：解释”：J 前缀（re-、un-）；K 词根（不能单独用的词根在接别的部分的那一边加“-”：开头的 bio-、'
            '中间的 -ped-、末尾的 -logue；母词、合成词里的词照原样写：popular、shoe、maker）；L 后缀（-ion、-er、-logy，中间的成分 -it-、-at- 也写在这里）。没有的写“-”。'
            '“为什么用 -er 不用 -or”写在它讲的那一列；讲整个词来历、拼写的说明写在词根列。这三列只讲各部分，怎么组合、意思怎么来的写在 M 列')
S['B31'] = ('三列各讲一种部分：每部分一行“标签：解释”，标签和拆分对得上：前缀写 re-（J 列），后缀写 -ion（L 列），词根写在 K 列：不能单独用的词根（拉丁语、希腊语的词根，'
            'bio、geo、photo 这类构词成分，连接元音、双写的字母）在接别的部分的那一边加“-”（bio-、-ped-、-logue、-i-），能单独用的英语单词（母词、合成词里的词）不加。'
            '只讲这一部分本身，不写“在这里”“意思怎么变”“用词规律”（写在组合列）。“为什么用 -er 不用 -or”跟着它讲的前缀或后缀；讲整个词来历的说明放词根列；一列没有内容写“-”。')
S.row_dimensions[20].height = 90; S.row_dimensions[31].height = 90
for c in 'ABCD':
    S[f'{c}104']._style = copy.copy(S[f'{c}103']._style)
S['A104'] = '词根加连字符'
S['B104'] = ('词根列里不能单独用的词根加“-”（1556 个：-ped-、-spect、bio-、-i-），母词、合成词里的英语单词不加；'
             'bio、geo、photo、psycho 等 17 个构词成分，dialogue、monologue 的 -logue、multiple 的 -ple 等 8 个，unify、twice、trio 的 uni-、twi-、tri- 改算词根，'
             '挪到词根列；写在词根列的前缀、后缀 9 个（debt 的 de-、season 的 -on……）挪回前缀、后缀列。逐行见 T 列“词根连字符：…”。')
S.merge_cells('B104:C104')
S['D104'] = '=COUNTIF(拆分结果!$T$2:$T$9294,"*词根连字符*")'
S.row_dimensions[104].height = 75
n0 = sum(1 for x in Rk.iter_rows(min_row=2, values_only=True) if x[0] is not None)
body = copy.copy(Rk.cell(2, 4)._style)
LOG = [('已修正', '词根列', '词根不是能单独用的单词，应该和前缀、后缀一样加连字符（用户提出）',
        '不能单独用的词根在接别的部分的那一边加“-”：开头的写 X-（vis-、bio-），中间的写 -X-（-ped-、-sati-、连接元音 -i-、双写的 -t-），末尾的写 -X（-spect、-port）；'
        '能单独用的英语单词（母词 popular、合成词里的 shoe、maker、专有名词 Hamburg）不加；英语单词在这里当拉丁、希腊词根用的（transport 的 port、relate 的 late、remember 的 member）加。'
        '共加了 1556 处，拿不准的约 600 处逐条看过。'),
       ('已修正', '构词成分', 'biology、geography、photograph 等 28 个词，原表把 bio-、-logy 标成前缀、后缀，词根列是“-”（第 100 条）',
        '用户定下按词根算：bio、geo、photo、hydro、psycho、thermo、astro、electro、archaeo、aut、rock、Portugu（17 个词）从前缀列挪到词根列；'
        'dialogue、monologue、prologue、catalogue、apology 的 -logue / -logy，multiple、triple 的 -ple，trillion 的 -llion（8 个）从后缀列挪到词根列（前面的 dia-、mono-、multi-、tri- 仍是前缀）；'
        'unify、twice、trio 的 uni-、twi-、tri-（3 个）挪到词根列（后面的 -fy、-ce、-o 只是词尾）。'),
       ('已修正', '前缀、词根、后缀', '有 9 个前缀、后缀没写连字符，被分到了词根列',
        '挪回去、补上连字符：debt 的 de-、beside 的 be-、enthusiasm 的 en-、reinforce 的 in-、neutral 的 ne-、pierce 的 pier-（前缀）；season 的 -on、zodiac 的 -di、debt 的 -t（后缀）')]
for k, (cat, w, what, how) in enumerate(LOG):
    i = n0 + k + 2
    for c, v in enumerate([n0 + k + 1, cat, '—', w, what, how], 1):
        cell = Rk.cell(i, c); cell.value = v; cell._style = copy.copy(body)
        cell.alignment = Alignment(wrap_text=True, vertical='top')
    Rk.cell(i, 2).fill = PatternFill('solid', start_color='E2EFDA')
    Rk.row_dimensions[i].height = 17.25 * max(1, math.ceil(max(len(what), len(how)) / 38))
# 第 100 条（28 个词词根列是“-”）已经按用户的意见改了：处理一栏补一句
for r in range(2, Rk.max_row + 1):
    if Rk.cell(r, 4).value == '只有前缀、后缀的词':
        Rk.cell(r, 6).value = str(Rk.cell(r, 6).value) + '。后来用户定下按词根算，已挪到词根列（见第 %d 条）' % (n0 + 2)
Rk.auto_filter.ref = f'A1:F{Rk.max_row}'
wb.save(OUT)
print(dict(st))

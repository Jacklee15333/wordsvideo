# -*- coding: utf-8 -*-
"""2026-11 拉丁语动词变化轮的改动清单（用户逐族过目、要恢复都靠它）。
  python3 report.py <改前.xlsx> <改后.xlsx> <清单.xlsx>
两版的行要一一对应。四张表：说明、动词变化（一族一行：三个样子、规律、这一族的分工、写进的行数和词）、词根列（改前改后）、没收的。"""
import sys, os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
import linetools as LT, dongbian as DB
import dongbian_data as DD, shenfen_data as FD

FONT = Font(name='微软雅黑', size=10); HEAD = Font(name='微软雅黑', size=10, bold=True, color='FFFFFF'); FILL = PatternFill('solid', fgColor='305496')
WRAP = Alignment(wrap_text=True, vertical='top')


def sheet(wb, title, head, rows, widths, freeze='A2'):
    ws = wb.create_sheet(title)
    ws.append(head)
    for r in rows: ws.append(['' if v is None else v for v in r])
    for j, w in enumerate(widths): ws.column_dimensions[get_column_letter(j + 1)].width = w
    for c in ws[1]: c.font = HEAD; c.fill = FILL; c.alignment = Alignment(vertical='center', wrap_text=True)
    for row in ws.iter_rows(min_row=2):
        for c in row: c.font = FONT; c.alignment = WRAP
    ws.freeze_panes = freeze
    if rows: ws.auto_filter.ref = 'A1:%s%d' % (get_column_letter(len(head)), len(rows) + 1)
    return ws


def kind_of(v):
    """这一族的过去式是哪一种变法（给用户按类看）"""
    r = v['rule']
    if not v.get('perf'): return '只有被动的样子（没有单独的过去式）'
    if '借来' in r: return '借别的动词（最不规则）'
    if DD.ARE in r: return '-are 这一类：加 -avi、-atus（最整齐）'
    if DD.REDUP in r: return '重复开头的音'
    if '只换元音' in r: return '只换元音（a → e）'
    if '念长' in r: return '只把元音念长'
    if DD.SAME in r: return '不变样（词根直接加词尾）'
    if re.search(r'加 s|再加 s', r): return '加 s（和前面的辅音合写成 x 等）'
    if re.search(r'加 u', r): return '加 u'
    if re.search(r'加 i?v', r): return '加 v'
    return '其他'


def main(a, b, dst):
    ha, Ca, da = LT.load_table(a)
    hb, Cb, db = LT.load_table(b)
    assert len(da) == len(db), '两版行数不一样'
    rows_root = []; fam_rows = collections.defaultdict(list); other = 0
    for i, (x, y) in enumerate(zip(da, db)):
        assert x[Ca['word']] == y[Cb['word']], '第 %d 行单词对不上' % (i + 2)
        for h in ha:
            if h == ha[Ca['root']] or h not in hb: continue
            if (x[ha.index(h)] or None) != (y[hb.index(h)] or None): other += 1
        ro, rn = str(x[Ca['root']] or ''), str(y[Cb['root']] or '')
        fams = []
        for line in rn.split('\n'):
            if DB.get(line):
                k = DB.fam_of(line, y[Cb['grp']])
                if k: fam_rows[k].append(y[Cb['word']]); fams.append('%d %s' % k)
        if ro != rn:
            same = '\n'.join(DB.strip(l) for l in rn.split('\n')) == ro
            rows_root.append([i + 2, y[Cb['word']], y[Cb['split']], '、'.join(fams), '只加了“动词变化”一段' if same else '还有别的改动（请看）', ro, rn])
    rows_verb = []
    for (g, X), v in DD.VERB.items():
        ws = fam_rows.get((g, X), [])
        rows_verb.append([g, X, '%s“%s”' % v['inf'], ('%s“%s”' % v['perf']) if v.get('perf') else '（没有单独的过去式）', '%s“%s”' % v['pp'], v['rule'], kind_of(v),
                          FD.FAM[(g, X)][1] if (g, X) in FD.FAM else '', len(ws), '、'.join(ws), ''])
    rows_verb.sort(key=lambda r: -r[8])
    rows_skip = [[g, X, why] for (g, X), why in DD.SKIP.items()]
    kinds = collections.Counter(r[6] for r in rows_verb)
    dep = [v['inf'][0] for (g, X), v in DD.VERB.items() if not v.get('perf')]
    pref = [(X, v['inf'][0]) for (g, X), v in DD.VERB.items() if X in v['inf'][0] and not v['inf'][0].startswith(X)]      # 词根前面还带着前缀：distinguere、experiri、defendere、refrigerare
    summ = [
        ['一、这一轮做了什么', '', ''],
        ['词根列加了“动词变化：…；规律：…”的行', len(rows_root), '见「词根列」表：改前、改后。写在这一行“身份：”的前面；同一个词根族每一行写同一句（和“分工”一样）'],
        ['　其中只加了这一段、别的字一个没动的', sum(1 for r in rows_root if r[4].startswith('只加了')), '把新加的一段去掉，和改前一模一样'],
        ['拉丁语动词词根族', len(rows_verb), '见「动词变化」表：一族一行。请过目——哪个形式、哪句规律不对，告诉我组号或词根，改了重写那一族'],
        ['　没有单独过去式的（只写原形、过去分词）', len(dep), '、'.join(dep) + '：这几个动词在拉丁语里只有被动的样子，视频里中间那个框画成虚线'],
        ['　写的是带前缀的动词的', len(pref), '；'.join('%s → %s' % p for p in pref) + '：词根单独不用（fend、stingu、peri），或者表里的词都带这个前缀（friger），写的是真实的带前缀的动词'],
        ['别的列的改动', other, '这一轮只动了词根列'],
        ['二、各种变法有多少族（「动词变化」表的“变法”一列可以筛）', '', ''],
    ] + [['　' + k, n, ''] for k, n in kinds.most_common()] + [
        ['三、没做的、要知道的', '', ''],
        ['上一轮 103 个词根族里也是拉丁语动词、这一轮没收的', len(rows_skip), '见「没收的」表（过去式查不准、没有过去分词，或者表里讲的是名词的词干）'],
        ['没有变体的动词词根（port、scrib、mit 这类）', '—', '它们的词根行没有“身份、分工”，视频里没有“身份和分工”那一幕，这一轮没写；要不要也加，请定'],
        ['形式的来源', '—', '57 族的原形、过去式、过去分词是照拉丁语语法写的（词典里的四个主要形式的后三个；过去式写第一人称单数）。逐个查过词典的只有 ovare（查完没收）；别的没有逐个再查'],
        ['希腊语的词根族（graph、gno、cri…）', '—', '没写：希腊语动词的变法和拉丁语不是一套'],
    ]
    wb = Workbook(); wb.remove(wb.active)
    ws = sheet(wb, '说明', ['这一轮（2026-11 拉丁语动词变化轮）', '数量', '说明'], summ, [62, 10, 110])
    for r in ws.iter_rows(min_row=2):
        if r[1].value == '': r[0].font = Font(name='微软雅黑', size=10, bold=True, color='305496')
    sheet(wb, '动词变化', ['组号', '词根', '原形', '过去式', '过去分词', '规律（视频照着写、照着念；括号里的不念）', '变法', '这一族的分工（上一轮写的，对照着看）', '写进的行数', '表里的词', '备注（请写在这里）'],
          rows_verb, [7, 10, 20, 20, 22, 70, 24, 70, 8, 40, 24], freeze='C2')
    sheet(wb, '词根列', ['行号', '单词', '拆分', '词根族', '改了什么', '改前', '改后'], rows_root, [7, 16, 22, 12, 18, 80, 100], freeze='C2')
    sheet(wb, '没收的', ['组号', '词根', '为什么没收'], rows_skip, [7, 10, 110])
    wb.save(dst)
    print('清单存好了：动词变化 %d 族、词根列 %d 行、没收的 %d 族；别的列改动 %d 格' % (len(rows_verb), len(rows_root), len(rows_skip), other))


if __name__ == '__main__':
    main(*sys.argv[1:4])

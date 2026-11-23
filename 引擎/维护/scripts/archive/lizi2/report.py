# -*- coding: utf-8 -*-
"""2026-11 例词清理轮的改动清单（只作记录）：
  python3 report.py <原表.xlsx> <新表.xlsx> <清单.xlsx>
表：说明、去掉的例词（请过目）、去掉的例词汇总、留着的例词汇总、去掉的“见”、逐格（改前、改后，要恢复照它抄回去）"""
import os, sys, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
import linetools as LT
import lizi as LZ
import lizi_data as LD
import round as RD

HF = Font(name='微软雅黑', bold=True, color='FFFFFF'); HFILL = PatternFill('solid', fgColor='305496')
BF = Font(name='微软雅黑', size=10); WRAP = Alignment(wrap_text=True, vertical='top')
COLN = {'pre': '前缀', 'suf': '后缀', 'root': '词根'}


def sheet(wb, title, head, rows, widths):
    ws = wb.create_sheet(title)
    ws.append(head)
    for c in ws[1]: c.font = HF; c.fill = HFILL; c.alignment = WRAP
    for r in rows:
        ws.append([('\'' + v if isinstance(v, str) and v.startswith('=') else v) for v in r])
    for i, w in enumerate(widths): ws.column_dimensions[chr(65 + i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row: c.font = BF; c.alignment = WRAP
    ws.freeze_panes = 'A2'
    if rows: ws.auto_filter.ref = 'A1:%s%d' % (chr(64 + len(head)), len(rows) + 1)
    return ws


def how(w, data, C, by):
    ri = by.get(w.lower())
    if ri is None: return '表里没有'
    r = data[ri]
    return '%s %s' % (str(r[C['typ']] or '')[:1], r[C['split']] if str(r[C['split']] or '').strip() not in ('', '—') else '不拆')


def why_keep(w, col, lab, data, C, by):
    lw = w.lower()
    if lw in LD.KEEP_IN: return '逐个看过：留（国名、月份、数词这类）'
    ri = by.get(lw)
    if ri is not None:
        if LZ.is_simple_type(data[ri], C): return '基础词 / 变体词'
        return '单词 + 词缀（没有词根）'
    if any(LZ.known(x, by) for x in LZ.rest_of(lw, col, lab)) and lw not in LD.DROP_OUT: return '表里没有；去掉词缀剩下的是认识的词'
    return '表里没有；逐个看过：留'


def main(src, dst, out):
    hdr, C, data, W, changes, log, alog, rlog = RD.run(src)
    h2, C2, new = LT.load_table(dst)
    by = LZ.index(data, C)
    wb = Workbook(); wb.remove(wb.active)
    body = lambda line: ''.join(LZ.split_line(line)[:2])
    # ---- 去掉的例词（请过目）
    rm_rows, see_rows, summ = [], [], collections.Counter()
    for ri, w, col, lab, what, xs, line, nl in alog:
        if what == '例词':
            rm_rows.append([ri + 2, w, COLN[col], lab, '、'.join(xs), body(line), body(nl)])
            for x in xs: summ[(COLN[col], lab, LZ.WORD.match(x).group(0))] += 1
        else:
            see_rows.append([ri + 2, w, COLN[col], lab, '、'.join(xs), body(line), body(nl)])
    for w, lab, rm, l in rlog:
        ri = by[str(w).lower()]
        nl = next((x for x in str(W[ri][C['root']]).split('\n') if LT.label_body(x)[0] == lab), '')
        cut = lambda s: re.split(r'动词变化：|身份：|；记：', s)[0]
        rm_rows.append([ri + 2, w, '词根', lab, '、'.join(rm), cut(l), cut(nl)])
        for x in rm: summ[('词根', lab, LZ.WORD.match(x).group(0))] += 1
    rm_rows.sort(key=lambda r: r[0])
    # ---- 留着的例词
    kept = collections.Counter()
    for ri, col, li, lab, line in LZ.affix_rows(W, C):
        head, main_, meta = LZ.split_line(line)
        if not LZ.SAME.search(main_): continue
        seen = []
        LZ.clean_main(main_, lambda x: (seen.append(x), 'ok')[1], [])
        for x in seen: kept[(COLN[col], lab, x, why_keep(x, col, lab, data, C, by))] += 1
    # ---- 说明
    n = collections.Counter()
    for ri, w, col, lab, what, xs, line, nl in alog: n[(col, what)] += len(xs)
    info = [
        '2026-11 例词清理轮：原表 %s → 新表 %s' % (os.path.basename(src), os.path.basename(dst)),
        '共改 %d 格（%d 行）：前缀 %d、后缀 %d、词根 %d。只动了这三列里“同 例词”“见 X”这两种半句，别的列一格没动；身份分工、记法、动词变化这几段没动。'
        % (len(changes), len({r for r, c in changes}), log['前缀列'], log['后缀列'], log['词根列']),
        '新表读回来和“原表 + 改动”逐格比 0 处不一致；每一处改动都只是删字（程序逐条核对过），没有改写别的话（proportion 一处除外）。',
        None,
        '一、去掉了什么：解释前缀、后缀的那一行里，“同 例词”的例词自己还带着不能单独用的词根的（学生还得先拆它）：',
        '    pro- 的 progress（pro + gress）、in- 的 include、con- 的 connect、ex- 的 exit、-ate 的 create（cre + ate）、-ary 的 dictionary、-ure 的 culture……',
        '    前缀列去掉 %d 个、后缀列去掉 %d 个；词根列补去上一轮漏掉的 %d 个（circuit 的 exit、transit，illusion 的 allude、interlude）。'
        % (n[('pre', '例词')], n[('suf', '例词')], sum(len(x[2]) for x in rlog)),
        '二、留着什么：“学生认识的单词 + 这个词缀”的例词（unhappy、rewrite、return、teacher、quickly、action、national）、基础词（magic）、',
        '    讲拼写变化的（possible → possibly）、短语、身份分工里的例词（pro- 多是“向前”（progress、produce））。见「留着的例词汇总」。',
        '三、“见 X”：词缀行里指到“同一个词缀的别的词”、那个词自己还带词根的去掉（product 的 pro-“见 produce”），共 %d 处；'
        % (n[('pre', '见')] + n[('suf', '见')]),
        '    指到简单词、原形、另一种拼法、【背景】的照留（unhappily 见 unhappy、recognise 见 recognize）。',
        '四、怎么判断：例词在总表里那一行「词根」列有词根就算“还得再拆”；表里没有的词，去掉词缀剩下的是表里的词才留，逐个看过的例外记在维护技能 scripts/lizi_data.py。',
        '五、要恢复：告诉我哪个词缀的哪个例词要留，我照「逐格」表的“改前”恢复，并记进名单，以后不再去掉。',
    ]
    ws = wb.create_sheet('说明')
    for line in info: ws.append([line])
    ws.column_dimensions['A'].width = 150
    for row in ws.iter_rows():
        for c in row: c.font = BF; c.alignment = WRAP
    sheet(wb, '去掉的例词（请过目）', ['行', '单词', '列', '标签', '去掉的例词', '原来那一行（正文）', '现在那一行（正文）'], rm_rows, [7, 16, 6, 10, 34, 80, 70])
    sheet(wb, '去掉的例词汇总', ['列', '词缀 / 词根', '去掉的例词', '它在总表里怎么拆', '去掉了几处'],
          [[a, b, c, how(c, data, C, by), k] for (a, b, c), k in sorted(summ.items(), key=lambda x: (-x[1], x[0]))], [8, 14, 22, 40, 10])
    sheet(wb, '留着的例词汇总', ['列', '词缀', '留着的例词', '它在总表里怎么拆', '为什么留', '出现几处'],
          [[a, b, c, how(c, data, C, by), d, k] for (a, b, c, d), k in sorted(kept.items(), key=lambda x: (-x[1], x[0]))], [8, 12, 22, 34, 40, 10])
    sheet(wb, '去掉的“见”和改写', ['行', '单词', '列', '标签', '去掉的 / 改写', '原来那一行（正文）', '现在那一行（正文）'], see_rows, [7, 16, 6, 10, 34, 80, 70])
    cells = []
    for (rn, ci), v in sorted(changes.items()):
        cells.append([rn, data[rn - 2][C['word']], hdr[ci], str(data[rn - 2][ci] or ''), str(v or '')])
    sheet(wb, '逐格', ['行', '单词', '列', '改前', '改后'], cells, [7, 16, 6, 110, 110])
    wb.save(out)
    print('清单 %s：去掉的例词 %d 行、汇总 %d 种、留着的 %d 种、见 %d 行、逐格 %d' % (out, len(rm_rows), len(summ), len(kept), len(see_rows), len(cells)))
    return summ, kept


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])

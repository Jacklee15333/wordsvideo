# -*- coding: utf-8 -*-
"""2026-11 词缀来历、记法轮的改动清单（只作记录）：
  python3 report.py <原表.xlsx> <新表.xlsx> <清单.xlsx> [原来的 dongbian_data.py]
表：说明、词缀来历（目录每一条换了几行）、词缀记法、来历没换的（认不出的旧写法，没动）、前缀后缀列（逐格）、
    动词变化（57 族规律改前改后）、去掉的例词（请过目）、词根记法（换掉的、新加的）、词根列（逐格）、词根变体处理"""
import os, sys, re, collections, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
import linetools as LT
import laili as LL
import laili_data as LD
import dongbian_data as DD
import round as RD

HF = Font(name='微软雅黑', bold=True, color='FFFFFF'); HFILL = PatternFill('solid', fgColor='305496')
BF = Font(name='微软雅黑', size=10); WRAP = Alignment(wrap_text=True, vertical='top')


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


def memo_of(line):
    m = LL.MEMO_RX.search(line or '')
    return line[m.start():].lstrip('；; ') if m else ''


def main(src, dst, out, old_dd=None):
    hdr, C, data, W, changes, log, st, lz, lstat, miss = RD.run(src)
    h2, C2, new = LT.load_table(dst)
    wb = Workbook(); wb.remove(wb.active)
    # ---- 词缀：逐行再算一遍做了什么
    per_entry = collections.defaultdict(collections.Counter)
    notrec, affix_rows = [], []
    for ri, col, li, lab, kind, sense, line in LL.rows_of(data, C):
        e = LL.entry_for(col, lab, kind, sense, LL.probe_of(line))
        if not e: continue
        nl, acts = LL.line_new(line, e)
        k = (e['col'], ' '.join(sorted(e['labels'])), e['kind'], e['new'], e['memo'])
        per_entry[k]['行'] += 1
        for a in acts: per_entry[k][a] += 1
        if '没认出' in acts:
            src_ = LL.find_src(LL.split_line(line)[1])
            notrec.append([ri + 2, data[ri][C['word']], {'pre': '前缀', 'suf': '后缀'}[col], lab, src_[2][src_[3]][0] if src_ else '', line[:400]])
    for (ri, ci), v in sorted(changes.items()):
        name = hdr[ci]
        if name not in ('前缀', '后缀'): continue
        a, b = str(data[ri - 2][ci] or ''), str(v or '')
        what = []
        if memo_of(b) and memo_of(b) != memo_of(a): what.append('加记法' if not memo_of(a) else '换记法')
        if LL.SHEN.sub('', a.split('；记：')[0]) != LL.SHEN.sub('', b.split('；记：')[0]): what.append('来历')
        if '身份：' in b and '身份：' not in a: what.append('补身份、分工')
        affix_rows.append([ri, data[ri - 2][C['word']], name, '、'.join(what), a, b])
    # ---- 说明
    ws = wb.create_sheet('说明')
    lines = [
        '2026-11 词缀来历、记法轮：原表 0词源拆分总表_动词变化版.xlsx → 新表 0词源拆分总表_词缀来历记法版.xlsx',
        '共改 %d 格（%d 行）：%s。只动了前缀、词根、后缀三列和「词根变体处理」两格，别的列一格没动；新表读回来和“原表 + 改动”逐格比 0 处不一致。' % (
            len(changes), len({r for r, c in changes}), '、'.join('%s %d' % kv for kv in collections.Counter(hdr[c] for r, c in changes).items())),
        '',
        '一、词缀来历（前缀列、后缀列）：每个词缀（一种用法）一条统一的来历，整句替换括号里原来的来源那一段；同一个括号里的“同 例词”、讲写法的半句照留。',
        '    认得出的旧写法才换，认不出的不动（「来历没换的」表）；一点来源都没写的行补上（只补了正文里哪儿也没提来源的几行）。目录在维护技能 scripts/laili_data.py。',
        '二、词缀记法：和词根一样，在那一行末尾加“；记：X ≈ Y（中文）：道理。音变：…”。名单是用户同意的：pro ≈ for、dis ≈ two、ad ≈ at、ab ≈ off、trans ≈ through（词典说“也许”）、',
        '    super ≈ over、sub ≈ up、un / in / non ≈ no、en ≈ in、mis ≈ miss、be ≈ by、-ly ≈ like、-ful ← full、-less ≈ lose、-ship ≈ shape、-teen / -ty ≈ ten；bio 写了 zoo、quick 两个词。',
        '    re-、com-、ex-、de-、-ion、-ment 等查不到学生认识的同族简单词，不写。',
        '三、动词变化（词根列 57 族、318 格）：规律的第一句加“原形去掉词尾 -ere 就是 duc（ducere → duc）”；规律括号里的复杂例词（respiratory、refrigerator……）去掉。',
        '四、复杂例词（词根列）：词根行“同 …”里同一个词根的“前缀 + 词根”“词根 + 词根”的词去掉（maintain 那一行的 contain、obtain、retain）——「去掉的例词（请过目）」表，要留的告诉我照原样恢复。',
        '五、词根记法：geo ≈ Gaia、bio ≈ zoo、vac ≈ want、logue / log ≈ logo 换掉了原来拿 geography、biology、vacation、dialogue 记的；新加 gen ≈ kind、mon ≈ mind、the ≈ do、ly ≈ loose；',
        '    index 补上了 dic ≈ teach。logic、prologue 有了记法，「词根变体处理」列的“记法待补”去掉（还剩 33 行）。',
        '',
        '体检：补成 22 列以后的 video_check、guoqu_check、hecheng_check、rule_check、zimu_check、pinxie_check、root_check、yingmei_check、audit、audit_split_labels、meaning 输出和原表一样；',
        'shenfen_check（14 项）、dongbian、tonggen_check、part_memo --check、laili --check、lizi、cizhui 都是 0。',
    ]
    for l in lines: ws.append([l])
    ws.column_dimensions['A'].width = 160
    for row in ws.iter_rows():
        for c in row: c.font = BF; c.alignment = Alignment(wrap_text=True)
    # ---- 词缀来历
    rows = []
    for k, cnt in sorted(per_entry.items(), key=lambda x: -x[1]['行']):
        col, labs, kind, new_, memo = k
        rows.append(['前缀' if col == 'pre' else '后缀', labs, '' if kind == '*' or col == 'pre' else kind, new_, cnt['行'], cnt['换'], cnt['补'], cnt['已是新'], cnt['没认出'], cnt['记'],
                     LD.memo_text(memo) if memo else ''])
    sheet(wb, '词缀来历', ['列', '词缀', '变成什么', '新来历（目录里的一句）', '这一类的行', '换了', '补了', '原来就是这一句', '认不出没动', '加记法', '记法'], rows,
          [7, 22, 8, 60, 8, 7, 7, 9, 9, 8, 70])
    rows = [[k, LD.memo_text(k), sum(c['记'] for kk, c in per_entry.items() if kk[4] == k)] for k in LD.MEMO]
    sheet(wb, '词缀记法', ['键', '记法（写在那一行末尾）', '加了几行'], rows, [10, 120, 10])
    sheet(wb, '来历没换的', ['行', '单词', '列', '标签', '括号里的来源那一段', '这一行'], notrec, [7, 16, 6, 10, 50, 100])
    sheet(wb, '前缀后缀列', ['行', '单词', '列', '做了什么', '改前', '改后'], affix_rows, [7, 16, 6, 14, 80, 80])
    # ---- 动词变化
    od = None
    if old_dd:
        spec = importlib.util.spec_from_file_location('old_dd', old_dd); od = importlib.util.module_from_spec(spec); spec.loader.exec_module(od)
    rows = []
    cnt_root = collections.Counter()
    for (ri, ci), v in changes.items():
        if hdr[ci] == '词根':
            for k in DD.VERB:
                if ('；规律：' + (DD.VERB[k].get('cut', '') + '；' if DD.VERB[k].get('cut') else '') + DD.VERB[k]['rule']) in str(v): cnt_root[k] += 1
    for k, v in DD.VERB.items():
        old_rule = od.VERB[k]['rule'] if od and k in od.VERB else ''
        new_rule = (v.get('cut') + '；' if v.get('cut') else '') + v['rule']
        rows.append([k[0], k[1], v['inf'][0], old_rule, new_rule, cnt_root[k]])
    sheet(wb, '动词变化', ['组号', '词根', '原形', '原来的规律', '现在的规律', '行数'], rows, [7, 9, 13, 70, 80, 6])
    rows = [[next((ri + 2 for ri, r in enumerate(data) if r[C['word']] == w), ''), w, lab, '、'.join(rm), l] for w, lab, rm, l in lz]
    sheet(wb, '去掉的例词（请过目）', ['行', '单词', '标签', '去掉的例词', '原来那一行'], rows, [7, 16, 12, 40, 120])
    rows = []
    for (ri, ci), v in sorted(changes.items()):
        if hdr[ci] not in ('前缀', '词根', '后缀'): continue
        a = str(data[ri - 2][ci] or '').split('\n'); b = str(v or '').split('\n')
        for la, lb in zip(a, b):
            ma, mb = memo_of(la), memo_of(lb)
            if mb and mb != ma and hdr[ci] == '词根' or (mb and ma and mb != ma):
                rows.append([ri, data[ri - 2][C['word']], hdr[ci], LT.label_body(lb)[0], ma, mb])
    sheet(wb, '词根记法', ['行', '单词', '列', '标签', '原来的记法', '现在的记法'], rows, [7, 16, 6, 10, 60, 90])
    rows = []
    for (ri, ci), v in sorted(changes.items()):
        if hdr[ci] != '词根': continue
        a, b = str(data[ri - 2][ci] or ''), str(v or '')
        what = []
        if '；规律：' in b and re.search(r'；规律：[^；]*去掉', b) and not re.search(r'；规律：[^；]*去掉', a): what.append('规律加去词尾一句')
        if any(w == data[ri - 2][C['word']] for w, *_ in lz): what.append('去掉例词')
        if memo_of(b) != memo_of(a) or re.findall(r'记：[^；]*', b) != re.findall(r'记：[^；]*', a): what.append('记法')
        rows.append([ri, data[ri - 2][C['word']], '、'.join(what), a, b])
    sheet(wb, '词根列', ['行', '单词', '做了什么', '改前', '改后'], rows, [7, 16, 18, 90, 90])
    rows = [[ri, data[ri - 2][C['word']], data[ri - 2][ci], v] for (ri, ci), v in sorted(changes.items()) if hdr[ci] == '词根变体处理']
    sheet(wb, '词根变体处理', ['行', '单词', '改前', '改后'], rows, [7, 16, 60, 40])
    wb.save(out)
    print('改动清单：%s（%s）' % (out, '、'.join('%s %d' % (ws.title, ws.max_row - 1) for ws in wb.worksheets[1:])))


if __name__ == '__main__':
    main(*sys.argv[1:5])

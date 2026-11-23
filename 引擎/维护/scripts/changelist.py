# -*- coding: utf-8 -*-
"""改动清单（project_rules.md 第 64 条）：比较两版总表，把改了的地方列成一份 xlsx，用户逐行过目、要恢复都靠它。
  python3 changelist.py <改前.xlsx> <改后.xlsx> <清单.xlsx>
两版的行要一一对应（同样的行数、同样的单词顺序）。按列名读表。
  · 组合列：一行 = 一条“　用词规律：”行的变化（这一步、原来、现在、处理）；另把“前提对不上 → 删掉”的单列一张表请用户过目
  · 别的列：一行 = 一格的变化（改前、改后、类别）"""
import re, sys, collections
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

RL = '\u3000用词规律：'
RETIRED = ('一个词用进某一行', '同一个词，英国、美国')      # 2026-11 取消的两条空洞说法


def read(path):
    wb = load_workbook(path, read_only=True)
    ws = wb['拆分结果'] if '拆分结果' in wb.sheetnames else wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True))
    return [str(h or '') for h in rows[0]], rows[1:]


def rules(cell):
    out, step = [], ''
    for l in str(cell or '').split('\n'):
        if l.startswith(RL):
            out.append((step, l[len(RL):]))
        else:
            step = l.strip()
    return out


def main(a, b, dst):
    ha, ra = read(a)
    hb, rb = read(b)
    assert len(ra) == len(rb), '两版行数不一样：%d / %d' % (len(ra), len(rb))
    W = next(i for i, h in enumerate(ha) if h.startswith('单词'))
    M = next(i for i, h in enumerate(ha) if h.startswith('组合'))
    key = lambda st: re.sub(r'\s+', '', st)
    memo = lambda t: re.findall(r'记：[^\n]*', str(t or ''))
    rule_rows, cell_rows, s1, s2 = [], [], collections.Counter(), collections.Counter()
    for n, (x, y) in enumerate(zip(ra, rb), start=2):
        assert str(x[W]) == str(y[W]), '第 %d 行单词对不上：%s / %s' % (n, x[W], y[W])
        w = x[W]
        for c, h in enumerate(ha):
            hb_c = hb.index(h) if h in hb else None
            if hb_c is None:
                continue
            so, sn = ('' if x[c] is None else str(x[c])), ('' if y[hb_c] is None else str(y[hb_c]))
            if so == sn:
                continue
            if c == M:
                o, nw = rules(so), rules(sn)
                steps_same = [l for l in so.split('\n') if not l.startswith(RL)] == [l for l in sn.split('\n') if not l.startswith(RL)]
                if not steps_same:                       # 步骤也改了：整格列出来
                    rule_rows.append((n, w, '（整格重写）', so, sn, '步骤也改了（整格）'))
                    s1['步骤也改了（整格）'] += 1
                    continue
                nd, od = collections.defaultdict(list), collections.defaultdict(list)
                for st, t in nw: nd[key(st)].append(t)
                for st, t in o: od[key(st)].append(t)
                for st, t in o:
                    news = nd.get(key(st), [])
                    if t in news:
                        continue
                    ret = t.startswith(RETIRED)
                    cand = [z for z in news if z not in od[key(st)]]
                    if cand:
                        kind = '空洞说法 → 换成真规律' if ret else ('规律没变，例子改了' if cand[0].split('（')[0] == t.split('（')[0] else '前提对不上 → 改贴别的规律')
                        rule_rows.append((n, w, st, t, cand[0], kind))
                    else:
                        kind = '空洞说法，找不到真规律 → 删掉' if ret else '前提对不上 → 删掉'
                        rule_rows.append((n, w, st, t, '', kind))
                    s1[kind] += 1
                for st, t in nw:
                    if key(st) not in od and t not in [z[1] for z in o]:
                        rule_rows.append((n, w, st, '', t, '新加'))
                        s1['新加'] += 1
                continue
            tags = []
            if h.startswith('拆分'):
                tags.append('拆分')
            elif h.startswith('词根变体处理'):
                tags.append('标记')
            else:
                if '由词根' in so and '的另一种写法' in sn: tags.append('“由词根 X 变来”→ 同一个词根的另一种写法 + 字母变化')
                if len(re.findall(r'见 ?[A-Za-z]', so)) > len(re.findall(r'见 ?[A-Za-z]', sn)): tags.append('去掉“见 同组的词”')
                mo, mn = memo(so), memo(sn)
                if mo != mn:
                    if mo and not mn: tags.append('记法去掉')
                    elif mn and not mo: tags.append('记法新加')
                    else:
                        if re.sub(r'。音变：.*', '', mn[0]) != re.sub(r'。音变：.*', '', mo[0]): tags.append('记法换了写法')
                        if '音变：' in mn[0] and '音变：' not in mo[0]: tags.append('记法补音变')
                if not tags: tags.append('其他')
            for t in tags: s2[t] += 1
            cell_rows.append((n, w, h.split('（')[0][:12], '；'.join(tags), so, sn))
    wb = Workbook()
    head, fill, wrap = Font(bold=True, color='FFFFFF'), PatternFill('solid', fgColor='2F5D50'), Alignment(wrap_text=True, vertical='top')

    def sheet(ws, title, cols, widths, rows):
        ws.title = title
        ws.append(cols)
        for i, wd in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = wd
            cc = ws.cell(1, i); cc.font = head; cc.fill = fill; cc.alignment = Alignment(vertical='center', wrap_text=True)
        for r in rows: ws.append(list(r))
        for row in ws.iter_rows(min_row=2):
            for cc in row: cc.alignment = wrap
        ws.freeze_panes = 'C2'
        ws.auto_filter.ref = ws.dimensions

    ws0 = wb.active
    ws0.title = '说明'
    ws0.column_dimensions['A'].width = 40; ws0.column_dimensions['B'].width = 120
    for row in [('改前', a), ('改后', b), ('怎么看', '每张表都开了筛选：按“处理 / 类别”一列筛。“行号”是总表里的 Excel 行号。用词规律一行 = 一条规律行的变化（现在是空的 = 删掉了）；别的列一行 = 一格的变化。'),
                ('　空洞说法 → 换成真规律', '原来是“一个词用进某一行…”或“同一个词，英国、美国的用法有时不一样”，换成了讲得出道理的规律。'),
                ('　空洞说法，找不到真规律 → 删掉', '同上两条，但这一步找不到真规律（步骤本身已经讲清了），规律那一行删掉。'),
                ('　前提对不上 → 删掉（请过目）', '别的规律套错了：这个词不是动作词、或词性对不上（“表示动作的词，也拿来叫做这件事用的东西”套在一个本来就是东西的词上）。'
                 '这一类单独列在「请过目：前提对不上删掉的」一张表里；哪一行该留，说行号或单词，照原样恢复。'),
                ('　前提对不上 → 改贴别的规律', '同上，但能换成对得上的规律（safe 安全的 → 保险箱：改成“表示性质、状态的词，也拿来叫有这种性质的东西”）。'),
                ('　规律没变，例子改了', '同一条规律在这个词里第二次出现只留熟悉的例子；或把例子换成和本词是一回事的。'),
                ('　“由词根 X 变来”→ 同一个词根的另一种写法 + 字母变化', 'duc / duce / duct 这类：不再当几个词根讲，每一行自己讲清字母怎么变；拆分写成 pro + duct(=duc)。'),
                ('　去掉“见 同组的词”', '词根那一行不再让学生去看同组别的派生词（见 reduce）。'),
                ('　记法换了写法 / 补音变 / 去掉', '关联词换成比本词更简单的；≈ 两边写法差得多的补“音变”；找不到简单关联词的去掉，在「词根变体处理」列标“记法待补”。'),
                ('用词规律各类行数', '；'.join('%s %d' % kv for kv in s1.most_common())), ('别的列各类格数', '；'.join('%s %d' % kv for kv in s2.most_common()))]:
        ws0.append(list(row))
    for row in ws0.iter_rows():
        for cc in row: cc.alignment = wrap
        row[0].font = Font(bold=True)
    cols = ['行号', '单词', '这一步', '原来的规律行', '现在的规律行（空 = 删掉）', '处理']
    order = {'前提对不上 → 删掉': 0, '前提对不上 → 改贴别的规律': 1, '空洞说法，找不到真规律 → 删掉': 2, '空洞说法 → 换成真规律': 3}
    drop = [r for r in rule_rows if r[5] == '前提对不上 → 删掉']
    if drop: sheet(wb.create_sheet(), '请过目：前提对不上删掉的', cols, [8, 16, 60, 70, 50, 26], drop)
    sheet(wb.create_sheet(), '用词规律（全部）', cols, [8, 16, 60, 70, 70, 30], sorted(rule_rows, key=lambda r: (order.get(r[5], 9), r[0])))
    sheet(wb.create_sheet(), '别的列（全部）', ['行号', '单词', '列', '类别', '改前', '改后'], [8, 16, 14, 40, 80, 80], cell_rows)
    wb.save(dst)
    print('用词规律 %d 行：%s' % (len(rule_rows), dict(s1)))
    print('别的列 %d 格：%s' % (len(cell_rows), dict(s2)))
    print('写好了', dst)


if __name__ == '__main__':
    main(*sys.argv[1:4])

# -*- coding: utf-8 -*-
"""2026-11 身份分工、辨析列轮的改动清单（用户逐行过目、要恢复都靠它）。
  python3 report.py <round.py 存的 round_shenfen.pkl> <清单.xlsx>"""
import sys, os, re, pickle, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..')); sys.path.insert(0, HERE)
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
import linetools as LT, shenfen, cizhui, bianxi as B, cols as CL
import shenfen_data as FD, cizhui_catalog as Z

FONT = Font(name='微软雅黑', size=10); HEAD = Font(name='微软雅黑', size=10, bold=True, color='FFFFFF'); FILL = PatternFill('solid', fgColor='305496')
WRAP = Alignment(wrap_text=True, vertical='top')
def sheet(wb, title, head, rows, widths):
    ws = wb.create_sheet(title)
    ws.append(head)
    for r in rows: ws.append(['' if v is None else v for v in r])
    for j, w in enumerate(widths): ws.column_dimensions[chr(65 + j)].width = w
    for c in ws[1]: c.font = HEAD; c.fill = FILL; c.alignment = Alignment(vertical='center', wrap_text=True)
    for row in ws.iter_rows(min_row=2):
        for c in row: c.font = FONT; c.alignment = WRAP
    ws.freeze_panes = 'A2'
    if rows: ws.auto_filter.ref = 'A1:%s%d' % (chr(64 + len(head)), len(rows) + 1)
    return ws

def main(pkl, dst):
    d = pickle.load(open(pkl, 'rb'))
    C, old, new, bcol, heqi, plan = d['C'], d['old'], d['new'], d['bcol'], d['heqi'], d['plan']
    W = lambda i: new[i][C['word']]
    wb = Workbook(); wb.remove(wb.active)
    # —— 词根列
    rows_root = []
    for i in range(len(old)):
        a, b = old[i][C['root']] or '', new[i][C['root']] or ''
        if a == b: continue
        cutc = '\n'.join(plan[i]['cut']) if i in plan else ''
        hq = next((l[5:] for l in str(new[i][C['combo']]).split('\n') if l.startswith('\u3000合起来：')), '')
        kinds = []
        if cutc: kinds.append('切掉了通到今义的链')
        if '身份：' in b and '身份：' not in a: kinds.append('加身份、分工')
        if b.count('\n') < a.count('\n'): kinds.append('“合起来”的一行挪到组合列')
        rows_root.append([i + 2, W(i), old[i][C['split']], '；'.join(kinds), a, b, cutc, hq])
    # —— 合起来
    rows_hq = []
    for i in range(len(old)):
        hq = next((l for l in str(new[i][C['combo']]).split('\n') if l.startswith('\u3000合起来：')), None)
        if not hq: continue
        src = []
        for col, name in (('root', '词根列'), ('pre', '前缀列'), ('wp', '单词部分列')):
            if (old[i][C[col]] or '') != (new[i][C[col]] or '') and (col != 'pre' or CL.strip_shenfen(new[i][C[col]] or '') != (old[i][C[col]] or '')): src.append(name)
        rows_hq.append([i + 2, W(i), old[i][C['split']], hq.strip(), '、'.join(src), str(new[i][C['combo']]).split('\n')[0]])
    # —— 前缀列、单词部分列里身份分工以外的改动
    rows_other = []
    for i in range(len(old)):
        for col, name in (('pre', '前缀'), ('wp', '单词部分'), ('suf', '后缀'), ('bg', '背景'), ('snd', '音变')):
            a, b = old[i][C[col]] or '', new[i][C[col]] or ''
            b0 = '\n'.join(CL.strip_shenfen(l) for l in b.split('\n'))
            if a != b0: rows_other.append([i + 2, W(i), name, a, b0, '“【辨析】”改成“辨析列”' if a.replace('【辨析】', '辨析列') == b0 else ('补“这里是”' if '这里是' in b0 and '这里是' not in a else '“合起来”的话挪到组合列')])
    # —— 词缀身份分工
    cnt = collections.Counter(); ex = {}
    for i in range(len(old)):
        for col in ('pre', 'suf'):
            for l in str(new[i][C[col]] or '').split('\n'):
                sf = CL.shenfen_of(l)
                if sf and '身份：' not in str(old[i][C[col]] or ''):
                    lab = LT.label_body(l)[0]; cnt[(lab, sf[0])] += 1; ex.setdefault((lab, sf[0]), []).append(W(i))
    grp_of = {}
    for (lab, k), (idt, g) in Z.SUF.items(): grp_of[(lab, idt)] = g
    for lab, e in Z.PRE.items():
        for it in (e if isinstance(e, list) else [e]): grp_of[(lab, it[-2])] = it[-1]
    rows_aff = [[lab, idt, grp_of.get((lab, idt), 'adj_n' if lab == '-ed' else ''), n, '、'.join(ex[(lab, idt)][:6])] for (lab, idt), n in sorted(cnt.items(), key=lambda kv: -kv[1])]
    rows_grp = [[g, t, sum(r[3] for r in rows_aff if r[2] == g)] for g, t in Z.GROUP.items()]
    # —— 词根族
    famrows = collections.Counter()
    for i in range(len(new)):
        for l in str(new[i][C['root']] or '').split('\n'):
            if '。分工：' in l:
                m = shenfen.VARL.match(l); lab = LT.label_body(l)[0]
                key = next(((g, X) for (g, X) in FD.FAM if g == new[i][C['grp']] and (X == (m.group(2) if m else None) or X.lower() == shenfen.core(lab).lower())), None)
                if key: famrows[key] += 1
    rows_fam = []
    for (g, X), (forms, text) in FD.FAM.items():
        ids = '\n'.join('%s：%s' % (Y, FD.ID.get(v, v) if not isinstance(v, dict) else '；'.join('%s%s' % ('' if k == '*' else k + ' 里是', FD.ID.get(x, x)) for k, x in v.items())) for Y, v in forms.items())
        rows_fam.append([g, X, ids, text, famrows[(g, X)]])
    rows_fam.sort(key=lambda r: -r[4])
    # —— 同义词组
    idx, terms = B.build_index(old, C)
    rows_syn = []
    for (pos, t), v in idx.items():
        keep = []
        for w, _ in v:
            if not any(B.same_lemma(w, y) for y in keep): keep.append(w)
        if len(keep) >= 2: rows_syn.append([t, pos, len(keep), '、'.join(keep)])
    rows_syn.sort(key=lambda r: (-r[2], r[0]))
    # —— 辨析列：补来的、待补的
    rows_fill, rows_todo = [], []
    for i, cell in enumerate(bcol):
        if not cell: continue
        _, bx = B.split_bianxi(old[i][C['combo']])
        syn = [l for l in cell.split('\n') if l.startswith('【同义词】')]
        body = '\n'.join(l for l in cell.split('\n') if not l.startswith('【同义词】'))
        if W(i) not in ('produce', 'product') and body.strip() != bx.strip():
            extra = body[len(bx):].strip() if body.startswith(bx) else body
            rows_fill.append([i + 2, W(i), '\n'.join(syn), extra])
        ws_ = B._syn_words(cell, W(i))
        if ws_ and not any(B._has(x, body) for x in ws_): rows_todo.append([i + 2, W(i), '\n'.join(syn), body])
    nbx = sum(1 for i in range(len(old)) if B.split_bianxi(old[i][C['combo']])[1])
    summ = [
        ['一、词根列只讲词根本身', '', ''],
        ['词根列改动的格', len(rows_root), '见「词根列」表：改前、改后、切出去的链、挪到组合列的“合起来”'],
        ['　其中切掉“词根的意思 → 前缀“…”… → 今天的意思”这种链的行', sum(1 for r in rows_root if '切掉' in r[3]), '链里带着前缀讲解的 193 行；组合列本来就有同样的推导'],
        ['　组合列新加“　合起来：”一行', len(rows_hq), '见「合起来」表：原来写在词根列（前缀列、单词部分列）的整合，或链里组合列没有的拉丁语、希腊语原词'],
        ['　前缀列补“这里是…”、前缀列 / 单词部分列里的“合起来”挪走', sum(1 for r in rows_other if r[5] != '“【辨析】”改成“辨析列”'), '见「其他列」表'],
        ['二、同一个词根几种写法的身份和分工', '', ''],
        ['词根族', len(FD.FAM), '见「词根族分工」表：每个写法的身份、整族怎么分工'],
        ['写进“身份：…。分工：…”的词根行', sum(famrows.values()), '“词根 X 的另一种写法”321 行 + 同族用原形的 138 行'],
        ['三、前缀、后缀的身份和分工', '', ''],
        ['加了“；身份：…。分工：…”的词缀行', sum(cnt.values()), '见「词缀身份」「词缀分工组」两张表；后缀 %d 格、前缀 %d 格' % (sum(1 for i in range(len(old)) if (old[i][C['suf']] or '') != (new[i][C['suf']] or '')), sum(1 for i in range(len(old)) if (old[i][C['pre']] or '') != (new[i][C['pre']] or '')))],
        ['四、辨析列', '', ''],
        ['组合列的【辨析】整段挪到新列「辨析」', nbx, '一字不改；组合列和别的列里“见【辨析】”改成“见辨析列”'],
        ['辨析列有内容的行', sum(1 for c in bcol if c), ''],
        ['　有【同义词】行的', sum(1 for c in bcol if c and '【同义词】' in c), '按含义列算：同一词性、同一个中文意思的几个词；全表的组见「同义词组」表'],
        ['　从同组别的词那一行补来辨析的', len(rows_fill), '见「辨析补来的」表'],
        ['　同义词组还没有辨析文字的（待补）', len(rows_todo), '见「辨析待补」表：做视频时第三部分要补，或以后一轮轮补'],
        ['　手写的样板', 2, 'produce、product（视频第三部分照它讲）'],
    ]
    ws = sheet(wb, '说明', ['这一轮做了什么', '数量', '说明'], summ, [58, 10, 90])
    for r in ws.iter_rows(min_row=2):
        if r[1].value == '': r[0].font = Font(name='微软雅黑', size=10, bold=True, color='305496')
    sheet(wb, '词根列', ['行号', '单词', '拆分', '改了什么', '改前', '改后', '切出去的链（组合列已有同样的推导）', '组合列新加的“合起来”'], rows_root, [7, 16, 22, 22, 70, 70, 50, 40])
    sheet(wb, '合起来', ['行号', '单词', '拆分', '组合列新加的一行', '原来写在', '组合列第一行'], rows_hq, [7, 16, 22, 80, 14, 60])
    sheet(wb, '其他列', ['行号', '单词', '列', '改前', '改后（不算身份、分工）', '类别'], rows_other, [7, 16, 10, 70, 70, 26])
    sheet(wb, '词根族分工', ['组号', '词根', '各种写法的身份', '分工', '写进的行数'], rows_fam, [7, 10, 60, 100, 10])
    sheet(wb, '词缀身份', ['词缀', '身份', '分工组', '加了多少行', '例词'], rows_aff, [9, 80, 12, 12, 50])
    sheet(wb, '词缀分工组', ['分工组', '分工那句话', '用到的行数'], rows_grp, [12, 150, 12])
    sheet(wb, '同义词组', ['中文意思', '词性', '词数', '总表里的词'], rows_syn, [18, 8, 7, 110])
    sheet(wb, '辨析补来的', ['行号', '单词', '【同义词】行', '从同组别的词那一行补来的话'], rows_fill, [7, 16, 50, 110])
    sheet(wb, '辨析待补', ['行号', '单词', '【同义词】行', '现在的辨析文字（没提到同组的词）'], rows_todo, [7, 16, 50, 110])
    wb.save(dst)
    print('清单存好了：词根列 %d、合起来 %d、其他列 %d、词根族 %d、词缀身份 %d、同义词组 %d、补来 %d、待补 %d' % (len(rows_root), len(rows_hq), len(rows_other), len(rows_fam), len(rows_aff), len(rows_syn), len(rows_fill), len(rows_todo)))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

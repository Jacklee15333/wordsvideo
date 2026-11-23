"""合成规律体检（2026-11 合成规律轮）：组合列（N）里的“　合成规律：”“　写法：”两种行。

  python3 hecheng_check.py <xlsx>                    # 各类数目（正常基线见 references/audit_checklist.md）
  python3 hecheng_check.py <xlsx> --show comp_missing 30
  python3 hecheng_check.py <xlsx> --fix-sheet <新.xlsx>   # 按全表重算「合成规律一览」的词数、前 40 个词（加了新词以后跑）

写法（writing_guide.md 第 11 节）：第一行【构词逻辑】（有后缀等式的接在等式后面）下面，先写合成规律（每条一行），再写一行写法：
  　合成规律：规律那句话（本词：短语 → 本词；同 例词）
  　写法：规律那句话（本词的例子、别的写法、历史）
规律那句话照 hecheng_catalog.py（=「合成规律一览」）一字不改：视频技能 3.7 照它念、照它认是哪一条。
"""
import re, sys, os
from collections import OrderedDict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openpyxl import load_workbook
import cols as C
import columns as COL
from hecheng_catalog import RULES

TEXT = {(r[1], r[2]): r[0] for r in RULES}
LINE = re.compile(r'^\s*(合成规律|写法)[：:]\s*(.*)$')
WRITE_KW = re.compile(r'连字符|连写|分开写|分写|拆开写|合写')
CATS = OrderedDict([
    ('comp_missing', '③ 合成词没有“合成规律”行（缩写 wouldn\'t 这类只写写法，不算）'),
    ('spell_missing', '③ 合成词或带连字符的词没有“写法”行'),
    ('spell_many', '“写法”写了不止一行（一个词只写一行）'),
    ('rule_unknown', '规律那句话不在 hecheng_catalog.py 里（措辞改了、打错了，视频认不出是哪一条）'),
    ('order_bad', '这两种行没紧跟在第一行（和后缀等式）下面，或者写法跑到了合成规律前面'),
    ('paren_bad', '这两种行里括号、引号不配对'),
    ('plus_minus', '这两种行里有“+ -”（会被当成后缀等式读走，写成“再加 -ed”）'),
    ('no_body', '规律后面没有括号里的本词例子（合成规律那一行一定要有）'),
    ('not_target', '不是合成词、也不带连字符的词写了这两种行'),
    ('write_scattered', '（参考）写法行以外还在讲连写、连字符的行（【语法】【辨析】、步骤括号、音变列），写法只写在写法那一行'),
    ('sheet_mismatch', '「合成规律一览」的词数和全表对不上（跑 --fix-sheet）'),
])


def rule_lines(N):
    L = str(N or '').split('\n')
    return [(i, m.group(1), m.group(2)) for i, l in enumerate(L) for m in [LINE.match(l)] if m]


def check(path):
    wb = load_workbook(path)
    ws = wb['拆分结果']
    found = {k: [] for k in CATS}
    use = {r[0]: [] for r in RULES}
    for r in range(2, ws.max_row + 1):
        w = str(ws.cell(r, C.WORD).value or '')
        typ = str(ws.cell(r, C.TYPE).value or '')
        N = str(ws.cell(r, C.COMBO).value or '')
        P = str(ws.cell(r, C.SOUND).value or '')
        target = typ.startswith('③') or '-' in w
        rl = rule_lines(N)
        add = lambda k, x='': found[k].append((r, w, x))
        if not target:
            if rl:
                add('not_target')
            continue
        comp = [x for x in rl if x[1] == '合成规律']
        spell = [x for x in rl if x[1] == '写法']
        if typ.startswith('③') and not comp and "'" not in w:
            add('comp_missing')
        if not spell:
            add('spell_missing')
        if len(spell) > 1:
            add('spell_many')
        L = N.split('\n')
        k = 1
        while k < len(L) and COL.sentence_from_eq(L[k]) and not COL.STEP.match(L[k]) and '+ -' in L[k]:
            k += 1
        idx = [i for i, _, _ in rl]
        if idx and (idx != list(range(k, k + len(idx))) or (spell and comp and max(i for i, _, _ in comp) > min(i for i, _, _ in spell))):
            add('order_bad', str(idx))
        for i, kind, body in rl:
            text = body.split('（', 1)[0].strip()
            rid = TEXT.get((kind, text))
            if not rid:
                add('rule_unknown', body[:40])
            else:
                if w not in use[rid]:
                    use[rid].append(w)
            if body.count('（') != body.count('）') or body.count('(') != body.count(')') or body.count('“') != body.count('”'):
                add('paren_bad', body[:40])
            if '+ -' in body:
                add('plus_minus', body[:40])
            if kind == '合成规律' and '（' not in body:
                add('no_body', body[:40])
        others = [l for j, l in enumerate(L) if j not in idx and j > 0 and WRITE_KW.search(l)]
        if others or WRITE_KW.search(P):
            add('write_scattered', (others[0] if others else P)[:50])
    if '合成规律一览' in wb.sheetnames:
        H = wb['合成规律一览']
        for rr in range(2, H.max_row + 1):
            rid = H.cell(rr, 2).value
            if rid in use and int(H.cell(rr, 7).value or 0) != len(use[rid]):
                found['sheet_mismatch'].append((rr, rid, '表里 %s，全表 %d' % (H.cell(rr, 7).value, len(use[rid]))))
    else:
        found['sheet_mismatch'].append((0, '合成规律一览', '没有这张表'))
    return wb, found, use


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    wb, found, use = check(a[0])
    if '--fix-sheet' in a:
        out = a[a.index('--fix-sheet') + 1]
        H = wb['合成规律一览']
        for rr in range(2, H.max_row + 1):
            rid = H.cell(rr, 2).value
            if rid in use:
                H.cell(rr, 7).value = len(use[rid])
                H.cell(rr, 8).value = '、'.join(use[rid][:40])
        wb.save(out)
        print('「合成规律一览」已按全表重算：' + out)
        return
    if '--show' in a:
        k = a[a.index('--show') + 1]
        n = int(a[a.index('--show') + 2]) if len(a) > a.index('--show') + 2 else 40
        for x in found[k][:n]:
            print('  第 %s 行  %s  %s' % x)
        return
    print('合成规律体检')
    for k, desc in CATS.items():
        print('  %-16s %5d  %s' % (k, len(found[k]), desc))
    print('  用到各条规律的词数：' + '，'.join('%s %d' % (r, len(v)) for r, v in use.items()))


if __name__ == '__main__':
    main()

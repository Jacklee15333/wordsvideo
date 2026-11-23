# -*- coding: utf-8 -*-
"""2026-11 例词清理轮的改表脚本（只作记录；以后同类的事直接用 lizi.py）。
  python3 round.py <原表.xlsx> <新表.xlsx>     全表试算 + 写回（xlsx_write.write）+ 读回来和“原表 + 改动”逐格比
  python3 round.py <原表.xlsx> --dry            只试算，打印各步改了多少格
顺序：① 前缀列、后缀列：去掉“同 …”里的复杂例词、指到同词缀别的词的“见 X”、个别改写（lizi.plan_affix）
      ② 词根列：补上一轮漏掉的复杂例词（lizi.plan）
别的列一格不动；身份分工、记法、动词变化这几段不动。"""
import os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
import linetools as LT
import lizi as LZ
import xlsx_write as XW


def run(src):
    hdr, C, data = LT.load_table(src)
    W = [list(r) for r in data]
    log = collections.OrderedDict()
    cells, alog = LZ.plan_affix(W, C)
    for (ri, col), v in cells.items(): W[ri][C[col]] = v
    log['前缀列'] = sum(1 for k in cells if k[1] == 'pre'); log['后缀列'] = sum(1 for k in cells if k[1] == 'suf')
    o, rlog = LZ.plan(W, C)
    for ri, v in o.items(): W[ri][C['root']] = v
    log['词根列'] = len(o)
    changes = {}
    for ri, (a, b) in enumerate(zip(data, W)):
        for ci in range(len(a)):
            if (a[ci] or None) != (b[ci] or None): changes[(ri + 2, ci)] = b[ci] if b[ci] is not None else ''
    return hdr, C, data, W, changes, log, alog, rlog


if __name__ == '__main__':
    src = sys.argv[1]
    hdr, C, data, W, changes, log, alog, rlog = run(src)
    for k, v in log.items(): print('%s：%d 格' % (k, v))
    n = collections.Counter()
    for ri, w, col, lab, what, xs, line, nl in alog: n[(col, what)] += len(xs)
    print('词缀行：去掉例词 前缀 %d、后缀 %d；去掉“见” %d；改写 %d' % (n[('pre', '例词')], n[('suf', '例词')], n[('pre', '见')] + n[('suf', '见')], n[('pre', '改写')] + n[('suf', '改写')]))
    print('词根列：去掉例词 %d' % sum(len(x[2]) for x in rlog))
    print('合计改动 %d 格（%d 行）；按列：%s' % (len(changes), len({r for r, c in changes}), dict(collections.Counter(hdr[c] for r, c in changes))))
    # 再跑一遍不变
    c2, a2 = LZ.plan_affix(W, C); o2, r2 = LZ.plan(W, C)
    print('再跑一遍：词缀 %d 格、词根 %d 格（都应为 0）' % (len(c2), len(o2)))
    if '--dry' in sys.argv: sys.exit(0)
    dst = sys.argv[2]
    XW.write(src, dst, changes)
    h2, C2, d2 = LT.load_table(dst)
    bad = 0
    for ri, (a, b) in enumerate(zip(W, d2)):
        for ci in range(len(a)):
            x, y = (a[ci] if a[ci] not in ('',) else None), (b[ci] if b[ci] not in ('',) else None)
            if isinstance(x, float) and x == int(x): x = int(x)
            if isinstance(y, float) and y == int(y): y = int(y)
            if x != y:
                bad += 1
                if bad <= 5: print('不一致', ri + 2, hdr[ci], repr(x)[:60], repr(y)[:60])
    print('读回来和“原表 + 改动”逐格比：%d 处不一致（行数 %d / %d）' % (bad, len(W), len(d2)))

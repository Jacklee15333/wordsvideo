# -*- coding: utf-8 -*-
"""2026-11 词缀来历、记法轮的改表脚本（只作记录；以后同类的事用 laili.py、lizi.py、part_memo.py、dongbian.py）。
  python3 round.py <原表.xlsx> <新表.xlsx>            全表试算 + 写回（xlsx_write.write）+ 读回来和“原表 + 改动”逐格比
  python3 round.py <原表.xlsx> --dry                   只试算，打印各步改了多少格
顺序：① 动词变化（dongbian_data 的 cut：原形去掉词尾就是词根；规律里去掉复杂例词）
      ② 词根列的复杂例词（lizi.py）
      ③ 记法：换掉 geo / bio / vac / logue 四个“拿含有同一个词根的词来记”的（geography、biology、vacation、dialogue），补新的（part_memo_data 新加的 gen、mon、the、ly 和早就有、没写上的）
      ④ 「词根变体处理」列：补上了记法的行去掉“记法待补：…”
      ⑤ 前缀、后缀列：来历换成目录里的一句、补来历、加记法（laili.py）"""
import os, sys, re, collections, copy, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
import linetools as LT
import dongbian as DB
import lizi as LZ
import laili as LL
import part_memo as PM
import xlsx_write as XW
import cizhui as CZ

OLD_ANCHORS = {'geography', 'biology', 'vacation', 'dialogue'}
COLS = {'pre': '前缀', 'root': '词根', 'suf': '后缀'}


def strip_old_memo(line):
    m = PM.MEMO_RX.search(line)
    if m and m.group(3).strip() in OLD_ANCHORS:
        return line[:m.start()].rstrip('；;，, ')
    return line


def memo_pass(W, C):
    """part_memo.plan 的内存版：-> {(行, 列): 新格}, 统计"""
    out, stat = {}, collections.Counter()
    for ri, r in enumerate(W):
        word = str(r[C['word']] or '')
        for col, name in COLS.items():
            v = r[C[col]]
            if not v or str(v).strip() in ('-', '—'): continue
            ls = str(v).split('\n'); new = []; ch = False
            for ln in ls:
                l0 = strip_old_memo(ln)
                if l0 != ln: ch = True; stat['去掉旧记法'] += 1
                m = PM.HEAD.match(l0)
                core = PM.core_of(m.group(1)) if m else ''
                if not core or '记：' in l0 or (col != 'root' and core not in PM.ALLOW[name]):
                    new.append(l0); continue
                hit = PM.pick(core, m.group(2), word)
                if not hit:
                    new.append(l0); continue
                i, inh = hit
                base = l0.rstrip().rstrip('。；;')
                new.append(base + '；' + PM.memo_text(PM.root_of(m.group(2)) or core if inh else core, i))
                ch = True; stat['加记法 ' + PM.R[i][3]] += 1
            if ch: out[(ri, col)] = '\n'.join(new)
    return out, stat


def run(src):
    hdr, C, data = LT.load_table(src)
    W = [list(r) for r in data]
    log = collections.OrderedDict()
    # ① 动词变化
    o, st = DB.plan(W, C)
    for ri, v in o.items(): W[ri][C['root']] = v
    log['动词变化（词根列）'] = len(o)
    # ② 复杂例词
    o, lz = LZ.plan(W, C)
    for ri, v in o.items(): W[ri][C['root']] = v
    log['复杂例词（词根列）'] = len(o)
    # ③ 记法
    o, st = memo_pass(W, C)
    for (ri, col), v in o.items(): W[ri][C[col]] = v
    log['记法（词根列等）'] = len(o)
    memo_rows = {ri for (ri, col) in o}
    # ④ 记法待补
    n = 0
    for ri in memo_rows:
        var = str(W[ri][C['var']] or '')
        if '记法待补' not in var: continue
        root = str(W[ri][C['root']] or '')
        m = re.search(r'记法待补：([A-Za-z]+)', var)
        if m and re.search(r'记：\s*' + m.group(1) + r'\b', root):
            nv = re.sub(r'[；;]?\s*记法待补：[^；;]*', '', var).strip('；; ')
            W[ri][C['var']] = nv or None; n += 1
    log['记法待补去掉'] = n
    # ⑤ 词缀来历、记法
    o, lstat, miss = LL.plan(W, C)
    for (ri, col), v in o.items(): W[ri][C[col]] = v
    log['词缀来历、记法（前缀、后缀列）'] = len(o)
    # ⑥ 身份、分工：来历换了以后 cizhui 新认得出的行（shepherdess 的 -ess）补上
    o, cst, cmiss = CZ.plan(W, C)
    for ri, res in o.items():
        for col, v in res.items(): W[ri][C[col]] = v
    log['补身份、分工'] = len(o)
    changes = {}
    for ri, (a, b) in enumerate(zip(data, W)):
        for ci in range(len(a)):
            if (a[ci] or None) != (b[ci] or None): changes[(ri + 2, ci)] = b[ci] if b[ci] is not None else ''
    return hdr, C, data, W, changes, log, st, lz, lstat, miss


if __name__ == '__main__':
    src = sys.argv[1]
    hdr, C, data, W, changes, log, st, lz, lstat, miss = run(src)
    for k, v in log.items(): print('%s：%d 格' % (k, v))
    print('合计改动 %d 格（%d 行）' % (len(changes), len({r for r, c in changes})))
    print('按列：', dict(collections.Counter(hdr[c] for r, c in changes)))
    print('记法：', dict(st))
    if '--dry' in sys.argv: sys.exit(0)
    dst = sys.argv[2]
    XW.write(src, dst, changes)
    # 读回来逐格比
    h2, C2, d2 = LT.load_table(dst)
    bad = 0
    for ri, (a, b) in enumerate(zip(W, d2)):
        for ci in range(len(a)):
            x, y = (a[ci] if a[ci] not in ('',) else None), (b[ci] if b[ci] not in ('',) else None)
            if isinstance(x, float) and x == int(x): x = int(x)
            if isinstance(y, float) and y == int(y): y = int(y)
            if str(x) != str(y) if x is not None or y is not None else False:
                bad += 1
                if bad < 5: print('不一致', ri + 2, hdr[ci], repr(x)[:60], repr(y)[:60])
    print('读回来逐格比：不一致 %d' % bad)
    json.dump({'%d,%d' % k: v for k, v in changes.items()}, open(dst + '.changes.json', 'w', encoding='utf-8'), ensure_ascii=False)

# -*- coding: utf-8 -*-
"""2026-11 身份分工、辨析列轮的改表脚本（只作记录；再用时先读 ../../shenfen.py、cizhui.py、bianxi.py 的说明）。
  python3 round.py plan  <原表.xlsx>                 # 只在内存里算，打印统计
  python3 round.py write <原表.xlsx> <新表.xlsx>      # 写出 17 列的新表（多一列「辨析」）和传输包
做四件事（先后有讲究）：
  1. 词根列：手工的几处（manual.py）→ shenfen.plan 切链、加身份分工、收集“合起来”；前缀列补“这里是”
  2. 前缀、后缀列：cizhui.plan 加身份、分工
  3. 辨析列：组合列的【辨析】整段挪到新列，前面加算出来的【同义词】行；别处的“见【辨析】”改成“见辨析列”
  4. 组合列第一行下面插“　合起来：”"""
import sys, os, pickle, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..')); sys.path.insert(0, HERE)
import linetools as LT, shenfen, cizhui, bianxi as B, manual as MN
import columns as CO

NEWCOL = '辨析'
def insert_heqi(combo, items):
    """组合格第一行（和它下面的后缀等式、构词 / 合成规律 / 写法行）后面插一行“　合起来：…”"""
    if not items: return combo
    lines = str(combo or '').split('\n')
    if not lines or not lines[0].startswith('【构词逻辑】'): return None
    k = 1
    while k < len(lines) and (lines[k].startswith('\u3000') or (CO.sentence_from_eq(lines[k]) and not CO.STEP.match(lines[k]))): k += 1
    text = '；'.join(x.strip().rstrip('。；') for x in items)
    lines.insert(k, '\u3000合起来：' + text)
    return '\n'.join(lines)

def compute(src):
    hdr, C, data = LT.load_table(src)
    assert 'bx' not in C, '这张表已经有辨析列了：这个脚本是给 16 列的老表用的'
    stat = collections.Counter()
    new = [list(r) for r in data]
    heqi = collections.defaultdict(list)
    widx = {}
    for i, r in enumerate(new): widx.setdefault(r[C['word']], i)
    for w, patches in MN.ROOT_PATCH.items():
        i = widx[w]
        for old, rep, hq in patches:
            assert old in new[i][C['root']], (w, old)
            new[i][C['root']] = new[i][C['root']].replace(old, rep); heqi[i].append(hq); stat['手工：词根行里的整合'] += 1
    for w, (old, rep, hq) in MN.PRE_PATCH.items():
        i = widx[w]; assert old in new[i][C['pre']], w
        new[i][C['pre']] = new[i][C['pre']].replace(old, rep); heqi[i].append(hq); stat['手工：前缀行里的整合'] += 1
    for w in MN.WP_MOVE:
        i = widx[w]; keep = []
        for l in str(new[i][C['wp']]).split('\n'):
            lab = LT.label_body(l)[0]
            h = shenfen.heqi_line(l, w) if lab is None or not re.match(r"^[-A-Za-z ]+$", lab or '') else None
            if h is None and re.match(r'^(古法语|中世纪拉丁语|拉丁语)\s', l): h = l
            if h is not None: heqi[i].append(h); stat['单词部分列里的“合起来”行'] += 1
            else: keep.append(l)
        new[i][C['wp']] = '\n'.join(keep) if keep else '-'
    plan, st = shenfen.plan(new, C)
    stat.update({'词根列：' + k: v for k, v in st.items()})
    for i, res in plan.items():
        w = new[i][C['word']]
        root = res['root']
        if w in MN.ROOT_AFTER:
            old, rep = MN.ROOT_AFTER[w]; assert old in root, w; root = root.replace(old, rep, 1)
        new[i][C['root']] = root
        hq = res['heqi']
        if w in MN.HEQI_FIX:          # 手工改的只替换从链里取出来的那些，整行挪过来的照旧
            moved = [h for h in res['heqi'] if any(h[:10] in l for l in str(data[i][C['root']]).split('\n'))]
            hq = moved + MN.HEQI_FIX[w]
        heqi[i] += hq
        if res['pre'] and w not in MN.PRE_SKIP:
            pl = str(new[i][C['pre']]).split('\n')
            for lab, gl in res['pre'].items():
                for k, l in enumerate(pl):
                    if LT.label_body(l)[0] == lab:
                        pl[k] = l.rstrip('；。') + '；这里是“%s”' % gl; stat['前缀列：补“这里是”'] += 1
            new[i][C['pre']] = '\n'.join(pl)
    ap, st2, miss = cizhui.plan(new, C)
    for i, res in ap.items():
        for col, t in res.items(): new[i][C[col]] = t
    stat['词缀行：加身份、分工'] = sum(st2.values())
    idx, terms = B.build_index(data, C); words = {r[C['word']] for r in data}
    bcol = []
    for i, r in enumerate(new):
        combo2, bx = B.split_bianxi(r[C['combo']])
        w = r[C['word']]
        if w in MN.BIANXI:
            cell = MN.BIANXI[w]; stat['辨析列：手写样板'] += 1
        else:
            sl = B.syn_lines(w, bx, idx, terms, words)
            cell = '\n'.join(sl + ([bx] if bx else []))
            if sl: stat['辨析列：有【同义词】行的'] += 1
        if bx: stat['辨析列：从组合列挪来的'] += 1
        if '【辨析】' in combo2: stat['组合列：“见【辨析】”改成“见辨析列”'] += 1
        new[i][C['combo']] = B.fix_refs(combo2)
        for col in ('bg', 'suf', 'wp', 'pre', 'root', 'snd'):
            t = r[C[col]]
            if t and '【辨析】' in t: new[i][C[col]] = B.fix_refs(t); stat['别的列：“【辨析】”改成“辨析列”'] += 1
        bcol.append(cell or None)
    bcol2, nfill = B.cross_fill([c or '' for c in bcol], [r[C['word']] for r in new])
    bcol = [c or None for c in bcol2]; stat['辨析列：从同组别的词那一行补来辨析的'] = nfill
    for i, items in heqi.items():
        items = [x for x in items if x]
        if not items: continue
        c2 = insert_heqi(new[i][C['combo']], items)
        if c2 is None:
            print('!! 组合列不是【构词逻辑】开头，合起来没处放：', new[i][C['word']], items); continue
        new[i][C['combo']] = c2; stat['组合列：加“合起来”行'] += 1
    k = C['combo'] + 1
    hdr2 = hdr[:k] + [NEWCOL] + hdr[k:]
    table = [hdr2] + [[v if isinstance(v, str) else None for v in (r[:k] + [bcol[i]] + r[k:])] for i, r in enumerate(new)]
    chg = collections.Counter(); rows_changed = 0
    for i, (a, b) in enumerate(zip(data, new)):
        ch = False
        for name, j in C.items():
            if (a[j] or None) != (b[j] or None): chg[name] += 1; ch = True
        if ch or bcol[i]: rows_changed += 1
    print('各列改动的格数：', dict(chg), '| 辨析列有内容', sum(1 for x in bcol if x), '| 涉及行', rows_changed)
    for kx, v in sorted(stat.items()): print('  %s: %d' % (kx, v))
    return dict(hdr=hdr2, table=table, old=data, new=new, bcol=bcol, C=C, heqi=dict(heqi), plan=plan, k=k)

if __name__ == '__main__':
    mode, src = sys.argv[1], sys.argv[2]
    d = compute(src)
    pickle.dump(d, open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[3] if mode == 'write' else src)), 'round_shenfen.pkl'), 'wb'))
    if mode == 'write':
        import xlsx_write as XW
        XW.rebuild(src, sys.argv[3], d['table'], new_cols={d['k']: (62, d['C']['combo'])})

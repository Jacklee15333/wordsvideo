"""拼写变化体检（2026-11 拼写变化轮）：加词缀时拼写变了的，那个词缀那一行要说明；双写的字母单独写一部分。

  python3 pinxie_check.py <xlsx>                     # 各类数目（应为 0）
  python3 pinxie_check.py <xlsx> --show missing 40

现象和说明的写法见 writing_guide.md 第 12 节、project_rules.md 第 53 条；认现象的规则在 pinxie.py（去 e、留 e 读软音、y 变 i、y 去掉、双写、-le 变 -ly、-ble 变 -bil-、
-le 变 -ul-、-nt 变 -nce / -ncy、-ate 变 -acy、-ous 变 -osity、-fy 变 -fication、-er 去 e、-or / -er 加 -ess、去掉末尾元音、d(e) 变 s / t、t 变 ss、-ceive / -scribe / -tain / -sume / -solve 的名词、ai 变 a、元音变……）。
拉丁语、法语词干本身就不一样的（repeat → repetition）认不出来，不报。"""
import json, re, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pinxie import norm, labels, classify, DONE, V, STRESS_FINAL
from openpyxl import load_workbook
import cols as C
if len(sys.argv) < 2:
    print(__doc__); sys.exit(0)
_ws = load_workbook(sys.argv[1], read_only=True)['拆分结果']
rows = []
for _i, _r in enumerate(_ws.iter_rows(min_row=2, values_only=True), start=2):
    g = lambda c: str(_r[c - 1] or '')
    rows.append({'row': _i, 'w': g(C.WORD), 'typ': g(C.TYPE), 'I': g(C.SPLIT), 'J': g(C.PRE), 'K': g(C.ROOT), 'L': g(C.WPART), 'M': g(C.SUF)})
plan = []          # (row, word, kind, col, line_index, note)
MULTI = []; NOTM = []
splitfix = {}      # row -> new I
stats = collections.Counter(); done = collections.Counter(); nolab = []
for d in rows:
    if d['typ'].startswith(('④', '⑤')): continue
    I0 = d['I'].split('；')[0]
    if ' + ' not in I0: continue
    head = ''
    if '← ' in I0:
        head, I0 = I0.rsplit('← ', 1); head += '← '
    raw = [p.strip() for p in I0.split(' + ')]
    parts = [norm(p) for p in raw]
    w = d['w']; wl = w.lower().replace('-', '').replace("'", '').replace(' ', '')
    LB = labels(d)
    pos = 0; newraw = list(raw); inserted = 0
    for i in range(len(parts) - 1):
        prev, nxt = parts[i], parts[i + 1]
        rest = wl[pos:]
        # 双写写进后缀里的（fun + ny）：拆成 fun + n + y
        if len(nxt) >= 2 and nxt[0] == prev[-1:] and nxt[0] not in V and nxt[1:] in LB and LB[nxt[1:]][0] == 'M' and rest.startswith(prev + nxt):
            j = i + 1 + inserted
            newraw[j:j + 1] = [nxt[0], raw[i + 1][1:]]
            inserted += 1
            kind, p2 = 'double', prev
            sufl = nxt[1:]
        elif len(raw[i + 1]) == 1 and raw[i + 1] == raw[i][-1:] and raw[i + 1] not in V:
            kind, p2 = 'double', prev; sufl = parts[i + 2] if i + 2 < len(parts) else ''
            pos += len(prev); continue_flag = True
        else:
            kind, res = classify(prev, nxt, rest, w, raw[i])
            sufl = nxt
            if kind is None:
                pos += len(res); continue
            if kind == 'other':
                stats['other'] += 1; break
            p2, note = res
            if kind == 'double_hidden':
                j = i + 1 + inserted
                newraw[j:j] = [prev[-1]]
                if newraw[j - 1].endswith('(%s)' % prev[-1]): newraw[j - 1] = newraw[j - 1][:-3]
                inserted += 1
                kind = 'double'
        if kind == 'double':
            # 双写的说明
            c = prev[-1]
            base = raw[i]
            us = None
            nsyl = len(re.findall(r'[aeiouy]+', prev))
            if prev == 'wool':
                note = 'woolly 的 l 双写是习惯写法（wool 不是“一个元音字母 + 一个辅音字母”结尾；美式也写 wooly）'
            elif prev == 'jewel' and sufl == 'ery':
                note = '英式 jewel 加 -ery 时 l 双写：jewellery；美式写 jewelry（l 不双写，连 e 也去掉）'
            elif prev == 'cancel':
                note = 'cancel 加 -ation 英美都多写 cancellation（l 双写；美式偶尔写 cancelation）'
            elif prev == 'metal':
                note = 'metal 加 -ic 时 l 双写：metallic（照拉丁语 metallicus，英美都这样写）'
            elif c == 'l' and re.search(r'[aeiou]l$', prev) and prev not in STRESS_FINAL and nsyl >= 2:
                note = '英式 %s 末尾的 l 加元音开头的 -%s 都双写（%s），美式重音不在最后一个音节时不双写（%s）' % (base, sufl, w, w.replace('ll', 'l', 1))
            elif prev in ('program',):
                note = 'program 重音在前，按规矩不用双写，可 programming、programmer、programmable 习惯双写 m'
            elif prev in STRESS_FINAL or nsyl >= 2:
                note = '%s 重音在最后一个音节，又以“一个元音字母 + 一个辅音字母”结尾，加元音开头的 -%s 时 %s 要双写：%s → %s' % (base, sufl, c, base, w)
                MULTI.append((w, base, sufl))
            else:
                note = '%s 以“一个元音字母 + 一个辅音字母”结尾，加元音开头的 -%s 时 %s 要双写：%s → %s（双写才能保住前面元音原来的读音，同 hop → hopping、hope → hoping）' % (base, sufl, c, base, w)
            p2 = prev if kind == 'double' else p2
        stats[kind] += 1
        if w == 'once': note = None
        if kind == 'drop_e_done' or note is None:
            pos += len(p2); continue
        lab = LB.get(sufl)
        if not lab:
            # 后缀行找不到时，写在前一部分那一行
            lab = LB.get(prev)
        if not lab:
            nolab.append((w, kind, sufl)); pos += len(p2); continue
        col, li = lab
        if col != 'M':
            NOTM.append((w, kind, col, sufl)); pos += len(p2); continue
        line = d[col].split('\n')[li]
        # “同 …”里去掉本词自己
        def dedupe(m):
            keep = [x for x in m.group(2).split('、') if not x.strip().endswith(' ' + w)]
            return (m.group(1) + '同 ' + '、'.join(keep) + '）') if keep else ('）' if m.group(1) != '（' else '')
        note = re.sub(r'([（，；])同 ([^（）]*)）', dedupe, note)
        if DONE.search(line):
            done[kind] += 1
        else:
            plan.append((d['row'], w, kind, col, li, note))
        pos += len(p2)
    if inserted:
        newI = head + ' + '.join(newraw)
        alts = d['I'].split('；'); alts[0] = newI
        splitfix[d['row']] = '；'.join(alts)
CATS = {'missing': '加词缀时拼写变了（去 e、y 变 i、双写、-le 变 -ly、-nt 变 -nce……），那个词缀那一行没说明',
        'double_in_suffix': '双写的字母写进了后缀（swim + ming、fun + ny），应写成 swim + m + ing',
        'double_hidden': '双写的字母没写出来（forget + able），应写成 forget + t + able'}
found = {'missing': [(x[1], x[2], x[5][:40]) for x in plan], 'double_in_suffix': [], 'double_hidden': []}
rr = {d['row']: d for d in rows}
for r_, I in splitfix.items():
    k = 'double_hidden' if any(len(p.strip()) == 1 for p in I.split(' + ')) and not re.search(r' \+ [a-z]{2,} \+', rr[r_]['I']) and len(I.split(' + ')) > len(rr[r_]['I'].split(' + ')) and not any(p.strip()[:1] == p.strip()[1:2] for p in rr[r_]['I'].split(' + ')[1:]) else 'double_in_suffix'
    found[k].append((rr[r_]['w'], rr[r_]['I'], I))
a = sys.argv[2:]
if '--show' in a:
    k = a[a.index('--show') + 1]; n = int(a[a.index('--show') + 2]) if len(a) > a.index('--show') + 2 else 40
    for x in found[k][:n]: print('  %s  %s  %s' % x)
else:
    print('拼写变化体检')
    for k, d in CATS.items(): print('  %-18s %5d  %s' % (k, len(found[k]), d))
    print('  （参考）各类现象：' + '，'.join('%s %d' % kv for kv in sorted(stats.items(), key=lambda x: -x[1])))

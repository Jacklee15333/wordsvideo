"""在三列上做：挪列、词根加连字符 → {行: (前缀, 词根, 后缀, [说明])}"""
import re, pickle, sys, collections
sys.path.insert(0, '/home/claude/work4'); sys.path.insert(0, '/home/claude/skills_new/maintain/etymology-table/scripts')
import cols as C
from decide import *
rows = pickle.load(open('/home/claude/rows4.pkl', 'rb'))
words = {str(r[4]).strip().lower() for r in rows[1:]}
lines_of = lambda v: [] if str(v or '').strip() in ('', '-') else str(v).split('\n')
out, stat = {}, collections.Counter()
def take(lines, label):
    for k, l in enumerate(lines):
        if C.label_of(l) == label:
            return lines.pop(k)
    raise SystemExit(f'找不到 {label}')
for i, r in enumerate(rows[1:], start=2):
    w, typ, split = str(r[4]), str(r[7] or ''), r[8]
    pre, root, suf = lines_of(r[9]), lines_of(r[10]), lines_of(r[11])
    notes = []
    if i in PRE_TO_ROOT:
        l = take(pre, PRE_TO_ROOT[i]); root.insert(0, l); notes.append(f'{PRE_TO_ROOT[i]} 从前缀列挪到词根列（构词成分，算词根）'); stat['pre_to_root'] += 1
    if i in SUF_TO_ROOT:
        l = take(suf, SUF_TO_ROOT[i]); root.append(l); notes.append(f'{SUF_TO_ROOT[i]} 从后缀列挪到词根列（构词成分，算词根）'); stat['suf_to_root'] += 1
    for (rn, lab) in TO_PRE:
        if rn == i:
            l = take(root, lab); pre.append(l.replace(lab, lab + '-', 1)); notes.append(f'{lab} 是前缀，从词根列挪到前缀列（写作 {lab}-）'); stat['to_pre'] += 1
    for (rn, lab) in TO_SUF:
        if rn == i:
            l = take(root, lab); suf.insert(0, l.replace(lab, '-' + lab, 1)); notes.append(f'{lab} 是后缀，从词根列挪到后缀列（写作 -{lab}）'); stat['to_suf'] += 1
    hy = []
    new_root = []
    for l in root:
        t = C.label_of(l)
        if t and C.is_part_label(t) and not t.startswith('为什么'):
            body = l.split('：', 1)[1] if '：' in l else ''
            d = root_decision(i, w, typ, split, t, body, words)
            if d == 'bound':
                where = C.split_positions(split)[C._norm(t)]
                nt = {'first': t + '-', 'last': '-' + t, 'mid': '-' + t + '-'}[where]
                l = l.replace(t, nt, 1); hy.append(nt); stat['hyph'] += 1
            elif d == 'free': stat['free'] += 1
        new_root.append(l)
    if hy: notes.append('词根加连字符：' + '、'.join(hy))
    f = lambda xs: '\n'.join(xs) if xs else '-'
    out[i] = (f(pre), f(new_root), f(suf), notes)
    if notes: stat['rows_changed'] += 1
pickle.dump(out, open('/home/claude/work4/new_cells.pkl', 'wb'))
print(dict(stat))
for i in (5347, 1552, 279, 5460, 21, 2154, 8, 1462, 523):
    p, ro, s, n = out[i]
    print('==', i, rows[i-1][4], '|', rows[i-1][8]); print('  前缀:', p[:80].replace('\n', ' ⏎ ')); print('  词根:', ro[:120].replace('\n', ' ⏎ ')); print('  后缀:', s[:80].replace('\n', ' ⏎ ')); print('  ', n)

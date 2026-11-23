"""单词列轮：词根列每一行分到 词根 / 单词部分（/ 前缀），算出新的 J、K、L(单词部分)、M(后缀) 四格和 T 列记录"""
import pickle, re, sys, collections
sys.path.insert(0, '/home/claude/orig/etymology-table/scripts')
import cols as C
from decisions import DEC
d = pickle.load(open('/home/claude/src_vals.pkl', 'rb'))
rows = d['拆分结果']
E = C.EMPTY
CJK = re.compile(r'[\u3400-\u9fff]')
CONNECT = {('nightingale', '-in-'), ('delight', '-gh-')}

def lines_of(v):
    return [l for l in str(v or '').split('\n') if l.strip() and l.strip() not in (E, '—')]

def line_kind(l):
    t = C.label_of(l)
    if not t: return 'note', None
    if t.startswith('为什么'): return 'why', t
    if not C.is_part_label(t): return 'note', t
    base = re.sub(r'（[^（）]*）|\([^()]*\)', '', t)
    if CJK.search(base) or ' → ' in base: return 'note', t
    return 'part', t

hy = lambda t: t.startswith('-') or t.endswith('-')
def connector(t, w): return len(re.sub(r'[^A-Za-zāæþðēīōūÆǣ]', '', t.strip('-'))) == 1 or (w, t) in CONNECT

used = set()
def override(r, l, t):
    if t is not None and (r, t) in DEC:
        used.add((r, t)); return DEC[(r, t)]
    for (rr, k), v in DEC.items():
        if rr == r and k.endswith('*') and l.lstrip().startswith(k[:-1]):
            used.add((rr, k)); return v
    if t == 'pea' and '孔雀' in l:
        return ('R', 'pea-')
    return None

def relabel(l, t, new):
    i = l.index(t)
    return l[:i] + new + l[i + len(t):]

def norm_line(l):
    """比对用：去掉标签两头的连字符"""
    t = C.label_of(l)
    if t and C.is_part_label(t) and not t.startswith('为什么') and t.strip('-') and t.strip('-') != t:
        return relabel(l, t, t.strip('-')).strip()
    return l.strip()

out, st, review = {}, collections.Counter(), []
for r, row in enumerate(rows[1:], start=2):
    w, typ, J, K, Lsuf = str(row[4] or ''), str(row[7] or ''), row[9], row[10], row[11]
    base_word = typ.startswith(('⑤', '④'))
    items = []
    for l in lines_of(K):
        kind, t = line_kind(l)
        ov = override(r, l, t)
        act, new = (ov if ov else (None, None))
        if act is None:
            if base_word: act = 'W'
            elif kind == 'part': act = 'R' if hy(t) else 'W'
        items.append([l, kind, t, act, new])
    real_root = any(a == 'R' and k == 'part' and not connector(t, w) for l, k, t, a, n in items)
    for it in items:
        if it[3] is None: it[3] = 'R' if real_root else 'W'
    pre, root, word, note = lines_of(J), [], [], collections.defaultdict(list)
    notes_w = False
    for l, kind, t, act, new in items:
        if act == 'W':
            if t and kind == 'part' and hy(t):
                l2 = relabel(l, t, t.strip('-')); note['wfix'].append(t.strip('-')); st['W_from_bound'] += 1
            else: l2 = l
            word.append(l2)
            if kind == 'part': note['w'].append(re.sub(r'[（(].*$', '', t.strip('-')).strip() or t)
            else: notes_w = True
        elif act == 'R':
            l2 = relabel(l, t, new) if (new and t and new != t) else l
            if new and t and new != t: note['rfix'].append(new); st['R_from_free'] += 1
            root.append(l2)
        elif act == 'P':
            l2 = relabel(l, t, new) if (new and t and new != t) else l
            pre.append(l2); note['p'].append(new or (t if kind == 'part' else '讲前缀的说明')); st['P'] += 1
    # 词根列一行都没剩、只剩连接成分的，“讲整个词”的说明已经跟着单词走了
    f = lambda xs: '\n'.join(xs) if xs else E
    newJ, newK, newL = f(pre), f(root), f(word)
    oldJ = str(J) if J is not None else E
    # 合起来的内容必须和原来一样（只看标签两头的连字符以外）
    old_lines = collections.Counter(norm_line(x) for x in C.combine(J, K, Lsuf).split('\n') if x.strip())
    new_lines = collections.Counter(norm_line(x) for x in C.combine(newJ, '\n'.join([newK if newK != E else '', newL if newL != E else '']).strip() or E, Lsuf).split('\n') if x.strip())
    if old_lines != new_lines:
        st['content_changed'] += 1
        if st['content_changed'] <= 5: print('!! 内容变了', r, w, old_lines - new_lines, new_lines - old_lines)
    parts = []
    if note['w']:
        ws_ = list(dict.fromkeys(note['w']))
        parts.append('、'.join(ws_[:6]) + (f' 等 {len(ws_)} 个' if len(ws_) > 6 else '') + ' 是单词，从词根列挪到单词部分' + ('（讲来历的说明一起挪）' if notes_w else ''))
    elif notes_w:
        parts.append('讲来历的说明从词根列挪到单词部分')
    if note['wfix']: parts.append('、'.join(note['wfix']) + ' 是能单独用的英语单词，去掉连字符')
    if note['rfix']: parts.append('、'.join(note['rfix']) + ' 不是英语单词，改算词根、加连字符')
    if note['p']: parts.append('、'.join(x for x in note['p']) + ' 挪到前缀列')
    tnote = ('单词列：' + '，'.join(parts)) if parts else ''
    out[r] = (newJ, newK, newL, tnote)
    st['rows_word'] += newL != E; st['rows_root'] += newK != E; st['rows_both'] += (newL != E and newK != E)
    st['rows_root_cleared'] += (newK == E and str(K or E) != E); st['rows_noted'] += bool(tnote)
    if newL != E and newK != E and any(k in ('note', 'why') for l, k, t, a, n in items):
        review.append((r, w, typ[:1], row[8], [(a, (t or l)[:28]) for l, k, t, a, n in items if k in ('note', 'why')],
                       [x[3] + ':' + (x[2] or '')[:12] for x in items if x[1] == 'part']))
missing = [k for k in DEC if k not in used]
print('没用上的判断：', missing)
print(dict(st))
pickle.dump((out, dict(st)), open('/home/claude/danci/new_cells.pkl', 'wb'))
for r in (2, 3, 4, 5, 9, 10, 140, 1346, 2401, 2104, 7191, 8337, 499):
    print('--', r, rows[r - 1][4], '|', out[r][0][:40].replace('\n', ' / '), '|K:', out[r][1][:60].replace('\n', ' / '), '|L:', out[r][2][:70].replace('\n', ' / '), '|T:', out[r][3])
print('==== 两样都有、还带说明的行：', len(review))
for x in review: print(x[0], x[1], x[2], x[3], '| 说明→', x[4], '| 部分:', ' '.join(x[5]))

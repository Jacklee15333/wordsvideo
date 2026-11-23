"""各部分解释（一格里好几行“标签：解释”）→ 前缀 / 词根 / 后缀 三列"""
import re, pickle, collections

CONNECT = {('significant', '-i-'), ('spokesman', '-s-'), ('nightingale', '-in-'), ('delight', '-gh-')}   # 两个词根中间的连接成分、拼写说明：放词根列

def label_of(line):
    m = re.match(r'^\s*([^：:]{1,60}?)[：:]', line)
    return m.group(1).strip() if m else None

def is_part_label(t):
    """部分的标签：英文字母、连字符、括号开头（re-、-ion、people、(uni)verse、no（形容词“没有”））；中文开头的是说明（注意、哪里变了、来历…）"""
    return bool(t) and bool(re.match(r'^[A-Za-z0-9āæþðēīōūÆǣ\(\-]', t))

def kind_of_label(t):
    if t.startswith('-') and t.endswith('-') and len(t) > 2: return 'infix'
    if t.startswith('-'): return 'suf'
    if re.match(r'^[A-Za-z]+(\([^)]*\))?-$', t) or (t.endswith('-') and not t.startswith('-')): return 'pre'
    return 'root'

AFFIX = re.compile(r'(?<![A-Za-z\-])(-[a-z]+-?|[a-z]+-)(?![A-Za-z])')

def first_affix(text, present):
    """“为什么用 -ar 不用 -al”：第一个提到的、本行拆分里有的词缀决定放哪一列"""
    for m in AFFIX.finditer(text):
        tok = m.group(1)
        if tok in present and present[tok] != 'root':
            return present[tok]
    return None

COLS = {'pre': 0, 'root': 1, 'suf': 2}

# 说明里提到了词缀、但讲的是整个词的来历（混血词、自己造的、同形词……）：放词根列
NOTE_ROOT = {('usage', '注意：不是 use'), ('princess', 'princess 是英语'), ('logo', '全称：很可能'), ('betray', '本族的 be-'),
             ('disorder', 'disorder 是英语'), ('since', '变化经过：'), ('difficult', '拉丁语原来的形容词'), ('painter', '注意：painter'),
             ('confused', '来历：这个词'), ('waver', 'waver 也能当'), ('automated', '来历：1952'), ('batter', '两种说法：'),
             ('urgency', '这个词很可能'), ('submarine', '英语自己用拉丁'), ('walnut', '古英语 walhhnutu'), ('horrify', '来源：可能是'),
             ('prayer', '另一个 prayer'), ('irony', '注意：另有一个'), ('Jewish', '今天的 Jewish'), ('mustard', '常见说法')}

def split_parts(word, H):
    """返回 ([前缀行], [词根行], [后缀行])，每行原样保留，列内保持原来的先后"""
    out = [[], [], []]
    lines = [l for l in str(H or '').split('\n') if l.strip()]
    labels = []
    for l in lines:
        t = label_of(l)
        labels.append(t if t and is_part_label(t) and not t.startswith('为什么') else None)
    present = {}           # 本行里出现的词缀标签 → 列
    for t in labels:
        if t:
            k = kind_of_label(t)
            if k == 'infix': k = 'root' if (word, t) in CONNECT else 'suf'
            present[t] = k
    prev = 'root'
    for l, t in zip(lines, labels):
        if t:                                   # 部分
            k = present[t]
        else:
            lab = label_of(l) or ''
            if lab.startswith('为什么'):         # “为什么用 -ar 不用 -al”：看第一个提到的词缀
                k = first_affix(lab, present) or 'root'
            else:                                # 说明：提到本行里的哪个前缀 / 后缀就放哪一列，不然放词根列
                hit = [present[x] for x in present if present[x] != 'root' and re.search(r'(?<![A-Za-z\-])' + re.escape(x) + r'(?![A-Za-z])', l)]
                k = hit[0] if hit else 'root'
                if any(word == w0 and l.strip().startswith(p0) for w0, p0 in NOTE_ROOT): k = 'root'
        out[COLS[k]].append(l)
        prev = k
    return out

def cells(word, H):
    a, b, c = split_parts(word, H)
    f = lambda xs: '\n'.join(xs) if xs else '-'
    return f(a), f(b), f(c)

def combine(pre, root, suf):
    """三列合回老的一格（前缀、词根、后缀的先后），给按老格式读的脚本、视频用"""
    out = []
    for x in (pre, root, suf):
        x = str(x or '').strip()
        if x and x not in ('-', '—'): out.append(x)
    return '\n'.join(out)

if __name__ == '__main__':
    rows = pickle.load(open('/home/claude/rows3.pkl', 'rb'))
    c = collections.Counter(); diff = []
    res = {}
    for i, r in enumerate(rows[1:], start=2):
        w, H = str(r[4]), str(r[9] or '')
        p, ro, s = cells(w, H)
        res[i] = (p, ro, s)
        comb = combine(p, ro, s)
        orig = '\n'.join(l for l in H.split('\n') if l.strip())
        if sorted(comb.split('\n')) != sorted(orig.split('\n')): c['lost'] += 1
        if comb != orig: c['order_changed'] += 1; diff.append(i)
        c['pre'] += p != '-'; c['root'] += ro != '-'; c['suf'] += s != '-'
    pickle.dump(res, open('/home/claude/work3/split3.pkl', 'wb'))
    print(dict(c))
    import random; random.seed(4)
    for i in random.sample(diff, 12):
        r = rows[i - 1]
        print('=====', i, r[4], '|', r[8]); print('  原：'); [print('    ', l[:100]) for l in str(r[9]).split('\n')]
        p, ro, s = res[i]
        print('  前缀：', p[:100].replace('\n', ' ⏎ ')); print('  词根：', ro[:160].replace('\n', ' ⏎ ')); print('  后缀：', s[:160].replace('\n', ' ⏎ '))

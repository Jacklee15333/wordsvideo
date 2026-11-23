"""含义：同词性的意思写一行（“；”隔开）；例句：每个有例子的意思一行“意思：例子”"""
import re, pickle, copy, collections, sys
sys.path.insert(0, '/home/claude/work2')
import overrides2 as O2

S0 = pickle.load(open('/home/claude/work2/senses0.pkl', 'rb'))

def strip_parens(s):
    while True:
        s2 = re.sub(r'（[^（）]*）|\([^()]*\)', '', s)
        if s2 == s: return s
        s = s2

def key_of(gloss):
    """例句列里用来对上意思的“意思”：去掉括号里的说明，冒号换成空格"""
    k = strip_parens(gloss).replace('：', ' ').replace(':', ' ')
    k = re.sub(r'\s+', ' ', k).strip()
    return k or gloss.strip()

def full_key(s):
    return re.sub(r'\s+', ' ', (''.join('（%s）' % l for l in s['labels']) + s['gloss']).replace('：', ' ').replace(':', ' ')).strip()

def senses_of(rn):
    out = []
    for i, s in enumerate(S0[rn]):
        if (rn, i) in O2.EDIT:
            for j, (pos, labels, gloss, ex) in enumerate(O2.EDIT[(rn, i)]):
                d = copy.deepcopy(s)
                if j > 0: d['circ'] = ''
                if pos: d['pos'] = pos
                if labels is not None: d['labels'] = labels
                if gloss is not None: d['gloss'] = gloss
                if ex is not None: d['ex'] = ex
                out.append(d)
        else:
            out.append(copy.deepcopy(s))
    return out

def text_of(s):
    return ''.join('（%s）' % l for l in s['labels']) + s['gloss']

def group(rn):
    ss = senses_of(rn)
    blocks = []
    for s in ss:
        if s['circ'] or not blocks: blocks.append([])
        blocks[-1].append(s)
    mean_lines, ex_lines, order = [], [], []
    base_n = collections.Counter(key_of(s['gloss']) for s in ss)
    full_n = collections.Counter(full_key(s) for s in ss)
    for b in blocks:
        pos_order, groups = [], {}
        for s in b:
            if s['pos'] not in groups: pos_order.append(s['pos']); groups[s['pos']] = []
            groups[s['pos']].append(s)
        circ = b[0]['circ']
        for k, p in enumerate(pos_order):
            items = [text_of(s) for s in groups[p]]
            mean_lines.append(p + ' ' + (circ + ' ' if circ and k == 0 else '') + '；'.join(items))
            for s in groups[p]:
                order.append(s)
                if s['ex']:
                    key = key_of(s['gloss'])
                    if base_n[key] > 1:                               # 去掉括号后和别的意思一样：带上标签（（数量、程度）高的）
                        key = full_key(s)
                        if full_n[key] > 1: key = p + ' ' + key       # 还一样（兼两种词性写了两次）：前面加词性
                    ex_lines.append(key + '：' + '；'.join(s['ex']))
    return '\n'.join(mean_lines), '\n'.join(ex_lines), order

if __name__ == '__main__':
    out = {}
    c = collections.Counter()
    for rn in S0:
        F, G, order = group(rn)
        out[rn] = (F, G)
        c['F_lines'] += F.count('\n') + 1
        c['G_lines'] += (G.count('\n') + 1) if G else 0
        c['rows_with_G'] += bool(G)
    pickle.dump(out, open('/home/claude/work2/fg.pkl', 'wb'))
    print(dict(c))
    for rn in (28, 8, 37, 5358, 2208, 152, 1702, 754, 8661, 3681, 527, 2235):
        F, G = out[rn]
        print('=====', rn); print(F); print('  --- 例句'); print('\n'.join('  ' + x for x in G.split('\n')))

import json, re, sys
from collections import defaultdict
sys.path.insert(0, '/home/claude/work/hc')
from catalog import TEXT, KIND, BY_ID
from wcat import CAT, EXTRA
from wphr import PH
import auto
from wordfreq import zipf_frequency

T = json.load(open('/home/claude/work/hc/feats.json'))
BYW = {t['w']: t for t in T}
ROWS = json.load(open('/home/claude/work/rows.json'))
ALLW = {str(r[5]).lower(): r for r in ROWS}

try:
    from wman import MAN, MANX, PLURAL
except ImportError:
    MAN, MANX, PLURAL = {}, {}, {}


def cat_of(t):
    return CAT.get(t['w']) or auto.auto(t)


CATS = {t['w']: cat_of(t) for t in T}


def short_sense(w):
    r = ALLW.get(w.lower())
    if not r:
        return ''
    F = str(r[6] or '')
    for l in F.split('\n'):
        m = re.match(r'^(?:modal v\.|aux\. v\.|n\.|v\.|adj\.|adv\.|pron\.|prep\.|conj\.|num\.|art\.|int\.|phr\.)\s+(.*)$', l.strip())
        if m:
            s = re.sub(r'^[①②③]\s*', '', m.group(1))
            while re.search(r'（[^（）]*）', s):
                s = re.sub(r'（[^（）]*）', '', s)
            s = s.split('；')[0]
            s = s.split('、')[0].split('，')[0].split('：')[0].strip()
            if len(s) > 10 or s.count('“') != s.count('”') or '（' in s or '）' in s:
                return ''
            return s
    return ''


def zipf(w):
    return zipf_frequency(w.replace('-', ' '), 'en') if '-' not in w else zipf_frequency(w.split('-')[0], 'en') - 3


def parts(t):
    return [p['b'] for p in t['parts']]


def lastp(t):
    return parts(t)[-1].lower()


def firstp(t):
    return parts(t)[0].lower()


def fam(t, cats=None, key='last', n=2, fmt='sense'):
    """同一条规律、共用最后（或最前）一个部分的别的词，挑常见的"""
    w = t['w']
    k = lastp(t) if key == 'last' else firstp(t)
    cand = []
    for u in T:
        if u['w'] == w or u['type'] != '③ 合成词':
            continue
        if cats and CATS.get(u['w']) not in cats:
            continue
        uk = lastp(u) if key == 'last' else firstp(u)
        if uk != k:
            continue
        if firstp(u) in PARTS and firstp(t) not in PARTS:
            continue
        # 同一个词的复数、变体不算
        a, b = w.lower().replace('-', ''), u['w'].lower().replace('-', '')
        if a.rstrip('s') == b.rstrip('s') or a.replace('men', 'man') == b.replace('men', 'man') or a == b:
            continue
        cand.append(u)
    cand.sort(key=lambda u: (not (0 < len(short_sense(u['w'])) <= 6), -zipf(u['w'])))
    out = []
    for u in cand[:n]:
        if fmt == 'sense':
            s = short_sense(u['w'])
            out.append(u['w'] + (' ' + s if s else ''))
        elif fmt == 'phrase':
            if u['w'] in PH:
                out.append(PH[u['w']][0] + ' → ' + u['w'])
            else:
                out.append(u['w'])
        else:
            out.append(u['w'])
    return out


PARTS = {'in','out','up','down','back','over','under','by','off','on','after','with','through'}


def cat_examples(rid, w, n=2):
    ex = [x.strip() for x in BY_ID[rid][4].split('；')]
    ex = [x for x in ex if x.split(' ')[0].lower() != w.lower()]
    return ex[:n]


def same(items):
    return ('同 ' + '、'.join(items)) if items else ''


def join_body(*xs):
    xs = [x for x in xs if x]
    return '；'.join(xs)


def line(rid, body=''):
    lab = '合成规律' if KIND[rid] == '合成规律' else '写法'
    return '　%s：%s%s' % (lab, TEXT[rid], '（%s）' % body if body else '')


def lit_of(t):
    return t['lit']


def formula(t):
    terms = t['terms']
    if not terms:
        return ''
    f = '+ '.join('%s（%s）' % (a, b) for a, b in terms)
    return f + ('=“%s”' % lit_of(t) if lit_of(t) else '')


def ex_of(w):
    """例句列里第一个带着这个词的例子：“意思：例子；例子”"""
    r = ALLW.get(w.lower())
    G = str(r[7] or '') if r else ''
    for l in G.split('\n'):
        body = l.split('：', 1)[-1]
        for e in body.split('；'):
            if w.lower() in e.lower():
                return e.strip()
    return ''


def head_desc(t):
    """H01：X 说的是 head：“字面意思”"""
    h = parts(t)[-1]
    h = re.sub(r'\(.*?\)', '', h)
    lit = lit_of(t)
    return '%s 说的是 %s%s' % (t['w'], h, '：“%s”' % lit if lit else '')


def ph_body(t, rid, fam_cats):
    p, z = PH[t['w']]
    me = '%s %s → %s' % (p, z, t['w'])
    f = fam(t, fam_cats, 'last', 1, 'phrase')
    if not f:
        f = fam(t, fam_cats, 'first', 1, 'phrase')
    if not f:
        f = [x.split(' ')[0] for x in cat_examples(rid, t['w'], 1)]
        f = [(PH[x][0] + ' → ' + x) if x in PH else x for x in f]
    return join_body(me, same(f))


NED_FIX = {'haired': 'hair', 'legged': 'leg', 'skinned': 'skin', 'furred': 'fur', 'capped': 'cap', 'leaved': 'leaf', 'leafed': 'leaf',
           'aged': 'age', 'shaped': 'shape', 'sized': 'size', 'colored': 'color', 'coloured': 'colour', 'hued': 'hue', 'sided': 'side',
           'toed': 'toe', 'eared': 'ear', 'eyed': 'eye', 'necked': 'neck', 'edged': 'edge', 'tempered': 'temper', 'fashioned': 'fashion',
           'minded': 'mind', 'hearted': 'heart', 'handed': 'hand', 'headed': 'head', 'tailed': 'tail', 'shelled': 'shell', 'coated': 'coat',
           'sailed': 'sail', 'patterned': 'pattern', 'scented': 'scent', 'structured': 'structure'}


def comp_lines(t):
    w = t['w']
    if w in MAN:                      # 手写的：[(规律代码, 括号里的话), …]
        out = [line(rid, body) for rid, body in MAN[w]]
        for x in EXTRA.get(w, []):
            out.append(line(x, MANX.get(w, {}).get(x, '【缺手写】')))
        return out
    c = CATS[w]
    out = []
    if c == 'PFX' or c == 'X15':
        out = []
    elif c in ('H01', 'H22'):
        f = fam(t, [c], 'last', 2)
        if not f and c == 'H01':
            f = fam(t, ['H01'], 'first', 2)
        if not f:
            f = cat_examples(c, w, 2)
        out.append(line(c, join_body(head_desc(t), same(f))))
    elif c in ('H02', 'H03', 'H04', 'H05', 'H06', 'H08', 'H09', 'H10', 'H17', 'H18', 'H34'):
        if w not in PH:
            out.append(line(c, '【缺短语】'))
        else:
            body = ph_body(t, c, [c])
            if c == 'H08':
                v0 = PH[w][0].split(' ')[0]
                p0 = parts(t)[0]
                if p0.lower() != v0.lower() and p0.lower() not in ('passer', 'passers'):
                    me = '%s %s → %s，动词换成 %s' % (PH[w][0], PH[w][1], w, p0)
                    pf = [u for u in ('grown-up', 'worn-out', 'dried-up', 'built-in', 'made-up', 'leftover') if u != w][:1]
                    body = join_body(me, same([PH[pf[0]][0] + ' → ' + pf[0]]))
            out.append(line(c, body))
    elif c == 'H12':
        ps = parts(t)
        if len(ps) == 3:
            a, n = ps[0], ps[1]
        else:
            a, last = ps[0], ps[1].lower()
            n = NED_FIX.get(last, re.sub(r'e?d$', '', last))
        me = '%s + %s 再加 -ed → %s“%s”' % (a, n, w, lit_of(t))
        f = fam(t, ['H12'], 'last', 1) or cat_examples('H12', w, 1)
        out.append(line(c, join_body(me, same(f))))
    elif c == 'H07':
        ex = ex_of(w)
        ph = ' '.join(re.sub(r'\(.*?\)', '', p) for p in parts(t))
        z = re.sub(r'的$', '', lit_of(t))
        me = '%s %s → %s' % (ph, z, ex if ex else w)
        f = fam(t, ['H07'], 'last', 1) or fam(t, ['H07'], 'first', 1) or cat_examples('H07', w, 1)
        out.append(line(c, join_body(me, same(f))))
    elif c == 'H13':
        ex = ex_of(w) or w
        out.append(line(c, join_body(ex, PLURAL.get(w, ''))))
    elif c in ('H19', 'H20', 'H21', 'H23', 'H24', 'H25', 'H26', 'H28'):
        me = formula(t)
        if c == 'H28':
            me = '%s → %s%s' % (t['split'], w, '：“%s”' % lit_of(t) if lit_of(t) else '')
        f = [] if c == 'H26' else fam(t, [c], 'last', 1)
        if c == 'H23':
            f = [{'whatever': 'whenever 无论何时', 'however': 'whatever 无论什么', 'whenever': 'wherever 无论在哪里', 'wherever': 'whenever 无论何时',
                  'whoever': 'whatever 无论什么', 'whomever': 'whoever 无论是谁', 'whichever': 'whatever 无论什么'}.get(w, 'whatever 无论什么')]
        f = f or cat_examples(c, w, 1)
        out.append(line(c, join_body(me, same(f))))
    else:
        out.append(line(c, '【缺手写】'))
    for x in EXTRA.get(w, []):
        out.append(line(x, MANX.get(w, {}).get(x, '【缺手写】')))
    return out


if __name__ == '__main__':
    res = {}
    for t in T:
        res[t['w']] = comp_lines(t)
    json.dump(res, open('/home/claude/work/hc/comp_out.json', 'w'), ensure_ascii=False, indent=0)
    miss = [w for w, ls in res.items() if any('【缺' in l for l in ls)]
    print('total', len(res), 'missing', len(miss))
    by = defaultdict(list)
    for w in miss:
        by[CATS[w]].append(w)
    for k, v in sorted(by.items()):
        print(k, len(v), ' '.join(v))

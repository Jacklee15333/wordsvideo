"""合成词特征：拆分的各部分、第一行等式的括号意思、字面意思、整个词的词性、各部分在表里的词性"""
import json, re, sys
sys.path.insert(0, '/home/claude/work/orig_maint/etymology-table/scripts')
rows = json.load(open('/home/claude/work/rows.json'))
W = {}
for r in rows:
    W.setdefault(str(r[5]).lower(), r)

POSRE = re.compile(r'^(modal v\.|aux\. v\.|n\.|v\.|adj\.|adv\.|pron\.|prep\.|conj\.|num\.|art\.|int\.|phr\.)\s')
def pos_list(F):
    out = []
    for l in str(F or '').split('\n'):
        m = POSRE.match(l.strip())
        if m and m.group(1) not in out:
            out.append(m.group(1))
    return out

def first_sense(F):
    for l in str(F or '').split('\n'):
        m = POSRE.match(l.strip())
        if m:
            body = l.strip()[m.end():]
            body = re.sub(r'^[①②③]\s*', '', body)
            s = body.split('；')[0]
            s = re.sub(r'（[^（）]*）', '', s).strip()
            return s
    return ''

def split_parts(I):
    sp = str(I or '').split('；')[0]
    return [p.strip() for p in re.split(r'\s\+\s', sp) if p.strip()]

def bare(p):
    return re.sub(r'\(.*?\)', '', p).strip()

def _top_split_plus(s):
    out, buf, d = [], '', 0
    for ch in s:
        if ch in '（(':
            d += 1
        elif ch in '）)':
            d = max(0, d - 1)
        if ch == '+' and d == 0:
            out.append(buf); buf = ''
        else:
            buf += ch
    out.append(buf)
    return [x.strip() for x in out if x.strip()]


def terms_of(line1):
    """【构词逻辑】A（…）+ B（…）=“…”：按括号外的 + 切开，每段取“部分（意思）”"""
    s = re.sub(r'^【构词逻辑】', '', line1)
    s = re.split(r'；\s*词性变化', s)[0]
    m = re.search(r'=\s*(?:（[^（）]*）\s*)?“((?:[^“”]|“[^“”]*”)*)”', s)
    lit = m.group(1) if m else ''
    left = s[:m.start()] if m else s
    terms = []
    for seg in _top_split_plus(left):
        mm = re.match(r'^(.*?)（((?:[^（）]|（[^（）]*）)*)）\s*$', seg)
        if mm and mm.group(1).strip() and re.search(r'[A-Za-z0-9æþðǣ]', mm.group(1)):
            terms.append((mm.group(1).strip(), mm.group(2).strip()))
    return terms, lit

def feats(r):
    w = str(r[5]); N = str(r[14] or '')
    L = N.split('\n')
    terms, lit = terms_of(L[0])
    parts = split_parts(r[9])
    pp = []
    for p in parts:
        b = bare(p)
        rr = W.get(b.lower())
        pp.append({'p': p, 'b': b, 'pos': pos_list(rr[6]) if rr else [], 'sense': first_sense(rr[6]) if rr else '', 'in': bool(rr)})
    return {'row': r[0], 'w': w, 'type': r[8], 'split': r[9], 'parts': pp, 'terms': terms, 'lit': lit,
            'pos': pos_list(r[6]), 'sense': first_sense(r[6]), 'line1': L[0], 'N': N, 'F': r[6], 'P': r[16], 'L': r[12]}

def targets():
    out = []
    for r in rows:
        if r[8] == '③ 合成词' or '-' in str(r[5]):
            out.append(feats(r))
    return out

if __name__ == '__main__':
    T = targets()
    json.dump(T, open('feats.json', 'w'), ensure_ascii=False)
    print(len(T))
    from collections import Counter
    print(Counter(tuple(t['pos'][:1]) for t in T))

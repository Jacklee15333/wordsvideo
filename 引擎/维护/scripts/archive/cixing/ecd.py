"""ECDICT 查词：每个词的各词性义项"""
import pickle, re
D = pickle.load(open('/home/claude/ecd.pkl', 'rb'))
LAB = {'n.': 'n.', 'pl.': 'n.', 'na.': 'n.', 'v.': 'v.', 'vt.': 'v.', 'vi.': 'v.', 'vi.vt.': 'v.', 'vt.vi.': 'v.',
       'a.': 'adj.', 'adj.': 'adj.', 'ad.': 'adv.', 'adv.': 'adv.', 'prep.': 'prep.', 'conj.': 'conj.',
       'pron.': 'pron.', 'int.': 'int.', 'interj.': 'int.', 'num.': 'num.', 'art.': 'art.', 'aux.': 'aux.'}
def entries(w):
    w = str(w).strip()
    es = D.get(w.lower(), [])
    exact = [e for e in es if e['word'] == w]
    return exact or es
def pos_lines(w):
    """[(pos, [items])]，按 ECDICT 里的先后"""
    out = []
    for e in entries(w):
        for line in e['translation'].split('\\n'):
            line = line.strip()
            m = re.match(r'^([a-z]+\.(?:[a-z]+\.)?)\s*(.*)$', line)
            if m and m.group(1) in LAB:
                p = LAB[m.group(1)]; body = m.group(2)
            elif re.search(r'的(过去式|过去分词)', line):
                p = 'v.'; body = line
            else:
                continue
            items = [x.strip() for x in re.split(r'[,，;；]', body) if x.strip()]
            out.append((p, items))
    return out
def first_pos(w):
    pl = pos_lines(w)
    return pl[0][0] if pl else ''

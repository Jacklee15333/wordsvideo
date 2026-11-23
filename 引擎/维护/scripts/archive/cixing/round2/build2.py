"""从上一版（一个意思一行）拆成：含义（同词性一行）+ 例句（每个意思一行“意思：例子”）"""
import re, pickle, collections
from ex_split import POS_RX, lead_labels, split_meaning, split_top

final = pickle.load(open('/home/claude/work/final.pkl', 'rb'))

def parse_line(line):
    m = POS_RX.match(line)
    pos, rest = m.group(1), m.group(2).strip()
    circ = ''
    mc = re.match(r'^([\u2460-\u2473])\s*', rest)
    if mc: circ, rest = mc.group(1), rest[mc.end():]
    labs, main = lead_labels(rest)
    gloss, exs = split_meaning(main)
    return {'pos': pos, 'circ': circ, 'labels': labs, 'gloss': gloss, 'ex': exs, 'raw': line}

def all_senses():
    out = {}
    for rn, (lines, moved) in final.items():
        out[rn] = [parse_line(l) for l in lines]
    return out

if __name__ == '__main__':
    S = all_senses()
    pickle.dump(S, open('senses0.pkl', 'wb'))
    c = collections.Counter()
    for rn, ss in S.items():
        for s in ss:
            c['senses'] += 1
            if s['ex']: c['with_ex'] += 1; c['ex_items'] += len(s['ex'])
            if not s['gloss']: c['empty'] += 1
            if re.search(r'[（(]', s['gloss']): c['gloss_paren'] += 1
    print(dict(c))

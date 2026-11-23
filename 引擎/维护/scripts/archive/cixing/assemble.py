"""把分析结果 + 人工核对写成新的含义列；挪走的条目写进 L 列"""
import re, pickle, importlib
import overrides as O
from posify import ROWS
from render import line_of

POSSET = ['n.', 'v.', 'modal v.', 'aux. v.', 'adj.', 'adv.', 'pron.', 'prep.', 'conj.', 'num.', 'art.', 'int.', 'phr.']
POSRX = re.compile(r'^(modal v\.|aux\. v\.|n\.|v\.|adj\.|adv\.|pron\.|prep\.|conj\.|num\.|art\.|int\.|phr\.) (.+)$')

def eng_word(rest):
    m = re.match(r"^([A-Za-z][A-Za-z'’\-]*(?:\s*/\s*[A-Za-z][A-Za-z'’\-]*)?)", rest)
    return m.group(1) if m else ''

def flat(note):
    """说明里的括号压平，免得括号套括号：短的中文注释改成引号，例子、年代、长的改成“：…”“，…”"""
    def f(m):
        x = m.group(1)
        if re.match(r'^\d', x): return '，' + x
        if re.search('[A-Za-z]', x): return '：' + x
        if len(x) <= 8: return '“' + x + '”'
        return '，' + x
    return re.sub(r'（([^（）]*)）', f, note)

def merge_note(prev, note):
    """把说明并进上一行：上一行以括号结尾的，接在括号里（用“；”）；否则新开一个括号"""
    n = flat(note)
    if prev.endswith('）'):
        return prev[:-1] + '；' + n + '）'
    return prev + '（' + n + '）'

def assemble(rn, a):
    lines, moved = [], []
    for o in a:
        key = (rn, o['k'])
        if key in O.DROP: continue
        if key in O.MOVE:
            text = ('（' + '）（'.join(o['labels']) + '）' if o['labels'] else '') + o['rest']
            w = eng_word(o['rest'])
            lab = '联想' if w in O.ASSOC else ('合成' if w in O.COMPOUND or (w.split('/')[0].strip() in O.COMPOUND) else '派生')
            moved.append((lab, text))
            continue
        if key in O.MERGE:
            text = ('（' + '）（'.join(o['labels']) + '）' if o['labels'] else '') + o['rest']
            lines[-1] = merge_note(lines[-1], text)
            continue
        if key in O.LINE:
            lines.extend(O.LINE[key].split('\n')); continue
        p = O.POS.get(key)
        if p is None:
            p = o['pos'][0] if o['pos'] else 'n.'
        lines.append(line_of(o, p, O.TXT.get(key)))
    return lines, moved

def build_all():
    res = pickle.load(open('/home/claude/work/res4.pkl', 'rb'))
    out = {}
    for rn, (a, D, dw, mg) in res.items():
        out[rn] = assemble(rn, a)
    return out

if __name__ == '__main__':
    out = build_all()
    pickle.dump(out, open('/home/claude/work/final.pkl', 'wb'))
    bad = []
    import collections
    pc = collections.Counter(); nl = collections.Counter()
    for rn, (lines, moved) in out.items():
        nl[len(lines)] += 1
        if not lines: bad.append((rn, 'empty'))
        for l in lines:
            m = POSRX.match(l)
            if not m: bad.append((rn, 'nopos', l)); continue
            pc[m.group(1)] += 1
            body = m.group(2)
            if not body.strip(): bad.append((rn, 'nobody', l))
            # 括号外的“；”
            d = q = 0
            for ch in body:
                if ch in '（(': d += 1
                elif ch in '）)': d = max(0, d - 1)
                elif ch == '“': q += 1
                elif ch == '”': q = max(0, q - 1)
                elif ch == '；' and d == 0 and q == 0: bad.append((rn, 'semicolon', l)); break
            if 'REL' in l: bad.append((rn, 'REL', l))
    print(pc.most_common()); print(sorted(nl.items()))
    print('bad', len(bad))
    for b in bad[:80]: print(b, ROWS[b[0]-1][4])

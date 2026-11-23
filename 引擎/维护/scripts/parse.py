"""Parse the 拆分 column, e.g. 'com + mon(=mun)' -> parts with surface/full/eqs.
两种拆法用“；”隔开时只看第一种；按括号外的“+”切（surg(=chirurg) + ery）。"""
import re
PAREN = re.compile(r'\(([^()]*)\)')
def parse_part(p):
    p = p.strip(); eqs = []
    def repl_full(m):
        c = m.group(1).strip()
        if c[:1] in ('=', '←', '≈'):
            eqs.append(c.lstrip('=←≈ ').strip()); return ''
        return c if re.fullmatch(r'[A-Za-z]+', c) else ''
    full = PAREN.sub(repl_full, p)
    return dict(raw=p, surface=PAREN.sub('', p).strip(), full=full.strip(), eqs=eqs)
def split_top(s, sep='+'):
    out, d, cur = [], 0, ''
    for ch in s:
        if ch in '(（': d += 1
        elif ch in ')）': d = max(0, d - 1)
        if ch == sep and d == 0: out.append(cur); cur = ''
        else: cur += ch
    out.append(cur)
    return [x for x in out if x.strip()]
def parse_split(s):
    s = str(s).strip()
    if s in ('—', 'nan', 'None', '') or '+' not in s: return None
    s = re.split(r'[；;]', s)[0]
    s2 = re.sub(r'（[^）]*）', '', s)
    return [parse_part(x) for x in split_top(s2)]

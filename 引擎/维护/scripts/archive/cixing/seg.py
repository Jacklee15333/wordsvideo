import re
def split_top(s, seps='；'):
    out, cur, d, q = [], '', 0, 0
    for ch in s:
        if ch in '（(': d += 1
        elif ch in '）)': d = max(0, d - 1)
        elif ch == '“': q += 1
        elif ch == '”': q = max(0, q - 1)
        if ch in seps and d == 0 and q == 0: out.append(cur); cur = ''
        else: cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]
def lead_tags(t):
    tags = []
    while True:
        m = re.match(r'^[（(]([^（）()]*)[）)]\s*', t)
        if not m: break
        tags.append(m.group(1)); t = t[m.end():]
    return tags, t
def split_circled(s):
    """括号外的 ②③… 前面切开（同形词的编号），① 留在开头"""
    out, cur, d = [], '', 0
    for ch in s:
        if ch in '（(': d += 1
        elif ch in '）)': d = max(0, d - 1)
        if d == 0 and '\u2461' <= ch <= '\u2469' and cur.strip():
            out.append(cur.strip()); cur = ''
        cur += ch
    out.append(cur.strip())
    return [x for x in out if x]
def segments(f):
    out = []
    for li, line in enumerate(str(f or '').split('\n')):
        for s in split_top(line):
            for t in split_circled(s):
                out.append((li, t))
    return out

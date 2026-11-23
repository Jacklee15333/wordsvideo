"""含义的每个意思：拆出例句、例词（括号里英文开头的、“说明：英文”冒号后面的），剩下的是干净的意思"""
import re

POS_RX = re.compile(r'^(modal v\.|aux\. v\.|n\.|v\.|adj\.|adv\.|pron\.|prep\.|conj\.|num\.|art\.|int\.|phr\.)\s+(.*)$')
CJK = r'\u3400-\u9fff'

def split_top(s, seps='；'):
    out, cur, d, q = [], '', 0, 0
    for ch in s:
        if ch in '（(': d += 1
        elif ch in '）)': d = max(0, d - 1)
        elif ch == '“': q += 1
        elif ch == '”': q = max(0, q - 1)
        if ch in seps and d == 0 and q == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]

def lead_labels(t):
    labs = []
    while True:
        m = re.match(r'^[（(]([^（）()]*)[）)]\s*', t)
        if not m: break
        labs.append(m.group(1)); t = t[m.end():]
    return labs, t

def trailing_group(s):
    """s 以“）”结尾时，找出最后一个括号（可以套括号）：返回 (前面的, 括号里的)；不以括号结尾返回 None"""
    s = s.rstrip()
    if not s.endswith(('）', ')')): return None
    d = 0
    for i in range(len(s) - 1, -1, -1):
        ch = s[i]
        if ch in '）)': d += 1
        elif ch in '（(':
            d -= 1
            if d == 0:
                return s[:i].rstrip(), s[i + 1:-1]
    return None

def is_example(item):
    """括号里的一项是不是例句、例词：英文开头、带英文字母；“如 / 比如 / 例如”后面接英文的也算"""
    t = item.strip()
    if not re.search(r'[A-Za-z]', t): return False
    if re.match(r'^[=＝]', t): return False                       # = should not：注释
    if re.match(r'^(如|比如|例如)\s*[A-Za-z]', t): return True
    if re.match(r'^[A-Za-z0-9“‘"\'…\.\-£$€¥%]', t):
        return True
    return False

def colon_split(item):
    """“构成比较级：more beautiful” → ('构成比较级', 'more beautiful')；不是这种返回 None"""
    m = re.match(r'^([^：:A-Za-z]*[' + CJK + r'][^：:]*?)[：:]\s*([A-Za-z“"‘\'….].*)$', item.strip())
    if m and re.search(r'[A-Za-z]', m.group(2)):
        return m.group(1).strip(), m.group(2).strip()
    return None

# 英文开头、其实是说明的：年代（1640s 起）、“X 的复数 / 比较级 / 简称 …”、“…也叫…”
NOTE_EN = re.compile(r'^(\d{3,4}s?\b|\d{3,4} ?年)|的(常用)?(复数|单数|比较级|最高级|过去式|过去分词|现在分词|全拼|简称|缩写|写法|缩略|全称)(说法)?|也叫|也常作|指整个|模型运行')

def classify(item):
    """括号里的一项 → ('ex', 例子) / ('note', 说明) / ('split', 说明, 例子)"""
    t = item.strip()
    if NOTE_EN.search(t):
        m = re.match(r'^(.*?)[：:]\s*([A-Za-z“"‘\'….].*)$', t)
        if m and re.search('[A-Za-z]', m.group(2)): return ('split', m.group(1).strip(), m.group(2).strip())
        return ('note', t)
    cs = colon_split(t)
    if cs and not is_example(t): return ('split', cs[0], cs[1])
    if is_example(t): return ('ex', re.sub(r'^(如|比如|例如)\s*', '', t))
    return ('note', t)

def split_meaning(main):
    """一个意思（不含开头的标签）→ (干净的意思, [例子…])"""
    examples = []
    s = main.strip()
    while True:
        tg = trailing_group(s)
        if not tg: break
        before, inside = tg
        items = split_top(inside)
        keep, moved = [], []
        for it in items:
            k = classify(it)
            if k[0] == 'split': keep.append(k[1]); moved.append(k[2])
            elif k[0] == 'ex': moved.append(k[1])
            else: keep.append(k[1])
        if not moved: break
        examples = moved + examples
        s = before + ('（' + '；'.join(keep) + '）' if keep else '')
        if keep: break           # 剩下的是说明，不再往前找
    # 括号外“说明：英文例子”
    if not examples:
        pass
    m = None
    d = 0; cut = -1
    for i, ch in enumerate(s):
        if ch in '（(': d += 1
        elif ch in '）)': d = max(0, d - 1)
        elif ch in '：:' and d == 0:
            rest = s[i + 1:].strip()
            if re.match(r'^[A-Za-z“"‘\'…]', rest) and re.search(r'[' + CJK + r']', s[:i]):
                cut = i; break
    if cut >= 0:
        examples = [s[cut + 1:].strip()] + examples
        s = s[:cut].strip()
    return s.strip(), examples

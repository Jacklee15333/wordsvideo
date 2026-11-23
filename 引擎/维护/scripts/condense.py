"""组合列“词性变化”一行写短：{词性}。{前面部分}“{意思}”加上 -xx（{后缀的意思}），就成了“{合起来的意思}”。
去掉模板里讲语法的套话（名词前面能加 the、my……；形容词说的是“什么样的”……），补上后缀本身的意思。
用词规律那一行：规律就挂在这一步下面，括号里重复本词的例子去掉，只留“同 熟悉的例子”。"""
import re

VERBOSE = ['一个动作当成东西', '就把这个动作当成一样东西来说', '就把这种性质当成一样东西来说', '（名词说的是“谁、什么东西”）',
           '放在名词前面或 be 后面', '放在名词前面去形容别的东西', '（动词说的是“做什么”）', '（副词修饰动词、形容词）',
           '使它变成这样，或者让它带上这样东西', '，合起来是“', '名词前面能加 the、my', '（名词能当主语、宾语）']
SPLIT_S = re.compile(r'(?:是一个动作|是一种人|是一样东西(?:或一种人|或一门学问)?|说的是一种性质(?:或一样东西)?|说的是一样东西或一种性质|'
                     r'说的是“什么样的”|本身说的就是“什么样的”|说东西“什么样的”|说的是一种特点或主张|说的是一件事、一种情况|，?\s*加上\s*-)')
GENERIC = {'做这个动作的人或东西', '做这件事、搞这一行的人'}
POSONLY = re.compile(r'^(动词|名词|形容词|副词)?(词尾|后缀|成分|标记)$|^变(成)?(动词|名词|形容词|副词)$')
# 表里没写后缀意思时用的说法（只管常见后缀）
AFFIX = {'-ate': '使…、做…', '-ize': '使…化', '-ise': '使…化', '-ify': '使…', '-fy': '使…', '-en': '使…', '-ion': '…这件事、…的结果', '-tion': '…这件事、…的结果',
         '-ation': '…这件事、…的结果', '-sion': '…这件事、…的结果', '-ment': '…的行为、结果', '-ness': '…的状态', '-ity': '…的性质、状态', '-ty': '…的性质、状态',
         '-er': '做…的人或东西', '-or': '做…的人或东西', '-ist': '…的人', '-ive': '有…性质的', '-ous': '充满…的、有…性质的', '-ful': '充满…的', '-less': '没有…的',
         '-able': '能被…的', '-ible': '能被…的', '-al': '…的', '-ic': '…的', '-ical': '…的', '-ly': '…地', '-y': '有…的', '-ing': '…这件事、正在…的', '-ed': '被…了的',
         '-d': '被…了的', '-age': '…的总体、行为', '-ance': '…的状态、行为', '-ence': '…的状态、行为', '-ant': '正在…的、…的人', '-ent': '正在…的、…的人',
         '-ure': '…的行为、结果', '-ary': '…的、…的地方', '-ory': '…的、…的地方', '-ism': '…主义、…的做法', '-ship': '…的身份、关系', '-hood': '…的身份、状态',
         '-dom': '…的状态、领域', '-th': '…的性质、状态', '-ward': '朝…方向的', '-ish': '有点…的、像…的', '-some': '有…倾向的', '-ee': '被…的人', '-ess': '女…',
         '-let': '小…', '-et': '小…', '-ette': '小…', '-ling': '小…', '-s': '复数', '-es': '复数', '-est': '最…的', '-st': '最…的', '-ar': '…的', '-ine': '…的'}


def top_eq_parts(first):
    """构词逻辑第一行 → ([(部分, 意思)], 字面意思)"""
    s = re.sub(r'^【构词逻辑】', '', str(first or '')).strip()
    def split_top(t, sep):
        out, d, cur = [], 0, ''
        for ch in t:
            if ch in '（(“':
                d += 1
            elif ch in '）)”':
                d = max(0, d - 1)
            if ch == sep and d == 0:
                out.append(cur)
                cur = ''
            else:
                cur += ch
        out.append(cur)
        return [x.strip() for x in out if x.strip()]
    term = lambda x: (lambda m: (m.group(1).strip(), m.group(2).strip()) if m else (x.strip(), ''))(re.match(r'^([^（(]*?)\s*[（(]([^（）()]*)[）)]', x))
    m = re.match(r'^派生路线[：:]\s*(.*)$', s)
    if m:
        items = [term(x) for x in split_top(m.group(1), '→')]
        return items, (items[-1][1] if items else ''), True
    d = q = 0
    for k, ch in enumerate(s):
        if ch in '（(':
            d += 1
        elif ch in '）)':
            d = max(0, d - 1)
        elif ch == '“':
            q += 1
        elif ch == '”':
            q = max(0, q - 1)
        elif ch == '=' and d == 0 and q == 0:
            mm = re.match(r'^\s*“((?:[^“”]|“[^“”]*”)*)”', s[k + 1:])
            return [term(x) for x in split_top(s[:k], '+')], (mm.group(1).strip() if mm else ''), False
    return [], '', False


def norm(t):
    return re.sub(r'[^a-z]', '', str(t).lower())


def affix_meaning(lab, H, terms):
    core = re.sub(r'（[^（）]*）', '', lab).strip()
    for t, g in terms:
        if norm(t) and norm(t) == norm(core) and g and len(g) <= 14 and not re.search(r'[“”]', g) and not POSONLY.match(g.strip()):
            return g.replace('；', '、')
    for l in str(H or '').split('\n'):
        if l.split('：', 1)[0].strip() == lab and '：' in l:
            role = l.split('：', 1)[1]
            role = re.split(r'（来自|（英语本来就有|（就是', role)[0]
            m = re.search(r'“([^“”]{1,14})”', role)
            if m and '…' in m.group(1) or (m and re.search(r'的$|地$', m.group(1))):
                return m.group(1).replace('；', '、')
    return AFFIX.get(core, '')


def condense(word, lab, txt, H, first):
    """返回新的“词性变化”文字；不该改的原样返回"""
    if not any(v in txt for v in VERBOSE) or '。' not in txt:
        return txt
    pos, rest = txt.split('。', 1)
    terms, lit, route = top_eq_parts(first)
    core = re.sub(r'（[^（）]*）', '', lab).strip()
    # 母词换了意思的那句（feel 本义“摸”：……，就成了“感觉”。）压成“feel“感觉”（本义“摸”）”
    base = ''
    m = re.match(r'^(?P<stem>[A-Za-z][A-Za-z\- +()]*?) 本义“(?P<orig>[^”]*)”：.*?，就成了“(?P<best>[^”]*)”。(?P<rest>.*)$', rest)
    if m:
        base = '%s“%s”（本义“%s”）' % (m.group('stem'), m.group('best'), m.group('orig'))
        rest = m.group('rest')
    sm = SPLIT_S.search(rest)
    S = rest[:sm.start()].strip().rstrip('，') if sm else ''
    if not base:
        S = re.sub(r'\s*合起来是“([^”]*)”$', r'“\1”', S)
        S = re.sub(r'\s*合起来$', '', S).strip()
        if S.startswith('“') or not re.search(r'[A-Za-z]', S):
            S = ''
        base = S
    if not base:
        idx = [k for k, (t, g) in enumerate(terms) if norm(t) == norm(core)]
        j = idx[-1] if idx else len(terms) - 1
        bt = terms[:j] if not route else terms[-2:-1]
        if len(bt) == 1:
            base = bt[0][0] + ('“%s”' % bt[0][1] if bt[0][1] and len(bt[0][1]) <= 12 else '')
        elif len(bt) > 1:
            base = ' + '.join(t for t, _ in bt)
    if not base:
        return txt
    # 合起来的意思：模板里写了具体的（“能被喜欢”“充满危险的”）就用它，套话就用构词逻辑的字面意思
    q = ''
    for rx in (r'说一样东西“([^”]*)”', r'说的是“([^”]*)”这种性质', r'意思是“([^”]*)”', r'合起来是“([^”]*)”', r'就是“([^”]*)”',
               r'就成了“([^”]*)”这个动作', r'，指“([^”]*)”', r'表示“([^”]*)”', r'就成了“([^”]*)”'):
        mm = re.search(rx, rest)
        if mm and mm.group(1) not in GENERIC:
            q = mm.group(1)
            break
    R = q or lit
    # 字面意思用的是古义、前面部分用的是今义时（subscribe“订阅”+ -ion =“写在下面的东西”），按今义说：订阅这件事
    gm = re.search(r'“([^”]*)”', base)
    g0 = re.split(r'[、/；，]', gm.group(1))[0].strip() if gm else ''
    zh = lambda t: {c for c in str(t) if '\u4e00' <= c <= '\u9fff'}
    kind = ('VN' if ('一个动作当成东西' in txt or '就把这个动作当成一样东西来说' in txt) else
            'AGENT' if '（名词说的是“谁、什么东西”）' in txt else 'ADJN' if '就把这种性质当成一样东西来说' in txt else
            'ADV' if '（副词修饰动词、形容词）' in txt else '')
    made = {'VN': g0 + '这件事', 'AGENT': g0 + '的人', 'ADJN': g0.rstrip('的') + '的状态', 'ADV': g0.rstrip('的') + '地'}.get(kind, '') if g0 else ''
    # 先用构词逻辑的字面意思（每个词手写的，比模板句准）；它和前面部分的意思对不上、或者有几条路时，用按今义说的；最后才用模板里的
    if lit and ' / ' not in lit and (not g0 or (zh(g0) & zh(lit))):
        R = lit
    elif made:
        R = made
    elif lit and ' / ' not in lit:
        R = lit
    elif q:
        R = q
    if not R:
        return txt
    M = affix_meaning(lab, H, terms)
    tail = ''
    mt = re.search(r'[，,]\s*(所以\s+\S+\s*(?:是|指)\s*.+)$', rest)
    if mt:
        tail = '，' + mt.group(1)
    sep = '' if base.endswith('”') or base.endswith('）') else ' '
    return '%s。%s%s加上 %s%s，就成了“%s”%s' % (pos, base, sep, core, '（%s）' % M if M else '', R.replace('；', '、'), tail)


def trim_rule(word, text):
    """用词规律：规律已经挂在这一步下面，括号里重复本词的例子去掉，只留“同 熟悉的例子”"""
    m = re.search(r'（((?:[^（）]|（[^（）]*）)*)）\s*$', text)
    if not m:
        return text
    parts, d, cur = [], 0, ''
    for ch in m.group(1):
        if ch in '（(':
            d += 1
        elif ch in '）)':
            d = max(0, d - 1)
        if ch == '；' and d == 0:
            parts.append(cur.strip())
            cur = ''
        else:
            cur += ch
    parts.append(cur.strip())
    w = re.escape(str(word).lower())
    keep = [p for p in parts if p and not re.match(w + r"(s|es|'s)?(?=[\s：:（(]|$)", p.lower())]
    if keep and keep[0].startswith('同 '):
        keep[0] = keep[0][2:]
    if len(keep) == len(parts) and not parts[0].startswith('同 '):
        return text
    body = text[:m.start()].rstrip()
    return body + ('（同 %s）' % '；'.join(keep) if keep else '')

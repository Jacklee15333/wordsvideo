"""本轮：组合列改成清爽格式（词性变化并进第一行、后缀写成等式、用词规律不编号）。convert_I(行号, 单词, H, I) → (新 I, 说明列表)"""
import re, sys
sys.path.insert(0, '/home/claude/work/etymology-table/scripts'); sys.path.insert(0, '/home/claude/work'); sys.path.insert(0, '/home/claude/work/round')
import columns as C, norm_pos as N
from fixes_pos import MULTI, FIX, INJECT
from condense import top_eq_parts


def strip_so_tail(text):
    head, sent = C.pos_head(text), C.pos_sentence(text)
    m = C.SENT.match(sent)
    if m and re.match(r'^[，,]\s*所以\s', m.group('tail')):
        return head + '。' + sent[:len(sent) - len(m.group('tail'))], True
    return text, False


def literal_end(head):
    s = head
    if re.sub(r'^【构词逻辑】', '', s).startswith('派生路线'):
        ks = C._top_positions(s, '→')
        if not ks:
            return None
        k = ks[-1] + 1
        m = re.match(r'^\s*[^（(]*?([（(])', s[k:])
        if not m:
            return None
        st = k + m.start(1)
        d = 0
        for j in range(st, len(s)):
            if s[j] in '（(':
                d += 1
            elif s[j] in '）)':
                d -= 1
                if d == 0:
                    return j + 1
        return None
    eqs = C._top_positions(s, '=')
    if not eqs:
        return None
    i = eqs[0] + 1
    while i < len(s) and s[i] == ' ':
        i += 1
    if i >= len(s) or s[i] != '“':
        return None
    d = 0
    for j in range(i, len(s)):
        if s[j] == '“':
            d += 1
        elif s[j] == '”':
            d -= 1
            if d == 0:
                return j + 1
    return None


def split_leadin(head):
    """第一行末尾“，有两条路：”这类引出下面步骤的话，挪到下一行"""
    if not head.rstrip().endswith(('：', ':')):
        return head, None
    e = literal_end(head)
    if e is None:
        return head, None
    rest = head[e:]
    cuts = C._top_positions(rest, '。') or C._top_positions(rest, '，')
    if not cuts:
        if rest.strip() in ('：', ':'):
            return head[:e], None
        return head, None
    c = cuts[-1]
    clause = rest[c + 1:].strip()
    return (head[:e] + rest[:c]).rstrip(), clause


def inject_gloss(head, sm):
    eqs = C._top_positions(head, '=')
    if not eqs:
        return head
    i = eqs[0]
    left = head[:i].rstrip()
    terms, lit, route = top_eq_parts(head)
    t = terms[-1][0] if terms else ''
    if not t or not left.endswith(t):
        return head
    return left + '（' + sm + '）' + head[i:]


def convert_I(rn, word, H, I):
    d = C.parse_I(I, word)
    notes = []
    if 'raw' in d:
        return I, notes
    had_rules = bool(d['rules'])
    rule_uses = sum(len(''.join(C.MARK.findall(l))) for l in d['logic'])
    if rn in MULTI:
        d['pos'] = list(MULTI[rn])
        notes.append('几个后缀逐个核对，中间一步写出意思')
    elif rn in FIX:
        d['pos'] = list(FIX[rn])
    elif d['pos']:
        newpos = []
        for lab, txt in d['pos']:
            t2, ch = N.normalize(word, lab, txt, H, d['logic'][0])
            newpos.append((lab, t2))
        d['pos'] = newpos
    tails = 0
    for k, (lab, txt) in enumerate(d['pos']):
        t2, ch = strip_so_tail(txt)
        if ch:
            d['pos'][k] = (lab, t2)
            tails += 1
    if tails:
        notes.append('去掉和【今义】重复的“所以 %s 指……”' % word)
    if d['pos']:
        h0, clause = split_leadin(d['logic'][0])
        if clause:
            d['logic'][0] = h0
            d['logic'].insert(1, clause)
            notes.append('第一行末尾的“%s”挪到下一行' % clause[:12])
        elif h0 != d['logic'][0]:
            d['logic'][0] = h0
        if rn in INJECT:
            h1 = inject_gloss(d['logic'][0], INJECT[rn])
            if h1 != d['logic'][0]:
                d['logic'][0] = h1
                notes.append('第一行补上后缀的意思（%s）' % INJECT[rn])
    new = C.compose_I(d)
    if d['pos']:
        eqn = sum(1 for k, (lab, txt) in enumerate(d['pos']) if C.eq_from_sentence(C.pos_sentence(txt)) and C._eq_needed(d, k))
        notes.insert(0, '词性变化并进构词逻辑第一行' + ('，后缀写成等式' if eqn else '（后缀等式和第一行一样，不再单写）'))
    if had_rules:
        notes.append('用词规律去掉编号，直接写在用到它的那一步下面' + ('（同一条再用到时只留熟悉的例子）' if rule_uses > len(d['rules']) else ''))
    return new, notes

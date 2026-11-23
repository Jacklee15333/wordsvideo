"""三列分工 + 组合列融合 + 清爽格式（2026-11 起）。

拆分（G）只拆；各部分解释（H）只讲每一部分；组合 → 现在的含义（I）讲怎么组合。I 的【构词逻辑】这一块写成一条线：

  【构词逻辑】等式（或派生路线）；词性变化（-or）：动词 → 名词（人或东西）       ← 词性变化并在第一行末尾（几个后缀：（-less、-ly）：名词 → 形容词 → 副词）
  communicate“传达、交流”+ -or（做…的人或东西）=“传达、交流的人”               ← 后缀等式：只在和第一行不重复时写（派生路线、几个后缀、第一行看不到的本义）
  → 第一步 → 结果
  → 第二步 → 结果
  　用词规律：规律（本词：A → B；一个熟悉的例子）                                 ← 不编号，直接写在用到它的那一步下面；同一条再用到，只留熟悉的例子
  【演变】只留步骤里没有的历史
  （2026-11 合成规律轮：合成词第一行下面还有“　合成规律：”“　写法：”两种行，parse_I 当普通行留在 logic 里，compose_I 原样写回，位置不变；2026-11 过去分词轮的“　构词：”一行也一样）
  【今义】【辨析】【趣】【例】

内部（parse_I 的结果）仍是老结构：pos = [(标签, "动词 → 名词。X“…”加上 -xx（…），就成了“…””)]，rules = {①: 文字}，
步骤末尾带〔用词规律①〕。所以 merge_cell、video_check.py、rule_check.py、sense_write.py 都不用改；parse_I 两种格式都认，compose_I 只写新格式。

用法：
  python3 columns.py split <in.xlsx> <out.xlsx> [--note 融合]   # 各部分解释里的组合内容搬进组合列，并按上面的样子写
  python3 columns.py merge <in.xlsx> <out.xlsx>                  # 反向：临时还原成旧格式（sense_write.py 内部用）
  python3 columns.py reformat <in.xlsx> <out.xlsx> [--note 清爽]  # 组合列统一写成上面的样子（再跑一遍不变）
  python3 columns.py check <in.xlsx>                             # 各部分解释里还剩多少组合内容
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from condense import condense  # noqa: E402  词性变化只讲重点：后缀的意思 + 合起来成了什么

CIRC = '①②③④⑤⑥⑦⑧⑨⑩'
MARK = re.compile(r'〔用词规律([①②③④⑤⑥⑦⑧⑨⑩]+)〕')
SEGHEAD = re.compile(r'^\s*[\u2460-\u2473]?\s*【([^【】\n]{1,10})】')
POSLINE = re.compile(r'^\s*词性变化（((?:[^（）]|（[^（）]*）)+)）[：:]\s*(.*)$')   # 标签里可以再带括号：-er（第一个）
RULELINE = re.compile(r'^\s*用词规律([①②③④⑤⑥⑦⑧⑨⑩])[：:]\s*(.*)$')
STEP = re.compile(r'^\s*[→⇒\u2460-\u2473]')
TAILPOS = re.compile(r'；\s*词性变化(（(?:[^（）]|（[^（）]*）)+）[：:].*)$')          # 新格式：第一行末尾的词性变化
RULE_NEW = re.compile(r'^\s*用词规律[：:]\s*(.*)$')                                   # 新格式：不编号的用词规律
SENT = re.compile(r'^(?P<base>.*?)\s*加上\s*(?P<suf>-[^\s（，,]+)(?P<sm>（(?:[^（）]|（[^（）]*）)*）)?，就成了“(?P<res>(?:[^“”]|“[^“”]*”)*)”(?P<tail>.*)$')
DATE = re.compile(r'\d|世纪|古英语|中古|晚期|约\s*\d')
PURE_DATE = re.compile(r'^(约\s*)?(\d{3,4}\s*(s|年)?|\d{1,2}\s*世纪(初|中|末|中叶|中期)?|(晚期|早期)?(古|中古)英语)(\s*(已见|起|左右|前后))?$')


# ---------------------------------------------------------------- 小工具
def nres(t):
    return re.sub(r'\s+', '', re.sub(r'（[^（）]*）|\([^()]*\)', '', str(t or '')))


def full_of(l):
    s = MARK.sub('', str(l)).strip()
    s = re.sub(r'^[→⇒]\s*', '', s)
    s = re.sub(r'^[\u2460-\u2473]\s*', '', s)
    return re.sub(r'\s+', '', s)


def raw_result(l):
    return re.sub(r'\s+', '', re.split(r'\s*→\s*', MARK.sub('', str(l)).strip())[-1])


def result_of(l):
    return nres(re.split(r'\s*→\s*', MARK.sub('', str(l)).strip())[-1])


def split_top(s, seps):
    out, d, cur = [], 0, ''
    for ch in s:
        if ch in '（(“〔':
            d += 1
        elif ch in '）)”〕':
            d = max(0, d - 1)
        if d == 0 and ch in seps:
            out.append(cur)
            cur = ''
        else:
            cur += ch
    out.append(cur)
    return out


def split_steps(body):
    """只在按顺序出现的下一个编号处切（①、②、③……），括号、〔〕里的不算"""
    out, d, cur, nxt = [], 0, '', 0
    for i, ch in enumerate(body):
        if ch in '（(〔':
            d += 1
        elif ch in '）)〕':
            d = max(0, d - 1)
        if d == 0 and nxt < len(CIRC) and ch == CIRC[nxt] and (not cur.strip() or body[i - 1].isspace()):
            if cur.strip():
                out.append(cur.strip())
            cur = ''
            nxt += 1
        cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def zh(t):
    return {c for c in re.sub(r'（[^（）]*）|\([^()]*\)', '', str(t)) if '\u4e00' <= c <= '\u9fff'}


def covered(sense, nodes):
    a = zh(sense)
    return bool(a) and any(sense.strip() and (sense.strip() in n or len(a & zh(n)) >= min(2, len(a))) for n in nodes)


def cut_here(line):
    """后缀行 → (去掉“在这里”一段后的行, “在这里：”后面那一段)"""
    k = line.find('在这里：')
    if k < 0:
        return line, None
    j = line.find('所以', k)
    if j >= 0:
        ends = [e for e in (line.find('；', j), line.find('。', j)) if e >= 0]
        e = min(ends) if ends else len(line)
    else:
        e, d = len(line), 0
        for i in range(k, len(line)):
            ch = line[i]
            if ch in '（(“':
                d += 1
            elif ch in '）)”':
                d = max(0, d - 1)
            elif ch == '；' and d == 0:
                e = i
                break
    seg = line[k + 4:e].strip().rstrip('；')
    before = line[:k].rstrip().rstrip('；，,')
    after = line[e:].lstrip('；。').strip()
    new = before + after if before.endswith('：') else before + ('；' + after if after else '')
    return new, seg


# ---------------------------------------------------------------- 新格式的小工具
def _top_positions(s, pat):
    """括号、引号外面 pat 出现的位置"""
    out, d, q = [], 0, 0
    for i, ch in enumerate(s):
        if ch in '（(〔':
            d += 1
        elif ch in '）)〕':
            d = max(0, d - 1)
        elif ch == '“':
            q += 1
        elif ch == '”':
            q = max(0, q - 1)
        elif d == 0 and q == 0 and s.startswith(pat, i):
            out.append(i)
    return out


def pos_head(text):
    """词性变化的文字“动词 → 名词。X“…”加上……” → “动词 → 名词”"""
    t = str(text or '').strip()
    return t.split('。', 1)[0].strip() if '。' in t else t


def pos_sentence(text):
    t = str(text or '').strip()
    return t.split('。', 1)[1].strip() if '。' in t else ''


def eq_from_sentence(sent):
    """“X“…”加上 -xx（…），就成了“…””→ 后缀等式“X“…”+ -xx（…）=“…””；认不出返回 None"""
    m = SENT.match(str(sent or '').strip())
    if not m or not m.group('base').strip():
        return None
    base = m.group('base').strip()
    sep = '' if base.endswith(('”', '）')) else ' '
    return '%s%s+ %s%s=“%s”%s' % (base, sep, m.group('suf'), m.group('sm') or '', m.group('res'), m.group('tail'))


def sentence_from_eq(line):
    """后缀等式 → “X“…”加上 -xx（…），就成了“…””；不是后缀等式返回 None"""
    s = str(line or '').strip()
    if not s or s[0] in '→⇒（(【　' or STEP.match(s) or s.startswith('用词规律') or '+ -' not in s:
        return None
    eqs = _top_positions(s, '=')
    if not eqs:
        return None
    i = eqs[0]
    right = s[i + 1:].lstrip()
    if not right.startswith('“'):
        return None
    d, j = 0, -1
    for k, ch in enumerate(right):
        if ch == '“':
            d += 1
        elif ch == '”':
            d -= 1
            if d == 0:
                j = k
                break
    if j < 0:
        return None
    res, tail = right[1:j], right[j + 1:]
    left = s[:i].rstrip()
    ks = _top_positions(left, '+ -')
    if not ks:
        return None
    base, sufsm = left[:ks[-1]].rstrip(), left[ks[-1] + 1:].strip()
    m = re.match(r'^(-[^\s（，,]+)\s*(（(?:[^（）]|（[^（）]*）)*）)?\s*$', sufsm)
    if not m or not base:
        return None
    sep = '' if base.endswith(('”', '）')) else ' '
    return '%s%s加上 %s%s，就成了“%s”%s' % (base, sep, m.group(1), m.group(2) or '', res, tail)


def parse_tail(body):
    """“（-less、-ly）：名词 → 形容词 → 副词”或“（-ize）：A → B；（-er）：B → C” → [(标签, 词性变化)]"""
    out = []
    for seg in re.split(r'；(?=（)', str(body or '')):
        m = re.match(r'^（((?:[^（）]|（[^（）]*）)+)）[：:]\s*(.*)$', seg.strip())
        if not m:
            continue
        labs = [x.strip() for x in split_top(m.group(1), '、') if x.strip()]
        chain = m.group(2).strip()
        if len(labs) == 1:
            out.append((labs[0], chain))
            continue
        nodes = [x.strip() for x in split_top(chain, '→') if x.strip()]
        if len(nodes) == len(labs) + 1:
            out += [(labs[k], nodes[k] + ' → ' + nodes[k + 1]) for k in range(len(labs))]
        else:
            out.append((m.group(1).strip(), chain))           # “-et、-in”合写一行的，当一个标签
    return out


def compose_tail(pos):
    """[(标签, 词性变化文字)] → “；词性变化（-or）：动词 → 名词”；几个后缀接成一条：（-less、-ly）：名词 → 形容词 → 副词"""
    heads = [(lab, pos_head(t)) for lab, t in pos]
    if not heads:
        return ''
    if len(heads) == 1:
        return '；词性变化（%s）：%s' % heads[0]
    core = lambda t: re.sub(r'（[^（）]*）', '', t).strip()
    nodes, ok = [], True
    for k, (lab, h) in enumerate(heads):
        ab = [x.strip() for x in split_top(h, '→') if x.strip()]
        if len(ab) != 2:
            ok = False
            break
        if k == 0:
            nodes = ab[:]
        elif core(nodes[-1]) == core(ab[0]):
            nodes.append(ab[1])
        else:
            ok = False
            break
    if ok:
        chain = nodes[0]
        for x in nodes[1:]:
            chain += ('→ ' if chain.endswith('）') else ' → ') + x
        return '；词性变化（%s）：%s' % ('、'.join(l for l, _ in heads), chain)
    return '；词性变化' + '；'.join('（%s）：%s' % x for x in heads)


def rule_body(text):
    """用词规律去掉最后那对括号（例子），用来认“同一条规律”"""
    t = str(text or '').strip()
    m = re.search(r'（((?:[^（）]|（[^（）]*）)*)）\s*$', t)
    return re.sub(r'\s+', '', t[:m.start()] if m else t)


def short_rule(text, word):
    """同一条规律再用到时：括号里本词的例子去掉（这一步就写在上面），只留熟悉的例子"""
    t = str(text or '').strip()
    m = re.search(r'（((?:[^（）]|（[^（）]*）)*)）\s*$', t)
    if not m or not word:
        return t
    items = [x.strip() for x in split_top(m.group(1), '；') if x.strip()]
    w = re.escape(str(word).lower())
    keep = [x for x in items if not re.match(w + r"(s|es|'s)?(?=[\s：:（(]|$)", x.lower())]
    body = t[:m.start()].rstrip()
    return body + ('（%s）' % '；'.join(keep) if keep else '')


def _eq_needed(d, k):
    """第 k 个后缀的等式要不要单写一行。写：派生路线（第一行看不到后缀的意思）、几个后缀（要讲中间一步）、
    句子末尾还有别的说明、带着第一行看不到的“本义”。不写：只有一个后缀，第一行的等式已经是“前面部分 + 后缀 = 字面意思”"""
    if len(d['pos']) != 1:
        return True
    from condense import top_eq_parts
    first = d['logic'][0] if d['logic'] else ''
    terms, lit, route = top_eq_parts(first)
    if route or not terms:
        return True
    m = SENT.match(pos_sentence(d['pos'][k][1]))
    if not m:
        return True
    if m.group('tail').strip():
        return True
    zh = lambda t: {c for c in str(t) if '\u4e00' <= c <= '\u9fff'}
    l1 = ''.join(g for _, g in terms) + lit
    for x in re.findall(r'本义“([^“”]*)”', m.group('base')):
        if not zh(x) <= zh(l1):
            return True
    return False


def _first_from_line1(d):
    """第一行（不含词性变化）的等式拼成“前面部分加上 -xx”，等式不单写时用来还原内部的那句话"""
    from condense import top_eq_parts
    terms, lit, route = top_eq_parts(d['logic'][0] if d['logic'] else '')
    return terms, lit


# ---------------------------------------------------------------- 组合列的结构
def parse_I(I, word=''):
    """组合列 → {logic: [等式 + 步骤等行], pos: [(标签, 文字)], rules: {编号: 文字}, blocks: [(段名, [行])]}；
    新格式（第一行末尾的词性变化、后缀等式、不编号的用词规律）、融合格式（词性变化（…）：、　用词规律①：）、
    更早的【词性变化】【用词规律】两段都认。内部一律还原成：pos 文字是“词性。……加上 -xx（…），就成了“…””，步骤末尾带〔用词规律①〕"""
    L = str(I or '').replace('\r', '').split('\n') if I else []
    d = {'logic': [], 'pos': [], 'rules': {}, 'blocks': [], 'word': word}
    if not L or not L[0].startswith('【构词逻辑】'):
        d['raw'] = L
        return d
    tail = None
    mt = TAILPOS.search(L[0])
    if mt:
        tail = parse_tail(mt.group(1))
        L = [L[0][:mt.start()].rstrip()] + L[1:]
    cur = None
    eqs = []
    bodies = {}
    for k, l in enumerate(L):
        m = SEGHEAD.match(l) if k else None
        if m:
            cur = [m.group(1), [l]]
            d['blocks'].append(cur)
            continue
        if cur is None:
            pm, rm, nm = POSLINE.match(l), RULELINE.match(l), RULE_NEW.match(l) if k else None
            if pm:
                d['pos'].append((pm.group(1).strip(), pm.group(2).strip()))
            elif rm:
                d['rules'][rm.group(1)] = rm.group(2).strip()
                bodies.setdefault(rule_body(rm.group(2)), rm.group(1))
            elif nm:
                txt = nm.group(1).strip()
                b = rule_body(txt)
                if b in bodies:
                    n = bodies[b]
                else:
                    n = CIRC[len(d['rules']) % len(CIRC)]
                    while n in d['rules']:
                        n = CIRC[(CIRC.index(n) + 1) % len(CIRC)]
                    d['rules'][n] = txt
                    bodies[b] = n
                st = next((i for i in range(len(d['logic']) - 1, 0, -1) if STEP.match(d['logic'][i])), None)
                if st is not None and ('〔用词规律' + n + '〕') not in d['logic'][st] and n not in ''.join(MARK.findall(d['logic'][st])):
                    ms = MARK.findall(d['logic'][st])
                    if ms:
                        d['logic'][st] = MARK.sub('', d['logic'][st]).rstrip() + '〔用词规律' + ''.join(ms) + n + '〕'
                    else:
                        d['logic'][st] = d['logic'][st].rstrip() + '〔用词规律' + n + '〕'
            elif tail is not None and k and not any(STEP.match(x) for x in d['logic'][1:]) and sentence_from_eq(l):
                eqs.append(sentence_from_eq(l))
            else:
                d['logic'].append(l)
        else:
            cur[1].append(l)
    if tail is not None:
        # 后缀等式按顺序配给各个后缀；没单写的，用第一行的等式还原内部那句话
        terms, lit = _first_from_line1(d)
        base_terms = terms[:-1]
        for i, (lab, head) in enumerate(tail):
            sent = eqs[i] if i < len(eqs) else ''
            if not sent and not terms:
                sent = '%s 加上 %s，就成了“%s”' % (word or '这个词', lab.split('（')[0], lit or word)
            if not sent and terms:
                parts = [t for t, _ in base_terms]
                semi = lambda t: str(t or '').replace('；', '、')        # 这句话视频按“；”切，还原时和 condense 一样换成“、”
                if len(base_terms) == 1 and base_terms[0][1]:
                    base = '%s“%s”' % (base_terms[0][0], semi(base_terms[0][1]))
                else:
                    base = ' + '.join(parts)
                sm = semi(terms[-1][1])
                sep = '' if base.endswith(('”', '）')) else ' '
                sent = '%s%s加上 %s%s，就成了“%s”' % (base, sep, lab.split('（')[0], '（%s）' % sm if sm else '', semi(lit))
            d['pos'].append((lab, head + ('。' + sent if sent else '')))
    keep = []
    for name, lines in d['blocks']:
        body = [re.sub(r'^\s*【' + name + r'】', '', lines[0]).strip()] + lines[1:]
        body = [x for x in body if x.strip()]
        if name == '词性变化':
            for x in body:
                if '：' in x:
                    lab, txt = x.split('：', 1)
                    d['pos'].append((lab.strip(), txt.strip()))
        elif name == '用词规律':
            for x in split_steps(' '.join(body)):
                m = re.match(r'^([①②③④⑤⑥⑦⑧⑨⑩])\s*(.*)$', x)
                if m:
                    d['rules'][m.group(1)] = m.group(2).strip()
        else:
            keep.append((name, lines))
    d['blocks'] = keep
    return d


def compose_I(d):
    """内部结构 → 新格式（清爽版）：词性变化并进第一行；后缀等式只在第一行看不到时单写；用词规律不编号，写在用到它的每一步下面"""
    if 'raw' in d:
        return '\n'.join(d['raw'])
    logic = list(d['logic'])
    word = d.get('word', '')
    first = logic[0] if logic else ''
    out = [first + compose_tail(d['pos'])] if d['pos'] else [first]
    for k, (lab, txt) in enumerate(d['pos']):
        eq = eq_from_sentence(pos_sentence(txt))
        if eq and _eq_needed(d, k):
            out.append(eq)
    placed = set()
    rest = logic[1:]
    last_step = max([i for i, l in enumerate(rest) if STEP.match(l)], default=-1)
    for i, l in enumerate(rest):
        if STEP.match(l):
            ms = ''.join(dict.fromkeys(''.join(MARK.findall(l))))      # 〔用词规律①①〕这种重复标的，只算一次
            keep = ''.join(n for n in ms if n not in d['rules'])       # 规律已搬走（merge 不建“意思怎么变”时）的编号留在步骤上
            out.append(MARK.sub('', l).rstrip() + ('〔用词规律%s〕' % keep if keep else ''))
            for n in ms:
                if n not in d['rules']:
                    continue
                out.append('　用词规律：' + (d['rules'][n] if n not in placed else short_rule(d['rules'][n], word)))
                placed.add(n)
        else:
            out.append(l)
        if i == last_step:
            for n in sorted(d['rules'], key=CIRC.index):
                if n not in placed:
                    out.append('　用词规律：' + d['rules'][n])
                    placed.add(n)
    for n in sorted(d['rules'], key=CIRC.index):
        if n not in placed:
            out.append('　用词规律：' + d['rules'][n])
    for name, lines in d['blocks']:
        out += lines
    return '\n'.join(out)


def step_nodes(logic):
    nodes = []
    for l in logic[1:]:
        if STEP.match(l):
            s = MARK.sub('', l).strip()
            s = re.sub(r'^[→⇒]\s*', '', s)
            s = re.sub(r'^[\u2460-\u2473]\s*(?:[^，。→“”（）]{1,16}[：:])?', '', s)
            nodes += [x.strip() for x in split_top(s, '→') if x.strip()]
    return nodes


def trim_so(d):
    """词性变化末尾“所以 W 是/指 A / B / C”：步骤里都讲到了就去掉"""
    nodes = step_nodes(d['logic'])
    if not nodes:
        return 0
    n = 0
    for k, (lab, txt) in enumerate(d['pos']):
        m = re.search(r'[，,]\s*所以\s+\S+\s*(?:是|指)\s*(.+)$', txt)
        if not m:
            continue
        senses = [x.strip() for x in m.group(1).split('/') if x.strip()]
        if senses and all(covered(x, nodes) for x in senses):
            d['pos'][k] = (lab, txt[:m.start()].rstrip('，, '))
            n += 1
    return n


def fold_evolution(d):
    """【演变】里的每一项都能在步骤里找到同一个意思：把年代并进那一步，去掉【演变】；有一项找不到就整段留着"""
    bi = next((i for i, (name, _) in enumerate(d['blocks']) if name == '演变'), None)
    if bi is None:
        return False
    lines = d['blocks'][bi][1]
    text = ' '.join([re.sub(r'^\s*【演变】', '', lines[0])] + lines[1:]).strip()
    if not text or '。' in text:
        return False
    items = [x.strip() for x in split_top(text, '→；') if x.strip()]
    logic = d['logic']
    idx = [i for i in range(1, len(logic)) if STEP.match(logic[i])]
    if not items or not idx:
        return False
    plan = []
    for it in items:
        m = re.match(r'^((?:[（(][^（）()]*[）)]\s*)*)(.*)$', it)
        pre, sense = m.group(1), m.group(2).strip()
        pars = [x.strip() for x in re.findall(r'[（(]([^（）()]*)[）)]', it)]
        dates = [x for x in pars if PURE_DATE.match(x)]
        whole = '\n'.join(logic)
        if any(x and not PURE_DATE.match(x) and not re.fullmatch(r'(v|n|adj|adv|vt|vi)\.?|名|动|形|副', x) and x not in whole for x in pars):
            return False                                   # 演变里括号中的说明（“已废”“最早指伦敦”“14 世纪初已作姓氏”……）步骤里没有，整段留着
        sense = re.sub(r'（[^（）]*）|\([^()]*\)', '', sense).strip()
        a = zh(sense)
        if not a:
            return False
        # 这一项讲的意思在哪一步里：整步（括号里的字也算）要包含这一项几乎所有的字；两三个字的短项要原样出现
        allz = lambda t: {c for c in str(t) if '\u4e00' <= c <= '\u9fff'}
        best, tie = None, False
        for i in idx:
            body = MARK.sub('', logic[i])
            ok = sense in body if len(a) <= 3 else len(a & allz(body)) / len(a) >= 0.85
            if not ok:
                continue
            sc = len(a & allz(body)) / len(allz(body) or {1})
            if best is None or sc > best[0]:
                best, tie = (sc, i), False
            elif sc == best[0]:
                tie = True
        if best is None or tie:
            return False
        nodes = [x for x in split_top(MARK.sub('', logic[best[1]]), '→') if x.strip()]
        node = max(nodes, key=lambda n: len(a & allz(n)))
        plan.append((best[1], node, dates[0] if dates else ''))
    done = set()
    lead = re.compile(r'^\s*(?:[→⇒]\s*)?(?:[\u2460-\u2473]\s*)?(?:[^，。→“”（）]{1,16}[：:])?\s*')
    for i, node, date in plan:
        if not date or (i, node) in done or DATE.search(''.join(re.findall(r'[（(]([^（）()]*)[）)]', node))) or date in logic[i]:
            continue                                   # 这一步里已经写了年代（或同一个年代写在别的地方），不再加
        line = logic[i]
        body = MARK.sub('', line)
        first = split_top(body, '→')[0]
        if node == first:                              # 第一段：年代放在“→ ”“① 名词：”这些开头的后面，不能放到最前面
            m = lead.match(line)
            line = line[:m.end()] + '（' + date + '）' + line[m.end():]
        else:
            core = node.strip()
            if not core or line.count(core) != 1:
                continue
            line = line.replace(core, '（' + date + '）' + core, 1)
        logic[i] = line
        done.add((i, node))
    del d['blocks'][bi]
    return True


# ---------------------------------------------------------------- 搬、还原
def split_cell(H, I, fold=True, word=''):
    """各部分解释里的组合内容 → 组合列，并融合。返回 (新 H, 新 I, 说明)"""
    H = str(H or '').replace('\r', '').split('\n') if H else []
    info = {'here': [], 'evo': False, 'rules': False, 'added_steps': 0, 'trim': 0, 'fold': False}
    d = parse_I(I, word)
    if 'raw' in d:
        return '\n'.join(H), compose_I(d), info
    newH, evo, rules = [], None, None
    for l in H:
        s = l.strip()
        if s.startswith('意思怎么变：'):
            evo = s
            continue
        if s.startswith('用词规律：'):
            rules = s
            continue
        if '在这里：' in l and '：' in l:
            new, seg = cut_here(l)
            if seg:
                lab = l.split('：', 1)[0]
                d['pos'] = [p for p in d['pos'] if p[0] != lab] + [(lab, seg)]
                info['here'].append(lab)
                newH.append(new)
                continue
        newH.append(l)
    logic = d['logic']
    if evo:
        info['evo'] = True
        body = re.sub(r'^意思怎么变：\s*', '', evo)
        body = re.sub(r'^从字面的“[^”]*”出发：\s*', '', body)
        used = set()
        for st in split_steps(body):
            marks = MARK.findall(st)
            txt = MARK.sub('', re.sub(r'^[①②③④⑤⑥⑦⑧⑨⑩]\s*', '', st)).strip()
            idx = [k for k in range(1, len(logic)) if STEP.match(logic[k]) and k not in used]
            hit = next((k for k in idx if full_of(logic[k]) == full_of(txt)), None)
            if hit is None:
                hit = next((k for k in idx if raw_result(logic[k]) == raw_result(txt)), None)
            if hit is None:
                hit = next((k for k in idx if result_of(logic[k]) == result_of(txt)), None)
            tag = ''.join('〔用词规律' + m + '〕' for m in marks)
            if hit is not None:
                used.add(hit)
                if tag and tag not in logic[hit]:
                    logic[hit] = logic[hit].rstrip() + tag
            elif txt and not txt.startswith('【'):
                logic.append('→ ' + txt + tag)
                used.add(len(logic) - 1)
                info['added_steps'] += 1
    if rules:
        info['rules'] = True
        for x in split_steps(re.sub(r'^用词规律：\s*', '', rules)):
            m = re.match(r'^([①②③④⑤⑥⑦⑧⑨⑩])\s*(.*)$', x)
            if m:
                d['rules'][m.group(1)] = m.group(2).strip()
    info['trim'] = trim_so(d)
    if fold:
        info['fold'] = fold_evolution(d)
    # 精简：词性变化只讲重点（后缀的意思 + 合起来成了什么）
    first = d['logic'][0] if d['logic'] else ''
    before = (list(d['pos']), dict(d['rules']))
    d['pos'] = [(lab, condense(word, lab, txt, '\n'.join(newH), first)) for lab, txt in d['pos']]
    # 用词规律括号里本词的例子（communication 交流、沟通 → 信息、消息）是规律用在这个词上的要点，保留
    info['condense'] = sum(a != b for a, b in zip(before[0], d['pos'])) + sum(before[1][n] != d['rules'][n] for n in d['rules'])
    return '\n'.join(newH), compose_I(d), info


def merge_cell(H, I, with_evo=True):
    """反向：组合列里的词性变化插回各后缀行（“在这里：”），〔用词规律〕和用词规律还原成各部分解释里的两行"""
    H = str(H or '').replace('\r', '').split('\n') if H else []
    d = parse_I(I)
    if 'raw' in d:
        return '\n'.join(H), compose_I(d)
    for lab, seg in d['pos']:
        k = next((i for i, l in enumerate(H) if l.split('：', 1)[0] == lab and '在这里：' not in l), None)
        if k is None:
            continue
        H[k] = H[k].rstrip().rstrip('；') + '；在这里：' + seg            # 接在这一行末尾，再分时原样切回
    logic = d['logic']
    idx = [k for k in range(1, len(logic)) if STEP.match(logic[k])]
    want = bool(d['rules']) or any(MARK.search(logic[k]) for k in idx)
    if isinstance(with_evo, str):
        want = '意思演变' in with_evo
    if want and idx:
        steps = []
        for n, k in enumerate(idx):
            marks = ''.join('〔用词规律' + m + '〕' for m in MARK.findall(logic[k]))
            txt = re.sub(r'^[\u2460-\u2473]\s*', '', re.sub(r'^[→⇒]\s*', '', MARK.sub('', logic[k]).strip()))
            logic[k] = MARK.sub('', logic[k]).rstrip()
            steps.append(CIRC[n % 10] + ' ' + txt + marks)
        H.append('意思怎么变：' + ' '.join(steps))
    if d['rules']:
        H.append('用词规律：' + ' '.join(n + ' ' + d['rules'][n] for n in sorted(d['rules'], key=CIRC.index)))
    d['pos'], d['rules'] = [], {}
    return '\n'.join(H), compose_I(d)


def count_combo(H):
    H = str(H or '')
    return {'在这里': H.count('在这里：'), '意思怎么变': H.count('意思怎么变：'), '用词规律': H.count('用词规律：')}


# ---------------------------------------------------------------- 表格
def _fit(ws, r):
    import math
    dw = lambda s: sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)
    best = 1
    import cols as C
    for col in C.TEXT_COLS:   # 有文字的列
        w = (ws.column_dimensions[col].width or 10) - 1.5
        v = str(ws[f'{col}{r}'].value or '')
        best = max(best, sum(max(1, math.ceil(dw(l) / w)) for l in v.split('\n')))
    ws.row_dimensions[r].height = round(min(409, best * 17.25), 2)


def run(mode, src, out, note=None, fold=True):
    import copy
    from openpyxl import load_workbook
    from openpyxl.styles import PatternFill, Alignment
    import cols as C
    wb = load_workbook(src)
    ws = wb['拆分结果']
    NR = ws.max_row
    st = dict(rows=0, here=0, evo=0, rules=0, added_steps=0, trim=0, fold=0)
    for r in range(2, NR + 1):
        H, I = C.get_parts(ws, r), ws.cell(r, C.COMBO).value   # 各部分解释（前缀、词根、单词部分、后缀四列合起来）、组合
        if mode == 'split':
            h2, i2, info = split_cell(H, I, fold=fold, word=str(ws.cell(r, 5).value or ''))
        elif mode == 'reformat':
            h2, i2, info = str(H or ''), compose_I(parse_I(I, str(ws.cell(r, 5).value or ''))), None
        else:
            h2, i2 = merge_cell(H, I, with_evo=str(ws.cell(r, C.ADJ).value or ''))
            info = None
        if h2 != str(H or '') or i2 != str(I or ''):
            C.set_parts(ws, r, h2 if h2 else H)
            ws.cell(r, C.COMBO).value = i2 if i2 else I
            st['rows'] += 1
            if info:
                st['here'] += len(info['here'])
                st['evo'] += info['evo']
                st['rules'] += info['rules']
                st['added_steps'] += info['added_steps']
                st['trim'] += info['trim']
                st['fold'] += info['fold']
            if note and mode == 'reformat':
                p = ws.cell(r, C.ADJ)
                p.value = (str(p.value) + '；' if p.value else '') + note + '：组合列按清爽格式重写'
            elif note:
                p = ws.cell(r, C.ADJ)
                p.value = (str(p.value) + '；' if p.value else '') + note + '：组合列融合（词性变化接在等式下，用词规律接在用到它的那一步下' + \
                    ('，演变的年代并进步骤' if info and info['fold'] else '') + '）'
            _fit(ws, r)
    if note and mode != 'reformat':
        R = wb['整表核对记录']
        n0 = sum(1 for row in R.iter_rows(min_row=2, values_only=True) if row[0] is not None)
        what = '组合列里，从各部分解释搬来的【词性变化】【用词规律】放在最下面，和原有的意思演变步骤、【演变】各讲各的，同一个意思讲了两三遍（communicate 的“所以 communicate 是交流、沟通 / 传达 / 传染”、【演变】“（1520s）……→ 交流、沟通”）'
        how = (f'按意思融合成一条线，涉及 {st["rows"]} 行：词性变化接在等式下面，末尾和步骤重复的“所以 W 指……”去掉 {st["trim"]} 处（有步骤没讲到的意思才留着）；'
               f'用词规律接在第一次用到它的那一步下面（编号和步骤末尾的〔用词规律N〕对上）；【演变】全被步骤讲到的 {st["fold"]} 段，年代并进步骤、去掉这一段，步骤里没有的历史照旧留在【演变】')
        for cc, v in enumerate([n0 + 1, '已修正', '—', '组合列融合', what, how], 1):
            cell = R.cell(n0 + 2, cc)
            cell.value = v
            cell._style = copy.copy(R.cell(2, 4)._style)
            cell.alignment = Alignment(wrap_text=True, vertical='top')
        R.cell(n0 + 2, 2).fill = PatternFill('solid', start_color='E2EFDA')
        R.row_dimensions[n0 + 2].height = 120.75
        R.auto_filter.ref = f'A1:F{R.max_row}'
    wb.save(out)
    return st


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    mode = sys.argv[1]
    if mode == 'check':
        from openpyxl import load_workbook
        ws = load_workbook(sys.argv[2], read_only=True)['拆分结果']
        tot = {'在这里': 0, '意思怎么变': 0, '用词规律': 0}
        import cols as C
        for r in ws.iter_rows(min_row=2, values_only=True):
            for k, v in count_combo(C.legacy(r)[9]).items():
                tot[k] += v
        print('各部分解释里还剩的组合内容：', tot)
    else:
        note = sys.argv[sys.argv.index('--note') + 1] if '--note' in sys.argv else None
        print(run(mode, sys.argv[2], sys.argv[3], note))

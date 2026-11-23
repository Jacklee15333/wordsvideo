# -*- coding: utf-8 -*-
"""第 126 条（第七十五版，详细考点轮）：「考点」列写详细——取代第 121 条“只写常考的一两行”。
用户：“看看总词库里面是否有考点这一列的数据，我希望能把这个数据补全，补详细，对应的是上海初中英语的考点”。

三档：
  ① 单元表 40 个词（7A-U4：camera … truly）：手写，kaodian_hand.HAND（变形、词性转换、短语、用法、易混五样都写全）。
  ② 考纲里的词（总表 1742 行）：照考纲词汇表、词组表补全——
       【变形】每个词性一组，规则的也写（名词复数，动词三单、过去式、过去分词、现在分词，形容词、副词的比较级、最高级），
               不规则、拼写变化（去 e、双写、y 变 i、f 变 v、加 es）括号里注明；考纲括号里标的形式照抄；代词、数词、国家和人照第 121 条。
       【词性转换】同根词（总表派生关系 + 考纲 + 复习资料），考纲里的排前面，最多 4 个。
       【短语】考纲词组表 + 总表「含义」里的 phr. + 表里的词组（alarm clock），最多 4 个。
       【用法】kaodian_data.USAGE（第 121 条手写的 172 条）+ 「含义」phr. 里带 doing / to do / sb. / sth. 的句型，最多 3 条。
       【易混】kaodian_data.CONFUSE + 「辨析」列里“A 侧重…；B 侧重…”这样对比的句子，最多 2 条。
  ③ 考纲外的词：按规则写变形、词性转换、短语（有 phr.、表里有词组的才有），用法、易混有现成材料的才写。
不可数名词：kaodian_data.UNCOUNT / BOTH + 这里的 MASS（常见的物质、抽象名词）+ -ness / -ism / 动名词结尾的；写“不可数”，不写复数。
形容词比较级：单音节、以 y / ow / le / er 结尾的双音节加 -er / -est；别的多音节只给考纲里的词写 more / most；不能比较的（wooden、main、daily…）不写。
"""
import re
from collections import OrderedDict

import kaodian as KD
import kaodian_data as D
from kaodian_hand import HAND

LIM = {'词性转换': 4, '短语': 4, '用法': 3, '易混': 2}
VOW = 'aeiou'
POS_RX = re.compile(r'^\s*((?:(?:modal |aux\. )?[a-z]+\.\s*/?\s*)+)')


# ---------------------------------------------------------------- 词性
def pos_list(T, K, w):
    """这个词有哪些词性（总表「含义」每一行开头的，再补考纲的），按出现的先后"""
    out = []
    n = T.words.get(w)
    if n is not None:
        for ln in T.v(T.data[n], '含义').split('\n'):
            m = POS_RX.match(ln)
            if not m:
                continue
            for p in re.split(r'\s*/\s*|\s+(?=[a-z]+\.)', m.group(1).strip()):
                p = p.strip()
                p = {'vt.': 'v.', 'vi.': 'v.', 'modal v.': 'aux.', 'aux. v.': 'aux.'}.get(p, p)
                if p and p not in out:
                    out.append(p)
    for p in K.pos(w):
        if p not in out:
            out.append(p)
    return out


# ---------------------------------------------------------------- 动词
def syl(w):
    """粗算音节数（够判断比较级用 -er 还是 more）"""
    s = w.lower()
    s = re.sub(r'(?<![aeiouy])e$', '', s) if not s.endswith(('le', 'ee', 'ye')) else s
    s = re.sub(r'(?<=[^aeiou])ed$', 'd', s) if len(s) > 4 else s
    return max(1, len(re.findall(r'[aeiouy]+', s)))


def third_person(w):
    if w in ('be',):
        return 'is', ''
    if w == 'have':
        return 'has', '不规则'
    if w in ('do', 'go'):
        return w + 'es', '加 es'
    if re.search(r'(s|x|z|ch|sh)$', w):
        return w + 'es', '加 es'
    if re.search(r'[^aeiou]y$', w):
        return w[:-1] + 'ies', 'y 变 i 加 es'
    if re.search(r'[^aeiou]o$', w):
        return w + 'es', '加 es'
    return w + 's', ''


def past_note(w, past):
    if past == w + 'ed':
        return ''
    if past == w + 'd' and w.endswith('e'):
        return '去 e 加 d'
    if re.search(r'[^aeiou]y$', w) and past == w[:-1] + 'ied':
        return 'y 变 i 加 ed'
    if past == w + w[-1] + 'ed':
        return '双写 %s' % w[-1]
    return '不规则'


def ing_note(w, ing):
    if ing == w + 'ing':
        return ''
    if w.endswith('ie') and ing == w[:-2] + 'ying':
        return 'ie 变 y 加 ing'
    if w.endswith('e') and ing == w[:-1] + 'ing':
        return '去 e 加 ing'
    if ing == w + w[-1] + 'ing':
        return '双写 %s' % w[-1]
    return ''


def pick_br(forms):
    """lemminflect 给两种拼法（signaled / signalled）：上海教材用英式，双写的排前面"""
    forms = [f for f in forms if f]
    if not forms:
        return None, None
    if len(forms) >= 2:
        dbl = [f for f in forms if re.search(r'(ll|pp|mm)(ed|ing)$', f)]
        if dbl:
            other = [f for f in forms if f != dbl[0]]
            return dbl[0], other[0] if other else None
    return forms[0], None


def lem(w, tag):
    try:
        from lemminflect import getInflection
        return list(getInflection(w, tag) or [])
    except Exception:
        return []


def verb_group(w, e):
    """v. 三单 …；过去式、过去分词 …；现在分词 …（括号里注明拼写变化、不规则）"""
    if ' ' in w:
        return ''
    chips = []
    t3, n3 = third_person(w)
    chips.append('三单 %s%s' % (t3, '（%s）' % n3 if n3 else ''))
    a = KD.ann_forms(e) if e else ''
    past = pp = None
    alt = ''
    if a:
        alts = [x.strip() for x in re.split(r'；|\s或\s', a) if x.strip()]
        pairs = [tuple(y.strip() for y in re.split(r'[,，]', x)) for x in alts]
        pairs = [p for p in pairs if len(p) == 2]
        if pairs:
            past = ' 或 '.join(dict.fromkeys(p[0] for p in pairs))
            pp = ' 或 '.join(dict.fromkeys(p[1] for p in pairs))
    if not past:
        p1, p2 = pick_br(lem(w, 'VBD'))
        q1, q2 = pick_br(lem(w, 'VBN'))
        past, pp = p1, q1 or p1
        if p2 and p2 != p1:
            alt = '美式 %s' % p2
    if not past:
        return ''
    if past == pp:
        note = past_note(w, past.split(' 或 ')[0])
        if alt:
            note = '英式双写 %s，%s' % (w[-1], alt) if note.startswith('双写') else (note + '，' + alt if note else alt)
        chips.append('过去式、过去分词 %s%s' % (past, '（%s）' % note if note else ''))
    else:
        note = '不规则' if past_note(w, past.split(' 或 ')[0]) == '不规则' or past_note(w, pp.split(' 或 ')[0]) == '不规则' else past_note(w, past)
        chips.append('过去式 %s、过去分词 %s%s' % (past, pp, '（%s）' % note if note else ''))
    g1, g2 = pick_br(lem(w, 'VBG'))
    if g1:
        nt = ing_note(w, g1)
        chips.append('现在分词 %s%s' % (g1, '（%s）' % nt if nt else ''))
    return '；'.join(chips)


# ---------------------------------------------------------------- 名词
MASS = set('''rice bread milk water juice tea coffee meat beef pork mutton chicken money information news advice homework housework
weather music furniture luggage baggage equipment knowledge traffic fun health help luck progress rubbish litter pollution air oil
snow rain ice sand salt sugar butter cheese cream soup toast jam honey grass cotton wool silk gold silver iron steel plastic sunshine
sunlight heat energy electricity freedom happiness love peace safety respect patience courage importance research evidence permission
harm wealth education scenery clothing jewellery jewelry machinery poetry mud dust smoke fog thunder lightning snowfall rainfall
weight height length width depth strength warmth youth childhood homework spelling grammar vocabulary software hardware garbage trash
cash change applause laughter nonsense mathematics physics economics politics athletics gymnastics chemistry biology geography history
english chinese french german japanese russian spanish art science medicine shopping swimming cooking cleaning heating'''.split())
SAME_PL = set('sheep deer fish means series species aircraft spacecraft chinese japanese swiss'.split())
COUNT_ING = set('''building meeting painting drawing feeling beginning ending wedding morning evening ceiling crossing sibling earring
recording saying booking reading writing finding opening setting thing king ring string spring wing sling sting swing duckling
darling pudding stocking dumpling ending offering wedding outing serving helping blessing warning greeting stuffing filling crossing
belonging coming happening hearing landing marking pairing rating saving sitting timing training'''.split())


def noun_group(T, K, w, e, main=True):
    if ' ' in w or w[:1].isupper():
        return ''
    n = T.words.get(w)
    mean = T.v(T.data[n], '含义') if n is not None else ''
    if w in MASS or re.search(r'(ness|ism)$', w) or (w.endswith('ing') and w not in COUNT_ING and len(w) > 5) \
            or re.search(r'n\.[^\n]*（不可数', mean) and not re.search(r'可数[^不]', mean):
        if w in D.BOTH:
            return D.BOTH[w]
        return '不可数，没有复数'
    if w in D.BOTH:
        return D.BOTH[w]
    p1, _ = pick_br(lem(w, 'NNS'))
    if not p1:
        return ''
    if p1 == w:
        return '单复数同形' if w in SAME_PL else '不可数，没有复数'
    # 复数在语料里几乎见不到、单数又常见的（independence、heating、furniture）：一般不可数
    if KD.zipf(w) >= 2.8 and KD.zipf(p1) < 1.6:
        return '一般不可数，不加 s'
    if not main and p1 in (w + 's', w + 'es'):
        return ''
    if p1 == w + 's':
        return '复数 %s' % p1
    if p1 == w + 'es':
        return '复数 %s（加 es）' % p1
    if re.search(r'[^aeiou]y$', w) and p1 == w[:-1] + 'ies':
        return '复数 %s（y 变 i 加 es）' % p1
    if re.search(r'fe?$', w) and p1.endswith('ves'):
        return '复数 %s（f、fe 变 v 加 es）' % p1
    if w.endswith('man') and p1 == w[:-3] + 'men':
        return '复数 %s（man 变 men）' % p1
    return '复数 %s（不规则）' % p1


# ---------------------------------------------------------------- 形容词、副词
IRR_ADJ = {'good': ('better', 'best'), 'well': ('better', 'best'), 'bad': ('worse', 'worst'), 'ill': ('worse', 'worst'),
           'badly': ('worse', 'worst'), 'many': ('more', 'most'), 'much': ('more', 'most'), 'little': ('less', 'least'),
           'far': ('farther 或 further', 'farthest 或 furthest'), 'old': ('older 或 elder', 'oldest 或 eldest')}
NONGRAD = set('''main whole own left right wrong real male female next last each every such same both mere sole prime chief top east west
north south only total daily weekly monthly yearly annual dead alive asleep awake wooden golden woollen woolen electric electrical
digital national international local medical musical chemical physical social political historical industrial agricultural
favourite favorite major minor senior junior former latter inner outer upper lower unique perfect pregnant impossible
square nuclear solar lunar plastic metal paper silver gold glass stone daily married single eastern western northern southern
central extra spare overall entire absolute personal public private official royal urban rural federal mental moral total
fellow former further former giant mini maximum minimum average'''.split())
TWO_ER = set('clever narrow simple gentle quiet polite able noble humble shallow hollow yellow mellow tender'.split())
FLAT_ADV = {'fast': ('faster', 'fastest'), 'hard': ('harder', 'hardest'), 'early': ('earlier', 'earliest'), 'late': ('later', 'latest'),
            'high': ('higher', 'highest'), 'low': ('lower', 'lowest'), 'near': ('nearer', 'nearest'), 'long': ('longer', 'longest'),
            'soon': ('sooner', 'soonest'), 'well': ('better', 'best'), 'badly': ('worse', 'worst'), 'much': ('more', 'most'),
            'little': ('less', 'least'), 'far': ('farther 或 further', 'farthest 或 furthest'), 'loud': ('louder', 'loudest'),
            'quick': ('quicker', 'quickest'), 'slow': ('slower', 'slowest'), 'close': ('closer', 'closest'), 'deep': ('deeper', 'deepest')}
MANNER_LY = set('''quickly slowly carefully carelessly clearly easily happily sadly loudly quietly politely seriously beautifully badly
heavily brightly warmly widely deeply closely freely safely strongly softly gently kindly patiently bravely correctly successfully
actively quickly angrily busily luckily noisily lazily healthily friendlily proudly rudely smoothly calmly comfortably confidently
honestly nervously peacefully perfectly quickly regularly silently smartly steadily strictly warmly wisely excitedly eagerly
fluently frequently often'''.split())


def er_forms(w):
    """单音节、以 y / ow / le / er 结尾的双音节：→ (比较级, 最高级, 说明)"""
    if w.endswith('e'):
        return w + 'r', w + 'st', '以 e 结尾，加 r、st'
    if re.search(r'[^aeiou]y$', w):
        return w[:-1] + 'ier', w[:-1] + 'iest', 'y 变 i'
    if syl(w) == 1 and re.search(r'[^aeiou][aeiou][^aeiouwxy]$', w) and not re.search(r'[aeiou]{2}[^aeiou]$', w):
        return w + w[-1] + 'er', w + w[-1] + 'est', '双写 %s' % w[-1]
    return w + 'er', w + 'est', ''


def adj_group(T, K, w, e, old_chip):
    if ' ' in w or w[:1].isupper() or w in NONGRAD or w.endswith(('ese', 'ish', 'en')) and K.get(w) is None:
        return old_chip or ''
    if old_chip:
        return old_chip
    if w in IRR_ADJ:
        a, b = IRR_ADJ[w]
        return '比较级 %s、最高级 %s（不规则）' % (a, b)
    s = syl(w)
    if w.startswith('un') and re.search(r'[^aeiou]y$', w) and syl(w[2:]) <= 2:
        a, b, nt = er_forms(w)
        return '比较级 %s、最高级 %s%s' % (a, b, '（%s）' % nt if nt else '')
    if s == 1 or (s == 2 and (re.search(r'[^aeiou]y$', w) or w.endswith(('ow', 'le', 'er')) or w in TWO_ER)):
        if w.endswith(('ed', 'ing')) or w in ('fun', 'own', 'live', 'like', 'ill'):
            return '比较级用 more、最高级用 most' if K.get(w) else ''
        a, b, nt = er_forms(w)
        return '比较级 %s、最高级 %s%s' % (a, b, '（%s）' % nt if nt else '')
    if K.get(w) and not re.search(r'(ic|al|ar|ary|ory)$', w) or w in ('beautiful', 'interesting', 'important', 'difficult', 'expensive', 'popular', 'famous', 'useful', 'careful', 'helpful'):
        return '比较级 more %s、最高级 most %s' % (w, w)
    return ''


def adv_group(T, K, w):
    if w in FLAT_ADV:
        a, b = FLAT_ADV[w]
        return '比较级 %s、最高级 %s%s' % (a, b, '（不规则）' if w in ('well', 'badly', 'much', 'little', 'far') else '')
    if w in MANNER_LY and (K.get(w) or KD.zipf(w) >= 4.0):
        return '比较级 more %s、最高级 most %s' % (w, w)
    return ''


# ---------------------------------------------------------------- 词性转换
def conv_full(T, K, w, old_chips):
    """考纲词：第 121 条写的（两头都在考纲、资料点名的）排前面；再补常用的同根词，最多 4 个"""
    out = OrderedDict()
    for ch in old_chips:
        key = re.sub(r'（.*$', '', ch).strip()
        out[key] = ch
    have = ' '.join(out.keys()).lower()
    mine = KD.posset(T, K, w)
    cands = []
    for c, (dirn, depth, kind) in KD.related(T, K, w).items():
        if c == w or re.search(r'\b%s\b' % re.escape(c), have) or c not in T.words:
            continue
        if re.fullmatch(re.escape(w.rstrip('y')) + r'(s|es|ies)', c) or re.fullmatch(re.escape(c.rstrip('y')) + r'(s|es|ies)', w):
            continue
        src = KD.pair_src(w, c)
        z = KD.zipf(c)
        if not (K.get(c) or src or z >= 3.4):
            continue
        pc = KD.show_pos(T, K, c, mine, child=w if dirn == 'up' else None)
        if pc not in KD.CONTENT:
            continue
        zh = K.zh(c, pc) or T.meaning_pos(c)[1]
        if not zh:
            continue
        note = KD.SPECIAL_CONV_NOTE.get((w, c)) or (KD.spell_note(w, c) if dirn == 'down' else '')
        score = (0 if K.get(c) else 1, 0 if pc not in mine else 1, depth, -z)
        cands.append((score, '%s %s %s%s' % (pc, c, zh, '（%s）' % note if note else '')))
    cands.sort()
    for _, ch in cands:
        if len(out) >= LIM['词性转换']:
            break
        out[re.sub(r'（.*$', '', ch).strip()] = ch
    return list(out.values())[:LIM['词性转换']]


# ---------------------------------------------------------------- 短语、用法
PATTERN = re.compile(r'\b(doing|to do|sb\.|sth\.|one\'s|oneself|that)\b')


def phr_lines(T, w):
    """总表「含义」里 phr. 那几行，一条一个（去掉“（1716 年已见）”这类年份）"""
    n = T.words.get(w)
    if n is None:
        return []
    out = []
    for ln in T.v(T.data[n], '含义').split('\n'):
        m = re.match(r'^\s*phr\.\s*(.+)$', ln)
        if not m:
            continue
        for it in KD.split_top(m.group(1), '；'):
            it = re.sub(r'[（(][^（）()]*(年|世纪|s）|已见|起)[^（）()]*[）)]', '', it).strip()
            it = re.sub(r'\s+', ' ', it)
            if not re.search(r'[\u4e00-\u9fff]', it) or not re.match(r'^[A-Za-z(…]', it) or len(it) > 34:
                continue
            out.append(it)
    return out


_MULTI = {}


def table_phrases(T, w):
    """表里收的词组（alarm clock、text message、keep track of）里有这个词的"""
    out = []
    if id(T) not in _MULTI:
        _MULTI[id(T)] = [(k, n) for k, n in T.words.items() if ' ' in k]
    for k, n in _MULTI[id(T)]:
        if w in k.split() and k != w:
            zh = T.meaning_pos(k)[1] or re.sub(r'^\s*[a-z.]+\s*', '', T.v(T.data[n], '含义').split('\n')[0]).split('；')[0]
            if zh:
                out.append('%s %s' % (k, zh))
    return out


def norm_en(t):
    return re.sub(r'[^a-z ]', '', re.split(r'[\u4e00-\u9fff（(]', t.lower())[0]).strip()


# ---------------------------------------------------------------- 易混（「辨析」列里对比的句子）
CMP = r'(侧重|重在|偏|多指|多说|多用于|强调|是|指)'
CMP_RX = re.compile(r'([A-Za-z][A-Za-z\-\']*(?: [a-z][a-z\-\']*){0,2})\s*' + CMP + r'\s*([^；。，]{2,24})')


def bianxi_confuse(T, w):
    n = T.words.get(w)
    if n is None:
        return []
    out = []
    for ln in T.v(T.data[n], '辨析').split('\n'):
        ln = ln.strip()
        if not ln or ln.startswith('【') or ln.startswith('逻辑不同'):
            continue
        heads = OrderedDict()
        for m in CMP_RX.finditer(ln):
            h = m.group(1).strip()
            if h.lower() in ('it', 'this', 'that', 'the', 'a', 'an') or len(h) < 2:
                continue
            desc = re.split(r'[（(]', m.group(3))[0].strip().rstrip('、，：:')
            if desc.count('“') > desc.count('”'):
                desc += '”'
            if len(desc) >= 2:
                heads.setdefault(h, (m.group(2), desc))
        heads = OrderedDict((h, v) for h, v in heads.items() if h.lower().split()[0] not in ('a', 'an', 'the', 'to', 'be'))
        mine = [h for h in heads if h.lower() == w or h.lower().split()[0] == w]
        others = [h for h in heads if h not in mine and w not in h.lower().split()]
        if mine and others:
            a, b = mine[0], others[0]
            da, db = heads[a], heads[b]
            chip = '%s / %s（%s %s%s，%s %s%s）' % (a, b, a, da[0], da[1], b, db[0], db[1])
            if len(chip) <= 80:
                out.append(chip)
        if len(out) >= LIM['易混']:
            break
    return out


# ---------------------------------------------------------------- 第 127 条：词性转换写成“单词 词性中文”
CONV_RX = re.compile(r'^(n|v|adj|adv|pron|prep|conj|num|int|art|aux)\.\s+([A-Za-z][A-Za-z\'’\- ]*?)\s+(\S.*)$')


def conv_fmt(chip):
    """第七十六版（用户：“考点部分，写单词的时候格式这样：protection n.保护；单词，词性，中文含义”）：
    n. protection 保护 → protection n.保护；true → truly（…）这种箭头的不动"""
    m = CONV_RX.match(chip.strip())
    return '%s %s.%s' % (m.group(2), m.group(1), m.group(3)) if m else chip.strip()


def fmt_kd(txt):
    """一格考点里【词性转换】那一行的每一块都换成新写法"""
    out = []
    for ln in str(txt or '').split('\n'):
        m = re.match(r'^【词性转换】\s*(.+)$', ln.strip())
        out.append('【词性转换】' + '；'.join(conv_fmt(c) for c in KD.split_top(m.group(1), '；')) if m else ln)
    return '\n'.join(out)


# ---------------------------------------------------------------- 一个词
def parse_rows(txt):
    rows = OrderedDict()
    for ln in str(txt or '').split('\n'):
        m = re.match(r'^【([^】]+)】\s*(.+)$', ln.strip())
        if m:
            rows[m.group(1)] = m.group(2)
    return rows


def full(T, K, n):
    """→ (考点, 依据)"""
    r = T.data[n]
    w0 = T.v(r, '单词').strip()
    w = w0.lower()
    if not w:
        return '', ''
    if w in HAND:
        return fmt_kd(HAND[w]), '【手写】第 126 条：单元表的词逐个手写（考纲词汇表、词组表、牛津上海版 7A Unit 4、上海中考常考题型）'
    old_kd, old_yj = KD.kaodian(T, K, n)
    old = parse_rows(old_kd)
    e = K.get(w)
    rows = OrderedDict()
    basis = OrderedDict((k, v) for k, v in parse_rows(old_yj).items())
    poss = pos_list(T, K, w)
    # ---------- 变形
    keep_old = bool(old.get('变形')) and (KD.inflected_row(w, K) or (e and (e.get('pron') or e.get('cardinal') or e.get('ordinal')
                                                  or e.get('people') or e.get('country'))) or w in ('be', 'can', 'may', 'shall', 'will', 'must', 'read', 'hang', 'lie')
                                          or w in D.VERB_NOTE)
    if keep_old:
        rows['变形'] = old['变形']
    elif ' ' in w:
        head = w.split()[0]
        if 'v.' in pos_list(T, K, head) or head in ('keep', 'take', 'make', 'get', 'go', 'put', 'give', 'look', 'turn', 'depend'):
            vg = verb_group(head, K.get(head))
            if vg:
                rows['变形'] = '%s %s' % (head, vg.replace('三单 ', '三单 ', 1))
        elif 'n.' in poss or not poss:
            last = w.split()[-1]
            pl, _ = pick_br(lem(last, 'NNS'))
            if pl and pl != last and last not in MASS and w not in ('health care',):
                rows['变形'] = 'n. 复数 %s' % (w[: len(w) - len(last)] + pl)
    else:
        old_groups = {}
        for g in (old.get('变形') or '').split(' / '):
            m = re.match(r'^(n\.|v\.|adj\.|adv\.)\s*(.+)$', g.strip())
            if m:
                old_groups[m.group(1)] = m.group(2)
        groups = []
        kp = [x for x in K.pos(w) if x in KD.CONTENT] if e else []
        use_pos = [p for p in poss if (p in kp or p == poss[0])] if kp else poss[:2]
        for p in use_pos:
            if p == 'v.' and not (e and e.get('pron')):
                g = verb_group(w, e)
                if g and w in ('be', 'have', 'do'):
                    g = old_groups.get('v.', g)
            elif p == 'n.':
                og = old_groups.get('n.') or ''
                g = (og if '不可数' in og else noun_group(T, K, w, e, main=(poss and poss[0] == 'n.'))) if w in MASS \
                    else (og or noun_group(T, K, w, e, main=(poss and poss[0] == 'n.')))
            elif p == 'adj.':
                g = adj_group(T, K, w, e, old_groups.get('adj.'))
            elif p == 'adv.' and 'adj.' not in [x for x in poss if x != 'adv.'][:1]:
                g = adv_group(T, K, w)
            else:
                g = ''
            if g and not any(x.startswith(p + ' ') for x in groups):
                groups.append('%s %s' % (p, g))
        if groups:
            rows['变形'] = ' / '.join(groups[:4])
            basis.setdefault('变形', '规则变化照评价指南·词形变化（名词复数、动词三单 / 过去式 / 过去分词 / 现在分词、形容词副词比较级）；'
                                    '不规则的照考纲括号里的标注和 lemminflect 的词形表')
    # ---------- 词性转换
    if not (e and (e.get('pron') or e.get('cardinal') or e.get('ordinal'))) and w not in ('be', 'being'):
        old_conv = KD.split_top(old.get('词性转换', ''), '；') if old.get('词性转换') else []
        if e and (e.get('country') or e.get('people')):
            conv = old_conv
        elif ' ' in w:
            conv = old_conv
        else:
            conv = conv_full(T, K, w, old_conv)
        done = rows.get('变形', '')
        conv = [c for c in conv if not re.search(r'\b%s\b' % re.escape((c.split() + ['', ''])[1]), done) or '→' in c]
        if conv:
            rows['词性转换'] = '；'.join(conv[:LIM['词性转换']])
            basis.setdefault('词性转换', '总表“拆分”“单词部分”的派生关系（评价指南·构词法：派生、转化）')
    # ---------- 短语、用法
    phr, use = [], []
    if old.get('短语'):
        phr += KD.split_top(old['短语'], '；')
    if old.get('用法'):
        use += KD.split_top(old['用法'], '；')
    if e and len(phr) < LIM['短语']:
        save = KD.MAXN['短语']
        KD.MAXN['短语'] = LIM['短语']
        try:
            more, _ = KD.phrase_line(K, w)
        finally:
            KD.MAXN['短语'] = save
        phr += more
    for it in phr_lines(T, w):
        (use if PATTERN.search(it) and len(use) < LIM['用法'] else phr).append(it)
    phr += table_phrases(T, w)
    seen, P2 = set(), []
    utext = ' '.join(norm_en(u) for u in use)
    for it in phr:
        k = norm_en(it)
        if not k or k in seen or (k in utext and len(k) > 3):
            continue
        seen.add(k)
        P2.append(it)
    if P2:
        rows['短语'] = '；'.join(P2[:LIM['短语']])
        basis.setdefault('短语', '考纲词组表 + 总表「含义」的 phr. + 表里收的词组')
    U2 = list(OrderedDict.fromkeys(use))
    if U2:
        rows['用法'] = '；'.join(U2[:LIM['用法']])
    # ---------- 易混
    conf = KD.split_top(old.get('易混', ''), '；') if old.get('易混') else []
    for c in bianxi_confuse(T, w):
        if len(conf) >= LIM['易混']:
            break
        a = c.split(' / ')[0].lower()
        if not any(a in x.lower() and c.split(' / ')[1].split('（')[0].lower() in x.lower() for x in conf):
            conf.append(c)
    if conf:
        rows['易混'] = '；'.join(conf[:LIM['易混']])
        basis.setdefault('易混', 'kaodian_data.CONFUSE + 总表「辨析」列')
    kd = fmt_kd('\n'.join('【%s】%s' % (k, rows[k]) for k in KD.LABELS if rows.get(k)))
    yj = '\n'.join('【%s】%s' % (k, basis.get(k, '—')) for k in KD.LABELS if rows.get(k))
    return kd, yj


def speed_up(T):
    """related() 里每个词都要把考纲 1724 个词的 prefix_root 算一遍：先缓存起来"""
    if getattr(T, '_pr_cached', False):
        return
    raw, cache = T.prefix_root, {}

    def pr(w):
        if w not in cache:
            cache[w] = raw(w)
        return cache[w]
    T.prefix_root = pr
    T._pr_cached = True


def build_all(T, K):
    speed_up(T)
    return [full(T, K, n) for n in range(len(T.data))]

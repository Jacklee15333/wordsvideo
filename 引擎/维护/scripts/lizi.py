# -*- coding: utf-8 -*-
"""复杂例词（project_rules.md 第 76 条：词根列；第 79–81 条：前缀列、后缀列）——解释一个部分的那一行里，不让学生去看更复杂的词。
  · 词缀行（前缀列、后缀列）的“同 例词”：例词要是“学生认识的单词 + 这个词缀”（unhappy、rewrite、teacher、quickly），一眼看得出词缀起了什么作用。
    例词自己还带着不能单独用的词根（progress = pro + gress、include = in + clude、create = cre + ate）的去掉——学生还得先拆它。
      例词在表里：它那一行「词根」列有不能单独用的词根（连接成分、“informat(=inform)”这类单词的过去分词词干不算）→ 去掉；
                  基础词、不好拆分、变体词（⑤ ④ ②）和没有词根的（单词 + 词缀、合成词）→ 留。
      例词不在表里：去掉这个词缀，剩下的是表里的词（replay → play、overeat → eat、teacher → teach）→ 留；不是 → 去掉。
                  逐个看过、和这条规则不一样的记在 lizi_data.py（OK_OUT 留、DROP_OUT 去掉、KEEP_IN 表里带词根也留）。
    留着不动的：讲变法的（同 possible → possibly、hop → hopping）、短语（同 turn over）、“为什么用 -er 不用 -or”那一行、辨析（原来的分工）里的例词、记法和音变里的对照。
  · 词缀行的“见 X”：X 只是含有同一个词缀的别的词（product 的 pro-“见 produce”、universe 的 uni-“见 unify”）去掉；
    X 是简单词（见 like、见 unhappy）、本词的另一种拼法（recognise 见 recognize）、“见 X 的【背景】”“详见 X”的照留；例外记在 lizi_data.SEE_KEEP。
  · 词根列（第 76 条）：“同 …”里同一个词根的“前缀 + 词根”“词根 + 词根”的词去掉；2026-11 例词清理轮补了三种上一轮漏掉的：
    两个字母的词根（circuit 的 it：exit、transit）、写法不一样的同一个词根（按拆分里的 (=X) 认：receive 的 ceive 和 accept 的 cept 都是 cap）、
    放在词根列的前缀成分（extreme 的 ex-：exit、export），和表里没有的“前缀 + 这个词根”的词（provoke 的 voke：invoke、revoke）。
  plan(data, C)        词根列 -> ({行下标: 新词根格}, [(单词, 标签, [去掉的例词], 原来那一行)])
  plan_affix(data, C)  前缀列、后缀列 -> ({(行下标, 'pre' / 'suf'): 新格}, [(行下标, 单词, 列, 标签, 做了什么, [去掉的], 原来那一行, 新的一行)])
  problems(data, C)    体检：还没去掉的（affix_ex、affix_see、root_ex 应为 0）
  python3 lizi.py <表.xlsx> [--show]   试算（写好的表应是 0）；--check 只打印体检数字
再跑一遍不变。"""
import re, sys, collections
import linetools as LT
import cols as CO
import parse as PA
import lizi_data as LD

SAME = re.compile(r'同\s+(?=[A-Za-z])')
VAR = re.compile(r'词根\s*([A-Za-z]+)\s*的另一种写法')
WORD = re.compile(r"^[A-Za-z][A-Za-z'’\-]*")
PHRASE = re.compile(r"^[A-Za-z][A-Za-z'’\-]*(?: [A-Za-z][A-Za-z'’\-]*)+")
ITEM_SPLIT = re.compile(r'、(?=\s*[A-Za-z])')
CONT = re.compile(r'^\s*[A-Za-z][A-Za-z\-]* [\u3400-\u9fff、]+：')          # “；forgo 放弃：走开、不要了”——上一段“同 …”接着举的例词
HAS_EXPL = re.compile(r'^[A-Za-z][A-Za-z\-]* [\u3400-\u9fff、]+：')

def core(lab):
    return re.sub(r'[（(][^（）()]*[）)]|[^A-Za-z]', '', lab or '').lower()

def index(data, C):
    by = {}
    for ri, r in enumerate(data):
        w = str(r[C['word']] or '').strip()
        if w and w.lower() not in by: by[w.lower()] = ri
    return by

def part_lines(r, C, col):
    """这一列里的部分行：[(标签, 解释)]（“为什么…”和说明行不算）"""
    out = []
    for l in str(r[C[col]] or '').split('\n'):
        lab, body = LT.label_body(l)
        if lab and not lab.startswith('为什么') and re.match(r'^-?[A-Za-z]', lab) and not CO.is_note_label(lab): out.append((lab, body))
    return out

def parts_of(r, C):
    """这个词的各部分：[(列, 标签核心)]"""
    return [(col, core(lab)) for col in ('pre', 'root', 'wp', 'suf') for lab, _ in part_lines(r, C, col)]

def split_keys(r, C):
    """拆分里每一部分的写法和括号里的 (=X)：{写法核心: {写法核心, X…}}"""
    out = {}
    for p in PA.parse_split(r[C['split']]) or []:
        k = core(p['surface'])
        if k: out.setdefault(k, {k}).update(e.lower() for e in p['eqs'] if re.fullmatch(r'[A-Za-z]+', e))
    return out

def bound_roots(r, C, by):
    """这一行里不能单独用的词根（标签核心）。不算：连接成分和双写的字母（-i-、-s-）、单词的过去分词词干（informat(=inform)：解释以“inform（…）”开头）"""
    w = str(r[C['word']] or '')
    sk = split_keys(r, C)
    out = []
    for lab, body in part_lines(r, C, 'root'):
        if CO.is_connector(lab, w): continue
        c = core(lab)
        stem = next((e for e in sk.get(c, ()) if e != c and e in by and str(body).lstrip().startswith(e + '（')), None)
        if stem: continue
        out.append(c)
    return out

def is_simple_type(r, C):
    return str(r[C['typ']] or '').startswith(('⑤', '②', '④'))

# ---------------------------------------------------------------- 词缀行的例词
PRE_FAM = [set(x.split()) for x in ('ad ac af ag al an ap ar as at a', 'in im il ir', 'en em', 'com con co col cor', 'ex e ef', 'dis dif di',
                                    'sub sup suf suc sus sug sum', 'ob op oc of', 'syn sym', 'ab abs', 'super sur', 'pro pur por')]
SUF_FAM = [set(x.split()) for x in ('ion ation tion sion ition', 'able ible', 'ize ise', 'ence ance ency ancy', 'ent ant', 'er or ar', 'al ial ical',
                                    'y ie', 'ous ious eous', 'ity ty', 'ery ry', 'ed d', 'es s', 'en n', 'est st', 'th eth')]
def family(c, col):
    for f in (PRE_FAM if col == 'pre' else SUF_FAM):
        if c in f: return f
    return {c}

def known(x, by):
    """x 是不是学生认识的词：表里的词，或表里的词加 -er / -ed / -ing / -s（smoker、eyed）"""
    if x in by or x in LD.BASIC: return True
    for suf in ('er', 'ed', 'ing', 's', 'r', 'd'):
        if x.endswith(suf) and len(x) > len(suf) + 2:
            b = x[:-len(suf)]
            if b in by or b in LD.BASIC or b + 'e' in by or (len(b) > 2 and b[-1] == b[-2] and b[:-1] in by): return True
    return False

GEN_PRE = ('un re dis mis over under out pre post non anti semi arch mini mega micro multi super sub inter co de en em fore mid self up down '
           'ultra extra auto tele tri bi uni vice counter cross off with be a in im il ir').split()
GEN_SUF = ('ly er est ed ing s es th eth ful less ness ment able ish hood like most ette let y ie an ian ese ic al ous ive ist or ion ity ery ry '
           'age en ward wards ship dom ism ize ise ify some proof free wide').split()

def _rests(lw, col, affixes):
    out = []
    for f in sorted(affixes, key=len, reverse=True):
        if col == 'pre':
            if lw.startswith(f) and len(lw) > len(f) + 1:
                rest = lw[len(f):].lstrip('-')
                out.append(rest)
                if '-' in rest: out.append(rest.split('-')[0])
        else:
            if lw.endswith(f) and len(lw) > len(f) + 1:
                b = lw[:-len(f)].rstrip('-')
                b = b.split('-')[-1] if '-' in b else b          # blue-eyed → ey、long-legged → legg
                out += [b, b + 'e']
                if len(b) > 2 and b[-1] == b[-2]: out.append(b[:-1])
                if b.endswith('i'): out.append(b[:-1] + 'y')
    return out

def rest_of(lw, col, lab):
    """去掉词缀以后剩下的（几种可能的写法）：先照这一行的词缀（和它的别的写法）去，对不上再照常见词缀去"""
    return _rests(lw, col, family(core(lab), col)) + _rests(lw, col, GEN_PRE if col == 'pre' else GEN_SUF)

def ex_status(w, col, lab, data, C, by):
    """词缀行里的一个例词 -> 'ok'（简单词 + 词缀、基础词）/ 'complex'（自己还带着词根，要再拆）"""
    lw = w.lower()
    if lw in LD.KEEP_IN: return 'ok'
    ri = by.get(lw)
    if ri is not None:
        r = data[ri]
        if is_simple_type(r, C): return 'ok'
        return 'complex' if bound_roots(r, C, by) else 'ok'
    if lw in LD.OK_OUT: return 'ok'
    if lw in LD.DROP_OUT: return 'complex'
    if any(known(x, by) for x in rest_of(lw, col, lab)): return 'ok'
    return 'complex'

def parens(s):
    out, d, st = [], 0, -1
    for i, ch in enumerate(s):
        if ch == '（':
            if d == 0: st = i
            d += 1
        elif ch == '）' and d > 0:
            d -= 1
            if d == 0: out.append((st, i))
    return out

def tok(s, seps):
    """按顶层（括号、引号外面）的分隔符切开，保留分隔符：[[文字, 分隔符], …]"""
    out, d, q, cur = [], 0, 0, ''
    for ch in s:
        if ch in '（(': d += 1
        elif ch in '）)': d = max(0, d - 1)
        elif ch == '“': q += 1
        elif ch == '”': q = max(0, q - 1)
        if d == 0 and q == 0 and ch in seps:
            out.append([cur, ch]); cur = ''
        else:
            cur += ch
    out.append([cur, ''])
    return out

def _item_word(it):
    """一个例词项 -> (单词, 是不是要判断的普通例词)。讲变法的（A → B、A / B）、短语、不是英文开头的不判断"""
    s = it.strip()
    m = WORD.match(s)
    if not m: return None, False
    head = s[:s.index('：')] if '：' in s else s
    if re.search(r'→|←|↔| / |=', head): return m.group(0), False
    if PHRASE.match(s): return m.group(0), False
    return m.group(0), True

def clean_segs(text, judge, removed, seps='；'):
    """一段文字（括号里面，或括号外面）按分号切开，去掉“同 …”里判为复杂的例词 -> 新文字"""
    segs = tok(text, seps)
    out = []           # [文字, 分隔符]
    i = 0
    while i < len(segs):
        seg, sep = segs[i]
        m = SAME.search(seg)
        if not m or (m.start() > 0 and seg[m.start() - 1] not in '，、： '):
            out.append([seg, sep]); i += 1; continue
        before, run = seg[:m.start()], seg[m.end():]
        its = [[x, '、'] for x in ITEM_SPLIT.split(run)]
        # 接在后面、用“；”隔开的例词（同 forbid 禁止：…；forgo 放弃：…）
        j = i
        while sep == '；' and j + 1 < len(segs) and HAS_EXPL.match(its[-1][0].strip()) and CONT.match(segs[j + 1][0]):
            j += 1
            its.append([segs[j][0], '；']); sep = segs[j][1]
        # 最后一项后面跟着的半句（“，见 on”）：不是例词的一部分
        tail = ''
        last = its[-1][0]
        k = LT.top_find(last, '，')
        if k >= 0 and '：' not in last[:k]:
            its[-1][0], tail = last[:k], last[k:]
        keep = []
        for x, s in its:
            w, plain = _item_word(x)
            if plain and judge(w) == 'complex': removed.append(x.strip())
            else: keep.append([x, s])
        if len(keep) == len(its):
            for t in range(i, j + 1): out.append(segs[t])
            i = j + 1; continue
        if keep:
            new = before + '同 ' + keep[0][0].lstrip() + ''.join(s + x for x, s in keep[1:]) + tail
        else:
            b = before.rstrip()
            while b and b[-1] in '，、：': b = b[:-1].rstrip()
            new = b + (tail if b else tail.lstrip('，'))
        out.append([new, sep]); i = j + 1
    # 去掉空了的段
    res = [s for s in out if s[0].strip()]
    if not res: return ''
    for t in range(len(res) - 1):
        if not res[t][1]: res[t][1] = '；'
    res[-1][1] = out[-1][1] if out and out[-1][0].strip() else ''
    return ''.join(a + b for a, b in res)

def clean_main(main, judge, removed):
    """词缀行的正文（开头的介绍，不带记法、辨析）：括号里、括号外的“同 …”都看"""
    ps = parens(main)
    for a, b in reversed(ps):
        inner = main[a + 1:b]
        if not SAME.search(inner): continue
        new = clean_segs(inner, judge, removed)
        if new == inner: continue
        main = main[:a] + ('（' + new + '）' if new.strip() else '') + main[b + 1:]
    # 括号外面的
    ps = parens(main)
    if SAME.search(''.join(ch for i, ch in enumerate(main) if not any(a <= i <= b for a, b in ps))):
        hold = []
        def mask(s):
            out, last = '', 0
            for a, b in parens(s):
                out += s[last:a] + '\x01%d\x02' % len(hold); hold.append(s[a:b + 1]); last = b + 1
            return out + s[last:]
        masked = mask(main)
        unmask = lambda t: re.sub(r'\x01(\d+)\x02', lambda m: hold[int(m.group(1))], t)
        k0 = len(removed)
        new = clean_segs(masked, judge, removed, seps='；。')
        removed[k0:] = [unmask(x) for x in removed[k0:]]
        if new != masked: main = unmask(new)
    return main

SHEN = re.compile(r'；身份：')
def split_line(line):
    """一行词缀解释 -> (标签部分“-ly：身份：”, 正文（开头的介绍）, 后面的“；记：…”“。辨析：…”)；2026-11 词缀身份辨析轮起的写法，老写法也切得开"""
    return LT.affix_split(line)

def affix_rows(data, C):
    """每一行词缀：(行下标, 列, 第几行, 标签, 这一行)"""
    for ri, r in enumerate(data):
        for col in ('pre', 'suf'):
            v = str(r[C[col]] or '')
            if v.strip() in ('', '-'): continue
            for li, line in enumerate(v.split('\n')):
                lab, rest = LT.label_body(line)
                if not lab or lab.startswith('为什么') or CO.is_note_label(lab): continue
                if col == 'suf' and not lab.startswith('-'): continue
                if col == 'pre' and not lab.endswith('-'): continue
                yield ri, col, li, lab, line

def _norm_variant(w):
    """英式 / 美式、带不带连字符这些写法归成一个样子（recognise = recognize、dialog = dialogue、program = programme）"""
    w = str(w).lower().replace('-', '')
    for a, b in (('isation', 'ization'), ('ise', 'ize'), ('yse', 'yze'), ('our', 'or'), ('ogue', 'og'), ('gramme', 'gram'), ('tre', 'ter'), ('nse', 'nce'), ('ll', 'l')):
        w = w.replace(a, b)
    return w

SEE = re.compile(r'(详)?见 ([A-Za-z][A-Za-z\-]*)(?![A-Za-z\-])(?! ?的)')
def see_drop(main, word, lab, removed, data, C, by):
    """词缀行里的“见 X”：X 只是含有同一个词缀、自己还带词根的别的词（product 的 pro-“见 produce”）去掉。
    留着：X 是简单词（见 like、见 unhappy、见 stepmother）、本词的另一种拼法（recognise 见 recognize）、“见 X 的【背景】”“详见 X”、名单 SEE_KEEP 里的"""
    for m in list(SEE.finditer(main))[::-1]:
        if m.group(1): continue
        x = m.group(2); lx = x.lower()
        ri = by.get(lx)
        if ri is None or (str(word).lower(), lx) in LD.SEE_KEEP: continue
        r = data[ri]
        if is_simple_type(r, C) or not bound_roots(r, C, by): continue
        if _norm_variant(x) == _norm_variant(word): continue
        a, b = m.start(), m.end()
        before, after = main[:a], main[b:]
        if before.endswith('（') and after.startswith('）'): new = before[:-1] + after[1:]            # （见 X）
        elif before.endswith('（') and after[:1] in '；，': new = before + after[1:].lstrip()          # （见 X；…
        elif before.rstrip()[-1:] in '；，' and after[:1] in '）；': new = before.rstrip()[:-1] + after   # …；见 X）
        else: continue
        removed.append('见 ' + x); main = new
    return main

def fix_affix_line(line, col, lab, word, data, C, by):
    """-> (新行, [去掉的例词], [去掉的“见 X”], [别的改写])"""
    head, main, meta = split_line(line)
    rm, see, oth = [], [], []
    judge = lambda w: ex_status(w, col, lab, data, C, by)
    if SAME.search(main): main = clean_main(main, judge, rm)
    main = see_drop(main, word, lab, see, data, C, by)
    for (w, l), pairs in LD.FIX.items():
        if w == word and l == lab:
            for a, b in pairs:
                if a in main: main = main.replace(a, b); oth.append('%s → %s' % (a, b))
    return head + main + meta, rm, see, oth

def plan_affix(data, C):
    by = index(data, C)
    cur, log = {}, []
    for ri, col, li, lab, line in affix_rows(data, C):
        w = data[ri][C['word']]
        nl, rm, see, oth = fix_affix_line(line, col, lab, w, data, C, by)
        if nl == line: continue
        k = (ri, col)
        if k not in cur: cur[k] = str(data[ri][C[col]]).split('\n')
        cur[k][li] = nl
        for what, xs in (('例词', rm), ('见', see), ('改写', oth)):
            if xs: log.append((ri, w, col, lab, what, xs, line, nl))
    return {k: '\n'.join(v) for k, v in cur.items()}, log

# ---------------------------------------------------------------- 词根列（第 76 条）
def prefix_set(data, C):
    out = set()
    for r in data:
        for lab, _ in part_lines(r, C, 'pre'):
            c = core(lab)
            if c: out.add(c)
    return out | {x for f in PRE_FAM for x in f}

def root_ex_complex(w, keys, lab, g, data, C, by, me, word, pres):
    """词根行里的一个例词是不是“同一个词根的复杂词”"""
    lw = w.lower()
    if lw in LD.ROOT_KEEP: return False
    if (str(word).lower(), lw) in LD.ROOT_DROP: return True
    R = core(lab)
    ri = by.get(lw)
    if ri is None:
        # 表里没有：前缀 + 这个词根（invoke = in + voke）才算复杂；别的（词根 + 后缀、不认识的）照留
        for k in sorted(keys, key=len, reverse=True):
            if len(k) < 3: continue
            p = lw.find(k)
            if p > 0 and lw[:p] in pres: return True
        return False
    if ri == me or lw in str(word).lower(): return False
    r = data[ri]
    if is_simple_type(r, C): return False
    ps = parts_of(r, C)
    roots = [c for col, c in ps if col in ('root', 'wp')]
    xpre = [c for col, c in ps if col == 'pre']
    # 放在词根列的前缀成分（extreme 的 ex-）：例词拿它当前缀，自己还带别的词根就算复杂
    if lab.endswith('-') and not lab.startswith('-') and any(c in keys for c in xpre):
        return bool(bound_roots(r, C, by))
    sk = split_keys(r, C)
    xkeys = set()
    for c in roots: xkeys |= sk.get(c, {c})
    same = (str(r[C['grp']]) == str(g) and roots) or (len(R) >= 3 and any(c[:3] == R[:3] for c in roots)) or bool(keys & xkeys)
    if not same: return False
    return bool(xpre) or len(roots) >= 2

def fix_line(line, word, g, data, C, by, me, pres=None, row=None):
    """词根列的一行 -> (新行, [去掉的例词])"""
    lab, body = LT.label_body(line)
    if not lab or CO.is_note_label(lab) or not re.match(r'^-?\(?[A-Za-z]', lab) or CO.is_connector(lab, str(word)): return line, []
    R = core(lab)
    keys = {R}
    m = VAR.search(body)
    if m: keys.add(m.group(1).lower())
    if row is not None: keys |= split_keys(row, C).get(R, set())
    keys = {k for k in keys if k}
    main, memo = LT.cut_memo(line)
    removed = []
    def repl(mm):
        seg = mm.group(0)
        items = seg[seg.index('同') + 1:].strip()
        if re.search(r'也是|，|：和', items): return seg          # 不是一串例词，是一句话：不动
        parts = [x for x in ITEM_SPLIT.split(items)]
        keep = []
        for x in parts:
            xs = x.strip()
            if re.search(r'→|←|见|\s的\s|\s和\s|里的|的 -?[A-Za-z]|=', xs) or not WORD.match(xs) or PHRASE.match(xs):
                keep.append(x); continue
            w = WORD.match(xs).group(0)
            if root_ex_complex(w, keys, lab, g, data, C, by, me, word, pres or set()): removed.append(xs)
            else: keep.append(x)
        if len(keep) == len(parts): return seg
        if not keep: return '\x00'
        return seg[:seg.index('同') + 1] + ' ' + '、'.join(k.strip() for k in keep)
    shen = re.search(r'(?:动词变化：|身份：)', main)
    head, tail = (main[:shen.start()], main[shen.start():]) if shen else (main, '')
    new_head = re.sub(r'同\s+[A-Za-z][^；。（）]*', repl, head)
    if not removed: return line, []
    new_head = re.sub(r'[，；、]\s*\x00', '', new_head)
    new_head = re.sub(r'（\x00）', '', new_head)
    new_head = re.sub(r'（\x00[；，]\s*', '（', new_head)
    new_head = new_head.replace('\x00', '')
    new_head = re.sub(r'（\s*）', '', new_head)
    return new_head + tail + memo, removed

def plan(data, C):
    by = index(data, C)
    pres = prefix_set(data, C)
    out, log = {}, []
    for ri, r in enumerate(data):
        v = str(r[C['root']] or '')
        if v.strip() in ('', '-'): continue
        ls = v.split('\n'); ch = False
        for i, l in enumerate(ls):
            nl, rm = fix_line(l, r[C['word']], r[C['grp']], data, C, by, ri, pres, r)
            if rm:
                log.append((r[C['word']], LT.label_body(l)[0], rm, l))
                ls[i] = nl; ch = True
        if ch: out[ri] = '\n'.join(ls)
    return out, log

def problems(data, C):
    """写好的表：词缀行里还没去掉的复杂例词（affix_ex）、名单里的“见 X”（affix_see）、词根列的复杂例词（root_ex）——都应为 0"""
    out = collections.defaultdict(list)
    cells, log = plan_affix(data, C)
    for ri, w, col, lab, what, xs, line, nl in log:
        out['affix_ex' if what == '例词' else 'affix_see' if what == '见' else 'affix_fix'].append((w, lab, xs))
    cells, log = plan(data, C)
    for w, lab, rm, l in log: out['root_ex'].append((w, lab, rm))
    return out

if __name__ == '__main__':
    hdr, C, data = LT.load_table(sys.argv[1])
    if '--check' in sys.argv:
        pr = problems(data, C)
        for k in ('affix_ex', 'affix_see', 'affix_fix', 'root_ex'):
            print('%s %d %s' % (k, len(pr[k]), pr[k][:5]))
        sys.exit(0)
    cells, log = plan_affix(data, C)
    n = collections.Counter()
    for ri, w, col, lab, what, xs, line, nl in log: n[(col, what)] += len(xs)
    print('词缀行：要改的格 %d（前缀 %d、后缀 %d）；去掉例词 前缀 %d、后缀 %d；去掉“见” %d；改写 %d' % (
        len(cells), sum(1 for k in cells if k[1] == 'pre'), sum(1 for k in cells if k[1] == 'suf'),
        n[('pre', '例词')], n[('suf', '例词')], n[('pre', '见')] + n[('suf', '见')], n[('pre', '改写')] + n[('suf', '改写')]))
    if '--show' in sys.argv:
        for ri, w, col, lab, what, xs, line, nl in log: print('%s | %s | %s：%s' % (w, lab, what, '、'.join(xs)))
    out, log = plan(data, C)
    print('词根列：要改的格 %d，去掉例词 %d 个' % (len(out), sum(len(x[2]) for x in log)))
    if '--show' in sys.argv:
        for w, lab, rm, l in log: print('%s | %s | 去掉：%s' % (w, lab, '、'.join(rm)))

# -*- coding: utf-8 -*-
"""词根的“形态”（2026-11 词根形态轮，project_rules.md 第 107–112 条）。
2026-11 词根形态补齐轮（第 113–118 条）：xingtai_verb.py 的新族合进 FAM、VERB；老写法的行（没有“分工”也没有“形态”）由 plain_fam 认族、line_for_plain 拆成四段；
数据改了，plan 用 refresh 重排已写好的行的来源、形态两段；--check 的 xt_diff 真的查。
用户看了第四十三版视频词根那两页：“目前词根的视频页面有点乱”“先写词根和含义：duc-；形态：原形 duc，来自拉丁语原形 ducere，然后去掉尾部 ere，这里要有去掉尾部的演示，举出例词；
过去式 dux，来自拉丁语过去式 duxi，写出怎么变化的，并做演示，举出例词；过去分词 duct，同上”“一个词根可能有其他形态，这个时候就把不同形态写出来，并写出演变”；
看了方案：“目前就是这一格乱导致的，就按你刚才的那种写法改”。
词根那一行（原来“另一种写法 → 字母变化 → 动词变化 → 规律 → 身份 → 分工 → 意思 → 记”八段）改成四段：
    标签：词根 duc-“领着走”（来自拉丁语动词 ducere“领”）。形态：原形 duc：来自拉丁语原形 ducere“领”，去掉词尾 -ere；英语里……（produce、reduce）。过去式 dux：来自拉丁语过去式 duxi“领了”，duc 加 s，c 和 s 合写成 x，再去掉词尾 -i；英语里几乎不用。过去分词 duct：……。这个词：用原形，写成 duce：duc → duce，……；记：……
  · 词根：“词根 X-“意思”（来源）。”——来源：拉丁语动词写“来自拉丁语动词 原形“中文””，别的照 xingtai_data.NV 的 src。
  · 形态：整个词根族一样（同族每一行同一段），一个形态一句，句号隔开；每句“名字 写法：来源和变化；英语里的用法（例词）；…”——第一个“；”前是来源和变化（写了“去掉词尾 -xx”的，视频演示把词尾去掉），后面每个分句是英语里的一种用法，括号里是例词。
    拉丁语动词：原形 / 过去式 / 过去分词（dongbian_data.VERB）；过去式英语里几乎不留词，写“英语里几乎不用”；没有单独过去式的写“过去式：这个动词只有被动的样子，没有单独的过去式”。
    英语里的用法是原来“分工”那句话切开、按讲到的写法归到各个形态下（shenfen_data.FAM 的身份代号：P、PW、PF、T 归过去分词，别的归原形；NV 照 sp）。
  · 这个词：这一行用的是哪个形态；写法和那个形态不一样的，接“，写成 X：”和原来“字母变化”那一段（没有的用身份代号的说明）；原来行里别的话（“这里是…”“准确说是…”）接在后面。
  · 记：照旧。
用法：
  line_for(key, 旧行, 单词)   新的一行
  get(line)                  -> dict(root, gloss, src, forms=[dict(k, en, la, zh, tail, rule, uses, note)], me, rest) 或 None
  plan(data, C)              全表试算 {行下标: 新的词根格}, 统计
  problems(data, C)          体检：xt_missing（族里的行还是老写法）、xt_diff（和数据算出来的不一样）、xt_bad（读不出来）、xt_stray（不在族里的行写了“形态：”）
  python3 xingtai.py <表>                    试算（写好以后应是“要改的格 0”）
  python3 xingtai.py <表> --show duc         看一族排出来的样子
  python3 xingtai.py <原表> --write <新表>   写回（只动词根列）"""
import re, sys, collections
import linetools as LT
import shenfen_data as FD
import dongbian_data as DD
import xingtai_data as XD
import xingtai_verb as XV          # 2026-11 词根形态补齐轮：只出现一种写法的拉丁语动词词根（第 113–118 条）

FAM = dict(FD.FAM); FAM.update(XV.FAM2)
for _k, _sp in XV.JOIN.items():                 # 已有词根族补进来的写法
    FAM[_k] = (dict(FAM[_k][0], **_sp), FAM[_k][1])
VERB = dict(DD.VERB); VERB.update(XV.VERB2)
NEW = set(XV.FAM2)
BY_G = collections.defaultdict(list)
for _k in FAM: BY_G[_k[0]].append(_k)
NOPP = '这个动词没有过去分词'
PPSTEM = re.compile(r'的过去分词词干[：:]|在这个词里的样子[：:].*过去分词|→\s*过去分词\s+\S+\s*→\s*词干|在过去分词里的样子')

PP_CODES = {'P', 'PW', 'PF', 'T', 'PE'}
NOTE = {'V': '动词原形的样子', 'W': '前面有前缀时元音弱化', 'PW': '前面有前缀时元音弱化', 'F': '经法语传进英语，变了形', 'PF': '经法语传进英语，变了形',
        'WF': '前面有前缀时弱化，又经法语变了形', 'L': '带上连接元音', 'N': '由它造出的名词的词干', 'A': '由它造出的形容词的词干', 'D': '由它造出的另一个动词的词干',
        'T': '过去分词词干，多出 at、it', 'S': '英语拼写上的另一种写法', 'G': '现在分词里的样子', 'P': '过去分词的样子', 'B': '原样',
        'E': '英语加不发音的 e', 'PE': '过去分词加不发音的 e'}
OLD_HEAD = re.compile(r'^(词根\s*([A-Za-z]+)\s*的另一种写法(（[^（）]*(?:（[^（）]*）[^（）]*)*）)?|(?:即)?本组词根“([^”]*)”(（[^（）]*(?:（[^（）]*）[^（）]*)*）)?)')
core = lambda s: re.sub(r'[（(][^（）()]*[）)]', '', s or '').strip().strip('-')
bare = lambda s: re.sub(r'[()]', '', s or '')


def fam_of(line, g):
    lab, body = LT.label_body(line)
    if not lab: return None
    if '分工：' not in line and '形态：' not in line: return plain_fam(line, g)
    m = re.match(r'词根\s*([A-Za-z]+)\s*的另一种写法', body) or re.match(r'词根\s*([A-Za-z]+)-“', body)
    if m and (g, m.group(1)) in FAM: return (g, m.group(1))
    c = core(lab).lower()
    return next(((gg, X) for (gg, X) in FAM if gg == g and X.lower() == c), None)


def plain_fam(line, g):
    """2026-11 词根形态补齐轮：还没排形态、也没写“分工”的词根行（-port：搬运（拉丁语 portare）；记：…）属于哪一族。
    只认拉丁语动词的族；标签要是这一族的写法（老族还认词根本身）；“X 的过去分词词干：…→ 词干 …”那种行不算（第 54、55 条另有写法）"""
    if PPSTEM.search(line): return None
    lab, body = LT.label_body(line)
    if any(g == gg and lab == ll and body.startswith(tt) for gg, ll, tt in XV.NOT): return None
    if not lab or not re.fullmatch(r'-?[A-Za-z()]+-?', lab.replace(' ', '')): return None
    c = bare(core(lab)).lower()
    for k in BY_G.get(g, ()):
        if k not in VERB: continue
        if c in {bare(x).lower() for x in FAM[k][0]} or (k not in NEW and c == k[1].lower()): return k
    return None


def _clauses(fg):
    return [c.strip() for c in LT.top_split(fg, '；') if c.strip()]


def _mentions(cl, sp):
    t = re.sub(r'（[^（）]*）', '', cl)
    for s in {sp, bare(sp), re.sub(r'\([^()]*\)', '', sp)}:
        if s and re.search(r'(^|[^A-Za-z])' + re.escape(s) + r'(?![A-Za-z])', t): return True
    return False


def _gloss(key, lines):
    m = re.search(r'(?:^|；)\s*' + re.escape(key[1]) + r' 是“([^”]+)”的原样', FAM[key][1])
    if m: return m.group(1)
    for l in lines:
        m = re.search(r'意思[：:]\s*[A-Za-z()]+“([^”]+)”', l) or re.search(r'本组词根“([^”]+)”', l)
        if m: return m.group(1).split('→')[-1].strip()
    m = re.search(r'是“([^”]+)”的(?:原样|过去分词)', FAM[key][1])
    if m: return m.group(1)
    return VERB[key]['inf'][1] if key in VERB else ''


def rows_of(key):
    """-> (来源, [形态 dict(k, en, s, sp, use)])"""
    ids, fg = FAM[key]
    root = key[1]
    if key in VERB:
        v = VERB[key]
        cut = v.get('cut') or ''
        m = re.search(r'（[A-Za-z]+\s*→\s*([A-Za-z]+)[^（）]*）\s*$', cut)
        inf_en = m.group(1) if m else root
        how = re.sub(r'（[^（）]*→[^（）]*）\s*$', '', cut).strip()
        how = re.sub(r'^原形', '', how).strip()
        how = re.sub(r'\s*就是\s*[A-Za-z]+$', '', how).strip()
        rc = _clauses(v['rule'])
        both = [c for c in rc if c.startswith('过去式、过去分词')]
        perf_r = '，'.join(re.sub(r'^.*?整齐：', '', c) for c in rc if '过去式' in c and c not in both) or '，'.join(both)
        pp_r = '，'.join(c for c in rc if '过去分词' in c and '过去式' not in c) or '，'.join(both) or '，'.join(c for c in rc if '过去分词' in c)
        if not both:
            perf_r = re.sub(r'^过去式(?:是\s*)?', '', perf_r).strip()
            pp_r = re.sub(r'^过去分词(?:是\s*)?', '', pp_r).strip()
        pp_more = [c for c in rc if '过去式' not in c and '过去分词' not in c]
        inf, zh = v['inf']
        k0 = inf.find(inf_en)
        pre = inf[:k0] if k0 > 0 and '前缀' in cut else ''
        dp = lambda st: st[len(pre):] if pre and st.startswith(pre) else st
        dtx = lambda t: ('再去掉前缀 %s 和词尾 -%s' % (pre, t)) if pre else ('再去掉词尾 -' + t)
        rows = [dict(k='原形', en=inf_en, s='来自拉丁语原形 %s“%s”，%s' % (inf, zh, how), sp=[])]
        if v.get('perf'):
            pf, pzh = v['perf']
            st = dp(pf[:-1])
            rows.append(dict(k='过去式', en=st, s='来自拉丁语过去式 %s“%s”，%s，%s' % (pf, pzh, perf_r, dtx('i')), sp=[],
                             use='写法和原形一样，英语里的词都算原形的' if st == inf_en else '英语里几乎不用'))
        else:
            rows.append(dict(k='过去式', en='', s='这个动词只有被动的样子，没有单独的过去式', sp=[], use=''))
        if v.get('pp'):
            pp, ppzh = v['pp']
            tail = 'us' if pp.endswith('us') else 'um'
            rows.append(dict(k='过去分词', en=dp(pp[:-len(tail)]), s='来自拉丁语过去分词 %s“%s”，%s，%s' % (pp, ppzh, pp_r, dtx(tail)), sp=[], more=pp_more))
        else:                                    # 没有过去分词的动词（timere、tremere……）：虚线、一句话
            rows.append(dict(k='过去分词', en='', s=NOPP, sp=[], use='', more=pp_more))
        for sp, code in ids.items():
            c = _cd(code)[0]
            (rows[2] if c in PP_CODES and rows[2]['en'] else rows[0])['sp'].append(sp)
        for r in (rows[0], rows[2]):
            if r['en'] and r['en'] not in r['sp']: r['sp'].append(r['en'])
        if root not in rows[0]['sp'] + rows[2]['sp']: rows[0]['sp'].append(root)
        src = '来自拉丁语动词 %s“%s”' % (inf, zh)
    else:
        nv = XD.NV[key]
        rows = [dict(r, sp=list(r['sp'])) for r in nv['rows']]
        if root not in sum((r['sp'] for r in rows), []): rows[0]['sp'].append(root)
        src = nv['src']
    # 分工那句话切开，归到讲到的写法所在的那一行（讲到几行的每行都放；一个也没讲到的放第一个有写法的行）
    for r in rows: r['uses'] = list(r.get('more') or [])
    who = lambda t: [r for r in rows if r.get('en') and any(_mentions(t, s) for s in r['sp'])]
    for cl in _clauses(fg):
        hit = who(cl)
        if len(hit) > 1:                     # 一句讲到两个形态（“原形 fac 变成 fic（…），过去分词 fact 变成 fect（…）”）：按“，”切开，各归各的
            lead, body = '', cl
            k = LT.top_find(cl, '：')
            if k > 0 and not re.search(r'[A-Za-z]', cl[:k]): lead, body = cl[:k + 1], cl[k + 1:]
            chunks = []
            for ch in LT.top_split(body, '，'):
                if chunks and len(who(ch)) == 0: chunks[-1] += '，' + ch
                else: chunks.append(ch)
            if len(chunks) > 1 and all(len(who(ch)) == 1 for ch in chunks):
                for ch in chunks: who(ch)[0]['uses'].append((lead + ch.strip()).strip())
                continue
        if not hit: hit = [rows[0]]
        for r in hit: r['uses'].append(cl)
    return src, rows


def xt_seg(key):
    src, rows = rows_of(key)
    out = []
    for r in rows:
        head = r['k'] + (' ' + r['en'] if r['en'] else '')
        uses = r['uses'] or ([r['use']] if r.get('use') else [])
        out.append(head + '：' + r['s'] + ''.join('；' + u for u in uses))
    return src, '形态：' + '。'.join(out) + '。'


def _cd(code, word=None):
    """写法代号 → (代号, 这个写法自己的说明)；代号可以是 {'*': 默认, 单词: …} 或 (代号, 一句话)"""
    if isinstance(code, dict): code = code.get(word, code['*']) if word else code['*']
    if isinstance(code, tuple): return code[0], code[1]
    return code, ''


def _code(key, sp, word):
    ids = FAM[key][0]
    c = ids.get(sp)
    if c is None:
        c = next((v for k, v in ids.items() if bare(k).lower() == bare(sp).lower()), None)
    if c is None: return None
    c, how = _cd(c, word)
    return how or c


def me_seg(key, sp, word, old):
    src, rows = rows_of(key)
    r = next((r for r in rows if r['en'] and sp.lower() in [x.lower() for x in r['sp']]), None) or next((r for r in rows if r['en'] and bare(sp).lower() in [bare(x).lower() for x in r['sp']]), rows[0])
    t = '用' + r['k']
    if bare(sp).lower() != r['en'].lower():
        mz = re.search(r'字母变化：([^。]*)', old)
        c = _code(key, sp, word)
        how = mz.group(1).strip() if mz else (NOTE.get(c, c) if c else '')
        t += '，写成 ' + sp + ('：' + how if how else '')
    else:
        t += ' ' + r['en']
    # 原来行里别的话：“（同一个词根；准确说是…）”、意思那一段后面的“；这里是…”
    extra = []
    ob = LT.label_body(old)[1]
    hd = ob[:LT.top_find(ob, '。')] if LT.top_find(ob, '。') >= 0 else ob
    m = OLD_HEAD.match(hd)
    if m and m.group(3):
        x = m.group(3)[1:-1].replace('同一个词根', '').strip('；， ')
        if x: extra.append(x)
    rem = hd[m.end():] if m else re.sub(r'^(?:即)?本组词根[，：]?', '', hd)
    rem = rem.strip('；，。 ')
    if rem and not rem.startswith(('字母变化', '动词变化', '身份', '意思')): extra.append(rem)
    body = re.sub(r'；记：.*$', '', old)
    mi = re.search(r'意思[：:]\s*[A-Za-z()]+“[^”]*”(（[^（）]*(?:（[^（）]*）[^（）]*)*）)?([^。]*)', body)
    if mi and mi.group(2).strip('；，。 '): extra.append(mi.group(2).strip('；，。 '))
    for mz in re.finditer(r'[；。]\s*(这里是“[^”]*”[^。；]*)', body):
        if mz.group(1) not in ' '.join(extra): extra.append(mz.group(1))
    return t + ''.join('；' + e for e in extra)


def line_for(key, old, word, gloss=None):
    lab = LT.label_body(old)[0]
    memo = LT.cut_memo(old)[1]
    src, seg = xt_seg(key)
    if gloss is None: gloss = ''
    sp = core(lab)
    return '%s：词根 %s-“%s”（%s）。%s这个词：%s%s' % (lab, key[1], gloss, src, seg, me_seg(key, sp, word, old), memo)


def head_gloss(key, lines):
    """词根后面引号里的意思：新立的族照 xingtai_verb.GLOSS；老族照这一族已经写好的行"""
    if key in XV.GLOSS: return XV.GLOSS[key]
    for l in lines:
        m = XT_RX.match(l)
        if m and m.group(2) == key[1]: return m.group(3)
    return _gloss(key, lines)


def _forms(key):
    """这一族的拉丁语词（原形、过去式、过去分词，cut 里提到的）：老行括号里只说“拉丁语 portare”的，形态里已经有了，不再留"""
    v = VERB.get(key, {})
    out = {norm(x[0]) for x in (v.get('inf'), v.get('perf'), v.get('pp')) if x}
    out |= {norm(x) for x in re.findall(r'[A-Za-zāēīōū]{3,}', v.get('cut', ''))}
    return out


def norm(s):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', str(s).lower()) if unicodedata.category(c) != 'Mn').replace('j', 'i')


def _pure(chunk, forms):
    c = chunk.strip().rstrip('。；，')
    c = re.sub(r'\s*里的词干\s*-?[A-Za-zāēīōū]*-?$', '', c)
    c = re.sub(r'的“[^”]*”(?:形式)?(?:的词干)?\s*-?[A-Za-zāēīōū]*-?$', '', c)
    c = re.sub(r'的过去分词(?:词干)?\s*-?[A-Za-zāēīōū]*-?$', '', c).strip()
    m = re.fullmatch(r'(?:来自|=)?\s*(?:古典|晚期|中世纪|俗|古)?拉丁语\s*(?:动词\s*)?-?([A-Za-zāēīōū]+)-?(?:\s*“[^”]*”)?', c)
    if not m: m = re.fullmatch(r'-?([A-Za-zāēīōū]+)-?(?:\s*“[^”]*”)?', c)
    return bool(m) and norm(m.group(1)) in forms


def _close(s, i):
    d = 0
    for j in range(i, len(s)):
        if s[j] in '（(': d += 1
        elif s[j] in '）)':
            d -= 1
            if d == 0: return j
    return len(s) - 1


def _gloss_end(s):
    """开头那段意思到哪儿为止：括号、引号外面第一个“（；。：”；意思里夹的短括号（“汲（水）、舀干”“（费大力气地）建造”）不算"""
    q, i = 0, 0
    while i < len(s):
        c = s[i]
        if c == '“': q += 1
        elif c == '”': q = max(0, q - 1)
        elif q == 0 and c == '（':
            j = _close(s, i)
            if j - i - 1 <= 6 and not re.search(r'[A-Za-z]', s[i + 1:j]): i = j + 1; continue
            return i
        elif q == 0 and c in '；。：': return i
        i += 1
    return len(s)


def parse_plain(body, key):
    """老写法的词根行（标签后面那一段，不带“；记：”）→ (这一行自己写的意思, [别的话…])。
    “搬运（拉丁语 portare）”“= rod“啃”（拉丁语 rodere“啃、咬掉”；同 rodent…）”“拉丁语 sequi“跟随”（见…）”“词根 lat“被带的”（…）。…”“““（被）给出的”（…）”都认；
    开头那段太长（超过 14 个字）的不当意思，整句留着；括号里只说“拉丁语 X”“X 的“被…了的”形式 Y”的半句去掉（形态里有了），别的话一字不丢"""
    forms = _forms(key)
    s, gl = body.strip(), ''
    LAT = r'(?:(?:古典|晚期|中世纪|俗|古)?拉丁语\s*)?(?:动词\s*)?'
    ok = lambda rest: rest == '' or rest[0] in '（；。，：'
    m = re.match(r'^词根\s*[A-Za-z]+\s*“([^”]*)”', s)
    if m: gl, s = m.group(1), s[m.end():]
    else:
        m = re.match(r'^=\s*' + LAT + r'-?[A-Za-zāēīōū()]+-?\s*“([^”]*)”', s) or re.match(r'^“([^”]*)”', s)
        if m and ok(s[m.end():]): gl, s = m.group(1), s[m.end():]
        else:
            m = re.match(r'^=\s*' + LAT + r'-?[A-Za-zāēīōū()]+-?\s*(?=[，（；。]|$)', s)
            if m: s = s[m.end():].lstrip('，').strip()
            m = re.match(r'^(?:来自)?(?:古典|晚期|中世纪|俗|古)?拉丁语\s*(?:动词\s*)?-?([A-Za-zāēīōū]+)\s*“([^”]*)”', s)
            if m and norm(m.group(1)) in forms and ok(s[m.end():]): gl, s = m.group(2), s[m.end():]
            elif not re.match(r'^(=|拉丁语|来自|“)', s) and not (s.startswith('（') and _gloss_end(s) == 0):
                k = _gloss_end(s)
                g0 = s[:k].strip().rstrip('，')
                if k <= 14 and not re.search(r'[A-Za-z]', g0) and not g0.startswith('这里') and '不是' not in g0: gl, s = g0, s[k:]
    extras = []
    s = s.strip().lstrip('：').strip()
    if s.startswith('（'):
        j = _close(s, 0)
        inner, s = s[1:j], s[j + 1:]
        for item in LT.top_split(inner, '；'):
            ch = [c.strip() for c in LT.top_split(item, '，') if c.strip() and not _pure(c, forms)]
            if ch: extras.append('，'.join(ch))
    for piece in LT.top_split(s.strip().lstrip('；。，：'), '。；'):
        p = re.sub(r'（([^（）]*)）', lambda m: '' if _pure(m.group(1), forms) else m.group(0), piece).strip().rstrip('。；，')
        if not p or _pure(p, forms) or re.fullmatch(r'意思[：:]\s*\S{1,12}', p): continue
        extras.append(p)
    return gl, extras


def _same(a, b):
    """两句话讲的是不是同一件事：有两个以上一样的三字片段（只看汉字）"""
    g = lambda t: {t[i:i + 3] for i in range(len(t) - 2) if all('\u4e00' <= ch <= '\u9fff' for ch in t[i:i + 3])}
    return len(g(a) & g(b)) >= 2


def me_plain(key, sp, word, gl, gloss, extras, code=None):
    src, rows = rows_of(key)
    low = bare(sp).lower()
    if code:                                     # xingtai_verb.AS：这个词实际用的写法不是标签上那个
        c, how = _cd(code)
        r = rows[2] if c in PP_CODES and rows[2]['en'] else rows[0]
    else:
        r = next((r for r in rows if r['en'] and low in [bare(x).lower() for x in r['sp']]), None) or rows[0]
        how = _code(key, sp, word)
    how = NOTE.get(how, how) if how else ''
    t = '用' + r['k']
    if how and (how == '原样' or any(_same(how, e) for e in extras)): how = ''   # 老行自己讲了怎么变的，不再重复
    if low != r['en'].lower():
        t += '，写成 ' + sp + ('：' + how if how else '')
    else:
        t += ' ' + r['en']
    ex = (['这里是“%s”' % gl] if gl and gl != gloss else []) + extras
    return t + ''.join('；' + e for e in ex)


def line_for_plain(key, old, word, gloss):
    """老写法的词根行 → 词根 → 形态 → 这个词 → 记 四段（第 113–118 条）"""
    lab = LT.label_body(old)[0]
    main, memo = LT.cut_memo(old)
    me = getattr(XV, 'ME', {}).get((word, lab))
    if me is None:
        gl, extras = parse_plain(LT.label_body(main)[1], key)
        sp, code = XV.AS.get((word, lab), (core(lab), None))
        me = me_plain(key, sp, word, gl, gloss, extras, code)
    src, seg = xt_seg(key)
    return '%s：词根 %s-“%s”（%s）。%s这个词：%s%s' % (lab, key[1], gloss, src, seg, me, memo)


def refresh(key, line):
    """已经排好形态的行：数据改了，就照数据重排“来源”和“形态”两段（词根的意思、这个词、记不动）"""
    m = XT_RX.match(line)
    if not m: return line
    src, seg = xt_seg(key)
    if m.group(4) == src and '形态：' + m.group(5) == seg: return line
    return '%s：词根 %s-“%s”（%s）。%s这个词：%s' % (m.group(1), m.group(2), m.group(3), src, seg, m.group(6))


def plan(data, C):
    fam_lines = collections.defaultdict(list)
    for r in data:
        for l in str(r[C['root']] or '').split('\n'):
            k = fam_of(l, r[C['grp']])
            if k: fam_lines[k].append(l)
    out, stat = {}, collections.Counter()
    for ri, r in enumerate(data):
        v = str(r[C['root']] or '')
        if v.strip() in ('', '-'): continue
        new = []
        for l in v.split('\n'):
            k = fam_of(l, r[C['grp']])
            nl = l
            if k and '分工：' in l:
                nl = line_for(k, l, str(r[C['word']]), _gloss(k, fam_lines[k])); stat['老写法'] += 1
            elif k and '形态：' in l:
                nl = refresh(k, l)
                if nl != l: stat['重排'] += 1
            elif k:
                nl = line_for_plain(k, l, str(r[C['word']]), head_gloss(k, fam_lines[k])); stat['补齐'] += 1; stat['族 %s %s' % k] += 1
            new.append(nl)
        nv = '\n'.join(new)
        if nv != v: out[ri] = nv
    return out, stat


XT_RX = re.compile(r'^([^：]{1,40})：词根\s+([A-Za-z]+)-“([^”]*)”（(.*?)）。形态：(.*?)这个词：(.*)$')
FORM_RX = re.compile(r'^(\S+?)(?:\s+([A-Za-z()]+))?：(.*)$')


def get(line):
    m = XT_RX.match(str(line or ''))
    if not m: return None
    me, memo = LT.cut_memo(m.group(6))
    forms = []
    for sen in [s for s in LT.top_split(m.group(5), '。') if s.strip()]:
        f = FORM_RX.match(sen.strip())
        if not f: return dict(bad=sen)
        parts = LT.top_split(f.group(3), '；')
        s0 = parts[0]
        la = re.search(r'来自(?:拉丁语|希腊语|古法语)?[^A-Za-z“]*\s([A-Za-zāēīōūæœ()*]+)“([^”]*)”', s0)
        tl = re.findall(r'(?:去掉|和)词尾\s*-([A-Za-zāēīōū]+)', s0)
        pf = re.search(r'去掉前缀\s*([a-z]+)', s0)
        forms.append(dict(k=f.group(1), en=f.group(2) or '', src=s0, la=la.group(1) if la else '', zh=la.group(2) if la else '', tail=tl[-1] if tl else '', pre=pf.group(1) if pf else '', uses=parts[1:]))
    return dict(label=m.group(1), root=m.group(2), gloss=m.group(3), src=m.group(4), forms=forms, me=me, memo=memo)


def problems(data, C):
    """xt_missing：族里的行还是老写法（“身份：…。分工：…”，或补齐轮要补形态的行）；xt_diff：形态、来源和数据排出来的不一样；
    xt_bad：读不出来；xt_stray：不在族里的行、或者前缀 / 单词部分 / 后缀列写了“形态：”"""
    out = collections.defaultdict(list)
    for n, r in enumerate(data, start=2):
        w, g = str(r[C['word']]), r[C['grp']]
        for col in ('pre', 'wp', 'suf'):
            if '形态：' in str(r[C[col]] or ''): out['xt_stray'].append((n, w, col))
        for l in str(r[C['root']] or '').split('\n'):
            k = fam_of(l, g)
            if '形态：' in l:
                if not k: out['xt_stray'].append((n, w, l[:40])); continue
                gg = get(l)
                if not gg or 'bad' in gg or not gg['forms']: out['xt_bad'].append((n, w, l[:50])); continue
                if refresh(k, l) != l: out['xt_diff'].append((n, w, l[:40]))
            elif k: out['xt_missing'].append((n, w, l[:40]))
    return out


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    hdr, C, data = LT.load_table(a[0])
    if '--show' in sys.argv:
        R = sys.argv[sys.argv.index('--show') + 1]
        for key in FAM:
            if key[1] == R:
                src, seg = xt_seg(key); print(key, src); print(seg.replace('。', '。\n'))
        sys.exit(0)
    if '--check' in sys.argv:
        pr = problems(data, C)
        for k in ('xt_missing', 'xt_diff', 'xt_bad', 'xt_stray'): print(k, len(pr[k]), pr[k][:4])
        sys.exit(0)
    out, stat = plan(data, C)
    print('要改的格 %d；%s' % (len(out), '、'.join('%s %d 行' % (k, v) for k, v in stat.items() if not k.startswith('族 ')) or '都不用改'))
    if '--write' in sys.argv:
        import xlsx_write as XW
        XW.write(a[0], a[1], {(ri + 2, C['root']): t for ri, t in out.items()})
        print('写好了', a[1])

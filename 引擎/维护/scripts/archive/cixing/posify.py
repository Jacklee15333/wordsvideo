"""含义列：每个意思定词性（自动 + 人工改）"""
import re, pickle, collections
from seg import split_top, lead_tags, segments
import ecd

ROWS = pickle.load(open('/home/claude/rows.pkl', 'rb'))
WORDS = {str(r[4]).strip().lower() for r in ROWS[1:]}
ORDER = ['n.', 'v.', 'adj.', 'adv.', 'pron.', 'prep.', 'conj.', 'num.', 'art.', 'int.', 'modal v.', 'aux. v.', 'phr.']

TOK = {
    'n.': 'n.', 'n': 'n.', '名': 'n.', '名词': 'n.', '美式 n.': 'n.',
    'v.': 'v.', 'vt.': 'v.', 'vi.': 'v.', '动': 'v.', '动词': 'v.',
    'adj.': 'adj.', '形': 'adj.', '形容词': 'adj.', 'a.': 'adj.',
    'adv.': 'adv.', '副': 'adv.', '副词': 'adv.',
    'prep.': 'prep.', '介': 'prep.', '介词': 'prep.',
    'conj.': 'conj.', '连': 'conj.', '连词': 'conj.',
    'pron.': 'pron.', '代词': 'pron.',
    'int.': 'int.', 'interj.': 'int.', '感叹': 'int.', '感叹词': 'int.',
    'num.': 'num.', '数词': 'num.', 'art.': 'art.', '冠词': 'art.',
}
# 映射到词性、但标签本身还有用（留在词性后面）
KEEP = {'关系代词': ('pron.', '关系代词'), '助动词': ('aux. v.', None), '情态动词': ('modal v.', None),
        'pl.': ('n.', '复数'), '复数': ('n.', '复数'), '作程度副词': ('adv.', '作程度副词'), '修饰形容词': ('adv.', '修饰形容词'),
        '口语连词': ('conj.', '口语'), '限定词': ('adj.', None)}
POSNAME = {'形容词': 'adj.', '名词': 'n.', '动词': 'v.', '副词': 'adv.', '连词': 'conj.', '介词': 'prep.', '代词': 'pron.'}
PAST = re.compile(r'^(?:动词 )?(?:[A-Za-z\-]+(?:（[^（）]*）)? ?的)?(过去式、过去分词|过去式和过去分词|过去式|过去分词)$')

def parse_tag(tag):
    """一个括号标签 → (词性列表, 留下的标签文字或 None)"""
    t = tag.strip()
    if t in TOK: return [TOK[t]], None
    if t in KEEP: return [KEEP[t][0]], KEEP[t][1]
    m = re.match(r'^(\S+)\s*(/[^/]+/)$', t)                 # v. /lɪv/、动 /haʊz/
    if m and m.group(1) in TOK: return [TOK[m.group(1)]], m.group(2)
    m = re.match(r'^([a-z]+\.)\s+([A-Za-z].*)$', t)           # n. edibles
    if m and m.group(1) in TOK: return [TOK[m.group(1)]], m.group(2)
    m = re.match(r'^([a-z]+\.)\s+([\u4e00-\u9fff].*)$', t)     # n. 复数、v. 口
    if m and m.group(1) in TOK: return [TOK[m.group(1)]], m.group(2)
    if PAST.match(t): return ['v.'], t
    m = re.match(r'^作(形容词|名词|动词|副词|连词|介词)$', t)
    if m: return [POSNAME[m.group(1)]], None
    if re.match(r'^集合名词', t): return ['n.'], t
    toks = [x.strip() for x in re.split(r'[，,、]|\s/\s|/(?=[a-z\u4e00-\u9fff])', t) if x.strip()]
    if len(toks) > 1:
        ps, rest = [], []
        for x in toks:
            if x in TOK: ps.append(TOK[x]); continue
            mm = re.match(r'^作?(形容词|名词|动词|副词|连词|介词|代词)$', x)
            if mm: ps.append(POSNAME[mm.group(1)]); continue
            mm = re.match(r'^(v|n|adj|adv)\.\s*(口|美口|英口|美|英)$', x)
            if mm: ps.append(TOK[mm.group(1) + '.']); rest.append(mm.group(2)); continue
            rest.append(x)
        if ps: return ps, ('，'.join(rest) if rest else None)
    m = re.match(r'^(v|n|adj|adv)\.\s+(口|美口|英口|美|英)$', t)
    if m: return [TOK[m.group(1) + '.']], m.group(2)
    return [], t

def core_of(text):
    s = text
    for _ in range(3): s = re.sub(r'（[^（）]*）|\([^()]*\)', '', s)
    return s.strip()

JPOS = {'名词': 'n.', '动词': 'v.', '形容词': 'adj.', '副词': 'adv.', '数词': 'num.', '序数词': 'num.', '代词': 'pron.', '连词': 'conj.', '介词': 'prep.'}
def jpos(r):
    first = str(r[9] or '').split('\n')[0]
    m = re.search(r'；词性变化(.*)$', first)
    if not m: return []
    chains = re.findall(r'：([^；]*)', m.group(1))
    if not chains: return []
    tgt = chains[-1].split('→')[-1].strip()
    tgt = re.sub(r'（.*$', '', tgt).strip()
    tgt = re.sub(r'^变成', '', tgt)
    return [JPOS[x] for x in re.split(r'[、，]', tgt) if x in JPOS]

NOUN_DI = set('土地 场地 基地 园地 陆地 田地 本地 当地 目的地 殖民地 营地 大地 草地 墓地 产地 盆地 高地 湿地 内地 外地 境地 余地 天地 腹地 工地 领地 驻地 圣地 胜地 林地 山地 平地 空地 沼泽地 栖息地 发源地 所在地 耕地 洼地 低地 质地 封地 属地 绿地 荒地 雪地 沙地 阵地 心地 见地 根据地 原产地 集散地 出生地 发祥地 聚居地 各地 此地 某地 原地 外地 遍地 就地 实地 旱地 草场地 用地 荒野地 林场地 牧地 宝地 禁地 险地 洼地 坡地 农田地 耕种地 殖民地 种植地 水域地 沼地 泥地 湿草地 野地 战地 墓园地 坟地 圣地 胜地 洞穴地 球场地 运动场地 停车场地 场地 地'.split())
def strong_form(core, w):
    c = core.rstrip('，、。…. ')
    if not c: return None
    if c.endswith('的') and not c.endswith('目的'): return 'adj.'
    if re.match(r'^(使|（使）|\(使\))', c): return 'v.'
    if c.endswith('地') and len(c) >= 2 and not any(c.endswith(x) for x in NOUN_DI if len(x) >= 2): return 'adv.'
    return None

def ecd_score(w, gloss):
    sc = collections.defaultdict(int)
    gs = [x for x in re.split(r'[、，,/]', gloss) if x.strip()]
    for p, items in ecd.pos_lines(w):
        items2 = [re.sub(r'[（(][^（）()]*[）)]|\.\.\.|…', '', x).strip() for x in items]
        for g in gs:
            g = g.strip().replace('…', '')
            if not g: continue
            best = 0
            for it in items2:
                if not it: continue
                if g == it: best = max(best, 3)
                elif len(g) >= 2 and len(it) >= 2 and (g in it or it in g): best = max(best, 2)
                else:
                    a, b = set(g), set(it)
                    if len(a & b) >= 2 and len(a & b) / len(a | b) >= 0.5: best = max(best, 1)
            sc[p] = max(sc[p], best)
    return dict(sc)

def possible(w):
    ps = {p for p, _ in ecd.pos_lines(w)}
    return ps

_wn = None
def wn_prior(w):
    global _wn
    if _wn is None:
        from nltk.corpus import wordnet as wn
        _wn = wn
    c = collections.Counter()
    for l in _wn.lemmas(w.lower().replace(' ', '_')):
        p = l.synset().pos(); p = {'n': 'n.', 'v': 'v.', 'a': 'adj.', 's': 'adj.', 'r': 'adv.'}[p]
        c[p] += l.count() + 0.01
    return c

INFL = re.compile(r'^([A-Za-z][A-Za-z\-]*)(?:（[^（）]*）|\([^()]*\))?\s*的\s*(过去式|过去分词|现在分词|复数|比较级|最高级|第三人称)')
ACRO = re.compile(r'^([A-Z]{1,4}|AI)\s*[\u4e00-\u9fff]')

def eng_head(rest):
    m = re.match(r"^((?:[A-Za-z0-9…\.'’!?,/\-]+|\.\.\.)(?:\s+(?:[A-Za-z0-9…\.'’!?,/\-()\[\]]+|\.\.\.|…|/))*)", rest)
    return m.group(1).strip() if m else ''
def norm(x): return re.sub(r'[^a-z]', '', x.lower())

def forms_of(w):
    wl = w.lower()
    fs = {wl, wl + 's', wl + 'es', wl + 'ed', wl + 'd', wl + 'ing'}
    if wl.endswith('e'): fs.add(wl[:-1] + 'ing')
    if wl.endswith('y'): fs |= {wl[:-1] + 'ies', wl[:-1] + 'ied'}
    if len(wl) >= 3 and wl[-1] not in 'aeiouwxy' and wl[-2] in 'aeiou' and wl[-3] not in 'aeiou':
        fs |= {wl + wl[-1] + 'ed', wl + wl[-1] + 'ing'}
    for e in ecd.entries(w):
        for part in e['exchange'].split('/'):
            if ':' in part:
                k, v = part.split(':', 1)
                if k in 'sdpi3' and v: fs.add(v.lower())
    return fs
def verb_forms(w):
    wl = w.lower(); fs = set()
    for e in ecd.entries(w):
        for part in e['exchange'].split('/'):
            if ':' in part:
                k, v = part.split(':', 1)
                if k in 'dpi' and v and v.lower() != wl: fs.add(v.lower())
    if not fs:
        fs = {wl + 'ed', wl + 'd', wl + 'ing', wl[:-1] + 'ing'}
    return fs

def related_kind(w, eng):
    toks = [t for t in re.split(r'\s+', eng) if t]
    wl = norm(w); nt = [norm(t) for t in toks]
    stems = forms_of(w) | {wl}
    stems = {norm(s) for s in stems}
    has = any(t in stems or (len(wl) > 2 and t.startswith(wl[:max(3, len(wl) - 2)]) and abs(len(t) - len(wl)) <= 3) for t in nt)
    if len(toks) == 1:
        t = nt[0]
        if t == wl: return 'same'
        if t in stems: return 'form'
        return 'related'
    if nt[0] in ('the', 'a', 'an') and len(toks) == 2 and nt[1] in stems: return 'the-n'
    return 'phr' if has else 'phr?'

DET = set("a an the this that these those my your his her its our their one's sb's no every each some any another such".split())
SUBJ = set("to will would can could may might must should shall don't doesn't didn't won't can't i you we they he she please let let's not never often always usually also just".split())
OBJ = DET | set("sb sth me him her us them it up out off down in on into for with about away over back yourself myself himself herself oneself".split())

def example_cue(w, seg):
    votes = collections.Counter()
    fs = forms_of(w); vf = verb_forms(w)
    for ch in re.findall(r'[（(]([^（）()]*)[）)]', seg):
        for sent in re.split(r'[；;，,/]|\s—\s', ch):
            toks = re.findall(r"[A-Za-z][A-Za-z'’\-]*", sent)
            low = [t.lower().replace('’', "'") for t in toks]
            for j, t in enumerate(low):
                if t not in fs: continue
                p = low[j - 1] if j > 0 else None
                q = low[j + 1] if j + 1 < len(low) else None
                if t in vf and t.endswith(('ed', 'ing')) is False and t in vf:
                    pass
                if p in DET or (p and p.endswith("'s")):
                    votes['n.'] += 1
                elif p in SUBJ:
                    votes['v.'] += 1
                elif j == 0 and q in OBJ:
                    votes['v.'] += 1
                elif t in vf and t != w.lower() and j > 0:
                    votes['v.'] += 0.5
    return votes

NOUNEND = set('者人家员师手器机物品件具剂药病症学术业室馆院所店场厅站台楼屋房门窗桌椅床车船舰鸟鱼虫兽树花草果菜肉汤茶酒水油粉布纸笔书报刊画歌曲舞剧片节日月年季期时秒度性感力权金费税价钱币卡票证照单表图线点面体状色声音味气光影子儿头部处区国省市县村镇城街路桥山河湖海岛洋星球天风雨雪云冰火土石沙泥木林竹系制式法情况态系统问题事情东西样子方式方法意见地方')

def analyze(rn, overrides=None):
    r = ROWS[rn - 1]
    w = str(r[4]).strip(); f = str(r[5] or '')
    segs = segments(f)
    defaults = jpos(r)
    P = possible(w)
    out = []
    for k, (li, s) in enumerate(segs):
        mc = re.match(r'^([\u2460-\u2469])\s*', s)
        circ = mc.group(1) if mc else ''
        tags, rest = lead_tags(s[mc.end():] if mc else s)
        pos_ex, labels = [], []
        for t in tags:
            ps, lab = parse_tag(t)
            pos_ex += [p for p in ps if p not in pos_ex]
            if lab: labels.append(lab)
        core = core_of(rest)
        kind = 'zh'; eng = ''; inf = ''
        if re.match(r'^[A-Za-z]|^(…|\.\.\.)\s*[A-Za-z]', rest) and not ACRO.match(rest):
            m = INFL.match(rest)
            if m: kind = 'infl'; inf = m.group(2)
            else: eng = eng_head(rest); kind = related_kind(w, eng)
        o = {'k': k, 'li': li, 'seg': s, 'circ': circ, 'tags': tags, 'labels': labels, 'rest': rest, 'core': core, 'kind': kind,
             'eng': eng, 'pos': None, 'why': '', 'sc': {}, 'form': None, 'ex': collections.Counter(), 'flags': [], 'conf': 'hi'}
        if pos_ex: o['pos'] = pos_ex; o['why'] = 'tag'
        elif kind == 'infl': o['pos'] = ['n.'] if inf == '复数' else (['adj.'] if inf in ('比较级', '最高级') else ['v.']); o['why'] = 'infl'
        elif kind == 'phr': o['pos'] = ['phr.']; o['why'] = 'phr'
        elif kind == 'phr?': o['pos'] = ['phr.']; o['why'] = 'phr?'; o['conf'] = 'lo'
        elif kind == 'the-n': o['pos'] = ['n.']; o['why'] = 'the-n'
        elif kind == 'related': o['pos'] = ['REL']; o['why'] = 'related'; o['conf'] = 'lo'
        else:
            o['form'] = strong_form(core, w)
            o['sc'] = ecd_score(w, core)
            o['ex'] = example_cue(w, s)
            if kind in ('same', 'form'): o['conf'] = 'lo'
        out.append(o)
    first_tag = next((i for i, o in enumerate(out) if o['why'] == 'tag'), len(out))
    lead = [o for o in out[:first_tag] if o['pos'] is None]
    votes = collections.Counter()
    for idx, o in enumerate(lead):
        wt = 2.0 if idx == 0 else 1.0
        if o['form']:
            votes[o['form']] += wt; continue
        sc = o['sc']
        if sc:
            top = max(sc.values()); bests = [p for p, v in sc.items() if v == top]
            if top >= 2 and len(bests) == 1: votes[bests[0]] += wt * (1.5 if top == 3 else 1.0)
            elif top >= 2:
                for b in bests: votes[b] += wt * 0.3
        for p, v in o['ex'].items(): votes[p] += wt * min(v, 2) * 0.8
        if o['core'] and o['core'][-1] in NOUNEND and not o['sc'].get('v.'): votes['n.'] += wt * 0.2
    D = None; dwhy = ''; margin = 0
    if defaults:
        for p in defaults:
            votes[p] += (3.0 if len(defaults) == 1 else 1.5) * (0.2 if P and p not in P else 1.0)
    if True:
        v2 = collections.Counter(votes)
        if P:
            for p in list(v2):
                if p not in P and p in ('n.', 'v.', 'adj.', 'adv.'): v2[p] *= 0.3
        ranked = sorted(v2.items(), key=lambda x: -x[1])
        if ranked and ranked[0][1] > 0:
            margin = ranked[0][1] - (ranked[1][1] if len(ranked) > 1 else 0)
            D = ranked[0][0]; dwhy = 'jvote' if defaults else 'vote'
        if not D or margin < 0.5:
            pr = wn_prior(w)
            for p, v in pr.items():
                if not P or p in P: v2[p] += 1.2 * v / (sum(pr.values()) or 1)
            ranked = sorted(v2.items(), key=lambda x: -x[1])
            if ranked and ranked[0][1] > 0:
                margin = ranked[0][1] - (ranked[1][1] if len(ranked) > 1 else 0)
                D = ranked[0][0]; dwhy = 'vote+wn'
        if not D:
            fp = ecd.first_pos(w)
            D = fp or 'n.'; dwhy = 'ecdfirst' if fp else 'guess'; margin = 0
    last_tag_pos = None
    for i, o in enumerate(out):
        if o['why'] == 'tag':
            last_tag_pos = o['pos'][0]; continue
        if o['pos'] is not None: continue
        if o['form']:
            o['pos'] = [o['form']]; o['why'] = 'form'
            if o['form'] == 'adv.': o['conf'] = 'mid'
        elif i < first_tag:
            o['pos'] = [D]; o['why'] = dwhy
            if dwhy in ('vote', 'vote+wn', 'jvote') and margin < 1.0: o['conf'] = 'lo'
            if defaults and D not in defaults: o['flags'].append('jdiff:' + '/'.join(defaults))
            if dwhy in ('ecdfirst', 'guess', 'jpos2'): o['conf'] = 'lo'
        else:
            o['pos'] = [last_tag_pos]; o['why'] = 'carry'
        sc = o['sc']; p = o['pos'][0]
        if sc:
            top = max(sc.values()); bests = [x for x, v in sc.items() if v == top]
            if top >= 3 and p not in bests and sc.get(p, 0) < 2: o['flags'].append('ecd:' + '/'.join(bests))
        if o['ex'] and o['why'] != 'form':
            ep = o['ex'].most_common(1)[0][0]
            if ep != p and o['ex'][ep] >= 1 and o['ex'].get(p, 0) == 0 and (p in ('n.', 'v.') or o['ex'][ep] >= 2):
                o['flags'].append('ex:' + ep)
        if P and p in ('n.', 'v.', 'adj.', 'adv.') and p not in P and o['why'] != 'form': o['flags'].append('notin:' + '/'.join(sorted(P)))
        cc = o['core'].rstrip('，、。…. ')
        if p == 'adj.' and o['why'] != 'form' and cc and not cc.endswith('的'): o['flags'].append('adj-no-de')
        if p == 'adv.' and o['why'] != 'form' and cc and not cc.endswith('地') and not w.lower().endswith('ly'): o['flags'].append('adv-no-di')
        if o['flags'] and o['conf'] == 'hi': o['conf'] = 'mid'
    return out, D, dwhy, margin

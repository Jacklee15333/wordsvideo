"""在 suffix_upgrade 的基础上：
1. “在这里”改成讲词性：原来是什么词、加上后缀变成什么词、两种词各说的是什么，所以有了哪几个意思；
2. 一词多义的词，在各部分解释里加“意思怎么变：…”（照组合列 → 那几行，每步标出用到的用词规律）和“用词规律：…”（规律 + 本词 + 一个熟悉的例子）。
"""
import re, sys, collections, pickle
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sense_suffix as su
import meaning as M
T, FIRST, LAB = su.T, su.FIRST, su.LAB

# ---------------- 今义里的几个意思 ----------------
def split_top(s, seps='；'):
    out, cur, d = [], '', 0
    for ch in s:
        if ch in '（(': d += 1
        elif ch in '）)': d = max(0, d - 1)
        if ch in seps and d == 0: out.append(cur); cur = ''
        else: cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]

JY = lambda i: '【今义】' + M.to_old(T[i - 2][5], T[i - 2][6])   # 今义 2026-11 起写在 F 列「含义」（一行一个意思、行首写词性），还原成老的一行写法再读

def senses(i, n=3):
    for l in [JY(i)]:
        if l.startswith('【今义】'):
            out = []
            for seg in split_top(l[4:]):
                t = seg
                while True:
                    m = re.match(r'^[（(][^（）()]*[）)]\s*', t)
                    if not m: break
                    t = t[m.end():]
                t = re.sub(r'（[^（）]*）|\([^()]*\)', '', t).strip().rstrip('，、。')
                if t and not re.search(r'[A-Za-z]', t) and len(t) <= 12 and t not in out: out.append(t)
                if len(out) >= n: break
            return out
    return []

# ---------------- 后缀把什么词变成什么词 ----------------
VN = {'-ion', '-tion', '-sion', '-ation', '-ition', '-ment', '-ure', '-age', '-sis', '-al@noun', '-ing@noun', '-ance@v', '-ence@v'}
AGENT = {'-er@agent', '-r@agent', '-or', '-ator'}
NAGENT = {'-ist', '-ian', '-an@n'}
VADJ = {'-able': '能被{g}', '-ible': '能被{g}', '-ive': '会{g}、起{g}的作用', '-ative': '会{g}、起{g}的作用', '-itive': '会{g}、起{g}的作用',
        '-ing@adj': '正在{g}，或者让人{g}', '-ed@pp': '已经被{g}了', '-d@pp': '已经被{g}了', '-en@pp': '已经被{g}了', '-n@pp': '已经被{g}了',
        '-ant': '正在{g}', '-ent': '正在{g}', '-ient': '正在{g}'}
NADJ = {'-al@adj': '和{g}有关的', '-ial': '和{g}有关的', '-ual': '和{g}有关的', '-ical': '和{g}有关的', '-ic': '和{g}有关的', '-tic': '和{g}有关的',
        '-atic': '和{g}有关的', '-ar': '和{g}有关的', '-ary': '和{g}有关的', '-ese': '属于{g}的', '-ous': '充满{g}的', '-ious': '充满{g}的',
        '-ful': '充满{g}的', '-less': '没有{g}的', '-y@adj': '有{g}的、像{g}的', '-ish@adj': '像{g}的、有点{g}的', '-ly@adj': '有{g}样子的',
        '-ed@adj': '长着{g}的、带着{g}的', '-d@adj': '长着{g}的、带着{g}的', '-like': '像{g}一样的', '-some': '带着{g}的、容易{g}的'}
ADJN = {'-ness', '-ity', '-ty@ity', '-ety', '-cy', '-ance@adj', '-ence@adj', '-ce'}
ADV = {'-ly@adv', '-ally'}
XV = {'-ize': '使变成{g}、让它带上{g}', '-ise': '使变成{g}、让它带上{g}', '-ify': '使变成{g}', '-fy': '使变成{g}', '-en@verb': '使变得{g}'}
NN = {'-ship': '当{g}的身份、和{g}之间的关系或状态', '-hood': '作为{g}的状态、那段时期或那一群人', '-dom': '{g}的状态、地位或管的地方',
      '-ism': '{g}的主张、做法或特点', '-ics': '和{g}有关的种种事，也就是一门学问', '-logy': '研究{g}的学问', '-ery': '做{g}的地方、行业，或一类{g}',
      '-ry': '一类{g}、做{g}的地方'}
DIM = {'-et', '-ette', '-let', '-ling', '-le@dim'}

def key_of(lab, line, stem):
    s = su.sense(lab, line)
    k = f'{lab}@{s}' if s else lab
    if lab in ('-ance', '-ence'): k = lab + ('@adj' if re.search(r'(ant|ent)$', stem.lower()) else '@v')
    if lab == '-an': k = '-an@n' if re.search(r'的人|人”|人；|当名词', line) else '-al@adj'
    return k

def stem_of(i, lab):
    """在构词逻辑第一行里找后缀前面那一部分和它的意思。多于两部分时返回 ('', '', n)。"""
    first = str(T[i - 2][10] or '').split('\n')[0]
    pl = su.parse_logic(first); c = su.norm(lab)
    if not pl: return None
    kind, items, lit = pl
    clean = lambda g: '' if (not g or re.search(r'[“”（）()=]', g) or len(g) > 10) else g
    if kind == 'eq':
        idx = [k for k, (t, g) in enumerate(items) if su.norm(t) == c]
        if not idx or idx[-1] == 0: return None
        k = idx[-1]; stem, g = items[k - 1]
        if k >= 2:
            q = re.match(r'^“([^“”]{1,24})”', lit or '')
            heads = ' + '.join(re.sub(r'\(([a-z]+)\)', r'\1', t.strip()) for t, _ in items[:k])
            return (heads, q.group(1) if q else '', k)
        if not re.fullmatch(r"[A-Za-z][A-Za-z'\-]*(?:\([a-z]+\))?", stem.strip()): return None
        g = clean(g) or clean(su.stem_gloss(i, stem))
        return (re.sub(r'\(([a-z]+)\)', r'\1', stem.strip()), g, 1)
    for k in range(1, len(items)):
        wp, gp = items[k - 1]; wn, gn = items[k]
        if su.norm(wn).endswith(c) and len(su.norm(wn)) > len(su.norm(wp)) and re.fullmatch(r"[A-Za-z][A-Za-z'\-]*", wp.strip()):
            return (wp.strip(), clean(gp) or clean(su.stem_gloss(i, wp)), 1)
    return None

def _split_top(s, sep):
    out, d, cur = [], 0, ''
    for ch in s:
        if ch in '（(': d += 1
        elif ch in '）)': d = max(0, d - 1)
        if ch == sep and d == 0: out.append(cur); cur = ''
        else: cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]

def _eq_parse(i):
    """构词逻辑第一行（和视频技能一样只认括号、引号外面的“=”）→ ('eq', [(部分, 意思)], 字面意思) / ('route', [(词, 意思)], 最后一步的意思) / None"""
    s = re.sub(r'^【构词逻辑】', '', str(T[i - 2][10] or '').split('\n')[0]).strip()
    term = lambda x: (lambda m: (m.group(1).strip(), m.group(2).strip()) if m else (x.strip(), ''))(re.match(r'^([^（(]*?)\s*[（(]([^（）()]*)[）)]', x.strip()))
    m = re.match(r'^派生路线[：:]\s*(.*)$', s)
    if m:
        items = [term(x) for x in _split_top(m.group(1), '→')]
        return ('route', items, items[-1][1] if items else '')
    d = q = 0
    for k, ch in enumerate(s):
        if ch in '（(': d += 1
        elif ch in '）)': d = max(0, d - 1)
        elif ch == '“': q += 1
        elif ch == '”': q = max(0, q - 1)
        elif ch == '=' and d == 0 and q == 0:
            mm = re.match(r'^\s*“((?:[^“”]|“[^“”]*”)*)”', s[k + 1:])
            return ('eq', [term(x) for x in _split_top(s[:k], '+')], mm.group(1).strip() if mm else '')
    return None

def _lit(i):
    """构词逻辑的字面意思（派生路线取最后一步的意思）；里面套的引号换成‘’"""
    pl = _eq_parse(i)
    return (pl[2] if pl else '').replace('“', '‘').replace('”', '’')

def overlap(a, b):
    za = {c for c in a if '\u4e00' <= c <= '\u9fff'}; zb = {c for c in b if '\u4e00' <= c <= '\u9fff'}
    return len(za & zb)

def bridge(i, stem, g):
    """母词的意思有好几个（“使共有、传达”），本词用的是后面那个时：先讲清楚本义怎么变成那个意思。"""
    items = [x.strip() for x in re.split('、', g) if x.strip()]
    if len(items) < 2 or stem.lower() not in FIRST: return None
    first = str(T[i - 2][10] or '').split('\n')[0]
    pl_ = su.parse_logic(first)
    lit = ''
    if pl_ and pl_[0] == 'eq': lit = pl_[2]
    elif pl_ and pl_[0] == 'route' and pl_[1]: lit = pl_[1][-1][1]
    target = lit or ' '.join(senses(i, 2))
    sc = [overlap(x, target) for x in items]
    best = max(range(len(items)), key=lambda k: sc[k])
    if best == 0 or sc[best] == 0 or sc[0] >= sc[best]: return None
    j = FIRST[stem.lower()]
    for l in str(T[j - 2][10] or '').split('\n'):
        l = l.strip()
        if not re.match(r'^[→⇒]', l): continue
        ps = [p.strip() for p in re.split(r'\s*→\s*', re.sub(r'^[→⇒]\s*', '', l))]
        if len(ps) >= 2 and items[best] in ps[-1]:
            why = re.sub(r'（[^（）]*）', '', ' → '.join(ps[:-1])).strip().rstrip('，')
            if why and len(why) <= 48:
                return items[0], why, items[best]
    return None

def _pos_sentence(i, lab, line, word):
    st = stem_of(i, lab)
    if not st: return None
    stem, g, n = st
    g = (g or '').replace('；', '、')          # “在这里”一段里不用“；”（视频按“；”切开）
    global _PRE
    _PRE = ''
    if n == 1 and g:
        br = bridge(i, stem, g)
        if br:
            orig, why, best = br
            _PRE = f'{stem} 本义“{orig}”：{why}，就成了“{best}”。'
            stem, g = '', best
    k = key_of(lab, line, stem)
    M = senses(i)
    if not M: return None
    m = ' / '.join(M)
    c = su.norm(lab)
    if n >= 2:
        S = f'{stem} 合起来是“{g}”，' if g else f'{stem} 合起来'
    elif _PRE:
        S = f'“{g}”'
    else:
        S = f'{stem}“{g}”' if g and stem else (stem if stem else '前面几部分合起来')
    G = g
    lit = _lit(i).replace('；', '、')
    adj = bool(g) and g.endswith('的') and not g.endswith('目的')     # 前面那部分本身是形容词（“…的”）
    def Q(tpl, ok=True):
        """模板引号里的话：母词有合适的意思就套模板，不然用构词逻辑的字面意思；都没有就不写，留给人工（不填“它”）"""
        if G and ok:
            return tpl.format(g=G)
        return lit or None
    multi = False
    if k in VN:
        a = '说的是一个动作' if multi else '是一个动作'
        return (f'在这里：动词 → 名词。{S}{a}，加上 -{c}，就把这个动作当成一样东西来说（名词前面能加 the、my，能当主语、宾语）。'
                f'一个动作当成东西，可以是这件事本身、做出来的结果、做它的本事或用的东西，所以 {word} 指{m}')
    if k == '-y@noun':
        return f'在这里：变成名词。{S}说的是一件事、一种情况，加上 -y，就成了说这件事、这种状态的名词（名词前面能加 the、my，能当主语、宾语），所以 {word} 指{m}'
    if k in AGENT:
        return f'在这里：动词 → 名词（人或东西）。{S}是一个动作，加上 -{c}，就成了“做这个动作的人或东西”（名词说的是“谁、什么东西”），所以 {word} 指{m}'
    if k == '-ee':
        q = ('被' + G + '的那个人') if G else lit
        if not q: return None
        return f'在这里：动词 → 名词（人）。{S}是一个动作，加上 -ee，就成了“{q}”，所以 {word} 指{m}'
    if k in NAGENT:
        what = '说的是一种特点或主张' if adj else '是一样东西或一门学问'
        return f'在这里：名词 → 名词（人）。{S}{what}，加上 -{c}，就成了“做这件事、搞这一行的人”，所以 {word} 指{m}'
    if k in VADJ:
        q = Q(VADJ[k], ok=not (G.endswith('的') or G.startswith('使')))
        if not q: return None
        return (f'在这里：动词 → 形容词。{S}是一个动作，加上 -{c} 变成形容词（形容词说的是“什么样的”，放在名词前面或 be 后面），'
                f'说一样东西“{q}”，所以 {word} 是{m}')
    if k in NADJ:
        q = Q(NADJ[k], ok=not adj and k != '-ly@adj')        # 名词 + -ly 套不出“有日样子的”，用字面意思“每天的”
        if not q: return None
        if adj:
            return (f'在这里：形容词 → 形容词。{S}本身说的就是“什么样的”，加上 -{c} 还是形容词（形容词说的是“什么样的”，放在名词前面去形容别的东西），'
                    f'说的是“{q}”这种性质，所以 {word} 是{m}')
        return (f'在这里：名词 → 形容词。{S}是一样东西，加上 -{c} 变成形容词（形容词说的是“什么样的”，放在名词前面去形容别的东西），'
                f'说的是“{q}”这种性质，所以 {word} 是{m}')
    if k in ADJN:
        return (f'在这里：形容词 → 名词。{S}说的是“什么样的”，是一种性质，加上 -{c}，就把这种性质当成一样东西来说（名词能当主语、宾语），所以 {word} 指{m}')
    if k in ADV:
        return (f'在这里：形容词 → 副词。{S}说东西“什么样的”，加上 -ly 变成副词，转过来说动作“是怎样做的、做到什么程度”（副词修饰动词、形容词），所以 {word} 是{m}')
    if k in XV:
        if k == '-en@verb':
            G2 = re.split('、', G)[0].rstrip('的') if G else ''
            q = lit or (('使变得' + G2) if G2 else None)      # strength + en：用字面意思“使有力量”，不写“使变得力量”
            if not q: return None
            pos = '形容词 → 动词。' + S + '说的是一种性质' if adj else '变成动词。' + S + '说的是一种性质或一样东西'
            return f'在这里：{pos}，加上 -en 变成动词（动词说的是“做什么”），意思是“{q}”，所以 {word} 是{m}'
        if G:
            return (f'在这里：变成动词。{S}说的是一样东西或一种性质，加上 -{c} 变成动词（动词说的是“做什么”），就把“{G}”变成一个动作：使它变成这样，或者让它带上这样东西，所以 {word} 是{m}')
        if not lit: return None
        return f'在这里：变成动词。{S}，加上 -{c} 变成动词（动词说的是“做什么”），就成了“{lit}”这个动作，所以 {word} 是{m}'
    if k == '-ate@verb':
        sep = '，' if S.endswith('合起来') else ''
        return f'在这里：变成动词。{S}{sep}加上 -ate，就成了一个动作（动词说的是“做什么”），所以 {word} 是{m}'
    if k in NN:
        q = lit if (adj or not G) else NN[k].format(g=G)
        if not q: return None
        if adj:
            return f'在这里：形容词 → 名词。{S}说的是“什么样的”，是一种性质，加上 -{c}，就把这种性质当成一样东西来说，指“{q}”，所以 {word} 指{m}'
        return f'在这里：名词 → 名词。{S}是一样东西或一种人，加上 -{c}，指“{q}”，所以 {word} 指{m}'
    if k in DIM:
        q = ('小' + G) if G else lit
        if not q: return None
        return f'在这里：名词 → 名词。加上 -{c}，表示“{q}”，所以 {word} 指{m}'
    return None

# ---------------- 意思怎么变 + 用词规律 ----------------
EX = {   # 规律 → （说明，例子）；例子里的词都要在总表里
 # 2026-11 用词规律轮：原来的 domain“一个词用进某一行…”、region“同一个词，英国、美国的用法有时不一样”两条取消了
 # （用户：“讲解了感觉像没有讲解”——它们只说了“有了专门意思”“两边不一样”，没讲出意思是怎么来的）。
 # 换成下面两条真规律（只手工标，不自动标）；别的情况归到 shape / narrow / wide / agent2tool / oldname……，找不到真规律的不标
 'core': ('词的核心意思不变，换了对象、场合，中文要换个说法，英语还是这个词', ['play 玩 → 踢（球）、演奏（乐器）', 'open 打开 → 开业', 'run 跑 → 经营']),
 'likefunc': ('作用、做法像什么，就借它的名字来叫', ['virus 病毒 → （电脑）病毒', 'memory 记忆力 → 内存']),
 'tool': ('表示动作的词，也拿来叫做这件事用的东西', ['transport 运 → 运输工具', 'cover 盖 → 盖子']),
 'result': ('表示动作的词，也拿来叫这个动作做出来、留下来的东西', ['invention 发明 → 发明物', 'building 建造 → 建筑物']),
 'person': ('表示动作、东西的词，也拿来叫做这件事的人', ['cook 做饭 → 厨师', 'guide 带路 → 导游']),
 'holder': ('表示性质、状态的词，也拿来叫有这种性质的人、东西或机构', ['beauty 美 → 美人', 'monopoly 垄断 → 垄断企业']),
 'agent2tool': ('表示“做这件事的人”的词，也拿来叫做这件事的东西、机器', ['computer 计算员 → 计算机', 'printer 印刷工 → 打印机']),
 'material': ('表示材料的词，也拿来叫用它做成的东西', ['glass 玻璃 → 玻璃杯', 'silver 银 → 银牌']),
 'animal': ('表示动物、植物的词，也拿来叫它的肉、皮毛、木头', ['chicken 鸡 → 鸡肉', 'lamb 小羊 → 羊肉']),
 'color': ('表示东西的词，也拿来说这种东西的颜色', ['copper 铜 → 铜色', 'silver 银 → 银色']),
 'shape': ('样子、形状像什么，就借它的名字来叫', ['mouse 老鼠 → 鼠标', 'dish 盘子 → 碟形天线']),
 'people': ('说动物、东西的词，也拿来比喻人', ['fox 狐狸 → 狡猾的人', 'swarm 蜂群 → 一大群人']),
 'feel': ('说冷热、软硬、甜苦这些感觉的词，也拿来说人的性格、态度', ['warm 暖和的 → 热情的', 'cold 冷的 → 冷淡的']),
 'time': ('说空间、位置的词，也拿来说时间', ['point 一个点 → 时刻', 'follow 跟在后面 → 接着发生']),
 'place': ('表示地方、建筑的词，也拿来代指在那儿的人或机构', ['school 学校 → 全校师生', 'corridor 走廊 → 权力中心']),
 'container': ('表示容器的词，也拿来说里面装的东西、那一份的量', ['cup 杯子 → 一杯']),
 'unit': ('装东西的容器、身体部位，也拿来当计量单位', ['foot 脚 → 英尺', 'ton 一大桶酒的分量 → 吨']),
 'plural': ('名词用复数时，常常专指一类东西、一整套或一大片', ['waters 水域', 'goods 货物']),
 'n2v': ('表示东西、性质的词，也能直接当动词用：用这样东西做事，或者使变成这样', ['water 水 → 浇水', 'clean 干净的 → 打扫']),
 'v2n': ('表示动作的词，也能直接当名词用，指这件事或做一次', ['walk 走 → 散步', 'drink 喝 → 饮料']),
 'n2adj': ('名词放在别的名词前面，也能当形容词用', ['stone 石头 → 石头做的（a stone wall）', 'gold 金子 → 金的']),
 'abstract': ('具体的意思，慢慢用到看不见、摸不着的事上：身体的动作，也拿来说心里的事', ['grasp 抓住 → 理解', 'see 看见 → 明白']),
 'degree': ('说“可怕、厉害、真的”这类词，常常变成只表示程度的“非常”', ['terribly 可怕地 → 非常', 'really 真正地 → 非常']),
 'euphem': ('不好直说的事，常换一个委婉的说法', ['depart 离开 → 去世', 'sleep 睡 → 长眠']),
 'oldname': ('东西换了代，干的还是那件事，旧名字就接着用', ['phone 电话 → 手机', 'torch 火把 → 手电筒']),
 'goodbad': ('一个词的褒贬会变：有的越用越好，有的越用越坏', ['nice 无知的 → 好的', 'silly 有福的 → 傻的']),
 'narrow': ('一个词的意思越用越窄：从一大类专指其中一种', ['meat 原来指一切食物 → 专指肉']),
 'wide': ('一个词的意思越用越宽：从一种说到一大类，或者从说一样东西到说更多东西', ['grow 草木生长 → 人、动物长大']),
}
for kk, (t, exs) in list(EX.items()):
    EX[kk] = (t, [e for e in exs if e.split()[0].lower().rstrip('s') in FIRST or e.split()[0].lower() in FIRST])
WHY = {
 'core': '英语的一个词管的是一个核心动作、核心样子，不管用在谁身上；汉语习惯按对象换词。看着像多了一个新意思，其实是老意思换了地方用，不用另背',
 'likefunc': '新东西、新做法还没有名字，看它起的作用、做事的样子像什么，就借什么的名字（和“样子像”是一对：一个看外形，一个看作用）',
 'tool': '说话时先想到动作，再用同一个词叫做这件事要用的东西，不必另造新词',
 'result': '动作做完会留下东西，母语者顺手用同一个词叫这个结果',
 'person': '做这件事的人，也用这件事来叫',
 'holder': '一种性质、状态，也拿来叫具有它的人、东西或机构',
 'agent2tool': '机器、工具替人做了这件事，就借做这件事的人的名字来叫它',
 'material': '东西用什么做，就借材料的名字叫它',
 'animal': '从动物、植物身上取下来的肉、皮、木头，还用原来的名字叫',
 'color': '看见一样东西，就借它的名字说它的颜色',
 'shape': '看着像，就借过来叫：形状相似，名字也相同',
 'people': '借动物、东西的特点来形容人',
 'feel': '把身体的感觉（冷热、软硬、甜苦）拿来比喻一个人给别人的感觉',
 'time': '人习惯把时间想成一条路，前后、远近这些说空间的词就用到了时间上',
 'place': '说一个地方，常常就是指在那里的人、机构',
 'container': '说容器，常常是指里面装的东西、那一份的量',
 'unit': '人最早拿身体、手边的容器来量东西，名字就成了单位',
 'plural': '复数把一样样东西合在一起，常常专指整套、整片的东西',
 'n2v': '英语里很多词不用改样子，直接换个词性用：东西 → 用它做事，性质 → 使变成这样',
 'v2n': '动作直接当名词用，指这件事或做一次',
 'n2adj': '名词放在别的名词前面，说明它是什么样的、用什么做的',
 'abstract': '人先认识看得见、摸得着的东西，再借这些说法去讲心里、脑子里的事',
 'degree': '说得夸张多了，原来的意思淡了，只剩下“很、非常”',
 'euphem': '不好听、不吉利的事，换一个柔和的说法',
 'oldname': '新东西顶替了老东西，干的是同一件事，大家叫惯了老名字，就接着叫',
 'goodbad': '人们常带着好恶用词，久而久之意思的好坏就变了',
 'narrow': '一个大类里最常说的那一种，慢慢独占了这个词',
 'wide': '用多了，用到更多相似的东西上，意思就变宽了',
}
DOM = r'法律|医学|医|计算机|电脑|网络|互联网|体育|篮球|足球|网球|棒球|音乐|化学|物理|数学|生物|航海|军事|宗教|商业|金融|经济|影视|电影|摄影|戏剧|语法|语言学|教学|科幻|天文|地理|建筑|艺术|新闻|印刷|农业|烹饪|美术|心理|电子|机械|游戏|植物学|动物学|解剖|统计|会计|政治|外交|天主教|基督教|赛车|拳击|高尔夫|板球'
MENTAL = r'信任|相信|理解|明白|懂|领会|想念|担心|在意|感觉|觉得|认为|记住|记得|忘|喜欢|讨厌|希望|盼|怕|害怕|决心|决定|打算|思考|思索|心情|情绪|感情|心思|主意|想法|看法|认识到|察觉|意识到'
PHYS = r'身子|拿住|抓住|抓|握|捏|靠上|推|拉|扛|搬|捡|摸|碰|挡|扔|压|敲|拴|捆|绑|撞|抱|托|举|扶|踩'
RULES = [   # (规律, 说明里的样子, 结果里的样子)
 # （2026-11 起不再按“（计算机）（英）”这类标签自动标规律：那两条空洞的说法取消了。core、likefunc 只手工标）
 ('euphem', r'委婉', r'^（委婉'),
 ('degree', r'加强语气|变成单纯|夸张|越说越重|越用越轻', r'非常|极(了|大|其)|十分|特别|简直|好极|绝了|了不起|太棒'),
 ('oldname', r'(早就|已经|如今|今天)[^，。]{0,8}不(用|是|再)[^，。]{0,12}(照样|还|仍)|词照样用|名字(还|却|就)?(留|沿用)(了)?下来|旧名字', None),
 ('material', r'用这种(料子|布|金属|木头|材料|皮|纸|石头|丝|玻璃)|这种(料子|金属|木头|材料|玻璃|纸)(做|制)的', None),
 ('animal', r'它的(肉|毛皮|皮毛|皮|毛|木头|木材)|这种(动物|鸟|鱼|鸡|羊|牛|猪|树)的(肉|皮|毛|木)', None),
 ('color', r'(这种|它的|那种)[^，。]{0,8}颜色|的颜色$', r'色(的)?$|色；|色、|色（'),
 ('shape', r'形状像|样子像|长得像|样子很像|外形像', None),
 ('people', r'拿来说人：|人也像|说人像|比喻人|拿来比喻|像[^，。]{1,8}一样的人', None),
 ('feel', r'(冷|热|暖|凉|甜|苦|酸|辣|软|硬|尖|锋利|钝|粗糙|光滑|温度|冰)', r'(热情|冷淡|冷漠|严厉|温和|温柔|和气|亲切|刻薄|尖刻|精明|敏锐|可爱|讨人喜欢|心酸|难受|苛刻|宽厚)'),
 ('time', r'时间上|用到时间|说时间|从空间到时间', None),
 ('place', r'代指(在|里面|那)|全校|全体师生|全家人|^（n\.）那(里|儿)的人', None),
 ('container', r'里面装的|装着的东西', r'^一(杯|碗|盒|箱|袋|勺|口|瓶|盘)(的量)?$'),
 ('unit', r'当(计量)?单位|拿来当[^，。]{0,4}单位|计量单位', r'（[^）]*单位）'),
 ('plural', r'（复数）', r'（复数）'),
 ('tool', r'用来(?!说|指|形容|讲|叫|表示|比喻|称)|用的(东西|工具)|做这件事用|拿来[^，。]{0,8}的(东西|工具)|的(机器|器械|装置|工具)$', r'工具|器具|手段|设备|装置|仪器'),
 ('result', r'(做|造|想|写|画|说|传|留|得|建|盖|生|产|长|挖|切|印|拍|录|编|织|烤|煮|发明|创作|翻译|剩)(了)?(出|下)(来|去)的|出来的(东西|那样|话)|过去的那样东西|做成的东西|的结果', None),
 ('person', r'做这件事的人|干这一行的人', None),
 ('holder', r'有这种[^，。]{0,6}的(人|东西|机构)|具有这种[^，。]{0,6}的|(占着|掌着|握着)[^，。]{0,10}的那(家|个)', None),
 ('n2v', r'当动词|（v\.[，）]|（vt\.[，）]|（vi\.[，）]', r'^（(v|vt|vi)\.[，）]'),
 ('n2adj', r'当形容词|（adj\.[，）]', r'^（adj\.[，）]'),
 ('v2n', r'当名词|（n\.[，）]', r'^（n\.[，）]'),
 ('abstract', r'比喻|抽象|心里看|心里“|脑子里“|用到[^，。]{0,6}(事|人|心|情感|思想)上|引申到', None),
 ('goodbad', r'(早先|原来|以前|起初|最早)[^。]{0,30}(贬|坏|臭名)[^。]{0,30}(今天|现在|后来)[^。]{0,16}(褒|好)|(早先|原来|以前|起初|最早)[^。]{0,30}(褒|好)[^。]{0,30}(今天|现在|后来)[^。]{0,16}(贬|坏)|越来越(贬|坏|差)|变成贬义|变成褒义|往贬义|往褒义|只剩褒义|只剩贬义|带上了?贬义|带上了?褒义', None),
 ('narrow', r'专指|特指|专门指', None),
 ('wide', r'泛指|统称|什么[^，。]{0,8}都(算|叫|行)|后来[^，。]{0,8}也(用|能)|扩大(成|到)|也能用来说', None),
]
def rules_of(reason, result, ctx=None):
    got = []
    pos0 = (ctx or {}).get('pos', '')
    agent = (ctx or {}).get('agent')           # 这个词本身是“做…的人”（-er、-or、-ist……）
    res0 = re.sub(r'（[^（）]*）', '', result).strip()
    for key, rr, rs in RULES:
        hit = (rr and re.search(rr, reason)) or (rs and re.search(rs, result))
        if key == 'result' and hit and re.search(r'的$', res0): hit = False          # 结果是形容词，不算“做出来的东西”
        if key == 'n2adj' and hit and re.search(r'当形容词(用)?：被|当形容词(用)?：用', reason): hit = False   # “被…了的”形式当形容词，是语法，不算规律
        if key == 'n2v' and hit and pos0 == 'v': hit = False                       # 本来就是动词
        if key == 'n2adj' and hit and pos0 in ('v', 'adj'): hit = False            # 动词、形容词本来的用法，不算名词当形容词
        if key == 'v2n' and hit:
            if pos0 == 'n': hit = False                                             # 本来就是名词
            elif pos0 == 'adj' or (ctx or {}).get('adj'):
                if 'holder' not in got: got.append('holder')
                hit = False
        if key == 'tool' and hit and re.search(r'^用来(说|指|形容)', reason): hit = False
        # 规律的前提要和这个词的词性对上：“表示动作的词…”只给动作；“做…的人”的词指机器、东西，用 agent2tool；形容词、副词不套
        if hit and key in ('tool', 'result', 'v2n') and agent:
            if key != 'v2n' and re.search(r'机器|装置|设备|仪器|器|机|软件|程序|工具|东西', res0 + reason) and 'agent2tool' not in got:
                got.append('agent2tool')
            hit = False
        if hit and key in ('tool', 'result') and pos0 in ('adj', 'adv'): hit = False
        # 2026-11 用词规律轮：“表示动作的词…”只给真的动作词——动词，或 -ion / -ment / -ing 这类动作名词；
        # 普通名词（leg“用来走路的肢体”、weapon“用来打的东西”）说明里有“用来”“…出来的”也不标
        if hit and key in ('tool', 'result') and pos0 != 'v' and not re.search(r'(ion|ment|ing|ance|ence|age|ure|sis|ery|al)$', (ctx or {}).get('word', '')): hit = False
        if key in ('feel', 'color', 'degree'): hit = bool(rr and re.search(rr, reason) and re.search(rs, result))
        if key == 'goodbad': hit = bool(re.search(rr, reason + ' → ' + result))
        if hit:
            if key == 'v2n' and any(g in got for g in ('tool', 'result', 'person', 'holder')): continue
            if key not in got: got.append(key)
        if len(got) >= 2: break
    if 'person' not in got and len(got) < 2 and re.search(r'当名词', reason) and re.search(r'(人|者|员|家|师|手)(；|、|$)', res0) and pos0 != 'n':
        got.append('person')
    if not got and re.search(PHYS, reason) and re.search(MENTAL, result) and not re.search(MENTAL, reason):
        got.append('abstract')
    return got

def short(t):
    t = re.sub(r'^(（[^（）]*）\s*)+', '', t.strip())
    t = split_top(t)[0] if t else t
    return re.sub(r'（[^（）]*）', '', t).strip()

def evolution(i, word):
    x = T[i - 2]; I = str(x[10] or '')
    if len(senses(i, 9)) < 2: return None
    steps = []
    for l in I.split('\n'):
        l = l.strip()
        if re.match(r'^[→⇒]', l) or (re.match(r'^[①②③④⑤]', l) and '→' in l):
            body = re.sub(r'^[→⇒①②③④⑤]\s*', '', l)
            ps = [p.strip() for p in re.split(r'\s*→\s*', body)]
            if len(ps) < 2 or not ps[-1]: continue
            steps.append((' → '.join(ps[:-1]), ps[-1], body))
    if len(steps) < 2: return None
    pl = su.parse_logic(I.split('\n')[0]) if I else None
    lit = ''
    if pl and pl[0] == 'eq': lit = pl[2]
    elif pl and pl[0] == 'route' and pl[1]: lit = pl[1][-1][1]
    if re.search(r'[（）()+=]', lit) or lit.count('“') != lit.count('”'): lit = ''
    order, used = [], {}
    parts = []
    prev = lit
    S0 = senses(i, 9)
    pos0 = ''
    for l in [JY(i)]:
        if l.startswith('【今义】'):
            m0 = re.match(r'^【今义】\s*[（(]([a-z]+)\.', l)
            if m0: pos0 = {'v': 'v', 'vt': 'v', 'vi': 'v', 'n': 'n', 'adj': 'adj', 'adv': 'adv'}.get(m0.group(1), '')
    ctx = {'pos': pos0, 'word': word, 'adj': bool(lit and lit.endswith('的')),
           'agent': bool(re.search(r'在这里：[^。]*名词（人', str(x[9] or '')))}
    for k, (reason, result, body) in enumerate(steps[:6]):
        tags = rules_of(reason, result, ctx)
        marks = []
        for t in tags:
            if t not in used:
                used[t] = len(order); order.append((t, reason, result))
            marks.append('①②③④⑤⑥'[used[t]])
        parts.append(f'{"①②③④⑤⑥"[k]} {body}' + (f'〔用词规律{"".join(marks)}〕' if marks else ''))
        prev = result
    head = f'意思怎么变：从字面的“{lit}”出发：' if lit and '“' not in lit else '意思怎么变：'
    evo = head + ' '.join(parts)
    rule = None
    if order:
        items = []
        for n, (t, reason, to) in enumerate(order):
            text, exs = EX[t]
            to_s = short(to); core = short(S0[0]) if S0 else ''
            same = (not core) or core == to_s or core in to_s or to_s in core
            if t == 'plural':
                mine = f'{word if word.endswith("s") else word + "s"} {to_s}'
            elif t in ('abstract', 'wide', 'narrow') or same:
                rs = re.sub(r'^当(动|名|形容)词[：:]\s*', '', re.sub(r'（[^（）]*）', '', reason).strip())
                mine = f'{word}：{rs} → {to_s}' if rs and len(rs) <= 24 else f'{word} {to_s}'
            else:
                mine = f'{word} {core} → {to_s}'
            ex = '；'.join([mine] + [e for e in exs if not e.split()[0].lower().startswith(word.lower())][:1])
            items.append(f'{"①②③④⑤⑥"[n]} {text}（{ex}）')
        rule = '用词规律：' + ' '.join(items)
    return evo, rule

# ---------------- 模板套不上时的通用写法（少见后缀、母词意思取不到、今义带英文的词）----------------
# 在这里：{词性变化}。{前面部分}加上 -xx（后缀的意思），合起来是“{构词逻辑的字面意思}”，所以 W 是/指 {今义}
POS_KEY = {
 '-s@pl': '名词 → 名词（复数）', '-es@pl': '名词 → 名词（复数）',
 '-s@adv': '变成副词', '-es@adv': '变成副词', '-wards': '变成副词', '-ward': '变成形容词、副词',
 '-ing@both': '动词 → 名词、形容词', '-ing@noun': '动词 → 名词', '-ing@adj': '动词 → 形容词',
 '-le@freq': '动词 → 动词（一下一下、反复地做）', '-er@freq': '动词 → 动词（一下一下、反复地做）',
 '-er@comp': '形容词 → 形容词（比较级）', '-est': '形容词 → 形容词（最高级）', '-st': '形容词 → 形容词（最高级）',
 '-ed@pp': '动词 → 形容词（被…了的）', '-d@pp': '动词 → 形容词（被…了的）', '-en@pp': '动词 → 形容词（已经…了的）', '-n@pp': '动词 → 形容词（已经…了的）',
 '-ed@adj': '名词 → 形容词', '-d@adj': '名词 → 形容词', '-ly@adv': '形容词 → 副词', '-ly@adj': '名词 → 形容词',
 '-ish@verb': '变成动词', '-ish@adj': '名词 → 形容词', '-ate@adj': '变成形容词', '-ate@verb': '变成动词', '-en@verb': '变成动词',
 '-ize': '变成动词', '-ise': '变成动词', '-ify': '变成动词', '-fy': '变成动词',
 '-th@noun': '变成名词', '-th@ord': '数词 → 序数词', '-teen': '数词 → 数词', '-ty@tens': '数词 → 数词',
 '-er@agent': '动词 → 名词（人或东西）', '-r@agent': '动词 → 名词（人或东西）', '-or': '动词 → 名词（人或东西）',
 '-ess': '名词 → 名词（女性）', '-eer': '名词 → 名词（人）', '-ier': '名词 → 名词（人）', '-ist': '名词 → 名词（人）',
 '-an@n': '名词 → 名词（人）', '-ian': '名词 → 名词（人）', '-ee': '动词 → 名词（人）', '-ness': '形容词 → 名词', '-cy': '形容词 → 名词', '-acy': '形容词 → 名词',
}
NOUN_FAM = set('-ad -ac -tra -tre -graph -oon -our -ie -ett -ute -ace -ito -k -ch -tue -red -ey -yer -io -ario -ies -ia -us -um -a -o -ics -t -el -cle -ium -um -ion -ation -tion -sion -ment -ure -ture -ature -age -ity -ty -ism -ics -logy -logue -graphy -nomy -metry -ess -eer -ier -ist -ee -kin -let -ling -ette -et -ot -ule -cule -icule -ella -illa -eria -orium -oir -ade -ado -ard -ery -ry -tery -try -mony -ony -menon -crat -naut -tor -itor -ador -ista -wala -ia -ica -ma -m(a) -mat -me -eme -ene -ol -in -ine -gen -oid -lyte -ode -rithm -scape -ledge -ware -ance -ence -ency -ancy -ice -itude -tude -iasm -ast -arian -zen -men -eum -ion -ison -iation -ification'.split())
ADJ_FAM = set('-id -ile -ic -able -ible -ble -bile -al -ial -ual -ar -ous -ious -tious -orious -ive -ful -less -etic -ique -ulent -olent -aneus -istic -escent -esque -ern -some -like -fic -ical -ese -wide -proof -free -ish -y -ane -ine -ant -ent -ient'.split())
VERB_FAM = set('-ate -ize -ise -ify -fy -en -ish -le -er'.split())
TAGS = {'v': '动词', 'vt': '动词', 'vi': '动词', '动': '动词', 'n': '名词', '名': '名词', 'adj': '形容词', '形': '形容词', 'adv': '副词', '副': '副词'}

def senses_loose(i, n=3):
    """今义里的几个意思（比 senses 宽：可以带英文、长到 16 个字；去掉开头的 = xxx：、①②）"""
    for l in [JY(i)]:
        if not l.startswith('【今义】'): continue
        body = re.sub(r'^=\s*[A-Za-z][A-Za-z\- ]*[：:]\s*', '', l[4:].strip())
        out = []
        for seg in split_top(body):
            t = re.sub(r'^[\u2460-\u2473]\s*', '', seg)
            while True:
                m = re.match(r'^[（(][^（）()]*[）)]\s*', t)
                if not m: break
                t = t[m.end():]
            t = re.sub(r'（[^（）]*）|\([^()]*\)', '', t).strip()
            t = re.split(r'[：:]', t)[0].strip().rstrip('，、。')
            if t and len(t) <= 16 and re.search('[\u4e00-\u9fff]', t) and t not in out: out.append(t)
            if len(out) >= n: break
        return out
    return []

def _clean_gloss(g, n=12):
    g = (g or '').replace('；', '、').strip()
    return '' if (not g or re.search(r'[“”（）()=]', g) or len(g) > n) else g

def _pos_label(i, k, lab, M):
    if any(re.search('过去分词|过去式', x) for x in M) and re.search(r'@pp$|^-(ed|d|en|n|t|ten|ne)$', k): return '动词 → 动词（过去式、过去分词）'
    if k in POS_KEY: return POS_KEY[k]
    jin = JY(i)
    m = re.match(r'^【今义】\s*[（(]([^（）()]*)[）)]', jin)
    if m:
        t = re.split(r'[.，,、\s/]', m.group(1).strip())[0].lower()
        if t in TAGS: return '变成' + TAGS[t]
    if M and M[0].endswith('的'): return '变成形容词'
    if M and M[0].endswith('地'): return '变成副词'
    base = lab.split('@')[0]
    for fam, name in ((NOUN_FAM, '名词'), (ADJ_FAM, '形容词'), (VERB_FAM, '动词')):
        if base in fam and not (name == '动词' and base in ('-ish', '-le', '-er', '-en')):
            return '变成' + name
    return '合起来看'

def _fallback(i, lab, line, word):
    M = senses(i) or senses_loose(i)
    if not M: return None
    lit = _lit(i).replace('；', '、')
    if not lit or '它' in lit: return None
    c = su.norm(lab)
    st = stem_of(i, lab)
    pl = _eq_parse(i)
    sg, base = '', []
    if pl and pl[0] == 'eq' and pl[1]:
        terms = pl[1]
        idx = [k for k, (t, g) in enumerate(terms) if su.norm(t) == c]
        j = idx[-1] if idx else len(terms) - 1
        sg = _clean_gloss(terms[j][1]) if 0 <= j < len(terms) else ''
        base = terms[:j]
    elif pl and pl[0] == 'route' and len(pl[1]) >= 2:
        base = [pl[1][-2]]
    clean_t = lambda t: re.sub(r'\(([a-z]+)\)', r'\1', t.strip())
    if st and st[2] >= 2:
        S = st[0] + ' '
    elif st:
        g = _clean_gloss(st[1])
        S = f'{st[0]}“{g}”' if g else st[0] + ' '
    elif len(base) == 1:
        g = _clean_gloss(base[0][1])
        S = f'{clean_t(base[0][0])}“{g}”' if g else clean_t(base[0][0]) + ' '
    elif len(base) >= 2:
        S = ' + '.join(clean_t(t) for t, _ in base) + ' '
    else:
        return None
    if not re.search('[A-Za-z]', S) or re.search(r'[“”（）\u3400-\u9fff]', S.split('“')[0]): return None
    k = key_of(lab, line, st[0] if st else '')
    label = _pos_label(i, k, lab, M)
    verb = '指' if re.search(r'名词(（[^）]*）)?$', label) else '是'
    return (f'在这里：{label}。{S}加上 {lab}' + (f'（{sg}）' if sg else '') + f'，合起来是“{lit}”，所以 {word} {verb}' + ' / '.join(x.replace('；', '、') for x in M))

_PRE = ''
def pos_sentence(i, lab, line, word):
    r = _pos_sentence(i, lab, line, word)
    if r and _PRE: r = r.replace('。', '。' + _PRE, 1)
    if not r: r = _fallback(i, lab, line, word)          # 模板套不上的，用通用写法，不再空着
    return r

def run():
    su.here_sentence = lambda i, lab, word: pos_sentence(i, lab, su_line[0], word)
    su.ROLE_DONE = re.compile(r'在这里：|词性')
    H = {i: str(x[9] or '').split('\n') for i, x in enumerate(T, start=2)}
    recs = []
    global su_line
    for i, x in enumerate(T, start=2):
        w = str(x[4])
        for k, l in enumerate(H[i]):
            m = LAB.match(l)
            if not m: continue
            lab = m.group(1).strip()
            if ' ' in lab or not lab.startswith('-') or lab.endswith('-'): continue
            su_line = [l]
            new, did = su.upgrade_line(i, lab, l, w)
            if new and duplicated(l, new): new = None          # 再跑一遍时不重复补同一段话
            if new:
                H[i][k] = new; recs.append(('后缀：' + '、'.join(did), i, w, lab, l, new))
    # 前缀补来源、in- 补见 in、-ly 补见 like、跨组同源恢复：沿用上一轮的做法
    H2, recs2 = su.run()
    for cat, i, w, lab, old, new in recs2:
        if cat.startswith('后缀') and '见 like' not in cat: continue
        k = next((j for j, l in enumerate(H[i]) if l == old), None)
        if k is None:
            k = next((j for j, l in enumerate(H[i]) if l.startswith(lab + '：')), None)
            if k is None: continue
            if cat.startswith('后缀'):
                n2 = re.sub(r'(和 like (?:同源|是一家)|和 like 是同一个[^，；。）]*)(）)', r'\1，见 like\2', H[i][k], count=1)
                if n2 == H[i][k]: n2 = re.sub(r'(和 like (?:同源|是一家))', r'\1（见 like）', H[i][k], count=1)
                if n2 != H[i][k] and not re.search(r'见 like(?![A-Za-z])', H[i][k]): H[i][k] = n2
                continue
            continue
        if duplicated(H[i][k], new): continue
        H[i][k] = new; recs.append((cat, i, w, lab, old, new))
    # 意思怎么变、用词规律
    for i, x in enumerate(T, start=2):
        if any(l.startswith('意思怎么变：') for l in H[i]): continue
        r = evolution(i, str(x[4]))
        if not r: continue
        evo, rule = r
        H[i].append(evo); recs.append(('意思怎么变', i, str(x[4]), '意思怎么变', '', evo))
        if rule: H[i].append(rule); recs.append(('用词规律', i, str(x[4]), '用词规律', '', rule))
    return H, recs

def duplicated(old, new):
    pieces = [p.strip() for p in re.split(r'[；（）]', new) if len(p.strip()) >= 10]
    return any(new.count(p) > old.count(p) >= 1 for p in pieces)

su_line = ['']
if __name__ == '__main__':
    H, recs = run()
    pickle.dump((H, recs), open(os.path.join(os.environ.get('ETY_WORK', '.'), 'pos_changes.pkl'), 'wb'))
    print(len(recs), collections.Counter(r[0].split('：')[0] for r in recs).most_common())
    print('例子缺词：', {k: v[1] for k, v in EX.items()})

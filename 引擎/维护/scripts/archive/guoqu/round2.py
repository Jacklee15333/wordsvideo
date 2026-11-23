"""过去分词轮（二）（2026-11）：
1. reduce + tion、produce + tion 这类 -tion 词（还有 nutri + tion、mix + ture）照第 54 条改成 reduct(=reduce) + ion（沿用 round.py 的改法，data.py 补了 5 个词）；
2. 所有写成过去分词词干的行，音变列第一行写【字母变化】链：拉丁语原形 → 过去分词 → 拉丁语名词 → 英语
   （describere（拉丁语）→ descriptus（拉丁语）→ descriptio（拉丁语）→ description（英语）），下面每一步一行，
   讲清过去分词怎么构成、为什么这样变（-are 动词加 -tus 成了 -atus；b 碰上 t 变成 p；d 碰上 t 念成 s……）、怎么进入英语；
   原来讲同一件事的一句话由步骤取代，别的说明加标签留在后面。
用法：python3 round2.py <源.xlsx> <新.xlsx>（同目录要有 round.py、data.py）"""
import sys, re, os, copy
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, 'round.py'), encoding='utf-8').read().split('# ---------- 「整表核对记录」')[0]
_src = _src.replace("'ature': 'ure', 'ure': 'ure'}", "'ature': 'ure', 'ture': 'ure', 'ure': 'ure'}")
_src = _src.replace("warn.append(f'{w} 已经有构词行，跳过'); continue", "continue")
exec(compile(_src, os.path.join(HERE, 'round.py'), 'exec'))        # 得到 b、ws、done_L（这一轮新改拆分的词）、E、L_DATA……
NEW = list(done_L)

# ---------------------------------------------------------------- 过去分词怎么构成（第二步）
KIND = {}
for k, vs in {
    'are': 'publicare organizare durare qualificare quotare restaurare explanare destinare vegetare exspectare notificare applicare salvare '
           'examinare praeparare informare transformare combinare modificare clarificare reputare vocare registrare explorare occupare '
           'recitare continuare praesentare repraesentare vacare invitare inspirare aspirare certificare determinare fundare confirmare '
           'considerare observare conservare praeservare reservare pronuntiare inclinare relaxare configurare adaptare variare limitare '
           'recommendare obligare installare refrigerare cancellare temptare intonare administrare gravitare exclamare purificare condensare '
           'infestare ovare curare comparare figurare temperare signare laborare respirare imperare miniare',
    'ari': 'conversari imaginari confrontari medicari admirari commentari',
    'ire': 'definire expedire nutrire',
    'itus': 'competere repetere addere',
    'pon': 'opponere supponere componere', 'quaer': 'acquirere', 'gnosc': 'recognoscere',
    'bt': 'describere subscribere', 'ct': 'reducere introducere producere',
    'dt': 'decidere dividere providere includere concludere excludere expandere extendere suspendere explodere persuadere invadere erodere collidere',
    'tend': 'attendere', 'vert': 'convertere', 'mitt': 'emittere permittere admittere', 'vt': 'solvere resolvere evolvere',
    'cip': 'recipere percipere', 'ten': 'retinere', 'stru': 'destruere', 'fac': 'satisfacere', 'misc': 'miscere'}.items():
    for v in vs.split():
        KIND[v] = k
DT_EXTRA = {'decidere': '；caedere“砍”进了复合词，ae 弱化成 i', 'collidere': '；laedere“撞”进了复合词，ae 弱化成 i',
            'includere': '；claudere“关”进了复合词，au 弱化成 u', 'concludere': '；claudere“关”进了复合词，au 弱化成 u',
            'excludere': '；claudere“关”进了复合词，au 弱化成 u', 'explodere': '；plaudere“拍手”进了复合词，au 变成 o',
            'extendere': '（tendere 的过去分词有 tensus、tentus 两种，这里用 tensus，同 tension）'}
PPH = '拉丁语变成过去分词（“被…了的”形式）'


def step2(inf, pp):
    k, s3 = KIND[inf], inf[:-3]
    if k in ('are', 'ire'):
        v = 'a' if k == 'are' else 'i'
        return f'② {PPH}，要把原形的词尾 -re 换成 -tus；{inf} 这类 -{k} 动词，词干末尾本来就是 {v}（{inf[:-2]}-），加上 -tus 就成了 -{v}tus：{inf} → {pp}'
    if k == 'ari':
        return f'② {PPH}：{inf} 是形式像被动的 -ari 动词，词干末尾也是 a（{inf[:-2]}-），加上 -tus 就成了 -atus：{inf} → {pp}'
    if k == 'itus':
        return f'② {PPH}：{inf} 这一类动词，在词干 {s3}- 和 -tus 之间要加一个连接元音 i，成了 -itus（同 petere → petitus、monere → monitus）：{inf} → {pp}'
    if k == 'pon':
        return f'② ponere“放”的过去分词不规则，是 positus（词根本来是 pos-，现在时才多了一个 n）；{inf} 跟着变成 {pp}（同 position）：{inf} → {pp}'
    if k == 'quaer':
        return '② quaerere“求”的过去分词是 quaesitus：r 变成 s，再加 -itus；进了复合词，ae 弱化成 i（同 require → requisition）：acquirere → acquisitus'
    if k == 'gnosc':
        return '② 原形里的 -sc- 是现在时才有的成分，过去分词直接用词根 gno-，加 -itus 时 o 弱化掉了（同 cognition）：recognoscere → recognitus'
    if k == 'bt':
        return (f'② {PPH}，在词干 {s3}- 后面加 -tus；b 碰上 t 变成 p：b 要振动声带，t 不振动，连着念时 b 被 t 带得也不振动了，'
                f'就成了同一个部位的 p（同 absorbere → absorptus）：{inf} → {pp}')
    if k == 'ct':
        return f'② {PPH}，在词干 {s3}- 后面加 -tus；c 本来就是不振动声带的清音，和 t 直接连在一起，成了 ct：{inf} → {pp}'
    if k == 'dt':
        return f'② {PPH}，在词干 {s3}- 后面加 -tus；d 碰上 t，两个舌尖音挤在一起念成了 s（拉丁语 dt → ss → s）{DT_EXTRA.get(inf, "")}：{inf} → {pp}'
    if k == 'tend':
        return '② tendere“伸”的过去分词有 tentus、tensus 两种写法；attendere 用 tentus，d 碰上 t 并成了一个 t（同 intend → intention；extend → extension 用的是 tensus）：attendere → attentus'
    if k == 'vert':
        return '② 在词干 convert- 后面加 -tus；t 碰上 t，两个舌尖音挤在一起念成了 s（同 divert → diversion）：convertere → conversus'
    if k == 'mitt':
        return f'② mittere“送”的词干是 mitt-，加 -tus 时 tt 碰上 t，念成了 ss（同 mission）：{inf} → {pp}'
    if k == 'vt':
        return f'② {PPH}，在词干 {s3}- 后面加 -tus；v 在 t 前变回元音 u（拉丁语的 v 本来就是 u 的辅音念法）：{inf} → {pp}'
    if k == 'cip':
        return f'② capere“拿”进了复合词，a 弱化成 i（{inf}）；到了过去分词弱化成 e，p 再碰上 -tus（同 accept、concept）：{inf} → {pp}'
    if k == 'ten':
        return '② tenere“握”进了复合词，e 弱化成 i（retinere）；过去分词还是 ten- 加 -tus（同 content、detention）：retinere → retentus'
    if k == 'stru':
        return '② struere“堆、建”的过去分词是 structus：它古时候的词根是 *strug-，g 碰上 t 变成了 c（同 instruct、construct）：destruere → destructus'
    if k == 'fac':
        return '② facere“做”的过去分词是 factus：词干 fac- 加 -tus，c 和 t 直接连在一起（同 fact、factory）：satisfacere → satisfactus'
    if k == 'misc':
        return '② miscere 的过去分词是 mixtus：词干 misc- 碰上 -tus，sc 和 t 挤在一起，写成 x（读 ks）：miscere → mixtus'
    raise KeyError(inf)


SUFX = {'ion': '名词词尾 -io，就是“…这件事”', 'ive': '形容词词尾 -ivus，就是“有…性质的”', 'ory': '形容词词尾 -orius，就是“与…有关的”',
        'ure': '名词词尾 -ura，就是“…的结果、状态”', 'or': '表示人的 -or，就是“做…的人”'}
CHG = {'ive': '-ivus 到法语里成了 -if，英语写成 -ive', 'ory': '-orius 到英语里写成 -ory', 'ure': '-ura 到法语、英语里写成 -ure'}
STEP1 = {'publication': '① 拉丁语原形 publicare“公开”：由形容词 publicus“公开的”造出来的动词；英语的形容词 public 来自 publicus，经法语来的动词成了 publish',
         'medication': '① 拉丁语原形 medicari“医治”：由 medicus“医生”造出来的动词（同 medicine）',
         'gravitation': '① 近代拉丁语照 gravitas“重”造出动词 gravitare“受重力牵引”（gravity 也来自 gravitas）',
         'imperative': '① 拉丁语原形 imperare“下令”：in + parare“备好”，“要人把东西备好交上来”；进了复合词，a 弱化成 e',
         'mixture': '① 拉丁语原形 miscere“混合”；英语的动词 mix 不是直接从它来的，而是 15 世纪末从 mixt“混合了的”（拉丁语过去分词 mixtus 经法语变来）倒推出来的'}
NV_EXTRA = {'pronunciation': 'pronounce 经法语把 u 变成了 ou，名词照拉丁语保留 u（ti 写成 ci）'}
FULL = {
    'sensitive': '''【字母变化】sentire（拉丁语）→ sensus（拉丁语）→ sensitivus（中世纪拉丁语）→ sensitive（英语）
① 拉丁语原形 sentire“感觉”：英语的 sense、sentence、sentiment 都是它这一家
② 拉丁语变成过去分词（“被…了的”形式），在词干 sent- 后面加 -tus；t 碰上 t，两个舌尖音挤在一起念成了 s：sentire → sensus（英语 sense 就是它）
③ 中世纪拉丁语造“有…性质的”形容词，照 positivus 这类词在 sens- 后面多加了 it，再加 -ivus：sensus → sensitivus
④ 14 世纪末经古法语 sensitif 进入英语：-ivus 到法语里成了 -if，英语写成 -ive：sensitivus → sensitive''',
    'sensation': '''【字母变化】sensus（拉丁语）→ sensatus（晚期拉丁语）→ sensatio（中世纪拉丁语）→ sensation（英语）
① 拉丁语 sensus“感觉”：sentire“感觉”的过去分词当名词用（英语 sense 就是它）
② 晚期拉丁语在名词后面加 -atus，造出形容词 sensatus“有感觉的”，和过去分词一样以 -atus 结尾：sensus → sensatus
③ 去掉词尾 -us，留下词干 sensat-，加上名词词尾 -io，就是“感觉到这件事”：sensatus → sensatio
④ 1610 年代经法语进入英语：法语、英语的 -ion 来自拉丁语名词的变格形式 sensationem：sensatio → sensation''',
    'constellation': '''【字母变化】stella（拉丁语）→ stellatus（拉丁语）→ constellatio（晚期拉丁语）→ constellation（英语）
① 拉丁语 stella“星”，词根是 stell-（和 star 同一个老祖宗）
② 名词后面加 -atus，造出形容词 stellatus“布满星星的”，和过去分词一样以 -atus 结尾：stella → stellatus
③ 前面加上 con-“一起”，去掉 -us、加名词词尾 -io，就是“星星聚在一起的样子”：stellatus → constellatio
④ 14 世纪经古法语进入英语：法语、英语的 -ion 来自变格形式 constellationem：constellatio → constellation''',
    'literature': '''【字母变化】littera（拉丁语）→ litteratus（拉丁语）→ litteratura（拉丁语）→ literature（英语）
① 拉丁语 littera“字母、文字”，词根是 liter-（英语 letter 是它经法语变来的样子）
② 名词后面加 -atus，造出形容词 litteratus“写满字母的、有文字修养的”，和过去分词一样以 -atus 结尾：littera → litteratus
③ 去掉词尾 -us，留下词干 litterat-，加上名词词尾 -ura，就是“用字母写成的东西”：litteratus → litteratura
④ 15 世纪初进入英语：用了 litera 的单 t 写法（拉丁语 littera、litera 两种拼法都有），-ura 到法语、英语里写成 -ure：litteratura → literature''',
    'miniature': '''【字母变化】miniare（拉丁语）→ miniatus（拉丁语）→ miniatura（意大利语）→ miniature（英语）
① 拉丁语原形 miniare“用铅丹涂红”：由 minium“铅丹”（一种红色颜料）造出来的动词
② 拉丁语变成过去分词（“被…了的”形式），miniare 这类 -are 动词，词干末尾本来就是 a（minia-），加上 -tus 就成了 -atus：miniare → miniatus
③ 意大利语照拉丁语的规矩，去掉 -us、加名词词尾 -ura，“用红铅丹画出来的东西”，转指手抄本彩饰、小画：miniatus → miniatura
④ 1580 年代进入英语，-ura 写成 -ure：miniatura → miniature'''}
# 原来音变列里没标签的那句话：多数是讲同一件变化的，由步骤取代；还有别的内容的加标签留着
P_KEEP = {'publication': '【对照】', 'imperative': '【拼写】', 'information': '【拼写】', 'occupation': '【拼写】', 'representative': '【短形式】',
          'relaxation': '【读音】', 'laboratory': '【读音】', 'obligation': '【读音】', 'cancellation': '【拼写】', 'temptation': '【拼写】',
          'administration': '【拼写】',
          'acquisition': ('【同类】', 'ae 变成 i 的还有 require、exquisite，都是 quaerere“求”这一家'),
          'explanation': ('【对照】', '动词有 ai、名词只有 a：动词受 plain 影响改了拼写，名词照拉丁语 explanatio 写（同 exclaim → exclamation、proclaim → proclamation）'),
          'application': ('【同类】', 'multiply → multiplication、reply → replication 也一样，名词里还原成拉丁语的 plic'),
          'admiration': ('【读音】', '重音落在 -a- 上：ad-mi-RA-tion'),
          'exclamation': ('【同类】', 'proclaim → proclamation、reclaim → reclamation 也一样，名词里 ai 回到拉丁原形 a')}


def ety_text(word, keys):
    es = E.get(word.lower(), [])
    for e in es:
        t = e.get('etymology', '')
        if any(k and k in t for k in keys):
            return t
    return es[0].get('etymology', '') if es else ''


def year_txt(t):
    t = t[:220]
    m = re.search(r'(c\. )?\b(\d{4})(s?)\b', t)
    if m:
        return ('约 ' if m.group(1) else '') + m.group(2) + (' 年代' if m.group(3) else ' 年')
    m = re.search(r'(early|mid-|late)?\s*\b(\d{1,2})c\.', t)
    return (m.group(2) + ' 世纪' + {'early': '初', 'mid-': '中', 'late': '末'}.get(m.group(1) or '', '')) if m else ''


def via_txt(t):
    t = t[:300]
    return '经古法语' if 'Old French' in t else '经法语' if 'French' in t else '直接从拉丁语' if 'Latin' in t else ''


def note_side(note):
    if not note:
        return '', ''
    if re.search(r'经法语|的 y |-ize 是|的 er |的 ea|的 ai|照 pose|倒推', note):
        return note, ''
    if '过去分词' in note:
        return '', ''
    return '', note


b.tag = '过去分词音变'
did, dropped, kept_lab, warn2 = [], [], 0, []
for r in range(2, ws.max_row + 1):
    w = str(ws.cell(r, C.WORD).value or '')
    if '过去分词：拆分' not in str(ws.cell(r, C.ADJ).value or '') or w not in L_DATA:
        continue
    oldP = str(ws.cell(r, C.SOUND).value or '').strip()
    if oldP.startswith('【字母变化】'):
        warn2.append(f'{w} 音变列已经有链，跳过'); continue
    d = L_DATA[w]
    ps = parse_split(str(ws.cell(r, C.SPLIT).value or ''))
    P = ps[-1]['surface'].strip().lower()
    stp = next(p for p in ps if p['eqs'])
    stem, base = stp['surface'].strip(), stp['eqs'][0]
    kline = next((l for l in str(ws.cell(r, C.ROOT).value or '').split('\n') if (C.label_of(l) or '').strip('-').lower() == stem.lower()), '')
    is_word = '由词根' not in kline
    inf, g, lstem, cls = d['inf'], d['g'], d['lstem'], d.get('cls', 'L')
    pp, N = lstem + 'us', d.get('N') or lstem + LATSUF[P]
    nv, nn = note_side(d.get('note', ''))
    nv = NV_EXTRA.get(w, nv)
    if w in FULL:
        chain_steps = FULL[w].split('\n')
    else:
        tn = ety_text(w, [N[:6], lstem[:5]])
        yr, via = year_txt(tn), via_txt(tn)
        m = re.search(r'(Late|Medieval|Modern) Latin\s+' + re.escape(N[:6]), tn)
        nlang = {'Late': '晚期拉丁语', 'Medieval': '中世纪拉丁语', 'Modern': '近代拉丁语'}[m.group(1)] if m else '拉丁语'
        ilang = '近代拉丁语' if w == 'gravitation' else '拉丁语'
        if w in STEP1:
            s1 = STEP1[w]
        elif is_word:
            tv = ety_text(base, [inf[:4]])
            vv = via_txt(tv) if inf[:4] in tv else ''
            s1 = f'① 拉丁语原形 {inf}“{g}”：英语的动词 {base} 就来自这个原形' + (f'（{vv}进入英语）' if vv else '') + (f'；{nv}' if nv else '')
        else:
            s1 = f'① 拉丁语原形 {inf}“{g}”，词根是 {base}-' + (f'；{nv}' if nv else '')
        s2 = step2(inf, pp)
        if cls == 'E':
            chain = f'【字母变化】{inf}（{ilang}）→ {pp}（拉丁语）→ {w.lower()}（英语）'
            s3 = f'③ {yr}英语照拉丁语的规矩，在过去分词词干 {lstem}- 后面直接加上 -{P}' + (f'；{nn}' if nn else '') + f'：{pp} → {w.lower()}'
            chain_steps = [chain, s1, s2, s3]
        elif P == 'or':
            chain = f'【字母变化】{inf}（{ilang}）→ {pp}（拉丁语）→ {N}（{nlang}、英语）'
            s3 = (f'③ 去掉过去分词的词尾 -us，留下词干 {lstem}-，加上{SUFX["or"]}：{pp} → {N}；' + f'{yr}{via}进入英语，原样没变')
            chain_steps = [chain, s1, s2, s3]
        else:
            sx = '表示地方的 -orium，就是“做…的地方”' if w == 'laboratory' else SUFX[P]
            chg = ('-orium 到英语里写成 -ory' if w == 'laboratory' else
                   f'法语、英语的 -ion 来自拉丁语名词的变格形式 {N}nem' if P == 'ion' else CHG[P])
            chain = f'【字母变化】{inf}（{ilang}）→ {pp}（拉丁语）→ {N}（{nlang}）→ {w.lower()}（英语）'
            s3 = f'③ 去掉过去分词的词尾 -us，留下词干 {lstem}-，加上{sx}：{pp} → {N}'
            s4 = f'④ {yr}{via}进入英语：{chg}' + (f'；{nn}' if nn else '') + f'：{N} → {w.lower()}'
            chain_steps = [chain, s1, s2, s3, s4]
    keep = []
    for l in oldP.split('\n'):
        l = l.strip()
        if not l or l in ('-', '—'):
            continue
        if l.startswith('【'):
            keep.append(l); continue
        segs = re.split(r'[。；](?=【)', l)
        if len(segs) > 1:
            keep += [x for x in segs if x.startswith('【')]; dropped.append((w, segs[0])); continue
        rule = P_KEEP.get(w)
        if rule:
            keep.append((rule if isinstance(rule, str) else rule[0]) + (l if isinstance(rule, str) else rule[1])); kept_lab += 1
        else:
            dropped.append((w, l))
    ws.cell(r, C.SOUND).value = '\n'.join(chain_steps + keep)
    b.note(r, f'音变列第一行写【字母变化】链 {chain_steps[0].replace("【字母变化】", "")}，下面每一步讲清怎么变、为什么这样变'
              + ('；原来讲同一件变化的那句话由步骤取代' if any(x[0] == w for x in dropped) else ''))
    b._fit(r); did.append(w)

print('这一轮新改拆分：', NEW)
print('音变列写了链的行：', len(did), '；原来那句话由步骤取代的', len({x[0] for x in dropped}), '；加标签留下的', kept_lab)
print('\n'.join(warn2))
open(os.path.join(HERE, 'review2.txt'), 'w', encoding='utf-8').write(
    '\n'.join(f'##### {r} {w}\n' + str(ws.cell(r, C.SOUND).value) for r in range(2, ws.max_row + 1)
              for w in [str(ws.cell(r, C.WORD).value or '')] if w in did) + '\n\n===== 由步骤取代的旧说明\n' + '\n'.join(f'{w}｜{l}' for w, l in dropped))

# ---------- 「整表核对记录」
b.fixed_other('过去分词：音变列',
              'describe 和 description 这类，动词和名词的字母不一样（be → pt、d → s、多出 it、at），音变列没讲清是怎么变的、为什么这样变（用户提出）',
              f'{len(did)} 行音变列第一行写【字母变化】链：拉丁语原形 → 过去分词 → 拉丁语名词 → 英语（describere → descriptus → descriptio → description），'
              '下面每一步一行：① 拉丁语原形，英语的动词就来自它；② 过去分词怎么构成、为什么这样变（-are 动词加 -tus 成了 -atus；b 碰上 t 变成 p；d 碰上 t 念成 s；'
              'v 变回元音 u；复合词里 a 弱化成 i、e……）；③ 去掉 -us、加 -io / -ivus / -orius / -ura；④ 什么时候、经什么语言进入英语。'
              '原来讲同一件变化的一句话由步骤取代，别的说明加上【对照】【拼写】【读音】【同类】【短形式】标签留在后面。逐行见 U 列“过去分词音变：…”')
b.fixed_other('-tion 词',
              'reduce + tion、produce + tion、introduce + tion、nutri + tion、mix + ture 的 t 也是过去分词带来的，上一轮没改',
              f'{len(NEW)} 行照第 54 条改成过去分词词干：' + '、'.join(NEW) + '（reduct(=reduce) + ion、mixt(=mix) + ure……），组合列加构词行')

# ---------- 「说明」
S = b.wb['说明']
def row_of(a):
    return next(i for i in range(1, S.max_row + 1) if S.cell(i, 1).value == a)
i = row_of('P 音变 / 字母变化')
add = ('名词、形容词接在拉丁语过去分词词干上的（description、competition、decision），第一行也写链：拉丁语原形 → 过去分词 → 拉丁语名词 → 英语'
       '（describere（拉丁语）→ descriptus（拉丁语）→ descriptio（拉丁语）→ description（英语）），下面每一步讲清怎么变、为什么这样变'
       '（-are 动词加 -tus 成了 -atus；b 碰上 t 变成 p；d 碰上 t 念成 s；动词来自原形，名词来自过去分词）。')
if add not in str(S.cell(i, 2).value):
    S.cell(i, 2).value = str(S.cell(i, 2).value) + add
    S.row_dimensions[i].height = max(S.row_dimensions[i].height or 15, 17.25 * (len(str(S.cell(i, 2).value)) // 60 + 1))
last = max(k for k in range(1, S.max_row + 1) if S.cell(k, 1).value)
new = last + 1
for c in 'ABCD':
    S[f'{c}{new}']._style = copy.copy(S[f'{c}{last}']._style)
S[f'A{new}'] = '过去分词的字母变化'
S[f'B{new}'] = (f'写成过去分词词干的 {len(did)} 个词，音变列第一行写【字母变化】链（describere → descriptus → descriptio → description），'
                '下面每一步讲清怎么变、为什么这样变：动词来自拉丁语原形，名词来自过去分词；过去分词怎么构成（-are 动词加 -tus 成了 -atus，b 碰上 t 变成 p，'
                'd 碰上 t 念成 s，v 变回元音 u……）；怎么进入英语。原来讲同一件变化的一句话由步骤取代，别的说明加标签留在后面。'
                f'reduce + tion 这类 -tion 词也照上一轮改成过去分词词干（{"、".join(NEW)}）。逐行见 U 列“过去分词音变：…”。')
S.merge_cells(f'B{new}:C{new}')
S[f'D{new}'] = '=COUNTIF(拆分结果!$U$2:$U$9294,"*过去分词音变：*")'
S.row_dimensions[new].height = 105
b.save(OUT)
print('写好了', OUT)

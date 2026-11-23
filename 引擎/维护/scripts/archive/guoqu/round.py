"""过去分词轮（2026-11）：名词、形容词整个从拉丁语借来、接在过去分词词干上的词（competition、information、decision……），
拆分改成“过去分词词干(=母词) + 后缀”，词根列写清词干怎么来，后缀列改回 -ion / -ive / -or / -ory / -ure 并写明接在过去分词词干后面，
组合列第一行跟着改、下面加“　构词：”一行；英语后来自己用现成的 -ation / -ative 造的词，拆分不改，组合列写明是英语造的。
用法：python3 round.py <源.xlsx> <新.xlsx>    （同目录写 review.txt 供人工看）"""
import sys, re, pickle, os
sys.path.insert(0, os.environ.get('ETY_SCRIPTS', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
import cols as C
from parse import parse_split
from fixlib import Book
from data import L_DATA, U_DATA, SPECIAL

SRC, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
E = pickle.load(open('/tmp/work/ety.pkl', 'rb')) if os.path.exists('/tmp/work/ety.pkl') else {}

PURE = {'ition': 'ion', 'ation': 'ion', 'tion': 'ion', 'sion': 'ion', 'ion': 'ion', 'itive': 'ive', 'ative': 'ive', 'ive': 'ive',
        'itor': 'or', 'ator': 'or', 'or': 'or', 'atory': 'ory', 'ory': 'ory', 'ature': 'ure', 'ure': 'ure'}
LATSUF = {'ion': 'io', 'ive': 'ivus', 'or': 'or', 'ory': 'orius', 'ure': 'ura'}
XS = {'ion': '造“…这件事”的 -io 名词', 'ive': '造“有…性质的”的 -ivus 形容词', 'or': '造“做…的人”的 -or 名词',
      'ory': '造“与…有关的”的 -orius 形容词', 'ure': '造“…的结果、状态”的 -ura 名词'}
STD = {'ion': '-ion：把动作变成名词：“…这件事”或“…的结果”（来自拉丁语名词词尾 -io，经法语进入英语；同 action 行动、invention 发明）',
       'ive': '-ive：“有…性质的、会…的、爱…的”（来自拉丁语形容词词尾 -ivus，经法语 -if / -ive 进入英语；同 active 活跃的、creative 有创造力的）',
       'or': '-or：“做…的人或东西”（来自拉丁语表示“做…的人”的词尾 -or，经古法语进入英语；同 actor 演员、inventor 发明者）',
       'ory': '-ory：形容词词尾，“与…有关的、起…作用的”（来自拉丁语 -orius；同 sensory 感官的）',
       'ure': '-ure：名词词尾，“…这件事、…的结果、状态”（来自拉丁语名词词尾 -ura，经法语进入英语；同 culture 文化、picture 图画）'}
STD_PLACE = '-ory：名词词尾，“做…的地方”（来自拉丁语 -orium；同 dormitory 宿舍：睡觉的地方、observatory 天文台：观测的地方）'
KEEP_RX = re.compile(r'重音|读音|英式|美式|英美')
DROP_RX = re.compile(r'过去分词|词干|这里写成|遇到元音开头|就去掉|y 变|多一个 c|多出一个 c|fication|ization|ai 加|变回|末尾的 -er|-are 结尾|变名词|-ate 型|变成 a|变成 s|变成 i|变成 u|照拉丁语|拉丁语 -are|都配它|几乎都配|一般是|一律是|-ize|-fy\b|-ify|只起连接作用|就是 -ive|就是 -or|-or 多接|同 -ion|it 是|at 是|-at- 加|-it- 加|加 -ation|加 -ition|-ive 是|接在拉丁|合起来读|ve 变')
SUF_SWAP = [(r'-(?:ition|ation|tion|sion)\b', '-ion'), (r'-(?:itive|ative)\b', '-ive'), (r'-(?:itor|ator)\b', '-or'),
            (r'-atory\b', '-ory'), (r'-ature\b', '-ure')]


def lines(v):
    return [l for l in str(v or '').split('\n') if l.strip() and l.strip() not in ('-', '—')]


def cell(xs):
    return '\n'.join(xs) if xs else '-'


def norm_label(t):
    return re.sub(r'（[^（）]*）|\([^()]*\)', '', str(t or '')).strip().strip('-').lower()


def top_split(s, sep='；'):
    out, d, cur = [], 0, ''
    for ch in s:
        if ch in '（(“': d += 1
        elif ch in '）)”': d = max(0, d - 1)
        if ch == sep and d == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    out.append(cur)
    return [x for x in out if x.strip()]


def year_of(w):
    t = ' '.join(e.get('etymology', '') for e in E.get(w.lower(), [])[:1])
    t = t[:220]
    m = re.search(r'(c\. )?\b(\d{4})(s?)\b', t)
    if m:
        return ('约 ' if m.group(1) else '') + m.group(2) + (' 年代' if m.group(3) else ' 年')
    m = re.search(r'(early|mid-|late)?\s*\b(\d{1,2})c\.', t)
    if m:
        return m.group(2) + ' 世纪' + {'early': '初', 'mid-': '中', 'late': '末'}.get(m.group(1) or '', '')
    return ''


def swap_suf(t):
    for a, b in SUF_SWAP:
        t = re.sub(r'(用|是|配|接)\s*' + a, lambda m: m.group(1) + ' ' + b, t)
    return t


b = Book(SRC, tag='过去分词')
ws = b.ws
review, warn, done_L, done_U = [], [], [], []
for r in range(2, ws.max_row + 1):
    w = str(ws.cell(r, C.WORD).value or '')
    if w not in L_DATA and w not in U_DATA:
        continue
    split = str(ws.cell(r, C.SPLIT).value or '')
    J, K, Lw, M = (lines(ws.cell(r, c).value) for c in (C.PRE, C.ROOT, C.WPART, C.SUF))
    combo = str(ws.cell(r, C.COMBO).value or '').split('\n')
    if any(l.strip().startswith('构词：') for l in combo):
        warn.append(f'{w} 已经有构词行，跳过'); continue
    ps = parse_split(split)
    if w in U_DATA:                                      # ---------- 英语后来自己造的：拆分不改
        u = U_DATA[w]
        base = u.get('base') or ps[-2]['surface']
        yr = u.get('year', None)
        yr = year_of(w) if yr is None else yr
        suf = '-' + ps[-1]['surface']
        gl = u.get('gouci') or (f'　构词：{w} 是英语后来自己造的词' + (f'（{yr}）' if yr else '') + f'：{suf} 是从 '
                                f'{"informative" if suf == "-ative" else "information"} 这类拉丁词里借来的现成后缀（at 本来是拉丁语过去分词的标志），'
                                f'英语把它当成一个整体，直接加在 {base} 后面' + (u.get('tail') or ''))
        k = next((i for i, l in enumerate(M) if C.label_of(l) == suf), None)
        if k is None:
            warn.append(f'{w} 找不到后缀行 {suf}')
        elif not re.search(r'现成|当成一个整体|整个当', M[k]):
            M[k] = M[k] + f'；英语后来把整个 {suf} 当成一个现成的后缀，自己造词也直接加它'
        ws.cell(r, C.SUF).value = cell(M)
        combo = combo[:1] + [gl] + combo[1:]
        ws.cell(r, C.COMBO).value = '\n'.join(combo)
        b.note(r, f'{w} 是英语后来用现成的 {suf} 造的，拆分不改；组合列加“构词”一行，后缀列补一句')
        b._fit(r); done_U.append(w)
        review.append(f'##### U {r} {w} | {split}\n  [M] {M[k] if k is not None else "?"}\n  [N] {combo[0]}\n  {gl}')
        continue
    # ---------- 整个从拉丁语借来、接在过去分词词干上的：拆分改成 过去分词词干(=母词) + 后缀
    d = dict(L_DATA[w]); sp = SPECIAL.get(w, {})
    suf_p = ps[-1]; suf_sf = suf_p['surface'].strip().lower(); P = PURE[suf_sf]
    bi, mid, dbl = len(ps) - 2, None, None
    if ps[bi]['surface'].lower() in ('it', 'at'):
        mid = ps[bi]['surface'].lower(); bi -= 1
    if len(re.sub('[^a-z]', '', ps[bi]['surface'].lower())) == 1 and bi > 0:
        dbl = ps[bi]['surface']; bi -= 1
    head = ps[:bi]; basep = ps[bi]
    hs = ''.join(re.sub('[^a-z]', '', p['surface'].lower()) for p in head)
    wl = w.lower()
    assert wl.startswith(hs) and wl.endswith(P), (w, split)
    stem = wl[len(hs):len(wl) - len(P)]
    base_sf = basep['surface'].strip()
    baseform = basep['eqs'][0] if basep['eqs'] else (basep['full'] if basep['full'] != base_sf else base_sf)
    new_split = ' + '.join([p['raw'] for p in head] + [f'{stem}(={baseform})', P])
    lab = (f'-{stem}-' if head else f'{stem}-')
    inf, g, lstem, note, cls = d['inf'], d['g'], d['lstem'], d.get('note', ''), d.get('cls', 'L')
    pp, N = lstem + 'us', d.get('N') or lstem + LATSUF[P]
    # 母词那一行在哪儿
    where = None
    for ci, col in (('L', Lw), ('K', K), ('J', J), ('M', M)):
        for i, l in enumerate(col):
            t = C.label_of(l)
            if t and C.is_part_label(t) and norm_label(t) in (base_sf.lower(), norm_label(basep['raw']), baseform.lower()):
                where = (ci, i); break
        if where: break
    if not where:
        warn.append(f'{w} 找不到母词 / 词根那一行：{base_sf}')
        continue
    oldline = {'L': Lw, 'K': K, 'J': J, 'M': M}[where[0]][where[1]]
    oldbody = oldline.split('：', 1)[1] if '：' in oldline else ''
    is_word = where[0] == 'L'
    first = combo[0]
    m = re.search(re.escape(base_sf) + r'（([^（）]*)）', first)
    bg = m.group(1) if m else re.split(r'[（；]', oldbody)[0]
    same = re.search(r'（同 ([^（）]+)）', oldbody)
    if sp.get('K'):
        newK = lab + '：' + sp['K']
    elif sp.get('Kpre'):
        newK = lab + '：' + sp['Kpre'] + (f'；{baseform}：{oldbody}' if oldbody else '')
    elif is_word:
        newK = f'{lab}：{base_sf}（{bg}）的过去分词词干：拉丁语 {inf}“{g}”→ 过去分词 {pp} → 词干 {lstem}-（见 {base_sf}）' + (f'；{note}' if note else '')
        if same and '同 ' not in note:
            newK += f'（同 {same.group(1)}）'
    else:
        tail = '' if stem == lstem else f'，{stem} 就是 {baseform} 在这个词干里的样子'
        newK = f'{lab}：由词根 {baseform} 变来：拉丁语 {inf}“{g}”→ 过去分词 {pp} → 词干 {lstem}-{tail}' + (f'；{note}' if note else '') + (f'；{baseform}：{oldbody}' if oldbody else '')
    # 各列：去掉母词行、夹在中间的 -it- / -at- 行，新词干行写进词根列
    cols = {'J': J, 'K': K, 'L': Lw, 'M': M}
    del cols[where[0]][where[1]]
    if mid:
        for cn in 'MKJL':
            k = next((i for i, l in enumerate(cols[cn]) if C.label_of(l) == f'-{mid}-'), None)
            if k is not None:
                del cols[cn][k]; break
    moved_K, moved_M = [], []
    keepL = []
    for l in cols['L']:
        t = C.label_of(l) or ''
        if l.startswith('注意：名词跟着拉丁语') or (t.startswith('为什么是') and '被…了' in l):
            continue
        if t.startswith('为什么') and re.search(r'-(ion|ation|ition|ment|ance|ive|ory|or|ure|ible|able)\b', t):
            moved_M.append(swap_suf(l))
        elif t and C.is_part_label(t) and not C.is_note_label(t):
            keepL.append(l)
        else:
            moved_K.append(l)
    if keepL:
        warn.append(f'{w} 单词部分还剩：{keepL}')
    cols['L'] = keepL
    if where[0] == 'K':
        cols['K'].insert(where[1], newK)
    else:
        cols['K'] = [newK] + cols['K']
    cols['K'] += moved_K
    # 后缀列：换成标准的 -ion / -ive……，写明接在过去分词词干后面；读音、英美写法这些说明留着
    k = next((i for i, l in enumerate(cols['M']) if C.label_of(l) == '-' + suf_sf), None)
    std = STD_PLACE if w == 'laboratory' else STD[P]
    att = f'；接在动词的过去分词词干后面，不接在原形上：{stem}- 加 -{P} → {wl}'
    if sp.get('att') is not None:
        att = sp['att']
    if k is None:
        warn.append(f'{w} 找不到后缀行 -{suf_sf}，新写一行')
        cols['M'].append(std + att)
    else:
        keep = [c for c in top_split(cols['M'][k])[1:] if KEEP_RX.search(c) or not DROP_RX.search(c)]
        cols['M'][k] = std + att + ''.join('；' + c.strip() for c in keep)
        cols['M'][k] = cols['M'][k].replace('cancel 加 -ation 英美都多写 cancellation（l 双写；美式偶尔写 cancelation）', '英美都多写 cancellation（美式偶尔写 cancelation）')
    cols['M'] = [l for i, l in enumerate(cols['M']) if not (i != k and (C.label_of(l) or '').startswith('为什么是 -') and '被…了' in l)]
    k = next((i for i, l in enumerate(cols['M']) if l.startswith(std[:6])), k)
    cols['M'] = [cols['M'][i] if i == k else (swap_suf(l) if (C.label_of(l) or '').startswith('为什么') else l) for i, l in enumerate(cols['M'])]
    FIX = {'erosion': ('为什么是 -ion，不是 -ion 或 -ment', None), 'medication': ('；-ation 侧重', '；-ion 侧重')}
    if w in FIX:
        a, b2 = FIX[w]
        cols['M'] = [(l.replace(a, b2) if b2 else '为什么用 -ion 不用 -ment：整个词是从拉丁语 erosio 经法语借来的，后缀早就定了，不配英语的 -ment（rodere 的 d 在过去分词里变成 s，同 corrode → corrosion）') if a in l else l for l in cols['M']]
    cols['M'] += moved_M
    for cn in cols:
        cols[cn] = [('为什么用 -ion 不用 -ment：整个词是从拉丁语 erosio 经法语借来的，后缀早就定了，不配英语的 -ment（rodere 的 d 在过去分词里变成 s，同 corrode → corrosion）'
                     if l.startswith('为什么是 -ion，不是 -ion 或 -ment') else l) for l in cols[cn]]
    # 组合列第一行
    if sp.get('first'):
        new_first, ok = sp['first'], True
    else:
        s, ok = first, True
        if mid:
            s2 = re.sub(r'\s*\+\s*' + mid + r'(（[^（）]*）)?(?=\s*\+)', '', s, count=1); ok &= s2 != s; s = s2
        if dbl:
            s = re.sub(r'\s*\+\s*' + re.escape(dbl) + r'(?=\s*\+)', '', s, count=1)
        s2 = re.sub(r'(】|\+\s*)' + re.escape(base_sf) + r'(?=（)', lambda m_: m_.group(1) + stem, s, count=1); ok &= s2 != s; s = s2
        if suf_sf != P:
            s2 = re.sub(r'(\+\s*)' + re.escape(suf_sf) + r'(?=（)', lambda m_: m_.group(1) + P, s, count=1); ok &= s2 != s; s = s2
        s = s.replace('（-' + suf_sf + '）', '（-' + P + '）').replace('（-' + suf_sf + '、', '（-' + P + '、')
        s = re.sub(r'（也可以看成[^（）]*）', '', s)
        new_first = re.sub(r'）\s+\+', '）+', s)
    if not ok:
        warn.append(f'{w} 第一行没改全：{first}')
    if sp.get('gouci'):
        gl = '　构词：' + sp['gouci']
    elif cls == 'E':
        gl = (f'　构词：{w} 是英语后来照拉丁语的规矩造的：-{P} 不接在动词原形上，而是接在过去分词（“被…了的”形式）后面：'
              f'{inf}（{g}）→ 过去分词 {pp} → 词干 {lstem}- → {wl}')
    else:
        who = f'{w} 不是英语自己用 {base_sf} 加 -{P} 造出来的' if is_word else f'{w} 不是英语自己造的'
        lang = d.get('lang', '拉丁语')
        X = '造“做…的地方”的 -orium 名词' if w == 'laboratory' else XS[P]
        gl = (f'　构词：{who}，而是整个从{lang} {N} 借来的。拉丁语{X}，不接在动词原形上，而是接在过去分词（“被…了的”形式）后面：'
              f'{inf}（{g}）→ 过去分词 {pp} → 词干 {lstem}- → {N}')
    k2 = 1
    while k2 < len(combo) and re.match(r'^\s*[A-Za-z][^：\n]*“[^”]*”\s*\+\s*-', combo[k2]):
        combo[k2] = combo[k2].replace('+ -' + suf_sf + '（', '+ -' + P + '（'); k2 += 1
    combo = [new_first] + combo[1:k2] + [gl] + combo[k2:]
    # 写回
    ws.cell(r, C.SPLIT).value = new_split
    for cn, cc in (('J', C.PRE), ('K', C.ROOT), ('L', C.WPART), ('M', C.SUF)):
        ws.cell(r, cc).value = cell(cols[cn])
    ws.cell(r, C.COMBO).value = '\n'.join(combo)
    b.note(r, f'拆分 {split} → {new_split}（名词、形容词接在拉丁语过去分词词干 {lstem}- 上）；词根列写清 {stem}- 怎么来，'
              f'后缀列改成 -{P}、写明接在过去分词词干后面，组合列加“构词”一行')
    b._fit(r); done_L.append(w)
    review.append(f'##### L {r} {w} | {split} → {new_split}\n  [K] ' + '\n  [K] '.join(cols['K']) +
                  ('\n  [L] ' + '\n  [L] '.join(cols['L']) if cols['L'] else '') + '\n  [M] ' + '\n  [M] '.join(cols['M']) +
                  f'\n  [N] {new_first}\n  {gl}')

miss = [x for x in list(L_DATA) + list(U_DATA) if x not in done_L + done_U]
print('改拆分（过去分词词干）', len(done_L), '；英语自己造、拆分不改', len(done_U), '；没找到的', miss)
print('\n'.join('!! ' + x for x in warn))
open(os.path.join(HERE, 'review.txt'), 'w', encoding='utf-8').write('\n'.join(review))

# ---------- 「整表核对记录」
b.fixed_other('过去分词词干',
              '拆分写成 compete + ition、inform + ation、decide + ion 这类，看不出这些名词、形容词是接在拉丁语过去分词词干上的'
              '（用户提出：competition 为什么不是 compete 直接加 -ion，要在拆分和后面几列讲清楚）',
              f'{len(done_L)} 行拆分改成“过去分词词干(=母词) + 后缀”：competit(=compete) + ion、informat(=inform) + ion、decis(=decide) + ion、'
              'explanat(=explain) + ory、temperat(=temper) + ure……；原来单独拆出 it、at 的 6 行（expedition、laboratory 等）也并进词干。'
              '词根列写清词干怎么来（拉丁语原形 → 过去分词 → 词干），后缀列改回 -ion / -ive / -or / -ory / -ure 并写明接在过去分词词干后面，'
              '组合列第一行跟着改，下面加一行“　构词：…”。逐行见 U 列“过去分词：…”')
b.fixed_other('英语自己造的 -ation 词',
              '-ation、-ative 结尾的词里，有的是英语（或法语）后来自己造的，不是从拉丁语整个借来的（transportation、globalization、talkative）',
              f'{len(done_U)} 行拆分不改（transport + ation：-ation 整个当成一个现成的后缀用），组合列加“构词”一行写明是英语造的，后缀列补一句')
b.special(None, '不改的：escalator（拼缀词，-ator 取自 elevator）；hesitate、visit 的 -it- 是表示“反复”的成分，不是过去分词；'
                '-ate 动词加 -ion（create + ion）本来就接在过去分词上（create 就是 creatus 变来的）；词根本身就写成过去分词词干的'
                '（posit + ion、edit + ion、curat + or）；reduce + tion、produce + tion 这类 -tion 里的 t 也是过去分词带来的，这一轮没改',
          '照旧；以后要统一时照本轮写法改')
b.special(None, 'sensitive、sensation、constellation、literature、miniature 不是规则的“动词原形 → 过去分词”：sensitivus 照 positivus 多加了 it；'
                'sensatus、stellatus、litteratus 是名词加 -atus 造的形容词；miniature 从意大利语来',
          '照实写进词根列和“构词”那一行')

# ---------- 「说明」
S = b.wb['说明']
def row_of(a):
    return next(i for i in range(1, S.max_row + 1) if S.cell(i, 1).value == a)
add = {'I 拆分': '；名词、形容词整个从拉丁语借来、接在过去分词词干上的，拆分写词干，括号里写母词：competit(=compete) + ion、informat(=inform) + ion、decis(=decide) + ion',
       '拆分': '名词、形容词整个从拉丁语借来、接在过去分词词干上的，拆分写“过去分词词干(=母词) + 后缀”：competit(=compete) + ion（不写 compete + ition）、'
               'informat(=inform) + ion、decis(=decide) + ion；英语后来自己用现成的 -ation 造的词照旧写 transport + ation。',
       '后缀行': '接在过去分词词干后面的 -ion、-ive、-or、-ory、-ure，这一行写明“接在动词的过去分词词干后面，不接在原形上：competit- 加 -ion → competition”；'
               '词干怎么来写在词根列（拉丁语原形 → 过去分词 → 词干）。',
       '组合 → 现在的含义': '名词、形容词接在拉丁语过去分词词干上的，第一行下面写一行“\u3000构词：competition 不是英语自己用 compete 加 -ion 造出来的，'
                     '而是整个从拉丁语 competitio 借来的。拉丁语造“…这件事”的 -io 名词，不接在动词原形上，而是接在过去分词（“被…了的”形式）后面：'
                     'competere（一起争取）→ 过去分词 competitus → 词干 competit- → competitio”；英语后来自己用 -ation 造的词，写明是英语造的、-ation 整个当后缀用。'}
for a, t in add.items():
    i = row_of(a)
    v = str(S.cell(i, 2).value)
    if t not in v:
        S.cell(i, 2).value = v + ('' if t.startswith('；') else '') + t
import copy
last = max(i for i in range(1, S.max_row + 1) if S.cell(i, 1).value)
new = last + 1
for c in 'ABCD':
    S[f'{c}{new}']._style = copy.copy(S[f'{c}{last}']._style)
S[f'A{new}'] = '过去分词词干'
S[f'B{new}'] = (f'名词、形容词整个从拉丁语借来、接在过去分词词干上的 {len(done_L)} 个词（competition、information、decision、description……），'
                '拆分改成“过去分词词干(=母词) + 后缀”：competit(=compete) + ion、informat(=inform) + ion、decis(=decide) + ion'
                '（原来写 compete + ition、inform + ation、decide + ion）；词根列写清词干怎么来（competere“一起争取”→ 过去分词 competitus → 词干 competit-），'
                '后缀列改回 -ion、-ive、-or、-ory、-ure 并写明接在过去分词词干后面，组合列第一行下面加一行“构词”。'
                f'英语后来自己用现成的 -ation、-ative 造的 {len(done_U)} 个词（transportation、globalization、talkative……）拆分不改，组合列写明是英语造的。'
                '逐行见 U 列“过去分词：…”。')
S.merge_cells(f'B{new}:C{new}')
S[f'D{new}'] = '=COUNTIF(拆分结果!$U$2:$U$9294,"*过去分词：*")'
S.row_dimensions[new].height = 105
for a in ('I 拆分', '拆分', '后缀行', '组合 → 现在的含义'):
    i = row_of(a)
    S.row_dimensions[i].height = max(S.row_dimensions[i].height or 15, 17.25 * (len(str(S.cell(i, 2).value)) // 60 + 1))
b.save(OUT)
print('写好了', OUT)

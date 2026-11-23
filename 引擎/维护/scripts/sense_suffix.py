"""本轮：后缀行补“来源（母词）+ 作用 + 在这里的作用”；跨组同源恢复“见 X”；前缀 re- / un- / dis- 补来源。"""
import re, pickle, collections, sys
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import meaning as M
import os
from openpyxl import load_workbook as _lw
_SRC = os.environ.get('ETY_SRC')          # sense_write.py 会先设好：要处理的总表
if _SRC:
    import cols as _C
    T = [_C.legacy(r) for r in _lw(_SRC, read_only=True)['拆分结果'].iter_rows(min_row=2, values_only=True)]   # 前缀、词根、单词部分、后缀合成一格，列号照旧
else:
    T = pickle.load(open('/home/claude/T2.pkl', 'rb'))
FIRST, GRP = {}, {}
for i, x in enumerate(T, start=2):
    FIRST.setdefault(str(x[4]).lower(), i); GRP[i] = x[2]
LAB = re.compile(r'^\s*([^：]{1,40})：')
EN = "英语本来就有"

# ---------------- 后缀：来源（母词） ----------------
O = {
 '-er@agent': f'{EN}的后缀，古英语写作 -ere',
 '-r@agent': f'就是 -er：{EN}的后缀，古英语写作 -ere',
 '-er@comp': f'{EN}的比较级词尾，古英语写作 -ra / -or',
 '-or': '来自拉丁语表示“做…的人”的词尾 -or，经古法语进入英语',
 '-ator': '来自拉丁语 -ator：动词词尾 -at- 加上表示“做…的人”的 -or',
 '-ist': '来自希腊语 -istēs，经拉丁语 -ista、法语 -iste 进入英语',
 '-ian': '来自拉丁语形容词词尾 -ianus“属于…的”',
 '-an': '来自拉丁语形容词词尾 -anus“属于…的”',
 '-ee': '来自法律法语里“被…了的”形式的词尾 -é，所以多指“被…的人”',
 '-ion': '来自拉丁语名词词尾 -io，经法语进入英语',
 '-tion': '来自拉丁语名词词尾 -tio，经法语 -tion 进入英语',
 '-sion': '来自拉丁语名词词尾 -sio，经法语进入英语',
 '-ation': '来自拉丁语 -atio：动词词干里的 -at- 加上名词词尾 -io',
 '-ition': '来自拉丁语 -itio：动词词干里的 -it- 加上名词词尾 -io',
 '-ment': '来自拉丁语名词词尾 -mentum，经法语进入英语',
 '-ness': f'{EN}的后缀，古英语写作 -nes',
 '-ity': '来自拉丁语 -itas，经法语 -ité 进入英语',
 '-ty@ity': '来自拉丁语 -tas，经法语 -té 进入英语',
 '-ty@tens': f'{EN}，古英语写作 -tig“几个十”，和 ten 同源',
 '-ety': '就是 -ity：来自拉丁语 -itas',
 '-al@adj': '来自拉丁语形容词词尾 -alis',
 '-al@noun': '来自拉丁语 -alis 的名词用法，经法语 -aille 进入英语',
 '-ial': '就是 -al：来自拉丁语形容词词尾 -alis',
 '-ual': '就是 -al：来自拉丁语形容词词尾 -alis',
 '-ical': '-ic 加 -al：-ic 来自拉丁语 -icus、希腊语 -ikos，-al 来自拉丁语 -alis',
 '-ic': '来自拉丁语 -icus、希腊语 -ikos，经法语 -ique 进入英语',
 '-tic': '就是 -ic：来自希腊语 -ikos、拉丁语 -icus',
 '-atic': '就是 -ic：来自希腊语 -ikos、拉丁语 -icus',
 '-ics': '来自希腊语 -ika（形容词词尾 -ikos 的复数）',
 '-ive': '来自拉丁语形容词词尾 -ivus，经法语 -if / -ive 进入英语',
 '-ative': '就是 -ive：来自拉丁语形容词词尾 -ivus',
 '-itive': '就是 -ive：来自拉丁语形容词词尾 -ivus',
 '-able': '来自拉丁语 -abilis，经法语进入英语；和单词 able 不是一个来源，只是长得像、意思也近',
 '-ible': '来自拉丁语 -ibilis（-abilis 的另一种样子）',
 '-ous': '来自拉丁语 -osus“充满…的”，经法语进入英语',
 '-ious': '就是 -ous：来自拉丁语 -osus“充满…的”',
 '-y@adj': f'{EN}的后缀，古英语写作 -ig',
 '-y@noun': '来自拉丁语、希腊语的名词词尾 -ia，经法语 -ie 进入英语',
 '-ing@noun': f'{EN}，古英语写作 -ung / -ing，专门把动作变成名词',
 '-ing@adj': f'{EN}：古英语“正在…的”写作 -ende，中古英语时和名词词尾 -ing 并成了一个',
 '-ing@both': f'{EN}：名词用法来自古英语 -ung / -ing，“正在…的”来自古英语 -ende，中古英语时并成了一个',
 '-ed@pp': f'{EN}，古英语写作 -ed / -od；和拉丁语“被…了的”词尾 -tus 同源',
 '-ed@adj': f'{EN}，古英语写作 -ede，加在名词后面表示“长着…的、带有…的”',
 '-d@pp': f'就是 -ed：{EN}，古英语写作 -ed / -od',
 '-d@adj': f'就是 -ed：{EN}，古英语写作 -ede',
 '-en@pp': f'{EN}，古英语“被…了的”形式的词尾 -en',
 '-n@pp': f'就是 -en：{EN}，古英语“被…了的”形式的词尾',
 '-en@verb': f'{EN}，古英语写作 -nian，加在形容词、名词后面造动词',
 '-ize': '来自希腊语动词词尾 -izein，经拉丁语 -izare、法语 -iser 进入英语',
 '-ise': '就是 -ize：来自希腊语动词词尾 -izein，经法语 -iser 进入英语',
 '-ism': '来自希腊语 -ismos，经拉丁语 -ismus 进入英语',
 '-ate@verb': '来自拉丁语“被…了的”形式的词尾 -atus，英语借拉丁动词时常拿它当动词用',
 '-ate@adj': '来自拉丁语“被…了的”形式的词尾 -atus',
 '-ure': '来自拉丁语名词词尾 -ura，经法语进入英语',
 '-ary': '来自拉丁语 -arius / -arium',
 '-iary': '就是 -ary：来自拉丁语 -arius',
 '-ory': '来自拉丁语 -orius / -orium',
 '-ant': '来自拉丁语“正在…的”形式的词尾 -ans（-antem）',
 '-ent': '来自拉丁语“正在…的”形式的词尾 -ens（-entem）',
 '-ient': '就是 -ent：来自拉丁语“正在…的”形式的词尾 -ens',
 '-ance': '来自拉丁语 -antia（由“正在…的”形式 -ans 变成名词），经法语 -ance 进入英语',
 '-ence': '来自拉丁语 -entia（由“正在…的”形式 -ens 变成名词），经法语进入英语',
 '-ce': '这里是 -ance / -ence 的一部分：来自拉丁语 -antia / -entia',
 '-cy': '来自拉丁语 -cia / -tia，经法语进入英语',
 '-ency': '来自拉丁语 -entia',
 '-ancy': '来自拉丁语 -antia',
 '-age': '来自法语 -age，再往上是拉丁语 -aticum',
 '-ery': '来自法语 -erie',
 '-ry': '就是 -ery：来自法语 -erie',
 '-ess': '来自法语 -esse，再往上是希腊语 -issa',
 '-ish@adj': f'{EN}的后缀，古英语写作 -isc',
 '-th@noun': f'{EN}，古英语写作 -þu / -þ',
 '-th@ord': f'{EN}，古英语写作 -oþa / -þa',
 '-le@freq': f'{EN}，古英语写作 -lian，表示“一下接一下地做”',
 '-le@dim': f'{EN}，古英语写作 -el，表示“小”',
 '-et': '来自古法语表示“小”的词尾 -et',
 '-ette': '来自法语表示“小”的词尾 -ette',
 '-let': '来自古法语表示“小”的词尾 -elet',
 '-dom': f'{EN}，古英语 dom“判决、状态”（今天的 doom）',
 '-some': f'{EN}，古英语写作 -sum',
 '-s@pl': f'{EN}，古英语的复数词尾 -as',
 '-es@pl': f'{EN}，古英语的复数词尾 -as',
 '-s@adv': f'{EN}，古英语表示“…的”的词尾 -es，拿来造副词',
 '-est': f'{EN}，古英语最高级词尾 -est / -ost',
 '-st': f'就是 -est：{EN}，古英语最高级词尾 -est',
 '-ar': '来自拉丁语形容词词尾 -aris（就是 -alis，前面有 l 时写成 -aris）',
 '-ese': '来自拉丁语 -ensis，经古法语 -eis 进入英语',
 '-ling': f'{EN}，古英语写作 -ling',
 '-ster': f'{EN}，古英语写作 -estre',
 '-logy': '来自希腊语 -logia，出自 logos“话、道理”',
 '-ology': '来自希腊语 -logia，出自 logos“话、道理”',
 '-ine': '来自拉丁语 -inus',
 '-ia': '来自拉丁语、希腊语名词词尾 -ia',
 '-ward': f'{EN}，古英语写作 -weard“朝着…的”',
 '-wards': f'{EN}，古英语 -weard“朝着…的”，加 -s 当副词',
 '-ly@adv': '来自古英语 lic“身体、样子”：带着…的样子 → 以…的方式；和 like 是一家，见 like',
 '-ly@adj': '来自古英语 lic“身体、样子”，和 like 是一家，见 like',
 '-ally': '-al 加 -ly：-ly 来自古英语 lic“身体、样子”（见 like）',
 '-ful': '就是 full“满的”变来的，见 full',
 '-less': '来自古英语 leas“没有…的”，和 loose“松开的”是一家，见 loose',
 '-like': '就是 like“像”，见 like',
 '-t': f'就是 -th：{EN}的名词词尾，古英语写作 -þ',
}
# 只有一个“意思”的行要在前面补作用（意思是引号开头、没写加在哪儿）
LEAD = {
 '-er@agent': '一般加在动词后面，表示', '-r@agent': '加在动词后面，表示', '-or': '一般加在动词后面，表示',
 '-ist': '一般加在名词后面，表示', '-ee': '加在动词后面，表示', '-ian': '表示', '-an': '表示',
 '-able': '一般加在动词后面，变成形容词：', '-ible': '变成形容词：', '-ive': '一般加在动词后面，变成形容词：',
 '-ative': '变成形容词：', '-itive': '变成形容词：', '-ed@pp': '加在动词后面，变成形容词：', '-ed@adj': '加在名词后面，变成形容词：',
 '-d@pp': '加在动词后面，变成形容词：', '-d@adj': '加在名词后面，变成形容词：', '-ful': '加在名词后面，变成形容词：',
 '-less': '加在名词后面，变成形容词：', '-ous': '加在名词后面，变成形容词：', '-ious': '变成形容词：',
 '-y@adj': '加在名词后面，变成形容词：', '-ment': '加在动词后面，变成名词：', '-ance': '变成名词：', '-ence': '变成名词：',
 '-ant': '变成形容词（有时是名词）：', '-ent': '变成形容词（有时是名词）：', '-ient': '变成形容词：', '-ism': '变成名词：',
 '-ity': '加在形容词后面，变成名词：', '-ary': '变成形容词或名词：', '-ion': '加在动词后面，变成名词：',
 '-ness': '加在形容词后面，变成名词：', '-ing@noun': '加在动词后面，变成名词：', '-ing@adj': '加在动词后面，变成形容词：',
}

def sense(lab, line):
    body = line.split('：', 1)[1] if '：' in line else line
    head = re.split(r'[（；]', body)[0]
    if lab in ('-er', '-r'):
        if '比较级' in body: return 'comp'
        if '反复' in head: return 'freq'
        return 'agent'
    if lab == '-y': return 'noun' if ('名词词尾' in head or re.search(r'-ia|-ie\b', body)) else 'adj'
    if lab == '-ing':
        n = bool(re.search(r'变名词|名词：|这件事', head)); a = bool(re.search(r'正在|形容词|令人|让人', head))
        return 'both' if n and a else ('adj' if a else 'noun')
    if lab in ('-ed', '-d'):
        return 'adj' if re.search(r'接在名词后|加在名词后|长着|带有|有着|带…的|有…的', head) else 'pp'
    if lab in ('-en', '-n'): return 'verb' if re.search(r'使', head) and not re.search(r'被…了|已经…了', head) else 'pp'
    if lab == '-al': return 'noun' if '名词词尾' in head else 'adj'
    if lab == '-ate': return 'adj' if '形容词' in head else 'verb'
    if lab == '-ish': return 'verb' if '动词' in body and '法语' in body else 'adj'
    if lab == '-th': return 'ord' if re.search(r'第', head) else 'noun'
    if lab == '-le': return 'freq' if re.search(r'反复|动词|一下', head) else ('dim' if '小' in head else '')
    if lab in ('-s', '-es'):
        if '副词' in head: return 'adv'
        if '复数' in head: return 'pl'
        return ''
    if lab == '-ty': return 'tens' if '十' in head else 'ity'
    if lab == '-ly': return 'adv' if '副词' in head and '不是副词' not in head else 'adj'
    return ''

def keyed(d, lab, s):
    return d.get(f'{lab}@{s}') if s else d.get(lab)

HAS_ORIGIN = re.compile(r'(拉丁语|古英语|希腊语|法语|古诺斯语|古诺尔斯语|意大利语|中古英语|日耳曼语)[^，；。]{0,16}-[a-z]|英语本族|本族的|本族后缀|本族词尾|英语本来就有|来自 full|就是 full|leas|like“像|-lic|-lice|\blic\b|facere|logos|-weard|-scipe|\bhad\b')
FUNC = re.compile(r'加在|接在|把|变成|词尾|后缀|构成|造')
ROLE_DONE = re.compile(r'在这里|这里(是|指|表示|多指|当|既|不是|取|大概|也许|只是|就是|还指|也指|说|接|来自|用|让|把|成了)|在 [A-Za-z\-]+ 里')

def top_cut(s, start):
    q = p = 0
    for k in range(start, len(s)):
        ch = s[k]
        if ch == '“': q += 1
        elif ch == '”': q = max(0, q - 1)
        elif ch == '（': p += 1
        elif ch == '）': p = max(0, p - 1)
        elif ch in '；。' and q == 0 and p == 0: return k
    return len(s)

# ---------------- 在这里：从【构词逻辑】第一行取 ----------------
TERM = re.compile(r'^\s*(.*?)\s*（([^（）]*)）\s*$')
def parse_logic(first):
    s = re.sub(r'^【构词逻辑】', '', str(first or '')).strip()
    if s.startswith('派生路线：'):
        items = []
        for it in s[5:].split('→'):
            m = TERM.match(it.strip())
            items.append((m.group(1).strip(), m.group(2).strip()) if m else (it.strip(), ''))
        return ('route', items, '')
    if '=' not in s: return None
    left, right = s.split('=', 1)
    terms = []
    for t in left.split('+'):
        m = TERM.match(t.strip())
        terms.append((m.group(1).strip(), m.group(2).strip()) if m else (t.strip(), ''))
    r = right.strip()
    cut = top_cut(r, 0)
    lit = r[:cut].strip()
    m = re.fullmatch(r'“([^“”]*)”', lit)
    if m: lit = m.group(1).strip()
    elif not lit.startswith('“'): lit = re.split(r'[，（]', lit)[0].strip()
    return ('eq', terms, lit)

def norm(t): return re.sub(r'\([^)]*\)|（[^（）]*）', '', t).strip().strip('-').lower()

def stem_gloss(i, stem):
    for l in str(T[i - 2][9] or '').split('\n'):
        m = LAB.match(l)
        if m and norm(m.group(1)) == norm(stem):
            g = l.split('：', 1)[1]
            g = re.split(r'[（；，。]', g)[0].strip().strip('“”')
            if g and len(g) <= 14 and not re.search(r'[“”（）()=]', g): return g
    return ''

POS = {'v.': '动词', 'vt.': '动词', 'vi.': '动词', 'n.': '名词', 'adj.': '形容词', 'adv.': '副词', 'prep.': '介词', 'conj.': '连词'}
def now_sense(i):
    for l in ['【今义】' + M.to_old(T[i - 2][5], T[i - 2][6])]:   # 今义 2026-11 起写在 F 列「含义」（一行一个意思、行首写词性），还原成老写法再读
        if l.startswith('【今义】'):
            t = l[4:].strip(); pos = ''
            while True:
                m = re.match(r'^[（(]([^（）()]*)[）)]\s*', t)
                if not m: break
                for tag in re.split(r'[，,、/\s]+', m.group(1)):
                    pos = pos or POS.get(tag.lower(), '')
                t = t[m.end():]
            first = re.split(r'[；（(]', t)[0].strip().rstrip('，、。')
            if first and len(first) <= 16 and not re.search(r'[A-Za-z]', first): return pos, first
            return None
    return None

def here_sentence(i, lab, word):
    x = T[i - 2]
    first = str(x[10] or '').split('\n')[0]
    pl = parse_logic(first)
    c = norm(lab)
    if not pl: return None
    kind, items, lit = pl
    if kind == 'eq':
        idx = [k for k, (t, g) in enumerate(items) if norm(t) == c]
        if not idx: return None
        k = idx[-1]
        if k == 0 or not lit: return None
        stem, g = items[k - 1]
        if not re.fullmatch(r"[A-Za-z][A-Za-z'\-]*(?:\([a-z]+\))?", stem.strip()): return None
        if not g or re.search(r'[“”（）()]', g): g = stem_gloss(i, stem)
        if g and re.search(r'[“”（）()]', g): g = ''
        st = norm(stem)
        stem = re.sub(r'\(([a-z]+)\)', r'\1', stem.strip())
        if not re.fullmatch(r"[a-z'\-]+", st): return None
        gl = f'{stem}“{g}”' if g else stem
        if len(items) == 2:
            ns = now_sense(i) if st in FIRST else None
            if ns:
                return f'在这里：{gl}加上 -{c}，成了{ns[0]} {word}“{ns[1]}”'
            return f'在这里：{gl}加上 -{c}，合起来就是“{lit}”' if '“' not in lit else f'在这里：{gl}加上 -{c}，合起来就是：{lit}'
        if not g or len(st) < 3 or '“' in lit: return None
        return f'在这里：接在 {gl}后面；合起来，{word} 就是“{lit}”'
    # 派生路线：找加上这个后缀的那一步
    for k in range(1, len(items)):
        w_prev, g_prev = items[k - 1]; w_now, g_now = items[k]
        if norm(w_now).endswith(c) and len(norm(w_now)) > len(norm(w_prev)) and g_now and not re.search(r'[“”（）()]', g_now):
            if not re.fullmatch(r"[A-Za-z][A-Za-z'\-]*", w_prev.strip()) or not re.fullmatch(r"[A-Za-z][A-Za-z'\-]*", w_now.strip()): return None
            if not g_prev or re.search(r'[“”（）()]', g_prev): g_prev = stem_gloss(i, w_prev)
            if g_prev and re.search(r'[“”（）()]', g_prev): g_prev = ''
            gl = f'{w_prev}“{g_prev}”' if g_prev else w_prev
            return f'在这里：{gl}加上 -{c}，成了 {w_now}“{g_now}”'
    return None

def upgrade_line(i, lab, line, word):
    s = sense(lab, line)
    o = keyed(O, lab, s)
    lead = keyed(LEAD, lab, s)
    st = line.index('：') + 1
    body = line[st:]
    out = line; did = []
    # 1) 作用：意思只是一个引号里的说法时，前面补上加在哪儿、变成什么
    if lead and body.startswith('“') and not FUNC.search(body[:top_cut(body, 0)]):
        out = line[:st] + lead + body; did.append('作用')
    # 2) 来源
    if o and not HAS_ORIGIN.search(out[st:]):
        cut = top_cut(out, st); seg = out[:cut]
        mm = re.search(r'”(?=：)', out[st:cut])
        if mm and not seg.endswith('）'):
            cut = st + mm.end(); seg = out[:cut]
        if seg.endswith('）'):
            j = seg.rfind('（')
            out = seg[:j] + '（' + o + '；' + seg[j + 1:-1] + '）' + out[cut:]
        else:
            out = seg + '（' + o + '）' + out[cut:]
        did.append('来源')
    # 3) 在这里
    if not ROLE_DONE.search(out[st:]):
        h = here_sentence(i, lab, word)
        if h:
            cut = top_cut(out, st)
            out = out[:cut] + '；' + h + out[cut:]
            did.append('在这里')
    return (out, did) if out != line else (None, did)

# ---------------- 前缀：re- / un- / dis- 等补来源（只补没写来源的） ----------------
PO = {
 're-': '拉丁语前缀 re-，本义“往回”，往回再来一次就是“再”；只用在词前，不单独成词',
 'un-@neg': f'{EN}，古英语 un-；和拉丁语表示“不”的 in-、希腊语 a- 同源',
 'un-@rev': f'{EN}，古英语 un- / on-“反过来”，和表示“不”的 un- 来源不同',
 'dis-': '拉丁语前缀 dis-，本义“一分为二、向两边”，和 duo“二”有关',
 'di-@dis': '就是拉丁语前缀 dis-“一分为二、向两边”',
 'di(s)-': '拉丁语前缀 dis-，本义“一分为二、向两边”',
 'des-': '古法语 des-，就是拉丁语前缀 dis-“一分为二、向两边”',
}
P_HAS = re.compile(r'拉丁语|古英语|希腊语|法语|英语本族|本族|英语本来就有|古北欧语|古诺斯语')
def upgrade_prefix(i, lab, line):
    if not P_HAS.search(line.split('：', 1)[1]):
        s = ''
        if lab == 'un-': s = 'rev' if re.search(r'反过来|解开|撤销', line.split('：', 1)[1][:30]) else 'neg'
        if lab == 'di-': s = 'two' if '二' in line else 'dis'
        o = keyed(PO, lab, s)
        if not o: return None
        st = line.index('：') + 1
        cut = top_cut(line, st); seg = line[:cut]
        if seg.endswith('）'):
            j = seg.rfind('（'); return seg[:j] + '（' + o + '；' + seg[j + 1:-1] + '）' + line[cut:]
        return seg + '（' + o + '）' + line[cut:]
    return None

# ---------------- 跨组同源：恢复对记词有帮助的“见 X” ----------------
COG_RESTORE = [  # (行, 行首, 现在的片段, 恢复后的片段)
 (5838, 'noct：', '（和英语 night 同源）', '（和英语 night 同源，见 night）'),
 (5953, 'ed：', '同一个印欧语词根 *ed-）', '同一个印欧语词根 *ed-，见 eat 的【背景】）'),
 (5962, 'semin：', '同一个祖语词根“播种”）', '同一个祖语词根“播种”，见 seed 的【背景】）'),
 (6331, 'Novem：', '和英语 nine 同源）', '和英语 nine 同源，见 nine）'),
 (266, 'un：', '和英语 one 是远亲）', '和英语 one 是远亲，见 one）'),
 (4265, 'aster：', '和 star 同源）', '和 star 同源，见 star）'),
 (4273, 'stell：', '同源）', '同源，见 star）'),
 (4259, 'star：', '同出一个印欧语词根 *ster-“星”', '同出一个印欧语词根 *ster-“星”（见 disaster、constellation）'),
 (4641, 'ali：', '和英语本族的 else 同源）', '和英语本族的 else 同源，见 else）'),
 (4646, 'al：', '见 alien', '见 else、alien'),
 (3598, 'for：', '（和 door 是远亲）', '（和 door 是远亲，见 door）'),
 (3611, 'forum：', '（和 door 是远亲）', '（和 door 是远亲，见 door）'),
 (3655, 'neur：', '（和 nerve 是亲戚）', '（和 nerve 是亲戚，见 nerve）'),
 (3650, 'nerve：', '（希腊语 neuron 是亲戚）', '（希腊语 neuron 是亲戚，见 neural）'),
 (1752, 'opt：', '同出 *okw-“看”）', '同出 *okw-“看”，见 eye 的【背景】）'),
 (3135, 'is：', '（和拉丁语 aqua 水同源）', '（和拉丁语 aqua 水同源，见 aquatic）'),
 (6409, 'ton：', '和 thunder 同源）', '和 thunder 同源，见 thunder）'),
 (5001, 'super：', '和英语 over 是远亲）', '和英语 over 是远亲，见 over）'),
 (628, 'word：', '和拉丁语 verbum 同源', '和拉丁语 verbum 同源（见 verb）'),
 (632, 'verb：', '和英语的 word 同源', '和英语的 word 同源（见 word）'),
 (6299, 'sauce：', '和 salt 同出一源', '和 salt 同出一源（见 salt）'),
 (6900, 'sake：', '*sag-“追查、搜寻”', '*sag-“追查、搜寻”（见 seek）'),
 (9168, 'spike：', 'spire（尖顶）', 'spire（尖顶，见 spire）'),
 (9170, 'spire：', '和 spike（长钉）是一家', '和 spike（长钉）是一家（见 spike）'),
 (3020, 'heavy：', '（和 have 同一个）', '（和 have 同一个，见 have 的【背景】）'),
 (8792, 'ultra-：', '（拉丁语 ultra，和 ultimate 同源）', '（拉丁语 ultra，和 ultimate 同源，见 ultimate）'),
]
IN_DIR = ('拉丁语 in“在…里、在…上、进入”，和英语 in 同源', '拉丁语 in“在…里、进入”，和英语 in 同源')

def run():
    H = {i: str(x[9] or '').split('\n') for i, x in enumerate(T, start=2)}
    recs = []
    for i, x in enumerate(T, start=2):
        w = str(x[4])
        for k, l in enumerate(H[i]):
            m = LAB.match(l)
            if not m: continue
            lab = m.group(1).strip()
            if ' ' in lab: continue
            new = None; did = []
            if lab.startswith('-') and not lab.endswith('-'):
                new, did = upgrade_line(i, lab, l, w)
                cat = '后缀：' + '、'.join(did) if new else None
            elif lab.endswith('-') and lab in ('re-', 'un-', 'dis-', 'di-', 'di(s)-', 'des-'):
                new = upgrade_prefix(i, lab, l); cat = '前缀：补来源'
            cur = new or l
            if lab in ('-ly', '-like', '-ally') and 'like' in cur and not re.search(r'见 like(?![A-Za-z])', cur):
                n3 = re.sub(r'(和 like (?:同源|是一家)|和 like 是同一个[^，；。）]*)(）)', r'\1，见 like\2', cur, count=1)
                if n3 == cur: n3 = re.sub(r'(和 like (?:同源|是一家))', r'\1（见 like）', cur, count=1)
                if n3 != cur:
                    new = n3; cat = (cat + '、见 like') if (cat and cat.startswith('后缀')) else '后缀：补“见 like”'
            if new:
                for a in IN_DIR: new = new.replace(a + '）', a + '，见 in）').replace(a + '；', a + '，见 in；')
                H[i][k] = new; recs.append((cat, i, w, lab, l, new))
            elif any(a in l for a in IN_DIR) and '见 in' not in l:
                n2 = l
                for a in IN_DIR: n2 = n2.replace(a + '）', a + '，见 in）').replace(a + '；', a + '，见 in；')
                if n2 != l: H[i][k] = n2; recs.append(('前缀：in- 补“见 in”', i, w, lab, l, n2))
    for r, pre, a, b in COG_RESTORE:
        L = H[r]; hit = [k for k, l in enumerate(L) if l.startswith(pre) and a in l and b not in l]
        if not hit: continue          # 只对当初那几行有用；别的表里没有就跳过
        k = hit[0]; old = L[k]; L[k] = old.replace(a, b, 1)
        recs.append(('同源：恢复“见”', r, str(T[r - 2][4]), pre.rstrip('：'), old, L[k]))
    return H, recs

if __name__ == '__main__':
    H, recs = run()
    pickle.dump((H, recs), open('/home/claude/suffix_changes.pkl', 'wb'))
    c = collections.Counter(r[0] for r in recs)
    print(len(recs), 'rows', len({r[1] for r in recs})); print(c.most_common())

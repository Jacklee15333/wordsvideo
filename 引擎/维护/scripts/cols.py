"""「拆分结果」的列（2026-11 单词列轮起 22 列）和「前缀 / 词根 / 单词部分 / 后缀」四列的读写。

列：A 批次、B 序号、C 组号、D 小类号、E 单词、F 含义、G 例句、H 类型、I 拆分、J 前缀、K 词根、L 单词部分、M 后缀、
    N 组合 → 现在的含义、O 新·背景、P 音变 / 字母变化、Q 核对结果、R 核对依据、S 来源链接、T 原表备注、U 本次调整、V 词根变体处理。
以前的「各部分解释」一格（好几行“标签：解释”）分成了四列：
  - 前缀列（J）：标签以 - 结尾的行（re-、un-、mono-）；
  - 词根列（K）：不能单独用的词根，在接别的部分的那一边加“-”（bio-、-ped-、-logue；外语里的成分 tsu-、-nami 也算），
    两个部分中间的连接成分、双写的字母（significant 的 -i-、spokesman 的 -s-、dubbing 的 -b-）；
  - 单词部分（L，2026-11 用户定下）：能单独用的英语单词，不加连字符——基础词本身（make）、母词（maker、rematch 的 make、match）、
    合成词里的各个词（make-up 的 make、up）、专有名词（Hamburg）、缩写字母代表的词（VIP 的 V）；复数、过去式这些形式（hands、days、behaved）也算；
  - 后缀列（M）：标签以 - 开头的行（-ion、-er、-logy），以及中间的成分（-it-、-at-）；
  - “为什么用 -ar 不用 -al”跟着它讲的那个前缀 / 后缀；讲整个词来历、拼写的说明跟着主体走：有词根（连接成分不算）的放词根列，没有的放单词部分；
    基础词（⑤）、不好拆分（④）的解释整格放单词部分；
  - 一列里没有内容写“-”。
读表的老脚本按 19 列、一格「各部分解释」写的：用 legacy(row) 把一行转成老的样子（四列合成一格，词根标签的连字符去掉），列号照旧。
写表的脚本用下面的列号常量，各部分解释用 get_parts / set_parts 读写（set_parts 先照每一行原来在哪一列放，新写的行按上面的规矩放）。
"""
import re
from parse import parse_split
import linetools as LT

HEAD = ['批次', '序号', '组号', '小类号', '单词', '含义', '例句', '类型', '拆分', '前缀', '词根', '单词部分', '后缀', '组合 → 现在的含义',
        '新·背景（只写在词族第一个词上）', '音变 / 字母变化', '核对结果', '核对依据', '来源链接', '原表备注', '本次调整', '词根变体处理']
# 列号（从 1 数）
WORD, MEAN, EX, TYPE, SPLIT, PRE, ROOT, WPART, SUF, COMBO, BG, SOUND, CHECK, BASIS, LINK, ORIG, ADJ, VAR = range(5, 23)
NCOL = 22
TEXT_COLS = 'FGIJKLMNOPRST'       # 估行高时看的有文字的列
WORD_TYPES = ('⑤', '④')          # 基础词、不好拆分：解释整格放单词部分
EMPTY = '-'

CONNECT = {('significant', '-i-'), ('spokesman', '-s-'), ('nightingale', '-in-'), ('delight', '-gh-')}
NOTE_ROOT = {('usage', '注意：不是 use'), ('princess', 'princess 是英语'), ('logo', '全称：很可能'), ('betray', '本族的 be-'),
             ('disorder', 'disorder 是英语'), ('since', '变化经过：'), ('difficult', '拉丁语原来的形容词'), ('painter', '注意：painter'),
             ('confused', '来历：这个词'), ('waver', 'waver 也能当'), ('automated', '来历：1952'), ('batter', '两种说法：'),
             ('urgency', '这个词很可能'), ('submarine', '英语自己用拉丁'), ('walnut', '古英语 walhhnutu'), ('horrify', '来源：可能是'),
             ('prayer', '另一个 prayer'), ('irony', '注意：另有一个'), ('Jewish', '今天的 Jewish'), ('mustard', '常见说法')}
AFFIX = re.compile(r'(?<![A-Za-z\-])(-[a-z]+-?|[a-z]+-)(?![A-Za-z])')



# 2026-11 身份分工轮（第 65、67 条）：词根那一行里的“身份：…。分工：…”（前缀、后缀行 2026-11 词缀身份辨析轮起改成“标签：身份：介绍；记：…。辨析：…”，见 linetools.py）。
# 这一段讲的是同一个词根（同一类词缀）的别的写法，体检脚本看这一行本身写了什么时要先去掉它
SHENFEN = re.compile(r'(?:[；。]\s*)?身份：[^。\n]*。分工：[^。\n]*?(?=。|；记：|$)')
SHENFEN_GET = re.compile(r'身份：([^。\n]*)。分工：([^。\n]*?)(?=。|；记：|$)')


def strip_shenfen(line):
    """一行解释去掉“身份：…。分工：…”那一段（词根行）；
    2026-11 词缀身份辨析轮起的词缀行（标签：身份：介绍；记：…。辨析：…）去掉“身份：”这个记号和最后的“。辨析：…”——辨析讲的是别的词缀"""
    s = SHENFEN.sub('', str(line or ''))
    if LT.label_body(s)[1].startswith(LT.ID_MARK):
        s = LT.cut_bianxi(s)[0]
        k = s.index(LT.ID_MARK)
        s = s[:k] + s[k + len(LT.ID_MARK):]
    return s


def plain_parts(text):
    """一格（或合回一格的各部分解释）里，词缀行只留“标签：开头的介绍”（去掉“身份：”这个记号、记法、辨析）；别的行原样。视频体检照视频读表的样子看这一行时用"""
    return '\n'.join(LT.affix_plain(l) if LT.label_body(l)[1].startswith(LT.ID_MARK) else l for l in str(text or '').split('\n'))


def shenfen_of(line):
    """一行解释里的 (身份, 分工)；没有返回 None"""
    m = SHENFEN_GET.search(str(line or ''))
    return (m.group(1).strip(), m.group(2).strip()) if m else None

# 2026-11 拉丁语动词变化轮（第 71 条）：词根那一行“身份：”前面的“动词变化：原形 …→ 过去式 …→ 过去分词 …；规律：…。”。
# 这一段讲的是整个动词（三个样子都写出来了），体检脚本看这一行这个写法本身是什么（是不是过去分词词干、有没有通到今义的链）之前先去掉它。
# 表里这一段总是以句号结束、后面紧跟“身份：”；这里也认句号已经被 strip_shenfen 吃掉以后的样子（后面是“；记：”或行末），所以两个 strip 谁先谁后都行
DONGBIAN = re.compile(r'动词变化：[^。\n]*?；规律：[^。\n]*?(?:。|(?=；记：)|$)')


def strip_dongbian(line):
    """一行解释去掉“动词变化：…；规律：…。”那一段"""
    s = str(line or '')
    m = DONGBIAN.search(s)
    if not m: return s
    head, tail = s[:m.start()], s[m.end():]
    if not m.group(0).endswith('。') and head.endswith('。'): head = head[:-1]      # 句号已经被 strip_shenfen 吃掉了：把前面那个句号也去掉，结果和先去这一段一样
    return head + tail


# 2026-11 词根形态轮（第 107–112 条）：词根行“词根 duc-“…”（…）。形态：…。这个词：…；记：…”——形态是整个词根族的，这个词是本行用哪个形态，体检看这一行本身之前先去掉
XINGTAI = re.compile(r'形态：.*?(?=这个词：)')
ZHEGECI = re.compile(r'这个词：.*?(?=；记：|$)')


def strip_xingtai(line):
    return ZHEGECI.sub('', XINGTAI.sub('', str(line or '')))


def strip_meta(line):
    """去掉“动词变化”“身份、分工”“形态、这个词”几段，剩下这一行自己讲这个写法的话"""
    return strip_shenfen(strip_dongbian(strip_xingtai(line)))


def label_of(line):
    m = re.match(r'^\s*([^：:]{1,60}?)[：:]', line)
    return m.group(1).strip() if m else None


def is_part_label(t):
    return bool(t) and bool(re.match(r'^[A-Za-z0-9āæþðēīōūÆǣ\(\-]', t))


def kind_of_label(t):
    if t.startswith('-') and t.endswith('-') and len(t) > 2:
        return 'infix'
    if t.startswith('-'):
        return 'suf'
    if t.endswith('-'):
        return 'pre'
    return 'root'


def split_parts(word, text):
    """一格各部分解释 → ([前缀行], [词根行], [后缀行])；每行原样，列内先后不变"""
    out = {'pre': [], 'root': [], 'suf': []}
    lines = [l for l in str(text or '').split('\n') if l.strip() and l.strip() not in (EMPTY, '—')]
    labels = []
    for l in lines:
        t = label_of(l)
        labels.append(t if t and is_part_label(t) and not t.startswith('为什么') else None)
    present = {}
    for t in labels:
        if t:
            k = kind_of_label(t)
            if k == 'infix':
                k = 'root' if (word, t) in CONNECT else 'suf'
            present[t] = k
    sufs = {x.lstrip('-'): x for x, k in present.items() if k == 'suf'}
    for l, t in zip(lines, labels):
        if t and ' + ' in t and not t.startswith('-'):
            # “coca + ine：a 和 i 连读…”讲的是拼起来以后的样子：最后一段是本行的后缀，就跟着后缀写（视频按原来的先后读）
            last = t.split('+')[-1].strip().lstrip('-')
            k = 'suf' if last in sufs else 'root'
        elif t:
            k = present[t]
        else:
            lab = label_of(l) or ''
            if lab.startswith('为什么'):
                k = next((present[m.group(1)] for m in AFFIX.finditer(lab) if present.get(m.group(1), 'root') != 'root'), 'root')
            else:
                hit = [present[x] for x in present if present[x] != 'root' and re.search(r'(?<![A-Za-z\-])' + re.escape(x) + r'(?![A-Za-z])', l)]
                k = hit[0] if hit else 'root'
                if any(word == w0 and l.strip().startswith(p0) for w0, p0 in NOTE_ROOT):
                    k = 'root'
        out[k].append(l)
    return out['pre'], out['root'], out['suf']


CJK = re.compile(r'[\u3400-\u9fff]')
LETTER = 'A-Za-zāæþðēīōūÆǣ'
FOREIGN_HINT = re.compile(r'^\s*(=\s*)?(由词根|本组词根|词根|(古|中古|原始|晚期|中世纪|俗)?(拉丁语|希腊语|法语|英法语|意大利语|西班牙语|葡萄牙语|阿拉伯语|波斯语|日语|汉语|德语|荷兰语|古诺尔斯语|古诺斯语|古北欧语|梵语))')


def _bare(t):
    return re.sub(r'（[^（）]*）|\([^()]*\)', '', t).strip()


def is_note_label(t):
    """标签其实是一句说明（“investigate 不是 invest + igate：…”“b 不发音：…”）"""
    b = _bare(t)
    return bool(CJK.search(b)) or ' → ' in b


def _is_part(l):
    t = label_of(l)
    return bool(t) and is_part_label(t) and not t.startswith('为什么') and not is_note_label(t)


def is_connector(t, word=''):
    """连接成分、双写的字母：只有一个字母（-i-、-s-、-b-），或 nightingale 的 -in-、delight 的 -gh-"""
    return len(re.sub('[^' + LETTER + ']', '', t.strip('-'))) == 1 or (word, t) in CONNECT


def _lemmas(w):
    out = {w}
    for suf, rep in (('ies', 'y'), ('es', ''), ('s', ''), ('ied', 'y'), ('ed', ''), ('ed', 'e'), ('d', ''), ('ing', ''), ('ing', 'e'), ('men', 'man')):
        if w.endswith(suf) and len(w) > len(suf) + 1:
            out.add(w[:-len(suf)] + rep)
    for suf in ('ed', 'ing'):
        if w.endswith(suf) and len(w) > len(suf) + 2 and w[-len(suf) - 1] == w[-len(suf) - 2]:
            out.add(w[:-len(suf) - 1])
    return out


def is_word_part(label, body, word='', typ='', words=()):
    """新写的一行（以前没有的）是不是能单独用的英语单词（→ 单词部分）；不是就算词根。
    基础词、不好拆分的整格算单词；带连字符的是词根；表里有这个词（或它的复数、过去式这些形式）、说明不是以“= 拉丁语”“由词根”开头的算单词；
    缩写字母（VIP 的 V）算单词。拿不准的写完自己看一眼，不对就把那一行挪到该去的列（下次 set_parts 照挪过的放）。"""
    if str(typ or '').startswith(WORD_TYPES):
        return True
    if label.startswith('-') or label.endswith('-'):
        return False
    base = _bare(label)
    if base.lower() == str(word).lower():
        return True
    if re.fullmatch(r'[A-Z](、[A-Z])*', base):
        return True
    if not re.fullmatch("[" + LETTER + "'’ .\\-]+", base):
        return False
    see_self = re.search(r'见\s*(第 ?\d+ ?组 ?)?' + re.escape(base.lower()) + r'(?![a-z])', str(body).lower())
    if FOREIGN_HINT.match(str(body)) and not see_self:
        return False
    return bool(see_self) or any(x in words for x in _lemmas(base.lower()))


def _norm_line(l):
    t = label_of(l)
    if t and is_part_label(t) and t.strip('-') and t.strip('-') != t:
        i = l.index(t)
        l = l[:i] + t.strip('-') + l[i + len(t):]
    return l.strip()


def split_parts4(word, text, prev=None, typ=None, words=None):
    """一格各部分解释（老写法）→ ([前缀行], [词根行], [单词行], [后缀行])；每行原样，列内先后不变。
    prev：这一行现在的（前缀、词根、单词部分、后缀）四格。以前写过的行照原来的列放（整行一样、或标签一样就算），
    新写的行：前缀、后缀照 split_parts 的规矩；其余的，能单独用的英语单词放单词部分，别的放词根列；
    说明行跟着主体走：这一行有词根（连接成分不算）就放词根列，没有就放单词部分。"""
    from collections import Counter
    pre, _, suf = split_parts(word, text)
    lines = [l for l in str(text or '').split('\n') if l.strip() and l.strip() not in (EMPTY, '—')]
    where = {}
    for k, cell in enumerate(prev or ()):
        for l in str(cell or '').split('\n'):
            if l.strip() and l.strip() not in (EMPTY, '—'):
                where.setdefault(('line', _norm_line(l)), k)
                t = label_of(l)
                if t:
                    where.setdefault(('label', t.strip('-')), k)
    cp, cs = Counter(pre), Counter(suf)
    col = []
    for l in lines:
        rc = None
        if cp[l] > 0:
            cp[l] -= 1; rc = 0
        elif cs[l] > 0:
            cs[l] -= 1; rc = 3
        t = label_of(l)
        k = where.get(('line', _norm_line(l)))
        if k is None and t and is_part_label(t):
            k = where.get(('label', t.strip('-')))
        col.append(k if k is not None else rc)
    for i, l in enumerate(lines):
        if col[i] is None:
            if str(typ or '').startswith(WORD_TYPES):
                col[i] = 2
            elif _is_part(l):
                col[i] = 2 if is_word_part(label_of(l), l.split('：', 1)[1] if '：' in l else '', word, typ, words or set()) else 1
    has_root = any(k == 1 and _is_part(l) and not is_connector(label_of(l), word) for l, k in zip(lines, col))
    out = ([], [], [], [])
    for l, k in zip(lines, col):
        out[k if k is not None else (1 if has_root else 2)].append(l)
    return out


def cells(word, text, split=None, words=None, prev_root=None, prev=None, typ=None):
    """一格各部分解释 → 四个格子的文字（前缀、词根、单词部分、后缀；没有的写“-”）；给了拆分和单词表的，词根列照规矩加连字符"""
    f = lambda xs: '\n'.join(xs) if xs else EMPTY
    pre, root, wpart, suf = split_parts4(word, text, prev, typ, words)
    if split is not None and words is not None:
        root = hyphenate_lines(root, split, words, prev_root)
    wpart = [strip_root_label(l) for l in wpart]          # 单词部分不加连字符
    return f(pre), f(root), f(wpart), f(suf)


def _order_core(root, wpart, split):
    """词根、单词部分两列的行合在一起时按拆分里的先后穿插，各列内部的先后不变（dubbing = dub + b + ing 合成 dub、b，和分列以前一样）；
    对不上拆分的行（说明）跟着它前面那一行"""
    R = [l for l in str(root or '').split('\n') if l.strip() and l.strip() not in (EMPTY, '—')]
    W = [l for l in str(wpart or '').split('\n') if l.strip() and l.strip() not in (EMPTY, '—')]
    if not R or not W or not split:
        return R + W
    s = str(split).split('；')[0]
    for arrow in ('←', '≈'):
        if arrow in s:
            s = s.split(arrow)[-1]
    order = {}
    for n, p in enumerate(parse_split(s) or []):
        full = re.sub(r'[^a-z0-9āæþðēīōū]', '', re.sub(r'\(\s*=[^)]*\)', '', str(p['raw']).lower()))   # n(e) → ne、Engl(a) → engla
        for k in (_norm(p['surface']), _norm(p['raw']), full):
            if k:
                order.setdefault(k, n)
    def keys(xs):
        out, last = [], 99.0
        for l in xs:
            t = label_of(l)
            k = order.get(_norm(t)) if t and is_part_label(t) else None
            last = float(k) if k is not None else last + 0.01
            out.append(last)
        return out
    kr, kw, out, i, j = keys(R), keys(W), [], 0, 0
    while i < len(R) or j < len(W):
        if j >= len(W) or (i < len(R) and kr[i] <= kw[j]):
            out.append(R[i]); i += 1
        else:
            out.append(W[j]); j += 1
    return out


def combine(pre, root, *rest, split=None):
    """几列合回一格（前缀、词根和单词部分、后缀的先后），“-”不算；词根列标签上的连字符去掉（老脚本、视频按“没有连字符的是词根”认）。
    combine(前缀, 词根, 单词部分, 后缀) 是现在的四列（给了 split 的，词根、单词部分的行按拆分里的先后穿插）；combine(前缀, 词根, 后缀) 是分三列时的老表"""
    four = (pre, root) + tuple(rest) if len(rest) == 2 else (pre, root, None, rest[0] if rest else None)
    rootl = '\n'.join(strip_root_label(l) for l in str(four[1] or '').split('\n')) if str(four[1] or '').strip() not in ('', EMPTY, '—') else ''
    core = _order_core(rootl, four[2], split)
    out = []
    for x in (four[0], '\n'.join(core), four[3]):
        x = str(x or '').strip()
        if x and x not in (EMPTY, '—'):
            out.append(x)
    return '\n'.join(out)


def is_new(row):
    return len(row) >= 21


def legacy(row):
    """22 列的一行 → 以前 19 列的样子（J 是合起来的各部分解释，后面的列号和以前一样）；21 列（分三列时）的也认；本来就是老表的原样返回"""
    row = list(row)
    if len(row) >= NCOL:
        return row[:9] + [combine(row[9], row[10], row[11], row[12], split=row[8])] + row[13:NCOL] + row[NCOL:]
    if len(row) >= 21:
        return row[:9] + [combine(row[9], row[10], row[11])] + row[12:21] + row[21:]
    return row


def get_parts(ws, r):
    return combine(ws.cell(r, PRE).value, ws.cell(r, ROOT).value, ws.cell(r, WPART).value, ws.cell(r, SUF).value, split=ws.cell(r, SPLIT).value)


_WORDS = {}


def table_words(ws):
    """表里的全部单词（小写），判断词根标签是不是能单独用的词"""
    k = id(ws)
    if k not in _WORDS:
        _WORDS[k] = {str(ws.cell(r, WORD).value or '').strip().lower() for r in range(2, ws.max_row + 1)}
    return _WORDS[k]


def set_parts(ws, r, text, word=None):
    """一格各部分解释（老写法，词根不带连字符）→ 写回前缀、词根、单词部分、后缀四列：以前写过的行照原来的列，新的照规矩；词根列照以前的写法或规矩加连字符"""
    word = word if word is not None else str(ws.cell(r, WORD).value or '')
    prev = tuple(ws.cell(r, c).value for c in (PRE, ROOT, WPART, SUF))
    vals = cells(word, text, ws.cell(r, SPLIT).value, table_words(ws), prev[1], prev, ws.cell(r, TYPE).value)
    for c, v in zip((PRE, ROOT, WPART, SUF), vals):
        ws.cell(r, c).value = v


# ---------------- 词根列的连字符（2026-11 用户定下：词根不是能单独用的词，也加“-”）----------------
# 词根列里，拆分的一部分、又不是能单独用的英语单词的，在接别的部分的那一边加“-”：
#   开头的 bio-（biology）、末尾的 -logue（dialogue）、中间的 -ped-（expedition）；
#   母词、合成词里的词（popular、shoe、maker）、讲来历时提到的外语词不加。
#   标签本来就是英语单词、但这里是拉丁 / 希腊词根的（trans + port 的 port：本组词根“运”），说明以“=”“由词根”“本组词根”开头，也加。
ROOT_HINT = re.compile(r'^\s*(=|由词根|本组词根|词根)')
LETTERS = "A-Za-zāæþðēīōūÆǣ'’"


def _norm(x):
    return re.sub(r'[^a-z0-9āæþðēīōū]', '', re.sub(r'\([^)]*\)', '', str(x).lower()))


def split_positions(split):
    """拆分 → {部分: 'first' / 'mid' / 'last'}；“X ← a + b”看箭头后面的；只有一部分的返回 {}"""
    s = str(split or '')
    for arrow in ('←', '≈'):
        if arrow in s:
            s = s.split(arrow)[-1]
    parts = parse_split(s) or []
    if len(parts) < 2:
        return {}
    pos = {}
    for i, p in enumerate(parts):
        where = 'first' if i == 0 else ('last' if i == len(parts) - 1 else 'mid')
        for k in (_norm(p['surface']), _norm(p['raw'])):
            if k:
                pos.setdefault(k, where)
    return pos


def hyphenate_root(label, body, split, words):
    """词根列一行的标签 → 该加连字符的加上（已经有的不动）"""
    if label.startswith('-') or label.endswith('-'):
        return label
    base = re.sub(r'\([^)]*\)', '', label).strip()
    if not re.fullmatch('[' + LETTERS + ']+', base) or len(base) < 2 or base.isupper():
        return label
    where = split_positions(split).get(_norm(label))
    if not where:
        return label
    if base.lower() in words and not ROOT_HINT.match(body):
        return label
    return {'first': label + '-', 'last': '-' + label, 'mid': '-' + label + '-'}[where]


def strip_root_label(line):
    """词根列一行：去掉标签两头的连字符（合回一格给老脚本、视频用，和以前一样）"""
    t = label_of(line)
    if not t or not is_part_label(t) or t.startswith('为什么'):
        return line
    bare = t.strip('-')
    if not bare or bare == t:
        return line
    i = line.index(t)
    return line[:i] + bare + line[i + len(t):]


def hyphenate_lines(root_lines, split, words, prev_root=None):
    """词根列的各行加连字符：以前写过的照以前的写法，新的照规矩"""
    prev = {}
    for l in str(prev_root or '').split('\n'):
        t = label_of(l)
        if t and is_part_label(t):
            prev.setdefault(t.strip('-'), t)
    out = []
    for l in root_lines:
        t = label_of(l)
        if not t or not is_part_label(t) or t.startswith('为什么'):
            out.append(l); continue
        bare = t.strip('-')
        new = prev.get(bare) or hyphenate_root(t, l.split('：', 1)[1] if '：' in l else '', split, words)
        out.append(l.replace(t, new, 1) if new != t else l)
    return out

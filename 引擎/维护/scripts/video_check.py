#!/usr/bin/env python3
"""视频体检：按《构词动画》视频技能读总表的规则，逐行检查「拆分结果」，列出视频会读错、读不全的地方。

用法：
  python3 video_check.py <总表.xlsx>                     # 打印各类数目（和 audit_checklist.md 的基线比）
  python3 video_check.py <总表.xlsx> --show 类别 [N]      # 打印某一类的前 N 条（默认 30），类别用下面的键
  python3 video_check.py <总表.xlsx> --json 结果.json      # 全部明细存成 json（行号、单词、说明）

视频技能读表的规矩（wordfilm.js 2.3 版起，改动时两边一起改；组合列 2026-11 起是清爽格式，先用 columns.merge_cell 还原再查）：
  - 拆分按括号外的“ + ”切开；X(=Y)、X(Y) 的括号是注释或省掉的字母。
  - 各部分解释每行“标签：解释”，标签可以带括号（al(l)、jack(=jaque)、state（v.））、可以写两个（-et、-in）。
    “意思怎么变”“用词规律”两行不算部分。
  - 组合列第一段【构词逻辑】的第一行要有等式：A（…）+ B（…）=“字面意思”；或者“派生路线：X（…）→ Y（…）”，最后一步带意思。
    下面 → 开头、①② 开头的行是意思一步步的变化；现在的意思写在 F 列「含义」（同词性一行、行首写词性），例子在 G 列「例句」（见 meaning.py）。
  - 2026-11 单词列轮起「拆分结果」22 列：F 含义、G 例句、H 类型、I 拆分、J 前缀、K 词根、L 单词部分、M 后缀、N 组合、U 本次调整；读表时用 cols.legacy 把四列合回一格（老的“各部分解释”），下面的列号照 19 列的老样子。
  - 后缀行：括号里写来源（来自拉丁语… / 英语本来就有…）；“在这里：A → B。……加上 -xx，……所以 …”，这一段里不用“；”。
"""
import json
import os
import re
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from columns import merge_cell, parse_I, compose_I  # noqa: E402
import meaning as M  # noqa: E402
import cols  # noqa: E402

CJK = '\u3400-\u9fff'
CIRC = '①②③④⑤⑥⑦⑧⑨⑩'

NAMES = OrderedDict([
    ('h_has_combo', '各部分解释里还有组合的内容（在这里、意思怎么变、用词规律应写在组合列）'),
    ('logic_in_parts', '各部分解释里写了【构词逻辑】字样（视频会把这一格当成组合列）'),
    ('logic_no_eq', '【构词逻辑】第一行没有等式，读不出字面意思'),
    ('no_jinyi', '没有含义（F 列「含义」是空的）'),
    ('mean_no_pos', '含义列有一行没以词性开头（n. / v. / adj. …，见 meaning.py）'),
    ('mean_dup_pos', '含义列同一个词性写了两行（同一词性的意思写在一行，用“；”隔开）'),
    ('mean_empty', '含义列有一行只有词性、没有意思'),
    ('mean_has_example', '含义里还带着例句、例词（括号里英文开头的，应挪到 G 列「例句」）'),
    ('mean_ex_bad', '例句列有一行没写成“意思：例子”'),
    ('mean_ex_unmatched', '例句列的“意思”在含义里找不到（视频配不上例句）'),
    ('split_plus_in_paren', '拆分的括号里带“ + ”'),
    ('part_no_line', '拆分的部分在各部分解释里找不到对应行'),
    ('suf_no_src', '后缀行没写来源'),
    ('suf_src_text_only', '后缀来源只写在正文里，没进括号（视频能读，口径要求进括号）'),
    ('suf_no_here', '拆分里的后缀行没有“在这里”（视频只能用自带的说法讲）'),
    ('here_no_label', '“在这里：”后面没有“A → B。”这一句（视频读不出词性牌和“在这里”）'),
    ('here_semicolon', '“在这里”一段里夹着“；”（视频按“；”切开，后半句丢掉）'),
    ('here_no_affix', '“在这里”没写“加上 -xx”（视频认不出这句）'),
    ('here_awkward', '“在这里”模板句不通顺'),
    ('rule_ex_circled', '用词规律的例子里混进了①②'),
    ('rule_mark_missing', '〔用词规律N〕在“用词规律”那一行里没有第 N 条'),
    ('rule_unmarked', '“用词规律”的第 N 条没在“意思怎么变”里标出来'),
    ('evo_no_step', '“意思怎么变”某一步的结果在组合列里对不上（视频按结果挂规律）'),
    ('fmt_old_pos', '组合列还有单独一行的“词性变化（…）：”（清爽格式要并进第一行）'),
    ('fmt_old_rule', '组合列还有〔用词规律①〕或带编号的“用词规律①：”（清爽格式不编号）'),
    ('fmt_not_canonical', '组合列不是清爽格式的标准写法（columns.py reformat 会改动它）'),
])

# ---------------------------------------------------------------- 后缀来源（和 wordfilm.js 的 affixSource 一样）

LANG = (r'拉丁语|拉丁|希腊语|希腊|古诺尔斯语|古诺斯语|北欧语|古法语|英法语|法兰克语|法语|意大利语|西班牙语|葡萄牙语|'
        r'普罗旺斯语|荷兰语|德语|阿拉伯语|印地语|日耳曼语|古英语|英语')
PRE = r'(?:古|中古|晚期|中世纪|俗|民间|现代|原始)?'
LANGS_IN_PAREN = r'拉丁语|希腊语|古诺尔斯语|古诺斯语|法语|意大利语|西班牙语|葡萄牙语|荷兰语|德语|阿拉伯语|印地语'


def norm_lang(x):
    if re.search(r'英语|日耳曼|本族|lic|leas', x):
        return '英语本族'
    if '拉丁' in x:
        return '拉丁语'
    if '希腊' in x:
        return '希腊语'
    if '诺尔斯' in x or '诺斯' in x or '北欧' in x:
        return '古诺尔斯语'
    if '法' in x:
        return '法语'
    return x


def strip_here(s):
    """去掉“在这里：……所以 ……”那一段（讲词性的话里不找来源）"""
    k = s.find('在这里：')
    if k < 0:
        return s
    j = s.find('所以', k)
    if j < 0:
        return s[:k]
    ends = [e for e in (s.find('；', j), s.find('。', j)) if e >= 0]
    return s[:k] + (s[min(ends):] if ends else '')


def paren_groups(s):
    out, d, st = [], 0, -1
    for i, ch in enumerate(s):
        if ch == '（':
            if d == 0:
                st = i
            d += 1
        elif ch == '）' and d > 0:
            d -= 1
            if d == 0:
                out.append((st, i, s[st + 1:i]))
    return out


TEXT_PATS = [
    r'^\s*(?:是|这是|一个)?' + PRE + '(' + LANG + ')',
    r'(?:来自|源自|出自|借自|取自|往上是|对应|就是|是|从|同出|出|=)\s*' + PRE + '(' + LANG + ')',
    PRE + '(' + LANG + r')[^，。；]{0,16}?(?:词尾|后缀|成分|标记|形式)',
    r'(拉丁|希腊|法)(?:语)?(?:来的|里的)',
    r'(英语本来就有|英语本族|本族的|本族后缀|本族词尾|古英语|日耳曼语|来自\s*-?lic|-leas)',
    PRE + r'(拉丁语|希腊语) -?[a-zāēīōū]',
]


def source_of(line):
    """返回 (来源, 方式)：方式 paren = 标准括号，text = 正文里写的，'' = 没写"""
    s = re.sub(r'\s+', ' ', str(line or '')).strip()
    s2 = strip_here(s)
    for _, _, p in paren_groups(s2):
        if re.search(r'来自|英语本来就有|英语本族|古英语|古诺尔斯语', p):
            if re.search(r'英语本来就有|英语本族|古英语', p) and not re.search(r'来自(拉丁语|希腊语|法语)', p):
                return '英语本族', 'paren'
            ls = re.findall(LANGS_IN_PAREN, p.split('经')[0])
            if ls:
                return '、'.join(dict.fromkeys(norm_lang(x) for x in ls[:2])), 'paren'
            m = re.search('(' + LANG + ')', p.split('经')[0])
            if m:
                return norm_lang(m.group(1)), 'paren'
    for _, _, p in paren_groups(s2):
        m = re.match(r'^\s*' + PRE + '(' + LANG + ')', p)
        if m:
            return norm_lang(m.group(1)), 'paren'
    body = re.sub(r'^[^：]*：', '', s2)
    best = None
    for p in TEXT_PATS:
        m = re.search(p, body)
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), m.group(1))
    if best:
        return norm_lang(best[1]), 'text'
    return '', ''


# ---------------------------------------------------------------- 和 wordfilm.js 一样的小工具
def one_line(s):
    return re.sub(r'\s+', ' ', str(s or '')).strip()


def norm_part(s):
    return re.sub(r'[^a-z0-9]', '', str(s or '').lower())


def norm_head(h):
    """标签 → 比对用的键：去掉（v.）这类中文括号、(=Y) 注释、末尾省掉的字母 (l)；前面的 (s) 留着"""
    s = re.sub(r'（[^（）]*）', '', str(h or ''))
    s = re.sub(r'\(\s*=[^()]*\)', '', s)
    s = re.sub(r'\([^()]*\)\s*-?\s*$', '', s)
    return norm_part(s)


def split_top(s, sep):
    out, depth, cur = [], 0, ''
    i = 0
    while i < len(s):
        ch = s[i]
        if ch in '（(':
            depth += 1
        elif ch in '）)':
            depth = max(0, depth - 1)
        if depth == 0 and s.startswith(sep, i):
            out.append(cur)
            cur = ''
            i += len(sep)
            continue
        cur += ch
        i += 1
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


PLACE = re.compile(r'^(—+|－+|-+|–+|无|暂无|没有|【待处理】|待处理|n/a|none|/)$', re.I)


def parse_split(raw):
    s = one_line(raw)
    if not s or PLACE.match(s):
        return 'single', []
    s = re.split(r'[；;]', s)[0].strip()
    s = re.sub(r'\s*（[^（）]*[%s][^（）]*）' % CJK, '', s).strip()
    if re.search(r'\s←\s', s):
        return 'variant', []
    if re.search(r'\s≈\s', s):
        return 'related', []
    parts = split_top(s, ' + ')
    if len(parts) >= 2:
        out = []
        for x in parts:
            m = re.match(r'^(.*?)\s*\(\s*(=?)\s*([^()]*)\)\s*$', x)
            out.append({'raw': x, 'text': (m.group(1) if m else x).strip(), 'inline': (m.group(3) if m else '').strip(), 'eq': bool(m and m.group(2))})
        return 'parts', out
    return 'single', []


HEAD_RX = re.compile(r'^((?:[^：:%s【】（）()]|\([^()：:]{0,24}\)|（[^（）：:]{0,12}）){1,48}?)\s*[：:]\s*(.*)$' % CJK)


def part_lines(t):
    """各部分解释 → [{head, norm, text}]；“-et、-in”“-ist + -ic”这种一行写两个的，拆成两条"""
    lines = [x.strip() for x in str(t or '').replace('\r', '').split('\n') if x.strip()]
    lines = [x for x in lines if not re.match(r'^(意思怎么变|用词规律)[：:]', x)]
    out = []
    for ln in lines:
        m = HEAD_RX.match(ln)
        if not m or not re.search(r'[A-Za-z0-9]', m.group(1)) or re.match(r'^https?$', m.group(1).strip(), re.I):
            continue
        head, text = m.group(1).strip(), m.group(2).strip()
        toks = [x for x in re.split(r'\s*(?:、|\s\+\s|，)\s*', head) if x]
        if len(toks) >= 2 and all(re.match(r'^-?[A-Za-z()=]+-?$', x) for x in toks):
            for tk in toks:
                out.append({'head': tk, 'norm': norm_head(tk), 'text': text, 'multi': True})
        else:
            out.append({'head': head, 'norm': norm_head(head), 'text': text})
    return out, len(lines)


def merge_doubled(parts):
    """plan + n + ed：双写的那个字母并进前一部分（plan(n)），卡片和颜色都跟着 plan"""
    out = []
    for p in parts:
        k = norm_part(p['text'])
        if out and len(k) == 1 and k.isalpha() and norm_part(out[-1]['text']).endswith(k):
            q = dict(out[-1])
            q['text'] = q['text'] + '(' + p['text'] + ')'
            out[-1] = q
        else:
            out.append(p)
    return out


def match_parts(parts, pl):
    """和 wordfilm.js 的 matchParts 一样：先找写法一样的，再找头尾对得上的，同一部分出现两次用同一行；
    一个字母的部分（双写的 n、连接用的 i）只认写法一样的，不按位置硬配"""
    res = [None] * len(parts)
    used = set()
    keys = [norm_part(p['text']) for p in parts]
    full = [norm_part(p['text'] + (p['inline'] if p.get('inline') and not p.get('eq') and re.fullmatch(r'[A-Za-z]+', p['inline']) else '')) for p in parts]
    for i, k in enumerate(keys):
        j = next((j for j, x in enumerate(pl) if j not in used and (x['norm'] == k or x['norm'] == full[i])), None)
        if j is not None:
            res[i] = j
            used.add(j)
    for i, k in enumerate(keys):
        if res[i] is not None:
            continue
        prev = next((res[a] for a in range(i) if keys[a] == k and res[a] is not None), None)
        if prev is not None:
            res[i] = prev
            continue
        if len(k) <= 1:
            j = next((j for j, x in enumerate(pl) if j not in used and x['norm'] and x['norm'] != k and x['norm'].endswith(k)), None)
            if j is not None:
                res[i] = j
                used.add(j)
            continue
        j = next((j for j, x in enumerate(pl) if j not in used and x['norm'] and k and
                  (x['norm'].endswith(k) or k.endswith(x['norm']) or x['norm'].startswith(k) or k.startswith(x['norm']))), None)
        if j is None:
            j = next((j for j, x in enumerate(pl) if x['norm'] and len(k) >= 2 and k in x['norm'] and len(x['norm']) > len(k)), None)
        if j is not None:
            res[i] = j
            used.add(j)
    for i, k in enumerate(keys):
        if res[i] is None and len(k) > 1:
            j = i if i < len(pl) and i not in used and not any(norm_part(p['text']) == pl[i]['norm'] for p in parts) else None
            if j is not None:
                res[i] = j
                used.add(j)
    return res


def segments(text):
    """组合列按【小标题】分段（行首、句号分号后面的才算）"""
    s = str(text or '').replace('\r', '').strip()
    cuts = []
    for m in re.finditer(r'【([^【】\n]{1,10})】', s):
        ls = s.rfind('\n', 0, m.start()) + 1
        head = s[ls:m.start()]
        if re.match(r'^\s*[\u2460-\u2473]?\s*$', head):
            cuts.append((ls, m.end(), m.group(1)))
        elif re.search(r'[。；;！？!?]\s*$', head):
            cuts.append((m.start(), m.end(), m.group(1)))
    out = []
    first = s[:cuts[0][0] if cuts else len(s)].strip()
    if first:
        out.append(('', first))
    for n, (a, b, mk) in enumerate(cuts):
        out.append((mk, s[b:cuts[n + 1][0] if n + 1 < len(cuts) else len(s)].strip()))
    return out


def top_eq(s):
    """括号、引号外面的第一个“=”"""
    depth = q = 0
    for i, ch in enumerate(s):
        if ch in '（(':
            depth += 1
        elif ch in '）)':
            depth = max(0, depth - 1)
        elif ch == '“':
            q += 1
        elif ch == '”':
            q = max(0, q - 1)
        elif ch == '=' and depth == 0 and q == 0:
            return i
    return -1


def literal_of(right):
    r = one_line(right)
    m = re.match(r'^“([^”]*)”', r)
    if m:
        return m.group(1)
    return re.sub(r'（[^（）]*）|\([^()]*\)', '', re.split(r'[，；;。]', r)[0]).strip().strip('“”')


def parse_equation(line):
    s = one_line(line)
    m = re.match(r'^派生路线[：:]\s*(.*)$', s)
    if m:
        route = split_top(m.group(1), '→')
        last = route[-1] if route else ''
        g = re.match(r'^[^（(]*?[（(]([^（）()]*)[）)]', last.strip())
        return {'route': True, 'literal': g.group(1).strip() if g else ''}
    i = top_eq(s)
    if i < 0:
        return None
    return {'route': False, 'literal': literal_of(s[i + 1:])}


def steps_of(logic):
    out = []
    for ln in str(logic or '').split('\n'):
        ln = ln.strip()
        if re.match(r'^[→⇒]', ln) or re.match(r'^[%s]' % CIRC, ln):
            body = re.sub(r'^[→⇒]\s*', '', ln)
            body = re.sub(r'^[%s]\s*(?:[^，。→“”（）]{1,16}[：:])?\s*' % CIRC, '', body)
            ps = re.split(r'\s*→\s*', body)
            if ps and ps[-1]:
                out.append(ps[-1].strip())
    return out


def _affix_source_old(text):
    """后缀来源：(括号里写的, 正文里写的)"""
    s = one_line(text).split('在这里：')[0]
    pars = re.findall(r'（[^（）]*(?:（[^（）]*）[^（）]*)*）', s)
    inparen = next((p for p in pars if SRC_PAREN.search(p)), '')
    body = re.sub(r'（[^（）]*(?:（[^（）]*）[^（）]*)*）', '', s)
    intext = ''
    if re.search(r'英语本来就有|英语本族|古英语|本族', body) or re.search(r'(?:来自|源自|出自|借自|取自|就是|=)\s*(?:古|中古|晚期|中世纪|俗|民间)?(?:%s)' % LANGS, body) \
            or re.search(r'^(?:一个|这是)?[^，。；]{0,6}(?:%s)[^，。；]{0,10}(?:词尾|后缀|名词|形容词|动词|成分|形式|写法|拼法|的)' % LANGS, body) \
            or re.search(r'(?:%s)(?:来的|语的)' % LANGS, body):
        intext = 'yes'
    return inparen, intext


AWK = [
    (r'“(正在它|能被它|和它有关的|充满它的|已经被它了|会它、|长着它的|使变得它|没有它的|属于它的|有它的|一类它|做它的|它”)', '引号里填了“它”'),
    (r'(?<!目)的的|了了|正在正在|使变得使', '“的的”“了了”这类叠字'),
    (r'使变得“?(力量|长度|高度|宽度|深度|强度|样子)', '“使变得+名词”'),
    (r'有[^，。“”]{1,4}样子的', '“有X样子的”'),
    (r'和[^，。“”]{1,12}的有关的', '“和…的有关的”'),
    (r'“[^”]{1,12}(?<!目)的”，?是一样东西', '把“…的”说成一样东西'),
    (r'“像”是一样东西', '把“像”说成一样东西'),
    (r'加上它', '“加上它”'),
    (r'是一个动作，加上 -[a-z]+ 变成形容词[^。]*说的是“和[^”]*的有关的”', '动作 → “和…有关的”'),
]


def here_part(text):
    m = re.search(r'在这里：(.*)$', one_line(text))
    return m.group(1) if m else ''


def parse_rules(line):
    s = re.sub(r'^用词规律[：:]\s*', '', one_line(line))
    out = OrderedDict()
    for p in re.split(r'(?=[①②③④⑤⑥](?!\s*[^\s]{0,3}[→）]))', s):
        m = re.match(r'^([①②③④⑤⑥])\s*(.*)$', p.strip())
        if not m:
            continue
        body, ex = m.group(2).strip(), ''
        if body.endswith('）'):
            d, k = 0, len(body) - 1
            while k >= 0:
                if body[k] == '）':
                    d += 1
                elif body[k] == '（':
                    d -= 1
                    if d == 0:
                        break
                k -= 1
            if k > 0:
                ex, body = body[k + 1:-1], body[:k]
        out[m.group(1)] = (body.strip(), ex.strip())
    return out


def parse_evo(line):
    """意思怎么变 → [{result, marks}]；步骤按顺序编号切开（可以多于 6 步），〔用词规律N〕在步骤里任何位置都认"""
    from columns import split_steps, MARK
    s = re.sub(r'^意思怎么变[：:]\s*', '', one_line(line))
    s = re.sub(r'^从字面的“[^”]*”出发[：:]\s*', '', s)
    out = []
    for p in split_steps(s):
        marks = ''.join(MARK.findall(p))
        body = MARK.sub('', re.sub(r'^[①②③④⑤⑥⑦⑧⑨⑩]\s*', '', p)).strip()
        out.append({'result': re.split(r'\s*→\s*', body)[-1].strip(), 'marks': list(marks)})
    return out


def nres(t):
    return re.sub(r'\s+', '', re.sub(r'（[^（）]*）|\([^()]*\)', '', one_line(t)))


# ---------------------------------------------------------------- 体检
def check_rows(rows):
    """rows：[(行号, [A..R 各列])]；返回 {类别: [(行号, 单词, 说明)]}"""
    found = OrderedDict((k, []) for k in NAMES)
    for rn, r in rows:
        w = str(r[4] or '')
        G, H, I = str(r[8] or ''), str(r[9] or ''), str(r[10] or '')   # I 拆分、J 各部分解释、K 组合（2026-11 起 G 列是「例句」）
        if not w:
            continue
        if re.search(r'在这里：|^意思怎么变：|^用词规律：', H, re.M):
            found['h_has_combo'].append((rn, w, ''))
        if re.search(r'^\s*词性变化（', I, re.M):
            found['fmt_old_pos'].append((rn, w, ''))
        if '〔用词规律' in I or re.search(r'^\s*用词规律[①②③④⑤⑥⑦⑧⑨⑩]', I, re.M):
            found['fmt_old_rule'].append((rn, w, ''))
        d0 = parse_I(I, w)
        if 'raw' not in d0 and compose_I(d0) != I.replace('\r', ''):
            found['fmt_not_canonical'].append((rn, w, ''))
        # 组合列（清爽格式）先临时还原成老格式：词性变化、“在这里”并回后缀行，用词规律编号、标回步骤，下面的检查照旧
        H, I = merge_cell(H, I, with_evo=True)
        add = lambda k, msg='': found[k].append((rn, w, msg))
        if '【构词逻辑】' in H:
            add('logic_in_parts')
        kind, parts = parse_split(G)
        for p in parts:
            if re.search(r'\(\s*=?[^()]*\s\+\s[^()]*\)', p['raw']):
                add('split_plus_in_paren', G)
        segs = segments(I)
        logic = next((b for mk, b in segs if mk == '构词逻辑'), '')
        first = logic.split('\n')[0] if logic else ''
        if kind == 'parts':
            eq = parse_equation(first)
            if not eq or not eq['literal']:
                add('logic_no_eq', first[:60])
        if not str(r[5] or '').strip():                       # 今义 2026-11 起写在 F 列「含义」
            add('no_jinyi')
        for k, line in M.problems(r[5], r[6]):                 # 2026-11 起含义同词性一行、行首写词性；例子在 G 列「例句」
            add('mean_' + k, line[:40])
        pl, _ = part_lines(H)
        alt = len(pl) == 1 and kind == 'parts' and (re.match(r'^见\s', pl[0]['text'] or '') or norm_part(pl[0]['head']) == norm_part(w))
        if kind == 'parts' and not alt:
            parts = merge_doubled(parts)
            res = match_parts(parts, pl)
            for j in res:
                if j is not None:
                    pl[j]['used'] = True
            for p, j in zip(parts, res):
                k = norm_part(p['text'])
                if j is None and len(k) > 1:
                    add('part_no_line', p['text'])
        # 后缀行（拆分里用到的那几行，标签以 - 开头）
        for x in pl:
            if not x['head'].startswith('-') or x.get('multi'):
                continue
            src, how = source_of(x['head'] + '：' + x['text'])
            if not how:
                add('suf_no_src', x['head'])
            elif how == 'text':
                add('suf_src_text_only', x['head'] + ' ' + src)
            hp = here_part(x['text'])
            if not hp and x.get('used') and not x['head'].rstrip().endswith('-'):     # -it-、-at- 这类夹在中间的成分不讲词性
                add('suf_no_here', x['head'])
            if hp and not re.match(r'^[^。；]*。', hp):
                add('here_no_label', x['head'])
            if hp:
                k = hp.find('所以')
                pre = hp if k < 0 else hp[:k]          # “在这里：”到“所以”之间：视频要从这里读出“加上 -xx，……”
                if '；' in pre:
                    add('here_semicolon', x['head'])
                elif not re.search(r'加上\s*-[A-Za-z]+', pre):
                    add('here_no_affix', x['head'])
                for rx, tag in AWK:
                    if re.search(rx, re.sub(r'（[^（）]*）', '', pre)):      # 括号里是后缀本身的意思（“有…样子的”），不算
                        add('here_awkward', x['head'] + ' ' + tag)
                        break
        # 意思怎么变、用词规律
        hl = [l.strip() for l in H.split('\n')]
        rl = next((l for l in hl if l.startswith('用词规律：')), '')
        el = next((l for l in hl if l.startswith('意思怎么变：')), '')
        rules = parse_rules(rl) if rl else {}
        for st, en, inner in paren_groups(rl):
            if re.search('[%s]' % CIRC, inner):
                add('rule_ex_circled', inner[:40])
        if el:
            evo = parse_evo(el)
            marks = set()
            stepres = {nres(x) for x in steps_of(logic)}
            for st in evo:
                for mk in st['marks']:
                    marks.add(mk)
                    if mk not in rules:
                        add('rule_mark_missing', mk)
                if st['marks'] and nres(st['result']) not in stepres:
                    add('evo_no_step', st['result'][:30])
            for n in rules:
                if n not in marks:
                    add('rule_unmarked', n)
    return found


def load_rows(path):
    from openpyxl import load_workbook
    wb = load_workbook(path, read_only=True)
    ws = wb['拆分结果'] if '拆分结果' in wb.sheetnames else wb.worksheets[0]
    out = []
    for i, r in enumerate(ws.iter_rows(values_only=True), start=1):
        if i == 1:
            continue
        r = cols.legacy(r)                       # 2026-11 起前缀、词根、单词部分、后缀四列：合回一格，列号照旧
        if len(r) > 9: r[9] = cols.plain_parts(r[9])          # 2026-11 词缀身份辨析轮：词缀行“标签：身份：介绍；记：…。辨析：…”只看开头的介绍（视频 6.2 也是这样读的；辨析里“是拉丁语来的”不算这一行的来源）
        out.append((i, list(r) + [None] * (19 - len(r))))
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    rows = load_rows(sys.argv[1])
    found = check_rows(rows)
    if '--show' in sys.argv:
        k = sys.argv[sys.argv.index('--show') + 1]
        n = int(sys.argv[sys.argv.index('--show') + 2]) if len(sys.argv) > sys.argv.index('--show') + 2 and sys.argv[sys.argv.index('--show') + 2].isdigit() else 30
        print('%s：%d 处' % (NAMES.get(k, k), len(found.get(k, []))))
        for rn, w, msg in found.get(k, [])[:n]:
            print('  第 %d 行 %s  %s' % (rn, w, msg))
        return
    if '--json' in sys.argv:
        json.dump({k: v for k, v in found.items()}, open(sys.argv[sys.argv.index('--json') + 1], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('视频体检（%d 个词）' % len(rows))
    for k, name in NAMES.items():
        print('  %-20s %5d  %s' % (k, len(found[k]), name))


if __name__ == '__main__':
    main()

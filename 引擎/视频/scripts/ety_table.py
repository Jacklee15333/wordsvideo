#!/usr/bin/env python3
"""词源总表 → 每个单词的“词条详情”（构词动画的输入）。

用法：
  python3 ety_table.py build   <词源表.xlsx> <work/ety.json>          # 整张表读一次存成 json（大表要十几秒，以后都读 json）
  python3 ety_table.py detail  <work/ety.json> <单词,单词,...> <work/details.json> [--pool 表] [--prefer 表]
  python3 ety_table.py find    <work/ety.json> <单词>                 # 看看这个词在不在表里、是哪一行
  python3 ety_table.py related <work/ety.json> <单词> [--pool 表] [--prefer 表]   # 小黑板“扩展”能挑的词（都在总表里）

扩展词（小黑板“扩展”那一行）只从总表里挑：同一组号的词，加上别的组里“拆分”带着同一个词根、意思也对得上的词，
按“和本词共用一部分、常见、不是本词加个后缀”排好；detail 的结果里叫 extend，前 4 个 pick: true 是默认写上黑板的。
  --pool 表    扩展词还必须在这张表里（比如只要课本单词表 6A-9A.xlsx 里的词）；可以给几张，逗号隔开
  --prefer 表  这张表里的词排前面（run.py 给了 --unit-list 时自动用它）

表格格式（第一行或前几行里有一行列名）：一列“单词”，其余各列按列名认：
  类型 → type（小标签）  拆分 → split（大字）  各部分解释 / 组合 → 现在的含义 / 音变 … → body（正文）
  …背景… → bg（只写在词族第一个词上，族里其他词借用）  …备注 → note  核对结果 → check  核对依据 → basis  …链接 → link
  组号 → 词族（同一组号的词是一家）；批次、序号、小类号这类编号列不用。
detail 的格式和“单词对照台”软件里的一样：{ w, fields: [{ l, s, role, t, from? }], family: [...], g, base, family_meanings }。
"""
import json
import os
import re
import sys
import unicodedata

ROLES = [
    ('prefix', re.compile(r'^前缀$')),        # 2026-11 起总表的「前缀」「词根」「后缀」三列（读表时也合成一格“各部分解释”）
    ('root', re.compile(r'^词根$')),
    ('suffix', re.compile(r'^后缀$')),
    ('word', re.compile(r'^单词部分$')),      # 2026-11 单词列轮起总表 L 列「单词部分」：能单独用的英语单词（make、up、match），卡片标“单词”
    ('meaning', re.compile(r'^(含义|词义|释义|意思|中文意思|中文释义|meaning|meanings?)$', re.I)),
    ('meaning_cz', re.compile(r'^(初中含义|常用含义|初中常用含义)$')),      # 6.32 起（总表“初中含义版”，第七十六版）：视频讲的意思照它   # 现在的意思（2026-11 起总表 F 列「含义」：同词性一行、行首写词性）
    ('examples', re.compile(r'^(例句|例词|例句、例词|例句 ?/ ?例词|例子|examples?)$', re.I)),          # 例句、例词（2026-11 起总表 G 列「例句」：每行“意思：例子”）
    ('bianxi', re.compile(r'^(辨析|同义词辨析|近义词辨析)$')),
    ('ti1', re.compile(r'^(题目|练习|练习题)\s*1$')), ('ti2', re.compile(r'^(题目|练习|练习题)\s*2$')), ('ti3', re.compile(r'^(题目|练习|练习题)\s*3$')),
    ('ti4', re.compile(r'^(题目|练习|练习题)\s*4$')), ('ti5', re.compile(r'^(题目|练习|练习题)\s*5$')),
    ('ti6', re.compile(r'^(题目|练习|练习题)\s*6$')), ('ti7', re.compile(r'^(题目|练习|练习题)\s*7$')),      # 6.31 起（总表“详细考点版”，第七十五版）：7 道题，第 6、7 题专门考考点      # 6.14 起（总表“练习题版”）：五道练习题，视频“练习”那一部分读它（维护技能第 122 条）
    ('daan', re.compile(r'^(答案|练习答案|题目答案)$')),      # 6.15 起（总表“练习答案版”）：五道题的答案和讲解，视频最后“答案”那一部分读它
    ('duyin', re.compile(r'^(读音现象|发音现象|读音说明)$')),      # 6.26 起（总表“读音现象版”，维护技能第 124 条）：读音特别的地方“现象 + 为什么”，视频读音拆分后面一条一幕讲
    ('kaodian', re.compile(r'^(考点|考试考点|常考点)$')),            # 6.11 起（总表“考点轮”）：「考点」列——【变形】【词性转换】【短语】【用法】【易混】，视频“考点”那一部分读它          # 6.0 起（总表“辨析列”轮）：「辨析」列——【同义词】行 + 辨析的话，视频第三部分读它
    ('type', re.compile(r'^(类型|词源类型|构词类型|拆分类型|类别|type)$', re.I)),
    ('split', re.compile(r'^(拆分|构词|拆解|构词拆分|词根词缀|词素拆分|split|morphemes?)', re.I)),
    ('check', re.compile(r'核对结果|核查结果|核对状态|审核结果|^check', re.I)),
    ('basis', re.compile(r'核对依据|核查依据|依据|basis', re.I)),
    ('link', re.compile(r'链接|网址|url|link', re.I)),
    ('bg', re.compile(r'背景|background', re.I)),
    ('note', re.compile(r'备注|^notes?$', re.I)),
]
SKIP = re.compile(r'^(序号|编号|行号|序|批次|批号|小类号|本次调整|调整记录|词根变体处理|no\.?|#|id|index|batch)$', re.I)
GROUP = re.compile(r'^(组号|词族|词族号|词族编号|族号|family|group)$', re.I)
# 含义列行首的词性（2026-11 起：同一词性的意思写一行，行首写词性；例子在「例句」列）
POS_LINE = re.compile(r'^(?:modal v\.|aux\. v\.|n\.|v\.|adj\.|adv\.|pron\.|prep\.|conj\.|num\.|art\.|int\.|phr\.)\s+')
PLACEHOLDER = re.compile(r'^(—+|－+|-+|–+|无|暂无|没有|【待处理】|待处理|n/a|none|/)$', re.I)


def strip_root(text):
    """词根列：每行标签两头的连字符去掉（“-ped-：…”→“ped：…”）"""
    out = []
    for l in str(text or '').split('\n'):
        m = re.match(r'^(\s*)((?:[A-Za-z0-9āæþðēīōū\-]|\([^()：:]*\))+?)([：:])', l)   # 标签里可以带括号（al(=el)-、mo(v)-）
        if m and (m.group(2).startswith('-') or m.group(2).endswith('-')) and m.group(2).strip('-'):
            l = m.group(1) + m.group(2).strip('-') + l[m.end(2):]
        out.append(l)
    return '\n'.join(out)


def role_of(label):
    for r, rx in ROLES:
        if rx.search(label):
            return r
    return 'body'


def short_label(label):
    s = re.sub(r'\s*[（(][^（）()]*[)）]\s*$', '', label)
    s = re.sub(r'^新\s*[·・]\s*', '', s).strip()
    return s or label


def key_of(w):
    w = unicodedata.normalize('NFKC', str(w or '')).strip().lower()
    w = re.sub(r'\s+', ' ', w)
    return re.sub(r'[.。]+$', '', w)


def cell_text(v):
    if v is None:
        return ''
    s = str(v).replace('\r\n', '\n').replace('\r', '\n')
    lines = [x.strip() for x in s.split('\n')]
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip()


# ---------------------------------------------------------------- 扩展词要用的：拆分的部分、各部分的意思
AFFIX_FREQ = 60          # 在总表里出现超过这么多次的部分（ly、ion、er、ing…）算常用词缀，不拿来找扩展词
NORM = lambda s: re.sub(r'[^a-z]', '', str(s or '').lower())
PART_LINE = re.compile(r'^((?:[^：:\u3400-\u9fff【】（）()]|\([^()：:]{0,24}\)|（[^（）：:]{0,12}）){1,48}?)\s*[：:]\s*(.*)$')


def norm_head(h):
    """标签 → 比对用的键：去掉（v.）、(=Y) 注释、末尾省掉的字母 (l)；和 wordfilm.js 的 normHead 一样"""
    s = re.sub(r'（[^（）]*）', '', str(h or ''))
    s = re.sub(r'\(\s*=[^()]*\)', '', s)
    s = re.sub(r'\([^()]*\)\s*-?\s*$', '', s)
    return NORM(s)


def split_top_plus(s):
    out, d, cur = [], 0, ''
    for ch in s:
        if ch in '（(':
            d += 1
        elif ch in '）)':
            d = max(0, d - 1)
        if ch == '+' and d == 0:
            out.append(cur)
            cur = ''
        else:
            cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]
STOP_CHARS = set('的了是一个把在和与或等这那里也就都而及之其使做…、，。；：“”（）() 有为对被让')


def split_parts(raw):
    """拆分那一格 → 部分（只认 a + b 这种；变体、同源、基础词返回空）"""
    s = re.split(r'[；;]', str(raw or '').strip())[0]
    s = re.sub(r'\s*（[^（）]*[\u3400-\u9fff][^（）]*）', '', s).strip()
    if not re.search(r'\s\+\s', s) or re.search(r'\s[←≈]\s', s):
        return []
    out = []
    for p in split_top_plus(s):
        n = NORM(re.sub(r'\([^()]*\)', '', p))
        if n:
            out.append(n)
    return out if len(out) >= 2 else []


def part_glosses(text):
    """各部分解释 → { 部分（只留字母）: 意思 }"""
    out = {}
    for ln in str(text or '').split('\n'):
        m = PART_LINE.match(ln.strip())
        if m and re.search(r'[A-Za-z]', m.group(1)) and not re.match(r'^https?$', m.group(1).strip(), re.I):
            out.setdefault(norm_head(m.group(1)), m.group(2).strip())
    return out


def gloss_chars(g):
    g = re.sub(r'（[^（）]*）|\([^()]*\)', '', str(g or ''))
    g = re.split(r'[；;]', g)[0]
    return {c for c in g if '\u3400' <= c <= '\u9fff' and c not in STOP_CHARS}


def same_sense(a, b):
    """两个部分的意思对不对得上：有一个实在的汉字相同就算（搬运 / 运送）；有一边没写意思就不好说，算对得上"""
    ca, cb = gloss_chars(a), gloss_chars(b)
    return not ca or not cb or bool(ca & cb)


def short_meaning(s, n=8):
    """小黑板上一个扩展词后面写的意思：短一点"""
    s = re.sub(r'（[^（）]*）|\([^()]*\)', '', str(s or '')).strip()
    s = re.split(r'[；;。：:]', s)[0].strip()
    if len(s) > n:
        s = re.split(r'[、，,]', s)[0].strip()
    return s[:n]


def longest_common(a, b):
    """最长公共子串有几个字母"""
    best = 0
    for i in range(len(a)):
        j = i + best + 1
        while j <= len(a) and a[i:j] in b:
            best = j - i
            j += 1
    return best


VARIANT_SUF = ('s', 'es', 'ed', 'd', 'ing', 'er', 'ers', 'or', 'ors', 'ive', 'ly', 'ily', 'ally', 'ion', 'ions', 'ation', 'ment',
               'ness', 'ity', 'al', 'ance', 'ence', 'ist', 'ism', 'ize', 'ise', 'y', 'ship', 'hood')
VARIANT_PRE = ('un', 'in', 'im', 'il', 'ir', 'dis', 'non', 'mis', 're')


def variant_of(a, b):
    """b 是不是 a 换个词尾、加个否定前缀（report / reporter，important / unimportant）：扩展词里这种只留一个"""
    a, b = a.lower().replace('-', ''), b.lower().replace('-', '')
    if a == b:
        return True
    s, l = (a, b) if len(a) <= len(b) else (b, a)
    for stem in {s, s[:-1] if len(s) > 4 and s[-1] in 'ey' else s}:
        if l.startswith(stem) and l[len(stem):] in VARIANT_SUF + tuple('i' + x for x in VARIANT_SUF):
            return True
    if l.endswith(s) and l[:-len(s)] in VARIANT_PRE:
        return True
    n = 0
    while n < min(len(a), len(b)) and a[n] == b[n]:
        n += 1
    return n >= 8


def strip_note(w):
    return re.sub(r'\s*[（(][^）)]*[）)]\s*', '', str(w or '')).strip()


def load_words(paths):
    """一张或几张表里的单词（小写），用来卡扩展词（--pool）或者排前面（--prefer）。
    认得：按册、单元排的单词表（6A-9A.xlsx）；有一列叫“单词 / word”的 xlsx；txt / csv（每行第一个词）"""
    words = set()
    for path in [p for p in re.split(r'[,，]', paths or '') if p.strip()]:
        path = path.strip()
        ext = os.path.splitext(path)[1].lower()
        if ext in ('.xlsx', '.xlsm'):
            items = []
            try:
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                from unit_words import read as read_units
                items = read_units(path)
            except Exception:
                items = []
            if items:
                words |= {key_of(strip_note(it['word'])) for it in items}
                continue
            from openpyxl import load_workbook
            wb = load_workbook(path, read_only=True)
            for ws in wb.worksheets:
                col = None
                for i, row in enumerate(ws.iter_rows(values_only=True)):
                    cells = [str(c).strip() if c is not None else '' for c in row]
                    if col is None:
                        col = next((j for j, c in enumerate(cells) if c in ('单词', '词条', 'word', 'Word', '英文')), None)
                        if col is None and i >= 10:
                            break
                        continue
                    if col < len(cells) and re.search(r'[A-Za-z]', cells[col]):
                        words.add(key_of(strip_note(cells[col])))
        else:
            for line in open(path, encoding='utf-8-sig'):
                first = re.split(r'[,\t，；;|]', line.strip())[0].strip()
                if re.search(r'[A-Za-z]', first):
                    words.add(key_of(strip_note(first)))
    return words


def build(xlsx, out):
    from openpyxl import load_workbook
    wb = load_workbook(xlsx, read_only=True)
    best = None
    sheets = [wb['拆分结果']] if '拆分结果' in wb.sheetnames else wb.worksheets      # 有「拆分结果」就只读它（别的表是记录、说明）
    for ws in sheets:
        if re.search(r'说明|规则|示例|readme', ws.title, re.I):
            continue
        rows = ws.iter_rows(values_only=True)
        head, hi = None, -1
        buf = []
        for i, row in enumerate(rows):
            buf.append(row)
            cells = [str(c).strip() if c is not None else '' for c in row]
            if head is None and i < 10 and any(c in ('单词', '词条', 'word', 'Word', '英文') for c in cells):
                head, hi = cells, i
            if head is None and i >= 10:
                break
        if head is None:
            continue
        rest = list(rows)
        allrows = buf[hi + 1:] + rest
        if best is None or len(allrows) > len(best[1]):
            best = (head, allrows, ws.title)
    if best is None:
        sys.exit('没找到“单词”列：表格前几行里要有一行列名，其中一列叫“单词”')
    head, rows, sheet = best
    wcol = next(i for i, c in enumerate(head) if c in ('单词', '词条', 'word', 'Word', '英文'))
    gcol = next((i for i, c in enumerate(head) if GROUP.match(c)), -1)
    # 2026-11 起总表把“各部分解释”拆成了「前缀」「词根」「后缀」三列（单词列轮起词根后面再加「单词部分」）：读的时候合回一格“各部分解释”（“-”不算），后面照老样子读
    tri = [next((i for i, c in enumerate(head) if c == n), -1) for n in ('前缀', '词根', '后缀')]
    merge3 = all(i >= 0 for i in tri)
    wpi = next((i for i, c in enumerate(head) if c == '单词部分'), -1)   # 2026-11 单词列轮起：词根后面多一列「单词部分」（能单独用的英语单词）
    parts = tri[:2] + ([wpi] if wpi >= 0 else []) + tri[2:]               # 合成“各部分解释”的先后：前缀、词根和单词部分（按拆分穿插）、后缀
    scol = next((i for i, c in enumerate(head) if role_of(c) == 'split'), -1)
    cols = [(i, c) for i, c in enumerate(head) if c and i not in (wcol, gcol) and not SKIP.match(c) and not (merge3 and i in parts[1:])]
    if merge3:
        cols = [(i, '各部分解释' if i == tri[0] else c) for i, c in cols] + [(i, head[i]) for i in parts]   # 各列也各留一份（角色 prefix / root / word / suffix）
    labels = [{'l': c, 's': short_label(c), 'role': role_of(c)} for _, c in cols]
    entries = []
    for row in rows:
        if not row or wcol >= len(row) or row[wcol] is None:
            continue
        w = cell_text(row[wcol])
        if not w or not re.search(r'[A-Za-z]', w):
            continue
        f = []
        for j, (i, lab) in enumerate(cols):
            if merge3 and i == tri[0] and lab == '各部分解释':
                # 词根列标签上的连字符（bio-、-ped-）去掉：视频按“没有连字符的是词根”认，和以前一样
                txt = {k: ((strip_root(cell_text(row[k])) if k == tri[1] else cell_text(row[k])) if k < len(row) else '') for k in parts}
                txt = {k: ('' if PLACEHOLDER.match(v.strip()) else v) for k, v in txt.items()}
                core = core_lines(txt[tri[1]], txt[wpi], row[scol] if scol >= 0 and scol < len(row) else '') if wpi >= 0 else [x for x in (txt[tri[1]],) if x]
                t = '\n'.join(x for x in [txt[tri[0]]] + core + [txt[tri[2]]] if x)
            else:
                t = cell_text(row[i]) if i < len(row) else ''
            if t:
                f.append([j, t])
        g = cell_text(row[gcol]) if gcol >= 0 and gcol < len(row) else ''
        entries.append({'w': w, 'g': g, 'f': f})
    json.dump({'sheet': sheet, 'labels': labels, 'entries': entries}, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
    print('读了“%s”：%d 个单词，%d 列内容（%s），%s' % (sheet, len(entries), len(labels), '、'.join(x['s'] for x in labels),
                                            '有组号（词族）' if gcol >= 0 else '没有组号列'))


def core_lines(root, word, raw_split):
    """「词根」「单词部分」两列的行合在一起，按拆分里的先后穿插，各列内部的先后不变（dubbing = dub + b + ing 读成 dub、b，和分列以前一样）；
    对不上拆分的行（说明）跟着它前面那一行"""
    R = [x for x in root.split('\n') if x.strip()] if root else []
    W = [x for x in word.split('\n') if x.strip()] if word else []
    if not R or not W:
        return R + W
    order = {}
    s = re.sub(r'\s*（[^（）]*[\u3400-\u9fff][^（）]*）', '', re.split(r'[；;]', str(raw_split or '').strip())[0]).strip()
    if split_parts(raw_split):
        for n, p in enumerate(split_top_plus(s)):
            for k in (NORM(re.sub(r'\([^()]*\)', '', p)), NORM(re.sub(r'\(\s*=[^()]*\)', '', p))):   # n(e) 也认 ne、Engl(a) 也认 engla
                if k:
                    order.setdefault(k, n)
    def keys(xs):
        out, last = [], 99.0
        for x in xs:
            m = PART_LINE.match(x)
            k = order.get(norm_head(m.group(1))) if m else None
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


class Table:
    def __init__(self, path):
        d = json.load(open(path, encoding='utf-8'))
        self.labels = d['labels']
        self.entries = d['entries']
        self.by_key = {}
        for i, e in enumerate(self.entries):
            self.by_key.setdefault(key_of(e['w']), []).append(i)
        self.groups = {}
        for i, e in enumerate(self.entries):
            if e['g']:
                self.groups.setdefault(e['g'], []).append(i)

    def text(self, e, role):
        for j, t in e['f']:
            if self.labels[j]['role'] == role and not PLACEHOLDER.match(t.strip()):
                return t
        return ''

    def find(self, w):
        """返回 (行号, 是不是用了原形)。写法完全一样的优先；找不到就试原形（复数、三单、过去式这些最常见的变化）"""
        k = key_of(w)
        hits = self.by_key.get(k)
        if hits:
            exact = [i for i in hits if self.entries[i]['w'] == str(w).strip()]
            return (exact or hits)[0], False
        for cand in lemma_candidates(k):
            if cand in self.by_key:
                return self.by_key[cand][0], True
        return None, False

    def meaning(self, i):
        """一个词现在的意思（一句话）：「含义」列的第一个意思；老表是“组合 → 现在的含义”里【今义】那一段的第一句"""
        e = self.entries[i]
        own = self.text(e, 'meaning')                       # 2026-11 起今义写在「含义」列
        if own:
            first = own.split('\n')[0]
            first = POS_LINE.sub('', first)                 # 2026-11 起一行一个意思、行首写词性：n. 比赛（a football match）
            first = re.sub(r'^[\u2460-\u2473]\s*', '', first)  # 同形词的 ①②
            s = re.sub(r'^(?:[（(][^（）()]*[）)]\s*)+', '', first)
            while True:                                      # 括号里还套着括号的，一层层去掉
                s2 = re.sub(r'（[^（）]*）|\([^()]*\)', '', s)
                if s2 == s: break
                s = s2
            return re.split(r'[；;。]', s)[0].strip()
        for j, t in e['f']:
            m = re.search(r'【今义】([^【\n]*)', t)
            if m:
                s = re.sub(r'（[^（）]*）|\([^()]*\)', '', m.group(1))
                return re.split(r'[；;。]', s)[0].strip()
        return ''

    # ------------------------------------------------------------ 扩展词
    def _index(self):
        if hasattr(self, '_parts'):
            return
        lab = next((j for j, x in enumerate(self.labels) if '各部分' in x['l']), None)
        self._parts, self.part_index, self.part_freq = [], {}, {}
        for i, e in enumerate(self.entries):
            ps = split_parts(self.text(e, 'split'))
            gl = {}
            if ps and lab is not None:
                gl = part_glosses(next((t for j, t in e['f'] if j == lab), ''))
            items = []
            for n in ps:
                g = gl.get(n) or next((v for k, v in gl.items() if k and (k.startswith(n) or n.startswith(k) or k.endswith(n) or n.endswith(k))), '')
                items.append((n, g))
                self.part_index.setdefault(n, []).append(i)
                self.part_freq[n] = self.part_freq.get(n, 0) + 1
            self._parts.append(items)

    def core_parts(self, i):
        """这个词里实在的部分（词根、不太常用的词缀），拿来找扩展词"""
        self._index()
        me = key_of(self.entries[i]['w']).replace('-', '')
        return [(n, g) for n, g in self._parts[i] if len(n) >= 2 and n != NORM(me) and self.part_freq.get(n, 0) <= AFFIX_FREQ]

    def share_of(self, i, k):
        """扩展词 k 和本词 i 共用的那一部分（小黑板上标颜色）；共用的部分意思要对得上"""
        self._index()
        kp = dict(self._parts[k])
        best = ''
        for n, g in self.core_parts(i):
            if n in kp and same_sense(g, kp[n]) and len(n) > len(best):
                best = n
        return best

    def related(self, i, pool=None, prefer=None, limit=12):
        """小黑板“扩展”能挑的词，排好序：[{w, m, via, share, score}]。都在总表里（给了 pool 还要在 pool 里）"""
        self._index()
        e = self.entries[i]
        me = key_of(e['w'])
        core = self.core_parts(i)
        cands = {}
        if e['g']:
            for k in self.groups.get(e['g'], []):
                cands[k] = 'g'
        for n, g in core:
            for k in self.part_index.get(n, []):
                if k not in cands and same_sense(g, dict(self._parts[k]).get(n, '')) and gloss_chars(g):
                    cands[k] = n
        rows = []
        for k, via in cands.items():
            w = self.entries[k]['w']
            kk = key_of(w)
            if k == i or kk == me or (pool is not None and kk not in pool):
                continue
            share = self.share_of(i, k)
            lw = kk.replace('-', '')
            s = (3 if via == 'g' else 0) + (3 if share else 0)
            if not share:
                sub = max((n for n, _ in core if len(n) >= 3 and n in lw), key=len, default='')
                if sub:
                    share, s = sub, s + 1
                elif via == 'g' and longest_common(me, lw) < 3:
                    s -= 1                                   # 一家，但看不出哪里像（perhaps 之于 happy）
            if prefer and kk in prefer:
                s += 3
            if lw.startswith(me) and len(lw) > len(me):
                s -= 2                                       # 本词加个后缀（transportation），没多学到什么
            elif me.startswith(lw.rstrip('e')) and len(lw) >= 3:
                s += 3                                       # 本词是从它来的（communicate 之于 communication、break 之于 breakfast）：最该写
            if re.search(r'[\s\-]', w) or w[:1].isupper():
                s -= 3                                       # 带空格、连字符的组合，专有名词
            s -= 0.05 * len(w)
            rows.append({'w': w, 'm': short_meaning(self.meaning(k)), 'via': 'group' if via == 'g' else 'part', 'share': share, 'score': round(s, 2)})
        rows.sort(key=lambda r: -r['score'])
        out = []
        for r in rows:
            if not any(variant_of(r['w'], x['w']) for x in out):
                out.append(r)
        # 默认写上黑板的 4 个：同一个共用部分最多 3 个（transport：import、export、report，再加一个 trans 的 transfer）
        picked, per = [], {}
        for r in out:
            key = r['share'] or '-'
            if per.get(key, 0) >= 3 and any((x['share'] or '-') != key for x in out if x not in picked):
                continue
            picked.append(r)
            per[key] = per.get(key, 0) + 1
            if len(picked) >= 4:
                break
        for r in out:
            r['pick'] = r in picked
        return out[:limit] + [r for r in out[limit:] if r['pick']]

    def normalize_extend(self, i, items, pool=None):
        """prefs.json 里手写的扩展词 → [{w, m, share}]；不在总表（或 pool）里的词挑出来"""
        out, bad = [], []
        for it in items or []:
            w = it if isinstance(it, str) else str((it or {}).get('w', ''))
            m = '' if isinstance(it, str) else str((it or {}).get('m', '') or '')
            k = key_of(w)
            hits = self.by_key.get(k)
            if not w.strip() or not hits or (pool is not None and k not in pool):
                bad.append(w)
                continue
            kidx = hits[0]
            out.append({'w': w.strip(), 'm': m or short_meaning(self.meaning(kidx)), 'share': self.share_of(i, kidx)})
        return out, bad

    def detail(self, w, pool=None, prefer=None):
        i, base = self.find(w)
        if i is None:
            return None
        e = self.entries[i]
        fields = []
        for j, t in e['f']:
            lab = self.labels[j]
            fields.append({'l': lab['l'], 's': lab['s'], 'role': lab['role'], 't': t})
        family, fam_idx = [], []
        if e['g']:
            for k in self.groups.get(e['g'], []):
                if self.entries[k]['w'] not in family:
                    family.append(self.entries[k]['w'])
                    fam_idx.append(k)
            # 背景只写在词族第一个词上：自己没写的，借族里写了的那个词的
            if not any(f['role'] == 'bg' and not PLACEHOLDER.match(f['t'].strip()) for f in fields):
                bg_lab = next((x for x in self.labels if x['role'] == 'bg'), None)
                for k in fam_idx:
                    t = self.text(self.entries[k], 'bg')
                    if t and k != i:
                        item = {'l': bg_lab['l'], 's': bg_lab['s'], 'role': 'bg', 't': t, 'from': self.entries[k]['w']}
                        order = [x['l'] for x in self.labels]
                        fields = [f for f in fields if f['role'] != 'bg']
                        pos = next((n for n, f in enumerate(fields) if order.index(f['l']) > order.index(bg_lab['l'])), len(fields))
                        fields.insert(pos, item)          # 放在“背景”那一列原来的位置
                        break
        fam_mean = {self.entries[k]['w']: self.meaning(k) for k in fam_idx if k != i}
        return {'w': e['w'], 'asked': str(w), 'fields': fields, 'family': family, 'g': e['g'], 'base': e['w'] if base else '',
                'family_meanings': fam_mean, 'others': [], 'extend': self.related(i, pool, prefer), 'syn': self.synonyms(i), 'demo': self.demos(i), 'near': self.near(i)}

    def near(self, i, n=6):
        """6.13 起：拼写、读音最像的几个词（视频“练习”的听力题拿来当干扰项：produce → product、protect、provide）。
        考纲里的词（「考点」列有字）优先；单词只和单词比，短语只和短语比"""
        import difflib
        w = self.entries[i]['w'].strip()
        lw, phrase = w.lower(), ' ' in w
        if not hasattr(self, '_near_pool'):
            self._near_pool = [(k, e['w'].strip(), bool(self.text(e, 'kaodian'))) for k, e in enumerate(self.entries)
                               if re.fullmatch(r"[A-Za-z][A-Za-z' -]*[A-Za-z]", e['w'].strip() or '')]
        out = []
        for k, x, kd in self._near_pool:
            lx = x.lower()
            if k == i or lx == lw or (' ' in x) != phrase or abs(len(x) - len(w)) > (6 if phrase else 3):
                continue
            r = difflib.SequenceMatcher(None, lw, lx).ratio() + (0.12 if lx[:2] == lw[:2] else 0) + (0.08 if kd else 0)
            if r >= (0.5 if phrase else 0.6) and not re.search(r'(的|之)(过去|复数|现在分词|比较级|最高级|第三人称)|的过去式|的缩写', self.meaning(k)):
                out.append((r, x, k))
        out.sort(key=lambda t: -t[0])
        seen, res = set(), []
        for r, x, k in out:
            if x.lower() in seen:
                continue
            seen.add(x.lower())
            res.append({'w': x, 'm': re.split(r'[：:]', self.meaning(k))[0]})
            if len(res) >= n:
                break
        return res

    def demos(self, i):
        """6.7 起：前缀、后缀那一行“。辨析：…”里每个用法括号的第一个例词（演示词），带上它自己那一行的含义、拆分、组合列第一行。
        视频“辨析”那一幕每个用法画一个“图 + 图 = 画”（preschool：pre（在…之前）+ school（学校）=“上学以前的”）"""
        e = self.entries[i]
        out = {}
        for j, t in e['f']:
            k0 = t.find('辨析：')
            if k0 < 0 or self.labels[j]['role'] == 'bianxi':
                continue
            for line in t.split('\n'):
                k = line.find('。辨析：')
                if k < 0:
                    continue
                core = line[k + 4:].split('；关系：')[0]
                for m in re.finditer(r"（([A-Za-z][A-Za-z'’\- 、]*)）", core):
                    w = m.group(1).split('、')[0].strip()
                    if w in out or ' ' in w:
                        continue
                    kk, _ = self.find(w)
                    if kk is None or self.entries[kk]['w'].lower() != w.lower():
                        continue
                    x = self.entries[kk]
                    logic = next((tt for jj, tt in x['f'] if self.labels[jj]['role'] == 'body' and tt.lstrip().startswith('【构词逻辑】')), '')
                    out[w] = {'m': self.meaning(kk), 'split': self.text(x, 'split'), 'logic1': logic.split('\n')[0] if logic else ''}
        return out

    def synonyms(self, i):
        """6.0 起：辨析列里提到的、总表里有的词（【同义词】行里的词、每个分句开头拿来比的词），带上它们自己那一行的材料：
        含义、拆分、组合列第一行（字面意思）、辨析。视频第三部分“同义词辨析”拿来做每个词的卡片"""
        e = self.entries[i]
        bx = self.text(e, 'bianxi')
        if not bx:
            return {}
        cand = []
        for line in bx.split('\n'):
            m = re.match(r'^【同义词】[^：]*：(.*)$', line)
            toks = re.findall(r"[A-Za-z][A-Za-z'\-]*", m.group(1) if m else line)
            for t in toks:
                if t not in cand and t.lower() != e['w'].lower():
                    cand.append(t)
        out = {}
        for t in cand:
            k, _ = self.find(t)
            if k is None or self.entries[k]['w'] != t or k == i:
                continue
            x = self.entries[k]
            logic = next((tt for j, tt in x['f'] if self.labels[j]['role'] == 'body' and tt.lstrip().startswith('【构词逻辑】')), '')
            out[t] = {'m': self.meaning(k), 'meaning': self.text(x, 'meaning'), 'split': self.text(x, 'split'),
                      'logic1': logic.split('\n')[0] if logic else '', 'bianxi': self.text(x, 'bianxi')}
            if len(out) >= 12:
                break
        return out


IRREG = {'went': 'go', 'gone': 'go', 'children': 'child', 'men': 'man', 'women': 'woman', 'feet': 'foot', 'teeth': 'tooth',
         'mice': 'mouse', 'geese': 'goose', 'people': 'person', 'did': 'do', 'done': 'do', 'was': 'be', 'were': 'be',
         'saw': 'see', 'seen': 'see', 'took': 'take', 'taken': 'take', 'gave': 'give', 'given': 'give', 'ate': 'eat', 'eaten': 'eat'}


def lemma_candidates(k):
    out = []
    if k in IRREG:
        out.append(IRREG[k])
    if k.endswith('ies') and len(k) > 4:
        out.append(k[:-3] + 'y')
    if k.endswith('es') and len(k) > 3:
        out.append(k[:-2])
    if k.endswith('s') and not k.endswith('ss') and len(k) > 3:
        out.append(k[:-1])
    if k.endswith('ied') and len(k) > 4:
        out.append(k[:-3] + 'y')
    if k.endswith('ed') and len(k) > 4:
        out += [k[:-2], k[:-1]]
    if k.endswith('ing') and len(k) > 5:
        out += [k[:-3], k[:-3] + 'e']
    return out


def opt(name):
    if name in sys.argv:
        k = sys.argv.index(name)
        val = sys.argv[k + 1]
        del sys.argv[k:k + 2]
        return val
    return None


def main():
    pool_arg, prefer_arg = opt('--pool'), opt('--prefer')
    pool = load_words(pool_arg) if pool_arg else None
    prefer = load_words(prefer_arg) if prefer_arg else None
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == 'build':
        build(sys.argv[2], sys.argv[3])
    elif cmd == 'detail':
        t = Table(sys.argv[2])
        words = [w.strip() for w in re.split(r'[,，]', sys.argv[3]) if w.strip()]
        out, missing = {}, []
        for w in words:
            d = t.detail(w, pool, prefer)
            if d:
                out[w] = d
            else:
                missing.append(w)
        json.dump(out, open(sys.argv[4], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('找到 %d 个：%s' % (len(out), ', '.join(w + ('（用原形 %s）' % d['base'] if d['base'] else '') for w, d in out.items())))
        if missing:
            print('表里没有 %d 个：%s' % (len(missing), ', '.join(missing)))
    elif cmd == 'related':
        t = Table(sys.argv[2])
        i, base = t.find(sys.argv[3])
        if i is None:
            sys.exit('表里没有 ' + sys.argv[3])
        print('%s 的扩展词候选（都在总表里%s；★ 是默认写上小黑板的）：' % (t.entries[i]['w'], '，也在 --pool 里' if pool is not None else ''))
        for r in t.related(i, pool, prefer, limit=20):
            print('  %s %-16s %-10s %s%s' % ('★' if r['pick'] else ' ', r['w'], r['m'], '同一组号' if r['via'] == 'group' else '别的组',
                                           ('，共用 ' + r['share']) if r['share'] else ''))
    elif cmd == 'find':
        t = Table(sys.argv[2])
        i, base = t.find(sys.argv[3])
        print('没有' if i is None else '第 %d 个词条：%s%s' % (i + 1, t.entries[i]['w'], '（原形）' if base else ''))
    else:
        print(__doc__)


if __name__ == '__main__':
    main()

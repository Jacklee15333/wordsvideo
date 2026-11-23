#!/usr/bin/env python3
"""考点列（2026-11 考纲考点轮，第 121 条；取代第 120 条“什么都写”的写法）。

用户：“考点要有依据，不是说我上面提到的都要写进去，就是你看上海初中英语，上面对应的这个词常见的考点是什么，
把这个词常见的考点，难点，易错点写好了就行了，不是说啥都要写进去，那样内容太多了”。

依据（详见 kaodian_data.py 开头）：
  S1 考纲词汇表（上海市教育考试院《2020年上海市初中英语课程终结性评价指南词汇表》，整理在 references/kaogang/kaogang.json）
  S2 评价指南（同一份指南的“知识内容”：词形变化、构词法、名词、代词、数词、比较级、时态、不定式、动名词……）
  S3 上海中考词性转换复习资料（二一教育网）；S4 上海中考、区模考“适当形式填空”原题

写不写：
  考纲里的词（表里 1742 行）——只写这个词真有的难点，没有就空着（camera、oven 这类空着）：
    【变形】考纲括号里标的不规则形式；没标但不规则的（spend、sing…）；双写、y 变 i、ie 变 y；名词加 es、o 结尾、
            f 变 v、man 变 men、单复数同形、只用复数、常考不可数（可数不可数两用的写清楚）；形容词不规则、双写、y 变 i；
            代词表、数词表（序数词、几十多岁）。规则的加 s、加 ed、加 er，多音节的 more / most 都不写。
    【词性转换】考纲里也有的同根词（总表“拆分”“单词部分”定的派生关系、② 变体关联、同前缀同词根），
            加上复习资料点名的（true → truly、depend → independent）；最多 3 个，真题、资料里有的排前面，再是词性变了的。
    【短语】考纲词组表里带这个词的，最多 3 个，常考的排前面。
    【用法】kaodian_data.USAGE（动名词、不定式、短暂动词、花费、句型转换的同义替换……）。
    【易混】kaodian_data.CONFUSE（already / yet、remember / remind……）。
  考纲外的词——只有由考纲词加前后缀变来、又常用（或资料、真题里有）的，写一条“true → truly（去 e 加 ly，易错）”；
            考纲词的变形（went、written、teeth）写“go 的过去式”。别的都不写。
  每一行的出处 kaodian() 也一起算出来（同样的【标签】、同样的顺序），--show 时打印出来核对；不写进总表（用户：“考点依据不用加了”）。

  python3 kaodian.py <总表.xlsx> --show produce,suggest,truly        # 看几个词写出来是什么样（连依据）
  python3 kaodian.py <总表.xlsx> --write <新表.xlsx>                  # 整列重写「考点」（表里没有这一列就加一列）
  python3 kaodian.py <新表.xlsx> --check                               # 体检：格式、标签
"""
import argparse, json, os, re, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kaodian_data as D  # noqa: E402

KG_PATH = os.path.join(HERE, '..', 'references', 'kaogang', 'kaogang.json')
LABELS = ('变形', '词性转换', '短语', '用法', '易混')
MAXN = {'词性转换': 3, '短语': 3, '用法': 2, '易混': 2}
VOW = 'aeiou'
CONTENT = ('n.', 'v.', 'adj.', 'adv.')


def zipf(w):
    try:
        from wordfreq import zipf_frequency
        return zipf_frequency(w, 'en')
    except Exception:
        return 4.0


def infl(w, tag):
    try:
        from lemminflect import getInflection
        r = getInflection(w, tag)
        return r[0] if r else None
    except Exception:
        return None


# ---------------------------------------------------------------- 考纲
class KG:
    def __init__(self, path=KG_PATH):
        d = json.load(open(path, encoding='utf-8'))
        self.W, self.P = d['words'], d['phrases']
        for p in self.P:
            p['toks'] = self.toks(p['p'])

    @staticmethod
    def toks(phrase):
        s = phrase.lower().replace('’', "'").replace('…', ' ').replace('...', ' ')
        return set(re.findall(r"[a-z][a-z'\-]*", s))

    def get(self, w):
        return self.W.get(str(w).strip().lower())

    POS_FIX = {'inventor': 'n.', 'terrible': 'adj.', 'seriously': 'adv.'}   # 考纲原文这三处词性印错了（inventor v.、terrible n.、seriously adj.）

    def pos(self, w):
        e = self.get(w)
        if str(w).lower() in self.POS_FIX:
            return [self.POS_FIX[str(w).lower()]]
        out = []
        for p in (e or {}).get('pos', []):
            for x in re.split(r'\s*&\s*', p[0]):
                x = x.strip()
                x = {'vt.': 'v.', 'vi.': 'v.', 'link': 'v.', 'aux. v.': 'aux.', 'aux': 'aux.'}.get(x, x)
                if x and x not in out:
                    out.append(x)
        return out

    def zh(self, w, pos=None):
        """考纲里的中文，取第一个意思（括号里的说明去掉）"""
        e = self.get(w)
        if not e:
            return ''
        for p in e['pos']:
            if pos and pos not in [x.strip() for x in re.split(r'&', p[0])] and not (pos == 'v.' and re.search(r'v\.|link', p[0])):
                continue
            t = re.sub(r'[（(][^（）()]*[)）]', '', p[1]).strip()
            t = re.split(r'[；;，,]', t)[0].strip()
            if t:
                return t
        return ''

    def page(self, w):
        e = self.get(w)
        return e.get('page') if e else None

    def ref(self, *ws):
        """“考纲第 61 页 suggest、suggestion”这种出处"""
        pg = []
        for w in ws:
            p = self.page(w)
            if p and p not in pg:
                pg.append(p)
        return '考纲词汇表第 %s 页 %s' % ('、'.join(str(p) for p in pg), '、'.join(ws)) if pg else '考纲词汇表 ' + '、'.join(ws)


# ---------------------------------------------------------------- 总表
class Table:
    def __init__(self, path):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        ws = wb['拆分结果']
        self.rows = [list(r) for r in ws.iter_rows(values_only=True)]
        self.hdr = [str(h) if h is not None else '' for h in self.rows[0]]
        self.ix = {h: i for i, h in enumerate(self.hdr)}
        self.data = self.rows[1:]
        self.words = {}
        for n, r in enumerate(self.data):
            w = self.v(r, '单词').strip()
            if w and w.lower() not in self.words:
                self.words[w.lower()] = n
        self._graph()

    def v(self, r, h):
        i = self.ix.get(h)
        return '' if i is None or i >= len(r) or r[i] is None else str(r[i])

    def meaning_pos(self, w):
        n = self.words.get(w.lower())
        if n is None:
            return None, ''
        for ln in self.v(self.data[n], '含义').split('\n'):
            m = re.match(r'^\s*((?:modal |aux\. )?[a-z]+\.)\s*(.*)$', ln)
            if m and m.group(1) in CONTENT:
                return m.group(1), re.split(r'[；、，]', re.sub(r'（[^）]*）', '', m.group(2)))[0].strip()
        return None, ''

    def _graph(self):
        """派生关系：parent[孩子] = [(母词, 种类)]，种类 suf / pre / var / comp"""
        self.parent = defaultdict(list)
        self.child = defaultdict(list)
        self.affix = {}
        for n, r in enumerate(self.data):
            w = self.v(r, '单词').strip().lower()
            sp = self.v(r, '拆分').split('；')[0].strip()
            if not w or not sp or sp in ('—', '-'):
                continue
            if '≈' in sp or '←' in sp:
                for x in re.split(r'[≈←]', sp)[1:]:
                    b = re.sub(r'[（(].*$', '', x).strip().lower()
                    if b in self.words and b != w:
                        self._add(b, w, 'var')
                continue
            bases = []
            for ln in self.v(r, '单词部分').split('\n'):
                m = re.match(r'^\s*([A-Za-z][A-Za-z\'\- ]*?)\s*[：:]', ln)
                if not m:
                    continue
                see = re.search(r'见 ([A-Za-z][A-Za-z\'\- ]*?)[）)]', ln)
                b = (see.group(1) if see else m.group(1)).strip().lower()
                if b in self.words and b != w and b not in bases:
                    bases.append(b)
            parts0 = sp.split(' + ')
            m0 = re.match(r'^\s*([A-Za-z]+)\(=([A-Za-z]+)\)\s*$', parts0[0]) if len(parts0) == 2 else None
            if m0:                                                # production：product(=produce) + ion；examination：examinat(=examine) + ion
                first, a = m0.group(1).lower(), m0.group(2).lower()
                if a in self.words and a != w and a not in bases:
                    bases.append(a)
                if first in self.words and first != w and first not in bases:
                    bases.append(first)
            pre, suf = self.v(r, '前缀').strip(), self.v(r, '后缀').strip()
            empty = ('', '-', '—')
            kind = 'pre' if pre not in empty else 'suf' if suf not in empty else 'comp'
            first = re.sub(r'\(.*?\)', '', sp.split(' + ')[0]).strip().lower()
            for b in bases:
                self._add(b, w, kind)
            self.affix[w] = first if kind == 'pre' else re.sub(r'\(.*?\)', '', sp.split(' + ')[-1]).strip().lower()

    def _add(self, b, w, kind):
        if (b, kind) not in self.parent[w]:
            self.parent[w].append((b, kind))
            self.child[b].append((w, kind))

    def prefix_root(self, w):
        """pro + duce(=duc) → ('pro', 'duc')"""
        n = self.words.get(w)
        if n is None:
            return None
        s = self.v(self.data[n], '拆分').split('；')[0].split(' + ')
        if len(s) != 2:
            return None
        m = re.search(r'\(=([^)]+)\)', s[1])
        return s[0].strip().lower(), (m.group(1) if m else s[1]).strip().lower()


# ---------------------------------------------------------------- 拼写规则
def spell_note(base, der):
    """base → der 的拼写变化（只认简单的几种）"""
    b, d = base.lower(), der.lower()
    if d.startswith(b):
        if len(d) > len(b) + 1 and d[len(b)] == b[-1] and b[-1] not in VOW + 'wxy' and len(b) >= 3 and b[-2] in VOW and b[-3] not in VOW \
                and (len(re.findall(r'[aeiou]+', b)) == 1 or b in ('begin', 'forget', 'prefer', 'control', 'admit', 'regret', 'permit', 'travel')):
            return '双写 %s' % b[-1]
        return ''
    if b.endswith('y') and d.startswith(b[:-1] + 'i') and d[len(b):] in ('es', 'ed', 'er', 'est', 'ness', 'ly', 'ful', 'ment', 'ous', 'an', 'ance', 'ar'):
        return 'y 变 i'
    if b.endswith('le') and d == b[:-1] + 'y':
        return '去 e 加 y'
    if b.endswith('e') and d.startswith(b[:-1]) and not d.startswith(b):
        return '去 e'
    return ''


SPECIAL_CONV_NOTE = {('true', 'truly'): '去 e 加 ly，易错', ('nine', 'ninth'): '去 e 加 th，易错', ('argue', 'argument'): '去 e，易错',
                     ('four', 'forty'): '去 u，易错', ('strange', 'stranger'): '名词“陌生人”，也是 strange 的比较级'}


# ---------------------------------------------------------------- 变形
PRON_SET = {
    'I': ('me', 'my', 'mine', 'myself'), 'you': ('you', 'your', 'yours', 'yourself / yourselves'), 'he': ('him', 'his', 'his', 'himself'),
    'she': ('her', 'her', 'hers', 'herself'), 'it': ('it', 'its', 'its', 'itself'), 'we': ('us', 'our', 'ours', 'ourselves'),
    'they': ('them', 'their', 'theirs', 'themselves'),
}
COUNTRY_ZH = {'America': '美国', 'Australia': '澳大利亚', 'Britain': '英国', 'Canada': '加拿大', 'China': '中国', 'England': '英格兰',
              'France': '法国', 'Germany': '德国', 'Italy': '意大利', 'Japan': '日本', 'Asia': '亚洲', 'Africa': '非洲', 'Europe': '欧洲',
              'American': '美国的', 'Australian': '澳大利亚的', 'British': '英国的', 'Canadian': '加拿大的', 'Chinese': '中国的',
              'English': '英国的、英语的', 'French': '法国的', 'German': '德国的', 'Italian': '意大利的', 'Japanese': '日本的',
              'Asian': '亚洲的', 'African': '非洲的', 'European': '欧洲的', 'Briton': '英国人'}
ORD_NOTE = {'one': ('first', '不规则'), 'two': ('second', '不规则'), 'three': ('third', '不规则'), 'five': ('fifth', 've 变 f，易错'),
            'eight': ('eighth', '只加 h，易错'), 'nine': ('ninth', '去 e 加 th，易错'), 'twelve': ('twelfth', 've 变 f，易错')}


def ann_forms(e):
    """考纲括号里的动词变化：'began, begun' / 'learnt，learnt；learned，learned' / 'burned, burned 或 burnt, burnt'"""
    cands = [e.get('note', '')]
    for p in e.get('pos', []):
        if len(p) > 2:
            cands.append(p[2])
        m = re.match(r'^\(([a-z ,，/或；]+)\)', p[1])
        if m and re.search(r'v\.', p[0]):
            cands.append(m.group(1))
    for c in cands:
        if c and re.match(r'^[a-z]', c) and not c.startswith(('美', '=')):
            return c
    return ''


def verb_line(w, e, K):
    """动词的难点 → (小块列表, 依据)"""
    chips, basis = [], ''
    if w == 'be':
        return ['现在时 am、is、are', '过去式 was、were', '过去分词 been'], K.ref('be') + '的注释'
    if w in ('can', 'may', 'shall'):
        return ['过去式 %s' % e['note']], K.ref(w) + '标注 (%s)' % e['note']
    if w == 'hang' or w == 'lie':
        return [D.VERB_NOTE[w]], K.ref(w) + '（两个意思两套变化）'
    a = ann_forms(e)
    if a:
        alts = [x.strip() for x in re.split(r'；|\s或\s', a) if x.strip()]
        pairs = [tuple(y.strip() for y in re.split(r'[,，]', x)) for x in alts]
        pasts = []
        for p in pairs:
            if len(p) == 2:
                pasts.append(p)
        if pasts:
            if all(p[0] == p[1] for p in pasts):
                chips.append('过去式、过去分词 %s（不规则）' % ' 或 '.join(p[0] for p in pasts))
            else:
                ps = ' 或 '.join(dict.fromkeys(p[0] for p in pasts))
                pp = ' 或 '.join(dict.fromkeys(p[1] for p in pasts))
                chips.append('过去式 %s、过去分词 %s（不规则）' % (ps, pp))
            basis = K.ref(w) + '标注 (%s)' % a
    else:
        past, pp = infl(w, 'VBD'), infl(w, 'VBN')
        regular = past and (past in (w + 'ed', w + 'd') or (w.endswith('y') and past == w[:-1] + 'ied') or past == w + w[-1] + 'ed')
        if past and not regular:
            chips.append(('过去式、过去分词 %s（不规则）' % past) if past == pp else ('过去式 %s、过去分词 %s（不规则）' % (past, pp)))
            basis = K.ref(w) + '（考纲没标，但是不规则动词）'
        elif past == w + w[-1] + 'ed' and w not in ('equal',):
            chips.append('过去式、过去分词 %s；现在分词 %s（双写 %s）' % (past, w + w[-1] + 'ing', w[-1]))
            basis = K.ref(w) + '；评价指南·词形变化（双写）'
        elif w.endswith('y') and len(w) > 2 and w[-2] not in VOW:
            chips.append('过去式、过去分词 %s；三单 %s（y 变 i）' % (w[:-1] + 'ied', w[:-1] + 'ies'))
            basis = K.ref(w) + '；评价指南·词形变化（y 变 i）'
    ing = infl(w, 'VBG')
    if a and ing and ing == w + w[-1] + 'ing':
        chips.append('现在分词 %s（双写 %s）' % (ing, w[-1]))
    if a and w.endswith('y') and w[-2] not in VOW:
        chips.append('三单 %s（y 变 i）' % (w[:-1] + 'ies'))
    if w in ('do', 'go'):
        chips.append('三单 %s' % (w + 'es'))
    if w == 'have':
        chips.append('三单 has')
    if w in D.VERB_NOTE:
        chips.append(D.VERB_NOTE[w])
        basis = basis or K.ref(w)
    if w == 'read':
        chips = ['过去式、过去分词 read（拼写不变，读音变成 /red/）']
    return chips, basis


def noun_line(w, e, K, main):
    """名词的难点。main：名词是不是考纲里第一个词性（不是的话只写特别的复数）"""
    note = e.get('note', '')
    m = re.match(r'^复(?:数)?\s*(.+)$', note)
    if m:
        return ['复数 %s（不规则）' % m.group(1).strip()] if m.group(1).strip() != w else ['单复数同形'], K.ref(w) + '标注 (%s)' % note
    key = e.get('w', w)
    if key in D.SAME_FORM or w in D.SAME_FORM:
        return [D.SAME_FORM.get(key) or D.SAME_FORM[w]], K.ref(w) + '；评价指南·名词复数'
    if key in D.PL_TRAP:
        return [D.PL_TRAP[key]], K.ref(w) + '；上海中考复习资料（German 复数 Germans）'
    if w in D.PLURAL_ONLY:
        return [D.PLURAL_ONLY[w]], K.ref(w) + '；评价指南·名词复数'
    if w in D.BOTH:
        return [D.BOTH[w]], K.ref(w) + ('的注释' if w in ('paper', 'glass') else '') + '；评价指南·可数、不可数名词'
    if w in D.UNCOUNT:
        t = '不可数' + ('：' + D.UNCOUNT[w] if D.UNCOUNT[w] else '，没有复数')
        return [t], K.ref(w) + '；评价指南·不可数名词'
    pl = infl(w, 'NNS')
    if w.endswith('man') and w not in ('human', 'german'):
        return ['复数 %s（man 变 men）' % (w[:-3] + 'men')], K.ref(w) + '；评价指南·名词复数（S4：2018 上海中考 policemen、2023 闵行二模 firemen）'
    if w == 'quiz':
        return ['复数 quizzes（双写 z 加 es，易错）'], K.ref(w) + '；评价指南·名词复数'
    if w.endswith('o'):
        if w in D.O_ES:
            return ['复数 %ses（加 es）' % w], K.ref(w) + '；上海中考复习资料（hero → heroes）'
        if w in ('photo', 'piano', 'radio', 'video', 'zoo', 'zero'):
            return ['复数 %ss（只加 s）' % w], K.ref(w) + '；上海中考复习资料（piano → pianos）'
        return [], ''
    if not main and not w.endswith(('f', 'fe', 'man')):
        return [], ''
    if re.search(r'[^aeiou]y$', w) and pl == w[:-1] + 'ies':
        return ['复数 %s（y 变 i 加 es）' % pl], K.ref(w) + '；评价指南·名词复数（S4：2023 长宁一模 libraries、2024 宝山一模 dictionaries）'
    if w in D.VOWEL_Y and w not in ('boy', 'day', 'way', 'birthday'):
        return ['复数 %ss（元音字母 + y，直接加 s）' % w], K.ref(w) + '；评价指南·名词复数（S4：2023 松江二模 toys）'
    if w.endswith(('f', 'fe')) and pl and pl.endswith('ves'):
        return ['复数 %s（f 变 v 加 es）' % pl], K.ref(w) + '；评价指南·名词复数'
    if re.search(r'(s|x|ch|sh)$', w) and pl == w + 'es' and not w.endswith(('ness', 'ics')) and w not in ('success', 'business', 'stress', 'research', 'chess', 'rubbish', 'christmas', 'progress', 'process'):
        return ['复数 %s（加 es）' % pl], K.ref(w) + '；评价指南·名词复数（S4：2019 上海中考 boxes）'
    return [], ''


def adj_line(w, e, K):
    note = e.get('note', '')
    m = re.match(r'^比较级\s*(.+?)[，,]\s*最高级\s*(.+)$', note)
    if w == 'far':
        return ['比较级 farther / further、最高级 farthest / furthest（不规则）'], K.ref(w) + '标注'
    if m:
        return ['比较级 %s、最高级 %s（不规则）' % (m.group(1).strip(), m.group(2).strip())], K.ref(w) + '标注 (%s)' % note
    if w == 'much':
        return ['比较级 more、最高级 most（不规则）'], K.ref(w) + '标注 (more, most)'
    if w in D.ADJ_IRREG_EXTRA:
        c, s, t = D.ADJ_IRREG_EXTRA[w]
        return ['比较级 %s、最高级 %s（%s）' % (c, s, t)], K.ref(w, 'elder') + '；评价指南·比较级'
    if w in D.ADJ_DOUBLE:
        return ['比较级 %s、最高级 %s（双写 %s）' % (w + w[-1] + 'er', w + w[-1] + 'est', w[-1])], K.ref(w) + '；评价指南·比较级的构成'
    if w in D.ADJ_Y:
        return ['比较级 %s、最高级 %s（y 变 i）' % (w[:-1] + 'ier', w[:-1] + 'iest')], K.ref(w) + '；评价指南·比较级的构成'
    return [], ''


def inflected_row(w, K):
    """考纲里标成“…的比较级 / 过去分词”的词（better、born、stuck、should），和考纲词的不规则变化（went、written、teeth）"""
    e = K.get(w)
    MODAL_PAST = {'could': 'can', 'might': 'may', 'would': 'will', 'should': 'shall'}
    if w in MODAL_PAST:
        b = MODAL_PAST[w]
        return '%s 的过去式' % b, K.ref(b if K.get(b) else w) + ('标注 (%s)' % w if K.get(b) and K.get(b).get('note') == w else '的注释')
    if e:
        note = e.get('note', '')
        m = re.match(r'^(.+?)\s*的(比较级|最高级)$', note)
        if m:
            base = m.group(1).replace(' 或 ', '、').replace(', ', '、').replace('，', '、')
            other = {'better': 'best', 'best': 'better', 'more': 'most', 'most': 'more'}.get(w, '')
            return '%s 的%s（%s %s）' % (base, m.group(2), '最高级' if m.group(2) == '比较级' else '比较级', other), K.ref(w) + '标注 (%s)' % note
        if w == 'born':
            return 'bear 的过去分词；be born 出生', K.ref(w) + '标注 (动词 bear 的过去分词)；考纲词组表第 73 页 be born'
        if w == 'stuck':
            return 'stick 的过去式、过去分词', K.ref(w)
        if w == 'lost':
            return 'lose 的过去式、过去分词；也作形容词', K.ref('lose', 'lost')
        return None
    # 考纲外：考纲词的不规则变化
    for base, be in K.W.items():
        if be.get('alias_of'):
            continue
        m = re.match(r'^复(?:数)?\s*(.+)$', be.get('note', ''))
        if m and m.group(1).strip() == w and w != base:
            return '%s 的复数（不规则）' % base, K.ref(base) + '标注 (%s)' % be['note']
        a = ann_forms(be) if be.get('pos') else ''
        if not a:
            continue
        forms = [x.strip() for x in re.split(r'[,，；/]|\s或\s', a) if x.strip()]
        if w in forms and w != base:
            pairs = [x.strip() for x in re.split(r'；|\s或\s', a)]
            p = [y.strip() for y in re.split(r'[,，]', pairs[0])]
            if len(p) == 2:
                kinds = []
                if w == p[0]:
                    kinds.append('过去式')
                if w == p[1]:
                    kinds.append('过去分词')
                if kinds:
                    rest = ('过去分词 %s' % p[1]) if kinds == ['过去式'] else ('过去式 %s' % p[0]) if kinds == ['过去分词'] else ''
                    return '%s 的%s%s' % (base, '、'.join(kinds), '（%s）' % rest if rest else ''), K.ref(base) + '标注 (%s)' % a
        m = re.match(r'^复(?:数)?\s*(.+)$', be.get('note', ''))
        if m and m.group(1).strip() == w and w != base:
            return '%s 的复数（不规则）' % base, K.ref(base) + '标注 (%s)' % be['note']
    return None


def pron_line(w, e, K):
    base = e.get('pron_base')
    if not base:
        return [], ''
    o, a, n, r = PRON_SET[base]
    ref = '考纲词汇表第 84 页 代词表'
    if w.lower() == base.lower():
        w = base
        chips = ['宾格 %s' % o] if o != w else []
        chips.append('物主代词 %s' % (a if a == n else '%s、%s' % (a, n)))
        chips.append('反身代词 %s' % r)
        if w == 'it':
            chips[-2] = '物主代词 its（不是 it\'s，易错）'
        return chips, ref
    if w in ('itself',):
        return ['it 的反身代词（复数 themselves）', '物主代词 its（不是 it\'s，易错）'], ref + '；S4：2021 上海中考 (it) → its'
    if e.get('pron') == '反身代词':
        return ['%s 的反身代词' % base], ref + ('；S4：2018 上海中考 (she) → herself' if w == 'herself' else '')
    return ['%s 的%s' % (base, e['pron'])], ref


def num_line(w, e, K):
    ref = '考纲词汇表第 85、86 页 基数词和序数词表'
    if e.get('ordinal') and w != 'hundred':
        o = e['ordinal']
        c = ['序数词 %s' % o + ('（%s）' % ORD_NOTE[w][1] if w in ORD_NOTE else '')]
        if w == 'one':
            c.append('次数 once')
        if w == 'two':
            c.append('次数 twice')
        if w == 'four':
            c.append('四十 forty（去 u，易错）')
        if re.search(r'ty$', w):
            c[0] = '序数词 %s（y 变 ie 加 th）' % o
            c.append('in one\'s %sies 在某人%s多岁时' % (w[:-1], {'twenty': '二十', 'thirty': '三十', 'forty': '四十', 'fifty': '五十', 'sixty': '六十', 'seventy': '七十', 'eighty': '八十', 'ninety': '九十'}.get(w, '')))
        ex = [v for (g, a2), v in D.SH_EXAM.items() if g == w]
        return c, ref + ('；S4：' + '；'.join(ex) if ex else '')
    if e.get('cardinal'):
        c = e['cardinal']
        note = ORD_NOTE.get(c, (None, ''))[1] or ('y 变 ie 加 th' if c.endswith('ty') else '')
        ex = [v for (g, a2), v in D.SH_EXAM.items() if a2 == w]
        return ['%s 的序数词%s' % (c, '（%s）' % note if note else '')], ref + ('；S4：' + '；'.join(ex) if ex else '')
    return [], ''


# ---------------------------------------------------------------- 词性转换
def sh_pairs():
    out = {}
    for a, b in D.SH_CONV:
        out[(a.lower(), b.lower())] = 'S3'
    for (a, b), v in D.SH_EXAM.items():
        out[(a.lower(), b.lower())] = v
    return out


SHP = sh_pairs()
INFL_EXAM = {('box', 'boxes'), ('eight', 'eighth'), ('stamp', 'stamps'), ('six', 'sixth'), ('she', 'herself'), ('policeman', 'policemen'),
             ('it', 'its'), ('dictionary', 'dictionaries'), ('nine', 'ninth'), ('bad', 'worse'), ('twenty', 'twenties'), ('her', 'hers'),
             ('library', 'libraries'), ('fireman', 'firemen'), ('toy', 'toys'), ('glove', 'gloves')}
for _p in INFL_EXAM:
    SHP.pop(_p, None)


def pair_src(a, b):
    return SHP.get((a, b)) or SHP.get((b, a))


NEG_PRE = ('un', 'dis', 'im', 'in', 'il', 'ir', 'non')
# ② 变体关联里算“词性转换”的（资料 S3 里有的已经在 SH_CONV；这里是考纲两头都有、课本里常讲的）
VAR_OK = {('think', 'thought'), ('sing', 'song'), ('dead', 'death'), ('live', 'life'), ('strong', 'strength'),
          ('grow', 'growth'), ('lose', 'loss'), ('believe', 'belief'), ('prove', 'proof')}
PERSON_SUF = ('er', 'or', 'ist', 'ian', 'an', 'ess', 'ress', 'ee', 'eer', 'yer', 'zen')


def posset(T, K, w):
    p = set(x for x in K.pos(w) if x in CONTENT)
    if not p:
        mp = T.meaning_pos(w)[0]
        if mp:
            p = {mp}
    return p


def pos1(T, K, w):
    """考纲里第一个实词词性（考纲没有就看总表含义的第一行）"""
    p = [x for x in K.pos(w) if x in CONTENT]
    return p[0] if p else T.meaning_pos(w)[0]


SUF_BASE_OK = {'ful': ('n.', 'v.'), 'less': ('n.', 'v.'), 'y': ('n.', 'v.'), 'ous': ('n.',), 'al': ('n.',), 'ial': ('n.',), 'ical': ('n.',),
               'ly': ('adj.', 'n.'), 'ness': ('adj.',), 'ity': ('adj.',), 'dom': ('adj.', 'n.'), 'ment': ('v.',), 'ion': ('v.',), 'tion': ('v.',),
               'ation': ('v.',), 'sion': ('v.',), 'able': ('v.', 'n.'), 'ible': ('v.', 'n.'), 'ive': ('v.', 'n.'), 'ance': ('v.',), 'ence': ('v.',),
               'ing': ('v.',), 'ed': ('v.', 'n.'), 'en': ('adj.', 'n.'), 'ern': ('n.', 'adj.'), 'ure': ('v.',), 'ize': ('n.', 'adj.')}
# -ed / -ing 当形容词的，只认“说感受”的这些动词（excited / exciting）；别的 -ed（wanted）不算
EMOTION = set('amaze annoy bore confuse disappoint embarrass excite frighten interest please relax satisfy surprise tire worry shock '
              'puzzle terrify encourage touch move amuse astonish depress exhaust delight scare'.split())


ZH_STOP = set('的地得人者性化一不使被有了可能是等物事东西方式之所以把对在于为与和或也又很更最大小上下中')
ING_OK = {'feeling', 'reading', 'writing', 'drawing', 'warning', 'swimming', 'living', 'shopping', 'running', 'meeting', 'painting',
          'building', 'beginning', 'meaning', 'learning', 'singing', 'dancing'}


def zh_all(T, K, w):
    """这个词所有的中文（考纲 + 总表含义），用来看两个词意思接不接得上"""
    e = K.get(w)
    t = ' '.join(p[1] for p in e['pos']) if e else ''
    n = T.words.get(w)
    if n is not None:
        t += ' ' + T.v(T.data[n], '含义').split('\n')[0]
    return set(ch for ch in t if '\u4e00' <= ch <= '\u9fff') - ZH_STOP


def same_meaning(T, K, base, der):
    """派生词的意思和母词接得上（race 比赛 / racial 种族的、idea 主意 / ideal 理想的 不算）"""
    return bool(zh_all(T, K, base) & zh_all(T, K, der))


# 派生关系对、但意思离得远或中考不考的（逐个看过）
BAD_PAIRS = {('idea', 'ideal'), ('provide', 'provision'), ('part', 'partial'), ('collect', 'collective'), ('fable', 'fabulous'),
             ('form', 'formal'), ('include', 'inclusion'), ('operation', 'operational'), ('blood', 'bloody'), ('try', 'trial'),
             ('kill', 'killer'), ('serve', 'server'), ('walk', 'walker'), ('rock', 'rocky'), ('enter', 'entry'), ('settle', 'settlement'),
             ('compare', 'comparable'), ('sense', 'sensitive'), ('progress', 'progressive'), ('available', 'availability'),
             ('human', 'humanity'), ('relative', 'relatively'), ('historical', 'historically'), ('technology', 'technological'),
             ('mathematics', 'mathematical'), ('biology', 'biological'), ('official', 'officially'), ('private', 'privately'),
             ('local', 'locally'), ('primary', 'primarily'), ('necessary', 'necessarily'), ('new', 'newly'), ('open', 'openly'),
             ('public', 'publicly'), ('apply', 'applicable'), ('receive', 'reception'), ('face', 'facial'), ('reduce', 'reduction'),
             ('prevent', 'prevention'), ('require', 'requirement'), ('good', 'goodness'), ('exist', 'existence'), ('type', 'typical'),
             ('support', 'supportive'), ('protect', 'protective'), ('product', 'productive'), ('effect', 'effective'), ('most', 'mostly')}


def edge_ok(T, K, base, der, kind):
    """base → der 这一步算不算“词性转换”的考点"""
    if (base, der) in BAD_PAIRS:
        return False
    if pair_src(base, der) or (base, der) in VAR_OK or (der, base) in VAR_OK:
        return True
    if kind == 'pre':
        if T.affix.get(der) not in NEG_PRE:
            return False
        zh = K.zh(der) or T.meaning_pos(der)[1]
        return bool(re.match(r'^(不|没|无|非|难|未)', zh))      # discover“发现”不算
    if kind == 'var':
        return False
    if kind == 'suf':
        suf = T.affix.get(der)
        if suf in ('s', 't', 'th', 'et', 'let', 'ling', 'ie', 'y(=ie)') or suf == 'ce' and not base.endswith('nt'):
            return False
        if suf in PERSON_SUF:
            zh = K.zh(der) or T.meaning_pos(der)[1]
            if (base, der) in SPECIAL_CONV_NOTE:
                return True                                       # strange → stranger
            bp = K.pos(base) or [pos1(T, K, base)]
            if not any(p in ('v.', 'n.') for p in bp):
                return False
            if K.get(der) and K.get(base):
                return True                                       # 两头都在考纲里（farm → farmer、report → reporter）
            return bool(re.search(r'[人者家员师手生工商官长主客匠匪迷民机]', zh)) and zipf(der) >= 4.4 \
                and same_meaning(T, K, base, der)                 # 考纲外的：poster“海报”、keeper 不算
        if suf in ('ed', 'ing') and base not in EMOTION and not (K.get(der) or der in ING_OK):
            return False                                          # publishing、thinking、finding 不算；feeling、reading 算
        ok = SUF_BASE_OK.get(suf)
        if ok and not any(p in ok for p in (K.pos(base) or [pos1(T, K, base)])):
            return False                                          # would → willing 这种不算
        return pos1(T, K, base) != pos1(T, K, der) and same_meaning(T, K, base, der)   # 词性变了、意思接得上才算
    return False                                                  # 合成词（under + stand、bath + room）不算


def related(T, K, w):
    """考纲里和 w 同根、算得上“词性转换”的词：{词: (方向, 层数, 种类)}"""
    out = {}
    for b, kind in T.parent.get(w, []):
        if edge_ok(T, K, b, w, kind):
            out.setdefault(b, ('up', 1, kind))
            if kind == 'var':                                     # 兄弟：dead ← die → death
                for c, k2 in T.child.get(b, []):
                    if k2 == 'var' and c != w and edge_ok(T, K, b, c, 'var'):
                        out.setdefault(c, ('side', 1, 'var'))
    for c, kind in T.child.get(w, []):
        if not edge_ok(T, K, w, c, kind):
            continue
        out.setdefault(c, ('down', 1, kind))
        if K.get(c) and kind == 'suf':                            # 再往下一层（care → careful → carefully），中间那个也要在考纲里
            for g, k2 in T.child.get(c, []):
                if g != w and k2 == 'suf' and edge_ok(T, K, c, g, k2):
                    out.setdefault(g, ('down', 2, k2))
    PAIRS = (('ent', 'ence'), ('ant', 'ance'), ('ence', 'ent'), ('ance', 'ant'))
    for b, kind in T.parent.get(w, []):                           # 同一个母词的 -ent / -ence（confident / confidence）
        for c, k2 in T.child.get(b, []):
            if c != w and kind == k2 == 'suf' and (T.affix.get(w), T.affix.get(c)) in PAIRS:
                out.setdefault(c, ('side', 1, 'pair'))
    if pos1(T, K, w) == 'adj.':                                   # 考纲里有、总表里没有的 -ly 副词（quick → quickly）
        for c in (w + 'ly', w[:-1] + 'ily' if w.endswith('y') else '', w[:-1] + 'y' if w.endswith('le') else ''):
            if c and K.get(c) and c not in out:
                out[c] = ('down', 1, 'ly')
    pr = T.prefix_root(w)                                         # 同前缀同词根、词性不同：produce / product
    if pr and len(pr[0]) <= 4:
        for c in K.W:
            if c != w and c in T.words and T.prefix_root(c) == pr and not (posset(T, K, c) & posset(T, K, w)):
                out.setdefault(c, ('side', 1, 'root'))
    for (a, b) in SHP:                                            # 资料、真题里的（表里没连上的也算）
        if a == w and b in T.words:
            out.setdefault(b, ('down', 1, 'sh'))
        if b == w and a in T.words:
            out.setdefault(a, ('up', 1, 'sh'))
    return out


SHOW_POS = ('v.', 'n.', 'adj.', 'adv.')


SUF_BASE = {'ful': 'n.', 'less': 'n.', 'y': 'n.', 'ous': 'n.', 'al': 'n.', 'ial': 'n.', 'ly': 'adj.', 'ness': 'adj.', 'ity': 'adj.',
            'th': 'adj.', 'dom': 'adj.', 'er': 'v.', 'or': 'v.', 'ment': 'v.', 'ion': 'v.', 'tion': 'v.', 'ation': 'v.', 'able': 'v.',
            'ive': 'v.', 'ance': 'v.', 'ence': 'v.', 'ing': 'v.', 'ed': 'v.', 'ist': 'n.', 'ian': 'n.', 'ship': 'n.', 'en': 'adj.'}


def show_pos(T, K, c, mine, child=None):  # noqa
    """related 词画面上写哪个词性：c 是本词的母词时写派生用的那个词性（careful 的 care 写 n.），
    别的写和本词不一样的那个（owner 的 own 写 v.）"""
    ps = [p for p in K.pos(c) if p in CONTENT] or [T.meaning_pos(c)[0]]
    if child:
        want = SUF_BASE.get(T.affix.get(child, ''))
        if want in ps:
            return want
    diff = [p for p in SHOW_POS if p in ps and p not in mine]
    return diff[0] if diff else ps[0]


def conv_line(T, K, w):
    """考纲词的【词性转换】→ (小块, 依据)"""
    mine = posset(T, K, w)
    cands = []
    for c, (dirn, depth, kind) in related(T, K, w).items():
        src = pair_src(w, c)
        if not K.get(c) and not src:
            continue                                         # 两头都要在考纲里；资料、真题点名的例外（truly、pianist）
        if c in (w, w + 's', w + 'es') or K.get(c) and K.get(c).get('alias_of') == w or K.get(w) and K.get(w).get('alias_of') == c:
            continue
        if re.fullmatch(re.escape(w.rstrip('y')) + r'(s|es|ies)', c):
            continue                                         # 复数不算词性转换
        pc = show_pos(T, K, c, mine, child=w if dirn == 'up' else None)
        if pc not in CONTENT:
            continue
        zh = K.zh(c, pc) or T.meaning_pos(c)[1]
        note = SPECIAL_CONV_NOTE.get((w, c)) or (spell_note(w, c) if dirn == 'down' else '')
        score = (0 if src and src != 'S3' else 1 if src else 2, 0 if pc not in mine else 1, depth, -zipf(c))
        cands.append((score, pc, c, zh, note, src))
    cands.sort()
    chips, srcs = [], []
    for score, pc, c, zh, note, src in cands[:MAXN['词性转换']]:
        chips.append('%s %s %s%s' % (pc, c, zh, '（%s）' % note if note else ''))
        if src and src != 'S3':
            srcs.append('S4：%s' % src)
        elif src:
            srcs.append('上海中考复习资料列了 %s' % ('%s → %s' % (w, c) if (w, c) in SHP else '%s → %s' % (c, w)))
    if not chips:
        return [], ''
    ins = [x for x in [w] + [c[2] for c in cands[:MAXN['词性转换']]] if K.get(x)]
    basis = K.ref(*ins) + '（评价指南·构词法）' + ('；' + '；'.join(dict.fromkeys(srcs)) if srcs else '')
    return chips, basis


TESTED_SUF = ('ly', 'er', 'or', 'ist', 'ian', 'an', 'ness', 'ment', 'tion', 'sion', 'ion', 'ation', 'ful', 'less', 'y', 'ous', 'al',
              'ial', 'ical', 'able', 'ible', 'ive', 'ity', 'ty', 'ance', 'ence', 'dom', 'ship', 'en', 'ese', 'ern', 'ed', 'ing', 'th',
              'ure', 'ee', 'ess', 'ress', 'ize', 'ise')
TESTED_PRE = ('un', 'dis', 'im', 'in', 'il', 'ir', 're', 'en', 'mis')


def derived_line(T, K, w):
    """考纲外的词：由考纲词变来、又常用（或资料、真题点名）的，写一条“true → truly（…）”"""
    if w.endswith('ise') and K.get(w[:-3] + 'ize'):
        return None
    for b, kind in T.parent.get(w, []):
        if not K.get(b) or kind == 'comp' and not pair_src(b, w):
            continue
        src = pair_src(b, w)
        n = T.words[w]
        r = T.data[n]
        if not src:
            if kind == 'var':
                continue
            sp = T.v(r, '拆分').split('；')[0]
            last = re.sub(r'\(.*?\)', '', sp.split(' + ')[-1]).strip().lower()
            first = re.sub(r'\(.*?\)', '', sp.split(' + ')[0]).strip().lower()
            ok = (kind == 'suf' and last in TESTED_SUF) or (kind == 'pre' and first in TESTED_PRE)
            if not ok or zipf(w) < 4.0 or w[:1].isupper() or not edge_ok(T, K, b, w, kind) or K.pos(b) and not any(p in CONTENT for p in K.pos(b)):
                continue
        pw = T.meaning_pos(w)
        note = SPECIAL_CONV_NOTE.get((b, w)) or spell_note(b, w)
        chip = '%s → %s%s' % (b, w, '（%s）' % note if note else '')
        basis = K.ref(b) + '（%s 不在考纲，评价指南·构词法：派生）' % w
        if src and src != 'S3':
            basis += '；S4：' + src
        elif src:
            basis += '；上海中考复习资料列了 %s → %s' % (b, w)
        return chip, basis
    return None


# ---------------------------------------------------------------- 短语、用法、易混
PHR_ALT = {   # (词组表原文, 这一行的词) → 画面写什么
    ('at first/last', 'first'): 'at first 起先', ('at first/last', 'last'): 'at last 最后、终于',
    ('at least/most', 'least'): 'at least 至少', ('at least/most', 'most'): 'at most 至多',
    ('be good/poor at', 'good'): 'be good at 擅长于', ('be good/poor at', 'poor'): 'be poor at 对……比较差',
    ('less/more than', 'less'): 'less than 少于', ('less/more than', 'more'): 'more than 多于',
    ('turn down/up', 'down'): 'turn down 调低', ('turn down/up', 'up'): 'turn up 调高', ('turn down/up', 'turn'): 'turn down / up 调低、调高',
    ('at breakfast/lunch/supper', 'breakfast'): 'at breakfast 早餐时', ('at breakfast/lunch/supper', 'lunch'): 'at lunch 午餐时',
    ('at breakfast/lunch/supper', 'supper'): 'at supper 晚餐时', ('by bus/train/plane', 'bus'): 'by bus 乘公共汽车',
    ('by bus/train/plane', 'train'): 'by train 乘火车', ('by bus/train/plane', 'plane'): 'by plane 乘飞机',
    ('to one’s joy/surprise', 'joy'): 'to one’s joy 使某人高兴的是', ('to one’s joy/surprise', 'surprise'): 'to one’s surprise 使某人惊奇的是',
    ('have a class/lesson', 'class'): 'have a class 上课', ('have a class/lesson', 'lesson'): 'have a lesson 上课',
    ('get along/on (with)', 'get'): 'get along / on with 与……相处', ('get along/on (with)', 'along'): 'get along with 与……相处',
}
PHR_SKIP = {('once', 'once every four years'), ('every', 'once every four years'), ('four', 'once every four years'), ('year', 'once every four years')}
STOP = set('a an the of to in on at for with by from up down out off over into as and or so than too not no one some each other '
           'sb sth oneself be one\'s it this that these those there what'.split())


def phrase_line(K, w, skip=()):
    e = K.get(w)
    if not e or w in STOP:
        return [], ''
    pos = K.pos(w)
    if not any(p in CONTENT for p in pos):
        return [], ''
    forms = {w, w + 's', w + 'es'}
    if 'v.' in pos:
        ed = infl(w, 'VBN')
        if ed and not K.get(ed):
            forms.add(ed)                                         # be connected to、be covered with、be supposed to
    hits = [p for p in K.P if forms & p['toks'] and not any(s in p['p'] for s in skip) and (w, p['p']) not in PHR_SKIP]
    if not hits:
        return [], ''

    def norm(t):
        t = t.lower().replace('’', "'")
        t = re.sub(r'\s*\([^()]*\)', '', t)
        t = re.sub(r'/[a-z\']+', '', t)
        return re.sub(r'\s+', ' ', t).strip()
    tops = [norm(t) for t in D.PHR_TOP]

    def rank(p):
        s = norm(p['p'])
        top = next((i for i, t in enumerate(tops) if s == t), 999)
        return (top, len(p['toks']), K.P.index(p))
    hits.sort(key=rank)
    pick = hits[:MAXN['短语']]
    def zh(t):
        t = re.sub(r'[（(][^（）()]*[)）]', '', t).strip()
        parts = [x.strip() for x in re.split(r'[；;]', t) if x.strip()]
        j = '、'.join(parts)
        return j if len(j) <= 12 else parts[0]
    chips = [PHR_ALT.get((p['p'], w)) or '%s %s' % (p['p'], zh(p['zh'])) for p in pick]
    pages = sorted({p['page'] for p in pick})
    return chips, '考纲词组表第 %s 页' % '、'.join(str(x) for x in pages)


CONF = defaultdict(list)
for keys, head, desc, cat in D.CONFUSE:
    for k in keys:
        CONF[k.lower()].append((keys, head, desc, cat))


def confuse_line(K, w):
    chips, srcs = [], []
    for keys, head, desc, cat in CONF.get(w, []):
        inK = [k for k in keys if K.get(k)]
        if not K.get(w) or len(keys) > 1 and len(inK) < 2:
            continue
        chips.append('%s（%s）' % (head, desc.replace('；', '，')))
        srcs.append('%s；%s' % (K.ref(*inK), D.B.get(cat, '')))
        if len(chips) >= MAXN['易混']:
            break
    return chips, '｜'.join(srcs)


def usage_line(w, phrase=False):
    items = (D.USAGE_PHR if phrase else D.USAGE).get(w, [])
    chips, srcs = [], []
    for t, cat in items:
        for seg in [x.strip() for x in split_top(t, '；') if x.strip()]:
            if len(chips) < MAXN['用法']:
                chips.append(seg)
        srcs.append(D.B.get(cat, cat))
    return chips, '；'.join(dict.fromkeys(srcs))


def split_top(s, sep):
    out, depth, cur = [], 0, ''
    for ch in s:
        if ch in '（(':
            depth += 1
        if ch in '）)':
            depth = max(0, depth - 1)
        if ch == sep and depth == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


# ---------------------------------------------------------------- 一个词
def kaodian(T, K, n):
    """→ (考点, 依据)，两段都是一行一个【标签】"""
    r = T.data[n]
    w0 = T.v(r, '单词').strip()
    w = w0.lower()
    if not w:
        return '', ''
    rows = []                                                # (标签, [小块], 依据)
    e = K.get(w)
    if ' ' in w:                                             # 表里的短语：只看考纲词组表
        hit = next((p for p in K.P if p['p'].lower().replace('’', "'") == w.replace('’', "'")), None)
        if hit:
            u, ub = usage_line(w, phrase=True)
            if u:
                rows.append(('用法', u, '考纲词组表第 %s 页 %s；%s' % (hit['page'], hit['p'], ub)))
        return pack(rows)
    if e and not (w0[:1].isupper() and not e.get('people') and not e.get('country') and w0 != 'I'):
        pos = K.pos(w)
        inf = inflected_row(w, K)
        if inf:
            rows.append(('变形', [inf[0]], inf[1]))
        elif e.get('pron'):
            c, b = pron_line(w, e, K)
            if c:
                rows.append(('变形', c, b))
        elif e.get('ordinal') or e.get('cardinal'):
            c, b = num_line(w, e, K)
            if c:
                rows.append(('变形', c, b))
        else:
            groups, bas = [], []
            plist = [x for x in pos if x in CONTENT or x == 'aux.']
            if 'v.' in plist and 'aux.' in plist:
                plist.remove('aux.')
            for i, p in enumerate(plist):
                if p == 'aux.' and w not in ('can', 'may', 'shall', 'will'):
                    c, b = [], ''
                elif p in ('v.', 'aux.'):
                    c, b = verb_line(w, e, K)
                elif p == 'n.':
                    c, b = noun_line(w, e, K, main=(i == 0))
                elif p in ('adj.', 'adv.'):
                    c, b = adj_line(w, e, K) if p == 'adj.' or 'adj.' not in pos else ([], '')
                else:
                    c, b = [], ''
                if c:
                    groups.append('%s %s' % ('v.' if p == 'aux.' else p, '；'.join(c)))
                    bas.append(b)
            if e.get('people') or e.get('country'):
                kw = e.get('w', w0)
                if kw in D.SAME_FORM or kw in D.PL_TRAP:
                    groups = ['n. ' + (D.SAME_FORM.get(kw) or D.PL_TRAP.get(kw))]
                    bas = ['考纲词汇表第 %s 页 国家和人' % e['page'] + '；上海中考复习资料（国名—国籍）']
            if groups:
                rows.append(('变形', groups, '；'.join(dict.fromkeys(bas))))
        if e.get('country') or e.get('people'):
            other = e.get('people') or e.get('country')
            pc = 'adj.' if e.get('people') else 'n.'
            ex = [v for (g, a), v in D.SH_EXAM.items() if (g, a) in ((w0, other), (other, w0))]
            rows.append(('词性转换', ['%s %s %s' % (pc, other, COUNTRY_ZH.get(other, ''))],
                         '考纲词汇表第 %s 页 国家、大洲及其对应的人；上海中考复习资料（国名—国籍）%s' % (e['page'], '；S4：' + ex[0] if ex else '')))
        elif not e.get('pron') and not e.get('ordinal') and not e.get('cardinal') and w not in ('be', 'being'):
            c, b = conv_line(T, K, w)
            done = ' '.join(x for r0 in rows for x in r0[1])
            keep = [i for i, ch in enumerate(c) if not re.search(r'\b%s\b' % re.escape(ch.split()[1]), done)]   # 变形里已经有的（beginning）不再列
            c = [c[i] for i in keep]
            if c:
                rows.append(('词性转换', c, b))
        conf_skip = []
        cc, cb = confuse_line(K, w)
        for ch in cc:
            conf_skip += re.findall(r'(?:in|on|at|by|hear|think|look|find|be|used) [a-z ]+?(?= /|（)', ch)
        u, ub = usage_line(w)
        c, b = phrase_line(K, w, skip=[x.strip() for x in conf_skip])
        nm = lambda t: re.sub(r'[.…。\s]+', ' ', t.lower().replace('’', "'")).strip()
        ut = nm(' '.join(u))
        c = [x for x in c if nm(re.sub(r'/\w+', '', re.split(r'\s(?=[\u3400-\u9fff(（])', x)[0])) not in ut]   # 用法里已经讲了的短语不再列
        if c:
            rows.append(('短语', c, b))
        if u:
            rows.append(('用法', u, ub))
        if cc:
            rows.append(('易混', cc, cb))
        return pack(rows)
    # 考纲外
    inf = inflected_row(w, K)
    if inf:
        rows.append(('变形', [inf[0]], inf[1]))
        return pack(rows)
    d = derived_line(T, K, w)
    if d:
        rows.append(('词性转换', [d[0]], d[1]))
    return pack(rows)


def pack(rows):
    kd, yj = [], []
    for lab, chips, basis in rows:
        if not chips:
            continue
        if lab == '变形':
            txt = ' / '.join(chips)
        else:
            txt = '；'.join(chips[:MAXN.get(lab, 4)])
        kd.append('【%s】%s' % (lab, txt))
        yj.append('【%s】%s' % (lab, basis or '—'))
    return '\n'.join(kd), '\n'.join(yj)


# ---------------------------------------------------------------- 命令行
def build_all(T, K):
    return [kaodian(T, K, n) for n in range(len(T.data))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('table')
    ap.add_argument('--show')
    ap.add_argument('--write')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--kg', default=KG_PATH)
    ap.add_argument('--old', action='store_true', help='写第 121 条的精简版（只写常考的一两行）；不加就写第 126 条的详细版（kaodian_full.py）')
    a = ap.parse_args()
    T = Table(a.table)
    if a.check:
        col, col2 = T.ix.get('考点'), T.ix.get('考点依据')
        if col is None:
            raise SystemExit('表里没有「考点」列')
        filled = bad = mism = 0
        lab = defaultdict(int)
        for r in T.data:
            t = '' if r[col] is None else str(r[col])
            y = '' if col2 is None or col2 >= len(r) or r[col2] is None else str(r[col2])
            if not t.strip():
                if y.strip():
                    mism += 1
                continue
            filled += 1
            tl = [re.match(r'^【(\S+?)】', x) for x in t.split('\n')]
            yl = [re.match(r'^【(\S+?)】', x) for x in y.split('\n')]
            for m in tl:
                if not m or m.group(1) not in LABELS:
                    bad += 1
                else:
                    lab[m.group(1)] += 1
            if col2 is not None and [m.group(1) if m else None for m in tl] != [m.group(1) if m else None for m in yl]:
                mism += 1
        print('考点：%d 个词有，格式不对的行 %d%s；%s' % (filled, bad, '，和「考点依据」对不上的 %d' % mism if col2 is not None else '', '，'.join('%s %d' % (k, lab[k]) for k in LABELS)))
        return
    K = KG(a.kg)
    if a.show:
        want = [x.strip().lower() for x in a.show.split(',')]
        for wd in want:
            n = T.words.get(wd)
            if n is None:
                print('==', wd, '（表里没有）'); continue
            if a.old:
                kd, yj = kaodian(T, K, n)
            else:
                import kaodian_full as F
                F.speed_up(T)
                kd, yj = F.full(T, K, n)
            print('==', T.v(T.data[n], '单词'), '｜考纲' if K.get(wd) else '｜考纲外')
            print(kd or '（没有考点）')
            if yj:
                print('  依据：' + yj.replace('\n', '\n        '))
        return
    if a.write:
        import xlsx_write
        if a.old:
            vals = build_all(T, K)
        else:
            import kaodian_full as F
            vals = F.build_all(T, K)
        col = T.ix.get('考点')
        drop = T.ix.get('考点依据')                       # 上一轮试过加「考点依据」列，用户说不用加：有的话去掉
        table = [list(T.rows[0])] + [list(r) for r in T.data]
        table = [[(None if v is None else (v if isinstance(v, (int, float)) else str(v))) for v in row] for row in table]
        new_cols = {}
        if col is None:
            for row in table:
                row.append(None)
            col = len(table[0]) - 1
            table[0][col] = '考点'
            new_cols[col] = (58, T.ix['辨析'])
        for k2, (kd, yj) in enumerate(vals):
            table[k2 + 1][col] = kd or None
        if drop is not None:
            raise SystemExit('表里有「考点依据」列：请用没有这一列的表（考点版）来写')
        xlsx_write.rebuild(a.table, a.write, table, new_cols)
        print('写好了：%s（%d 个词有考点）' % (a.write, sum(1 for v in vals if v[0])))


if __name__ == '__main__':
    main()

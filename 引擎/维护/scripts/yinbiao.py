#!/usr/bin/env python3
"""读音拆分：读音节划分表（比如“音节划分_总词库7869词_细分版.xlsx”），给视频开头的“一、读音拆分”用。

  python3 syllables.py build 音节划分_….xlsx syl.json            # 读整张表（约 3 秒）：每个词的拆块、标注、关键解释
  python3 syllables.py show syl.json camera,make,education         # 看拆块、每块的读音、对得齐不齐
  python3 syllables.py check syl.json                             # 全表试对一遍：哪些词对不齐（读音拆分会退成只念整词）

表里每个格子是富文本，样式就是标注（和表里“说明”工作表一致）：
  红色删除线 = 不发音的字母；蓝色下划线 = 固定组合（单线、双线）；绿色加粗 = 元辅e 里读字母音的元音；紫色加粗 = 音变、特殊读音。
每一块的读音：先用单词表的音标（--list 给的 6A-9A 这种表里有“音标”列），没有就用语音模型自带的英式词典
（$WORDFILM_MODELS/kokoro-multi-lang-v1_1/lexicon-gb-en.txt，音节表“说明”写着英音为准），再按字母一个个对到音上，
分到每一块；关键解释里写了“X 读 /…/”的（education 的 du 读 /dʒu/），照表里的音改。
配音念每一块，用的是“音素词”：在配音模型的词典里临时加一个词（qzca = k æ），念出来正好是这一块的音，不会把 me 念成 /miː/。
"""
import json, os, re, sys

MODELS = os.environ.get('WORDFILM_MODELS', os.path.expanduser('~/wordfilm-models'))
LEX_GB = os.path.join(MODELS, 'kokoro-multi-lang-v1_1', 'lexicon-gb-en.txt')
LEX_US = os.path.join(MODELS, 'kokoro-multi-lang-v1_1', 'lexicon-us-en.txt')

# ---------------------------------------------------------------- 读表
COLOR = {'FFC00000': 'red', 'FF0070C0': 'blue', 'FF00A050': 'green', 'FF7030A0': 'purple'}


def _font_of(f):
    col = ''
    if f is not None and getattr(f, 'color', None) is not None:
        col = COLOR.get(str(getattr(f.color, 'rgb', '') or '').upper(), '')
    u = getattr(f, 'u', None) if f is not None else None
    return {'silent': bool(getattr(f, 'strike', False)) if f is not None else False,
            'u': 2 if u in ('double', 'doubleAccounting') else 1 if u else 0,
            'k': 'long' if col == 'green' else 'special' if col == 'purple' else ''}


def parse_cell(cell):
    """富文本 → [{t: 'ca', L: [{c, silent, u, k}]}]；“ + ”分块"""
    from openpyxl.cell.rich_text import CellRichText
    v = cell.value
    runs = []
    if isinstance(v, CellRichText):
        for part in v:
            if isinstance(part, str):
                runs.append((part, _font_of(cell.font)))
            else:
                runs.append((part.text, _font_of(part.font)))
    else:
        runs.append((str(v or ''), _font_of(cell.font)))
    chunks, cur = [], []
    for text, st in runs:
        for ch in text:
            if ch == '+':
                if cur:
                    chunks.append(cur)
                cur = []
            elif ch.strip():
                cur.append(dict(st, c=ch))
    if cur:
        chunks.append(cur)
    return [{'t': ''.join(x['c'] for x in L), 'L': L} for L in chunks]


def build(xlsx, out):
    from openpyxl import load_workbook
    wb = load_workbook(xlsx, rich_text=True)
    ws = wb['音节划分'] if '音节划分' in wb.sheetnames else wb.worksheets[0]
    data = {}
    for row in ws.iter_rows(min_row=2):
        w = row[0].value
        if not w or len(row) < 2:
            continue
        w = str(w).strip()
        chunks = parse_cell(row[1])
        if not chunks:
            continue
        note = str(row[2].value).strip() if len(row) > 2 and row[2].value else ''
        data.setdefault(w.lower(), {'w': w, 'chunks': chunks, 'note': [x.strip() for x in note.split('\n') if x.strip()]})
    for name, key in (('待复核', 'review'), ('跳过的条目', 'skipped')):
        if name in wb.sheetnames:
            for r in wb[name].iter_rows(min_row=2, values_only=True):
                if not r or not r[0]:
                    continue
                k = str(r[0]).strip().lower()
                why = str(r[-1] or '').strip() if key == 'skipped' else str(r[2] or '').strip()
                if key == 'skipped':
                    data.setdefault('#skipped', {})[k] = why
                elif k in data:
                    data[k]['review'] = why
    json.dump(data, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
    print('读了“音节划分”：%d 个词 -> %s' % (len([k for k in data if not k.startswith('#')]), out))
    return data


# ---------------------------------------------------------------- 音标：词典（Kokoro 的音素）和课本音标都转成同一套“音”
VOW = {'æ', 'e', 'ɪ', 'ɒ', 'ʌ', 'ʊ', 'ə', 'i', 'u', 'iː', 'ɑː', 'ɔː', 'uː', 'ɜː', 'eɪ', 'aɪ', 'ɔɪ', 'aʊ', 'əʊ', 'ɪə', 'eə', 'ʊə', 'ɐ'}
TOK2P = {'A': 'eɪ', 'I': 'aɪ', 'W': 'aʊ', 'Y': 'ɔɪ', 'Q': 'əʊ', 'O': 'əʊ', 'a': 'æ', 'æ': 'æ', 'ɛ': 'e', 'ɹ': 'r', 'ɾ': 't', 'ʔ': 't',
         'ʤ': 'dʒ', 'ʧ': 'tʃ', 'ɡ': 'ɡ', 'g': 'ɡ', 'ɐ': 'ʌ', 'ɑ': 'ɑ', 'ɔ': 'ɔ', 'ɜ': 'ɜ', 'ᵻ': 'ɪ'}
# 音 → 配音模型的音素（Kokoro 的写法；英式）
P2TOK = {'eɪ': ['A'], 'aɪ': ['I'], 'aʊ': ['W'], 'ɔɪ': ['Y'], 'əʊ': ['Q'], 'e': ['ɛ'], 'r': ['ɹ'], 'dʒ': ['ʤ'], 'tʃ': ['ʧ'],
         'iː': ['i', 'ː'], 'ɑː': ['ɑ', 'ː'], 'ɔː': ['ɔ', 'ː'], 'uː': ['u', 'ː'], 'ɜː': ['ɜ', 'ː'], 'ɪə': ['ɪ', 'ə'], 'eə': ['ɛ', 'ː'],
         'ʊə': ['ʊ', 'ə'], 'ɡ': ['ɡ'], 'ts': ['t', 's']}
IPA_SYMS = sorted(['tʃ', 'dʒ', 'eɪ', 'aɪ', 'ɔɪ', 'aʊ', 'əʊ', 'ɪə', 'eə', 'ʊə', 'iː', 'ɑː', 'ɔː', 'uː', 'ɜː', 'æ', 'e', 'ɪ', 'ɒ', 'ʌ', 'ʊ',
                   'ə', 'i', 'u', 'ɑ', 'ɔ', 'ɜ', 'p', 'b', 't', 'd', 'k', 'ɡ', 'f', 'v', 'θ', 'ð', 's', 'z', 'ʃ', 'ʒ', 'h', 'm', 'n', 'ŋ',
                   'l', 'r', 'j', 'w', 'x'], key=len, reverse=True)

_lex = {}


def lexicon(path):
    if path not in _lex:
        d = {}
        if os.path.exists(path):
            for line in open(path, encoding='utf-8'):
                p = line.rstrip('\n').split(' ')
                if len(p) > 1 and p[0] not in d:
                    d[p[0]] = p[1:]
        _lex[path] = d
    return _lex[path]


def from_tokens(toks):
    """Kokoro 音素 → [{p: 音, s: 重音 0/1/2, syl: 成音节的 ə}]"""
    out, stress = [], 0
    for t in toks:
        if t == 'ˈ':
            stress = 1
            continue
        if t == 'ˌ':
            stress = stress or 2
            continue
        if t == 'ː':
            if out:
                last = out[-1]
                last['p'] = {'e': 'eə', 'i': 'iː', 'u': 'uː', 'ɑ': 'ɑː', 'ɔ': 'ɔː', 'ɜ': 'ɜː', 'ə': 'ɜː', 'æ': 'ɑː'}.get(last['p'], last['p'] + 'ː')
            continue
        if t == 'ᵊ':
            out.append({'p': 'ə', 's': 0, 'syl': True})
            continue
        p = TOK2P.get(t, t)
        if p in ('ɑ', 'ɔ', 'ɜ'):
            p = {'ɑ': 'ɑː', 'ɔ': 'ɔː', 'ɜ': 'ɜː'}[p] if False else p      # 单独出现时下面统一处理
        ph = {'p': p, 's': 0}
        if p in VOW or p in ('ɑ', 'ɔ', 'ɜ'):
            ph['s'], stress = stress, 0
        out.append(ph)
    # 两个符号合成一个双元音（ɪ ə → ɪə）；ɑ ɔ ɜ 后面没跟 ː 的（美式）当长音
    res = []
    for ph in out:
        if res and ph['p'] == 'ə' and not ph.get('syl') and not ph['s'] and res[-1]['p'] in ('ɪ', 'ʊ') and res[-1].get('s') and not res[-1].get('syl'):
            res[-1] = dict(res[-1], p=res[-1]['p'] + 'ə')
            continue
        if ph['p'] in ('ɑ', 'ɔ', 'ɜ'):
            ph = dict(ph, p=ph['p'] + 'ː')
        res.append(ph)
    return res


def from_ipa(ipa):
    """课本音标 /kəˈrɪə(r)/ → 同上；读不了的返回 None"""
    s = str(ipa or '').strip().strip('/[]').split('/')[0].strip()
    s = re.sub(r'\([^)]*\)', '', s).replace(':', 'ː').replace('ʧ', 'tʃ').replace('ʤ', 'dʒ').replace('g', 'ɡ').replace('ɚ', 'ə').replace('ɝ', 'ɜː')
    s = s.replace("'", 'ˈ').replace(',', 'ˌ').replace('.', '').replace(' ', '')
    if not s:
        return None
    out, i, pend = [], 0, 0
    while i < len(s):
        if s[i] in 'ˈˌ':
            pend = 1 if s[i] == 'ˈ' else 2
            i += 1
            continue
        m = next((x for x in IPA_SYMS if s.startswith(x, i)), None)
        if not m:
            return None
        ph = {'p': m, 's': 0}
        if m in VOW:
            ph['s'], pend = pend, 0
        out.append(ph)
        i += len(m)
    return out or None


def lexicon_phones(word):
    """英式词典里的音；没有的复合词试着拆成两个词（hometown = home + town）"""
    w = word.lower().replace('’', "'")
    for path in (LEX_GB, LEX_US):
        L = lexicon(path)
        if w in L:
            return from_tokens(L[w]), '英式词典' if path == LEX_GB else '美式词典'
    L = lexicon(LEX_GB)
    for k in range(len(w) - 2, 1, -1):
        a, b = w[:k], w[k:]
        if a in L and b in L and len(b) >= 2:
            pa, pb = from_tokens(L[a]), from_tokens(L[b])
            for ph in pb:
                if ph['s'] == 1:
                    ph['s'] = 2
            return pa + pb, '英式词典（%s + %s）' % (a, b)
    return None, ''


# ---------------------------------------------------------------- 字母对到音（动态规划）
VL = set('aeiou')
T1 = {
    'a': {'æ', 'ɑː', 'eɪ', 'ə', 'ɒ', 'ɔː', 'e', 'ɪ', 'eə', 'ʌ', 'i'}, 'e': {'e', 'iː', 'ɪ', 'ə', 'ɜː', 'ɪə', 'eɪ', 'i', 'eə', 'æ'},
    'i': {'ɪ', 'aɪ', 'iː', 'ə', 'ɜː', 'i', 'j', 'æ'}, 'o': {'ɒ', 'əʊ', 'ʌ', 'ɔː', 'uː', 'ʊ', 'ə', 'ɜː', 'aʊ', 'ɔɪ', 'ɪ', 'w'},
    'u': {'ʌ', 'ʊ', 'uː', 'ə', 'ɜː', 'ɪ', 'w', 'e', 'ʊə', 'u'}, 'y': {'i', 'ɪ', 'aɪ', 'j', 'ə'}, 'w': {'w'},
    'b': {'b'}, 'c': {'k', 's', 'ʃ', 'tʃ'}, 'd': {'d', 'dʒ', 't'}, 'f': {'f', 'v'}, 'g': {'ɡ', 'dʒ', 'ʒ', 'f', 'k'}, 'h': {'h'},
    'j': {'dʒ', 'j', 'ʒ', 'h'}, 'k': {'k'}, 'l': {'l'}, 'm': {'m'}, 'n': {'n', 'ŋ'}, 'p': {'p', 'f'}, 'q': {'k'}, 'r': {'r', 'ə'},
    's': {'s', 'z', 'ʃ', 'ʒ'}, 't': {'t', 'ʃ', 'tʃ', 'θ', 'ð', 'd'}, 'v': {'v', 'f'}, 'x': {'z', 'k', 's'}, 'z': {'z', 's', 'ʒ'}}
DIGRAPH_2ND = {('c', 'h'), ('s', 'h'), ('t', 'h'), ('p', 'h'), ('w', 'h'), ('g', 'h'), ('r', 'h'), ('c', 'k'), ('n', 'g'), ('g', 'n'), ('k', 'n'), ('w', 'r')}


def _isv(p):
    return p in VOW


def cost0(L, i):
    x = L[i]
    c, prev, nxt = x['c'].lower(), L[i - 1]['c'].lower() if i else '', L[i + 1]['c'].lower() if i + 1 < len(L) else ''
    if x.get('silent'):
        return 0.0
    if c == prev and c not in VL:
        return 0.1
    if (prev, c) in DIGRAPH_2ND:
        return 0.1
    if (c, nxt) in (('c', 'k'), ('t', 'c'), ('d', 'g'), ('g', 'h'), ('k', 'n'), ('w', 'r'), ('g', 'n')):
        return 0.2
    if c in VL and (prev in VL or nxt in VL or (c == 'e' and nxt in 'wy')):
        return 0.25
    if c in 'wy' and prev in VL:
        return 0.2
    if c == 'r' and prev in VL | {'y'}:
        return 0.2
    if c == 'h' and prev in VL:
        return 0.3
    if c == 'u' and prev in 'qg':
        return 0.4
    if c == 'e' and (x.get('end') or not nxt):
        return 0.4
    if c == 'g' and prev == 'n':
        return 0.3
    if c in VL:
        return 1.2
    return 2.5


def cost1(L, i, p):
    x = L[i]
    c = x['c'].lower()
    if x.get('silent'):
        return 5.0
    if p in T1.get(c, ()):
        return 0.0
    if c in VL | {'y'} and _isv(p):
        return 1.0
    if c not in VL | {'y'} and not _isv(p):
        return 2.0
    if c in 'yiuow' and p in ('j', 'w'):
        return 0.5
    return 3.0


def cost2(L, i, p1, p2):
    x = L[i]
    c = x['c'].lower()
    if x.get('silent'):
        return 6.0
    if c == 'x' and (p1, p2) in (('k', 's'), ('ɡ', 'z'), ('k', 'ʃ')):
        return 0.0
    if c == 'u' and p1 == 'j' and _isv(p2):
        return 0.1
    if c == 'o' and (p1, p2) == ('w', 'ʌ'):
        return 0.3
    if c == 'q' and (p1, p2) == ('k', 'w'):
        return 0.2
    if c in VL | {'y'} and _isv(p1) and p2 == 'ə':
        return 0.6
    if c in 'lnm' and p1 == 'ə' and p2 == c:                 # 成音节的 l、n、m（table 的 ble：l 带着一个很轻的 ə）
        return 0.4
    if c == 'e' and p1 == 'j' and _isv(p2) and i + 1 < len(L) and L[i + 1]['c'].lower() == 'w':   # ew 读 /juː/（few、news）
        return 0.1
    if c in ('c', 't') and (p1, p2) == ('t', 's'):
        return 0.3
    return 4.0


def align(letters, phones):
    """→ (总代价, 每个字母对到的音的下标列表)"""
    n, m = len(letters), len(phones)
    INF = 1e9
    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    bk = [[None] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0.0
    P = [ph['p'] for ph in phones]
    for j in range(m):
        if dp[0][j] < INF and dp[0][j] + dcost(P[j]) < dp[0][j + 1]:
            dp[0][j + 1], bk[0][j + 1] = dp[0][j] + dcost(P[j]), -1
    for i in range(n):
        for j in range(m + 1):
            v = dp[i][j]
            if v >= INF:
                continue
            c = v + cost0(letters, i)
            if c < dp[i + 1][j]:
                dp[i + 1][j], bk[i + 1][j] = c, 0
            if j < m:
                c = v + cost1(letters, i, P[j])
                if c < dp[i + 1][j + 1]:
                    dp[i + 1][j + 1], bk[i + 1][j + 1] = c, 1
            if j + 1 < m:
                c = v + cost2(letters, i, P[j], P[j + 1])
                if c < dp[i + 1][j + 2]:
                    dp[i + 1][j + 2], bk[i + 1][j + 2] = c, 2
        # 同一个字母位置上，词典多出来的音可以不要（弱读的 ə、ɪ 便宜，别的贵）
        for j in range(m):
            v = dp[i + 1][j]
            if v >= INF:
                continue
            c = v + (0.6 if phones[j].get('syl') else dcost(P[j]))
            if c < dp[i + 1][j + 1]:
                dp[i + 1][j + 1], bk[i + 1][j + 1] = c, -1
    if dp[n][m] >= INF:
        return INF, None, []
    spans, dropped, i, j = [None] * n, [], n, m
    while i > 0 or j > 0:
        k = bk[i][j]
        if k is None:
            return INF, None, []
        if k == -1:
            dropped.append(j - 1)
            j -= 1
            continue
        spans[i - 1] = list(range(j - k, j))
        j -= k
        i -= 1
    return dp[n][m], spans, sorted(dropped)


def dcost(p):
    return 0.35 if p in ('ə', 'ɪ', 'i') else 2.0 if p in VOW else 3.0


# ---------------------------------------------------------------- 显示用的音标
ONSETS = {('p',), ('b',), ('t',), ('d',), ('k',), ('ɡ',), ('f',), ('v',), ('θ',), ('ð',), ('s',), ('z',), ('ʃ',), ('ʒ',), ('h',), ('m',),
          ('n',), ('l',), ('r',), ('j',), ('w',), ('tʃ',), ('dʒ',),
          ('p', 'r'), ('p', 'l'), ('b', 'r'), ('b', 'l'), ('t', 'r'), ('d', 'r'), ('k', 'r'), ('k', 'l'), ('ɡ', 'r'), ('ɡ', 'l'), ('f', 'r'),
          ('f', 'l'), ('θ', 'r'), ('ʃ', 'r'), ('s', 'p'), ('s', 't'), ('s', 'k'), ('s', 'm'), ('s', 'n'), ('s', 'l'), ('s', 'w'), ('t', 'w'),
          ('d', 'w'), ('k', 'w'), ('ɡ', 'w'), ('s', 'p', 'r'), ('s', 'p', 'l'), ('s', 't', 'r'), ('s', 'k', 'r'), ('s', 'k', 'w'),
          ('p', 'j'), ('b', 'j'), ('t', 'j'), ('d', 'j'), ('k', 'j'), ('f', 'j'), ('v', 'j'), ('m', 'j'), ('n', 'j'), ('h', 'j'), ('l', 'j'),
          ('s', 'j'), ('k', 'w')}


def show_ipa(phones, stress_marks=True):
    """课本样子的音标：重音符号放在音节开头（按“音节开头尽量多带辅音”挪到辅音前面），成音节的 ə 不写（/ˈpiːpl/）"""
    marks = {}
    if stress_marks:
        for k, ph in enumerate(phones):
            if ph.get('s') and _isv(ph['p']):
                j = k
                while j > 0 and not _isv(phones[j - 1]['p']) and tuple(x['p'] for x in phones[j - 1:k]) in ONSETS:
                    j -= 1
                marks[j] = 'ˈ' if ph['s'] == 1 else 'ˌ'
    out = ''
    for k, ph in enumerate(phones):
        out += marks.get(k, '')
        if ph.get('syl') and k + 1 < len(phones) and phones[k + 1]['p'] in ('l', 'n', 'm') and (k + 2 == len(phones) or not _isv(phones[k + 2]['p'])):
            continue
        out += ph['p']
    return out.replace('ɡ', 'g')


def to_tokens(phones, stress=True):
    out = []
    if phones and len(phones) >= 2 and not any(_isv(p['p']) or p.get('syl') for p in phones) and phones[-1]['p'] in ('n', 'l', 'm'):
        phones = phones[:-1] + [{'p': 'ə', 's': 0, 'syl': True}] + phones[-1:]
    for ph in phones:
        if ph.get('syl'):
            out.append('ᵊ')
            continue
        if stress and ph.get('s') and _isv(ph['p']):
            out.append('ˈ' if ph['s'] == 1 else 'ˌ')
        out += P2TOK.get(ph['p'], [ph['p']])
    return out


# ---------------------------------------------------------------- 关键解释：“X 读 /…/”照表里改，念的时候把音标换成音素词
NOTE_RX = re.compile(r'^\s*-?([A-Za-z]+)\s*读[^/：:]*?/([^/]+)/')


def note_overrides(note_lines):
    out = []
    for ln in note_lines:
        m = NOTE_RX.match(ln)
        if m and '_' not in m.group(1):
            ph = from_ipa(m.group(2))
            if ph:
                out.append((m.group(1).lower(), ph, m.group(2)))
    return out


def apply_override(letters, phones, spans, grp, new):
    """把 grp 这几个字母（优先找表里标了颜色的那一处）对到的音换成 new"""
    s = ''.join(x['c'].lower() for x in letters)
    hits = [m.start() for m in re.finditer('(?=%s)' % re.escape(grp), s)]
    if not hits:
        return phones, spans, False
    def marked(a):
        return any(letters[k].get('k') or letters[k].get('u') for k in range(a, a + len(grp)))
    a = next((h for h in hits if marked(h)), hits[0])
    idx = sorted({j for k in range(a, a + len(grp)) for j in (spans[k] or [])})
    if not idx or idx != list(range(idx[0], idx[-1] + 1)):
        return phones, spans, False
    old = phones[idx[0]:idx[-1] + 1]
    if [(x['p'], bool(x.get('syl'))) for x in old] == [(x['p'], bool(x.get('syl'))) for x in new]:
        return phones, spans, False
    st = max([x.get('s', 0) for x in old if _isv(x['p'])] or [0], key=lambda v: (v == 1, v == 2))
    new = [dict(x) for x in new]
    for x in new:
        if _isv(x['p']):
            x['s'] = x.get('s') or st
            break
    phones2 = phones[:idx[0]] + new + phones[idx[-1] + 1:]
    # 这几个字母重新分：音按字母平均分（够用：显示、配音都只用到“每一块有哪些音”）
    d = len(new) - len(old)
    spans2 = []
    for k, sp in enumerate(spans):
        if a <= k < a + len(grp):
            spans2.append(None)
        elif sp and sp[0] > idx[-1]:
            spans2.append([j + d for j in sp])
        else:
            spans2.append(sp)
    pos = idx[0]
    ks = list(range(a, a + len(grp)))
    per = [len(new) // len(ks) + (1 if t < len(new) % len(ks) else 0) for t in range(len(ks))]
    for k, cnt in zip(ks, per):
        spans2[k] = list(range(pos, pos + cnt))
        pos += cnt
    return phones2, spans2, True


ALPHA = 'abcdefghijklmnopqrstuvwxyz'


def _key(prefix, n):
    s = ''
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = ALPHA[r] + s
    return prefix + s


def note_say(line, lex, used):
    """关键解释的一行 → 配音：字母一个个念，/音标/ 换成音素词（真念出这个音）；行首的 a_e、u_e（元辅e 的解释）念规则的名字“元辅 e 结尾”（6.3），
    句子中间的 a_e 还念“a 后面隔一个辅音跟着 e”"""
    t = str(line or '')
    t = re.sub(r'（[^（）]*）|\([^()]*\)', '', t)
    def ipa_word(m):
        ph = from_ipa(m.group(1))
        if not ph:
            return ''
        tok = ' '.join(to_tokens(ph, stress=len([x for x in ph if _isv(x['p'])]) > 1))
        for k, v in lex.items():
            if v == tok:
                return ' ' + k + ' '
        k = _key('qzn', used[0])
        used[0] += 1
        lex[k] = tok
        return ' ' + k + ' '
    t = re.sub(r'/([^/]+)/', ipa_word, t)
    t = re.sub(r'^\s*[aeiouy]_e(?=\s*[：:])', '元辅 e 结尾', t)          # 6.3：元辅e 的解释念规则的名字“元辅 e 结尾”（画面上写“元辅e结尾（uce）”）
    t = re.sub(r'(?<![A-Za-z])([aeiouy])_e(?![A-Za-z])', r'\1 后面隔一个辅音跟着 e', t)

    def spell(m):                     # 字母组合一个个字母念（t i o n）；长的当单词念；音素词不动
        w = m.group(1)
        if w.startswith('qz') or len(w) > 4:
            return ' ' + w + ' '
        return ' ' + ' '.join(w.lower()) + ' '
    t = re.sub(r'(?<![A-Za-z])-?([A-Za-z]+)(?![A-Za-z])', spell, t)
    t = re.sub(r'[“”"]', '', t).strip()
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'\s*([，。：；、])\s*', r'\1', t)
    return t.rstrip('，；、') + ('' if re.search(r'[。！？]$', t) else '。')


# ---------------------------------------------------------------- 一个词的读音拆分
def find(data, word):
    """音节表里找这个词；带连字符的（well-known）用几个词拼起来"""
    k = word.strip().lower()
    if k in data and not k.startswith('#'):
        return data[k], ''
    parts = [p for p in re.split(r'[-\s]+', k) if p]
    if len(parts) > 1 and all(p in data for p in parts):
        chunks = []
        note = []
        for i, p in enumerate(parts):
            if i:
                chunks.append({'t': '-', 'L': [{'c': '-', 'silent': True, 'u': 0, 'k': '', 'sep': True}], 'sep': True})
            chunks += json.loads(json.dumps(data[p]['chunks']))
            note += data[p].get('note') or []
        return {'w': word, 'chunks': chunks, 'note': note, 'joined': parts}, '用 %s 拼起来的' % ' + '.join(parts)
    why = (data.get('#skipped') or {}).get(k, '')
    return None, ('音节表跳过了这个词（%s）' % why) if why else '音节表里没有这个词'


def pron(entry, word, ipa=None, chunk_ipa=None):
    """→ 视频用的读音拆分：每一块的字母（带标注）、音标、配音用的音素词；对不齐时 ok = False（只念整词）"""
    chunks = json.loads(json.dumps(entry['chunks']))
    note = list(entry.get('note') or [])
    for c in chunks:
        if c['L']:
            c['L'][-1]['end'] = True
    letters = [x for c in chunks for x in c['L'] if not x.get('sep')]
    owner = [ci for ci, c in enumerate(chunks) for x in c['L'] if not x.get('sep')]
    src, phones = '', None
    if ipa:
        phones = from_ipa(ipa)
        src = '单词表音标' if phones else ''
    if not phones:
        phones, src = lexicon_phones(word if not entry.get('joined') else ''.join(entry['joined']))
        if not phones and entry.get('joined'):
            phones = []
            for p in entry['joined']:
                ph, _ = lexicon_phones(p)
                if not ph:
                    phones = None
                    break
                phones += ph
            src = '英式词典（分开查）' if phones else ''
    res = {'w': word, 'chunks': chunks, 'note': note, 'src': src, 'ok': False, 'warn': '', 'review': entry.get('review', '')}
    marks = {'silent': False, 'combo': False, 'long': False, 'special': False}
    for x in letters:
        marks['silent'] |= bool(x.get('silent'))
        marks['combo'] |= bool(x.get('u'))
        marks['long'] |= x.get('k') == 'long'
        marks['special'] |= x.get('k') == 'special'
    res['marks'] = marks
    if not phones:
        res['warn'] = '查不到读音（词典里没有），读音拆分只念整词'
        return res
    cost, spans, dropped = align(letters, phones)
    if spans is None:
        res['warn'] = '字母和读音对不上，只念整词'
        return res
    if dropped:                                   # 表里划掉了、词典里还读的弱读元音：整词也不读（different /ˈdɪfrənt/）
        keep = [j for j in range(len(phones)) if j not in set(dropped)]
        remap = {old_j: new_j for new_j, old_j in enumerate(keep)}
        phones = [phones[j] for j in keep]
        spans = [[remap[j] for j in sp] if sp else sp for sp in spans]
    fixed = []
    for grp, new, raw in note_overrides(note):
        phones, spans, ch = apply_override(letters, phones, spans, grp, new)
        if ch:
            fixed.append('%s 照表读 /%s/' % (grp, raw))
    # 每一块的音
    per = [[] for _ in chunks]
    for k, sp in enumerate(spans):
        per[owner[k]] += sp or []
    for ci, c in enumerate(chunks):
        live = [x for x in c['L'] if not x.get('silent') and not x.get('sep')]
        if per[ci] or not any(x['c'].lower() in 'aeiouy' for x in live) or ci == 0 or not per[ci - 1]:
            continue
        j = max(per[ci - 1])
        two = {'ɪə': 'ɪ', 'ʊə': 'ʊ', 'eə': 'e'}.get(phones[j]['p'])
        if two:
            phones = phones[:j] + [dict(phones[j], p=two), {'p': 'ə', 's': 0}] + phones[j + 1:]
            per = [[x + 1 if x > j else x for x in q] for q in per]
            per[ci] = [j + 1]
    bad = []
    for ci, c in enumerate(chunks):
        if c.get('sep'):
            continue
        idx = sorted(set(per[ci]))
        c['ph'] = [phones[j] for j in idx]
        live = [x for x in c['L'] if not x.get('silent')]
        has_v = any(x['c'].lower() in 'aeiouy' for x in live)
        if not idx and live and all(x['c'].lower() in 'rhwy' for x in live):
            c['mute'] = True                      # 英音里不单独发音（ore 读 /ɔː/：r 不读），跟着前一块亮，不单独念
            continue
        if not idx and len(live) == 1 and live[0]['c'].lower() in 'aeiou':
            c['ph'] = [{'p': 'ə', 's': 0}]       # 词典里吞掉了的弱读元音（valuable 的 a）：念 /ə/
            at = max([j for q in per[:ci] for j in q] or [-1]) + 1
            phones = phones[:at] + c['ph'] + phones[at:]
            per = [[x + 1 if x >= at else x for x in q] for q in per]
            continue
        if not idx and live:
            bad.append(c['t'] + ' 没有对到音')
        elif has_v and not any(_isv(p['p']) or p.get('syl') for p in c['ph']) \
                and not any(c['ph'][k]['p'] in ('n', 'l', 'm') and not _isv(c['ph'][k - 1]['p']) for k in range(1, len(c['ph']))) \
                and not all(x['c'].lower() in 'y' for x in live if x['c'].lower() in 'aeiouy'):
            # 带元音字母的一块没对到元音：除非这个元音字母本来就弱读到听不见（every 的第二个 e）
            if not (len(live) <= 2 and cost < 3):
                bad.append(c['t'] + ' 没有元音')
    n_let = max(1, len(letters))
    res['cost'] = round(cost, 2)
    ok = not bad and cost <= 1.2 + 0.35 * n_let
    if chunk_ipa and isinstance(chunk_ipa, list):
        real = [c for c in chunks if not c.get('sep')]
        if len(chunk_ipa) == len(real):
            okm = True
            for c, s in zip(real, chunk_ipa):
                ph = from_ipa(s)
                if ph is None and str(s).strip():
                    okm = False
                    break
                c['ph'] = ph or []
            if okm:
                phones = [p for c in real for p in c['ph']]
                if not any(p.get('s') == 1 for p in phones):
                    for p in phones:
                        if _isv(p['p']):
                            p['s'] = 1
                            break
                ok, bad, src = True, [], '手写（prefs 的 sylIpa）'
    res['src'] = src
    if not ok:
        res['warn'] = '；'.join(bad) or '对得不太准（代价 %.1f）' % cost
    res['ok'] = ok
    res['fixed'] = fixed
    # 重音在哪一块：只有一个元音的词不标（/meɪk/）；只有次重音的，第一个次重音当重音
    vows = [p for p in phones if _isv(p['p']) and not p.get('syl')]
    def has_nucleus(c):                           # 这一块自己成一个音节：有元音，或者是成音节的 l、n、m（ple /pl/、tion /ʃn/）
        ph = c.get('ph') or []
        return any(_isv(q['p']) or q.get('syl') for q in ph) or any(ph[k]['p'] in ('n', 'l', 'm') and not _isv(ph[k - 1]['p']) for k in range(1, len(ph)))
    nsyl = sum(1 for c in chunks if not c.get('sep') and not c.get('mute') and has_nucleus(c))
    if len(vows) <= 1 and nsyl <= 1:
        for p in phones:
            p['s'] = 0
    elif not any(p.get('s') == 1 for p in vows):
        sec = next((p for p in vows if p.get('s') == 2), vows[0])
        sec['s'] = 1
    stress = -1
    for ci, c in enumerate(chunks):
        if any(p.get('s') == 1 and _isv(p['p']) for p in c.get('ph') or []):
            stress = ci
            break
    res['stress'] = stress
    res['ipa'] = show_ipa(phones)
    # 配音用的音素词：每一块一个，整词一个
    lex, used = {}, {}
    for ci, c in enumerate(chunks):
        if c.get('sep'):
            continue
        if c.get('mute'):
            c['ipa'] = ''
            continue
        c['ipa'] = show_ipa(c.get('ph') or [], stress_marks=False)
        toks = to_tokens(c.get('ph') or [], stress=(ci == stress))
        base = 'qz' + re.sub(r'[^a-z]', '', c['t'].lower())
        key = base
        k = 0
        while key in lex and lex[key] != ' '.join(toks):
            k += 1
            key = base + ALPHA[k % 26] * (1 + k // 26)
        if toks:
            lex[key] = ' '.join(toks)
            c['key'] = key
        used[key] = 1
    wkey = 'qz' + re.sub(r'[^a-z]', '', word.lower())
    if wkey in lex:
        wkey += 'w'
    lex[wkey] = ' '.join(to_tokens(phones))
    res['key'] = wkey
    cnt = [0]
    res['noteSay'] = [note_say(ln, lex, cnt) for ln in note]
    res['lex'] = lex
    for c in chunks:
        c.pop('ph', None)
    return res


def describe(p):
    if not p:
        return '（没有）'
    real = [c for c in p['chunks'] if not c.get('sep')]
    s = ' + '.join('%s /%s/' % (c['t'], c.get('ipa', '?')) for c in real)
    s += ' → /%s/' % p.get('ipa', '')
    if p.get('stress', -1) >= 0 and len(real) > 1:
        s += '，重音在第 %d 块（%s）' % (p['stress'] + 1, p['chunks'][p['stress']]['t'])
    s += '；音标来源：%s' % (p.get('src') or '没有')
    if p.get('fixed'):
        s += '；' + '、'.join(p['fixed'])
    if not p.get('ok'):
        s += '；⚠ ' + (p.get('warn') or '对不齐')
    if p.get('note'):
        s += '；关键解释：' + ' ｜ '.join(p['note'])
    if p.get('review'):
        s += '；表里待复核：' + p['review']
    return s


def main():
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == 'build':
        build(a[1], a[2])
    elif len(a) >= 3 and a[0] == 'show':
        data = json.load(open(a[1], encoding='utf-8'))
        for w in re.split(r'[,，]', a[2]):
            w = w.strip()
            e, how = find(data, w)
            print(w, '：', describe(pron(e, w)) if e else how, ('（' + how + '）') if e and how else '')
    elif len(a) >= 2 and a[0] == 'check':
        data = json.load(open(a[1], encoding='utf-8'))
        words = [k for k in data if not k.startswith('#')]
        bad = []
        for w in words:
            p = pron(data[w], data[w]['w'])
            if not p['ok']:
                bad.append((w, p['warn'], p.get('cost')))
        print('全表 %d 个词，对不齐 %d 个（%.1f%%）' % (len(words), len(bad), 100.0 * len(bad) / max(1, len(words))))
        for w, why, c in bad[:int(a[2]) if len(a) > 2 else 40]:
            print('  %s：%s %s' % (w, why, '' if c is None else '（%.1f）' % c))
    else:
        print(__doc__)


if __name__ == '__main__':
    main()

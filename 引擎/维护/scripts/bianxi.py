# -*- coding: utf-8 -*-
"""辨析列（2026-11 身份分工、辨析列轮，project_rules.md 第 68 条）。
总表在「组合 → 现在的含义」后面单独一列「辨析」，视频第三部分“同义词辨析”读它：
  【同义词】产品：product、produce（农产品）        ← 中文意思一样（或一个包着另一个）的几个词，都是总表里的词；本词写在最前面；最多 3 行、每行最多 6 个词
  product 是可数的“产品”；produce 是不可数的“农产品”…   ← 辨析的话（2026-11 以前写在组合列的【辨析】段，整段挪过来，一字不改）
  逻辑不同：…                                          ← 可以有：两个词构词的逻辑差在哪儿（手写的样板 produce / product 有）
这里的工具：
  split_bianxi(组合格)             → (去掉【辨析】段的组合格, 辨析文字)
  build_index(data, C)            → 按含义列建“(词性, 中文意思) → 词”的索引（只收前面没带括号的普通意思；过去式、另一种拼法不收）
  syn_lines(词, 辨析文字, …)       → 这个词的【同义词】行：辨析里点了名、中文意思对得上的排在前面，再按意思的先后
  cross_fill(cells, words)        → 同义词组里的词，本行的辨析一个也没提到的，把同组别的词那一行里提到本词的那句话抄过来（每一行自己讲清）
  fix_refs(文字)                   → 别处的“见【辨析】”改成“见辨析列”
  python3 bianxi.py <表.xlsx> [--groups 清单.xlsx]   打印统计；--groups 把全表的同义词组列成一张清单（中文意思、词性、哪些词）"""
import re, collections
import meaning as M

SEG = re.compile(r'^\s*【([^【】\n]{1,12})】')
def split_bianxi(combo):
    """组合格 → (去掉【辨析】段以后的组合格, 辨析那一段的文字（不带【辨析】两个字）)"""
    lines = str(combo or '').split('\n')
    keep, bx, cur = [], [], False
    for l in lines:
        m = SEG.match(l)
        if m:
            cur = (m.group(1) == '辨析')
            if cur:
                bx.append(l[m.end():].strip()); continue
        if cur: bx.append(l)
        else: keep.append(l)
    return '\n'.join(keep), '\n'.join(x for x in bx if x.strip())

def spell_key(w):
    k = w.lower().replace('-', '').replace(' ', '')
    for a, b in (('isation', 'ization'), ('ise', 'ize'), ('ising', 'izing'), ('yse', 'yze'), ('our', 'or'), ('tre', 'ter'), ('ll', 'l'), ('ae', 'e'), ('ogue', 'og'), ('ence', 'ense'), ('mme', 'm'), ('ey', 'ay')):
        k = k.replace(a, b)
    return k

FORM = re.compile(r'的(过去式|过去分词|复数|现在分词|比较级|最高级|第三人称|缩写|简写|另一种拼法)|英式拼写，同|美式拼写，同|^=|^（=')
LABEL = re.compile(r'^（(英|美|口|俚|旧|古|正式|非正式|喻|比喻|贬|褒|书|文|诗|计算机|电脑|网络|数|数学|物|物理|化|化学|医|医学|法|法律|语法|音|音乐|体|体育|军|军事|宗|宗教|经|经济|商|生|生物|天文|地|地理|烹饪|戏剧|航海|建筑|哲|哲学|心理|语言|统计|金融|会计|电|机械|植|动|解剖|摄影|美式|英式|口语|俚语|旧时|古时|复数|常用复数|方言|苏格兰|澳)[^（）]{0,3}）')
def terms_of(F, loose=False):
    """含义格 → [(词性, 中文意思, 是第几个意思)]。loose=False：只要前面没带括号的普通意思（建索引用）；
    loose=True：前面带限定语的（（短途）旅行）去掉括号也算（只拿来和辨析里点了名的词对）"""
    out = []
    try: ss = M.senses(F, '')
    except Exception: return out
    for k, s in enumerate(ss):
        if s['pos'] == 'phr.': continue
        t = s['text'].strip()
        if FORM.search(t): return []
        if t.startswith('（') and (not loose or LABEL.match(t)): continue
        t = re.sub(r'（[^（）]*(?:（[^（）]*）[^（）]*)*）', '', t)
        for term in re.split(r'[、，,]', t):
            term = term.strip()
            if term and not re.search(r'[A-Za-z0-9…]', term) and len(term) <= 8:
                out.append((s['pos'], term, k))
    return out

LOOSE = {}
def build_index(data, C):
    idx = collections.defaultdict(list); terms = {}; LOOSE.clear()
    for r in data:
        w = r[C['word']]
        ts = terms_of(r[C['mean']])
        terms[w] = ts
        LOOSE[w] = terms_of(r[C['mean']], loose=True)
        seen = set()
        for pos, t, k in ts:
            if (pos, t) in seen: continue
            seen.add((pos, t)); idx[(pos, t)].append((w, k))
    return idx, terms

def clause_words(text, words):
    """辨析文字里，放在每个分句开头被拿来比的英语词（总表里的）"""
    out = []
    for cl in re.split(r'[；。\n]', text):
        m = re.match(r"^\s*(?:汉语[^，：]*[，：])?\s*([A-Za-z][A-Za-z\-']*)", cl)
        if m and m.group(1) in words and m.group(1) not in out: out.append(m.group(1))
        for m2 in re.finditer(r"[，、]\s*([A-Za-z][A-Za-z\-']*)\s*(?:是|指|偏|强调|多指|更|只|才是|侧重|重在|带)", cl):
            if m2.group(1) in words and m2.group(1) not in out: out.append(m2.group(1))
        for m3 in re.finditer(r"(?:是|用|说|叫|写)\s*([A-Za-z][A-Za-z\-']*)\s*(?=$|[，（])", cl):
            if m3.group(1) in words and m3.group(1) not in out: out.append(m3.group(1))
    return out

MAXW, MAXL = 6, 3
INFL = ('s', 'es', 'd', 'ed', 'ing', 'n', 'en', 't', 'ly', 'ies', 'ied', 'er', 'est')
def same_lemma(a, b):
    a, b = a.lower(), b.lower()
    if spell_key(a) == spell_key(b): return True
    if len(a) > len(b): a, b = b, a
    if b.startswith(a) and b[len(a):] in INFL: return True
    if a.endswith('e') and b.startswith(a[:-1]) and b[len(a) - 1:] in ('ed', 'ing', 'er', 'est', 'en'): return True
    if a.endswith('y') and b.startswith(a[:-1] + 'i') and b[len(a):] in ('es', 'ed', 'er', 'est'): return True
    return False

def syn_lines(w, text, idx, terms, words, grp=None):
    """这个词的【同义词】行：先排辨析里点了名、中文意思对得上的词，再按意思的先后排索引里同义的"""
    mention = [x for x in clause_words(text, words) if x != w and not same_lemma(x, w)]
    cands = []
    mineL = LOOSE.get(w, [])
    bykey = collections.OrderedDict()
    for m in mention:
        best = None
        for pos, t, k in mineL:
            for pos2, t2, k2 in LOOSE.get(m, []):
                if pos != pos2: continue
                if t == t2: cand = (0, k + k2, t, t, t2, k)
                else:
                    a, b = (t, t2) if len(t) <= len(t2) else (t2, t)
                    if not (len(a) >= 2 and b.endswith(a)): continue
                    cand = (1, k + k2, a, t, t2, k)
                if best is None or cand < best: best = cand
        if best:
            _, _, key, t, t2, k = best
            e = bykey.setdefault(key, dict(k=k, mine=t, ms=[]))
            e['ms'].append(m + ('（%s）' % t2 if t2 != key else ''))
    for key, e in bykey.items():
        head = w + ('（%s）' % e['mine'] if e['mine'] != key else '')
        cands.append(((0, e['k']), '【同义词】%s：%s' % (key, '、'.join([head] + e['ms'][:MAXW - 1])), key))
    used = set(bykey)
    for pos, t, k in terms.get(w, []):
        if t in used: continue
        ps = [(x, kk) for x, kk in idx.get((pos, t), []) if x != w and not same_lemma(x, w)]
        if not ps: continue
        ps.sort(key=lambda z: (z[0] not in mention, z[1] != 0, z[1], len(z[0])))
        sel = []
        for x, kk in ps:
            if any(same_lemma(x, y) for y in sel): continue
            sel.append(x)
            if len(sel) >= MAXW - 1: break
        used.add(t)
        cands.append(((1, k), '【同义词】%s：%s' % (t, '、'.join([w] + sel)), t))
    cands.sort(key=lambda c: c[0])
    return [c[1] for c in cands[:MAXL]]

REF = re.compile(r'【辨析】')
def fix_refs(t):
    """别处说“见【辨析】”的，改成“见辨析列”"""
    return REF.sub('辨析列', t) if t else t


def _syn_words(cell, w):
    out = []
    for l in str(cell or '').split('\n'):
        if l.startswith('【同义词】') and '：' in l:
            for x in l.split('：', 1)[1].split('、'):
                x = re.sub(r'（[^（）]*）', '', x).strip()
                if x and x != w and x not in out: out.append(x)
    return out

def _body(cell):
    return '\n'.join(l for l in str(cell or '').split('\n') if not l.startswith('【同义词】'))

def _has(word, text):
    return re.search(r'(?<![A-Za-z])' + re.escape(word) + r'(?![A-Za-z\-])', text) is not None

def cross_fill(cells, wordlist, maxn=2):
    """cells[i] 是第 i 行的辨析格，wordlist[i] 是那一行的单词。本行有【同义词】行、辨析文字却一个同组的词也没提到的，
    从同组别的词那一行抄提到本词的那一句（最多 maxn 句）。返回 (新 cells, 补了几行)"""
    at = {}
    for i, w in enumerate(wordlist): at.setdefault(w, i)
    bodies = [_body(c) for c in cells]
    out = list(cells); n = 0
    for i, cell in enumerate(cells):
        w = wordlist[i]
        ws = _syn_words(cell, w)
        if not ws or any(_has(x, bodies[i]) for x in ws): continue
        got = []
        for x in ws:
            j = at.get(x)
            if j is None or not bodies[j]: continue
            for sent in re.split(r'(?<=。)|\n', bodies[j]):
                sent = sent.strip().rstrip('。')
                if sent and _has(w, sent) and len(sent) < 220 and not sent.startswith('逻辑不同'):
                    sent = re.sub(r'（见 %s）' % re.escape(w), '', sent)
                    if not _has(x, sent): sent = x + '：' + sent          # 那一行里没点自己的名字（主语就是它自己）：抄过来要写明说的是谁
                    if sent not in bodies[i] and all(sent != g for g in got): got.append(sent)
                    break
            if len(got) >= maxn: break
        if got:
            out[i] = '\n'.join([cell] + got); n += 1
    return out, n

if __name__ == '__main__':
    import sys
    from linetools import load_table
    hdr, C, data = load_table(sys.argv[1])
    idx, terms = build_index(data, C)
    groups = {k: [w for w, _ in v] for k, v in idx.items()}
    multi = {}
    for (pos, t), ws in groups.items():
        keep = []
        for w in ws:
            if not any(same_lemma(w, y) for y in keep): keep.append(w)
        if len(keep) >= 2: multi[(pos, t)] = keep
    print('中文意思（同一词性）被两个以上的词共用的：%d 个，涉及 %d 个词' % (len(multi), len({w for v in multi.values() for w in v})))
    if 'bx' in C:
        n = sum(1 for r in data if r[C['bx']]); m = sum(1 for r in data if '【同义词】' in str(r[C['bx']] or ''))
        print('辨析列有内容 %d 行，有【同义词】行 %d 行' % (n, m))
    if '--groups' in sys.argv:
        from openpyxl import Workbook
        wb = Workbook(); ws = wb.active; ws.title = '同义词组'
        ws.append(['中文意思', '词性', '词数', '总表里的词'])
        for (pos, t), v in sorted(multi.items(), key=lambda kv: (-len(kv[1]), kv[0][1])): ws.append([t, pos, len(v), '、'.join(v)])
        ws.column_dimensions['A'].width = 18; ws.column_dimensions['D'].width = 110; ws.freeze_panes = 'A2'
        wb.save(sys.argv[sys.argv.index('--groups') + 1]); print('清单存好了')

"""含义列（F）、例句列（G）的读写（2026-11 起）。

含义（F）：同一个词性的意思写一行，行首是词性缩写加一个空格，几个意思用“；”隔开；不写例子：
    adj. 受欢迎的；流行的、大众的；通俗的；民众的
    n. （英）酒馆、酒吧；…                      ← （英）（口）（喻）这类标签写在意思前面
    v. ① 轻拍、轻敲；（触屏）轻点                ← 同形词的 ①② 写在词性后面，第二个词从“② …”那一行起
    phr. carry on 继续；carry out 执行          ← 固定搭配、习语
  词性只用：n. v. modal v. aux. v. adj. adv. pron. prep. conj. num. art. int. phr.
  意思后面括号里只留说明（尤指…、复数 X、英式拼写，同 X、1910 年已见）。
例句（G）：每个有例子的意思一行，“意思：例句或例词”，几个例子用“；”隔开：
    受欢迎的：a popular teacher
    公开的：make it public 公之于众
  “意思”是含义里那个意思去掉括号以后的样子；同一个意思兼两种词性、写了两次的，前面加词性（v. 出口：…）。

用法：
    import meaning as M
    M.senses(F, G)    → [{'pos', 'circ', 'text', 'ex'}]：一个意思一项（text 不带例子），例句按“意思”对上
    M.to_old(F, G)    → 老的一行写法“（n.）比赛（a football match）；（v.）相配”，给按老写法读【今义】的脚本用
    M.problems(F, G)  → 不合写法的地方 [(类别, 那一行)]：no_pos / dup_pos / empty / has_example / ex_bad / ex_unmatched
    python3 meaning.py <总表.xlsx>   体检全表，统计各词性
老写法（一行一个意思、或“；”隔开括号里写词性）也认。
"""
import re
import sys

POS = ['modal v.', 'aux. v.', 'n.', 'v.', 'adj.', 'adv.', 'pron.', 'prep.', 'conj.', 'num.', 'art.', 'int.', 'phr.']
POS_ZH = {'n.': '名词', 'v.': '动词', 'modal v.': '情态动词', 'aux. v.': '助动词', 'adj.': '形容词', 'adv.': '副词',
          'pron.': '代词', 'prep.': '介词', 'conj.': '连词', 'num.': '数词', 'art.': '冠词', 'int.': '感叹词', 'phr.': '短语'}
POS_RX = re.compile(r'^(modal v\.|aux\. v\.|n\.|v\.|adj\.|adv\.|pron\.|prep\.|conj\.|num\.|art\.|int\.|phr\.)\s+(.*)$')
OLD_TAG = {'modal v.': 'v.，情态', 'aux. v.': 'v.，助动'}   # 老写法括号里不放“字母 空格 字母”，免得被当成英文例子
CJK = '\u3400-\u9fff'


def split_top(s, seps='；'):
    """在括号、引号外面的“；”处切开"""
    out, cur, d, q = [], '', 0, 0
    for ch in s:
        if ch in '（(': d += 1
        elif ch in '）)': d = max(0, d - 1)
        elif ch == '“': q += 1
        elif ch == '”': q = max(0, q - 1)
        if ch in seps and d == 0 and q == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


def lines(cell):
    return [x.strip() for x in str(cell or '').replace('\r\n', '\n').split('\n') if x.strip()]


def strip_parens(s):
    while True:
        s2 = re.sub(r'（[^（）]*）|\([^()]*\)', '', s)
        if s2 == s:
            return s
        s = s2


def key_of(text):
    """例句列里用来对上意思的“意思”：去掉括号（标签、说明），冒号换成空格"""
    k = strip_parens(text).replace('：', ' ').replace(':', ' ')
    k = re.sub(r'\s+', ' ', k).strip()
    return k or text.strip()


def _norm(k):
    return re.sub(r'[\s，,、。.；;：:“”"‘’\'!！?？…]', '', k)


def examples(G):
    """例句列 → [(词性或 '', 意思, [例子…])]"""
    out = []
    for line in lines(G):
        if '：' not in line:
            out.append(('', '', [line])); continue
        k, rest = line.split('：', 1)
        m = POS_RX.match(k.strip())
        p, k = (m.group(1), m.group(2)) if m else ('', k)
        out.append((p, k.strip(), split_top(rest.strip())))
    return out


def senses(F, G=None):
    out = []
    for line in lines(F):
        m = POS_RX.match(line)
        if not m:
            out.extend({'pos': '', 'circ': '', 'text': s, 'ex': []} for s in split_top(line))
            continue
        p, rest = m.group(1), m.group(2).strip()
        circ = ''
        mc = re.match(r'^([\u2460-\u2473])\s*', rest)
        if mc:
            circ, rest = mc.group(1), rest[mc.end():]
        for k, s in enumerate(split_top(rest)):
            out.append({'pos': p, 'circ': circ if k == 0 else '', 'text': s, 'ex': []})
    used = set()
    for p, k, exs in examples(G):
        nk = _norm(k)
        cand = [s for s in out if id(s) not in used and (not p or s['pos'] == p)]
        # 先按带标签的整句对（“（数量、程度）高的”），再按去掉括号的意思对（“高的”）
        hit = next((s for s in cand if _norm(re.sub(r'[：:]', ' ', s['text'])) == nk), None) or \
            next((s for s in cand if _norm(key_of(s['text'])) == nk), None)
        if hit:
            hit['ex'] = exs; used.add(id(hit))
    return out


def to_old(F, G=None):
    parts = []
    for s in senses(F, G):
        circ = s['circ'] + ' ' if s['circ'] else ''
        tag = f"（{OLD_TAG.get(s['pos'], s['pos'])}）" if s['pos'] and s['pos'] != 'phr.' else ''
        ex = '（' + '；'.join(s['ex']) + '）' if s['ex'] else ''
        parts.append(circ + tag + s['text'] + ex)
    return '；'.join(parts)


# 括号里的一项是不是例子（英文开头）；年代、“X 的复数”、“也叫…”这类英文开头的是说明
NOTE_EN = re.compile(r'^(\d{3,4}s?\b|\d{3,4} ?年)|的(常用)?(复数|单数|比较级|最高级|过去式|过去分词|现在分词|全拼|简称|缩写|写法|缩略|全称)(说法)?|也叫|也常作|指整个|模型运行')


def is_example(item):
    t = item.strip()
    if not re.search(r'[A-Za-z]', t) or re.match(r'^[=＝]', t) or NOTE_EN.search(t):
        return False
    return bool(re.match(r'^(如|比如|例如)\s*[A-Za-z]', t) or re.match(r'^[A-Za-z0-9“‘"\'…\.\-£$€¥%]', t))


def trailing_paren(s):
    s = s.rstrip()
    if not s.endswith(('）', ')')):
        return None
    d = 0
    for i in range(len(s) - 1, -1, -1):
        if s[i] in '）)': d += 1
        elif s[i] in '（(':
            d -= 1
            if d == 0:
                return s[i + 1:-1]
    return None


def problems(F, G=None):
    out = []
    block, seen = 0, set()
    for line in lines(F):
        m = POS_RX.match(line)
        if not m:
            out.append(('no_pos', line)); continue
        p, body = m.group(1), m.group(2).strip()
        if re.match(r'^[\u2460-\u2473]', body):
            block += 1
        if (block, p) in seen:
            out.append(('dup_pos', line))
        seen.add((block, p))
        items = split_top(re.sub(r'^[\u2460-\u2473]\s*', '', body))
        if not items:
            out.append(('empty', line)); continue
        for it in items:
            t = trailing_paren(it)
            if t and any(is_example(x) for x in split_top(t)):
                out.append(('has_example', it)); break
    if G is not None:
        got = sum(1 for s in senses(F, G) if s['ex'])
        exs_all = examples(G)
        for p, k, exs in exs_all:
            if not k:
                out.append(('ex_bad', exs[0]))
        if got < sum(1 for p, k, _ in exs_all if k):
            matched = {tuple(s['ex']) for s in senses(F, G) if s['ex']}
            for p, k, exs in exs_all:
                if k and tuple(exs) not in matched:
                    out.append(('ex_unmatched', f'{(p + " ") if p else ""}{k}：' + '；'.join(exs)))
    return out


if __name__ == '__main__':
    from openpyxl import load_workbook
    import collections
    ws = load_workbook(sys.argv[1], read_only=True)['拆分结果']
    c = collections.Counter(); ex = collections.defaultdict(list); pc = collections.Counter(); ne = 0
    for i, r in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        G = r[6] if len(r) > 18 else None          # 2026-11 起 G 列是「例句」
        for k, l in problems(r[5], G):
            c[k] += 1; ex[k].append((i, r[4], l))
        for s in senses(r[5], G):
            pc[s['pos'] or '（没写）'] += 1; ne += len(s['ex'])
    print('含义列体检：', dict(c) or '没有问题')
    print('词性：', '、'.join(f'{p} {n}' for p, n in pc.most_common()), f'（共 {sum(pc.values())} 个意思，例子 {ne} 个）')
    for k, v in ex.items():
        print('=====', k)
        for x in v[:20]: print('  ', *x)

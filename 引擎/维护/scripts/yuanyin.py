"""术语简化 + 音变原因（2026-11 视频界面轮 project_rules.md 第 97、98 条；2026-11 音变原因轮 第 99–102 条）

1. 术语简化（用户：“把原始印欧语词根简化一下，这个有点长”）：
     原始印欧语 → 印欧语（印欧语词根 *per-“向前”、印欧语的 p，英语念成 f）
     原始日耳曼语 → 日耳曼语（日耳曼语 *fram-“向前”）
   shuyu.py 换“老祖宗”时也直接写简化的说法。
2. 音变原因（视频界面轮：“先说发生了什么音变：p--f；再说明原因”；音变原因轮：“为什么要这样变最好也说一下，
   p-f 为什么可以，是发音相似还是什么原因，最好能说明白……然后再举一些例子就更好”）：
   记法后面的“音变：p 对 f：印欧语的 p，英语念成 f（…）”，凡是格林定律管的（p、t、k → f、th、h；b、d、g → p、t、k；bh、dh、gh → b、d、g），
   末尾接一段原因，分四块，块和块之间用“；”，后三块开头有记号（视频第四十二版按记号切开，画成单独一幕“为什么 p 会变成 f？”）：
     ；原因：〈总说：英语属于日耳曼语……这叫格林定律，拉丁语没有这样变〉
     ；发音：念 p，〈怎么念〉，念 f，〈怎么念〉，两个音……，所以 p 容易念成 f（两对的再接“，另外 d 和 t ……”）
     ；起因：没有定论，一种说法是……
     ；例子：拉丁语 piscis 和 fish、plenus 和 full、paucus 和 few
   · 原因里不能有句号（视频按“。辨析：”切这一行；SEG_RX 也只取到句号为止）；“发音”这一块里只用逗号，“两个音”开头的那一句是结论（视频照这几个字切）。
   · 哪几对算：PAIR（“谁对谁”→ 第几类、印欧语的音、英语的音）；一句里有几类就都写上（foot：p 对 f、d 对 t）。
   · 发音（SAY、SHORT）：p→f、t→th、k→h 讲“只差闭不闭紧 / 顶不顶住”（堵住再放开 → 留缝擦出来）；d→t、g→k 讲“只差声带振不振”；
     dh→d、bh→b 讲“只差带不带一股气”。k→h 加一句“像汉语拼音的 h”（日耳曼语的 h 本来就是汉语拼音 h 那个音）。
   · 起因（QI）：查过 Wikipedia“Grimm's law”、Stenbrenden 等——为什么这样念没有定论；第一类写“重音方式变了、气流压力加大”这一说，
     第二、三类写“一个变走、下一个补上”（拉链）这一说，并写明谁先谁后有争议。
   · 例子（EX）：都是教科书里的标准同源词，逐个对过 etymonline；先挑拉丁语（比的是希腊语那一支的挑希腊语），不够再从另一种语言补，
     标出语言。不重复这一句里已经出现的词和记法的关联词（pro ≈ for 的那一行不再举 foot、father）：只看“记：X ≈ Y”的 Y 和音变那一句，
     所以表里、目录（laili_data.py 的 MEMO、part_memo_data.py 的 SHIFT）里生成的一字不差。
   · 不加的：经法语磨掉的（catch、close）、拉丁语 v 本来念 w 的（way、will）、sub- / super-、right、light“轻的”、warm、eye……
     这些句子本身已经在讲怎么变，或者不是格林定律一条讲得清的。
   · 比的是希腊语那一支的（erg- / work、hydr- / water、the- / do），总说里写“希腊语没有这样变”。
   · pro-、trans- 的音变补一句“拉丁语还是 p / t”（ad-、dis-、ab- 本来就写了拉丁语那一边）。

用法：
  python3 yuanyin.py <表.xlsx>                  # 查：术语没简化、该加原因没加、原因不是现在这个写法的格（都应为 0）
  python3 yuanyin.py <表.xlsx> --write <新表>    # 简化术语、加或重写原因，写回（读回来逐格比）
  python3 yuanyin.py --catalog                  # 目录里的句子照现在的写法重写（laili_data.py 的 MEMO、part_memo_data.py 的 SHIFT）
  python3 yuanyin.py --files a.md b.py …        # 说明里的“原始印欧语”也换掉
  from yuanyin import add, simplify, fix, parse_why
"""
import re, sys, os

MARK = '；原因：'
OLD_RX = re.compile('原始印欧语|原始日耳曼语')

# 谁对谁（拉丁语 / 希腊语那一边，英语这一边）→ (格林定律的第几类, 印欧语的音, 英语的音)
PAIR = {('p', 'f'): (1, 'p', 'f'), ('t', 'th'): (1, 't', 'th'), ('c', 'h'): (1, 'k', 'h'), ('c', 'gh'): (1, 'k', 'h'), ('k', 'h'): (1, 'k', 'h'),
        ('b', 'f'): (1, 'p', 'f'),                    # ab-：拉丁语自己把 p 念成 b，英语这一支 p → f
        ('d', 't'): (2, 'd', 't'), ('g', 'k'): (2, 'g', 'k'), ('v', 'c'): (2, 'g', 'k'),     # come：gw 的 g → k
        ('f', 'd'): (3, 'dh', 'd'), ('f', 'b'): (3, 'bh', 'b'), ('th', 'd'): (3, 'dh', 'd')}
CAT = {1: ('p、t、k', 'f、th、h'), 2: ('b、d、g', 'p、t、k'), 3: ('bh、dh、gh', 'b、d、g')}
# 第三类：拉丁语、希腊语自己把 bh、dh、gh 念成了什么（拉丁语只在词头）
CAT3 = {'拉丁语': '它在词头把 bh、dh、gh 念成了 f、f、h', '希腊语': '它把 bh、dh、gh 念成了 ph、th、kh'}

# 发音：(念前一个音怎么动, 念后一个音怎么动, 两个音像在哪儿、差在哪儿)。“两个音”开头那一句是结论，视频照这几个字切开
SAY = {('p', 'f'): ('两片嘴唇先闭紧、再一下子放开', '下嘴唇轻贴上牙、不闭紧，气从缝里擦出来', '两个音都用嘴唇，只差闭不闭紧'),
       ('t', 'th'): ('舌尖先顶住上牙床、再一下子放开', '舌尖轻放在上下牙中间、不顶住，气从缝里擦出来', '两个音都用舌尖，只差顶不顶住'),
       ('k', 'h'): ('舌根先顶住上腭后部、再一下子放开', '舌根抬起来、不顶住，气从缝里擦出来，像汉语拼音的 h', '两个音都用舌根，只差顶不顶住'),
       ('d', 't'): ('舌尖先顶住上牙床、再放开，喉咙里的声带同时振动', '舌尖动作一样，声带不振动', '两个音舌尖动作一样，只差声带振不振'),
       ('g', 'k'): ('舌根先顶住上腭后部、再放开，喉咙里的声带同时振动', '舌根动作一样，声带不振动', '两个音舌根动作一样，只差声带振不振'),
       ('dh', 'd'): ('舌尖顶住上牙床、再放开，放开时带出一股气', '舌尖动作一样，不带这股气', '两个音只差带不带一股气'),
       ('bh', 'b'): ('两片嘴唇闭紧、再放开，放开时带出一股气', '嘴唇动作一样，不带这股气', '两个音只差带不带一股气')}
SHORT = {('p', 'f'): '都用嘴唇，只差闭不闭紧', ('t', 'th'): '都用舌尖，只差顶不顶住', ('k', 'h'): '都用舌根，只差顶不顶住',
         ('d', 't'): '舌尖动作一样，只差声带振不振', ('g', 'k'): '舌根动作一样，只差声带振不振',
         ('dh', 'd'): '只差带不带一股气', ('bh', 'b'): '只差带不带一股气'}

# 起因（按这一句有哪几类）：前面接“没有定论，一种说法是”
QI = {(1,): '重音方式变了，说话时气流压力加大，p、t、k 先带出一股气，再变成摩擦',
      (2,): 'p、t、k 变成 f、th、h 以后空出了位置，b、d、g 补上去念成了 p、t、k，这几步谁先谁后学者还有争议',
      (3,): 'b、d、g 念成 p、t、k 以后空出了位置，bh、dh、gh 丢掉那股气补了上去，这几步谁先谁后学者还有争议',
      (1, 2): '重音方式变了，说话时气流压力加大，p、t、k 先变成摩擦，空出的位置再由 b、d、g 补上，这几步谁先谁后学者还有争议',
      (2, 3): 'p、t、k 变走以后，b、d、g 补上去念成了 p、t、k，bh、dh、gh 再丢掉那股气补上去，这几步谁先谁后学者还有争议',
      (1, 3): '重音方式变了，说话时气流压力加大，p、t、k 先变成摩擦，b、d、g 和 bh、dh、gh 再一个接一个补上去，这几步谁先谁后学者还有争议'}

# 例子（印欧语的音 → 英语的音）：教科书里的标准同源词，逐个对过 etymonline；靠前的先用
EX = {('p', 'f'): {'拉丁语': [('piscis', 'fish'), ('plenus', 'full'), ('paucus', 'few'), ('pater', 'father'), ('pes', 'foot')],
                   '希腊语': [('pyr', 'fire'), ('pente', 'five'), ('pous', 'foot')]},
      ('t', 'th'): {'拉丁语': [('tres', 'three'), ('tenuis', 'thin'), ('tonare', 'thunder'), ('tu', 'thou')],
                    '希腊语': [('treis', 'three')]},
      ('k', 'h'): {'拉丁语': [('centum', 'hundred'), ('cornu', 'horn'), ('canis', 'hound'), ('cor', 'heart'), ('collis', 'hill')],
                   '希腊语': [('kardia', 'heart'), ('kyon', 'hound')]},
      ('k', 'gh'): {'拉丁语': [('noct-', 'night'), ('octo', 'eight'), ('luc-', 'light'), ('rectus', 'right'), ('centum', 'hundred'), ('cornu', 'horn')],
                    '希腊语': [('okto', 'eight')]},
      ('d', 't'): {'拉丁语': [('duo', 'two'), ('decem', 'ten'), ('dens', 'tooth'), ('edere', 'eat'), ('sedere', 'sit'), ('domare', 'tame')],
                   '希腊语': [('deka', 'ten'), ('odont-', 'tooth'), ('duo', 'two')]},
      ('g', 'k'): {'拉丁语': [('genu', 'knee'), ('granum', 'corn'), ('gelu', 'cold'), ('ager', 'acre'), ('iugum', 'yoke')],
                   '希腊语': [('gonu', 'knee'), ('genos', 'kin')]},
      ('dh', 'd'): {'拉丁语': [('fores', 'door'), ('fingere', 'dough'), ('fumus', 'dust')],
                    '希腊语': [('thygater', 'daughter'), ('thyra', 'door')]},
      ('bh', 'b'): {'拉丁语': [('frater', 'brother'), ('flos', 'bloom'), ('fundus', 'bottom'), ('fagus', 'beech')],
                    '希腊语': [('phrater', 'brother'), ('phero', 'bear')]}}

PAIR_RX = re.compile(r'^((?:[A-Za-z]+\s*对\s*[A-Za-z]+)(?:、[A-Za-z]+\s*对\s*[A-Za-z]+)*)[：:]')
SEG_RX = re.compile(r'音变：([^。\n]*)')
MEMO_Y = re.compile(r'记[：:]\s*[A-Za-z][A-Za-z()\-]*\s*[≈∽←]\s*([A-Za-z][A-Za-z\'’ \-]*?)\s*[（(]')
LABELS = ('发音', '起因', '例子')

# 整句补一点的（pro-、trans-：写出拉丁语那一边）
FIX = [('p 对 f：印欧语的 p，英语念成 f（印欧语词根 *per-“向前”', 'p 对 f：印欧语的 p，拉丁语还是 p，英语念成 f（印欧语词根 *per-“向前”'),
       ('t 对 th：印欧语的 t，英语念成 th（印欧语词根 *tere-“穿过去”', 't 对 th：印欧语的 t，拉丁语还是 t，英语念成 th（印欧语词根 *tere-“穿过去”')]


def simplify(s):
    return OLD_RX.sub(lambda m: m.group(0)[2:], s) if isinstance(s, str) else s


def pairs_of(s):
    """一句音变（“p 对 f、d 对 t：…”）→ 格林定律管的几对 [(类, 印欧语的音, 英语的音, 拉丁语那边的写法, 英语那边的写法)]"""
    m = PAIR_RX.match(s or '')
    if not m or '英语' not in s or '印欧语' not in s:
        return []
    out = []
    for x in m.group(1).split('、'):
        a, b = (y.strip() for y in x.split('对'))
        if (a, b) in PAIR:
            c, i, e = PAIR[(a, b)]
            if not any(o[1:3] == (i, e) for o in out):
                out.append((c, i, e, a, b))
    return out


def cats_of(s):
    return sorted({p[0] for p in pairs_of(s)})


def _has(word, ctx):
    w = word.rstrip('-').lower()
    return bool(re.search(r'(?<![A-Za-z])' + re.escape(w) + r'(?![A-Za-z])', ctx.lower()))


def examples(pairs, lang, ctx):
    """每一对挑几个例子（一对挑 3 个，两对各挑 2 个），不重复 ctx 里已经有的词 → 写成“拉丁语 piscis 和 fish、…”"""
    n = 3 if len(pairs) == 1 else 2
    other = '希腊语' if lang == '拉丁语' else '拉丁语'
    got, seen = [], set()
    for c, i, e, a, b in pairs:
        key = (i, 'gh') if (i, e, b) == ('k', 'h', 'gh') else (i, e)
        pool = EX.get(key, {})
        k = 0
        for lg in (lang, other):
            for la, en in pool.get(lg, []):
                if k >= n:
                    break
                if en in seen or _has(en, ctx) or _has(la, ctx):
                    continue
                got.append((lg, la, en)); seen.add(en); k += 1
    out, cur = [], ''
    for lg, la, en in got:
        out.append(('' if lg == cur else lg + ' ') + la + ' 和 ' + en)
        cur = lg
    return '、'.join(out)


def reason(pairs, lang, ctx=''):
    """原因那一段（不带“；原因：”）"""
    cats = sorted({p[0] for p in pairs})
    gen = '英语属于日耳曼语，日耳曼语两千多年前' + '，'.join(('把 %s 成批地念成了 %s' if k == 0 else '把 %s 念成了 %s') % CAT[c] for k, c in enumerate(cats)) \
        + '，这叫格林定律，' + lang + '没有这样变' + ('，' + CAT3[lang] if 3 in cats else '')
    c, i, e, a, b = pairs[0]
    A, B, C = SAY[(i, e)]
    fa = '念 %s，%s，念 %s，%s，%s，所以 %s 容易念成 %s' % (i, A, e, B, C, i, e)
    for c2, i2, e2, a2, b2 in pairs[1:2]:
        fa += '，另外 %s 和 %s %s' % (i2, e2, SHORT[(i2, e2)])
    q = QI.get(tuple(cats), QI[(1, 3)])
    qi = '没有定论，一种说法是' + (' ' if re.match('[A-Za-z]', q) else '') + q
    ex = examples(pairs, lang, ctx)
    return gen + '；发音：' + fa + '；起因：' + qi + ('；例子：' + ex if ex else '')


def add(s, y=''):
    """一句音变（“p 对 f：…”，不带“音变：”，可以已经带着原因）→ 照现在的写法接上“；原因：…”。
    y：记法的关联词（记：pro ≈ for 的 for），挑例子时避开它；已经是现在这个写法的不变（幂等）"""
    if not isinstance(s, str):
        return s
    body = s.split(MARK)[0]
    for a, b in FIX:
        body = body.replace(a, b)
    ps = pairs_of(body)
    if not ps:
        return s
    lang = '希腊语' if '希腊语' in body and '拉丁语' not in body else '拉丁语'
    return body + MARK + reason(ps, lang, body + ' ' + (y or ''))


def parse_why(why):
    """原因那一段 → {'gen': 总说, '发音': …, '起因': …, '例子': …}（视频 wordfilm.js 的 whyOf 是同一套）"""
    out, cur = {'gen': ''}, 'gen'
    for part in (why or '').split('；'):
        m = re.match(r'^(%s)：(.*)$' % '|'.join(LABELS), part)
        if m:
            cur = m.group(1); out[cur] = m.group(2)
        elif part:
            out[cur] = out[cur] + '；' + part if out.get(cur) else part
    return out


def _line_fix(line, parts):
    t = simplify(line)
    if not (parts and '音变：' in t):
        return t
    m = MEMO_Y.search(t)
    y = m.group(1) if m else ''
    return SEG_RX.sub(lambda q: '音变：' + add(q.group(1), y), t)


def fix(text, parts=True):
    """一格：术语简化；parts=True（前缀、词根、单词部分、后缀四列）再给“音变：…”加上或重写原因"""
    if not isinstance(text, str):
        return text
    return '\n'.join(_line_fix(ln, parts) for ln in text.split('\n'))


def todo(text, parts=True):
    """还没简化、该加原因没加、原因不是现在这个写法的地方（体检用）"""
    out = []
    if isinstance(text, str):
        if OLD_RX.search(text):
            out.append('术语没简化')
        if parts:
            for ln in text.split('\n'):
                m = MEMO_Y.search(ln)
                y = m.group(1) if m else ''
                for q in SEG_RX.finditer(ln):
                    s = q.group(1)
                    if add(s, y) != s:
                        out.append('原因不是现在的写法' if MARK in s else '音变没写原因')
    return out


def catalog(here):
    """目录里的句子照现在的写法重写：laili_data.py 的 MEMO（关联词是第 3 项）、part_memo_data.py 的 SHIFT（键是关联词）"""
    sys.path.insert(0, here)
    import importlib
    jobs = []
    L = importlib.import_module('laili_data')
    for k, v in L.MEMO.items():
        if v[5]:
            jobs.append(('laili_data.py', v[5], add(simplify(v[5]), v[2])))
    P = importlib.import_module('part_memo_data')
    for k, v in P.SHIFT.items():
        y = k[0] if isinstance(k, tuple) else k
        for s in (v.values() if isinstance(v, dict) else [v]):
            jobs.append(('part_memo_data.py', s, add(simplify(s), y)))
    n = {}
    for f in ('laili_data.py', 'part_memo_data.py'):
        p = os.path.join(here, f)
        t = open(p, encoding='utf-8').read()
        for g, old, new in jobs:
            if g == f and old != new:
                if old not in t:
                    if new in t:
                        continue                  # 同一句给几个写法共用（part_memo_data.py 的 ten：dec、deca、decim），换过一次了
                    raise SystemExit('%s 里找不到：%s' % (f, old[:40]))
                t = t.replace(old, new); n[f] = n.get(f, 0) + 1
        open(p, 'w', encoding='utf-8').write(t)
    print('目录里重写了：%s' % (n or '没有要改的'))


def main(a):
    here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
    if a and a[0] == '--catalog':
        return catalog(here)
    if a and a[0] == '--files':
        for p in a[1:]:
            s = open(p, encoding='utf-8').read()
            t = simplify(s)
            if t != s:
                open(p, 'w', encoding='utf-8').write(t)
            print('%s：%s' % (p, '换了' if t != s else '没有要换的'))
        return
    from openpyxl import load_workbook
    src = a[0]
    ws = load_workbook(src)['拆分结果']
    head = [c.value for c in ws[1]]
    PARTS = {i for i, h in enumerate(head) if h in ('前缀', '词根', '单词部分', '后缀')}
    ch, left, nrs = {}, [], 0
    for row in ws.iter_rows(min_row=2):
        for c in row:
            v = c.value
            if not isinstance(v, str):
                continue
            ip = c.column - 1 in PARTS
            n = fix(v, ip)
            if n != v:
                ch[(c.row, c.column - 1)] = n
                nrs += n.count(MARK)
            for k in todo(n if '--write' in a else v, ip):
                left.append((c.row, head[c.column - 1], k))
    if '--write' not in a:
        import collections
        print('还要改的：%d 处（应为 0）' % len(left), dict(collections.Counter(k for _, _, k in left)), left[:12])
        return
    out = a[a.index('--write') + 1]
    import xlsx_write
    xlsx_write.write(src, out, ch)
    wb2 = load_workbook(out); w2 = wb2['拆分结果']; bad = 0
    for row in ws.iter_rows(min_row=1):
        for c in row:
            want = ch.get((c.row, c.column - 1), c.value)
            if w2.cell(c.row, c.column).value != want:
                bad += 1
    print('改了 %d 格（这些格里一共 %d 处原因），写到 %s；读回来逐格比：%d 处不一致；还要改的 %d 处' % (len(ch), nrs, out, bad, len(left)))


if __name__ == '__main__':
    main(sys.argv[1:])

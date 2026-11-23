#!/usr/bin/env python3
"""「读音现象」列（2026-11 读音现象轮，第 124 条）：一个词里读音特别、学生容易不明白的地方，写出“现象 + 为什么”。

用户：“总表里面还差一个数据，就是一些发音比较特殊的现象没有解释，比如：speaker，这里的 p 读成了 b，但是视频没有讲出来，
很多学生可能不知道，不光要讲出这个现象，还要说为什么会这样。special 这里的 ci 为什么不读 s，education 这里的 du，exactly 的 ex
等等，你先查看一下总表，看看有多少单词存在这样的现象，然后再在总表增加一列：读音现象，专门用来说明这些现象，并做解释的；
视频里面就放在读音拆分这部分进行讲解”。

怎么找：每个词查英式词典的音（和视频读音拆分用的是同一本：Kokoro 的 lexicon-gb-en.txt），用 yinbiao.py（= 视频技能的
syllables.py）把字母一个个对到音上，再按下面十二类规则找；每一类写一行：
    【类别】字母：现象。为什么：原因。
视频技能（wordfilm.js duyinOf）照这个格式读：【】里是类别，第一个“：”前面是这个词里的那几个字母，“为什么：”前后分开；
括号（）里的是例词、古英语和拉丁语的写法，画面上写、配音不念。一格几行按字母在词里的先后排（education：先 du、再 ti）。

十二类（视频按这个顺序讲）：
  1 清辅音浊化   s 后面的 p、t、k 不送气，听着像 b、d、g（speaker、student、school、explore）
  2 ci/ti/si 读 /ʃ/ /ʒ/（special、nation、vision、sure、pleasure）
  3 du/tu 读 /dʒ/ /tʃ/（education、individual、picture、question）
  4 x 读 /ɡz/（exactly、example、exist）
  5 n 读 /ŋ/（thank、uncle、English、finger）
  6 不发音的辅音字母（know、write、light、climb、listen、hour、walk、autumn、island、guess……各有各的原因）
  7 ch 读 /k/ 或 /ʃ/（school、Christmas；machine）
  8 gh 读 /f/（enough、laugh）
  9 o 读 /ʌ/（come、love、mother、Monday）
 10 w 后面的 a、or 变音（want、water、word、work）
 11 s 读 /z/（music、rose、busy）
 12 失去爆破（doctor、picture、football）

用法：
  python3 duyin.py <总表.xlsx> --show speaker,special,education     看这几个词找出了什么
  python3 duyin.py <总表.xlsx> --report                             每一类多少个词、举例（不写表）
  python3 duyin.py <总表.xlsx> --write <新表.xlsx>                   整列写进去（没有「读音现象」列就加在最后）
词典：$WORDFILM_MODELS/kokoro-multi-lang-v1_1/lexicon-gb-en.txt（视频技能 setup.sh 装的），或者 --lex 指定。
"""
import argparse, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

COL = '读音现象'
VOWEL_L = set('aeiou')
PLOS = {'p', 'b', 't', 'd', 'k', 'ɡ'}
VOICED = {'p': 'b', 't': 'd', 'k': 'ɡ'}
ORDER = ['清辅音浊化', '读 /ʃ/', '读 /dʒ/', 'x 读 /ɡz/', 'n 读 /ŋ/', '不发音', 'ch 读', 'gh 读 /f/', 'o 读 /ʌ/', 'w 后面', 's 读 /z/', '失去爆破']


def _Y():
    import yinbiao as Y
    return Y


def phones_of(word):
    Y = _Y()
    ph, src = Y.lexicon_phones(word)
    if not ph:
        return None, None
    cost, spans, dropped = Y.align([{'c': ch} for ch in word.lower()], ph)
    if spans is None:
        return ph, None
    return ph, spans


def is_v(p):
    return _Y()._isv(p) if hasattr(_Y(), '_isv') else p in _Y().VOW


def fmt(k, tag, lt, what, why, short, tryit='', ex=''):
    """一行读音现象（第三稿）：【类别】字母：现象。为什么：讲清原因（总表里看的，可以长一点）。试一试：自己能体会的办法。一句话：视频里念的重点。（例词）"""
    t = '【%s】%s：%s为什么：%s' % (tag, lt, what, why)
    if tryit:
        t += '试一试：' + tryit
    t += '一句话：' + short
    return (k, t + (('（%s）' % ex) if ex else ''))


def find(word, cuts=()):
    """→ [(类别序号, 一行文字)]。cuts：合成词（③）两个单词的分界（字母位置），浊化、不发音不跨这个分界算"""
    w = word.strip()
    if not re.fullmatch(r"[A-Za-z]+", w):            # 短语、带连字符、带撇号的不找（各部分自己是单词，有自己的行）
        return []
    lw = w.lower()
    ph, spans = phones_of(lw)
    if not ph or spans is None:
        return []
    Y = _Y()
    P = [x['p'] for x in ph]
    S = [x.get('s', 0) for x in ph]
    n, m = len(lw), len(P)
    VOW = Y.VOW
    owner = [[] for _ in range(m)]
    for i, sp in enumerate(spans):
        for j in sp or []:
            owner[j].append(i)
    letters = lambda js: ''.join(lw[i] for i in sorted({i for j in js for i in owner[j]}))
    span = lambda i: [P[j] for j in (spans[i] or [])]
    out = []

    # 1 清辅音浊化：/s/ + /p t k/（+ r l j w）+ 重读元音，或者在词头
    for j in range(m - 2):
        if P[j] == 's' and P[j + 1] in VOICED:
            k = j + 2
            if k < m and P[k] in ('ɹ', 'r', 'l', 'j', 'w'):
                k += 1
            if k < m and P[k] in VOW and (S[k] in (1, 2) or j == 0):
                st = P[j + 1]
                idx = sorted({i for i in owner[j + 1]})
                while idx and idx[-1] + 1 < n and lw[idx[-1] + 1] == 'h' and not spans[idx[-1] + 1]:
                    idx.append(idx[-1] + 1)                 # school 的 ch：h 不单独发音，跟着 c
                s_idx = sorted({i for i in owner[j]})
                nxt = min(owner[j + 2]) if j + 2 < m and owner[j + 2] else idx[-1] + 1     # 后面那个音从第几个字母起（waste|water：t 后面的 e 不发音）
                if cuts and s_idx and idx and any(s_idx[-1] < b <= nxt for b in cuts):
                    continue                                 # 合成词两个单词的分界上（business|person、ice|cream、trust|worthy）：后一个词的 p、t、k 照常送气
                stop_l = ''.join(lw[i] for i in idx)
                s_l = letters([j])
                lt = ''.join(lw[i] for i in sorted({i for i in owner[j]} | set(idx)))
                vl = VOICED[st].replace('ɡ', 'g')
                pre = '%s 后面的 %s' % (s_l, stop_l) if s_l == 's' else '%s 读 /ks/，后面的 %s 跟在 s 后面' % (s_l, stop_l) if s_l == 'x' else '/s/ 后面的 %s' % stop_l
                # 2026-11 读音现象轮第二稿（用户：“这样解释太复杂，也不太好懂，就是说英语里面为什么要这样处理”）：
                # 讲清“英语为什么省掉这口气”（念完 s 再喷气太费劲），再用汉语“怕 / 爸”说明为什么听着像 b
                # 第三稿（用户：“sp 这种解释的不错了，能体会，也能懂；但是在视频里面要把解释再说的简短一些”）：为什么照旧，加“试一试”和视频念的“一句话”
                sl = stop_l if len(stop_l) == 1 else st
                pair, asp, una = {'p': ('念 pen，手上有一股气；再念 spend，几乎感觉不到', '怕', '爸'), 't': ('念 top，手上有一股气；再念 stop，几乎感觉不到', '他', '大'),
                                  'k': ('念 cool，手上有一股气；再念 school，几乎感觉不到', '卡', '嘎')}[st]
                out.append(fmt(0, '清辅音浊化', lt, '%s听起来像 /%s/。' % (pre + ' ' if re.search(r'[A-Za-z]$', pre) else pre, VOICED[st]),
                               '念 %s 本来要喷出一口气。可是 s 一直在往外吐气，念完 s 再马上喷一口气太费劲，英语就把这口气省了。汉语里“%s”喷气、“%s”不喷气；不喷气的 %s 就和“%s”的开头一样，所以听着像 %s。'
                               % (sl, asp, una, sl, una, vl),
                               '念完 s，气已经吐出去了，%s 就不再喷气，听起来就像“%s”的开头。' % (sl, una),
                               '手放在嘴前，%s。' % pair, 'speak、student、school 都这样'))
                break

    # 2 ci、ti、si、ssi、sci、ce、xi + 元音 → /ʃ/ /ʒ/；su（sure、pleasure、usual）→ /ʃ/ /ʒ/
    for i in range(n - 1):
        c = lw[i]
        if c not in 'cstx' or (i > 0 and lw[i - 1] + c in ('ss', 'sc') and False):
            continue
        if i + 1 < n and lw[i + 1] == 'h':
            continue
        grp = [i]
        if i > 0 and lw[i - 1] == 's' and c in 'sc':
            grp = [i - 1, i]
        sounds = [p for g in grp + ([i + 1] if i + 1 < n else []) for p in span(g)]
        hit = None
        if lw[i + 1] in 'ie' and i + 2 < n and lw[i + 2] in VOWEL_L and c in 'cstx':
            if 'ʃ' in sounds or 'ʒ' in sounds:
                hit = ''.join(lw[g] for g in grp) + lw[i + 1]
        elif c == 's' and lw[i + 1] == 'u' and ('ʃ' in sounds or 'ʒ' in sounds):
            hit = ''.join(lw[g] for g in grp) + 'u'
        if hit and not (c == 't' and 'tʃ' in sounds):
            zh = 'ʒ' if 'ʒ' in sounds and 'ʃ' not in sounds else 'ʃ'
            c0 = 'z' if zh == 'ʒ' else ('s' if c in 'sc' else 't' if c == 't' else 'ks')
            # 第三稿（用户：“cia……这些解释的目前还不是很懂，没有体会”）：英语里 s 碰上 y 的音会粘成 /ʃ/（yod coalescence），
            # 学生能体会的是 miss you 说快了像 /mɪʃuː/；单词里的 i 在元音前念得像 y，几百年前 special 念 spe-si-al，说快了 s 和 y 粘在一起
            w0 = {'c': 's', 's': 's', 't': 't', 'x': 'ks'}[c]
            v_after = lw[i + 2] if i + 2 < n else ''
            if zh == 'ʒ':
                why = ('s 夹在元音中间，先读成 /z/；%s 后面像 y 的音（%s）碰上 /z/，两个音挨得太近，说快了舌头来不及分开，就粘成了一个音 /ʒ/。英语里 z 碰上 y 常常这样：as you 说快了，听起来就像 /æʒuː/。'
                       % (hit, '这里的 u 读 you' if hit.endswith('u') else 'i 后面紧跟元音，念得像 y'))
                short, tryit, ex = 's 在这里先读成 /z/，再和后面像 y 的音说快了粘成一个音 /ʒ/，就像 as you 说快了变成 /æʒuː/。', '快速说 as you、as you，听听是不是像 /æʒuː/。', 'usual、vision、pleasure 都这样'
            elif hit.endswith('u'):
                why = '这里的 u 读 you，su 就是 s 加 you。s 和 you 的 y 挨得太近，说快了舌头来不及分开，就粘成了一个音 /ʃ/。英语里 s 碰上 y 常常这样：miss you 说快了，听起来就像 /mɪʃuː/。'
                short, tryit, ex = 's 和 you 挨得太近，说快了粘成了一个音 /ʃ/，就像 miss you 说快了变成 /mɪʃuː/。', '快速说 miss you、miss you，听听是不是变成了 /mɪʃuː/。', 'sure、sugar、pressure 都这样'
            else:
                hist = {'c': '几百年前这个词念的是 s 加 %s 加元音（special 念 spe-si-al）。' % hit[-1], 's': '', 't': '这个词尾从法语来，ti 在法语里就读 s 的音（nation 几百年前念 na-si-on）。', 'x': 'x 读 /ks/，最后是 s 的音。'}[c]
                why = ('%s%s 后面紧跟着元音 %s，%s 念得又轻又快，像 y。s 和 y 挨得太近，说快了舌头来不及分开，就粘成了一个音 /ʃ/。英语里 s 碰上 y 常常这样：miss you 说快了，听起来就像 /mɪʃuː/。'
                       % (hist, hit, v_after, hit[-1]))
                lead = {'t': 'ti 在法语里读 s 的音，', 'x': 'x 的最后是 s 的音，'}.get(c, '%s 后面紧跟元音，' % hit)
                short = '%s%s 念得像 y；s 和 y 说快了粘成一个音 /ʃ/，就像 miss you 说快了变成 /mɪʃuː/。' % (lead, hit[-1])
                tryit, ex = '快速说 miss you、miss you，听听是不是变成了 /mɪʃuː/。', '-cial、-tion、-sion 都这样：special、nation、mission'
            out.append(fmt(1, '%s 读 /%s/' % (hit, zh), hit, '%s 读 /%s/，不读 /%s/。' % (hit, zh, w0), why, short, tryit, ex))
            break

    # 3 du、tu、di、ti 读 /dʒ/ /tʃ/
    for i in range(n - 1):
        c = lw[i]
        if c not in 'dt' or lw[i + 1] not in 'ui':
            continue
        if i + 2 <= n and lw[i + 1:i + 3] in ('ch',) or (c == 'd' and lw[i + 1] == 'g'):
            continue
        sounds = span(i) + span(i + 1)
        tgt = 'dʒ' if c == 'd' else 'tʃ'
        yod = lw[i + 1] == 'u' and sounds[:2] == [c, 'j'] and (S[(spans[i + 1] or [0])[-1]] in (0, 2) or c == 'd')   # 英音 /dju/：常连读成 /dʒu/
        if (tgt in sounds or yod) and not (lw[i + 1] == 'i' and not (i + 2 < n and lw[i + 2] in VOWEL_L)):
            hit = lw[i:i + 2]
            other = ('tu', 'tʃ', 'picture、future、nature') if c == 'd' else ('du', 'dʒ', 'education、individual')
            # 第三稿（用户：“educa……还不是很懂，没有体会”“学生还会问 did you 不应该读 dju 吗，为什么最后要读 /dʒ/”）：
            # 讲清是 d 和 y 挨得太近、说快了粘在一起；用学生说过的 did you、Nice to meet you 让他们自己听出来
            y_src = '这里的 u 读 you，%s 就是 %s 加 you' % (hit, c) if lw[i + 1] == 'u' else '%s 后面紧跟元音，i 念得像 y' % hit
            if c == 'd':
                why = ('%s。d 和 y 挨得太近，说快了舌头来不及分开（d 是舌尖顶上牙后面，y 是舌面往上抬），就粘成了一个音 /dʒ/。英语里 d 碰上 y 常常这样：did you 说快了，听起来就像 /dɪdʒuː/。'
                       '慢慢一个个念可以读 /dju/，平常说话都粘成 /dʒu/。' % y_src)
                short = ('u 读 you，' if lw[i + 1] == 'u' else 'i 念得像 y，') + 'd 和 y 挨得太近，说快了粘成一个音 /dʒ/，就像 did you 说快了变成 /dɪdʒuː/。'
                tryit = '快速说 did you、did you，听听是不是变成了 /dɪdʒuː/。'
            else:
                why = ('%s。t 和 y 挨得太近，说快了舌头来不及分开，就粘成了一个音 /tʃ/。英语里 t 碰上 y 常常这样：Nice to meet you 说快了，meet you 听起来就像 /miːtʃuː/。' % y_src)
                short = ('u 读 you，' if lw[i + 1] == 'u' else 'i 念得像 y，') + 't 和 y 挨得太近，说快了粘成一个音 /tʃ/，就像 meet you 说快了变成 /miːtʃuː/。'
                tryit = '快速说 Nice to meet you，听听 meet you 是不是变成了 /miːtʃuː/。'
            out.append(fmt(2, '%s 读 /%s/' % (hit, tgt), hit, '%s 读 /%s/，不读 /%s/。' % (hit, tgt, c), why, short, tryit,
                           '%s 读 /%s/：%s' % (other[0], other[1], other[2])))
            break

    # 4 x 读 /ɡz/
    for i in range(n):
        if lw[i] == 'x' and span(i) == ['ɡ', 'z']:
            hit = lw[max(0, i - 1):i + 1] if i and lw[i - 1] == 'e' else 'x'
            # 第三稿（用户：“exact……还不是很懂，没有体会”；查的资料：重音紧跟在 x 后面、x 后面是元音时读 /ɡz/，ex 自己重读时读 /ks/，
            # 美国人常开玩笑说 exactly 听着像 eggs-actly）
            out.append(fmt(3, 'x 读 /ɡz/', hit, 'x 读 /ɡz/，不读 /ks/。',
                           '要看重音在哪儿。重音紧跟在 x 后面（e-XACT-ly、e-XAM）时，x 读 /ɡz/；ex 自己重读（EX-cellent、EX-ercise）时，x 读 /ks/。'
                           '读 /ɡz/ 更顺口：e 和后面的元音都要嗓子振动，/ɡz/ 也振动，嗓子从头到尾不用停；读 /ks/ 嗓子中间要停一下。所以 exactly 听起来像 eggs-actly（eggs，鸡蛋）。',
                           '重音紧跟在 x 后面，x 读 /ɡz/，嗓子不用停，更顺口；exactly 听起来就像 eggs-actly。',
                           '手摸着喉咙念 exam，嗓子从头到尾一直在振；再念 excellent 的 ex，中间停了一下。',
                           'exam、example、exist 读 /ɡz/；excellent、exercise 读 /ks/'))
            break

    # 5 n 在 /k/ /ɡ/ 前读 /ŋ/
    for i in range(n):
        sp = spans[i] or []
        if lw[i] == 'n' and span(i) == ['ŋ'] and sp[-1] + 1 < m and P[sp[-1] + 1] in ('k', 'ɡ'):
            nxt = letters([sp[-1] + 1])
            hit = 'n' + nxt
            out.append(fmt(4, 'n 读 /ŋ/', hit, 'n 读 /ŋ/，不读 /n/。',
                           'n 后面紧跟着 /%s/，念 /%s/ 舌根要抬起来。念 n 的时候舌根已经提前抬好了，n 就成了 /ŋ/，就是汉语“昂”的尾音。' % (P[sp[-1] + 1], P[sp[-1] + 1]),
                           'n 后面是 /%s/，舌根提前抬起来，n 就成了“昂”的尾音 /ŋ/。' % P[sp[-1] + 1],
                           '念 thank 的时候，舌尖不碰上牙，an 念得像“昂”。', 'thank、uncle、English 都这样'))
            break

    # 6 不发音的辅音字母（每种一个原因）
    # 2026-11 读音现象轮第二稿：原因用学生听得懂的话说——以前念、后来为了省劲不念了，写法没改；或者是从别的语言照抄来的写法
    SILENT = [
        (r'^kn', 0, 'k', '很久以前 know 里的 k 是念的。后来大家觉得 k 和 n 连着念太费劲，就不念 k 了，可写法一直没改。（knife、knee 也一样）'),
        (r'^wr', 0, 'w', '很久以前 write 里的 w 也是念的。后来 w 和 r 连着念太费劲，就不念 w 了，写法留着。（wrong、wrist 也一样）'),
        (r'(?<=[st])w(?=o)', 0, 'w', 'w 夹在中间，念起来拗口，很早就不念了，写法留着。（two、sword、answer）'),
        (r'^wh(?=o)', 0, 'w', 'who 这些词里的 wh 只读 /h/，w 很早就不念了。（who、whose、whole）'),
        (r'(?<!n)gn', 0, 'g', '这些词是从法语、拉丁语来的，法语里 g 在 n 前面不念，英语也跟着不念。加了后缀，g 又会念出来：sign 不念，signal 就念。'),
        (r'(?<=[aeiou])gh', 0, 'gh', '很久以前 gh 念一个从喉咙里发出的“赫”音。后来英语里没有这个音了，gh 就不念了，写法没改。（light、night、eight、daughter）'),
        (r'(?<=m)b(?![aeiouy])', 0, 'b', 'm 和 b 都要用两片嘴唇，念完 m 再念 b 是多余的，b 就省掉了。（climb、comb、lamb、thumb）'),
        (r'b(?=t)', 0, 'b', '这个 b 从来没念过：几百年前的学者照着拉丁语的写法，把 b 加进了拼写。（doubt 来自拉丁语 dubitare，debt 来自 debitum）'),
        (r'(?<=s)t(?=(l|en|m))', 0, 't', 's、t 后面又跟着一个辅音，三个连在一起太难念，中间的 t 就省掉了。（castle、listen、Christmas）'),
        (r'(?<=f)t(?=en)', 0, 't', 'f、t、n 连着念费劲，t 就省掉了。（often、soften；often 也有人念出 t）'),
        (r'^h', 0, 'h', '这些词是从法语来的，法语里 h 不念，英语也跟着不念。（hour、honest、honour）'),
        (r'(?<=[xaeiou])h(?=[aeiou])', 0, 'h', 'h 夹在两个音中间，被轻轻带过去，就不念了。（exhibit、exhausted、vehicle）'),
        (r'(?<=r)h|(?<=^g)h', 0, 'h', '这个 h 不念：rh 是从希腊语照抄来的写法（rhyme、rhythm）；ghost 的 h 是几百年前印书的人加上去的。'),
        (r'(?<=[ao])l(?=[kfm])|(?<=ou)l(?=d)', 0, 'l', '很久以前这个 l 是念的，后来被前面的 a、o 吞掉了，a、o 也跟着念长了。（walk、talk、half、calm；could 的 l 是照着 would、should 加上去的）'),
        (r'(?<=m)n$', 0, 'n', '词尾的 n 跟在 m 后面念不出来，就不念了；加了后缀又会念出来：autumn 不念，autumnal 就念。（column → columnist）'),
        (r'^is(?=l)|^ais(?=l)', 1, 's', '这个 s 是后来照着法语 isle 的样子加进拼写的，从来没念过。（island）'),
        (r'd(?=nes)|(?<=n)d(?=s)', 0, 'd', 'd 夹在两个辅音中间，念快了就省掉了。（Wednesday、handsome）'),
        (r'^p(?=[sn])|p(?=b)|p(?=t$)', 0, 'p', '希腊语来的 ps、pn 放在词头，英语念不出两个辅音连着，p 就不念了。（psychology；cupboard 的 p 被后面的 b 吞掉了；receipt 的 p 是照拉丁语加上去的）'),
        (r'(?<=s)c(?=[eiy])', 0, 'c', 'sc 在 e、i、y 前面读 /s/，c 不念，这是从拉丁语照抄来的写法。（science、scene、muscle）'),
        (r'(?<=g)u(?=[eiy])', 0, 'u', '这个 u 不念，它是个记号：告诉你前面的 g 读 /ɡ/，不读 /dʒ/。（guess、guide、guitar）'),
    ]
    SILENT_SHORT = [   # 第三稿：视频里念的“一句话”，和 SILENT 一一对应
        '以前 k 是念的，后来嫌 k、n 连着念费劲，就不念了，写法没改。',
        '以前 w 是念的，后来嫌 w、r 连着念费劲，就不念了，写法没改。',
        'w 夹在中间念着拗口，很早就不念了。',
        'w 很早就不念了，wh 只读 /h/。',
        '这些词从法语来，法语里 g 在 n 前面不念，英语跟着不念。',
        '以前 gh 念喉咙里的“赫”音，后来这个音没了，写法没改。',
        'm、b 都用嘴唇，念完 m 再念 b 是多余的，b 就省了。',
        '这个 b 从来没念过，是照着拉丁语的写法加进去的。',
        's、t 后面还有辅音，三个挤在一起太难念，t 就省了。',
        'f、t、n 连着念费劲，t 就省了。',
        '这些词从法语来，法语里 h 不念，英语跟着不念。',
        'h 夹在两个音中间，被轻轻带过去，就不念了。',
        '这个 h 是照希腊语的写法或者印书时加上的，不念。',
        '以前 l 是念的，后来被前面的 a、o 吞掉了。',
        '词尾的 n 跟在 m 后面念不出来，就不念了。',
        '这个 s 是后来照法语加进去的，从来没念过。',
        'd 夹在两个辅音中间，念快了就省掉了。',
        'ps 放在词头英语念不出来，p 就不念了。',
        'sc 在 e、i 前面读 /s/，c 不念，是照拉丁语的写法。',
        'u 不念，只是个记号：告诉你前面的 g 读 /ɡ/。',
    ]
    used = set()
    for (rx, off, lt, why), short in zip(SILENT, SILENT_SHORT):
        for mm in re.finditer(rx, lw):
            i0 = mm.start() + off
            idx = list(range(i0, i0 + len(lt)))
            if any(i >= n for i in idx) or any(spans[i] for i in idx) or (lt, why[:6]) in used:
                continue
            used.add((lt, why[:6]))
            mx = re.match(r'^(.*?)(（[^（）]*）)?$', why)
            out.append(fmt(5, '%s 不发音' % lt, lt, '%s 里的 %s 不发音。' % (lw, lt), mx.group(1), short, '', (mx.group(2) or '')[1:-1]))
            break

    # sc 在 e、i、y 前面合起来读一个 /s/（science、scene）：词典有时把 /s/ 对到 c 上、s 空着，上面的规则找不到，这里补上
    if not any(t.startswith('【c 不发音】') for _, t in out):
        for mm in re.finditer(r'sc(?=[eiy])', lw):
            i0 = mm.start()
            if (span(i0) + span(i0 + 1)) == ['s']:
                out.append(fmt(5, 'c 不发音', 'sc', 'sc 合起来读一个 /s/，c 不发音。', 'sc 在 e、i、y 前面读 /s/，c 不念，这是从拉丁语照抄来的写法。',
                               'sc 在 e、i 前面读 /s/，c 不念，是照拉丁语的写法。', '', 'science、scene、muscle'))
                break

    # 7 ch 读 /k/ 或 /ʃ/
    for i in range(n - 1):
        if lw[i:i + 2] == 'ch' and not (i and lw[i - 1] == 't'):
            snd = span(i) + span(i + 1)
            if snd == ['k']:
                out.append(fmt(6, 'ch 读 /k/', 'ch', 'ch 读 /k/，不读 /tʃ/。', '这些词是从希腊语来的。希腊语里有个读 k 的字母 χ，罗马人把它写成 ch，英语照着写，所以读 /k/。',
                               '这些词来自希腊语，希腊语的这个字母读 k，英语照抄写成了 ch。', '', 'school、Christmas、stomach'))
                break
            if snd == ['ʃ']:
                out.append(fmt(6, 'ch 读 /ʃ/', 'ch', 'ch 读 /ʃ/，不读 /tʃ/。', '这些词是从法语来的，法语里的 ch 就读 /ʃ/，英语照着念。',
                               '这些词来自法语，法语的 ch 就读 /ʃ/。', '', 'machine、chef'))
                break

    # 8 gh 读 /f/
    for i in range(n - 1):
        if lw[i:i + 2] == 'gh' and span(i) + span(i + 1) == ['f']:
            out.append(fmt(7, 'gh 读 /f/', 'gh', 'gh 读 /f/。', '很久以前 gh 念一个从喉咙里发出的“赫”音。在 enough、laugh 这些词里，这个音慢慢变成了 /f/，写法没跟着改。',
                           '以前 gh 念喉咙里的“赫”音，在这些词里慢慢变成了 /f/。', '', 'enough、laugh、cough'))
            break

    # 9 o 读 /ʌ/（单个 o，不是 oo、ou、ow、oa、oi、oy）
    for i in range(n):
        if lw[i] == 'o' and span(i) == ['ʌ'] and not (i + 1 < n and lw[i + 1] in 'ouawiy') and not (i and lw[i - 1] in 'o'):
            out.append(fmt(8, 'o 读 /ʌ/', 'o', '这里的 o 读 /ʌ/，不读 /ɒ/。',
                           '这是以前留下来的写法。有的词原来写 u，书是手抄的，u 和旁边的 m、n、v 都是一竖一竖的，连在一起分不清，就改写成了 o，读音没变；有的词原来读长音，后来读短了（mother、other）。读音变了，写法没改。',
                           '这些词的 o 原来写的是 u，手抄时怕和 m、n、v 连在一起看不清，就改写成了 o，读音没变。', '', 'come、love、Monday、mother'))
            break

    # 10 w（qu）后面的 a 读 /ɒ/ /ɔː/，wor 读 /ɜː/
    for i in range(1, n):
        if lw[i] == 'a' and (lw[i - 1] == 'w' or lw[max(0, i - 2):i] == 'qu') and span(i) in (['ɒ'], ['ɔː']) and not (i + 1 < n and lw[i + 1] in 'lw'):
            s0 = span(i)[0]
            out.append(fmt(9, 'w 后面的 a 读 /%s/' % s0, ('w' if lw[i - 1] == 'w' else 'qu') + 'a', 'a 读 /%s/，不读 /æ/。' % s0,
                           '念 w 嘴唇要撅成圆形，后面的 a 来不及把嘴张开，就跟着念成了圆嘴的 /%s/。' % s0,
                           '念 w 嘴唇撅圆，后面的 a 来不及张开，就念成了圆嘴的 /%s/。' % s0, '念 wa，嘴唇还是圆的。', 'want、watch 读 /ɒ/；warm、water 读 /ɔː/'))
            break
        if lw[i:i + 2] == 'or' and lw[i - 1] == 'w' and (span(i) == ['ɜː'] or span(i) + span(i + 1) == ['ɜː']):
            out.append(fmt(9, 'wor 读 /wɜː/', 'wor', 'or 读 /ɜː/，不读 /ɔː/。', 'w 后面的 or 读得和 bird、turn 一样。很久以前这些 or 念得很短，r 前面的短元音后来在英语里都念成了 /ɜː/。',
                           'w 后面的 or 读得和 bird、turn 一样，都是 /ɜː/。', '', 'word、work、world'))
            break

    # 11 s 读 /z/（夹在两个元音字母中间）
    for i in range(1, n - 1):
        if lw[i] == 's' and lw[i - 1] in VOWEL_L | {'y'} and lw[i + 1] in VOWEL_L | {'y'} and span(i) == ['z']:
            out.append(fmt(10, 's 读 /z/', 's', 's 读 /z/，不读 /s/。', 's 夹在两个元音中间。元音都要嗓子振动，s 读成 /z/，嗓子就不用中途停一下，念起来更顺口，所以读 /z/。',
                           's 夹在元音中间，读成 /z/ 嗓子不用停，更顺口。', '手摸着喉咙念 busy，嗓子从头到尾一直在振。', 'music、busy、visit'))
            break

    # 12 失去爆破：两个爆破音挨着（第二个也可以是 /tʃ/ /dʒ/）
    pairs = []
    for j in range(m - 1):
        if P[j] in PLOS and (P[j + 1] in PLOS or P[j + 1] in ('tʃ', 'dʒ')):
            a, b = letters([j]), letters([j + 1])
            if a and b and a != b:
                pairs.append((a, b, P[j], P[j + 1]))
    if pairs:
        a, b, pa, pb = pairs[0]
        more = '' if len(pairs) == 1 else '（%s 也一样）' % '、'.join('%s%s' % (x[0], x[1]) for x in pairs[1:])
        out.append(fmt(11, '失去爆破', a + b, '%s 的 /%s/ 只摆好嘴型、不念出来，紧接着念 /%s/%s。' % (a, pa, pb, more),
                       '/%s/ 和 /%s/ 都要先憋住一口气、再冲开。两个挨在一起，要连着憋两次、冲两次，又慢又累；所以前一个只摆好嘴型不冲开，直接念后一个，这叫失去爆破。' % (pa, pb),
                       '/%s/ 和 /%s/ 挨着，前一个只摆好嘴型、不冲开，念起来又快又顺。' % (pa, pb), '念 doctor，c 的地方舌根顶上去就停住，不松开，直接念 t。', 'doctor、football'))
    def pos(t):                       # 按字母在词里的先后讲（education：先 du、再 ti），同一处按类别
        lt = t[t.index('】') + 1:t.index('：')] if '】' in t and '：' in t else ''
        k = lw.find(lt) if lt else -1
        return k if k >= 0 else 99
    out.sort(key=lambda x: (pos(x[1]), x[0]))
    return out


def cell(word):
    return '\n'.join(t for _, t in find(word))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('table')
    ap.add_argument('--show')
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--write')
    ap.add_argument('--lex', help='英式词典 lexicon-gb-en.txt 的路径（不写就用 $WORDFILM_MODELS 里的）')
    a = ap.parse_args()
    if a.lex:
        os.environ['WORDFILM_MODELS'] = os.path.dirname(os.path.dirname(os.path.abspath(a.lex)))
    Y = _Y()
    if not os.path.exists(Y.LEX_GB):
        raise SystemExit('找不到英式词典 %s（视频技能 setup.sh 会下载；或者 --lex 指定）' % Y.LEX_GB)
    from kaodian import Table
    T = Table(a.table)
    cuts = {}                      # 合成词（③）两个单词的分界
    for r in T.data:
        w = T.v(r, '单词').strip()
        if '合成' in str(T.v(r, '类型') or ''):
            parts = [re.sub(r'[^a-z]', '', x.lower()) for x in str(T.v(r, '拆分') or '').split('+')]
            if len(parts) > 1 and ''.join(parts) == re.sub(r'[^a-z]', '', w.lower()):
                b, cs = 0, set()
                for x in parts[:-1]:
                    b += len(x); cs.add(b)
                cuts[w] = cs
    if a.show:
        for w in a.show.split(','):
            print('==', w); print('\n'.join(t for _, t in find(w, cuts.get(w, ()))) or '（没有）')
        return
    words = [T.v(r, '单词').strip() for r in T.data]
    res = {}
    for w in dict.fromkeys(words):
        res[w] = find(w, cuts.get(w, ()))
    if a.report or not a.write:
        import collections
        cnt, ex = collections.Counter(), collections.defaultdict(list)
        for w, fs in res.items():
            for k, t in fs:
                lab = t[1:t.index('】')]
                key = ORDER[k] if k < len(ORDER) else lab
                cnt[key] += 1
                if len(ex[key]) < 14:
                    ex[key].append(w)
        n_any = sum(1 for fs in res.values() if fs)
        print('总表 %d 个词（不重复），有读音现象的 %d 个' % (len(res), n_any))
        for key in ORDER:
            print('  %-10s %4d 个：%s' % (key, cnt[key], '、'.join(ex[key])))
        return
    import xlsx_write
    table = [[(None if v is None else (v if isinstance(v, (int, float)) else str(v))) for v in row] for row in T.rows]
    new_cols = {}
    if COL not in table[0]:
        for row in table:
            row.append(None)
        table[0][-1] = COL
        new_cols[len(table[0]) - 1] = (60, T.ix['考点'])
    ix = table[0].index(COL)
    n_w = 0
    for k, r in enumerate(T.data):
        t = '\n'.join(x for _, x in res.get(T.v(r, '单词').strip(), []))
        table[k + 1][ix] = t or None
        n_w += bool(t)
    xlsx_write.rebuild(a.table, a.write, table, new_cols)
    print('写好了：%s（%d 行有读音现象）' % (a.write, n_w))


if __name__ == '__main__':
    main()

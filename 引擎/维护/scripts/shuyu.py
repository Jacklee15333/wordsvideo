"""术语：表里不写“老祖宗 / 老词根 / 老音”这类口语说法，换成专业的说法（2026-11 专业术语轮，project_rules.md 第 93–96 条）。

  老祖宗 *per-“向前”           → 印欧语词根 *per-“向前”      （构拟的形式是日耳曼语的：日耳曼语 *fram-“向前”）（2026-11 视频界面轮起写简化的说法，原来写“原始印欧语 / 原始日耳曼语”）
  老祖宗的 p，英语念成 f        → 原始印欧语的 p，英语念成 f
  同一个老音 dh                → 原始印欧语的 dh
  和 … 同一个老祖宗            → 和 … 同源
  出自同一个表示“不”的老词根    → 出自同一个表示“不”的原始印欧语词根
  没写出构拟形式、也看不出是哪一层的 → 祖语词根（“祖语”是语言学里说的“祖先语言”，原始印欧语、原始日耳曼语都是）
  说的是某一种语言里的词（老祖宗是拉丁语 lancea）→ 源头

每一条只看这几个字前后紧挨着的话，不看整格——目录里的句子（laili_data.py、part_memo_data.py、sense_suffix.py、cizhui_catalog.py）
和表里的句子换出来才一样。

用法：
  python3 shuyu.py <表.xlsx>                  # 查：表里还有没有这些说法（应为 0）
  python3 shuyu.py <表.xlsx> --write <新表>    # 换掉，写回（写完读回来逐格比）
  python3 shuyu.py --files a.py b.md …        # 把这些文件里的说法也换掉（目录、说明）
  from shuyu import pro, BAD_RX                # pro(文字) → 换好的文字；BAD_RX 查还有没有
"""
import re, sys, os

# 2026-11 视频界面轮（第 97 条，用户：“把原始印欧语词根简化一下，这个有点长”）：写简化的说法“印欧语 / 日耳曼语”，表里原来的“原始…”也换掉（yuanyin.simplify）
PIE, PGM, ZU = '印欧语', '日耳曼语', '祖语词根'
BAD_RX = re.compile(r'原始印欧语|原始日耳曼语|老祖宗|(?<!古)老词根|同一个老音|同一个老词(?=有)|(?<![祖老])祖宗(?![：、；（）])')

# 构拟形式是原始日耳曼语的（查 etymonline：这些都标 Proto-Germanic）；别的带 * 的都是原始印欧语词根
PGMC = {'*aznon', '*aust-', '*fram-', '*gaduri-', '*gōda-', '*hwis-', '*kiltham', '*lisnojanan', '*liston', '*writan', '*wikō(n)-', '*laid-', '*missjan'}
_STAR = re.compile(r'\s*(?:PIE\s*)?(\*[^\s“”，；。）（、：:\n/]+)')
_PGM_SHAPE = re.compile(r'(?:janan|jan|anan|az|iz|uz|ōn?)\)?-?$')


def _star(m):
    s = _STAR.match(m.string, m.end())
    return s.group(1) if s else ''


def _root(m):
    """后面跟着构拟形式时用哪个词：原始印欧语词根 / 原始日耳曼语"""
    st = _star(m)
    if st and (st in PGMC or _PGM_SHAPE.search(st)):
        return PGM + ('词根' if re.search('(同一个|出一个|同出)$', m.string[:m.start()]) else '')      # “和 lead 同一个原始日耳曼语词根 *laid-”
    return PIE + '词根'


def _near(m, n=10):
    """没写构拟形式的：紧挨着说到拉丁语、希腊语、梵语（和英语对着讲），就是原始印欧语词根；看不出来的叫“祖语词根”"""
    s = m.string
    return PIE + '词根' if re.search('拉丁语|希腊语|梵语|印欧', s[max(0, m.start() - n):m.end() + n]) else ZU


_NORM = {'印欧语词根': PIE + '词根', '印欧词根': PIE + '词根', '印欧语的': PIE + '的', '印欧语里': PIE + '里', '印欧语': PIE, 'PIE': PIE}
_FOLLOW = r'(?!\s*[\*“]|在|还|到了|得到)'

RULES = [
    # —— 指明了是哪一支的
    (r'日耳曼老祖宗', PGM + '形式'),
    (r'印欧老祖宗的(?=\s*[a-z]{1,3}(?![a-z]))', PIE + '的'),
    (r'印欧老祖宗', PIE + '词根'),
    (r'(个|的)日耳曼老词根', r'\1' + PGM + '词根'),
    (r'这些语言的老祖宗', '这些语言共同的祖语'),
    (r'共同的老祖宗(?=（原始印欧语)', '共同的祖语'),
    # —— “老祖宗是印欧语 *…”：后面已经说了是哪种语言，只换成“源头”；“印欧语 / PIE”写全成“原始印欧语”
    (r'老祖宗((?:也|都|还|就)?是)\s*(?:原始)?(印欧语词根|印欧词根|印欧语的|印欧语里|印欧语|PIE)', lambda m: '源头' + m.group(1) + _NORM[m.group(2)]),
    (r'老祖宗((?:也|都|还|就)?是)(?=原始日耳曼|日耳曼|希腊语|拉丁语|另一个|一个|表示|指示)', r'源头\1'),
    # —— 同一个老祖宗（后面没有跟词根）：同源
    (r'(出自|来自|从|以)同一个老祖宗' + _FOLLOW, lambda m: m.group(1) + '同一个' + _near(m)),
    (r'(?<![不本])是同一个老祖宗' + _FOLLOW, '同源'),
    (r'同出?一个老祖宗' + _FOLLOW, '同源'),
    (r'是一个老祖宗' + _FOLLOW, '同源'),
    (r'(共同的|不同的)老祖宗', r'\1源头'),
    (r'同一个老祖宗(?=在|还|到了|得到)', lambda m: '同一个' + _near(m)),
    # —— 音
    (r'老祖宗的(?=\s*[a-z]{1,3}(?![a-z]))', PIE + '的'),
    (r'老祖宗(?=(?:开头)?是\s*[a-z]{1,3}\s*[两三]个音)', PIE + '里'),
    (r'老祖宗(?=词首的)', PIE),
    (r'同一个老音(?=\s*[a-z])', PIE + '的'),
    (r'同一个老词(?=有两种词尾)', '同一个' + PIE + '的词'),
    # —— 后面跟着构拟的形式（*per-）
    (r'老祖宗\s*PIE(?=\s*\*)', PIE + '词根'),
    (r'老祖宗(?=\s*\*)', _root),
    (r'老祖宗((?:也许|很可能|可能|似乎|一般构拟为|大概|“据说”)?(?:也|都|还|就)?(?:是|构拟为)?)(?=\s*\*)', lambda m: _root(m) + m.group(1)),
    # —— 没写出形式，只说意思
    (r'(?<=和英语的 un- 是远亲，)老祖宗', PIE + '词根'),
    (r'老祖宗的(?=(?:基本)?意思|本义)', lambda m: _near(m) + '的'),
    (r'老祖宗(?=(?:也许|很可能|似乎|大概)?(?:也|都|还|就)?(?:是|意思是)?“)', _near),
    (r'(?<=”的)老祖宗', _near),
    (r'(这个|那个|同音的)老祖宗', lambda m: m.group(1) + _near(m)),
    (r'两个老祖宗(?=只是同音)', '两个词根'),
    # —— 老词根
    (r'(?<!古)老词根(?=\s*\*)', _root),
    (r'((?:词典说|一说)[^。；，]*出自同一个(?:表示[^。；，]{1,12}的)?|它们出自同一个(?:表示[^。；，]{1,12}的)?|“?活的”?，也出自这个|出自同一个表示“?活”?的)老词根', lambda m: m.group(1) + PIE + '词根'),
    (r'同一个老词根(?=既是|的另一支)', '同一个' + PIE + '词根'),
    (r'(?<!古)老词根', _near),
    # —— 剩下的
    (r'老祖宗', '源头'),
]
_C = [(re.compile(a), b) for a, b in RULES]

# 整句重写的（2026-11：用户指出 pre- / pro- / fore- 的关系容易看成“fore- 也是拉丁语来的”）
WHOLE = [
    ('pre- 和 pro- 不是一个变出另一个（不像 duc、duct 那样是动词原形和过去分词），它们是同一个老词根在拉丁语里长出的两个介词（prae“在前面”、pro“向前”，老祖宗是 *per-“向前”），是一对兄弟；'
     'fore- 和 pre-、pro- 出自同一个老词根，是它在英语里的样子，老祖宗的 p 英语念成 f',
     'pre- 和 pro- 不是一个变出另一个（不像 duc、duct 那样是动词原形和过去分词），它们是拉丁语里两个同源的介词（prae“在前面”、pro“向前”，都来自原始印欧语词根 *per-“向前”）；'
     'fore- 和 pre-、pro- 同源，但它是英语本族的前缀，不是从拉丁语来的（古英语 fore 也来自 *per-，原始印欧语的 p 到英语这一支变成 f，这叫格林定律）'),
]


# 2026-11 本族词轮（第 125 条，用户：“speak，-er 不要说英语本来就有，换成英语本土词，英语本土后缀，英语本土前缀，英语本土词根；要用更专业的”）：
# 英语词汇学按来源把词分成“本族语词（native words）”和“外来语词（borrowed words）”（自考《英语词汇学》），表里本来也多半写“英语本族”，
# 所以统一写“英语本族词 / 英语本族前缀 / 英语本族后缀 / 英语本族词根”；“英语自己的…”也换成“英语本族的…”，“英语自己新造、自己用…”换成“英语里…”
BZ_COL = {'前缀': '前缀', '后缀': '后缀', '词根': '词根', '单词部分': '词'}
BZ_BAD = re.compile(r'(?<!古)英语本来就有|英语自己')


def benzu(text, col=None):
    """“英语本来就有 / 英语自己的”→ 专业说法（col：这一格在哪一列，决定写“本族前缀 / 后缀 / 词根 / 词”）"""
    if not isinstance(text, str) or not re.search('本来就有|英语自己', text):
        return text
    t = re.sub(r'(?<!古)英语本来就有的(前缀|后缀|词根|词)', r'英语本族\1', text)
    t = re.sub(r'(?<!古)英语本来就有的', '英语本族的', t)
    if col in BZ_COL:
        t = re.sub(r'(?<!古)英语本来就有(?=[，；。）、：:\s]|$)', '英语本族' + BZ_COL[col], t)
    t = t.replace('英语自己的样子', '英语的样子')
    t = re.sub(r'英语自己的(老)?词(?![根尾缀])', lambda m: '英语本族的老词' if m.group(1) else '英语本族词', t)
    t = t.replace('英语自己的', '英语本族的')
    t = t.replace('英语自己原有', '英语本族原有')
    t = t.replace('英语自己', '英语里')          # 剩下的都是“英语自己拼出来、自己拿 X 加 -ment、古英语自己有…”：说的是在英语里怎么造词，写“英语里”
    return t


def pro(text, log=None):
    """把一段话里的口语说法换成专业说法。log（列表）给了就记下每一处用的是第几条规则"""
    if not isinstance(text, str) or not re.search('老祖宗|老词根|老音|老词|原始印欧语|原始日耳曼语', text):
        return text
    out = text
    for a, b in WHOLE:
        if a in out:
            out = out.replace(a, b)
            if log is not None:
                log.append((-1, a[:30], b[:30]))
    for k, (rx, rep) in enumerate(_C):
        def f(m, k=k, rep=rep):
            r = rep(m) if callable(rep) else m.expand(rep)
            if log is not None:
                log.append((k, m.string[max(0, m.start() - 16):m.end() + 18], r))
            return r
        out = rx.sub(f, out)
    return re.sub('原始(印欧语|日耳曼语)', r'\1', out)


def main(a):
    here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
    if a and a[0] == '--files':
        for p in a[1:]:
            s = open(p, encoding='utf-8').read(); t = pro(s)
            if t != s:
                open(p, 'w', encoding='utf-8').write(t)
            print('%s：%s' % (p, '换了' if t != s else '没有要换的'))
        return
    from openpyxl import load_workbook
    src = a[0]
    ws = load_workbook(src)['拆分结果']
    ch, left, bz_left = {}, [], []
    hdr = [c.value for c in ws[1]]
    for row in ws.iter_rows(min_row=2):
        for c in row:
            v = c.value
            if not isinstance(v, str):
                continue
            n = pro(benzu(v, hdr[c.column - 1] if c.column - 1 < len(hdr) else None))   # 第 125 条：本族词说法
            if BZ_BAD.search(n):
                bz_left.append((c.row, hdr[c.column - 1], BZ_BAD.search(n).group(0)))
            if n != v:
                ch[(c.row, c.column - 1)] = n
            if BAD_RX.search(n if '--write' in a else v):
                left.append((c.row, c.column, BAD_RX.search(n if '--write' in a else v).group(0)))
    if '--write' not in a:
        print('表里还有口语说法的格：%d（应为 0）' % len(left), left[:20])
        print('要换成“英语本族…”的格：%d' % sum(1 for k in ch), '；换完还剩：%d' % len(bz_left), bz_left[:8])
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
    print('换了 %d 格，写到 %s；读回来逐格比：%d 处不一致；还剩口语说法 %d 格；还剩“英语本来就有 / 英语自己” %d 格 %s' % (len(ch), out, bad, len(left), len(bz_left), bz_left[:8]))


if __name__ == '__main__':
    main(sys.argv[1:])

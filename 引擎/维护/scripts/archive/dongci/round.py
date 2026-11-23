"""动词变化形式轮（2026-11）的改表脚本，只作记录。用法：python3 round.py <源表.xlsx> <新表.xlsx> [--show 单词,单词]
不规则动词的过去式、过去分词 154 个（made、wrote、written、taken……）：
  组合列（N）：第一行“write（写）→ written =“被写下来的””，下面先讲这个形式的作用——过去式“说这件事在过去发生、已经结束了”，
             过去分词“有完成、被动两层意思：跟在 have 后面是已经…了，跟在 be 后面是被…”（不及物动词的过去分词只有“已经…了”），
             再讲过去分词当形容词就是“被…了的”，最后是意思再往下变的步骤；【语法】补上三种形式（write – wrote – written）。
             原来那几条把“过去分词当形容词”标成用词规律的（done、built、spent、sunk、given……）去掉：这是语法，不算用词规律。
  音变列（P）：讲清这个形式怎么变成今天的样子；有字母变化的写成【字母变化】链（macode → makede → made），下面每一步一行，
             原有的【同形异义】【合成】【异干】等标签段落照原文留在后面。
写法见 vdata1.py、vdata2.py（模板在 vhelp.py），规矩见 references/project_rules.md 第 47 条。"""
import os, sys, re, json, copy, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from fixlib import Book
import cols as C
from vdata1 import E as E1
from vdata2 import E as E2

E = dict(E1); E.update(E2)
CIRC = '①②③④⑤⑥⑦⑧⑨⑩'

# 原形 → (过去式, 过去分词)
PARTS = {
 'make': ('made', 'made'), 'learn': ('learnt / learned', 'learnt / learned'), 'think': ('thought', 'thought'), 'show': ('showed', 'shown / showed'),
 'take': ('took', 'taken'), 'mistake': ('mistook', 'mistaken'), 'say': ('said', 'said'), 'see': ('saw', 'seen'), 'oversee': ('oversaw', 'overseen'),
 'find': ('found', 'found'), 'get': ('got', 'got（美式 gotten）'), 'forget': ('forgot', 'forgotten'), 'bear': ('bore', 'born / borne'),
 'feel': ('felt', 'felt'), 'keep': ('kept', 'kept'), 'tell': ('told', 'told'), 'become': ('became', 'become'), 'come': ('came', 'come'),
 'write': ('wrote', 'written'), 'rewrite': ('rewrote', 'rewritten'), 'understand': ('understood', 'understood'),
 'misunderstand': ('misunderstood', 'misunderstood'), 'stand': ('stood', 'stood'), 'wake': ('woke', 'woken'), 'awake': ('awoke', 'awoken'),
 'build': ('built', 'built'), 'rebuild': ('rebuilt', 'rebuilt'), 'be': ('was / were', 'been'), 'swear': ('swore', 'sworn'),
 'bring': ('brought', 'brought'), 'know': ('knew', 'known'), 'mean': ('meant', 'meant'), 'choose': ('chose', 'chosen'),
 'light': ('lit / lighted', 'lit / lighted'), 'grow': ('grew', 'grown'), 'outgrow': ('outgrew', 'outgrown'), 'go': ('went', 'gone'),
 'undergo': ('underwent', 'undergone'), 'give': ('gave', 'given'), 'forgive': ('forgave', 'forgiven'), 'begin': ('began', 'begun'),
 'run': ('ran', 'run'), 'teach': ('taught', 'taught'), 'speak': ('spoke', 'spoken'), 'sit': ('sat', 'sat'), 'break': ('broke', 'broken'),
 'lose': ('lost', 'lost'), 'pay': ('paid', 'paid'), 'do': ('did', 'done'), 'redo': ('redid', 'redone'), 'catch': ('caught', 'caught'),
 'wear': ('wore', 'worn'), 'win': ('won', 'won'), 'hold': ('held', 'held'), 'spend': ('spent', 'spent'), 'spin': ('spun', 'spun'),
 'lead': ('led', 'led'), 'hear': ('heard', 'heard'), 'overhear': ('overheard', 'overheard'), 'ride': ('rode', 'ridden'), 'meet': ('met', 'met'),
 'drink': ('drank', 'drunk'), 'fall': ('fell', 'fallen'), 'hide': ('hid', 'hidden'), 'send': ('sent', 'sent'), 'sleep': ('slept', 'slept'),
 'draw': ('drew', 'drawn'), 'withdraw': ('withdrew', 'withdrawn'), 'fight': ('fought', 'fought'), 'lay': ('laid', 'laid'),
 'prove': ('proved', 'proved / proven'), 'rise': ('rose', 'risen'), 'arise': ('arose', 'arisen'), 'speed': ('sped / speeded', 'sped / speeded'),
 'deal': ('dealt', 'dealt'), 'drive': ('drove', 'driven'), 'smell': ('smelt / smelled', 'smelt / smelled'), 'fly': ('flew', 'flown'),
 'flee': ('fled', 'fled'), 'sell': ('sold', 'sold'), 'feed': ('fed', 'fed'), 'buy': ('bought', 'bought'), 'shine': ('shone', 'shone'),
 'weave': ('wove', 'woven'), 'shake': ('shook', 'shaken'), 'stick': ('stuck', 'stuck'), 'throw': ('threw', 'thrown'),
 'burn': ('burnt / burned', 'burnt / burned'), 'dig': ('dug', 'dug'), 'hang': ('hung', 'hung'), 'strike': ('struck', 'struck'),
 'tear': ('tore', 'torn'), 'swim': ('swam', 'swum'), 'eat': ('ate', 'eaten'), 'sow': ('sowed', 'sown / sowed'), 'freeze': ('froze', 'frozen'),
 'sing': ('sang', 'sung'), 'blow': ('blew', 'blown'), 'ring': ('rang', 'rung'), 'shoot': ('shot', 'shot'), 'reshoot': ('reshot', 'reshot'),
 'bend': ('bent', 'bent'), 'bind': ('bound', 'bound'), 'seek': ('sought', 'sought'), 'lend': ('lent', 'lent'),
 'kneel': ('knelt / kneeled', 'knelt / kneeled'), 'slide': ('slid', 'slid'), 'sweep': ('swept', 'swept'), 'steal': ('stole', 'stolen'),
 'sink': ('sank', 'sunk'), 'sew': ('sewed', 'sewn / sewed'), 'cling': ('clung', 'clung'), 'sneak': ('sneaked / snuck', 'sneaked / snuck'),
 'sting': ('stung', 'stung'), 'swing': ('swung', 'swung'), 'weep': ('wept', 'wept'), 'stride': ('strode', 'stridden'),
 'beat': ('beat', 'beaten'), 'bite': ('bit', 'bitten'), 'forbid': ('forbade', 'forbidden'),
}
SEG = re.compile(r'^\s*【([^【】\n]{1,10})】')


def split_n(N):
    L = str(N or '').split('\n')
    k = next((i for i in range(1, len(L)) if SEG.match(L[i])), len(L))
    return L[0], L[1:k], L[k:]


def number(steps):
    out, n = [], 0
    for s in steps:
        if s.startswith('# '):
            out.append(CIRC[n] + ' ' + s[2:]); n += 1
        else:
            out.append(s)
    return out


def forms_note(word, base, role):
    past, pp = PARTS[base]
    f = f'{base} – {past} – {pp}'
    if role == 'p':
        note = f'：{word} 只当过去式，不能跟在 have、be 后面'
    elif role == 'pp':
        note = f'：{word} 是过去分词，跟在 have、be 后面，或当形容词'
    elif past == pp:
        note = '：过去式、过去分词同形'
    else:
        note = f'：{word} 既是过去式，也是过去分词'
    return f, note


def build_n(word, base, role, old, e):
    first, logic, segs = split_n(old)
    l1 = '【构词逻辑】' + e['l1'] if e.get('l1') else first
    # 功能步骤（过去式、过去分词）的结果要短（视频把结果写成大字）：结果里的英文整句挪到【语法】那一行当例句
    exs = []
    def pull(m):
        exs.append(m.group(1).strip()); return ''
    st = [re.sub(r'（([^（）]*[A-Za-z][^（）]*[.!?][^（）]*)）', pull, x) if x.startswith('# ') else x for x in e['st']]
    steps = number(st)
    if e.get('keepsteps'):
        steps += [l for l in logic if re.match(r'^\s*[→⇒]', l)]
    drop = set(e.get('segdrop', []))
    rep = e.get('segrep', {})
    out = []
    for s in segs:
        lab = SEG.match(s).group(1) if SEG.match(s) else None
        if lab in drop:
            continue
        out.append(rep.pop(lab) if lab in rep else s)
    out += list(rep.values())
    f, note = forms_note(word, base, role)
    note = e.get('formsnote', note)
    head = f.split('（')[0]
    ex = ('（' + ' / '.join(exs) + '）') if exs else ''
    g = next((i for i, s in enumerate(out) if s.startswith('【语法】')), None)
    if not any(head in s for s in out):
        if g is not None:
            out[g] = '【语法】' + f + note + ex + '；' + out[g][len('【语法】'):]
        else:
            out.append('【语法】' + f + note + ex)
    elif ex:
        if g is not None:
            out[g] = out[g].rstrip('。') + '；例：' + ex.strip('（）')
        else:
            out.append('【语法】例：' + ex.strip('（）'))
    return '\n'.join([l1] + [x.replace('→ （', '→（') for x in steps] + out)


def old_p_parts(P):
    """原来的音变列 → (没有标签的话, [标签段落])；一行里“…。【同形异义】…”这样接着写的，从【处切开"""
    plain, labeled = [], []
    for line in str(P or '').split('\n'):
        if not line.strip():
            continue
        i = line.find('【')
        if i < 0:
            plain.append(line); continue
        if i > 0:
            plain.append(line[:i])
        for m in re.finditer(r'【[^】]+】(?:(?!【[^】]{1,10}】).)*', line[i:]):
            labeled.append(m.group(0).rstrip('。； '))
    return plain, labeled


def build_p(old, e):
    plain, labeled = old_p_parts(old)
    mine = e['P']
    have = set(re.findall(r'(?m)^【([^】]+)】', mine))
    keep = [s for s in labeled if SEG.match(s).group(1) not in have | set(e.get('pdrop', [])) | {'字母变化'}]
    return mine + ('\n' + '\n'.join(keep) if keep else ''), plain, keep


def main():
    from vlist import ITEMS as IT
    ITEMS = [(w, base, role) for w, base, role, _ in IT]
    ROW = {w: r for w, _, _, r in IT}
    SRC, OUT = sys.argv[1], sys.argv[2]
    show = sys.argv[sys.argv.index('--show') + 1].split(',') if '--show' in sys.argv else []
    b = Book(SRC, tag='动词变化形式')
    ws = b.ws
    assert set(E) == {w for w, _, _ in ITEMS}, (set(E) ^ {w for w, _, _ in ITEMS})
    dropped = []
    for word, base, role in ITEMS:
        r = ROW[word]
        assert str(ws.cell(r, C.WORD).value) == word, (word, r)
        e = E[word]
        oldN = str(ws.cell(r, C.COMBO).value or '')
        oldP = str(ws.cell(r, C.SOUND).value or '')
        newN = build_n(word, base, role, oldN, e)
        newP, plain, keep = build_p(oldP, e)
        dropped.append((word, plain))
        if word in show:
            print('=====', word); print(newN); print('--- P'); print(newP); print('--- 去掉的原话：', plain)
        ws.cell(r, C.COMBO).value = newN
        ws.cell(r, C.SOUND).value = newP
        what = {'p': '过去式', 'pp': '过去分词', 'b': '过去式、过去分词'}[role]
        chain = newP.split('\n')[0]
        how = ('音变列写成字母变化链（' + ' → '.join(re.findall(r"(\*?[A-Za-z][A-Za-z'’\-]*)\s*（", chain)) + '），下面每一步一行'
               if chain.startswith('【字母变化】') else '音变列讲清这个形式怎么变成今天的样子')
        fn = {'p': '过去发生、已经结束', 'pp': '完成、被动', 'b': '过去发生；完成、被动'}[role]
        b.note(r, f'组合列先讲{what}的作用（{fn}）再讲意思怎么来，【语法】补三种形式；{how}')
        b._fit(r)
    if '--dry' in sys.argv:
        return dropped
    nchain = sum(1 for w, _, _ in ITEMS if E[w]['P'].startswith('【字母变化】'))
    b.log += [
     ('已修正', None, '动词变化形式',
      f'不规则动词的过去式、过去分词 {len(ITEMS)} 个（made、took、written、found……），组合列多只写“当动词：做了 / 当形容词：被做出来的”，没讲过去式、过去分词各起什么作用，也没讲这个作用怎么带出现在的意思；'
      '音变列多只有一句（made：“中古英语 maked 中间的 k 脱落，缩成 made”），关键的一步没讲（k 掉了以后怎么成了 made，末尾的 e 是哪来的）',
      '组合列：第一行“write（写）→ written =“被写下来的””，下面先讲这个形式的作用——过去式“说这件事在过去发生、已经结束了”，过去分词“有完成、被动两层意思：跟在 have 后面是已经…了，跟在 be 后面是被…”（不及物动词的过去分词只有“已经…了”），'
      f'过去分词当形容词就是“被…了的”，再接意思往下变的步骤；【语法】补三种形式（write – wrote – written）。音变列：{nchain} 个写成字母变化链（macode → makede → made、wrat → wroot → wrote、funden → founden → found），下面每一步一行；'
      f'其余 {len(ITEMS) - nchain} 个（sang、began、stuck、带前缀的 mistook、understood……）写成一段说明。中间形式对照 etymonline。逐行见 U 列“动词变化形式：…”'),
     ('已修正', None, '动词变化形式（用词规律）',
      '过去分词当形容词被标成了用词规律：built、done、spent、sunk 标“名词放在别的名词前面，也能当形容词用”，given、shot 标“表示东西、性质的词，也能直接当动词用”，bent 标“表示性质、状态的词，也拿来叫有这种性质的人”，worn 标“说动物、东西的词，也拿来比喻人”；usage_rules.md 说“被…了的”形式当形容词是语法，不算用词规律',
      '这 8 处规律行去掉，改在步骤里讲“过去分词当形容词就是被…了的”；shot 当名词“子弹”的那一条（表示动作的词，也能直接当名词用）保留。「用词规律一览」按全表重算'),
     ('已修正', ROW['worn'], 'worn',
      '音变列写着“古英语过去分词 geworen”；etymonline wear 条目说古英语 werian 是规则动词（过去式、过去分词 wered），14 世纪才照 bear、tear 改成 wore、worn',
      '改成“wear 的过去分词本是规则的 wered；14 世纪照押韵的 bear – born、tear – torn 改成 o 再加 -n”'),
    ]
    # ---------------- 说明 ----------------
    S = b.wb['说明']
    def find_row(a, bstart=None):
        for rr in range(1, S.max_row + 1):
            if S.cell(rr, 1).value == a and (bstart is None or str(S.cell(rr, 2).value or '').startswith(bstart)):
                return rr
        raise KeyError(a)
    def fit_height(rr):
        w = S.column_dimensions['B'].width or 60
        dw = sum(2 if ord(ch) > 0x2E80 else 1 for ch in str(S.cell(rr, 2).value))
        S.row_dimensions[rr].height = max(S.row_dimensions[rr].height or 17.25, 17.25 * math.ceil(dw / max(10, w - 2)))
    rN = find_row('N 组合 → 现在的含义')
    S.cell(rN, 2).value = str(S.cell(rN, 2).value).rstrip('。') + ('。动词的过去式、过去分词（made、written）先讲这个形式的作用：过去式“说这件事在过去发生、已经结束了”，'
        '过去分词“有完成、被动两层意思：跟在 have 后面是已经…了，跟在 be 后面是被…”（不及物动词的过去分词只有“已经…了”），过去分词当形容词就是“被…了的”，再讲意思往下怎么变；【语法】写三种形式（write – wrote – written）。')
    fit_height(rN)
    rP = find_row('P 音变 / 字母变化')
    S.cell(rP, 2).value = str(S.cell(rP, 2).value).rstrip('。') + ('。不规则动词的过去式、过去分词（made、wrote、written）讲清这个形式怎么变成今天的样子：'
        '有字母变化的也写成链（macode（古英语）→ makede（中古英语）→ made（中古英语、英语）），① 讲古英语的三种形式（强变化动词靠换元音：wrītan – wrāt – writen），下面每一步一行。')
    fit_height(rP)
    r0 = S.max_row
    assert S.cell(r0, 1).value == '字母变化同源词', S.cell(r0, 1).value
    rn = r0 + 1
    for c in range(1, 5):
        S.cell(rn, c)._style = copy.copy(S.cell(r0, c)._style)
    S.cell(rn, 1).value = '动词变化形式'
    S.cell(rn, 2).value = (f'不规则动词的过去式、过去分词 {len(ITEMS)} 个（made、took、written、found……）：组合列先讲这个形式的作用（过去式：过去发生、已经结束；过去分词：完成、被动；当形容词：“被…了的”），'
                           f'再讲意思怎么来，【语法】补三种形式；音变列讲清这个形式怎么变成今天的样子，{nchain} 个写成字母变化链（made：macode → makede → made，k 掉了以后 ma-ke-de 缩成 ma-de）。'
                           '过去分词当形容词标成用词规律的 8 处去掉（这是语法，不算规律）。逐行见 U 列“动词变化形式：…”。')
    S.cell(rn, 4).value = '=COUNTIF(拆分结果!$U$2:$U$9294,"*动词变化形式*")'
    S.row_dimensions[rn].height = max(S.row_dimensions[r0].height or 17.25, 17.25 * 4)
    # ---------------- 用词规律一览：按全表重算词数、词表，按词数重排 ----------------
    import collections
    import columns as CC
    G = b.wb['用词规律一览']
    texts = [G.cell(rr, 2).value for rr in range(2, G.max_row + 1)]
    data = {G.cell(rr, 2).value: [G.cell(rr, c).value for c in range(1, 7)] for rr in range(2, G.max_row + 1)}
    use = collections.defaultdict(list)
    for rr in range(2, ws.max_row + 1):
        d = CC.parse_I(ws.cell(rr, C.COMBO).value); w = str(ws.cell(rr, C.WORD).value)
        for n, t in d.get('rules', {}).items():
            body = t.split('（')[0].strip()
            k = body if body in data else next((x for x in texts if x.startswith(body) or body.startswith(x)), None)
            if k and w not in use[k]:
                use[k].append(w)
    order = sorted(texts, key=lambda t: -len(use[t]))           # sorted 是稳定的：词数一样的照原来的先后
    for i, t in enumerate(order):
        rr = i + 2
        vals = data[t][:]
        vals[0], vals[4], vals[5] = i + 1, len(use[t]), '、'.join(use[t][:40])
        for c in range(1, 7):
            G.cell(rr, c).value = vals[c - 1]
    b.save(OUT)
    return dropped


if __name__ == '__main__':
    main()

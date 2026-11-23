# -*- coding: utf-8 -*-
"""词根变体、“见 X”、记法三件事（2026-11 同一个词根轮）：
1. “由词根 X 变来”改成“词根 X 的另一种写法（同一个词根）”，后面紧跟“字母变化：X → Y，怎么变的”，每一行自己讲清，不再“见 别的词”；拆分里这一部分写成 Y(=X)；
2. 词根那一行里指到同组别的词的“见 X”去掉（词根的意思、来源就在本行说）；
3. 记法的关联词比本词还复杂的：换成更简单的词，找不到的去掉、在“词根变体处理”列标“记法待补”；变体行的记法统一写词根本身（duc ∽ duck，不写 duct ≈ …）。
输出 ws23_changes.pkl：{(行下标, 列下标): 新文字}"""
import pickle, re, sys, collections
sys.path.insert(0, 'sk_table/etymology-table/scripts')
from part_memo_data import R as MEMO_R
import shift_notes as SN
hdr, data = pickle.load(open('table.pkl', 'rb'))
H, I, J, K, L, P = 7, 8, 9, 10, 11, 15
MEMO_RX = re.compile(r'[；;，,。]?\s*记[：:]\s*([A-Za-z][A-Za-z()\-]*)\s*([≈∽←])\s*([A-Za-z][A-Za-z\'’ \-]*?)\s*[（(]([^（）()]*)[）)]\s*[：:]\s*([^\n]*)$')
LEAD = '词根 %s 的另一种写法（同一个词根）'
TPL = {(anc, zh): (sym, why) for cores, need, sym, anc, zh, why, avoid in MEMO_R}
# 记法：换成更简单的关联词
REPL = {
 'introduce': ('∽', 'duck', '鸭子', '鸭妈妈走在前面，领着一队小鸭子走，{c} 就是领着走；两个词只是长得像，帮你记'),
 'transport': ('≈', 'port', '港口', SN.WHY['port']),
 'factory':   ('≈', 'do', '做', 'do 是做，{c} 也是做；词典说它们出自同一个老词根'),
 'dictionary': ('≈', 'teach', '教', 'teach 是教，老师把道理说给你听、指给你看，{c} 就是说；词典说它们出自同一个老词根'),
 'lean':      ('∽', 'climb', '爬', 'climb 是爬，山坡是斜的才要爬，{c} 就是斜、靠；两个词只是长得像，帮你记'),
}
REMOVE = {'collect', 'message', 'grammar'}                 # 找不到更简单的词：去掉，标“记法待补”
REMOVE_AT = {('double', 'simple'), ('dialogue', 'logic'), ('dialogue', 'prologue')}  # 只在这个词上不合适（关联词不比本词简单）
SAME_OK = {'port'}        # 词根和单独的词写法一样、意思不同（词根 port 搬运 ≈ 单词 port 港口）
LANG = r'(?:拉丁语|晚期拉丁语|俗拉丁语|中世纪拉丁语|希腊语|古英语|中古英语|古法语|法语|日耳曼语|古诺斯语|古北欧语|意大利语|PIE|原始印欧语)'

def core(lab): return re.sub(r'[（(][^（）()]*[）)]', '', lab).strip().strip('-').lower()
grp_of = collections.defaultdict(set)
for r in data: grp_of[r[4]].add(r[2])

# 每一对“词根 → 变形”的字母变化说明（取本组里写全了的那一行）、每个词根的来源
CANON = {}; CANON_G = {}; CANON_W = {}; SRC = {}
for r in data:
    for line in (r[J] or '').split('\n'):
        m = re.match(r'^([^：]+)：由词根 ?([A-Za-z\-]+) 变来。词形：(.*?)。意思：', line)
        if m:
            Y, X = core(m.group(1)), m.group(2)
            CANON_G.setdefault((r[2], X, Y), m.group(3)); CANON.setdefault((X, Y), m.group(3)); CANON_W.setdefault((r[4], X), m.group(3))
        for m in re.finditer(r'(?:本组词根|\b([A-Za-z]+))“[^”]*”（(' + LANG + r'[^（），；]*)', line):
            x = m.group(1)
            if x: SRC.setdefault((r[2], x.lower()), m.group(2).strip())
            else: SRC.setdefault((r[2], '*'), m.group(2).strip())
        m = re.match(r'^([^：]{1,40})：[^（]{0,30}（((?:来自)?' + LANG + r'[^（），；）]*)', line)
        if m: SRC.setdefault((r[2], core(m.group(1))), m.group(2).strip())
for k in list(SRC):                       # 来源里的引号被“；”切断的：只留到词为止
    v = SRC[k]
    if v.count('“') != v.count('”'): SRC[k] = v[:v.rindex('“')].strip()
HAND = {   # 本组里没有现成说明的，手写
 ('aug', 'auct'): 'aug → auct，拉丁语 augere“增加”的“被…了的”形式词干是 auct-：g 碰上 t 写成 c',
 ('batt', 'bat'): 'batt → bat，古法语 batre 只有一个 t',
 ('cad', 'casc'): 'cad → cas → casc，cadere 的“落下了的”形式是 casus：d 碰上 t 变成了 s',
 ('graph', 'gram'): 'graph → gramm → gram，希腊语 graphein“写”加名词词尾 -ma 成了 gramma：ph 碰上后面的 m，同化成 m；英语词尾双写的 m 简化成一个',
 ('graph', 'gramme'): 'graph → gramm → gramme，希腊语 graphein“写”加名词词尾 -ma 成了 gramma：ph 碰上后面的 m，同化成 m',
 ('ly', 'lyze'): 'ly → lyse → lyze，名词 analysis 去掉词尾 -is、加不发音的 e 成了 lyse',
 ('spec', 'pect'): 'spec → spect → pect，拉丁语 specere“看”的“看过了”形式 spectus 多了一个 t',
 ('spond', 'sponse'): 'spond → spons → sponse，拉丁语 spondere 的“被许诺了的”形式是 sponsus：d 碰上后面的 t 变成了 s',
 ('sta', 'stin'): 'sta → stin，拉丁语 destinare“定下、固定”里的 -stinare，是 sta 加上 n 的形式',
 ('pend', 'pense'): 'pend → pens → pense，拉丁语 pendere 的“被…了的”形式是 pensus：pend 后面接词尾 -tus，d 和 t 碰在一起变成了 s，英语加不发音的 e',
 ('ante', 'vance'): 'ante → vant → vance，晚期拉丁语 abante“从前面”里，ab 的 b 和 ante 连在一起，到法语成了 v，所以 vant 里的 v 其实是 ab 的 b 变来的',
}
HAND_WORD = {   # 这几个词的变法和本组样板词不一样，单独写
 'stage': 'sta → st，俗拉丁语 *staticum“站的地方”经古法语 estage 进入英语，sta 的 a 并进了后面的 age',
 'contrast': 'sta → st，拉丁语 stare“站”经意大利语 contrastare、法语 contraste 进入英语，词尾的元音磨掉了，只剩 st',
 'arrest': 'sta → st，拉丁语 restare“站住、留下”经古法语 arester 进入英语，词尾的元音磨掉了，只剩 st',
}
def tidy(how, word):
    how = how.replace('，见音变栏', '')
    how = re.sub(r'。本组的.*$', '', how)
    how = re.sub(r'（同 [^（）]*\b' + re.escape(word) + r'\b[^（）]*）$', '', how)
    return how
def canon(g, X, Y, word, W=None):
    if word in HAND_WORD: return HAND_WORD[word]
    c = HAND.get((X, Y)) or (W and CANON_W.get((W, X)) if W and CANON_W.get((W, X), '').replace(' ', '').startswith((X + '→').replace(' ', '')) and re.search(r'→\s*' + re.escape(Y) + r'\b', CANON_W.get((W, X), '').split('，')[0].split('：')[0] + ' ') else None) or CANON_G.get((g, X, Y)) or CANON.get((X, Y))
    return tidy(c, word) if c else None

typ_of = {r[4]: (r[6] or '')[:1] for r in data}
def strip_see(line, g, X=None, only=None):
    """词根行里指到同组别的词的“见 W”去掉；“X“意思”（见 W）”的括号换成词根的来源（有的话）"""
    same = lambda w: g in grp_of.get(w, ()) and (only is None or typ_of.get(w) in only)
    src = SRC.get((g, (X or '').lower())) or SRC.get((g, '*')) if X else SRC.get((g, '*'))
    def paren(m):
        w = m.group(1)
        if not same(w): return m.group(0)
        before = line[:m.start()]
        if src and (re.search(r'“[^”]*”$', before) or only) and src not in line and not re.search(LANG, line): return '（' + src + '）'
        return ''
    line = re.sub(r'（见 ?([A-Za-z][A-Za-z\-]*)(?: 的【[^】]*】)?）', paren, line)
    def tail(m):
        return m.group(0) if not same(m.group(2)) else m.group(3)
    line = re.sub(r'([，；]\s*)见 ?([A-Za-z][A-Za-z\-]*)(?: 的【[^】]*】)?(?: 和 [A-Za-z][A-Za-z\-]*)?([）；])', tail, line)
    line = re.sub(r'（见 ?([A-Za-z][A-Za-z\-]*)、[A-Za-z][A-Za-z\-]*）', lambda m: '' if same(m.group(1)) else m.group(0), line)
    return line

changes = {}; log = collections.Counter(); todo = []; pend = collections.defaultdict(list); samples = collections.defaultdict(list)
for ri, r in enumerate(data):
    g, word = r[2], r[4]
    add_eq = []                                     # 拆分里要加 (=X) 的部分
    for col in (I, J, L):
        v = r[col]
        if not v or str(v).strip() in ('-', '—'): continue
        new_lines = []
        for line in str(v).split('\n'):
            old = line
            mm = MEMO_RX.search(line)
            memo = mm.groups() if mm else None
            base = line[:mm.start()] if mm else line
            X = None
            if col == J:
                m = re.match(r'^([^：]{1,40})：由词根 ?([A-Za-z\-]+) 变来(.*)$', base, re.S)
                if m:
                    lab, X, tail = m.group(1), m.group(2), m.group(3); Y = core(lab); lead = LEAD % X; done = True
                    if tail.startswith('。词形：'):
                        base = lab + '：' + lead + '。字母变化：' + tail[len('。词形：'):]; log['A 词形→字母变化'] += 1
                        if Y != X.lower(): add_eq.append((Y, X))
                    elif tail.startswith('（'):
                        d = 0
                        for k, ch in enumerate(tail):
                            if ch == '（': d += 1
                            elif ch == '）':
                                d -= 1
                                if d == 0: break
                        par, rest = tail[1:k], tail[k + 1:]
                        mc = re.match(r'^(' + re.escape(X) + r' → [^，；：]+?)(?:[，；：]\s*(.*?))?[，；]?\s*(?:v 的来历)?见 ?([A-Za-z][A-Za-z\-]*)(?: 和 [A-Za-z\-]+)?(?:；(.*))?$', par)
                        if mc:
                            chain, own_how, Wp, extra = mc.group(1), (mc.group(2) or '').strip('，； '), mc.group(3), mc.group(4)
                            if own_how and word not in HAND_WORD and (X, Y) not in HAND: how = chain + '，' + own_how
                            else: how = canon(g, X, Y, word, Wp) or chain
                            if how == chain: todo.append((ri + 2, word, '没有现成的字母变化说明', old[:80]))
                            if extra: how += '；' + extra
                            if rest.startswith('，意思是'): rest = '。意思是' + rest[len('，意思是'):]
                            elif rest.startswith('：'): rest = '；' + rest[1:]
                            elif rest.startswith('，'): rest = '；' + rest[1:]
                            mx = re.match(r'^；([^。]*)。', rest)                 # 括号后面本词自己的补充：已经写进字母变化里的不再重复
                            if mx and (mx.group(1) in how or word in HAND_WORD): rest = rest[len(mx.group(0)) - 1:]
                            base = lab + '：' + lead + '。字母变化：' + how + rest; log['B 补上字母变化'] += 1
                            if Y != X.lower(): add_eq.append((Y, X))
                        elif re.match(r'^' + re.escape(X) + r' → ', par) and '见 ' not in par:      # 括号里自己写了怎么变
                            how = re.sub(r'^(' + re.escape(X) + r' → [^，；：]+?)：', r'\1，', par)
                            if rest.startswith('，意思是'): rest = '。意思是' + rest[len('，意思是'):]
                            base = lab + '：' + lead + '。字母变化：' + how + rest; log['B 补上字母变化'] += 1
                            if Y != X.lower(): add_eq.append((Y, X))
                        elif re.match(r'^(准确说|不是)', par):
                            base = lab + '：' + lead[:-1] + '；' + par + '）' + rest.replace('。词形：', '。字母变化：', 1); log['C 带说明'] += 1
                        else:
                            done = False
                    elif tail.startswith('：'):
                        base = lab + '：' + lead + '。字母变化：' + X + ' → ' + Y + '，' + tail[1:]; log['D 过去分词词干'] += 1
                    else:
                        done = False
                    if not done: todo.append((ri + 2, word, '写法没认出来', old[:90])); X = None
                else:
                    m2 = re.search(r'；([a-z]+)：由词根 ?([A-Za-z\-]+) 变来。词形：', base)      # destination 这种行中间的
                    if m2:
                        base = base.replace('：由词根 %s 变来。词形：' % m2.group(2), '：' + (LEAD % m2.group(2)) + '。字母变化：', 1); log['E 行中间'] += 1; X = m2.group(2)
                if '由词根' in old or '本组词根' in old or X:
                    b2 = strip_see(base, g, X)
                    if b2 != base: log['去掉“见 同组的词”'] += 1; base = b2
                elif '过去分词' not in base and re.match(r'^[^：]{1,40}：', base):
                    b2 = strip_see(base, g, core(base.split('：')[0]), only=('①', '③'))
                    if b2 != base: log['其余词根行去掉“见 同组的词”'] += 1; base = b2
            # 记法
            if memo:
                a, sym, b, zh, why = memo
                key = b.strip()
                if key in REMOVE or (key, word) in REMOVE_AT:
                    pend[ri].append('%s（原来的 %s 不比本词简单，已去掉）' % ((X or core(a) or a), key)); memo = None; log['记法：去掉待补'] += 1
                elif key in REPL:
                    sym, b, zh, tpl = REPL[key]; a2 = X or a
                    memo = (a2, sym, b, zh, tpl.format(c=a2)); log['记法：换成更简单的词'] += 1
                elif X and core(a) != X.lower() and (key, zh) in TPL:
                    memo = (X, sym, b, zh, TPL[(key, zh)][1].format(c=X)); log['记法：变体行改写词根本身'] += 1
                if memo and (memo[2].lower() == word.lower() or (memo[2].lower() == memo[0].lower() and memo[2].lower() not in SAME_OK)):      # 关联词就是本词、就是这一部分：不写
                    print('  关联词就是本词：', word, memo[:3]); memo = None; log['记法：关联词就是本词，去掉'] += 1
            if memo and memo[1] == '≈' and '音变：' not in memo[4]:        # ≈ 两边写法差得多的：补上哪个音、哪个字母对哪个
                nt = SN.note_for(memo[2].strip(), memo[3], core(memo[0]))
                if nt: memo = memo[:4] + (memo[4].rstrip('。') + '。音变：' + nt,); log['记法：补音变'] += 1
            line = base + ('；记：%s %s %s（%s）：%s' % memo if memo else '')
            if line != old and len(samples[col]) < 400: samples[col].append((ri + 2, word, old, line))
            new_lines.append(line)
        nv = '\n'.join(new_lines)
        if nv != v: changes[(ri, col)] = nv
    # 拆分：这一部分写成 Y(=X)
    if add_eq and r[H]:
        sp = r[H]; first = sp.split('；')[0]; rest = sp[len(first):]
        parts = re.split(r'(\s\+\s)', first); hit = False
        for Y, X in add_eq:
            for k, p in enumerate(parts):
                if p.strip().lower() == Y and '(' not in p:
                    parts[k] = p.replace(p.strip(), p.strip() + '(=' + X + ')'); hit = True; break
        if hit: changes[(ri, H)] = ''.join(parts) + rest; log['拆分加 (=词根)'] += 1
    if ri in pend:
        note = '记法待补：' + '；'.join(dict.fromkeys(pend[ri]))
        changes[(ri, P)] = (str(r[P]) + '；' + note) if r[P] else note
pickle.dump(changes, open('ws23_changes.pkl', 'wb')); pickle.dump(samples, open('ws23_samples.pkl', 'wb'))
print('改动的格数', len(changes)); print(dict(log)); print('要手看的', len(todo))
for t in todo: print('  ', t)

# ---------- 手工补几处
idx = {}
for i, r in enumerate(data): idx.setdefault(r[4], []).append(i)
def cur(i, c): return changes.get((i, c), data[i][c])
def patch(word, col, old, new, must=True):
    for i in idx[word]:
        v = cur(i, col) or ''
        if old in v: changes[(i, col)] = v.replace(old, new, 1); return
    if must: raise SystemExit('没对上：%s %s' % (word, old[:30]))
DUCK = '；记：duc ∽ duck（鸭子）：鸭妈妈走在前面，领着一队小鸭子走，duc 就是领着走；两个词只是长得像，帮你记'
PORT = '；记：port ≈ port（港口）：' + SN.WHY['port'].format(c='port')
patch('transport', J, '-port：搬运', '-port：搬运（拉丁语 portare）' + PORT)
patch('introduce', J, '→ 介绍', '→ 介绍' + DUCK)
patch('dictionary', J, '→ 词典', '→ 词典；记：dic ≈ teach（教）：teach 是教，老师把道理说给你听、指给你看，dic 就是说；词典说它们出自同一个老词根。音变：' + SN.SHIFT['teach'])
patch('fact', J, '→ 做成了的事 → 事实', '→ 做成了的事 → 事实；记：fac ≈ do（做）：do 是做，fac 也是做；词典说它们出自同一个老词根。音变：' + SN.SHIFT['do'])
patch('combat', J, '搏斗、战斗；与…斗争', '搏斗、战斗；与…斗争；记：batt ∽ bat（球棒）：bat 是球棒，拿着它打；batt 就是打、击，两个词只是长得像，帮你记')
for _w in ('surprise', 'enterprise'):
    patch(_w, J, '。字母变化：拉丁语 prehendere“抓”先缩短成 prendere', '。字母变化：prehend → prend → pris → prise，拉丁语 prehendere“抓”先缩短成 prendere', must=False)
patch('exquisite', J, '。字母变化：拉丁语“被寻找的”是 quaesitus', '。字母变化：quaer → quaes → quis → quisite，拉丁语“被寻找的”是 quaesitus')
patch('quantity', J, '和 qualitas 成对（见 quality 的【背景】）', '和 qualitas 成对')
patch('occupation', J, '；cap：由词根 cap 变来。词形：cap → cup，', '；cap → cup：')
patch('majesty', J, 'maj-：大（由词根 magn 变来：mag“大”，比较级早期写作 *magios，g 在 i 前弱化掉了）',
      'maj-：词根 magn 的另一种写法（同一个词根；准确说是 magn 去掉 n 的 mag“大”），意思是“大”。字母变化：mag → maj，比较级早期写作 *magios，g 在 i 前弱化掉了（maior），后来又把 i 写成 j')
patch('suspicion', J, '-spic-：看（由词根 spec 变来：拉丁语 specere 进了复合词写成 -spicere，e 弱化成 i）；',
      '-spic-：词根 spec 的另一种写法（同一个词根），意思是“看”。字母变化：spec → spic，拉丁语 specere 进了复合词写成 -spicere，e 弱化成 i；')
patch('suspicion', J, '记：spic ≈ spy（暗中看）：spy 是偷偷地看，spic 也是看', '记：spec ≈ spy（暗中看）：spy 是偷偷地看，spec 也是看')
patch('suspicion', H, 'spic + ion', 'spic(=spec) + ion')
pickle.dump(changes, open('ws23_changes.pkl', 'wb'))
# ---------- 体检
left = collections.Counter(); memos = collections.Counter(); badm = 0
for i, r in enumerate(data):
    for c in (I, J, L):
        for line in str(cur(i, c) or '').split('\n'):
            if '由词根' in line: left['还有“由词根”'] += 1; print('  还有“由词根”：', r[4], line[:70])
            if '记：' in line:
                m = MEMO_RX.search(line)
                if not m: badm += 1; print('  记法写法不对：', r[4], line[-60:])
                else: memos[(m.group(2), m.group(3), m.group(4))] += 1
            if line.count('（') != line.count('）'): left['括号不配对'] += 1; print('  括号不配对：', r[4], line[:60])
print('改动的格数', len(changes), dict(left), '记法写法不对', badm, '；记法共', sum(memos.values()), '行、关联词', len(memos), '个')
print('新的关联词：', {k: v for k, v in memos.items() if k[1] in ('duck', 'port', 'do', 'teach', 'climb')})
print('待补的行数', sum(1 for k in changes if k[1] == P))

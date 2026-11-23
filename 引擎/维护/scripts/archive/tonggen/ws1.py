# -*- coding: utf-8 -*-
"""用词规律轮（2026-11）：
1. “一个词用进某一行…”“同一个词，英国、美国的用法有时不一样”两条说法是空的（没讲出意思是怎么来的），861 行逐条换成真正的规律，找不到的去掉；
2. 其余规律里前提和这个词对不上的（“表示动作的词…”套在不是动作的词上这类）逐条改或去掉。
输出 ws1_changes.pkl：{行下标(0 起): 新的组合列文字}"""
import pickle, re, collections
from codes_all import DOM, REG
import codes_rev2 as R2
hdr, data = pickle.load(open('table.pkl', 'rb'))
items = pickle.load(open('rules_items.pkl', 'rb'))
M = 12
PRE = '\u3000用词规律：'
S = {
 'c': '词的核心意思不变，换了对象、场合，中文要换个说法，英语还是这个词',
 'f': '作用、做法像什么，就借它的名字来叫',
 's': '样子、形状像什么，就借它的名字来叫',
 'n': '一个词的意思越用越窄：从一大类专指其中一种',
 'w': '一个词的意思越用越宽：从一种说到一大类，或者从说一样东西到说更多东西',
 'a': '表示“做这件事的人”的词，也拿来叫做这件事的东西、机器',
 'p': '说动物、东西的词，也拿来比喻人',
 'l': '表示地方、建筑的词，也拿来代指在那儿的人或机构',
 'b': '具体的意思，慢慢用到看不见、摸不着的事上：身体的动作，也拿来说心里的事',
 'o': '东西换了代，干的还是那件事，旧名字就接着用',
 'r': '表示动作的词，也拿来叫这个动作做出来、留下来的东西',
 't': '表示动作的词，也拿来叫做这件事用的东西',
 'h': '表示性质、状态的词，也拿来叫有这种性质的人、东西或机构',
 'm': '表示材料的词，也拿来叫用它做成的东西',
 'j': '表示动作、东西的词，也拿来叫做这件事的人',
 'e': '不好直说的事，常换一个委婉的说法',
 'k': '说冷热、软硬、甜苦这些感觉的词，也拿来说人的性格、态度',
}
EX = {
 'c': ['play 玩 → 踢（球）、演奏（乐器）', 'open 打开 → 开业', 'run 跑 → 经营'],
 'f': ['virus 病毒 → （电脑）病毒', 'memory 记忆力 → 内存'],
 's': ['mouse 老鼠 → 鼠标', 'dish 盘子 → 碟形天线'],
 'n': ['meat 原来指一切食物 → 专指肉'],
 'w': ['grow 草木生长 → 人、动物长大'],
 'a': ['computer 计算员 → 计算机', 'printer 印刷工 → 打印机'],
 'p': ['fox 狐狸 → 狡猾的人', 'swarm 蜂群 → 一大群人'],
 'l': ['school 学校 → 全校师生', 'corridor 走廊 → 权力中心'],
 'b': ['grasp 抓住 → 理解', 'see 看见 → 明白'],
 'o': ['phone 电话 → 手机', 'torch 火把 → 手电筒'],
 'r': ['invention 发明 → 发明物', 'building 建造 → 建筑物'],
 't': ['transport 运 → 运输工具', 'cover 盖 → 盖子'],
 'h': ['beauty 美 → 美人', 'monopoly 垄断 → 垄断企业'],
 'm': ['glass 玻璃 → 玻璃杯', 'silver 银 → 银牌'],
 'j': ['cook 做饭 → 厨师', 'guide 带路 → 导游'],
 'e': ['depart 离开 → 去世', 'sleep 睡 → 长眠'],
 'k': ['warm 暖和的 → 热情的', 'cold 冷的 → 冷淡的'],
}
OLD_OLDNAME = '东西变了，旧名字还接着用'
OWN_DOM = {59: 'prompt 提示 → 提示符', 63: 'right 右边 → 右派、保守派', 69: 'application 应用 → 应用程序', 333: 'cloud 云 → 云端',
           336: 'camera 暗室 → 照相机 → 摄像机', 340: 'center 中心、中间 → 中锋', 413: 'seed 种子 → 种子选手', 425: 'operation 运转、操作 → 运算',
           483: 'axis 轴 → 轴心、同盟', 238: 'developer 让东西显现的人或物 → 显影液、显影剂', 252: 'fixer 把东西固定住的人或物 → 定影剂'}
OWN_REG = {67: 'car 马车 → 火车车厢', 142: 'coach 四轮大马车 → 长途大巴', 191: 'trunk 大箱子 → 汽车后备箱', 200: 'boot 马车上放东西的地方 → 汽车后备厢',
           252: 'hen 母鸡 → 女人'}
OWN_WORD = {('monk', 'o'): 'monk 独自修行的隐士 → 修道院里的修士', ('plain', 'h'): 'plain 平坦的 → 平原', ('mounting', 't'): 'mounting 安装、架设 → 底座、支架',
            ('binding', 't'): 'binding 捆扎、装订 → 装订、封皮', ('fitting', 't'): 'fitting 安装 → 配件、装置'}
DROP_REG = {92, 123, 124}

def split_ex(body):
    depth = 0; cut = None
    for j in range(len(body) - 1, -1, -1):
        ch = body[j]
        if ch == '）': depth += 1
        elif ch == '（':
            depth -= 1
            if depth == 0: cut = j; break
    if cut is None: return body, '', ''
    rule = body[:cut]; inner = body[cut + 1:-1]
    parts = []; d = 0; cur = ''
    for ch in inner:
        if ch == '（': d += 1
        if ch == '）': d -= 1
        if ch == '；' and d == 0: parts.append(cur); cur = ''
        else: cur += ch
    parts.append(cur)
    return rule, parts[0], '；'.join(parts[1:])

def noparen(t):
    t2 = None
    while t2 != t:
        t2 = t; t = re.sub(r'（[^（）]*）', '', t)
    return t.strip()

def own_from_step(word, step):
    s = re.sub(r'^[→①-⑳\s]+', '', step.strip())
    segs = [x.strip() for x in re.split(r'\s*→\s*', s) if x.strip()]
    if not segs: return word
    res = noparen(segs[-1]) or segs[-1]
    if len(segs) == 1: return '%s %s' % (word, res)
    return '%s：%s → %s' % (word, noparen(segs[0]).rstrip('：，；。'), res)

def fam_for(code, word):
    w = word.lower()
    for e in EX[code]:
        if e.split()[0].lower() != w: return e
    return EX[code][-1]

dec = collections.defaultdict(dict)    # row -> {line: (code, own override, item)}
dom = [it for it in items if it['rule'].startswith('一个词用进某一行')]
reg = [it for it in items if it['rule'].startswith('同一个词，英国、美国')]
assert len(dom) == len(DOM) and len(reg) == len(REG)
for n, (it, c) in enumerate(zip(dom, DOM)): dec[it['row']][it['line']] = (c, OWN_DOM.get(n), it)
for n, (it, c) in enumerate(zip(reg, REG)):
    if n in DROP_REG or c in 'qgv': c = 'x'
    dec[it['row']][it['line']] = (c, OWN_REG.get(n), it)
for it in items:
    if it['rule'] == OLD_OLDNAME: dec[it['row']][it['line']] = ('o', None, it)
# 其余规律的复核
by = {(it['row'], it['line']): it for it in items}
for name, codes in (('tool', R2.TOOL), ('result', R2.RESULT)):
    sel = pickle.load(open('sel_%s.pkl' % name, 'rb')); assert len(sel) == len(codes)
    for key, c in zip(sel, codes):
        if c != '=': dec[key[0]][key[1]] = (c, None, by[key])
sel = pickle.load(open('sel_small1.pkl', 'rb'))
for n, c in R2.SMALL1.items():
    key = sel[n]; dec[key[0]][key[1]] = (c, None, by[key])
def pos_set(F): return set(re.findall(r'^(modal v\.|aux\. v\.|n\.|v\.|adj\.|adv\.|pron\.|prep\.|conj\.|num\.|art\.|int\.|phr\.)', F or '', re.M))
for it in items:
    r = data[it['row']]; ps = pos_set(r[5]); w = it['word']; rule = it['rule']; c = None
    if rule.startswith('表示动作的词，也能直接当名词用') and not ('v.' in ps and 'n.' in ps): c = R2.V2N.get(w)
    elif rule.startswith('表示东西、性质的词，也能直接当动词用') and not ('v.' in ps and ('n.' in ps or 'adj.' in ps)): c = R2.N2V.get(w)
    elif rule.startswith('名词放在别的名词前面') and 'n.' not in ps: c = R2.N2ADJ.get(w)
    elif rule.startswith('表示性质、状态的词') and 'adj.' not in ps and not re.search(r'(ness|ity|ty|cy|ce|th|dom|hood|ship|ism|y)$', w): c = R2.HOLDER.get(w)
    if c: dec[it['row']][it['line']] = (c, None, it)

changes = {}; stat = collections.Counter(); newlines = []
for row, dd in dec.items():
    word = data[row][4]; lines = (data[row][M] or '').split('\n'); out = []
    for k, l in enumerate(lines):
        if k in dd:
            code, ov, it = dd[k]
            stat[code] += 1
            if code == 'x': continue
            own = ov or OWN_WORD.get((word, code)) or (it['own'] if it['fam'] else None) or own_from_step(word, it['step'])
            out.append(['R', S[code], own, code, None])
        elif l.startswith(PRE):
            rule, own, fam = split_ex(l[len(PRE):])
            out.append(['E', rule, own if fam else None, None, fam or own])
        else:
            out.append(l)
    seen = set(); res = []; here = set()      # here：这一步下面已经写过的规律（同一步不写两遍）
    for x in out:
        if isinstance(x, str): res.append(x); here = set() if not x.startswith('\u3000') else here; continue
        kind, rule, own, code, fam0 = x
        if rule in here: continue
        here.add(rule)
        first = rule not in seen; seen.add(rule)
        if kind == 'R':
            fam = fam_for(code, word)
            line = PRE + rule + ('（%s；%s）' % (own, fam) if first else '（%s）' % fam)
            newlines.append((code, word, line))
        else:
            if first and own is None:
                j = len(res) - 1
                while j >= 0 and res[j].startswith('\u3000'): j -= 1
                own = own_from_step(word, res[j] if j >= 0 else '')
                line = PRE + rule + '（%s；%s）' % (own, fam0)
            elif not first and own is not None:
                line = PRE + rule + '（%s）' % fam0
            else:
                line = PRE + rule + ('（%s；%s）' % (own, fam0) if own is not None else '（%s）' % fam0)
        res.append(line)
    new = '\n'.join(res)
    if new != data[row][M]: changes[row] = new

# 两个词手写（用户点到的 produce、product）
def hand(word, old, new):
    for i, r in enumerate(data):
        if r[4] == word:
            cur = changes.get(i, r[M]); assert old in cur, word
            changes[i] = cur.replace(old, new); return
    raise SystemExit('没找到 ' + word)
hand('produce',
     PRE + '表示动作的词，也能直接当名词用，指这件事或做一次（produce 生产、制造 → 农产品；walk 走 → 散步）',
     PRE + S['r'] + '（produce 生出、结出 → 农产品；invention 发明 → 发明物）')
hand('produce',
     '→ 把戏搬上舞台、把片子拍出来摆到观众面前 → 上演；制作（电影、节目）\n',
     '→ 把戏搬上舞台、把片子拍出来摆到观众面前 → 上演；制作（电影、节目）\n' + PRE + S['c'] + '（produce 拿到前面来 → 出示（证件）、制作（节目）；play 玩 → 踢（球）、演奏（乐器））\n')
hand('product',
     '→ 工厂造出来拿去卖的东西 → 产品\n→ 一番努力“造出来”的东西 → 结果\n',
     '→ 工厂造出来拿去卖的东西 → 产品\n' + PRE + S['n'] + '（product 一切造出来的东西 → 专指工厂造出来卖的产品；meat 原来指一切食物 → 专指肉）\n'
     '→ 一番努力“造出来”的东西 → 结果\n' + PRE + S['b'] + '（product 造出来的东西 → 一番努力的结果；grasp 抓住 → 理解）\n')
pickle.dump(changes, open('ws1_changes.pkl', 'wb')); pickle.dump(newlines, open('ws1_newlines.pkl', 'wb'))
print('改动的行数', len(changes), '；各类条数', dict(stat))
# 体检：改完以后全表的规律说法、括号配对、“第一次带本词例子，后面只留熟悉例子”
allrules = collections.Counter(); bad = 0
for i, r in enumerate(data):
    m = changes.get(i, r[M]) or ''; seen = set()
    for l in m.split('\n'):
        if l.startswith(PRE):
            rule, own, fam = split_ex(l[len(PRE):]); allrules[rule] += 1
            if l.count('（') != l.count('）'): bad += 1; print('括号不配对', r[4], l[:80])
            if (rule in seen) == bool(fam) and r[4] != 'pants': bad += 1; print('先后不对', r[4], l[:80])
            seen.add(rule)
print('规律说法', len(allrules), '种；问题', bad)
for k, v in allrules.most_common(): print(v, k)

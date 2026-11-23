"""字母变化体检（2026-11 字母变化轮，references/project_rules.md 第 44 条）。
  python3 zimu_check.py <xlsx>           一、挂到源头词根上的外来基础词（② 拆分写 X ← Y、Y 是词根列里的源头词根）音变列要有【字母变化】链；
                                         二、写了链的行，链和步骤的写法要对。两项都应为 0
  python3 zimu_check.py <xlsx> --todo    三、以后可以接着写链的候选（人工看）：② 变体关联里和源头字母差得多、音变列还没有两步以上链的；
                                         拆分里带 (=…)、变化大的。截短、缩写（phone ← telephone、ATM）、as(=ad) 这类前缀同化一般不用写；
                                         ≈ 词逐个看过、不写链的（SKIP_APPROX）不列
第一行带“：”的是以前的写法（【字母变化】开头的一句说明，drought、tight、fierce、endorse、falcon），不当链查。
≈ 的词（rail ≈ rule）写的链从本词自己的源头写到本词，① 讲清和 ≈ 后面那个词的关系；检查和别的链一样（不要求 ① 写出词根）。
链的写法：第一行“【字母变化】形式（语言）→ 形式（语言）→ … → 本词（英语）”，推出来的形式前面加 *，英语原样借来的最后一个写“X（古法语、英语）”；
下面每一步一行：① 讲第一个形式、写出词根 Y-；以后一个箭头一行，第 k 行要写到链上第 k 个形式；最后一个写成“（…、英语）”的可以再多一行讲英语里的读音。
视频技能（wordfilm.js 的 chainOf）用同一套规则读链，两边改写法要一起改。
"""
import os, re, sys
from openpyxl import load_workbook
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cols as C

CIRC = '①②③④⑤⑥⑦⑧⑨⑩'
ITEM = re.compile(r'^\s*(\*?)([A-Za-zæþðÆÞÐ][A-Za-zæþðÆÞÐ\'’\-]*)\s*（([^（）]+)）\s*$')   # 古英语的 æ、þ、ð 也算字母（2026-11 动词变化形式轮）
FOREIGN = re.compile(r'拉丁|法语|希腊|意大利|西班牙|葡萄牙|阿拉伯|荷兰|德语|北欧|凯尔特|爱尔兰|梵语|波斯')
# 字母变化同源词轮（2026-11）逐个看过、不写链的 70 个 ≈ 词（本族词、来源不确定、变化很小，名单见「整表核对记录」第 114 条），--todo 不再列出
SKIP_APPROX = set('''match weigh wagon wet booth there though twist deed yard chill drown glow bench weave month streak shallow dig dyke tusk wasp yarn
blast wail reef widow pitch storey guess dune rubble carol hockey buoy glitch haunt prune pant cabbage pilot core label lush turtle lava mushroom puck fee
guarantee ribbon tier physique costume critique ration graffiti false salsa pouch climax Hindu rink carpet filter salute gas lime border supper'''.split())
CHAIN2 = re.compile(r'[A-Za-zāēīōūæœçéèêëàâîïôûü*\-]{2,}[^→\n]{0,40}→[^→\n]{0,40}[A-Za-zāēīōūæœçéèêëàâîïôûü]{2,}[^→\n]{0,40}→')


def chain_of(line):
    """“【字母变化】a（拉丁语）→ b（古法语）→ …”→ [(形式, 语言, 是不是推出来的)]；写法不对返回 None"""
    out = []
    for it in re.sub(r'^\s*【字母变化】', '', line).split('→'):
        m = ITEM.match(it)
        if not m:
            return None
        out.append((m.group(2), m.group(3).strip(), m.group(1) == '*'))
    return out if len(out) >= 2 else None


def problems(word, P, root=None):
    L = str(P or '').split('\n')
    if not L or not L[0].startswith('【字母变化】'):
        return ['音变列第一行不是【字母变化】链']
    ch = chain_of(L[0])
    if not ch:
        return ['链写法不对（每个形式后面要有“（语言）”，用“ → ”连）']
    out = []
    if ch[-1][0].lower() != str(word).lower():
        out.append('链的最后一个不是本词')
    steps = [l for l in L[1:] if l[:1] in CIRC]
    extra = '、英语' in ch[-1][1]
    if not (len(steps) == len(ch) or (extra and len(steps) == len(ch) + 1)):
        out.append(f'步骤 {len(steps)} 行，链上 {len(ch)} 个形式')
    for k, st in enumerate(steps):
        if st[0] != CIRC[k]:
            out.append('步骤编号不连')
            break
        if 1 <= k < len(ch) and ch[k][0].lower() not in st.lower():
            out.append(f'第 {k + 1} 步没写到 {ch[k][0]}')
    if root and steps and root + '-' not in steps[0]:
        out.append(f'① 没写出词根 {root}-')
    return out


def lev(a, b):
    a, b = a.lower(), b.lower()
    d = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, cb in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (ca != cb))
    return d[-1]


def main():
    path, todo = sys.argv[1], '--todo' in sys.argv
    ws = load_workbook(path, read_only=True)['拆分结果']
    need, bad, has, cand_v, cand_e, legacy = [], [], 0, [], [], []
    for rn, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 2):
        g = lambda c: str(row[c - 1] or '')
        word, typ, sp, K, P = g(C.WORD), g(C.TYPE), g(C.SPLIT), g(C.ROOT), g(C.SOUND)
        heads = {re.sub(r'[\-\s]', '', m.group(1)) for m in re.finditer(r'(?m)^\s*([A-Za-z\-]+)\s*：', K)}
        m = re.match(r'^\s*(\S+)\s*←\s*([A-Za-z]+)\s*$', sp.split('；')[0].split('\n')[0])
        is_need = typ.startswith('②') and m and m.group(2) in heads
        if P.startswith('【字母变化】') and '：' in P.split('\n')[0] and not is_need:
            legacy.append(word)                # 以前用【字母变化】开头写的一句说明（drought、tight……），不是链，不查
            continue
        if P.startswith('【字母变化】') or is_need:
            if P.startswith('【字母变化】'):
                has += 1
            pr = problems(word, P, m.group(2) if is_need else None)
            if is_need:
                need.append(word)
            if pr:
                bad.append((rn, word, pr))
        if not todo or is_need or P.startswith('【字母变化】'):
            continue
        txt = K + '\n' + g(C.WPART) + '\n' + P
        mv = re.match(r'^\s*(\S+)\s*(←|≈)\s*([^；;\n]+)', sp)
        if typ.startswith('②') and mv and FOREIGN.search(txt):
            a = re.sub(r'[^a-z]', '', mv.group(1).lower())
            b = re.sub(r'[^a-z]', '', re.sub(r'\(.*?\)|（.*?）', '', mv.group(3)).split('+')[0].split('/')[0].lower())
            if a and b and lev(a, b) >= 3 and not CHAIN2.search(P) and not (mv.group(2) == '≈' and word in SKIP_APPROX):
                cand_v.append((rn, word, sp.split('\n')[0], mv.group(2)))
        eqs = [(x, y) for x, y in re.findall(r'([A-Za-z]+)\(=([A-Za-z]+)\)', sp) if lev(x, y) >= 2 or (x[0].lower() != y[0].lower() and len(x) > 2)]
        eqs = [(x, y) for x, y in eqs if not (x[:3].lower() == y[:3].lower() and re.search(r'(?:at|it|ut|s|t)$', x))]   # 过去分词轮：competit(=compete) 这类过去分词词干不算
        if eqs and not CHAIN2.search(P):
            cand_e.append((rn, word, sp))
    print('一、挂到源头词根上的外来基础词', len(need), '行，音变列缺【字母变化】链或写法不对', sum(1 for x in bad if x[1] in need))
    print('二、写了【字母变化】链的', has, '行，链或步骤写法不对', len(bad))
    if legacy:
        print('   （另有', len(legacy), '行以前用【字母变化】开头写的一句说明，不是链，不查：' + '、'.join(legacy) + '）')
    for rn, w, pr in bad[:40]:
        print('   ', rn, w, '；'.join(pr))
    if todo:
        arr = [x for x in cand_v if x[3] == '←']
        print(f'三、以后可以写链的候选：② 变体关联 {len(cand_v)} 个（写成 ← 的 {len(arr)} 个，多是截短、缩写；写成 ≈ 的 {len(cand_v) - len(arr)} 个；逐个看过、不写链的 ≈ 词 {len(SKIP_APPROX)} 个不列），拆分带 (=…) 变化大的 {len(cand_e)} 个')
        print('   ②：', '、'.join(f'{w}（{s}）' for _, w, s, _ in cand_v[:40]))
        print('   (=…)：', '、'.join(f'{w}（{s}）' for _, w, s in cand_e[:40]))


if __name__ == '__main__':
    main()

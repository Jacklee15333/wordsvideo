# -*- coding: utf-8 -*-
"""词缀的来历、记法（2026-11 词缀来历、记法轮，project_rules.md 第 73–75 条；目录在 laili_data.py）。
  plan(data, C)            全表试算 -> ({(行下标, 'pre' / 'suf'): 新格}, 统计, 没换的清单)
  line_new(line, e)        一行：换来历 / 补来历 / 加记法 -> (新行, 做了什么)
  problems(data, C)        体检：认得出的旧写法还没换的、该有记法没写的、记法写法不对的、来历里“经”字前面混了别的语言的
  python3 laili.py <表.xlsx> [--show 键 20]   试算，打印每个词缀换了多少、补了多少、没换的旧写法（最常见的在前）
  python3 laili.py <表.xlsx> --check          体检（写好的表各项应为 0）
再跑一遍不变：已经是新来历的行不再换，已经有“记：”的行不再加。"""
import re, sys, collections
import linetools as LT
import cols as CO
import cizhui as CZ
import cizhui_catalog as ZC
import laili_data as LD

SRCW = re.compile(r'来自|英语本来就有|英语本族|古英语|古诺尔斯语|拉丁语|希腊语|法语|本族')
SHEN = re.compile(r'；身份：')
HAS_MEMO = re.compile(r'记：\s*[A-Za-z][A-Za-z()\-]*\s*[≈∽←]')
SRCX = re.compile(r'来自|英语本来就有|英语本族|本族的|古英语|古诺尔斯语|拉丁|希腊语|法语')       # 正文里提到来源的字样（有就不补）
MEMO_RX = re.compile(r'[；;，,。]?\s*记[：:]\s*([A-Za-z][A-Za-z()\-]*)\s*([≈∽←])\s*([A-Za-z][A-Za-z\'’ \-]*?)\s*[（(]([^（）()]*)[）)]\s*[：:]\s*([^\n]*)$')
LANGS = re.compile(r'拉丁语|希腊语|古诺尔斯语|法语|意大利语|西班牙语|葡萄牙语|荷兰语|德语|阿拉伯语|印地语')


def parens(s):
    """顶层括号 [(起, 止)]（止是“）”的位置）"""
    out, d, st = [], 0, -1
    for i, ch in enumerate(s):
        if ch == '（':
            if d == 0: st = i
            d += 1
        elif ch == '）' and d > 0:
            d -= 1
            if d == 0: out.append((st, i))
    return out


def tok(s, seps):
    """按顶层（括号、引号外面）的分隔符切开，保留分隔符：[[文字, 分隔符], …]"""
    out, d, q, cur = [], 0, 0, ''
    for ch in s:
        if ch in '（(': d += 1
        elif ch in '）)': d = max(0, d - 1)
        elif ch == '“': q += 1
        elif ch == '”': q = max(0, q - 1)
        if d == 0 and q == 0 and ch in seps:
            out.append([cur, ch]); cur = ''
        else:
            cur += ch
    out.append([cur, ''])
    return out


def untok(ts):
    return ''.join(a + b for a, b in ts)


def split_line(line):
    """一行词缀解释 -> (标签部分“-ly：身份：”, 正文（开头的介绍）, 后面的“；记：…”“。辨析：…”)"""
    return LT.affix_split(line)          # 2026-11 词缀身份辨析轮：头“标签：身份：”，正文是开头的介绍，尾是“；记：…”“。辨析：…”


def drop_clauses(text, rx):
    """括号里的一段按“，”“：”切开，去掉整句对上 rx 的（连同前面的分隔符）"""
    if not rx or not text: return text
    ts = tok(text, '，：')
    keep = []
    for i, (a, sep) in enumerate(ts):
        if re.fullmatch(rx, a.strip()):
            if keep and not sep: keep[-1][1] = ''          # 去掉的是最后一句：前一句后面的分隔符也不要了
            continue
        keep.append([a, sep])
    out = untok(keep)
    return out.rstrip('，：')


def find_src(main):
    """正文里第一个带来源字样的括号：(括号起, 止, 段列表, 第几段)；没有返回 None"""
    for a, b in parens(main):
        segs = tok(main[a + 1:b], '；')
        for k, (sg, _) in enumerate(segs):
            if SRCW.search(sg): return a, b, segs, k
    return None


def entry_for(col, lab, kind, sense, probe):
    for e in LD.ENTRIES:
        if e['col'] != col or lab not in e['labels']: continue
        if col == 'suf' and e['kind'] != '*' and e['kind'] != kind: continue
        if e['sense'] and e['sense'] != sense: continue
        if e['need'] and not re.search(e['need'], probe): continue
        if e['avoid'] and re.search(e['avoid'], probe): continue
        return e
    return None


def line_new(line, e):
    """-> (新行, 动作集合)；动作：换 / 补 / 记 / 已是新 / 没认出"""
    head, main, meta = split_line(line)
    acts = set()
    src = find_src(main)
    if src:
        a, b, segs, k = src
        sg = segs[k][0]
        if sg.startswith(e['new']):
            acts.add('已是新')
        else:
            m = re.match(e['head'], sg)
            if m:
                tail = drop_clauses(sg[m.end():], e['drop'])
                if tail and tail[0] not in '，：；（': tail = '，' + tail
                segs[k][0] = e['new'] + tail
                acts.add('换')
            else:
                acts.add('没认出')
        if e['drop']:                                    # 括号里整段都是已经讲过的（“和 like 是一家，见 like”“同一个前缀两个意思…”）
            segs = [s for i, s in enumerate(segs) if i == k or not re.fullmatch('(?:%s)(?:，(?:%s))*' % (e['drop'], e['drop']), s[0].strip())]
            if segs: segs[-1][1] = ''
        main = main[:a + 1] + untok(segs) + main[b:]
    elif e['fill'] and not SRCX.search(main) and not re.search(r'^这里|不是|对应|缩写|= ?古|就是 |本来|其实|看上去|误', tok(main, '；')[0][0]):
        # 只给一点来源都没写的行补（正文里哪儿也没提哪种语言）；第一句讲的不是这个词缀的本义（“这里不是…”“= 古法语 a”“其实是假的”）也不补
        ts = tok(main, '；')
        first = ts[0][0]
        ps = parens(first)
        new = e['new'] + e['fillx']
        if ps and ps[-1][1] == len(first.rstrip()) - 1:          # 第一句末尾是括号（同 例词 / 在 b、p 前写成 em-）：来历插在括号最前面
            a, b = ps[-1]
            inner = first[a + 1:b]
            if e['drop']:
                inner = '；'.join(s for s, _ in tok(inner, '；') if not re.fullmatch('(?:%s)' % e['drop'], s.strip()))
            first = first[:a + 1] + new + ('；' + inner if inner else '') + first[b:]
        else:
            first = first.rstrip() + '（' + new + '）'
        ts[0][0] = first
        main = untok(ts)
        acts.add('补')
    if e['top']:
        ts = tok(main, '；')
        keep = [t for i, t in enumerate(ts) if i == 0 or not re.search(e['top'], t[0].strip())]
        if len(keep) != len(ts):
            keep[-1][1] = ''
            main = untok(keep); acts.add('去重复')
    out = head + main + meta
    if e['memo'] and not HAS_MEMO.search(out):          # “可以这样记：…”这类老说明不算记法
        out = LT.add_memo(out, LD.memo_text(e['memo']))          # 有“。辨析：…”的插在它前面（身份 → 记 → 辨析）
        acts.add('记')
    return out, acts


def rows_of(data, C):
    """每一行词缀：(行下标, 列, 第几行, 标签, 后缀变成什么, 前缀的意思, 这一行)"""
    for ri, r in enumerate(data):
        tl = CZ.tail_of(r[C['combo']])
        for col in ('pre', 'suf'):
            v = str(r[C[col]] or '')
            if v.strip() in ('', '-'): continue
            for li, line in enumerate(v.split('\n')):
                lab, rest = LT.label_body(line)
                if not lab or lab.startswith('为什么'): continue
                if col == 'suf' and not lab.startswith('-'): continue
                if col == 'pre' and not lab.endswith('-'): continue
                rest = LT.label_body(LT.affix_plain(line))[1]          # 开头的介绍（不带“身份：”这个记号和后面的记法、辨析）
                kind = sense = None
                if col == 'suf':
                    src, tgt = tl.get(lab, (None, None))
                    kind = CZ.kind_of(tgt) if tgt else None
                else:
                    ent = ZC.PRE.get(lab)
                    if isinstance(ent, list):
                        hd = re.split(r'（', rest, 1)[0][:40]
                        grp = next((g for rx, x, g in ent if re.search(rx, hd)), None)
                        sense = grp if grp in ('neg', 'into') else None
                yield ri, col, li, lab, kind, sense, line


def probe_of(line):
    head, main, meta = split_line(line)
    return main


def plan(data, C):
    new_cells, stat, miss = {}, collections.Counter(), collections.defaultdict(collections.Counter)
    cur = {}
    for ri, col, li, lab, kind, sense, line in rows_of(data, C):
        e = entry_for(col, lab, kind, sense, probe_of(line))
        if not e: continue
        nl, acts = line_new(line, e)
        key = (e['col'], ' '.join(sorted(e['labels'])), e['kind'])
        for a in acts: stat[(key, a)] += 1
        stat[(key, '行')] += 1
        if '没认出' in acts:
            src = find_src(split_line(line)[1])
            miss[key][src[2][src[3]][0][:70] if src else '∅'] += 1
        if nl != line:
            k2 = (ri, col)
            if k2 not in cur: cur[k2] = str(data[ri][C[col]]).split('\n')
            cur[k2][li] = nl
    for k2, ls in cur.items(): new_cells[k2] = '\n'.join(ls)
    return new_cells, stat, miss


def problems(data, C):
    """写好的表：认得出的旧写法没换（old_left）、该加的记法没加（memo_missing）、记法写法不对（memo_bad）、新来历“经”前面混了别的语言（src_lang）"""
    out = collections.defaultdict(list)
    for ri, col, li, lab, kind, sense, line in rows_of(data, C):
        e = entry_for(col, lab, kind, sense, probe_of(line))
        if not e: continue
        nl, acts = line_new(line, e)
        w = data[ri][C['word']]
        if '换' in acts or '补' in acts or '去重复' in acts: out['old_left'].append((w, lab))
        if '记' in acts: out['memo_missing'].append((w, lab))
        if HAS_MEMO.search(line) and not MEMO_RX.search(line): out['memo_bad'].append((w, lab))
        before = e['new'].split('经')[0]
        ls = set(LANGS.findall(before))
        if len(ls) > 2: out['src_lang'].append((w, lab))
    return out


if __name__ == '__main__':
    hdr, C, data = LT.load_table(sys.argv[1])
    if '--check' in sys.argv:
        pr = problems(data, C)
        for k in ('old_left', 'memo_missing', 'memo_bad', 'src_lang'):
            print('%s %d %s' % (k, len(pr[k]), pr[k][:6]))
        sys.exit(0)
    cells, stat, miss = plan(data, C)
    keys = sorted({k for k, a in stat}, key=lambda k: -stat[(k, '行')])
    print('要改的格 %d' % len(cells))
    for k in keys:
        print('%-28s 行 %4d  换 %4d  补 %3d  已是新 %4d  没认出 %3d  记 %4d  去重复 %d' % (
            '%s %s %s' % (k[0], k[1][:18], k[2]), stat[(k, '行')], stat[(k, '换')], stat[(k, '补')], stat[(k, '已是新')], stat[(k, '没认出')], stat[(k, '记')], stat[(k, '去重复')]))
    if '--show' in sys.argv:
        n = int(sys.argv[sys.argv.index('--show') + 2]) if len(sys.argv) > sys.argv.index('--show') + 2 else 20
        want = sys.argv[sys.argv.index('--show') + 1]
        for k in keys:
            if want in k[1] or want == 'all':
                for s, c in miss[k].most_common(n): print('   没认出 %s×%d  %s' % (k[1][:12], c, s))

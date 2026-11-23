# -*- coding: utf-8 -*-
"""前缀、后缀的身份和辨析（2026-11 词缀身份辨析轮，project_rules.md 第 83–88 条；上一版叫“身份和分工”，第 67 条）。
前缀列、后缀列里讲一个词缀的那一行写成：
    标签：身份：开头的介绍（意思、作用、来历括号）[；记：记法][。辨析：辨析的话]
  - 身份：就是原来开头的介绍（用户：“开头的介绍和身份其实讲的是一个意思”，并成一个）；每一行词缀都标，没有辨析的（re-、de-、-s）也标。
  - 记：帮着记住这个词缀的，紧跟在身份后面。
  - 辨析（原来的“分工”）：意思、功能相近的几个词缀放在一起讲，每个都讲清接什么词、说什么意思、和旁边那个差在哪儿（不能只说来自哪里）。
    整句照 cizhui_catalog.py 的 GROUP 一字不改（视频照念），放在这一行最后，前面是句号，里面没有句号。
  - 关系（2026-11 词缀关系轮，第 89–92 条）：辨析的最后可以有一段“；关系：…”——这一组里来自同一种语言、写法不同的词缀彼此是什么关系
    （-ant / -ent 是同一个现在分词词尾跟着动词原形走的两种写法；pre- / pro- 不是谁变出谁，是一对兄弟）。有才写；目录的 REL，整句在 GROUP 里。
  - 这个词为什么用它，还是下面单独一行“为什么用 -ous 不用 -ful：…”。
挑哪一组：后缀按“写法 + 变成什么词性”查（词性从组合列第一行末尾的“词性变化（-ous）：名词 → 形容词”读），前缀按写法查（in- 这类两种意思的看开头说的是“不”还是“向里”）；
这一行明说自己不是那个词缀的（“不是 actor 里表“人”的 -or”“看上去是 ad-，其实是假的”）不挂辨析；逐个看过的例外在 cizhui_catalog.py 的 NO_BX / FORCE。
  plan(data, C) -> ({行下标: {'pre': 新前缀格, 'suf': 新后缀格}}, 统计, 没加的原因)   给没标“身份：”的行标上、查得到辨析的行挂上、
                                                 辨析后面的“关系”和目录不一样的照目录重写、NO_BX 里的去掉辨析、挑到另一组的换组（目录的 REL / NO_BX / FORCE 改了以后跑一遍就行）；写好的表再跑一遍不变
  problems(data, C) -> 体检五项（都应为 0）：affix_no_id、affix_old、bianxi_bad、bianxi_diff、guanxi_bad
  python3 cizhui.py <表.xlsx>             打印试算的统计（不写表）
  python3 cizhui.py <表.xlsx> --check     体检五项 + 还能加、还要重写的行
  python3 cizhui.py <表.xlsx> --write <新表.xlsx>   把试算的结果写回（xlsx_write.write，写完读回来逐格比）
  python3 cizhui.py <表.xlsx> --groups    每一组辨析挂在哪些词缀上、各多少行"""
import re, sys, collections
import linetools as LT
from linetools import label_body, top_split
import cizhui_catalog as Z
import columns as CO

def tail_of(combo):
    first = str(combo or '').split('\n')[0]
    mt = CO.TAILPOS.search(first)
    tail = CO.parse_tail(mt.group(1)) if mt else []
    out = {}
    for lab, ch in tail:
        labs = [x.strip().split('（')[0] for x in lab.split('、')]
        nodes = [x.strip() for x in ch.split('→')]
        if len(labs) == 1: out[labs[0]] = (nodes[0] if len(nodes) > 1 else '', nodes[-1])
        elif len(nodes) == len(labs) + 1:
            for i, l in enumerate(labs): out[l] = (nodes[i], nodes[i + 1])
    return out

def kind_of(tgt):
    t = re.sub(r'（.*$', '', tgt)
    ks = [k for k in ('形容词', '名词', '动词', '副词') if k in t]
    return ks[0] if len(ks) == 1 else None

DIM = {'-et', '-ette', '-let', '-ling', '-ie', '-cle', '-ule', '-le', '-el'}
PERSON = {'-er', '-or', '-ist', '-ian', '-an', '-ee', '-eer', '-ess', '-ier'}
NOT_ME = re.compile(r'^(?:这里)?(?:其实)?不是|^看上去|^看着像')          # 这一行开头就说自己不是那个词缀

def pick_suffix(label, src, tgt, line):
    """line：“标签：开头的介绍”（不带“身份：”这个记号和后面的记法、辨析）-> (来头, 辨析组) 或 None"""
    body = line.split('：', 1)[1] if '：' in line else line
    if NOT_ME.search(body): return None
    if label == '-er' and '更' in re.split(r'（', body, 1)[0][:30]: return Z.SUF[('-er', '形容词')]      # fewer、smarter：比较级的 -er（组合列的词性变化写成别的也认）
    if label in ('-y', '-ie') and re.search(r'昵称|亲昵|小称', re.split(r'（', body, 1)[0][:40]): return Z.SUF[('-ie', '名词')]      # doggy、bunny、auntie：表示“小、亲昵”的 -y / -ie（词性变化没写、写成别的也认）
    if label in ('-ward', '-wards') and '副词' in tgt: return Z.SUF[(label, '副词')]                      # forward：既是形容词又是副词
    k = kind_of(tgt)
    if k is None: return None
    e = Z.SUF.get((label, k))
    if e is None: return None
    idt, grp = e
    head = re.split(r'（', body, 1)[0][:40]
    if k == '形容词' and re.search(r'名词词尾|名词后缀|这里是名词', head): return None        # 这一行自己说是名词词尾：组合列的词性变化和它对不上，不加
    if k == '名词' and re.search(r'形容词词尾|形容词后缀|这里是形容词', head): return None
    if (label, k) == ('-ed', '形容词') and src == '名词':
        return ('英语本族的后缀（古英语 -ede），接在名词后面，说“有…的、带…的”；和动词过去分词的 -ed 写法一样', 'adj_n')
    if label in DIM and '小' not in top_split(body, '；')[0][:60]: return None      # “小”要写在第一句里（tentacle 的 -cle 第一句是“用来…的东西”，“小”是后面带的一句：不算小称）
    if label in PERSON and k == '名词' and not ('人' in tgt or '人' in body[:50]): return None
    if (label, k) == ('-er', '形容词') and '比较' not in body and '更' not in body: return None
    if (label, k) == ('-est', '形容词') and '最' not in body: return None
    if (label, k) == ('-er', '名词') and src != '动词' and '人' not in body[:40]: return None
    if (label, k) in (('-en', '形容词'), ('-ed', '形容词'), ('-ing', '形容词')) and src not in ('动词', '名词', ''): return None
    if (label, k) == ('-en', '形容词') and re.search(r'材料|做的', body[:40]): return None             # wooden、golden：接在材料名词后面的 -en（“…做的”），不是过去分词
    if (label, k) == ('-ly', '形容词') and src != '名词': return None
    if (label, k) == ('-ly', '副词') and src not in ('形容词', ''): return None
    if (label, k) == ('-y', '形容词') and src not in ('名词', '动词', ''): return None
    if (label, k) == ('-al', '名词') and src != '动词': return None
    if (label, k) == ('-al', '形容词') and src not in ('名词', '形容词', ''): return None
    if (label, k) == ('-ate', '动词') and ('形容词' in body[:12] or '名词词尾' in body[:12]): return None
    if (label, k) == ('-en', '动词') and src not in ('形容词', '名词'): return None
    if (label, k) == ('-ish', '形容词') and src == '': return None
    return idt, grp

def pick_prefix(label, line):
    e = Z.PRE.get(label)
    if e is None: return None
    body = line.split('：', 1)[1] if '：' in line else line
    m = re.match(r'^(?:这里)?不是“[^”]*”[，；]?\s*(?:而是)?', body)          # “这里不是“不”，而是拉丁语 in“在…上、在…里””：看“而是”后面说的是什么
    if m and isinstance(e, list): body = body[m.end():]
    elif NOT_ME.search(body): return None
    if isinstance(e, list):
        head = re.split(r'（', body, 1)[0][:40]
        for rx, idt, grp in e:
            if re.search(rx, head): return idt, grp
        return None
    return e

def pick(col, word, label, src, tgt, plain):
    """这一行该挂哪一组辨析：先看逐个定下的例外（FORCE、NO_BX），再按规则挑。-> 组名 或 None"""
    key = (str(word), label)
    if key in Z.FORCE: return Z.FORCE[key]
    if key in Z.NO_BX: return None
    if col == 'suf':
        e = pick_suffix(label, src, tgt or '', plain)          # 组合列没写这个后缀的词性变化（tgt 空着）：只认开头的介绍说得明白的几种（更… / 亲昵）
    else:
        e = pick_prefix(label, plain)
    return e[1] if e else None

def add(line, grp):
    """给一行词缀挂上辨析（没标“身份：”的顺手标上）：标签：身份：介绍[；记：…]。辨析：…"""
    P = LT.affix_parts(line.rstrip())
    return LT.affix_join(P['label'], P['id'], P['memo'], Z.GROUP[grp])

def mark(line):
    """只标“身份：”（目录里没有辨析的词缀：re-、de-、-s）"""
    P = LT.affix_parts(line.rstrip())
    return LT.affix_join(P['label'], P['id'], P['memo'], P['bx'])

def affix_lines(data, C):
    """每一行词缀：(行下标, 列, 第几行, 标签, 这一行, (母词词性, 变成什么词性))"""
    for ri, r in enumerate(data):
        tl = None
        for col in ('suf', 'pre'):
            v = str(r[C[col]] or '')
            if v.strip() in ('', '-'): continue
            for li, line in enumerate(v.split('\n')):
                lab = label_body(line)[0]
                if not lab or not LT.is_affix_label(lab, col): continue
                if tl is None: tl = tail_of(r[C['combo']])
                yield ri, col, li, lab, line, (tl.get(lab, (None, None)) if col == 'suf' else (None, None))

def want(data, C, ri, col, lab, line, st):
    return pick(col, data[ri][C['word']], lab, st[0], st[1], LT.affix_plain(line))

def plan(data, C):
    out = {}; stat = collections.Counter(); miss = collections.Counter(); cur = {}
    for ri, col, li, lab, line, st in affix_lines(data, C):
        P = LT.affix_parts(line)
        if not P['new'] and re.search(r'；身份：|。分工：', line): miss['old_format'] += 1; continue      # 上一版的老写法：不自动改（身份里独有的话要人并进开头的介绍）
        if P['bx']:
            # 2026-11 词缀关系轮：辨析本身是目录里的句子（CORE）的行，照目录现在的样子重写——目录加了、改了“关系”的整句换掉；
            # 逐个定下不挂的（NO_BX）去掉辨析；规则 / FORCE 现在挑的是另一组的换组。辨析不是目录里的句子的不自动改（体检 bianxi_diff 报）
            g0 = CORE2GRP.get(LT.bx_split(P['bx'])[0])
            if g0 is None: continue
            gw = want(data, C, ri, col, lab, line, st)
            if gw == g0 and P['bx'] == Z.GROUP[g0]: continue
            if gw is None: new = LT.affix_join(P['label'], P['id'], P['memo'], ''); stat[col + ':去掉辨析 ' + g0] += 1
            elif gw != g0: new = LT.affix_join(P['label'], P['id'], P['memo'], Z.GROUP[gw]); stat[col + ':换组 %s→%s' % (g0, gw)] += 1
            else: new = LT.affix_join(P['label'], P['id'], P['memo'], Z.GROUP[g0]); stat[col + ':关系 ' + g0] += 1
            k2 = (ri, col)
            if k2 not in cur: cur[k2] = str(data[ri][C[col]]).split('\n')
            cur[k2][li] = new
            continue
        grp = want(data, C, ri, col, lab, line, st)
        if grp is None:
            if P['new']: miss[col + ('_no_tail' if col == 'suf' and st[1] is None else '_no_entry')] += 1; continue
            new = mark(line); stat[col + ':只标身份'] += 1
        else:
            new = add(line, grp); stat[col + ':' + grp] += 1
        if new == line: continue
        k2 = (ri, col)
        if k2 not in cur: cur[k2] = str(data[ri][C[col]]).split('\n')
        cur[k2][li] = new
    for (ri, col), ls in cur.items(): out.setdefault(ri, {})[col] = '\n'.join(ls)
    return out, stat, miss

TEXT2GRP = {t: g for g, t in Z.GROUP.items()}
CORE2GRP = {t: g for g, t in Z.CORE.items()}          # 不带“关系”的辨析 -> 组
# 2026-11 辨析精简演示轮：上一版（音变原因版）的句子也认得，--write 照目录换成精简的新句子
CORE2GRP.update({t: g for g, t in getattr(Z, 'PREV_CORE', {}).items() if t not in CORE2GRP})

DEMO_RX = re.compile(r'（([A-Za-z][A-Za-z\'’\- 、]*)）')
def demo_words(core):
    """一组辨析里每个用法括号的第一个例词（视频的演示词）"""
    return [m.group(1).split('、')[0].strip() for m in DEMO_RX.finditer(core)]

def demo_problems(data, C):
    """demo_bad：演示词不在总表里，或者它那一行组合列第一行不是“A（…）+ B（…）=“…””（视频画不出“图 + 图 = 画”）。
    短语（more beautiful）和逐个看过、本来就没有等式的（hard）记在 Z.DEMO_SKIP"""
    idx = {str(r[C['word']] or '').strip().lower(): r for r in data}
    out = []
    for g, core in Z.CORE.items():
        for w in demo_words(core):
            if w in getattr(Z, 'DEMO_SKIP', ()): continue
            r = idx.get(w.lower())
            c1 = str(r[C['combo']] or '').split('\n')[0] if r is not None else ''
            if r is None or '+' not in c1 or '=“' not in c1: out.append((g, w, '不在表里' if r is None else c1[:40]))
    return out

def problems(data, C):
    """词缀行体检（各项都应为 0）：
    affix_no_id   讲词缀的那一行开头没有“身份：”
    affix_old     还留着上一版的老写法“；身份：…。分工：…”
    bianxi_bad    辨析写法不对：不是这一行的最后一段、前面不是句号、里面有句号、写在“；记：”前面、一行写了两段、“记：”前面不是分号
    bianxi_diff   辨析的话不是目录里的句子（手改过表，或者目录改了没重写——目录加了、改了“关系”也算），或者和目录给这一行挑的那一组不一样（挂错了组、不该挂的挂了）
    guanxi_bad    “关系”写法不对：不是辨析的最后一段（前面要是分号）、一行写了两段、是空的、哪一条不是词缀打头（视频靠条首的词缀认这一条讲的是谁）"""
    out = collections.defaultdict(list)
    for ri, col, li, lab, line, st in affix_lines(data, C):
        n, w = ri + 2, str(data[ri][C['word']])
        P = LT.affix_parts(line)
        if re.search(r'[；。]身份：[^。\n]*。分工：', line): out['affix_old'].append((n, w, lab))
        if not P['new']: out['affix_no_id'].append((n, w, lab)); continue
        body = label_body(line)[1]
        nb = body.count('辨析：'); k = body.find(LT.MEMO_MARK); b = body.find(LT.BX_MARK)
        if nb > 1 or (nb == 1 and b < 0) or (b >= 0 and '。' in body[b + len(LT.BX_MARK):]) or (0 <= b < k) or body.count('身份：') != 1 \
                or re.search(r'(?<![；这样])记：\s*[A-Za-z][A-Za-z()\-]*\s*[≈∽←]', body):
            out['bianxi_bad'].append((n, w, lab)); continue
        if P['bx']:
            g = TEXT2GRP.get(P['bx'])
            if g is None or g != want(data, C, ri, col, lab, line, st): out['bianxi_diff'].append((n, w, '%s %s' % (lab, g or '不在目录里')))
            core, rel = LT.bx_split(P['bx'])
            if '关系：' in P['bx'] and (P['bx'].count('关系：') > 1 or LT.REL_MARK not in P['bx'] or not rel.strip()
                                      or any(not LT.rel_heads(x) for x in LT.rel_items(rel))):
                out['guanxi_bad'].append((n, w, lab))
    return out

def groups(data, C):
    use = collections.defaultdict(collections.Counter)
    for ri, col, li, lab, line, st in affix_lines(data, C):
        g = TEXT2GRP.get(LT.affix_parts(line)['bx'])
        if g: use[g][lab] += 1
    return use


if __name__ == '__main__':
    from linetools import load_table
    hdr, C, data = load_table(sys.argv[1])
    if '--groups' in sys.argv:
        for g, c in sorted(groups(data, C).items(), key=lambda x: -sum(x[1].values())):
            print('%-9s %4d 行  %s' % (g, sum(c.values()), '、'.join('%s %d' % kv for kv in c.most_common())))
            print('          ' + Z.GROUP[g])
        sys.exit(0)
    out, stat, miss = plan(data, C)
    if '--check' in sys.argv:
        pr = problems(data, C); total = len(out)
        pr['demo_bad'] = demo_problems(data, C)
        for k in ('affix_no_id', 'affix_old', 'bianxi_bad', 'bianxi_diff', 'guanxi_bad', 'demo_bad'):
            print('%-12s %d %s' % (k, len(pr[k]), pr[k][:6])); total += len(pr[k])
        print('%-12s %d' % ('affix_todo', len(out)))
        print('合计 %d' % total)
        sys.exit(0)
    print('还能标身份、挂辨析的行 %d（%d 行词缀）' % (len(out), sum(stat.values())))
    for k, v in sorted(stat.items(), key=lambda x: -x[1]): print('  %s %d' % (k, v))
    print('  没加的：', dict(miss))
    if '--write' in sys.argv and out:
        import xlsx_write as XW
        dst = sys.argv[sys.argv.index('--write') + 1]
        ch = {(ri + 2, C[col]): v for ri, d in out.items() for col, v in d.items()}
        XW.write(sys.argv[1], dst, ch)
        h2, C2, d2 = load_table(dst)
        bad = sum(1 for ri, r in enumerate(data) for ci in range(len(hdr))
                  if str(d2[ri][ci] if d2[ri][ci] is not None else '') != str(ch.get((ri + 2, ci), r[ci] if r[ci] is not None else '')))
        print('写回 %d 格；读回来和“原表 + 改动”逐格比：%d 处不一致' % (len(ch), bad))

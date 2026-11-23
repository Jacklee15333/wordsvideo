# -*- coding: utf-8 -*-
"""拉丁语动词的三个样子（原形、过去式、过去分词）和变化规律，写进词根那一行（2026-11 拉丁语动词变化轮，project_rules.md 第 71 条）。
词根行的先后：`标签：词根 X 的另一种写法（同一个词根）。字母变化：…。动词变化：…；规律：…。身份：…。分工：…。意思：…；记：…`
            （不是变体的：`标签：本组词根“意思”（来源）。动词变化：…；规律：…。身份：…。分工：…；记：…`）
这一段是整个词根族的（同族每一行写同一句，和“分工”一样），数据在 dongbian_data.py 的 VERB，只给写了“身份、分工”的行加。
用法：
  seg(key)             这一族的那一段：“动词变化：原形 …→ 过去式 …→ 过去分词 …；规律：…”（不带句号）
  get(line)            一行里的 dict(forms=[(原形 / 过去式 / 过去分词, 拉丁语, 中文)…], rule=规律) ；没有返回 None
  strip(line)          去掉这一段（别的体检脚本看这一行本身写了什么之前先去掉：shenfen.cut、guoqu_check、tonggen_check）
  put(line, key)       写上（已经有的先去掉再写，所以再跑不变）
  fam_of(line, 组号)   这一行属于 shenfen_data.FAM 的哪一族
  plan(data, C)        全表试算：{行下标: 新的词根格}, 统计
  problems(data, C)    体检：该有没有的、和数据对不上的、位置不对的、不该有却有的（shenfen_check.py 调它）
  python3 dongbian.py <表.xlsx>                     试算（写好以后应是“要改的格 0”）
  python3 dongbian.py <表.xlsx> --list              列出各族的三个样子、规律、行数
  python3 dongbian.py <原表.xlsx> --write <新表.xlsx>  写回（只动词根列；xlsx_write.write），再把新表读回来和“原表 + 改动”逐格比"""
import re, sys, collections
import linetools as LT
import shenfen_data as FD
import dongbian_data as DD

SEG = re.compile(r'动词变化：([^。\n]*?)；规律：([^。\n]*)。')
FORM = re.compile(r'^(原形|过去式|过去分词)\s+([A-Za-z]+)“([^”]+)”$')
SF_AT = re.compile(r'身份：[^。\n]*。分工：')
VARL = re.compile(r'^([^：]{1,40})：词根\s*([A-Za-z]+)\s*的另一种写法')
core = lambda lab: re.sub(r'[（(][^（）()]*[）)]', '', lab or '').strip().strip('-')


def seg(key):
    v = DD.VERB[key]
    forms = ['原形 %s“%s”' % v['inf']] + (['过去式 %s“%s”' % v['perf']] if v.get('perf') else []) + ['过去分词 %s“%s”' % v['pp']]
    rule = (v['cut'] + '；' + v['rule']) if v.get('cut') else v['rule']        # 2026-11 第 73 条：第一句讲原形去掉词尾就是词根
    return '动词变化：' + '→ '.join(forms) + '；规律：' + rule


def strip(line):
    return SEG.sub('', str(line or ''))


def get(line):
    m = SEG.search(str(line or ''))
    if not m: return None
    forms = []
    for x in m.group(1).split('→'):
        f = FORM.match(x.strip())
        if not f: return dict(forms=None, rule=m.group(2).strip(), raw=m.group(0))
        forms.append((f.group(1), f.group(2), f.group(3)))
    return dict(forms=forms, rule=m.group(2).strip(), raw=m.group(0))


def fam_of(line, g):
    m = VARL.match(line)
    if m and (g, m.group(2)) in FD.FAM: return (g, m.group(2))
    lab = LT.label_body(line)[0]
    if lab and not m:
        c = core(lab).lower()
        return next(((gg, X) for (gg, X) in FD.FAM if gg == g and X.lower() == c), None)
    return None


def put(line, key):
    base = strip(line)
    m = SF_AT.search(base)
    assert m and base[m.start() - 1] == '。', '这一行没有“。身份：…。分工：”：' + line[:60]
    return base[:m.start()] + seg(key) + '。' + base[m.start():]


def plan(data, C):
    out, stat = {}, collections.Counter()
    for ri, r in enumerate(data):
        v = str(r[C['root']] or '')
        if '分工：' not in v and '动词变化：' not in v: continue
        g = r[C['grp']]
        new = []
        for line in v.split('\n'):
            key = fam_of(line, g) if '分工：' in line else None
            if key in DD.VERB:
                nl = put(line, key)
                if nl != line: stat['%s %s' % key] += 1
                new.append(nl)
            else:
                new.append(line)
        nv = '\n'.join(new)
        if nv != v: out[ri] = nv
    return out, stat


def problems(data, C):
    """-> {类别: [(Excel 行号, 单词, 说明)]}
    verb_missing  这一族在 dongbian_data.VERB 里，这一行（写了身份、分工的）却没有“动词变化：…；规律：…”
    verb_diff     写了，和 VERB 里的不一样（数据改了没重写，或者手改过表）
    verb_bad      写法不对：三个样子不是“原形 / 过去式 / 过去分词 拉丁语“中文””、不是紧挨在“身份：”前面、规律里有“意思是 / 意思：”
    verb_stray    这一行不属于 VERB 里的词根族（或没写身份、分工），却写了“动词变化”"""
    out = collections.defaultdict(list)
    for n, r in enumerate(data, start=2):
        v = str(r[C['root']] or ''); w = str(r[C['word']]); g = r[C['grp']]
        for col, name in (('pre', '前缀列'), ('wp', '单词部分列'), ('suf', '后缀列')):      # “动词变化：双写 t（vetted）”这种别的话不算，只认带“；规律：”的这一段
            if get(str(r[C[col]] or '')): out['verb_stray'].append((n, w, '写在了' + name))
        if '分工：' not in v and '动词变化：' not in v: continue
        for line in v.split('\n'):
            key = fam_of(line, g) if '分工：' in line else None
            got = get(line)
            if key in DD.VERB:
                if not got: out['verb_missing'].append((n, w, line[:40])); continue
                if got['raw'] != seg(key) + '。': out['verb_diff'].append((n, w, got['raw'][:50]))
                k = line.find(got['raw'])
                if not got['forms'] or not line[k + len(got['raw']):].startswith('身份：') or re.search(r'意思(是|[：:])', got['rule']) or len(SEG.findall(line)) != 1:
                    out['verb_bad'].append((n, w, got['raw'][:50]))
            elif got:
                out['verb_stray'].append((n, w, line[:40]))
    return out


def show(C, data):
    rows = collections.Counter()
    for r in data:
        for line in str(r[C['root']] or '').split('\n'):
            if '分工：' in line:
                k = fam_of(line, r[C['grp']])
                if k: rows[k] += 1
    tot = 0
    for key, v in DD.VERB.items():
        tot += rows[key]
        print('%-18s %2d 行  %s' % ('%d %s' % key, rows[key], seg(key)))
    print('共 %d 族、%d 行；没有单独过去式的 %d 族' % (len(DD.VERB), tot, sum(1 for v in DD.VERB.values() if not v.get('perf'))))
    lost = [k for k in DD.VERB if k not in FD.FAM]
    if lost: print('!! VERB 里这几族不在 shenfen_data.FAM 里：', lost)


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    hdr, C, data = LT.load_table(a[0])
    if '--list' in sys.argv:
        show(C, data); sys.exit(0)
    out, stat = plan(data, C)
    print('要改的格 %d（%d 族）' % (len(out), len(stat)))
    if '--write' in sys.argv:
        import xlsx_write as XW
        dst = a[1]
        XW.write(a[0], dst, {(ri + 2, C['root']): t for ri, t in out.items()})
        h2, C2, d2 = LT.load_table(dst)
        bad = 0
        for ri, (x, y) in enumerate(zip(data, d2)):
            for j in range(len(hdr)):
                want = out[ri] if (j == C['root'] and ri in out) else x[j]
                if (want if want not in ('',) else None) != (y[j] if y[j] not in ('',) else None): bad += 1
        print('读回来和“原表 + 改动”逐格比：%d 行 × %d 列，不一致 %d 格' % (len(d2), len(h2), bad + abs(len(data) - len(d2))))

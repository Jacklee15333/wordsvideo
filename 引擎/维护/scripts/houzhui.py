# -*- coding: utf-8 -*-
"""后缀那一行开头的介绍照前缀的样子写（2026-11 词根形态补齐轮，project_rules.md 第 117 条）。
用户：“检查一下后缀现在是不是也按照前缀的样式来进行写的”。前缀行开头是“意思”（来历）：
    pro-：身份：“向前”（来自拉丁语介词 pro“在前面、向前”，本来是单独的一个词）；也表示“预先”；这里是“向前、到前面来”
后缀行原来多半先写作用、意思夹在中间（视频的身份框就成了“来自…；把动作变成名词：…”，和前缀的“来自…；表示“…””对不上）：
    -ful：身份：加在名词后面，变成形容词：“充满…的、有…的”（英语本来就有的后缀…；同 helpful 有帮助的、useful 有用的）
改成意思打头、来历括号紧跟在后面、作用放到后面一段：
    -ful：身份：“充满…的、有…的”（英语本来就有的后缀…；同 helpful 有帮助的、useful 有用的）；加在名词后面，变成形容词
只动“身份：”后面第一段（到括号外第一个“；”），记、辨析、关系和后面的话一字不动。不动的：开头是“= -ize”这种别名的（视频靠它认）、
开头是“这里…”或第一段里有“不是”的、第一段里没有引号里的意思的、引号里的意思不止一处的（-ing 名词、形容词两用）、来历括号不在第一段末尾的。
前缀列有 256 行也是先写作用的，一起照这个样子改（--pre）。
  plan(data, C, col='suf') -> ({行下标: 新格}, 统计)
  python3 houzhui.py <表> [--show 20] [--pre]     试算（写好的表应是“要改的格 0”；--pre 看前缀列）
  python3 houzhui.py <原表> --write <新表>          写回（只动后缀列）"""
import re, sys, collections
import linetools as LT

MEAN = re.compile(r'“[^”]*”(?:\s*(?:或|、|和)\s*“[^”]*”)*')
TAIL = re.compile(r'(?:表示|意思是|意思|本义|原义|是|即|叫|说)$')
LAILI = re.compile(r'来自|本来|本族|古英语|拉丁语|希腊语|法语|意大利语|日耳曼语|印欧语')
# 改了以后 cizhui.py 挂的辨析会变（它看这一行开头的几十个字）的行，照原样不改：plan 里自动退回，名单记在这里备查
KEEP = {('peasant', 'suf'), ('bunny', 'suf'), ('calendar', 'suf'), ('discovery', 'suf')}


def _paren_tail(s):
    """s 末尾那个括号外面的“（…）”从哪儿开始；末尾不是括号返回 -1"""
    if not s.endswith('）'): return -1
    d = 0
    for i in range(len(s) - 1, -1, -1):
        if s[i] == '）': d += 1
        elif s[i] == '（':
            d -= 1
            if d == 0: return i
    return -1


def fix_intro(intro):
    segs = LT.top_split(intro, '；')
    first = segs[0].rstrip()
    k = _paren_tail(first)
    if k <= 0: return intro, '来历括号不在第一段末尾'
    H, P = first[:k].rstrip(), first[k:]
    if H.startswith(('=', '这里')) or '不是' in H: return intro, '别名或“这里…”'
    if not LAILI.search(P): return intro, '括号里不是来历'
    m = MEAN.search(H)
    if not m: return intro, '没有引号里的意思'
    if MEAN.search(H, m.end()) or MEAN.search(H[:m.start()]): return intro, '有两个意思（-ing 名词、形容词两用这类）'
    before, after = H[:m.start()].strip(' ，：、'), H[m.end():].strip(' ，：、')
    if not before and not after: return intro, '已经是“意思”（来历）'
    before = TAIL.sub('', before).strip(' ，：、')
    F = '，'.join(x for x in (before, after) if x)
    return '；'.join([m.group(0) + P + ('；' + F if F else '')] + segs[1:]), '改'


def fix_line(line, col='suf'):
    lab, body = LT.label_body(line)
    if not lab or not LT.is_affix_label(lab, col) or not body.startswith('身份：'): return line, None
    head = line[:len(line) - len(body)]
    rest = body[3:]
    cut = min([j for j in (rest.find('；记：'), rest.find('。辨析：')) if j >= 0] or [len(rest)])
    new, why = fix_intro(rest[:cut])
    return (head + '身份：' + new + rest[cut:]) if why == '改' else line, why


def plan(data, C, col='suf'):
    out, stat, ex = {}, collections.Counter(), []
    for ri, r in enumerate(data):
        v = str(r[C[col]] or '')
        if v.strip() in ('', '-'): continue
        new = []
        for l in v.split('\n'):
            nl, why = fix_line(l, col)
            if (str(r[C['word']]), col) in KEEP: nl, why = l, '照原样（cizhui 挂的辨析会变）'
            if why: stat[why] += 1
            if nl != l and len(ex) < 400: ex.append((str(r[C['word']]), l, nl))
            new.append(nl)
        nv = '\n'.join(new)
        if nv != v: out[ri] = nv
    return out, stat, ex


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    hdr, C, data = LT.load_table(a[0])
    col = 'pre' if '--pre' in sys.argv else 'suf'
    out, stat, ex = plan(data, C, col)
    print('要改的格 %d；%s' % (len(out), '、'.join('%s %d 行' % kv for kv in stat.most_common())))
    if '--show' in sys.argv:
        for w, l, nl in ex[:int(sys.argv[sys.argv.index('--show') + 1])]: print('  %s\n    改前 %s\n    改后 %s' % (w, l[:120], nl[:120]))
    if '--write' in sys.argv:
        import xlsx_write as XW
        XW.write(a[0], a[1], {(ri + 2, C[col]): t for ri, t in out.items()})
        print('写好了', a[1])

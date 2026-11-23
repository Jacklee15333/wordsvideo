"""e 结尾的词加 -er / -ed / -en / -est：拆分写全后缀（make + er），两个 e 只写一个。
拆分、后缀列（标签、说明）、组合列（公式、词性变化）一起改；shown、known、first 这类本来就只加 n、st 的不动。"""
import re
FULL = {'r': 'er', 'd': 'ed', 'n': 'en', 'st': 'est', '(e)d': 'ed'}
SHORT = {'er': 'r', 'ed': 'd', 'en': 'n', 'est': 'st'}


def parts_of(I):
    return [p.strip() for alt in I.split('；') for p in alt.split(' + ')]


def split_fix(I, M):
    out = []
    for alt in I.split('；'):
        parts = alt.split(' + ')
        for i in range(1, len(parts)):
            a = re.sub(r'\([^()]*\)$', '', parts[i - 1].strip().split('← ')[-1])
            p = parts[i].strip()
            if p in FULL and a.endswith('e') and re.search(r'(^|\n)-(%s|%s)：' % (re.escape(p.replace('(e)', '')), FULL[p]), M):
                parts[i] = parts[i].replace(p, FULL[p])
        out.append(' + '.join(parts))
    return '；'.join(out)


def note_fix(s, word):
    def note(m):
        base, suf = m.group(1), FULL[m.group(2)]
        return '%s 已经以 e 结尾，和 -%s 的 e 只写一个：%s + %s → %s' % (base, suf, base, suf, word.split('-')[-1])
    s = re.sub(r'([A-Za-z\-]+) (?:已经|已)?以 e 结尾，(?:只|直接)加 -?(r|d|n|st)(?![A-Za-z])', note, s)
    s = re.sub(r'词尾已(?:经)?有 e，(?:只|直接)加 -?(r|d|n|st)(?![A-Za-z])', lambda m: '词尾已经有 e，和 -%s 的 e 只写一个' % FULL[m.group(1)], s)
    return s


def process(d):
    I, M, N, w = d['I'], d['M'], d['N'], d['w']
    I2 = split_fix(I, M)
    full = {SHORT[p] for p in parts_of(I2) if p in SHORT}          # 拆分里写全了的后缀
    full -= {SHORT[p] for p in parts_of(I2) if p in SHORT and False}
    shorts = {p for p in parts_of(I2) if p in ('r', 'd', 'n', 'st')}  # 还真的只加 n、st 的（shown、first）
    conv = full - shorts
    M2L = []
    for l in M.split('\n'):
        m = re.match(r'-(d|n|r|st)：', l)
        if m and m.group(1) in conv:
            f = FULL[m.group(1)]
            l = '-' + f + '：' + l[m.end():]
            l = re.sub(r'^-(%s)：= -%s[，“]?' % (f, f), lambda mm: '-' + f + '：' + ('“' if mm.group(0).endswith('“') else ''), l)
            l = l.replace('（就是 -%s：' % f, '（')
        M2L.append(l)
    M2 = note_fix('\n'.join(M2L), w)
    if I2 != I:
        M2 = re.sub(r'加上 -(d|n|r|st)(?![A-Za-z])', lambda m: '加上 -' + FULL[m.group(1)], M2)
        M2 = re.sub(r'的 -(d|n|st)(?=[）；，。])', lambda m: '的 -' + FULL[m.group(1)], M2)
    L = N.split('\n')
    if I2 != I:
        L[0] = re.sub(r'\+ (r|d|n|st)（', lambda m: '+ ' + FULL[m.group(1)] + '（', L[0])
    out = []
    for l in L:
        l = re.sub(r'(?<=[（、])-(d|n|r|st)(?=[、）])', lambda m: '-' + FULL[m.group(1)] if m.group(1) in conv else m.group(0), l)
        l = re.sub(r'\+ -(d|n|r|st)(?=（| )', lambda m: '+ -' + FULL[m.group(1)] if m.group(1) in conv else m.group(0), l)
        if I2 != I:
            l = re.sub(r'加上 -(d|n|r|st)(?![A-Za-z])', lambda m: '加上 -' + FULL[m.group(1)], l)
        out.append(note_fix(l, w))
    N2 = '\n'.join(out)
    return I2, M2, N2

"""动词变化形式轮（2026-11）：不规则动词的过去式、过去分词，组合列（N）讲清形式的作用，音变 / 字母变化列（P）讲清一步步怎么变来的。
E(...) 登记一行：组合列写【构词逻辑】那一段（第一行 + 步骤），【语法】由 gram() 按形式自动写，原来的【演变】【辨析】【例】等照原文留着；
音变列写新的链和步骤（或【元音交替】【变化】段），原来带标签的段落（【同形异义】【合成】……）照原文留在后面。"""
import re

BASE = {}      # 原形 → (过去式, 过去分词, 意思, 及物)
ROWS = []      # 登记的行


def B(base, past, pp, bm, tr=True):
    BASE[base] = (past, pp, bm, tr)


def E(row, word, base, kind, logic, P, drop=(), gram_old='keep', gram_extra='', gram=None, p_drop=()):
    """kind：p 过去式、pp 过去分词、b 过去式和过去分词同形、m 情态动词等（【语法】手写，gram 给全文）
    drop：组合列原来要去掉的段（标签名，如 '辨析'）；gram_old：原来的【语法】段 keep 接在新的后面 / drop 不要"""
    ROWS.append(dict(r=row, w=word, base=base, kind=kind, logic=logic.strip('\n'), P=P.strip('\n'),
                     drop=set(drop), gram_old=gram_old, gram_extra=gram_extra, gram=gram, p_drop=tuple(p_drop)))


def _bm(bm, k):
    return bm if isinstance(bm, str) else bm[k]


def gram_text(e):
    if e['gram'] is not None:
        return '【语法】' + e['gram']
    w, base, kind = e['w'], e['base'], e['kind']
    past, pp, bm, tr = BASE[base]
    done, pas = _bm(bm, 0), _bm(bm, 1)
    forms = '%s – %s – %s' % (base, past, pp)
    if kind == 'p':
        s = '%s：%s 是过去式，只说动作在过去已经发生，自己就能作谓语，前面不加 have、be；' % (forms, w)
        s += ('“已经%s了”“被%s”要用过去分词 %s（have %s、be %s）' % (done, pas, pp, pp, pp)) if tr else ('“已经%s了”要用过去分词 %s（have %s）' % (done, pp, pp))
    elif kind == 'pp':
        if tr:
            s = ('%s：%s 是过去分词，不单独作谓语：跟在 have 后面说完成，have %s“已经%s了”；跟在 be 后面说被动，be %s“被%s”。'
                 '完成、被动都带着“…了的”的意思，所以过去分词常直接当形容词用，意思是“被…了的”' % (forms, w, w, done, w, pas))
        else:
            s = ('%s：%s 是过去分词，不单独作谓语：跟在 have 后面说完成，have %s“已经%s了”。%s 后面不带宾语，没有被动；'
                 '过去分词当形容词用，意思是“已经…了的”' % (forms, w, w, done, base))
    elif kind == 'b':
        s = '%s：%s 既是过去式，也是过去分词。当过去式，自己作谓语，说动作在过去已经发生；当过去分词，跟在 have 后面说完成（have %s“已经%s了”）' % (forms, w, w, done)
        s += ('，跟在 be 后面说被动（be %s“被%s”）' % (w, pas)) if tr else ''
        s += '。看前面有没有 have、be，就分得出是哪一种'
    else:
        raise ValueError(kind)
    return '【语法】' + s + '。' + e['gram_extra']


SEG = re.compile(r'^\s*[\u2460-\u2473]?\s*【([^【】\n]{1,10})】')


def blocks_of(N):
    """组合列 → [(段名, [行])]（第一段【构词逻辑】那一段名为 None）"""
    out = [[None, []]]
    for k, l in enumerate(str(N or '').split('\n')):
        m = SEG.match(l) if k else None
        if m and m.group(1) != '构词逻辑':
            out.append([m.group(1), [l]])
        else:
            out[-1][1].append(l)
    return out


def compose_N(e, oldN):
    bl = blocks_of(oldN)
    lines = e['logic'].split('\n')
    if lines[0] == '【构词逻辑】*':                      # 第一行照原文（拆分写成 take + n 这类，第一行的等式和词性变化不动）
        lines[0] = bl[0][1][0]
    assert lines[0].startswith('【构词逻辑】'), e['w']
    g = gram_text(e)
    old_g = [b for b in bl[1:] if b[0] == '语法']
    if old_g and e['gram_old'] == 'keep':
        t = '\n'.join(old_g[0][1])
        t = re.sub(r'^\s*【语法】\s*', '', t)
        g = g.rstrip('。') + '。' + t.rstrip('。') + '。'
    out = lines + [g]
    for name, ls in bl[1:]:
        if name == '语法' or name in e['drop']:
            continue
        out += ls
    return '\n'.join(out)


LAB = re.compile(r'【[^【】]{1,10}】')


def labeled_segments(P):
    """音变列原文里带标签的段落（【同形异义】……），按原样取出；不带标签的话（原来那句讲变化的）不要"""
    segs = []
    for line in str(P or '').split('\n'):
        pos = [m.start() for m in LAB.finditer(line)]
        for i, p in enumerate(pos):
            s = line[p:pos[i + 1]] if i + 1 < len(pos) else line[p:]
            segs.append(s.rstrip('。 ').strip())
    return segs


def dropped_text(P):
    """原文里不带标签、要被新写法替换掉的话（核对用）"""
    out = []
    for line in str(P or '').split('\n'):
        m = LAB.search(line)
        head = line[:m.start()] if m else line
        if head.strip(' 。'):
            out.append(head.strip())
    return out


def compose_P(e, oldP):
    segs = [s for s in labeled_segments(oldP) if not any(s.startswith('【' + k + '】') for k in e['p_drop'])]
    return e['P'] + ('\n' + '\n'.join(segs) if segs else '')

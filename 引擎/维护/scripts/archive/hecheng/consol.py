"""把散在组合列（N）【语法】【辨析】【提醒】、步骤括号、指路行和音变列（P）里讲连写、连字符、分开写的话收拢到“写法”那一行。
返回：新 N 的其余行、新 P、收拢来的句子（给写法那一行的括号用）、改动说明。"""
import re
from mixfix import MIXFIX, ALL

WKW = re.compile(r'连字符|连写|分开写|分写|拆开写|拆开说|合写|写成两个词|写成一个词|合成一个词|连成一个词|不加连字符|直接合写|直接连写|两词连写|两个词连写|两词直接|两个词直接')
VAR = re.compile(r'也(常|可|可以)?(连写|分写|分开写)?(写|作|写作|写成|拼作)\s*[A-Za-z]')
TAG = re.compile(r'^\s*【(语法|辨析|提醒|变体)】')
POINTER = re.compile(r'^\s*（[^（）]*(见【(辨析|语法|提醒)】)[^（）]*）\s*$')
STEP = re.compile(r'^\s*[→⇒\u2460-\u2473]')


def top_split(s, seps='；。'):
    out, buf, d = [], '', 0
    for ch in s:
        if ch in '（(':
            d += 1
        elif ch in '）)':
            d = max(0, d - 1)
        if ch in seps and d == 0:
            if buf.strip():
                out.append(buf.strip())
            buf = ''
        else:
            buf += ch
    if buf.strip():
        out.append(buf.strip())
    return out


CUR = ['']
MIXED = []


def norm(x):
    return re.sub(r'[\s\-]', '', x.lower())


def var_ok(sent):
    """“也写作 X、Y”：X 和本词只差空格、连字符，才算写法上的变体"""
    m = VAR.search(sent)
    if not m:
        return False
    toks = re.findall(r"[A-Za-z][A-Za-z' \-]*[A-Za-z]", sent[m.start():])
    toks = [t.strip() for t in toks if t.strip()]
    return bool(toks) and all(norm(t) == norm(CUR[0]) for t in toks[:1])


def writing_only(sent):
    """这句话是不是只在讲写法（连写、连字符、分开写、也写作 X）"""
    s = re.sub(r'（[^（）]*）|\([^()]*\)', '', sent)
    if not WKW.search(sent) and VAR.search(sent):
        return var_ok(sent) and not re.search(r'意思|指|反义', s)
    return bool(WKW.search(sent)) and not re.search(
        r'意思|指|反义|更口语|可数|只指人|语气|常用于|否定|疑问|肯定|作“|本义|字面|来源|来自|词典|也说|也叫|同义|近义|不说 [a-z]|进入英语|经[^，。]{0,8}(语|进入)|说法|=', s)


def strip_step(l):
    """步骤行末尾、中间只讲写法的括号去掉；“用连字符连起来，”这类话去掉"""
    out = l
    for m in list(re.finditer(r'（((?:[^（）]|（[^（）]*）)*)）', l)):
        inner = m.group(1)
        if WKW.search(inner) and not re.search(r'\d{3,4}|世纪|只放在|只作', inner):
            out = out.replace(m.group(0), '')
    out = re.sub(r'(两个词|几个词)?用连字符连(起来|成一个词)[，、]\s*', '', out)
    out = re.sub(r'连成一个词放在名词前', '放在名词前', out)
    out = re.sub(r'\s+$', '', out)
    return out


def consolidate(N, P, word=''):
    CUR[0] = word
    L = str(N or '').split('\n')
    first, rest = L[0], L[1:]
    keep, took, notes = [], [], []
    for l in rest:
        if POINTER.match(l) and WKW.search(l):
            notes.append('删指路行：' + l.strip())
            continue
        if STEP.match(l):
            n = strip_step(l)
            if n != l:
                notes.append('步骤去写法括号：' + l.strip())
                took += [x for x in re.findall(r'（((?:[^（）]|（[^（）]*）)*)）', l) if WKW.search(x)]
            keep.append(n)
            continue
        m = TAG.match(l)
        if m:
            body = l[m.end():]
            sents = top_split(body, '；。')
            w_s = [s for s in sents if writing_only(s)]
            o_s = [s for s in sents if not writing_only(s)]
            if not w_s:
                keep.append(l)
                continue
            if o_s:
                fx = MIXFIX.get((CUR[0], 'N'))
                if fx is None:
                    keep.append(l)
                    MIXED.append((CUR[0], 'N', l))
                elif fx[0] == 'KEEP':
                    keep.append(l)
                elif fx[0] == 'DROPTAIL':
                    keep.append(l.replace('。' + fx[1], '').replace(fx[1], ''))
                    took.append(fx[1])
                    notes.append('%s 去掉写法的话：%s' % (m.group(1), fx[1]))
                elif fx[0] is None:
                    took.append(body if fx[1] == ALL else fx[1])
                    notes.append('删【%s】：%s' % (m.group(1), body))
                else:
                    keep.append(fx[0])
                    if fx[1]:
                        took.append(fx[1])
                    notes.append('改【%s】：%s → %s' % (m.group(1), body, fx[0]))
            else:
                took += w_s
                notes.append('删【%s】：%s' % (m.group(1), body))
            continue
        keep.append(l)
    newP_lines, Ptook = [], []
    for l in str(P or '').split('\n') if P else []:
        if not l.strip():
            continue
        m = TAG.match(l)
        head = '【%s】' % m.group(1) if m else ''
        body = l[m.end():] if m else l
        # P 列一行里常常跟着别的【标签】段落：只看第一个【…】之前的那一段
        cut = re.search(r'【[^【】]{1,8}】', body)
        tail = body[cut.start():] if cut else ''
        body0 = body[:cut.start()] if cut else body
        sents = top_split(body0, '；。')
        w_s = [s for s in sents if writing_only(s)]
        o_s = [s for s in sents if not writing_only(s)]
        if not w_s:
            newP_lines.append(l)
            continue
        if o_s or tail:
            fx = MIXFIX.get((CUR[0], 'P'))
            if fx is None:
                newP_lines.append(l)
                MIXED.append((CUR[0], 'P', l))
            elif fx[0] == 'KEEP':
                newP_lines.append(l)
            elif fx[0] is None:
                Ptook.append(body if fx[1] == ALL else fx[1])
                notes.append('音变列删：' + l.strip())
            else:
                newP_lines.append(fx[0])
                if fx[1]:
                    Ptook.append(fx[1])
                notes.append('音变列改：%s → %s' % (l.strip(), fx[0]))
        else:
            Ptook += w_s
            notes.append('音变列删：' + l.strip())
    newP = '\n'.join(newP_lines) if newP_lines else None
    return first, keep, newP, took + Ptook, notes

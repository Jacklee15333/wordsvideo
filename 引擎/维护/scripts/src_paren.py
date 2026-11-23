"""后缀来源统一进括号（口径：-ion：作用（来源；同 例词）；其他说明）。
只改 video_check.py 的 suf_src_text_only 那几行（来源写在正文里、没进括号）：
  A 正文里写了“它本身来自古英语 lic…”“，来自希腊语 -ikos”→ 这一句挪进括号；
  B “英语本族的后缀 / 词尾”→ 去掉，括号里写“英语本来就有的后缀，古英语写作 …”；
  C 开头就是“拉丁语比较级词尾 -ior，……”→ 改成“比较级词尾，……（来自拉丁语 -ior）”；
  D 正文只提到“英语本族词”，后缀本身没写来源 → 括号里补这个后缀的标准来源（STD）。
括号里已有“（同 …）”就并成“（来源；同 …）”。
用法：python3 src_paren.py <in.xlsx> <out.xlsx> [--note 来源进括号]；也可 import fix_line(标签, 这一行) 用。"""
import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LANG = r'(?:古|中古|晚期|中世纪|俗|现代|古北部)?(?:拉丁|希腊|古法|英法|法|古英|意大利|西班牙|葡萄牙|荷兰|德|古诺尔斯|阿拉伯|印地|波斯|普罗旺斯)语?'
OWN = re.compile(r'^(?:这里|它本身|它|本身|这个后缀|这个词尾)?\s*(?:其实|也|就|都|最早|最终|往上)?\s*(?:是)?(?:(?:来自|源自|出自|借自|取自)\s*|经\S{1,6}?来自\s*|(?:是|就是)\s*(?=' + LANG + r'(?:原有的|里的|的)?\s*-))' + LANG)
CONT = re.compile(r'^(?:和 \S+ ?(?:是一家|同源|是同一个|是亲戚|同出一源)|经|再经|即|也就是|古英语|写作|原来是|本来是|在古法语里|见 |← |本义)')
NATIVE = re.compile(r'^(?:这是|是|一个)?英语本族(?:的)?(?:形容词|名词|动词|副词)?(?:后缀|词尾)(?:，|$)')
OE = {'-ness': '古英语写作 -nes', '-hood': '古英语写作 -had', '-ward': '古英语写作 -weard', '-wards': '古英语写作 -weardes', '-ish': '古英语写作 -isc',
      '-y': '古英语写作 -ig', '-dom': '古英语写作 -dom', '-ship': '古英语写作 -scipe', '-th': '古英语写作 -þu / -þ', '-ling': '古英语写作 -ling',
      '-some': '古英语写作 -sum', '-er': '古英语写作 -ere', '-less': '古英语写作 -leas', '-en': '', '-n': '', '-le': '', '-ful': '就是 full“满的”变来的，见 full'}
STD = {
    '-er': '英语本来就有的后缀，古英语写作 -ere', '-ers': '英语本来就有的后缀，古英语写作 -ere',
    '-able': '来自拉丁语 -abilis，经法语进入英语；和单词 able 不是一个来源，只是长得像、意思也近', '-ible': '来自拉丁语 -ibilis，经法语进入英语',
    '-ly': '来自古英语 lic“身体、样子”，和 like 是一家，见 like', '-ness': '英语本来就有的后缀，古英语写作 -nes',
    '-less': '来自古英语 leas“没有…的”，和 loose“松开的”是一家，见 loose', '-ful': '英语本来就有的后缀，就是 full“满的”变来的，见 full',
    '-ative': '来自拉丁语 -ativus，经法语进入英语', '-ive': '来自拉丁语 -ivus，经法语进入英语', '-ic': '来自拉丁语 -icus、希腊语 -ikos，经法语 -ique 进入英语',
    '-ical': '来自拉丁语 -icus、希腊语 -ikos，再加拉丁语 -alis', '-al': '来自拉丁语形容词词尾 -alis', '-ate': '来自拉丁语“被…了的”形式的词尾 -atus，英语借拉丁动词时常拿它当动词用',
    '-ment': '来自拉丁语名词词尾 -mentum，经法语进入英语', '-age': '来自拉丁语 -aticum，经古法语 -age 进入英语', '-ant': '来自拉丁语 -ans / -antis，经法语进入英语',
    '-ent': '来自拉丁语 -ens / -entis', '-ous': '来自拉丁语 -osus“充满…的”，经法语进入英语', '-or': '来自拉丁语表示“做…的人”的词尾 -or，经古法语进入英语',
    '-s': '英语本来就有，古英语的复数词尾 -as', '-th': '英语本来就有，古英语写作 -þu / -þ', '-ship': '英语本来就有的后缀，古英语写作 -scipe',
    '-hood': '英语本来就有的后缀，古英语写作 -had', '-dom': '英语本来就有的后缀，古英语写作 -dom', '-ward': '英语本来就有的后缀，古英语写作 -weard',
    '-some': '英语本来就有的后缀，古英语写作 -sum', '-ling': '英语本来就有的后缀，古英语写作 -ling', '-ty': '来自拉丁语 -tas，经法语 -té 进入英语',
    '-ity': '来自拉丁语 -itas，经法语 -ité 进入英语', '-ize': '来自希腊语动词词尾 -izein，经拉丁语 -izare、法语 -iser 进入英语',
    '-ise': '来自希腊语动词词尾 -izein，经拉丁语 -izare、法语 -iser 进入英语', '-ance': '来自拉丁语 -antia，经法语进入英语', '-ence': '来自拉丁语 -entia，经法语进入英语',
    '-ary': '来自拉丁语 -arius', '-ory': '来自拉丁语 -orius', '-ar': '来自拉丁语形容词词尾 -aris', '-ion': '来自拉丁语名词词尾 -io，经法语进入英语',
    '-ist': '来自希腊语 -istēs，经拉丁语 -ista、法语 -iste 进入英语', '-ism': '来自希腊语 -ismos，经拉丁语 -ismus 进入英语', '-ian': '来自拉丁语 -ianus',
    '-ee': '来自法语“被…的”形式的词尾 -é', '-ette': '来自法语表示“小”的词尾 -ette', '-et': '来自古法语表示“小”的词尾 -et', '-ure': '来自拉丁语 -ura，经法语进入英语',
    '-ery': '来自古法语 -erie', '-ation': '来自拉丁语 -atio，经法语进入英语', '-iation': '来自拉丁语 -atio，经法语进入英语', '-ish': '英语本来就有的后缀，古英语写作 -isc', '-ed': '英语本来就有，古英语“被…了的”形式的词尾 -ed',
    '-ing': '英语本来就有，古英语写作 -ung / -ing', '-est': '英语本来就有，古英语最高级词尾 -est', '-ier': '英语本来就有，古英语比较级词尾 -ra',
}
DIFF = re.compile(r'不是英语本族|而是|并不是|来自古法语|法语来的|法语的|拉丁来的|希腊来的|这里来自|这里是')


def tokens(s):
    """顶层按 ，；：。 切开：[(文字, 后面的分隔符)]"""
    out, d, q, cur = [], 0, 0, ''
    for ch in s:
        if ch in '（(':
            d += 1
        elif ch in '）)':
            d = max(0, d - 1)
        elif ch == '“':
            q += 1
        elif ch == '”':
            q = max(0, q - 1)
        if d == 0 and q == 0 and ch in '，；：。':
            out.append([cur, ch])
            cur = ''
        else:
            cur += ch
    out.append([cur, ''])
    return out


def join(toks):
    s = ''.join(t + sep for t, sep in toks)
    return s


def tidy_src(S):
    S = S.strip().strip('，；。')
    S = re.sub(r'^(?:这里|它本身|它|本身|这个后缀|这个词尾)\s*', '', S)
    S = re.sub(r'^(?:其实|也|就|都|最早)\s*', '', S)
    S = re.sub(r'^是(?=来自|源自|出自|借自)', '', S)
    S = re.sub(r'^(?:是|就是)\s*(' + LANG + r')(?:原有的|里的|的)?\s*', r'来自\1 ', S)
    S = re.sub(r'^经(\S{1,6}?)来自\s*(\S+)', r'来自\2，经\1', S)
    S = re.sub(r'（同 ([^（）]*)）', r'；同 \1', S)
    S = re.sub(r'（见第 \d+ 组 [^（）]*）', '', S)
    S = re.sub(r'（见 ([^（）]+)）', r'，见 \1', S)
    S = re.sub(r'（(经[^（）]*)）', r'，\1', S)
    S = re.sub(r'（(←[^（）]*)）', r'，\1', S)
    S = re.sub(r'（([^（）]*)）', r'：\1', S)
    S = re.sub(r'(来自|源自|出自)' + r'((?:古|中古|晚期|中世纪|俗)?(?:拉丁|希腊|法|意大利|西班牙|荷兰|德|古诺尔斯|葡萄牙))(?!语)', r'\1\2语', S)
    S = re.sub(r'的(?=\s*-)', '', S, count=1) if re.match(r'^来自\S+语的\s*-', S) else S
    S = re.sub(r'，，+', '，', S)
    return S.strip('，；')


def insert_src(body, S):
    """把来源 S 放进括号：有“（同 …）”就并进去，没有就跟在第一小句后面"""
    m = re.search(r'（同 ', body)
    if m and _depth(body, m.start()) == 0:
        return body[:m.start()] + '（' + S + '；同 ' + body[m.end():]
    toks = tokens(body)
    toks[0][0] = toks[0][0].rstrip() + '（' + S + '）'
    return join(toks)


def _depth(s, i):
    d = 0
    for ch in s[:i]:
        if ch in '（(':
            d += 1
        elif ch in '）)':
            d = max(0, d - 1)
    return d


def fix_line(lab, line):
    """返回 (新行, 用的哪种办法)；办不了返回 (原行, '')"""
    if '：' not in line:
        return line, ''
    head, body = line.split('：', 1)
    core = re.sub(r'（[^（）]*）', '', lab).strip()
    toks = tokens(body)
    # A：正文里有一句是这个后缀自己的来源
    for i, (t, sep) in enumerate(toks):
        ts = t.strip()
        if OWN.match(ts) and not re.search(r'整个词|这个词|单词|这个名字|动词本身|名词本身', ts.split('来自')[0]):
            j = i
            while j + 1 < len(toks) and toks[j][1] == '，' and CONT.match(toks[j + 1][0].strip()):
                j += 1
            S = tidy_src('，'.join(x[0].strip() for x in toks[i:j + 1]))
            rest = toks[:i] + toks[j + 1:]
            if i > 0 and j + 1 < len(toks):
                rest[i - 1][1] = toks[i - 1][1] if toks[i - 1][1] in '；。' else toks[j][1]
            elif i > 0:
                rest[i - 1][1] = toks[j][1]
            body2 = join(rest).strip()
            body2 = re.sub(r'[，；]\s*$', '', body2)
            if not body2:
                return line, ''
            return head + '：' + insert_src(body2, S), 'A'
    # B：写着“英语本族的后缀 / 词尾”
    for i, (t, sep) in enumerate(toks):
        ts = t.strip()
        if NATIVE.match(ts) and not re.search(r'不是', ts):
            S = '英语本来就有的后缀' + ('，' + OE[core] if OE.get(core) else '')
            rest = toks[:i] + toks[i + 1:]
            if i > 0:
                rest[i - 1][1] = toks[i - 1][1] if toks[i - 1][1] in '；。' or i + 1 >= len(toks) else sep
            body2 = re.sub(r'[，；]\s*$', '', join(rest).strip())
            if not body2:
                return line, ''
            return head + '：' + insert_src(body2, S), 'B'
        m = re.search(r'[，；]?\s*(?:这是|是)?英语本族(?:的)?(?:形容词|名词|动词)?(?:后缀|词尾)(?=[，；。]|$)', t)
        if m and not re.search(r'不是|而是|而$', t[:m.end()]) and not t[:m.start()].rstrip().endswith('而'):
            S = '英语本来就有的后缀' + ('，' + OE[core] if OE.get(core) else '')
            toks[i][0] = t[:m.start()] + t[m.end():]
            body2 = re.sub(r'[，；]\s*$', '', join(toks).strip())
            return head + '：' + insert_src(body2, S), 'B'
    # C：开头就是“拉丁语……词尾 -ior”
    m = re.match(r'^(?:是|这是|一个|=\s*|就是\s*)?(' + LANG + r')(?:的)?\s*(.*)$', body)
    if m and m.group(1) and not re.match(r'^(?:里|中)?(?:的)?(?:单词|这个词)', m.group(2)):
        lang = m.group(1)
        lang = lang if lang.endswith('语') else lang + '语'
        rest = re.sub(r'^(?:里|中|来的|里的|的)\s*', '', m.group(2))
        form = ''
        f = re.match(r'^(-[A-Za-zāēīōūæœþðȳ\-]+(?:\s*/\s*-[A-Za-zāēīōūæœþðȳ\-]+)?)\s*[，、]?\s*', rest)
        if f:
            form, rest = f.group(1), rest[f.end():]
        else:
            f = re.search(r'(词尾|后缀|成分|标记|形式|结尾|词缀)\s*(-[A-Za-zāēīōūæœþðȳ\-]+(?:\s*/\s*-[A-Za-zāēīōūæœþðȳ\-]+)?)', rest)
            if f and _depth(rest, f.start(2)) == 0:
                form = f.group(2)
                rest = rest[:f.start(2)].rstrip() + rest[f.end(2):]
            else:
                f = re.search(r'(词尾|后缀|成分|标记|形式|结尾|词缀)（(-?[A-Za-zāēīōūæœþðȳ\- /]+)）', rest)
                if f:
                    form = f.group(2).strip()
                    rest = rest[:f.end(1)] + rest[f.end():]
        f2 = re.match(r'^（(经[^（）]*|←[^（）]*)）\s*', rest)
        via = ''
        if f2:
            via, rest = '，' + f2.group(1), rest[f2.end():]
        else:
            f3 = re.search(r'(词尾|后缀|成分|标记|形式)（(经[^（）]*|←[^（）]*)）', rest)
            if f3:
                via = '，' + f3.group(2)
                rest = rest[:f3.end(1)] + rest[f3.end():]
        rest = re.sub(r'^[，、\s]+', '', rest)
        rest = re.sub(r'(词尾|后缀|成分|标记|形式)\s+(?=经)', r'\1，', rest)
        if lang == '日耳曼语':
            return line, ''
        if not rest:
            return line, ''
        S = '来自' + lang + (' ' + form if form else '') + via
        return head + '：' + insert_src(rest, S), 'C'
    # D：后缀本身没写来源，补标准说法（这一行若说明它另有来历，就不补，留给人工）
    pm = re.search(r'（经([^（），]+)，来自([^（）]+)）', body)
    if pm:
        return head + '：' + body[:pm.start()] + '（来自' + pm.group(2) + '，经' + pm.group(1) + '进入英语）' + body[pm.end():], 'P'
    if re.search(r'反复|一下又一下|一下一下|一下接一下', body) and core in ('-er', '-le', '-el'):
        S = '英语本来就有的后缀，古英语写作 ' + ('-rian' if core == '-er' else '-lian') + '，表示“一下接一下地做”'
        return head + '：' + insert_src(re.sub(r'(?:这里不是“…的人”，而是)?英语本族的(?:“反复”)?(?:动词)?词尾[：，]?', '', body), S), 'D'
    if core in ('-en', '-n'):
        if re.search(r'使|变得', body) and not re.search(r'被…了|已经…了', body):
            return head + '：' + insert_src(body, '英语本来就有的后缀，古英语写作 -nian'), 'D'
        if re.search(r'被…了|已经…了', body) and not re.search(r'不是|而是', body):
            return head + '：' + insert_src(body, '英语本来就有，古英语“被…了的”形式的词尾 -en'), 'D'
    if core == '-ish' and re.search(r'法语来的动词', body):
        return head + '：' + insert_src(body, '来自古法语动词变化时带出的 -iss-，← 拉丁语 -isc-'), 'D'
    if core == '-y' and re.search(r'^形容词词尾', body) and not re.search(r'不是|而是', body):
        b2 = re.sub(r'[；，]\s*古英语(?:里就是|写作|里是) -ig(?=[，；。]|$)', '', body)
        return head + '：' + insert_src(b2, '英语本来就有的后缀，古英语写作 -ig'), 'D'
    if core in STD and not DIFF.search(body) and not (core in ('-er', '-or') and not re.search(r'的人|的东西|的家伙', body)):
        S = STD[core]
        if core == '-y' and re.match(r'^名词词尾', body):
            S = '来自拉丁语、希腊语的名词词尾 -ia，经法语 -ie 进入英语'
        if core == '-en':
            S = None
        if core == '-ish' and re.search(r'动词', body):
            S = None
        if core == '-le':
            S = None
        if S:
            return head + '：' + insert_src(body, S), 'D'
    return line, ''


_fix_plain = fix_line
def fix_line(lab, line):
    """2026-11 词缀身份辨析轮起：新写法的词缀行（标签：身份：介绍；记：…。辨析：…）只改“开头的介绍”那一段，“身份：”这个记号、记法、辨析照留"""
    import linetools as LT
    head, main, tail = LT.affix_split(line)
    if not head.endswith(LT.ID_MARK): return _fix_plain(lab, line)
    plain_head = head[:-len(LT.ID_MARK)]
    new, how = _fix_plain(lab, plain_head + main)
    if not how or not new.startswith(plain_head): return line, ''
    return head + new[len(plain_head):] + tail, how


def run(src, out, note='来源进括号'):
    import json, copy
    from openpyxl import load_workbook
    from video_check import check_rows, load_rows, source_of
    rows = load_rows(src)
    found = check_rows(rows)
    want = {}
    for rn, w, msg in found['suf_src_text_only']:
        want.setdefault(rn, set()).add(msg.split(' ')[0])
    wb = load_workbook(src)
    ws = wb['拆分结果']
    done, left = [], []
    for rn, labs in sorted(want.items()):
        import cols as C
        H = C.get_parts(ws, rn).split('\n')                # 前缀、词根、单词部分、后缀四列合起来
        changed = []
        for k, l in enumerate(H):
            lab = l.split('：', 1)[0]
            if lab not in labs:
                continue
            new, how = fix_line(lab, l)
            if how and source_of(new)[1] == 'paren':
                H[k] = new
                changed.append(lab)
                done.append((rn, ws.cell(rn, 5).value, lab, how, l, new))
            else:
                left.append((rn, ws.cell(rn, 5).value, lab, l))
        if changed:
            C.set_parts(ws, rn, '\n'.join(H))
            p = ws.cell(rn, C.ADJ)
            p.value = (str(p.value) + '；' if p.value else '') + note + '：' + '、'.join(changed) + ' 的来源挪进括号'
    wb.save(out)
    return done, left


if __name__ == '__main__':
    import pickle
    note = sys.argv[sys.argv.index('--note') + 1] if '--note' in sys.argv else '来源进括号'
    done, left = run(sys.argv[1], sys.argv[2], note)
    pickle.dump((done, left), open(sys.argv[2] + '.srcfix.pkl', 'wb'))
    print('挪进括号', len(done), '行；没处理', len(left), '行')

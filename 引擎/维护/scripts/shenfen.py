# -*- coding: utf-8 -*-
"""词根列只讲词根本身 + 同一个词根几种写法的身份和分工（2026-11 身份分工、辨析列轮，project_rules.md 第 65、66 条）。
1. 词根列每一行只讲这个词根：把“词根的意思 → 前缀“…”… → 今天的意思”这条链切出去（怎么组合、意思怎么来在组合列）；
   链里组合列没有的东西（拉丁语、希腊语里合成的那个原词）和单独一行讲“合起来是…”的话，挪到组合列第一行下面的“　合起来：”一行；
   前缀在这个词里取的意思，前缀列没写的补“；这里是“…””。
2. 同一个词根的几种写法：词根那一行在“字母变化：…。”后面加“身份：…。分工：…。”（数据在 shenfen_data.py，一个词根族一条）。
用法：
  cut(line)            一行词根解释里要切出去的链（没有返回 None）——shenfen_check.py 用它查还有没有混着的
  heqi_line(line, w)   这一行是不是单独讲“合起来”的
  plan(data, C)        全表试算：{行下标: {root: 新词根格, heqi: [合起来的话], pre: {前缀标签: 要补的意思}, notes: […]}}，统计
  python3 shenfen.py <表.xlsx>      打印试算的统计和要人工看的提示（不写表；写表见 scripts/archive/shenfen/round.py）"""
import re, collections
from linetools import top_find, top_split, cut_memo, label_body
import shenfen_data as FD

VARL = re.compile(r'^([^：]{1,40})：词根\s*([A-Za-z]+)\s*的另一种写法')
DONGBIAN = re.compile(r'动词变化：[^。\n]*?；规律：[^。\n]*?(?:。|(?=；记：)|$)')      # 和 cols.py、dongbian.py 同一个写法
ANCH = re.compile(r'意思(?:是|[：:])')
LANGS = ['日耳曼语', '中世纪拉丁语', '晚期拉丁语', '俗拉丁语', '通俗拉丁语', '民间拉丁语', '拉丁语', '中世纪希腊语', '希腊语', '古北部法语', '古法语', '英法语', '法语',
         '古英语', '中古英语', '意大利语', '西班牙语', '古诺尔斯语', '古诺斯语', '阿拉伯语', '德语', '荷兰语', '梵语', '法兰克语']
core = lambda lab: re.sub(r'[（(][^（）()]*[）)]', '', lab).strip().strip('-')
FOREIGN = re.compile(r"\*?[A-Za-zāēīōūăĕĭŏŭæœéèêáíóúàçñþðǣ]{3,}(?:[-’'][A-Za-zāēīōū]+)?")

CUE = re.compile(r'词典|说法不一|无关|不是|省掉|相反|其实|存疑|注意|有没有关系')
FACT = re.compile(r'\d{3,4}\s*年?|\d{1,2}\s*世纪|亚里士多德|斯托克斯|罗马人|拜占庭|阿拉伯|骑士|神父|教会|炼金')

def top_ok(s, i):
    pre = s[:i]
    return pre.count('（') + pre.count('(') == pre.count('）') + pre.count(')') and pre.count('“') == pre.count('”')

def find_anchor(rest):
    """意思那一段从哪儿起：(起点, 锚的长度, 类型)"""
    k0 = 0
    mc = re.search(r'字母变化：', rest)
    if mc:
        e = top_find(rest, '。', mc.end())
        k0 = e + 1 if e >= 0 else len(rest)
    for m in ANCH.finditer(rest):
        if m.start() >= k0 and top_ok(rest, m.start()):
            return m.start(), m.end() - m.start(), 'yisi'
    for m in re.finditer(r'(?:即)?本组词根(?=“)', rest):
        if top_ok(rest, m.start()):
            return m.start(), m.end() - m.start(), 'benzu'
    for m in re.finditer(r'[；。]\s*这里是(?=“)', rest):
        if top_ok(rest, m.start()):
            return m.start(), m.end() - m.start(), 'zheli'
    return None

def cut(line):
    """-> dict 或 None（这一行没有要切的链）"""
    body, memo = cut_memo(DONGBIAN.sub('', line))      # 2026-11 拉丁语动词变化轮：“动词变化：原形 …→ 过去式 …→ 过去分词 …；规律：…。”里的“→”不是通到今义的链
    label, rest = label_body(body)
    if label is None: return None
    a = find_anchor(rest)
    if not a: return None
    st, ln, kind = a
    seg = rest[st + ln:]
    k = top_find(seg, '→')
    if k < 0: return None
    return dict(label=label, head=rest[:st], anchor=rest[st:st + ln], gloss=seg[:k].rstrip(), chain=seg[k:].strip(), memo=memo, kind=kind)

def eq_terms(combo):
    """组合列第一行等式左边的 [(部分, 括号里的意思)]"""
    first = str(combo or '').split('\n')[0].replace('【构词逻辑】', '')
    first = re.sub(r'；\s*词性变化.*$', '', first)
    i = top_find(first, '=')
    left = first[:i] if i >= 0 else first
    out = []
    for t in top_split(left, '+'):
        m = re.match(r'^\s*([A-Za-z()=\-\' ]+?)\s*（(.*)）\s*$', t.strip())
        if m: out.append((m.group(1).strip(), m.group(2).strip()))
    return out

def lang_of(*texts):
    for t in texts:
        best = None
        for L in LANGS:
            k = str(t or '').find(L)
            if k >= 0 and (best is None or k < best[0]): best = (k, L)
        if best: return best[1]
    return ''

def nodes_of(chain):
    return [x.strip() for x in top_split(chain, '→') if x.strip()]

def forms_in(node):
    """这一步括号里的外语原词：[(原词, 括号里它自己的意思, 括号里别的话, 语言)]"""
    out = []
    for m in re.finditer(r'（([^（）]*(?:（[^（）]*）[^（）]*)*)）', node):
        inner = m.group(1).strip()
        if re.match(r'^(同|见|即|如|比如|也|今|英|美|数|名词|动词|形容词|怎样|热|身体|较)', inner): continue
        lang = next((L for L in LANGS if inner.startswith(L)), '')
        body = inner[len(lang):].strip()
        mf = re.match(r'^(\*?[A-Za-zāēīōūæœéèêçñ]{3,}(?:\s*[/／]\s*\*?[A-Za-zāēīōū]+)?)\s*(?:“([^”]*)”)?\s*[，：:；]?\s*(.*)$', body)
        if not mf: continue
        out.append((mf.group(1), mf.group(2) or '', mf.group(3).strip(), lang))
    return out

def node_text(node):
    t = re.sub(r'（[^（）]*(?:（[^（）]*）[^（）]*)*）', '', node).strip()
    t = re.sub(r'^([A-Za-z]+(?:\([A-Za-z=]+\))?)\s*“([^”]*)”', r'\2', t)      # ef“出来”做 → 出来做
    return t.strip(' ；，')

def norm(s):
    return re.sub(r'[āăǣ]', 'a', re.sub(r'[ēĕ]', 'e', re.sub(r'[īĭ]', 'i', re.sub(r'[ōŏ]', 'o', re.sub(r'[ūŭ]', 'u', s.lower()))))).replace('*', '')

def bigrams(t):
    z = re.sub(r'[^\u4e00-\u9fff]', '', t)
    return {z[i:i + 2] for i in range(len(z) - 1)}

# ------------------------------------------------------------------ 单独一行讲“合起来”的（整个词在拉丁语、希腊语里是怎么合成的）
HEQI_HEAD = [
    (re.compile(r'^来历：两部分很可能合成了'), '很可能是'),
    (re.compile(r'^(两部分|两者)?合起来(是|就是|：)\s*'), ''),
    (re.compile(r'^(两部分|两者)合成(了)?\s*'), ''),
    (re.compile(r'^日耳曼语的合成词：'), '日耳曼语 '),
]
LANG_LEAD = re.compile(r'^(' + '|'.join(LANGS) + r')\s*(?:短语\s*)?\*?[A-Za-zāēīōūæé]+')
NO_MOVE = {'fountain', 'catapult', 'hustle', 'couple'}
KEEP_EXTRA = re.compile(r'^(整个词|哪里变了|怎么变成|拼写|读音|变化经过|传进英语的路线|字母怎么变|为什么|注意|易混|对照|来源|要点|切分|①|②)')

def heqi_line(line, word):
    """词根列（单词部分列）里单独一行、讲两部分合起来是什么的 → 组合列“合起来”那一行的文字；不是返回 None"""
    s = line.strip()
    if KEEP_EXTRA.match(s) or word in NO_MOVE: return None
    for rx, rep in HEQI_HEAD:
        if rx.match(s):
            return rep + rx.sub('', s, count=1)
    if LANG_LEAD.match(s) and not re.match(r'^[^：]{1,12}：', s):
        return s
    return None

FGALL = {}
def fam_gloss_table(data, C):
    """每个词根族最常见的“词根“意思”（来源）”写法（给只写了“这里是…”的行补词根本身的意思）"""
    cnt = collections.defaultdict(collections.Counter)
    for r in data:
        for line in str(r[C['root']] or '').split('\n'):
            m = VARL.match(line)
            if not m: continue
            c = cut(line)
            body = cut_memo(line)[0]
            g = c['gloss'] if c and c['kind'] == 'yisi' else None
            if g is None:
                mm = re.search(r'意思(?:是|[：:])\s*([^；。→]*)', body)
                g = mm.group(1).strip() if mm else None
            if not g: continue
            X = m.group(2)
            g = norm_gloss(g, X)
            if re.match(r'^[A-Za-z]+“[^”]+”', g): cnt[(r[C['grp']], X)][g] += 1 + (2 if '（' in g else 0)
    FGALL.clear(); FGALL.update({k: list(v) for k, v in cnt.items()})
    return {k: v.most_common(1)[0][0] for k, v in cnt.items()}

def norm_gloss(g, X):
    """“意思”后面那一段写齐引号：站 → “站”；带着词根的（sta“站”（来源））原样"""
    g = g.strip()
    if re.match(r'^[\u4e00-\u9fff、]+$', g): return '“%s”' % g
    m = re.match(r'^([\u4e00-\u9fff、]+)(（.*）)$', g)
    if m: return '“%s”%s' % (m.group(1), m.group(2))
    return g

def identity(forms, Y, word):
    v = forms.get(Y)
    if v is None: return None
    if isinstance(v, dict): v = v.get(word, v['*'])
    return FD.ID.get(v, v)

def plan(data, C):
    words = {r[C['word']] for r in data}
    FG = fam_gloss_table(data, C)
    GBG = {}
    for r in data:
        if r[C['bg']] and r[C['grp']] not in GBG: GBG[r[C['grp']]] = str(r[C['bg']])
    out = {}          # rowidx -> dict(root=新词根格, heqi=[合起来的话], pre={前缀标签: 要补的“这里是”}, notes=[给人看的提示])
    stat = collections.Counter()
    for ri, r in enumerate(data):
        v = str(r[C['root']] or '')
        if v.strip() in ('', '-'): continue
        word, g = r[C['word']], r[C['grp']]
        other = '\n'.join(str(r[C[k]] or '') for k in ('combo', 'bg', 'snd', 'pre', 'suf', 'wp')) + '\n' + GBG.get(g, '')
        for l0 in v.split('\n'):
            c0 = cut(l0)
            other += '\n' + ((c0['head'] + c0['gloss']) if c0 else l0)
        other_n = norm(other)
        terms = eq_terms(r[C['combo']])
        res = dict(root=None, heqi=[], pre={}, notes=[], cut=[])
        newlines = []
        lines = v.split('\n')
        # 先看单独的“合起来”行：它们讲到的原词算已经有了
        moved = []
        for li, line in enumerate(lines):
            h = heqi_line(line, word) if li > 0 or label_body(line)[0] is None else None
            moved.append(h)
        moved_text = norm(' '.join(x for x in moved if x))
        for li, line in enumerate(lines):
            if moved[li] is not None:
                res['heqi'].append(moved[li]); stat['heqi_line_moved'] += 1
                continue
            body, memo = cut_memo(line)
            label, rest = label_body(body)
            mv = VARL.match(line)
            c = cut(line)
            new_body = body
            if c:
                stat['chain_cut'] += 1
                X = mv.group(2) if mv else ''
                chain = c['chain']
                # 链后面跟着的别的话（句号以后）：留在词根行
                trail = ''
                kdot = top_find(chain, '。')
                if kdot >= 0:
                    trail = chain[kdot + 1:].strip(); chain = chain[:kdot]
                nodes = nodes_of(chain)
                if nodes:
                    parts = top_split(nodes[-1], '；')
                    kk = next((i for i, x in enumerate(parts) if i and CUE.search(x)), None)
                    if kk is not None:
                        trail = '；'.join(parts[kk:]).strip() + ('。' + trail if trail else '')
                        nodes[-1] = '；'.join(parts[:kk])
                for nd in nodes:
                    for mk in FACT.findall(node_text(nd)):
                        if mk not in other: res['notes'].append('史实没着落：' + mk + ' ← ' + node_text(nd)[:40])
                # 前缀在这个词里的意思
                m0 = re.match(r'^([A-Za-z]+)(?:\(=?([A-Za-z]+)\))?\s*“([^”]*)”', nodes[0]) if nodes else None
                if m0:
                    stat['chain_with_prefix'] += 1
                    pfx, gl = m0.group(1), m0.group(3)
                    pl = next((l for l in str(r[C['pre']] or '').split('\n') if core(label_body(l)[0] or '').lower() == pfx.lower()), None)
                    eg = next((gg for t, gg in terms if core(t).lower() == pfx.lower()), '')
                    if pl is not None:
                        key = lambda s: set(re.sub(r'[^\u4e00-\u9fff]', '', s))
                        covered = gl in pl or (eg and eg in pl) or '这里' in pl or (len(key(gl) & key(pl)) >= max(1, len(key(gl)) - 1))
                        if not covered:
                            res['pre'][label_body(pl)[0]] = eg or gl; stat['prefix_here_added'] += 1
                # 链里组合列没有的原词
                items = []
                last_lang = ''
                for nd in nodes:
                    for form, fgl, note, lang in forms_in(nd):
                        fn = norm(form.split('/')[0].strip())
                        if fn in words or fn in other_n or fn in moved_text or fn == norm(word): continue
                        gl = fgl or node_text(nd)
                        lang = lang or lang_of(c['head'] + c['gloss'], r[C['bg']]) or ''
                        it = ('%s %s' % (lang, form) if lang and lang != last_lang else form) + ('“%s”' % gl if gl else '') + ('（%s）' % note if note else '')
                        last_lang = lang or last_lang
                        items.append(it.strip())
                if items:
                    res['heqi'].append(' → '.join(items)); stat['heqi_from_chain'] += 1
                # 链里的话组合列有没有：没有的提示出来人工看
                cb = bigrams(str(r[C['combo']] or ''))
                weak = []
                for nd in nodes[(1 if m0 else 0):]:
                    b = bigrams(node_text(nd))
                    if len(b) >= 3 and len(b & cb) / len(b) < 0.34: weak.append(node_text(nd))
                if weak: res['notes'].append('链里这几步组合列没有相近的话：' + ' | '.join(weak))
                res['cut'].append(c['chain'])
                # 新的一行
                gloss = c['gloss']
                if c['kind'] == 'yisi':
                    gl2 = norm_gloss(gloss, X) if mv else gloss
                    fg = FG.get((g, X), '') if mv else ''
                    mq = re.match(r'^(?:[A-Za-z]+)?“([^”]+)”$', gl2)
                    if mq:
                        full = [x for x in FGALL.get((g, X), []) if x.startswith('%s“%s”（' % (X, mq.group(1)))]
                        if full: gl2 = min(full, key=len)
                    tail = ('意思：' if mv else c['anchor']) + gl2
                    new_body = label + '：' + c['head'] + tail
                elif c['kind'] == 'benzu':
                    new_body = label + '：' + c['head'] + c['anchor'] + gloss
                else:   # 这里是“放”（…）
                    fg = FG.get((g, X), '')
                    head = c['head'].rstrip('；。 ')
                    new_body = label + '：' + head + '。意思：' + (fg + '；' if fg else '') + '这里是' + gloss
                if trail: new_body += ('；' if CUE.search(trail[:30]) and not trail.startswith('。') else '。') + trail.lstrip('。')
            # 身份、分工
            fam = None
            Y = (label or '').strip('-') if label else ''
            if mv and (g, mv.group(2)) in FD.FAM: fam = (g, mv.group(2))
            elif label and not mv:
                X2 = next((X for (gg, X) in FD.FAM if gg == g and X.lower() == core(label).lower()), None)
                if X2 and li == 0: fam = (g, X2); Y = X2
            if fam and '分工：' not in new_body:
                forms, text = FD.FAM[fam]
                idt = identity(forms, Y, word) or identity(forms, core(label), word)
                if idt is None: idt = FD.ID['B'] if not mv else None
                if idt is None:
                    res['notes'].append('没找到这个写法的身份：' + Y)
                else:
                    seg = '身份：%s。分工：%s' % (idt, text)
                    lab2, rest2 = label_body(new_body)
                    a = find_anchor(rest2)
                    if mv and a and a[2] == 'yisi':
                        st = a[0]
                        headp = rest2[:st].rstrip()
                        if headp and headp[-1] in '；，': headp = headp[:-1]
                        if headp and headp[-1] != '。': headp += '。'
                        new_body = lab2 + '：' + headp + seg + '。' + rest2[st:]
                    else:
                        nb = new_body.rstrip()
                        if nb[-1] in '；，': nb = nb[:-1]
                        new_body = nb + ('' if nb.endswith('。') else '。') + seg
                    stat['fenggong_var' if mv else 'fenggong_base'] += 1
            newlines.append(new_body + memo)
        new_root = '\n'.join(newlines) if newlines else '-'
        if new_root != v or res['heqi'] or res['pre']:
            res['root'] = new_root
            out[ri] = res
    return out, stat


if __name__ == '__main__':
    import sys
    from linetools import load_table
    hdr, C, data = load_table(sys.argv[1])
    out, stat = plan(data, C)
    print('要改的行 %d' % len(out)); [print('  %s: %d' % kv) for kv in sorted(stat.items())]
    for ri, v in out.items():
        for nt in v['notes']: print('  [%s] %s' % (data[ri][C['word']], nt))

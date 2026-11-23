"""把不标准的“词性变化”句子统一成：X“意思”加上 -xx（后缀的意思），就成了“结果”"""
import re, sys
sys.path.insert(0, '/home/claude/work/etymology-table/scripts')
import columns as C
from condense import top_eq_parts, affix_meaning, norm, GENERIC

TPL = re.compile(r'\s*(?:合起来)?(?:是一样东西或一种人|是一样东西或一门学问|是一样东西|是一种人|是一个动作|说的是一种特点或主张|说的是一种性质(?:或一样东西)?|'
                 r'说的是一样东西或一种性质|本身说的就是“什么样的”|说的是“什么样的”|说东西“什么样的”|说的是一件事、一种情况|说的是一个动作)\s*，?\s*')
EXTRA_SM = {'-ism': '…主义、…的做法', '-ship': '…的身份、关系、本事', '-hood': '…的身份、状态、时期', '-dom': '…的地位、领域', '-logy': '…学、研究…的学问',
            '-ics': '…学', '-ery': '…的地方、行业、一类东西', '-ry': '…的一类东西、行当', '-ful': '满满一…的量', '-et': '小…', '-ette': '小…', '-let': '小…',
            '-ling': '小…', '-ian': '…的人', '-ist': '做…的人、主张…的人', '-ee': '被…的人', '-cy': '…的性质、状态', '-ce': '…的性质、状态'}

def sm_for(lab, H, terms):
    core = re.sub(r'（[^（）]*）', '', lab).strip()
    m = affix_meaning(lab, H, terms)
    if not m or m in ('…', ''):
        m = EXTRA_SM.get(core, '')
    return m

def normalize(word, lab, txt, H, first):
    """返回 (新文字, 改了没有)"""
    head, sent = C.pos_head(txt), C.pos_sentence(txt)
    terms, lit, route = top_eq_parts(first)
    orig = sent
    s = sent
    # 母词换了意思的长句：X 本义“A”：……，就成了“B”。“B”是一样东西……，加上 -xx，指“R”
    m = re.match(r'^(?P<stem>[A-Za-z][A-Za-z\- ]*?) 本义“(?P<orig>[^”]*)”：.*?就成了“(?P<best>[^”]*)”。\s*“[^”]*”(?P<rest>.*)$', s)
    if m:
        s = '%s“%s”（本义“%s”）%s' % (m.group('stem'), m.group('best'), m.group('orig'), m.group('rest'))
    # X（g） 合起来 → X“g”
    s = re.sub(r'^([A-Za-z][A-Za-z\-]*)（([^（）]*)）\s*', lambda mm: '%s“%s”' % (mm.group(1), mm.group(2).replace(' + ', '、')), s)
    s = TPL.sub('', s)
    s = re.sub(r'，?\s*就成了一种主张', '', s)
    s = re.sub(r'，?\s*(?:指|表示|当动词就是)“', '，就成了“', s)
    s = re.sub(r'^，', '', s).strip()
    if not s.startswith('加上') and '加上' in s:
        pass
    # 没有前面部分：从第一行的等式取
    if s.startswith('加上') and terms:
        bt = terms[:-1] if len(terms) > 1 else terms
        if len(bt) == 1 and bt[0][1]:
            base = '%s“%s”' % bt[0]
        else:
            base = ' + '.join(t for t, _ in bt)
        s = base + ('' if base.endswith('”') else ' ') + s
    # 意思不变
    s = re.sub(r'），意思不变$', '），就成了“%s”（意思不变）' % (lit or ''), s)
    mm = C.SENT.match(s)
    if not mm:
        return txt, False
    base, suf, sm, res, tail = mm.group('base').strip(), mm.group('suf'), mm.group('sm') or '', mm.group('res'), mm.group('tail')
    if not sm:
        g = sm_for(lab, H, terms)
        if g:
            sm = '（%s）' % g
    if res in GENERIC and lit and ' / ' not in lit:
        res = lit
    new = '%s%s加上 %s%s，就成了“%s”%s' % (base, '' if base.endswith(('”', '）')) else ' ', suf, sm, res, tail)
    out = head + '。' + new
    return out, out != txt

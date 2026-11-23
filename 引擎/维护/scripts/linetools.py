# -*- coding: utf-8 -*-
"""读表（按列名，16 列 / 17 列的精简表、22 列的全表都行）和解释行的小工具。2026-11 身份分工、辨析列轮起的脚本都用它。
2026-11 词缀身份辨析轮（project_rules.md 第 83–88 条）起，前缀、后缀那一行写成
    标签：身份：开头的介绍[；记：记法][。辨析：辨析的话]
is_affix_label / affix_split / affix_parts / affix_join 认这个写法（上一版“标签：正文；身份：…。分工：…；记：…”的老写法也切得开，只是不再往表里写）。
2026-11 词缀关系轮（第 89–92 条）起，辨析的话最后可以有一段“；关系：…”（同一种语言来的几个词缀彼此是什么关系）：bx_split / rel_items / rel_heads。"""
import re

NAMES = dict(word='单词', mean='含义', typ='类型', split='拆分', pre='前缀', root='词根', wp='单词部分', suf='后缀', combo='组合',
             bx='辨析', bg='新·背景', snd='音变', var='词根变体处理', grp='组号', sub='小类号', batch='批次', seq='序号', ex='例句')

def load_table(path):
    """-> (表头 list, {角色: 列下标}, 数据行 list[list])。没有的列（辨析、例句）不在字典里"""
    from openpyxl import load_workbook
    wb = load_workbook(path, read_only=True)
    ws = wb['拆分结果'] if '拆分结果' in wb.sheetnames else wb.worksheets[0]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    hdr = [str(h or '') for h in rows[0]]
    n = len(hdr)
    data = [r + [None] * (n - len(r)) for r in rows[1:]]
    return hdr, cols_of(hdr), data

def cols_of(hdr):
    C = {}
    for k, name in NAMES.items():
        i = next((i for i, h in enumerate(hdr) if str(h).startswith(name)), None)
        if i is not None: C[k] = i
    return C

def top_find(s, chars, start=0):
    """括号、引号外面第一个属于 chars 的字符的位置；没有返回 -1"""
    d = q = 0
    for i in range(len(s)):
        c = s[i]
        if c in '（(': d += 1
        elif c in '）)': d = max(0, d - 1)
        elif c == '“': q += 1
        elif c == '”': q = max(0, q - 1)
        elif d == 0 and q == 0 and c in chars and i >= start:
            return i
    return -1

def top_split(s, seps):
    out, cur, d, q = [], '', 0, 0
    for c in s:
        if c in '（(': d += 1
        elif c in '）)': d = max(0, d - 1)
        elif c == '“': q += 1
        elif c == '”': q = max(0, q - 1)
        if c in seps and d == 0 and q == 0:
            out.append(cur); cur = ''
        else:
            cur += c
    out.append(cur)
    return out

MEMO_SPLIT = re.compile(r'；记：')
def cut_memo(line):
    """一行解释 → (正文, “；记：…”那一段)"""
    m = MEMO_SPLIT.search(line)
    if not m: return line, ''
    return line[:m.start()], line[m.start():]

def label_body(line):
    """“标签：解释” → (标签, 解释)；没有标签返回 (None, 整行)"""
    m = re.match(r'^\s*([^：:\n]{1,60}?)[：:]', line)
    if not m: return None, line
    return m.group(1).strip(), line[m.end():]


# ---------------------------------------------------------------- 2026-11 词缀身份辨析轮：词缀行的新写法
ID_MARK = '身份：'          # 紧跟在“标签：”后面：开头的介绍就是这个词缀的身份
MEMO_MARK = '；记：'
BX_MARK = '。辨析：'        # 一行的最后一段，到行末为止，里面没有句号
_AFFIX_TOK = r'-?[A-Za-z\u00C0-\u024F]+-?'
_AFFIX_LAB = re.compile(r'%s(?:\s*[、/]\s*%s)*' % (_AFFIX_TOK, _AFFIX_TOK))

def bare_label(lab):
    """标签去掉括号里的话：il-（= in-）→ il-，di(s)- → di-，-on(e) → -on"""
    return re.sub(r'（[^（）]*）|\([^()]*\)', '', str(lab or '')).strip()

def is_affix_label(lab, col):
    """这一行是不是讲一个词缀的行：前缀列（col='pre'）里以 - 结尾、后缀列（'suf'）里以 - 开头的标签。
    “为什么用 -ous 不用 -ful”“-ize 还是 -ise”“-ist + -ic”“注意”这类说明行不算"""
    b = bare_label(lab)
    if not b or not _AFFIX_LAB.fullmatch(b): return False
    toks = re.split(r'\s*[、/]\s*', b)
    return all(t.endswith('-') for t in toks) if col == 'pre' else all(t.startswith('-') for t in toks)

def affix_split(line):
    """词缀行 -> (头, 正文, 尾)，三段接起来就是原来那一行。
    新写法：头“标签：身份：”，正文是开头的介绍（这个词缀的身份），尾是“；记：…”“。辨析：…”（没有就是空的）
    老写法：头“标签：”，正文是这一行自己的话，尾是“；身份：…。分工：…”“；记：…”"""
    lab, body = label_body(line)
    head = line[:len(line) - len(body)]
    if body.startswith(ID_MARK):
        head += ID_MARK; body = body[len(ID_MARK):]
        cut = min([k for k in (body.find(MEMO_MARK), body.find(BX_MARK)) if k >= 0] or [len(body)])
        return head, body[:cut], body[cut:]
    main, memo = cut_memo(body)
    k = main.find('；身份：')
    if k >= 0: return head, main[:k], main[k:] + memo
    return head, main, memo

def affix_parts(line):
    """词缀行 -> dict(new 是不是新写法, label 标签, id 身份（开头的介绍）, memo 记法（不带“；记：”）, bx 辨析的话（不带“。辨析：”）)"""
    head, main, tail = affix_split(line)
    new = head.endswith(ID_MARK)
    memo = bx = ''
    if new:
        b = tail.find(BX_MARK)
        if b >= 0: bx = tail[b + len(BX_MARK):]; tail = tail[:b]
        if tail.startswith(MEMO_MARK): memo = tail[len(MEMO_MARK):]
    else:
        memo = cut_memo(tail)[1][len(MEMO_MARK):]
    return dict(new=new, label=label_body(line)[0], id=main, memo=memo, bx=bx)

def affix_join(label, idt, memo='', bx=''):
    """照新写法拼一行：标签：身份：介绍[；记：记法][。辨析：辨析的话]。介绍、记法末尾的句号、分号去掉"""
    s = '%s：%s%s' % (label, ID_MARK, str(idt).strip().rstrip('；。，'))
    if memo: s += MEMO_MARK + str(memo).strip().rstrip('；。')
    if bx: s += BX_MARK + str(bx).strip().rstrip('。')
    return s

def affix_plain(line):
    """词缀行去掉“身份：”这个记号和后面的记法、辨析，只剩“标签：开头的介绍”（体检脚本看这一行自己写了什么时用）"""
    head, main, tail = affix_split(line)
    return (head[:-len(ID_MARK)] if head.endswith(ID_MARK) else head) + main

def add_memo(line, memo):
    """给一行解释接上记法（memo 以“记：”开头）：词缀行有“。辨析：…”的插在它前面（身份 → 记 → 辨析），别的行接在行末"""
    line = line.rstrip()
    b = line.find(BX_MARK) if label_body(line)[1].startswith(ID_MARK) else -1
    if b < 0: return line.rstrip('。；;') + '；' + memo
    return line[:b].rstrip('。；;') + '；' + memo.rstrip('。；') + line[b:]

def cut_bianxi(line):
    """词缀行 -> (前面的, “。辨析：…”那一段)；不是新写法的词缀行、没有辨析的，后一半是空的"""
    b = line.find(BX_MARK) if label_body(line)[1].startswith(ID_MARK) else -1
    return (line, '') if b < 0 else (line[:b], line[b:])


# ---------------------------------------------------------------- 2026-11 词缀关系轮：辨析最后的“；关系：…”（project_rules.md 第 89–92 条）
REL_MARK = '；关系：'        # 辨析的话的最后一段：这一组里来自同一种语言、写法不同的词缀彼此是什么关系
_AFFIX_ONE = r'(?:-[A-Za-z]+|[A-Za-z]+-)'          # 一头带连字符的才算词缀：pre-、-ant

def bx_split(bx):
    """辨析的话 -> (辨析本身, 关系的话)；关系的话不带“关系：”，没有就是空的"""
    s = str(bx or '')
    k = s.find(REL_MARK)
    return (s, '') if k < 0 else (s[:k], s[k + len(REL_MARK):])

def rel_items(rel):
    """关系的话 -> 一条一条（括号、引号外面的“；”隔开）"""
    return [x.strip() for x in top_split(str(rel or ''), '；') if x.strip()]

def rel_heads(item):
    """一条关系开头讲的是哪几个词缀：“-ant、-ent 是…”“pre- 和 pro- 不是…” -> ['-ant', '-ent']；不是词缀打头的返回 []（体检会报）"""
    m = re.match(r'^(%s(?:\s*[、和]\s*%s)*)' % (_AFFIX_ONE, _AFFIX_ONE), str(item or '').strip())
    return re.findall(_AFFIX_ONE, m.group(1)) if m else []

# -*- coding: utf-8 -*-
"""部分记忆：给拆开以后还不好懂的部分加“；记：X ≈ Y（中文）：道理”（project_rules.md 第 59 条）
  python3 part_memo.py <表.xlsx> --dry              试一遍：各条用了几次、例子、要人看的短词根、还没有记法的词根
  python3 part_memo.py <表.xlsx> --write <新.xlsx>   写回：直接改 xlsx 里的共享字符串（别的格、格式、冻结、筛选都不动）
  python3 part_memo.py <表.xlsx> --check            体检：记法行写法对不对（和视频 wordfilm.js 的 MEMO_RX 同一套规则）、有没有关联词就是本词的
再跑一遍不变（已经有“记：”的行跳过）。"""
import re, sys, os, collections, zipfile, zlib, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from part_memo_data import R, ALLOW, SAME_OK, EXCEPT_AT, shift_for
from openpyxl import load_workbook
import linetools as LT

HEAD = re.compile(r'^\s*([^：:\n]{1,40})[：:]\s*(.*)$', re.S)
MEMO_RX = re.compile(r'[；;，,。]?\s*记[：:]\s*([A-Za-z][A-Za-z()\-]*)\s*([≈∽←])\s*([A-Za-z][A-Za-z\'’ \-]*?)\s*[（(]([^（）()]*)[）)]\s*[：:]\s*([^\n]*)$')
COLS = ('前缀', '词根', '后缀')
BY = collections.defaultdict(list)
for i, (cores, need, sym, anc, zh, why, avoid) in enumerate(R):
    for c in cores.split():
        BY[c].append(i)

def core_of(lab):
    s = re.sub(r'[（(][^（）()]*[）)]', '', lab).strip().lower()
    s = s.strip('-').strip()
    return s if re.fullmatch(r'[a-z]+', s) else ''

ROOT_OF = re.compile(r'词根\s*([A-Za-z]+)\s*的另一种写法|由词根\s*([A-Za-z]+)\s*变来')
def root_of(text):
    """词根的另一种写法那一行（“词根 duc 的另一种写法（同一个词根）…”，老写法“由词根 duc 变来”）：返回词根本身"""
    m = ROOT_OF.search(text)
    return (m.group(1) or m.group(2)).lower() if m else ''

def pick(core, text, word):
    """这一行用哪条记法：先看自己的写法，再看这一行说的词根（“词根 X 的另一种写法”）；need 对得上、avoid 对不上、关联词不是本词也不是这一部分"""
    tries = [(core, False)]
    x = root_of(text)
    if x and x != core:
        tries.insert(0, (x, True))            # 2026-11：变体行先按词根本身配（记法写 duc ∽ duck，不写 duct ≈ …）
    for c, inh in tries:
        for i in BY.get(c, []):
            cores, need, sym, anc, zh, why, avoid = R[i]
            if not re.search(need, text) or (avoid and re.search(avoid, text)):
                continue
            wl, al = word.lower(), anc.lower()
            if (anc, word) in EXCEPT_AT:                                       # 关联词不比这个词简单：这个词不写（标“记法待补”）
                return None
            if al == wl or (al == c and al not in SAME_OK) or ((al.startswith(wl) or wl.startswith(al)) and al not in SAME_OK):     # 关联词就是本词（或本词的另一种拼法 dialog / dialogue）
                return None
            return i, inh
    return None

def memo_text(core, i):
    cores, need, sym, anc, zh, why, avoid = R[i]
    t = '记：%s %s %s（%s）：%s' % (core, sym, anc, zh, why.format(c=core))
    nt = shift_for(anc, zh, core) if sym == '≈' else None        # ≈ 两边写法差得多的：接上“音变”
    return t + ('。音变：' + nt if nt else '')

def plan(path):
    wb = load_workbook(path, read_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = ws.iter_rows(values_only=True)
    hdr = list(next(rows))
    ci = {h: hdr.index(h) for h in COLS}
    wi = hdr.index('单词')
    changes, stat, todo, short, inh_list = {}, collections.Counter(), collections.Counter(), collections.defaultdict(list), []
    for rn, r in enumerate(rows, start=2):
        word = str(r[wi] or '')
        for col in COLS:
            v = r[ci[col]]
            if not v or str(v).strip() in ('-', '—'):
                continue
            lines = str(v).split('\n'); new = []; changed = False
            for ln in lines:
                m = HEAD.match(ln)
                core = core_of(m.group(1)) if m else ''
                if not core or '记：' in ln or (col != '词根' and core not in ALLOW[col]):
                    new.append(ln); continue
                body = LT.affix_parts(ln)['id'] if m.group(2).startswith(LT.ID_MARK) else m.group(2)      # 词缀行只看开头的介绍（不看记号、辨析里别的词缀的话）
                hit = pick(core, body, word)
                if not hit:
                    if col == '词根':
                        todo[core] += 1
                    new.append(ln); continue
                i, inh = hit
                new.append(LT.add_memo(ln, memo_text(root_of(m.group(2)) or core if inh else core, i))); changed = True      # 词缀行有“。辨析：…”的，记法插在它前面
                stat[i] += 1
                if inh: inh_list.append((word, core, R[i][3]))
                if len(core) <= 3: short[(core, R[i][3])].append(word)
            if changed:
                changes[(rn, ci[col])] = '\n'.join(new)
    wb.close()
    return hdr, changes, stat, todo, short, inh_list

def dry(path):
    hdr, changes, stat, todo, short, inh = plan(path)
    lines = sum(1 for v in changes.values() for ln in v.split('\n') if '记：' in ln)
    print('要改的格 %d，加记法的行 %d；用到的条目 %d / %d' % (len(changes), lines, len(stat), len(R)))
    print('按关联词：' + '  '.join('%s%s×%d' % (R[i][2], R[i][3], n) for i, n in stat.most_common()))
    print('没用上的条目：' + '、'.join(R[i][3] for i in range(len(R)) if i not in stat))
    print('\n短词根（3 个字母以内）用到的词（人工看意思对不对）：')
    for (c, a), ws in sorted(short.items()):
        print('  %s→%s：%s' % (c, a, '、'.join(ws[:14]) + ('…%d' % len(ws) if len(ws) > 14 else '')))
    print('\n“由词根 X 变来”借用的：' + '、'.join('%s(%s→%s)' % x for x in inh[:60]) + ('…共%d' % len(inh) if len(inh) > 60 else ''))
    print('\n词根列还没有记法的行 %d（%d 个写法），最常见：' % (sum(todo.values()), len(todo)) + '、'.join('%s×%d' % kv for kv in todo.most_common(45)))
    return changes

def check(path):
    wb = load_workbook(path, read_only=True); ws = wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True)); hdr = list(rows[0]); rows = rows[1:]; wi = hdr.index('单词')
    typ_of = {str(r[wi]): str(r[hdr.index('类型')] or '') for r in rows}; split_of = {str(r[wi]): str(r[hdr.index('拆分')] or '') for r in rows}
    n = bad = hard = notroot = noshift = 0
    for r in rows:
        for col in COLS:
            for ln in str(r[hdr.index(col)] or '').split('\n'):
                if not re.search(r'记：\s*[A-Za-z][A-Za-z()\-]*\s*[≈∽←]', ln): continue      # “可以这样记：…”这类老说明不算
                n += 1
                m = MEMO_RX.search(ln)
                if not m or m.group(3).strip().lower() == str(r[wi]).lower():
                    bad += 1; print('写法不对：', r[wi], ln[-80:]); continue
                a, sym, anc, zh = m.group(1), m.group(2), m.group(3).strip(), m.group(4)
                core = re.sub(r'[()\-]', '', a).lower()
                # 2026-11：关联词要比本词简单——总表里它自己是“前缀 + 这个词根”的词（introduce = intro + duce），就不比本词简单
                sp = split_of.get(anc, '')
                if len(anc) >= len(str(r[wi])) and typ_of.get(anc, '').startswith('①') and ' + ' in sp and not re.match(r'^' + re.escape(core[:3]), sp.split(' + ')[0].strip('-').lower()) and any(core[:3] == re.sub(r'\(.*', '', x).strip('-').lower()[:3] for x in sp.split(' + ')[1:]):
                    hard += 1; print('关联词不比本词简单（它自己是“前缀 + 这个词根”，也不比本词短）：', r[wi], '%s %s %s' % (a, sym, anc))
                x = root_of(ln[:m.start()])
                if x and core != x:
                    notroot += 1; print('变体行的记法没写词根本身：', r[wi], '%s %s %s，应写 %s' % (a, sym, anc, x))
                if sym == '≈' and shift_for(anc, zh, core) and '音变：' not in m.group(5):
                    noshift += 1; print('≈ 两边写法差得多，却没写音变：', r[wi], '%s ≈ %s' % (a, anc))
    print('记法行 %d，写法不对 %d，关联词不比本词简单 %d，变体行没写词根本身 %d，该写音变没写 %d' % (n, bad, hard, notroot, noshift))

def col_letter(i):
    s = ''; i += 1
    while i: i, k = divmod(i - 1, 26); s = chr(65 + k) + s
    return s

def write(src, dst, changes):
    z = zipfile.ZipFile(src); names = [x.filename for x in z.infolist()]; mem = {n: z.read(n) for n in names}; z.close()
    SH = 'xl/worksheets/sheet1.xml'; SST = 'xl/sharedStrings.xml'
    sh = mem[SH].decode('utf-8'); sst = mem[SST].decode('utf-8')
    sis = re.findall(r'<si>(.*?)</si>', sst, re.S)
    head = sst[:sst.index('<si>')]; tail = sst[sst.rindex('</si>') + 5:]
    cell_rx = re.compile(r'<c r="([A-Z]+[0-9]+)"([^>]*?)>(.*?)</c>', re.S)
    refs = collections.Counter(int(v) for a, inner in ((m.group(2), m.group(3)) for m in cell_rx.finditer(sh)) if 't="s"' in a for v in re.findall(r'<v>(\d+)</v>', inner))
    want = {'%s%d' % (col_letter(c), rn): txt for (rn, c), txt in changes.items()}
    esc = lambda s: html.escape(s, quote=False)
    done = 0
    def rep(m):
        nonlocal done
        ref = m.group(1)
        if ref not in want or 't="s"' not in m.group(2): return m.group(0)
        k = int(re.search(r'<v>(\d+)</v>', m.group(3)).group(1))
        si = '<t xml:space="preserve">%s</t>' % esc(want[ref])
        done += 1
        if refs[k] == 1:
            sis[k] = si; return m.group(0)
        sis.append(si)
        return '<c r="%s"%s><v>%d</v></c>' % (ref, m.group(2), len(sis) - 1)
    sh = cell_rx.sub(rep, sh)
    assert done == len(want), (done, len(want))
    head = re.sub(r'uniqueCount="\d+"', 'uniqueCount="%d"' % len(sis), head)
    mem[SH] = sh.encode('utf-8'); mem[SST] = (head + ''.join('<si>%s</si>' % x for x in sis) + tail).encode('utf-8')
    deflate = None
    try:
        import zopfli
        for mk in (lambda: zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE, iterations=1),
                   lambda: zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE, numiterations=1),
                   lambda: zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE)):
            try:
                c = mk(); o = c.compress(b'abcabcabc') + c.flush()
                if zlib.decompress(o, -15) == b'abcabcabc':
                    deflate = (lambda m: (lambda b: (lambda c: c.compress(b) + c.flush())(m())))(mk); break
            except Exception:
                pass
        if deflate is None:
            import zopfli.zlib as zz
            try:
                zz.compress(b'abc', numiterations=1); deflate = lambda b: zz.compress(b, numiterations=1)[2:-4]
            except TypeError:
                deflate = lambda b: zz.compress(b)[2:-4]
            assert zlib.decompress(deflate(b'abcabcabc'), -15) == b'abcabcabc'
    except Exception as e:
        print('没有 zopfli（pip install zopfli），用 zlib9：', e)
    og = zipfile._get_compressor
    class ZC:
        def __init__(s): s.b = []
        def compress(s, d): s.b.append(d); return b''
        def flush(s): return deflate(b''.join(s.b))
    if deflate: zipfile._get_compressor = lambda ct, cl=None: ZC() if ct == zipfile.ZIP_DEFLATED else og(ct, cl)
    try:
        with zipfile.ZipFile(dst, 'w') as zo:
            for n in names:
                zi = zipfile.ZipInfo(n, date_time=(2026, 11, 8, 12, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
                zo.writestr(zi, mem[n], compresslevel=None if deflate else 9)
    finally:
        zipfile._get_compressor = og
    print('写好了 %s（%d 格；%s 压缩）%d 字节' % (dst, done, 'zopfli' if deflate else 'zlib9', os.path.getsize(dst)))
    # 2026-11 词缀身份辨析轮起不再出 LZMA 传输包（Windows 自带的解压打不开）；要压缩包用 xlsx_write.pack_zip(dst)（标准 zip）
    return dst

if __name__ == '__main__':
    p = sys.argv[1]
    if '--check' in sys.argv: check(p)
    elif '--write' in sys.argv:
        ch = dry(p); write(p, sys.argv[sys.argv.index('--write') + 1], ch)
    else: dry(p)

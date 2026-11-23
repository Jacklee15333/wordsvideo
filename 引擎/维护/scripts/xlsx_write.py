# -*- coding: utf-8 -*-
"""把改动写进 xlsx，出 zopfli 压缩的 xlsx（没装 zopfli 就用 zlib 9 级）。pack=True 再出一个标准 zip（pack_zip；默认不出，直接发 xlsx）。两种用法：
  write(src, dst, changes)：只改了几列文字的——直接改共享字符串（别的格、格式、冻结、筛选都不动），改过的行重估行高。
      changes：{(Excel 行号, 列下标 0 起): 新文字}。原来没有的格（空着的“词根变体处理”）会补一格，样式照同一行的“音变”列。
  rebuild(src, dst, table, new_cols)：改动很多、或者要加一列的（2026-11 辨析列轮起）——照内存里的整张表重写工作表和共享字符串：
      table 是 [表头行, 数据行…]（每行一个 list，文字列放 str，没有内容放 None）；new_cols = {新列下标: (列宽, 样式照哪一列的原下标)}。
      每一格的样式照原表同一格（新列照指定的那一列），列宽、冻结窗格、筛选范围跟着改；共享字符串按列再按行排（同一列的内容挨在一起好压）；
      行高：文字没变的行不动，变了的重估。批次、序号、组号这些数字格原样留着。"""
import re, os, sys, zipfile, zlib, html, math, collections

def col_letter(i):
    s = ''; i += 1
    while i: i, k = divmod(i - 1, 26); s = chr(65 + k) + s
    return s
def col_index(L):
    n = 0
    for ch in L: n = n * 26 + ord(ch) - 64
    return n - 1
WIDTH = {5: 36, 6: 11.5, 7: 20.5, 8: 30, 9: 44, 10: 44, 11: 44, 12: 99.75, 13: 48, 14: 55, 15: 26}     # 16 列老表；write() 会先照表里的 <cols> 改
def read_widths(sh):
    """工作表 xml 里的列宽 → {列下标: 宽}（只要第 6 列「含义」以后的文字列）"""
    out = {}
    for m in re.finditer(r'<col min="(\d+)" max="(\d+)" width="([\d.]+)"', sh):
        a, b, w = int(m.group(1)), int(m.group(2)), float(m.group(3))
        if b - a > 50: continue
        for c in range(a, b + 1):
            if c - 1 >= 5: out[c - 1] = w
    return out
dw = lambda s: sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)
def fit(texts, width=None):
    best = 1
    for c, w in (width or WIDTH).items():
        v = str(texts.get(c) or '')
        best = max(best, sum(max(1, math.ceil(dw(l) / (w - 1.5))) for l in v.split('\n')))
    return round(min(409, best * 17.25), 2)

def write(src, dst, changes, pack=False):
    z = zipfile.ZipFile(src); names = [x.filename for x in z.infolist()]; mem = {n: z.read(n) for n in names}; z.close()
    SH = 'xl/worksheets/sheet1.xml'; SST = 'xl/sharedStrings.xml'
    sh = mem[SH].decode('utf-8'); sst = mem[SST].decode('utf-8')
    W = read_widths(sh) or WIDTH
    snd = max((c for c in W), default=14) - 1          # 「音变」列（最后一列「词根变体处理」前面那一列）：补空格时照它的样式
    sis = re.findall(r'<si>(.*?)</si>', sst, re.S)
    head = sst[:sst.index('<si>')]; tail = sst[sst.rindex('</si>') + 5:]
    unesc = lambda s: html.unescape(re.sub(r'<[^>]+>', '', s))
    esc = lambda s: html.escape(s, quote=False)
    cell_rx = re.compile(r'<c r="([A-Z]+)(\d+)"([^>]*?)(?:/>|>(.*?)</c>)', re.S)
    refs = collections.Counter(int(v) for m in cell_rx.finditer(sh) if 't="s"' in m.group(3) for v in re.findall(r'<v>(\d+)</v>', m.group(4) or ''))
    by_row = collections.defaultdict(dict)
    for (rn, c), t in changes.items(): by_row[rn][c] = t
    done = 0
    def new_si(txt):
        sis.append('<t xml:space="preserve">%s</t>' % esc(txt)); return len(sis) - 1
    def do_row(m):
        nonlocal done
        rn = int(m.group(1))
        if rn not in by_row: return m.group(0)
        attrs, body = m.group(2), m.group(3)
        want = dict(by_row[rn]); texts = {}; old_texts = {}; style_o = ''
        cells = []
        for cm in cell_rx.finditer(body):
            ci = col_index(cm.group(1)); a = cm.group(3); inner = cm.group(4) or ''
            val = None
            if 't="s"' in a:
                mv = re.search(r'<v>(\d+)</v>', inner)
                if mv: val = unesc(sis[int(mv.group(1))])
            old_texts[ci] = val
            if ci == snd: style_o = (re.search(r's="(\d+)"', a) or [None, ''])[1]
            if ci in want:
                txt = want.pop(ci); done += 1
                mv = re.search(r'<v>(\d+)</v>', inner) if 't="s"' in a else None
                if mv and refs[int(mv.group(1))] == 1:
                    sis[int(mv.group(1))] = '<t xml:space="preserve">%s</t>' % esc(txt); cells.append(cm.group(0))
                else:
                    if mv: refs[int(mv.group(1))] -= 1
                    a2 = re.sub(r'\s*t="[^"]*"', '', a) + ' t="s"'
                    cells.append('<c r="%s%d"%s><v>%d</v></c>' % (cm.group(1), rn, a2, new_si(txt)))
                texts[ci] = txt
            else:
                cells.append(cm.group(0)); texts[ci] = val
        for ci, txt in sorted(want.items()):                      # 原来没有这一格：补上
            done += 1; texts[ci] = txt
            cell = '<c r="%s%d"%s t="s"><v>%d</v></c>' % (col_letter(ci), rn, (' s="%s"' % style_o) if style_o else '', new_si(txt))
            pos = len(cells)
            for k, cxml in enumerate(cells):
                if col_index(re.match(r'<c r="([A-Z]+)', cxml).group(1)) > ci: pos = k; break
            cells.insert(pos, cell)
        mh = re.search(r'\sht="([\d.]+)"', attrs)
        old_ht = float(mh.group(1)) if mh else None
        nh = fit(texts, W)
        if old_ht is not None and abs(old_ht - fit(old_texts, W)) > 1.0: nh = max(old_ht, nh)      # 原来不是按字数估的行高：只加不减
        if mh: attrs = attrs.replace(mh.group(0), ' ht="%s"' % ('%g' % nh))
        else: attrs += ' ht="%g" customHeight="1"' % nh
        return '<row r="%d"%s>%s</row>' % (rn, attrs, ''.join(cells))
    sh = re.sub(r'<row r="(\d+)"([^>]*)>(.*?)</row>', do_row, sh, flags=re.S)
    assert done == len(changes), (done, len(changes))
    head = re.sub(r'uniqueCount="\d+"', 'uniqueCount="%d"' % len(sis), head)
    mem[SH] = sh.encode('utf-8'); mem[SST] = (head + ''.join('<si>%s</si>' % x for x in sis) + tail).encode('utf-8')
    _save(dst, names, mem, pack, done)


def _save(dst, names, mem, pack=False, done=None):
    """mem（{包里的文件名: 内容}）→ zopfli 压缩的 xlsx（没装 zopfli：zlib 9 级）；pack=True 再出一个标准 zip"""
    try:
        import zopfli
    except ImportError:
        with zipfile.ZipFile(dst, 'w') as zo:
            for n in names:
                zi = zipfile.ZipInfo(n, date_time=(2026, 11, 10, 12, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zo.writestr(zi, mem[n], compresslevel=9)
        print('写好了 %s%s %d 字节（没有 zopfli，用 zlib 9 级：pip install zopfli 能再小一点）' % (dst, '（%d 格）' % done if done is not None else '', os.path.getsize(dst)))
        if pack: pack_zip(dst)
        return
    def deflate(b):
        for mk in (lambda: zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE, iterations=1), lambda: zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE, numiterations=1), lambda: zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE)):
            try:
                c = mk(); o = c.compress(b) + c.flush()
                if zlib.decompress(o, -15) == b: return o
            except Exception: pass
        import zopfli.zlib as zz
        o = zz.compress(b)[2:-4]; assert zlib.decompress(o, -15) == b; return o
    og = zipfile._get_compressor
    class ZC:
        def __init__(s): s.b = []
        def compress(s, d): s.b.append(d); return b''
        def flush(s): return deflate(b''.join(s.b))
    zipfile._get_compressor = lambda ct, cl=None: ZC() if ct == zipfile.ZIP_DEFLATED else og(ct, cl)
    try:
        with zipfile.ZipFile(dst, 'w') as zo:
            for n in names:
                zi = zipfile.ZipInfo(n, date_time=(2026, 11, 10, 12, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; zo.writestr(zi, mem[n])
    finally:
        zipfile._get_compressor = og
    print('写好了 %s%s %d 字节' % (dst, '（%d 格）' % done if done is not None else '', os.path.getsize(dst)))
    if pack: pack_zip(dst)


def pack_zip(xlsx):
    """另出一个标准 zip（deflate 压缩，Windows、macOS 自带的解压双击就能打开）。
    2026-11 词缀身份辨析轮起（第 88 条）：以前的“传输包”外层用 LZMA，Windows 自带的解压不认（用户：“压缩包我的电脑好像打不开”），不再出。
    xlsx 本身已经是压缩过的，标准 zip 小不了多少（和 xlsx 差不多大）——平时直接发 xlsx，用户要压缩包时才调它"""
    packp = re.sub(r'\.xlsx$', '', xlsx) + '_压缩包.zip'
    with zipfile.ZipFile(packp, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zo: zo.write(xlsx, arcname=os.path.basename(xlsx))
    with zipfile.ZipFile(packp) as zp:
        assert zp.testzip() is None and zp.read(os.path.basename(xlsx)) == open(xlsx, 'rb').read()
        assert all(i.compress_type in (zipfile.ZIP_DEFLATED, zipfile.ZIP_STORED) for i in zp.infolist())
    print('压缩包（标准 zip）%s %d 字节' % (packp, os.path.getsize(packp)))
    return packp


def rebuild(src, dst, table, new_cols=None, pack=False):
    """照内存里的整张表重写（见文件开头）。table[0] 是表头；new_cols = {新列下标: (列宽, 样式照哪一列的原下标)}"""
    new_cols = new_cols or {}
    z = zipfile.ZipFile(src); names = [x.filename for x in z.infolist()]; mem = {n: z.read(n) for n in names}; z.close()
    SH = 'xl/worksheets/sheet1.xml'; SST = 'xl/sharedStrings.xml'; WB = 'xl/workbook.xml'
    sh = mem[SH].decode('utf-8'); sst = mem[SST].decode('utf-8')
    sis = re.findall(r'<si>(.*?)</si>', sst, re.S)
    unesc = lambda t: html.unescape(re.sub(r'<[^>]+>', '', t))
    esc = lambda t: html.escape(t, quote=False)
    NC = len(table[0])
    # 新列下标 → 原列下标（新加的列是 None）
    omap, k = [], 0
    for j in range(NC):
        if j in new_cols: omap.append(None)
        else: omap.append(k); k += 1
    NO = k
    # 原表每一行：属性、每一格（样式、是不是文字、原文）
    row_rx = re.compile(r'<row r="(\d+)"([^>]*)>(.*?)</row>', re.S)
    cell_rx = re.compile(r'<c r="([A-Z]+)(\d+)"([^>]*?)(?:/>|>(.*?)</c>)', re.S)
    orig = {}
    for m in row_rx.finditer(sh):
        rn = int(m.group(1)); cells = {}
        for cm in cell_rx.finditer(m.group(3)):
            ci = col_index(cm.group(1)); a = cm.group(3); inner = cm.group(4) or ''
            st = (re.search(r'\ss="(\d+)"', a) or [None, ''])[1]
            val = None; raw = None
            if 't="s"' in a:
                mv = re.search(r'<v>(\d+)</v>', inner)
                if mv: val = unesc(sis[int(mv.group(1))])
            elif inner: raw = (a, inner)
            cells[ci] = (st, val, raw)
        orig[rn] = (m.group(2), cells)
    assert len(orig) == len(table), (len(orig), len(table))
    # 列宽
    Wo = {}
    for m in re.finditer(r'<col min="(\d+)" max="(\d+)" width="([\d.]+)"([^>]*)/>', sh):
        a, b, w = int(m.group(1)), int(m.group(2)), float(m.group(3))
        if b - a > 50: continue
        for c in range(a, b + 1): Wo[c - 1] = w
    Wn = {j: (new_cols[j][0] if omap[j] is None else Wo.get(omap[j], 8.54)) for j in range(NC)}
    Wn_txt = {j: w for j, w in Wn.items() if j >= 5}
    Wo_txt = {j: w for j, w in Wo.items() if j >= 5}
    # 共享字符串：按列、再按行排
    order = {}
    for j in range(NC):
        for rn in range(1, len(table) + 1):
            v = table[rn - 1][j]
            if isinstance(v, str) and v != '' and v not in order: order[v] = len(order)
    out_rows = []; changed = 0
    for rn in range(1, len(table) + 1):
        attrs, cells = orig[rn]
        row = table[rn - 1]; xml = []; new_txt = {}; old_txt = {}
        for j in range(NC):
            oj = omap[j]
            st, oval, raw = cells.get(oj, (None, None, None)) if oj is not None else (None, None, None)
            if oj is None:
                st = cells.get(new_cols[j][1], (None, None, None))[0]
            elif st is None and row[j] not in (None, ''):          # 原来没有这一格、现在有字：样式照左边最近的一格
                for jj in range(oj - 1, -1, -1):
                    if jj in cells and cells[jj][0]: st = cells[jj][0]; break
            sa = ' s="%s"' % st if st else ''
            ref = '%s%d' % (col_letter(j), rn)
            v = row[j]
            if oj is not None: old_txt[oj] = oval
            if raw is not None and oj is not None and (v is None or not isinstance(v, str)):
                xml.append('<c r="%s"%s>%s</c>' % (ref, re.sub(r'\s*r="[^"]*"', '', raw[0]) if False else raw[0], raw[1]))   # 数字格原样
                continue
            if isinstance(v, str) and v != '':
                xml.append('<c r="%s"%s t="s"><v>%d</v></c>' % (ref, sa, order[v])); new_txt[j] = v
            elif oj is not None and oj in cells or oj is None and st:
                xml.append('<c r="%s"%s/>' % (ref, sa))
        # 行高
        mh = re.search(r'\sht="([\d.]+)"', attrs)
        old_ht = float(mh.group(1)) if mh else None
        same = all((new_txt.get(j) or None) == (old_txt.get(omap[j]) or None) for j in range(NC) if omap[j] is not None) and not any(new_txt.get(j) for j in new_cols)
        a2 = re.sub(r'\sspans="[^"]*"', ' spans="1:%d"' % NC, attrs)
        if not same and rn > 1:
            changed += 1
            nh = fit(new_txt, Wn_txt)
            if old_ht is not None and abs(old_ht - fit(old_txt, Wo_txt)) > 1.0: nh = max(old_ht, nh)
            if mh: a2 = a2.replace(mh.group(0), ' ht="%g"' % nh)
            else: a2 += ' ht="%g" customHeight="1"' % nh
        out_rows.append('<row r="%d"%s>%s</row>' % (rn, a2, ''.join(xml)))
    last = col_letter(NC - 1); NR = len(table)
    i0 = sh.index('<sheetData>'); i1 = sh.index('</sheetData>')
    head, tail = sh[:i0], sh[i1 + len('</sheetData>'):]
    head = re.sub(r'<dimension ref="[^"]*"/>', '<dimension ref="A1:%s%d"/>' % (last, NR), head)
    # 列宽重写
    mc = re.search(r'<cols>(.*?)</cols>', head, re.S)
    if mc:
        style = (re.search(r'style="(\d+)"', mc.group(1)) or [None, '1'])[1]
        cols = ''.join('<col min="%d" max="%d" width="%s" style="%s" customWidth="1"/>' % (j + 1, j + 1, ('%.10g' % Wn[j]), style) for j in range(NC))
        mrest = re.search(r'<col min="\d+" max="16384"[^>]*/>', mc.group(1))
        if mrest: cols += re.sub(r'min="\d+"', 'min="%d"' % (NC + 1), mrest.group(0))
        head = head[:mc.start()] + '<cols>' + cols + '</cols>' + head[mc.end():]
    # 冻结窗格留着，光标回到左上角
    head = re.sub(r'topLeftCell="[A-Z]+\d+"', 'topLeftCell="G2"', head)
    head = re.sub(r'<selection pane="bottomRight"[^>]*/>', '<selection pane="bottomRight" activeCell="G2" sqref="G2"/>', head)
    tail = re.sub(r'(<autoFilter ref=")[^"]*(")', r'\g<1>A1:%s%d\g<2>' % (last, NR), tail)
    mem[SH] = (head + '<sheetData>' + ''.join(out_rows) + '</sheetData>' + tail).encode('utf-8')
    sst_head = re.sub(r'count="\d+"', 'count="%d"' % sum(1 for r in table for v in r if isinstance(v, str) and v != ''), sst[:sst.index('<si>')])
    sst_head = re.sub(r'uniqueCount="\d+"', 'uniqueCount="%d"' % len(order), sst_head)
    mem[SST] = (sst_head + ''.join('<si><t xml:space="preserve">%s</t></si>' % esc(v) for v in order) + sst[sst.rindex('</si>') + 5:]).encode('utf-8')
    wb = mem[WB].decode('utf-8')
    wb = re.sub(r'(_xlnm\._FilterDatabase"[^>]*>[^<!]*!\$A\$1:\$)[A-Z]+(\$)\d+', r'\g<1>%s\g<2>%d' % (last, NR), wb)
    mem[WB] = wb.encode('utf-8')
    print('重写：%d 行 × %d 列，文字变了的 %d 行，共享字符串 %d 条' % (NR, NC, changed, len(order)))
    _save(dst, names, mem, pack)

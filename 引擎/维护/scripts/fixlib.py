"""直接修改「拆分结果」的小工具（改拆分、改某一行解释、补丢字），2026-11 起各部分解释是前缀、词根、单词部分、后缀四列（见 cols.py）。每处改动自动：
  - 在 U 列“本次调整”追加一句“<标记>：…”
  - 记进「整表核对记录」（没有这张表就新建；有就接着往下编号）
  - 按需加高行高
不插行、不删行，所以「整表核对记录」的超链接不受影响。整类的批量修改用 fixed_other 记一条汇总。

用法（写一个小脚本）：
    import sys; sys.path.insert(0, '<技能目录>/scripts')
    from fixlib import Book
    b = Book(SRC)                                   # 默认标记“整表核对”
    b.set_split('chopsticks', 'chopstick + s', '母词 chopstick 在表里', typ='① 词根词缀')
    b.replace_line('firecracker', 'cracker：', 'crack：…\\n-er：…', '解释少一行')
    b.replace_text('beggar', 'beg：）', 'beg：乞讨、乞求）', '丢字')                 # 不写 col：在前缀、词根、单词部分、后缀四列里找
    b.set_logic('improvise', '【构词逻辑】im（不）+ …')   # 只换 I 列第一行，不单独记录
    b.special('aware', 'ware 和第 813 组 ware 不是一个词', '不移动')   # 只记录，不改表
    b.save(OUT)
"""
import re, copy, math
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter

COLS = {c: i for i, c in enumerate('ABCDEFGHIJKLMNOPQRSTUV', 1)}   # 2026-11 单词列轮起 22 列：H 类型、I 拆分、J 前缀、K 词根、L 单词部分、M 后缀、N 组合、U 本次调整
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import cols as C

class Book:
    def __init__(self, src, tag='整表核对'):
        self.wb = load_workbook(src); self.ws = self.wb['拆分结果']; self.tag = tag
        self.row = {}
        for r in range(2, self.ws.max_row + 1):
            self.row.setdefault(str(self.ws.cell(r, 5).value), r)
        self.log = []

    def r(self, word, nth=1):
        """取单词所在行；同形词（bore、lie…）用 nth=2 取第二行。"""
        rows = [r for r in range(2, self.ws.max_row + 1) if str(self.ws.cell(r, 5).value) == word]
        assert len(rows) >= nth, f'表里找不到第 {nth} 个 {word}'
        return rows[nth - 1]

    def note(self, r, txt):
        c = self.ws.cell(r, C.ADJ); c.value = (c.value + '；' if c.value else '') + f'{self.tag}：{txt}'

    def set_split(self, word, new, why, typ=None, nth=1):
        r = self.r(word, nth); old = self.ws.cell(r, 9).value; self.ws.cell(r, 9).value = new
        if typ: self.ws.cell(r, 8).value = typ
        self.note(r, f'拆分 {old} → {new}（{why}）')
        self.log.append(('已修正', r, word, f'拆分写成 {old}，{why}', f'拆分改为 {new}' + (f'，类型改为 {typ}' if typ else '')))

    def replace_line(self, word, label_start, new, why, nth=1):
        """把各部分解释（前缀、词根、单词部分、后缀四列）里以 label_start 开头的那一行换成 new（new 里可用 \\n 变成多行）；改完分回四列（原来在哪列还在哪列）。"""
        r = self.r(word, nth); L = C.get_parts(self.ws, r).split('\n')        # 前缀、词根、单词部分、后缀四列合起来找
        k = [i for i, l in enumerate(L) if l.startswith(label_start)]
        assert k, f'{word} 的解释里没有以 {label_start} 开头的行'
        L[k[0]] = new; C.set_parts(self.ws, r, '\n'.join(L))
        self.note(r, why); self.log.append(('已修正', r, word, why, f'改写“{label_start}”这一行'))

    def replace_text(self, word, old, new, why, col=None, nth=1, log=True):
        """col 不写：在前缀、词根、单词部分、后缀四列里找（以前的各部分解释）；写列字母就只在那一列找"""
        r = self.r(word, nth)
        if col is None:
            col = next((L for L in 'JKLM' if old in str(self.ws.cell(r, COLS[L]).value or '')), 'K')
        c = self.ws.cell(r, COLS[col]); v = str(c.value)
        assert old in v, f'{word} 的 {col} 列里没有：{old}'
        c.value = v.replace(old, new, 1)
        if log: self.note(r, why); self.log.append(('已修正', r, word, why, f'{col} 列：{old} → {new}'))

    def set_logic(self, word, first_line, nth=1):
        r = self.r(word, nth); L = str(self.ws.cell(r, C.COMBO).value).split('\n'); L[0] = first_line
        self.ws.cell(r, C.COMBO).value = '\n'.join(L)

    def special(self, word, what, how='保留', nth=1):
        self.log.append(('特殊（未改）', self.r(word, nth) if word else None, word or '—', what, how))

    def fixed_other(self, label, what, how):
        """记录不在「拆分结果」里的改动（如其他 sheet）。"""
        self.log.append(('已修正', None, label, what, how))

    def _fit(self, r):
        ws = self.ws; W = {}
        # 列宽要按 min..max 范围取：openpyxl 读进来的列宽常是一段一段的（K–M 共用一条），直接取 column_dimensions['L'] 会得到默认宽 13，行高算得过高（2026-11 字母变化同源词轮改）
        for d in ws.column_dimensions.values():
            for i in range(d.min or 0, (d.max or 0) + 1):
                if i: W[get_column_letter(i)] = d.width
        W = {c: W.get(c) or 10 for c in C.TEXT_COLS}
        dw = lambda s: sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)
        best = max(sum(max(1, math.ceil(dw(l) / (W[c] - 1.5))) for l in str(ws[f'{c}{r}'].value or '').split('\n')) for c in C.TEXT_COLS)
        need = round(best * 17.25, 2)
        need = min(need, 409)                                          # Excel 行高上限 409 磅
        if (ws.row_dimensions[r].height or 0) < need: ws.row_dimensions[r].height = need

    def _write_log(self):
        wb = self.wb
        if '整表核对记录' not in wb.sheetnames:
            R = wb.create_sheet('整表核对记录', index=wb.sheetnames.index('说明') if '说明' in wb.sheetnames else None)
            ref = wb['补充说明记录'] if '补充说明记录' in wb.sheetnames else self.ws
            for c, h in enumerate(['序', '类别', '所在行', '单词', '发现的情况', '处理'], 1):
                R.cell(1, c).value = h; R.cell(1, c)._style = copy.copy(ref.cell(1, 1)._style)
            for col, w in zip('ABCDEF', (6, 12, 12, 18, 60, 48)): R.column_dimensions[col].width = w
            R.freeze_panes = 'A2'
        R = wb['整表核对记录']
        n0 = sum(1 for r in R.iter_rows(min_row=2, values_only=True) if r[0] is not None)
        body = copy.copy(R.cell(2, 4)._style) if R.max_row >= 2 else None
        for k, (cat, r, w, what, how) in enumerate(self.log):
            i = n0 + k + 2
            vals = [n0 + k + 1, cat, f'=HYPERLINK("#\'拆分结果\'!E{r}","第 {r} 行")' if r else '—', w, what, how]
            for c, v in enumerate(vals, 1):
                cell = R.cell(i, c); cell.value = v
                if body: cell._style = copy.copy(body)
                cell.alignment = Alignment(wrap_text=True, vertical='top')
            if r: R.cell(i, 3).font = Font(name='微软雅黑', size=10, color='0563C1', underline='single')
            R.cell(i, 2).fill = PatternFill('solid', start_color='E2EFDA' if cat == '已修正' else 'FFF2CC')
            R.row_dimensions[i].height = 17.25 * max(1, math.ceil(max(len(what), len(how)) / 38))
        R.auto_filter.ref = f'A1:F{R.max_row}'

    def save(self, out):
        for _, r, *_ in self.log:
            if r: self._fit(r)
        if self.log: self._write_log()
        self.wb.save(out)
        print('记录', len(self.log), '条，其中已修正', sum(1 for x in self.log if x[0] == '已修正'))

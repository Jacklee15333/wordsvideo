# -*- coding: utf-8 -*-
"""同一个词根体检（2026-11 同一个词根轮，project_rules.md 第 60–63 条）。按列名读表，16 列的精简表、22 列的全表都能跑。
  python3 tonggen_check.py <表.xlsx> [每类列几条]
各项都应为 0（“记法待补”只是报个数）：
  left_old     词根列还写“由词根 X 变来”（把一个词根的几种写法讲成了几个词根）；genuine 词典有两说，不算
  no_change    写了“词根 X 的另一种写法”，后面却没有“字母变化：X → …”（字母怎么变的要在本行讲清，不能“见 别的词”）
  chain_bad    “字母变化”那条链不是从这个词根写起
  split_eq     这一部分是词根的另一种写法，拆分里却没写成 Y(=X)
  see_derived  词根那一行指到同组别的派生词（“见 reduce”）：词根的意思、来源就在本行说，不让学生去看更复杂的词
               （指到简单的基础词、变体词 people / two，过去分词词干指到母词 compete，不算）
  old_rule     组合列里还有取消了的空洞说法（“一个词用进某一行…”“同一个词，英国、美国…”“东西变了，旧名字还接着用”）
  记法待补      「词根变体处理」列标了“记法待补”的行数（找不到比本词更简单的关联词，先不写记法）"""
import re, sys, collections
from openpyxl import load_workbook
KEEP_OLD = {'genuine'}
KEEP_SPLIT = {'stationery', 'carnival'}          # stationer 是一整个派生出来的词干、levare 是拉丁语动词原样：拆分不写 (=词根)
VAR = re.compile(r'^([^：]{1,40})：词根\s*([A-Za-z]+)\s*的另一种写法(（[^（）]*(?:（[^（）]*）[^（）]*)*）)?')
OLD_RULES = ('一个词用进某一行', '同一个词，英国、美国', '东西变了，旧名字还接着用')
DONGBIAN = re.compile(r'动词变化：[^。\n]*?；规律：[^。\n]*?(?:。|(?=；记：)|$)')      # 和 cols.py 的 DONGBIAN 同一个写法（这个脚本不 import cols，16 列的表也能单独跑）
core = lambda lab: re.sub(r'[（(][^（）()]*[）)]', '', lab).strip().strip('-').lower()

def main(path, show=8):
    wb = load_workbook(path, read_only=True); ws = wb['拆分结果'] if '拆分结果' in wb.sheetnames else wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True)); hdr = [str(h or '') for h in rows[0]]; rows = rows[1:]
    col = lambda name: next(i for i, h in enumerate(hdr) if h.startswith(name))
    W, G, T, S, R, C = col('单词'), col('组号'), col('类型'), col('拆分'), col('词根'), col('组合')
    P = next((i for i, h in enumerate(hdr) if h.startswith('词根变体处理')), None)
    grp = collections.defaultdict(set); typ = {}
    for r in rows: grp[str(r[W])].add(r[G]); typ[str(r[W])] = str(r[T] or '')[:1]
    out = collections.defaultdict(list); pend = 0
    for n, r in enumerate(rows, start=2):
        w = str(r[W])
        if P is not None and r[P] and '记法待补' in str(r[P]): pend += 1
        for l in str(r[C] or '').split('\n'):
            if l.startswith('\u3000用词规律：') and l[6:].startswith(OLD_RULES): out['old_rule'].append((n, w, l[:60]))
        v = str(r[R] or '')
        if v.strip() in ('', '-', '—'): continue
        for line in v.split('\n'):
            line = DONGBIAN.sub('', line)          # 2026-11 拉丁语动词变化轮：“动词变化：…；规律：…。”讲的是整个动词，不算这一行自己的话
            if '由词根' in line and '变来' in line and w not in KEEP_OLD: out['left_old'].append((n, w, line[:70]))
            m = VAR.match(line)
            if m:
                lab, X, note = m.group(1), m.group(2), m.group(3) or ''
                mc = re.search(r'字母变化：\s*([A-Za-z*é]+)\s*→', line)
                if not mc: out['no_change'].append((n, w, line[:70]))
                elif mc.group(1).lower() != X.lower() and not (X.lower().startswith(mc.group(1).lower()) and '准确说' in note): out['chain_bad'].append((n, w, line[:70]))
                Y = core(lab); sp = str(r[S] or '').split('；')[0]
                parts = [p.strip() for p in re.split(r'\s\+\s', sp)]
                bare = [p for p in parts if p.strip('-').lower() == Y]
                if Y != X.lower() and bare and w not in KEEP_SPLIT and '准确说' not in note and not re.search(r'过去分词', line.split('意思')[0]): out['split_eq'].append((n, w, sp))
            if '过去分词' in line: continue
            for ms in re.finditer(r'[（，；]\s*见 ?([A-Za-z][A-Za-z\-]*)(?: 的【[^】]*】)?', line):
                Wd = ms.group(1)
                if re.search(r'(英式|美式)写 ?[A-Za-z\-]+$', line[:ms.start()]): continue        # “英式写 analyse（见 analyse）”：另一种拼法指到主拼法，照旧
                if r[G] in grp.get(Wd, ()) and typ.get(Wd) in ('①', '③'): out['see_derived'].append((n, w, line[max(0, ms.start() - 16):ms.end() + 4]))
    total = 0
    for k in ('left_old', 'no_change', 'chain_bad', 'split_eq', 'see_derived', 'old_rule'):
        v = out[k]; total += len(v)
        print('%-12s %d' % (k, len(v)))
        for it in v[:show]: print('    ', it)
    print('记法待补      %d 行' % pend)
    print('合计 %d' % total)
    return total

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8)

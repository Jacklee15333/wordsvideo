"""Print to-do items START..END of sheet 词根变体待处理 with each group's 背景 and the lines
of 各部分解释 whose label is one of the listed root forms.
Usage: python3 show_items.py <xlsx> <start> <end>"""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from openpyxl import load_workbook
from parse import parse_split
xlsx, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
wb = load_workbook(xlsx, read_only=True)
X = list(wb['词根变体待处理'].iter_rows(min_row=2, values_only=True))
T = list(wb['拆分结果'].iter_rows(min_row=2, values_only=True))
for item in X:
    k, g, w0, link, forms, wl, st = item[:7]
    if not (a <= k <= b): continue
    forms = str(forms).split('、')
    rows = [(i, x) for i, x in enumerate(T, start=2) if x[2] == g]
    print(f'######## 项{k} 组{g} 状态={st} 写法={forms}')
    bg = [x[9] for i, x in rows if x[9]]
    if bg: print('  背景:', str(bg[0])[:400])
    for i, x in rows:
        ps = parse_split(str(x[6] or '')) or []
        sf = {p['surface'].lower() for p in ps}
        if not sf & set(forms): continue
        print(f'  {i} {x[4]} = {x[6]}')
        for l in str(x[7]).split('\n'):
            m = re.match(r'^\s*([^：:]{1,40})[：:]', l)
            lab = re.sub(r'\([^)]*\)', '', m.group(1)).strip().strip('-').lower() if m else ''
            if lab in forms: print('      ', l[:170])

"""拆分的每一部分在“各部分解释”里有没有对应行（已滤掉双写辅音、带 ← ≈ 的拆分等常见误报）。用法：python3 audit_split_labels.py <xlsx>"""
import re,sys
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from parse import parse_split
import cols as C
from openpyxl import load_workbook
ws=load_workbook(sys.argv[1],read_only=True)['拆分结果']
T=[C.legacy(x) for x in ws.iter_rows(min_row=2,values_only=True)]   # 前缀、词根、单词部分、后缀合成一格
def norm(l): return re.sub(r'[（(][^）)]*[）)]','',l).strip().strip('-').lower()   # 2026-11 拼写变化轮：全角括号（mat（v.））也去掉
out=[]
for i,x in enumerate(T,start=2):
    s=str(x[8] or '')
    if '←' in s or '≈' in s or '（' in s: continue
    ps=parse_split(s)
    if not ps: continue
    labs=[]
    for l in str(x[9] or '').split('\n'):
        m=re.match(r'^\s*([^：:]{1,40})[：:]',l)
        if m: labs.append(norm(m.group(1)))
    prev=''
    for p in ps:
        sf=p['surface'].lower(); raw=norm(p['raw']); full=re.sub(r'[()]','',p['raw']).lower()
        last=prev; prev=raw or sf
        if sf in labs or raw in labs or full in labs: continue
        # 2026-11 拼写变化轮：双写的字母单独写一部分（forget + t + able、program + m + ing），不要求有解释行
        if len(raw)==1 and raw not in 'aeiou' and last.endswith(raw): continue
        # suffix fragments: r/st/ed/n/l/ten etc. explained under a longer suffix label ending with it
        if any(l.endswith(sf) and len(l)<=len(sf)+3 for l in labs): continue
        out.append((i,x[4],s,p['raw'],'|'.join(labs)))
print(len(out))
for o in out: print(*o)

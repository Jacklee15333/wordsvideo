"""整表核对：python3 audit.py <xlsx>。各项含义和常见误报见 references/audit_checklist.md。"""
import re,sys,collections
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from parse import parse_split
import cols as C   # 2026-11 起各部分解释分成前缀、词根、单词部分、后缀四列：legacy() 合回一格，下面的列号照旧
from openpyxl import load_workbook
F=sys.argv[1]
wb=load_workbook(F,read_only=True); ws=wb['拆分结果']
T=[C.legacy(x) for x in ws.iter_rows(min_row=2,values_only=True)]
R=lambda n:T[n-2]
words=collections.Counter(str(x[4]) for x in T)
wl={w.lower() for w in words}
P=lambda *a:print(*a)
P('总行数',len(T))
# 1 duplicates
d=[w for w,c in words.items() if c>1]; P('\n[1] 重复的词',len(d),d[:30])
# 2 group contiguity & background
seen=set(); prev=None; noncontig=[]
first={}
for i,x in enumerate(T,start=2):
    g=x[2]
    if g!=prev:
        if g in seen: noncontig.append((i,g))
        seen.add(g); first.setdefault(g,i)
    prev=g
P('\n[2a] 组号不连续（同一组被拆散）',len(noncontig),noncontig[:20])
bad=[(i,x[2],x[4]) for i,x in enumerate(T,start=2) if x[11] and '【背景】' in str(x[11]) and first[x[2]]!=i]
P('[2b] 【背景】不在组的第一行',len(bad),bad[:20])
nobg=[g for g,i in first.items() if not (R(i)[11] and '【背景】' in str(R(i)[11]))]
P('[2c] 第一行没有【背景】的组',len(nobg),nobg[:15])
# 3 seq numbers per batch
cnt=collections.Counter(); badseq=[]
for i,x in enumerate(T,start=2):
    cnt[x[0]]+=1
    if str(x[1])!=str(cnt[x[0]]): badseq.append((i,x[0],x[1],cnt[x[0]]))
P('\n[3] 序号不连号',len(badseq),badseq[:10])
# 4 empties
for c,n in [(4,'单词'),(5,'含义'),(7,'类型'),(8,'拆分'),(9,'各部分解释'),(10,'组合→含义')]:   # 2026-11 起 G 列是「例句」，后面的列往后挪一列
    e=[(i,x[4]) for i,x in enumerate(T,start=2) if x[c] in (None,'')]
    P(f'[4] {n} 为空',len(e),e[:10])
P('[4b] 类型分布',collections.Counter(x[7] for x in T))
# 5 split parts vs H labels
def norm(l): return re.sub(r'\([^)]*\)','',l).strip().strip('-').lower()
miss=[]
for i,x in enumerate(T,start=2):
    ps=parse_split(str(x[8] or ''))
    if not ps: continue
    labs=set()
    for l in str(x[9] or '').split('\n'):
        m=re.match(r'^\s*([^：:]{1,40})[：:]',l)
        if m: labs.add(norm(m.group(1)))
    for p in ps:
        s=norm(p['raw'])
        if s and s not in labs and p['surface'].lower() not in labs:
            miss.append((i,x[4],x[8],p['raw']))
P('\n[5] 拆分里的部分在解释里找不到对应行',len(miss)); [P('   ',*m) for m in miss[:40]]
# 6 见 X
see=collections.Counter(); seerows=collections.defaultdict(list)
for i,x in enumerate(T,start=2):
    for c in (9,10,11,12):
        for w in re.findall(r'见 ([A-Za-z][A-Za-z\-\' ]*?)(?:[ ）)，、；的]|$)',str(x[c] or '')):
            w=w.strip()
            if w.lower() not in wl: see[w]+=1; seerows[w].append(i)
P('\n[6] “见 X”指向表里没有的词',len(see)); P('   ',[(w,c,seerows[w][:3]) for w,c in see.most_common(60)])
# 7 brackets
pairs=[('（','）'),('“','”'),('【','】'),('(',')')]
br=[]
for i,x in enumerate(T,start=2):
    for c in (8,9,10,11,12):
        v=str(x[c] or '')
        for a,b in pairs:
            if v.count(a)!=v.count(b): br.append((i,x[4],['I','J–L','M','N','O'][c-8],a+b,v.count(a),v.count(b)))
P('\n[7] 括号/引号不配对',len(br)); [P('   ',*b) for b in br[:60]]
# 8 ascii colon labels
ac=[(i,x[4],l[:40]) for i,x in enumerate(T,start=2) for l in str(x[9] or '').split('\n') if re.match(r'^[A-Za-z()\-]{1,25}:',l)]
P('\n[8] 解释行标签用了半角冒号',len(ac),ac[:15])
# 9 P column 第 N 行 references
refbad=[]
for i,x in enumerate(T,start=2):
    v=str(x[17] or '')
    for n,w in re.findall(r'第 (\d+) 行 ([A-Za-z][A-Za-z\-\']*)',v)+[(n,w) for w,n in re.findall(r'母词 ([A-Za-z][A-Za-z\-\']*) 已补在第 (\d+) 行',v)]:
        n=int(n)
        if not (2<=n<=len(T)+1) or str(R(n)[4])!=w: refbad.append((i,x[4],n,w,R(n)[4] if 2<=n<=len(T)+1 else None))
P('\n[9] 本次调整列里“第 N 行”指错',len(refbad),refbad[:20])
# 10 root consistency in processed rows
rc=[]
for i,x in enumerate(T,start=2):
    q=str(x[18] or ''); m=re.search(r'本组词根 ([A-Za-z]+)',q)
    if not m: continue
    for r in re.findall(r'由词根 ([A-Za-z]+) 变来',str(x[9])):
        if r.lower()!=m.group(1).lower(): rc.append((i,x[4],r,m.group(1)))
P('\n[10] 由词根 X 变来 与本组词根不一致',len(rc),rc[:20])
# 11 I column starts with 构词逻辑
noI=[(i,x[4]) for i,x in enumerate(T,start=2) if x[10] and not str(x[10]).lstrip().startswith('【构词逻辑】')]
P('\n[11] 组合列不以【构词逻辑】开头',len(noI),noI[:15])
# 12 '=' text
eq=[(i,c) for i,x in enumerate(T,start=2) for c,v in enumerate(x) if isinstance(v,str) and v.startswith('=')]
P('[12] 以 = 开头的单元格',len(eq),eq[:5])
# 13 「整表核对记录」的超链接（其他索引表已删）
def chk(name,linkcol,wordcol):
    bad=[]
    for r in wb[name].iter_rows(min_row=2,values_only=True):
        l=str(r[linkcol] or '')
        if not l or l=='—': continue
        m=re.search(r"!E(\d+)\",\"第 (\d+) 行",l)
        if not m:
            bad.append(('无法解析',r[0],l[:40])); continue
        a,b=int(m.group(1)),int(m.group(2))
        w=str(r[wordcol])
        if a!=b or str(R(a)[4])!=w: bad.append((r[0],w,a,b,R(a)[4]))
    P(f'[13] {name} 第{linkcol+1}列链接指错',len(bad),bad[:10])
if '整表核对记录' in wb.sheetnames: chk('整表核对记录',2,3)
P('\n[14] 视频读表的体检另跑：python3 video_check.py <xlsx>（基线见 references/audit_checklist.md）')

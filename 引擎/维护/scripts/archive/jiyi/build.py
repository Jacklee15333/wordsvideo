import pickle, re, math, zipfile, zlib, time, os, sys, shutil
sys.path.insert(0, '/home/claude/work')
from memo_data import D, COMBO
from openpyxl import load_workbook
W='/home/claude/work'; SRC=f'{W}/table/master.xlsx'; NAME='词源拆分总表_不好拆分记忆版'
OUTD=f'{W}/out'; TMP=f'{OUTD}/tmp.xlsx'; FINAL=f'{OUTD}/{NAME}.xlsx'; PACK=f'{OUTD}/{NAME}_传输包.zip'
SIM='\u223d'
osheet=zipfile.ZipFile(SRC).read('xl/worksheets/sheet1.xml')
orig_f=osheet.count(b'<f>')+osheet.count(b'<f ')
print('原表公式数:', orig_f)
data={}
for w,split,typ,memo in D:
    split=split.replace(' ~ ',f' {SIM} '); memo=memo.replace(' ~ ',f' {SIM} ')
    assert '~' not in split+memo, w
    data[w]=(split,typ,memo)
assert len(data)==118
t=time.time(); wb=load_workbook(SRC); ws=wb['拆分结果']; print('读入', round(time.time()-t,1),'秒')
hdr=[c.value for c in ws[1]]
assert hdr[4]=='单词' and hdr[6]=='类型' and hdr[7]=='拆分' and hdr[12].startswith('组合') and hdr[14].startswith('音变'), hdr
print('冻结', ws.freeze_panes, '筛选', ws.auto_filter.ref)
widths={}
for k,cd in ws.column_dimensions.items():
    if cd.width:
        for i in range((cd.min or 0),(cd.max or 0)+1): widths[i]=cd.width
def units(s): return sum(2 if (ord(ch)>=0x2E80 or ch in '“”‘’…—') else 1 for ch in s)
def est_h(text,width): return 17.25*sum(max(1,math.ceil(units(l)/max(4,width))) for l in str(text).split('\n'))
done=[]; ffix=0; grown=0
for row in ws.iter_rows(min_row=2):
    if orig_f==0:
        for c in row:
            if c.data_type=='f': c.data_type='s'; ffix+=1
    w=row[4].value; t0=row[6].value
    if not (t0 and '④' in str(t0)): continue
    split,typ,memo=data[w]
    row[7].value=split
    if typ: row[6].value=typ
    old=row[14].value
    row[14].value=memo+('\n'+str(old) if old not in (None,'') else '')
    if w in COMBO:
        o,n=COMBO[w]; lines=str(row[12].value).split('\n'); assert lines[0]==o,(w,lines[0]); lines[0]=n; row[12].value='\n'.join(lines)
    r=row[0].row; h0=ws.row_dimensions[r].height or 16.5; need=min(409,est_h(row[14].value,widths.get(15,55)))
    if need>h0: ws.row_dimensions[r].height=need; grown+=1
    done.append(w)
assert sorted(done)==sorted(data), set(data)^set(done)
print('改了', len(done), '行；被当成公式又改回文字的格', ffix, '；加高行高', grown)
t=time.time(); wb.save(TMP); print('保存', round(time.time()-t,1),'秒', os.path.getsize(TMP))
# ---------- 压缩：共享字符串按列排 + 更强的 deflate
def colnum(s):
    n=0
    for ch in s: n=n*26+ord(ch)-64
    return n
z=zipfile.ZipFile(TMP); names=[i.filename for i in z.infolist()]; mem={n:z.read(n) for n in names}; z.close()
print('xlsx 里的文件:', names)
SS=[n for n in names if n.lower().endswith('sharedstrings.xml')][0]; SH=[n for n in names if n.startswith('xl/worksheets/') and n.endswith('.xml')][0]
ss=mem[SS].decode(); sh=mem[SH].decode()
head,body,tail=re.match(r'(.*?<sst\b[^>]*>)(.*)(</sst>\s*)$',ss,re.S).groups()
items=re.findall(r'<si>.*?</si>',body,re.S); assert ''.join(items)==body
cre=re.compile(r'(<c r="([A-Z]+)(\d+)"[^>]*?t="s"[^>]*>\s*<v>)(\d+)(</v>)')
first={}
for mm in cre.finditer(sh):
    k=int(mm.group(4)); first.setdefault(k,(colnum(mm.group(2)),int(mm.group(3))))
order=sorted(range(len(items)),key=lambda i:first.get(i,(999,i))); newi={o:n for n,o in enumerate(order)}
sh2=cre.sub(lambda mm:mm.group(1)+str(newi[int(mm.group(4))])+mm.group(5),sh); ss2=head+''.join(items[i] for i in order)+tail
c1=len(zlib.compress(ss.encode(),9))+len(zlib.compress(sh.encode(),9)); c2=len(zlib.compress(ss2.encode(),9))+len(zlib.compress(sh2.encode(),9))
print('zlib9 按行排', c1, '按列排', c2)
if c2<c1: mem[SS]=ss2.encode(); mem[SH]=sh2.encode()
import zopfli
def mk(it):
    for kw in ('numiterations','iterations'):
        try:
            c=zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE, **{kw:it}); out=c.compress(b'abcabcabc')+c.flush()
            if zlib.decompress(out,-15)==b'abcabcabc': return kw
        except Exception as e: pass
    return None
KW=mk(1); print('zopfli 参数:', KW)
use=None
if KW:
    smp=mem[SS][:1000000]; t=time.time()
    c=zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE, **{KW:1}); zs=c.compress(smp)+c.flush(); dt=time.time()-t
    tot=sum(len(v) for v in mem.values()); print('zopfli 1MB 用时', round(dt,1), '秒；', len(zs), 'vs zlib', len(zlib.compress(smp,9))-6, '；全表估计', round(dt*tot/1e6),'秒')
    if dt*tot/1e6<240: use=1
og=zipfile._get_compressor
class ZC:
    def __init__(s): s.c=zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE, **{KW:use})
    def compress(s,d): return s.c.compress(d)
    def flush(s): return s.c.flush()
def write_zip(path,method):
    if method=='zopfli': zipfile._get_compressor=lambda ct,cl=None: ZC() if ct==zipfile.ZIP_DEFLATED else og(ct,cl)
    try:
        with zipfile.ZipFile(path,'w') as zo:
            for n in names:
                zi=zipfile.ZipInfo(n,date_time=(2026,11,8,12,0,0)); zi.compress_type=zipfile.ZIP_STORED if method=='stored' else zipfile.ZIP_DEFLATED
                zo.writestr(zi,mem[n],compresslevel=9 if method=='zlib9' else None)
    finally: zipfile._get_compressor=og
t=time.time(); write_zip(f'{OUTD}/z9.xlsx','zlib9'); s9=os.path.getsize(f'{OUTD}/z9.xlsx'); print('zlib9 xlsx', s9, round(time.time()-t,1),'秒')
best=f'{OUTD}/z9.xlsx'
if use:
    t=time.time(); write_zip(f'{OUTD}/zp.xlsx','zopfli'); sp=os.path.getsize(f'{OUTD}/zp.xlsx'); print('zopfli xlsx', sp, round(time.time()-t,1),'秒')
    if sp<s9: best=f'{OUTD}/zp.xlsx'
shutil.copy(best,FINAL)
with zipfile.ZipFile(FINAL) as zf:
    assert zf.testzip() is None
    for n in names: assert zf.read(n)==mem[n]
# ---------- 传输包：里面的 xlsx 不压缩，外层用更强的压缩
STO=f'{OUTD}/stored.xlsx'; write_zip(STO,'stored'); sizes={}
for ct,lab in ((zipfile.ZIP_LZMA,'lzma'),(zipfile.ZIP_BZIP2,'bzip2')):
    p=f'{OUTD}/pack_{lab}.zip'
    with zipfile.ZipFile(p,'w',ct) as zo: zo.write(STO,arcname=f'{NAME}.xlsx')
    sizes[lab]=os.path.getsize(p)
lab=min(sizes,key=sizes.get); shutil.copy(f'{OUTD}/pack_{lab}.zip',PACK)
print('传输包', sizes, '选', lab, '；解开后的 xlsx', os.path.getsize(STO))
# ---------- 体检
rows=pickle.load(open(f'{W}/rows.pkl','rb'))
def readall(p):
    wb2=load_workbook(p,read_only=True); r=[list(x) for x in wb2['拆分结果'].iter_rows(values_only=True)]; wb2.close(); return r
rows2=readall(FINAL)
assert len(rows2)==len(rows) and all(len(a)==len(b) for a,b in zip(rows,rows2))
diff={}
for i,(a,b) in enumerate(zip(rows,rows2)):
    for j,(x,y) in enumerate(zip(a,b)):
        if x!=y: diff.setdefault(hdr[j],[]).append(i)
print('改动的列和格数:', {k:len(v) for k,v in diff.items()})
assert set(diff)<= {hdr[6],hdr[7],hdr[12],hdr[14]}
xml=zipfile.ZipFile(FINAL).read(SH).decode()
print('冻结窗格:', re.search(r'<pane[^>]*>',xml).group(0)[:120]); print('公式数:', xml.count('<f>'))
def kind(s):
    s=str(s).replace('\n',' ').strip()
    if re.fullmatch(r'(—+|－+|-+|–+|无|暂无|没有|【待处理】|待处理|n/a|none|/)',s,re.I): return 'single(基础)'
    s=re.split(r'[；;]',s)[0].strip(); s=re.sub(r'\s*（[^（）]*[\u3400-\u9fff][^（）]*）','',s).strip()
    if re.search(r'\s←\s',s):
        to,fr=re.split(r'\s*←\s*',s,maxsplit=1); return 'variant' if to and fr and not re.search(r'\s\+\s',fr) else 'single'
    if re.search(r'\s≈\s',s): return 'related'
    if re.search(r'\s\+\s',s): return 'parts'
    return 'single(∽)' if SIM in s else 'single'
from collections import Counter
idx={r[4]:r for r in rows2[1:]}
print('视频读法:', Counter(kind(idx[w][7]) for w in data))
print('类型:', Counter(idx[w][6] for w in data), '；还有【待处理】:', sum(1 for r in rows2[1:] if r[7]=='【待处理】'))
print('全表类型:', Counter(r[6] for r in rows2[1:]))
for w in ('goal','lump','slash','tag','golf','jazz'):
    r=idx[w]; print(f'\n[{w}] {r[6]} | {r[7]}\n  音变: {str(r[14]).splitlines()[0]}\n  组合: {str(r[12]).splitlines()[0]}')
# 传输包能读
with zipfile.ZipFile(PACK) as zp: zp.extract(f'{NAME}.xlsx', f'{OUTD}/chk')
r3=readall(f'{OUTD}/chk/{NAME}.xlsx'); assert r3==rows2
print('\n传输包解开后和正式版一样：', len(r3)-1, '个词')
os.makedirs('/mnt/user-data/outputs',exist_ok=True)
for p in (FINAL,PACK): shutil.copy(p,'/mnt/user-data/outputs/')
print('原表', os.path.getsize(SRC), '原 zip', os.path.getsize('/mnt/user-data/uploads/0总表-词源拆分.zip'), '新 xlsx', os.path.getsize(FINAL), '传输包', os.path.getsize(PACK))

import pickle, re, zipfile, zlib, time, os, shutil, subprocess, json
from collections import Counter
from openpyxl import load_workbook
W='/home/claude/work'; SRC=f'{W}/table/master.xlsx'; NAME='词源拆分总表_不好拆分记忆版'
OUTD=f'{W}/out'; TMP=f'{OUTD}/tmp.xlsx'; FINAL=f'{OUTD}/{NAME}.xlsx'; PACK=f'{OUTD}/{NAME}_传输包.zip'; SIM='\u223d'
z=zipfile.ZipFile(TMP); names=[i.filename for i in z.infolist()]; mem={n:z.read(n) for n in names}; z.close()
SH='xl/worksheets/sheet1.xml'; sh=mem[SH].decode()
print('XML 头:', sh[:80].replace(chr(10),' '))
def unesc(m):
    cp=int(m.group(1),16) if m.group(1) else int(m.group(2))
    return chr(cp) if cp>=0xA0 and not (0xD800<=cp<=0xDFFF) and cp not in (0xFFFE,0xFFFF) else m.group(0)
n0=len(sh.encode()); sh=re.sub(r'&#x([0-9a-fA-F]+);|&#(\d+);',unesc,sh)
sh=re.sub(r'^<\?xml[^>]*\?>','<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',sh)
print('汉字从 &#…; 还原成 UTF-8：', n0, '→', len(sh.encode()), '字节'); mem[SH]=sh.encode()
print('rels:', mem['xl/_rels/workbook.xml.rels'].decode()[-300:])
# ---------- 内联字符串 → 共享字符串（按列、再按行排，同一列的内容挨在一起，压得更小）
def colnum(s):
    n=0
    for ch in s: n=n*26+ord(ch)-64
    return n
cre=re.compile(r'<c ([^>]*?)t="inlineStr"([^>]*)><is>(.*?)</is></c>',re.S)
cells=[]; 
for m in cre.finditer(sh):
    rr=re.search(r'r="([A-Z]+)(\d+)"',m.group(1)); cells.append((colnum(rr.group(1)),int(rr.group(2)),m.group(3)))
print('内联字符串格数', len(cells))
order=[]; seen={}
for c,r,inner in sorted(cells):
    if inner not in seen: seen[inner]=len(order); order.append(inner)
sh2=cre.sub(lambda m:f'<c {m.group(1)}t="s"{m.group(2)}><v>{seen[m.group(3)]}</v></c>',sh)
sst=('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
     f'count="{len(cells)}" uniqueCount="{len(order)}">'+''.join(f'<si>{x}</si>' for x in order)+'</sst>')
a=len(zlib.compress(sh.encode(),9)); b=len(zlib.compress(sh2.encode(),9))+len(zlib.compress(sst.encode(),9))
print('zlib9 内联', a, '共享按列', b)
if b<a:
    mem[SH]=sh2.encode(); mem['xl/sharedStrings.xml']=sst.encode(); names.insert(names.index(SH)+1,'xl/sharedStrings.xml')
    ct=mem['[Content_Types].xml'].decode(); assert 'sharedStrings' not in ct
    mem['[Content_Types].xml']=ct.replace('</Types>','<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>').encode()
    rl=mem['xl/_rels/workbook.xml.rels'].decode(); assert 'sharedStrings' not in rl
    mem['xl/_rels/workbook.xml.rels']=rl.replace('</Relationships>','<Relationship Id="rIdSST1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/></Relationships>').encode()
import zopfli
KW=None
for kw in ('numiterations','iterations'):
    try:
        c=zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE,**{kw:1}); o=c.compress(b'abcabcabc')+c.flush()
        if zlib.decompress(o,-15)==b'abcabcabc': KW=kw; break
    except Exception: pass
tot=sum(len(v) for v in mem.values()); use=None
if KW:
    big=max(mem,key=lambda n:len(mem[n])); smp=mem[big][:1000000]; t=time.time()
    c=zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE,**{KW:1}); zz=c.compress(smp)+c.flush(); dt=time.time()-t
    print('zopfli 1MB', round(dt,1),'秒', len(zz),'vs zlib',len(zlib.compress(smp,9))-6,'；全部估计',round(dt*tot/1e6),'秒')
    if dt*tot/1e6<240: use=1
og=zipfile._get_compressor
class ZC:
    def __init__(s): s.c=zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE,**{KW:use})
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
t=time.time(); write_zip(f'{OUTD}/z9.xlsx','zlib9'); s9=os.path.getsize(f'{OUTD}/z9.xlsx'); print('zlib9 xlsx', s9, round(time.time()-t,1),'秒'); best=f'{OUTD}/z9.xlsx'
if use:
    t=time.time(); write_zip(f'{OUTD}/zp.xlsx','zopfli'); sp=os.path.getsize(f'{OUTD}/zp.xlsx'); print('zopfli xlsx', sp, round(time.time()-t,1),'秒')
    if sp<s9: best=f'{OUTD}/zp.xlsx'
shutil.copy(best,FINAL)
with zipfile.ZipFile(FINAL) as zf:
    assert zf.testzip() is None
    for n in names: assert zf.read(n)==mem[n]
STO=f'{OUTD}/stored.xlsx'; write_zip(STO,'stored'); sizes={}
for ct,lab in ((zipfile.ZIP_LZMA,'lzma'),(zipfile.ZIP_BZIP2,'bzip2')):
    p=f'{OUTD}/pack_{lab}.zip'
    with zipfile.ZipFile(p,'w',ct) as zo: zo.write(STO,arcname=f'{NAME}.xlsx')
    sizes[lab]=os.path.getsize(p)
lab=min(sizes,key=sizes.get); shutil.copy(f'{OUTD}/pack_{lab}.zip',PACK); print('传输包', sizes, '选', lab, '；解开后', os.path.getsize(STO))
# ---------- 体检：和原表逐格比
rows=pickle.load(open(f'{W}/rows.pkl','rb')); hdr=rows[0]
def readall(p):
    wb2=load_workbook(p,read_only=True); r=[list(x) for x in wb2['拆分结果'].iter_rows(values_only=True)]; wb2.close(); return r
rows2=readall(FINAL)
assert len(rows2)==len(rows) and all(len(a)==len(b) for a,b in zip(rows,rows2))
diff={}
for i,(a,b) in enumerate(zip(rows,rows2)):
    for j,(x,y) in enumerate(zip(a,b)):
        if x!=y: diff.setdefault(hdr[j],[]).append(i)
print('改动的列和格数:', {k:len(v) for k,v in diff.items()}); assert set(diff)<={hdr[6],hdr[7],hdr[12],hdr[14]}
xml=zipfile.ZipFile(FINAL).read(SH).decode(); print('冻结:', re.search(r'<pane[^>]*>',xml).group(0)[:90], '筛选:', re.search(r'<autoFilter[^>]*>',xml).group(0) if '<autoFilter' in xml else '无', '公式:', xml.count('<f>'))
def kind(s):
    s=str(s).replace('\n',' ').strip()
    if re.fullmatch(r'(—+|－+|-+|–+|无|暂无|没有|【待处理】|待处理|n/a|none|/)',s,re.I): return 'single(—)'
    s=re.split(r'[；;]',s)[0].strip(); s=re.sub(r'\s*（[^（）]*[\u3400-\u9fff][^（）]*）','',s).strip()
    if re.search(r'\s←\s',s):
        to,fr=re.split(r'\s*←\s*',s,maxsplit=1); return 'variant' if to and fr and not re.search(r'\s\+\s',fr) else 'single'
    if re.search(r'\s≈\s',s): return 'related'
    if re.search(r'\s\+\s',s): return 'parts'
    return 'single(∽)' if SIM in s else 'single'
mrows=[r for r in rows2[1:] if str(r[14] or '').startswith('【记忆】')]
print('有【记忆】的行', len(mrows), '；视频读法', Counter(kind(r[7]) for r in mrows), '；类型', Counter(r[6] for r in mrows), '；剩【待处理】', sum(1 for r in rows2[1:] if r[7]=='【待处理】'))
print('全表类型', Counter(r[6] for r in rows2[1:]))
with zipfile.ZipFile(PACK) as zp: zp.extract(f'{NAME}.xlsx',f'{OUTD}/chk')
assert readall(f'{OUTD}/chk/{NAME}.xlsx')==rows2; print('传输包解开后和正式版逐格一样')
# LibreOffice 能不能打开（在副本上试）
shutil.copy(FINAL,f'{OUTD}/lo_chk.xlsx')
r=subprocess.run(['python3','/mnt/skills/public/xlsx/scripts/recalc.py',f'{OUTD}/lo_chk.xlsx','240'],capture_output=True,text=True); print('LibreOffice 打开检查:', (r.stdout or r.stderr).strip()[:200])
for p in (FINAL,PACK): shutil.copy(p,'/mnt/user-data/outputs/')
try:
    import pyppmd; raw=open(STO,'rb').read(); pp=pyppmd.compress(raw,max_order=6,mem_size=256<<20); print('参考：PPMd(7z 用的算法) 能压到', len(pp))
except Exception as e: print('PPMd 测不了', e)
print('大小：原 zip', os.path.getsize('/mnt/user-data/uploads/0总表-词源拆分.zip'), '原 xlsx', os.path.getsize(SRC), '→ 新 xlsx', os.path.getsize(FINAL), '传输包', os.path.getsize(PACK))

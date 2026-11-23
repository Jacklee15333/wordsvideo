import zipfile, zlib, lzma, time, os, shutil, struct, inspect
NAME='词源拆分总表_不好拆分记忆版'; OUTD='out'; FINAL=f'{OUTD}/{NAME}.xlsx'; PACK=f'{OUTD}/{NAME}_传输包.zip'
z=zipfile.ZipFile(FINAL); names=[i.filename for i in z.infolist()]; mem={n:z.read(n) for n in names}; z.close()
import zopfli
print('zopfli 里有:', [x for x in dir(zopfli) if not x.startswith('_')])
def zdeflate(b, it=1):
    for f in (lambda: zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE, iterations=it),
              lambda: zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE, numiterations=it),
              lambda: zopfli.ZopfliCompressor(zopfli.ZOPFLI_FORMAT_DEFLATE)):
        try:
            c=f(); o=c.compress(b)+c.flush(); assert zlib.decompress(o,-15)==b; return o
        except Exception as e: err=e
    import zopfli.zlib as zz
    o=zz.compress(b)[2:-4]; assert zlib.decompress(o,-15)==b; return o
smp=mem['xl/sharedStrings.xml'][:500000]; t=time.time(); o=zdeflate(smp); dt=time.time()-t
tot=sum(len(v) for v in mem.values()); print('zopfli 0.5MB', round(dt,1),'秒 →', len(o), 'vs zlib9', len(zlib.compress(smp,9))-6, '；全部估计', round(dt*tot/5e5),'秒')
og=zipfile._get_compressor
class ZC:
    def __init__(s): s.b=[]
    def compress(s,d): s.b.append(d); return b''
    def flush(s): return zdeflate(b''.join(s.b))
if dt*tot/5e5 < 420:
    zipfile._get_compressor=lambda ct,cl=None: ZC() if ct==zipfile.ZIP_DEFLATED else og(ct,cl)
    t=time.time()
    try:
        with zipfile.ZipFile(f'{OUTD}/zp.xlsx','w') as zo:
            for n in names:
                zi=zipfile.ZipInfo(n,date_time=(2026,11,8,12,0,0)); zi.compress_type=zipfile.ZIP_DEFLATED; zo.writestr(zi,mem[n])
    finally: zipfile._get_compressor=og
    with zipfile.ZipFile(f'{OUTD}/zp.xlsx') as zf:
        assert zf.testzip() is None and all(zf.read(n)==mem[n] for n in names)
    print('zopfli xlsx', os.path.getsize(f'{OUTD}/zp.xlsx'), '原来', os.path.getsize(FINAL), round(time.time()-t),'秒')
    if os.path.getsize(f'{OUTD}/zp.xlsx')<os.path.getsize(FINAL): shutil.copy(f'{OUTD}/zp.xlsx',FINAL)
# 传输包：LZMA 调成适合文字的参数（字典 64MB、极限档、pb=0）
STO=f'{OUTD}/stored.xlsx'; sto=open(STO,'rb').read()
best=os.path.getsize(PACK); print('传输包原来', best)
F={'id':lzma.FILTER_LZMA1,'preset':9|lzma.PRESET_EXTREME,'dict_size':64<<20,'lc':3,'lp':0,'pb':0,'nice_len':273}
def _init(self):
    props=lzma._encode_filter_properties(F)
    self._comp=lzma.LZMACompressor(lzma.FORMAT_RAW,filters=[lzma._decode_filter_properties(lzma.FILTER_LZMA1,props)])
    return struct.pack('<BBH',9,4,len(props))+props
oi=zipfile.LZMACompressor._init; zipfile.LZMACompressor._init=_init
try:
    t=time.time()
    with zipfile.ZipFile(f'{OUTD}/pack_x.zip','w',zipfile.ZIP_LZMA) as zo: zo.write(STO,arcname=f'{NAME}.xlsx')
finally: zipfile.LZMACompressor._init=oi
with zipfile.ZipFile(f'{OUTD}/pack_x.zip') as zp: assert zp.read(f'{NAME}.xlsx')==sto
sx=os.path.getsize(f'{OUTD}/pack_x.zip'); print('调过参数的 LZMA', sx, round(time.time()-t),'秒')
if sx<best: shutil.copy(f'{OUTD}/pack_x.zip',PACK)
# 另做一份不调参数的标准 LZMA 检查：解压软件都认 LZMA 的 zip（方法号 14）
with zipfile.ZipFile(PACK) as zp: print('传输包方法号', [i.compress_type for i in zp.infolist()], '能解开:', zp.testzip() is None)
for p in (FINAL,PACK): shutil.copy(p,'/mnt/user-data/outputs/')
print('最终：xlsx', os.path.getsize(FINAL), '传输包', os.path.getsize(PACK))

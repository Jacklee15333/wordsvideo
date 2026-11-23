import pickle, sys, time
sys.path.insert(0,'.')
from write_xlsx import write
hdr,data = pickle.load(open('table.pkl','rb'))
c1=pickle.load(open('ws1_changes.pkl','rb')); c23=pickle.load(open('ws23_changes.pkl','rb'))
changes={}
for i,t in c1.items(): changes[(i+2,12)]=t
for (i,c),t in c23.items(): changes[(i+2,c)]=t
pickle.dump(changes,open('all_changes.pkl','wb'))
print('共改', len(changes), '格；涉及', len({k[0] for k in changes}), '行')
t=time.time()
dst = sys.argv[1] if len(sys.argv)>1 else 'out/test.xlsx'
write('0词源拆分总表_部分记忆版.xlsx', dst, changes, pack=('--pack' in sys.argv))
print(round(time.time()-t),'秒')

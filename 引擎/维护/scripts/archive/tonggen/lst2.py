import pickle, sys
items=pickle.load(open('rules_items.pkl','rb'))
keys=sys.argv[1].split(','); a=int(sys.argv[2]); b=int(sys.argv[3])
sel=[it for it in items if any(it['rule'].startswith(k) for k in keys)]
pickle.dump([ (it['row'],it['line']) for it in sel], open('sel_'+sys.argv[4]+'.pkl','wb'))
for n,it in enumerate(sel[a:b],a):
    own=it['own']; w=it['word']
    o=own[len(w):].strip() if own.startswith(w) else '~'
    print(f"{n}|{w}|{o[:40]}")

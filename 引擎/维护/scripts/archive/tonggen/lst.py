import pickle, sys
items=pickle.load(open('rules_items.pkl','rb'))
key=sys.argv[1]; a=int(sys.argv[2]); b=int(sys.argv[3])
sel=[it for it in items if it['rule'].startswith(key)]
def desc(step):
    return step.lstrip('→①②③④⑤⑥⑦⑧⑨ ').strip()
for n,it in enumerate(sel[a:b],a):
    own=it['own']; w=it['word']
    o=own[len(w):].strip() if own.startswith(w) else '~'+own
    d=desc(it['step']).split('→')[0].strip()
    if o.startswith('：'): print(f"{n}|{w}|{o[:52]}")
    else: print(f"{n}|{w}|{o[:36]}|{d[:26]}")

import sys
f=sys.argv[1]; a=int(sys.argv[2]) if len(sys.argv)>2 else 1; b=int(sys.argv[3]) if len(sys.argv)>3 else 10**9; m=int(sys.argv[4]) if len(sys.argv)>4 else 300
for i,l in enumerate(open(f,encoding='utf-8',errors='replace').read().split('\n'),1):
    if a<=i<=b: print(i, l[:m])

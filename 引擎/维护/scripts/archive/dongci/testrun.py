import sys, os, importlib, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..')); sys.path.insert(0, HERE)
import lib, cols as C
from fixlib import Book
for m in ['bases', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6']:
    importlib.import_module(m)
b = Book(sys.argv[1], tag='动词变化形式'); ws = b.ws
rep = open(sys.argv[3], 'w', encoding='utf-8') if len(sys.argv) > 3 else None
for e in lib.ROWS:
    r = e['r']; assert str(ws.cell(r, C.WORD).value) == e['w'], (r, e['w'], ws.cell(r, C.WORD).value)
    oldN, oldP = str(ws.cell(r, C.COMBO).value or ''), str(ws.cell(r, C.SOUND).value or '')
    ws.cell(r, C.COMBO).value = lib.compose_N(e, oldN)
    ws.cell(r, C.SOUND).value = lib.compose_P(e, oldP)
    b._fit(r)
    if rep:
        rep.write('#%d %s\n  DROPPED-P: %s\n  DROPPED-N-blocks: %s\n' % (r, e['w'], ' || '.join(lib.dropped_text(oldP)),
                  ' || '.join(n for n, _ in lib.blocks_of(oldN)[1:] if n in e['drop'] or n == '语法')))
b.save(sys.argv[2])

"""找出需要“按词根归队”的词：
处理过的行（Q 列“词根变体处理”有值）里，若这个词的词根 R（解释里“由词根 R 变来”或“本组词根 R”）
和它现在所在组的本组词根不同，而表里另有一个组以 R 为本组词根，就建议把它移到那一组。
“本组词根”优先取 Q 列的“本组词根 X”；没有处理过的组，看哪个组的拆分里 R 出现得最多。
用法：python3 check_moves.py <xlsx>     输出建议，并写出 moves.json（[{word, row, from_group, to_group, root}]）"""
import re, sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openpyxl import load_workbook
from parse import parse_split
wb = load_workbook(sys.argv[1], read_only=True); T = list(wb['拆分结果'].iter_rows(min_row=2, values_only=True))
group_root = {}                       # 组号 -> 本组词根（来自 Q 列）
root_count = collections.defaultdict(collections.Counter)   # 词根 -> {组号: 次数}
for x in T:
    q = str(x[16] or '') if len(x) > 16 else ''
    m = re.search(r'本组词根 ([A-Za-z]+)', q)
    if m: group_root.setdefault(x[2], m.group(1).lower())
    for p in parse_split(str(x[6] or '')) or []:
        root_count[p['surface'].lower()][x[2]] += 1
def own_root(H):
    m = re.search(r'由词根 ([A-Za-z]+) 变来', H) or re.search(r'^\s*[A-Za-z()\-]+：(?:本组)?词根 ?([A-Za-z]+)', H, re.M)
    return m.group(1).lower() if m else None
moves = []
for i, x in enumerate(T, start=2):
    if len(x) <= 16 or not x[16]: continue
    R = own_root(str(x[7] or ''))
    g = x[2]
    if not R or group_root.get(g) == R: continue
    cands = [gg for gg, r in group_root.items() if r == R and gg != g]
    if not cands:
        cands = [gg for gg, n in root_count[R].most_common() if gg != g and n >= 2]
    if cands:
        moves.append(dict(word=str(x[4]), row=i, from_group=g, to_group=cands[0], root=R))
print(f'建议移动 {len(moves)} 个词')
for mv in moves: print(f"  第 {mv['row']} 行 {mv['word']}：词根 {mv['root']}，第 {mv['from_group']} 组 → 第 {mv['to_group']} 组")
json.dump(moves, open('moves.json', 'w'), ensure_ascii=False, indent=1)

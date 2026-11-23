#!/usr/bin/env python3
"""从 stdin 读“第七十八版”这样的文件夹名（一行一个），打印编号最大的那个。"""
import re, sys
D = {'零': 0, '〇': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
def cn(s):
    if s.isdigit():
        return int(s)
    total = num = 0
    for ch in s:
        if ch in D:
            num = D[ch]
        elif ch == '十':
            total += (num or 1) * 10; num = 0
        elif ch == '百':
            total += (num or 1) * 100; num = 0
        else:
            return -1
    return total + num
best = None
for line in sys.stdin:
    name = line.strip().rstrip('/').split('/')[-1]
    m = re.fullmatch(r'第(.+)版', name)
    if m and cn(m.group(1)) >= 0 and (best is None or cn(m.group(1)) > best[0]):
        best = (cn(m.group(1)), name)
if not best:
    sys.exit('没找到“第…版”文件夹')
print(best[1])

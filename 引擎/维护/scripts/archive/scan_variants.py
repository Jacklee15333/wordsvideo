"""在已经定了本组词根的组里（Q 列有“本组词根 X”），找还没写“由词根…变来 / 本组词根”的词根写法。
用法：python3 scan_variants.py <xlsx> [--words]
  默认：列出拆分里不是完整单词的部分（如 fect、capt、vey）
  --words：再列出看起来像完整单词、但其实是词根用法的部分（如 fit、gram、ward、cup），
           只列带“(=…)”或解释开头写了来源语言的行
输出里有不少噪音（复合词的另一半、别的词根、母词行），要逐条判断，只挑本组词根一家的写法。"""
import re, sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse import parse_split
from openpyxl import load_workbook
words_mode = '--words' in sys.argv
wb = load_workbook(sys.argv[1], read_only=True); ws = wb['拆分结果']
T = list(ws.iter_rows(min_row=2, values_only=True))
words = {str(x[4]).lower() for x in T}
groot = {}
for x in T:
    m = re.search(r'本组词根 ([A-Za-z]+)', str(x[16] or '') if len(x) > 16 else '')
    if m: groot.setdefault(x[2], m.group(1))
def norm(l): return re.sub(r'\([^)]*\)', '', l).strip().strip('-').lower()
out = collections.defaultdict(list)
for i, x in enumerate(T, start=2):
    g = x[2]
    if g not in groot: continue
    for p in parse_split(str(x[6] or '')) or []:
        s = p['surface'].lower()
        if not s or (s in words) != words_mode: continue
        for l in str(x[7] or '').split('\n'):
            mm = re.match(r'^\s*([^：:]{1,40})[：:]', l)
            if not mm: continue
            lab = mm.group(1).strip()
            if lab.startswith('-') or lab.endswith('-') or norm(lab) != s: continue
            if re.search(r'由词根|本组词根|词根 ?[A-Za-z]', l): continue
            if words_mode and not (p['eqs'] or re.search(r'拉丁语|希腊语|古法语|法语|意大利语|西班牙语|古英语', l.split('（见')[0][:60])): continue
            out[g].append((i, str(x[4]), str(x[6]), l[:150]))
for g, v in out.items():
    print(f'### 组{g} 本组词根={groot[g]}')
    for r in v: print('  ', *r)

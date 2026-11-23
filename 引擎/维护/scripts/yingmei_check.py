"""英美写法体检（2026-11 英美写法轮）：英式、美式写法不同的词，含义列（F）要标出是哪一边的写法，并写出另一边怎么写。

  python3 yingmei_check.py <xlsx>                 # 各类数目（应为 0）
  python3 yingmei_check.py <xlsx> --show unlabeled 40

标法（writing_guide.md 第 7 节、project_rules.md 第 51 条），写在含义第一行末尾，一个词只写一处：
  （英式拼写，美式写作 X）/（美式拼写，英式写作 X）       ——字母不同：colour / color、metre / meter
  （英式写法，美式多连写成 X）/（美式写法，英式写作 X）   ——连字符、连写、分开写不同：make-up / makeup
要不要标，看 yingmei_data.py（逐个定下的 US、UK、SPECIAL、HY、SKIP）；装了 breame（pip install breame）还会按英美拼写对照表把全表再扫一遍，
列出名单外、可能要标的词（-ize 的词英式也用，不算美式；SKIP 里的是不同的词、旧写法或两边都用）。"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openpyxl import load_workbook
import cols as C
from yingmei_data import US, UK, SPECIAL, HY, SKIP

LABEL = re.compile(r'（[^（）]*(英式|美式|英美)[^（）]*）')
CATS = {
    'unlabeled': '名单里的词，含义列没标英式 / 美式写法，或没写出另一边的写法',
    'bare_label': '含义列写了“英式拼写 / 美式拼写”，却没写另一边怎么写',
    'old_format': '还是旧写法“（英式拼写，同 X）”（改成“英式拼写，美式写作 X”）',
    'double_label': '一个词标了不止一处英美写法',
    'maybe': '（参考，要装 breame）名单外的词，对照表说是英式或美式拼写，人工看要不要标、要不要加进 yingmei_data.py',
}


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    ws = load_workbook(a[0], read_only=True)['拆分结果']
    found = {k: [] for k in CATS}
    known = set(US) | set(UK) | set(SPECIAL) | set(HY) | set(SKIP)
    try:
        from breame.spelling import american_spelling_exists, british_spelling_exists
    except ImportError:
        american_spelling_exists = british_spelling_exists = None
    for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        w, F = str(row[C.WORD - 1] or ''), str(row[C.MEAN - 1] or '')
        labs = [m.group(0) for m in LABEL.finditer(F) if re.search(r'拼写|写法|写作|拼作|连写|分开写', m.group(0))]
        if re.search(r'（英式拼写，(意思)?同 [A-Za-z]', F):
            found['old_format'].append((i, w, ''))
        for l in labs:
            if re.search(r'(英式|美式)拼写', l) and not re.search(r'[A-Za-z]', l):
                found['bare_label'].append((i, w, l))
        if len(labs) > 1:
            found['double_label'].append((i, w, ' '.join(labs)))
        if w in US or w in UK or w in SPECIAL or w in HY:
            other = (US.get(w) or UK.get(w) or '').lower()
            if not labs or (other and other not in F.lower()):
                found['unlabeled'].append((i, w, F.split('\n')[0][:40]))
        elif american_spelling_exists and w not in known and not labs:
            for p in [w] + re.split(r'[-\s]', w):
                pl = p.lower()
                if not pl or re.search(r'(ize|izes|ized|izing|ization|izations|izer|izers|yze|yzed)$', pl):
                    continue
                if american_spelling_exists(pl) or british_spelling_exists(pl):
                    found['maybe'].append((i, w, p)); break
    if '--show' in a:
        k = a[a.index('--show') + 1]; n = int(a[a.index('--show') + 2]) if len(a) > a.index('--show') + 2 else 40
        for x in found[k][:n]: print('  第 %s 行  %s  %s' % x)
        return
    print('英美写法体检' + ('' if american_spelling_exists else '（没装 breame，只查名单里的词）'))
    for k, d in CATS.items():
        print('  %-14s %5d  %s' % (k, len(found[k]), d))


if __name__ == '__main__':
    main()

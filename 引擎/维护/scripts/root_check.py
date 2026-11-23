#!/usr/bin/env python3
"""源头词根体检（2026-11 源头词根轮起）：找“经法语变了样的英语词冒充母词”的拆分，和该挂到源头词根上的外来基础词。

用法：
  python3 root_check.py <总表.xlsx>            # 一、派生词：单词部分里“在这个词里写成 X-：拉丁语…的写法；W 是它经法语变来的样子”这类行（基线 0）
  python3 root_check.py <总表.xlsx> --base     # 二、另列出可能要挂到源头词根上的外来基础词（⑤，人工看）

规矩（project_rules.md 第 42 条）：
  - 这个词直接来自拉丁语（希腊语），用的是拉丁原形，而拆分里的英语词是同一个词根经法语磨短、变了样的（popular 的 people、regular 的 rule、
    terminal 的 term），拆分写源头词根：popul + ar，词根列“popul-：人民、民众（拉丁语 populus）；people 是它经法语变来的样子（见 people）”。
  - 在完整单词上加缀的照旧写单词（popularity = popular + ity、population = populate + ion）。
  - 只差一个字母、一眼看得出的（community / common），-cle / -cul- 固定互换的（circular），英语词本身就是拉丁原形的（parcel / part），
    在法语里就这样组成的（achieve），英语本族词的元音变化（strength），动词和它的名词（decide / decision），不改：名单在 KEEP。
  - 外来基础词，同组在用源头词根、自己又变了样的：⑤ → ② 变体关联，拆分写 people ← popul，词根列补源头词根。
"""
import re, sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cols as C
from openpyxl import load_workbook

# 判断过、决定不改的派生词（单词：理由）
KEEP = {
    'community': '只差一个字母（common / commun-），communicate = common + ic + ate 是技能里定下的例子',
    'communicate': '同 community',
    'exemplary': '只差一个字母（example / exempl-）',
    'technician': '-ique / -ic 只是法语拼法（technique / technic-）',
    'particular': '-cle / -cul- 固定互换（同 -ble / -bil-）',
    'spectacular': '-cle / -cul- 固定互换',
    'circular': '-cle / -cul- 固定互换',
    'restaurant': '法语 restaurer 就是 restore，au / o 一眼看得出',
    'scholar': '只差一个字母（school / schol-）',
    'porcelain': 'c / k 拼法（pork / porc-）',
    'parcel': 'part 本身就是拉丁词根原形',
    'inert': 'art 本身就是拉丁词根原形',
    'plural': 'plus 本身就是拉丁原词',
    'prince': 'prime 本身就是拉丁词根原形（m 在 c 前变 n）',
    'degree': 'grade 本身就是拉丁词根原形',
    'achieve': '法语里就是 a + chief',
    'dessert': '法语里就是 des + servir',
    'align': '法语里就是 a + ligne',
    'gradual': 'grade 就是拉丁语 gradus 的词干，u 是拉丁词原有的',
    'graduate': '同 gradual',
    'individual': 'divide 本身就是拉丁动词，dividu- 是它的形容词',
    'Atlantic': 'Atlas 本身就是希腊原词（主格），Atlant- 是变格露出的词干',
    'only': '英语本族词的元音变化（one / on-）',
    'once': '同 only',
    'further': '英语本族词（forth / furth-）',
    'twelve': '英语本族词（two / twe-）',
    'husband': '英语本族词（house / hus-）',
}
HINT = re.compile(r'经法语|变格时露出|的写法|古法语形式|走了样|法语拼法')


def derived(rows):
    out = []
    for i, r in rows:
        w = str(r[C.WORD - 1] or '')
        for line in str(r[C.WPART - 1] or '').split('\n'):
            m = re.match(r'^\s*([^：:]{1,40})[：:].*在这个词里写成\s*([^：:]+)[：:](.*)$', line)
            if m and HINT.search(m.group(3)) and w not in KEEP:
                out.append((i, w, str(r[C.SPLIT - 1]), m.group(1), m.group(2), m.group(3)[:60]))
    return out


def base(rows):
    norm = lambda s: re.sub(r'[^a-z]', '', re.sub(r'\([^)]*\)', '', str(s).lower()))
    grp = collections.defaultdict(list)
    for i, r in rows:
        grp[r[2]].append(r)
    out = []
    for i, r in rows:
        if not str(r[C.TYPE - 1] or '').startswith('⑤') or not re.search(r'拉丁|希腊|法语', str(r[C.WPART - 1] or '')):
            continue
        w = norm(r[C.WORD - 1])
        roots = set()
        for m in grp[r[2]]:
            if m is r:
                continue
            for line in str(m[C.ROOT - 1] or '').split('\n'):
                t = C.label_of(line)
                if t and C.is_part_label(t) and len(norm(t)) >= 3:
                    roots.add(norm(t))
        hidden = sorted(x for x in roots if not w.startswith(x[:3]) and x[0] == w[0])
        if hidden:
            out.append((i, r[C.WORD - 1], '、'.join(hidden)))
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    ws = load_workbook(sys.argv[1], read_only=True)['拆分结果']
    rows = [(i, list(r)) for i, r in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2)]
    d = derived(rows)
    print('一、派生词：英语词冒充母词（KEEP 名单外）', len(d))
    for x in d:
        print('  第 %d 行 %s  拆分 %s  | %s → %s：%s' % x)
    if '--base' in sys.argv:
        b = base(rows)
        print('二、外来基础词，同组有词根、自己的写法里看不出来（人工看，多半是不同的词根，不一定要改）', len(b))
        for x in b:
            print('  第 %d 行 %s  同组词根：%s' % x)


if __name__ == '__main__':
    main()

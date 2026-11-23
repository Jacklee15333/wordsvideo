"""字母变化同源词轮（2026-11）的改表脚本，只作记录。用法：python3 round.py <源表.xlsx> <新表.xlsx>
拆分写成 X ≈ Y 的 116 个外来词逐个看过：46 个音变 / 字母变化列（P）第一行写成一步步的字母变化链，下面每一步一行，
原有的【同源】等说明照原文留在后面，原来那句话里步骤没讲到的补成标签段落（写法见 zimu2_data.py，规矩见 references/project_rules.md 第 44、46 条）；
另外 70 个不写链（本族词、来源不确定、变化很小），名单记进「整表核对记录」。每行写 U 列，「整表核对记录」记 2 条，「说明」改 P 列说明、第七节加一行。"""
import os, sys, re, copy, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from fixlib import Book
import cols as C
from zimu2_data import DATA, SKIP

SRC, OUT = sys.argv[1], sys.argv[2]
b = Book(SRC, tag='字母变化同源词')
ws = b.ws

def order_secs(old, secs):
    def pos(s):
        if s in old: return old.index(s)
        m = re.match(r'^(【[^】]+】)', s)
        return old.index(m.group(1)) if m and m.group(1) in old else -1
    return sorted(secs, key=pos)

# P 列（音变 / 字母变化）列宽 50 → 55：这一轮 dress、trouble 的链有五步，按 50 宽要超过 Excel 行高上限 409 磅
for d in ws.column_dimensions.values():
    if (d.min or 0) <= 16 <= (d.max or 0):
        assert d.min == d.max == 16 and d.width == 50, (d.min, d.max, d.width)
        d.width = 55

for r, w, new, keep, rew in DATA:
    assert str(ws.cell(r, C.WORD).value) == w, (r, w, ws.cell(r, C.WORD).value)
    assert '≈' in str(ws.cell(r, C.SPLIT).value), (w, ws.cell(r, C.SPLIT).value)
    old = str(ws.cell(r, C.SOUND).value or '')
    assert not old.startswith('【字母变化】'), w
    for s in keep:
        assert s in old, (w, s[:30])
    secs = order_secs(old, keep + rew)
    ws.cell(r, C.SOUND).value = new + ('\n' + '\n'.join(secs) if secs else '')
    forms = re.findall(r"(\*?[A-Za-z][A-Za-z'’\-]*)\s*（", new.split('\n')[0])
    other = str(ws.cell(r, C.SPLIT).value).split('≈')[1].split('\n')[0].strip()
    msg = ('音变列改成一步步的字母变化链（' + ' → '.join(forms) + '），下面每一步一行讲清哪个字母掉了、哪个变了、读音怎么变；'
           f'① 讲清和 {other} 的关系（同一个源头走了两条路）；原有的【同源】等说明留在后面')
    if rew:
        msg += '；原来那句话里步骤没讲到的补成' + '、'.join(re.match(r'^(【[^】]+】)', x).group(1) for x in rew)
    b.note(r, msg)
    b._fit(r)

names = lambda k: '、'.join(SKIP[k].split())
b.log += [
 ('已修正', None, '字母变化同源词',
  '拆分写成 X ≈ Y 的外来词（rail ≈ rule、dress ≈ direct、danger ≈ dominate……），本词和源头字母差得多，音变列原来只有一句话（有的只讲了一处变化，有的只讲读音），学生看不出 regula 是怎么一步步变成 rail 的',
  '逐个看了 zimu_check.py --todo 列出的 116 个 ≈ 词，46 个音变列第一行写成字母变化链“【字母变化】regula（拉丁语）→ *regla（俗拉丁语）→ reille（古法语）→ rail（英语）”，下面每一步一行讲清哪个字母掉了、哪个变了、读音怎么变，并举同类的例子；链从这个词自己的源头写到它本身，≈ 两边的词是兄弟（同一个源头走了两条路），① 里讲清两者的关系。原有的【同源】【易混】【同形异义】等照原文留在后面；原来那句话里步骤没讲到的补成标签段落（apprentice【短形式】prentice、scent【同类】scythe、pattern【分工】等）。中间形式、年代逐个对照 etymonline。P 列列宽 50 → 55（dress、trouble 五步的链按 50 宽要超过 Excel 行高上限）。逐行见 U 列“字母变化同源词：…”'),
 ('特殊（未改）', None, '字母变化同源词（不写链）',
  f'另外 70 个 ≈ 词不写字母变化链。本族词 {len(SKIP["本族词"].split())} 个（一直在英语里，没有经过别的语言，不是这种一步步的字母变化）：{names("本族词")}；'
  f'来源不确定 {len(SKIP["来源不确定"].split())} 个（词典自己说“也许、说法不一”，写不出可靠的步骤）：{names("来源不确定")}；'
  f'变化很小 {len(SKIP["变化很小"].split())} 个（基本只差拼写、词尾，或是照别的词造出来的，如 gas 照 chaos 造）：{names("变化很小")}',
  '不写链，音变列照旧；zimu_check.py --todo 不再列出这 70 个（名单在 scripts/zimu_check.py 的 SKIP_APPROX）'),
]

# ---------------- 说明 ----------------
S = b.wb['说明']
def find_row(a, bstart=None):
    for r in range(1, S.max_row + 1):
        if S.cell(r, 1).value == a and (bstart is None or str(S.cell(r, 2).value or '').startswith(bstart)):
            return r
    raise KeyError(a)
def fit_height(r, col='B'):
    w = S.column_dimensions[col].width or 60
    dw = sum(2 if ord(ch) > 0x2E80 else 1 for ch in str(S.cell(r, 2).value))
    S.row_dimensions[r].height = max(S.row_dimensions[r].height or 17.25, 17.25 * math.ceil(dw / max(10, w - 2)))

r = find_row('P 音变 / 字母变化')
v = S.cell(r, 2).value
old_head = '字母和源头差得多的词（people ← popul 这类），'
assert v.startswith(old_head), v[:40]
S.cell(r, 2).value = v.replace(old_head, '字母和源头差得多的词（people ← popul、rail ≈ rule 这类），', 1).replace(
    '以后一个箭头一行，讲清哪个字母掉了、哪个变了、读音怎么变。',
    '以后一个箭头一行，讲清哪个字母掉了、哪个变了、读音怎么变；拆分写成 X ≈ Y 的，链从本词自己的源头写起，① 讲清和 Y 的关系（同一个源头走了两条路）。', 1)
assert S.cell(r, 2).value != v
fit_height(r)
r0 = find_row('字母变化', '挂到源头词根上的')
r0 = S.max_row
rn = r0 + 1
for c in range(1, 5):
    S.cell(rn, c)._style = copy.copy(S.cell(r0, c)._style)
S.cell(rn, 1).value = '字母变化同源词'
S.cell(rn, 2).value = ('拆分写成 X ≈ Y 的 116 个外来词逐个看过：46 个音变列第一行写成字母变化链（rail：regula → *regla → reille → rail；dress：directus → *directiare → drecier → dresser → dress），'
                       '下面每一步一行讲清字母、读音怎么变，① 讲清和 ≈ 后面那个词的关系（兄弟，不是谁从谁变来的）；原有的【同源】【易混】等留在后面，原话里步骤没讲到的补成标签段落。'
                       '另外 70 个（本族词、来源不确定、变化很小）不写链，名单见「整表核对记录」。逐行见 U 列“字母变化同源词：…”。')
S.cell(rn, 4).value = '=COUNTIF(拆分结果!$U$2:$U$9294,"*字母变化同源词*")'
S.row_dimensions[rn].height = max(S.row_dimensions[r0].height or 17.25, 17.25 * 4)
# 上一轮的 COUNTIF 只数“字母变化：”（不把这一轮的“字母变化同源词：”算进去）
assert S.cell(r0, 1).value == '字母变化'
S.cell(r0, 4).value = '=COUNTIF(拆分结果!$U$2:$U$9294,"*字母变化：*")'

b.save(OUT)
print('改了', len(DATA), '行；说明第', r, '行、第', rn, '行')

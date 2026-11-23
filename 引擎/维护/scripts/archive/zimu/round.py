"""字母变化轮（2026-11）的改表脚本，只作记录。用法：python3 round.py <源表.xlsx> <新表.xlsx>
挂到源头词根上的 37 个外来基础词（people ← popul 这类），音变 / 字母变化列（P）第一行写成一步步的字母变化链，
下面每一步一行；原有的【同源】等说明照原文留在后面（写法见 zimu_data.py，规矩见 references/project_rules.md 第 44 条）。
顺带改正 flower 的【同源】（第 45 条）。每行写 U 列，「整表核对记录」记 2 条，「说明」改 P 列说明、第七节加一行。"""
import os, sys, re, copy, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from fixlib import Book
import cols as C
from zimu_data import DATA

SRC, OUT = sys.argv[1], sys.argv[2]
b = Book(SRC, tag='字母变化')
ws = b.ws

def order_secs(old, secs):
    """保留的段落按它们在原文里的先后排；新写的【对照】这类原文里没有的排在最前（它们是从原来那句讲变化的话里拆出来的）"""
    def pos(s):
        if s in old: return old.index(s)
        m = re.match(r'^(【[^】]+】)', s)
        return old.index(m.group(1)) if m and m.group(1) in old else -1
    return sorted(secs, key=pos)

for r, w, new, keep, rew in DATA:
    assert str(ws.cell(r, C.WORD).value) == w, (r, w, ws.cell(r, C.WORD).value)
    old = str(ws.cell(r, C.SOUND).value or '')
    for s in keep:
        assert s in old, (w, s[:20])
    secs = order_secs(old, keep + rew)
    ws.cell(r, C.SOUND).value = new + ('\n' + '\n'.join(secs) if secs else '')
    forms = re.findall(r'(\*?[A-Za-z][A-Za-z\'’\-]*)\s*（', new.split('\n')[0])
    msg = '音变列改成一步步的字母变化链（' + ' → '.join(forms) + '），下面每一步一行讲清哪个字母掉了、哪个变了、读音怎么变；原有的【同源】等说明留在后面'
    if w == 'flower':
        msg += '；【同源】里“14 世纪末起‘花’义才固定写作 flower”改正为“面粉原来也写 flower，约 1830 年起才固定写成 flour”（etymonline flour 条目）'
    b.note(r, msg)
    b._fit(r)

b.log += [
 ('已修正', None, '字母变化',
  '挂到源头词根上的 37 个外来基础词（people ← popul、rule ← regul、order ← ordin、voice ← voc、city ← civ……），字母和源头差得多，音变列原来只有一句话，order、image、matter、mount、letter、prove、place、course 等根本没讲字母怎么变，学生看不出 popul 是怎么一步步变成 people 的',
  '音变列第一行写成字母变化链“【字母变化】populus（拉丁语）→ pople（古法语）→ peuple（古法语）→ people（英语）”，下面每一步一行（①②③…）讲清哪个字母掉了、哪个变了、读音怎么变，并举同类的例子；没留下文字、推出来的形式带 *（*retundus、*capum）；原有的【同源】【易混】【趣】等照原文留在后面。中间形式、年代逐个对照 etymonline。逐行见 U 列“字母变化：…”'),
 ('已修正', 4007, 'flower',
  '【同源】写着“14 世纪末起‘花’义才固定写作 flower”；etymonline flour 条目说的是“面粉”原来也写 flower，约 1830 年起才固定写成 flour、和“花”分开（flour 那一行本来就写对了）',
  '改成“flower / flour 本是一个词：‘面粉’是麦子磨出来最精华的部分，原来也写 flower，约 1830 年起才固定写成 flour，和‘花’分开（见 flour）”'),
]
assert str(ws.cell(4007, C.WORD).value) == 'flower'

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
assert S.cell(r, 2).value == '也放【同源】【易混】【联想】', S.cell(r, 2).value
S.cell(r, 2).value = ('字母和源头差得多的词（people ← popul 这类），第一行写一步步的字母变化链：【字母变化】populus（拉丁语）→ pople（古法语）→ peuple（古法语）→ people（英语），'
                      '每个形式后面括号里写语言，没留下文字、推出来的形式前面加 *，英语原样借来的最后一个写“grace（古法语、英语）”；下面每一步一行（①②③…）：① 讲源头那个形式和词根，'
                      '以后一个箭头一行，讲清哪个字母掉了、哪个变了、读音怎么变。视频“怎么变来的”那一幕照这条链一步步变字母。也放【同源】【易混】【联想】【对照】【派生】【合成】')
fit_height(r)
r0 = find_row('源头词根', '拆分里冒充母词')
assert r0 == S.max_row, '「源头词根」不是最后一行'
rn = r0 + 1
for c in range(1, 5):
    S.cell(rn, c)._style = copy.copy(S.cell(r0, c)._style)
S.cell(rn, 1).value = '字母变化'
S.cell(rn, 2).value = ('挂到源头词根上的 37 个外来基础词（people ← popul、rule ← regul、order ← ordin……），音变列第一行写成一步步的字母变化链（populus → pople → peuple → people），每个形式后面写语言；'
                       '下面每一步一行讲清哪个字母掉了、哪个变了、读音怎么变，并举同类的例子（order 的 n 变 r：拉丁 Londinium → 法语 Londres）；原有的【同源】【易混】【趣】留在后面。'
                       '顺带改正 flower 的【同源】（“面粉”约 1830 年才固定写成 flour）。逐行见 U 列“字母变化：…”。')
S.cell(rn, 4).value = '=COUNTIF(拆分结果!$U$2:$U$9294,"*字母变化*")'
S.row_dimensions[rn].height = max(S.row_dimensions[r0].height or 17.25, 17.25 * 4)

b.save(OUT)
print('改了', len(DATA), '行；说明第', r, '行、第', rn, '行')

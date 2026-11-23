import sys, re, json, copy, math, pickle, collections
sys.path.insert(0, '/home/claude/work/etymology-table/scripts')
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment
import columns as C
import ast, types
def _load_ex():
    src = open('/home/claude/work/etymology-table/scripts/sense_rules.py', encoding='utf-8').read()
    out = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', '') in ('EX', 'WHY') for t in node.targets):
            out[node.targets[0].id] = ast.literal_eval(node.value)
    return types.SimpleNamespace(**out)
PL = _load_ex()
from insert_rows import rebuild_with_inserts, fit_height

SRC, OUT = '/home/claude/work/src.xlsx', sys.argv[1]
wb = load_workbook(SRC)
ws = wb['拆分结果']
N0 = ws.max_row
row_of = {}
for r in range(2, N0 + 1):
    row_of.setdefault(str(ws.cell(r, 5).value), r)
R = lambda w: row_of[w]
get = lambda r, c: ws.cell(r, c).value or ''
def setv(r, c, v): ws.cell(r, c).value = v
P_LATER = collections.defaultdict(list)          # 要用到新行号的 P 记录，重排后再写
def addP(r, t): v = get(r, 16); setv(r, 16, (v + '；' if v else '') + t)
lab = lambda l: l.split('：', 1)[0].strip() if '：' in l else ''

def H_keep(r, first, keep, edit=None, extra=()):
    out = [first] if first else []
    for l in [x for x in get(r, 8).split('\n') if x.strip()]:
        if any(lab(l) == k or (k.endswith('*') and lab(l).startswith(k[:-1])) for k in keep):
            out.append(edit(l) if edit else l)
    return '\n'.join(list(out) + list(extra))

def I_new(r, first, drop_blocks=(), drop_lines=(), repl=None, add=None):
    L = get(r, 9).split('\n')
    out, seen, skip = [first], False, False
    for l in L[1:]:
        m = re.match(r'^\s*【([^【】]{1,10})】', l)
        if m:
            skip = m.group(1) in drop_blocks
        if skip:
            continue
        if C.STEP.match(l):
            seen = True
        if not seen and C.sentence_from_eq(l):
            continue                              # 原来逐个写的后缀等式
        if any(d in l for d in drop_lines):
            continue
        for a, b in (repl or {}).items():
            l = l.replace(a, b)
        out.append(l)
    if add:
        for after, lines in add.items():
            k = next(i for i, l in enumerate(out) if after in l)
            out[k + 1:k + 1] = lines
    return '\n'.join(out)

def canon(I, w):
    return C.compose_I(C.parse_I(I, w))

LESS = '-less：加在名词后面，变成形容词：“没有…的”（来自古英语 leas“没有…的”，和 loose“松开的”是一家，见 loose；同 careless 粗心的、tireless 不知疲倦的）'
IZE = '-ize：动词词尾“使…化、使成为…”（来自希腊语动词词尾 -izein，经拉丁语 -izare、法语 -iser 进入英语；同 modernize 使现代化）'
ICAL = '-ical：= -ic + -al，形容词词尾“…的、与…有关的”（-ic 加 -al：-ic 来自拉丁语 -icus、希腊语 -ikos，-al 来自拉丁语 -alis）'

# ======================================================================== 一、派生词改用直接母词
CH = {}      # 派生词 → dict(G, H, I, K?, M?, L?, parent, kind)
def ch(w, G, H, I, parent, kind, why='', **kw):
    CH[w] = dict(G=G, H=H, I=I, parent=parent, kind=kind, why=why, **kw)

r = R('thoughtlessly')
ch('thoughtlessly', 'thoughtless + ly',
   H_keep(r, 'thoughtless：没有考虑的、轻率的（见 thoughtless）；不变，直接加 -ly', ['-ly']),
   I_new(r, '【构词逻辑】thoughtless（没有考虑的）+ ly（…地）=“不加考虑地”；词性变化（-ly）：形容词 → 副词', drop_blocks=('演变',)),
   'thoughtless', 'new', extra='；thoughtless 的年代（1590s、1680s、1794）挪到 thoughtless 那一行')
r = R('breathlessly')
ch('breathlessly', 'breathless + ly',
   H_keep(r, 'breathless：喘不上气的、屏住呼吸的（见 breathless）；不变，直接加 -ly', ['-ly']),
   I_new(r, '【构词逻辑】breathless（喘不上气的）+ ly（以…的方式）=“喘不上气地”；词性变化（-ly）：形容词 → 副词'),
   'breathless', 'new')
r = R('aimlessly')
ch('aimlessly', 'aimless + ly',
   H_keep(r, 'aimless：没有目标的、漫无目的的（见 aimless）；不变，直接加 -ly', ['-ly']),
   I_new(r, '【构词逻辑】aimless（没有目标的）+ ly（以…的方式）=“没有目标地”；词性变化（-ly）：形容词 → 副词'),
   'aimless', 'new')
r = R('fertilizer')
ch('fertilizer', 'fertilize + r',
   H_keep(r, 'fertilize：使肥沃、施肥（见 fertilize）', ['-er']),
   I_new(r, '【构词逻辑】fertilize（使肥沃）+ r（…的东西）=“使土地肥沃的东西”；词性变化（-er）：动词 → 名词（东西）'),
   'fertilize', 'new')
r = R('civilization')
ch('civilization', 'civilize + ation',
   H_keep(r, 'civilize：使开化、使文明（见 civilize）；在这个词里写成 civiliz-：去掉词尾 e，再加 -ation', ['-ation', '为什么*']),
   I_new(r, '【构词逻辑】civilize（使开化、使文明）+ ation（这件事 / 结果）=“开化的过程和结果”；词性变化（-ation）：动词 → 名词'),
   'civilize', 'new')
r = R('civilisation')
ch('civilisation', 'civilise + ation',
   H_keep(r, 'civilise：使开化（英式拼写，见 civilise）；在这个词里写成 civilis-：去掉词尾 e，再加 -ation', ['-ation']),
   I_new(r, '【构词逻辑】civilise（使开化）+ ation（…这件事）=“开化的过程和结果”；词性变化（-ation）：动词 → 名词'),
   'civilise', 'new')
r = R('industrialization')
ch('industrialization', 'industrialize + ation',
   H_keep(r, 'industrialize：使工业化（见 industrialize）；在这个词里写成 industrializ-：去掉词尾 e，再加 -ation', ['-ation']),
   I_new(r, '【构词逻辑】industrialize（使工业化）+ ation（…这件事）=“使工业化的过程”；词性变化（-ation）：动词 → 名词'),
   'industrialize', 'new')
r = R('urbanization')
ch('urbanization', 'urbanize + ation',
   H_keep(r, 'urbanize：使城市化（见 urbanize）', ['-ation']),
   I_new(r, '【构词逻辑】urbanize（使城市化）+ ation（…这件事、…的过程）=“城市化的过程”；词性变化（-ation）：动词 → 名词'),
   'urbanize', 'new')
r = R('linguistic')
ch('linguistic', 'linguist + ic',
   H_keep(r, 'linguist：语言学家；通晓多种语言的人（见 linguist）；不变，直接加 -ic', ['-ic']),
   I_new(r, '【构词逻辑】linguist（语言学家）+ ic（…的）=“语言学家的”；词性变化（-ic）：名词 → 形容词'),
   'linguist', 'new')
r = R('binoculars')
ch('binoculars', 'binocular + s',
   H_keep(r, 'binocular：双眼的、双眼并用的（见 binocular）；不变，直接加 -s', ['-s']),
   I_new(r, '【构词逻辑】binocular（双眼并用的）+ s（复数）=“两只眼睛一起用的东西”；词性变化（-s）：形容词 → 名词（复数）',
         drop_blocks=('演变',), drop_lines=('→（形容词 binocular）双眼并用的',),
         repl={'→（复数名词）双筒望远镜': '→（复数名词）双筒望远镜（1866 年已见）'}),
   'binocular', 'new', extra='；binocular 的年代（1713、1738）挪到 binocular 那一行')
r = R('tropics')
ch('tropics', 'tropic + s',
   H_keep(r, 'tropic：回归线（见 tropic）；不变，直接加 -s', ['-s']),
   '\n'.join(['【构词逻辑】tropic（回归线）+ s（复数）=“（太阳）掉头的那两条线（之间）”；词性变化（-s）：名词 → 名词（复数）',
              '→ 南北两条回归线合起来说，再指两条线中间的整片地区 →（复数）热带（the tropics，1817 年起）',
              '　用词规律：名词用复数时，常常专指一类东西、一整套或一大片（tropics 热带；waters 水域）',
              '【今义】the tropics：热带（地区）（plants that grow in the tropics 生长在热带的植物）']),
   'tropic', 'new', J='', K='', extra='；“回归线”这一步、【演变】的前两段、【辨析】、K 列【同源】和本组【背景】挪到 tropic 那一行')
r = R('furnishings')
ch('furnishings', 'furnishing + s',
   H_keep(r, 'furnishing：配进屋里的东西（见 furnishing）；不变，直接加 -s', ['-s']),
   I_new(r, '【构词逻辑】furnishing（配进屋里的东西）+ s（复数）=“配进屋里的各样东西”；词性变化（-s）：名词 → 名词（复数）'),
   'furnishing', 'new')
r = R('crackly')
ch('crackly', 'crackle + y',
   H_keep(r, 'crackle：噼噼啪啪地响（见 crackle）', ['-y']),
   I_new(r, '【构词逻辑】crackle（噼噼啪啪响个不停）+ y（有…特点的）=“带着噼啪声的”；词性变化（-y）：动词 → 形容词'),
   'crackle', 'new')
r = R('sophisticated')
ch('sophisticated', 'sophisticate + d',
   H_keep(r, 'sophisticate：掺假、使不纯；使不再单纯（见 sophisticate）', ['-ed']),
   I_new(r, '【构词逻辑】sophisticate（掺假、使不再单纯）+ d（被…了的）=“被掺了假的、不再单纯的”；词性变化（-ed）：动词 → 形容词'),
   'sophisticate', 'new')
r = R('containerized')
ch('containerized', 'containerize + d',
   H_keep(r, 'containerize：使集装箱化（见 containerize）', ['-d']),
   I_new(r, '【构词逻辑】containerize（使集装箱化）+ d（被…了的、已经…了的）=“已经集装箱化的”；词性变化（-d）：动词 → 形容词'),
   'containerize', 'new')
# ---- 母词生僻、临时造或已废：不补行，各部分解释里讲清母词
r = R('calendarized')
ch('calendarized', 'calendarize + d',
   H_keep(r, 'calendarize：按日历来安排、处理（calendar 日历 + -ize 使…化，见 calendar；calendar 本身也能当动词“排进日程”，calendarize 更像专业用语，词典标为美式，财务分析里也常用；英式也拼 calendarise）', ['-ed']),
   I_new(r, '【构词逻辑】calendarize（按日历来安排、处理）+ d（被…了的、已经…了的）=“被按日历处理过的”；词性变化（-ed）：动词 → 形容词'),
   'calendarize', 'inline', why='较新的专业用词')
r = R('mascotized')
ch('mascotized', 'mascotize + d',
   H_keep(r, 'mascotize：做成吉祥物（mascot 吉祥物 + -ize 使…化、使成为…，见 mascot；按规则派生的新词，词典一般不收；英式也拼 mascotise）', ['-d']),
   I_new(r, '【构词逻辑】mascotize（做成吉祥物）+ d（被…了的）=“被做成吉祥物了的”；词性变化（-d）：动词 → 形容词（被…了的）'),
   'mascotize', 'inline', why='按规则临时造的词')
r = R('opinionated')
ch('opinionated', 'opinionate + d',
   H_keep(r, 'opinionate：持有看法（约 1600 年用 opinion“看法”+ -ate“使…、做…”造的动词，见 opinion；后来基本不用了，只剩形容词 opinionated）', ['-d'],
          edit=lambda l: l.replace('；动词 opinionate 后来基本不用了，只剩形容词 opinionated', '')),
   I_new(r, '【构词逻辑】opinionate（持有看法）+ d（被…了的）=“被看法塞满了的”；词性变化（-d）：动词 → 形容词'),
   'opinionate', 'inline', why='已经不用的动词')
r = R('sorcerer')
ch('sorcerer', 'sorcer + er',
   '\n'.join(['sorcer：抽签算命的人（14 世纪末借自古法语 sorcier；往上是中世纪拉丁语 sortiarius“抽签算命的人”，来自拉丁语 sors“签、命运”，见 sort；t 到了法语里变成 c）；sorcer 后来不再单用',
              '-er：英语本族的“做…的人”（英语本来就有的后缀，古英语写作 -ere；同 teacher 老师）；sorcer 本来就是“…的人”，15 世纪初又多加了一个 -er，等于“人”说了两遍（同 caterer 承办酒席的人、upholsterer 室内装潢商）；也有一说 sorcerer 是从 sorcery“巫术”倒推出来的']),
   I_new(r, '【构词逻辑】sorcer（抽签算命的人）+ er（…的人）=“抽签算命的人”（-er 叠了一次，意思不变；见 sort 的【背景】）；词性变化（-er）：名词（人）→ 名词（人）'),
   'sorcer', 'inline', why='中古英语里的词、后来不单用')
r = R('trashcapes')
ch('trashcapes', 'trashcape + s',
   H_keep(r, 'trashcape：= trashscape“垃圾景观”（trash 垃圾 + -scape“…的景象、景观”，见 trash；-scape 来自荷兰语 -schap，从 landscape 里截出来，1796 年起这样用；两个 s 撞在一起，这里只写了一个）', ['-s']),
   I_new(r, '【构词逻辑】trashcape（垃圾景观）+ s（复数）=“（一处处）垃圾景观”；词性变化（-s）：名词 → 名词（复数）'),
   'trashcape', 'inline', why='仿 cityscape 临时造的词')
# ---- -ical 当一个后缀
r = R('technical')
ch('technical', 'techn + ical',
   H_keep(r, None, ['techn', '为什么*']).replace('\n为什么', '\n' + ICAL + '；英语先有 technic“技艺的”（1610s），再加 -al 成了 technical\n为什么', 1),
   I_new(r, '【构词逻辑】techn（技艺）+ ical（…的）=“技艺上的”；词性变化（-ical）：名词 → 形容词'),
   'techn', 'ical')
r = R('geological')
ch('geological', 'geology + ical',
   '\n'.join(['geology：地质学（见 geology）；在这个词里写成 geolog-：去掉词尾 y，再加 -ical',
              ICAL + '；geologic、geological 都有，都是“地质的”'] + [l for l in get(r, 8).split('\n') if l.startswith('为什么')]),
   I_new(r, '【构词逻辑】geology（地质学）+ ical（…的）=“地质学的、地质的”；词性变化（-ical）：名词 → 形容词'),
   'geology', 'ical', L='✅ 一致', M='geological 条目：1791 年，geology + -ical；复核（2026-11）：联网核对 etymonline，与表里一致', N='etymonline · geological')
r = R('mythical')
ch('mythical', 'myth + ical',
   H_keep(r, None, ['myth', '为什么*']).replace('\n为什么', '\n' + ICAL + '；先有 mythic“神话的”（1660s），再加 -al 成了 mythical（1670s）\n为什么', 1),
   I_new(r, '【构词逻辑】myth（神话）+ ical（…的）=“属于神话的”；词性变化（-ical）：名词 → 形容词'),
   'myth', 'ical')

# ======================================================================== 二、补出来的母词（放在派生词正上方）
r_tro = R('tropics')
NEW = [
 dict(w='thoughtless', above='thoughtlessly', G='thought + less',
      H=['thought：想法、考虑（见 thought）', LESS],
      I=['【构词逻辑】thought（考虑）+ less（没有…的）=“没有考虑的”；词性变化（-less）：名词 → 形容词',
         '→ 做事前没先想一想 → 不加思考的、轻率的（1590s）',
         '→ 只顾自己，没替别人想一想 → 不体谅人的、不顾别人的（也许 1794 年起）',
         '【演变】（1680s）愚钝的、不会思考的（这个意思后来不用了）',
         '【今义】欠考虑的、轻率的（a thoughtless remark 欠考虑的话）；不体谅人的（It was thoughtless of him to keep us waiting. 他让我们干等，太不体谅人了）',
         '【辨析】thoughtless 多半不是故意的，只是“没想到”；careless 是“粗心、不小心”；反义词是 thoughtful（体贴的）'],
      M='thoughtless 条目：1590s“不加思考的、轻率的”，thought + -less；1680s 有“愚钝的”；“不体谅别人的”也许 1794 年起', key='thoughtless'),
 dict(w='breathless', above='breathlessly', G='breath + less',
      H=['breath：气、一口气（见 breath）', LESS.replace('tireless 不知疲倦的', 'homeless 无家可归的')],
      I=['【构词逻辑】breath（气）+ less（没有…的）=“没气的”；词性变化（-less）：名词 → 形容词',
         '→ 一口气也吸不进来 → 喘不过气的（14 世纪末）',
         '→ 跑得太急，上气不接下气 → 气喘吁吁的（15 世纪中）',
         '→ 激动、紧张、盼着什么，连气都忘了喘 → 屏住呼吸的、激动得透不过气的（1765 年起）',
         '【演变】（1590s）也指“没了气息的、死了的”（这个意思后来不用了）',
         '【今义】气喘吁吁的、上气不接下气的（breathless after running up the stairs 跑上楼梯后气喘吁吁）；屏住呼吸的、激动得透不过气的（breathless with excitement）'],
      M='breathless 条目：14 世纪末“无法呼吸的”，breath + -less；“气喘吁吁的”15 世纪中；1590s 也作“死了的”；因激动、期待而“忘了呼吸的”1765 年起', key='breathless'),
 dict(w='aimless', above='aimlessly', G='aim + less',
      H=['aim：目标（见 aim）', LESS.replace('tireless 不知疲倦的', 'homeless 无家可归的') + '；和表示“更少”的 less 不是一回事'],
      I=['【构词逻辑】aim（目标）+ less（没有…的）=“没有目标的”；词性变化（-less）：名词 → 形容词',
         '→ 做事、过日子不知道要奔哪儿去 → 没有目标的、漫无目的的（1620s）',
         '【今义】没有目标的、漫无目的的（an aimless life 没有目标的生活）',
         '【辨析】aimless 说没有方向和目的；pointless 说“没有意义、白费力气的”'],
      M='aimless 条目：1620s“没有目标、没有目的的”，aim (n.) + -less', key='aimless'),
 dict(w='fertilize', above='fertilizer', G='fertile + ize',
      H=['fertile：肥沃的；能生育的（见 fertile）；在这个词里写成 fertil-：去掉词尾 e，再加 -ize', IZE + '；英式也写 -ise（fertilise）'],
      I=['【构词逻辑】fertile（肥沃的）+ ize（使…）=“使肥沃”；词性变化（-ize）：形容词 → 动词',
         '→ 往地里施肥，让土地肥起来 → 施肥、使（土地）肥沃（1640s）',
         '→ fertile 也有“能生育的”意思：让卵子受精、花朵受粉，好长出后代 →（生物）使受精、使受粉（1859 年起）',
         '【今义】施肥（fertilize the soil 给土壤施肥）；（生物）使受精、使受粉（a fertilized egg 受精卵）'],
      M='fertilize 条目：1640s“使肥沃”，fertile + -ize；生物学义“使（卵）受精”1859 年起', key='fertilize'),
 dict(w='civilize', above='civilization', G='civil + ize',
      H=['civil：公民的、有礼的（见 civil）', IZE + '；civilize 约 1600 年借自法语 civiliser；英式多写 civilise'],
      I=['【构词逻辑】civil（公民的、有礼的）+ ize（使…化）=“使成为有礼的公民”；词性变化（-ize）：形容词 → 动词',
         '→ 让过着部落生活的人有了法度、秩序，像城里的公民那样过日子 → 使开化、使文明（约 1600 年）',
         '→ 让一个人的言谈举止变得斯文 → 使有教养、使文雅',
         '【今义】使开化、使文明（civilize a society）；使有教养、使文雅',
         '【辨析】civilize 说一群人、一个社会走向文明；educate 说教育、培养一个人'],
      M='civilize 条目：约 1600 年，借自法语 civiliser（古法语 civil，拉丁语 civilis“公民的”）：使脱离野蛮、建立秩序、使文雅；不及物“变得文明”1868 年起', key='civilize'),
 dict(w='civilise', above='civilisation', G='civil + ise',
      H=['civil：公民的、有礼的（见 civil）', '-ise：= -ize，动词词尾“使…化”（就是 -ize：来自希腊语动词词尾 -izein，经法语 -iser 进入英语）；英式多写 -ise，美式一律写 -ize（见 civilize）'],
      I=['【构词逻辑】civil（有礼的）+ ise（使…化）=“使开化”；词性变化（-ise）：形容词 → 动词',
         '→ 同 civilize（英式拼写）：使开化、使文明；使有教养',
         '【今义】使开化、使文明；使有教养（英式拼写，同 civilize）'],
      M='etymonline 把 civilise 当作 civilize 的英式拼写（civilize 条目：约 1600 年借自法语 civiliser）', key='civilize'),
 dict(w='industrialize', above='industrialization', G='industrial + ize',
      H=['industrial：工业的（见 industrial）', IZE + '；英式多写 industrialise'],
      I=['【构词逻辑】industrial（工业的）+ ize（使…化）=“使工业化”；词性变化（-ize）：形容词 → 动词',
         '→ 盖工厂、用机器大批生产，让一个国家、地区从种地、手工为主变成工业为主 →（使）工业化（1852）',
         '【今义】（使）工业化（an industrialized country 工业化国家）'],
      M='industrialize 条目：1852 年，industrial + -ize，可能仿照法语 industrialiser（1842）', key='industrialize'),
 dict(w='urbanize', above='urbanization', G='urban + ize',
      H=['urban：城市的（见 urban）', IZE + '；英式也拼 urbanise'],
      I=['【构词逻辑】urban（城市的）+ ize（使…化）=“使城市化”；词性变化（-ize）：形容词 → 动词',
         '→ 17 世纪先说人：使有城里人的风度 → 使文雅（1640s，这个意思后来不用了）',
         '→ 农田、村庄盖成楼房街道，人往城里聚 → 使城市化（1884 年起，这个意思来自法语 urbaniser）',
         '【今义】使城市化（an urbanized area 城市化地区）'],
      M='urbanize 条目：1640s“使更文雅”；1884 年起“使变成城市”，这个意思来自法语 urbaniser（1873）', key='urbanize'),
 dict(w='linguist', above='linguistic', G='lingu + ist',
      H=['lingu：= lingua“舌头 → 语言”（见 language）；去掉词尾 a 再接后缀',
         '-ist：一般加在名词后面，表示“…的人、精通…的人”（来自希腊语 -istēs，经拉丁语 -ista、法语 -iste 进入英语；同 artist 艺术家、scientist 科学家）；linguist 是拉丁语词根配希腊来的后缀，混搭出来的词'],
      I=['【构词逻辑】lingu（语言）+ ist（精通…的人）=“精通语言的人”；词性变化（-ist）：名词 → 名词（人）',
         '→ 会说好几种语言的人 → 通晓多种语言的人（1580s）',
         '→ 专门研究语言本身的人 → 语言学家（1640s）',
         '【今义】语言学家；通晓多种语言的人（She is a good linguist. 她学外语很有天赋）',
         '【辨析】linguist 研究语言或通晓多种语言；translator 是笔译，interpreter 是口译'],
      M='linguist 条目：1580s“精通多种语言的人”，拉丁语 lingua“舌头、语言”+ -ist 的混合词；“研究语言的人”1640s', key='linguist'),
 dict(w='binocular', above='binoculars', G='bin + ocul + ar',
      H=[l for l in get(R('binoculars'), 8).split('\n') if lab(l) in ('bin', 'ocul', '-ar')],
      I=['【构词逻辑】bin（成对的）+ ocul（眼睛）+ ar（…的）=“两只眼睛一起用的”；词性变化（-ar）：名词 → 形容词',
         '→ 两只眼睛同时看 → 双眼的、双眼并用的（1738，binocular vision 双眼视觉）',
         '→ 两只眼睛一起看的望远镜，先叫 binocular glass，后来只说 binocular → 双筒望远镜（1871，多用复数 binoculars，见 binoculars）',
         '　用词规律：表示性质、状态的词，也拿来叫有这种性质的人、东西或机构（binocular 双眼并用的 → 双筒望远镜；beauty 美 → 美人）',
         '【演变】（1713）有两只眼睛的；1738 年的“双眼并用的”借自法语 binoculaire；这种望远镜更早叫 binocle',
         '【今义】（adj.）双眼的、双眼并用的（binocular vision 双眼视觉）；（n.）双筒望远镜（多用复数 binoculars）'],
      M='binocular 条目：1738“双眼并用的”，更早 1713“有两只眼的”；借自法语 binoculaire（拉丁语 bini“成对的”+ ocularis“眼睛的”）；指望远镜 1871 年，是 binocular glass 的省略，更早叫 binocle', key='binocular'),
 dict(w='tropic', above='tropics', G='trop + ic',
      H=[l for l in get(r_tro, 8).split('\n') if lab(l) == 'trop'] +
        ['-ic：形容词词尾，“…的、与…有关的”（来自拉丁语 -icus、希腊语 -ikos，经法语 -ique 进入英语；同 basic 基本的、magic 魔法的）；希腊语 tropikos kyklos 就是“（太阳）转向的那个圈”，后来单说 tropic 就指这个圈'],
      I=['【构词逻辑】trop（转）+ ic（…的）=“（太阳）转向的”；词性变化（-ic）：名词 → 形容词（后来当名词）',
         '→ 太阳直射点北移到北纬约 23.5° 就“掉头”往南，到南纬约 23.5° 再“掉头”往北 → 天上太阳掉头的那两个圈（14 世纪末，天文）',
         '→ 地球上和它们对应的两条纬线 → 回归线（1520s，地理）',
         '→ 两条回归线之间的地区 →（the tropics）热带（见 tropics）',
         '【今义】回归线（the Tropic of Cancer 北回归线；the Tropic of Capricorn 南回归线）；（the tropics）热带'] +
        [l for l in get(r_tro, 9).split('\n') if l.startswith('【辨析】')],
      J=get(r_tro, 10), K=get(r_tro, 11),
      M='tropic 条目：14 世纪末天文用语，指天球上太阳到达最北、最南的两个圈；来自中世纪拉丁语 tropicus、拉丁语 tropicus、希腊语 tropikos“转向的；至日的”；1520s 起指地球上的两条回归线', key='tropic'),
 dict(w='furnishing', above='furnishings', G='furnish + ing',
      H=['furnish：给房子配家具、陈设（见 furnish）',
         '-ing：加在动词后变名词，可以指“…这件事”，也可以指“由此而来的东西”（英语本来就有，古英语写作 -ung / -ing，专门把动作变成名词）'],
      I=['【构词逻辑】furnish（给房子配东西）+ ing（…这件事 / 配进来的东西）=“布置房子这件事 / 配进屋里的东西”；词性变化（-ing）：动词 → 名词',
         '→ 给屋子配家具、挂窗帘这件事 → 布置、陈设',
         '→ 配进屋里的那一样样东西 →（多用复数 furnishings）家具陈设、室内用品（约 1600 年）',
         '　用词规律：表示动作的词，也拿来叫做这件事用的东西（furnishing 布置 → 家具陈设；cover 盖 → 盖子）',
         '【今义】（多用复数）家具陈设、室内用品（soft furnishings 布艺软装）；（作定语）家具装饰用的（furnishing fabrics 家具装饰布料）'],
      M='etymonline 无 furnishing 单独条目；furnishings 条目：约 1600 年，furnish (v.) 的动名词复数，指家具陈设', key='furnishings'),
 dict(w='crackle', above='crackly', G='crack + le',
      H=['crackle_crack', 'crackle_le'],
      I=['【构词逻辑】crack（噼啪一响）+ le（一下一下地…）=“噼噼啪啪响个不停”；词性变化（-le）：动词 → 动词（一下一下、反复地做）',
         '→ 柴火烧着、油锅里炸东西，一连串细碎的响声 → 噼啪作响（15 世纪中）',
         '→ 当名词：这一连串的响声 → 噼啪声、爆裂声；（电话、收音机里的）杂音',
         '　用词规律：表示动作的词，也能直接当名词用，指这件事或做一次（crackle 噼啪作响 → 噼啪声；walk 走 → 散步）',
         '【今义】（v.）噼啪作响（The fire crackled. 火噼啪作响）；（n.）噼啪声、爆裂声（the crackle of the fire）'],
      M='crackle 条目：15 世纪中 crackelen“不停地噼啪作响”，crack (v.) 的反复形式', key='crackle'),
 dict(w='sophisticate', above='sophisticated', G='sophistic + ate',
      H=['sophistic：诡辩的、耍小聪明的（拉丁语 sophisticus、希腊语 sophistikos“诡辩家的”：soph“智慧”+ -ist“…的人”+ -ic“…的”；希腊语 sophistēs 原是“行家、智者、老师”，后来在雅典专指收费教人的人，被看成玩弄言辞的诡辩家；soph 见 philosophy）',
         '-ate：动词词尾“使…、做…”（来自拉丁语“被…了的”形式的词尾 -atus，英语借拉丁动词时常拿它当动词用）：中世纪拉丁语 sophisticare“掺假；欺骗；诡辩”，英语约 1400 年借来成了 sophisticate'],
      I=['【构词逻辑】sophistic（诡辩家式的）+ ate（使…）=“像诡辩家那样掺假”；词性变化（-ate）：形容词 → 动词',
         '→ 往酒、药里偷偷兑别的东西，让它不纯 → 掺假、使不纯（约 1400 年）',
         '→ 用似是而非的道理把事情搅浑 → 用诡辩迷惑（约 1600 年）',
         '→ 让人经过世事，不再天真单纯 → 使变得世故、使不再单纯（1796 年起）',
         '→ 后来也当名词用：见过世面、讲究品位的人 → 老于世故的人、老练的人',
         '【今义】（n.）老于世故的人、见过世面的人；（v.）使变得世故、使不再单纯；（旧）掺假'],
      M='sophisticate 条目：约 1400 年“掺杂使不纯”，来自中世纪拉丁语 sophisticare“掺假；欺骗；诡辩”（拉丁语 sophisticus，希腊语 sophistikos“诡辩家的”）；约 1600 年“用诡辩迷惑”，1796 年起“使不再单纯”', key='sophisticate'),
 dict(w='containerize', above='containerized', G='container + ize',
      H=['container：集装箱；（计算机）容器（见 container）', IZE + '；英式也拼 containerise'],
      I=['【构词逻辑】container（集装箱、容器）+ ize（使…化）=“使集装箱化”；词性变化（-ize）：名词 → 动词',
         '→ 20 世纪 50 年代兴起集装箱运输：散货先装进统一规格的大铁箱，整箱装船、装车 → 用集装箱装运、使集装箱化',
         '→ 软件也学这个办法：把程序连同它要用的东西打包进一个个“容器”里运行 →（计算机）容器化',
         '　用词规律：一个词用进某一行（电脑、法律、体育、音乐……），就有了那一行的专门意思（containerize 用集装箱装运 → （计算机）容器化；mouse 老鼠 → （电脑）鼠标）',
         '【今义】用集装箱装运、使集装箱化；（计算机）把（应用程序）容器化'],
      L='✅ 随词族', M='etymonline 无 containerize 单独条目；container 已核；container + -ize，常规派生，随 20 世纪 50 年代的集装箱运输出现', key='container'),
]
crk = [l for l in get(R('crackly'), 8).split('\n')]
for d in NEW:
    if d['w'] == 'crackle':
        d['H'] = [next(l for l in crk if lab(l) == 'crack'), next(l for l in crk if lab(l) == '-le')]

# ======================================================================== 三、⏳ 待核查 / ❓ 查无：联网复核结果
VER = {   # 单词: (依据摘要, 来源条目)
 'usable': ('14 世纪末借自古法语 usable；约 1840 年以后才常用，很可能是按 use + -able 重新造的', 'usable'),
 'maximum': ('名词 1740 年，借自法语、拉丁语 maximum（maximus“最大的”的中性形式，magnus“大”的最高级）；形容词 1834 年', 'maximum'),
 'worker': ('14 世纪中 werker“干活的人”，work (v.) + -er；1747 年起指工蜂，1848 年起指雇工', 'worker'),
 'deviate': ('1630s，来自晚期拉丁语 deviare（拉丁语 de via：de“离开”+ via“路”）；“偏离、背离”1690s', 'deviate'),
 'changed': ('无 changed 单独条目；change (v.) 已核，过去分词作形容词，常规构词', 'change'),
 'bearable': ('15 世纪中，bear (v.) + -able“能忍受的”', 'bearable'),
 'qualification': ('1540s，来自法语 qualification、中世纪拉丁语 qualificatio（qualificare“使有资格”）；后来指“使人胜任的资历、条件”', 'qualification'),
 'washed': ('无 washed 单独条目；wash (v.) 已核，过去分词作形容词，常规构词', 'wash'),
 'uncontrollable': ('1570s 先作“无可辩驳的”（18 世纪后不用），un- + controllable；“管不住、难以抑制的”1640s', 'uncontrollable'),
 'suspicion': ('约 1300 年，经英法语 suspecioun、古法语 suspicion 来自晚期拉丁语，和 suspect 同出拉丁语 suspicere“往上看 → 怀疑”', 'suspicion'),
 'commemorate': ('1590s，来自拉丁语 commemorare：com- 这里也许只是加强语气 + memorare“提醒”；“纪念”义 1630s', 'commemorate'),
 'noticed': ('无 noticed 单独条目；notice (v.) 已核，常规构词', 'notice'),
 'employment': ('15 世纪中，employ + -ment；1640s 起指“职业、工作”', 'employment'),
 'saving': ('作形容词约 1300 年（save (v.) 的现在分词）；作介词 14 世纪末；“存款”义见 savings', 'saving'),
 'check-up': ('1921 年，美国英语，来自短语动词 check up（1889）', 'check-up'),
 'amid': ('中古英语 amidde，来自古英语 on middan“在中间”', 'amid'),
 'inject': ('约 1600 年医学用语，来自拉丁语 inicere（in“向里”+ iacere“扔”）', 'inject'),
 'profess': ('14 世纪初“发愿入修会”，由 profession 倒推或来自中世纪拉丁语 professare（拉丁语 profiteri“公开声明”）', 'profess'),
 'finished': ('约 1300 年，finish (v.) 的过去分词作形容词；1580s 起“已完成的”', 'finished'),
 'finite': ('15 世纪初，来自拉丁语 finitum（finire“划定界限”的过去分词）', 'finite'),
 'internationalize': ('1864 年，international + -ize', 'internationalize'),
 'undoubted': ('15 世纪中，un- + doubt (v.) 的过去分词', 'undoubted'),
 'duo': ('1580s“二重唱”，经意大利语或法语来自拉丁语 duo“二”；“二人组”1887 年', 'duo'),
 'pre-order': ('1630s“预先安排”（OED 标为罕用），pre- + order (v.)；“预订（商品）”是后来的用法', 'pre-order'),
 'teaching': ('晚期古英语 tecunge“教导”，teach 的动名词；约 1300 年起指“教的内容”', 'teaching'),
 'accord': ('动词 12 世纪初，来自古法语 acorder、俗拉丁语 *accordare（ad“向”+ cor“心”）；名词 13 世纪末', 'accord'),
 'connective': ('1650s，connect + -ive；connective tissue（结缔组织）1839 年', 'connective'),
 'disconnect': ('1770 年，dis- + connect，也许是从 disconnection 倒推的', 'disconnect'),
 'challenged': ('1570s“被挑战的”，challenge (v.) 的过去分词作形容词；1985 年起委婉指“残障的”', 'challenged'),
 'initiate': ('动词约 1600 年，来自晚期拉丁语 initiare（initium“开端”）；名词 1732 年', 'initiate'),
 'accountable': ('约 1400 年（英法语 14 世纪中），来自古法语 acontable，account (v.) + -able', 'accountable'),
 'avail': ('约 1300 年，英法语合成：a-“向”+ valoir“值”（拉丁语 valere“强壮、值”）', 'avail'),
 'perceive': ('约 1300 年，经英法语、古北部法语来自拉丁语 percipere（per + capere“抓”）', 'perceive'),
 'coincide': ('1705、1715 年，来自中世纪拉丁语 coincidere（com“一起”+ incidere“落在…上”：in + cadere“落”）', 'coincide'),
 'intentional': ('1520s，intention + -al，或来自中世纪拉丁语 intentionalis', 'intentional'),
 'antique': ('形容词 1530s、1540s，来自法语 antique、拉丁语 antiquus“从前的”（PIE *anti-“在前”）；名词 1520s，1771 年起指“古董”', 'antique'),
 'convert': ('约 1300 年，来自古法语 convertir、拉丁语 convertere（com + vertere“转”）', 'convert'),
 'adverse': ('14 世纪末，来自古法语 advers、拉丁语 adversus（advertere“转向”的过去分词）', 'adverse'),
 'co-produce': ('无 co-produce 单独条目；co-、produce 已核，常规构词', 'produce'),
 'treated': ('无 treated 单独条目；treat (v.) 已核，常规构词', 'treat'),
 'situate': ('15 世纪初，来自中世纪拉丁语 situare“安放”（拉丁语 situs“位置”）', 'situate'),
 'ageing': ('aging（也拼 ageing）1860 年，age (v.) 的动名词', 'aging'),
 'friendly': ('古英语 freondlic，friend + -ly', 'friendly'),
 'marking': ('古英语 mearcung，mark (v.) 的动名词', 'marking'),
 'mechanise': ('mechanize 的英式拼写', 'mechanise'),
 'mechanize': ('1670s“使机械化”，mechanic (adj.) + -ize', 'mechanize'),
 'dominant': ('15 世纪中，来自古法语 dominant、拉丁语 dominari“统治”的现在分词（dominus“主人”）', 'dominant'),
 'beautiful': ('15 世纪中，beauty + -ful', 'beautiful'),
 '6th-grader': ('无 6th-grader 条目；grade、-er 已核，常规合成', 'grade'),
 '7th-grader': ('无 7th-grader 条目；grade、-er 已核，常规合成', 'grade'),
 'proceed': ('14 世纪末，来自古法语 proceder、拉丁语 procedere“向前走”（pro + cedere）', 'proceed'),
 'literal': ('14 世纪末，来自晚期拉丁语 literalis“文字的”（littera“字母”）', 'literal'),
 'midfield': ('无 midfield 单独条目；mid-、field 已核，常规合成', 'field'),
 'tireless': ('1590s“不知疲倦的”，tire (v.) + -less（接的是动词 tire“累”）；1862 年起指车轮“没装轮胎的”', 'tireless'),
 'serving': ('名词约 1200 年“服侍”；1769 年起指“（一份）饭菜”；形容词约 1300 年', 'serving'),
 'lie': ('lie (v.1)：古英语 leogan“欺骗、背叛”，原始日耳曼语 *leuganan；来源不确定，拉丁语、希腊语、梵语里都没有', 'lie'),
 'cheery': ('15 世纪中，cheer (n.) + -y', 'cheery'),
 'troubleshoot': ('1918 年（见于 troubleshooting），多半是从 troubleshooter 倒推的', 'troubleshoot'),
 'bore': ('名词 1766 年“厌烦”、1778 年“令人厌烦的事”，动词 1768 年；通常说是 bore“钻孔”的比喻，OED 有疑问，早期证据显示也许和法语有关', 'bore'),
 'super': ('形容词 1837 年，从前缀 super-（superfine 等）而来；1895 年起俚语泛指“极好的”', 'super'),
 'race': ('race (n.2)：1560s 借自法语 race，再往上也许是意大利语 razza，来源不明', 'race'),
 'destructible': ('1704 年，来自晚期拉丁语 destructibilis（destruere“拆毁”）', 'destructible'),
 'co-author': ('名词 1850 年，co- + author；1948 年起作动词', 'co-author'),
 'authorized': ('无 authorized 单独条目；authorize 已核，过去分词作形容词，常规构词', 'authorize'),
 'harmed': ('无 harmed 单独条目；harm (v.) 已核，常规构词', 'harm'),
 'hurried': ('1660s“匆忙的”，hurry (v.) 的过去分词作形容词', 'hurried'),
 'joking': ('1660s，joke (v.) 的动名词；作形容词是现在分词', 'joking'),
 'apt': ('14 世纪中“倾向于”、14 世纪末“合适的”，来自古法语 ate 或直接来自拉丁语 aptus（*apere“系、连”的过去分词）', 'apt'),
 'earning': ('earning 见 earnings 条，earn 的动名词', 'earnings'),
 'mandate': ('名词约 1500 年“命令”，来自法语 mandat、拉丁语 mandatum“被交代的事”（mandare 过去分词的中性形式）；动词 1620s 由名词而来', 'mandate'),
 'obese': ('1650s，由 obesity 倒推，也部分来自拉丁语 obesus“吃胖了的”（obedere：ob + edere“吃”）；19 世纪以前少见', 'obese'),
 'encode': ('1917 年，en- + code (n.)；计算机义 1955 年', 'encode'),
 'trade-off': ('1959 年“为得到一样而放弃另一样”，来自短语动词 trade off（1793 年“以物换掉”）', 'trade-off'),
 'livestream': ('无 livestream 条目；live (adj.)“实况的”、stream 已核，常规合成（韦氏收有此词，见来源链接）', 'live'),
 'Frank': ('Frank (n.)：古英语 franc，来自中世纪拉丁语 francus（借自法兰克语 *Frank，族名）；族名来源不确定，传统说法是来自“标枪”', 'frank'),
 'victor': ('14 世纪中，经英法语、古法语来自拉丁语 victor“征服者”（vincere 的过去分词词干）', 'victor'),
 'emphasis': ('1570s，来自拉丁语、希腊语 emphasis（emphainein“显现”：en + phainein）', 'emphasis'),
 'filtered': ('无 filtered 单独条目；filter (v.) 已核，常规构词', 'filter'),
 'credible': ('14 世纪末，来自拉丁语 credibilis（credere“相信”）', 'credible'),
 'surrounding': ('surroundings 1857 年“周围环境”，surround (v.) 的动名词复数；surrounding (n.) 1825 年“包围”', 'surroundings'),
 'administer': ('14 世纪末，来自古法语 aministrer、拉丁语 administrare（ad + ministrare“服侍”）', 'administer'),
 'grandmother': ('15 世纪初，grand- + mother，多半仿法语 grand-mère；取代了更早的 grandame', 'grandmother'),
 'sparing': ('14 世纪末“节省的”，spare (v.) 的现在分词作形容词；sparingly 15 世纪中', 'sparing'),
 'cinematograph': ('无单独条目；cinema 条目：法语 cinématographe，1890s 卢米埃尔兄弟用希腊语 kinēmat-“运动”造的词，cinema 由它截短；cinematographer 1897 年', 'cinema'),
 'integer': ('1570s“整数”，来自拉丁语 integer“完整的、没被碰过的”（in- + tangere“碰”）', 'integer'),
 'preschool': ('形容词 1886 年“学龄前的”，名词 1910 年“幼儿园”', 'preschool'),
 'seventy': ('古英语 (hund)seofontig，seven + -ty', 'seventy'),
 'mine': ('mine (n.1)：约 1300 年，来自古法语 mine、中世纪拉丁语 mina，来源不确定，很可能来自凯尔特语', 'mine'),
 'disciplinary': ('1590s，来自中世纪拉丁语 disciplinarius（disciplina）', 'disciplinary'),
 'gravitation': ('1640s 物理用语，来自近代拉丁语 gravitare（见 gravitate；拉丁语 gravitas“重”）', 'gravitation'),
 'scale': ('scale (n.1)：约 1300 年，来自古法语 escale“壳、荚”，日耳曼语来源（原始日耳曼语 *skæla“劈开”）', 'scale'),
 'senate': ('约 1200 年，来自古法语 senat、拉丁语 senatus“长老会议”（senex“老人”）', 'senate'),
 'equate': ('15 世纪初，来自拉丁语 aequare“使相等”', 'equate'),
 'equity': ('14 世纪初，来自古法语 equite、拉丁语 aequitas', 'equity'),
 'fury': ('14 世纪末，来自古法语 furie、拉丁语 furia（furere“发狂”，来源不确定）', 'fury'),
 'romance': ('约 1300 年，来自古法语 romanz“用俗语写的诗体故事”，原是副词“用俗语（说、写）”', 'romance'),
 'migrating': ('无 migrating 单独条目；migrate 已核，常规构词', 'migrate'),
 'instinctive': ('1640s，拉丁语 instinct-（instinguere“激发”）+ -ive', 'instinctive'),
 'erode': ('1610s，由 erosion 倒推或来自法语 éroder、拉丁语 erodere（ex + rodere“啃”）', 'erode'),
 'Atlas': ('1580s 神话里扛天的巨神；“地图集”1636 年（墨卡托地图集扉页画着 Atlas）', 'atlas'),
 'malice': ('约 1300 年，来自古法语 malice、拉丁语 malitia（malus“坏”）', 'malice'),
 'fifteen': ('古英语 fiftyne，fif“五”+ -tyne（-teen）', 'fifteen'),
 'wanted': ('1690s“缺少的”，1812 年起“被通缉的”，want (v.) 的过去分词作形容词', 'wanted'),
 'sanitary': ('1823 年，来自法语 sanitaire（1812）、拉丁语 sanitas“健康”', 'sanitary'),
 'rite': ('14 世纪初，来自拉丁语 ritus“习俗、仪式”，也许出自 PIE *re-“计算、思考”', 'rite'),
 'rose': ('rose (n.1)：古英语 rose，来自拉丁语 rosa', 'rose'),
 'vice': ('vice (n.1)：约 1300 年，来自古法语 vice、拉丁语 vitium“缺陷、过错”', 'vice'),
 'divine': ('形容词 14 世纪末，来自古法语 divin、拉丁语 divinus（divus，和 deus“神”有关）', 'divine'),
 'nose': ('古英语 nosu，原始日耳曼语 *nuso-，PIE *nas-“鼻子”', 'nose'),
 'ridicule': ('名词 1670s，来自法语 ridicule 或拉丁语 ridiculum（ridere“笑”）；动词 1680s', 'ridicule'),
 'sewer': ('sewer (n.1)：约 1400 年，来自英法语 sewere、古北部法语 sewiere“池塘的泄水闸”，字面“让水流走的东西”', 'sewer'),
 'trimming': ('1510s“整理、修整”，trim (v.) 的动名词；1530s 起“打扮、装饰”', 'trimming'),
 'pizza': ('1845 年，来自意大利语 pizza“饼、馅饼”，来源不确定', 'pizza'),
}
FIX = {   # ⏳ 里内容有错、这次改掉的（词性变化写错）
 'tireless': ('tire 是动词“累”（etymonline：tire (v.) + -less），词性变化原写“名词 → 形容词”', '改成“动词 → 形容词”，tire 一行写明是动词'),
 'mandate': ('mandate 先有名词“被交代下来的事”（约 1500 年），动词 1620s 才有，第一行却写“（-ate）：变成动词”', '改成“（-ate）：动词 → 名词”'),
 'senate': ('-ate 在这里是表示“团体”的名词词尾，第一行却写“（-ate）：变成动词”', '改成“（-ate）：变成名词”'),
 'instinctive': ('instinct 是名词“本能”，第一行却写“（-ive）：动词 → 形容词”', '改成“名词 → 形容词”，-ive 一行写明这里加在名词后面'),
}
r = R('tireless')
setv(r, 8, get(r, 8).replace('tire：疲倦（见 tire）', 'tire：累、疲倦（这里是动词，见 tire）').replace(LESS.replace('tireless 不知疲倦的', 'endless 无尽的'), LESS.replace('tireless 不知疲倦的', 'endless 无尽的') + '；这里少见地接在动词 tire 后面'))
setv(r, 9, get(r, 9).replace('；词性变化（-less）：名词 → 形容词', '；词性变化（-less）：动词 → 形容词'))
r = R('mandate'); setv(r, 9, get(r, 9).replace('；词性变化（-ate）：变成动词', '；词性变化（-ate）：动词 → 名词'))
r = R('senate'); setv(r, 9, get(r, 9).replace('；词性变化（-ate）：变成动词', '；词性变化（-ate）：变成名词'))
r = R('instinctive')
setv(r, 9, get(r, 9).replace('；词性变化（-ive）：动词 → 形容词', '；词性变化（-ive）：名词 → 形容词'))
setv(r, 8, get(r, 8).replace('；instinctive 17 世纪 40 年代起', '；这里加在名词 instinct 后面（拉丁语里接的是动词 instinguere“激发”的词干 instinct-）；instinctive 17 世纪 40 年代起'))
for w in FIX:
    assert '变成动词' not in get(R(w), 9).split('\n')[0] and '名词 → 形容词；' not in get(R(w), 9)[:0], w
QUERY = {   # ❓ 查无：复核后仍保留
 'unbelieve': 'etymonline、韦氏仍查不到 unbelieve；AHD、韦氏收的是 misbelieve（误信）、disbelieve（不信，约 1644 年）；只有个别网上词表收 unbelieve，照字面理解',
 'air-draw': 'etymonline（2026 年版）、主要词典仍未收；照字面理解（同 air-kiss、air guitar 的构词）',
 'safe-shell': 'etymonline（2026 年版）、主要词典仍未收；shell 已核，照字面理解',
}
nver = collections.Counter()
for i in range(2, N0 + 1):
    L0 = get(i, 12)
    if not L0.startswith(('⏳', '❓')):
        continue
    w = str(get(i, 5))
    if L0.startswith('❓'):
        setv(i, 13, get(i, 13) + '；复核（2026-11）：' + QUERY[w])
        addP(i, '联网复核：❓ 查无复核，' + QUERY[w].split('；')[0] + '，保留 ❓')
        nver['❓'] += 1
        continue
    summ, key = VER[w]
    m = re.match(r'新增母词：(.*?补出)', get(i, 13))
    head = '新增母词：' + m.group(1) if m else get(i, 13)
    if w in FIX:
        setv(i, 12, '✏️ 已修正')
        setv(i, 13, f'{head}；联网复核（2026-11）：etymonline {key} 条目：{summ}；表里已改：{FIX[w][1]}')
        addP(i, f'联网复核：⏳ 待核查 → ✏️ 已修正（{FIX[w][0]}，{FIX[w][1]}）')
        nver['✏️'] += 1
    else:
        setv(i, 12, '✅ 一致')
        setv(i, 13, f'{head}；联网复核（2026-11）：etymonline {key} 条目：{summ}；与表里一致')
        addP(i, f'联网复核：⏳ 待核查 → ✅ 一致（etymonline {key} 条目）')
        nver['✅'] += 1
    nk = 'merriam-webster.com · livestream；etymonline · live、stream' if w == 'livestream' else f'etymonline · {key}'
    setv(i, 14, nk)
print('复核', dict(nver))

# ======================================================================== 四、写派生词（旧行上直接改），再补行
for w, d in CH.items():
    r = R(w)
    d['oldG'] = get(r, 7)
    setv(r, 7, d['G']); setv(r, 8, d['H'])
    I = canon(d['I'], w)
    if I != d['I']:
        print('【canon 改动】', w); print('  手写：', d['I'].replace('\n', ' ⏎ ')[:400]); print('  canon：', I.replace('\n', ' ⏎ ')[:400])
    setv(r, 9, I)
    for col, k in ((10, 'J'), (11, 'K'), (12, 'L'), (13, 'M'), (14, 'N')):
        if k in d:
            setv(r, col, d[k] or None)
r = R('tropical'); setv(r, 8, get(r, 8).replace('tropic：回归线（见 tropics）', 'tropic：回归线（见 tropic）'))
inserts = []
for d in NEW:
    a = R(d['above'])
    I = '\n'.join(d['I'])
    I2 = canon(I, d['w'])
    if I2 != I:
        print('【canon 改动·新行】', d['w']); print('  手写：', I.replace('\n', ' ⏎ ')[:500]); print('  canon：', I2.replace('\n', ' ⏎ ')[:500])
    vals = {5: d['w'], 6: '① 词根词缀', 7: d['G'], 8: '\n'.join(d['H']), 9: I2, 10: d.get('J') or None, 11: d.get('K') or None,
            12: d.get('L', '✅ 一致'), 13: d['M'] + '；联网核对（2026-11）', 14: f"etymonline · {d['key']}", 15: None, 17: None}
    inserts.append({'above': a, 'values': vals})
o2n, new_rows, LAST, changed = rebuild_with_inserts(wb, inserts)
ws = wb['拆分结果']
print('新行', list(zip([d['w'] for d in NEW], new_rows)), '末行', LAST, '改写引用', dict(changed))
plain = next(rr for rr in range(2, 50) if not ws.cell(rr, 17).value)
for d, n in zip(NEW, new_rows):
    ws.cell(n, 17)._style = copy.copy(ws.cell(plain, 17)._style)
    dn = o2n[R(d['above'])]
    ws.cell(n, 16).value = (f"直接母词：新增母词，为第 {dn} 行 {d['above']} 补出（几个后缀的词改用直接母词）；批次、组号、小类号与 {d['above']} 相同；"
                            f"内容据 etymonline {d['key']} 条目和 {d['above']} 条整理，联网核对" + ('；本组【背景】、K 列【同源】从 tropics 挪到这里' if d['w'] == 'tropic' else ''))
P2 = {d['above']: (d['w'], n) for d, n in zip(NEW, new_rows)}
for w, d in CH.items():
    n = o2n[R(w)]
    c = ws.cell(n, 16)
    if d['kind'] == 'new':
        t = f"直接母词：拆分 {d['oldG']} → {d['G']}（母词 {d['parent']} 已补在第 {P2[w][1]} 行，各部分解释写“见 {d['parent']}”）；组合列第一行改成母词加最后一个后缀的等式，词性变化只写这个后缀{d.get('extra', '')}"
    elif d['kind'] == 'inline':
        t = f"直接母词：拆分 {d['oldG']} → {d['G']}（{d['parent']} 是{d['why']}，不单独成行，各部分解释里讲清它怎么来）；组合列第一行改成母词加最后一个后缀的等式"
    else:
        t = f"直接母词：拆分 {d['oldG']} → {d['G']}（-ic、-al 合成 -ical 一个后缀，和 historical、psychological 一样）；组合列只写一个等式"
    c.value = (c.value + '；' if c.value else '') + t
    fit_height(ws, n)
nt = o2n[R('tropical')]
ws.cell(nt, 16).value += f'；直接母词：tropic 已补在第 {P2["tropics"][1]} 行，tropic 一行改见 tropic'
for w in list(FIX) + ['tropical']:
    fit_height(ws, o2n[R(w)])

# ======================================================================== 五、用词规律一览（按全表重算）
norm = lambda t: re.sub(r'\s+', '', str(t or ''))
key_of = {norm(v[0]): k for k, v in PL.EX.items()}
use = collections.defaultdict(list)
for n in range(2, LAST + 1):
    w = str(ws.cell(n, 5).value)
    for t in C.parse_I(ws.cell(n, 9).value or '', w)['rules'].values():
        b = C.rule_body(t)
        k = key_of.get(b) or next((kk for kk, vv in PL.EX.items() if b.startswith(norm(vv[0]))), None)
        if k and w not in use[k]:
            use[k].append(w)
G = wb['用词规律一览']
rowsG = []
for rr in range(2, G.max_row + 1):
    if G.cell(rr, 2).value:
        rowsG.append([G.cell(rr, c).value for c in range(1, 7)])
diff = []
for x in rowsG:
    k = key_of.get(norm(x[1]))
    if k is None:
        print('一览里认不出的规律：', x[1]); continue
    if x[4] != len(use[k]):
        diff.append((x[1][:18], x[4], len(use[k])))
    x[4], x[5] = len(use[k]), '、'.join(use[k][:40])
print('用词规律一览 词数变化：', diff)
rowsG.sort(key=lambda x: -x[4])
for i, x in enumerate(rowsG, start=2):
    x[0] = i - 1
    for c in range(1, 7):
        G.cell(i, c).value = x[c - 1]

# ======================================================================== 六、整表核对记录、说明
Rk = wb['整表核对记录']
n0 = sum(1 for x in Rk.iter_rows(min_row=2, values_only=True) if x[0] is not None)
body = copy.copy(Rk.cell(2, 4)._style)
LOG = [('已修正', None, '几个后缀的词',
        '几个后缀的英语派生词，拆分从最早的词一路写下来（thought + less + ly），组合列要逐个写等式，学生得一步步推；中间那个词本身就是单词',
        '改用直接母词：补母词 15 行（thoughtless、breathless、aimless、fertilize、civilize、civilise、industrialize、urbanize、linguist、binocular、tropic、furnishing、crackle、sophisticate、containerize，放在派生词正上方），派生词改成“母词 + 最后一个后缀”、各部分解释写“见 X”；母词生僻、临时造或已废的 5 行（calendarize、mascotize、opinionate、sorcer、trashcape）不补行，在各部分解释里讲清；-ical 词 3 行写成 techn + ical、geology + ical、myth + ical。逐行见 P 列“直接母词：…”'),
       ('特殊（未改）', None, '几个后缀的词（外语里的构造）',
        '19 个词的中间一步只在拉丁语、希腊语、法语、意大利语里有，或是倒推、音变：statistic、scissors、against、dictionary、cultivate、fundamental、solidarity、nocturnal、legitimate、Australia、gasoline、vascular、tweezers、calculate、porcelain、broccoli、logistics、spaghetti、spontaneous',
        '保留逐个写的等式（复杂成分三步的老规矩）；scissor、tweezer 是从复数倒推出来的，不是母词'),
       ('已修正', None, '⏳ 待核查',
        f'113 行补出来的母词还没单独联网核对',
        f'逐行对照 etymonline 条目（2026 年 1 月的整站数据，52,126 条；thoughtless 等和网站现在的页面逐字一致）：{nver["✅"]} 行一致改 ✅，{nver["✏️"]} 行改 ✏️（词性变化写错）；M 列写依据、N 列写条目。逐行见 P 列“联网复核：…”'),
       ] + [('已修正', o2n[R(w)], w, FIX[w][0], FIX[w][1]) for w in FIX] + [
       ('特殊（未改）', None, '❓ 查无', 'unbelieve、air-draw、safe-shell 三行复核', '主要词典仍查不到（unbelieve 只见 misbelieve、disbelieve），照字面理解，保留 ❓；M 列末尾记“复核（2026-11）”')]
for k, (cat, rr, w, what, how) in enumerate(LOG):
    i = n0 + k + 2
    vals = [n0 + k + 1, cat, f'=HYPERLINK("#\'拆分结果\'!E{rr}","第 {rr} 行")' if rr else '—', w, what, how]
    for c, v in enumerate(vals, 1):
        cell = Rk.cell(i, c); cell.value = v; cell._style = copy.copy(body)
        cell.alignment = Alignment(wrap_text=True, vertical='top')
    if rr:
        Rk.cell(i, 3).font = Font(name='微软雅黑', size=10, color='0563C1', underline='single')
    Rk.cell(i, 2).fill = PatternFill('solid', start_color='E2EFDA' if cat == '已修正' else 'FFF2CC')
    Rk.row_dimensions[i].height = 17.25 * max(1, math.ceil(max(len(what), len(how)) / 38))
Rk.auto_filter.ref = f'A1:F{Rk.max_row}'
S = wb['说明']
old20 = S.cell(20, 2).value
S.cell(20, 2).value = old20.replace('（派生路线、几个后缀、第一行没有的本义）',
    '（派生路线、第一行没有的本义）；几个后缀的英语派生词，拆分用直接母词（thoughtlessly = thoughtless + ly，各部分解释写“见 thoughtless”），所以也只有一个后缀等式；中间一步只在外语里有的（dictionary、spaghetti）才逐个写')
assert S.cell(20, 2).value != old20
last = max(rr for rr in range(76, S.max_row + 1) if S.cell(rr, 1).value)
add = [('直接母词', '几个后缀的英语派生词改用直接母词（thoughtlessly = thoughtless + ly，不再写 thought + less + ly）：补母词 15 行（放在派生词正上方；tropic 成了本组第一行，【背景】随之上移），派生词改成“母词 + 最后一个后缀”、各部分解释写“见 X”；母词生僻或已废的 5 行在各部分解释里讲清母词；-ical 词 3 行写成 X + ical；外语里的构造 19 行保留逐个写的等式。逐行见 P 列“直接母词：…”。',
        f'=COUNTIF(拆分结果!$P$2:$P${LAST},"*直接母词*")'),
       ('待核查联网复核', f'⏳ 待核查 113 行逐行对照 etymonline：{nver["✅"]} 行 ✅ 一致，{nver["✏️"]} 行 ✏️ 已修正（tireless、mandate、senate、instinctive 的词性变化写错）；❓ 查无 3 行复核后仍保留。逐行见 P 列“联网复核：…”。',
        f'=COUNTIF(拆分结果!$P$2:$P${LAST},"*联网复核*")')]
for k, (a, b, d) in enumerate(add, start=1):
    rr = last + k
    for c in (1, 2, 3, 4):
        S.cell(rr, c)._style = copy.copy(S.cell(last, c)._style)
    S.cell(rr, 1).value, S.cell(rr, 2).value, S.cell(rr, 4).value = a, b, d
    S.merge_cells(f'B{rr}:C{rr}')
    S.row_dimensions[rr].height = S.row_dimensions[last].height
wb.save(OUT)
print('saved', OUT)

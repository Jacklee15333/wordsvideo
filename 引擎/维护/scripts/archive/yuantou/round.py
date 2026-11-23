"""源头词根轮（2026-11）的改表脚本，只作记录。用法：python3 round.py <源表.xlsx> <新表.xlsx>
一、派生词：拆分里冒充母词的、经法语变了样的英语词，换回这个词实际用的拉丁原形（popular：people + ar → popul + ar）。
二、外来基础词：同组在用源头词根、自己又变了样的，⑤ → ② 变体关联，拆分写 people ← popul，词根列补源头词根。
三、顺带：major、minor 的 -or 是比较级，词性变化写错。"""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
from fixlib import Book
import cols as C

SRC, OUT = sys.argv[1], sys.argv[2]
b = Book(SRC, tag='源头词根')
ws = b.ws
edited = []

def get(r, c): return ws.cell(r, c).value
def put(r, c, v): ws.cell(r, c).value = v
def chk(r, w):
    assert str(get(r, C.WORD)) == w, (r, w, get(r, C.WORD))
def first_line(r): return str(get(r, C.COMBO)).split('\n')[0]
def set_first(r, new):
    L = str(get(r, C.COMBO)).split('\n'); L[0] = new; put(r, C.COMBO, '\n'.join(L))
def drop_sound(r, prefix):
    L = [l for l in str(get(r, C.SOUND) or '').split('\n') if l.strip() and not l.startswith(prefix)]
    put(r, C.SOUND, '\n'.join(L) if L else None)

# ---------------- 一、派生词 ----------------
# (行, 单词, 新拆分, 冒充母词的英语词, 源头词根, 词根列, 第一行：(旧, 新) 或整行, 音变：('drop', 前缀) / ('set', 新) / None, 为什么, 其他列)
A = [
 (18, 'popular', 'popul + ar', 'people', 'popul', 'popul-：人民、民众（拉丁语 populus“一国的全体人民”）；people 是它经法语变来的样子（见 people）',
  ('people（人民）', 'popul（人民）'), ('drop', 'people → '), 'popular 直接来自拉丁语 popularis，people 是 populus 经法语变来的样子，不是它的母词', {}),
 (25, 'populate', 'popul + ate', 'people', 'popul', 'popul-：人、人民（拉丁语 populus；people 是它经法语变来的样子，见 people）',
  ('people（人）', 'popul（人）'), ('set', '整词来自中世纪拉丁语 populatus（populare“使有人居住”的“被…了的”形式），-atus 在英语里写成 -ate'),
  'populate 来自中世纪拉丁语 populatus，用的是拉丁原形 popul-', {}),
 (27, 'populous', 'popul + ous', 'people', 'popul', 'popul-：人民（拉丁语 populus；people 是它经法语变来的样子，见 people）',
  ('people（人）', 'popul（人）'), ('drop', 'people → '), 'populous 来自后期拉丁语 populosus，用的是拉丁原形 popul-', {}),
 (100, 'majesty', 'maj + es + ty', 'major', 'maj', 'maj-：大（由词根 magn 变来：mag“大”，比较级早期写作 *magios，g 在 i 前弱化掉了；见 major）',
  '【构词逻辑】maj（大）+ es（更…）+ ty（…的性质、状态）=“更大、更高的那种气象”；词性变化（-ty）：形容词 → 名词', ('drop', 'major → '),
  'majesty 来自拉丁语 maiestas（maius“更大的”+ -tas），不是英语 major 加 -ty；和 major（maj + or）一样从词根 maj- 讲起',
  {'M_pre': '-es-：表示“更…”的比较级成分（来自拉丁语比较级词尾：中性 maius“更大的”里是 -ius，造 maiestas 时是 -es-；同 major 的 -or）'}),
 (1225, 'principal', 'princip + al', 'prince', 'princip', 'princip-：首领、拿头一份的人（拉丁语 princeps = prin“第一”+ cip“拿”，变格时写作 princip-）；prince 是它经法语缩短的样子（见 prince）',
  ('prince（首领）', 'princip（首领）'), ('drop', 'prince → '), 'principal 来自拉丁语 principalis，用的是 princeps 的词干 princip-；prince 是 princeps 经法语缩短的样子，不是它的母词', {}),
 (1226, 'principle', 'princip + le(=ium)', 'prince', 'princip', 'princip-：开端、第一（拉丁语 principium“开端、起源”，来自 princeps“拿头一份的、第一的”= prin“第一”+ cip“拿”）；prince 是 princeps 经法语缩短的样子（见 prince）',
  ('prince（第一、开端）', 'princip（第一、开端）'), ('drop', 'prince → '), 'principle 来自拉丁语 principium，用的是词干 princip-', {}),
 (1363, 'regular', 'regul + ar', 'rule', 'regul', 'regul-：规矩、直木条（拉丁语 regula“直尺、规矩”）；rule 是它经法语磨短的样子（见 rule）',
  ('rule（规矩）', 'regul（规矩）'), ('drop', 'rule → '), 'regular 直接来自拉丁语 regularis，用的是 regula 的原形 regul-；rule 是 regula 经法语磨短的样子', {}),
 (1371, 'regulate', 'regul + ate', 'rule', 'regul', 'regul-：规矩（拉丁语 regula；rule 是它经法语磨短的样子，见 rule）',
  ('rule（规矩）', 'regul（规矩）'), ('set', '整词来自晚期拉丁语 regulatus（regulare“按规矩调整”的“被…了的”形式），-atus 在英语里写成 -ate'),
  'regulate 来自晚期拉丁语 regulatus，用的是 regul-', {}),
 (2172, 'ordinary', 'ordin + ary', 'order', 'ordin', 'ordin-：次序、行列（拉丁语 ordo，变格时写作 ordin-，属格 ordinis）；order 是它经法语变来的样子（见 order）\n整个词经古法语来自拉丁语 ordinarius“照常的、按规矩来的”',
  ('order（次序）', 'ordin（次序）'), ('drop', 'order → '), 'ordinary 来自拉丁语 ordinarius，用的是 ordo 的词干 ordin-；order 是 ordo 经法语变来的样子', {}),
 (2175, 'coordinate', 'co + ordin + ate', 'order', 'ordin', '-ordin-：次序、等级（拉丁语 ordo，变格时写作 ordin-；order 是它经法语变来的样子，见 order）\n整个词来自中世纪拉丁语 coordinare“排列、安排”',
  ('order（次序、等级）', 'ordin（次序、等级）'), ('drop', 'order → '), 'coordinate 来自中世纪拉丁语 coordinare，用的是 ordin-', {}),
 (4261, 'determine', 'de + termin + e', 'term', 'termin', '-termin-：划定边界（拉丁语 terminare，来自 terminus“界石”）；term 是 terminus 经法语磨短的样子（见 term）',
  ('term（划定边界）', 'termin（划定边界）'), ('set', '整词经古法语 determiner 来自拉丁语 determinare“划定界限”'), 'determine 来自拉丁语 determinare，用的是 termin-', {}),
 (4265, 'terminal', 'termin + al', 'term', 'termin', 'termin-：边界、终点（拉丁语 terminus）；term 是它经法语磨短的样子（见 term）',
  ('term（终点、边界）', 'termin（终点、边界）'), ('set', '整词来自拉丁语 terminalis“边界的、终点的”'), 'terminal 来自拉丁语 terminalis，用的是 termin-', {}),
 (3490, 'imagine', 'imagin + e', 'image', 'imagin', 'imagin-：像（拉丁语 imago，变格时写作 imagin-，属格 imaginis）；image 是它经法语磨短的样子（见 image）',
  ('image（像）', 'imagin（像）'), ('drop', 'image → '), 'imagine 来自拉丁语 imaginari，用的是 imago 的词干 imagin-；image 是 imago 经法语磨短的样子', {}),
 (3497, 'imaginal', 'imagin + al', 'image', 'imagin', 'imagin-：像（拉丁语 imago，变格时写作 imagin-；image 是它经法语磨短的样子，见 image）',
  ('image（像）', 'imagin（像）'), ('drop', 'image → '), 'imaginal 用的是 imago 的词干 imagin-', {}),
 (2640, 'material', 'materi + al', 'matter', 'materi', 'materi-：材料、物质（拉丁语 materia 去掉词尾 a）；matter 是它经法语变来的样子（见 matter）\n合起来是晚期拉丁语 materialis“属于物质的”',
  ('matter（物质、材料）', 'materi（物质、材料）'), ('drop', 'matter → '), 'material 来自晚期拉丁语 materialis，用的是 materi-；matter 是 materia 经法语变来的样子', {}),
 (4009, 'floral', 'flor + al', 'flower', 'flor', 'flor-：花（拉丁语 flos，变格时写作 flor-，s 变成 r）；flower 是它经法语变来的样子（见 flower）\n为什么是 flor 不是 flower：整个词是从法语 floral（← 拉丁语 floralis）借来的，用的是拉丁词干 flor-，不是英语的 flower',
  ('flower（花）', 'flor（花）'), ('drop', 'flower → '), 'floral 来自拉丁语 floralis，用的是 flor-', {}),
 (8186, 'criminal', 'crimin + al', 'crime', 'crimin', 'crimin-：罪、罪行（拉丁语 crimen，加后缀时写作 crimin-）；crime 是它经法语磨短的样子（见 crime）',
  ('crime（罪、罪行）', 'crimin（罪、罪行）'), None, 'criminal 来自拉丁语 criminalis，用的是 crimen 的词干 crimin-', {}),
 (4783, 'hospital', 'hospit + al', 'host', 'hospit', 'hospit-：客人；主人（拉丁语 hospes，变格时写作 hospit-，属格 hospitis）——拉丁语里同一个词既指“客”也指“主”（同 hospitality 好客）；host 是它经法语磨短的样子，中间的 pi 脱落（见 host）',
  ('host（客人）', 'hospit（客人）'), ('drop', 'host → '), 'hospital 来自中世纪拉丁语 hospitale，用的是 hospes 的词干 hospit-；host 是 hospes 经法语磨短的样子', {}),
 (2386, 'humility', 'humil + ity', 'humble', 'humil', 'humil-：低的、贴着地面的（拉丁语 humilis，来自 humus“地、泥土”）；humble 是它经法语走了样的形式（见 humble）',
  ('humble（谦逊的、谦卑的）', 'humil（谦逊的、谦卑的）'), None, 'humility 来自拉丁语 humilitas，用的是 humilis 的原形 humil-；humble 是 humilis 经法语走了样的形式', {}),
 (3655, 'prejudice', 'pre + judic + e', 'judge', 'judic', '-judic-：判断（拉丁语 iudicium“审判、判断”，来自 iudex“法官”= ius“法”+ dic“说”，变格时写作 iudic-）；judge 是它经法语变来的样子，dge 就是 dic（见 judge）',
  ('judge（判断）', 'judic（判断）'), ('drop', 'judge → '), 'prejudice 来自拉丁语 praeiudicium，用的是 iudic-；judge 是 iudex 经法语变来的样子', {}),
 (4639, 'poverty', 'pover + ty', 'poor', 'pover', 'pover-：穷（= 拉丁语 pauper“穷的”，到古法语成了 povre：au 变成 o，两元音间的 p 弱化成 v）；poor 也来自 povre，又丢了 v（见 poor）',
  ('poor（贫穷的）', 'pover（贫穷的）'), None, 'poverty 来自古法语 poverte（← 拉丁语 paupertas），用的是 povre 的样子 pover-；poor 是 povre 又丢了 v 的样子', {}),
 (1941, 'imperial', 'im + peri + al', 'empire', 'peri', '-peri-：号令、统辖（拉丁语 imperium“命令、最高权力；帝国”，来自 imperare“下令”= in + parare“备好”，见 emperor）；empire 是 imperium 经法语变来的样子（见 empire）',
  '【构词逻辑】im（向、对着）+ peri（号令、统辖）+ al（…的）=“属于帝国、属于皇帝的”；词性变化（-al）：名词 → 形容词', ('drop', 'empire → '),
  'imperial 来自拉丁语 imperialis，用的是 imperium 的样子 im + peri；empire 是 imperium 经法语变来的样子',
  {'J': 'im-：= in-“向、对着”（拉丁语 in“在…里、进入”，和英语 in 同源，见 in）\n为什么是 im- 不是 em-：empire 走的是法语的路（im 变成 em）；imperial 在古法语里 imperial、emperial 两种拼法都有，英语用的是照拉丁语 imperialis 拼的 im-'}),
 (1163, 'suspicion', 'su(=sub) + spic + ion', 'suspect', 'spic', '-spic-：看（由词根 spec 变来：拉丁语 specere 进了复合词写成 -spicere，e 弱化成 i）；suspicere“从下往上偷看 → 怀疑”，suspect 是它“看过了”的形式（见 suspect）',
  '【构词逻辑】su（从下往上）+ spic（看）+ ion（…这件事）=“从下往上偷看这件事”= 怀疑；词性变化（-ion）：动词 → 名词',
  ('set', '整词经英法语 suspeciun 来自拉丁语 suspicionem“怀疑”（suspicere 的名词）；suspect 来自 suspicere 的“被…了的”形式 suspectus'),
  'suspicion 来自拉丁语 suspicio，是 suspicere 的名词，不是由 suspect 加 -ion（那样会是 suspection）；suspect 是 suspicere 的“被…了的”形式',
  {'J': 'su-：= sub-“在下面”（来自拉丁语 sub“在下面”，f 前写成 suf-，p 前写成 sup-；在 s 前 b 干脆掉了，写成 su-；同 subway 地铁）；这里是“从下面往上”'}),
 (2155, 'debit', 'de + b(=hab) + it', 'debt', 'b', '-b-：= hab“拿着”（拉丁语 habere；de + habere 缩成 debere“欠”，b 就是 hab 剩下的）；debt 是 debitum 经法语磨短的样子，b 是后来照拉丁语补回去的（见 debt）',
  '【构词逻辑】de（离开）+ b（拿着）+ it（被…了的）=“被欠着的（一笔）”；词性变化（-it）：变成名词', ('drop', 'debt → '),
  'debit 直接来自拉丁语 debitum，和 debt（de + b + t）同一个拆法；debt 是 debitum 经法语磨短的样子，不是 debit 的母词',
  {'J': 'de-：“离开”（拉丁语 de-，同 depart 离开）'}),
]

for rn, w, split, ow, root, K, n1, snd, why, extra in A:
    chk(rn, w)
    old = get(rn, C.SPLIT)
    put(rn, C.SPLIT, split)
    put(rn, C.ROOT, K)
    put(rn, C.WPART, '-')
    if 'J' in extra: put(rn, C.PRE, extra['J'])
    if 'M_pre' in extra: put(rn, C.SUF, extra['M_pre'] + '\n' + str(get(rn, C.SUF)))
    f = first_line(rn)
    if isinstance(n1, tuple):
        assert n1[0] in f, (w, f); set_first(rn, f.replace(n1[0], n1[1], 1))
    else:
        set_first(rn, n1)
    if snd and snd[0] == 'drop': drop_sound(rn, snd[1])
    elif snd and snd[0] == 'set': put(rn, C.SOUND, snd[1])
    b.note(rn, f'拆分 {old} → {split}（{why}）；单词部分的 {ow} 换成源头词根 {root}-')
    edited.append(rn)

# ---------------- 二、外来基础词 ----------------
# (行, 单词, 源头词根, 词根列, 第一行里括号中的路线)
Bs = [
 (17, 'people', 'popul', 'popul-：人民、民众（拉丁语 populus“一国的全体人民”，来源不明，有伊特鲁里亚语一说）；popular、populate、populous 保留了这个写法', '拉丁语 populus → 古法语 pople / peuple → people'),
 (1361, 'rule', 'regul', 'regul-：直木条、规矩（拉丁语 regula，出自 regere“使直、引导”）；regular、regulate 保留了这个写法', '拉丁语 regula → 古法语 riule / reule → rule'),
 (2167, 'order', 'ordin', 'ordin-：一排、次序（拉丁语 ordo，变格时写作 ordin-，原指织布机上的一排经线）；ordinary、coordinate 保留了这个写法', '拉丁语 ordo，变格写作 ordin- → 古法语 ordre → order'),
 (4256, 'term', 'termin', 'termin-：界石、边界、终点（拉丁语 terminus）；determine、terminal 保留了这个写法', '拉丁语 terminus → 古法语 terme → term'),
 (3495, 'image', 'imagin', 'imagin-：仿出来的像（拉丁语 imago，变格时写作 imagin-）；imagine、imaginal 保留了这个写法', '拉丁语 imago，变格写作 imagin- → 古法语 image'),
 (2639, 'matter', 'materi', 'materi-：造东西用的材料（拉丁语 materia）；material 保留了这个写法', '拉丁语 materia → 古法语 matere → matter'),
 (4007, 'flower', 'flor', 'flor-：花（拉丁语 flos，变格时写作 flor-）；floral 保留了这个写法，flourish 的 flour- 也是它', '拉丁语 flos，变格写作 flor- → 古法语 flor / flour → flower'),
 (8185, 'crime', 'crimin', 'crimin-：控告、罪行（拉丁语 crimen，变格时写作 crimin-）；criminal 保留了这个写法', '拉丁语 crimen，变格写作 crimin- → 古法语 crimne → crime'),
 (4637, 'poor', 'pauper', 'pauper-：穷的、产出少的（拉丁语 pauper）；到古法语成了 povre，poverty 的 pover- 就是它', '拉丁语 pauper → 古法语 povre → poor'),
 (2787, 'voice', 'voc', 'voc-：声音、叫（拉丁语 vox，变格时写作 voc-，和 vocare“叫、喊”是一家）；vocation、vocabulary 保留了这个写法', '拉丁语 vox，变格写作 voc- → 古法语 voiz → voice'),
 (1114, 'city', 'civ', 'civ-：城里人、公民（拉丁语 civis；civitas“全体公民 → 城邦”）；civil 保留了这个写法', '拉丁语 civis“公民”→ civitas → 古法语 cite → city'),
 (2714, 'peace', 'pac', 'pac-：和约、安宁（拉丁语 pax，变格时写作 pac-）；Pacific 保留了这个写法', '拉丁语 pax，变格写作 pac- → 古法语 pais → peace'),
 (1688, 'sound', 'son', 'son-：声音（拉丁语 sonus）；sonic、resonate、consonant 保留了这个写法', '拉丁语 sonus → 古法语 son → 中古英语 soun → sound'),
 (2542, 'clear', 'clar', 'clar-：响亮的、明亮的（拉丁语 clarus）；clarify、clarity 保留了这个写法', '拉丁语 clarus → 古法语 cler → clear'),
 (1465, 'save', 'salv', 'salv-：完好的、安全的（拉丁语 salvus，salvare“使安全”）；salvage、salvation 保留了这个写法', '拉丁语 salvare → 古法语 sauver → save'),
 (3299, 'cross', 'cruc', 'cruc-：木桩、十字架（拉丁语 crux，变格时写作 cruc-）；crucial 保留了这个写法', '拉丁语 crux，变格写作 cruc- → 古爱尔兰语 cros → 北欧语 kross → cross'),
 (2879, 'waste', 'vast', 'vast-：空的、荒凉的（拉丁语 vastus，vastare“使荒芜”）；vast、devastate 保留了这个写法', '拉丁语 vastare → 北部古法语 waster → waste'),
 (2726, 'grace', 'grat', 'grat-：令人喜欢的；感激的（拉丁语 gratus，名词 gratia“恩惠、好意”）；gratitude、grateful 保留了这个写法', '拉丁语 gratia → 古法语 grace'),
 (2893, 'mount', 'mont', 'mont-：山（拉丁语 mons，变格时写作 mont-）；mountain 的 mount- 就是它（o 在英语里写成 ou）', '拉丁语 mons，变格写作 mont- → 民间拉丁语 *montare → 古法语 monter → mount'),
 (3569, 'duke', 'duc', 'duc-：领着走（拉丁语 ducere；dux“领头的人”，变格时写作 duc-）；ducat、educate 保留了这个写法', '拉丁语 dux，变格写作 duc- → 古法语 duc → duke'),
 (4067, 'letter', 'liter', 'liter-：字母（拉丁语 littera）；literal、literature 保留了这个写法', '拉丁语 littera → 古法语 letre → letter'),
 (4557, 'prove', 'prob', 'prob-：检验、证明（拉丁语 probare，← probus“好的”）；probable 保留了这个写法', '拉丁语 probare → 古法语 prover → prove'),
 (7819, 'brief', 'brev', 'brev-：短的（拉丁语 brevis）；abbreviate 保留了这个写法', '拉丁语 brevis → 古法语 bref → brief'),
 (7595, 'wine', 'vin', 'vin-：葡萄酒（拉丁语 vinum）；vintage、vinegar 保留了这个写法', None),
 (3692, 'reason', 'rat', 'rat-：算、想（拉丁语 reri“计算、思考”的“被…了的”形式 ratus；名词 ratio“计算 → 道理”，变格时写作 ration-）；ratio 保留了这个写法', '拉丁语 ratio，变格写作 ration- → 古法语 raison → reason'),
 (3732, 'paint', 'pict', 'pict-：画（拉丁语 pingere“画、着色”的“被画了的”形式 pictus）；depict 保留了这个写法', '拉丁语 pictus，民间说 pinctus → 古法语 peint → paint'),
 (3963, 'chief', 'cap', 'cap-：头（拉丁语 caput，变格时写作 capit-）；capital 的 capit- 也是它', '拉丁语 caput → 俗拉丁语 *capum → 古法语 chief'),
 (4772, 'price', 'preci', 'preci-：价值、价钱（拉丁语 pretium，ti 后来写成 ci）；precious、appreciate 保留了这个写法', '拉丁语 pretium → 古法语 pris → price'),
 (4990, 'faith', 'fid', 'fid-：信任（拉丁语 fides“信任、信用”，fidere“信任”）；confident 保留了这个写法', '拉丁语 fides → 古法语 feid → faith'),
 (5808, 'nurse', 'nutri', 'nutri-：喂养（拉丁语 nutrire“喂奶、哺育”，nutrix“奶妈”）；nutrition、nutrient 保留了这个写法', '拉丁语 nutrix“奶妈”→ 古法语 norrice → nurse'),
 (7798, 'vain', 'van', 'van-：空的（拉丁语 vanus）；vanish 保留了这个写法', '拉丁语 vanus → 古法语 vain'),
 (7824, 'poison', 'pot', 'pot-：喝（拉丁语 potare“喝”，potio“饮料”）；potion 保留了这个写法', '拉丁语 potionem“饮料”→ 古法语 poison'),
 (6383, 'air', 'aer', 'aer-：空气、雾气（希腊语 aēr，拉丁语 aer）；aerial 保留了这个写法', '希腊语 aēr → 拉丁语 aer → 古法语 air'),
 (5762, 'lion', 'leo', 'leo-：狮子（拉丁语 leo，变格时写作 leon-，← 希腊语 leōn）；leopard 保留了这个写法', '拉丁语 leo，变格写作 leon- → 古法语 lion'),
 (881, 'round', 'rot', 'rot-：轮子（拉丁语 rota；rotundus“像轮子一样的、圆的”）；rotate、rotary 保留了这个写法', '拉丁语 rota“轮子”→ rotundus → 古法语 roont → round'),
 (591, 'place', 'plat', 'plat-：宽、平（希腊语 platys；拉丁语 platea“宽阔的大街”）；platform、plateau 的 plat- 同出 platys', '希腊语 platys“宽”→ 拉丁语 platea → 古法语 place'),
 (2222, 'course', 'curs', 'curs-：跑（拉丁语 currere“跑”，名词 cursus“奔跑；路线”）；cursive 保留了这个写法', '拉丁语 cursus → 古法语 cors → course'),
]
FIRST_OVERRIDE = {
 'duke': '【构词逻辑】duke 由源头词根 duc 变来（拉丁语 dux，变格写作 duc- → 古法语 duc → duke），可以理解成“领着大家走的人”（见 reduce 的【背景】）：',
 'wine': '【构词逻辑】wine 由源头词根 vin 变来，是拉丁语 vinum 的日耳曼读法（古典拉丁语 v 读 /w/，古英语借成 win；见 vine 的【背景】）：',
}
for rn, w, R, K, chain in Bs:
    chk(rn, w)
    assert str(get(rn, C.TYPE)).startswith('⑤') and get(rn, C.SPLIT) == '—', (w, get(rn, C.TYPE), get(rn, C.SPLIT))
    put(rn, C.TYPE, '② 变体关联')
    put(rn, C.SPLIT, f'{w} ← {R}')
    Ls = [l for l in str(get(rn, C.WPART) or '').split('\n') if l.strip()]
    own = [l for l in Ls if l.startswith(w + '：')]
    notes = [l for l in Ls if not l.startswith(w + '：')]
    assert len(own) == 1, (w, Ls)
    put(rn, C.WPART, own[0])
    put(rn, C.ROOT, '\n'.join([K] + notes))
    f = first_line(rn)
    if w in FIRST_OVERRIDE:
        new = FIRST_OVERRIDE[w]
    else:
        m = re.match(r'^【构词逻辑】' + re.escape(w) + r' 本身(?:不再拆分|就是最小单位)，(.*)$', f)
        assert m, (w, f)
        new = f'【构词逻辑】{w} 由源头词根 {R} 变来（{chain}），{m.group(1)}'
    set_first(rn, new)
    b.note(rn, f'基础词改为变体关联（⑤ → ②），拆分 — → {w} ← {R}，词根列补源头词根 {R}-，组合列第一行写明由源头词根变来' + ('；讲来历的说明随词根挪到词根列' if notes else ''))
    edited.append(rn)

# ---------------- 三、顺带：-or 比较级的词性变化 ----------------
b.tag = '整表核对'
for rn, w in ((95, 'major'), (6603, 'minor')):
    chk(rn, w)
    f = first_line(rn); old = '词性变化（-or）：动词 → 名词（人或东西）'
    assert old in f; set_first(rn, f.replace(old, '词性变化（-or）：变成形容词'))
    b.note(rn, '-or 是比较级“更…的”，词性变化“动词 → 名词（人或东西）”改成“变成形容词”（同 junior、superior）')
    edited.append(rn)
m = str(get(6603, C.SUF)); o = '（来自拉丁语表示“做…的人”的词尾 -or，经古法语进入英语；'
assert o in m; put(6603, C.SUF, m.replace(o, '（来自拉丁语比较级词尾 -ior / -or；'))
b.note(6603, '-or 的来源括号写成了“做…的人”的 -or，改成比较级词尾')
b.tag = '源头词根'

# ---------------- 整表核对记录 ----------------
b.log += [
 ('已修正', None, '源头词根（派生词）',
  '24 个词的拆分把经法语变了样的英语词当成母词：popular = people + ar、regular = rule + ar、terminal = term + al、hospital = host + al、imagine = image + e……这些词其实直接来自拉丁语，用的是拉丁原形（popul-、regul-、termin-、hospit-、imagin-），英语词只是同一个词根经法语变来的样子（早先“母词替换”那一轮换上去的）',
  '拆分改回源头词根（popul + ar），词根列写“popul-：人民、民众（拉丁语 populus）；people 是它经法语变来的样子（见 people）”，单词部分写“-”；组合列第一行的公式、音变列里“people → popul-”这类旧说明跟着改。在完整单词上加缀的（popularity = popular + ity、population = populate + ion）不改。逐行见 U 列“源头词根：…”'),
 ('已修正', None, '源头词根（基础词）',
  '37 个外来基础词，同组的词都在用源头词根，它自己却算成“本身就是最小单位”：people（popul-）、rule（regul-）、order（ordin-）、voice（voc-）、city（civ-）、peace（pac-）……音变列其实已经讲清了字母、读音怎么变',
  '类型 ⑤ 基础词 → ② 变体关联，拆分写 people ← popul，词根列补源头词根（意思、拉丁原词、同组哪些词保留了这个写法），组合列第一行写“people 由源头词根 popul 变来（拉丁语 populus → 古法语 pople / peuple → people）”；单词部分只留这个词自己的来历说明'),
 ('特殊（未改）', None, '源头词根（没改的）',
  '这几类没改：只差一个字母、一眼看得出的（community / common、exemplary / example、scholar / school、technician / technique、reveal / veil、reconcile / council）；-cle 和 -cul- 固定互换的（circular、particular、spectacular，同 -ble / -bil-）；英语词本身就是拉丁词根原形的（parcel / part、inert / art、degree / grade、plural / plus、prince / prime）；在法语里就这样组成的（achieve、dessert、align、restaurant）；英语本族词的元音变化（strength、only、birth、holy）；动词和它的名词（decide / decision、destroy / destruction）；已经用 ≈ 挂到同组词上的 ②（host ≈ hospital、mayor ≈ major）',
  '保留；要改时照这一轮的写法改'),
 ('已修正', 95, 'major',
  'major、minor 的 -or 是比较级“更…的”，组合列词性变化却写成“动词 → 名词（人或东西）”；minor 后缀来源括号也写成了“做…的人”的 -or',
  '词性变化改成“变成形容词”（同 junior、superior），minor 的来源改成“来自拉丁语比较级词尾 -ior / -or”'),
]

# ---------------- 说明 ----------------
S = b.wb['说明']
def find_row(a, bstart=None):
    for r in range(1, S.max_row + 1):
        if S.cell(r, 1).value == a and (bstart is None or str(S.cell(r, 2).value or '').startswith(bstart)):
            return r
    raise KeyError(a)
r = find_row('② 变体关联', '拆不干净')
v = S.cell(r, 2).value; o = '例：popular = popul(=people) + ar'; assert o in v
S.cell(r, 2).value = v.replace(o, '例：made ← maked、mayor ≈ major；外来的基础词，同组在用源头词根、自己经法语又变了样的，挂到源头词根上：people ← popul（词根 popul- 写在 K 列）')
r = find_row('⑤ 基础词', '本身就是最小单位')
v = S.cell(r, 2).value; o = '例：make、people（解释写在 L 列「单词部分」）'; assert o in v
S.cell(r, 2).value = v.replace(o, '例：make、pop（解释写在 L 列「单词部分」）；外来的、同组又在用源头词根的（people、voice）写成 ② 变体关联')
r = find_row('前缀、词根、单词部分、后缀')
S.cell(r, 2).value = S.cell(r, 2).value + '经法语变了样的英语词不冒充母词：popular 写 popul + ar（K 列“popul-：…；people 是它经法语变来的样子”），不写 people + ar；在完整单词上加缀的照旧写单词（popularity = popular + ity）。'
r = find_row('I 拆分')
v = S.cell(r, 2).value; o = '② 常写 X ← Y 或 X ≈ Y'; assert o in v
S.cell(r, 2).value = v.replace(o, '② 常写 X ← Y 或 X ≈ Y（外来基础词挂到源头词根上：people ← popul）')
r0 = find_row('单词列')
import copy
rn = S.max_row + 1 if r0 == S.max_row else None
assert rn, '「单词列」不是最后一行'
for c in range(1, 5):
    S.cell(rn, c)._style = copy.copy(S.cell(r0, c)._style)
S.cell(rn, 1).value = '源头词根'
S.cell(rn, 2).value = ('拆分里冒充母词的、经法语变了样的英语词换回源头词根：popular、regular、terminal、hospital、imagine 等 24 个词改成 popul + ar、regul + ar、termin + al……（词根列写“people 是它经法语变来的样子”）；'
                       '同组在用源头词根的 37 个外来基础词由 ⑤ 改成 ② 变体关联，拆分写 people ← popul，词根列补源头词根（voice ← voc、city ← civ、rule ← regul……）。在完整单词上加缀的（popularity = popular + ity）不改。顺带改正 major、minor 的词性变化。逐行见 U 列“源头词根：…”。')
S.cell(rn, 4).value = '=COUNTIF(拆分结果!$U$2:$U$9294,"*源头词根*")'
S.row_dimensions[rn].height = S.row_dimensions[r0].height

for r in set(edited):
    b._fit(r)
b.save(OUT)
print('改了', len(set(edited)), '行')

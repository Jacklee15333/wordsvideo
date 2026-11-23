# -*- coding: utf-8 -*-
"""词根的“形态”（2026-11 词根形态轮，project_rules.md 第 107–112 条）里，不是拉丁语动词的 46 个词根族（名词、形容词、希腊语、法语、英语本族……）。
拉丁语动词的 57 族不在这里：它们的三个样子照 dongbian_data.py 的 VERB 自动排（原形 / 过去式 / 过去分词）。
NV[(组号, 词根)] = dict(src=来源（词根后面括号里那句）, rows=[形态, …])
  形态 = dict(k=形态的名字, en=英语里的写法, s=来源和变化（写了“去掉词尾 -xx”的，视频演示把词尾去掉）, sp=[归这一行的写法…], use=没有例词时写的话)
  · 名字：名词用“原形 / 所有格”（像英语的 foot → foot's：拉丁语名词接词尾时才露出词根，pes → pedis → ped）；
    形容词用“原级 / 比较级 / 最高级”（像英语的 good → better → best）；希腊语用“原形 / 名词 / …”；别的照实写（经法语、带连接元音、双写……）。
  · 分工那句话里讲到某个写法的分句，归到 sp 里有它的那一行；讲到词根本身的归 en 是词根的那一行；都没有的归第一行。"""

NV = {
 (1401, 'Olymp'): dict(src='来自希腊语地名 Olympia“奥林匹亚”', rows=[
   dict(k='原形', en='Olymp', s='地名 Olympia 去掉词尾 -ia', sp=['Olymp']),
   dict(k='带地名里的元音', en='Olympi', s='留着地名里的 i，只去掉词尾 -a', sp=['Olympi'])]),
 (1017, 'ann'): dict(src='来自拉丁语名词 annus“年”', rows=[
   dict(k='原形', en='ann', s='来自拉丁语原形 annus“年”，去掉词尾 -us', sp=['ann']),
   dict(k='所有格', en='anni', s='所有格 anni“年的”，词尾 i 留着接别的词根', sp=['anni']),
   dict(k='形容词', en='annu', s='来自形容词 annuus“每年的”，去掉词尾 -us', sp=['annu'])]),
 (276, 'ante'): dict(src='来自拉丁语介词 ante“在前”', rows=[
   dict(k='原样', en='ante', s='拉丁语介词 ante 原样', sp=['ante'], use='表里的词都不用原样'),
   dict(k='经法语', en='an', s='经法语传进英语，磨成了几种样子', sp=['anci', 'an', 'vant', 'vance'])]),
 (912, 'batt'): dict(src='来自拉丁语动词 battuere“打”', rows=[
   dict(k='原形', en='batt', s='来自拉丁语原形 battuere“打”（口语写 battere），去掉词尾 -ere', sp=['batt']),
   dict(k='经法语', en='bat', s='经法语传进英语，只剩一个 t', sp=['bat', 'bate'])]),
 (1966, 'cann'): dict(src='来自拉丁语名词 canna“芦苇、管子”', rows=[
   dict(k='原形', en='cann', s='来自拉丁语原形 canna“芦苇、管子”，去掉词尾 -a', sp=['cann']),
   dict(k='经西班牙语', en='cany', s='nn 变成 ñ，英语改拼成 ny', sp=['cany'])]),
 (599, 'capit'): dict(src='来自拉丁语名词 caput“头”', rows=[
   dict(k='原形', en='caput', s='拉丁语名词 caput“头”单说时的样子', sp=[], use='英语里不单用'),
   dict(k='所有格', en='capit', s='来自所有格 capitis“头的”，去掉词尾 -is', sp=['capit', 'cipit', 'capt'])]),
 (692, 'chem'): dict(src='来自炼金术 alchemy（希腊语 khēmeia 经阿拉伯语传来）', rows=[
   dict(k='原形', en='chem', s='alchemy 去掉前面的 al（阿拉伯语的“这个”），再去掉词尾 -y', sp=['chem']),
   dict(k='名词', en='chemy', s='带着名词词尾 -y', sp=['chemy'])]),
 (348, 'circ'): dict(src='来自拉丁语名词 circus“圈、环”', rows=[
   dict(k='原形', en='circ', s='来自拉丁语原形 circus“圈、环”，去掉词尾 -us', sp=['circ']),
   dict(k='当介词', en='circum', s='它的另一种格 circum，当“绕着”用', sp=['circum'])]),
 (591, 'cli'): dict(src='来自希腊语动词 klinein“倾斜”', rows=[
   dict(k='原形', en='clin', s='来自希腊语原形 klinein“倾斜”，去掉词尾 -ein', sp=['clin']),
   dict(k='名词', en='cli', s='来自名词 klima“斜坡、地带”，去掉词尾 -ma', sp=['cli'])]),
 (1925, 'corp'): dict(src='来自拉丁语名词 corpus“身体”', rows=[
   dict(k='原形', en='corp', s='来自拉丁语原形 corpus“身体”，去掉词尾 -us', sp=['corp', 'cors']),
   dict(k='所有格', en='corpor', s='来自所有格 corporis“身体的”，去掉词尾 -is', sp=['corpor'])]),
 (1113, 'cri'): dict(src='来自希腊语动词 krinein“分辨”', rows=[
   dict(k='原形', en='cri', s='来自希腊语原形 krinein“分辨”，去掉词尾 -nein', sp=['cri']),
   dict(k='名词', en='crit', s='来自名词 kritēs“判断的人”，去掉词尾 -ēs', sp=['crit'])]),
 (846, 'dra'): dict(src='来自希腊语动词 dran“做”', rows=[
   dict(k='原形', en='dra', s='来自希腊语原形 dran“做”，去掉词尾 -n', sp=['dra']),
   dict(k='“做了的”', en='drast', s='来自 drastos“做了的”，去掉词尾 -os', sp=['drast'])]),
 (671, 'dyna'): dict(src='来自希腊语动词 dynasthai“能够”', rows=[
   dict(k='原形', en='dyna', s='来自希腊语原形 dynasthai“能够”，去掉词尾 -sthai', sp=['dyna'], use='表里的词都用下面两个名词'),
   dict(k='名词', en='dynam', s='来自名词 dynamis“力量”，去掉词尾 -is', sp=['dynam']),
   dict(k='名词', en='dynast', s='来自名词 dynastēs“统治者”，去掉词尾 -ēs', sp=['dynast'])]),
 (541, 'fid'): dict(src='来自拉丁语动词 fidere“信任”', rows=[
   dict(k='原形', en='fid', s='来自拉丁语原形 fidere“信任”，去掉词尾 -ere', sp=['fid']),
   dict(k='经法语', en='fy', s='经法语磨掉了 d', sp=['fy'])]),
 (478, 'gen'): dict(src='来自拉丁语名词 genus“种、族”', rows=[
   dict(k='原形', en='gen', s='来自拉丁语原形 genus“种、族”，去掉词尾 -us', sp=['gen', 'gine']),
   dict(k='所有格', en='gener', s='来自所有格 generis“种族的”，去掉词尾 -is', sp=['gener']),
   dict(k='另一个名词', en='gent', s='来自名词 gens“氏族”的所有格 gentis，去掉词尾 -is', sp=['gent'])]),
 (95, 'gno'): dict(src='来自希腊语动词 gignōskein“认识”', rows=[
   dict(k='原形', en='gno', s='来自希腊语原形 gignōskein“认识”，去掉开头重复的 gi 和词尾 -skein', sp=['gno']),
   dict(k='名词', en='gnose', s='来自名词 gnōsis“认识”，英语去掉词尾 -is、加 e，倒推出动词', sp=['gnose'])]),
 (340, 'graph'): dict(src='来自希腊语动词 graphein“写、画”', rows=[
   dict(k='原形', en='graph', s='来自希腊语原形 graphein“写、画”，去掉词尾 -ein', sp=['graph', 'graphy']),
   dict(k='名词', en='gram', s='来自名词 gramma“写下来的东西”，去掉词尾 -ma', sp=['gram', 'gramm', 'gramme'])]),
 (221, 'grat'): dict(src='来自拉丁语形容词 gratus“令人愉快的、感激的”', rows=[
   dict(k='原级', en='grat', s='来自拉丁语原级 gratus“令人愉快的”，去掉词尾 -us', sp=['grat', 'grate', 'gree']),
   dict(k='动词', en='gratul', s='来自由它造的动词 gratulari“道贺”，去掉词尾 -ari', sp=['gratul'])]),
 (78, 'hap'): dict(src='来自古诺尔斯语名词 happ“运气”', rows=[
   dict(k='原样', en='hap', s='古诺尔斯语 happ 到英语里只写一个 p', sp=['hap', 'haps']),
   dict(k='双写', en='happ', s='后面接元音开头的后缀时 p 双写', sp=['happ'])]),
 (936, 'janu'): dict(src='来自拉丁语名词 ianua“门”', rows=[
   dict(k='原形', en='janu', s='来自拉丁语原形 ianua“门”，去掉词尾 -a，i 后来写成 j', sp=['janu']),
   dict(k='换连接元音', en='jani', s='后面接 -tor 时换成连接元音 i', sp=['jani'])]),
 (128, 'lief'): dict(src='来自古英语名词 gelēafa“信任”', rows=[
   dict(k='名词', en='lief', s='名词里的样子', sp=['lief']),
   dict(k='动词', en='lieve', s='变成动词时 f 变成 v，再加不发音的 e', sp=['lieve'])]),
 (373, 'liter'): dict(src='来自拉丁语名词 littera“字母”', rows=[
   dict(k='原形', en='liter', s='来自拉丁语原形 littera“字母”，去掉词尾 -a（英语写一个 t）', sp=['liter']),
   dict(k='形容词', en='literat', s='来自形容词 litteratus“有文字修养的”，去掉词尾 -us', sp=['literat'])]),
 (925, 'ly'): dict(src='来自希腊语动词 lyein“松开”', rows=[
   dict(k='原形', en='ly', s='来自希腊语原形 lyein“松开”，去掉词尾 -ein', sp=['ly']),
   dict(k='名词', en='lys', s='来自名词 lysis“松开、解开”，去掉词尾 -is', sp=['lyse', 'lyze'])]),
 (625, 'magn'): dict(src='来自拉丁语形容词 magnus“大的”', rows=[
   dict(k='原级', en='magn', s='来自拉丁语原级 magnus“大的”，去掉词尾 -us', sp=['magn', 'magni']),
   dict(k='比较级', en='maj', s='来自比较级 maior“更大的”，去掉词尾 -or，i 后来写成 j', sp=['maj', 'mas']),
   dict(k='最高级', en='maxim', s='来自最高级 maximus“最大的”，去掉词尾 -us', sp=['maxim'])]),
 (412, 'man'): dict(src='来自拉丁语名词 manus“手”', rows=[
   dict(k='原形', en='man', s='来自拉丁语原形 manus“手”，去掉词尾 -us', sp=['man', 'main', 'mani']),
   dict(k='带词干元音', en='manu', s='留着 manus 的 u，后面接别的成分', sp=['manu'])]),
 (528, 'merc'): dict(src='来自拉丁语名词 merx“货物”', rows=[
   dict(k='原形', en='merx', s='merx“货物”单说时的样子：merc 加 s，c 和 s 合写成 x', sp=[], use='英语里不单用'),
   dict(k='所有格', en='merc', s='来自所有格 mercis“货物的”，去掉词尾 -is', sp=['merc', 'merch', 'merce'])]),
 (656, 'morgen'): dict(src='来自古英语名词 morgen“早晨”', rows=[
   dict(k='原样', en='morgen', s='古英语原样', sp=['morgen'], use='今天不单用'),
   dict(k='缩短', en='morn', s='g 磨掉以后缩成 morn', sp=['morn'])]),
 (190, 'mun'): dict(src='来自拉丁语名词 munus“职责”', rows=[
   dict(k='原形', en='mun', s='来自拉丁语原形 munus“职责”，去掉词尾 -us', sp=['mun', 'mon', 'muni']),
   dict(k='形容词', en='mune', s='来自形容词 immunis“不用尽职责的”，去掉词尾 -is，加不发音的 e', sp=['mune'])]),
 (2436, 'ov'): dict(src='来自拉丁语动词 ovare“欢呼”', rows=[
   dict(k='原形', en='ov', s='来自拉丁语原形 ovare“欢呼”，去掉词尾 -are', sp=['ov'], use='表里的词用过去分词'),
   dict(k='过去分词', en='ovat', s='来自过去分词 ovatus“受过欢呼的”，去掉词尾 -us', sp=['ovat'])]),
 (423, 'patr'): dict(src='来自拉丁语名词 pater“父亲”', rows=[
   dict(k='原形', en='pater', s='拉丁语名词 pater“父亲”单说时的样子', sp=[], use='英语里不单用'),
   dict(k='所有格', en='patr', s='来自所有格 patris“父亲的”，去掉词尾 -is', sp=['patr']),
   dict(k='希腊语', en='patri', s='来自希腊语 patris“祖国”，去掉词尾 -s', sp=['patri'])]),
 (1085, 'ped'): dict(src='来自拉丁语名词 pes“脚”', rows=[
   dict(k='原形', en='pes', s='pes“脚”单说时的样子：ped 加 s，d 并掉了', sp=[], use='英语里不单用'),
   dict(k='所有格', en='ped', s='来自所有格 pedis“脚的”，去掉词尾 -is', sp=['ped', 'pion', 'pe']),
   dict(k='动词', en='pedit', s='来自动词 expedire 的过去分词 expeditus，去掉前缀 ex 和词尾 -us', sp=['pedit'])]),
 (696, 'phys'): dict(src='来自希腊语名词 physis“自然”', rows=[
   dict(k='原形', en='phys', s='来自希腊语原形 physis“自然”，去掉词尾 -is', sp=['phys']),
   dict(k='形容词', en='physic', s='来自形容词 physikos“自然的”，去掉词尾 -os', sp=['physic'])]),
 (381, 'plas'): dict(src='来自希腊语动词 plassein“塑造”', rows=[
   dict(k='原形', en='plas', s='来自希腊语原形 plassein“塑造”，去掉词尾 -sein', sp=['plas']),
   dict(k='“被塑成的”', en='plast', s='来自 plastos“被塑成的”，去掉词尾 -os', sp=['plast'])]),
 (1037, 'poli'): dict(src='来自希腊语名词 polis“城邦”', rows=[
   dict(k='原形', en='poli', s='来自希腊语原形 polis“城邦”，去掉词尾 -s', sp=['poli']),
   dict(k='名词', en='polit', s='来自名词 politēs“公民”，去掉词尾 -ēs', sp=['polit'])]),
 (672, 'quadr'): dict(src='来自拉丁语形容词 quadrus“四方的”', rows=[
   dict(k='原级', en='quadr', s='来自拉丁语原级 quadrus“四方的”，去掉词尾 -us', sp=['quadr']),
   dict(k='经法语', en='quare', s='经法语把 dr 磨成 r', sp=['quare'])]),
 (545, 'qual'): dict(src='来自拉丁语形容词 qualis“什么样的”', rows=[
   dict(k='原级', en='qual', s='来自拉丁语原级 qualis“什么样的”，去掉词尾 -is', sp=['qual']),
   dict(k='带连接元音', en='quali', s='后面接 -fy 时带连接元音 i', sp=['quali'])]),
 (1642, 'sacr'): dict(src='来自拉丁语形容词 sacer“神圣的”', rows=[
   dict(k='原级', en='sacer', s='sacer“神圣的”单说时的样子', sp=[], use='英语里不单用'),
   dict(k='变化时', en='sacr', s='一接词尾 e 就掉了（sacra、sacrum），去掉词尾 -a', sp=['sacr']),
   dict(k='带连接元音', en='sacri', s='后面接 -fice 时带连接元音 i', sp=['sacri'])]),
 (1118, 'satis'): dict(src='来自拉丁语副词 satis“足够”', rows=[
   dict(k='原样', en='satis', s='拉丁语副词 satis 原样', sp=['satis']),
   dict(k='动词', en='sati', s='来自由它造的动词 satiare“使饱足”，去掉词尾 -are', sp=['sati']),
   dict(k='经法语', en='set', s='经法语磨成 set', sp=['set'])]),
 (526, 'sider'): dict(src='来自拉丁语名词 sidus“星”', rows=[
   dict(k='原形', en='sidus', s='sidus“星”单说时的样子', sp=[], use='英语里不单用'),
   dict(k='所有格', en='sider', s='来自所有格 sideris“星的”，去掉词尾 -is', sp=['sider', 'sire'])]),
 (548, 'simil'): dict(src='来自拉丁语形容词 similis“像的”', rows=[
   dict(k='原级', en='simil', s='来自拉丁语原级 similis“像的”，去掉词尾 -is', sp=['simil', 'semble']),
   dict(k='动词', en='simul', s='来自由它造的动词 simulare“使相像”，去掉词尾 -are', sp=['simul'])]),
 (475, 'stell'): dict(src='来自拉丁语名词 stella“星”', rows=[
   dict(k='原形', en='stell', s='来自拉丁语原形 stella“星”，去掉词尾 -a', sp=['stell']),
   dict(k='形容词', en='stellat', s='来自形容词 stellatus“布满星星的”，去掉词尾 -us', sp=['stellat'])]),
 (149, 'techn'): dict(src='来自希腊语名词 technē“手艺”', rows=[
   dict(k='原形', en='techn', s='来自希腊语原形 technē“手艺”，去掉词尾 -ē', sp=['techn']),
   dict(k='带连接元音', en='techno', s='后面接别的词根时带连接元音 o', sp=['techno'])]),
 (2138, 'terra'): dict(src='来自拉丁语名词 terra“土地”', rows=[
   dict(k='原形', en='terra', s='拉丁语原形 terra“土地”原样', sp=['terra']),
   dict(k='接后缀时', en='terr', s='后面接后缀时去掉词尾 -a', sp=['terr']),
   dict(k='带连接元音', en='terri', s='换成连接元音 i', sp=['terri'])]),
 (861, 'thea'): dict(src='来自希腊语动词 theasthai“看”', rows=[
   dict(k='原形', en='thea', s='来自希腊语原形 theasthai“看”，去掉词尾 -sthai', sp=['thea']),
   dict(k='名词', en='theor', s='来自名词 theōros“旁观者”，去掉词尾 -os', sp=['theor'])]),
 (290, 'velop'): dict(src='来自古法语动词 voloper“包、裹”', rows=[
   dict(k='原形', en='velop', s='来自古法语 (des)veloper“包、裹”，去掉词尾 -er', sp=['velop']),
   dict(k='名词', en='velope', s='名词照法语多留一个 e', sp=['velope'])]),
 (554, 'ward'): dict(src='来自法兰克语动词 *wardōn“看守”', rows=[
   dict(k='原样', en='ward', s='北部法语保留着 w', sp=['ward']),
   dict(k='经中部法语', en='gard', s='进了中部法语，w 变成 g', sp=['gard'])]),
}

# -*- coding: utf-8 -*-
"""词缀的来历和记法（2026-11 词缀来历、记法轮，project_rules.md 第 73–75 条）。
前缀列、后缀列每一行的来源括号“（来源；同 例词）”里，来源那一段换成这个词缀统一的一句“来历”：哪种语言、原来是什么（单独的词 / 词尾）、什么意思、怎么进入英语。
  · 一个词缀（一种用法）一条来历，整句替换；同一行括号里的“同 例词”、讲写法的半句（在 c 前写成 ac-）、别的说明都照留
    （例词里自己还带词根的复杂词由 lizi.py 去掉，第 79 条；这里不管）。
  · 认得出的旧写法（head 正则，从这一段开头对）才换；认不出的行不动，列进清单（laili.py --dry 打印、改动清单「来历没换的」表）。
  · 来源一段也没有的行（fill=True 的词缀）：补进去——第一句末尾是“（同 …）”的插在括号最前面，不然在第一句后面加一个括号。
  · 视频（wordfilm.js 的 affixSource）靠括号里“经”字前面的语言名认来源：来历里“经…”之前只写来源语言本身，不要提别的语言名；英语本族的写“英语本来就有…”或“古英语…”。
  · 和英语简单词同源的，不写在来历里，写成那一行末尾的“；记：X ≈ Y（中文）：道理。音变：…”（MEMO，和词根的记法同一个写法，视频 5.1 起照读）。
条目字段：
  col   'pre' / 'suf'；labels 适用的标签；kind 后缀变成什么词性（读组合列第一行的“词性变化”；'*' 不管）；sense 'neg' / 'into'（in- / im- 两种意思）
  new   新来历；head 旧来源一段开头要对上的正则；drop 括号里要去掉的半句、整段（已经由新来历或记法讲了的：“和 like 是一家，见 like”）
  need / avoid  这一行（去掉身份、分工、记法）里要有 / 不能有的字，保证是这个意思
  fill  没有来源一段时补；fillx 补的时候接在后面的一段（re- 的“只用在词前，不单独成词”）
  top   这一行括号外面要去掉的、重复讲来历的整段（“-ly 本身来自古英语 lic…”）
  memo  MEMO 里的键（没有写 None）"""

def E(col, labels, new, head, **kw):
    d = dict(col=col, labels=set(labels.split()), new=new, head=head, kind='*', sense=None, drop=None, need=None, avoid=None,
             fill=False, fillx='', top=None, memo=None)
    d.update(kw)
    return d

ADV = '，本来是单独的一个词'
DROP_LIKE = r'和 like(?:“像”)? ?(?:是一家|同源|同出一源|本是同一个词)|见 like|与 like 同源|和 like：像本是同一个词|本义(?:是)?“[^”]*”|见【趣】|lic 本义“[^”]*”'
END = r'(?=，同 |，见 |$)'          # 旧来源后面紧跟“同 例词”或就结束了（后面还有路线、说明的不认，免得重复）

ENTRIES = [
 # ======== 前缀
 E('pre', 're-', '来自拉丁语前缀 re-，本义“往回”，往回再来一次就是“再”',
   r'(?:来自)?拉丁语(?:前缀)? re-(?:，本义“往回”，往回再来一次就是“再”|“回、再”)', drop=r'同一个前缀两个意思：往回 / 再一次|一个前缀两个意思：往回 / 再一次',
   need=r'回|再|又|重新|反', fill=True, fillx='；只用在词前，不单独成词'),
 E('pre', 'un-', '英语本来就有，古英语 un-', r'(?:英语本来就有(?:的前缀)?(?:，古英语 un-)?|古英语 un-)$',
   need=r'不|没|未', avoid=r'反过来|解开|撤销|打开|把.{0,6}(?:解|反)', fill=True, memo='un'),
 E('pre', 'in- im-', '来自拉丁语介词 in“在…里、进入”，和英语的 in 本是同一个词',
   r'(?:来自)?拉丁语(?:介词)? in-?(?:“[^”]*”)?(?:，和英语 in 同源(?:，见 in)?)?(?=，|$)',
   drop=r'(?:这里)?不是(?:表示“不”的 in-|incorrect 里表示“不”的那个 in-)|和英语 in 同源|见 in', sense='into', avoid=r'英语本族|法语', fill=True),
 E('pre', 'in- im- il- ir-', '来自拉丁语表示“不”的前缀 in-',
   r'(?:来自)?拉丁语(?:表示“不”的前缀|的否定前缀|否定前缀|来的否定前缀)?(?: in-)?(?:，和英语 un- (?:同源|是远亲))?(?=，|$)',
   drop=r'和英语 un- (?:同源|是远亲)', sense='neg', avoid=r'法语', fill=True, memo='in'),
 E('pre', 'de-', '来自拉丁语介词 de“从…下来、离开”' + ADV, r'(?:来自)?拉丁语 de-?(?:“(?:从…下来、离开|从…离开、向下)”)?(?=，|$)',
   avoid=r'^这里不是|dis-|des-', fill=True),
 E('pre', 'con- com- co- col- cor-', '来自拉丁语 com-，就是介词 cum“和…一起”',
   r'(?:来自)?拉丁语 (?:com-（cum“和…一起”）|cum“和…一起”|com-?(?=，|$| 在))(?:，= com-)?',
   need=r'一起|共|相互|加强|完全|牢牢|彻底|全|com-', fill=True),
 E('pre', 'ex- e- ef-', '来自拉丁语介词 ex“从…出来、离开”' + ADV, r'(?:来自)?拉丁语 ex(?:“(?:出、离开|从…出来)”)?(?=，|$)',
   need=r'外|出|ex-|彻底|离开', avoid=r'electronic|电子|古法语习惯|st 前|com-|ge-', fill=True),
 E('pre', 'dis- dif- di-', '来自拉丁语前缀 dis-，本义“一分为二、向两边”',
   r'(?:来自)?拉丁语前缀 dis-，本义“一分为二、向两边”(?:，和 duo“二”有关)?|(?:就是)?拉丁语前缀 dis-“一分为二、向两边”|来自拉丁语 dis-“分开”',
   drop=r'和 duo“二”有关', need=r'分|散|相反|不|去掉|dis-|离|没有', avoid=r'希腊语', fill=True, memo='dis'),
 E('pre', 'pro-', '来自拉丁语介词 pro“在前面、向前”' + ADV, r'(?:来自)?拉丁语 pro“(?:向前|向前、在前)”(?:，见 pro)?(?=，|$)',
   need=r'前|替|为|代|出', fill=True, memo='pro'),
 E('pre', 'en- em-', '来自法语 en-，往上是拉丁语介词 in“在…里、进入”',
   r'(?:来自法语(?: en-)?，往上是拉丁语 in-(?:“进入”)?|← 拉丁语 in-|拉丁语 in-，经古法语写成 en-|来自拉丁语 in-(?=，|$))',
   need=r'使|放进|里|进入|em-|en-|in-|给', avoid=r'希腊语|和 in- 常混', fill=True, memo='en'),
 E('pre', 'pre-', '来自拉丁语介词 prae“在前面”' + ADV, r'(?:来自)?拉丁语 prae“在前”', need=r'前|预先', fill=True),
 E('pre', 'over-', '英语本来就有，就是单词 over，古英语写作 ofer', r'英语本来就有的前缀，古英语 ofer', drop=r'见 over', fill=True),
 E('pre', 'ad-', '来自拉丁语介词 ad“向、到”' + ADV, r'(?:来自)?拉丁语 ad“(?:向、到|到、向)”', need=r'向|到|朝|加', avoid=r'ex-', fill=True, memo='ad'),
 E('pre', 'ac- af- ag- al- an- ap- ar- as- at- a-', '来自拉丁语介词 ad“向、到”' + ADV, r'(?:来自)?拉丁语 ad“(?:向、到|到、向)”',
   need=r'ad-|ad“', avoid=r'ex-|古英语|and-|希腊语|意大利语', fill=True, memo='ad'),
 E('pre', 'be-', '英语本来就有，古英语 be-，就是 bi“在旁边、在周围”读轻了的样子',
   r'(?:英语本来就有的前缀，)?古英语(?:前缀)? (?:bi-|be-)(?:，读轻了变成 be-|“在…周围、在旁边”|，就是 by“在旁边”读轻了的样子|，by 轻读时就成了 be-)?(?=，|$)',
   fill=True, memo='be'),
 E('pre', 'sub- sup- suf- suc- sus- sug- sum-', '来自拉丁语介词 sub“在下面”' + ADV, r'(?:来自)?拉丁语 sub“在下面”',
   need=r'下|sub-|在后面', avoid=r'super|法语 sur', fill=True, memo='sub'),
 E('pre', 'inter-', '来自拉丁语介词 inter“在…之间”' + ADV, r'来自拉丁语 inter“在…之间”', need=r'之间|相互|中间', fill=True),
 E('pre', 'non-', '来自拉丁语 non“不”，本来是 ne oinom“一个也不”', r'来自拉丁语 non“不”', need=r'不|非', fill=True, memo='non'),
 E('pre', 'super-', '来自拉丁语介词 super“在上面”' + ADV, r'(?:来自)?拉丁语 super“在上面(?:、超过)?”(?:，见 super)?', need=r'上|超', fill=True, memo='super'),
 E('pre', 'sur-', '来自法语 sur-，往上是拉丁语介词 super“在上面”',
   r'(?:来自法语 sur，往上是拉丁语 super，到法语里缩成 sur-|法语里 super- 变成了 sur-|= 拉丁语 super-)', need=r'super|上方|上面', fill=True, memo='super'),
 E('pre', 'out-', '英语本来就有，就是单词 out，古英语写作 ut', r'英语本来就有的前缀，古英语 ut', fill=True),
 E('pre', 'mid-', '英语本来就有，就是古英语 midd“中间的”，和 middle 是一家',
   r'(?:(?:来自)?古英语(?:形容词)? midd?(?:“中间的”)?|英语本(?:来就有|族)的前缀，古英语 midd)(?=，|$)', drop=r'和 middle (?:中间 )?(?:同源|是一家)|见第 \d+ 组', fill=True),
 E('pre', 'trans-', '来自拉丁语介词 trans“越过、到另一边”' + ADV, r'(?:来自)?拉丁语 trans“越过”', fill=True, memo='trans'),
 E('pre', 'per-', '来自拉丁语介词 per“穿过”' + ADV, r'来自拉丁语 per“穿过”', fill=True),
 E('pre', 'under-', '英语本来就有，就是单词 under，古英语写作 under', r'英语本来就有的前缀，古英语 under', need=r'下|不足|低|不够', fill=True),
 E('pre', 'ob- op- oc- of-', '来自拉丁语介词 ob“对着、挡在前面”' + ADV, r'(?:来自)?拉丁语 ob“对着(?:、迎着)?”', need=r'对|迎|挡|ob-|反', fill=True),
 E('pre', 'mis-', '英语本来就有，古英语 mis-“错、偏”', r'(?:英语本来就有的前缀，)?古英语 mis-(?=，|$)', need=r'错|坏', avoid=r'minus|拉丁语', fill=True, memo='mis'),
 E('pre', 'dia-', '来自希腊语介词 dia“穿过、分开”' + ADV, r'(?:来自)?希腊语(?: dia(?:“穿过、分开”)?| ?前缀)$', need=r'穿|之间|分|彻底', fill=True),
 E('pre', 'up-', '英语本来就有，就是单词 up，古英语写作 up', r'英语本来就有的前缀，古英语 up', fill=True),
 E('pre', 'ab- abs-', '来自拉丁语介词 ab“离开”' + ADV, r'(?:来自)?拉丁语 ab“离开”', need=r'离', avoid=r'= ad-', fill=True, memo='ab'),
 E('pre', 'anti-', '来自希腊语介词 anti“对着、反对”' + ADV, r'来自希腊语 anti“对着、反对”', need=r'反对|对抗|抵消', avoid=r'ante', fill=True),
 E('pre', 'tele-', '来自希腊语 tēle“在远处”', r'(?:来自)?希腊语 tēle(?:“(?:远|在远处)”)?$', need=r'远', fill=True),
 E('pre', 'micro-', '来自希腊语 mikros“小的”', r'(?:来自)?希腊语 mikros(?:“小(?:的)?”)?$', need=r'小|微', fill=True),
 E('pre', 'syn- sym-', '来自希腊语介词 syn“和…一起”' + ADV, r'(?:来自)?希腊语(?: syn(?:-)?(?:“[^”]*”)?| ?前缀)?(?=，|$)', need=r'一起|共|同', fill=True),
 E('pre', 'post-', '来自拉丁语介词 post“在后面、在…之后”' + ADV, r'(?:来自)?拉丁语 post(?:“[^”]*”)?(?=，|$)', need=r'后', fill=True),
 # ======== 后缀
 E('suf', '-ly', '来自古英语 lic“身体、样子”，本来是一个单独的词：带着…的样子 → 以…的方式', r'(?:来自)?古英语 -?lic(?:e)?(?:“[^”]*”)?(?:：带着…的样子 → 以…的方式)?',
   kind='副词', drop=DROP_LIKE, top=r'^-ly 本身来自古英语 lic“[^”]*”，和 like 是一家（见 like）$', fill=True, memo='ly'),
 E('suf', '-ly', '来自古英语 lic“身体、样子”，本来是一个单独的词：接在名词后面，就是“有…样子的”', r'(?:来自)?古英语 -?lic(?:e)?(?:“[^”]*”)?(?:：带着…的样子 → 以…的方式)?',
   kind='形容词', drop=DROP_LIKE, fill=True, memo='ly_adj'),
 E('suf', '-ion', '来自拉丁语名词词尾 -io，变格时写作 -ionem，经法语磨成 -ion 进入英语', r'来自拉丁语(?:名词词尾)? -io(?:，经法语进入英语|，宾格 -ionem)' + END, kind='名词'),
 E('suf', '-er', '英语本来就有的后缀，古英语写作 -ere', r'(?:英语本来就有的后缀，古英语写作|(?:来自)?古英语) -ere' + END, kind='名词', need=r'人|东西|者|工具|机|器', fill=True),
 E('suf', '-er', '英语本来就有的比较级词尾，古英语写作 -ra / -or', r'(?:英语本来就有的比较级词尾，古英语写作 -ra / -or|(?:来自)?古英语(?:写)? -ra)' + END, kind='形容词', need=r'更|比较', fill=True),
 E('suf', '-er', '英语本来就有的后缀，古英语写作 -rian，表示“一下接一下地做”',
   r'(?:英语本来就有的(?:动词词尾|后缀)(?:，古英语写作 -(?:rian|ere)(?:，表示“一下接一下地做”)?)?|来自古英语 -erian)' + END, kind='动词', need=r'反复|一下|重复', fill=True),
 E('suf', '-est', '英语本来就有，古英语最高级词尾 -est / -ost', r'(?:英语本来就有，古英语最高级词尾 -est(?: / -ost)?|古英语 -ost / -est)' + END, kind='形容词', need=r'最', fill=True),
 E('suf', '-ed', '英语本来就有，古英语写作 -ed / -od', r'英语本来就有，古英语写作 -ed(?: / -od)?' + END, kind='形容词', need=r'被|已经|了的|感到', avoid=r'-ede|名词后', fill=True),
 E('suf', '-ing', '英语本来就有，古英语写作 -ung / -ing，专门把动作变成名词', r'(?:英语本来就有，)?古英语(?:写作)? -ung(?: / |、)-ing(?:，专门把动作变成名词)?' + END, kind='名词', fill=True),
 E('suf', '-ing', '英语本来就有：古英语“正在…的”写作 -ende，中古英语时和名词词尾 -ing 并成了一个', r'英语本来就有：古英语“正在…的”写作 -ende，中古英语时和名词词尾 -ing 并成了一个' + END, kind='形容词', need=r'正在|令人|的', fill=True),
 E('suf', '-al', '来自拉丁语形容词词尾 -alis“属于…的、和…有关的”，经法语或直接从拉丁语进入英语', r'来自拉丁语(?:形容词词尾)? -alis' + END, kind='形容词', fill=True),
 E('suf', '-al', '来自拉丁语形容词词尾 -alis 的复数 -alia，经法语 -aille 进入英语，成了名词词尾',
   r'(?:来自拉丁语 -alis 的名词用法，经法语 -aille 进入英语|来自拉丁语形容词词尾 -alis 的复数形式，经法语变成了名词词尾|来自法语 -aille ← 拉丁语 -alia|来自英法语 -aille)' + END, kind='名词'),
 E('suf', '-y', '英语本来就有的后缀，古英语写作 -ig', r'(?:英语本来就有的后缀，古英语写作|(?:来自)?古英语) -ig' + END, kind='形容词', fill=True),
 E('suf', '-able', '来自拉丁语 -abilis“能…的”，经法语进入英语', r'来自拉丁语(?: -abilis)?，经法语(?:进入英语)?' + END + r'|来自拉丁语$', kind='形容词', fill=True),
 E('suf', '-ible', '来自拉丁语 -ibilis，是 -abilis 的另一种样子', r'来自拉丁语 -ibilis(?:（-abilis 的另一种样子）|，经法语进入英语)?' + END, kind='形容词', fill=True),
 E('suf', '-ate', '来自拉丁语“被…了的”形式的词尾 -atus：英语借拉丁语动词时，常借它的“被…了的”形式，去掉 -us 就成了 -ate',
   r'来自拉丁语(?:“被…(?:了|过)的”形式的词尾|过去分词的词尾)? -atus(?:，英语借拉丁动词时常拿它当动词用)?' + END, kind='动词', fill=True),
 E('suf', '-ate', '来自拉丁语“被…了的”形式的词尾 -atus：去掉 -us 就成了 -ate，当形容词还是“被…了的、处在…的”',
   r'来自拉丁语(?:“被…了的”形式的词尾 -atus| -atus(?:“已经…了的”)?|“已经…了的”)' + END, kind='形容词', need=r'的'),
 E('suf', '-ic', '来自拉丁语 -icus、希腊语 -ikos，经法语 -ique 进入英语',
   r'来自(?:拉丁语 -icus、希腊语 -ikos|希腊语 -ikos(?:、拉丁语 -icus)?)(?:，经(?:拉丁语 -icus、)?法语 -ique 进入英语)?' + END, kind='形容词', fill=True),
 E('suf', '-ive', '来自拉丁语形容词词尾 -ivus，经法语 -if / -ive 进入英语', r'来自拉丁语(?:形容词词尾)? -ivus，经法语(?: -if / -ive)? ?进入英语' + END, kind='形容词', fill=True),
 E('suf', '-ity', '来自拉丁语 -itas，变格时写作 -itatem，经法语 -ité 进入英语', r'来自拉丁语 -itas，经法语 -ité 进入英语' + END, kind='名词', fill=True),
 E('suf', '-ty', '来自拉丁语 -tas，变格时写作 -tatem，经法语 -té 进入英语，是 -ity 的短样子',
   r'(?:(?:来自)?拉丁语 -tas，经(?:古)?法语(?: -té| ?变成 -té)?(?: 进入英语)?|来自古法语 -té、拉丁语 -tas|来自拉丁语 -itas 经法语磨短的样子，和 -ity 是一家)' + END, kind='名词', need=r'性质|状态|-ity|的事|程度', fill=True),
 E('suf', '-ty', '英语本来就有，古英语写作 -tig“十个一组”', r'(?:英语本来就有(?:的后缀)?，)?(?:来自)?古英语(?:写作)? -tig(?:“[^”]*”)?', kind='*', need=r'十', avoid=r'性质|状态|拉丁语|法语', drop=r'韦氏词典说它和 ten 同源|和 ten 同源', fill=True, memo='ty'),
 E('suf', '-teen', '英语本来就有，古英语写作 -tene', r'(?:英语本来就有(?:的后缀)?，)?(?:来自)?古英语(?:写作)? -t[iyeē]+ne(?: / -t[iye]+ne)?(?:“[^”]*”)?', kind='*', need=r'十', drop=r'就是 ten 的一种形式', fill=True, memo='teen'),
 E('suf', '-ness', '英语本来就有的后缀，古英语写作 -nes', r'(?:英语本来就有的后缀，古英语写作|(?:来自)?古英语) -nes' + END, kind='名词', fill=True),
 E('suf', '-ment', '来自拉丁语名词词尾 -mentum“用来…的东西、…的结果”，经法语进入英语',
   r'来自(?:拉丁语(?:名词词尾)? -mentum(?:“用来…的东西”)?(?:，经法语进入英语)?|法语，← 拉丁语 -mentum)' + END, kind='名词', fill=True),
 E('suf', '-s', '英语本来就有，古英语的复数词尾 -as', r'(?:英语本来就有，古英语的复数词尾|英语本族，古英语|(?:来自)?古英语(?:阳性名词的复数词尾)?) -as' + END, kind='名词', need=r'复数', fill=True),
 E('suf', '-s', '英语本来就有，古英语表示“…的”的词尾 -es，拿来造副词', r'(?:英语本来就有，古英语表示“…的”的词尾 -es，拿来造副词|来自古英语(?: -es)?)' + END, kind='副词', fill=True),
 E('suf', '-or', '来自拉丁语表示“做…的人”的词尾 -or，经古法语进入英语', r'来自拉丁语(?:表示“做…的人”的词尾)? -or，经(?:古)?法语进入英语' + END, kind='名词', need=r'人|东西', avoid=r'状态|感受', fill=True),      # 2026-11 词缀关系轮：tumor、terror、horror 这类表示状态的 -or 不是“做…的人”
 E('suf', '-less', '来自古英语 leas“没有的、丢了的”，本来是一个单独的词', r'(?:英语本来就有的后缀，)?(?:来自)?古英语(?:写作)? -?l[eē]as(?:“[^”]*”)?',
   kind='形容词', drop=r'和 loose(?:“松开的”|“松的”| 松的)? ?(?:是一家|同源)|见 loose', fill=True, memo='less'),
 E('suf', '-ent', '来自拉丁语“正在…的”形式的词尾 -ens，变格时写作 -entem', r'来自拉丁语(?:“正在…的”形式的词尾 -ens（-entem）| -ens / -entis，经法语进入英语)' + END, kind='形容词', fill=True),
 E('suf', '-ant', '来自拉丁语“正在…的”形式的词尾 -ans，变格时写作 -antem，多经法语进入英语',
   r'来自拉丁语(?:“正在…的”形式的词尾 -ans（-antem）| -ans / -antis，经法语进入英语|表示“正在…”的词尾 -antem)' + END, kind='形容词', fill=True),
 E('suf', '-ize', '来自希腊语动词词尾 -izein，经拉丁语 -izare、法语 -iser 进入英语',
   r'来自希腊语(?:动词词尾)? -izein(?:，经(?:拉丁语 -izare、法语 -iser|晚期拉丁语、古法语)进入英语)?' + END, kind='动词', fill=True),
 E('suf', '-ise', '就是 -ize：来自希腊语动词词尾 -izein，经法语 -iser 进入英语', r'就是 -ize：来自希腊语动词词尾 -izein，经法语 -iser 进入英语' + END, kind='动词', need=r'-ize|使', fill=True),
 E('suf', '-ous', '来自拉丁语 -osus“充满…的”，经法语进入英语', r'来自拉丁语 -osus(?:“充满…的”)?(?:，经法语进入英语)?' + END, kind='形容词', fill=True),
 E('suf', '-ist', '来自希腊语 -istēs，经拉丁语 -ista、法语 -iste 进入英语', r'来自希腊语 -ist[eē]s，经拉丁语 -ista、法语 -iste 进入英语' + END, kind='名词', fill=True),
 E('suf', '-ful', '英语本来就有的后缀，古英语写作 -full，本来就是单词 full“满的”', r'英语本来就有的后缀(?:，就是 full“满的”变来的，见 full)?' + END,
   kind='形容词', drop=r'由 full“满的”变来，作词尾只写一个 l', fill=True, memo='ful'),
 E('suf', '-ful', '英语本来就有的后缀，古英语写作 -full，本来就是单词 full“满的”', r'英语本来就有的后缀(?:，就是 full“满的”变来的，见 full)?' + END, kind='名词', need=r'满|量', fill=True, memo='ful_n'),
 E('suf', '-ary', '来自拉丁语 -arius / -arium：本来是“和…有关的”，当名词时指和它有关的人、地方', r'来自拉丁语 -arius(?: / -arium)?(?:，经法语进入英语)?' + END, kind='形容词', fill=True),
 E('suf', '-age', '来自法语 -age，再往上是拉丁语 -aticum“和…有关的东西”',
   r'来自(?:法语 -age，再往上是拉丁语 -aticum|拉丁语 -aticum(?:“和…有关的：东西”，在古法语里正好变成 -age|，经古法语 -age 进入英语)?)' + END, kind='名词', fill=True),
 E('suf', '-en', '英语本来就有的后缀，古英语写作 -nian：接在形容词、名词后面造动词', r'(?:英语本来就有(?:的后缀)?，)?(?:来自)?古英语(?:写作)? -nian(?:，加在形容词、名词后面造动词)?' + END, kind='动词', need=r'使|变得', fill=True),
 E('suf', '-en', '英语本来就有，古英语“被…了的”形式的词尾 -en', r'(?:英语本来就有，古英语“被…了的”形式的词尾(?: -en)?|英语本来就有(?:的后缀)?(?:，古英语写作 -en)?|古英语就是 -en)' + END, kind='形容词', need=r'被|了的|已经'),
 E('suf', '-ure', '来自拉丁语名词词尾 -ura，经法语进入英语', r'来自拉丁语名词词尾 -ura，经法语进入英语' + END, kind='名词', fill=True),
 E('suf', '-ance', '来自拉丁语 -antia，是“正在…的”形式 -ans 变成的名词，经法语 -ance 进入英语',
   r'来自(?:拉丁语 -antia(?:（由“正在…的”形式 -ans 变成名词）)?，经法语(?: -ance)? ?进入英语|法语，← 拉丁语 -antia)' + END, kind='名词', fill=True),
 E('suf', '-ence', '来自拉丁语 -entia，是“正在…的”形式 -ens 变成的名词，经法语进入英语', r'来自拉丁语 -entia(?:（由“正在…的”形式 -ens 变成名词）)?，经法语进入英语' + END, kind='名词', fill=True),
 E('suf', '-ar', '来自拉丁语形容词词尾 -aris，就是 -alis，前面有 l 时写成 -aris', r'来自拉丁语(?:形容词词尾)? -aris(?:（就是 -alis，前面有 l 时写成 -aris）)?' + END, kind='形容词', fill=True),
 E('suf', '-et', '来自古法语表示“小”的词尾 -et', r'(?:来自古法语表示“小”的词尾 -et|来自法语$|古法语 -et(?:te)? / -et(?:te)?)' + END, kind='名词', need=r'小', fill=True),
 E('suf', '-le', '英语本来就有，古英语写作 -lian，表示“一下接一下地做”', r'英语本来就有(?:的后缀)?(?:，古英语写作 -lian，表示“一下接一下地做”)?' + END, kind='动词', need=r'反复|一下|连续|不停', fill=True),
 E('suf', '-ian', '来自拉丁语形容词词尾 -ianus“属于…的”', r'(?:来自)?拉丁语(?:形容词词尾)? -ianus(?:“属于…的”)?(?:，经法语(?: -ien)? 进入英语)?' + END, kind='名词', fill=True),
 E('suf', '-an', '来自拉丁语形容词词尾 -anus“属于…的”', r'(?:来自)?拉丁语(?:形容词词尾)? -anus(?:“属于…的”)?' + END, kind='名词', fill=True),
 E('suf', '-ish', '英语本来就有的后缀，古英语写作 -isc', r'(?:英语本来就有的后缀，古英语写作|(?:来自)?古英语) -isc' + END, kind='形容词', fill=True),
 E('suf', '-ish', '来自古法语动词变化时带出的 -iss-，往上是拉丁语表示“开始…”的 -isc-', r'来自古法语动词(?:变化时带出的|变化里的|的加长形式) -iss-(?:，← 拉丁语 -isc-)?',
   kind='动词', fill=True, need=r'不是“有点|动词词尾|-iss'),
 E('suf', '-ship', '英语本来就有的后缀，古英语写作 -scipe“…的样子、状态”', r'(?:英语本来就有的后缀，古英语写作|(?:来自)?古英语) -sci(?:e)?pe(?:“[^”]*”)?',
   kind='名词', drop=r'和 shape(?:“[^”]*”)? ?(?:同源|是一家)', fill=True, memo='ship'),
 E('suf', '-ory', '来自拉丁语 -orius，当名词时是 -orium', r'来自拉丁语 -orius(?: / -orium)?' + END, kind='形容词', fill=True),
 E('suf', '-like', '英语本来就有，就是单词 like“像”，古英语写作 gelic“同一个样子的”',
   r'英语本来就有(?:的后缀)?(?:，(?:就是|来自) like“像”(?:，见 like)?|，来自古英语 lic“身形”)?' + END + r'|古英语 gelic(?:，字面“同一个身形的”)?$', kind='形容词', drop=r'见第 \d+ 组|见 like', need=r'像', fill=True),
 E('suf', '-cy', '来自拉丁语 -cia / -tia，经法语进入英语', r'(?:来自)?拉丁语 -(?:cia / -tia|tia)(?:，经(?:古)?法语(?: -cie)? 进入英语)?' + END, kind='名词', fill=True),
 E('suf', '-ify', '来自拉丁语 -ificare，里面的 fic 就是 facere“做”，经法语 -ifier 进入英语', r'来自拉丁语(?: -ficare，←)? facere“做”' + END, kind='动词', need=r'使|做', fill=True),
 E('suf', '-id', '来自拉丁语形容词词尾 -idus', r'来自拉丁语(?:形容词词尾)?(?: -idus)?' + END, kind='形容词', fill=True),
 E('suf', '-ery', '来自古法语 -erie', r'(?:来自)?(?:古)?法语 -erie' + END, kind='名词', fill=True),
 E('suf', '-th', '英语本来就有，古英语写作 -þu / -þ', r'英语本来就有(?:的后缀)?，古英语写作 -þu / -þ' + END, kind='名词', fill=True),
 E('suf', '-ile', '来自拉丁语形容词词尾 -ilis', r'来自拉丁语(?: -ilis)?' + END, kind='形容词', fill=True),
 E('suf', '-ess', '来自法语 -esse，往上是希腊语 -issa', r'来自(?:法语(?: -esse，再往上是希腊语 -issa)?|希腊语 -issa(?:，经晚期拉丁语 -issa、法语 -esse 进入英语)?)' + END, kind='名词', need=r'女|雌', fill=True),
 E('suf', '-hood', '英语本来就有，古英语 had“身份、状态”，本来是一个单独的词', r'(?:英语本来就有的后缀，)?(?:来自)?古英语(?:写作)? -?had(?:“[^”]*”)?' + END, kind='名词', fill=True),
 E('suf', '-dom', '英语本来就有，古英语 dom“判定、状态”，本来是一个单独的词', r'(?:英语本来就有的后缀，)?(?:来自)?古英语(?:写作)? -?dom(?:“[^”]*”)?' + END, kind='名词', fill=True),
 E('suf', '-some', '英语本来就有的后缀，古英语写作 -sum', r'(?:英语本来就有的后缀，古英语写作|(?:来自)?古英语) -sum(?:“[^”]*”)?' + END, kind='形容词', fill=True),
 E('suf', '-ward', '英语本来就有的后缀，古英语写作 -weard“朝着…的”', r'(?:英语本来就有(?:的后缀)?，古英语写作|(?:来自)?古英语) -weard(?:“[^”]*”)?' + END, kind='*', need=r'向|朝|方向', fill=True),
]

# 词缀的记法：(写法, 符号, 关联词, 中文, 道理, 音变)；写法相近的不写音变。同源关系都对照过 etymonline（2026-11）。
# ≈ 真的是一家；← 从它变来；trans ≈ through 词典只说“也许”（Watkins），道理里照写。
MEMO = {
 'pro': ('pro', '≈', 'for', '为了', 'for 是“为了、替”，它最早的意思是“在…前面”，和 pro 一样；站到前面替人出头，就是“为了”。它们本是一家',
         'p 对 f：印欧语的 p，拉丁语还是 p，英语念成 f（印欧语词根 *per-“向前”；同 ped- 和 foot、patr- 和 father）；原因：英语属于日耳曼语，日耳曼语两千多年前把 p、t、k 成批地念成了 f、th、h，这叫格林定律，拉丁语没有这样变；发音：念 p，两片嘴唇先闭紧、再一下子放开，念 f，下嘴唇轻贴上牙、不闭紧，气从缝里擦出来，两个音都用嘴唇，只差闭不闭紧，所以 p 容易念成 f；起因：没有定论，一种说法是重音方式变了，说话时气流压力加大，p、t、k 先带出一股气，再变成摩擦；例子：拉丁语 piscis 和 fish、plenus 和 full、paucus 和 few'),
 'dis': ('dis', '≈', 'two', '二', 'two 是二；dis- 本义“一分为二、向两边”，东西分成两半就分开了，所以 dis- 是“分开”，也是“相反、不”。它们本是一家',
         'd 对 t：印欧语词根 *dwis-“两次、分成两半”，拉丁语只留下 d，英语把 d 念成 t（同 du- 和 two、dec- 和 ten）；原因：英语属于日耳曼语，日耳曼语两千多年前把 b、d、g 成批地念成了 p、t、k，这叫格林定律，拉丁语没有这样变；发音：念 d，舌尖先顶住上牙床、再放开，喉咙里的声带同时振动，念 t，舌尖动作一样，声带不振动，两个音舌尖动作一样，只差声带振不振，所以 d 容易念成 t；起因：没有定论，一种说法是 p、t、k 变成 f、th、h 以后空出了位置，b、d、g 补上去念成了 p、t、k，这几步谁先谁后学者还有争议；例子：拉丁语 dens 和 tooth、edere 和 eat、sedere 和 sit'),
 'ad': ('ad', '≈', 'at', '在、向', 'at 是“在、向着”，ad 也是“向、到”。它们本是一家',
        'd 对 t：印欧语词根 *ad-“向、到”，拉丁语还是 d，英语念成 t（同 du- 和 two、ped- 和 foot）；原因：英语属于日耳曼语，日耳曼语两千多年前把 b、d、g 成批地念成了 p、t、k，这叫格林定律，拉丁语没有这样变；发音：念 d，舌尖先顶住上牙床、再放开，喉咙里的声带同时振动，念 t，舌尖动作一样，声带不振动，两个音舌尖动作一样，只差声带振不振，所以 d 容易念成 t；起因：没有定论，一种说法是 p、t、k 变成 f、th、h 以后空出了位置，b、d、g 补上去念成了 p、t、k，这几步谁先谁后学者还有争议；例子：拉丁语 decem 和 ten、dens 和 tooth、edere 和 eat'),
 'ab': ('ab', '≈', 'off', '离开', 'off 是“离开”，ab 也是“离开”，of 也是这一家。它们本是一家',
        'b 对 f：印欧语词根 *apo-“离开”，拉丁语把 p 念成了 b，英语念成 f（同 ped- 和 foot）；原因：英语属于日耳曼语，日耳曼语两千多年前把 p、t、k 成批地念成了 f、th、h，这叫格林定律，拉丁语没有这样变；发音：念 p，两片嘴唇先闭紧、再一下子放开，念 f，下嘴唇轻贴上牙、不闭紧，气从缝里擦出来，两个音都用嘴唇，只差闭不闭紧，所以 p 容易念成 f；起因：没有定论，一种说法是重音方式变了，说话时气流压力加大，p、t、k 先带出一股气，再变成摩擦；例子：拉丁语 piscis 和 fish、plenus 和 full、paucus 和 few'),
 'sub': ('sub', '≈', 'up', '向上', '同一个印欧语词根既是“在下面”，又是“从下面往上”：拉丁语留下了“下”，就是 sub；英语留下了“上”，就是 up。'
         '所以 sub 有时也是“从下面往上”：support 就是从下面往上托住，sup 就是 sub',
         'b 对 p：印欧语词根 *upo“在下面、从下面往上”，拉丁语在前面多加了一个 s，p 念成了 b（印欧语词根 *(s)up-；希腊语的 hypo- 也是它）'),
 'super': ('super', '≈', 'over', '在上面', 'over 是“在上面、越过”，super 也是“在上面、超过”。它们本是一家',
           'p 对 v：印欧语词根 *uper“在上面”，拉丁语在前面多加了一个 s，英语把 p 念成 v（古英语 ofer；同 sub- 和 up）'),
 'un': ('un', '≈', 'no', '不', 'no 是“不”，un- 也是“不”。它们出自同一个表示“不”的印欧语词根，拉丁语的 in-、non 也是这一家', ''),
 'in': ('in', '≈', 'no', '不', 'no 是“不”，表示“不”的 in- 也是“不”。它们出自同一个表示“不”的印欧语词根，英语的 un- 也是这一家；和表示“向里”的 in- 只是写法一样', ''),
 'non': ('non', '≈', 'no', '不', 'no 是“不”，non 也是“不”，它本来是拉丁语的“一个也不”。它们出自同一个表示“不”的印欧语词根', ''),
 'en': ('en', '≈', 'in', '在…里', 'in 是“在…里”，en- 是“放进…里、使…”；en- 是拉丁语 in- 到了法语里的样子，和英语的 in 本是一家', ''),
 'mis': ('mis', '≈', 'miss', '错过', 'miss 是“没打中、错过”，mis- 是“弄错、弄偏”：没对准就错了。它们本是一家', ''),
 'be': ('be', '≈', 'by', '在旁边', 'by 是“在旁边”，be- 就是 by 读轻了的样子，beside 就是“在旁边”。它们本是一家', ''),
 'ly': ('ly', '≈', 'like', '像', 'like 是“像”；-ly 本来是“…的样子”，quickly 本来就是“快的样子”，带着快的样子去做就是“快快地”。它们本是一家', ''),
 'ly_adj': ('ly', '≈', 'like', '像', 'like 是“像”；-ly 本来是“…的样子”，friendly 就是“朋友的样子的”、像朋友一样。它们本是一家', ''),
 'ful': ('ful', '←', 'full', '满的', '-ful 就是 full 变来的：装满了…，就是“充满…的”；当后缀只写一个 l', ''),
 'ful_n': ('ful', '←', 'full', '满的', '-ful 就是 full 变来的：handful 就是满满一把的量；当后缀只写一个 l', ''),
 'less': ('less', '≈', 'lose', '丢失', 'lose 是丢了，丢了就没有了；-less 就是“没有…的”。它们本是一家；和单词 less“更少的”只是长得像', ''),
 'ship': ('ship', '≈', 'shape', '形状', 'shape 是形状、样子；-ship 本来是“…的样子、状态”，friendship 就是朋友之间的样子，就是友谊。它们本是一家', ''),
 'teen': ('teen', '≈', 'ten', '十', 'ten 是十，-teen 就是 ten：thirteen 就是“三加十”。它们本是一家', ''),
 'ty': ('ty', '≈', 'ten', '十', 'ten 是十，-ty 是“几个十”：twenty 就是“两个十”。它们本是一家', ''),
 'trans': ('trans', '≈', 'through', '穿过', 'through 是“穿过”，trans 也是“越过、穿过，到另一边”。词典说它们也许出自同一个表示“穿过去”的印欧语词根',
           't 对 th：印欧语的 t，拉丁语还是 t，英语念成 th（印欧语词根 *tere-“穿过去”；同 tri- 和 three）；原因：英语属于日耳曼语，日耳曼语两千多年前把 p、t、k 成批地念成了 f、th、h，这叫格林定律，拉丁语没有这样变；发音：念 t，舌尖先顶住上牙床、再一下子放开，念 th，舌尖轻放在上下牙中间、不顶住，气从缝里擦出来，两个音都用舌尖，只差顶不顶住，所以 t 容易念成 th；起因：没有定论，一种说法是重音方式变了，说话时气流压力加大，p、t、k 先带出一股气，再变成摩擦；例子：拉丁语 tenuis 和 thin、tonare 和 thunder、tu 和 thou'),
}
# 查过、不写记法的（etymonline 里找不到学生认识的同族简单词）：re-、com- / con-、ex-、de-、pre-、inter-、per-、ob-、-ion、-ment、-al、-ous、-ive、-ity……
NO_MEMO = 're- com- con- ex- de- -ion -ment'.split()


def memo_text(key):
    a, sym, b, zh, why, sh = MEMO[key]
    return '记：%s %s %s（%s）：%s' % (a, sym, b, zh, why) + ('。音变：' + sh if sh else '')

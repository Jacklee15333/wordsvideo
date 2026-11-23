# -*- coding: utf-8 -*-
"""词缀的辨析（2026-11 词缀身份辨析轮，project_rules.md 第 83–88 条；上一版叫“身份和分工”，第 67 条）：
意思、功能相近的前缀、后缀放在一起讲——每个都讲清接什么词、说什么意思、和旁边那个差在哪儿（用户：“不能只说来自哪里，也要说具体的用法，起到什么作用”）。
（2026-11 词缀关系轮起，一组辨析的最后可以有一段“；关系：…”：同一种语言来的几个词缀彼此是什么关系，见下面的 REL；第 89–92 条。）
GROUP[辨析组] = 辨析那句话：一个词缀（或写法相近的几个）一条，“；”隔开，开头“同样是…：”是总说，括号里是例词（都是总表里的词）；
              里面没有句号；去掉括号念出来是通顺的一句话（视频照念）。写进前缀列、后缀列那一行的最后：“…。辨析：…”，一字不改。
SUF[(后缀, 变成什么)] = (来头, 辨析组)；PRE[前缀] = (来头, 辨析组) 或 [(开头的介绍里要有的字, 来头, 辨析组), …]（同一个写法两种意思的）。
    “来头”是上一版单独写的那句身份，现在不再写进表（开头的介绍就是身份），留着给新写一行时参考。
NO_BX：逐个看过、不挂辨析的行（这一行明说自己不是那个词缀：grammar 的 -ar、e-book 的 e-、advantage 的 ad-）。
FORCE：逐个看过、规则挑不对的行，直接定哪一组。
这个词为什么用它，写在下面单独一行“为什么用 -ous 不用 -ful：…”（原来就有的写法）。"""
# 2026-11 辨析精简演示轮（project_rules.md 第 103–106 条）：20 组辨析、10 组关系按“精简”的写法重写（用户：“有很多口语话的词可以去掉，还有一些不是很必要的词也可以去掉，让句子简化一下，减少视频时间”“要把总表里面有同样问题的都进行这样的处理”）：
#   来源写成“拉丁语 / 英语本族 / 希腊语 / 法语”，紧跟在词缀后面（不写“是拉丁语来的”“是英语自己的”）；不写“接在、加在、日常的、正好、别弄混”这类话；
#   每个用法一小句“名词前是“…”（例词）”“动词词根前是“…”（例词）”，例词紧跟在它说明的那个用法后面——括号里第一个词是视频的“演示词”（用户：“重点是要说明是加动词还是加名词……加动词的效果和加名词的效果要体现出来”），
#   视频取它自己那一行组合列第一行的等式画“图 + 图 = 画”；演示词要在总表里、组合列第一行写成“A（…）+ B（…）=“…””（cizhui.py --check 的 demo_bad）。关系里不写“这叫格林定律”。
# PREV_CORE / PREV_REL 是上一版（音变原因版）的句子，cizhui.py 靠它认出要换成新句子的行。
GROUP = {
 'adj_n': '同样是把名词变成形容词：-ful 英语本族，名词后是“充满…的、带来…的”（careful、useful）；-less 英语本族，和 -ful 相反，名词后是“没有…的”（careless、useless）；-y 英语本族，接短名词，说“有…的、…多的”，口语味最浓（rainy、sunny）；-ish 英语本族，说“有点像…的”，常带贬义，也表示国籍、语言（childish、English）；-ly 英语本族，多接表示人的名词，说“像…一样的”，接形容词才是副词（friendly）；-ous 拉丁语，经法语进来，说“充满…的、有…特点的”（dangerous、famous）；-al、-ic 拉丁语、希腊语，只说“和…有关的”，多用在书面词、学科词，可叠成 -ical（national、basic、historic、historical）',
 'adj_v': '同样是把动词变成形容词：-ive 拉丁语，多接过去分词词干，说“会…的、有…作用的”，讲东西自己的性质（active、creative）；-able 拉丁语，动词后是“能被…的、值得…的”，讲别人能对它做什么，英语造词都用它，-ible 是拉丁语借词里的写法（usable、visible）；-ing 英语本族，现在分词当形容词，说“让人…的”，多讲东西给人的感觉（interesting、exciting）；-ed 英语本族，过去分词当形容词，说“被…了的、感到…的”，多讲人的感受，不规则动词用 -en（interested、excited、taken）；-ant、-ent 拉丁语，说“处在…状态的”，只在拉丁语、法语借词里，写哪个照原词（important、different）；-ory 拉丁语，也接过去分词词干，说“起…作用的”（introductory、sensory）',
 'n_act': '同样是把动词变成名词：-ing 英语本族，什么动词都能接，说“做这件事”（reading、swimming）；-ion 拉丁语，接拉丁语动词的过去分词词干，最多、最正式，说“这个行为”，也指结果，英语造词多用 -ation（action、invention、organization）；-ment 拉丁语，经法语进来，多接法语来的动词，说“做成的结果、用来…的东西”（movement、agreement）；-ance、-ence 拉丁语，说“…的状态、表现”，和形容词的 -ant、-ent 成对（importance、difference）；-ure、-age、-al 多是借词带来的，说“…的结果、过程”，-age 还说“总量、费用”（pressure、marriage、arrival）',
 'n_qual': '同样是把形容词变成名词，说“…的性质、状态”：-ness 英语本族，什么形容词都能接（happiness、kindness）；-ity 拉丁语，多接拉丁语、法语来的形容词，更书面，-ty 是它的短写法（popularity、ability、safety）；-ce、-cy 专配 -ant、-ent 结尾的形容词，把 t 换成 ce、cy（importance、frequency）；-th 英语本族的老后缀，只留在几个常用词里，元音常跟着变（warmth、length、strength）',
 'n_person': '同样是说“人”：-er 英语本族，动词后是“做这件事的人或东西”，最常用（driver、maker）；-or 拉丁语，作用和 -er 一样，接拉丁语动词，多接过去分词词干（actor、inventor）；-ist 希腊语，名词后是“干这一行、信这一套主张的人”（artist、scientist）；-ian、-an 拉丁语，地名、学科名后是“某地的人、精通某门学问的人”（musician、Italian）；-ee 法语，和 -er 相对，动词后是“被…的人”（employee、interviewee）',
 'n_status': '这几个多接名词，变成另一个名词：-ship 说“关系、身份、本事”（friendship、leadership）；-hood 说“…的时期、身份”，也指这一类人的全体（childhood、neighbourhood）；-dom 名词后是“…管的地方”（kingdom），形容词后是“…的状态”（freedom）；-ism 希腊语，说“主义、学说、一贯的做法”，也指行当，信它、干它的人用 -ist（realism、tourism）；-ery 说“这一行的手艺、这类东西的总称、干这事的地方”，-ry 是短写法（bakery、scenery）',
 'n_dim': '这几个本来都表示“小”：-let 还能造新词，名词后是“小的…”（booklet、droplet）；-ling 说“幼小的、刚长出来的”，多指小动物、小苗（duckling、seedling）；-ie 口语叫法，带亲昵、随意的味道，也写成 -y（auntie、sweetie）；-et、-ette 法语，-et 的“小”多已看不出，-ette 还说“小型的”（pocket、cigarette）；-cle、-ule、-le、-el 多是拉丁语的小称词尾，跟着整个词借进来，多已看不出“小”（particle、capsule、circle、parcel）',
 'v_make': '同样是变成动词，说“使…”：-en 英语本族，多接短形容词，说“使变得更…”（widen、shorten）；-ize 希腊语，最能造新词，接名词、形容词，说“使…化、照…的样子办”，英式多写 -ise（modernize、organize）；-ify 拉丁语，说“使成为…”，和 -ize 相近，-fy 是短写法（simplify、classify）；-ate 不是后加的后缀，是英语借拉丁语动词带来的词尾，这类动词多有配套的 -ation 名词（create、educate）',
 'adv': '同样是变成副词：-ly 英语本族，形容词后是“以…的方式、…地”，最常用（sadly、loudly）；-ally 是 -ic 结尾的形容词变副词的写法（basically）；-ward、-wards 英语本族，接方向词，说“朝…方向”，英式多用 -wards（forward、backward）；少数短词形容词、副词同形，不加 -ly（hard、late）',
 'cmp': '同样表示比较：-er、-est 英语本族，接短的形容词、副词：-er 是“更…”（later），-est 是“最…”（latest）；三个音节以上的长词不加词尾，前面用 more、most（more beautiful）；少数常用词不规则，要单独记（better、best）',
 'neg': '同样表示“不”：un- 英语本族，最常用：形容词前是“不…的”（unhappy、unkind），动词前是“把动作反过来、解开”（unlock、undo）；in- 拉丁语，接拉丁语、法语来的形容词，说“不…的”，b、m、p 前写 im-，l 前写 il-，r 前写 ir-（incorrect、impossible、illegal、irregular）；dis- 本义“分开”，动词、名词前是“相反的动作、不再…”（disagree、disappear）；non- 名词、形容词前，只客观地说“不是、不属于”，不带好坏（non-verbal、non-profit）；mis- 动词、名词前，不是“不做”，是“做错、弄坏”（misunderstand、misuse）',
 'over': '同样是“在上面、超过”：over- 英语本族：动词前是“越过、做过头”（overflow、oversleep），形容词前是“太…、超过”（overweight）；super- 拉丁语，名词、形容词前是“超级的、比一般大得多、强得多”（supermarket、superstar）；sur- 是 super- 经法语变来的写法，只在法语借词里，说“在…上面、超出”（surface、surplus）',
 'under': '同样是“在下面”：under- 英语本族：名词前是位置“在…下面”（underground、underwater），动词前是程度“不够、不足”（underestimate）；sub- 拉丁语，说“在下面、往下”（subway、submarine），名词前还是“低一级的、分出来的”（subtitle）；suc-、suf-、sug-、sup-、sus- 都是 sub-，随后面的字母变写法，常说“从下面往上”（support、suggest、sustain）',
 'out': '同样是“向外、出来”：out- 英语本族：名词前是“外面的、往外的”（outside、outdoor），动词前是“比…更好、超过”（outrun）；ex- 拉丁语，动词词根前是“往外、出去”，有时只加强语气“彻底”（export、exit、expand）；e-、ef- 都是 ex-，f 前写 ef-，d、l、m、v 等前写 e-（effect、emit、elect）',
 'into': '同样是“向里、进入”：in- 拉丁语，动词词根前是“往里、进入”，b、m、p 前写 im-，l、r 前写 il-、ir-（include、inject、import）；en- 是 in- 经法语变来的写法，b、m、p 前写 em-，接形容词、名词造动词：形容词前是“使变得…”（enlarge、enable），名词前是“使处于…、使有…”（endanger、empower）',
 'with': '同样是“一起”：com- 拉丁语，动词词根前是“凑到一起”，有时只加强语气“完全”，用在 b、m、p 前（combine、compare、complete）；con-、col-、cor- 都是 com-，l 前写 col-，r 前写 cor-，别的辅音前多写 con-（connect、collect、correct）；co- 是 com- 在元音和 h 前的写法，还能造新词，名词、动词前是“共同、合伙”（cooperate、coworker、co-author）；syn- 希腊语，多在学科、技术词里，说“合在一起、同时”，b、m、p 前写 sym-（synonym、symbol、symphony）',
 'before': '同样和“前面”有关：pre- 拉丁语，表示时间、顺序上的“先”：名词、形容词前是“…之前的”（preschool、prehistoric），动词词根前是“预先做”（predict、prepare）；pro- 拉丁语，多表示方向上的“向前”，不是时间上的“先”：动词词根前是“往前走、往前送、往前推”（progress、produce、promote）；fore- 英语本族，接本族词：名词前是“前面的部分”（forehead、foreground），动词前是“预先”（forecast）',
 'self': '同样是“自己”：self- 就是单词 self，名词、形容词前是“对自己、靠自己”，加连字符（self-control、self-confidence、self-respect）；auto- 希腊语，多在机器、技术词里，说东西“自己会动、不用人管”（automatic、automobile、automation）',
 'ad': '这几个都是拉丁语前缀 ad-：ad- 动词词根前是“朝着、加到…上”，有时只加强语气（adapt、adopt、admit）；ac-、af-、ag-、al-、an-、ap-、ar-、as-、at- 都是 ad-，d 变成后面的字母，所以常有两个一样的辅音连在一起（accept、affect、apply、arrive、assist、attract）',
 'between': '同样和“中间、穿过”有关：inter- 拉丁语：名词、形容词前是“…之间的”（international、Internet），动词前是“互相”（interact）；trans- 拉丁语，多在动词词根前，说“从这边到那边、穿过、转变”（transport、translate、transform）；mid- 英语本族，时间、地点名词前是“正中间的”（midnight、midday、midsummer）',
}
# 2026-11 词缀关系轮（project_rules.md 第 89–92 条）。用户：“pro-、pre- 这两个都是拉丁语，除了说含义上的区别，还要看看两者之间的关系，pro- 是 pre- 的分词吗？
# 就像 duc 和 duct 这样；来自同种语言的前后缀，不同形态，是不是存在这种关系，如果有就写出来，没有就算了”。
# REL[辨析组] = 关系的话：这一组里来自同一种语言、写法不同的词缀彼此是什么关系——同一个词尾的两种写法（-ant / -ent 跟着动词原形走）、
#   谁加了什么变成谁（-ation = at + -ion、-ance = -ant + -ia）、是不是某种语法形式（-ee 是法语过去分词的词尾）、还是各有来历的兄弟（pre- / pro-）。
#   一条讲一组词缀，条首写词缀（“-ant、-ent 是…”“pre- 和 pro- 不是…”），“；”隔开，没有句号；括号里是补充（拉丁语原词、源头、例词：总表里的词），
#   视频写在画面上、配音不念。只写查得到出处的（etymonline 整站数据逐条对过）；词典自己说“也许”的照写“词典说也许 / 多半”。
#   辨析那几条里已经讲了的（con-、col- 都是 com-；sur- 是 super- 经法语变来的；-ty 是 -ity 的短写法）、记法里已经讲了的（pro ≈ for、super ≈ over、sub ≈ up、un ≈ no、ly ≈ like）不重复；
#   每一行的来历里已经写了的（名词的 -al 来自 -alia、-age 来自 -aticum）也不重复；关系里的话不能和这一组某一行自己的讲法打架
#   （bakery 那一行讲的是 bake + ery，所以 -ery 那一条不举“baker → bakery”）。
#   没有关系的不写（neg、into、over、under、out、with、ad、self、cmp、adj_n 十组没有这一段）。
# 写进表：接在这一组辨析的最后“…（例词）；关系：…”。GROUP 是整句（辨析 + 关系），CORE 是不带关系的辨析（上一版总表里的句子，cizhui.py 靠它认出要补、要改关系的行）。
REL = {
 'before': 'pre- 和 pro- 不是谁变出谁，是拉丁语两个同源介词（prae“在前面”、pro“向前”，都来自印欧语词根 *per-）；fore- 和 pre-、pro- 同源，但是英语本族前缀，不是从拉丁语借来的（古英语 fore 也来自 *per-，p 变成了 f）',
 'between': 'inter- 是拉丁语介词 in 加上表示“两者之间”的 -ter（在两个的里面就是“之间”），和表示“向里”的前缀 in- 同源；trans- 词典说也许本是拉丁语动词“穿过”的现在分词（“正在穿过的”），末尾的 ns 和 -ant、-ent 是同一个现在分词词尾',
 'adj_v': '-ant、-ent 是同一个拉丁语现在分词词尾，原形 -are 的用 -ant，-ere、-ire 的用 -ent，经法语来的常写 -ant（important、different、assistant）；-able、-ible 是同一个拉丁语后缀（-bilis），-are 的动词带 a，-ere、-ire 的带 i；-ing 对着拉丁语的 -ant、-ent，都是现在分词，-ed 对着拉丁语过去分词的 t，都是过去分词；-ive、-ory 都接过去分词词干，和 -ion、-or 是一套（act → active、action、actor）',
 'n_act': '-ation 不是另一个后缀，是 -are 动词过去分词的标志 at 加 -ion，所以 -ate 动词变名词正好是 -ation（educate → education）；-ance、-ence 是 -ant、-ent 加拉丁语名词词尾 -ia，经法语磨成现在的样子，写 a 还是 e 跟着 -ant、-ent 走；-ion、-ure 都接过去分词词干，所以前面常是 t 或 s（action、pressure）',
 'n_qual': '-ity、-ty 是同一个拉丁语后缀（-tas），-ity 多带了词干的 i，-ty 是经法语磨短的；-ce、-cy 是 -ant、-ent 的 t 加名词词尾 -ia，t 和 i 合念成 s，写成 ce、cy（important → importance、frequent → frequency）；-th 在 h 后有时变成 -t（high → height）',
 'n_person': '-or 接拉丁语过去分词词干，和 -ion、-ive 是一套（act → actor、action、active）；-er 和 -or 不是同一种语言的，-er 是英语本族的，词典说也许很早借自拉丁语 -arius“干…的人”，-eer、-ier 是 -arius 经法语变来的；-ee 是法语过去分词词尾（-é，来自拉丁语 -atus，和 -ate 是同一个），所以是“被…的人”，和 -er、-or 配成一对；-ian 就是 -an，多带一个 i；-ist 和 -ism、-ize 是希腊语一套，-ize 是做，-ism 是主张，-ist 是做的人',
 'n_status': '-ism 和 -ist、-ize 是希腊语一套，-ize 是做，-ism 是主张、行当，-ist 是做的人；-ery 是法语 -erie，由表示“干这一行的人”的 -er 加名词词尾 -y 合成，说这一行、干这事的地方，-ry 是短写法',
 'n_dim': '-ette 是 -et 的阴性形式（法语名词分阴阳）；-let 是 -el 加 -et，两个表示“小”的词尾叠在一起；-cle、-ule、-el、-le 都出自拉丁语小称词尾 -ulus，多一个 c 是 -culus（-cle），叠两层是 -ellus（-el），经法语磨短成 -le；-ling 词典说多半是 -le 加 -ing，本来不表示“小”',
 'v_make': '-fy、-ify 里的 f 就是词根 fac“做”（拉丁语 -ficare），经法语磨成 fy，名词 -fication 里 fic 又露出来（classify → classification）；-ate 是拉丁语 -are 动词过去分词的词尾（-atus），at 是过去分词的标志，和 duct 的 t 一样，所以 -ate 动词配 -ation 名词（educate → education）；-ize 和 -ism、-ist 是希腊语一套，-ize 是做，-ism 是主张，-ist 是做的人',
 'adv': '-ly 当副词词尾和当形容词词尾（friendly）本是同一个古英语词（lic“样子”），副词本来多一个 e（-lice），e 掉了才写成一样；-ally 是 -al 加 -ly；-wards 是 -ward 加一个古英语副词词尾 s，nowadays 末尾的 s 也是它',
}
CORE = dict(GROUP)
DEMO_SKIP = {'more beautiful', 'hard'}      # 演示词没有等式、逐个看过的：视频这一个用法不画演示
PREV_CORE = {
 'adj_n': '同样是把名词变成形容词：-ful 是英语自己的，接日常的名词，说“充满…的、带来…的”（careful、useful）；-less 也是英语自己的，和 -ful 正好相反，说“没有…的”（careless、useless）；-y 是英语自己的，接日常的短词，说“有…的、…多的”，口语味最浓（rainy、sunny）；-ish 是英语自己的，说“有点像…的、带点…味道的”，常带贬义，也表示国籍、语言（childish、English）；-ly 是英语自己的，多接表示人的名词，说“有…样子的、像…一样的”，接在形容词后面才是副词（friendly）；-ous 是跟着法语、拉丁语的词进来的，说“充满…的、有…特点的”（dangerous、famous）；-al、-ic 也是外来的，只说“和…有关的、属于…的”，不带别的意思，书面的词、学科的词多用它们，两个还能叠成 -ical，意思多半不变，少数词分了工（national、basic、historic、historical）',
 'adj_v': '同样是把动词变成形容词：-ive 多接拉丁语动词的过去分词词干，说“主动会…的、有…作用的”，讲的是东西自己的性质（active、creative）；-able 说“能被…的、值得…的”，讲的是别人能对它做什么，英语自己造词都用它，-ible 是它在拉丁语借来的词里的写法（usable、visible）；-ing 说“正在…的、让人…的”，就是动词的现在分词当形容词用，多讲东西给人的感觉，和 -ed 正好一对（interesting、exciting）；-ed 说“被…了的、感到…的”，就是动词的过去分词当形容词用，多讲人自己的感受，和 -ing 相对，不规则动词用 -en（interested、excited、taken）；-ant、-ent 说“正在…着的、处在…状态的”，只留在拉丁语、法语来的词里，写哪一个照原词（important、different）；-ory 在拉丁语里也接过去分词词干，说“起…作用的、用来…的”（introductory、sensory）',
 'n_act': '同样是把动词变成名词：-ing 是英语自己的，什么动词都能接，说“做这件事、这项活动”（reading、swimming）；-ion 接拉丁语来的动词，接在它的过去分词词干后面，最多、最正式，说“这个行为”，也指它的结果，英语自己造词多用 -ation（action、invention、organization）；-ment 多接法语来的动词，常说“做成的结果、用来…的东西”（movement、agreement）；-ance、-ence 说“…的状态、表现”，和形容词的 -ant、-ent 成对（importance、difference）；-ure、-age、-al 多是整个借来的词带着的，说“…的结果、过程”，-ure 在拉丁语里也接过去分词词干，-age 还说“总量、费用”（pressure、marriage、arrival）',
 'n_qual': '同样是把形容词变成名词，说“…的性质、状态”：-ness 是英语自己的，什么形容词都能接，日常的词都用它（happiness、kindness）；-ity 是拉丁语来的，多接拉丁语、法语来的形容词，更书面，-ty 是它的短写法（popularity、ability、safety）；-ce、-cy 专门配 -ant、-ent 结尾的形容词，把 t 换成 ce、cy（importance、frequency）；-th 是很老的本族后缀，只留在几个常用词里，不再造新词，加上它元音常跟着变（warmth、length、strength）',
 'n_person': '同样是说“人”：-er 是英语自己的，接在动词后面，说“做这件事的人或东西”，最常用，新词都用它（driver、maker）；-or 作用和 -er 一样，只接拉丁语来的动词，多接在它的过去分词词干后面，多是整个借来的词（actor、inventor）；-ist 接在名词后面，说“专门干这一行、信这一套主张的人”（artist、scientist）；-ian、-an 接在地名、学科名后面，说“某个地方的人、精通某一门学问的人”（musician、Italian）；-ee 正好和 -er 相对，说“被…的人、接受这个动作的人”（employee、interviewee）',
 'n_status': '这几个多接在名词后面，变成另一个名词：-ship 说“两个人之间的关系、当…的身份、当…的本事”（friendship、leadership）；-hood 说“当…的那段时期、那种身份”，也指这一类人的全体（childhood、neighbourhood）；-dom 也接形容词，说“…管的地方、…的状态”（kingdom、freedom）；-ism 是希腊语来的，说“主义、学说、一贯的做法”，也指一个行当，信它、干它的人用 -ist（realism、tourism）；-ery 说“干这一行的手艺、这一类东西的总称、干这事的地方”，-ry 是它的短写法（bakery、scenery）',
 'n_dim': '这几个本来都表示“小”：-let 现在还能造新词，接在名词后面说“小的…”（booklet、droplet）；-ling 说“幼小的、刚长出来的”，多指小动物、小苗（duckling、seedling）；-ie 是口语里的叫法，带着亲昵、随意的味道，也写成 -y（auntie、sweetie）；-et、-ette 来自法语，-et 的“小”多半已经看不出来，-ette 还说“小型的”（pocket、cigarette）；-cle、-ule、-le、-el 多是拉丁语的小称词尾，跟着整个词借进来，英语本族也有一个表示“小”的 -el、-le，多半都已经看不出“小”的意思（particle、capsule、circle、parcel）',
 'v_make': '同样是变成动词，说“使…”：-en 是英语自己的，多接本族的短形容词，说“使变得更…”（widen、shorten）；-ize 最能造新词，接名词、形容词，说“使…化、照…的样子办”，英式多写 -ise（modernize、organize）；-ify 接拉丁语来的词，说“使成为…、做成…”，和 -ize 意思相近，-fy 是它的短写法（simplify、classify）；-ate 不是后来加上去的后缀，是英语借拉丁语动词时带着的词尾，这类动词多半有配套的 -ation 名词（create、educate）',
 'adv': '同样是变成副词：-ly 说“以…的方式、…地”，最常用，形容词后面基本都加它（sadly、loudly）；-ally 是 -ic 结尾的形容词变副词时的写法，不直接加 -ly（basically）；-ward、-wards 接在表示方向的词后面，说“朝着…的方向”，英式多用 -wards（forward、backward）；少数短词形容词、副词同形，不加 -ly（hard、late）',
 'cmp': '同样是表示比较：-er 说“更…”，-est 说“最…”，接在短的形容词、副词后面（later、latest）；三个音节以上的长词不加词尾，前面用 more、most（more beautiful）；少数常用词不规则，要单独记（better、best）',
 'neg': '同样表示“不”：un- 是英语自己的，最常用，加在形容词前是“不…的”，加在动词前是“把做了的事反过来、解开”（unhappy、unkind、unlock、undo）；in- 是拉丁语来的，多接拉丁语、法语来的形容词，说“不…的”，在 b、m、p 前写成 im-，在 l 前写成 il-，在 r 前写成 ir-（incorrect、impossible、illegal、irregular）；dis- 本义是“分开”，多加在动词、名词前，说“相反的动作、不再…”（disagree、disappear）；non- 加在名词、形容词前，只是客观地说“不是、不属于这一类”，不带好坏（non-verbal、non-profit）；mis- 加在动词、名词前，不是“不做”，是“做错了、弄坏了”（misunderstand、misuse）',
 'over': '同样是“在上面、超过”：over- 是英语自己的，接日常的词，说“从上面越过去”，更常说“过了头、太多”（overflow、oversleep、overweight）；super- 是拉丁语来的，加在名词、形容词前，说“超级的、比一般的大得多、强得多”（supermarket、superstar）；sur- 是 super- 经法语变来的样子，只留在法语来的词里，说“在…上面、超出”，英语不拿它造新词（surface、surplus）',
 'under': '同样是“在下面”：under- 是英语自己的，接日常的词，说位置“在…下面”，也说程度“不够、不足”（underground、underwater、underestimate）；sub- 是拉丁语来的，说“在下面、往下”，加在名词前还表示“低一级的、分出来的一小部分”（subway、submarine、subtitle）；suc-、suf-、sug-、sup-、sus- 都是 sub-，跟着后面的字母变了写法，这时常说“从下面往上”（support、suggest、sustain）',
 'out': '同样是“向外、出来”：out- 是英语自己的，接日常的词，在名词前说“外面的、往外的”，在动词前还说“比…做得更好、超过”（outside、outdoor、outrun）；ex- 是拉丁语来的，接在动词词根前，说动作“往外、出去”，有时只是加强语气“彻底”（export、exit、expand）；e-、ef- 都是 ex-，在 f 前写成 ef-，在 d、l、m、v 等字母前简写成 e-（effect、emit、elect）',
 'into': '同样是“向里、进入”：in- 是拉丁语来的，接在动词词根前，说动作“往里、进到里面”，在 b、m、p 前写成 im-，在 l、r 前写成 il-、ir-（include、inject、import）；en- 是 in- 经法语变来的样子，英语拿它接在名词、形容词前造动词，说“使变得…、把…放进…里”，在 b、m、p 前写成 em-（enable、enlarge、endanger、empower）',
 'with': '同样是“一起”：com- 是拉丁语来的，接在动词词根前，说“凑到一起、合到一处”，有时只是加强语气“完全”，用在 b、m、p 前面（combine、compare、complete）；con-、col-、cor- 都是 com-，跟着后面的字母变了写法，l 前写 col-，r 前写 cor-，别的辅音前多写 con-（connect、collect、correct）；co- 是 com- 在元音和 h 前的写法，英语现在还拿它自己造词，加在名词、动词前说“共同、合伙”（cooperate、coworker、co-author）；syn- 是希腊语来的，多见于学科、技术的词，说“合在一起、同时”，在 b、m、p 前写成 sym-（synonym、symbol、symphony）',
 'before': '同样和“前面”有关：pre- 拉丁语，表示时间、顺序上的“先”，加在名词、形容词前是“…之前的”，接在动词词根前是“预先做”（preschool、prehistoric、prepare、predict）；pro- 也是拉丁语，多表示方向上的“向前”，不是时间上的“先”，接在动词词根前是“往前走、往前送、往前推”，和 pre- 只差一个字母，别弄混（progress、produce、promote）；fore- 英语自己的，接日常的本族词，在名词前指“前面的那一部分”，在动词前是“预先”（forehead、foreground、forecast）',
 'self': '同样是“自己”：self- 就是单词 self，接在名词、形容词前，说人“对自己、靠自己、自己管自己”，后面加连字符（self-control、self-confidence、self-respect）；auto- 是希腊语来的，多用在机器、技术的词里，说东西“自己会动、不用人来管”（automatic、automobile、automation）',
 'ad': '这几个都是同一个拉丁语前缀 ad-：ad- 接在动词词根前，说动作“朝着…去、加到…上面”，有时只是加强语气（adapt、adopt、admit）；ac-、af-、ag-、al-、an-、ap-、ar-、as-、at- 都是 ad-，后面的字母是什么，d 就变成什么，所以这些词里常有两个一样的辅音字母连在一起（accept、affect、apply、arrive、assist、attract）',
 'between': '同样和“中间、穿过”有关：inter- 说“在两个、几个之间”，加在名词、形容词前是“…之间的”，加在动词前是“互相”（international、Internet、interact）；trans- 说“从这一边到那一边”，多接在动词词根前，是“穿过去、转过去、变成另一个样子”（transport、translate、transform）；mid- 是英语自己的，接在表示时间、地点的名词前，说“正中间的那一段”（midnight、midday、midsummer）',
}
PREV_REL = {
 'before': 'pre- 和 pro- 不是一个变出另一个（不像 duc、duct 那样是动词原形和过去分词），它们是拉丁语里两个同源的介词（prae“在前面”、pro“向前”，都来自印欧语词根 *per-“向前”）；fore- 和 pre-、pro- 同源，但它是英语本族的前缀，不是从拉丁语来的（古英语 fore 也来自 *per-，印欧语的 p 到英语这一支变成 f，这叫格林定律）',
 'between': 'inter- 是拉丁语的介词 in 加上表示“两个比一比”的 -ter 长出来的（in 是“在里面”，在两个的里面就是“之间”），和表示“向里”的前缀 in- 是一家；trans- 词典说也许本来是一个拉丁语动词“穿过”的现在分词（“正在穿过去的”），末尾的 ns 和 -ant、-ent 是同一个现在分词词尾',
 'adj_v': '-ant、-ent 是同一个拉丁语现在分词词尾的两种写法，动词原形是 -are 的用 -ant，是 -ere、-ire 的用 -ent，经法语进来的词常一律写成 -ant（important、different、assistant）；-able、-ible 是同一个拉丁语后缀（-bilis），前面的元音是动词带来的，-are 的动词带 a，-ere、-ire 的动词带 i；-ing 对着拉丁语的 -ant、-ent，都是现在分词，-ed 对着拉丁语过去分词的 t（-ate、act 里的 t），都是过去分词，往上各是同一个老后缀；-ive、-ory 都接在拉丁语动词的过去分词词干后面，和 -ion、-or 是一套，所以一个词干能配出一串词（act → active、action、actor）',
 'n_act': '-ation 不是另一个后缀，是 -are 动词过去分词的标志 at 加上 -ion，所以 -ate 结尾的动词变名词正好是 -ation（educate → education）；-ance、-ence 是形容词的 -ant、-ent 加上拉丁语名词词尾 -ia（-antia、-entia），经法语磨成现在的样子，写 a 还是 e 跟着 -ant、-ent 走；-ion、-ure 在拉丁语里都接在过去分词词干后面，所以它们前面常是 t 或 s（action、pressure）',
 'n_qual': '-ity、-ty 是同一个拉丁语后缀（-tas），-ity 只是前面多带了词干的 i，-ty 是经法语磨短的样子；-ce、-cy 是 -ant、-ent 的 t 加上拉丁语名词词尾 -ia，t 和 i 合起来念成 s 的音，写成 ce、cy（important → importance、frequent → frequency）；-th 在 h 后面有时磨成 -t（high → height）',
 'n_person': '-or 在拉丁语里接在过去分词词干后面，和 -ion、-ive 是一套，所以一个词干能配出一串词（act → actor、action、active）；-er 和 -or 不是同一种语言里的词尾，-er 是英语自己的，词典说它很早以前也许借自拉丁语 -arius“干…的人”，-eer、-ier 是这个 -arius 经法语变来的样子；-ee 是法语过去分词的词尾（-é，往上是拉丁语的 -atus，和 -ate 是同一个），所以是“被…的人”，和“做…的人”的 -er、-or 正好配成一对；-ian 就是 -an，前面多带了一个 i；-ist 和 -ism、-ize 是希腊语里的一套，-ize 是做，-ism 是这样做的一套主张，-ist 是这样做的人',
 'n_status': '-ism 和 -ist、-ize 是希腊语里的一套，-ize 是做，-ism 是这样做的一套主张、一个行当，-ist 是这样做的人；-ery 是法语的 -erie，本来是表示“干这一行的人”的 -er 再加一个名词词尾 -y 合成的，说的是这一行、干这事的地方，-ry 是它的短写法',
 'n_dim': '-ette 是 -et 的阴性形式，法语的名词分阴阳，本来是同一个后缀；-let 是 -el 加 -et，两个表示“小”的词尾叠在一起；-cle、-ule、-el、-le 都出自拉丁语的小称词尾 -ulus，前面多一个 c 是 -culus（-cle），叠两层是 -ellus（-el），经法语磨短就剩 -le；-ling 词典说多半是 -le 加 -ing，本来不表示“小”',
 'v_make': '-fy、-ify 里的 f 就是词根 fac“做”（拉丁语 -ficare），经法语磨成了 fy，所以它的名词写成 -fication，fic 又露出来（classify → classification）；-ate 是拉丁语 -are 动词过去分词的词尾（-atus），at 是过去分词的标志，和 duct 的 t 是一回事，所以 -ate 的动词配 -ation 的名词（educate → education）；-ize 和名词的 -ism、-ist 是希腊语里的一套，-ize 是做，-ism 是这样做的一套主张，-ist 是这样做的人',
 'adv': '-ly 当副词词尾和当形容词词尾（friendly）本是同一个古英语词（lic“样子”），副词本来多一个 e（-lice），后来 e 掉了，两个才写成一样；-ally 是 -al 加 -ly；-wards 是 -ward 加上一个老的副词词尾 s，nowadays 末尾的 s 也是它',
}
GROUP = {g: t + ('；关系：' + REL[g] if g in REL else '') for g, t in CORE.items()}
A = lambda idt, grp: (idt, grp)
SUF = {
 # —— 形容词
 ('-ful', '形容词'): A('英语本族的形容词后缀（就是 full“满”），接在名词后面，说“充满…的、带来…的”', 'adj_n'),
 ('-y', '形容词'): A('英语本族的形容词后缀（古英语 -ig），接在日常的短名词后面，说“有…的、多…的”，口语味最浓', 'adj_n'),
 ('-ish', '形容词'): A('英语本族的形容词后缀（古英语 -isc），说“像…的、有点…的”，也表示国籍、语言', 'adj_n'),
 ('-less', '形容词'): A('英语本族的形容词后缀（古英语 leas“没有”），接在名词后面，说“没有…的”，和 -ful 正好相反', 'adj_n'),
 ('-ly', '形容词'): A('英语本族的后缀（古英语 -lic“有…样子的”），接在名词后面是形容词，说“像…的、有…样子的”；接在形容词后面才是副词', 'adj_n'),
 ('-like', '形容词'): A('就是单词 like“像”，接在名词后面，说“像…一样的”', 'adj_n'),
 ('-some', '形容词'): A('英语本族的形容词后缀（古英语 -sum），说“容易…的、让人…的”', 'adj_n'),
 ('-ous', '形容词'): A('拉丁语来的形容词后缀（-osus），经法语进入英语，说“充满…的、有…特点的”；多半跟着整个词一起借进来', 'adj_n'),
 ('-ious', '形容词'): A('-ous 前面带着词干的 i 的写法；-ous 是拉丁语来的形容词后缀，说“充满…的、有…特点的”', 'adj_n'),
 ('-al', '形容词'): A('拉丁语来的形容词后缀（-alis），接在拉丁语、法语来的名词后面，只说“和…有关的、属于…的”', 'adj_n'),
 ('-ial', '形容词'): A('-al 前面带着词干的 i 的写法；-al 是拉丁语来的形容词后缀，只说“和…有关的”', 'adj_n'),
 ('-ual', '形容词'): A('-al 前面带着词干的 u 的写法；-al 是拉丁语来的形容词后缀，只说“和…有关的”', 'adj_n'),
 ('-ar', '形容词'): A('-al 的另一种写法：词干里已经有 l，再接 -al 就有两个 l，拉丁语把后一个换成 r', 'adj_n'),
 ('-ic', '形容词'): A('希腊语、拉丁语来的形容词后缀（-ikos、-icus），多接希腊语来的名词（学科、物质、抽象的东西），说“…的、有…性质的”', 'adj_n'),
 ('-ical', '形容词'): A('-ic 再加 -al，两个后缀叠在一起，意思还是“…的”；有的词 -ic、-ical 分了工（historic 有历史意义的，historical 历史上的）', 'adj_n'),
 ('-ary', '形容词'): A('拉丁语来的形容词后缀（-arius），说“和…有关的”', 'adj_n'),
 ('-ese', '形容词'): A('拉丁语来的后缀（-ensis“属于某地的”），经意大利语、法语进入英语，表示国籍、语言', 'adj_n'),
 ('-ive', '形容词'): A('拉丁语来的形容词后缀（-ivus），接在动词后面（多是过去分词词干），说“主动会…的、有…作用的”', 'adj_v'),
 ('-able', '形容词'): A('拉丁语来的形容词后缀（-abilis），经法语进入英语，接在动词后面，说“能被…的、值得…的”；英语自己造词都用它', 'adj_v'),
 ('-ible', '形容词'): A('-able 的另一种写法（拉丁语 -ibilis），只出现在整个从拉丁语借来的词里，英语自己造词不用它', 'adj_v'),
 ('-ent', '形容词'): A('拉丁语现在分词（“正在…的”形式）的词尾 -ens，接在动词后面；写 -ent 还是 -ant 照拉丁语原词', 'adj_v'),
 ('-ant', '形容词'): A('拉丁语现在分词（“正在…的”形式）的词尾 -ans，接在动词后面；写 -ant 还是 -ent 照拉丁语原词', 'adj_v'),
 ('-ient', '形容词'): A('-ent 前面带着词干的 i 的写法；-ent 是拉丁语现在分词（“正在…的”形式）的词尾', 'adj_v'),
 ('-ing', '形容词'): A('动词的现在分词（“正在…的”形式）当形容词用，英语本族的词尾', 'adj_v'),
 ('-ed', '形容词'): A('动词的过去分词（“被…了的”形式）当形容词用，英语本族的词尾；接在名词后面是“有…的”', 'adj_v'),
 ('-en', '形容词'): A('不规则动词的过去分词词尾（古英语 -en），当形容词用是“被…了的”', 'adj_v'),
 ('-ory', '形容词'): A('拉丁语来的形容词后缀（-orius），接在过去分词词干后面，说“起…作用的、用来…的”', 'adj_v'),
 # —— 名词：动作、结果
 ('-ion', '名词'): A('拉丁语来的名词后缀（-io），接在拉丁语来的动词（过去分词词干）后面，说“…这件事、…的结果”', 'n_act'),
 ('-ation', '名词'): A('-ion 带着过去分词标志 at 的样子，英语把它当成一个现成的后缀，自己造词也直接加它', 'n_act'),
 ('-ment', '名词'): A('拉丁语来的名词后缀（-mentum），经法语进入英语，接在动词后面，说“…的结果、用来…的东西”', 'n_act'),
 ('-ing', '名词'): A('英语本族的名词后缀（古英语 -ung、-ing），什么动词都能接，说“做这件事”，也指做出来的东西', 'n_act'),
 ('-ance', '名词'): A('拉丁语来的名词后缀（-antia），和形容词的 -ant 成对，说“…的状态、…这件事”', 'n_act'),
 ('-ence', '名词'): A('拉丁语来的名词后缀（-entia），和形容词的 -ent 成对，说“…的状态、…这件事”', 'n_act'),
 ('-ure', '名词'): A('拉丁语来的名词后缀（-ura），接在过去分词词干后面，说“…的结果、…的过程”', 'n_act'),
 ('-age', '名词'): A('法语来的名词后缀（-age，往上是拉丁语 -aticum），说“…这件事、…的总量、…的费用”', 'n_act'),
 ('-al', '名词'): A('拉丁语来的名词后缀（-alia，就是形容词词尾 -alis 的复数形式当名词用），接在动词后面，说“…这件事”', 'n_act'),
 # —— 名词：性质、状态
 ('-ness', '名词'): A('英语本族的名词后缀（古英语 -nes），什么形容词都能接，说“…的性质、状态”', 'n_qual'),
 ('-ity', '名词'): A('拉丁语来的名词后缀（-itas），经法语进入英语，接在拉丁语、法语来的形容词后面，说“…的性质、状态”', 'n_qual'),
 ('-ty', '名词'): A('-ity 的短写法（拉丁语 -itas 经法语 -té），说“…的性质、状态”', 'n_qual'),
 ('-ce', '名词'): A('-ance、-ence 的一部分：-ant、-ent 结尾的形容词变名词，把 t 换成 ce', 'n_qual'),
 ('-cy', '名词'): A('拉丁语来的名词后缀（-cia、-tia），-ant、-ent 结尾的形容词变名词时写成 -ancy、-ency', 'n_qual'),
 ('-th', '名词'): A('很老的英语本族名词后缀（古英语 -þ），把形容词、动词变成名词，今天不再用它造新词', 'n_qual'),
 # —— 名词：人
 ('-er', '名词'): A('英语本族的名词后缀（古英语 -ere），接在动词后面，说“做这件事的人或东西”', 'n_person'),
 ('-or', '名词'): A('拉丁语来的名词后缀（-or），接在拉丁语来的动词（过去分词词干）后面，说“做这件事的人或东西”', 'n_person'),
 ('-ist', '名词'): A('希腊语来的名词后缀（-istēs），接在名词后面，说“干这一行、信这一套的人”', 'n_person'),
 ('-ian', '名词'): A('拉丁语来的后缀（-ianus），说“某个地方、某一门学问的人”', 'n_person'),
 ('-an', '名词'): A('拉丁语来的后缀（-anus），说“属于某个地方、某一类的人”', 'n_person'),
 ('-ee', '名词'): A('法语来的名词后缀（-é，法语过去分词词尾），说“被…的人”，和 -er 相对', 'n_person'),
 ('-eer', '名词'): A('法语来的名词后缀（-ier），说“干这一行、管这件事的人”', 'n_person'),
 ('-ess', '名词'): A('法语来的名词后缀（-esse），表示女性', 'n_person'),
 ('-ier', '名词'): A('法语来的名词后缀（-ier），说“干这一行的人”', 'n_person'),
 # —— 名词：身份、集体
 ('-ship', '名词'): A('英语本族的名词后缀（古英语 -scipe），接在名词后面，说“身份、关系、本事”', 'n_status'),
 ('-hood', '名词'): A('英语本族的名词后缀（古英语 -had“状态”），接在名词后面，说“身份、时期”', 'n_status'),
 ('-dom', '名词'): A('英语本族的名词后缀（古英语 -dom“判定、领地”），说“领域、状态”', 'n_status'),
 ('-ism', '名词'): A('希腊语来的名词后缀（-ismos），说“主义、学说、做法”', 'n_status'),
 ('-ery', '名词'): A('法语来的名词后缀（-erie），说“这一行、这类东西、干这事的地方”', 'n_status'),
 ('-ry', '名词'): A('-ery 的短写法（法语 -erie），说“这一行、这类东西”', 'n_status'),
 # —— 名词：小称
 ('-et', '名词'): A('法语来的小称后缀（-et），本来表示“小”', 'n_dim'),
 ('-ette', '名词'): A('法语来的小称后缀（-ette，-et 的阴性），表示“小”', 'n_dim'),
 ('-let', '名词'): A('法语来的小称后缀（-el 加 -et），英语现在还用它表示“小”', 'n_dim'),
 ('-ling', '名词'): A('英语本族的小称后缀，表示“小的、幼小的”', 'n_dim'),
 ('-ie', '名词'): A('英语里表示“小、亲昵”的后缀（也写 -y）', 'n_dim'),
 ('-cle', '名词'): A('拉丁语的小称词尾（-culus），本来表示“小”', 'n_dim'),
 ('-ule', '名词'): A('拉丁语的小称词尾（-ulus、-ula），本来表示“小”', 'n_dim'),
 ('-le', '名词'): A('拉丁语小称词尾（-ulus、-ellus）经法语留下的样子，本来表示“小”', 'n_dim'),
 ('-el', '名词'): A('拉丁语小称词尾（-ellus）经法语留下的样子，本来表示“小”', 'n_dim'),
 # —— 动词
 ('-ize', '动词'): A('希腊语来的动词后缀（-izein），经拉丁语、法语进入英语，接在名词、形容词后面，说“使…化、使成为…”', 'v_make'),
 ('-ise', '动词'): A('-ize 的英式写法（照法语 -iser）；希腊语来的动词后缀，说“使…化、使成为…”', 'v_make'),
 ('-ify', '动词'): A('拉丁语来的动词后缀（-ificare，里面的 fic 就是“做”），经法语进入英语，说“使成为…”', 'v_make'),
 ('-fy', '动词'): A('-ify 的短写法（拉丁语 -ficare“做成”），说“使成为…”', 'v_make'),
 ('-ate', '动词'): A('拉丁语过去分词词尾 -atus 留下的动词词尾：英语借拉丁动词时常借它的过去分词，去掉 -us 就成了 -ate', 'v_make'),
 ('-en', '动词'): A('英语本族的动词后缀，接在本族的短形容词、名词后面，说“使变得…”', 'v_make'),
 # —— 副词
 ('-ly', '副词'): A('英语本族的副词后缀（古英语 -lice），接在形容词后面，说“以…的方式”', 'adv'),
 ('-ally', '副词'): A('-ic 结尾的形容词变副词时的写法：先加 -al 再加 -ly', 'adv'),
 ('-ward', '副词'): A('英语本族的后缀（古英语 -weard“朝向”），说方向', 'adv'),
 ('-wards', '副词'): A('-ward 加副词词尾 -s 的样子，说方向，英式多用', 'adv'),
 # —— 比较
 ('-er', '形容词'): A('比较级词尾，英语本族的，说“更…”', 'cmp'),
 ('-est', '形容词'): A('最高级词尾，英语本族的，说“最…”', 'cmp'),
}
NEG = '不|没有|否定|相反|非'
PRE = {
 'un-': A('英语本族的否定前缀（古英语 un-）', 'neg'),
 'in-': [(NEG, '拉丁语来的否定前缀，接拉丁语来的形容词', 'neg'), ('里|进|入|内', '拉丁语来的前缀“向里、进入”，和英语的 in 同源', 'into')],
 'im-': [(NEG, '否定前缀 in- 在 b、m、p 前的写法', 'neg'), ('里|进|入|内', '前缀 in-“向里”在 b、m、p 前的写法', 'into')],
 'il-': [(NEG, '否定前缀 in- 在 l 前的写法', 'neg'), ('里|进|入|内', '前缀 in-“向里”在 l 前的写法', 'into')],
 'ir-': [(NEG, '否定前缀 in- 在 r 前的写法', 'neg'), ('里|进|入|内', '前缀 in-“向里”在 r 前的写法', 'into')],
 'dis-': A('拉丁语来的前缀，本义“分开”，多加在动词、名词前，说“相反、不再”', 'neg'),
 'non-': A('拉丁语来的前缀（non“不”），只是客观地说“不是、非”', 'neg'),
 'mis-': A('英语本族的前缀（古英语 mis-），说“错、坏”', 'neg'),
 'over-': A('英语本族的前缀，就是介词 over', 'over'),
 'super-': A('拉丁语来的前缀（super“在上面”）', 'over'),
 'sur-': A('super- 经法语变来的样子', 'over'),
 'under-': A('英语本族的前缀，就是介词 under', 'under'),
 'sub-': A('拉丁语来的前缀（sub“在下面”）', 'under'),
 'suf-': A('前缀 sub- 在 f 前的写法', 'under'),
 'sup-': A('前缀 sub- 在 p 前的写法', 'under'),
 'suc-': [('sub|下|后面', '前缀 sub- 在 c 前的写法', 'under')], 'sug-': [('sub|下', '前缀 sub- 在 g 前的写法', 'under')],
 'sus-': [('sub|下', '前缀 sub- 在 c、p、t 前的写法（subs- 简化来的）', 'under')],
 'out-': A('英语本族的前缀，就是副词 out', 'out'),
 'ex-': A('拉丁语来的前缀（ex“出、离开”）', 'out'),
 'e-': [('ex-|出|外', '前缀 ex- 的简写（在 d、m、l、v 等字母前）', 'out')],          # e-book 的 e-（electronic）、enough 的 e- 不算
 'ef-': A('前缀 ex- 在 f 前的写法', 'out'),
 'en-': A('拉丁语 in- 经法语变来的样子，常用来造动词', 'into'),
 'em-': A('前缀 en- 在 b、m、p 前的写法', 'into'),
 'com-': A('拉丁语来的前缀（cum“和…一起”），在 b、m、p 前的写法', 'with'),
 'con-': A('拉丁语前缀 com-“一起”最常见的写法', 'with'),
 'col-': A('前缀 com-“一起”在 l 前的写法', 'with'),
 'cor-': A('前缀 com-“一起”在 r 前的写法', 'with'),
 'co-': A('前缀 com-“一起”在元音和 h 前的写法；英语现在也拿它自己造词', 'with'),
 'syn-': A('希腊语来的前缀（syn“一起”）', 'with'),
 'sym-': A('希腊语前缀 syn-“一起”在 b、m、p 前的写法', 'with'),
 'fore-': A('英语本族的前缀，就是 fore“前面”', 'before'),
 'pre-': A('拉丁语来的前缀（prae“在前”）', 'before'),
 'pro-': A('拉丁语来的前缀（pro“向前”）', 'before'),
 'self-': A('英语本族的前缀，就是单词 self“自己”', 'self'),
 'auto-': A('希腊语来的构词成分（autos“自己”）', 'self'),
 'ad-': A('拉丁语来的前缀（ad“向、到”）本来的样子', 'ad'),
 'ac-': A('前缀 ad-“向、到”在 c、q 前的写法', 'ad'), 'af-': A('前缀 ad-“向、到”在 f 前的写法', 'ad'),
 'ag-': [('ad-', '前缀 ad-“向、到”在 g 前的写法', 'ad')], 'al-': [('ad-', '前缀 ad-“向、到”在 l 前的写法', 'ad')], 'an-': [('ad-', '前缀 ad-“向、到”在 n 前的写法', 'ad')],
 'ap-': A('前缀 ad-“向、到”在 p 前的写法', 'ad'), 'ar-': A('前缀 ad-“向、到”在 r 前的写法', 'ad'),
 'as-': A('前缀 ad-“向、到”在 s 前的写法', 'ad'), 'at-': A('前缀 ad-“向、到”在 t 前的写法', 'ad'),
 'inter-': A('拉丁语来的前缀（inter“在…之间”）', 'between'),
 'trans-': A('拉丁语来的前缀（trans“越过、到另一边”）', 'between'),
 'mid-': A('英语本族的前缀，就是 mid“中间的”', 'between'),
}

# 逐个看过的例外（见文件开头）：下面两张表由体检对着总表定下来，加新词时照样补
NO_BX = {      # (单词, 标签)：这一行讲的不是目录里那个词缀（希腊语的 en-、英语自己的 in、electronic 缩成的 e-、拉丁语形容词词尾 -est……），不挂辨析
 ('advance', 'ad-'), ('afford', 'af-'), ('cellar', '-ar'), ('liar', '-ar'), ('poplar', '-ar'), ('seminar', '-ar'),
 ('solidarity', '-ar'), ('astonish', 'as-'), ('police', '-ce'), ('twice', '-ce'), ('jury', '-y'), ('embryo', 'em-'), ('empathy', 'em-'),
 ('alien', '-en'), ('dozen', '-en'), ('energy', 'en-'), ('enthusiasm', 'en-'), ('enthusiast', 'en-'), ('maiden', '-en'),
 ('corner', '-er'), ('register', '-er'), ('honest', '-est'), ('modest', '-est'), ('comet', '-et'), ('barrier', '-ier'),
 ('frontier', '-ier'), ('inland', 'in-'), ('insight', 'in-'), ('Viking', '-ing'), ('companion', '-ion'), ('recognise', '-ise'),
 ('recognize', '-ize'), ('proportion', 'pro-'), ('moisture', '-ure'),
 # 2026-11 词缀关系轮核对“人”那一组时发现的：表示“状态”的拉丁语名词词尾 -or、表示“一下一下地做”的动词词尾 -er、archivum 的词尾 -ive，都不是这一组讲的那个词缀
 ('tumor', '-or'), ('terror', '-or'), ('tremor', '-or'), ('error', '-or'), ('horror', '-or'), ('clutter', '-er'), ('archive', '-ive'),
}
FORCE = {      # (单词, 标签): 辨析组 —— 开头的介绍绕了个弯（“这里不是“不”，而是“把动作反过来””“看着像…，其实对应拉丁语 -arius“从事…的人””），规则挑不出来，逐个定的
 ('plumber', '-er'): 'n_person', ('guardian', '-ian'): 'n_person', ('puddle', '-le'): 'n_dim', ('arguably', '-ly'): 'adv',
 ('insure', 'in-'): 'into', ('undo', 'un-'): 'neg',
 ('relaxing', '-ing'): 'adj_v',      # 这一行自己说“这里是②…让人…的”（形容词）；组合列的词性变化写成了“动词 → 名词”（那一格没改，第 87 条 ②）
}

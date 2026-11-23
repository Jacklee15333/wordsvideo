"""动词变化形式轮：第一批。每个词：l1 组合列第一行（None 表示照旧）；st 步骤；P 音变列新写的部分（原有的【同形异义】等标签段落自动留在后面）；
可选 segdrop（组合列要去掉的段落）、segrep（换掉的段落）、pdrop（音变列要去掉的标签段落）。"""
from vhelp import PT, PPT, PPI, AT, AI, GVS

E = {}

E['made'] = dict(
 l1='make（做）→ made =“做了；被做出来的”',
 st=[PT('做了'), PPT('做', '已经做好了；被做成（be made of 由…做成）'),
     AT('做', '…制造的、…做成的（made in China 中国制造；homemade 自制的）', '，说东西是怎么来的')],
 P=f"""【字母变化】macode（古英语）→ makede（中古英语）→ made（中古英语、英语）
① 古英语 macian“做”是规则（弱变化）动词：过去式在词干 mac- 后面加 -ode（macode），过去分词加 -od（gemacod），和今天 play → played 一样是“加词尾”。
② 到中古英语，词尾 -ode 弱化成 -ede；c 改写成 k（c 在 e 前面会被念成 s，写 k 才保住 k 音）：macode → makede（过去分词 maked）。
③ 关键的一步：k 夹在两个元音中间，口语里越念越轻，最后掉了；它后面那个弱读的 e 也一起并掉，ma-ke-de 三个音节缩成 ma-de 两个：makede → made（过去分词 maked 也缩成 maad、made）。所以中间没有 maed 这一步：k 一掉，a 就拉成长音，末尾的 e 是过去式词尾 -de 剩下的，当时还念 /ə/。
④ 后来词尾的 e 不念了，made 成了一个音节；这个不发音的 e 正好留下来，当作前面 a 读长音的记号（同 name、take、came）。{GVS}，/aː/ 成了 /eɪ/，所以读 /meɪd/。had 也是这样缩来的：古英语 hæfde，中间的 f 并进后面的 d，成了 hadde、had。""")

E['learnt'] = dict(
 l1='learn（学）→ learnt =“学了；被学会了”',
 st=[PT('学过、学会了；得知了'), PPT('学会', '已经学会了；被学会'), '（形容词“有学问的”只写 learned，见【辨析】）'],
 P="""learn 是规则动词（古英语 leornian – leornode），过去式、过去分词本来都加 -ed。-ed 读 /d/ 还是 /t/ 看前面的音；近代英语里一批以 l、n、m 结尾的动词，-ed 常读成清音 /t/，拼写也就照读音写成 t：learned → learnt（同 burn → burnt、spell → spelt、smell → smelt、dream → dreamt）。英式两种都用，美式几乎只用 learned。""")

E['thought'] = dict(
 l1='think（想）→ thought =“想了；被想到的；想出来的东西”',
 st=[PT('想了、认为过'), '# 过去分词：跟在 have 后面是“已经想过了”，跟在 be 后面是“被认为” → 已经想过了；被认为（It is thought that… 人们认为…）',
     '→ 当名词：想出来的东西 → 想法、念头',
     '　用词规律：表示动作的词，也拿来叫这个动作做出来、留下来的东西（thought：想出来的东西 → 想法、念头；invention 发明 → 发明物）',
     '→ “想”这个过程 → 思考', '→ 很多人一代代想出来、成了体系的 → 思想', '→ 心里替别人想着 → 关心、心意'],
 P="""【字母变化】thohte（古英语）→ thoughte（中古英语）→ thought（英语）
① 古英语 þencan“想”（þ 就是 th，链里写成 th）是规则（弱变化）动词，过去式本该是“词干 + -te”：词干 thank- 碰上 t，k 先念成喉音 h（像德语 ach 的 ch），n 也掉了，前面的元音拉长，念成长音 o：*thank-te → thohte（过去分词 geþoht）。现在时那边，a 受后面 -j- 音的影响变成了 e（þencan），中古英语又在 nk 前变成 i：think。所以 think 和 thought 长得不像。
② 中古英语用 gh 来写这个喉音 h，长音 o 写成 ou：thohte → thoughte。
③ 词尾的 e 不念了，去掉；gh 的喉音后来也不念了，ou 读 /ɔː/：thoughte → thought，读 /θɔːt/（同 brought、bought、sought、fought）。""")

E['shown'] = dict(
 st=[PPT('展示', '已经给人看了、已经表明了；被展示、被放映'), AT('展示', '被展示的；（电影）被放映的')],
 P="""show 原是规则动词（古英语 scēawian“看”– scēawode），过去分词本来是 showed；shown 是后来照 know – known、blow – blown、sow – sown 加上 -n 的，今天更常用（两种都对）。show 的读音以元音结尾，-n 直接加在后面。""")

E['took'] = dict(
 l1='take（拿）→ took =“拿了”',
 st=[PT('拿了、带走了；花了（时间）；乘坐了；接受了')],
 P=f"""【字母变化】tok（北欧语）→ took（英语）
① take 是古英语晚期从古北欧语 taka“拿、抓”借来的（取代了古英语 niman），借来时连变化一起借：taka – tók – tekinn，是强变化动词，过去式靠把 a 换成长音 o 表示“过去”（同 shake → shook）。
② 中古英语写 tok、toke，o 读长音；后来用双写的 oo 表示这个长音：tok → took。{GVS}，/oː/ 成了 /uː/，后来又缩短成 /ʊ/（同 book、good、look），读 /tʊk/。""")

E['taken'] = dict(
 st=[PPT('拿', '已经拿了；被拿走'), AT('占', '（座位）有人的、已被占用的', '：座位已经被人“拿”了'),
     '→ 心被某样东西“拿”走了 →（be taken with）被…吸引、喜欢上', '→ 人已经被别人“拿”走了 →（口语）有对象的'],
 P="""【字母变化】tekinn（北欧语）→ taken（英语）
① 古北欧语 taka 的过去分词 tekinn“被拿了的”：a 受词尾 i 音的影响念成了 e，词尾 -inn 就是北欧语的过去分词词尾（相当于英语的 -en）。
② 进了英语，按英语自己的样子写：元音跟原形 take 一样用 a，词尾用英语的过去分词词尾 -en：tekinn → taken；a 读长音，后来经元音大推移读 /eɪ/，读 /ˈteɪkən/。""")

E['mistook'] = dict(
 l1='mistake（弄错）→ mistook =“弄错了”',
 st=[PT('误解了、弄错了；把…错当成了…')],
 P="""mistake – mistook – mistaken：mistake 是 13 世纪从古北欧语 mistaka“拿错”借来的，里面的 take 照 take – took – taken 变（见 took）。""")

E['said'] = dict(
 l1='say（说）→ said =“说了；被说过的”',
 st=[PT('说了、说过'), PPT('说', '已经说过了；被说（It is said that… 据说…）'),
     AT('说', '（法律、公文）上述的、该', '：前面已经说过的那个')],
 P="""【字母变化】seide（中古英语）→ said（英语）
① 古英语 secgan“说”是规则（弱变化）动词：过去式 sægde，加 -de；g 跟在元音后面念得像 y，中古英语就写成 seide、sayde（同 day ← dæg、way ← weg）。
② 拼写照 say 的样子把 ei 写成 ai，词尾的 e 不念、去掉：seide → said。读音本来是 /seɪd/，后来口语里说得多、念得快，缩短成 /sed/（同 says 读 /sez/）；pay → paid、lay → laid 没有缩短。""")

E['saw'] = dict(
 l1='see（看见）→ saw =“看见了”',
 st=[PT('看见了；明白了；见过面')],
 P="""【字母变化】sawon（古英语）→ sawe（中古英语）→ saw（英语）
① 古英语 sēon“看见”是强变化动词，靠换元音表示时态：sēon – seah（过去式单数）/ sāwon（过去式复数“我们、他们看见了”）– gesewen。今天的 saw 来自复数 sāwon 这一支（etymonline）。
② 中古英语里词尾 -on 弱化成 -e：sawon → sawe（单数那一支写 sagh、saugh，后来不用了）。
③ 词尾的 e 不念、去掉：sawe → saw，aw 读 /ɔː/。""")

E['seen'] = dict(
 st=[PPT('看见', '见过、已经看见了；被看见'), '→ 被别人“看成”某个样子（be seen as）→ 被看作、被视为',
     AT('看见', '（古）看得见的、明白的', '：一眼就看得见')],
 P="""【字母变化】gesewen（古英语）→ isene（中古英语）→ seen（英语）
① 古英语 sēon 的过去分词 gesewen（也写 gesegen）：前面带 ge-，后面带过去分词词尾 -en，中间的 w 是原来词干里的辅音。
② 到中古英语，ge- 念轻，写成 i- / y-；中间的 w 掉了，e 拉长：gesewen → isene（也写 isen、sene）。
③ i- 也掉了，长音 e 照 see 写成 ee，词尾 -ne 只剩 -n：isene → seen，读 /siːn/。""")

E['oversaw'] = dict(
 l1='oversee（监督）→ oversaw =“监督了”',
 st=[PT('监督了、主管了')],
 P="""oversee – oversaw – overseen：oversee 里的 see 照 see 变（见 saw）。古英语 oferseon 已有“俯视、看守、察看”义。""")

E['found'] = dict(
 l1='find（找到）→ found =“找到了；被找到的”',
 st=[PT('找到了、发现了', '（找的过程结束了）'), PPT('找到', '已经找到了；被找到、被发现'),
     AT('发现', '被发现的；（法庭上）被判定的')],
 segrep={'语法': '【语法】find – found – found：过去式、过去分词同形'},
 P=f"""【字母变化】funden（古英语）→ founden（中古英语）→ found（英语）
① 古英语 findan“找到”是强变化动词，靠换元音表示时态：findan – fand – funden（过去式 a，过去分词 u）。今天的 found 来自过去分词 funden 这一支，后来过去式也改用它，fand 就不用了。
② u 在 nd 前面拉长成 /uː/，中古英语照法语习惯把长音 u 写成 ou：funden → founden（同 bind → bound、grind → ground、wind → wound）。
③ 词尾 -en 掉了：founden → found；{GVS}，/uː/ 成了 /aʊ/，所以读 /faʊnd/。""")

E['got'] = dict(
 l1='get（得到）→ got =“得到了；已经得到”',
 st=[PT('得到了；到达了；变得（…了）'), '# 过去分词：英式里跟在 have 后面，说“已经得到了” → 已经得到了；已经变得（英式）',
     '→ have got 本来是“已经得到”：东西已经到手，现在就在你这儿 →（英式口语）have got = 有',
     '→ have got 等于 have，所以 have to（不得不）也说成 have got to → 不得不'],
 P="""【字母变化】gat（中古英语）→ got（英语）
① get 是约 1200 年从古北欧语 geta 借来的（古英语自己的同源词只留在 forget、beget 里），是强变化动词：过去式 gat，过去分词 geten、goten。
② 后来过去式也改用过去分词里的 o：gat → got（钦定本《圣经》里还有 gat、begat）；英式过去分词也缩成了 got，美式保留老样子 gotten。""")

E['gotten'] = dict(
 st=['# 过去分词：美式里跟在 have 后面，说“已经弄到了、已经变得” → 已经得到了、弄到了；已经变得（美式）',
     '→ 美式分了工：have got 说“有”，have gotten 说“弄到了、变得”（见【辨析】）'],
 P="""【字母变化】goten（中古英语）→ gotten（英语）
① 中古英语 get 的过去分词 geten、goten，带强变化动词的过去分词词尾 -en（etymonline：gotten 留着古英语那一支动词的痕迹）。
② 短元音 o 后面的 t 双写，表示前面是短元音：goten → gotten（同 forgotten、written）。英式后来去掉 -en，只说 got；美式一直保留 gotten。""")

E['forgot'] = dict(
 l1='forget（忘记）→ forgot =“忘了”',
 st=[PT('忘了；忘带了')],
 P="""forget – forgot – forgotten：forget 里的 get 照 get 变（见 got）。古英语 forgietan 是强变化动词（过去式 forgeat），开头的 g 念 y；中古英语起照北欧来的 get 念硬音 g，过去式也跟着 get 改成 forgat、forgot。""")

E['forgotten'] = dict(
 st=[PPT('忘记', '已经忘了；被忘记'), AT('忘记', '被遗忘的', '：被大家忘掉了')],
 P="""forget 的过去分词保留了强变化动词的 -en：forgot + ten（短元音 o 后面 t 双写，同 gotten）。get 的过去分词英式已经缩成 got，forget 却一直是 forgotten。""")

E['born'] = dict(
 l1='bear（生）→ born =“被生下来的”',
 st=['# 过去分词：跟在 be 后面是“被生下来”，be born 就是“出生” → 出生（I was born in 2012.）',
     AT('生', '生来就是…的、天生的（a born teacher 天生当老师的料）', '：生下来就是这样的'),
     '→ 放在地名、国名后面 → …出生的（Beijing-born 北京出生的）'],
 P="""【字母变化】boren（古英语）→ born（英语）
① 古英语 beran“带着；生（孩子）”是强变化动词：beran – bær – boren，过去分词换成 o 再加 -en。
② 中古英语里，-en 前面那个弱读的 e 在 r 后面掉了：boren → born（同 swear → sworn、tear → torn、wear → worn）。17 世纪起拼写分了工：“出生”写 born，“承受、携带”写 borne。""")

E['bore'] = dict(
 l1='bear（扛；生；忍受）→ bore =“扛了；生了；忍受了”',
 st=[PT('承受了；生了；带有过')],
 P="""【字母变化】bare（中古英语）→ bore（英语）
① 古英语 beran“带着；生；忍受”是强变化动词：beran – bær – boren，过去式 bær（æ 读 /æ/）中古英语写成 bare。
② 约 1400 年起照过去分词 boren、born 的 o 改成 bore：bare → bore；但直到 1600 年以后书面语还常用 bare（钦定本《圣经》里写 she bare a son）。读 /bɔː/（同 tear → tore、swear → swore、wear → wore）。""")

E['felt'] = dict(
 l1='feel（感觉；摸）→ felt =“感觉到了；被感觉到的”',
 st=[PT('感觉到了、觉得；摸了；认为（过）'), PPT('感觉到', '已经感觉到了；被感觉到（The earthquake was felt in Tokyo. 东京也有震感）')],
 P="""【字母变化】felde（古英语）→ felte（中古英语）→ felt（英语）
① 古英语 fēlan“摸、感觉”是规则（弱变化）动词：过去式加 -de，fēlde，ē 是长音。
② 长元音碰上后面两个辅音（l + d）变短；词尾 -de 跟在 l 后面念成清音，写成 -te：felde → felte（同 dwell → dwelt、spell → spelt）。
③ 词尾的 e 不念了，去掉：felte → felt。原形 feel 的长 ee 经元音大推移读 /iː/，felt 的短 e 没变，所以一个读 /fiːl/，一个读 /felt/。""")

E['kept'] = dict(
 l1='keep（保持、留着）→ kept =“保持了；被保留的”',
 st=[PT('保持了；保留了；一直（做着）'), PPT('保留', '已经保留了；被保存、被照管'),
     AT('保存', '被保存着的、被照管着的（a well-kept garden 照料得很好的花园）')],
 P="""【字母变化】cepte（古英语）→ kepte（中古英语）→ kept（英语）
① 古英语 cēpan“抓住、留意”是规则（弱变化）动词：过去式在 p 后面加 -te，cēpte，ē 是长音。
② 长元音碰上后面两个辅音（p + t）变短；c 改写成 k：cepte → kepte（同 sleep → slept、weep → wept、sweep → swept）。
③ 词尾的 e 不念了，去掉：kepte → kept。原形 keep 的长 ee 经元音大推移读 /iː/，kept 的短 e 没变，读 /kept/。""")

E['told'] = dict(
 l1='tell（讲；数）→ told =“讲了；被告诉的；被数过的”',
 st=[PT('讲了、告诉了'), PPT('告诉', '已经告诉了；被告诉（I\'m told… 听说…）'),
     '→ 老意思“被数过的”：全都数进去 →（all told）总共、全部算上'],
 P="""【字母变化】tealde（古英语）→ tolde（中古英语）→ told（英语）
① 古英语 tellan“数、讲”是规则（弱变化）动词，过去式 tealde。现在时的 e 是 a 受后面 -j- 音影响变来的（*taljan → tellan，同 sell），过去式没有这个 -j-，保留了 a（写成 ea）。
② a 在 ld 前面拉长，后来变成长音 o（同古英语 ald → old、cald → cold）：tealde → tolde。
③ 词尾的 e 不念了，去掉：tolde → told，读 /təʊld/（同 sell → sold）。口语里 told 常读成 tole（1797 年已见于印刷品）。""")

E['became'] = dict(
 l1='become（变成）→ became =“变成了”',
 st=[PT('变成了、成为了')],
 P="""become – became – become：become 里的 come 照 come 变（见 came）；过去分词和原形同形。""")

E['came'] = dict(
 l1='come（来）→ came =“来了”',
 st=[PT('来了；到达了；发生了')],
 P=f"""【字母变化】kvam（北欧语）→ cam（中古英语）→ came（英语）
① 古英语 cuman“来”是强变化动词：cuman – cōm – cumen。今天的过去式一般认为来自古北欧语的 kvam（koma“来”的过去式），中古英语时取代了古英语的 cōm（etymonline 说“很可能”）。
② kv 念成 k，写成 c：kvam → cam。
③ a 后来读长音，加上不发音的 e 作记号：cam → came；{GVS}，读 /keɪm/。""")

E['wrote'] = dict(
 l1='write（写）→ wrote =“写了”',
 st=[PT('写了', '（笔已经停下，纸上留下了字）')],
 P=f"""【字母变化】wrat（古英语）→ wroot（中古英语）→ wrote（英语）
① 古英语 wrītan“刻、划、写”是强变化动词，不加 -ed，靠换元音表示时态：wrītan – wrāt – writen；过去式 wrāt 的 ā 是长音。
② 中古英语里长音 ā 变成长音 o，常双写成 oo：wrat → wroot（同 stān → stone、bān → bone、hām → home）。
③ 后来改用“o + 辅音 + 不发音的 e”表示长音 o：wroot → wrote；{GVS}，读 /rəʊt/，开头的 w 早已不念。""")

E['written'] = dict(
 l1='write（写）→ written =“被写下来的”',
 st=[PPT('写', '已经写了（I have written two letters.）；被写（It was written in 1850.）'),
     AT('写', '书面的（a written test 笔试；和 spoken 口头的相对）', '：用文字写下来')],
 P="""【字母变化】writen（古英语）→ written（英语）
① 古英语 wrītan 的过去分词 (ge)writen：元音 i 是短的（原形 wrītan 的 ī 是长的），后面加 -en。
② 短 i 后面的 t 双写，表示前面是短元音：writen → written；原形 write 的长 ī 经元音大推移读 /aɪ/，written 的短 i 没变，读 /ˈrɪtn/（同 ride → ridden、bite → bitten）。""")

E['rewrote'] = dict(
 st=[PT('重写了、改写了')],
 P="""rewrite – rewrote – rewritten：rewrite 里的 write 照 write 变（见 wrote）。""")

E['understood'] = dict(
 l1='understand（懂）→ understood =“懂了；被理解了的”',
 st=[PT('懂了、理解了'), PPT('理解', '已经懂了；被理解'),
     AT('理解', '不言而喻的、心照不宣的', '：大家早就懂了、不用说出来')],
 P="""understand – understood – understood：understand 里的 stand 照 stand 变（见 stood）：去掉现在时多出来的 n，元音 a 换成长音 o（古英语 understandan – understōd），后来写成 oo、读 /ʊ/。同类：withstand → withstood。""")

E['misunderstood'] = dict(
 st=[PT('误解了'), PPT('误解', '已经误解了；被误解'), AT('误解', '被误解的、不被理解的', '：别人一直没懂他、把他想错了')],
 P="""misunderstand – misunderstood – misunderstood：变化跟着 understand 走（见 understood）。""")

E['stood'] = dict(
 l1='stand（站）→ stood =“站了；已经站了”',
 st=[PT('站了、立过；经受住了、忍受了'), PPI('站', 'stand', '站过、已经站了一段时间')],
 P=f"""【字母变化】stod（古英语）→ stood（英语）
① 古英语 standan“站”是强变化动词：standan – stōd – standen。现在时的 n 是现在时专有的，过去式里没有；元音换成长音 o：stōd。
② 中古英语起长音 o 写成 oo：stod → stood；{GVS}，/oː/ 成了 /uː/，又缩短成 /ʊ/（同 good、foot），读 /stʊd/。过去分词原来是 standen，后来也改用 stood。同类：understand → understood、withstand → withstood。""")

E['woke'] = dict(
 l1='wake（醒）→ woke =“醒了”',
 st=[PT('醒了；叫醒了'), '→ 2010 年代起，口语拿“醒着”比喻“对社会不公看得清” →（adj.）有政治、社会觉悟的',
     '→ 后来常被批评者用作贬义（见【辨析】）'],
 P="""【字母变化】woc（古英语）→ woke（英语）
① 古英语有两个“醒”：强变化的 wacan（过去式 wōc，过去分词 wacen）和规则的 wacian（过去式 wacode），后来合成了今天的 wake。woke 来自强变化那一支的 wōc：靠把 a 换成长音 o 表示“过去”（同 take → took）。
② c 改写成 k，加上不发音的 e 表示 o 读长音：woc → woke；后来经元音大推移读 /wəʊk/。""")

E['woken'] = dict(
 l1='wake（醒、叫醒）→ woken =“已经醒了；被叫醒了的”',
 st=[PPT('叫醒', '已经醒了、已经叫醒了；被叫醒')],
 P="""【字母变化】wacen（古英语）→ woken（英语）
① 古英语强变化动词 wacan 的过去分词 wacen，元音和原形一样是 a，后面加 -en。
② 后来照过去式 woke 的 o 改成 woken（同 speak – spoke – spoken、break – broke – broken 这一类）：wacen → woken；美式也常用规则的 waked。""")

E['awoke'] = dict(
 l1='awake（醒来）→ awoke =“醒来了”',
 st=[PT('醒来了；唤醒了')],
 P="""awake – awoke – awoken，变化同 wake（见 woke）。古英语 āwacan“醒来”是强变化动词，过去式 āwōc；awoke、awoken 原本属于 awaken，后来才转给了 awake（见【演变】）。""")

E['built'] = dict(
 l1='build（盖）→ built =“盖了；被盖好的”',
 st=[PT('盖了、建了'), PPT('建', '已经建好了；被建造（The bridge was built in 1937.）'),
     AT('建', '建成的、造好的（purpose-built 专门建造的）'),
     '→ 说人的身体是怎么“搭”起来的 →（前面加副词）……体格的、身材……的（well-built 体格健壮的）'],
 P="""build 原是规则动词（古英语 byldan – bylde；中古英语 bilden – bilde、bilded），所以拆分写 built ← builded。以 -ld、-nd 结尾的动词，过去式的 -de、-ed 常和词尾的 d 并成一个清音 t：builded → built（同 send → sent、spend → spent、bend → bent）；builded 今天只在古旧文字里见到。u 不发音，是 build 本来的拼法（来历词典也说不清）。""")

E['rebuilt'] = dict(
 st=[PT('重建了'), PPT('重建', '已经重建了；被重建'), AT('重建', '翻新的', '：旧机器拆开重新装好')],
 P="""rebuild – rebuilt – rebuilt：变化跟着 build 走（见 built）。""")

E['been'] = dict(
 formsnote='：been 是过去分词，跟在 have 后面（have been）',
 st=['# 过去分词：跟在 have 后面，说从过去到现在一直“是”、一直“在” → 一直是、一直在（have been）',
     '→ 在某地“待过”又回来了 → 去过（have been to）',
     '→ 跟在 have 后面，再接别的动词的过去分词 → 构成完成时的被动语态（have been done）'],
 P="""be 的过去分词：古英语 bēon 这一支没有过去分词（“已经是”说 gewesen，属于 was 那一支）；13 世纪起照 seen、done 这些过去分词的样子，在 be 后面加 -n，造出 been（也写 ibeen、ben），慢慢顶替了 gewesen。读音英式 /biːn/，美式多读 /bɪn/。""")

E['swore'] = dict(
 l1='swear（发誓）→ swore =“发了誓”',
 st=[PT('发了誓、宣过誓；咒骂过')],
 P="""【字母变化】swor（古英语）→ swore（英语）
① 古英语 swerian“发誓”是强变化动词：swerian – swōr – sworen，过去式换成长音 o。
② 加上不发音的 e，表示 o 读长音：swor → swore，读 /swɔː/（同 bear → bore、tear → tore、wear → wore）。15–17 世纪还常用照 bear → bare 造的 sware，今天只见于古雅文字。""")

E['brought'] = dict(
 l1='bring（带来）→ brought =“带来了；被带来的”',
 st=[PT('带来了；导致了'), PPT('带来', '已经带来了；被带来'), '→ 被一点点往上“带”大 →（be brought up）被抚养长大'],
 P="""【字母变化】brohte（古英语）→ broughte（中古英语）→ brought（英语）
① 古英语 bringan“带来”的过去式是 brōhte（过去分词 brōht）：词干 brang- 碰上过去式的 -te，g 念成喉音 h，n 掉了，元音拉长成 o——和 think → thought 是同一种变化。
② 中古英语用 gh 写这个喉音 h，长音 o 写成 ou：brohte → broughte。
③ 词尾的 e 不念了，去掉；gh 后来也不念了，ou 读 /ɔː/：broughte → brought，读 /brɔːt/。""")

E['knew'] = dict(
 l1='know（知道、认识）→ knew =“知道了；认识了”',
 st=[PT('知道（了）；认识')],
 P="""【字母变化】cneow（古英语）→ knew（英语）
① 古英语 cnāwan“知道、认出”是强变化动词：cnāwan – cnēow – cnāwen，过去式把元音换成 ēo。
② c 改写成 k（kn 里的 k 当时还念），ēo 简化，写成 ew：cneow → knew；后来 k 不念了，读 /njuː/（美式 /nuː/）（同 grow → grew、throw → threw、blow → blew）。""")

E['known'] = dict(
 st=[PPT('知道', '已经知道了；被（大家）知道'), AT('知道', '知名的、出名的；已知的', '：被大家都知道'),
     '→ 被人知道是什么身份、因为什么出名 →（be known as / for）被称为…；以…出名'],
 P="""【字母变化】cnawen（古英语）→ knowen（中古英语）→ known（英语）
① 古英语 cnāwan 的过去分词 cnāwen：元音和原形一样是长音 ā，后面加 -en。
② 长音 ā 到中古英语变成长音 o，写成 ow；c 改写成 k：cnawen → knowen（同 stān → stone）。
③ -en 里弱读的 e 不念了，缩成 -n：knowen → known，读 /nəʊn/（同 grown、thrown、blown）。""")

E['meant'] = dict(
 l1='mean（意思是；打算）→ meant =“意思是；被打算好的”',
 st=[PT('意思是…；打算过'), '# 过去分词：跟在 have 后面是“已经打算了”，跟在 be 后面是“被（人或命运）安排好” → 已经打算好；被安排好',
     '→ 被安排好要做某事 →（be meant to）应该、本该', '→ 被安排给某人、某事的 →（be meant for）注定属于、天生适合'],
 P="""【字母变化】mente（中古英语）→ meant（英语）
① 古英语 mǣnan“意思是、打算”是规则（弱变化）动词，过去式 mǣnde；长元音碰上 n + d 变短，词尾在 n 后面念成清音 -te，中古英语写成 mente（同 dream → dreamt）。
② 后来拼写照 mean 写成 ea，词尾 e 去掉：mente → meant；读音还是短的 /ment/（拼写像 mean，读音是短 e）。""")

E['chose'] = dict(
 l1='choose（选择）→ chose =“选择了”',
 st=[PT('选择了、挑了')],
 P="""古英语 cēosan“选”是强变化动词：cēosan – cēas – coren；c 在 e 前面念 ch，后来就写成 ch。中古英语过去式写 chees，后来照过去分词 chosen 的 o 改成 chose（同 freeze → froze），读 /tʃəʊz/。""")

E['chosen'] = dict(
 l1='choose（选择）→ chosen =“被选中的”',
 st=[PPT('选', '已经选好了；被选中'), AT('选', '被选中的、精选的', '：从一群里被挑出来'),
     '→ 被上帝挑出来的那一群人 →（the chosen people）上帝的选民'],
 P="""【字母变化】coren（古英语）→ chosen（英语）
① 古英语 cēosan 的过去分词 coren：词干里的 s 在这里变成了 r（同 was / were 的 s / r 交替；lose 的老过去分词 loren 还留在 forlorn 里）。
② 约 1200 年照原形 choose 把 r 拉回成 s；开头也照原形写成 ch：coren → chosen，-en 不变，读 /ˈtʃəʊzn/。""")

E['lit'] = dict(
 st=[PT('点燃了、照亮了'), PPT('点燃', '已经点着了；被点亮、被照亮'), AT('点燃', '点着的、亮着的（moonlit 月光照耀的）'),
     '→（俚语）喝醉的（1914 年起）；（美国俚语）很棒的、很嗨的（可以这样记：人像被“点着”了一样，又红又兴奋）'],
 P="""【字母变化】lihte（古英语）→ lighte（中古英语）→ lit（英语）
① 古英语 līhtan“点燃、照亮”是规则（弱变化）动词：过去式在 t 后面加 -te，līhte；h 是喉音（像德语 ach 的 ch）。
② 中古英语用 gh 写这个喉音：lihte → lighte（同 night、light 的 gh）。
③ 过去式里的长元音变短，喉音和词尾的 e 都掉了，缩成 lit：lighte → lit（同 bite → bit、hide → hid）；规则的 lighted 也一直在用。""")

E['grew'] = dict(
 l1='grow（长）→ grew =“长了”',
 st=[PT('长了、长大了；增长了；种了；渐渐变得')],
 P="""【字母变化】greow（古英语）→ grew（英语）
① 古英语 grōwan“生长”是强变化动词：grōwan – grēow – grōwen，过去式把元音换成 ēo。
② ēo 简化，写成 ew：greow → grew，读 /ɡruː/（同 know → knew、throw → threw、blow → blew）。""")

E['grown'] = dict(
 st=['# 过去分词：跟在 have 后面是“已经长了”；作“种”讲时，跟在 be 后面是“被种” → 已经长了、已经变得；被种出来（home-grown 自家种的）', AI('长', '成年的、长成的', '：长大了、长成了')],
 P="""【字母变化】growen（古英语）→ grown（英语）
① 古英语 grōwan 的过去分词 grōwen：元音和原形一样，后面加 -en。
② -en 里弱读的 e 掉了，缩成 -n：growen → grown，读 /ɡrəʊn/（同 known、thrown、blown）。""")

E['outgrew'] = dict(
 keepsteps=True,
 st=[PT('长大后穿不下了；长大后不再有了；长得比…高了')],
 P="""outgrow – outgrew – outgrown：outgrow 里的 grow 照 grow 变（见 grew）。""")

E['gone'] = dict(
 st=[PPI('走', 'go', '（已经）走了、去了'), AI('走', '走了的、不在了的；（委婉）去世了的', '：人走了、不在这儿了'),
     '→ 东西被用得一点不剩，像都“走”光了 → 用光的', '→ 走掉了就回不来 → 无可挽回的、没救了的'],
 P="""【字母变化】gegan（古英语）→ ygon（中古英语）→ gone（英语）
① 古英语 gān“去”的过去分词 gegān：前面加 ge-，元音是长音 ā，末尾的 n 是过去分词的词尾。
② 到中古英语，ge- 念轻，写成 y-；长音 ā 变成长音 o（同 stān → stone）：gegan → ygon（也写 ygo、gon）。
③ y- 掉了，末尾加上不发音的 e：ygon → gone；后来元音变短，读 /ɡɒn/（美 /ɡɔːn/），和 go /ɡəʊ/ 分开了。""")

E['undergone'] = dict(
 st=['# 过去分词：跟在 have 后面，说“已经经历过了” → 经历过、经受过'],
 P="""undergo – underwent – undergone：undergo 里的 go 照 go 变（见 gone、went）。""")

E['went'] = dict(
 l1='wend（转身前往）→ went =“转身走了”',
 st=['→ 人掉转身子，朝另一头走开：“转过身走了”就是“去了” → 动身去了',
     '→ 意思和 go 的过去式一样，went 慢慢替 go 顶了班，把 go 原来的过去式 ēode 挤掉 → go 的过去式',
     PT('去了、走了')],
 P="""【字母变化】wende（古英语）→ went（英语）
① 古英语 wendan“转、转身前往”是规则（弱变化）动词，过去式 wende（词干的 d 和过去式的 -de 并成一个）；go 的过去式原来是 ēode（来源不明），和 go 长得完全不一样。
② 约 1200 年起，-nd 结尾的动词过去式里的 d 念成清音 t（同 send → sent、spend → spent）：wende → went。15 世纪 went 开始替 go 当过去式，到 1500 年左右完全取代了 ēode；wend 自己改用 wended。""")

E['underwent'] = dict(
 st=[PT('经历了、经受了')],
 P="""undergo – underwent – undergone：undergo 里的 go 照 go 变，过去式借用 went（见 went）。""")

E['gave'] = dict(
 l1='give（给）→ gave =“给了”',
 st=[PT('给了、送了')],
 P=f"""【字母变化】gaf（中古英语）→ gave（英语）
① 古英语 giefan“给”是强变化动词：giefan – geaf – giefen，开头的 g 念 y（中古英语写 yeven、yaf）。今天开头念硬音 g，一般认为是受北欧语 gefa – gaf – gefinn 的影响，过去式也成了 gaf。
② a 后来读长音，加上不发音的 e 作记号；f 夹在元音中间念 v，就写成 v（英语词尾不写 v，v 后面总跟个 e）：gaf → gave；{GVS}，读 /ɡeɪv/。""")

E['given'] = dict(
 st=[PPT('给', '已经给了；被给予（be given a book 得到一本书）'), AT('给定', '特定的、规定的', '：事先就“给定”、分配好'),
     '→ 已经摆在面前、当作前提的 →（介）考虑到、鉴于；（n.）既定事实、已知条件',
     '→ 人把自己“交给”了某种习惯 →（be given to）惯于、爱…'],
 P="""【字母变化】yeven（中古英语）→ given（英语）
① 古英语 giefan 的过去分词 giefen，开头的 g 念 y，中古英语写成 yeven、yiven。
② 一般认为受北欧语 gefinn 影响，开头改念硬音 g，写成 gi-；f 夹在元音中间念 v，写成 v：yeven → given，读 /ˈɡɪvn/（对比 gave 换了元音，given 的元音和原形一样）。""")

E['forgave'] = dict(
 st=[PT('原谅了')],
 P="""forgive – forgave – forgiven：forgive 里的 give 照 give 变（见 gave）。""")

E['forgiven'] = dict(
 st=[PPT('原谅', '已经原谅了；被原谅')],
 P="""forgive – forgave – forgiven：变化跟着 give 走（见 given），forgive 后面加 -n。""")

E['began'] = dict(
 l1='begin（开始）→ began =“开始了”',
 st=[PT('开始了')],
 P="""begin – began – begun：古英语 beginnan – began – begunnen 就是强变化动词，不加 -ed，靠换元音表示时态（i → a → u，同 sing – sang – sung、drink – drank – drunk）。过去式 began 的写法从古英语到今天没变（古英语里更常用的是 onginnan – ongann）。""")

E['begun'] = dict(
 l1='begin（开始）→ begun =“已经开始了的”',
 st=['# 过去分词：跟在 have 后面，说“已经开始了” → 已经开始了（Work has begun. 工作已经开始了）'],
 P="""【字母变化】begunnen（古英语）→ begun（英语）
① 古英语 beginnan 的过去分词 begunnen：元音换成 u，后面加 -en。
② 词尾 -en 掉了，nn 简化成 n：begunnen → begun（同 sing → sung、swim → swum、win → won）。""")

E['ran'] = dict(
 l1='run（跑）→ ran =“跑了”',
 st=[PT('跑了；（机器）运转了；经营了')],
 P="""run – ran – run：古英语 rinnan“跑、流”是强变化动词：rinnan – ran – runnen，过去式 ran 一千多年没变样。原形 run 的 u 是后来照过去分词 runnen 改的（中古英语里 rinnen、rennen、runnen 几种原形并存）；过去分词又丢了 -en，和原形一样是 run。""")

E['taught'] = dict(
 l1='teach（教）→ taught =“教了；被教过的”',
 st=[PT('教了'), PPT('教', '已经教了；被教'), AT('教', '受过训练的（多出现在复合词里：self-taught 自学的）', '：被人教过、练过')],
 P="""【字母变化】taughte（中古英语）→ taught（英语）
① 古英语 tǣcan“指给人看、教”是规则（弱变化）动词，过去式 tǣhte：c 碰上过去式的 -te，念成喉音 h，就和现在时 teach（c 念 ch）分开了；中古英语写成 taughte，gh 记喉音 h。
② 词尾的 e 不念了，去掉；gh 的喉音后来也不念了，au 读 /ɔː/：taughte → taught（同 catch → caught）。""")

E['spoke'] = dict(
 l1='speak（说）→ spoke =“说了”',
 st=[PT('说了、讲过')],
 P="""【字母变化】spak（中古英语）→ spoke（英语）
① 古英语 sprecan / specan“说”是强变化动词：sp(r)ecan – sp(r)æc – sp(r)ecen（中间的 r 后来掉了）；过去式中古英语写成 spak、spake。
② 后来照过去分词 spoken 的 o 改成 spoke：spak → spoke，读 /spəʊk/（spoken 的 o 又是照 stolen、broken 这一类来的；同 break → broke）。""")

E['spoken'] = dict(
 l1='speak（说）→ spoken =“被说出来的”',
 st=[PPT('说', '已经说了；被说、被讲'), AT('说', '口头的、口语的', '：用嘴说出来、不是写出来的'),
     '→ 和别的词合成，说一个人说话的样子 →（复合词里）说话…的（soft-spoken 说话温和的）'],
 P="""【字母变化】specen（古英语）→ spoken（英语）
① 古英语 sp(r)ecan 的过去分词 sp(r)ecen：元音和原形一样，后面加 -en。
② 中古英语照 stolen、broken 这一类强变化动词把元音改成 o，c 改写成 k：specen → spoken，读 /ˈspəʊkən/。""")

E['sat'] = dict(
 l1='sit（坐）→ sat =“坐了；已经坐了”',
 st=[PT('坐了、坐下了'), PPI('坐', 'sit', '坐过、已经坐了一段时间')],
 P="""sit – sat – sat：古英语 sittan“坐”是强变化动词：sittan – sæt – seten，过去式把元音换成 æ（读 /æ/），中古英语写成 sat。过去分词原来是 seten、sitten，后来也改用 sat；从前过去式也可以是 set（今只见于方言）和 sate（已古旧）。""")

E['broke'] = dict(
 l1='break（打破）→ broke =“打破了；（口）没钱了的”',
 st=[PT('打破了'),
     '→ 过去分词 broken 去掉 -en 也是 broke：一个商人的买卖“破”了，钱袋也空了 → 破产的 →（口语）身无分文的、没钱的'],
 P="""【字母变化】brak（中古英语）→ broke（英语）
① 古英语 brecan“打破”是强变化动词：brecan – bræc – brocen，过去式中古英语写成 brak、brake。
② 后来照过去分词 broken 的 o 改成 broke：brak → broke，brake 慢慢成了古旧说法。过去分词 broken 去掉 -en 也写 broke（14 世纪已见，17–18 世纪很常见），1716 年起当“没钱的”讲。""")

E['broken'] = dict(
 l1='break（打破）→ broken =“被打破了的”',
 st=[PPT('打破', '已经打破了；被打破'), AT('打破', '破碎的、坏了的；（骨头）断了的'),
     '→ 说好的约定被“打破”了 →（诺言）被违背的', '→ 心被“打碎”了 →（心）碎了的、伤心的',
     '→ 话说得一截一截、连不起来 →（语言）蹩脚的、不流利的', '→ 中间一次次被打断的 → 断断续续的'],
 P="""【字母变化】brocen（古英语）→ broken（英语）
① 古英语 brecan“打破”是强变化动词：brecan – bræc – brocen，过去分词换成 o 再加 -en。
② c 改写成 k：brocen → broken，读 /ˈbrəʊkən/（同 speak → spoken、steal → stolen）。""")

E['lost'] = dict(
 l1='lose（丢失）→ lost =“丢了；被弄丢了的”',
 st=[PT('丢了；输了'), PPT('弄丢', '已经丢了；被弄丢、被输掉'), AT('弄丢', '丢失的'),
     '→ 人找不到路 → 迷路的', '→ 已经输掉、注定要输的 → 失败的', '→ 听着听着找不到头绪 → 困惑的、糊涂的',
     '→ 时间、机会白白丢掉了 → 浪费的、错过的'],
 P="""【字母变化】losode（古英语）→ losed（中古英语）→ lost（英语）
① 古英语 losian“丢失、毁灭”是规则（弱变化）动词：过去式加 -ode，losode。
② 到中古英语，-ode 弱化成 -ed：losode → losed。
③ 中间的 e 不念了，s 和 d 挨在一起都念清音，d 写成 t：losed → lost；元音也变短，所以 lose 读 /luːz/，lost 读 /lɒst/（同 keep → kept）。""")

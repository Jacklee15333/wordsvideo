"""字母变化同源词轮（2026-11）：拆分写成 X ≈ Y 的 46 个外来词，音变列第一行写字母变化链，下面每一步一行。
每条：(行号, 单词, 新写的链和步骤, 照原文保留的段落, 新补的标签段落)。
链从这个词自己的源头写到它本身；≈ 两边的词是兄弟（同一个源头走了两条路），不是一个从另一个变来的，① 里讲清两者的关系。
原来那句讲变化的话由步骤取代；步骤里没讲到的原话补成标签段落（【短形式】【对照】【同类】【分工】）。中间形式、年代对照 etymonline 整站数据。"""

DATA = [
(422, 'apprentice',
"""【字母变化】apprehendere（拉丁语）→ apprendere（中世纪拉丁语）→ aprendre（古法语）→ aprentiz（古法语）→ apprentice（英语）
① 拉丁语 apprehendere：ap-pre-hen-de-re，“抓住”，用手抓、用脑子抓都行（ad“向”+ prehendere“抓”）；词根 prehend- 原样留在 apprehend 里。apprehend 是英语直接从拉丁语借的，apprentice 走的是法语这条路，两个是兄弟，不是谁从谁变来的。
② 口语里中间的 he 被吞掉，prehendere 缩成 prendere：apprehendere → apprendere；中世纪拉丁语里它已经当“学”讲（用脑子“抓住”）。
③ 到古法语，双写的 pp 简化成 p，没有重音的 e 被吞掉，词尾 -ere 磨成 -re：apprendere → aprendre“学；教”（今天法语 apprendre）。
④ 由动词造出名词“正在学的人”，d 在 t 前面脱落：aprendre → aprentiz（今天法语 apprenti）。
⑤ 约 1300 年进入英语，词尾的 z 写成 c，加上不发音的 e，后来又照拉丁语把 p 双写回去：aprentiz → apprentice，读 /əˈprentɪs/。""",
[], ['【短形式】英语里长期更常用的是截掉开头 ap- 的短形式 prentice']),

(1045, 'wait',
"""【字母变化】*wahton（法兰克语）→ waitier（北部古法语）→ waiten（中古英语）→ wait（英语）
① 法兰克语（征服高卢的日耳曼人说的话）*wahton：“守望、看守”（带 * 的是没留下文字、由后来的语言推出来的形式），和英语本族的 watch、wake 出自同一个日耳曼词干 *waht-。watch 一直留在英语里，wait 是先借进法语、再从法语借回英语的，两个是远亲，不是谁从谁变来的。
② 进了法语，法国人不会发 t 前面那个喉音 h，念成了元音 i（同拉丁 factum → 法语 fait、noctem → nuit），再加上法语动词词尾 -ier：*wahton → waitier。北部古法语保留开头的 w，中部古法语把 w 念成 g，写 gaitier（今天法语 guetter）。
③ 约 1200 年进入英语，换上英语动词词尾 -en：waitier → waiten“盯着、埋伏着等”。
④ 后来英语动词的词尾 -en 掉了（同 helpen → help）：waiten → wait；ai 原来读 /ai/，后来变成 /eɪ/，读 /weɪt/。""",
['【w ↔ g】北部法语保留日耳曼的 w，中部法语变成 g(u)：wait / guetter（同 ward / guard、warranty / guarantee、war / 法语 guerre）', '【同源】watch、wake'], []),

(1145, 'spice',
"""【字母变化】species（拉丁语）→ espice（古法语）→ spice（英语）
① 拉丁语 species：spe-ci-es，本义“外表、样子”，引申为“种类”，晚期拉丁语里又指“一种种货物”，尤其是香料（出自 specere“看”）；词根 spec- 原样留在 species、special 里。species 是英语原样借的拉丁词，spice 是走法语变了样的，两个本是同一个词。
② 到古法语，c 后面的元音挤在一起，-ecies 缩成 -ice；法国人不习惯词首直接念 sp，前面垫了个 e：species → espice（同拉丁 stabilis → 古法语 estable，英语 establish 也留着这个 e；今天法语 épice，é 就是这个 e）。
③ 约 1200 年进入英语，用的是英法语里不带 e- 的形式：espice → spice；i 读长音 /iː/，后来英语的长元音整体变了读法（元音大推移），/iː/ 成了 /aɪ/，所以读 /spaɪs/（同 nice、price）。""",
[], []),

(1231, 'premier',
"""【字母变化】primarius（拉丁语）→ premier（法语、英语）
① 拉丁语 primarius：pri-ma-ri-us，“头等的、首要的”，由 primus“第一”加 -arius 变来；词根 prim- 原样留在 primary、prime 里。primary 是英语直接从拉丁语借的同一个词，premier 走的是法语这条路，两个是兄弟。
② 到法语，词尾 -arius 变成 -ier（同拉丁 carpentarius → 法语 charpentier，英语 carpenter），没有重音的 i 念成 e，pri- 变成 pre-：primarius → premier“第一的、首席的”。
③ 15 世纪中原样进入英语，字母没再变；读 /ˈpremiə/（美式 /prɪˈmɪr/），1711 年起当名词指“首相”。""",
['【跨组同源】primary 是从拉丁直接借的同一个词'], []),

(1366, 'rail',
"""【字母变化】regula（拉丁语）→ *regla（俗拉丁语）→ reille（古法语）→ rail（英语）
① 拉丁语 regula：re-gu-la，“直木条、尺子”（出自 regere“使直、引导”）；词根 regul- 原样留在 regular、regulate 里。rule 是同一个 regula 走另一条路变来的（regula → reule → rule），rail 和 rule 是兄弟，不是谁从谁变来的。
② 俗拉丁语（老百姓说的口语拉丁语）里，中间没有重音的 u 被吞掉：regula → *regla（带 * 的是没留下文字、由后来的语言推出来的形式）。
③ 到古法语，g 和 l 并成一个“软 l”（舌面贴着上腭念的 l），法语写成 ill；前面的 e 跟着念成 ei，词尾 -a 磨成不发音的 e：*regla → reille“门闩、横杆”（同拉丁 vigilare → 法语 veiller；也写 raille）。
④ 约 1300 年进入英语，先写 raile、reile，后来定成 rail：软 l 在英语里念成普通的 l，ai 后来读 /eɪ/，所以读 /reɪl/。""",
['【同形异义】rail 还有动词“怒斥、抱怨”（rail against，← 古法语 raillier“取笑”）和水鸟“秧鸡”两个意思，都与本词无关'], []),

(1373, 'dress',
"""【字母变化】directus（拉丁语）→ *directiare（俗拉丁语）→ drecier（古法语）→ dresser（古法语）→ dress（英语）
① 拉丁语 directus：di-rec-tus，“摆直了的、直的”，是 dirigere“摆直”（dis- + regere“使直”）的“被…了的”形式；词根 rect- 原样留在 direct、correct 里。direct 是英语直接从拉丁语借的，dress 是走法语变了样的，两个是一家。
② 俗拉丁语用它造出动词“弄直”：去掉词尾 -us，加上动词词尾 -iare：directus → *directiare（带 * 的是推出来的形式）。
③ 到古法语，开头 di 的 i 没有重音，被吞掉，dir- 成了 dr-；-cti- 一串辅音简化成一个 ts 音，写成 c：*directiare → drecier“立起；摆好；弄直”（address 来自 adrecier，同理）。
④ ts 后来念成 s，写成 ss，动词词尾写成 -er：drecier → dresser（今天法语还写 dresser）。
⑤ 约 1300 年进入英语，法语的动词词尾不要了：dresser → dress，读 /dres/；14 世纪末起才有“打扮、穿衣”的意思。""",
['【同源】军队口令 dress ranks（排齐队列）还留着“摆直”的老意思；salad dressing（约 1500 年起的“调味汁”）、伤口的 dressing（1713 年起的“敷料”）都来自“整治好、处理好”'], []),

(1395, 'alert',
"""【字母变化】erecta（拉丁语）→ erta（意大利语）→ all'erta（意大利语）→ alerte（法语）→ alert（英语）
① 拉丁语 erecta：e-rec-ta，“竖起来的”，是 erigere“竖起”（e-“向上”+ regere“使直”）的“被…了的”形式；词根 rect- 原样留在 erect 里。erect 是英语直接借的拉丁词，alert 绕道意大利语、法语才来，两个是一家。
② 到意大利语，中间的 ec 被吞掉，erecta 成了 erta，当名词用，指“高处、瞭望台”：erecta → erta。
③ 前面加上 alla“到…去”，两个 a 并成一个，写成 all'：erta → all'erta“到高处去、上瞭望台”，是放哨时的喊声。
④ 17 世纪法语借过去，粘成一个词：ll 简化成 l，词尾 -a 换成不发音的 e：all'erta → alerte“警惕的”。
⑤ 1610 年代进入英语，词尾不发音的 e 去掉：alerte → alert，读 /əˈlɜːt/。""",
['【同源】erect（直立的）'], ['【对照】alarm ← all\'arme“拿起武器！”结构完全一样']),

(1403, 'reign',
"""【字母变化】regnum（拉丁语）→ reigne（古法语）→ reign（英语）
① 拉丁语 regnum：reg-num，“王权、统治；王国”，和 rex“国王”、regere“统治”同根；词根 reg- 原样留在 regent、regal 里。royal 是同一个词根经法语变来的另一个词（拉丁 regalis → 古法语 roial），reign 和 royal 是一家。
② 到古法语，gn 念成一个“软 n”（舌面贴着上腭念的 n，像西班牙语 ñ），前面的 e 跟着念成 ei，就写成 eign；词尾 -um 磨成不发音的 e：regnum → reigne（今天法语 règne）。
③ 13 世纪初进入英语，先写 regne，后写 reigne、reign：软 n 在英语里念成普通的 n，g 只留在拼写里，不发音（同 sign、campaign）；ei 后来读 /eɪ/，所以读 /reɪn/。""",
['【易混】reign 和 rain（雨）、rein（缰绳）同音，三者来源各不相同；give sb free rein（放手让人干）原是“放松缰绳”，常被误写成 free reign'], []),

(1649, 'essay',
"""【字母变化】exagium（拉丁语）→ essai（古法语）→ essay（英语）
① 晚期拉丁语 exagium：ex-a-gi-um，“称一称、分量”，出自 exigere“赶出来；要求；检验”（ex-“出”+ agere“推动”）；词根 ag- 原样留在 agent、act 里。examine 出自同一个 exigere 一族（examen“秤舌”），essay 和 examine 是一家：都是“放到秤上称一称”。
② 到古法语，x（ks）里的 k 被吞掉，剩下的 s 写成 ss（同 exire → issir，见 issue）；夹在元音中间的 g 念轻、脱落，-agium 缩成 -ai：exagium → essai“尝试、试验”。
③ 1590 年代进入英语，词尾的 i 照英语习惯写成 y（同 array、delay）：essai → essay，读 /ˈeseɪ/；“短文”这个意思最早见于培根，很可能是仿蒙田的《随笔》（Essais），意思是“试着写写”。""",
['【同源】assay“（金属成色的）化验”与 essay 同出一词（etymonline 提示对照 assay）'], []),

(2009, 'allow',
"""【字母变化】allocare（拉丁语）→ aloer（古法语）→ allouen（中古英语）→ allow（英语）
① 拉丁语 allocare：al-lo-ca-re，“放到…去、拨给”（ad“向”+ locare“放置”，ad 在 l 前写成 al）；词根 loc- 原样留在 allocate、local 里。allocate 是英语直接借的拉丁词，allow 走的是法语这条路，两个是“双胞胎”（古法语里另有一个来自 allaudare“称赞”的 aloer，两个撞成了一个词，见单词部分）。
② 到古法语，夹在两个元音中间的 c 越念越轻，最后脱落；ll 简化成 l，动词词尾 -are 变成 -er：allocare → aloer（同 locare → louer“出租”）。
③ 14 世纪初进入英语，照英法语 alouer 的读音写成 allou-，换上英语动词词尾 -en：aloer → allouen。
④ 词尾 -en 掉了，ou 写成 ow：allouen → allow；ou 原来读长音 /uː/，后来英语的长元音整体变了读法（元音大推移），/uː/ 成了 /aʊ/，所以读 /əˈlaʊ/（同 how、now）。""",
['【联想】今天法语还有两个 louer：“出租”（← locare）和“赞扬”（← laudare）——恰好对应 allow 合并的两个来源'], []),

(2053, 'tissue',
"""【字母变化】texere（拉丁语）→ tistre（古法语）→ tissu（古法语）→ tissue（英语）
① 拉丁语 texere：te-xe-re，“编织”；词根 tex- 原样留在 text、texture 里（text 是“织成的文字”）。text 是英语从拉丁语 textus 借的，tissue 是走法语变了样的，两个是一家。
② 到古法语，中间没有重音的 e 被吞掉，x（ks）的 k 也掉了，s 和 r 之间垫进一个 t：texere → tistre“织”（同拉丁 *essere → 古法语 estre，今天法语 être）。
③ 它的“被…了的”形式写成 tissu“织成的”，当名词指织成的丝带、头带、腰带：tistre → tissu（同 venir → venu，这类法语过去分词以 -u 结尾）。
④ 14 世纪末进入英语，先写 tissu、tisseu、tisshewe，后来定成 tissue，词尾加上 e：tissu → tissue；ss 跟着后面的 u 念成 /ʃ/，读 /ˈtɪʃuː/（同 issue）。""",
['【跨组同源】与 text、texture 同出 texere'], []),

(2095, 'doubt',
"""【字母变化】dubitare（拉丁语）→ doter（古法语）→ douten（中古英语）→ doubt（英语）
① 拉丁语 dubitare：du-bi-ta-re，“犹豫、拿不定”，出自 duo“二”：心里有两个主意；词根 dub- 原样留在 dubious 里，du- 就是 duo、dual 的 du-。dual 说的是“二”本身，doubt 是从“二”生出来的词，两个是一家。
② 到古法语，中间没有重音的 bi 被吞掉，b 也跟着没了；u 念成 o，动词词尾 -are 变成 -er：dubitare → doter“怀疑；害怕”。
③ 约 1200 年进入英语，o 照英法语写成 ou（读长音 /uː/），加上英语动词词尾 -en：doter → douten。
④ 14—16 世纪抄写员照拉丁语 dubitare 把 b 加回拼写，词尾 -en 也掉了：douten → doubt；法语 17 世纪又把 b 去掉，英语留到今天，但 b 从来不读（同 debt）。后来英语的长元音整体变了读法（元音大推移），/uː/ 成了 /aʊ/，所以读 /daʊt/。""",
['【同源】德语 Zweifel“怀疑”出自 zwei“二”；古英语也用 tweogan（← tweon“二”）表示怀疑'], []),

(2140, 'able',
"""【字母变化】habilis（拉丁语）→ hable（古法语）→ able（英语）
① 拉丁语 habilis：ha-bi-lis，“容易拿住的、顺手的”，由 habere“拿着”变来；词根 hab- 原样留在 habit、habitat 里。able 和 habit 同出 habere，是一家。
② 到古法语，中间没有重音的 i 被吞掉，词尾 -is 磨成不发音的 e，b、l 挨在一起：habilis → hable“能干的、合适的”（-ilis → -le，同拉丁 nobilis → noble）；词首的 h 在口语里早就不念了，也常写成 able。
③ 14 世纪初进入英语，h 不发音，拼写也去掉了：hable → able；16—17 世纪学者想把 h 恢复也没成功（habiliment、habilitate 这些后来经法语借来的词才带着 h）。后来英语的长元音整体变了读法（元音大推移），a 成了 /eɪ/，所以读 /ˈeɪbl/。""",
['【易混】后缀 -able、-ability 与 able、ability 并不同源，只是常被联想在一起'], []),

(2410, 'mould',
"""【字母变化】modulus（拉丁语）→ modle（古法语）→ molde（中古英语）→ mould（英语）
① 拉丁语 modulus：mo-du-lus，“小尺度、样子”，是 modus“尺度、方式”加上表示“小”的 -ulus；词根 mod- 原样留在 mode、modern 里。model 是同一个 modulus 经意大利语 modello 变来的，mould 是走古法语变来的，两个是一家。
② 到古法语，中间没有重音的 u 被吞掉，词尾 -us 磨成不发音的 e：modulus → modle“样式、模型；方式”。
③ 约 1200 年进入英语，d 和 l 换了位置：modle → molde（两个辅音前后对调叫“换位”，同 bird ← 古英语 brid）。
④ 词尾的 e 不念了；o 在 ld 前面念成复合元音 /əʊ/，英式照这个音写成 ou：molde → mould（美式写 mold，同 gold、cold）。今天法语写 moule，是 l 又念成了 u。""",
['【同形异义】mould 另有“霉菌”“松软的土”两义，来源不同'], []),

(2512, 'fuel',
"""【字母变化】focalia（拉丁语）→ foaille（古法语）→ feuel（中古英语）→ fuel（英语）
① 拉丁语 focalia：fo-ca-li-a，“柴禾”，是 focalis“灶的”的复数当名词用，由 focus“灶、火塘”变来；中世纪拉丁语里是法律用语“砍柴烧火的权利”；词根 foc- 原样留在 focus 里。fuel 和 focus 是一家。
② 到古法语，夹在两个元音中间的 c 越念越轻，最后脱落；li 和后面的元音并成“软 l”，写成 ill：focalia → foaille“烧火的柴”（同 regula → reille，见 rail）。
③ 约 1200 年进入英语，软 l 念成普通的 l，oai 一串元音简化，写成 feuel、feul：foaille → feuel。
④ 后来写成 fuel：feuel → fuel，读 /ˈfjuːəl/。""",
[], []),

(2643, 'issue',
"""【字母变化】exire（拉丁语）→ issir（古法语）→ issue（古法语、英语）
① 拉丁语 exire：ex-i-re，“出去”（ex-“向外”+ ire“走”）；exit 就是 exire 的“他出去了”，transit 里的 -it 也是这个“走”。exit 是英语直接借的拉丁词，issue 走的是法语这条路，两个是一家。
② 到古法语，x（ks）的 k 被吞掉，剩下的 s 双写；开头的 e 念成 i，动词词尾 -ire 变成 -ir：exire → issir（同 exagium → essai，见 essay）。
③ issir 的阴性过去分词“出去了的”当名词用，指“出口、出去”：issir → issue（-ue 是古法语阴性过去分词词尾，同 venir → venue）。约 1300 年原样进入英语。
④ 英语里 ss 后来跟着后面的 u 念成 /ʃ/，所以读 /ˈɪʃuː/（同 tissue）。""",
[], ['【对照】同样由法语阴性过去分词变成名词的，还有本批的 entry（← entree）']),

(2758, 'feast',
"""【字母变化】festa（拉丁语）→ feste（古法语）→ feast（英语）
① 拉丁语 festa：fes-ta，“节日、宴席”，是 festus“节日的、欢乐的”的复数当名词用；词根 fest- 原样留在 festival、festive 里。festival 是英语直接借的拉丁词（加了 -al），feast 是走法语变了样的，两个是一家。
② 到古法语，词尾的 -a 磨成不发音的 e：festa → feste（同拉丁 rosa → 法语 rose）。
③ 约 1200 年进入英语，e 读长音，中古英语用 ea 来写这个长音 e，词尾 e 去掉：feste → feast；后来英语的长元音整体变了读法（元音大推移），所以读 /fiːst/（同 beast ← 古法语 beste）。""",
['【同源】西班牙语 fiesta“节日”同出 *festa'], ['【对照】法语后来把 s 也丢了，写成 fête，帽子 ^ 就是丢掉的 s 留下的记号（fête ↔ feast，同 forêt ↔ forest）']),

(2922, 'scent',
"""【字母变化】sentire（拉丁语）→ sentir（古法语）→ senten（中古英语）→ scent（英语）
① 拉丁语 sentire：sen-ti-re，“感觉、觉察”；词根 sent- / sens- 原样留在 sentiment、sense 里。sense 是 sentire 的“被…了的”形式 sensus 借来的，scent 是 sentire 走法语变来的，两个是一家。
② 到古法语，动词词尾 -ire 磨成 -ir：sentire → sentir“感觉、闻、摸、尝”。
③ 14 世纪末进入英语，是打猎用语“（猎犬）嗅出”，换上英语动词词尾 -en：sentir → senten；名词写 sent“气味”。
④ 词尾 -en 掉了，17 世纪又平白多出一个 c：senten → scent；c 不发音、没有词源依据，可能受 ascent、descent 或 science 影响，读 /sent/。""",
['【易混】cent（分）、sent（send 的过去式）与 scent 同音不同源'], ['【同类】scythe“镰刀”的 c 也是这样后加的；那时 site、situate 还一度写成 scite、scituate']),

(3063, 'chase',
"""【字母变化】captare（拉丁语）→ *captiare（俗拉丁语）→ chacier（古法语）→ chase（英语）
① 拉丁语 captare：cap-ta-re，“不停地去抓”，是 capere“拿、抓”的反复说法；词根 capt- 原样留在 capture、captive 里。catch 是同一个 *captiare 走北部法语变来的（cachier），chase 走的是巴黎一带的法语，两个是兄弟。
② 俗拉丁语里加上 -iare：captare → *captiare“设法抓住、追”（带 * 的是推出来的形式）。
③ 到古法语，pt 的 p 被吞掉，t 和后面的 i 并成 ts，写成 c；开头 ca 的 c 在巴黎一带念成 ch（同拉丁 cattus → 法语 chat、campus → champ）：*captiare → chacier“打猎、追赶”（北部法语还念 k，写 cachier）。
④ 约 1300 年进入英语，先写 chacen，ts 念成 s，词尾去掉：chacier → chase；后来英语的长元音整体变了读法（元音大推移），a 成了 /eɪ/，所以读 /tʃeɪs/。""",
[], []),

(3072, 'cable',
"""【字母变化】capulum（拉丁语）→ cable（北部古法语、英语）
① 中世纪拉丁语 capulum：ca-pu-lum，“套索、拴牲口的缰绳”，由 capere“拿、抓”变来；词根 cap- 原样留在 capture、captive 里。capture 和 cable 同出 capere，是一家。
② 到北部古法语，中间没有重音的 u 被吞掉，p 和 l 挨在一起；p 念轻，变成 b（同拉丁 duplum → 法语 double）；词尾 -um 磨成不发音的 e：capulum → cable（-ulum → -le，同 tabula → table）。
③ 约 1200 年原样进入英语。北部法语开头的 c 一直念 k，没像巴黎法语那样念成 ch（同 catch 和 chase）；a 后来经元音大推移读 /eɪ/，所以读 /ˈkeɪbl/。""",
[], []),

(3112, 'river',
"""【字母变化】riparia（俗拉丁语）→ riviere（古法语）→ river（英语）
① 俗拉丁语 riparia：ri-pa-ri-a，“河岸、海岸，也指河”，是拉丁语 riparius“河岸的”的阴性当名词用，由 ripa“岸”变来；词根 rip- 原样留在 riparian（河岸的）里。arrive 也出自 ripa（“到岸”），river 和 arrive 是一家。
② 到古法语，夹在两个元音中间的 p 念轻，变成 v（同拉丁 sapere → savoir；arrive 的 v 也是这样来的）；-aria 变成 -iere（同 primarius → premier，见 premier）：riparia → riviere“河、河边、河岸”。
③ 13 世纪初进入英语，英法语写 rivere，后来词尾写成 -er：riviere → river（同法语 -re 写成 -er：order、letter），读 /ˈrɪvə/。""",
['【趣】riverbank 字面就是“岸边的岸”'], []),

(3518, 'kitchen',
"""【字母变化】coquina（拉丁语）→ *cocina（俗拉丁语）→ cycene（古英语）→ kitchen（英语）
① 拉丁语 coquina：co-qui-na，“厨房”，由 coquus“厨子”、coquere“煮”变来；词根 coqu-“煮”也留在 concoct、precocious 里。cook 是 coquus 很早借进古英语变来的（coc），kitchen 和 cook 是一家。
② 俗拉丁语里 qu 念成 c（k）：coquina → *cocina（带 * 的是推出来的形式；今天西班牙语 cocina、法语 cuisine 都由它来）。
③ 很早借进日耳曼语（德语 Küche），古英语写作 cycene：第一个 o 受后面 i 的影响念成 y（像德语 ü）；第二个 c 在前元音前软化成 ch 音（同 cheese ← 拉丁 caseus）：*cocina → cycene。
④ 中古英语写 kichene：开头的 c 在 i 前改写成 k，表示还念 k；中间的 ch 音在短元音后写成 tch（同 itch、switch），词尾弱化成 -en：cycene → kitchen，读 /ˈkɪtʃɪn/。""",
[], []),

(3905, 'danger',
"""【字母变化】dominus（拉丁语）→ *dominarium（俗拉丁语）→ dongier（古法语）→ dangier（古法语）→ danger（英语）
① 拉丁语 dominus：do-mi-nus，“主人”（domus“房子”的主人）；词根 domin- 原样留在 dominate、domination 里。dominate 是英语直接借的拉丁词，danger 是走法语变了样的，两个是一家（dungeon 也是）。
② 俗拉丁语里加上 -arium，造出 *dominarium“领主的权力”（带 * 的是推出来的形式）。
③ 到古法语，中间没有重音的 i 被吞掉，m 和 n 挨在一起念成 ng；-arium 变成 -ier（同 primarius → premier）：*dominarium → dongier（同 dominionem → donjon，就是 dungeon）。
④ 人们联想到 damnum“损害”（damage 的来源），把 o 换成 a：dongier → dangier“掌控、能加害别人的权力”。
⑤ 13 世纪中进入英语，英法语写 daunger，词尾 -ier 简化成 -er：dangier → danger；14 世纪晚期起才有“危险”的意思。a 后来读 /eɪ/，g 在 e 前念软，读 /ˈdeɪndʒə/。""",
['【跨组同源】timber（第 2554 组，可能也出自 *dem-）'], []),

(4382, 'pattern',
"""【字母变化】patronus（拉丁语）→ patron（古法语）→ pattern（英语）
① 拉丁语 patronus：pa-tro-nus，“保护人”，由 pater“父亲”变来；词根 patr- 原样留在 patriot、paternal 里。patron 和 pattern 本是同一个词的两种写法，后来才分了工。
② 到古法语，词尾 -us 掉了：patronus → patron，既指“保护人”，也指“样板、供人照着做的原件”（保护人是大家学的榜样）；约 1300 年进入英语。
③ 一般认为，近代英语里词尾没有重音，-ron 念得含糊，r 和后面的元音换了位置，写成 -tern；t 双写，保住前面 a 的短音：patron → pattern（16 世纪起两种写法并存），读 /ˈpætn/。""",
['【跨语同源】与本族词 father 同出 PIE *pəter-（第 2311 组）'], ['【分工】18 世纪以前 patron、pattern 形、义都没分清；后来 patron 管“人”（保护人、主顾），pattern 管“样子”。法语 patron 至今兼有“老板”和“（裁剪用的）纸样”两义']),

(4496, 'fault',
"""【字母变化】*fallita（俗拉丁语）→ falte（古法语）→ faute（古法语）→ fault（英语）
① 俗拉丁语 *fallita：fal-li-ta，“欠缺、跌落”（带 * 的是推出来的形式），由拉丁语 fallere“欺骗、使失望、落空”变来；词根 fall- 原样留在 fallacy 里。false 是 fallere 的“被…了的”形式 falsus 变来的，fault 和 false 是一家。
② 到古法语，中间没有重音的 i 被吞掉，ll 简化成 l，词尾 -a 磨成不发音的 e：*fallita → falte“缺口；失误；欠缺”。
③ l 在辅音前念成 u（同拉丁 salmo → 法语 saumon、alter → autre）：falte → faute（今天法语还写 faute）。
④ 13 世纪末进入英语，先写 faute；16 世纪照拉丁语把 l 补回拼写：faute → fault，这个 l 直到 18 世纪才开始念出来，读 /fɔːlt/（assault、vault 也补回了 l）。""",
[], []),

(4668, 'trouble',
"""【字母变化】turbidus（拉丁语）→ *turbulare（俗拉丁语）→ turbler（古法语）→ trubler（古法语）→ trouble（英语）
① 拉丁语 turbidus：tur-bi-dus，“浑浊的、混乱的”，由 turba“骚乱、人群”变来；词根 turb- 原样留在 disturb、turbulent 里。disturb 是英语直接借的拉丁词，trouble 是走法语变了样的，两个是一家。
② 俗拉丁语里造出动词 *turbulare“搅浑、扰乱”（带 * 的是推出来的形式；晚期拉丁语也有 turbidare）。
③ 到古法语，中间没有重音的 u 被吞掉，b 和 l 挨在一起，动词词尾 -are 变成 -er：*turbulare → turbler“搅扰；把水搅浑”。
④ u 和 r 换了位置（换位），tur- 成了 tru-：turbler → trubler（同 bird ← 古英语 brid、third ← thridda）。
⑤ 约 1200 年进入英语，u 照法语习惯写成 ou，动词词尾不要了，留下不发音的 e：trubler → trouble；ou 在这里读短音 /ʌ/（同 double、couple），读 /ˈtrʌbl/。""",
['【同源】disturb（本组）、turbulent（湍急的、动荡的）、turbine（涡轮）都出自拉丁 turba', '【有争议】storm（第 464 组）：Pokorny 把 turba 也归入 *(s)twer-“旋转”，etymonline 引 De Vaan 说 turba 来源不明'], []),

(4784, 'host',
"""【字母变化】hospitem（拉丁语）→ hoste（古法语）→ host（英语）
① 拉丁语 hospitem：hos-pi-tem，是 hospes“客人；主人”的变格形式；词根 hospit- 原样留在 hospital、hospitality 里。hospital 是 hospes 的形容词 hospitalis 借来的，host 是走法语变了样的，两个是一家。
② 到古法语，中间没有重音的 i 被吞掉，p 夹在 s、t 中间也掉了，词尾 -em 磨成不发音的 e：hospitem → hoste（也写 oste；今天法语 hôte，^ 是脱落的 s 留下的记号）。
③ 13 世纪末进入英语，词尾 e 去掉：hoste → host；o 在 st 前读长音（同 most、post），读 /həʊst/。""",
['【同形异义】host 另有“一大群”（a host of problems 一大堆问题，← 拉丁 hostis“敌人”→ 中世纪拉丁“敌军”）和“（弥撒）圣饼”（← 拉丁 hostia“祭品”）两个词，来源不同'], []),

(4788, 'hostel',
"""【字母变化】hospitale（拉丁语）→ hostel（古法语、英语）
① 中世纪拉丁语 hospitale：hos-pi-ta-le，“客栈；大宅子”，是 hospitalis“待客的”的中性当名词用，由 hospes“客人”变来；词根 hospit- 原样留在 hospital、hospitality 里。hospital 是同一个词照拉丁语借的，hostel 是走法语变了样的，两个是一家。
② 到古法语，中间没有重音的 pi 被吞掉，-ale 变成 -el：hospitale → hostel“住所；客栈”（同 hospitem → hoste，见 host）。
③ 13 世纪初原样进入英语，读 /ˈhɒstl/；16 世纪以后不用了，1808 年司各特（Walter Scott）又把它和 hostelry 用了起来。""",
[], ['【对照】法语后来又丢了 s 成 hôtel，英语再借一次，就有了 hotel']),

(4964, 'medley',
"""【字母变化】*misculare（俗拉丁语）→ mesler（古法语）→ medler（北部古法语）→ medlee（古法语）→ medley（英语）
① 俗拉丁语 *misculare：mis-cu-la-re，“掺和、混合”（带 * 的是推出来的形式），由拉丁语 miscere“混合”变来；词根 misc- 原样留在 miscellaneous 里。mix 是从 miscere 的“被…了的”形式 mixtus 倒推出来的，medley 和 mix 是一家。
② 到古法语，中间的 cu 被吞掉，sc 里的 c 也掉了，i 念成 e，动词词尾变成 -er：*misculare → mesler“混合、掺和”。
③ 北部古法语里 s 在 l 前面念成 d：mesler → medler（英语 meddle“干涉”就是它）。
④ 加上“被…了的”阴性词尾 -ee，当名词用，指“混在一起的东西；混战”：medler → medlee（-r 去掉，同 entree）。
⑤ 约 1300 年进入英语，词尾 -ee 写成 -ey：medlee → medley，读 /ˈmedli/。""",
['【联想】melee（混战）、meddle（干涉）都出自 mesler'], ['【对照】今法语 mêler 里 ê 上的“帽子”就是脱落的 s']),

(5331, 'campaign',
"""【字母变化】campania（拉丁语）→ campagna（意大利语）→ campagne（法语）→ campaign（英语）
① 晚期拉丁语 campania：cam-pa-ni-a，“平原、平坦的乡野”，由 campus“田野”变来；词根 camp- 原样留在 camp、campus 里。camp 也出自 campus，campaign 和 camp 是一家。
② 到意大利语，ni 和后面的元音并成“软 n”（舌面贴着上腭念的 n），写成 gn：campania → campagna（同拉丁 Hispania → 西班牙语 España 的 ñ）。
③ 法语借过去，词尾的 -a 磨成不发音的 e：campagna → campagne“乡野、旷野”。
④ 1640 年代进入英语，是军事用语“野战、一季的战事”（军队冬天住营房，夏天才到“旷野”去打仗）；英语照 -ain 的写法把 -agne 写成 -aign：campagne → campaign，g 不发音，读 /kæmˈpeɪn/（同 reign 的 g）。""",
['【同源】champagne（香槟）与 campaign 是一对“双胞胎”：都来自 campania“平原”，香槟酒因产自法国 Champagne 平原地区而得名'], []),

(5428, 'etiquette',
"""【字母变化】*stikkan（法兰克语）→ estiquer（古法语）→ estiquette（古法语）→ etiquette（法语、英语）
① 法兰克语 *stikkan：“刺进去、钉住、贴上”（带 * 的是推出来的形式），和英语 stick 是同一个日耳曼词根。ticket 和 etiquette 都由古法语 estiquette 而来：ticket 截掉了开头，etiquette 留着，两个原是同一个词。
② 进了法语，法国人不习惯词首直接念 st，前面垫了个 e；kk 写成 qu，换上法语动词词尾 -er：*stikkan → estiquer“钉上、贴上”（词首加 e 同 species → espice，见 spice）。
③ 加上表示“小”的词尾 -ette，指“贴上去的小纸条、告示”：estiquer → estiquette（14 世纪末）。
④ s 在 t 前不念了，后来也不写（今天法语写 étiquette，é 标着丢掉的 s），意思变成“宫廷里规定的礼节”（也许出自写着礼仪规矩的小卡片）：estiquette → etiquette；1750 年英语原样借来，读 /ˈetɪket/。""",
['【同源】ticket / etiquette / stick 都出自 *steig-“刺、贴”'], []),

(5663, 'counsel',
"""【字母变化】consilium（拉丁语）→ conseil（古法语）→ counseil（英法语）→ counsel（英语）
① 拉丁语 consilium：con-si-li-um，“计划、意见；商议”。它和 consult 的关系有两说：韦氏说出自 consulere“商议”（consult 的来源），etymonline 说是 com“一起”+ calare“召集”；按前一说，counsel 和 consult 是一家。
② 到古法语，-lium 里的 li 和后面的元音并成“软 l”，前面的 i 跟着念成 ei，写成 -eil；词尾 -um 掉了：consilium → conseil（今天法语还写 conseil）。
③ 英法语（英国诺曼人说的法语）里，o 在 n 前写成 ou（读长音 /uː/）：conseil → counseil（同 count、mountain 的 ou）。
④ 约 1200 年进入英语，词尾没有重音，-eil 弱化成 -el：counseil → counsel；后来英语的长元音整体变了读法（元音大推移），/uː/ 成了 /aʊ/，所以读 /ˈkaʊnsl/。""",
['【易混】council ← 拉丁 concilium“集会”（com + calare“召集”）'], []),

(5774, 'ray',
"""【字母变化】radius（拉丁语）→ rai（古法语）→ ray（英语）
① 拉丁语 radius：ra-di-us，“棍、杆；车轮的辐条；一束光”；词根 radi- 原样留在 radiate、radio 里。radius 是 16 世纪 90 年代英语原样借的拉丁原词，ray 是走法语变了样的，两个是同一个词。
② 到古法语，夹在两个元音中间的 d 越念越轻、脱落（同拉丁 videre → 古法语 veoir，今天法语 voir），a 和 i 并成 ai，词尾 -us 掉了：radius → rai“（太阳的）光线；辐条”。
③ 14 世纪初进入英语，词尾的 i 照英语习惯写成 y（同 essay、day）：rai → ray；ai 后来读 /eɪ/，所以读 /reɪ/。""",
['【同形异义】ray 另指“鳐鱼”（拉丁 raia）；rayon 人造丝（1924）来自法语 rayon“光线”，因为它闪亮'], []),

(5785, 'solder',
"""【字母变化】solidare（拉丁语）→ solder（古法语）→ souder（古法语）→ solder（英语）
① 拉丁语 solidare：so-li-da-re，“使变实、使牢固”，由 solidus“实心的”变来；词根 solid- 原样留在 solid、solidarity 里。solid 是英语直接借的拉丁词，solder 是走法语变了样的，两个是一家。
② 到古法语，中间没有重音的 i 被吞掉，l、d 挨在一起，动词词尾 -are 变成 -er：solidare → solder“使牢固、接合、焊上”。
③ l 在辅音前按规律念成 u（同拉丁 pulverem → 法语 poudre、calidus → chaud）：solder → souder；14 世纪初英语借来的就是这个没有 l 的样子：souder、soudur“焊料”。
④ 15 世纪初英语照拉丁语把 l 写了回去（soldier 也是这样），1724 年起定成今天的写法：souder → solder。英式读 /ˈsəʊldə/，美式常读 /ˈsɑːdɚ/，l 不发音。""",
[], []),

(5923, 'rhyme',
"""【字母变化】rhythmos（希腊语）→ rithmus（拉丁语）→ rime（古法语）→ ryme（中古英语）→ rhyme（英语）
① 希腊语 rhythmos：rhyth-mos，“有规律的流动、节奏”，和 rhein“流”同根；rhythm 是它照希腊拼法借来的，rhyme 一般认为也出自它，两个是一家。
② 罗马人借来写成 rithmus（也写 rhythmus）：口语写法里 rh、y 写成 r、i，-os 换成拉丁语的 -us：rhythmos → rithmus；中世纪拉丁语用它指押韵的诗。
③ 到古法语，th、m 一串辅音简化，th 的音脱落，词尾 -us 磨成不发音的 e：rithmus → rime“诗句”。
④ 约 1200 年进入英语，写成 ryme、rime（先指“格律、节奏”，后来指押韵）：rime → ryme。
⑤ 16、17 世纪为了看起来像希腊词，又添上 h、照 rhythm 写成 rhyme（中间还写过 rhime），读音没变：ryme → rhyme；旧拼法 rime 至今偶见。后来英语的长元音整体变了读法（元音大推移），/iː/ 成了 /aɪ/，所以读 /raɪm/。""",
[], []),

(6104, 'league',
"""【字母变化】ligare（拉丁语）→ legare（意大利语）→ liga（意大利语）→ ligue（法语）→ league（英语）
① 拉丁语 ligare：li-ga-re，“捆、绑”；词根 lig- 原样留在 ligament、obligation 里。ally 也出自 ligare（经古法语 alier），league 和 ally 是一家。
② 到意大利语，没有重音的 i 念成 e：ligare → legare“捆、绑”。
③ 去掉动词词尾，当名词“结在一起的、同盟”，写成 lega，也写 liga：legare → liga。
④ 15 世纪法语借过去，词尾 -a 磨成不发音的 e；g 后面加 u，让 g 在 e 前保持硬音 /g/：liga → ligue“同盟”。
⑤ 15 世纪中进入英语，先写 ligg；i 读长音，后来照英语习惯用 ea 写这个长音（同 feast）：ligue → league，读 /liːɡ/。""",
['【同形异义】league 另有“里格”（约 3 英里的旧长度单位，来自晚期拉丁 leuga，罗马作家说源自高卢语），与“联盟”无关：《海底两万里》英文名 Twenty Thousand Leagues Under the Sea 用的就是这个义'], []),

(6134, 'lantern',
"""【字母变化】lampter（希腊语）→ lanterna（拉丁语）→ lanterne（古法语）→ lantern（英语）
① 希腊语 lampter：lamp-ter，“火把、烽火”，由 lampein“发光”变来；词根 lamp- 原样留在 lamp 里。lamp 也出自 lampein，lantern 和 lamp 是一家。
② 罗马人借过去，p 被吞掉，m 在 t 前变成同部位的 n（同 com- 在 t 前写作 con-，如 contain）；词尾又照拉丁语 lucerna“灯”改成 -erna：lampter → lanterna“灯笼、灯、火把”。
③ 到古法语，词尾的 -a 磨成不发音的 e：lanterna → lanterne。
④ 13 世纪中进入英语，词尾 e 去掉：lanterne → lantern，读 /ˈlæntən/；16—19 世纪还写过 lanthorn，是因为灯罩常用磨薄的牛角（horn）做。""",
['【跨组同源】lamp、streetlamp 见第 990 组', "【合成】jack-o'-lantern 万圣节南瓜灯"], []),

(6348, 'pillar',
"""【字母变化】pila（拉丁语）→ pilare（中世纪拉丁语）→ piler（古法语）→ pillar（英语）
① 拉丁语 pila：pi-la，“柱子、石墩”（来源不明）；词根 pil- 原样留在 pile“桩、柱”里。pile 是 pila 直接变来的，pillar 是加了词尾以后变来的，两个是一家。
② 中世纪拉丁语加上 -are：pila → pilare“柱子”。
③ 到古法语，-are 变成 -er：pilare → piler（今天法语 pilier）。
④ 约 1200 年进入英语，先写 piler；后来 l 双写，保住前面 i 的短音，-er 改写成 -ar：piler → pillar，读 /ˈpɪlə/。""",
[], []),

(6490, 'eager',
"""【字母变化】acer（拉丁语）→ *acrus（俗拉丁语）→ aigre（古法语）→ egre（中古英语）→ eager（英语）
① 拉丁语 acer：a-cer，“尖的、锐利的；热切的”（印欧词根 *ak-“尖、刺”）；词根 ac- 原样留在 acid、acute 里。acid 是英语直接借的拉丁词（acidus“酸的”），eager 是走法语变了样的，两个是一家。
② 俗拉丁语里换上常见的形容词词尾 -us：acer → *acrus（带 * 的是推出来的形式；意大利语 agro、西班牙语 agrio 都由它来）。
③ 到古法语，夹在元音和 r 中间的 c 念轻，变成 g，a 跟着念成 ai，词尾 -us 磨成不发音的 e：*acrus → aigre“酸的；尖刻的；急切的”（同拉丁 macrum → 法语 maigre“瘦”）。
④ 13 世纪末进入英语，ai 写成 e：aigre → egre。
⑤ e 读长音，后来用 ea 来写；法语式的 -gre 改写成 -ger：egre → eager（同 tigre → tiger、ordre → order），读 /ˈiːɡə/。""",
['【联想】vinegar（醋）= 法语 vin“酒”+ aigre“酸”：后半截正是 eager 的前身——“变酸的酒”', '【同源】*ak- 一族还有 acute、acme、acupuncture、edge、oxygen'], []),

(7052, 'sleigh',
"""【字母变化】slede（荷兰语）→ slee（荷兰语）→ sleigh（英语）
① 荷兰语 slede：sle-de，“雪橇”（今天荷兰语还这样写），和 slide“滑”同根；英语的 sled 也出自中古荷兰语 sledde，sleigh 和 sled 是兄弟。
② 荷兰语口语里，夹在两个元音中间的 d 脱落，剩下的长元音写成 ee：slede → slee。
③ 1703 年起见于美国、加拿大英语（荷兰移民带来的），英语照 weigh、neigh 的写法写成 -eigh，gh 不发音：slee → sleigh，读 /sleɪ/。""",
[], []),

(7912, 'Mandarin',
"""【字母变化】mantrin（梵语）→ mantri（马来语）→ mandarim（葡萄牙语）→ Mandarin（英语）
① 梵语 mantrin-：man-trin，“出主意的人、谋臣”，由 mantra“商议、主意”变来（印欧词根 *men-“想”，同 mind、mental）；英语 mantra 就是这个词，Mandarin 和 mantra 是一家。
② 到印地语、马来语里说 mantri“大臣”，词尾的 n 掉了：mantrin → mantri。
③ 16 世纪葡萄牙人在东方借过去：t 浊化成 d，中间多出一个 a，词尾又多了鼻音 -m（OED 说来由不明）；拼法还受葡萄牙语 mandar“命令”影响：mantri → mandarim。
④ 1580 年代进入英语，词尾的 m 写成 n（荷兰语写 mandorijn）：mandarim → Mandarin；先指“中国的官员”，约 1600 年起指官员说的话，就是“官话、普通话”。""",
['【易混】看着像 mandar“命令”（同 command、mandate），其实出自梵语 mantra“主意”：本义是“出主意的人”，不是“发号施令的人”'], []),

(8054, 'grill',
"""【字母变化】craticula（拉丁语）→ graille（古法语）→ gril（法语）→ grill（英语）
① 拉丁语 craticula：cra-ti-cu-la，“小烤架”，是 cratis“编条、格架”加上表示“小”的 -cula；词根 crat- 原样留在 crate 里。crate 也出自 cratis，grill 和 crate 是一家。
② 到古法语，开头的 c 浊化成 g；夹在元音中间的 t 脱落，-icula 里的 cl 并成“软 l”，写成 ill：craticula → graille“格栅、栏杆”（同拉丁 auricula → 法语 oreille“耳朵”）。
③ 后来写成 greil、gril，词尾的软 l 念成普通的 l：graille → gril（今天法语 gril“烤架”，另有 grille“格栅”）。
④ 1680 年代进入英语，l 双写（同 still、will）：gril → grill，读 /ɡrɪl/。""",
['【跨组同源】hurdle（第 2358 组，原指“编条围栏”）是日耳曼语里的同源词，同出 PIE *kert-“编、绕”（crate、grill 条对此只说“也许”）'], []),

(8319, 'kitten',
"""【字母变化】cattus（拉丁语）→ caton（北部古法语）→ kitoun（中古英语）→ kitten（英语）
① 晚期拉丁语 cattus：cat-tus，“猫”；cat 是同一个 cattus 很早借进古英语变来的（catt），kitten 和 cat 是一家。
② 到法语，加上表示“小”的词尾 -on：cattus → caton“小猫”；北部和诺曼法语开头还念 k，中部法语念成 ch，写 chaton（今天法语 chat、chaton）。
③ 14 世纪末进入英语，写成 kitoun（很可能来自英法语的一种说法）：a 念成了 i，c 在 i 前写成 k，表示还念 k（同 kitchen）；on 照英法语写成 oun：caton → kitoun。
④ 词尾没有重音，-oun 弱化成 -en；t 双写，保住前面 i 的短音：kitoun → kitten，读 /ˈkɪtn/。""",
['【同源】cat / kitten / 法语 chat 同出晚期拉丁 cattus'], []),

(8437, 'frantic',
"""【字母变化】phreneticus（拉丁语）→ frenetike（古法语）→ frentik（中古英语）→ frantik（中古英语）→ frantic（英语）
① 拉丁语 phreneticus：phre-ne-ti-cus，“精神错乱的”，来自希腊语 phrenitikos，由 phrenitis“脑炎、精神错乱”（phrēn“心智”+ -itis“炎症”）变来；词根 phren- 留在 frenzy、frenetic 里。frenzy 是同一个希腊词的名词经法语变来的，frantic 和 frenzy 是一家。
② 到古法语，ph 写成 f，c 写成 k，词尾 -us 磨成不发音的 e：phreneticus → frenetike“发疯的”。
③ 14 世纪进入英语，先写 frenetik；重音在第一音节，中间没有重音的 e 被吞掉：frenetike → frentik（韦氏据 frentik、frantike 这些变体推断）。
④ e 又变成 a：frentik → frantik，这一步词典都说原因不明（frenzy 在方言里也说 franzy）。
⑤ 词尾的 k 改写成 c（同 music、logic 的 -ic）：frantik → frantic，读 /ˈfræntɪk/。""",
['【同源】frenetic、phrenetic（恢复了希腊拼法 ph-，与 frantic 是“双生词”）、frenzy'], []),

(8563, 'chime',
"""【字母变化】cymbalum（拉丁语）→ chimbe（古法语）→ chymbe（中古英语）→ chime（英语）
① 拉丁语 cymbalum：cym-ba-lum，“钹”，来自希腊语 kymbalon，由 kymbē“碗”变来（两片钹像两只浅浅的铜碗）。cymbal 是英语照拉丁语写的同一个词，chime 是走法语变了样的，两个本是一个词。
② 到古法语，开头的 c 写成 ch，y 写成 i；后半截 -alum 被截掉，只剩不发音的 e：cymbalum → chimbe（etymonline 说先在古法语里截短）。
③ 约 1300 年进入英语，写成 chymbe；中古英语有 chymbe belle 的说法，词尾像是被当成 bell“钟”拆了出去，chime 就单独用来说钟（dictionary.com 称“错误分析”）：chimbe → chymbe。
④ mb 里的 b 后来不念、也不写了，y 写成 i：chymbe → chime；后来英语的长元音整体变了读法（元音大推移），/iː/ 成了 /aɪ/，所以读 /tʃaɪm/。""",
['【联想】bell 见第 994 组'], []),

(6600, 'menu',
"""【字母变化】minutus（拉丁语）→ menu（法语、英语）
① 拉丁语 minutus：mi-nu-tus，“被弄小了的、小的”，是 minuere“使变小”的“被…了的”形式；词根 minu- 原样留在 minute、diminish 里。minute 是同一个拉丁词照书面拼法进英语的，menu 是走法语变了样的，两个是一家。
② 到法语，没有重音的 i 念成 e，夹在元音中间的 t 脱落，词尾 -us 也掉了：minutus → menu“小的、细的”（中间的 t 脱落，同拉丁 vita → 法语 vie）。
③ 1837 年英语原样借来，指“菜单”（法语 menu de repas“一餐里上的菜的细单”，把吃的一样样细细列出）；读 /ˈmenjuː/。""",
[], ['【同类】minuet（小步舞曲）← 法语 menuet“小巧的”← menu']),
]

# 没写链的 70 个 ≈ 词（字母变化同源词轮逐个看过，zimu_check.py --todo 不再列出）
SKIP = {
 '本族词': 'match weigh wagon wet booth there though twist deed yard chill drown glow bench weave month streak shallow dig dyke tusk wasp yarn blast wail reef widow pitch',
 '来源不确定': 'storey guess dune rubble carol hockey buoy glitch haunt prune pant cabbage pilot core label lush turtle lava mushroom puck fee guarantee ribbon tier',
 '变化很小': 'physique costume critique ration graffiti false salsa pouch climax Hindu rink carpet filter salute gas lime border supper',
}

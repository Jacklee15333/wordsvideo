"""合成规律、写法的目录（2026-11 合成规律轮）。表里组合列的“　合成规律：”“　写法：”两种行都从这里取规律那句话。
每条：id、类（合成规律 / 写法）、规律（一句话，视频照念，所以不写“…”和箭头）、为什么、例子（总表里的词）。
维护技能 scripts/hecheng_check.py 和视频技能 wordfilm.js 都按“规律那句话”认是哪一条，改措辞要三处一起改。"""

RULES = [
    # ---------------------------------------------------------------- 合成规律：两个词谁在前、谁在后，合起来是什么意思
    ('H01', '合成规律', '最后一个词是主体，前面的词说明它',
     '英语合成词和汉语一样，说明的词在前，被说明的词在后：classroom 是一种 room（上课的房间），toolbox 是一种 box（装工具的箱子）。'
     '所以读合成词要从后往前读：先看最后一个词是什么，再看前面的词给它加了什么——什么样的、干什么用的、在哪儿的、谁的。'
     '前后一换，主体就换了，意思也跟着变：boathouse 是放船的屋子，houseboat 是能住人的船。',
     'classroom 教室；toolbox 工具箱；bookshelf 书架'),
    ('H02', '合成规律', '动词带着宾语合成一个词，宾语挪到前面，动词放在最后当主体',
     '英语句子里是“动词 + 宾语”：cut paper（剪纸）、wash dishes（洗碗）、make shoes（做鞋）。合成一个词时要守住“最后一个词是主体”：'
     '要说的是“剪”这件事、“洗”的机器、“做”的人，所以动词带上 -ing（这件事）、-er（做这件事的人或东西）放在最后，宾语挪到前面去说明它：'
     'paper-cutting、dishwasher、shoemaker。汉语“剪纸、洗碗机”是动词在前，英语正好倒过来。'
     '要是写成 cutting-paper，主体就成了 paper，变成“剪着用的纸”（同 notepaper 写便条用的纸）；分开写的 cutting paper 只是普通的动词短语“剪纸（这个动作）”。',
     'paper-cutting 剪纸；dishwasher 洗碗机；shoemaker 鞋匠；energy-saving 节能的'),
    ('H03', '合成规律', '动词带着用什么、在哪儿合成一个词，这个名词挪到前面，介词省掉，动词放在最后',
     'fight with swords（用剑打）→ sword-fighting；dive in the sky（在天上“潜水”）→ skydiving；write by hand（用手写）→ handwriting。'
     '和宾语一样，名词挪到动词前面，with、in、by 这些介词省掉，最后带 -ing、-er 的动词是主体。',
     'sword-fighting 剑术；skydiving 跳伞；handwriting 手写；typewriter 打字机'),
    ('H04', '合成规律', '名词和过去分词合成形容词，名词挪到前面，介词省掉，过去分词放在最后',
     '英语说“用手做的”是 made by hand，“被雪盖住的”是 covered with snow，过去分词在前、名词在后。'
     '合成一个形容词时还是“最后一个词是主体”：过去分词放最后，名词挪到前面说“被谁、用什么、在哪儿”，by、with、in 这些介词省掉：'
     'handmade、snow-covered、moonlit。',
     'handmade 手工做的；snow-covered 被雪覆盖的；moonlit 月光照着的'),
    ('H05', '合成规律', '动词带着副词合成形容词，副词挪到前面，动词放在最后',
     '英语说“工作努力”是 work hard，“卖得最好”是 sell best，“知道得清楚”是 known well，副词都在动词后面。'
     '合成一个形容词时，动词放最后当主体（用 -ing 是主动、正在，用过去分词是被动、已经），副词挪到前面：hard-working、best-selling、well-known。',
     'hard-working 努力工作的；best-selling 最畅销的；well-known 出名的'),
    ('H06', '合成规律', '名词和形容词合成形容词，名词挪到前面，介词省掉，形容词放在最后',
     '英语说“像雪一样白”是 white as snow，“对用户友好”是 friendly to users，“不含糖”是 free of sugar，“全世界有名”是 famous in the world，形容词在前、名词在后。'
     '合成一个形容词时形容词放最后当主体，名词挪到前面说“像什么、对什么、在哪方面、没有什么”，as、to、of、in 这些小词省掉：'
     'snow-white、user-friendly、sugar-free、world-famous。',
     'user-friendly 好用的；sugar-free 无糖的；waterproof 防水的；world-famous 世界闻名的'),
    ('H07', '合成规律', '一个短语整个当一个词用，多放在名词前当形容词，短语里的词先后不变',
     '英语可以把一个短语原封不动地搬到名词前面当形容词：a job for part of the time → a part-time job；a call over a long distance → a long-distance call；'
     'a map that is up to date → an up-to-date map。短语里的词先后不变，用连字符连起来，告诉读者这几个词是一个整体。',
     'part-time 兼职的；long-distance 长途的；up-to-date 最新的；face-to-face 面对面的'),
    ('H08', '合成规律', '动词短语整个变成名词或形容词，先后不变，动词在前、小词在后',
     'make up、take off、check out 这类“动词 + 小词”的短语很常用，英语干脆把整个短语拿来当名词、形容词：make-up 化妆品、takeoff 起飞、checkout 结账台。'
     '先后不变，只是连写或加连字符；读的时候重音挪到前面：动词 take ˈoff，名词 ˈtakeoff。',
     'make-up 化妆品；takeoff 起飞；checkout 结账；grown-up 成年人'),
    ('H09', '合成规律', '小词放在动词前面合成一个词，像前缀一样',
     '这是另一种造法：把 in、out、up、down 这些小词放到动词前面，像前缀一样：come in（进来）→ income 收入；come out（出来）→ outcome 结果；'
     'break out（爆发）→ outbreak；put out → output。这类词都连写。两种顺序都有的，意思不一样：set up（建立）→ setup 设置、安排；up + set → upset 打翻、心烦。',
     'income 收入；outcome 结果；outbreak 爆发；download 下载'),
    ('H10', '合成规律', '介词和后面的词连成一个词，先后不变',
     '常说的介词短语说多了，就连成了一个词，先后不变：up the stairs（在楼上）→ upstairs；on line（在线路上）→ online；'
     'in stead（在…的位置上）→ instead；in deed（在行动上）→ indeed。',
     'upstairs 在楼上；online 在线的；instead 代替；indeed 确实'),
    ('H11', '合成规律', '动词在前、宾语在后，像一句命令，整个词说的是做这件事的人、东西或这件事',
     '这类词像一句命令：scare crow!（吓走乌鸦！）→ scarecrow 稻草人；break fast（打破禁食）→ breakfast 早餐；cease fire!（停火！）→ ceasefire 停火。'
     '它们的主体不在词里，说的是词外面那个做这件事的人、东西或这件事。英语这样造的词不多，有的是照法语的造法来的'
     '（pastime 照法语 passe-temps“打发时间”）——法语、意大利语、汉语造词都爱把动词放在前面（汉语“磕头”借进英语成了 kowtow）。',
     'scarecrow 稻草人；breakfast 早餐；pastime 消遣；ceasefire 停火'),
    ('H12', '合成规律', '名词带上 -ed 和前面的形容词连起来，说的是长着、有着这样东西的',
     'kind-hearted = kind（善良的）+ heart（心）+ -ed（有…的）=“长着一颗善良的心的”；long-tailed 长尾巴的、curly-haired 卷头发的。'
     '单独的 hearted、tailed 一般不用，要连着前面的词才成一个意思，所以中间加连字符。前面也可以是数词、名词：three-legged 三条腿的、heart-shaped 心形的。',
     'kind-hearted 好心的；three-legged 三条腿的；heart-shaped 心形的'),
    ('H13', '合成规律', '数词和名词连起来放在名词前当形容词，名词用单数',
     'a ten-dollar bill（十美元的钞票）、a two-hour delay（两小时的延误）、an eight-year-old boy（八岁的男孩）：数词和名词连成一个形容词，中间加连字符，'
     '名词用单数，不说 a ten-dollars bill。不放在名词前时照常用复数：The boy is eight years old. 这是考试常考的地方。',
     'ten-dollar 十美元的；two-hour 两小时的；eight-year-old 八岁的'),
    ('H14', '合成规律', '两个词平起平坐，没有主次，说的是这个和那个，或者既是这个又是那个',
     'teacher-director 既是老师又是导演；black-and-white 又黑又白；urban-rural 城市和乡村之间的。'
     '英语的方位词也是并列的：northeast 东北、southwest 西南——英语南北在前、东西在后，汉语正好相反。',
     'black-and-white 黑白的；northeast 东北；urban-rural 城乡的'),
    ('H15', '合成规律', '两个意思差不多的词叠在一起，说得更清楚',
     'pathway = path（小路）+ way（路）；until = un（到）+ till（到）；courtyard = court（院子）+ yard（院子）。'
     '还有一种是前一个词本来就是这样东西，后来大家不太认得了，再加一个类名说明它是哪一类：reindeer 的 rein 在古北欧语里本来就是“驯鹿”，再加上 deer“鹿”；'
     'chestnut 的 chest 本来就是“栗子”，再加上 nut“坚果”。',
     'pathway 小路；until 直到；reindeer 驯鹿'),
    ('H16', '合成规律', '合成词说的不是最后那个词，而是有这个特点的人或东西',
     'humpback = hump（隆起）+ back（背）：本来是“驼着的背”，拿来叫背驼的人，又叫背上鼓起一块的座头鲸；high-five = high（高处的）+ five（五指，一只手）：'
     '举到高处的手 → 击掌。这种词的主体不在词里，说的是“有这个特点的”人、动物、东西或动作，要靠联想去懂。',
     'humpback 座头鲸；high-five 击掌；high-rise 高楼'),
    ('H17', '合成规律', '名词或形容词放在动词前面合成动词，前面的词说用什么、怎样做',
     'hand-wash（用手洗）、deep-fry（在深油里炸）、double-check（查两遍）。英语这样造的动词不多，不少是先有 -er、-ing 结尾的名词，'
     '再去掉 -er、-ing 倒推出来的：troubleshoot 很可能来自 troubleshooter（排除故障的人），kidnap 也许来自更早的 kidnapper（拐子）。',
     'double-check 复查；deep-fry 油炸；troubleshoot 排除故障'),
    ('H18', '合成规律', '主语和动词合成名词，说的是这件事，先后和句子一样',
     'the sun rises（太阳升起）→ sunrise 日出；the earth quakes（大地颤动）→ earthquake 地震；the heart beats（心跳）→ heartbeat。'
     '后一个词是动词当名词用，前一个词就是做这个动作的东西，先后和句子里一样，不用倒过来。',
     'sunrise 日出；earthquake 地震；heartbeat 心跳；waterfall 瀑布'),
    ('H19', '合成规律', '两位数十位在前、个位在后，和汉语的顺序一样',
     'forty-five = forty（四十）+ five（五）；ninety-nine。21 到 99 之间十位、个位都有的数，中间加连字符；'
     '13 到 19 是古英语就连在一起的老词，不加连字符：fourteen = four + teen（= ten 十）“四加十”。',
     'forty-five 四十五；ninety-nine 九十九'),
    ('H20', '合成规律', '分数分子在前、分母在后，和汉语先说分母正好相反',
     'one-third = one（一个）+ third（三分之一）=“一个三分之一”，汉语说“三分之一”，先说分母。英语分子用基数词，分母用序数词；'
     '分子大于一时分母加 s：two-thirds 三分之二。',
     'one-third 三分之一；one-fifth 五分之一'),
    ('H21', '合成规律', '十三到十九的数，个位在前、十在后，古英语就连成了一个词',
     'fourteen = four（四）+ teen（= ten 十）“四加十”；seventeen = seven + teen。这些数古英语里就连成一个词（fēowertīene），不加连字符；'
     '二十以上反过来是十位在前：twenty-four。',
     'fourteen 十四；seventeen 十七'),
    ('H22', '合成规律', 'some、any、every、no 和后面的小词合成一个词，后一个是主体，前一个说哪一个、多少',
     'something = some（某个）+ thing（东西）“某样东西”；anyone =“随便哪一个人”；everywhere =“每一个地方”；nobody =“没有一个人”。'
     '后一个词是主体（东西、人、地方、时候），前一个说“哪一个、多少”。',
     'anything 任何东西；everyone 每个人；nowhere 无处'),
    ('H23', '合成规律', '疑问词带上 ever，说的是不管什么、不管哪里',
     'whatever = what（什么）+ ever（不论）“不管什么”；whenever 不管什么时候；wherever 不管在哪里；however 不管怎样。'
     'ever 在这里加强语气，意思是“不论、随便”。',
     'whatever 无论什么；whenever 无论何时；however 无论怎样'),
    ('H24', '合成规律', '代词带上 self，说的是某人自己，复数改成 selves',
     'itself = it + self“它自己”；ourselves = our + selves。单数用 self，复数把 f 变成 v 再加 -es：selves（同 leaf → leaves、wolf → wolves）。',
     'itself 它自己；ourselves 我们自己；themselves 他们自己'),
    ('H25', '合成规律', '两个小词合成一个新的小词，意思由两个小词合起来',
     'without = with（对着）+ out（外面）；within；upon = up + on；onto = on（在上面）+ to（到）“到…上面”；throughout = through（穿过）+ out（到底）。'
     '这类词很常用，早就连写成一个词。',
     'without 没有；within 在里面；onto 到…上；throughout 遍及'),
    ('H26', '合成规律', '很老的合成词，用了上千年，读音、拼写磨损了，已经看不出是两个词',
     'window = wind（风）+ eye（眼睛，古北欧语 auga）“风眼”：屋顶上通风透光的洞；woman = wif（女人）+ man（人）；husband = house（房子）+ 户主。'
     '越常用的词磨损得越厉害：字母掉了、元音变了，后人就当成一个词来记。拆开来看，常常能看出古人的生活。',
     'window 窗户；woman 女人；husband 丈夫'),
    ('H27', '合成规律', '在别的语言里就合成好了，整个借进英语，词的先后照那种语言',
     'republic 来自拉丁语 res publica =“事 + 公共的”：拉丁语、法语、意大利语常把形容词放在名词后面，所以“公共的事”说成“事 + 公共的”'
     '（同 vinegar：法语 vin aigre“酒 + 酸的”）；kowtow 来自汉语“磕头”，动词在前；tsunami 来自日语“津波”（港口 + 浪），和英语一样主体在后。',
     'republic 共和国；vinegar 醋；kowtow 磕头；tsunami 海啸'),
    ('H28', '合成规律', '各截两个词的一段拼成一个新词，意思是两样合在一起',
     'smog = sm(oke)（烟）+ (f)og（雾）；vlog = v(ideo) + (b)log；podcast = (i)Pod + (broad)cast。截去的那一段一般能从剩下的字母猜出来。'
     '这类词都连写，多是近代造的新词。',
     'smog 烟雾；vlog 视频博客；podcast 播客'),
    ('H29', '合成规律', '用 man 合成的词，复数只把 man 改成 men；不分男女时多用 person 或别的说法',
     'postman → postmen、businessman → businessmen：只改 man 这一截。今天说不分男女的人多用 -person（salesperson、businessperson）'
     '或换个词（firefighter 代替 fireman）。注意 German、human 不是用 man 合成的，复数加 s：Germans、humans。',
     'postmen 邮递员们；businessmen 商人们；salesperson 售货员'),
    ('H30', '合成规律', '中间的 s 是古英语表示“的”的词尾留下来的',
     'craftsman 古时写作 craftes man“手艺的人”，salesman 是 sale 加上表示“的”的 -s 再加 man（卖货的人），中间的 s 相当于今天的 \'s。'
     'spokesman 是照着 craftsman 这样的词造的。',
     'craftsman 工匠；salesperson 售货员；spokesman 发言人'),
    ('H31', '合成规律', '合成词的复数加在主体上，主体在后加在最后，主体在前就加在前面',
     'grown-up → grown-ups、check-up → check-ups：主体在最后，s 加在最后；passer-by → passers-by：主体是 passer“走过的人”，'
     'by 只是说明“从旁边”，所以 s 加在 passer 上（同 mother-in-law → mothers-in-law）。',
     'passers-by 过路人；grown-ups 大人们；check-ups 体检'),
    ('H32', '合成规律', '两个词连成一个词以后，意思固定下来，不再是两个词简单相加',
     'greenhouse 是温室，不是“绿色的房子”（a green house）；hot dog 是热狗，不是“热的狗”。读的时候也不一样：'
     '合成词重音在前（ˈgreenhouse），两个分开的词重音在后（a green ˈhouse）。',
     'greenhouse 温室；hot-dog 热狗；deadline 截止日期'),
    ('H33', '合成规律', '词尾加在整个短语上，短语先连成一个词，再带上词尾',
     'sixth grade（六年级）加上 -er（…的人）→ sixth-grader 六年级学生；four post（四根柱子）加上 -er → four-poster 四柱床；'
     'eight years old 连成 eight-year-old 以后，还能当名词“八岁的孩子”，复数 eight-year-olds。',
     'sixth-grader 六年级学生；four-poster 四柱床'),
    ('H34', '合成规律', 'self 放在前面，说这件事是对自己做的，或是自己做的，后面的词是主体',
     'self-control 控制自己、self-esteem 对自己的看重、self-driving 自己会开的。英语说“对自己的…”“由自己…”时，常把 self 放在最前面，'
     '后面的词是主体；这和 paper-cutting 把宾语挪到前面是一个道理：control oneself → self-control。',
     'self-control 自制力；self-esteem 自尊；self-driving 自动驾驶的'),
    # ---------------------------------------------------------------- 写法：连写、加连字符、分开写
    ('W01', '写法', '合成词常走分开写、加连字符、连写这条路，用熟了、定型了的就连写，不加连字符',
     '新的合成词刚出现时常分开写或加连字符，用的人多了、大家都认得了，就连写成一个词：to-morrow → tomorrow、web site → website、e-mail → email。'
     '所以常用的老合成词多连写（classroom、notebook），新的、少见的多带连字符。',
     'classroom；website（早期写作 web site）；tomorrow（以前写作 to-morrow）'),
    ('W02', '写法', '还没用熟的合成词常用连字符把几个词连成一个，用熟了多会连写',
     '连字符告诉读者“这几个词是一个词”。新造的、少见的、临时组合的合成词常这样写（paper-cutting、survey-taker、aqua-classroom），'
     '以后用的人多了，常常连写（e-mail → email）。词典里同一个词常有两三种写法，就是因为它正走在这条路上。',
     'paper-cutting；survey-taker；e-mail / email'),
    ('W03', '写法', '几个词合起来当一个形容词用，中间加连字符，表明它们是一个整体，放在名词前时尤其要加',
     'a well-known writer、a part-time job、an energy-saving lamp。连字符提醒读者：这几个词合起来才说明后面的名词，免得读错'
     '（a man-eating shark 吃人的鲨鱼 ≠ a man eating shark 一个在吃鲨鱼的人）。其中“well + 过去分词”、整个短语这两类放在 be 后面时常分开写：'
     'The writer is well known. / The map is up to date.',
     'well-known；energy-saving；kind-hearted；up-to-date'),
    ('W04', '写法', '动词短语变成的名词、形容词，加连字符或连写；当动词用总是分开写；名词重音在前，动词重音在后',
     'take off（起飞，动词）→ takeoff（名词）；make up → make-up / makeup；check up → check-up。同一个说法，分开写是动词短语，连起来是名词；'
     '读音也跟着变：take ˈoff → ˈtakeoff。英式多加连字符，美式多连写。',
     'takeoff；make-up / makeup；check-up；setup'),
    ('W05', '写法', '二十一到九十九的两位数、分数，中间都加连字符',
     'twenty-one、forty-five、ninety-nine；one-third、two-fifths。百位、千位之间不加：three hundred and five。',
     'forty-five；ninety-nine；one-third'),
    ('W06', '写法', '字母、缩写、数字和单词合成时，中间加连字符',
     'e-book（e = electronic）、X-ray、AI-powered、3D-printed、6th-grader。不加连字符，字母和单词粘在一起就认不出来了。'
     '用得非常多的也会连写：e-mail → email。',
     'e-book；X-ray；AI-powered；6th-grader'),
    ('W07', '写法', 'self 打头的合成词都加连字符',
     'self-control、self-esteem、self-driving：self 在前面表示“自己、对自己、由自己”，这类词一律加连字符；'
     'selfish、selfless 里的 self 是词的主体，后面是后缀，不加。',
     'self-control；self-esteem；self-driving'),
    ('W08', '写法', '名词后面接 like、free、friendly、based、related 这类词时多加连字符，用久了的有的连写',
     'cat-like、sugar-free、user-friendly、nature-based、job-related、heart-shaped、solar-powered。这类词的后半截像后缀一样能接很多名词，'
     '新组合一般加连字符；用了很久的老词有的已经连写（childlike、worldwide、waterproof）。'
     '-like 前面的词以 l 结尾、很长或是专有名词时，一定加连字符（bell-like，免得三个 l 连在一起）。',
     'cat-like；sugar-free；user-friendly；nature-based'),
    ('W09', '写法', '并列的两个词之间加连字符，表示和、兼、对',
     'teacher-director（老师兼导演）、urban-rural（城乡）、problem-solution（问题—解决）。用 and 连起来的短语每两个词之间都加：'
     'black-and-white、hide-and-seek。方位词例外：northeast、southwest 早就连写。',
     'teacher-director；urban-rural；black-and-white'),
    ('W10', '写法', '整个短语当一个词用时，每两个词之间都加连字符，不当一个词用就分开写',
     'an up-to-date map / The map is up to date.；a face-to-face talk / meet face to face；mother-in-law、forget-me-not 这类本身就是名词的短语也加。',
     'up-to-date；face-to-face；step-by-step'),
    ('W11', '写法', '连写成一个词和分开写成两个词，意思、用法不一样',
     'everyday（日常的）↔ every day（每天）；anyone（任何人）↔ any one（任何一个）；maybe（也许）↔ may be（可能是）；'
     'already（已经）↔ all ready（都准备好了）；sometime（某个时候）↔ some time（一段时间）。写作时最容易写错。',
     'everyday / every day；maybe / may be；already / all ready'),
    ('W12', '写法', '少数很老、很常用的合成词连写时掉了字母，一般的合成词两个词原样拼起来，字母重了也不删',
     'all → al：already、also、although、almost、altogether；well → wel：welfare；full → ful：fulfil；pass → pas：pastime；till → til：until。'
     '一般的合成词两个词照原样拼：roommate（mm）、earring（rr）、nighttime（tt）、granddaughter（dd），一个字母都不删。',
     'already；welfare；roommate；earring'),
    ('W13', '写法', '前缀一般和后面的词连写，后面是大写字母、数字，或是新的、临时的组合，或是两个元音挨在一起时，加连字符',
     'mid-January、non-VR（大写字母前一定加）；post-movie、mini-doctor（临时组合）；co-author（两个元音挨在一起）；'
     'non-verbal / nonverbal（英式多加，美式多连写）。',
     'mid-January；non-VR；co-author；non-verbal'),
    ('W14', '写法', '重复的词、模仿声音的词，中间加连字符',
     'tuk-tuk、quack-quack-quack、ping-pong、peep-peep-peep。',
     'ping-pong；tuk-tuk'),
    ('W15', '写法', '两个词缩成一个时，用撇号代替省掉的字母',
     'would not → wouldn\'t（撇号代替 not 里的 o）；it is → it\'s；I am → I\'m。',
     "wouldn't"),
    ('W16', '写法', '这类名词平时多分开写成两个词，放在名词前当形容词时才加连字符',
     'science fiction（科幻小说）/ a science-fiction movie；first aid（急救）/ a first-aid kit；rush hour / rush-hour traffic。'
     '英语里很多名词合成词是分开写的：ice cream、high school、living room。',
     'science-fiction；first-aid；rush-hour'),
    ('W17', '写法', '专有名词首字母大写，合成的部分连写',
     '国名、节日、星期、人名这些专有名词，首字母大写，合成的部分连写：England、Saturday、Thanksgiving、Shakespeare。',
     'England；Saturday；Thanksgiving'),
    ('W18', '写法', 'ly 结尾的副词和后面的词连用，按多数写作规范不加连字符',
     'a highly skilled worker、a remotely operated vehicle、an environmentally friendly product：-ly 已经表明它是副词、修饰后面的词，不会读错，'
     '所以多数写作规范不加连字符；加了也常见，但不推荐。',
     'highly-skilled；remotely-operated；environmentally-friendly'),
]

BY_ID = {r[0]: r for r in RULES}
TEXT = {r[0]: r[2] for r in RULES}
KIND = {r[0]: r[1] for r in RULES}

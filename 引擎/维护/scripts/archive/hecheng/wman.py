"""手写的合成规律：MAN[词] = [(规律代码, 括号里的话)]，代替自动生成的；MANX[词] = {规律代码: 括号里的话}，第二行特殊规律；
PLURAL：数词 + 名词那一类，接在例子后面的单复数说明。"""

MAN = {}
def m(w, *pairs):
    MAN[w] = list(pairs)

# ---------------------------------------------------------------- 外语里就合成好的（H27）：讲那种语言里的先后
m('republic', ('H27', '拉丁语 res publica =“事 + 公共的”：拉丁语的形容词常放在名词后面，“公共的事”就说成“事 + 公共的”；同 vinegar：法语 vin aigre“酒 + 酸的”'))
m('surgery', ('H27', '希腊语 kheirourgia = kheir（手）+ ergon（工作）“用手干活”，说明在前、主体在后；经拉丁语、法语一路磨短成 surg-；同 allergy'))
m('allergy', ('H27', '1906 年德国医生用希腊语 allos（别的）+ ergon（作用）造的 Allergie，说明在前、主体在后；同 surgery'))
m('platform', ('H27', '法语 plateforme = plate（平的）+ forme（形状），整个借进英语，照原样连写；同 republic'))
m('helicopter', ('H27', '1861 年法国人用希腊语 helix（螺旋，加词尾写成 helico-）+ pteron（翅膀）造的 hélicoptère，说明在前、主体在后；后人切错成 heli + copter（见词根列）；同 dinosaur'))
m('standard', ('H27', '古法语 estandart“军旗”：主流说法是 stand 站 + ard 牢，“插在地上站得牢牢的旗杆”，整个借进英语，说法不一，见单词部分；同 platform'))
m('medieval', ('H27', '现代拉丁语 medium aevum“中间的 + 时代”，英语加上 -al 造成形容词；同 longevity 里的 aevum“一生、岁月”'))
m('carnival', ('H27', '意大利语 carnevale，出自中世纪拉丁语 carnelevare =“肉 + 拿走”：宾语在前、动词在后（拉丁语常把动词放在最后），斋期一开始就把肉撤下饭桌；同 vintage：vindemia“葡萄 + 摘下”'))
m('artifact', ('H27', '拉丁语 arte factum“凭手艺 + 做成的”：说“用什么”的在前，和英语 handmade 一样；同 manuscript：manu scriptus“用手 + 写成的”'))
m('alarm', ('H27', '意大利语的一声喊 all\'arme!“拿起武器！”= a（到）+ le（那些）+ arme（武器）：整个介词短语借进来，经法语 alarme 进入英语；同 deluxe'))
m('agriculture', ('H27', '拉丁语 agri cultura =“田地的 + 耕种”：“谁的”在前、主体在后，和英语一样；拉丁语里原是两个词，后来合写；同 legislator'))
m('encyclopedia', ('H27', '希腊语 enkyklios paideia“一整圈的 + 教育”：形容词在前、主体在后，后人把两个词连成一个；同 agriculture'))
m('kindergarten', ('H27', '德语 Kinder（孩子们）+ Garten（花园）：德语也是“谁的”在前、主体在后，和英语一样；英语照德语拼法写 -garten；同 agriculture'))
m('longevity', ('H27', '拉丁语 longaevitas：longus（长）+ aevum（一生）先合成 longaevus“长寿的”，再加上 -itas（英语 -ity）；同 medieval'))
m('madam', ('H27', '古法语 ma dame“我的 + 夫人”：“我的”在前，和英语 my lady 一样；两个词连写，去掉了词尾的 e；同 deluxe'))
m('maintain', ('H27', '拉丁语 manu tenere“用手 + 握住”：说“用什么”的在前、动词在后；同 manuscript：manu scriptus“用手写的”'))
m('manufacture', ('H27', '拉丁语 manu（用手）+ factura（做出来这件事）：说“用什么”的在前、主体在后，和英语 handmade 的先后一样；同 maintain'))
m('maneuver', ('H27', '中世纪拉丁语 manu operare“用手 + 干活”，经法语 manœuvre 进入英语：“用什么”在前、动词在后；同 maintain'))
m('manuscript', ('H27', '拉丁语 manu scriptus“用手 + 写成的”：“用什么”在前、过去分词在后，和英语 handwritten 一模一样；同 maintain'))
m('centipede', ('H27', '拉丁语 centipeda =“一百 + 脚”：数词在前、主体在后；同 octopus：希腊语“八 + 脚”'))
m('pedestal', ('H27', '意大利语 piedistallo = pie（脚）+ di（…的）+ stallo（位置、座）“座子的脚”：用“的”（di）连起来时主体在前，和英语 the foot of… 一样；经法语 piédestal 进入英语'))
m('bankrupt', ('H27', '意大利语 banca rotta“长凳 + 破了的”：形容词放在名词后面；同 republic：res publica“事 + 公共的”'))
m('alchemy', ('H27', '阿拉伯语 al-kimiya：al 是阿拉伯语的 the，连冠词一起借进来；同 algebra：al-jabr'))
m('privilege', ('H27', '拉丁语 privilegium = privus（单个人的）+ lex（法律）“只针对一个人的法律”：“谁的”在前、主体在后；同 legislator'))
m('leopard', ('H27', '希腊人把 leōn（狮子）+ pardos（豹）拼成 leopardos“狮豹”，两样并列：古人以为它是狮子和豹子生的；同 octopus'))
m('melody', ('H27', '希腊语 melōidia = melos（歌的一节）+ ōidē（歌），说明在前、主体在后；同 tragedy：“山羊 + 歌”'))
m('tragedy', ('H27', '希腊语 tragōidia“山羊 + 歌”，说明在前、主体在后（为什么是山羊说法不一，见组合列下文）；同 comedy：“狂欢 + 歌”'))
m('comedy', ('H27', '希腊语 kōmōidia“狂欢 + 歌”，说明在前、主体在后；同 tragedy：“山羊 + 歌”'))
m('legislate', ('H27', '拉丁语 legis lator“法律的 + 提出者”：英语先借了 legislator，再截掉 -or 倒推出动词 legislate；同 legislator'))
m('legislator', ('H27', '拉丁语 legis lator“法律的 + 提出者”两个词连写：“谁的”在前、主体在后；同 agriculture：agri cultura“田地的 + 耕种”'))
m('octopus', ('H27', '希腊语 oktōpous =“八 + 脚”：数词在前、主体在后；同 centipede：拉丁语“一百 + 脚”'))
m('atmosphere', ('H27', '17 世纪学者用希腊语 atmos（水汽）+ sphaira（球）造的 atmosphaera，说明在前、主体在后；同 dinosaur'))
m('deluxe', ('H27', '法语短语 de luxe“奢华的”（de 相当于 of）：介词短语整个借进来，后来连写成一个词；同 denim：de Nîmes'))
m('picnic', ('H27', '法语 piquenique：pique、nique 前后押韵，最早是讽刺诗里虚构的人名，整个借进英语；同 ping-pong 这类押韵、重复的词'))
m('squirrel', ('H27', '希腊语 skiouros = skia（影子）+ oura（尾巴）“影子尾巴”，说明在前、主体在后；经拉丁语、法语进入英语时又加上了表示“小”的词尾'))
m('rosemary', ('H27', '拉丁语 ros marinus“露水 + 海的”：形容词放在名词后面；英语后来把它改成了 rose（玫瑰）+ Mary 的样子；同 republic'))
m('tsunami', ('H27', '日语“津波”：tsu（港口）+ nami（浪），日语也是说明在前、主体在后，和英语一样；同 karate：“空 + 手”'))
m('emoji', ('H27', '日语“絵文字”：e（画）+ moji（文字），说明在前、主体在后；同 tsunami：“港口 + 浪”'))
m('vintage', ('H27', '拉丁语 vindemia =“葡萄 + 摘下”：宾语在前（拉丁语常把动词放在后面），经法语 vendage 进入英语；同 carnival：“肉 + 拿走”'))
m('vinegar', ('H27', '法语 vin aigre“酒 + 酸的”：法语的形容词常放在名词后面；同 republic：res publica“事 + 公共的”'))
m('alphabet', ('H27', '希腊人拿字母表开头的两个字母 alpha、beta 连起来叫整套字母（汉语也说“ABC”指入门）；同 algebra'))
m('slogan', ('H27', '盖尔语 sluagh-ghairm“军队 + 呼喊”：说明在前、主体在后，本是苏格兰高地氏族的战斗口号；同 tsunami'))
m('pharaoh', ('H27', '古埃及语 pr-aa“房子 + 大的”：形容词放在名词后面，本指王宫，后来指住在里面的国王；同 republic'))
m('pajamas', ('H27', '波斯语 pae jamah“腿 + 衣服”：说明在前、主体在后，经印地语进入英语；同 tsunami'))
m('algebra', ('H27', '阿拉伯语 al-jabr：al（the）+ jabr（接合、复原），出自一本数学书的书名，连冠词一起借进来；同 alchemy'))
m('dinosaur', ('H27', '1841 年英国学者用希腊语 deinos（可怕的）+ sauros（蜥蜴）造的 Dinosauria，说明在前、主体在后；同 helicopter'))
m('malaria', ('H27', '意大利语 mala aria“坏的 + 空气”：这里形容词在前，连读时省掉一个 a；同 bankrupt：banca rotta 形容词在后'))
m('ad-lib', ('H27', '拉丁语短语 ad libitum“按 + 心意”，英语截短成 ad lib；同 deluxe：法语 de luxe'))
m('alligator', ('H27', '西班牙语 el lagarto“那只 + 蜥蜴”：连冠词一起借进来；同 algebra：al-jabr'))
m('chameleon', ('H27', '希腊语 khamaileōn“地上的 + 狮子”，说明在前、主体在后；同 leopard：“狮 + 豹”'))
m('ostrich', ('H27', '俗拉丁语 avis struthio“鸟 + 鸵鸟”：先说类名“鸟”，经古法语 ostruce 缩成 ostrich；同 reindeer（类名 deer 在后）'))
m('terracotta', ('H27', '意大利语 terra cotta“土 + 烧过的”：形容词放在名词后面；同 vinegar：法语 vin aigre'))
m('Vietnam', ('H27', '越南语 Việt Nam“越 + 南”：越南语的说明词放在后面，“南方的越”就说成“越 + 南”（汉字写作“越南”）；同 republic'))
m('caterpillar', ('H27', '古北部法语 catepelose“猫 + 多毛的”：形容词放在名词后面；同 terracotta'))
m('cobalt', ('H27', '德语 Kobold“家宅地精”= kobe（小屋）+ 精灵，说明在前、主体在后；矿工以为难炼的矿是地精在捣鬼，就拿它叫这种金属'))
m('protocol', ('H27', '希腊语 prōtokollon“第一 + 粘上去的（纸）”，说明在前、主体在后；同 dinosaur'))
m('denim', ('H27', '法语短语 serge de Nîmes“尼姆产的斜纹呢”：英语只留下 de Nîmes，连写成一个词；同 deluxe：de luxe'))
m('gallop', ('H27', '法兰克语 *wala hlaupan“好好地 + 跑”（词典说“很可能”）：副词在前、动词在后，经法语进入英语；同 maintain'))
m('karate', ('H27', '日语“空手”：kara（空）+ te（手），说明在前、主体在后；同 tsunami：“港口 + 浪”'))
m('ketchup', ('H27', '闽南话“膎汁”kê-chiap：膎（腌鱼）+ 汁，说明在前、主体在后（来源说法不一）；同 kowtow：“磕头”'))
m('petroleum', ('H27', '中世纪拉丁语 petra（岩石）+ oleum（油）“岩石油”，说明在前、主体在后；同 agriculture'))

# ---------------------------------------------------------------- 像一句命令（H11）
m('scarecrow', ('H11', 'scare crows（吓走乌鸦）→ scarecrow：最早指受雇在田里赶鸟的人，后来指稻草人；同 pastime：pass time → pastime'))
m('breakfast', ('H11', 'break fast（打破禁食：一夜没吃东西，早上头一顿饭把它打破）→ breakfast；同 scarecrow'))
m('pastime', ('H11', 'pass time（打发时间）→ pastime：照着法语 passe-temps 造的，passe 是“过”的命令式；同 scarecrow'))
m('ceasefire', ('H11', 'Cease fire!（停止射击！）原是战场上的口令 → ceasefire 停火；同 scarecrow'))
m('makeshift', ('H11', 'make shift（想个办法应付）→ makeshift 临时凑合的（东西）；同 scarecrow'))
m('farewell', ('H11', 'Fare well!（一路走好！）道别时的一句话 → farewell 告别；同 ceasefire'))
m('Shakespeare', ('H11', 'shake spear（挥舞长矛）→ 姓 Shakespeare“使长矛的人”；同类的老姓还有 Shakelance、Shakeshaft；同 scarecrow'))
m('passport', ('H11', '法语 passeport：passe（通过！）+ port（港口）“准你通过港口的文书”；法语造词爱把动词放在前面；同 pastime：passe-temps'))
m('portfolio', ('H11', '意大利语 portafoglio：porta（拿着！）+ foglio（纸页）“拿纸页的东西”= 文件夹；意大利语造词也爱把动词放在前面；同 passport'))
m('wardrobe', ('H11', '北部古法语 warderobe：warder（看管）+ robe（衣服）“看管衣服的地方”；同 passport'))
m('kowtow', ('H11', '汉语“磕头”：磕（动词）+ 头（宾语），汉语动词在前，借进英语照原样；同 pastime'))

# ---------------------------------------------------------------- 并列（H14）
m('teacher-director', ('H14', '既是老师又是负责人（导演）；同 singer-actor-dancer 歌手兼演员兼舞者'))
m('human-tech', ('H14', '人和技术之间的；同 urban-rural 城乡的'))
m('give-and-take', ('H14', 'give（给）和 take（拿）：有给有拿 → 互相让步；同 hide-and-seek 一边躲一边找'))
m('problem-solution', ('H14', '问题和解决办法并列成一对，不是“对问题的解决”；同 cause-and-effect 原因和结果'))
m('cause-and-effect', ('H14', '原因和结果并列成一对；同 problem-solution'))
m('science-music', ('H14', '科学和音乐平起平坐，结合在一起；同 stem-art 理工加艺术'))
m('right-and-wrong', ('H14', '对和错并列；同 black-and-white 黑白的'))
m('hide-and-seek', ('H14', 'hide（躲）和 seek（找）：一边躲一边找 → 捉迷藏；同 give-and-take'))
m('southeast', ('H14', 'south + east：南和东之间 → 东南；英语南北在前、东西在后，汉语正好相反；同 northwest 西北'))
m('southwest', ('H14', 'south + west：南和西之间 → 西南；英语南北在前，汉语东西在前；同 northeast 东北'))
m('northwest', ('H14', 'north + west：北和西之间 → 西北；英语南北在前，汉语东西在前；同 southeast 东南'))
m('northeast', ('H14', 'north + east：北和东之间 → 东北；英语南北在前，汉语东西在前；同 southwest 西南'))
m('compound-complex', ('H14', '既是并列句又是复合句的（语法术语）；同 teacher-director'))
m('black-and-white', ('H14', 'black 和 white 并列：又黑又白 → 黑白的；同 blue-and-white 蓝白相间的'))
m('white-yellow', ('H14', '两个颜色平起平坐：白里带黄、白黄相间；同 golden-brown 金棕色的'))
m('time-and-money', ('H14', '时间和金钱并列；同 cause-and-effect'))
m('blue-and-white', ('H14', 'blue 和 white 并列：蓝白相间 → 青花的；同 black-and-white'))
m('singer-actor-dancer', ('H14', '三个身份平起平坐：歌手兼演员兼舞者；同 teacher-director'))
m('ping-pong', ('H14', 'ping（乒）+ pong（乓）：两个模仿击球声的词并在一起，换个元音重复；同 quack-quack-quack 嘎嘎嘎'))
m('urban-rural', ('H14', '城市和乡村之间的，两个形容词并列；同 parent-teacher 家长和老师之间的'))
m('golden-brown', ('H14', '金色和棕色平起平坐：金色里透着棕；同 white-yellow'))
m('stem-art', ('H14', '理工四科和艺术并列；同 science-music'))
m('quack-quack-quack', ('H14', '把鸭叫声 quack 原样重复三遍；同 ping-pong'))
m('parent-teacher', ('H14', '家长和老师之间的，两个名词并列；同 urban-rural'))
m('lullaby', ('H14', 'lulla + by：两个哄孩子睡觉时哼的声音并在一起，“噜啦——拜”；同 ping-pong'))

# ---------------------------------------------------------------- 近义叠用、加类名（H15）
m('until', ('H15', 'un（到）+ till（到）：两个“到”叠在一起，更强调“一直到那个点”；同 underneath'))
m('underneath', ('H15', 'under（在下面）+ neath（在下面）：两个“在下面”叠在一起，更强调就在正下方；同 until'))
m('courtyard', ('H15', 'court（院子）+ yard（院子）：两个说“院子”的词叠在一起；同 pathway'))
m('pathway', ('H15', 'path（小路）+ way（路）：两个说“路”的词叠在一起；同 alleyway'))
m('alleyway', ('H15', 'alley（小巷）+ way（路）：两个说“路”的词叠在一起；同 pathway'))
m('reindeer', ('H15', 'rein 在古北欧语里本来就是“驯鹿”，英语里不认得了，再加上类名 deer“鹿”；同 chestnut'))
m('chestnut', ('H15', 'chest 本来就是“栗子”（来自希腊语 kastanea），后来再加上类名 nut“坚果”；同 reindeer'))
m('peafowl', ('H15', 'pea 本来就是“孔雀”（古英语 pawa），再加上类名 fowl“禽鸟”；同 reindeer'))
m('charcoal', ('H15', 'char 也许本来就是“木炭”（法语 charbon），再加上 coal“炭”，成了“炭 + 炭”；也有词典说 char 是“变成”。说法不一；同 reindeer'))

# ---------------------------------------------------------------- 有这个特点的人或东西（H16）
m('humpback', ('H16', 'hump（隆起）+ back（背）：本是“驼着的背”，拿来叫背驼的人，又叫背上鼓起一块的座头鲸（humpback whale）；同 high-five'))
m('Bluetooth', ('H16', 'blue（蓝）+ tooth（牙）：本是十世纪一位丹麦国王的绰号“蓝牙”，拿来给把设备连起来的无线技术起名；说的不是牙；同 humpback'))
m('high-five', ('H16', 'high（高处的）+ five（五指，一只手）：举到高处的手 → 击掌；说的不是“五”，是这个动作；同 high-rise'))
m('high-rise', ('H16', 'high（高）+ rise（升起）：升得很高的 → 高楼；说的不是“升起”，是有这个特点的楼；同 high-five'))
m('barefoot', ('H16', 'bare（光着的）+ foot（脚）：光着的脚 → 光着脚的、光着脚地，说的是人的样子；同 high-five'))
m('freelance', ('H16', 'free（自由的）+ lance（长矛）：没跟定哪个主人的长矛 → 拿长矛的雇佣兵（司各特 1820 年的小说里这样用）→ 自由职业者；同 high-five'))

# ---------------------------------------------------------------- 词尾加在整个短语上（H33）
for _w, _p in [('6th-grader', '6th grade'), ('7th-grader', '7th grade'), ('sixth-grader', 'sixth grade'), ('seventh-grader', 'seventh grade'),
               ('eighth-grader', 'eighth grade'), ('ninth-grader', 'ninth grade')]:
    m(_w, ('H33', '%s（年级）先连成一个词，再带上 -er（…的人）→ %s；同 four-poster' % (_p, _w)))
m('6th-graders', ('H33', '6th grade 连成一个词带上 -er，复数 s 加在最后：6th-graders；同 7th-graders'))
m('7th-graders', ('H33', '7th grade 连成一个词带上 -er，复数 s 加在最后：7th-graders；同 6th-graders'))
m('four-poster', ('H33', 'four posts（四根柱子）先连成 four-post（名词用单数），再带上 -er（有…的东西）→ four-poster 四柱床；同 sixth-grader'),
  ('H16', '说的不是柱子，是有四根柱子的床；同 high-rise'))
m('year-old', ('H33', 'eight years old（八岁）连成 eight-year-old 当形容词（year 用单数），还能当名词“八岁的孩子”，复数 eight-year-olds；year-old 就是这一串里“…岁的”那一截；同 eight-year-old'))

# ---------------------------------------------------------------- 个别词手写
m('paper-cutting', ('H02', 'cut paper 剪纸 → paper-cutting；倒过来写成 cutting-paper，主体就成了 paper，是“剪着用的纸”，就像 notepaper 是写便条用的纸；同 make paper → paper-making'))
m('setup', ('H08', 'set up 建立、安排 → setup；倒过来的 upset 是“打翻、心烦”，前后一换意思就变；同 make up → make-up'))
m('upset', ('H09', 'up + set（往上放）→ upset，后来意思变成“打翻、心烦”；和 set up → setup（建立、设置）是同一对词倒过来，意思差得很远；同 outcome：come out → outcome'))
m('outlook', ('H09', 'look out（往外看）→ outlook 景色 → 前景、看法；倒过来的 lookout 是“瞭望、警戒”，前后一换意思就变；同 outcome：come out → outcome'))
m('download', ('H09', 'down（向下）+ load（装）：往下装 → 下载；同 upload：往上装 → 上传'))
m('upload', ('H09', 'up（向上）+ load（装）：往上装 → 上传；同 download：往下装 → 下载'))
m('passer-by', ('H08', 'pass by（从旁边走过）→ passer-by：-er 加在动词 pass 上，by 留在后面；同 grow up → grown-up'))
m('passers-by', ('H08', 'pass by（从旁边走过）→ passer-by，复数 passers-by；同 grow up → grown-ups'))
m('well-worn', ('H05', 'worn a lot（被用了很多次）→ well-worn，well 在这里是“充分地、很多”；同 know well → well-known'))
m('hard-earned', ('H05', 'earned by working hard（辛辛苦苦挣来的）→ hard-earned，副词 hard 挪到过去分词前面；同 work hard → hard-working'))
m('brand-new', ('H06', 'brand 本指燃烧的木头、烧红的铁：new as a brand（像刚出火的一样新）→ brand-new；同 as high as the sky → sky-high'))
m('maybe', ('H07', 'it may be（可能是这样）缩成一个副词 maybe“也许”，先后不变；同 worthwhile：worth while → worthwhile'))
m('highly-skilled', ('H07', 'highly skilled（技术非常好的）：副词放在形容词前面，本来就是英语正常的先后；同 environmentally-friendly'))
m('environmentally-friendly', ('H07', 'environmentally friendly（在环境方面友好的）：副词放在形容词前面，先后不变；换成名词就要挪到前面：friendly to the environment → eco-friendly'))
m('upside-down', ('H07', '最早是 up so down“上面的像是成了下面的”，后来改成 upside down（上面那一面朝下），先后不变；同 one-size-fits-all'))
m('never-ending', ('H07', 'it never ends（永远不会结束）→ never-ending：never 本来就在动词前面，先后不变；同 never-seen-before'))
m('never-smiling', ('H07', 'he never smiles（从不笑）→ never-smiling：never 本来就在动词前面，先后不变；同 never-ending'))
m('never-seen-before', ('H07', 'never seen before（以前从没被看见过的）整个短语放到名词前：never-seen-before footage；同 never-ending'))
m('much-anticipated', ('H07', 'much anticipated（大大期待着的）：much 本来就放在过去分词前面，先后不变 → the much-anticipated sequel；同 never-ending'))
m('newfound', ('H07', 'newly found（新近找到的）：new 在这里当副词“新近”用，先后不变 → newfound confidence；同 much-anticipated'))
m('fresh-cut', ('H07', 'freshly cut（刚剪下的）：fresh 在这里当副词“刚刚”用，先后不变 → fresh-cut flowers；同 newfound'))
m('rivals-turned-ally', ('H07', 'rivals turned ally（对手变成了盟友）整个短语当名词用；“X-turned-Y”是常见格式（actor-turned-politician 演员出身的政治家）；同 one-size-fits-all'))
m('wouldn\'t', )

MAN.pop("wouldn't")

# ---------------------------------------------------------------- 第二行（特殊规律）的括号
MANX = {}
def x(w, rid, body):
    MANX.setdefault(w, {})[rid] = body

_MEN = {
    'sportsman': ('sportsmen', ''), 'sportsmen': ('sportsman', ''), 'nobleman': ('noblemen', ''), 'middleman': ('middlemen', ''),
    'middlemen': ('middleman', ''), 'gentleman': ('gentlemen', ''), 'gentlemen': ('gentleman', ''), 'repairman': ('repairmen', ''),
    'weatherman': ('weathermen', ''), 'freshman': ('freshmen', ''), 'freshmen': ('freshman', ''), 'fireman': ('firemen', '不分男女说 firefighter'),
    'fisherman': ('fishermen', ''), 'cameraman': ('cameramen', ''), 'businessman': ('businessmen', '不分男女说 businessperson'),
    'businessmen': ('businessman', '不分男女说 businesspeople'), 'footman': ('footmen', ''), 'footmen': ('footman', ''),
    'mailman': ('mailmen', ''), 'Frenchman': ('Frenchmen', ''), 'Englishman': ('Englishmen', ''), 'craftsman': ('craftsmen', '不分男女说 craftsperson'),
    'craftsmen': ('craftsman', '不分男女说 craftspeople'), 'snowmen': ('snowman', ''), 'policemen': ('policeman', '不分男女说 police officers'),
    'postman': ('postmen', ''), 'postmen': ('postman', ''), 'boatman': ('boatmen', ''), 'boatmen': ('boatman', ''),
    'spokesman': ('spokesmen', '不分男女说 spokesperson'), 'policewoman': ('policewomen', ''), 'policewomen': ('policewoman', ''),
    'postwoman': ('postwomen', ''), 'saleswoman': ('saleswomen', ''), 'businesswoman': ('businesswomen', ''), 'craftswoman': ('craftswomen', ''),
}
for _w, (_o, _alt) in _MEN.items():
    if _w.endswith(('man', 'woman')):
        body = '%s 的复数是 %s' % (_w, _o)
    else:
        body = '%s 是 %s 的复数' % (_w, _o)
    if _alt:
        body += '；' + _alt
    body += '；同 postman → postmen' if _w not in ('postman', 'postmen') else '；同 policeman → policemen'
    x(_w, 'H29', body)
x('salesgirl', 'H29', '不分男女说 salesperson（复数 salespeople）')
x('salesperson', 'H29', 'salesman 的不分男女的说法，复数 salespeople；同 businessperson')
x('businessperson', 'H29', 'businessman 的不分男女的说法，复数 businesspeople；同 salesperson')
x('craftsperson', 'H29', 'craftsman 的不分男女的说法；复数 craftspeople；同 salesperson')
x('craftspeople', 'H29', 'craftsperson 的复数，不分男女；同 businesspeople')
x('craftsman', 'H30', 'craftsman 古时写作 craftes man“手艺的人”，s 相当于今天的 \'s；同 salesperson')
x('craftsmen', 'H30', '同 craftsman：古时写作 craftes man“手艺的人”')
x('craftsperson', 'H30', '照 craftsman 的样子，中间留着那个 s')
x('craftspeople', 'H30', '照 craftsman 的样子，中间留着那个 s')
x('craftswoman', 'H30', '照 craftsman 的样子，中间留着那个 s')
x('salesperson', 'H30', 'sales 的 s 原是 sale 表示“的”的词尾：salesman 就是“卖货的人”；同 craftsman')
x('saleswoman', 'H30', '同 salesman：sale 加表示“的”的 s 再加 woman')
x('salesgirl', 'H30', '同 salesman：sale 加表示“的”的 s 再加 girl')
x('spokesman', 'H30', 'spoke（speak 的过去式）+ s + man：这个 s 不表示“的”，是照着 craftsman 这样的词加的；同 craftsman')
x('passer-by', 'H31', '主体是 passer“走过的人”，by 只说明“从旁边”，复数 s 加在前面：passers-by；同 grown-up → grown-ups（主体在后，s 加在最后）')
x('passers-by', 'H31', 'passer-by 的复数：主体 passer 在前，s 就加在 passer 上；同 grown-ups')
x('grown-ups', 'H31', 'grown-up 当名词“大人”，复数 s 加在最后；比较 passer-by → passers-by')
x('check-ups', 'H31', 'check-up 的复数，s 加在最后；同 trade-offs')
x('trade-offs', 'H31', 'trade-off 的复数，s 加在最后；同 check-ups')
x('6th-graders', 'H31', 'sixth-grader 的复数，s 加在最后；同 7th-graders')
x('7th-graders', 'H31', 'seventh-grader 的复数，s 加在最后；同 6th-graders')
x('greenhouse', 'H32', 'greenhouse 温室 ≠ a green house 一座绿色的房子；读音也不同：ˈgreenhouse 重音在前，a green ˈhouse 重音在后；同 hot-dog')
x('hot-dog', 'H32', 'hot dog 热狗 ≠ 热的狗；同 greenhouse 温室 ≠ 绿色的房子')
x('deadline', 'H32', 'deadline 截止日期 ≠ 一条死掉的线；同 greenhouse')
x('highlight', 'H32', 'highlight 最精彩的部分 ≠ 高处的光；同 greenhouse')
x('blueprint', 'H32', 'blueprint 蓝图、计划 ≠ 一张蓝色的印刷品；同 greenhouse')
x('hotline', 'H32', 'hotline 热线 ≠ 一条热的线；同 hot-dog')
x('software', 'H32', 'software 软件 ≠ 软的货；同 hardware 硬件')
x('hardware', 'H32', 'hardware 五金、硬件 ≠ 硬的货；同 software 软件')
x('blacklist', 'H32', 'blacklist 黑名单 ≠ 一张黑色的名单；同 greenhouse')

# ---------------------------------------------------------------- 数词 + 名词：例子后面的单复数说明
PLURAL = {
    'one-time': '换成别的数，time 也不加 s：a two-time champion 两届冠军',
    'one-day': '换成别的数，day 也不加 s：a four-day trip；不放在名词前时用复数：The trip lasts four days.',
    'one-way': 'way 用单数；同 two-way',
    'two-way': '不说 a two-ways street',
    'two-storey': '不说 a two-storeys house；不放在名词前时用复数：The house has two storeys.',
    'one-step': '换成别的数，step 也不加 s：a three-step plan',
    'one-person': '换成别的数，person 也不变：a three-person team（不说 three-people team）',
    'ten-dollar': '不说 a ten-dollars bill；不放在名词前时用复数：It costs ten dollars.',
    'eighth-grade': '不放在名词前时分开写：She is in eighth grade.',
    'seven-mile': '不说 a seven-miles walk；不放在名词前时用复数：We walked seven miles.',
    'hundred-year': '不放在名词前时用复数：a hundred years',
    'single-dish': 'single 相当于 one，dish 用单数',
    'third-floor': '不放在名词前时分开写：on the third floor',
    '100-foot-tall': 'foot 用单数，不说 100-feet-tall；放在 be 后面用复数、不加连字符：The tree is 100 feet tall.',
    'four-day': '不说 a four-days week；不放在名词前时用复数：four days',
    'five-hundred-metre': 'metre 用单数；当比赛项目名时说 the 500 metres',
    'three-dimensional': 'three dimensions（三个维度）→ dimension 用单数再加 -al：three-dimensional',
    'two-hour': '不说 a two-hours meeting；不放在名词前时用复数：The meeting lasted two hours.',
    'fifteen-year': '不说 a fifteen-years plan；不放在名词前时用复数：The plan lasts fifteen years.',
    'fifteen-minute': '不说 a fifteen-minutes walk；不放在名词前时用复数：It takes fifteen minutes.',
    'one-bedroom': '换成别的数，bedroom 也不加 s：a three-bedroom house',
    'three-bedroom': '不说 a three-bedrooms house；不放在名词前时用复数：The house has three bedrooms.',
}
for _n in ['eight', 'fourteen', 'six', 'thirteen', 'twelve', 'eighteen', 'fifteen', 'five', 'four', 'thousand', 'three']:
    PLURAL['%s-year-old' % _n] = 'year 用单数，不说 %s-years-old；不放在名词前时用复数、分开写：She is %s years old.' % (_n, _n if _n != 'thousand' else 'a thousand')
PLURAL['thousand-year-old'] = 'year 用单数，不说 thousand-years-old；不放在名词前时用复数、分开写：The tree is a thousand years old.'

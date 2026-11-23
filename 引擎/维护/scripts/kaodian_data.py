# -*- coding: utf-8 -*-
"""考点列（2026-11 考纲考点轮，第 121 条）用的人工整理材料。每一样都写明出处，kaodian.py 用它算出每一行考点的出处（--show 时打印，不写进表）。

出处（S1–S4 是网址，S5 起是评价指南里的条目）：
  S1 上海市教育考试院《2020年上海市初中英语课程终结性评价指南词汇表》https://www.shmeea.edu.cn/download/20190926/07.pdf
     （整理成 references/kaogang/kaogang.json：单词 1724 条、词组 342 条、括号标注 136 个，附录的代词、数词、月份星期、国家和人）
  S2 上海市教育考试院《2020年上海市初中英语课程终结性评价指南》https://www.shmeea.edu.cn/download/20190926/03.pdf
     词汇：①单词释义 ②词形变化 ③构词法（合成、派生、转化）；词法：名词复数、不可数名词、代词、数词、比较级最高级、
     动词时态语态、不定式、动名词……；题型示例：a ___ driver (care) → careless
  S3 二一教育网《上海2022年中考复习：词性转换专题训练》https://zy.21cnjy.com/11977654
     “出题量最大的方向——同词根不同词类之间的相互转换”；“必考方向——名词复数、代词、数词”；列了上百组常考转换
  S4 上海中考、区模考“用括号中所给单词的适当形式完成句子”的原题（见 SH_EXAM 每一条后面的出处）
"""

SRC = {
    'S1': '考纲词汇表（上海市教育考试院 2020）',
    'S2': '评价指南（上海市教育考试院 2020）',
    'S3': '上海中考词性转换复习资料（二一教育网）',
}

# ---------- 上海复习资料（S3）里点名的转换：(给的词, 要填的词)。只收两头至少有一个在考纲里的
SH_CONV = [
    # 动词 → 名词
    ('pollute', 'pollution'), ('invent', 'invention'), ('discuss', 'discussion'), ('decide', 'decision'), ('solve', 'solution'),
    ('invite', 'invitation'), ('organize', 'organization'), ('work', 'worker'), ('teach', 'teacher'), ('write', 'writer'),
    ('speak', 'speaker'), ('run', 'runner'), ('win', 'winner'), ('invent', 'inventor'), ('act', 'actor'), ('visit', 'visitor'),
    ('build', 'building'), ('begin', 'beginning'), ('paint', 'painting'), ('mean', 'meaning'), ('develop', 'development'),
    ('amuse', 'amusement'), ('wait', 'waitress'), ('act', 'actress'), ('appear', 'appearance'), ('perform', 'performance'),
    ('serve', 'service'), ('speak', 'speech'), ('fish', 'fisherman'), ('enter', 'entrance'), ('know', 'knowledge'),
    ('weigh', 'weight'), ('please', 'pleasure'), ('choose', 'choice'), ('tour', 'tourist'), ('die', 'death'),
    ('succeed', 'success'), ('fly', 'flight'), ('memorize', 'memory'), ('mix', 'mixture'), ('safe', 'safety'),
    ('act', 'activity'), ('able', 'ability'), ('operate', 'operation'), ('locate', 'location'), ('produce', 'product'),
    ('sell', 'sale'), ('bake', 'baker'), ('enjoy', 'joy'),
    # 动词 → 形容词
    ('act', 'active'), ('attract', 'attractive'), ('change', 'changeable'), ('enjoy', 'enjoyable'), ('excite', 'exciting'),
    ('follow', 'following'), ('freeze', 'freezing'), ('freeze', 'frozen'), ('frighten', 'frightened'), ('bore', 'bored'),
    ('forget', 'forgetful'), ('forget', 'unforgettable'), ('depend', 'independent'), ('like', 'likely'), ('break', 'broken'),
    ('die', 'dead'), ('live', 'alive'), ('please', 'pleasant'), ('please', 'pleased'), ('satisfy', 'satisfied'),
    ('sleep', 'asleep'), ('wide', 'widen'), ('rich', 'enrich'), ('able', 'enable'),
    # 名词 → 形容词
    ('care', 'careful'), ('use', 'useful'), ('power', 'powerful'), ('care', 'careless'), ('home', 'homeless'),
    ('help', 'helpless'), ('help', 'helpful'), ('use', 'useless'), ('friend', 'friendly'), ('love', 'lovely'), ('sun', 'sunny'),
    ('wind', 'windy'), ('health', 'healthy'), ('noise', 'noisy'), ('luck', 'lucky'), ('fun', 'funny'),
    ('interest', 'interesting'), ('south', 'southern'), ('north', 'northern'), ('danger', 'dangerous'), ('wood', 'wooden'),
    ('gold', 'golden'), ('nation', 'national'), ('education', 'educational'), ('medicine', 'medical'), ('nature', 'natural'),
    ('chemistry', 'chemical'), ('history', 'historical'), ('physics', 'physical'), ('tradition', 'traditional'),
    ('office', 'official'), ('fool', 'foolish'), ('foreigner', 'foreign'), ('wound', 'wounded'), ('electricity', 'electric'),
    # 形容词 → 名词
    ('difficult', 'difficulty'), ('honest', 'honesty'), ('different', 'difference'), ('important', 'importance'),
    ('ill', 'illness'), ('kind', 'kindness'), ('sad', 'sadness'), ('happy', 'happiness'), ('free', 'freedom'),
    ('wise', 'wisdom'), ('high', 'height'), ('long', 'length'), ('true', 'truth'), ('responsible', 'responsibility'),
    # 形容词 → 副词
    ('careful', 'carefully'), ('main', 'mainly'), ('easy', 'easily'), ('heavy', 'heavily'), ('lucky', 'luckily'),
    ('possible', 'possibly'), ('gentle', 'gently'), ('terrible', 'terribly'), ('true', 'truly'), ('nice', 'nicely'),
    ('wide', 'widely'), ('safe', 'safely'), ('deep', 'deeply'), ('polite', 'politely'), ('correct', 'correctly'),
    ('serious', 'seriously'), ('proper', 'properly'), ('recent', 'recently'), ('immediate', 'immediately'),
    # 名词 → 名词
    ('art', 'artist'), ('science', 'scientist'), ('piano', 'pianist'), ('city', 'citizen'), ('custom', 'customer'),
    ('engine', 'engineer'), ('friend', 'friendship'), ('business', 'businessman'), ('law', 'lawyer'), ('library', 'librarian'),
    ('music', 'musician'), ('office', 'officer'),
    # 前缀
    ('possible', 'impossible'), ('polite', 'impolite'), ('patient', 'impatient'), ('healthy', 'unhealthy'), ('happy', 'unhappy'),
    ('lucky', 'unlucky'), ('honest', 'dishonest'), ('appear', 'disappear'), ('like', 'dislike'), ('fair', 'unfair'),
    ('advantage', 'disadvantage'), ('necessary', 'unnecessary'), ('male', 'female'), ('regular', 'irregular'),
    # 国名 → 国籍
    ('Australia', 'Australian'), ('America', 'American'), ('Canada', 'Canadian'), ('Britain', 'British'), ('England', 'English'),
    ('Italy', 'Italian'), ('France', 'French'), ('Germany', 'German'), ('China', 'Chinese'), ('Japan', 'Japanese'),
]

# ---------- 上海中考、区模考的原题（S4）：(给的词, 答案) → 出处。只收在搜索结果里看得到原题和答案的
SH_EXAM = {
    ('box', 'boxes'): '2019 上海中考：three ___ of local snacks (box)',
    ('eight', 'eighth'): '2019 上海中考：On the ___ page of the book (eight)',
    ('entrance', 'enter'): '2019 上海中考：you will ___ your dream school (entrance)',
    ('stamp', 'stamps'): '2018 上海中考：likes to collect ___ (stamp)',
    ('six', 'sixth'): '2018 上海中考：The ___ lady from the left (six)',
    ('she', 'herself'): '2018 上海中考：cooked a meal…by ___ (she)',
    ('policeman', 'policemen'): '2018 上海中考：Tony\'s father and uncle are both ___ (policeman)',
    ('it', 'its'): '2021 上海中考：with ___ beautiful night view (it)',
    ('harm', 'harmful'): '2021 上海中考：the release of ___ chemicals (harm)',
    ('care', 'careless'): '2020 评价指南题型示例：a ___ driver (care)',
    ('dictionary', 'dictionaries'): '2024 宝山一模：look up…in ___ (dictionary)',
    ('nine', 'ninth'): '2024 宝山一模、2023 长宁一模：the ___ floor (nine)',
    ('bad', 'worse'): '2024 宝山一模 (bad) → worse',
    ('operation', 'operate'): '2024 宝山一模 (operation) → operate',
    ('possible', 'possibly'): '2024 宝山一模 (possible) → possibly',
    ('invent', 'invention'): '2024 宝山一模 (invent) → inventions',
    ('necessary', 'unnecessary'): '2024 宝山一模 (necessary) → unnecessary',
    ('discover', 'discovery'): '2023 静安二模：The ___ of silver (discover)',
    ('twenty', 'twenties'): '2023 静安二模：in her ___ (twenty)',
    ('her', 'hers'): '2023 静安二模：buying one like ___ (her)',
    ('climb', 'climber'): '2023 静安二模：a mountain ___ (climb)',
    ('China', 'Chinese'): '2023 静安二模：likes ___ food (China)',
    ('bright', 'brightly'): '2023 静安二模：The Sun shines ___ (bright)',
    ('success', 'successful'): '2023 长宁一模：you will be ___ (success)',
    ('library', 'libraries'): '2023 长宁一模：two ___ in our school (library)',
    ('fireman', 'firemen'): '2023 闵行二模：two ___ were slightly injured (fireman)',
    ('toy', 'toys'): '2023 松江二模：all his ___ (toy)',
    ('serve', 'service'): '2024 黄浦二模：has been in ___ (serve)',
    ('glove', 'gloves'): '2024 黄浦二模：wear your ___ (glove)',
    ('hopeful', 'hopefully'): '2023 上海一模卷：he asked ___ (hopeful)',
}

# ---------- 名词：常考不可数、单复数同形、只用复数、可数不可数两用（S2 词法①b、c；S1 里 paper、glass 的注释）
UNCOUNT = {
    # 中考常考的不可数名词（量词、谓语单复数、不说 an / 不加 s 的题）；“不可数”后面那半句，空着就只写“不可数，没有复数”
    'advice': 'a piece of advice，不说 an advice', 'information': 'a piece of information', 'news': '以 s 结尾也不可数，谓语用单数',
    'homework': '不说 homeworks', 'housework': '不说 houseworks', 'furniture': 'a piece of furniture', 'luggage': 'a piece of luggage',
    'knowledge': '', 'weather': '不说 a weather', 'bread': 'a piece of bread', 'money': 'How much money…?', 'water': 'a glass of water',
    'milk': 'a glass of milk', 'rice': 'a bowl of rice', 'meat': '', 'juice': 'a glass of juice', 'tea': 'a cup of tea',
    'coffee': 'a cup of coffee', 'traffic': 'heavy traffic', 'fun': 'have fun，不说 a fun', 'progress': 'make progress，不说 a progress',
    'luck': 'Good luck!', 'equipment': '',
}
BOTH = {
    'paper': '纸不可数（a piece of paper）；报纸、考卷、文件可数',
    'glass': '玻璃不可数；玻璃杯可数（glasses 还指眼镜）',
    'time': '时间不可数；次数可数（three times）',
    'room': '空间不可数（make room for）；房间可数',
    'experience': '经验不可数；经历可数（experiences）',
    'fish': '鱼肉不可数；鱼的复数还是 fish，种类多时用 fishes',
    'chicken': '鸡肉不可数；鸡可数',
    'food': '总称不可数；说种类时可数（foods）',
    'fruit': '总称不可数；说种类时可数（fruits）',
    'hair': '头发总称不可数；几根头发可数',
    'exercise': '锻炼不可数（take exercise）；练习、体操可数（do exercises）',
}
PLURAL_ONLY = {'clothes': '只用复数，没有单数', 'trousers': '只用复数（a pair of trousers）', 'jeans': '只用复数（a pair of jeans）',
               'people': '本身就是复数，谓语用复数', 'manner': '“礼貌”用复数 manners', 'manners': '“礼貌”用复数 manners', 'chopstick': '一般成双说：a pair of chopsticks'}
SAME_FORM = {'sheep': '单复数同形', 'Chinese': '中国人单复数同形', 'Japanese': '日本人单复数同形', 'deer': '单复数同形'}
PL_TRAP = {'German': '复数 Germans（不是 Germen，易错）', 'human': '复数 humans（不是 humen，易错）'}
# 元音字母 + y 结尾，直接加 s（模考考过 toys）
VOWEL_Y = {'toy', 'key', 'monkey', 'turkey', 'journey', 'holiday', 'survey', 'boy', 'day', 'way', 'birthday'}
# 以 o 结尾：加 es 的只有这几个（考纲里的）
O_ES = {'hero', 'potato', 'tomato'}

# ---------- 形容词：比较级、最高级的难点（S2 词法⑤d；不规则的看 S1 的括号）
ADJ_DOUBLE = {'big', 'fat', 'hot', 'thin', 'wet', 'sad'}
ADJ_Y = {'angry', 'busy', 'dirty', 'dry', 'early', 'easy', 'friendly', 'funny', 'happy', 'healthy', 'heavy', 'hungry', 'lazy',
         'lonely', 'lovely', 'lucky', 'noisy', 'pretty', 'silly', 'tidy', 'crazy', 'thirsty'}
ADJ_IRREG_EXTRA = {'old': ('older / elder', 'oldest / eldest', 'elder、eldest 只说家里的兄弟姐妹')}

# ---------- 动词拼写里另外要提一句的（S2 词形变化）
VERB_NOTE = {
    'write': 'written 双写 t，writing 只有一个 t（易错）',
    'lie': '“躺”是 lay、lain；“说谎”是 lied、lied；现在分词都是 lying',
    'hang': '“悬挂”是 hung、hung；“绞死”是 hanged、hanged',
    'travel': '英式 travelled、travelling，美式 traveled、traveling',
    'die': '现在分词 dying（ie 变 y）',
    'tie': '现在分词 tying（ie 变 y）',
}

# ---------- 用法（S2 词法、句法；“句型转换”指上海中考“按要求改写句子”里常考的同义替换）
B = {
    'ing': '评价指南·动名词作宾语', 'inf': '评价指南·不定式作宾语、宾补', 'bare': '评价指南·不带 to 的不定式',
    'tense': '评价指南·动词时态', 'zhuan': '上海中考句型转换（同义替换）', 'n': '评价指南·名词（可数、不可数）',
    'adj': '评价指南·形容词', 'adv': '评价指南·副词', 'pron': '评价指南·代词', 'conj': '评价指南·连词、从句',
    'prep': '评价指南·介词', 'num': '评价指南·数词', 'modal': '评价指南·情态动词', 'link': '评价指南·连系动词',
    'excl': '评价指南·感叹句', 'voice': '评价指南·语态', 'phr': '考纲词组表', 'kg': '考纲词汇表的注释', 'v': '评价指南·动词',
}
USAGE = {
    # 动词 + doing
    'enjoy': [('enjoy doing sth.；enjoy oneself 玩得开心', 'ing')],
    'finish': [('finish doing sth.（不说 finish to do）', 'ing')],
    'mind': [('mind doing sth.；Would you mind doing…?', 'ing')],
    'practice': [('practise doing sth.（动词英式写 practise）', 'ing')],
    'keep': [('keep doing sth. 一直做；keep + 形容词（keep quiet）', 'ing')],
    'avoid': [('avoid doing sth.', 'ing')],
    'consider': [('consider doing sth.', 'ing')],
    'suggest': [('suggest doing sth.（不说 suggest sb. to do）', 'ing'), ('suggest that sb. (should) do sth.', 'conj')],
    'succeed': [('succeed in doing sth.', 'ing')],
    'thank': [('thank sb. for (doing) sth.', 'ing')],
    'worth': [('be worth doing（主动形式表示被动）', 'ing')],
    'busy': [('be busy with sth. / be busy doing sth.', 'phr')],
    # 动词 + to do / sb. to do
    'afford': [('afford to do / afford sth.（常和 can、can\'t 连用）', 'inf')],
    'decide': [('decide to do = make a decision to do（句型转换）', 'zhuan')],
    'hope': [('hope to do / hope that…，不说 hope sb. to do', 'inf')],
    'wish': [('wish sb. to do；wish sb. sth.（祝愿）', 'inf')],
    'want': [('want to do / want sb. to do', 'inf')],
    'plan': [('plan to do sth.', 'inf')],
    'agree': [('agree to do sth.；agree with sb. 同意某人', 'inf')],
    'refuse': [('refuse to do sth.', 'inf')],
    'manage': [('manage to do sth. 设法做成', 'inf')],
    'fail': [('fail to do sth. 没能做成', 'inf')],
    'expect': [('expect to do / expect sb. to do', 'inf')],
    'learn': [('learn to do sth.；learn from 向…学习', 'inf')],
    'promise': [('promise to do sth.', 'inf')],
    'pretend': [('pretend to do sth.', 'inf')],
    'offer': [('offer to do；offer sb. sth. = offer sth. to sb.', 'inf')],
    'choose': [('choose to do sth.', 'inf')],
    'prepare': [('prepare to do；prepare for 为…做准备', 'inf')],
    'allow': [('allow sb. to do；allow doing', 'inf')],
    'ask': [('ask sb. (not) to do sth.', 'inf')],
    'tell': [('tell sb. (not) to do sth.', 'inf')],
    'advise': [('advise sb. to do sth.', 'inf')],
    'encourage': [('encourage sb. to do sth.', 'inf')],
    'invite': [('invite sb. to do sth.', 'inf')],
    'teach': [('teach sb. to do / teach sb. sth.', 'inf')],
    'warn': [('warn sb. (not) to do sth.', 'inf')],
    'remind': [('remind sb. to do sth.；remind sb. of sth.', 'inf')],
    'order': [('order sb. to do sth. 命令某人做', 'inf'), ('in order to = so that（句型转换）', 'zhuan')],
    'help': [('help sb. (to) do / help sb. with sth.', 'inf')],
    'need': [('need to do（实义动词）；needn\'t do（情态动词）', 'modal')],
    'dare': [('dare not do（疑问、否定句里后面不带 to）', 'kg')],
    # 两种都能接、意思不同
    'stop': [('stop doing 停止正在做的；stop to do 停下来去做另一件事', 'ing')],
    'remember': [('remember doing 记得做过；remember to do 记得要做', 'ing')],
    'forget': [('forget doing 忘了做过；forget to do 忘了要做', 'ing')],
    'try': [('try to do 尽力做；try doing 试着做', 'ing')],
    # 不带 to
    'let': [('let sb. do（不带 to）', 'bare')],
    'make': [('make sb. do（不带 to）；被动 be made to do', 'bare')],
    'have': [('have sb. do sth.；have to 不得不', 'bare')],
    'see': [('see sb. do 看见全过程；see sb. doing 看见正在做', 'bare')],
    'hear': [('hear sb. do / doing', 'bare')],
    'watch': [('watch sb. do / doing', 'bare')],
    'notice': [('notice sb. do / doing', 'bare')],
    # 花费
    'spend': [('spend 时间、钱 on sth. / (in) doing（主语是人）', 'zhuan')],
    'cost': [('sth. costs sb. 钱（主语是物）', 'zhuan')],
    'pay': [('pay 钱 for sth.（主语是人）', 'zhuan')],
    'take': [('It takes sb. 时间 to do sth.', 'zhuan')],
    # 短暂动词
    'buy': [('短暂动词：和一段时间连用改成 have had', 'tense')],
    'die': [('短暂动词：和一段时间连用改成 have been dead', 'tense')],
    'borrow': [('短暂动词：借多久用 keep（keep it for two weeks）', 'tense')],
    'join': [('短暂动词：加入多久用 be in / be a member of', 'tense')],
    'leave': [('leave for 动身去；短暂动词，离开多久用 be away', 'tense')],
    'begin': [('短暂动词：开始多久用 be on', 'tense')],
    # 其他动词
    'arrive': [('arrive at 小地方 / in 大地方 = get to = reach', 'zhuan')],
    'reach': [('reach + 地点（不加介词）= arrive at / in', 'zhuan')],
    'belong': [('belong to sb.（不用进行时，没有被动）', 'phr')],
    'happen': [('happen to sb.；happen to do 碰巧做（没有被动）', 'phr')],
    'seem': [('seem to do / seem + 形容词 = It seems that…', 'zhuan')],
    'look': [('look + 形容词（look happy）；look like 看上去像', 'link')],
    'feel': [('feel + 形容词（feel tired）', 'link')],
    'sound': [('sound + 形容词（That sounds great.）', 'link')],
    'smell': [('smell + 形容词（smell good）', 'link')],
    'taste': [('taste + 形容词（taste delicious）', 'link')],
    'become': [('系动词，后接形容词或名词', 'link')],
    'turn': [('turn + 形容词 变得（turn red）', 'link')],
    'grow': [('grow + 形容词 变得（grow old）', 'link')],
    'depend': [('depend on 依靠、取决于 = rely on（句型转换）', 'zhuan')],
    'rely': [('rely on = depend on（句型转换）', 'zhuan')],
    'prevent': [('prevent…from doing = stop / keep…from doing', 'zhuan')],
    'protect': [('protect…from… 保护…免受…', 'phr')],
    'provide': [('provide sb. with sth. = provide sth. for sb.', 'phr')],
    'share': [('share sth. with sb.', 'phr')],
    'worry': [('worry about = be worried about（句型转换）', 'zhuan')],
    'care': [('take care of = look after（句型转换）', 'zhuan')],
    'use': [('used to do 过去常常；be used to doing 习惯于', 'phr')],
    'prefer': [('prefer A to B；prefer to do sth.', 'phr')],
    'explain': [('explain sth. to sb.（不说 explain sb. sth.）', 'v')],
    'walk': [('walk to … = go to … on foot（句型转换）', 'zhuan')],
    'waste': [('waste 时间、钱 on sth. / (in) doing sth.', 'ing')],
    'cook': [('厨师就是 cook；cooker 是炊具（易错）', 'n')],
    # 名词
    'population': [('人口用 large / small，不说 many / much；What\'s the population of…?', 'n')],
    'temperature': [('温度说 high / low', 'n')],
    'matter': [('What\'s the matter (with sb.)? = What\'s wrong (with sb.)?（句型转换）', 'zhuan')],
    'chess': [('play chess，棋类、球类前面不加 the', 'n')],
    'football': [('play football，球类前面不加 the', 'n')],
    'basketball': [('play basketball，球类前面不加 the', 'n')],
    'volleyball': [('play volleyball，球类前面不加 the', 'n')],
    'tennis': [('play tennis，球类前面不加 the', 'n')],
    'piano': [('play the piano，乐器前面加 the', 'n')],
    'violin': [('play the violin，乐器前面加 the', 'n')],
    'guitar': [('play the guitar，乐器前面加 the', 'n')],
    'hour': [('前面用 an：an hour（h 不发音）', 'n')],
    'honest': [('前面用 an：an honest boy（h 不发音）', 'adj')],
    'useful': [('前面用 a：a useful book（u 读 /juː/）', 'adj')],
    'university': [('前面用 a：a university（u 读 /juː/）', 'n')],
    'uniform': [('前面用 a：a uniform（u 读 /juː/）', 'n')],
    'family': [('看作整体，谓语用单数；指一家人，谓语用复数', 'n')],
    'number': [('a number of + 复数（谓语复数）；the number of…（谓语单数）', 'n')],
    'pair': [('a pair of + 复数名词，谓语跟着 pair 变', 'n')],
    'price': [('价格说 high / low，不说 expensive / cheap', 'n')],
    'hundred': [('前面有具体数字不加 s（two hundred）；hundreds of 好几百', 'num')],
    'thousand': [('前面有具体数字不加 s（five thousand）；thousands of 成千上万', 'num')],
    'million': [('前面有具体数字不加 s（two million）；millions of 数百万', 'num')],
    'habit': [('get into the habit of doing 养成…的习惯', 'phr')],
    # 形容词
    'afraid': [('be afraid of doing / be afraid to do；I\'m afraid (that)…', 'phr')],
    'good': [('be good at = do well in（句型转换）', 'zhuan')],
    'famous': [('be famous for 因…出名', 'phr')],
    'different': [('be different from ↔ the same as（句型转换）', 'zhuan')],
    'full': [('be full of 充满', 'phr')],
    'proud': [('be proud of 为…自豪', 'phr')],
    'ready': [('be ready for sth. / be ready to do', 'phr')],
    'strict': [('be strict with sb.', 'phr')],
    'interested': [('be interested in (doing) sth.', 'phr')],
    'enough': [('形容词、副词放在前面（old enough）；名词放在后面（enough money）', 'adj')],
    'kind': [('It\'s kind of you to do sth.（夸人的形容词用 of）', 'adj')],
    'alive': [('只作表语或放在名词后面（keep the fish alive）', 'adj')],
    'asleep': [('只作表语：fall asleep 睡着', 'adj')],
    # 副词
    'perhaps': [('perhaps = maybe（句型转换）', 'zhuan')],
    'almost': [('almost = nearly（句型转换）', 'zhuan')],
    'ever': [('现在完成时：Have you ever…?', 'tense')],
    'never': [('现在完成时：I have never…；反意疑问句用肯定', 'tense')],
    'just': [('just 刚刚（现在完成时）；just now 刚才（一般过去时）', 'tense')],
    'already': [('现在完成时的标志：have already done', 'tense')],
    'yet': [('现在完成时的否定句、疑问句：haven\'t…yet', 'tense')],
    'since': [('since + 时间点 / 过去时的句子，主句用现在完成时', 'tense')],
    'ago': [('一段时间 + ago，用一般过去时', 'tense')],
    'hardly': [('表示否定，反意疑问句用肯定（He can hardly…, can he?）', 'adv')],
    'seldom': [('表示否定，反意疑问句用肯定', 'adv')],
    'else': [('放在疑问词、不定代词后面：what else、something else', 'adv')],
    'instead': [('instead 放句末；instead of + 名词 / doing', 'phr')],
    'once': [('一次 once、两次 twice、三次以上 three times', 'num')],
    'twice': [('一次 once、两次 twice、三次以上 three times', 'num')],
    # 连词
    'if': [('条件状语从句主将从现；宾语从句里是“是否”', 'conj')],
    'unless': [('unless = if…not（句型转换），主将从现', 'zhuan')],
    'until': [('not…until 直到…才', 'conj')],
    'although': [('although 不和 but 连用', 'conj')],
    'though': [('though 不和 but 连用', 'conj')],
    'because': [('because 不和 so 连用；because of + 名词', 'conj')],
    'whether': [('whether…or not；宾语从句用陈述语序', 'conj')],
    'both': [('both…and 连接主语，谓语用复数', 'conj')],
    'either': [('either…or 连接主语，谓语跟着最近的主语', 'conj')],
    'neither': [('neither…nor 谓语跟着最近的主语；Neither do I. 我也不', 'conj')],
    # 代词
    'each': [('each 作主语谓语用单数；each of + 复数', 'pron')],
    'every': [('every + 单数名词，谓语用单数', 'pron')],
    'something': [('形容词放在后面：something special', 'pron')],
    'anything': [('形容词放在后面：anything new', 'pron')],
    'nothing': [('形容词放在后面：nothing serious', 'pron')],
    'everything': [('形容词放在后面；作主语谓语用单数', 'pron')],
    'everyone': [('作主语谓语用单数（Everyone is here.）', 'pron')],
    'everybody': [('作主语谓语用单数（Everybody is here.）', 'pron')],
    'none': [('none 回答 how many / how much；no one 回答 who', 'pron')],
    'nobody': [('作主语谓语用单数；回答 who 的问题', 'pron')],
    'it': [('形式主语：It\'s + 形容词 + (for sb.) to do sth.', 'pron')],
    'one': [('one 指同类中的一个；it 指前面说的那一个', 'pron')],
    'what': [('感叹句：What + (a/an) + 形容词 + 名词！', 'excl')],
    'how': [('感叹句：How + 形容词 / 副词！', 'excl')],
    # 介词
    'by': [('by + 交通工具，中间不加冠词（by bus）', 'prep')],
    'without': [('without + 名词 / doing', 'prep')],
    # 情态动词
    'must': [('Must I…? 否定回答用 No, you needn\'t / don\'t have to', 'modal')],
    'may': [('May I…? 否定回答用 No, you can\'t / mustn\'t', 'modal')],
    'shall': [('Shall I / we…? 征求对方意见', 'modal')],
    # 反身代词
    'itself': [('主语和宾语是同一个东西时用（The cat washed itself.）', 'pron')],
}
# 词组那一行（表里写成短语的）
USAGE_PHR = {
    'depend on': [('depend on = rely on（句型转换）', 'zhuan'), ('on 后面接名词、代词或 doing；It depends. 看情况', 'phr')],
}

# ---------- 易混（中考单选、选词填空里的经典辨析；每组的词都在考纲里才用）
CONFUSE = [
    # (挂在哪些词上, 画面上写什么, 区别, 依据类别)
    (['already', 'yet'], 'already / yet', '肯定句用 already，否定句、疑问句用 yet', 'tense'),
    (['ago', 'before'], 'ago / before', 'ago 跟一般过去时，before 单用常跟完成时', 'tense'),
    (['since', 'for'], 'since / for', 'since + 时间点，for + 一段时间', 'tense'),
    (['spend', 'cost', 'pay', 'take'], 'spend / cost / pay / take', 'spend、pay 主语是人，cost 主语是物，take 用 It takes…', 'zhuan'),
    (['say', 'speak', 'talk', 'tell'], 'say / speak / talk / tell', 'say 说内容，speak 说语言，talk 交谈，tell 告诉、讲', 'v'),
    (['look', 'see', 'watch', 'read'], 'look / see / watch / read', 'look 看的动作，see 看见，watch 观看，read 读', 'v'),
    (['hear', 'listen'], 'listen / hear', 'listen 是去听（listen to），hear 是听见', 'v'),
    (['borrow', 'lend', 'keep'], 'borrow / lend / keep', 'borrow 借入，lend 借出，keep 借多久', 'v'),
    (['bring', 'take', 'carry'], 'bring / take / carry', 'bring 带来，take 带走，carry 搬、随身带', 'v'),
    (['arrive', 'reach'], 'arrive / reach / get to', 'arrive 后接 at、in，reach 直接加地点', 'v'),
    (['remember', 'remind'], 'remember / remind', 'remember 是自己记得，remind 是提醒别人', 'v'),
    (['wear', 'dress'], 'wear / put on / dress', 'wear 穿着（状态），put on 穿上（动作），dress 后接人', 'v'),
    (['join', 'attend'], 'join / take part in / attend', 'join 加入组织，take part in 参加活动，attend 出席会议、上课', 'v'),
    (['win', 'beat'], 'win / beat', 'win 赢比赛、奖，beat 打败人、队', 'v'),
    (['hope', 'wish'], 'hope / wish', 'wish 能说 wish sb. to do、wish sb. sth.，hope 不能', 'inf'),
    (['lie', 'lay'], 'lie / lay', 'lie 躺（lay, lain）、说谎（lied），lay 放（laid, laid）', 'v'),
    (['rise', 'raise'], 'rise / raise', 'rise 升起，后面不带宾语，raise 举起、筹钱，要带宾语', 'v'),
    (['fall', 'feel'], 'fell / felt', 'fell 是 fall 的过去式，felt 是 feel 的过去式', 'v'),
    (['few', 'little'], 'few / little', 'few 修饰可数，little 修饰不可数，前面不带 a 表示否定', 'pron'),
    (['many', 'much'], 'many / much', 'many + 可数名词复数，much + 不可数名词', 'pron'),
    (['other', 'another'], 'another / the other / others', 'another 三个以上中另一个，the other 两个中另一个，others 别的', 'pron'),
    (['some', 'any'], 'some / any', 'some 用于肯定句和请求，any 用于否定句、疑问句', 'pron'),
    (['both', 'all', 'either', 'neither'], 'both / all / either / neither', '说两个用 both、either、neither，三个以上用 all', 'pron'),
    (['each', 'every'], 'each / every', 'each 可以单独用、强调个体，every 不能单独用', 'pron'),
    (['too', 'also', 'either'], 'too / also / either', 'too 放句末，also 放句中，否定句用 either', 'adv'),
    (['so', 'such'], 'so / such', 'so + 形容词、副词，such + (a/an) + 形容词 + 名词', 'adv'),
    (['hard', 'hardly'], 'hard / hardly', 'hard 努力地，hardly 几乎不（表示否定）', 'adv'),
    (['near', 'nearly'], 'near / nearly', 'near 在附近，nearly 几乎', 'adv'),
    (['quiet', 'quite'], 'quiet / quite', 'quiet 安静的，quite 相当，拼写易混', 'adj'),
    (['alone', 'lonely'], 'alone / lonely', 'alone 独自（客观），lonely 孤独（心里的感觉）', 'adj'),
    (['die', 'dead', 'death'], 'die / dead / death', 'die 动词，dead 形容词（be dead），death 名词', 'adj'),
    (['alive', 'live', 'lively'], 'alive / live / lively', 'alive 活着的（作表语），live 活的（放名词前），lively 活泼的', 'adj'),
    (['interested', 'interesting'], 'interested / interesting', '-ed 说人的感受，-ing 说事物令人…', 'adj'),
    (['excited', 'exciting'], 'excited / exciting', '-ed 说人的感受，-ing 说事物令人…', 'adj'),
    (['bored', 'boring'], 'bored / boring', '-ed 说人的感受，-ing 说事物令人…', 'adj'),
    (['frightened', 'frightening'], 'frightened / frightening', '-ed 说人的感受，-ing 说事物令人…', 'adj'),
    (['satisfied', 'satisfying'], 'satisfied / satisfying', '-ed 说人的感受，-ing 说事物令人…', 'adj'),
    (['pleased', 'pleasant'], 'pleased / pleasant', 'pleased 说人满意，pleasant 说事物令人愉快', 'adj'),
    (['beside', 'besides', 'except'], 'beside / besides / except', 'beside 在旁边，besides 除…还有，except 除…不算', 'prep'),
    (['among', 'between'], 'between / among', 'between 两者之间，among 三者以上之间', 'prep'),
    (['across', 'through', 'over', 'past'], 'across / through / over / past', 'across 从表面横过，through 从中间穿过，over 从上方越过，past 从旁经过', 'prep'),
    (['noise', 'sound', 'voice'], 'noise / sound / voice', 'noise 噪音，sound 各种声音，voice 人的嗓音', 'n'),
    (['job', 'work'], 'job / work', 'job 可数，work（工作）不可数', 'n'),
    (['trip', 'travel', 'journey', 'tour'], 'trip / travel / journey / tour', 'trip 短途，travel 泛指旅行，journey 长途旅程，tour 观光', 'n'),
    (['maybe'], 'maybe / may be', 'maybe 是副词、放句首，may be 是情态动词 + be', 'adv'),
    (['sometimes'], 'sometimes / sometime / some time', 'sometimes 有时，sometime 某个时候，some time 一段时间', 'adv'),
    (['everyday'], 'everyday / every day', 'everyday 形容词“日常的”，every day 每天', 'adj'),
    (['if', 'whether'], 'if / whether', '后面接 or not、放在句首时只能用 whether', 'conj'),
    (['when', 'while'], 'when / while', 'while 后面接持续的动作，常用进行时', 'conj'),
    (['find'], 'look for / find / find out', 'look for 找（过程），find 找到（结果），find out 查明', 'phr'),
    (['advice', 'advise'], 'advice / advise', 'advice 名词、不可数，advise 动词，拼写易混', 'n'),
    (['practice', 'practise'], 'practice / practise', 'practice 名词，practise 动词（英式）', 'kg'),
    (['breath', 'breathe'], 'breath / breathe', 'breath 名词，breathe 动词，拼写易混', 'n'),
    (['lose', 'lost'], 'lose / lost', 'lose 动词（lost, lost），lost 也是形容词“丢失的、迷路的”', 'kg'),
    (['however'], 'but / however', 'but 直接连两句，however 后面要有逗号', 'conj'),
    (['problem', 'question'], 'problem / question', 'problem 要 solve，question 要 answer', 'n'),
    (['receive', 'accept'], 'receive / accept', 'receive 是收到，accept 是同意接受', 'v'),
    (['ill', 'sick'], 'ill / sick', 'ill 只作表语，sick 还能放在名词前（a sick boy）', 'adj'),
    (['excuse'], 'Excuse me / Sorry', 'Excuse me 打扰之前说，Sorry 做错之后说', 'v'),
    (['suggestion', 'advice'], 'suggestion / advice', 'suggestion 可数（some suggestions），advice 不可数', 'n'),
    (['hear'], 'hear of / hear from', 'hear of 听说，hear from 收到…的来信', 'phr'),
    (['think'], 'think of / think about / think over', 'think of 想起、认为，think about 考虑，think over 仔细考虑', 'phr'),
    (['time'], 'in time / on time', 'in time 及时，on time 准时', 'phr'),
    (['end'], 'in the end / at the end of', 'in the end 最后，at the end of 在…的末尾', 'phr'),
    (['way'], 'by the way / on the way', 'by the way 顺便问一下，on the way 在路上', 'phr'),
    (['make'], 'be made of / be made up of', 'be made of 由…制成，be made up of 由…组成', 'phr'),
    (['use'], 'used to / be used to', 'used to do 过去常常，be used to doing 习惯于', 'phr'),
    (['deal'], 'deal with / do with', 'how 问句用 deal with，what 问句用 do with', 'phr'),
]
# 词组表里成对的（易混挂在两个词上）：在上面 CONFUSE 用单词键，比如 time → in time / on time

# ---------- 短语优先挑的（上海中考句型转换、单选里常见的，考纲词组表里都有）
PHR_TOP = '''take part in|take place|take care of|look after|look forward to|look up|look for|give up|get along|get up|get rid of|
make progress|make a decision|make friends with|make a mistake|pay attention to|pay for|put off|put on|put out|put up|
turn on|turn off|turn down|turn up|be good at|be interested in|be afraid of|be famous for|be proud of|be full of|
be made of|be made up of|be used to|used to|be different from|be similar to|be satisfied with|be pleased with|
be strict with sb.|be late for|be ready for|be busy with sth.|be able to|be supposed to|be responsible for|be fond of|
depend on|rely on|deal with|belong to|agree with|worry about|wait for|listen to|laugh at|hear from|hear of|
think of|think about|think over|come true|come from|find out|run out of|set out|show off|stay up|wake up|grow up|
hand in|fill in|pick up|point out|search for|prefer...to|prevent...from|protect...from|provide...with|stop...from|
keep...from|share...with|tell...from|instead of|because of|in order to|so that|as soon as|as long as|as well|no longer|
more than|at least|at last|in time|on time|in the end|at the end of|at the same time|in fact|for example|such as|
in front of|next to|on foot|by the way|on the way|in danger|in trouble|in a hurry|take action|do one’s best|do harm to|
keep in touch|keep fit|keep doing sth.|would rather|had better|would like|have no idea|so far|one after another|
from time to time|the same...as|too...to|each other|a lot of|plenty of|a pair of|a piece of|take notes|catch cold|
fall asleep|lose weight|make up one’s mind|take off|go on|go over|go out|go wrong|go ahead|get to|get off|get on|
get ready for|give sb. a hand|help sb. with sth.|come on|lose one’s way|make a living|have a good time'''.replace('\n', '').split('|')

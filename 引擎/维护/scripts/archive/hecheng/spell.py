import re, json, sys
sys.path.insert(0, '/home/claude/work/hc')
from catalog import TEXT
from spell_rule import spell_rule
from gen import BYW, CATS, parts, ex_of, ALLW
from wphr import PH

# 写法那一行手写的括号（或连规律一起换）：词 → 括号里的话，或 (规律代码, 括号里的话)
SPELLX = {
    'giant-king': ('W02', '新组合常加连字符；同 giant-killer 屠巨人者（1726 年已见）'),
    'giant-prince': ('W02', '新组合常加连字符；同 giant-king'),
    'time-and-money': 'time-and-money costs；同 a day-to-day job、an up-to-date map',
    'childcare': '也写作 child care',
    'ninety-nine': '同 twenty-one、forty-five',
    'forty-five': '同 twenty-one、ninety-nine',
    'ninety-eight': '整十的 twenty、ninety 不加连字符；同 twenty-one',
    'seventy-nine': '同 twenty-one、forty-five',
    'mud-covered': 'mud-covered boots；同 snow-covered、hand-made、sun-dried',
    'showerhead': 'showerhead / shower head 两种写法都通行',
    'seaview': '词典里多分开写作 sea view；连写的 seaview 多见于酒店、楼盘的名称',
    'deep-sea': 'deep-sea fishing 远洋捕鱼；当名词时分开写：the deep sea 深海',
    'sky-high': 'sky-high prices 天价；同 knee-deep 齐膝深的、ice-cold 冰冷的',
    'urban-rural': 'the urban-rural gap 城乡差距；同 parent-teacher',
    'rivals-turned-ally': '“X-turned-Y”格式：X 是原来的身份，Y 是现在的身份；同 actor-turned-politician 演员出身的政治家',
    'quack-quack-quack': ('W14', '原样重复三遍；tick-tock、ding-dong 这类叠词要换元音，quack-quack-quack 不换'),
    'ping-pong': ('W14', 'ping、pong 换个元音重复；同 tick-tock、ding-dong'),
    'ad-lib': '作动词、名词时常带连字符（ad-lib），作副词常写 ad lib',
    'diamond-like': '-like 有时连写（childlike、lifelike），有时加连字符（diamond-like），两种写法都常见',
    'flatbread': '也有人写作 flat bread',
    'Vietnam': '英语一般连写成 Vietnam；联合国、ISO 和越南政府的标准写法是分开的 Viet Nam（越南语一个音节写成一个词：Việt Nam）',
    'baroque-era': 'baroque-era music；当名词时分开写：the Baroque era',
    'giraffe-necked': 'a giraffe-necked weevil 长颈鹿象鼻虫（马达加斯加的一种甲虫）',

    'black-and-white': 'a black-and-white film；不放在名词前时一般分开写：in black and white（白纸黑字）',
    'century-old': 'a century-old building；同 a ten-year-old boy',
    'decade-old': 'a decade-old dispute；同 a week-old baby、a century-old tradition',
    'ten-dollar': 'a ten-dollar bill 一张十美元钞票',
    'long-term': 'a long-term goal；当名词短语用时分开写：in the long term（同 full-time、high-speed）',
    'year-round': 'a year-round job；短语 all year round 不加连字符：It\'s warm all year round.',
    'fast-food': '名词写作 fast food；放在名词前当形容词时写成 fast-food：a fast-food restaurant',
    'far-off': 'a far-off country；放在 be 后面拆开写：Spring is not far off.（春天不远了）；也写作 faroff',
    'pick-up': '动词短语分开写：pick up；名词、形容词加连字符或连写：a pick-up = a pickup（同 a check-up = a checkup）',
    '6th-graders': '数字和单词之间加连字符',
    '7th-graders': '数字和单词之间加连字符',
    'high-performance': 'a high-performance engine；当名词时分开写：The engine offers high performance.',
    'math-related': 'math-related problems；放在名词后面要拆开说：problems related to math（同 health-related、work-related）',
    'not-for-profit': 'a not-for-profit group；当普通短语用时分开写：The club is run not for profit.',
    'no-waste': 'a no-waste kitchen；同 no-fly zone 禁飞区、no-win situation 怎么做都不利的局面',
    'rush-hour': '名词多写作 rush hour；放在名词前当形容词时加连字符：rush-hour trains',

    'highly-skilled': 'a highly skilled worker：按多数写作规范不加连字符；highly-skilled 的写法常见，但不推荐',
    'remotely-operated': 'a remotely operated vehicle（遥控潜水器，缩写 ROV）：按规范不加连字符',
    'environmentally-friendly': ('W18', 'an environmentally friendly product：多数写作规范不加连字符；也常说 environment-friendly、eco-friendly'),
    'heart-broken': '今天词典多以连写的 heartbroken 为主，heart-broken 是带连字符的写法，意思、用法完全相同',
    'heartbroken': '也写作 heart-broken；今天词典多以连写的 heartbroken 为主',
    'off-course': '放在名词前写 off-course：an off-course plane；放在 be 后面分开写：be off course',
    'teacher-director': '同 singer-songwriter 创作歌手、actor-director 演员兼导演',
    'cross-role': ('W03', 'cross- 和名词连成形容词时多加连字符：cross-role collaboration 跨岗位协作（同 cross-age、cross-cultural）'),
    'cross-age': ('W03', 'cross- 和名词连成形容词时多加连字符：cross-age tutoring（同 cross-role）'),
    'hardworking': '同 hard-working，美式多连写成 hardworking',
    'hard-working': 'a hard-working student；美式多连写成 hardworking',

    'make-up': '英式多写 make-up，美式多连写成 makeup；动词：make up；读音：ˈmake-up（名词）↔ make ˈup（动词）',
    'makeup': '美式多连写成 makeup，英式多写 make-up；动词：make up；读音：ˈmakeup（名词）↔ make ˈup（动词）',
    'made-up': ('W03', 'a made-up story 编出来的故事；放在 be 后面就分开写：The story was made up.'),
    'paper-cutting': ('W02', '也常分开写成 paper cutting；放在名词前当形容词时一般加连字符：paper-cutting art'),
    'wouldn\'t': 'would not → wouldn\'t：撇号代替 not 里的 o',
    'anytime': '美式常连写 anytime；英式多分开写 any time，尤其在 at any time 里',
    'anyone': '分开写的 any one 是“任何一个”，强调“一个”（any one of these books）；anyone 古英语起就两词连用，1844 年才合写成一个词',
    'anybody': '约 1300 年写作 ani-bodi，1826 年起连写成一个词',
    'anymore': '美式多写 anymore，英式多分开写 any more；表示数量“再多一些”时一律分开写：Do you want any more cake?（1865 年起常连写）',
    'anyway': '分开写的 any way 还是本义“以任何方式”（in any way）；连写的 anyway 是“无论如何、反正”（1830s 起常连写）',
    'everyday': 'everyday（一个词）是形容词“日常的”，只放在名词前：everyday life；every day（两个词）是“每天”：I walk to work every day.——写成 I go there everyday 是常见错误',
    'everyone': 'everyone（一个词）= everybody，只指人；every one（两个词）强调“每一个”，人、物都行，常接 of：every one of the books',
    'someday': 'someday（一个词）是“（将来）总有一天”；some day 分开写意思一样，也常见',
    'sometime': 'sometime（一个词）是“某个时候”；some time（两个词）是“一段时间”；sometimes 是“有时”：I\'ll call you sometime. / It takes some time.',
    'somebody': 'somebody = someone；分开写的 some body 是“某个身体、某具尸体”，意思完全不同',
    'someone': 'someone（一个词）= somebody，指人；some one（两个词）强调“某一个”，常接 of：some one of them',
    'nobody': 'nobody = no one；但 no one 必须分开写，不能写成 noone',
    'nothing': 'nothing（一个词）是“没有东西”；no thing 分开写很少见，只在强调“没有一样东西”时用',
    'maybe': 'maybe（一个词）是副词“也许”，多放句首：Maybe he is at home.；may be（两个词）是“情态动词 + be”：He may be at home.',
    'already': 'already（一个词）是“已经”，all 掉了一个 l；分开写的 all ready 是“全都准备好了”（We are all ready.）',
    'altogether': 'altogether（一个词）是“完全；总共”，all 掉了一个 l：That\'s altogether wrong.；all together（两个词）是“全都在一起”：We were all together in the room.',
    'onto': 'onto（到…上面）：起初分开写 on to，1715 年起照着 into 连写；分开写的 on to 是“继续、接着”：move on to the next question（不能连写）',
    'forever': 'forever 是“永远；老是”；英式传统上把“永远”分开写成 for ever（14 世纪就是两个词，17 世纪末起常连写），“老是”的意思只写 forever',
    'faraway': '只放在名词前：a faraway land；放在 be 后面要拆开写：The town is far away.（也写作 far-away）',
    'alone': 'all one 连写时 all 掉了一个 l',
    'also': 'all so 连写时 all 掉了一个 l（同 already、almost、although）',
    'although': 'all though 连写时 all 掉了一个 l（同 also、already）',
    'almost': 'all most 连写时 all 掉了一个 l（同 also、already）',
    'welfare': 'well fare 连写时 well 掉了一个 l（同 welcome 也是 well + come）',
    'fulfil': 'full fill 连写时 full 掉了一个 l；英式写 fulfil，美式写 fulfill',
    'until': 'un + till 连写时 till 掉了一个 l',
    'pastime': 'pass time 连写时掉了一个 s',
    'Christmas': ('W12', 'Christ + mass 连写时 mass 掉了一个 s，t 也不发音：/ˈkrɪsməs/；晚期古英语还是两个词 Cristes mæsse，14 世纪中才连成一个词'),
    'roommate': 'room + mate 两个 m 都写出来（也写作 room-mate）',
    'earring': 'ear + ring 两个 r 都写出来',
    'granddaughter': 'grand + daughter 两个 d 都写出来',
    'nighttime': 'night + time 两个 t 都写出来',
    'headdress': ('W12', 'head + dress 两个 d 都写出来（也写作 head-dress）'),
    'bathhouse': ('W12', 'bath + house 两个 h 都写出来（也可写作 bath-house，1705 年起见用）'),
    'gospel': 'good spell 连写时 good 的 o 变短、d 也掉了（gōdspel → godspel → gospel）',
    'bonfire': 'bone fire 连写时 bone 的 e 掉了，读音也变短：bonfire',
    'shepherd': 'sheep herd 连写时 sheep 的两个 e 剩一个，读 /ˈʃepəd/',
    'England': ('W17', 'Engla land 两个词连写，中间的 a 掉了'),
    'icecream': ('W16', '标准写法是两个词 ice cream；英式放在名词前当形容词时常加连字符：an ice-cream cone；连写成 icecream 一般不算规范拼写'),
    'email': '早期写作 e-mail（1982 年），美联社写作规范 2011 年起改成不带连字符的 email，今天这是主流写法',
    'e-mail': ('W06', 'e = electronic（电子的）；1982 年起写作 e-mail，今天多连写成 email'),
    'website': '1994 年已见，早期多分开写成 web site、Web site，后来连写成 website',
    'tomorrow': '16 世纪前分开写成 to morrow，后来写作 to-morrow，直到 20 世纪初才连写',
    'tonight': '18 世纪以前分开写成 to night，之后写作 to-night，直到 20 世纪初才连写',
    'instead': '17 世纪中以前常分开写成 in stead',
    'indeed': '约 1600 年才合写成一个词',
    'percent': '美式多写 percent（一个词），英式常写 per cent（两个词）；符号 % 读作 percent',
    'blockchain': '2008 年比特币论文里还是分开的 block 和 chain，后来写成 block chain，约 2015 年起连写成 blockchain',
    'soulmate': '1822 年柯勒律治最早写作 soul mate，20 世纪初起连写',
    'wasteland': '1825 年起才连写成一个词',
    'barcode': '1963 年首见时写作 bar code，后来也常连写',
    'healthcare': '美式常分开写 health care，英式多连写 healthcare；放在名词前时也常写成 health-care',
    'teenage': '1911 年起，早先写作 teen age、teen-age，后来连写',
    'freelance': '最初写作两个词 free lance，后来加连字符 free-lance，今多连写',
    'worthwhile': '原是两个词 worth while（值得花时间），后来连写成一个形容词',
    'likewise': '来自短语 in like wise，15 世纪起连写成一个副词',
    'online': '分开写的 on line 在美国口语里还可以是“排着队”（stand on line）',
    'setup': '名词写作 setup / set-up；动词短语要分开写：set up a tent（搭帐篷）、set up a company（创办公司）；名词 ˈsetup 重音在前',
    'takeoff': '名词 takeoff；动词：The plane will take off soon.；读音：ˈtakeoff（名词）↔ take ˈoff（动词）',
    'checkout': '名词 checkout 连写；动词分开写：check out of the hotel',
    'layout': '名词 layout 连写；动词分开写：lay out a garden → the layout of the garden',
    'standby': '分开写的 stand by 是动词短语：stand by sb 支持某人；连写（也写作 stand-by）的 standby 才是名词、形容词',
    'backup': '动词短语分开写：back up your files（备份文件）；名词、形容词连写 backup（也写 back-up）',
    'handout': '动词短语分开写：hand out the papers；名词连写：a handout（同 printout）',
    'workout': '动词短语分开写：work out at the gym；名词连写：a workout',
    'crossover': '名词、形容词 crossover 连写；动词短语分开写：cross over to the other side',
    'tryout': '动词短语分开写：try out for the team；名词连写 tryout（也作 try-out）；读音：动词 try ˈout，名词 ˈtryout',
    'blackout': '名词连写 blackout（也作 black-out）；动词短语分开写：He blacked out.',
    'runoff': '名词也写 run-off；动词短语分开写：The water ran off the roof.',
    'comeback': '动词短语分开写：come back home；名词连写：make a comeback；读音：come ˈback → ˈcomeback',
    'pickup': '动词短语分开写：I\'ll pick you up at six.；名词、形容词连写 pickup 或用连字符 pick-up',
    'cleanup': '作动词必须分开写：clean up the room；作名词连写、加连字符都可以：a cleanup / a clean-up',
    'clean-up': '动词短语分开写：clean up the room；名词连写或加连字符：a clean-up / a cleanup',
    'check-up': '动词短语分开写：check up on sb；名词也写作 checkup',
    'check-ups': '也连写作 checkups',
    'follow-up': '动词短语分开写：follow up on sth；名词、形容词加连字符：a follow-up',
    'warm-up': '动词短语分开写：warm up before running；名词常加连字符：a warm-up',
    'growing-up': '作主语时常分开写：Growing up in the countryside was fun.（在乡下长大很开心）',
    'light-up': '动词短语分开写：Her face lit up.；放在名词前当形容词才加连字符：light-up toys',
    'run-down': '形容词带连字符：a run-down house；动词短语分开写：run down',
    'throw-away': '也连写成 throwaway；动词短语分开写：throw away the rubbish',
    'pop-up': '动词短语分开写：A window popped up.；名词、形容词加连字符：a pop-up window',
    'shake-up': '也写作 shakeup；动词短语分开写：shake up the team',
    'trade-off': '动词短语分开写：trade off speed for safety；名词加连字符：a trade-off',
    'trade-offs': 'trade-off 的复数，动词短语还是分开写：trade off',
    'cut-up': '动词短语分开写：cut up the paper；形容词加连字符：cut-up paper',
    'built-in': '放在名词前当形容词加连字符：a built-in camera；动词短语分开写：build in a shelf',
    'worn-out': '放在名词前加连字符：a worn-out sofa；放在 be 后面通常分开写：I\'m worn out.',
    'dried-up': '放在名词前加连字符：a dried-up river；动词短语分开写：The river dried up.',
    'grown-up': '当名词、形容词加连字符：a grown-up；动词短语分开写：When I grow up…',
    'grown-ups': 'grown-up 的复数；动词短语还是分开写：grow up',
    'leftover': '名词、形容词连写：leftovers；动词短语分开写：There is some food left over.',
    'makeover': '名词连写：a makeover；动词短语分开写：make over the room',
    'takeout': '美式名词连写 takeout（英式说 takeaway）；动词短语分开写：take out the rubbish',
    'turnaround': '名词连写（英式也作 turnround）；动词短语分开写：turn around',
    'stopover': '名词连写（也写作 stop-over）；动词短语分开写：stop over in Paris',
    'setback': '名词连写（也写作 set-back）；动词短语分开写：set back the plan',
    'breakthrough': '名词连写；动词短语分开写：break through the wall',
    'drawback': '名词连写；动词短语分开写：draw back',
    'feedback': '名词连写；动词短语 feed back 分开写，很少用',
    'meltdown': '名词连写；动词短语分开写：The ice melted down.',
    'hideout': '名词连写；动词短语分开写：hide out in the hills',
    'passer-by': '复数 passers-by；也写作 passerby',
    'passers-by': '也写作 passersby',
    'self-check-out': '也写作 self-checkout（中间不再加连字符）',
    'x-ray': ('W06', 'X 代表“未知”：伦琴 1895 年发现它时不知道它是什么；也常写成大写的 X-ray'),
    'wh-question': ('W06', 'wh 指 what、who、where 这类 wh 开头的疑问词'),
    'to-infinitive': ('W06', 'to 是不定式前面那个小词，和术语 infinitive 连起来指“带 to 的不定式”'),
    '100-foot-tall': ('W06', '数字和单词之间加连字符；放在 be 后面用复数、不加连字符：The tree is 100 feet tall.'),
    '3D-printed': ('W06', '3D = three-dimensional（三维的）；放在 be 后面常分开写：The parts were 3D printed.'),
    'year-old': ('W03', 'an eight-year-old girl；单独说年龄时 year 用复数、不加连字符：She is eight years old.'),
}


def ex_or_word(w):
    e = ex_of(w)
    return e if e else ''


GEN = [  # 和规律那句重复的套话：去掉，只留例子
    (r'^(“[^”]*”)?(的)?(复合|合成)(形容词|名词)?(放在名词前)?(时)?(要|常|一般)?(中间)?(加|带)连字符$', ''),
    (r'^(两个词|两词|几个词|三个词)(用|以)?连字符(合成|连成|连接)(一个)?(形容词|整体|名词)?(，?放在名词前)?$', ''),
    (r'^连字符把.*连成(一个)?(前置)?(形容词|整体|名词|临时合成词)$', ''),
    (r'^(作定语|放在名词前作定语|放在名词前|作前置定语|作定语放在名词前|作定语放名词前)(时)?(常|多|一般|要)?(中间)?(加|带|用)连字符$', ''),
    (r'^(作定语|放在名词前作定语|放在名词前|作前置定语|作定语放在名词前|作定语放名词前)(时)?(常|多|一般|要)?(中间)?(加|带|用)连字符[：:]\s*', ''),
    (r'^(作定语|放在名词前作定语|放在名词前|作前置定语|作定语放在名词前|作定语放名词前)(时)?(常|多|一般|要)?(中间)?(加|带|用)连字符（(.*)）$', r'\6'),
    (r'^(作表语|放在 be 后|放在系动词后|放在 be 动词后|放在名词后)(时)?(常|可|一般|多|通常)?(不加(连字符)?|分写|拆开写|分开写|不加连字符)（(.*)）$', r'放在 be 后面常分开写：\6'),
    (r'^(作表语|放在 be 后|放在系动词后|放在 be 动词后|放在名词后)(时)?(常|可|一般|多|通常)?(不加(连字符)?|分写|拆开写|分开写)[：:]\s*', '放在 be 后面常分开写：'),
    (r'^(作副词|作状语)(时)?(多|可|常|一般)?(不加(连字符)?|分写|分开写)[（：:]\s*(.*?)）?$', r'当副词用时常分开写：\6'),
    (r'^也(常)?(连写|分写|分开写)?(作|写作|写|写成|连写作|连写成|分写成|分写作)\s*', r'也写作 '),
    (r'^也可(连写|分写)(成|作)\s*', '也写作 '),
    (r'^(“[^”]*”)(连成|构成)(复合)?(形容词|名词)(放在名词前)?(时)?(，)?(中间)?(要|常)?(加|带)连字符(（(.*)）)?$', r'\12'),
]


def _clauses(s):
    out, buf, d = [], '', 0
    for ch in s:
        if ch in '（(':
            d += 1
        elif ch in '）)':
            d = max(0, d - 1)
        if ch in '，；' and d == 0:
            out.append(buf)
            buf = ''
        else:
            buf += ch
    out.append(buf)
    return [x.strip() for x in out if x.strip()]


EN = re.compile(r'[A-Za-z]')
PRED = re.compile(r'作表语|放在 ?be ?(动词)?后|放在系动词后|放在名词后|放在后面|放在动词后')
ADVB = re.compile(r'作副词|作状语')
NOUNP = re.compile(r'作名词|单独作名词|名词短语|名词多写作|名词写作')


def clean_took(s):
    s = s.strip().strip('；。').strip()
    s = re.sub(r'^【[^】]+】', '', s)
    s = re.sub(r'^同 ([A-Za-z\-]+)，写法不同（(.*)）$', r'\2', s)
    out = []
    for c in _clauses(s):
        inner = re.findall(r'（((?:[^（）]|（[^（）]*）)*)）', c)
        hq0 = re.sub(r'“[^”]*”|（((?:[^（）]|（[^（）]*）)*)）', '', c).strip()
        if (re.search(r'复合形容词|复合定语|复合名词|复合词|连成形容词|连成一个(前置)?形容词|构成形容词|^连字符把|^名词表示|^见【', hq0)
                or re.fullmatch(r'(放在名词前|作定语|作前置定语|作定语时|放在名词前时|作定语，带连字符|带连字符|放在名词前当形容词用|连成一个词放在名词前|其余位置一般不加|(两词|两个词)直接(连写|合写)(，不加连字符)?|已连写成一个词|英式常连写|[A-Za-z\-]+ 作定语(时)?带连字符|(放在名词前|作定语)(作定语)?(时)?(才)?加|[A-Za-z]+ 不加 s)', hq0)
                or re.search(r'作前置定语时$|数量 . 时间名词 . old|连成(颜色)?形容词|整个放到名词前作定语时|多放在名词前作定语|^表示“被', hq0)
                or re.fullmatch(r'[“”]?(名词|副词|形容词|数词)( ?/ ?(名词|副词|形容词))? ?\+ ?(现在分词|过去分词|形容词|名词|动名词|动词-ing|-driven)[”]?', hq0)):
            for x in inner:
                x = x.strip()
                if x.startswith('同 '):
                    out.append(x)
                elif EN.search(x) and not re.search(r'[\u4e00-\u9fff]{4,}', re.sub(r'[A-Za-z].*', '', x)):
                    lst = re.fullmatch(r'[A-Za-z][^、]*(、[A-Za-z][^、]*)+', x)
                    out.append(('同 ' + x) if lst else x)
            m2 = re.search(r'(同 [A-Za-z][^（）]*)$', c)
            if m2 and m2.group(1) not in out:
                out.append(m2.group(1))
            continue
        en_inner = [x for x in inner if EN.search(x)]
        head = re.sub(r'（((?:[^（）]|（[^（）]*）)*)）', '', c).strip()
        if PRED.search(head) and ('不加' in head or '分写' in head or '拆开' in head or '分开' in head):
            ex = head.split('：', 1)[1].strip() if '：' in head else ''
            if not ex:
                ex = next((x for x in en_inner if not x.startswith('同')), '')
            if ex:
                be = re.search(r"\b(is|was|are|were|be|am)\b|'m\b|'s\b", ex)
                out.append(('放在 be 后面常分开写：' if be or '名词后' not in head else '放在名词后面就分开写：') + ex)
            for x in en_inner:
                if x.startswith('同'):
                    out.append(x)
            continue
        if re.match(r'^作(短语|名词短语|普通短语)(时)?(分开写|不加)', head):
            ex = head.split('：', 1)[1].strip() if '：' in head else (en_inner[0] if en_inner else '')
            if ex:
                out.append('当名词短语用时分开写：' + ex)
            continue
        if re.match(r'^作动词(时)?(常)?加连字符', head) and '：' in head:
            out.append('当动词用时常加连字符：' + head.split('：', 1)[1].strip())
            continue
        if re.match(r'^分开用就是名词短语', head):
            ex = en_inner[0] if en_inner else ''
            out.append('当名词时分开写：' + (ex or re.sub(r'^分开用就是名词短语\s*', '', head)))
            continue
        if ADVB.search(head) and ('不加' in head or '分写' in head or '分开' in head):
            ex = en_inner[0] if en_inner else (head.split('：', 1)[1].strip() if '：' in head else '')
            if ex:
                out.append('当副词用时常分开写：' + ex)
            continue
        if NOUNP.search(head) and ('不加' in head or '分写' in head or '两个词' in head or '写' in head) and '连字符' not in head.replace('不加连字符', ''):
            ex = en_inner[0] if en_inner else (head.split('：', 1)[1].strip() if '：' in head else re.sub(r'^.*?(写作|写成|写)\s*', '', head))
            ex = re.sub(r'（[^（）]*）', '', ex).strip()
            if ex and EN.search(ex):
                out.append('当名词时多分开写：' + ex)
            continue
        hq = re.sub(r'“[^”]*”', '', head)
        if '连字符' in hq and '：' in hq and EN.search(hq.split('：', 1)[1]):
            out.append(head.split('：', 1)[1].strip())
            continue
        if '连字符' in hq and not EN.search(hq.replace('-', '')):
            # 只是在讲“要加连字符”：留下括号里的例子
            for x in inner:
                x = x.strip()
                if EN.search(x):
                    lst = re.fullmatch(r'[A-Za-z][^、]*(、[A-Za-z][^、]*)+', x)
                    out.append(('同 ' + x) if lst and not x.startswith('同') else x)
            continue
        if re.match(r'^也(常|可以|可)?(连写|分写|分开写)?(作|写作|写成|写|连写作|连写成|分写成|分写作|成)?\s*[A-Za-z]', head):
            out.append(re.sub(r'^也(常|可以|可)?(连写|分写|分开写)?(作|写作|写成|写|连写作|连写成|分写成|分写作|成)?\s*', '也写作 ', c))
            continue
        out.append(c)
    s = '，'.join(out)
    return s.strip().strip('；。，').strip()


def default_body(t, rid):
    w = t['w']
    if rid == 'W03':
        return ex_or_word(w)
    if rid == 'W04':
        if w in PH:
            p = PH[w][0]
            pos = t['pos'][0] if t['pos'] else ''
            return '动词短语分开写：%s；%s %s' % (p, '名词' if pos == 'n.' else '形容词', w)
        return ''
    if rid == 'W06':
        m = re.match(r'^(e)-', w)
        if m:
            return 'e = electronic（电子的）'
        if w.startswith('AI-'):
            return 'AI = artificial intelligence（人工智能）'
        if w.startswith('VR-'):
            return 'VR = virtual reality（虚拟现实）'
        if re.match(r'^\d', w):
            return '数字和单词之间加连字符'
        return ''
    if rid == 'W16':
        return '名词多写作 %s' % w.replace('-', ' ')
    if rid == 'W18':
        return '按规范写作 %s' % (ex_of(w).replace(w, w.replace('-', ' ')) if ex_of(w) else w.replace('-', ' '))
    if rid == 'W10':
        return ex_or_word(w)
    if rid in ('W08',):
        return ''
    return ''


PFX_BODY = {
    'non': 'non- 英式常加连字符，美式多连写：%s / %s',
    'co': 'co- 英式常加连字符，美式多连写（%s）；后面是元音字母时尤其要加（co-author、co-operate）',
    'mid': 'mid- 后面是大写字母、数字时一定加（mid-January、mid-1990s）；别的英式多加，美式常连写（%s）',
    'semi': 'semi- 英式常加连字符，美式多连写：%s',
    'post': 'post- 和新的、临时的词连用时加连字符（post-movie 看完电影以后的）；用熟了的连写（postwar 也写 post-war）',
    'pre': 'pre- 一般连写（preview），新组合常加连字符；pre-order / preorder 两种写法都常见',
    'super': 'super- 一般连写（supermarket），表示“特别、超级”的临时组合常加连字符（super-excited）',
    'anti': 'anti- 一般连写（antibody），新组合、后面是元音或大写字母时常加连字符；anti-ageing 是英式拼法，美式写 anti-aging',
    'mini': 'mini- 一般连写（minibus），新的、临时的组合常加连字符（mini-doctor）',
    'multi': 'multi- 一般连写（multimedia），新组合常加连字符（multi-device）',
    'nano': 'nano- 用熟了的连写（nanotechnology），新组合常加连字符（nano-level research）',
    'neuro': 'neuro- 接辅音开头的词时一般连写（neuroscience），这里用连字符是为了让新词好认',
    'vice': 'vice-（副…）常加连字符：vice-president（美式也常分开写 vice president）',
    'near': 'near（几乎）和形容词连成“几乎…的”时加连字符：near-perfect、near-liquid',
    'off': 'off 和名词连成形容词时加连字符：an off-peak ticket；也可当副词：travel off-peak',
    'cross': 'cross- 和形容词、名词连用时多加连字符：cross-cultural、cross-border',
    'over': 'over- 一般连写（overload）；over-reliance 英式常加连字符，美式多连写 overreliance',
}
PFX_SPECIAL = {
    'non-VR': ('W13', '后面是大写字母，一定加连字符：non-VR（同 non-English）'),
    'mid-January': ('W13', '后面是大写字母，一定加连字符，月份照常大写：mid-January、mid-1990s；接普通词时多连写：midnight、midday'),
    'mid-thirties': ('W13', 'mid- 接年龄、年代常加连字符：in his mid-thirties；美式也写 midthirties'),
    'sci-fi': ('W02', 'science fiction 两个词各截一段（sci + fi），中间加连字符；同 hi-fi = high fidelity'),
    'good-bye': ('W02', 'God be with ye 缩成 good-bye，今天多连写成 goodbye：分开写、加连字符、连写，一步步走过来'),
    'easy-goingly': ('W03', '从 easy-going 加 -ly 变来，原来的连字符照留'),
    'easy-goingness': ('W03', '从 easy-going 加 -ness 变来，原来的连字符照留'),
    'peep-peep-peep': ('W14', '把鸟叫声 peep 原样重复三遍，中间加连字符'),
    'tuk-tuk': ('W14', '泰语里模仿发动机声音的叠词，中间加连字符'),
}


def body_for_prefix(w):
    if w in PFX_SPECIAL:
        return PFX_SPECIAL[w]
    if w.endswith('-like'):
        return ('W08', '-like 接常用短词多连写（catlike、childlike），接长词、l 结尾的词、新组合多加连字符（%s）' % w)
    p = w.split('-')[0].lower()
    tmpl = PFX_BODY.get(p, '')
    if '%s' in tmpl:
        if tmpl.count('%s') == 2:
            tmpl = tmpl % (w, w.replace('-', ''))
        else:
            tmpl = tmpl % w.replace('-', '')
    return ('W13', tmpl)


def spell_line(t, took):
    w = t['w']
    from pass2 import SPELL_MORE
    SPELLX.update(SPELL_MORE)
    if CATS[w] == 'PFX':
        rid, body = body_for_prefix(w)
        extra = [clean_took(x) for x in took]
        extra = [x for x in extra if x.startswith('也写作') and x.replace('也写作 ', '') not in body]
        if extra:
            body = body + '；' + '；'.join(dict.fromkeys(extra))
        return rid, '　写法：%s%s' % (TEXT[rid], '（%s）' % body if body else '')
    rid = spell_rule(t)
    body = None
    if w in SPELLX:
        v = SPELLX[w]
        if isinstance(v, tuple):
            rid, body = v
        else:
            body = v
    if body is None:
        parts_ = [clean_took(x) for x in took]
        parts_ = [x for x in parts_ if x]
        flat = []
        for x in parts_:
            flat += [y.strip() for y in re.split(r'[，；](?![^（）]*）)', x) if y.strip()]
        parts_ = flat
        d = default_body(t, rid)
        wl = w.lower()
        if rid in ('W03', 'W10') and any(wl in x.lower() for x in parts_):
            d = ''
        if rid == 'W16':
            op = w.replace('-', ' ').lower()
            parts_ = [x for x in parts_ if not (x.lower().endswith(op) and re.match(r'^(也写作|当名词时多分开写：|今天多写成两个词|一般写作两个词)', x))]
        parts_ = [x for x in parts_ if not re.fullmatch(r'(两词|两个词)直接(连写|合写)(，不加连字符)?|已连写成一个词（同 [^）]*）|连成一个词放在名词前|放在名词前当形容词用|[A-Za-z]+ 不加 s|作定语', x)]
        if CATS[w] == 'H09':
            d, parts_ = '小词放在前面的这类合成词都连写（同 income、outcome）', []
        seen = []
        for x in ([d] if d else []) + parts_:
            if x and not any(x in y for y in seen):
                seen = [y for y in seen if y not in x]
                seen.append(x)
        body = '；'.join(seen)
    return rid, '　写法：%s%s' % (TEXT[rid], '（%s）' % body if body else '')

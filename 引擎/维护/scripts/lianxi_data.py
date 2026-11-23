# -*- coding: utf-8 -*-
"""第 122、123 条：练习题（「题目1」–「题目5」五列）和答案（「答案」列：答案 + 讲解，讲解就是每道题的 why）的原稿，一个词 5 道，第 1 道是听力。
选择题的 opts 第一个写正确答案，lianxi.py 按单词和题号把它挪到 A–D 里的某一个（每次一样，不会都是 A）。
出题要求（用户：“答案不一定是这个词，但是跟这个有关系，或者这个能决定答案”）：
  本词多半出现在题干里，由它决定答案（词性、可数不可数、搭配、三单、不规则变化、易混词）；5 道里答案就是本词原形的最多 1 道。
  听力念一个含本词的短句，问句子说了什么。句子 12 个词以内、初中词汇、答案唯一。kd 写考的是哪一条考点（总表「考点」列的标签）。
L(听的句子, 问题, [对的, 错的…], 解析)            听力（选项多是中文）
C(题型, 要求, 题干, [对的, 错的…], 解析, kd)     选择
F(题型, 要求, 题干, 答案, 解析, kd, zh=中文)     填空、改错、句型转换（答案几个空用“；”隔开；题干“\\n”另起一行）
"""
def L(listen, ask, opts, why):
    return dict(type='听力', ask='听录音，回答问题：' + ask, listen=listen, opts=opts, why=why)
def C(t, ask, stem, opts, why, kd=''):
    return dict(type=t, ask=ask, stem=stem, opts=opts, why=why, kd=kd)
def F(t, ask, stem, ans, why, kd='', zh=''):
    return dict(type=t, ask=ask, stem=stem, ans=ans, why=why, kd=kd, zh=zh)

DX = '选出最恰当的一项。'
SX = '用所给单词的适当形式填空。'
WC = '根据中文完成句子，每空一词。'
GC = '句子里有一处错误，找出来并改正。'
def XC(*ws): return '从 ' + '、'.join(ws) + ' 中选一个，用适当形式填空。'

Q = {}
Q['camera'] = [
 L('Lily wants to buy a new camera to take photos on her trip.', 'Lily 想买什么？', ['一台新相机', '一部新手机', '一个新背包', '一张旅行地图'], 'camera 是“照相机”，to take photos（拍照）也说明是相机。'),
 C('单项选择', DX, 'My uncle has two ______. One is for photos, and the other is for videos.', ['cameras', 'camera', "camera's", 'cameraes'], 'two 后面用复数；camera 直接加 s：cameras。'),
 F('选词填空', XC('photo', 'camera', 'video'), 'I took many ______ of the Bund with my new camera.', 'photos', '用相机拍下来的“照片”是 photo，many 后面用复数 photos；camera 是拍照的机器。'),
 F('完成句子', WC, 'He ______ his camera ______ the taxi.', 'left；in', '“把…落在某处”用 leave sth. in…，过去式 left。', zh='他把相机落在出租车里了。'),
 C('单项选择', DX, "—Whose camera is this?\n—It's ______. I bought it last week.", ['mine', 'my', 'me', 'I'], '后面没有名词，用名词性物主代词 mine（= my camera）。'),
]
Q['speaker'] = [
 L("Mr. Brown is the speaker at today's school meeting.", 'Mr. Brown 在今天的学校会议上是什么人？', ['演讲的人', '主持人', '听众', '摄影师'], 'speaker 是 speak 加 -er：“说话的人、演讲人”。'),
 F('改错', GC, 'The two speaker spoke very clearly at the meeting.', 'speaker → speakers', '“演讲人”可数，two 后面用复数 speakers。', '词性转换'),
 C('单项选择', DX, 'English ______ all over the world. Many people are English ______.', ['is spoken; speakers', 'speaks; speakers', 'is spoken; speaker', 'is speaking; speaks'], '英语“被说”用被动 is spoken；people 是复数，用 speakers（说英语的人）。', '词性转换'),
 F('选词填空', XC('speaker', 'speech', 'speak'), 'She gave a wonderful ______ about saving water.', 'speech', 'give a speech 做演讲，speech 是“演讲”；speaker 是做演讲的人。', '词性转换'),
 C('单项选择', DX, 'Turn down the ______, please. The music is too loud.', ['speaker', 'speech', 'speaking', 'spoken'], 'speaker 还是“扬声器、音箱”：声音太大，把音箱调小。'),
]
Q['thermostat'] = [
 L('The room is too cold. Please turn up the thermostat.', '说话人想让对方做什么？', ['把温度调高', '关上窗户', '打开灯', '关掉音乐'], 'thermostat 是“温控器”，turn up the thermostat 就是把温度调高。'),
 C('单项选择', DX, 'A thermostat helps us ______ the temperature of a room.', ['control', 'controls', 'controlling', 'controlled'], 'help sb. do sth.，后面用动词原形 control。'),
 F('选词填空', XC('thermometer', 'thermostat'), 'The nurse used a ______ to take my temperature.', 'thermometer', '量体温用 thermometer（温度计）；thermostat 是控制温度的温控器。'),
 F('完成句子', WC, 'When it is cold, we ______ the thermostat ______ 22 degrees.', 'set；to', '“把…调到…”用 set … to …。', zh='天冷的时候，我们把温控器调到 22 度。'),
 C('单项选择', DX, 'In "thermostat", "thermo" means ______.', ['热', '光', '声音', '水'], 'thermo 是“热”（thermometer 温度计），stat 是“使保持不变”：让温度保持不变的东西。'),
]
Q['itself'] = [
 L("The baby cat can't wash itself yet.", '小猫还不能做什么？', ['自己洗澡', '自己吃饭', '自己走路', '自己睡觉'], 'wash itself 是“给自己洗”，itself 指小猫自己。'),
 C('单项选择', DX, "The dog is wagging ______ tail. ______ very happy.", ["its; It's", "it's; Its", 'its; Its', "it's; It's"], "its 是“它的”；it's = it is。", '变形'),
 F('适当形式填空', SX, 'The children enjoyed ______ at the party. (they)', 'themselves', '主语是 the children，“玩得开心”enjoy oneself，复数用 themselves。', '变形'),
 C('单项选择', DX, 'The door opened by ______. Nobody touched it.', ['itself', 'herself', 'it', 'its'], 'by itself 自动地；门是物，用 itself。', '用法'),
 F('改错', GC, 'The robot can clean itself room every day.', 'itself → its', 'room 前面要“它的”，用物主代词 its；itself 是“它自己”，不能放在名词前。', '变形'),
]
Q['alarm'] = [
 L('The fire alarm rang, so all the students left the building quickly.', '学生们为什么很快离开大楼？', ['火警警报响了', '下课铃响了', '下雨了', '老师叫他们'], 'fire alarm 是“火警警报”。'),
 C('单项选择', DX, "My alarm didn't ______ this morning, so I was late.", ['go off', 'go on', 'go out', 'go away'], '闹钟、警报“响”用 go off。'),
 F('选词填空', XC('alarm', 'alarming', 'alarmed'), 'The number of wild animals is going down at an ______ speed.', 'alarming', '修饰“速度”（物）用 -ing 形容词：alarming 令人担忧的。'),
 F('完成句子', WC, 'She was ______ ______ hear the news.', 'alarmed；to', '“感到惊慌”用 -ed 形容词：be alarmed to do sth.。', zh='听到这个消息，她很惊慌。'),
 C('单项选择', DX, 'Please ______ the alarm for six o\'clock.', ['set', 'sit', 'put', 'take'], '“定闹钟”用 set the alarm for…。'),
]
Q['stranger'] = [
 L("Don't open the door to a stranger when you are at home alone.", '独自在家时，不要给谁开门？', ['陌生人', '邻居', '父母', '老师'], 'stranger 是“陌生人”，strange（陌生的）加 r。'),
 C('单项选择', DX, 'That story is strange, but this one is even ______.', ['stranger', 'strange', 'strangest', 'more strange'], 'even 加比较级；strange 以 e 结尾，加 r：stranger。这里是“更奇怪的”，不是“陌生人”。', '词性转换'),
 F('适当形式填空', SX, 'Everything looks ______ to me in the new city. (stranger)', 'strange', 'look 是系动词，后面用形容词 strange（陌生的）。', '词性转换'),
 F('改错', GC, 'There are two stranger at the school gate.', 'stranger → strangers', '“陌生人”可数，two 后面用复数 strangers。', '词性转换'),
 C('单项选择', DX, 'The man looked at me ______. I felt a little afraid.', ['strangely', 'strange', 'stranger', 'strangers'], '修饰动词 looked at 用副词 strangely。'),
]
Q['lock'] = [
 L('Remember to lock the door before you go out.', '出门前要记得做什么？', ['锁门', '关灯', '带钥匙', '关窗'], 'lock the door 是“锁门”。'),
 C('单项选择', DX, "I can't open the box. It's ______.", ['locked', 'lock', 'locking', 'to lock'], '箱子“被锁着”，用过去分词 locked 作表语。'),
 F('选词填空', XC('lock', 'key'), "I lost my ______, so I couldn't open the lock.", 'key', '开锁用的是 key（钥匙）；lock 是锁。'),
 F('完成句子', WC, 'He ______ ______ lock his car last night.', 'forgot；to', '忘了要做的事用 forget to do，过去式 forgot。', zh='他昨晚忘了锁车。'),
 F('适当形式填空', SX, 'The school gate ______ (lock) at ten every night.', 'is locked', '大门“被锁上”，每晚都这样：一般现在时的被动 is locked。'),
]
Q['explore'] = [
 L('Many young people want to explore the deep sea in the future.', '很多年轻人将来想做什么？', ['探索深海', '去海边游泳', '保护海洋', '当渔民'], 'explore 是“探索”，the deep sea 是深海。'),
 F('适当形式填空', SX, 'The ______ found a new island in 1820. (explore)', 'explorer', 'the 后面要名词，“探险者”是 explore 去 e 加 er：explorer。'),
 C('单项选择', DX, "It's interesting ______ the old town on foot.", ['to explore', 'explore', 'explored', 'explores'], "It's + 形容词 + to do，真正的主语是 to explore。"),
 F('选词填空', XC('explore', 'express', 'expect'), 'We ______ to see you at the party next week.', 'expect', 'expect to do 期待做某事；explore 是探索。'),
 F('完成句子', WC, 'They ______ three days ______ the forest.', 'spent；exploring', 'spend 时间 doing sth.，过去式 spent。', zh='他们花了三天时间探索那片森林。'),
]
Q['rock'] = [
 L('Be careful! The rocks near the river are very wet.', '说话人提醒注意什么？', ['河边的石头很湿滑', '河水很深', '天要下雨', '河里鱼很多'], 'rocks 是“岩石、石头”，very wet 很湿。'),
 C('单项选择', DX, 'There are many ______ on the beach.', ['rocks', 'rock', 'a rock', 'rockes'], 'many 后面接可数名词复数，rock 直接加 s。'),
 F('选词填空', XC('rock', 'stone', 'sand'), 'The children built a castle with ______ on the beach.', 'sand', '在沙滩上堆城堡用 sand（沙子，不可数）。'),
 C('单项选择', DX, 'My brother likes ______ rock music.', ['listening to', 'listen', 'hearing to', 'listens to'], 'like doing；“听音乐”是 listen to music。'),
 F('完成句子', WC, 'The rock ______ ______ an elephant.', 'looks；like', '“看起来像…”用 look like，主语单数用 looks。', zh='那块岩石看起来像一头大象。'),
]
Q['shower'] = [
 L('I usually take a shower after running in the morning.', '说话人早上跑步后通常做什么？', ['洗个淋浴', '吃早饭', '睡觉', '看书'], 'take a shower 是“洗淋浴”。'),
 C('单项选择', DX, 'The weather report says there will be ______ this afternoon.', ['showers', 'shower', 'a showers', 'showering'], '“阵雨”常用复数 showers。'),
 F('完成句子', WC, 'I ______ ______ a shower when the phone rang.', 'was；taking', '一个动作正在进行时另一个动作发生：过去进行时 was taking。', zh='电话响的时候，我正在洗澡。'),
 F('选词填空', XC('shower', 'bath', 'bathroom'), 'There is a big ______ with a shower in the new house.', 'bathroom', '装着淋浴的房间是 bathroom（浴室）。'),
 C('单项选择', DX, 'There was a short shower ______ the afternoon.', ['in', 'on', 'at', 'for'], '在下午用 in the afternoon。'),
]
Q['mode'] = [
 L('Please turn your phone to silent mode during the film.', '看电影时要怎么做？', ['把手机调成静音模式', '关掉手机', '给手机充电', '用手机拍照'], 'silent mode 是“静音模式”，mode 是模式、方式。'),
 C('单项选择', DX, 'Walking and cycling are green ______ of transport.', ['modes', 'mode', 'model', 'models'], 'mode of transport 交通方式；主语是两种，用复数 modes。'),
 F('选词填空', XC('mode', 'model', 'mood'), 'He is in a good ______ today because he won the game.', 'mood', '心情是 mood；mode 是方式、模式；model 是模型、模特。'),
 F('适当形式填空', SX, 'The subway is the ______ mode of transport in our city. (fast)', 'fastest', 'the 后面用最高级 fastest。'),
 C('单项选择', DX, 'Which mode of transport is ______, the bus or the bike?', ['cheaper', 'cheap', 'cheapest', 'the cheapest'], '两者比较用比较级 cheaper。'),
]
Q['text message'] = [
 L("I'll send you a text message when I get to the station.", '说话人到车站后会做什么？', ['发短信', '打电话', '写信', '发邮件'], 'send a text message 是“发短信”。'),
 C('单项选择', DX, 'I got three ______ from my mom this morning.', ['text messages', 'text message', 'texts message', 'texts messages'], '复数只在后面的名词上加 s：text messages。'),
 F('完成句子', WC, "Don't forget ______ ______ me a text message.", 'to；send', '别忘了要做的事：forget to do sth.。', zh='别忘了给我发短信。'),
 F('选词填空', XC('message', 'massage', 'passage'), 'Please read the ______ and answer the questions.', 'passage', '阅读的“短文”是 passage；message 是消息、短信。'),
 C('单项选择', DX, "It's not polite ______ text messages in class.", ['to send', 'send', 'sending', 'sent'], "It's not polite to do sth. 做某事不礼貌。"),
]
Q['bedroom'] = [
 L("My bedroom is small, but it's clean and tidy.", '说话人的卧室怎么样？', ['小，但干净整齐', '大而整洁', '小而乱', '大但很乱'], 'small 小，clean and tidy 干净整齐。'),
 C('单项选择', DX, 'The house has three ______.', ['bedrooms', 'bedroom', 'bedroomes', 'beds room'], 'three 后面用复数 bedrooms。'),
 F('选词填空', XC('bedroom', 'kitchen', 'living room'), 'Mum is cooking dinner in the ______.', 'kitchen', '做饭在 kitchen（厨房）；bedroom 是卧室。'),
 F('完成句子', WC, 'My bedroom is ______ the ______ floor.', 'on；second', '“在几楼”用 on the … floor，“二楼”用序数词 second。', zh='我的卧室在二楼。'),
 C('单项选择', DX, 'There ______ a bed, a desk and two chairs in my bedroom.', ['is', 'are', 'be', 'have'], 'there be 就近原则：紧挨着的 a bed 是单数，用 is。'),
]
Q['bathroom'] = [
 L('Excuse me, where is the bathroom?', '说话人在找什么地方？', ['卫生间', '卧室', '厨房', '教室'], 'bathroom 在美国英语里也指“卫生间”。'),
 C('单项选择', DX, '—May I use your bathroom?\n—______ It\'s over there.', ['Of course.', "No, you can't.", "I don't know.", "That's right."], '对方借用卫生间，答应用 Of course.。'),
 F('选词填空', XC('bath', 'bathe', 'bathroom'), 'The baby is having a ______ in the bathroom.', 'bath', 'have a bath 洗澡，bath 是名词；bathroom 是浴室。'),
 F('完成句子', WC, 'The bathroom is ______ ______ the bedroom.', 'next；to', '“在…旁边”用 next to。', zh='浴室在卧室旁边。'),
 F('适当形式填空', SX, 'Our new flat has two ______. (bathroom)', 'bathrooms', 'two 后面用复数 bathrooms。'),
]
Q['suggest'] = [
 L('My teacher suggested reading English books every day.', '老师建议做什么？', ['每天读英语书', '每天写日记', '每天看电影', '每天跑步'], 'suggest doing sth. 建议做某事。'),
 C('单项选择', DX, 'My doctor suggests ______ more vegetables.', ['eating', 'eat', 'to eat', 'eats'], 'suggest doing sth.，不说 suggest to do。', '用法'),
 F('适当形式填空', SX, 'Thanks for your ______. They are very helpful. (suggest)', 'suggestions', 'your 后面要名词；They are 说明是复数：suggestions。', '词性转换'),
 F('完成句子', WC, 'He suggested that we ______ ______ off early.', 'should；set', 'suggest that sb. (should) do sth.。', '用法', zh='他建议我们早点出发。'),
 F('改错', GC, 'Mom suggested me to go to bed early.', 'suggested me to go → suggested that I (should) go', 'suggest 不接“sb. to do”，要说 suggest that sb. (should) do。', '用法'),
]
Q['protect'] = [
 L('We should protect the wild animals in the forest.', '我们应该保护什么？', ['森林里的野生动物', '河里的鱼', '城市里的树', '农场的动物'], 'protect 保护，wild animals 野生动物。'),
 C('单项选择', DX, 'Sunglasses can protect your eyes ______ the strong sunlight.', ['from', 'with', 'by', 'to'], 'protect … from … 保护…免受…。', '用法'),
 F('适当形式填空', SX, 'The workers wear hard hats for ______. (protect)', 'protection', 'for 后面要名词：protection 保护。'),
 F('选词填空', XC('protect', 'provide', 'produce'), 'Our school ______ free lunch for the students.', 'provides', '“提供”是 provide，主语三单加 s；protect 是保护。'),
 F('完成句子', WC, 'We must ______ the earth ______ pollution.', 'protect；from', 'protect … from … 保护…免受…。', '用法', zh='我们必须保护地球免受污染。'),
]
Q['review'] = [
 L("Let's review the new words before the test.", '考试前要做什么？', ['复习新单词', '预习新课', '写作文', '读课文'], 'review 是“复习”，re- 再、view 看。'),
 C('单项选择', DX, "You'd better ______ your notes every day.", ['review', 'to review', 'reviewing', 'reviewed'], "had better do sth.，后面用原形。"),
 F('选词填空', XC('review', 'preview', 'view'), 'Before the new lesson, we ______ it at home.', 'preview', '上新课之前先看叫“预习”preview；学过之后再看叫“复习”review。'),
 F('完成句子', WC, 'He is busy ______ his ______ for the exam.', 'reviewing；lessons', 'be busy doing sth. 忙于做某事。', zh='他正忙着复习功课准备考试。'),
 C('单项选择', DX, 'The new film got good ______ in the newspapers.', ['reviews', 'review', 'reviewer', 'viewing'], 'review 还是“评论”，可数，good reviews 好评。'),
]
Q['heating'] = [
 L("It's cold outside, but our classroom is warm because of the heating.", '教室为什么暖和？', ['开了暖气', '关了窗', '人很多', '出太阳了'], 'heating 是“暖气”。'),
 C('单项选择', DX, 'The heating ______ broken. We need someone to fix it.', ['is', 'are', 'were', 'be'], 'heating 不可数，谓语用单数 is。'),
 F('适当形式填空', SX, 'The sun ______ the earth every day. (heat)', 'heats', '一般现在时，主语三单，heat 加 s。'),
 F('选词填空', XC('heat', 'hot', 'heating'), "It's too ______ today. Let's go swimming.", 'hot', 'too 后面用形容词 hot；heat 是“热量”或“加热”，heating 是暖气。'),
 F('完成句子', WC, 'Please ______ ______ the heating.', 'turn；on', '“打开（电器、暖气）”用 turn on。', zh='请把暖气打开。'),
]
Q['guide'] = [
 L('Our tour guide told us many interesting stories about the old town.', '谁给大家讲了古镇的故事？', ['导游', '老师', '司机', '当地农民'], 'tour guide 是“导游”。'),
 C('单项选择', DX, 'The old man ______ us to the station yesterday.', ['guided', 'guide', 'guides', 'guiding'], 'yesterday 用过去式；guide 以 e 结尾，加 d。'),
 F('完成句子', WC, 'She wants to ______ ______ tour guide in the future.', 'be；a', 'want to be a … 想成为…；guide 前面用 a。', '短语', zh='她将来想当一名导游。'),
 F('选词填空', XC('guide', 'guess', 'guard'), 'Can you ______ who is coming?', 'guess', '“猜”是 guess；guide 是引导、导游。'),
 C('单项选择', DX, 'This book is a useful ______ for travellers.', ['guide', 'guided', 'guiding', 'guides'], 'a useful 后面要单数名词：guide 指南、手册。'),
]
Q['personal'] = [
 L("Please don't read my diary. It's personal.", '说话人为什么不让别人看日记？', ['日记是私人的东西', '写得不好', '还没写完', '是英文写的'], 'personal 是“个人的、私人的”。'),
 F('适当形式填空', SX, 'Every ______ has his or her own dream. (personal)', 'person', 'every 后面要单数名词：person 人。', '词性转换'),
 C('单项选择', DX, 'It\'s not polite to ask ______ questions like "How old are you?"', ['personal', 'person', 'personally', 'persons'], '修饰名词 questions 用形容词 personal（私人的）。', '词性转换'),
 F('选词填空', XC('personal', 'person', 'personally'), "______, I think it's a good idea.", 'Personally', '放在句首说“就我个人而言”，用副词 personally。', '词性转换'),
 F('完成句子', WC, 'The famous actor came to our school ______ ______.', 'in；person', 'in person 亲自。', '词性转换', zh='这位著名演员亲自来到了我们学校。'),
]
Q['owner'] = [
 L('The owner of the restaurant is a kind old man.', '饭店的主人是什么样的人？', ['一位善良的老人', '一位年轻女士', '一位严厉的厨师', '一位外国人'], 'owner 是“主人、所有者”。'),
 F('适当形式填空', SX, 'My uncle ______ a small shop in Shanghai. (owner)', 'owns', '这里要动词“拥有”own，主语三单加 s。', '词性转换'),
 C('单项选择', DX, 'Is this your ______ bike, or did you borrow it?', ['own', 'owner', 'owns', 'owned'], "one's own 自己的；owner 是名词“主人”。", '词性转换'),
 F('完成句子', WC, 'Where is the ______ ______ the dog?', 'owner；of', '“…的主人”用 the owner of …。', zh='这只狗的主人在哪儿？'),
 F('选词填空', XC('owner', 'worker', 'visitor'), 'Many ______ came to see the famous painting in the museum.', 'visitors', '来博物馆参观的人是 visitor，many 后面用复数；owner 是主人。'),
]
Q['alarm clock'] = [
 L('My alarm clock rings at six thirty every morning.', '闹钟每天早上几点响？', ['6:30', '6:00', '7:00', '7:30'], 'six thirty 是 6:30。'),
 C('单项选择', DX, 'I forgot ______ my alarm clock, so I got up late.', ['to set', 'set', 'setting', 'sets'], 'forget to do 忘了要做的事（没做）。'),
 C('单项选择', DX, 'There are two ______ on my desk.', ['alarm clocks', 'alarm clock', 'alarms clock', 'alarms clocks'], '复数只在后面的名词上加 s：alarm clocks。'),
 F('完成句子', WC, "The alarm clock ______ ______, but I didn't get up.", 'went；off', '闹钟“响”用 go off，过去式 went off。', zh='闹钟响了，但我没有起床。'),
 F('选词填空', XC('clock', 'watch'), 'I wear a ______ on my wrist to know the time.', 'watch', '戴在手腕上的是 watch（手表）；clock 是挂钟、座钟。'),
]
Q['keep track of'] = [
 L('This app helps me keep track of how much water I drink every day.', '这个应用帮说话人记录什么？', ['每天喝多少水', '每天走多少路', '每天睡多久', '每天花多少钱'], 'keep track of 是“记录、掌握…的情况”。'),
 C('单项选择', DX, "It's hard to keep track ______ all the homework.", ['of', 'on', 'with', 'for'], '固定短语 keep track of。'),
 F('完成句子', WC, 'He uses a notebook ______ ______ track of his money.', 'to；keep', '用某物来做某事：use sth. to do sth.。', zh='他用一个笔记本记录自己的花销。'),
 C('单项选择', DX, 'Your mom keeps track of your study, ______?', ["doesn't she", 'does she', "isn't she", 'is she'], '反意疑问句前肯后否；keeps 是实义动词三单，用 doesn\'t she。'),
 F('选词填空', XC('keep track of', 'lose track of'), 'I was reading so happily that I ______ the time.', 'lost track of', 'lose track of 不知道…的情况（忘了时间）；keep track of 是一直掌握着。'),
]
Q['schedule'] = [
 L('According to the schedule, the train leaves at nine fifteen.', '火车几点出发？', ['9:15', '9:05', '9:50', '10:15'], 'schedule 是“时刻表”，nine fifteen 是 9:15。'),
 C('单项选择', DX, 'The meeting ______ for next Monday.', ['is scheduled', 'schedules', 'scheduled', 'is scheduling'], '会议“被安排”，用被动 is scheduled。'),
 F('完成句子', WC, 'We finished the work ______ ______.', 'on；schedule', 'on schedule 按计划、按时。', zh='我们按计划完成了这项工作。'),
 C('单项选择', DX, 'My schedule is full. I have no time ______ TV.', ['to watch', 'watch', 'watching', 'watched'], 'have time to do sth. 有时间做某事。'),
 F('改错', GC, 'The bus is behind schedule. It will arrive early.', 'early → late', 'behind schedule 晚于计划、晚点，所以会晚到 late。'),
]
Q['health care'] = [
 L('Good health care is important for old people.', '什么对老年人很重要？', ['好的医疗保健', '好的饮食', '好的住房', '好的朋友'], 'health care 是“医疗保健”。'),
 C('单项选择', DX, 'Health care ______ more and more important now.', ['becomes', 'become', 'are becoming', 'have become'], 'health care 不可数，谓语用单数 becomes。'),
 F('适当形式填空', SX, 'Eating more fruit is good for your ______. (healthy)', 'health', 'your 后面用名词 health（健康）。'),
 F('选词填空', XC('health', 'healthy', 'healthily'), 'We should eat ______ and exercise more.', 'healthily', '修饰动词 eat 用副词 healthily。'),
 F('完成句子', WC, 'It is important to ______ good ______ of yourself.', 'take；care', 'take good care of 好好照顾。', zh='好好照顾自己很重要。'),
]
Q['order'] = [
 L("Can I take your order now?", '这句话最可能在哪里听到？', ['餐馆', '医院', '图书馆', '学校'], 'take your order 是服务员问“可以点菜了吗”。'),
 C('单项选择', DX, 'The teacher ordered the boys ______ in the classroom.', ['not to run', 'not run', "don't run", 'no running'], 'order sb. (not) to do sth. 命令某人（不要）做某事。', '用法'),
 F('句型转换', '保持句意不变，每空一词。', 'He got up early in order to catch the bus.\nHe got up early ______ ______ he could catch the bus.', 'so；that', 'in order to do = so that + 从句，都表示“为了”。', '用法'),
 F('选词填空', XC('order', 'other', 'over'), 'Put the words in the right ______ to make a sentence.', 'order', 'in the right order 按正确的顺序。'),
 F('改错', GC, 'The lift is out of the order. Please take the stairs.', 'out of the order → out of order', 'out of order 坏了、出故障，中间没有 the。'),
]
Q['signal'] = [
 L("I can't hear you clearly. The signal here is bad.", '说话人为什么听不清？', ['这里信号不好', '周围太吵', '手机没电了', '对方声音太小'], 'signal 是“信号”。'),
 C('单项选择', DX, "A red light is a signal ______ stop.", ['to', 'for', 'of', 'at'], 'a signal to do sth. 做某事的信号。'),
 F('选词填空', XC('signal', 'sign', 'sigh'), 'There is a "No Smoking" ______ on the wall.', 'sign', '墙上写字的牌子是 sign（标志）；signal 是信号。'),
 F('完成句子', WC, 'The phone signal is very ______ ______ the subway.', 'weak；in', '“弱的”用 weak；在地铁里 in the subway。', zh='地铁里手机信号很弱。'),
 C('单项选择', DX, 'The policeman gave a signal, and the cars stopped ______.', ['quickly', 'quick', 'quicker', 'quickest'], '修饰动词 stopped 用副词 quickly。'),
]
Q['sense'] = [
 L("Dogs have a good sense of smell. They can find things people can't.", '狗的哪种感觉很好？', ['嗅觉', '视觉', '听觉', '味觉'], 'sense of smell 是“嗅觉”。'),
 C('单项选择', DX, 'My father has a good sense ______ humour.', ['of', 'for', 'in', 'with'], 'a sense of humour 幽默感。'),
 F('改错', GC, 'What you said makes no senses.', 'senses → sense', 'make sense 讲得通，这里 sense 不加 s。'),
 C('单项选择', DX, 'Our five senses are seeing, hearing, smelling, tasting and ______.', ['touching', 'touch', 'touched', 'to touch'], '并列的几样用同样的形式，都是 -ing。'),
 C('单项选择', DX, 'I could sense that she ______ worried.', ['was', 'is', 'be', 'were'], '主句是过去时 could sense，宾语从句也用过去时 was。'),
]
Q['manage'] = [
 L('The test was hard, but Tom managed to finish it on time.', 'Tom 最后怎么样？', ['按时做完了', '没做完', '迟到了', '没及格'], 'manage to do 设法做成了。'),
 C('单项选择', DX, 'We managed ______ the top of the mountain at last.', ['to reach', 'reach', 'reaching', 'reached'], 'manage to do sth. 设法做成某事。', '用法'),
 F('适当形式填空', SX, 'Mr. Wang is the ______ of this hotel. (manage)', 'manager', 'the 后面要名词“经理”：manage 加 r，manager。', '词性转换'),
 F('选词填空', XC('manage', 'try'), 'It was difficult, but he ______ to find the way home.', 'managed', '“成功做到了”用 manage to do；try to do 只是努力去做，不一定成功。', '用法'),
 F('改错', GC, 'She managed passing the exam.', 'passing → to pass', 'manage to do sth.，不接 doing。', '用法'),
]
Q['remind'] = [
 L('Please remind me to buy some milk on the way home.', '说话人让对方提醒自己做什么？', ['买牛奶', '早点回家', '买面包', '打电话'], 'remind sb. to do sth. 提醒某人做某事。'),
 C('单项选择', DX, 'This photo reminds me ______ my happy childhood.', ['of', 'for', 'with', 'at'], 'remind sb. of sth. 使某人想起某事。', '用法'),
 C('单项选择', DX, "—Don't forget to close the windows.\n—Thanks for ______ me.", ['reminding', 'remembering', 'remind', 'remember'], '是你提醒了我：remind，for 后面用 doing；remember 是自己记得。', '易混'),
 F('完成句子', WC, "I'll ______ ______ call you back.", 'remember；to', '自己记得要去做：remember to do。', '易混', zh='我会记得给你回电话的。'),
 F('改错', GC, 'Mom reminded me take an umbrella.', 'take → to take', 'remind sb. to do sth.。', '用法'),
]
Q['produce'] = [
 L('This farm produces fresh milk and eggs every day.', '这个农场每天出产什么？', ['牛奶和鸡蛋', '水果和蔬菜', '牛奶和蔬菜', '汽车和玩具'], 'produces 是“出产、生产”，后面跟的 fresh milk and eggs 就是农场出产的东西。'),
 C('单项选择', DX, 'Fresh ______ like carrots and apples ______ sold at the market.', ['produce; is', 'produce; are', 'products; is', 'product; are'], '蔬菜、水果是 produce（农产品），不可数，谓语用单数 is。', '词性转换'),
 F('改错', GC, 'Many new product are shown at the fair.', 'product → products', 'product（产品）可数，前面有 many，要用复数 products。', '词性转换'),
 F('选词填空', XC('produce', 'provide', 'protect'), 'The sun ______ us with light and heat.', 'provides', 'provide sb. with sth. 给某人提供某物；produce 是“生产、产生”，不这样用。'),
 F('句型转换', '改为一般疑问句，每空一词。', 'This factory produces toys.\n______ this factory ______ toys?', 'Does；produce', 'produces 是三单，一般疑问句借助 does，后面的动词还原成 produce。'),
]
Q['store'] = [
 L('We store our winter clothes in the big box under the bed.', '冬天的衣服放在哪里？', ['床下的大箱子里', '衣柜里', '门后面', '楼上'], 'store 是“储存、存放”。'),
 C('单项选择', DX, 'Food should be ______ in a cool place.', ['stored', 'store', 'storing', 'to store'], '食物“被存放”，should be + 过去分词 stored。'),
 F('选词填空', XC('store', 'storm', 'story'), 'A big ______ is coming. Stay at home.', 'storm', '“暴风雨”是 storm；store 是商店、储存。'),
 F('完成句子', WC, "I'm going ______ the ______ to buy some fruit.", 'to；store', 'go to the store 去商店（美国英语）。', zh='我要去商店买些水果。'),
 F('适当形式填空', SX, 'There are many big ______ on Nanjing Road. (store)', 'stores', 'many 后面用复数 stores。'),
]
Q['sore'] = [
 L("I have a sore throat, so I can't sing today.", '说话人今天为什么不能唱歌？', ['嗓子疼', '头疼', '太累了', '不会唱'], 'sore throat 是“嗓子疼”。'),
 C('单项选择', DX, "—What's the matter?\n—My legs are ______ after the long walk.", ['sore', 'sorry', 'sour', 'soft'], 'sore 酸痛的；sorry 抱歉的，sour 酸的（味道），soft 软的。'),
 F('选词填空', XC('sore', 'sorry', 'sorrow'), "I'm ______ to hear that you are ill.", 'sorry', '“听到…很难过”用 be sorry to hear；sore 是身体疼。'),
 F('完成句子', WC, 'I ______ ______ a sore throat for two days.', 'have；had', 'for two days 一段时间，用现在完成时 have had。', zh='我嗓子已经疼了两天了。'),
 F('改错', GC, 'She has a sore eyes.', 'a sore eyes → sore eyes', 'eyes 是复数，前面不用 a。'),
]
Q['throat'] = [
 L('The doctor looked at my throat and said I had a cold.', '医生检查了说话人的哪里？', ['喉咙', '眼睛', '耳朵', '牙齿'], 'throat 是“喉咙”。'),
 C('单项选择', DX, "The singer has a sore throat. She ______ sing tonight.", ["can't", 'can', 'must', 'need'], '嗓子疼，所以不能唱：can\'t。'),
 F('选词填空', XC('throat', 'throw', 'through'), 'The train went ______ the tunnel.', 'through', '“穿过”隧道用 through；throat 是喉咙，throw 是扔。'),
 F('完成句子', WC, "What's ______ ______ your throat?", 'wrong；with', '“…怎么了”用 What\'s wrong with …?。', zh='你的喉咙怎么了？'),
 C('单项选择', DX, 'You should ______ some medicine for your sore throat.', ['take', 'eat', 'drink', 'make'], '“吃药”用 take medicine。'),
]
Q['understand'] = [
 L("Sorry, I don't understand. Could you say it again, please?", '说话人请对方做什么？', ['再说一遍', '说慢一点', '写下来', '大声一点'], "I don't understand 我没听懂，所以请对方再说一遍（say it again）。"),
 F('适当形式填空', SX, 'The story is easy. It can ______ by children. (understand)', 'be understood', '故事“被理解”：can be + 过去分词，understand 的过去分词是不规则的 understood。', '变形'),
 C('单项选择', DX, '—Have you ______ the rules of the game?\n—Yes, I have.', ['understood', 'understand', 'understanding', 'understands'], 'have + 过去分词，understand 的过去分词是 understood（不规则）。', '变形'),
 F('选词填空', XC('understand', 'understanding', 'misunderstand'), 'Thank you for your ______.', 'understanding', 'your 后面用名词 understanding（理解、体谅）。'),
 F('完成句子', WC, 'Do you understand ______ I ______?', 'what；mean', '宾语从句 what I mean（我的意思）。', zh='你明白我的意思吗？'),
]
Q['already'] = [
 L('I have already finished my homework, so I can watch TV now.', '说话人现在可以做什么？', ['看电视', '写作业', '睡觉', '出去玩'], 'have already finished 已经做完了作业。'),
 C('单项选择', DX, "—Have you had lunch ______?\n—Yes, I've ______ had it.", ['yet; already', 'already; yet', 'yet; yet', 'already; already'], '疑问句用 yet，肯定句用 already。', '易混'),
 F('适当形式填空', SX, 'The film had already ______ when we got to the cinema. (begin)', 'begun', 'had already + 过去分词，begin 的过去分词是 begun。', '用法'),
 F('句型转换', '改为否定句，每空一词。', 'I have already read the book.\nI ______ read the book ______.', "haven't；yet", '否定句里 already 换成 yet，放句末。', '易混'),
 C('单项选择', DX, 'My father ______ to Beijing. He is still there now.', ['has already gone', 'has already been', 'already went', 'goes already'], 'has gone to 去了还没回来；has been to 是去过、已经回来了。', '用法'),
]
Q['depend'] = [
 L('Whether we go to the park depends on the weather.', '去不去公园取决于什么？', ['天气', '时间', '妈妈', '作业'], 'depend on 取决于。'),
 F('适当形式填空', SX, 'Children should learn to be ______ as they grow up. (depend)', 'independent', 'be 后面用形容词；“独立的”是 in + dependent：independent。', '词性转换'),
 F('同义替换', '保持句意不变，每空一词。', 'You can depend on him.\nYou can ______ ______ him.', 'rely；on', 'depend on = rely on 依靠、信赖。', '用法'),
 C('单项选择', DX, "—Shall we go hiking tomorrow?\n—It ______. Maybe it will rain.", ['depends', 'depend', 'depending', 'is depended'], 'It depends. 看情况而定，it 是三单。', '用法'),
 F('改错', GC, 'Many old people depend their children.', 'depend → depend on', 'depend 不能直接带宾语，要说 depend on sb.。', '用法'),
]
Q['depend on'] = [
 L('You can depend on Jack. He always keeps his promises.', '说话人觉得 Jack 怎么样？', ['可以信赖', '很粗心', '很聪明', '很懒'], 'depend on 信赖；keeps his promises 守信用。'),
 C('单项选择', DX, 'Success depends on ______ hard.', ['working', 'work', 'to work', 'works'], 'on 是介词，后面接 doing。', '用法'),
 F('同义替换', '保持句意不变，每空一词。', "We shouldn't depend on others all the time.\nWe shouldn't ______ ______ others all the time.", 'rely；on', 'depend on = rely on。', '用法'),
 F('完成句子', WC, 'Whether you can pass the exam depends on ______.', 'yourself', '“你自己”用反身代词 yourself。', zh='你能不能及格取决于你自己。'),
 C('单项选择', DX, '—Will you go to the party?\n—It ______ how much homework I have.', ['depends on', 'depend on', 'depends in', 'is depended on'], 'it 是三单用 depends；搭配是 depend on。', '用法'),
]
Q['oven'] = [
 L('Mum is baking a cake in the oven for my birthday.', '妈妈在用烤箱做什么？', ['烤蛋糕', '烤面包', '烤鸡', '烤饼干'], 'baking a cake in the oven 在烤箱里烤蛋糕。'),
 C('单项选择', DX, 'Be careful! The oven is very ______.', ['hot', 'hotly', 'heat', 'cold'], 'be 后面用形容词 hot；烤箱“很烫”所以要小心。'),
 F('完成句子', WC, 'Put the chicken ______ the oven ______ twenty minutes.', 'in；for', '放进烤箱 in the oven；“烤 20 分钟”一段时间用 for。', zh='把鸡肉放进烤箱烤二十分钟。'),
 F('选词填空', XC('oven', 'over', 'often'), 'How ______ do you use the oven?', 'often', 'How often 问频率“多久一次”。'),
 F('改错', GC, 'There are two oven in our kitchen.', 'oven → ovens', 'two 后面用复数 ovens。'),
]
Q['truly'] = [
 L("I'm truly sorry for being late again.", '说话人在做什么？', ['道歉', '感谢', '邀请', '抱怨'], "truly sorry 真心抱歉，是在道歉。"),
 F('适当形式填空', SX, 'Your dream will come ______ if you work hard. (truly)', 'true', 'come true 实现，用形容词 true。', '词性转换'),
 C('单项选择', DX, 'He ______ loves his job.', ['truly', 'true', 'truth', 'trues'], '修饰动词 loves 用副词 truly（true 去 e 加 ly）。', '词性转换'),
 F('选词填空', XC('true', 'truly', 'truth'), 'Please tell me the ______.', 'truth', 'the 后面用名词 truth（真相）。', '词性转换'),
 F('改错', GC, 'She was truely happy to see her old friends.', 'truely → truly', 'true 变副词要去 e 加 ly，没有 truely。', '词性转换'),
]

# ---------------------------------------------------------------------------------------------
# 第 126 条（第七十五版）：每个词加两道——「题目6」「题目7」，专门考「考点」列（kd 必写），
# 考的是考点里前 5 道还没考到的点（kaodian_hand.py 手写的详细考点）；题型尽量和前 5 道不重复；答案就是本词原形的，7 道里还是最多 1 道。
SG = '保持句意不变，每空一词。'
Q['camera'] += [
 F('适当形式填空', SX, 'Two ______ are filming the football match. (cameraman)', 'cameramen', 'cameraman 摄影师，man 变成 men：cameramen。', '词性转换'),
 F('改错', GC, 'I took these photos by my new camera.', 'by → with', '用某个工具做事用 with：with my new camera。', '用法'),
]
Q['speaker'] += [
 F('适当形式填空', SX, 'He has ______ at three meetings this month. (speak)', 'spoken', 'has 后面用过去分词；speak 的过去分词是 spoken（不规则）。', '词性转换'),
 F('完成句子', WC, 'She is a ______ English ______.', 'native；speaker', '“说母语的人”是 native speaker。', '短语', zh='她是以英语为母语的人。'),
]
Q['thermostat'] += [
 F('改错', GC, "It's too cold. Please turn up it.", 'turn up it → turn it up', 'turn up 的宾语是代词时放在中间：turn it up。', '用法'),
 F('适当形式填空', SX, 'Most new houses have smart ______ now. (thermostat)', 'thermostats', 'houses 是复数，每家都有，用复数 thermostats。', '变形'),
]
Q['itself'] += [
 F('同义替换', SG, 'The cat lives alone in the old house.\nThe cat lives ______ ______ in the old house.', 'by；itself', 'by itself = alone，独自。', '短语'),
 C('单项选择', DX, '—Help ______ to some fruit, boys and girls.\n—Thank you.', ['yourselves', 'yourself', 'themselves', 'ourselves'], 'help oneself to sth. 随便吃；对 boys and girls 说，用 yourselves。', '变形'),
]
Q['alarm'] += [
 F('适当形式填空', SX, 'The fire alarm ______ (go) off during the class yesterday.', 'went', 'go off（警报）响；yesterday 用过去式 went（不规则）。', '短语'),
 F('改错', GC, 'We were alarming by the loud noise.', 'alarming → alarmed', '人感到惊慌用 alarmed；alarming 说事情让人惊慌。', '易混'),
]
Q['stranger'] += [
 F('完成句子', WC, "Sorry, I'm ______ ______ here.", 'a；stranger', 'I\'m a stranger here. 问路时说“我对这儿不熟”；stranger 可数，前面加 a。', '用法', zh='对不起，我对这儿不熟。'),
 C('单项选择', DX, "Don't talk ______ strangers on the way home.", ['to', 'at', 'for', 'of'], 'talk to sb. 和某人说话。', '短语'),
]
Q['lock'] += [
 F('适当形式填空', SX, "I can't ______ the door. I have the wrong key. (lock)", 'unlock', '打不开门，要的是“开锁”：un- 表示相反的动作，unlock。', '词性转换'),
 F('完成句子', WC, '______ ______ your money before you go to bed.', 'Lock；up', 'lock up 锁好、锁起来；祈使句，句首大写。', '短语', zh='睡觉前把钱锁好。'),
]
Q['explore'] += [
 F('改错', GC, 'They explored into the old castle last week.', 'explored into → explored', 'explore 后面直接加地方，不加 into。', '用法'),
 C('单项选择', DX, 'Look! The children ______ the forest.', ['are exploring', 'explore', 'explored', 'are exploreing'], 'Look! 说明正在发生，用现在进行时；explore 去 e 加 ing：exploring。', '变形'),
]
Q['rock'] += [
 F('适当形式填空', SX, 'The road up the hill is very ______. Be careful! (rock)', 'rocky', 'is 后面要形容词：rock 加 y 变成 rocky（多岩石的）。', '词性转换'),
 F('改错', GC, 'My cousin plays in a rocks band.', 'rocks → rock', 'rock band 摇滚乐队，rock 作定语用单数。', '短语'),
]
Q['shower'] += [
 F('改错', GC, 'I usually do a shower after PE class.', 'do → take', '洗淋浴说 take / have a shower，不说 do a shower。', '短语'),
 F('适当形式填空', SX, 'He ______ (shower) and went to bed at ten last night.', 'showered', 'shower 也能当动词“洗淋浴”；和 went 并列，用过去式 showered。', '变形'),
]
Q['mode'] += [
 F('完成句子', WC, 'Please turn on ______ ______ on the plane.', 'flight；mode', '飞行模式是 flight mode。', '短语', zh='在飞机上请打开飞行模式。'),
 F('改错', GC, 'Taking the subway is a green mode for transport.', 'for → of', '“…的方式”说 a mode of transport，用 of。', '用法'),
]
Q['text message'] += [
 F('句型转换', SG, 'I sent my mom a text message.\nI sent a text message ______ my mom.', 'to', 'send sb. sth. = send sth. to sb.。', '用法'),
 F('适当形式填空', SX, 'My sister ______ (text) me an hour ago.', 'texted', 'text 也能当动词“发短信”；an hour ago 用过去式 texted。', '词性转换'),
]
Q['bedroom'] += [
 F('适当形式填空', SX, 'My ______ (parent) bedroom is next to mine.', "parents'", '父母的卧室：parents 是以 s 结尾的复数，所有格只加 ’：parents\'。', '用法'),
 C('单项选择', DX, "I'm very tired. I'm going to my ______ to have a rest.", ['bedroom', 'bathroom', 'kitchen', 'garden'], '休息、睡觉在卧室 bedroom；bathroom 是浴室，kitchen 是厨房。', '易混'),
]
Q['bathroom'] += [
 C('单项选择', DX, 'Excuse me, I need to ______ the bathroom.', ['go to', 'go', 'come', 'get'], 'go to the bathroom 去洗手间；go 后面接地方要加 to。', '短语'),
 F('改错', GC, 'My little brother is having a bathroom now.', 'bathroom → bath', '洗澡是 have / take a bath；bathroom 是浴室。', '易混'),
]
Q['suggest'] += [
 C('单项选择', DX, 'My teacher ______ me to read more English books.', ['advised', 'suggested', 'said', 'spoke'], 'advise sb. to do sth. 可以；suggest 后面不能接 sb. to do。', '易混'),
 F('句型转换', SG, 'Why not take a walk after supper?\nI ______ ______ a walk after supper.', 'suggest；taking', 'Why not do…? = I suggest doing…（suggest 后接动名词）。', '用法'),
]
Q['protect'] += [
 C('单项选择', DX, 'The heavy rain ______ us from going out yesterday.', ['prevented', 'protected', 'provided', 'produced'], '阻止某人做某事用 prevent sb. from doing；protect … from 是保护…免受…。', '易混'),
 F('适当形式填空', SX, 'These rare birds ______ (protect) by law in China.', 'are protected', '鸟是“被保护”，主语是复数，用被动 are protected。', '用法'),
]
Q['review'] += [
 F('同义替换', SG, 'We should review our lessons after class.\nWe should ______ ______ our lessons after class.', 'go；over', 'go over = review，复习。', '用法'),
 F('适当形式填空', SX, 'The ______ said the new film was boring. (review)', 'reviewer', 'the 后面要名词，“写评论的人”是 reviewer（review 加 -er）。', '词性转换'),
]
Q['heating'] += [
 C('单项选择', DX, "It's cold. Let's turn on the ______ next to the sofa.", ['heater', 'heat', 'hot', 'heats'], '沙发旁边的取暖器是一件东西，用 heater；heating 是整套供暖。', '易混'),
 F('完成句子', WC, 'Please ______ ______ the soup again.', 'heat；up', 'heat up sth. 把…热一下。', '词性转换', zh='请把汤再热一下。'),
]
Q['guide'] += [
 F('适当形式填空', SX, "Under the teacher's ______, we finished the project. (guide)", 'guidance', '所有格后面要名词，“指导”是 guidance（去 e 加 ance）。', '词性转换'),
 F('改错', GC, 'Our guide is guideing us through the old town.', 'guideing → guiding', 'guide 以 e 结尾，去 e 加 ing：guiding。', '变形'),
]
Q['personal'] += [
 F('适当形式填空', SX, 'Tom has a warm and friendly ______. (personal)', 'personality', 'a … 后面要名词，“个性”是 personality。', '词性转换'),
 F('改错', GC, 'He came to see me in personal.', 'in personal → in person', '“亲自”是 in person，person 是名词。', '短语'),
]
Q['owner'] += [
 F('完成句子', WC, 'He finished the work ______ his ______.', 'on；own', 'on one\'s own = alone，独自。', '短语', zh='他独自完成了这项工作。'),
 F('改错', GC, 'I want to have a room of my owner.', 'owner → own', 'of one\'s own 自己的；owner 是“主人”。', '易混'),
]
Q['alarm clock'] += [
 F('改错', GC, "I set my alarm clock in six o'clock.", 'in → for', '把闹钟定在几点：set the alarm clock for + 时间。', '短语'),
 F('适当形式填空', SX, 'Look! The alarm clock ______ (ring). Get up now!', 'is ringing', 'Look! 说明正在发生，用现在进行时 is ringing。', '用法'),
]
Q['keep track of'] += [
 F('适当形式填空', SX, 'Last month she ______ (keep) track of her spending in a notebook.', 'kept', 'last month 用过去式；keep 的过去式是 kept（不规则）。', '变形'),
 C('单项选择', DX, 'This app helps me keep track of ______ steps I walk every day.', ['how many', 'how much', 'how long', 'how often'], 'keep track of 后面可以接 wh- 从句；steps 可数，用 how many。', '用法'),
]
Q['schedule'] += [
 F('完成句子', WC, 'We finished the project two days ______ ______ schedule.', 'ahead；of', 'ahead of schedule 提前。', '短语', zh='我们提前两天完成了这个项目。'),
 F('适当形式填空', SX, 'The football match is scheduled ______ (start) at 3 p.m.', 'to start', 'be scheduled to do sth. 定于做某事。', '用法'),
]
Q['oven'] += [
 C('单项选择', DX, 'Mum is cooking noodles on the ______.', ['stove', 'oven', 'fridge', 'sink'], '在炉灶上煮面：on the stove；oven 是烤箱，东西放 in the oven 里烤。', '易混'),
 F('完成句子', WC, "Let's heat the milk in the ______ ______.", 'microwave；oven', '微波炉是 microwave oven。', '短语', zh='用微波炉把牛奶热一下吧。'),
]
Q['sore'] += [
 F('适当形式填空', SX, 'My throat is even ______ today than yesterday. (sore)', 'sorer', 'than 前面用比较级；sore 以 e 结尾，加 r：sorer。', '变形'),
 F('完成句子', WC, "I have a ______ ______, so I can't go running.", 'sore；back', 'have a sore + 身体部位：a sore back 背疼。', '短语', zh='我背疼，不能去跑步了。'),
]
Q['throat'] += [
 F('改错', GC, 'Both of the singers have sore throat.', 'throat → throats', 'both 说的是两个人，各有一个喉咙，用复数 sore throats。', '变形'),
 F('同义替换', SG, "What's wrong with your throat?\nWhat's the ______ ______ your throat?", 'matter；with', "What's wrong with…? = What's the matter with…?", '用法'),
]
Q['understand'] += [
 F('适当形式填空', SX, 'Sorry, I ______ you. I thought you said Monday. (understand)', 'misunderstood', '“我以为你说的是周一”：是误解，mis- + understand，过去式 misunderstood。', '词性转换'),
 C('单项选择', DX, 'He speaks Chinese well, so he can make himself ______ in Beijing.', ['understood', 'understand', 'understanding', 'to understand'], 'make oneself understood 使别人理解自己的意思，用过去分词。', '短语'),
]
Q['already'] += [
 F('改错', GC, 'I already have finished my homework.', 'already have → have already', 'already 放在 have / has 和过去分词中间。', '用法'),
 F('选词填空', XC('already', 'yet', 'still'), "It's ten o'clock, but Tom is ______ sleeping.", 'still', '“还在睡”用 still（仍然）；already 是“已经”，yet 用在否定句、疑问句里。', '易混'),
]
Q['depend'] += [
 F('适当形式填空', SX, 'Many young people want more ______ from their parents. (depend)', 'independence', 'more 后面要名词，“独立”是 independence（in- 表示否定）。', '词性转换'),
 F('完成句子', WC, 'We are depending ______ you ______ help us.', 'on；to', 'depend on sb. to do sth. 指望某人做某事。', '短语', zh='我们指望你来帮我们。'),
]
Q['depend on'] += [
 F('适当形式填空', SX, 'When he was young, he ______ (depend) on his parents for everything.', 'depended', '说的是小时候，用过去式 depended。', '变形'),
 F('改错', GC, 'You can depend on him finish the work on time.', 'finish → to finish', 'depend on sb. to do sth. 指望某人做某事，to 不能省。', '用法'),
]
Q['order'] += [
 C('单项选择', DX, 'I ordered a pizza ______ my little brother.', ['for', 'to', 'with', 'at'], 'order sth. for sb. 给某人订（点）某物。', '用法'),
 F('改错', GC, 'So as to get good grades, he studies hard.', 'So as to → In order to', '表目的放在句首用 In order to；so as to 不放句首。', '易混'),
]
Q['signal'] += [
 F('适当形式填空', SX, 'The policeman ______ (signal) the driver to stop.', 'signalled', '说的是过去的事，用过去式；英式双写 l：signalled（美式 signaled）。', '变形'),
 C('单项选择', DX, 'The traffic ______ turned green, so we crossed the road.', ['signal', 'sign', 'mark', 'symbol'], 'traffic signal 交通信号灯，会变颜色；sign 是写着字的标志牌。', '易混'),
]
Q['sense'] += [
 F('选词填空', XC('sensible', 'sensitive'), "It was ______ of you to bring an umbrella. It's raining now.", 'sensible', '带伞是明智的做法，用 sensible（明智的）；sensitive 是“敏感的”。', '易混'),
 F('适当形式填空', SX, "Don't talk ______. That's not true at all! (sense)", 'nonsense', 'talk nonsense 胡说；sense 前面加 non-。', '词性转换'),
]
Q['manage'] += [
 F('同义替换', SG, 'He managed to find the lost dog.\nHe ______ ______ finding the lost dog.', 'succeeded；in', 'manage to do sth. = succeed in doing sth.。', '用法'),
 C('单项选择', DX, "I ______ to open the window, but I couldn't.", ['tried', 'managed', 'succeeded', 'finished'], '“但没打开”，用 try to do（努力去做，不一定成功）；manage to do 是做成了。', '易混'),
]
Q['remind'] += [
 F('适当形式填空', SX, 'I put a ______ on the fridge so I would not forget. (remind)', 'reminder', 'a 后面要名词，“提醒的东西”是 reminder（remind 加 -er）。', '词性转换'),
 F('完成句子', WC, 'The teacher reminded us ______ we had a test the next day.', 'that', 'remind sb. that + 从句，提醒某人…。', '短语', zh='老师提醒我们第二天有考试。'),
]
Q['produce'] += [
 F('适当形式填空', SX, 'Her father is a famous film ______. (produce)', 'producer', 'a famous film 后面要名词，“制片人”是 producer（去 e 加 er）。', '词性转换'),
 C('单项选择', DX, 'These cars ______ in Shanghai last year.', ['were produced', 'produced', 'are produced', 'were producing'], '车是“被生产”，last year 用一般过去时的被动：were produced。', '用法'),
]
Q['store'] += [
 F('完成句子', WC, 'My mother works in a ______ ______.', 'department；store', '百货商店是 department store。', '短语', zh='我妈妈在一家百货商店工作。'),
 F('适当形式填空', SX, 'We need more ______ space for our books. (store)', 'storage', 'space 前面要“储存”的意思，用名词 storage（去 e 加 age）。', '词性转换'),
]
Q['truly'] += [
 F('完成句子', WC, "To ______ the ______, I don't like this film.", 'tell；truth', 'to tell the truth 说实话。', '短语', zh='说实话，我不喜欢这部电影。'),
 F('适当形式填空', SX, "The story sounds ______. I don't believe it. (true)", 'untrue', '不相信，说明故事“不真实”：true 前面加 un-，untrue。', '词性转换'),
]
Q['health care'] += [
 F('适当形式填空', SX, 'Eating too much fast food is ______ for children. (health)', 'unhealthy', 'is 后面要形容词，意思是“不健康的”：unhealthy（un- 表示否定）。', '词性转换'),
 F('改错', GC, 'Doctors give the old people good health cares.', 'health cares → health care', 'health care 不可数，不能加 s。', '用法'),
]

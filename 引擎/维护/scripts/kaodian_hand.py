# -*- coding: utf-8 -*-
"""第 126 条（第七十五版，详细考点轮）：7A-U4 这 40 个词（单元表 camera … truly）手写的详细考点。
kaodian.py --write 时这些词照这里写（整格替换），别的词按 kaodian_full.py 的规则写。
写法和视频技能 wordfilm.js 的 kaodianOf 对得上：
  【变形】每个词性一组，组和组之间用“ / ”；一组里几样用“；”（视频里一样一个小块）
  【词性转换】【短语】【用法】【易混】几条用“；”隔开（括号里的“；”“，”不算）
  条数：词性转换 ≤ 4、短语 ≤ 4、用法 ≤ 3、易混 ≤ 2（视频照这个数画，详见视频技能规矩 59）
依据：上海市教育考试院《2020 年上海市初中英语课程终结性评价指南》词汇表、词组表和知识内容（词形变化、构词法、名词、
代词、动词的时态和语态、非谓语动词），牛津上海版 7A Unit 4 的课文用法，上海中考、区模考的常考题型（适当形式填空、
句型转换、单项选择）。每个词出的“题目6”“题目7”考的就是这里写的点（lianxi_data.py）。
"""

HAND = {
    'camera': """【变形】n. 复数 cameras
【词性转换】n. cameraman 摄影师（复数 cameramen）
【短语】take photos with a camera 用相机拍照；a digital camera 数码相机；a security camera 监控摄像头
【用法】camera 可数：a camera、two cameras；用相机拍照用 with（工具）：with my camera，不说 by my camera
【易混】camera / photo / video（camera 是拍照的机器，photo 是拍出来的照片，video 是录像）""",

    'speaker': """【变形】n. 复数 speakers
【词性转换】v. speak 说（过去式 spoke、过去分词 spoken，不规则）；n. speech 演讲（不说 speakion）
【短语】a native speaker 说母语的人；an English speaker 说英语的人；give a speech 发表演讲
【用法】speak + -er 表示“…的人”：speaker 说话的人、演讲人；也指“扬声器、音箱”：turn down the speaker
【易混】speaker / speech（speaker 是演讲的人，speech 是演讲本身）；speak / say / talk / tell（speak + 语言，say + 内容，talk with / about，tell sb. sth.）""",

    'thermostat': """【变形】n. 复数 thermostats
【短语】turn up / down the thermostat 调高 / 调低温控器；set the thermostat to 22 degrees 把温控器设到 22 度
【用法】turn up / turn down 的宾语是代词时放中间：turn it up，不说 turn up it；set sth. to + 温度
【易混】thermostat / thermometer（thermostat 温控器，自己控制温度；thermometer 温度计，只量温度）""",

    'itself': """【变形】pron. it 的反身代词；反身代词：myself、yourself、himself、herself、itself、ourselves、yourselves、themselves
【短语】by itself 独自、自动地；in itself 本身；help oneself to sth. 随便吃（用）某物
【用法】反身代词和主语是同一个：The cat is washing itself.；by itself = alone（独自），也表示“自动地”：The door opened by itself.
【易混】itself / its / it's（itself 它自己，its 它的，it's = it is / it has）""",

    'alarm': """【变形】n. 复数 alarms / v. 三单 alarms；过去式、过去分词 alarmed；现在分词 alarming
【词性转换】adj. alarmed 惊恐的（人感到）；adj. alarming 令人担忧的（事情让人）
【短语】a fire alarm 火警警报；set the alarm (for six) 定闹钟（定在六点）；the alarm goes off 警报 / 闹钟响了
【用法】go off（警报、闹钟）响，过去式 went off；be alarmed at / by sth. 对…感到惊慌
【易混】alarmed / alarming（-ed 说人感到惊慌，-ing 说事情让人惊慌）""",

    'stranger': """【变形】n. 复数 strangers
【词性转换】adj. strange 奇怪的、陌生的；adv. strangely 奇怪地
【短语】a complete stranger 完全陌生的人；talk to strangers 和陌生人说话；be a stranger here 对这儿不熟
【用法】问路时说 Sorry, I'm a stranger here.（我对这儿不熟）；stranger 可数，前面要有 a / the 或用复数
【易混】stranger 名词“陌生人” / stranger 也是 strange 的比较级“更奇怪的”（看前面有没有 a、the，后面有没有 than）""",

    'lock': """【变形】n. 复数 locks / v. 三单 locks；过去式、过去分词 locked；现在分词 locking
【词性转换】v. unlock 开锁（un- 表示相反的动作）；adj. locked 锁着的
【短语】lock the door 锁门；lock up 锁好、锁起来；lock sth. in … 把…锁在…里
【用法】被动：The gate is locked at ten every night.；forget to lock 忘了去锁（没锁），forget locking 忘了已经锁过
【易混】lock / key（lock 锁，key 钥匙：the key to the door）""",

    'explore': """【变形】v. 三单 explores；过去式、过去分词 explored（去 e 加 d）；现在分词 exploring（去 e 加 ing）
【词性转换】n. explorer 探险家（去 e 加 r）；n. exploration 探索、勘探
【短语】explore the world 探索世界；explore space / the deep sea 探索太空 / 深海；explore the old town 游览古镇
【用法】explore 是及物动词，直接加地方：explore the forest，不说 explore into；spend time (in) exploring sth. 花时间探索
【易混】explore / expect（形近：explore 探索，expect 期待：expect to do）；explore / explode（explode 爆炸）""",

    'rock': """【变形】n. 复数 rocks / v. 三单 rocks；过去式、过去分词 rocked；现在分词 rocking
【词性转换】adj. rocky 多岩石的（rock 加 y）
【短语】rock music 摇滚乐；a rock band 摇滚乐队；rock the baby 摇婴儿
【用法】“岩石”可数：many rocks；“摇滚乐”不可数：listen to rock；rock 作定语用单数：a rock band，不说 a rocks band
【易混】rock / stone（rock 大块岩石、岩层，stone 小块石头、石料）""",

    'shower': """【变形】n. 复数 showers / v. 三单 showers；过去式、过去分词 showered；现在分词 showering
【短语】take / have a shower 洗淋浴；a heavy shower 一场大阵雨；showers 阵雨（天气预报）
【用法】洗淋浴说 take / have a shower，不说 do a shower；shower 也能当动词：He showered and went to bed.
【易混】shower / bath（shower 淋浴，bath 盆浴：take / have a bath）""",

    'mode': """【变形】n. 复数 modes
【短语】a mode of transport 一种交通方式；green modes of transport 绿色出行方式；silent mode 静音模式；flight mode 飞行模式
【用法】“…的方式”用 of：a mode of transport；one of the + 最高级 + modes：one of the fastest modes of transport
【易混】mode / mood（形近：mode 方式、模式，mood 心情：in a good mood）""",

    'text message': """【变形】n. 复数 text messages
【词性转换】v. text 发短信（text sb.；过去式 texted）
【短语】send sb. a text message 给某人发短信；get a text message from sb. 收到某人的短信；leave a message 留言
【用法】send sb. sth. = send sth. to sb.：send my mom a text message = send a text message to my mom
【易混】message / massage（形近：message 消息、留言，massage 按摩）""",

    'bedroom': """【变形】n. 复数 bedrooms
【短语】in the bedroom 在卧室里；a two-bedroom flat 两居室的公寓
【用法】合成词：bed + room = bedroom，同样 bathroom、classroom，living room 分开写；名词所有格 + bedroom：my parents' bedroom（复数 s 后只加 ’）
【易混】bedroom / bathroom / living room（bedroom 卧室，睡觉、休息；bathroom 浴室、卫生间；living room 客厅）""",

    'bathroom': """【变形】n. 复数 bathrooms
【短语】go to the bathroom 去洗手间；clean the bathroom 打扫浴室
【用法】May I use your bathroom? 能用一下你的洗手间吗？（美式 bathroom，英式多说 toilet）；go 后面接地方要加 to：go to the bathroom
【易混】bath / bathroom（bath 洗澡：have / take a bath，bathroom 浴室）""",

    'suggest': """【变形】v. 三单 suggests；过去式、过去分词 suggested；现在分词 suggesting
【词性转换】n. suggestion 建议（可数：make a suggestion、give sb. some suggestions）
【短语】make a suggestion 提建议；suggest sth. to sb. 向某人提出某事
【用法】suggest doing sth.（不说 suggest sb. to do）；suggest that sb. (should) do sth.（从句用动词原形，should 可省）；Why not do…? = I suggest doing…
【易混】suggest / advise（advise sb. to do 可以，suggest sb. to do 不行）；suggestion 可数 / advice 不可数（a piece of advice）""",

    'protect': """【变形】v. 三单 protects；过去式、过去分词 protected；现在分词 protecting
【词性转换】n. protection 保护；adj. protective 保护的；n. protector 保护者
【短语】protect … from … 保护…免受…；protect the environment 保护环境；protect wild animals 保护野生动物
【用法】protect sb. / sth. from (doing) sth.（from 后接名词或动名词）；被动 be protected by …：The birds are protected by law.
【易混】protect / prevent（protect … from 保护…不受伤害，prevent … from doing 阻止…做某事）；protect / provide（形近：provide 提供：provide sb. with sth.）""",

    'review': """【变形】v. 三单 reviews；过去式、过去分词 reviewed；现在分词 reviewing / n. 复数 reviews
【词性转换】n. reviewer 评论者（review 加 -er）；n. view 看法、景色（re- 再 + view 看）
【短语】review the new words 复习新单词；review for the exam 为考试复习；get good reviews 获得好评
【用法】review = go over（复习，同义替换常考）；作名词“评论”可数：good reviews
【易混】review / preview（review 学过之后再看，就是复习；preview 上课之前先看，就是预习）""",

    'heating': """【变形】n. 不可数，没有复数
【词性转换】v. heat 加热（三单 heats）；n. heat 热、热量；adj. hot 热的；n. heater 加热器、取暖器
【短语】turn on / off the heating 打开 / 关掉暖气；central heating 集中供暖；heat (up) the soup 把汤热一下
【用法】heating 不可数，谓语用单数：The heating is broken.；heat 作动词：heat up sth. / heat sth. up
【易混】heating / heater（heating 供暖、暖气系统，heater 一台取暖器）；heat / hot（heat 名词、动词，hot 形容词）""",

    'guide': """【变形】n. 复数 guides / v. 三单 guides；过去式、过去分词 guided（去 e 加 d）；现在分词 guiding（去 e 加 ing）
【词性转换】n. guidance 指导（去 e 加 ance）；n. guidebook 旅行指南
【短语】a tour guide 导游；a guide to Shanghai 上海指南；under sb.'s guidance 在某人的指导下
【用法】guide sb. to / through sp. 带领某人去 / 游览某地；be a guide / work as a guide 当导游
【易混】guide / lead（guide 熟悉路的人带路、讲解，lead 走在前面带领、领导）""",

    'personal': """【词性转换】n. person 人；adv. personally 就个人而言；n. personality 个性
【短语】personal information 个人信息；personal things 私人物品；a personal question 私人问题；in person 亲自
【用法】personal 作定语或表语：a personal question、It's personal.；Personally, I think … 就我个人而言（放句首）
【易混】personal / person（personal 形容词“私人的”，person 名词“人”）；in person / personally（in person 亲自到场，personally 就个人而言）""",

    'owner': """【变形】n. 复数 owners
【词性转换】v. own 拥有（三单 owns）；adj. own 自己的；n. ownership 所有权
【短语】the owner of … …的主人；on one's own 独自；of one's own 自己的
【用法】own 作形容词前面要有物主代词：my own room、a room of my own；on one's own = alone
【易混】owner / own（owner 名词“主人”，own 动词“拥有”、形容词“自己的”）""",

    'alarm clock': """【变形】n. 复数 alarm clocks
【短语】set the alarm clock for six 把闹钟定在六点；the alarm clock goes off / rings 闹钟响了
【用法】set the alarm clock for + 时间（用 for，不用 in、on）；go off 响，过去式 went off；正在响用进行时：It's ringing.
【易混】clock / watch（clock 挂钟、座钟、闹钟，watch 手表）""",

    'keep track of': """【变形】keep 过去式、过去分词 kept（不规则）
【短语】keep track of 记录、了解…的动向；lose track of 不了解、失去联系（过去式 lost）
【用法】keep track of + 名词 / wh- 从句：keep track of how many steps you walk；keep 后面用 of，不说 keep track for
【易混】keep track of / lose track of（keep 一直记着、掌握情况，lose 弄不清了：lose track of time 忘了时间）""",

    'schedule': """【变形】n. 复数 schedules / v. 三单 schedules；过去式、过去分词 scheduled（去 e 加 d）；现在分词 scheduling
【短语】on schedule 按时；ahead of schedule 提前；behind schedule 落后于计划；a busy schedule 繁忙的日程
【用法】be scheduled for + 时间：The meeting is scheduled for Monday.；be scheduled to do sth. 定于做某事
【易混】on schedule / on time（on schedule 按计划表，on time 按约定的时间，都表“按时”）；ahead of / behind schedule（提前 / 落后）""",

    'oven': """【变形】n. 复数 ovens
【短语】bake a cake in the oven 在烤箱里烤蛋糕；a microwave oven 微波炉；turn on the oven 打开烤箱
【用法】在烤箱里用 in：in the oven；bake sth. for + 时间：bake it for twenty minutes
【易混】oven / stove（oven 烤箱，东西放在里面烤；stove 炉子、灶，在上面煮：on the stove）""",

    'sore': """【变形】adj. 比较级 sorer、最高级 sorest（以 e 结尾，加 r、st）
【短语】have a sore throat 喉咙痛；sore eyes 眼睛痛；a sore back 背痛
【用法】have a sore + 身体部位：I have a sore throat.；作表语：My legs are sore.；复数部位前不加 a：sore eyes
【易混】sore / sorry（形近：sore 疼痛的，sorry 抱歉的、难过的）""",

    'throat': """【变形】n. 复数 throats
【短语】have a sore throat 喉咙痛；clear one's throat 清嗓子
【用法】What's wrong with your throat? = What's the matter with your throat?；两个人各有一个：sore throats
【易混】throat / through（形近：throat 喉咙，through 穿过）""",

    'understand': """【变形】v. 三单 understands；过去式、过去分词 understood（不规则）；现在分词 understanding
【词性转换】n. understanding 理解、谅解；v. misunderstand 误解（过去式 misunderstood）；adj. understandable 可以理解的
【短语】make oneself understood 使别人理解自己；be easy / hard to understand 容易 / 难以理解
【用法】understand 说的是一种状态，一般不用进行时：Do you understand? 不说 Are you understanding?；被动 be understood
【易混】understand / know（understand 懂得、理解意思，know 知道、认识）""",

    'already': """【用法】already 用于肯定句，放在 have / has 和过去分词之间：I have already finished it.；用在疑问句里表示惊讶：Have you finished already?；have already gone to 已经去了（人不在这儿）/ have been to 去过
【易混】already / yet（already 肯定句“已经”，yet 否定句“还”、疑问句“已经”，放句末）；already / still（still 仍然：He is still sleeping.）""",

    'depend': """【变形】v. 三单 depends；过去式、过去分词 depended；现在分词 depending
【词性转换】adj. independent 独立的（in- + depend + -ent）；n. independence 独立；adj. dependent 依赖的
【短语】depend on / upon 依靠、取决于；It depends. 看情况；depend on sb. to do sth. 指望某人做某事
【用法】depend 后面要接 on / upon，不直接带宾语：depend on my parents，不说 depend my parents；depend on + 名词 / 代词 / 动名词 / 从句
【易混】depend on / rely on（都表“依靠”，depend on 还表“取决于”）；dependent / independent（依赖的 / 独立的）""",

    'depend on': """【变形】depend 三单 depends；过去式、过去分词 depended
【短语】It depends. 看情况；It depends on … 取决于…；depend on sb. to do sth. 指望某人做某事
【用法】depend on + 名词 / 代词 / 动名词 / 从句：It depends on the weather.、Success depends on working hard.；depend on sb. to do sth.（to 不能省）
【易混】depend on / rely on（都表“依靠”，depend on 还表“取决于”）""",

    'order': """【变形】n. 复数 orders / v. 三单 orders；过去式、过去分词 ordered；现在分词 ordering
【词性转换】adj. orderly 有秩序的；n. disorder 混乱（dis- 表示否定）
【短语】in order to do 为了；out of order 出故障；in the right order 按正确的顺序；take one's order 点菜
【用法】order sb. (not) to do sth. 命令某人（不要）做某事；order sth. for sb. 给某人订（点）某物；in order to do = so as to do = so that + 从句
【易混】in order to / so as to（都表目的，in order to 能放句首，so as to 不放句首）；out of order / out of the order（“出故障”不加 the）""",

    'signal': """【变形】n. 复数 signals / v. 三单 signals；过去式、过去分词 signalled（英式双写 l，美式 signaled）；现在分词 signalling
【词性转换】n. sign 标志、迹象；n. signature 签名
【短语】a traffic signal 交通信号灯；a phone signal 手机信号；a signal to stop 停下来的信号
【用法】signal (to) sb. to do sth. 示意某人做某事；信号的好坏：The signal is good / bad / weak here.
【易混】signal / sign（signal 用灯光、声音、手势发出的信号，会变；sign 写着字、画着图的标志牌）""",

    'sense': """【变形】n. 复数 senses / v. 三单 senses；过去式、过去分词 sensed（去 e 加 d）；现在分词 sensing
【词性转换】adj. sensible 明智的；adj. sensitive 敏感的；n. nonsense 胡说（non- 表示“没有”）
【短语】a sense of humour 幽默感；a sense of smell 嗅觉；make sense 有道理；talk nonsense 胡说
【用法】make sense 里 sense 不加 s：What you said makes no sense.；sense that … 感觉到…
【易混】sensible / sensitive（sensible 明智的、通情达理的，sensitive 敏感的）""",

    'manage': """【变形】v. 三单 manages；过去式、过去分词 managed（去 e 加 d）；现在分词 managing（去 e 加 ing）
【词性转换】n. manager 经理（去 e 加 er）；n. management 管理（不去 e）
【短语】manage to do sth. 设法做成某事；manage a shop 经营商店；manage one's time 管理时间
【用法】manage to do sth. = succeed in doing sth.（句型转换常考）；manage 后面接 to do，不接 doing
【易混】manage to do / try to do（manage to do 做成了，try to do 努力去做、不一定成功）""",

    'remind': """【变形】v. 三单 reminds；过去式、过去分词 reminded；现在分词 reminding
【词性转换】n. reminder 提醒的东西、提示
【短语】remind sb. of sth. 使某人想起某事；remind sb. to do sth. 提醒某人做某事；remind sb. that … 提醒某人…
【用法】remind sb. to do sth.（to 不能省，不说 remind sb. doing）；remind sb. of / about sth.
【易混】remind / remember（remind 提醒别人，remember 自己记得：remember to do 记得要做，remember doing 记得做过）""",

    'produce': """【变形】v. 三单 produces；过去式、过去分词 produced（去 e 加 d）；现在分词 producing（去 e 加 ing） / n. 农产品，不可数
【词性转换】n. product 产品（可数）；n. production 生产；n. producer 生产者、制片人
【短语】produce food / cars 生产食物 / 汽车；be produced in … 在某地生产；fresh produce 新鲜农产品
【用法】被动 be produced：These cars were produced in Shanghai.；produce 作名词不可数，谓语用单数
【易混】produce / product（produce 农产品，不可数；product 产品，可数）；produce / provide（provide 提供：provide sb. with sth.）""",

    'store': """【变形】n. 复数 stores / v. 三单 stores；过去式、过去分词 stored（去 e 加 d）；现在分词 storing（去 e 加 ing）
【词性转换】n. storage 储存（去 e 加 age）
【短语】a department store 百货商店；a book store 书店；go to the store 去商店；store sth. in … 把…存放在…
【用法】作动词“储存”常用被动：Food should be stored in a cool place.；美式 store = 英式 shop
【易混】store / shop（都是“商店”，store 美式、多指大商店，shop 英式、多指小店）；store / storm（形近：storm 暴风雨）""",

    'truly': """【词性转换】adj. true 真的（true → truly 去 e 加 ly，易错）；n. truth 真相；adj. untrue 不真实的
【短语】come true 实现；tell the truth 说实话；Yours truly 您忠实的（信末客套）
【用法】truly 修饰形容词、动词：truly sorry、truly love sth.；come true 用形容词 true，不说 come truly
【易混】truly / truely（没有 truely，拼写易错）；true / truly（true 形容词，truly 副词）""",

    'health care': """【词性转换】adj. healthy 健康的；adv. healthily 健康地；adj. unhealthy 不健康的
【短语】take care of 照顾；take good care of oneself 照顾好自己；be good for one's health 对健康有益
【用法】health care 不可数，不加 s：good health care；health 是名词：keep in good health，healthy 是形容词：keep healthy
【易混】health / healthy（health 名词“健康”，healthy 形容词“健康的”）""",
}

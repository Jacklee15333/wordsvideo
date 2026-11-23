"""含义 + 例句 拆分时的人工改动：(行号, 第几个意思) → 新的意思（可以拆成几个）。
每项是 (词性, 标签列表, 意思, 例子列表)；词性写 None 表示不变，标签写 None 表示不变。"""
EDIT = {}
def E(rn, i, pos=None, labels=None, gloss=None, ex=None):
    EDIT[(rn, i)] = [(pos, labels, gloss, ex)]
def SPLIT(rn, i, *items):
    EDIT[(rn, i)] = list(items)

# 拆出例子以后，意思只剩“作定语”这类说明的：写出真正的意思
E(3395, 1, labels=['作定语时连成一个词'], gloss='关于是非的', ex=['a right-and-wrong question 是非题'])
E(3494, 1, labels=['放在最高级或 every、all 后面加强语气'], gloss='能想到的', ex=['the best result imaginable 能想到的最好结果'])
E(3601, 1, labels=['作定语'], gloss='高峰期的', ex=['rush-hour traffic 高峰期车流'])
E(6738, 1, labels=['作定语'], gloss='只把问题往后推的、拖延了事的')
E(6744, 1, pos='adj.', labels=['作定语'], gloss='爆米花式的、轻松热闹的', ex=['popcorn movie 爆米花电影（轻松热闹的商业娱乐片）'])
E(7033, 1, labels=['作定语'], gloss='海景的', ex=['a sea-view room / a seaview apartment 海景房、海景公寓'])
E(8098, 1, pos='adj.', labels=['作定语，用单数 pajama'], gloss='睡衣的')
E(546, 2, labels=['关系，也可指物'], gloss='…的')
E(8596, 3, pos='n.', labels=[], gloss='自我放逐', ex=['self-imposed exile'])
# 意思本身写成了例句：意思写中文，例句挪到例句列
E(305, 0, labels=[], gloss='see 的过去分词', ex=['I have seen it.'])
E(2110, 0, labels=[], gloss='go 的过去分词', ex=['He has gone home.'])
E(6469, 0, labels=[], gloss='shoot 的过去式、过去分词', ex=['He shot the ball.'])
E(754, 2, labels=['礼貌请求'], gloss='能否…、愿意…吗', ex=['Would you mind…?'])
E(755, 2, labels=['反问'], gloss='难道不…吗', ex=["Wouldn't it be nice…? 那岂不是很好？"])
E(1313, 2, labels=['委婉请求'], gloss='能…吗', ex=['Could you help me? 能帮我一下吗？'])
E(5126, 1, labels=['作形式主语、形式宾语'], gloss='不必译出', ex=['It is important to…'])
E(5126, 2, labels=['指情况'], gloss='情况、事情', ex=["How's it going? 情况怎么样"])
E(1193, 3, labels=[], gloss='构成完成时的被动语态', ex=['has been built 已经被建成'])
E(1608, 2, labels=['法庭用语'], gloss='反对', ex=['Objection! 反对！'])
E(1647, 2, labels=['答语'], gloss='一点没错', ex=['Exactly! 一点没错！'])
E(2869, 4, labels=[], gloss='成交', ex=['Done! 成交！'])
E(4576, 3, labels=['英'], gloss='干杯（1919）', ex=['Cheers!'])
E(7202, 3, pos='phr.', labels=[], gloss='Good heavens! 天哪', ex=[])
E(8606, 3, labels=['感叹'], gloss='天哪、谢天谢地', ex=['Oh my God! / Thank God!'])
E(8994, 2, labels=['训狗口令'], gloss='跟上', ex=['Heel!'])
E(9186, 2, labels=['英，口气偏老派'], gloss='好极了', ex=['Splendid!'])
# 例子夹在意思中间的
E(4717, 1, gloss='a bit 有点儿、一会儿', ex=['a bit tired', 'wait a bit'])
SPLIT(6470, 4, ('phr.', [], 'shooting star 流星（“划过天空的星”）', []), ('phr.', [], 'shooting pain 一阵阵的刺痛', []))
E(232, 0, gloss='开放权重的（训练好的参数公开、可下载，通常附有特定的许可证）', ex=['an open-weight model 开放权重模型'])
E(1296, 0, gloss='认得出的、可辨认的（英式拼写；美式 recognizable）', ex=['barely recognisable 几乎认不出来'])
E(1298, 0, gloss='认得出的、可辨认的（美式拼写；英式 recognisable）', ex=['instantly recognizable 一眼就认得出'])
E(1834, 0, gloss='高清的（常缩写为 HD）', ex=['a high-definition TV 高清电视'])
E(4291, 0, gloss='无路的、人迹罕至的（多见于文学）', ex=['a pathless forest'])
E(4530, 1, gloss='十三岁的孩子（刚进入 teenage“青少年时期”的年纪）', ex=['a thirteen-year-old'])
E(4532, 1, gloss='十八岁的人（在许多国家是法定成年的年纪）', ex=['an eighteen-year-old'])
E(5590, 0, gloss='态度上的、与态度有关的（多见于心理学、社会学文章）', ex=['attitudinal change 态度的转变', 'attitudinal survey 态度调查'])
SPLIT(6678, 2, (None, [], '砸开、撬开', ['crack a nut 砸核桃', 'crack a safe 撬保险柜']), (None, [], '破解', ['crack a code 破译密码']))
E(7138, 0, gloss='跨学科的（与 interdisciplinary 基本同义）', ex=['cross-disciplinary collaboration 跨学科合作'])
E(7853, 0, gloss='藻基的、用藻类做的（近年环保、新材料语境里的新造词）', ex=['algae-made plastic 藻类塑料', 'algae-made fuel 藻类燃料'])
SPLIT(3681, 3, (None, [], '由…产生', ['result from']), (None, [], '导致', ['result in']))
E(6159, 0, gloss='比特币（常见写法：Bitcoin 指整个系统，bitcoin 指货币单位）', ex=[])
# 词性：拆成两行以后，后面几个意思的词性没跟着改的
E(527, 2, pos='n.'); E(527, 4, pos='n.')
E(2201, 2, pos='n.'); E(2235, 2, pos='n.'); E(7382, 2, pos='n.')

# 例子是名词用法、意思也是名词的
E(171, 1, pos='n.'); E(1762, 1, pos='n.'); E(4145, 3, pos='n.'); E(8286, 0, pos='n.'); E(7578, 4, pos='n.'); E(7580, 1, pos='n.'); E(6699, 1, pos='n.'); E(5305, 1, pos='n.'); E(7692, 2, pos='n.'); E(6926, 3, pos='n.')

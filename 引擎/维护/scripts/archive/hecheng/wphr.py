"""每个词是从哪个短语合成来的：词|短语|短语的中文。合成规律那一行写成“短语（中文）→ 本词”。"""

RAW = r'''
# H02 宾语提前
shoemaker|make shoes|做鞋
timekeeper|keep time|计时
storyteller|tell stories|讲故事
storytelling|tell stories|讲故事
energy-saving|save energy|节约能源
life-changing|change one's life|改变人生
life-giving|give life|给予生命
Thanksgiving|give thanks|献上感谢
sightseeing|see the sights|看风景、看名胜
history-making|make history|创造历史
survey-taker|take a survey|做调查
video-editing|edit videos|剪辑视频
world-building|build a world|构建一个世界
tree-planting|plant trees|种树
line-sharing|share a line|共用线路
water-saving|save water|节约用水
water-testing|test water|检测水
handwashing|wash one's hands|洗手
turn-taking|take turns|轮流
decision-maker|make decisions|做决定
time-consuming|consume time|耗费时间
life-saving|save lives|救命
lifesaving|save lives|救命
caretaker|take care (of)|照管
caregiving|give care|给予照顾
eye-opening|open one's eyes|让人睁开眼睛
movie-making|make movies|拍电影
heartbreaking|break one's heart|让人心碎
record-breaking|break a record|打破纪录
heartwarming|warm one's heart|温暖人心
paper-cutting|cut paper|剪纸
paper-making|make paper|造纸
problem-solving|solve problems|解决问题
thought-provoking|provoke thought|引人思考
motion-sensing|sense motion|感知移动
scriptwriter|write scripts|写剧本
eye-catching|catch the eye|吸引目光
load-bearing|bear a load|承重
nerve-racking|rack one's nerves|折磨神经
filmmaker|make films|拍电影
language-teaching|teach languages|教语言
ground-covering|cover the ground|覆盖地面
groundbreaking|break ground|破土
goalkeeper|keep the goal|守球门
lawmaker|make laws|立法
lawmaking|make laws|立法
woodcutter|cut wood|砍木头
woodworker|work wood|加工木头
firefighter|fight fires|救火
firefighting|fight fires|救火
cheerleader|lead cheers|带头欢呼
troublemaker|make trouble|惹麻烦
troubleshooting|shoot trouble|“打掉”故障
robot-building|build robots|造机器人
prize-winning|win a prize|获奖
screwdriver|drive screws|拧螺丝
gravity-defying|defy gravity|违抗重力
tiebreaker|break a tie|打破平局
award-winning|win an award|获奖
risk-taking|take risks|冒险
tower-building|build towers|造塔、盖高楼
gatekeeper|keep the gate|看门
shopkeeper|keep a shop|开店、看店
breathtaking|take one's breath away|让人一下子喘不过气
foot-tapping|tap one's foot|用脚打拍子
homeowner|own a home|拥有住房
money-making|make money|赚钱
brick-maker|make bricks|做砖
painstaking|take pains|下苦功
bowl-washing|wash bowls|洗碗
code-breaking|break a code|破译密码
automaker|make autos|造汽车
songwriter|write songs|写歌
songwriting|write songs|写歌
glass-blower|blow glass|吹玻璃
glass-blowing|blow glass|吹玻璃
air-conditioner|condition the air|调节空气
air-conditioned|condition the air|调节空气
moneylender|lend money|放债
sea-crossing|cross the sea|横渡大海
hairdressing|dress hair|打理头发
hairdresser|dress hair|打理头发
fortune-telling|tell fortunes|算命
beer-maker|make beer|酿啤酒
tomb-sweeping|sweep tombs|扫墓
mosquito-repelling|repel mosquitoes|把蚊子赶走
zookeeper|keep a zoo|看管动物园
dishwasher|wash dishes|洗碗碟
blockbuster|bust a block|炸平一个街区
carpooling|pool cars|几个人合用汽车
tear-jerking|jerk tears|把眼泪“拽”出来
anteater|eat ants|吃蚂蚁
rock-eater|eat rocks|吃岩石
tongue-twister|twist the tongue|把舌头拧住
newscaster|cast news|播新闻
nutcracker|crack nuts|把坚果夹裂
fundraiser|raise funds|筹集资金
skyscraper|scrape the sky|刮擦天空
lifeguard|guard lives|守护生命
cowherd|herd cows|放牛
windbreak|break the wind|挡住风
shot-put|put the shot|推铅球
role-play|play a role|扮演角色
haircut|cut hair|剪头发
chimney-sweep|sweep chimneys|扫烟囱
climate-control|control the climate|控制车里、屋里的小气候
time-management|manage time|管理时间
proofread|read proofs|看校样
troubleshoot|shoot trouble|“打掉”故障
kidnap|nab a kid|抢走小孩
career-exploration|explore careers|探索职业
power-supply|supply power|供电
eldercare|care for the elderly|照料老人
childcare|care for children|照看孩子
healthcare|care for health|照料健康
gameplay|play a game|玩游戏
# H03 用什么、在哪儿、由谁提前
sword-fighting|fight with swords|用剑打斗
skydiving|dive in the sky|在天上“潜水”
scuba-diving|dive with scuba|背着水肺潜水
handwriting|write by hand|用手写
typewriter|write with type|用铅字写字
typewrite|write with type|用铅字写字
city-driving|drive in the city|在城里开车
water-living|live in water|生活在水里
windsurfing|surf with the wind|借风冲浪
windsurf|surf with the wind|借风冲浪
crowdfunding|be funded by a crowd|由一大群人出钱
concertgoer|go to concerts|去听音乐会
theatergoer|go to the theater|去看戏
grasshopper|hop in the grass|在草里蹦
spacewalk|walk in space|在太空里走
time-travel|travel in time|在时间里旅行
wordplay|play with words|拿词语来玩
# H04 名词 + 过去分词
typewritten|written with a typewriter|用打字机打出来的
handmade|made by hand|用手做的
handwritten|written by hand|用手写的
handheld|held in the hand|拿在手里的
action-packed|packed with action|塞满动作场面的
nature-based|based on nature|以大自然为基础的
tech-driven|driven by technology|被技术推着走的
cursive-written|written in cursive|用连笔写的
heartbroken|one's heart is broken|心碎了
heart-broken|one's heart is broken|心碎了
heartfelt|felt in the heart|从心里感受到的
human-made|made by humans|由人做出来的
human-led|led by humans|由人带领的
voice-activated|activated by voice|用声音启动的
voice-controlled|controlled by voice|用声音控制的
factory-farmed|farmed like in a factory|像在工厂里一样养殖的
curiosity-driven|driven by curiosity|被好奇心推动的
space-based|based in space|设在太空的
windswept|swept by the wind|被风吹扫的
time-tested|tested by time|经过时间检验的
home-cooked|cooked at home|在家里做的
hand-painted|painted by hand|用手画的
custom-made|made for a customer|为顾客专门做的
sunlit|lit by the sun|被阳光照亮的
solar-powered|powered by solar energy|用太阳能驱动的
handprinted|printed by hand|用手印的
star-centered|centered on stars|以明星为中心的
internet-connected|connected to the internet|连着互联网的
hand-woven|woven by hand|用手织的
family-owned|owned by a family|归一个家族所有的
color-coded|coded with colors|用颜色编码的
frost-covered|covered with frost|被霜盖住的
homemade|made at home|在家里做的
moonlit|lit by the moon|被月光照亮的
airborne|borne by the air|被空气托着的
battery-powered|powered by batteries|用电池驱动的
photosynthesis-enhanced|enhanced in photosynthesis|光合作用被增强了的
mud-covered|covered with mud|被泥盖住的
gasoline-powered|powered by gasoline|用汽油驱动的
snow-covered|covered with snow|被雪盖住的
snow-dusted|dusted with snow|撒了一层雪的
trash-covered|covered with trash|被垃圾盖满的
leather-bound|bound in leather|用皮革装订的
man-made|made by man|由人做出来的
tech-enhanced|enhanced by technology|被科技增强了的
VR-based|based on VR|以 VR 为基础的
yogurt-based|based on yogurt|以酸奶为底的
dot-based|based on dots|以点为基础的
jewel-trimmed|trimmed with jewels|用宝石镶边的
hand-knitted|knitted by hand|用手织的
algae-made|made from algae|用藻类做的
AI-powered|powered by AI|由 AI 驱动的
AI-generated|generated by AI|由 AI 生成的
AI-assisted|assisted by AI|由 AI 协助的
AI-guided|guided by AI|由 AI 引导的
AI-predicted|predicted by AI|由 AI 预测的
pavement-embedded|embedded in the pavement|嵌在路面里的
grease-stained|stained with grease|被油弄脏的
paint-smeared|smeared with paint|被颜料抹过的
3D-printed|printed in 3D|用 3D 打印出来的
# H05 副词提前
well-organized|organize well|组织得好
long-lasting|last long|持续很久
well-kept|keep well|照管得好
best-kept|keep best|保守得最好
well-rounded|round well|磨得很圆
hard-working|work hard|努力工作
hardworking|work hard|努力工作
hardest-working|work hardest|工作最努力
well-known|know well|很了解
best-known|know best|最了解
backwards-facing|face backwards|朝后
professional-looking|look professional|看起来专业
kind-looking|look kind|看上去和善
well-prepared|prepare well|准备得好
remotely-operated|operate remotely|远程操作
well-paid|pay well|报酬给得好
far-reaching|reach far|伸得很远
well-behaved|behave well|表现得好
ancient-seeming|seem ancient|看起来古老
well-developed|develop well|发展得好
well-educated|educate well|教育得好
tired-looking|look tired|看起来很累
quick-drying|dry quickly|干得快
easy-going|go easily|走得从容
strange-looking|look strange|看起来奇怪
low-lying|lie low|低低地躺着
best-selling|sell best|卖得最好
best-preserved|preserve best|保存得最好
quick-learning|learn quickly|学得快
quick-thinking|think quickly|想得快
tough-looking|look tough|看上去不好惹
salty-tasting|taste salty|尝起来咸
tight-fitting|fit tightly|贴得紧
foolish-looking|look foolish|看起来傻
sweet-smelling|smell sweet|闻起来香
widespread|spread widely|散得很广
broadcast|cast broadly|撒得很宽
well-shaped|shape well|塑得好
well-tempered|temper well|调和得好
ready-made|made ready|做好、备好
# H06 名词 + 形容词
lifelong|as long as life|和一生一样长
worldwide|as wide as the world|和全世界一样广
trustworthy|worthy of trust|值得信任
water-efficient|efficient in using water|用水高效
world-famous|famous in the world|在全世界有名
nationwide|as wide as the nation|和全国一样广
car-free|free of cars|没有汽车
energy-efficient|efficient in using energy|用能高效
cost-effective|effective for the cost|花的钱少、效果好
touch-sensitive|sensitive to touch|对触碰敏感
period-accurate|accurate for the period|对那个年代来说准确
energy-intensive|intensive in energy use|大量用能
paper-thin|as thin as paper|像纸一样薄
eco-friendly|friendly to the environment|对环境友好
user-friendly|friendly to users|对用户友好
newsworthy|worthy of news|值得上新闻
company-wide|as wide as the company|遍及全公司
seasick|sick from the sea|因为海上颠簸而难受
nutrient-dense|dense in nutrients|营养素密集
nutrient-rich|rich in nutrients|富含营养素
sugar-free|free of sugar|不含糖
silky-smooth|smooth as silk|像丝一样光滑
cancer-free|free of cancer|没有癌症
sky-high|as high as the sky|像天一样高
crystal-clear|clear as crystal|像水晶一样清澈
cruelty-free|free of cruelty|不含虐待
waist-deep|deep up to the waist|深到腰
bird-friendly|friendly to birds|对鸟友好
water-related|related to water|和水有关
dehydration-related|related to dehydration|和脱水有关
job-related|related to the job|和工作有关
career-related|related to careers|和职业有关
math-related|related to math|和数学有关
Christmas-related|related to Christmas|和圣诞节有关
nutrition-balanced|balanced in nutrition|营养上均衡
fire-resistant|resistant to fire|顶得住火
lightning-fast|as fast as lightning|像闪电一样快
waterproof|proof against water|挡得住水
fire-proof|proof against fire|挡得住火
rainproof|proof against rain|挡得住雨
rust-proof|proof against rust|顶得住锈
movie-like|like a movie|像电影一样
human-like|like a human|像人一样
countryside-like|like the countryside|像乡村一样
real-life-like|like real life|像现实生活一样
brush-like|like a brush|像刷子一样
bowl-like|like a bowl|像碗一样
umbrella-like|like an umbrella|像伞一样
eagle-like|like an eagle|像鹰一样
harp-like|like a harp|像竖琴一样
cat-like|like a cat|像猫一样
diamond-like|like a diamond|像钻石一样
dog-like|like a dog|像狗一样
flame-red|as red as flame|像火焰一样红
rose-red|as red as a rose|像玫瑰一样红
peacock-blue|as blue as a peacock's feathers|像孔雀羽毛一样蓝
chestnut-brown|as brown as a chestnut|像栗子一样棕
# H08 动词短语变名词、形容词（短语照写）
make-up|make up|拼凑起来
makeup|make up|拼凑起来
makeover|make over|从头到尾重做一遍
made-up|make up|编造
workout|work out|锻炼
leftover|leave over|剩下
takeoff|take off|起飞
takeout|take out|带出去
comeback|come back|回来
turnaround|turn around|掉过头来
standby|stand by|待命
follow-up|follow up|跟进
stopover|stop over|中途停留
backup|back up|支持、备份
built-in|build in|装进里面
handout|hand out|分发
check-up|check up|检查
check-ups|check up|检查
checkout|check out|结账离开
clean-up|clean up|打扫干净
cleanup|clean up|打扫干净
light-up|light up|亮起来
grown-up|grow up|长大
grown-ups|grow up|长大
growing-up|grow up|长大
runoff|run off|流走
run-down|run down|耗尽、衰败
passer-by|pass by|从旁边走过
passers-by|pass by|从旁边走过
warm-up|warm up|热身
setback|set back|往后推
setup|set up|建立、安排
breakthrough|break through|冲破
worn-out|wear out|穿坏、用坏
cut-up|cut up|切碎
crossover|cross over|越过去
pick-up|pick up|拣起来、接人
pickup|pick up|拣起来、接人
hideout|hide out|躲起来
drawback|draw back|往后拉
dried-up|dry up|干透
layout|lay out|摆开、布置
feedback|feed back|送回去
shake-up|shake up|彻底摇一遍
throw-away|throw away|扔掉
meltdown|melt down|熔化、垮掉
pop-up|pop up|突然冒出来
trade-off|trade off|拿一样换另一样
trade-offs|trade off|拿一样换另一样
tryout|try out|试一试
blackout|black out|全部弄黑
# H09 小词在前
intake|take in|收进来
income|come in|进来
outcome|come out|出来
input|put in|放进去
output|put out|放出去
outbreak|break out|爆发
downpour|pour down|倾泻而下
upcoming|come up|到跟前来
outlook|look out|往外看
outfit|fit out|配齐装备
# H10 介词短语连成一个词
upstairs|up the stairs|顺着楼梯往上
downstairs|down the stairs|顺着楼梯往下
downtown|down to the town|下到城里去
online|on line|在线路上
offline|off line|离开线路
off-stage|off the stage|离开舞台
off-course|off course|偏离航线
off-key|off key|偏离了调
off-ice|off the ice|离开冰面
after-school|after school|放学以后
instead|in stead|在…的位置上
indeed|in deed|在实际行动上
tonight|to night|在这一夜
tomorrow|to morrow|在（第二天）早上
behalf|by half|在…这一边
alongside|along side|沿着侧边
forever|for ever|直到永远
perhaps|per haps|凭运气
nowadays|now a days|在现在这些日子里
percent|per cent|按每一百
# H17 名词、形容词 + 动词 = 动词
hand-wash|wash by hand|用手洗
air-draw|draw in the air|在空中画
deep-fry|fry in deep oil|在深油里炸
stir-fry|fry while stirring|一边翻一边炒
double-check|check twice|查两遍
cross-check|check crosswise|交叉核对
double-click|click twice|点两下
safe-keep|keep safe|稳妥地保管
dive-bombed|bomb while diving|俯冲着轰炸
headbutt|butt with the head|用头撞
whitewash|wash white|刷白
homebake|bake at home|在家烤
slam-dunk|dunk with a slam|砰地一下扣进去
video-called|call by video|用视频打电话
fulfil|fill full|填满
livestreamed|stream live|实况传送
# H18 主语 + 动词
sunrise|the sun rises|太阳升起
sunset|the sun sets|太阳落下
sunshine|the sun shines|太阳照耀
sundown|the sun goes down|太阳下去
earthquake|the earth quakes|大地颤动
heartbeat|the heart beats|心跳动
rainfall|rain falls|雨落下
snowfall|snow falls|雪落下
waterfall|water falls|水落下
snowmelt|snow melts|雪融化
airflow|air flows|空气流动
landslide|land slides|土地滑落
frostbite|frost bites|严寒“咬”人
headache|one's head aches|头疼
stomachache|one's stomach aches|胃疼
toothache|a tooth aches|牙疼
sunstroke|the sun strikes|太阳“击中”人
# H34 self 在前
self-expression|express oneself|表达自己
self-introduction|introduce oneself|介绍自己
self-discipline|discipline oneself|管住自己
self-driving|drive itself|自己开
self-control|control oneself|控制自己
self-belief|believe in oneself|相信自己
self-talk|talk to oneself|对自己说话
self-care|care for oneself|照顾自己
self-centered|centered on oneself|以自己为中心
self-check-out|check out by oneself|自己结账
self-checkout|check out by oneself|自己结账
self-coached|coached by oneself|由自己当教练
self-confidence|be confident in oneself|对自己有信心
self-defense|defend oneself|保护自己
self-disclosure|disclose oneself|把自己的事说出来
self-doubt|doubt oneself|怀疑自己
self-encouragement|encourage oneself|给自己鼓劲
self-esteem|esteem oneself|看重自己
self-important|think oneself important|自以为重要
self-improvement|improve oneself|改进自己
self-interest|one's own interest|自己的利益
self-publish|publish by oneself|自己出版
self-published|published by oneself|由自己出版的
self-reliance|rely on oneself|依靠自己
self-respect|respect oneself|尊重自己
self-sustaining|sustain itself|自己维持自己
'''

PH = {}
for line in RAW.strip().split('\n'):
    if not line.strip() or line.startswith('#'):
        continue
    w, p, z = line.split('|')
    PH[w] = (p, z)

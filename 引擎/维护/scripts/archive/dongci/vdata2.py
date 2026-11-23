"""动词变化形式轮：第二批（paid 起）"""
from vhelp import PT, PPT, PPI, AT, AI, GVS

E = {}

E['paid'] = dict(
 l1='pay（付钱）→ paid =“付了；被付了钱的”',
 st=[PT('付了'), PPT('付', '已经付了；被付钱'), AT('付', '已付的；有报酬的、（假期）带薪的（paid leave 带薪假）')],
 P="""【字母变化】paied（中古英语）→ paid（英语）
① pay 是约 1200 年从古法语 paier 借来的，按英语的规则变化，过去式、过去分词加 -ed，中古英语写成 paied、payed。
② 词尾 -ed 里的 e 不念，拼写也省掉，y、i 统一写成 i：paied → paid（同 lay → laid、say → said）；play 却一直写规则的 played，只能单记。""")

E['done'] = dict(
 l1='do（做）→ done =“已经做了的”',
 st=[PPT('做', '已经做完了；被做（It\'s done. 做完了）'), AT('做完', '完成的、结束的'),
     '→ 饭菜做到了火候 →（食物）熟了的', '→ 人自己也“完了”：力气用光、耐心用尽 →（口）累坏了、受够了',
     '→ 讨价还价到这儿，事情算是“做成了” →（答语）成交！一言为定！'],
 P="""【字母变化】gedon（古英语）→ ydon（中古英语）→ done（英语）
① 古英语 dōn“做”的过去分词 gedōn：前面加 ge-，元音是长音 ō，末尾的 n 是过去分词的词尾。
② 到中古英语，ge- 念轻，写成 y-：gedon → ydon（也写 idon、don）。
③ y- 掉了，末尾加上不发音的 e：ydon → done；长音 /oː/ 经元音大推移成了 /uː/，后来又缩短成 /ʌ/（同 blood、flood），读 /dʌn/，和 do /duː/ 分开了。""")

E['redid'] = dict(
 st=[PT('重做了、改做了；重新装修了')],
 P="""redo – redid – redone：redo 里的 do 照 do 变。did 来自古英语 dyde：把词干的 d 重复一次表示过去，是日耳曼语里仅存的这种“重复式”过去式（etymonline）。""")

E['caught'] = dict(
 l1='catch（抓住）→ caught =“抓住了；被抓住的”',
 st=[PT('抓住了、赶上了、染上了'), PPT('抓', '已经抓住了；被抓住、被困住（be caught in the rain 被雨淋了）')],
 P="""【字母变化】caughte（中古英语）→ caught（英语）
① 中古英语 cacchen“追、抓”是从北部古法语 cachier 借来的（见 chase），外来动词本该走规则变化 catched；但它照意思相近的本族动词 lacchen“抓住”（今天的 latch）的过去式 laughte，变出了 caughte（etymonline 说可能如此）。
② 词尾的 e 不念了，去掉；gh 后来也不念了，au 读 /ɔː/：caughte → caught，读 /kɔːt/（同 teach → taught）。""")

E['wore'] = dict(
 l1='wear（穿；磨损）→ wore =“穿了；磨损了”',
 st=[PT('穿了、戴了、留了；磨损了')],
 P="""wear – wore – worn：古英语 werian“穿”本是规则动词（过去式、过去分词都是 wered）；14 世纪照押韵的 bear – bore – born、tear – tore – torn 改成了换元音的强变化，wore 的 o 就是照它们来的（etymonline）。""")

E['worn'] = dict(
 l1='wear（穿；磨损）→ worn =“被穿过的、被磨过的”',
 st=[PPT('穿', '已经穿过了；被穿、被磨'), AT('穿', '磨损的、穿旧的', '：衣服、鞋子被穿久了、磨旧了'),
     '→ 人也像衣服一样被日子“磨”过 → 疲惫的、憔悴的'],
 P="""wear 的过去分词本是规则的 wered（古英语 werian 是规则动词）；14 世纪照押韵的 bear – born、tear – torn 改成 o 再加 -n：worn（etymonline）。""")

E['won'] = dict(
 l1='win（赢）→ won =“赢了；被赢得的”',
 st=[PT('赢了、获胜了；赢得了'), PPT('赢得', '已经赢了；被赢得')],
 P="""【字母变化】wunnen（古英语）→ won（英语）
① 古英语 winnan“苦干、争取”是强变化动词：winnan – wann – wunnen。今天的 won 来自过去分词 wunnen 这一支，后来过去式也改用它，wann 就不用了。
② 词尾 -en 掉了，nn 简化；u 照中古英语的抄写习惯改写成 o（u 挨着 n、m、w 写在一起容易看错，同 son、come、love），读音还是 /ʌ/：wunnen → won，读 /wʌn/。""")

E['held'] = dict(
 l1='hold（拿住；举行）→ held =“拿住了；被举行的”',
 st=[PT('拿住了、握过；举行了'), PPT('举行', '已经举行了；被拿住、被举行'),
     '→ 会议“被举行”，汉语直接说“举行、召开”（The Olympics are held every four years.）→ 举行、召开（见【辨析】）'],
 P="""【字母变化】heold（古英语）→ held（英语）
① 古英语 healdan“握住、保持”是强变化动词：healdan – hēold – healden，过去式把元音换成 ēo（同 feallan – fēoll，就是 fall – fell）。
② ēo 简化成 e，元音变短：heold → held（同 behold → beheld、uphold → upheld）。过去分词原来是 holden，16 世纪起改用 held，holden 只剩在 beholden（欠人情的）这类说法里。""")

E['spent'] = dict(
 l1='spend（花）→ spent =“花了；已经被花掉的”',
 st=[PT('花了；度过了'), PPT('花', '已经花了；被花掉'), AT('花光', '用过的、耗尽的', '：像烧完的火柴、打空的弹壳'),
     '→ 人的力气全花光了 → 精疲力竭的', '→ 势头、影响力都耗光了 → 风光不再的（见【辨析】）'],
 P="""【字母变化】spende（古英语）→ spent（英语）
① 古英语 spendan“花费”（借自拉丁语 expendere）是规则动词，过去式 spende：词干的 d 和过去式的 -de 并成一个。
② 中古英语起，-nd 结尾的动词过去式里的 d 念成清音 t：spende → spent（同 send → sent、lend → lent、bend → bent、wend → went）。""")

E['spun'] = dict(
 l1='spin（纺；转）→ spun =“纺了、转了；被纺成的”',
 st=[PT('纺了；转了'), PPT('纺', '已经纺好了；被纺成'), AT('纺', '纺成的')],
 P="""【字母变化】spunnen（古英语）→ spun（英语）
① 古英语 spinnan“纺线”是强变化动词：spinnan – spann – spunnen，过去分词换成 u 再加 -en。
② 词尾 -en 掉了，nn 简化：spunnen → spun；后来过去式也改用 spun，span 就过时了（同 sting → stung、swing → swung）。""")

E['led'] = dict(
 l1='lead（带领）→ led =“带领了；被带领的”',
 st=[PT('带领了、领先了'), PPT('带领', '已经带领了；被带领'), AT('带领', '（多接在别的词后面）由…主导的、由…带动的（student-led 学生主导的）')],
 P="""【字母变化】ledde（中古英语）→ led（英语）
① 古英语 lǣdan“带领”是规则（弱变化）动词，过去式 lǣdde（词干的 d 加过去式的 -de）；长元音碰上两个 d 变短，中古英语写成 ledde。
② 词尾的 e 不念了，dd 简化成 d：ledde → led（同 feed → fed、speed → sped、bleed → bled）。原形 lead 的长音经元音大推移读 /iː/，led 读短的 /e/。""")

E['heard'] = dict(
 l1='hear（听）→ heard =“听见了；被听见的”',
 st=[PT('听见了'), PPT('听见', '已经听见了；被听见'),
     '→ 早就从别人那里听到过 →（have heard of）听说过、知道（有这么个人、这回事）'],
 P="""【字母变化】herde（中古英语）→ heard（英语）
① 古英语 hīeran / hēran“听”是规则（弱变化）动词，过去式 hīerde / hērde；长元音碰上 r + d 变短，中古英语写成 herde。
② 拼写照 hear 写成 ea，词尾的 e 去掉：herde → heard；元音在 r 前后来变成 /ɜː/（同 her、herd），所以 hear 读 /hɪə/，heard 读 /hɜːd/。""")

E['overheard'] = dict(
 keepsteps=True,
 st=[PT('无意中听到了'), PPT('听到', '已经听到了；被（无意中）听到')],
 P="""overhear – overheard – overheard：overhear 里的 hear 照 hear 变（见 heard）。
【对照】over- 在 overhear 里是“越过界线”，在 overlook 里却是“忽略”：古英语 oferhieran 正好也是“不听”""")

E['rode'] = dict(
 l1='ride（骑）→ rode =“骑了”',
 st=[PT('骑了、乘坐了')],
 P=f"""【字母变化】rad（古英语）→ rood（中古英语）→ rode（英语）
① 古英语 rīdan“骑”是强变化动词，靠换元音表示时态：rīdan – rād – riden；过去式 rād 的 ā 是长音。
② 中古英语里长音 ā 变成长音 o，常双写成 oo：rad → rood（同 wrāt → wrote，名词 rād → road 也是这样变的）。
③ 后来改用“o + 辅音 + 不发音的 e”表示长音 o：rood → rode；{GVS}，读 /rəʊd/。""")

E['ridden'] = dict(
 st=[PPT('骑', '骑过、乘过（have ridden）；被骑'),
     '→ 像马一样被人骑在背上，甩都甩不掉 →（接在名词后）被…压着的、充斥着…的、被…困扰的（guilt-ridden 内疚不已的）'],
 P="""【字母变化】riden（古英语）→ ridden（英语）
① 古英语 rīdan 的过去分词 riden：i 是短的（原形 rīdan 的 ī 是长的），后面加 -en。
② 短 i 后面的 d 双写，表示前面是短元音：riden → ridden；原形 ride 的长 i 经元音大推移读 /aɪ/，ridden 读短 /ɪ/（同 write → written、bite → bitten）。""")

E['met'] = dict(
 l1='meet（碰上）→ met =“碰上了；已经碰上过”',
 st=[PT('遇见了；见了面'), '# 过去分词：跟在 have 后面是“已经见过了”；跟在 be 后面，多说需要、要求“被满足” → 见过、认识（have met）；（需要、要求）被满足（needs are met）'],
 P="""【字母变化】mette（古英语）→ met（英语）
① 古英语 mētan“碰见”是规则（弱变化）动词，过去式在 t 后加 -te：mētte；长元音碰上两个 t 变短（长元音后面辅音一多就容易变短，同 five → fifteen、house → husband、break → breakfast）。
② 词尾的 e 不念了，tt 简化成 t：mette → met（同 feed → fed、lead → led）。原形 meet 的长 ee 经元音大推移读 /iː/，met 读短 /e/。""")

E['drank'] = dict(
 l1='drink（喝）→ drank =“喝了”',
 st=[PT('喝了')],
 P="""【字母变化】dranc（古英语）→ drank（英语）
① 古英语 drincan“喝”是强变化动词：drincan – dranc – druncen，靠换元音表示时态（i → a → u）。
② c 改写成 k（中古英语起 k 的写法普及）：dranc → drank（同 sing – sang – sung、swim – swam – swum）。""")

E['fell'] = dict(
 l1='fall（落下、倒下）→ fell =“落下了、倒下了”',
 st=[PT('落下了、跌倒了；（价格）下降了')],
 P="""【字母变化】feoll（古英语）→ fell（英语）
① 古英语 feallan“落下、倒下”是强变化动词：feallan – fēoll – feallen，过去式把元音换成 ēo（同 healdan – hēold，就是 hold – held）。
② ēo 简化成 e，元音变短：feoll → fell，读 /fel/。""")

E['fallen'] = dict(
 st=[PPI('落下', 'fall', '已经落下了、已经倒下了'), AI('落下', '落下的、倒下的（fallen leaves 落叶）'),
     '→ 在战场上倒下、再没起来 → 阵亡的；（the fallen）阵亡将士', '→ 从高处“掉”下来，在道德上往下落 → 堕落的'],
 P="""【字母变化】feallen（古英语）→ fallen（英语）
① 古英语 feallan 的过去分词 feallen：元音和原形一样，后面加 -en。
② ea 简化成 a：feallen → fallen，-en 一直保留到今天，读 /ˈfɔːlən/。""")

E['hid'] = dict(
 l1='hide（藏、躲）→ hid =“藏了、躲了”',
 st=[PT('藏了、躲了')],
 P="""【字母变化】hidde（中古英语）→ hid（英语）
① 古英语 hȳdan“藏”是规则（弱变化）动词，过去式 hȳdde（词干的 d 加过去式的 -de）；长元音碰上两个 d 变短，中古英语写成 hidde。
② 词尾的 e 不念了，dd 简化成 d：hidde → hid；原形 hide 的长 i 经元音大推移读 /aɪ/，hid 读短 /ɪ/（同 slide → slid）。""")

E['hidden'] = dict(
 st=[PPT('藏', '已经藏好了；被藏起来'), AT('藏', '隐藏的、隐蔽的'), '→ 藏在背后、不让人知道的 → 隐秘的、不为人知的'],
 P="""hide 原是规则动词，过去分词本来也是 hid（has hid 是旧式说法）；后来照 ride – ridden、bite – bitten 这类强变化动词，在 hid 后面加上 -en（d 双写，保住短 i），成了今天的标准形式 hidden。""")

E['sent'] = dict(
 l1='send（送）→ sent =“送了；被送出的”',
 st=[PT('送了、寄了、派了'), PPT('寄', '已经寄出了；被寄出、被派出')],
 P="""【字母变化】sende（古英语）→ sent（英语）
① 古英语 sendan“送、派”是规则（弱变化）动词，过去式 sende：词干的 d 和过去式的 -de 并成一个。
② 约 1200 年起，-nd 结尾的动词过去式里的 d 念成清音 t：sende → sent（同 spend → spent、lend → lent、bend → bent、wend → went）。规则形式 sended 14 世纪晚期也出现过，后来没有流传下来。""")

E['slept'] = dict(
 l1='sleep（睡）→ slept =“睡了；睡过”',
 st=[PT('睡了、睡过'), PPI('睡', 'sleep', '睡过、已经睡了一觉')],
 P="""【字母变化】slepte（中古英语）→ slept（英语）
① 古英语 slǣpan“睡”原是强变化动词（过去式 slēp）；中古英语改走规则的弱变化，过去式在 p 后面加 -te，长元音碰上 p + t 变短，写成 slepte。
② 词尾的 e 不念了：slepte → slept；原形 sleep 的长 ee 经元音大推移读 /iː/，slept 读短 /e/（同 keep → kept、weep → wept、sweep → swept）。""")

E['drew'] = dict(
 l1='draw（拉；画）→ drew =“拉了；画了”',
 st=[PT('拉了、画了、吸引了……（draw 的各个意思都能这样说过去）')],
 P="""draw – drew – drawn：古英语 dragan“拉”是强变化动词：dragan – drōg – dragen。g 在 a、o 后面先念成喉音，后来变成 w 音（dragan → drawen → draw）；中古英语过去式写 drough、drow，后来照 grow → grew、know → knew 这一类写成 drew，读 /druː/。""")

E['drawn'] = dict(
 st=[PPT('拉', '已经拉了、画了；被拉、被画'), AT('拉', '拔出的（剑）；拉上的（窗帘）'),
     '→ 脸上的皮肉像被拉紧、拉薄了 →（脸）憔悴的、紧绷的', '→ 跟着 draw“打平” →（比赛）平局的'],
 P="""【字母变化】dragen（古英语）→ drawen（中古英语）→ drawn（英语）
① 古英语 dragan“拉”的过去分词 dragen：元音和原形一样，后面加 -en。
② g 在 a 后面先念成喉音，再变成 w 音：dragen → drawen（原形 dragan 也这样变成了 draw）。
③ -en 里弱读的 e 掉了，缩成 -n：drawen → drawn，读 /drɔːn/。""")

E['withdrew'] = dict(
 l1='withdraw（撤回）→ withdrew =“撤回了”',
 st=[PT('撤回了、退出了、取了（钱）')],
 P="""withdraw – withdrew – withdrawn：withdraw 里的 draw 照 draw 变（见 drew）；过去分词 withdrawn 还作形容词“孤僻的、内向的”。""")

E['fought'] = dict(
 l1='fight（打）→ fought =“打了；被打过的”',
 st=[PT('打过、战斗过、争取过'), '# 过去分词：跟在 have 后面是“已经打过了”；跟在 be 后面，说一场仗、一场比赛是在哪儿、怎么打的（The battle was fought in 1066.） → 已经打过了；（仗、比赛）打完了（a hard-fought game 打得很激烈的比赛）'],
 P="""【字母变化】fohten（古英语）→ foughten（中古英语）→ fought（英语）
① 古英语 feohtan“战斗”是强变化动词：feohtan – feaht – fohten。今天的 fought 来自过去分词 fohten 这一支，后来过去式也改用它。
② h 是喉音，中古英语写成 gh；o 写成 ou：fohten → foughten（这个形式 18 世纪起才古旧）。
③ 词尾 -en 掉了：foughten → fought；gh 不念了，ou 读 /ɔː/，读 /fɔːt/（同 thought、brought，来历各不相同）。""")

E['laid'] = dict(
 l1='lay（放）→ laid =“放了；被放下的”',
 st=[PT('放了、铺了；下（蛋）了'), PPT('放', '已经放好了；被放下、被铺设'), AT('放', '铺好的、摆好的'),
     '→ 身子往后一靠、放松地躺着 →（laid-back，口语）悠闲的、松弛的'],
 P="""【字母变化】leide（中古英语）→ laid（英语）
① 古英语 lecgan“放”是规则（弱变化）动词，过去式 legde：g 跟在元音后面念得像 y，中古英语写成 leide、layde（同 say → said）。
② 拼写照 lay 改成 ai，词尾的 e 去掉：leide → laid，读 /leɪd/。""")

E['proven'] = dict(
 st=[PPT('证明', '已经证明了；被证明（has been proven 已被证明）'),
     '→ 先是苏格兰的法律用语（1650s）：not proven 是“罪证不足”的裁决 → 未经证明（的）',
     AT('证明', '已证明的、行之有效的', '：经过检验、证明可靠')],
 P="""prove 是从古法语 prover 借来的规则动词，标准过去分词是 proved；proven 是另一种照强变化动词加 -en 的过去分词（同 ridden、written），先用在苏格兰的法律用语里（1650s），后来进入标准英语，多作形容词。prove 已有词尾 e，只加 n。""")

E['rose'] = dict(
 l1='rise（起来）→ rose =“起来了”',
 st=[PT('升起了；上涨了；起身了')],
 P=f"""【字母变化】ras（古英语）→ roos（中古英语）→ rose（英语）
① 古英语 rīsan“起来”是强变化动词：rīsan – rās – risen；过去式 rās 的 ā 是长音。
② 中古英语里长音 ā 变成长音 o，常双写成 oo：ras → roos（同 stān → stone、bān → bone、hām → home）。
③ 后来改用“o + 辅音 + 不发音的 e”表示长音 o：roos → rose；{GVS}，读 /rəʊz/。""")

E['risen'] = dict(
 st=[PPI('升起', 'rise', '（已经）升起、上涨'), AI('起来', '（宗教）复活的', '：死后又“起来”了')],
 P="""古英语 rīsan – rās – risen：过去分词就是 risen，i 是短的，后面加 -en；原形 rise 的长 i 经元音大推移读 /aɪ/，risen 的短 i 没变，读 /ˈrɪzn/（同 drive → driven、ride → ridden）。""")

E['arose'] = dict(
 l1='arise（出现）→ arose =“出现了”',
 st=[PT('出现了、发生了')],
 P="""arise – arose – arisen：arise 里的 rise 照 rise 变（见 rose）。""")

E['sped'] = dict(
 l1='speed（疾驰）→ sped =“疾驰了”',
 st=[PT('疾驰了、飞快地驶过'), PPI('疾驰', 'speed', '已经驶过了')],
 P="""【字母变化】spedde（古英语）→ sped（英语）
① 古英语 spēdan“成功、兴旺”是规则（弱变化）动词，过去式 spēdde（词干的 d 加过去式的 -de）；长元音碰上两个 d 变短。
② 词尾的 e 不念了，dd 简化成 d：spedde → sped（同 feed → fed、lead → led）；规则的 speeded 也有人用。""")

E['dealt'] = dict(
 l1='deal（分发；处理）→ dealt =“分了；被处理的”',
 st=[PT('分发了、发了（牌）；处理了'), PPT('处理', '已经处理了；被分发、被处理（be dealt with）')],
 P="""【字母变化】delte（中古英语）→ dealt（英语）
① 古英语 dǣlan“分”是规则（弱变化）动词，过去式 dǣlde；长元音碰上 l + d 变短，词尾在 l 后面念成清音，中古英语写成 delte（同 feel → felt）。
② 拼写照 deal 写成 ea，词尾的 e 去掉：delte → dealt；读音还是短的 /delt/。""")

E['driven'] = dict(
 l1='drive（驱赶、推动）→ driven =“被驱赶的、被推动的”',
 st=[PPT('驾驶', '已经开过、驱赶过；被驾驶、被驱动'), AT('推动', '（接在名词后）…驱动的（solar-driven 太阳能驱动的）'),
     '→ 人被心里的目标推着走、停不下来 →（形）有强烈内在动力的、拼命的', '→ 雪被风“赶”到一处 →（雪）被风吹积的'],
 P="""【字母变化】drifen（古英语）→ driven（英语）
① 古英语 drīfan“驱赶”是强变化动词：drīfan – drāf – drifen，过去分词的 i 是短的，后面加 -en。
② f 夹在两个元音中间念 v，后来就写成 v：drifen → driven；原形 drive 的长 i 经元音大推移读 /aɪ/，driven 读短 /ɪ/（同 ride → ridden）。""")

E['drove'] = dict(
 l1='drive（驱赶；开车）→ drove =“赶了；开了”',
 st=[PT('开（车）了；赶了；驱使了')],
 P=f"""【字母变化】draf（古英语）→ drof（中古英语）→ drove（英语）
① 古英语 drīfan“驱赶”是强变化动词：drīfan – drāf – drifen；过去式 drāf 的 ā 是长音。
② 中古英语里长音 ā 变成长音 o：draf → drof（同 rād → rode、wrāt → wrote）。
③ f 念成 v，英语词尾不写 v，后面加个不发音的 e（同时表示 o 读长音）：drof → drove；{GVS}，读 /drəʊv/。""")

E['smelt'] = dict(
 l1='smell（闻）→ smelt =“闻了、闻到了”',
 st=[PT('闻了、闻到了；发出了…的气味'), PPT('闻到', '（英式）已经闻到了；被闻到')],
 P="""smell 是规则动词，过去式、过去分词本来都加 -ed；英式英语里一批以 l、n、m 结尾的动词，-ed 常读成清音 /t/，拼写也就照读音写成 t（smell → smelt、spell → spelt、spill → spilt、learn → learnt、dream → dreamt），美式多用规则的 smelled。""")

E['flew'] = dict(
 l1='fly（飞）→ flew =“飞了”',
 st=[PT('飞了；坐飞机去了')],
 P="""fly – flew – flown：古英语 flēogan“飞”是强变化动词：flēogan – flēag – flogen。中古英语过去式写 fleigh、flew 等好几种，后来定成 flew（同 blow – blew、grow – grew 这一类），过去分词 flogen 后来变成 flown。""")

E['fled'] = dict(
 l1='flee（逃）→ fled =“逃了”',
 st=[PT('逃了、逃离了'), '# 过去分词：跟在 have 后面，说“已经逃了” → 已经逃走了'],
 P="""【字母变化】fledde（中古英语）→ fled（英语）
① 古英语 flēon“逃”原是强变化动词（过去式 flēah，过去分词 flogen）；中古英语受北欧语影响，改走规则的弱变化，过去式写成 fledde（长元音碰上 dd 变短）。
② 词尾的 e 不念了，dd 简化成 d：fledde → fled（同 feed → fed、lead → led）。""")

E['sold'] = dict(
 l1='sell（卖）→ sold =“卖了；被卖掉的”',
 st=[PT('卖了'), PPT('卖', '已经卖了；被卖掉'), AT('卖', '已售出的；（be sold out）卖光、售罄'),
     '→ 拍卖师一落槌，东西就算卖出去了 →（拍卖时喊）成交',
     '→ 一个想法“卖”给了你，你也买了账 →（口语）被说服的、对…深信不疑'],
 P="""【字母变化】sealde（古英语）→ solde（中古英语）→ sold（英语）
① 古英语 sellan“给、卖”是规则（弱变化）动词，过去式 sealde。现在时的 e 是 a 受后面 -j- 音影响变来的（*saljan → sellan，同 tell），过去式没有这个 -j-，保留了 a（写成 ea）。
② a 在 ld 前面拉长，后来变成长音 o（同古英语 ald → old）：sealde → solde。
③ 词尾的 e 不念了，去掉：solde → sold，读 /səʊld/（同 tell → told）。""")

E['fed'] = dict(
 l1='feed（喂）→ fed =“喂了；被喂的”',
 st=[PT('喂了'), PPT('喂', '已经喂了；被喂'), AT('喂', '喂过的；吃得好的、养得胖的'),
     '→ 牲口被喂得饱饱的，再喂就腻了 →（fed up，1900 年的英国俚语）厌烦、受够了'],
 P="""【字母变化】fedde（古英语）→ fed（英语）
① 古英语 fēdan“喂”是规则（弱变化）动词，过去式 fēdde（词干的 d 加过去式的 -de）；长元音碰上两个 d 变短。
② 词尾的 e 不念了，dd 简化成 d：fedde → fed（同 lead → led、meet → met、bleed → bled）。""")

E['bought'] = dict(
 l1='buy（买）→ bought =“买了；被买来的”',
 st=[PT('买了'), PPT('买', '已经买了；被买'), AT('买', '（美式口语，1912 年起）商店买的（store-bought）', '：从店里买来、不是自家做的')],
 P="""【字母变化】bohte（古英语）→ boughte（中古英语）→ bought（英语）
① 古英语 bycgan“买”是规则（弱变化）动词，过去式 bohte：词干里的 g 碰上过去式的 -te，念成喉音 h。现在时的 y 是元音受后面 -j- 音影响变来的，过去式没有，保留了 o。
② 中古英语用 gh 写这个喉音，o 写成 ou：bohte → boughte。
③ 词尾的 e 不念了；gh 后来也不念了，ou 读 /ɔː/：boughte → bought（同 brought、thought、sought）。""")

E['shone'] = dict(
 l1='shine（发光）→ shone =“发过光了”',
 st=[PT('照耀了、发光了'), PPI('照耀', 'shine', '已经照耀过')],
 P="""【字母变化】scan（古英语）→ shoon（中古英语）→ shone（英语）
① 古英语 scīnan“发光”是强变化动词：scīnan – scān – scinen（sc 念 sh）；过去式 scān 的 ā 是长音。
② sc 改写成 sh，长音 ā 变成长音 o，常双写成 oo：scan → shoon（同 rād → rode、wrāt → wrote）。
③ 后来改用“o + 辅音 + 不发音的 e”：shoon → shone；后来元音在英式里变短，读 /ʃɒn/，美式读 /ʃoʊn/。过去分词 scinen 后来也改用 shone。""")

E['wove'] = dict(
 l1='weave（织）→ wove =“织了”',
 st=[PT('织了、编了'), '（作“在…中穿行”讲时，过去式多用规则的 weaved，见 weave 的【辨析】）'],
 P="""【字母变化】wave（中古英语）→ wove（英语）
① 古英语 wefan“织”是强变化动词：wefan – wæf – wefen；f 夹在元音中间念 v，过去式中古英语写成 wave。
② 中古英语里过去式改成 o：wave → wove（etymonline；同 speak → spoke、steal → stole 这一类的 o），读 /wəʊv/。""")

E['woven'] = dict(
 l1='weave（织）→ woven =“被织成的”',
 st=[PPT('织', '已经织好了；被织成'), AT('织', '织成的、编织的'),
     '→ 许多线索像经纬一样交织在一起 →（比喻）交织在一起的、结构紧密的'],
 P="""【字母变化】wefen（古英语）→ woven（英语）
① 古英语 wefan 的过去分词 wefen：元音和原形一样，后面加 -en。
② 后来照过去式 wove 改成 o，f 夹在元音中间念 v，写成 v：wefen → woven，读 /ˈwəʊvn/（同 speak → spoken、steal → stolen）。""")

E['shook'] = dict(
 l1='shake（摇、抖）→ shook =“摇过了、抖过了”',
 st=[PT('摇了、抖了；握了（手）'),
     '→ 被摇过、晃过，心还没定下来 →（口）（情绪上）受了惊扰的；（all shook up）心慌意乱、激动不已'],
 P=f"""【字母变化】scoc（古英语）→ shook（英语）
① 古英语 sceacan“摇”是强变化动词：sceacan – scōc – scacen（sc 念 sh），过去式靠把 a 换成长音 o 表示“过去”（同 take → took）。
② sc 改写成 sh，长音 o 写成 oo，c 改写成 k：scoc → shook；{GVS}，/oː/ 成了 /uː/，后来又缩短成 /ʊ/，读 /ʃʊk/。""")

E['stuck'] = dict(
 l1='stick（扎住、粘住）→ stuck =“扎住了；被粘住了”',
 st=[PT('扎了、粘住了；卡住了'), PPT('粘', '已经粘上了；被粘住、被卡住'),
     AT('卡住', '卡住的；困住的', '：车轮陷进泥里，越使劲越出不来'),
     '→ 想一道题，想到一半“卡”住了 →（被问题）难住的', '→ 被一样东西“粘”上，甩也甩不掉 →（be stuck with）甩不掉、只好接受'],
 P="""stick 原是规则动词（古英语 stician – sticode），规则的 sticked 一直用到 17 世纪；stuck 是近代早期才出现的不规则形式，一般认为是受意思相近的强变化动词（如 steek“刺”）影响，元音换成 u（同 dig → dug、strike → struck、sting → stung）。今天不说 sticked。""")

E['threw'] = dict(
 l1='throw（扔）→ threw =“扔了”',
 st=[PT('扔了、投了')],
 P="""【字母变化】threow（古英语）→ threw（英语）
① 古英语 þrāwan“扭、转”（þ 就是 th）是强变化动词：þrāwan – þrēow – þrāwen，过去式把元音换成 ēo。
② ēo 简化，写成 ew：threow → threw，读 /θruː/（同 know → knew、grow → grew、blow → blew）。""")

E['thrown'] = dict(
 st=[PPT('扔', '已经扔了；被扔、被甩下来（be thrown from a horse 被马甩下来）'),
     '→ 说丝线时还留着 throw 最早的“扭、转” → 捻过的（见【辨析】）'],
 P="""【字母变化】thrawen（古英语）→ throwen（中古英语）→ thrown（英语）
① 古英语 þrāwan 的过去分词 þrāwen（也写 geþrāwen）：元音和原形一样是长音 ā，后面加 -en。
② 长音 ā 到中古英语变成长音 o，写成 ow：thrawen → throwen（同 cnāwen → known）。
③ -en 里弱读的 e 掉了，缩成 -n：throwen → thrown，读 /θrəʊn/（同 grown、known、blown）。""")

E['burnt'] = dict(
 st=[PT('烧了、烧伤了'), PPT('烧', '已经烧了；被烧'), AT('烧', '烧焦的、烧坏的', '：火候过了头')],
 P="""burn 的过去式、过去分词按规则写 burned；-ed 跟在 n 后面常读成清音 /t/，英式就照读音写成 burnt（同 learnt、spelt、smelt、dreamt）。读音也不同：burnt 读 /t/，burned 多读 /d/。古英语里“烧”有 byrnan、bærnan 两个动词，后来合成了 burn。""")

E['dug'] = dict(
 l1='dig（挖）→ dug =“挖了；被挖的”',
 st=[PT('挖了'), PPT('挖', '已经挖了；被挖出来'),
     '→ 加上 out，dug-out 就是“挖出来的”东西：一整根树干挖空做成的船 → 独木舟',
     '→ 往地下挖出来的掩体、球场边往下挖低的座位区 → 防空壕；球员席'],
 P="""dig 原是规则动词（过去式 digged，钦定本《圣经》里还常见）；强变化的 dug 16 世纪才出现，照 sting → stung、cling → clung 这类把元音换成 u，etymonline 说它“不合词源”。""")

E['hung'] = dict(
 l1='hang（挂）→ hung =“挂了；被挂着的”',
 st=[PT('挂了'), PPT('挂', '已经挂好了；被挂着'),
     '→ 陪审团的意见像被挂在半空、落不了地 →（a hung jury）意见僵持、做不出裁决的陪审团',
     '→ 心思一直挂在某件事上放不下 →（口，be hung up on）对…念念不忘'],
 P="""古英语有两个“挂”：强变化的 hōn（过去式 hēng，过去分词 hangen，“把…挂起来”）和规则的 hangian（过去式 hangode，“挂着”），后来合成了 hang。hung 是 16 世纪英格兰北方方言里兴起的过去分词，元音换成 u（同 sting → stung、swing → swung），后来过去式也用它；法律语言比较保守，说绞刑时一直沿用规则的 hanged。""")

E['struck'] = dict(
 l1='strike（打、击）→ struck =“打了；被打中的”',
 st=[PT('打了、击中了；（钟）敲了'), PPT('打', '已经打了；被打中、被击中'),
     '→ 心被一件事“击中” →（be struck by）被…打动、对…印象很深',
     '→ 接在别的词后面 → 被…击中的、着了迷的（awestruck 惊呆了的，见【语法】）'],
 P="""古英语 strīcan“轻轻擦过”是强变化动词：strīcan – strāc – stricen。中古英语过去式写 strak、strook，后来定成 struck，过去分词也用它（u 的来历词典说法不一）；老过去分词 stricken 留下来作形容词“遭受（打击）的”（grief-stricken 悲痛欲绝的）。""")

E['torn'] = dict(
 l1='tear（撕）→ torn =“被撕了的”',
 st=[PPT('撕', '已经撕了；被撕破'), AT('撕', '撕破的、扯破的'),
     '→ 心被两头同时往外扯 →（be torn between）左右为难、内心挣扎',
     '→ 一个地方被战争撕得七零八落 →（war-torn）饱受战争摧残的'],
 P="""【字母变化】toren（古英语）→ torn（英语）
① 古英语 teran“撕”是强变化动词：teran – tær – toren，过去分词换成 o 再加 -en。
② -en 前面那个弱读的 e 在 r 后面掉了：toren → torn，读 /tɔːn/（同 bear → born、swear → sworn）。""")

E['tore'] = dict(
 l1='tear（撕）→ tore =“撕了”',
 st=[PT('撕了、扯了')],
 P="""【字母变化】tare（中古英语）→ tore（英语）
① 古英语 teran“撕”是强变化动词：teran – tær – toren，过去式 tær 中古英语写成 tare。
② 后来照过去分词 toren、torn 的 o 改成 tore：tare → tore，读 /tɔː/（同 bear → bore）。""")

E['swam'] = dict(
 l1='swim（游）→ swam =“游了”',
 st=[PT('游了、游过')],
 P="""【字母变化】swamm（古英语）→ swam（英语）
① 古英语 swimman“游”是强变化动词：swimman – swamm – swummen，靠换元音表示时态（i → a → u）。
② 词尾双写的 mm 简化成 m：swamm → swam（同 sing – sang – sung、drink – drank – drunk）。""")

E['ate'] = dict(
 l1='eat（吃）→ ate =“吃了”',
 st=[PT('吃了')],
 P="""eat – ate – eaten：古英语 etan“吃”是强变化动词：etan – ǣt – eten，过去式把元音换成长音 ǣ。中古英语过去式写 et、eet、at、ate 好几种：英式读 /et/ 来自 et 这一支，今天的拼写 ate 和美式读音 /eɪt/ 来自 ate 这一支。""")

E['eaten'] = dict(
 st=[PPT('吃', '吃过、已经吃了；被吃'), AT('吃', '被…吃了的、被…蛀了的（moth-eaten 被虫蛀了的）')],
 P="""【字母变化】eten（古英语）→ eaten（英语）
① 古英语 etan“吃”的过去分词 eten：元音和原形一样，后面加 -en。
② 原形的 e 后来读长音，写成 ea（eat），过去分词也照原形写成 ea：eten → eaten，读 /ˈiːtn/。""")

E['sown'] = dict(
 st=[PPT('播', '已经播下；被播下（The seeds were sown.）'), AT('播', '播了种的')],
 P="""【字母变化】sawen（古英语）→ sowen（中古英语）→ sown（英语）
① 古英语 sāwan“播种”是强变化动词：sāwan – sēow – sāwen，过去分词元音和原形一样，后面加 -en。
② 长音 ā 到中古英语变成长音 o，写成 ow：sawen → sowen（同 cnāwen → known）。
③ -en 里弱读的 e 掉了：sowen → sown，读 /səʊn/。过去式后来改成规则的 sowed，过去分词 sown、sowed 都用。""")

E['frozen'] = dict(
 l1='freeze（冻）→ frozen =“已经冻住了的”',
 st=[PPT('冻', '已经冻住了；被冻住、被冻结'), AT('冻', '冻住的、结冰的；冷冻的（frozen food 冷冻食品）'),
     '→ 人冷到身体发僵 → 冻僵的；吓得像冻住一样 → 吓呆的',
     '→ 钱、账户被“冻”住、不能动 →（1922）（资产、账户）被冻结的'],
 P="""【字母变化】froren（古英语）→ frozen（英语）
① 古英语 frēosan“结冰”是强变化动词：frēosan – frēas – froren；过去分词里词干的 s 变成了 r（同 was / were 的 s / r 交替，chosen 原来也是 coren）。
② 后来照原形 freeze 把 r 拉回成 z 音：froren → frozen，-en 不变（同 choose → chosen）。""")

E['froze'] = dict(
 l1='freeze（冻）→ froze =“冻住了”',
 st=[PT('结冰了、冻住了；（人）一下子僵住了')],
 P="""freeze – froze – frozen：古英语 frēosan“结冰”是强变化动词：frēosan – frēas – froren。中古英语过去式写 frees、fres，后来照过去分词 frozen 的 o 改成 froze（同 choose → chose），读 /frəʊz/。""")

E['sang'] = dict(
 l1='sing（唱）→ sang =“唱了”',
 st=[PT('唱了')],
 P="""sing – sang – sung：古英语 singan“唱”是强变化动词：singan – sang – sungen，不加 -ed，靠把元音 i 换成 a 表示过去（同 drink → drank、swim → swam）。过去式 sang 的写法从古英语到今天没变。""")

E['sung'] = dict(
 l1='sing（唱）→ sung =“被唱的；已经唱了”',
 st=[PPT('唱', '唱过（have sung）；被唱'), AT('唱', '唱出来的（不是念出来的）')],
 P="""【字母变化】sungen（古英语）→ sung（英语）
① 古英语 singan 的过去分词 sungen：元音换成 u，后面加 -en。
② 词尾 -en 掉了：sungen → sung（同 begin → begun、drink → drunk）。""")

E['blew'] = dict(
 l1='blow（吹）→ blew =“吹了”',
 st=[PT('吹了、刮了')],
 P="""【字母变化】bleow（古英语）→ blew（英语）
① 古英语 blāwan“吹”是强变化动词：blāwan – blēow – blāwen，过去式把元音换成 ēo。
② ēo 简化，写成 ew：bleow → blew，读 /bluː/（同 grow → grew、know → knew、throw → threw）。""")

E['blown'] = dict(
 l1='blow（吹）→ blown =“被吹的；已经吹了”',
 st=[PPT('吹', '吹过、已经刮过；被吹'), AT('吹', '（保险丝）烧断的', '：被吹得胀破了'),
     '（full-blown“全面的”里的 blown 原是另一个动词“开花”，见【辨析】）'],
 P="""【字母变化】blawen（古英语）→ blowen（中古英语）→ blown（英语）
① 古英语 blāwan 的过去分词 blāwen：元音和原形一样是长音 ā，后面加 -en。
② 长音 ā 到中古英语变成长音 o，写成 ow：blawen → blowen（同 cnāwen → known）。
③ -en 里弱读的 e 掉了：blowen → blown，读 /bləʊn/（同 grown、thrown、known）。""")

E['rang'] = dict(
 l1='ring（响）→ rang =“响了”',
 st=[PT('（铃、电话）响了；打过电话')],
 P="""ring“（铃）响”原是规则动词（古英语 hringan – hringde）；中古英语时照押韵的 sing – sang – sung 变出了 rang、rung（i → a → u）。""")

E['rung'] = dict(
 l1='ring（响；打电话）→ rung =“已经响过；已经打过电话”',
 st=[PPT('敲响', '已经响过、已经打过电话；被敲响'), '（梯子的横档也叫 rung，是另一个词，见音变栏）'],
 P="""ring“（铃）响”原是规则动词（古英语 hringan – hringde）；中古英语时照押韵的 sing – sang – sung 变出了 rang、rung，过去分词 rung 的 u 就是照 sung 来的。""")

E['shot'] = dict(
 l1='shoot（射）→ shot =“射了；被射中的；射出去的那一下”',
 st=[PT('射了、开（枪）了；拍了；投（篮）了'), PPT('射', '已经射了；被射中、被拍下（be shot 中枪）'),
     '→ 当名词：射出去的东西 → 子弹、炮弹、铅弹等各种弹丸',
     '　用词规律：表示动作的词，也能直接当名词用，指这件事或做一次（shot：射 → 子弹、炮弹、铅弹等各种弹丸；walk 走 → 散步）',
     '→ 开一下枪 → 一次射击；枪声', '→ 球场上射一下、投一下 → 射门、投篮',
     '→ 针头一下子扎进胳膊 → 打针、注射；镜头对准了“拍一下” → 一个镜头',
     '→ 瞄准目标射一下，不一定射中 → 尝试',
     '→ 一小杯烈酒（来路说不准；可以这样记：一仰脖，“一下子”灌下去）',
     '→（口）坏了的、筋疲力尽的（可以这样记：像被子弹打烂了一样）'],
 P="""【字母变化】scoten（古英语）→ shotten（中古英语）→ shot（英语）
① 古英语 scēotan“射、冲”是强变化动词：scēotan – scēat – scoten（sc 念 sh），过去分词的 o 是短的。
② sc 改写成 sh，短 o 后面的 t 双写：scoten → shotten（这个形式还留在 shotten herring“产过卵的瘦鲱鱼”这类老说法里）。
③ 词尾 -en 掉了：shotten → shot；后来过去式也改用 shot。名词 shot“射击；子弹”古英语就有，和动词这个形式成了同形。""")

E['reshot'] = dict(
 st=[PT('重拍了、补拍了'), PPT('重拍', '已经重拍了；被重拍')],
 P="""reshoot – reshot – reshot：reshoot 里的 shoot 照 shoot 变（见 shot）。""")

E['bent'] = dict(
 l1='bend（弄弯）→ bent =“弄弯了；被弄弯了的”',
 st=[PT('弄弯了；弯下了（腰）'), PPT('弄弯', '已经弄弯了；被弄弯'), AT('弄弯', '弯曲的'),
     '→ 心思整个“弯”向一件事 →（be bent on）一心要（做某事）', '→ 天生往某个方向“弯” →（n.）天生的爱好、才能',
     '→ 和“直”（正直）反着来 →（英俚）不老实的、腐败的'],
 P="""【字母变化】bende（古英语）→ bent（英语）
① 古英语 bendan“拉弓、弄弯”是规则（弱变化）动词，过去式 bende：词干的 d 和过去式的 -de 并成一个。
② 中古英语起，-nd 结尾的动词过去式里的 d 念成清音 t：bende → bent（同 send → sent、spend → spent、lend → lent、build → built）。""")

E['bound'] = dict(
 l1='bind（捆）→ bound =“捆了；被捆住了的”',
 st=[PT('捆了、绑了；装订了'), PPT('捆', '已经捆好了；被捆住'), AT('捆', '被捆绑的'),
     '→ 被法律、合同“捆”住 → 有义务的、受约束的', '→ 被“捆”着只能往一个方向去 →（be bound to do）一定会、注定',
     '→ 书页被捆在一起 → 装订的；放在名词后 →（-bound）被…困住的（snowbound 被雪困住的）'],
 P=f"""【字母变化】bunden（古英语）→ bounden（中古英语）→ bound（英语）
① 古英语 bindan“捆”是强变化动词：bindan – band – bunden。今天的 bound 来自过去分词 bunden 这一支，后来过去式也改用它，band 就不用了。
② u 在 nd 前面拉长成 /uː/，中古英语照法语习惯写成 ou：bunden → bounden（bounden duty“义不容辞的责任”里还留着这个形式）。
③ 词尾 -en 掉了：bounden → bound；{GVS}，/uː/ 成了 /aʊ/，读 /baʊnd/（同 find → found、grind → ground、wind → wound）。""")

E['sought'] = dict(
 l1='seek（寻找）→ sought =“找过了；被人找的”',
 st=[PT('寻找过、谋求过'), PPT('寻找', '已经找过了；被寻找、被谋求'), AT('找', '抢手的、吃香的（sought-after）', '：大家都在找、都想要')],
 P="""【字母变化】sohte（古英语）→ soughte（中古英语）→ sought（英语）
① 古英语 sēcan“寻找”是规则（弱变化）动词，过去式 sōhte：词干的 c 碰上过去式的 -te，念成喉音 h。现在时的 ē 是 ō 受后面 -j- 音影响变来的，过去式没有，保留了 o。
② 中古英语用 gh 写这个喉音，o 写成 ou：sohte → soughte。
③ 词尾的 e 不念了；gh 后来也不念了，ou 读 /ɔː/：soughte → sought（同 thought、brought、bought）。""")

E['lent'] = dict(
 l1='lend（借出）→ lent =“借出了；被借出的”',
 st=[PT('借出了'), PPT('借出', '已经借出了；被借出')],
 P="""【字母变化】lende（中古英语）→ lent（英语）
① 古英语 lǣnan“借给”（同 loan）是规则动词，过去式 lǣnde；原形本来没有 d，中古英语里过去式 lende 的 d 被当成了词干的一部分，原形也就成了 lend（etymonline）。
② 照 send → sent、bend → bent 的样子，过去式里的 d 念成清音 t：lende → lent。""")

E['knelt'] = dict(
 l1='kneel（跪下）→ knelt =“跪下了”',
 st=[PT('跪下了、跪着'), PPI('跪', 'kneel', '已经跪下了')],
 P="""kneel 本是规则动词（古英语 cnēowlian），过去式 kneeled；knelt 是 19 世纪才照 feel → felt、deal → dealt 的样子造的：长音 ee 变短 e，-ed 写成 -t（etymonline）。英式多用 knelt，北美多用 kneeled。""")

E['slid'] = dict(
 l1='slide（滑）→ slid =“滑了”',
 st=[PT('滑了、滑过；（价格）下滑了'), PPI('滑', 'slide', '已经滑下去了')],
 P="""【字母变化】sliden（古英语）→ slid（英语）
① 古英语 slīdan“滑”是强变化动词：slīdan – slād – sliden，过去分词的 i 是短的。
② 词尾 -en 掉了：sliden → slid；后来过去式也改用 slid，slād 就不用了（另一种过去分词 slidden 也有人用）。原形 slide 的长 i 经元音大推移读 /aɪ/，slid 读短 /ɪ/。""")

E['swept'] = dict(
 l1='sweep（扫）→ swept =“扫了；被扫过的”',
 st=[PT('扫了；席卷了'), PPT('扫', '已经扫过了；被扫、被卷走'),
     '→ 被卷走、被冲走 →（be swept away）被冲走；（比喻）被深深打动、被迷住'],
 segdrop=['例'],
 P="""【字母变化】swepte（中古英语）→ swept（英语）
① 中古英语 swepen“扫”是 14 世纪初出现的（取代了更早的 swope），过去式在 p 后面加 -te，长元音碰上 p + t 变短：swepte。
② 词尾的 e 不念了：swepte → swept（同 keep → kept、sleep → slept、weep → wept）。""")

E['stole'] = dict(
 l1='steal（偷）→ stole =“偷了”',
 st=[PT('偷了；溜了；抢了（风头）')],
 P="""【字母变化】stal（中古英语）→ stole（英语）
① 古英语 stelan“偷”是强变化动词：stelan – stæl – stolen，过去式 stæl 中古英语写成 stal。
② 后来照过去分词 stolen 的 o 改成 stole：stal → stole，读 /stəʊl/（同 speak → spoke、break → broke）。""")

E['stolen'] = dict(
 l1='steal（偷）→ stolen =“被偷了的”',
 st=[PPT('偷', '已经偷了；被偷（My bike was stolen.）'), AT('偷', '被偷的、赃的', '：被人偷走'),
     '→ 偷偷得到的 → 偷偷的、偷闲的（a stolen kiss 偷偷的一吻）'],
 P="""steal – stole – stolen：古英语 stelan – stæl – stolen，过去分词就是 stolen，元音换成 o 再加 -en，从古英语到今天没变（同 speak → spoken、break → broken、choose → chosen）。""")

E['sank'] = dict(
 l1='sink（下沉）→ sank =“沉下去了”',
 st=[PT('沉下去了、沉没了；（心情）一沉；（价格）跌了')],
 P="""【字母变化】sanc（古英语）→ sank（英语）
① 古英语 sincan“下沉”是强变化动词：sincan – sanc – suncen，靠换元音表示时态（i → a → u）。
② c 改写成 k：sanc → sank（同 drink – drank – drunk、swim – swam – swum）。""")

E['sunk'] = dict(
 l1='sink（下沉）→ sunk =“已经沉下去了”',
 st=[PPT('弄沉', '已经沉没；被弄沉'), AI('沉', '堕落的、低下的（1680s）；（情绪）消沉的（1719）', '：人像沉了下去'),
     '→ 事情沉了底，捞不回来 →（口语）完蛋了、没救了；（sunk cost）沉没成本'],
 P="""【字母变化】suncen（古英语）→ sunk（英语）
① 古英语 sincan 的过去分词 suncen：元音换成 u，后面加 -en。
② 词尾 -en 掉了，c 改写成 k：suncen → sunk（同 drink → drunk、swim → swum）；保留 -en 的老形式 sunken 今天作形容词（a sunken ship 沉船）。""")

E['sewn'] = dict(
 st=[PPT('缝', '已经缝好了；被缝起来'), AT('缝', '缝好的（hand-sewn 手工缝制的）')],
 P="""sew 一直是规则动词（古英语 siwian），过去分词本来是 sewed；sewn 是后来照 sow – sown、show – shown 加 -n 的，今天更常用。sewn 和 sown（播了种的）同音不同义。""")

E['clung'] = dict(
 l1='cling（紧抓、紧贴）→ clung =“紧抓了、紧贴了”',
 st=[PT('紧紧抓住了、贴住了'), PPI('紧抓', 'cling', '已经紧紧抓住了')],
 P="""【字母变化】clungen（古英语）→ clung（英语）
① 古英语 clingan“粘住、紧贴”是强变化动词：clingan – clang – clungen。
② 词尾 -en 掉了：clungen → clung；后来过去式也改用 u 形，clang 就不用了（同 sting → stung、swing → swung，比较 sing → sang 还保留 a）。""")

E['snuck'] = dict(
 l1='sneak（溜）→ snuck =“溜了”',
 st=[PT('溜了、偷偷做了'), '# 过去分词：跟在 have 后面，说“已经溜了” → 已经溜进去了、已经偷偷做了'],
 P="""sneak 原是规则动词（过去式 sneaked）；snuck 是 19 世纪末美国口语里照 stick → stuck、strike → struck、dig → dug 造出来的，元音换成 u。新词一般都走规则变化，snuck 是少见的“规则变不规则”（同美式 dive → dove）；正式写作仍以 sneaked 为准。""")

E['stung'] = dict(
 l1='sting（蜇）→ stung =“蜇了；被蜇了”',
 st=[PT('蜇了'), PPT('蜇', '已经蜇了；被蜇、（比喻）被刺伤、被坑了')],
 P="""【字母变化】stungen（古英语）→ stung（英语）
① 古英语 stingan“蜇”是强变化动词：stingan – stang – stungen。
② 词尾 -en 掉了：stungen → stung；后来过去式也改用 u，stang 就不用了（同 cling → clung、swing → swung）。""")

E['swung'] = dict(
 l1='swing（挥、摆）→ swung =“挥过了、摆过了”',
 st=[PT('摆动了、挥过'), PPT('甩', '已经挥过了；被甩动')],
 P="""【字母变化】swungen（古英语）→ swung（英语）
① 古英语 swingan“打、挥”是强变化动词：swingan – swang – swungen。
② 词尾 -en 掉了：swungen → swung；后来过去式也改用 swung，swang 就成了已废的旧形式（同 sting → stung）。""")

E['wept'] = dict(
 l1='weep（哭泣）→ wept =“哭过了”',
 st=[PT('哭了、流过泪（书面）'), PPI('哭', 'weep')],
 P="""【字母变化】wepte（中古英语）→ wept（英语）
① 古英语 wēpan“哭”原是强变化动词（过去式 wēop）；中古英语改走规则的弱变化，过去式在 p 后面加 -te，长元音变短：wepte。
② 词尾的 e 不念了：wepte → wept；原形 weep 的长 ee 经元音大推移读 /iː/，wept 读短 /e/（同 keep → kept、sleep → slept、sweep → swept）。""")

E['strode'] = dict(
 l1='stride（大步走）→ strode =“大步走了”',
 st=[PT('大步走了、阔步走了')],
 P=f"""【字母变化】strad（古英语）→ strood（中古英语）→ strode（英语）
① 古英语 strīdan“跨、骑上”是强变化动词：strīdan – strād – striden；过去式 strād 的 ā 是长音。
② 中古英语里长音 ā 变成长音 o，常双写成 oo：strad → strood（同 rād → rode、wrāt → wrote）。
③ 后来改用“o + 辅音 + 不发音的 e”：strood → strode；{GVS}，读 /strəʊd/。""")

E['beaten'] = dict(
 st=[PPT('打', '已经打过；被打、被打败'), AT('打', '被打败的；（金属）锤薄的', '：比赛里被打下去；金属被一下下锤打'),
     '→ 路被很多人的脚一遍遍“打”过、踩实 →（路）被踩出来的（off the beaten track 人迹罕至的）'],
 P="""古英语 bēatan“打”是强变化动词：bēatan – bēot – bēaten，过去分词就是 beaten，元音和原形一样，后面加 -en，一千多年没变；过去式 beat 是约 1500 年起照原形改的（古英语是 bēot）。""")

E['bitten'] = dict(
 st=[PPT('咬', '已经咬了；被咬'), AT('咬', '被（狗、蛇等）咬了的；被蚊虫叮了的')],
 P="""【字母变化】biten（古英语）→ bitten（英语）
① 古英语 bītan“咬”是强变化动词：bītan – bāt – biten，过去分词的 i 是短的，后面加 -en。
② 短 i 后面的 t 双写：biten → bitten；原形 bite 的长 i 经元音大推移读 /aɪ/，bitten 读短 /ɪ/（同 write → written）。""")

E['forbidden'] = dict(
 st=[PPT('禁止', '已经禁止了；被禁止'), AT('禁止', '被禁止的、不许的'),
     '→ 不许人进去的地方 → 禁止进入的（the Forbidden City 紫禁城）'],
 P="""古英语 forbēodan“禁止”是强变化动词：forbēodan – forbēad – forboden；中古英语过去分词写 forbode，后来照 bid – bidden 改成 forbidden（d 双写，保住短 i）。""")

# 字母变化轮：37 个“X ← 源头词根”的外来基础词，音变 / 字母变化列（P 列）的新写法
# 每条：(行号, 单词, 新的字母变化部分, [原文里要保留的段落（必须一字不差地在原文里）], [改写过的保留段落])
# 新写法：第一行【字母变化】是一条链（每个形式后面括号里写语言），下面每一步一行：① 讲源头那个形式，②③… 每一行讲一个箭头。

DATA = [
(17, 'people', '''【字母变化】populus（拉丁语）→ pople（古法语）→ peuple（古法语）→ people（英语）
① 拉丁语 populus：po-pu-lus，“一国的全体人民”；词根 popul- 原样留在 popular、populate、populous 里。
② 在法国人的口语里，中间没有重音的 u 被吞掉，词尾的 -us 也磨成一个不发音的 e：populus → pople。
③ 开头那个重读的 o 拉长，变成复合元音，写成 eu：pople → peuple（今天法语还这样写；西班牙语 pueblo 的 ue 也是这个 o 变来的）。
④ 约 1300 年进入英语，先多写 peple，读长音 /eː/；拼写后来照英法语（英国诺曼人说的法语）定成 people，eo 只是记这个长元音的一种写法。后来英语的长元音整体变了读法（元音大推移），/eː/ 变成了 /iː/，所以今天读 /ˈpiːpl/，o 不发音。''',
 ['【同源】西班牙语 pueblo（村镇；人民）、意大利语 popolo 也出自 populus'], []),

(591, 'place', '''【字母变化】plateia（希腊语）→ platea（拉丁语）→ placea（中世纪拉丁语）→ place（古法语、英语）
① 希腊语 plateia（hodos）：“宽阔的（路）”，是 platys“宽、平”的阴性形式；词根 plat- 就是 platys 的头一截。
② 罗马人借来写成 platea：pla-te-a，指“宽阔的大街；庭院、空地”；希腊语的 ei 在拉丁语里写成 e。
③ t 后面紧跟着 e 和另一个元音，读音滑成 ts，抄写的人就改写成 c：platea → placea（意大利语 piazza 的 zz 至今还读 ts）。
④ 到古法语，词尾的 -ea 磨成一个不发音的 e：place，c 的读音也由 ts 简化成 s。英语约 1200 年原样借来，字母没再变；后来英语的长元音整体变了读法（元音大推移），a 成了 /eɪ/，所以读 /pleɪs/。''',
 ['【同源】意大利语 piazza、西班牙语 plaza、德语 Platz 都来自同一个拉丁词；英语 place 取代了古英语 stow、stede'], []),

(881, 'round', '''【字母变化】rotundus（拉丁语）→ *retundus（俗拉丁语）→ roont（古法语）→ round（英语）
① 拉丁语 rotundus：ro-tun-dus，“像轮子一样的、圆的”，由 rota“轮子”变来；词根 rot- 原样留在 rotate、rotary 里。
② 俗拉丁语（老百姓说的口语拉丁语）里，第一个 o 念成了 e：rotundus → *retundus（带 * 的是没留下文字、由后来的语言推出来的形式；西班牙语 redondo 还看得出这一步）。
③ 到古法语，夹在两个元音中间的 t 先念成 d、后来脱落；un 念成 on，词尾的 -us 掉了，留在词末的 d 念成 t：reont；第一个 e 又跟着后面的 o 念成 o：roont（今天法语写 rond）。
④ 约 1300 年进入英语，英法语（英国诺曼人说的法语）写成 round、rounde：两个 o 并成一个长音 /uː/，照法语的习惯写成 ou；后来英语的长元音整体变了读法（元音大推移），/uː/ 成了 /aʊ/，所以读 /raʊnd/（同 sound、count）。''',
 ['【同源】rotate、rotary、roulette、roll、role、control 都出自拉丁 rota“轮子”（PIE *ret-“跑、转、滚”；德语 Rad“轮子”同源）',
  '【联想】德语 rund、荷兰语 rond 反过来是从法语借的'], []),

(1114, 'city', '''【字母变化】civitatem（拉丁语）→ citatem（晚期拉丁语）→ citet（古法语）→ cite（古法语）→ city（英语）
① 拉丁语 civitas“全体公民；城邦”，法语、英语的词都是从它的变格形式 civitatem（ci-vi-ta-tem）变来的；词根 civ- 原样留在 civil、civic 里。
② 口语里没有重音的 vi 整个音节被吞掉，v 并进了后面的 t：civitatem → citatem（晚期拉丁语里已经有这种写法）。
③ 到古法语，重读的 a 变成 e（法语的老规矩，同拉丁 mare“海”→ 法语 mer），词尾的 -em 掉了，只剩一个 t：citatem → citet。
④ 词尾这个 t 后来也不念了：citet → cite（今天法语写 cité，é 上读重音）。
⑤ 约 1200 年进入英语，先写 cite、citee；重音挪到第一个音节，词尾的 e 念成轻轻的 /i/，后来写成 y：city，读 /ˈsɪti/（c 在 i 前面读 /s/）。''',
 [], []),

(1361, 'rule', '''【字母变化】regula（拉丁语）→ reule（古法语）→ rule（英语）
① 拉丁语 regula：re-gu-la，“直木条、尺子”（出自 regere“使直、引导”）；词根 regul- 原样留在 regular、regulate 里。
② 到古法语，夹在两个元音中间的 g 越念越轻，最后脱落，e 和 u 挤到了一起；词尾的 -a 弱化成不发音的 e：regula → reule（诺曼人这样写，巴黎一带写 riule；今天法语的 règle 是后来照拉丁语部分改回的写法）。
③ 约 1200 年进入英语，先写 reule、riule、rewle，这几个元音字母合起来读一个复合元音 /iu/；后来它在 r 后面变成长音 /uː/（同 rude、true），拼写也简化成 rule：读 /ruːl/。''',
 ['【同源】rail（栏杆、铁轨）是 regula 走另一条路变来的（见 rail）；regular、regulate 直接取自拉丁。',
  '【跨组同源】与本族词 right（第 100 组）同出 PIE *reg-'], []),

(1465, 'save', '''【字母变化】salvare（晚期拉丁语）→ sauver（古法语）→ saven（中古英语）→ save（英语）
① 晚期拉丁语 salvare：sal-va-re，“使安全、救出来”，由 salvus“完好的、安全的”变来；词根 salv- 原样留在 salvage、salvation 里。
② 到古法语，辅音前面的 l 念成了 u（舌头不再去碰上颚），动词词尾 -are 变成 -er：salvare → sauver（今天法语还这样写；同拉丁 salmo → 法语 saumon“鲑鱼”，英语 salmon 的 l 写着却不念）。
③ 约 1200 年进入英语，au 念成单个的 a，u 也就不写了，再接上当时英语动词的词尾 -en：saven。
④ 词尾的 -en 后来脱落，只剩一个不发音的 e：save；后来英语的长元音整体变了读法（元音大推移），a 成了 /eɪ/，所以读 /seɪv/。''',
 [], ['【同源】safe、salvage、salvation、salute']),

(1688, 'sound', '''【字母变化】sonus（拉丁语）→ son（古法语）→ soun（中古英语）→ sound（英语）
① 拉丁语 sonus：so-nus，“声音、响声”；词根 son- 原样留在 sonic、resonate、consonant 里。
② 到古法语，词尾的 -us 掉了：sonus → son（今天法语还是 son）。
③ 13 世纪末进入英语，o 在 n 前面念成长音 /uː/，照英法语（英国诺曼人说的法语）的习惯写成 ou：soun。
④ 约 1350—1550 年间，n 后面多出一个不合词源的 d（英语有在 n 后面添 d 的倾向，一般认为是念着顺口）：sound；后来英语的长元音整体变了读法（元音大推移），/uː/ 成了 /aʊ/，所以读 /saʊnd/。''',
 ['【同源】swan（天鹅）也出自 *swen-，本义“会叫的鸟”',
  '【同形异义】sound“健全的、可靠的”（safe and sound、a sound argument）来自古英语 gesund（德语 gesund 健康、Gesundheit），见第 126 组 soundly'], []),

(2167, 'order', '''【字母变化】ordinem（拉丁语）→ ordene（古法语）→ ordre（古法语）→ order（英语）
① 拉丁语 ordo“一排、次序”，变格时写作 ordin-（如 ordinem：or-di-nem），法语的词就是从这个形式变来的；词根 ordin- 原样留在 ordinary、coordinate 里。
② 到古法语，没有重音的 i 弱化成 e，词尾的 -m 掉了：ordinem → ordene（早期的写法）。
③ 中间的 e 也被吞掉，d 和 n 挤到一起，n 变成了 r：ordene → ordre（今天法语还这样写；法语里这样 n 变 r 的还有拉丁 Londinium“伦敦”→ 法语 Londres）。
④ 约 1200 年进入英语，先照法语写 ordre；后来词尾的 -re 照英语的习惯写成 -er：order（同 chamber、number 也是由法语的 -bre 改成 -ber）。''',
 ['【有争议】词库“跨语同源”栏把 order 明确归入 PIE *ar-；etymonline 的 *ar- 词根表虽然收了它，order 条目却说 *ordn- 来源不确定，宜看作两说并存'], []),

(2222, 'course', '''【字母变化】cursus（拉丁语）→ cors（古法语）→ cours（中古英语）→ course（英语）
① 拉丁语 cursus：cur-sus，“奔跑；路线”，由 currere“跑”变来；词根 curs- 原样留在 cursive、cursor 里。
② 到古法语，u 念成了 o，词尾的 -us 掉了：cursus → cors（后来法语又写成 cours）。
③ 约 1300 年进入英语，o 念成长音 /uː/，照法语的新写法写成 ou：cours。
④ 词尾加一个不发音的 e，免得 s 结尾看着像复数（英语拼写的老习惯，同 house、horse）：course；ou 在 r 前面后来念成 /ɔː/（同 court、source），所以读 /kɔːs/，和 coarse 同音。''',
 ['【跨组同源】car、carry、career、charge（第 161 组）同出 PIE *kers-',
  '【易混】course 与 coarse 同音（见 coarse）'], []),

(2542, 'clear', '''【字母变化】clarus（拉丁语）→ cler（古法语）→ clear（英语）
① 拉丁语 clarus：cla-rus，先说声音“响亮的”，再说光“明亮的、清楚的”；词根 clar- 原样留在 clarify、clarity 里。
② 到古法语，重读的 a 变成 e（法语的老规矩，同拉丁 mare“海”→ 法语 mer），词尾的 -us 掉了：clarus → cler（今天法语写 clair）。
③ 约 1300 年进入英语，先写 cler、clere，读一个长 e 音；16 世纪前后写成 clear，ea 是当时专门记这个长音的写法（同 sea、meat）；后来英语的长元音整体变了读法（元音大推移），它在 r 前面念成 /ɪə/（美式 /ɪr/）。''',
 [], ['【同根】claim（声称）、clamor（喧嚷）、exclaim（呼喊）、declare（宣布）都出自 *kele-“喊”']),

(2639, 'matter', '''【字母变化】materia（拉丁语）→ matere（古法语）→ matter（英语）
① 拉丁语 materia：ma-te-ri-a，“造东西用的材料”，原指树干中心最坚硬的心材；词根 materi- 原样留在 material 里。
② 到古法语，词尾的 -ia 磨成一个不发音的 e：materia → matere（今天法语写 matière）。
③ 约 1200 年进入英语，先写 materie、matere；重音在第一个音节，后面的 -ere 念得很轻，缩成 -er；t 双写成 tt，表示前面的 a 读短音（英语拼写的老习惯，同 dinner、summer）：matter，读 /ˈmætə/。''',
 ['【同源】西班牙语 madera、葡萄牙语 madeira“木头”（马德拉群岛 Madeira 因林木茂密得名）；material（材料）由它派生'], []),

(2714, 'peace', '''【字母变化】pacem（拉丁语）→ pais（古法语）→ pes（中古英语）→ peace（英语）
① 拉丁语 pax“和约、安宁”，法语的词是从它的变格形式 pacem（pa-cem）变来的；词根 pac- 原样留在 Pacific、pacify 里。
② 到古法语，c 在 e 前面念软，分成一个 i 音和一个 s 音，词尾的 -em 掉了：pacem → pais（同拉丁 placere → 法语 plaisir“乐趣”；今天法语写 paix）。
③ 英法语（英国诺曼人说的法语）把 ai 念成长 e，写成 pes；英语 12 世纪中借来，写 pes、pees。
④ 后来改写成 peace：ea 记这个长 e 音（同 clear、sea），词尾写 ce，表示读 /s/、不读 /z/（同 face、voice）；后来英语的长元音整体变了读法（元音大推移），读成 /piːs/。''',
 ['【同源】pay（付钱，本义“使和平”）、pact（协约）、Pacific（太平洋）都出自同一个 pax / *pag-'], []),

(2726, 'grace', '''【字母变化】gratia（拉丁语）→ grace（古法语、英语）
① 拉丁语 gratia：gra-ti-a，“恩惠、好意；讨人喜欢的样子；谢意”，由 gratus“令人喜欢的”变来；词根 grat- 原样留在 gratitude、grateful 里。
② ti 后面紧跟着元音，读音滑成 ts，中世纪的抄本里常写成 gracia（西班牙语至今写 gracia）；到古法语，词尾的 -ia 磨成一个不发音的 e：gratia → grace，c 的读音也由 ts 简化成 s（今天法语写 grâce）。
③ 英语 12 世纪末原样借来，字母没再变；后来英语的长元音整体变了读法（元音大推移），a 成了 /eɪ/，所以读 /ɡreɪs/。''',
 ['【同源】agree（a gré）、grateful、gratitude、congratulate 都出自 gratus；coup de grâce（1690s）“仁慈的一击”'], []),

(2787, 'voice', '''【字母变化】vocem（拉丁语）→ voiz（古法语）→ voice（英语）
① 拉丁语 vox“声音、喊声”（和 vocare“叫、喊”是一家），法语的词是从它的变格形式 vocem（vo-cem）变来的；词根 voc- 原样留在 vocal、vocation、vocabulary 里。
② 到古法语，c 在 e 前面念软，分成一个 i 音和一个 ts 音（写成 z），词尾的 -em 掉了：vocem → voiz（同 pacem → pais；今天法语写 voix）。
③ 13 世纪末进入英语，oi 读 /ɔɪ/；词尾的 z 改写成 ce，表示读 /s/（同 peace、choice）：voice，读 /vɔɪs/。''',
 ['【跨组同源】希腊来源的 epic（第 2306 组）也出自 *wekw-；voice 取代了古英语 stefn“声音”'], []),

(2879, 'waste', '''【字母变化】vastare（拉丁语）→ waster（北部古法语）→ wasten（中古英语）→ waste（英语）
① 拉丁语 vastare：vas-ta-re，“使荒芜”，由 vastus“空的、荒凉的”变来；词根 vast- 原样留在 vast、devastate 里。
② 法兰克人（中世纪初统治法国北部的日耳曼人）的话里有个意思相近的 *wostjan，受它影响，开头的 v 念成了 w；动词词尾 -are 变成 -er：vastare → waster（北部古法语；巴黎一带把这个 w 念成 g，写 gaster，今天法语是 gâter“弄坏”）。
③ 约 1200 年进入英语，接上当时英语动词的词尾 -en：wasten。
④ 词尾的 -en 后来脱落，只剩一个不发音的 e：waste；后来英语的长元音整体变了读法（元音大推移），a 成了 /eɪ/，所以读 /weɪst/。''',
 ['【同源】vast、devastate（本组）；vacant、vacuum、void、vain，以及本族词 want（缺）、wane（月亏）都在 *eue- 词根表里'],
 ['【对照】同样的 w ↔ g(u)：war / 法语 guerre，ward / guard，warranty / guarantee']),

(2893, 'mount', '''【字母变化】montem（拉丁语）→ *montare（俗拉丁语）→ monter（古法语）→ mount（英语）
① 拉丁语 mons“山”，变格时写作 mont-（如 montem：mon-tem）；mountain、amount 里的 mount- 都是由这个 mont- 变来的。
② 俗拉丁语（也叫民间拉丁语，老百姓说的口语拉丁语）用它造了个动词 *montare“往山上走、登高”：mont- 加上动词词尾 -are（带 * 的是没留下文字、推出来的形式）。
③ 到古法语，动词词尾 -are 变成 -er：*montare → monter“上去、攀登、骑上”（今天法语还这样写）。
④ 约 1300 年进入英语写 mounten：o 在 n 前面念成长音 /uː/，照英法语（英国诺曼人说的法语）的习惯写成 ou，词尾换成当时英语动词的 -en；-en 后来掉了：mount；后来英语的长元音整体变了读法（元音大推移），/uː/ 成了 /aʊ/，所以读 /maʊnt/（同 count、fountain）。''',
 ['【同源】mountain、amount、prominent（本组）；eminent（杰出的）、imminent（迫近的）、promontory（海角）都出自 *men- (2)“突出”'], []),

(3299, 'cross', '''【字母变化】crux（拉丁语）→ cros（古爱尔兰语）→ kross（北欧语）→ cross（英语）
① 拉丁语 crux：“木桩、十字架”（罗马人的行刑用具），变格时写作 cruc-（crucis、crucem）；词根 cruc- 原样留在 crucial、crucify 里，这两个词是后来照拉丁语书面借的。
② 基督教传到爱尔兰，古爱尔兰语借来写成 cros：u 念成了 o，x（读 ks）只剩一个 s 音：crux → cros。
③ 维京人（北欧人）在爱尔兰一带学会了这个词，写成 kross：北欧文字用 k 记这个音，词尾的 s 双写。
④ 10 世纪中进入英语，古英语写 cros，最早指基督受难的十字架；后来照英语拼写的习惯，短元音后面词尾的 s 双写（同 loss、boss）：cross，读 /krɒs/。''',
 [], ['【同源】法语 croix、意大利语 croce、西班牙语 cruz、德语 Kreuz 也都出自拉丁 crux']),

(3495, 'image', '''【字母变化】imaginem（拉丁语）→ imagene（古法语）→ image（古法语、英语）
① 拉丁语 imago“仿出来的像”，变格时写作 imagin-（如 imaginem：i-ma-gi-nem），法语的词就是从这个形式变来的；词根 imagin- 原样留在 imagine、imaginal 里。
② 到古法语，没有重音的 i 弱化成 e，词尾的 -m 掉了：imaginem → imagene（11 世纪的写法）。
③ 后面的 -ne 也磨掉，只剩一个不发音的 e：imagene → image（今天法语还这样写）；g 在 e 前面不再读 /g/，念成了 /dʒ/。英语约 1200 年原样借来，重音在第一个音节，a 念得很轻：/ˈɪmɪdʒ/。''',
 ['【同源】*aim-“模仿”：imitate（见本组）、emulate（效仿）；imagine 用的是 imago 的拉丁词干 imagin-'], []),

(3569, 'duke', '''【字母变化】dux（拉丁语）→ duc（古法语）→ duke（英语）
① 拉丁语 dux“领袖、统帅”（出自 ducere“领着走”），变格时写作 duc-（ducis、ducem）；词根 duc- 原样留在 ducat、educate 里。
② 古法语照它的词干写成 duc，c 读 /k/：dux → duc（今天法语还是 duc）。
③ 12 世纪初进入英语，先写 duc、duk；词尾后来加个不发音的 e，表示前面的 u 读长音（同 rule、tune）：duke，读 /djuːk/（美式 /duːk/）。同根的 ducal（公爵的）、duchy（公国）还保留 duc-。''',
 [], ['【同源】德语 Herzog“公爵”、古英语 heretoga 的后半部分与它同根（字面“领兵的人”）']),

(3692, 'reason', '''【字母变化】rationem（拉丁语）→ raison（古法语）→ resoun（中古英语）→ reason（英语）
① 拉丁语 ratio“计算 → 道理”，变格时写作 ration-（如 rationem：ra-ti-o-nem），法语的词就是从这个形式变来的；词根 rat- 原样留在 ratio、rational 里。
② 这个词在法国人嘴里口头流传，ti 后面紧跟着元音，先念成 ts，又软化成一个 i 音和一个 z 音，词尾的 -em 掉了：rationem → raison（今天法语还这样写）。
③ 英法语（英国诺曼人说的法语）把 ai 念成长 e，把 on 写成 oun：raison → resoun；约 1200 年进入英语就是这个样子。
④ 后来拼写改成 reason：ea 记这个长 e 音（同 peace、clear），oun 写回 on；后来英语的长元音整体变了读法（元音大推移），读成 /ˈriːzn/（s 夹在两个元音中间读 /z/）。''',
 ['【同源】*re- 词根表还可能收录 read（读；古英语还指“劝告”）、arithmetic（算术）、hundred（百）、rhyme（韵）'],
 ['【对照】同一个拉丁词照书面原样借进英语，就是 ration、ratio（同 poison ↔ potion 一对）']),

(3732, 'paint', '''【字母变化】pictus（拉丁语）→ *pinctus（俗拉丁语）→ peint（古法语）→ paint（英语）
① 拉丁语 pingere“画、着色”，“被画了的”说 pictus：pic-tus；词根 pict- 原样留在 picture、depict 里。
② 俗拉丁语（老百姓说的口语拉丁语）照现在时 pingere 把鼻音 n 也放了进来：pictus → *pinctus（带 * 的是没留下文字、推出来的形式；西班牙语 pintar“画”也是从这里来的）。
③ 到古法语，ct 里的 c 念成 i，和前面的 i 并成 ei，n 让前面的元音念成鼻音，词尾的 -us 掉了：*pinctus → peint（同拉丁 factum → 法语 fait“做成的事”）。
④ 古法语由 peint 造了动词 peintier“画”；13 世纪中进入英语写 peinten，词尾的 -en 后来掉了，ei 改写成 ai：paint，读 /peɪnt/。''',
 ['【同源】去掉鼻音 n 就是 pict-（picture、depict）和 pig-（pigment）；pixel 里的 pix 也来自 picture（见各条）'], []),

(3963, 'chief', '''【字母变化】caput（拉丁语）→ *capum（俗拉丁语）→ chief（古法语、英语）
① 拉丁语 caput：ca-put，“头；首领；顶端”；词根 cap- 原样留在 capital 里。
② 俗拉丁语（老百姓说的口语拉丁语）把词尾换成更常见的 -um：caput → *capum（带 * 的是没留下文字、推出来的形式；意大利语 capo、西班牙语 cabo 都从它来）。
③ 到巴黎一带的古法语，一下子变了三处：a 前面的 c 念成 ch（/tʃ/）；跟在 ch 后面的重读 a 变成 ie；词尾的元音掉了，p 先念成 v，到了词末又念成 f：*capum → chief（同 caput 的小词 capitulum → 古法语 chapitre，英语 chapter）。
④ 约 1300 年进入英语，字母没再变；ch 保留 /tʃ/，ie 读长音 /iː/：chief，读 /tʃiːf/。法语后来变成 chef，英语 19 世纪又借了一次，就是“厨师长”chef。''',
 [], ['【对照】法国北部方言保留 ca-：catel → cattle（牲口），和巴黎一带的 chatel → chattel（动产）是一对']),

(4007, 'flower', '''【字母变化】florem（拉丁语）→ flor（古法语）→ flour（中古英语）→ flower（英语）
① 拉丁语 flos“花”，变格时写作 flor-（如 florem：flo-rem）；词根 flor- 原样留在 floral、florist 里。
② 到古法语，词尾的 -em 掉了：florem → flor（后来法语又变成 fleur）。
③ 约 1200 年进入英语，o 念成长音 /uː/，照英法语（英国诺曼人说的法语）的习惯写成 ou：flour（当时也写 flur、flor）。
④ 后来英语的长元音整体变了读法（元音大推移），/uː/ 成了 /aʊ/，后面带出一个轻轻的 ə 音，就写成 ower：flower，读 /ˈflaʊə/（同 power、tower 的 ower）。''',
 ['【易混】flower 来自拉丁 flos，与 flow（流动，第 514 组）无关，拼写相近纯属巧合'],
 ['【同源】flower / flour 本是一个词：“面粉”是麦子磨出来最精华的部分，原来也写 flower，约 1830 年起才固定写成 flour，和“花”分开（见 flour）；拉丁词干 flor- 见于 floral、florist、flourish']),

(4067, 'letter', '''【字母变化】littera（拉丁语）→ letre（古法语）→ letter（英语）
① 拉丁语 littera：lit-te-ra，“字母”，复数 litterae 指书信、文献（也写 litera，一个 t）；词根 liter- 原样留在 literal、literature 里。
② 到古法语，i 念成 e，tt 写成一个 t，词尾的 -a 磨成不发音的 e：littera → letre（今天法语写 lettre，t 又双写了）。
③ 约 1200 年进入英语，先照法语写 letre；后来词尾的 -re 照英语的习惯写成 -er（同 order、number），t 也双写成 tt，表示前面的 e 读短音：letter，读 /ˈletə/。''',
 ['【趣】它取代了古英语 bōcstæf“书棍”（德语至今称字母为 Buchstabe）和 ǣrendgewrit“差事文书”（信）',
  '【有争议】若来自 diphthera，则 d 变 l（同 lachrymose“爱流泪的”与希腊 dakry“泪”）',
  '【同形异义】letter 另有“出租人”（let + -er）一义，来源不同'], []),

(4256, 'term', '''【字母变化】terminus（拉丁语）→ terme（古法语）→ term（英语）
① 拉丁语 terminus：ter-mi-nus，“界石、边界、终点”；词根 termin- 原样留在 determine、terminal 里。
② 到古法语，没有重音的 i 被吞掉，m 和 n 挤在一起不好念，n 也掉了；词尾的 -us 磨成一个不发音的 e：terminus → terme（今天法语还这样写）。
③ 约 1200 年进入英语，先写 terme，词尾的 e 后来不写了：term；er 读成 /ɜː/（同 her、serve）。''',
 [], []),

(4557, 'prove', '''【字母变化】probare（拉丁语）→ prover（古法语）→ prove（英语）
① 拉丁语 probare：pro-ba-re，“检验、试一试；证明”，由 probus“好的”变来；词根 prob- 原样留在 probable、probe 里。
② 到古法语，夹在两个元音中间的 b 念轻，变成了 v（同拉丁 habere → 法语 avoir“有”）；动词词尾 -are 变成 -er：probare → prover（今天法语写 prouver）。
③ 约 1200 年进入英语，先写 preven、pruven、proven（-en 是当时英语动词的词尾）；-en 后来掉了，只剩不发音的 e：prove；后来英语的长元音整体变了读法（元音大推移），o 读成 /uː/（同 move、lose）。''',
 ['【易混】improve 的 -prove 是 prou“利益”，与本词无关，只是拼写受 prove 一类词影响（improve 见第 32 批）',
  '【同源】probe、probable、proof、approve 都出自 probare'], []),

(4637, 'poor', '''【字母变化】pauperem（拉丁语）→ povre（古法语）→ pore（中古英语）→ poor（英语）
① 拉丁语 pauper“穷的、产出少的”，法语的词是从它的变格形式 pauperem（pau-pe-rem）变来的；词根 pauper- 原样留在 pauper（穷人）里。
② 到古法语，au 念成一个 o；夹在两个元音中间的 p 念轻，变成 v（同拉丁 sapere → 法语 savoir“知道”）；中间没有重音的 e 被吞掉，词尾的 -em 磨成不发音的 e：pauperem → povre（今天法语写 pauvre，又照拉丁语写回 au）。
③ 约 1200 年进入英语，先照法语写 povre；v 这个音在 r 前面渐渐不念了，写成 pore、poore。
④ 拼写最后定成 poor，读 /pʊə/（也读 /pɔː/，美式 /pʊr/）；直接从古法语 poverte 借来的 poverty 里还留着 v（pover-ty）。''',
 ['【同源】few（少）：本族词，同出 *pau-“少”（p ↔ f，同 pater / father）；pauper（赤贫者）、paucity（缺乏）'], []),

(4772, 'price', '''【字母变化】pretium（拉丁语）→ precium（晚期拉丁语）→ pris（古法语）→ price（英语）
① 拉丁语 pretium：pre-ti-um，“价值、价钱、报酬”；词根 preci-（就是 preti-）原样留在 precious、appreciate 里。
② ti 后面紧跟着元音，读音滑成 ts，晚期拉丁语就写成 ci：pretium → precium（同 gratia 常写成 gracia）。
③ 到古法语，e 和后面的 i 音并成一个 i，ts 简化成 s，词尾的 -um 掉了：precium → pris（今天法语写 prix）。
④ 约 1200 年进入英语，先写 pris；后来写成 price，词尾的 ce 表示读 /s/（同 peace、voice）；i 读长音，后来英语的长元音整体变了读法（元音大推移），成了 /aɪ/，所以读 /praɪs/。praise（称赞）、prize（奖品）也是从这个 pris 分出来的。''',
 [], ['【同源】praise、prize、precious、appreciate（第507组）；希腊 pernanai“卖”也出自 *per-（5），interpret 可能也是']),

(4990, 'faith', '''【字母变化】fidem（拉丁语）→ feid（古法语）→ feith（中古英语）→ faith（英语）
① 拉丁语 fides“信任、信用”，法语的词是从它的变格形式 fidem（fi-dem）变来的；词根 fid- 原样留在 confident、fidelity 里。
② 到古法语，重读的 i 念成 e，又拖出一个 i 音，成了 ei；词尾的 -em 掉了，留在词末的 d 念得很轻，像英语 th 那样：fidem → feid。
③ 13 世纪中进入英语，用 th 写这个音（也照着 truth、health 这些 -th 结尾的词）：feid → feith（也写 fei、fai）。
④ ei 后来改写成 ai：faith，读 /feɪθ/。法语这边连这个音也丢了，成了今天的 foi。''',
 ['【同源】fidelity（忠诚）、confide、federal（见本组）'], []),

(5762, 'lion', '''【字母变化】leonem（拉丁语）→ lion（古法语、英语）
① 拉丁语 leo“狮子”（借自希腊语 leōn），变格时写作 leon-（如 leonem：le-o-nem），法语的词是从这个形式变来的；词根 leo- 原样留在 leopard 里。
② 到古法语，e 紧挨着 o，念成了 i；词尾的 -em 掉了：leonem → lion（今天法语还这样写）。
③ 英语 12 世纪末原样借来，字母没再变；i 读长音，后来英语的长元音整体变了读法（元音大推移），成了 /aɪ/，所以读 /ˈlaɪən/。''',
 ['【合成】lion-hearted 勇猛无畏的（1708 年见）'],
 ['【联想】dandelion 蒲公英 = 古法语 dent de lion“狮子牙”（叶子像锯齿）；chameleon 变色龙 = 希腊语“地上的狮子”；Leo 狮子座']),

(5808, 'nurse', '''【字母变化】nutrix（拉丁语）→ *nutricia（晚期拉丁语）→ norrice（古法语）→ nurse（英语）
① 拉丁语 nutrix：nu-trix，“奶妈”（字面“喂奶的女人”），由 nutrire“喂奶、哺育”变来；词根 nutri- 原样留在 nutrition、nutrient 里。
② 晚期拉丁语由它变出 *nutricia“奶妈、保姆”（带 * 的是没留下文字、推出来的形式）：nutrix → *nutricia。
③ 到古法语，tr 里的 t 念轻、并进了 r，成了 rr（同拉丁 petra“石头”→ 法语 pierre）；u 念成了 o（古法语 norrir“喂养”也是这样，今天法语写 nourrir）；ci 念成 ts，写成 c；词尾的 -ia 磨成不发音的 e：*nutricia → norrice“奶妈、养母”（英文姓氏 Norris 就是它）。
④ 约 1200 年进入英语，先写 norice、nurrice；14 世纪末，中间没有重音的 i 被吞掉，r 和 c 挤在一起，c 改写成 s：nurse，读 /nɜːs/。''',
 ['【同源】nourish（滋养）、nursery（托儿所；苗圃）、nutrition（营养）都出自拉丁 nutrire：nurse 走口语路线，nutri- 在古法语里磨成 norr- / nur-；nutrition 是后来照拉丁原样借的书面词'], []),

(6383, 'air', '''【字母变化】aer（希腊语、拉丁语）→ air（古法语、英语）
① 希腊语 aēr：a-ēr，两个音节，“雾、霾、云气”，后来指“空气”；拉丁语借来写成 aer；词根 aer- 原样留在 aerial、aero- 里。
② 到古法语，两个音节并成一个：e 念成 i，和前面的 a 连成 ai：aer → air（今天法语还这样写）。
③ 约 1300 年进入英语，字母没再变；ai 在 r 前面后来念成 /eə/（美式 /er/）。''',
 [], ['【同形异义】air“神态、样子”（an air of mystery；put on airs 摆架子）多半是另一个词（一说出自拉丁 ager“出身之地”）；air“曲调”（1580s）借自意大利语 aria。',
      '【同源】aria（咏叹调）、aerial、aero-、malaria（mala aria“坏空气”）都出自希腊 aēr']),

(7595, 'wine', '''【字母变化】vinum（拉丁语）→ win（古英语）→ wine（英语）
① 拉丁语 vinum：vi-num，“葡萄酒”；词根 vin- 原样留在 vintage、vinegar 里（这两个词是后来经法语借的，所以还是 v）。
② 古典拉丁语的 v 读 /w/、i 读长音 /iː/，vinum 念起来像“wiː-num”。罗马时代日耳曼人就照这个读音借了去，词尾的 -um 掉了，后来英语的祖先把它带到英国：vinum → win，古英语读 /wiːn/（德语 Wein、荷兰语 wijn 也是这样来的）。
③ 中古英语也写 wyn；词尾加个不发音的 e，表示 i 是长音：wine；后来英语的长元音整体变了读法（元音大推移），/iː/ 成了 /aɪ/，所以读 /waɪn/（同 mine、line）。''',
 ['【趣】vinyl（乙烯基、黑胶唱片）也来自拉丁 vinum：因为葡萄酒里含的是乙醇'], []),

(7798, 'vain', '''【字母变化】vanus（拉丁语）→ vain（古法语、英语）
① 拉丁语 vanus：va-nus，“空的”；词根 van- 原样留在 vanish、vanity 里。
② 到古法语，n 前面重读的 a 念成 ai（同拉丁 manus → 法语 main“手”、panem → pain“面包”），词尾的 -us 掉了：vanus → vain（也写 vein）。
③ 约 1300 年进入英语，字母没再变；ai 后来读成 /eɪ/：vain，读 /veɪn/（所以和 vein、vane 同音）。''',
 [], ['【易混】vain / vein（静脉）/ vane（风向标）三词同音。【同源】vanity（虚荣）；vainglory（虚荣心，字面“空的荣耀”）']),

(7819, 'brief', '''【字母变化】brevis（拉丁语）→ bref（古法语）→ brief（英语）
① 拉丁语 brevis：bre-vis，“短的”；词根 brev- 原样留在 brevity、abbreviate 里（这两个词是直接从拉丁语借的，所以还是 v）。
② 到古法语，词尾的 -is 掉了，v 到了词末念不出浊音，变成了 f：brevis → bref（今天法语还是 bref）。
③ 约 1300 年进入英语，先写 bref，e 读长音；后来照古法语的另一种写法写成 brief（同 chief 的 ie）；后来英语的长元音整体变了读法（元音大推移），读成 /iː/：brief，读 /briːf/。''',
 [], ['【同源】德语 Brief 是“信”。【跨语同源】日耳曼语的 merry（第 1970 组）很可能也出自 *mregh-u-']),

(7824, 'poison', '''【字母变化】potionem（拉丁语）→ poison（古法语、英语）
① 拉丁语 potio“喝；饮料”（由 potare“喝”变来），变格时写作 potion-（如 potionem：po-ti-o-nem），法语的词是从这个形式变来的；词根 pot- 原样留在 potion、potable 里。
② 这个词在法国人嘴里口头流传，ti 后面紧跟着元音，先念成 ts，又软化成一个 i 音和一个 z 音，词尾的 -em 掉了：potionem → poison（同 rationem → raison，英语 reason；traditionem → trahison，英语 treason）。
③ 约 1200 年进入英语（先写 poisoun），后来写回 poison；oi 读 /ɔɪ/，s 夹在两个元音中间读 /z/：读 /ˈpɔɪzn/。直接照拉丁语书面借的 potion 还保留 t。''',
 [], ['【同源】potion（药水）、potable（可饮用的）、beverage（饮料）。【对照】德语毒药叫 Gift，正相当于英语的 gift（给出去的东西）']),

(8185, 'crime', '''【字母变化】crimen（拉丁语）→ crimne（古法语）→ crime（古法语、英语）
① 拉丁语 crimen：cri-men，“指控、控告；罪行”，变格时写作 crimin-（如 criminis）；词根 crimin- 原样留在 criminal 里。
② 到古法语，没有重音的 e 被吞掉，m 和 n 挤在一起，后面再补一个不发音的 e：crimen → crimne。
③ mn 连着念不顺，n 也掉了：crimne → crime（今天法语还这样写）。英语 13 世纪中借来，字母没再变；i 读长音，后来英语的长元音整体变了读法（元音大推移），成了 /aɪ/，所以读 /kraɪm/（同 time）。''',
 ['【跨组同源】若取 cernere 一说，则与 certain / secret / concern（第 376 组）、crisis / critic（第 1113 组）同出 PIE *krei-“筛、分辨”；discriminate 的 discrimen“区分”就是由 discernere 派生的名词'], []),
]

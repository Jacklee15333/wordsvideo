# 进度记录与已做的判断

最新文件：`0词源拆分总表_专业术语版.xlsx`（2026-11 专业术语轮；17 列、1 张表；没有传输包、没有改动清单；维护技能 `0词源拆分表维护技能_专业术语版.skill`，视频技能 `0单词根据词源生成视频_读总表第四十版.skill`，6.4.0）。
上一版：`0词源拆分总表_词缀关系版.xlsx`（2026-11 词缀关系轮；维护技能同名版，视频技能第三十九版 6.3.0）。
再往前：`0词源拆分总表_词缀身份辨析版.xlsx`（2026-11 词缀身份辨析轮；17 列、1 张表；不再出传输包，这一轮没出改动清单；维护技能 `0词源拆分表维护技能_词缀身份辨析版.skill`，视频技能 `0单词根据词源生成视频_读总表第三十八版.skill`，6.2.0）。
再上一版：`0词源拆分总表_复杂例词清理版.xlsx`（2026-11 例词清理轮；维护技能同名版，视频技能第三十七版 6.1.2）。
更早：`0词源拆分总表_词缀来历记法版.xlsx`（2026-11 词缀来历、记法轮；17 列、1 张表；另有 _传输包.zip、_改动清单.xlsx；维护技能 `0词源拆分表维护技能_词缀来历记法版.skill`，视频技能 `0单词根据词源生成视频_读总表第三十六版.skill`，6.1.1）。
上一版：`0词源拆分总表_动词变化版.xlsx`（2026-11 拉丁语动词变化轮；维护技能 `0词源拆分表维护技能_动词变化版.skill`，视频技能第三十五版，6.1）。各轮记录按先后写在下面，最新的在最后。
这一行以前写的是：`词源拆分总表_不好拆分记忆版.xlsx`（2026-11，用户删到 16 列、1 张表，见 project_rules.md 第 57 条；更早是 `词源拆分总表_拼写变化版.xlsx`）（5 张工作表，9293 个词，「拆分结果」22 列；维护技能：`词源拆分表维护技能_拼写变化版.skill`；视频技能：`单词根据词源生成视频_读总表第十九版.skill`，3.9）

注意：下面各轮记录里写的列字母（“Q 列”“P 列”“L 列”……）是当时的列；2026-11 先在 E 后面插了 F「含义」，又在 F 后面插了 G「例句」，再把各部分解释拆成 J 前缀、K 词根、L 后缀三列，又在词根后面插了 L「单词部分」（后缀成了 M，组合 N、本次调整 U），现在的列见 project_rules.md 第 1 节。
各组本组词根对照表：见 `archive/group_roots.md`（清单 100 项，已全部完成）。

## 2026-11 音变原因轮（总表“音变原因版”，视频第四十二版）

- 用户看第四十一版 produce 的预览图：音变的原因要讲为什么这样变、p 为什么能变成 f（是不是发音相近），再举例子；身份框省字（“表示“向前”和“预先””）、“这里是…”醒目；辨析开头简写成“拉丁语，表示…”；总表、维护技能、视频技能一起改。
- 查了 Wikipedia“Grimm’s law”、Stenbrenden、etymonline，写进 yuanyin.py（SAY 发音、QI 起因、EX 例子池），第 99–102 条。
- 总表改了 348 格：318 处原因重写（前缀 198 格、词根 120 格），辨析 62 格；读回逐格比 0 处不一致。目录 30 句跟着重写（`yuanyin.py --catalog`）。体检和专业术语简化版一样（该为 0 的都是 0；rule_check 参考 29 条、合成规律一览 1 项原来就有）。
- 还能做的：别的 19 组辨析开头要不要也写成“拉丁语，…”（等用户说）；“PIE”这个缩写（294 格，多在音变列）还没换。

## 已完成

| 轮次 | 内容 | 结果 |
|---|---|---|
| 词根变体 第一轮 | 清单 1–22 | 已处理（第 10 项误筛） |
| 词根变体 第二轮 | 清单 23–42 | 89 行 |
| 词根变体 第三轮 | 清单 43–100 | 154 行（第 56、90、96、100 项误筛） |
| 补全 | 已处理组里清单外的写法 + 第一轮 8 行标签 + improvise | 117 行 |
| 整表核对 | 结构/内容/引用全查 | 修 28 处，记录 44 条（「整表核对记录」） |

Q 列共标注约 460 行；清单已全部处理（清单表已删，对照表在 archive/group_roots.md）。

## 关键判断（以后遇到同一个词别再改回去）

兄弟 / 远亲（不是由本组词根变来）：
- qual / quant（*kwo-）；mun / mut（*mei-，远亲）；plic / plex（*plek-）
- techn / tecton（*teks-）；simil / simul（*sem-：ensemble、assemble 的 semble 出自 simul；resemble 的 semble 出自 simulare，由 simil 变来）
- quadr / quart（quattuor）；fid / feder（*bheidh-）；viv / vit（*gwei-）；sacr / sanct；ward / ware（aware，*wer-）
- ward / warn（garnish、garment：etymonline 分作两个同音的 *wer-；garage 说法不一）
- fer / lat（relate、translate、superlative：ferre 借 lātus 补位，出自 *tel-）
- cri（第 1113 组）和 cern（第 376 组）是远亲（*krei-“筛”）

拼法巧合：believe/belief 的 lief、lieve 和 relief/relieve 的 lief、lieve；第 584 组 terr“吓”和第 2138 组 terra“土地”；第 513 组 curr“跑”和第 265 组 cur“操心”；第 370 组 capt“抓”和 captain 的 capt“头”；aware 的 ware“留神的”和第 813 组 ware“货物”。

说法不一（照实写了两说）：genuine 的 genu（“生”或“膝盖”）；consider、desire 是否和 sidus“星”有关；garage；gratul 的 ul；ornare 是否出自 ordo；prosper。

误筛（不改，状态写“核对”）：第 10 项 dehydration；第 56 项 extern、ter；第 90 项 robber、robbery 的 ber、bery；第 96 项 tropic（母词）；第 100 项 reci、proc、reciprocat。另有项内部分误筛：第 29 项 passer、passers、passeng；第 36 项 consequent（整项核对）；第 61 项 defying；第 65 项 authorize；第 89 项 lympic(s)。

按词根归队：scripts/archive/check_moves.py 目前只会提出 1 条建议——aware → 第 813 组，核对后**不移**（不是同一个 ware）。以后再看到这条直接从 moves.json 删掉。

## 整表核对修过的问题（别再出现）
- beggar 的解释和【构词逻辑】丢了“乞讨”两个字（全表唯一一处丢字）。
- 拆分没按母词写：chopsticks、goosebumps、zookeepers、Paralympics、11 个 X-year-old。
- 拆分和解释行数不一致：firecracker、dishwasher、burger-scented、family/life/right-sized、gymnastics、breathlessly、muddy-shelled、delicate、improvise。
- 「保留的成分」18 条例词过时，已注明“→ 现为 …”。



## 维护轮（2026-11-03）

- **见X引用修正版**：H 列约 1,700 处前后缀的“见 X”指向的只是含同一词缀的别的词。改 1,672 处（1,630 行）：词缀有母词的改见母词（334 行，-ly 见 like、-ful 见 full、self- 见 self……）；母词是拉丁语、希腊语介词的写明来源（120 行，com- 写“拉丁语 cum‘和…一起’”）；纯后缀删掉无关的“见”（1,081 行）；合成词里单词部分改见本词（71 行）。记录在「见X引用修正记录」。
- **后缀说明、意思演变**（最新文件：词源拆分_第001-195批_合并_母词补全版_用词规律扩充版.xlsx）：后缀行改写 4,054 处（来源 2,875、作用 945、在这里讲词性 3,378；母词意思过渡 115 处）；前缀 re-/un-/dis- 补来源 239 行、in- 补见 in 20 行；跨组同源恢复“见” 26 处；“意思怎么变” 6,361 行、“用词规律” 2,446 行，规律 27 种。记录在「后缀说明补充记录」「意思演变补充记录」，规律汇总在「用词规律一览」。
- 整表核对和以前一样：[5] 303、[6] 14、[7] 1，公式 0 错误。
- 还可以做：约 250 行少见后缀（-id、-ile、-ior、-ium 等）没有来源；约 360 行后缀没有“在这里”（构词逻辑读不出前面那部分）；用词规律只标了有把握的，组合列 → 行里还有不少步骤没标，可以按 usage_rules.md 再加规律、再跑。


## 精简体检轮（2026-11-03，文件：…_精简体检版.xlsx）

- **删表**：8 张早期逐条记录表全删（新增母词索引、复杂成分处理记录、保留的成分、补充说明记录、词根变体待处理、见X引用修正记录、后缀说明补充记录、意思演变补充记录），只留 4 张；「说明」重写成一页（四张表、各列、写法约定、类型、核对结果、统计、各轮调整）；「整表核对记录」旧条目里提到已删表的改成“「拆分结果」P 列”。文件 10 MB → 约 7.7 MB。
- **视频体检**：用视频技能真正的 wordfilm.js 把 9278 个词全部起草一遍，按读出来的问题改表（P 列“体检修正：…”，「整表核对记录」第 54–61 条）：
  - 构词逻辑第一行补等式 91 行（living、building、matching……；几条路用“ / ”）；补【今义】15 行（model、science、nice……）；
  - 后缀补来源 162 行（-ful、-ant、-like、-ar、-ty、-ile……）；
  - “在这里”：-ate 的“加上它”102 行，引号里的“；”108 行，不通顺的模板句约 390 处（“正在它”“和它有关的”“的的”“有日样子的”“使变得力量”……多用构词逻辑的字面意思替换），词性说错的整段重写 43 处（strengthen、wisdom、dictionary、handful、destiny、expertise……）；
  - 用词规律：tap 改标“东西变了，旧名字还接着用”，fan 去掉误标的“用进某一行”（粉丝来自 fanatic 截短），tap、fan、peep 的例子去掉①；
  - 拆分：surgery 改 surg(=chirurg) + ery；stalk 改成“stal + k（茎）；stal(=steal) + k（潜行跟踪）”；superstition 的各部分解释去掉【构词逻辑】字样。
- 视频技能同时升到 2.3（读表更宽容，见那边 SKILL.md）。用真实解析器实测：卡片配错 128 → 1（instal 是另一种拼法）、拼不出字面意思 98 → 0、后缀缺来源 464 → 0、前缀缺来源 363 → 189。
- 维护技能：词根变体、归队两块归档；新增 video_check.py（视频体检）、list_checks.py（按 L 列列出要复核的行）；sense_write.py 不再新建记录表，sense_rules.py 的模板改掉“它”占位等问题。

## 内容补全轮（2026-11-03，文件：…_内容补全版.xlsx）

起因：用户看到“精简体检版”，以为是“体验版”、还有内容没生成，要完整版。“体检”指按视频读表的规则查一遍；但表里确实还有没写全的地方，这一轮补齐（P 列“内容补全：…”“后缀说明：…”，「整表核对记录」最后几条）。

- 前缀行补来源 701 行：拉丁语（de-、in-、con-、ex-、pro-、ad- 及 ac-、ap-……）、希腊语（bio-、geo-、tele-……）、法语（en-、em-、sur-）、英语本来就有（un-、over-、out-、self-、mis-……）；a-、e-、an- 按各行写的来历分开。i-、s-、ava-、Portugu- 4 个特殊的没补，来历要单独查。
- 后缀行“在这里”全部补齐：sense_write.py 补 889 行（模板套不上的用通用写法，见 writing_guide.md 第 3 节），其中定不了词性的 127 句逐句定了词性；模板写不了的 35 行手写（once、towards、Georgian、larvae、tropics、英式拼写的 realise、memorise……）；表示“小”的词尾补上“名词 → 名词。”43 行；kitten 的 -en 是表示“小”的词尾，改正。
- 意思演变：新补 18 行（上一轮补了等式后能解析的词）。
- 视频实测（wordfilm.js 起草全表）：后缀卡片缺“在这里”973 → 39（剩下的是 -it-、-at-、-un- 这类夹在中间的成分，不讲词性）、缺词性牌 626 → 18、前缀缺来源 189 → 4。video_check.py 除提示项外全部为 0。

## 三列分工轮（文件：词源拆分总表_三列分工版.xlsx）

起因：用户发现各部分解释里写了很多“组合”的内容（之前以为表里没有组合列）。定下三列分工：拆分只拆；各部分解释只讲各部分；组合 → 现在的含义讲怎么组合、意思怎么来、用词规律。

- 各部分解释里的“在这里”4302 段 → 组合列【词性变化】（一个后缀一行）；“意思怎么变”6374 行去掉（组合列 → 行里本来就有这些步骤），〔用词规律〕标到对应那一步末尾（先按整句、再按带括号的结果配，language 的“（计算机）语言”、plan 两步都以“计划、打算”结尾的都配对了）；“用词规律”2451 行 → 组合列【用词规律】（一条一行）。共 7689 行，P 列“分列：…”，「整表核对记录」“三列分工”一条，「说明」第二、三节改了写法说明。
- 新脚本 columns.py（split / merge / check）；sense_write.py 改成三步入口（merge → sense_write_core.py → split），video_check.py 先 merge 再查，并加 h_has_combo 一项。
- 视频技能升到 2.4：从组合列读“在这里”、步骤末尾的〔用词规律〕和【用词规律】，老格式照样认。用真实解析器逐词对比：9278 个词的卡片、字面意思、今义、演变链和上一版完全一样；31 个词多读到了表里标了、旧版没读出来的用词规律（rent、tip、monkey……）。

## 组合列融合轮（文件：词源拆分总表_组合列融合版.xlsx）

起因：三列分工后，从各部分解释搬来的【词性变化】【用词规律】放在组合列最下面，和原有的步骤、【演变】各讲各的，同一个意思讲了两三遍（communicate：步骤、“所以 communicate 是交流、沟通 / 传达 / 传染”、【演变】都在讲“传达 → 交流、沟通”）。用户要求按意思融合。

- 词性变化接到等式下面（“词性变化（-ion）：……”），末尾和步骤重复的“所以 W 指……”去掉 4284 处（有步骤没讲到的意思才留着）。
- 用词规律接到第一次用到它的那一步下面（“　用词规律①：……”），编号和步骤末尾的〔用词规律N〕对上。
- 【演变】的每一项都被步骤讲到、括号说明也都在步骤里的 361 段：年代并进步骤，这一段去掉（communicate、cultural、survivor……）；其余【演变】有步骤里没有的历史，照旧保留。
- 共 5903 行，P 列“融合：…”，「整表核对记录」“组合列融合”一条，「说明」改了写法说明。每个词构词逻辑里的步骤数都没变；columns.py 再跑一遍、来回搬（merge → split）都不变。
- 视频技能升到 2.5：读融合格式（等式下的词性变化、步骤下的用词规律）；逐词对比，读到的卡片、词性牌、“在这里”、来源、字面意思、今义、演变链、规律和上一版完全一样。

## 组合列精简轮（文件：词源拆分总表_组合列精简版.xlsx）

起因：用户指出词性变化只说了词性（“-ate：变成动词”），没讲后缀本身的意思、在这个词里起什么作用；有些解释话多、没讲到重点（communication 那一大段）。要求语言适当简化、讲到核心，但不能把重要的推导删掉。

- 词性变化 4096 行改成一句：`{前面部分}“{意思}”加上 -xx（后缀的意思），就成了“{合起来的意思}”`。后缀的意思先取构词逻辑里这个后缀的注释，再取各部分解释里的说法，都没有才用常用说法（-ate 使…、-ion …这件事……）；合起来的意思先用每个词手写的字面意思，字面意思是古义、对不上前面部分的今义时按今义说（subscribe“订阅”+ -ion → 订阅这件事）。去掉讲语法的套话；母词换了意思的那句压成“（本义“…”）”。平均长度 74 → 45 字。
- 例：communicate“加上 -ate（使…），就成了‘使（东西）变成大家共有的’”；communication“communicate‘传达’（本义‘使共有’）加上 -ion（…这件事），就成了‘传达这件事’”。
- lively、orderly、elderly 构词逻辑的字面意思“有生命样子的”这类改通顺。
- 用词规律括号里本词的例子保留（试过去掉，但那是规律落到这个词上的要点，视频小黑板也要用）。推导步骤、步骤里的说明都没动。
- 视频技能升到 2.6：卡片的“在这里”配音随之变短（“在这里，就成了传达这件事”）；后缀卡片的词性图标也认“动词 → 形容词”这一句。其余（卡片、来源、字面意思、今义、演变链、规律）读到的和上一版一样。

## 用词规律改正轮（文件：词源拆分总表_用词规律改正版.xlsx）

起因：用户指出 communicator 的“沟通者 → 通信装置”标成“表示动作的词，也拿来叫做这件事用的东西”是错的——communicator 加了 -or 已经是“做…的人”，这一步是人变成机器。要求查全表。

- 写了 rule_check.py：看规律开头说的词（动作、东西、性质、名词）和这个词本身的词性对不对得上，加上“某一行”“英美”“复数”那一步有没有标记。全表查出 230 多条可疑，逐条核对。
- 新增第 28 条规律“表示‘做这件事的人’的词，也拿来叫做这件事的东西、机器”（computer 计算员 → 计算机；printer 印刷工 → 打印机）：改用它 22 处（communicator、player、controller、transformer……），补标 25 处（computer、printer、speaker、lighter……）。
- 形容词当名词用的（private 私人的 → 列兵、automatic 自动的 → 自动武器、chemical 化学的 → 化学品）改成“表示性质、状态的词，也拿来叫有这种性质的人、东西或机构”31 处；really“加重语气 → 非常”改成“说‘可怕、厉害、真的’这类词…”；birch、pup、cheat 等改成材料、比喻人、做这件事的人。
- 前提对不上、又没有合适规律的去掉 120 处（tool、machine、device 这类名词套了“表示动作的词…”；形容词“用来…的”套了“做这件事用的东西”；本来就是名词、动词的又套了“直接当名词 / 动词用”）。核对后保留 29 处。共涉及 187 个词，P 列“规律改正：…”。
- sense_rules.py 认规律时也加了这些前提检查，以后补新词不会再这样标。

## 组合列清爽轮（2026-11-04，文件：词源拆分总表_组合列清爽版.xlsx）

起因：用户看 communicator 的组合列，觉得“词性变化”单独一行和派生路线讲的是一回事，“……加上 -or（…），就成了“…””句子长，〔用词规律①〕要学生来回对编号。要求：词性变化并进构词逻辑那一行；那句话写成等式；用词规律去掉编号，需要的地方直接换行写。顺带完成上一轮“还可以做的事”里的三项。

- **组合列清爽**（P 列“清爽：…”，5776 行）：词性变化 4241 行并进第一行；后缀等式 870 行单写、3371 行和第一行一样不单写（单后缀、第一行已是等式的，如 computer）；用词规律 2407 行去掉编号、写在那一步下面（同一条再用到时只留熟悉的例子，149 行）。顺手改：几个后缀的 58 行逐个核对中间一步（thoughtlessly、fertilizer、civilization……，basically、historical、uncontrollably 多出来的行去掉）；“是一样东西或一种人，加上 -ism，指…”这类模板残句 204 句；第一行末尾“有两条路：”93 处单独成行；“所以 W 指…”17 处去掉（【今义】都有）；〔用词规律①①〕重复标 10 行；22 行第一行补上后缀的意思。
- **后缀来源进括号**（P 列“来源进括号：…”，803 行 816 处）：新脚本 src_paren.py 自动处理 704 处，手改 112 处；video_check 的 suf_src_text_only 816 → 0。注意：不少行原来正文里其实没写来源（“work 是英语本族词，配本族的 -er”被当成写了来源），这次补上了标准说法；-er 表“反复”（batter、linger、shudder）、-en 表“使…”、法语来的 -ish（publish、finish）分别给了各自的来源。
- **补背景**（P 列“补背景：…”）：105 组全部补写，audit [2c] 105 → 0。拟声词（moo、hiss、coo、ding……）讲模仿的声音和最早的年代；来源不明的照 M 列依据写“也许 / 说法不一”。
- **存疑复核**（P 列“存疑复核：…”，493 行）：逐行对照 M 列依据查表里有没有照实写“也许”。481 行已写；12 行没写的逐个看：8 行没把不确定的那层写成定论（weather、hint 写了“Watkins 认为”“看来”）；4 行补上（thousand“推测出自 *teue-”、top-notch“也许指刻度最高一格”、boring“钻孔的比喻 OED 认为说不准”、equip“很可能和 ship 同出一词”）；drew 核实古英语过去式 drōg，改 ✅。联网抽查 sly，和依据一致。现在 ⚠️ 492 行。
- 脚本：columns.py 新增清爽格式的读写（parse_I 新旧都认、compose_I 只写清爽格式）和 reformat 模式；video_check.py 加 fmt_old_pos、fmt_old_rule、fmt_not_canonical 三项；新增 src_paren.py。回归测试：split、reformat、merge → split 都是 0 行改动；video_check 全部 0；rule_check 31（基线）。
- 视频技能要跟着改才能读新格式（第一行先切掉“；词性变化…”再解析；规律行属于上面那一步），读法写在 SKILL.md。

## 还可以做的事（用户提新任务时参考）

- ⚠️ 存疑 492 行：可以用 etymonline 整站数据（工作三）先在本地逐行比，只把 etymonline 已经写成定论、表里还写“也许”的挑出来联网再查。
- ⚠️ 492 行已对照依据复核；用户要“逐组联网再核”时，按组号一批批查 etymonline，只改有出入的。
- 后缀等式现在只在第一行看不到时写；用户若要每个词都写，改 columns._eq_needed 后跑 columns.py reformat。
- 用词规律只标了有把握的，组合列 → 行里还有不少步骤没标，可以按 usage_rules.md 再加规律、再跑。
- 清单外的组里也可能有词根写法不同的情况（全表 2620 组，清单只覆盖 100 组），需要时按 archive/root_variants.md 的流程做。

## 直接母词、待核查复核轮（2026-11-04，文件：词源拆分总表_直接母词复核版.xlsx）

起因：用户看 thoughtlessly 的组合列（“thought“考虑”+ -less …；thoughtless + -ly …”），要几个后缀的词直接用直接母词：thoughtless + -ly =“不加考虑地”，标“见 thoughtless”。查下来 thoughtless 其实不在表里（上一轮补母词时 thoughtlessly 拆成 thought + less + ly，脚本没看出缺母词），用户同意补行。

- **几个后缀的 42 行**（第一行词性变化写了两个以上后缀）：补母词 15 行（派生词正上方；tropic 成了第 1927 组第一行，【背景】和 K 列【同源】随之上移），派生词 15 行改成“母词 + 最后一个后缀”；不补行的 5 行（calendarized、mascotized、opinionated、sorcerer、trashcapes）在各部分解释里讲清母词；-ical 3 行（technical、geological、mythical）；外语里的构造 19 行不动（「整表核对记录」记了一条特殊情况）。tropical 的“见 tropics”改见 tropic。P 列“直接母词：…”。
- **⏳ 待核查 113 行**：用 etymonline 整站数据（2026-01，52,126 条）逐行比，109 行 ✅；4 行 ✏️——词性变化写错：tireless（tire 是动词）、mandate（-ate 是名词，先有名词）、senate（-ate 是名词词尾）、instinctive（instinct 是名词）。❓ 3 行（unbelieve、air-draw、safe-shell）复核后仍查无，保留。P 列“联网复核：…”。
- 新脚本 insert_rows.py（补行、重排序号、改写行号引用、冻结窗格写回 F2——openpyxl 读出的 freeze_panes 是滚动位置 F2482，原样写回会冻住两千多行）。
- 体检：video_check 全 0；audit [5] 298 → 290（多后缀改直接母词后对上了），其余同基线；rule_check 31 → 30（mandate 改对词性后不再误报）；columns split / reformat 0 改动；recalc 0 错误。用词规律一览按全表重算，5 条规律各多 1 个词（新补的母词）。
- 视频技能升到 2.7：读清爽格式（wordfilm.js 的 fromQingshuang，和 columns.parse_I 同一套规则）。9293 个词逐词对比：来源、词性牌、“在这里”、字面意思、今义、演变链都和 2.6 一样；826 个词的后缀卡片改用后缀等式里的意思（communicator 的 -or 原来写成“一般加在动词后面”）；32 个多读到旧读法漏掉的规律；7 个不再念空的“在这里”；小黑板同一条规律不再写两遍。communicator、computer、thoughtlessly 做成了视频。

## 组合公式、含义列轮（2026-11-04，文件：词源拆分总表_组合公式含义列版.xlsx）

起因：用户看 communicative、communicator：第一行“派生路线：communicate（交流）→ communicative（爱交流的）”，下面紧跟着组合公式“communicate“交流”+ -ive …=“爱交流的””，两行讲同一件事，只要组合公式；【今义】从组合列挪到单词后面新加的「含义」列，组合列只讲构词逻辑和意思怎么变。

- **组合公式**（Q 列“组合公式：…”，859 行）：有后缀的 801 行（第一行改成“母词（意思）+ 后缀（后缀的意思）=“字面意思””，后缀等式不再单写；19 行母词换了意思的写“（传达，本义“使共有”）”）；没有后缀的前缀词、合成词 31 行写成 un + likely 这样；27 行手写（reusable、unthinkable、diplomat、economically……，三段拆分的、后缀等式写得不对的、带年代的）。字面意思用派生路线最后一步手写的那句（保留两条路的“ / ”），只是占位的（“…地”“这种性质”）才换成后缀等式里的。preschooler 的词性变化改对（名词 → 名词（人））。
- 保留派生路线 33 行：截短、缩写、变体（app、exam、memoir、lone……）、-men 复数（freshmen、postmen……）、defence、statistic。
- **含义列**：E 后面插 F 列「含义」，9293 个词的【今义】都挪过去，后面的列都往右挪一列（组合列现在是 J，本次调整是 Q）；冻结 G2。「说明」的列说明、写法约定、统计公式、各轮调整里的列字母，「整表核对记录」里的“P 列”这类说法都改成新列。13 个以“=”开头的今义（= neighbour：邻居）写成“（= neighbour）邻居”，免得 Excel 当成公式。
- 脚本：audit、audit_split_labels、columns、fixlib、insert_rows、list_checks、rule_check、sense_rules、sense_suffix、sense_write_core、src_paren、video_check 都改成新列号；sense_rules、sense_suffix 读今义改读含义列；video_check 的 no_jinyi 查含义列。体检和基线一样。
- 视频技能 2.8：今义从「含义」列读。9293 个词逐词对比 2.7：去掉的派生路线 857 行；母词卡片的意思改用组合公式括号里的（601 行，“相配（见 match）”→“相配”）；字面意思变了 11 个，都是原来的占位说法换成了真正的意思（distantly“…地”→“远地”）；13 个“= neighbour”开头的词，开头那句意思从“= neighbour”变成“邻居”。
- 还可以做：组合列里的【辨析】（7904 行）【趣】【语法】【例】【提醒】也可以挪出去（挪到含义列后面，或单独一列），要用户定。

## 含义词性分行轮（2026-11-04，文件：词源拆分总表_含义词性分行版.xlsx）

起因：用户要求含义列 ① 每个意思前面加词性缩写（n. / adj. / v. / prep. / phr.）；② 不同的意思写在不同的行；③ 照技能看全表还有没有别的问题。用户确认格式是“每个意思单独一行，每行前面都加词性”。

- **含义分行加词性**（Q 列“含义词性：…”，9293 行）：原来 24,167 个“；”隔开的条目，整理后 24,061 个意思，一行一个，行首写词性：n. 11671、v. 5084、adj. 4813、adv. 1056、phr. 1048、prep. 131、pron. 84、num. 59、conj. 46、int. 39、modal v. 26、aux. v. 4。
  - 词性的依据：原有括号标签约 2,700 处（“（动）（形）（n.）”换成行首词性，“（英）（口）（喻）”留在词性后面）；中文写法（…的 / …地 / 使…）；原表习惯——作者只在换词性时才标括号，第一个标签前面那几条和它词性不同（查出 hire、hook、roar、cancel 等 129 个词开头的意思判错）；组合列词性变化；ECDICT 英汉词典（skywind3000/ECDICT）释义比对；括号里的英文例句；WordNet 频率只在打平时用。
  - 人工核对：拿不准、几种依据冲突的约 2,400 条，加全部 236 个功能词（that、would、among……），改词性 610 处、整行重写 70 多处。功能词定法：情态动词 modal v.（could、may、must、should、would……），助动词用法 aux. v.（do、be、have），限定词 adj.，序数词 num.。
  - 一个意思标两个词性的（“（v./n.）出口”“（n./v.）信任、信赖”）拆成两行；同形词 ①② 写在词性后面，tap 的“② 水龙头”原来没和前一条分开，现在单独成行。
- **挪出含义列**：121 条其实是别的词（dazzling、falconer、ponytail、zero-sum……），挪到 L 列【派生】【合成】（Scorpio、Scorpius 写【联想】），110 行。
- **说明并进括号**：30 条（“复数 thieves”“也写 data set”“反义 unethical”……）。
- **补意思**：prioritise、memorise、socialise、behaviour 原来只写“同 X”；“同 colorful：色彩鲜艳的”这类 15 条改成“色彩鲜艳的（英式拼写，同 colorful）”。changed、washed 等 5 格只有“（change 的过去式、过去分词）”，改成正文。
- **内容改错**：mines 的例句“He mines coal. 他采煤”原来跟在“布雷”后面，挪到“开采”后面；组合列 26 处“见【今义】”改为“见含义列”。
- 「整表核对记录」第 87–96 条；「说明」改了 F 列说明、第三节加“含义”一行、Q 列说明、第七节加“含义词性分行”（D 列 COUNTIF Q 列“含义词性”= 9293）。F 列宽 30 → 40，行高只加高不减（3,676 行加高）。
- 脚本：新增 meaning.py（含义列读写、体检）；sense_rules.py、sense_suffix.py 读今义改用 meaning.to_old；video_check.py 加 mean_no_pos、mean_two_senses、mean_empty 三项。体检和基线一样（audit [5] 290、[6] 14、[7] 1；audit_split_labels 151；video_check 全 0；rule_check 30；columns split / reformat 0 改动；recalc 0 错误）。
- 视频技能升到 2.9：wordfilm.js 的 fromPosLines 把新写法还原成老写法再读；ety_table.py 的 meaning 去掉行首词性。9287 个词逐词对比 2.8 读上一版表：开头那句意思变了 37 个（都是原来读出“同 nonverbal”“= localize”“have been”这类说明，现在读出真正的意思；better、near、each 这类拆成两行的取第一行），8978 个词的每个意思都有了词性牌（原来只有标了括号的才有），拆分卡片、来源、字面意思、演变链、用词规律都没变。
- 一次性脚本在 scripts/archive/cixing/（自动定词性、人工核对清单、写回总表），只作记录。

还可以做：含义列的意思顺序现在照原表，用户要按词性归组（n. 的放一起、v. 的放一起）时可以再排；sense_write.py 试跑有 24 处待补的后缀说明、意思演变（见 audit_checklist.md 末尾），需要时跑一遍再核对。
- 发现：上传的表只冻结了第一行（技能约定冻结 G2）。原因是 recalc.py 用 LibreOffice 重算时把冻结的列丢了（xSplit 写成 0）；这一轮重算后用新脚本 fix_pane.py 改回 G2，以后每轮收尾都要跑。

## 例句分列轮（2026-11-04，文件：词源拆分总表_含义例句分列版.xlsx）

起因：用户看了上一版（一个意思一行、行首写词性）以后提两点：① 每个意思后面都有例子，含义不清爽，要专门生成一列放例句、例词；② 同一种词性的意思放一行，不要一个意思一行（分行太多不好看）。

- **新增 G 列「例句」**（在 F「含义」后面插一列，H 以后的列往右挪一列：类型 H、拆分 I、各部分解释 J、组合 K、背景 L、音变 M、核对结果 N、依据 O、链接 P、原表备注 Q、本次调整 R、词根变体 S）。8391 行有例句，共 18,370 个例子；每行“意思：例子”。
  - 哪些算例子：括号里英文开头的（例句、例词、搭配）；“说明：例子”拆开，说明留在含义的括号里。留在含义里的说明：中文说明、年代（1640s 起）、“X 的复数 / 比较级 / 简称”、“也叫…”、“= X”。
  - 例句里的“意思”和含义对得上：去掉括号后的意思；重了带标签（（数量、程度）高的），还重加词性（n. 聊天、闲谈）。
- **含义同词性一行**：24,064 个意思写成 12,590 行（原来一个意思一行）；词性的先后按第一次出现，同一词性里照原来的先后；同形词 ①② 按词分块。6463 行因此并了行。
- **改写**（54 行，「整表核对记录」第 98 条）：意思本身写成例句的改成中文意思（could、would、wouldn't 的请求 / 反问用法，seen、gone、shot 的过去分词，objection、exactly、done、cheer、heel、splendid 的感叹用法，it 的形式主语、指情况）；拆出例子后只剩“作定语”的写出意思（rush-hour“高峰期的”、seaview“海景的”、popcorn“爆米花式的、轻松热闹的”、pajamas“睡衣的”）；例子夹在意思中间的拆开（bit、crack、result、open-weight、attitudinal……）；拆行后没跟上的词性改正 15 处（import 的进口商品、意义，hope 的希望所寄托的人或事，mention 的提名，sprint 的迭代，lifetime、design、draft、ditch、drill、flicker、shift、decline、collapse、fence 名词义）。
- 「说明」：第二节 F、G 写在一行（“F 含义、G 例句”），后面各列字母往后挪；第三节“含义”一行改写；第六节统计公式范围跟着挪（类型 $H、背景 $L、核对结果 $N）；第七节加“含义、例句分列”（D 列 COUNTIF R 列“例句分列”）。「整表核对记录」第 97–98 条；以前各条里的“Q 列”等字母已按新列改写。
- 脚本：meaning.py 改成读“含义 + 例句”（senses / to_old / problems 都带 G 列）；所有脚本的列号 +1（G 起）；video_check 的含义检查改成 mean_no_pos、mean_dup_pos、mean_empty、mean_has_example、mean_ex_bad、mean_ex_unmatched。体检和基线一样。
- 视频技能升到 3.0：ety_table.py 认「例句」列（角色 examples）；wordfilm.js 的 fromPosLines(含义, 例句) 合成老写法；dropParens 一层层去括号。9287 个词对比上一版：开头那句变了 9 个（seen、gone、shot 不再念例句，weekend、insufficient 等去掉了括号里的小注），例子 170 个变干净（“接不可数名词：much water”→“much water”），第二个意思变了 123 个（同词性并行后先后变了），拆分卡片、来源、字面意思、演变链都没变。

## 分三列轮（2026-11-05，文件：词源拆分总表_前缀词根后缀分列版.xlsx）

起因：用户说各部分解释一列里什么都有，有点乱，软件、技能提取也难，要换成前缀、词根、后缀三列，一列解释一个部分，没有的写“-”，各部分解释这一列删掉。

- **J 前缀、K 词根、L 后缀**：原来的每一行原样分到三列（一字没改），按标签分：x- 前缀、-x 后缀（中间成分 -x- 也算后缀，两个词根中间的连接成分算词根）、没有连字符的是词根；“为什么…”跟着它提到的本词词缀；说明行提到本词词缀的放那一列，不然放词根列（20 条提到词缀但讲整个词的也放词根列）。有前缀的 1410 行、有词根的 9265 行、有后缀的 4283 行；28 个希腊、拉丁构词成分组成的词（biology、geography……）词根列是“-”。
- 列：J 以后的往右挪两列（组合 M、背景 N、音变 O、核对结果 P、依据 Q、链接 R、原表备注 S、本次调整 T、词根变体处理 U），21 列。「说明」第二节“J 前缀、K 词根、L 后缀”写一行、后面的列字母跟着挪，第三节“前缀、词根、后缀”一行改写，统计公式范围跟着挪（背景 $N、核对结果 $P、本次调整 $T），第七节加“各部分解释分三列”。「整表核对记录」第 99–100 条（100 是 28 个只有前缀、后缀的词，特殊情况）。逐行见 T 列“分三列：…”。
- 脚本：新增 cols.py（列号常量、split_parts / cells / combine / legacy / get_parts / set_parts）；读表的脚本都改成 cols.legacy(row)（三列合回一格，列号照以前 19 列）；写表的（columns.run、fixlib、sense_write_core、src_paren、insert_rows）用 cols 的常量和 get_parts / set_parts。fixlib.replace_text 不写 col 时在三列里找。体检和基线一样，sense_write 试跑和上一版一样（25 处）。
- 视频技能 3.1：ety_table.py 读表时把「前缀」「词根」「后缀」合回一格“各部分解释”（“-”不算），后面照旧。9287 个词逐词对比 3.0（读上一版表），读出来的东西完全一样（cocaine 的“coca + ine：…”读音说明跟着后缀放，才没有变）。

## 词根连字符轮（2026-11-05，文件：词源拆分总表_词根连字符版.xlsx）

起因：上一版 biology、geography 等 28 个词词根列是“-”。用户说 bio、geo、photo 应该算词根（对整个词的意思起主导作用），并要求“不管前后缀，词根都要加连字符，因为它们不是真正独立的单词”。

- 28 个词按用户同意的三类挪到词根列（第 39 条）；9 个写在词根列的前缀、后缀挪回去（debt 的 de-、-t，season 的 -on，zodiac 的 -di- 等）。
- 词根列加连字符 1556 处（加在接别的部分的那一边）；能单独用的英语单词不加。自动判断 + 约 550 处人工核对。1516 行有改动，逐行见 T 列“词根连字符：…”；「整表核对记录」第 101–103 条；「说明」第二、三节改写、第七节加“词根加连字符”。
- cols.py：legacy / combine 读的时候去掉词根标签的连字符；set_parts 写回时照原来的写法加回去（新内容照 hyphenate_root 的规矩）。体检和基线一样。
- 视频技能 3.2：ety_table 合成“各部分解释”时去掉词根连字符，另把三列各存一份（角色 prefix / root / suffix）；wordfilm 写在「词根」列的部分都当词根（ROOT_HEADS）。对比 3.1：28 + 9 个挪了列的词，另外 101 个词的部分卡片改对了（unique、union 的 un 是“一”不是“不”，real 的 re 是“东西”不是“再”，trial、comet、obese、rely、ally、Irish 等），合成词里的 in、up、out（intake、upset、outcome）原来被画成前缀卡片，现在照表画成词（词根）。

## 单词列轮（2026-11-05，文件：词源拆分总表_单词列版.xlsx）

起因：用户发现基础词（make）、合成词里的词（make-up 的 make、up）、母词（rematch、matching 的 match）都写在词根列，和真正的词根分不清，要再加一列“单词”专门放这些单词；前后缀加单词的，前后缀放词缀列、单词放单词列。

- **新增 L 列「单词部分」**（K 词根后面，后面的列往右挪一列，22 列）：能单独用的英语单词从词根列挪过来，7704 行单词部分有内容；词根列 1684 行有内容（7609 行原来写的全是单词，现在是“-”），两样都有的 95 行（yesterday = yester- + day、agriculture = agri- + culture）。三列内容一字没改，只换了列；合回一格和原来的各行一样。U 列“单词列：…”7904 行。
- **改正上一轮连字符的错判**：37 处去掉连字符（hands、days、selves、roots、crafts、behaved、did、box……）；253 处改算词根、加连字符（外语成分 tsu-、-te、de-、dino-、al-，周几的 Tues-、Thurs-、Fri-，拉丁词根 -vi-、un-、nat-、-sta-、-miss-、-the-、mod-……）；5 处前缀挪到前缀列。判断名单在 scripts/archive/danci/decisions.py。
- 「说明」：第二节“J 前缀、K 词根、L 单词部分、M 后缀”一行重写，后面的列字母、统计公式范围跟着挪，第三节写法约定、第四节③⑤补一句，第七节加“单词列”（D 列 COUNTIF U 列“单词列” = 7904）。「整表核对记录」第 104–106 条。
- 脚本：cols.py 改成四列（WPART = 12；legacy / combine / get_parts / set_parts / cells；set_parts 先照原来的列放，新行用 is_word_part 判断；合回一格时词根和单词部分按拆分先后穿插）；fixlib 的列字母到 V、replace_text 在 J–M 四列里找；insert_rows 默认 22 列。体检和基线一样：audit [5] 290、[6] 14、[7] 1；audit_split_labels 151；video_check 全 0；rule_check 30；columns split / reformat 0 改动；meaning.py 没有问题；全表 get_parts → set_parts 来回一趟 0 行变化；recalc 0 错误，fix_pane 冻结回 G2。
- 视频技能 3.3：ety_table.py 认「单词部分」（角色 word），wordfilm.js 把这一列的部分画成“单词”卡片、配音“单词是 make……”。9286 个词逐词对比 3.2（读上一版表）：6329 张卡片从“词根”改成“单词”；enthusiast、monopoly、monarch、illusion 的 en、mono、il 改成前缀卡片（它们的词根卡片随之带上词族来源）；exercise、fountain、jacket、stallion 的卡片标题去掉了漏去的连字符；字面意思、今义、演变链、来源、词性牌都没变。

## 源头词根轮（2026-11，文件：词源拆分总表_源头词根版.xlsx）

起因：用户看 people、popular：popular 拆成 people + ar，people 是“基础词”，两个都算成单词；其实两个都来自拉丁词根 popul-（音变列已经讲清了字母、读音怎么变），应该把源头词根说出来；popular 往下的 popularity、popularize 照旧在 popular 上加后缀。要求找出类似情况，一个词一个词判断。

- 查下来，表里原来写的就是 popul + ar，早先“母词替换”那一轮把拉丁词根换成了经法语变了样的英语词（U 列“母词替换：…拉丁语等原有的部分 / 拼写变化”69 行，单词部分写“在这个词里写成 popul-：拉丁语 populus 的写法；people 是它经法语变来的样子”）。这样拆，部分也拼不回这个词，视频开头的彩色分段线画不出来。
- **派生词 24 个**改回源头词根（第 42 条）：popular、populate、populous → popul-；regular、regulate → regul-；ordinary、coordinate → ordin-；determine、terminal → termin-；imagine、imaginal → imagin-；principal、principle → princip-；material、floral、criminal、hospital、humility、prejudice、poverty；majesty = maj + es + ty、imperial = im + peri + al、suspicion = su + spic + ion、debit = de + b + it。
- **外来基础词 37 个** ⑤ → ②，拆分写 people ← popul，词根列补源头词根（rule ← regul、voice ← voc、city ← civ、peace ← pac、poor ← pauper……），组合列第一行写“由源头词根 popul 变来（拉丁语 populus → 古法语 pople / peuple → people）”。
- 不改的（一个字母之差、-cle / -cul-、英语词本身就是拉丁原形、法语里组成的、本族词、动词和名词、已用 ≈ 挂好的 ②）记在「整表核对记录」第 109 条和 root_check.py 的 KEEP。
- 顺带：major、minor 的 -or 词性变化写成了“动词 → 名词（人或东西）”，改成“变成形容词”；minor 的来源括号改成比较级词尾（第 110 条）。
- U 列“源头词根：…”61 行（major、minor 记“整表核对：…”）；「整表核对记录」第 107–110 条；「说明」第二节 I 拆分、第三节写法约定、第四节 ②⑤ 的例子改写，第七节加“源头词根”。
- 新脚本 `root_check.py`（找英语词冒充母词的拆分，KEEP 名单外应为 0；`--base` 列出外来基础词供人工看）；改表脚本在 `scripts/archive/yuantou/round.py`。体检和基线一样（类型分布除外，见 audit_checklist.md）。
- 视频技能 3.4：② 变体关联、箭头后面是词根列里的源头词根时（people ← popul），配音念“people，是从拉丁语词根 popul 变来的；popul 的意思是：人民、民众”，画面和小黑板写“popul（人民、民众）→ people”；popular 的卡片从“单词是 people”变成“词根是 popul，来自拉丁语”，部分拼得回单词，开头的彩色分段线也画出来了。别的变体（made ← maked、story ← history）念法不变。

还可以做：root_check.py --base 的 62 个外来基础词，多数是同组用了另一个词根（turn / tour-、power / poss-），用户要一个个挂到源头词根上时再逐个查；community / communicate 等“只差一个字母”的，用户要改成 commun- 时照第 42 条改。

## 字母变化轮（2026-11，文件：词源拆分总表_字母变化版.xlsx）

起因：用户看了源头词根版以后说，rule ← regul、people ← popul、order ← ordin 这种单词和词根差得多的，要讲清楚是怎样一步步变过来的（经过了好几种语言），写在音变 / 字母变化列；简单的 y → i、去掉 e 不算。

- **37 个外来基础词**（第 42 条挂到源头词根上的）音变列第一行写成字母变化链，下面每一步一行（第 44 条）。中间形式、年代逐个对照 etymonline 整站数据：people（populus → pople → peuple → people）、rule（regula → reule → rule）、order（ordinem → ordene → ordre → order，n 变 r 同 Londinium → Londres）、city（civitatem → citatem → citet → cite → city）、cross（crux → 古爱尔兰语 cros → 北欧语 kross → cross）、chief（caput → *capum → chief）。原来 order、image、matter、mount、letter、prove、place、course 等音变列根本没讲字母怎么变。原来那一句讲变化的话由步骤取代，【同源】【易混】【趣】等照原文留在后面；waste、reason、chief 原来那句里的对照例子单列成【对照】，cross 补了【同源】（法语 croix、德语 Kreuz）。
- 顺带改正 flower 的【同源】（第 45 条）。
- P 列（音变 / 字母变化）列宽 40 → 50：按 40 宽有 5 行（round、waste、mount、reason、nurse）要超过 Excel 行高上限 409 磅，放宽后 37 行都放得下；别的行只是 P 列多了点空白。
- U 列“字母变化：…”37 行；「整表核对记录」第 111、112 条；「说明」第二节 P 列说明改写，第七节加“字母变化”。
- 新脚本 `zimu_check.py`；改表脚本和 37 条的写法在 `scripts/archive/zimu/`。体检和基线一样（见 audit_checklist.md）。
- 视频技能 3.5：“怎么变来的”那一幕照链一步步变字母（people 7.4 秒、rule 5.8 秒、city 9.0 秒），配音不变。

还可以做（`zimu_check.py --todo`）：② 变体关联里和源头字母差得多、音变列还没有两步以上链的 173 个（写成 ← 的 57 个多是截短、缩写；写成 ≈ 的 116 个，如 rail ≈ rule、dress ≈ direct、reign ≈ royal），拆分带 (=…) 变化大的 157 个（judge 的 dge(=dic) 这类，多数是前缀同化，不用写）。用户看过这 37 个的效果后，照同样写法往下做。

## 字母变化同源词轮（2026-11，文件：词源拆分总表_字母变化同源词版.xlsx）

起因：用户看了字母变化轮 37 个词的写法，说“可以，继续做”，接着做 zimu_check.py --todo 列出的 116 个 ≈ 词。

- **46 个写了链**（第 46 条）：链从本词自己的源头写到本词，① 讲清和 ≈ 后面那个词的关系。几个有意思的：rail ≈ rule（regula → *regla → reille → rail，g 和 l 并成“软 l”，法语写 ill，同 vigilare → veiller）；dress ≈ direct（directus → *directiare → drecier → dresser → dress）；kitchen ≈ cook（coquina → *cocina → 古英语 cycene → kitchen）；trouble（turbler → trubler，u 和 r 换位，同 bird ← brid）；danger ≈ dominate（*dominarium → dongier → dangier，o 变 a 是联想到 damnum“损害”）；solder（solidare → solder → souder → solder，l 掉了又照拉丁语写回去）。中间形式、年代逐个对照 etymonline 整站数据。
- 原有的【同源】【易混】等照原文留着；原话里步骤没讲到的补成标签段落（apprentice【短形式】prentice、scent【同类】scythe、pattern【分工】、alert【对照】alarm、issue【对照】entry）。
- **70 个不写链**：本族词 28、来源不确定 24、变化很小 18，名单记在「整表核对记录」第 114 条，zimu_check.py 的 SKIP_APPROX 不再列出。
- P 列宽 50 → 55；fixlib `_fit` 取列宽改成按范围取（以前把 K–M 当成默认宽 13，行高算高了），行高封顶 409。
- U 列“字母变化同源词：…”46 行；「整表核对记录」第 113、114 条；「说明」P 列说明补“rail ≈ rule 这类”和 ≈ 的写法，第七节加“字母变化同源词”（上一轮“字母变化”那一行的 COUNTIF 改成只数“字母变化：”，仍是 37）。改表脚本和 46 条的写法在 `scripts/archive/zimu2/`。体检和基线一样。
- 视频技能 3.6：≈ 的词“和谁是一家”那一幕也照链一步步变字母，最后一行写“rail ≈ rule（同一个来源）”。

还可以做（`zimu_check.py --todo`）：拆分带 (=…) 的 157 个，多数是 as(=ad) 这类前缀同化，不用写；值得写的是 judge 的 dge(=dic)、despite 的 spite(=spect) 这一类。写成 ← 的 57 个多是截短、缩写，值得写的只有 inch、porch、money、cousin 几个。

## 动词变化形式轮（2026-11，文件：词源拆分总表_动词变化版.xlsx）

起因：用户看了 made 的组合列，说过去式、过去分词、现在分词“也是单词，有不同的含义”，组合列只写了“当动词 / 当形容词”，没讲这些形式的作用和对意思的影响；又说不规则形式的音变要讲清，made 的“maked 怎么成了 made”这关键一步没讲。

- **154 个不规则形式**（made、took、written、found、been、went……，名单和行号在 `scripts/archive/dongci/vlist.py`）：组合列先讲作用（过去式：过去发生、已经结束；过去分词：完成、被动；当形容词：被…了的），再讲意思；【语法】补三种形式。音变列 102 个写成字母变化链，52 个写成一段说明。中间形式对照 etymonline（made：macode → makede → made，k 掉了以后 ma-ke-de 缩成 ma-de，末尾的 e 是词尾 -de 剩下的）。
- 过去分词当形容词标成用词规律的 8 处去掉（built、done、spent、sunk、given、shot、bent、worn），「用词规律一览」重算（n2adj 118 → 114 等）。
- worn 的音变原写“古英语过去分词 geworen”，改正为“本是规则的 wered，14 世纪照 bear、tear 改成 worn”。
- U 列“动词变化形式：…”154 行；「整表核对记录」第 115–117 条；「说明」N、P 两列的说明各补一句，第七节加“动词变化形式”。体检除字母变化链 83 → 185 行外，和上一版一样。
- 视频技能不用改：第十六版照样读这些链（made、wrote、found 的“怎么变来的”那一幕照链一步步变字母）。

还可以做：-ing、-ed 成对的规则形式（surprised / surprising、bored / boring……，拆分写成 动词 + ing / ed 的 400 多个），照同样的写法讲现在分词、过去分词、动名词的作用；情态动词 could、would、should、might、ought 的“过去式”也可以单独讲。

## 合成规律轮（2026-11，文件：词源拆分总表_合成规律版.xlsx）

起因：用户看了 make-up、made-up、paper-cutting 三行：带“-”的没讲连字符的作用、为什么有的加有的不加；paper-cutting 为什么不是 cutting-paper；要在组合列讲清合成词两个词的先后和意思的关系、有哪些规则，并找出别的特殊规则；三个附件（总表、两个技能）同步改。

- **规律目录**：34 条合成规律、18 条写法（scripts/hecheng_catalog.py、新工作表「合成规律一览」）。
- **组合列**：1408 个合成词、59 个带连字符的前缀词，第一行下面加“　合成规律：”（1474 行）和“　写法：”（1467 行）。各条用到的词数：主体在后 562、宾语提前 116、短语当一个词 91、外语里合成的 61、名词 + 过去分词 60、名词 + 形容词 58、有…的 53、动词短语变名词 51、老合成词 43、副词提前 42、man → men 41……；写法：用熟了连写 793、形容词加连字符 248、新词加连字符 79、like / free 这类 60、动词短语变的名词 50、前缀的连字符 47……
- 300 多行手写：外语词讲原语言的先后（republic、vinegar、terracotta、Vietnam 形容词或说明在后；kowtow、passport、portfolio、wardrobe 动词在前），命令式（scarecrow、breakfast、pastime、ceasefire、Shakespeare），并列（方位 northeast 和汉语“东北”先后相反），类名叠加（reindeer、chestnut、peafowl），有这个特点的（humpback、Bluetooth、high-five）。历史说法对照 etymonline（leopard 古人以为是狮豹杂交；island 的 s 是照 isle 加的；craftsman、salesman 的 s 是古英语“…的”；kidnap 也许、troubleshoot 很可能是倒推的）。
- **写法归拢**：散在【语法】【辨析】【提醒】、步骤括号、指路行、音变列里讲写法的话（466 行 544 处）并进写法那一行，原处删掉（第 49 条）。
- U 列“合成规律：…”1467 行；「整表核对记录」第 118–120 条；「说明」第一节改成五张工作表，第二节 N、U 两列、第三节组合列写法约定补一句，第七节加“合成规律”。
- 新脚本 `hecheng_check.py`、`hecheng_catalog.py`；这一轮的脚本在 `scripts/archive/hecheng/`。体检和基线一样（见 audit_checklist.md）。
- 视频技能 3.7：“合起来”后面多一幕 rule（一条规律一张卡，配音“英语里，规律。短语，就成了本词。”），合成规律写上小黑板“重点”第一条，带连字符的再写上写法。

还可以做：-ing、-ed 成对的规则形式（surprised / surprising）；用户要“重音”单独讲时，可以把合成名词重音在前（ˈgreenhouse）、动词短语重音在后（make ˈup）这条从写法里拆成一条合成规律。

## 英美写法轮（2026-11，文件：词源拆分总表_英美写法版.xlsx）

起因：用户看 makeover 没加连字符，问是不是美式写法；要在含义列标出是哪一边的写法、补上英式写法，并查全表有没有这种情况。

- makeover：牛津（英）、韦氏（美）都连写，英美一样（make-over 只是少见的另一种写法）；不标含义，组合列写法那一行写明，并和 make-up / makeup（英式 / 美式）对比。
- 用英美拼写对照表 breame 扫了全表单词和合成词的每一段，加上逐个列出的连字符、连写英美不同的词：含义第一行末尾统一标“（英式拼写，美式写作 X）”“（美式写法，英式写作 X）”这类说法，174 个词；原来 16 行“（英式拼写，同 X）”改成“美式写作 X”；原来零散的“（美式拼写）”“（= neighbour）”“（同 nonverbal）”去掉，一个词只写一处（第 51 条）。
- 写法英美不同的合成词，组合列写法那一行写明两边各怎么写（18 行）。
- U 列“英美写法：…”；「整表核对记录」第 121、122 条；「说明」第三节含义一行补一句，第七节加“英美写法”。
- 新脚本 `yingmei_data.py`、`yingmei_check.py`；改表脚本在 `scripts/archive/yingmei/`。视频技能不用改：含义括号里的说明视频本来就不念。

还可以做：英美说法不同的词（takeout / takeaway、sidewalk / pavement、postcode / ZIP code、apartment / flat）含义里已多半标了“（美）”“（英）”，用户要的话可以同样统一成“（美式说法，英式说 X）”。

## e 结尾加后缀轮（2026-11，文件：词源拆分总表_后缀写全版.xlsx）

起因：用户看 maker 拆成 make + r，问是不是该拆成 make + er、再去掉一个重复的 e。

- 表里同一种情况两种写法：多数写全（organize + er、time + ing、use + able），154 个按旧规矩（第 69 行“e 结尾词写 make + r”）把后缀砍短；been 写成 be + n，拼出来是 ben。统一写全后缀（第 52 条），后缀列标签、说明，组合列公式、词性变化一起改；另 29 个拆分早写全、说明还写“只加 d”的一并改。
- U 列“e 结尾：…”183 行；「整表核对记录」第 123、124 条；「说明」第三节拆分一行补一句，第七节加“e 结尾加后缀”。
- 体检：audit [5] 290 → 223、audit_split_labels 151 → 149，其余不变。
- 视频技能 3.8：单词字母按部分上色时，前一部分末尾的 e 去掉再对（mak | er）；这样 make + er、time + ing、populate + ion 这类 642 个词开头的单词也能按部分上色了，原来能上色的 5466 个词一个没变。

## 拼写变化轮（2026-11，文件：词源拆分总表_拼写变化版.xlsx）

起因：用户要求 time + ing、use + able、populate + ion 这类在后缀列补“去掉 e”，并找出别的加词缀时的特殊现象。

- 全表逐个边界对拆分和单词拼法（scripts/archive/pinxie/sp_survey.py），认出 30 种现象（第 53 条）。在词缀那一行补说明 813 处、835 行：去 e 403、双写 87、y 变 i 81、y 去掉 49、拉丁语过去分词拼法 38（decide → decision 等）、前缀同化 31、-nt 变 -nce 22、去掉末尾元音 14、去 e 的例外 14、-fy 变 -fication 12、元音变 13、-er 去 e 11、-le 变 -ly 10、留 e 9……；已经讲了的约 120 处不重复。
- 双写的字母统一单独写一部分：84 个（swim + ming → swim + m + ing、forget + able → forget + t + able），组合列公式、后缀标签跟着改；gotten 的说明里旧拆分一并改。population 组合列公式写着 + ation、拆分是 + ion，改成 + ion。
- U 列“拼写变化：…”；「整表核对记录」第 125–127 条；「说明」第三节拆分、后缀行各补一句，第七节加“拼写变化”。
- 新脚本 pinxie.py、pinxie_check.py；audit_split_labels.py 把单独一部分的双写字母、全角括号标签滤掉（149 → 31）。
- 视频技能 3.9：单词字母按部分上色，只有一部分变了样的（happy + ness → happi | ness、silent + ce → silen | ce、decide + ion → decis | ion），两头照原样对上，剩下的字母算给变了样的那一部分；能按部分上色的词比 3.7 多 1167 个，原来能上色的一个没变。

## 过去分词轮（2026-11，文件：词源拆分总表_过去分词版.xlsx）

起因：用户看 competition 拆成 compete + ition，问为什么不是直接在 compete 后面加 -ion、哪些情况要这样、是不是叫中缀，想加一列「中缀」。先答：competition 是整个从拉丁语 competitio 借来的，拉丁语的 -io 接在过去分词词干 competit- 上；严格说 it 不是中缀（中缀插在词根里面）。用户看了方案说“还是不用中缀了，这样不方便学生理解，我觉得还是从构词的角度来讲比较好”，要在拆分和后面几列讲清楚。

- **145 行拆分改成“过去分词词干(=母词) + 后缀”**（第 54 条）：-ation 71、-ition 8、-ative 6、-atory 4、-itive 3、-ator 2、-ature 2、-itor 1，原来单独拆出 it、at 的 6 行（expedition、laboratory、respiratory、signature、imperative、miniature），动词 + ion 字母变了样的 42 行（decision、description、solution、permission、reception……）。
- 每个词对照 etymonline 定来历（整个借来 / 英语照拉丁规矩造 / 英语后来用现成 -ation 造）。不规则的照实写：sensitive 照 positivus 多加了 it；sensation、constellation、literature 是名词加 -atus 造的形容词；miniature 从意大利语来。
- **27 个英语（或法语）后来自己用现成 -ation、-ative 造的词**（transportation、civilization、globalization、talkative、vaccination、aviation……）拆分不改，组合列加构词行写明，后缀列补一句。
- 原来散在单词部分、后缀列里讲“这里写成 -ition：it 是…”“e 遇到 -ition 去掉”“y 变 ic”“d(e) 遇到 -ion 变成 s”的话由词根列那一行取代；“为什么用 -ion 不用 -ment”照旧（-ation 改称 -ion）；“为什么是 division 不是 divide + -tion”这类内容被构词行取代的“为什么”行去掉。
- U 列“过去分词：…”172 行；「整表核对记录」第 128–131 条；「说明」第二节 I 拆分、第三节拆分、后缀行、组合各补一句，第七节加“过去分词词干”。
- 新脚本 `guoqu_check.py`；zimu_check.py --todo 不再把过去分词词干当“(=…) 变化大”的候选；改表脚本和逐词数据在 `scripts/archive/guoqu/`。体检数字见 audit_checklist.md。
- 视频技能 4.0：读“构词”一行做成一张绿卡“★ 构词”（配音先讲这个词怎么来，再念规律和链），词干卡片念“词根是 competit，就是 compete 的过去分词形式”，小黑板“重点”第一条写这条规律。

还可以做：reduce + tion、produce + tion 这类 -tion 词（t 也是过去分词带来的），照第 54 条写成 reduct(=reduce) + ion；-ate 动词 + ion（creation）可以在构词行里补一句“create 本身就是过去分词 creatus 变来的，所以直接加 -ion”。

## 过去分词轮（二）（2026-11，文件：词源拆分总表_过去分词音变版.xlsx）

起因：用户看了 description 这一行（拆分 descript(=describe) + ion），要求 describe → description 这类“还要在音变这一列写好是怎么变化的，为什么这样变，具体怎么变化的”；同时把上一轮说的下一步做掉：reduce + tion、produce + tion 这类改成 reduct(=reduce) + ion。

- **-tion 词 5 个**改成过去分词词干（第 54 条）：reduction、introduction、production（c 和 t 连成 ct）、nutrition（nutrit(=nutri) + ion）、mixture（mixt(=mix) + ure；英语的 mix 是 15 世纪末从 mixt 倒推出来的）。
- **150 行音变列写【字母变化】链和步骤**（第 55 条）：拉丁语原形 → 过去分词 → 拉丁语名词 → 英语；第二步按动词类型讲清过去分词怎么构成、为什么这样变（-are 动词成了 -atus、b 碰上 t 变成 p、d 碰上 t 念成 s、v 变回元音 u、复合词元音弱化……）。原来没标签的那句话 63 行由步骤取代，16 行加标签留下（【对照】【拼写】【读音】【同类】【短形式】）。
- U 列“过去分词音变：…”150 行；「整表核对记录」第 132–133 条；「说明」P 列说明补一句，第七节加“过去分词的字母变化”。
- guoqu_check.py 加 no_chain；改表脚本 scripts/archive/guoqu/round2.py（沿用 round.py 改 -tion 词，再写链）。
- 视频技能 4.1：代码不用改，新改的 5 个词照 4.0 有词干卡片和“构词”卡；音变列的这些链视频暂不读（parts 型的词不做“怎么变来的”那一幕）。

还可以做：让视频照音变列的链，在“构词”卡后面一步步变字母（照 3.5 的 variantChain）；-ate 动词 + ion（creation、education）和 act、collect、protect 这类本身就是过去分词词干的动词（action = act + ion），可以在构词行补一句“create 本身就是过去分词 creatus 变来的，所以直接加 -ion”。


## 不好拆分记忆轮（2026-11，文件：词源拆分总表_不好拆分记忆版.xlsx，另有 _传输包.zip）

起因：用户说 ④ 不好拆分的词学生记起来麻烦，要“约等于的单词”或别的办法，科学、有逻辑；再要求关联词要简单，适合基础差的学生；还要把 Excel 压小（最好 1–3 MB）。
- 118 个 ④ 全部处理（第 56 条）：≈ 8 个、← 1 个（这 9 个类型改 ②），∽ 91 个，“—”18 个；每个都在音变列第一行加【记忆】。全表类型：① 5254、⑤ 1587、③ 1408、② 935、④ 109。
- 每个词先对照 etymonline 整站数据定能不能写 ≈：词典说“也许 / 一说”的才写 ≈，并在括号里写明；其余写 ∽，明说只帮助记忆。
- 用户这版总表 16 列、1 张表（第 57 条）；文件 7.67 MB → 4.87 MB，传输包 3.33 MB（第 58 条）。
- 体检：和原表逐格比，只有类型 9 格、拆分 118 格、组合 9 格、音变 118 格变了；冻结 G2、筛选 A1:P9294 都在；LibreOffice 打开 0 错误；传输包解开后和正式版逐格一样。

还可以做：视频技能认 ∽，做一幕“和谁长得像”（配音读【记忆】那一行）；⑤ 基础词（1587 个）里难记的也可以照这一轮加【记忆】。

## 部分记忆轮（2026-11，文件：0词源拆分总表_部分记忆版.xlsx，另有 _传输包.zip）

起因：用户看了 thermostat、explore 的视频，说 thermo、stat 拆开了也不好懂，可以用约等于来记（stat ≈ stand），要分析总表，把拆开了也不好懂的部分都这样再处理；另说 ex- 的动画箭头不清楚、跑出了画面（视频技能 5.1 一起改）。
- 分析：词根列 2067 行、1402 个写法，出现在两个词以上的 347 个；前缀、后缀列里的构词成分另挑。按第 59 条写“记：”。
- 113 条规则，468 行（词根 449、前缀 16、后缀 3）。用得最多的：stand 29（sta、st、stat、sist、stitute）、catch 21、factory 18、video 14、message 13、grammar 12、spy 11、come 10、collect 10、bear 9、move 9、full 9。
- 试跑排除的误配：logistics（log = lodge）、legal（lex 法律）、college、religion（两说）、dialect（希腊语“说”）、recent（recens）、dialog（关联词就是本词另一种拼法）；absent、absence、presence 的 s(=es) 补上 ≈ is。
- 和原表逐格比，只有前缀、词根、后缀三列变了；冻结 G2、筛选 A1:P9294 都在；part_memo.py --check：468 行、写法不对 0。xlsx 4.95 MB，传输包 3.34 MB。

还可以做：剩下约 1530 行词根（多是只出现一次的）接着配；常用前缀要配的话先查是不是同源，拿不准写 ∽。

## 用词规律轮 + 同一个词根轮（2026-11，文件：0词源拆分总表_真规律同词根版.xlsx，另有 _传输包.zip、_改动清单.xlsx）

起因：用户看 camera、produce、product 三行，提了三件事——① camera 的用词规律“一个词用进某一行…就有了那一行的专门意思”讲了像没讲，要讲真正的规律；
② produce / product 的词根行写“见 reduce”“记：duct ≈ introduce”，让学生去看更复杂的词；③ duc、duce、duct 是同一个词根的不同形态，不该当几个词根讲，字母怎么变要说清。
都要求“看看总表其他地方是否也有同样的问题”。中途又定：找不到真规律的行直接删；dic 用 teach；fac ≈ do、dic ≈ teach 这类写法差得多的要补音变；port ≈ port（港口）可以有，但要讲清港口和词根的关联。

- **用词规律**（组合列，3039 行 → 2538 行，28 种说法）：取消“用进某一行”571 行、“英美不一样”290 行，逐条人工判断（scripts/archive/tonggen/codes_all.py）：
  核心意思不变 362、作用像 77、越用越窄 42、样子像 26、越用越宽 17、性质 → 东西 16、做事的人 → 东西 11、换代沿用 9……共换 592 条；找不到真规律、删掉 269 条。
  其余规律复核（codes_rev2.py）：“动作 → 用的东西”129 行里只有 30 行前提对得上，“动作 → 做出来的东西”106 行里 49 行；连同“动作当名词”“名词当形容词”里词性对不上的，删 226 条（211 个词）、改贴 60 条（改动清单里单列“请过目”一张表，等用户看过）。
  新增两条、改一条说法（第 60 条）。camera、produce、product 三行手写。
- **同一个词根**（词根列）：“由词根 X 变来”320 行改成“词根 X 的另一种写法（同一个词根）。字母变化：…”；其中 102 行原来只写“见 别的词”，补上了字母变化（照被指到的那个词的说明，stage / contrast / arrest 等单独写）；
  拆分 224 行加 (=词根)；词根行去掉指到同组派生词的“见 X”628 处（括号里只有“见 X”的换成来源）。
- **记法**：换关联词 44 行（duck 8、port 8、do 18、teach 9、climb 5，后来 fact、introduce、transport、dictionary、combat 又补上 5 行）；去掉标“记法待补”35 行；变体行改写词根本身 118 行；补“音变”270 行（SHIFT 72 条）。
- 共改 2204 格、1796 行。和原表逐格比，别的格一字不差；冻结、筛选、样式都在；改过的行重估了行高。
- 体检：video_check 全 0；rule_check 29（A 1、F 12、K 15、L 1，G 类 0）；tonggen_check 各项 0、记法待补 35；part_memo --check 438 行、五项 0，--dry 0 改动；audit [7] 和原来一样。
- 视频技能同步出 5.11（第三十三版）：读“词根 X 的另一种写法 / 字母变化 / 音变”，卡片和配音跟着改；画面可以写 when（说到哪个词出哪样东西）；起草多三项“讲的和画的”检查；新工具 matchsheet.py（逐句对照图）。

还可以做：PENDING 里的 lect、mit / miss、graph / gram 想到更简单的词再补；其余 23 种规律（当动词、当名词、复数……约 1500 行）只按词性自动查过，没有逐条看；
前缀、后缀列和单词部分列的“见 X”没动（用户只说了词根）；还有约 1500 行词根没有记法。

## 身份分工轮 + 辨析列轮（2026-11，文件：0词源拆分总表_身份分工辨析版.xlsx，另有 _传输包.zip、_改动清单.xlsx）

起因见 project_rules.md“2026-11 身份分工轮、辨析列轮定下的”开头。从用户上传的“真规律同词根版”（16 列）做起。

- **词根列只讲词根**（第 65 条）：541 格。416 行切掉“词根的意思 → 前缀“…”… → 今天的意思”的链（193 行带着前缀讲解；“意思是 / 意思：”开头的 315 行、“本组词根…→”开头的 93 行，另有“；这里是“放”…→”这类）。
  判断：抽看 introduce、efficient、condition、vocation、defy、doctor、police、satisfy、explode、immune 等，链里的步骤组合列都有、而且更详细；链里才有的东西只有拉丁语 / 希腊语原词，挪到“合起来”。
  程序另查了两样：链里括号里的外语原词在这一行别处（含本组【背景】）有没有；链里带年代、人名的话别处有没有——只查出 implement 的“1806 年起作动词”，和组合列的“1707”对不上，etymonline 是 1707，没挪。
- **“合起来”一行**（第 66 条）：132 行。自动拼出来的逐条看过，手改 9 条（gesture、except、concept、perceive、circuit、construct、commotion、provoke 补语言或改通顺；fluorescent 那句“萤石…所以叫 fluor”是词根自己的事，留在词根行）；
  fountain、catapult、hustle、couple 四行开头像“拉丁语 X…”但讲的是拼写，没挪。
- **词根的身份和分工**（第 67 条）：103 个词根族、459 行（变体 321 + 用原形的 138）。分工逐族手写，例词用程序核对过都在总表里（只有 occurred 是变化形式）。
  顺手统一了“意思”那一段：`意思是“领着走”`、`意思：站` 写成 `意思：duc“领着走”（拉丁语 ducere）`、`意思：“站”`（同族别的行有带来源的写法就用它）。
- **词缀的身份和分工**（第 67 条）：4316 行（后缀 3472 格、前缀 844 格），目录 77 种后缀用法、43 个前缀、20 个分工组。没加的约 1360 行：目录里没有的词缀，或那一行自己说的词性和组合列对不上的（discovery、melody、rehearsal 等几行组合列的“词性变化”像是写错了，没改，留给以后核对）。
- **辨析列**（第 68 条）：7879 行【辨析】整段挪到新列（第 14 列）；【同义词】行 4986 行；从同组的词补来辨析 538 行；produce、product 手写样板（含“逻辑不同”）。别处“见【辨析】”改“见辨析列”约 520 处。
- 共涉及 8805 行。新表读回来和内存里的表逐格比 0 不一致，数字列和原表一样；冻结 G2、筛选 A1:Q9294、列宽（辨析 62）都对；LibreOffice 打开 0 错误。xlsx 5.26 MB（比上传的 6.2 MB 小：共享字符串按列排 + zopfli），传输包 3.50 MB。
- 体检：shenfen_check 10 项全 0（原表：root_chain 416、heqi_in_parts 93、var_no_id 321、affix_todo 4184）；shenfen.py、cizhui.py 再跑 0 改动；tonggen_check 各项 0、记法待补 35；part_memo --check 438 行、五项 0；
  补成 22 列以后 video_check、guoqu_check、zimu_check、pinxie_check、root_check、rule_check、yingmei_check 和原表一样，hecheng_check 只有参考项 write_scattered 35 → 32（【辨析】挪走了）；columns reformat 0 改动。
  guoqu_check.py 改了一处：认“过去分词词干”的行之前先去掉“身份、分工”那一段（分工里会提到别的写法的过去分词词干）。
- 视频技能同步出 6.0（第三十四版）：四部分（读音拆分、含义拆分、同义词辨析、总结）、“身份和分工”一幕、“同义词辨析”一幕，读辨析列。起草、预览、截图、无配音渲染都试过；带配音的整段视频没有重做。

还可以做（按用户在意的先后）：
1. **辨析待补 2191 行**（`shenfen_check.py --todo`）：同义词组没有辨析的话。先做课本里常用的、学生真会混的组；每组写每个词一句 + 能讲的“逻辑不同”。
2. **“为什么用 -ous 不用 -ful”**：现在 1072 行有，其余词缀行没有。用户明确要“为什么这个单词要用 ous，却不用其他的”——要逐词查 etymonline（整个借来的 / 英语自己造的），可以先从形容词后缀（-ous、-ful、-al、-ic、-ive、-y，约 700 行）做起。
3. 【同义词】行逐组看一遍，去掉牵强的（中文说法碰巧一样、其实不混的）。
4. 词根族分工 103 条请用户过目（改动清单「词根族分工」表）；目录外的词缀（-s、re-、de-、a- 等约 1360 行）要不要也写身份。
5. 词根列里讲整词拼写变化的约 60 行，要不要挪到音变列（第 65 条没动的那一类）。
6. 上一轮留下的：PENDING 里的 lect、mit / miss、graph / gram 的记法；约 1500 行词根没有记法；其余 23 种用词规律没有逐条看。

## 拉丁语动词变化轮（2026-11，文件：0词源拆分总表_动词变化版.xlsx，另有 _传输包.zip、_改动清单.xlsx）

起因见 project_rules.md“2026-11 拉丁语动词变化轮定下的”开头。从用户上传的“身份分工辨析版”（17 列）做起。
（文件名里的“动词变化版”和上面“动词变化形式轮”的老文件撞名，不是一回事：那一轮讲英语不规则动词 made、wrote，是 22 列的老表。）
这一轮在上一个对话里做过一遍，文件用户没能下载；这是在新对话里照那次的对话记录重做的——做法、写法一样，57 族也一样多，行数这次是 318（上一遍报的是 317，差在哪一行对不出来），拉丁语形式和规律的文字是重新写的。

- **动词变化**（第 71 条）：57 个拉丁语动词词根族、318 行的词根行，在“身份：”前面加“动词变化：原形 …→ 过去式 …→ 过去分词 …；规律：…。”。只动了词根列；去掉新加的一段，318 格和原表一模一样。
  各种变法：-are 整齐的 16 族，加 s 的 10 族，重复开头的音、不变样、加 u、加 v 各 5 族，只换元音、只把元音念长各 3 族，没有单独过去式的 4 族（gradi、mirari、metiri、experiri），借别的动词的 1 族（ferre → tuli → latus）。
- **判断**（以后遇到别再改回去）：
  - 从 FAM 的 103 族里挑：这个词根是不是拉丁语动词、三个主要形式站不站得住。和动词沾边却没收的 5 族：ov（ovare 古典拉丁语里几乎只见现在分词 ovans，Wiktionary 说过去式只在后来的拉丁语里才有——这一个是联网查的）、
    batt（battuere 没有过去分词）、fid（fidere 的过去式是 fisus sum，表里的词用的是名词 fides）、gen（表里讲的是名词 genus、gens）、ped（名词 pes）。希腊语的词根族都没写。
  - 单独不用的词根写带前缀的真实动词：fend → defendere、stingu → distinguere、peri → experiri；friger 写 refrigerare（表里两个词都是它）。ple 写 plere（少见，但表里“意思”一段写的就是拉丁语 plēre）。
  - cre 族写的是 crescere → crevi → cretus（表里 5 个词有 4 个出自它：crescent、increase、decrease、concrete），create 的 creare 在规律末尾带一句。
  - mens、gest 两族的词根本身就是过去分词（metiri → mensus、gerere → gestus）：三个样子照写，规律里讲原形为什么不一样（gerere 的 r 本来是 s）。
  - fer 族：tuli、latus 是借来的，和第 25 组 relate / translate 那几行（-late：词根 lat“被带的”…ferre 没有自己的“被带的”形式）说的是同一回事，规律末尾点了 relate、translate。
  - 过去式写第一人称单数（duxi），不写第三人称；过去分词写 -us（不写词典常用的 -um），和表里“字母变化”一段一致。不写长音符号（vidi、movi、veni 的规律说“只把元音念长，写法不变”）。
  - 这一段放在“身份：”前面（先看见三个样子，再说这一行是哪个样子）；不放在“分工”后面——那样 `shenfen_check` 的 SF、视频的 `shenfenOf` 都不用动，“意思：”也还在最后。
- **脚本**：新加 `dongbian_data.py`、`dongbian.py`、`archive/dongbian/report.py`；`cols.py` 加 `strip_dongbian` / `strip_meta`；`shenfen.py`（cut）、`guoqu_check.py`、`tonggen_check.py` 看一行之前先去掉这一段；`shenfen_check.py` 加四项。
  没打补丁的上一版脚本对着新表：shenfen_check 的 root_chain 81 行（“本组词根“…”…→”被当成链）、guoqu_check 的 no_gouci / no_chain 各 96 行（“→ 过去分词 d…”被当成过去分词词干）；tonggen_check 不报错，但 split_eq、see_derived 两项对这 318 行等于不查了。
- **核对**：`dongbian.py --write` 写完读回来和“原表 + 改动”逐格比 0 不一致；另写脚本独立比了一遍（词根列 318 格、别的列 0 格、去掉新加的一段和原表不一样的 0 格；冻结 G2、筛选 A1:Q9294、列宽都没变）；
  LibreOffice 打开转成 csv，和 openpyxl 读的逐格比 0 不一致。xlsx 5.27 MB，传输包 3.50 MB。
- **体检**：shenfen_check 14 项全 0；dongbian.py 再跑“要改的格 0”；shenfen.py、cizhui.py、tonggen_check、part_memo --check，和补成 22 列以后的 video_check、guoqu_check、hecheng_check、rule_check、zimu_check、pinxie_check、root_check、yingmei_check、audit、audit_split_labels、meaning.py，输出和原表逐字一样。
- 视频技能同步出 6.1（第三十五版）：“身份和分工”那一幕画三个框、写规律、配音多一句；总结放不下分两页。起草、预览、截图、无配音渲染（produce 139.5 秒）、578 个词的画出界检查都做了；带配音的没有做。

还可以做（按用户在意的先后；身份分工轮留下的 1–6 条照旧）：
1. **请用户过目 57 族**（改动清单「动词变化」表）：形式照语法写的，没有逐个查词典。哪族不对，改 `dongbian_data.py`、`dongbian.py --write`。
2. **没有变体的动词词根**（port、scrib、mit、tract、ject、pos、press、tend……）：学生同样会问“为什么 description 有 p”。这些词根行没有“身份、分工”，视频没有那一幕；要做得先定讲在哪儿（词根卡片下面加一条？过去分词词干的词已经有“构词”卡）。
3. 没收的 5 族、希腊语词根族要不要另想讲法（希腊语的 graph / gram、ly / lysis 是“动词 / 名词”的对立，不是三个样子）。
4. 上一轮的：辨析待补 2191 行；“为什么用 -ous 不用 -ful”；【同义词】行逐组看；词根族分工 103 条过目。

## 词缀来历、记法轮（2026-11，文件：0词源拆分总表_词缀来历记法版.xlsx，另有 _传输包.zip、_改动清单.xlsx）

起因见 project_rules.md“2026-11 词缀来历、记法轮定下的”开头。从用户上传的“动词变化版”（17 列）做起。前两个对话做的试算、目录和改写程序都没留下来，第三个对话照对话记录里定下的从头做完
（对话记录只留下了最后一轮：Claude 的总结 + 用户对 bio、sub ≈ up 的两条回复）。

- **词缀来历**（第 73 条）：目录 laili_data.py 约 100 条（前缀 51 种写法 / 意思，后缀约 60 种“写法 + 变成什么词性”）。前缀、后缀列换 2855 行、补 4 行；原来就是目录那一句的 1501 行；认不出的 101 行没动。
  前缀多数写成“来自拉丁语介词 X“…”，本来是单独的一个词”；后缀讲原来是什么词尾、经什么语言进来（-ion 写明“变格时写作 -ionem，经法语磨成 -ion”）。
- **词缀记法**（第 74 条）：约 1006 行，名单是用户同意的那 20 条（-ly ≈ like 406 行、un / in / non ≈ no、ad ≈ at、dis ≈ two、pro ≈ for、sub ≈ up……）；sub ≈ up 先讲清一“下”一“上”为什么是一家。
- **动词变化**（第 75 条）：57 族规律第一句加“原形去掉词尾 -ere 就是 duc（ducere → duc）”（318 格）；规律括号里的复杂例词去掉 19 个；改完每族最多三句，视频画面三行放得下（vac、cern、quaer、cre、fer、viv 六族截图看过）。
- **复杂例词**（第 76 条）：词根行“同 …”里去掉 52 个（40 格），改动清单单列「去掉的例词（请过目）」。
- **词根记法**（第 77 条）：geo ≈ Gaia、bio ≈ zoo（写了 zoo、quick 两个可能）、vac ≈ want、logue / log ≈ logo 换掉旧的 10 行、新加 27 行（kind 5、mind 5、do 4、loose 4、logo 6 里有 logic、prologue 两行原来“记法待补”……）；index 补上 dic ≈ teach。
- 顺带：shepherdess 的 -ess 换了来历以后 cizhui 认得出了，补上身份、分工（affix_todo 才是 0）。
- 共改 3359 格（2944 行）：前缀 1067、后缀 1912、词根 378、词根变体处理 2。新表读回来和“原表 + 改动”逐格比 0 处不一致；xlsx 5.31 MB，传输包 3.51 MB。
- **体检**：补成 22 列以后的 video_check、guoqu_check、hecheng_check、rule_check、zimu_check、pinxie_check、root_check、yingmei_check、audit、audit_split_labels、meaning 输出和原表逐字一样；
  shenfen_check 14 项 0、dongbian 0、tonggen_check 0（记法待补 33）、part_memo --check 五项 0（记法行 1471：它也查前缀、后缀列里的词缀记法，-teen、-ty ≈ ten 因此把 SHIFT['ten'] 改成只给 dec 一族）、laili --check 0、lizi 0、cizhui 0。
- **视频**：第三十六版（6.1.1）只改说明，代码和 6.1 一样。用新表起草 produce、support、careless 和 6 个动词族的词：前缀、后缀卡片多了“记”框（pro ≈ for，p → f），
  配音多“记法：p r o 约等于 for 这个词……音变：p 对 f……”；三个样子的规律第一句念“原形去掉词尾 e r e 就是 d u c”。
- 脚本：新加 laili_data.py、laili.py、lizi.py、archive/laili/round.py、report.py；改了 dongbian_data.py（cut、去掉复杂例词）、dongbian.py（seg 写 cut）、part_memo_data.py（4 条换掉、4 条新加、SHIFT）。

还可以做（按用户在意的先后）：
1. **请用户过目**改动清单「去掉的例词（请过目）」52 个、「词缀来历」100 条、「来历没换的」101 行（多是这一行自己的特殊来历，要统一的话逐行改）。
2. 词缀记法的视频效果：-ly 的词每个都会多念一句“记法：l y 约等于 like……”，用户觉得啰嗦的话，可以只在 -ly 第一次出现时讲（要改视频技能，或在 prefs 里关掉）。
3. 少见的词缀（5 行以下）还没进目录；补来历只补了 4 行（别的行正文里自己讲了来源）。
4. 词根记法：还有约 1500 行没有；lect、mit / miss、graph / gram 想到更简单的词再补。
5. 上一轮留下的：57 族的拉丁语形式请用户过目；没有变体的动词词根（port、scrib、mit……）要不要也写三个样子；辨析待补 2191 行；“为什么用 -ous 不用 -ful”。

## 例词清理轮（2026-11，文件：0词源拆分总表_复杂例词清理版.xlsx，另有 _传输包.zip、_改动清单.xlsx）

起因见 project_rules.md“2026-11 例词清理轮定下的”开头：用户看 produce 那一行，前缀列还留着“（同 progress 进步：往前走）”。从用户上传的“词缀来历记法版”（17 列）做起，用了两个回合：
第一回合全表查了一遍、写好 lizi.py、试算，问了用户两件事；用户回复“先不去掉”（简单例词、“也表示“预先””都留），第二回合定名单、写回、出清单和技能。

- **词缀行的复杂例词**（第 79 条）：前缀列 451 格去掉 560 个、后缀列 563 格去掉 834 个。表里的词按它自己那一行有没有词根判断（306 种）；表里没有的 190 多种逐个看过，名单在 lizi_data.py。
- **“见 X”**（第 80 条）：32 处（product 的 pro-“见 produce”……）；proportion 一处改写。
- **词根列补漏**（第 81 条）：51 格、68 个例词（两个字母的词根、写法不一样的同一个词根、词根列里的前缀成分、表里没有的“前缀 + 词根”）。
- 共改 1065 格（1010 行）：前缀 451、后缀 563、词根 51；别的列一格没动。新表读回来和“原表 + 改动”逐格比 0 处不一致；每一处改动程序核对过只是删字、没有留下空括号和连着的分号。xlsx 5.30 MB，传输包 3.50 MB。
- **体检**：补成 22 列以后的 video_check、guoqu_check、hecheng_check、rule_check、zimu_check、pinxie_check、root_check、yingmei_check、audit、audit_split_labels、meaning，和 tonggen_check、shenfen_check（14 项 0）、
  dongbian、cizhui、shenfen、part_memo --check（1471 行、五项 0）、laili --check：新旧两张表输出逐字一样；lizi --check 四项从 989 / 32 / 1 / 53 变成 0。
  （tentacle 的 -cle 一处：去掉例词以后 cizhui 会多认出一行，把 pick_suffix 的“小”收紧到第一句，见第 82 条 ⑦。）
- **视频**：第三十七版（6.1.2）只改说明，代码不变。用新表起草 produce、product、include：前缀卡片、“记”框、身份和分工都照常；核心版本来就不念“同 例词”，详细版的“比如 X”只念留下的例词。
- 脚本：lizi.py 重写（plan_affix、ex_status、see_drop、problems、--check；词根列的 plan 补了三种认法），新加 lizi_data.py、archive/lizi2/round.py、report.py；cizhui.py 一处。

还可以做（按用户在意的先后）：
1. **请用户过目**改动清单：「去掉的例词（请过目）」1042 行、「去掉的例词汇总」621 种、「留着的例词汇总」1082 种。要恢复的照「逐格」恢复并记进名单。
2. 用户说“先不去掉”的两样：简单例词（同 unhappy、同 teacher）、“也表示“预先””这类半句——以后要去掉再做。
3. 身份、分工里的例词（pro- 多是“向前”（progress、produce））还是复杂词，视频“身份和分工”那一幕照念；要换得改 cizhui_catalog.py / shenfen_data.py 的目录。
4. 对比说明里的括号例词（include 包括）、单词部分列的“同 …”没动。
5. 上几轮留下的：词缀记法 -ly 每个词都念一遍；少见词缀没进来历目录；词根记法还有约 1500 行没有；57 族的拉丁语形式请用户过目；辨析待补 2191 行。

## 词缀身份辨析轮（2026-11，文件：0词源拆分总表_词缀身份辨析版.xlsx；没有传输包、没有改动清单）

- 起因：用户看 produce 的前缀列——开头的介绍和“身份”重复，要并成一个；“分工”改成“辨析”，把相近的前后缀都讲一讲；“记”放在身份后面；辨析不能只说来自哪里，要讲具体怎么用（规矩第 83–88 条）。
- **分了两个对话做**。第一个对话：问定两点（身份开头不加来头、所有词缀行都标“身份：”），改表（前缀 1408 行、后缀 4321 行，5672 格），20 段辨析全部重写，顺带改了挂错、认错组、来历填错的一百多行（第 87 条）；
  工具三次用到上限，最后只交了总表，维护技能和视频技能改到一半的脚本没有交付（沙盒里的文件没留下来）。
- 第二个对话（用户上传了新总表、上个对话的记录、两份旧技能）：
  - **核对总表**：5729 行词缀行全部是“标签：身份：…；记：…。辨析：…”，先后都对，没有老写法；20 段辨析没有句号、例词都在表里。又改 24 格（第 87 条）：辨析挂漏的 19 行（-ward 10、-ule 2、亲昵的 -y / -ie 7，其中 4 行来历一并改正）、来历括号插错位置的 4 行、invent 一处。
  - **维护技能照新表重做**：linetools.py 加词缀行的读写；cizhui_catalog.py 的 GROUP 从总表逐字取回（20 组），新加 suc- / sug- / sus- / ag- / al- / an- / -ule 和“向里”的 il- / ir-，例外名单 NO_BX 34 行、FORCE 6 行（对着总表定的：规则挑的和表里挂的逐行一样）；
    cizhui.py 重写（标身份、挂辨析、--check、--write、--groups）；shenfen_check.py 加四项（affix_no_id、affix_old、bianxi_bad、bianxi_diff）；laili.py、lizi.py、part_memo.py、src_paren.py 认新写法（新记法插在辨析前面）；
    cols.py 的 strip_shenfen 也去掉词缀行的记号和辨析、新加 plain_parts；video_check.py 照视频读表的样子先去掉记号、记法、辨析再查；xlsx_write.py 不再出 LZMA 传输包（pack_zip 出标准 zip，默认不出）。
  - **视频技能第三十八版（6.2.0）**：读新写法（bianxiOf）、“前缀辨析 / 后缀辨析”一幕（身份小框、辨析一条一条、最多念 3 条、省略号念“什么”）、老表照旧（老写法的 produce 前缀行，第三十七、三十八版起草逐字一样）；
    `--draft-only --preview-cell 960` 出整段视频的大预览图。用户：“先生成图片吧，不生成视频”——只起草、出了 produce 的预览图，**没有配音、没有渲染**。
- 体检（新表，新脚本）：shenfen_check 18 项 0；cizhui --check 合计 0（没加的：817 + 574、52）；tonggen_check 各项 0、记法待补 33；laili --check 四项 0、要改的格 0；lizi --check 四项 0、要改的格 0；
  part_memo --check 记法行 1472、五项 0、--dry 0；dongbian、shenfen 要改 0；补成 22 列以后 video_check 全 0、guoqu_check 151 行各项 0、hecheng_check（write_scattered 32）、rule_check 29、zimu_check、pinxie_check、root_check、yingmei_check、
  audit（[5] 242、[6] 13、[7] 0）、audit_split_labels、meaning.py 没有问题、columns.py check 0。写回后读回来和“上传的表 + 24 格改动”逐格比 0 处不一致；xlsx 5.50 MB（上传的 7.23 MB，那一版没用 zopfli）。

还可以做（按用户在意的先后）：
1. **请用户看辨析的话**：20 段都是上一个对话里写的，用户只看过 pre- / pro- / fore- 那一段；`python3 scripts/cizhui.py <表> --groups` 列出全部，哪一段没讲清就改目录、重写那一组（工作十七第 4 步）。
2. 词根列要不要也改成“身份 → 记 → 分工 / 辨析”的先后（现在是“…身份。分工。意思；记”）：等用户定。
3. 组合列约 20 行“词性变化”写错（upper、removal…）：等用户定要不要另做一轮。
4. 第 87 条 ③ 那几类没挂辨析的行；辨析里的例词要不要也按“单词 + 这个词缀”筛。
5. 视频：produce 带配音的整段还没做（新加的“再来辨析一下……”几句没听过）；用户看了预览图满意再做。
6. 上几轮留下的：少见词缀没进来历目录；词根记法还有约 1500 行没有；57 族的拉丁语形式请用户过目；辨析列待补 2191 行。

## 词缀关系轮（2026-11，文件：0词源拆分总表_词缀关系版.xlsx）

- 起因：用户看 produce 的“前缀辨析”——pre-、pro- 都是拉丁语，除了含义上的区别，还要讲两者之间的关系（“pro- 是 pre- 的分词吗？就像 duc 和 duct 这样”），所有来自同一种语言、写法不同的前后缀都看一遍，有关系就写、没有就算了；
  另一条是读音拆分：元音 + 辅音 + e 结尾的写规则的名字“元辅e结尾”（规矩第 89–92 条）。
- **分了两次回复做**：第一次工具用到上限，只说明了做到哪、发现了什么，没有交付；第二次改完交付。
- 做法：20 组辨析逐组看（每个词缀的行数、来历、记法先列出来），对着 etymonline 整站数据查了一百来个词缀的条目；10 组写了关系（2758 行），10 组不写（辨析、记法里已经讲了，或没有关系）。
  关系写进 `cizhui_catalog.REL`，`cizhui.py` 照目录整组重写；从上传的表一次写出新表（2765 格、2753 行），读回来和“原表 + 改动”逐格比 0 处不一致。
- 顺带改 8 行挂错的（第 91 条）；起先写进去、核对时去掉的：-ery 的例子“baker → bakery”（和 bakery 那一行的 bake + ery 打架）、名词 -al 和 -age 两条（来历里已经有了）。
- 脚本：linetools.py 加 bx_split / rel_items / rel_heads；cizhui_catalog.py 加 REL、CORE，NO_BX 加 7 行、FORCE 加 1 行；cizhui.py 的 plan 照目录现在的样子重写（补、改关系，NO_BX 的去掉辨析，换组），体检多一项 guanxi_bad；shenfen_check.py 19 项；laili_data.py 的 -or 条加 avoid。
- 视频技能第三十九版（6.3.0）：“关系”框和一句配音；元辅e结尾。只起草、出了 produce 的整段预览图，另起草了 important、employee、visible、actor、education、classify、forward、booklet、international、popularity、tourism、organise、pocket 看各组的配音稿和最挤的画面；**没有配音、没有渲染**。
- 体检（新表、新脚本；原表也跑了一遍，输出逐行比）：shenfen_check 19 项 0；cizhui --check 六项合计 0（没加的：suf_no_entry 824、pre_no_entry 574、suf_no_tail 52）；`--groups` 20 组共 4279 行，带关系的 2758 行；
  tonggen_check 各项 0、记法待补 33；laili --check 四项 0、要改的格 0；lizi --check 四项 0；part_memo --check 记法行 1472、五项 0；dongbian、shenfen 要改 0；
  补成 22 列以后 video_check 全 0、guoqu_check 151 行各项 0、hecheng_check（write_scattered 32）、rule_check 29、zimu_check、pinxie_check、root_check、yingmei_check 各项 0、audit（[5] 242、[6] 13、[7] 0）、meaning.py 没有问题、columns.py check 0。xlsx 约 5.7 MB。

还可以做：
1. 请用户看这 10 段关系（`python3 scripts/cizhui.py <表> --groups`），哪一段讲深了、讲浅了就改 REL 重写（工作十七第 8 步）。
2. 上一轮留下的照旧：20 段辨析用户只看过 pre- / pro- / fore-；词根列的先后；组合列约 20 行“词性变化”写错（archive、relaxing 也在里面）；辨析列待补 2191 行。
3. 音节划分表的关键解释还是“u_e：…”的写法（视频读的时候换成“元辅e结尾”）；用户要表里也改时另做。
4. 视频：带配音的整段还没做，“再看它们的关系：…”“元辅 e 结尾：…”这两句没听过。

## 专业术语轮（2026-11，文件：0词源拆分总表_专业术语版.xlsx）

用户看第三十九版 produce 的预览图，提了两类意见。一类是说法：“老祖宗的 p，英语念成 f（老祖宗 *per-“向前”；同 ped- 和 foot、patr- 和 father）——把老祖宗去掉，换成专业的说法，视频里面也要换”“produce 里面最后的关系好像写的有点问题，把 fore 也说成出自同一个老词根了”。
另一类是视频的画面（“视频页面比较花”，一页一页说了去掉什么、怎么摆——见视频技能第四十版 6.4.0）。总表这边只做第一类（project_rules.md 第 93–96 条，writing_guide.md 第 24 节）。

**做了什么**
- 新脚本 `scripts/shuyu.py`：`pro(文字)` 把“老祖宗 / 老词根 / 老音”换成专业说法，规则只看紧挨着的话；带 * 的形式分原始印欧语、原始日耳曼语（PGMC 名单）。
- 总表换了 1645 格、1368 行：前缀 460、单词部分 365、词根 284、后缀 127、背景 397、组合 6、音变 6。换出来“原始印欧语…”1657 处、“同源”327 处、“祖语词根”204 处、“源头”117 处、“原始日耳曼语…”22 处。
- pre- / pro- / fore- 的关系（62 行）整句重写：写明 fore- 是英语本族的前缀、和 pre- / pro- 同源，“一对兄弟”去掉，括号里带一句“这叫格林定律”。
- 目录同步：laili_data.py、part_memo_data.py、sense_suffix.py、cizhui_catalog.py 里的句子用同一个 `pro` 换过；references 里举例的句子也换了。
- 出表：`shuyu.py <原表> --write <新表>`（里面调 `xlsx_write.write`），写完读回来逐格比 0 处不一致。
- 体检：新表配新脚本、原表配原脚本各跑一遍全套（video_check、hecheng_check、guoqu_check、zimu_check、pinxie_check、root_check、rule_check、yingmei_check、audit、tonggen_check、shenfen_check、shenfen、bianxi、dongbian、meaning、part_memo / laili / lizi / cizhui --check、cizhui --groups），输出逐行比，只有 before 那一组的句子不同；`shuyu.py <新表>` 0。

**做的判断**
1. fore- 那句不是事实错，是说法让人误会（查了 etymonline 的 fore、fore-、for-、*per- 几条）——改说法，不改事实，回复里向用户说明了。
2. 没写出构拟形式、看不出是哪一层的，叫“祖语词根”，不硬说成原始印欧语；目录里那十来句记法（un / in / non、sub、trans、fac、dict、pan、bio、vac、thermo、measure）出处清楚，写“原始印欧语词根”。
3. 原始日耳曼语的 22 处是照构拟形式的样子（-an、-jan、-az、-ō）和记得的 etymonline 标注判断的，**没有逐个再联网查**；*dail-、*stai-、*kailo- 这几个样子像日耳曼语、etymonline 标的是 PIE，照原始印欧语写。
4. “念成”没有换成“变成”；“一家、亲戚、兄弟”这些口语没动（用户只点了“老祖宗”）；“格林定律”只写在 fore- 那一条。
5. “英语自己的老词”“古老词根”不是这回事，没动。

**还能做的事**
1. 请用户定：p 对 f、t 对 th、d 对 t、c 对 h、g 对 k 这几类“音变”要不要也标“格林定律”；“一家、亲戚”要不要也换成“同源”。
2. “祖语词根”204 处（多在【背景】）可以逐个查 etymonline，写实成原始印欧语 / 原始日耳曼语；原始日耳曼语那 22 处可以再核一遍。
3. 上一轮留下的照旧：10 段关系用户只看过 pre- / pro- / fore-；20 段辨析只看过这一组；词根列的先后；组合列约 20 行“词性变化”写错；辨析列待补 2191 行；音节划分表的关键解释还是“u_e：…”的写法。
4. 视频：第四十版的画面只出了预览图，带配音的整段还没做；词根的“身份和分工”那一幕，用户说“后续再对词根也按照前后缀的样式来写”。

## 视频界面轮（2026-11-12，文件：0词源拆分总表_专业术语简化版.xlsx）

- 起点：仓库里只有词缀关系版的表，用 shuyu.py 重新升到专业术语（1645 格，和专业术语轮的数一样，读回逐格比 0 处不一致）。
- 术语简化（第 97 条）、音变原因（第 98 条，318 处）：yuanyin.py 一次改 1527 格，读回逐格比 0 处不一致。
- 体检：video_check、laili、part_memo、cizhui、lizi、shenfen_check、tonggen、root_check、zimu、guoqu、yingmei、dongbian、shuyu、yuanyin 该为 0 的都是 0。
  和升级前的表比：mean_ex_bad 9293（例句列早先去掉了）、hecheng 的 write_scattered 3 / sheet_mismatch 1 一样；后缀来源两项 suf_no_src 111 → 107、suf_src_text_only 216 → 219（换说法以后几行的来源认法变了，没逐行看）；
  audit.py 读 17 列的表在第 80 行出错（要第 18 列），升级前的表也一样，没修。
- 视频第四十一版（6.5.0）：分段标题编号、前缀后缀特写、音变原因、三个样子分栏（见视频技能 SKILL.md）。
- 还能做的：词根特写照前后缀的样子改（用户：“后续再对词根也按照前后缀的样式来写”）；“PIE”294 格要不要换成“印欧语”。


## 2026-11 辨析精简演示轮

- 20 组辨析、10 组关系精简重写（例词紧跟用法、第一个是演示词，关系去掉“这叫格林定律”），表里 4274 格（前缀、后缀两列），读回来逐格比 0 处不一致；全套体检 0。
- cizhui.py：认上一版句子（PREV_CORE）、新体检 demo_bad；目录 DEMO_SKIP。视频第四十三版配套。
- 还能做的：别的词辨析演示的画（视频起草时“还要补”列出只有自动小图标的演示词）；音变原因里的“这叫格林定律”要不要也去掉，等用户定。

## 2026-11 词根形态轮（第 107–112 条）
- 词根列 459 格（103 个词根族）从八段改成“词根 → 形态 → 这个词 → 记”四段：57 个拉丁语动词族写原形 / 过去式 / 过去分词，46 族写名词的原形 / 所有格、形容词的原级 / 比较级 / 最高级、希腊语的原形 / 名词、法语和英语本族的原样 / 变来的样子。
- 新脚本 xingtai.py、xingtai_data.py；shenfen_check.py 的 verb_* 换成 xt_*；cols.strip_meta 去掉形态、这个词。体检：xingtai --check 0，shenfen_check 合计 0，tonggen_check 0，video_check 0，part_memo 0。
- 配套视频第四十四版（6.8.0）。下一步可以做：给只出现一种写法的拉丁语动词词根（port、mit、ject、tract、scrib……）立族、补形态。

## 2026-11 词根形态补齐轮（第 113–118 条，文件：词源拆分总表_词根形态补齐版.xlsx）
- 用户：“第二种也补上”（只出现一种写法的拉丁语动词词根）；“顺带再检查一下后缀…是不是也按照前缀的样式来进行写的”。
- 词根列 392 格：新立 174 族 + 老族补写法（fer 补 relate、translate、superlative 的 lat / late；par 补 prepare、repair、emperor；spir 补 inspire、expire、aspire；put 补 compute），curr 的 course 也排上了。数据 xingtai_verb.py（由 scripts/archive/xingtai2/build_xv.py 照 spec.py 生成，例词取当时表里的词）。
- 后缀列 2922 格、前缀列 87 格：开头的介绍先写意思（houzhui.py）。没改的后缀行：引号里的意思不止一处 319、别名或“这里…”275、来历括号不在第一段末尾 259、没有引号里的意思 227、括号里不是来历 115、照原样 7 行（4 个词）。
- 体检：新表配新脚本，和改前的表逐项比：只有 xingtai --check、shenfen_check 的 xt_missing（392 → 0）不同；tonggen、part_memo、laili、lizi、cizhui、yuanyin、shuyu、meaning、video_check、guoqu、zimu、hecheng、root_check、pinxie、yingmei、rule_check 逐字一样；读回逐格比 0 处不一致。这一轮装上了 zopfli，xlsx 约 5.7 MB。
- 视频第四十五版：起草了 important、attract、timid 的整段预览图（形态页、没有过去分词的虚线行、后缀身份框都看过），没有配音、没有渲染。
- 还能做的：① 过去分词词干行（111 个）要不要也写形态；② 来自名词、形容词的单个词根（rot、son、loc、termin、clar…）要不要像上一轮 46 族那样写“原形 / 所有格”“原级…”；③ 只经法语来的单个写法（tour、cuit、cover 的 ver）；④ 后缀没改的 1200 多行（多半是两用的 -ing、别名行）要不要逐类手改；⑤ 新族“英语里的用法”是自动拼的（“port 是“搬运”的原样（…）”“mit：英语只写一个 t（…）”），可以逐族润色。

## 2026-11 视频补词轮（第 119 条，文件：2词源拆分总表_补词版.xlsx）
- 用户要给一个单元（智能家居）的 40 个词做视频，其中 6 个总表里没有：bathroom、alarm clock、text message、health care、keep track of、depend on。
- 表的末尾新加第 196 批 6 行（第 9295–9300 行），组号挂在各自的词族上（bath 974、alarm 744、text 396、health 274、track 608、depend 285），全部写成 ③ 合成词：拆分“A + B（+ C）”，单词部分每个词一行“…（见 X）”（of 总表里没有，写“…的（介词）”）。
- 合成规律、写法照 hecheng_catalog.py 一字不改：bathroom 用 H01 + W01；alarm clock、text message、health care 用 H01 + W16（平时分开写成两个词）；keep track of、depend on 两个动词短语目录里没有对得上的，不写这两行，组合列用【提醒】讲用法（lose track of；depend 要先接 on / upon）。
- 用词规律：bathroom 的“厕所”义挂“不好直说的事，常换一个委婉的说法”（和 convenience、depart 同一条）。辨析三组：bathroom / toilet、text message / text、depend on / rely on。
- 写法：直接往原表的 sheet1.xml、sharedStrings.xml 末尾追加（每一格的样式照 bedroom 那一行，筛选范围、workbook 的定义名改到第 9300 行），没有用 openpyxl 整表重存——它会把共享字符串写成行内字符串，文件从 5.7 MB 变成 8.2 MB。zlib 9 级，约 6.2 MB（这一轮的沙盒没装 zopfli）。
- 视频第四十七版用这张表做了这 6 个词。
- 还能做的：短语进总表是第一次，video_check、hecheng_check 这些体检没有对新 6 行逐项跑；音节划分表里没有 bathroom、keep track of、depend on（视频里这几个没有读音拆分那一部分），要的话在音节表里补。

## 2026-11 考点轮（第 120 条，文件：2词源拆分总表_考点版.xlsx）
- 用户：“我想把总表再加一个内容：考点……单复数变形，比较级，最高级，高频短语，固定搭配，动词的形态变化；词性转换（比如 produce 会考 product）等等”。
- 新脚本 kaodian.py（lemminflect 变形 + 拼写规则、wordfreq 词频；`--show` 看几个词、`--write` 整列写、`--check` 体检），xlsx_write.rebuild 加一列（样式照辨析列，列宽 58），zopfli 压缩约 5.7 MB。
- 结果：9299 个词 8649 个有考点，空的 650；变形 7088 格、词性转换 4431、短语 960、用法 1027、易混 5014；格式不对的行 0。抽看过 produce、child、good、run、care、information、suggest、personal、depend、speaker、written、went、sheep、knife 等。
- 已知不足：短语只来自表里的 phr. 行（常考的 take care of 这类表里没写的就没有）；不可数名词靠词表和“不可数”字样，漏的会写成复数；词性转换偶尔会挑到不常考的同根词。视频第四十八版配套。


## 2026-11 考纲考点轮（第 121 条，文件：2词源拆分总表_考纲考点版.xlsx）
- 用户：“考点要有依据，不是说我上面提到的都要写进去，就是你看上海初中英语，上面对应的这个词常见的考点是什么……不是说啥都要写进去，那样内容太多了”；后来又说“考点依据不用加了”。
- 依据：考纲词汇表 PDF（mahavivo/english-wordlists 的副本，和考试院官网 07.pdf 核对过）→ references/kaogang/kaogang.json；评价指南 03.pdf 的知识内容；二一教育网上海词性转换复习资料；30 道能看到原题的上海中考、区模考题。
- 新的 kaodian.py + kaodian_data.py（取代第 120 条那一版）。结果：1220 个词有考点（考纲词 1742 行里多数有一两行，考纲外只写一条转换或变形），变形 465、词性转换 562、短语 224、用法 162、易混 133；一行的 957 个、两行 208 个、三行以上 55 个；格式不对的行 0；前 17 列和考点版逐格比 0 处不同。
- 试过加第 19 列「考点依据」（每条考点一行出处），用户说不用加：出处只在 --show 里看。
- 单元 40 个词里有考点的 17 个：speaker、itself、stranger、suggest、protect、guide、personal、owner、order、manage、remind、produce、understand、already、depend、depend on、truly；camera、alarm、lock、oven、heating、keep track of 等没有。
- 已知不足：真题只核对了 30 道，常考不常考主要靠考纲 + 复习资料 + 经典辨析；USAGE、CONFUSE、BAD_PAIRS 是人工整理的，可以照真题、学校资料再补；考纲是 2020 年版（找得到的最新官方版本）。

## 2026-11 练习题轮（第 122 条）
- 总表加第 19–23 列「题目1」–「题目5」，出“词源拆分总表_练习题版.xlsx”（23 列）；前 18 列和考纲考点版逐格比过，0 处不同。
- 单元表 40 个词每词 5 道（共 200 道）写进去，lianxi.py --check：40 个词、0 个有问题；选择题答案 A 26、B 25、C 28、D 24。
- 视频技能第五十一版（6.14）照读这五列。

## 2026-11 练习答案轮（第 123 条）
- 加第 24 列「答案」，出“词源拆分总表_练习答案版.xlsx”（24 列）；题目格去掉答案、解析，40 个词的答案和讲解写进答案列；lianxi.py --check：40 个词、0 个有问题。
- 视频技能第五十二版（6.15）：练习只出题，答案在总结后面一题一幕讲。

## 2026-11 读音现象轮

- 新加第 25 列「读音现象」（第 124 条）：`scripts/duyin.py`（新）、`scripts/yinbiao.py`（新，视频技能 syllables.py 的副本，字母对到音上）。
- 出表：`词源拆分总表_读音现象版.xlsx`，前 24 列和练习答案版逐格一样，2366 行（2364 个不重复的词）有读音现象。



## 2026-11-17　详细考点轮（第七十五版，第 126 条）

- 「考点」：第七十四版 1220 个词有，现在 8000 多个；7A-U4 的 40 个词手写（kaodian_hand.py），其余照 kaodian_full.py 的规则写。
- 练习题 7 道：40 个词各加两道（题目6、题目7，专门考考点），lianxi.py --check 0 个有问题。
- 文件：最新工作版/第七十五版/2词源拆分总表_详细考点版.xlsx（27 列）。


## 2026-11-17 第七十六版（初中含义轮，第 127 条）
- 加「初中含义」列（9299 个词都有；考纲词照考纲词汇表，考纲外的从含义取，7A-U4 的 40 个手写）。
- 「考点」词性转换换成“protection n.保护”的写法（2565 格）。
- 配合视频技能 6.32：只讲初中含义里的意思；配音停顿照标点；切换快的一句一个人念。样本 protect 精简版。

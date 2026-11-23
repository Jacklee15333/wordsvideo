# 项目规矩（之前几轮已定下，不要改回去）

## 目录
1. 表格结构
2. 已定下的做法（按做的先后）
3. 用户的偏好
4. 改表时的硬规矩
（后面按轮次接着写，最新的在最后：2026-11 身份分工轮、辨析列轮是第 65–70 条，拉丁语动词变化轮是第 71–72 条，词缀来历、记法轮是第 73–78 条，例词清理轮是第 79–82 条）

## 1. 表格结构

**现状（2026-11 例词清理轮以后）**：用户手里的总表是 `0词源拆分总表_复杂例词清理版.xlsx`，列没变，只在前缀、词根、后缀三列里删了复杂例词和几十处“见 X”（第 79–82 条）。

**上一版（2026-11 词缀来历、记法轮以后）**：`0词源拆分总表_词缀来历记法版.xlsx`，列和下面说的“动词变化版”一样，只改了前缀、词根、后缀三列和「词根变体处理」两格（第 73–78 条）。
**上一版（2026-11 拉丁语动词变化轮以后）**：精简表 `0词源拆分总表_动词变化版.xlsx`，只有「拆分结果」一张、17 列（批次、序号、组号、小类号、单词、含义、类型、拆分、前缀、词根、单词部分、后缀、组合 → 现在的含义、辨析、新·背景、音变 / 字母变化、词根变体处理），见第 57、70 条；列和“身份分工辨析版”一样，318 行的词根列多了“动词变化”一段（第 71 条）。下面是全表（22 列、几张表）的样子，列的分工没变。

总表 5 张工作表（2026-11-03 精简成 4 张：8 张早期逐条记录表已删；2026-11 合成规律轮加了「合成规律一览」）：

| 工作表 | 内容 |
|---|---|
| 拆分结果 | 主表，第 1 行表头，9293 个词（行 2–9294）。视频技能只读这一张 |
| 用词规律一览 | 27 条用词规律：为什么、例子、表里用到的词数和前 40 个词；sense_write.py 每次按全表重算 |
| 合成规律一览 | 34 条合成规律、18 条写法：编号、类、规律那句话（组合列照这句写）、为什么、例子、表里用到的词数和前 40 个词；`hecheng_check.py --fix-sheet` 按全表重算 |
| 整表核对记录 | 序 / 类别（已修正=绿、特殊（未改）=黄）/ 所在行（超链接）/ 单词 / 发现的情况 / 处理。逐处的改动用 fixlib.py 记；整类的批量修改记一条汇总（所在行写“—”） |
| 说明 | 一、四张工作表；二、各列；三、写法约定；四、五种类型；五、核对结果；六、统计（COUNTIF 公式，范围 $2:$9294）；七、各轮调整（每轮一行，D 列按 R / U 列计数） |

「拆分结果」各列：

| 列 | 内容 |
|---|---|
| A | 批次（1–195） |
| B | 序号（每个批次内从 1 连号） |
| C | 组号（同一词族一个组号，组内的行连在一起） |
| D | 小类号（如 306-2） |
| E | 单词 |
| F | 含义：现在的意思（2026-11 从组合列的【今义】挪过来）：同一词性的意思写一行，行首写词性，几个意思用“；”隔开（adj. 受欢迎的；流行的、大众的），不写例子；每个词都有（写法见第 29、35 条、`scripts/meaning.py`） |
| G | 例句：例句、例词，每个有例子的意思一行“意思：例子”（受欢迎的：a popular teacher）；没有例子的词留空（2026-11 新增） |
| H | 类型：① 词根词缀 / ② 变体关联 / ③ 合成词 / ④ 不好拆分 / ⑤ 基础词 |
| I | 拆分（如 `con + dit(=dic) + ion`；接在拉丁语过去分词词干上的写 `competit(=compete) + ion`（第 54 条）；④ 写【待处理】；⑤ 写“—”；② 常写 `X ← Y` 或 `X ≈ Y`；两种拆法用“；”隔开，第一种是主拆法） |
| J | 前缀：每个前缀一行 `re-：意思（来源；同 例词）`，还有跟着它的“为什么用 in- 不用 un-”、只讲这个前缀的说明；没有前缀写“-” |
| K | 词根：不能单独用的词根，加连字符（bio-、-ped-、-logue，见第 39 条；外语里的成分 tsu-、-nami 也算，见第 40 条）；两个部分中间的连接成分、双写的字母（significant 的 -i-、spokesman 的 -s-、dubbing 的 -b-）；有词根的词讲整个词来历、拼写、读音的说明；没有写“-” |
| L | 单词部分（2026-11 单词列轮新增，见第 40 条）：能单独用的英语单词，每个一行 `make：…`、`up：…`，不加连字符——基础词本身、母词、合成词里的各个词、专有名词、缩写字母代表的词，复数、过去式这些形式也算；没有词根的词（基础词、合成词）讲来历的说明也写在这里；没有写“-” |
| M | 后缀：每个后缀一行 `-ion：作用（来源；同 例词）`，中间的成分（-un-、-es-，hesitate 表示反复的 -it-）也写在这里；过去分词带来的 it、at 不单独拆，并进词干（第 54 条）；跟着它的“为什么用 -ar 不用 -al”、只讲这个后缀的说明（“-ble 结尾的词加 -ly 时…”）；没有写“-”。J、K、L、M 四列合起来就是以前的“各部分解释”（2026-11 拆开） |
| N | 组合 → 现在的含义（清爽格式）：【构词逻辑】一条线——第一行组合公式（截短、缩写、变体这类写不出组合公式的才写派生路线），末尾“；词性变化（-xx）：A → B”；第二行后缀等式“X“…”+ -xx（…）=“…””（只在第一行看不到时写）；→ / ①② 开头的意思变化行，用到规律的那一步下面紧接“　用词规律：……”（不编号）。再有【演变】（只留步骤里没有的历史）【辨析】【趣】【例】；现在的意思在 F 列「含义」 |
| O | 新·背景：只写在每组第一个词上；写【背景】…（2026-11 起 2620 组全都有）；派生词留空 |
| P | 音变 / 字母变化：字母和源头差得多的词，第一行写【字母变化】链（populus（拉丁语）→ pople（古法语）→ peuple（古法语）→ people（英语）），下面每一步一行讲清字母、读音怎么变（第 44 条）；也放【同源】【易混】【联想】【对照】【派生】【合成】 |
| Q | 核对结果（✅ 一致 / ✅ 随词族 / ✏️ 已修正 / ⚠️ 存疑 / ⏳ 待核查 / ❓ 查无） |
| R | 核对依据 |
| S | 来源链接 |
| T | 原表备注 |
| U | 本次调整：每一处改动的记录（“母词 + 词缀：…”“补充说明：…”“词根说明：…”“整表核对：…”“引用修正：…”“后缀说明：…”“意思演变：…”“体检修正：…”“含义词性：…”“例句分列：…”“分三列：…”“词根连字符：…”“单词列：…”） |
| V | 词根变体处理：“清单第 N 项 · 本组词根 X”（绿底 E2EFDA），同时 J–M 列涂浅绿 F1F8EC；清单本身已归档到 references/archive/group_roots.md |

样式：微软雅黑 10–11 号；表头白字加粗、底色 #305496；冻结 G2（单词、含义一直看得见，例句是右边第一列）；筛选 A1:V 末行；行高约每行文字 17.25 磅（按 F、G、I–P、R–T 列里最长的那一格算，见 cols.TEXT_COLS）；F 列宽 36、G 列宽 44、J 列宽 30、K、L、M 列宽 44、P 列宽 50（2026-11 字母变化轮从 40 放宽：字母变化链和步骤写得长）、自动换行；行高最多 409 磅（Excel 的上限）。

## 2. 已定下的做法（按做的先后）

1. **母词 + 词缀**：由另一个词变来的词，拆分写“直接母词 + 词缀”，用上一级母词（communication = communicate + ion，不追到 common）。母词得是这个词真正的来源：只是同一个拉丁词根经法语变了样的英语词（popular 的 people）不算母词，拆分写源头词根（第 42 条）。J–L 列母词一行写成“母词：意思（见 母词）；在这个词里写成 X-：怎么变，再加 -后缀”。表里没有的母词已在上方补行。
2. **复杂成分三步**：① 能对应常见母词就写母词（communicate = common + ic + ate；母词和这个词里的写法差得多、要靠音变列才讲得清的，写源头词根，见第 42 条）；② 没有母词但能拆就继续拆；③ 不能拆就保留。多出来的部分要么单列解释（-ic-、连接元音 i），要么说明是拉丁语原有的部分。
3. **“为什么还要加 -ate”**：-are 和 -atus 是同一个拉丁动词词尾的两种样子，英语借 -atus → -ate；-ic + -al 叠用也补了“为什么”。
4. **词根变体**：同一组里词根写法不同，在 J–L 列写明由本组词根怎么变来；不是由它变来的写明关系（兄弟、远亲、拼法巧合）。清单 100 项已全部完成（流程和写法已归档）。（2026-11 起改口径：几种写法当同一个词根讲，写“词根 X 的另一种写法（同一个词根）。字母变化：…”，见第 61 条。）
5. **按词根归队**：到目前为止没有真正需要移动的词（aware 的建议核对后否决）。
6. **整表核对**：结构、内容、引用全部核过一遍，修了 28 处，特殊情况记在「整表核对记录」。
7. **“见 X”**只能指向：这一部分的母词或变体；词缀的母词（-ful 见 full、-less 见 loose）；对记词根有帮助的跨组同源词（noct 见 night）。只是含有同一个词缀的别的词，不写“见”。（2026-11 起词根行不再指到同组别的派生词，见第 62 条。）
8. **后缀行写全三样**：作用、来源（进括号）、在这里（讲词性）；来源说法和构词动画技能一致：“英语本来就有”“来自拉丁语 -io”“来自希腊语 -istēs”；-ic、-ical 是“拉丁语、希腊语”。母词意思要过渡：先讲本义怎么变成本词用的那个意思。
9. **一词多义**的词在各部分解释加“意思怎么变”“用词规律”两行（usage_rules.md）。用户很看重用词规律：学生掌握了，才知道英语单词怎么一词多义。
10. **视频读得出来**（精简体检轮定下）：构词逻辑第一行必须有等式（几条路用“ / ”）；每个词要有【今义】；“在这里”一段不用“；”、要写“加上 -xx”、引号里不填“它”；用词规律的例子里不写①②；拆分括号里不写“+”；各部分解释里不写【构词逻辑】字样。每轮跑 video_check.py 保持 0。
12. **三列分工**（用户定下，最重要）：拆分只拆；各部分解释只讲各部分；组合 → 现在的含义讲怎么组合、意思怎么来、用词规律。原来写在各部分解释里的“在这里”（4302 段）、“意思怎么变”（6374 行）、“用词规律”（2451 行）已搬到组合列（【词性变化】、步骤末尾的〔用词规律〕、【用词规律】）。以后补内容、改表都按这个放，video_check.py 的 h_has_combo 保持 0。
15. **用词规律的前提要和词性对上**（用户指出 communicator 标错后定下）：规律开头说的是“表示动作的词”“表示东西、性质的词”“名词”，这个词就得真是那样的词；对不上又没有合适规律的，宁可不标。新增第 28 条“表示‘做这件事的人’的词，也拿来叫做这件事的东西、机器”。每次改完跑 rule_check.py。
14. **讲到重点**（用户定下）：语言适当简化、讲到核心，但推导不能删。词性变化必须讲出后缀本身的意思和在这个词里起的作用（“加上 -ate（使…），就成了‘使大家共有’”），不能只写“变成动词”；不写讲语法的套话。用词规律括号里本词的例子保留（那是规律落到这个词上的要点）。
13. **组合列融合**（用户定下）：组合列里同一个意思只讲一遍。词性变化接在等式下面，步骤讲到的意思不在末尾重复“所以 W 指……”；用词规律接在第一次用到它的那一步下面；【演变】和步骤讲同一回事时年代写进步骤、这一段去掉（只在不丢任何说明时才去），步骤里没有的历史留在【演变】。
11. **内容补全**（2026-11-03 定下）：前缀行也写来源（进括号）；拆分里的每个后缀行都有“在这里”（-it-、-at- 这类夹在中间的成分除外），模板套不上就用通用写法（writing_guide.md 第 3 节）。

全表一贯的写法习惯（不是错误，不要“统一”掉；视频 2.3 也都读得出）：
- 双写辅音：拆分写 `swim + m + ing`、`rob + b + er`、`plan + n + ed`、`forget + t + able`（双写的字母单独写一部分，后缀照原样写全；2026-11 拼写变化轮起不写 `swim + ming`，见第 53 条），M 列标签写 `-ing`、`-er`、`-ed`；e 结尾词加 -er、-ed、-en、-est 写全后缀：`make + er`、`use + ed`、`take + en`、`late + est`（两个 e 只写一个，M 列写明；2026-11 起，见第 52 条，以前写的 `make + r` 已全部改掉）。
- `-men` 复数：拆分写 `foot + men`，H 按 `footman` 写。
- 另一种拼法（instal、pickup、harbour、defense）：H 只写一句“见 主拼法”或一行同名标签。
- 拆分里带括号的写法 `cloth(e)`、`Engl(a)`、`n(e)`、`v(ideo)`，H 标签可以写全 `clothe`、`engla`、`ne`、`video`。
- 同形异义词各占一行、分在不同组：bore、lie、rose、race、scale、mine（各两行）。

## 3. 用户的偏好

- 用中文交流，语气简洁；结果说明里举具体例子。
- 重视“学生好理解”：意思路径一步步讲逻辑（“看 → 看过了 → 看到的东西 → 看法”），不要只给起点和终点；词形变化要具体（d 变 s、a 弱化成 i、经古法语磨掉 c）。
- 重视准确：用户或清单的判断不对时要直说；拿不准的写“词典说法不一 / 也许”，不编造。
- 表要清爽：不要再加逐条记录的工作表，改动写 T 列，整类修改在「整表核对记录」记一条汇总。组合列也要清爽：一样的内容放一处（词性变化和派生路线放一行），能写成等式就写等式，用词规律不编号、就近写，学生不用来回对照。
- 每轮生成新的 Excel，文件名 `词源拆分总表_<这轮做了什么>.xlsx`，方便下载保存。
- 三列各管各的：做视频时拆分看拆分列，每一部分看各部分解释，逻辑、意思、用词规律看组合列。
- 喜欢一次多做一点；范围说得前后矛盾时先问清楚；内容改写类的大改动，方向说清楚后用户会让你直接改。

## 4. 改表时的硬规矩

- 每次都从用户最新上传的文件开始做（/mnt/user-data/uploads/）；没上传就用 /mnt/user-data/outputs/ 里最新的那个，并说一声。
- 不删行；要补行（补母词）用 scripts/insert_rows.py，它会改写所有行号引用（SKILL.md 工作六）。
- 每处改动都在 T 列留一句记录。
- 只改该改的那一行/那一格。
- 以 "=" 开头的普通文字必须存成文本。
- 出文件前跑 recalc.py（0 错误），再跑 fix_pane.py（重算会丢掉冻结的列）、audit.py 和 video_check.py（和基线一致）。

## 2026-11 组合列清爽轮定下的（接在第 2 节后面看）

16. **组合列清爽格式**（用户定下）：词性变化并进【构词逻辑】第一行（“；词性变化（-or）：动词 → 名词（人或东西）”，几个后缀接成一条）；后缀那句写成等式“communicate“传达、交流”+ -or（做…的人或东西）=“传达、交流的人””；用词规律去掉〔用词规律①〕和编号，直接换行写在用到它的那一步下面，“学生不会去一个个查，只要知道这里的规律是什么、怎么用”。
17. **后缀等式和第一行重复时不单写**（本轮的默认判断，用户问过、回复“继续”）：第一行本身就是“前面部分 + 后缀 = 字面意思”的单后缀词（computer、communicate），等式和它一字不差，不再写；派生路线、几个后缀、第一行看不到的本义才写。用户若要每个词都写，改 `columns.py` 的 `_eq_needed` 后跑 `columns.py reformat`。
18. **几个后缀的词逐个讲中间一步**：每个后缀一行等式，前一个的结果是后一个的前面部分（thought + -less =“没有考虑的”；thoughtless + -ly =“不加考虑地”）。拆分只有一个后缀的（basically = basic + ally），不再另写 -ly、-ic、-al 行。
19. **后缀来源一律进括号**：“（来源；同 例词）”，正文不再写“它本身来自…”“拉丁语…词尾 -ior，…”；正文其实没写来源的，补这个后缀的标准说法（src_paren.py 的 STD）。来源和“这里不是…而是…”连在一起的，括号里写“这里来自 …”。
20. **每组都有【背景】**：原来写“—”的 105 组已补；来源不明的照依据写“也许 / 说法不一”，不编造。
21. **⚠️ 存疑的复核口径**：查的是“表里有没有照来源写明不确定”。写成定论的补“也许 / 很可能 / 推测”，P 列仍是 ⚠️；核实其实没有疑问的改 ✅；Q 列末尾记“复核（年月）：…”。

## 2026-11 直接母词轮定下的

22. **几个后缀的词用直接母词**（用户定下）：“thoughtless 本身也是一个单词，而且也讲解了，标注 见 thoughtless 就可以了，让学生去看 thoughtless”。thoughtlessly = thoughtless + ly，组合列只有一个等式、一个词性变化；中间那个词不在表里的，常用的补成新行（15 行：thoughtless、breathless、aimless、fertilize、civilize、civilise、industrialize、urbanize、linguist、binocular、tropic、furnishing、crackle、sophisticate、containerize），生僻、临时造或已废的不补行、在各部分解释里讲清（calendarize、mascotize、opinionate、sorcer、trashcape）。
23. **哪些不改**：中间一步只在拉丁语、希腊语、法语、意大利语里有的（dictionary、cultivate、spaghetti、broccoli……共 19 个）照“复杂成分三步”逐个写等式；scissor、tweezer 是从复数倒推的，不是母词；-ical 当一个后缀（technical = techn + ical、geological = geology + ical、mythical = myth + ical）。
24. **补母词的行**：放在派生词正上方，批次、组号、小类号随派生词；T 列写“直接母词：新增母词，为第 N 行 X 补出”，派生词 T 列写“直接母词：拆分 A → B（母词 X 已补在第 N 行）”；母词的年代、意思演变挪到母词那一行，派生词只留自己的。
25. **联网复核用 etymonline 整站数据**：先在本地逐行比（SKILL.md 工作三），再联网查数据里没有的；Q 列写“联网复核（年月）：etymonline X 条目：要点；与表里一致 / 表里已改：…”，R 列写“etymonline · 条目”。

## 2026-11 组合公式、含义列轮定下的

26. **组合列只写组合公式，不写派生路线**（用户定下）：“派生路线：communicate（交流）→ communicative（爱交流的）”和紧跟着的“communicate“交流”+ -ive …=“爱交流的””讲的是同一件事，只留组合公式：`communicate（交流）+ ive（有…性质的、会…的、爱…的）=“爱交流的”；词性变化（-ive）：动词 → 形容词`。字面意思用原来派生路线最后一步手写的那句（两条路的“ / ”、几个意思的“；”都留着），母词换了意思的写“（传达，本义“使共有”）”。截短、缩写、变体、-men 复数、倒推出来的写不出组合公式，保留派生路线（33 行）。
27. **今义挪到「含义」列**（用户定下）：单词后面新增 F 列「含义」，原来组合列最后的【今义】都挪过去；组合列“只负责解释构词逻辑、不同含义是怎样演变的”。【辨析】【趣】【语法】【例】【提醒】这些补充说明这一轮没动，还在组合列，用户要挪时再挪。
28. **「拆分结果」18 列**（2026-11 例句分列轮起是 19 列，见第 36 条）：A 批次、B 序号、C 组号、D 小类号、E 单词、F 含义、G 类型、H 拆分、I 各部分解释、J 组合 → 现在的含义、K 新·背景、L 音变 / 字母变化、M 核对结果、N 核对依据、O 来源链接、P 原表备注、Q 本次调整、R 词根变体处理。冻结 G2。

## 2026-11 含义词性分行轮定下的

29. **含义行首写词性**（用户定下：“含义前面要加上词性缩写”“不同的含义要在不同的行”“每个意思单独一行，每行前面都加词性”；同月看了以后改成同词性一行、例子另放一列，见第 35 条，这里“一行一个意思”的几条作废）：
    - 行首是词性缩写加一个空格：n. 名词、v. 动词、modal v. 情态动词、aux. v. 助动词（do、be、have 构成疑问、否定、时态的用法）、adj. 形容词、adv. 副词、pron. 代词、prep. 介词、conj. 连词、num. 数词、art. 冠词、int. 感叹词、phr. 短语（固定搭配、习语、短语动词：phr. carry out 执行）。
    - 标签写在词性后面：`n. （英）酒馆、酒吧（go to the pub）`；同形词的 ①② 写在词性后面：`v. ① 轻拍、轻敲`、`n. ② （英）水龙头`。
    - 一行只写一个意思；括号里的例子可以用“；”。同一个意思兼两种词性（原来标“（v./n.）”的）写两行：`v. 出口` / `n. 出口`。
    - 意思的先后照原来的，不按词性重新归组（作者原来的顺序就是讲解的顺序；视频的开头那句用第一行）。
    - 限定词（every、each、some、no）写 adj.；代词用法写 pron.；序数词（first、second、twentieth）写 num.，“…分之一”写 n.；“the + 形容词”（the poor、the wealthy）写 n.。
30. **不是这个词的意思的，挪出含义列**：派生词（dazzle 下的 dazzling、falcon 下的 falconer）写到 O 列【派生】，合成词（pony 下的 ponytail、zero 下的 zero-sum）写【合成】，scorpion 的 Scorpio、Scorpius 写【联想】（121 条、110 行）。含这个词的固定搭配（mineral water、spill the beans）是这个词的用法，留在含义列写 phr.；变体本身的意思（folks、baggies、the homeless）留在含义列。
31. **说明并进括号**：“复数 thieves”“也写 data set”“反义 unethical”这类不是意思的，并进上一个意思后面的括号（用“；”接在括号里，括号里再有括号的压平：“反义 unavoidable“不可避免的”更常用”）。
32. **拼写变体写意思**：不写“同 colorful：色彩鲜艳的”“同 prioritize（英式拼写）”，写“色彩鲜艳的（英式拼写，同 colorful）”；只写了“同 X”的补上意思（prioritise、memorise、socialise、behaviour）。
33. 组合列里指向【今义】的“见【今义】”一律写“见含义列”。
34. 词性怎么定的（以后补新词照这个定）：原有的括号标签（“（动）（形）（n.）”）→ 中文写法（“…的”adj.、“…地”adv.、“使…”v.）→ 原表习惯：作者只在换词性时才加标签，所以第一个标签前面那几个意思的词性和这个标签不同 → 组合列的词性变化、ECDICT 释义、括号里的英文例句；拿不准的、功能词逐条人工定（这一轮人工核对约 2,600 条）。

## 2026-11 例句分列轮定下的

35. **含义同词性一行，例子另放 G 列「例句」**（用户定下：“每个含义后面都有例子，我希望再专门生成一列，用来放例句，例词”“同一种词性的放一行，不要换行”）：
    - 含义：一个词性一行，行首词性加一个空格，意思之间用“；”：`adj. 受欢迎的；流行的、大众的；通俗的；民众的`。词性的先后按第一次出现的先后；同一词性里意思的先后照原来的。
    - 同形词：①② 写在词性后面，每个词的几行连在一起，第二个词从“② …”那一行起（tap：`v. ① 轻拍、轻敲；（触屏）轻点` / `n. 踢踏舞` / `n. ② （英）水龙头` / `phr. tap water 自来水；on tap …` / `v. 开发利用；窃听`）。
    - 例句：每个有例子的意思一行“意思：例子；例子”；“意思”是含义里那个意思去掉括号的样子，重了的带上标签，再重的前面加词性。英文开头的括号内容（例句、例词、搭配）都算例子；年代（1910 年已见）、“X 的复数 / 比较级 / 简称”、“也叫…”、“= X”、中文说明留在含义的括号里。“说明：例子”的拆开，说明留下、例子挪走（“（接不可数名词：much water）”→ 含义“许多的（接不可数名词）”、例句“许多的：much water”）。
    - 意思本身写成例句的改写成中文意思（could“（委婉请求）Could you help me?”→“（委婉请求）能…吗”，例句挪走；seen“I have seen it.”→“see 的过去分词”；rush-hour“作定语：rush-hour traffic”→“（作定语）高峰期的”）。
36. **「拆分结果」19 列**（2026-11 分三列轮起是 21 列，见第 37 条）：A 批次、B 序号、C 组号、D 小类号、E 单词、F 含义、G 例句、H 类型、I 拆分、J 各部分解释、K 组合 → 现在的含义、L 新·背景、M 音变 / 字母变化、N 核对结果、O 核对依据、P 来源链接、Q 原表备注、R 本次调整、S 词根变体处理。冻结 G2。「说明」第二节把“F 含义、G 例句”写在一行（第二节没有空行可加）。

## 2026-11 分三列轮定下的

37. **各部分解释拆成前缀、词根、后缀三列**（用户定下：“各部分解释换成三列：前缀，词根，后缀；每一列个解释一个部分”“有前缀，词根，后缀的就写上内容，没有的就用 -”“各部分解释这一列删除掉”）：
    - J 前缀：标签以“-”结尾的行（re-、un-、dif-、bio-）；K 词根：没有连字符的标签（people、shoe、maker、ped、6th-grader）；L 后缀：标签以“-”开头的行（-ion、-er、-logy）和中间的成分（-it-、-at-、-un-、-m-）。两个词根中间的连接成分写在词根列（significant 的 -i-、spokesman 的 -s-、nightingale 的 -in-；delight 的 -gh- 是拼写说明，也在词根列）。
    - “为什么…”行跟着它第一个提到的、本词拆分里有的前缀或后缀（“为什么用 -ar 不用 -al”→ 后缀列，“为什么用 in- 不用 un-”→ 前缀列）；没提词缀的（“为什么是 nunci 不是 nounc”“为什么不是 satisfication”）放词根列。
    - 说明行（没有部分标签的、“注意：”“来历：”“拼写：”“读音：”开头的）：提到本词的某个前缀、后缀的放那一列（“-ble 结尾的词加 -ly 时…”“注意：这个 -or 表示人、东西”）；讲整个词来历的放词根列（20 条提到了词缀但讲的是整个词：princess“英语自己用 prince + -ess 造的”、submarine、painter、irony……，名单在 cols.NOTE_ROOT）。“coca + ine：…”这种讲拼起来以后读音的，跟着最后那个后缀。
    - 一列没有内容写“-”。（28 个由希腊、拉丁构词成分组成的词，这一轮先照标签放，下一轮用户定下按词根算，见第 39 条。）
    - 三列的内容就是原来的各行，一字没改；合起来（前缀、词根、后缀的先后）和原来比，9293 行里 453 行行的先后变了（说明行挪到了它讲的那一列），视频读出来的东西一样。
38. **「拆分结果」21 列**：A 批次、B 序号、C 组号、D 小类号、E 单词、F 含义、G 例句、H 类型、I 拆分、J 前缀、K 词根、L 后缀、M 组合 → 现在的含义、N 新·背景、O 音变 / 字母变化、P 核对结果、Q 核对依据、R 来源链接、S 原表备注、T 本次调整、U 词根变体处理。冻结 G2。「说明」第二节把“J 前缀、K 词根、L 后缀”写在一行。脚本的列号都在 `scripts/cols.py`。

## 2026-11 词根连字符轮定下的

39. **词根加连字符，构词成分算词根**（用户定下：“bio、geo、photo 这些应该算词根，对整个单词的含义起主导作用”“不管前后缀，词根都要加连字符，因为他们不是真正独立的单词”）：
    - 连字符加在接别的部分的那一边：在拆分里排第一的写 X-（vis-、bio-、hes-），中间的写 -X-（-ped-、-sati-、连接元音 -i-、双写的 -t-），最后的写 -X（-spect、-port、-logue）。照拆分列的位置定（`cols.split_positions`）。
    - 不加的：能单独用的英语单词——母词（popular、count）、合成词里的词（shoe、maker、in、up、out）、专有名词（Hamburg、Canton）；不是拆分里的一部分、只是讲来历时提到的词（people、slupan）；缩写里的大写字母（scuba 的 B）。
    - 英语单词在这里当拉丁、希腊词根用的要加：说明以“由词根”“本组词根”“= 拉丁语 / 希腊语…”开头、又没写“（见 自己）”的（transport 的 -port、relate 的 -late、remember 的 -member、prevent 的 -vent）。自动判断以后，拿不准的约 550 处逐条看过（名单在 scripts/archive/sanlie/round2/decide.py 的 FREE / BOUND）。共加 1556 处。
    - 构词成分算词根（28 个词）：bio、geo、photo、hydro、psycho、thermo、astro、electro、archaeo、aut、rock、Portugu 从前缀列挪到词根列；dialogue、monologue、prologue、catalogue、apology 的 -logue / -logy，multiple、triple 的 -ple，trillion 的 -llion 从后缀列挪到词根列（dia-、mono-、pro-、cata-、apo-、multi-、tri- 仍是前缀）；unify、twice、trio 的 uni-、twi-、tri- 挪到词根列（-fy、-ce、-o 只是词尾）。-logy“…学”、-graphy、-nomy、-metry、-gen 接在构词成分后面时仍算后缀。
    - 原来没写连字符、被分到词根列的前缀、后缀挪回去：debt 的 de-、beside 的 be-、enthusiasm 的 en-、reinforce 的 in-、neutral 的 ne-、pierce 的 pier-；season 的 -on、debt 的 -t（来源进括号、组合列补词性变化），zodiac 的 -di-（夹在中间）。
    - 读的时候（cols.legacy、视频）词根标签的连字符去掉，和以前一样；视频另外看「词根」列：写在词根列的都画成词根卡片（unique 的 un、real 的 re、trial 的 tri 以前被当成前缀，现在对了）。

## 2026-11 单词列轮定下的

40. **词根后面加 L 列「单词部分」**（用户定下：“有些单词是基础词，找不到词根词缀的，但仍然会放到词根里面”“如果是单体词，没有词根词缀的，再增加一列：单词”“合成词的，也是把里面有关的解释都放在单词列”“前后缀加单词的，前后缀就放在词缀列，单词就放在单词列”）：
    - 列名叫「单词部分」：E 列已经叫“单词”，同名两列视频技能和单词对照台会认错（它们按列名认列）。放在词根和后缀之间：J 前缀、K 词根、L 单词部分、M 后缀，后面往右挪一列，共 22 列（第 41 条）。
    - 单词部分放**能单独用的英语单词**，不加连字符：基础词本身（make 的整格解释）、变体词本身（made）、母词（maker、rematch、matching 的 make、match；thoughtlessly 的 thoughtless）、合成词里的各个词（make-up 的 make、up）、专有名词（Hamburg、Shanghai）、缩写字母代表的词（VIP 的 V、I、P）；复数、过去式、-ing 这些形式（hands、days、selves、behaved、did）也算。⑤ 基础词、④ 不好拆分的整格放这里。
    - 词根列只留**不能单独用的**：拉丁、希腊词根和构词成分（-spect、bio-），外语里的成分（tsunami 的 tsu-、-nami，karate 的 kara-、-te，deluxe 的 de-、-luxe，algebra 的 al-），古英语里今天不单用的成分（yesterday 的 yester-、together 的 -gether），截下来的半截词（smog 的 sm-、-og，Paralympic 的 para-），和英语词同形、意思不相干的（mission 的 miss-“送”、synthesis 的 -the-“放”、nightmare 的 -mare“夜魔”），连接成分、双写的字母（-i-、-s-、-b-）。
    - 讲整个词来历、拼写、读音的说明跟着主体走：这一行有词根（连接成分不算）就放词根列，没有就放单词部分（spokesman“造得不规则”、email“去掉连字符的写法”在单词部分；diplomat、investigate 的说明在词根列）。只讲前缀的说明放前缀列（mistrust 的“mis- 和 dis- 不一样”）。
    - 拿不准的照上一轮的判断：说明里写了“见 自己”、指向同形英语单词的拉丁来源词（depart 的 part、design 的 sign、artifact 的 art、centipede 的 cent）算单词；明说等于某个英语词的缩写形式（also、already 的 al = all，bonfire 的 bon = bone，lady 的 la = loaf，unless 的 un = on）算单词。
    - 顺带改正上一轮加连字符的错判（「整表核对记录」第 105 条）：37 处英语单词形式误加了连字符（hands-on 的 hands-、schooldays 的 -days、grassroots 的 -roots、craftsman 的 crafts-），253 处外语成分、拉丁词根没加（tsu、de、dino、Tues、vi、un“一”、nat、sta、miss、the……）。原因：自动判断只看“表里有没有这个词”（hands 不在表里），合成词的部分一律当单词，“见 X”又只比开头几个字母（“见 via”把 vi 当成单词）。5 处前缀写在了词根列（monopoly、monarch 的 mono-，enthusiast 的 en-，illusion 的 il-），挪到前缀列。
    - 新写内容时：set_parts 先照每一行原来在哪一列放；新的一行，表里有这个词（或它的复数、过去式）、说明不是“= 拉丁语…”“由词根…”开头的算单词，别的算词根（cols.is_word_part）。写完看一眼，不对就手挪。
41. **「拆分结果」22 列**：A 批次、B 序号、C 组号、D 小类号、E 单词、F 含义、G 例句、H 类型、I 拆分、J 前缀、K 词根、L 单词部分、M 后缀、N 组合 → 现在的含义、O 新·背景、P 音变 / 字母变化、Q 核对结果、R 核对依据、S 来源链接、T 原表备注、U 本次调整、V 词根变体处理。冻结 G2，筛选 A1:V。「说明」第二节写成“J 前缀、K 词根、L 单词部分、M 后缀”一行，统计公式范围跟着挪（背景 $O、核对结果 $Q、本次调整 $U、词根变体 $V）。脚本的列号都在 `scripts/cols.py`；合回一格时词根和单词部分的行按拆分里的先后穿插（cols._order_core），和分列以前的先后一样（dubbing 读成 dub、b）。

## 2026-11 源头词根轮定下的

42. **源头词根**（用户定下：“people 和 popular 其实都是有词根的，都来自拉丁文词根 popul-……应该要把它们的源头词根说出来；音变里面其实已经说的很清楚了”“popular 演变的单词，就按原来的就可以了，在 popular 的基础上加后缀”“按照单个单词来处理”）：
    - **派生词**：这个词直接来自拉丁语（希腊语），用的是拉丁原形，拆分里的英语词却是同一个词根经法语磨短、变了样的（早先“母词替换”那一轮换上去的），拆分写源头词根：popular = popul + ar（不写 people + ar）。词根列写“popul-：人民、民众（拉丁语 populus“一国的全体人民”）；people 是它经法语变来的样子（见 people）”，单词部分写“-”，组合列公式跟着换（popul（人民）+ ar（…的）），音变列“people → popul-：…”这类旧说明去掉（只剩它一行的，换成整词从哪个拉丁词来）。共 24 个：popular、populate、populous、majesty（maj + es + ty，同 major = maj + or）、principal、principle、regular、regulate、ordinary、coordinate、determine、terminal、imagine、imaginal、material、floral、criminal、hospital、humility、prejudice、poverty、imperial（im + peri + al）、suspicion（su + spic + ion）、debit（de + b + it，同 debt）。
    - **在完整单词上加缀的照旧写单词**：popularity = popular + ity、population = populate + ion、imagination = imagine + ation——一个词一个词判断。
    - **外来基础词**：同组在用源头词根、自己经法语又变了样的，⑤ 基础词 → ② 变体关联，拆分写 `people ← popul`；词根列补源头词根“popul-：意思（拉丁原词）；popular、populate、populous 保留了这个写法”；单词部分只留这个词自己的来历那一行（别的讲来历的说明随词根挪到词根列）；组合列第一行写“people 由源头词根 popul 变来（拉丁语 populus → 古法语 pople / peuple → people），意思从“…”发展：”。共 37 个：people、rule、order、term、image、matter、flower、crime、poor（← pauper）、voice、city、peace、sound、clear、save、cross、waste、grace、mount、duke、letter、prove、brief、wine、reason、paint、chief、price、faith、nurse、vain、poison、air、lion、round、place、course。视频 3.4 起念成“people，是从拉丁语词根 popul 变来的；popul 的意思是：人民、民众”，画面上 popul 一个个字母变成 people。
    - **不改的**（「整表核对记录」“源头词根（没改的）”，`scripts/root_check.py` 的 KEEP）：只差一个字母、一眼看得出的（community / common、exemplary / example、scholar / school、technician / technique、reveal / veil、reconcile / council）；-cle / -cul- 固定互换的（circular、particular、spectacular，同 -ble / -bil-）；英语词本身就是拉丁（希腊）原形的（parcel / part、inert / art、degree / grade、plural / plus、prince / prime、gradual / grade、Atlantic / Atlas）；在法语里就这样组成的（achieve、dessert、align、restaurant）；英语本族词的元音变化（strength、only、once、twelve、further、husband）；动词和它的名词（decide / decision、destroy / destruction）；已经用 ≈ 挂到同组词上的 ②（host ≈ hospital、mayor ≈ major）；外来基础词里，同组的词根和它不是同一个写法的来源（turn / tour-、power / poss-、heir / herit-、join / junct-……，`root_check.py --base` 列的 62 个，人工看过）。
    - 以后新写、改写：`python3 scripts/root_check.py <xlsx>` 应为 0；新出现的逐个按上面判断，决定不改的补进 KEEP 并写理由。
43. 顺带改正：major、minor 的 -or 是比较级“更…的”，词性变化写“变成形容词”（同 junior、superior），不是“动词 → 名词（人或东西）”；minor 的来源括号写“来自拉丁语比较级词尾 -ior / -or”。

## 2026-11 字母变化轮定下的

44. **字母变化写成一步步的链**（用户定下：“rule ← regul 这种变化，是怎样一步步由 regul 变成 rule 的”“像这种单词和词根之间变化比较大的要解释清楚是怎样一步步变化来的，要不然学生记的时候又困难”“这种变化比较大的肯定是经过了好几个语言，最后形成的，之间的变化过程要讲清楚，写在 音变 / 字母变化 这一列里面”；简单的 y → i、去掉 e 不算）：
    - **范围**：这一轮做了挂到源头词根上的 37 个外来基础词（第 42 条的 people ← popul、rule ← regul……）。别的字母差得多的（② 变体关联里 ≈ 挂到同源词上的、拆分里带 (=…) 变化大的）用户看过效果再做，`zimu_check.py --todo` 列出候选；截短、缩写（phone ← telephone、ATM）、as(=ad) 这类前缀同化不用写。
    - **第一行是链**：`【字母变化】regula（拉丁语）→ reule（古法语）→ rule（英语）`。括号里只写语言；没留下文字、由后来的语言推出来的形式前面加 *（*retundus、*capum、*montare），步骤里写“带 * 的是没留下文字、推出来的形式”；英语原样借来、字母没再变的，最后一个写 `grace（古法语、英语）`。法语的词多从拉丁语的变格形式来，链从变格形式写起（vocem、pacem、civitatem、rationem），① 里写“法语的词是从它的变格形式 X 变来的”。链上只写字母串（不带长音符号），视频照它一个字母一个字母地变。
    - **下面每一步一行**：① 讲源头那个形式（音节 po-pu-lus、意思），写出词根 X-（“词根 popul- 原样留在 popular、populate、populous 里”）；以后一个箭头一行，第 k 行写到链上第 k 个形式（“…：populus → pople”），讲清哪个字母掉了、哪个变了、读音怎么变，尽量举同类的例子（拉丁 mare → 法语 mer、Londinium → Londres、salmo → saumon）；进入英语那一步写年代和今天的读音，英语长元音变了读法的写“后来英语的长元音整体变了读法（元音大推移）”。最后一个写成“（古法语、英语）”的可以再多一行讲英语里的读音。
    - **原有的说明**：原来那一句讲变化的话由步骤取代；【同源】【易混】【趣】【联想】【对照】【有争议】【同形异义】【合成】照原文留在后面（和步骤重复的去掉，如 term 的“determine、terminal 的 termin- 就是 terminus”）；原来那句里的对照例子单列成【对照】（waste、reason、chief）。
    - **不确定的照来源写**：中间一步词典只给了结果的，只写结果或写“一般认为…”；来源说法不一的照第 21 条。中间形式、年代都对照 etymonline 整站数据（工作三）。
    - 以前有 5 行（drought、tight、fierce、endorse、falcon）用【字母变化】开头写一句说明（第一行带“：”），不是链，照旧；以后改写这些词时再改成链。
    - 体检：`python3 scripts/zimu_check.py <xlsx>`（一、该写链没写的；二、链的写法、步骤数不对的；都应为 0）。
45. 顺带改正：flower 的【同源】原来写“14 世纪末起‘花’义才固定写作 flower”；etymonline flour 条目说的是“面粉”原来也写 flower，约 1830 年起才固定写成 flour（flour 那一行本来就写对了）。

## 2026-11 字母变化同源词轮定下的

46. **≈ 的词也写字母变化链**（用户看了第一轮 37 个以后说“可以，继续做”，接着做 zimu_check.py --todo 列出的 116 个 ≈ 词）：
   - 拆分写成 X ≈ Y 的外来词，本词和源头字母差得多的，音变列第一行照第 44 条写链。链从**这个词自己的源头**写到它本身（rail：regula → *regla → reille → rail），不从 Y 写起：≈ 两边的词是兄弟（同一个源头走了两条路，一个直接借拉丁语、一个经法语），不是一个从另一个变来的；① 讲源头形式以后，接着讲清和 Y 的关系（“rule 是同一个 regula 走另一条路变来的，rail 和 rule 是兄弟”）。
   - 原有的【同源】【易混】【同形异义】【联想】等照原文留在后面；原来那句讲变化的话由步骤取代，里面步骤没讲到的补成标签段落：【短形式】（apprentice 以前常说 prentice）、【同类】（scent 的 c 和 scythe 一样是后加的）、【对照】（alarm ← all'arme、hôtel → hotel）、【分工】（patron 管人、pattern 管样子）。
   - **不写链的三类**（名单在「整表核对记录」第 114 条、zimu_check.py 的 SKIP_APPROX，--todo 不再列出）：本族词（wet ≈ water、match ≈ make，一直在英语里，没有经过别的语言）；来源不确定（hockey、buoy、haunt，词典自己说“也许”）；变化很小（physique、costume，只差拼写、词尾；gas 是照 chaos 造的词）。
   - 46 个词：apprentice、wait、spice、premier、rail、dress、alert、reign、essay、allow、tissue、doubt、able、mould、fuel、issue、feast、scent、chase、cable、river、kitchen、danger、pattern、fault、trouble、host、hostel、medley、campaign、etiquette、counsel、ray、solder、rhyme、league、lantern、pillar、eager、sleigh、Mandarin、grill、kitten、frantic、chime、menu。
   - P 列列宽 50 → 55（dress、trouble 五步的链按 50 宽要超过 Excel 行高上限 409 磅）。fixlib 的 `_fit` 以前取列宽时没管 openpyxl 一段一段的列宽（K–M 共用一条），算出的行高偏高，这一轮改正，行高也封顶 409。

## 2026-11 动词变化形式轮定下的

47. **动词的过去式、过去分词要讲清作用，音变列要讲清怎么变来的**（用户：“动词的过去式、过去分词、现在分词也是单词，有不同的含义，但是组合 → 现在的含义这一列没有对这些解释清楚……没有对过去分词、现在分词的功能以及对这个单词的含义的影响讲出来”；“对于不规则的动词变化形态，要在音变 / 字母变化对这种变化要有解释，就像 made 一样……maked 最后怎么就变成 made 了，这关键的一步没有解释”）：
   - **组合列**：第一行 `write（写）→ written =“被写下来的”`（拆分写成 take + n 这类的，第一行照旧）；下面先讲这个形式的作用，再讲意思怎么来：
     ① 过去式：说这件事在过去发生、已经结束了 → 写了
     ② 过去分词：有“完成”“被动”两层意思——跟在 have 后面是“已经…了”，跟在 be 后面是“被…” → 已经写了；被写
     （不及物动词 go、fall、rise、sit、sleep……的过去分词只有“已经…了”，没有“被…”）
     → 过去分词放在名词前、be 后面当形容词，就是“被…了的”（不及物的是“已经…了的”状态） → 书面的
     → 意思再往下变的步骤照旧。
     结果要短（视频把结果写成大字）：英文整句例子挪到【语法】那一行。【语法】写三种形式 `write – wrote – written` 和一句用法（wrote 只当过去式，不能跟在 have、be 后面）。
   - **过去分词当形容词是语法，不算用词规律**（usage_rules.md 早就这样说）：built、done、spent、sunk 标的“名词放在别的名词前面，也能当形容词用”，given、shot 标的“表示东西、性质的词，也能直接当动词用”，bent、worn 标的规律，这一轮去掉了；「用词规律一览」按全表重算。
   - **音变列**：讲清这个形式怎么变成今天的样子。有字母变化的写成【字母变化】链（写法同第 44 条），从古英语（或北欧语、中古英语）的形式写到今天：`macode（古英语）→ makede（中古英语）→ made（中古英语、英语）`；① 讲古英语的三种形式（强变化动词靠换元音：wrītan – wrāt – writen；规则动词加 -de / -te），关键的一步要讲出来（made：k 掉了，它后面弱读的 e 也一起并掉，ma-ke-de 缩成 ma-de，末尾的 e 是过去式词尾 -de 剩下的）。古英语字母 þ、æ 进不了链，写成 th、ae 或从中古英语形式写起。没有字母变化的（sang、began 从古英语到今天没变）、带前缀的（mistook、understood 照 take、stand 变）、近代才出现的（stuck、dug、snuck）写成一段说明。原有的【同形异义】【合成】【异干】等标签段落照原文留在后面。
   - 这一轮做了 154 个不规则形式（102 个写链）；-ing、-ed 成对的规则形式（surprised / surprising……）还没做。

## 2026-11 合成规律轮定下的

48. **合成词讲合成规律、写法**（用户：“像这些有 - 符号的，没有解释这些符号的作用，为什么有的词会加 -；有的却不加”“还有像 paper-cutting，为什么不是 cutting-paper”“就是英语单词合成一个单词时，顺序的排列和单词的含义之间是什么关系，有哪些规则；这些要在组合 → 现在的含义这一列里面讲出来，方便学生理解原理，要不然只能死记”“你再看看还有没有其他的一些特殊规则”）：
    - **范围**：③ 合成词全部（1408 个），加上别的类型里带连字符的词（non-verbal、co-writer、mid-January、sci-fi、good-bye 这类 59 个，只写写法）。
    - **两种行**，紧跟在【构词逻辑】第一行下面（有后缀等式的接在等式后面），先合成规律、后写法，前面一个全角空格，和“　用词规律：”一个样子：
      `　合成规律：规律那句话（本词：短语 中文 → 本词；同 例词）`——一到三行：第一行讲两个词的先后和关系，后面可以接特殊规律（man → men、中间的 s、复数加在主体上、连写后意思固定）；
      `　写法：规律那句话（本词的例子、别的写法、历史）`——一行。
    - **规律那句话**照 `scripts/hecheng_catalog.py`（=「合成规律一览」）一字不改：视频技能 3.7 照这句话念、上小黑板；体检按它认是哪一条。规律那句话里不写“…”、箭头、括号（视频照念）；括号里不写“+ -”（parse_I 会当成后缀等式读走，写“再加 -ed”）。
    - **34 条合成规律**的主线：最后一个词是主体（classroom）；宾语提前（cut paper → paper-cutting，倒过来的 cutting-paper 是“剪着用的纸”）；用什么、在哪儿、由谁提前（handwriting、skydiving）；名词 + 过去分词（made by hand → handmade）；副词提前（work hard → hard-working）；名词 + 形容词（free of sugar → sugar-free）；短语整个当一个词（part-time、up-to-date）；动词短语变名词（make up → make-up，先后不变）；小词在前（come out → outcome；setup ↔ upset）；介词短语连成词（upstairs）；像一句命令（scarecrow、pastime ← 法语 passe-temps）；有…的（kind-hearted）；数词 + 名词用单数（a ten-dollar bill / ten dollars）；并列（black-and-white；方位 northeast 和汉语“东北”先后相反）；近义叠用、加类名（pathway、reindeer）；有这个特点的人或东西（humpback、high-five）；名词 + 动词 = 动词（double-check；troubleshoot 很可能倒推自 troubleshooter）；主语 + 动词（sunrise）；数字（forty-five；分数 one-third 和汉语先后相反；十几 fourteen）；小词合成（anyone、whatever、itself、without）；老合成词磨损（window = wind + eye）；外语里合成的照原语言的先后（republic = res publica 形容词在后、kowtow“磕头”动词在前、Vietnam 越南语说明词在后）；拼缀词（smog）；特殊规律（man → men、craftsman 的 s 是古英语“…的”、passers-by、greenhouse ≠ a green house、6th-grader 词尾加在短语上、self- 在前）。
    - **18 条写法**：用熟了连写（分开写 → 加连字符 → 连写）；还没用熟的加连字符；几个词当一个形容词（放在名词前尤其要加；well-known、up-to-date 放在 be 后面常分开写）；动词短语变的名词（连写或加连字符，动词永远分开写，名词重音在前）；数字；字母、缩写、数字开头；self-；like、free、friendly、based 这类；并列；短语连成词；连写分开写意思不同（everyday / every day、maybe / may be）；掉字母、重字母不删（already、welfare / roommate、earring）；前缀的连字符（大写字母前一定加，英式比美式爱加）；重复的词；撇号；名词常分开写（science fiction / a science-fiction novel）；专有名词；-ly 副词不加（a highly skilled worker）。
49. **讲写法的话只放写法那一行**：原来散在组合列【语法】【辨析】【提醒】、步骤末尾的括号、“（…见【辨析】）”指路行和音变列里讲连写、连字符、分开写的话（466 行 544 处），并进写法那一行（例子、别的写法、年代照原话带过去），原处删掉；一行里还有别的内容的，只删讲写法的那半句（145 行逐条定，名单在 scripts/archive/hecheng/mixfix.py、pass2.py）。不动的：【演变】里讲一个词什么时候连写的历史（anyway 1830s 起常合写）、republic / legislator 讲拉丁短语合写的来历、co-writer 里“合写”是“合着写”的意思、run-down ≠ rundown 这类讲意思的辨析（hecheng_check.py 的 write_scattered 基线 35）。
50. 这一轮的几个判断：giant-king、giant-prince 原【语法】说“前一个名词修饰后一个”，按主体在后讲（巨人一样的国王），不当并列；never-ending、much-anticipated、newfound、highly skilled 这类副词本来就在前面的，按“短语整个当一个词、先后不变”讲，不说“副词挪到前面”；family-sized 的 family 不是 -ly 副词；charcoal、ketchup、gallop、standard 照词典写“说法不一 / 很可能”；数词 + 名词那一类的单复数（不说 a ten-dollars bill）写在合成规律那一行，原来【语法】里的同一句删掉。

## 2026-11 英美写法轮定下的

51. **含义列标英式、美式写法**（用户问 makeover 为什么不加连字符、是不是美式写法：“如果是这样，我希望在含义列里面要标注好是哪个写法，并且要再补充英式写法。再检查一下总表，看看其他的是不是也有这样的情况”）：
    - makeover 查过牛津（英）、韦氏（美）都连写，英美一样，不标；组合列写法那一行写明“英美词典都连写成 makeover，不像 make-up / makeup 分英美”。
    - 英式、美式写法不同的词，含义第一行末尾写一处：字母不同写“（英式拼写，美式写作 X）/（美式拼写，英式写作 X）”（colour、metre、defence、traveller、ageing……）；连字符、连写、分开写不同写“（英式写法，美式多连写成 X）/（美式写法，英式写作 X）”（make-up / makeup、take-off / takeoff、set-up / setup、check-up / checkup、second-hand / secondhand、non-verbal / nonverbal、co-author / coauthor、semi-final / semifinal、per cent / percent、any time / anytime……）；分工复杂的整句手写（license / licence：名词英美不同、动词都写 license；program / programme：“计算机程序”英美都写 program；practice / practise；meter / metre）。原来零散的标注（“（美式拼写）”“（= neighbour）”“（同 nonverbal）”“（英式拼写，同 X）”）去掉，统一成上面的说法；第 32 条的“（英式拼写，同 X）”改成“（英式拼写，美式写作 X）”。
    - 不标的：-ize（英式牛津拼法也用 -ize，所以 -ize 不算美式；-ise 的词标“英式拼写，美式写作 -ize”）；不同的词（filter / philtre、tire / tyre、ton / tonne）；旧写法（gramme、connexion、mediaeval）；两边都常用前一种的（glamour、cancellation、archaeology、aesthetic、dialogue、monologue、likeable、woolly）；按意思分工、含义里已讲的（disc / disk、draft / draught）。名单在 scripts/yingmei_data.py 的 SKIP。
    - 写法英美不同的合成词，组合列“写法”那一行也写明两边各怎么写（life-saving、second-hand、clean-up、check-up、takeoff、setup、runoff、easy-going、quarterfinal、pre-order……）。
    - 用英美拼写对照表 breame 把全表单词和合成词里的每一段对了一遍，再加上连字符、连写不同的词，共标 174 个；`yingmei_check.py` 各项为 0。

## 2026-11 e 结尾加后缀轮定下的

52. **e 结尾的词加后缀，拆分写全后缀**（用户：“像这种是不是应该为 make + er；然后删除一个重复的 e？”）：
    - 拆分写 `make + er`、`use + ed`、`take + en`、`late + est`、`see + en`、`been ← be + en`，不写 `make + r`、`use + d`、`take + n`、`late + st`、`piece + (e)d`——学生看到的应该是真有的后缀 -er、-ed，不是并不存在的“r”“d”；和表里多数早就这样写的词一致（organize + er、time + ing、use + able、populate + ion）。
    - 后缀列标签写 -er / -ed / -en / -est，说明写“make 已经以 e 结尾，和 -er 的 e 只写一个：make + er → maker”；组合列第一行公式写 `make（做）+ er（…的人）`，词性变化写（-er）。
    - 不改的：前面的词不是 e 结尾、本来就只加 n、st 的（show + n、know + n、grow + n、fir + st、amid + st）；arrest 的 st 是词根（拉丁语 stare“站”）。
    - 这一轮拆分改了 154 个，另有 29 个拆分早就写全、说明还写“只加 d / 只加 r”的一并改成同样的说法。audit [5] 从 290 降到 223，audit_split_labels 从 151 降到 149（都是因为“r”“d”对不上“-er”“-ed”那一行）。
    - 视频技能 3.8：拼的时候前一部分末尾的 e 去掉，字母照“mak | er”“tim | ing”对，共用的 e 算后缀的。

## 2026-11 拼写变化轮定下的

53. **加词缀时拼写变了的，在那个词缀那一行写明**（用户：“time + ing、use + able、populate + ion 这类……后缀列补一句‘time 的 e 遇到 -ing 去掉’；顺带看看还有没有其他的类似这样添加词缀会有一些特殊的现象的”）：
    - 写在这个后缀（前缀同化写在前缀）那一行末尾，“；”隔开，一句话 + 本词的例子：`time 末尾的 e 遇到元音开头的 -ing 就去掉：time + ing → timing`。已经讲了的（“去 e 加 -ing”“y 变 i”“在 c 前写成 ac-”）不重复。
    - 现象和说法（认的规则在 scripts/pinxie.py）：去 e（元音开头的后缀；-y 也算：tide + y → tidy）；留 e 读软音（change + able → changeable、courage + ous → courageous：c、g 后面直接跟 a、o 会读成 /k/、/g/）；去 e 的例外（true + ly → truly、wise + dom → wisdom、judge + ment → judgment）；y 变 i（happy + ness → happiness，y 前面是辅音时）；y 遇到 i 开头的后缀去掉（history + ic → historic）；ie 变 y（die + ing → dying）；双写（run + n + er → runner；重音在后的多音节词也双写：begin、forget、control；英式 l 都双写：traveller / 美式 traveler；program → programming 是习惯）；-le 变 -ly（possible → possibly）；-ble 变 -bil-（able → ability）；-le 变 -ul-（circle → circular）；-nt 变 -nce / -ncy（silent → silence）；-ate 变 -acy（private → privacy）；-ous 变 -osity；-fy 变 -fication（qualify → qualification）；-er 去 e（hunger → hungry、enter → entry）；-or / -er 加 -ess（actor → actress）；去掉末尾元音（piano → pianist、India → Indian）；拉丁语过去分词的拼法（decide → decision、attend → attention、permit → permission、reduce → reduction、receive → reception、describe → description、retain → retention、consume → consumption、solve → solution）；ai 变 a（explain → explanation）；元音变（long → length、deep → depth）；前缀同化（ad- 在 c 前写成 ac-、in- 在 b、m、p 前写成 im-、con- 在 l 前写成 col-、ex- 在 f 前写成 ef-、sub- 在 p 前写成 sup-……）。
    - 双写的字母单独写一部分（第 69 行）：swim + ming、fun + ny 这类 84 个改成 swim + m + ing、fun + n + y；没写出来的（forget + able、wed + ing、bag(g) + y）补上。
    - 不说明的：拉丁语、法语词干本身就不一样的（repeat → repetition、acquire → acquisition、Norway → Norwegian、maximum + ize）；合成词两个词之间的（wherever、twentieth）。
    - 这一轮补了 813 处（835 行）；体检 `scripts/pinxie_check.py`（missing、double_in_suffix、double_hidden 都应为 0）。

## 2026-11 过去分词轮定下的

54. **整个从拉丁语借来、接在过去分词词干上的名词、形容词，拆分写词干**（用户问 competition“为什么不是直接在 compete 后面加 ion，而是要加 ition”“是不是叫作中缀”；看了加一列「中缀」的方案后定下：“还是不用中缀了，这样不方便学生理解，我觉得还是从构词的角度来讲比较好”“对于有这种情况的单词，在拆分这一列要讲清楚，同时后面几列也要讲清楚”）：
    - **道理**（用户认可的说法）：competition 不是英语自己用 compete 加 -ion 造出来的，而是整个从拉丁语 competitio 借来的。拉丁语造“…这件事”的 -io 名词（还有 -ivus 形容词、-or 名词、-orius / -orium、-ura），不接在动词原形上，而是接在过去分词（“被…了的”形式）的词干后面：competere（一起争取）→ 过去分词 competitus → 词干 competit- → competitio。英语的动词来自原形（compete），名词来自过去分词，所以看起来多了 it、at（definition、information），或者字母变了（decide → decision、describe → description、solve → solution、permit → permission）。严格说 it 不是中缀（中缀插在词根里面，如拉丁语 vincere 的 n），表里不用“中缀”这个说法，也不把 it、at 单独拆成一部分。
    - **拆分**：“过去分词词干(=母词) + 后缀”：competit(=compete) + ion、informat(=inform) + ion、decis(=decide) + ion、explanat(=explain) + ory、temperat(=temper) + ure、competit(=compete) + ive；有前缀的照旧拆前缀，括号里写本组词根：re + putat(=put) + ion、ex + pedit(=ped) + ion、im + perat(=par) + ive。词干照单词里的拼法写，部分拼起来正好是这个词。
    - **词根列**：词干一行，加连字符（competit-、-putat-）。英语母词的写“competit-：compete（竞争、比赛）的过去分词词干：拉丁语 competere“一起争取”→ 过去分词 competitus → 词干 competit-（见 compete）”，字母变了的补一句（d 在过去分词里变成 s；explain 经法语把 a 变成了 ai，名词照拉丁语写，还是 a；-ify 动词的 y 是经法语磨出来的，名词照拉丁语写成 -ific-）；本组词根的写“由词根 put 变来：拉丁语 reputare“反复思量”→ 过去分词 reputatus → 词干 reputat-，putat 就是 put 在这个词干里的样子；put：……（原来那一行）”。母词不再单写在单词部分。
    - **后缀列**：写真正的后缀 -ion / -ive / -or / -ory / -ure（标准写法），末尾写“接在动词的过去分词词干后面，不接在原形上：competit- 加 -ion → competition”；“为什么用 -ion 不用 -ment”这类照旧。原来“这里写成 -ition：it 是…”“compete 的 e 遇到 -ition 去掉”“y 变 ic”“d(e) 遇到 -ion 变成 s”这些话，由词根列那一行取代。
    - **组合列**：第一行公式跟着拆分写（competit（竞争、比赛）+ ion（这件事）=“一起争取”这件事；词性变化（-ion）），下面紧接一行“　构词：”，照用户认可的说法写：`　构词：competition 不是英语自己用 compete 加 -ion 造出来的，而是整个从拉丁语 competitio 借来的。拉丁语造“…这件事”的 -io 名词，不接在动词原形上，而是接在过去分词（“被…了的”形式）后面：competere（一起争取）→ 过去分词 competitus → 词干 competit- → competitio`。没有英语母词的写“X 不是英语自己造的，而是整个从拉丁语 Z 借来的。……”；英语后来照拉丁规矩、用拉丁词干自己造的（competitive、repetitive、exclamatory、refrigerator、gravitation、explosive）写“X 是英语后来照拉丁语的规矩造的：-ive 不接在动词原形上，而是接在过去分词（“被…了的”形式）后面：链 → 本词”；不规则的照实写（sensitive 照 positivus 多加了 it；sensation、constellation、literature 是名词加 -atus 造的形容词，写“和过去分词一样以 -atus 结尾”；miniature 从意大利语来）。链固定写成“原形（意思）→ 过去分词 X → 词干 Y- → 拉丁原词”，视频照它一步步念；行里不写“+ -”。
    - **英语（或法语）后来自己用现成的 -ation、-ative 造的词**（transportation、civilization、globalization、talkative、vaccination、aviation 等 27 个，名单在 guoqu_check.py 的 KEEP）：-ation 当一个整体后缀，拆分照旧（transport + ation），构词行写“transportation 是英语后来自己造的词（1530 年代）：-ation 是从 information 这类拉丁词里借来的现成后缀（at 本来是拉丁语过去分词的标志），英语把它当成一个整体，直接加在 transport 后面”，后缀列补“英语后来把整个 -ation 当成一个现成的后缀，自己造词也直接加它”。来历照 etymonline：“from Latin …ionem”是整个借来的，“noun of action from X (v.)”“from French …”是后来造的。
    - **不改的**：escalator（拼缀词）；hesitate、visit 的 -it-（表示“反复”，不是过去分词）；-ate 动词加 -ion（create + ion：create 本身就是过去分词 creatus 变来的）；词根本身就写成过去分词词干的（posit + ion、edit + ion、curat + or）；reduce + tion、produce + tion 这类 -tion 词（t 也是过去分词带来的，这一轮没改，以后照本条写成 reduct(=reduce) + ion）。
    - 这一轮拆分改了 145 行（-ation 71、-ition 8、-ative 6、-atory 4、-itive 3、-ator 2、-ature 2、-itor 1，原来单独拆出 it、at 的 6 行，动词 + ion 字母变了样的 42 行），英语自己造的 27 行加了构词行；体检 `scripts/guoqu_check.py`（各项 0）。

## 2026-11 过去分词轮（二）定下的

55. **写成过去分词词干的词，音变列写字母变化链**（用户看了 description 这一行：“describe 变成了 description 这些情况，还要在音变这一列写好是怎么变化的，为什么这样变，具体怎么变化的”；同时把上一轮说的下一步做掉：reduce + tion、produce + tion 这类改成 reduct(=reduce) + ion）：
    - **范围**：拆分写成过去分词词干的词（第 54 条）全部写，150 个：上一轮的 145 个，加这一轮改的 reduction、introduction、production、nutrition（nutrit(=nutri) + ion）、mixture（mixt(=mix) + ure；英语的 mix 是 15 世纪末从 mixt 倒推出来的）。
    - **链**：`【字母变化】describere（拉丁语）→ descriptus（拉丁语）→ descriptio（拉丁语）→ description（英语）`：拉丁语原形 → 过去分词 → 拉丁语名词（形容词）→ 英语；拉丁语名词照 etymonline 写明晚期拉丁语、中世纪拉丁语；-or 词英语原样借来的，最后一个写 `competitor（拉丁语、英语）`；英语照拉丁规矩自己造的（competitive、repetitive、exclamatory、refrigerator、gravitation、explosive）链是“原形 → 过去分词 → 本词”。写法和第 44 条一样，zimu_check.py 照样查。
    - **步骤**：① 拉丁语原形和意思，英语的动词就来自它（经古法语 / 经法语 / 直接从拉丁语进入英语；动词经法语变了样的补一句：explain 经法语把 a 变成了 ai）；② 过去分词怎么构成、为什么这样变：-are 动词词干末尾本来就是 a，加上 -tus 成了 -atus；-ire 动词成了 -itus；competere、repetere、addere 加连接元音 i；b 碰上 t 变成 p（b 要振动声带，t 不振动，连着念 b 被 t 带得不振动了）；c 和 t 直接连成 ct；d、t 碰上 t 念成 s（dt → ss → s）；tt 碰上 t 念成 ss；v 在 t 前变回元音 u；复合词里 capere 的 a、tenere 的 e、caedere / laedere 的 ae、claudere 的 au 弱化；ponere → positus、quaerere → quaesitus、struere → structus、miscere → mixtus 这些不规则的单讲；③ 去掉 -us，留下词干，加上 -io（“…这件事”）/ -ivus / -or / -orius（laboratory 是 -orium）/ -ura；④ 什么时候、经什么语言进入英语，-ionem → -ion、-ivus → -if → -ive、-orius → -ory、-ura → -ure；英语拼法和拉丁语不同的补一句（拉丁语的 ae 到英语简化成 e）。
    - **原来音变列的话**：没标签的那一句多是讲同一件变化的（“d 变 s：decide → decision”“scribe → script：b 在 t 前清化成 p”），由步骤取代（63 行，原话记在 review2.txt，见 scripts/archive/guoqu/round2.py）；还有别的内容的加标签留下（【对照】publish、【拼写】informacion、【读音】、【同类】、【短形式】rep，16 行）；原来有标签的【同源】【易混】等照原文放在后面。
    - 不规则的手写（sensitive、sensation、constellation、literature、miniature）：sensation、constellation、literature 链从名词写起（sensus → sensatus → sensatio → sensation），写“和过去分词一样以 -atus 结尾”。
    - 视频暂不读这条链（parts 型的词只读组合列的“构词”行，做成“构词”卡）。体检：zimu_check.py 二（链和步骤写法）、guoqu_check.py 的 no_chain 都应为 0。


## 2026-11 不好拆分记忆轮定下的

56. **④ 不好拆分的词写“约等于的词”和【记忆】**（用户：“这些不能拆分的单词，有时候记起来比较麻烦，能来一些约等于的单词吗”“学生都是那种不擅长学习的……希望能科学的、有逻辑的让这些学生也能记住”；看了方案后定下：“关联的单词要简单一些……lump ∽ bump / hump 这几个单词都比较难，要再找一些更简单的，适合基础差的学生的单词”）：
    - **范围**：118 个 ④（拆分原来写【待处理】），全部处理，【待处理】为 0。
    - **三种写法**，因为表里 ≈ 的意思是“同一个来源”，视频会念“X 和 Y，是同一个来源”，来源不明的词不能随便写 ≈：
      - `A ≈ B（一说 / 也许 / 可能）`：词典说可能同源，类型改 ② 变体关联（照 hockey ≈ hook）。8 个：tag ≈ tail、sincere ≈ simple、disciple ≈ doctor、bully ≈ brother、paddle ≈ pan、kidney ≈ egg、bet ≈ better、jaw ≈ chew。
      - `A ← B`：从它变来，类型改 ②。1 个：golf ← colf（中古荷兰语“球棍”）。
      - `A ∽ B`（U+223D，借初中几何的“相似”）：记忆联想，长得像（押韵、只差一两个字母、开头一样）、意思连得上，**不表示同源**，类型留 ④。91 个：goal ∽ go、tiny ∽ mini / little、noise ∽ voice、pull ∽ push、hike ∽ bike、bother ∽ brother、lump ∽ jump、slash ∽ flash、sprain ∽ pain、shark ∽ sharp、roam ∽ Rome、scam ∽ scan……
      - 找不到合适简单词的写“—”，只写【记忆】。18 个：job、clever、lavender、boost、hub、gadget、jazz、pudding、bias、quirk、junk、gravy、hassle、prawn、slum、stunt、tub、bungee。
    - **∽ 后面的词要简单**：只用小学、初一的常见词（go、push、top、bike、boy、brother、dog、room、sun、hen、big、jump、egg……），不用 bump、hump、rubble、smash 这类。科学依据写进【记忆】：语音象征（fl- 飘、bl- 猛吹、st- 稳、sl- 细、-ump 沉甸甸、-ash 唰的一下、i 音表示小）和用学生认识的英语词当钩子（不用中文谐音，读音不带歪）；汉语音译词直接用（爵士 jazz、布丁 pudding、蹦极 bungee、高尔夫 golf、马克杯 mug）。
    - **【记忆】行**：音变 / 字母变化列第一行，`【记忆】goal ∽ go（走、去）：goal 读起来就是 go 后面加个 l。……只帮助记忆，不表示同源`；≈ 的写词典的把握（只是一说 / 也许）。原来的【联想】【有争议】【同形异义】照留在后面。
    - **组合列**：改成 ≈ / ← 的 9 个，第一行写明关联（`【构词逻辑】tag 来源不明；一说和 tail（尾巴）同源，意思从…发展：`）；∽ 和 “—” 的不动。
    - **视频**：∽ 现在被视频技能读成 single（像基础词那样讲“来历”），不会说成“同一个来源”；要专门做一幕“和谁长得像”，要改 wordfilm.js 的 parseSplit（认 ∽）和 draft_plan.js 的配音（念“X 和 Y 长得像，……”），配音用【记忆】那一行。
    - 逐词数据和出表脚本：scripts/archive/jiyi/（memo_data.py 118 个词的拆分、类型、【记忆】；build.py 改表，build2.py、build3.py 压缩、出传输包）。

57. **用户这一版总表只剩 16 列、1 张表**（2026-11 上传的“0总表-词源拆分”）：「拆分结果」A 批次、B 序号、C 组号、D 小类号、E 单词、F 含义、G 类型、H 拆分、I 前缀、J 词根、K 单词部分、L 后缀、M 组合 → 现在的含义、N 新·背景、O 音变 / 字母变化、P 词根变体处理；例句、核对结果、核对依据、来源链接、原表备注、本次调整四列多和另外 4 张工作表用户自己删了（为了文件小）。scripts/ 里的体检脚本按 22 列写：用之前先在内存里补回空列（或改 cols.py 的列号），不要给用户把列加回去。没有「说明」「整表核对记录」了，改动只在回复里说明。

58. **出表要小**（用户：“每次我发给你很久才成功，压缩的要很小，最好 1~3M”）：
    - 原因：WPS 存盘把一格文字按字体（微软雅黑 / Noto Sans CJK SC）切成 23 万多段富文本，sharedStrings.xml 解开 36.8 MB；openpyxl 存盘又写成内联字符串，汉字写成 &#…; 数字引用（解开 37.6 MB）。
    - 做法（build2.py、build3.py）：openpyxl 读写（富文本自动去掉，内容一字不变）→ 汉字还原成 UTF-8 → 内联字符串改成共享字符串、按列再按行排（同一列的内容挨在一起好压）→ zopfli 压缩。7.67 MB → 4.87 MB；LibreOffice 能打开，和原表逐格比只有改的那几列不同。
    - Excel 格式只能用 deflate 压缩，表里纯文字就有 13 MB（组合列占一半），不删内容 xlsx 到不了 3 MB 以下；另出“传输包”zip：里面的 xlsx 不压缩，外层用 LZMA（方法号 14，字典 64 MB、pb=0），3.33 MB，用 7-Zip、Bandizip、WinRAR、360 压缩能解开（Windows 自带的解压不认 LZMA）；用户上传传输包时直接用 zipfile 解开再读。PPMd 试过只小到 3.19 MB，不值得换 7z。

## 2026-11 部分记忆轮定下的

59. **拆开以后还不好懂的部分，那一行末尾写“记：”**（用户看了 thermostat = thermo + stat 的视频：“这两个部分都不太好理解，我觉得可以用约等于来进行记忆理解，比如 stat 约等于 stand 这样来记；这需要对总表进行分析，总表的拆分部分，看看哪些就算是拆分开了，也不太好懂的，这个时候就把这些进行这样的再处理”）：
    - **哪些算不好懂**：词根列（K）里不能单独用的拉丁、希腊词根（stat、ject、duct、spect……），加上前缀、后缀列里几个当词根用的构词成分（-stat、-meter、-graph、-phone；tri-、bi-、bio-、geo-、thermo-、uni-、cent(i)-、dec(a)-、oct(o)-）。能单独用的英语单词（单词部分列）、常用前后缀（re-、un-、-er、-ly、-tion……）、过去分词词干（competit(=compete)，括号里已经有英语词）不加。
    - **写法**：那一行末尾接“；记：X ≈ Y（中文）：道理”。X 是这一部分（不带连字符），Y 只用小学、初一的简单词，道理一两句、不带括号：`-stat：…（希腊语 statos…）；记：stat ≈ stand（站）：stand 是站，stat 也是站、站住；它们本是一家`。符号和第 56 条一样：≈ 真的同源（同一个拉丁、希腊词根，或词典说同出一个印欧语词根；拿不准的道理里写“一说 / 词典说”，如 thermo ≈ warm）；∽ 只是长得像、意思连得上，帮助记忆（plore ∽ roar、min ∽ mini、tact ∽ touch、flu ∽ flow、di ∽ day）；← 从它变来。
    - **先看意思再配词**：同一个写法意思不同的分开配（port“搬运”≈ transport，portion 的 port“份”≈ part；capt“拿”≈ catch，captain 的 capt“头”≈ head；ply“填满”≈ full（supply、comply），ply“折”不配（apply、reply）；vey“看”≈ video（survey），vey“路”≈ way（convey））；词典有两说的、讲“不是…”的行不配（religion、logistics、legal、college、dialect、recent 试跑时都排除了）；关联词就是本词或本词另一种拼法的不写（video、dialog）。“由词根 X 变来”的变体跟着 X 配（sist、stitute ← sta ≈ stand）。
    - **范围**：这一轮 113 条规则、468 行（词根 449、前缀 16、后缀 3），覆盖出现在两个词以上的词根和这一批视频的词；还有约 1530 行词根没有记法（多是只出现一次的词根、连接成分），以后照同样的办法接着补（`scripts/part_memo.py --dry` 列出最常见的）。
    - **视频**：视频技能 5.1 起读这一段：卡片上加黄色“记”框，配音念“记法：stat，约等于 stand，站。……”（∽ 念“长得像”，← 念“来自”），小黑板多一行“记”。
    - 规则和脚本：`scripts/part_memo_data.py`（每条：写法、要对上的意思 need、要躲开的说法 avoid、符号、关联词、中文、道理）、`scripts/part_memo.py`（--dry 试跑、--write 写回、--check 体检）。写回直接改 xlsx 的共享字符串，别的格、格式、冻结、筛选都不动，再按第 58 条出 zopfli 压缩的 xlsx 和 LZMA 传输包。

## 2026-11 用词规律轮、同一个词根轮定下的

60. **用词规律要讲真正的规律**（用户看 camera 那一行“一个词用进某一行…就有了那一行的专门意思”：“这个解释就显得多余……讲解了感觉像没有讲解一下”“要讲的是真正的用词规律”）：
    - 规律得说得出“意思是怎么来的”，学生拿它能猜别的词；只是摆事实的话（“有了专门意思”“英美不一样”）不算规律。
    - “一个词用进某一行…”“同一个词，英国、美国的用法有时不一样”两条取消，原来的 861 行逐条换成真规律或删掉；新增“词的核心意思不变，换了对象、场合，中文要换个说法，英语还是这个词”
      和“作用、做法像什么，就借它的名字来叫”；“东西变了，旧名字还接着用”改成“东西换了代，干的还是那件事，旧名字就接着用”。目录、怎么选见 usage_rules.md 开头。
    - 找不到真规律的，规律那一行不写（用户同意：“直接删掉那一行可以”）。别的规律前提对不上的（leg“用来走路的肢体”标成“动作 → 用的东西”）也照这个办：复核后删 226 条（211 个词）、改贴 60 条——这一类是复核时主动删的，改动清单里单列一张“请过目”的表，用户说要留的照原样恢复。
    - camera：`　用词规律：东西换了代，干的还是那件事，旧名字就接着用（camera 暗室 → 照相机 → 摄像机；phone 电话 → 手机）`；
      produce：“动作 → 做出来的东西”（生出、结出 → 农产品）+“核心意思不变”（拿到前面来 → 出示、制作）；product：“越用越窄”（一切造出来的东西 → 产品）+“具体 → 抽象”（→ 结果）。
    - 不再按“（计算机）（英）”这类标签自动标规律（sense_rules.py 的 RULES 去掉了 domain、region；“表示动作的词…”只给动词和 -ion / -ment / -ing 这类动作名词）。

61. **同一个词根的几种写法，当同一个词根讲**（用户看 produce / product：“duc 和 duct 明显应该是同一个词根不同的形态，这里不应该当两个词根来讲，这样让词根变得更多了，更复杂了……
    不同的形态要当同一个词根来讲，只不过要做具体的说明，字母是怎么变化的，怎么演变的要说清楚”）：
    - **词根列**：不写“由词根 X 变来”，写 `-duct：词根 duc 的另一种写法（同一个词根）。字母变化：duc → duct，ducere 的“被领出来的”形式是 ductus：duc 后面加 t。意思：duc“领着走”（拉丁语 ducere）→ …`。
      三样都要有：是哪个词根、字母变化（从词根写起的一条链 + 怎么变的、为什么变）、意思。词根有特别说明的写进第一个括号：`（同一个词根；准确说是 magn 去掉 n 的 mag“大”）`。
    - **每一行自己讲清**：字母变化不能写“见 reduce”——别的词已经讲过，也要在本行再讲一遍（照本组样板词的说明写；这个词变法不一样的单独写：stage、contrast、arrest）。
    - **拆分列**：这一部分写成 `Y(=X)`：`pro + duce(=duc)`、`pro + duct(=duc)`、`vis(=vid) + it`、`con + st(=sta) + ant`（224 行）。整个词干是派生出来的（stationer）、拉丁语原样（levare）、词根本身带说明的（maj ← magn 去掉 n）不加。
    - 320 行改写（只剩 genuine：词典有两说，照旧）。体检 `scripts/tonggen_check.py`（各项 0）。视频技能 5.11 起读这种写法：卡片写“duct = 词根 duc”，演字母变化，配音念“词根是 duc……在这里写成 duct”。

62. **词根那一行不让学生去看更复杂的词**（用户：“这里说见 reduce，感觉没有意义，只是说 duc 这个词根，为什么要我见 reduce 呢？这样更复杂了，我希望说 duc 的时候，就专门说这个词，不要让学生去看更复杂的”）：
    - 词根列里指到**同组别的派生词**（类型 ① 词根词缀、③ 合成词）的“见 X”一律不写；括号里只有“见 X”的，换成这个词根的来源（`-scribe：写（拉丁语 scribere）`），查不到就不写括号。628 处。
    - 照旧可以写的：指到简单的基础词、变体词（⑤ / ②：见 people、见 two、见 via）；过去分词词干指到母词（见 compete，第 54 条）；跨组的同源词（noct 见 night）；另一种拼法指到主拼法（英式写 analyse（见 analyse））。
    - 第 7 条“见 X 只能指向……词根行同组的词”作废，以本条为准。前缀、后缀列和单词部分列没动。

63. **记法（第 59 条）补三条**（用户：“约等于的时候要用……更简单的，实在找不到就不约等于了，标注一下，等后续再想”；又：“像这样两个单词写法变化比较大的，要添加音变和字母变化的解释，
    就是为什么 fac 会变成 do，在发音和不同语种变化过程中，哪些字母发生了变化要解释清楚，要不然学生不太容易记住，fac 和 do 他们会认为缺少关联”）：
    - **关联词要比本词简单**：不能是同一个词根的另一个“前缀 + 词根”的词（duct ≈ introduce、port ≈ transport）。换成：duc ∽ duck（鸭妈妈走在前面，领着一队小鸭子走）、
      port ≈ port（港口）、fac ≈ do、dic ≈ teach、cli ∽ climb。**找不到就不写**：lect（捡、选）、mit / miss（送）、graph / gram（写、画），和 simple 的 ple、logic 的 log、prologue 的 logue，
      共 35 行去掉记法，在「词根变体处理」列标 `记法待补：mit（原来的 message 不比本词简单，已去掉）`（筛这一列的“记法待补”就能找到），名单在 part_memo_data.py 的 PENDING / EXCEPT_AT。
    - **≈ 两边写法差得多的写“音变”**：记法后面接 `。音变：f 对 d：印欧语的 dh，拉丁语在词头念成 f，英语念成 d（印欧语词根 *dhe-“放、做”…；同 foreign 的 for- 和 door）`；
      经法语变来的写一条链 `音变：regula（拉丁语）→ reule（古法语）→ rule（英语）：夹在两个元音中间的 g 越念越轻，脱落了`。270 行（≈ 共 407 行，写法相近的不加）。
      内容在 part_memo_data.py 的 SHIFT（72 条），同源关系对照过 etymonline；例子互相引用，让学生反复看到同几条对应（p 对 f、d 对 t、t 对 th、c 对 h、g 对 k、f 对 b、v 对 w）。
    - **词根和单独的词写法一样的可以写**（port ≈ port 港口），道理里讲清两个意思怎么连上：“港口是船把货运进运出的地方；拉丁语的港口 portus、城门 porta 和搬运 portare 是一家……”（用户：“这个可以有，但是要解释港口和词根 port- 的关联性”）。
    - **变体行的记法写词根本身**：product 那一行写 duc ∽ duck，不写 duct ≈ …（118 行）。体检 `python3 scripts/part_memo.py <表> --check`（五项都应为 0）。

64. **这一版总表怎么写回**（16 列、没有“本次调整”列）：`scripts/xlsx_write.py` 的 `write(src, dst, changes)`——直接改共享字符串，原来没有的格（空着的「词根变体处理」）会补一格，改过的行重估行高，
    再出 zopfli 压缩的 xlsx 和 LZMA 传输包。改动另出一份清单：`python3 scripts/changelist.py <改前.xlsx> <改后.xlsx> <清单.xlsx>`（用词规律一行一条规律行：这一步、原来、现在、处理；别的列一格一行：改前、改后、类别；主动删掉的单列一张“请过目”），用户要逐行看、要恢复都靠它。

## 2026-11 身份分工轮、辨析列轮定下的

起因：用户看 introduce、produce、product 三行和上一版视频，提了三件事，中途又加了一件：
① 视频要多一部分“同义词辨析”（produce、product 中文都叫“产品”，区别要讲出来）；② duce 和 duct 的关系没讲明——“为什么有的用 duce：produce；有的用 duct：product”；
③ “词根，前缀，后缀没有分开……词根 duce 里面还混得有 intro 的讲解，以及 intro + duce 的整合”；④ 我提出每个词根族补一段“分工”以后，用户：“这个很关键，就是不同写法分别是什么身份，怎么分工；这个一定要讲清楚”，
并要求“不同的前后缀，但意思相近的也要这样来进行辨析，比如 al、ous、ful、ive 这些都是形容词后缀……也要说明它们的身份是什么，有什么样的分工，为什么这个单词要用 ous，却不用其他的 ive、ful”；
组合列的【辨析】——“把辨析挪到新列，专门成立一个辨析列，这样解释的更明确”。

65. **词根列只讲词根本身**（各管各的）。词根那一行的先后：`标签：词根 X 的另一种写法（同一个词根）。字母变化：…。身份：…。分工：…。意思：X“意思”（来源）；记：…`（不是变体的：`标签：本组词根“意思”（来源）。身份：…。分工：…；记：…`）。拉丁语动词的词根族，“身份：”前面还有一段“动词变化：…；规律：…。”（第 71 条）。
    - 不写“词根的意思 → 前缀“…”… → 今天的意思”这条链：`→ intro“往里”领 → 领进来 → 引进；把人领到大家面前 → 介绍` 这种，前半是前缀的讲解，后半是组合，都不是词根的事（416 行切掉，其中 193 行带着前缀讲解）。切之前逐行查过：链里的步骤组合列都有同样的推导（更详细）；链里才有的拉丁语、希腊语原词挪到“合起来”一行（第 66 条）。
    - 前缀在这个词里取什么意思，写在前缀列那一行“；这里是“…””（这一轮补了 5 行：recipe、recipient 的 re-“回到自己这边”等）。
    - 留在词根行里的：词根本身意思的转变（cosm-：秩序 → 宇宙；“轻 → 举起”）、这个词根在这个词里取的意思（“；这里是“放”（印欧语词根 *dhe- 的本义）”）、过去分词词干怎么来的（explanare → explanatus → explanat-）、对来源拿不准的话（“和“星”有没有关系，词典说法不一”）。
    - **没动的**：讲整个词拼写、读音怎么变的行（“哪里变了：tonnel → tunnel”“怎么变成 strange 的：…”“整个词：A → B → C”“拼写怎么变的”，约 60 行）照分三列轮的规矩（讲整个词来历、拼写、读音的说明跟着主体走）留在词根列；用户只说了前缀的讲解和整合，这些没提。后缀列“在这个词里，X 加上 -ion，合起来就是 -ation”讲的是后缀怎么写，也留着。
    体检 `shenfen_check.py` 的 root_chain、heqi_in_parts（应为 0）；`shenfen.cut(行)` 能切出东西来就是还混着。

66. **“合起来”一行**（组合列）。前缀和词根（几个部分）在拉丁语、希腊语、法语、古英语里合成的那个原词和它的意思，写在组合列第一行下面：
    `　合起来：拉丁语 efficere“做出来、做成”→ efficiens“正在把事做成的”`（全角空格开头，和“　构词：”“　合成规律：”“　写法：”一样；位置在第一行、后缀等式和这几种行的后面，步骤的前面；一格只有一行，几句用“；”隔开）。132 行：
    原来单独写在词根列（“合起来是拉丁语 praesidere“坐在前面”→ 主持、监管”“拉丁语 perficere“做完、做到底”→ perfectus…”）的 78 行整行挪过来，链里才有的原词 45 行，前缀列、单词部分列里的 7 行，手工 5 行（commit、arrogant、intrigue、relevant、compulsory）。
    组合列已经讲过同样内容的不再加。视频暂不读这一行。`columns.py reformat` 把它当普通行留在原位（再跑不变）。

67. **身份和分工**。同一个词根的几种写法、意思相近的前缀和后缀，都要讲清两件事：各是什么**身份**（这个写法 / 这个词缀是什么来头），怎么**分工**（什么时候用哪个）。写法：`身份：一句话。分工：一句话`——身份后面是句号；分工里面不能有句号，一条讲一个（一类）写法，用“；”隔开，括号里是例词；分工后面是“。意思：…”“；记：…”或行末。
    - **词根**（459 行、103 个词根族）：写在“字母变化：…。”后面。身份是这一行这个写法的，从固定的几种里挑（`shenfen_data.py` 的 ID）：词根本来的样子；动词原形的样子；过去分词的样子（“被…了的、做过了的”，相当于英语的 -ed 形式）；接在前缀后面的样子（复合词里元音弱化）；
      经法语传进英语的样子；带连接元音的样子；由它造出的名词 / 形容词 / 另一个动词的词干；-at- 过去分词词干；英语拼写上的另一种写法……个别的直接写一句（maj：比较级的样子（“更大”）；maxim：最高级的样子）。
      分工是整个词根族的，同族每一行（用原形的行也算，138 行）写同一句：`duce 是动词原形的样子，当动词，说“领”这个动作（produce、reduce、introduce）；duct 是过去分词“被领出来的”，当名词（product），后面还能接 -ion（production、introduction）；英语有时直接拿拉丁语的过去分词当动词，所以 conduct 当动词也用 duct（同 act、collect）；duc 原样留在 educate、duke 里`。
      讲法的核心（用户认可的）：**拉丁语动词有“原形”和“过去分词”两个样子，就像英语 make / made；原形进英语当动词，过去分词（多一个 t / s）当名词、形容词，后面再接 -ion、-ive、-or**；别的几种是“前面有前缀时元音弱化”“经法语口语磨损”“带连接元音”。例词都是总表里的词。
    - **前缀、后缀**（4316 行：后缀 3472 格、前缀 844 格）：写在那一行末尾（有“；记：”的在它前面）。身份、分工照 `cizhui_catalog.py` 一字不改：后缀按“写法 + 变成什么词性”查（词性读组合列第一行末尾的“词性变化（-ous）：名词 → 形容词”），77 种；前缀按写法查，in- / im- 这类两种意思的看那一行开头说的是“不”还是“向里”，43 个；
      分工组 20 个（名词变形容词、动词变形容词、动词变名词、形容词变名词、说“人”的、身份集体、小称、变动词、副词、比较级；否定、在上、在下、向外、向里、一起、在前、自己、ad- 的各种写法、中间穿过）。
      这一行自己说的词性和目录对不上的不加（行里写“名词词尾”、组合列却写“变成形容词”）；目录里没有的词缀（约 1360 行：-s 复数、-e、-on、re-、de-、a- 等）没加。
    - **这个词为什么用它**：还是写在词缀行下面单独一行“为什么用 -ous 不用 -y / -ful：…”（以前各轮手写的 1072 行，这一轮没有新写）。新写要逐词查 etymonline：整个从法语、拉丁语借来的（后缀早就定了），还是英语自己造的（配本族的后缀）——不能按“外来词配外来后缀”一概而论（beautiful、powerful 都是法语来的词配 -ful）。
    数据：`shenfen_data.py`（ID、FAM）、`cizhui_catalog.py`（SUF、PRE、GROUP）；试算 `shenfen.py`、`cizhui.py`（再跑不变）；体检 `shenfen_check.py` 的 var_no_id、id_bad、fam_missing、affix_todo。

68. **辨析列**（17 列表的第 14 列，紧跟在组合列后面）。组合列原来的【辨析】段整段挪过来（7879 行，一字不改，不带“【辨析】”三个字），组合列不再有；组合列步骤里的“（…见【辨析】）”和别的列里的“X 的【辨析】”改成“见辨析列”“X 的辨析列”（约 520 处）。一格的样子：
    ```
    【同义词】产品：product、produce（农产品）
    【同义词】结果：product、result、outcome、consequence、effect
    product 是可数的“产品”：工厂造出来、拿去卖的一件件东西（a new product 一件新产品）
    produce 是不可数的“农产品”：地里长出来的蔬菜、水果（fresh produce 新鲜农产品）
    逻辑不同：product 用的是过去分词 duct“被领出来的”，说的是“已经造好的一件东西”；produce 用的是动词原形 duce，是把动词“生产”直接当名词用，说的是“地里产出来的那一类东西”
    ```
    - **【同义词】行是算出来的**（`bianxi.syn_lines`，4986 行有）：含义列里同一词性、同一个中文意思（“、”隔开的每一个说法算一个）的词算一组；前面带括号的意思（（英）（计算机）（短途）…）不进索引；过去式、另一种拼法、英美两种写法、同一个词的变化形式不算。
      辨析的话里点了名的词排在前面，它的中文意思和本词一个包着另一个的也算（produce 农产品 / product 产品，括号里写它自己的说法）。本词写在最前面；一格最多 3 行、每行最多 6 个词。全表 3323 组、涉及 4647 个词（`bianxi.py --groups` 出清单）。
      它只管“中文意思一样”，不管常不常混——introduce 的“提出：float、pose、file…”这种也在。要不要拿来讲，做视频时看。
    - **辨析的话**：原文照搬。同组的词本行一个也没提到的，从同组别的词那一行抄提到本词的那一句（538 行；那一句没点自己的名字的，前面加“词：”）。还有 2191 行同义词组没有任何辨析的话（`shenfen_check.py --todo`、改动清单「辨析待补」表），以后一轮轮补。
    - **“逻辑不同：”一行**：从构词上讲两个词差在哪儿（一个是动词原形直接当名词，一个是过去分词）。这一轮只有 produce、product 两行手写了样板；以后补辨析时，能讲的加上。

69. **这一轮没有做、不要当成已经做了的**：① 逐词的“为什么用 -ous 不用 -ful”没有新写（第 67 条）；② 【同义词】行没有逐行人工看过，只抽看了几十行；③ 词缀的身份、分工是一个分工组一段话，没有照每个词改写；
    ④ 词根族的分工 103 条是手写的，身份对照过表里原有的“字母变化”说明，没有逐条再查词典——用户或以后发现哪条不对，改 `shenfen_data.py` 再重写那一族；⑤ 讲整词拼写变化的行还在词根列（第 65 条）。

70. **表现在 17 列，怎么写回**。加列、改动面大（这一轮 8805 行）用 `xlsx_write.rebuild`（照内存里的整张表重写；见 SKILL.md“出表”）；小改动还用 `xlsx_write.write`（列宽从表里读，16、17 列都行）。
    按列名读表用 `linetools.load_table`；按 22 列写的老脚本先 `to22.py`。改动清单这一轮是 `scripts/archive/shenfen/report.py`（词根列改前改后、合起来、其他列、词根族分工、词缀身份、词缀分工组、同义词组、辨析补来的、辨析待补）。

## 2026-11 拉丁语动词变化轮定下的

起因：用户看了视频第三十四版“身份和分工”那一幕（duce 是动词原形的样子、duct 是过去分词的样子）和结尾的总结，提了两件事：
① “要写出来拉丁语原形，过去式，过去分词的变化规律”；② “最后的总结部分有溢出；有的内容比较多的，可以分两页进行总结”（②只关视频技能，见它的 6.1）。
①要动总表：视频照表画、照表念，表里得先有这个动词的三个样子和规律。

71. **拉丁语动词的词根族，词根行写出三个样子和变化规律**。写法（紧挨在“身份：”前面，前后都是句号）：
    `动词变化：原形 ducere“领”→ 过去式 duxi“领了”→ 过去分词 ductus“被领的”；规律：过去式是 duc 加 s，c 和 s 合写成 x；过去分词是 duc 加 t。`
    - **是整个词根族的**：同族每一行（变体行、用原形的行）写同一句，和“分工”一样；这一行用的是哪个样子，看它后面的“身份：”。数据在 `scripts/dongbian_data.py` 的 VERB，钥匙和 `shenfen_data.py` 的 FAM 一样是（组号, 词根）；只给写了“身份、分工”的行加。57 族、318 行。
    - **三个样子**：名字只用“原形”“过去式”“过去分词”（用户的说法；学生拿英语的 do / did / done 对）。原形写不定式（ducere），过去式写词典里的第三个主要形式（第一人称单数 duxi“我领了”），过去分词写 -us（ductus，和表里“字母变化”一段的写法一致）；一律不写长音符号。
      每个后面是引号里的中文：过去式“…了”，过去分词“被…的 / …了的”（照这一族分工里的说法：站定了的、看过了的、被领的）。
    - **没有单独过去式的**（异相动词 gradi、mirari、metiri、experiri——样子是被动的、意思是主动的）：只写“原形 …→ 过去分词 …”，规律第一句说“这个动词只有被动的样子，没有单独的过去式”。视频里中间那个框画成虚线。
    - **单独不用的词根**（fend、stingu、peri）写一个真实的带前缀的动词（defendere、distinguere、experiri），规律第一句说明“fend 只接在前缀后面用（这里是 de 加 fend）”；friger 表里两个词都是 refrigerare，也写带前缀的。
    - **规律那句话**（视频写在三个框下面、配音照念）：先过去式、后过去分词，用“；”隔开，里面不能有句号，不写“意思是 / 意思：”；**念出来的部分只用词根、单个字母和中文，拉丁语、英语的整词放进括号**（括号里的字画面上有、配音不念）；
      说法和这一族各行“字母变化”一段对得上（d 碰上 t 变成 s、g 在 t 前面写成 c、v 在 t 前面掉了、前面有前缀时元音弱化）。同一种变法用同一句话（`dongbian_data.py` 的 ARE、DEP、REDUP、SAME）：
      重复开头的音（steti、cecidi、cucurri、pependi、spopondi）；只换元音 a → e（feci、cepi、fregi）；只把元音念长、写法不变（vidi、movi、veni）；加 s，和前面的辅音合写成 x（duxi、dixi、spexi、struxi、fluxi、vixi、auxi、distinxi；plausi、gessi）；
      不变样（verti、volvi、prehendi、pandi、defendi）；加 u（monui、docui、serui、terrui、nocui）；加 v（plevi、crevi、nutrivi、quaesivi）；-are 这一类最整齐，加 -avi、-atus（16 族）；ferre → tuli → latus 是借别的动词。
    - **不让这一段干扰别的体检**：它里面有“→”“过去分词”，原来的脚本会把它当成“通到今义的链”“过去分词词干”。看这一行本身写了什么之前先去掉这一段：`cols.strip_dongbian`（和 `strip_shenfen` 谁先谁后都行）、`cols.strip_meta`（两段都去）；
      `shenfen.cut`、`guoqu_check.py`、`tonggen_check.py` 已经这样做了。以后新写的体检脚本读词根行，也先 `strip_meta`。
    - 表里别处原来就有“动词变化”四个字（-ish 那几行的“古法语动词变化时带出的 -iss-”、swear 的“动词变化：swear – swore – sworn”、vet 的“动词变化：双写 t”）：那是另一回事，不动；脚本和视频只认带“；规律：”的这一段。
    体检 `shenfen_check.py` 的 verb_missing、verb_diff、verb_bad、verb_stray（都应为 0）；试算 `dongbian.py <表>`（要改的格 0）。

72. **这一轮没有做、不要当成已经做了的**：① 57 族的拉丁语形式是照语法写的（词典的主要形式），逐个查过词典的只有 ovare（过去式只在后来的拉丁语里才有，没收）；别的没有逐个再查——用户或以后发现哪个不对，改 `dongbian_data.py` 再 `--write`；
    ② FAM 里还有 5 族和动词沾边、没收（ov、batt、fid、gen、ped，原因记在 `dongbian_data.py` 的 SKIP）；③ 没有变体的动词词根（port、scrib、mit、tract、ject……）词根行没有“身份、分工”，视频没有“身份和分工”那一幕，这一轮没写三个样子——用户说要再做（那要先给它们立词根族、定画在哪一幕）；
    ④ 希腊语的词根族（graph、gno、cri、ly、plas、dra、thea……）没写：希腊语动词的变法不是这一套；⑤ 这一段只写在词根列，后缀列讲 -ion“接在过去分词词干后面”的地方没有回指它；⑥ 上一版维护技能（身份分工辨析版）对着这张表会误报，要用这一版。
    出表这一轮是 `dongbian.py --write`（=`xlsx_write.write`，只动 318 格）；改动清单 `scripts/archive/dongbian/report.py`（说明、动词变化、词根列、没收的）。

## 2026-11 词缀来历、记法轮定下的

起因：用户看了视频第三十五版（6.1）以后要求：前缀、后缀也像词根一样讲清来历、给出记法（pro ≈ for 这种）；三个样子那一幕要讲清“ducere 怎么成了 duc”；词根行里复杂的例词去掉；
geo ≈ geography、bio ≈ biology、vac ≈ vacation、logue ≈ dialogue 这种拿含有同一个词根的词来记的换掉（用户：“geo 应该是盖亚女神吧”“这些不好看的你可以再网上查找一下试试”；
bio：“两个都写一下，就说有两个可能”；sub ≈ up：“可以写，但是要解释清楚，逻辑上要清晰”）。这一轮前后用了三个对话（前两个对话做的改动都没留下来），第三个对话照对话记录里定下的做完。

73. **词缀来历**（前缀列、后缀列）：每个词缀（一种用法）一条来历，写在来源括号里，整句替换原来的来源那一段。
    - 写法：哪种语言 + 原来是什么（单独的词 / 词尾）+ 什么意思 + 怎么进入英语。例：`来自拉丁语介词 pro“在前面、向前”，本来是单独的一个词`、
      `来自古英语 lic“身体、样子”，本来是一个单独的词：带着…的样子 → 以…的方式`、`来自拉丁语名词词尾 -io，变格时写作 -ionem，经法语磨成 -ion 进入英语`、`英语本来就有，就是单词 over，古英语写作 ofer`。
    - 来历里不写同源的英语简单词（写在记法里，第 74 条），不写例词（“同 例词”照旧跟在后面；2026-11 例词清理轮起只留“单词 + 这个词缀”的简单例词，第 79 条），不套括号（视频卡片上只显示一行，括号套括号看不清）。
    - 视频（wordfilm.js 的 affixSource）靠括号里“经”字前面的语言名认来源：“经…”前面只写来源语言本身；英语本族的写“英语本来就有…”或“古英语…”。
    - 目录：`scripts/laili_data.py` 的 ENTRIES（约 100 条：前缀按写法和意思 sense / need，后缀按写法和“变成什么词性”kind）；工具 `scripts/laili.py`。
      旧来源那一段从开头对得上目录里的 head 正则才换；同一个括号里的“同 例词”、讲写法的半句（在 c 前写成 ac-）、别的说明照留；
      已经由新来历或记法讲了的半句（“和 like 是一家，见 like”“和 duo“二”有关”“同一个前缀两个意思：往回 / 再一次”）去掉。
    - 认不出的旧写法不动（101 行，改动清单「来历没换的」）：多是这一行自己的特殊来历（prisoner 的 -er 来自古法语 -ier、exchange 的 es-、moisture 的 -our）。
      一点来源都没写、正文里也没提哪种语言的才补（这一轮 4 行）；第一句讲的不是这个词缀本义的（“这里不是…”“= 古法语 a”“看上去是 ad-，其实是假的”）不补。
    - 这一轮：换 2855 行、补 4 行；1501 行原来就是目录那一句（-er、-ed、-ic、-ness 这些以前就统一了）。
74. **词缀记法**：和词根的记法（第 59、63 条）同一个写法，写在那一行末尾（身份、分工后面）：`；记：pro ≈ for（为了）：道理。音变：p 对 f：一句话（印欧语词根 *…；同 …）`。约 1006 行。
    - 名单（用户同意的，同源关系都对照过 etymonline 整站数据）：pro ≈ for；dis ≈ two；ad ≈ at（ac-、af-、ap-、ar-、as-、at- 这些写法也写 ad）；ab ≈ off；super ≈ over（sur- 也写 super）；
      sub ≈ up（sup-、suc-、suf-、sus- 也写 sub）；trans ≈ through（词典说“也许”，道理里照写）；表示“不”的 un- / in- / non- ≈ no（im-、il-、ir- 写 in）；en ≈ in（em- 写 en）；
      mis ≈ miss；be ≈ by；-ly ≈ like（副词、形容词两种道理）；-ful ← full（← 是“从它变来”）；-less ≈ lose（道理里说清和单词 less“更少的”只是长得像）；-ship ≈ shape；-teen / -ty ≈ ten（只给数词的 -ty）。
    - 不写的：re-、com- / con-、ex-、de-、pre-、inter-、per-、ob-、-ion、-ment、-al、-ous、-ive、-ity……（查不到学生认识的同族简单词）；表示“把…反过来”的 un-（undo、untie）不写 un ≈ no；
      mischief 这类拉丁语来的 mis-、希腊语的 di-“二”、en-“在里面”、名词的 -ty（来自拉丁语 -tas）不写。
    - sub ≈ up 的道理先讲清为什么一“下”一“上”还是一家（用户：“逻辑上要清晰”）：`同一个印欧语词根既是“在下面”，又是“从下面往上”：拉丁语留下了“下”，就是 sub；英语留下了“上”，就是 up。所以 sub 有时也是“从下面往上”：support 就是从下面往上托住，sup 就是 sub`。
      道理的第一句要能单独看懂：卡片上的“记”框只显示两行，后面的配音照念。
    - 已经有老说明“可以这样记：…”的行照样加（那不是 X ≈ Y 的记法）。数据在 laili_data.py 的 MEMO；体检 `laili.py --check`（memo_missing、memo_bad）和 `part_memo.py --check`（音变）。
75. **拉丁语动词的规律，第一句讲“原形去掉词尾就是词根”**（用户看三个样子：ducere 和 duc 怎么连上）：`规律：原形去掉词尾 -ere 就是 duc（ducere → duc）；过去式是 duc 加 s，…；过去分词是 duc 加 t`。
    - 数据：`dongbian_data.py` 每族加 `cut`，`dongbian.seg` 写成“规律：cut；rule”（57 族、318 格）。只接在前缀后面的写“fend 只接在前缀后面用：原形去掉前缀 de 和词尾 -ere 就是 fend（defendere → fend）”；
      原形里多出来的字母在这一句讲（cresc 的 sc、frang 的 n、cern 的 n、quaer 的 r 本来是 s、ger 的 r 本来是 s、fluc、strug 原来带的辅音）。
    - 拉丁语整词放进括号（画面上有，配音不念），念出来是“原形去掉词尾 e r e 就是 d u c”。规律最多三句（视频一句一行、最多三行）；原来就三句的族，把“去词尾”并进第一句。
    - 规律括号里的复杂例词去掉：respiratory、refrigerator、vocation、duration、elevate、complicate、mutate、curator、admiration、tentative、vegetation、salvation、imperative、reputation、desperate、ornament、flux、fluctuate、exploit；
      只留学生认识的：vacation、separate、accurate、question、secret、certain、create、victory、relate、translate。
76. **词根列的复杂例词去掉**：词根行“同 …”里，同一个词根的“前缀 + 词根”“词根 + 词根”的词（学生还得先拆它）去掉：maintain 的 contain、obtain、retain，event 的 prevent、adventure，important 的 transport。
    和第 62、63 条一个道理（“不要让学生去看更复杂的”）。
    - 留着的：音变对照（同 ped- 和 foot）、讲变法的（同 invade → invasive、triple ← triplus）、带“见”或“X 的 Y”的说明（receive 的 ei，见音变栏）、表里没有的词、不含这个词根的词、
      本词里就包着的（production 的 product、opposition 的 position）、基础词和变体词（⑤ ②：dose、faith）、只是词根加后缀的（porter、author、mandate）、“同 …”后面是一句话的。
    - 工具 `scripts/lizi.py`（试算；写好的表应是 0）。这一轮 40 格、52 个例词，改动清单单列「去掉的例词（请过目）」，用户要留的照原样恢复。前缀、后缀列的“同 例词”这一轮没动——**这个判断错了**：用户要去掉的“复杂例词”本来就包括 pro- 行的“同 progress”，下一轮（例词清理轮，第 79 条）补做。
77. **词根记法补换**（第 59、63 条接着做）：
    - 换掉 4 个拿含有同一个词根的词来记的：geo ≈ geography → **geo ≈ Gaia**（盖亚，大地女神；她的名字就是“大地”，gē 和 gaia 是同一个词的两种写法）；
      bio ≈ biology → **bio ≈ zoo**（动物园），道理里写两个可能：zoo（希腊语 zōion“活的东西”）、quick（最早是“活的”），音变 b 对 z、b 对 qu；
      vac ≈ vacation → **vac ≈ want**（want 最早是“缺少”；两个词都出自 *eue-“缺、空”），音变 v 对 w；logue / log ≈ dialogue → **≈ logo**（logo 很可能是 logogram“代表一个词的符号”的缩写，来自希腊语 logos“词、话”）。
      logic、prologue 因此有了记法，「词根变体处理」的“记法待补”去掉，还剩 33 行（lect、mit / miss、graph / gram、simple 的 ple）。
    - 新加：gen / gener ≈ kind（g 对 k）、mon ≈ mind（o 对 i；monitor、summon、monster、monument、demonstrate）、the ≈ do（th 对 d；道理里说明不是冠词 the）、ly ≈ loose（analysis、paralyze）；index 补上了早就有的 dic ≈ teach。
    - part_memo_data.py 的 SHIFT['ten'] 改成只给 dec 一族（-teen、-ty ≈ ten 写法相近，不要音变）。
78. **这一轮没有做、不要当成已经做了的**：① 目录只收了 5 行以上的词缀用法（前缀 51 种、后缀约 60 种），少见的词缀和 101 行认不出的旧写法还是原样；② 补来历只补了 4 行，
    别的行正文里已经用自己的话讲了来源（“它是拉丁语来的前缀”），没有再加括号；③ 词缀记法只写了用户同意的名单；④ 词根记法还有约 1500 行没有（多是只出现一次的词根、连接成分），
    lect、mit / miss、graph / gram 还是待补；⑤ 去掉的例词是程序按规矩挑的，逐个看过一遍，没有一个个查课本。
    改表脚本 `scripts/archive/laili/round.py`，改动清单 `scripts/archive/laili/report.py`。

## 2026-11 例词清理轮定下的

起因：用户拿上一版总表看 produce 那一行，前缀列还写着 `pro-：“向前”（来自拉丁语介词 pro…）；也表示“预先”（同 progress 进步：往前走）；…；记：pro ≈ for…`：
“很早之前的一些残留的信息上个对话进行的优化还没有去除……之前就是因为 pro 同 progress 进步：往前走；用 progress 来记 pro 把问题变得更加复杂了，所以才进行的优化，新版本是优化好了，
但是这些之前的信息好像没有删除，还在里面，这样不行，会误导学生，我希望能把这些信息去掉，让新版本的内容更加准确，没有其他误导信息……你看一下整个表里面，看看还有多少存在这样的情况”。
上一轮只换了来历、加了记法，把前缀、后缀列的“同 例词”当成“这个词缀的例子”一个没动（第 76 条末尾）——用户说的“复杂例词”其实包括它们。
查完向用户问了两件事（“简单例词要不要也去掉”“‘也表示“预先”’要不要留”），回复：**“先不去掉”**——所以只去复杂的。

79. **词缀行的复杂例词去掉**（前缀列、后缀列）。和第 62、63、76 条一个道理：解释一个部分的那一行，不让学生去看更复杂的词。
    - **规矩**：“同 例词”的例词要是“学生认识的单词 + 这个词缀”（unhappy = un + happy、rewrite、return、disagree、teacher、quickly、action、national），一眼看得出词缀加上去起了什么作用。
      例词自己还带着不能单独用的词根（progress = pro + gress、include = in + clude、connect、exit、prepare、create = cre + ate、visible、culture、dictionary、finish）的去掉——学生还得先拆它，gress、clude 他不认识。
    - **怎么判断**（scripts/lizi.py 的 `ex_status`）：
      例词在表里 → 它那一行「词根」列有不能单独用的词根就算复杂（连接成分 -i-、双写的字母不算；informat(=inform) 这类“单词的过去分词词干”——解释以“inform（…）”开头——算单词）；
      基础词、不好拆分、变体词（⑤ ④ ②：magic、written）和没有词根的词（单词 + 词缀、合成词：input、kind-hearted）留。
      例词不在表里 → 去掉这个词缀（或常见词缀）剩下的是表里的词、或表里的词加 -er / -ed / -ing / -s，就留（replay → play、non-smoker → smoke、blue-eyed → eye）；不是就去掉（picture 剩 pict、sympathy、evade）。
      逐个看过、和规则不一样的记在 scripts/lizi_data.py：`KEEP_IN`（表里带词根也留：English、Irish、Portuguese、Australia、January、fifteen、best、inner、scissors——国名、民族名、月份、数词、不规则的比较级最高级，讲的不是怎么拆）、
      `OK_OUT`（表里没有、可以留：American、Japanese、always、drunkard、observatory……）、`DROP_OUT`（表里没有、剩下的碰巧是个词、其实还得拆：triad、animal、inferior、canine……）、`BASIC`（学生认识、表里没有单独一行的基础词：big、fast、ten、mouth、bus……）。
    - **留着不动的**：讲变法的对照（同 possible → possibly、hop → hopping、communicate → communication）、短语（同 turn over）、“为什么用 -er 不用 -or”那一行、身份分工里的例词（pro- 多是“向前”（progress、produce）——那是讲分工的，见第 82 条）、
      记法和音变里的对照（同 ped- 和 foot）、不带“同”字的对比说明（和表示“向里”的 in-（include 包括）长得一样）。
    - **只删字，不改写别的话**：例词去掉以后括号空了就去掉括号；`（来历；同 progress 进步：往前走）` → `（来历）`；`在 r 前写成 ar-，同 arrive 到达；在 c 前写成 ac-，同 accept 接受` → `在 r 前写成 ar-；在 c 前写成 ac-`；
      `；也表示“预先”（同 progress 进步：往前走）` → `；也表示“预先”`（“也表示…”这句本身留着，用户：“先不去掉”）；一串例词里只去掉复杂的（`同 include 包括、input 输入` → `同 input 输入`）。
      程序逐条核对过：每一行的新文字都能由旧文字只删字得到，没有留下空括号、连着的分号。
    - 这一轮：前缀列 451 格、去掉 560 个例词（exit 49、connect 37、combine 37、include 31、progress 26、export 25、prepare 23、descend 22、accept 22……）；
      后缀列 563 格、去掉 834 个（create 70、visible 36、culture 28、celebrate 22、dictionary 19、library 18、finish 14、physics 14、punish 13、picture 12……）。
      留着的例词约 5200 处：单词 + 词缀 4134（action、invention、teacher、quickly、national、rainy、rewrite、return、unhappy……）、表里没有的简单词 910、基础词和变体词 135、名单里的 19。
80. **词缀行的“见 X”**：X 只是含有同一个词缀的别的词、自己还带词根的去掉（product 的 pro-“见 produce”、universe 的 uni-“见 unify”、biofuel 的 bio-“见 biology”、receipt 的 re-“见 receive”、telegraph 的 tele-“见 telegram”）——
    每一行现在都有自己的来历，不用再让学生去看别的词（第 62 条用到词缀行上）。32 处（前缀 30、后缀 2）。
    - 留着的：X 是简单词或基础词（见 like、见 full、见 self、见 unhappy、见 react、见 stepmother、见 nanometre）、本词的另一种拼法（recognise 见 recognize、dialog 见 dialogue、program 见 programme——`_norm_variant` 把 -ise / -ize、-our / -or、连字符这些归成一个样子再比）、
      “见 X 的【背景】”“详见 X”。例外可以记在 lizi_data.SEE_KEEP（现在是空的）。
    - 个别改写记在 lizi_data.FIX：proportion 的 `pro-：这里是拉丁语 pro“按照、依照”（不是 progress 里的“向前”）` → `（不是“向前”的意思）`。
81. **词根列补漏**（第 76 条接着做）：上一轮的程序只认“同组、或写法前三个字母一样”的词根，漏了三种，这一轮补上，共 68 个例词、51 格：
    - 两个字母的词根：circuit 的 it 行“同 exit 出口：走出去、transit 经过：走过去”；
    - 写法不一样的同一个词根（按拆分里的 (=X) 认）和放在词根列的前缀成分：extreme 的 ex- 行“同 exit、export”、perform 的 per- 行“同 perfect”、religion 的 lig 行“同 rely”、control 的 contra- 行“同 contrast”；
    - 表里没有的“前缀 + 这个词根”的词：provoke 的 voke 行“同 invoke、revoke”、invade 的“同 evade、pervade”、intrude 的“同 extrude、protrude”、illusion 的“同 allude、interlude”（上一轮答应去掉、没去成的）。
      程序认得出“已知前缀 + 这个词根”的；认不出的逐个看过记在 lizi_data.ROOT_DROP（(本词, 例词) 30 对），ROOT_KEEP 是留着的（wouldn't、alchemy：讲的是同一个写法）。
    - 照第 76 条留着的没变：“词根 + 后缀”的词（version、porter、ludicrous、noxious）、音变对照、讲变法的、带“见”“…里的 X”的说明、连接成分那一行的例词（sportsman、craftsman）、“动词变化”“身份、分工”里的例词。
82. **这一轮没有做、不要当成已经做了的**：
    ① **简单例词留着**（用户：“先不去掉”）：un- 行还有“同 unhappy 不开心的”，-er 行还有“同 teacher 老师、driver 司机”。用户以后要是说词缀行一个“同 例词”都不留，再做一轮（改 lizi.ex_status 一律返回 complex 就行，变法对照另说）。
    ② “也表示“预先””这类讲词缀别的意思的半句留着（produce 那一行用不上“预先”，provide 那一行用得上）。
    ③ **身份、分工里的例词没动**：`pro- 多是“向前”（progress、produce）`、`in- …（include、import）` 是目录 cizhui_catalog.py / shenfen_data.py 里的话，视频“身份和分工”那一幕照念“比如 progress、produce”。要换成简单词得改目录、重写几千行，另做一轮。
    ④ 不带“同”字的对比说明里的例词没动（`和表示“向里”的 in-（include 包括）长得一样`，约 160 种说法 200 处），单词部分列的“同 …”（多是讲拼写、读音的对照）没动。
    ⑤ 去掉例词以后一个例词都不剩的词缀行（-ate、-ary、-id、ex-、con- 的不少行），没有另补简单例词——有来历、作用、身份分工和本词自己，够讲；要补得一个词缀一个词缀挑（-ate：activate；ex-：ex-wife 之类意思不一样，不好挑）。
    ⑥ 表里没有的例词是逐个看着定的（OK_OUT / DROP_OUT），没有一个个查课本；改动清单「去掉的例词（请过目）」「留着的例词汇总」请用户过目，要恢复的照「逐格」的改前恢复、并记进名单。
    ⑦ 顺带：tentacle 的 -cle 去掉例词以后，“小”字挪进了前 60 个字，cizhui.py 会把它认成小称后缀、要加身份分工；这一行第一句讲的是“用来…的东西”，不是“小”，
       所以把 cizhui.pick_suffix 改成“小”要写在第一句（第一个“；”以前）里才算——体检和上一版一样是 0，没有给它加身份。
    改表脚本 `scripts/archive/lizi2/round.py`，改动清单 `scripts/archive/lizi2/report.py`。

## 2026-11 词缀身份辨析轮定下的

用户看上一版总表 produce 那一行的前缀列（`pro-：“向前”（来自拉丁语介词 pro…）；也表示“预先”；这里是“向前、到前面来”；身份：拉丁语来的前缀（pro“向前”）。分工：…；记：…`）：
“你看前缀，有身份、分工、记这几个部分，我觉得很好；但是现在最开头的介绍和身份好像重复了，我希望这两个能变成一个，合并起来……这开头的介绍和身份其实讲的是一个意思”
“分工我觉得可以变成辨析：就是有的前缀意思、功能都差不多，但这个词就是用 ive，不用 ful，要分别把这些前后缀都讲一讲，其实就是现在分工做的事情”
“最后的记这一部分，放在身份的后面，因为是帮我们专门记住这个前后缀、词根的”“先把前缀、后缀这两部分优化一下”。
看了辨析的样子又说：“pro-、pre- 两者相近，要放在一起，而且还要说 pro- 和 pre- 的区别，具体怎么用也要说一下；fore- 是英语自己的，具体怎么用也要说一下；就是不能只说来自哪里，也要说具体的用法，起到什么作用”。

83. **词缀行的写法：身份 → 记 → 辨析**。前缀列、后缀列里讲一个词缀的那一行（前缀 1408 行、后缀 4321 行）写成
    `标签：身份：开头的介绍[；记：记法][。辨析：辨析的话]`。
    - “标签：”后面紧跟“身份：”；“；记：…”在中间；“。辨析：…”是这一行最后一段，前面是句号，到行末为止，里面没有句号。
    - 讲词缀的行：前缀列里标签以 - 结尾、后缀列里标签以 - 开头（标签里括号的话不算：`il-（= in-）`、`di(s)-`、`-et / -ette`）。“为什么用 -ous 不用 -ful”“注意”“-ize 还是 -ise”“-ist + -ic”这类说明行不是词缀行，照旧。
    - 只动了前缀、后缀两列。**词根列这一轮没动**，还是“…。字母变化：…。动词变化：…。身份：…。分工：…。意思：…；记：…”（第 65、66、71 条）；用户说的是“先把前缀、后缀这两部分优化一下”，词根要不要也改成这个先后，等用户定。
    - 读写用 `scripts/linetools.py`：`is_affix_label`、`affix_split`（头 / 正文 / 尾，接起来就是原行）、`affix_parts`（身份、记、辨析）、`affix_join`、`add_memo`（新记法插在辨析前面）。
84. **身份 = 开头的介绍**。原来开头的介绍直接当身份，单独那句“身份：拉丁语来的前缀（pro“向前”）”并掉（4317 行）——括号里已经写了“来自拉丁语介词 pro”。
    - 身份开头**不加**“拉丁语来的前缀”这种来头（问过用户，用户：“按你的要求来”——照当时的倾向：不加，免得和括号里的“来自拉丁语”重复）。
    - **每一行词缀都标“身份：”**，原来没有身份、分工的行（re-、de-、-s 等，约 1400 行）也标（同上，照倾向：全表一致）。
    - 原来那句身份里独有、开头没讲的话接在介绍后面，不丢（-ness 的“英语本族的后缀…几乎什么形容词都能接”、-able 行里“和 -ible 的分工：英语自己新造的词多用 -able…”）。
    - 以后新写一行：先写意思 / 作用，来历进括号（第 73 条），这个词里取什么意思、写法怎么变接在后面——这一整段就是身份；目录 SUF / PRE 里那句“来头”只作参考，不写进表。
85. **辨析（原来的“分工”）：讲清每个词缀怎么用，不能只说来历**。意思、功能相近的词缀放在一组，一组一句话，同组每一行写同一句（一字不改，照 `scripts/cizhui_catalog.py` 的 GROUP）：
    - 开头是总说：“同样和“前面”有关：”“同样是把名词变成形容词：”“这几个都是同一个拉丁语前缀 ad-：”。
    - 一个词缀（或写法相近的几个：`-al、-ic`、`con-、col-、cor-`）一条，“；”隔开。每一条：是哪儿来的（英语自己的 / 拉丁语来的 / 经法语变来的）→ **接什么词**（日常的本族词、拉丁语来的动词的过去分词词干、名词、形容词…）→ **说什么意思**（引号里）→ **和旁边那个差在哪儿**（“和 -ful 正好相反”“不是时间上的“先””“和 pre- 只差一个字母，别弄混”“-ing 多讲东西给人的感觉，-ed 多讲人自己的感受，正好一对”）。
    - 写法相近、容易混的挨着放（pre- 在前、pro- 紧跟，fore- 最后）。括号里是例词，都是总表里的词（“more beautiful”是短语，例外），放在这一条的最后。
    - 20 组：前缀 10 组（neg 不、into 向里、out 向外、with 一起、ad、before 前面、over 上面、under 下面、between 中间、self 自己，共 834 行），
      后缀 10 组（adj_n 名词变形容词、adj_v 动词变形容词、n_act 动词变名词、n_qual 形容词变名词、n_person 人、n_status 身份集体、n_dim 小、v_make 变动词、adv 变副词、cmp 比较，共 3452 行）。`python3 scripts/cizhui.py <表> --groups` 列出来。
    - 视频第三十八版照这句话画“前缀辨析 / 后缀辨析”、一条念一句：所以一条开头写词缀，总说用“同样…：”或“这几个…：”开头，例词括号里只写英文，整句没有句号、没有“意思是“”。
86. **哪一行挂哪一组**（`scripts/cizhui.py` 的 pick）：后缀按“写法 + 变成什么词性”（读组合列第一行末尾的词性变化），前缀按写法（in- / im- / il- / ir- 两种意思的看开头说的是“不”还是“向里”）。
    - 这一行明说自己不是那个词缀的不挂（“不是 actor 里表“人”的 -or”“看上去是 ad-，其实是假的”“这里不是“有点…”的 -ish”）：开头是“不是 / 这里不是 / 看上去 / 看着像”的规则直接跳过；别的逐个记在目录的 `NO_BX`（34 行：希腊语的 en- / em-、英语自己的 in、electronic 缩成的 e-、拉丁语形容词词尾 -est、材料名词后面的 -en…）。
    - 开头的介绍绕了弯、规则挑不对的，逐个记在 `FORCE`（6 行：undo 的 un-、insure 的 in-、guardian、plumber、arguably、puddle）。
    - 几条专门的认法：开头的介绍前 30 个字里有“更”的 -er 是比较级（fewer、smarter，组合列的词性变化写成别的也认）；讲“亲昵、昵称、小称”的 -y / -ie 归“小”那一组（doggy、bunny、auntie）；-ward / -wards 变成的词性里有副词就归副词那一组（forward 既是形容词又是副词）；
      “小”要写在第一句里才算小称（第 82 条 ⑦）；接在材料名词后面的 -en（wooden）不算过去分词；e- 的开头要提到 ex- 或“出、外”才算。
    - 新加了词，`cizhui.py --check` 的 affix_todo 会列出来，逐个看（工作十七）。
87. **顺带改正的，和这一轮没有做的**。
    - 上一个对话里改表时处理的（据对话记录；没有出改动清单）：辨析挂错的 65 行不再挂（dozen 的 -en、e-book 的 e-、grammar 的 -ar）；认错组的 7 行改过来（fewer、smarter 的 -er 是“更…”）；
      来历填错的 31 行改正或去掉（eighty 的 -ty 写成了“来自拉丁语 -tas”，upper“更…的”却写“古英语 -ere”）；括号外重复讲来历的 21 行去掉（careful 的“，来自 full“满的””）；新挂上辨析的 15 行（suc-、sug-、sus-、ag-、al-、an-）。
    - 这一轮核对总表时又改 24 格：**辨析挂漏的 19 行**——10 个 -ward 词（forward、backward 是辨析里的例词，自己却没挂；原因是词性变化写的“形容词、副词”两样，程序认不出）、capsule 和 schedule 的 -ule、
      7 个表示亲昵的 -y / -ie（auntie、hoodie、rookie、bunny、piggy、teddy、softy；doggy、sweetie 早就挂了）；其中 **4 行来历填错**一并改正（softy、bunny 写成了抽象名词 -y 的“来自拉丁语、希腊语的名词词尾 -ia”，piggy、teddy 写成了形容词 -y 的“古英语 -ig”，都改成“英语本来就有的亲昵词尾，先见于苏格兰英语”）；
      **来历括号插错位置的 4 行**（词缀来历轮补来历时插进了引号里的小括号：intimidate“使进入（来自拉丁语介词 in…，某种状态）”→“使进入（某种状态）”（来自拉丁语介词 in…），还有 theirs 的 -s、desire 的 de-、off-peak 的 off-）；invent 的 in-“不是表示“不”的 in-”从来历括号里挪到括号外（和别的 in- 行一样）。
      以后补来历：第一句末尾的括号要是在引号里面（“使进入（某种状态）”），来历另起一个括号，不插进去。
    - **没有做、不要当成已经做了的**：① 词根列没动（见第 83 条）；② 组合列约 20 行“词性变化”写错（upper 写成“动词 → 名词”、removal 写成“名词 → 形容词”），上一个对话里发现、记下，等用户定要不要另做一轮；
      ③ 没挂辨析但也说得通的行没补：-ing 写“①变名词 ②作形容词”两用的 44 行（两组都沾边）、“这里不是“被…了的”，而是接在名词后…“有…的””的 5 行（talented）、in- / im-“在…上、向着”的几行（insist、index）、upper 和 inner 的 -er；
      ④ 改动清单这一轮没出（用户：“清单不用生成的”）；⑤ 辨析里的例词是照“总表里有、学生认得”挑的，没有按第 79 条“单词 + 这个词缀”的标准筛（progress、produce 还在 pro- 那一条里——那是讲 pro- 怎么用的例子）。
88. **出表和交付**：
    - **不再出 LZMA 传输包**。用户：“每次你生成的总词库压缩包我的电脑好像打不开”——以前为了压到 3.5 MB，外层用 LZMA（第 58 条），Windows 自带的解压不认，要 7-Zip、Bandizip 才能开。
      `xlsx_write.write` / `rebuild`、`part_memo.py --write` 默认只出 xlsx（zopfli，约 5.5 MB）；用户要压缩包时 `xlsx_write.pack_zip(表)` 出标准 zip（deflate，双击能开）——xlsx 本身已经压过，标准 zip 和 xlsx 差不多大，所以平时直接发 xlsx。
    - 用户赶时间时说得很明白：“只生成这 3 个文件就可以了”“清单不用生成的，打包的暂时不打包”“使用工具时要把不是非常必要的 command 省掉，让整个过程效率最大化”“先生成图片吧，不生成视频；生成一张整个视频的图就可以了”。
      照做：只交要的文件；体检照跑（省不得），但几项并在一条命令里；视频先 `--draft-only --preview-cell 960` 出一张整段视频的预览图，不配音不渲染。
    - 一轮做不完（工具用到上限）时，回复里先如实说清“做到哪了、哪些验证过、哪些还没交付”，再说下一步；不要把没交付的说成做好了。
    - 总表、维护技能、视频技能三样要配套：表的写法变了，两个技能同一轮改（这一轮：表“词缀身份辨析版”、维护技能同名版、视频技能第三十八版 6.2.0）。

## 2026-11 词缀关系轮定下的

用户看第三十八版 produce 的预览图（“前缀辨析”那一幕 pre- / pro- / fore- 三条）：
“前缀 pro-、pre- 这两个都是拉丁语，除了说含义上的区别，还要看看两者之间的关系，pro- 是 pre- 的分词吗？类似这样的，就像 duc 和 duct 这样；
你看看来自同种语言的前后缀，不同形态，是不是存在这种关系，如果有就写出来，没有就算了；比如 or、er、ir 是不是也有这样的区别等等；这个要看看总表，看看所有的这种类似的前后缀，来自同种语言的是不是存在这种关系，要优化一下”。
同一条消息里还有读音拆分的一条（第 92 条）。

89. **关系写在辨析的最后**：`…（例词）；关系：一条；一条`。
    - 位置：辨析的话里最后一段，前面是分号，“关系：”只出现一次；整行还是“标签：身份：…[；记：…]。辨析：…[；关系：…]”，辨析到行末、里面没有句号这两条不变。
    - 一条讲一组词缀，**条首写词缀**（一头带连字符：`-ant、-ent 是…`、`pre- 和 pro- 不是…`、`-ly 当副词词尾…`），条和条用“；”隔开，一条里面不用分号。视频靠条首的词缀认这一条讲的是谁。
    - 括号里放补充：拉丁语、古英语的原词（prae、-bilis、lic），印欧语词根（*per-“向前”），例词（总表里的词，成对的写 `educate → education`）。视频把括号里的话写在画面上、配音不念——去掉括号念出来要是通顺的一句话。
    - 一组一句，同组每一行写同一句，照 `scripts/cizhui_catalog.py` 的 REL 一字不改；`GROUP[组]` = 辨析 + “；关系：” + REL，`CORE[组]` 是不带关系的辨析。读写用 `linetools.bx_split` / `rel_items` / `rel_heads`。
90. **写什么关系、不写什么**。
    - 写的是“来自同一种语言、写法不同的词缀，彼此是什么关系”，像词根 duc / duct 那样讲清身份：
      ① 同一个词尾的两种写法，各跟着什么走（-ant / -ent、-able / -ible 跟着拉丁语动词原形的 -are、-ere / -ire；-ity / -ty）；
      ② 谁加了什么变成谁（-ation = 过去分词的标志 at + -ion；-ance / -ence = -ant / -ent + -ia；-ce / -cy = t + -ia；-ally = -al + -ly；-wards = -ward + s；-let = -el + -et；-ian = i + -an；-ery = -er + -y）；
      ③ 是不是某种语法形式（-ee 是法语过去分词的词尾；-ate 是拉丁语过去分词的词尾；-ette 是 -et 的阴性；trans- 也许本来是现在分词；-ing / -ed 对着拉丁语的现在分词、过去分词）；
      ④ 配成一套的（-or、-ion、-ive、-ory、-ure 都接在过去分词词干后面：act → actor、action、active；-ize、-ism、-ist 是希腊语里的一套）；
      ⑤ 不是谁变出谁、各自长出来的兄弟（pre- / pro-：拉丁语里两个同源的介词）——用户问到“是不是分词”的，不是也要写明。
    - **不写**：辨析那几条里已经讲了的（con-、col-、cor- 都是 com-；suc-、sup- 都是 sub-；e-、ef- 都是 ex-；im-、il-、ir- 是 in- 的写法；en- 是 in- 经法语变来的；sur- 是 super- 经法语变来的；-ty 是 -ity 的短写法）；
      记法里已经讲了的（pro ≈ for、super ≈ over、sub ≈ up、un / in / non ≈ no、ly ≈ like、trans ≈ through、en ≈ in、ad ≈ at）；每一行的来历里已经写了的（名词的 -al 来自 -alia、-age 来自 -aticum）；
      查不到关系的（self- / auto-、-ship / -hood / -dom、-ful / -less / -y / -ish 各有各的来历）——用户：“没有就算了”。所以 neg、into、over、under、out、with、ad、self、cmp、adj_n 十组没有这一段。
    - **出处**：逐条对过 etymonline 整站数据（工作三）。词典自己说 perhaps / probably 的照写“词典说也许 / 多半”（trans- 也许是现在分词；-er 也许借自拉丁语 -arius；-ling 多半是 -le 加 -ing）；
      etymonline 上查不到的不写（sub- 和 super- 是不是一家：它只分别说出自 *upo、*uper，没有说两者的关系，没有写）。-ery =“干这一行的人”的 -er + -y 是照《牛津英语词典》-ery 条的讲法（法语 -erie = -ier + -ie），etymonline 只说到拉丁语 -arius。
    - **关系里的话不能和这一组某一行自己的讲法打架**：写完对一遍例词所在的行（-ery 那一条起先举了“baker → bakery”，而 bakery 那一行讲的是 bake + ery，去掉了）。
91. **这一轮写了什么、顺带改了什么**。
    - 10 组有关系（2758 行词缀行）：before（pre- / pro- / fore-）、between（inter-、trans-）、adj_v（-ant / -ent、-able / -ible、-ing / -ed、-ive / -ory）、n_act（-ation、-ance / -ence、-ion / -ure）、
      n_qual（-ity / -ty、-ce / -cy、-th）、n_person（-or、-er / -or、-ee、-ian、-ist）、n_status（-ism、-ery）、n_dim（-ette、-let、-cle / -ule / -el / -le、-ling）、v_make（-fy / -ify、-ate、-ize）、adv（-ly、-ally、-wards）。`python3 scripts/cizhui.py <表> --groups` 列出整句。
    - 用户问的三处：**pro- 不是 pre- 的分词**（一对兄弟）；**-or 和 -er 不是同一种语言**（-or 拉丁语、接过去分词词干；-er 英语自己的，词典说很早以前也许借自拉丁语 -arius）；**总表里没有 -ir 这个后缀**（只有前缀 ir-，就是 in- 在 r 前的写法；liar 的 -ar 是 -er 的另一种拼法）。
    - 顺带改的 8 行（上一版留下的，核对“人”那一组时发现）：tumor、terror、tremor、error、horror 的 -or 是拉丁语表示状态的名词词尾，却挂了“同样是说“人””的辨析、来历也填成了“做…的人”——辨析去掉、来历改成“来自拉丁语表示状态的名词词尾 -or”；
      clutter 的 -er 是“一下一下地做”的动词词尾，辨析去掉、来历照 wander、linger 那几行改；archive 的 -ive 是 archivum 的词尾、不是形容词后缀，辨析去掉、来历改成“来自希腊语表示地方的词尾 -eion”；relaxing 是形容词，辨析从“动词变名词”换到“动词变形容词”。
      前七行记进 `cizhui_catalog.NO_BX`，relaxing 记进 `FORCE`；`laili_data.py` 里 -or 那一条加了 avoid（开头讲“状态、感受”的不算“做…的人”）。
    - 起先写进去、核对时去掉的：名词 -al、-age 两条（来历里已经有了）；-ery 的例子（见第 90 条）。
    - **没有做**：archive、relaxing 组合列的“词性变化”还是错的（属于第 87 条 ② 那一类，等用户定）；词根列、别的列没动；没有出改动清单（用户上一轮说过不用）。
92. **配套的视频第三十九版（6.3.0）和读音拆分的一条**。
    - 视频：“前缀辨析 / 后缀辨析”那一幕下面多一个绿框“关系”（讲本词缀的一两条），配音多一句“再看它们的关系：…”（只念第一条）。
    - 用户同一条消息：“produce 这种读音拆分，对于 uce、name、home 这种元音 + 辅音 + e 结尾的，就写发音规则就可以了，元辅e结尾”——这是视频读音节划分表的事，总表不涉及：
      视频把音节表关键解释里的“u_e：e 不发音，让 u 读字母音 /juː/”画成标题“元辅e结尾（uce）”，配音念“元辅 e 结尾：…”。音节划分表本身没有改（用户只要三个文件）；name、home 在音节表里查不到单独的条目。
    - 交付照第 88 条：只交总表、维护技能、视频技能三个文件和一张 produce 的整段预览图，不配音不渲染，不出清单；体检并在一条命令里跑，新表和原表各跑一遍、输出逐行比对（除了辨析几项和改的那 8 行，别的要一字不差）。

93. **表里不写“老祖宗、老词根、老音”，写专业的说法**（2026-11 专业术语轮。用户看 produce 的预览图：“老祖宗的 p，英语念成 f（老祖宗 *per-“向前”；同 ped- 和 foot、patr- 和 father）——把老祖宗去掉，换成专业的说法，视频里面也要换”）。
    全表换了 1645 格、1368 行（前缀 460、单词部分 365、词根 284、后缀 127、背景 397、组合 6、音变 6）。换法：
    - **后面跟着构拟形式（带 *）的**：`老祖宗 *per-“向前”` → `印欧语词根 *per-“向前”`。那个形式其实是日耳曼语的（*aznon、*aust-、*fram-、*gaduri-、*gōda-、*hwis-、*kiltham、*lisnojanan、*liston、*writan、*wikō(n)-、*laid-，名单在 `scripts/shuyu.py` 的 PGMC；形式以 -an、-jan、-az、-ō 结尾的也算）写 `日耳曼语 *fram-“向前”`；
      `日耳曼老祖宗 *missjan` → `日耳曼语形式 *missjan`。一共 22 处（learn、good、together、write、week、list、load、miss、raise、furnish、whisper、earn、child、east 这些行）。
    - **讲音的**：`老祖宗的 p，英语念成 f` → `印欧语的 p，英语念成 f`；`同一个老音 dh，拉丁语在词头念成 f` → `印欧语的 dh，拉丁语在词头念成 f`；`老祖宗开头是 gw 两个音连着念` → `印欧语里开头是 gw 两个音连着念`。
    - **同一个老祖宗**：后面没有词根的 → `同源`（`和拉丁语“被…了的”词尾 -tus 同源`、`和英语 night 同源`）；后面有词根的只换名词（`和 two 同一个印欧语词根 *dwo-“二”`）。
    - **老词根**：目录里的句子（un / in / non、sub、trans、fac、dict、pan、bio、vac、thermo、measure 的记法）和紧挨着说到拉丁语、希腊语、梵语的 → `印欧语词根`（`它们出自同一个表示“不”的印欧语词根`）；
      【背景】里没写出形式、看不出是印欧语还是日耳曼语的 → `祖语词根`（“祖语”是语言学里说的祖先语言，两种都算；204 处）——宁可说得宽，不把日耳曼语的词根说成印欧语的。
    - **后面已经说了是哪种语言的**：`老祖宗是印欧语 *skel-“切”` → `源头是印欧语 *skel-“切”`（“印欧语 / PIE / 印欧词根”顺手写全成“印欧语 / 印欧语词根”）；`老祖宗是拉丁语 lancea`、`这一家词的老祖宗是希腊语 platys` → `源头是…`。
    - **没动的**：“这是英语自己的老词”“日耳曼语里的老词”（“老词”是很早就有的词，不是这回事）；“古老词根”；“一家、亲戚、兄弟”（≈ 的记号和【背景】里的口语）；“念成”。只有 pre- / pro- 那段关系里的“一对兄弟”换成了“同源”（第 95 条）。
94. **换法只看紧挨着的话，目录和表一起换**：`scripts/shuyu.py` 的 `pro(文字)` 一条一条规则只看“老祖宗”前后紧挨着的字，不看整格——所以目录里的句子（laili_data.py、part_memo_data.py、sense_suffix.py、cizhui_catalog.py）和表里的句子换出来一样。
    这一轮就是表、目录各跑一遍 `pro`：新表配新脚本、原表配原脚本各跑一遍全套体检，输出逐行比，只有 `cizhui.py --groups` 里 before 那一组的句子不同。
    以后写新内容直接用新说法；`python3 scripts/shuyu.py <表>` 查表里还有没有（应为 0，收尾时跑），`--write <新表>` 把漏网的换掉（写完读回来逐格比），`--files a.py b.md` 换目录、说明。新碰到的日耳曼语形式加进 PGMC。
95. **pre- / pro- / fore- 的关系重写**（用户：“produce 里面最后的关系好像写的有点问题，把 fore 也说成出自同一个老词根了”）。
    查 etymonline：fore 条“from Proto-Germanic *fura … from PIE *prae-, extended form of root *per- (1) "forward"”，*per- 条把拉丁语 pro、prae 和古英语 fore 列在一起——三个确实同源，原来的话没有错；毛病在“老词根”听着像拉丁语的词根，读成了“fore- 也是拉丁语来的”，和辨析里“fore- 是英语自己的”打架。现在（62 行）：
    `pre- 和 pro- 不是一个变出另一个（不像 duc、duct 那样是动词原形和过去分词），它们是拉丁语里两个同源的介词（prae“在前面”、pro“向前”，都来自印欧语词根 *per-“向前”）；fore- 和 pre-、pro- 同源，但它是英语本族的前缀，不是从拉丁语来的（古英语 fore 也来自 *per-，印欧语的 p 到英语这一支变成 f，这叫格林定律）`
    - 讲“同源”要说清**各是哪种语言自己的、不是互相借来的**；“老祖宗、兄弟”这类比方容易让人把“同一个来源”听成“同一种语言”。用户说“写错了”的地方先查出处：事实没错就不改事实，改说法，并且在回复里说明查到了什么。
    - 第二条条首还是“fore- 和 pre-、pro-”：视频看条首认这一条讲谁，pre-、pro-、fore- 三个词缀的页面都要画这一条。括号里不放分号。
    - “格林定律”只在这一处写了（括号里，不念）；p 对 f、t 对 th、d 对 t、c 对 h、g 对 k 这些“音变”行没有加，用户要再加（改 laili_data.py、part_memo_data.py 里的句子，再 `laili.py`、`part_memo.py` 写回）。
96. **配套的视频第四十版（6.4.0）**：这一轮用户主要提的是视频的画面（“视频页面比较花”），总表的记号（“身份：”“。辨析：”“；关系：”“记：”“音变：”“字母变化：”）一个没变——第三十九版照样读得了这张表，第四十版也读得了上一版的表。和写表有关的三处：
    - 前缀、后缀的“身份”（开头的介绍）现在画在那一部分的卡片上：蓝框第一行是介绍的第一句和来历（“向前”，来自拉丁语介词 pro），下面小字是介绍里第一个分号后面的话（也表示“预先”；这里是“向前、到前面来”）——**介绍第一句要短、后面的补充用分号隔开**（第 83 条）更要守，第一句太长会折成两行。
    - “辨析”那一幕只画辨析和关系，字不小于 22 号；一组条目多、放不下时只画讲到的几条（本词缀那一条和这一组里排在前面的两条），右上角注“另有 N 条，见总表”——**目录里一组辨析的先后**决定画哪几条，最常拿来比的放前面。
    - 词根的另一种写法“字母变化：duc → duce，…，英语加不发音的 e”挪到“身份和分工”那一幕画和讲（“从 d u c 到 duce：英语加不发音的 e。”）；念的还是“字母变化”里最后一个逗号后面的那半句。
    - 交付照第 88 条：总表、维护技能、视频技能三个文件加一张 produce 整段预览图，不配音不渲染，不出清单。
97. **术语简化（2026-11 视频界面轮）**：用户：“把原始印欧语词根简化一下，这个有点长”。表里一律写“印欧语 / 日耳曼语”：`印欧语词根 *per-“向前”`、`印欧语的 p，英语念成 f`、`日耳曼语 *fram-“向前”`（第 93 条的“原始印欧语 / 原始日耳曼语”到这一轮为止）；“祖语词根”“源头”“同源”照旧。`scripts/yuanyin.py` 的 `simplify` 换、查；shuyu.py 换“老祖宗”时直接写简化的说法。“PIE”（294 格，多在音变列）这一轮没动。
98. **音变要讲原因（2026-11 视频界面轮）**：用户：“音标 p--f 要解释一下为什么印欧语的 p 英语要读成 f……先说发生了什么音变：p--f；再说明原因”。记法后面的“音变：谁对谁：一句话（…）”是格林定律管的（p、t、k → f、th、h；b、d、g → p、t、k；bh、dh、gh → b、d、g），末尾接
    `；原因：英语属于日耳曼语，日耳曼语两千多年前把 p、t、k 成批地念成了 f、th、h，这叫格林定律；拉丁语没有这样变`（一句里有几类就都写；比的是希腊语那一支的写“希腊语没有这样变”）。
    哪几对算、怎么写都在 `yuanyin.py`（PAIR、CAT）；目录 laili_data.py、part_memo_data.py 里的句子已经带上，新写音变用 `yuanyin.add()` 生成，不手写。经法语磨掉的、拉丁语 v 本来念 w 的、sub- / super-、right、light“轻的”、warm、eye 不加（句子本身在讲怎么变，或者不是一条定律讲得清的）。
    原因里不能有句号（视频按“。辨析：”切这一行）。视频第四十一版把它画成记框里单独一行“原因”、配音单独一句（“为什么英语念成 f 呢？……”）。

## 2026-11 音变原因轮定下的

99. **音变的原因要讲清“为什么能变、为什么这样变”，再举例子**（用户：“为什么要这样变最好也说一下，p-f 为什么可以，是发音相似还是什么原因，最好能说明白，可以网上进行搜索；然后再举一些例子就更好”）。第 98 条的原因改成四块，块和块之间用“；”，后三块开头有记号：
    `；原因：英语属于日耳曼语，日耳曼语两千多年前把 p、t、k 成批地念成了 f、th、h，这叫格林定律，拉丁语没有这样变；发音：念 p，两片嘴唇先闭紧、再一下子放开，念 f，下嘴唇轻贴上牙、不闭紧，气从缝里擦出来，两个音都用嘴唇，只差闭不闭紧，所以 p 容易念成 f；起因：没有定论，一种说法是重音方式变了，说话时气流压力加大，p、t、k 先带出一股气，再变成摩擦；例子：拉丁语 piscis 和 fish、plenus 和 full、paucus 和 few`
    · 总说：“拉丁语没有这样变”前面的分号改成逗号；第三类再接“，它在词头把 bh、dh、gh 念成了 f、f、h”（希腊语：“它把 bh、dh、gh 念成了 ph、th、kh”），学生看得出拉丁语的 f 是怎么来的。
    · 发音：p→f、t→th、k→h“只差闭不闭紧 / 顶不顶住”（堵住再放开 → 留缝擦出来，发音部位没变）；d→t、g→k“只差声带振不振”；dh→d、bh→b“只差带不带一股气”；k→h 加“像汉语拼音的 h”。两对的接“，另外 d 和 t 舌尖动作一样，只差声带振不振”。“两个音”开头的是结论。
    · 起因：查过 Wikipedia“Grimm's law”（发生在公元前一千年里的原始日耳曼语、细节不清楚、“拉链”还是“推链”有争议、很可能先经过送气）和 Stenbrenden 的论文（重音变成力重音、声门下气压升高，引出送气、摩擦和清化）。
      写“没有定论，一种说法是……”：第一类写重音那一说；第二、三类写“一个变走、下一个补上”那一说，并写“这几步谁先谁后学者还有争议”。
    · 例子：每类一个池子（yuanyin.py 的 EX），都是教科书里的标准同源词，逐个对过 etymonline（fumus 和 dust 同出 *dheu-、fingere 和 dough 同出 *dheigh-……）；一对挑 3 个、两对各挑 2 个；先拉丁语（比的是希腊语那一支的先希腊语），不够从另一种语言补，标出语言。
      不重复这一句里已经出现的词和记法的关联词（pro ≈ for 那一行不再举 foot、father，举 fish、full、few）。
    · 原因里不能有句号；“发音”这一块里只用逗号。
100. **表和目录一字不差**：挑例子时避开的只看“记：X ≈ Y”的 Y 和音变那一句（不看整格），所以 `yuanyin.add(句子, Y)` 在表里、在目录里（laili_data.py 的 MEMO 第 3 项、part_memo_data.py 的 SHIFT 的键）生成的一样。
    `python3 scripts/yuanyin.py --catalog` 照现在的写法重写目录；`yuanyin.py <表>` 多查一项“原因不是现在的写法”（应为 0）。这一轮表里重写了 318 处原因（前缀 198 格、词根 120 格），目录 30 句（laili_data.py 5、part_memo_data.py 25）。
101. **辨析里说来源的开头写简短**（用户：“是拉丁语来的，说时间、顺序上的“先”……简化成：拉丁语，表示时间、顺序上的“先”……”）：pre- / pro- / fore- 那一组写成
    `pre- 拉丁语，表示时间、顺序上的“先”……；pro- 也是拉丁语，多表示方向上的“向前”……；fore- 英语自己的，接日常的本族词……`（cizhui_catalog.py 的 before，表里前缀列 62 格；pro-、fore- 跟着 pre- 一起改，一组里写法一致）。
    别的 19 组还是“X 是拉丁语来的”“是英语自己的”，用户没说要改，先不动（回复里问过）。视频画面照表写，配音补上“来自 / 是”。
102. **配套的视频第四十二版（6.6.0）**：原因画成单独一幕“为什么 p 会变成 f？”（格林定律三对、两块会动的嘴的剖面图、黄条结论、起因、例子），卡片的记框只留“音变 p → f”；
    身份框写“来自拉丁语介词 pro；表示“向前”和“预先””（视频代码把介绍里的“也表示“预先””并上去，表里不用改），“这里是…”单独一行醒目。
    第四十一版读这张表会把整段原因（带“；发音：…；起因：…；例子：…”）挤进记框的“原因”一行，要用第四十二版；第四十二版读上一版的表照旧（没有这一幕）。

## 2026-11 辨析精简演示轮定下的

用户看第四十二版 produce 的预览图：“这里的句子要简化一下，有很多口语话的词可以去掉，还有一些不是很必要的词也可以去掉，让句子简化一下，减少视频时间”“关系部分也是一样，把不必要的词去掉，要简化，但不能把关键信息去掉了”
“我希望这些能有演示，就像后面的组合一样，要不然干讲这个学生不一定理解”“重点是要说明是加动词还是加名词，这个是关键点，就是加动词的效果和加名词的效果要体现出来，并加以说明”
“这叫格林定律 去掉，学生听了也不一定记得住，加重了负担”“需要，我的意思就是要把总表里面有同样问题的都进行这样的处理”。

103. **辨析写精简**（20 组全改，cizhui_catalog.py 的 GROUP；表里前缀、后缀两列 4274 格）：
    - 来源紧跟在词缀后面，只写语言：`pre- 拉丁语，…`、`fore- 英语本族，…`、`-ism 希腊语，…`、`-ous 拉丁语，经法语进来，…`、`inter- 拉丁语：…`（不写“是拉丁语来的”“是英语自己的”“也是”）；原来没写来源的条不硬补。
    - 去掉口语、可有可无的字：接在、加在、日常的、那一、正好、别弄混、只差一个字母、基本都；**表示准确程度的“多、常、多半、也许”留着**（pro- 也有时间上的“预先”：provide、program，所以“多表示方向上的“向前””的“多”不能去）。
    - 用法写成“名词、形容词前是“…”／动词词根前是“…”／名词后是“…”／形容词后是“…””，加在什么词上要写出来。
104. **例词紧跟在它说明的那个用法后面，第一个是演示词**：`名词、形容词前是“…之前的”（preschool、prehistoric），动词词根前是“预先做”（predict、prepare）`。
    - 演示词要在总表里，组合列第一行是等式（`pre（在…之前）+ school（学校）=“上学以前的”`），最好是“词缀 + 学生认识的词”；视频取这一行画“图 + 图 = 画”、念“比如 preschool，上学以前的”。
    - 体检 `cizhui.py --check` 的 demo_bad（应为 0）；短语（more beautiful）、本来没有等式的（hard）记在目录的 DEMO_SKIP，视频这个用法不画演示。fore- 原来的 foresee 总表里没有，去掉了。
105. **关系写精简**（10 组，REL）：去掉比方和重复的话（“不像 duc、duct 那样是动词原形和过去分词”“它们是”“这一支”），**不写“这叫格林定律”**；关键的事实（不是谁变出谁、是不是同源、哪种语言的、谁加了什么变成谁）一条不少，括号里只留原词、词根。
    “往上各是同一个老后缀”“是一家”这类口语说法换成“同源”或去掉。音变的原因（第 99 条）里的“这叫格林定律”这一轮没动（用户说的是关系那一段）。
106. **配套的视频第四十三版（6.7.0）**：辨析那一幕每个用法一个演示（牌子“加在名词、形容词前 / 加在动词词根前”），分段标题不画线。上一版的句子留在 cizhui_catalog.py 的 PREV_CORE / PREV_REL，cizhui.py 靠它认出要换的行。
    交付照第 88 条：总表、维护技能、视频技能和 produce 的整段预览图，不配音不渲染，不出清单；体检（cizhui、shenfen_check、laili、lizi、part_memo、yuanyin、shuyu、tonggen_check）都是 0。

## 2026-11 词根形态轮定下的

起因：用户看第四十三版 produce 的视频，“目前词根的视频页面有点乱，我希望：先写词根和含义 duc-；形态：原形 duc，来自拉丁语原形 ducere，然后去掉尾部 ere，这里要有去掉尾部的演示，举出例词；过去式 dux，来自拉丁语过去式 duxi，写出怎么变化的，并做演示，举出例词；过去分词 duct，同上”
“一个词根可能有其他形态，这个时候就把不同形态写出来，并写出演变”“如果是其他词性，你再想想看怎么排版和讲解比较好”“视频里面的内容来自总词库，所以要先把总词库按上面的更新一下”。
看了方案（八段并成四段）：“目前就是这一格乱导致的，就按你刚才的那种写法改”。

107. **词根那一格四段：词根 → 形态 → 这个词 → 记**。`标签：词根 X-“意思”（来源）。形态：…。这个词：…；记：…`（一行，不换行）。原来的“词根 X 的另一种写法（同一个词根）”“字母变化：”“动词变化：…；规律：…”“身份：…。分工：…”“意思：”都不再写（第 61、65、67、71、75 条讲的词根写法到这一轮为止；它们的内容都进了形态和这个词）。
     第 61 条“几种写法当一个词根讲”照旧：开头就写词根 duc-，形态讲清每种写法从哪来、怎么变。
108. **形态一个一句**：`名字 写法：来源和变化；英语里的用法（例词）；…`。来源和变化先说原词（“来自拉丁语原形 ducere“领””），再说怎么变（“duc 加 s，c 和 s 合写成 x”），最后“去掉词尾 -ere / 再去掉词尾 -i / 再去掉前缀 di 和词尾 -us”（视频照它演示去掉词尾）。英语里的用法是原来“分工”那句话切开归过来的，例词还是总表里的词。
109. **拉丁语动词三句：原形、过去式、过去分词**。过去式的样子是过去式去掉词尾 -i（duxi → dux、feci → fec、steti → stet）；拉丁语的过去式英语里几乎不留词，57 族都写“英语里几乎不用”，不硬凑例词（写法和原形一样的 vid、mov、vert、ven、volv、pand、prehend、fend 写“写法和原形一样，英语里的词都算原形的”）；
     只有被动样子的（grad、mir、mens、peri）写“过去式：这个动词只有被动的样子，没有单独的过去式”。只接在前缀后面的（stingu、fend、peri、friger）三个样子都去掉前缀。规律里两样都讲的（fer：“过去式、过去分词都是从别的动词借来的”）两句都写；都没讲的（“relate、translate 用的就是这个 lat”）归过去分词的用法。
110. **别的词性**（46 族，xingtai_data.NV）：名词“原形 / 所有格”——拉丁语名词接词尾才露出词根（pes“脚”→ 所有格 pedis“脚的”去掉 -is → ped；caput → capitis → capit；merx 是 merc 加 s，和 dux 一样 c 和 s 合写成 x），原形英语里不单用的写“英语里不单用”；
     形容词“原级 / 比较级 / 最高级”（magnus → magn、maior → maj、maximus → maxim）；希腊语“原形 / 名词”（graphein → graph、gramma → gram；dynasthai → dyna、dynamis → dynam）；法语、英语本族照实写（ward / 经中部法语 gard，hap / 双写 happ，lief / 动词 lieve）。
111. **这个词**：本行用哪个形态（“用原形 duc”“用过去分词 duct”“用所有格 ped”）；写法和那个形态不一样的写“，写成 duce：”再接原来“字母变化”那一段（没有的写身份代号的说明：经法语传进英语，变了形……）；原来行里别的话（“；这里是“扛、承载””“准确说是 magn 去掉 n 的 mag“大””“etymonline 说…”“和英语自己的 bear…同出…”）用“；”接在后面，一字不丢。
112. **工具和这一轮没做的**：`scripts/xingtai.py`（`--write` 只动词根列 459 格，再跑要改的格 0）、`--check` 四项 0；视频第四十四版（6.8.0）读这种写法（wordfilm.js 的 `xingtaiOf`，两边一起改）。
     没做的：① 表里只出现一种写法、没有立词根族的拉丁语动词词根（port、mit、ject、tract、scrib……）还没有形态——用户要补时，先在 shenfen_data.FAM 立族（写法、身份、分工），在 dongbian_data.VERB 写三个样子，再 --write；② 形态里英语用法的句子是原来分工的原话，没有逐句改写；③ 46 族的原词（所有格、比较级、希腊语名词）是照语法写的，没有逐个再查词典。

## 2026-11 词根形态补齐轮定下的

起因：上一轮只给 103 个词根族排了形态。用户问了“只出现一种写法的拉丁语动词词根要不要补”以后说：“第二种也补上”；又说：“顺带再检查一下后缀，检查一下后缀现在是不是也按照前缀的样式来进行写的”。

113. **补齐的范围**：词根列里还没写形态、讲的是拉丁语动词的词根行都补上（新立 174 族，老族 fer / par / spir / put 补了写法，共 392 格）；几种写法却没立过族的也在里面（mit / miss / mise / mess、cess / ceed、sid / side / sess、tang / tact / tag、vinc / vict）。
     **不补的**：过去分词词干行（recognit-、informat-，第 54、55 条另有写法，视频靠它做“构词”卡）；行里写明来自名词、形容词的（rot ← rota、son ← sonus、loc ← locus、legal 的 leg ← lex、annotate 的 not ← nota、profound 的 found ← fundus）；只剩一两个字母的（add 的 -d、debt 的 -b-）；希腊语的（-ste-、stat-）；行里只讲法语、意大利语来路的（tour、cuit、cover 的 ver、venge、sort）；动词本身拿不准、没有常用三个样子的（-minere、decere、licere、solere、angere、excellere、lacere）。
114. **写法和上一轮一样**（第 107–112 条），数据在 `scripts/xingtai_verb.py`：FAM2、VERB2 和 shenfen_data.FAM、dongbian_data.VERB 同一个样子，xingtai.py 读的时候合在一起；JOIN 是老族补的写法；GLOSS 是词根后面引号里的意思；NOT 是标签像、其实不是这一族的行；AS 是这个词实际用的写法和标签不一样的（absolute 用 solute，fundamental 用 funda）；ME 是手写“这个词”那一段的行。
     写法代号多了 E（原形加不发音的 e）、PE（过去分词加不发音的 e），也可以写 (代号, 一句话)，这句话就是“这个词”里“写成 X：”后面的说明。词根写英语里常见的写法（tract、ject、mit），和上一轮 gest、mens 一样；同一个动词在别的组再立族，词根和三个样子照第一族（fac、cap、vert、dic、fer、ag、sed、scrib、ten、ced）。
115. **老写法的行怎么拆进“这个词”**：开头的意思（“搬运”“= rod“啃””“拉丁语 sequi“跟随””）和这一族的意思不一样的，写“这里是“…””；括号里只说“拉丁语 portare”“trahere 的“被…了的”形式 tractus”的半句去掉（形态里有了），别的话一字不丢、照原来的先后用“；”接上；原话已经讲了怎么变的，“写成 X：”后面不再重复数据里的说明。
     词根行不写“→”链（第 65 条）：vulnerable、lavish、excerpt 三行改成了“造出了”“到古法语成了”。
116. **三类特殊动词**：只有被动样子的（sequi、pati、nasci、fateri、opinari、testari、luctari、solari、vereri、oriri、reri、fungi、labi、moliri、tueri、imitari）照旧写“这个动词只有被动的样子，没有单独的过去式”；
     **没有过去分词的**（timere、tremere、horrere、stupere、splendere、tumere、rigere、arere、silere、liquere、lucere、patere、valere、pārēre“出现”）写“过去分词：这个动词没有过去分词”，视频画成虚线行；
     只接在前缀后面、单用没有这几个样子的，写一个真实的带前缀的动词（discutere、polluere、invadere、incendere、consulere、dividere），说明里写“只接在前缀后面用”。三个样子用 Whitaker's Words 逐个核过，只有 sorbere 词典给的是罕见的 sorbitus，表里写 absorption 里看得见的 sorptus。
117. **词缀开头的介绍先写意思**：后缀行（和 87 行先写作用的前缀行）“身份：”后面第一段改成“意思”（来历括号）；作用：`-er：身份：“做…的人或东西”（英语本来就有的后缀…）；一般加在动词后面`，视频身份框就和前缀一样是“来自…；表示“…””。只动第一段，记、辨析、关系一字不动。
     **不动的**：开头是“= -ize”这种别名（视频靠它认）、开头是“这里…”或里面有“不是”的、括号里不是来历的、来历括号不在第一段末尾的、引号里的意思不止一处的（-ing 名词、形容词两用）、没有引号里的意思的；改了以后 cizhui.py 挂的辨析会变的 4 个词（bunny、calendar、discovery、peasant）照原样（houzhui.py 的 KEEP）。
118. **工具**：xingtai.py 加了 plain_fam（老写法的行属于哪一族）、parse_plain / me_plain / line_for_plain（拆进四段）、refresh（数据改了重排来源、形态两段）；`--check` 的 xt_diff 真的查了（以前只列了名字）。新文件 houzhui.py：试算、`--pre`、`--write`。视频第四十五版（6.8.1）代码没改：没有过去分词的那一行走原来“没有单独过去式”的虚线画法，后缀身份框照新写法自动变。
119. **视频要做的短语、合成词可以补进总表**（2026-11 视频补词轮）：总表原来只收单词，短语写在中心词「含义」的 phr. 行里；用户点名要做视频、表里又没有的（alarm clock、keep track of），在表的末尾另起一批补成独立的行：
     类型写 ③ 合成词，拆分照词与词的先后写“A + B（+ C）”，单词部分每个词一行（见 X）；能单独用的意思照常写词性（动词短语写 v.，视频里讲“它说的是动作，所以是动词”）；
     合成规律、写法只用 hecheng_catalog.py 里有的条目，对不上的（动词 + 介词、动词 + 名词 + 介词）不写这两行，用法写在【提醒】里；组号挂在最主要的那个词的词族上。
     往表里加行不用 openpyxl 整表重存（会变成行内字符串、文件大三成），直接追加 sheet1.xml 的行和共享字符串，样式照同类词的一行，筛选范围、定义名跟着改末行号。
120. **考点列**（2026-11 考点轮；已被第 121 条取代）：第 18 列「考点」，scripts/kaodian.py 整列生成（`--write`），一格几行，每行“【标签】内容”，标签只用 变形、词性转换、短语、用法、易混 五种，没有内容的行不写：
     - 变形：词性写在前面（n. / v. / adj. / adv.），几个词性用“ / ”隔开，一个词性里几项用“；”；拼写规则写在括号里（去 e 加 d、双写 p 加 ed、y 变 i 加 es、f 变 v 加 es、不规则、单复数同形）；不可数名词写“不可数，没有复数”（常考词表 UNCOUNT + 含义、辨析里写了“不可数”的）；
       本身就是变形的词（went、written、better）写“go 的过去式：…”；名词、动词不是第一个词性时，只有特殊的复数、常用或不规则的动词变化才写。形容词：不规则的、单音节和 -y / -ow / -le / -er 结尾的双音节加 er / est，多音节、常见、能分程度的写 more / most，national、wooden 这类不写。
     - 词性转换：同一组号里由本词派生的（往下两层）、本词由它派生的（speaker ← speak）、和本词同前缀同词根的（produce / product）以及它们派生的；变形词、合成词、≈ / ← 的不算；wordfreq 词频 3.2 以上；词性变了的排前面，最多 4 个，写“词性 词 短意思”。
     - 短语：本词含义的 phr. 行，再补别的词 phr. 行里带着本词、每个词都常见的，最多 3 个。用法：辨析列和组合列【提醒】【语法】里讲搭配、可数、接什么、不说什么的句子，最多 2 句、每句 80 字以内。易混：辨析列【同义词】行（最多 3 个词）和“≠”。
     - 这一列是程序写的，人工改过的格以后整列重写会被盖掉：要改就改 kaodian.py 的规则（或在视频 prefs 的 kaodian 里手写），或者重写以后再把手改的格贴回去。视频第四十八版（6.11）读它。
121. **考点列照上海考纲写**（2026-11 考纲考点轮，取代第 120 条）：用户：“考点要有依据，不是说我上面提到的都要写进去，就是你看上海初中英语，上面对应的这个词常见的考点是什么，把这个词常见的考点，难点，易错点写好了就行了，不是说啥都要写进去，那样内容太多了”。
     标签还是 变形、词性转换、短语、用法、易混 五种（视频认这五种），一格多半一两行；没有考点的空着。依据 S1–S4 见 SKILL.md“考点列”一节，kaodian.py 每一行都算出出处（--show 打印），不写进表（用户：“考点依据不用加了”）。
     - **写不写**：考纲里的词才写；考纲外的词只写两种一行的：由考纲词加前后缀变来、常用（wordfreq ≥ 4）或资料、真题点名的“true → truly（去 e 加 ly，易错）”“strange → stranger（名词“陌生人”，也是 strange 的比较级）”，
       和考纲词的不规则变化“go 的过去式（过去分词 gone）”“tooth 的复数（不规则）”。heat → heating、publish → publishing 这类不常考的不写。
     - **变形**：只写难点——考纲括号里标的（不规则动词、复数、比较级）；没标但不规则的（spend、sing、rise、forgive、mistake）；双写（stopped、beginning）、y 变 i（studied、flies）、ie 变 y（dying）；
       名词加 es（boxes）、o 结尾（heroes / pianos 只加 s）、f 变 v（halves）、man 变 men、单复数同形、只用复数、常考不可数（advice、news… 带量词），可数不可数两用的写清楚（paper、glass、time、work 不写，易混里讲）；
       形容词不规则、双写（bigger）、y 变 i（happier）；代词表（I：宾格 me / 物主代词 my、mine / 反身代词 myself；its 不是 it's）、数词表（ninth 去 e、fifth ve 变 f、twenties）。规则的加 s、加 ed、加 er 和 more / most 不写。
       词性以考纲为准：produce 考纲里只有 v.，不讲“农产品”。
     - **词性转换**：考纲里也有的同根词，最多 3 个，资料、真题里有的排前面，再是词性变了的。关系取总表“拆分”“单词部分”（见 X）、② 变体关联（≈ / ←，只认 SH_CONV 和 VAR_OK 里的）、同前缀同词根（produce / product）、同一个母词的 -ent / -ence；
       否定前缀只认意思是“不…”的（unhealthy；discover 不算）；后缀要词性变了、意思接得上（race / racial、idea / ideal 不算），-er / -or 要是“人”；加 s、t、th 的（news、gift）不算；BAD_PAIRS 是逐个看过不算的。
     - **短语**：考纲词组表里带这个词的（-ed 形式、复数也算：be connected to、at weekends），最多 3 个，PHR_TOP 里常考的排前面；“at first/last”这种按这一行的词挑一半（PHR_ALT）；用法、易混里讲了的不再列。
     - **用法**：kaodian_data.USAGE（动名词、不定式、不带 to、短暂动词、花费、系动词、反意疑问句、句型转换的同义替换、冠词 an hour、play chess / play the piano……），每个词最多 2 条。
     - **易混**：kaodian_data.CONFUSE（already / yet、remember / remind、-ed / -ing……），每组的词都在考纲里，最多 2 条；写成“A / B（区别）”，括号里不用“；”。
     - 这一列是程序写的，人工改的格整列重写会被盖掉：要改就改 kaodian_data.py（材料）或 kaodian.py（规则）。视频第四十九版（6.12）读它。

122. **练习题五列**（2026-11 练习题轮）：用户：“现在先把总词库更新一下，增加5个题目列，对应五个题目，然后你再把题目生成出来；然后维护skill和视频生成skill进行同步更新”。
    第 19–23 列「题目1」–「题目5」，一格一道题（写法见 SKILL.md“练习题五列”），原稿 scripts/lianxi_data.py，lianxi.py --write 写、--check 体检。
    第 1 题听力（念含本词的短句，问说了什么）；其余考考点和视频讲过的区别，答案由本词决定、不总是本词——用户：“答案不一定是这个词，但是跟这个有关系，或者这个能决定答案”；答案就是本词原形的最多 1 道。
    题型照上海中考，不重复；选择题正确答案的位置由 lianxi.py 按单词和题号排（A–D 各占四分之一左右）。现在写好的是单元表 40 个词。

123. **答案列**（2026-11 练习答案轮）：用户：“题目答案放在总表里面，加一个答案列；并配上讲解；答案放在视频末尾，放在总结后”。
    第 24 列「答案」，一格五道，每道两行：“【1】D（牛奶和鸡蛋）”“讲解：…”（写法见 SKILL.md）；「题目1」–「题目5」只写题，不再写“答案：”“解析：”。
    lianxi.py --write 整列写（原稿 lianxi_data.py 里 why 就是讲解），--check 查答案列和题目对得上。视频第五十二版：练习只出题，答案放到总结后面。

## 第 124 条（2026-11 读音现象轮）：加「读音现象」列

用户：“总表里面还差一个数据，就是一些发音比较特殊的现象没有解释，比如：speaker，这里的 p 读成了 b，但是视频没有讲出来，很多学生可能不知道，不光要讲出这个现象，还要说为什么会这样。special 这里的 ci 为什么不读 s，education 这里的 du，exactly 的 ex 等等，你先查看一下总表，看看有多少单词存在这样的现象，然后再在总表增加一列：读音现象，专门用来说明这些现象，并做解释的；视频里面就放在读音拆分这部分进行讲解”。
- 第 25 列「读音现象」，`scripts/duyin.py --write` 整列写；一行一个现象“【类别】字母：现象。为什么：原因。（例词）”，按字母在词里的先后排。
- 十二类规则和每类的说法见 SKILL.md“读音现象列”一节；9293 个词里 2364 个有。
- 视频技能第六十三版（6.26）读这一列：读音拆分（和关键解释）后面一个现象一幕；关键解释里讲同一处的（produce 的 “d u 读 /dʒu/”）只留读音现象那一条。



## 第 125 条（2026-11 本族词轮）

英语本族的部分写专业说法：英语本族词、英语本族前缀、英语本族后缀、英语本族词根（英语词汇学的“本族语词 native words”，和“外来语词 borrowed words”相对）。不写“英语本来就有”“英语自己的”。“英语自己拼出来、自己拿 X 加…”写“英语里…”。脚本：shuyu.py 的 benzu()。用户原话：“speak，-er 不要说英语本来就有，换成英语本土词，英语本土后缀，英语本土前缀，英语本土词根；要用更专业的”。


## 第 126 条　详细考点、练习 7 道（2026-11，第七十五版）

用户：“最新版生成的视频把原先的考点部分给去掉了……我希望能在做精简版的视频时，也要把考点给加上去”“看看总词库……考点这一列的数据，我希望能把这个数据补全，补详细，对应的是上海初中英语的考点”“后面的练习题还是用原来的逻辑，但是要增加对考点的考察，由原来的5道题增加到7道题”。

1. 「考点」写详细，取代第 121 条“只写常考的一两行”（第 121 条的依据 S1–S4、考纲材料照旧用）。单元表的词手写（kaodian_hand.py），考纲词照考纲词汇表、词组表补全五样，考纲外的词按规则写变形、词性转换、短语。规则的变形也写，括号里注明拼写变化和不规则；不可数名词写“不可数”。条数：变形每个词性一组（最多 4 组），词性转换 ≤ 4，短语 ≤ 4，用法 ≤ 3，易混 ≤ 2（和视频 KD_MAX 一样）。
2. 「题目6」「题目7」插在「题目5」后面（第 24、25 列），「答案」第 26 列写七道，「读音现象」第 27 列。第 6、7 题专门考考点（“考点：”必写），考前 5 道没考到的点；前 5 道的出法（第 122 条）不变。
3. 视频技能 6.31.0（第七十五版）配合：精简版固定讲考点、一页放不下分两页；练习、答案各 7 幕；总结整页直接出来。


## 第 127 条（2026-11 初中含义轮，第七十六版）
1. 加第 28 列「初中含义」（chuzhong.py 写）：视频讲的意思照它，初中常用的一两个意思，相近的只留一个（protect：v. 保护，不再讲“防护”“保护本国产业”）。依据上海市教育考试院 2020 年《初中英语课程终结性评价指南》词汇表的中文；考纲外的词从「含义」取前两个意思；单元表 40 个词手写，和视频画面设置里每幅画的意思一字不差。
2. 「含义」列照旧完整（组合列、演变、辨析都照它写），不删。
3. 「考点」【词性转换】写成“单词 词性中文”：protection n.保护（用户：“写单词的时候格式这样：protection n.保护；单词，词性，中文含义”），箭头写法（true → truly）不变。
4. 视频配音的停顿和“一个人念”是视频技能 6.32 的事（停顿照标点分长短；中英切换很快的一句用老师本人的声音一口气念），总表不用为它改写法；要停得长的地方用句号、分号、省略号。

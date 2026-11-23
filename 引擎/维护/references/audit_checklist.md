# 核对清单（scripts/audit.py、scripts/video_check.py 的各项怎么读）

跑法：`python3 scripts/audit.py <xlsx>`，再跑 `python3 scripts/audit_split_labels.py <xlsx>` 和 `python3 scripts/video_check.py <xlsx>`。
下面是三列分工版的“正常基线”：数字和这里一样就说明没有引入新问题；变多了就逐条看新增的。

## audit.py

| 项 | 查什么 | 正常基线 / 常见误报 |
|---|---|---|
| [1] | 重复的词 | 6 个同形异义词：bore、lie、rose、race、scale、mine（正常） |
| [2a] | 同一组号被拆散 | 0 |
| [2b] | 【背景】不在组的第一行 | 0 |
| [2c] | 第一行没写【背景】的组 | 0（2026-11 补齐了原来写“—”的 105 组） |
| [3] | 批次内序号不连号 | 0 |
| [4] | 单词/含义/类型/拆分/解释/组合 为空 | 全 0（含义是 2026-11 新加的 F 列） |
| [5] | 拆分部分在解释里找不到对应行 | 290（2026-11 直接母词后；原 298），几乎都是写法习惯（双写辅音、括号写法、合并标签、带 ← ≈ 的拆分）；看 audit_split_labels.py 的过滤结果（161）更准 |
| [6] | “见 X”指向表外的词 | 14，都是参见或“××年见于…”，正常 |
| [7] | 括号/引号不配对 | 1（emoji 里引了 :-)，正常） |
| [8] | 解释标签用半角冒号 | 0 |
| [9] | T 列“第 N 行 某词”指错 | 0 |
| [10] | “由词根 X 变来”和 U 列本组词根不一致 | 0 |
| [11] | M 列不以【构词逻辑】开头 | 0 |
| [12] | 以 = 开头的文字格 | 0 |
| [13] | 「整表核对记录」超链接指错 | 0（其他索引表已删） |

另外两种手工扫描（audit.py 不查，需要时自己写一小段）：
- 丢字 / 乱码：`：）`、`（）`、`“”`、连续标点、`�`。
- 拆分结构和解释结构不一致：拆分是 A + B + C，解释却把 B、C 并成一行（或反过来）；拆分没用表里现成的母词，而解释是按母词写的。

## video_check.py（视频读表的体检）

| 项 | 正常基线 |
|---|---|
| h_has_combo（各部分解释里还有组合内容） | 0 |
| logic_in_parts、logic_no_eq、no_jinyi、split_plus_in_paren | 0 |
| mean_no_pos、mean_dup_pos、mean_empty、mean_has_example、mean_ex_bad、mean_ex_unmatched（含义：行首写词性、同词性一行、不带例子；例句：“意思：例子”、对得上） | 0（2026-11 例句分列轮起；明细用 `python3 meaning.py <xlsx>` 看） |
| part_no_line | 0（另一种拼法 instal 这类只写一行同名标签的不算） |
| suf_no_src | 0 |
| suf_no_here、here_no_label | 0（-it-、-at- 这类夹在中间的成分不算） |
| suf_src_text_only | 0（2026-11 全部挪进括号；新出现的跑 src_paren.py） |
| here_semicolon、here_no_affix、here_awkward | 0 |
| rule_ex_circled、rule_mark_missing、rule_unmarked、evo_no_step | 0 |
| fmt_old_pos、fmt_old_rule、fmt_not_canonical（组合列是不是清爽格式） | 0（不为 0 就跑 columns.py reformat） |

修的时候用 `scripts/fixlib.py`，每处自动写 T 列并记进「整表核对记录」；只记录不改的“特殊情况”用 `b.special(...)`；整类批量修改记一条汇总（`b.fixed_other(...)`）。

## rule_check.py（用词规律体检）

| 类 | 正常基线（都已逐条核对过，保留） |
|---|---|
| A 做…的人的词，套了“表示动作的词…” | 1（stutter：-er 在这里是“一再地”，stutter 本来就是动词） |
| B 形容词/副词，套了“表示动作的词…”；C 性质名词套了“表示动作的词…”；D 本来是名词套了“动作直接当名词用” | 0 |
| E 本来就是动词，套了“东西、性质直接当动词用” | 0（mandate 的词性变化 2026-11 改成“动词 → 名词”，不再误报） |
| F 不是名词，套了“名词当形容词用” | 12（assistant、narrative、merchant……名词义在前，核对过） |
| G 取消了的空洞说法（用进某一行 / 英美不一样 / 东西变了）还在表里（2026-11 用词规律轮起） | 0（原表 863） |
| I/J 复数没写标记；规律认不出 | 0 |
| K 规律说“表示动作的词”，本词原来的意思像个东西 | 15（dress“穿衣”、drive“开车”、pick-up……其实是动作，核对过；2026-11 用词规律轮以前是 16） |
| L 做…的人的词，后来指机器，还没标规律 | 1（flier“投机”，误报） |

## 组合列格式的回归测试（改过组合列或脚本以后跑）

- `columns.py split <表> <新>`：改动 0 行；`columns.py reformat <表> <新>`：改动 0 行。
- `columns.py merge` 再 `split`（sense_write.py 的流程）：来回一趟改动 0 行。

rule_check.py 合计正常基线 30（2026-11 直接母词轮后）。补行以后另看 audit.py 的 [2b][3][9][13]，都应为 0。

2026-11 组合公式、含义列轮以后：「拆分结果」18 列（F 列「含义」），所有脚本按新列号改过，体检数字和上面的基线一样（[5] 290、[6] 14、[7] 1，video_check 全 0，rule_check 30）。video_check 的 no_jinyi 现在查的是 F 列「含义」空不空；audit [12]（以 = 开头的单元格）在含义列也要是 0：“= neighbour：邻居”写成“（= neighbour）邻居”。

2026-11 含义词性分行轮以后：含义列每个意思一行、行首写词性；`meaning.py <xlsx>` 应输出“没有问题”，词性统计约 n. 11671、v. 5084、adj. 4813、adv. 1056、phr. 1048、prep. 131、pron. 84、num. 59、conj. 46、int. 39、modal v. 26、aux. v. 4（共 24,061 个意思）。audit、audit_split_labels、video_check、rule_check、columns 的数字都和上面的基线一样（[5] 290、[6] 14、[7] 1、151、全 0、30、0）。
sense_write.py 试跑（不写回）：和上一版表的试跑相比，各部分解释、组合列只多出 3 行改动（treetop、teachings 补“名词用复数时…”规律，imaginal 补“用进某一行”规律），是含义拆清楚以后才认得出的；其余 21 处两版一样，是以前就有的待补项（这一轮没写回）。

2026-11 例句分列轮以后：「拆分结果」19 列（F 含义、G 例句，后面的列往右挪一列），所有脚本按新列号改过，体检数字仍和上面的基线一样（audit [5] 290、[6] 14、[7] 1；audit_split_labels 151；video_check 全 0；rule_check 30；columns split / reformat 0 改动）。`meaning.py <xlsx>` 应输出“没有问题”，约 24,064 个意思（n. 11685、v. 5070、adj. 4814、adv. 1056、phr. 1051、prep. 131、pron. 84、num. 59、conj. 46、int. 38、modal v. 26、aux. v. 4），例子 18,370 个，8391 行有例句。sense_write.py 试跑：和上一版相比各部分解释、组合列只多出 stairway 1 行（用词规律），其余 24 处同上一版。

2026-11 分三列轮以后：「拆分结果」21 列（J 前缀、K 词根、L 后缀，后面的列往右挪两列）。读表的脚本用 cols.legacy 把三列合回一格，体检数字和基线一样（audit [5] 290、[6] 14、[7] 1；audit_split_labels 151；video_check 全 0；rule_check 30；columns split / reformat 0 改动；meaning.py 没有问题）。sense_write.py 试跑和上一版完全一样（25 处）。有前缀的 1410 行、有词根的 9265 行、有后缀的 4283 行。

词根连字符轮以后：读表时 legacy 去掉词根标签的连字符，体检数字和基线一样（audit [5] 290、[6] 14、[7] 1；audit_split_labels 151；video_check 全 0；rule_check 30；columns split / reformat 0 改动）。挪到后缀列的 -t（debt）、-on（season）补了来源括号和词性变化，-di-（zodiac）写成中间成分，所以 suf_src_text_only、suf_no_here 仍是 0。

单词列轮以后：「拆分结果」22 列（K 词根后面插 L「单词部分」，后面的列往右挪一列）。legacy 把四列合回一格（词根和单词部分的行按拆分里的先后穿插，和分列以前一样），体检数字和基线一样（audit [5] 290、[6] 14、[7] 1；audit_split_labels 151；video_check 全 0；rule_check 30；columns split / reformat 0 改动；meaning.py 没有问题）。另加一项回归：全表每行 `cells(单词, combine(四列), 拆分, 单词表, 词根, 四列, 类型)` 要和原来的四格一模一样（0 行变化；做法见 scripts/archive/danci/idem_test.py）。

源头词根轮以后：audit [4b] 类型分布 ① 5254、⑤ 1587、③ 1408、② 926、④ 118（37 个外来基础词 ⑤ → ②）；其余数字都和上面一样（[5] 290、[6] 14、[7] 1；audit_split_labels 151；video_check 全 0；rule_check 30；columns split / reformat 0 改动；四列来回一趟 0 行变化；meaning.py 没有问题）。新加 `root_check.py`：一（英语词冒充母词）基线 0；`--base` 二（可能要挂到源头词根上的外来基础词）基线 62，都人工看过，同组词根和它不是一个写法来源，不改。

字母变化轮以后：只改了 37 行的 P 列（音变 / 字母变化）和 U 列，体检数字和源头词根轮一样（audit [4b] ① 5254、⑤ 1587、③ 1408、② 926、④ 118，[5] 290、[6] 14、[7] 1；audit_split_labels 和上一版一样；video_check 全 0；rule_check 30；root_check 0；meaning.py 没有问题；recalc 0 错误，fix_pane 冻结回 G2）。新加 `zimu_check.py`：一（该写链没写）0、二（链或步骤写法不对）0，写了链的 37 行；另有 5 行以前用【字母变化】开头写的一句说明（drought、tight、fierce、endorse、falcon），不查。`--todo` 三（候选，人工看）：② 173 个（← 57、≈ 116），拆分 (=…) 变化大的 157 个。

字母变化同源词轮以后：只改了 46 行的 P 列和 U 列（P 列宽 50 → 55），体检数字和字母变化轮完全一样（audit、audit_split_labels、root_check、video_check、rule_check 输出逐字相同；meaning.py 没有问题；recalc 0 错误，fix_pane 冻结回 G2）。zimu_check：一 0、二 0，写了链的 83 行（37 + 46）；`--todo` 三：② 57 个（全是 ←；≈ 的 46 个写了链、70 个逐个看过不写，在 SKIP_APPROX 里不列），拆分 (=…) 变化大的 157 个。

动词变化形式轮以后：改了 154 行的组合列、音变列和 U 列；audit、audit_split_labels、root_check、video_check、rule_check 输出和字母变化同源词版逐字相同；meaning.py 没有问题；recalc 0 错误（公式 119 个），fix_pane 冻结回 G2。zimu_check：一 0、二 0，写了链的 185 行（83 + 102 个动词形式）。「用词规律一览」按全表重算，和组合列对得上（用 parse_I 数每条规律的词，0 处不同）。

合成规律轮以后：组合列加了 1474 行“　合成规律：”、1467 行“　写法：”，音变列 268 行去掉了讲写法的话。audit、audit_split_labels、root_check、video_check、rule_check、zimu_check、meaning.py 输出和动词变化版逐字相同；columns split / reformat 0 改动。新加 `hecheng_check.py`：comp_missing、spell_missing、spell_many、rule_unknown、order_bad、paren_bad、plus_minus、no_body、not_target、sheet_mismatch 都应为 0；write_scattered（写法行以外还在讲连写、连字符的行）基线 35，都是留着的：【演变】里的连写历史、republic / legislator 的拉丁短语、co-writer 的“合写”、run-down ≠ rundown 这类讲意思的辨析。columns.py merge 再 split：J–N 列只有 liven 一行的前缀、后缀两格不同，动词变化版跑出来也是这样，是以前就有的（和这一轮无关）。

英美写法轮以后：只改了含义列（F）190 行、组合列写法那一行 18 行；`yingmei_check.py` 各项 0（装了 breame 时 maybe 也是 0）；meaning.py 没有问题；其余体检和合成规律版一样。

e 结尾加后缀轮以后（make + r → make + er 等 154 个）：audit [5] 223（原 290，少掉的都是“r”“d”对不上“-er”“-ed”行的），audit_split_labels 149（原 151），以后以这两个数为基线；其余体检和英美写法版一样，columns split / reformat 0 改动。

拼写变化轮以后：`pinxie_check.py` missing / double_in_suffix / double_hidden 都是 0；audit_split_labels 31（这一轮把“双写的字母单独一部分”滤掉了，原 149；同一个脚本跑上一版是 94）；audit [5] 244（粗查，双写的字母单独一部分也算进去，所以比 223 多）；其余体检不变，columns split / reformat 0 改动。

过去分词轮以后（拆分改成过去分词词干 X(=Y) 的 145 行，只加构词行的 27 行）：audit [5] 242（原 244，以后以 242 为基线）、[6] 14、[7] 1、[10] 0；audit_split_labels 31；video_check 全 0；rule_check 30；root_check 0；zimu_check 一 0、二 0；hecheng_check 各项 0（write_scattered 35）；yingmei_check 0；pinxie_check missing / double_in_suffix / double_hidden 0；meaning.py 没有问题；columns reformat 0 改动；recalc 0 错误（公式 124 个），fix_pane 冻结回 G2。新加 `guoqu_check.py`：写成过去分词词干的行 146（其中 season 是以前就有的老行，在 OLD_PP 里，不要求构词行），KEEP 27；old_suffix、no_gouci、gouci_bad、stem_no_line、keep_no_gouci 都应为 0。zimu_check --todo 的“(=…) 变化大”不再列 competit(=compete) 这类过去分词词干。

过去分词轮（二）以后（-tion 词 5 行改成过去分词词干，150 行音变列写了链）：zimu_check 一 0、二 写了链的 335 行（原 185）、写法不对 0；guoqu_check 写成过去分词词干的行 151（含老行 season），KEEP 27，old_suffix、no_gouci、gouci_bad、stem_no_line、keep_no_gouci、no_chain 都是 0；其余和上一轮一样：audit [5] 242、[6] 14、[7] 1、[10] 0；audit_split_labels 31；video_check 全 0；rule_check 30；root_check 0；pinxie_check 0；columns reformat 0 改动；recalc 0 错误，fix_pane 冻结回 G2。

- 部分记忆（2026-11）：`python3 scripts/part_memo.py <xlsx> --check` 记法行 468、写法不对 0；`--dry` 再跑“要改的格 0”（已有“记：”的行跳过）。

- 用词规律轮 + 同一个词根轮（2026-11）：`python3 scripts/tonggen_check.py <xlsx>`——left_old、no_change、chain_bad、split_eq、see_derived、old_rule 都应为 0，“记法待补”35 行（按列名读表，16 列、22 列都能跑）；
  `rule_check.py` 合计 29（A 1、F 12、K 15、L 1；G 类 0）；`part_memo.py --check` 记法行 438，写法不对、关联词不比本词简单、变体行没写词根本身、该写音变没写都是 0，`--dry` 0 改动；
  video_check 全 0。这一版表只有 16 列：别的体检脚本按 22 列写，要先在内存里补回空列再跑（第 57 条）。

- 身份分工轮 + 辨析列轮（2026-11，17 列表）：`python3 scripts/shenfen_check.py <xlsx>`——root_chain、heqi_in_parts、var_no_id、id_bad、fam_missing、affix_todo、combo_bianxi、ref_old、syn_bad、heqi_pos 都应为 0；
  另报：辨析列有内容 8355 行、有【同义词】行 4986 行、同义词组里的词辨析文字一个也没提到 2191 行（待补，不算错）。`python3 scripts/shenfen.py <xlsx>`“要改的行 0”，`python3 scripts/cizhui.py <xlsx>`“还能加身份、分工的行 0”（没加的：目录里没有 793 + 567、读不出词性变化 46）。
  `tonggen_check.py` 各项 0、记法待补 35；`part_memo.py --check` 记法行 438、五项 0。按 22 列写的脚本先 `python3 scripts/to22.py <xlsx> <临时.xlsx>` 再跑：video_check 全 0；guoqu_check 写成过去分词词干的行 151、各项 0；
  hecheng_check 各项 0、write_scattered 32；rule_check 合计 29；zimu_check、pinxie_check、root_check、yingmei_check 和上一轮一样。`columns.py` 的 compose_I(parse_I(组合格)) 全表和原格一样（“　合起来：”当普通行留在原位）。

- 拉丁语动词变化轮（2026-11，17 列表 `0词源拆分总表_动词变化版.xlsx`）：`python3 scripts/shenfen_check.py <xlsx>` 14 项都应为 0——原来的 10 项，加 verb_missing、verb_diff、verb_bad、verb_stray；
  另报“写了“动词变化”的词根行 318 行”（辨析列的三个数没变：8355、4986、2191）。`python3 scripts/dongbian.py <xlsx>`“要改的格 0（0 族）”，`--list` 末行“共 57 族、318 行；没有单独过去式的 4 族”。
  别的体检和身份分工辨析版**输出逐字一样**（这一轮只在 318 格词根列里加了一段，脚本看这一行本身之前先去掉它）：shenfen.py、cizhui.py、tonggen_check（各项 0、记法待补 35）、part_memo --check（438、五项 0）；
  补成 22 列以后 video_check 全 0、guoqu_check 151 行各项 0、hecheng_check（write_scattered 32）、rule_check 29、zimu_check、pinxie_check、root_check、yingmei_check、audit、audit_split_labels、meaning.py。
  要是 guoqu_check 冒出 no_gouci / no_chain 几十上百行、shenfen_check 的 root_chain 冒出 81 行：是用了上一版（身份分工辨析版）的脚本，它不认识“动词变化”这一段——换这一版的脚本再跑。

## 2026-11 词缀来历、记法轮以后的基线（0词源拆分总表_词缀来历记法版.xlsx）

- 补成 22 列（to22.py）以后的 video_check、guoqu_check、hecheng_check、rule_check、zimu_check、pinxie_check、root_check、yingmei_check、audit、audit_split_labels、meaning：输出和“动词变化版”逐字一样。
- shenfen_check：14 项 0（affix_todo 0）；dongbian.py：要改的格 0；tonggen_check：各项 0，记法待补 33 行（上一版 35）。
- part_memo.py --check：记法行 1471，写法不对、关联词不比本词简单、变体行没写词根本身、该写音变没写都 0；--dry：要改的格 0。
- laili.py --check：old_left（认得出的旧来历还没换）、memo_missing（该加的词缀记法没加）、memo_bad（X ≈ Y 记法写法不对）、src_lang（来历“经”字前面混了别的语言）都 0。
- lizi.py：要改的格 0（复杂例词）；cizhui.py：还能加身份、分工的行 0。

## 2026-11 例词清理轮以后的基线（0词源拆分总表_复杂例词清理版.xlsx）

- 补成 22 列（to22.py）以后的 video_check、guoqu_check、hecheng_check、rule_check、zimu_check、pinxie_check、root_check、yingmei_check、audit、audit_split_labels、meaning：输出和“词缀来历记法版”逐字一样。
- shenfen_check 14 项 0；dongbian.py 要改的格 0；tonggen_check 各项 0、记法待补 33 行；part_memo.py --check 记法行 1471、五项 0；laili.py --check 四项 0；cizhui.py 还能加身份、分工的行 0（没加的：792 + 567、46）；shenfen.py 要改的行 0。
- `python3 scripts/lizi.py <xlsx> --check`：affix_ex（词缀行还没去掉的复杂例词）、affix_see（指到同词缀别的词的“见 X”）、affix_fix（名单里的个别改写）、root_ex（词根列的复杂例词）都应为 0。
  不带 --check：“词缀行：要改的格 0……词根列：要改的格 0”。拿这一版脚本查上一版的表是 989 / 32 / 1 / 53。
  新加了词以后 affix_ex 不是 0：`--show` 看是哪个例词——换一个“单词 + 这个词缀”的例词，或者（国名、数词这类）记进 lizi_data.KEEP_IN / OK_OUT。

## 2026-11 词缀身份辨析轮以后的基线（0词源拆分总表_词缀身份辨析版.xlsx）

- 补成 22 列（to22.py）以后：video_check 全 0（它先用 `cols.plain_parts` 把词缀行的“身份：”记号、记法、辨析去掉再查——和视频 6.2 读表一样；辨析里“是拉丁语来的”不算这一行的来源）；
  guoqu_check 151 行各项 0；hecheng_check 各项 0、write_scattered 32；rule_check 合计 29；zimu_check、pinxie_check、root_check、yingmei_check 各项 0；audit [5] 242、[6] 13、[7] 0；audit_split_labels 和上一版一样；meaning.py 没有问题；columns.py check 三项 0。
- `python3 scripts/shenfen_check.py <xlsx>`：**18 项**都 0——原来的 14 项，加词缀行的四项：
  affix_no_id（讲词缀的那一行开头没有“身份：”）、affix_old（还留着上一版的“；身份：…。分工：…”）、bianxi_bad（辨析不是最后一段、前面不是句号、里面有句号、在“；记：”前面、一行两段）、
  bianxi_diff（辨析的话不是 cizhui_catalog.py 里的句子，或者和目录给这一行挑的那一组不一样）；affix_todo 现在也包括“还没标身份：”的行。id_bad 只管词根列的“身份：…。分工：…”。
  拿这一版脚本查上一版的表（复杂例词清理版）：affix_no_id、affix_old 会报五千多行——那张表配上一版的技能。
- `python3 scripts/cizhui.py <xlsx> --check`：五项合计 0。不带 --check：“还能标身份、挂辨析的行 0”，没加的：suf_no_entry 817、pre_no_entry 574（目录里没有这个词缀，或这一行不算）、suf_no_tail 52（组合列没写这个后缀的词性变化）。
  `--groups`：20 组共 4286 行（adj_n 770、n_act 671、adj_v 574、n_person 427、adv 409、n_qual 236、neg 232、v_make 211、with 130、into 99、out 78、ad 76、n_dim 71、n_status 64、before 62、over 47、under 41、between 40、self 29、cmp 19）。
- tonggen_check 各项 0、记法待补 33 行；dongbian.py、shenfen.py 要改 0；part_memo.py --check 记法行 1472、五项 0，--dry 要改的格 0；laili.py --check 四项 0、不带 --check “要改的格 0”；lizi.py --check 四项 0、不带 --check 两个 0。
- 新加了词以后 affix_todo 不是 0：`python3 scripts/cizhui.py <xlsx>` 看要标、要挂的是哪些；该挂的 `--write` 写回，不该挂的记进 cizhui_catalog.NO_BX，规则挑错组的记进 FORCE（工作十七）。
- 出表：`xlsx_write.write` 默认只出 xlsx（约 5.5 MB），不再有 `_传输包.zip`。

## 2026-11 词缀关系轮以后的基线（0词源拆分总表_词缀关系版.xlsx）

- 和词缀身份辨析版的基线一样的：补成 22 列以后 video_check 全 0、guoqu_check 151 行各项 0、hecheng_check 各项 0（write_scattered 32；精简表没有「合成规律一览」，sheet_mismatch 报 1 不算）、rule_check 合计 29、
  zimu_check / pinxie_check / root_check / yingmei_check 各项 0、audit（[5] 242、[6] 13、[7] 0）、audit_split_labels 31 行、meaning.py 没有问题、columns.py check 三项 0；
  tonggen_check 各项 0、记法待补 33；dongbian.py、shenfen.py 要改 0；part_memo.py --check 记法行 1472、五项 0；laili.py --check 四项 0、“要改的格 0”；lizi.py --check 四项 0。
- `python3 scripts/shenfen_check.py <xlsx>`：**19 项**都 0（多了 guanxi_bad：“关系”不是辨析的最后一段、一行两段、是空的、哪一条不是词缀打头）。
- `python3 scripts/cizhui.py <xlsx> --check`：六项合计 0。不带 --check：“还能标身份、挂辨析的行 0”，没加的：suf_no_entry 824、pre_no_entry 574、suf_no_tail 52。
  `--groups`：20 组共 4279 行（adj_n 770、n_act 670、adj_v 574、n_person 421、adv 409、n_qual 236、neg 232、v_make 211、with 130、into 99、out 78、ad 76、n_dim 71、n_status 64、before 62、over 47、under 41、between 40、self 29、cmp 19）；其中 10 组带“关系”，共 2758 行。
- 拿这一版脚本查上一版的表（词缀身份辨析版）：bianxi_diff、affix_todo 各报两千七百多行（关系还没写进去）——`python3 scripts/cizhui.py <表> --write <新表>` 一步补上。
- 改了 REL、NO_BX、FORCE 以后：`cizhui.py <表>` 试算会打印“关系 / 去掉辨析 / 换组”各多少行，`--write` 写回，再 `--check`。
- 全套体检想一次跑完、和上一版逐行比：把各脚本的输出接到一个文件里（新表、旧表各一份）再 diff；这一轮除了辨析几项和改的那 8 行（laili.py 的统计行），别的一字不差。
- `python3 scripts/shuyu.py <xlsx>`（2026-11 专业术语轮起）：表里还有“老祖宗 / 老词根 / 老音”的格 **0**。
- 专业术语版的基线：各脚本的数字和词缀关系版一样（只换了说法）；`cizhui.py --groups` 里 before 那一组的句子是新写的那一句（…它们是拉丁语里两个同源的介词…；fore- 和 pre-、pro- 同源，但它是英语本族的前缀…）。
  拿上一版脚本查这张表：目录里的句子还是“老祖宗”，`laili.py --check`、`part_memo.py --check`、`cizhui.py --check` 的 bianxi_diff 会报一千多行——换成这一版脚本就是 0。

## yuanyin.py（2026-11 视频界面轮起；音变原因轮起三项）

`python3 scripts/yuanyin.py <表>`：术语没简化（“原始印欧语 / 原始日耳曼语”）、音变没写原因（格林定律管的音变后面没有“；原因：”）、原因不是现在的写法（还是上一版只有总说的一句，或例子和现在挑的不一样）——都应为 0。
有就 `--write <新表>` 重写（读回来逐格比）；目录不对的先 `--catalog`。

- 2026-11 词根形态补齐轮：`xingtai.py <表> --check` 四项 0（xt_diff 真的查了）；`houzhui.py <表>`、`--pre` 要改的格 0；写了“形态”的词根行 851 行。

## 考点列（第 121 条）
- `python3 scripts/kaodian.py <表> --check`：考纲考点版是“1220 个词有，格式不对的行 0；变形 465，词性转换 562，短语 224，用法 162，易混 133”。改了 kaodian_data.py 以后数字会变，格式不对的行要一直是 0。
- 抽看：`--show produce,suggest,truly,depend,itself,take`，看每一行的出处对不对。

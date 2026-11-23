# 已归档：词根变体说明、按词根归队

这两项工作已全部完成（清单 100 项，见 group_roots.md；按词根归队核对后没有真正要移动的词）。下面是当时的流程和写法，用户要给清单外的新组写词根变体时再用。

注意：脚本在 `scripts/archive/`，是为早先 12 张工作表的版本写的。apply_roots.py 会更新「词根变体待处理」清单状态，这张表已删；move_rows.py 会改写各索引表的超链接，那些表也已删。再用前先把这些部分改成只处理「拆分结果」和「整表核对记录」（见 scripts/archive/README.md）。

# 第一部分：流程

## 任务 A：词根变体说明（包括给新的组做、补漏）

写法口径、样例和脚本识别格式的坑全在 本文件第二部分，动笔前一定要读。

1. **找要处理的组**
   - 清单里的组：`python3 scripts/archive/show_items.py <xlsx> <起> <止>`（打印每项的【背景】和相关解释行）。
   - 已定本组词根的组里还漏写的：`python3 scripts/archive/scan_variants.py <xlsx>`，再加 `--words` 跑一遍。输出噪音多，只挑本组词根一家的写法。
   - 清单外的新组：先自己做一张清单（组号、各种写法），和用户确认范围。
2. **逐组判断**（最关键，必须自己判断，不照抄清单）：本组词根定成这一家最基本的写法，以【背景】说的来源为准；每个写法判断是：
   - 由本组词根变来；
   - 兄弟或远亲；
   - 只是拼法巧合；
   - 说法不一；
   - 清单误筛。

   先查 `progress_log.md` 的“关键判断”，已经判过的照旧。
3. **写 round 模块** `/home/claude/roundN.py`（格式见 本文件第二部分 第 4 节）。写完检查 E 里每个词在表里只出现一次。
4. **写入**：`python3 scripts/archive/apply_roots.py <源.xlsx> <输出.xlsx> roundN.py`。
   `not applied` 必须为空，否则改好标签键后从源文件重跑。脚本会做这些事：
   - 替换解释行；
   - 在 P 列写“词根说明”；
   - 更新清单状态；
   - 给 Q 列做标注（绿底），H 列涂浅绿。
5. **检查 Q 列标签**：统计输出文件 Q 列各“清单第 N 项 · 本组词根 X”。同一项出现两种写法（如 Janu / janu）或缺本组词根，就是踩了识别格式的坑，改写法后重跑。
6. 接着做任务 B。

## 任务 B：按词根归队（移动行）

规矩：一个词的词根 R 如果在表里另有一组（那组的本组词根就是 R），就把这个词移到那一组；表里没有 R 的组就留在原位。

```bash
cd /home/claude && python3 <技能目录>/scripts/archive/check_moves.py <xlsx>      # 列出建议，写出 moves.json
```

逐条核对：必须确实是同一个词根，目标组也确实是这个词根的一家。aware → 第 813 组这条已核对否决，直接删掉。

删完还有要移的，再执行下面这一步。脚本会改批次、组号、小类号，重排序号，交接【背景】，并改写所有行号引用和超链接：

```bash
python3 <技能目录>/scripts/archive/move_rows.py <xlsx> <xlsx> moves.json
```



# 第二部分：写法

## 1. 五种行的模板

**a. 由本组词根变来（第一次出现，完整式）**
`X：由词根 R 变来。词形：R → X，<哪个字母变了/加了什么/掉了什么，以及原因>。意思：R“本义”（来源）→ 第二步 → … → 在这个词里的意思`

**b. 同组里第二次及以后出现（短式）**
`X：由词根 R 变来（R → X，见 <第一个词>），意思是“…”→ 前缀含义 → 本词意思`

**c. 和本组词根同形**
`R：本组词根“意思”（来源，见 …）→ 前缀含义 → 本词意思`

**d. 兄弟 / 远亲（不是从本组词根变来）**
`X：词根 X“意思”（来源）。它不是从本组词根 R 变来的，两者是兄弟：都出自 …。意思：…`
（开头必须是“X：词根 X”，检查脚本靠它认出这一行自己的词根；后面出现“本组词根 R”，Q 列才会标成 R。）

**e. 只是拼法巧合 / 来历说法不一**
在行末写“和 … 里的 X 只是拼法巧合”；来历不定写“来历词典说法不一：一说…；一说…”，不写成“由词根 R 变来”。

**清单误筛**（其实是完整的词、母词、后缀、前缀）：不改解释，状态写 `核对：…，不是词根变体`。

写法要点：
- 意思路径一步一步写逻辑；词形变化写具体：d 碰上 t 变成 s、a 弱化成 i / e、经古法语磨掉 c / d、加不发音的 e、-sc- 只在现在时里出现、s 夹在元音间变成 r（genus → generis）、n 只在现在时里出现（cernere、frangere）、g 碰上 t 写成 c（structus、auctus）。
- 原行里有用的信息（年代、同源词、“和‘折痕’crease 无关”这类提醒）尽量保留进新行。
- 准确优先：mag 去掉 n 的情况写“由词根 magn 变来（准确说是 magn 去掉 n 的 mag）”；借来补位的形式（ferre 的 lātus）写清“借来”。

## 2. 已完成的样例

- common：`mon：由词根 mun 变来。词形：mun → mon，拉丁语 communis 里是 u，到中古英语写成了 o。意思：mun 本是“大家互相出的力、交的份子”（拉丁语 munus，老祖宗是原始印欧语 *mei-“交换”）→ 为城邦尽的公共义务 → 和 com“一起”合起来，就是“一起分担义务的”→ 共同的`
- exist：`sist：由词根 sta 变来。词形：sta → sist，拉丁语 sistere“使站住”是把 st 叠了一下（si + st），a 也没了。意思：sta“站”→ 使站住、站定 → ex + sistere = exsistere“站出来”→ 出现 → 存在；x 里本来就带 s 音，后面的 s 就省掉了`
- assist（短式）：`sist：由词根 sta 变来（sta → sist，见 exist），意思是“站、使站住”`
- index：`dex：由词根 dic 变来。词形：dic → dex，拉丁语 index 的词干是 indic-（属格 indicis），主格加词尾 -s 时 c 和 s 拼成 x，i 也变成了 e；复数 indices 里又露出了 dic。意思：dic“指出”→ in“向着”指 → 指出者（食指、告密人都叫 index）→ 索引；指数`
- advantage：`vant：由词根 ante 变来。词形：ante → vant：晚期拉丁语 abante“从前面”里，ab 的 b 和 ante 连在一起，到法语成了 v，ante 词尾的 e 也掉了，于是成了 avant“在前”；16 世纪英语误把开头的 a- 当成 ad-，插进 d，拆开来 ad 后面就剩下 vant。…`
- recipe：`cipe：由词根 cap 变来。词形：cap → cip → cipe：recipere 里 a 弱化成 i；末尾的 e 不是不发音的 e，而是拉丁语下命令的词尾：recipe =“拿着！”。…`
- tectonic（兄弟）：`tecton：词根 tecton“建造者、木匠”（希腊语 tektōn…）。它不是从本组词根 techn 变来的，两者是兄弟：都出自老祖宗 *teks-“编织、制作”…`
- relate（借来补位）：`late：词根 lat“被带的”（拉丁语 lātus）。它不是从本组词根 fer 变来的：拉丁语 ferre 没有自己的“被带的”形式，就借了另一个词根的 lātus 来补（就像英语 go 的过去式借了 went）；lātus 本是 tlātus，老祖宗 *tel-“举起、承受”…`
- garage（说法不一）：`gar：来历词典说法不一。法语 garer“遮护、安置”…；etymonline 把它归到“盖住、护住”的 *wer-，也有说法认为和本组词根 ward 同源。意思：…`
- resemble 与 ensemble：同写 semble，来路不同：resemble 来自 simulare（由 simil 变来，写 a 式），ensemble / assemble 来自 simul“一起”（兄弟，写 d 式），在行里注明“写法一样，来路不同”。

状态写法：`'已处理'`、`'已处理（qual、quant 是兄弟词根）'`、`'核对：dehydration 是完整的词，不是词根变体'`。

## 3. 脚本识别格式的坑（务必看）

mark_rows.py 给 Q 列取本组词根的规则（re.search，取整格里最先出现的匹配）：
1. `由词根 X 变来`
2. `本组词根 X`（“本组词根”后面紧跟空格和字母）
3. 行首 `X：本组词根`

check_moves.py 取一行自己的词根：先找 `由词根 X 变来`，再找行首 `X：词根 X` 或 `X：本组词根X`。

由此踩过的坑：
- `mut：词根，拉丁语 …`（“词根”后面是逗号）：两边都认不出 → Q 列没有本组词根。改成 `mut：本组词根“…”`。
- `Janu：本组词根 janu…`：规则 3 在行首先命中，Q 列标成大写的 Janu。改成 `Janu：即本组词根 janu“…”`。
- 兄弟行一定要以 `X：词根 X` 开头，否则 check_moves 会把它当成本组词根一家，或者认不出。
- 别在一行开头部分写别的词根的“由词根 Y 变来”，会被当成这一行的词根。
- 标签键 = 冒号前的标签，去掉括号里的内容、去掉连字符、转小写：`(s)pect` → `pect`，`mo(v)` → `mo`，`gar(ne)` → `gar`，`Olymp` → `olymp`，`de + lic` → `de + lic`。
- apply_roots.py 按“单词第一次出现的行”找行，同形词（bore、lie…）要用 fixlib.py 的 `nth=2`。
- 同组不同词根时本组词根要起不同的名字，避免互相串（第 513 组 curr“跑”vs 第 265 组 cur“操心”；第 584 组 terr“吓”vs 第 2138 组 terra“土地”；第 370 组 cap“拿”vs 第 599 组 capit“头”）。

## 4. round 模块格式（apply_roots.py 用）

```python
SPS = 'spect：由词根 spec 变来（spec → spect，见 respect），意思是“看”'
E = {
  'respect': {'spect': 'spect：由词根 spec 变来。词形：…。意思：spec“看”→ re“回头”看 → 回头再看一眼 → 重视、尊敬'},
  'inspect': {'spect': SPS + ' → in“往里”看 → 检查'},
  'improvise': {'provise': 'pro-：“向前、预先”…\nvise：由词根 vid 变来…'},   # 值里有 \n 就把一行拆成两行
}
STATUS = {17: '已处理'}   # 清单序号 → 状态；不改清单时写 STATUS = {}
```
写完先检查 E 里每个词在表里只出现一次（同形词改用 fixlib），再跑 apply_roots.py；输出 `not applied` 不为空就是标签键写错了，改好后从原文件重跑。



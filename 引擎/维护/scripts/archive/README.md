# 已归档的脚本（词根变体、按词根归队）

这些脚本是为早先 12 张工作表的总表写的；2026-11-03 起总表只剩「拆分结果」「用词规律一览」「整表核对记录」「说明」。再用前要改：

- apply_roots.py：会更新「词根变体待处理」的状态列，这张表已删，把那一段去掉（清单状态改记在 references/archive/group_roots.md）。
- mark_rows.py：只改「拆分结果」Q 列和 H 列底色，可以直接用。
- show_items.py、scan_variants.py：读「词根变体待处理」清单的部分要改成读 references/archive/group_roots.md。
- check_moves.py、move_rows.py：move_rows.py 会改写各索引表的超链接，那些表已删；只保留改写「拆分结果」P 列“第 N 行”和「整表核对记录」超链接的部分。

## qingshuang/（2026-11 组合列清爽轮，只作记录）

- convert.py：把旧格式的组合列转成清爽格式（今后直接用 `columns.py reformat`）。
- fixes_pos.py：58 行几个后缀的词、6 行认不出的句子、22 行补后缀意思的手工核对结果。
- norm_pos.py：“是一样东西或一种人，加上 -ism，指…”这类模板句的整理。
- src_manual.py：111 行来源和说明连在一起、要手改的后缀行（原文片段 → 新片段）。

- `danci/`：单词列轮（2026-11，词根后面加 L 列「单词部分」）的判断名单和写回脚本，见 danci/README.md。
- `yuantou/`：源头词根轮（2026-11）的改表脚本 round.py：24 个派生词改回源头词根（popul + ar），37 个外来基础词 ⑤ → ②（people ← popul），major、minor 的词性变化；只作记录，以后用 scripts/root_check.py 查、手改。

- `zimu/`：字母变化轮（2026-11）：round.py + zimu_data.py（37 个词的字母变化链），只作记录

- `guoqu/`：过去分词轮（2026-11）：round.py 改表、data.py 逐词数据（拉丁语原形、意思、过去分词词干），见 guoqu/README.md

- `shenfen/`：身份分工轮 + 辨析列轮（2026-11）：round.py 改表（16 列 → 17 列）、manual.py 手工定的几处和 produce / product 的辨析样板、report.py 改动清单，见 shenfen/README.md

- `dongbian/`：拉丁语动词变化轮（2026-11）：report.py 改动清单（说明、动词变化、词根列、没收的）；这一轮的数据和写回在 scripts/dongbian_data.py、scripts/dongbian.py，见 dongbian/README.md

- `laili/`：词缀来历、记法轮（2026-11）：round.py 改表（动词变化 → 复杂例词 → 词根记法 → 词缀来历和记法）、report.py 改动清单，只作记录

- `lizi2/`：例词清理轮（2026-11）：round.py 改表（lizi.plan_affix → lizi.plan，只删字）、report.py 改动清单（去掉的例词（请过目）、去掉的例词汇总、留着的例词汇总、去掉的“见”和改写、逐格），只作记录

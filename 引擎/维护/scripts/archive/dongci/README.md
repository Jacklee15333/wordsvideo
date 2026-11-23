# 动词变化形式轮（2026-11）的一次性脚本，只作记录

round.py <源表> <新表>：在字母变化同源词版上，把 154 个不规则动词形式（vlist.py：单词、原形、过去式 / 过去分词、行号）的组合列、音变列换成新写法（vdata1.py、vdata2.py，模板在 vhelp.py），每行写 U 列“动词变化形式：…”，「整表核对记录」记 3 条，「说明」改 N、P 两列的说明、第七节加一行，「用词规律一览」按全表重算。跑完再 recalc、fix_pane。加 --dry --show made,wrote 只打印不写表。
规矩见 references/project_rules.md 第 47 条，写法见 writing_guide.md 第 10 节。

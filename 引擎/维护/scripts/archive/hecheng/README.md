# 合成规律轮（2026-11）的一次性脚本，只作记录

- catalog.py：34 条合成规律、18 条写法的目录（同 scripts/hecheng_catalog.py、「合成规律一览」）
- feat.py / auto.py：读表、给每个词起初步分类；wcat.py：逐个定下的分类；wphr.py：每个词是从哪个短语来的（cut paper → paper-cutting）
- wman.py：手写的合成规律（外语原来的先后、命令式、并列、类名叠加……）和第二行特殊规律（man → men、中间的 s、复数位置、意思固定）
- gen.py：生成“　合成规律：”行；spell_rule.py / spell.py：生成“　写法：”行
- consol.py / mixfix.py / pass2.py：把散在【语法】【辨析】【提醒】、步骤括号、指路行、音变列里讲写法的旧说明并进写法那一行
- apply.py：写回总表（逐行 parse_I / compose_I 来回校验）、U 列记录、「合成规律一览」、「整表核对记录」、「说明」
运行顺序：feat.py → gen.py → apply.py <源> <新>（apply 会调用 consol、spell、pass2）。路径写死在 /home/claude/work/hc，再用时先改路径。

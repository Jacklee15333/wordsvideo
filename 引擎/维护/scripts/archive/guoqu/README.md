# 过去分词轮（2026-11）的脚本，只作记录

| 文件 | 做什么 |
|---|---|
| data.py | 逐词数据：L_DATA（整个从拉丁语借来、接在过去分词词干上的 145 个：拉丁语原形、意思、过去分词词干、词根列补的一句；cls='E' 是英语照拉丁规矩造的）、U_DATA（英语后来自己用现成 -ation / -ative 造的 27 个）、SPECIAL（不规则的手写：sensitive、sensation、constellation、literature、miniature、imperative、publication、gravitation） |
| round.py | 改表：拆分改成“过去分词词干(=母词) + 后缀”，词根列写词干怎么来，后缀列换成标准的 -ion / -ive / -or / -ory / -ure 并写“接在过去分词词干后面”，组合列第一行跟着改、下面加“　构词：”一行；U 列、「整表核对记录」「说明」一起写。`python3 round.py <源.xlsx> <新.xlsx>`，同目录写 review.txt 供人工看。U_DATA 的年代取自 etymonline 整站数据（/tmp/work/ety.pkl，没有就不写年代） |

以后新补这类词：照 data.py 加一条再跑，或照 writing_guide.md 第 13 节手写；写完跑 scripts/guoqu_check.py。
| round2.py | 过去分词轮（二）：沿用 round.py 改 5 个 -tion 词（reduction、introduction、production、nutrition、mixture），再给所有写成过去分词词干的行在音变列写【字母变化】链和步骤；KIND、step2 按动词类型写第二步（-are、-ire、连接元音 i、b → p、c + t、d → s、tt → ss、v → u、复合词元音弱化、不规则的），FULL 是手写的 5 个，P_KEEP 是原来那句话要加标签留下的。`python3 round2.py <源.xlsx> <新.xlsx>` |

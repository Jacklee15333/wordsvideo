# 词根形态补齐轮（2026-11，第 113–118 条）的一次性脚本，只作记录
- spec.py：逐族定下的数据（F 新立一族、C 照搬已有词根族的三个样子、J 老族补写法）
- build_xv.py：照 spec.py 和当时的表生成 scripts/xingtai_verb.py（分工那句话的例词取表里这一组用这个写法的词），并用 Whitaker's Words（github.com/mk270/whitakers-words 的 DICTLINE.GEN）核三个样子
以后改一族直接改 scripts/xingtai_verb.py，不用再跑这两个脚本（路径是当时工作目录里的）。

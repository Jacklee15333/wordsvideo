# 拉丁语动词变化轮（2026-11）的脚本，只作记录

起因、规矩见 references/project_rules.md 第 71、72 条。

- 这一轮没有单独的改表脚本：数据在 `scripts/dongbian_data.py`，写回就是
  `python3 scripts/dongbian.py <身份分工辨析版.xlsx> --write <动词变化版.xlsx>`（只动词根列 318 格；xlsx_write.write；写完读回逐格比）。
- `report.py`：`python3 report.py <改前.xlsx> <改后.xlsx> <清单.xlsx>` 出这一轮的改动清单（说明、动词变化、词根列、没收的）。
- 同一轮改的别的脚本（都是为了不让这一段干扰原来的体检）：
  `cols.py` 加 `strip_dongbian` / `strip_meta`；`shenfen.py` 的 `cut` 先去掉这一段再找通到今义的链；`guoqu_check.py` 认“过去分词词干”的行之前去掉这一段；
  `tonggen_check.py` 看这一行提没提“过去分词”之前去掉这一段；`shenfen_check.py` 加 verb_missing / verb_diff / verb_bad / verb_stray 四项。
  没打这些补丁的上一版脚本对着新表会误报：shenfen_check 的 root_chain 81、guoqu_check 的 no_gouci / no_chain 各 96。

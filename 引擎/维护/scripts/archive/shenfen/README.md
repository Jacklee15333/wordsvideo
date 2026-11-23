# 身份分工轮 + 辨析列轮（2026-11）的改表脚本，只作记录

- `round.py`：从 16 列的“真规律同词根版”算出 17 列的“身份分工辨析版”。`python3 round.py plan <原表>` 只试算；`python3 round.py write <原表> <新表>` 写表（`xlsx_write.rebuild`）并在新表旁边存一份 `round_shenfen.pkl`（改前、改后、每行切出去的链，给 report.py 用）。
  先后：手工的几处 → 词根列（`shenfen.plan`：切链、身份分工、收集“合起来”）→ 前缀列补“这里是” → 词缀身份分工（`cizhui.plan`）→ 辨析列（挪【辨析】、算【同义词】、从同组的词补）→ 组合列插“合起来”。
  它只认没有辨析列的 16 列表（有辨析列会停下）。在 17 列表上接着做，用 `scripts/` 里的 shenfen.py、cizhui.py、bianxi.py 各自试算，再照这里的写法组织。
- `manual.py`：自动规则办不了、手工定的：HEQI_FIX（从链里拼出来不通顺的“合起来”）、ROOT_PATCH / ROOT_AFTER（commit、arrogant、intrigue、fluorescent 的词根行）、PRE_PATCH（relevant、compulsory 前缀行里的整合）、WP_MOVE（单词部分列里的“合起来”行）、BIANXI（produce、product 的辨析样板）。
- `report.py`：`python3 report.py round_shenfen.pkl <清单.xlsx>` 出这一轮的改动清单（10 张表）。

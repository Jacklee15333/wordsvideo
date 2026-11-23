# 7A-U4 kit 里现成的词

文件夹名是 `~/kit/words/` 里的文件名（词组用下划线）。“画图脚本”按顺序写，就是 make_word.sh 的第三个参数。
“依据”一栏：README = 视频技能 `~/kit/README.md` 里写明的；推测 = 按文件名或单元顺序推的，**跑之前和用户确认序号**；缺图时脚本会提示要加哪个画图脚本。
画风按序号每 5 个换一种：01–05 图画书、06–10 青绿工笔、11–15 水墨写意、16–20 中西合璧、21–25 图画书、26–30 青绿工笔……（`styles.py` 的 `style_for` 决定，make_word.sh 自动转）。

| 序号 | 文件夹名 | 画图脚本 | 依据 |
|---|---|---|---|
| 01 | camera | cam | 序号 README；脚本推测 |
| 03 | thermostat | thermo | 推测 |
| 04 | itself | itself | 序号见归档“04 itself.mp4”；脚本核对过 |
| 05 | alarm | alarm | README |
| 06 | stranger | street | 序号 README；脚本推测（kit 里没有 stranger_art.py，缺图时按提示补，可能要 owner） |
| 07 | lock | lock | 推测 |
| 08 | explore | explore | 推测 |
| 09 | rock | explore,rock | README（山林背景和飞鸟要先跑 explore）；序号推测 |
| 10 | shower | shower | 推测 |
| 11 | mode | mode | 序号 README；脚本按画面设置里用到的图核对过 |
| 12 | text_message | textmsg | 序号 README；脚本按画面设置里用到的图核对过 |
| 13 | bedroom | shower,bedroom | 序号 README；脚本推测 |
| 14 | bathroom | shower,bedroom,bathroom | README |
| 15 | suggest | explore,shower,bedroom,suggest | README |
| 16 | protect | explore,shower,itself,protect | README（第七十七、七十八版样本就是这样出的） |
| 17 | review | explore,review | README |
| 18 | heating | shower,bedroom,thermo,heating | README |
| 19 | guide | street,explore,textmsg,guide | README |
| 20 | personal | street,shower,bathroom,personal | README |
| 21 | owner | owner | README |
| 22 | alarm_clock | alarm,alarmclock | README |
| 23 | keep_track_of | street,explore,mode,ktrack | README；**要先手改一句配音**，见下 |
| 24 | schedule | schedule | README |
| 25 | health_care | alarm,healthcare | README |
| 26 | order | street,alarm,order | README |
| 27 | signal | street,explore,signal | README |
| 28 | sense | owner,sense | README |
| 29 | manage | explore,manage | README |
| 30 | remind | owner,remind | README |

speaker（02）没有在 kit 里，是视频技能的标准样例（`references/example-speaker/`），本技能不包。

## 要先手改配音的词

- **keep_track_of**：先 `make_word.sh keep_track_of 23 street,explore,mode,ktrack --no-run`，再【WSL】
  `cd ~/skills/word-construction-video/scripts && python3 ~/kit/tools/fixsay.py keep_track_of "单词是 of，of。" "单词是 of，表示“…的”。track of a rabbit，就是兔子的踪迹。"`
  然后跑不带 `--no-run` 的同一条命令。（总表 of 那一格没写意思。）
- **protect**：两处已经写在本技能的 `fixes/protect.py` 里，make_word.sh 自动改，不用管。

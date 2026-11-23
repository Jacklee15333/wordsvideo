# 角色库（5.2 起）

配音说到某个时代、某种身份的人时，画里要画那样的人（pictures.md 第十一节）。画好的角色放这里，以后的词复制到自己的 art/ 里用。

- `roman-hunter.svg`：古罗马猎人（explore 用过）。朝右走，红色短袍金边、腰带、斗篷和别针、短卷发、绑带凉鞋，后面的手握猎矛，前面的手拢在嘴边喊（嘴张开）。viewBox 260 × 440，嘴在 (171, 113) 附近：声波写 `on` 这个角色、从 x≈200 往右画（见 explore 的 prefs：`shout_on`）。站在地上：`y` = 地面高度 − `s` / 2。
- `duck.svg`、`duckling.svg`（5.11）：鸭妈妈（白，朝右）和小鸭子（黄，朝右）。词根 duc“领着走”的记法 duc ∽ duck 用：鸭妈妈走在前面，后面跟一串小鸭子，一起往右走（`go` + `anim: "ride"`）。
  viewBox 220 × 200 / 130 × 120。摆法：鸭妈妈 `s` 0.46，小鸭子 `s` 是它的 0.46 倍、`y` 低 0.27 × s，一只比一只靠后 0.46 × s（见 example-produce 的 partPics、flow 第一框）。
  同一个词根的词（produce、product、introduce、reduce、conduct、educate）都用它。

## 6.22 起：图画书画风人物（scripts/bookstyle.py 生成），中外结合

腰部以上、正面，站在讲台 / 书桌 / 课桌后面让家具挡住腰（见 `../example-speaker/`）。说话的人嘴边加 `waves.svg`（`on` 挂在人身上：x 292、y 186）。文件名 `cn-` 是中国人、`west-` 是欧美人，一个词里两种都要有（规矩 48）。

| 文件 | 人物 |
|---|---|
| cn-teacher-talk / say / calm | 中国女老师，两个发髻，黄衣湖蓝领：抬手讲解说话 / 手放下说话 / 微笑 |
| cn-boy-smile / talk | 中国男生，黑短发，蓝衣白领 |
| cn-girl-smile | 中国女生，扎马尾，玫红衣服 |
| west-man-talk / calm | 欧美男士，棕发络腮胡，深蓝西装红领带 |
| west-girl-smile / talk | 欧美女孩，红色卷发、雀斑，蓝衣黄领 |
| west-woman-smile | 欧美女士，金色长发，玫红衣服 |
| west-boy-smile | 黑人男孩，黑色卷短发，橙色衣服 |
| west-clerk | 戴眼镜的职员（“计算的人”），棕发，绿色毛衣领带 |

要别的人：`from bookstyle import person`（参数见 `pictures.md` 第十六节）。6.20、6.21 的写实人物（scripts/people.py）不再用。

## 6.24 起：动作、表情（scripts/poses.py 生成，在 `poses/`）

同一个人在不同画面换动作和表情，说话、挥手、听音乐的做成动图（几帧轮着放）。画布 0 0 720 560，嘴在 (360, 192)。

| 文件 | 动作、表情 |
|---|---|
| cn-teacher-point_f0 / f1 | 中国女老师指着黑板讲（嘴一张一合，动图） |
| cn-teacher-listen | 手放胸前、歪着头听 |
| cn-teacher-laugh | 笑眯眯地哈哈笑 |
| cn-boy-raise_f0 / f1 | 中国男生睁大眼睛举手（动图） |
| west-girl-listen | 红发女孩歪头微笑着听 |
| west-girl-raise_f0 / f1 | 举手发言（动图） |
| west-girl-explain_f0 / f1 | 两手摊开讲（动图） |
| west-girl-music_f0 … f3 | 听音乐笑眯眯地摇头、竖大拇指（四帧动图） |
| west-girl-surprised | 吃惊：圆嘴、睁大眼睛 |
| west-man-hello_f0 / f1 | 外国男士挥手打招呼（动图） |
| west-man-present_f0 / f1 | 两手摊开、举高讲解（动图，讲台后面也看得见） |
| west-man-point_f0 / f1 | 指着旁边（屏幕）讲（动图） |
| west-man-speech_f0 / f1 | 竖起手指强调（动图） |
| west-man-smile | 手放胸前、笑眯眯 |
| west-clerk-think | 职员托着下巴想 |
| west-clerk-happy | 职员竖大拇指大笑 |


## 6.25：会动的人

`python3 scripts/poses.py <art 文件夹> --motion`：`MOTIONS` 里每个动作生成几帧（说话 = 手势 × 嘴型，听 = 慢慢动 + 闭眼的几帧，笑、跟着音乐摇头），`WALKERS` 生成全身走路的人（6 帧一步，拖行李箱 / 背书包，中外都有），并写 `motions.json`（每个动作的帧和放法 seq、fps、mouths、gfps）。prefs 怎么写见 `references/pictures.md` 第十八节、`references/example-speaker/make_prefs.py` 的 `actor`、`walker`。

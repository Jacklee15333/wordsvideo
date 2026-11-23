---
name: wordsvideo-handoff
description: 接着开发“单词工作台”（GitHub 仓库 Jacklee15333/wordsvideo）的交接说明：项目是什么、仓库和软件怎么组织、怎么改、怎么测、怎么按版本规矩发布、踩过的坑、做到哪了、下一步做什么。用户在新聊天里发来这个技能，或者说“继续做单词工作台”“改一下单词工作台”“wordsvideo 软件”“出题软件/做视频软件出问题了”时，一定要先读这个技能。
---

# 单词工作台 · 交接

## 一、用户和项目

- 用户是中学英语老师，用 Windows 11（20 核、32 GB、RTX 5060 Ti），会一点编程。要中文、简短、带具体数字和文件名；界面要“傻瓜化”，一看就知道怎么点。
- 项目：给初中词源拆分总表（9,299 行）里的每个词做“构词动画”教学视频。每个词要三样：① 7 道练习题 ② 视频画面（画面设置）③ 视频。以后还要能把网上的学习资料发给软件提取、加工、分类（还没做）。
- 软件“单词工作台”在仓库 **Jacklee15333/wordsvideo**（私有，分支 main）。用户用 GitHub Desktop 克隆在 `D:\my projects\出题工作台\wordsvideo`，双击 `启动.bat` 运行（Python 后台 + 本地网页，Edge 应用窗口，http://127.0.0.1:8766）。
- 旧仓库 **Jacklee15333/ciyuanchaifeng**：以前的全部资料。除了 67 个 mp4（1.6 GB）都已经搬进 wordsvideo；旧仓库以后不再更新词库数据，以 wordsvideo 为准。
- 用户的电脑走代理：Clash 类软件，端口 **7892**，智能分流。git 全局已设 `http.proxy http://127.0.0.1:7892`。

## 二、仓库结构（wordsvideo）

```
启动.bat                    装 openpyxl、playwright，跑 app\server.py
app\VERSION                 版本号（现在 1.7.0）
app\server.py               HTTP 服务、全部接口（/api/...），开 Edge 应用窗口（单独资料夹 data\edge-app）
app\core.py                 配置、SQLite、git、总表/索引/README、简写稿体检、提示词、出题流水线、AI 调用、任务队列、定时、手动接力
app\pics.py                 做视频画面（AI 写画面设置 JSON + SVG 插图，检查，可选 WSL 起草检查，存盘）
app\video.py                出片：引擎同步进 WSL、装环境、建批次、开工、登记视频（WSL 部分没在真机测过）
app\clip.py               Windows 剪贴板读写（手动接力用）
app\selfup.py               版本、检查更新（git pull）、备份、回退、让网页 AI 改软件
app\web_model.py            操作 sorryios 网页 ChatGPT（超能小助 super-assistant 原样拷来，不要改，要改就从超能小助拷新的）
app\web_tools.py            web_model 要的两个小函数的替身
app\web\index.html          整个界面（一个文件，CSS/JS 都在里面，不引用外网）
app\web\icon2-*.png、icon2.ico、logo.svg   图标（改图标要换新文件名，Edge 会缓存旧的）
词库\总表\第八十五版\2词源拆分总表_初中含义版.xlsx    总表（出新版就建“第八十六版”文件夹，软件用编号最大的）
词库\总表视频细节数据\      每个词一个 json（题目、题目原稿、画面、插图）、索引.tsv、README.md（进度表、总表问题）、工具\（lianxi.py 体检正本）、出题技能\zongbiao-questions.skill（规矩、范例）
词库\画面设置\              AI 做的画面：words\<词>.json/.py、art\<词>\*.svg、<词>ai_art.py、清单.tsv
词库\视频清单.tsv           做好的视频登记（视频本身在 D:\构词视频，不进 git）
引擎\维护 视频 本地出片 批量出片   四个技能原样解开（视频技能 6.41.0，kit 里有 7A-U4 的 29 个词）
素材\                       音色录音、画风试样
旧仓库资料\                 旧仓库其余资料（软件不读）
版本备份\v<版本号>\app       每个旧版本的 app
CHANGELOG.md                更新记录（最新的在最上面）
data\（不进 git）            config.json（令牌、账号）、app.db、repo\（软件自己的稀疏仓库副本：只放 词库/引擎/素材）
```

## 三、软件怎么工作（要点）

- **数据以 GitHub 为准**：软件在 `data\repo` 克隆一份稀疏副本，出好的东西写进去、提交、马上推送；用户在 GitHub Desktop 里 Pull 就到本地。每组（25 个词）记 README 进度表一行、一次提交（“题目第 N 批第 K 组”，4 组一批）。
- **出题**：按总表顺序取“缺”的词，提示词＝出题技能的 rules.md + example.md + 附加要求 + 总表材料，要求 AI 只输出一个代码块里的简写稿、最后一行 `ZBQ-END`。体检＝仓库 `工具/lianxi.py`（fmt_word、check_word）+ 附加检查（4 个选项、2–5 题型不重复、句子 ≤12 词）。没过带着报错退回改（默认 3 轮），还不过进“待人工”（自动出题跳过）。
- **出题用哪个 AI**（任务页「⚙ 设置」三选一 + 模拟）：`web` 网页镜像 ChatGPT（sorryios，web_model 自动操作浏览器）；`api` 接口 AI（OpenAI 兼容、流式；DeepSeek，或 Anthropic `https://api.anthropic.com/v1` + `claude-opus-5-5`）；`relay` 手动接力（比如 zd87 上的 Claude：软件自动把提示词放进 Windows 剪贴板、响一声；用户在网页里粘贴发送，写完点网页的「复制」，软件盯着剪贴板（clip.py，GetClipboardSequenceNumber），看到带 ZBQ-END、提到这批词的回复就自己接着做；也能手动粘回；一次 25 个词）；`mock` 只测流程。每个词、README 都记是哪个 AI 出的。
- **做视频画面**：pics.py。提示词＝视频技能 data-format.md + pictures.md 摘要 + camera 范例 + 现成场景名（77 个）+ 会动的人（22 个，名字里两个以上“-”的）。AI 输出 JSON 画面设置 + `<<<SVG 名字.svg … >>>END` 插图；人物写 `{"actor": 动作名, x, y, s}`，`words/<词>.py` 在 WSL 里用 prefkit.actor 换成会动的人。检查：JSON、插图都在、动作名对、不许表情图（"e"）、SVG 能解析；出片环境装好了再跑视频技能起草检查（要“还要补：都齐了”）。
- **任务页**：三步卡片（出题 → 做视频画面 → 出视频）、“做指定的词”输入框、手动接力黄框、实时画面（浏览器截图、AI 实时回复、步骤记录）、每天定时、时间窗口。
- **出片**：video.py 用 `wsl -d Ubuntu-24.04 -u root -- bash -lc` 调用批量流水线 `~/lwb/scripts/wsl/batch.sh`；“同步引擎进 WSL”代替原来的 02_get_repo.sh。批次 UPLOAD=0，视频拷到 D:\构词视频\<批次>，登记进视频清单。

## 四、怎么改、怎么测（在 Claude 的沙盒里）

1. 克隆：令牌由用户给（以前放在上传的 txt 里）。**绝不打印令牌**，用 `http.extraHeader`：
   ```bash
   TOKEN=$(python3 -c "import re;print(re.search(r'github_pat_[A-Za-z0-9_]+',open('令牌文件',encoding='utf-8').read()).group(0))")
   B=$(printf "x-access-token:%s" "$TOKEN" | base64 -w0)
   git -c http.extraHeader="Authorization: Basic $B" clone https://github.com/Jacklee15333/wordsvideo.git wv
   ```
   bash 里用 `bash -c '…'` 包一层（默认 sh 不认识 `{a,b}`、`${#X}`）。
2. 本地测试远端：`git clone --bare wv test.git; git -C test.git config uploadpack.allowFilter true`；测试文件夹放 `data/config.json`：`{"repoUrl":"file:///…/test.git","provider":"mock"}`，再把 app 拷进去（**先删掉目标里的 app 再 cp -r**，不然会拷成 app/app）。
3. 跑：`cd 测试/app && CHUTI_PORT=87xx CHUTI_NO_BROWSER=1 setsid nohup python3 server.py > log 2>&1 < /dev/null &`。别用 `pkill -f server.py`（会连自己这条命令一起杀掉），换端口另起一个就行。
   - `CHUTI_MOCK_DELAY=20`：模拟 AI 慢慢写（测实时画面）；`CHUTI_RELAY_AUTO=1`：手动接力自动交回。
4. 截图看界面：沙盒有 Playwright 和 Chromium（`/opt/pw-browsers`），`pg.on('pageerror')` 收集报错。JS 语法：`node -e` 把 `<script>` 里的内容 `new Function(...)` 一下。
5. 直接测函数：`python3 -c "import core as C; C.ensure_repo(); ..."`（在 app 目录里）。

## 五、发布规矩（每次改软件都要照做）

1. 旧版本的 app（git HEAD 里的）整个备份到 `版本备份/v旧版本号/app`；
2. `app/VERSION` 升版本：加功能升中间一位（1.5.0→1.6.0），修小问题升最后一位；
3. `CHANGELOG.md` 最上面加一条：`## v新版本（日期）标题`，几行“- 说明”，最后一行“- 旧版本备份在「版本备份/v旧版本号」”；
4. 提交“单词工作台 v新版本：标题”，推到 main；
5. 跟用户说：Pull、重开软件；左下角会显示新版本号。

`scripts/release.py` 一条命令做完 1–4：`python3 scripts/release.py wv "标题" "说明1" "说明2" [--patch] --token-file 令牌文件`。软件里“让 AI 改软件”发布的版本也照同样规矩（selfup.publish）。

## 六、踩过的坑（别再踩）

- **Windows 不许叫 con/prn/aux/nul/com1…的文件**：词 con 的文件存成 `con_.json`（save_questions.py、core.save_word、pics.save 都照这个）。
- **别往 git 传中文路径参数**（Windows 上可能出问题）：列文件用 `git ls-tree -r -z --name-only HEAD` 再在 Python 里挑；稀疏规则直接写 `.git/info/sparse-checkout`；`git add -A` 不带路径。
- **data\repo 里的 git 命令设了 GIT_CEILING_DIRECTORIES**：副本坏了时，git 会往上找到用户克隆的仓库，在那里查到“0 个文件”还会乱改设置。副本不完整就删掉重克隆（rmtree 要先去只读）。
- **私有仓库没令牌克隆不了**：没填令牌先提示，不让 git 弹窗卡住（GCM_INTERACTIVE=never）。
- **连不上 GitHub**：net_git 依次试 设置里的代理 → 直连 → Windows 系统代理 → 本机代理端口（7890/7892/7897/10809…），通了记进设置；还不通就用本机词库（离线），每 3 分钟重连。
- **浏览器会自动填账号密码框**（填成过 main 和 GitHub 令牌）：密码框都要 `autocomplete="new-password"`。
- **Edge 缓存图标**：换图标要换文件名。
- **模拟 AI 的测试文字别和源码里的原文一样**（改软件的测试会“出现 2 次”）。
- **令牌**：用户在对话里发过好几次，每次都提醒他用完作废；令牌只填在软件设置里（data\config.json），不进 git。旧资料里找到的令牌上传前删掉（GitHub 会拦）。

## 七、做到哪了（2026-11-23，v1.7.0）

- 词库：9,299 行，约 6,244 行有题目，约 3,000 行缺；有画面设置的只有 kit 的 29 个词；视频 0 个登记。
- 用户刚开始用软件出题。出题 AI：sorryios 的 ChatGPT 自动；或者手动接力用 zd87（紫刀 AI）上的 Claude。
- **zd87 不做自动操作**：那是多人合用的 Claude 网页账号池，自动点网页违反 Anthropic 条款。用户问过两次，已经说明了，只做了“手动接力”。想全自动用 Claude 就用 Claude API（接口 AI）。
- 没在真机上测过的：WSL 出片那一整套（同步引擎、装环境、批次）；AI 做的视频画面实际出片效果。

## 八、下一步（用户提过、还没做的）

1. 用户先挑 3 个词做画面、出视频，看质量；按反馈调 pics.py 的提示词（或者照 kit 的写法加更多现成素材）。
2. 视频页在真机跑通：同步引擎 → 装系统软件 → 装声音模型 → 建批次 → 开工。音节划分表（`音节划分_总词库7869词_细分版.xlsx`）两个仓库里都没有，读音拆分要它：请用户放进「词库」。
3. 以后：资料收集（发学习资料给软件，提取、加工、分类，放「词库/资料」）。

## 九、怎么跟用户说话

- 中文，短，先说结论和要他做的事；带版本号、提交号、数字。
- 每次改完：说改了什么（用他的话）、测了什么、没测到什么、他要点哪里。
- 界面文字用大白话；按钮写清做什么（“开始出题”，不要“提交”）。

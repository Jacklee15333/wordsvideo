---
name: local-wordfilm-batch
description: 在用户自己的电脑（WSL2）上批量出“构词动画”视频的流水线：一个单元（比如 7A-U4 的 29 个词）按清单分五个组分工——准备组（画图、起草检查、画风）、配音组、渲染组、质检组、交付组（拷到 D 盘，做好一个就传一个到 GitHub）——不同的词同时在不同的组里做；你当调度：建批次、体检、开工前一次问完用户（等确认）、开工后不再打断用户、盯进度、按事先定的规矩处理卡住的词、看关键画面图、出报告；也可以几个 Claude Code 对话分工（调度、质检、画面组）。用户说“批量出片”“整个单元一起做”“做 7A-U4 全部视频”“流水线”“分工出片”“批量生成视频”时，一定要用这个技能。要先用 local-wordfilm 装好环境。
---

# 本地批量出片（流水线分工）

这个技能在 local-wordfilm 装好的环境上，把一个单元的词排成一条流水线：每个词依次过五个组，几个组同时干活——A 词在渲染时，B 词在配音，C 词在准备。干活、排队、重试都是脚本做；**你当调度**。用户的要求：**批量开工前要问，等用户确认好；开工以后中间不要再问**——所以要用户拿主意的事，全部在第 2 步一次问完；制作中卡住的词按用户事先定的办法处理，每一处都用 `batch.sh note` 记下，最后在报告里一起交代。

## 分工

| 组 | 做什么 | 谁做 |
|---|---|---|
| 准备组 | 画图 → 起草检查（必须“还要补：都齐了”）→ 按序号转画风 → 缩写念全 → 已知的配音修正 | 脚本（同时 1～2 个词） |
| 配音组 | 几个进程一起念，每句用识别模型听一遍；有没听清的就标“要处理” | 脚本（一次 1 个词，2～3 个进程） |
| 渲染组 | 几个浏览器一起渲染 | 脚本（一次 1 个词，4～5 个浏览器） |
| 质检组 | 自动：文件完整、没退回 38 号、没有没听清、没有只有英文的字幕，拼 9 格关键画面图；**人：看关键画面图** | 脚本 + 你（或质检对话） |
| 交付组 | 拷到 `D:\构词视频\<批次>\`；开了上传就马上传到 GitHub，一个一个传 | 脚本 |
| 调度 | 建批次、体检、开工、每 3～5 分钟看进度、处理“要处理”、出报告 | 你 |
| 画面组 | 给没有画面设置、或画面设置过时的词做画面设置（要动脑） | 另开的对话，或你在用户同意后做 |

几个组同时做几个、开几个进程，流水线按 CPU、内存和显卡自动定（`batch.sh status` 第二行会写）。第八十版起配音用上显卡时配音组同时念两个词（`LANE_VOICE`）。第八十一版起画面用显卡编码时，渲染组一次只做一个词、用上尽量多的浏览器（`RENDER_JOBS=0` = 按核数和空闲内存自动定，最多 16 个），一个词先出片；准备组起草时不出预览图（检查没过才出）。`batch.sh status` 会写“速度：平均几分钟出一个”和各组平均用时——用户要的是**一个视频 2 分钟左右**，比这个慢就看哪一组最慢（见 `references/exceptions.md` 第 5 节）。

## 开工前（只做一次）

1. local-wordfilm 的第 1～5 步都做完（WSL、01、02、03 都是 ✅）。有 NVIDIA 显卡的再做它的**第 5.5 步**（`04_gpu.sh`）：配音和画面编码用显卡，内存够的话配音组、渲染组能各开两条道（`batch.sh status` 第二行写着“显卡：…”）。
2. 视频技能最好是**第八十二版（6.38）以上**（能用显卡；传帧也能在显卡上做；一个词用上十几个浏览器一起画；要学的单词没听清时只那一句多念几遍、还不行改美式女声念；kit 补好了 itself、alarm、thermostat），至少第七十九版（6.35）：【WSL】`bash ~/lw/scripts/wsl/02_get_repo.sh`，看最后一行的版本。
3. 把本技能拷进 WSL：`powershell -ExecutionPolicy Bypass -File "<本技能目录>\scripts\windows\sync_batch_to_wsl.ps1"`，最后一行 `SYNC_OK`；再开 keepalive：`powershell -ExecutionPolicy Bypass -File "<本技能目录>\scripts\windows\keepalive.ps1"`（电脑重启后要再开）。
4. 内存（建议）：在 Windows 上跑 local-wordfilm 的 `scripts\windows\set_wsl_memory.ps1`（把 `.wslconfig` 的 memory 调到 24 GB，已有的 `networkingMode=mirrored` 原样保留），确认没有在出片再 `wsl --shutdown`，再开 keepalive。不加也能跑，配音组、渲染组只各开一条道。
5. 告诉用户：批量期间电脑接通电源时别睡眠（设置 → 系统 → 电源）。

【WSL】的意思和 local-wordfilm 一样：PowerShell 里 `wsl -d Ubuntu-24.04 -u root -- bash -lc '命令'`；Git Bash 里前面再加 `MSYS_NO_PATHCONV=1 `。下文 `batch.sh` 都是 `bash ~/lwb/scripts/wsl/batch.sh` 的简写。

## 流程（调度）

1. **建批次、体检**：`batch.sh new 7A-U4 ~/lwb/lists/7A-U4.tsv`。它会逐个词查画面设置和画图脚本，再查环境和分工。把结果告诉用户。第八十版起 kit 已经补好 itself、alarm、thermostat；keep_track_of 的起草检查误报，准备组会自动放行（只差标签、精简版稿子里说到了才放行）。camera、stranger、explore 的画面设置还跟不上规矩（camera 有几幅画是静止的；stranger、explore 的辨析还是自动小图标），会在准备组卡住、要画面组做（`references/exceptions.md` 第 1 节）；别的词不受影响，可以照常开工。
2. **开工前一次问完，等用户确认**（这一步不能省：没确认 `batch.sh start` 会拒绝开工）。在**一条消息**里把下面几件事列给用户，每件都写上建议的答案（括号里是用户 2026-11-18 说过的，已经是 `batch.sh new` 写好的默认值），请用户确认或改：
   1. 要不要上传到 GitHub？（要）放仓库哪个文件夹？（「最新工作版/<批次>」，7A-U4 就是「最新工作版/7A-U4」，以前 01～14 的视频也放在那里）
   2. 视频拷到哪？（`D:\构词视频\<批次>`）
   3. 交付前要不要用户先看？（不用：自动质检过了就交付、上传；你照样看关键画面图，有问题重做、重传覆盖）
   4. 体检里有问题的词怎么办（逐个列出来，比如 7A-U4 的 itself、alarm、thermostat：画面设置过时）：A. 先跳过，最后报告里说；B. 你照 `references/exceptions.md` 第 1 节换成意思最接近的现有动作或图（把打算怎么换写出来给用户看）。
   5. 制作中卡住的词（配音没听清、缺图提示加画图脚本、渲染内存不够……）：A.（建议）你照 `references/exceptions.md` 的规矩自己处理，处理不了的跳过，最后在报告里一起交代；B. 一律跳过，最后报告。
   6. 配音里个别英文单词你的声音多念了还是念不清：（用户 2026-11-19 定了：改成美式女声念）这一句改成中文你的声音 + 英文美式女声拼着念，这个词不会卡住，默认就是这样（`MIX_FALLBACK=1`）；用户想改回第七十七版的规矩才 `batch.sh set 批次 MIX_FALLBACK=0`。报告里会列出哪几句改了。
   7. 要上传的话，开工前先登录 GitHub：`batch.sh login 批次`，Windows 上会弹出登录窗口，请用户登录（以前登录过就不弹）。

   用户确认后：把改动 `batch.sh set` 进去（第 5 条选 B 就 `set 批次 ON_STUCK=skip`），第 4 条的决定照做（或 `skip`），并 `batch.sh note` 记下；最后 `batch.sh set 批次 CONFIRMED=1`。
3. **开工**：`batch.sh start 7A-U4`（后台常驻；做完或都卡住就自己停）。**从这里开始不再问用户问题**，直到第 7 步。
4. **盯进度**：每隔 3～5 分钟 `batch.sh status 7A-U4`，不要让一条命令挂着等。有词交付好了，可以简短说一声（哪个词好了、在哪），但不提问、不等回复。
5. **处理“要处理”“出错”**：`batch.sh log 7A-U4 <词> <阶段>` 看原因，照 `references/exceptions.md` 对应的那一节处理——按第 2 步用户定的办法（`ON_STUCK=fix` 自己处理；`skip` 就跳过），**不问用户**；每处理一处都 `batch.sh note 7A-U4 <词> 说明`（改了哪句、原句和新句、换了哪个动作、为什么跳过）；同一个词处理两轮还过不去就 `skip` 并 note。处理好：`batch.sh retry 7A-U4 <词>`（从卡住的那一组接着做；要从别的组重做就写上组名）。
6. **质检（人看）**：每个过了自动质检的词，打开它的关键画面图（`~/wordfilm-out/7A-U4/<序号> <词>_关键画面.jpg`，Windows 上在拷出去的文件夹里）看一遍：封面有单词和画；读音现象只讲现象；考点 ①②③ 编号、例句另起一行；总结整页出现；没有方框字、缺块、画面错位。有问题就重做（`batch.sh retry 7A-U4 <词> 准备`，或配音、渲染），重传会覆盖仓库里那个文件，并 note；`HOLD_QA=1` 时看过没问题就 `batch.sh ok 7A-U4 <词>` 放行交付。
7. **收尾**：`batch.sh report 7A-U4`（存成 report.md），一次告诉用户：完成几个、每个用了多久、视频在哪、传到了哪；制作中你替用户做了哪些处理（note 都在报告里）；哪些没做和为什么、要用户拿主意的事（这时候才问）。

## 几个对话分工（可选）

进度全在文件里，几个 Claude Code 对话可以同时干不同的活，都通过 `batch.sh` 改进度（不要直接改 state.json）：
- **对话 A：调度**——上面第 1～5、7 步；只有它 `start`、`stop`、`set`。
- **对话 B：质检**——隔几分钟 `batch.sh status`，看新做好的词的关键画面图；没问题 `ok`（`HOLD_QA=1` 时），有问题 `retry <词> 准备/配音/渲染` 并告诉用户。
- **对话 C：画面组**——给“没有画面设置 / 画面设置过时”的词做画面设置：把 `~/kit/words/<词>.py`（和要改的 `<名字>_art.py`）拷到 `~/kit-extra/` 对应位置再改（流水线先用 `~/kit-extra` 的；跑 02 更新视频技能也不会被冲掉），照视频技能 `~/skills/word-construction-video/SKILL.md` 的“做视频 第 2 步”和 `references/pictures.md`。改好告诉调度：`batch.sh retry 7A-U4 <词>`。

## 规矩

1. Linux 命令都在 WSL 里用 root 跑，不用 sudo。
2. 不改视频技能的代码和说明（仓库里按“第…版”管理）；kit 里过时的画面设置也不在原地改，改的放 `~/kit-extra`。
3. 不让用户把 GitHub 令牌贴进对话；上传走 Windows 的 Git 凭据管理器，开工前 `batch.sh login` 先登录好。
4. 做好一个交一个（交付组自动），不等整批。
5. **开工前问完，开工后不问**：要用户拿主意的只在第 2 步（开工前）和第 7 步（收尾）说；中间照用户事先定的规矩处理并 note。
6. 同一个词不要同时用 local-wordfilm 的 make_word.sh 和这条流水线做。
7. 批量期间别关 keepalive。WSL 或电脑重启了：开 keepalive，再 `batch.sh start 7A-U4`，从停下的地方接着做（做了一半的那一组从头做，配音缓存还在）。

## 设置（`batch.sh set 批次 键=值`）

| 键 | 意思 | 默认 |
|---|---|---|
| `UPLOAD` | 1 = 交付时上传到 GitHub | 1（开工前问用户确认） |
| `UPLOAD_DIR` | 传到仓库哪个文件夹 | `最新工作版/<批次>`（开工前问用户确认） |
| `WIN_DIR` | 拷到 Windows 哪里（`/mnt/d/…` 或 `D:\…`） | `/mnt/d/构词视频/<批次>` |
| `HOLD_QA` | 1 = 人看过关键画面图（`ok`）才交付 | 0（开工前问用户确认） |
| `SYNTH_JOBS`、`RENDER_JOBS`、`LANE_PREP` | 配音进程数、渲染浏览器数、准备组同时几个词 | 按 CPU、内存自动 |
| `HEAVY_TOGETHER` | 0 = 配音和渲染不同时跑（内存紧时） | 内存 ≥ 8 GB 时同时跑 |
| `GPU` | 0 = 不用本地的 GPU 补丁 | 1（有补丁就用） |
| `STOP_AFTER` | 做到哪一组就停（比如 `准备` = 只画图、起草，先全单元体检一遍） | 空 |
| `ON_STUCK` | 制作中卡住的词：`fix` = 照 exceptions.md 自己处理（处理不了跳过）；`skip` = 一律跳过 | fix（开工前问用户） |
| `CONFIRMED` | 1 = 用户已经确认第 2 步那几件事；不是 1 不能开工 | 0 |

## batch.sh 命令

`new 批次 清单` 建批次并体检 · `check 批次` 再体检 · `set 批次 键=值…` · `login 批次` · `start 批次`（要先 CONFIRMED=1）· `note 批次 词 说明` · `status 批次` · `log 批次 词 [阶段] [行数]` · `retry 批次 词 [阶段]` · `ok 批次 词` · `skip 批次 词 [原因]` · `reload 批次`（改了清单、加了词）· `stop 批次` · `report 批次` · `list`。阶段名用中文：准备、配音、渲染、质检、交付。

清单格式（Tab 隔开）：`序号	文件夹名	画图脚本（逗号隔开，按先后）	备注`，`#` 开头是注释。见 `lists/7A-U4.tsv`。

## 用户自己跑（不用 AI）

PowerShell 里跑上面“开工前”第 3 步的两条命令，然后 `wsl -d Ubuntu-24.04 -u root` 进 Ubuntu：
```
bash ~/lwb/scripts/wsl/batch.sh new 7A-U4 ~/lwb/lists/7A-U4.tsv
cat ~/wf-batch/7A-U4/config.env                       # 看一眼设置，要改用 batch.sh set
bash ~/lwb/scripts/wsl/batch.sh login 7A-U4
bash ~/lwb/scripts/wsl/batch.sh set 7A-U4 CONFIRMED=1
bash ~/lwb/scripts/wsl/batch.sh start 7A-U4
bash ~/lwb/scripts/wsl/batch.sh status 7A-U4
```
隔一会儿再看 status；“要处理”的按 `references/exceptions.md` 处理，再 `retry`。

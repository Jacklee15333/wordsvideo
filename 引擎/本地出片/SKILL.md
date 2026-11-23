---
name: local-wordfilm
description: 在用户自己的 Windows 11 电脑上（WSL2 里的 Ubuntu 24.04）搭好“构词动画视频”的出片环境并出片——检查 WSL2（装在 D 盘）、装系统软件和字体、从 GitHub 仓库 Jacklee15333/ciyuanchaifeng 取「最新工作版」里最新一版的视频技能和总表、装声音模型、用视频技能 kit 里现成的画面设置出单词的精简版视频（先出 protect 试一个）、检查成片、拷到 D 盘、按用户要求一个一个传回仓库。用户说“在本地出片”“在我电脑上做视频”“搭环境”“跑 protect”“做 7A-U4 的视频”“本地跑构词动画”“把视频传到仓库”时，一定要用这个技能，即使没提 WSL。
---

# 本地出片（Windows + WSL2）

## 省 token（必须遵守；2026-11-19 用户要求，和下面冲突以这里为准）

每来回一次，整段对话都要重新发给模型一遍，所以：**少来回，每次读短的**。

1. **等进度用 `batch.sh wait <批次> 30`**：在 WSL 里等，有词做完、卡住、流水线停了才回来（最多 30 分钟），只打几行。不要每几分钟查一次 status，不要开“每 N 分钟汇报”的后台监控 / 定时任务。用户要定时汇报，间隔不少于 30 分钟（就是 `wait <批次> 30`）。
2. **看进度 `batch.sh status <批次>`**（三行）。整张表 `status <批次> full` 只在用户要、或者要找某个词的时候用。
3. **日志只看尾巴**：`batch.sh log <批次> <词> <阶段> 20`，不要 cat 整个日志。02 / 03 / 04、同步这类长命令，把输出写到文件，只看最后 3 行（`… > x.log 2>&1; tail -n 3 x.log`），出错了再多看几行。
4. **不要 `ps` 打完整命令行**（浏览器一条就几百字）。看电脑用 `monitor.ps1 -Report -Short`（一行）。
5. **后台任务等完成通知**，不要反复去读输出文件。
6. **给用户汇报不超过 5 行**：说结论和要用户做的事，不复述命令输出、不贴表；用户说“原样贴”才贴。
7. **说明读一次就够**：这份 SKILL.md 和 references 读过就别再读；视频技能的 SKILL.md 很长，不要读，遇到问题只看 references 里对应的那一节。
8. **对话长了就换**：一批做完、或者对话已经很长，建议用户新开一个对话（或 `/compact`）再接着做，上下文短了每次都省。

你（Claude Code，跑在用户的 Windows 电脑上）用这个技能在 WSL2 的 Ubuntu 里出“构词动画”视频。真正出片的是仓库里的视频技能（word-construction-video）；本技能的脚本负责装环境、取最新版、按固定顺序跑、检查、拷出、上传。**出片本身不用你动脑：照步骤跑脚本、等、看结果、跟用户说。**

用户的电脑：Intel Core Ultra 7 265K（20 核）、32 GB 内存、RTX 5060 Ti（第八十版起配音和画面编码可以用显卡，见第 5.5 步）。C 盘只剩约 74 GB，所以 WSL 放 D 盘，做好的视频拷到 `D:\构词视频\`。

## 先记住这几条

1. **Linux 命令都在 WSL 里用 root 跑，不用 sudo**（你没法输密码）。下文写【WSL】的，按你用的终端这样包一层：
   - PowerShell：`wsl -d Ubuntu-24.04 -u root -- bash -lc '命令'`
   - Git Bash：`MSYS_NO_PATHCONV=1 wsl -d Ubuntu-24.04 -u root -- bash -lc '命令'`（不加 `MSYS_NO_PATHCONV=1`，`/root/…` 会被改成 `C:/Program Files/Git/root/…`）
2. **久的活一律放后台**：装环境、下模型、出片都用 `bg.sh start`，然后每隔 3～5 分钟 `bg.sh status` 看一次。不要让一条命令挂着等十几分钟。放后台之前先开 keepalive（第 2 步），不然 Windows 这边没有 wsl 进程时 WSL 会自己关掉，后台的活跟着停。
3. **每一步看最后一行**：`✅` 才往下走；`❌` 照提示或 `references/troubleshooting.md` 处理，处理不了就把那几行原样告诉用户。
4. **不要让用户把 GitHub 令牌贴进对话**，也不要把令牌写进命令或文件。上传用 Windows 的 Git 凭据管理器登录（第 8 步）。
5. **不改视频技能的代码和说明**：它在仓库里按“第…版”管理，改了要出新版本，用户说了才做。
6. 工作文件都放在 WSL 自己的盘里（`~`），不要放 `/mnt/c`、`/mnt/d`（跨系统读写很慢）；做好的视频用 copy_out.sh 拷出来。
7. 用户的习惯：**做好一个就交一个**（拷出来；要上传的马上传），不要等一批全做完。

## 第 1 步：检查 WSL（Windows 这边）

```
powershell -ExecutionPolicy Bypass -File "<本技能目录>\scripts\windows\check_wsl.ps1"
```
`<本技能目录>` 是这个 SKILL.md 所在的文件夹。看最后一行 `RESULT:`：
- `OK`：往下走。
- `NO_WSL` 或 `NO_DISTRO`：脚本会打印要**用户本人**做的命令（管理员权限，可能要重启，装完 Ubuntu 会弹窗让设用户名和密码）。把这几行原样给用户，等用户说装好了，再跑一次第 1 步。
- `ON_C`：Ubuntu 在 C 盘。把脚本打印的“挪到 D 盘”的命令给用户看，**用户同意后**再一条一条跑，每条成功了再跑下一条。
- `WSL1`：跑 `wsl --set-version Ubuntu-24.04 2`（几分钟），再跑第 1 步。

## 第 2 步：把本技能的脚本拷进 WSL，开 keepalive

```
powershell -ExecutionPolicy Bypass -File "<本技能目录>\scripts\windows\sync_to_wsl.ps1"
powershell -ExecutionPolicy Bypass -File "<本技能目录>\scripts\windows\keepalive.ps1"
```
第一条最后要有 `SYNC_OK`：脚本拷到 WSL 的 `~/lw`，顺手换掉 Windows 换行符。本技能文件夹有更新就再跑一次。
第二条在后台挂一个不占资源的 wsl 进程，WSL 就不会自己关；电脑重启后要再跑一次，想关掉加 `-Stop`。

## 第 3 步：装系统软件、字体、浏览器（10～20 分钟）

【WSL】`bash ~/lw/scripts/wsl/bg.sh start boot bash ~/lw/scripts/wsl/01_bootstrap.sh`

- 默认 apt、pip 用清华源。GitHub 慢、下载失败时要用代理：命令最后加 ` --proxy http://地址:端口`（WSL 里的代理地址见 troubleshooting.md 第 1 节）。代理会记下来，后面的脚本自动用。
- 看进度：【WSL】`bash ~/lw/scripts/wsl/bg.sh status boot`，等最后一行 `✅ 01 完成`。
- 字体会配成和以前云端出片一样（英文 Cambria → Caladea，中文 Noto Sans CJK SC），这样视频和仓库里的样本长得一样。

## 第 4 步：取仓库里的最新版（1～3 分钟，直接跑）

【WSL】`bash ~/lw/scripts/wsl/02_get_repo.sh`

自动找「最新工作版」里编号最大的“第…版”，只下总表、视频技能和音节表（不下归档里的视频），解开视频技能到 `~/skills/word-construction-video`。最后一行 `✅ 02 完成：第…版（视频技能 6.xx）`。仓库出了新版就再跑一次。

## 第 5 步：装声音模型（约 1.6 GB）

【WSL】`bash ~/lw/scripts/wsl/bg.sh start models bash ~/lw/scripts/wsl/03_models.sh`

要看到 `声音：✅ …`、`准备好了`、`✅ 03 完成`。断了就再 start 一次，会接着下；下不动见 troubleshooting.md 第 2 节。

## 第 5.5 步：开显卡（可选；视频技能第八十版起；约 2.5 GB、10～20 分钟）

【WSL】`bash ~/lw/scripts/wsl/bg.sh start gpu bash ~/lw/scripts/wsl/04_gpu.sh`

它在单独的 Python 环境 `~/wf-gpu` 里装显卡版的 sherpa-onnx（CUDA 12）、onnxruntime-gpu 1.26 和 NVIDIA 的 CUDA 12 库（不动系统里原来的），再跑 `gpu_check.py`：配音三路（声音克隆、英文、识别检查）在 CPU 和显卡上各念几句比一比，显卡上念得对、快 15% 以上才用；三路放一个进程里再一起试一遍；最后试画面的显卡编码（NVENC）。第八十一版起还量画面：浏览器画画面（CPU 和四种显卡接法各画 protect 中间 240 帧），每种接法量两条传帧的路——浏览器压 JPEG（老办法）和显卡转 NV12 直接交给编码器（第八十二版）；显卡画出来要和 CPU 画的几乎一样才算数；再量 CPU / 显卡编码多快、显卡最多同时编码几路，按这台电脑能开几个浏览器估每种组合，挑整体最快的，估一个 5 分钟的视频画面要多久。测好写进 `~/.wordfilm-gpu.env`，打印几张表（每一项 CPU 多快、显卡多快、用哪个；最后是“估计：…”），最后一行 `✅ 04 完成：用显卡的有 …`。**把这几张表原样告诉用户**——用户要的是一个视频 2 分钟左右，表里看得出时间花在哪。

- 以前做实验装在系统里的 onnxruntime-gpu 1.32 + CUDA 13 库不用管（这里用不到）；`gpu_patch.sh` 第八十版起删了，视频技能自己会用显卡。
- 关掉显卡：`bash ~/lw/scripts/wsl/04_gpu.sh --off`；换了驱动、更新了视频技能后重测：`bash ~/lw/scripts/wsl/04_gpu.sh --check`；临时不用：命令前加 `GPU=0`。
- 浏览器画画面：WSL 里浏览器能不能用显卡要看驱动，`gpu_check.py` 挨个试，用得上又画得一样才开（日志里有“浏览器没用上显卡”就是那一次自动改回 CPU 画）。用不上也不要紧：显卡编码把 CPU 让给浏览器，第八十一版起一个词用上十几个浏览器一起画。
- 内存：WSL 默认只能用一半内存（15 GB 左右）。批量出片想让配音、渲染各开两条道，在 **Windows** 上跑 `powershell -ExecutionPolicy Bypass -File "<本技能目录>\scripts\windows\set_wsl_memory.ps1"`（只改 `.wslconfig` 的 memory 一行，调到 24 GB），确认没有在出片再 `wsl --shutdown`、重新开 keepalive。

## 第 6 步：出 protect 试一个

【WSL】`bash ~/lw/scripts/wsl/bg.sh start protect bash ~/lw/scripts/wsl/make_word.sh protect 16 explore,shower,itself,protect`

脚本分 6 步打印进度：画图 → 起草检查（必须“还要补：都齐了”）→ 转画风（16 号是中西合璧风）→ 缩写念全 → protect 已知的两处配音修正 → 配音和渲染。最后一步最久；`bg.sh status protect` 会显示“配音：念好 X / 共 Y 段”，念完以后是“画面 N / M 段”。最后一行 `✅ 做好了：…/16 protect.mp4`。

配音那一步开始时打印一行 `显卡：声音克隆 …、英文 …、识别 …、画面编码 …`（第 5.5 步测好的；没做第 5.5 步就是“没开”，全用 CPU，照样能出片）。第八十版起要学的单词没听清时视频技能自己把那一句多念几遍；改了稿子再跑同一条命令，只重念改过的和没听清的句子。

做好以后：
1. 【WSL】`bash ~/lw/scripts/wsl/check_video.sh protect`：查文件完整；退回 38 号念的句子要是 0；只有英文的字幕要是 0；再拼一张 9 格的关键画面图。**用你读图片的功能打开这张图看一遍**（它会打印 Windows 路径）：封面第一帧有单词和画；考点两页有 ①②③ 编号，例句另起一行；总结整页出现；没有缺块、方框字。
2. 【WSL】`bash ~/lw/scripts/wsl/copy_out.sh protect`：拷到 `D:\构词视频\7A-U4\`。
3. 跟用户说：用了多长时间、视频多长、检查结果、Windows 上的路径，请用户和仓库「最新工作版」里最新版本文件夹的 protect 样本对比一下。

## 第 7 步：做别的词

**kit 里有现成画面设置的词**（`~/kit/words/<词>.py` 存在的，7A-U4 的二十九个词）：
- 命令和第 6 步一样，换三样：文件夹名、序号、画图脚本。查 `references/kit_words.md`：每个词的画图脚本和先后、已知的序号。
- **序号**决定画风和文件名。表里标“推测”的、没写的，**先问用户**，不要猜。
- 第 1 步报“缺图”时，脚本会提示“可能要加画图脚本 …”，把它加到前面再跑。
- 可以同时跑 2～3 个词（每个约占 3 GB 内存），`bg.sh` 用各自的词当名字。
- 有的词要先手改一句配音（表里写了）：先跑 `make_word.sh … --no-run`，照表改好，再跑一次不带 `--no-run` 的（手改过的配音稿不会被覆盖）。

**kit 里没有的词**：要先写画面设置和插图脚本，这是要动脑的部分，照 `~/skills/word-construction-video/SKILL.md` 的“做视频 第 2 步”和它的 `references/pictures.md` 做，动手前先和用户确认。本技能不包这一块。

**详解版**：本技能只出精简版（用户现在主要要这个）。要详解版先问用户，再照视频技能 SKILL.md 用 `--edition detail` 跑。

## 第 8 步：上传到仓库（用户要的时候；做好一个传一个）

【WSL】`bash ~/lw/scripts/wsl/upload.sh "<本地文件>" [仓库里的文件夹] [文件名]`

- 默认放进「最新工作版/<最新版>」，文件名不变。文件夹、文件名照用户说的写；用户以前的命名：样本 `protect_精简版样本_第七十八版.mp4`，单元视频 `16 protect.mp4`。
- 第一次推送会在 Windows 上弹出 GitHub 登录窗口：跑之前先告诉用户“请在弹出的窗口里登录 GitHub”。
- 只新增或更新这一个文件；推送前先对齐远端最新，不动仓库里别的东西。
- 想自己写提交说明：命令前面加 `MSG='…' `。

## 用户自己跑（不用 AI）

在 PowerShell 里跑第 1、2 步的命令；然后 `wsl -d Ubuntu-24.04 -u root` 进到 Ubuntu，依次输：
```
bash ~/lw/scripts/wsl/01_bootstrap.sh
bash ~/lw/scripts/wsl/02_get_repo.sh
bash ~/lw/scripts/wsl/03_models.sh
bash ~/lw/scripts/wsl/make_word.sh protect 16 explore,shower,itself,protect
bash ~/lw/scripts/wsl/check_video.sh protect
bash ~/lw/scripts/wsl/copy_out.sh protect
```
出片时窗口别关；关了就再跑同一条命令，念好的配音会接着用。

## 出错了

看 `references/troubleshooting.md`：网络和代理、模型手动下载、浏览器下载、配音“没听清”、起草没过、WSL 自己关了、内存、上传登录、换行符、字体、视频技能出了新版。

## 盯着电脑：CPU、显卡、内存、温度（2026-11-19 加，用户要求）

`scripts\windows\monitor.ps1`（**Windows** 上跑）每 10 秒记一行：CPU 占用、内存（含 WSL 占的）、显卡占用 / 显存 / 温度 / 功耗 / 编码路数、CPU 温度，记到 `%USERPROFILE%\wordfilm-monitor.csv`（Excel 能直接打开）。

- **开始记**（放后台一直记，出片、批量一开工就开）：`powershell -ExecutionPolicy Bypass -File "<本技能目录>\scripts\windows\monitor.ps1"`。已经在记会说“已经在记了”，不会开两份。
- **看汇总**：`powershell -ExecutionPolicy Bypass -File "<本技能目录>\scripts\windows\monitor.ps1" -Report -Minutes 5`：最近 5 分钟每一样的平均 / 最高，超标会写 ⚠。
- **停**：`… monitor.ps1 -Stop`。
- **CPU 温度**：Windows 自己不给。要用户装 LibreHardwareMonitor（GitHub 上 LibreHardwareMonitor/LibreHardwareMonitor 的 Releases 下 zip，解压到 `D:\tools\LibreHardwareMonitor`），**右键以管理员身份运行**，最小化开着；可以帮用户下载解压，管理员确认要用户自己点。下载 Releases 里的 `LibreHardwareMonitor.zip`（不要 `.NET.10` 那个，那个要另装 .NET 10）。**0.9.6 起它没有 WMI 选项**：要用户在它的菜单 `Options → Remote Web Server → Run` 打开网页接口（默认 8085 端口，它会记住，下次打开还是开着），monitor.ps1 从 `http://localhost:8085/data.json` 读 CPU Package 温度。没开它，汇总里 CPU 温度写“没读到”，别的照记。
- **汇报**：用户要看时、每次汇报出片进度时，附上 `-Report -Short` 那一行（省 token）。
- **超标怎么办**（用户 2026-11-19 同意“温度偏高再把浏览器数调小”）：
  - CPU 到过 100°C，或者连续两次汇总都到过 95°C：`batch.sh set <批次> RENDER_JOBS=8`（渲染最多 8 个浏览器，慢十几秒，CPU 少用约三分之一），再告诉用户。降下来以后不用自己改回去，问用户。
  - 内存到过 95%：先告诉用户关掉不用的程序（抖音、QQ 浏览器、千问……）；连续两次还是这样，`RENDER_JOBS=8`，告诉用户。
  - 显卡到过 85°C：告诉用户看看机箱通风。
  - 别的情况只汇报，不改设置。

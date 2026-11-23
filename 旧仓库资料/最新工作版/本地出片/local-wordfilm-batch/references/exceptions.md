# 卡住了怎么办（按组）

先 `batch.sh log 批次 词 阶段` 看最后几行，再找下面对应的一节。处理好以后 `batch.sh retry 批次 词`（从卡住的那一组接着做）。

**制作中不问用户**：用户要求开工后不再打断。按开工前定的 `ON_STUCK` 办：`fix` = 照下面的规矩自己处理；`skip` = `batch.sh skip`。**每一处处理都 `batch.sh note 批次 词 说明`**（原来什么样、改成什么样、为什么），收尾时报告里一起交代。开工后遇到开工前没问到、又要用户拿主意的事，就 skip 并 note，留到收尾再说。同一个词处理两轮还过不去，skip 并 note。

1. 准备组：缺图、画面设置过时、起草检查没过、没有画面设置
2. 配音组：没听清、退回 38 号
3. 渲染组：出错
4. 质检组：没过
5. 交付组：上传失败
6. 流水线停了
7. 改清单、加词
8. 内存、速度

## 1. 准备组

- **缺图，提示“可能要加画图脚本 X”**：清单里这个词的画图脚本少了 X 或先后不对。改 `~/wf-batch/<批次>/list.tsv` 这一行（把 X 加在前面），`batch.sh retry 批次 词`（retry 会读新清单）。
- **缺图，提示“会动的人……现在的动作表里没有它（kit 的画面设置过时了）”**：kit 的画面设置用了一个已经不存在的动作。这要画面组处理：把 `~/kit/words/<词>.py` 拷到 `~/kit-extra/words/<词>.py`，把那个动作换成提示里列出的现有动作之一（选意思最接近的；开工前用户同意过的方案就照做），保存后 retry，并 note。用户开工前选了“跳过”，或者开工前没问到：skip 并 note。
- **缺图，提示“没找到是哪个画图脚本画的”**：画面设置要的图（比如图标）现在没有脚本画了。画面组处理：在 `~/kit-extra/words/<词>.py` 里换成现有的图，或者照视频技能 `references/pictures.md` 补一个画图脚本放 `~/kit-extra/`。
- 7A-U4 已知（2026-11-18 逐个画过一遍）：
  - **itself**：`cn-boy-mirror` 动作没有了，现有的有 `cn-boy-self`、`cn-boy-raise`。
  - **alarm**：`cn-boy-drum`、`cn-girl-drum`、`west-man-scared` 三个动作没有了（`cn-girl-wake` 由 alarmclock 画，清单已经加上）。现有的：cn-boy 有 guard、raise、wake；west-man 有 hello、point、present、shout、smile、speech。
  - **thermostat**：`icon-stat`、`icon-thermo` 两个图标没有脚本画。
- **起草检查没过**（“还要补”不是“都齐了”）：不要硬做（不加 --force-draft）。skip 并 note 那一行原文，收尾时告诉用户。
- **没有画面设置**（清单里的词 `~/kit` 和 `~/kit-extra` 都没有 `words/<词>.py`）：新词，画面组先做；或者 `batch.sh skip 批次 词`。

## 2. 配音组

**第八十版起先看这里**：视频技能自己会把没听清的那一句多念最多 8 遍（语速轮着放慢一点），日志里写“这一句再念最多 8 遍”。还是没听清才停下来标“要处理”。用户开工前选了 `MIX_FALLBACK=1` 的，这一句会自动改成中文你的声音 + 英文美式女声，不会停下来。改了稿子再 retry：只重念改过的和没听清的句子，几十秒就好，不用等整个词重念。下面的两招（英文词后加冒号 / 加“这个词”“这三个词”）照样能用。


- **有句子没听清**：日志里列了是哪几句。在 `~/wordfilm-work/<词>/brief/plan.json`（`scenes` 下面各幕的 `segs`）找到这一句，换个说法，意思不变、**不改画面上的字**。好用的两招：
  - 英文单词后面接冒号：“shield 这个词，是挡住……” → “shield：挡住、保护，就是……”
  - 一串英文词后面加几个中文字再接下文：“从 protect、provide、produce 中选一个” → “从 protect、provide、produce，这三个词中选一个”

  只用这两招、意思不变、不碰画面上的字，不问用户；note 原句和新句。改好 `batch.sh retry 批次 词 配音`（念好的句子会复用，只重念改过的）。更多说法见视频技能 `references/narration-guide.md` 第五节。
- **退回 38 号**：声音克隆没装好或参考录音找不到。按 local-wordfilm 跑一次 03（`bash ~/lw/scripts/wsl/03_models.sh`），再 retry。

## 3. 渲染组

出错会自动再试一次。还不行：看日志。返回码 -9 或 “Killed” 多半是内存不够，`batch.sh set 批次 RENDER_JOBS=2`（或 `HEAVY_TOGETHER=0`）再 `retry 批次 词 渲染`。日志写“先不渲染”：是配音有句子没听清，按第 2 节处理。

## 4. 质检组

日志里写了哪一项没过：
- 解码有错误、时长不对：`retry 批次 词 渲染`。
- 退回 38 号、没听清：按第 2 节。
- 有只有英文的字幕：视频技能的毛病（第七十八版起不该有），把那条字幕和词告诉用户。
- 人看关键画面图发现问题：告诉用户，按问题从准备、配音或渲染重做（`retry 批次 词 准备`）。

## 5. 交付组

- **上传**：开工前 `batch.sh login` 已经登录好。制作中还是登录失败（比如登录过期）：不问用户，让交付组卡着（视频照样拷到 D 盘了），别的词照做；note 一下，收尾时请用户登录，再对每个卡在交付的词 `retry 批次 词 交付`。
- **没找到 Git 凭据管理器**：装 Git for Windows；或者请用户自己在 Ubuntu 窗口里做一次（令牌只在用户自己的窗口里粘贴，**不要贴进对话**）：`git config --global credential.helper store`，然后 `retry`，推送时问 Username 填 GitHub 用户名、Password 粘贴令牌。
- **拷到 Windows 失败**：看 `WIN_DIR` 对不对（`/mnt/d/…`），D 盘在不在。
- 网络慢、推不上去：按 local-wordfilm 的 troubleshooting 第 1 节配代理。

## 6. 流水线停了

`batch.sh status` 第一行写“没在跑”：
- 都做完或都卡住了，流水线自己停了——正常，处理卡住的再 retry（retry 会自动开工）。
- WSL 被关了、电脑重启了：开 keepalive，再 `batch.sh start 批次`。做到一半的那一组从头做，缓存都在。

## 7. 改清单、加词

编辑 `~/wf-batch/<批次>/list.tsv`（不是 `~/lwb/lists/` 里的模板），然后 `batch.sh reload 批次`：新加的词排到最后；改过画图脚本的，下次做这个词时用新的（已经卡住的要 retry）。

## 8. 内存、速度

`batch.sh status` 第二行是现在的分工。进程被系统停掉（返回码 -9）就少开几个：`batch.sh set 批次 SYNTH_JOBS=2 RENDER_JOBS=3`；还不行 `HEAVY_TOGETHER=0`（配音、渲染轮流跑）。给 WSL 更多内存（`.wslconfig` 的 `memory=24GB`）能开得更多。


## 5. 太慢（第八十一版起：用户要一个视频 2 分钟左右）

`batch.sh status` 的“各组平均”看哪一组最慢——流水线几组同时干活，出片速度由最慢的那一组定：
- **配音最慢**：看配音日志开头的“设备（6.36）”，声音克隆要是 cpu，显卡没用上：跑 local-wordfilm 的 `04_gpu.sh --check`，把表给用户看；用上了还慢，`batch.sh set 批次 LANE_VOICE=2`（配音组同时念两个词）。
- **渲染最慢**：看渲染日志“画面：N 个浏览器一起渲染（…编码：…）”。编码是 CPU libx264：显卡编码没开（`04_gpu.sh --check`）；浏览器个数少：多半是 WSL 内存不够（`set_wsl_memory.ps1` 调到 24 GB）。日志里有“浏览器没用上显卡”的，按 gpu_check 的结论办。
- **准备最慢**（很少见）：`batch.sh set 批次 LANE_PREP=2`。
- 都改了还是慢，把 `batch.sh status` 和 `04_gpu.sh --check` 的表原样告诉用户。

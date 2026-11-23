# 出错了怎么办

1. 网络和代理
2. 声音模型下不动（手动下载）
3. Chromium 下载失败
4. 配音“没听清”、没有渲染
5. 起草检查没过（不是“都齐了”）
6. WSL 自己关了、后台的活没了
7. 内存不够
8. 上传：登录 GitHub
9. `$'\r': command not found`
10. 画面里的字是方框、字体和以前不一样
11. 视频技能出了新版

## 1. 网络和代理

apt、pip 默认走清华源（01 里换好了）。GitHub 上的东西（仓库、声音模型、Chromium）在国内可能很慢或下不动，这时用代理。
用户 Windows 上开着代理软件（比如端口 7890）时，WSL 里这样用：
- **方法 A（推荐）**：在 `C:\Users\<用户名>\.wslconfig` 里加（文件已经有就加这两行，不要整个覆盖；这个设置对所有 WSL 系统都生效）：
  ```
  [wsl2]
  networkingMode=mirrored
  ```
  然后 PowerShell 跑 `wsl --shutdown`，再跑第 2 步的 keepalive。代理地址就是 `http://127.0.0.1:7890`。
- **方法 B**：不改设置，代理软件里打开“允许局域网连接”，WSL 里用 Windows 的地址：【WSL】`ip route show default | awk '{print $3}'` 得到 IP，代理是 `http://<IP>:7890`。

然后【WSL】`bash ~/lw/scripts/wsl/01_bootstrap.sh --proxy http://…`。代理会记在 `~/.wordfilm-local.env`，后面的脚本自动用；不想用了就删掉那个文件里 `PROXY=` 那一行。

## 2. 声音模型下不动（手动下载）

在 Windows 上用浏览器（可以开代理）下载这几个文件，放进 `D:\模型下载\`：
```
https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/sherpa-onnx-zipvoice-distill-fp32-zh-en-emilia.tar.bz2
https://github.com/k2-fsa/sherpa-onnx/releases/download/vocoder-models/vocos_24khz.onnx
https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/lexicon-en-us.txt
https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-multi-lang-v1_0.tar.bz2
https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17.tar.bz2
https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-multi-lang-v1_1.tar.bz2
https://github.com/lxgw/LxgwWenKai/releases/download/v1.530/LXGWWenKai-Regular.ttf
```
然后【WSL】（一条一条跑）：
```
M=~/wordfilm-models; mkdir -p $M/.done
cp /mnt/d/模型下载/*.tar.bz2 $M/
cp /mnt/d/模型下载/vocos_24khz.onnx /mnt/d/模型下载/lexicon-en-us.txt $M/
date > $M/.done/vocos_24khz.onnx; date > $M/.done/lexicon-en-us.txt
mkdir -p ~/.local/share/fonts && cp /mnt/d/模型下载/LXGWWenKai-Regular.ttf ~/.local/share/fonts/ && fc-cache -f
```
再跑第 5 步：压缩包它会自己解压、检查。两个单个文件一定要写 `.done` 标记，不然 setup.sh 会删掉重下。

## 3. Chromium 下载失败

01 会先从官方地址下，不行再换两个国内镜像。都不行就按第 1 节配代理，再跑 01。

## 4. 配音“没听清”、没有渲染

视频技能会把配音每一句用识别模型听一遍，要学的单词没听清就重念，4 遍都不行就停下不渲染，日志里会写是哪一句。处理：
1. 在 `~/wordfilm-work/<词>/brief/plan.json` 里找到这一句（`scenes` 下面各幕的 `segs`），换个说法，意思不变，**不改画面上的字**。好用的两招（protect 就是这样修好的）：
   - 英文单词后面接冒号：“shield 这个词，是挡住……” → “shield：挡住、保护，就是……”
   - 一串英文词后面加几个中文字再接下文：“从 protect、provide、produce 中选一个” → “从 protect、provide、produce，这三个词中选一个”
2. 改之前把原句和改后的句子给用户看。
3. 再跑同一条 make_word.sh：手改过的配音稿不会被覆盖，念好的句子直接复用，只重念改过的。

更多说法见视频技能的 `references/narration-guide.md` 第五节。

## 5. 起草检查没过（不是“都齐了”）

把“还要补：……”这一行原样告诉用户，不要加 `--force-draft` 硬做（除非用户同意）。“缺图”时脚本会提示可能要加的画图脚本。

## 6. WSL 自己关了、后台的活没了

- 先跑第 2 步的 keepalive。
- 批量出片时，Windows“设置 → 系统 → 电源”里把接通电源时的睡眠改成“从不”，不然电脑睡着了也会停。
- 停了不要紧：再 `bg.sh start` 同一条命令，配音缓存还在，接着做。

## 7. 内存不够

WSL 默认最多用一半内存（16 GB）。每个词出片约占 3 GB，同时跑 3 个没问题。要跑更多，在 `.wslconfig` 的 `[wsl2]` 下面加 `memory=24GB`，再 `wsl --shutdown`。

## 8. 上传：登录 GitHub

upload.sh 用 Windows 的 Git 凭据管理器（装了 Git for Windows 就有），第一次推送弹窗登录。
没有 Git for Windows 时，请用户自己在 Ubuntu 窗口里做一次（令牌只在用户自己的窗口里粘贴，**不要贴进任何对话**）：
```
git config --global credential.helper store
bash ~/lw/scripts/wsl/upload.sh "<文件>"
```
问 Username 填 GitHub 用户名，问 Password 粘贴 GitHub 令牌。之后会记住（存在 `~/.git-credentials`，是明文，只在这台电脑上）。

## 9. `$'\r': command not found`

脚本带了 Windows 换行符。再跑一次第 2 步的 `sync_to_wsl.ps1`（它会换掉）。

## 10. 画面里的字是方框、字体和以前不一样

再跑 01（会重装字体、重写字体设置）。不要把 Windows 的字体（微软雅黑、Cambria）加进 WSL：加了画面会和以前云端出的视频不一样。

## 11. 视频技能出了新版

再跑 02，会换成新版的视频技能和总表；已经做好的视频不受影响，新做的按新版。`fixes/protect.py` 只认原来的两句说法，新版起草的说法变了，它会打印“没有要改的”，这不是错误。


## 12. 显卡（第八十版起）

- **`04_gpu.sh` 第 1 步说看不到显卡**：WSL 里 `nvidia-smi` 要能看到 RTX 5060 Ti。看不到就在 Windows 上更新 NVIDIA 驱动（WSL 不用另外装驱动），再 `wsl --shutdown` 重开。看不到也能出片，全用 CPU。
- **sherpa-onnx 显卡版没装上**：显卡版要和系统里的 sherpa-onnx 同一个版本号（`${版本}+cuda12.cudnn9`），从 `k2-fsa.github.io/sherpa/onnx/cuda-cn.html` 或 `cuda.html` 下（文件在 huggingface / hf-mirror）。下不动就开代理再跑；还不行，声音克隆和识别检查就用 CPU，英文和画面编码照样能用显卡。
- **表里某一项写“出错”**：那一项就用 CPU，不影响出片。把那一行的报错原样告诉用户。常见的是缺某个 CUDA 12 的库（再跑一遍 `04_gpu.sh` 会接着装）。
- **“三路一起跑”写“冲突，…退回 CPU”**：两套 onnxruntime 同时用显卡打架了，脚本已经把一路退回 CPU，不用管。
- **出片日志里有“提醒：显卡编码（NVENC）出错了…改用 CPU”**：这个词自动改用 CPU 渲染画面，照样出片；经常出现就把 `~/.wordfilm-gpu.env` 里的 `WORDFILM_ENCODER=nvenc` 改成 `x264`。显卡同时编码的路数有限，默认最多 3 路（`WORDFILM_NVENC_SLOTS`）。
- **想全关**：`bash ~/lw/scripts/wsl/04_gpu.sh --off`；`~/wf-gpu` 文件夹删掉也行（`rm -rf ~/wf-gpu`），系统里原来的程序没动过。

## 13. WSL 起不来、Ubuntu 是空壳（2026-11-18 用户电脑上遇到过）

- **WSL 起不来，说虚拟化没开**：Windows 的启动设置里虚拟化被关了。管理员 PowerShell：`bcdedit /set hypervisorlaunchtype auto`，重启电脑。
- **Ubuntu 打开就退出、或者在 C 盘上什么都没有**：是个空壳。`wsl --unregister <名字>` 注销（会删掉里面的东西，先确认里面没有要的），再按第 1 步装到 D 盘。
- **WSL 内存不够（出片进程被停掉，返回码 -9）**：跑 `scripts\windows\set_wsl_memory.ps1` 调到 24 GB，或者批量时少开几个进程（`batch.sh set 批次 SYNTH_JOBS=1 RENDER_JOBS=2`）。

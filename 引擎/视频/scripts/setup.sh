#!/usr/bin/env bash
# 一次性准备（每个新对话第一次用的时候跑；3～5 分钟；装好的会跳过，没装完的接着装）
#   bash setup.sh           装（可以放后台：setsid nohup bash setup.sh > ~/setup.log 2>&1 &，再看 ~/setup.log）
#   bash setup.sh --check   只检查，不下载（几秒）
# 最后一行是“声音：✅ …”才算好；“声音：❌ …”就再跑一遍（下载接着下，解压从头来）。退出码：0 = 都好了，1 = 还缺东西。
#
# 6.9 起（第四十六版）为什么这样写：以前只看模型文件夹在不在。477 MB 的 decoder.onnx 解压到一半命令被停掉，
# 再跑一遍就当成“已经有了”跳过，最后还说“声音克隆：准备好了”，合成时却悄悄整段改用 38 号念。现在：
#   - 下载先存成 .part，断了接着下（curl -C -），下完才改名；
#   - 解压到临时文件夹，tar 成功了才挪到位，再写完成标记 $MODELS/.done/<名字>；没有标记的文件夹当没装完，删掉重装；
#   - 先装你的声音（ZipVoice + 声码器 + 英文音标词典），再装英文声音 af_heart（Kokoro v1.0）、识别模型、Kokoro v1.1（词典）；
#   - 最后的检查和 synth.py、run.py 用同一个函数（voice_config.voice_problems），说好了就真的好了。
# 装什么：Python 包 sherpa-onnx、soundfile、numpy、scipy、noisereduce、pypinyin、praat-parselmouth、openpyxl、pillow、playwright、espeakng-loader（6.17）；
#   声音克隆 ZipVoice 蒸馏版 fp32（约 456 MB；装不上用 int8 版 104 MB）+ Vocos 声码器（54 MB）+ 英文音标词典（6 MB）；
#   英文声音 Kokoro v1.0（af_heart，约 350 MB）；识别模型 SenseVoice（约 165 MB）；Kokoro v1.1（音标词典，约 365 MB）；霞鹜文楷字体。
set -u
MODELS=${WORDFILM_MODELS:-$HOME/wordfilm-models}
HERE=$(cd "$(dirname "$0")" && pwd)
DONE="$MODELS/.done"
mkdir -p "$MODELS" "$DONE"
say() { printf '%s\n' "$*"; }
REL=https://github.com/k2-fsa/sherpa-onnx/releases/download

fetch() {   # 下载地址 存到哪（先存 .part，断了接着下）；成功返回 0
  local url=$1 dest=$2
  [ -s "$dest" ] && return 0
  for try in 1 2; do
    if curl -fsSL --retry 3 --retry-delay 2 --max-time 1200 -C - -o "$dest.part" "$url"; then
      mv -f "$dest.part" "$dest"; return 0
    fi
    rm -f "$dest.part"          # 断点续不上（比如上次其实已经下完了）：从头下一遍
  done
  return 1
}

get() {   # 模型文件夹名 下载地址
  local name=$1 url=$2 arc="$MODELS/$1.tar.bz2" tmp="$MODELS/.tmp-$1"
  if [ -f "$DONE/$name" ] && [ -d "$MODELS/$name" ]; then say "  已经有 $name"; return 0; fi
  if [ -e "$MODELS/$name" ]; then say "  $name 上次没装完整，删掉重装"; rm -rf "$MODELS/$name"; fi
  if [ -s "$arc" ]; then say "  用上次下好的 $name 压缩包"; else say "  下载 $name …"; fi
  fetch "$url" "$arc" || { say "  下载失败：$url（检查网络能不能访问 github.com；再跑一遍会接着下）"; return 1; }
  say "  解压 $name …"
  rm -rf "$tmp"; mkdir -p "$tmp"
  if tar -xjf "$arc" -C "$tmp" && [ -d "$tmp/$name" ]; then
    mv "$tmp/$name" "$MODELS/$name" && rm -rf "$tmp" "$arc" && date > "$DONE/$name" && say "  装好了 $name" && return 0
  fi
  rm -rf "$tmp" "$arc"; say "  解压失败：$name（压缩包可能坏了，已删掉；再跑一遍重下）"; return 1
}

file() {   # 文件名 下载地址 最小字节数
  local name=$1 url=$2 min=$3
  if [ -f "$DONE/$name" ] && [ -s "$MODELS/$name" ]; then say "  已经有 $name"; return 0; fi
  rm -f "$MODELS/$name"
  say "  下载 $name …"
  if fetch "$url" "$MODELS/$name" && [ "$(stat -c %s "$MODELS/$name")" -ge "$min" ]; then
    date > "$DONE/$name"; say "  装好了 $name"; return 0
  fi
  rm -f "$MODELS/$name"; say "  下载失败：$url"; return 1
}

if [ "${1:-}" != "--check" ]; then
  say "1/6 安装 Python 包…"
  pip install -q --break-system-packages sherpa-onnx onnxruntime soundfile numpy scipy noisereduce pypinyin praat-parselmouth openpyxl pillow >/dev/null 2>&1 \
    || pip install -q sherpa-onnx onnxruntime soundfile numpy scipy noisereduce pypinyin praat-parselmouth openpyxl pillow >/dev/null 2>&1 \
    || say "  pip 安装失败：检查网络能不能访问 pypi.org"
  python3 -c "import playwright" 2>/dev/null || pip install -q --break-system-packages playwright >/dev/null 2>&1
  # 6.17：espeak-ng（自带在 espeakng-loader 里，几 MB）：词典里没有的词根（duc、ject）按拼读规则给读音，当单词念，不再一个个字母念
  python3 -c "import espeakng_loader" 2>/dev/null || pip install -q --break-system-packages espeakng-loader >/dev/null 2>&1 \
    || pip install -q espeakng-loader >/dev/null 2>&1 || say "  espeakng-loader 没装上：词典里没有的词根会一个个字母念"
  python3 - <<'PY' 2>/dev/null || { say "  装 Chromium…"; python3 -m playwright install chromium >/dev/null 2>&1; }
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    p.chromium.launch().close()
PY

  say "2/6 你的声音：声音克隆（ZipVoice）、声码器、英文音标词典…"
  get sherpa-onnx-zipvoice-distill-fp32-zh-en-emilia "$REL/tts-models/sherpa-onnx-zipvoice-distill-fp32-zh-en-emilia.tar.bz2" \
    || get sherpa-onnx-zipvoice-distill-int8-zh-en-emilia "$REL/tts-models/sherpa-onnx-zipvoice-distill-int8-zh-en-emilia.tar.bz2"
  file vocos_24khz.onnx "$REL/vocoder-models/vocos_24khz.onnx" 50000000
  file lexicon-en-us.txt "$REL/tts-models/lexicon-en-us.txt" 1000000      # 没有它，英文单词会被悄悄跳过
  say "3/6 英文声音 af_heart（Kokoro v1.0）…"
  get kokoro-multi-lang-v1_0 "$REL/tts-models/kokoro-multi-lang-v1_0.tar.bz2"
  say "4/6 识别模型（SenseVoice，检查念得清不清楚）…"
  get sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17 "$REL/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17.tar.bz2"
  say "5/6 音标词典（Kokoro v1.1；它的 38 号只在明说要用时才用）…"
  get kokoro-multi-lang-v1_1 "$REL/tts-models/kokoro-multi-lang-v1_1.tar.bz2"
  say "6/6 小黑板字体（霞鹜文楷）…"
  FONTS=$HOME/.local/share/fonts
  mkdir -p "$FONTS"
  if fc-list 2>/dev/null | grep -qi "LXGW WenKai"; then
    say "  已经有了"
  elif curl -fsSL --max-time 300 -o "$FONTS/LXGWWenKai-Regular.ttf" https://github.com/lxgw/LxgwWenKai/releases/download/v1.530/LXGWWenKai-Regular.ttf; then
    fc-cache -f >/dev/null 2>&1 || true; say "  装好了"
  else
    rm -f "$FONTS/LXGWWenKai-Regular.ttf"; say "  下载失败：小黑板改用楷体 / 思源宋体"
  fi
fi

say "检查…"
ok=1
for t in ffmpeg ffprobe node; do command -v $t >/dev/null || { say "  缺少 $t"; ok=0; }; done
ffmpeg -hide_banner -encoders 2>/dev/null | grep -q libx264 || { say "  ffmpeg 没有 libx264（H.264 编码）"; ok=0; }
fc-list 2>/dev/null | grep -qi "Noto Color Emoji" || say "  提醒：没有彩色表情字体（Noto Color Emoji），图会显示成方块"
fc-list :lang=zh 2>/dev/null | grep -q . || { say "  缺少中文字体"; ok=0; }
python3 -c "import sys; sys.path.insert(0, '$HERE'); import readings; sys.exit(0 if readings.have_espeak() else 1)" 2>/dev/null \
  || say "  提醒：没有 espeak-ng（pip install espeakng-loader）：词典里没有的词根会一个个字母念（不影响出片）"
for m in kokoro-multi-lang-v1_1 sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17; do
  { [ -f "$DONE/$m" ] && [ -d "$MODELS/$m" ]; } || { say "  $m 没装完整"; ok=0; }
done
python3 -c "import noisereduce" 2>/dev/null || say "  提醒：没装 noisereduce，配音少一道降噪"
WORDFILM_MODELS="$MODELS" python3 - "$HERE" <<'PY'
import sys
sys.path.insert(0, sys.argv[1])
import voice_config as V
p = V.voice_problems()
if p:
    print('声音：❌ 没准备好，不能出片（不会再悄悄用 38 号念）：')
    for x in p:
        print('  - ' + x)
    print('  再跑一遍 bash setup.sh（下载接着下）')
    sys.exit(1)
print('声音：✅ ' + V.describe())
PY
[ $? = 0 ] || ok=0
[ $ok = 1 ] && { say "准备好了。模型在 $MODELS"; exit 0; } || { say "有东西没准备好，看上面的提示"; exit 1; }

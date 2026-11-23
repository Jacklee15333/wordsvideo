#!/usr/bin/env bash
# 04 显卡（第八十版起，可选）：装“显卡版”的配音程序，再逐项测配音三路（声音克隆、英文、识别检查）和画面编码在显卡上快不快、对不对，
#   测好写进 ~/.wordfilm-gpu.env（出片脚本自动读：make_word.sh、批量技能）。约 2.5 GB 下载，10～20 分钟。放后台：
#     bash ~/lw/scripts/wsl/bg.sh start gpu bash ~/lw/scripts/wsl/04_gpu.sh
#   全装在单独的 Python 环境 ~/wf-gpu 里（CUDA 12 一套：sherpa-onnx 显卡版、onnxruntime-gpu 1.26、NVIDIA 的 CUDA 12 库），不动系统里原来的。
#   为什么是 CUDA 12：sherpa-onnx 只有 CUDA 12 的显卡版；onnxruntime-gpu 1.27 起要 CUDA 13，两套 cuDNN 文件名一样，混在一起会互相顶掉。
#   以前做实验装在系统里的 onnxruntime-gpu 1.32 + CUDA 13 库不用管，这里用不到。
#   关掉显卡：bash 04_gpu.sh --off（出片回到全用 CPU）；重测：bash 04_gpu.sh --check
. "$(dirname "$0")/common.sh"
apply_proxy
V=$HOME/wf-gpu; ENVG=$HOME/.wordfilm-gpu.env
case "${1:-}" in
  --off) rm -f "$ENVG"; say "✅ 显卡关掉了（出片全用 CPU）；再开：bash ~/lw/scripts/wsl/04_gpu.sh --check"; exit 0 ;;
esac
say "1/5 WSL 里能不能看到显卡…"
nvidia-smi -L 2>/dev/null | grep -q GPU || die "WSL 里看不到 NVIDIA 显卡（nvidia-smi 不行）：Windows 上装好 NVIDIA 驱动再试。看不到也不影响出片，全用 CPU"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader | sed 's/^/  /'
if [ "${1:-}" != --check ]; then
  say "2/5 单独的 Python 环境 $V …"
  if [ ! -x "$V/bin/python" ]; then
    python3 -m venv --system-site-packages "$V" 2>/dev/null || { apt-get install -y -q python3-venv >/dev/null 2>&1; python3 -m venv --system-site-packages "$V"; } \
      || die "建不了 Python 环境（apt-get install python3-venv 再试）"
  fi
  SV=$(python3 -c "import sherpa_onnx as s; print(s.__version__.split('+')[0])" 2>/dev/null) || die "系统里没有 sherpa-onnx：先跑 03_models.sh"
  say "3/5 sherpa-onnx 显卡版（约 250 MB）…"
  # 第八十三版：显卡版的名字现在带 onnxruntime 后缀（2.0.1+cuda12.cudnn9.onnxruntime1.28.2），先从下载页上找实际有哪些，同版本的优先
  CANDS=$("$V/bin/python" - "$SV" <<'PY'
import re, sys, urllib.request
sv = sys.argv[1]
for u in ('https://k2-fsa.github.io/sherpa/onnx/cuda-cn.html', 'https://k2-fsa.github.io/sherpa/onnx/cuda.html'):
    try:
        html = urllib.request.urlopen(u, timeout=90).read().decode('utf-8', 'replace').replace('%2B', '+').replace('%2b', '+')
    except Exception as e:
        print('#', u, e, file=sys.stderr); continue
    vs = sorted(set(re.findall(r'sherpa_onnx-([0-9][0-9.]*\+cuda12\.cudnn9[0-9A-Za-z.]*)-cp312-cp312-[^"<>\s]*linux_x86_64\.whl', html)))
    if not vs:
        continue
    def key(v):
        base, _, loc = v.partition('+')
        ort = re.search(r'onnxruntime([0-9.]+)', loc)
        return (base == sv, [int(x) for x in base.split('.') if x.isdigit()], [int(x) for x in ort.group(1).split('.')] if ort else [0])
    print(u)
    for v in sorted(vs, key=key, reverse=True)[:6]:
        print(v)
    break
PY
)
  FL=$(printf '%s\n' "$CANDS" | head -1); ok=0
  if [ -z "$CANDS" ]; then say "  ⚠ 下载页打不开（k2-fsa.github.io），开代理再跑"; fi
  for ver in $(printf '%s\n' "$CANDS" | tail -n +2); do
    say "  试 sherpa-onnx==$ver"
    timeout 1800 "$V/bin/pip" install -q --no-deps "sherpa-onnx==$ver" -f "$FL" && "$V/bin/python" -c "import sherpa_onnx as s; assert 'cuda' in s.__version__" 2>/dev/null && { ok=1; say "  装好了 $ver"; break; }
  done
  [ $ok = 1 ] || say "  ⚠ 没装上显卡版 sherpa-onnx：声音克隆和识别检查用 CPU（把上面的报错原样告诉用户）"
  say "  浏览器用显卡要的 Mesa 驱动（D3D12 / Vulkan 转到 Windows 的显卡）…"
  apt-get install -y -q mesa-vulkan-drivers libgl1-mesa-dri libegl1 libgles2 vulkan-tools >/dev/null 2>&1 || say "  ⚠ Mesa 驱动没装上（apt），浏览器多半只能用 CPU 画"
  apt-get install -y -q mesa-utils mesa-utils-bin >/dev/null 2>&1 || true
  command -v vulkaninfo >/dev/null && vulkaninfo --summary 2>/dev/null | grep -i "deviceName" | sed 's/^ */  Vulkan 看到：/' | head -3
  say "4/5 onnxruntime-gpu 1.26（CUDA 12 的最后一版）和 NVIDIA CUDA 12 的库（约 2 GB）…"
  timeout 3600 "$V/bin/pip" install -q onnxruntime-gpu==1.26.0 nvidia-cuda-runtime-cu12 nvidia-cublas-cu12 nvidia-cufft-cu12 nvidia-curand-cu12 \
      nvidia-cudnn-cu12 nvidia-cuda-nvrtc-cu12 || say "  ⚠ CUDA 12 的库没装全（看上面 pip 的报错；再跑一遍会接着装）"
fi
[ -x "$V/bin/python" ] || die "还没装：bash 04_gpu.sh"
if [ ! -f "$JOBS/protect/details.json" ] || [ ! -f "$WORK/protect/brief/prefs.json" ]; then     # 第八十一版：量画面速度要用 protect
  say "  先把 protect 准备好（量画面速度用，1～2 分钟，不配音、不渲染）…"
  bash "$LW/scripts/wsl/make_word.sh" protect 16 explore,shower,itself,protect --no-run > /dev/null 2>&1 \
    || bash "$LW/scripts/wsl/make_word.sh" protect 16 explore,shower,itself,protect --no-run --force-draft > /dev/null 2>&1 \
    || say "  ⚠ protect 没准备好，这次不量画面速度"
fi
say "5/5 逐项测（配音三路在 CPU 和显卡上各念几句比一比；浏览器画画面、编码各量一次；5～10 分钟）…"
LIBS=$("$V/bin/python" - <<'PY'
import glob, site, os
d = [p for s in site.getsitepackages() if s.startswith(os.environ.get('VIRTUAL_ENV', '~')) or '/wf-gpu/' in s for p in sorted(glob.glob(s + '/nvidia/*/lib'))]
print(':'.join(d + ['/usr/lib/wsl/lib']))
PY
)
VIRTUAL_ENV=$V PATH="$V/bin:$PATH" LD_LIBRARY_PATH="$LIBS${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
  "$V/bin/python" "$LW/scripts/wsl/gpu_check.py" --write "$ENVG" --venv "$V" --libs "$LIBS"

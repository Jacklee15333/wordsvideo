#!/usr/bin/env bash
# 批量出片共用的路径和小工具（各脚本 source 它；都在 WSL 里用 root 跑）
set -o pipefail
[ -f "$HOME/lw/scripts/wsl/common.sh" ] && . "$HOME/lw/scripts/wsl/common.sh"   # local-wordfilm 的设置（代理、GPU 库路径），有就用
export LWB=${LWB:-$HOME/lwb}                         # 本技能拷进 WSL 的位置
export WORDFILM_MODELS=${WORDFILM_MODELS:-$HOME/wordfilm-models}
export WORK=$HOME/wordfilm-work                      # 不要改：kit 的画面设置写死了 ~/wordfilm-work/<词>/art
export JOBS=${JOBS:-$HOME/wf-jobs}                   # 每个词单独一个 --work，几个词能同时做
export OUTROOT=${OUTROOT:-$HOME/wordfilm-out}
export REPO=${REPO:-$HOME/ciyuanchaifeng}
export BROOT=${BROOT:-$HOME/wf-batch}                # 每个批次一个文件夹：清单、设置、进度、日志
export S=$HOME/skills/word-construction-video
ENVF=$HOME/.wordfilm-local.env; [ -f "$ENVF" ] && . "$ENVF"
say() { printf '%s\n' "$*"; }
die() { printf '❌ %s\n' "$*"; exit 1; }            # 出错（流水线会自动再试一次）
need() { printf '⚠ %s\n' "$*"; exit 2; }           # 要人看一下才能往下走（流水线标成“要处理”，别的词照做）
type apply_proxy >/dev/null 2>&1 && apply_proxy
# 第八十版：local-wordfilm 的 04_gpu.sh 测好的显卡设置（~/.wordfilm-gpu.env：配音哪几路用显卡、画面用不用显卡编码）；批次设 GPU=0 就全用 CPU
type apply_gpu_env >/dev/null 2>&1 && apply_gpu_env
# 第八十四版：批次设 GPU=0 = 全用 CPU（流水线是带着显卡设置开起来的，这里要明确关掉，不然关不掉）；VOICE_GPU=0 = 只有配音用 CPU，画面编码照样用显卡
if [ "${GPU:-1}" = 0 ]; then
  unset WORDFILM_DEVICE WORDFILM_ZV_DEVICE WORDFILM_EN_DEVICE WORDFILM_ASR_DEVICE WORDFILM_BROWSER_GPU WORDFILM_BROWSER_ARGS WORDFILM_BROWSER_CHANNEL WORDFILM_CAPTURE
  export WORDFILM_ENCODER=x264
elif [ "${VOICE_GPU:-1}" = 0 ]; then
  export WORDFILM_ZV_DEVICE=cpu WORDFILM_EN_DEVICE=cpu WORDFILM_ASR_DEVICE=cpu; unset WORDFILM_DEVICE
fi
# 个别英文单词你的声音多念了还是念不清：这一句改成中文你的声音 + 英文美式女声（用户 2026-11-19 定的，默认开；批次设 MIX_FALLBACK=0 才不改）
[ "${MIX_FALLBACK:-1}" = 0 ] && export WORDFILM_MIX_FALLBACK=0
# 画面设置先找 ~/kit-extra（画面组给新词做的，跑 02 更新视频技能也不会被冲掉），再找视频技能自带的 ~/kit
kitfile() { for d in "$HOME/kit-extra" "$HOME/kit"; do [ -f "$d/$1" ] && { printf '%s\n' "$d/$1"; return 0; }; done; return 1; }

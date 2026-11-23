#!/usr/bin/env bash
# 共用的路径和小工具（其他脚本都 source 它）。都在 WSL 里用 root 跑。
set -o pipefail
export LW=${LW:-$HOME/lw}                        # 本技能拷进 WSL 的位置（sync_to_wsl.ps1 拷过来）
export REPO=${REPO:-$HOME/ciyuanchaifeng}        # 仓库（只取用得到的几个文件）
export WORDFILM_MODELS=${WORDFILM_MODELS:-$HOME/wordfilm-models}
export WORK=$HOME/wordfilm-work                  # 不要改：视频技能 kit 里写死了 ~/wordfilm-work/<词>/art
export JOBS=${JOBS:-$HOME/wf-jobs}               # 每个词单独一个 --work，几个词能同时跑
export OUTROOT=${OUTROOT:-$HOME/wordfilm-out}    # 做好的视频先放这里，再用 copy_out.sh 拷到 Windows
export ENVF=$HOME/.wordfilm-local.env            # 01、02 记下的设置（代理、总表路径……）
[ -f "$ENVF" ] && . "$ENVF"
say() { printf '%s\n' "$*"; }
die() { printf '❌ %s\n' "$*"; exit 1; }
envset() {   # envset 名字 值：写进 $ENVF（下次自动读）
  touch "$ENVF"; sed -i "/^$1=/d" "$ENVF"; printf "%s='%s'\n" "$1" "${2//\'/\'\\\'\'}" >> "$ENVF"; export "$1=$2"
}
apply_gpu_env() {   # 第八十版：04_gpu.sh 测好的显卡设置（~/.wordfilm-gpu.env：配音哪几路用显卡、画面用不用显卡编码）；GPU=0 全用 CPU
  if [ "${GPU:-1}" != 0 ] && [ -f "$HOME/.wordfilm-gpu.env" ]; then . "$HOME/.wordfilm-gpu.env"; fi
  return 0
}
gpu_line() {        # 打一行：这次哪几样用显卡
  if [ "${GPU:-1}" != 0 ] && [ -f "$HOME/.wordfilm-gpu.env" ]; then
    printf '显卡：声音克隆 %s、英文 %s、识别 %s、画面编码 %s\n' "${WORDFILM_ZV_DEVICE:-cpu}" "${WORDFILM_EN_DEVICE:-cpu}" "${WORDFILM_ASR_DEVICE:-cpu}" "${WORDFILM_ENCODER:-x264}"
  else
    printf '显卡：没开（全用 CPU；开：bash ~/lw/scripts/wsl/04_gpu.sh）\n'
  fi
}
apply_proxy() {
  if [ -n "${PROXY:-}" ]; then
    export http_proxy=$PROXY https_proxy=$PROXY HTTP_PROXY=$PROXY HTTPS_PROXY=$PROXY ALL_PROXY=$PROXY no_proxy=localhost,127.0.0.1
  fi
}

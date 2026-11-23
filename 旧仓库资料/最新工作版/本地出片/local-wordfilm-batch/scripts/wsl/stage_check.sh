#!/usr/bin/env bash
# 质检组（自动部分）：文件完整、没有退回 38 号、没有没听清的、没有只有英文的字幕，拼一张 9 格关键画面图给人看
# 用法：stage_check.sh 序号 文件夹名
. "$(dirname "$0")/bcommon.sh"
n=$1; w=$2
f=$(cat "$JOBS/$w/result.txt" 2>/dev/null); [ -f "$f" ] || die "没有 $w 的成片记录：先过渲染组"
python3 "$LWB/scripts/wsl/check_one.py" "$f" "$WORK/$w/brief"

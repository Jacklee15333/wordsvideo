#!/usr/bin/env bash
# 交付组：拷到 Windows（默认 D:\构词视频\<批次>）；开了上传就马上传到仓库（一个一个传，不等整批做完）
# 用法：stage_deliver.sh 序号 文件夹名
. "$(dirname "$0")/bcommon.sh"
n=$1; w=$2; UNIT=${UNIT:-batch}
f=$(cat "$JOBS/$w/result.txt" 2>/dev/null); [ -f "$f" ] || die "没有 $w 的成片记录"
dest=${WIN_DIR:-/mnt/d/构词视频/$UNIT}
case "$dest" in [A-Za-z]:*) dest=$(wslpath -u "$dest") ;; esac
mkdir -p "$dest" || die "建不了目录 $dest"
cp -f "$f" "$dest/" || die "拷到 Windows 失败：$dest"
sheet="${f%.mp4}_关键画面.jpg"; [ -f "$sheet" ] && cp -f "$sheet" "$dest/"
say "拷好了：$(wslpath -w "$dest/$(basename "$f")" 2>/dev/null || echo "$dest/$(basename "$f")")"
if [ "${UPLOAD:-0}" = 1 ]; then
  [ -n "${UPLOAD_DIR:-}" ] || need "开了上传但没设上传到哪个文件夹：batch.sh set <批次> UPLOAD_DIR=…"
  bash "$LWB/scripts/wsl/git_add_one.sh" "$f" "$UPLOAD_DIR" "$(basename "$f")" "$UNIT：$(basename "$f" .mp4)（本地批量出片，精简版）" || exit $?
fi
say "✅ 交付好了"

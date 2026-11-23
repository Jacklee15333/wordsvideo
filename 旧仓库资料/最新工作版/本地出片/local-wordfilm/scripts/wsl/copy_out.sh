#!/usr/bin/env bash
# copy_out.sh 文件夹名 [Windows 目录]：把做好的视频和关键画面图拷到 Windows（默认 D:\构词视频\<单元>）
. "$(dirname "$0")/common.sh"
w=${1:?用法：copy_out.sh 文件夹名 [Windows 目录]}
f=$(cat "$JOBS/$w/result.txt" 2>/dev/null); [ -f "$f" ] || die "没找到 $w 做好的视频"
dest=${2:-}
if [ -z "$dest" ]; then
  drv=d; [ -d /mnt/d ] || drv=e; [ -d /mnt/$drv ] || die "没有 D 盘、E 盘：写上 Windows 目录，比如 copy_out.sh $w 'G:\\构词视频'"
  dest=/mnt/$drv/构词视频/${UNIT:-7A-U4}
elif printf '%s' "$dest" | grep -q '^[A-Za-z]:'; then dest=$(wslpath -u "$dest"); fi
mkdir -p "$dest" || die "建不了目录 $dest"
cp -f "$f" "$dest/" && { [ -f "${f%.mp4}_关键画面.jpg" ] && cp -f "${f%.mp4}_关键画面.jpg" "$dest/"; true; } || die "拷贝失败"
say "✅ 拷好了：$(wslpath -w "$dest/$(basename "$f")")"

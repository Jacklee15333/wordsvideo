#!/usr/bin/env bash
# check_video.sh 文件夹名：检查做好的视频——文件完整、时长分辨率、配音有没有退回 38 号、字幕、音效，再截一张关键画面拼图
. "$(dirname "$0")/common.sh"
w=${1:?用法：check_video.sh 文件夹名}
f=$(cat "$JOBS/$w/result.txt" 2>/dev/null); [ -f "$f" ] || die "没找到 $w 做好的视频（make_word.sh 跑完会记在 $JOBS/$w/result.txt）"
P=$WORK/$w/brief; L=$HOME/lw-logs/$w.log
say "== 文件 =="; say "$f"
ffprobe -v error -show_entries format=duration,size:stream=codec_type,width,height -of csv=p=0 "$f" | sed 's/^/  /'
if [ -n "$(ffmpeg -v error -i "$f" -map 0:v:0 -map 0:a:0 -f null - 2>&1)" ]; then say "  ❌ 解码有错误"; bad=1; else say "  从头到尾解码没有错误"; fi
say "== 配音 =="
if [ -f "$L" ]; then
  k=$(grep -ac '\[kokoro\]' "$L"); say "  退回 38 号念的句子：$k 句（要是 0）"; [ "$k" = 0 ] || bad=1
  grep -a "没听清\|音效：\|字幕：" "$L" | sed 's/^/  /'
else say "  （没有后台日志 $L，跳过）"; fi
say "== 字幕 =="
python3 - "$P/subtitles.srt" <<'PY'
import re, sys
try:
    blocks = [b.split('\n')[2:] for b in open(sys.argv[1], encoding='utf-8').read().strip().split('\n\n')]
except OSError:
    sys.exit(print('  没有字幕文件'))
lines = [' '.join(b) for b in blocks if b]
en = [l for l in lines if not re.search(r'[\u3400-\u9fff]', l)]
print(f'  {len(lines)} 条；只有英文的：{len(en)} 条（要是 0）' + ('：' + ' | '.join(en) if en else ''))
PY
say "== 关键画面 =="
sheet="${f%.mp4}_关键画面.jpg"
python3 "$LW/scripts/wsl/frames.py" "$f" "$P/timing.json" "$sheet" >/dev/null && say "  $sheet" && say "  Windows 路径：$(wslpath -w "$sheet" 2>/dev/null || echo "$sheet")"
[ -z "${bad:-}" ] && say "✅ 检查完：打开上面的关键画面图看一眼，再用 copy_out.sh 拷到 Windows" || say "❌ 有问题（见上面）"

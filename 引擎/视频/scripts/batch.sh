#!/usr/bin/env bash
# 一批词在后台一个接一个出片（6.10 起，第四十七版）。沙盒会不定时整个重启（后台进程全停，文件还在），
# 所以每一轮开头都再跑一遍这条命令：做好的跳过，做到一半的接着做（配音按句缓存、画面每 30 秒一段）。
#
#   setsid nohup bash batch.sh <总表.xlsx> <视频文件夹> [edits.json] > ~/wordfilm-work/q/batch.log 2>&1 < /dev/null &
#
# 要做的词写在 ~/wordfilm-work/q/list.txt（一行一个，按用户给的顺序；随时可以往后加）。
# 做好的记进 q/done.txt；没做成的记进 q/skip.txt（看 q/<单词>.log，改好以后从 skip.txt 删掉那一行，会重新排上）。
# q/force.txt 里的词加 --force（英文只是识别模型没听出来、确认没问题时用）。音节表：环境变量 WORDFILM_SYL。
set -u
TABLE=$1; OUT=$2; EDITS=${3:-}
Q=${WORDFILM_WORK:-$HOME/wordfilm-work}/q
mkdir -p "$Q"; touch "$Q/list.txt" "$Q/done.txt" "$Q/skip.txt" "$Q/force.txt"
exec 9>"$Q/lock"
flock -n 9 || { echo "已经有一个在跑"; exit 0; }
HERE=$(cd "$(dirname "$0")" && pwd)
while true; do
  w=$(grep -vxF -f <(cat "$Q/done.txt" "$Q/skip.txt") "$Q/list.txt" | grep -v '^\s*$' | head -1)
  [ -z "$w" ] && { echo "$(date +%T) 队列空了"; sleep 20; continue; }
  echo "$(date +%T) ==== 开始 $w"
  args=(--table "$TABLE" --words "$w" --out "$OUT")
  [ -n "$EDITS" ] && args+=(--edits "$EDITS")
  [ -n "${WORDFILM_SYL:-}" ] && args+=(--syl "$WORDFILM_SYL")
  grep -qxF "$w" "$Q/force.txt" && args+=(--force)
  python3 "$HERE/run.py" "${args[@]}" > "$Q/$w.log" 2>&1
  # 6.27：视频叫“单词.mp4”“单词（详解）.mp4”（前面可能带序号）
  if grep -q "==== 做好了 [1-9]" "$Q/$w.log" && ls "$OUT"/*.mp4 2>/dev/null | grep -qE "/([0-9]+ )?$w(（详解）)?\.mp4$"; then
    echo "$w" >> "$Q/done.txt"; echo "$(date +%T) ==== 做好了 $w"
  else
    echo "$w" >> "$Q/skip.txt"; echo "$(date +%T) ==== 没做成 $w（看 $Q/$w.log）"
  fi
  pkill -f headless_shell 2>/dev/null; true
done

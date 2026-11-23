#!/bin/bash
# queue2.sh：按 ~/kit/q.txt（每行“文件夹名 序号”，词组用下划线）一个个做，前面的做完才做后面的；做好马上传 GitHub。
# 只做准备好了的（~/wordfilm-work/ready_<文件夹名>：画风转好、缩写念全以后才建）。q.txt 可以随时往后加。
exec 8>~/kit/queue2.lock; flock -n 8 || exit 0
while pgrep -f "run.py --table" >/dev/null; do sleep 5; done
idle=0
while [ $idle -lt 360 ]; do
  next=""
  while read -r s n; do
    [ -z "$s" ] && continue
    grep -qx "$s" ~/kit/uploaded.txt ~/kit/failed.txt 2>/dev/null && continue
    [ -f ~/wordfilm-work/ready_$s ] || continue
    next="$s $n"; break
  done < ~/kit/q.txt
  if [ -z "$next" ]; then sleep 10; idle=$((idle+1)); continue; fi
  idle=0
  set -- $next; s=$1; n=$2; w="${s//_/ }"; f="/mnt/user-data/outputs/7A-U4/$n $w.mp4"
  if [ -f "$f" ] && grep -qE "做好了 1 个|视频已经做好了" ~/wordfilm-work/run_$s.log 2>/dev/null; then
    if python3 ~/gh/gh_add.py "7A-U4：$n $w" "最新工作版/7A-U4/$n $w.mp4=$f" >> ~/kit/upload.log 2>&1 < /dev/null; then echo "$s" >> ~/kit/uploaded.txt; else sleep 30; fi
  else
    t=$(cat ~/wordfilm-work/tries_$s 2>/dev/null || echo 0); echo $((t+1)) > ~/wordfilm-work/tries_$s
    if [ "$t" -ge 16 ]; then echo "$s" >> ~/kit/failed.txt; continue; fi
    ~/kit/go2.sh "$s" "$n" > /dev/null < /dev/null
  fi
done

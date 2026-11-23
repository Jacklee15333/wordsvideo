#!/bin/bash
# queue.sh：按 ~/kit/q.txt（每行“单词 序号”）一个个做，做好马上传 GitHub
exec 9>~/kit/queue.lock; flock -n 9 || exit 0
while read -r w n; do
  [ -z "$w" ] && continue
  grep -qx "$w" ~/kit/uploaded.txt 2>/dev/null && continue
  [ -f ~/wordfilm-work/edits_$w.json ] || continue
  for i in 1 2 3 4 5 6 7 8 9 10; do
    f="/mnt/user-data/outputs/7A-U4/$n $w.mp4"
    [ -f "$f" ] && grep -qE "做好了 1 个|视频已经做好了" ~/wordfilm-work/run_$w.log 2>/dev/null && break
    ~/kit/go.sh $w $n > /dev/null < /dev/null
  done
  f="/mnt/user-data/outputs/7A-U4/$n $w.mp4"
  if [ -f "$f" ]; then
    python3 ~/gh/gh_add.py "7A-U4：$n $w" "最新工作版/7A-U4/$n $w.mp4=$f" >> ~/kit/upload.log 2>&1 < /dev/null && echo "$w" >> ~/kit/uploaded.txt
  fi
done < ~/kit/q.txt

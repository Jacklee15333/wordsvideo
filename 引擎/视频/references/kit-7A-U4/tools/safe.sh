#!/bin/bash
# safe.sh 命令…：配音（synth.py，声音克隆约占 2.5 GB）在跑、或者剩余内存不到 1.5 GB 时先等（最多约 4 分钟），再跑后面的命令。
# 起草出预览图要开浏览器，和配音挤在一起，4 GB 的沙盒会整个重启（6.30 一轮重启了四次）
for i in $(seq 1 48); do
  avail=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
  if ! pgrep -f synth.py >/dev/null && [ "$avail" -gt 1500 ]; then break; fi
  sleep 5
done
"$@"

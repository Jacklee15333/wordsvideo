#!/bin/bash
# 沙盒会不定时整个重启，后台的排队会停：每次干活前跑一下，没在跑就重新拉起来（setsid -f：不占着当前命令的输出，命令能马上结束）
pgrep -f "kit/queue2.sh" >/dev/null || { cd ~ && setsid -f bash ~/kit/queue2.sh > ~/kit/queue2.out 2>&1 < /dev/null; echo "（排队重新拉起来了）"; }

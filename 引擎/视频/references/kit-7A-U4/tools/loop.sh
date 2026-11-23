#!/bin/bash
# loop.sh 单词 序号：后台一段一段跑，直到做好
for i in 1 2 3 4 5 6 7 8; do
  ~/kit/go.sh $1 $2 > /dev/null
  grep -q "做好了 1 个" ~/wordfilm-work/run_$1.log && break
done
echo DONE >> ~/wordfilm-work/run_$1.log

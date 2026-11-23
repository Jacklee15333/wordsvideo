#!/bin/bash
# go2.sh 文件夹名 序号：前台跑一段（最多约 4 分半），没做完再跑。词组的文件夹名用下划线（text_message 12）
s=$1; n=$2; w="${s//_/ }"
cd ~/skills/word-construction-video/scripts
export WORDFILM_MODELS=~/wordfilm-models
timeout -k 5 280 python3 run.py --table /home/claude/v69/2词源拆分总表_本族词版.xlsx --syl /home/claude/v69/4音节划分_总词库7869词_细分版.xlsx \
  --words "$w" --number $n --out /mnt/user-data/outputs/7A-U4 --edits ~/wordfilm-work/edits_$s.json --edition brief --budget 230 >> ~/wordfilm-work/run_$s.log 2>&1
pkill -f synth.py; pkill -f render.py; pkill -f headless_shell; pkill ffmpeg

#!/bin/bash
# go.sh 单词 序号 ：前台跑一段（最多约 4 分半），没做完再跑
w=$1; n=$2
cd ~/skills/word-construction-video/scripts
export WORDFILM_MODELS=~/wordfilm-models
timeout -k 5 280 python3 run.py --table /home/claude/v69/2词源拆分总表_本族词版.xlsx --syl /home/claude/v69/4音节划分_总词库7869词_细分版.xlsx \
  --words $w --number $n --out /mnt/user-data/outputs/7A-U4 --edits ~/wordfilm-work/edits_$w.json --edition brief --budget 230 >> ~/wordfilm-work/run_$w.log 2>&1
pkill -f synth.py; pkill -f render.py; pkill -f headless_shell; pkill ffmpeg
grep -v "resampler\|sample_rate\|AcceptWaveform" ~/wordfilm-work/run_$w.log | tail -4 | cut -c1-200

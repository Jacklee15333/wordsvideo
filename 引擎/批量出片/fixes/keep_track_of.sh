#!/usr/bin/env bash
# keep_track_of：总表 of 那一格没写意思，起草出来是“单词是 of，of。”，改成讲清楚（视频技能 kit README 的做法）
cd ~/skills/word-construction-video/scripts || exit 1
python3 ~/kit/tools/fixsay.py keep_track_of "单词是 of，of。" "单词是 of，表示“…的”。track of a rabbit，就是兔子的踪迹。" 2>&1 | tail -2 \
  || echo "（已经改过，或者起草的说法变了：看一眼配音稿里 of 那一句）"
exit 0

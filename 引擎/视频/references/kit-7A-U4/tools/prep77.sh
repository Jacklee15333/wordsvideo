#!/bin/bash
# prep77.sh 单词 序号 [art脚本名]：prep.sh 的第七十七版路径版（总表 = 初中含义版，音节表在 ~/tables）
w=$1; n=$2; a=${3:-$1}; word="${w//_/ }"
S=~/skills/word-construction-video
A=~/wordfilm-work/$w/art
T=~/tables/2词源拆分总表_初中含义版.xlsx
Y=~/tables/4音节划分_总词库7869词_细分版.xlsx
mkdir -p $A
cp $S/references/scenes/*.svg $A/ 2>/dev/null
cd $S/scripts
export WORDFILM_MODELS=~/wordfilm-models
python3 poses.py $A --motion > ~/wordfilm-work/prep_$w.log 2>&1 || echo "poses 出错"
for x in ${a//,/ }; do [ -f ~/kit/${x}_art.py ] && { python3 ~/kit/${x}_art.py $A >> ~/wordfilm-work/prep_$w.log 2>&1 || echo "${x}_art 出错"; }; done
python3 ~/kit/words/$w.py ~/wordfilm-work/edits_$w.json >> ~/wordfilm-work/prep_$w.log 2>&1 || echo "words/$w 出错"
python3 - "$w" <<'PY'
import json,sys,os,re
w=sys.argv[1]; s=open(os.path.expanduser(f'~/wordfilm-work/edits_{w}.json'),encoding='utf-8').read()
miss=sorted(set(f for f in re.findall(r'art/([^"\s]+?\.(?:svg|png))',s) if not os.path.exists(os.path.expanduser(f'~/wordfilm-work/{w}/art/{f}'))))
print('缺图：', miss if miss else '无')
PY
mkdir -p ~/wordfilm-draft; [ -L ~/wordfilm-draft/$w ] || ln -sfn ~/wordfilm-work/$w ~/wordfilm-draft/$w
timeout 280 python3 run.py --table $T --syl $Y \
  --words "$word" --number $n --out /mnt/user-data/outputs/7A-U4 --edits ~/wordfilm-work/edits_$w.json --edition brief --draft-only --work ~/wordfilm-draft > ~/wordfilm-work/draft_$w.log 2>&1
echo "draft exit: $?"
python3 ~/kit/tools/show.py ~/wordfilm-work/draft_$w.log 1 400 300 | grep "还要补\|音效\|Traceback\|Error" | tail -8

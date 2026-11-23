#!/bin/bash
# prep.sh 单词 序号 [art脚本名]：拷场景、生成会动的人、画这个词的图、写画面设置、起草（图画书风）
w=$1; n=$2; a=${3:-$1}; word="${w//_/ }"   # 词组的文件夹、设置文件用下划线（text_message），run.py 用空格
S=~/skills/word-construction-video
A=~/wordfilm-work/$w/art
mkdir -p $A
cp $S/references/scenes/*.svg $A/ 2>/dev/null
cd $S/scripts
export WORDFILM_MODELS=~/wordfilm-models
python3 poses.py $A --motion > ~/wordfilm-work/prep_$w.log 2>&1 || echo "poses 出错"
for x in ${a//,/ }; do [ -f ~/kit/${x}_art.py ] && { python3 ~/kit/${x}_art.py $A >> ~/wordfilm-work/prep_$w.log 2>&1 || echo "${x}_art 出错"; }; done
python3 ~/kit/words/$w.py ~/wordfilm-work/edits_$w.json >> ~/wordfilm-work/prep_$w.log 2>&1 || echo "words/$w 出错"
# 画面设置里用到的 art 文件都在吗
python3 - "$w" <<'PY'
import json,sys,os,re
w=sys.argv[1]; s=open(os.path.expanduser(f'~/wordfilm-work/edits_{w}.json'),encoding='utf-8').read()
miss=sorted(set(f for f in re.findall(r'art/([^"\s]+?\.(?:svg|png))',s) if not os.path.exists(os.path.expanduser(f'~/wordfilm-work/{w}/art/{f}'))))
print('缺图：', miss if miss else '无')
PY
# 6.30：起草用单独的 --work（~/wordfilm-draft，这个词的文件夹链接回 ~/wordfilm-work/<词>）：
# 排队里的 run.py 每跑一段都会重写 ~/wordfilm-work/details.json，两边同时起草会互相覆盖（“details.json 里没有 …”）
mkdir -p ~/wordfilm-draft; [ -L ~/wordfilm-draft/$w ] || ln -sfn ~/wordfilm-work/$w ~/wordfilm-draft/$w
timeout 280 python3 run.py --table /home/claude/v69/2词源拆分总表_本族词版.xlsx --syl /home/claude/v69/4音节划分_总词库7869词_细分版.xlsx \
  --words "$word" --number $n --out /mnt/user-data/outputs/7A-U4 --edits ~/wordfilm-work/edits_$w.json --edition brief --draft-only --work ~/wordfilm-draft > ~/wordfilm-work/draft_$w.log 2>&1
python3 ~/kit/tools/show.py ~/wordfilm-work/draft_$w.log 1 400 300 | grep "还要补\|音效\|Traceback\|Error" | tail -8

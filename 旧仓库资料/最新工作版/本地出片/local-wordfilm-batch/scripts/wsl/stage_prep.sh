#!/usr/bin/env bash
# 准备组：画图 → 起草检查（要“还要补：都齐了”）→ 按序号转画风 → 配音稿里的缩写念全 → 已知的配音修正
# 用法：stage_prep.sh 序号 文件夹名 画图脚本(逗号隔开，按先后)
. "$(dirname "$0")/bcommon.sh"
n=$1; w=$2; arts=$3; word="${w//_/ }"; UNIT=${UNIT:-batch}
[ -f "${TABLE:-}" ] && [ -f "${SYL:-}" ] || die "没找到总表或音节表：先按 local-wordfilm 跑 02_get_repo.sh"
wp=$(kitfile "words/$w.py") || need "没有 $w 的画面设置（~/kit-extra 或 ~/kit 的 words/$w.py）：这个词要先由“画面组”做画面设置"
A=$WORK/$w/art; J=$JOBS/$w; OUT=$OUTROOT/$UNIT
mkdir -p "$WORK/$w" "$J" "$OUT"; ln -sfn "$WORK/$w" "$J/$w"
cd "$S/scripts" || die "视频技能不在 $S"
export PYTHONUNBUFFERED=1
say "【画图】$arts"
rm -rf "$A"; mkdir -p "$A"                          # 每次从头画（上次转过画风的也清掉）
cp "$S/references/scenes/"*.svg "$A/" 2>/dev/null
python3 poses.py "$A" --motion > "$J/prep_art.log" 2>&1 || { tail -5 "$J/prep_art.log"; die "poses.py 出错"; }
for x in ${arts//,/ }; do
  ap=$(kitfile "${x}_art.py") || need "没有画图脚本 ${x}_art.py（清单里 $w 的画图脚本写错了？）"
  python3 "$ap" "$A" >> "$J/prep_art.log" 2>&1 || { tail -5 "$J/prep_art.log"; die "${x}_art.py 出错"; }
done
python3 "$wp" "$WORK/edits_$w.json" >> "$J/prep_art.log" 2>&1 || { tail -5 "$J/prep_art.log"; die "words/$w.py 出错"; }
python3 "$LWB/scripts/wsl/missing_art.py" "$w" || need "画面设置里用到的图没画出来：照上面的提示改清单里 $w 的画图脚本（按先后），再 retry"
say "【起草检查】"
python3 run.py --table "$TABLE" --syl "$SYL" --words "$word" --number "$n" --out "$OUT" --edits "$WORK/edits_$w.json" \
    --edition brief --draft-only --no-preview --work "$J" > "$J/draft.log" 2>&1 || { tail -15 "$J/draft.log"; die "起草出错（$J/draft.log）"; }
# 第八十一版：起草时不出预览图（一个词省几十秒）；起草检查没过才补一张给人看（见下面 preview_for_people）
preview_for_people() {
  python3 run.py --table "$TABLE" --syl "$SYL" --words "$word" --number "$n" --out "$OUT" --edits "$WORK/edits_$w.json" \
      --edition brief --draft-only --work "$J" >> "$J/draft.log" 2>&1 || true
}
line=$(grep -a '还要补' "$J/draft.log" | tail -1 | sed 's/^ *//')
say "$line"
fixed=0
apply_fix() {
  if [ -f "$LWB/fixes/$w.py" ]; then python3 "$LWB/fixes/$w.py" "$WORK/$w/brief/plan.json"
  elif [ -f "$LWB/fixes/$w.sh" ]; then bash "$LWB/fixes/$w.sh"
  else say "没有"; fi
}
case "$line" in
  *都齐了*) ;;
  *)
    # 第八十版：先打已知的配音修正。起草检查看的是详解版的稿子（kit README：keep track of 修正以后检查还会报“标签‘兔子的踪迹’配音里没有说到”，
    #   精简版的稿子已经说到了）。剩下的只差“标签配音里没有说到”、而这些标签精简版稿子里都说到了，就放行；别的问题照旧停下
    say "【已知的配音修正（先打，再看起草检查）】"; apply_fix; fixed=1
    python3 "$LWB/scripts/wsl/label_ok.py" "$line" "$WORK/$w/brief/plan.json" \
      || { preview_for_people; need "起草检查没过：$line（预览图 $WORK/$w/brief/preview.png）"; } ;;
esac
say "【画风】"
st=$(python3 -c "import styles; print(styles.style_for(int('$n')))") || die "styles.py 出错"
if [ "$st" != book ]; then python3 styles.py "$st" "$A" | tail -1; else say "第 $n 个是图画书风，不用转"; fi
say "【缩写念全】"; python3 "$HOME/kit/tools/expand.py" "$w" | tail -1
say "【已知的配音修正】"
if [ $fixed = 1 ]; then say "上面打过了"; else apply_fix; fi
say "✅ 准备好了"

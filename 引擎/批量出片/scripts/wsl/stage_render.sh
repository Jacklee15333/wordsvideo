#!/usr/bin/env bash
# 渲染组：出片（第七十九版起几个浏览器一起渲染）。配音组写好了记号，这里不会重念
# 用法：stage_render.sh 序号 文件夹名
. "$(dirname "$0")/bcommon.sh"
n=$1; w=$2; word="${w//_/ }"; UNIT=${UNIT:-batch}
J=$JOBS/$w; OUT=$OUTROOT/$UNIT; mkdir -p "$OUT"
cd "$S/scripts" || die "视频技能不在 $S"
export PYTHONUNBUFFERED=1 WORDFILM_SYNTH_JOBS=1 WORDFILM_RENDER_JOBS=${RENDER_JOBS:-}
touch "$J/render.start"
python3 run.py --table "$TABLE" --syl "$SYL" --words "$word" --number "$n" --out "$OUT" --edits "$WORK/edits_$w.json" \
    --edition brief --work "$J" > "$J/render.log" 2>&1
rc=$?
grep -av "resampler\|sample_rate\|AcceptWaveform\|^ *in_sample_rate\|^ *output_sample_rate" "$J/render.log" | grep -a "画面：\|字幕：\|音效：\|秒，\|先不渲染\|跳过\|Error\|出错" | tail -n 8
if grep -aq "先不渲染" "$J/render.log"; then need "run.py 没有渲染：$(grep -a '先不渲染' "$J/render.log" | tail -1)"; fi
f="$OUT/$n $word.mp4"; [ -f "$f" ] || f=$(ls -t "$OUT"/*" $word.mp4" 2>/dev/null | head -1)
if [ $rc = 0 ] && [ -f "$f" ] && { [ "$f" -nt "$J/render.start" ] || grep -aq "视频已经做好了" "$J/render.log"; }; then
  printf '%s\n' "$f" > "$J/result.txt"; say "✅ 渲染好了：$f"; exit 0
fi
die "渲染没出片（返回码 $rc，日志 $J/render.log）"

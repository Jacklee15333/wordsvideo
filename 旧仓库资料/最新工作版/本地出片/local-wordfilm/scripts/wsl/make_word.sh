#!/usr/bin/env bash
# make_word.sh 文件夹名 序号 画图脚本1,画图脚本2… [--no-run] [--force-draft]
#   用视频技能 kit 里现成的画面设置，出一个词的精简版视频：
#   画图 → 起草检查（要“都齐了”）→ 按序号转画风 → 配音稿里的缩写念全 → 已知的配音修正 → 配音、渲染
#   词组的文件夹名用下划线（text_message）。序号是单元里的顺序，决定画风和文件名（16 → “16 protect.mp4”、中西合璧风）。
#   例：bash ~/lw/scripts/wsl/bg.sh start protect bash ~/lw/scripts/wsl/make_word.sh protect 16 explore,shower,itself,protect
#   中途停了（关机、WSL 被关）：再跑同一条命令，念好的配音会复用。
. "$(dirname "$0")/common.sh"
[ $# -ge 3 ] || die "用法：make_word.sh 文件夹名 序号 画图脚本(逗号隔开)"
w=$1; n=$2; arts=$3; shift 3
RUN=1; FORCE=0
for x in "$@"; do case $x in --no-run) RUN=0;; --force-draft) FORCE=1;; *) die "不认识的参数 $x";; esac; done
word="${w//_/ }"
S=$HOME/skills/word-construction-video
[ -f "${TABLE:-}" ] || die "没找到总表：先跑 02_get_repo.sh"
[ -f "${SYL:-}" ] || die "没找到音节表：先跑 02_get_repo.sh"
[ -f "$HOME/kit/words/$w.py" ] || die "kit 里没有 $w 的画面设置（~/kit/words/$w.py）：这个词要先写画面设置，见本技能 SKILL.md 第 7 步"
apply_proxy
A=$WORK/$w/art; J=$JOBS/$w; OUT=$OUTROOT/${UNIT:-7A-U4}
mkdir -p "$WORK/$w" "$J" "$OUT"; ln -sfn "$WORK/$w" "$J/$w"; rm -f "$J/result.txt"
T0=$(date +%s)
stage() { say ""; say "【$1】$(date +%H:%M:%S)"; }
cd "$S/scripts" || die "视频技能不在 $S"
export PYTHONUNBUFFERED=1

stage "1/6 画图：场景、会动的人、画图脚本 $arts"
rm -rf "$A"; mkdir -p "$A"                       # 每次从头画（上次转过画风的也清掉）
cp "$S/references/scenes/"*.svg "$A/" 2>/dev/null
python3 poses.py "$A" --motion > "$J/prep.log" 2>&1 || { tail -5 "$J/prep.log"; die "poses.py 出错（$J/prep.log）"; }
for x in ${arts//,/ }; do
  [ -f "$HOME/kit/${x}_art.py" ] || die "kit 里没有画图脚本 ${x}_art.py"
  python3 "$HOME/kit/${x}_art.py" "$A" >> "$J/prep.log" 2>&1 || { tail -5 "$J/prep.log"; die "${x}_art.py 出错（$J/prep.log）"; }
done
python3 "$HOME/kit/words/$w.py" "$WORK/edits_$w.json" >> "$J/prep.log" 2>&1 || { tail -5 "$J/prep.log"; die "words/$w.py 出错"; }
python3 - "$w" "$WORK" <<'PY' || die "画面设置里用到的图没画出来：画图脚本的先后可能不对（看 ~/kit/README.md）"
import os, re, sys
w, work = sys.argv[1], sys.argv[2]
s = open(f'{work}/edits_{w}.json', encoding='utf-8').read()
miss = sorted(set(f for f in re.findall(r'art/([^"\s]+?\.(?:svg|png))', s) if not os.path.exists(f'{work}/{w}/art/{f}')))
print('缺图：' + ('、'.join(miss) if miss else '无'))
if miss:   # 找找是哪个画图脚本画的这些图（文件名的主干出现在脚本里）
    import glob
    kit = os.path.expanduser('~/kit')
    for f in miss:
        stem = re.sub(r'(_f\d+)?\.(svg|png)$', '', f)
        who = sorted(os.path.basename(x)[:-7] for x in glob.glob(kit + '/*_art.py') if stem in open(x, encoding='utf-8').read())
        print(f'  {f}：可能要加画图脚本 ' + ('、'.join(who) if who else '（没找到，看 ~/kit/README.md）'))
sys.exit(1 if miss else 0)
PY

stage "2/6 起草检查（不配音、不渲染）"
python3 run.py --table "$TABLE" --syl "$SYL" --words "$word" --number "$n" --out "$OUT" --edits "$WORK/edits_$w.json" \
    --edition brief --draft-only --work "$J" > "$J/draft.log" 2>&1 || { tail -15 "$J/draft.log"; die "起草出错（$J/draft.log）"; }
need=$(grep -a '还要补' "$J/draft.log" | tail -1 | sed 's/^ *//')
say "$need"
if ! printf '%s' "$need" | grep -q '都齐了'; then
  [ $FORCE = 1 ] && say "（加了 --force-draft，照样往下做）" || die "起草检查没过：把上面“还要补”这一行告诉用户，不要自己硬做"
fi
say "预览图：$WORK/$w/brief/preview.png"

stage "3/6 画风"
st=$(python3 -c "import styles; print(styles.style_for(int('$n')))") || die "styles.py 出错"
if [ "$st" != book ]; then python3 styles.py "$st" "$A" | tail -1; else say "第 $n 个是图画书风，不用转"; fi

stage "4/6 配音稿里的英文缩写念全"
python3 "$HOME/kit/tools/expand.py" "$w" | tail -1

stage "5/6 已知的配音修正"
if [ -f "$LW/fixes/$w.py" ]; then python3 "$LW/fixes/$w.py" "$WORK/$w/brief/plan.json"; else say "这个词没有要预先改的"; fi

if [ $RUN = 0 ]; then say ""; say "✅ 准备好了（--no-run：没有配音、渲染）"; exit 0; fi
stage "6/6 配音、渲染（最久的一步）"
apply_gpu_env; say "  $(gpu_line)"          # 第八十版：04_gpu.sh 测好的显卡设置（视频技能第八十版起自己会用显卡，不再打补丁）
( bash setup.sh --check > "$J/check.log" 2>&1 ) || { tail -4 "$J/check.log"; die "声音模型没装好：先跑 03_models.sh"; }
python3 run.py --table "$TABLE" --syl "$SYL" --words "$word" --number "$n" --out "$OUT" --edits "$WORK/edits_$w.json" \
    --edition brief --work "$J" 2>&1 | grep -av --line-buffered "resampler\|sample_rate\|AcceptWaveform\|^ *in_sample_rate\|^ *output_sample_rate"
rc=${PIPESTATUS[0]}
f="$OUT/$n $word.mp4"; [ -f "$f" ] || f=$(ls -t "$OUT"/*" $word.mp4" 2>/dev/null | head -1)
mins=$(( ($(date +%s) - T0 + 59) / 60 ))
if [ $rc = 0 ] && [ -f "$f" ] && [ "$f" -nt "$J/draft.log" ]; then
  printf '%s\n' "$f" > "$J/result.txt"
  say ""; say "✅ 做好了：$f（这一轮用时约 $mins 分钟）。下一步：bash ~/lw/scripts/wsl/check_video.sh $w"
else
  say ""; say "❌ 没做完（用时 $mins 分钟）：看上面的日志。有句子“没听清”见 troubleshooting.md 第 4 节；改好以后再跑同一条命令，念好的句子会复用"
  exit 1
fi

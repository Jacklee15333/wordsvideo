#!/usr/bin/env bash
# batch.sh：本地批量出片（流水线）的总开关。阶段名用中文：准备 配音 渲染 质检 交付
#   new 批次 清单.tsv     建批次（复制清单、写默认设置），并体检
#   check 批次            再体检一次（改了清单、画面组加了新词以后）
#   set 批次 键=值 …      改设置（UPLOAD=1、UPLOAD_DIR=…、WIN_DIR=…、HOLD_QA=1、SYNTH_JOBS=…、RENDER_JOBS=…）
#   start 批次            开工（后台常驻；做完或都卡住就自己停；重复 start 不会开两个）
#   status 批次           进度表（隔 3～5 分钟看一次）
#   log 批次 词 [阶段] [行数]  看某个词某一组的日志
#   retry 批次 词 [阶段]  处理好以后接着做（不写阶段 = 从卡住的那一组）；也用来让做完的词从某一组重做
#   ok 批次 词            HOLD_QA=1 时：人看过关键画面图，放行交付
#   login 批次            开工前先登录 GitHub（Windows 上弹窗；省得做到一半等登录）
#   note 批次 词 说明     记下制作中替用户做的处理（改了哪句配音、换了哪个动作、跳过了谁），报告里会列出来
#   skip 批次 词          这个词不做了
#   reload 批次           清单加了词 / 改了画图脚本以后，让流水线读新清单
#   stop 批次             停下（正在做的这一组下次从头做，缓存还在）
#   report 批次           出报告（每个词每一组用了多久）
#   list                  看有哪些批次
. "$(dirname "$0")/bcommon.sh"
cmd=${1:-}; name=${2:-}; BD=$BROOT/$name
running() { [ -f "$BD/pipeline.pid" ] && kill -0 "$(cat "$BD/pipeline.pid")" 2>/dev/null; }
send() { mkdir -p "$BD/cmd"; printf '%s\n' "$1" > "$BD/cmd/$(date +%s%N).json"; }
jstr() { python3 -c 'import json,sys; print(json.dumps(sys.argv[1], ensure_ascii=False))' "$1"; }
start_daemon() {
  running && { say "流水线已经在跑（pid $(cat "$BD/pipeline.pid")）"; return 0; }
  setsid nohup python3 "$LWB/scripts/wsl/pipeline.py" "$BD" >> "$BD/pipeline.log" 2>&1 < /dev/null &
  sleep 3; running && say "流水线开工了（pid $(cat "$BD/pipeline.pid")）。隔 3～5 分钟看一次：batch.sh status $name" \
                   || { tail -5 "$BD/pipeline.log"; die "流水线没起来"; }
}
[ "$cmd" = list ] || [ -n "$name" ] || die "要写批次名：batch.sh $cmd 批次名 …（看有哪些：batch.sh list）"
case $cmd in
  new)
    list=${3:-}; [ -f "$list" ] || die "用法：batch.sh new 批次名 清单.tsv（清单格式见 lists/7A-U4.tsv）"
    [ -e "$BD" ] && die "批次 $name 已经有了（$BD）：换个名字，或者确定不要了再删掉那个文件夹"
    mkdir -p "$BD/logs" "$BD/cmd"; cp "$list" "$BD/list.tsv"
    cat > "$BD/config.env" <<CFG
# 批次 $name 的设置（batch.sh set 改；流水线每隔几秒读一次，下一个词开始用）
# 下面是建议值（用户 2026-11-18 说过的）。开工前要问用户、等用户确认（SKILL.md 第 2 步），确认后 set CONFIRMED=1 才能开工
UNIT=$name
WIN_DIR=/mnt/d/构词视频/$name
UPLOAD=1
UPLOAD_DIR=最新工作版/$name
HOLD_QA=0
ON_STUCK=fix
# 个别英文单词你的声音多念了还是念不清：1 = 这一句改成中文你的声音 + 英文美式女声（用户 2026-11-19 定的）；0 = 不改（标“要处理”，按 ON_STUCK 办）
MIX_FALLBACK=1
CONFIRMED=0
CFG
    say "建好了：$BD"; python3 "$LWB/scripts/wsl/pipeline.py" --check "$BD" ;;
  check) [ -d "$BD" ] || die "没有批次 $name"; python3 "$LWB/scripts/wsl/pipeline.py" --check "$BD" ;;
  set)
    [ -f "$BD/config.env" ] || die "没有批次 $name"; shift 2
    for kv in "$@"; do k=${kv%%=*}; [ "$k" != "$kv" ] || die "要写成 键=值：$kv"
      sed -i "/^$k=/d" "$BD/config.env"; printf '%s\n' "$kv" >> "$BD/config.env"; say "设好了：$kv"; done ;;
  start)
    [ -d "$BD" ] || die "没有批次 $name：先 batch.sh new"
    [ -f "$S/SKILL.md" ] || die "没有视频技能：先按 local-wordfilm 装好环境"
    grep -qx 'CONFIRMED=1' "$BD/config.env" || die "还没问用户：开工前要把设置和要处理的词一次问完、等用户确认（SKILL.md 第 2 步），确认后 batch.sh set $name CONFIRMED=1"
    start_daemon ;;
  login)
    [ -d "$BD" ] || die "没有批次 $name"
    bash "$LWB/scripts/wsl/git_add_one.sh" --login ;;
  note)
    w=${3:?要写词}; shift 3; [ $# -gt 0 ] || die "用法：batch.sh note 批次 词 说明"
    printf -- '- %s %s：%s\n' "$(date '+%m-%d %H:%M')" "$w" "$*" >> "$BD/notes.md"; say "记下了（报告里会列出来）" ;;
  status) [ -d "$BD" ] || die "没有批次 $name"         # 省 token：默认三行；整张表加 full
    if [ "${3:-}" = full ]; then python3 "$LWB/scripts/wsl/pipeline.py" --status "$BD"; else python3 "$LWB/scripts/wsl/pipeline.py" --brief "$BD"; fi ;;
  wait) [ -d "$BD" ] || die "没有批次 $name"           # 省 token：等到有词做完 / 卡住 / 流水线停了才回来，最多等 ${3:-30} 分钟
    python3 "$LWB/scripts/wsl/pipeline.py" --wait "$BD" "${3:-30}" ;;
  log)
    w=${3:?要写词}; st=${4:-}
    declare -A M=([准备]=prep [配音]=voice [渲染]=render [质检]=check [交付]=deliver)
    if [ -n "$st" ]; then f="$BD/logs/$w.${M[$st]:-$st}.log"; else f=$(ls -t "$BD/logs/$w".*.log 2>/dev/null | head -1); fi
    [ -f "$f" ] || die "没有日志：$w ${st}"; say "== $f =="; tail -n "${5:-20}" "$f" ;;
  retry|redo) w=${3:?要写词}; send "{\"op\":\"retry\",\"word\":$(jstr "$w"),\"stage\":$(jstr "${4:-}")}"; say "已让 $w ${4:+从 $4 }接着做"; start_daemon ;;
  ok) w=${3:?要写词}; send "{\"op\":\"ok\",\"word\":$(jstr "$w")}"; say "已放行 $w 交付"; start_daemon ;;
  skip) w=${3:?要写词}; send "{\"op\":\"skip\",\"word\":$(jstr "$w"),\"why\":$(jstr "${4:-跳过}")}"; say "$w 不做了"; running || python3 - "$BD" "$w" <<'PY'
import json, sys, os
p = os.path.join(sys.argv[1], 'state.json')
if os.path.exists(p):
    s = json.load(open(p, encoding='utf-8'))
    for w in s['words']:
        if w['word'] == sys.argv[2]: w['stage'], w['status'] = 'skipped', ''
    json.dump(s, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
PY
    ;;
  reload) send '{"op":"reload"}'; say "让流水线读新清单"; start_daemon ;;
  stop)
    running || { say "流水线没在跑"; exit 0; }
    send '{"op":"stop"}'; for i in $(seq 1 30); do running || break; sleep 1; done
    running && die "30 秒没停下，再等一下或看 $BD/pipeline.log" || say "停了。接着做：batch.sh start $name" ;;
  report) [ -d "$BD" ] || die "没有批次 $name"; python3 "$LWB/scripts/wsl/pipeline.py" --report "$BD"; say "（存在 $BD/report.md）" ;;
  list) for d in "$BROOT"/*/; do [ -d "$d" ] || continue; n=$(basename "$d"); [ -f "$d/pipeline.pid" ] && kill -0 "$(cat "$d/pipeline.pid")" 2>/dev/null && say "$n（在跑）" || say "$n"; done ;;
  *) sed -n '2,19p' "$0" ;;
esac

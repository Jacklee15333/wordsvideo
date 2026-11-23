#!/usr/bin/env bash
# bg.sh start 名字 命令…   放后台跑（关掉这个窗口也不停），日志 ~/lw-logs/名字.log
# bg.sh status 名字 [行数] 看进度（出片的会多一行“配音：念好 X / 共 Y 段”）
# bg.sh stop 名字          停掉
# bg.sh list               看有哪些在跑
. "$(dirname "$0")/common.sh"
D=$HOME/lw-logs; mkdir -p "$D"
alive() { [ -f "$D/$1.pid" ] && kill -0 "$(cat "$D/$1.pid")" 2>/dev/null; }
case ${1:-} in
  start)
    n=$2; shift 2; [ $# -gt 0 ] || die "start 后面要写名字和命令"
    if alive "$n"; then say "$n 已经在跑（pid $(cat "$D/$n.pid")），看进度：bash $LW/scripts/wsl/bg.sh status $n"; exit 0; fi
    [ -f "$D/$n.log" ] && mv -f "$D/$n.log" "$D/$n.log.1"
    setsid nohup bash -c 'echo $$ > "$0"; exec "$@"' "$D/$n.pid" "$@" > "$D/$n.log" 2>&1 < /dev/null &
    sleep 2
    say "已经放后台：$n（日志 $D/$n.log）。隔 3～5 分钟看一次：bash $LW/scripts/wsl/bg.sh status $n" ;;
  status)
    n=$2; f=$D/$n.log; [ -f "$f" ] || die "没有 $n 的日志"
    if alive "$n"; then say "== $n：正在跑 =="; else say "== $n：已经停了（看最后一行是 ✅ 还是 ❌）=="; fi
    grep -av "resampler\|sample_rate\|AcceptWaveform\|^ *in_sample_rate\|^ *output_sample_rate\|^\s*$" "$f" | tail -n "${3:-12}"
    P=$WORK/$n/brief
    if [ -f "$P/plan.json" ] && [ -d "$P/audio" ]; then
      python3 - "$P" <<'PY'
import json, sys, glob, os
p = sys.argv[1]
segs = sum(len(s.get('segs', [])) for s in json.load(open(p + '/plan.json', encoding='utf-8'))['scenes'].values())
done = len([f for f in glob.glob(p + '/audio/*_seg*.wav')])
print(f'配音：念好 {done} / 共 {segs} 段' + ('（配音念完了，在渲染或已做好）' if done >= segs else ''))
PY
    fi
    alive "$n" ;;
  stop)
    n=$2; alive "$n" || { say "$n 没在跑"; exit 0; }
    kill -TERM -- -"$(cat "$D/$n.pid")" 2>/dev/null; sleep 2; say "停了 $n" ;;
  list)
    for p in "$D"/*.pid; do [ -f "$p" ] || continue; n=$(basename "$p" .pid); alive "$n" && say "在跑：$n"; done; true ;;
  *) die "用法：bg.sh start|status|stop|list …" ;;
esac

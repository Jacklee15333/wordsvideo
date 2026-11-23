#!/usr/bin/env bash
# 配音组：念配音稿（第七十九版起几个进程一起念），每句听一遍；写好和 run.py 一样的“配音做完”记号，渲染组不会重念
# 用法：stage_voice.sh 序号 文件夹名
# 第八十版：用不用显卡看 ~/.wordfilm-gpu.env（bcommon.sh 读）；要学的单词没听清时视频技能自己多念几遍（只那一句），
#   改了稿子再跑这一组，只重念改过的和没听清的句子（别的直接用上次的结果）
. "$(dirname "$0")/bcommon.sh"
n=$1; w=$2
ew=$WORK/$w/brief; plan=$ew/plan.json; audio=$ew/audio
[ -f "$plan" ] || die "没有配音稿 $plan：先过准备组"
cd "$S/scripts" || die "视频技能不在 $S"
( bash setup.sh --check > "$JOBS/$w/voice_check.log" 2>&1 ) || { tail -3 "$JOBS/$w/voice_check.log"; die "声音模型没装好：按 local-wordfilm 跑 03_models.sh"; }
export PYTHONUNBUFFERED=1 WORDFILM_SYNTH_JOBS=${SYNTH_JOBS:-}
python3 synth.py "$plan" "$audio" 2>&1 | grep -av --line-buffered "resampler\|sample_rate\|AcceptWaveform\|^ *in_sample_rate\|^ *output_sample_rate"
rc=${PIPESTATUS[0]}
[ "$rc" = 0 ] || die "配音出错（返回码 $rc）"
python3 - "$plan" "$audio" "$S/scripts" <<'PY'
import json, hashlib, sys
plan_p, audio, sdir = sys.argv[1:4]
sys.path.insert(0, sdir)
import voice_config
b = open(plan_p, 'rb').read()
d = hashlib.md5(b + voice_config.signature(json.loads(b.decode('utf-8')) or {}).encode('utf-8')).hexdigest()
open(audio + '/plan.md5', 'w').write(d)          # 和 run.py 一样的记号：稿子、声音都没变，渲染时就不重念
man = json.load(open(audio + '/manifest.json', encoding='utf-8'))
miss = ['%s/%s：%s' % (k, s['name'], s.get('text', '')[:40]) for k, segs in man.items() for s in segs if s.get('miss')]
k38 = ['%s/%s' % (k, s['name']) for k, segs in man.items() for s in segs if s.get('engine') == 'kokoro']
if k38:
    print('⚠ 有 %d 句退回了 38 号念：%s' % (len(k38), '、'.join(k38[:5]))); sys.exit(2)
if miss:
    print('⚠ 有 %d 句要学的单词没听清，先不渲染（改说法见 references/exceptions.md 第 2 节）：' % len(miss))
    for m in miss: print('   ' + m)
    sys.exit(2)
print('✅ 配音好了：%d 句' % sum(len(v) for v in man.values()))
PY

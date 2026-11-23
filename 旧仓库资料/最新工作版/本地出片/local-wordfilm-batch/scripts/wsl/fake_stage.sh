#!/usr/bin/env bash
# 只给测流水线用（config.env 写 FAKE=1）：不真做，睡一会儿；FAKE_FAIL="词:阶段:返回码,…" 让某一组第一次失败
n=$1; w=$2; st=$BATCH_STAGE; sleep "${FAKE_SLEEP:-1}"
IFS=, read -ra F <<< "${FAKE_FAIL:-}"
for x in "${F[@]}"; do IFS=: read -r fw fs fc <<< "$x"
  if [ "$fw" = "$w" ] && [ "$fs" = "$st" ] && [ ! -f "$BATCH_DIR/fake_$w.$st" ]; then
    touch "$BATCH_DIR/fake_$w.$st"; [ "$fc" = 2 ] && echo "⚠ 假装要人看：$w $st" || echo "❌ 假装出错：$w $st"; exit "$fc"; fi
done
echo "✅ $st 好了：$n $w"

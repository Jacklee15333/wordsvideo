#!/usr/bin/env bash
# 03 装声音模型（约 1.6 GB，从 GitHub 下；断了再跑一遍会接着下）。最后两行是“声音：✅ …”“准备好了”才算好。
# 放后台跑：bash ~/lw/scripts/wsl/bg.sh start models bash ~/lw/scripts/wsl/03_models.sh
. "$(dirname "$0")/common.sh"
apply_proxy
S=$HOME/skills/word-construction-video/scripts
[ -f "$S/setup.sh" ] || die "先跑 02_get_repo.sh"
cd "$S" && bash setup.sh
rc=$?
[ $rc = 0 ] && say "✅ 03 完成：声音模型都装好了（$WORDFILM_MODELS）" \
             || say "❌ 03 还缺东西：看上面的提示；再跑一遍会接着下。下不动见 troubleshooting.md 第 2 节"
exit $rc

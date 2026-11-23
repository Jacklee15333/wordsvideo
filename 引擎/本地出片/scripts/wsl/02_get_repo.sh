#!/usr/bin/env bash
# 02 从 GitHub 取最新版：总表、视频技能（「最新工作版」里编号最大的“第…版”）和音节划分表；解开视频技能。
# 只下用得到的几个文件（不下归档里的视频）。仓库是公开的，下载不用登录。可以重复跑（会更新到最新）。
. "$(dirname "$0")/common.sh"
apply_proxy
URL=${REPO_URL:-https://github.com/Jacklee15333/ciyuanchaifeng.git}
git config --global core.quotepath false
if [ ! -d "$REPO/.git" ]; then
  say "克隆仓库（只要目录，不下文件）…"
  git clone -q --filter=blob:none --depth=1 --no-checkout "$URL" "$REPO" || die "克隆失败：检查能不能访问 github.com（慢就给 01 加 --proxy）"
  git -C "$REPO" sparse-checkout init --no-cone
else
  say "更新仓库…"
  git -C "$REPO" fetch -q --depth=1 origin master || die "更新失败：检查网络 / 代理"
  git -C "$REPO" reset -q --hard origin/master
fi
cd "$REPO" || exit 1
VER=$(git ls-tree --name-only HEAD "最新工作版/" | python3 "$LW/scripts/wsl/pick_version.py") || die "「最新工作版」里没有“第…版”文件夹"
SYLP=$(git ls-tree -r --name-only HEAD | grep '音节划分_总词库7869词_细分版\.xlsx$' | head -1)
[ -n "$SYLP" ] || die "仓库里没找到音节划分表"
printf '%s\n' '/.gitignore' "/最新工作版/$VER/" "/$SYLP" > .git/info/sparse-checkout
say "下载 $VER 和音节表…"
git checkout -q master 2>/dev/null; git sparse-checkout reapply || die "下载文件失败"
TABLE=$(ls "$REPO/最新工作版/$VER/"2词源拆分总表*.xlsx 2>/dev/null | head -1)
SKZ=$(ls "$REPO/最新工作版/$VER/"3单词根据词源生成视频*.skill 2>/dev/null | head -1)
[ -f "$TABLE" ] || die "$VER 里没有总表（2词源拆分总表….xlsx）"
[ -f "$SKZ" ] || die "$VER 里没有视频技能（3单词根据词源生成视频….skill）"
say "解开视频技能…"
rm -rf "$HOME/skills/word-construction-video"; mkdir -p "$HOME/skills"
unzip -q -o "$SKZ" -d "$HOME/skills" || die "视频技能解不开：$SKZ"
[ -f "$HOME/skills/word-construction-video/SKILL.md" ] || die "视频技能包里没有 word-construction-video/SKILL.md"
ln -sfn "$HOME/skills/word-construction-video/references/kit-7A-U4" "$HOME/kit"
envset VER "$VER"; envset TABLE "$TABLE"; envset SYL "$REPO/$SYLP"
cur=$(grep -m1 '^当前 6\.' "$HOME/skills/word-construction-video/SKILL.md" | sed -E 's/^当前 ([0-9.]+).*/\1/')
say "✅ 02 完成：$VER（视频技能 $cur）"
say "   总表：$TABLE"
say "   音节表：$REPO/$SYLP"

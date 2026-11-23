#!/usr/bin/env bash
# git_add_one.sh 本地文件 仓库里的文件夹 仓库里的文件名 提交说明：先对齐远端最新，只新增/更新这一个文件，推送
# 登录用 Windows 的 Git 凭据管理器（第一次推送在 Windows 上弹出 GitHub 登录窗口）；不要把令牌写进命令或对话
. "$(dirname "$0")/bcommon.sh"
src=$1; dir=${2%/}; name=$3; msg=$4
[ -d "$REPO/.git" ] || die "没有仓库 $REPO：先按 local-wordfilm 跑 02_get_repo.sh"
[ "$src" = --login ] || [ -f "$src" ] || die "没有这个文件：$src"
if [ -z "$(git config --global credential.helper)" ]; then
  gcm=""
  for d in c d e; do for p in "Program Files/Git/mingw64/bin/git-credential-manager.exe" "Program Files/Git/mingw64/libexec/git-core/git-credential-manager.exe"; do
    [ -z "$gcm" ] && [ -f "/mnt/$d/$p" ] && gcm="/mnt/$d/$p"; done; done
  [ -n "$gcm" ] || need "没找到 Windows 的 Git 凭据管理器（装 Git for Windows 才有）：见 references/exceptions.md 第 5 节"
  git config --global credential.helper "${gcm// /\\ }"
fi
[ -n "$(git config --global user.name)" ] || git config --global user.name "Jacklee15333"
[ -n "$(git config --global user.email)" ] || git config --global user.email "Jacklee15333@users.noreply.github.com"
cd "$REPO" || exit 1
if [ "$src" = --login ]; then        # 开工前登录：试推一次（不真推），让凭据管理器弹窗登录，登录信息记在 Windows 里
  say "正在登录 GitHub：Windows 上会弹出登录窗口（以前登录过就不会弹）…"
  timeout 600 git push --dry-run -q origin HEAD:master >/dev/null 2>&1 || need "登录没成功：请用户在弹出的窗口里登录 GitHub，再 batch.sh login"
  say "✅ GitHub 登录好了，制作中上传不会再弹窗"; exit 0
fi
timeout 300 git fetch -q --depth=1 origin master || die "取远端最新失败：检查网络 / 代理"
git reset -q --hard origin/master
grep -qxF "/$dir/" .git/info/sparse-checkout || printf '%s\n' "/$dir/" >> .git/info/sparse-checkout
git sparse-checkout reapply
mkdir -p "$dir" && cp -f "$src" "$dir/$name"
git add -- "$dir/$name"
if git diff --cached --quiet; then say "仓库里已经是一样的文件，不用传"; exit 0; fi
git commit -q -m "$msg"
say "推送中（第一次会在 Windows 上弹出 GitHub 登录窗口）…"
timeout 900 git push -q origin HEAD:master || need "推送失败：没登录成功或网络问题（登录好以后 retry）"
say "传好了：$dir/$name（提交 $(git rev-parse --short HEAD)）"

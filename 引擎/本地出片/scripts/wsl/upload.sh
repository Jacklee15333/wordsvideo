#!/usr/bin/env bash
# upload.sh 本地文件 [仓库里的文件夹] [仓库里的文件名]：只新增（或更新）这一个文件，推到 GitHub。
#   默认放进「最新工作版/<最新版>」，文件名不变。先对齐远端最新，别人新传的东西不会被盖掉。
#   登录用 Windows 的 Git 凭据管理器：第一次推送会在 Windows 上弹出 GitHub 登录窗口，用户登录一次就行。
#   不要把令牌贴进对话，也不要写进命令。
. "$(dirname "$0")/common.sh"
src=${1:?用法：upload.sh 本地文件 [仓库里的文件夹] [文件名]}; [ -f "$src" ] || die "没有这个文件：$src"
dir=${2:-最新工作版/${VER:?先跑 02_get_repo.sh}}; name=${3:-$(basename "$src")}
dst="${dir%/}/$name"; msg=${MSG:-"$(basename "${dir%/}")：$name"}
apply_proxy
[ -d "$REPO/.git" ] || die "先跑 02_get_repo.sh"
if [ -z "$(git config --global credential.helper)" ]; then
  gcm=$(for drv in /mnt/c /mnt/d /mnt/e; do
          ls "$drv/Program Files/Git/mingw64/bin/git-credential-manager.exe" \
             "$drv/Program Files/Git/mingw64/libexec/git-core/git-credential-manager.exe" \
             "$drv/Program Files/Git/mingw64/libexec/git-core/git-credential-manager-core.exe" 2>/dev/null
        done | head -1)
  [ -n "$gcm" ] || die "没找到 Windows 的 Git 凭据管理器（装了 Git for Windows 才有）。见 troubleshooting.md 第 8 节"
  git config --global credential.helper "${gcm// /\\ }"
  say "已设置用 Windows 的 Git 凭据管理器登录 GitHub"
fi
[ -n "$(git config --global user.name)" ] || git config --global user.name "Jacklee15333"
[ -n "$(git config --global user.email)" ] || git config --global user.email "Jacklee15333@users.noreply.github.com"
cd "$REPO" || exit 1
git fetch -q --depth=1 origin master || die "取远端最新失败：检查网络"
git reset -q --hard origin/master
grep -qxF "/${dir%/}/" .git/info/sparse-checkout || printf '%s\n' "/${dir%/}/" >> .git/info/sparse-checkout
git sparse-checkout reapply
mkdir -p "$dir" && cp -f "$src" "$dst"
git add -- "$dst"
git diff --cached --quiet && { say "仓库里已经是一样的文件，不用传"; exit 0; }
git commit -q -m "$msg"
say "推送中（第一次会在 Windows 上弹出 GitHub 登录窗口，请用户登录）…"
git push -q origin HEAD:master || die "推送失败：没登录成功或网络问题"
say "✅ 传好了：$dst（提交 $(git rev-parse --short HEAD)）"

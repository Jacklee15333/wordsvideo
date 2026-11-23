#!/usr/bin/env bash
# 01 装系统软件、字体、Python 包、浏览器（root；10～20 分钟；可以重复跑，装过的会跳过）
# 用法：bash 01_bootstrap.sh [--proxy http://地址:端口] [--no-cn-mirror]
#   默认 apt、pip 用清华源（国内快）；GitHub 上的东西（仓库、模型、浏览器）慢就加 --proxy（见 troubleshooting.md 第 1 节）
. "$(dirname "$0")/common.sh"
CN=1
while [ $# -gt 0 ]; do
  case $1 in --proxy) envset PROXY "$2"; shift 2;; --no-cn-mirror) CN=0; shift;; *) die "不认识的参数 $1";; esac
done
[ "$(id -u)" = 0 ] || die "要用 root 跑：wsl -d Ubuntu-24.04 -u root -- bash -lc '…'"
apply_proxy
export DEBIAN_FRONTEND=noninteractive

if [ $CN = 1 ]; then
  say "1/6 apt 换清华源…"
  for f in /etc/apt/sources.list.d/ubuntu.sources /etc/apt/sources.list; do
    [ -f "$f" ] && sed -i -E 's#https?://(archive|security)\.ubuntu\.com/ubuntu/?#https://mirrors.tuna.tsinghua.edu.cn/ubuntu/#g' "$f"
  done
else
  say "1/6 apt 用默认源"
fi

say "2/6 装系统软件（ffmpeg、Node.js、Python、git、字体）…"
apt-get update -q >/tmp/apt-update.log 2>&1 || { tail -5 /tmp/apt-update.log; die "apt-get update 失败：检查网络 / 代理"; }
apt-get install -y -q python3 python3-pip git curl wget ca-certificates bzip2 xz-utils unzip zip ffmpeg nodejs \
    fontconfig fonts-noto-cjk fonts-noto-color-emoji fonts-dejavu-core fonts-crosextra-caladea libsndfile1 procps psmisc \
    >/tmp/apt-install.log 2>&1 || { tail -8 /tmp/apt-install.log; die "apt 安装失败"; }
for p in fonts-inter fonts-crosextra-carlito; do apt-get install -y -q $p >/dev/null 2>&1 || say "  （可选的 $p 没装上，不影响）"; done

say "3/6 字体设置（和之前出片的环境一样：英文 Cambria → Caladea，中文 Noto Sans CJK SC）…"
cat > /etc/fonts/local.conf <<'XML'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<!-- local-wordfilm：通用字体族的首选，和云端出片环境一致；不要把 Windows 的字体加进来，画面会和以前不一样 -->
<fontconfig>
  <alias><family>sans-serif</family><prefer><family>Inter</family><family>Noto Sans CJK SC</family></prefer></alias>
  <alias><family>serif</family><prefer><family>DejaVu Serif</family><family>Noto Serif CJK SC</family></prefer></alias>
</fontconfig>
XML
fc-cache -f >/dev/null 2>&1

say "4/6 pip 设置…"
[ $CN = 1 ] && pip3 config --global set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple >/dev/null
pip3 config --global set global.break-system-packages true >/dev/null
pip3 config --global set global.timeout 120 >/dev/null

say "5/6 装 Playwright 和 Chromium（画面渲染用的浏览器）…"
pip3 install -q playwright >/tmp/pip-pw.log 2>&1 || { tail -5 /tmp/pip-pw.log; die "pip 装 playwright 失败"; }
python3 -m playwright install-deps chromium >/tmp/pw-deps.log 2>&1 || { tail -5 /tmp/pw-deps.log; die "装浏览器依赖失败"; }
ok=0
for host in "" https://registry.npmmirror.com/-/binary/playwright https://npmmirror.com/mirrors/playwright; do
  if [ -z "$host" ]; then python3 -m playwright install chromium >/tmp/pw.log 2>&1 && ok=1
  else PLAYWRIGHT_DOWNLOAD_HOST=$host python3 -m playwright install chromium >/tmp/pw.log 2>&1 && ok=1; fi
  [ $ok = 1 ] && break
  say "  下载 Chromium 失败，换一个下载地址再试…"
done
[ $ok = 1 ] || { tail -5 /tmp/pw.log; die "Chromium 下载失败：加 --proxy 再跑（troubleshooting.md 第 1、3 节）"; }
python3 - <<'PY' || die "Chromium 装好了但起不来（看上面的报错）"
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    p.chromium.launch().close()
print('  Chromium 能用')
PY

say "6/6 检查…"
v=$(node -v 2>/dev/null | sed 's/^v//; s/\..*//'); [ "${v:-0}" -ge 18 ] || die "Node.js 版本太低（要 18 以上）：$(node -v 2>&1)"
grep -q libx264 <(ffmpeg -hide_banner -encoders 2>/dev/null) || die "ffmpeg 没有 libx264"
grep -qi "Noto Sans CJK" <(fc-list) || die "中文字体没装上"
grep -qi caladea <(fc-match Cambria) || say "  提醒：Cambria 没对上 Caladea（英文字体会和以前略有不同）"
say "✅ 01 完成：Python $(python3 -V | cut -d' ' -f2)、Node $(node -v)、ffmpeg、Chromium、字体都好了${PROXY:+（代理 $PROXY）}"

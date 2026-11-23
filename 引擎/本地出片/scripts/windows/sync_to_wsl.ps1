# 把本技能文件夹拷进 WSL 的 ~/lw（每次更新本技能后再跑一次）。成功最后一行是 SYNC_OK
# 第八十四版：先拷到 ~/lw.new，拷成功了才换掉旧的（以前先删旧的，拷失败就空了）。
# 从 Git Bash 调本脚本、技能放在中文路径下时，路径会被转成乱码（GBK）：先把技能文件夹拷到纯英文路径（比如 D:\wf-sync）再跑
param([string]$Distro = "Ubuntu-24.04")
$env:WSL_UTF8 = "1"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$lin = ((& wsl.exe -d $Distro -u root -- wslpath -a ($root -replace "\\", "/")) | Out-String) -replace "`0", ""      # 第八十三版：用正斜杠，从 Git Bash 调也不会把反斜杠吃掉
$lin = $lin.Trim()
if (-not $lin) { Write-Output "转换不了路径：$root（先确认第 1 步是 RESULT: OK）"; exit 1 }
Write-Output "从 $root（WSL 里是 $lin）拷到 ~/lw"
& wsl.exe -d $Distro -u root -- bash -c "rm -rf ~/lw.new && mkdir -p ~/lw.new && cp -r '$lin/.' ~/lw.new/ && rm -rf ~/lw && mv ~/lw.new ~/lw && find ~/lw -type f \( -name '*.sh' -o -name '*.py' -o -name '*.md' \) -exec sed -i 's/\r`$//' {} + && chmod +x ~/lw/scripts/wsl/*.sh && echo SYNC_OK"

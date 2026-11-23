# 把本技能文件夹拷进 WSL 的 ~/lw（每次更新本技能后再跑一次）。成功最后一行是 SYNC_OK
param([string]$Distro = "Ubuntu-24.04")
$env:WSL_UTF8 = "1"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$lin = ((& wsl.exe -d $Distro -u root -- wslpath -a ($root -replace "\\", "/")) | Out-String) -replace "`0", ""      # 第八十三版：用正斜杠，从 Git Bash 调也不会把反斜杠吃掉
$lin = $lin.Trim()
if (-not $lin) { Write-Output "转换不了路径：$root（先确认第 1 步是 RESULT: OK）"; exit 1 }
Write-Output "从 $root（WSL 里是 $lin）拷到 ~/lw"
& wsl.exe -d $Distro -u root -- bash -c "rm -rf ~/lw && mkdir -p ~/lw && cp -r '$lin/.' ~/lw/ && find ~/lw -type f \( -name '*.sh' -o -name '*.py' -o -name '*.md' \) -exec sed -i 's/\r`$//' {} + && chmod +x ~/lw/scripts/wsl/*.sh && echo SYNC_OK"

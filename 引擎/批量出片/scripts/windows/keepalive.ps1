# 在后台挂一个不占资源的 wsl 进程，WSL 就不会在没有窗口时自己关掉（后台出片不会被停）。
#   开：powershell -ExecutionPolicy Bypass -File keepalive.ps1
#   关：powershell -ExecutionPolicy Bypass -File keepalive.ps1 -Stop
param([string]$Distro = "Ubuntu-24.04", [switch]$Stop)
$mine = Get-CimInstance Win32_Process -Filter "Name='wsl.exe'" | Where-Object { $_.CommandLine -like "*wordfilm-keepalive*" }
if ($Stop) {
  $mine | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
  Write-Output "keepalive 关掉了"; exit 0
}
if ($mine) { Write-Output "keepalive 已经在运行"; exit 0 }
# 第八十三版：参数写成一整串（以前数组拼起来 bash -c 后面那段没加引号，keepalive 一开就退出）
Start-Process -WindowStyle Hidden -FilePath "wsl.exe" -ArgumentList "-d $Distro -u root -- bash -c `"exec -a wordfilm-keepalive sleep infinity`""
Start-Sleep -Seconds 3
$chk = ((& wsl.exe -d $Distro -u root -- pgrep -f wordfilm-keepalive) | Out-String) -replace "`0", ""
if ($chk.Trim()) { Write-Output "keepalive 开好了（电脑重启后要再运行一次）" } else { Write-Output "keepalive 没开起来：在 WSL 里看 pgrep -f wordfilm-keepalive"; exit 1 }

# 给 WSL 多分内存（第八十版）。WSL 默认只能用电脑内存的一半（32 GB 的电脑是 15～16 GB），批量出片时配音、渲染只能各开一条道。
# 只改 C:\Users\<用户名>\.wslconfig 里 [wsl2] 下面 memory 这一行，别的设置（比如 networkingMode=mirrored）原样保留。
# 生效要关掉 WSL 再打开（wsl --shutdown 会停掉正在跑的出片！先确认没有在跑：batch.sh status），本脚本不会自己关。
param([string]$Size = "24GB")
$f = Join-Path $env:USERPROFILE ".wslconfig"
$lines = @()
if (Test-Path $f) { $lines = [System.IO.File]::ReadAllLines($f) }
$out = New-Object System.Collections.Generic.List[string]
$inWsl2 = $false; $done = $false; $hasSection = $false
foreach ($l in $lines) {
  if ($l -match '^\s*\[(.+)\]\s*$') {
    if ($inWsl2 -and -not $done) { $out.Add("memory=$Size"); $done = $true }
    $inWsl2 = ($Matches[1].Trim().ToLower() -eq 'wsl2'); if ($inWsl2) { $hasSection = $true }
    $out.Add($l); continue
  }
  if ($inWsl2 -and $l -match '^\s*memory\s*=') { if (-not $done) { $out.Add("memory=$Size"); $done = $true }; continue }
  $out.Add($l)
}
if ($inWsl2 -and -not $done) { $out.Add("memory=$Size"); $done = $true }
if (-not $hasSection) { $out.Add("[wsl2]"); $out.Add("memory=$Size") }
[System.IO.File]::WriteAllLines($f, $out)
Write-Output "写好了：$f（[wsl2] memory=$Size）"
Get-Content $f | ForEach-Object { Write-Output "  $_" }
Write-Output "要生效：确认没有在出片（batch.sh status 显示“没在跑”），再运行 wsl --shutdown，然后重新打开 Ubuntu。RESULT: OK"

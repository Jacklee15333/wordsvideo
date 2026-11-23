# 检查 WSL2 和 Ubuntu-24.04 装好没有、装在哪个盘。最后一行 RESULT: OK / NO_WSL / NO_DISTRO / WSL1 / ON_C
param([string]$Distro = "Ubuntu-24.04", [string]$Target = "D:\WSL\Ubuntu-24.04")
$env:WSL_UTF8 = "1"
function Clean($s) { ($s | Out-String) -replace "`0", "" }

if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) {
  Write-Output "这台电脑还没有 WSL。请用户本人用【管理员身份】打开 PowerShell，依次运行："
  Write-Output "  wsl --install --no-distribution"
  Write-Output "  （提示重启就重启电脑，然后接着运行）"
  Write-Output "  wsl --update"
  Write-Output "  wsl --install -d $Distro --location $Target"
  Write-Output "装完会弹出 Ubuntu 窗口，按提示设一个用户名和密码。"
  Write-Output "RESULT: NO_WSL"; exit 2
}
$help = Clean (& wsl.exe --help 2>&1)
$hasLocation = $help -match "--location"
$hasMove = $help -match "--move"
$list = Clean (& wsl.exe -l -v 2>&1)
Write-Output $list
$line = ($list -split "`r?`n") | Where-Object { $_ -match [regex]::Escape($Distro) } | Select-Object -First 1
if (-not $line) {
  Write-Output "还没装 $Distro。请用户本人用【管理员身份】打开 PowerShell，运行："
  Write-Output "  wsl --update"
  Write-Output "  wsl --install -d $Distro --location $Target"
  Write-Output "（要是提示不认识 --location：去掉 --location 和后面的路径再装，装好后再跑一次本检查，按提示挪到 D 盘）"
  Write-Output "装完会弹出 Ubuntu 窗口，按提示设一个用户名和密码。"
  Write-Output "RESULT: NO_DISTRO"; exit 2
}
$ver = if ($line -match "\s2\s*$") { 2 } else { 1 }
$base = $null
Get-ChildItem "HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss" -ErrorAction SilentlyContinue | ForEach-Object {
  $p = Get-ItemProperty $_.PSPath
  if ($p.DistributionName -eq $Distro) { $base = [string]$p.BasePath }
}
$base = $base -replace '^\\\\\?\\', ''
Write-Output "$Distro ：WSL$ver，装在 $base"
if ($base) {
  $d = $base.Substring(0, 1).ToUpper()
  $drive = Get-PSDrive -Name $d -ErrorAction SilentlyContinue
  if ($drive) { Write-Output ("{0} 盘剩余 {1} GB" -f $d, [math]::Round($drive.Free / 1GB, 1)) }
}
$gcm = @("C:\Program Files\Git\mingw64\bin\git-credential-manager.exe",
         "C:\Program Files\Git\mingw64\libexec\git-core\git-credential-manager.exe",
         "D:\Program Files\Git\mingw64\bin\git-credential-manager.exe",
         "D:\Program Files\Git\mingw64\libexec\git-core\git-credential-manager.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
if ($gcm) { Write-Output "Git 凭据管理器：有（上传时用它登录 GitHub）" } else { Write-Output "Git 凭据管理器：没找到（只影响上传；要上传先装 Git for Windows）" }

if ($ver -ne 2) {
  Write-Output "要换成 WSL2：wsl --set-version $Distro 2"
  Write-Output "RESULT: WSL1"; exit 3
}
if ($base -and $base.Substring(0, 1).ToUpper() -eq "C") {
  Write-Output "Ubuntu 在 C 盘（C 盘空间紧）。用户同意后挪到 D 盘，一条一条运行，每条成功了再运行下一条（里面的文件原样保留）："
  Write-Output "  wsl --shutdown"
  if ($hasMove) {
    Write-Output "  wsl --manage $Distro --move $Target"
  } else {
    Write-Output "  mkdir D:\WSL -Force"
    Write-Output "  wsl --export $Distro D:\WSL\ubuntu-backup.tar"
    Write-Output "  wsl --unregister $Distro          （上一条成功、D:\WSL\ubuntu-backup.tar 有几个 GB 才运行这条）"
    Write-Output "  wsl --import $Distro $Target D:\WSL\ubuntu-backup.tar --version 2"
    Write-Output "  （确认能用以后再删 D:\WSL\ubuntu-backup.tar。这样挪完默认登录用户会变成 root，本技能本来就用 root）"
  }
  Write-Output "RESULT: ON_C"; exit 4
}
Write-Output "RESULT: OK"

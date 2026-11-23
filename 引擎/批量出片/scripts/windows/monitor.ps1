# 盯着电脑（本地出片，2026-11-19 加）：每隔几秒记一行 CPU、内存、显卡（占用、显存、温度、功耗、编码路数）、CPU 温度到表格（CSV），
# -Report 看最近一段的平均、最高和提醒。
#   开始记（放后台，一直记）：powershell -ExecutionPolicy Bypass -File monitor.ps1
#   看汇总：                  powershell -ExecutionPolicy Bypass -File monitor.ps1 -Report -Minutes 5
#   只记一次就退：            powershell -ExecutionPolicy Bypass -File monitor.ps1 -Once
#   停：                      powershell -ExecutionPolicy Bypass -File monitor.ps1 -Stop
# CPU 温度：Windows 自己不给，要开着 LibreHardwareMonitor（以管理员身份运行，最小化开着就行），本脚本从它读；没开就只记别的几样。
#   0.9.6 起它没有 WMI：要在它的菜单 Options → Remote Web Server → Run 打开网页接口（默认 8085 端口），本脚本从 http://localhost:8085/data.json 读。
# 记录文件默认 %USERPROFILE%\wordfilm-monitor.csv（用 Excel 能直接打开），超过 20 MB 自动改名成 .old.csv 重新记。
# 省 token：-Report -Short 只打一行
param([int]$Every = 10, [string]$Log = "", [switch]$Report, [int]$Minutes = 10, [switch]$Once, [switch]$Stop, [switch]$Short, [int]$LhmPort = 8085)
if (-not $Log) { $Log = Join-Path ([Environment]::GetFolderPath('UserProfile')) 'wordfilm-monitor.csv' }

function Get-Mine {
  try {
    Get-CimInstance Win32_Process -Filter "Name='powershell.exe' OR Name='pwsh.exe'" -ErrorAction Stop |
      Where-Object { $_.CommandLine -like '*monitor.ps1*' -and $_.CommandLine -notlike '*-Stop*' -and $_.CommandLine -notlike '*-Report*' -and $_.CommandLine -notlike '*-Once*' -and $_.ProcessId -ne $PID }
  } catch { @() }
}

if ($Stop) {
  $m = @(Get-Mine)
  $m | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
  Write-Output ("停了 {0} 个记录进程" -f $m.Count); exit 0
}

function Fmt($v, $f) { if ($null -eq $v -or "$v".Trim() -eq '' -or "$v" -match 'N/A|Not Supported|\[') { return '' }; try { return ($f -f [double]$v) } catch { return '' } }

function Get-Sample {
  $r = [ordered]@{}
  $r['时间'] = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
  $r['CPU%'] = ''
  try { $p = Get-CimInstance Win32_PerfFormattedData_PerfOS_Processor -Filter "Name='_Total'" -ErrorAction Stop; $r['CPU%'] = [string][int]$p.PercentProcessorTime } catch {}
  $r['内存已用GB'] = ''; $r['内存总GB'] = ''; $r['内存%'] = ''
  try {
    $os = Get-CimInstance Win32_OperatingSystem -ErrorAction Stop
    $tot = $os.TotalVisibleMemorySize / 1MB; $free = $os.FreePhysicalMemory / 1MB
    $r['内存已用GB'] = '{0:0.0}' -f ($tot - $free); $r['内存总GB'] = '{0:0.0}' -f $tot; $r['内存%'] = [string][int](100 * ($tot - $free) / $tot)
  } catch {}
  $r['WSL内存GB'] = ''
  try { $w = Get-Process -Name vmmemWSL, vmmem -ErrorAction SilentlyContinue | Measure-Object WorkingSet64 -Sum; if ($w.Count) { $r['WSL内存GB'] = '{0:0.0}' -f ($w.Sum / 1GB) } } catch {}
  foreach ($k in '显卡%', '显存已用MB', '显存总MB', '显卡温度', '显卡功耗W', '编码路数') { $r[$k] = '' }
  try {
    $smi = (Get-Command nvidia-smi -ErrorAction SilentlyContinue).Source
    if (-not $smi -and (Test-Path "$env:WINDIR\System32\nvidia-smi.exe")) { $smi = "$env:WINDIR\System32\nvidia-smi.exe" }
    if ($smi) {
      $out = & $smi --query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw,encoder.stats.sessionCount --format=csv,noheader,nounits 2>$null
      if ($LASTEXITCODE -ne 0 -or -not $out) { $out = & $smi --query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw --format=csv,noheader,nounits 2>$null }
      $f = @((@($out)[0] -split ',') | ForEach-Object { $_.Trim() })
      $r['显卡%'] = Fmt $f[0] '{0:0}'; $r['显存已用MB'] = Fmt $f[1] '{0:0}'; $r['显存总MB'] = Fmt $f[2] '{0:0}'
      $r['显卡温度'] = Fmt $f[3] '{0:0}'; $r['显卡功耗W'] = Fmt $f[4] '{0:0}'
      if ($f.Count -gt 5) { $r['编码路数'] = Fmt $f[5] '{0:0}' }
    }
  } catch {}
  $r['CPU温度'] = ''; $r['CPU温度来源'] = ''
  try {
    $s = @(Get-CimInstance -Namespace root/LibreHardwareMonitor -ClassName Sensor -ErrorAction Stop | Where-Object { $_.SensorType -eq 'Temperature' -and $_.Identifier -like '*cpu*' })
    $pk = $s | Where-Object { $_.Name -match 'Package|Core Max|Tctl|CPU Total' } | Sort-Object Value -Descending | Select-Object -First 1
    if (-not $pk) { $pk = $s | Sort-Object Value -Descending | Select-Object -First 1 }
    if ($pk) { $r['CPU温度'] = '{0:0}' -f [double]$pk.Value; $r['CPU温度来源'] = 'LibreHardwareMonitor ' + $pk.Name }
  } catch {}
  if (-not $r['CPU温度']) {
    # LibreHardwareMonitor 0.9.6 起没有 WMI 了：从它自带的网页接口读（Options → Remote Web Server → Run，默认 8085 端口）
    try {
      $j = Invoke-RestMethod -Uri ("http://localhost:{0}/data.json" -f $LhmPort) -TimeoutSec 2 -ErrorAction Stop
      $best = $null
      function Walk($n, $hw) {
        if ($null -eq $n) { return }
        $h = $hw
        if ("$($n.ImageURL)" -match 'cpu' -or "$($n.Text)" -match 'Intel|AMD|Ryzen|Core\(TM\)|Core Ultra') { $h = $true }
        $isT = ("$($n.Type)" -eq 'Temperature') -or ("$($n.SensorId)" -match '/temperature/') -or ("$($n.Value)" -match '°C')
        if ($h -and $isT -and "$($n.Text)" -match 'CPU Package|Core Max|Tctl|Tdie|CPU Total') {
          $m = [regex]::Match("$($n.Value)", '[0-9]+([.,][0-9]+)?')
          if ($m.Success) {
            $v = [double]($m.Value -replace ',', '.')
            if (-not $script:best -or $v -gt $script:best.V) { $script:best = @{ V = $v; N = "$($n.Text)" } }
          }
        }
        foreach ($c in @($n.Children)) { Walk $c $h }
      }
      $script:best = $null
      Walk $j $false
      if ($script:best) { $r['CPU温度'] = '{0:0}' -f $script:best.V; $r['CPU温度来源'] = 'LibreHardwareMonitor 网页 ' + $script:best.N }
    } catch {}
  }
  if (-not $r['CPU温度']) {
    try {
      $z = Get-CimInstance -Namespace root/wmi -ClassName MSAcpi_ThermalZoneTemperature -ErrorAction Stop | Sort-Object CurrentTemperature -Descending | Select-Object -First 1
      if ($z) { $r['CPU温度'] = '{0:0}' -f ($z.CurrentTemperature / 10 - 273.15); $r['CPU温度来源'] = '主板温区（不一定是 CPU）' }
    } catch {}
  }
  [pscustomobject]$r
}

function Write-Sample($o) {
  $utf8 = New-Object System.Text.UTF8Encoding($true)
  if ((Test-Path $Log) -and ((Get-Item $Log).Length -gt 20MB)) { Move-Item $Log ($Log -replace '\.csv$', '.old.csv') -Force }
  $lines = @($o | ConvertTo-Csv -NoTypeInformation)
  if (-not (Test-Path $Log)) { [System.IO.File]::WriteAllText($Log, ($lines -join "`r`n") + "`r`n", $utf8) }
  else { [System.IO.File]::AppendAllText($Log, $lines[-1] + "`r`n", (New-Object System.Text.UTF8Encoding($false))) }
}

if ($Report) {
  if (-not (Test-Path $Log)) { Write-Output "还没有记录：先开始记（不带参数运行 monitor.ps1）"; exit 1 }
  $since = (Get-Date).AddMinutes(-$Minutes)
  $rows = @(Import-Csv $Log -Encoding UTF8 | Where-Object { try { [datetime]$_.'时间' -ge $since } catch { $false } })
  if ($rows.Count -eq 0) { Write-Output "最近 $Minutes 分钟没有记录（记录在跑吗？不带参数运行 monitor.ps1 开始记）"; exit 1 }
  function St($col) {
    $v = @($rows | ForEach-Object { $_.$col } | Where-Object { "$_".Trim() -ne '' } | ForEach-Object { [double]$_ })
    if ($v.Count -eq 0) { return $null }
    return @{ Avg = ($v | Measure-Object -Average).Average; Max = ($v | Measure-Object -Maximum).Maximum }
  }
  function Two($s, $unit) { if ($s) { return ('{0:0}{2} / {1:0}{2}' -f $s.Avg, $s.Max, $unit) } else { return '没读到' } }
  $cpu = St 'CPU%'; $ct = St 'CPU温度'; $mem = St '内存%'; $wsl = St 'WSL内存GB'; $g = St '显卡%'; $vm = St '显存已用MB'; $gt = St '显卡温度'; $gw = St '显卡功耗W'; $en = St '编码路数'
  $last = $rows[-1]
  if ($Short) {
    function T2($s, $u) { if ($s) { return ('{0:0}/{1:0}{2}' -f $s.Avg, $s.Max, $u) } else { return '—' } }
    $w = @()
    if ($ct -and $ct.Max -ge 100) { $w += '⚠CPU太热' } elseif ($ct -and $ct.Max -ge 95) { $w += '⚠CPU偏热' }
    if ($mem -and $mem.Max -ge 95) { $w += '⚠内存快满' } elseif ($mem -and $mem.Max -ge 90) { $w += '内存偏高' }
    if ($gt -and $gt.Max -ge 85) { $w += '⚠显卡偏热' }
    Write-Output ('电脑（近{0}分钟 平均/最高）：CPU {1}，温度 {2}，内存 {3}，显卡 {4}、{5}{6}' -f $Minutes, (T2 $cpu '%'), (T2 $ct '°C'), (T2 $mem '%'), (T2 $g '%'), (T2 $gt '°C'), $(if ($w.Count) { ' ' + ($w -join ' ') } else { ' ✅' }))
    exit 0
  }
  Write-Output ("最近 {0} 分钟（{1} 条记录，{2} ~ {3}）    平均 / 最高" -f $Minutes, $rows.Count, $rows[0].'时间'.Substring(11), $last.'时间'.Substring(11))
  Write-Output ("  CPU 占用      " + (Two $cpu '%'))
  if ($ct) { Write-Output ("  CPU 温度      " + (Two $ct '°C') + '（' + $last.'CPU温度来源' + '）') } else { Write-Output "  CPU 温度      没读到（要开着 LibreHardwareMonitor，以管理员身份运行）" }
  Write-Output ("  内存          " + (Two $mem '%') + ('（共 {0} GB；WSL 现在占 {1} GB）' -f $last.'内存总GB', $last.'WSL内存GB'))
  Write-Output ("  显卡占用      " + (Two $g '%') + ('；显存 {0} MB（共 {1} MB）' -f $last.'显存已用MB', $last.'显存总MB'))
  Write-Output ("  显卡温度      " + (Two $gt '°C') + '；功耗 ' + (Two $gw ' W') + $(if ($en) { '；编码最多 {0:0} 路' -f $en.Max } else { '' }))
  $warn = @()
  if ($ct -and $ct.Max -ge 100) { $warn += '⚠ CPU 太热（到过 100°C）：会自动降频变慢。清灰、查散热；或少开浏览器：batch.sh set <批次> RENDER_JOBS=8' }
  elseif ($ct -and $ct.Max -ge 95) { $warn += '⚠ CPU 温度偏高（到过 95°C）：留意散热，持续这样就把 RENDER_JOBS 调成 8' }
  if ($mem -and $mem.Max -ge 95) { $warn += '⚠ 内存快满（到过 95%）：出片进程可能被系统停掉。关掉不用的程序（抖音、浏览器、千问…），或 RENDER_JOBS 调小' }
  elseif ($mem -and $mem.Max -ge 90) { $warn += '提醒：内存到过 90%，关掉不用的程序会稳一些' }
  if ($gt -and $gt.Max -ge 85) { $warn += '⚠ 显卡偏热（到过 85°C）：看看机箱通风' }
  if ($warn.Count) { $warn | ForEach-Object { Write-Output "  $_" } } else { Write-Output "  ✅ 都正常" }
  exit 0
}

if ($Once) { $o = Get-Sample; Write-Sample $o; $o | Format-List | Out-String | Write-Output; exit 0 }

if (@(Get-Mine).Count -gt 0) { Write-Output "已经在记了（停：monitor.ps1 -Stop）"; exit 0 }
Write-Output "开始记：每 $Every 秒一条，记到 $Log（停：monitor.ps1 -Stop）"
while ($true) { try { Write-Sample (Get-Sample) } catch {}; Start-Sleep -Seconds $Every }

$ws = New-Object -ComObject WScript.Shell
$dir = 'C:\Users\user\Desktop\chuti-helper\chuti-helper'
$su = [Environment]::GetFolderPath('Startup')
foreach ($n in @('watch_start', 'runner_start')) {
    $lnk = Join-Path $su ($n + '.lnk')
    $s = $ws.CreateShortcut($lnk)
    $s.TargetPath = Join-Path $dir ($n + '.bat')
    $s.WorkingDirectory = $dir
    $s.WindowStyle = 7
    $s.Description = 'chuti helper'
    $s.Save()
    Write-Output ('created: ' + $lnk)
}
Get-ChildItem $su -Filter '*.lnk' | Select-Object -ExpandProperty Name

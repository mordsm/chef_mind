param([switch]$StartOnly)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$python = Join-Path $projectRoot '.venv/Scripts/python.exe'
$script = Join-Path $PSScriptRoot 'on_demand.py'
$runtime = Join-Path $projectRoot '.runtime'
New-Item -ItemType Directory -Force -Path $runtime | Out-Null
if (-not $StartOnly) {
    $action = New-ScheduledTaskAction -Execute $python -Argument ('"' + $script + '"') -WorkingDirectory $projectRoot
    $trigger = New-ScheduledTaskTrigger -AtLogOn -User ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name)
    $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit ([TimeSpan]::Zero) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
    Register-ScheduledTask -TaskName 'ChefMind-OnDemand' -Action $action -Trigger $trigger -Settings $settings -Description 'Chef network gateway and connector; starts the kitchen on incoming requests.' -Force | Out-Null
}
$listener = Get-NetTCPConnection -State Listen -LocalPort 8800 -ErrorAction SilentlyContinue
if ($listener) {
    throw 'Port 8800 is already occupied. Stop the existing Chef launcher before starting the on-demand gateway.'
}
Start-Process -FilePath $python -ArgumentList ('"' + $script + '"') -WorkingDirectory $projectRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runtime 'on-demand.out.log') -RedirectStandardError (Join-Path $runtime 'on-demand.err.log') | Out-Null
Write-Output 'Chef on-demand gateway started on 127.0.0.1:8800.'

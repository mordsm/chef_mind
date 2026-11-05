param(
    [ValidateSet('Start', 'Status', 'Stop')]
    [string]$Action = 'Start',
    [ValidateRange(5, 60)]
    [int]$WaitSeconds = 45
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$runtime = Join-Path $projectRoot '.runtime'
$statePath = Join-Path $runtime 'cloudflare.json'
$origin = 'http://127.0.0.1:8800'

function Test-ChefUrl([string]$url) {
    try { return (Invoke-RestMethod -Uri ($url+'/health') -TimeoutSec 6).service -eq 'chef-core' }
    catch {
        if ($url.StartsWith('https://') -and (Get-Command node -ErrorAction SilentlyContinue)) {
            $priorChefCa = $env:NODE_USE_SYSTEM_CA
            try {
                $env:NODE_USE_SYSTEM_CA = '1'
                & node -e "fetch(process.argv[1]+'/health',{signal:AbortSignal.timeout(6000)}).then(r=>r.json()).then(d=>process.exit(d.service==='chef-core'?0:1)).catch(()=>process.exit(1))" $url | Out-Null
                return $LASTEXITCODE -eq 0
            } finally { $env:NODE_USE_SYSTEM_CA = $priorChefCa }
        }
        return $false
    }
}

function Get-TunnelState {
    if (Test-Path -LiteralPath $statePath) {
        return Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
    }
    return $null
}

function Get-OwnedTunnel($state) {
    if (-not $state) { return $null }
    $candidate = Get-Process -Id $state.process_id -ErrorAction SilentlyContinue
    if ($candidate -and $candidate.ProcessName -eq 'cloudflared' -and
        $candidate.Path -eq $state.executable -and
        $candidate.StartTime.ToUniversalTime().ToString('o') -eq $state.started_at) {
        return $candidate
    }
    return $null
}

$state = Get-TunnelState
$existing = Get-OwnedTunnel $state
if ($Action -eq 'Stop') {
    if ($existing) {
        $existing.Kill()
        $existing.WaitForExit(5000) | Out-Null
        Write-Output 'Chef Cloudflare tunnel stopped. The local Chef server is unchanged.'
    } else {
        Write-Output 'No running Chef Cloudflare tunnel.'
    }
    exit 0
}
if ($Action -eq 'Status') {
    if (-not $existing) { Write-Output 'Chef Cloudflare tunnel is not running.'; exit 1 }
    if (-not (Test-ChefUrl $origin) -or -not (Test-ChefUrl $state.url)) {
        Write-Output 'Chef remote access is unavailable; run Start to repair it.'; exit 1
    }
    Write-Output $state.url
    exit 0
}
if ($existing) {
    if ((Test-ChefUrl $origin) -and (Test-ChefUrl $state.url)) {
        @('[InternetShortcut]', ('URL='+$state.url)) | Set-Content -LiteralPath (Join-Path $runtime 'Chef-Remote.url') -Encoding ASCII
        Write-Output $state.url
        exit 0
    }
    $existing.Kill()
    $existing.WaitForExit(5000) | Out-Null
}

try {
    $health = Invoke-RestMethod -Uri "$origin/health" -TimeoutSec 5
    if ($health.service -ne 'chef-core') { throw 'The origin is not Chef Core.' }
} catch {
    New-Item -ItemType Directory -Path $runtime -Force | Out-Null
    $python = Join-Path $projectRoot '.venv\Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $python)) { throw 'Install Chef dependencies before starting remote access.' }
    $previousPythonPath = $env:PYTHONPATH
    try {
        $env:PYTHONPATH = Join-Path $projectRoot 'backend'
        Start-Process -FilePath $python -ArgumentList @('-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8800') `
            -WorkingDirectory $projectRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runtime 'chef-remote.out.log') `
            -RedirectStandardError (Join-Path $runtime 'chef-remote.err.log') | Out-Null
    } finally { $env:PYTHONPATH = $previousPythonPath }
    $serverDeadline = (Get-Date).AddSeconds(20)
    while (-not (Test-ChefUrl $origin) -and (Get-Date) -lt $serverDeadline) { Start-Sleep -Milliseconds 500 }
    if (-not (Test-ChefUrl $origin)) { throw 'Chef did not start; see .runtime/chef-remote.err.log' }
}
$command = Get-Command cloudflared -ErrorAction SilentlyContinue
$executable = if ($command) { $command.Source } else { 'C:\Program Files (x86)\cloudflared\cloudflared.exe' }
if (-not (Test-Path -LiteralPath $executable)) {
    throw 'Install cloudflared, then run this script again.'
}
New-Item -ItemType Directory -Path $runtime -Force | Out-Null
$runId = [guid]::NewGuid().ToString('N')
$outLog = Join-Path $runtime "cloudflare-$runId.out.log"
$errLog = Join-Path $runtime "cloudflare-$runId.err.log"
$tunnelProcess = Start-Process -FilePath $executable -ArgumentList @(
    'tunnel', '--no-autoupdate', '--protocol', 'auto', '--edge-ip-version', '4', '--url', $origin
) -WorkingDirectory $projectRoot -WindowStyle Hidden -RedirectStandardOutput $outLog `
    -RedirectStandardError $errLog -PassThru
$startedAt = $tunnelProcess.StartTime.ToUniversalTime().ToString('o')
$deadline = (Get-Date).AddSeconds($WaitSeconds)
while ((Get-Date) -lt $deadline) {
    $tunnelProcess.Refresh()
    if ($tunnelProcess.HasExited) { throw "cloudflared exited. See $errLog" }
    $logs = @($outLog, $errLog) | ForEach-Object {
        if (Test-Path -LiteralPath $_) { Get-Content -LiteralPath $_ -Raw }
    }
    $match = [regex]::Match(($logs -join "`n"), 'https://[a-z0-9-]+\.trycloudflare\.com')
    if ($match.Success -and ($logs -join "`n") -match 'Registered tunnel connection') {
        $state = [ordered]@{
            process_id = $tunnelProcess.Id
            executable = $executable
            started_at = $startedAt
            url = $match.Value
            origin = $origin
            stdout_log = $outLog
            stderr_log = $errLog
        }
        $state | ConvertTo-Json | Set-Content -LiteralPath $statePath -Encoding UTF8
        @('[InternetShortcut]', ('URL='+$match.Value)) | Set-Content -LiteralPath (Join-Path $runtime 'Chef-Remote.url') -Encoding ASCII
        Write-Output $match.Value
        exit 0
    }
    Start-Sleep -Milliseconds 500
}
# Do not leave an unmanaged background connector after a failed startup.
if (-not $tunnelProcess.HasExited) { $tunnelProcess.Kill() }
throw "Cloudflare did not allocate a URL within $WaitSeconds seconds. See $errLog"

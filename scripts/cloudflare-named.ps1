param(
    [ValidateSet('Prepare', 'Start', 'Status', 'Stop')]
    [string]$Action = 'Status',
    [string]$Hostname,
    [string]$TokenFile,
    [ValidateRange(5, 60)][int]$WaitSeconds = 45
)

# Remotely-managed named tunnel. Configure the public hostname in Cloudflare first.
# The token stays in an ignored file; it is never printed or passed on the command line.
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$runtime = Join-Path $projectRoot '.runtime'
$statePath = Join-Path $runtime 'cloudflare-named.json'
$origin = 'http://127.0.0.1:8800'

function Test-ChefUrl([string]$url) {
    try { return (Invoke-RestMethod -Uri ($url+'/health') -TimeoutSec 5).service -eq 'chef-core' }
    catch { return $false }
}

$state = if (Test-Path -LiteralPath $statePath) { Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json } else { $null }
$existing = $null
if ($state) {
    $candidate = Get-Process -Id $state.process_id -ErrorAction SilentlyContinue
    if ($candidate -and $candidate.ProcessName -eq 'cloudflared' -and
        $candidate.Path -eq $state.executable -and
        $candidate.StartTime.ToUniversalTime().ToString('o') -eq $state.started_at) { $existing = $candidate }
}
if ($Action -eq 'Stop') {
    if ($existing) { $existing.Kill(); $existing.WaitForExit(5000) | Out-Null }
    Write-Output 'Only the recorded Chef named tunnel was stopped; Chef remains unchanged.'
    exit 0
}
if ($Action -eq 'Status') {
    if (-not $existing) { Write-Output 'The Chef named tunnel is not running.'; exit 1 }
    if (-not (Test-ChefUrl $origin) -or -not (Test-ChefUrl $state.url)) { Write-Output 'Named tunnel health check failed.'; exit 1 }
    Write-Output ($state.url+'/report/')
    exit 0
}
if (-not $Hostname -or $Hostname.Length -gt 253 -or $Hostname -notmatch '^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?\.[a-z]{2,}$' -or $Hostname.EndsWith('.trycloudflare.com')) {
    throw 'Provide your fixed public hostname, for example chef.example.com.'
}
if ($Action -eq 'Prepare') {
    New-Item -ItemType Directory -Path $runtime -Force | Out-Null
    [ordered]@{ hostname=$Hostname; service=$origin; page="https://$Hostname/report/" } |
        ConvertTo-Json | Set-Content -LiteralPath (Join-Path $runtime 'cloudflare-named-route.json') -Encoding UTF8
    Write-Output 'Routing plan prepared. Create a named tunnel in Cloudflare, publish the hostname to http://127.0.0.1:8800, and save its connector token in a private file.'
    exit 0
}
if ($existing) {
    if ($state.url -ne "https://$Hostname") { throw 'Stop the recorded tunnel before changing its hostname.' }
    if ((Test-ChefUrl $origin) -and (Test-ChefUrl $state.url)) { Write-Output ($state.url+'/report/'); exit 0 }
    throw 'The recorded tunnel is running but unhealthy. Inspect Cloudflare routing, then use Stop before restarting.'
}
if (-not (Test-ChefUrl $origin)) { throw 'Start and migrate Chef first; localhost health is unavailable.' }
if (-not $TokenFile -or -not (Test-Path -LiteralPath $TokenFile -PathType Leaf)) { throw 'Provide -TokenFile pointing to the private connector-token file.' }
$resolvedTokenFile = (Resolve-Path -LiteralPath $TokenFile).Path
$command = Get-Command cloudflared -ErrorAction SilentlyContinue
$executable = if ($command) { $command.Source } else { 'C:\Program Files (x86)\cloudflared\cloudflared.exe' }
if (-not (Test-Path -LiteralPath $executable)) { throw 'Install cloudflared first.' }
New-Item -ItemType Directory -Path $runtime -Force | Out-Null
$runId = [guid]::NewGuid().ToString('N')
$outLog = Join-Path $runtime "named-$runId.out.log"
$errLog = Join-Path $runtime "named-$runId.err.log"
$tunnelProcess = Start-Process -FilePath $executable -ArgumentList @(
    'tunnel', '--no-autoupdate', 'run', '--token-file', ('"'+$resolvedTokenFile+'"')
) -WorkingDirectory $projectRoot -WindowStyle Hidden -RedirectStandardOutput $outLog -RedirectStandardError $errLog -PassThru
$startedAt = $tunnelProcess.StartTime.ToUniversalTime().ToString('o')
$deadline = (Get-Date).AddSeconds($WaitSeconds)
while ((Get-Date) -lt $deadline) {
    $tunnelProcess.Refresh()
    if ($tunnelProcess.HasExited) { throw "The named tunnel exited. Inspect $errLog locally." }
    if (Test-ChefUrl "https://$Hostname") {
        [ordered]@{process_id=$tunnelProcess.Id; executable=$executable; started_at=$startedAt; url="https://$Hostname"} |
            ConvertTo-Json | Set-Content -LiteralPath $statePath -Encoding UTF8
        Write-Output "https://$Hostname/report/"
        exit 0
    }
    Start-Sleep -Milliseconds 500
}
if (-not $tunnelProcess.HasExited) { $tunnelProcess.Kill() }
throw 'The fixed hostname did not reach Chef. Check the published hostname, origin port and connector token.'

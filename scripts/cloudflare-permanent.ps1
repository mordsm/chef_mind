param(
    [ValidateSet('Login','Deploy','Sync','Status')][string]$Action = 'Status'
)

# Stable workers.dev gateway; Python/data stay on this computer.
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$runtime = Join-Path $projectRoot '.runtime'
$workerConfig = Join-Path $projectRoot 'infra/cloudflare-gateway/wrangler.jsonc'
New-Item -ItemType Directory -Path $runtime -Force | Out-Null
$env:npm_config_cache = Join-Path $runtime 'npm-cache'
$env:XDG_CONFIG_HOME = Join-Path $runtime 'cloudflare-config'
$env:NODE_USE_SYSTEM_CA = '1'
$env:npm_config_fetch_retries = '1'
$env:npm_config_fetch_timeout = '20000'
$env:WRANGLER_SEND_METRICS = 'false'

function Test-PermanentChef([string]$url) {
    & node -e "fetch(process.argv[1]+'/health',{signal:AbortSignal.timeout(10000)}).then(r=>r.json()).then(d=>process.exit(d.service==='chef-core'?0:1)).catch(()=>process.exit(1))" $url | Out-Null
    if ($LASTEXITCODE -eq 0) { return $true }
    $probePython = Join-Path $projectRoot '.venv/Scripts/python.exe'
    $probeScript = Join-Path $PSScriptRoot 'check_remote_health.py'
    if (Test-Path -LiteralPath $probePython) {
        & $probePython $probeScript $url | Out-Null
        return $LASTEXITCODE -eq 0
    }
    return $false
}

if ($Action -eq 'Login') {
    & npx.cmd --yes wrangler@4.152.0 login --device --browser=false --scopes account:read user:read workers_scripts:write
    if ($LASTEXITCODE -ne 0) { throw 'Cloudflare login did not complete.' }
    exit 0
}
if ($Action -eq 'Status') {
    & npx.cmd --yes wrangler@4.152.0 whoami
    if ($LASTEXITCODE -ne 0) { throw 'Cloudflare authentication is unavailable.' }
    $urlFile = Join-Path $runtime 'permanent-cloudflare-url.txt'
    if (Test-Path -LiteralPath $urlFile) {
        $url = (Get-Content -LiteralPath $urlFile -Raw).Trim()
        try {
            if (-not (Test-PermanentChef $url)) { throw 'Not Chef Core.' }
            Write-Output "$url/report/"
        } catch { throw 'The permanent address is saved, but the kitchen origin is unavailable. Run Sync.' }
    }
    exit 0
}

# This repair helper reuses a healthy Quick Tunnel or replaces a failed one.
# Only its recorded connector is managed; account login remains explicit.
$origin = & (Join-Path $PSScriptRoot 'cloudflare.ps1') -Action Start
$origin = ($origin | Select-Object -Last 1).ToString().Trim()
if ($origin -notmatch '^https://[a-z0-9-]+\.trycloudflare\.com$') { throw 'A healthy Chef tunnel origin was not returned.' }
if ($Action -eq 'Deploy') {
    $output = & npx.cmd --yes wrangler@4.152.0 deploy --config $workerConfig 2>&1
    $output | ForEach-Object { Write-Output $_ }
    if ($LASTEXITCODE -ne 0) { throw 'The Worker deployment failed; finish Cloudflare Login first.' }
    $match = [regex]::Match(($output -join "`n"), 'https://[a-z0-9-]+\.[a-z0-9-]+\.workers\.dev')
    if (-not $match.Success) { throw 'Deployment returned no workers.dev address; inspect Wrangler output.' }
    $match.Value | Set-Content -LiteralPath (Join-Path $runtime 'permanent-cloudflare-url.txt') -Encoding ASCII
}
$urlPath = Join-Path $runtime 'permanent-cloudflare-url.txt'
if (-not (Test-Path -LiteralPath $urlPath)) { throw 'Deploy the permanent gateway before running Sync.' }
# An origin URL is configuration, not a user credential. Passing stdin avoids command interpolation.
$origin | & npx.cmd --yes wrangler@4.152.0 secret put CHEF_ORIGIN --config $workerConfig
if ($LASTEXITCODE -ne 0) { throw 'Could not update the gateway origin; the permanent address has not changed.' }
$url = (Get-Content -LiteralPath $urlPath -Raw).Trim()
if (-not (Test-PermanentChef $url)) { throw 'The permanent gateway did not reach Chef Core.' }
@('[InternetShortcut]', "URL=$url/report/") | Set-Content -LiteralPath (Join-Path $runtime 'Chef-Permanent.url') -Encoding ASCII
Write-Output "$url/report/"

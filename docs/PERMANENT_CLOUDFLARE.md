# Permanent Cloudflare address without purchasing a domain

The gateway in `infra/cloudflare-gateway` gives the existing Chef application a stable `https://chef-mind-gateway.<account-subdomain>.workers.dev` address. A Cloudflare account and its Workers subdomain are required. No purchased domain is required for this Workers address.

This is a gateway, not migration of Python/PostgreSQL hosting to Cloudflare. Chef and its database still run on this computer, which must remain powered, online and awake. The upstream connection is a Quick Tunnel; its hostname may change. Updating the gateway origin leaves the public Workers address and PWA browser storage origin unchanged. Quick Tunnels retain their availability and service limitations; the stable gateway does not turn them into a production-grade named tunnel.

## Set up

```powershell
cd C:\workspace\chef_mind
.\scripts\cloudflare-permanent.ps1 -Action Login
.\scripts\cloudflare-permanent.ps1 -Action Deploy
```

Login prints a Cloudflare device verification link and a short-lived code. Open the link, enter the code and sign in to your own account. This device flow does not depend on a reachable localhost callback. Tokens are stored under ignored `.runtime/cloudflare-config`; do not paste tokens into chat. Deploy creates or updates the specifically named `chef-mind-gateway` Worker in the authorized account. Its initial origin is unavailable until configuration is applied and verified. Worker observability is disabled so report contents/authorization headers are not intentionally logged.

The deployment prints the real permanent URL after both gateway and origin health checks succeed. It also creates the local `.runtime/Chef-Permanent.url` shortcut. The account's Workers subdomain must be set up if Cloudflare asks for it. Do not assume a placeholder URL is active.

## Reconnect after a tunnel change

### Automatic start on access (Windows)

Run `powershell -ExecutionPolicy Bypass -File scripts/install-on-demand.ps1` once.
The `ChefMind-OnDemand` task starts the loopback gateway at Windows sign-in and
restarts it after a failure. The computer must be awake, online and signed in.
Port 8800 belongs to this gateway; do not also launch the old server on that port.
Incoming application requests start the installed `chef-mind-db-1` container
(checked against the database port in `.env`) and Chef on loopback port 8801.
Existing volumes and migrations are preserved. Set `CHEF_DB_CONTAINER` in the
gateway environment if the installed container has a different name.

During startup, HTML navigation displays a waiting page and checks every three
seconds, reloading the original URL only after `/ready` succeeds. Failed API writes
receive 503 with Retry-After and are never replayed by the gateway. Connector
health checks do not start Chef. Docker Desktop is started if necessary, so a cold
start can take longer than an ordinary application start. The gateway launches
the existing connector watchdog, which repairs the tunnel while preserving the
Workers address. Recovery from a disconnected tunnel is checked every 30 seconds
and can take longer; Cloudflare authorization must remain valid.

Logs are `.runtime/on-demand*.log` and `.runtime/cloudflare-watchdog.json`.
The gateway's `/health` describes gateway liveness; `/ready` checks Chef storage.

```powershell
.\scripts\cloudflare-permanent.ps1 -Action Sync
.\scripts\cloudflare-permanent.ps1 -Action Status
```

Sync reuses/repairs the local tunnel and updates `CHEF_ORIGIN` in the existing Worker. It never changes the public Workers hostname. For automatic recovery while the computer is running, use `uv run python scripts/cloudflare_keepalive.py --watch`; one instance is allowed, with status in `.runtime/cloudflare-watchdog.json`. It checks every thirty seconds and retains the existing Workers address. Authentication may need renewal. It is not a reboot/startup service. The Worker forwards the application and APIs without caching private responses; the existing application authentication is still required. Install the PWA from the permanent `/report/` address on both devices.

If you later supply your own Cloudflare-managed domain, prefer the ordinary named tunnel in `scripts/cloudflare-named.ps1`, which avoids the Quick Tunnel origin dependency.

References: [Workers default addresses](https://developers.cloudflare.com/workers/configuration/routing/workers-dev/), [Worker reverse proxy example](https://developers.cloudflare.com/workers/examples/respond-with-another-site/), [Quick Tunnel limitations](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/).

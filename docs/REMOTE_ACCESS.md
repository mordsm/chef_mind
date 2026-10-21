# Remote access through Cloudflare

From PowerShell, with Chef already running locally:

```powershell
cd C:\workspace\chef_mind
.\scripts\cloudflare.ps1 -Action Start
```

The command starts Chef if it is stopped, then starts `cloudflared` hidden in
the background and prints the public HTTPS URL. Open that URL from your phone
or another computer. Start reuses the existing tunnel only when both the local
service and public HTTPS health endpoint respond; otherwise it repairs the
connection with a new URL. This is a manual repair command, not an unattended
watchdog. The local Chef service remains bound to
`127.0.0.1:8800`; no router port forwarding is needed.

```powershell
.\scripts\cloudflare.ps1 -Action Status
.\scripts\cloudflare.ps1 -Action Stop
```

Status checks actual local and public connectivity before printing the URL;
it reports failure when a process exists but its connection has failed. Start
also writes `.runtime/Chef-Remote.url` as a shortcut to the current address.
Stop closes only the tunnel created by this
script; it does not stop Chef or other Cloudflare tunnels. Process identity is
checked before reuse or stopping. Runtime state and logs live under ignored
`.runtime/` and contain no Chef access tokens.

This is a **Quick Tunnel**: the URL changes when a new tunnel is created. Keep
this computer awake, Chef running, and the connector running. Quick Tunnels
are intended for temporary access and do not have an availability guarantee.
See [Cloudflare's Quick Tunnel documentation](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/).

The public URL provides the guest cooking interface and the original YAML
sources. Private inventory, saved journeys and editing still require your Chef
access token. Enter it in **חיבור למטבח האישי ושחזור מלאי** on the remote device;
never add a token to the URL. Local browser inventory from `127.0.0.1` is a
different browser storage area and is not transferred automatically to the
public URL. Server-saved private data is available after connecting as the same
user.

For a stable address, configure a named tunnel and hostname in your own
Cloudflare account, pointing to `http://127.0.0.1:8800`. Cloudflare Access can
restrict that hostname to selected users. Account/domain setup is separate from
this temporary tunnel; no account credentials or DNS settings are changed by
this script.

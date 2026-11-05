# Cooking action reporting PWA

This is one responsive Hebrew/RTL application served by the existing FastAPI service at `/report/`. A link is also available from a cooking journey. The account's access token must be entered in each device; tokens remain in page memory and are never put in IndexedDB, service-worker caches, URLs or generated exports.

## Run locally

From the project directory, with the existing database and `.env` configured:

```powershell
uv sync --locked
$env:PYTHONPATH='backend'
uv run alembic upgrade head
uv run uvicorn app.main:app --host 127.0.0.1 --port 8800
```

Open `http://127.0.0.1:8800/report/`. For phone access, use a public HTTPS address. Use the same account and choose the same cooking session on both devices. An unlinked session is given a timestamp label, with no typed title needed. New cooking sessions appear in the other device's selector within ten seconds; changes within the selected session use authenticated long polling, checked every 400 ms on the server, without holding database connections during the wait.

Desktop/Android: choose the browser's Install option or the app's install button when offered. iPhone/iPad: open the HTTPS address in Safari, Share -> Add to Home Screen, then launch from that icon. First load needs connectivity so the service worker can cache the application shell. Close existing app tabs and reopen to activate a new shell version after an update.

## Reports and configuration

`backend/app/static/report/actions.json` defines ingredients, action names/icons, defaults, numeric presets/bounds, choice lists and automatic-timer behavior. The initial actions are cooking, cutting and adding an ingredient. Supported field types are `number`, `choice` and `ingredient`. Add an action using those field types without changing the UI. A timer action needs a numeric `duration` field measured in minutes. Bump the configuration version when changing its contract; unsynchronized reports from an incompatible old contract are retained for explicit correction.

All structured values come from choices or numeric controls. The only free-text field in a report is the optional note, which is stored and displayed without interpreting it. A temperature is the reported appliance setting, not a measured food temperature. It defaults to unknown for a pot; values such as 160/180/200 are available as buttons. Defaults and the last confirmed values are conveniences for the cook to review, not inferred observations.

Reports include client-generated IDs, action/config version, parameters, observed start, optional reported finish, planned timer deadline, notes, owner and cooking/recipe IDs. Server receipt time and optimistic revisions are recorded separately. Timers start after successful local save. Several timers may run together; expiry does not finish a cooking operation. Editing duration recalculates the deadline from the original start. The “finished now” button records the actual reported end. Deletion stops its timer and synchronizes a tombstone.

## Offline sync and conflicts

IndexedDB stores account-partitioned sessions, reports and a transactionally ordered outbox. With the application open, reconnect triggers automatic replay. Stable retry IDs prevent duplication after a lost response. Edits and deletes made offline are queued in revision order. Another device's conflicting edit is preserved: choose its version or open your local version as a new report for review. Notes are never fed into a model or used to determine parameter values.

After closing/reopening, the last account's local data can be used offline. Enter that account's token again to resume server synchronization. Pending offline timers cannot generate a server push until they have reached the server. Signing out hides that account's data and invalidates the browser push subscription. Saved data remains on that device; the application does not claim encryption of local IndexedDB contents.

## Notifications with the app closed

Web Push is implemented in `backend/app/web_push.py` and `/report/sw.js`. It uses a persistent timer deadline, account/device subscriptions, leased delivery attempts, retry backoff, cancellation after timer changes and deactivation of expired endpoints. Notification tags collapse repeated delivery. Lock-screen notifications omit private notes and ingredient details.

Generate a private key without overwriting an existing key:

```powershell
uv run python scripts/generate_push_keys.py
```

Only the public browser key is printed. Set these values in the private environment configuration, using the generated public key and your real contact address:

```dotenv
CHEF_PUSH_ENABLED=true
CHEF_PUSH_WORKER_ENABLED=true
CHEF_PUSH_VAPID_PRIVATE_KEY_FILE=C:/workspace/chef_mind/.runtime/webpush-private.pem
CHEF_PUSH_VAPID_PUBLIC_KEY=generated-public-key
CHEF_PUSH_VAPID_SUBJECT=mailto:your-contact@example.com
```

Restart the server, connect on each device, and press the button for notifications with the screen locked. This requests OS/browser notification permission and registers that device. The private key and connector tokens are excluded from Git; treat logical database backups as private because push subscription credentials are included.

The built-in worker requires an always-running server with CPU available while idle. It retries after transient failures and catches up eligible missed deadlines within one hour. Delivery is at least once; tags minimize duplicates. The phone needs connectivity, notification permission and platform support; focus/silent modes can suppress sound and delivery is not an exact alarm guarantee. On iOS/iPadOS, install as a Home Screen app before enabling notifications. Test a real locked device after public deployment; automated transport tests do not substitute for this.

For an externally scheduled deployment, set `CHEF_PUSH_WORKER_ENABLED=false`. Authenticated reviewers can invoke `POST /v1/action-log/push/dispatch`; ordinary cooking tokens cannot. A Cloud Scheduler invocation can dispatch due timers periodically but adds scheduling delay. Per-timer Cloud Tasks integration is a possible cost optimization; automatic task creation is not implemented in this MVP.

## Hosting

- A fixed Cloudflare **Tunnel** hostname needs your own configured domain and a running origin server. `scripts/cloudflare-named.ps1` prepares a routing plan and starts/stops only its recorded named connector, using a private token file. It does not create DNS records or publish an account configuration on your behalf. See `docs/REMOTE_ACCESS.md` for the temporary tunnel.
- Cloudflare **Pages** offers a `pages.dev` hostname without buying a domain, but a separate compatible backend is still needed for this FastAPI/PostgreSQL application.
- GitHub Pages serves static files; it cannot host this Python API/database.
- Google Cloud Run can serve the existing container at Google's HTTPS hostname without a purchased domain. Use durable PostgreSQL with pgvector support for the full existing Chef application; container-local SQLite is not persistent Cloud Run storage. Set the container port to `8000` for the existing Dockerfile and supply credentials via secrets. Run migrations separately before serving requests. The always-running timer worker requires idle CPU and a kept-alive instance, which costs more than scale-to-zero. Select an external scheduling design before claiming low-cost closed-app notifications. No cloud resources or paid services have been provisioned.

Reference docs: [Cloud Run](https://docs.cloud.google.com/run/docs/triggering/https-request), [Cloudflare Pages](https://developers.cloudflare.com/pages/configuration/custom-domains/), [WebKit push requirements](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/).

## Verification

```powershell
uv run pytest tests/test_action_log.py tests/test_web_push.py tests/test_backup.py tests/test_evaluation_and_migrations.py
uv run python scripts/check_action_log_browser.py
node --test tests/report_worker.test.cjs
```

The browser regression uses a disposable real HTTP server and two isolated browser/device contexts. It checks live sync, offline records, lost-response deduplication, concurrent edits, real service-worker offline reload, timer persistence, parallel timers, deletion, responsive touch targets and absence of stored tokens. Server push tests exercise delivery through an injected transport; actual handset permission, sound and locked-screen presentation remain deployment checks.

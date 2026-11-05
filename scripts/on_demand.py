"""Always-on loopback gateway; start Chef only when application traffic arrives."""

import asyncio
import json
import os
import subprocess
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import urlsplit

import httpx
from dotenv import dotenv_values
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from starlette.background import BackgroundTask

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".runtime"
BACKEND = "http://127.0.0.1:8801"
HIDDEN = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
HOP = {"connection", "keep-alive", "transfer-encoding", "te", "trailer", "upgrade", "host"}
WAIT = """<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>המטבח עולה</title><body style="font:22px system-ui;line-height:1.7;max-width:650px;margin:12vh auto;padding:24px;color:#173b30">
<h1>מפעילים את המטבח…</h1><p id="status">הכניסה תתבצע אוטומטית כשהמטבח מוכן. בודקים שוב בעוד 3 שניות.</p>
<p id="elapsed"></p><a href="">נסה שוב עכשיו</a>
<script>const started=Date.now();async function poll(){
document.getElementById('elapsed').textContent='זמן המתנה: '+Math.floor((Date.now()-started)/1000)+' שניות';
try{const r=await fetch('/__chef_start_status',{cache:'no-store'});const s=await r.json();
if(s.ready){location.reload();return;}
if(s.failed)document.getElementById('status').textContent='ההפעלה מתעכבת. מנסים שוב אוטומטית; אם התקלה נמשכת יש לבדוק את מחשב המטבח.';
}catch{}setTimeout(poll,3000);}setTimeout(poll,3000);</script></body></html>"""


class Launcher:
    def __init__(self):
        self.task = None
        self.process = None
        self.retry_at = 0
        self.failed = False

    async def ready(self, client):
        try:
            response = await client.get(BACKEND + "/ready", timeout=2)
            return response.status_code == 200
        except httpx.HTTPError:
            return False

    def ensure_started(self, client):
        if (self.task is None or self.task.done()) and time.monotonic() >= self.retry_at:
            self.task = asyncio.create_task(self.start(client))

    async def start(self, client):
        self.failed = False
        try:
            if await self.ready(client):
                return
            probe = await asyncio.to_thread(
                subprocess.run, ["docker", "info"], stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, creationflags=HIDDEN, timeout=15,
            )
            if probe.returncode and os.name == "nt":
                desktop = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Docker/Docker/Docker Desktop.exe"
                await asyncio.to_thread(subprocess.Popen, [str(desktop)], creationflags=HIDDEN)
                for _ in range(45):
                    await asyncio.sleep(2)
                    probe = await asyncio.to_thread(
                        subprocess.run, ["docker", "info"], stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL, creationflags=HIDDEN, timeout=15,
                    )
                    if probe.returncode == 0:
                        break
            # Restart the installed database only after matching its published port.
            config = dotenv_values(ROOT / ".env")
            database = urlsplit(os.environ.get("CHEF_DATABASE_URL") or config.get("CHEF_DATABASE_URL", ""))
            container = os.environ.get("CHEF_DB_CONTAINER", "chef-mind-db-1")
            inspected = await asyncio.to_thread(
                subprocess.run, ["docker", "inspect", container], capture_output=True,
                text=True, creationflags=HIDDEN, timeout=15,
            )
            if inspected.returncode:
                raise RuntimeError("Installed Chef database container not found")
            metadata = json.loads(inspected.stdout)[0]
            ports = metadata.get("HostConfig", {}).get("PortBindings", {}).get("5432/tcp", [])
            if database.hostname not in {"127.0.0.1", "localhost"} or not any(
                p["HostPort"] == str(database.port) for p in ports
            ):
                raise RuntimeError("Database container does not match configured local database")
            result = await asyncio.to_thread(
                subprocess.run,
                ["docker", "start", container],
                cwd=ROOT,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=HIDDEN, timeout=90,
            )
            if result.returncode:
                raise RuntimeError("Database startup failed")
            if self.process is None or self.process.poll() is not None:
                env = {**os.environ, "PYTHONPATH": str(ROOT / "backend")}
                with (RUNTIME / "on-demand-backend.log").open("ab") as log:
                    self.process = await asyncio.to_thread(subprocess.Popen,
                        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8801"],
                        cwd=ROOT, env=env, stdout=log, stderr=log, creationflags=HIDDEN,
                    )
            for _ in range(60):
                if await self.ready(client):
                    return
                await asyncio.sleep(2)
            raise RuntimeError("Chef readiness timeout")
        except (OSError, RuntimeError, subprocess.SubprocessError):
            self.failed = True
            self.retry_at = time.monotonic() + 30


launcher = Launcher()


@asynccontextmanager
async def lifespan(app):
    RUNTIME.mkdir(exist_ok=True)
    # This client connects exclusively to fixed loopback HTTP, never to HTTPS.
    async with httpx.AsyncClient(timeout=60, follow_redirects=False, trust_env=False, verify=False) as client:
        app.state.client = client
        yield
        if launcher.task and not launcher.task.done():
            launcher.task.cancel()


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)


@app.api_route("/{path:path}", methods=["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
async def proxy(request: Request, path: str):
    client = request.app.state.client
    headers = {"Cache-Control": "no-store"}
    # Connector monitoring must not itself start the application.
    if path == "health":
        return JSONResponse({"service": "chef-core", "gateway": "on-demand"}, headers=headers)
    ready = await launcher.ready(client)
    if not ready:
        launcher.ensure_started(client)
    if path == "__chef_start_status":
        return JSONResponse({"ready": ready, "failed": launcher.failed}, headers=headers)
    if not ready:
        headers["Retry-After"] = "3"
        if request.method == "GET" and "text/html" in request.headers.get("accept", ""):
            return HTMLResponse(WAIT, headers=headers)
        return JSONResponse({"error": "kitchen_starting", "retry_after": 3}, status_code=503, headers=headers)
    # raw_path/query preserve escaping; the destination host is always fixed.
    target = BACKEND + request.scope["raw_path"].decode("ascii")
    if request.url.query:
        target += "?" + request.url.query
    upstream = client.build_request(
        request.method, target,
        headers=[(k, v) for k, v in request.headers.items() if k.lower() not in HOP],
        content=request.stream(),
    )
    try:
        response = await client.send(upstream, stream=True)
    except httpx.HTTPError:
        return JSONResponse({"error": "kitchen_unavailable"}, status_code=503, headers=headers)
    outgoing = {k: v for k, v in response.headers.items() if k.lower() not in HOP}
    outgoing.update(headers)
    location = outgoing.get("location", "")
    if location.startswith(BACKEND + "/"):
        outgoing["location"] = location[len(BACKEND):]
    return StreamingResponse(response.aiter_raw(), status_code=response.status_code,
                             headers=outgoing, background=BackgroundTask(response.aclose))


if __name__ == "__main__":
    import uvicorn

    RUNTIME.mkdir(exist_ok=True)
    with (RUNTIME / "on-demand-connector.log").open("ab") as connector_log:
        subprocess.Popen(
            [sys.executable, str(ROOT / "scripts/cloudflare_keepalive.py"), "--watch"],
            cwd=ROOT, stdout=connector_log, stderr=connector_log, creationflags=HIDDEN,
        )
    uvicorn.run(app, host="127.0.0.1", port=8800, access_log=False)

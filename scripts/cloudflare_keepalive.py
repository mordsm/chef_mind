"""Repair the Chef tunnel origin while keeping the deployed workers.dev address fixed."""

import argparse
import json
import os
import re
import shutil
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".runtime"
STATE = RUNTIME / "cloudflare.json"
SYNCED = RUNTIME / "permanent-origin-synced.txt"
HIDDEN = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
PUBLIC = "https://chef-mind-gateway.chef-mind.workers.dev"
origin_failures = 0


def run(args, **kwargs):
    return subprocess.run(
        args,
        check=False,
        cwd=ROOT,
        creationflags=HIDDEN,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        **kwargs,
    )


def healthy(url):
    if not url or not (
        url in ("http://127.0.0.1:8800", PUBLIC) or re.fullmatch(r"https://[a-z0-9-]+\.trycloudflare\.com", url)
    ):
        return False
    result = run(
        [
            "node",
            "-e",
            "fetch(process.argv[1]+'/health',{signal:AbortSignal.timeout(7000)}).then(r=>r.json()).then(d=>process.exit(d.service==='chef-core'?0:1)).catch(()=>process.exit(1))",
            url,
        ],
        timeout=12,
    )
    if result.returncode == 0:
        return True
    if url.startswith("https://"):
        probe = run(
            [str(ROOT / ".venv/Scripts/python.exe"), str(ROOT / "scripts/check_remote_health.py"), url],
            timeout=30,
        )
        return probe.returncode == 0
    return False


def status(phase, **details):
    (RUNTIME / "cloudflare-watchdog.json").write_text(
        json.dumps(
            {"pid": os.getpid(), "phase": phase, "checked_at": datetime.now(UTC).isoformat(), **details}
        ),
        encoding="utf-8",
    )


def restart(state):
    old_pid = int(state.get("process_id", 0))
    if old_pid:
        # Verify identity and creation time in the same process before stopping anything.
        started = state.get("started_at", "")
        if not re.fullmatch(r"[0-9T:.+Z-]+", started):
            raise ValueError("Unrecognized old process creation time")
        script = f"$p=Get-Process -Id {old_pid} -ErrorAction SilentlyContinue;if($p){{if($p.ProcessName -ne 'cloudflared' -or $p.StartTime.ToUniversalTime().ToString('o') -ne '{started}'){{exit 2}};Stop-Process -Id {old_pid}}};exit 0"
        result = run(["powershell.exe", "-NoProfile", "-Command", script], timeout=10)
        if result.returncode:
            raise RuntimeError("Old connector ownership could not be verified")
    executable = shutil.which("cloudflared") or "C:/Program Files (x86)/cloudflared/cloudflared.exe"
    stamp = str(time.time_ns())
    out_path, err_path = RUNTIME / f"origin-{stamp}.out.log", RUNTIME / f"origin-{stamp}.err.log"
    with out_path.open("w") as out, err_path.open("w") as err:
        process = subprocess.Popen(
            [
                executable,
                "tunnel",
                "--no-autoupdate",
                "--protocol",
                "auto",
                "--edge-ip-version",
                "4",
                "--url",
                "http://127.0.0.1:8800",
            ],
            cwd=ROOT,
            stdout=out,
            stderr=err,
            creationflags=HIDDEN,
        )
    metadata = run(
        [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            f"$p=Get-Process -Id {process.pid};@{{process_id=$p.Id;executable=$p.Path;started_at=$p.StartTime.ToUniversalTime().ToString('o')}}|ConvertTo-Json -Compress",
        ],
        timeout=10,
    )
    state = {
        **json.loads(metadata.stdout),
        "origin": "http://127.0.0.1:8800",
        "url": "",
        "stdout_log": str(out_path),
        "stderr_log": str(err_path),
    }
    STATE.write_text(json.dumps(state), encoding="utf-8")
    deadline = time.monotonic() + 50
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Connector exited before becoming available")
        text = err_path.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", text)
        if match and "Registered tunnel connection" in text:
            state["url"] = match.group()
            STATE.write_text(json.dumps(state), encoding="utf-8")
            if healthy(state["url"]):
                return state
        time.sleep(2)
    raise RuntimeError("New origin did not pass its health check")


def synchronize(origin):
    choices = list((RUNTIME / "npm-cache/_npx").glob("*/node_modules/wrangler/bin/wrangler.js"))
    cli = next(
        (
            path
            for path in choices
            if json.loads((path.parent.parent / "package.json").read_text())["version"] == "4.152.0"
        ),
        None,
    )
    if not cli:
        raise RuntimeError("Install the pinned Wrangler CLI first")
    result = run(
        [
            "node",
            str(cli),
            "secret",
            "put",
            "CHEF_ORIGIN",
            "--config",
            str(ROOT / "infra/cloudflare-gateway/wrangler.jsonc"),
        ],
        input=origin + "\n",
        timeout=60,
    )
    if result.returncode:
        raise RuntimeError("Gateway update failed; Cloudflare authorization may need renewal")
    SYNCED.write_text(origin, encoding="ascii")


def cycle():
    global origin_failures
    if not healthy("http://127.0.0.1:8800"):
        status("waiting_for_local_chef")
        return
    state = json.loads(STATE.read_text(encoding="utf-8-sig")) if STATE.exists() else {}
    if not healthy(state.get("url")):
        origin_failures += 1
        if origin_failures < 2:
            status("confirming_origin_failure", consecutive_failures=origin_failures)
            return
        status("repairing_origin")
        state = restart(state)
    origin_failures = 0
    origin = state["url"]
    if not SYNCED.exists() or SYNCED.read_text().strip() != origin:
        synchronize(origin)
    if not healthy(PUBLIC):
        # A healthy connector alone does not prove the public Worker uses its URL.
        status("repairing_public_gateway", origin=origin)
        synchronize(origin)
        if not healthy(PUBLIC):
            status("waiting_for_public_gateway", origin=origin)
            return
    status("connected", origin=origin)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", action="store_true")
    args = parser.parse_args()
    RUNTIME.mkdir(exist_ok=True)
    os.environ["NODE_USE_SYSTEM_CA"] = "1"
    os.environ["XDG_CONFIG_HOME"] = str(RUNTIME / "cloudflare-config")
    os.environ["WRANGLER_SEND_METRICS"] = "false"
    # Only one keepalive process should manage this connector.
    with (RUNTIME / "cloudflare-watchdog.lock").open("a+b") as lock:
        if os.name == "nt":
            import msvcrt

            lock.seek(0)
            if not lock.read(1):
                lock.write(b"0")
                lock.flush()
            lock.seek(0)
            try:
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                raise SystemExit("A Chef Cloudflare keepalive is already running")
        while True:
            try:
                cycle()
            except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
                status("retrying", error_type=type(error).__name__)
                if not args.watch:
                    raise
            if not args.watch:
                break
            time.sleep(30)


if __name__ == "__main__":
    main()

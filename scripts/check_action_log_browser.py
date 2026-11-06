"""Real HTTP/PWA browser test with two isolated devices and actual IndexedDB/SW."""

import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
TOKEN = "pwa-browser-test-access-token-12345"


def serve(path, port):
    import uvicorn
    from app.config import Settings
    from app.db import Base, make_engine
    from app.main import create_app

    settings = Settings(
        _env_file=None,
        database_url="sqlite+pysqlite:///" + path,
        api_keys={TOKEN: {"user_id": "owner", "role": "cook"}},
        sync_enabled=False,
    )
    engine = make_engine(settings.database_url)
    Base.metadata.create_all(engine)
    uvicorn.run(create_app(settings, engine), host="127.0.0.1", port=int(port), log_level="error")


def check():
    from playwright.sync_api import expect, sync_playwright

    (ROOT / ".runtime").mkdir(exist_ok=True)
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    with tempfile.TemporaryDirectory(prefix="pwa-browser-", dir=ROOT / ".runtime", ignore_cleanup_errors=True) as temp:
        process = subprocess.Popen(
            [sys.executable, str(Path(__file__)), "--serve", str(Path(temp) / "test.sqlite"), str(port)],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        try:
            origin = f"http://127.0.0.1:{port}"
            for _ in range(80):
                try:
                    with socket.create_connection(("127.0.0.1", port), timeout=1) as probe:
                        probe.sendall(b"GET /health HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n")
                        if b"200 OK" not in probe.recv(512):
                            raise OSError("Test service not ready")
                    break
                except OSError:
                    if process.poll() is not None:
                        raise RuntimeError(process.stderr.read().decode(errors="replace")[-3000:])
                    time.sleep(0.2)
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(channel="msedge", headless=True)
                kitchen = browser.new_context(viewport={"width": 1440, "height": 1000})
                phone = browser.new_context(viewport={"width": 390, "height": 844})
                first, second = kitchen.new_page(), phone.new_page()
                errors = []
                for page in (first, second):
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.goto(origin + "/report/")
                    page.locator("#access-token").fill(TOKEN)
                    page.locator("#login button").click()
                    expect(page.locator("#workspace")).to_be_visible()
                    expect(page.locator("#identity")).to_contain_text("owner")
                    page.locator('#report-history summary').click()
                    expect(page.locator('[data-action="cook"]')).to_be_enabled()
                    expect(page.locator("#session option")).to_have_count(1)
                    page.wait_for_function("""async () => {const s=await import('/assets/report/storage.js');return (await s.all('sessions','owner')).length>0&&(await s.all('sessions','owner')).every(item=>!item.pending);}""")
                assert first.locator("#session").input_value() == second.locator("#session").input_value()

                # Three configured forms, numeric controls, parallel timers and live sync.
                first.locator('[data-action="cook"]').click()
                first.locator("#number-duration").fill("1")
                first.locator("#save-report").click()
                expect(first.locator(".timer")).to_have_count(1)
                expect(second.locator("#history li[data-report-id]")).to_have_count(1, timeout=10000)
                first.locator('[data-action="cook"]').click()
                first.locator("#number-duration").fill("5")
                first.locator("#save-report").click()
                expect(second.locator(".timer")).to_have_count(2, timeout=10000)
                first.locator('[data-action="cut"]').click()
                first.locator('[data-field="size"] button[data-value="fine"]').click()
                first.locator("#save-report").click()
                expect(second.locator("#history li[data-report-id]")).to_have_count(3, timeout=10000)
                cut_id = (
                    second.locator("#history li").filter(has_text="לחתוך").get_attribute("data-report-id")
                )
                cut_first = first.locator(f'[data-report-id="{cut_id}"]')
                cut_second = second.locator(f'[data-report-id="{cut_id}"]')

                # An offline edit conflicts with a concurrent edit, preserving both.
                phone.set_offline(True)
                cut_second.get_by_role("button", name="עריכה", exact=True).click()
                second.locator('.report-notes summary').click()
                second.locator("#notes").fill("local offline observation")
                second.locator("#save-report").click()
                second.wait_for_function("""async id => {const s=await import('/assets/report/storage.js');const row=await s.read('entries',['owner',id]);return row?.pending&&row.notes==='local offline observation';}""", arg=cut_id)
                cut_first.get_by_role("button", name="עריכה", exact=True).click()
                first.locator('.report-notes summary').click()
                first.locator("#notes").fill("kitchen observation")
                first.locator("#save-report").click()
                first.wait_for_function("""async id => {const s=await import('/assets/report/storage.js');const row=await s.read('entries',['owner',id]);return row?.notes==='kitchen observation'&&!row.pending;}""", arg=cut_id)
                phone.set_offline(False)
                expect(cut_second).to_have_class("pending conflict", timeout=15000)
                expect(cut_second).to_contain_text("local offline observation")
                cut_second.get_by_role("button", name="קבל את גרסת השרת").click()
                expect(cut_second).to_contain_text("kitchen observation")

                # Offline create is sent automatically after reconnect, without retry click.
                phone.set_offline(True)
                second.locator('[data-action="add"]').click()
                second.locator('[data-field="quantity"] button[data-value="2"]').click()
                second.locator("#save-report").click()
                expect(second.locator("#history .pending")).to_have_count(1)
                phone.set_offline(False)
                expect(first.locator("#history li[data-report-id]")).to_have_count(4, timeout=15000)
                expect(second.locator("#history .pending")).to_have_count(0, timeout=15000)

                # Lose one successful server response; retry must not create duplicates.
                lost = {"once": True}

                def lose_response(route):
                    if lost["once"] and route.request.post_data_json.get("kind") == "put":
                        lost["once"] = False
                        route.fetch()
                        route.abort("failed")
                    else:
                        route.continue_()

                second.route("**/v1/action-log/mutations", lose_response)
                second.locator('[data-action="add"]').click()
                second.locator("#save-report").click()
                expect(first.locator("#history li[data-report-id]")).to_have_count(5, timeout=15000)
                expect(second.locator("#history .pending")).to_have_count(0, timeout=15000)
                second.unroute("**/v1/action-log/mutations", lose_response)
                assert first.locator("#history li[data-report-id]").count() == 5

                # Real SW offline navigation and IndexedDB recovery after page destruction.
                second.evaluate("() => navigator.serviceWorker.ready")
                expect(second.locator("#status")).not_to_contain_text("טוען")
                phone.set_offline(True)
                second.reload()
                expect(second.locator("#history li[data-report-id]")).to_have_count(5)
                expect(second.locator(".timer")).to_have_count(2)
                second.locator('[data-action="cut"]').click()
                second.locator("#save-report").click()
                expect(second.locator("#history .pending")).to_have_count(1)
                phone.set_offline(False)
                second.locator("#access-token").fill(TOKEN)
                second.locator("#login button").click()
                expect(first.locator("#history li[data-report-id]")).to_have_count(6, timeout=15000)

                # Deletion syncs and timer deadlines survive refresh / virtual elapsed time.
                first.once("dialog", lambda dialog: dialog.accept())
                cut_first.get_by_role("button", name="מחיקה", exact=True).click()
                expect(second.locator(f'[data-report-id="{cut_id}"]')).to_have_count(0, timeout=15000)
                first.clock.install()
                first.clock.fast_forward(61000)
                expect(first.locator(".timer.expired")).to_have_count(1)
                expect(first.locator(".timer")).to_have_count(2)
                for width in (390, 900, 1440):
                    first.set_viewport_size({"width": width, "height": 900})
                    if first.locator('dialog[open]').count():
                        first.keyboard.press('Escape')
                    expect(first.locator('[data-action="cook"]')).to_be_visible()
                    assert first.evaluate("document.documentElement.scrollWidth <= innerWidth"), width
                    assert first.locator('[data-action="cook"]').bounding_box()["height"] >= 48
                saved = second.evaluate(
                    """async () => {const s=await import('/assets/report/storage.js');return JSON.stringify([await s.all('entries','owner'),await s.pending('owner'),await s.meta('last-owner')]);}"""
                )
                assert TOKEN not in saved
                assert not errors, errors
                browser.close()
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            process.stderr.close()
    print(
        "Passed: two-device live sync, configurable forms, offline outbox/reconnect, lost-response deduplication, conflict resolution, offline PWA reload, parallel timers, deletion, responsive touch sizes and no stored token."
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        serve(sys.argv[2], sys.argv[3])
    else:
        check()

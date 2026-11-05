"""Station acceptance offline, or against a live URL in an isolated guest browser."""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.config import Settings
from app.db import Base, make_engine
from app.main import create_app
from app.station_protocol import configuration
from fastapi.testclient import TestClient
from playwright.sync_api import expect, sync_playwright


def main(live_url=None):
    settings = Settings(
        _env_file=None,
        database_url="sqlite+pysqlite:///:memory:",
        sync_enabled=False,
        dish_model_provider="disabled",
        model_enabled=False,
    )
    engine = make_engine(settings.database_url)
    Base.metadata.create_all(engine)
    states, errors = [], []
    with TestClient(create_app(settings, engine)) as client, sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        try:
            for width in (1440, 390):
                page = browser.new_page(viewport={"width": width, "height": 1000}, accept_downloads=True)
                page.on("pageerror", lambda error: errors.append(str(error)))

                def serve(route):
                    request = route.request
                    if urlsplit(request.url).netloc != "127.0.0.1:8800":
                        route.abort()
                        return
                    response = client.request(
                        request.method,
                        urlsplit(request.url).path,
                        headers={k: v for k, v in request.headers.items() if k == "content-type"},
                        content=request.post_data,
                    )
                    if urlsplit(request.url).path == "/v1/coach/preview" and response.status_code == 200:
                        states.append(response.json())
                    route.fulfill(
                        status=response.status_code,
                        body=response.content,
                        headers={
                            k: v
                            for k, v in response.headers.items()
                            if k not in ("content-length", "transfer-encoding")
                        },
                    )

                if live_url:
                    def capture(response):
                        if urlsplit(response.url).path == "/v1/coach/preview" and response.status == 200:
                            states.append(response.json())

                    page.on("response", capture)
                else:
                    page.route("**/*", serve)
                page.goto(live_url or "http://127.0.0.1:8800/", timeout=45000)
                page.locator("#custom-dish-title").fill("נסיכת הנילוס")
                page.locator("#start-work").click()
                dock = page.locator("#active-work-guidance .station-protocol")
                expect(dock.locator(".station-block")).to_have_count(6)
                expect(dock).to_contain_text("geosmin")
                expect(dock).to_contain_text("Chenin Blanc")
                expect(dock).to_contain_text("Anjou")
                expect(dock).to_contain_text("[[Nile Perch]]")
                expect(dock).to_contain_text("#culinary/ingredient/freshwater-fish")
                expect(dock).to_contain_text("Knowledge Base Extension Needed")
                expect(dock).to_contain_text("215–217")
                science_details = dock.locator('[data-station-block="3"] details')
                expect(science_details).not_to_have_attribute("open", "")
                expect(dock.locator('[data-station-block="6"]')).to_contain_text("אין צורך להוסיף אותו שוב")
                expect(dock.locator('[data-station-block="6"] details')).not_to_have_attribute("open", "")
                expect(dock.locator('[data-station-block="1"]')).not_to_contain_text("טיפול אופציונלי")
                expect(dock.locator('[data-station-block="2"]')).not_to_contain_text("UNKNOWN")
                expect(dock.locator('[data-station-block="2"]')).to_contain_text("זה אינו זמן הבישול הכולל")
                expect(dock.locator('[data-station-block="2"]')).to_contain_text("ולא מספר בכפתור הכיריים")
                expect(dock.locator('[data-station-block="4"]')).to_contain_text("פירורי לחם")
                expect(dock.locator('[data-station-block="4"]')).to_contain_text("אין הכוונה לשפוך אותם לרוטב")
                expect(dock.locator('[data-station-block="6"] a').first).to_be_visible()
                expect(dock.locator('[data-station-block="2"]')).to_contain_text("5–8 דקות")
                expect(dock.locator('[data-station-block="1"]')).to_contain_text("בהכנה הזו אין צורך בהשריה")
                expect(dock.locator('[data-station-block="4"]')).to_contain_text("חסר מלח?")
                background = dock.locator('[data-station-block="6"] details')
                background.locator("summary").click()
                term = background.get_by_role("button", name="הסבר: HACCP", exact=True)
                term.click()
                dictionary = page.locator("#culinary-glossary-dialog")
                expect(dictionary).to_be_visible()
                expect(dictionary).to_contain_text("מודדים חום במרכז הדג")
                page.keyboard.press("Escape")
                expect(dictionary).not_to_be_visible()
                expect(term).to_be_focused()
                background.locator("summary").click()
                page.locator("#culinary-glossary-open").click()
                expect(dictionary).to_contain_text("שליקה")
                dictionary.get_by_role("button", name="סגור הסבר").click()
                science_details.locator("summary").click()
                expect(science_details.locator("p")).to_be_visible()
                science_details.locator("summary").click()
                if configuration()["fish_safety"]["approval_status"] == "APPROVED":
                    expect(dock).to_contain_text("63°C")
                    expect(dock).to_contain_text("15 שניות")
                else:
                    expect(dock).to_contain_text("ממתין לאישור")
                family_page = page.locator(".intake-page").filter(has=page.locator("#intake-family"))
                if not family_page.evaluate("node => node.open"):
                    family_page.locator("summary").click()
                fish = family_page.get_by_role("button", name="דגים", exact=True)
                if fish.get_attribute("aria-pressed") == "true":
                    fish.click()
                fish.click()
                page.locator("#cooking-intake-form button[type=submit]").click()
                page.wait_for_function("() => mentor.state.revision >= 2")
                expect(page.locator(".intake-saved")).to_have_count(0)
                expect(page.locator("#intake-save-result")).not_to_contain_text("63°C")
                expect(dock.locator(".station-block")).to_have_count(6)
                editor = page.locator(".voice-question-editor")
                if editor.count() and not editor.evaluate("node => node.open"):
                    editor.locator("summary").click()
                page.locator("#work-report").fill("איך להכין את נסיכת הנילוס?")
                page.locator("#user-report-form button[type=submit]").click()
                page.wait_for_function("() => mentor.state.revision >= 3")
                expect(dock.locator(".station-block")).to_have_count(6)
                expect(dock).to_contain_text("עובי")
                with page.expect_download() as downloaded:
                    dock.get_by_role("button", name="ייצוא פתק Obsidian").click()
                destination = ROOT / ".runtime" / f"station-acceptance-{width}.md"
                downloaded.value.save_as(destination)
                assert "type: culinary-station-log" in destination.read_text(encoding="utf-8")
                page.evaluate("protocol => renderDecision({station_protocol:protocol})", states[-1]["station_protocol"])
                expect(page.locator("#decision .station-block")).to_have_count(6)
                page.close()
        finally:
            browser.close()
    assert not errors, errors
    model_statuses = {s["dish_identity"]["status"] for s in states}
    if not live_url:
        assert model_statuses == {"disabled"}
    assert any(s["revision"] >= 3 for s in states)
    print(
        json.dumps(
            {
                "passed": True,
                "widths": [1440, 390],
                "model": sorted(model_statuses),
                "live_url": live_url,
                "six_blocks": True,
                "obsidian_download": True,
                "core_approval": configuration()["fish_safety"]["approval_status"],
            }
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Live Chef URL; uses guest preview without saving server data")
    main(parser.parse_args().url)
